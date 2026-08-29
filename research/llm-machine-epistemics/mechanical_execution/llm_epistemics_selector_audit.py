#!/usr/bin/env python3
"""Spec V3 §5 — RESPONSIBILITY_SELECTOR_AUDIT_V1.

Verifies the responsibility-decision cost semantics of
RESPONSIBILITY_DECISION_QUOTIENT_V2.md exactly (prime-exponent log algebra):

  R21  min-selector entropy == min conditional entropy over valid
        action-sufficient state partitions (per predictive fibre);
  R22  canonical-action cost H(tau(H)|P) with registered tie rule;
  R23  optimal-action-set cost H(A*(H)|P);  chain R21 <= R22 <= R23;
  R24  action-and-risk cost H((d,rho)|P) + chain-rule marginal H(rho|P,d);
  R25  exact-target special case reduces to H(Q|P);
  R26  joint family cost == joint-partition minimum; witness where joint
       optimization strictly beats the sum of individually minimized costs;
  R27  zero cost iff common optimal action inside every predictive fibre.

Mandatory fixtures: §5.2 tie fixture, §5.3 exact-target control.
"""
from __future__ import annotations

import argparse
import itertools
import random
import sys
import time
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_epistemics_common import (
    block_of, dump_json, expr_add, expr_diff, expr_is_zero, expr_to_dec,
    intersect_all, rgs_partitions, rational_distributions,
)

LN2_EXPR = {2: Fraction(1)}  # exactly 1 bit
EPS = Decimal(10) ** -40  # Decimal-safe epsilon (never mix with float)


def expr_scale(e: dict, c: Fraction) -> dict:
    return {p: c * v for p, v in e.items() if c * v != 0}


def expr_eq(a: dict, b: dict) -> bool:
    return expr_is_zero(expr_diff(a, b))


def fibre_entropy_of_map(probs, values) -> dict:
    """Exact nats of the distribution induced by `values` within one fibre."""
    acc: dict = {}
    for p, v in zip(probs, values):
        acc[v] = acc.get(v, Fraction(0)) + p
    e = {}
    for q in acc.values():
        expr_add(e, q, 1 / q)
    return e


def min_selector(probs, astar):
    """(dec, expr, choice) minimising kernel entropy over valid selectors."""
    best = None
    for choice in itertools.product(*[sorted(s) for s in astar]):
        e = fibre_entropy_of_map(probs, list(choice))
        d = expr_to_dec(e)
        if best is None or d < best[0]:
            best = (d, e, choice)
    return best


def all_min_selectors(probs, astar):
    """Every selector attaining the exact minimum kernel entropy."""
    best = min_selector(probs, astar)
    out = []
    for choice in itertools.product(*[sorted(s) for s in astar]):
        e = fibre_entropy_of_map(probs, list(choice))
        if expr_eq(e, best[1]):
            out.append(choice)
    return best, out


def min_valid_partition(probs, astar):
    """(dec, expr, partition) minimising entropy over fibre-valid partitions.

    A partition is fibre-valid iff every block has nonempty intersection of
    optimal-action sets (ANY_OPTIMAL_ACTION decodability).
    """
    k = len(probs)
    best = None
    for part in rgs_partitions(k):
        blocks = block_of(part)
        ok = True
        for b in blocks.values():
            inter = intersect_all([astar[h] for h in b])
            if not inter:
                ok = False
                break
        if not ok:
            continue
        e = fibre_entropy_of_map(probs, list(part))
        d = expr_to_dec(e)
        if best is None or d < best[0]:
            best = (d, e, part)
    return best


def any_cost(probs, astar) -> dict:
    """R21 per-fibre minimum selector entropy (exact nats expr)."""
    return min_selector(probs, astar)[1]


def canonical_cost(probs, astar, tau) -> dict:
    """R22: H(tau(A*(H))) with tie rule tau (lexicographic-smallest here)."""
    values = [tau(s) for s in astar]
    return fibre_entropy_of_map(probs, values)


def set_cost(probs, astar) -> dict:
    """R23: H(A*(H)) — the fixed set-valued signature."""
    values = [tuple(sorted(s)) for s in astar]
    return fibre_entropy_of_map(probs, values)


