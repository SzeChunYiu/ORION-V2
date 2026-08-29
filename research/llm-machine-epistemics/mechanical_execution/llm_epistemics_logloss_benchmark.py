#!/usr/bin/env python3
"""Spec V4 §11 — LOGLOSS_PARENT_BENCHMARK_V1.

Exact arithmetic audit of the registered reveal/erasure rate-distortion
construction for a deterministic exact target Q:

  R(D) = max(H(Q|P) - D, 0)   at distortion ratios r in {0,.1,...,1},
                              D_r = r * H(Q|P)

Part A  achievability: the rational time-sharing construction
        (Theta ~ Bern(1-r) independent per fibre; Z = Q if Theta=1
        else erasure) attains I(Q;Z|P) = (1-r)H(Q|P) and expected
        registered erasure distortion E[d] = r*H(Q|P), both exactly.
        Converse: I(Q;Z|P) >= H(Q|P) - E[d] reduces cellwise to the
        manifestly nonnegative I(Q; e | P) >= 0 on exhaustive small
        fibre-dependent erasure channels.
Part B  conditionally independent Q_i given P: additivity of the joint
        entropy and the product/shared-Theta achievability at the
        normalized distortion grid {0,.25,.5,.75,1}.
Part C  correlated controls: Q2=Q1, Q1=f(Q2), partially correlated,
        independent — each quantifying the exact inflation
        sum_i H(Q_i|P) - H(joint|P); no independent-novelty credit is
        emitted anywhere in the output.

All identities are exact prime-exponent log-linear Fraction checks;
conditional entropies go through the marginalizing wrapper cond_h_m
(cond_h_expr sums per ATOM and needs atoms == (cond,var) cells).
Decimal (>=110 digits) is an independent cross-implementation only.
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
    cmi_expr, cond_h_expr, dump_json, expr_diff, expr_is_zero, expr_to_dec,
    joint_from_marginal, marginal,
)
from llm_epistemics_universality_audit import cond_h_m, expr_plus

EPS = Decimal(10) ** -30
VERDICTS = []


def record(check_id, verdict):
    VERDICTS.append((check_id, verdict))
    return verdict


def cmi_m(tab, a, b, cond):
    """I(A;B|C) with EACH term marginalized to its own granularity:
    H(A|C) on the (A,C)-marginal minus H(A|B,C) on the (A,B,C)-marginal.
    (A single (A,B,C)-marginal is NOT enough: cond_h_expr carries the
    ATOM mass inside the log, so H(A|C) computed from (A,B,C)-cells
    overcounts by the within-cell mixing entropy of B.)"""
    return expr_diff(cond_h_m(tab, cond, a),
                     cond_h_m(tab, list(cond) + list(b), a))


def q_p_table(probs, P, qmap):
    """Table over atoms (h, P, Q) for positive-mass histories."""
    samples = [(h, P[h], qmap[h]) for h in range(len(probs))
               if probs[h] > 0]
    pl = [p for p in probs if p > 0]
    return joint_from_marginal(samples, pl)


def h_q_given_p(tab):
    """cols: 0=h,1=P,2=Q -> H(Q|P)."""
    return cond_h_m(tab, [1], [2])


def expr_scale(c: Fraction, e: dict) -> dict:
    return {p: c * v for p, v in e.items()}


def fibre_subtables(tab, pcol=1):
    """Split a table into per-fibre sub-tables (atoms sharing tab[pcol])."""
    out = {}
    for key, mass in tab.items():
        out.setdefault(key[pcol], {})[key] = mass
    return out


def prune(tab):
    """Drop zero-mass atoms (r=0/1 grid points create them; entropy
    helpers divide by atom mass)."""
    return {k: v for k, v in tab.items() if v > 0}


def build_ext(tab, rfun):
    """Reveal/erasure extension.  tab atoms (h, P, Q); rfun maps a
    (Q, P) cell to the rational erasure probability.  Returns a table
    over (Q, P, Theta, Z) with Theta=1 reveal / 0 erasure and
    Z = Q on reveal, 'e' on erasure."""
    ext = {}
    for key, mass in tab.items():
        _, p, q = key
        r = rfun(q, p)
        a = (q, p, 1, q)
        b = (q, p, 0, "e")
        ext[a] = ext.get(a, Fraction(0)) + mass * (1 - r)
        ext[b] = ext.get(b, Fraction(0)) + mass * r
    return prune(ext)


def part_a_achievability():
    """Shared-r erasure channel: I(Q;Z|P) == (1-r)H(Q|P),
    E[d] == r*H(Q|P), hence R(D_r) == I with D_r == E[d], exactly."""
    rgrid = [Fraction(i, 10) for i in range(11)]
    worlds = part_a_worlds()
    stats = dict(worlds=len(worlds), pairs_checked=0, failures=[])
    for probs, P, qmap in worlds:
        tab = q_p_table(probs, P, qmap)
        Hqp = h_q_given_p(tab)
        # independent chain-rule certificate: H(Q|P) == sum_p p_p H(Q|p)
        fib = {}
        for sub in fibre_subtables(tab).values():
            fe = cond_h_m(sub, [1], [2])  # atoms (h,P,Q): marginalize!
            fib = expr_plus(fib, fe)
        if not expr_is_zero(expr_diff(Hqp, fib)):
            stats["failures"].append(("chainrule", probs, P, qmap))
            continue
        for r in rgrid:
            ext = build_ext(tab, lambda q, p, r=r: r)
            I = cmi_m(ext, [0], [3], [1])
            Ed = distortion_expr(ext)
            ok_I = expr_is_zero(expr_diff(I, expr_scale(1 - r, Hqp)))
            ok_E = expr_is_zero(expr_diff(Ed, expr_scale(r, Hqp)))
            # R(D_r) = max(H - D, 0) attained: I == H - E[d] >= 0
            ok_R = expr_is_zero(expr_diff(I, expr_diff(Hqp, Ed)))
            ok_nonneg = expr_to_dec(I) >= -EPS
            stats["pairs_checked"] += 1
            if not (ok_I and ok_E and ok_R and ok_nonneg):
                stats["failures"].append(
                    ("achieve", r, ok_I, ok_E, ok_R, ok_nonneg))
                return stats
    return stats


def distortion_expr(ext):
    """E[d] under the registered erasure metric
    d(q, q')=0, d(q, e | P=p) = H(Q|P=p):  sum over erasure atoms of
    mass * H(Q|p), exact."""
    total = {}
    subs = fibre_subtables(ext)
    for p, sub in subs.items():
        e_mass = sum((m for k, m in sub.items() if k[2] == 0),
                     Fraction(0))
        if e_mass == 0:
            continue
        p_mass = sum(sub.values(), Fraction(0))
        # cond_h_m marginalizes (Q,P): == p_p * H(Q|p)  (fibre-local)
        fe = cond_h_m(sub, [1], [0])
        total = expr_plus(total, expr_scale(e_mass / p_mass, fe))
    return total


def part_a_worlds():
    """Small exhaustive n=3 worlds plus sampled n=4/5."""
    out = []
    from llm_epistemics_common import rational_distributions, rgs_partitions
    probs3 = [Fraction(1, 3)] * 3, [Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)]
    for probs in probs3:
        n = len(probs)
        for P in rgs_partitions(n):
            for bits in itertools.product((0, 1), repeat=n):
                if len(set(bits)) < 2:
                    continue  # target must be non-constant
                out.append((list(probs), list(P), list(bits)))
    rng = random.Random(20260901)
    dcount = 0
    for n in (4, 5):
        for probs in rational_distributions(n, n, n + 2):
            dcount += 1
            if dcount % 5 != 0:
                continue
            P = rng.choice(list(rgs_partitions(n)))
            bits = tuple(rng.randint(0, 1) for _ in range(n))
            if len(set(bits)) < 2:
                bits = tuple(i % 2 for i in range(n))
            out.append((list(probs), list(P), list(bits)))
    return out


def part_a_converse():
    """Registered-class tightness.  The REGISTERED channel class is
    reveal/erasure with Theta independent of Q given the fibre
    (per-fibre erasure probability r_p).  Within this class verify
    exactly

        I(Q;Z|P) == H(Q|P) - E[d]

    (achievability = converse; the time-sharing line is tight), plus
    the independent sub-identity
        H(Q|Z,P) == sum_p P(e,p) H(Q|p).

    SCOPE (recorded, not checked as a theorem): Q-DEPENDENT erasure
    (Theta coupled to Q within a fibre) leaves the finite-distortion
    regime but can achieve I(Q;Z|P) < H(Q|P) - E[d] — the log-loss
    converse R >= H - D does NOT extend beyond the registered class
    under the erasure metric.  Counterexample frozen below."""
    scope_counterexample = {
        "Q_marginal": ["9/10", "1/10"],
        "erasure_probs": {"Q=0": "1/10", "Q=1": "9/10"},
        "note": "P(e)=9/50; I(Q;Z) = H(Q) - 9/50 bits < H(Q) - E[d] = H(Q)*(1 - 9/50) bits since H(Q) < 1 bit",
    }
    G = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4),
         Fraction(1)]
    worlds = part_a_worlds()[:14]
    stats = dict(worlds=0, channels=0, failures=[],
                 scope_counterexample=scope_counterexample)
    for probs, P, qmap in worlds:
        tab = q_p_table(probs, P, qmap)
        Hqp = h_q_given_p(tab)
        fibres = sorted({p for (_, p, _) in tab})
        combos = list(itertools.product(G, repeat=len(fibres)))
        rng = random.Random(20260902)
        if len(combos) > 900:
            combos = rng.sample(combos, 900)
        stats["worlds"] += 1
        for rvec in combos:
            rmap = dict(zip(fibres, rvec))
            ext = build_ext(tab, lambda q, p: rmap[p])
            I = cmi_m(ext, [0], [3], [1])
            Ed = distortion_expr(ext)
            # exact registered-class tightness
            ok_eq = expr_is_zero(expr_diff(I, expr_diff(Hqp, Ed)))
            # independent sub-identity for H(Q|Z,P)
            hqzp = cond_h_m(ext, [1, 3], [0])
            rhs = {}
            for sub in fibre_subtables(ext).values():
                pm = sum(sub.values(), Fraction(0))
                em = sum((m for k2, m in sub.items() if k2[2] == 0),
                         Fraction(0))
                if em:
                    rhs = expr_plus(
                        rhs, expr_scale(em / pm, cond_h_m(sub, [1], [0])))
            ok_sub = expr_is_zero(expr_diff(hqzp, rhs))
            ok_ineq = (expr_to_dec(I)
                       >= expr_to_dec(Hqp) - expr_to_dec(Ed) - EPS)
            stats["channels"] += 1
            if not (ok_eq and ok_sub and ok_ineq):
                stats["failures"].append((str(rmap), ok_eq, ok_sub,
                                          ok_ineq))
                return stats
    return stats


def ci_table(fibres):
    """Cleaner builder: fibres = [(p_label, p_mass, [w_1, .., w_k])]."""
    tab = {}
    for plabel, pm, ws in fibres:
        for qs in itertools.product(*[range(len(w)) for w in ws]):
            m = pm
            for i, q in enumerate(qs):
                m *= ws[i][q]
            tab[tuple(qs) + (plabel,)] = m
    return tab


def part_b_product():
    """Additivity for conditionally independent Q_i|P and the product
    sum at the normalized distortion grid {0,.25,.5,.75,1}:
    shared-Theta:  I(joint) == (1-r) * sum_i H_i,  E[d] == r * sum_i H_i;
    per-coordinate Theta_i:  I(joint) == sum_i (1-r_i) H_i,
    E[d] == sum_i r_i H_i  (coordinate-wise independent erasure)."""
    grid = [Fraction(i, 4) for i in range(5)]
    W2 = [Fraction(1, 2)]
    W3 = [Fraction(1, 3), Fraction(1, 4), Fraction(2, 3)]
    stats = dict(worlds=0, checks=0, failures=[])
    worlds = [
        [("p0", Fraction(1, 3), [[Fraction(1, 2), Fraction(1, 2)],
                                 [Fraction(1, 4), Fraction(3, 4)]]),
         ("p1", Fraction(2, 3), [[Fraction(3, 4), Fraction(1, 4)],
                                 [Fraction(1, 2), Fraction(1, 2)]])],
        [("p0", Fraction(1, 5), [[Fraction(1, 3), Fraction(2, 3)],
                                 [Fraction(2, 5), Fraction(3, 5)],
                                 [Fraction(1, 2), Fraction(1, 2)]]),
         ("p1", Fraction(4, 5), [[Fraction(1, 4), Fraction(3, 4)],
                                 [Fraction(1, 6), Fraction(5, 6)],
                                 [Fraction(3, 4), Fraction(1, 4)]])],
        [("p0", Fraction(1, 2), [[Fraction(1, 2), Fraction(1, 2)],
                                 [Fraction(1, 2), Fraction(1, 2)]]),
         ("p1", Fraction(1, 4), [[Fraction(1, 8), Fraction(7, 8)],
                                 [Fraction(5, 8), Fraction(3, 8)]]),
         ("p2", Fraction(1, 4), [[Fraction(1, 3), Fraction(2, 3)],
                                 [Fraction(1, 5), Fraction(4, 5)]])],
    ]
    for fibres in worlds:
        k = len(fibres[0][2])
        qcols = list(range(k))
        pcol = k
        tab = ci_table(fibres)
        Hj = cond_h_m(tab, [pcol], qcols)
        Hs = [cond_h_m(tab, [pcol], [i]) for i in qcols]
        add = Hs[0]
        for e in Hs[1:]:
            add = expr_plus(add, e)
        if not expr_is_zero(expr_diff(Hj, add)):
            stats["failures"].append(("additivity", fibres))
            return stats
        stats["worlds"] += 1
        # shared-Theta erasure of the JOINT (registered d(e|p)=Hjoint|p)
        for r in grid:
            # joint reveal/erasure: cols (Q1..Qk, P, Th, Z)
            extj = {}
            for key, m in tab.items():
                qs, p = key[:k], key[k]
                for th, w in ((1, 1 - r), (0, r)):
                    z = qs if th else "e"  # reveal carries the VALUE
                    ek = qs + (p, th, z)
                    extj[ek] = extj.get(ek, Fraction(0)) + m * w
            extj = prune(extj)
            I = cmi_m(extj, qcols, [k + 2], [k])
            Ed = joint_distortion_expr(extj, k)
            ok_I = expr_is_zero(expr_diff(I, expr_scale(1 - r, Hj)))
            ok_E = expr_is_zero(expr_diff(Ed, expr_scale(r, Hj)))
            stats["checks"] += 1
            if not (ok_I and ok_E):
                stats["failures"].append(("shared", r, ok_I, ok_E))
                return stats
        # per-coordinate independent Theta_i: rate + distortion split
        for rvec in itertools.product(grid, repeat=k):
            extc = {}
            for key, m in tab.items():
                qs, p = key[:k], key[k]
                for reveals in itertools.product((0, 1), repeat=k):
                    zz = tuple(qs[i] if reveals[i] else "e"
                               for i in range(k))
                    w = Fraction(1)
                    for i in range(k):
                        w *= (1 - rvec[i]) if reveals[i] else rvec[i]
                    ek = qs + (p,) + reveals + (zz,)
                    extc[ek] = extc.get(ek, Fraction(0)) + m * w
            extc = prune(extc)
            # cols: Q1..Qk(0..k-1), P(k), Th1..Thk(k+1..2k), Z(2k+1,
            # a single tuple column)
            I = cmi_m(extc, qcols, [2 * k + 1], [k])
            Is = {}
            for i in range(k):
                Is = expr_plus(Is, expr_scale(1 - rvec[i], Hs[i]))
            Ed = {}
            for sub in fibre_subtables(extc, pcol=k).values():
                pm = sum(sub.values(), Fraction(0))
                for i in range(k):
                    ei = sum((m for kk, m in sub.items()
                              if kk[k + 1 + i] == 0), Fraction(0))
                    if ei:
                        # registered d_i(e|p) = H(Q_i|P=p): PER-FIBRE
                        fe = cond_h_m(sub, [k], [i])
                        Ed = expr_plus(Ed, expr_scale(ei / pm, fe))
            ok_I = expr_is_zero(expr_diff(I, Is))
            ok_E = expr_is_zero(expr_diff(Ed, expr_diff(Hj, Is)))
            stats["checks"] += 1
            if not (ok_I and ok_E):
                stats["failures"].append(("percoord", rvec, ok_I, ok_E))
                return stats
    return stats


def joint_distortion_expr(extj, k):
    """E[d] for the joint registered erasure metric
    d(q, q')=0, d(q, e | p) = H(Q_1..Q_k | P=p)."""
    total = {}
    for sub in fibre_subtables(extj, pcol=k).values():
        em = sum((m for kk, m in sub.items() if kk[k + 1] == 0),
                 Fraction(0))
        if em == 0:
            continue
        pm = sum(sub.values(), Fraction(0))
        fe = cond_h_m(sub, [k], list(range(k)))
        total = expr_plus(total, expr_scale(em / pm, fe))
    return total


def part_c_controls():
    """Correlated controls, k=2, exact inflation
    infl = H(Q1|P) + H(Q2|P) - H(Q1Q2|P):
      Q2=Q1            infl == H(Q1|P)
      Q1 = f(Q2)       infl == H(Q1|Q2,P)   (chain rule)
      partially corr.  infl == I(Q1;Q2|P)    (exact CMI)
      independent      infl == 0
    Only the inflation values are recorded — no independent-novelty
    credit quantity is computed or emitted anywhere."""
    stats = dict(worlds=0, failures=[], inflation_bits={})
    rng = random.Random(20260903)

    def infl_of(tab):
        Hj = cond_h_m(tab, [2], [0, 1])
        H1 = cond_h_m(tab, [2], [0])
        H2 = cond_h_m(tab, [2], [1])
        return expr_diff(expr_plus(H1, H2), Hj), Hj, H1, H2

    # --- Q2 = Q1 (shared exact target) ---
    w_tab = {}
    for plabel, w in (("p0", [Fraction(1, 2), Fraction(1, 2)]),
                      ("p1", [Fraction(1, 4), Fraction(3, 4)])):
        pm = Fraction(1, 3) if plabel == "p0" else Fraction(2, 3)
        for q in range(2):
            w_tab[(q, q, plabel)] = pm * w[q]
    infl, Hj, H1, H2 = infl_of(w_tab)
    cmi = cmi_m(w_tab, [0], [1], [2])
    ok = expr_is_zero(expr_diff(infl, cmi))
    # structural certificate: Q2=Q1  =>  H(Q2|Q1,P) = 0 and infl = H1
    ok_det = expr_is_zero(cond_h_m(w_tab, [0, 2], [1]))
    ok_h1 = expr_is_zero(expr_diff(infl, H1))
    stats["worlds"] += 1
    stats["inflation_bits"]["Q2_equals_Q1"] = str(expr_to_dec(infl))
    if not (ok and ok_det and ok_h1):
        stats["failures"].append(("Q2=Q1", ok, ok_det, ok_h1))
        return stats

    # --- Q1 = f(Q2), f non-injective (Q2 ternary, Q1 binary parity-ish) ---
    f_tab = {}
    for plabel, w2 in (("p0", [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]),
                       ("p1", [Fraction(1, 8), Fraction(3, 8), Fraction(1, 2)])):
        pm = Fraction(2, 5) if plabel == "p0" else Fraction(3, 5)
        for q2 in range(3):
            q1 = q2 % 2  # f: 0->0, 1->1, 2->0  (non-injective)
            f_tab[(q1, q2, plabel)] = pm * w2[q2]
    infl, Hj, H1, H2 = infl_of(f_tab)
    cmi = cmi_m(f_tab, [0], [1], [2])
    ok = expr_is_zero(expr_diff(infl, cmi))
    # structural certificate: Q1 = f(Q2)  =>  H(Q1|Q2,P) = 0
    ok_det = expr_is_zero(cond_h_m(f_tab, [1, 2], [0]))
    stats["worlds"] += 1
    stats["inflation_bits"]["Q1_deterministic_function_of_Q2"] = \
        str(expr_to_dec(infl))
    if not (ok and ok_det):
        stats["failures"].append(("Q1=f(Q2)", ok, ok_det))
        return stats

    # --- partially correlated rational joints (neither degenerate nor
    #     independent), random rational within-fibre joints ---
    for trial in range(300):
        p_tab = {}
        for plabel in ("p0", "p1"):
            while True:
                num = [rng.randint(1, 9) for _ in range(4)]
                den = sum(num)
                w = [Fraction(x, den) for x in num]
                row_marg = [w[0] + w[1], w[2] + w[3]]
                col_marg = [w[0] + w[2], w[1] + w[3]]
                # non-degenerate coordinates, not independent
                if (all(0 < x < 1 for x in row_marg + col_marg)
                        and w[0] * w[3] != w[1] * w[2]):
                    break
            pm = Fraction(1, 3) if plabel == "p0" else Fraction(2, 3)
            for i in range(2):
                for j in range(2):
                    p_tab[(i, j, plabel)] = pm * w[2 * i + j]
        infl, Hj, H1, H2 = infl_of(p_tab)
        cmi = cmi_m(p_tab, [0], [1], [2])
        ok = expr_is_zero(expr_diff(infl, cmi))
        stats["worlds"] += 1
        if not ok:
            stats["failures"].append(("partial", trial))
            return stats
        stats["inflation_bits"].setdefault(
            "partially_correlated_pairs_checked", 0)
        stats["inflation_bits"]["partially_correlated_pairs_checked"] += 1

    # --- independent control: inflation == 0 exactly ---
    i_tab = {}
    for plabel, (w1, w2) in (
            ("p0", ([Fraction(1, 2), Fraction(1, 2)],
                    [Fraction(1, 4), Fraction(3, 4)])),
            ("p1", ([Fraction(3, 4), Fraction(1, 4)],
                    [Fraction(1, 2), Fraction(1, 2)]))):
        pm = Fraction(1, 3) if plabel == "p0" else Fraction(2, 3)
        for i in range(2):
            for j in range(2):
                i_tab[(i, j, plabel)] = pm * w1[i] * w2[j]
    infl, Hj, H1, H2 = infl_of(i_tab)
    ok = expr_is_zero(infl)
    stats["worlds"] += 1
    stats["inflation_bits"]["independent_pair"] = "0"
    if not ok:
        stats["failures"].append(("independent",))
        return stats
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    out = {
        "schema": "orion.51.logloss-parent-benchmark.v1",
        "spec": "MECHANICAL_EXECUTION_SPEC_V4.md section 11",
        "construction": "registered reveal/erasure, exact rational arithmetic",
        "independent_novelty_credit": "none_emitted",
    }
    a1 = part_a_achievability()
    ok_a1 = not a1["failures"]
    record("A_achievability_shared_r", "PASS" if ok_a1 else "FAIL")
    a2 = part_a_converse()
    ok_a2 = not a2["failures"]
    record("A_registered_class_tightness", "PASS" if ok_a2 else "FAIL")
    b = part_b_product()
    ok_b = not b["failures"]
    record("B_cond_independent_product_sum", "PASS" if ok_b else "FAIL")
    c = part_c_controls()
    ok_c = not c["failures"]
    record("C_correlated_controls_exact_inflation",
           "PASS" if ok_c else "FAIL")
    out["part_a_achievability"] = a1
    out["part_a_converse"] = a2
    out["part_b_product"] = b
    out["part_c_controls"] = {
        "worlds": c["worlds"],
        "inflation_bits": c["inflation_bits"],
        "failures": [str(f) for f in c["failures"]],
    }
    out["verdicts"] = dict(VERDICTS)
    out["overall"] = "PASS" if all(
        v == "PASS" for _, v in VERDICTS) else "FAIL"
    dump_json(Path(args.output), out)
    for cid, verdict in VERDICTS:
        print(f"CHECK {cid} {verdict}")
    print(f"OVERALL {out['overall']}")
    print(f"worlds A1={a1['worlds']} pairs={a1['pairs_checked']} "
          f"A2={a2['worlds']} channels={a2['channels']} "
          f"B={b['worlds']} checks={b['checks']} C={c['worlds']}")
    return 0 if out["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
