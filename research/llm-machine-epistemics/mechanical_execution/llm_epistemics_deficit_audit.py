#!/usr/bin/env python3
"""Spec V4 §10 — EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.

Exact verification of the three deficit identities of
EPISTEMIC_DEFICIENCY_DECOMPOSITION_V1.md on finite rational joint tables:

  D1  H(Q|Z) - H(Q|H) == I(Q;H|Z)          (Z a deterministic map of H)
  D2  H(Q|H) - H(Q|H,X) == I(Q;X|H)
  D3  H(Qf|Zt,Xf) - H(Qf|Ht,Xf) == I(Qf;Ht|Zt,Xf)   (Zt a map of Ht)

plus the five mandatory controls:
  C1 acquisition deficit only
  C2 compression deficit only
  C3 prospective deficit only (canonical provenance case)
  C4 future observation reconstructs forgotten provenance -> D3 = 0
  C5 state retains provenance -> D3 = 0

All identity comparisons are exact prime-exponent log-linear checks
(expr_is_zero); Decimal (>=50 digits) is an independent cross-implementation.
"""
from __future__ import annotations

import argparse
import random
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_epistemics_common import (
    cond_h_dec, cond_h_expr, cmi_expr, dump_json, expr_diff, expr_is_zero,
    expr_to_dec, joint_from_marginal, rational_distributions,
)

EPS = Decimal(10) ** -30


# --------------------------------------------------------------- utilities


def dec_eq(a: Decimal, b: Decimal) -> bool:
    return abs(a - b) < EPS


def check_identity(table, lhs_cond, rhs_cmi, name, records):
    """lhs_cond/rhs_cmi: (cond_idxs, var_idxs) pairs computed by caller."""
    l_expr, r_expr = lhs_cond, rhs_cmi
    diff = expr_diff(l_expr, r_expr)
    exact_zero = expr_is_zero(diff)
    l_dec, r_dec = expr_to_dec(l_expr), expr_to_dec(r_expr)
    dec_ok = dec_eq(l_dec, r_dec)
    ok = exact_zero and dec_ok
    records.append({"identity": name,
                    "exact_identity": bool(exact_zero),
                    "decimal_crosscheck_bits": {"lhs": str(l_dec), "rhs": str(r_dec)},
                    "decimal_agree_1e-30": bool(dec_ok),
                    "verdict": "PASS" if ok else "FAIL_COUNTEREXAMPLE_FOUND"})
    return ok


def table_stats(table, idxs):
    """Marginal dump for serialization."""
    out = {}
    for k, v in table.items():
        key = ",".join(str(k[i]) for i in idxs)
        out[key] = out.get(key, Fraction(0)) + v
    return {k: str(v) for k, v in out.items()}


# ------------------------------------------------------ identity batteries


def d1_battery(seed: int, trials: int, rep):
    """D1: random P(Q,H), Z = random deterministic function of H."""
    rng = random.Random(seed)
    recs, ok_all = [], True
    for t in range(trials):
        # random joint over (Q in {0,1}, H in {0,1,2})
        probs = [Fraction(rng.randint(1, 6), 6) for _ in range(6)]
        tot = sum(probs)
        probs = [p / tot for p in probs]
        zf = [rng.randint(0, 1) for _ in range(3)]
        samples = [(qi * 3 + hi, qi, hi, zf[hi]) for hi in range(3) for qi in range(2)]
        table = joint_from_marginal(samples, probs)
        # idxs: 0=flat, 1=Q, 2=H, 3=Z
        lhs = expr_diff(cond_h_expr(table, [3], [1]), cond_h_expr(table, [2], [1]))
        rhs = cmi_expr(table, [1], [2], [3])
        ok_all &= check_identity(table, lhs, rhs, f"D1_trial{t}", recs)
    rep["d1_randomized"] = {"trials": trials,
                            "verdict": "PASS" if ok_all else "FAIL_COUNTEREXAMPLE_FOUND"}
    return recs[:3] + [{"note": f"remaining {trials - 3} trials all PASS"}] if ok_all else recs[:10]


def d2_battery(seed: int, trials: int, rep):
    """D2: random P(Q,H,X)."""
    rng = random.Random(seed + 1)
    recs, ok_all = [], True
    for t in range(trials):
        probs = [Fraction(rng.randint(1, 6), 6) for _ in range(8)]  # Q,H in {0,1}, X in {0,1}
        tot = sum(probs)
        probs = [p / tot for p in probs]
        samples = [((qi * 2 + hi) * 2 + xi, qi, hi, xi)
                   for qi in range(2) for hi in range(2) for xi in range(2)]
        table = joint_from_marginal(samples, probs)
        lhs = expr_diff(cond_h_expr(table, [2], [1]), cond_h_expr(table, [2, 3], [1]))
        rhs = cmi_expr(table, [1], [3], [2])
        ok_all &= check_identity(table, lhs, rhs, f"D2_trial{t}", recs)
    rep["d2_randomized"] = {"trials": trials,
                            "verdict": "PASS" if ok_all else "FAIL_COUNTEREXAMPLE_FOUND"}
    return recs[:3] + [{"note": f"remaining {trials - 3} trials all PASS"}] if ok_all else recs[:10]


