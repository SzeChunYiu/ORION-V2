"""Exact finite checker for KSO_THREE_VALUED_WARRANT_AND_REOPENING_V1.md (stdlib only).

Checks, with exact rational arithmetic and exhaustive enumeration where stated:
  KS-T21  three-valued liveness on warrant intervals is a Kleene homomorphism (n = 3 exhaustive);
  §1.3    the completeness-bit composite reads UNKNOWN where ∧₃ says DEAD (planted counterexample);
  KS-T04c prune–solve equivalence on the two-head witness, including the head-share clause, with
          the head-renormalising mutant shown to differ;
  KS-T22  reopening report on the eight-atom witness (REOPEN / RECHECK / UNAFFECTED; no-op; cycle),
          with the one-hop mutant shown to differ.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction

# ---------------------------------------------------------------------------------------------
# warrant antichains (KS-T01 objects) and intervals
# ---------------------------------------------------------------------------------------------


class CannotCheck(RuntimeError):
    pass


def canon(items):
    unique = {frozenset(w) for w in items}
    return tuple(sorted((w for w in unique if not any(v < w for v in unique)), key=lambda w: (len(w), sorted(w))))


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


def leq(p, q):  # P ≤ Q ⇔ every warrant of P contains a warrant of Q
    return all(any(w2 <= w1 for w2 in q) for w1 in p)


LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


def kand(a, b):
    return DEAD if DEAD in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else LIVE)


def kor(a, b):
    return LIVE if LIVE in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else DEAD)


def liveness(interval, r):
    lo, up = interval
    if live(lo, r):
        return LIVE
    if not live(up, r):
        return DEAD
    return UNKNOWN


def imeet(p, q):
    return (meet(p[0], q[0]), meet(p[1], q[1]))


def ijoin(p, q):
    return (join(p[0], q[0]), join(p[1], q[1]))


def all_profiles(n):
    subsets = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(range(n), k)]
    out = set()
    for mask in range(1 << len(subsets)):
        out.add(canon([subsets[i] for i in range(len(subsets)) if mask & (1 << i)]))
    return sorted(out, key=lambda p: (len(p), [sorted(w) for w in p]))


def check_ks_t21(n=3):
    ps = all_profiles(n)
    revs = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(range(n), k)]
    intervals = [(lo, up) for lo in ps for up in ps if leq(lo, up)]
    hom = red = mono = 0
    for a in ps:
        for r in revs:
            v = liveness((a, a), r)
            assert v != UNKNOWN and (v == LIVE) == live(a, r)
            red += 1
    for p in intervals:
        for q in intervals:
            refines = leq(p[0], q[0]) and leq(q[1], p[1])
            for r in revs:
                lp, lq = liveness(p, r), liveness(q, r)
                assert liveness(imeet(p, q), r) == kand(lp, lq), (p, q, r)
                assert liveness(ijoin(p, q), r) == kor(lp, lq), (p, q, r)
                hom += 1
                if refines:
                    assert lp == lq or lp == UNKNOWN
                    mono += 1
    return {"profiles": len(ps), "intervals": len(intervals), "reduction_checks": red, "homomorphism_checks": hom, "refinement_checks": mono}


def check_completeness_bit_counterexample():
    """The single-bit composite: profile = meet, complete = both complete."""
    p_profile, p_complete = ZERO, False
    q_profile, q_complete = (frozenset({2}),), True
    r = frozenset({2})
    bit_value = LIVE if live(meet(p_profile, q_profile), r) else (DEAD if (p_complete and q_complete) else UNKNOWN)
    interval_value = liveness(imeet((ZERO, ONE), (q_profile, q_profile)), r)
    kleene = kand(liveness((ZERO, ONE), r), liveness((q_profile, q_profile), r))
    assert kleene == DEAD and interval_value == DEAD and bit_value == UNKNOWN
    return {"bit_reads": bit_value, "interval_reads": interval_value, "kleene": kleene, "counterexample_fires": 1}


# ---------------------------------------------------------------------------------------------
# minimal typed hypergraph with frozen-denominator navigation (KS-T04 objects)
# ---------------------------------------------------------------------------------------------


def nav_matrix(atoms, edges, revoked, *, prune=False, renormalize_heads=False):
    """atoms: {id: interval}; edges: list of (id, tails, heads, weight, head_weights, interval).
    Gated matrix with frozen denominators; if prune, dead heads are dropped (shares retained unless
    renormalize_heads, the planted mutant)."""
    ids = list(atoms)
    idx = {x: i for i, x in enumerate(ids)}
    n = len(ids)
    out = [[Fraction(0) for _ in ids] for _ in ids]
    denom = {x: Fraction(0) for x in ids}
    for _, tails, _, w, _, _ in edges:
        for t in tails:
            denom[t] += w
    lv = {x: liveness(atoms[x], revoked) == LIVE for x in ids}
    for _, tails, heads, w, hw, ew in edges:
        if liveness(ew, revoked) != LIVE or not all(lv[t] for t in tails):
            continue
        total = sum(hw, Fraction(0))
        shares = {h: Fraction(x) / total for h, x in zip(heads, hw)}
        if prune:
            shares = {h: s for h, s in shares.items() if lv[h]}
            if renormalize_heads and shares:
                tot = sum(shares.values(), Fraction(0))
                shares = {h: s / tot for h, s in shares.items()}
        for t in tails:
            if denom[t] == 0:
                continue
            for h, s in shares.items():
                if lv[h]:
                    out[idx[t]][idx[h]] += (w / denom[t]) * s
    return ids, out


def fixed_point(ids, p, seed, alpha):
    n = len(ids)
    a = [[Fraction(int(i == j)) - (1 - alpha) * p[j][i] for j in range(n)] for i in range(n)]
    b = [alpha * s for s in seed]
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        piv = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if piv is None:
            raise CannotCheck("singular")
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    return [row[-1] for row in aug]


def check_ks_t04c_head_share():
    one = (ONE, ONE)
    atoms = {"t": one, "h1": one, "h2": ((frozenset({0}),), (frozenset({0}),))}
    edges = [("e", ("t",), ("h1", "h2"), Fraction(1), (Fraction(1), Fraction(1)), one)]
    ids, gated = nav_matrix(atoms, edges, {0})
    _, pruned = nav_matrix(atoms, edges, {0}, prune=True)
    _, mutant = nav_matrix(atoms, edges, {0}, prune=True, renormalize_heads=True)
    assert gated == pruned and gated[0][1] == Fraction(1, 2) and mutant[0][1] == Fraction(1)
    seed = [Fraction(1), Fraction(0), Fraction(0)]
    fg, fp = fixed_point(ids, gated, seed, Fraction(1, 3)), fixed_point(ids, pruned, seed, Fraction(1, 3))
    assert fg == fp and fg[2] == 0
    # the retraction witness s→a→{b,z}→c→d
    atoms = {"s": one, "a": one, "b": ((frozenset({0}),), (frozenset({0}),)), "z": one, "c": one, "d": one}
    E = [("sa", ("s",), ("a",), Fraction(1), (Fraction(1),), one), ("ab", ("a",), ("b",), Fraction(1), (Fraction(1),), one), ("az", ("a",), ("z",), Fraction(1), (Fraction(1),), one),
         ("bc", ("b",), ("c",), Fraction(1), (Fraction(1),), one), ("zc", ("z",), ("c",), Fraction(1), (Fraction(1),), one), ("cd", ("c",), ("d",), Fraction(1), (Fraction(1),), one)]
    ids, g = nav_matrix(atoms, E, {0})
    _, p = nav_matrix(atoms, E, {0}, prune=True)
    assert g == p and sum(g[ids.index("a")], Fraction(0)) == Fraction(1, 2)
    seed = [Fraction(int(x == "s")) for x in ids]
    pre = fixed_point(ids, nav_matrix(atoms, E, set())[1], seed, Fraction(1, 3))
    post = fixed_point(ids, g, seed, Fraction(1, 3))
    assert post[ids.index("b")] == 0 and post[ids.index("z")] == pre[ids.index("z")] and post[ids.index("c")] < pre[ids.index("c")]
    return {"head_share_matrix_equal": 1, "head_share_fixed_point_equal": 1, "head_renormalising_mutant_differs": 1, "witness_matrix_equal": 1, "witness_unrelated_unchanged": 1}


# ---------------------------------------------------------------------------------------------
# reopening report (KS-T22)
# ---------------------------------------------------------------------------------------------


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


def check_ks_t22():
    one = (ONE, ONE)
    w0 = ((frozenset({0}),), (frozenset({0}),))
    w05 = ((frozenset({0}), frozenset({5})), (frozenset({0}), frozenset({5})))
    atoms = {"a": w0, "b": one, "c": one, "d": one, "e": w05, "x": one, "y": one, "z": one}
    dep = [(("a",), ("b",)), (("b",), ("c",)), (("c",), ("d",)), (("a",), ("e",)), (("x",), ("y",)), (("y",), ("x",)), (("b", "z"), ("d",))]

    def report(r0, r1):
        changed = frozenset(x for x, iv in atoms.items() if liveness(iv, r0) != liveness(iv, r1))
        cone = impact_cone(changed, dep)
        return changed, cone, cone & changed, cone - changed, frozenset(atoms) - cone

    changed, cone, reopen, recheck, unaffected = report(set(), {0})
    assert changed == {"a"} and cone == {"a", "b", "c", "d", "e"} and reopen == {"a"} and recheck == {"b", "c", "d", "e"} and unaffected == {"x", "y", "z"}
    assert impact_cone({"x"}, dep) == {"x", "y"}
    assert report(set(), {9})[1] == frozenset()
    assert report(set(), {0, 5})[0] == {"a", "e"}
    one_hop = {"a"} | {h for tails, heads in dep if "a" in tails for h in heads}
    assert "c" not in one_hop and "c" in cone
    return {"reopen": sorted(reopen), "recheck": sorted(recheck), "unaffected": sorted(unaffected), "cycle_handled": 1, "irrelevant_noop": 1, "one_hop_mutant_differs": 1}


def run_all():
    return {"KS-T21": check_ks_t21(3), "completeness_bit_counterexample": check_completeness_bit_counterexample(), "KS-T04c": check_ks_t04c_head_share(), "KS-T22": check_ks_t22(), "NOVELTY": "NOT_ESTABLISHED"}


def main(argv=None):
    try:
        out = run_all()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except AssertionError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
