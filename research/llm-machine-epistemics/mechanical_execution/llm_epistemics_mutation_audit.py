#!/usr/bin/env python3
"""Spec V4 §9 — PREDICTIVE_COMPRESSION_ASSUMPTION_MATRIX_V1.

Mutation battery on the exact deterministic theorem (T2: the
entropy-minimal predictive-sufficient representation is S_P up to
isomorphism). For each mutation: exhaustive small-grid search freezing the
smallest counterexample, or the exact corollary that survives.

Registered mutations:
  M1 drop entropy minimality                (expect non-uniqueness witness)
  M2 approximate sufficiency H(Q|Z)<=eps   (witness + data-processing floor)
  M3 stochastic representation Z~p(Z|H)    (expect corollary, no witness)
  M4 cardinality minimality                (expect corollary on this lattice)
  M5 zero-mass nominal histories           (expect non-uniqueness witness)
  M6 near-minimal entropy delta-slack      (expect non-sufficiency witness)

World model (identical to the partition audit): H finite, p(h) rational,
deterministic exact target Q: H->{0..}. Predictive sufficiency of Z
  <=> Z determines Q on positive mass  <=> Z refines the Q-partition.
S_P = Q-partition, H(S_P) = H(Q-marginal) exactly (deterministic target).

Exact arithmetic: prime-exponent log-linear Fractions for identities;
Decimal >= 110 digits as independent cross-check; inequalities are checked
cellwise by exact Fraction sign (conditional entropies are manifestly
nonnegative sums). No new approximate theorem is formulated.
"""
from __future__ import annotations

import argparse
import itertools
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_epistemics_common import (
    cond_h_expr, dump_json, expr_diff, expr_is_zero, expr_to_dec,
    h_expr, joint_from_marginal, marginal, rational_distributions,
)

EPS = Decimal(10) ** -30


# ---------------------------------------------------------------- helpers


def all_maps(n, k):
    for combo in itertools.product(range(k), repeat=n):
        yield combo


def z_determines_q(zmap, qmap, probs):
    """Exact sufficiency: z(h)==z(h') with both p>0 => q(h)==q(h')."""
    for h1 in range(len(probs)):
        if probs[h1] == 0:
            continue
        for h2 in range(h1 + 1, len(probs)):
            if probs[h2] == 0:
                continue
            if zmap[h1] == zmap[h2] and qmap[h1] != qmap[h2]:
                return False
    return True


def n_blocks_of(m):
    return len(set(m))


def h_of_map(probs, fmap):
    samples = [(fmap[h],) for h in range(len(probs))]
    table = joint_from_marginal(samples, list(probs))
    return h_expr(table, [0])


def h_of_map_dec(probs, fmap):
    return expr_to_dec(h_of_map(probs, fmap))


def cond_h_qz(probs, zmap, qmap):
    """Exact H(Q|Z) expr."""
    samples = [(qmap[h], zmap[h]) for h in range(len(probs))]
    table = joint_from_marginal(samples, list(probs))
    return cond_h_expr(table, [1], [0])


def witness_dict(**kw):
    return {k: (str(v) if isinstance(v, Decimal) else v) for k, v in kw.items()}


# ------------------------------------------------- M1: drop entropy minimality