def common_action(probs, astar) -> bool:
    return bool(intersect_all(astar))


def audit(args):
    rng = random.Random(args.seed)
    rep = {"schema_version": "orion.51.responsibility-selector-audit.v1",
           "seed": args.seed, "verdicts": {}, "sections": {}}
    sections = rep["sections"]
    ok = {k: True for k in
          ("R21", "R22", "R23", "R24", "R25", "R26", "R27", "TIE")}

    # ---------------------------------------------------------- §5.2 fixture
    probs_tie = [Fraction(1, 2), Fraction(1, 2)]
    A_h1 = frozenset({"a", "b"})
    A_h2 = frozenset({"b", "c"})
    astar_tie = [A_h1, A_h2]
    tau_lex = lambda s: min(s)
    any_tie = any_cost(probs_tie, astar_tie)
    set_tie = set_cost(probs_tie, astar_tie)
    can_ab = fibre_entropy_of_map(probs_tie, ["a", "b"])  # canonical [a,b]
    can_bb = fibre_entropy_of_map(probs_tie, ["b", "b"])  # canonical [b,b]
    tie_ok = (expr_eq(any_tie, {}) and expr_eq(set_tie, LN2_EXPR)
              and expr_eq(can_ab, LN2_EXPR) and expr_eq(can_bb, {}))
    ok["TIE"] = tie_ok
    sections["tie_fixture"] = {
        "probs": ["1/2", "1/2"],
        "A_star": [["a", "b"], ["b", "c"]],
        "ANY_OPTIMAL_ACTION_bits": str(expr_to_dec(any_tie)),
        "OPTIMAL_ACTION_SET_bits": str(expr_to_dec(set_tie)),
        "canonical_ab_bits": str(expr_to_dec(can_ab)),
        "canonical_bb_bits": str(expr_to_dec(can_bb)),
        "expected": {"any": "0", "set": "1", "canonical_ab": "1",
                     "canonical_bb": "0"},
        "verdict": "PASS" if tie_ok else "FAIL_TIE_SEMANTICS",
    }

    # ------------------------------------------------- §5.3 exact-target R25
    r25_ok = True
    r25_trials = 0
    for t in range(args.trials):
        n = rng.randint(2, 5)
        dists = list(rational_distributions(n, 2, 8))
        probs = list(rng.choice(dists))
        nq = rng.randint(2, 4)
        Q = [rng.randrange(nq) for _ in range(n)]
        astar = [frozenset({q}) for q in Q]
        m = min_selector(probs, astar)[1]
        hq = fibre_entropy_of_map(probs, Q)
        r25_trials += 1
        if not expr_eq(m, hq):
            r25_ok = False
            sections.setdefault("r25_counterexample", []).append(
                {"probs": [str(p) for p in probs], "Q": Q})
            break
    ok["R25"] = r25_ok
    sections["exact_target_control"] = {
        "trials": r25_trials,
        "verdict": ("PASS" if r25_ok else "FAIL_COUNTEREXAMPLE_FOUND"),
    }

    # ------------------------------------------- generic R21/R22/R23/R27 grid
    r21_bad = r22_bad = r23_bad = r27_bad = 0
    trials = 0
    for t in range(args.trials):
        n = rng.randint(2, 5)
        dists = list(rational_distributions(n, 2, 8))
        probs = list(rng.choice(dists))
        na = rng.randint(2, 3)
        astar = []
        for _ in range(n):
            k = rng.randint(1, min(na, 2))
            astar.append(frozenset(rng.sample(range(na), k)))
        ms = min_selector(probs, astar)
        mp = min_valid_partition(probs, astar)
        if not expr_eq(ms[1], mp[1]):
            r21_bad += 1
            sections.setdefault("r21_counterexamples", []).append(
                {"probs": [str(p) for p in probs],
                 "A_star": [sorted(s) for s in astar],
                 "min_selector_bits": str(expr_to_dec(ms[1])),
                 "min_partition_bits": str(expr_to_dec(mp[1]))})
        can = canonical_cost(probs, astar, tau_lex)
        sc = set_cost(probs, astar)
        if expr_to_dec(can) < expr_to_dec(ms[1]) - EPS:
            r22_bad += 1
        if expr_to_dec(sc) < expr_to_dec(can) - EPS:
            r23_bad += 1
        zero_sel = expr_is_zero(ms[1])
        if zero_sel != common_action(probs, astar):
            r27_bad += 1
            sections.setdefault("r27_counterexamples", []).append(
                {"probs": [str(p) for p in probs],
                 "A_star": [sorted(s) for s in astar],
                 "min_selector_bits": str(expr_to_dec(ms[1])),
                 "common_action": common_action(probs, astar)})
        trials += 1
    ok["R21"] = r21_bad == 0
    ok["R22"] = r22_bad == 0
    ok["R23"] = r23_bad == 0
    ok["R27"] = r27_bad == 0
    sections["generic_grid"] = {
        "trials": trials, "distributions": "positive rationals, denominators 2..8",
        "R21_selector_equals_partition_min_violations": r21_bad,
        "R22_ge_R21_violations": r22_bad,
        "R23_ge_R22_violations": r23_bad,
        "R27_zero_cost_iff_common_action_violations": r27_bad,
    }

    # -------------------------------------------------------- §5.4 R26 joint
    fam = family_search(args, rng)
    ok["R26"] = fam["r26_ok"]
    sections["family_search"] = fam

    # --------------------------------------------------- R24 action + risk
    # Single predictive fibre {h1,h2}, equal prior. Registered target law:
    #   h1: P(Q=a)=P(Q=b)=1/2  -> A*={a,b}, rho=1/2
    #   h2: P(Q=b)=1           -> A*={b},   rho=0
    # Tie rule tau prefers b -> canonical d=(b,b): H(d|P)=0, but rho splits.
    pr = [Fraction(1, 2), Fraction(1, 2)]
    d_sig = ["b", "b"]
    rho_sig = [Fraction(1, 2), Fraction(0)]
    pairs = list(zip(d_sig, rho_sig))
    e_pair = fibre_entropy_of_map(pr, pairs)
    e_d = fibre_entropy_of_map(pr, d_sig)
    e_rho_given_d = cond_marginal_chain(pr, pairs, 0)
    chain_ok = expr_eq(e_pair, add_exprs(e_d, e_rho_given_d))
    r24_ok = expr_eq(e_pair, LN2_EXPR) and expr_is_zero(e_d) and chain_ok
    ok["R24"] = r24_ok
    sections["action_and_risk_fixture"] = {
        "fibre": "single predictive fibre, equal prior",
        "canonical_action": d_sig,
        "rho": ["1/2", "0"],
        "H_C_r_bits": str(expr_to_dec(e_pair)),
        "H_d_bits": str(expr_to_dec(e_d)),
        "H_rho_given_d_bits": str(expr_to_dec(e_rho_given_d)),
        "chain_rule_H_pair_equals_H_d_plus_H_rho_given_d": chain_ok,
        "expected": {"H_C_r": "1", "H_d": "0",
                     "marginal_risk": "1"},
        "verdict": "PASS" if r24_ok else "FAIL_COUNTEREXAMPLE_FOUND",
    }

    rep["verdicts"] = {
        "R21_ANY_OPTIMAL_MIN_SELECTOR_ENTROPY":
            "PASS" if ok["R21"] else "FAIL_COUNTEREXAMPLE_FOUND",
        "R22_CANONICAL_ACTION_COST":
            "PASS" if ok["R22"] else "FAIL_COUNTEREXAMPLE_FOUND",
        "R23_OPTIMAL_ACTION_SET_COST":
            "PASS" if ok["R23"] else "FAIL_COUNTEREXAMPLE_FOUND",
        "R24_ACTION_AND_RISK_COST":
            "PASS" if ok["R24"] else "FAIL_COUNTEREXAMPLE_FOUND",
        "R25_EXACT_TARGET_SPECIAL_CASE":
            "PASS" if ok["R25"] else "FAIL_COUNTEREXAMPLE_FOUND",
        "R26_JOINT_ANY_OPTIMAL_SELECTOR_COST":
            fam["verdict_R26"],
        "R27_ZERO_COST_COMMON_OPTIMAL_ACTION":
            "PASS" if ok["R27"] else "FAIL_COUNTEREXAMPLE_FOUND",
        "TIE_SEMANTICS_FIXTURE":
            "PASS" if ok["TIE"] else "FAIL_TIE_SEMANTICS",
    }
    return rep


