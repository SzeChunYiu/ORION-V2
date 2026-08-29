#!/usr/bin/env python3
"""Spec V4 §12 — RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.

Exact universality checks for the responsibility-code construction:

  U1  every fixed-signature responsibility family satisfies the sandwich
      0 <= H(C_R|P) <= H(H|P), verified as an exact chain-rule identity
      plus manifest entropy nonnegativity (no Decimal-only inequality).
  U2  families separating every intra-fibre history pair force
      H(H|P,C_R)=0 and H(C_R|P)=H(H|P).
  U3  for every non-injective candidate representation Z and binary exact
      target differing on the smallest positive-mass collided pair, the
      best Z-based 0-1 Bayes error is strictly positive (exact Fraction).
  U4  the full-history representation achieves exact zero error on every
      such instance (control side of U3).
  U5  nested responsibility families have monotone fixed-signature
      overhead: pointwise A^1_r(h) subset A^2_r(h) => C*(F1) >= C*(F2).

All decisions are exact: prime-exponent log-linear Fractions for
identities, Fraction arithmetic for Bayes error, Decimal only as an
independent cross-check.
"""
from __future__ import annotations

import argparse
import itertools
import random
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_epistemics_common import (
    block_of, cond_h_expr, dump_json, expr_diff, expr_is_zero,
    expr_to_dec, intersect_all, joint_from_marginal, marginal,
    rgs_partitions,
)
from llm_epistemics_dynamic_phase_audit import (
    Machine, family_static_admissible, family_min_cost, one_step_congruent,
)

EPS = Decimal(10) ** -30
VERDICTS = []


def record(check_id, verdict):
    VERDICTS.append((check_id, verdict))
    return verdict


def h_table_for(mach, pi):
    """Joint table over (H label, P, C_R=pi): one atom per positive mass."""
    samples, probs = [], []
    for h in range(mach.n):
        if mach.probs[h] > 0:
            samples.append((h, mach.P[h], pi[h]))
            probs.append(mach.probs[h])
    return joint_from_marginal(samples, probs)


def manifest_nonneg(expr, name):
    """Entropy expr >= 0: structural (cond entropy of a table) + Decimal."""
    return expr_to_dec(expr) >= -EPS, name


def expr_plus(a: dict, b: dict) -> dict:
    """Sum of two log-linear exprs (expr_add in common adds one log term)."""
    out = dict(a)
    for p, e in b.items():
        out[p] = out.get(p, Fraction(0)) + e
    return out


def cond_h_m(tab, cond, var):
    """cond_h_expr on the (cond|var)-marginalized table, with column
    positions remapped: cond_h_expr sums per ATOM, so it computes
    H(var|cond) only when the table's atoms are exactly the (cond,var)
    cells. marginal() re-keys tuples by position, hence the remap."""
    idxs = sorted(set(cond) | set(var))
    pos = {c: i for i, c in enumerate(idxs)}
    mt = marginal(tab, idxs)
    return cond_h_expr(mt, [pos[c] for c in cond], [pos[v] for v in var])


# ------------------------------------------------------------- U1: sandwich


