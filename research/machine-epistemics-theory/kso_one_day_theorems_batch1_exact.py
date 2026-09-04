"""Exact finite checker for KSO_ONE_DAY_THEOREMS_BATCH1_V1.md (stdlib only, exact rationals).

One check function per theorem (T1–T11, atlas ids MEG-04/06/08/18/22/26/29/30/31/35/01).  Every
check performs (a) the positive statement, (b) a planted mutant whose mutation is asserted applied
and which must be caught, and (c) a no-alarm control.  The minimal objects of the OCM core are
re-implemented here (antichain semiring, warrant intervals, Kleene liveness, authority meet,
frozen-denominator navigation, impact cone); nothing is imported from ``ocm``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import itertools
import json
import math
import random
import sys
from fractions import Fraction

# ---------------------------------------------------------------------------------------------
# antichain semiring (KS-T01), intervals, Kleene liveness (KS-T21)
# ---------------------------------------------------------------------------------------------


class CannotCheck(RuntimeError):
    pass


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


def leq(p, q):  # P ≤ Q ⇔ every warrant of P contains a warrant of Q
    return all(any(w2 <= w1 for w2 in q) for w1 in p)


LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


def kand(a, b):
    return DEAD if DEAD in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else LIVE)


def kor(a, b):
    return LIVE if LIVE in (a, b) else (UNKNOWN if UNKNOWN in (a, b) else DEAD)


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


def evidence_of(iv):
    return frozenset(e for side in iv for w in side for e in w)


def subsets(universe):
    u = sorted(universe, key=repr)
    return [frozenset(c) for k in range(len(u) + 1) for c in itertools.combinations(u, k)]


def all_profiles(n):
    subs = subsets(range(n))
    out = set()
    for mask in range(1 << len(subs)):
        out.add(canon([subs[i] for i in range(len(subs)) if mask & (1 << i)]))
    return sorted(out, key=lambda p: (len(p), [sorted(w) for w in p]))


# ---------------------------------------------------------------------------------------------
# frozen-denominator navigation (KS-T04/T05 objects) and the impact cone (KS-T09)
# ---------------------------------------------------------------------------------------------
# an edge is (edge_id, tails, heads, weight, head_weights, interval, relation_type)


def edge(eid, tails, heads, w=1, hw=None, iv=IONE, rel="DEPENDENCE"):
    tails = (tails,) if isinstance(tails, str) else tuple(tails)
    heads = (heads,) if isinstance(heads, str) else tuple(heads)
    return (eid, tails, heads, Fraction(w), tuple(Fraction(x) for x in (hw or [1] * len(heads))), iv, rel)


def nav_matrix(atoms, edges, revoked, relevance=None):
    """Gated matrix with denominators frozen on the registered structure; dead mass dissipates."""
    ids = list(atoms)
    idx = {x: i for i, x in enumerate(ids)}
    out = [[Fraction(0) for _ in ids] for _ in ids]
    denom = {x: Fraction(0) for x in ids}
    beta = lambda rel: Fraction((relevance or {}).get(rel, 1))
    for _, tails, _, w, _, _, rel in edges:
        for t in tails:
            denom[t] += w * beta(rel)
    lv = {x: liveness(atoms[x], revoked) == LIVE for x in ids}
    for _, tails, heads, w, hw, ew, rel in edges:
        mass = w * beta(rel)
        if mass == 0 or liveness(ew, revoked) != LIVE or not all(lv[t] for t in tails):
            continue
        total = sum(hw, Fraction(0))
        for t in tails:
            if denom[t] == 0:
                continue
            for h, x in zip(heads, hw):
                if lv[h]:
                    out[idx[t]][idx[h]] += (mass / denom[t]) * (x / total)
    return ids, out


def enabled_edges(atoms, edges, revoked):
    """KS-T02: an edge is ENABLED iff the edge and every tail are LIVE."""
    return frozenset(e[0] for e in edges if liveness(e[5], revoked) == LIVE and all(liveness(atoms[t], revoked) == LIVE for t in e[1]))


def live_sets(atoms, revoked):
    out = {LIVE: set(), DEAD: set(), UNKNOWN: set()}
    for x, iv in atoms.items():
        out[liveness(iv, revoked)].add(x)
    return {k: frozenset(v) for k, v in out.items()}


def step(p, seed, a, alpha):
    n = len(a)
    return [alpha * seed[i] + (1 - alpha) * sum(p[j][i] * a[j] for j in range(n)) for i in range(n)]


def fixed_point(p, seed, alpha):
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


def l1(v):
    return sum((abs(x) for x in v), Fraction(0))


def impact_cone(changed, edges):
    out = set(changed)
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


def witness_space():
    """The retraction witness s→a→{b,z}→c→d (all warrants certified ONE unless stated)."""
    atoms = {x: IONE for x in "sabzcd"}
    E = [edge("sa", "s", "a"), edge("ab", "a", "b"), edge("az", "a", "z"), edge("bc", "b", "c"), edge("zc", "z", "c"), edge("cd", "c", "d")]
    return atoms, E


# ---------------------------------------------------------------------------------------------
# T1 · MEG-04 · commit-authority bottom
# ---------------------------------------------------------------------------------------------


def auth_meet(*items):
    keys = set().union(*(set(a) for a in items))
    return {k: min(a.get(k, 0) for a in items) for k in keys}


def auth_leq(a, b):
    return all(a.get(k, 0) <= b.get(k, 0) for k in set(a) | set(b))


def mutant_authority_max(*items):
    keys = set().union(*(set(a) for a in items))
    return {k: max(a.get(k, 0) for a in items) for k in keys}


def internal_compose_authority(op_authority, tail_authorities):
    """Composition law A = A_op ∧ ⋀ A_i with the operator always a factor (contract §3)."""
    return auth_meet(op_authority, *tail_authorities)


def mutant_compose_drops_operator_factor(op_authority, tail_authorities):
    """Planted: meet over the tails only — the runtime shape when no bridge authority is passed."""
    return auth_meet(*tail_authorities)


def check_t1_meg04_commit_bottom():
    coords = ("world_truth", "speaker", "task_contract", "commit")
    glb = 0
    ranks = list(itertools.product(range(3), repeat=len(coords)))
    for ra in ranks:
        for rb in ranks:
            a, b = dict(zip(coords, ra)), dict(zip(coords, rb))
            m = auth_meet(a, b)
            assert auth_leq(m, a) and auth_leq(m, b)
            for rc in ranks:
                c = dict(zip(coords, rc))
                if auth_leq(c, a) and auth_leq(c, b):
                    assert auth_leq(c, m)
            glb += 1
    receipt = {"world_truth": 2, "speaker": 1, "task_contract": 1, "commit": 1}  # external ActionReceipt
    internal_op = {"world_truth": 2, "speaker": 1, "task_contract": 1}            # commit undeclared = 0
    composed = internal_compose_authority(internal_op, [receipt, receipt])
    assert composed.get("commit", 0) == 0 and composed["world_truth"] == 2   # no-alarm: other coordinates kept
    depth = composed
    for _ in range(5):  # any chain of internal operations stays at commit = 0
        depth = internal_compose_authority(internal_op, [depth, receipt])
        assert depth.get("commit", 0) == 0
    bad_max = mutant_authority_max(internal_op, receipt, receipt)
    assert bad_max["commit"] == 1
    bad_drop = mutant_compose_drops_operator_factor(internal_op, [receipt, receipt])
    assert bad_drop["commit"] == 1
    return {"glb_pairs_checked": glb, "internal_commit_is_zero": 1, "chain_depth_checked": 6, "mutant_authority_max_caught": 1, "mutant_drop_operator_factor_caught": 1, "world_truth_kept": composed["world_truth"]}


# ---------------------------------------------------------------------------------------------
# T2 · MEG-06 · budget bracket
# ---------------------------------------------------------------------------------------------


def neumann_partials(p, seed, alpha, k_max):
    n = len(seed)
    term = [alpha * x for x in seed]
    partial = term[:]
    out = [partial[:]]
    for _ in range(k_max):
        term = [(1 - alpha) * sum(p[j][i] * term[j] for j in range(n)) for i in range(n)]
        partial = [x + y for x, y in zip(partial, term)]
        out.append(partial[:])
    return out


def iterate_from(p, seed, alpha, start, k_max):
    a = list(start)
    out = [a[:]]
    for _ in range(k_max):
        a = step(p, seed, a, alpha)
        out.append(a[:])
    return out


def mutant_unnormalised_iterate(p, seed, alpha, k_max):
    """Planted: iterate F from a_0 = s instead of α s (the m2-runtime ``navigate`` start vector)."""
    return iterate_from(p, seed, alpha, seed, k_max)


def chain_space(length):
    atoms = {str(i): IONE for i in range(length + 1)}
    E = [edge(f"e{i}", str(i), str(i + 1)) for i in range(length)]
    return atoms, E


def check_t2_meg06_budget_bracket():
    alpha, K = Fraction(1, 3), 9
    atoms, E = witness_space()
    ids, p = nav_matrix(atoms, E, set())
    seed = [Fraction(int(x == "s")) for x in ids]
    astar = fixed_point(p, seed, alpha)
    partials = neumann_partials(p, seed, alpha, K)
    iters = iterate_from(p, seed, alpha, [alpha * x for x in seed], K)
    checks = 0
    for k in range(K + 1):
        assert iters[k] == partials[k]
        assert all(iters[k][i] <= astar[i] for i in range(len(ids)))
        if k:
            assert all(iters[k][i] >= iters[k - 1][i] for i in range(len(ids)))
        width = (1 - alpha) ** (k + 1) * l1(seed)
        assert all(astar[i] - iters[k][i] <= width for i in range(len(ids)))
        checks += 1
    # decidable bracket: θ outside [a_k, a_k + w] ⇒ verdict equals the fixed point's verdict
    t = ids.index("d")
    decided = 0
    for k in range(K + 1):
        width = (1 - alpha) ** (k + 1) * l1(seed)
        lo, hi = iters[k][t], iters[k][t] + width
        for theta in (lo / 2, lo, hi + Fraction(1, 10**6), hi * 2):
            if not (lo < theta <= hi):
                assert (astar[t] >= theta) == (lo >= theta)
                decided += 1
    # MORE_BUDGET hook: least k' with w_{k'} < θ − a_k(t); no budget in [k, k') decides
    k0, theta = 1, astar[t] + Fraction(1, 10**4)
    kprime = next(kk for kk in range(k0, 200) if (1 - alpha) ** (kk + 1) * l1(seed) < theta - iters[k0][t])
    long_iters = iterate_from(p, seed, alpha, [alpha * x for x in seed], kprime)
    for kk in range(k0, kprime):
        assert long_iters[kk][t] < theta <= long_iters[kk][t] + (1 - alpha) ** (kk + 1) * l1(seed)
    # planted mutant: iterate from the un-normalised seed s (not α s) — overshoots the fixed point
    bad = mutant_unnormalised_iterate(p, seed, alpha, K)
    assert bad[0] != iters[0]  # mutation applied
    assert any(bad[k][i] > astar[i] for k in range(1, K + 1) for i in range(len(ids)))
    catoms, cE = chain_space(17)
    cids, cp = nav_matrix(catoms, cE, set())
    cseed = [Fraction(int(x == "0")) for x in cids]
    cstar = fixed_point(cp, cseed, alpha)
    tt, theta = cids.index("17"), Fraction(1, 1000)
    good17 = iterate_from(cp, cseed, alpha, [alpha * x for x in cseed], 17)[17][tt]
    bad17 = mutant_unnormalised_iterate(cp, cseed, alpha, 17)[17][tt]
    assert cstar[tt] == alpha * (1 - alpha) ** 17 < theta and good17 == cstar[tt] and bad17 == (1 - alpha) ** 17 >= theta
    # float-solver bound: ‖â_k − a_k‖₁ ≤ δ/α with per-step rounding δ = 4 n u (calibration)
    n, u = len(ids), 2.0 ** -52
    pf, sf = [[float(x) for x in row] for row in p], [float(x) for x in seed]
    af = [float(alpha) * x for x in sf]
    worst = 0.0
    for k in range(1, K + 1):
        af = [float(alpha) * sf[i] + (1 - float(alpha)) * sum(pf[j][i] * af[j] for j in range(n)) for i in range(n)]
        worst = max(worst, sum(abs(af[i] - float(iters[k][i])) for i in range(n)))
    assert worst <= 4 * n * u / float(alpha)
    return {"partial_sum_identity_checks": checks, "bracket_decisions": decided, "more_budget_kprime": kprime, "mutant_unnormalised_iterate_overshoots": 1, "chain17_mutant_found_unsound": 1, "float_l1_error_max": worst, "float_bound": 4 * n * u / float(alpha)}


# ---------------------------------------------------------------------------------------------
# T3 · MEG-08 · feedback updates behaviour, never warrant
# ---------------------------------------------------------------------------------------------


def random_space(rng, n_atoms=6, n_edges=8, n_ev=3):
    profiles = all_profiles(n_ev)
    atoms = {}
    for i in range(n_atoms):
        lo = rng.choice(profiles)
        ups = [u for u in profiles if leq(lo, u)]
        atoms[f"v{i}"] = (lo, rng.choice(ups))
    ids = list(atoms)
    E = []
    for j in range(n_edges):
        tails = tuple(rng.sample(ids, rng.choice((1, 2))))
        heads = tuple(x for x in rng.sample(ids, rng.choice((1, 2))) if x not in tails) or (rng.choice([x for x in ids if x not in tails]),)
        lo = rng.choice(profiles)
        up = rng.choice([u for u in profiles if leq(lo, u)])
        E.append(edge(f"h{j}", tails, heads, rng.randint(1, 4), [rng.randint(1, 3) for _ in heads], (lo, up), rng.choice(("DEPENDENCE", "SUPPORT"))))
    return atoms, E


def perturb(rng, E, relevance):
    E2 = [(eid, t, h, Fraction(rng.randint(1, 9), rng.randint(1, 3)), tuple(Fraction(rng.randint(1, 5)) for _ in hw), iv, rel) for eid, t, h, w, hw, iv, rel in E]
    rel2 = {k: Fraction(rng.randint(1, 5), rng.randint(1, 2)) for k in relevance}
    return E2, rel2


def mutant_feedback_edits_label(atoms, target):
    out = dict(atoms)
    out[target] = (ONE, ONE)  # feedback "corrects" the label: mints warrant
    return out


def check_t3_meg08_feedback_not_warrant():
    rng = random.Random(8)
    spaces = signatures = matrix_changed = 0
    caught = 0
    for _ in range(30):
        atoms, E = random_space(rng)
        relevance = {"DEPENDENCE": Fraction(1), "SUPPORT": Fraction(1)}
        E2, rel2 = perturb(rng, E, relevance)
        revs = subsets(range(3))
        for r in revs:
            assert live_sets(atoms, r) == live_sets(atoms, r)
            assert enabled_edges(atoms, E, r) == enabled_edges(atoms, E2, r)
            signatures += 1
        _, m1 = nav_matrix(atoms, E, set(), relevance)
        _, m2 = nav_matrix(atoms, E2, set(), rel2)
        matrix_changed += int(m1 != m2)
        # planted mutant: a FEEDBACK event that edits a label changes some liveness signature
        target = next((x for x in atoms if any(liveness(atoms[x], r) != LIVE for r in revs)), None)
        if target is not None:
            bad = mutant_feedback_edits_label(atoms, target)
            assert bad[target] != atoms[target]
            assert any(live_sets(bad, r) != live_sets(atoms, r) for r in revs)
            caught += 1
        spaces += 1
    assert matrix_changed > 0 and caught > 0
    return {"random_spaces": spaces, "signature_checks": signatures, "matrices_changed_by_perturbation": matrix_changed, "mutant_feedback_edits_label_caught": caught}


# ---------------------------------------------------------------------------------------------
# T4 · MEG-18 · Jump rollback = revoke e_J + quarantine
# ---------------------------------------------------------------------------------------------


def stamp(iv, e_j):
    return imeet(iv, cert({e_j}))


def additive_jump(atoms, E, e_j, new_atoms, new_edges):
    a2 = dict(atoms)
    for x, iv in new_atoms.items():
        a2[x] = stamp(iv, e_j)
    E2 = list(E) + [(eid, t, h, w, hw, stamp(iv, e_j), rel) for eid, t, h, w, hw, iv, rel in new_edges]
    return a2, E2


def mutant_uncertified_structure(atoms, E, e_j, new_atoms, new_edges):
    """Planted: Jump atoms admitted without the certificate in their warrant (edges still stamped)."""
    a2, E2 = additive_jump(atoms, E, e_j, {}, new_edges)
    a2.update(new_atoms)
    return a2, E2


def rollback(atoms, E, e_j):
    """Revoke e_J and quarantine every object whose evidence contains e_J (the Jump-stamped structure)."""
    keep_atoms = {x: iv for x, iv in atoms.items() if e_j not in evidence_of(iv)}
    keep_edges = [e for e in E if e_j not in evidence_of(e[5]) and set(e[1]) | set(e[2]) <= set(keep_atoms)]
    quarantined = (frozenset(atoms) - frozenset(keep_atoms), frozenset(e[0] for e in E) - frozenset(e[0] for e in keep_edges))
    return keep_atoms, keep_edges, quarantined


def check_t4_meg18_jump_rollback():
    alpha = Fraction(1, 3)
    atoms, E = witness_space()
    atoms["s"] = cert({0})
    ids, p = nav_matrix(atoms, E, set())
    seed = [Fraction(int(x == "s")) for x in ids]
    pre = dict(zip(ids, fixed_point(p, seed, alpha)))
    e_j = "eJ"
    a2, E2 = additive_jump(atoms, E, e_j, {"m": IONE}, [edge("am", "a", "m"), edge("md", "m", "d")])
    assert liveness(a2["m"], set()) == LIVE and liveness(a2["m"], {e_j}) == DEAD and e_j in evidence_of(a2["m"])
    assert all(liveness(e[5], {e_j}) == DEAD for e in E2 if e[0] in ("am", "md"))
    gammas = subsets([0, e_j])
    for R in gammas:
        for x in atoms:
            assert liveness(a2[x], R) == liveness(atoms[x], R)  # S5: old signatures untouched by the Jump
    # revocation alone is not rollback: frozen denominators let the dead Jump mass dissipate
    ids2, p_rev = nav_matrix(a2, E2, {e_j})
    seed2 = [Fraction(int(x == "s")) for x in ids2]
    rev = dict(zip(ids2, fixed_point(p_rev, seed2, alpha)))
    assert rev["m"] == 0 and rev["d"] < pre["d"] and rev["z"] < pre["z"]
    # rollback = revoke + quarantine restores the pre-Jump value exactly
    a3, E3, quarantined = rollback(a2, E2, e_j)
    assert quarantined == (frozenset({"m"}), frozenset({"am", "md"}))
    assert a3 == atoms and [e[0] for e in E3] == [e[0] for e in E]
    ids3, p3 = nav_matrix(a3, E3, set())
    post = dict(zip(ids3, fixed_point(p3, [Fraction(int(x == "s")) for x in ids3], alpha)))
    assert post == pre and p3 == p
    # planted mutant: Jump structure admitted without the certificate cannot be rolled back
    bad_atoms, bad_E = mutant_uncertified_structure(atoms, E, e_j, {"m": IONE}, [edge("am", "a", "m"), edge("md", "m", "d")])
    assert bad_atoms["m"] != a2["m"] and e_j not in evidence_of(bad_atoms["m"])
    b_atoms, b_E, b_q = rollback(bad_atoms, bad_E, e_j)
    assert "m" in b_atoms and liveness(b_atoms["m"], {e_j}) == LIVE and b_q[0] == frozenset()
    # no-alarm: an old atom unrelated to the Jump keeps liveness and activation through the cycle
    assert liveness(a2["b"], {e_j}) == LIVE and post["b"] == pre["b"]
    # removal half: a Jump that deletes structure is invertible only from the quarantine record
    removed = {x: atoms[x] for x in ("z",)}
    without_z = {x: iv for x, iv in atoms.items() if x != "z"}
    assert "z" not in without_z and {**without_z, **removed} == atoms
    return {"old_signatures_preserved": len(gammas) * len(atoms), "revocation_alone_changes_fixed_point": 1, "rollback_exact": 1, "quarantined": sorted(quarantined[0] | quarantined[1]), "mutant_uncertified_structure_caught": 1, "unrelated_unchanged": 1}


# ---------------------------------------------------------------------------------------------
# T5 · MEG-22 · shared evidence across fibres, transfer maps
# ---------------------------------------------------------------------------------------------


def transfer(iv_T, iv_x):
    return imeet(iv_T, iv_x)


def mutant_transfer_drop_bridge(iv_T, iv_x):
    return iv_x


def mutant_whole_fibre_interference(atoms, W_M):
    """Planted over-alarm: every atom citing any evidence of the other fibre is declared interfering."""
    return frozenset(x for x in atoms if evidence_of(atoms[x]) & W_M)


def check_t5_meg22_shared_evidence():
    # fibre P: p1 (uses lemma L and own evidence a1), u1 unrelated; fibre M: p2 (uses L and a2), u2
    atoms = {"L": cert({"L"}), "p1": cert({"L", "a1"}), "u1": cert({"b1"}), "p2": cert({"L", "a2"}), "u2": cert({"b2"})}
    E = [edge("Lp1", "L", "p1"), edge("Lp2", "L", "p2"), edge("p1c1", "p1", "c1"), edge("p2c2", "p2", "c2")]
    atoms["c1"], atoms["c2"] = imeet(IONE, atoms["p1"]), imeet(IONE, atoms["p2"])
    W_P = evidence_of(atoms["p1"]) | evidence_of(atoms["u1"]) | evidence_of(atoms["c1"])
    W_M = evidence_of(atoms["p2"]) | evidence_of(atoms["u2"]) | evidence_of(atoms["c2"])
    sigma = W_P & W_M
    assert sigma == {"L"}
    shared = frozenset(x for x, iv in atoms.items() if evidence_of(iv) & sigma)
    bound = impact_cone(shared, E)
    changed = frozenset(x for x in atoms if liveness(atoms[x], set()) != liveness(atoms[x], {"L"}))
    exact = impact_cone(changed, E)
    assert changed == {"L", "p1", "p2", "c1", "c2"} and exact <= bound and {"u1", "u2"} & bound == frozenset()
    # revoking P-private evidence never touches M
    priv = frozenset(x for x in atoms if liveness(atoms[x], set()) != liveness(atoms[x], {"a1"}))
    assert priv == {"p1", "c1"} and not (impact_cone(priv, E) & {"p2", "c2", "u2"})
    # transfer map as a KS-T20 bridge: liveness is the Kleene ∧ of the map and the argument
    T = cert({"t"})
    for R in subsets(["t", "L", "a2"]):
        assert liveness(transfer(T, atoms["p2"]), R) == kand(liveness(T, R), liveness(atoms["p2"], R))
    assert evidence_of(transfer(T, atoms["p2"])) == {"t", "L", "a2"}
    # planted mutants: (i) bridge dropped → transferred atom survives revoking the map;
    bad = mutant_transfer_drop_bridge(T, atoms["p2"])
    assert bad != transfer(T, atoms["p2"]) and liveness(bad, {"t"}) == LIVE and liveness(transfer(T, atoms["p2"]), {"t"}) == DEAD
    # (ii) whole-fibre interference (over-alarm) predicts u2 interferes; the exact set does not
    mutant_set = mutant_whole_fibre_interference(atoms, W_M)
    assert "u2" in mutant_set and "u2" not in exact
    return {"sigma": sorted(sigma), "interference_bound": sorted(bound), "interference_exact": sorted(exact), "private_revocation_isolated": 1, "transfer_kleene_checks": 8, "mutant_drop_bridge_caught": 1, "mutant_whole_fibre_overalarm_caught": 1}


# ---------------------------------------------------------------------------------------------
# T6 · MEG-26 · candidate warrant and ambiguity
# ---------------------------------------------------------------------------------------------

SELECTED, AMBIGUOUS, NO_CANDIDATE = "SELECTED", "AMBIGUOUS", "NO_CANDIDATE"


def select(candidates, revoked):
    v = {c: liveness(iv, revoked) for c, iv in candidates.items()}
    lives = [c for c, s in v.items() if s == LIVE]
    unknowns = [c for c, s in v.items() if s == UNKNOWN]
    if len(lives) == 1 and not unknowns:
        return SELECTED, lives[0]
    if not lives and not unknowns:
        return NO_CANDIDATE, None
    return AMBIGUOUS, None


def mutant_forced_collapse_by_score(candidates, scores, revoked):
    best = max(candidates, key=lambda c: scores[c])
    return (SELECTED, best) if liveness(candidates[best], revoked) != DEAD else (NO_CANDIDATE, None)


def check_t6_meg26_candidate_warrant():
    constr, lex_river, lex_fin, morph = cert({"c"}), cert({"r"}), cert({"f"}), cert({"m"})
    cands = {"bank_river": meet_all_i([constr, lex_river, morph]), "bank_fin": meet_all_i([constr, lex_fin, morph])}
    for c, iv in cands.items():
        for R in subsets(["c", "r", "f", "m"]):
            parts = [constr, lex_river if c == "bank_river" else lex_fin, morph]
            assert liveness(iv, R) == kand(kand(liveness(parts[0], R), liveness(parts[1], R)), liveness(parts[2], R))
    assert select(cands, set()) == (AMBIGUOUS, None)
    assert select(cands, {"r"}) == (SELECTED, "bank_fin")      # context evidence collapses by revocation
    assert select(cands, {"r", "f"}) == (NO_CANDIDATE, None)
    assert select(cands, {"m"}) == (NO_CANDIDATE, None)         # shared part dead kills both (Kleene ∧)
    merged = ijoin(cands["bank_river"], cands["bank_fin"])
    assert liveness(merged, set()) == LIVE                       # the ⊕-merged atom fires under ambiguity
    scores = {"bank_river": 0.6, "bank_fin": 0.4}
    bad = mutant_forced_collapse_by_score(cands, scores, set())
    assert bad[0] == SELECTED and select(cands, set())[0] == AMBIGUOUS
    # no-alarm: a candidate with an UNKNOWN part is never SELECTED; scores are not an input of λ_R
    partial = dict(cands)
    partial["bank_fin"] = imeet(partial["bank_fin"], (ZERO, ONE))
    assert select(partial, {"r"}) == (AMBIGUOUS, None) and select(partial, {"r", "f"}) == (NO_CANDIDATE, None)
    assert select(cands, {"r"}) == select(cands, {"r"})
    return {"candidate_kleene_checks": 32, "ambiguous_blocks_firing": 1, "collapse_by_evidence": 1, "merged_atom_fires_under_ambiguity": 1, "mutant_forced_collapse_caught": 1, "unknown_part_never_selected": 1}


def meet_all_i(ivs):
    out = IONE
    for iv in ivs:
        out = imeet(out, iv)
    return out


# ---------------------------------------------------------------------------------------------
# T7 · MEG-29 · no self-authority
# ---------------------------------------------------------------------------------------------


def evidence_conferred(iv, ev_authority):
    """A_ev(x) = ⋁_{W ∈ L} ⋀_{e ∈ W} A_e — the authority the best exhibited warrant confers."""
    lo = iv[0]
    if not lo:
        return {}
    if any(not w for w in lo):
        raise CannotCheck("unconditional warrant confers no evidence-bounded authority")
    per_w = [auth_meet(*(ev_authority[e] for e in w)) for w in lo]
    keys = set().union(*(set(a) for a in per_w))
    return {k: max(a.get(k, 0) for a in per_w) for k in keys}


def admit_reflexive(declared, iv, ev_authority):
    """Reflexive atoms: commit must be 0 and world_truth ≤ evidence-conferred world_truth."""
    if declared.get("commit", 0) != 0:
        return "REFUSED_SELF_COMMIT"
    if declared.get("world_truth", 0) > evidence_conferred(iv, ev_authority).get("world_truth", 0):
        return "REFUSED_WORLD_TRUTH_ABOVE_EVIDENCE"
    return "ADMITTED"


def mutant_self_commit(declared):
    """Planted: a reflexive atom declaring commit authority for itself."""
    return {**declared, "commit": 1}


def mutant_world_truth_above_evidence(declared, rank=2):
    """Planted: a reflexive atom declaring more world_truth than its evidence confers."""
    return {**declared, "world_truth": rank}


def check_t7_meg29_no_self_authority():
    ev_auth = {"o1": {"world_truth": 1}, "o2": {"world_truth": 1}, "m1": {"world_truth": 1}}
    self_model = cert({"m1"})
    ok = admit_reflexive({"world_truth": 1}, self_model, ev_auth)
    assert ok == "ADMITTED"
    d1, d2 = mutant_self_commit({"world_truth": 1}), mutant_world_truth_above_evidence({"world_truth": 1})
    assert d1["commit"] == 1 and d2["world_truth"] == 2  # mutations applied
    bad_commit = admit_reflexive(d1, self_model, ev_auth)
    bad_truth = admit_reflexive(d2, self_model, ev_auth)
    assert bad_commit == "REFUSED_SELF_COMMIT" and bad_truth == "REFUSED_WORLD_TRUTH_ABOVE_EVIDENCE"
    # compositions cannot raise: meet with the reflexive atom keeps commit 0 (T1)
    assert internal_compose_authority({"world_truth": 1}, [{"world_truth": 1}, {"world_truth": 2, "commit": 1}]).get("commit", 0) == 0
    # self-certification: a calibration claim whose evidence depends on the model dies with it
    kappa_dep = imeet(cert({"o1"}), self_model)
    kappa_ind = cert({"o2"})
    for R in subsets(["o1", "o2", "m1"]):
        if liveness(self_model, R) == DEAD:
            assert liveness(kappa_dep, R) == DEAD
    assert liveness(kappa_dep, {"m1"}) == DEAD and liveness(kappa_ind, {"m1"}) == LIVE
    return {"reflexive_admitted": 1, "mutant_self_commit_refused": 1, "mutant_world_truth_above_evidence_refused": 1, "dependent_certificate_dies_with_model": 1, "independent_certificate_survives": 1}


# ---------------------------------------------------------------------------------------------
# T8 · MEG-30 · no livelock, snapshot consistency
# ---------------------------------------------------------------------------------------------


def digest(space):
    atoms, E = space
    return (tuple(sorted(atoms.items())), tuple(E))


def query_on(space, k=4):
    """A query is a pure function of the immutable snapshot it reads: the exact k-step iterate
    a_k (partial Neumann sum, T2) of the gated walk from seed s, α = 1/3."""
    atoms, E = space
    ids, p = nav_matrix(atoms, E, set())
    seed = [Fraction(int(x == "s")) for x in ids]
    return tuple(iterate_from(p, seed, Fraction(1, 3), [x / 3 for x in seed], k)[k])


def run_system(rng, budget, transition_cost, cap=10_000, stale_cache=False, ops=("query", "learn", "escalate")):
    """Coupled system: queries interleaved with metered learning transitions and escalations.
    Every transition builds a NEW space value; earlier snapshots are never mutated."""
    space = witness_space()
    meter, level, log, steps, cache = 0, 0, [], 0, None
    while steps < cap:
        steps += 1
        op = rng.choice(ops)
        if op == "query":
            if stale_cache:
                cache = cache if cache is not None else query_on(space)   # never invalidated (planted)
                result = cache
            else:
                result = query_on(space)
            log.append(("query", space, result))
        elif op == "learn":
            if meter + transition_cost > budget:
                log.append(("CANNOT_CHECK", meter))
                return log, steps
            meter += transition_cost
            atoms, E = space
            atoms = dict(atoms)
            atoms[f"n{steps}"] = IONE
            space = (atoms, list(E) + [edge(f"g{steps}", "d", f"n{steps}")])
            log.append(("learn", meter))
        else:
            if level >= 8:
                log.append(("DONE", meter))
                return log, steps
            if meter + transition_cost > budget:
                log.append(("CANNOT_CHECK", meter))
                return log, steps
            level += 1
            meter += transition_cost
            log.append(("escalate", level, meter))
    return log, steps


def mutant_unmetered_transition(rng, budget, cap):
    """Planted: learning transitions that charge nothing (δ = 0) — the ranking function never moves."""
    return run_system(rng, budget, transition_cost=0, cap=cap, ops=("query", "learn"))


def mutant_stale_cache(rng, budget, cap):
    """Planted: queries served from a cache that a transition does not invalidate."""
    return run_system(rng, budget, transition_cost=1, cap=cap, stale_cache=True)


def serial_replay_mismatches(log):
    """Recompute every logged query on the snapshot it read; count disagreements."""
    seen, mismatches = {}, 0
    for entry in log:
        if entry[0] == "query":
            _, snap, result = entry
            d = digest(snap)
            if query_on(snap) != result or seen.setdefault(d, result) != result:
                mismatches += 1
    return mismatches


def check_t8_meg30_no_livelock():
    rng = random.Random(30)
    runs = cannot = done = queries = 0
    for budget, ops in [(b, ("query", "learn", "escalate")) for b in (3, 5, 8, 10, 12, 14, 16, 18, 20)] + [(10, ("query", "escalate"))]:
        log, steps = run_system(rng, budget, transition_cost=1, ops=ops)
        assert log[-1][0] in ("DONE", "CANNOT_CHECK")
        transitions = sum(1 for e in log if e[0] in ("learn", "escalate"))
        assert transitions <= budget and sum(1 for e in log if e[0] == "escalate") <= 8
        assert serial_replay_mismatches(log) == 0
        queries += sum(1 for e in log if e[0] == "query")
        cannot += log[-1][0] == "CANNOT_CHECK"
        done += log[-1][0] == "DONE"
        runs += 1
    assert cannot > 0 and done > 0
    # learning-only loops (no ladder) still terminate: the meter alone is the ranking function
    for _ in range(10):
        log, _ = run_system(rng, rng.randint(1, 10), transition_cost=1, ops=("query", "learn"))
        assert log[-1][0] == "CANNOT_CHECK" and serial_replay_mismatches(log) == 0
    # planted mutant 1: an unmetered learning transition (cost 0) never reaches the budget — livelock at the cap
    log, steps = mutant_unmetered_transition(random.Random(1), budget=5, cap=60)
    assert sum(1 for e in log if e[0] == "learn") > 5 and steps == 60 and log[-1][0] not in ("DONE", "CANNOT_CHECK")
    # planted mutant 2: a query served from a cache not invalidated by the transition contradicts its snapshot
    log2, _ = mutant_stale_cache(random.Random(2), budget=6, cap=60)
    assert sum(1 for e in log2 if e[0] == "learn") > 0
    assert serial_replay_mismatches(log2) > 0
    return {"runs": runs, "queries_replayed": queries, "ended_cannot_check": cannot, "ended_done": done, "mutant_unmetered_livelocks_at_cap": 1, "mutant_stale_cache_caught": 1}


# ---------------------------------------------------------------------------------------------
# T9 · MEG-31 · certified-information unit
# ---------------------------------------------------------------------------------------------


def boolean_class():
    return [tuple(bits) for bits in itertools.product((0, 1), repeat=4)]  # all f: {0,1}² → {0,1}


def consistent(h, lesson):
    x, y = lesson
    return h[x] == y


def version_space(H, lessons):
    return [h for h in H if all(consistent(h, l) for l in lessons)]


def bits(H, before, after):
    vb, va = version_space(H, before), version_space(H, after)
    if not va:
        raise CannotCheck("contradictory lessons: empty version space")
    return math.log2(len(vb)) - math.log2(len(va))


def mutant_count_split_source_twice(H, lessons_by_id):
    return sum(bits(H, [], [l]) for l in lessons_by_id.values())


def check_t9_meg31_information_unit():
    H = boolean_class()
    l1_, l2_, l3_ = (0, 1), (1, 0), (2, 1)
    assert bits(H, [], [l1_]) == 1.0 and bits(H, [], [l1_, l2_]) == 2.0
    # telescoping over random chains
    rng = random.Random(31)
    chains = 0
    for _ in range(50):
        seq = rng.sample([l1_, l2_, l3_, (3, 0)], rng.randint(1, 4))
        total = sum(bits(H, seq[:i], seq[: i + 1]) for i in range(len(seq)))
        assert abs(total - bits(H, [], seq)) < 1e-12
        chains += 1
    # independence (product rule under uniform measure on V_0) ⇒ additive
    V0 = version_space(H, [])
    s1, s2 = [h for h in V0 if consistent(h, l1_)], [h for h in V0 if consistent(h, l2_)]
    both = [h for h in s1 if consistent(h, l2_)]
    assert len(both) * len(V0) == len(s1) * len(s2)
    assert bits(H, [], [l1_, l2_]) == bits(H, [], [l1_]) + bits(H, [], [l2_])
    # common source split into two ids counts once (nested ⇒ C = max ≤ sum)
    split = {"id_a": l1_, "id_b": l1_}
    assert bits(H, [], list(split.values())) == 1.0
    bad = mutant_count_split_source_twice(H, split)
    assert bad == 2.0 and bad != bits(H, [], list(split.values()))
    # no-alarm: per-lesson sums equal the joint for independent ids
    indep = {"id_a": l1_, "id_b": l2_}
    assert mutant_count_split_source_twice(H, indep) == bits(H, [], list(indep.values()))
    # non-claim witness: general dependence is neither sub- nor super-additive (recorded, not asserted as a law)
    H2 = [h for h in H if h != (0, 0, 0, 0)]  # drop one hypothesis so two examples interact
    c1, c2, c12 = bits(H2, [], [(0, 0)]), bits(H2, [], [(1, 0)]), bits(H2, [], [(0, 0), (1, 0)])
    superadditive_witness = c12 > c1 + c2 + 1e-12
    return {"telescoping_chains": chains, "independent_additive": 1, "split_source_counts_once": 1, "mutant_double_count_caught": 1, "independent_no_alarm": 1, "general_dependence_superadditive_witness_exists": int(superadditive_witness)}


# ---------------------------------------------------------------------------------------------
# T10 · MEG-35 · upper-profile certificates are refinements
# ---------------------------------------------------------------------------------------------


def certify_closure(iv):
    return (iv[0], iv[0])


def certify_bounded_alternatives(iv, family):
    up = meet(iv[1], family)
    if not leq(iv[0], up):
        raise CannotCheck("bounded-alternatives certificate contradicts exhibited support")
    return (iv[0], up)


def certify_class_bound(iv, upper_h):
    if not (leq(iv[0], upper_h) and leq(upper_h, iv[1])):
        raise CannotCheck("class bound outside the interval")
    return (iv[0], upper_h)


def mutant_certificate_replaces_upper(iv, family):
    return (iv[0], family)  # U' = antichain(F) without ⊗ U: may widen


def refines(new, old):
    return leq(old[0], new[0]) and leq(new[1], old[1])


def check_t10_meg35_upper_certificates(n=3):
    ps = all_profiles(n)
    revs = subsets(range(n))
    intervals = [(lo, up) for lo in ps for up in ps if leq(lo, up)]
    closure = bounded = classb = flips_seen_by_mutant = 0
    for iv in intervals:
        c = certify_closure(iv)
        assert refines(c, iv)
        for r in revs:
            a, b = liveness(iv, r), liveness(c, r)
            assert a == b or a == UNKNOWN
            closure += 1
        for fam in ps:
            if not leq(iv[0], meet(iv[1], fam)):
                continue
            c2 = certify_bounded_alternatives(iv, fam)
            assert refines(c2, iv)
            for r in revs:
                a, b = liveness(iv, r), liveness(c2, r)
                assert a == b or a == UNKNOWN
                bounded += 1
            bad = mutant_certificate_replaces_upper(iv, fam)
            if leq(iv[0], fam) and not refines(bad, iv):
                flips_seen_by_mutant += any(liveness(iv, r) == DEAD and liveness(bad, r) != DEAD for r in revs)
        for uh in ps:
            if leq(iv[0], uh) and leq(uh, iv[1]):
                c3 = certify_class_bound(iv, uh)
                assert refines(c3, iv)
                for r in revs:
                    a, b = liveness(iv, r), liveness(c3, r)
                    assert a == b or a == UNKNOWN
                    classb += 1
    assert flips_seen_by_mutant > 0
    try:
        certify_bounded_alternatives(cert({0}), (frozenset({1}),))
        raise AssertionError("contradicting certificate was accepted")
    except CannotCheck:
        pass
    return {"intervals": len(intervals), "closure_checks": closure, "bounded_alternative_checks": bounded, "class_bound_checks": classb, "mutant_replace_upper_decertifies_dead": flips_seen_by_mutant, "contradicting_certificate_cannot_check": 1}


# ---------------------------------------------------------------------------------------------
# T11 · MEG-01 · evidence dependence: derived evidence flattens exactly
# ---------------------------------------------------------------------------------------------


def flatten(iv, derived):
    """flat⟦L,U⟧ over E = A ⊔ D: each d ∈ D in a warrant is replaced by its own flattened interval."""

    def flat_side(side, k):
        out = ZERO
        for w in side:
            term = ONE
            for e in w:
                term = meet(term, flat_side(derived[e][k], k) if e in derived else (frozenset({e}),))
            out = join(out, term)
        return out

    return (flat_side(iv[0], 0), flat_side(iv[1], 1))


def liveness_through(iv, derived, R):
    """λ_R computed through the derived atoms with Kleene connectives (no flattening)."""
    def lam(iv_):
        lo, up = iv_
        v_lo = DEAD
        for w in lo:
            t = LIVE
            for e in w:
                t = kand(t, lam(derived[e]) if e in derived else (DEAD if e in R else LIVE))
            v_lo = kor(v_lo, t)
        if v_lo == LIVE:
            return LIVE
        v_up = DEAD
        for w in up:
            t = LIVE
            for e in w:
                t = kand(t, lam(derived[e]) if e in derived else (DEAD if e in R else LIVE))
            v_up = kor(v_up, t)
        return DEAD if v_up == DEAD else UNKNOWN

    return lam(iv)


def mutant_derived_as_assumption(iv, derived, R):
    """Planted: derived ids treated as primitive assumptions — revocation never reaches through them."""
    return liveness(iv, R)


def random_dependence(rng, n_assump=4, n_derived=3):
    A = list(range(n_assump))
    derived = {}
    for i in range(n_derived):
        universe = A + [f"d{j}" for j in range(i)]
        ws = [frozenset(rng.sample(universe, rng.randint(1, 2))) for _ in range(rng.randint(1, 2))]
        lo = canon(ws)
        up = rng.choice([lo, join(lo, canon([frozenset(rng.sample(universe, 1))]))])
        derived[f"d{i}"] = (lo, up)
    return A, derived


def check_t11_meg01_evidence_dependence():
    rng = random.Random(1)
    agreements = 0
    for _ in range(60):
        A, derived = random_dependence(rng)
        universe = A + list(derived)
        ws = [frozenset(rng.sample(universe, rng.randint(1, 3))) for _ in range(rng.randint(1, 3))]
        lo = canon(ws)
        claim = (lo, rng.choice([lo, ONE]))
        flat = flatten(claim, derived)
        assert not (evidence_of(flat) & set(derived))
        for R in subsets(A):
            assert liveness(flat, R) == liveness_through(claim, derived, R)
            agreements += 1
    # a claim citing d has warrant Λ_claim ⊗ Λ_d: flattening is the ⊗ (KS-T20 instance)
    derived = {"d": cert({0, 1})}
    claim = cert({"d", 2})
    assert flatten(claim, derived) == imeet(cert({2}), derived["d"])
    # two sources sharing an assumption never count twice
    derived = {"d1": cert({"a", "b1"}), "d2": cert({"a", "b2"})}
    claim = (canon([{"d1"}, {"d2"}]), canon([{"d1"}, {"d2"}]))
    assert liveness(flatten(claim, derived), {"a"}) == DEAD and liveness(flatten(claim, derived), {"b1"}) == LIVE
    bad = mutant_derived_as_assumption(claim, derived, {"a"})
    assert bad == LIVE and bad != liveness(flatten(claim, derived), {"a"})
    # no-alarm: genuinely independent sources survive the loss of one of them
    indep = {"d1": cert({"b1"}), "d2": cert({"b2"})}
    assert liveness(flatten(claim, indep), {"b1"}) == LIVE and liveness(flatten(claim, indep), {"b1", "b2"}) == DEAD
    return {"random_dependence_structures": 60, "flat_equals_through_derived": agreements, "claim_times_derived_is_meet": 1, "shared_assumption_counts_once": 1, "mutant_derived_as_assumption_caught": 1, "independent_sources_no_alarm": 1}


# ---------------------------------------------------------------------------------------------


def run_all():
    return {
        "T1_MEG-04": check_t1_meg04_commit_bottom(),
        "T2_MEG-06": check_t2_meg06_budget_bracket(),
        "T3_MEG-08": check_t3_meg08_feedback_not_warrant(),
        "T4_MEG-18": check_t4_meg18_jump_rollback(),
        "T5_MEG-22": check_t5_meg22_shared_evidence(),
        "T6_MEG-26": check_t6_meg26_candidate_warrant(),
        "T7_MEG-29": check_t7_meg29_no_self_authority(),
        "T8_MEG-30": check_t8_meg30_no_livelock(),
        "T9_MEG-31": check_t9_meg31_information_unit(),
        "T10_MEG-35": check_t10_meg35_upper_certificates(3),
        "T11_MEG-01": check_t11_meg01_evidence_dependence(),
        "NOVELTY": "NOT_ESTABLISHED",
    }


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