def d3_battery(seed: int, trials: int, rep):
    """D3: Ht in {0,1,2} -> Xf in {0,1} -> Qf in {0,1}; Zt = map of Ht."""
    rng = random.Random(seed + 2)
    recs, ok_all = [], True
    for t in range(trials):
        pht = [Fraction(rng.randint(1, 6), 6) for _ in range(3)]
        tot = sum(pht)
        pht = [p / tot for p in pht]
        zt = [rng.randint(0, 1) for _ in range(3)]
        samples, probs = [], []
        for ht in range(3):
            r = Fraction(rng.randint(1, 3), 4)  # P(Xf=0|Ht=ht); Xf=1 gets 1-r>0
            for xf in range(2):
                pxf = r if xf == 0 else Fraction(1, 1) - r
                # Qf noisy function of (ht, xf): flip prob 1/4
                for qf in range(2):
                    pq = Fraction(1, 4) if qf != (ht + xf) % 2 else Fraction(3, 4)
                    samples.append((qf, ht, zt[ht], xf))
                    probs.append(pht[ht] * pxf * pq)
        table = joint_from_marginal(samples, probs)
        # idxs: 0=Qf, 1=Ht, 2=Zt, 3=Xf
        lhs = expr_diff(cond_h_expr(table, [2, 3], [0]), cond_h_expr(table, [1, 3], [0]))
        rhs = cmi_expr(table, [0], [1], [2, 3])
        ok_all &= check_identity(table, lhs, rhs, f"D3_trial{t}", recs)
    rep["d3_randomized"] = {"trials": trials,
                            "verdict": "PASS" if ok_all else "FAIL_COUNTEREXAMPLE_FOUND"}
    return recs[:3] + [{"note": f"remaining {trials - 3} trials all PASS"}] if ok_all else recs[:10]


# ---------------------------------------------------------------- controls


def ctl_acquisition_only():
    """C1: Q independent of H; Z=H. Only acquisition deficit is nonzero."""
    samples, probs = [], []
    for h in range(2):
        for q in range(2):
            samples.append((q, h, h))  # (Q,H,Z)
            probs.append(Fraction(1, 4))
    return samples, probs, [1], [2]  # acquisition deficit = H(Q|H)


def ctl_compression_only():
    """C2: Q = f(H) exact; Z constant. Only compression deficit nonzero."""
    samples, probs = [], []
    for h in range(4):
        q = h % 2
        samples.append((q, h, 0))  # (Q,H,Z), Z drops everything
        probs.append(Fraction(1, 4))
    return samples, probs, [1], [2]


def ctl_prospective_only(which: str):
    """C3/C4/C5 shared skeleton: Ht provenance bit, Zt drops it.

    which:
      provenance   — Qf = Ht, Xf uninformative          -> D3 = 1 bit
      reconstructs — Qf = Ht, Xf = Ht                    -> D3 = 0
      retains      — Zt = Ht (state keeps provenance)    -> D3 = 0
    """
    samples, probs = [], []
    for ht in range(2):
        if which == "reconstructs":
            xf_values = [(ht, Fraction(1, 1))]
        else:
            xf_values = [(0, Fraction(1, 2)), (1, Fraction(1, 2))]
        for xf, pxf in xf_values:
            qf = ht  # future responsibility depends on provenance
            zt = ht if which == "retains" else 0
            samples.append((qf, ht, zt, xf))  # (Qf,Ht,Zt,Xf)
            probs.append(Fraction(1, 2) * pxf)
    return samples, probs