def m1(rep):
    """Sufficiency alone: any refinement of S_P is sufficient, including
    strictly finer ones with strictly larger entropy. Smallest witness."""
    rec = {"mutation": "M1_no_entropy_minimality"}
    found = None
    for n in (2, 3, 4):
        for qmap in all_maps(n, 2):
            if n_blocks_of(qmap) < 2:
                continue
            probs = [Fraction(1, n)] * n
            h_sp = h_of_map_dec(probs, qmap)
            for zmap in all_maps(n, n):
                if not z_determines_q(zmap, qmap, probs):
                    continue
                h_z = h_of_map_dec(probs, zmap)
                # non-isomorphic to S_P and strictly higher entropy
                if h_z > h_sp + EPS and n_blocks_of(zmap) != n_blocks_of(qmap):
                    found = witness_dict(n=n, probs=[str(p) for p in probs],
                                         Q=list(qmap), Z=list(zmap),
                                         H_SP_bits=h_sp, H_Z_bits=h_z,
                                         blocks_SP=n_blocks_of(qmap),
                                         blocks_Z=n_blocks_of(zmap))
                    break
            if found:
                break
        if found:
            break
    rec["witness"] = found
    rec["corollary"] = ("sufficiency is closed under refinement: without the "
                        "entropy-minimality selection rule the S_P isomorph "
                        "is not singled out")
    rec["verdict"] = "FAIL_COUNTEREXAMPLE_FOUND" if found else "PASS"
    rep["mutations"].append(rec)


# ------------------------------------- M2: approximate predictive sufficiency


def m2(rep):
    """eps-approximate sufficiency. Two exact statements:
    (a) floor: H(Q|Z) >= H(Q) - H(Z) = H(S_P) - H(Z), from
        I(Q;Z) <= H(Z); H(Z|Q) is a cellwise nonnegative exact sum.
    (b) non-uniqueness: an eps-sufficient Z, not isomorphic to S_P, with
        H(Z) < H(S_P) exists (uniqueness fails under approximation).
    """
    rec = {"mutation": "M2_approximate_predictive_sufficiency"}
    eps = Fraction(1, 10)
    eps_dec = Decimal(eps.numerator) / Decimal(eps.denominator)

    # (a) chain-rule identity + cellwise nonnegativity on random tables
    import random
    rng = random.Random(20260829)
    ident_ok, cell_ok = True, True
    for _ in range(200):
        n = 3
        ps = [Fraction(rng.randint(1, 6), 6) for _ in range(n)]
        tot = sum(ps)
        ps = [p / tot for p in ps]
        qmap = tuple(rng.randint(0, 1) for _ in range(n))
        zmap = tuple(rng.randint(0, 1) for _ in range(n))
        samples = [(qmap[h], zmap[h]) for h in range(n)]
        table = joint_from_marginal(samples, list(ps))
        # H(Q|Z) - H(Q) + H(Z) == H(Z|Q) exactly
        lhs = expr_diff(cond_h_expr(table, [1], [0]),
                        expr_diff(h_expr(table, [0]), h_expr(table, [1])))
        rhs = cond_h_expr(table, [0], [1])
        ident_ok &= expr_is_zero(expr_diff(lhs, rhs))
        mq = marginal(table, [0])
        for key, pqz in table.items():
            cell_ok &= mq[(key[0],)] >= pqz  # exact Fraction comparison
        # decimal cross-check of the floor inequality
        floor = expr_to_dec(h_expr(table, [0])) - expr_to_dec(h_expr(table, [1]))
        hqz = expr_to_dec(cond_h_expr(table, [1], [0]))
        if hqz < floor - EPS:
            ident_ok = False
    rec["floor_identity_trials"] = 200
    rec["floor_identity_exact_and_cellwise_nonneg"] = bool(ident_ok and cell_ok)
    rec["floor_statement"] = ("H(Q|Z) >= H(S_P) - H(Z) exactly; approximate "
                              "sufficiency cannot beat the data-processing "
                              "entropy floor")

    # (b) witness search: smallest-denominator rational grid, d ascending.
    # Ordering: cheap structural tests first; exact H(Q|Z) only when the
    # entropy inequality already holds.
    found = None
    for probs in rational_distributions(3, dmin=4, dmax=40):
        for qmap in all_maps(3, 2):
            if n_blocks_of(qmap) < 2:
                continue
            h_sp = h_of_map_dec(probs, qmap)
            for zmap in all_maps(3, 3):
                # cross-fibre merge <=> Z not a refinement of S_P
                # <=> not exactly sufficient (deterministic maps)
                if z_determines_q(zmap, qmap, probs):
                    continue
                h_z = h_of_map_dec(probs, zmap)
                if h_z >= h_sp - EPS:
                    continue
                hqz_dec = expr_to_dec(cond_h_qz(probs, zmap, qmap))
                if hqz_dec <= eps_dec + EPS and hqz_dec > EPS:
                    found = witness_dict(probs=[str(p) for p in probs],
                                         Q=list(qmap), Z=list(zmap),
                                         eps=str(eps), H_Q_given_Z_bits=hqz_dec,
                                         H_Z_bits=h_z, H_SP_bits=h_sp,
                                         floor_check_bits=str(
                                             hqz_dec - (h_sp - h_z)))
                    break
            if found:
                break
        if found:
            break
    rec["witness"] = found
    rec["corollary"] = ("approximate sufficiency destroys isomorphism "
                        "uniqueness but preserves the exact floor "
                        "H(Q|Z) >= H(S_P) - H(Z)")
    rec["verdict"] = "FAIL_COUNTEREXAMPLE_FOUND" if found else "PASS"
    rep["mutations"].append(rec)


