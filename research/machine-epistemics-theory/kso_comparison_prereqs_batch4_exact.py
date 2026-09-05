"""Exact finite checker for KSO_COMPARISON_PREREQUISITE_THEOREMS_BATCH4_V1.md (stdlib only, exact).

One check function per theorem (D1–D8, atlas ids MEG-32/14/02/07/20/34/09/23).  Every check performs
(a) the positive statement, (b) at least one planted mutant whose mutation is asserted applied and which
must be caught, and (c) a no-alarm control.  The minimal objects of the OCM core are re-implemented
here (antichain semiring, warrant intervals, Kleene liveness, authority meet, frozen-denominator
navigation with exact rational fixed points, impact cone / reopening report, version spaces and the B2
per-input warrant, quotients / lumpability / measurability, DPO-style organisation rewrites, exact
binomial / multinomial enumeration); nothing is imported from ``ocm``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import sys
from fractions import Fraction
from functools import lru_cache
from math import comb, factorial, log2


class CannotCheck(RuntimeError):
    pass


# ---------------------------------------------------------------------------------------------
# antichain semiring (KS-T01), intervals, Kleene liveness (KS-T21) — as in batches 1–3
# ---------------------------------------------------------------------------------------------


def canon(items):
    unique = {frozenset(w) for w in items}
    return tuple(sorted((w for w in unique if not any(v < w for v in unique)), key=lambda w: (len(w), sorted(map(repr, w)))))


ZERO, ONE = (), (frozenset(),)


def join(p, q):
    return canon((*p, *q))


def meet(p, q):
    if not p or not q:
        return ZERO
    return canon(a | b for a in p for b in q)


def meet_all(ps):
    out = ONE
    for p in ps:
        out = meet(out, p)
    return out


def live(p, r):
    r = frozenset(r)
    return any(not (w & r) for w in p)


LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


def kand(a, b):
    return DEAD if DEAD in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else LIVE)


def liveness(iv, r):
    lo, up = iv
    if live(lo, r):
        return LIVE
    if not live(up, r):
        return DEAD
    return UNKNOWN


def imeet(p, q):
    return (meet(p[0], q[0]), meet(p[1], q[1]))


def ijoin(p, q):
    return (join(p[0], q[0]), join(p[1], q[1]))


def cert(*warrants):
    p = canon(frozenset(w) for w in warrants)
    return (p, p)


IONE = (ONE, ONE)
IUNKNOWN = (ZERO, ONE)


def subsets(universe):
    u = sorted(universe, key=repr)
    return [frozenset(c) for k in range(len(u) + 1) for c in itertools.combinations(u, k)]


def all_profiles(n):
    subs = subsets(range(n))
    out = set()
    for mask in range(1 << len(subs)):
        out.add(canon([subs[i] for i in range(len(subs)) if mask & (1 << i)]))
    return sorted(out, key=lambda p: (len(p), [sorted(w) for w in p]))


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=repr).encode()).hexdigest()


def auth_meet(*items):
    keys = set().union(*(set(a) for a in items))
    return {k: min(a.get(k, 0) for a in items) for k in keys}


DEPENDENCY = frozenset({"DEPENDENCE", "SUPPORT", "COMPOSITION", "CONSTRAINT"})


def edge(eid, tails, heads, w=1, hw=None, iv=IONE, rel="DEPENDENCE"):
    tails = (tails,) if isinstance(tails, str) else tuple(tails)
    heads = (heads,) if isinstance(heads, str) else tuple(heads)
    return (eid, tails, heads, Fraction(w), tuple(Fraction(x) for x in (hw or [1] * len(heads))), iv, rel)


# ---------------------------------------------------------------------------------------------
# navigation: frozen denominators, gated matrix, exact restart fixed point (KS-T03/T04b/T05)
# ---------------------------------------------------------------------------------------------


def nav_matrix(atoms, edges, revoked):
    """Gated matrix with denominators frozen on the registered structure; dead mass dissipates."""
    ids = list(atoms)
    idx = {x: i for i, x in enumerate(ids)}
    out = [[Fraction(0) for _ in ids] for _ in ids]
    denom = {x: Fraction(0) for x in ids}
    for _, tails, _, w, _, _, _ in edges:
        for t in tails:
            denom[t] += w
    lv = {x: liveness(atoms[x], revoked) == LIVE for x in ids}
    for _, tails, heads, w, hw, ew, _ in edges:
        if w == 0 or liveness(ew, revoked) != LIVE or not all(lv[t] for t in tails):
            continue
        total = sum(hw, Fraction(0))
        for t in tails:
            if denom[t] == 0:
                continue
            for h, x in zip(heads, hw):
                if lv[h]:
                    out[idx[t]][idx[h]] += (w / denom[t]) * (x / total)
    return ids, out


def fixed_point(p, seed, alpha):
    """Unique solution of a = α s + (1−α) Pᵀ a (exact Gauss–Jordan)."""
    n = len(p)
    aug = [[Fraction(int(i == j)) - (1 - alpha) * p[j][i] for j in range(n)] + [alpha * seed[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if piv is None:
            raise CannotCheck("singular navigation system")
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    return [row[-1] for row in aug]


ALPHA_NAV = Fraction(1, 3)


def gated_seed(atoms, ids, revoked, seed_map):
    return [seed_map.get(x, Fraction(0)) if liveness(atoms[x], revoked) == LIVE else Fraction(0) for x in ids]


def solve_activation(atoms, edges, revoked, seed_map, alpha=ALPHA_NAV, matrix=None):
    ids, p = matrix or nav_matrix(atoms, edges, revoked)
    return dict(zip(ids, fixed_point(p, gated_seed(atoms, ids, revoked, seed_map), alpha)))


def uniform_seed(atoms):
    n = Fraction(1, len(atoms))
    return {x: n for x in atoms}


def reach_ungated(start, edges):
    out = set(start)
    grew = True
    while grew:
        grew = False
        for _, tails, heads, *_ in edges:
            if any(t in out for t in tails):
                for h in heads:
                    if h not in out:
                        out.add(h)
                        grew = True
    return frozenset(out)


def random_space(rng, n_atoms, n_edges, n_ev):
    atoms = {}
    for i in range(n_atoms):
        w1 = frozenset(rng.sample(range(n_ev), rng.randint(1, 2)))
        atoms[f"v{i}"] = cert(w1) if rng.random() < 0.7 else cert(w1, frozenset(rng.sample(range(n_ev), 1)))
    edges = []
    names = list(atoms)
    for j in range(n_edges):
        t = rng.choice(names)
        h = rng.choice([x for x in names if x != t])
        edges.append(edge(f"e{j}", t, h, w=rng.randint(1, 3)))
    return atoms, edges


# ---------------------------------------------------------------------------------------------
# D1 · MEG-32 · adopt-not-invent: pre-registered exact equivalence / residual decision rules
# ---------------------------------------------------------------------------------------------

ALPHA, DELTA, HALF = Fraction(1, 20), Fraction(1, 10), Fraction(1, 2)
RESIDUAL, PARENT_SUFFICIENT, PARENT_DOMINATES, INCONCLUSIVE = "RESIDUAL_SUPPORTED", "PARENT_SUFFICIENT", "PARENT_DOMINATES", "INCONCLUSIVE"
VERDICTS = (RESIDUAL, PARENT_SUFFICIENT, PARENT_DOMINATES, INCONCLUSIVE)


def binom_pmf(n, k, p):
    return Fraction(comb(n, k)) * p**k * (1 - p) ** (n - k)


@lru_cache(maxsize=None)
def pmf_table(n, p):
    pmf = [binom_pmf(n, j, p) for j in range(n + 1)]
    cum, acc = [], Fraction(0)
    for x in pmf:
        acc += x
        cum.append(acc)
    return tuple(pmf), tuple(cum)


def p_ge(n, k, p):
    _, cum = pmf_table(n, p)
    return Fraction(1) if k <= 0 else (Fraction(0) if k > n else 1 - cum[k - 1])


def p_le(n, k, p):
    _, cum = pmf_table(n, p)
    return Fraction(0) if k < 0 else cum[min(k, n)]


def decide_discordant(n10, n01, delta=DELTA, alpha=ALPHA):
    """Pre-registered rule on the discordant scale p_d = P(OCM wins | discordant pair).
    RESIDUAL: exact one-sided binomial rejects H0: p_d ≤ ½+δ.  PARENT_SUFFICIENT: TOST (both
    H0: p_d ≤ ½−δ and H0: p_d ≥ ½+δ rejected).  PARENT_DOMINATES: H0: p_d ≥ ½−δ rejected."""
    nd = n10 + n01
    if nd == 0:
        return INCONCLUSIVE
    if p_ge(nd, n10, HALF + delta) <= alpha:
        return RESIDUAL
    if p_le(nd, n10, HALF - delta) <= alpha:
        return PARENT_DOMINATES
    if p_ge(nd, n10, HALF - delta) <= alpha and p_le(nd, n10, HALF + delta) <= alpha:
        return PARENT_SUFFICIENT
    return INCONCLUSIVE


def mcnemar_exact_two_sided(n10, n01):
    nd = n10 + n01
    if nd == 0:
        return Fraction(1)
    return min(Fraction(1), 2 * min(p_ge(nd, n10, HALF), p_le(nd, n10, HALF)))


def decide_unconditional_equivalence(n, n10, n01, delta_u, alpha=ALPHA):
    """Paired-difference scale θ = p10 − p01: PARENT_SUFFICIENT iff both H0: p10 ≥ δ_u and
    H0: p01 ≥ δ_u are rejected by exact one-sided binomial tests at α/2 (⇒ |θ| < δ_u at 1−α)."""
    a2 = alpha / 2
    if p_le(n, n10, delta_u) <= a2 and p_le(n, n01, delta_u) <= a2:
        return PARENT_SUFFICIENT
    return INCONCLUSIVE


def clopper_pearson(nd, n10, alpha=ALPHA, grid=1000):
    lower = next((Fraction(k, grid) for k in range(grid + 1) if p_ge(nd, n10, Fraction(k, grid)) > alpha / 2), Fraction(1))
    upper = next((Fraction(k, grid) for k in range(grid, -1, -1) if p_le(nd, n10, Fraction(k, grid)) > alpha / 2), Fraction(0))
    return lower, upper


def verdict_distribution(rule, nd, p):
    out = {v: Fraction(0) for v in VERDICTS}
    for n10 in range(nd + 1):
        out[rule(n10, nd - n10)] += binom_pmf(nd, n10, p)
    return out


def mutant_p_gt_005_equivalent(n10, n01):
    """Planted: 'not significantly different ⇒ equivalent'."""
    if n10 + n01 == 0:
        return INCONCLUSIVE
    return PARENT_SUFFICIENT if mcnemar_exact_two_sided(n10, n01) > Fraction(1, 20) else RESIDUAL


def mutant_stop_when_leading_size(p, n_max, delta=DELTA, alpha=ALPHA):
    """Planted: look after every discordant pair and stop at the first rejection.  Exact
    probability of ever declaring RESIDUAL under p (DP over (n, wins))."""
    dist = {0: Fraction(1)}
    ever = Fraction(0)
    for n in range(1, n_max + 1):
        nxt = {}
        for b, pr in dist.items():
            for win in (0, 1):
                nb = b + win
                nxt[nb] = nxt.get(nb, Fraction(0)) + pr * (p if win else 1 - p)
        dist = {}
        for b, pr in nxt.items():
            if p_ge(n, b, HALF + delta) <= alpha:
                ever += pr
            else:
                dist[b] = pr
    return ever


def mutant_posthoc_exclusion_size(nd, p, k):
    """Planted: after seeing the table, relabel up to k OCM losses as 'annotation errors'."""
    total = Fraction(0)
    for b in range(nd + 1):
        losses = nd - b
        if decide_discordant(b, losses - min(k, losses)) == RESIDUAL:
            total += binom_pmf(nd, b, p)
    return total


def multinomial_tables(n):
    for n11 in range(n + 1):
        for n10 in range(n - n11 + 1):
            for n01 in range(n - n11 - n10 + 1):
                yield n11, n10, n01, n - n11 - n10 - n01


def multinomial_pmf(table, probs):
    n = sum(table)
    out = Fraction(factorial(n))
    for k, p in zip(table, probs):
        out = out * p**k / factorial(k)
    return out


def check_d1_meg32_equivalence_rules():
    size_checks = 0
    worst = {RESIDUAL: Fraction(0), PARENT_SUFFICIENT: Fraction(0), PARENT_DOMINATES: Fraction(0)}
    grid = [Fraction(k, 20) for k in range(21)]
    for nd in range(1, 16):
        for p in grid:
            d = verdict_distribution(decide_discordant, nd, p)
            if p <= HALF + DELTA:
                assert d[RESIDUAL] <= ALPHA, (nd, p, d)
                worst[RESIDUAL] = max(worst[RESIDUAL], d[RESIDUAL])
            if p >= HALF - DELTA:
                assert d[PARENT_DOMINATES] <= ALPHA
                worst[PARENT_DOMINATES] = max(worst[PARENT_DOMINATES], d[PARENT_DOMINATES])
            if abs(p - HALF) >= DELTA:
                assert d[PARENT_SUFFICIENT] <= ALPHA
                worst[PARENT_SUFFICIENT] = max(worst[PARENT_SUFFICIENT], d[PARENT_SUFFICIENT])
            size_checks += 1
    # exhaustive over small-n outcome tables (n11, n10, n01, n00), multinomial cell probabilities on a grid
    tables_checked = grids = 0
    for n in range(1, 11):
        tables = list(multinomial_tables(n))
        for r in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
            for pd in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 5), Fraction(3, 4), Fraction(1)):
                probs = ((1 - r) / 2, r * pd, r * (1 - pd), (1 - r) / 2)
                mass = {v: Fraction(0) for v in VERDICTS}
                for t in tables:
                    mass[decide_discordant(t[1], t[2])] += multinomial_pmf(t, probs)
                assert sum(mass.values()) == 1
                if pd <= HALF + DELTA:
                    assert mass[RESIDUAL] <= ALPHA
                if abs(pd - HALF) >= DELTA:
                    assert mass[PARENT_SUFFICIENT] <= ALPHA
                grids += 1
                tables_checked += len(tables)
    # unconditional (paired-difference) equivalence rule: size ≤ α/2 exhaustively for n ≤ 8
    delta_u = Fraction(1, 5)
    uncond_checks = 0
    for n in range(1, 9):
        tables = list(multinomial_tables(n))
        for p10 in (Fraction(0), Fraction(1, 10), Fraction(1, 5), Fraction(2, 5)):
            for p01 in (Fraction(0), Fraction(1, 10), Fraction(1, 5), Fraction(2, 5)):
                probs = ((1 - p10 - p01) / 2, p10, p01, (1 - p10 - p01) / 2)
                mass = sum((multinomial_pmf(t, probs) for t in tables if decide_unconditional_equivalence(n, t[1], t[2], delta_u) == PARENT_SUFFICIENT), Fraction(0))
                if max(p10, p01) >= delta_u:
                    assert mass <= ALPHA / 2
                uncond_checks += 1
    assert decide_unconditional_equivalence(20, 0, 0, delta_u) == PARENT_SUFFICIENT and decide_unconditional_equivalence(8, 0, 0, delta_u) == INCONCLUSIVE
    # ME-X3 0/540 discordance: the smallest margin (1/1000 grid) at which PARENT_SUFFICIENT is an equivalence
    m2_margin = next(Fraction(k, 1000) for k in range(1, 1000) if (1 - Fraction(k, 1000)) ** 540 <= ALPHA / 2)
    assert decide_unconditional_equivalence(540, 0, 0, m2_margin) == PARENT_SUFFICIENT and decide_discordant(0, 0) == INCONCLUSIVE
    # power curves (exact) for planned discordant counts
    power = {}
    for nd in (10, 20, 30, 50):
        for p in (HALF, Fraction(3, 5), Fraction(7, 10), Fraction(4, 5), Fraction(9, 10)):
            power[f"residual@nd={nd},p={p}"] = round(float(verdict_distribution(decide_discordant, nd, p)[RESIDUAL]), 4)
    equiv_power = {nd: round(float(verdict_distribution(decide_discordant, nd, HALF)[PARENT_SUFFICIENT]), 4) for nd in (10, 20, 30, 50, 100, 200)}
    first_nd_with_equivalence_power = next((nd for nd in range(1, 301) if verdict_distribution(decide_discordant, nd, HALF)[PARENT_SUFFICIENT] > 0), None)
    assert power["residual@nd=20,p=9/10"] > 0.5 and equiv_power[200] > equiv_power[100]
    # the equivalence size bound is exercised where TOST can pass at all (nd ≥ 76 at δ = 1/10): false PARENT_SUFFICIENT ≤ α, and > 0
    eq_size_checks, worst_eq = 0, Fraction(0)
    for nd in (76, 100, 150, 200):
        for p in (Fraction(0), Fraction(1, 5), HALF - DELTA, HALF + DELTA, Fraction(4, 5), Fraction(1)):
            d = verdict_distribution(decide_discordant, nd, p)
            assert d[PARENT_SUFFICIENT] <= ALPHA
            worst_eq = max(worst_eq, d[PARENT_SUFFICIENT])
            eq_size_checks += 1
    assert worst_eq > 0
    ci = clopper_pearson(20, 15)
    assert ci[0] < Fraction(3, 4) < ci[1]
    # mutants
    m1 = verdict_distribution(mutant_p_gt_005_equivalent, 10, Fraction(7, 10))[PARENT_SUFFICIENT]
    assert m1 > ALPHA
    m2 = mutant_stop_when_leading_size(HALF + DELTA, 30)
    fixed_size = verdict_distribution(decide_discordant, 30, HALF + DELTA)[RESIDUAL]
    assert m2 > ALPHA >= fixed_size
    m3 = mutant_posthoc_exclusion_size(20, HALF + DELTA, 2)
    assert m3 > ALPHA >= verdict_distribution(decide_discordant, 20, HALF + DELTA)[RESIDUAL]
    return {
        "size_checks": size_checks, "worst_false_residual": str(worst[RESIDUAL]), "worst_false_equivalence": str(worst[PARENT_SUFFICIENT]),
        "tables_checked": tables_checked, "table_grids": grids, "unconditional_grid_checks": uncond_checks,
        "m2_zero_discordance_margin": str(m2_margin), "m2_conditional_verdict": decide_discordant(0, 0),
        "power": power, "equivalence_power_at_half": equiv_power, "first_nd_equivalence_possible": first_nd_with_equivalence_power,
        "equivalence_size_checks_large_nd": eq_size_checks, "worst_false_equivalence_large_nd": round(float(worst_eq), 4),
        "cp_interval_20_15": [str(ci[0]), str(ci[1])],
        "mutant_p_gt_005_false_equivalence": round(float(m1), 4), "mutant_optional_stopping_size": round(float(m2), 4),
        "mutant_posthoc_exclusion_size": round(float(m3), 4), "fixed_rule_size_at_boundary_30": round(float(fixed_size), 4),
    }


# ---------------------------------------------------------------------------------------------
# D2 · MEG-14 · per-channel acquisition bounds on the registered finite classes (parent-owned table)
# ---------------------------------------------------------------------------------------------

INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))
ALL16 = tuple(itertools.product((0, 1), repeat=4))
AFFINE8 = tuple(t for t in ALL16 if sum(t) % 2 == 0)
MONOTONE6 = tuple(t for t in ALL16 if all(t[i] <= t[j] for i in range(4) for j in range(4) if all(a <= b for a, b in zip(INPUTS[i], INPUTS[j]))))
# six transitive-clause orders (L0 construction class): input kinds = aligned pair with distinct nouns
# (reveals the order) or with the same lexeme as agent and patient (reveals the verb position only)
SIX_ORDERS = tuple("".join(p) for p in itertools.permutations("SVO"))
SIX_ORDER_CLASS = tuple((o, o.index("V")) for o in SIX_ORDERS)
CLASSES = {"ALL16": ALL16, "AFFINE8": AFFINE8, "MONOTONE6": MONOTONE6, "SIX_ORDERS": SIX_ORDER_CLASS}


def consistent(cls, h, T):
    return [g for g in cls if all(g[i] == h[i] for i in T)]


def teaching_dimension(cls):
    n = len(cls[0])
    per = {}
    for h in cls:
        per[h] = next(k for k in range(n + 1) if any(len(consistent(cls, h, T)) == 1 for T in itertools.combinations(range(n), k)))
    return max(per.values()), per


def extended_teaching_dimension(cls):
    n = len(cls[0])
    alphabets = [sorted({h[i] for h in cls}) for i in range(n)]
    best = 0
    for f in itertools.product(*alphabets):
        spec = next(k for k in range(n + 1) if any(len(consistent(cls, f, T)) <= 1 for T in itertools.combinations(range(n), k)))
        best = max(best, spec)
    return best


def membership_query_complexity(cls):
    n = len(cls[0])
    memo = {}

    def rec(V):
        if len(V) <= 1:
            return 0
        if V in memo:
            return memo[V]
        best = n + 1
        for i in range(n):
            groups = {}
            for h in V:
                groups.setdefault(h[i], []).append(h)
            if len(groups) == 1:
                continue
            best = min(best, 1 + max(rec(frozenset(g)) for g in groups.values()))
        memo[V] = best
        return best

    return rec(frozenset(cls))


def demonstration_from_random_pairs(cls, dist, n_max):
    """Exact identification from i.i.d. aligned pairs whose input is drawn from ``dist``: for each
    true h, the absorbing chain on 'inputs seen'; returns P(identified by n) for n ≤ n_max and the
    exact expected number of pairs (fundamental matrix), averaged over h."""
    n = len(cls[0])
    inputs = list(range(n))
    p_ident = [Fraction(0)] * (n_max + 1)
    expect = Fraction(0)
    for h in cls:
        ident = {T: len(consistent(cls, h, T)) == 1 for T in subsets(inputs)}
        dist_state = {frozenset(): Fraction(1)}
        for k in range(1, n_max + 1):
            nxt = {}
            for T, pr in dist_state.items():
                if ident[T]:
                    nxt[T] = nxt.get(T, Fraction(0)) + pr
                    continue
                for i, q in dist.items():
                    if q:
                        nxt[T | {i}] = nxt.get(T | {i}, Fraction(0)) + pr * q
            dist_state = nxt
            p_ident[k] += sum((pr for T, pr in dist_state.items() if ident[T]), Fraction(0)) / len(cls)
        # expected time: E[T] = Σ_k P(N > k) — solve exactly on the transient states
        transient = [T for T in subsets(inputs) if not ident[T]]
        if any(ident[T] is False and all(dist.get(i, 0) == 0 for i in inputs if i not in T) for T in transient):
            return None  # never identified from this distribution
        idx = {T: j for j, T in enumerate(transient)}
        m = len(transient)
        aug = [[Fraction(int(a == b)) for b in range(m)] + [Fraction(1)] for a in range(m)]
        for T in transient:
            for i, q in dist.items():
                if q and not ident[T | {i}] and (T | {i}) in idx:
                    aug[idx[T]][idx[T | {i}]] -= q
                elif q and (T | {i}) == T:
                    aug[idx[T]][idx[T]] -= q
        sol = fixed_point_generic(aug)
        expect += sol[idx[frozenset()]] / len(cls)
    return {"p_identified": p_ident, "expected_pairs": expect}


def fixed_point_generic(aug):
    n = len(aug)
    aug = [row[:] for row in aug]
    for col in range(n):
        piv = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if piv is None:
            raise CannotCheck("singular system")
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    return [row[-1] for row in aug]


def bits(m_before, m_after):
    return log2(m_before) - log2(m_after)


def audit_measured(cls_name, channel, count, identified):
    """Falsifier: a channel that identifies a target with fewer lessons than the class's lower
    bound for that channel has received information from outside the channel (laundering)."""
    row = BOUNDS[cls_name]
    lower = {"INSTRUCTION": row["teaching_dimension"], "DEMONSTRATION": row["teaching_dimension"], "INTERACTION": row["membership_query_complexity"], "EXPERIMENTATION": row["closure_evaluations"]}[channel]
    if identified and count < lower:
        return "BELOW_LOWER_BOUND"
    return "CONSISTENT"


BOUNDS = {}


def check_d2_meg14_channel_bounds():
    table = {}
    for name, cls in CLASSES.items():
        td, per = teaching_dimension(cls)
        xtd = extended_teaching_dimension(cls)
        mq = membership_query_complexity(cls)
        n_in = len(cls[0])
        uniform = {i: Fraction(1, n_in) for i in range(n_in)}
        demo = demonstration_from_random_pairs(cls, uniform, 24)
        m = len(cls)
        row = {
            "M": m, "log2M_ceil": (m - 1).bit_length(),
            "teaching_dimension": td, "extended_teaching_dimension": xtd, "membership_query_complexity": mq,
            "closure_evaluations": n_in, "demo_expected_pairs_uniform": str(demo["expected_pairs"]),
            "demo_n_for_90pct_uniform": next((k for k in range(25) if demo["p_identified"][k] >= Fraction(9, 10)), None),
        }
        # LI-1 envelope: the certified bits at identification telescope to log2 M (T9); no channel identifies below ⌈log2 M⌉ bits
        assert abs(bits(m, 1) - log2(m)) < 1e-12
        if name != "SIX_ORDERS":   # Boolean membership answers: Hegedüs 1995 XTD ≤ MQ ≤ XTD·⌈log2 M⌉ and MQ ≥ ⌈log2 M⌉
            assert xtd <= mq <= xtd * row["log2M_ceil"] and mq >= row["log2M_ceil"]
        else:
            assert td == xtd == mq == 1   # one distinct-noun pair identifies the order (6-valued answer)
        table[name] = row
        BOUNDS[name] = row
    # exact values pinned by the parent definitions
    assert table["ALL16"]["teaching_dimension"] == 4 and table["ALL16"]["membership_query_complexity"] == 4 and table["ALL16"]["demo_expected_pairs_uniform"] == "25/3"
    assert table["AFFINE8"]["teaching_dimension"] == 3 and table["AFFINE8"]["membership_query_complexity"] == 3 and table["AFFINE8"]["demo_expected_pairs_uniform"] == "13/3"
    # six-order class from a pair distribution with distinct-noun probability q: identified iff q > 0 (else V stalls at 2)
    six_dist = {}
    for q in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)):
        r = demonstration_from_random_pairs(SIX_ORDER_CLASS, {0: q, 1: 1 - q}, 12)
        six_dist[str(q)] = None if r is None else str(r["expected_pairs"])
    assert six_dist["0"] is None and six_dist["1/4"] == "4" and six_dist["1"] == "1"
    # measured lesson counts (KSO_M3_LEARNING_RESULTS_V1.json: class ALL16, target AND, every channel 4, feedback 2 → 16 remain)
    measured = {"INSTRUCTION": 4, "DEMONSTRATION": 4, "INTERACTION": 4, "EXPERIMENTATION": 4}
    audits = {c: audit_measured("ALL16", c, k, True) for c, k in measured.items()}
    assert all(v == "CONSISTENT" for v in audits.values())
    assert all(k == table["ALL16"][{"INSTRUCTION": "teaching_dimension", "DEMONSTRATION": "teaching_dimension", "INTERACTION": "membership_query_complexity", "EXPERIMENTATION": "closure_evaluations"}[c]] for c, k in measured.items())
    incomplete_demo = 16 // 2**3   # M3 hostile: 3 demonstrations leave 16/8 = 2 hypotheses (bits telescope)
    assert incomplete_demo == 2
    # batch-2 B3: AFFINE8, four examples for a⊕b — consistent, one redundant (TD = 3)
    assert audit_measured("AFFINE8", "DEMONSTRATION", 4, True) == "CONSISTENT" and 4 - table["AFFINE8"]["teaching_dimension"] == 1
    # falsifier fires: a claimed identification of AND on ALL16 from 2 demonstrations
    assert audit_measured("ALL16", "DEMONSTRATION", 2, True) == "BELOW_LOWER_BOUND"
    assert audit_measured("ALL16", "INTERACTION", 3, True) == "BELOW_LOWER_BOUND"
    assert audit_measured("ALL16", "DEMONSTRATION", 2, False) == "CONSISTENT"   # not identified: no alarm
    return {"table": table, "six_order_expected_pairs_by_distinct_prob": six_dist, "measured_m3_all16": measured, "audits_m3": audits, "measured_equal_bound_channels": 4,
            "mutant_below_bound_caught": 2, "no_alarm_unidentified": 1, "six_order_measured": "NOT_MEASURED (no lesson-count receipt in KSO_M3/M5 results)"}


# ---------------------------------------------------------------------------------------------
# D3 · MEG-02 (graded half) · statistical operator outputs enter as ⟦0,U⟧ with a score outside the lattice
# ---------------------------------------------------------------------------------------------


def conformal_coverage_exact(n_cal, delta):
    """Split conformal on n_cal + 1 exchangeable distinct scores: exact coverage of the level-(1−δ)
    set = ⌈(n+1)(1−δ)⌉/(n+1), counted over all (n+1)! orderings."""
    k = -(-((n_cal + 1) * (1 - delta)) // 1)   # ceil
    k = int(k)
    total = covered = 0
    for perm in itertools.permutations(range(n_cal + 1)):
        total += 1
        test_rank = perm.index(0)   # score 0 (the test point's identity) placed at its rank position
        if test_rank + 1 <= k:
            covered += 1
    return Fraction(covered, total), k


def check_d3_meg02_graded_operator_warrant():
    # (i) no composition whose components are all UNKNOWN is LIVE (exhaustive at n = 3)
    profiles = all_profiles(3)
    unknown_ivs = [(ZERO, u) for u in profiles if u != ZERO]
    rs = subsets(range(3))
    comp_checks = 0
    for a in unknown_ivs:
        for b in unknown_ivs:
            for iv in (imeet(a, b), ijoin(a, b)):
                for r in rs:
                    assert liveness(iv, r) != LIVE
                    comp_checks += 1
    # (ii) scoped bridge: coverage claim about the operator on scope S, warranted by calibration evidence
    delta = Fraction(1, 3)
    cov, k = conformal_coverage_exact(5, delta)
    assert cov == Fraction(k, 6) and cov >= 1 - delta
    cal_ev = frozenset({"cal1", "cal2", "cal3", "cal4", "cal5"})
    claim = {"content": f"coverage ≥ {1 - delta} on S under exchangeability", "iv": cert(cal_ev), "scope": frozenset({"S"}), "channel": "EXPERIMENTATION"}
    assert liveness(claim["iv"], frozenset()) == LIVE and liveness(claim["iv"], {"cal3"}) == DEAD   # revoking a calibration point kills the claim
    # candidates: (score, truth) — truth is known to the fixture's exact checker only
    candidates = [("c1", Fraction(95, 100), True), ("c2", Fraction(90, 100), False), ("c3", Fraction(60, 100), True), ("c4", Fraction(40, 100), False), ("c5", Fraction(99, 100), False)]
    ivs = {name: IUNKNOWN for name, _, _ in candidates}
    assert all(liveness(iv, frozenset()) == UNKNOWN for iv in ivs.values())
    # a candidate becomes LIVE only through an exact-checker certificate: c1 checked ⇒ LIVE; c5 unchecked stays UNKNOWN
    ivs["c1"] = cert({"chk_c1"})
    assert liveness(ivs["c1"], frozenset()) == LIVE and liveness(ivs["c5"], frozenset()) == UNKNOWN
    # the set-valued claim 'truth ∈ C(x)' on S: warrant = bridge ⊗ (candidate set membership is a claim about the operator)
    set_claim = imeet(claim["iv"], cert({"member_x"}))
    assert liveness(set_claim, frozenset()) == LIVE and liveness(set_claim, {"cal1"}) == DEAD
    # (iii) scope: the certificate on S does not transfer to S' ≠ S; on S' the claim's scope is S ∩ S'
    s_prime = frozenset({"S_prime"})
    assert claim["scope"] & s_prime == frozenset()    # nothing covered on S'
    # exact non-exchangeable fixture for S': the test score is always the largest ⇒ coverage 0 < 1−δ
    shifted_total = shifted_cov = 0
    for perm in itertools.permutations(range(6)):
        if perm[-1] == 0:      # S': the test point's score is the maximum
            shifted_total += 1
            shifted_cov += int(perm.index(0) + 1 <= k)
    cov_shift = Fraction(shifted_cov, shifted_total)
    assert cov_shift == 0 < 1 - delta
    # mutants
    tau = Fraction(85, 100)
    mutant_score_as_warrant = {name: (cert({"score_" + name}) if s >= tau else IUNKNOWN) for name, s, _ in candidates}
    live_false = [name for name, _, t in candidates if liveness(mutant_score_as_warrant[name], frozenset()) == LIVE and not t]
    assert live_false == ["c2", "c5"]   # caught: score minted LIVE on false candidates
    honest_live_false = [name for name, _, t in candidates if liveness(ivs[name], frozenset()) == LIVE and not t]
    assert honest_live_false == []
    # certificate transferred across scope: claims coverage ≥ 1−δ on S' — the exact S' coverage refutes it
    mutant_transfer_claim = {"scope": s_prime, "iv": claim["iv"]}
    assert liveness(mutant_transfer_claim["iv"], frozenset()) == LIVE and cov_shift < 1 - delta   # LIVE claim, false content: caught by the scope rule (S ∩ S' = ∅)
    # (iv) certified-only gating: scores never enter the gated matrix (syntactic non-dependence, batch-1 T3 shape)
    atoms = {"s": cert({"e"}), "x": IUNKNOWN, "y": cert({"f"})}
    edges = [edge("sx", "s", "x"), edge("sy", "s", "y")]
    ids, p1 = nav_matrix(atoms, edges, frozenset())
    scores = {"x": Fraction(99, 100), "y": Fraction(1, 100)}
    scores["x"], scores["y"] = scores["y"], scores["x"]   # a score change
    ids2, p2 = nav_matrix(atoms, edges, frozenset())
    assert p1 == p2 and p1[ids.index("s")][ids.index("x")] == 0   # UNKNOWN head is gated out regardless of its score
    return {"all_unknown_composition_checks": comp_checks, "conformal_coverage_n5_delta_1_3": str(cov), "conformal_k": k, "shifted_scope_coverage": str(cov_shift),
            "candidates": len(candidates), "mutant_score_as_warrant_live_false": live_false, "honest_live_false": honest_live_false,
            "mutant_certificate_transferred_caught": 1, "revoking_calibration_kills_claim": 1, "gating_score_independent": 1}


# ---------------------------------------------------------------------------------------------
# D4 · MEG-07 · no-drop guarantee for the surprise functional under fan-out
# ---------------------------------------------------------------------------------------


def backgrounds(atoms, edges, revoked, alpha=ALPHA_NAV):
    """π = uniform-seed fixed point (contract §6); π' = π − α·u (teleport-free / propagated)."""
    ids, p = nav_matrix(atoms, edges, revoked)
    u = uniform_seed(atoms)
    pi = solve_activation(atoms, edges, revoked, u, alpha, matrix=(ids, p))
    pi_prop = {x: pi[x] - alpha * (u[x] if liveness(atoms[x], revoked) == LIVE else 0) for x in ids}
    return pi, pi_prop


