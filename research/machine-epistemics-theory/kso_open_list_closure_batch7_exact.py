"""Exact finite checker for KSO_OPEN_LIST_CLOSURE_THEOREMS_BATCH7_V1.md (stdlib only, exact).

One check function per open-list item (G1–G9).  Every check performs (a) the positive statement by
exhaustive enumeration of a finite fixture, (b) at least one planted hostile whose mutation is asserted
applied and which must be caught, and (c) a no-alarm control.  Items whose honest status is an exact
impossibility or PARENT_OWNED report the falsifier search they ran and the smallest holding / failing
fixture.  The minimal objects of the OCM core are re-implemented here (antichain semiring, warrant
intervals, Kleene liveness, the restart walk of `ocm.kso.navigation`, the batch-5/6 Boolean towers,
the batch-5 B7 chain); nothing is imported from ``ocm``.  Every probability, size and power is an
exact ``Fraction``; the only float is the ranking value a·ln(a/π), and every ranking decision it
supports is also asserted by exact dominance.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


# ---------------------------------------------------------------------------------------------
# antichain semiring (KS-T01), intervals, Kleene liveness (KS-T21) — as in batches 1–6
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


def live(p, r):
    r = frozenset(r)
    return any(not (w & r) for w in p)


LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


def liveness(iv, r):
    lo, up = iv
    if live(lo, r):
        return LIVE
    if not live(up, r):
        return DEAD
    return UNKNOWN


def cert(*warrants):
    p = canon(frozenset(w) for w in warrants)
    return (p, p)


def subsets(universe, max_size=None):
    u = sorted(universe, key=repr)
    top = len(u) if max_size is None else max_size
    return [frozenset(c) for k in range(top + 1) for c in itertools.combinations(u, k)]


ALPHA = Fraction(1, 20)


def binom_pmf(n, k, p):
    return Fraction(math.comb(n, k)) * p ** k * (1 - p) ** (n - k)


def binom_tail(n, k, p):
    """P(Bin(n, p) ≥ k), exact."""
    return sum((binom_pmf(n, j, p) for j in range(k, n + 1)), Fraction(0))


def popcount(x):
    return bin(x).count("1")


# ---------------------------------------------------------------------------------------------
# G1 · MEG-28 · ceilings beyond the 3-input tower: depth-4 tower exact; J4 reformulation relative to a
#      registered class; J5 tool invention has no uniform ceiling (witness) — decidable per registered class
# ---------------------------------------------------------------------------------------------


ZERO_MASK = {n: [sum(1 << p for p in range(1 << n) if not p & (1 << i)) for i in range(n)] for n in (2, 3, 4)}
POP16 = [popcount(i) for i in range(16)]
_ANF, _DEG = {}, {}


def anf_int(table, n):
    """Möbius transform on a packed truth table (bit p = f(point p), point bits = variables): bit S = coefficient of monomial S."""
    key = (table, n)
    if key not in _ANF:
        t = table
        for i in range(n):
            t ^= (t & ZERO_MASK[n][i]) << (1 << i)
        _ANF[key] = t
    return _ANF[key]


def degree_int(table, n):
    key = (table, n)
    if key not in _DEG:
        a = anf_int(table, n)
        _DEG[key] = max((POP16[S] for S in range(1 << n) if a >> S & 1), default=0)
    return _DEG[key]


def witness_check_int(table, S, n):
    """Independent witness check (no Möbius): the parity of f over the sub-cube {x : x ⊆ S} is odd."""
    return sum(table >> p & 1 for p in range(1 << n) if p & ~S == 0) % 2 == 1


def ceiling_certificate_int(table, level, n, degree_fn=None, with_witness=False):
    """C_ℓ(q): q ∉ S_ℓ with a checkable witness (a monomial of degree > ℓ with odd sub-cube parity); the witness list is materialised on request."""
    deg = (degree_fn or (lambda t: degree_int(t, n)))(table)
    if deg <= level:
        return {"status": "LOWER_LEVEL_SUFFICIENT", "level": level, "has_witness": False}
    c = {"status": "CEILING", "level": level, "has_witness": True}
    if with_witness:
        a = anf_int(table, n)
        c["witness"] = [S for S in range(1 << n) if a >> S & 1 and POP16[S] > level]
    return c


def minimum_level_int(table, n, oracles=None, degree_fn=None):
    for level in range(1, n + 1):
        if oracles and oracles.get(level) == "CANNOT_CHECK":
            return "CANNOT_CHECK"
        if ceiling_certificate_int(table, level, n, degree_fn)["status"] == "LOWER_LEVEL_SUFFICIENT":
            return level
    return None


def assess_jump_int(table, incumbent, proposal, trigger, n, degree_fn=None):
    """Governed Jump assessment on a nested tower (batch-6 F7 shape, any depth)."""
    if trigger.get("kind") not in {"EXPRESSIVE_CEILING"} or not trigger.get("witness_ids"):
        return "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"
    if proposal <= incumbent:
        return "NOT_A_JUMP"
    for level in range(incumbent, proposal):
        c = ceiling_certificate_int(table, level, n, degree_fn)
        if c["status"] != "CEILING" or not c["has_witness"]:
            return "NO_JUMP_NEEDED_LOWER_LEVEL_SUFFICIENT"
    if ceiling_certificate_int(table, proposal, n, degree_fn)["status"] == "CEILING":
        return "PROPOSED_LEVEL_INSUFFICIENT"
    return "CANDIDATE_FOR_PROTECTED_EVALUATION"


def trigger_from_chain_int(table, incumbent, n, degree_fn=None):
    c = ceiling_certificate_int(table, incumbent, n, degree_fn, with_witness=True)
    if c["status"] != "CEILING":
        return {"kind": None, "witness_ids": []}
    return {"kind": "EXPRESSIVE_CEILING", "witness_ids": [str(w) for w in c["witness"]]}


def mutant_partial_level3_degree(table):
    """Planted: a level-3 enumerator that never forms the cubic monomial {y, z, w} (S = 0b1110) — reads the target as degree 4."""
    a = anf_int(table, 4)
    d = degree_int(table, 4)
    if d == 3 and a >> 0b1110 & 1:
        return 4
    return d


def mutant_poor_score_trigger():
    return {"kind": "POOR_SCORE", "witness_ids": ["score"]}


def gf2_affine_maps(n=3):
    """Every invertible affine map x ↦ Ax + b on GF(2)^n as a point permutation (list indexed by point)."""
    maps = []
    for rows in itertools.product(range(1 << n), repeat=n):
        img = [sum(((popcount(rows[i] & x) & 1) << i) for i in range(n)) for x in range(1 << n)]
        if len(set(img)) != 1 << n:
            continue
        for b in range(1 << n):
            maps.append(tuple(y ^ b for y in img))
    return maps


def compose_table(table, perm, n):
    """(q ∘ φ)(p) = q(φ(p))."""
    return sum((table >> perm[p] & 1) << p for p in range(1 << n))


def reformulation_level(space, maps, n):
    """S^Φ := {q ∘ φ : q ∈ S, φ ∈ Φ} — the J4 (problem reformulation) level over a registered class Φ."""
    return frozenset(compose_table(q, phi, n) for q in space for phi in maps)


def span_int(tables, n):
    out = set()
    for coeffs in itertools.product((0, 1), repeat=len(tables)):
        v = 0
        for c, t in zip(coeffs, tables):
            if c:
                v ^= t
        out.add(v)
    return frozenset(out)


def mutant_uniform_reformulation_ceiling(table, registry_level_space):
    """Planted: a J4 ceiling read off the degree alone, ignoring the registered reformulation class."""
    return "CEILING" if degree_int(table, 3) > 1 else "LOWER_LEVEL_SUFFICIENT"


def mutant_unregistered_tool(table, affine_basis, tool_class):
    """Planted: 'a tool exists' certified with the tool t = q itself, which is not in the registered class."""
    return {"status": "LOWER_LEVEL_SUFFICIENT", "tool": table, "registered": table in tool_class}


def check_g1_ceilings_beyond_three_inputs():
    n = 4
    all4 = range(1 << 16)
    sizes = {1: 0, 2: 0, 3: 0, 4: 0}
    min_level_eq_degree = witness_checks = admissible_iff = skip_refused = insufficient_refused = 0
    poor_score_refused = partial3_caught = cannot_check_cases = 0
    degrees = {}
    for t in all4:
        d = degree_int(t, n)
        degrees[t] = d
        for lv in (1, 2, 3, 4):
            if d <= lv:
                sizes[lv] += 1
        m = minimum_level_int(t, n)
        assert m == max(1, d)
        min_level_eq_degree += 1
        if d >= 2:
            c = ceiling_certificate_int(t, d - 1, n, with_witness=True)
            assert c["status"] == "CEILING" and c["witness"] and all(POP16[S] == d for S in c["witness"])
            assert witness_check_int(t, c["witness"][0], n)                                  # independent sub-cube parity
            witness_checks += 1
        for incumbent in (1, 2, 3):
            for proposal in range(incumbent + 1, 5):
                verdict = assess_jump_int(t, incumbent, proposal, trigger_from_chain_int(t, incumbent, n), n)
                if m <= incumbent:
                    expected = "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"
                elif m == proposal:
                    expected = "CANDIDATE_FOR_PROTECTED_EVALUATION"
                elif m < proposal:
                    expected = "NO_JUMP_NEEDED_LOWER_LEVEL_SUFFICIENT"
                else:
                    expected = "PROPOSED_LEVEL_INSUFFICIENT"
                assert verdict == expected
                admissible_iff += 1
                skip_refused += verdict == "NO_JUMP_NEEDED_LOWER_LEVEL_SUFFICIENT"
                insufficient_refused += verdict == "PROPOSED_LEVEL_INSUFFICIENT"
        if t % 257 == 0:                                                                     # every 257th target: hostile probe (cost)
            assert assess_jump_int(t, 1, 2, mutant_poor_score_trigger(), n) == "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"
            poor_score_refused += 1
        if d == 3 and anf_int(t, n) >> 0b1110 & 1:
            honest = ceiling_certificate_int(t, 3, n)["status"]
            planted = ceiling_certificate_int(t, 3, n, degree_fn=mutant_partial_level3_degree)["status"]
            assert honest == "LOWER_LEVEL_SUFFICIENT" and planted == "CEILING"                # mutation applied: a false ceiling at level 3
            partial3_caught += 1
        ml = minimum_level_int(t, n, oracles={3: "CANNOT_CHECK"})
        assert ml == (max(1, d) if d <= 2 else "CANNOT_CHECK")
        cannot_check_cases += ml == "CANNOT_CHECK"
    assert sizes == {1: 32, 2: 2048, 3: 32768, 4: 65536}
    # J4 · problem reformulation relative to a registered class Φ (3-input tower): affine reformulations add nothing at any level
    n3 = 3
    aff_maps = gf2_affine_maps(n3)
    assert len(aff_maps) == 1344
    levels3 = {lv: frozenset(t for t in range(256) if degree_int(t, n3) <= lv) for lv in (1, 2, 3)}
    assert {lv: len(s) for lv, s in levels3.items()} == {1: 16, 2: 128, 3: 256}
    degree_invariant = 0
    for t in range(256):
        d = degree_int(t, n3)
        for phi in aff_maps:
            assert degree_int(compose_table(t, phi, n3), n3) == d
            degree_invariant += 1
    j4_gain_affine = {lv: len(reformulation_level(levels3[lv], aff_maps, n3) - levels3[lv]) for lv in (1, 2)}
    assert j4_gain_affine == {1: 0, 2: 0}
    # a registered non-affine reformulation (the transposition 000 ↔ 001) changes the J4 level: the ceiling is a function of the registry
    sigma = list(range(8))
    sigma[0], sigma[1] = 1, 0
    registry_prime = aff_maps + [tuple(sigma)]
    level1_prime = reformulation_level(levels3[1], registry_prime, n3)
    gained = sorted(level1_prime - levels3[1])
    assert gained and all(degree_int(q, n3) == 2 for q in gained)
    registry_dependence_witness = gained[0]
    assert mutant_uniform_reformulation_ceiling(registry_dependence_witness, level1_prime) == "CEILING"        # mutation applied
    assert registry_dependence_witness in level1_prime                                                        # honest: reachable under the registry, no ceiling
    # J5 · tool invention: with an unrestricted tool class the ceiling predicate is identically false (witness t = q), so no uniform
    # ceiling exists; with a registered finite class it is decidable by enumeration
    affine_basis = [0xFF, sum(1 << p for p in range(8) if p & 1), sum(1 << p for p in range(8) if p & 2), sum(1 << p for p in range(8) if p & 4)]
    assert span_int(affine_basis, n3) == levels3[1]
    unrestricted_ceilings = sum(1 for q in range(256) if q not in span_int(affine_basis + [q], n3))
    assert unrestricted_ceilings == 0
    tools = {"xy": sum(1 << p for p in range(8) if p & 1 and p & 2), "yz": sum(1 << p for p in range(8) if p & 2 and p & 4),
             "xz": sum(1 << p for p in range(8) if p & 1 and p & 4), "xyz": sum(1 << p for p in range(8) if p == 7)}
    tool_class = frozenset(tools.values())
    one_tool_level = frozenset().union(*(span_int(affine_basis + [t], n3) for t in tool_class))
    registered_ceilings = [q for q in range(256) if q not in one_tool_level]
    assert len(one_tool_level) == 16 + 4 * 16 and len(registered_ceilings) == 256 - 80
    q_two_tools = tools["xy"] ^ tools["yz"]
    assert q_two_tools in registered_ceilings
    planted = mutant_unregistered_tool(q_two_tools, affine_basis, tool_class)
    assert planted["status"] == "LOWER_LEVEL_SUFFICIENT" and not planted["registered"]                        # caught: the tool is not registered
    # no-alarm: affine targets produce no trigger at any proposed level (depth-4 tower)
    affine_no_jump = sum(1 for t in all4 if degrees[t] <= 1 for p in (2, 3, 4) if assess_jump_int(t, 1, p, trigger_from_chain_int(t, 1, n), n) == "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED")
    assert affine_no_jump == 32 * 3
    return {"depth4_targets": 1 << 16, "level_sizes": {str(k): v for k, v in sizes.items()}, "minimum_level_equals_anf_degree": min_level_eq_degree,
            "witness_checks_independent": witness_checks, "jump_admissible_iff_minimum_level": admissible_iff, "skip_to_higher_level_refused": skip_refused,
            "proposed_level_insufficient_refused": insufficient_refused, "mutant_poor_score_refused": poor_score_refused, "mutant_partial_level3_caught": partial3_caught,
            "cannot_check_when_level3_oracle_missing": cannot_check_cases, "affine_no_jump_no_alarm": affine_no_jump,
            "j4_affine_maps": len(aff_maps), "j4_degree_invariant_checks": degree_invariant, "j4_gain_under_affine_registry": j4_gain_affine,
            "j4_gain_under_registry_with_transposition": len(gained), "j4_registry_dependence_witness_table": registry_dependence_witness,
            "mutant_uniform_reformulation_ceiling_caught": 1, "j5_unrestricted_tool_class_ceilings": unrestricted_ceilings, "j5_witness": "t = q for every target",
            "j5_registered_class_size": len(tool_class), "j5_one_tool_level_size": len(one_tool_level), "j5_registered_ceilings": len(registered_ceilings),
            "mutant_unregistered_tool_caught": 1,
            "status": "PROVED depth-4 tower (degree levels); J4 exact relative to a registered reformulation class (registry-dependence witness); "
                      "J5 uniform ceiling impossible (vacuous, witness t = q), decidable per registered finite tool class"}


# ---------------------------------------------------------------------------------------------
# G2 · MEG-07 · per-source normalisation: monotone re-normalisation cannot rescue the M2.1 misses without breaking KS-T06;
#      matched-cardinality background is the uniform background (linearity); the registered structural clause gives no-drop
# ---------------------------------------------------------------------------------------------


def solve_linear(A, b):
    n = len(b)
    M = [list(row) + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [v / piv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [rv - f * cv for rv, cv in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def activation(atoms, out, seed, alpha):
    """Exact restart walk a = α s + (1−α) Pᵀ a with P row-normalised by out-degree (substochastic: dangling mass is lost)."""
    idx = {x: i for i, x in enumerate(atoms)}
    n = len(atoms)
    A = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for u in atoms:
        heads = out.get(u, [])
        for v in heads:
            A[idx[v]][idx[u]] -= (1 - alpha) / len(heads)
    b = [alpha * Fraction(seed.get(x, 0)) for x in atoms]
    sol = solve_linear(A, b)
    return {x: sol[idx[x]] for x in atoms}


def uniform_seed(atoms):
    return {x: Fraction(1, len(atoms)) for x in atoms}


def surprise_positive(a, pi):
    """ρ(v) > 0 ⇔ a(v) > π(v) for a > 0 (a·ln(a/π) > 0 ⇔ a > π): exact sign, no float."""
    return {x: (a[x] > 0 and a[x] > pi[x]) for x in a}


def m21_fixture(k=13, p=5):
    """The M2.1 finding-1 shape: request atom r with fan-out k, p popular sources feeding every child, grand-children; two further seeds."""
    atoms = ["r", "s2", "s3"] + [f"c{j}" for j in range(k)] + [f"u{i}" for i in range(p)] + [f"w{j}" for j in range(k)]
    out = {x: [] for x in atoms}
    out["r"] = [f"c{j}" for j in range(k)]
    for i in range(p):
        out[f"u{i}"] = [f"c{j}" for j in range(k)]
    for j in range(k):
        out[f"c{j}"] = [f"w{j}"]
    return atoms, out


def one_hop_heads(out, support, sigma, revoked, warrants):
    """The registered structural clause: LIVE one-hop heads v of a seed s with in-share (1/out-degree of s) ≥ σ."""
    heads = set()
    for s in support:
        hs = out.get(s, [])
        if hs and Fraction(1, len(hs)) >= sigma:
            heads.update(v for v in hs if liveness(warrants[v], revoked) == LIVE)
    return heads


def reacting_subgraph(a, pi, out, seed, sigma, revoked, warrants, clause=True):
    surprise = {x for x, ok in surprise_positive(a, pi).items() if ok}
    return surprise | set(seed) | (one_hop_heads(out, seed, sigma, revoked, warrants) if clause else set())


def mutant_seed_conditioned_background(atoms, out, seed, alpha):
    """Planted: 'seed-count-conditioned background' read as the walk from the same seed support with uniform weights."""
    return activation(atoms, out, {s: Fraction(1, len(seed)) for s in seed}, alpha)


def mutant_rescaled_background(pi, seed, atoms):
    """Planted: background scaled by |S|/N to 'match the seed cardinality'."""
    f = Fraction(len(seed), len(atoms))
    return {x: v * f for x, v in pi.items()}


def mutant_attribution_ratio(a_single, seed, atoms):
    """Planted: per-source reactivity = query attribution / background attribution through the same source = N·w_s for every atom reached."""
    n = len(atoms)
    return {x: max((Fraction(n) * Fraction(w) for s, w in seed.items() if a_single[s][x] > 0), default=Fraction(0)) for x in atoms}


def check_g2_per_source_normalisation():
    alpha, sigma = Fraction(1, 5), Fraction(1, 16)
    atoms, out = m21_fixture()
    warrants = {x: cert({f"e_{x}"}) for x in atoms}
    seed = {"r": Fraction(1, 3), "s2": Fraction(1, 3), "s3": Fraction(1, 3)}
    a = activation(atoms, out, seed, alpha)
    pi = activation(atoms, out, uniform_seed(atoms), alpha)
    children = [x for x in atoms if x.startswith("c")]
    grandchildren = [x for x in atoms if x.startswith("w")]
    # the miss: every LIVE one-hop child of the request atom has a_Q < π although its in-share 1/13 ≥ σ
    misses = [c for c in children if a[c] < pi[c]]
    assert len(misses) == 13 and all(a[c] > 0 for c in children)
    assert all(liveness(warrants[c], frozenset()) == LIVE for c in children) and Fraction(1, 13) >= sigma
    sp = surprise_positive(a, pi)
    assert not any(sp[c] for c in children) and sp["r"]
    # (i) monotone impossibility: φ nondecreasing in a, nonincreasing in π, φ(x, x) ≤ 0 (KS-T06) ⇒ φ(a, π) ≤ 0 whenever a ≤ π
    functionals = {"log_ratio": lambda x, y: float(x) * math.log(float(x) / float(y)), "difference": lambda x, y: x - y, "ratio_minus_one": lambda x, y: x / y - 1}
    monotone_excluded = 0
    for name_, phi in functionals.items():
        assert phi(Fraction(1, 7), Fraction(1, 7)) == 0 or abs(phi(Fraction(1, 7), Fraction(1, 7))) < 1e-15
        for c in misses:
            assert phi(a[c], pi[c]) <= 0
            monotone_excluded += 1
    # (ii) placebo: the mean activation over all seed sets of cardinality m equals the uniform background for every m (linearity)
    small_atoms = ["a", "b", "c", "d", "e", "f", "g"]
    small_out = {"a": ["b", "c"], "b": ["d"], "c": ["d", "e"], "d": ["a"], "e": ["f"], "f": [], "g": ["a", "e"]}
    pi_small = activation(small_atoms, small_out, uniform_seed(small_atoms), alpha)
    placebo_checks = 0
    for m in range(1, len(small_atoms) + 1):
        sets = list(itertools.combinations(small_atoms, m))
        mean = {x: Fraction(0) for x in small_atoms}
        for S in sets:
            act = activation(small_atoms, small_out, {s: Fraction(1, m) for s in S}, alpha)
            for x in small_atoms:
                mean[x] += act[x] / len(sets)
        assert mean == pi_small
        placebo_checks += len(sets)
    # (iii) the structural clause: no-drop for LIVE one-hop heads with in-share ≥ σ; surprise values untouched; cone bound
    g_surprise = reacting_subgraph(a, pi, out, seed, sigma, frozenset(), warrants, clause=False)
    g_clause = reacting_subgraph(a, pi, out, seed, sigma, frozenset(), warrants, clause=True)
    assert set(children) <= g_clause and not (set(children) & g_surprise)
    assert g_clause - g_surprise == set(children) and len(g_clause - g_surprise) <= sum(min(len(out[s]), int(1 / sigma)) for s in seed)
    assert not (set(grandchildren) & g_clause)
    # revocation gating: a DEAD child never enters through the clause
    g_rev = reacting_subgraph(a, pi, out, seed, sigma, frozenset({"e_c0"}), warrants, clause=True)
    assert "c0" not in g_rev and set(children[1:]) <= g_rev
    # KS-T06 / T06b on the hub fixture: values unchanged by the clause
    hub_atoms = ["s", "h", "x", "u1", "u2", "u3", "u4", "u5"]
    hub_out = {"s": ["h", "x"], "h": [], "x": [], "u1": ["h"], "u2": ["h"], "u3": ["h"], "u4": ["h"], "u5": ["h"]}
    hub_w = {z: cert({f"e_{z}"}) for z in hub_atoms}
    pi_h = activation(hub_atoms, hub_out, uniform_seed(hub_atoms), alpha)
    a_s = activation(hub_atoms, hub_out, {"s": Fraction(1)}, alpha)
    a_hub_only = activation(hub_atoms, hub_out, {"u1": Fraction(1)}, alpha)
    # T06: under the query-independent (uniform) seed every atom's surprise is zero, the hub included
    a_uni = activation(hub_atoms, hub_out, uniform_seed(hub_atoms), alpha)
    assert not any(surprise_positive(a_uni, pi_h).values())
    # T06b: seed touching hub and specific atom — specific first by surprise (h has none), hub first by popularity; hub-only seed: hub first by both
    assert a_s["h"] == a_s["x"] and pi_h["h"] > pi_h["x"]
    assert surprise_positive(a_s, pi_h)["x"] and not surprise_positive(a_s, pi_h)["h"]
    assert pi_h["h"] == max(pi_h.values())
    assert surprise_positive(a_hub_only, pi_h)["h"] and a_hub_only["x"] == 0
    g_hub = reacting_subgraph(a_s, pi_h, hub_out, {"s": Fraction(1)}, sigma, frozenset(), hub_w, clause=True)
    assert g_hub == {"s", "x", "h"}                                                             # clause adds h (LIVE one-hop, share 1/2); a and π are read, never written
    # hostiles
    pi_mut = mutant_seed_conditioned_background(atoms, out, seed, alpha)
    assert pi_mut == a                                                                           # mutation applied: background = query activation
    assert not any(surprise_positive(a, pi_mut).values())                                        # caught: everything dropped, the request atom included
    pi_res = mutant_rescaled_background(pi, seed, atoms)
    sp_res = surprise_positive(a, pi_res)
    assert all(sp_res[c] for c in children)                                                      # mutation applied: the misses are admitted …
    extra = {x for x, ok in sp_res.items() if ok} - g_clause
    assert set(grandchildren) <= extra                                                           # … caught: 13 second-hop atoms admitted, cone bound broken
    a_single = {s: activation(hub_atoms, hub_out, {s: Fraction(1)}, alpha) for s in ("s",)}
    ratio = mutant_attribution_ratio(a_single, {"s": Fraction(1)}, hub_atoms)
    assert ratio["h"] == ratio["x"] == 8                                                         # caught: T06b's strict order is lost (tie)
    # no-alarm: with σ = 1 (clause disabled for any fan-out > 1) G_Q equals the surprise set plus seeds
    assert reacting_subgraph(a, pi, out, seed, Fraction(1), frozenset(), warrants, clause=True) == g_surprise
    return {"fixture_atoms": len(atoms), "fan_out": 13, "popular_sources": 5, "misses_reproduced": len(misses), "in_share": "1/13", "sigma": str(sigma),
            "request_activation": str(a["r"]), "child_activation": str(a["c0"]), "child_background": str(pi["c0"]),
            "monotone_functional_exclusions": monotone_excluded, "placebo_seed_sets": placebo_checks, "placebo_graph_atoms": len(small_atoms),
            "clause_admits_children": 13, "clause_extra_bound": sum(min(len(out[s]), int(1 / sigma)) for s in seed), "grandchildren_excluded": len(grandchildren),
            "dead_child_excluded": 1, "t06_uniform_seed_zero_surprise": 1, "t06b_specific_first_hub_popular": 1, "t06b_hub_only": 1,
            "mutant_seed_conditioned_caught": 1, "mutant_rescaled_extra_atoms": len(extra), "mutant_rescaled_caught": 1, "mutant_attribution_ratio_caught": 1, "sigma_one_no_alarm": 1,
            "status": "PROVED: monotone re-normalisation cannot admit a < π without breaking KS-T06; matched-cardinality background is the uniform background; "
                      "no-drop by the registered structural clause (cone ≤ Σ_s min(k_s, ⌊1/σ⌋)) with KS-T06/T06b untouched"}


# ---------------------------------------------------------------------------------------------
# G3 · MEG-27 · context-free inventory: exact prefix commitment by product fixed point; bounded lookahead complete at ℓ*;
#      ℓ* unbounded over prefixes (no prefix-independent bound); CF acceptability = undecidable intersection (cited)
# ---------------------------------------------------------------------------------------------

CF_TOKENS = {"cat": ("N", "cat"), "dog": ("N", "dog"), "bird": ("N", "bird"), "that": ("REL", None), "chased": ("V", "c1"), "ran": ("V", "c2"), "sang": ("V", "c3")}
PRODUCTIONS = {"S": [("NP", "VP"), ("NP", "REL", "S", "VP")], "NP": [("N",)], "VP": [("V",)]}
CF_TERMINALS = {"N", "REL", "V"}


def cf_token_step(tok, used, state):
    """The acceptability predicate per token (regular given the state): referent resolvable and within budget; claim LIVE."""
    cat, payload = CF_TOKENS[tok]
    if cat == "N":
        if payload not in state["refs"]:
            return None
        u2 = used | {payload}
        return u2 if len(u2) <= state["budget"] else None
    if cat == "V":
        return used if state["live"].get(payload) == LIVE else None
    return used


_EXPAND = {}


def expand_to_terminal_top(stack):
    """All stacks derivable from `stack` by expanding leading nonterminals until a terminal is on top (finite: no left recursion)."""
    stack = tuple(stack)
    if stack in _EXPAND:
        return _EXPAND[stack]
    out, frontier = set(), [stack]
    while frontier:
        st = frontier.pop()
        if not st or st[0] in CF_TERMINALS:
            out.add(st)
            continue
        for prod in PRODUCTIONS[st[0]]:
            frontier.append(prod + st[1:])
    _EXPAND[stack] = frozenset(out)
    return _EXPAND[stack]


def state_key(state):
    return (frozenset(state["refs"]), tuple(sorted(state["live"].items())), state["budget"])


_CONFIGS = {}


def cf_prefix_configs(prefix, state):
    key = (tuple(prefix), state_key(state))
    if key in _CONFIGS:
        return _CONFIGS[key]
    configs = {(st, frozenset()) for st in expand_to_terminal_top(("S",))}
    for tok in prefix:
        cat = CF_TOKENS[tok][0]
        nxt = set()
        for st, used in configs:
            if not st or st[0] != cat:
                continue
            u2 = cf_token_step(tok, used, state)
            if u2 is None:
                continue
            for st2 in expand_to_terminal_top(st[1:]):
                nxt.add((st2, u2))
        configs = nxt
    _CONFIGS[key] = frozenset(configs)
    return _CONFIGS[key]


def cf_universe(state):
    refs = sorted(state["refs"] | {p for c, p in CF_TOKENS.values() if c == "N"})
    return [frozenset(u) for u in subsets(refs)]


def cf_gen_table(state):
    """Least fixed point: gen[X][U] = set of used-sets reachable after generating X acceptably from U (finite lattice ⇒ terminates)."""
    universe = cf_universe(state)
    gen = {X: {U: set() for U in universe} for X in PRODUCTIONS}

    def run_symbol(sym, current):
        out = set()
        for U in current:
            if sym in CF_TERMINALS:
                for tok, (cat, _) in CF_TOKENS.items():
                    if cat == sym:
                        u2 = cf_token_step(tok, U, state)
                        if u2 is not None:
                            out.add(u2)
            else:
                out |= gen[sym][U]
        return out

    changed = True
    while changed:
        changed = False
        for X, prods in PRODUCTIONS.items():
            for U in universe:
                acc = set()
                for prod in prods:
                    cur = {U}
                    for sym in prod:
                        cur = run_symbol(sym, cur)
                        if not cur:
                            break
                    acc |= cur
                if not acc <= gen[X][U]:
                    gen[X][U] |= acc
                    changed = True
    return gen, run_symbol


def cf_exact(prefix, state, table=None):
    """Exact prefix commitment: SAT iff some configuration of the prefix generates an acceptable completion (product fixed point)."""
    configs = cf_prefix_configs(prefix, state)
    if not configs:
        return "UNSAT"
    gen, run_symbol = table or cf_gen_table(state)
    for st, used in configs:
        cur = {used}
        for sym in st:
            cur = run_symbol(sym, cur)
            if not cur:
                break
        if cur:
            return "SAT"
    return "UNSAT"


def cf_bounded(prefix, state, k):
    """Bounded lookahead: SAT if an acceptable completion of ≤ k tokens exists; UNSAT only if every continuation died with nothing pruned;
    CANNOT_CHECK when unfinished continuations were cut off by the bound."""
    configs = cf_prefix_configs(prefix, state)
    if not configs:
        return "UNSAT"
    pruned = False
    frontier = set()
    for st, used in configs:
        if len(st) <= k:
            frontier.add((st, used))
        else:
            pruned = True
    for consumed in range(k + 1):
        if any(not st for st, _ in frontier):
            return "SAT"
        if not frontier:
            return "CANNOT_CHECK" if pruned else "UNSAT"
        remaining = k - consumed
        if remaining == 0:
            return "CANNOT_CHECK"
        nxt = set()
        for st, used in frontier:
            cat = st[0]
            for tok, (c, _p) in CF_TOKENS.items():
                if c != cat:
                    continue
                u2 = cf_token_step(tok, used, state)
                if u2 is None:
                    continue
                for st2 in expand_to_terminal_top(st[1:]):
                    if len(st2) <= remaining - 1:
                        nxt.add((st2, u2))
                    else:
                        pruned = True
        frontier = nxt
    return "CANNOT_CHECK"


INF = 10 ** 9


def cf_min_length_table(state):
    """Exact shortest-completion lengths ml[X][U][U'] = min tokens generating X acceptably from U and ending in U' — the computable threshold."""
    universe = cf_universe(state)
    ml = {X: {U: {} for U in universe} for X in PRODUCTIONS}

    def step(sym, cur):
        nxt = {}
        for u, L in cur.items():
            if sym in CF_TERMINALS:
                for t, (c, _) in CF_TOKENS.items():
                    if c == sym:
                        u2 = cf_token_step(t, u, state)
                        if u2 is not None:
                            nxt[u2] = min(nxt.get(u2, INF), L + 1)
            else:
                for u2, L2 in ml[sym][u].items():
                    nxt[u2] = min(nxt.get(u2, INF), L + L2)
        return nxt

    changed = True
    while changed:
        changed = False
        for X, prods in PRODUCTIONS.items():
            for U in universe:
                acc = {}
                for prod in prods:
                    cur = {U: 0}
                    for sym in prod:
                        cur = step(sym, cur)
                        if not cur:
                            break
                    for u2, L in cur.items():
                        acc[u2] = min(acc.get(u2, INF), L)
                for u2, L in acc.items():
                    if L < ml[X][U].get(u2, INF):
                        ml[X][U][u2] = L
                        changed = True
    return ml, step


def cf_threshold(prefix, state, step):
    """ℓ*(prefix, state): the exact shortest acceptable completion length over the prefix's configurations (INF if none)."""
    thr = INF
    for stack, used in cf_prefix_configs(prefix, state):
        cur = {used: 0}
        for sym in stack:
            cur = step(sym, cur)
            if not cur:
                break
        if cur:
            thr = min(thr, min(cur.values()))
    return thr


def mutant_bound_is_pass(verdict):
    return "SAT" if verdict == "CANNOT_CHECK" else verdict


def mutant_fixed_bound_is_unsat(verdict):
    return "UNSAT" if verdict == "CANNOT_CHECK" else verdict


def mutant_regular_approximation(prefix, state):
    """Planted: the CF inventory approximated by the DFA N (REL N)* V+ (nesting depth forgotten)."""
    q = 0
    for tok in prefix:
        cat = CF_TOKENS[tok][0]
        if q == 0 and cat == "N":
            q = 1
        elif q == 1 and cat == "REL":
            q = 0
        elif q in (1, 2) and cat == "V":
            q = 2
        else:
            return "UNSAT"
    return "SAT"


def check_g3_context_free_inventory():
    tokens = list(CF_TOKENS)
    full = {"refs": {"cat", "dog", "bird"}, "live": {"c1": LIVE, "c2": LIVE, "c3": LIVE}, "budget": 3}
    prefixes = [()]
    for n in range(1, 5):
        prefixes += [p for p in itertools.product(tokens, repeat=n) if cf_prefix_configs(p, full)]
    states = [{"refs": set(r), "live": {"c1": l1, "c2": l2, "c3": l3}, "budget": b}
              for r in subsets(["cat", "dog", "bird"]) for l1 in (LIVE, DEAD) for l2 in (LIVE, DEAD) for l3 in (LIVE, DEAD) for b in (1, 2, 3)]
    bounds = range(0, 6)
    n = agree = cannot = sat_cases = unsat_cases = unsat_never_by_bound = 0
    exact_at_threshold = sat_beyond_bounds = fixed_point_agrees_min_length = mutant_pass_caught = mutant_unsat_caught = 0
    lstar_hist = {}
    for st in states:
        table = cf_gen_table(st)
        ml, step = cf_min_length_table(st)
        for p in prefixes:
            n += 1
            ex = cf_exact(p, st, table)
            thr = cf_threshold(p, st, step)
            assert (thr < INF) == (ex == "SAT")                              # the set fixed point and the min-plus table agree
            fixed_point_agrees_min_length += 1
            verdicts = {k: cf_bounded(p, st, k) for k in bounds}
            for k, v in verdicts.items():
                if v != "CANNOT_CHECK":
                    assert v == ex                                              # a decisive bounded verdict never contradicts the exact decision
                    agree += 1
                else:
                    cannot += 1
                if mutant_bound_is_pass(v) == "SAT" and ex == "UNSAT":
                    mutant_pass_caught += 1
                if mutant_fixed_bound_is_unsat(v) == "UNSAT" and ex == "SAT":
                    mutant_unsat_caught += 1
            if ex == "SAT":
                sat_cases += 1
                sat_bounds = [k for k, v in verdicts.items() if v == "SAT"]
                if sat_bounds:
                    lstar = min(sat_bounds)
                    assert lstar == thr and all(verdicts[k] == "CANNOT_CHECK" for k in bounds if k < thr)   # complete iff k ≥ ℓ*, honest below
                    exact_at_threshold += 1
                    lstar_hist[lstar] = lstar_hist.get(lstar, 0) + 1
                else:
                    assert thr > max(bounds) and all(v == "CANNOT_CHECK" for v in verdicts.values())
                    sat_beyond_bounds += 1
            else:
                unsat_cases += 1
                if all(v == "CANNOT_CHECK" for v in verdicts.values()):
                    assert all(l == DEAD for l in st["live"].values()) and cf_prefix_configs(p, st)   # only dead-claim UNSAT escapes every bound
                    unsat_never_by_bound += 1
    assert unsat_never_by_bound > 0                                                            # dead-claim UNSAT is decided by the fixed point alone
    # no prefix-independent bound: the nested prefix with d open clauses needs exactly d + 1 tokens (d = 0 … 4)
    depth_table = {}
    for d in range(0, 5):
        p = ("cat",) + ("that", "cat") * d
        assert cf_exact(p, full) == "SAT"
        lstar = min(k for k in range(0, 8) if cf_bounded(p, full, k) == "SAT")
        assert lstar == d + 1 and cf_bounded(p, full, d) == "CANNOT_CHECK"
        depth_table[d] = lstar
    # regular approximation commits a prefix outside the inventory
    bad = ("cat", "chased", "ran")
    assert mutant_regular_approximation(bad, full) == "SAT" and cf_exact(bad, full) == "UNSAT"
    # no-alarm: with every claim LIVE, all referents resolvable and budget 3, every prefix of a full sentence commits (SAT)
    assert all(cf_exact(("cat", "that", "dog", "chased", "ran")[:i], full) == "SAT" for i in range(6))
    # budget exhaustion is a genuine UNSAT decided by the exact check; dead claims are UNSAT never reached by any bound
    tight = {"refs": {"cat", "dog", "bird"}, "live": {"c1": LIVE, "c2": LIVE, "c3": LIVE}, "budget": 1}
    assert cf_exact(("cat", "that", "dog"), tight) == "UNSAT" and cf_exact(("cat", "that", "cat"), tight) == "SAT"
    dead = {"refs": {"cat", "dog", "bird"}, "live": {"c1": DEAD, "c2": DEAD, "c3": DEAD}, "budget": 3}
    assert cf_exact(("cat",), dead) == "UNSAT" and all(cf_bounded(("cat",), dead, k) == "CANNOT_CHECK" for k in range(1, 6))
    return {"prefixes": len(prefixes), "states": len(states), "cases": n, "bounds": list(bounds), "bounded_agrees_with_exact": agree, "bounded_cannot_check": cannot,
            "fixed_point_agrees_with_min_length_table": fixed_point_agrees_min_length, "sat_cases": sat_cases, "unsat_cases": unsat_cases,
            "unsat_never_reached_by_any_bound": unsat_never_by_bound, "sat_complete_exactly_at_lstar": exact_at_threshold, "sat_beyond_every_tried_bound": sat_beyond_bounds,
            "lstar_histogram": {str(k): v for k, v in sorted(lstar_hist.items())}, "depth_to_lstar": {str(k): v for k, v in depth_table.items()},
            "mutant_bound_is_pass_caught": mutant_pass_caught, "mutant_fixed_bound_is_unsat_caught": mutant_unsat_caught, "mutant_regular_approximation_caught": 1,
            "full_sentence_no_alarm": 1, "budget_unsat_exact": 1, "dead_claims_unsat_only_by_fixed_point": 1,
            "status": "PROVED (CF inventory, state-regular acceptability: exact by product fixed point; bounded check complete iff k ≥ ℓ*; ℓ* unbounded over prefixes); "
                      "CF acceptability: intersection emptiness undecidable — PARENT_OWNED (Bar-Hillel–Perles–Shamir 1961), CANNOT_CHECK is the only honest answer without a threshold"}


# ---------------------------------------------------------------------------------------------
# G4 · MEG-19 · deconsolidation decision: MDL rule (PARENT_OWNED, executable) with its falsifier; the parts that are not parent-owned
# ---------------------------------------------------------------------------------------------


def edge(eid, tails, heads, rel="DEPENDENCE"):
    tails = (tails,) if isinstance(tails, str) else tuple(tails)
    heads = (heads,) if isinstance(heads, str) else tuple(heads)
    return (eid, tails, heads, rel)


def nav_cost(edges, seed, target):
    seen, frontier, cost = {seed}, [seed], 0
    while frontier:
        nxt = []
        for x in frontier:
            for e in edges:
                if x in e[1]:
                    cost += 1
                    for h in e[2]:
                        if h == target:
                            return cost, True
                        if h not in seen:
                            seen.add(h)
                            nxt.append(h)
        frontier = nxt
    return cost, False


def chain_space(k):
    fine = [edge("s->x1", "s", "x1")] + [edge(f"x{i}->x{i+1}", f"x{i}", f"x{i+1}") for i in range(1, k)] + [edge(f"x{k}->t", f"x{k}", "t")]
    coarse = [edge("s->m", "s", "m"), edge("m->t", "m", "t")]
    return fine, coarse


def multiscale_cost(fine, coarse, target, exported):
    c_cost, found = nav_cost(coarse, "s", target if target in exported else "__absent__")
    if found:
        return c_cost
    f_cost, _ = nav_cost(fine, "s", target)
    return c_cost + f_cost


def mdl_decision(k, uses, live_exceptions, name_cost=1):
    """Two-part code (Rissanen; DreamCoder/LILO library objective): keep the macro iff its code length ≤ the spelled-out code length."""
    without = uses * k
    with_macro = (k + name_cost) + uses * name_cost + live_exceptions * (k + name_cost)
    return ("KEEP" if with_macro <= without else "SPLIT"), with_macro, without


def live_exception_count(exceptions, revoked):
    return sum(1 for iv in exceptions if liveness(iv, revoked) == LIVE)


def mutant_count_dead_exceptions(exceptions, revoked):
    return len(exceptions)


def mutant_mdl_implies_navigation_gain(k, Q):
    """Planted: 'MDL keeps ⇒ navigation on Q improves'."""
    fine, coarse = chain_space(k)
    before = sum(nav_cost(fine, "s", q)[0] for q in Q)
    after = sum(multiscale_cost(fine, coarse, q, {"t"}) for q in Q)
    return after < before


def check_g4_deconsolidation_decision():
    table, crossover = {}, {}
    n = 0
    for k in range(1, 6):
        for uses in range(0, 9):
            for e in range(0, 7):
                n += 1
                d, w, wo = mdl_decision(k, uses, e)
                table[(k, uses, e)] = d
                assert d == ("KEEP" if (k + 1) * (1 + e) <= uses * (k - 1) else "SPLIT")     # closed form of the fixture's code
        crossover[k] = {e: min((u for u in range(0, 40) if mdl_decision(k, u, e)[0] == "KEEP"), default=None) for e in range(0, 4)}
    assert all(v is None for v in crossover[1].values())                                   # a 1-constituent macro never pays
    # not parent-owned (a): exceptions count only while LIVE — a revoked exception is no obligation
    exc = [cert({"g1"}), cert({"g2"}), cert({"g3"})]
    live_gated = dead_counted = premature_split = 0
    for R in subsets(["g1", "g2", "g3"]):
        lc = live_exception_count(exc, R)
        mc = mutant_count_dead_exceptions(exc, R)
        assert lc == 3 - len(R) and mc == 3
        live_gated += 1
        if R:
            dead_counted += 1
            # at k = 3, uses = 8: KEEP iff 4(1+e) ≤ 16 ⇔ e ≤ 3: honest keeps for every R; the mutant with 3 counted keeps too — so use uses = 6: KEEP iff e ≤ 2
            honest = mdl_decision(3, 6, lc)[0]
            planted = mdl_decision(3, 6, mc)[0]
            assert planted == "SPLIT"
            if honest == "KEEP":
                premature_split += 1
    assert premature_split == 7                                                              # every non-empty revocation set: mutant splits while honest keeps
    # not parent-owned (b): MDL keep is not navigation gain — E8 fixture k = 1, Q = {t, x1}: KEEP at uses ≥ … never (k=1); k = 2, uses 8, e = 0: KEEP (3·1 ≤ 8), navigation 4 → 5
    assert mdl_decision(2, 8, 0)[0] == "KEEP" and not mutant_mdl_implies_navigation_gain(2, ["t", "x1"])
    assert mutant_mdl_implies_navigation_gain(2, ["t"])                                      # and it does improve when Q ⊆ exports (3 → 2)
    # not parent-owned (c): the decision is a governed proposal — self-adoption refused (batch-5 E4 shape re-checked minimally)
    def adopt(decision, external_commit):
        return "ADOPTED" if external_commit else "PROPOSAL_ONLY"
    assert adopt("SPLIT", False) == "PROPOSAL_ONLY" and adopt("SPLIT", True) == "ADOPTED"
    # no-alarm: no exceptions, many uses of a long macro — both counts agree, KEEP
    assert mdl_decision(4, 8, live_exception_count([], frozenset()))[0] == mdl_decision(4, 8, mutant_count_dead_exceptions([], frozenset()))[0] == "KEEP"
    return {"mdl_cases": n, "closed_form_checks": n, "crossover_uses_by_k_and_exceptions": {str(k): {str(e): v for e, v in d.items()} for k, d in crossover.items()},
            "exception_liveness_gating_checks": live_gated, "mutant_dead_exception_cases": dead_counted, "mutant_premature_split_caught": premature_split,
            "mdl_keep_without_navigation_gain_witness": {"k": 2, "uses": 8, "Q": ["t", "x1"], "before": 4, "after": 5}, "governed_proposal_only": 1, "no_exception_no_alarm": 1,
            "status": "PARENT_OWNED decision (MDL two-part code; DreamCoder/LILO) executable with closed form; PROVED not parent-owned: LIVE-gated exception count, "
                      "warrant exactness (R1), governance (proposal only), and MDL-keep ≠ navigation gain (E8 witness)"}


# ---------------------------------------------------------------------------------------------
# G5 · KS-T12 / KS-T14 improvement halves: exact clauses (theorems) and exact refutations of the unconditional forms
# ---------------------------------------------------------------------------------------------

F1, FA, FB, FAB = (1, 1, 1, 1), (0, 0, 1, 1), (0, 1, 0, 1), (0, 0, 0, 1)
FEATURES = {"feat_1": F1, "feat_a": FA, "feat_b": FB, "feat_ab": FAB}
ALL_TABLES = [tuple(bits) for bits in itertools.product((0, 1), repeat=4)]


def xor_span(tables):
    out = set()
    for coeffs in itertools.product((0, 1), repeat=len(tables)):
        out.add(tuple(sum(c * f[i] for c, f in zip(coeffs, tables)) % 2 for i in range(4)))
    return frozenset(out)


def ceiling_on(Q, R):
    return len(set(Q) & xor_span([FEATURES[f] for f in R]))


def check_g5_improvement_halves():
    # KS-T12 on the chain family: exact clause
    t12_cases = clause_checks = never_worse_exports = 0
    refutation = None
    for k in range(1, 7):
        fine, coarse = chain_space(k)
        internals = [f"x{i}" for i in range(1, k + 1)]
        for r in range(1, k + 2):
            for Q in itertools.combinations(internals + ["t"], r):
                t12_cases += 1
                before = sum(nav_cost(fine, "s", q)[0] for q in Q)
                after = sum(multiscale_cost(fine, coarse, q, {"t"}) for q in Q)
                n_int = sum(q != "t" for q in Q)
                predicted_improves = (k - 1) * ("t" in Q) > 2 * n_int
                assert (after < before) == predicted_improves
                assert (before - after) == (k - 1) * ("t" in Q) - 2 * n_int                   # exact gain
                clause_checks += 1
                if set(Q) <= {"t"}:
                    assert after <= before
                    never_worse_exports += 1
                if refutation is None and after > before:
                    refutation = {"k": k, "Q": list(Q), "before": before, "after": after}
    assert refutation == {"k": 1, "Q": ["x1"], "before": 1, "after": 3}
    fine2, coarse2 = chain_space(2)
    assert (nav_cost(fine2, "s", "t")[0], multiscale_cost(fine2, coarse2, "t", {"t"})) == (3, 2)          # smallest holding fixture
    # KS-T14: nested Jump (span(R) ⊆ span(R')) never lowers the ceiling; improves on Q iff Q meets span(R') \ span(R); non-nested can lower
    feats = list(FEATURES)
    pairs = monotone_nested = lowered_non_nested = improve_iff = 0
    harmful = None
    for R in subsets(feats):
        for Rp in subsets(feats):
            sR, sRp = xor_span([FEATURES[f] for f in R]), xor_span([FEATURES[f] for f in Rp])
            nested = sR <= sRp
            for Q in (ALL_TABLES, [FAB], [(0, 1, 1, 0)], [FAB, (0, 1, 1, 0)]):
                pairs += 1
                before, after = ceiling_on(Q, R), ceiling_on(Q, Rp)
                if nested:
                    assert after >= before
                    monotone_nested += 1
                    assert (after > before) == bool(set(Q) & (sRp - sR))
                    improve_iff += 1
                elif after < before:
                    lowered_non_nested += 1
                    if harmful is None and Q == [(0, 1, 1, 0)] and R == frozenset({"feat_1", "feat_a", "feat_b"}) and Rp == frozenset({"feat_1", "feat_ab"}):
                        harmful = {"R": sorted(R), "R'": sorted(Rp), "Q": Q, "before": before, "after": after}
    assert lowered_non_nested > 0 and harmful == {"R": ["feat_1", "feat_a", "feat_b"], "R'": ["feat_1", "feat_ab"], "Q": [(0, 1, 1, 0)], "before": 1, "after": 0}
    assert ceiling_on([(0, 1, 1, 0)], ["feat_1", "feat_a", "feat_b"]) == 1 and ceiling_on([(0, 1, 1, 0)], ["feat_1", "feat_ab"]) == 0   # the S6 shape
    # hostiles: the unconditional laws, planted as predicates — each refuted by the recorded counterexample
    def mutant_t12_unconditional(k, Q):
        return True
    def mutant_t14_unconditional(R, Rp, Q):
        return True
    assert mutant_t12_unconditional(1, ["x1"]) and not mutant_mdl_implies_navigation_gain(1, ["x1"])
    assert mutant_t14_unconditional(["feat_1", "feat_a", "feat_b"], ["feat_1", "feat_ab"], [(0, 1, 1, 0)]) and ceiling_on([(0, 1, 1, 0)], ["feat_1", "feat_ab"]) < ceiling_on([(0, 1, 1, 0)], ["feat_1", "feat_a", "feat_b"])
    # no-alarm: Q ⊆ exports, k ≥ 2 improves (3 → 2); AND under affine → quadratic improves (0 → 1)
    assert mutant_mdl_implies_navigation_gain(2, ["t"]) and ceiling_on([FAB], ["feat_1", "feat_a", "feat_b"]) == 0 and ceiling_on([FAB], feats) == 1
    return {"t12_chain_cases": t12_cases, "t12_clause_checks": clause_checks, "t12_never_worse_when_Q_in_exports": never_worse_exports,
            "t12_smallest_holding": {"k": 2, "Q": ["t"], "before": 3, "after": 2}, "t12_unconditional_refutation": refutation,
            "t14_pairs_x_Q": pairs, "t14_monotone_when_nested": monotone_nested, "t14_improve_iff_Q_meets_difference": improve_iff, "t14_lowered_when_not_nested": lowered_non_nested,
            "t14_unconditional_refutation": {"R": ["feat_1", "feat_a", "feat_b"], "R'": ["feat_1", "feat_ab"], "Q": "XOR", "before": 1, "after": 0},
            "mutant_unconditional_t12_refuted": 1, "mutant_unconditional_t14_refuted": 1, "no_alarm": 1,
            "status": "PROVED (exact clauses on the recorded fixtures): KS-T12 gain = (k−1)[t∈Q] − 2|Q∩internals| on the chain family; KS-T14 nested ⇒ monotone, "
                      "improves iff Q meets span(R')∖span(R); both unconditional forms REFUTED (counterexamples recorded)"}


# ---------------------------------------------------------------------------------------------
# G6 · MEG-02 · the (+,×) reading as a measure over warrants: what it licenses (expectation receipts) without being a homomorphism
# ---------------------------------------------------------------------------------------------

E6 = ("a", "b", "c")


def antichains(ids):
    fams = set()
    allsets = [frozenset(s) for s in subsets(ids)]
    for r in range(0, len(allsets) + 1):
        for combo in itertools.combinations(allsets, r):
            fams.add(canon(combo))
    return sorted(fams, key=lambda p: (len(p), repr(p)))


def world_probability(world, grades):
    p = Fraction(1)
    for e, g in grades.items():
        p *= g if e in world else (1 - g)
    return p


def supported(D, world, revoked):
    return any(d <= world and not (d & revoked) for d in D)


def measure(D, grades, revoked=frozenset()):
    """μ_R(D) = P_g(some alternative of D survives R and lies in the true world) — exact by world enumeration; revoked ids forced false."""
    return sum((world_probability(w, grades) for w in subsets(E6) if supported(D, w, revoked)), Fraction(0))


def plus_times_sum(D, grades):
    return sum((math.prod(grades[e] for e in d) for d in D), Fraction(0)) if D else Fraction(0)


def joint_coverage(Ds, grades, threshold):
    """P(#supported ≥ threshold) exactly from the joint law (sharing honoured)."""
    return sum((world_probability(w, grades) for w in subsets(E6) if sum(supported(D, w, frozenset()) for D in Ds) >= threshold), Fraction(0))


def mutant_independent_coverage(Ds, grades, threshold):
    """Planted: coverage computed as if the atoms were independent (Poisson-binomial of the marginals)."""
    mus = [measure(D, grades) for D in Ds]
    total = Fraction(0)
    for bits in itertools.product((0, 1), repeat=len(mus)):
        if sum(bits) >= threshold:
            total += math.prod(m if b else 1 - m for m, b in zip(mus, bits))
    return total


def mutant_measure_promotes_liveness(iv, grades, revoked):
    return LIVE if measure(iv[1], grades, revoked) > Fraction(1, 2) else liveness(iv, revoked)


def check_g6_measure_reading():
    fams = antichains(E6)
    assert len(fams) == 20                                                                     # Dedekind M(3)
    gradings = [{"a": Fraction(1, 2), "b": Fraction(1, 3), "c": Fraction(2, 3)}, {"a": Fraction(9, 10), "b": Fraction(3, 5), "c": Fraction(1, 4)}]
    valuation = monotone = disjoint_product = shared_not_product = sum_eq_iff_single = retract_exact = 0
    sum_over_one = None
    for g in gradings:
        for D1 in fams:
            for D2 in fams:
                # inclusion–exclusion on the lattice: μ(D1 ⊕ D2) = μ(D1) + μ(D2) − μ(D1 ⊗ D2)
                assert measure(join(D1, D2), g) == measure(D1, g) + measure(D2, g) - measure(meet(D1, D2), g)
                valuation += 1
                if all(any(d1 <= d2 for d1 in D1) for d2 in D2):                               # D2 ≤ D1 in the antichain order ⇒ μ(D2) ≤ μ(D1)
                    assert measure(D2, g) <= measure(D1, g)
                    monotone += 1
                ids1, ids2 = frozenset().union(*D1) if D1 else frozenset(), frozenset().union(*D2) if D2 else frozenset()
                prod_eq = measure(meet(D1, D2), g) == measure(D1, g) * measure(D2, g)
                if not (ids1 & ids2):
                    assert prod_eq
                    disjoint_product += 1
                elif D1 and D2:
                    assert not prod_eq                                                         # sharing ⇒ the product rule fails (grades strictly inside (0,1))
                    shared_not_product += 1
            # (+,×) homomorphic sum equals the measure iff at most one alternative; it can exceed 1
            s, m = plus_times_sum(D1, g), measure(D1, g)
            assert (s == m) == (len(D1) <= 1)
            sum_eq_iff_single += 1
            if s > 1 and sum_over_one is None:
                sum_over_one = {"D": [sorted(d) for d in D1], "sum": str(s), "measure": str(m)}
            # retraction: forcing revoked ids false equals re-measuring the surviving alternatives
            for R in subsets(E6):
                surv = canon(d for d in D1 if not (d & R))
                assert measure(D1, g, R) == measure(surv, g)
                retract_exact += 1
    assert sum_over_one is not None
    # what the measure licenses: E[#supported] = Σ μ_i for every batch, sharing or not (linearity); concentration needs the joint law
    g = gradings[0]
    triples = [(fams[i], fams[j], fams[k]) for i in range(len(fams)) for j in range(i, len(fams)) for k in range(j, len(fams))]
    expectation_checks = independent_wrong = independent_right_when_disjoint = 0
    for Ds in triples:
        exp_joint = sum((world_probability(w, g) * sum(supported(D, w, frozenset()) for D in Ds) for w in subsets(E6)), Fraction(0))
        assert exp_joint == sum(measure(D, g) for D in Ds)
        expectation_checks += 1
        ids = [frozenset().union(*D) if D else frozenset() for D in Ds]
        pairwise_disjoint = all(not (ids[i] & ids[j]) for i in range(3) for j in range(i + 1, 3))
        truth, planted = joint_coverage(Ds, g, 2), mutant_independent_coverage(Ds, g, 2)
        if pairwise_disjoint:
            assert truth == planted
            independent_right_when_disjoint += 1
        elif truth != planted:
            independent_wrong += 1
    assert independent_wrong > 0
    # the score is not a warrant: an UNKNOWN interval with μ(up) > ½ stays UNKNOWN; the mutant promotes it
    iv = (ZERO, canon([frozenset({"a"})]))
    assert liveness(iv, frozenset()) == UNKNOWN and measure(iv[1], gradings[1]) == Fraction(9, 10)
    assert mutant_measure_promotes_liveness(iv, gradings[1], frozenset()) == LIVE                  # mutation applied and caught by KS-T21's rule
    # the R3 witness as a measure: D = {{a, b1}, {a, b2}} with all grades ½ — sum ½ (double count) vs measure 3/8
    g3 = {"a": Fraction(1, 2), "b": Fraction(1, 2), "c": Fraction(1, 2)}
    D_r3 = canon([frozenset({"a", "b"}), frozenset({"a", "c"})])
    assert plus_times_sum(D_r3, g3) == Fraction(1, 2) and measure(D_r3, g3) == Fraction(3, 8)
    # no-alarm: a single derivation — sum, measure and product rule coincide
    single = canon([frozenset({"a"})])
    assert plus_times_sum(single, g) == measure(single, g) == g["a"]
    return {"antichains": len(fams), "gradings": len(gradings), "valuation_identity_checks": valuation, "monotone_checks": monotone, "disjoint_product_rule_checks": disjoint_product,
            "shared_product_rule_fails": shared_not_product, "sum_equals_measure_iff_single_checks": sum_eq_iff_single, "sum_exceeds_one_witness": sum_over_one,
            "retraction_by_forcing_equals_survivors": retract_exact, "batches": len(triples), "expectation_linearity_checks": expectation_checks,
            "mutant_independent_coverage_wrong": independent_wrong, "independent_coverage_right_when_disjoint": independent_right_when_disjoint,
            "mutant_measure_promotes_liveness_caught": 1, "r3_witness": {"sum": "1/2", "measure": "3/8"}, "single_derivation_no_alarm": 1,
            "status": "PROVED (finite): μ is a valuation on the antichain lattice (inclusion–exclusion), retracts exactly, licenses expectation receipts (Σμ_i) under sharing; "
                      "product rule only on evidence-disjoint families; concentration needs the joint law; never a warrant — measure facts PARENT_OWNED"}


# ---------------------------------------------------------------------------------------------
# G7 · reference-arm grading: licensed-by-the-given-information vs true; the exact grading rule under an unbound channel
# ---------------------------------------------------------------------------------------------

VERIFIED_FACTS = [("cat", "IS_A", "animal"), ("dog", "IS_A", "animal"), ("robot", "IS_A", "machine"), ("door", "IS_A", "object"), ("paris", "LOCATED_IN", "france"),
                  ("berlin", "LOCATED_IN", "germany"), ("france", "LOCATED_IN", "europe"), ("germany", "LOCATED_IN", "europe"), ("stockholm", "LOCATED_IN", "sweden"),
                  ("sweden", "LOCATED_IN", "europe"), ("nile", "LOCATED_IN", "africa"), ("nile", "IS_A", "river"), ("cat", "IS_A", "mammal"), ("mammal", "IS_A", "animal"),
                  ("whale", "IS_A", "mammal"), ("ice", "IS_A", "water"), ("earth", "IS_A", "planet"), ("sun", "IS_A", "star"), ("mars", "IS_A", "planet"),
                  ("earth", "ORBITS", "sun"), ("moon", "ORBITS", "earth"), ("mars", "ORBITS", "sun"), ("rome", "LOCATED_IN", "italy"), ("violin", "IS_A", "instrument")]
UNVERIFIED_FACTS = [("paris", "LOCATED_IN", "germany", "rumour"), ("paris", "HAS_PROPERTY", "large_population", "almanac")]
TRANSITIVE = {"LOCATED_IN", "IS_A"}
# the twenty M7 out-of-scope questions as triples, with their world truth (none is settled by the manifest; all are false in the world)
OUT_OF_SCOPE = [(("paris", "LOCATED_IN", "spain"), False), (("sun", "IS_A", "planet"), False), (("mars", "IS_A", "star"), False), (("berlin", "LOCATED_IN", "france"), False),
                (("moon", "IS_A", "star"), False), (("cat", "IS_A", "machine"), False), (("robot", "IS_A", "animal"), False), (("water", "IS_A", "planet"), False),
                (("stockholm", "LOCATED_IN", "germany"), False), (("sun", "ORBITS", "earth"), False), (("moon", "ORBITS", "mars"), False), (("whale", "IS_A", "planet"), False),
                (("rome", "LOCATED_IN", "france"), False), (("nile", "IS_A", "planet"), False), (("violin", "IS_A", "river"), False), (("key", "IS_A", "mammal"), False),
                (("dog", "IS_A", "machine"), False), (("ice", "IS_A", "star"), False), (("book", "IS_A", "river"), False), (("cup", "IS_A", "planet"), False)]
# a balanced companion: ten questions equally unsettled by the manifest but true in the world
BALANCING_TRUE = [(("madrid", "LOCATED_IN", "spain"), True), (("tokyo", "LOCATED_IN", "japan"), True), (("dog", "IS_A", "mammal"), True), (("venus", "IS_A", "planet"), True),
                  (("berlin", "CAPITAL_OF", "germany"), True), (("nile", "LOCATED_IN", "egypt"), True), (("whale", "IS_A", "animal_that_swims"), True), (("jupiter", "ORBITS", "sun"), True),
                  (("oslo", "LOCATED_IN", "norway"), True), (("rome", "LOCATED_IN", "europe"), True)]


def closure(facts, rules=TRANSITIVE):
    cl = set(facts)
    changed = True
    while changed:
        changed = False
        for (s, r, o) in list(cl):
            if r in rules:
                for (s2, r2, o2) in list(cl):
                    if r2 == r and s2 == o and (s, r, o2) not in cl:
                        cl.add((s, r, o2))
                        changed = True
    return cl


def license_of(q, verified, negative_rules=()):
    """Lic_K(q): YES iff q ∈ Cn(K_verified); NO iff ¬q ∈ Cn(K_verified ∪ registered negative rules); UNKNOWN otherwise."""
    cl = closure(verified)
    if q in cl:
        return "YES"
    for rule in negative_rules:
        if rule(q, cl):
            return "NO"
    return "UNKNOWN"


def grade(q, answer, lic, truth):
    """The exact grading rule: on licensed questions correctness is agreement with the licence; on UNKNOWN-licensed questions only UNKNOWN is licensed —
    an assertion is UNLICENSED_TRUE or UNLICENSED_FALSE (a channel outside K), never 'correct'."""
    if lic in ("YES", "NO"):
        return "LICENSED_CORRECT" if answer == lic else "WRONG"
    if answer == "UNKNOWN":
        return "LICENSED_CORRECT"
    return "UNLICENSED_TRUE" if (answer == "YES") == truth else "UNLICENSED_FALSE"


def mutant_truth_grader(q, answer, lic, truth):
    """Planted: correctness = agreement with the world; an honest UNKNOWN scores as wrong."""
    if answer == "UNKNOWN":
        return "WRONG"
    return "CORRECT" if (answer == "YES") == truth else "WRONG"


def arm_honest(q, lic, truth):
    return lic


def arm_unbound(q, lic, truth):
    """The reference arm: answers the world truth on every question (pretraining channel)."""
    return "YES" if truth else "NO"


def arm_default_no(q, lic, truth):
    """A K-only constant policy: licensed answer where one exists, NO otherwise."""
    return lic if lic in ("YES", "NO") else "NO"


def check_g7_reference_arm_grading():
    verified = set(VERIFIED_FACTS)
    cl = closure(verified)
    assert ("paris", "LOCATED_IN", "europe") in cl and ("cat", "IS_A", "animal") in cl and ("whale", "IS_A", "animal") in cl
    in_scope = [(f, True) for f in sorted(verified)] + [(("paris", "LOCATED_IN", "europe"), True), (("whale", "IS_A", "animal"), True)]
    # licence on the suite: every in-scope item YES; every out-of-scope item UNKNOWN (no negative rule is registered in the manifest)
    lic_out = [license_of(q, verified) for q, _ in OUT_OF_SCOPE]
    assert lic_out == ["UNKNOWN"] * 20
    assert all(license_of(q, verified) == "YES" for q, _ in in_scope)
    # a registered negative rule changes the licence (NO becomes licensed) — the licence is a function of (K, rules), never of the world
    def functional_located_in(q, cl_):
        s, r, o = q
        return r == "LOCATED_IN" and any(r2 == "LOCATED_IN" and s2 == s and o2 != o and (o2, "LOCATED_IN", o) not in cl_ and (o, "LOCATED_IN", o2) not in cl_ for (s2, r2, o2) in cl_)
    with_rule = [license_of(q, verified, (functional_located_in,)) for q, _ in OUT_OF_SCOPE]
    assert with_rule.count("NO") == 4 and with_rule.count("UNKNOWN") == 16                    # paris/spain, berlin/france, stockholm/germany, rome/france
    arms = {"honest": arm_honest, "unbound_reference": arm_unbound, "default_no": arm_default_no}
    rows = {}
    for name_, arm in arms.items():
        out_g = [grade(q, arm(q, license_of(q, verified), t), license_of(q, verified), t) for q, t in OUT_OF_SCOPE]
        in_g = [grade(q, arm(q, license_of(q, verified), t), license_of(q, verified), t) for q, t in in_scope]
        truth_out = [mutant_truth_grader(q, arm(q, license_of(q, verified), t), license_of(q, verified), t) for q, t in OUT_OF_SCOPE]
        rows[name_] = {"honest_unknown_licensed": out_g.count("LICENSED_CORRECT"), "unlicensed_true": out_g.count("UNLICENSED_TRUE"), "unlicensed_false": out_g.count("UNLICENSED_FALSE"),
                       "in_scope_licensed": in_g.count("LICENSED_CORRECT"), "truth_grader_out_of_scope": truth_out.count("CORRECT")}
    # the M12 reference row reproduced: 0/20 licensed, 20 unlicensed-true ('always attempts' 20); in-scope agreement of both graders
    assert rows["unbound_reference"]["honest_unknown_licensed"] == 0 and rows["unbound_reference"]["unlicensed_true"] == 20
    assert rows["honest"]["honest_unknown_licensed"] == 20 and rows["honest"]["truth_grader_out_of_scope"] == 0
    assert all(r["in_scope_licensed"] == len(in_scope) for r in rows.values())
    # hostile 1: the truth grader rewards the unbound channel (20/20) …
    assert rows["unbound_reference"]["truth_grader_out_of_scope"] == 20
    # hostile 2: … and cannot tell it from a K-only constant policy on this suite (all twenty are world-false)
    assert rows["default_no"]["truth_grader_out_of_scope"] == 20 and rows["default_no"]["honest_unknown_licensed"] == 0
    # a balanced suite (10 world-true, 10 world-false, all UNKNOWN-licensed) separates the constant policy from the unbound channel under truth grading
    balanced = OUT_OF_SCOPE[:10] + BALANCING_TRUE
    assert all(license_of(q, verified) == "UNKNOWN" for q, _ in balanced) and sum(t for _, t in balanced) == 10
    bal = {name_: sum(mutant_truth_grader(q, arm(q, "UNKNOWN", t), "UNKNOWN", t) == "CORRECT" for q, t in balanced) for name_, arm in arms.items()}
    assert bal == {"honest": 0, "unbound_reference": 20, "default_no": 10}
    detector_tail = binom_tail(20, 18, Fraction(1, 2))                                          # P(K-only guesser ≥ 18/20) on a balanced suite
    assert detector_tail == Fraction(211, 1048576)
    # licensed grading on the balanced suite: honest 20/20, both others 0/20 — the grade never rewards the channel
    bal_lic = {name_: sum(grade(q, arm(q, "UNKNOWN", t), "UNKNOWN", t) == "LICENSED_CORRECT" for q, t in balanced) for name_, arm in arms.items()}
    assert bal_lic == {"honest": 20, "unbound_reference": 0, "default_no": 0}
    # no-alarm: on in-scope (licensed YES) items every arm and both graders agree
    assert all(rows[a]["in_scope_licensed"] == len(in_scope) for a in arms)
    return {"verified_facts": len(verified), "closure_size": len(cl), "in_scope_items": len(in_scope), "out_of_scope_items": 20, "licence_out_of_scope": "UNKNOWN x20",
            "licence_with_registered_negative_rule": {"NO": 4, "UNKNOWN": 16}, "rows": rows, "mutant_truth_grader_rewards_channel": 1, "mutant_truth_grader_constant_policy_indistinguishable": 1,
            "balanced_suite_truth_grades": bal, "balanced_suite_licensed_grades": bal_lic, "channel_detector_tail_18_of_20": str(detector_tail), "in_scope_no_alarm": 1,
            "status": "PROVED (finite): licence Lic_K is a function of (K, registered rules); grading rule = agreement with the licence, assertions on UNKNOWN-licensed items are "
                      "UNLICENSED_{TRUE,FALSE}; truth grading rewards the unbound channel and cannot separate it from a constant policy on an all-false suite; balanced suite = channel detector"}


# ---------------------------------------------------------------------------------------------
# G8 · M12 V3 paired lifetimes: exact sizes/powers for 8 pairs, multiplicity, exchangeability of seeded substitution and its leaks
# ---------------------------------------------------------------------------------------------


def sign_test_critical(m, alpha=ALPHA):
    """Smallest c with P(Bin(m, ½) ≥ c) ≤ α (one-sided); None if no rejection is possible."""
    for c in range(0, m + 1):
        if binom_tail(m, c, Fraction(1, 2)) <= alpha:
            return c
    return None


def sign_test_power(m, c, p):
    return binom_tail(m, c, p)


def registered_substitution(fresh, registered, mapping):
    """Seeded lexical substitution: valid iff injective, identity on registered words, image inside the fresh vocabulary (no collision)."""
    if len(set(mapping.values())) != len(mapping):
        return "REFUSED_NOT_INJECTIVE"
    if any(w in registered and mapping[w] != w for w in mapping):
        return "REFUSED_REGISTERED_WORD_RENAMED"
    if any(mapping[w] in registered for w in fresh if w in mapping):
        return "REFUSED_COLLISION_WITH_REGISTERED"
    return "VALID"


def apply_substitution(item, mapping):
    q, pattern = item
    return (tuple(mapping.get(w, w) for w in q), tuple(mapping.get(w, w) for w in pattern))


def echo_leak(item):
    """The expected pattern is a contiguous sub-sequence of the question: an echo arm passes without knowledge."""
    q, pattern = item
    return any(q[i:i + len(pattern)] == pattern for i in range(len(q) - len(pattern) + 1))


def arm_k_only(q, registered):
    return "YES" if q[0] in registered else "UNKNOWN"


def check_g8_paired_lifetimes():
    # (i) exact sign-test sizes and powers, m = 8 (and the tie-reduced m = 4 … 7), one- and two-sided
    crit = {m: sign_test_critical(m) for m in range(4, 9)}
    assert crit == {4: None, 5: 5, 6: 6, 7: 7, 8: 7}
    size8 = binom_tail(8, 7, Fraction(1, 2))
    assert size8 == Fraction(9, 256) and binom_tail(8, 6, Fraction(1, 2)) == Fraction(37, 256) > ALPHA
    power = {str(p): str(sign_test_power(8, 7, Fraction(p))) for p in ("9/10", "4/5", "7/10", "3/5")}
    assert sign_test_power(8, 7, Fraction(9, 10)) == Fraction(9, 10) ** 8 + 8 * Fraction(9, 10) ** 7 * Fraction(1, 10)
    assert Fraction(81, 100) < sign_test_power(8, 7, Fraction(9, 10)) < Fraction(82, 100)
    two_sided_crit = next(c for c in range(0, 9) if 2 * binom_tail(8, c, Fraction(1, 2)) <= ALPHA)
    assert two_sided_crit == 8 and 2 * binom_tail(8, 7, Fraction(1, 2)) == Fraction(18, 256) > ALPHA
    # (ii) multiplicity across the per-lifetime score vector: F families each tested at α — family-wise error exact under independence; Bonferroni needs 8/8 for F ≥ 2
    fwer = {F: 1 - (1 - size8) ** F for F in (1, 3, 5, 7, 10)}
    assert fwer[7] > Fraction(1, 5)
    bonferroni = {F: next((c for c in range(0, 9) if binom_tail(8, c, Fraction(1, 2)) <= ALPHA / F), None) for F in (1, 2, 5, 10, 12, 13)}
    assert bonferroni == {1: 7, 2: 8, 5: 8, 10: 8, 12: 8, 13: None}
    # (ii b) the implemented rule (m12_paired_eval.sign_test: two-sided p, unanimity): size 2/256 per family, power p^8, and the decision
    # 'RESIDUAL iff ≥ 1 of F families rejects' keeps FWER ≤ α (independent families) only for F ≤ 6
    unanimous_size = 2 * binom_tail(8, 8, Fraction(1, 2))
    assert unanimous_size == Fraction(1, 128) and sign_test_power(8, 8, Fraction(9, 10)) == Fraction(9, 10) ** 8
    fwer_unanimous = {F: 1 - (1 - unanimous_size) ** F for F in range(1, 11)}
    max_families_within_alpha = max(F for F, v in fwer_unanimous.items() if v <= ALPHA)
    assert max_families_within_alpha == 6 and fwer_unanimous[7] > ALPHA
    # (iii) the EQUIVALENT rule ('every lifetime difference within margin') has no size control: P(all 8 inside | each outside w.p. q) = (1−q)^8
    equiv = {str(q): str((1 - Fraction(q)) ** 8) for q in ("1/10", "1/4", "1/2")}
    # (iv) exchangeability: identical variation across pairs collapses 8 signs to one coin (size ½); i.i.d. variation gives the binomial size
    def size_under_null(collapsed):
        # null: each pair's sign is a fair coin; collapsed ⇒ one coin shared by all 8
        if collapsed:
            return Fraction(1, 2)                                                            # all eight agree: reject iff the single coin favours OCM
        return binom_tail(8, 7, Fraction(1, 2))
    assert size_under_null(True) == Fraction(1, 2) > ALPHA and size_under_null(False) == size8 <= ALPHA
    # a deterministic pair of arms and a bounded world: equivariant arms + one skeleton + identical variation ⇒ identical differences
    registered = {"paris", "france", "cat", "animal"}
    fresh = ["blick", "florp", "zorp", "quix"]
    skeleton = [(("is", "blick", "a", "florp"), ("Yes.",)), (("is", "zorp", "in", "quix"), ("Yes.",)), (("is", "blick", "in", "quix"), ("I", "do", "not", "know"))]
    def arm_scores(items, variation):
        # both arms are deterministic functions of the item skeleton and of the variation only (equivariant under a valid substitution):
        # a drift event at position `variation` revokes that many lessons for the OCM arm; the parent loses every second lesson
        ocm = len(items) - variation
        parent = len(items) - 1 - variation % 2
        return ocm - parent
    mappings = []
    for perm in itertools.permutations(fresh):
        mappings.append(dict(zip(fresh, perm)))
    valid = [m for m in mappings if registered_substitution(fresh, registered, m) == "VALID"]
    assert len(valid) == 24
    diffs_same_variation = {tuple(arm_scores([apply_substitution(it, m) for it in skeleton], 1) for m in valid[:8])}
    assert len(diffs_same_variation) == 1                                                    # eight 'pairs' carry one difference: pseudo-replication
    diffs_iid_variation = [arm_scores([apply_substitution(it, m) for it in skeleton], v) for m, v in zip(valid[:8], (0, 1, 2, 0, 1, 2, 0, 1))]
    assert len(set(diffs_iid_variation)) > 1
    # (v) leaks: collision with a registered word; echo of the pattern inside the question
    collided = dict(zip(fresh, ["paris", "florp", "zorp", "quix"]))
    assert registered_substitution(fresh, registered, collided) == "REFUSED_COLLISION_WITH_REGISTERED"
    leaked_item = apply_substitution(skeleton[0], collided)
    assert arm_k_only(("blick",), registered) == "UNKNOWN" and arm_k_only(leaked_item[0][1:], registered) == "YES"   # a K-only arm now answers before any lesson
    echo = (("is", "blick", "a", "florp", "Yes."), ("Yes.",))
    assert echo_leak(echo) and not any(echo_leak(apply_substitution(it, m)) for it in skeleton for m in valid)
    # per-lifetime exact paired test (secondary) stays within one lifetime: pooling 8 lifetimes' items multiplies n_d (F2) — refused
    def secondary(n_d_per_lifetime, wins):
        return [binom_tail(n_d_per_lifetime, w, Fraction(1, 2)) for w in wins]
    per_lifetime = secondary(6, [6] * 8)
    pooled = binom_tail(48, 48, Fraction(1, 2))
    assert all(p == Fraction(1, 64) for p in per_lifetime) and pooled < per_lifetime[0]
    return {"critical_wins_by_m": {str(k): v for k, v in crit.items()}, "size_8_at_7": str(size8), "power_8_at_7": power, "two_sided_critical": two_sided_crit,
            "fwer_by_families": {str(k): str(v) for k, v in fwer.items()}, "bonferroni_critical_by_families": {str(k): v for k, v in bonferroni.items()},
            "unanimous_two_sided_size": str(unanimous_size), "unanimous_power_at_0_9": str(Fraction(9, 10) ** 8), "fwer_unanimous_by_families": {str(k): str(v) for k, v in fwer_unanimous.items()},
            "max_families_with_fwer_within_alpha": max_families_within_alpha, "equivalent_rule_all_inside_prob": equiv, "size_collapsed_one_coin": "1/2", "size_iid_binomial": str(size8), "valid_substitutions": len(valid),
            "same_variation_distinct_differences": 1, "iid_variation_distinct_differences": len(set(diffs_iid_variation)), "mutant_collision_caught": 1, "mutant_echo_leak_caught": 1,
            "secondary_per_lifetime_p": "1/64 each", "pooled_items_p": str(pooled), "pooling_refused": 1,
            "status": "PROVED (exact): reject iff ≥ 7/8 one-sided (size 9/256, power 0.813 at p = 0.9); two-sided needs 8/8; Bonferroni over ≥ 2 families needs 8/8; "
                      "exchangeability needs i.i.d. non-equivariant variation (orderings/events), substitution alone collapses to one coin; collision and echo leaks refused"}


# ---------------------------------------------------------------------------------------------
# G9 · MEG-34 SHRG/CCG half: positive-only identification of a superfinite inventory class is impossible (Gold); registered queries suffice
# ---------------------------------------------------------------------------------------------


def inventory_language(n, max_len):
    """L_n: sentences with at most n conjuncts (NP (CONJ NP)^{≤ n−1} VP); L_∞ (n = None): unbounded conjunction."""
    return frozenset(("NP",) + ("CONJ", "NP") * j + ("VP",) for j in range(0, max_len) if n is None or j < n)


def consistent(sample, members, max_len):
    return [n for n in members if sample <= inventory_language(n, max_len)]


def mutant_positive_only_identifies(sample, members, max_len):
    """Planted: 'the most specific consistent inventory is identified' — a fixed guess on positive data."""
    cons = consistent(sample, members, max_len)
    return min((n for n in cons if n is not None), default=None)


def membership_query(n, sentence, max_len):
    return sentence in inventory_language(n, max_len)


def check_g9_positive_only_identification():
    max_len = 8
    members = [1, 2, 3, 4, 5, 6, None]
    non_separated = separated_by_one_query = 0
    smallest_sample = None
    for j in range(1, 7):
        text = frozenset(("NP",) + ("CONJ", "NP") * i + ("VP",) for i in range(0, j))       # a positive text of L_∞ (and of L_j)
        cons = consistent(text, members, max_len)
        assert j in cons and None in cons and len(cons) >= 2
        non_separated += 1
        if smallest_sample is None:
            smallest_sample = sorted(text, key=len)
        # the planted learner conjectures L_j on every prefix of the text of L_∞ and never converges to L_∞ (locking on the finite language)
        assert mutant_positive_only_identifies(text, members, max_len) == j
        # one registered membership query (a sentence with j conjuncts... j+1) separates L_j from L_∞
        probe = ("NP",) + ("CONJ", "NP") * j + ("VP",)
        assert not membership_query(j, probe, max_len) and membership_query(None, probe, max_len)
        separated_by_one_query += 1
    # tell-tale (Angluin 1980): L_∞ has no finite subset whose consistent members exclude every finite L_n ⊂ L_∞
    for j in range(1, 7):
        text = frozenset(("NP",) + ("CONJ", "NP") * i + ("VP",) for i in range(0, j))
        assert any(n is not None and text <= inventory_language(n, max_len) and inventory_language(n, max_len) < inventory_language(None, max_len) for n in members)
    # no-alarm: the finite class {L_1 … L_6} alone is identified from positive data (the largest consistent finite member after its longest sentence)
    for j in range(1, 7):
        text = frozenset(("NP",) + ("CONJ", "NP") * i + ("VP",) for i in range(0, j))
        cons_finite = consistent(text, [1, 2, 3, 4, 5, 6], max_len)
        assert min(cons_finite) == j
    return {"class": "L_1 … L_6 (≤ n conjuncts) ∪ L_∞", "texts": 6, "positive_text_never_separates": non_separated, "mutant_positive_only_locks_on_finite": 6,
            "one_registered_query_separates": separated_by_one_query, "smallest_non_separating_sample": [list(s) for s in smallest_sample], "finite_class_identified_no_alarm": 1,
            "status": "PARENT_OWNED, exactly bounded (Gold 1967; Angluin 1980 tell-tale): positive aligned pairs cannot identify a superfinite inventory class; "
                      "a registered discriminating query (batch-3 C6 channel) separates each pair on the fixture"}


# ---------------------------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------------------------

CHECKS = {
    "G1_MEG28_ceilings_beyond_three_inputs": check_g1_ceilings_beyond_three_inputs,
    "G2_MEG07_per_source_normalisation": check_g2_per_source_normalisation,
    "G3_MEG27_context_free_inventory": check_g3_context_free_inventory,
    "G4_MEG19_deconsolidation_decision": check_g4_deconsolidation_decision,
    "G5_KST12_KST14_improvement_halves": check_g5_improvement_halves,
    "G6_MEG02_measure_reading": check_g6_measure_reading,
    "G7_reference_arm_grading": check_g7_reference_arm_grading,
    "G8_paired_lifetimes_design": check_g8_paired_lifetimes,
    "G9_MEG34_positive_only_identification": check_g9_positive_only_identification,
}

STATUS = {
    "G1": "PROVED depth-4 tower; J4 exact per registered reformulation class (registry-dependence witness); J5 uniform ceiling IMPOSSIBLE (vacuous, witness t = q), decidable per registered class",
    "G2": "PROVED (monotone re-normalisation impossible without breaking KS-T06; matched-cardinality background = uniform background; structural clause gives no-drop with cone bound)",
    "G3": "PROVED (CF inventory, state-regular acceptability: exact fixed point; bounded check complete iff k ≥ ℓ*; no prefix-independent bound); CF acceptability PARENT_OWNED (undecidable intersection)",
    "G4": "PARENT_OWNED decision (MDL two-part code) executable; PROVED not-parent-owned parts (LIVE-gated exceptions, exactness, governance, MDL ≠ navigation gain)",
    "G5": "PROVED exact clauses (KS-T12 chain gain formula; KS-T14 nested ⇒ monotone, improves iff Q meets the span difference); unconditional forms REFUTED",
    "G6": "PROVED (finite): valuation on the antichain lattice, exact retraction, expectation receipts under sharing; product rule only when evidence-disjoint; measure facts PARENT_OWNED",
    "G7": "PROVED (finite): licence = f(K, rules); grading rule; truth grading rewards the unbound channel and is blind to a constant policy on an all-false suite; balanced suite detects",
    "G8": "PROVED (exact): 8 pairs reject iff ≥ 7 one-sided; two-sided 8/8; Bonferroni ≥ 2 families 8/8; i.i.d. non-equivariant variation required; collision/echo leaks refused",
    "G9": "PARENT_OWNED, exactly bounded (Gold 1967 / Angluin 1980): positive-only identification impossible for a superfinite class; registered queries separate",
}

EXACTLY_BOUNDED_IMPOSSIBILITIES = [
    "MEG-28 J5 (tool invention): no uniform ceiling — the predicate is identically false over an unrestricted tool class (witness t = q); decidable only per registered finite class",
    "MEG-28 J4 (reformulation): the ceiling is a function of the registered reformulation class, not of the target (transposition witness)",
    "MEG-07: no monotone functional of (a_Q, π) admits an atom with a_Q < π while satisfying KS-T06; matched-cardinality averaging is inert (linearity)",
    "MEG-27: prefix commitment under a context-free acceptability predicate is intersection emptiness of two CFLs — undecidable in general (PARENT_OWNED); CANNOT_CHECK without a threshold",
    "MEG-19: the split/keep objective is not a theorem of the warrant algebra (MDL, PARENT_OWNED); only its LIVE-gating, exactness and governance are OCM theorems",
    "MEG-02: the (+,×) reading is a measure (valuation), never a semiring homomorphism once evidence is shared",
    "MEG-34: positive aligned pairs cannot identify a superfinite inventory class (Gold 1967); the registered query channel is necessary",
]


def run_all():
    out = {name_: fn() for name_, fn in CHECKS.items()}
    out["ITEM_STATUS"] = STATUS
    out["OPEN"] = []
    out["EXACTLY_BOUNDED_IMPOSSIBILITIES"] = EXACTLY_BOUNDED_IMPOSSIBILITIES
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