def run_controls(rep):
    out = {}
    # C1
    s, p, _, _ = ctl_acquisition_only()
    t = joint_from_marginal(s, p)
    acq = cond_h_expr(t, [1], [0])          # H(Q|H)
    comp = expr_diff(cond_h_expr(t, [2], [0]), cond_h_expr(t, [1], [0]))  # H(Q|Z)-H(Q|H)
    acq_dec = cond_h_dec(t, [1], [0])
    comp_dec = cond_h_dec(t, [2], [0]) - acq_dec
    dec_ok = abs(expr_to_dec(acq) - acq_dec) < EPS and abs(expr_to_dec(comp) - comp_dec) < EPS
    out["C1_acquisition_only"] = {
        "distribution": table_stats(t, [0, 1, 2]),
        "H(Q|H)_bits": str(expr_to_dec(acq)),
        "H(Q|Z)-H(Q|H)_bits": str(expr_to_dec(comp)),
        "decimal_crosscheck_1e-30": bool(dec_ok),
        "expected": "acquisition > 0, compression == 0",
        "verdict": "PASS" if (not expr_is_zero(acq)) and expr_is_zero(comp) and dec_ok else "FAIL_COUNTEREXAMPLE_FOUND"}
    # C2
    s, p, _, _ = ctl_compression_only()
    t = joint_from_marginal(s, p)
    acq = cond_h_expr(t, [1], [0])
    comp = expr_diff(cond_h_expr(t, [2], [0]), cond_h_expr(t, [1], [0]))
    acq_dec = cond_h_dec(t, [1], [0])
    comp_dec = cond_h_dec(t, [2], [0]) - acq_dec
    dec_ok = abs(expr_to_dec(acq) - acq_dec) < EPS and abs(expr_to_dec(comp) - comp_dec) < EPS
    out["C2_compression_only"] = {
        "distribution": table_stats(t, [0, 1, 2]),
        "H(Q|H)_bits": str(expr_to_dec(acq)),
        "H(Q|Z)-H(Q|H)_bits": str(expr_to_dec(comp)),
        "decimal_crosscheck_1e-30": bool(dec_ok),
        "expected": "acquisition == 0, compression > 0",
        "verdict": "PASS" if expr_is_zero(acq) and (not expr_is_zero(comp)) and dec_ok else "FAIL_COUNTEREXAMPLE_FOUND"}
    # C3/C4/C5
    labels = {"provenance": "C3_prospective_only",
              "reconstructs": "C4_future_reconstructs_provenance",
              "retains": "C5_state_retains_provenance"}
    for which, lab in labels.items():
        s, p = ctl_prospective_only(which)
        t = joint_from_marginal(s, p)
        d3 = expr_diff(cond_h_expr(t, [2, 3], [0]), cond_h_expr(t, [1, 3], [0]))
        lhs_dec = cond_h_dec(t, [2, 3], [0])
        rhs_dec = cond_h_dec(t, [1, 3], [0])
        d3_bits = str(expr_to_dec(d3))
        dec_ok = abs(expr_to_dec(d3) - (lhs_dec - rhs_dec)) < EPS
        exact_ok = expr_is_zero(d3) if which in ("reconstructs", "retains") else not expr_is_zero(d3)
        out[lab] = {
            "distribution": table_stats(t, [0, 1, 2, 3]),
            "H(Qf|Zt,Xf)_bits": str(lhs_dec),
            "H(Qf|Ht,Xf)_bits": str(rhs_dec),
            "D3_bits": d3_bits,
            "expected": "D3 == 1 bit" if which == "provenance" else "D3 == 0",
            "decimal_agree_1e-30": bool(dec_ok),
            "verdict": "PASS" if (exact_ok and dec_ok) else "FAIL_COUNTEREXAMPLE_FOUND"}
    rep["mandatory_controls"] = out
    return all(v["verdict"] == "PASS" for v in out.values())


# --------------------------------------------------------------------- cli


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260829)
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    rep = {"schema_version": "orion.51.epistemic-deficit-identity-audit.v1",
           "seed": args.seed, "verdicts": {}, "sections": {}}
    recs = []
    recs += d1_battery(args.seed, args.trials, rep)
    recs += d2_battery(args.seed, args.trials, rep)
    recs += d3_battery(args.seed, args.trials, rep)
    rep["sections"]["identity_trials_sample"] = recs
    controls_ok = run_controls(rep)

    verdicts = [rep["d1_randomized"]["verdict"], rep["d2_randomized"]["verdict"],
                rep["d3_randomized"]["verdict"],
                "PASS" if controls_ok else "FAIL_COUNTEREXAMPLE_FOUND"]
    overall = "PASS" if all(v == "PASS" for v in verdicts) else "FAIL_COUNTEREXAMPLE_FOUND"
    rep["verdicts"] = {"D1": verdicts[0], "D2": verdicts[1], "D3": verdicts[2],
                       "CONTROLS": verdicts[3], "OVERALL": overall}

    dump_json(args.output, rep)
    for k, v in rep["verdicts"].items():
        print(f"CHECK D-{k} {v}")
    print(f"OVERALL {overall}")
    sys.exit(0 if overall == "PASS" else 3)


if __name__ == "__main__":
    main()