# ------------------------------------------- M3: stochastic representation


def m3(rep):
    """Z stochastic given H (Z carries Q-label plus independent noise).
    Exact sufficiency of a stochastic Z with Q=f(H) forces each Z-cell to
    be q-constant; then H(Z) - H(Q) = H(Z|Q) is a cellwise nonnegative
    exact sum, so the deterministic entropy floor survives stochasticity
    and the independent noise is paid in full.
    """
    rec = {"mutation": "M3_stochastic_representation"}
    sufficient, counterexamples, ident_ok = 0, 0, True
    for n in (2, 3):
        for qmap in all_maps(n, 2):
            if n_blocks_of(qmap) < 2:
                continue
            probs = [Fraction(1, n)] * n
            h_sp_dec = h_of_map_dec(probs, qmap)
            for label in all_maps(n, 2):
                # Z = (label(H), U), U ~ Bern(1/2) independent of H
                samples = [(qmap[h], label[h], u)
                           for h in range(n) for u in (0, 1)]
                pl = [probs[h] * Fraction(1, 2)
                      for h in range(n) for u in (0, 1)]
                table = joint_from_marginal(samples, pl)
                # exact sufficiency <=> every (z1,z2) cell q-constant
                cells = {}
                cellwise_constant = True
                for key, p in table.items():
                    zcell = (key[1], key[2])
                    if zcell in cells and cells[zcell] != key[0]:
                        cellwise_constant = False
                    cells[zcell] = key[0]
                if not cellwise_constant:
                    continue
                # H(Q|Z1,Z2) == 0 exactly
                hqz = cond_h_expr(table, [1, 2], [0])
                if not expr_is_zero(hqz):
                    ident_ok = False  # cellwise test disagrees with entropy
                    continue
                sufficient += 1
                hz = h_expr(table, [1, 2])
                hz_dec = expr_to_dec(hz)
                if hz_dec < h_sp_dec - EPS:
                    counterexamples += 1
                    rec.setdefault("witness", {
                        "n": n, "Q": list(qmap), "label": list(label),
                        "H_Z_bits": str(hz_dec), "H_SP_bits": str(h_sp_dec)})
                # chain rule: H(Z) - H(Q) == H(Z|Q), cellwise >= 0
                lhs = expr_diff(hz, h_expr(table, [0]))
                rhs = cond_h_expr(table, [0], [1, 2])
                if not expr_is_zero(expr_diff(lhs, rhs)):
                    ident_ok = False
                mq = marginal(table, [0])
                for key, p in table.items():
                    if mq[(key[0],)] < p:
                        ident_ok = False
    rec["exactly_sufficient_stochastic_channels"] = sufficient
    rec["counterexamples"] = counterexamples
    rec["chain_rule_and_cellwise_consistent"] = bool(ident_ok)
    rec["non_vacuous"] = sufficient > 0
    rec["corollary"] = ("exact stochastic sufficiency inherits the "
                        "deterministic floor H(Z) >= H(S_P) cellwise, and "
                        "independent noise entropy is paid additively on "
                        "top of it")
    rec["verdict"] = ("FAIL_COUNTEREXAMPLE_FOUND" if counterexamples or not ident_ok
                      or sufficient == 0 else "PASS")
    rep["mutations"].append(rec)


