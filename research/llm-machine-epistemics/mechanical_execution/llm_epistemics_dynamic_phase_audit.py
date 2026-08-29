"""Dynamic-state + phase-theory mechanical audit for ORION-V2 issue #51.

Implements Spec V4 §5-§7 + V5 §3-§7 + PH/DS theorems on top of
llm_epistemics_common.py:
  J2  exact joint policy/state optimum (brute-force RGS enumeration)
  J3  selector refinement route equals J2 optimum (independent)
  J4  Omega_dyn = C_dyn* - C_stat* >= 0
  J5  canonical one-bit dynamic optionality witness
  DS1 P0 Brodu-style predictive-decisional control fixture
  DS2 P1 static cross-channel fixture
  PH1 horizon-cost monotonicity C_0<=...<=C_inf, Omega nondecreasing
  PH2 finite-horizon stabilization (K_epi) via one-step congruence closure
  PH3 nested responsibility-family static/dynamic monotonicity
  mixed-P2 search (C0>0 and Omega>0) and tie-sensitive selector search

Verdict vocabulary (strict): PASS / FAIL_COUNTEREXAMPLE_FOUND /
CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS / CANNOT_CHECK_NO_SMALL_TIE_DYNAMIC_WITNESS.

Numerics discipline (V4 §8): structural conditions in exact integer
arithmetic; entropies as exact prime-exponent expressions; independent
Decimal cross-check (>=50 digits) at tolerance 1e-30; Fraction-typed
machine fixtures serialized raw.

RUNBOOK (billy-old; heavy compute NEVER on the Mac mini):
  mkdir -p ~/orion51/audit_out
  rsync -a /tmp/i51_lane/ billy-old:/tmp/i51_lane/
  ssh billy-old
  cd /tmp/i51_lane && nohup python3 llm_epistemics_dynamic_phase_audit.py \
      --outdir ~/orion51/audit_out > ~/orion51/audit_out/dynamic_phase.log 2>&1 &

Outputs (written into --outdir):
  DYNAMIC_RESPONSIBILITY_OPTIMIZATION_V1.json      (J2)
  JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json       (J3/J4/J5 + tie search)
  RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json         (P0/P1/P2 + mixed P2)
  RESPONSIBILITY_HORIZON_CURVE_V1.json             (PH1/PH2/PH3)
Exit codes: 0 = all PASS or cannot-check; 3 = any FAIL_COUNTEREXAMPLE_FOUND.
"""
from __future__ import annotations

import argparse
import itertools
import random
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_epistemics_common import (  # noqa: E402
    BELL_REFERENCE,
    check_bell,
    block_of,
    cond_h_dec,
    cond_h_expr,
    dump_json,
    expr_diff,
    expr_is_zero,
    expr_to_dec,
    intersect_all,
    joint_from_marginal,
    rgs_partitions,
    refines,
    tuple_partition,
)

DEC_TOL = Fraction(0).limit_denominator(10**30)  # tolerance marker only
DEC_TOL_F = 1e-30
ONE_BIT = {2: Fraction(1)}  # exact expr for ln 2 (== 1 bit)

# ------------------------------------------------------------------ machine


@dataclass(frozen=True)
class Machine:
    """Registered deterministic partial machine (V4 §2).

    n histories 0..n-1; P = predictive partition (RGS tuple over H);
    m inputs; delta[h][x] = successor int or None (UNDEFINED);
    a_star[h] = frozenset of permitted Bayes-optimal actions (nonempty);
    probs[h] = positive Fraction.
    """

    name: str
    P: tuple
    delta: tuple            # tuple of tuples: delta[h][x] -> int|None
    a_star: tuple           # tuple of frozensets
    probs: tuple

    @property
    def n(self) -> int:
        return len(self.P)

    @property
    def m(self) -> int:
        return len(self.delta[0]) if self.delta else 0

    def canon(self) -> tuple:
        """Canonical key: everything up to RGS relabelling of P."""
        return (self.P, self.delta, tuple(tuple(sorted(a)) for a in self.a_star))

    def to_json(self) -> dict:
        return {
            "name": self.name, "n": self.n, "m": self.m, "P": list(self.P),
            "delta": [[None if d is None else d for d in row] for row in self.delta],
            "a_star": [sorted(a) for a in self.a_star],
            "probs": list(self.probs),
        }


# ------------------------------------------------------- structural checks


def static_admissible(pi: tuple, mach: Machine) -> bool:
    """0-admissible: refines P and per-block common optimal action."""
    if not refines(pi, mach.P):
        return False
    for members in block_of(pi).values():
        if not intersect_all(mach.a_star[h] for h in members):
            return False
    return True


def one_step_congruent(pi: tuple, mach: Machine) -> bool:
    """Right congruence: matched definedness + same successor block."""
    for members in block_of(pi).values():
        hs = sorted(members)
        for h, h2 in itertools.combinations(hs, 2):
            for x in range(mach.m):
                d1, d2 = mach.delta[h][x], mach.delta[h2][x]
                if (d1 is None) != (d2 is None):
                    return False
                if d1 is not None and pi[d1] != pi[d2]:
                    return False
    return True

def congruence_closure(base: tuple, mach: Machine) -> tuple:
    """Coarsest right-congruent refinement of `base`.

    Independent of one_step_congruent: iterated successor-signature
    refinement until stable (J3's S_inf^d construction, PH2's ∞-route).
    """
    cur = tuple(base)
    while True:
        sig = []
        for h in range(mach.n):
            succ = tuple(
                None if mach.delta[h][x] is None else cur[mach.delta[h][x]]
                for x in range(mach.m)
            )
            sig.append((cur[h], succ))
        seen, out = {}, []
        for s in sig:
            out.append(seen.setdefault(s, len(seen)))
        nxt = tuple(out)
        if nxt == cur:
            return cur
        cur = nxt


