#!/usr/bin/env python3
"""PC-R6 analysis layer: design section 4 verbatim, gates section 5, routing section 6.

Refuses to run unless `PC_R6_GR0_RECEIPT.json` reports `gr0_status == "PASS"`
(GR0 discipline: nothing evaluates on an invalid lane).

Statistics are executed by IMPORTING the frozen analyzer
(`scripts/analyze_orion_real_problem_results.py`, the E60 code path):
`frozen_majority`, `paired_binary_comparison` (paired table, exact two-sided
discordant test, Clopper-Pearson interval), `paired_bootstrap_difference`
(10,000 draws, TASK unit, PROJECT-stratified) re-seeded to the registered
20260902, and `holm_adjust` (step-down within each cell's pre-registered
family).  The analysis layer is authoritative for `None` handling: an
evaluation without a count stays `None`, the task-level majority keeps it in
the denominator (`frozen_majority`), and a task whose aggregate is `None` in
either arm is excluded from that contrast's risk-difference denominator and
listed in `missing_task_ids` -- no imputation anywhere.

No mean-success quantity is computed here (no-rescue clause, design section 7).
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SEED = 20260902
BOOTSTRAP_DRAWS = 10000
NON_INFERIORITY_MARGIN = 0.02
NECESSITY_MARGIN = 0.02
EXACT_DISCORDANT_MAX = 10
ANALYSIS_VERSION = "orion.v2.pc-r6-fullreg-analysis.v1"
DESIGN_ID = "PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1"

CELL_FAMILIES: dict[str, dict[str, Any]] = {
    "e30r11": {
        "left": "F2_ORION_METABOLIC_FULL",
        "rights": ["F0_PARENT_FEDERATION", "SAME_MODEL_REFLECTION", "SIMPLE_DIRECT"],
        "family_size": 3,
        "label": "Cell 1 (E30-R11): F2 vs each other arm",
    },
    "e60": {
        "left": "F2_ORION_METABOLIC_FULL",
        "rights": ["F2_MINUS_DECOMPOSITION", "F2_MINUS_NATIVE_RECOVERY",
                   "F2_MINUS_COUNTERPROBE", "F2_MINUS_SELECTIVE_REOPEN"],
        "family_size": 4,
        "label": "Cell 2 (E60): FULL vs each MINUS_X (GR3 evaluates the MINUS_X - FULL orientation)",
    },
}
GR1_CONTRAST = ("e30r11", "F2_ORION_METABOLIC_FULL", "F0_PARENT_FEDERATION")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


class AnalysisRefused(RuntimeError):
    pass


def require_gr0(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AnalysisRefused(f"GR0 receipt missing: {path}")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("gr0_status") != "PASS":
        raise AnalysisRefused(f"GR0 receipt status is {receipt.get('gr0_status')!r}, not PASS")
    components = receipt.get("components", {})
    for name in ("PC_R6_GR0A_RECEIPT.json", "PC_R6_GR0B_RECEIPT.json"):
        if components.get(name, {}).get("status") != "PASS":
            raise AnalysisRefused(f"GR0 component {name} is not PASS")
    return receipt


def any_true_aggregate(values: list[bool | None]) -> bool | None:
    """E60's registered critical-failure aggregation (sensitivity annex only)."""
    if any(value is True for value in values):
        return True
    if all(value is False for value in values):
        return False
    return None


def mcnemar_asymptotic_p(n10: int, n01: int) -> float | None:
    """Continuity-corrected McNemar chi-square (supplementary only; exact test is registered)."""
    n = n10 + n01
    if n == 0:
        return None
    statistic = (abs(n10 - n01) - 1) ** 2 / n
    return math.erfc(math.sqrt(statistic / 2.0))