def surprising(a, pi):
    """ρ_Q(v) > 0 ⇔ a_Q(v) > 0 and a_Q(v) > π(v)  (exact reading of a·[log((a+ε)/(π+ε))]_+)."""
    return {x: (a[x] > 0 and a[x] > pi[x]) for x in a}


def fanout_fixture(k, fillers):
    atoms = {"r": cert({"er"})}
    edges = []
    for i in range(k):
        atoms[f"c{i}"] = cert({f"ec{i}"})
        edges.append(edge(f"rc{i}", "r", f"c{i}"))
    prev = None
    for j in range(fillers):
        atoms[f"f{j}"] = cert({f"ef{j}"})
        if prev:
            edges.append(edge(f"ff{j}", prev, f"f{j}"))
        prev = f"f{j}"
    return atoms, edges


def check_d4_meg07_surprise_no_drop():
    rng = random.Random(4)
    alpha = ALPHA_NAV
    # (i) exact equivalence and (ii) one-hop lower bound a_Q(v) ≥ α(1−α) Σ_s s_Q(s) P_R(s, v) on random spaces
    one_hop_checks = equivalence_checks = 0
    for _ in range(30):
        atoms, edges = random_space(rng, 6, 9, 3)
        ids, _ = nav_matrix(atoms, edges, frozenset())
        for r in subsets(range(3)):
            idsr, p = nav_matrix(atoms, edges, r)
            seeds = [x for x in ids if liveness(atoms[x], r) == LIVE][:2]
            if not seeds:
                continue
            smap = {x: Fraction(1, len(seeds)) for x in seeds}
            a = solve_activation(atoms, edges, r, smap, alpha, matrix=(idsr, p))
            pi, pi_p = backgrounds(atoms, edges, r, alpha)
            for v in ids:
                lower = alpha * (1 - alpha) * sum((smap.get(s, 0) * p[idsr.index(s)][idsr.index(v)] for s in seeds), Fraction(0))
                assert a[v] >= lower
                one_hop_checks += 1
                assert surprising(a, pi)[v] == (a[v] > 0 and a[v] > pi[v])
                equivalence_checks += 1
    # (iii) matched seed cardinality is a no-op: the average fixed point over all seed sets of size m equals the uniform fixed point
    atoms, edges = random_space(rng, 6, 9, 3)
    ids, p = nav_matrix(atoms, edges, frozenset())
    live_ids = [x for x in ids if liveness(atoms[x], frozenset()) == LIVE]
    pi, pi_p = backgrounds(atoms, edges, frozenset(), alpha)
    noop = 0
    for m in (1, 2, 3):
        sets = list(itertools.combinations(ids, m))
        avg = {x: Fraction(0) for x in ids}
        for S in sets:
            a = solve_activation(atoms, edges, frozenset(), {x: Fraction(1, m) for x in S}, alpha, matrix=(ids, p))
            for x in ids:
                avg[x] += a[x] / len(sets)
        assert avg == pi
        noop += len(sets)
    # (iv) teleport-free background is pointwise ≤ π, hence never drops an atom the uniform background surfaced
    monotone = 0
    for _ in range(30):
        atoms2, edges2 = random_space(rng, 6, 9, 3)
        for r in subsets(range(3)):
            pi, pi_p = backgrounds(atoms2, edges2, r, alpha)
            ids2, p2 = nav_matrix(atoms2, edges2, r)
            seeds = [x for x in ids2 if liveness(atoms2[x], r) == LIVE][:2]
            if not seeds:
                continue
            a = solve_activation(atoms2, edges2, r, {x: Fraction(1, len(seeds)) for x in seeds}, alpha, matrix=(ids2, p2))
            su, sp = surprising(a, pi), surprising(a, pi_p)
            assert all(pi_p[x] <= pi[x] for x in ids2) and all((not su[x]) or sp[x] for x in ids2)
            monotone += 1
    # (v) the M2 fan-out finding reproduced exactly: |V| = 20, fan-out 13, α = 1/3: (1−α)(|V|−1) < k ⇒ the one-hop head is dropped by π and kept by π'
    k, fillers = 13, 6
    atoms3, edges3 = fanout_fixture(k, fillers)
    assert len(atoms3) == 20 and (1 - alpha) * (len(atoms3) - 1) < k
    pi, pi_p = backgrounds(atoms3, edges3, frozenset(), alpha)
    a = solve_activation(atoms3, edges3, frozenset(), {"r": Fraction(1)}, alpha)
    assert a["c0"] == alpha * (1 - alpha) / k and pi["c0"] == alpha / 20 * (1 + (1 - alpha) / k)
    assert not surprising(a, pi)["c0"] and surprising(a, pi_p)["c0"]
    dropped_uniform = sum(1 for i in range(k) if not surprising(a, pi)[f"c{i}"])
    kept_prop = sum(1 for i in range(k) if surprising(a, pi_p)[f"c{i}"])
    # in-share σ = 1/k, |S| = 1: the sufficient condition α(1−α)σ/|S| > π'(v)
    assert alpha * (1 - alpha) * Fraction(1, k) > pi_p["c0"]
    # three-seed variant (M2: 3-seed questions) — still dropped by π, kept by π'
    a3 = solve_activation(atoms3, edges3, frozenset(), {"r": Fraction(1, 3), "f0": Fraction(1, 3), "f3": Fraction(1, 3)}, alpha)
    assert not surprising(a3, pi)["c0"] and surprising(a3, pi_p)["c0"]
    # (vi) KS-T06 / KS-T06b preserved under both backgrounds on the hub witness
    hub_atoms = {"s1": cert({"e"}), "spec": cert({"e"}), "hub": cert({"e"})}
    hub_edges = [edge("s1h", "s1", "hub", w=2), edge("s1p", "s1", "spec", w=1)]
    for i in range(5):
        hub_atoms[f"x{i}"] = cert({"e"})
        hub_edges.append(edge(f"x{i}h", f"x{i}", "hub"))
    pi, pi_p = backgrounds(hub_atoms, hub_edges, frozenset(), alpha)
    aq = solve_activation(hub_atoms, hub_edges, frozenset(), {"s1": Fraction(1)}, alpha)
    assert aq["hub"] > aq["spec"]                                        # hub first by popularity
    for bg in (pi, pi_p):
        s = surprising(aq, bg)
        assert s["spec"] and not s["hub"]                                # specific atom first by surprise
        ah = solve_activation(hub_atoms, hub_edges, frozenset(), {"x0": Fraction(1)}, alpha)
        assert surprising(ah, bg)["hub"] and ah["hub"] == max(v for x, v in ah.items() if x != "x0")   # hub-only query: hub first by both
        a_uni = solve_activation(hub_atoms, hub_edges, frozenset(), uniform_seed(hub_atoms), alpha)
        assert not any(surprising(a_uni, pi).values())                   # KS-T06: a_Q = π ⇒ ρ = 0
    # mutant: a scaled background π/2 (tuned to surface more) breaks KS-T06 — the query-independent seed becomes surprising everywhere
    pi_half = {x: v / 2 for x, v in pi.items()}
    a_uni = solve_activation(hub_atoms, hub_edges, frozenset(), uniform_seed(hub_atoms), alpha)
    assert all(surprising(a_uni, pi_half).values())
    # mutant: 'seed-count-conditioned background' claimed as the fix — it is π itself (no-op), so the fan-out head stays dropped
    pi_matched = {x: Fraction(0) for x in atoms3}
    sets = list(itertools.combinations(list(atoms3), 1))
    for S in sets:
        aS = solve_activation(atoms3, edges3, frozenset(), {x: Fraction(1) for x in S}, alpha)
        for x in atoms3:
            pi_matched[x] += aS[x] / len(sets)
    pi3, _ = backgrounds(atoms3, edges3, frozenset(), alpha)
    assert pi_matched == pi3 and not surprising(a, pi_matched)["c0"]
    return {"one_hop_lower_bound_checks": one_hop_checks, "equivalence_checks": equivalence_checks, "matched_cardinality_noop_seed_sets": noop,
            "teleport_free_monotone_checks": monotone, "fanout_k": k, "space_size": len(atoms3), "fanout_heads_dropped_uniform": dropped_uniform, "fanout_heads_kept_propagated": kept_prop,
            "three_seed_variant": 1, "hub_witness_both_backgrounds": 2, "ks_t06_preserved": 1, "mutant_scaled_background_breaks_t06": 1, "mutant_matched_cardinality_is_noop": 1}