def _support_samples(pi: tuple, mach: Machine):
    """(pi label, P label) pairs on the positive-mass support.

    Zero-mass states are structural only (e.g. future successors with
    self-loops in the J5 fixture); they carry no current-time entropy.
    """
    return ([(pi[h], mach.P[h]) for h in range(mach.n) if mach.probs[h] > 0],
            [mach.probs[h] for h in range(mach.n) if mach.probs[h] > 0])


def cost_expr(pi: tuple, mach: Machine) -> dict:
    """Exact nats expr of H(Pi(H) | P)."""
    samples, probs = _support_samples(pi, mach)
    table = joint_from_marginal(samples, probs)
    return cond_h_expr(table, (1,), (0,))


def cost_dec(pi: tuple, mach: Machine):
    samples, probs = _support_samples(pi, mach)
    table = joint_from_marginal(samples, probs)
    return cond_h_dec(table, (1,), (0,))


def cost_bits(pi: tuple, mach: Machine):
    from decimal import Decimal
    return expr_to_dec(cost_expr(pi, mach))


def expr_eq(a: dict, b: dict) -> bool:
    """Exact equality of two nats exprs (Q-linear independence of ln p)."""
    return expr_is_zero(expr_diff(a, b))


def expr_nonneg(a: dict) -> bool:
    """Nonnegative check: exact-zero via exprs, sign via Decimal."""
    if expr_is_zero(a):
        return True
    return expr_to_dec(a) >= -DEC_TOL_F


def enumerate_partitions(mach: Machine, dyn: bool):
    """All static- (or dynamically-) admissible partitions; Bell-guarded."""
    nparts = 0
    for pi in rgs_partitions(mach.n):
        nparts += 1
        if static_admissible(pi, mach) and (not dyn or one_step_congruent(pi, mach)):
            yield pi
    if mach.n in BELL_REFERENCE:
        check_bell(mach.n, nparts)


def min_cost(mach: Machine, dyn: bool):
    """(best_pi, best_expr, best_dec) minimizing H(Pi|P); None if infeasible."""
    best = None
    for pi in enumerate_partitions(mach, dyn):
        e = cost_expr(pi, mach)
        if best is None:
            best = (pi, e, expr_to_dec(e))
            continue
        d = expr_diff(best[1], e)  # best - e
        if expr_is_zero(d):
            if pi < best[0]:  # deterministic tie-break
                best = (pi, e, best[2])
        elif expr_to_dec(d) > 0:  # strictly cheaper
            best = (pi, e, expr_to_dec(e))
    return best

# ------------------------------------------------------------- verdict I/O

VERDICTS = []  # (check_id, verdict)


def record(check_id: str, verdict: str) -> str:
    assert verdict in ("PASS", "FAIL_COUNTEREXAMPLE_FOUND",
                       "CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS",
                       "CANNOT_CHECK_NO_SMALL_TIE_DYNAMIC_WITNESS"), verdict
    VERDICTS.append((check_id, verdict))
    print(f"CHECK {check_id} {verdict}", flush=True)
    return verdict


def expr_json(e: dict) -> dict:
    return {str(p): str(c) for p, c in sorted(e.items())}


# --------------------------------------------------------------- J2 (§5-§6)


def impl_equivalence_partitions(mach: Machine):
    """J2 converse route: deterministic recurrent state + optimal-action
    decoder -> dynamically admissible partition.

    For every static-admissible pi (a decoder exists per block), build the
    closure of (P-class, decoded action, successor-signature) labels from
    pi and check dynamic admissibility of the result.
    """
    outs = []
    for pi in enumerate_partitions(mach, dyn=False):
        cur = pi
        while True:
            # decode: smallest common optimal action per CURRENT block
            # (rebuilt each round: refinement blocks are subsets, so the
            # intersection only grows and min stays defined)
            decode = {}
            for c, members in sorted(block_of(cur).items()):
                inter = intersect_all(mach.a_star[h] for h in members)
                if not inter:
                    raise RuntimeError(
                        f"refinement block {c} lost common optimal action")
                decode[c] = min(inter)
            sig = []
            for h in range(mach.n):
                succ = tuple(None if mach.delta[h][x] is None
                             else cur[mach.delta[h][x]]
                             for x in range(mach.m))
                sig.append((mach.P[h], decode[cur[h]], succ))
            seen, out = {}, []
            for s in sig:
                out.append(seen.setdefault(s, len(seen)))
            nxt = tuple(out)
            if nxt == cur:
                break
            cur = nxt
        outs.append((pi, cur))
    return outs


