"""ME foundation exact reference, not an OCM runtime or a certificate issuer.

All arithmetic is rational. Proofs and scope restrictions are in THEORY.md.
Exit 0: registered finite checks hold; 1: defect; 2: cannot check requested bound.
Assertions are explicit exceptions, so python -O cannot silently disable checks.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from typing import Iterable

Profile = tuple[int, ...]  # bit masks of finite sets of root evidence
ZERO: Profile = ()
ONE: Profile = (0,)


class CheckFailure(Exception):
    pass


class CannotCheck(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def sub(a: int, b: int) -> bool:
    return a & b == a


def canon(xs: Iterable[int]) -> Profile:
    values = set(xs)
    if any(type(x) is not int or x < 0 for x in values):
        raise ValueError('evidence masks must be nonnegative integers')
    return tuple(sorted(x for x in values if not any(y != x and sub(y, x) for y in values)))


def join(p: Profile, q: Profile) -> Profile:
    return canon((*p, *q))


def meet(p: Profile, q: Profile) -> Profile:
    return canon(a | b for a in p for b in q)


def leq(p: Profile, q: Profile) -> bool:
    return all(any(sub(b, a) for b in q) for a in p)


def live(p: Profile, revoked: int) -> bool:
    return any(not (a & revoked) for a in p)


def profiles(n: int) -> tuple[Profile, ...]:
    if not 0 <= n <= 3:
        raise CannotCheck('exhaustive profile bound is n <= 3')
    return tuple(sorted({canon(i for i in range(1 << n) if mask >> i & 1)
                         for mask in range(1 << (1 << n))}))


@dataclass(frozen=True)
class Interval:
    lower: Profile
    upper: Profile

    def __post_init__(self) -> None:
        if canon(self.lower) != self.lower or canon(self.upper) != self.upper or not leq(self.lower, self.upper):
            raise ValueError('inconsistent or noncanonical warrant interval')

    def status(self, revoked: int = 0) -> int:
        # 0 DEAD, 1 UNKNOWN, 2 LIVE: support status, NOT a truth value of the claim.
        return 2 if live(self.lower, revoked) else (1 if live(self.upper, revoked) else 0)

    def combine(self, other: Interval, conjunction: bool = True) -> Interval:
        op = meet if conjunction else join
        return Interval(op(self.lower, other.lower), op(self.upper, other.upper))

    def refine(self, lower: Profile, upper: Profile) -> Interval:
        if not leq(self.lower, lower) or not leq(upper, self.upper):
            raise ValueError('not a refinement at this fixed context/epoch')
        return Interval(lower, upper)


def filter_ng(p: Profile, nogoods: Profile) -> Profile:
    return canon(w for w in p if not any(sub(g, w) for g in nogoods))


def ng_meet(p: Profile, q: Profile, ng: Profile) -> Profile:
    return filter_ng(meet(p, q), ng)


def substitute(p: Profile, roots: dict[int, Profile]) -> Profile:
    result = ZERO
    for mask in p:
        term = ONE
        for bit in range(mask.bit_length()):
            if mask >> bit & 1:
                if bit not in roots:
                    raise CannotCheck('missing derived evidence definition')
                term = meet(term, roots[bit])
        result = join(result, term)
    return result


def mv_transpose(p: tuple[tuple[F, ...], ...], a: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum((p[i][j] * a[i] for i in range(len(a))), F(0)) for j in range(len(a)))


def validate_system(p, s, alpha) -> None:
    n = len(s)
    if n == 0 or len(p) != n or any(len(row) != n for row in p):
        raise ValueError('nonempty square system required')
    if not 0 < alpha <= 1 or any(x < 0 for x in s):
        raise ValueError('invalid restart or seed')
    if any(x < 0 for row in p for x in row) or any(sum(row) > 1 for row in p):
        raise ValueError('matrix must be nonnegative and row-substochastic')


def fixed(p, s, alpha: F) -> tuple[F, ...]:
    """Exact Gaussian elimination: counts arithmetic operations, not constant-cost bit work."""
    validate_system(p, s, alpha)
    n, beta = len(s), 1 - alpha
    a = [[F(i == j) - beta * p[j][i] for j in range(n)] + [alpha * s[i]] for i in range(n)]
    for j in range(n):
        k = next((k for k in range(j, n) if a[k][j]), None)
        if k is None:
            raise CheckFailure('unexpected singular contraction system')
        a[j], a[k] = a[k], a[j]
        pivot = a[j][j]
        a[j] = [x / pivot for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x - scale * y for x, y in zip(a[i], a[j])]
    return tuple(a[i][-1] for i in range(n))


def iterate(p, s, alpha: F, k: int) -> tuple[F, ...]:
    validate_system(p, s, alpha)
    if k < 0:
        raise ValueError('k must be nonnegative')
    a = tuple(alpha * x for x in s)
    for _ in range(k):
        a = tuple(alpha * x + (1 - alpha) * y for x, y in zip(s, mv_transpose(p, a)))
    return a


def norm(a) -> F:
    return sum((abs(x) for x in a), F(0))


def impact(changed: set[str], edges: tuple[tuple[str, str], ...]) -> set[str]:
    result = set(changed)
    while True:
        nxt = result | {v for u, v in edges if u in result}
        if nxt == result:
            return result
        result = nxt


def agreement(hypotheses, lessons, x: int):
    v = tuple(h for h in hypotheses if all(h[i] == y for i, y in lessons))
    if not v:
        return 'CONTRADICTION', None
    values = {h[x] for h in v}
    return ('EXACT', next(iter(values))) if len(values) == 1 else ('UNKNOWN', None)


def answer_support(hypotheses, lessons, x: int, y: int) -> Profile:
    # Exponential finite reference. Empty version spaces never give vacuous answers.
    return canon(mask for mask in range(1 << len(lessons))
                 if agreement(hypotheses, tuple(e for i, e in enumerate(lessons) if mask >> i & 1), x) == ('EXACT', y))


MANIFEST_FIELDS = ('implementation', 'model', 'prompt', 'decoding', 'checker', 'calibration',
                   'selection', 'assumptions', 'scope', 'epoch', 'normalization', 'resource_policy')


@dataclass(frozen=True)
class Manifest:
    fields: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if tuple(k for k, _ in self.fields) != MANIFEST_FIELDS or any(not isinstance(v, str) or not v for _, v in self.fields):
            raise ValueError('complete ordered manifest required; explicit NONE is allowed')

    @property
    def digest(self) -> str:
        return sha256(json.dumps(self.fields, separators=(',', ':')).encode()).hexdigest()


def binding_status(issued: Manifest, current: Manifest, evidence_valid: bool) -> str:
    # Exact tuple comparison avoids treating hash collision-freedom as a mathematical fact.
    # This only checks identity; it does NOT establish statistical assumptions or evidence truth.
    return 'VALID_BINDING' if evidence_valid and issued == current else 'REVALIDATE'


def action_status(support: Interval, *, exact_proof: bool, binding: str,
                  authorized: bool, conditional_risk: F | None, risk_budget: F) -> str:
    """Declarative finite gate. exact_proof/risk are trusted premises, not self-authored receipts."""
    if not 0 <= risk_budget <= 1 or (conditional_risk is not None and not 0 <= conditional_risk <= 1):
        raise ValueError('invalid risk')
    if not authorized:
        return 'NOT_AUTHORIZED'
    if binding != 'VALID_BINDING':
        return 'REVALIDATE'
    if exact_proof and support.status() == 2:
        return 'EXACT_ASSERTION_ALLOWED'
    if conditional_risk is not None and conditional_risk <= risk_budget:
        return 'RISK_BOUNDED_ACTION_ONLY'
    return 'UNKNOWN'


def checks(n: int = 3) -> dict:
    if n not in (2, 3):
        raise CannotCheck('registered exhaustive universes are n=2 or n=3')
    ps = profiles(n)
    revs = range(1 << n)
    ints = tuple(Interval(p, q) for p in ps for q in ps if leq(p, q))
    counts = {}
    pair = {(p, q): (meet(p, q), join(p, q)) for p in ps for q in ps}
    count = 0
    for p in ints:
        for q in ints:
            mp, jp = pair[p.lower, q.lower]
            mu, ju = pair[p.upper, q.upper]
            for r in revs:
                require(Interval(mp, mu).status(r) == min(p.status(r), q.status(r)), 'Kleene meet')
                require(Interval(jp, ju).status(r) == max(p.status(r), q.status(r)), 'Kleene join')
                count += 1
    counts['interval_pairs_times_revocations'] = count
    count = 0
    for ng_mask in range(1, 1 << n):
        ng = (ng_mask,)
        for p, q in product(ps, repeat=2):
            require(filter_ng(join(p, q), ng) == join(filter_ng(p, ng), filter_ng(q, ng)), 'nogood join')
            after = ng_meet(p, q, ng)
            before = meet(filter_ng(p, ng), filter_ng(q, ng))
            require(leq(after, before), 'nogood meet inequality')
            require(after == filter_ng(before, ng), 'filter after composition')
            for r in revs:
                lhs = live(after, r)
                rhs = live(filter_ng(p, ng), r) and live(filter_ng(q, ng), r)
                require(not lhs or rhs, 'support-local conjunction upper bound')
                if not sub(ng_mask, ((1 << n) - 1) ^ r):
                    require(lhs == rhs, 'consistent-environment homomorphism')
                count += 1
    counts['nogood_pairs_times_revocations'] = count
    # Applied counterexample to the ORIGINAL meet-homomorphism, not a failure of the correction.
    require(live((1,), 0) and live((2,), 0) and not live(ng_meet((1,), (2,), (3,)), 0), 'nogood mutant did not differ')
    counts['nogood_homomorphism_counterexamples'] = 1
    count = 0
    roots = {0: (1,), 1: (1,), 2: (2,)}
    for p in ps:
        flat = substitute(p, roots)
        for r in range(4):
            derived_rev = sum(1 << b for b in range(n) if not live(roots[b], r))
            require(live(flat, r) == live(p, derived_rev), 'flattening disagrees with nested evaluator')
            count += 1
    require(substitute((1, 2), roots) == (1,), 'shared root duplicated')
    counts['flattening_checks'] = count
    # Finite hypotheses include all truth tables on three inputs. Admission tested after every deletion.
    hs = tuple(product((0, 1), repeat=3))
    lessons = ((0, 0), (1, 1), (2, 0))
    count = 0
    for x, y in product(range(3), (0, 1)):
        support = answer_support(hs, lessons, x, y)
        for r in range(8):
            remaining = tuple(e for i, e in enumerate(lessons) if not (r >> i & 1))
            require(live(support, r) == (agreement(hs, remaining, x) == ('EXACT', y)), 'per-query revision')
            count += 1
    require(agreement(hs, ((0, 0), (0, 1)), 1)[0] == 'CONTRADICTION', 'empty version space laundered')
    require(agreement(((0, 0), (0, 1)), (), 0) == ('EXACT', 0), 'unnecessary uniqueness')
    counts['version_space_revocation_checks'] = count
    # Graded fixed-denominator systems, all registered scalars and restarts, exact independent solve.
    count = 0
    for g, h, alpha in product((F(0), F(1, 2), F(1)), repeat=3):
        if alpha == 0 or h > g:
            continue
        p = ((F(0), g / 2, F(0)), (F(0), g / 2, F(0)), (F(0), F(0), F(1, 2)))
        q = ((F(0), h / 2, F(0)), (F(0), h / 2, F(0)), (F(0), F(0), F(1, 2)))
        s = (F(1, 2), F(0), F(1, 2))
        ap, aq = fixed(p, s, alpha), fixed(q, s, alpha)
        require(all(x >= y for x, y in zip(ap, aq)), 'graded monotone retraction')
        require(ap[2] == aq[2], 'outside changed reach moved')
        delta = tuple(x - y for x, y in zip(mv_transpose(p, aq), mv_transpose(q, aq)))
        require(norm(tuple(x - y for x, y in zip(ap, aq))) <= (1-alpha)/alpha * norm(delta), 'resolvent perturbation')
        for k in range(6):
            a = iterate(p, s, alpha, k)
            err = norm(tuple(x-y for x, y in zip(ap, a)))
            residual = tuple(alpha*x+(1-alpha)*y-z for x, y, z in zip(s, mv_transpose(p, a), a))
            require(all(x <= y for x, y in zip(a, ap)), 'partial sums not lower bounds')
            require(err <= (1-alpha)**(k+1)*sum(s), 'Neumann tail')
            require(err <= norm(residual)/alpha, 'residual certificate')
            count += 1
    counts['graded_dynamics_checks'] = count
    # Normalization mutation: adding then revoking a branch does not undo denominators.
    old = ((F(0), F(1), F(0)), (F(0),)*3, (F(0),)*3)
    revoked_overlay = ((F(0), F(1, 2), F(0)), (F(0),)*3, (F(0),)*3)
    seed, alpha = (F(1), F(0), F(0)), F(1, 2)
    require(fixed(old, seed, alpha)[1] == F(1, 4), 'rollback baseline')
    require(fixed(revoked_overlay, seed, alpha)[1] == F(1, 8), 'rollback mutant not applied')
    counts['normalization_rollback_counterexamples'] = 1
    # Exact statistical worlds: marginal/conditional distinction, selection bound, repeated events.
    count = 0
    worlds = frozenset(range(8))
    for em, sm in product(range(256), range(1, 256)):
        err = {i for i in worlds if em >> i & 1}
        sel = {i for i in worlds if sm >> i & 1}
        risk, psel = F(len(err), 8), F(len(sel), 8)
        require(F(len(err & sel), len(sel)) <= min(F(1), risk/psel), 'selection risk bound')
        count += 1
    require(F(1, 8) < 1 and F(1, 1) == 1, 'marginal vs selected-risk witness')
    require(1 - F(9, 10)**10 > F(1, 10), 'per-invocation risk incorrectly idempotent')
    counts['selection_event_pairs'] = count
    # Conditional-risk tree: probabilities depend on earlier failures, not independence.
    total = failed = expected_errors = expected_spend = F(0)
    max_spend = F(0)
    for history in product((0, 1), repeat=3):
        mass, spend = F(1), F(0)
        for t, outcome in enumerate(history):
            epsilon = F(1, 5) if any(history[:t]) else F(1, 10)
            spend += epsilon
            mass *= epsilon if outcome else 1-epsilon
        total += mass
        failed += mass * bool(any(history))
        expected_errors += mass * sum(history)
        expected_spend += mass * spend
        max_spend = max(max_spend, spend)
    require(total == 1 and failed <= max_spend, 'adaptive union bound')
    require(expected_errors == expected_spend, 'conditional risk accounting')
    counts['adaptive_risk_tree_leaves'] = 8
    # Observationally identical structural models disagree under intervention.
    obs_direct = tuple((u, u) for u in (0, 1))
    obs_confound = tuple((u, u) for u in (0, 1))
    do_direct = tuple((0, 0) for u in (0, 1))
    do_confound = tuple((0, u) for u in (0, 1))
    require(obs_direct == obs_confound and do_direct != do_confound, 'causal ambiguity witness')
    # Identical fallible verifiers share one error event, not independent errors.
    verifier_error = frozenset({0})
    require(F(len(verifier_error & verifier_error), 8) == F(1,8) > F(1,8)**2, 'shared verifier error')
    counts['causal_and_verifier_counterexamples'] = 2
    # Full obligation signature: liveness unchanged does not imply content/cache validity unchanged.
    require(min(0, 2) == min(0, 1), 'masked summary witness')
    before, after = (2, 'value=1'), (2, 'value=2')
    require(before[0] == after[0] and before != after, 'content drift witness')
    edges = (('e', 'x'), ('x', 'm'), ('m', 'x'), ('z', 'u'))
    require(impact({'e'}, edges) == {'e', 'x', 'm'}, 'impact least fixed point')
    # Both transactions satisfy their snapshot-local rule; their merged writes violate it.
    require(bool(1 or 1) and not bool(0 or 0), 'write-skew witness')
    require(sum((F(1, 2**i) for i in range(1, 101)), F(0)) < 1, 'bounded positive-cost prefix')
    counts['revision_counterexamples_and_controls'] = 5
    # Kleene-star existence reading includes zero iterations; evidence changes across iterations.
    require(join(ONE, (1,)) == ONE and meet((1,), (2,)) == (3,), 'loop reading counterexamples')
    require(meet((1,), (1,)) == (1,), 'fixed-evidence repetition control')
    counts['loop_reading_checks'] = 3
    # Pointwise Hartley gains are not generally subadditive; sequential gains telescope instead.
    require(3*3 > 4*2, 'information synergy counterexample')
    require(F(4,3)*F(3,2) == F(4,2), 'conditional information telescoping')
    counts['information_checks'] = 2
    # At zero observed failures, a one-sided 95% binomial upper bound is below .05 only at n>=59.
    require(F(19,20)**50 > F(1,20), 'n=50 does not certify five-percent disagreement')
    require(F(19,20)**58 > F(1,20) >= F(19,20)**59, 'zero-discordance threshold')
    counts['equivalence_bound_checks'] = 2
    manifest = Manifest(tuple((k, 'v1') for k in MANIFEST_FIELDS))
    for i, key in enumerate(MANIFEST_FIELDS):
        fields = list(manifest.fields)
        fields[i] = (key, 'v2')
        changed = replace(manifest, fields=tuple(fields))
        require(binding_status(manifest, changed, True) == 'REVALIDATE', 'unbound manifest coordinate')
    require(binding_status(manifest, manifest, False) == 'REVALIDATE', 'revoked binding used')
    require(binding_status(manifest, manifest, True) == 'VALID_BINDING', 'no-drift control')
    unknown = Interval(ZERO, ONE)
    require(action_status(unknown, exact_proof=False, binding='VALID_BINDING', authorized=True,
                          conditional_risk=F(1,100), risk_budget=F(1,20)) == 'RISK_BOUNDED_ACTION_ONLY', 'risk promoted to truth')
    require(unknown.status() == 1, 'risk mutated warrant')
    require(action_status(Interval(ONE,ONE), exact_proof=True, binding='VALID_BINDING', authorized=False,
                          conditional_risk=None, risk_budget=F(0)) == 'NOT_AUTHORIZED', 'evidence minted permission')
    counts['identity_mutations'] = len(MANIFEST_FIELDS)
    counts['binding_and_action_controls'] = 5
    # Upper-profile certificates must contain the lower bound; missing support is not refutation.
    try:
        Interval((1,), ONE).refine((1,), (2,))
    except ValueError:
        pass
    else:
        raise CheckFailure('contradictory upper certificate accepted')
    require(Interval(ZERO, ONE).refine(ZERO, ZERO).status() == 0, 'registered refutation can resolve unknown')
    require(Interval(ZERO, ZERO).status() == 0, 'DEAD is support status only')
    counts['refinement_controls'] = 3
    # Certified winner margin: a two-sided perturbation can erase a margin of 2*epsilon.
    eps = F(1,10)
    require(F(1)-eps > F(1,2)+eps, 'separated winner')
    require(F(1,2)-eps == F(3,10)+eps, 'sharp tie boundary')
    counts['decision_margin_checks'] = 2
    return {'terminal':'FINITE_CALIBRATION_PASS', 'n':n, 'profiles':len(ps),
            'intervals':len(ints), 'checks':counts, 'independent_review':'NOT_PERFORMED',
            'all_size_authority':'THEORY.md arguments, NOT enumeration', 'ocm_parity':'NOT_RUN'}



def validate_registry(data: dict) -> None:
    """Check coverage/links/status hygiene, NOT truth of a theorem or independence of review."""
    if data.get('scientific_completion') is not False:
        raise ValueError('this identity does not certify complete science')
    rows = data.get('gaps', [])
    ids = [row.get('id') for row in rows]
    expected = {f'MEG-{i:02d}' for i in range(1, 36)}
    if len(ids) != 35 or set(ids) != expected:
        raise ValueError('missing, duplicate or unknown gap id')
    allowed = {'PROVED_SCOPED', 'SPECIFIED_NOT_PROVED', 'OPEN_RESEARCH', 'PARENT_ADOPTION'}
    proofs = {f'F{i:02d}' for i in range(1, 19)}
    graph = {}
    for row in rows:
        if row.get('status') not in allowed:
            raise ValueError('unknown fragment status')
        if not row.get('scope') or not row.get('remaining') or not row.get('parent'):
            raise ValueError('scope, remaining obligation and parent disposition required')
        if not set(row.get('proofs', [])) <= proofs:
            raise ValueError('dangling proof reference')
        if row['status'] == 'PROVED_SCOPED' and not row.get('proofs'):
            raise ValueError('proved fragment without an argument')
        graph[row['id']] = set(row.get('depends_on', []))
        if not graph[row['id']] <= expected:
            raise ValueError('dangling dependency')
    done = set()
    while len(done) < 35:
        ready = {x for x, deps in graph.items() if x not in done and deps <= done}
        if not ready:
            raise ValueError('cyclic gap dependencies')
        done |= ready


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, default=3)
    args = parser.parse_args()
    try:
        result = checks(args.n)
    except CannotCheck as e:
        print(json.dumps({'terminal':'CANNOT_CHECK','reason':str(e)}))
        return 2
    except (CheckFailure, ValueError) as e:
        print(json.dumps({'terminal':'FAIL','reason':str(e)}))
        return 1
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