# ---------------------------------------------------------------------------------------------
# D5 · MEG-20 · sufficiency certificate: restricted lumpability ∧ measurability
# ---------------------------------------------------------------------------------------


def block_of(blocks):
    return {x: i for i, B in enumerate(blocks) for x in B}


def reachable_rows(ids, p, seed_ids):
    reached = set(seed_ids)
    grew = True
    while grew:
        grew = False
        for v in list(reached):
            for u in ids:
                if p[ids.index(v)][ids.index(u)] > 0 and u not in reached:
                    reached.add(u)
                    grew = True
    return reached


def lumpable_on(ids, p, blocks, rows):
    """Kemeny–Snell block-row equality restricted to ``rows`` (the seed-reachable subchain)."""
    bo = block_of(blocks)
    for B in blocks:
        members = [v for v in B if v in rows]
        for B2 in blocks:
            masses = {sum((p[ids.index(v)][ids.index(u)] for u in B2), Fraction(0)) for v in members}
            if len(masses) > 1:
                return False
    return True


def measurable(atoms, blocks, gammas):
    return all(len({liveness(atoms[x], r) for x in B}) == 1 for B in blocks for r in gammas)


def quotient_solve(atoms, edges, blocks, seed_map, target, r, alpha=ALPHA_NAV, forced=False):
    """Coarse solve: quotient matrix on blocks (row of any member; averaged when ``forced``),
    block liveness (uniform, or join when ``forced``), pushed-forward seed; returns
    (activation mass of the target block, liveness of the target block)."""
    ids, p = nav_matrix(atoms, edges, r)
    bo = block_of(blocks)
    q = [[Fraction(0)] * len(blocks) for _ in blocks]
    for i, B in enumerate(blocks):
        live_members = [v for v in B if liveness(atoms[v], r) == LIVE]
        members = live_members if forced else list(B)
        if not members:
            continue
        for j, B2 in enumerate(blocks):
            masses = [sum((p[ids.index(v)][ids.index(u)] for u in B2), Fraction(0)) for v in members]
            q[i][j] = sum(masses, Fraction(0)) / len(masses) if forced else masses[0]
    bl = []
    for B in blocks:
        ls = {liveness(atoms[x], r) for x in B}
        bl.append((LIVE if LIVE in ls else (DEAD if ls == {DEAD} else UNKNOWN)) if forced else (next(iter(ls)) if len(ls) == 1 else UNKNOWN))
    seed = [Fraction(0)] * len(blocks)
    for x, s in seed_map.items():
        if liveness(atoms[x], r) == LIVE:
            seed[bo[x]] += s
    for i in range(len(blocks)):
        if bl[i] != LIVE:
            seed[i] = Fraction(0)
            q[i] = [Fraction(0)] * len(blocks)
            for row in q:
                row[i] = Fraction(0)
    a = fixed_point(q, seed, alpha)
    return a[bo[target]], bl[bo[target]]