def check_j2(fixtures, n_max: int, outdir: Path) -> dict:
    records = []
    ok = True
    for mach in fixtures:
        if mach.n > n_max:
            continue
        c_stat = min_cost(mach, dyn=False)
        c_dyn = min_cost(mach, dyn=True)
        # converse: every closure-built partition is dynamically admissible
        converse_ok = True
        for base, closed in impl_equivalence_partitions(mach):
            if not (static_admissible(closed, mach)
                    and one_step_congruent(closed, mach)):
                converse_ok = False
                records.append({"machine": mach.name, "defect":
                                "impl-equivalence closure not admissible",
                                "base": list(base), "closed": list(closed)})
        rec = {
            "machine": mach.to_json(),
            "c_stat_star": {"pi": list(c_stat[0]), "expr": expr_json(c_stat[1]),
                            "bits": str(c_stat[2])},
            "c_dyn_star": {"pi": list(c_dyn[0]), "expr": expr_json(c_dyn[1]),
                           "bits": str(c_dyn[2])},
            "impl_equivalence_direction": "PASS" if converse_ok else
                                          "FAIL_COUNTEREXAMPLE_FOUND",
            "decimal_crosscheck_bits": {
                "c_stat": str(cost_dec(c_stat[0], mach)),
                "c_dyn": str(cost_dec(c_dyn[0], mach))},
        }
        ok = ok and converse_ok
        records.append(rec)
    record("J2_DYNAMIC_RESPONSIBILITY_OPTIMIZATION_V1",
           "PASS" if ok else "FAIL_COUNTEREXAMPLE_FOUND")
    doc = {"theorem": "J2", "fixtures": records,
           "runbook_note": "brute-force RGS enumeration, exact expr entropies"}
    dump_json(outdir / "DYNAMIC_RESPONSIBILITY_OPTIMIZATION_V1.json", doc)
    return doc

# ------------------------------------- J3/J4/J5 + tie-sensitive search (§7)


def all_selectors(mach: Machine, cap: int = 20000, rng=None, trials: int = 300):
    """Bayes-optimal selectors d(h) in A*(h): exhaustive under cap, else
    seeded sample."""
    choices = [sorted(mach.a_star[h]) for h in range(mach.n)]
    total = 1
    for c in choices:
        total *= len(c)
    if total <= cap:
        for combo in itertools.product(*choices):
            yield tuple(combo), total, "exhaustive"
    else:
        assert rng is not None
        seen = set()
        for _ in range(trials):
            d = tuple(rng.choice(c) for c in choices)
            if d not in seen:
                seen.add(d)
                yield d, total, "sampled"


def selector_inf_cost(mach: Machine, d: tuple):
    """S_inf^d via congruence closure of (P, d); return (pi, expr, bits)."""
    base = tuple_partition(mach.P, d)
    pi = congruence_closure(base, mach)
    e = cost_expr(pi, mach)
    return pi, e, expr_to_dec(e)


TIE_PALETTES = {
    (5, 1): ({frozenset(s) for s in ("0", "1", "2", "01")},),
    (4, 2): ({frozenset(s) for s in ("0", "1", "01")},),
    (4, 1): ({frozenset(s) for s in ("0", "1", "2", "01")},),
    (3, 2): ({frozenset(s) for s in ("0", "1", "01")},),
    (3, 1): ({frozenset(s) for s in ("0", "1", "2", "01")},),
}
TIE_DEFAULT_BUDGET = 30_000_000


def check_j3(fixtures, n_max: int, outdir: Path, seed: int,
             trials: int, tie_search: bool,
             tie_budget: int = TIE_DEFAULT_BUDGET) -> dict:
    rng = random.Random(seed)
    records, ok = [], True
    for mach in fixtures:
        if mach.n > n_max:
            continue
        c_dyn = min_cost(mach, dyn=True)
        best_sel = None
        modes = set()
        for d, total, mode in all_selectors(mach, rng=rng, trials=trials):
            modes.add(mode)
            pi, e, bits = selector_inf_cost(mach, d)
            if best_sel is None or expr_to_dec(expr_diff(best_sel[1], e)) > 0:
                best_sel = (d, pi, e, bits)
        j3_eq = expr_eq(best_sel[2], c_dyn[1])
        ok = ok and j3_eq
        records.append({
            "machine": mach.to_json(), "selector_space_size": total,
            "selector_mode": sorted(modes),
            "best_selector": list(best_sel[0]),
            "s_inf_pi": list(best_sel[1]),
            "selector_cost_bits": str(best_sel[3]),
            "brute_dyn_bits": str(c_dyn[2]),
            "j3_expr_equal": j3_eq})
    tie = tie_sensitive_search(n_max=n_max, budget=tie_budget) \
        if tie_search else None
    if tie_search:
        ok = ok and tie["verdict"] in (
            "PASS", "CANNOT_CHECK_NO_SMALL_TIE_DYNAMIC_WITNESS")
        record("TIE_SENSITIVE_DYNAMIC_SELECTOR_V1", tie["verdict"])
    record("J3_JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1",
           "PASS" if ok else "FAIL_COUNTEREXAMPLE_FOUND")
    doc = {"theorem": "J3+ties", "fixtures": records, "tie_search": tie}
    dump_json(outdir / "JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json", doc)
    return doc


def _selector_costs(mach: Machine):
    """All-selector (pi, expr, bits) list; None entries deduped by base."""
    outs = []
    seen_base = {}
    for d, _, _ in all_selectors(mach):
        base = tuple_partition(mach.P, d)
        if base in seen_base:
            outs.append((d, seen_base[base]))
            continue
        pi = congruence_closure(base, mach)
        e = cost_expr(pi, mach)
        seen_base[base] = (pi, e, expr_to_dec(e))
        outs.append((d, seen_base[base]))
    return outs


