#!/usr/bin/env python3
"""E30-R13 analysis: the E30-R12 registered arithmetic, plus two channel gates.

E30-R12 halted at ``EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ``.  Its endpoint
arithmetic was never exercised on data and is not in question; what failed was the
execution channel, and no registered gate observed it.  E30-R13 therefore does not
re-derive the statistics: it **imports E30-R12's analysis module by path under a
sha256 pin** and reuses ``build_tables``, ``family``, ``evaluate_gates`` and ``route``
verbatim.  Retyping them would make the two studies' endpoint definitions merely
similar; importing them makes them the same code.

What E30-R13 adds are the two gates whose absence let R12 mistake a moved
experimental condition for an execution hiccup:

``GR0d  CHANNEL_CONTRACT_HOMOGENEITY``
    every response envelope records exactly one request-body contract, and it is the
    frozen one -- by sha256 over the contract bytes, not by its label.

``GR0e  CHANNEL_BEHAVIOUR_CONFORMANCE``
    no call stopped at ``max_tokens`` and no call emitted zero text characters.  This
    is the *behavioural* half: R12's 116 failures all sat at the cap with a thinking
    block and no text, at an unchanged served model id, and GR0c over the served id
    passed on every envelope it saw.

Both gates publish their denominators, and both distinguish COULD-NOT-CHECK from
CHECKED-AND-CLEAN with a distinct status and a distinct process exit code.  A gate that
reports ``0 offenders`` after reading ``0 envelopes`` is the failure mode this study
exists to close, so it may not be expressible here.
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DESIGN_ID = "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1"
SCHEMA = "orion.v2.e30-r13-analysis.v1"
CELL_NAME = "e30r13"
SEED = 20260903
BOOTSTRAP_DRAWS = 10000

#: The E30-R12 analysis module, imported rather than copied.  The pin is asserted at
#: run time: an unpinned import would let R12's frozen file drift under R13 silently.
R12_ANALYSIS_RELATIVE = Path("..") / "e30-r12" / "e30_r12_analysis.py"

#: Exit codes.  "Could not check" is NOT "checked and fine", and must not share a code.
EXIT_OK = 0
EXIT_PRECONDITION_REFUSED = 3
EXIT_GATE_FAIL = 4
EXIT_GATE_COULD_NOT_CHECK = 5


class AnalysisRefused(RuntimeError):
    """A precondition of the registered analysis is not met; no gate may be read."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_r12_analysis(path: Path, expected_sha256: str | None):
    import importlib.util

    if not path.is_file():
        raise AnalysisRefused(f"E30-R12 analysis module not found at {path}")
    got = sha256_file(path)
    if expected_sha256 and got != expected_sha256:
        raise AnalysisRefused(
            f"E30-R12 analysis sha256 {got} != pinned {expected_sha256}; "
            "the imported arithmetic is not the registered arithmetic")
    spec = importlib.util.spec_from_file_location("e30_r12_analysis_imported", path)
    if spec is None or spec.loader is None:
        raise AnalysisRefused(f"cannot import the E30-R12 analysis at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["e30_r12_analysis_imported"] = module
    spec.loader.exec_module(module)
    return module, got


# ------------------------------------------------------------------- channel gates
def _iter_envelopes(campaign: Path, arms: list[str], reps: list[str],
                    task_ids: list[str]):
    for rep in reps:
        for arm in arms:
            for task_id in task_ids:
                path = (campaign / "run" / f"confirmatory-r{rep}" / "responses"
                        / arm / f"{task_id}.json")
                yield rep, arm, task_id, path


def channel_contract_homogeneity(campaign: Path, arms: list[str], reps: list[str],
                                 task_ids: list[str], expected_contract_id: str,
                                 expected_contract_sha256: str) -> dict[str, Any]:
    """GR0d: one request-body contract across the campaign, equal to the frozen one."""
    expected_envelopes = len(reps) * len(arms) * len(task_ids)
    offenders: list[dict[str, Any]] = []
    contract_counts: dict[str, int] = {}
    sha_counts: dict[str, int] = {}
    envelopes_read = 0
    envelopes_with_a_receipt = 0
    calls_seen = 0
    calls_reporting_a_contract = 0

    for rep, arm, task_id, path in _iter_envelopes(campaign, arms, reps, task_ids):
        where = {"rep": rep, "arm": arm, "task_id": task_id}
        if not path.is_file():
            offenders.append(where | {"reason": "RESPONSE_MISSING"})
            continue
        envelopes_read += 1
        envelope = json.loads(path.read_text())
        receipt = envelope.get("channel_receipt")
        if not isinstance(receipt, dict):
            offenders.append(where | {"reason": "CHANNEL_RECEIPT_ABSENT"})
            continue
        envelopes_with_a_receipt += 1
        calls_seen += int(receipt.get("model_calls", 0) or 0)
        reporting = int(receipt.get("calls_reporting_a_contract", 0) or 0)
        calls_reporting_a_contract += reporting
        if reporting != int(receipt.get("model_calls", 0) or 0):
            offenders.append(where | {
                "reason": "CALLS_WITHOUT_A_REPORTED_CONTRACT",
                "model_calls": receipt.get("model_calls"),
                "calls_reporting_a_contract": reporting})
        ids = receipt.get("contract_ids")
        shas = receipt.get("contract_sha256s")
        if not isinstance(ids, list) or len(ids) != 1:
            offenders.append(where | {"reason": "CONTRACT_IDS_NOT_A_SINGLETON", "observed": ids})
            continue
        if not isinstance(shas, list) or len(shas) != 1:
            offenders.append(where | {"reason": "CONTRACT_SHA256S_NOT_A_SINGLETON", "observed": shas})
            continue
        contract_counts[str(ids[0])] = contract_counts.get(str(ids[0]), 0) + 1
        sha_counts[str(shas[0])] = sha_counts.get(str(shas[0]), 0) + 1
        if str(ids[0]) != expected_contract_id:
            offenders.append(where | {"reason": "CONTRACT_ID_MISMATCH", "observed": ids[0]})
        if str(shas[0]) != expected_contract_sha256:
            offenders.append(where | {"reason": "CONTRACT_SHA256_MISMATCH", "observed": shas[0]})

    if envelopes_with_a_receipt == 0:
        status = "COULD_NOT_CHECK"
    elif offenders or len(sha_counts) != 1:
        status = "FAIL"
    else:
        status = "PASS"
    return {
        "gate_id": "GR0d", "name": "CHANNEL_CONTRACT_HOMOGENEITY",
        "expected_contract_id": expected_contract_id,
        "expected_contract_sha256": expected_contract_sha256,
        "envelopes_expected": expected_envelopes,
        "envelopes_read": envelopes_read,
        "envelopes_with_a_channel_receipt": envelopes_with_a_receipt,
        "model_calls_seen": calls_seen,
        "model_calls_reporting_a_contract": calls_reporting_a_contract,
        "contract_id_counts": contract_counts,
        "contract_sha256_counts": sha_counts,
        "offenders": offenders[:50],
        "offender_count": len(offenders),
        "status": status,
    }


def channel_behaviour_conformance(campaign: Path, arms: list[str], reps: list[str],
                                  task_ids: list[str]) -> dict[str, Any]:
    """GR0e: the channel actually answered -- no truncation, no empty-text call."""
    offenders: list[dict[str, Any]] = []
    envelopes_with_a_receipt = 0
    calls_seen = 0
    stop_reason_counts: dict[str, int] = {}
    max_output_tokens_observed = 0

    for rep, arm, task_id, path in _iter_envelopes(campaign, arms, reps, task_ids):
        where = {"rep": rep, "arm": arm, "task_id": task_id}
        if not path.is_file():
            offenders.append(where | {"reason": "RESPONSE_MISSING"})
            continue
        envelope = json.loads(path.read_text())
        receipt = envelope.get("channel_receipt")
        if not isinstance(receipt, dict):
            offenders.append(where | {"reason": "CHANNEL_RECEIPT_ABSENT"})
            continue
        envelopes_with_a_receipt += 1
        calls_seen += int(receipt.get("calls_reporting_a_contract", 0) or 0)
        for reason in receipt.get("stop_reasons", []) or []:
            stop_reason_counts[str(reason)] = stop_reason_counts.get(str(reason), 0) + 1
        max_output_tokens_observed = max(
            max_output_tokens_observed, int(receipt.get("max_output_tokens_observed", 0) or 0))
        if "max_tokens" in [str(r) for r in (receipt.get("stop_reasons") or [])]:
            offenders.append(where | {"reason": "CALL_TRUNCATED_AT_MAX_TOKENS",
                                      "stop_reasons": receipt.get("stop_reasons")})
        zero_text = int(receipt.get("calls_with_zero_text_chars", 0) or 0)
        if zero_text:
            offenders.append(where | {"reason": "CALL_EMITTED_ZERO_TEXT_CHARACTERS",
                                      "calls_with_zero_text_chars": zero_text})

    if envelopes_with_a_receipt == 0:
        status = "COULD_NOT_CHECK"
    elif offenders:
        status = "FAIL"
    else:
        status = "PASS"
    return {
        "gate_id": "GR0e", "name": "CHANNEL_BEHAVIOUR_CONFORMANCE",
        "envelopes_expected": len(reps) * len(arms) * len(task_ids),
        "envelopes_with_a_channel_receipt": envelopes_with_a_receipt,
        "model_calls_checked": calls_seen,
        "stop_reason_counts": stop_reason_counts,
        "max_output_tokens_observed": max_output_tokens_observed,
        "offenders": offenders[:50],
        "offender_count": len(offenders),
        "status": status,
    }


def hard_gate_terminal(gates: dict[str, Any]) -> dict[str, str]:
    """The terminal for a run that fails a hard gate, in the registered precedence order.

    Separated from the endpoint routing because it must be reachable WITHOUT any endpoint
    table having been built: the design's failure action is HALT_NO_GATE_EVALUATION, and a
    halted run that still emitted contrast estimates would leave numbers the design forbids
    lying in the rollup for a later reader to quote.
    """
    for gate_id, terminal in (("GR0d", "CHANNEL_CONTRACT_VIOLATION"),
                              ("GR0e", "CHANNEL_BEHAVIOUR_VIOLATION"),
                              ("GR0c", "LANE_DEFECT")):
        gate = gates.get(gate_id)
        if gate is None or gate["status"] == "PASS":
            continue
        if gate["status"] == "COULD_NOT_CHECK":
            return {"terminal": "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ",
                    "detail": f"{gate_id} could not be evaluated; this is not a null and not a "
                              "gate pass, and no endpoint is read"}
        return {"terminal": terminal,
                "detail": f"{gate_id} {gate['name']} failed with {gate['offender_count']} "
                          f"offenders; no endpoint may be read"}
    raise AssertionError("hard_gate_terminal called with every hard gate passing")


def route_with_channel_gates(r12, gates: dict[str, Any], per_arm: dict[str, Any]) -> dict[str, str]:
    """The registered routing, with the two channel gates ahead of everything else."""
    for gate_id, terminal in (("GR0d", "CHANNEL_CONTRACT_VIOLATION"),
                              ("GR0e", "CHANNEL_BEHAVIOUR_VIOLATION")):
        status = gates[gate_id]["status"]
        if status == "COULD_NOT_CHECK":
            return {"terminal": "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ",
                    "detail": f"{gate_id} could not be evaluated; this is not a null and not a "
                              "gate pass, and no endpoint is read"}
        if status != "PASS":
            return {"terminal": terminal,
                    "detail": f"{gate_id} {gates[gate_id]['name']} failed with "
                              f"{gates[gate_id]['offender_count']} offenders over "
                              f"{gates[gate_id]['envelopes_with_a_channel_receipt']} envelopes "
                              "carrying a channel receipt; no endpoint may be read"}
    return r12.route(gates, per_arm)


# ------------------------------------------------------------------------- refusal
def render_refusal_markdown(result: dict[str, Any]) -> str:
    """The artifact a halted run produces. It contains no endpoint number, by construction."""
    gates = result["gates"]
    lines = [
        "# E30-R13 — halted before any endpoint was read",
        "",
        f"**Terminal: `{result['routing']['terminal']}`.** {result['routing']['detail']}",
        "",
        "No endpoint was read, no contrast was computed and no table appears below, because "
        "the registered routing halts here. This is **not** a null on E1, **not** a null on "
        "E2, **not** `NO_ARM_SEPARATION`, **not** `PARENT_SUFFICIENT`, and **not** evidence "
        "of equivalence between any two arms.",
        "",
        "| gate | status | denominators | offenders |",
        "|---|---|---|---|",
    ]
    for gate_id in ("GR0c", "GR0d", "GR0e"):
        gate = gates.get(gate_id)
        if not gate:
            continue
        denominators = (
            f"{gate.get('envelopes_with_a_channel_receipt', gate.get('envelopes_read'))}"
            f"/{gate.get('envelopes_expected', '—')} envelopes")
        lines.append(f"| {gate_id} {gate['name']} | **{gate['status']}** | {denominators} | "
                     f"{gate.get('offender_count')} |")
    lines += ["", "## Endpoints", "", "None read.", ""]
    return "\n".join(lines)


# --------------------------------------------------------------------------- render
def render_markdown(r12, result: dict[str, Any]) -> str:
    fmt = r12._fmt
    per_arm = result["per_arm"]
    lines = [
        "# E30-R13 rollup (V1)",
        "",
        f"Analysis `{SCHEMA}` over rollup `{result['inputs']['rollup_sha256'][:12]}…` "
        f"(GR0 receipt `{result['inputs']['gr0_sha256'][:12]}…`, design "
        f"`{result['inputs']['design_sha256'][:12]}…`, generated {result['generated_utc']}).",
        "",
        f"Endpoint arithmetic imported verbatim from `e30_r12_analysis.py` "
        f"(sha256 `{result['inputs']['e30_r12_analysis_sha256'][:12]}…`). "
        f"Seed {SEED}; bootstrap {BOOTSTRAP_DRAWS} draws, PROJECT-stratified; two "
        "independent Holm families of three, one per endpoint. No imputation.",
        "",
        "## Per-arm endpoints and the apply-rate diagnostic",
        "",
        "| arm | E1 success / checkable | E1 rate | E2 any-critical / checkable | D1 apply rate | D1 apply-fail | PC-R6 comparator |",
        "|---|---|---|---|---|---|---|",
    ]
    for arm in [r12.LEFT_ARM] + r12.RIGHT_ARMS:
        item = per_arm.get(arm, {})
        lines.append(
            f"| `{arm}` | {item.get('E1_tasks_success')}/{item.get('E1_tasks_checkable')} | "
            f"{fmt(item.get('E1_rate'), 3)} | "
            f"{item.get('E2_tasks_any_critical_new_failure')}/{item.get('E2_tasks_checkable')} | "
            f"{fmt(item.get('D1_patch_apply_rate'), 4)} | "
            f"{fmt(item.get('D1_patch_apply_failure_rate'), 4)} | "
            f"{fmt(item.get('D1_pc_r6_comparator_failure_rate'), 4)} |")
    for label, key in (("E1 — registered failing test fixed (primary)", "E1_contrasts"),
                       (f"E1 — sensitivity denominator "
                        f"({result['denominators']['E1_sensitivity']} tasks, excluding "
                        f"{result['E1_sensitivity_excluded_task_ids'] or 'none'})",
                        "E1_sensitivity_contrasts"),
                       ("E2 — any critical new failure (co-primary)", "E2_contrasts")):
        lines += ["", f"## {label}", "",
                  "| contrast | paired (bothF/bothT/L-only/R-only) | checkable | RD [CI95] | exact p | Holm p | reject |",
                  "|---|---|---|---|---|---|---|"]
        for block in result[key]:
            t, rd = block["paired_table"], block["risk_difference"]
            lines.append(
                f"| {block['left_arm']} − {block['right_arm']} | "
                f"{t['both_false']}/{t['both_true']}/{t['left_only']}/{t['right_only']} | "
                f"{block['checkable_task_count']} | {fmt(rd['estimate'])} "
                f"[{fmt(rd['ci95'][0])}, {fmt(rd['ci95'][1])}] | "
                f"{fmt(block.get('exact_discordant_p'))} | {fmt(block.get('holm_p'))} | "
                f"{fmt(block.get('holm_reject'))} |")

    d, e = result["gates"]["GR0d"], result["gates"]["GR0e"]
    lines += ["", "## Channel gates (E30-R13's addition; denominators published)", "",
              "| gate | status | denominators | detail |", "|---|---|---|---|",
              f"| GR0d {d['name']} | **{d['status']}** | "
              f"{d['envelopes_with_a_channel_receipt']}/{d['envelopes_expected']} envelopes carry a "
              f"receipt; {d['model_calls_reporting_a_contract']}/{d['model_calls_seen']} calls report a "
              f"contract | distinct contract sha256s: {d['contract_sha256_counts'] or 'none'}; "
              f"offenders {d['offender_count']} |",
              f"| GR0e {e['name']} | **{e['status']}** | "
              f"{e['envelopes_with_a_channel_receipt']}/{e['envelopes_expected']} envelopes carry a "
              f"receipt; {e['model_calls_checked']} calls checked | stop reasons "
              f"{e['stop_reason_counts'] or 'none'}; max output tokens "
              f"{e['max_output_tokens_observed']}; offenders {e['offender_count']} |",
              "",
              "`COULD_NOT_CHECK` is a distinct status from `PASS` and routes to "
              "`EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ`, not to a null.",
              "", "## Registered gates (imported from E30-R12)", "",
              "| gate | status | detail |", "|---|---|---|"]
    for gate_id in ("GR0c", "GR1", "GR2", "GR3"):
        gate = result["gates"][gate_id]
        detail = {
            "GR0c": f"{gate.get('envelopes_read')} envelopes, {gate.get('offender_count')} offenders, "
                    f"ids {gate.get('served_model_counts')}",
            "GR1": f"all arms below {r12.APPLY_FAIL_CEILING} apply-fail and below the PC-R6 "
                   f"comparator: {gate['status'] == 'PASS'}",
            "GR2": f"rejected: {gate.get('rejected_contrasts') or 'none'}",
            "GR3": f"RD={fmt(gate.get('risk_difference'))}, "
                   f"upper={fmt(gate.get('one_sided_97_5_upper_bound'))}, "
                   f"n={gate.get('checkable_paired_tasks')}, margin {r12.NON_INFERIORITY_MARGIN}",
        }[gate_id]
        lines.append(f"| {gate_id} {gate['name']} | **{gate['status']}** | {detail} |")
    lines += ["", "## Dispositions applied (registered pre-dispatch)", "",
              f"- E2 excluded with count under `{', '.join(result['E2_exclusion_rule'])}`: "
              f"{result['E2_excluded_task_ids'] or 'none'}",
              f"- E1 denominator {result['denominators']['E1']}; E1 sensitivity denominator "
              f"{result['denominators']['E1_sensitivity']}; E2 denominator "
              f"{result['denominators']['E2']}",
              "", "## Pre-registered routing", "",
              f"**{result['routing']['terminal']}** — {result['routing']['detail']}",
              "", "## Power boundary (registered pre-dispatch)", "",
              "At n = 40 the exact test cannot reject unless at least 7 tasks are discordant in "
              "the same direction (risk difference ≥ 0.175). Power against the registered "
              "5-percentage-point minimum important difference is 1–2%. A non-rejection here is "
              "NOT evidence of equivalence.",
              "",
              "## Comparison to earlier runs", "",
              "E30-R11 recorded no served model id and ran under no registered request-body "
              "contract, so **any R13-vs-R11 comparison is descriptive only** — twice over. "
              "E30-R12 read no endpoint at all, so there is nothing to compare R13 with.", ""]
    return "\n".join(lines)


# ----------------------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rollup", type=Path, required=True)
    parser.add_argument("--gr0", type=Path, required=True)
    parser.add_argument("--gr0b", type=Path)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--analyzer", type=Path, required=True)
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--r12-analysis", type=Path,
                        default=(Path(__file__).resolve().parent / R12_ANALYSIS_RELATIVE).resolve())
    parser.add_argument("--r12-analysis-sha256")
    parser.add_argument("--served-model", default="glm-5.3")
    parser.add_argument("--channel-contract", required=True)
    parser.add_argument("--channel-contract-sha256", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        r12, r12_sha = load_r12_analysis(args.r12_analysis, args.r12_analysis_sha256)
    except AnalysisRefused as exc:
        print(f"ANALYSIS_REFUSED: {exc}", file=sys.stderr)
        return EXIT_PRECONDITION_REFUSED
    try:
        # The imported module raises its OWN AnalysisRefused, which is a different class
        # from this module's; catching only the local one would let a missing or failing
        # GR0 receipt escape as a traceback and lose the registered refusal exit code.
        gr0 = r12.require_gr0(args.gr0)          # asserted BEFORE any endpoint is read
    except (AnalysisRefused, r12.AnalysisRefused) as exc:
        print(f"ANALYSIS_REFUSED: {exc}", file=sys.stderr)
        return EXIT_PRECONDITION_REFUSED

    analyzer = r12.load_module("orion_real_problem_analyzer", args.analyzer)
    original_bootstrap = analyzer.paired_bootstrap_difference
    analyzer.paired_bootstrap_difference = functools.partial(
        original_bootstrap, repetitions=BOOTSTRAP_DRAWS, seed=SEED)

    rollup = json.loads(args.rollup.read_text())
    cell = rollup["cells"][CELL_NAME]

    gr0c = r12.served_model_homogeneity(args.campaign, cell["arms"], cell["reps"],
                                        cell["task_ids"], args.served_model)
    gr0d = channel_contract_homogeneity(args.campaign, cell["arms"], cell["reps"],
                                        cell["task_ids"], args.channel_contract,
                                        args.channel_contract_sha256)
    gr0e = channel_behaviour_conformance(args.campaign, cell["arms"], cell["reps"],
                                         cell["task_ids"])

    # HALT_NO_GATE_EVALUATION, taken literally.  Computing the endpoint tables and then
    # routing away from them would still write contrast estimates into the rollup that a
    # later reader could quote as results -- exactly the kind of number the design forbids
    # a halted run to produce.  So the hard channel gates and the served-model gate are
    # evaluated FIRST, and if any of them is not PASS the run writes a refusal artifact
    # carrying the gates and the terminal and NOTHING ELSE.
    hard_gates = {"GR0c": gr0c, "GR0d": gr0d, "GR0e": gr0e}
    if any(gate["status"] != "PASS" for gate in hard_gates.values()):
        routing = hard_gate_terminal(hard_gates)
        refusal = {
            "schema_version": SCHEMA, "design": DESIGN_ID, "seed": SEED,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "status": "HALTED_BEFORE_ENDPOINT_READ",
            "inputs": {
                "rollup_sha256": sha256_file(args.rollup),
                "gr0_sha256": sha256_file(args.gr0),
                "design_sha256": sha256_file(args.design),
                "e30_r12_analysis_sha256": r12_sha,
                "campaign": str(args.campaign),
            },
            "gates": hard_gates,
            "routing": routing,
            "endpoints_read": [],
            "endpoint_tables_computed": False,
            "status_is_not": ["a null on E1", "a null on E2", "a NO_ARM_SEPARATION terminal",
                              "a PARENT_SUFFICIENT terminal",
                              "evidence of equivalence between any two arms"],
            "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                          "grants_publication_readiness": False},
        }
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "E30_R13_ROLLUP_V1.json").write_text(
            json.dumps(refusal, indent=2, sort_keys=True) + "\n")
        (args.out / "E30_R13_ROLLUP_V1.md").write_text(render_refusal_markdown(refusal) + "\n")
        print(json.dumps({"routing": routing["terminal"],
                          "gates": {k: v["status"] for k, v in hard_gates.items()}}))
        if "COULD_NOT_CHECK" in (gr0d["status"], gr0e["status"]):
            return EXIT_GATE_COULD_NOT_CHECK
        return EXIT_GATE_FAIL

    tables = r12.build_tables(cell, analyzer)
    e1 = r12.family(analyzer, tables["E1"], analyzer.success, "E1 success")
    excluded = r12.e1_sensitivity_exclusions(args.gr0b)
    e1_sensitivity_tables = {
        arm: {task_id: item for task_id, item in table.items() if task_id not in excluded}
        for arm, table in tables["E1"].items()}
    e1_sensitivity = r12.family(analyzer, e1_sensitivity_tables, analyzer.success,
                                "E1 success, sensitivity denominator")
    e2 = r12.family(analyzer, tables["E2"], analyzer.critical_failure, "E2 critical failure")

    gates = r12.evaluate_gates(tables["per_arm"], e1, e2, gr0c)
    gates["GR0d"], gates["GR0e"] = gr0d, gr0e
    routing = route_with_channel_gates(r12, gates, tables["per_arm"])

    result = {
        "schema_version": SCHEMA, "design": DESIGN_ID, "seed": SEED,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "bootstrap_draws": BOOTSTRAP_DRAWS, "stratification": "PROJECT",
        "inputs": {
            "rollup_sha256": sha256_file(args.rollup),
            "gr0_sha256": sha256_file(args.gr0),
            "design_sha256": sha256_file(args.design),
            "analyzer_sha256": sha256_file(args.analyzer),
            "e30_r12_analysis_sha256": r12_sha,
            "campaign": str(args.campaign),
            "gr0_status": gr0.get("status"),
        },
        "endpoint_arithmetic_provenance": (
            "build_tables, family, evaluate_gates and route imported from "
            "research/experiments/e30-r12/e30_r12_analysis.py under a sha256 pin; "
            "E30-R12's file is frozen terminal and is not modified by this study"),
        "per_arm": tables["per_arm"],
        "E1_contrasts": e1,
        "E1_sensitivity_contrasts": e1_sensitivity,
        "E1_sensitivity_excluded_task_ids": excluded,
        "E2_contrasts": e2,
        "E2_excluded_task_ids": tables["E2_excluded_task_ids"],
        "E2_exclusion_rule": tables["E2_exclusion_rule"],
        "E1_sensitivity_condition": r12.E1_SENSITIVITY_CONDITION,
        "denominators": {
            "E1": len(cell["task_ids"]),
            "E1_sensitivity": len(cell["task_ids"]) - len(excluded),
            "E2": len(cell["task_ids"]) - len(tables["E2_excluded_task_ids"]),
        },
        "gates": gates,
        "routing": routing,
        "no_rescue_clause": (
            "E30-R11, E60, PC-R6 and E30-R12 receipts are frozen; nothing here revises, "
            "re-scores or reinterprets them. E30-R12 read no endpoint, so R13 is not a "
            "re-analysis of it; R13 is a new campaign identity with its own responses."),
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "grants_publication_readiness": False},
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "E30_R13_ROLLUP_V1.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    (args.out / "E30_R13_ROLLUP_V1.md").write_text(render_markdown(r12, result) + "\n")
    print(json.dumps({"routing": routing["terminal"],
                      "gates": {k: v["status"] for k, v in gates.items()}}))
    if "COULD_NOT_CHECK" in (gr0d["status"], gr0e["status"]):
        return EXIT_GATE_COULD_NOT_CHECK
    if "FAIL" in (gr0d["status"], gr0e["status"]):
        return EXIT_GATE_FAIL
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