def fine_solve(atoms, edges, blocks, seed_map, target, r, alpha=ALPHA_NAV):
    a = solve_activation(atoms, edges, r, seed_map, alpha)
    bo = block_of(blocks)
    return sum((a[x] for x in atoms if bo[x] == bo[target]), Fraction(0)), liveness(atoms[target], r)


def sufficiency_certificate(atoms, edges, blocks, Q, gammas, alpha=ALPHA_NAV):
    """SufficiencyCertificate(m, Q) := (κ, Q, proof that Solve(K, q) = Solve(K̄, q) ∀ q ∈ Q, R ∈ Γ);
    issued iff κ is lumpable on the seed-reachable subchain of P_R for every R ∈ Γ and measurable on Γ."""
    if not measurable(atoms, blocks, gammas):
        return "REFINE_REQUIRED:NOT_MEASURABLE"
    for r in gammas:
        ids, p = nav_matrix(atoms, edges, r)
        for seed_map, _ in Q:
            rows = reachable_rows(ids, p, [x for x in seed_map if liveness(atoms[x], r) == LIVE])
            if not lumpable_on(ids, p, blocks, rows):
                return "REFINE_REQUIRED:NOT_LUMPABLE_ON_REACHABLE"
    return "CERTIFIED"


def d5_fixture():
    atoms = {"s": cert({"es"}), "a1": cert({"ea"}), "a2": cert({"ea"}), "b1": cert({"eb"}), "b2": cert({"eb"}), "t": cert({"et"}), "u1": cert({"eu"}), "u2": cert({"eu"})}
    edges = [edge("sa1", "s", "a1"), edge("sa2", "s", "a2"), edge("a1b1", "a1", "b1"), edge("a2b2", "a2", "b2"), edge("b1t", "b1", "t"), edge("b2t", "b2", "t"),
             edge("u1b1", "u1", "b1"), edge("u1u2", "u1", "u2")]   # u-rows are not lumpable (u1 → B mass 1/2, u2 → 0) but unreachable from s
    blocks = [["s"], ["a1", "a2"], ["b1", "b2"], ["t"], ["u1", "u2"]]
    return atoms, edges, blocks