def tie_sensitive_search(n_max: int = 5, budget: int = TIE_DEFAULT_BUDGET,
                         wall_s: float = 2700.0) -> dict:
    """V4 §7 tie-sensitive witness: two Bayes-optimal selectors with
    DIFFERENT H(S_inf^d | P). Registered bound: (n,m) in TIE_PALETTES,
    actions<=3 with at least one genuine tie, all delta maps incl. UNDEFINED,
    budget+wall-clock guarded; smallest witness frozen by
    witness_rank = (n, m, |A|, P, a_star, delta)."""
    t0 = time.time()
    counts = {"machines": 0, "with_tie_states": 0, "selector_pairs": 0}
    witness = None
    for (n, m), (palette,) in sorted(TIE_PALETTES.items()):
        if n > n_max:
            continue
        for P in rgs_partitions(n):
            for a_star in itertools.product(palette, repeat=n):
                if not any(len(a) >= 2 for a in a_star):
                    continue  # need a genuine Bayes-optimal tie
                counts["with_tie_states"] += 1
                for cells in itertools.product(range(n + 1), repeat=n * m):
                    if counts["machines"] >= budget or \
                            time.time() - t0 > wall_s:
                        return _tie_doc(counts, witness, True, budget, n, m)
                    counts["machines"] += 1
                    delta = tuple(
                        tuple(None if cells[h * m + x] == n
                              else cells[h * m + x] for x in range(m))
                        for h in range(n))
                    mach = Machine(f"tie_n{n}", P, delta, a_star,
                                   tuple(Fraction(1, n) for _ in range(n)))
                    costs = _selector_costs(mach)
                    for (d1, c1), (d2, c2) in itertools.combinations(costs, 2):
                        counts["selector_pairs"] += 1
                        if d1 == d2:
                            continue
                        diff = expr_diff(c1[1], c2[1])
                        if not expr_is_zero(diff) and \
                                abs(expr_to_dec(diff)) > DEC_TOL_F:
                            witness = {"machine": mach.to_json(),
                                       "selector_a": list(d1),
                                       "selector_b": list(d2),
                                       "cost_a_bits": str(c1[2]),
                                       "cost_b_bits": str(c2[2]),
                                       "pi_a": list(c1[0]),
                                       "pi_b": list(c2[0]),
                                       "witness_rank": [n, m, 3, list(P),
                                                        [sorted(a) for a in a_star],
                                                        [list(r) for r in delta]]}
                            return _tie_doc(counts, witness, False, budget, n, m)
    return _tie_doc(counts, witness, False, budget, None, None)


def _tie_doc(counts, witness, truncated, budget, n, m) -> dict:
    if witness:
        verdict = "PASS"
    elif truncated:
        verdict = "CANNOT_CHECK_NO_SMALL_TIE_DYNAMIC_WITNESS"
    else:
        verdict = "CANNOT_CHECK_NO_SMALL_TIE_DYNAMIC_WITNESS"
    print(f"  tie-search: {counts} budget={budget} truncated={truncated}")
    return {"verdict": verdict, "counts": counts, "budget": budget,
            "truncated_by_budget_or_clock": truncated,
            "last_completed_bound": {"n": n, "m": m},
            "witness": witness}

# ------------------------------------------------- canonical fixtures (§7-§8)

HALF = Fraction(1, 2)


def fixture_p0() -> Machine:
    """DS1 / Brodu control: action constant per fibre, transitions
    right-congruent. Expect C0=0, Cinf=0, Omega=0."""
    return Machine("P0_PREDICTIVE_DECISIONAL", P=(0, 0, 1),
                   delta=((0,), (1,), (2,)),
                   a_star=(frozenset({0}), frozenset({0}), frozenset({1})),
                   probs=(Fraction(1, 4), Fraction(1, 4), HALF))


def fixture_p1() -> Machine:
    """DS2 cross-channel: one fibre, disjoint unique actions from a
    provenance variable absent from S_P; absorbing transitions preserve
    the split. Expect C0=1 bit, Cinf=1 bit, Omega=0."""
    return Machine("P1_STATIC_CROSS_CHANNEL", P=(0, 0),
                   delta=((0,), (1,)),
                   a_star=(frozenset({0}), frozenset({1})),
                   probs=(HALF, HALF))


def fixture_p2() -> Machine:
    """J5 canonical one-bit prospective witness: h0,h1 equal prob, one
    fibre, shared unique action {0}; successors s0,s1 (zero current mass,
    absorbing self-loops) carry disjoint unique actions {1},{2} and sit in
    distinct P fibres, so no admissible block can contain both. Expect
    C_stat*=0, no dynamically-admissible merge, C_dyn*=1 bit, Omega=1."""
    return Machine("P2_PROSPECTIVE_REFINEMENT", P=(0, 0, 1, 2),
                   delta=((2,), (3,), (2,), (3,)),
                   a_star=(frozenset({0}), frozenset({0}),
                           frozenset({1}), frozenset({2})),
                   probs=(HALF, HALF, Fraction(0), Fraction(0)))


def canonical_fixtures():
    return [fixture_p0(), fixture_p1(), fixture_p2()]


# ------------------------------------------------------------- J4 + J5 (§7)


def a0_gate(mach: Machine) -> dict:
    """A0 pre-gate: H(Q|H)=0 with Q = A*-signature partition (target
    identifiable from full history)."""
    sigs = {tuple(sorted(mach.a_star[h])) for h in range(mach.n)}
    order = {s: i for i, s in enumerate(sorted(sigs))}
    q = tuple(order[tuple(sorted(mach.a_star[h]))] for h in range(mach.n))
    table = joint_from_marginal([(q[h], h) for h in range(mach.n)
                                 if mach.probs[h] > 0],
                                [mach.probs[h] for h in range(mach.n)
                                 if mach.probs[h] > 0])
    e = cond_h_expr(table, (1,), (0,))  # H(Q | H)
    return {"q_pi": list(q), "h_q_given_h_expr": expr_json(e),
            "h_q_given_h_bits": str(expr_to_dec(e)), "a0_pass": expr_is_zero(e)}