# --------------------------------------------- M4: cardinality minimality


def m4(rep):
    """On the exact sufficient lattice (Z refines the Q-partition):
    (i) every sufficient Z has n_blocks >= n_blocks(S_P) and
        H(Z) >= H(S_P) exactly (chain rule + cellwise nonnegativity);
    (ii) the Q-partition attains both minima, so cardinality and entropy
    minimality select the same structure.
    """
    rec = {"mutation": "M4_cardinality_minimality"}
    worlds = 0
    bad = 0
    ident_ok = True
    for n in (2, 3, 4):
        for probs in rational_distributions(n, dmin=n, dmax=10):
            for qmap in all_maps(n, min(n, 3)):
                if n_blocks_of(qmap) < 2:
                    continue
                h_q_dec = h_of_map_dec(probs, qmap)
                nb_q = n_blocks_of(qmap)
                any_sufficient = False
                for zmap in all_maps(n, n):
                    if not z_determines_q(zmap, qmap, probs):
                        continue
                    any_sufficient = True
                    if n_blocks_of(zmap) < nb_q:
                        bad += 1
                        rec.setdefault("cardinality_witness",
                                       {"n": n, "Q": list(qmap), "Z": list(zmap)})
                    # H(Z) - H(Q) == H(Z|Q) exact, cellwise >= 0
                    samples = [(qmap[h], zmap[h]) for h in range(n)]
                    table = joint_from_marginal(samples, list(probs))
                    hz = h_expr(table, [1])
                    lhs = expr_diff(hz, h_expr(table, [0]))
                    rhs = cond_h_expr(table, [0], [1])
                    if not expr_is_zero(expr_diff(lhs, rhs)):
                        ident_ok = False
                    mq = marginal(table, [0])
                    for key, p in table.items():
                        if mq[(key[0],)] < p:
                            ident_ok = False
                    if expr_to_dec(hz) < h_q_dec - EPS:
                        bad += 1
                        rec.setdefault("entropy_witness",
                                       {"n": n, "Q": list(qmap), "Z": list(zmap)})
                if any_sufficient:
                    worlds += 1
    rec["worlds_with_sufficient_maps"] = worlds
    rec["non_vacuous"] = worlds > 0
    rec["chain_rule_and_cellwise_consistent"] = bool(ident_ok)
    rec["corollary"] = ("on the exact deterministic lattice, entropy and "
                        "cardinality minimality both select the Q-partition "
                        "structure; the two criteria coincide")
    rec["verdict"] = "FAIL_COUNTEREXAMPLE_FOUND" if bad or not ident_ok else "PASS"
    rep["mutations"].append(rec)


# --------------------------------------------- M5: zero-mass histories


def m5(rep):
    """Zero-mass nominal histories are unconstrained by both sufficiency
    and entropy: two entropy-minimal sufficient maps differing only on a
    zero-mass history. Uniqueness therefore holds only up to the
    positive-mass support."""
    rec = {"mutation": "M5_zero_mass_histories"}
    probs = [Fraction(1, 2), Fraction(1, 2), Fraction(0)]
    qmap = (0, 1, 0)
    z_a = (0, 1, 0)
    z_b = (0, 1, 1)  # differs only on h2, which carries no mass
    suff_a = z_determines_q(z_a, qmap, probs)
    suff_b = z_determines_q(z_b, qmap, probs)
    h_a = h_of_map_dec(probs, z_a)
    h_b = h_of_map_dec(probs, z_b)
    h_sp = h_of_map_dec(probs, qmap)
    equal_entropy = abs(h_a - h_b) < EPS
    minimal = abs(h_a - h_sp) < EPS
    agree_on_support = all(z_a[h] == z_b[h] for h in range(3) if probs[h] > 0)
    found = suff_a and suff_b and equal_entropy and minimal and (z_a != z_b)
    rec["witness"] = (witness_dict(probs=[str(p) for p in probs],
                                   Q=list(qmap), Z_a=list(z_a), Z_b=list(z_b),
                                   both_sufficient=[suff_a, suff_b],
                                   H_bits=h_a, agree_on_positive_mass=agree_on_support)
                      if found else None)
    rec["corollary"] = ("the T2 isomorphism is pinned only on the "
                        "positive-mass support; nominal zero-mass histories "
                        "are free labels")
    rec["verdict"] = "FAIL_COUNTEREXAMPLE_FOUND" if found else "PASS"
    rep["mutations"].append(rec)