def check_d5_meg20_sufficiency_certificate():
    atoms, edges, blocks = d5_fixture()
    gammas = [frozenset(), frozenset({"ea"}), frozenset({"eb"}), frozenset({"eu"})]
    Q = [({"s": Fraction(1)}, "t"), ({"s": Fraction(1)}, "b1")]
    assert sufficiency_certificate(atoms, edges, blocks, Q, gammas) == "CERTIFIED"
    ids, p = nav_matrix(atoms, edges, frozenset())
    assert not lumpable_on(ids, p, blocks, set(ids))   # the global check fails (u-rows); the restricted certificate is the sufficient one
    agreements = 0
    for r in gammas:
        for seed_map, target in Q:
            assert fine_solve(atoms, edges, blocks, seed_map, target, r) == quotient_solve(atoms, edges, blocks, seed_map, target, r)
            agreements += 1
    # a query outside Q (seeded at u1) is not covered: the certificate says REFINE_REQUIRED and the forced coarse answer is wrong
    Qu = [({"u1": Fraction(1)}, "b1")]
    assert sufficiency_certificate(atoms, edges, blocks, Qu, gammas) == "REFINE_REQUIRED:NOT_LUMPABLE_ON_REACHABLE"
    assert fine_solve(atoms, edges, blocks, {"u1": Fraction(1)}, "b1", frozenset()) != quotient_solve(atoms, edges, blocks, {"u1": Fraction(1)}, "b1", frozenset(), forced=True)
    # mutant: certificate without measurability — a1 gets its own evidence; block {a1, a2} has mixed liveness under {ea1}
    atoms_m = dict(atoms)
    atoms_m["a1"] = cert({"ea1"})
    gammas_m = [frozenset(), frozenset({"ea1"})]
    assert not measurable(atoms_m, blocks, gammas_m) and sufficiency_certificate(atoms_m, edges, blocks, Q, gammas_m) == "REFINE_REQUIRED:NOT_MEASURABLE"

    def mutant_certificate_without_measurability(atoms_, edges_, blocks_, Q_, gammas_):
        for r in gammas_:
            ids_, p_ = nav_matrix(atoms_, edges_, r)
            for seed_map, _ in Q_:
                rows = reachable_rows(ids_, p_, [x for x in seed_map if liveness(atoms_[x], r) == LIVE])
                if not lumpable_on(ids_, p_, blocks_, rows):
                    return "REFINE_REQUIRED"
        return "CERTIFIED"

    assert mutant_certificate_without_measurability(atoms_m, edges, blocks, Q, [frozenset()]) == "CERTIFIED"   # mutation applied (lumpable at ∅)
    fine_a1 = fine_solve(atoms_m, edges, blocks, {"s": Fraction(1)}, "a1", frozenset({"ea1"}))
    coarse_a1 = quotient_solve(atoms_m, edges, blocks, {"s": Fraction(1)}, "a1", frozenset({"ea1"}), forced=True)
    assert fine_a1[1] == DEAD and coarse_a1[1] == LIVE   # caught: the macro answers LIVE for a member that is DEAD after the revocation
    # tightened: measurability alone does not give lumpability under gating — a co-tail witness
    atoms_c = dict(atoms)
    atoms_c["x"] = cert({"ex"})
    edges_c = [e if e[0] != "a1b1" else edge("a1b1", ("a1", "x"), "b1") for e in edges]   # a1's edge needs the co-tail x
    gammas_c = [frozenset(), frozenset({"ex"})]
    blocks_c = blocks + [["x"]]
    assert measurable(atoms_c, blocks_c, gammas_c)
    ids0, p0 = nav_matrix(atoms_c, edges_c, frozenset())
    idsx, px = nav_matrix(atoms_c, edges_c, frozenset({"ex"}))
    rows0 = reachable_rows(ids0, p0, ["s"])
    assert lumpable_on(ids0, p0, blocks_c, rows0) and not lumpable_on(idsx, px, blocks_c, reachable_rows(idsx, px, ["s"]))
    assert sufficiency_certificate(atoms_c, edges_c, blocks_c, Q, gammas_c) == "REFINE_REQUIRED:NOT_LUMPABLE_ON_REACHABLE"
    assert sufficiency_certificate(atoms_c, edges_c, blocks_c, Q, [frozenset()]) == "CERTIFIED"   # per-R check is what refuses it
    # no-alarm: with the certificate, the summary answers every q ∈ Q from the quotient (ANSWERED_FROM_SUMMARY); without it REFINE_REQUIRED
    answers = {"with_certificate": "ANSWERED_FROM_SUMMARY" if sufficiency_certificate(atoms, edges, blocks, Q, gammas) == "CERTIFIED" else "REFINE_REQUIRED",
               "without": "REFINE_REQUIRED"}
    return {"agreements_over_gamma_x_Q": agreements, "global_lumpability_fails_restricted_certifies": 1, "uncovered_query_refine_required": 1,
            "mutant_without_measurability_caught": 1, "cotail_witness_measurable_not_lumpable_under_R": 1, "answers": answers}


