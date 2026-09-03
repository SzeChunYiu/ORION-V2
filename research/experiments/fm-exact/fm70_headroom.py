#!/usr/bin/env python3
"""FM70 extension — routing headroom on the exact FM suites.

The FM70 lane terminated at gate 0 on 2026-08-30
(`INSUFFICIENT_ROUTING_SIGNAL_ON_DEVELOPMENT_FOLD`) because pre-outcome task
features carried no recoverable routing signal among SIMPLE / F0 / F2 on 40
BugsInPy defect-repair tasks.  That receipt stands and is not restarted.

This extends it to the exact FM suites, which did not exist when it was written,
and it does so **without fitting anything**.  A regime selector can only pay if
there is *headroom*: instances where some routable arm is correct while the best
single always-arm is wrong.  The headroom is an exact, model-free statistic:

    ceiling      = number of instances on which at least one routable arm is correct
    best_always  = max over arms of the number of instances that arm gets right
    headroom     = ceiling - best_always

If the headroom is zero, no selector - however well fitted, however rich its
features - can beat the best always-arm.  That is a structural fact about the
outcome matrix, not an empirical claim about any particular model, so it needs no
held-out fold and admits no overfitting.

**The statistic is validated before it is believed.**  Run on the same protected
outcome matrices restricted to the *single* parents, it must report a nonzero
headroom; a headroom computation that can only ever return zero would be worth
nothing.  Both checks run in the same execution as the verdict.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

SUITES = {
    "FM10": {
        "dir": "fm10",
        "arm_key": lambda r: r["disposition"],
        "expected_key": lambda e: e["disposition"],
        "federation": "F0_PARENT_FEDERATION",
        "mechanic": "M_F2_TRANSFER_DISCOVERY_FULL",
        "single_parents": [
            "P0_SURFACE_SIMILARITY",
            "P1_SME_STRUCTURE_MAPPING",
            "P2_COMPLETE_HOMOMORPHISM",
            "P3_FIXED_LESSON_INJECTION",
            "P4_INVARIANCE_PARENT",
        ],
    },
    "FM20": {
        "dir": "fm20",
        "arm_key": lambda r: f"{r['disposition']}|" + "".join("1" if c else "0" for c in r["coverage"]),
        "expected_key": lambda e: f"{e['disposition']}|" + "".join("1" if c else "0" for c in e["coverage"]),
        "federation": "F0_PARENT_FEDERATION",
        "mechanic": "M_F2_ABSTRACTION_INDUCTION_FULL",
        "single_parents": [
            "P0_FIXED_LESSON_INJECTION",
            "P1_PLOTKIN_LGG",
            "P2_CANDIDATE_ELIMINATION",
            "P3_MDL_COMPRESSION",
        ],
    },
}


def headroom(suite: str, arms: list[str], base: Path) -> dict:
    cfg = SUITES[suite]
    d = base / cfg["dir"] / "results"
    res = json.loads((d / f"{suite}_PROTECTED_RESULTS_V1.json").read_text())
    cus = json.loads((d / f"{suite}_PROTECTED_EXPECTED_CUSTODY_V1.json").read_text())
    exp = {c["instance_id"]: cfg["expected_key"](c["expected"]) for c in cus["instances"]}
    per = {a: 0 for a in arms}
    ceiling = 0
    for rec in res["instances"]:
        want = exp[rec["instance_id"]]
        best = 0
        for a in arms:
            ok = int(cfg["arm_key"](rec["arms"][a]) == want)
            per[a] += ok
            best = max(best, ok)
        ceiling += best
    n = len(res["instances"])
    best_always = max(per.values())
    return {
        "suite": suite,
        "n": n,
        "arms": arms,
        "always_arm_correct": per,
        "best_always": best_always,
        "best_always_arm": max(per, key=lambda a: per[a]),
        "oracle_routing_ceiling": ceiling,
        "headroom": ceiling - best_always,
    }


def run(base: Path) -> dict:
    out: dict = {
        "schema_version": "orion.v2.fm70-extension.routing-headroom.v1",
        "verdict_scope": "the exact FM suites with protected outcomes",
        "full_arm_set": {},
        "validation_single_parents_only": {},
    }
    for suite, cfg in SUITES.items():
        full = cfg["single_parents"] + [cfg["federation"], cfg["mechanic"]]
        out["full_arm_set"][suite] = headroom(suite, full, base)
        out["validation_single_parents_only"][suite] = headroom(suite, cfg["single_parents"], base)
    zero = all(v["headroom"] == 0 for v in out["full_arm_set"].values())
    live = all(v["headroom"] > 0 for v in out["validation_single_parents_only"].values())
    out["headroom_is_zero_on_full_arm_set"] = zero
    out["statistic_is_live"] = live
    out["terminal"] = (
        "NO_ROUTING_HEADROOM_PARENT_FEDERATION_ALREADY_OPTIMAL"
        if (zero and live)
        else "CANNOT_CHECK"
        if not live
        else "ROUTING_HEADROOM_PRESENT"
    )
    out["authority"] = {
        "grants_scientific_truth": False,
        "grants_F2_superiority": False,
        "grants_field_status": False,
        "grants_submission_readiness": False,
    }
    return out


if __name__ == "__main__":
    import sys

    base = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
    r = run(base)
    print(json.dumps(r, indent=2, sort_keys=True))
    for suite, v in r["full_arm_set"].items():
        c = r["validation_single_parents_only"][suite]
        print(
            f"{suite}: ceiling {v['oracle_routing_ceiling']}/{v['n']}, "
            f"best always {v['best_always']} ({v['best_always_arm']}), "
            f"headroom {v['headroom']}  |  validation (single parents only): "
            f"headroom {c['headroom']}",
            file=sys.stderr,
        )
    print(f"TERMINAL: {r['terminal']}", file=sys.stderr)
    sys.exit(0 if r["terminal"] != "CANNOT_CHECK" else 1)
