"""Deterministic reference calibration; the accompanying proof is not enumeration."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys

from threshold_lifecycle import (Context, Observation, Snapshot, identify,
                                 optimal_repair_queries, predict, revoke,
                                 tolerates_revocations, version_space)


def check():
    context = Context("reference_host", "integer_guard", "exact_v1", "epoch_1")

    def records(points, theta, units=None):
        units = units or [f"unit_{i}" for i in range(len(points))]
        return Snapshot(context, tuple(Observation(f"record_{i}", units[i], x, int(x >= theta), context)
                                       for i, x in enumerate(points)))

    def oracle(theta):
        serial = itertools.count()

        def ask(x):
            name = f"oracle_{next(serial)}"
            return Observation(name, name, x, int(x >= theta), context)
        return ask

    interval_cases = 0
    for lower in range(-3, 4):
        for size in range(1, 33):
            upper = lower + size - 1
            worst = 0
            for theta in range(lower, upper + 1):
                snapshot = records((lower - 1, upper), theta)
                result = identify(snapshot, oracle(theta))
                assert result.status == "IDENTIFIED" and result.threshold == theta
                worst = max(worst, len(result.query_points))
                interval_cases += 1
            assert worst == optimal_repair_queries(snapshot) == (size - 1).bit_length()

    deletion_cases = 0
    for left, right in itertools.product(range(1, 4), repeat=2):
        snapshot = records((-1,) * left + (0,) * right, 0)
        units = tuple(r.revocation_unit for r in snapshot.records)
        for r in range(4):
            survives = True
            for k in range(min(r, len(units)) + 1):
                for deleted in itertools.combinations(units, k):
                    revised = revoke(snapshot, frozenset(deleted))
                    survives &= version_space(revised).cardinality == 1
                    deletion_cases += 1
            assert survives == tolerates_revocations(snapshot, r) == (min(left, right) > r)

    full = records((-1, 0, 2), 1)
    compressed = Snapshot(context, full.records[1:])
    deletion = frozenset({"unit_1"})
    assert version_space(full) == version_space(compressed)
    assert predict(revoke(full, deletion), -1).status == "LIVE"
    assert predict(revoke(compressed, deletion), -1).status == "UNKNOWN"

    large_targets = (-(10**100), -1025, -1, 0, 1, 1025, 10**100)
    for theta in large_targets:
        result = identify(Snapshot(context), oracle(theta), max_queries=1024, max_integer_bits=512)
        assert result.status == "IDENTIFIED" and result.threshold == theta
        assert len(result.query_points) <= 2 * (abs(theta) + 1).bit_length() + 4

    root = Path(__file__).resolve().parents[3]
    folder = Path(__file__).resolve().parent
    sources = [folder / name for name in ("PROTOCOL_V1.json", "PROTOCOL_V2.json",
               "PROOFS_AND_PARENT_REDUCTION_V1.md", "threshold_lifecycle.py", "check.py")]
    sources.append(root / "tests/unit/test_infinite_threshold_lifecycle.py")
    return {
        "schema": "ORION_INFINITE_THRESHOLD_LIFECYCLE_CALIBRATION_V2",
        "status": "PASS",
        "scope": "REFERENCE_CALIBRATION_OF_PROVED_INFINITE_INTEGER_THRESHOLD_CLASS",
        "scientific_promotion": "NONE",
        "parent_disposition": "PARENT_SUFFICIENT",
        "grammar_frontier": "SHRG_CCG_F7_REMAINS_OPEN",
        "protocol": "PROTOCOL_V2.json",
        "registration_order": "V1_BEFORE_INITIAL_CALIBRATION__V2_SCOPE_CLARIFICATION_BEFORE_THIS_SUCCESSOR_RUN",
        "finite_interval_target_cases": interval_cases,
        "revocation_subset_cases": deletion_cases,
        "large_integer_representation_controls": len(large_targets),
        "compression_loses_useful_retention": "CONFIRMED",
        "sources": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in sources},
    }


def main():
    if not __debug__:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": "assertion-based calibration requires normal Python"}))
        return 2
    try:
        result = check()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "reason": f"{type(exc).__name__}: {exc}"}))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