# ---------------------------------------------------------------------------------------------
# D6 · MEG-34 · identifiability of a construction inventory up to lifecycle equivalence ≡_L
# ---------------------------------------------------------------------------------------

# aligned pairs over the six-order class: kind 0 = distinct nouns (reveals the order), kind 1 = same lexeme
# as agent and patient (reveals only the verb position); a registered query family of held-out inputs
SIX_INPUTS = ("distinct", "reflexive")
QUERY_FAMILY_SIX = ("distinct", "reflexive")


def vsw_six(examples):
    """examples: list of (input_index, evidence_id) all consistent with the true order (SVO)."""
    truth = SIX_ORDER_CLASS[SIX_ORDERS.index("SVO")]
    S = {j: (examples[j][0], examples[j][1]) for j in range(len(examples))}
    out = {}
    for i in range(len(SIX_INPUTS)):
        agreeing = []
        for J in subsets(list(S)):
            vs = [h for h in SIX_ORDER_CLASS if all(h[S[j][0]] == truth[S[j][0]] for j in J)]
            if vs and len({h[i] for h in vs}) == 1:
                agreeing.append(frozenset(S[j][1] for j in J))
        out[i] = canon(agreeing)
    return out


def behaviour_six(examples):
    truth = SIX_ORDER_CLASS[SIX_ORDERS.index("SVO")]
    vs = [h for h in SIX_ORDER_CLASS if all(h[i] == truth[i] for i, _ in examples)]
    return tuple((next(iter({h[i] for h in vs})) if len({h[i] for h in vs}) == 1 else "AMBIGUOUS") for i in range(len(SIX_INPUTS)))


def reopening_sets(vsw):
    """Per evidence id: the inputs whose per-input warrant dies when that id is revoked."""
    ev = sorted({e for p in vsw.values() for w in p for e in w})
    return {e: frozenset(i for i, p in vsw.items() if live(p, frozenset()) and not live(p, {e})) for e in ev}


def lifecycle_signature(vsw):
    """(behaviour-free) reopening structure up to renaming of evidence ids: the sorted multiset of
    per-input antichains with ids replaced by canonical indices."""
    ev = sorted({e for p in vsw.values() for w in p for e in w})
    best = None
    for perm in itertools.permutations(range(len(ev))):
        ren = {e: perm[k] for k, e in enumerate(ev)}
        sig = tuple(tuple(sorted(tuple(sorted(ren[e] for e in w)) for w in vsw[i])) for i in sorted(vsw))
        best = sig if best is None or sig < best else best
    return best


def ocm_equivalent(ex1, ex2):
    return behaviour_six(ex1) == behaviour_six(ex2) and lifecycle_signature(vsw_six(ex1)) == lifecycle_signature(vsw_six(ex2))


def mutant_behaviour_only_equivalent(ex1, ex2):
    return behaviour_six(ex1) == behaviour_six(ex2)


def check_d6_meg34_inventory_identifiability():
    inv1 = [(0, "d1")]                       # one distinct-noun pair
    inv2 = [(1, "r1"), (0, "d2")]            # a reflexive pair then a distinct pair
    assert behaviour_six(inv1) == behaviour_six(inv2) == (("SVO", 1))
    w1, w2 = vsw_six(inv1), vsw_six(inv2)
    assert w1 == {0: canon([{"d1"}]), 1: canon([{"d1"}])}
    assert w2 == {0: canon([{"d2"}]), 1: canon([{"r1"}, {"d2"}])}
    r1, r2 = reopening_sets(w1), reopening_sets(w2)
    assert r1 == {"d1": frozenset({0, 1})} and r2 == {"d2": frozenset({0}), "r1": frozenset()}
    assert not ocm_equivalent(inv1, inv2) and mutant_behaviour_only_equivalent(inv1, inv2)   # mutant declares equivalent; caught by the lifecycle test
    # no-alarm: renamed evidence ids are ≡_L
    assert ocm_equivalent(inv1, [(0, "d9")]) and ocm_equivalent(inv2, [(1, "rr"), (0, "dd")])
    # STRUCTURAL_NONIDENTIFIABILITY witness lifted: distinct example sets with identical (behaviour, warrant) signatures
    # exhaustive over all example multisets of size ≤ 3 over the two kinds (evidence ids fresh)
    pool = []
    for n in range(1, 4):
        for kinds in itertools.product((0, 1), repeat=n):
            pool.append([(k, f"e{j}") for j, k in enumerate(kinds)])
    classes = {}
    for ex in pool:
        classes.setdefault((behaviour_six(ex), lifecycle_signature(vsw_six(ex))), []).append(ex)
    beh_classes = {}
    for ex in pool:
        beh_classes.setdefault(behaviour_six(ex), []).append(ex)
    nonident_witnesses = sum(1 for v in classes.values() if len(v) > 1)
    assert nonident_witnesses > 0 and len(classes) > len(beh_classes)   # ≡_L strictly refines behavioural equivalence
    # every pair with equal behaviour but different reopening structure is separated by the lifecycle test
    separated = sum(1 for a, b in itertools.combinations(pool, 2) if behaviour_six(a) == behaviour_six(b) and lifecycle_signature(vsw_six(a)) != lifecycle_signature(vsw_six(b)) and not ocm_equivalent(a, b))
    conflated_by_mutant = sum(1 for a, b in itertools.combinations(pool, 2) if behaviour_six(a) == behaviour_six(b) and lifecycle_signature(vsw_six(a)) != lifecycle_signature(vsw_six(b)) and mutant_behaviour_only_equivalent(a, b))
    assert separated == conflated_by_mutant > 0
    # which aligned-pair distributions identify the inventory: q = P(distinct) > 0 identifies the behaviour a.s. (E = 1/q pairs);
    # q = 0 leaves the version space at {SVO, OVS} forever (AMBIGUOUS on distinct inputs); the lifecycle class of the learned
    # inventory is sample-dependent (inv1 vs inv2 are both reachable under any 0 < q < 1)
    ident = {}
    for q in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)):
        p_by_n = [1 - (1 - q) ** n for n in range(0, 7)]
        ident[str(q)] = {"expected_pairs": None if q == 0 else str(1 / q), "p_identified_by_n": [str(x) for x in p_by_n]}
    assert behaviour_six([(1, "r1"), (1, "r2")]) == ("AMBIGUOUS", 1)
    # both lifecycle classes reachable under q = 1/2: P(first pair distinct) = 1/2 → inv1's class; P(reflexive then distinct) = 1/4 → inv2's class
    return {"behaviour_equal_lifecycle_different": 1, "reopen_inv1": {k: sorted(v) for k, v in r1.items()}, "reopen_inv2": {k: sorted(v) for k, v in r2.items()},
            "mutant_behaviour_only_caught": 1, "renamed_ids_equivalent": 2, "example_sets": len(pool), "lifecycle_classes": len(classes), "behaviour_classes": len(beh_classes),
            "nonidentifiability_witness_classes": nonident_witnesses, "pairs_separated_by_lifecycle_test": separated, "pairs_conflated_by_mutant": conflated_by_mutant,
            "identification_by_distinct_prob": ident, "reflexive_only_ambiguous": 1}


# ---------------------------------------------------------------------------------------------
# D7 · MEG-09 · multiscale navigation coherence on a two-level fixture
# ---------------------------------------------------------------------------------------

FOUND, GAP, OBSTRUCTION, REFINE_REQUIRED = "FOUND", "GAP", "OBSTRUCTION_WITNESSED", "REFINE_REQUIRED"
THETA = Fraction(1, 50)


def coarse_graph(atoms, edges, blocks, min_cross=1):
    """Registered coarse structure: a cell edge per pair of cells with ≥ min_cross crossing fine edges."""
    bo = block_of(blocks)
    cross = {}
    for _, tails, heads, *_ in edges:
        for t in tails:
            for h in heads:
                if bo[t] != bo[h]:
                    cross[(bo[t], bo[h])] = cross.get((bo[t], bo[h]), 0) + 1
    catoms = {f"B{i}": cert({f"cell{i}"}) for i in range(len(blocks))}
    cedges = [edge(f"B{i}B{j}", f"B{i}", f"B{j}", w=n) for (i, j), n in sorted(cross.items()) if n >= min_cross]
    return catoms, cedges


def level_outcome(atoms, edges, seed_ids, target, r, alpha=ALPHA_NAV):
    if target not in reach_ungated(seed_ids, edges):
        return OBSTRUCTION
    a = solve_activation(atoms, edges, r, {s: Fraction(1, len(seed_ids)) for s in seed_ids}, alpha)
    if liveness(atoms[target], r) == LIVE and a[target] >= THETA:
        return FOUND
    return GAP


def multiscale_solve(atoms, edges, blocks, seed, target, r, min_cross=1):
    """Coarse walk over cells; descend on REFINE_REQUIRED; OBSTRUCTION only if the ceiling walker fails at every level."""
    bo = block_of(blocks)
    catoms, cedges = coarse_graph(atoms, edges, blocks, min_cross)
    coarse = level_outcome(catoms, cedges, [f"B{bo[seed]}"], f"B{bo[target]}", frozenset())
    fine = level_outcome(atoms, edges, [seed], target, r)
    if coarse == FOUND:
        return fine, coarse, "DESCEND_WITH_CERTIFICATE"
    if coarse == GAP:
        return fine, coarse, REFINE_REQUIRED
    # coarse OBSTRUCTION: final only if the fine ceiling walker also fails
    return (OBSTRUCTION if fine == OBSTRUCTION else fine), coarse, "CEILING_CHECKED_AT_FINE_LEVEL"


def mutant_coarse_obstruction_is_final(atoms, edges, blocks, seed, target, r, min_cross=1):
    bo = block_of(blocks)
    catoms, cedges = coarse_graph(atoms, edges, blocks, min_cross)
    coarse = level_outcome(catoms, cedges, [f"B{bo[seed]}"], f"B{bo[target]}", frozenset())
    if coarse in (GAP, OBSTRUCTION):
        return OBSTRUCTION
    return level_outcome(atoms, edges, [seed], target, r)


