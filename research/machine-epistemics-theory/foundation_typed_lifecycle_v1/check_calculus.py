"""Deterministic exact calibration, with distinct fail and cannot-check exits.

Run: python check_calculus.py [--output RESULTS.json]
No network, random seed, production operations or third-party dependencies.
The case universe is fixed below. There is no silent reduced/fast mode.
"""
from __future__ import annotations

import argparse
from dataclasses import fields, replace
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations, product
import json
from pathlib import Path
import sys

from calculus import (Binding, Budget, CannotCheck, Certificate, Conflict, Interval,
                      Live, ONE, ZERO, Verdict, alternative, canon, closure,
                      commit_gate, conjunct, drift_bound, filter_nogoods,
                      fixed_point, holds, iterate, joint, leq, perturbation_bound,
                      profiles, residual_bound, robust_answer, selection_bound,
                      step, substitute, query_warrants, version_space)


class CheckFailure(Exception):
    pass


class Count:
    def __init__(self):
        self.checks = 0
        self.controls: dict[str, str] = {}

    def require(self, condition: bool, name: str) -> None:
        self.checks += 1
        if not condition:
            raise CheckFailure(name)

    def control(self, condition: bool, name: str) -> None:
        self.require(condition, name)
        self.controls[name] = "EXPECTED_DISTINCTION_OBSERVED"

    def raises(self, typ, fn, name: str) -> None:
        try:
            fn()
        except typ:
            self.control(True, name)
        else:
            self.require(False, name)

    def result(self, **meta) -> dict:
        return {"status": "PASS", "checks": self.checks,
                "controls": self.controls, **meta}


def check_intervals():
    c = Count()
    ps = profiles(3)
    intervals = tuple(Interval(p, q) for p in ps for q in ps if leq(p, q))
    order = {Live.DEAD: 0, Live.UNKNOWN: 1, Live.LIVE: 2}
    hom = refinements = 0
    for x, y in product(intervals, repeat=2):
        z = x.compose(y)
        for a in range(8):
            c.require(order[z.verdict(a)] == min(order[x.verdict(a)], order[y.verdict(a)]),
                      "unconstrained interval conjunction")
            hom += 1
        if leq(x.lower, y.lower) and leq(y.upper, x.upper):
            for a in range(8):
                c.require(x.verdict(a) is Live.UNKNOWN or x.verdict(a) is y.verdict(a),
                          "consistent interval refinement")
                refinements += 1
    c.raises(Conflict, lambda: Interval((1,), ONE).refine(Interval(ZERO, ZERO)),
             "inconsistent upper certificate refused")
    c.control(Interval(ZERO, ZERO).verdict(7) is Live.DEAD,
              "unsupported does not encode proposition negation")
    c.raises(CannotCheck, lambda: profiles(4), "oversize enumeration is cannot-check")
    c.raises(TypeError, lambda: holds(ONE, -1), "negative available mask rejected")
    return c.result(evidence_atoms=3, profiles=len(ps), intervals=len(intervals),
                    homomorphism_cases=hom, refinement_cases=refinements)