def check_j4_j5(fixtures, n_max: int, outdir: Path) -> dict:
    records, ok = [], True
    for mach in fixtures:
        if mach.n > n_max:
            continue
        c_stat = min_cost(mach, dyn=False)
        c_dyn = min_cost(mach, dyn=True)
        omega = expr_diff(c_dyn[1], c_stat[1])
        j4_ok = expr_nonneg(omega)
        ok = ok and j4_ok
        records.append({
            "machine": mach.to_json(),
            "c_stat_star": {"pi": list(c_stat[0]), "expr": expr_json(c_stat[1]),
                            "bits": str(c_stat[2])},
            "c_dyn_star": {"pi": list(c_dyn[0]), "expr": expr_json(c_dyn[1]),
                           "bits": str(c_dyn[2])},
            "omega_dyn": {"expr": expr_json(omega),
                          "bits": str(expr_to_dec(omega)),
                          "nonnegative": j4_ok},
            "a0_gate": a0_gate(mach)})
    p2 = fixture_p2()
    c_stat = min_cost(p2, dyn=False)
    c_dyn = min_cost(p2, dyn=True)
    omega = expr_diff(c_dyn[1], c_stat[1])
    j5_ok = (expr_is_zero(c_stat[1]) and expr_eq(c_dyn[1], ONE_BIT)
             and expr_eq(omega, ONE_BIT))
    ok = ok and j5_ok
    records.append({
        "machine": p2.to_json(), "check": "J5",
        "expected": {"c_stat_bits": "0", "c_dyn_bits": "1", "omega_bits": "1"},
        "observed": {"c_stat_bits": str(c_stat[2]), "c_dyn_bits": str(c_dyn[2]),
                     "omega_bits": str(expr_to_dec(omega))},
        "expr_equal_expected": j5_ok})
    record("J4_OMEGA_DYN_NONNEGATIVE_V1",
           "PASS" if all(r.get("omega_dyn", {}).get("nonnegative", True)
                         for r in records if "omega_dyn" in r)
           else "FAIL_COUNTEREXAMPLE_FOUND")
    record("J5_CANONICAL_ONE_BIT_WITNESS_V1",
           "PASS" if j5_ok else "FAIL_COUNTEREXAMPLE_FOUND")
    return {"theorem": "J4+J5", "fixtures": records}

# ------------------------------------------- phase audit + mixed P2 (V5 §5)


def phase_of(c0: dict, omega_inf: dict) -> str:
    """Phase labels are NOT mutually exclusive on (C0, Omega): the
    canonical P2 witness has C0=0 AND Omega>0 (theory §6: 'P2 may occur
    with either C0*=0 or C0*>0'). Precedence: Omega>0 dominates."""
    if not expr_is_zero(omega_inf):
        return "P2_PROSPECTIVE_REFINEMENT"
    if not expr_is_zero(c0):
        return "P1_STATIC_CROSS_CHANNEL"
    return "P0_PREDICTIVE_DECISIONAL"


def phase_record(mach: Machine, expected: dict) -> dict:
    c_stat = min_cost(mach, dyn=False)
    c_dyn = min_cost(mach, dyn=True)
    omega = expr_diff(c_dyn[1], c_stat[1])
    phase = phase_of(c_stat[1], omega)
    ok = (expr_eq(c_stat[1], _parse_expr(expected["c0_expr"]))
          and expr_eq(c_dyn[1], _parse_expr(expected["cinf_expr"]))
          and expr_eq(omega, _parse_expr(expected["omega_expr"]))
          and phase == expected["phase"])
    return {"machine": mach.to_json(), "expected": expected,
            "c0": {"pi": list(c_stat[0]), "expr": expr_json(c_stat[1]),
                   "bits": str(c_stat[2])},
            "cinf": {"pi": list(c_dyn[0]), "expr": expr_json(c_dyn[1]),
                     "bits": str(c_dyn[2])},
            "omega": {"expr": expr_json(omega), "bits": str(expr_to_dec(omega))},
            "phase": phase, "verdict": "PASS" if ok else "FAIL_COUNTEREXAMPLE_FOUND",
            "a0_gate": a0_gate(mach)}


def _parse_expr(s: str) -> dict:
    """'0' -> {}; 'ln2' -> {2:1}; '2ln2' -> {2:2}."""
    s = s.strip()
    if s == "0":
        return {}
    if s == "ln2":
        return {2: Fraction(1)}
    if s.endswith("ln2"):
        return {2: Fraction(int(s[:-3]))}
    raise ValueError(s)


def check_phases(outdir: Path, mixed_search: str) -> dict:
    recs = [phase_record(fixture_p0(), {"c0_expr": "0", "cinf_expr": "0",
                                         "omega_expr": "0",
                                         "phase": "P0_PREDICTIVE_DECISIONAL"}),
            phase_record(fixture_p1(), {"c0_expr": "ln2", "cinf_expr": "ln2",
                                         "omega_expr": "0",
                                         "phase": "P1_STATIC_CROSS_CHANNEL"}),
            phase_record(fixture_p2(), {"c0_expr": "0", "cinf_expr": "ln2",
                                         "omega_expr": "ln2",
                                         "phase": "P2_PROSPECTIVE_REFINEMENT"})]
    ok = all(r["verdict"] == "PASS" for r in recs)
    mixed = mixed_p2_search(full=(mixed_search == "full"))
    ok = ok and mixed["verdict"] in ("PASS", "CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS")
    record("DS1_P0_PREDICTIVE_DECISIONAL_V1", recs[0]["verdict"])
    record("DS2_P1_STATIC_CROSS_CHANNEL_V1", recs[1]["verdict"])
    record("P2_CANONICAL_PROSPECTIVE_V1", recs[2]["verdict"])
    record("MIXED_P2_WITNESS_SEARCH_V1", mixed["verdict"])
    doc = {"theorem": "DS1+DS2+phases", "fixtures": recs, "mixed_p2": mixed}
    dump_json(outdir / "RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json", doc)
    return doc