def pushforward(a, blocks):
    bo = block_of(blocks)
    out = [Fraction(0)] * len(blocks)
    for x, v in a.items():
        out[bo[x]] += v
    return out


def quotient_fixed_point(atoms, edges, blocks, seed_map, r, alpha=ALPHA_NAV):
    ids, p = nav_matrix(atoms, edges, r)
    bo = block_of(blocks)
    q = [[Fraction(0)] * len(blocks) for _ in blocks]
    bl = []
    for i, B in enumerate(blocks):
        ls = {liveness(atoms[x], r) for x in B}
        bl.append(next(iter(ls)) if len(ls) == 1 else "MIXED")
        members = [v for v in B if liveness(atoms[v], r) == LIVE] or list(B)
        for j, B2 in enumerate(blocks):
            masses = [sum((p[ids.index(v)][ids.index(u)] for u in B2), Fraction(0)) for v in members]
            q[i][j] = sum(masses, Fraction(0)) / len(masses)      # forced reading: row average (the KS-T07 mutant when not lumpable)
    seed = [Fraction(0)] * len(blocks)
    for x, s in seed_map.items():
        if liveness(atoms[x], r) == LIVE:
            seed[bo[x]] += s
    for i in range(len(blocks)):
        if bl[i] == DEAD:
            q[i] = [Fraction(0)] * len(blocks)
            for row in q:
                row[i] = Fraction(0)
    return fixed_point(q, seed, alpha), bl


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p


def check_d7_meg09_multiscale_coherence():
    rng = random.Random(9)
    # two-level fixture: cells A = {a1,a2,a3}, B = {b1,b2}, C = {c1}; one revocation inside A
    atoms = {"a1": cert({"ea1"}), "a2": cert({"ea2"}), "a3": cert({"ea3"}), "b1": cert({"eb"}), "b2": cert({"eb"}), "c1": cert({"ec"})}
    edges = [edge("a1a2", "a1", "a2"), edge("a1a3", "a1", "a3"), edge("a2b1", "a2", "b1"), edge("a3b2", "a3", "b2"), edge("b1b2", "b1", "b2"), edge("b2c1", "b2", "c1"), edge("a3c1", "a3", "c1")]
    blocks = [["a1", "a2", "a3"], ["b1", "b2"], ["c1"]]
    gammas = [frozenset(), frozenset({"ea2"}), frozenset({"ea3"}), frozenset({"eb"})]
    # (i) coherence: the honest coarse graph over-approximates fine reachability, so a coarse OBSTRUCTION is sound; a coarse GAP is REFINE_REQUIRED
    outcomes = {}
    for r in gammas:
        for target in ("b1", "b2", "c1"):
            res = multiscale_solve(atoms, edges, blocks, "a1", target, r)
            outcomes[f"{target}|{sorted(r)}"] = res
            fine = level_outcome(atoms, edges, ["a1"], target, r)
            assert res[0] == fine                                      # the multiscale answer is the fine answer
            assert res[1] != OBSTRUCTION or fine == OBSTRUCTION        # coarse OBSTRUCTION ⇒ fine OBSTRUCTION (sound ceiling)
    # a pruned coarse graph (learned/thresholded cells) can fail its ceiling while the fine walker succeeds: OBSTRUCTION only after the fine check
    res = multiscale_solve(atoms, edges, blocks, "a1", "c1", frozenset(), min_cross=2)
    assert res[1] == OBSTRUCTION and res[0] == FOUND and res[2] == "CEILING_CHECKED_AT_FINE_LEVEL"
    assert mutant_coarse_obstruction_is_final(atoms, edges, blocks, "a1", "c1", frozenset(), min_cross=2) == OBSTRUCTION   # caught: fine FOUND declared obstructed
    # coarse GAP → REFINE_REQUIRED never OBSTRUCTION: raise θ on the coarse level by a long cell chain
    chain_atoms = {f"n{i}": cert({"en"}) for i in range(12)}
    chain_edges = [edge(f"n{i}", f"n{i}", f"n{i+1}") for i in range(11)]
    chain_blocks = [[f"n{i}"] for i in range(12)]
    res = multiscale_solve(chain_atoms, chain_edges, chain_blocks, "n0", "n11", frozenset())
    assert res[1] == GAP and res[2] == REFINE_REQUIRED and res[0] != OBSTRUCTION
    assert mutant_coarse_obstruction_is_final(chain_atoms, chain_edges, chain_blocks, "n0", "n11", frozenset()) == OBSTRUCTION
    # (ii) cross-level prune–solve commutation κ_*(a*_{K,R}) = a*_{q(K),R}: exhaustive over partitions of a 5-atom space × Γ × singleton seeds
    space_atoms = {"p": cert({"e1"}), "q": cert({"e2"}), "r": cert({"e2"}), "s": cert({"e3"}), "t": cert({"e3"})}
    space_edges = [edge("pq", "p", "q"), edge("pr", "p", "r"), edge("qs", "q", "s"), edge("rs", "r", "s"), edge("st", "s", "t"), edge("tp", "t", "p")]
    gam = [frozenset(), frozenset({"e1"}), frozenset({"e2"}), frozenset({"e3"})]
    ids = list(space_atoms)
    partitions = list(set_partitions(ids))
    admissible = commute_all = 0
    adm_and_commute = nonadm_commute = 0
    for blocks_ in partitions:
        adm = measurable(space_atoms, blocks_, gam) and all(lumpable_on(*nav_matrix(space_atoms, space_edges, r_), blocks_, set(ids)) for r_ in gam)
        commutes = True
        for r_ in gam:
            for seed in ids:
                fine_a = solve_activation(space_atoms, space_edges, r_, {seed: Fraction(1)})
                coarse_a, _ = quotient_fixed_point(space_atoms, space_edges, blocks_, {seed: Fraction(1)}, r_)
                if pushforward(fine_a, blocks_) != coarse_a:
                    commutes = False
        admissible += adm
        commute_all += commutes
        if adm:
            assert commutes
            adm_and_commute += 1
        elif commutes:
            nonadm_commute += 1
    assert admissible == adm_and_commute and admissible >= 2    # admissible ⇒ commutes (the discrete partition and {q, r} included)
    qr_blocks = [["p"], ["q", "r"], ["s"], ["t"]]
    assert measurable(space_atoms, qr_blocks, gam) and all(lumpable_on(*nav_matrix(space_atoms, space_edges, r_), qr_blocks, set(ids)) for r_ in gam)
    # (iii) the fixture's own partition: commutation holds for R inside cell A only when A's members are measurable — one revocation inside A breaks it
    fix_ok = all(pushforward(solve_activation(atoms, edges, r_, {"a1": Fraction(1)}), blocks) == quotient_fixed_point(atoms, edges, blocks, {"a1": Fraction(1)}, r_)[0] for r_ in [frozenset()])
    fix_break = pushforward(solve_activation(atoms, edges, frozenset({"ea2"}), {"a1": Fraction(1)}), blocks) != quotient_fixed_point(atoms, edges, blocks, {"a1": Fraction(1)}, frozenset({"ea2"}))[0]
    assert not measurable(atoms, blocks, [frozenset({"ea2"})])
    return {"fixture_outcomes": {k: list(v) for k, v in outcomes.items()}, "pruned_coarse_ceiling_checked_at_fine": 1, "mutant_coarse_obstruction_final_caught": 2,
            "coarse_gap_refine_required": 1, "partitions": len(partitions), "admissible_partitions": admissible, "commuting_partitions": commute_all,
            "admissible_all_commute": adm_and_commute, "nonadmissible_but_commuting": nonadm_commute, "fixture_commutes_at_empty": int(fix_ok), "fixture_breaks_under_inner_revocation": int(fix_break)}


# ---------------------------------------------------------------------------------------------
# D8 · MEG-23 · organisation search admissibility (Org = fibres, exports, transports, router)
# ---------------------------------------------------------------------------------------

CONSTITUTION = {"Check": "exact_checker_v1", "Authority": "meet_lattice_v1", "Meter": "resource_vector_v1", "Commit": "external_receipt_v1"}
CONSTITUTION_DIGEST = digest(CONSTITUTION)


def make_org(atoms, auth, edges, fibres, exports, transports, router, constitution=CONSTITUTION):
    return {"atoms": dict(atoms), "auth": dict(auth), "edges": list(edges), "fibres": [list(f) for f in fibres], "exports": dict(exports), "transports": dict(transports), "router": dict(router), "constitution": dict(constitution)}


def export_ok(org, name):
    """KS-T20/T23: export m = (constituents, corr, operator authority) with Λ(m) = Λ_corr ⊗ ⊗Λ(x),
    authority = A_op ∧ ⋀ A(x) (operator factor present, batch-1 T1), constituents inside one fibre."""
    m = org["exports"][name]
    want = meet_all([m["corr"], *(org["atoms"][x][0] for x in m["constituents"])])
    want_auth = auth_meet(m["op_auth"], *(org["auth"][x] for x in m["constituents"]))
    return m["iv"][0] == want and m["auth"] == want_auth and any(set(m["constituents"]) <= set(f) for f in org["fibres"])


def transport_ok(org, name):
    t = org["transports"][name]
    if t["source_export"] not in org["exports"]:
        return False          # dangling: the export the transport uses is gone (not a DPO match)
    src = org["exports"][t["source_export"]]
    return t["iv"][0] == meet(t["map_iv"][0], src["iv"][0]) and t["auth"] == auth_meet(t["map_auth"], src["auth"]) and any(t["target"] in f for f in org["fibres"])


def fibre_rows_ok(org, i, gammas):
    """The fibre partition as a quotient, checked on fibre i's rows: measurable on Γ and lumpable
    (block-row equality for its members) under every gated matrix P_R (the D5 certificate shape)."""
    blocks = org["fibres"]
    if not measurable(org["atoms"], [blocks[i]], gammas):
        return False
    for r in gammas:
        ids, p = nav_matrix(org["atoms"], org["edges"], r)
        if not lumpable_on(ids, p, blocks, set(blocks[i])):
            return False
    return True


def adm(org, gammas):
    if digest(org["constitution"]) != CONSTITUTION_DIGEST:
        return "REFUSED:CONSTITUTION_TOUCHED"
    flat = [x for f in org["fibres"] for x in f]
    if sorted(flat) != sorted(org["atoms"]) or len(set(flat)) != len(flat):
        return "REFUSED:NOT_A_PARTITION"
    for i in range(len(org["fibres"])):
        if not fibre_rows_ok(org, i, gammas):
            return "REFUSED:FIBRE_NOT_ADMISSIBLE"
    for name in org["exports"]:
        if not export_ok(org, name):
            return "REFUSED:EXPORT_MINTS_WARRANT_OR_AUTHORITY"
    for name in org["transports"]:
        if not transport_ok(org, name):
            return "REFUSED:TRANSPORT_DANGLING_OR_MINTS"
    if any(w < 0 for w in org["router"].values()):
        return "REFUSED:ROUTER"
    return "ADMISSIBLE"