def build_task_tables(cell: dict[str, Any], analyzer) -> dict[str, Any]:
    reps = [f"r{rep}" for rep in cell["reps"]]
    projects = cell["task_projects"]
    majority_tables: dict[str, dict[str, dict[str, Any]]] = {}
    any_true_tables: dict[str, dict[str, dict[str, Any]]] = {}
    per_arm: dict[str, Any] = {}
    for arm in cell["arms"]:
        majority_tables[arm] = {}
        any_true_tables[arm] = {}
        counted = 0
        any_failure_evaluations = 0
        checkable_tasks = 0
        task_any_true = 0
        none_reasons: dict[str, int] = {}
        instability = 0
        for task_id in cell["task_ids"]:
            entries = cell["evaluations"].get(f"{arm}/{task_id}", {})
            values: list[bool | None] = []
            counts: list[int | None] = []
            for rep in reps:
                entry = entries.get(rep, {"status": "MISSING"})
                count = entry.get("critical_new_failure_count")
                if count is None:
                    values.append(None)
                    counts.append(None)
                    reason = entry.get("critical_new_failure_status") or entry.get("status") or "NONE_UNKNOWN"
                    none_reasons[reason] = none_reasons.get(reason, 0) + 1
                else:
                    counted += 1
                    values.append(count > 0)
                    counts.append(int(count))
                    any_failure_evaluations += count > 0
            aggregate = analyzer.frozen_majority(values)
            checkable = {value for value in values if value is not None}
            instability += len(checkable) > 1
            if aggregate is not None:
                checkable_tasks += 1
                task_any_true += aggregate is True
            base = {"task_id": task_id, "arm_id": arm, "project": projects.get(task_id, "UNKNOWN"),
                    "_critical_failure_values": values, "_critical_new_failure_counts": counts}
            majority_tables[arm][task_id] = {**base, "_aggregate_critical_failure": aggregate}
            any_true_tables[arm][task_id] = {**base, "_aggregate_critical_failure": any_true_aggregate(values)}
        totals = cell["arm_totals"].get(arm, {})
        per_arm[arm] = {
            "evaluations": totals.get("evaluations"),
            "counted_evaluations": counted,
            "evaluations_with_any_critical_new_failure": any_failure_evaluations,
            "checkable_tasks_after_majority": checkable_tasks,
            "tasks_with_any_critical_new_failure_majority": task_any_true,
            "task_rate_any_critical_new_failure_majority": (task_any_true / checkable_tasks) if checkable_tasks else None,
            "cannot_check_tasks_after_majority": len(cell["task_ids"]) - checkable_tasks,
            "rep_instability_task_count": instability,
            "none_reasons_per_evaluation": none_reasons,
            "patch_apply_failure_rate": totals.get("patch_apply_failure_rate"),
            "compile_failure_rate": totals.get("compile_failure_rate"),
            "checkable_rate_per_evaluation": totals.get("checkable_rate"),
        }
    return {"majority": majority_tables, "any_true": any_true_tables, "per_arm": per_arm}