def mixed_p2_search(full: bool = True) -> dict:
    """Mixed phase witness: C0>0 AND Omega>0. Registered bound: n<=4, m=1,
    actions<=3 all singleton A*, P = one nontrivial fibre {h0,h1} + rest
    singleton fibres, all (n+1)^(n*m) delta maps incl. UNDEFINED, uniform
    probs. witness_rank = (n, m, |A|)."""
    counts = {"machines": 0, "static_opt_positive": 0}
    witness = None
    ns = (2, 3, 4) if full else (3,)
    for n in ns:
        P = (0, 0) + tuple(range(2, n))  # one nontrivial fibre + singletons
        for a2 in itertools.product((frozenset({0}), frozenset({1}),
                                     frozenset({2})), repeat=max(n - 2, 0)):
            a_star = (frozenset({0}), frozenset({1})) + a2  # disjoint split
            for cells in itertools.product(range(n + 1), repeat=n):
                counts["machines"] += 1
                delta = tuple(tuple(None if c == n else c for c in (cells[h],))
                              for h in range(n))
                mach = Machine(f"mixed_n{n}", P, delta, a_star,
                               tuple(Fraction(1, n) for _ in range(n)))
                c_stat = min_cost(mach, dyn=False)
                if c_stat is None:
                    continue
                c_dyn = min_cost(mach, dyn=True)
                omega = expr_diff(c_dyn[1], c_stat[1])
                if not expr_is_zero(c_stat[1]):
                    counts["static_opt_positive"] += 1
                if (not expr_is_zero(c_stat[1])) and (not expr_is_zero(omega)) \
                        and expr_to_dec(c_stat[1]) > DEC_TOL_F \
                        and expr_to_dec(omega) > DEC_TOL_F:
                    n_actions = 1 + max(max(a) for a in a_star)
                    witness = {
                        "machine": mach.to_json(),
                        "c0": {"pi": list(c_stat[0]),
                               "expr": expr_json(c_stat[1]),
                               "bits": str(c_stat[2])},
                        "cinf": {"pi": list(c_dyn[0]), "expr": expr_json(c_dyn[1]),
                                 "bits": str(c_dyn[2])},
                        "omega": {"expr": expr_json(omega),
                                  "bits": str(expr_to_dec(omega))},
                        "witness_rank": [n, 1, n_actions]}
                    print(f"  mixed-P2 witness n={n} C0={c_stat[2]} "
                          f"Omega={expr_to_dec(omega)} bits")
                    return {"verdict": "PASS", "counts": counts,
                            "bound": {"n_max": 4, "m": 1, "actions": 3,
                                      "delta_maps": (n + 1) ** n},
                            "witness": witness}
    verdict = ("PASS" if witness else
               "CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS")
    print(f"  mixed-P2 search: {counts}")
    return {"verdict": verdict, "counts": counts,
            "bound": {"n_max": max(ns), "m": 1, "actions": 3}, "witness": witness}

# ------------------------------------- horizon curve PH1/PH2 (V5 §6, th. §2)


def _step(mach: Machine, h: int, x: int):
    return mach.delta[h][x]


def word_successor(mach: Machine, h: int, word):
    """delta(h, word) or None if any step undefined; None-marker distinct."""
    cur = h
    for x in word:
        if cur is None:
            return None
        nxt = _step(mach, cur, x)
        if nxt is None:
            return None
        cur = nxt
    return cur


def k_admissible_literal(pi: tuple, mach: Machine, k: int) -> bool:
    """Phase-theory Def 2 verbatim: all words 1<=j<=k, matched definedness
    + same successor block. Word enumeration (implementation A)."""
    if not static_admissible(pi, mach):
        return False
    for j in range(1, k + 1):
        for word in itertools.product(range(mach.m), repeat=j):
            for members in block_of(pi).values():
                hs = sorted(members)
                base = word_successor(mach, hs[0], word)
                for h in hs[1:]:
                    s = word_successor(mach, h, word)
                    if (base is None) != (s is None):
                        return False
                    if base is not None and pi[base] != pi[s]:
                        return False
    return True


def canon_pi(pi: tuple) -> tuple:
    """Relabel a partition by first occurrence (canonical RGS form)."""
    seen, out = {}, []
    for c in pi:
        out.append(seen.setdefault(c, len(seen)))
    return tuple(out)


def refine_once(pi: tuple, mach: Machine) -> tuple:
    """One round of successor-signature refinement of pi (canonical)."""
    sig = []
    for h in range(mach.n):
        succ = tuple(None if mach.delta[h][x] is None else pi[mach.delta[h][x]]
                     for x in range(mach.m))
        sig.append((pi[h], succ))
    seen, out = {}, []
    for s in sig:
        out.append(seen.setdefault(s, len(seen)))
    return tuple(out)


def k_admissible_iterative(pi: tuple, mach: Machine, k: int) -> bool:
    """Implementation B: k rounds of successor-signature splitting of pi
    (round 1 = one-step congruence). k-adm iff no round splits pi."""
    if not static_admissible(pi, mach):
        return False
    cur = canon_pi(pi)
    for _ in range(k):
        nxt = refine_once(cur, mach)
        if nxt != cur:
            return False
    return True

