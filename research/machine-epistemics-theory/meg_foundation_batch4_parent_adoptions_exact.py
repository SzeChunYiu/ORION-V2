"""Exact policy/counterexample checker for Foundation Batch 4 parent adoptions.

MEG-14: demonstrates that helpful-teacher teaching dimension and adaptive membership-query
complexity are distinct information resources on a finite concept class.
MEG-32: enforces that ordinary non-rejection of a difference is not an equivalence terminal;
a predeclared margin plus a registered paired-equivalence interval/test is required.

Exit 0 PASS, 1 FAIL, 2 CANNOT_CHECK. No novelty claim.
"""
from __future__ import annotations

import itertools
import json
from functools import lru_cache


class CannotCheck(RuntimeError):
    pass


def teaching_dimension(concepts):
    """Worst-target minimum helpful-teacher set size for a finite Boolean class."""
    C = tuple(tuple(x) for x in concepts)
    n = len(C[0])
    per_target = []
    for f in C:
        best = None
        for k in range(n + 1):
            for S in itertools.combinations(range(n), k):
                if all(any(f[i] != g[i] for i in S) for g in C if g != f):
                    best = k
                    break
            if best is not None:
                break
        if best is None:
            raise CannotCheck("duplicate/indistinguishable concepts")
        per_target.append(best)
    return max(per_target), tuple(per_target)


def membership_query_complexity(concepts):
    """Minimum worst-case adaptive decision-tree depth using coordinate membership queries."""
    C = tuple(sorted(tuple(x) for x in concepts))
    n = len(C[0])

    @lru_cache(None)
    def dp(V):
        if len(V) <= 1:
            return 0
        best = None
        for i in range(n):
            groups = {}
            for h in V:
                groups.setdefault(h[i], []).append(h)
            if len(groups) < 2:
                continue
            cand = 1 + max(dp(tuple(sorted(group))) for group in groups.values())
            best = cand if best is None else min(best, cand)
        if best is None:
            raise CannotCheck("no distinguishing membership query")
        return best

    return dp(C)


def check_meg14():
    C = ((0, 0, 0), (0, 1, 1), (1, 0, 1))
    td, per = teaching_dimension(C)
    mq = membership_query_complexity(C)
    assert td == 1 and per == (1, 1, 1)
    assert mq == 2
    assert td != mq
    two = ((0, 0), (1, 1))
    td2, _ = teaching_dimension(two)
    mq2 = membership_query_complexity(two)
    assert td2 == mq2 == 1
    return {
        "counterexample_class": [list(x) for x in C],
        "teaching_dimension": td,
        "membership_query_complexity": mq,
        "td_equals_mq_refuted": 1,
        "equality_can_hold_no_alarm": 1,
    }


def equivalence_decision(*, ordinary_difference_p=None, alpha=0.05, margin=None, ci=None, method_id=None):
    """Policy layer only: consumes an interval from a registered paired-equivalence method."""
    if margin is None or method_id is None or ci is None:
        return "CANNOT_CHECK"
    if margin <= 0:
        raise ValueError("equivalence margin must be positive")
    lo, hi = ci
    if lo > hi:
        raise ValueError("invalid interval")
    return "EQUIVALENT" if (-margin < lo and hi < margin) else "NOT_EQUIVALENT_OR_INCONCLUSIVE"


def mutant_nonsignificant_means_equivalent(p, alpha=0.05):
    return "EQUIVALENT" if p > alpha else "NOT_EQUIVALENT"


def check_meg32():
    # Superficially strong tie: ordinary difference p=1.0, but no equivalence margin/interval.
    p = 1.0
    assert mutant_nonsignificant_means_equivalent(p) == "EQUIVALENT"
    assert equivalence_decision(ordinary_difference_p=p) == "CANNOT_CHECK"
    # A registered paired-equivalence result wholly inside the predeclared margin can pass.
    assert equivalence_decision(alpha=0.05, margin=0.10, ci=(-0.04, 0.05), method_id="paired-exact-v1") == "EQUIVALENT"
    # Point estimate/tie is not enough if uncertainty crosses the margin.
    assert equivalence_decision(alpha=0.05, margin=0.10, ci=(-0.12, 0.08), method_id="paired-exact-v1") == "NOT_EQUIVALENT_OR_INCONCLUSIVE"
    assert equivalence_decision(alpha=0.05, margin=0.10, ci=(-0.09, 0.11), method_id="paired-exact-v1") == "NOT_EQUIVALENT_OR_INCONCLUSIVE"
    return {
        "ordinary_p_nonrejection_not_equivalence": 1,
        "missing_margin_or_interval_is_cannot_check": 1,
        "registered_interval_inside_margin_equivalent": 1,
        "interval_crossing_margin_refused": 2,
        "p_gt_alpha_mutant_caught": 1,
    }


def run_all():
    return {"MEG-14": check_meg14(), "MEG-32": check_meg32(), "GENERAL_NOVELTY": "NOT_ESTABLISHED"}


def main():
    try:
        out = run_all()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}, sort_keys=True))
        return 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "type": type(exc).__name__, "reason": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps({"status": "PASS", "result": out}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