def contrast(analyzer, left_tasks, right_tasks, left_id: str, right_id: str) -> dict[str, Any]:
    block = analyzer.paired_binary_comparison(left_tasks, right_tasks, analyzer.critical_failure)
    swapped = analyzer.paired_binary_comparison(right_tasks, left_tasks, analyzer.critical_failure)
    table = block["paired_table"]
    discordant = table["left_only"] + table["right_only"]
    ci = block["risk_difference"]["ci95"]
    block.update({
        "left_arm": left_id, "right_arm": right_id,
        "risk_difference_orientation": f"{left_id} - {right_id}",
        "discordant_count": discordant,
        "registered_test": "EXACT_TWO_SIDED_DISCORDANT" if discordant <= EXACT_DISCORDANT_MAX
        else "EXACT_TWO_SIDED_DISCORDANT (discordants > 10; exact test remains valid, asymptotic McNemar reported as supplement)",
        "mcnemar_asymptotic_p_supplementary": mcnemar_asymptotic_p(table["left_only"], table["right_only"]),
        "one_sided_97_5_upper_bound": ci[1],
        "one_sided_97_5_lower_bound": ci[0],
        "ci95_excludes_zero": (ci[0] is not None and ci[1] is not None and (ci[0] > 0 or ci[1] < 0)),
        "swapped_orientation": {
            "risk_difference_orientation": f"{right_id} - {left_id}",
            "estimate": swapped["risk_difference"]["estimate"],
            "ci95": swapped["risk_difference"]["ci95"],
            "lower_bound": swapped["risk_difference"]["ci95"][0],
        },
    })
    if block["risk_difference"]["estimate"] is not None and swapped["risk_difference"]["estimate"] is not None:
        block["swapped_orientation"]["negation_consistent"] = (
            abs(block["risk_difference"]["estimate"] + swapped["risk_difference"]["estimate"]) < 1e-12
            and abs(ci[0] + swapped["risk_difference"]["ci95"][1]) < 1e-9
            and abs(ci[1] + swapped["risk_difference"]["ci95"][0]) < 1e-9)
    return block


def analyze_cell(cell_name: str, cell: dict[str, Any], analyzer) -> dict[str, Any]:
    family = CELL_FAMILIES[cell_name]
    tables = build_task_tables(cell, analyzer)
    contrasts = []
    sensitivity = []
    for right in family["rights"]:
        left_tasks = tables["majority"][family["left"]]
        right_tasks = tables["majority"][right]
        contrasts.append(contrast(analyzer, left_tasks, right_tasks, family["left"], right))
        sensitivity.append(contrast(analyzer, tables["any_true"][family["left"]], tables["any_true"][right],
                                    family["left"], right))
    holm = analyzer.holm_adjust([{"success": item} for item in contrasts])
    holm["endpoint"] = "TASK_LEVEL_MAJORITY_ANY_CRITICAL_NEW_FAILURE"
    holm["registered_family_size"] = family["family_size"]
    assert holm["registered_family_size"] == len(contrasts)
    project_strata = {}
    for right in family["rights"]:
        project_strata[right] = {}
        for project in sorted(set(cell["task_projects"].values())):
            left_sub = {t: v for t, v in tables["majority"][family["left"]].items() if v["project"] == project}
            right_sub = {t: v for t, v in tables["majority"][right].items() if v["project"] == project}
            block = analyzer.paired_binary_comparison(left_sub, right_sub, analyzer.critical_failure)
            project_strata[right][project] = {
                "paired_table": block["paired_table"], "checkable_task_count": block["checkable_task_count"],
                "risk_difference_estimate": block["risk_difference"]["estimate"],
            }
    return {
        "label": family["label"], "left_arm": family["left"], "campaign": cell.get("campaign"),
        "analysis_unit": "TASK_AFTER_WITHIN_TASK_REPETITION_MAJORITY (frozen_majority; None stays in denominator)",
        "endpoint": "any_critical_new_failure (critical_new_failure_count > 0) per evaluation -> majority over reps",
        "per_arm": tables["per_arm"], "contrasts": contrasts, "multiplicity": holm,
        "project_strata": project_strata,
        "baseline_status_counts": _count(cell["baselines"].values(), "status"),
        "sensitivity_any_true_aggregation_not_a_gate": {
            "rule": "E60 registered critical aggregation ANY_TRUE_ELSE_FALSE_ONLY_IF_ALL_EXPECTED_REPETITIONS_ARE_FALSE",
            "note": "descriptive annex only; the PC-R6 design fixes MAJORITY as the gate aggregation",
            "contrasts": [{k: v for k, v in item.items() if k in (
                "left_arm", "right_arm", "paired_table", "risk_difference", "exact_discordant_p",
                "checkable_task_count")} for item in sensitivity],
        },
    }


