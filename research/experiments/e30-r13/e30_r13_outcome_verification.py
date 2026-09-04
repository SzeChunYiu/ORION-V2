#!/usr/bin/env python3
"""E30-R13 outcome verification -- read-only checks over a completed campaign.

Every number in ``E30_R13_OUTCOME_RECEIPT.md`` that is not lifted verbatim from the
frozen design or from ``E30_R13_ROLLUP_V1.json`` comes from here, so no receipt figure
is a human transcription of a log line.

This module computes **no endpoint, no contrast and no terminal**. It re-runs gate
predicates that ``e30_r13_analysis.py`` already ran and asserts the published values
reproduce, reconciles the published denominators against the raw rollup, and checks that
the gate predicates can actually fire -- a gate that has never been shown to fail is a
gate whose ``0 violations`` means nothing.

Three statuses, deliberately distinct:

``PASS``             the check ran and held
``FAIL``             the check ran and did not hold
``COULD_NOT_CHECK``  the check could not run at all

and three exit codes: 0 all PASS, 4 some FAIL, 5 some COULD_NOT_CHECK (5 wins over 4
only when nothing failed; a real failure is never hidden behind a missing input).
Reporting ``COULD_NOT_CHECK`` as a pass is prohibited by the design's no-rescue clause,
so it gets its own code rather than being folded into either neighbour.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

SCHEMA = "orion.v2.e30-r13-outcome-verification.v1"
HERE = Path(__file__).resolve().parent

PASS, FAIL, COULD_NOT_CHECK = "PASS", "FAIL", "COULD_NOT_CHECK"


# --------------------------------------------------------------------------- helpers
def load_analysis(path: Path):
    """Import ``e30_r13_analysis`` from an explicit path (the campaign's own copy)."""
    spec = importlib.util.spec_from_file_location("e30_r13_analysis_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def applied_set(cell: dict[str, Any], arm: str) -> set[tuple[str, str]]:
    """The (rep, task) slots where this arm's patch applied cleanly."""
    out: set[tuple[str, str]] = set()
    for key, reps in cell["evaluations"].items():
        arm_id, _, task_id = key.partition("/")
        if arm_id != arm:
            continue
        for rep, entry in reps.items():
            if entry.get("patch_apply_returncode") == 0:
                out.add((rep, task_id))
    return out


def e2_checkable_by_majority(cell: dict[str, Any], arm: str,
                             excluded: list[str]) -> int:
    """Reconstruct ``E2_tasks_checkable`` from the raw rollup under the majority rule.

    The published per-arm denominator is a count of TASKS whose three repetitions
    resolve to a majority, not a count of countable evaluations; those two differ
    whenever a task has one uncountable repetition, and quoting the wrong one would
    describe the study's own denominator incorrectly.
    """
    n = 0
    for key, reps in cell["evaluations"].items():
        arm_id, _, task_id = key.partition("/")
        if arm_id != arm or task_id in excluded:
            continue
        values = []
        for rep in ("r1", "r2", "r3"):
            count = reps.get(rep, {}).get("critical_new_failure_count")
            values.append(None if count is None else int(count) > 0)
        resolved = [v for v in values if v is not None]
        if sum(1 for v in resolved if v) > 1 or sum(1 for v in resolved if not v) > 1:
            n += 1
    return n


def per_arm_channel_load(campaign: Path, arms: list[str], reps: list[str],
                         task_ids: list[str]) -> dict[str, dict[str, Any]]:
    """Model calls and per-call token peaks, broken out per arm.

    GR0d and GR0e aggregate over all 1080 calls, so neither would notice if every arm
    made the same number of calls -- which the registered execution-lane contract says
    they must not.  This is the breakdown those two gates cannot see.
    """
    out: dict[str, dict[str, Any]] = {}
    for arm in arms:
        envelopes = calls = peak = 0
        for rep in reps:
            for task_id in task_ids:
                path = campaign / f"run/confirmatory-r{rep}/responses/{arm}/{task_id}.json"
                if not path.is_file():
                    continue
                receipt = json.loads(path.read_text(encoding="utf-8")).get("channel_receipt") or {}
                envelopes += 1
                calls += int(receipt.get("model_calls") or 0)
                peak = max(peak, int(receipt.get("max_output_tokens_observed") or 0))
        out[arm] = {
            "envelopes": envelopes, "model_calls": calls,
            "calls_per_envelope": round(calls / envelopes, 4) if envelopes else None,
            "max_output_tokens_observed": peak,
        }
    return out


def synthetic_campaign(root: Path, arm: str, task_ids: list[str],
                       receipt: dict[str, Any]) -> int:
    """Write a one-arm, one-repetition campaign whose every envelope carries ``receipt``."""
    out = root / f"run/confirmatory-r1/responses/{arm}"
    out.mkdir(parents=True, exist_ok=True)
    for task_id in task_ids:
        (out / f"{task_id}.json").write_text(
            json.dumps({"task_id": task_id, "arm_id": arm,
                        "channel_receipt": dict(receipt)}), encoding="utf-8")
    return len(task_ids)


R12_SIGNATURE = {
    # E30-R12's measured failure, verbatim: the whole budget spent before any text.
    "model_calls": 1, "calls_reporting_a_contract": 1,
    "stop_reasons": ["max_tokens"], "max_output_tokens_observed": 6000,
    "calls_with_zero_text_chars": 1,
}
R13_OBSERVED = {
    "model_calls": 1, "calls_reporting_a_contract": 1,
    "stop_reasons": ["end_turn"], "max_output_tokens_observed": 775,
    "calls_with_zero_text_chars": 0,
}


# ---------------------------------------------------------------------------- checks
def run_checks(campaign: Path, rollup: dict[str, Any], raw: dict[str, Any],
               analysis, r12_campaign: Path | None,
               design: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: str, detail: str, **data: Any) -> None:
        checks.append({"check_id": check_id, "status": status, "detail": detail, **data})

    cell = raw["cells"]["e30r13"]
    arms = list(cell["arms"])
    reps = [str(rep) for rep in cell["reps"]]
    tasks = list(cell["task_ids"])
    gates = rollup["gates"]
    contract_id = gates["GR0d"]["expected_contract_id"]
    contract_sha = gates["GR0d"]["expected_contract_sha256"]

    # -- V1: the published channel gates reproduce from the envelopes on disk ---------
    gr0d = analysis.channel_contract_homogeneity(
        campaign, arms, reps, tasks, contract_id, contract_sha)
    gr0e = analysis.channel_behaviour_conformance(campaign, arms, reps, tasks)
    reproduced = (
        gr0d["status"] == gates["GR0d"]["status"]
        and gr0d["envelopes_read"] == gates["GR0d"]["envelopes_read"]
        and gr0d["model_calls_seen"] == gates["GR0d"]["model_calls_seen"]
        and gr0d["offender_count"] == gates["GR0d"]["offender_count"]
        and gr0e["status"] == gates["GR0e"]["status"]
        and gr0e["offender_count"] == gates["GR0e"]["offender_count"]
        and gr0e["stop_reason_counts"] == gates["GR0e"]["stop_reason_counts"]
        and gr0e["max_output_tokens_observed"] == gates["GR0e"]["max_output_tokens_observed"])
    add("V1_channel_gates_reproduce_from_envelopes", PASS if reproduced else FAIL,
        f"GR0d {gr0d['status']} over {gr0d['envelopes_read']}/{gr0d['envelopes_expected']} "
        f"envelopes and {gr0d['model_calls_seen']} calls, {gr0d['offender_count']} offenders; "
        f"GR0e {gr0e['status']}, stop reasons {gr0e['stop_reason_counts']}, largest single "
        f"call {gr0e['max_output_tokens_observed']} output tokens, "
        f"{gr0e['offender_count']} offenders",
        gr0d_recomputed={k: gr0d[k] for k in
                         ("status", "envelopes_read", "envelopes_expected",
                          "envelopes_with_a_channel_receipt", "model_calls_seen",
                          "model_calls_reporting_a_contract", "contract_sha256_counts",
                          "offender_count")},
        gr0e_recomputed={k: gr0e[k] for k in
                         ("status", "envelopes_with_a_channel_receipt", "model_calls_checked",
                          "stop_reason_counts", "max_output_tokens_observed", "offender_count")})

    # -- V2: the same predicates, replayed over E30-R12's archive --------------------
    # Read-only.  R12's receipts are frozen terminal and nothing here writes to them.
    if r12_campaign is None or not r12_campaign.is_dir():
        add("V2_predicates_replayed_on_e30_r12", COULD_NOT_CHECK,
            f"no E30-R12 campaign directory at {r12_campaign}; the replay did not run "
            "and nothing may be concluded from its absence")
    else:
        envelopes = sorted(r12_campaign.glob("run/confirmatory-r*/responses/*/*.json"))
        r12_tasks = sorted({p.stem for p in envelopes})
        r12_arms = sorted({p.parent.name for p in envelopes})
        r12_reps = sorted({p.parent.parent.parent.name.replace("confirmatory-r", "")
                           for p in envelopes})
        if not envelopes:
            add("V2_predicates_replayed_on_e30_r12", COULD_NOT_CHECK,
                "E30-R12 directory present but holds no response envelopes")
        else:
            d12 = analysis.channel_contract_homogeneity(
                r12_campaign, r12_arms, r12_reps, r12_tasks, contract_id, contract_sha)
            e12 = analysis.channel_behaviour_conformance(
                r12_campaign, r12_arms, r12_reps, r12_tasks)
            # hard_gate_terminal asserts that some hard gate is non-PASS, so it is only
            # asked for a terminal once one of them is.  Both passing here would mean the
            # replay found a conformant campaign, which is itself the failure this check
            # is looking for -- not a terminal to name.
            if d12["status"] == PASS and e12["status"] == PASS:
                terminal = None
            else:
                terminal = analysis.hard_gate_terminal(
                    {"GR0c": {"status": PASS}, "GR0d": d12, "GR0e": e12})["terminal"]
            held = (d12["status"] == COULD_NOT_CHECK and e12["status"] == COULD_NOT_CHECK
                    and terminal == "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ")
            add("V2_predicates_replayed_on_e30_r12", PASS if held else FAIL,
                f"{len(envelopes)} E30-R12 envelopes read, "
                f"{d12['envelopes_with_a_channel_receipt']} carrying a channel receipt: "
                f"GR0d={d12['status']} GR0e={e12['status']} -> {terminal}. "
                "The gate does not silently pass an unreceipted campaign; it reports that "
                "it could not check and halts before any endpoint is read.",
                envelopes_read=len(envelopes),
                envelopes_with_a_channel_receipt=d12["envelopes_with_a_channel_receipt"],
                gr0d_status=d12["status"], gr0e_status=e12["status"],
                terminal=terminal)

    # -- V3: the predicates can fire, and do not fire when they should not -----------
    tmp = Path(tempfile.mkdtemp(prefix="e30r13-verify-"))
    try:
        arm = arms[0]
        made = synthetic_campaign(tmp, arm, tasks,
                                  R12_SIGNATURE | {"contract_ids": [contract_id],
                                                   "contract_sha256s": [contract_sha]})
        fired = analysis.channel_behaviour_conformance(tmp, [arm], ["1"], tasks)
        reasons = Counter(o["reason"] for o in fired["offenders"])
        ok = fired["status"] == FAIL and fired["offender_count"] == 2 * made
        add("V3_gr0e_fires_on_the_e30_r12_signature", PASS if ok else FAIL,
            f"{made} envelopes carrying E30-R12's measured signature (stop_reason "
            f"max_tokens at the cap, zero text characters) -> GR0e {fired['status']} with "
            f"{fired['offender_count']} offenders against the expected {2 * made} "
            f"(one truncation and one zero-text offence each); the offender LIST is capped "
            f"at 50 entries, the COUNT is not, so the listed reasons {dict(reasons)} sum to "
            f"{sum(reasons.values())}, not to the count",
            synthetic_envelopes=made, offender_count=fired["offender_count"],
            offender_reasons_listed=dict(reasons))

        synthetic_campaign(tmp, arm, tasks,
                           R13_OBSERVED | {"contract_ids": [contract_id],
                                           "contract_sha256s": [contract_sha]})
        quiet = analysis.channel_behaviour_conformance(tmp, [arm], ["1"], tasks)
        add("V3b_gr0e_silent_on_conforming_envelopes",
            PASS if quiet["status"] == PASS and quiet["offender_count"] == 0 else FAIL,
            f"the same {made} envelopes rewritten with end_turn and text present -> "
            f"GR0e {quiet['status']}, {quiet['offender_count']} offenders. A gate that "
            "cried wolf here would be switched off on its first real run.")

        drifted = sorted((tmp / f"run/confirmatory-r1/responses/{arm}").glob("*.json"))[0]
        envelope = json.loads(drifted.read_text(encoding="utf-8"))
        envelope["channel_receipt"]["contract_sha256s"] = ["0" * 64]
        drifted.write_text(json.dumps(envelope), encoding="utf-8")
        drift = analysis.channel_contract_homogeneity(
            tmp, [arm], ["1"], tasks, contract_id, contract_sha)
        add("V3c_gr0d_fires_on_contract_drift",
            PASS if drift["status"] == FAIL and drift["offender_count"] == 1 else FAIL,
            f"one envelope out of {made} rewritten with a different contract sha256 -> "
            f"GR0d {drift['status']}, {drift['offender_count']} offenders, "
            f"{len(drift['contract_sha256_counts'])} distinct contract digests. This is the "
            "E30-R12 drift mode -- a condition moving under a fixed served model id.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # -- V4: the per-arm channel load the aggregate gates cannot see -----------------
    load = per_arm_channel_load(campaign, arms, reps, tasks)
    registered = ((design or {}).get("execution_lane_contract") or {}).get(
        "calls_per_task_repetition_by_arm")
    described = "; ".join(
        f"{arm} {item['model_calls']} calls over {item['envelopes']} envelopes "
        f"({item['calls_per_envelope']}/envelope, peak "
        f"{item['max_output_tokens_observed']} output tokens)"
        for arm, item in sorted(load.items()))
    if registered is None:
        add("V4_per_arm_channel_load_matches_the_registered_contract", COULD_NOT_CHECK,
            "no design supplied, so the measured per-arm load could not be compared "
            f"against the registered contract. Measured: {described}", per_arm=load)
    else:
        conforms = all(
            item["calls_per_envelope"] == float(registered.get(arm))
            for arm, item in load.items() if registered.get(arm) is not None)
        distinct = len({item["model_calls"] for item in load.values()})
        add("V4_per_arm_channel_load_matches_the_registered_contract",
            PASS if conforms else FAIL,
            f"{described}. The registered execution-lane contract is {registered} calls "
            f"per task-repetition and every arm "
            f"{'matches it exactly' if conforms else 'does NOT match it'}; the measured "
            f"loads span {distinct} distinct call totals across {len(load)} arms. GR0d and "
            "GR0e aggregate over every call, so neither observes this breakdown and "
            "neither would notice arms that had collapsed onto the same call load.",
            per_arm=load, registered_calls_per_task_repetition=registered,
            conforms=conforms, distinct_call_totals=distinct)

    # -- V5: two arms with identical apply counts are not sharing state --------------
    left, right = "F2_ORION_METABOLIC_FULL", "F0_PARENT_FEDERATION"
    ls, rs = applied_set(cell, left), applied_set(cell, right)
    add("V5_equal_apply_counts_are_coincidence_not_shared_state",
        PASS if ls != rs else FAIL,
        f"{left} applied on {len(ls)} of {len(reps) * len(tasks)} slots and {right} on "
        f"{len(rs)}; the two sets share {len(ls & rs)} slots and are "
        f"{'identical' if ls == rs else 'distinct'}. Equal cardinality alone would not "
        "have distinguished coincidence from a shared evaluation path.",
        left_applied=len(ls), right_applied=len(rs), intersection=len(ls & rs),
        identical=ls == rs)

    # -- V6: the published E2 denominators follow the registered majority rule -------
    excluded = list(rollup.get("E2_excluded_task_ids") or [])
    recon = {arm: e2_checkable_by_majority(cell, arm, excluded) for arm in arms}
    published = {arm: rollup["per_arm"][arm]["E2_tasks_checkable"] for arm in arms}
    countable = {arm: cell["arm_totals"][arm]["counted"] for arm in arms}
    add("V6_e2_denominator_is_tasks_by_majority_not_countable_evaluations",
        PASS if recon == published else FAIL,
        f"reconstructed {recon} against published {published}; countable EVALUATIONS per "
        f"arm are {countable}, which is a different quantity and does not divide by three. "
        f"E2 excludes {excluded} with count, per the registered disposition.",
        reconstructed=recon, published=published, countable_evaluations=countable,
        excluded_task_ids=excluded)

    # -- V7: GR3's margin against the resolution its denominator can offer -----------
    n = gates["GR3"]["checkable_paired_tasks"]
    margin = gates["GR3"]["margin"]
    if not n:
        add("V7_gr3_resolution_against_its_margin", COULD_NOT_CHECK,
            "GR3 reports no checkable paired task count")
    else:
        add("V7_gr3_resolution_against_its_margin", PASS,
            f"GR3 is {gates['GR3']['status']} at n={n}, where the smallest risk difference "
            f"the paired table can express is 1/{n} = {1 / n:.4f}. The registered margin is "
            f"{margin}, which is {(1 / n) / margin:.1f}x finer than the denominator can "
            f"resolve, so no achievable outcome at this n separates non-inferiority within "
            f"{margin} from a {1 / n:.3f} regression. The gate status is real; it is not "
            "informative at this denominator, and the observed upper bound of exactly "
            f"{gates['GR3']['one_sided_97_5_upper_bound']} is the tell.",
            n=n, margin=margin, minimum_resolvable_risk_difference=1 / n,
            ratio=(1 / n) / margin)

    # -- V8: the emitted terminal is the first firing registered clause --------------
    firing = []
    if gates["GR0c"]["status"] != PASS:
        firing.append("LANE_DEFECT")
    if gates["GR2"]["status"] == "REJECT" and gates["GR2"].get("direction") == "F2_DISFAVOURED":
        firing.append("F2_HARMFUL")
    if gates["GR3"]["status"] == FAIL:
        firing.append("CRITICAL_REGRESSION")
    if gates["GR1"]["status"] == FAIL:
        firing.append("INTERFACE_STILL_BROKEN")
    emitted = rollup["routing"]["terminal"]
    add("V8_terminal_is_the_first_firing_registered_clause",
        PASS if firing and firing[0] == emitted else FAIL,
        f"clauses firing in the registered order: {firing or 'none'}; emitted {emitted}. "
        f"GR1 FAIL preempts both PARENT_SUFFICIENT and NO_ARM_SEPARATION, so neither was "
        f"reachable this run. Counterfactually, had GR1 passed, F0's E1 rate "
        f"({rollup['per_arm']['F0_PARENT_FEDERATION']['E1_rate']}) is below F2's "
        f"({rollup['per_arm']['F2_ORION_METABOLIC_FULL']['E1_rate']}), so PARENT_SUFFICIENT "
        f"would still not have fired and the terminal would have been NO_ARM_SEPARATION.",
        firing_clauses=firing, emitted_terminal=emitted,
        parent_sufficient_reachable=False, no_arm_separation_reachable=False)

    # -- V9: the rollup is complete and its denominators are published ---------------
    missing_baselines = [t for t, item in cell["baselines"].items()
                         if item.get("status") == "MISSING"]
    missing_evals = [(k, r) for k, entries in cell["evaluations"].items()
                     for r, v in entries.items() if v.get("status") == "MISSING"]
    slots = sum(len(v) for v in cell["evaluations"].values())
    complete = (raw.get("complete") is True and not missing_baselines and not missing_evals
                and len(cell["evaluations"]) == len(arms) * len(tasks)
                and slots == len(arms) * len(tasks) * len(reps))
    add("V9_rollup_is_complete_over_published_denominators", PASS if complete else FAIL,
        f"complete={raw.get('complete')}; {len(cell['baselines'])} baselines "
        f"({len(missing_baselines)} missing); {len(cell['evaluations'])} arm-task keys = "
        f"{len(arms)} arms x {len(tasks)} tasks; {slots} evaluation slots = that grid x "
        f"{len(reps)} repetitions ({len(missing_evals)} missing). A three-second rollup "
        "over a complete grid is a fast read, not an empty one.",
        baselines=len(cell["baselines"]), missing_baselines=missing_baselines,
        evaluation_keys=len(cell["evaluations"]), evaluation_slots=slots,
        missing_evaluations=len(missing_evals))

    # -- V10: the dispatch guard re-armed after the run -------------------------------
    live = (campaign / "PROTECTED_RUN_AUTHORIZATION.json").exists()
    archived = (campaign / "PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json").exists()
    add("V10_authorization_archived_and_guard_rearmed",
        PASS if archived and not live else FAIL,
        f"live authorization present={live}, archived present={archived}; seed revealed "
        f"post-run as {rollup['seed']}; registered denominators {rollup['denominators']}. "
        "A spent authorization left in place would let a later resubmission dispatch "
        "without a fresh one.",
        live_authorization=live, archived_authorization=archived, seed=rollup["seed"])

    return checks


# ------------------------------------------------------------------------------ main
def exit_code(checks: list[dict[str, Any]]) -> int:
    if any(c["status"] == FAIL for c in checks):
        return 4
    if any(c["status"] == COULD_NOT_CHECK for c in checks):
        return 5
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", type=Path, required=True)
    ap.add_argument("--rollup", type=Path, required=True)
    ap.add_argument("--raw-rollup", type=Path, required=True)
    ap.add_argument("--r12-campaign", type=Path, default=None)
    ap.add_argument("--analysis", type=Path,
                    default=HERE / "e30_r13_analysis.py")
    ap.add_argument("--design", type=Path,
                    default=HERE / "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)

    if sys.version_info < (3, 11):
        # 3.9 swallowed a zip(strict=True) TypeError elsewhere in this repo and let a
        # whole check pass vacuously.  Refuse rather than repeat it.
        print(f"REFUSING: verifier needs >= 3.11, got {sys.version.split()[0]}")
        return 5

    analysis = load_analysis(args.analysis)
    rollup = json.loads(args.rollup.read_text(encoding="utf-8"))
    raw = json.loads(args.raw_rollup.read_text(encoding="utf-8"))
    design = (json.loads(args.design.read_text(encoding="utf-8"))
              if args.design and args.design.is_file() else None)
    checks = run_checks(args.campaign, rollup, raw, analysis, args.r12_campaign, design)

    payload = {
        "schema_version": SCHEMA,
        "verifier_python": sys.version.split()[0],
        "campaign": str(args.campaign),
        "e30_r12_campaign": str(args.r12_campaign) if args.r12_campaign else None,
        "analysis_module": str(args.analysis),
        "design": str(args.design) if design else None,
        "computes_no_endpoint_no_contrast_no_terminal": True,
        "status_counts": dict(Counter(c["status"] for c in checks)),
        "checks": checks,
    }
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    for check in checks:
        print(f"[{check['status']}] {check['check_id']}: {check['detail']}")
    print(f"verifier python {sys.version.split()[0]}; "
          f"{payload['status_counts']}; wrote {args.out}")
    return exit_code(checks)


if __name__ == "__main__":
    raise SystemExit(main())
