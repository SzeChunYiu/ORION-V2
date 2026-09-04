"""Deductive extension registered in ADDENDUM.md after the primary calibration.

Exact subset-sum parent for joint transport, and audit-benefit supermodularity.
No protected experiment, model validation, or external authority is implied.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from fractions import Fraction as Q

from transport import (
    CannotCheck, distribution, mask, probability, mass, subsets,
    fixed_event, joint_frontier, audit_bound,
)
from checks import integer_simplex, require, valid_witness


def subset_sum_frontier(p, old, mutable, epsilon, eta):
    """CT-03b: exact reachable-mass DP; no integer denominator inflation.

    Removing old failures is weakly dominated. Track one representative mask
    for each attainable added mass, preferring nonempty supports in zero ties.
    State count can be exponential; this is a faithful parent, not a speed claim.
    """
    pp = distribution(p)
    old, mutable = mask(old, len(pp)), mask(mutable, len(pp))
    epsilon, eta = probability(epsilon), probability(eta)
    useful = mutable & ~old
    states = {Q(0): 0}
    transitions = 0
    for i, weight in enumerate(pp):
        if not useful & (1 << i):
            continue
        for value, selected in list(states.items()):
            transitions += 1
            candidate_value = value + weight
            if candidate_value > eta:
                continue
            candidate = selected | (1 << i)
            previous = states.get(candidate_value)
            if previous is None or (candidate.bit_count(), -candidate) > (previous.bit_count(), -previous):
                states[candidate_value] = candidate
    best_value = max(states)
    selected = states[best_value]
    result = fixed_event(pp, old | selected, epsilon)
    return result, {"reachable_masses": len(states), "transitions": transitions,
                    "added_mass": str(best_value), "added_mask": selected}


def run():
    pairs = total_states = transitions = max_states = supermodular = nested = 0
    grid = list(integer_simplex(3, 3))
    for weights in grid:
        p = tuple(Q(x, 3) for x in weights)
        for old in range(8):
            for mutable in range(8):
                useful = mutable & ~old
                for e in range(4):
                    epsilon = Q(e, 3)
                    for h in range(4):
                        eta = Q(h, 3)
                        parent, work = subset_sum_frontier(p, old, mutable, epsilon, eta)
                        brute = joint_frontier(p, old, mutable, epsilon, eta)
                        require(parent.risk == brute.bound.risk, (p, old, mutable, e, h))
                        require(mass(p, parent.event ^ old) <= eta, "change-mass witness")
                        require(not (parent.event ^ old) & ~mutable, "mutable mask witness")
                        valid_witness(p, epsilon, parent)
                        pairs += 1
                        transitions += work["transitions"]
                        total_states += work["reachable_masses"]
                        max_states = max(max_states, work["reachable_masses"])
                    audits = list(subsets(useful))
                    risks = {a: audit_bound(p, old, mutable, a, epsilon).risk for a in audits}
                    for a in audits:
                        for b in audits:
                            # Benefit supermodular <=> residual risk submodular.
                            require(risks[a]+risks[b] >= risks[a|b]+risks[a&b],
                                    ("supermodularity", p, old, mutable, epsilon, a, b))
                            supermodular += 1
                            if not a & ~b:
                                require(risks[b] <= risks[a], "audit monotonicity")
                                nested += 1
    p = (Q(1, 2), Q(1, 2))
    risks = {a: audit_bound(p, 0, 3, a, Q(1, 2)).risk for a in range(4)}
    gains = {a: risks[0] - r for a, r in risks.items()}
    require(gains[1]+gains[2] < gains[3]+gains[0], "strict submodularity counterexample")
    require(gains[1] == gains[2] == 0 and gains[3] == 1, "zero-marginal stopping defect")
    return {
        "study": "ME-CERTIFICATE-TRANSPORT-V1-DEDUCTIVE-ADDENDUM",
        "registration": "ADDENDUM.md, after first primary run, before this supplementary run",
        "terminal": "EXACT_FINITE_PARENT_PARITY_AND_SUPERMODULARITY_CALIBRATION",
        "counts": {"joint_parent_pairs": pairs, "subset_sum_transitions": transitions,
                   "reachable_mass_states_total": total_states, "max_reachable_mass_states": max_states,
                   "supermodular_inequalities": supermodular, "nested_monotonicity_checks": nested},
        "strict_counterexample": {"P": ["1/2", "1/2"], "old": 0, "mutable": 3,
                                  "epsilon": "1/2", "risk_by_audited_mask": {str(a): str(r) for a,r in risks.items()},
                                  "submodularity_claim_refuted": True},
        "authority": {"novelty": "NOT_ESTABLISHED", "independent_review": False,
                      "real_model_validity": False, "all_size_proof_from_enumeration": False},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args(argv)
    try:
        result = run()
        if args.verify:
            require(json.loads(args.verify.read_text()) == result, "supplementary result drift")
        text = json.dumps(result, sort_keys=True, indent=2) + "\n"
        if args.output:
            args.output.write_text(text)
        else:
            print(text, end="")
        return 0
    except (CannotCheck, ValueError, OSError) as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (AssertionError, ArithmeticError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