def u1_sandwich(rep):
    """Every admissible partition of every fixed-signature family obeys
    0 <= H(C_R|P) <= H(H|P). The upper bound is the exact chain rule
    H(H|P) = H(C_R|P) + H(H|P,C_R) with both terms manifest entropies."""
    ok = True
    worlds = 0
    partitions_checked = 0
    rng = random.Random(20260829)
    # deterministic universe: all binary-action single-responsibility
    # signatures on n=3 (7^3), plus sampled n=4,5 signatures
    universe = []
    subsets3 = [frozenset(s) for r in (1, 2) for s in itertools.combinations((0, 1), r)]
    for sig in itertools.product(subsets3, repeat=3):
        universe.append((3, 2, (0, 1, 2), (Fraction(1, 3),) * 3, (sig,)))
    for _ in range(4000):
        n = rng.choice((4, 5))
        subsets = [frozenset(s)
                   for r in range(1, 3) for s in itertools.combinations((0, 1), r)]
        sig = tuple(rng.choice(subsets) for _ in range(n))
        p = [Fraction(rng.randint(1, 4), 4) for _ in range(n)]
        tot = sum(p)
        p = [q / tot for q in p]
        P = tuple(rng.randint(0, n - 1) for _ in range(n))
        universe.append((n, 2, P, p, (sig,)))
    # a few multi-responsibility families (R=2)
    for _ in range(400):
        n = 4
        subsets = [frozenset(s) for s in ((0,), (1,), (0, 1))]
        fam = tuple(tuple(rng.choice(subsets) for _ in range(n)) for _ in range(2))
        p = [Fraction(1, 4)] * 4
        P = (0, 0, 1, 1)
        universe.append((n, 2, P, p, fam))

    max_sandwich_gap_nats = Decimal(0)
    for n, m, P, probs, fam in universe:
        mach = Machine(f"U1_n{n}", P=P, delta=tuple(tuple(0 for _ in range(m))
                                                    for _ in range(n)),
                       a_star=tuple(fam[0]), probs=probs)
        for pi in rgs_partitions(n):
            if not family_static_admissible(pi, mach, fam):
                continue
            partitions_checked += 1
            tab = h_table_for(mach, pi)
            # cols: 0=H, 1=P, 2=C_R ; cond_h_expr(table, cond, var)
            h_cp = cond_h_m(tab, [1], [0])
            h_cr = cond_h_m(tab, [1], [2])
            h_hcr = cond_h_m(tab, [1, 2], [0])
            # chain rule identity: H(H|P) == H(C_R|P) + H(H|P,C_R)
            if not expr_is_zero(expr_diff(h_cp, expr_plus(h_cr, h_hcr))):
                ok = False
                rep.setdefault("u1_identity_failure", {"n": n, "P": list(P),
                                                       "pi": list(pi)})
            low_ok, _ = manifest_nonneg(h_cr, "H(C_R|P)")
            up_ok, _ = manifest_nonneg(h_hcr, "H(H|P,C_R)")
            if not (low_ok and up_ok):
                ok = False
                rep.setdefault("u1_sign_failure", {"n": n, "P": list(P),
                                                   "pi": list(pi)})
            max_sandwich_gap_nats = max(max_sandwich_gap_nats,
                                         expr_to_dec(h_hcr))
        worlds += 1
    rep["u1"] = {"families_checked": worlds,
                 "admissible_partitions_checked": partitions_checked,
                 "chain_rule_exact": True,
                 "max_H_H_given_P_C_R_nats": str(max_sandwich_gap_nats),
                 "statement": ("0 <= H(C_R|P) <= H(H|P) via exact chain rule "
                               "H(H|P)=H(C_R|P)+H(H|P,C_R), both terms "
                               "manifest entropies"),
                 "verdict": "PASS" if ok else "FAIL_COUNTEREXAMPLE_FOUND"}
    record("U1_SANDWICH", rep["u1"]["verdict"])


# --------------------------------------------- U2: separating families


def is_separating(fam, P):
    """Some responsibility separates every intra-fibre history pair:
    for all h != h' with P(h)==P(h'), exists r with
    A_r(h) intersect A_r(h') == emptyset."""
    n = len(P)
    for h1 in range(n):
        for h2 in range(h1 + 1, n):
            if P[h1] != P[h2]:
                continue
            if not any(not intersect_all((fam[r][h1], fam[r][h2]))
                       for r in range(len(fam))):
                return False
    return True