def d8_fixture():
    atoms = {"p1": cert({"e1"}), "p2": cert({"e1"}), "x1": cert({"e1"}), "q1": cert({"e3"}), "q2": cert({"e3"}), "r1": cert({"e4"})}
    auth = {x: {"world_truth": 1} for x in atoms}
    edges = [edge("p1p2", "p1", "p2"), edge("p2x1", "p2", "x1"), edge("x1p1", "x1", "p1"), edge("q1q2", "q1", "q2"), edge("q2q1", "q2", "q1"), edge("r1r1", "r1", "r1")]
    fibres = [["p1", "p2", "x1"], ["q1", "q2"], ["r1"]]
    corr = cert({"corr"})[0]
    m_iv = (meet_all([corr, atoms["p1"][0], atoms["p2"][0]]), meet_all([corr, atoms["p1"][1], atoms["p2"][1]]))
    exports = {"m1": {"constituents": ["p1", "p2"], "corr": corr, "op_auth": {"world_truth": 1}, "iv": m_iv, "auth": {"world_truth": 1}}}
    t_iv = (meet(cert({"tmap"})[0], m_iv[0]), meet(cert({"tmap"})[1], m_iv[1]))
    transports = {"T1": {"source_export": "m1", "target": "q1", "map_iv": cert({"tmap"}), "map_auth": {"world_truth": 1}, "iv": t_iv, "auth": {"world_truth": 1}}}
    return make_org(atoms, auth, edges, fibres, exports, transports, {"F0": 1, "F1": 1, "F2": 1})


def rewrite(org, fibres=None, transports=None, exports=None, constitution=None):
    """A DPO-style rewrite: the interface (exports, transports, constitution) is carried verbatim unless
    the move names it; only the fibre partition (and the router, re-indexed) changes."""
    new = dict(org)
    if fibres is not None:
        new["fibres"] = [list(f) for f in fibres]
        new["router"] = {f"F{i}": 1 for i in range(len(new["fibres"]))}
    if transports is not None:
        new["transports"] = transports
    if exports is not None:
        new["exports"] = exports
    if constitution is not None:
        new["constitution"] = constitution
    return new


def dpo_split(org, fibre_index, part_a):
    f = org["fibres"][fibre_index]
    a, b = [x for x in f if x in part_a], [x for x in f if x not in part_a]
    if not a or not b:
        return None
    return rewrite(org, fibres=[ff for i, ff in enumerate(org["fibres"]) if i != fibre_index] + [a, b])


def dpo_merge(org, i, j):
    return rewrite(org, fibres=[ff for k, ff in enumerate(org["fibres"]) if k not in (i, j)] + [org["fibres"][i] + org["fibres"][j]])


def relink(org, transport, new_target, raise_authority=False):
    t = dict(org["transports"][transport])
    t["target"] = new_target
    if raise_authority:
        t["auth"] = {"world_truth": 2, "commit": 1}
    return rewrite(org, transports={**org["transports"], transport: t})


def affected_fibres(org, new):
    """Fibres that must re-certify: the rewritten ones and every fibre with an edge into a rewritten atom."""
    rewritten = [i for i, f in enumerate(new["fibres"]) if f not in org["fibres"]]
    ratoms = {x for i in rewritten for x in new["fibres"][i]}
    out = set(rewritten)
    for i, f in enumerate(new["fibres"]):
        if any(t in f and any(h in ratoms for h in heads) for _, tails, heads, *_ in new["edges"] for t in tails):
            out.add(i)
    return out, rewritten


def pareto_dominates(u, v):
    """Every coordinate at least as good (higher accuracy/transfer, lower cost) and one strictly."""
    better = [(u[0] >= v[0]), (u[1] <= v[1]), (u[2] >= v[2])]
    strict = [(u[0] > v[0]), (u[1] < v[1]), (u[2] > v[2])]
    return all(better) and any(strict)


def pareto_compare(u, v):
    if pareto_dominates(u, v):
        return "FIRST"
    if pareto_dominates(v, u):
        return "SECOND"
    return "INCOMPARABLE"


def mutant_scalar_objective(u, v, weights):
    su = weights[0] * u[0] - weights[1] * u[1] + weights[2] * u[2]
    sv = weights[0] * v[0] - weights[1] * v[1] + weights[2] * v[2]
    return "FIRST" if su > sv else ("SECOND" if sv > su else "TIE")


def check_d8_meg23_organisation_admissibility():
    org = d8_fixture()
    gammas = [frozenset(), frozenset({"e1"})]
    assert adm(org, gammas) == "ADMISSIBLE"
    # closure under split/merge/relink: exhaustive over the fixture's moves —
    # global Adm(Org') ⇔ interface carried verbatim ∧ affected fibres re-certify ∧ exports/transports lawful ∧ 𝔠 untouched
    moves = []
    for i, f in enumerate(org["fibres"]):
        for k in range(1, len(f)):
            for part in itertools.combinations(f, k):
                new = dpo_split(org, i, set(part))
                if new is not None:
                    moves.append(("split", new))
    for i, j in itertools.combinations(range(len(org["fibres"])), 2):
        moves.append(("merge", dpo_merge(org, i, j)))
    for target in org["atoms"]:
        moves.append(("relink", relink(org, "T1", target)))
    verdicts = {"split": {}, "merge": {}, "relink": {}}
    local_equals_global = unaffected_kept = 0
    for kind, new in moves:
        v = adm(new, gammas)
        verdicts[kind][v] = verdicts[kind].get(v, 0) + 1
        affected, rewritten = affected_fibres(org, new)
        interface_kept = new["exports"] == org["exports"] and new["constitution"] == org["constitution"] and all(new["transports"][t]["auth"] == org["transports"][t]["auth"] and new["transports"][t]["iv"] == org["transports"][t]["iv"] for t in org["transports"])
        local = interface_kept and all(fibre_rows_ok(new, i, gammas) for i in affected) and all(export_ok(new, m) for m in new["exports"]) and all(transport_ok(new, t) for t in new["transports"])
        for i, f in enumerate(new["fibres"]):
            if i not in affected:
                assert fibre_rows_ok(new, i, gammas) == fibre_rows_ok(org, org["fibres"].index(f), gammas) is True   # locality: certificates of unaffected fibres persist
                unaffected_kept += 1
        assert (v == "ADMISSIBLE") == local, (kind, v, local)
        local_equals_global += 1
    assert verdicts["split"].get("ADMISSIBLE", 0) > 0 and verdicts["merge"].get("ADMISSIBLE", 0) > 0 and verdicts["relink"].get("ADMISSIBLE", 0) > 0
    assert verdicts["split"].get("REFUSED:FIBRE_NOT_ADMISSIBLE", 0) > 0 and verdicts["merge"].get("REFUSED:FIBRE_NOT_ADMISSIBLE", 0) > 0
    # mutants
    bad = relink(org, "T1", "r1", raise_authority=True)
    assert bad["transports"]["T1"]["auth"] != org["transports"]["T1"]["auth"] and adm(bad, gammas) == "REFUSED:TRANSPORT_DANGLING_OR_MINTS"
    touched = rewrite(org, constitution=dict(CONSTITUTION, Commit="self_commit"))
    assert adm(touched, gammas) == "REFUSED:CONSTITUTION_TOUCHED"
    minted = rewrite(org, exports={"m1": dict(org["exports"]["m1"], iv=ijoin(org["atoms"]["p1"], org["atoms"]["p2"]))})   # ⊕ over constituents (KS-T23 mutant)
    assert adm(minted, gammas) == "REFUSED:EXPORT_MINTS_WARRANT_OR_AUTHORITY"
    dangling = rewrite(org, exports={})       # removing the export a transport uses: no DPO match (dangling condition)
    assert adm(dangling, gammas) == "REFUSED:TRANSPORT_DANGLING_OR_MINTS"
    # the evaluation object is a Pareto vector: two organisations incomparable under dominance are ordered by every scalarisation, and the order flips with the weights
    u, v = (Fraction(9, 10), Fraction(3), Fraction(2)), (Fraction(8, 10), Fraction(1), Fraction(1))   # (accuracy, cost, transfer)
    assert pareto_compare(u, v) == "INCOMPARABLE"
    s1, s2 = mutant_scalar_objective(u, v, (20, 1, 1)), mutant_scalar_objective(u, v, (1, 1, 0))
    assert s1 == "FIRST" and s2 == "SECOND"
    dom = (Fraction(9, 10), Fraction(1), Fraction(2))
    assert pareto_compare(dom, v) == "FIRST" and pareto_compare(v, dom) == "SECOND"
    # a router update is feedback (batch-1 T3): liveness signatures unchanged under any re-weighting; a negative weight is refused
    org_r = dict(org)
    org_r["router"] = {"F0": 5, "F1": 0, "F2": 1}
    sig = lambda o: {x: tuple(liveness(o["atoms"][x], r) for r in gammas) for x in o["atoms"]}
    assert sig(org_r) == sig(org) and adm(org_r, gammas) == "ADMISSIBLE"
    return {"moves": len(moves), "verdicts": verdicts, "local_predicate_equals_global": local_equals_global, "unaffected_fibre_certificates_kept": unaffected_kept,
            "mutant_relink_raises_authority_caught": 1, "mutant_constitution_touched_refused": 1, "mutant_export_join_refused": 1, "dangling_transport_refused": 1,
            "pareto_incomparable_scalar_orders_flip": 1, "router_reweight_is_feedback": 1}


# ---------------------------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------------------------

CHECKS = {
    "D1_MEG32_equivalence_rules": check_d1_meg32_equivalence_rules,
    "D2_MEG14_channel_bounds": check_d2_meg14_channel_bounds,
    "D3_MEG02_graded_operator_warrant": check_d3_meg02_graded_operator_warrant,
    "D4_MEG07_surprise_no_drop": check_d4_meg07_surprise_no_drop,
    "D5_MEG20_sufficiency_certificate": check_d5_meg20_sufficiency_certificate,
    "D6_MEG34_inventory_identifiability": check_d6_meg34_inventory_identifiability,
    "D7_MEG09_multiscale_coherence": check_d7_meg09_multiscale_coherence,
    "D8_MEG23_organisation_admissibility": check_d8_meg23_organisation_admissibility,
}


def run_all():
    out = {name: fn() for name, fn in CHECKS.items()}
    out["NOVELTY"] = "NOT_ESTABLISHED"
    out["status"] = "ALL_HOLD"
    return out


def main(argv=None):
    try:
        out = run_all()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except AssertionError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
