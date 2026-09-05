"""Exact checker for MEG-07 extraction no-drop impossibility and certificate condition.

The theorem is information/capacity based, not specific to PageRank/surprise. Finite enumeration
here supplies hostile witnesses; the general proof is in ME_FRONTIER_F1_EXTRACTION_NO_DROP_V1.md.

Exit 0 PASS, 1 FAIL, 2 CANNOT_CHECK. No novelty claim.
"""
from __future__ import annotations

import itertools
import json
import hashlib
import sys
from dataclasses import dataclass
from fractions import Fraction
from math import comb


class CannotCheck(RuntimeError):
    pass


def _capacity(k):
    if type(k) is not int or k < 0:
        raise ValueError("capacity must be a nonnegative integer")


def _atom_set(value):
    if not isinstance(value, (set, frozenset)) or any(type(x) is not str or not x for x in value):
        raise ValueError("atom ids must be an explicit set of nonempty strings")
    return frozenset(value)


def _family(possible):
    if not isinstance(possible, (tuple, list)):
        raise CannotCheck("finite task family must be explicitly enumerated")
    return tuple(_atom_set(d) for d in possible)


def family_digest(universe, possible):
    """Identity of a finite family defined by this exact enumeration, not a sample."""
    universe = _atom_set(universe)
    possible = _family(possible)
    if any(not d <= universe for d in possible):
        raise ValueError("decisive atom outside extraction universe")
    payload = [sorted(universe), sorted({tuple(sorted(d)) for d in possible})]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class ExtractionCoverageCertificate:
    candidates: frozenset[str]
    capacity: int
    task_family: str
    state_digest: str
    checker_id: str
    scope: str
    epoch: str
    universe: frozenset[str] | None = None
    decisive_family_digest: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "candidates", _atom_set(self.candidates))
        if self.universe is not None:
            object.__setattr__(self, "universe", _atom_set(self.universe))

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
        universe=None,
        registered_family_digest=None,
    ):
        _capacity(self.capacity)
        _capacity(capacity)
        expected = (capacity, task_family, state_digest, checker_id, scope, epoch)
        bound = (self.capacity, self.task_family, self.state_digest, self.checker_id, self.scope, self.epoch)
        if any(type(x) is not str or not x for x in expected[1:] + bound[1:]):
            return "CANNOT_CHECK_MALFORMED_IDENTITY"
        if bound != expected:
            return "CANNOT_CHECK_IDENTITY_DRIFT"
        if universe is None or self.universe is None or not registered_family_digest or not self.decisive_family_digest:
            return "CANNOT_CHECK_UNREGISTERED_FINITE_FAMILY"
        if any(type(d) is not str or len(d) != 64 or any(c not in "0123456789abcdef" for c in d)
               for d in (registered_family_digest, self.decisive_family_digest)):
            return "CANNOT_CHECK_MALFORMED_IDENTITY"
        try:
            actual = family_digest(universe, possible_decisive_sets)
            selected = _atom_set(self.candidates)
            if _atom_set(self.universe) != _atom_set(universe):
                return "CANNOT_CHECK_IDENTITY_DRIFT"
        except (ValueError, CannotCheck):
            return "CANNOT_CHECK_MALFORMED_FINITE_FAMILY"
        if actual != registered_family_digest or actual != self.decisive_family_digest:
            return "CANNOT_CHECK_FAMILY_IDENTITY_DRIFT"
        if not selected <= universe:
            return "INELIGIBLE_CANDIDATE"
        if len(self.candidates) > self.capacity:
            return "CAPACITY_OVERFLOW"
        union = frozenset().union(*possible_decisive_sets) if possible_decisive_sets else frozenset()
        if not union <= self.candidates:
            return "COVERAGE_NOT_PROVED"
        return "CERTIFIED"


def deterministic_impossibility(n=4, k=2):
    _capacity(k)
    if type(n) is not int:
        raise ValueError("n must be an integer")
    if not (0 <= k < n):
        raise ValueError("registered impossibility witness requires 0 <= k < n")
    if n > 20 or n * sum(comb(n, size) for size in range(k + 1)) > 1_000_000:
        raise CannotCheck("finite witness enumeration budget exceeded")
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
    _capacity(k)
    possible_decisive_sets = _family(possible_decisive_sets)
    union = frozenset().union(*possible_decisive_sets) if possible_decisive_sets else frozenset()
    return len(union) <= k, union


def randomized_uniform_k_subset(n=4, k=2):
    _capacity(k)
    if type(n) is not int:
        raise ValueError("n must be an integer")
    if not (0 <= k < n):
        raise ValueError("registered randomized witness requires 0 <= k < n")
    if n > 20 or n * comb(n, k) > 1_000_000:
        raise CannotCheck("finite witness enumeration budget exceeded")
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
        "universe": cert.universe,
        "registered_family_digest": cert.decisive_family_digest,
    }
    ctx.update(overrides)
    return cert.validate(possible, **ctx)


def _certificate(selected, possible):
    universe = frozenset({"a", "b", "c"})
    return ExtractionCoverageCertificate(selected, 2, "registered-family", "z1", "checker-v1", "S", "e1",
                                         universe, family_digest(universe, possible))


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
    cert = _certificate(union, possible)
    assert _validate(cert, possible) == "CERTIFIED"

    overflow = _certificate(frozenset({"a", "b", "c"}), (frozenset({"a"}),))
    assert _validate(overflow, (frozenset({"a"}),)) == "CAPACITY_OVERFLOW"

    too_many = (frozenset({"a"}), frozenset({"b"}), frozenset({"c"}))
    ok2, union2 = union_condition(too_many, 2)
    assert not ok2 and len(union2) == 3
    undercert = _certificate(frozenset({"a", "b"}), too_many)
    assert _validate(undercert, too_many) == "COVERAGE_NOT_PROVED"

    no_alarm = (frozenset({"a"}), frozenset({"a", "b"}))
    ok3, union3 = union_condition(no_alarm, 2)
    assert ok3
    no_alarm_cert = _certificate(union3, no_alarm)
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
        if sys.flags.optimize:
            raise CannotCheck("assertions disabled by optimized Python")
        out = check_meg07()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}, sort_keys=True)); return 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "type": type(exc).__name__, "reason": str(exc)}, sort_keys=True)); return 1
    print(json.dumps({"status": "PASS", "result": out}, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