# ------------------------------------------- M6: near-minimal entropy slack


def m6(rep):
    """delta-close entropy does not imply sufficiency: exhaustive search
    over 2-block Z for the smallest-denominator world with an insufficient
    Z satisfying H(S_P) < H(Z) < H(S_P) + 1/10."""
    rec = {"mutation": "M6_near_minimal_entropy"}
    delta = Fraction(1, 10)
    delta_dec = Decimal(delta.numerator) / Decimal(delta.denominator)
    found = None
    for probs in rational_distributions(4, dmin=4, dmax=16):
        for qmap in all_maps(4, 2):
            if n_blocks_of(qmap) < 2:
                continue
            h_sp = h_of_map_dec(probs, qmap)
            for zmap in all_maps(4, 2):  # 2-block Z only (registered family)
                if len(set(zmap)) < 2:
                    continue
                if z_determines_q(zmap, qmap, probs):
                    continue  # exactly sufficient: not a slack witness
                h_z = h_of_map_dec(probs, zmap)
                if h_sp + EPS < h_z < h_sp + delta_dec - EPS:
                    found = witness_dict(probs=[str(p) for p in probs],
                                         Q=list(qmap), Z=list(zmap),
                                         delta=str(delta), H_SP_bits=h_sp,
                                         H_Z_bits=h_z)
                    break
            if found:
                break
        if found:
            break
    rec["search_family"] = "all 2-block Z on n=4, denominator d<=16 grids"
    rec["witness"] = found
    rec["corollary"] = ("no metric stability: entropy closeness to the "
                        "minimum carries no sufficiency guarantee (the "
                        "sufficient lattice is not entropy-isolated)")
    rec["verdict"] = "FAIL_COUNTEREXAMPLE_FOUND" if found else "PASS"
    rep["mutations"].append(rec)


# --------------------------------------------------------------------- cli


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    rep = {"schema_version": "orion.51.predictive-compression-assumption-matrix.v1",
           "note": ("grid searches are exhaustive over the registered "
                    "families; witnesses are frozen smallest-denominator "
                    "hits; a FAIL_COUNTEREXAMPLE_FOUND verdict on a "
                    "mutation reports the MUTATED statement failing, not "
                    "the parent theorem"),
           "mutations": []}
    for fn in (m1, m2, m3, m4, m5, m6):
        fn(rep)

    executed = len(rep["mutations"])
    n_witness = sum(1 for m in rep["mutations"]
                    if m["verdict"] == "FAIL_COUNTEREXAMPLE_FOUND")
    n_survive = executed - n_witness
    rep["summary"] = {"mutations_executed": executed,
                      "mutation_counterexamples_frozen": n_witness,
                      "mutations_survived_by_parent_conclusion": n_survive}
    dump_json(args.output, rep)
    for m in rep["mutations"]:
        print(f"CHECK {m['mutation']} {m['verdict']}")
    print(f"OVERALL MATRIX_COMPLETE executed={executed} "
          f"witnesses={n_witness} survived={n_survive}")
    sys.exit(0 if executed == 6 else 3)


if __name__ == "__main__":
    main()
