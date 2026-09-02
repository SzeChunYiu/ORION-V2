#!/usr/bin/env python3
"""E30-R12 analysis: registered endpoints, dispositions, gates and routing.

Implements sections 5, 6, 7, 9 and 10 of ``E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1``.
Reads only the full-regression rollup, the GR0 receipt and the campaign's response
envelopes; it computes no test and reads no gate until GR0 is asserted PASS.

All statistics are delegated to ``scripts/analyze_orion_real_problem_results.py``, the
E30-freeze-pinned analyzer (``E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1.json``), so the
paired tables, the exact discordant test, the PROJECT-stratified bootstrap and Holm are
literally the same code the programme's other confirmatory cells used.

Endpoints (design section 5)
  E1  registered_failing_test_fixed      -- primary, denominator 40 (+39 sensitivity)
  E2  any_critical_new_failure           -- co-primary, non-inferiority margin 0.02
  D1  patch_apply_rate                   -- registered diagnostic, per evaluation

Two independent Holm families of three, one per endpoint (design section 5, statistics).
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DESIGN_ID = "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1"
SCHEMA = "orion.v2.e30-r12-analysis.v1"
SEED = 20260902
BOOTSTRAP_DRAWS = 10000
CELL_NAME = "e30r12"
LEFT_ARM = "F2_ORION_METABOLIC_FULL"
RIGHT_ARMS = ["F0_PARENT_FEDERATION", "SIMPLE_DIRECT", "SAME_MODEL_REFLECTION"]
ALPHA = 0.05
NON_INFERIORITY_MARGIN = 0.02          # analysis plan section 7, fixed pre-outcome
APPLY_FAIL_CEILING = 0.40              # design section 5, D1
PC_R6_APPLY_FAIL_COMPARATOR = {        # design section 5, D1 historical comparator
    "F2_ORION_METABOLIC_FULL": 0.8167,
    "F0_PARENT_FEDERATION": 0.8000,
    "SAME_MODEL_REFLECTION": 0.8083,
    "SIMPLE_DIRECT": 0.7833,
}
# Design section 6.  Keyed to machine-detected baseline condition codes, never to names.
E2_EXCLUDING_BASELINE_STATUSES = {"BASELINE_SUITE_NO_PASSING_TESTS"}
E1_SENSITIVITY_CONDITION = "REGISTERED_TEST_UNFIXABLE_BY_SOURCE_ONLY_PATCH"
# The GR0b gold control marks a task whose registered test no source-only patch can flip
# (the fixed commit adds a fixture the frozen checkout never copies).  That is the
# machine-detectable form of the third registered disposition: it is read from R12's own
# GR0b receipt, never assumed from PC-R6's finding.
GOLD_NOT_APPLICABLE_PREFIX = "GOLD_NOT_APPLICABLE_MISSING_FIXTURE"


class AnalysisRefused(RuntimeError):
    """A precondition of the registered analysis is not met; no gate may be read."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AnalysisRefused(f"cannot import {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------- preconditions
def require_gr0(path: Path) -> dict[str, Any]:
    """GR0a and GR0b must both be PASS before any endpoint is touched."""
    if not path.is_file():
        raise AnalysisRefused(f"GR0 receipt missing: {path}")
    receipt = json.loads(path.read_text())
    if receipt.get("gr0_status") != "PASS":
        raise AnalysisRefused(f"GR0 receipt status is {receipt.get('gr0_status')!r}, not PASS")
    components = receipt.get("components", {})
    for name in ("PC_R6_GR0A_RECEIPT.json", "PC_R6_GR0B_RECEIPT.json"):
        if components.get(name, {}).get("status") != "PASS":
            raise AnalysisRefused(f"GR0 component {name} is not PASS")
    return receipt


def served_model_homogeneity(campaign: Path, arms: list[str], reps: list[str],
                             task_ids: list[str], expected: str) -> dict[str, Any]:
    """GR0c: every envelope records exactly one served id, and all are identical."""
    observed: dict[str, int] = {}
    offenders: list[dict[str, Any]] = []
    envelopes = 0
    for rep in reps:
        for arm in arms:
            for task_id in task_ids:
                path = campaign / "run" / f"confirmatory-r{rep}" / "responses" / arm / f"{task_id}.json"
                if not path.is_file():
                    offenders.append({"rep": rep, "arm": arm, "task_id": task_id,
                                      "reason": "RESPONSE_MISSING"})
                    continue
                envelopes += 1
                ids = (json.loads(path.read_text()).get("resource_receipt") or {}).get("served_model_ids")
                if not isinstance(ids, list) or len(ids) != 1:
                    offenders.append({"rep": rep, "arm": arm, "task_id": task_id,
                                      "reason": "SERVED_MODEL_IDS_NOT_A_SINGLETON",
                                      "observed": ids})
                    continue
                served = str(ids[0])
                observed[served] = observed.get(served, 0) + 1
                if expected and served != expected:
                    offenders.append({"rep": rep, "arm": arm, "task_id": task_id,
                                      "reason": "SERVED_MODEL_MISMATCH", "observed": served})
    return {
        "gate_id": "GR0c", "name": "SERVED_MODEL_HOMOGENEITY",
        "expected_served_model": expected,
        "envelopes_read": envelopes,
        "served_model_counts": observed,
        "offenders": offenders[:50],
        "offender_count": len(offenders),
        "status": "PASS" if (envelopes and not offenders and len(observed) == 1) else "FAIL",
    }


# ------------------------------------------------------------------------ endpoints
def e1_sensitivity_exclusions(gr0b_path: Path | None) -> list[str]:
    """Tasks the GR0b gold control proved unfixable by any source-only patch."""
    if gr0b_path is None or not gr0b_path.is_file():
        return []
    receipt = json.loads(gr0b_path.read_text())
    excluded = set()
    for item in list(receipt.get("not_applicable", [])) + list(receipt.get("tasks", [])):
        if str(item.get("gold_control_status", "")).startswith(GOLD_NOT_APPLICABLE_PREFIX):
            excluded.add(str(item["task_id"]))
    return sorted(excluded)


def _majority(analyzer, values: list[bool | None]) -> bool | None:
    return analyzer.frozen_majority(values)


def build_tables(cell: dict[str, Any], analyzer) -> dict[str, Any]:
    """Per-arm task tables for E1 and E2, plus the per-arm D1 diagnostic."""
    reps = [f"r{rep}" for rep in cell["reps"]]
    projects = cell.get("task_projects", {})
    baselines = cell.get("baselines", {})
    e2_excluded = sorted(
        task_id for task_id, item in baselines.items()
        if str(item.get("status")) in E2_EXCLUDING_BASELINE_STATUSES
    )
    e1_tables: dict[str, dict[str, dict[str, Any]]] = {}
    e2_tables: dict[str, dict[str, dict[str, Any]]] = {}
    per_arm: dict[str, Any] = {}
    for arm in cell["arms"]:
        e1_tables[arm], e2_tables[arm] = {}, {}
        e1_true = e1_checkable = 0
        e2_true = e2_checkable = 0
        e1_instability = 0
        for task_id in cell["task_ids"]:
            entries = cell["evaluations"].get(f"{arm}/{task_id}", {})
            e1_values: list[bool | None] = []
            e2_values: list[bool | None] = []
            for rep in reps:
                entry = entries.get(rep, {"status": "MISSING"})
                native = entry.get("native_success")
                e1_values.append(bool(native) if isinstance(native, bool) else None)
                count = entry.get("critical_new_failure_count")
                e2_values.append(None if count is None else int(count) > 0)
            base = {"task_id": task_id, "arm_id": arm,
                    "project": projects.get(task_id, "UNKNOWN")}
            e1_aggregate = _majority(analyzer, e1_values)
            e1_tables[arm][task_id] = {**base, "_aggregate_success": e1_aggregate,
                                       "_rep_values": e1_values}
            if e1_aggregate is not None:
                e1_checkable += 1
                e1_true += e1_aggregate is True
            e1_instability += len({v for v in e1_values if v is not None}) > 1
            if task_id in e2_excluded:
                continue                                  # design section 6, excluded with count
            e2_aggregate = _majority(analyzer, e2_values)
            e2_tables[arm][task_id] = {**base, "_aggregate_critical_failure": e2_aggregate,
                                       "_rep_values": e2_values}
            if e2_aggregate is not None:
                e2_checkable += 1
                e2_true += e2_aggregate is True
        totals = cell["arm_totals"].get(arm, {})
        evaluations = int(totals.get("evaluations") or 0)
        applied = int(totals.get("patch_applied") or 0)
        apply_fail_rate = totals.get("patch_apply_failure_rate")
        comparator = PC_R6_APPLY_FAIL_COMPARATOR.get(arm)
        per_arm[arm] = {
            "E1_tasks_checkable": e1_checkable,
            "E1_tasks_success": e1_true,
            "E1_rate": (e1_true / e1_checkable) if e1_checkable else None,
            "E1_rate_exact_ci95": analyzer.exact_binomial_interval(e1_true, e1_checkable),
            "E1_rep_instability_task_count": e1_instability,
            "E2_tasks_checkable": e2_checkable,
            "E2_tasks_any_critical_new_failure": e2_true,
            "E2_rate": (e2_true / e2_checkable) if e2_checkable else None,
            "D1_evaluations": evaluations,
            "D1_patch_applied": applied,
            "D1_patch_apply_rate": (applied / evaluations) if evaluations else None,
            "D1_patch_apply_rate_exact_ci95": analyzer.exact_binomial_interval(applied, evaluations),
            "D1_patch_apply_failure_rate": apply_fail_rate,
            "D1_pc_r6_comparator_failure_rate": comparator,
            "D1_below_comparator": (
                None if apply_fail_rate is None or comparator is None
                else bool(apply_fail_rate < comparator)),
            "D1_below_registered_ceiling": (
                None if apply_fail_rate is None else bool(apply_fail_rate < APPLY_FAIL_CEILING)),
            "compile_failure_rate": totals.get("compile_failure_rate"),
            "none_reasons_per_evaluation": totals.get("none_reasons"),
        }
    return {"E1": e1_tables, "E2": e2_tables, "per_arm": per_arm,
            "E2_excluded_task_ids": e2_excluded,
            "E2_exclusion_rule": sorted(E2_EXCLUDING_BASELINE_STATUSES)}


def family(analyzer, tables: dict[str, dict[str, dict[str, Any]]], extractor,
           orientation: str) -> list[dict[str, Any]]:
    """The three registered F2-vs-control contrasts, Holm-adjusted within the family."""
    contrasts = []
    for right in RIGHT_ARMS:
        block = analyzer.paired_binary_comparison(tables[LEFT_ARM], tables[right], extractor)
        table = block["paired_table"]
        ci = block["risk_difference"]["ci95"]
        block.update({
            "left_arm": LEFT_ARM, "right_arm": right,
            "risk_difference_orientation": f"{LEFT_ARM} - {right} ({orientation})",
            "discordant_count": table["left_only"] + table["right_only"],
            "one_sided_97_5_upper_bound": ci[1],
            "one_sided_97_5_lower_bound": ci[0],
            "ci95_excludes_zero": bool(ci[0] is not None and ci[1] is not None
                                       and (ci[0] > 0 or ci[1] < 0)),
        })
        contrasts.append(block)
    # holm_adjust operates on {"success": block} wrappers and writes the adjusted p and
    # the rejection flag back into each block (PC-R6 convention, verbatim).
    analyzer.holm_adjust([{"success": block} for block in contrasts], alpha=ALPHA)
    for block in contrasts:
        block["holm_p"] = block.get("holm_adjusted_p")
        block["holm_reject"] = bool(block.get("holm_reject_at_alpha_0_05"))
    return contrasts


# ---------------------------------------------------------------------------- gates
def evaluate_gates(per_arm: dict[str, Any], e1: list[dict[str, Any]],
                   e2: list[dict[str, Any]], gr0c: dict[str, Any]) -> dict[str, Any]:
    apply_ok = all(bool(item["D1_below_registered_ceiling"]) and bool(item["D1_below_comparator"])
                   for item in per_arm.values())
    gr1 = {"gate_id": "GR1", "name": "APPLY_RATE_DIAGNOSTIC",
           "status": "PASS" if apply_ok else "FAIL",
           "registered_ceiling_failure_rate": APPLY_FAIL_CEILING,
           "per_arm": {arm: {"patch_apply_failure_rate": item["D1_patch_apply_failure_rate"],
                             "pc_r6_comparator": item["D1_pc_r6_comparator_failure_rate"],
                             "below_ceiling": item["D1_below_registered_ceiling"],
                             "below_comparator": item["D1_below_comparator"]}
                       for arm, item in per_arm.items()}}
    rejected = [c for c in e1 if c.get("holm_reject") is True]
    gr2 = {"gate_id": "GR2", "name": "PRIMARY_SEPARATION",
           "status": "REJECT" if rejected else "NULL",
           "rejected_contrasts": [c["right_arm"] for c in rejected],
           "direction": ("F2_FAVOURED"
                         if rejected and all((c["risk_difference"]["estimate"] or 0) > 0 for c in rejected)
                         else "F2_DISFAVOURED" if rejected else None)}
    f0 = next((c for c in e2 if c["right_arm"] == "F0_PARENT_FEDERATION"), None)
    upper = f0["one_sided_97_5_upper_bound"] if f0 else None
    gr3 = {"gate_id": "GR3", "name": "CRITICAL_NON_INFERIORITY",
           "margin": NON_INFERIORITY_MARGIN,
           "risk_difference": (f0 or {}).get("risk_difference", {}).get("estimate"),
           "one_sided_97_5_upper_bound": upper,
           "checkable_paired_tasks": (f0 or {}).get("checkable_task_count"),
           "status": ("CANNOT_CHECK" if upper is None
                      else "PASS" if upper <= NON_INFERIORITY_MARGIN else "FAIL")}
    return {"GR0c": gr0c, "GR1": gr1, "GR2": gr2, "GR3": gr3}


def route(gates: dict[str, Any], per_arm: dict[str, Any]) -> dict[str, str]:
    """Design section 11, evaluated in the registered order."""
    if gates["GR0c"]["status"] != "PASS":
        return {"terminal": "LANE_DEFECT",
                "detail": "GR0c served-model homogeneity failed; no endpoint may be read"}
    if gates["GR2"]["status"] == "REJECT" and gates["GR2"]["direction"] == "F2_DISFAVOURED":
        return {"terminal": "F2_HARMFUL",
                "detail": "a primary contrast rejects against F2; reported as plainly as a positive"}
    if gates["GR3"]["status"] == "FAIL":
        return {"terminal": "CRITICAL_REGRESSION",
                "detail": "non-compensatory: no F2 advantage of any size may be claimed"}
    if gates["GR1"]["status"] == "FAIL":
        return {"terminal": "INTERFACE_STILL_BROKEN",
                "detail": ("emission-side canonicalization did not materially raise the apply "
                           "rate; E1/E2 are reported with the measured apply rate attached and "
                           "the study does not claim to have tested repair")}
    if gates["GR2"]["status"] == "REJECT" and gates["GR3"]["status"] == "PASS":
        return {"terminal": "FIRST_REGISTERED_POSITIVE",
                "detail": "requires independent replication under a new identity before any paper claim"}
    f2 = per_arm.get(LEFT_ARM, {}).get("E1_rate")
    f0 = per_arm.get("F0_PARENT_FEDERATION", {}).get("E1_rate")
    if f2 is not None and f0 is not None and f0 >= f2:
        return {"terminal": "PARENT_SUFFICIENT",
                "detail": ("the strongest native parent is at or above F2 on the primary endpoint; "
                           "a valid terminal that closes the F2-superiority line on real debugging")}
    return {"terminal": "NO_ARM_SEPARATION",
            "detail": ("no separation under a working interface, tail-safe at the registered "
                       "margin; an expected and legitimate terminal, not a failed study")}


# --------------------------------------------------------------------------- render
def _fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def render_markdown(result: dict[str, Any]) -> str:
    per_arm = result["per_arm"]
    lines = [
        f"# E30-R12 rollup (V1)",
        "",
        f"Analysis `{SCHEMA}` over rollup `{result['inputs']['rollup_sha256'][:12]}…` "
        f"(GR0 receipt `{result['inputs']['gr0_sha256'][:12]}…`, design "
        f"`{result['inputs']['design_sha256'][:12]}…`, generated {result['generated_utc']}).",
        "",
        "Seed 20260902; bootstrap 10000 draws, PROJECT-stratified; two independent Holm "
        "families of three, one per endpoint. No imputation.",
        "",
        "## Per-arm endpoints and the apply-rate diagnostic",
        "",
        "| arm | E1 success / checkable | E1 rate | E2 any-critical / checkable | D1 apply rate | D1 apply-fail | PC-R6 comparator |",
        "|---|---|---|---|---|---|---|",
    ]
    for arm in [LEFT_ARM] + RIGHT_ARMS:
        item = per_arm.get(arm, {})
        lines.append(
            f"| `{arm}` | {item.get('E1_tasks_success')}/{item.get('E1_tasks_checkable')} | "
            f"{_fmt(item.get('E1_rate'), 3)} | "
            f"{item.get('E2_tasks_any_critical_new_failure')}/{item.get('E2_tasks_checkable')} | "
            f"{_fmt(item.get('D1_patch_apply_rate'), 4)} | "
            f"{_fmt(item.get('D1_patch_apply_failure_rate'), 4)} | "
            f"{_fmt(item.get('D1_pc_r6_comparator_failure_rate'), 4)} |")
    for label, key in (("E1 — registered failing test fixed (primary)", "E1_contrasts"),
                       ("E1 — sensitivity denominator "
                        f"({result['denominators']['E1_sensitivity']} tasks, "
                        f"excluding {result['E1_sensitivity_excluded_task_ids'] or 'none'})",
                        "E1_sensitivity_contrasts"),
                       ("E2 — any critical new failure (co-primary)", "E2_contrasts")):
        lines += ["", f"## {label}", "",
                  "| contrast | paired (bothF/bothT/L-only/R-only) | checkable | RD [CI95] | exact p | Holm p | reject |",
                  "|---|---|---|---|---|---|---|"]
        for block in result[key]:
            t = block["paired_table"]
            rd = block["risk_difference"]
            lines.append(
                f"| {block['left_arm']} − {block['right_arm']} | "
                f"{t['both_false']}/{t['both_true']}/{t['left_only']}/{t['right_only']} | "
                f"{block['checkable_task_count']} | {_fmt(rd['estimate'])} "
                f"[{_fmt(rd['ci95'][0])}, {_fmt(rd['ci95'][1])}] | "
                f"{_fmt(block.get('exact_discordant_p'))} | {_fmt(block.get('holm_p'))} | "
                f"{_fmt(block.get('holm_reject'))} |")
    lines += ["", "## Gates", "", "| gate | status | detail |", "|---|---|---|"]
    for gate_id in ("GR0c", "GR1", "GR2", "GR3"):
        gate = result["gates"][gate_id]
        detail = {"GR0c": f"{gate.get('envelopes_read')} envelopes, "
                          f"{gate.get('offender_count')} offenders, ids {gate.get('served_model_counts')}",
                  "GR1": f"all arms below {APPLY_FAIL_CEILING} apply-fail and below the PC-R6 comparator: "
                         f"{gate['status'] == 'PASS'}",
                  "GR2": f"rejected: {gate.get('rejected_contrasts') or 'none'}",
                  "GR3": f"RD={_fmt(gate.get('risk_difference'))}, upper={_fmt(gate.get('one_sided_97_5_upper_bound'))}, "
                         f"n={gate.get('checkable_paired_tasks')}, margin {NON_INFERIORITY_MARGIN}"}[gate_id]
        lines.append(f"| {gate_id} {gate['name']} | **{gate['status']}** | {detail} |")
    lines += ["", "## Dispositions applied (registered pre-dispatch, design section 6)", "",
              f"- E2 excluded with count under `{', '.join(result['E2_exclusion_rule'])}`: "
              f"{result['E2_excluded_task_ids'] or 'none'}",
              f"- E1 denominator {result['denominators']['E1']}; "
              f"E1 sensitivity denominator {result['denominators']['E1_sensitivity']}; "
              f"E2 denominator {result['denominators']['E2']}",
              "", "## Pre-registered routing", "",
              f"**{result['routing']['terminal']}** — {result['routing']['detail']}",
              "", "## Power boundary (registered pre-dispatch, design section 7)", "",
              "At n = 40 the exact test cannot reject unless at least 7 tasks are discordant in "
              "the same direction (risk difference ≥ 0.175). Power against the registered "
              "5-percentage-point minimum important difference is 1–2%. A non-rejection here is "
              "NOT evidence of equivalence.", ""]
    return "\n".join(lines)


# ----------------------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rollup", type=Path, required=True)
    parser.add_argument("--gr0", type=Path, required=True)
    parser.add_argument("--gr0b", type=Path,
                        help="GR0b receipt; supplies the machine-detected E1 sensitivity "
                             "exclusions (design section 6, third condition)")
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--analyzer", type=Path, required=True,
                        help="scripts/analyze_orion_real_problem_results.py")
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--served-model", default="glm-5.3")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        gr0 = require_gr0(args.gr0)               # asserted BEFORE any endpoint is read
    except AnalysisRefused as exc:
        print(f"ANALYSIS_REFUSED: {exc}", file=sys.stderr)
        return 3
    analyzer = load_module("orion_real_problem_analyzer", args.analyzer)
    # Pin the registered bootstrap identity (design section 5): 10000 draws, seed 20260902.
    # The pinned analyzer's own default seed is a different study's; binding it here keeps
    # the frozen file byte-unchanged while making R12's interval reproducible.
    original_bootstrap = analyzer.paired_bootstrap_difference
    analyzer.paired_bootstrap_difference = functools.partial(
        original_bootstrap, repetitions=BOOTSTRAP_DRAWS, seed=SEED)
    rollup = json.loads(args.rollup.read_text())
    cell = rollup["cells"][CELL_NAME]

    gr0c = served_model_homogeneity(args.campaign, cell["arms"], cell["reps"],
                                    cell["task_ids"], args.served_model)
    tables = build_tables(cell, analyzer)
    e1 = family(analyzer, tables["E1"], analyzer.success, "E1 success")
    excluded = e1_sensitivity_exclusions(args.gr0b)
    e1_sensitivity_tables = {
        arm: {task_id: item for task_id, item in table.items() if task_id not in excluded}
        for arm, table in tables["E1"].items()}
    e1_sensitivity = family(analyzer, e1_sensitivity_tables, analyzer.success,
                            "E1 success, sensitivity denominator")
    e2 = family(analyzer, tables["E2"], analyzer.critical_failure, "E2 critical failure")
    gates = evaluate_gates(tables["per_arm"], e1, e2, gr0c)
    routing = route(gates, tables["per_arm"])

    result = {
        "schema_version": SCHEMA, "design": DESIGN_ID, "seed": SEED,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "bootstrap_draws": BOOTSTRAP_DRAWS, "stratification": "PROJECT",
        "inputs": {
            "rollup_sha256": sha256_file(args.rollup),
            "gr0_sha256": sha256_file(args.gr0),
            "design_sha256": sha256_file(args.design),
            "analyzer_sha256": sha256_file(args.analyzer),
            "campaign": str(args.campaign),
            "gr0_status": gr0.get("status"),
        },
        "per_arm": tables["per_arm"],
        "E1_contrasts": e1,
        "E1_sensitivity_contrasts": e1_sensitivity,
        "E1_sensitivity_excluded_task_ids": excluded,
        "E2_contrasts": e2,
        "E2_excluded_task_ids": tables["E2_excluded_task_ids"],
        "E2_exclusion_rule": tables["E2_exclusion_rule"],
        "E1_sensitivity_condition": E1_SENSITIVITY_CONDITION,
        "denominators": {
            "E1": len(cell["task_ids"]),
            "E1_sensitivity": len(cell["task_ids"]) - len(excluded),
            "E2": len(cell["task_ids"]) - len(tables["E2_excluded_task_ids"]),
        },
        "gates": gates,
        "routing": routing,
        "no_rescue_clause": (
            "E30-R11, E60 and PC-R6 endpoints are frozen terminal; nothing here revises, "
            "re-scores or reinterprets them, and the apply-rate diagnostic may not be used "
            "to re-read E30-R11's null."),
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "grants_publication_readiness": False},
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "E30_R12_ROLLUP_V1.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (args.out / "E30_R12_ROLLUP_V1.md").write_text(render_markdown(result) + "\n")
    print(json.dumps({"routing": routing["terminal"],
                      "gates": {k: v["status"] for k, v in gates.items()}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
