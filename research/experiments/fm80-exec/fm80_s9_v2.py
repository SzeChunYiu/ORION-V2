"""FM80 §9 execution amendment V2 — reserve draw, witness screen and the registered routing table.

Frozen design: research/experiments/fm80-exec/FM80_SECTION_9_EXECUTION_AMENDMENT_V2.{md,json}.

The routing table decides, per counting domain, whether the §9.1 contrast is reachable *at all* on
this instrument, before any treatment arm is dispatched. FG80 R3 put five arms at 80/80 on the same
channel one day earlier; a categorical endpoint compared in percentage points is exactly the shape
that saturates. Row 1's 0.90 is derived rather than chosen: §9.1 needs A3 >= best + 0.10 and no
accuracy exceeds 1.00.

Every predicate here is registered before any model call. `--self-test` plants a case that MUST hit
each row and asserts the no-alarm case for each, because a router that cannot fire is worth nothing
and a router that always fires is worse.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from typing import Any

CEILING = 0.90          # derived: s9.1 needs best + 0.10 <= 1.00
FLOOR = 0.10
NARROW = 0.80
MINORITY_MIN = 0.20     # witness non-degeneracy
BAR_PER_DOMAIN = 61     # repair branch 1, selected in the amendment

CEILING_ROW = "AT_CEILING__SECTION_9_1_UNREACHABLE_BY_ARITHMETIC"
FLOOR_ROW = "AT_FLOOR__NO_DYNAMIC_RANGE_FOR_THE_SECTION_9_CONTRAST"
MAJORITY_ROW = "BASELINE_DOES_NOT_BEAT_THE_MAJORITY_CLASS__INSTRUMENT_UNINFORMATIVE"
NARROW_ROW = "NARROW_HEADROOM__A3_MUST_REACH_NEAR_PERFECT_TO_CLEAR_10_PP"
PROCEED_ROW = "DYNAMIC_RANGE_PRESENT__PROCEED"
DEGENERATE = "WITNESS_DEGENERATE__CANNOT_EXPOSE_A_WRONG_TRANSFER"
PROGRAMME_NO_RANGE = "FM80_S9_INSTRUMENT_WITHOUT_DYNAMIC_RANGE__NO_VERDICT_REACHABLE"

COUNTS: dict[str, bool] = {
    CEILING_ROW: False, FLOOR_ROW: False, MAJORITY_ROW: False,
    NARROW_ROW: True, PROCEED_ROW: True,
}


def route_domain(acc0: float, acc1: float, maj: float) -> dict[str, Any]:
    """Registered routing table. First matching row wins; order is part of the freeze."""
    for value, name in ((acc0, "acc0"), (acc1, "acc1"), (maj, "maj")):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name}={value!r} outside [0,1]; refusing rather than reporting a row")
    best = max(acc0, acc1)
    if best >= CEILING:
        row, disp = 1, CEILING_ROW
    elif best <= FLOOR:
        row, disp = 2, FLOOR_ROW
    elif best <= maj:
        row, disp = 3, MAJORITY_ROW
    elif best >= NARROW:
        row, disp = 4, NARROW_ROW
    else:
        row, disp = 5, PROCEED_ROW
    return {"row": row, "disposition": disp, "best": best, "acc0": acc0, "acc1": acc1,
            "maj": maj, "counts_toward_section_9": COUNTS[disp]}


def witness_screen(labels: list[str]) -> dict[str, Any]:
    """FM80 s3f: a witness that cannot expose a wrong transfer is no witness."""
    if not labels:
        return {"status": "CANNOT_CHECK", "reason": "no labels", "n": 0}
    counts = Counter(labels)
    n = len(labels)
    minority = min(counts.values()) / n if len(counts) > 1 else 0.0
    ok = len(counts) > 1 and minority >= MINORITY_MIN
    return {"status": "NON_DEGENERATE" if ok else DEGENERATE, "n": n,
            "classes": dict(counts), "minority_share": round(minority, 4),
            "threshold": MINORITY_MIN, "counts_toward_section_9": ok}


def programme_terminal(domain_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Step-4 evaluation, over the three ASSEMBLED counting domains.

    Refuses on fewer than three rather than returning a terminal. Called with two -- as the
    range-finding probe would, since the third domain is not assembled until step 4 -- it
    would otherwise return PROGRAMME_NO_RANGE unconditionally, manufacturing exactly the
    structurally guaranteed negative this design exists to prevent, and a reader could not
    tell it from a real one.
    """
    if len(domain_rows) < 3:
        raise ValueError(
            f"programme_terminal needs three assembled domains, got {len(domain_rows)}: "
            f"{sorted(domain_rows)}. At probe stage report per-domain routing only.")
    counting = [d for d, r in domain_rows.items() if r["counts_toward_section_9"]]
    if len(counting) < 3:
        return {"terminal": PROGRAMME_NO_RANGE, "counting_domains": counting,
                "reading": ("an instrument terminal. NEVER evidence that structural donor discovery "
                            "or typed transfer adds nothing. A saturated or uninformative instrument "
                            "is silent, not exculpatory.")}
    return {"terminal": "PROCEED_TO_STAGE_A", "counting_domains": counting}