def add_exprs(a: dict, b: dict) -> dict:
    out = dict(a)
    for p, e in b.items():
        out[p] = out.get(p, Fraction(0)) + e
    return {p: e for p, e in out.items() if e != 0}


def cond_marginal_chain(probs, pairs, cond_idx: int) -> dict:
    """H(rho | d) exactly from the joint (d,rho) distribution on one fibre."""
    from llm_epistemics_common import marginal
    table = {}
    for p, v in zip(probs, pairs):
        table[v] = table.get(v, Fraction(0)) + p
    md = marginal(table, [cond_idx])
    e = {}
    for key, pxy in table.items():
        expr_add(e, pxy, md[(key[cond_idx],)] / pxy)
    return e


# ------------------------------------------------------------ §5.4 family

def joint_stats_product(probs, astars):
    """Per-responsibility minima + joint minimum via full selector product.

    Only used where the product is small (n=2 exhaustive route)."""
    mins = [min_selector(probs, a) for a in astars]
    per_resp = [list(itertools.product(*[sorted(s) for s in a]))
                for a in astars]
    best = None
    for sel in itertools.product(*per_resp):
        values = list(zip(*sel))  # per-history tuple of actions
        e = fibre_entropy_of_map(probs, values)
        d = expr_to_dec(e)
        if best is None or d < best[0]:
            best = (d, e, sel)
    return mins, best


