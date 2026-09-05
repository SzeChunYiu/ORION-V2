"""Exact sanity/hostile checker for Machine Epistemics Foundation Batch 2.

Covers the finite/executable cores of:
  MEG-02 statistical warrant vs risk-bounded actionability + certificate identity drift;
  MEG-03 epoch expiry / supersession locality;
  MEG-16 ATMS nogoods in warrant intervals (corrected meet law);
  MEG-17 reinstate vs relearn lifecycle semantics and local repair;
  MEG-20 restricted sufficiency certificates for quotient summaries.

The accompanying theory note contains all-size proofs where claimed. Finite enumeration here is
counterexample/calibration evidence, not authority for an all-size theorem.

Exit codes: 0 = all registered checks hold; 1 = defect; 2 = CANNOT_CHECK.
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from dataclasses import dataclass
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


def canon(items):
    unique = {frozenset(w) for w in items}
    return tuple(sorted((w for w in unique if not any(v < w for v in unique)), key=lambda w: (len(w), sorted(map(repr, w)))))


ZERO, ONE = (), (frozenset(),)
LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


def join(p, q):
    return canon((*p, *q))


def meet(p, q):
    if not p or not q:
        return ZERO
    return canon(a | b for a in p for b in q)


def leq(p, q):
    return all(any(w2 <= w1 for w2 in q) for w1 in p)


def live(p, revoked):
    r = frozenset(revoked)
    return any(not (w & r) for w in p)


def liveness(interval, revoked):
    lo, up = interval
    if live(lo, revoked):
        return LIVE
    if not live(up, revoked):
        return DEAD
    return UNKNOWN


def all_profiles(n):
    subsets = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(range(n), k)]
    out = set()
    for mask in range(1 << len(subsets)):
        out.add(canon(subsets[i] for i in range(len(subsets)) if mask & (1 << i)))
    return sorted(out, key=lambda p: (len(p), [sorted(w) for w in p]))


@dataclass(frozen=True)
class OperatorIdentity:
    implementation: str
    configuration: str
    checker: str
    calibration: str
    assumptions: str
    scope: str
    epoch: str

    @property
    def digest(self):
        body = "\0".join((self.implementation, self.configuration, self.checker, self.calibration,
                          self.assumptions, self.scope, self.epoch))
        return hashlib.sha256(body.encode()).hexdigest()


@dataclass(frozen=True)
class RiskReceipt:
    operator_digest: str
    delta: Fraction
    scope: str
    epoch: str
    guarantee: str = "MARGINAL_COVERAGE"

    def __post_init__(self):
        if not (Fraction(0) <= self.delta < Fraction(1)):
            raise ValueError("delta out of range")


def statistical_candidate_interval(input_upper=ONE):
    return (ZERO, input_upper)


def action_gate(interval, receipt, identity, *, task_max_risk, scope, epoch):
    if receipt.operator_digest != identity.digest:
        return "CANNOT_CHECK"
    if receipt.scope != scope or receipt.epoch != epoch:
        return "CANNOT_CHECK"
    if receipt.guarantee != "MARGINAL_COVERAGE":
        return "CANNOT_CHECK"
    if receipt.delta > task_max_risk:
        return "DENY"
    return "ALLOW"


def mutant_promote_coverage_to_truth(receipt, identity, *, scope, epoch):
    if receipt.operator_digest == identity.digest and receipt.scope == scope and receipt.epoch == epoch:
        return (ONE, ONE)
    return statistical_candidate_interval()


def check_meg02():
    ident = OperatorIdentity("model-A@sha256:111", "temp=0", "checker-v1", "cal-set@222", "exchangeable", "S", "e1")
    rr = RiskReceipt(ident.digest, Fraction(1, 10), "S", "e1")
    iv = statistical_candidate_interval()
    assert liveness(iv, ()) == UNKNOWN
    assert action_gate(iv, rr, ident, task_max_risk=Fraction(1, 10), scope="S", epoch="e1") == "ALLOW"
    assert liveness(iv, ()) == UNKNOWN
    assert liveness(mutant_promote_coverage_to_truth(rr, ident, scope="S", epoch="e1"), ()) == LIVE
    mass = {"a": Fraction(9, 10), "b": Fraction(1, 10)}
    coverage = {"a": 1, "b": 0}
    marginal = sum(mass[x] * coverage[x] for x in mass)
    assert marginal == Fraction(9, 10) and coverage["b"] == 0
    drifted = OperatorIdentity("model-A@sha256:111", "temp=0.7", "checker-v1", "cal-set@222", "exchangeable", "S", "e1")
    assert drifted.digest != ident.digest
    assert action_gate(iv, rr, drifted, task_max_risk=Fraction(1, 10), scope="S", epoch="e1") == "CANNOT_CHECK"
    assert action_gate(iv, rr, ident, task_max_risk=Fraction(1, 10), scope="T", epoch="e1") == "CANNOT_CHECK"
    assert action_gate(iv, rr, ident, task_max_risk=Fraction(1, 10), scope="S", epoch="e2") == "CANNOT_CHECK"
    assert action_gate(iv, rr, ident, task_max_risk=Fraction(1, 20), scope="S", epoch="e1") == "DENY"
    return {"truth_status": UNKNOWN, "risk_gate": "ALLOW", "marginal_coverage": str(marginal),
            "conditional_coverage_at_b": 0, "identity_drift_caught": 1, "scope_drift_caught": 1,
            "epoch_drift_caught": 1, "risk_tolerance_enforced": 1,
            "score_or_coverage_promoted_to_truth_mutant_caught": 1}


@dataclass(frozen=True)
class EpochScope:
    start: int | None = None
    end: int | None = None

    @property
    def empty(self):
        return self.start is not None and self.end is not None and self.start >= self.end

    def contains(self, t):
        if self.empty:
            return False
        return (self.start is None or self.start <= t) and (self.end is None or t < self.end)

    def intersect(self, other):
        starts = [x for x in (self.start, other.start) if x is not None]
        ends = [x for x in (self.end, other.end) if x is not None]
        return EpochScope(max(starts) if starts else None, min(ends) if ends else None)


EMPTY_SCOPE = EpochScope(0, 0)


def impact_cone(changed, dep_edges):
    out = set(changed)
    grew = True
    while grew:
        grew = False
        for tails, heads in dep_edges:
            if any(t in out for t in tails):
                for h in heads:
                    if h not in out:
                        out.add(h)
                        grew = True
    return frozenset(out)


def partition_measurable(blocks, truth_by_atom):
    return all(len({truth_by_atom[x] for x in block}) <= 1 for block in blocks)


def check_meg03():
    scopes = [EpochScope(None, None), EpochScope(0, 5), EpochScope(2, 8), EpochScope(5, 9), EMPTY_SCOPE]
    assoc = annih = 0
    for a in scopes:
        for b in scopes:
            for c in scopes:
                assert a.intersect(b).intersect(c) == a.intersect(b.intersect(c))
                assoc += 1
        assert a.intersect(EMPTY_SCOPE).empty
        annih += 1
    atoms = {"old": EpochScope(1, 3), "new": EpochScope(3, None), "plan": EpochScope(1, None), "unrelated": EpochScope(None, None)}
    alive_t2 = {x: s.contains(2) for x, s in atoms.items()}
    alive_t4 = {x: s.contains(4) for x, s in atoms.items()}
    good = [("old",), ("new",), ("plan", "unrelated")]
    bad = [("old", "new"), ("plan",), ("unrelated",)]
    assert partition_measurable(good, alive_t2) and partition_measurable(good, alive_t4)
    assert not partition_measurable(bad, alive_t2) and not partition_measurable(bad, alive_t4)
    deps = [(('old',), ('plan',)), (('new',), ('plan',)), (('unrelated',), ('other',))]
    cone = impact_cone({'old'}, deps)
    assert cone == {'old', 'plan'} and 'new' not in cone and 'unrelated' not in cone
    assert alive_t2['old'] and not alive_t4['old'] and (not alive_t2['new']) and alive_t4['new']
    return {"scope_associativity_checks": assoc, "empty_annihilator_checks": annih,
            "epoch_partition_good": 1, "cross_epoch_partition_rejected": 1,
            "supersession_impact": sorted(cone), "unrelated_no_alarm": 1}


@dataclass(frozen=True)
class Nogoods:
    items: tuple[frozenset, ...] = ()

    @staticmethod
    def of(*sets):
        return Nogoods(canon(sets))

    def violates(self, warrant):
        return any(n <= warrant for n in self.items)

    def filter(self, profile):
        return canon(w for w in profile if not self.violates(w))

    def filter_interval(self, interval):
        return (self.filter(interval[0]), self.filter(interval[1]))


def trit_leq(a, b):
    order = {DEAD: 0, UNKNOWN: 1, LIVE: 2}
    return order[a] <= order[b]


def kand(a, b):
    return DEAD if DEAD in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else LIVE)


def kor(a, b):
    return LIVE if LIVE in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else DEAD)


def check_meg16(n=3):
    ps = all_profiles(n)
    revs = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(range(n), k)]
    nonempty = [frozenset(c) for k in range(1, n + 1) for c in itertools.combinations(range(n), k)]
    families = [Nogoods.of(s) for s in nonempty]
    join_checks = meet_ineq = strict = kleene_join = kleene_meet_ineq = never_revives = 0
    for ng in families:
        for p in ps:
            fp = ng.filter(p)
            for r in revs:
                before = liveness((p, p), r)
                after = liveness((fp, fp), r)
                assert not (before == DEAD and after == LIVE)
                never_revives += 1
            for q in ps:
                assert ng.filter(join(p, q)) == join(ng.filter(p), ng.filter(q))
                join_checks += 1
                left = ng.filter(meet(p, q))
                mutant = meet(ng.filter(p), ng.filter(q))
                assert leq(left, mutant)
                meet_ineq += 1
                strict += int(left != mutant)
                for r in revs:
                    lp = liveness((ng.filter(p), ng.filter(p)), r)
                    lq = liveness((ng.filter(q), ng.filter(q)), r)
                    lj = liveness((ng.filter(join(p, q)), ng.filter(join(p, q))), r)
                    lm = liveness((left, left), r)
                    assert lj == kor(lp, lq)
                    assert trit_leq(lm, kand(lp, lq))
                    kleene_join += 1
                    kleene_meet_ineq += 1
    ng = Nogoods.of({0, 1})
    p, q = (frozenset({0}),), (frozenset({1}),)
    assert ng.filter(meet(p, q)) == ZERO
    assert meet(ng.filter(p), ng.filter(q)) == (frozenset({0, 1}),)
    assert strict > 0
    joint = ng.filter(meet(p, q))
    assert not live(joint, ()) and live(ng.filter(p), ()) and live(ng.filter(q), ())
    return {"profiles": len(ps), "nogood_families": len(families), "join_homomorphism_checks": join_checks,
            "meet_subhomomorphism_checks": meet_ineq, "strict_meet_counterexamples": strict,
            "kleene_join_checks": kleene_join, "kleene_meet_subhomomorphism_checks": kleene_meet_ineq,
            "never_revives_checks": never_revives, "atlas_meet_homomorphism_refuted": 1,
            "constraint_kills_joint_composite": 1}


def profile(*supports):
    return canon(frozenset(s) for s in supports)


def lifecycle_signature(interval, evidence_universe):
    out = {}
    ev = tuple(evidence_universe)
    for k in range(len(ev) + 1):
        for r in itertools.combinations(ev, k):
            out[r] = liveness(interval, r)
    return out


def check_meg17():
    old = (profile({"e_old"}), profile({"e_old"}))
    new = (profile({"e_new"}), profile({"e_new"}))
    assert liveness(old, ()) == LIVE and liveness(new, ()) == LIVE
    assert liveness(old, {"e_old"}) == DEAD
    assert liveness(old, ()) == LIVE
    sig_old = lifecycle_signature(old, ("e_old", "e_new"))
    sig_new = lifecycle_signature(new, ("e_old", "e_new"))
    assert sig_old != sig_new and sig_old[("e_old",)] == DEAD and sig_new[("e_old",)] == LIVE
    deps = [(("lesson",), ("skill",)), (("skill",), ("answer",)), (("other",), ("other_answer",))]
    cone = impact_cone({"lesson"}, deps)
    assert cone == {"lesson", "skill", "answer"}
    local_cost = len(cone)
    global_cost = len({"lesson", "skill", "answer", "other", "other_answer"})
    assert local_cost < global_cost
    assert impact_cone({"lesson"}, deps) == cone and "other_answer" not in cone
    return {"reinstate_exact": 1, "relearn_current_behavior_equal": 1,
            "relearn_lifecycle_profile_differs": 1, "repair_impact": sorted(cone),
            "local_work": local_cost, "global_rederive_mutant_work": global_cost, "unrelated_preserved": 1}


def row_block_sums(P, blocks):
    return [[sum(P[i][j] for j in block) for block in blocks] for i in range(len(P))]


def strong_lumpable(P, blocks):
    sums = row_block_sums(P, blocks)
    for block in blocks:
        for i in block:
            for j in block:
                if sums[i] != sums[j]:
                    return False
    return True


def quotient_matrix(P, blocks):
    if not strong_lumpable(P, blocks):
        raise CannotCheck("partition not lumpable")
    sums = row_block_sums(P, blocks)
    return [[sums[block[0]][b] for b in range(len(blocks))] for block in blocks]


def pushforward(vec, blocks):
    return [sum(vec[i] for i in block) for block in blocks]


def fixed_point(P, seed, alpha=Fraction(1, 3), steps=200):
    a = [Fraction(0) for _ in seed]
    for _ in range(steps):
        nxt = [alpha * s for s in seed]
        for i in range(len(P)):
            for j in range(len(P)):
                nxt[j] += (1 - alpha) * P[i][j] * a[i]
        if nxt == a:
            return nxt
        a = nxt
    return a


def measurable(blocks, values):
    return all(len({values[i] for i in block}) <= 1 for block in blocks)


@dataclass(frozen=True)
class SufficiencyCertificate:
    blocks: tuple[tuple[int, ...], ...]
    query_family: tuple[str, ...]
    revocation_family: tuple[str, ...]
    answer_measurable: bool


def verify_sufficiency(P_by_revocation, liveness_by_revocation, cert):
    blocks = [tuple(b) for b in cert.blocks]
    if not cert.answer_measurable:
        return "REFINE_REQUIRED"
    for r in cert.revocation_family:
        P = P_by_revocation[r]
        if not strong_lumpable(P, blocks):
            return "REFINE_REQUIRED"
        if not measurable(blocks, liveness_by_revocation[r]):
            return "REFINE_REQUIRED"
    return "CERTIFIED"


def check_meg20():
    P = [[Fraction(0), Fraction(0), Fraction(1, 2), Fraction(1, 2)],
         [Fraction(0), Fraction(0), Fraction(1, 3), Fraction(2, 3)],
         [Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
         [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]]
    blocks = ((0, 1), (2, 3))
    lv = {"none": [LIVE, LIVE, LIVE, LIVE], "r": [LIVE, LIVE, DEAD, DEAD]}
    cert = SufficiencyCertificate(blocks, ("q",), ("none", "r"), True)
    assert verify_sufficiency({"none": P, "r": P}, lv, cert) == "CERTIFIED"
    seed = [Fraction(1), Fraction(0), Fraction(0), Fraction(0)]
    a = fixed_point(P, seed)
    Q = quotient_matrix(P, [tuple(b) for b in blocks])
    aq = fixed_point(Q, pushforward(seed, [tuple(b) for b in blocks]))
    assert pushforward(a, [tuple(b) for b in blocks]) == aq
    badP = [row[:] for row in P]
    badP[1][2], badP[1][3] = Fraction(0), Fraction(1, 2)
    assert not strong_lumpable(badP, [tuple(b) for b in blocks])
    assert verify_sufficiency({"none": badP, "r": badP}, lv, cert) == "REFINE_REQUIRED"
    bad_lv = {"none": [LIVE, DEAD, LIVE, LIVE], "r": [LIVE, DEAD, DEAD, DEAD]}
    assert verify_sufficiency({"none": P, "r": P}, bad_lv, cert) == "REFINE_REQUIRED"
    bad_answer = SufficiencyCertificate(blocks, ("q",), ("none", "r"), False)
    assert verify_sufficiency({"none": P, "r": P}, lv, bad_answer) == "REFINE_REQUIRED"
    return {"valid_certificate": "CERTIFIED", "pushforward_fixed_point_equal": 1,
            "nonlumpable_mutant_refused": 1, "nonmeasurable_warrant_refused": 1,
            "answer_not_factoring_refused": 1}


def run_all():
    return {"MEG-02": check_meg02(), "MEG-03": check_meg03(), "MEG-16": check_meg16(),
            "MEG-17": check_meg17(), "MEG-20": check_meg20(), "GENERAL_NOVELTY": "NOT_ESTABLISHED"}


def main():
    try:
        result = run_all()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}, sort_keys=True))
        return 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "type": type(exc).__name__, "reason": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps({"status": "PASS", "result": result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