def _count(items, key: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        value = str(item.get(key))
        result[value] = result.get(value, 0) + 1
    return result


def evaluate_gates(cells: dict[str, Any]) -> dict[str, Any]:
    gates: dict[str, Any] = {}
    # GR1
    gr1: dict[str, Any] = {"gate": "GR1_CRITICAL_NON_INFERIORITY", "margin": NON_INFERIORITY_MARGIN,
                           "rule": "Cell 1 F2 vs F0: one-sided 97.5% upper bound of RD(F2 - F0) <= 0.02"}
    cell1 = cells.get("e30r11")
    block = None
    if cell1:
        block = next((c for c in cell1["contrasts"] if c["right_arm"] == GR1_CONTRAST[2]), None)
    if block is None or block["checkable_task_count"] == 0 or block["one_sided_97_5_upper_bound"] is None:
        gr1.update({"status": "CANNOT_CHECK", "reason": "no checkable paired tasks for F2 vs F0"})
    else:
        gr1.update({"estimate": block["risk_difference"]["estimate"],
                    "one_sided_97_5_upper_bound": block["one_sided_97_5_upper_bound"],
                    "checkable_task_count": block["checkable_task_count"],
                    "status": "PASS" if block["one_sided_97_5_upper_bound"] <= NON_INFERIORITY_MARGIN else "FAIL"})
    gates["GR1"] = gr1
    # GR2
    fired = []
    considered = []
    for cell_name, cell in cells.items():
        for item in cell["contrasts"]:
            estimate = item["risk_difference"]["estimate"]
            upper = item["risk_difference"]["ci95"][1]
            entry = {"cell": cell_name, "contrast": item["risk_difference_orientation"],
                     "estimate": estimate, "ci95": item["risk_difference"]["ci95"],
                     "checkable_task_count": item["checkable_task_count"],
                     "holm_adjusted_p": item.get("holm_adjusted_p"),
                     "fires": bool(estimate is not None and estimate < 0 and upper is not None and upper < 0)}
            considered.append(entry)
            if entry["fires"]:
                fired.append(entry)
    checkable_any = any(entry["checkable_task_count"] for entry in considered)
    gates["GR2"] = {
        "gate": "GR2_TAIL_INSURANCE",
        "rule": "any pre-registered contrast (F2/FULL on the left, amendment A5) with point RD < 0 and bootstrap 95% CI excluding 0",
        "status": "CANNOT_CHECK" if not checkable_any else ("FIRED" if fired else "NULL"),
        "fired": fired, "considered": considered,
    }
    # GR3
    fired3 = []
    considered3 = []
    cell2 = cells.get("e60")
    if cell2:
        for item in cell2["contrasts"]:
            lower = item["swapped_orientation"]["lower_bound"]
            entry = {"component": item["right_arm"],
                     "contrast": item["swapped_orientation"]["risk_difference_orientation"],
                     "estimate": item["swapped_orientation"]["estimate"],
                     "ci95": item["swapped_orientation"]["ci95"],
                     "checkable_task_count": item["checkable_task_count"],
                     "fires": bool(lower is not None and lower >= NECESSITY_MARGIN)}
            considered3.append(entry)
            if entry["fires"]:
                fired3.append(entry)
    gates["GR3"] = {
        "gate": "GR3_COMPONENT_NECESSITY_TAIL", "margin": NECESSITY_MARGIN,
        "rule": "Cell 2: some component with RD(MINUS_X - FULL) 95% lower bound >= +0.02",
        "status": ("CANNOT_CHECK" if not cell2 or not any(e["checkable_task_count"] for e in considered3)
                   else ("FIRED" if fired3 else "NULL")),
        "fired": fired3, "considered": considered3,
    }
    # routing (design section 6)
    if gr1["status"] == "CANNOT_CHECK":
        route = "CANNOT_CHECK__NO_CHECKABLE_PAIRS_FOR_GR1 (report counts; no programme consequence issues)"
    elif gates["GR2"]["status"] == "FIRED" or gates["GR3"]["status"] == "FIRED":
        route = ("GR2_or_GR3_fire: P-C first registered positive evidence class; claim structure "
                 "mean-null + tail-insured(/component-necessary); manuscript result block re-opened under a new freeze")
    elif gr1["status"] == "FAIL":
        route = ("GR1_fail: revision B refuted in the harmful direction; feeds contraction matrix and "
                 "P-C manuscript limitation section as a registered result")
    else:
        route = ("GR1_pass_GR2_GR3_null: P-C closes as mean-null + tail-safe at the registered margin; "
                 "theory revision B survives as a boundary claim; no component earns tail-necessity")
    gates["routing"] = route
    return gates


def render_markdown(result: dict[str, Any]) -> str:
    lines = [f"# PC-R6 full-regression rollup (V1)", "",
             f"Analysis `{ANALYSIS_VERSION}` over `{result['rollup_sha256'][:12]}…` "
             f"(GR0 receipt `{result['gr0_receipt_sha256'][:12]}…`, generated {result['generated_utc']}).",
             "", "No mean-success quantity is computed or reported here (no-rescue clause).", ""]
    for cell_name, cell in result["cells"].items():
        lines += [f"## {cell['label']}", "", "| arm | evaluations | counted | checkable tasks (majority) | tasks any-critical | rate | patch-apply fail | compile fail |",
                  "|---|---|---|---|---|---|---|---|"]
        for arm, item in cell["per_arm"].items():
            rate = item["task_rate_any_critical_new_failure_majority"]
            lines.append(f"| `{arm}` | {item['evaluations']} | {item['counted_evaluations']} | "
                         f"{item['checkable_tasks_after_majority']} | {item['tasks_with_any_critical_new_failure_majority']} | "
                         f"{'—' if rate is None else f'{rate:.3f}'} | "
                         f"{_fmt(item['patch_apply_failure_rate'])} | {_fmt(item['compile_failure_rate'])} |")
        lines += ["", "| contrast (RD orientation) | paired (both_F/both_T/L-only/R-only) | checkable | RD [CI95] | one-sided 97.5% upper | exact p | Holm p |",
                  "|---|---|---|---|---|---|---|"]
        for item in cell["contrasts"]:
            table = item["paired_table"]
            rd = item["risk_difference"]
            lines.append(f"| {item['risk_difference_orientation']} | {table['both_false']}/{table['both_true']}/{table['left_only']}/{table['right_only']} | "
                         f"{item['checkable_task_count']} | {_fmt(rd['estimate'])} [{_fmt(rd['ci95'][0])}, {_fmt(rd['ci95'][1])}] | "
                         f"{_fmt(item['one_sided_97_5_upper_bound'])} | {_fmt(item['exact_discordant_p'])} | {_fmt(item.get('holm_adjusted_p'))} |")
        lines.append("")
    gates = result["gates"]
    lines += ["## Gates", "", "| gate | status | detail |", "|---|---|---|"]
    gr1 = gates["GR1"]
    lines.append(f"| GR1 non-inferiority (≤ {gr1['margin']}) | **{gr1['status']}** | "
                 f"RD(F2−F0)={_fmt(gr1.get('estimate'))}, upper={_fmt(gr1.get('one_sided_97_5_upper_bound'))}, n={gr1.get('checkable_task_count', 0)} |")
    lines.append(f"| GR2 tail insurance | **{gates['GR2']['status']}** | fired: {[e['contrast'] for e in gates['GR2']['fired']] or 'none'} |")
    lines.append(f"| GR3 component necessity (tail) | **{gates['GR3']['status']}** | fired: {[e['component'] for e in gates['GR3']['fired']] or 'none'} |")
    lines += ["", f"**Routing (design §6):** {gates['routing']}", ""]
    return "\n".join(lines) + "\n"


def _fmt(value) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def render_outcome_receipt(result: dict[str, Any]) -> str:
    gates = result["gates"]
    lines = ["# PC-R6 outcome receipt", "",
             f"**Design:** `{DESIGN_ID}` (sha256 `{(result.get('design_sha256') or 'n/a')[:12]}…`)  ",
             f"**Campaign:** `{result.get('campaign_id', 'n/a')}`  ",
             f"**Rollup:** `PC_R6_FULLREG_RAW_ROLLUP_V1.json` sha256 `{result['rollup_sha256']}`  ",
             f"**GR0 receipt:** sha256 `{result['gr0_receipt_sha256']}` (PASS, enforced before any gate)  ",
             f"**Seed:** {SEED}; bootstrap {BOOTSTRAP_DRAWS} draws, PROJECT-stratified; Holm within families 3 and 4.", "",
             "| gate | status |", "|---|---|",
             f"| GR0 LANE_VALID | PASS |",
             f"| GR1 CRITICAL_NON_INFERIORITY | {gates['GR1']['status']} |",
             f"| GR2 TAIL_INSURANCE | {gates['GR2']['status']} |",
             f"| GR3 COMPONENT_NECESSITY_TAIL | {gates['GR3']['status']} |", "",
             f"**Pre-registered routing:** {gates['routing']}", "",
             "No mean-success claim issues from this lane (design §7).", ""]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rollup", type=Path, required=True)
    parser.add_argument("--gr0-receipt", type=Path, required=True)
    parser.add_argument("--analyzer", type=Path, required=True,
                        help="frozen scripts/analyze_orion_real_problem_results.py")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--design", type=Path, help="design JSON (sha256 recorded)")
    parser.add_argument("--campaign-id", default=None)
    args = parser.parse_args(argv)
    try:
        gr0 = require_gr0(args.gr0_receipt)
    except AnalysisRefused as exc:
        print(f"ANALYSIS_REFUSED: {exc}", file=sys.stderr)
        return 2
    analyzer = load_module("pc_r6_frozen_analyzer", args.analyzer)
    original_bootstrap = analyzer.paired_bootstrap_difference
    analyzer.paired_bootstrap_difference = functools.partial(
        original_bootstrap, repetitions=BOOTSTRAP_DRAWS, seed=SEED)
    rollup = json.loads(args.rollup.read_text(encoding="utf-8"))
    cells = {name: analyze_cell(name, cell, analyzer) for name, cell in rollup["cells"].items()
             if name in CELL_FAMILIES}
    result = {
        "schema_version": ANALYSIS_VERSION, "design": DESIGN_ID, "generated_utc": datetime.now(timezone.utc).isoformat(),
        "seed": SEED, "bootstrap_draws": BOOTSTRAP_DRAWS, "stratification": "PROJECT",
        "rollup_sha256": sha256_file(args.rollup), "gr0_receipt_sha256": sha256_file(args.gr0_receipt),
        "gr0_status": gr0.get("gr0_status"), "analyzer_sha256": sha256_file(args.analyzer),
        "rollup_complete": rollup.get("complete"), "campaign_id": args.campaign_id,
        "design_sha256": sha256_file(args.design) if args.design else None,
        "cells": cells, "gates": evaluate_gates(cells),
        "no_rescue_clause": "no mean-success claim; only re-evaluation of the exact frozen proposals",
    }
    write_json(args.out / "PC_R6_FULLREG_ROLLUP_V1.json", result)
    (args.out / "PC_R6_FULLREG_ROLLUP_V1.md").write_text(render_markdown(result), encoding="utf-8")
    (args.out / "PC_R6_OUTCOME_RECEIPT.md").write_text(render_outcome_receipt(result), encoding="utf-8")
    print(json.dumps({"GR1": result["gates"]["GR1"]["status"], "GR2": result["gates"]["GR2"]["status"],
                      "GR3": result["gates"]["GR3"]["status"], "routing": result["gates"]["routing"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
