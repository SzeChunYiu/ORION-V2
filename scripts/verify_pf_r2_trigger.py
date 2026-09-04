#!/usr/bin/env python3
"""Re-derive the P-F activation trigger from in-repo R2 archives.

The trigger is PF_MACHINE_NATIVE_MECHANISM_FOLLOWUP_PROTOCOL_V1.md §1: it fires only on a
statistically supported FG80 advantage of the full machine-native/F2 arm over the simple
direct control.

Exit codes are three-way on purpose. "Could not check" must never be laundered into a
negative:

    0  FIRED         trigger satisfied
    1  DID_NOT_FIRE  checked, and the required separation is absent or reversed
    2  CANNOT_CHECK  the contrast is unmeasurable from the artifacts on hand

Run --self-test first: it asserts the checker can reach all three verdicts, including the
no-alarm case, before any of its verdicts on real data are trusted.
"""
from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "research/experiments/fmfg-r2/rollup-r2/EVALUATION_SUMMARY_n80.json"

TREATMENT = "F2_FORMAL_DISCOVERY_FULL"
CONTROL = "TARGET_ONLY_DIRECT"

FIRED, DID_NOT_FIRE, CANNOT_CHECK = 0, 1, 2
NAME = {FIRED: "FIRED", DID_NOT_FIRE: "DID_NOT_FIRE", CANNOT_CHECK: "CANNOT_CHECK"}


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value from the discordant cells."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2**n)


def worst_case_p(correct_t: int, correct_c: int, tasks: int) -> float:
    """Least favourable exact McNemar p over every paired table consistent with the margins.

    Aggregate summaries fix only the margins, so the paired table is not identified. The
    difference correct_c - correct_t pins b - c; c ranges over what the margins allow. This
    returns the largest (least significant) p in that family, so a verdict derived from it
    is conservative with respect to the unobserved pairing.
    """
    d = correct_c - correct_t
    b_minus_c = abs(d)
    lo_hi = min(correct_t, correct_c, tasks - max(correct_t, correct_c) + min(correct_t, correct_c))
    worst = 0.0
    for c in range(0, max(0, lo_hi) + 1):
        b = c + b_minus_c
        if b > tasks or b + c > tasks:
            break
        worst = max(worst, mcnemar_exact(b, c))
    return worst if worst else mcnemar_exact(b_minus_c, 0)


def evaluate(summary: dict, alpha: float = 0.05) -> tuple[int, dict]:
    """Return (exit_code, report). Every refusal path returns CANNOT_CHECK, never a negative."""
    facts: dict = {"alpha": alpha}
    arms = summary.get("summary")
    if not isinstance(arms, dict):
        return CANNOT_CHECK, {**facts, "reason": "no `summary` block in the evaluation archive"}

    for name in (TREATMENT, CONTROL):
        if name not in arms:
            return CANNOT_CHECK, {**facts, "reason": f"trigger arm {name} absent from the archive",
                                  "arms_present": sorted(arms)}

    for name in (TREATMENT, CONTROL):
        a = arms[name]
        if not a.get("run_valid", False):
            return CANNOT_CHECK, {**facts, "reason": f"{name} run_valid is false"}
        if a.get("missing_or_invalid", 0) != 0:
            return CANNOT_CHECK, {**facts, "reason": f"{name} has {a['missing_or_invalid']} missing/invalid dispatches"}
        if not a.get("tasks"):
            return CANNOT_CHECK, {**facts, "reason": f"{name} has an empty denominator"}

    t, c = arms[TREATMENT], arms[CONTROL]
    if t["tasks"] != c["tasks"]:
        return CANNOT_CHECK, {**facts, "reason": f"denominators differ: {t['tasks']} vs {c['tasks']}"}

    tasks = t["tasks"]
    # Denominators are published, never implied.
    facts.update({
        "tasks": tasks,
        "treatment": {"arm": TREATMENT, "correct": t["correct"], "accuracy": t["correct"] / tasks},
        "control": {"arm": CONTROL, "correct": c["correct"], "accuracy": c["correct"] / tasks},
        "delta_tasks": t["correct"] - c["correct"],
        "delta_pp": 100 * (t["correct"] - c["correct"]) / tasks,
    })

    if t["correct"] <= c["correct"]:
        facts["reason"] = "the full machine-native arm does not exceed the simple direct control"
        facts["worst_case_exact_p_on_the_deficit"] = worst_case_p(t["correct"], c["correct"], tasks)
        return DID_NOT_FIRE, facts

    p = worst_case_p(t["correct"], c["correct"], tasks)
    facts["worst_case_exact_p"] = p
    if p >= alpha:
        facts["reason"] = f"advantage present but not statistically supported (worst-case p={p:.4g})"
        return DID_NOT_FIRE, facts
    facts["reason"] = "statistically supported advantage over the simple direct control"
    return FIRED, facts


def self_test() -> bool:
    """Assert the checker reaches all three verdicts, including the no-alarm case."""
    ok = True

    def case(label: str, summary: dict, want: int) -> None:
        nonlocal ok
        got, rep = evaluate(summary)
        good = got == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: want {NAME[want]}, got {NAME[got]}"
              f" ({rep.get('reason', '')})")

    def s(tc: int, cc: int, tasks: int = 80, **kw) -> dict:
        base = {"tasks": tasks, "run_valid": True, "missing_or_invalid": 0}
        return {"summary": {TREATMENT: {**base, "correct": tc, **kw},
                            CONTROL: {**base, "correct": cc, **kw}}}

    # It must be able to fire — a checker that can never alarm is worthless.
    case("positive control: treatment 60/80 vs control 30/80", s(60, 30), FIRED)
    # It must be able to stay silent — the no-alarm case, asserted not assumed.
    case("no-alarm control: treatment 41/80 vs control 40/80 (tiny, unsupported)", s(41, 40), DID_NOT_FIRE)
    case("no-alarm control: exact tie 40/80 vs 40/80", s(40, 40), DID_NOT_FIRE)
    # It must refuse rather than report a negative when it cannot see.
    case("cannot-check: trigger arm missing",
         {"summary": {CONTROL: {"tasks": 80, "correct": 42, "run_valid": True, "missing_or_invalid": 0}}},
         CANNOT_CHECK)
    case("cannot-check: invalid dispatches present", s(23, 42, missing_or_invalid=7), CANNOT_CHECK)
    case("cannot-check: empty denominator", s(0, 0, tasks=0), CANNOT_CHECK)
    case("cannot-check: run_valid false", s(23, 42, run_valid=False), CANNOT_CHECK)
    # The real shape, on synthetic numbers, must land on the negative.
    case("real-shape: treatment 23/80 vs control 42/80", s(23, 42), DID_NOT_FIRE)
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", type=Path, default=SUMMARY)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    print(f"interpreter: python {sys.version.split()[0]}")

    if a.self_test:
        print("self-test (checker validated before any verdict is trusted):")
        good = self_test()
        print("self-test:", "PASS" if good else "FAIL")
        return 0 if good else 2

    if not a.summary.exists():
        print(f"verdict: CANNOT_CHECK — archive not found: {a.summary}")
        return CANNOT_CHECK

    code, rep = evaluate(json.loads(a.summary.read_text()))
    print(f"archive: {a.summary}")
    print(f"verdict: {NAME[code]} (exit {code})")
    print(json.dumps(rep, indent=2, sort_keys=True))
    if code == DID_NOT_FIRE:
        print("terminal: NO_R2_EFFECT_TO_EXPLAIN__P_F_STANDALONE_ROUTE_CLOSED_OR_MERGE")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
