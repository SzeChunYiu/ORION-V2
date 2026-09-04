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

    def validate(self, possible_decisive_sets):
        if self.capacity < 0:
            raise ValueError("negative capacity")
        if len(self.candidates) > self.capacity:
            return "CAPACITY_OVERFLOW"
        union = frozenset().union(*possible_decisive_sets) if possible_decisive_sets else frozenset()
        if not union <= self.candidates:
            return "COVERAGE_NOT_PROVED"
        return "CERTIFIED"


def deterministic_impossibility(n=4, k=2):
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
    union = frozenset().union(*possible_decisive_sets) if possible_decisive_sets else frozenset()
    return len(union) <= k, union


def randomized_uniform_k_subset(n=4, k=2):
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
    assert cert.validate(possible) == "CERTIFIED"

    overflow = ExtractionCoverageCertificate(frozenset({"a", "b", "c"}), 2, "registered-family", "z1", "checker-v1", "S", "e1")
    assert overflow.validate((frozenset({"a"}),)) == "CAPACITY_OVERFLOW"

    too_many = (frozenset({"a"}), frozenset({"b"}), frozenset({"c"}))
    ok2, union2 = union_condition(too_many, 2)
    assert not ok2 and len(union2) == 3
    undercert = ExtractionCoverageCertificate(frozenset({"a", "b"}), 2, "registered-family", "z1", "checker-v1", "S", "e1")
    assert undercert.validate(too_many) == "COVERAGE_NOT_PROVED"

    no_alarm = (frozenset({"a"}), frozenset({"a", "b"}))
    ok3, union3 = union_condition(no_alarm, 2)
    assert ok3 and ExtractionCoverageCertificate(union3, 2, "f", "z", "c", "S", "e").validate(no_alarm) == "CERTIFIED"

    return {
        "deterministic": det,
        "randomized_inclusion_probability": str(min(probs.values())),
        "randomized_worst_case_miss_probability": str(randomized_worst_case_miss),
        "certified_positive_case": 1,
        "capacity_overflow_rejected": 1,
        "union_exceeds_capacity_impossible": 1,
        "undercertificate_rejected": 1,
        "capacity_exact_no_alarm": 1,
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