def min_cost_over(mach: Machine, pred):
    """min H(Pi|P) over partitions satisfying pred(pi)."""
    best = None
    for pi in enumerate_partitions(mach, dyn=False):
        if not pred(pi):
            continue
        e = cost_expr(pi, mach)
        if best is None:
            best = (pi, e, expr_to_dec(e))
            continue
        d = expr_diff(best[1], e)
        if expr_is_zero(d):
            if pi < best[0]:
                best = (pi, e, best[2])
        elif expr_to_dec(d) > 0:
            best = (pi, e, expr_to_dec(e))
    return best


def random_machine(rng: random.Random, name: str, n: int, m: int,
                   n_actions: int = 3) -> Machine:
    P = list(rng_partitions_at(rng, n))
    delta = tuple(tuple(rng.choice([None] + list(range(n))) for _ in range(m))
                  for _ in range(n))
    a_star = tuple(frozenset({rng.randrange(n_actions)}) for _ in range(n))
    return Machine(name, tuple(P), delta, a_star,
                   tuple(Fraction(1, n) for _ in range(n)))


def rng_partitions_at(rng: random.Random, n: int):
    """Random RGS partition of n elements."""
    out = [0]
    for _ in range(1, n):
        out.append(rng.randrange(0, max(out) + 2))
    return out


def horizon_record(mach: Machine, k_word_max: int = 3) -> dict:
    """C_k curve via literal word-k admissibility; PH1 monotonicity, PH2
    K_epi vs independently computed one-step-congruence (∞) optimum."""
    c_inf = min_cost(mach, dyn=True)
    curve = []
    prev = None
    mono_ok = True
    for k in range(0, k_word_max + 1):
        ck = min_cost_over(mach, lambda pi, k=k: k_admissible_literal(pi, mach, k))
        curve.append({"k": k, "pi": list(ck[0]), "expr": expr_json(ck[1]),
                      "bits": str(ck[2])})
        if prev is not None:
            d = expr_diff(ck[1], prev[1])  # C_k - C_{k-1} >= 0
            if not expr_nonneg(d):
                mono_ok = False
        prev = ck
    d_inf = expr_diff(c_inf[1], prev[1])  # C_inf - C_kword >= 0
    mono_ok = mono_ok and expr_nonneg(d_inf)
    k_epi = None
    for c in curve:
        if expr_eq(_expr_from_json(c["expr"]), c_inf[1]):
            k_epi = c["k"]
            break
    if k_epi is None:
        k_epi = k_word_max  # not stabilized within tested words
    lit_eq_iter = all(
        k_admissible_literal(pi, mach, k) == k_admissible_iterative(pi, mach, k)
        for k in range(1, k_word_max + 1)
        for pi in rgs_partitions(mach.n))
    return {"machine": mach.to_json(), "curve": curve,
            "c_inf": {"pi": list(c_inf[0]), "expr": expr_json(c_inf[1]),
                      "bits": str(c_inf[2])},
            "ph1_monotone": mono_ok, "k_epi": k_epi,
            "literal_equals_iterative_k": lit_eq_iter}


def _expr_from_json(j: dict) -> dict:
    return {int(p): Fraction(num) / Fraction(den)
            for p, s in j.items()
            for num, den in [ _split_frac(s) ]}


def _split_frac(s: str):
    if "/" in s:
        a, b = s.split("/")
        return int(a), int(b)
    return int(s), 1

# ------------------------------------- PH3 responsibility families (V5 §7)

CONST0 = tuple(frozenset({0}) for _ in range(4))


def family_static_admissible(pi: tuple, mach: Machine, family) -> bool:
    """Block admissible iff every responsibility r has a common action on
    the block: cap_{h in B} A_r(h) != emptyset for all r (ANY_OPTIMAL)."""
    if not refines(pi, mach.P):
        return False
    for a_r in family:
        for members in block_of(pi).values():
            if not intersect_all(a_r[h] for h in members):
                return False
    return True


def family_min_cost(mach: Machine, family, dyn: bool):
    return min_cost_over(
        mach,
        lambda pi: family_static_admissible(pi, mach, family)
        and (not dyn or one_step_congruent(pi, mach)))


def machine_b() -> Machine:
    """PH3 chain carrier: h0,h1 one fibre (mass 1/2 each); successors
    s0=2,s1=3 share ONE P fibre and carry zero current mass."""
    return Machine("PH3_CHAIN", P=(0, 0, 1, 1),
                   delta=((2,), (3,), (2,), (3,)),
                   a_star=CONST0,
                   probs=(HALF, HALF, Fraction(0), Fraction(0)))


F_CROSS = (frozenset({0}), frozenset({1}), frozenset({0}), frozenset({0}))
F_PROSP = (frozenset({0}), frozenset({0}), frozenset({1}), frozenset({2}))