def draw_reserve(seed: str, case_ids: list[str], k: int) -> list[str]:
    """Deterministic seeded draw. Keyed hash rather than random.shuffle so the draw is reproducible
    from the revealed seed alone, on any interpreter version."""
    scored = sorted(case_ids, key=lambda c: hashlib.sha256(f"{seed}:{c}".encode()).hexdigest())
    return scored[:k]


def _self_test() -> int:
    checks: list[tuple[str, bool]] = []

    # Every row must be reachable by a planted case -- a router that cannot fire is worth nothing.
    checks.append(("row1 ceiling fires", route_domain(0.95, 0.30, 0.60)["row"] == 1))
    checks.append(("row1 fires exactly at 0.90", route_domain(0.90, 0.10, 0.50)["row"] == 1))
    checks.append(("row2 floor fires", route_domain(0.05, 0.08, 0.02)["row"] == 2))
    checks.append(("row3 majority fires", route_domain(0.60, 0.55, 0.64)["row"] == 3))
    checks.append(("row4 narrow fires", route_domain(0.85, 0.40, 0.60)["row"] == 4))
    checks.append(("row5 proceed fires", route_domain(0.72, 0.55, 0.64)["row"] == 5))

    # No-alarm: a healthy instrument must NOT be routed out. This is the half that a checker
    # written only to catch saturation would omit, and it is why FG80's lesson generalises.
    healthy = route_domain(0.75, 0.68, 0.64)
    checks.append(("no-alarm: healthy domain proceeds", healthy["disposition"] == PROCEED_ROW))
    checks.append(("no-alarm: healthy domain counts", healthy["counts_toward_section_9"] is True))
    checks.append(("ceiling does not count", route_domain(0.99, 0.99, 0.64)["counts_toward_section_9"] is False))
    checks.append(("narrow still counts", route_domain(0.85, 0.40, 0.60)["counts_toward_section_9"] is True))

    # Order matters: a domain both at ceiling and below majority routes to ceiling, the earlier row.
    checks.append(("row order: ceiling precedes majority", route_domain(0.95, 0.10, 0.97)["row"] == 1))

    # Out-of-range refuses rather than reporting a row.
    try:
        route_domain(1.5, 0.5, 0.5)
        checks.append(("refuses out-of-range", False))
    except ValueError:
        checks.append(("refuses out-of-range", True))

    # Witness screen: planted degenerate, planted healthy, planted just-under threshold.
    checks.append(("witness: constant is degenerate",
                   witness_screen(["PASS"] * 50)["status"] == DEGENERATE))
    checks.append(("witness: 10/90 split is degenerate",
                   witness_screen(["PASS"] * 90 + ["FAIL"] * 10)["status"] == DEGENERATE))
    checks.append(("no-alarm: 36/64 split is non-degenerate",
                   witness_screen(["PASS"] * 36 + ["FAIL"] * 64)["status"] == "NON_DEGENERATE"))
    checks.append(("witness: exactly 20 % passes",
                   witness_screen(["PASS"] * 20 + ["FAIL"] * 80)["status"] == "NON_DEGENERATE"))
    checks.append(("witness: empty is CANNOT_CHECK not a pass",
                   witness_screen([])["status"] == "CANNOT_CHECK"))

    # Programme terminal.
    two_ok = {"a": {"counts_toward_section_9": True}, "b": {"counts_toward_section_9": True},
              "c": {"counts_toward_section_9": False}}
    three_ok = {k: {"counts_toward_section_9": True} for k in "abc"}
    checks.append(("programme: 2 of 3 -> instrument terminal",
                   programme_terminal(two_ok)["terminal"] == PROGRAMME_NO_RANGE))
    checks.append(("no-alarm: 3 of 3 -> proceed",
                   programme_terminal(three_ok)["terminal"] == "PROCEED_TO_STAGE_A"))

    # Reserve draw is deterministic, seed-sensitive, and a subset.
    ids = [f"C-{i}" for i in range(200)]
    d1, d2 = draw_reserve("seedA", ids, 30), draw_reserve("seedA", ids, 30)
    d3 = draw_reserve("seedB", ids, 30)
    checks.append(("draw deterministic", d1 == d2))
    checks.append(("draw seed-sensitive", d1 != d3))
    checks.append(("draw is a subset of size k", len(set(d1)) == 30 and set(d1) <= set(ids)))

    failed = [n for n, ok in checks if not ok]
    for name, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"{len(checks) - len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--route", nargs=3, type=float, metavar=("ACC0", "ACC1", "MAJ"))
    a = ap.parse_args()
    if a.self_test:
        return _self_test()
    if a.route:
        print(json.dumps(route_domain(*a.route), indent=2))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