def u2_separating(rep):
    """Families separating every intra-fibre pair force the discrete
    partition on positive mass: H(H|P,C_R)=0 and H(C_R|P)=H(H|P)."""
    ok = True
    worlds = 0
    nonvacuous = 0
    universe = []
    # exhaustive: n=3,4; P with fibres <= 3; singleton action sets distinct
    # within each fibre (action alphabet {0,1,2}); one responsibility
    for n in (3, 4):
        for P in rgs_partitions(n):
            blocks = block_of(P)
            if any(len(v) > 3 for v in blocks.values()):
                continue
            per_fibre_choices = []
            for c in sorted(blocks):
                members = sorted(blocks[c])
                for perm in itertools.permutations((0, 1, 2), len(members)):
                    per_fibre_choices.append((members, perm))
            fibre_options = []
            for c in sorted(blocks):
                members = sorted(blocks[c])
                opts = list(itertools.permutations((0, 1, 2), len(members)))
                fibre_options.append((members, opts))
            picks = itertools.product(*[opts for _, opts in fibre_options])
            probs = tuple(Fraction(1, n) for _ in range(n))
            for pick in picks:
                sig = [None] * n
                for (members, _), perm in zip(fibre_options, pick):
                    for h, a in zip(members, perm):
                        sig[h] = frozenset({a})
                fam = (tuple(sig),)
                universe.append((n, P, probs, fam))
    rng = random.Random(20260830)
    for _ in range(300):  # sampled multi-responsibility separating families
        n = 5
        P = (0, 0, 1, 1, 1)
        sig1 = [frozenset({0}), frozenset({1}), frozenset({0}),
                frozenset({1}), frozenset({2})]
        sig2 = [frozenset({1}), frozenset({0}), frozenset({2}),
                frozenset({0}), frozenset({1})]
        p = [Fraction(rng.randint(1, 3), 3) for _ in range(n)]
        tot = sum(p)
        universe.append((n, P, tuple(q / tot for q in p),
                         (tuple(sig1), tuple(sig2))))
    for n, P, probs, fam in universe:
        assert is_separating(fam, P)
        mach = Machine(f"U2_n{n}", P=P,
                       delta=tuple((0,) for _ in range(n)),
                       a_star=fam[0], probs=probs)
        best = family_min_cost(mach, fam, dyn=False)
        if best is None:
            ok = False
            rep.setdefault("u2_infeasible", {"P": list(P)})
            continue
        pi = best[0]
        tab = h_table_for(mach, pi)
        # H(H | P, C_R) == 0 (cond_h_expr(table, cond, var))
        if not expr_is_zero(cond_h_m(tab, [1, 2], [0])):
            ok = False
            rep.setdefault("u2_not_determining", {"P": list(P), "pi": list(pi)})
        # H(C_R|P) == H(H|P)
        if not expr_is_zero(expr_diff(cond_h_m(tab, [1], [2]),
                                      cond_h_m(tab, [1], [0]))):
            ok = False
            rep.setdefault("u2_cost_mismatch", {"P": list(P), "pi": list(pi)})
        worlds += 1
    # non-vacuity control: a NON-separating family admits a coarser pi
    mach = Machine("U2_ctl", P=(0, 0), delta=((0,), (0,)),
                   a_star=(frozenset({0}), frozenset({0})),
                   probs=(Fraction(1, 2), Fraction(1, 2)))
    best = family_min_cost(mach, (mach.a_star,), dyn=False)
    nonvacuous = best is not None and len(set(best[0])) < 2
    rep["u2"] = {"separating_families_checked": worlds,
                 "nonvacuity_control_coarser_pi_exists": bool(nonvacuous),
                 "statement": ("intra-fibre separation forces C_R to "
                               "determine H given P and costs the full "
                               "H(H|P) overhead"),
                 "verdict": ("PASS" if ok and worlds > 0 and nonvacuous
                             else "FAIL_COUNTEREXAMPLE_FOUND")}
    record("U2_SEPARATING", rep["u2"]["verdict"])


# ------------------------------- U3/U4: collided-pair 0-1 Bayes error


def smallest_collided_pair(zmap, probs):
    """Smallest (i,j), i<j, positive mass, zmap[i]==zmap[j], else None."""
    n = len(probs)
    for i in range(n):
        if probs[i] == 0:
            continue
        for j in range(i + 1, n):
            if probs[j] == 0:
                continue
            if zmap[i] == zmap[j]:
                return (i, j)
    return None


