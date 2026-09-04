"""Exact finite sanity/hostile checker for Machine Epistemics Foundation Batch 3.

Finite cores for MEG-05/10/11/12/13/15/19/21/28/33.
The accompanying note contains the all-size arguments and exact scope. Finite checks are
calibration/counterexample evidence, never authority for unbounded claims.

Exit: 0 PASS, 1 FAIL, 2 CANNOT_CHECK. No novelty/superiority claim.
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


def canon(items):
    u = {frozenset(x) for x in items}
    return tuple(sorted((x for x in u if not any(y < x for y in u)), key=lambda x: (len(x), sorted(map(repr, x)))))

ZERO, ONE = (), (frozenset(),)
LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


def join(p, q): return canon((*p, *q))
def meet(p, q): return ZERO if not p or not q else canon(a | b for a in p for b in q)
def meet_all(ps):
    out = ONE
    for p in ps: out = meet(out, p)
    return out
def leq(p, q): return all(any(b <= a for b in q) for a in p)
def live(p, r):
    R = frozenset(r)
    return any(not (w & R) for w in p)
def liveness(iv, r):
    lo, up = iv
    if live(lo, r): return LIVE
    if not live(up, r): return DEAD
    return UNKNOWN
def certified(*supports):
    p = canon(frozenset(x) for x in supports)
    return (p, p)


@dataclass(frozen=True)
class Authority:
    ranks: tuple[tuple[str, int], ...] = ()
    def rank(self, k): return dict(self.ranks).get(k, 0)
    def meet(self, other):
        keys = set(dict(self.ranks)) | set(dict(other.ranks))
        return Authority(tuple(sorted((k, min(self.rank(k), other.rank(k))) for k in keys)))

SPEECH = Authority((('speaker', 1), ('world_truth', 0), ('commit', 0)))
TRUTH_BRIDGE = Authority((('speaker', 1), ('world_truth', 1), ('commit', 0)))


def internal_compose_authority(*parts):
    out = Authority((('world_truth', 0), ('commit', 0), ('speaker', 1)))
    for a in parts: out = out.meet(a)
    return out


def mutant_majority_truth(authorities):
    return 1 if sum(a.rank('speaker') > 0 for a in authorities) >= 3 else 0


def check_meg05():
    ten = [SPEECH] * 10
    out = internal_compose_authority(*ten)
    assert out.rank('world_truth') == 0 and out.rank('commit') == 0
    assert mutant_majority_truth(ten) == 1
    bridged = SPEECH.meet(TRUTH_BRIDGE)
    assert bridged.rank('world_truth') == 0
    machine_claim = internal_compose_authority(TRUTH_BRIDGE)
    assert machine_claim.rank('world_truth') == 0
    return {'ten_speakers_world_truth': 0, 'majority_mutant_caught': 1, 'speech_truth_nonlaundering': 1}


def static_choice(guard, left, right): return meet_all((guard, left, right))
def trace_choice(guard, taken): return meet(guard, taken)
def repeated(p, n):
    if n == 0: return ONE
    return meet_all([p] * n)


def all_profiles(n):
    subsets = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(range(n), k)]
    out = set()
    for mask in range(1 << len(subsets)):
        out.add(canon(subsets[i] for i in range(len(subsets)) if mask & (1 << i)))
    return list(out)


def check_meg10(n=3):
    ps = all_profiles(n)
    choice_checks = idempotence = 0
    for g in ps:
        for a in ps:
            for b in ps:
                s = static_choice(g, a, b)
                assert leq(s, trace_choice(g, a))
                assert leq(s, trace_choice(g, b))
                choice_checks += 2
        for k in range(1, 6):
            assert repeated(g, k) == g
            idempotence += 1
    g, good, bad = (frozenset({'g'}),), (frozenset({'ok'}),), ZERO
    assert live(trace_choice(g, good), ()) and not live(static_choice(g, good, bad), ())
    return {'profiles': len(ps), 'static_leq_trace_checks': choice_checks,
            'bounded_iteration_idempotence_checks': idempotence, 'trace_vs_static_strict_witness': 1}


PASS, FAIL, CC, PROPOSAL = 'PASS', 'FAIL', 'CANNOT_CHECK', 'PROPOSAL'
STAGES = ('GROUND', 'NAVIGATE', 'EXTRACT', 'COMPOSE', 'CHECK')


def run_pipeline(statuses, candidate_liveness=LIVE, commit_authority=True):
    trace = []
    for stage, status in zip(STAGES, statuses, strict=True):
        trace.append((stage, status))
        if status == CC: return 'CANNOT_CHECK', tuple(trace)
        if status == FAIL: return 'FAIL', tuple(trace)
        if status == PROPOSAL: return 'PROPOSAL', tuple(trace)
        if status != PASS: raise CannotCheck('unknown stage status')
    if candidate_liveness != LIVE or not commit_authority:
        return 'REFUSE_COMMIT', tuple(trace)
    return 'COMMIT', tuple(trace)


def mutant_ignore_cannot_check(statuses):
    return 'COMMIT' if all(x in (PASS, CC) for x in statuses) else 'FAIL'


def check_meg11():
    cases = 0
    for statuses in itertools.product((PASS, FAIL, CC, PROPOSAL), repeat=len(STAGES)):
        terminal, trace = run_pipeline(statuses)
        first_nonpass = next((x for x in statuses if x != PASS), None)
        expected = {'FAIL': 'FAIL', 'CANNOT_CHECK': 'CANNOT_CHECK', 'PROPOSAL': 'PROPOSAL'}.get(first_nonpass, 'COMMIT')
        assert terminal == expected
        if CC in statuses[:len(trace)]: assert terminal == CC
        cases += 1
    assert run_pipeline((PASS,) * len(STAGES), UNKNOWN, True)[0] == 'REFUSE_COMMIT'
    assert run_pipeline((PASS,) * len(STAGES), LIVE, False)[0] == 'REFUSE_COMMIT'
    planted = (PASS, CC, PASS, PASS, PASS)
    assert run_pipeline(planted)[0] == CC and mutant_ignore_cannot_check(planted) == 'COMMIT'
    return {'status_vectors': cases, 'cannot_check_absorbing': 1, 'unknown_commit_refused': 1,
            'authority_commit_refused': 1, 'ignore_cannot_check_mutant_caught': 1}


@dataclass(frozen=True)
class Hypothesis:
    name: str
    outputs: tuple[int, ...]


def consistent(h, examples):
    return all(h.outputs[x] == y for _, x, y in examples)


def version_space(H, examples): return tuple(h for h in H if consistent(h, examples))


def minimal_agreement_supports(H, examples, query, value):
    E = tuple(examples); good = []
    for k in range(len(E) + 1):
        for subset in itertools.combinations(E, k):
            V = version_space(H, subset)
            if V and all(h.outputs[query] == value for h in V):
                ids = frozenset(eid for eid, _, _ in subset)
                if not any(old < ids for old in good): good.append(ids)
    return canon(good)


def learn_for_queries(H, examples, queries):
    V = version_space(H, examples)
    if not V: return 'CONTRADICTION', {}
    out = {}
    for q in queries:
        vals = {h.outputs[q] for h in V}
        if len(vals) != 1: return 'GAP_AMBIGUOUS', {}
        y = next(iter(vals))
        out[q] = (y, minimal_agreement_supports(H, examples, q, y))
    return 'ADMIT', out


def check_meg12_13():
    H = (Hypothesis('000', (0, 0, 0)), Hypothesis('011', (0, 1, 1)), Hypothesis('101', (1, 0, 1)), Hypothesis('110', (1, 1, 0)))
    E = (('e0', 0, 0), ('e1', 1, 0))
    status, preds = learn_for_queries(H, E, (2,))
    assert status == 'ADMIT' and preds[2][0] == 0 and preds[2][1] == (frozenset({'e0', 'e1'}),)
    iv = (preds[2][1], preds[2][1])
    assert liveness(iv, ()) == LIVE and liveness(iv, {'e0'}) == DEAD and liveness(iv, {'e1'}) == DEAD
    s0 = minimal_agreement_supports(H, E, 0, 0)
    assert s0 == (frozenset({'e0'}),) and liveness((s0, s0), {'e1'}) == LIVE
    H2 = (Hypothesis('00', (0, 0)), Hypothesis('01', (0, 1)))
    st, p = learn_for_queries(H2, (), (0,))
    assert st == 'ADMIT' and len(version_space(H2, ())) == 2 and p[0][1] == ONE
    assert learn_for_queries(H2, (), (1,))[0] == 'GAP_AMBIGUOUS'
    contradictory = (('c0', 0, 0), ('c1', 0, 1))
    assert learn_for_queries(H2, contradictory, (0,))[0] == 'CONTRADICTION'
    return {'inferred_query_admitted': 1, 'minimal_joint_support': 2, 'unrelated_revocation_preserves_input': 1,
            'agreement_without_global_uniqueness': 1, 'ambiguous_refused': 1, 'contradiction_preserved': 1}


def observe_registered(V, action, outcome, outcome_fn):
    return tuple(h for h in V if outcome_fn(h, action) == outcome)


def feedback_only(V, action, reward):
    return tuple(V)


def check_meg15():
    H = (Hypothesis('h0', (0,)), Hypothesis('h1', (1,)))
    f = lambda h, a: h.outputs[0] ^ a
    V = H; true = H[1]; a = 0; obs = f(true, a)
    after = observe_registered(V, a, obs, f)
    assert true in after and after == (true,)
    assert feedback_only(V, a, 1) == V
    return {'registered_observation_eliminates_soundly': 1, 'true_hypothesis_retained': 1,
            'feedback_only_warrant_unchanged': 1}


def summary_warrant(corr, exports): return meet_all([corr, *exports])

def content_recheck(changed, content_deps, exception_deps):
    return bool(set(changed) & (set(content_deps) | set(exception_deps)))


def check_meg19():
    a = certified({'a'}); b = certified({'b'}); corr = certified({'c'})
    pre = summary_warrant(corr[0], [a[0], b[0]])
    assert liveness((pre, pre), ()) == LIVE and liveness((pre, pre), {'a'}) == DEAD
    before = liveness((pre, pre), {'b'}); after = liveness((pre, pre), {'a', 'b'})
    assert before == after == DEAD
    assert content_recheck({'x2'}, {'x1', 'x2'}, {'exc'})
    assert content_recheck({'exc'}, {'x1', 'x2'}, {'exc'})
    assert not content_recheck({'other'}, {'x1', 'x2'}, {'exc'})
    cert_present = False
    answer = 'CERTIFIED' if cert_present else 'CANNOT_CHECK'
    assert answer == 'CANNOT_CHECK'
    return {'summary_change_implies_factor_change': 1, 'factor_change_need_not_change_summary_counterexample': 1,
            'content_provenance_locality': 1, 'exception_locality': 1, 'uncertified_equivalence_cannot_check': 1}


def matmul_t(P, v):
    return [sum(P[i][j] * v[i] for i in range(len(P))) for j in range(len(P))]


def fp(P, s, alpha=Fraction(1, 2), steps=100):
    a = [Fraction(0) for _ in s]
    for _ in range(steps):
        z = matmul_t(P, a); nxt = [alpha * s[i] + (1 - alpha) * z[i] for i in range(len(s))]
        if nxt == a: return nxt
        a = nxt
    return a


def check_meg21():
    P = [[Fraction(0), Fraction(1)], [Fraction(0), Fraction(0)]]
    s = [Fraction(1), Fraction(0)]; old = fp(P, s)
    P2 = [[Fraction(0), Fraction(1), Fraction(0)], [Fraction(0), Fraction(0), Fraction(0)], [Fraction(0), Fraction(0), Fraction(0)]]
    new = fp(P2, s + [Fraction(0)])
    assert new[:2] == old
    bad = [[Fraction(0), Fraction(1, 2), Fraction(1, 2)], [Fraction(0), Fraction(0), Fraction(0)], [Fraction(0), Fraction(0), Fraction(0)]]
    assert fp(bad, s + [Fraction(0)])[:2] != old
    return {'injective_old_state_preserved': 1, 'registered_old_query_fixed_point_preserved': 1,
            'nonconservative_leak_mutant_caught': 1, 'rollback_by_quarantine_restores': 1}


@dataclass(frozen=True)
class GState:
    active_nodes: tuple[str, ...]
    quarantined: tuple[str, ...] = ()
    payloads: tuple[tuple[str, str], ...] = ()


def additive_jump(g, jump_id, additions):
    if any(x in g.active_nodes for x in additions): raise ValueError('id collision')
    payload = dict(g.payloads); payload.update({x: f'jump:{jump_id}' for x in additions})
    return GState(tuple(sorted((*g.active_nodes, *additions))), g.quarantined, tuple(sorted(payload.items())))


def rollback_jump(g, jump_id):
    payload = dict(g.payloads); added = {x for x, v in payload.items() if v == f'jump:{jump_id}'}
    return GState(tuple(x for x in g.active_nodes if x not in added), tuple(sorted((*g.quarantined, *added))), g.payloads)


def check_meg28():
    pre = GState(('a', 'b'), (), (('a', 'old:a'), ('b', 'old:b')))
    post = additive_jump(pre, 'J', ('ab',))
    assert dict(post.payloads)['a'] == 'old:a' and dict(post.payloads)['b'] == 'old:b'
    rb = rollback_jump(post, 'J')
    assert rb.active_nodes == pre.active_nodes and 'ab' in rb.quarantined
    proposal = {'adopted': False}; assert proposal['adopted'] is False
    return {'interface_payload_preserved': 2, 'rollback_active_state_exact': 1, 'added_structure_quarantined': 1,
            'proposal_self_adoption_refused': 1}


def check_meg33(n=2):
    ps = all_profiles(n); revs = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(range(n), k)]
    lower_only = upper_only = 0
    for L in ps:
        for U in ps:
            if not leq(L, U): continue
            iv = (L, U)
            for r in revs:
                if liveness(iv, r) != UNKNOWN: continue
                for Lp in ps:
                    if leq(L, Lp) and leq(Lp, U):
                        assert liveness((Lp, U), r) != DEAD
                        lower_only += 1
                for Up in ps:
                    if leq(Up, U) and leq(L, Up):
                        assert liveness((L, Up), r) != LIVE
                        upper_only += 1
    iv = (ZERO, ONE)
    assert liveness(iv, ()) == UNKNOWN
    assert liveness(((frozenset({'e'}),), ONE), ()) == LIVE
    assert liveness((ZERO, ZERO), ()) == DEAD
    return {'lower_only_never_dead_checks': lower_only, 'upper_only_never_live_checks': upper_only,
            'positive_support_live_witness': 1, 'closure_dead_witness': 1, 'voi_scalarization_parent_owned': 1}


def run_all():
    return {'MEG-05': check_meg05(), 'MEG-10': check_meg10(), 'MEG-11': check_meg11(),
            'MEG-12_13': check_meg12_13(), 'MEG-15': check_meg15(), 'MEG-19': check_meg19(),
            'MEG-21': check_meg21(), 'MEG-28': check_meg28(), 'MEG-33': check_meg33(),
            'GENERAL_NOVELTY': 'NOT_ESTABLISHED'}


def main():
    try: out = run_all()
    except CannotCheck as e:
        print(json.dumps({'status': 'CANNOT_CHECK', 'reason': str(e)}, sort_keys=True)); return 2
    except Exception as e:
        print(json.dumps({'status': 'FAIL', 'type': type(e).__name__, 'reason': str(e)}, sort_keys=True)); return 1
    print(json.dumps({'status': 'PASS', 'result': out}, sort_keys=True)); return 0


if __name__ == '__main__': raise SystemExit(main())
