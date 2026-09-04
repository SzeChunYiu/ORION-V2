"""Frozen finite calibration; integer-simplex oracle is separate from transport.py.

This is an alternative formulation in ONE authoring session, not independent
external review. No counts/expected successes are read from committed results.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import itertools
import json
from pathlib import Path
import sys

from transport import (MANIFEST_FIELDS, CannotCheck, audit_bound, audit_exhaustive,
                       audit_knapsack, binding_status, fixed_event, joint_frontier,
                       manifest_digest)


def require(condition: bool, context: object) -> None:
    # Deliberately not an assert: checks remain active under python -O.
    if not condition:
        raise AssertionError(context)


def integer_simplex(n: int, total: int):
    if n == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in integer_simplex(n - 1, total - first):
                yield (first,) + rest


def integer_mass(p, bits):
    return sum(p[i] for i in range(len(p)) if (bits >> i) & 1)


def oracle_table(weights, denominator, grid):
    """Brute enumeration of deployment distributions; never calls fixed_event."""
    values = {}
    comparisons = 0
    for e in range(denominator + 1):
        for event in range(1 << len(weights)):
            possible = []
            for q in grid:
                comparisons += 1
                if sum(abs(a - b) for a, b in zip(weights, q)) <= 2 * e:
                    possible.append(integer_mass(q, event))
            require(bool(possible), "reference distribution must be feasible")
            values[e, event] = max(possible)
    return values, comparisons


def valid_witness(p, epsilon, bound):
    q = bound.attaining_distribution
    require(all(x >= 0 for x in q) and sum(q) == 1, "invalid extremal distribution")
    require(sum(abs(a-b) for a, b in zip(p, q)) / 2 <= epsilon, "TV overrun")
    observed = sum((q[i] for i in range(len(p)) if bound.event & (1 << i)), Q(0))
    require(observed == bound.risk, "risk not attained")


def run():
    n, d = 3, 3
    grid = list(integer_simplex(n, d))
    fixed_cells = joint_cells = audit_semantics = audit_pairs = 0
    oracle_comparisons = joint_work = audit_work = dp_work = peak_dp = 0
    for weights in grid:
        p = tuple(Q(x, d) for x in weights)
        table, comparisons = oracle_table(weights, d, grid)
        oracle_comparisons += comparisons
        for old in range(1 << n):
            for e in range(d + 1):
                epsilon = Q(e, d)
                bound = fixed_event(p, old, epsilon)
                require(bound.risk == Q(table[e, old], d), ("fixed", p, old, e))
                valid_witness(p, epsilon, bound)
                fixed_cells += 1
            for mutable in range(1 << n):
                for e in range(d + 1):
                    epsilon = Q(e, d)
                    for h in range(d + 1):
                        result = joint_frontier(p, old, mutable, epsilon, Q(h, d))
                        candidates = [g for g in range(1 << n)
                                      if not (old ^ g) & ~mutable
                                      and integer_mass(weights, old ^ g) <= h]
                        expected = max(table[e, g] for g in candidates)
                        require(result.bound.risk == Q(expected, d),
                                ("joint", weights, old, mutable, e, h, result))
                        require(result.bound.event in candidates, "invalid event witness")
                        require(result.feasible == len(candidates), "wrong denominator")
                        valid_witness(p, epsilon, result.bound)
                        joint_cells += 1
                        joint_work += result.candidates
                    for audited in range(1 << n):
                        if audited & ~mutable:
                            continue
                        compatible = [g for g in range(1 << n)
                                      if not (old ^ g) & ~mutable
                                      and not (old ^ g) & audited]
                        expected = max(table[e, g] for g in compatible)
                        result = audit_bound(p, old, mutable, audited, epsilon)
                        require(result.risk == Q(expected, d),
                                ("audit semantics", p, old, mutable, audited, e))
                        valid_witness(p, epsilon, result)
                        audit_semantics += 1
                    for costs, budgets in (((1, 1, 1), range(4)), ((1, 2, 3), range(7))):
                        for budget in budgets:
                            brute = audit_exhaustive(p, old, mutable, epsilon, costs, budget)
                            parent = audit_knapsack(p, old, mutable, epsilon, costs, budget)
                            require((brute.bound.risk, brute.cost) ==
                                    (parent.bound.risk, parent.cost),
                                    ("parent parity", weights, old, mutable, e, costs, budget))
                            require(parent.cost <= budget and not parent.audited & ~mutable,
                                    "parent audit violates budget/scope")
                            require(parent.bound.risk == audit_bound(
                                p, old, mutable, parent.audited, epsilon).risk,
                                "parent witness mismatch")
                            audit_pairs += 1
                            audit_work += brute.work
                            dp_work += parent.work
                            peak_dp = max(peak_dp, parent.peak_states)
    controls = {}

    def plant(name, mutated, correct):
        require(mutated != correct, ("unapplied or powerless mutant", name))
        controls[name] = {"detected": True, "mutated": str(mutated), "correct": str(correct)}

    p = (Q(1, 4), Q(3, 4))
    plant("omitted_distribution_drift", fixed_event(p, 1, 0).risk,
          fixed_event(p, 1, Q(1, 4)).risk)
    plant("omitted_operator_change", joint_frontier(p, 0, 3, 0, 0).bound.risk,
          joint_frontier(p, 0, 3, 0, Q(1, 4)).bound.risk)
    plant("ignored_mutable_scope", joint_frontier(p, 0, 3, 0, 1).bound.risk,
          joint_frontier(p, 0, 1, 0, 1).bound.risk)
    plant("missing_TV_half", fixed_event(p, 1, Q(1, 8)).risk,
          fixed_event(p, 1, Q(1, 4)).risk)
    p2 = (Q(2, 5), Q(3, 5))
    plant("fractional_relaxation_claimed_exact", Q(1, 2),
          joint_frontier(p2, 0, 3, 0, Q(1, 2)).bound.risk)
    plant("zero_mass_error_declared_impossible", Q(0),
          fixed_event((1, 0), 2, Q(1, 4)).risk)
    plant("empty_event_given_spurious_drift_risk", Q(1, 4),
          fixed_event((1, 0), 0, Q(1, 4)).risk)
    plant("unaudited_region_ignored", Q(0), audit_bound((1, 0), 0, 3, 1, Q(1, 4)).risk)
    plant("revoked_audit_kept_valid", audit_bound(p, 0, 3, 3, 0).risk,
          audit_bound(p, 0, 3, 2, 0).risk)
    # A metadata-only belief that same operator id suffices misses every binding field.
    manifest = {key: "v1:" + key for key in MANIFEST_FIELDS}
    manifest["claim_kind"] = "RISK_BOUND"
    for key in MANIFEST_FIELDS:
        other = dict(manifest)
        other[key] += ":changed"
        require(manifest_digest(other) != manifest_digest(manifest), ("unbound field", key))
        expected = "WRONG_CLAIM_KIND" if key == "claim_kind" else "REVALIDATE"
        require(binding_status(manifest, other, ["calibration:1"]) == expected, key)
    plant("dependency_revocation_ignored", "BINDING_MATCH_ONLY",
          binding_status(manifest, manifest, ["calibration:1"], ["calibration:1"]))
    no_alarm = {
        "canonical_field_order": binding_status(
            manifest, dict(reversed(list(manifest.items()))), ["calibration:1"]) == "BINDING_MATCH_ONLY",
        "unrelated_revocation": binding_status(
            manifest, manifest, ["calibration:1"], ["unrelated"]) == "BINDING_MATCH_ONLY",
        "identity_transport": joint_frontier(p, 1, 0, 0, 0).bound.risk == Q(1, 4),
        "complete_audit": audit_bound((1, 0), 0, 3, 3, Q(1, 4)).risk == 0,
        "full_event": fixed_event(p, 3, 1).risk == 1,
    }
    for name, held in no_alarm.items():
        require(held, ("no-alarm control", name))
    examples = {
        "granularity": joint_frontier(p2, 0, 3, 0, Q(1, 2)).as_dict(),
        "zero_mass_before_audit": audit_bound((1, 0), 0, 2, 0, Q(1, 4)).as_dict(),
        "zero_mass_after_audit": audit_bound((1, 0), 0, 2, 2, Q(1, 4)).as_dict(),
        "audit_curve": [audit_knapsack((Q(1,2), Q(1,3), Q(1,6), 0), 4, 15,
                                      Q(1,12), (3,2,1,1), b).as_dict() for b in range(8)],
    }
    return {
        "study": "ME-CERTIFICATE-TRANSPORT-V1", "terminal": "EXACT_FINITE_PARENT_PARITY",
        "scope": "public complete finite rational model, not empirical calibration",
        "grid": {"atoms": n, "denominator": d, "distributions": len(grid)},
        "counts": {"fixed_event_cells": fixed_cells, "joint_frontier_cells": joint_cells,
                   "audit_semantic_cells": audit_semantics, "audit_parent_pairs": audit_pairs,
                   "oracle_distribution_comparisons": oracle_comparisons,
                   "joint_candidate_masks": joint_work, "exhaustive_audit_masks": audit_work,
                   "parent_DP_work": dp_work, "parent_peak_states": peak_dp,
                   "applied_mutants_detected": len(controls),
                   "manifest_fields_mutated": len(MANIFEST_FIELDS), "no_alarm_controls": len(no_alarm)},
        "controls": controls, "no_alarm": no_alarm, "examples": examples,
        "authority": {"all_size_proof_from_enumeration": False, "independent_review": False,
                      "real_model_coverage": False, "novelty": "NOT_ESTABLISHED",
                      "OCM_adoption": False, "external_action": False},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args(argv)
    try:
        result = run()
        text = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.verify:
            require(json.loads(args.verify.read_text()) == result, "receipt result drift")
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