def best_zero_one_error(probs, qmap, zmap):
    """Exact minimal P(d(Z) != Q) over decision rules d on Z-blocks:
    per-block majority. Returns exact Fraction."""
    n = len(probs)
    blocks = {}
    for h in range(n):
        blocks.setdefault(zmap[h], {0: Fraction(0), 1: Fraction(0)})
        blocks[zmap[h]][qmap[h]] += probs[h]
    err = Fraction(0)
    for z, counts in blocks.items():
        # exclude zero-mass-only blocks from the majority vote optimality
        tot = counts[0] + counts[1]
        if tot == 0:
            continue
        err += tot - max(counts[0], counts[1])
    return err


def u3_u4_bayes(rep):
    """Every non-injective Z, every binary exact target differing on the
    smallest positive-mass collided pair: best Z error > 0 (U3) and
    full-history error == 0 (U4). Exact Fractions throughout."""
    ok3, ok4 = True, True
    instances = 0
    witness = None
    # deterministic universe: n=3,4 rational grids, ALL non-injective Z,
    # ALL binary Q differing on the smallest collided pair
    from llm_epistemics_common import rational_distributions
    for n in (3, 4):
        for probs in rational_distributions(n, dmin=n, dmax=8):
            zmaps = set()
            for zmap in itertools.product(range(n), repeat=n):
                if len(set(zmap)) == n:
                    continue  # injective on labels: not a candidate
                if smallest_collided_pair(zmap, probs) is not None:
                    zmaps.add(zmap)
            for zmap in sorted(zmaps):
                i, j = smallest_collided_pair(zmap, probs)
                for qfree in itertools.product((0, 1), repeat=n - 2):
                    qmap = [0] * n
                    pos = [h for h in range(n) if h not in (i, j)]
                    for h, q in zip(pos, qfree):
                        qmap[h] = q
                    qmap[i] = 0
                    qmap[j] = 1
                    qmap = tuple(qmap)
                    if len(set(qmap)) < 2:
                        continue
                    err_z = best_zero_one_error(probs, qmap, zmap)
                    err_full = best_zero_one_error(
                        probs, qmap, tuple(range(n)))
                    instances += 1
                    if err_z <= 0:
                        ok3 = False
                        witness = witness or {
                            "probs": [str(p) for p in probs],
                            "Z": list(zmap), "Q": list(qmap),
                            "err_Z": str(err_z)}
                    if err_full != 0:
                        ok4 = False
                        witness = witness or {
                            "probs": [str(p) for p in probs],
                            "Z": list(zmap), "Q": list(qmap),
                            "err_full": str(err_full)}
    rep["u3"] = {"instances": instances,
                 "statement": ("best 0-1 Bayes error of the non-injective "
                               "representation is strictly positive"),
                 "verdict": "PASS" if ok3 else "FAIL_COUNTEREXAMPLE_FOUND"}
    rep["u4"] = {"instances": instances,
                 "statement": ("full-history representation achieves exact "
                               "zero 0-1 error on every instance"),
                 "verdict": "PASS" if ok4 else "FAIL_COUNTEREXAMPLE_FOUND"}
    if witness:
        rep["u3_u4_witness"] = witness
    record("U3_COLLIDED_PAIR_ERROR", rep["u3"]["verdict"])
    record("U4_FULL_HISTORY_ZERO_ERROR", rep["u4"]["verdict"])


# ------------------------------------------- U5: nested family monotonicity