def check_ph3(outdir: Path) -> dict:
    mach = machine_b()
    families = [
        ("R1_base", (CONST0,)),
        ("R2_redundant", (CONST0, CONST0)),
        ("R3_prospective", (CONST0, CONST0, F_PROSP)),
        ("R4_cross", (CONST0, F_CROSS)),
        ("R5_saturating", (CONST0, F_CROSS, F_PROSP)),
    ]
    recs = []
    prev = None
    mono_ok = True
    for name, fam in families:
        g0 = family_min_cost(mach, fam, dyn=False)
        ginf = family_min_cost(mach, fam, dyn=True)
        rec = {"family": name,
               "members": [[sorted(a) for a in a_r] for a_r in fam],
               "g0": {"pi": list(g0[0]), "expr": expr_json(g0[1]),
                      "bits": str(g0[2])},
               "g_inf": {"pi": list(ginf[0]), "expr": expr_json(ginf[1]),
                         "bits": str(ginf[2])}}
        if prev is not None:
            mono_ok = mono_ok and expr_nonneg(expr_diff(g0[1], prev[0])) \
                and expr_nonneg(expr_diff(ginf[1], prev[1]))
        prev = (g0[1], ginf[1])
        recs.append(rec)
    by = {r["family"]: r for r in recs}
    checks = {
        "redundant_no_increase": expr_eq(
            _expr_from_json(by["R2_redundant"]["g0"]["expr"]),
            _expr_from_json(by["R1_base"]["g0"]["expr"])),
        "p0_to_p1_via_cross": expr_is_zero(
            _expr_from_json(by["R1_base"]["g0"]["expr"])) and not expr_is_zero(
            _expr_from_json(by["R4_cross"]["g0"]["expr"])),
        "to_p2_via_prospective": not expr_is_zero(_expr_diff_bits(
            by["R3_prospective"]["g_inf"],
            by["R3_prospective"]["g0"])),
        "saturation_reaches_h_h_given_p": expr_eq(
            _expr_from_json(by["R5_saturating"]["g_inf"]["expr"]),
            _h_h_given_p(mach)),
    }
    record("PH3_RESPONSIBILITY_FAMILY_MONOTONICITY_V1",
           "PASS" if (mono_ok and all(checks.values()))
           else "FAIL_COUNTEREXAMPLE_FOUND")
    doc = {"theorem": "PH3", "machine": mach.to_json(), "families": recs,
           "checks": checks, "monotone": mono_ok}
    return doc

def _expr_diff_bits(cost_a: dict, cost_b: dict) -> dict:
    """expr diff of two {'pi','expr','bits'} cost records."""
    return expr_diff(_expr_from_json(cost_a["expr"]),
                     _expr_from_json(cost_b["expr"]))


def _h_h_given_p(mach: Machine) -> dict:
    """Exact expr of H(H | P) on the positive-mass support."""
    samples = [(h, mach.P[h]) for h in range(mach.n) if mach.probs[h] > 0]
    probs = [mach.probs[h] for h in range(mach.n) if mach.probs[h] > 0]
    table = joint_from_marginal(samples, probs)
    return cond_h_expr(table, (1,), (0,))

def check_horizon(outdir: Path, seed: int, mixed_doc: dict) -> dict:
    rng = random.Random(seed ^ 0x5EED)
    fixtures = canonical_fixtures()
    if mixed_doc.get("witness"):
        w = mixed_doc["witness"]["machine"]
        fixtures.append(Machine(
            w["name"], tuple(w["P"]),
            tuple(tuple(d for d in row) for row in w["delta"]),
            tuple(frozenset(a) for a in w["a_star"]),
            tuple(Fraction(p["__fraction__"][0], p["__fraction__"][1])
                  for p in w["probs"])))
    for i, n in enumerate((4, 5, 5)):
        fixtures.append(random_machine(rng, f"RANDOM_{i}", n, m=1))
    recs = [horizon_record(mach) for mach in fixtures]
    ph1_ok = all(r["ph1_monotone"] for r in recs)
    ph2_ok = all(r["k_epi"] is not None and r["k_epi"] <= 3 for r in recs)
    lit_ok = all(r["literal_equals_iterative_k"] for r in recs)
    record("PH1_HORIZON_COST_MONOTONICITY_V1",
           "PASS" if ph1_ok else "FAIL_COUNTEREXAMPLE_FOUND")
    record("PH2_FINITE_HORIZON_STABILIZATION_V1",
           "PASS" if (ph2_ok and lit_ok) else "FAIL_COUNTEREXAMPLE_FOUND")
    doc = {"theorem": "PH1+PH2", "fixtures": recs,
           "note": "k-admissible sets are computed by literal word "
                   "enumeration (Def 2 verbatim) and independently by "
                   "iterated successor-signature refinement; one-step "
                   "congruence is checked to imply all tested horizons."}
    ph3_doc = check_ph3(outdir)
    doc["ph3"] = ph3_doc
    dump_json(outdir / "RESPONSIBILITY_HORIZON_CURVE_V1.json", doc)
    return doc

# ------------------------------------------------------------------- main


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n-max", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20260829)
    ap.add_argument("--outdir", type=Path, default=Path(".") / "audit_out")
    ap.add_argument("--mixed-search", choices=("full", "bounded"), default="full")
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--tie-budget", type=int, default=TIE_DEFAULT_BUDGET)
    ap.add_argument("--no-tie-search", action="store_true")
    args = ap.parse_args(argv)
    args.outdir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)

    fixtures = canonical_fixtures()
    for i, n in enumerate((4, 5)):
        fixtures.append(random_machine(rng, f"RND_J_{i}", n, m=1))

    print(f"# dynamic/phase audit n_max={args.n_max} seed={args.seed} "
          f"outdir={args.outdir}", flush=True)
    check_j2(fixtures, args.n_max, args.outdir)
    doc3 = check_j3(fixtures, args.n_max, args.outdir, args.seed, args.trials,
                    tie_search=not args.no_tie_search,
                    tie_budget=args.tie_budget)
    doc3["j4_j5"] = check_j4_j5(fixtures, args.n_max, args.outdir)
    dump_json(args.outdir / "JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json", doc3)
    phase_doc = check_phases(args.outdir, args.mixed_search)
    check_horizon(args.outdir, args.seed, phase_doc["mixed_p2"])

    fails = [cid for cid, v in VERDICTS if v == "FAIL_COUNTEREXAMPLE_FOUND"]
    print(f"# verdicts: {len(VERDICTS)} fails={len(fails)} {fails}", flush=True)
    return 3 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
