"""Exact checker for MEG-07 extraction no-drop impossibility and certificate condition.

The theorem is information/capacity based, not specific to PageRank/surprise. Finite enumeration
here supplies hostile witnesses; the general proof is in ME_FRONTIER_F1_EXTRACTION_NO_DROP_V1.md.

Exit 0 PASS, 1 FAIL, 2 CANNOT_CHECK. No novelty claim.
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


@dataclass(frozen=True)
class ExtractionCoverageCertificate:
    candidates: frozenset[str]
    capacity: int
    task_family: str
    state_digest: str
    checker_id: str
    scope: str
    epoch: str

    def validate(
        self,
        possible_decisive_sets,
        *,
        capacity: int,
        task_family: str,
        state_digest: str,
        checker_id: str,
        scope: str,
        epoch: str,
    ):
        if self.capacity < 0 or capacity < 0:
            raise ValueError("negative capacity")
        expected = (capacity, task_family, state_digest, checker_id, scope, epoch)
        bound = (self.capacity, self.task_family, self.state_digest, self.checker_id, self.scope, self.epoch)
        if bound != expected:
            return "CANNOT_CHECK_IDENTITY_DRIFT"
        if len(self.candidates) > self.capacity:
            return "CAPACITY_OVERFLOW"
        union = frozenset().union(*possible_decisive_sets) if possible_decisive_sets else frozenset()
        if not union <= self.candidates:
            return "COVERAGE_NOT_PROVED"
        return "CERTIFIED"


def deterministic_impossibility(n=4, k=2):
    if not (0 <= k < n):
        raise ValueError("registered impossibility witness requires 0 <= k < n")
    V = tuple(f"v{i}" for i in range(n))
    selectors = []
    for size in range(k + 1):
        selectors.extend(frozenset(x) for x in itertools.combinations(V, size))
    checked = misses = 0
    for S in selectors:
        per_selector_miss = False
        for v in V:
            D = frozenset({v})
            checked += 1
            if not D <= S:
                per_selector_miss = True
                misses += 1
        assert per_selector_miss, S
    return {"n": n, "k": k, "selectors": len(selectors), "selector_task_pairs": checked, "miss_pairs": misses}


def union_condition(possible_decisive_sets, k):
    if k < 0:
        raise ValueError("negative capacity")
    union = frozenset().union(*possible_decisive_sets) if possible_decisive_sets else frozenset()
    return len(union) <= k, union


def randomized_uniform_k_subset(n=4, k=2):
    if not (0 <= k < n):
        raise ValueError("registered randomized witness requires 0 <= k < n")
    V = tuple(range(n))
    subsets = tuple(itertools.combinations(V, k))
    probs = {}
    for v in V:
        containing = sum(v in S for S in subsets)
        probs[v] = Fraction(containing, len(subsets))
    assert sum(probs.values(), Fraction(0)) == k
    assert all(p == Fraction(k, n) for p in probs.values())
    assert all(p < 1 for p in probs.values())
    return probs


def _validate(cert, possible, **overrides):
    ctx = {
        "capacity": 2,
        "task_family": "registered-family",
        "state_digest": "z1",
        "checker_id": "checker-v1",
        "scope": "S",
        "epoch": "e1",
    }
    ctx.update(overrides)
    return cert.validate(possible, **ctx)


def check_meg07():
    det = deterministic_impossibility(4, 2)
    assert det["selectors"] == 11
    assert det["miss_pairs"] > 0

    probs = randomized_uniform_k_subset(4, 2)
    assert min(probs.values()) == Fraction(1, 2)
    randomized_worst_case_miss = 1 - min(probs.values())
    assert randomized_worst_case_miss == Fraction(1, 2)

    possible = (frozenset({"a"}), frozenset({"b"}), frozenset({"a", "b"}))
    ok, union = union_condition(possible, 2)
    assert ok and union == {"a", "b"}
    cert = ExtractionCoverageCertificate(union, 2, "registered-family", "z1", "checker-v1", "S", "e1")
    assert _validate(cert, possible) == "CERTIFIED"

    overflow = ExtractionCoverageCertificate(frozenset({"a", "b", "c"}), 2, "registered-family", "z1", "checker-v1", "S", "e1")
    assert _validate(overflow, (frozenset({"a"}),)) == "CAPACITY_OVERFLOW"

    too_many = (frozenset({"a"}), frozenset({"b"}), frozenset({"c"}))
    ok2, union2 = union_condition(too_many, 2)
    assert not ok2 and len(union2) == 3
    undercert = ExtractionCoverageCertificate(frozenset({"a", "b"}), 2, "registered-family", "z1", "checker-v1", "S", "e1")
    assert _validate(undercert, too_many) == "COVERAGE_NOT_PROVED"

    no_alarm = (frozenset({"a"}), frozenset({"a", "b"}))
    ok3, union3 = union_condition(no_alarm, 2)
    assert ok3
    no_alarm_cert = ExtractionCoverageCertificate(union3, 2, "registered-family", "z1", "checker-v1", "S", "e1")
    assert _validate(no_alarm_cert, no_alarm) == "CERTIFIED"

    # A true coverage statement for another extractor state/family/checker/scope/epoch/capacity is stale here.
    drift_results = {
        "capacity": _validate(cert, possible, capacity=3),
        "task_family": _validate(cert, possible, task_family="other-family"),
        "state_digest": _validate(cert, possible, state_digest="z2"),
        "checker_id": _validate(cert, possible, checker_id="checker-v2"),
        "scope": _validate(cert, possible, scope="T"),
        "epoch": _validate(cert, possible, epoch="e2"),
    }
    assert set(drift_results.values()) == {"CANNOT_CHECK_IDENTITY_DRIFT"}

    return {
        "deterministic": det,
        "randomized_inclusion_probability": str(min(probs.values())),
        "randomized_worst_case_miss_probability": str(randomized_worst_case_miss),
        "certified_positive_case": 1,
        "capacity_overflow_rejected": 1,
        "union_exceeds_capacity_impossible": 1,
        "undercertificate_rejected": 1,
        "capacity_exact_no_alarm": 1,
        "certificate_identity_drift_dimensions_caught": len(drift_results),
        "terminal": "NO_UNIVERSAL_NO_DROP_WITHOUT_DISCRIMINATING_STRUCTURE",
        "GENERAL_NOVELTY": "NOT_ESTABLISHED",
    }


def main():
    try:
        out = check_meg07()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}, sort_keys=True)); return 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "type": type(exc).__name__, "reason": str(exc)}, sort_keys=True)); return 1
    print(json.dumps({"status": "PASS", "result": out}, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