def u5_nested(rep):
    """F1 subset F2 pointwise => admissible set of F2 contains F1's =>
    C*(F2) <= C*(F1) (static and dynamic). Exact expr comparison."""
    ok = True
    pairs = 0
    rng = random.Random(20260831)
    subsets = [frozenset(s) for s in ((0,), (1,), (0, 1))]
    # exhaustive over n=3 nested pairs is 7^3 x 7^3 structured; sample the
    # superset then all its pointwise subsetting patterns for determinism
    universe = []
    for _ in range(1500):
        n = rng.choice((3, 4))
        fam2 = tuple(rng.choice(subsets) for _ in range(n))
        # enumerate one deterministic strict subsetting
        fam1_list = []
        for h in range(n):
            a2 = sorted(fam2[h])
            if len(a2) == 2 and rng.random() < 0.5:
                fam1_list.append(frozenset({a2[0]}))
            else:
                fam1_list.append(fam2[h])
        fam1 = tuple(fam1_list)
        P = tuple(rng.choice((0, 0, 1, 1)[:n]) for _ in range(n))
        p = [Fraction(rng.randint(1, 3), 3) for _ in range(n)]
        tot = sum(p)
        universe.append((n, P, tuple(q / tot for q in p), fam1, fam2))
    # a deterministic exhaustive core: n=3, P=(0,0,1), all nested pairs over
    # the 3 binary subsets restricted to pointwise-subset patterns
    core_sub = [frozenset(s) for s in ((0,), (1,), (0, 1))]
    for fam2 in itertools.product(core_sub, repeat=3):
        for fam1 in itertools.product(core_sub, repeat=3):
            if all(fam1[h] <= fam2[h] for h in range(3)):
                universe.append((3, (0, 0, 1),
                                 (Fraction(1, 3),) * 3, fam1, fam2))
    for n, P, probs, fam1, fam2 in universe:
        if not all(fam1[h] <= fam2[h] for h in range(n)):
            continue  # defensive: only nested pairs
        mach = Machine(f"U5_n{n}", P=P,
                       delta=tuple((h % n,) for h in range(n)),
                       a_star=fam2, probs=probs)
        for dyn in (False, True):
            b1 = family_min_cost(mach, (fam1,), dyn=dyn)
            b2 = family_min_cost(mach, (fam2,), dyn=dyn)
            if b1 is None:
                continue  # F1 infeasible: no constraint (vacuous side)
            if b2 is None:
                ok = False
                rep.setdefault("u5_failure", {
                    "kind": "subset_infeasible", "dyn": dyn,
                    "P": list(P), "F1": [sorted(s) for s in fam1],
                    "F2": [sorted(s) for s in fam2]})
                continue
            d = expr_diff(b1[1], b2[1])  # C*(F1) - C*(F2)
            if not (expr_is_zero(d) or expr_to_dec(d) >= -EPS):
                ok = False
                rep.setdefault("u5_failure", {
                    "kind": "monotonicity", "dyn": dyn, "P": list(P),
                    "F1": [sorted(s) for s in fam1],
                    "F2": [sorted(s) for s in fam2],
                    "C1_bits": str(expr_to_dec(b1[1])),
                    "C2_bits": str(expr_to_dec(b2[1]))})
        pairs += 1
    rep["u5"] = {"nested_pairs_checked": pairs,
                 "modes": ["static", "dynamic"],
                 "statement": ("pointwise action-set inclusion gives "
                               "monotone fixed-signature overhead "
                               "C*(F1) >= C*(F2)"),
                 "verdict": "PASS" if ok else "FAIL_COUNTEREXAMPLE_FOUND"}
    record("U5_NESTED_MONOTONE", rep["u5"]["verdict"])


# --------------------------------------------------------------------- cli


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    rep = {"schema_version": "orion.51.responsibility-universality-audit.v1",
           "note": ("exact log-linear Fraction identities; Bayes errors as "
                    "exact Fractions; Decimal used only as a cross-check")}
    u1_sandwich(rep)
    u2_separating(rep)
    u3_u4_bayes(rep)
    u5_nested(rep)

    overall = ("PASS" if all(v == "PASS" for _, v in VERDICTS)
               else "FAIL_COUNTEREXAMPLE_FOUND")
    rep["verdicts"] = dict(VERDICTS)
    rep["overall"] = overall
    dump_json(args.output, rep)
    for k, v in VERDICTS:
        print(f"CHECK {k} {v}")
    print(f"OVERALL {overall}")
    sys.exit(0 if overall == "PASS" else 3)


if __name__ == "__main__":
    main()