def selector_from_partition(part, astars):
    """Joint selector realising a valid partition: per block, the
    lexicographically smallest common action per coordinate."""
    blocks = block_of(part)
    cache = {}
    out = []
    for h, bid in enumerate(part):
        if bid not in cache:
            b = blocks[bid]
            cache[bid] = tuple(
                min(intersect_all([astars[i][h] for h in b]))
                for i in range(len(astars)))
        out.append(cache[bid])
    return out


def witness_rank(astars):
    return (sum(len(s) for s in astars),
            len(astars),
            tuple(tuple(sorted(s)) for r in astars for s in r))


def family_search(args, rng):
    """§5.4: exhaustive n=2/m=2/actions<=3; sampled extensions; joint==joint-
    partition-min check; freeze smallest strict-saving witness."""
    probs = [Fraction(1, 2), Fraction(1, 2)]
    subsets3 = [frozenset(c) for k in (1, 2, 3)
                for c in itertools.combinations(range(3), k)]
    best_witness = None
    best_witness2 = None
    witness_count = 0
    checked = 0
    joint_part_bad = 0
    indiv_not_joint = 0

    def consider(astars):
        nonlocal best_witness, witness_count, checked, joint_part_bad
        nonlocal indiv_not_joint
        checked += 1
        mins, best = joint_stats_product(probs, astars)
        alls = [all_min_selectors(probs, a) for a in astars]
        indiv_sum = sum(float(expr_to_dec(m[1])) for m in mins)
        joint_bits = float(best[0])
        # joint == min over jointly-valid partitions (rectangular validity)
        jp = min_valid_partition_joint(probs, astars)
        if not expr_eq(jp[1], best[1]):
            joint_part_bad += 1
        if indiv_sum > joint_bits + 1e-40:
            witness_count += 1
            rank = witness_rank(astars)
            if best_witness is None or rank < best_witness[0]:
                best_witness = (rank, {
                    "A_star": [[sorted(s) for s in r] for r in astars],
                    "probs": ["1/2", "1/2"],
                    "sum_individual_min_bits": str(indiv_sum),
                    "joint_min_bits": str(joint_bits),
                    "individual_minimizers": [list(m[2]) for m in mins],
                    "a_joint_minimizer": [list(s) for s in best[2]],
                })
        # do ALL individual-minimizer combos fail to be joint-minimizing?
        fail_all = True
        for combo in itertools.product(*[sel[1] for sel in alls]):
            values = list(zip(*combo))
            e = fibre_entropy_of_map(probs, values)
            if expr_eq(e, best[1]):
                fail_all = False
                break
        if fail_all:
            indiv_not_joint += 1
            rank = witness_rank(astars)
            if best_witness2 is None or rank < best_witness2[0]:
                best_witness2 = (rank, {
                    "A_star": [[sorted(s) for s in r] for r in astars],
                    "probs": ["1/2", "1/2"],
                    "individual_minimizers":
                        [sorted(sel[1]) for sel in alls],
                    "joint_min_bits": str(joint_bits),
                })

    # exhaustive n=2, m=2, actions<=3: 21^4 = 194481 families
    for a1h1 in subsets3:
        for a1h2 in subsets3:
            for a2h1 in subsets3:
                for a2h2 in subsets3:
                    consider([[a1h1, a1h2], [a2h1, a2h2]])
    exhaustive_count = checked

    # sampled extensions: n=2 m=3, and n=3..6 with m in {2,3}.
    # Joint minimum via the valid-partition route (O(B(n)) per family) plus a
    # reconstruction cross-check: the per-block lex-smallest common tuple is a
    # joint selector whose kernel entropy must equal the partition minimum.
    sample_counts = {}
    for n, m in [(2, 3), (3, 2), (3, 3), (4, 2), (5, 2), (6, 2), (6, 3)]:
        dists = list(rational_distributions(n, 2, 8))
        cnt = 0
        for _ in range(args.samples):
            p = list(rng.choice(dists))
            astars = []
            for _ in range(m):
                astars.append(
                    [frozenset(rng.sample(range(3), rng.randint(1, 2)))
                     for _ in range(n)])
            mins = [min_selector(p, a) for a in astars]
            jp = min_valid_partition_joint(p, astars)
            sel = selector_from_partition(jp[2], astars)
            e_sel = fibre_entropy_of_map(p, sel)
            if not expr_eq(e_sel, jp[1]):
                joint_part_bad += 1
            indiv_sum = sum(float(expr_to_dec(mm[1])) for mm in mins)
            joint_bits = float(expr_to_dec(jp[1]))
            if indiv_sum > joint_bits + 1e-40:
                witness_count += 1
            cnt += 1
        sample_counts[f"n={n},m={m}"] = cnt
        checked += cnt

    r26_ok = joint_part_bad == 0 and best_witness is not None
    return {
        "exhaustive_n2_m2_actions3_families": exhaustive_count,
        "sampled_families": sample_counts,
        "families_checked": checked,
        "joint_equals_joint_partition_min_violations": joint_part_bad,
        "strict_saving_witnesses": witness_count,
        "smallest_witness": best_witness[1] if best_witness else None,
        "smallest_all_individual_minimizers_suboptimal_witness":
            best_witness2[1] if best_witness2 else None,
        "witnesses_with_all_individual_minimizers_suboptimal": indiv_not_joint,
        "r26_ok": r26_ok,
        "verdict_R26": ("PASS" if r26_ok
                        else ("CANNOT_CHECK_NO_SMALL_JOINT_SELECTOR_WITNESS"
                              if best_witness is None
                              else "FAIL_COUNTEREXAMPLE_FOUND")),
    }


def min_valid_partition_joint(probs, astars):
    """Min-entropy partition whose blocks admit a common joint selector:
    rectangular validity — every block has nonempty per-coordinate
    intersections simultaneously."""
    k = len(probs)
    best = None
    for part in rgs_partitions(k):
        blocks = block_of(part)
        ok = True
        for b in blocks.values():
            for astar in astars:
                if not intersect_all([astar[h] for h in b]):
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        e = fibre_entropy_of_map(probs, list(part))
        d = expr_to_dec(e)
        if best is None or d < best[0]:
            best = (d, e, part)
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260829)
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--samples", type=int, default=2000)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    t0 = time.time()
    rep = audit(args)
    rep["seconds"] = round(time.time() - t0, 1)
    dump_json(args.output, rep)
    print("verdicts:", rep["verdicts"])
    print("witness:", rep["sections"]["family_search"]["smallest_witness"])
    print("seconds:", rep["seconds"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