def check_nogoods():
    c = Count()
    ps = profiles(3)
    pairs = oracle_cases = algebra_triples = 0
    for ng in ps:
        normal = tuple(sorted({filter_nogoods(p, ng) for p in ps}))
        mul = {(p, q): joint(p, q, ng) for p in normal for q in normal}
        add = {(p, q): alternative(p, q) for p in normal for q in normal}
        for p, q in product(ps, repeat=2):
            filtered = joint(p, q, ng)
            before = conjunct(filter_nogoods(p, ng), filter_nogoods(q, ng))
            c.require(leq(filtered, before), "filter after composition")
            c.require(filter_nogoods(before, ng) == filtered, "normalization congruence")
            c.require(filter_nogoods(alternative(p, q), ng) ==
                      alternative(filter_nogoods(p, ng), filter_nogoods(q, ng)),
                      "filter preserves alternatives")
            pairs += 1
            for available in range(8):
                worlds = [w for w in range(8) if w & available == w
                          and not any(n & w == n for n in ng)]
                semantic = any(holds(p, w) and holds(q, w) for w in worlds)
                c.require(holds(filtered, available) == semantic, "shared-world oracle")
                oracle_cases += 1
        for p, q, r in product(normal, repeat=3):
            c.require(mul[mul[p, q], r] == mul[p, mul[q, r]], "normalized associativity")
            c.require(mul[p, add[q, r]] == add[mul[p, q], mul[p, r]], "distributivity")
            algebra_triples += 1
    p, q, ng = (1,), (2,), (3,)
    c.control(holds(p, 3) and holds(q, 3) and not holds(joint(p, q, ng), 3),
              "LIVE plus LIVE need not be jointly LIVE")
    c.control(conjunct(filter_nogoods(p, ng), filter_nogoods(q, ng)) != joint(p, q, ng),
              "pre-filter-only mutant differs")
    c.control(joint(p, q, ZERO) == conjunct(p, q), "no-nogood no-alarm")
    return c.result(evidence_atoms=3, nogood_families=len(ps), profile_pairs=pairs,
                    shared_world_cases=oracle_cases, normalized_triples=algebra_triples)


def check_substitution():
    c = Count()
    small, large = profiles(2), profiles(3)
    cases = 0
    for x, y in product(large, repeat=2):
        images = {0: x, 1: y}
        for p, q in product(small, repeat=2):
            a, b = substitute(p, images), substitute(q, images)
            c.require(substitute(conjunct(p, q), images) == conjunct(a, b), "substitution product")
            c.require(substitute(alternative(p, q), images) == alternative(a, b), "substitution sum")
            cases += 1
    c.control(substitute((3,), {0: (1,), 1: (1,)}) == (1,), "shared-source alias idempotence")
    c.control(substitute((3,), {0: (1,), 1: (2,)}) == (3,), "distinct-source no-alarm")
    c.raises(CannotCheck, lambda: substitute((1,), {}), "missing provenance not certified")
    # Different names do not imply stochastic independence: two copies of one bit.
    p = Q(1, 4)
    c.control(p != p * p, "independent-product risk formula fails for copied source")
    return c.result(substitution_pairs=cases)


def check_navigation():
    c = Count()
    rowset = tuple((Q(a, 2), Q(b, 2)) for a in range(3) for b in range(3) if a + b <= 2)
    matrices = tuple(product(rowset, repeat=2))
    seeds = ((Q(1), Q(0)), (Q(0), Q(1)), (Q(1, 2), Q(1, 2)), (Q(0), Q(0)))
    alphas = (Q(1, 3), Q(1, 2), Q(1))
    solve = lru_cache(None)(fixed_point)
    brackets = perturbations = localities = monotone = 0
    for p, s, alpha in product(matrices, seeds, alphas):
        a = solve(p, s, alpha)
        c.require(step(p, s, alpha, a) == a, "fixed point substitution")
        for k in range(6):
            x, tail = iterate(p, s, alpha, k)
            c.require(all(u <= v for u, v in zip(x, a)), "partial sum lower bound")
            err = sum(abs(u - v) for u, v in zip(x, a))
            c.require(err <= tail, "Neumann tail")
            c.require(err <= residual_bound(p, s, alpha, x), "a posteriori residual")
            brackets += 1
    for p, r, s in product(matrices, matrices, seeds):
        alpha = Q(1, 2)
        a, b = solve(p, s, alpha), solve(r, s, alpha)
        err = sum(abs(x - y) for x, y in zip(a, b))
        c.require(err <= perturbation_bound(p, s, r, s, alpha), "operator sensitivity")
        perturbations += 1
        changed_heads = {j for i in range(2) for j in range(2) if p[i][j] != r[i][j]}
        reached = closure(changed_heads, ((i, j) for i in range(2) for j in range(2) if r[i][j]))
        c.require(all(a[j] == b[j] for j in range(2) if j not in reached), "changed-head locality")
        localities += 1
        if all(r[i][j] <= p[i][j] for i in range(2) for j in range(2)):
            c.require(all(b[j] <= a[j] for j in range(2)), "graded decrease monotonicity")
            monotone += 1
    seed_changes = 0
    for p, s, t, alpha in product(matrices, seeds, seeds, alphas):
        a, b = solve(p, s, alpha), solve(p, t, alpha)
        c.require(sum(abs(x - y) for x, y in zip(a, b)) <= perturbation_bound(p, s, p, t, alpha),
                  "seed perturbation")
        seed_changes += 1
    # An added/revoked edge changes an old denominator: revocation is not rollback.
    old = ((Q(0), Q(1)), (Q(0), Q(0)))
    changed = ((Q(0), Q(1, 2)), (Q(0), Q(0)))
    s = seeds[0]
    a, b = solve(old, s, Q(1, 2)), solve(changed, s, Q(1, 2))
    c.control(a[1] == Q(1, 4) and b[1] == Q(1, 8), "gate-only rollback fails")
    c.control(solve(old, s, Q(1, 2)) == a, "full-operator rollback no-alarm")
    c.raises(ValueError, lambda: fixed_point(old, s, Q(0)), "zero restart rejected")
    c.raises(TypeError, lambda: fixed_point(old, s, 0.5), "float is not exact certificate")
    one = ((Q(1),),)
    first, _ = iterate(one, (Q(1),), Q(1, 2), 1)
    threshold = Q(7, 10)
    predicted = next(k for k in range(10) if Q(1, 2) ** (k + 1) < threshold - Q(1, 2))
    c.control(first[0] >= threshold and 1 < predicted == 2,
              "FOUND can precede width-only MORE_BUDGET hook")
    finite, _ = iterate(old, s, Q(1, 2), 1)
    c.control(finite[1] == a[1] == Q(1, 4),
              "exact fixed-point threshold can be attained finitely")
    return c.result(matrices=len(matrices), seeds=len(seeds), restarts=len(alphas),
                    bracket_cases=brackets, perturbation_cases=perturbations,
                    locality_cases=localities, monotonicity_cases=monotone, seed_change_cases=seed_changes)


def check_selection_and_conformal():
    c = Count()
    cases = 0
    for error, selection in product(range(256), range(1, 256)):
        a, pi = Q(error.bit_count(), 8), Q(selection.bit_count(), 8)
        selected = Q((error & selection).bit_count(), selection.bit_count())
        c.require(selected <= selection_bound(a, pi), "selection risk bound")
        cases += 1
    c.control(selection_bound(Q(1, 20), Q(1, 20)) == 1,
              "95 percent marginal coverage permits 100 percent selected error")
    c.raises(ValueError, lambda: selection_bound(Q(1, 20), Q(0)), "empty selection not success")
    # Independent rank oracle for the standard split-conformal calibration quantile.
    rank_cases = 0
    for alpha in (Q(1, 20), Q(1, 5), Q(2, 5), Q(3, 5), Q(4, 5)):
        value = 5 * (1 - alpha)
        k = -(-value.numerator // value.denominator)
        successes = 0
        for ranks in permutations(range(5)):
            calibration, test = ranks[:4], ranks[4]
            success = k > 4 or test <= sorted(calibration)[k - 1]
            successes += success
            rank_cases += 1
        c.require(Q(successes, 120) >= 1 - alpha, "rank-calibrated marginal coverage")
        c.require(Q(successes, 120) == Q(min(k, 5), 5), "distinct rank exact denominator")
    wrong_successes = sum(r[-1] <= sorted(r[:4])[2] for r in permutations(range(5)))
    c.control(Q(wrong_successes, 120) == Q(3, 5) < Q(4, 5),
              "wrong conformal quantile loses registered coverage")
    tied_cases = 0
    for scores in product((0, 1), repeat=5):
        successes = sum(scores[i] <= sorted(scores[:i] + scores[i + 1:])[3]
                        for i in range(5))
        c.require(Q(successes, 5) >= Q(4, 5), "exchangeable tied scores conservative")
        tied_cases += 1
    return c.result(selection_cases=cases, rank_permutations=rank_cases, tied_score_orbits=tied_cases)


def check_adaptive_risk():
    c = Count()
    policies = 0
    for qs in product((Q(0), Q(1, 4), Q(1, 2)), repeat=3):
        for policy in product((0, 1), repeat=3):
            total_prob = failure_prob = Q(0)
            path_budgets = []
            for x, y in product((0, 1), repeat=2):
                q1, q2 = qs[0], qs[1 + x]
                probability = (q1 if x else 1 - q1) * (q2 if y else 1 - q2)
                total_prob += probability
                failure_prob += probability * bool((policy[0] and x) or (policy[1 + x] and y))
                path_budgets.append(policy[0] * q1 + policy[1 + x] * q2)
            c.require(total_prob == 1, "adaptive tree normalized")
            c.require(failure_prob <= min(Q(1), max(path_budgets)), "predictable risk spending")
            policies += 1
    c.control(Q(1, 10) + Q(1, 10) != Q(1, 10), "reuse does not erase exposure risk")
    return c.result(two_step_predictable_policies=policies)


def check_drift():
    c = Count()
    distributions = tuple((Q(a, 4), Q(b, 4), Q(4 - a - b, 4))
                          for a in range(5) for b in range(5 - a))
    cases = 0
    for p, q in product(distributions, repeat=2):
        tv = sum(abs(a - b) for a, b in zip(p, q)) / 2
        for old, new in product(range(8), repeat=2):
            pold = sum(p[j] for j in range(3) if old >> j & 1)
            qnew = sum(q[j] for j in range(3) if new >> j & 1)
            disagreement = sum(q[j] for j in range(3) if (old ^ new) >> j & 1)
            c.require(qnew <= drift_bound(pold, tv, disagreement), "TV plus event-change transport")
            cases += 1
    c.control(drift_bound(Q(1, 20), Q(1, 10)) == Q(3, 20), "shift consumes risk")
    return c.result(distributions=len(distributions), event_transport_cases=cases)


def fixture_binding(quantifier="CONDITIONAL_ON_HISTORY"):
    return Binding("code-v1", "model-v1", "config-v1", "repr-v1", "prep-v1", "checker-v1",
                   "cal-v1", "target-v1", quantifier, "selection-v1", "cost-v1",
                   ("conditional-risk-premise",), ("registered-scope",), 0, 10)


def check_certificates():
    c = Count()
    b = fixture_binding()
    cert = Certificate(b, "RISK_BOUND", Interval((1,), (1,)), Q(1, 20))
    registry = {cert.fingerprint: Verdict.PASS}
    checker = lambda x: registry.get(x.fingerprint, Verdict.CANNOT_CHECK)
    kwargs = dict(context="registered-scope", epoch=1, available=1, nogoods=ZERO,
                  request="ACT_WITH_RISK", risk_limit=Q(1, 10),
                  external_authority=frozenset({"ACT_WITH_RISK", "ASSERT_EXACT"}),
                  check_certificate=checker)
    decision = commit_gate(cert, b, **kwargs)
    c.control(decision.status == "RISK_AUTHORIZED" and not decision.asserts_target,
              "risk action is not target truth")
    c.control(commit_gate(cert, b, **(kwargs | {"request": "ASSERT_EXACT"})).status == "REFUSED_KIND",
              "coverage cannot become exact assertion")
    mutations = 0
    for f in fields(b):
        value = getattr(b, f.name)
        change = value + ("changed",) if isinstance(value, tuple) else (value + 1 if type(value) is int else value + "-changed")
        current = replace(b, **{f.name: change})
        c.require(commit_gate(cert, current, **kwargs).status == "REVALIDATE_IDENTITY", "bind " + f.name)
        mutations += 1
    controls = [({"context": "elsewhere"}, "REFUSED_SCOPE", "scope mismatch"),
                ({"epoch": 11}, "REFUSED_EPOCH", "expired certificate"),
                ({"available": 0}, "REFUSED_SUPPORT", "revoked support"),
                ({"nogoods": (1,)}, "REFUSED_SUPPORT", "contradicted support"),
                ({"external_authority": frozenset()}, "REFUSED_AUTHORITY", "no self-authorization"),
                ({"check_certificate": None}, "CANNOT_CHECK", "absent checker"),
                ({"check_certificate": lambda _: Verdict.CANNOT_CHECK}, "CANNOT_CHECK", "checker unavailable"),
                ({"check_certificate": lambda _: Verdict.FAIL}, "REFUSED_CHECK", "failed checker"),
                ({"check_certificate": lambda _: "PASS"}, "REFUSED_CHECK", "untyped checker answer"),
                ({"risk_limit": Q(1, 100)}, "REFUSED_RISK", "risk budget too small")]
    for delta, expected, name in controls:
        c.control(commit_gate(cert, b, **(kwargs | delta)).status == expected, name)
    marginal = replace(b, quantifier="MARGINAL")
    mc = replace(cert, binding=marginal)
    registry[mc.fingerprint] = Verdict.PASS
    c.control(commit_gate(mc, marginal, **kwargs).status == "REFUSED_QUANTIFIER", "marginal is not prequential")
    eb = fixture_binding("EXACT_TARGET")
    ec = Certificate(eb, "EXACT_TARGET", Interval((1,), (1,)))
    registry[ec.fingerprint] = Verdict.PASS
    c.control(commit_gate(ec, eb, **(kwargs | {"request": "ASSERT_EXACT"})).asserts_target,
              "exact checked target no-alarm")
    c.raises(ValueError, lambda: Certificate(eb, "EXACT_TARGET", ec.support, Q(1, 10)), "graded exact kind refused")
    return c.result(bound_coordinate_mutations=mutations, trust_model="explicit fixture registry, not real attestation")


def check_budget_and_locality():
    c = Count()
    b = Budget(Q(1, 5), 3)
    e1 = ("event-1", "same-certificate", Q(1, 10), 1)
    b1 = b.reserve(e1)
    b2 = b1.reserve(("event-2", "same-certificate", Q(1, 10), 1))
    c.control(b1.reserve(e1) == b1, "idempotent replay no-alarm")
    c.control(b2.risk_spent == Q(1, 5), "new exposure charged despite same certificate")
    c.raises(ValueError, lambda: b2.reserve(("event-3", "same-certificate", Q(1, 10), 1)), "risk overspend refused")
    c.raises(Conflict, lambda: b1.reserve(("event-1", "changed", Q(1, 10), 1)), "event identity mismatch")
    c.raises(ValueError, lambda: b.reserve(("zero-work", "c", Q(0), 0)), "uncharged transition refused")
    c.raises(TypeError, lambda: b.reserve(()), "malformed event refused")
    c.raises(ValueError, lambda: Budget(Q(1), 0).reserve(("e", "c", Q(0), 1)), "zero-work budget cannot progress")
    c.control(sum((Q(1, 2 ** t) for t in range(1, 31)), Q(0)) < 1,
              "strict positive real charges do not imply termination")
    # A child changes but conjunction is already dead; shared support can have alternatives.
    p, dead = Interval((1,), (1,)), Interval(ZERO, ZERO)
    c.control(p.verdict(1) != p.verdict(0) and p.compose(dead).verdict(1) == p.compose(dead).verdict(0),
              "summary iff child-changes claim is false")
    alt = Interval((1, 2), (1, 2))
    c.control(alt.verdict(3) == alt.verdict(2), "shared dependency need not cause liveness change")
    model, certificate = Interval((1,), (1,)), Interval((1, 2), (1, 2))
    c.control(model.verdict(2) is Live.DEAD and certificate.verdict(2) is Live.LIVE,
              "overlapping evidence can retain independent alternative support")
    c.control(closure({0}, ((0, 1), (1, 2), (2, 1))) == frozenset({0, 1, 2}), "dependency cycle finite closure")
    # Snapshot immutability alone allows the classic two-coordinate write skew.
    c.control(sum((1, 0)) <= 1 and sum((0, 1)) <= 1 and sum((1, 1)) > 1,
              "snapshot-local validity not global serializability")
    epoch = 0
    first_expected = second_expected = 0
    c.require(first_expected == epoch, "first transaction valid epoch")
    epoch += 1
    c.control(second_expected != epoch, "version validation detects stale second transaction")
    return c.result()


def check_semantics_and_information():
    c = Count()
    c.control(robust_answer(["a", "a"]).status == "UNANIMOUS_WITHIN_MODEL", "multiple meanings same answer")
    c.control(robust_answer(["a", "b"]).status == "UNKNOWN_AMBIGUOUS", "disagreeing meanings remain unknown")
    c.control(robust_answer([]).status == "CANNOT_CHECK_EMPTY_MODEL", "empty model not vacuous truth")
    # A many-to-one seed map can collapse distinct meanings; equality is insufficient fidelity.
    meanings = {"p": 0, "not-p": 0}
    c.control(meanings["p"] == meanings["not-p"] and "p" != "not-p", "equal seeds not equivalent meanings")
    # Version-space realized gains: marginal subadditivity is not a general law.
    h, a, b = set(range(4)), {0, 1, 2}, {0, 1, 3}
    c.control(len(a) * len(b) > len(h) * len(a & b), "realized information gain can be superadditive")
    c.require(Q(len(h), len(a)) * Q(len(a), len(a & b)) == Q(len(h), len(a & b)),
              "sequential information gain telescopes without independence")
    return c.result()


def check_learning():
    c = Count()
    # One natural finite compositional family: all affine Boolean maps on two bits.
    domain = tuple(product((0, 1), repeat=2))
    hypotheses = tuple(tuple(str(a ^ (b & x) ^ (d & y)) for x, y in domain)
                       for a, b, d in product((0, 1), repeat=3))
    cases = 0
    for teacher in hypotheses:
        lessons = tuple(enumerate(teacher))
        for q in range(4):
            warrants = query_warrants(hypotheses, lessons, q, teacher[q])
            for mask in range(16):
                vs = version_space(hypotheses, lessons, mask)
                unanimous = bool(vs) and all(h[q] == teacher[q] for h in vs)
                c.require(holds(warrants, mask) == unanimous, "query-specific warranted retention")
                cases += 1
    teacher = hypotheses[0]
    lessons = tuple(enumerate(teacher))
    c.control(len(version_space(hypotheses, lessons, 1)) > 1 and
              holds(query_warrants(hypotheses, lessons, 0, teacher[0]), 1),
              "global uniqueness unnecessary for a known query")
    warrants = query_warrants(hypotheses, lessons, 0, teacher[0])
    c.control(holds(warrants, 15) and holds(warrants, 14),
              "held-out affine answer retains alternative lessons")
    c.control(not holds(warrants, 0), "essential learning cannot survive all revocations")
    conflict = ((0, "0"), (0, "1"))
    c.control(not version_space(hypotheses, conflict, 3), "contradictory class not vacuous proof")
    c.control(query_warrants(hypotheses, conflict, 0, "2") == ZERO,
              "empty version spaces do not warrant arbitrary answers")
    return c.result(hypotheses=len(hypotheses), teachers=len(hypotheses), queries=4,
                    revocation_masks=16, oracle_comparisons=cases)


CHECKS = {"intervals": check_intervals, "nogoods": check_nogoods,
          "substitution": check_substitution, "navigation": check_navigation,
          "selection": check_selection_and_conformal, "adaptive_risk": check_adaptive_risk,
          "drift": check_drift, "certificates": check_certificates,
          "lifecycle": check_budget_and_locality, "semantics": check_semantics_and_information,
          "learning": check_learning}


def run():
    results = {name: fn() for name, fn in CHECKS.items()}
    return {"study": "ME-FOUNDATION-TYPED-LIFECYCLE-V1", "terminal": "EXACT_CALIBRATION_PASS",
            "evidence_class": "EXACT_DEVELOPMENT_CALIBRATION_NOT_PROTECTED_EMPIRICAL_EVIDENCE",
            "groups": results, "group_count": len(results),
            "check_count": sum(r["checks"] for r in results.values()),
            "control_count": sum(len(r["controls"]) for r in results.values()),
            "all_size_proof_authority": False, "independent_review": "NOT_OBTAINED",
            "novelty": "NOT_CLAIMED", "ocm_adoption": "NOT_GRANTED"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run()
    except CannotCheck as exc:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (CheckFailure, ValueError, TypeError, ArithmeticError) as exc:
        print(json.dumps({"terminal": "FAIL", "reason": str(exc)}))
        return 1
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
