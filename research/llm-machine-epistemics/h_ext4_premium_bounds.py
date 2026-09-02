#!/usr/bin/env python3
"""H-EXT-4 mechanized checks: quantitative prospective-revision premium.

Companion to ``H_EXT4_QUANTITATIVE_REVISION_PREMIUM_V1.md``.  Pure Python,
finite exhaustive enumeration over tiny deterministic machines in the
registered PRA model (same object as
``mechanical_execution/llm_epistemics_dynamic_phase_audit.py``: n states, a
predictive fibre partition P, a deterministic partial successor map delta,
nonempty Bayes-optimal action sets A*(h), positive-or-zero masses; cost of a
partition Pi is H(Pi | P) in bits over positive-mass states).

What is checked (each item is a numbered check in the receipt):

  A.L1  one-step reduction lemma on the terminal family
  A.P1  epsilon-criterion == (minimax cell regret <= epsilon)
  A.P2  Bayes-regret identity + garbling monotonicity (Blackwell direction)
  A.T1  per-representation sandwich: for every static-admissible Pi,
          -log2(1-R*(Pi)) <= Delta(Pi)                  (ALL machines)
          Delta(Pi) <= sum_x phi_x(R*_x(Pi))             (terminal + PC)
        where Delta(Pi) = min entropy a dynamic refinement must add to Pi
  A.T2  premium level: Omega_dyn <= min_{static-optimal} Delta(Pi_s)
        <= Fano form (terminal + PC); Fano form FAILS without PC
        (phantom-premium counterexample); label form holds without PC
  A.T3  tightness census; witness tight at uniform prior (both sides),
        all priors (Fano side)
  A.C1  conjectured lower bounds on Omega in terms of static-optimum regret
        are REFUTED (named counterexample + vanishing-premium family);
        the naive min-over-all-partitions lower bound is vacuous (attained by
        the dynamic optimum itself) and is not reported as a result
  B.1   cardinality premium Omega_card, C* <= log2 K*, witness formula,
        no ordering between Omega_dyn and Omega_card, zero-conditions differ
  C.1   RC & N1  =>  W_k ; W_k => N1 ; N1 =/=> W_2 (k=2 dormant conflict)
  C.2   injective zero-mass chain: word-compatibility of the initial partition
        <=> recursive extension exists; shared-successor counterexample
  C.3   multi-step Fano-type upper bound on depth-2 chains

The script grants no empirical LLM claim and changes no manuscript claim.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Callable, Iterable, Sequence

TOL = 1e-9
SCHEMA = "orion-v2.h-ext4-premium-bounds.v1"

# --------------------------------------------------------------- partitions


def rgs_partitions(n: int):
    """All set partitions of range(n) as restricted-growth tuples."""
    if n == 0:
        yield ()
        return
    a = [0] * n
    while True:
        yield tuple(a)
        i = n - 1
        while i >= 0:
            a[i] += 1
            if a[i] <= max(a[:i], default=-1) + 1:
                break
            a[i] = 0
            i -= 1
        if i < 0:
            return


def canon(pi: Sequence[int]) -> tuple:
    seen: dict = {}
    return tuple(seen.setdefault(c, len(seen)) for c in pi)


def refines(finer: Sequence[int], coarser: Sequence[int]) -> bool:
    m: dict = {}
    for f, c in zip(finer, coarser):
        if m.setdefault(f, c) != c:
            return False
    return True


def blocks_of(pi: Sequence[int]) -> dict:
    out: dict = {}
    for i, c in enumerate(pi):
        out.setdefault(c, []).append(i)
    return out


def join(*parts: Sequence[int]) -> tuple:
    """Common refinement (meet in the coarseness order)."""
    return canon(list(zip(*parts)))


def h_bits(ps: Iterable[float]) -> float:
    return -sum(p * math.log2(p) for p in ps if p > 0)


def hb(p: float) -> float:
    return h_bits([p, 1 - p])


def fano_phi(p: float, k: int) -> float:
    """Fano right-hand side h_b(p) + p*log2(k-1) for an alphabet of size k."""
    if k <= 1:
        return 0.0
    return hb(p) + p * math.log2(k - 1)


# ----------------------------------------------------------------- machine


@dataclass(frozen=True)
class Machine:
    P: tuple                 # predictive fibre id per state
    delta: tuple             # delta[h][x] -> int | None
    a_star: tuple            # frozenset per state, nonempty
    probs: tuple             # Fraction per state (>= 0)
    name: str = ""

    @property
    def n(self) -> int:
        return len(self.P)

    @property
    def m(self) -> int:
        return len(self.delta[0]) if self.delta else 0

    def to_json(self) -> dict:
        return {
            "name": self.name, "n": self.n, "m": self.m, "P": list(self.P),
            "delta": [list(r) for r in self.delta],
            "a_star": [sorted(a) for a in self.a_star],
            "probs": [str(p) for p in self.probs],
        }

    def actions(self) -> set:
        return set().union(*self.a_star)


def static_admissible(pi: Sequence[int], m: Machine) -> bool:
    if not refines(pi, m.P):
        return False
    for members in blocks_of(pi).values():
        common = frozenset(m.a_star[members[0]])
        for h in members[1:]:
            common &= m.a_star[h]
            if not common:
                return False
    return True


def right_congruent(pi: Sequence[int], m: Machine) -> bool:
    for members in blocks_of(pi).values():
        h0 = members[0]
        for h in members[1:]:
            for x in range(m.m):
                d0, d1 = m.delta[h0][x], m.delta[h][x]
                if (d0 is None) != (d1 is None):
                    return False
                if d0 is not None and pi[d0] != pi[d1]:
                    return False
    return True


def dynamic_admissible(pi: Sequence[int], m: Machine) -> bool:
    return static_admissible(pi, m) and right_congruent(pi, m)


def cost_bits(pi: Sequence[int], m: Machine) -> float:
    """H(Pi(H) | P) in bits over positive-mass states."""
    total = sum(m.probs)
    fibre_mass: dict = {}
    block_mass: dict = {}
    for h in range(m.n):
        p = m.probs[h]
        if p == 0:
            continue
        fibre_mass[m.P[h]] = fibre_mass.get(m.P[h], Fraction(0)) + p
        block_mass[(m.P[h], pi[h])] = block_mass.get((m.P[h], pi[h]), Fraction(0)) + p
    out = 0.0
    for (f, _), pb in block_mass.items():
        out += float(pb / total) * math.log2(float(fibre_mass[f] / pb))
    return out


def cond_entropy_bits(label: Sequence, given: Sequence, m: Machine) -> float:
    """H(label | given) in bits over positive-mass states."""
    total = sum(m.probs)
    g_mass: dict = {}
    j_mass: dict = {}
    for h in range(m.n):
        p = m.probs[h]
        if p == 0:
            continue
        g_mass[given[h]] = g_mass.get(given[h], Fraction(0)) + p
        key = (given[h], label[h])
        j_mass[key] = j_mass.get(key, Fraction(0)) + p
    out = 0.0
    for (g, _), pj in j_mass.items():
        out += float(pj / total) * math.log2(float(g_mass[g] / pj))
    return out


def _terminal_extensions(m: Machine, dyn: bool):
    """Terminal model: enumerate partitions of the current histories only and
    extend canonically to the zero-mass successors (Lemma A.L1): for the
    dynamic class, successors of a block under x form one block; for the
    static class, successors are singletons.  Cost, regret, Delta and K depend
    only on the current-history blocks, so this loses nothing and replaces
    Bell(n) by Bell(n0) partitions per machine."""
    cur = [h for h in range(m.n) if m.probs[h] > 0]
    for pi0 in rgs_partitions(len(cur)):
        full = [None] * m.n
        for i, h in enumerate(cur):
            full[h] = pi0[i]
        nxt = max(pi0, default=-1) + 1
        ids: dict = {}
        for i, h in enumerate(cur):
            for x in range(m.m):
                s = m.delta[h][x]
                if s is None:
                    continue
                key = (pi0[i], x) if dyn else ("s", s)
                if key not in ids:
                    ids[key] = nxt
                    nxt += 1
                full[s] = ids[key]
        for h in range(m.n):
            if full[h] is None:
                full[h] = nxt
                nxt += 1
        yield canon(full)


def admissible_partitions(m: Machine, pred: Callable) -> list:
    if is_terminal_model(m) and pred in (static_admissible, dynamic_admissible):
        gen = _terminal_extensions(m, pred is dynamic_admissible)
    else:
        gen = rgs_partitions(m.n)
    return [pi for pi in gen if pred(pi, m)]


def min_cost(m: Machine, pred: Callable):
    """(min cost, list of minimisers, list of (pi, cost)) over pred."""
    rows = [(pi, cost_bits(pi, m)) for pi in admissible_partitions(m, pred)]
    if not rows:
        return None, [], rows
    best = min(c for _, c in rows)
    return best, [pi for pi, c in rows if abs(c - best) <= TOL], rows


# --------------------------------------------------------- future regret


def regret_01_event(pi: Sequence[int], m: Machine, x: int) -> float:
    """Minimal expected 0-1 future regret of the best (Pi, x)-measurable rule.

    A history with delta(h, x) undefined contributes no regret.  Correct means
    the chosen action lies in A*(delta(h, x)).  Exact Bayes-risk identity
    (Prop. A.2): sum over cells of min_a P(cell) P(a not acceptable | cell).
    """
    total = sum(m.probs)
    acts = sorted(m.actions())
    out = Fraction(0)
    for members in blocks_of(pi).values():
        best = None
        for a in acts:
            err = Fraction(0)
            for h in members:
                s = m.delta[h][x]
                if s is not None and a not in m.a_star[s]:
                    err += m.probs[h]
            best = err if best is None else min(best, err)
        out += best or Fraction(0)
    return float(out / total)


def regret_01(pi: Sequence[int], m: Machine) -> float:
    return max(regret_01_event(pi, m, x) for x in range(m.m)) if m.m else 0.0


def bayes_regret_general(pi: Sequence[int], m: Machine, x: int, loss: dict) -> float:
    """General registered future loss: loss[(state, action)] -> Fraction.

    Regret r(h,a) = loss(delta(h,x), a) - min_a' loss(delta(h,x), a').
    """
    total = sum(m.probs)
    acts = sorted(m.actions())
    out = Fraction(0)
    for members in blocks_of(pi).values():
        best = None
        for a in acts:
            r = Fraction(0)
            for h in members:
                s = m.delta[h][x]
                if s is None:
                    continue
                r += m.probs[h] * (loss[(s, a)] - min(loss[(s, b)] for b in acts))
            best = r if best is None else min(best, r)
        out += best or Fraction(0)
    return float(out / total)


def minimax_cell_regret(members: Sequence[int], m: Machine, x: int, loss: dict) -> Fraction:
    acts = sorted(m.actions())
    best = None
    for a in acts:
        worst = Fraction(0)
        for h in members:
            s = m.delta[h][x]
            if s is None:
                continue
            worst = max(worst, loss[(s, a)] - min(loss[(s, b)] for b in acts))
        best = worst if best is None else min(best, worst)
    return best if best is not None else Fraction(0)


def eps_sets_intersect(members: Sequence[int], m: Machine, x: int, loss: dict, eps: Fraction) -> bool:
    acts = sorted(m.actions())
    common = set(acts)
    for h in members:
        s = m.delta[h][x]
        if s is None:
            continue
        mn = min(loss[(s, b)] for b in acts)
        common &= {a for a in acts if loss[(s, a)] - mn <= eps}
    return bool(common)


# ------------------------------------------------------- premium quantities


def premium(m: Machine) -> dict:
    c_stat, stat_opt, stat_rows = min_cost(m, static_admissible)
    c_dyn, dyn_opt, _ = min_cost(m, dynamic_admissible)
    if c_stat is None or c_dyn is None:
        return {"feasible": False}
    return {
        "feasible": True, "c_stat": c_stat, "c_dyn": c_dyn,
        "omega": c_dyn - c_stat, "stat_opt": stat_opt, "dyn_opt": dyn_opt,
        "stat_rows": stat_rows,
    }


def refines_on_support(finer: Sequence[int], coarser: Sequence[int], m: Machine) -> bool:
    """Refinement compared on positive-mass states only (zero-mass states are free)."""
    supp = [h for h in range(m.n) if m.probs[h] > 0]
    return refines([finer[h] for h in supp], [coarser[h] for h in supp])


def delta_of(pi: Sequence[int], m: Machine, dyn_parts: list | None = None) -> float:
    """Delta(Pi) = min over dynamic-admissible Pi' refining Pi on the support
    of H(Pi' | Pi): the entropy a given representation of the current histories
    must add to become prospectively adequate.  The discrete partition is always
    dynamic-admissible, so Delta is finite.
    """
    if dyn_parts is None:
        dyn_parts = admissible_partitions(m, dynamic_admissible)
    best = math.inf
    for pj in dyn_parts:
        if refines_on_support(pj, pi, m):
            best = min(best, cond_entropy_bits(pj, pi, m))
    return best


def regret_lb(pi: Sequence[int], m: Machine) -> float:
    """-log2(1 - R*(Pi)): proved lower bound on Delta(Pi) (min-entropy + Jensen)."""
    r = regret_01(pi, m)
    return math.inf if r >= 1 else -math.log2(1 - r)


def fano_ub(pi: Sequence[int], m: Machine) -> float:
    """sum_x phi_{k_x}(R*_x(Pi)): proved upper bound on Delta(Pi) under terminal+PC."""
    tot = 0.0
    for x in range(m.m):
        alphabet = set()
        for h in range(m.n):
            s = m.delta[h][x]
            if s is not None and m.probs[h] > 0:
                alphabet |= m.a_star[s]
        tot += fano_phi(regret_01_event(pi, m, x), len(alphabet))
    return tot


def conjecture_c1(m: Machine, pr: dict) -> float:
    """Refuted candidate: Omega >= min over static-OPTIMAL Pi of -log2(1-R*(Pi))."""
    return min(regret_lb(pi, m) for pi in pr["stat_opt"])


def vanishing_premium(u: Fraction) -> Machine:
    """Masses (1-2u, u, u); current {0},{0,1},{1}; future {0},{1},{1}.

    For u < 1/3 the unique static optimum {h0,h1},{h2} has regret u, while
    Omega_dyn = h_b(2u) - h_b(u) -> 0 as u -> 1/3: no nontrivial lower bound
    on the premium in terms of the static optimum's regret exists.
    """
    cur = (frozenset({0}), frozenset({0, 1}), frozenset({1}))
    succ = (frozenset({0}), frozenset({1}), frozenset({1}))
    return _terminal_machine(3, 1, (0, 0, 0), cur, succ, (1 - 2 * u, u, u), name=f"vanishing_u={u}")


def is_terminal_model(m: Machine) -> bool:
    """Current states = positive mass; successors distinct, zero mass, absorbing."""
    current = [h for h in range(m.n) if m.probs[h] > 0]
    succ = []
    for h in current:
        for x in range(m.m):
            s = m.delta[h][x]
            if s is None:
                continue
            if m.probs[s] > 0 or s in succ:
                return False
            succ.append(s)
    for s in range(m.n):
        if m.probs[s] == 0 and any(m.delta[s][x] not in (None, s) for x in range(m.m)):
            return False
    return True


def satisfies_pc(m: Machine) -> bool:
    """PC: definedness and successor fibre are functions of (P(h), x)."""
    seen: dict = {}
    for h in range(m.n):
        if m.probs[h] == 0:
            continue
        for x in range(m.m):
            s = m.delta[h][x]
            sig = None if s is None else m.P[s]
            key = (m.P[h], x)
            if key in seen and seen[key] != sig:
                return False
            seen[key] = sig
    return True


def successor_selectors(m: Machine):
    """All selectors d over successor states (d(s) in A*(s)); current states fixed."""
    succ = [s for s in range(m.n) if m.probs[s] == 0]
    for choice in itertools.product(*[sorted(m.a_star[s]) for s in succ]):
        yield dict(zip(succ, choice))


def upper_bound_label(m: Machine, pr: dict) -> float:
    """UB_label = min over static-optimal Pi_s and selectors d of
    H(L_d | Pi_s, P) with L_d(h) = (defined_x, fibre(succ_x), d(succ_x))_x."""
    best = math.inf
    for pi_s in pr["stat_opt"]:
        given = [(m.P[h], pi_s[h]) for h in range(m.n)]
        for d in successor_selectors(m):
            label = []
            for h in range(m.n):
                lab = []
                for x in range(m.m):
                    s = m.delta[h][x]
                    lab.append(None if s is None else (m.P[s], d[s]))
                label.append(tuple(lab))
            best = min(best, cond_entropy_bits(label, given, m))
    return best


def upper_bound_fano(m: Machine, pr: dict) -> float:
    """UB_fano = min over static-optimal Pi_s of sum_x phi_x(R*_x(Pi_s))."""
    return min(fano_ub(pi_s, m) for pi_s in pr["stat_opt"])


def upper_bound_delta(m: Machine, pr: dict) -> float:
    """min over static-optimal Pi_s of Delta(Pi_s)  (>= Omega_dyn)."""
    dyn = admissible_partitions(m, dynamic_admissible)
    return min(delta_of(pi_s, m, dyn) for pi_s in pr["stat_opt"])


# ----------------------------------------------------- cardinality premium


def blocks_per_fibre(pi: Sequence[int], m: Machine) -> int:
    per: dict = {}
    for h in range(m.n):
        if m.probs[h] > 0:
            per.setdefault(m.P[h], set()).add(pi[h])
    return max(len(v) for v in per.values())


def cardinality_premium(m: Machine, pr: dict) -> dict:
    k_stat = min(blocks_per_fibre(pi, m) for pi, _ in pr["stat_rows"])
    dyn = admissible_partitions(m, dynamic_admissible)
    k_dyn = min(blocks_per_fibre(pi, m) for pi in dyn)
    card_opt_dyn_exists = any(
        blocks_per_fibre(pi, m) == k_stat for pi in dyn)
    return {
        "k_stat": k_stat, "k_dyn": k_dyn,
        "omega_card": math.log2(k_dyn) - math.log2(k_stat),
        "omega_card_zero": k_dyn == k_stat,
        "omega_dyn_zero": abs(pr["omega"]) <= TOL,
        "card_opt_dyn_exists": card_opt_dyn_exists,
    }


# ------------------------------------------------------- multi-step notions


def word_successor(m: Machine, h: int, word: Sequence[int]):
    cur = h
    for x in word:
        cur = m.delta[cur][x]
        if cur is None:
            return None
    return cur


def n1(pi: Sequence[int], m: Machine) -> bool:
    """One-step action compatibility at every node (non-recursive)."""
    for members in blocks_of(pi).values():
        for x in range(m.m):
            defined = [m.delta[h][x] is not None for h in members]
            if any(defined) != all(defined):
                return False
            if not any(defined):
                continue
            common = None
            for h in members:
                s = m.delta[h][x]
                common = set(m.a_star[s]) if common is None else common & m.a_star[s]
            if not common:
                return False
    return True


def w_k(pi: Sequence[int], m: Machine, k: int) -> bool:
    """Word action compatibility for all words of length 1..k from every block."""
    for j in range(1, k + 1):
        for word in itertools.product(range(m.m), repeat=j):
            for members in blocks_of(pi).values():
                succ = [word_successor(m, h, word) for h in members]
                defined = [s is not None for s in succ]
                if any(defined) != all(defined):
                    return False
                if not any(defined):
                    continue
                common = None
                for s in succ:
                    common = set(m.a_star[s]) if common is None else common & m.a_star[s]
                if not common:
                    return False
    return True


def rc_closure(pi: Sequence[int], m: Machine) -> tuple:
    """Coarsest right-congruent refinement of pi (successor-signature iteration)."""
    cur = canon(pi)
    while True:
        sig = []
        for h in range(m.n):
            succ = tuple(None if m.delta[h][x] is None else cur[m.delta[h][x]] for x in range(m.m))
            sig.append((cur[h], succ))
        nxt = canon(sig)
        if nxt == cur:
            return cur
        cur = nxt


# --------------------------------------------------------- machine families


def _terminal_machine(n0: int, n_events: int, P0: Sequence[int], cur_sets: Sequence,
                      succ_sets: Sequence, probs0: Sequence[Fraction],
                      succ_fibres: Sequence | None = None, name: str = "") -> Machine:
    """Current states 0..n0-1; successor (h,x) -> n0 + h*n_events + x (absorbing).

    Default successor fibres follow PC: fibre(succ) = distinct id per (P0(h), x).
    """
    n = n0 + n0 * n_events
    P = list(P0)
    delta = []
    a_star = list(cur_sets)
    probs = list(probs0)
    for h in range(n0):
        delta.append(tuple(n0 + h * n_events + x for x in range(n_events)))
    fibre_base = max(P0) + 1
    for h in range(n0):
        for x in range(n_events):
            if succ_fibres is None:
                P.append(fibre_base + P0[h] * n_events + x)
            else:
                P.append(fibre_base + succ_fibres[h * n_events + x])
            a_star.append(frozenset(succ_sets[h * n_events + x]))
            probs.append(Fraction(0))
    for s in range(n0, n):
        delta.append(tuple(s for _ in range(n_events)))
    return Machine(tuple(P), tuple(delta), tuple(frozenset(a) for a in a_star),
                   tuple(probs), name)


SETS_2 = [frozenset({0}), frozenset({1}), frozenset({0, 1})]
SETS_3 = [frozenset(s) for r in (1, 2, 3) for s in itertools.combinations(range(3), r)]


BELL = {1: 1, 2: 2, 3: 5, 4: 15, 5: 52}


def terminal_family_size(n0: int, n_events: int, sets: Sequence, priors: Sequence) -> int:
    return BELL[n0] * len(sets) ** (n0 + n0 * n_events) * len(priors)


def terminal_family(n0: int, n_events: int, sets: Sequence, priors: Sequence, cap: int | None = None):
    """PC terminal family; exhaustive, or a deterministic stride subsample of
    at most ``cap`` machines (every ``stride``-th machine in enumeration order)."""
    size = terminal_family_size(n0, n_events, sets, priors)
    stride = 1 if cap is None or size <= cap else -(-size // cap)
    i = 0
    for P0 in rgs_partitions(n0):
        for cur in itertools.product(sets, repeat=n0):
            for succ in itertools.product(sets, repeat=n0 * n_events):
                for pr in priors:
                    if i % stride == 0:
                        yield _terminal_machine(n0, n_events, P0, cur, succ, pr)
                    i += 1


def uniform_prior(n0: int):
    return tuple(Fraction(1, n0) for _ in range(n0))


def skewed_priors(n0: int):
    if n0 == 2:
        return [(Fraction(9, 10), Fraction(1, 10)), (Fraction(3, 4), Fraction(1, 4))]
    if n0 == 3:
        return [(Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
                (Fraction(8, 10), Fraction(1, 10), Fraction(1, 10))]
    return [(Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8))]


def random_general_machine(rng: random.Random, n: int, m: int, n_actions: int) -> Machine:
    """Arbitrary registered machine: any delta (partial), masses on any state."""
    P = canon([rng.randrange(2) for _ in range(n)])
    delta = tuple(tuple(rng.choice([None] + list(range(n))) if rng.random() < 0.15
                        else rng.randrange(n) for _ in range(m)) for _ in range(n))
    a_star = tuple(frozenset(rng.sample(range(n_actions), rng.randint(1, n_actions)))
                   for _ in range(n))
    probs = tuple(Fraction(rng.randint(0, 3)) for _ in range(n))
    if sum(probs) == 0:
        probs = tuple(Fraction(1) for _ in range(n))
    return Machine(P, delta, a_star, probs, "random")


def random_terminal_nonpc(rng: random.Random, n0: int, n_events: int, sets: Sequence) -> Machine:
    P0 = canon([rng.randrange(2) for _ in range(n0)])
    cur = [rng.choice(sets) for _ in range(n0)]
    succ = [rng.choice(sets) for _ in range(n0 * n_events)]
    fibres = [rng.randrange(3) for _ in range(n0 * n_events)]
    probs = tuple(Fraction(rng.randint(1, 3)) for _ in range(n0))
    return _terminal_machine(n0, n_events, P0, cur, succ, probs, succ_fibres=fibres,
                             name="random_nonpc")


# --------------------------------------------------------- named fixtures


def witness(q: Fraction, same_succ_fibre: bool = False) -> Machine:
    """Two-history provenance witness with prior (q, 1-q).

    RETAIN=0 now for both; after x: REOPEN=1 for h_A, RETAIN=0 for h_B.
    The paper's fixture places the successors in distinct fibres; the variant
    ``same_succ_fibre`` keeps them in one fibre so the premium is decision-driven.
    """
    fibres = [0, 0] if same_succ_fibre else None
    return _terminal_machine(2, 1, (0, 0), (frozenset({0}), frozenset({0})),
                             (frozenset({1}), frozenset({0})), (q, 1 - q),
                             succ_fibres=fibres, name=f"witness_q={q}")


def phantom_premium() -> Machine:
    """Successors in distinct fibres, identical unique actions everywhere:
    Omega_dyn = 1 bit with zero future regret for every rule (PC violated)."""
    return _terminal_machine(2, 1, (0, 0), (frozenset({0}), frozenset({0})),
                             (frozenset({0}), frozenset({0})), (Fraction(1, 2), Fraction(1, 2)),
                             succ_fibres=[0, 1], name="phantom_premium")


def loose_upper_bound_example() -> Machine:
    """4 equiprobable histories: Omega_dyn = 0.5 bit but UB = 1 bit."""
    cur = (frozenset({0}), frozenset({0, 1}), frozenset({1}), frozenset({0, 1}))
    succ = (frozenset({2}), frozenset({3}), frozenset({2}), frozenset({3}))
    return _terminal_machine(4, 1, (0, 0, 0, 0), cur, succ, uniform_prior(4),
                             name="loose_ub")


def loose_ub_label_example() -> Machine:
    """Masses (1/2,1/4,1/4); current {0},{0,1},{1}; future {0},{1},{1}.

    Unique static optimum {h0,h1},{h2} (0.811 bit); dynamic optimum {h0},{h1,h2}
    (1 bit) does not refine it: Omega = 0.189 < UB_label = 0.689 and
    -log2(1-R*(static optimum)) = 0.415 > Omega, refuting conjecture C1.
    """
    cur = (frozenset({0}), frozenset({0, 1}), frozenset({1}))
    succ = (frozenset({0}), frozenset({1}), frozenset({1}))
    return _terminal_machine(3, 1, (0, 0, 0), cur, succ,
                             (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)), name="loose_ub_label")


def omega_dyn_zero_card_positive() -> Machine:
    """Masses (49,49,1,1)/100; current {0,1},{0,2},{1},{2}; future {0},{0},{1},{2}.

    Entropy-optimal static partition {h0,h1},{h2},{h3} (3 blocks) is dynamic, so
    Omega_dyn = 0; the only 2-block static partition {h0,h2},{h1,h3} is not
    dynamic, so K_stat = 2 < K_dyn = 3 and Omega_card = log2(3/2) > 0.
    """
    cur = (frozenset({0, 1}), frozenset({0, 2}), frozenset({1}), frozenset({2}))
    succ = (frozenset({0}), frozenset({0}), frozenset({1}), frozenset({2}))
    pr = (Fraction(49, 100), Fraction(49, 100), Fraction(1, 100), Fraction(1, 100))
    return _terminal_machine(4, 1, (0, 0, 0, 0), cur, succ, pr, name="omega_dyn_zero_card_positive")


def dormant_two_step() -> Machine:
    """Depth-2 chain: h0,h1 -> s0,s1 -> t0,t1.  All actions {0} except t0:{1}, t1:{2}.

    Pi = {h0,h1},{s0},{s1},{t0},{t1} satisfies N1 (one-step compatibility at every
    node) but not W_2 and is not a right congruence: the conflict is dormant for
    one step and surfaces at step 2.  Masses: h 1/2 each, deeper states 0.
    """
    P = (0, 0, 1, 1, 2, 2)
    delta = ((2,), (3,), (4,), (5,), (4,), (5,))
    a = (frozenset({0}),) * 4 + (frozenset({1}), frozenset({2}))
    probs = (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    return Machine(P, delta, a, probs, "dormant_two_step")


def shared_successor() -> Machine:
    """Non-injective delta: h0,h2 -> s_a ; h1 -> s_b ; h3 -> s_c.

    A*(s_a)={0,1}, A*(s_b)={0}, A*(s_c)={1}.  Initial partition {h0,h1},{h2,h3}
    is word-compatible (W_1) yet has no recursive (right-congruent) extension:
    the successor blocks {s_a,s_b} and {s_a,s_c} must merge into an incompatible
    block.
    """
    P = (0, 0, 0, 0, 1, 1, 1)
    delta = ((4,), (5,), (4,), (6,), (4,), (5,), (6,))
    a = (frozenset({0}),) * 4 + (frozenset({0, 1}), frozenset({0}), frozenset({1}))
    probs = (Fraction(1, 4),) * 4 + (Fraction(0),) * 3
    return Machine(P, delta, a, probs, "shared_successor")


def depth2_chain(cur_sets, mid_sets, leaf_sets, probs0, name="chain2") -> Machine:
    """n0 current -> n0 middle (zero mass) -> n0 leaves (absorbing), one event."""
    n0 = len(cur_sets)
    P = [0] * n0 + [1] * n0 + [2] * n0
    delta = [(n0 + h,) for h in range(n0)] + [(2 * n0 + h,) for h in range(n0)] \
        + [(2 * n0 + h,) for h in range(n0)]
    a = list(cur_sets) + list(mid_sets) + list(leaf_sets)
    probs = list(probs0) + [Fraction(0)] * (2 * n0)
    return Machine(tuple(P), tuple(delta), tuple(frozenset(s) for s in a), tuple(probs), name)


# ------------------------------------------------------------------ checks


def check_a_l1(machines: Iterable[Machine]) -> dict:
    """One-step reduction lemma: on terminal machines, dynamic admissibility ==
    static + per-block (matched definedness, constant successor fibre, nonempty
    joint future intersection)."""
    count = mismatches = 0
    for m in machines:
        assert is_terminal_model(m)
        for pi in rgs_partitions(m.n):
            lhs = dynamic_admissible(pi, m)
            rhs = static_admissible(pi, m)
            if rhs:
                for members in blocks_of(pi).values():
                    cur = [h for h in members if m.probs[h] > 0]
                    if not cur:
                        continue
                    for x in range(m.m):
                        sig = {(m.delta[h][x] is None,
                                None if m.delta[h][x] is None else m.P[m.delta[h][x]]) for h in cur}
                        if len(sig) > 1:
                            rhs = False
                            break
                        common = None
                        for h in cur:
                            s = m.delta[h][x]
                            if s is None:
                                continue
                            common = set(m.a_star[s]) if common is None else common & m.a_star[s]
                        if common is not None and not common:
                            rhs = False
                            break
                    if not rhs:
                        break
            # successor-side blocks must also be admissible for lhs; rhs is a
            # statement about current blocks given free successor blocks, so
            # compare on the projection: lhs implies rhs; rhs implies existence
            # of some dynamic partition with the same current blocks.
            if lhs and not rhs:
                mismatches += 1
            if rhs and not lhs:
                # find a dynamic partition with identical current blocks
                cur_ids = [h for h in range(m.n) if m.probs[h] > 0]
                proj = canon([pi[h] for h in cur_ids])
                ok = any(canon([pj[h] for h in cur_ids]) == proj and dynamic_admissible(pj, m)
                         for pj in rgs_partitions(m.n))
                if not ok:
                    mismatches += 1
            count += 1
        # count machines
    return {"partitions_checked": count, "mismatches": mismatches,
            "verdict": "PASS" if mismatches == 0 else "FAIL_COUNTEREXAMPLE_FOUND"}


def check_a_p1_p2(rng: random.Random, trials: int) -> dict:
    """epsilon-criterion and Bayes-regret identity / garbling monotonicity."""
    eps_checks = eps_mismatch = garble_checks = garble_viol = 0
    for _ in range(trials):
        n0 = rng.choice([2, 3, 4])
        m = random_terminal_nonpc(rng, n0, 1, SETS_3)
        acts = sorted(m.actions())
        loss = {(s, a): Fraction(rng.randint(0, 4)) for s in range(m.n) for a in acts}
        for pi in rgs_partitions(m.n):
            if not refines(pi, m.P):
                continue
            for members in blocks_of(pi).values():
                if all(m.probs[h] == 0 for h in members):
                    continue
                mm = minimax_cell_regret(members, m, 0, loss)
                for eps in (Fraction(0), Fraction(1), Fraction(2), mm, mm - Fraction(1, 2)):
                    if eps < 0:
                        continue
                    lhs = eps_sets_intersect(members, m, 0, loss, eps)
                    rhs = mm <= eps
                    eps_checks += 1
                    eps_mismatch += lhs != rhs
        # garbling: coarser partition -> Bayes regret no smaller
        parts = [pi for pi in rgs_partitions(m.n) if refines(pi, m.P)]
        for fine in parts:
            for coarse in parts:
                if refines(fine, coarse):
                    garble_checks += 1
                    if bayes_regret_general(coarse, m, 0, loss) < bayes_regret_general(fine, m, 0, loss) - TOL:
                        garble_viol += 1
    return {"eps_criterion_checks": eps_checks, "eps_mismatches": eps_mismatch,
            "garbling_pairs": garble_checks, "garbling_violations": garble_viol,
            "verdict": "PASS" if eps_mismatch == 0 and garble_viol == 0 else "FAIL_COUNTEREXAMPLE_FOUND"}


def check_bounds(machines: Iterable[Machine], require_pc: bool, conj_examples: list,
                 ub_examples: list, tag: str) -> dict:
    """Per-representation sandwich (A.T1) and premium-level bounds (A.T2)."""
    n = parts = 0
    lb_viol = fano_viol = lb_tight = fano_tight = both_tight = 0
    om_ub_delta_viol = om_fano_viol = label_eq_delta_viol = 0
    omega_pos = ub_delta_tight_pos = ub_fano_tight_pos = conj_viol = 0
    for m in machines:
        pr = premium(m)
        if not pr["feasible"]:
            continue
        n += 1
        om = pr["omega"]
        dyn = admissible_partitions(m, dynamic_admissible)
        terminal_pc = is_terminal_model(m) and (satisfies_pc(m) or not require_pc)
        fano_applicable = is_terminal_model(m) and satisfies_pc(m)
        for pi, _c in pr["stat_rows"]:
            parts += 1
            d = delta_of(pi, m, dyn)
            lb = regret_lb(pi, m)
            if lb > d + TOL:
                lb_viol += 1
            if abs(lb - d) <= TOL and d > TOL:
                lb_tight += 1
            if fano_applicable:
                fu = fano_ub(pi, m)
                if d > fu + TOL:
                    fano_viol += 1
                if abs(fu - d) <= TOL and d > TOL:
                    fano_tight += 1
                    both_tight += abs(lb - d) <= TOL
        ubd = upper_bound_delta(m, pr)
        if om > ubd + TOL:
            om_ub_delta_viol += 1
        if om > TOL:
            omega_pos += 1
            ub_delta_tight_pos += abs(ubd - om) <= TOL
            c1 = conjecture_c1(m, pr)
            if c1 > om + TOL:
                conj_viol += 1
                if len(conj_examples) < 3:
                    conj_examples.append({"machine": m.to_json(), "omega": om, "conjectured_lb": c1})
        if terminal_pc:
            ubl = upper_bound_label(m, pr)
            if abs(ubl - ubd) > TOL:
                label_eq_delta_viol += 1
            ubf = upper_bound_fano(m, pr)
            if om > ubf + TOL:
                om_fano_viol += 1
                if len(ub_examples) < 3:
                    ub_examples.append({"machine": m.to_json(), "omega": om, "ub_delta": ubd,
                                        "ub_fano": ubf, "pc": satisfies_pc(m)})
            if om > TOL and abs(ubf - om) <= TOL:
                ub_fano_tight_pos += 1
    return {"family": tag, "machines": n, "static_partitions": parts, "omega_positive": omega_pos,
            "T1_regret_lb_violations": lb_viol, "T1_fano_ub_violations": fano_viol,
            "T1_regret_lb_tight_delta_positive": lb_tight,
            "T1_fano_ub_tight_delta_positive": fano_tight,
            "T1_both_tight_delta_positive": both_tight,
            "T2_omega_gt_min_delta_violations": om_ub_delta_viol,
            "T2_omega_gt_fano_violations": om_fano_viol,
            "T2_label_formula_ne_delta": label_eq_delta_viol,
            "T2_min_delta_tight_among_omega_positive": ub_delta_tight_pos,
            "T2_fano_tight_among_omega_positive": ub_fano_tight_pos,
            "C1_conjecture_violations": conj_viol}


def check_b(machines: Iterable[Machine]) -> dict:
    n = viol = 0
    gt = lt = 0
    dyn0_card_pos = card0_dyn_pos = 0
    ex: dict = {}
    for m in machines:
        pr = premium(m)
        if not pr["feasible"]:
            continue
        n += 1
        cp = cardinality_premium(m, pr)
        if pr["c_stat"] > math.log2(cp["k_stat"]) + TOL or pr["c_dyn"] > math.log2(cp["k_dyn"]) + TOL:
            viol += 1
        if pr["omega"] > cp["omega_card"] + TOL:
            gt += 1
            ex.setdefault("omega_dyn_gt_omega_card", {"machine": m.to_json(), "omega_dyn": pr["omega"], "omega_card": cp["omega_card"]})
        if pr["omega"] < cp["omega_card"] - TOL:
            lt += 1
            ex.setdefault("omega_dyn_lt_omega_card", {"machine": m.to_json(), "omega_dyn": pr["omega"], "omega_card": cp["omega_card"]})
        if cp["omega_dyn_zero"] and not cp["omega_card_zero"]:
            dyn0_card_pos += 1
            ex.setdefault("omega_dyn_zero_but_omega_card_positive", {"machine": m.to_json(), "k_stat": cp["k_stat"], "k_dyn": cp["k_dyn"]})
        if cp["omega_card_zero"] and not cp["omega_dyn_zero"]:
            card0_dyn_pos += 1
            ex.setdefault("omega_card_zero_but_omega_dyn_positive", {"machine": m.to_json(), "omega_dyn": pr["omega"], "k_stat": cp["k_stat"], "k_dyn": cp["k_dyn"]})
    return {"machines": n, "log_cardinality_bound_violations": viol,
            "omega_dyn_gt_omega_card": gt, "omega_dyn_lt_omega_card": lt,
            "omega_dyn_zero_but_omega_card_positive": dyn0_card_pos,
            "omega_card_zero_but_omega_dyn_positive": card0_dyn_pos,
            "examples": ex,
            "verdict": "PASS" if viol == 0 else "FAIL_COUNTEREXAMPLE_FOUND"}


def witness_table() -> list:
    rows = []
    for q in (Fraction(1, 2), Fraction(3, 4), Fraction(9, 10), Fraction(99, 100)):
        for same in (False, True):
            m = witness(q, same_succ_fibre=same)
            pr = premium(m)
            cp = cardinality_premium(m, pr)
            merged = tuple(0 for _ in range(m.n))
            merged = canon([0, 0, 1, 2]) if not same else canon([0, 0, 1, 1])
            r = regret_01(merged, m)
            rows.append({
                "q": str(q), "successors_same_fibre": same,
                "c_stat": pr["c_stat"], "c_dyn": pr["c_dyn"], "omega_dyn": pr["omega"],
                "h_b(q)": hb(float(q)), "omega_card": cp["omega_card"],
                "regret_of_merged_state": r, "h_b(regret)": hb(r),
                "delta_of_merged": delta_of(merged, m), "regret_lb": regret_lb(merged, m),
                "fano_ub": fano_ub(merged, m),
                "omega_eq_hb_q": abs(pr["omega"] - hb(float(q))) <= TOL,
                "omega_eq_hb_regret": abs(pr["omega"] - hb(r)) <= TOL,
                "fano_tight": abs(fano_ub(merged, m) - pr["omega"]) <= TOL,
                "regret_lb_tight": abs(regret_lb(merged, m) - pr["omega"]) <= TOL,
            })
    return rows


def check_c(rng: random.Random, trials: int) -> dict:
    """Multi-step notions on random general machines + named fixtures."""
    impl_viol = wk_n1_viol = 0
    n1_not_w2 = 0
    checks = 0
    for _ in range(trials):
        m = random_general_machine(rng, rng.choice([3, 4, 5]), rng.choice([1, 2]), 3)
        for pi in rgs_partitions(m.n):
            if not static_admissible(pi, m):
                continue
            checks += 1
            rc = right_congruent(pi, m)
            a1 = n1(pi, m)
            w2 = w_k(pi, m, 2)
            w3 = w_k(pi, m, 3)
            if rc and a1 and not (w2 and w3):
                impl_viol += 1
            if (w2 or w3) and not a1:
                wk_n1_viol += 1
            if a1 and not w2:
                n1_not_w2 += 1
    # named fixture: dormant two-step
    d = dormant_two_step()
    pi_d = (0, 0, 1, 2, 3, 4)
    dormant = {
        "machine": d.to_json(), "pi": list(pi_d),
        "static": static_admissible(pi_d, d), "N1": n1(pi_d, d),
        "W1": w_k(pi_d, d, 1), "W2": w_k(pi_d, d, 2), "RC": right_congruent(pi_d, d),
        "rc_closure": list(rc_closure(pi_d, d)),
        "c_stat": premium(d)["c_stat"], "c_dyn": premium(d)["c_dyn"],
        "c_W1": min(cost_bits(p, d) for p in rgs_partitions(d.n) if static_admissible(p, d) and w_k(p, d, 1)),
        "c_W2": min(cost_bits(p, d) for p in rgs_partitions(d.n) if static_admissible(p, d) and w_k(p, d, 2)),
    }
    # shared successor: initial partition W-compatible but no RC extension
    s = shared_successor()
    init = (0, 0, 1, 1)
    cur_ids = [0, 1, 2, 3]
    has_rc_ext = any(canon([p[h] for h in cur_ids]) == canon(init) and dynamic_admissible(p, s)
                     for p in rgs_partitions(s.n))
    w_ok = all(w_k(p, s, 3) for p in [(0, 0, 1, 1, 2, 3, 4)])
    shared = {"machine": s.to_json(), "initial_partition": list(init),
              "word_compatible_from_initial_blocks": w_ok,
              "recursive_extension_exists": has_rc_ext}
    # injective zero-mass chain equivalence: W_inf(initial) <=> RC extension
    chain_checks = chain_viol = 0
    for _ in range(trials):
        n0 = rng.choice([2, 3])
        cur = [rng.choice(SETS_3) for _ in range(n0)]
        mid = [rng.choice(SETS_3) for _ in range(n0)]
        leaf = [rng.choice(SETS_3) for _ in range(n0)]
        ch = depth2_chain(cur, mid, leaf, uniform_prior(n0))
        for init in rgs_partitions(n0):
            full = tuple(init) + tuple(range(n0, 3 * n0))  # discrete deeper
            full = canon(full)
            if not static_admissible(full, ch):
                continue
            wc = w_k(full, ch, 2)
            ext = any(canon([p[h] for h in range(n0)]) == canon(init) and dynamic_admissible(p, ch)
                      for p in rgs_partitions(ch.n))
            chain_checks += 1
            if wc != ext:
                chain_viol += 1
    return {"random_partition_checks": checks,
            "rc_and_n1_implies_wk_violations": impl_viol,
            "wk_implies_n1_violations": wk_n1_viol,
            "n1_but_not_w2_instances": n1_not_w2,
            "dormant_two_step": dormant, "shared_successor": shared,
            "chain_equivalence_checks": chain_checks, "chain_equivalence_violations": chain_viol,
            "verdict": "PASS" if impl_viol == 0 and wk_n1_viol == 0 and chain_viol == 0
            and dormant["N1"] and not dormant["W2"] and not dormant["RC"]
            and shared["word_compatible_from_initial_blocks"] and not shared["recursive_extension_exists"]
            else "FAIL_COUNTEREXAMPLE_FOUND"}


def multistep_fano_ub(m: Machine, pr: dict, k: int) -> float:
    """Omega <= min_{Pi_s} Fano(sum_w R*_w(Pi_s), |A|^W) over words |w|<=k
    (terminal chain model with PC); loose but valid.  Word-regret uses the
    successor's A* at the end of the word."""
    best = math.inf
    words = [w for j in range(1, k + 1) for w in itertools.product(range(m.m), repeat=j)]
    acts = sorted(m.actions())
    total = sum(m.probs)
    for pi_s in pr["stat_opt"]:
        tot_r = 0.0
        for w in words:
            r = Fraction(0)
            for members in blocks_of(pi_s).values():
                best_a = None
                for a in acts:
                    err = Fraction(0)
                    for h in members:
                        if m.probs[h] == 0:
                            continue
                        s = word_successor(m, h, w)
                        if s is not None and a not in m.a_star[s]:
                            err += m.probs[h]
                    best_a = err if best_a is None else min(best_a, err)
                r += best_a or Fraction(0)
            tot_r += float(r / total)
        tot_r = min(tot_r, 1 - 1 / len(acts) ** len(words)) if tot_r > 0 else 0.0
        best = min(best, fano_phi(tot_r, len(acts) ** len(words)))
    return best


def check_c3(rng: random.Random, trials: int) -> dict:
    n = viol = 0
    for _ in range(trials):
        n0 = rng.choice([2, 3])
        cur = [rng.choice(SETS_2) for _ in range(n0)]
        mid = [rng.choice(SETS_2) for _ in range(n0)]
        leaf = [rng.choice(SETS_2) for _ in range(n0)]
        ch = depth2_chain(cur, mid, leaf, rng.choice([uniform_prior(n0)] + skewed_priors(n0)))
        pr = premium(ch)
        if not pr["feasible"]:
            continue
        n += 1
        if pr["omega"] > multistep_fano_ub(ch, pr, 2) + TOL:
            viol += 1
    return {"chains": n, "violations": viol, "verdict": "PASS" if viol == 0 else "FAIL_COUNTEREXAMPLE_FOUND"}


# --------------------------------------------------------------- driver


def run(full: bool, seed: int = 20260902, cap: int | None = None) -> dict:
    """``cap``: per-family bound on examined terminal machines (stride subsample);
    None = exhaustive.  The cap and stride are recorded per family."""
    rng = random.Random(seed)
    specs = [("terminal_n0=2_x=1_A<=3_uniform+skewed", 2, 1, SETS_3, [uniform_prior(2)] + skewed_priors(2))]
    if full:
        specs += [("terminal_n0=3_x=1_A<=3_uniform", 3, 1, SETS_3, [uniform_prior(3)]),
                  ("terminal_n0=3_x=1_A<=2_skewed", 3, 1, SETS_2, skewed_priors(3)),
                  ("terminal_n0=4_x=1_A<=2_uniform", 4, 1, SETS_2, [uniform_prior(4)]),
                  ("terminal_n0=3_x=2_A<=2_uniform", 3, 2, SETS_2, [uniform_prior(3)])]
    else:
        specs += [("terminal_n0=3_x=1_A<=2_uniform", 3, 1, SETS_2, [uniform_prior(3)])]
    conj_examples: list = []
    ub_examples: list = []
    bound_rows = []
    for tag, n0, ne, sets, priors in specs:
        size = terminal_family_size(n0, ne, sets, priors)
        row = check_bounds(terminal_family(n0, ne, sets, priors, cap), True, conj_examples, ub_examples, tag)
        row["family_size"] = size
        row["cap"] = cap
        row["stride"] = 1 if cap is None or size <= cap else -(-size // cap)
        row["exhaustive"] = row["stride"] == 1
        bound_rows.append(row)
    # general machines (LB only) and non-PC terminal (UB failure expected)
    n_rand = 3000 if full else 300
    general = [random_general_machine(rng, rng.choice([3, 4, 5]), rng.choice([1, 2]), 3) for _ in range(n_rand)]
    bound_rows.append(check_bounds(general, True, conj_examples, ub_examples, "random_general_n<=5"))
    nonpc = [random_terminal_nonpc(rng, rng.choice([2, 3]), 1, SETS_3) for _ in range(n_rand)]
    nonpc_ex: list = []
    bound_rows.append(check_bounds(nonpc, False, [], nonpc_ex, "random_terminal_nonPC"))
    named = {}
    for m in (witness(Fraction(1, 2)), phantom_premium(), loose_upper_bound_example(),
              loose_ub_label_example(), omega_dyn_zero_card_positive()):
        pr = premium(m)
        cp = cardinality_premium(m, pr)
        named[m.name] = {"machine": m.to_json(), "c_stat": pr["c_stat"], "c_dyn": pr["c_dyn"],
                         "omega": pr["omega"],
                         "conjecture_c1_value": conjecture_c1(m, pr),
                         "min_delta_static_opt": upper_bound_delta(m, pr),
                         "ub_label": upper_bound_label(m, pr), "ub_fano": upper_bound_fano(m, pr),
                         "per_static_optimum": [
                             {"pi": list(p), "regret": regret_01(p, m), "delta": delta_of(p, m),
                              "regret_lb": regret_lb(p, m), "fano_ub": fano_ub(p, m)}
                             for p in pr["stat_opt"]],
                         "pc": satisfies_pc(m), "static_optima": [list(p) for p in pr["stat_opt"]],
                         "dynamic_optima": [list(p) for p in pr["dyn_opt"]],
                         "regret_static_opt": [regret_01(p, m) for p in pr["stat_opt"]],
                         "k_stat": cp["k_stat"], "k_dyn": cp["k_dyn"], "omega_card": cp["omega_card"]}
    a_l1 = check_a_l1(list(terminal_family(3, 1, SETS_2, [uniform_prior(3)])) + nonpc[:200])
    a_p = check_a_p1_p2(rng, 60 if full else 15)
    b_fams = list(terminal_family(2, 1, SETS_3, [uniform_prior(2)] + skewed_priors(2)))
    b_fams += list(terminal_family(3, 1, SETS_2, [uniform_prior(3)] + skewed_priors(3)))
    if full:
        b_fams += list(terminal_family(4, 1, SETS_2, [uniform_prior(4)] + skewed_priors(4)))
    b = check_b(b_fams + general[: (1000 if full else 100)])
    c = check_c(rng, 400 if full else 40)
    c3 = check_c3(rng, 400 if full else 40)
    t1_ok = all(r["T1_regret_lb_violations"] == 0 and r["T1_fano_ub_violations"] == 0 for r in bound_rows)
    t2_ok = all(r["T2_omega_gt_min_delta_violations"] == 0 and r["T2_label_formula_ne_delta"] == 0
                and r["T2_omega_gt_fano_violations"] == 0
                for r in bound_rows if r["family"] != "random_terminal_nonPC")
    nonpc_row = next(r for r in bound_rows if r["family"] == "random_terminal_nonPC")
    vanishing = []
    for u in (Fraction(1, 4), Fraction(3, 10), Fraction(8, 25), Fraction(33, 100), Fraction(333, 1000)):
        vm = vanishing_premium(u)
        vp = premium(vm)
        vanishing.append({"u": str(u), "omega": vp["omega"],
                          "min_regret_static_optima": min(regret_01(p, vm) for p in vp["stat_opt"]),
                          "n_static_optima": len(vp["stat_opt"])})
    receipt = {
        "schema": SCHEMA, "full": full, "seed": seed, "cap_per_terminal_family": cap,
        "A_L1_one_step_reduction": a_l1,
        "A_P1_P2_eps_criterion_and_bayes_regret": a_p,
        "A_T1_T2_bounds_by_family": bound_rows,
        "A_T1_sandwich_verdict": "PASS" if t1_ok else "FAIL_COUNTEREXAMPLE_FOUND",
        "A_T2_premium_bounds_pc_verdict": "PASS" if t2_ok else "FAIL_COUNTEREXAMPLE_FOUND",
        "A_T2_upper_bound_without_pc": {
            "omega_gt_min_delta_violations": nonpc_row["T2_omega_gt_min_delta_violations"],
            "label_formula_ne_delta": nonpc_row["T2_label_formula_ne_delta"],
            "omega_gt_fano_violations": nonpc_row["T2_omega_gt_fano_violations"],
            "machines": nonpc_row["machines"], "examples": nonpc_ex,
            "verdict": ("PC_LOAD_BEARING_FOR_FANO_FORM__LABEL_FORM_HOLDS"
                        if nonpc_row["T2_omega_gt_fano_violations"] > 0
                        and nonpc_row["T2_omega_gt_min_delta_violations"] == 0
                        and nonpc_row["T2_label_formula_ne_delta"] == 0
                        else "FAIL_COUNTEREXAMPLE_FOUND" if nonpc_row["T2_omega_gt_min_delta_violations"] > 0
                        or nonpc_row["T2_label_formula_ne_delta"] > 0
                        else "NO_VIOLATION_FOUND")},
        "A_C1_no_nontrivial_lower_bound_on_omega": {
            "conjecture_violations": sum(r["C1_conjecture_violations"] for r in bound_rows),
            "examples": conj_examples,
            "named_counterexample": named["loose_ub_label"],
            "vanishing_premium_family": vanishing,
            "verdict": "REFUTED" if (conj_examples or named["loose_ub_label"]["conjecture_c1_value"]
                                     > named["loose_ub_label"]["omega"] + TOL) else "NOT_REFUTED_IN_FAMILY"},
        "A_T3_named_examples": named,
        "A_T3_witness_table": witness_table(),
        "B_cardinality": b,
        "C_multistep": c,
        "C3_multistep_fano_ub_depth2": c3,
        "scientific_authority": False, "empirical_llm_result": False,
    }
    return receipt


TERMINALS = {
    "A_eps_criterion": {
        "terminal": "PARENT_OWNED",
        "parent": "Li-Walsh-Littman 2006 a*-irrelevance abstraction; Abel-Hershkowitz-Littman 2016 approximate abstraction; sublevel-set restatement of min_a max_h regret <= eps",
        "proved": True, "mechanized": "A_P1_P2"},
    "A_expected_regret_identity": {
        "terminal": "PARENT_OWNED",
        "parent": "Bayes risk of a garbled experiment; Blackwell 1953 garbling monotonicity; Le Cam deficiency as the loss-uniform version",
        "proved": True, "mechanized": "A_P1_P2"},
    "A_representation_sandwich": {
        "terminal": "PROVED_ELEMENTARY_COMPOSITION",
        "statement": "for every static-admissible Pi: -log2(1-R*(Pi)) <= Delta(Pi) (every registered machine) and Delta(Pi) <= sum_x phi_{k_x}(R*_x(Pi)) (one-step terminal model + predictive congruence); Delta(Pi) = entropy a dynamic refinement must add",
        "premium_level": "Omega_dyn <= min_{static-optimal Pi_s} Delta(Pi_s) <= Fano form; hence every static optimum has regret >= phi^{-1}(Omega_dyn) under terminal+PC",
        "tight_on": "two-history witness: both sides at uniform prior, Fano side at every prior; uniform cells with all-distinct required actions",
        "not_tight": "loose_ub_label: Delta=0.689, regret_lb=0.415, fano_ub=0.811",
        "assumption_load_bearing": "PC: phantom_premium has Omega=1 with zero regret (Fano form fails; label form holds)",
        "parents_conceded": "Fano 1961; H_inf <= H (min-entropy); Jensen; Li-Walsh-Littman a*-irrelevance; ISFSM/right-congruence refinement",
        "mechanized": "A_T1_T2_T3"},
    "A_lower_bound_on_premium_from_regret": {
        "terminal": "NO_NONTRIVIAL_BOUND",
        "counterexample": "vanishing_premium family masses (1-2u,u,u): unique static optimum has regret u while Omega_dyn = h_b(2u)-h_b(u) -> 0 as u -> 1/3; loose_ub_label refutes Omega >= -log2(1-R*(static optimum)); the min-over-all-partitions bound is attained by the dynamic optimum itself (vacuous)",
        "mechanized": "A_C1"},
    "B_cardinality_premium": {
        "terminal": "PARENT_OWNED",
        "parent": "Paull-Unger 1959 minimal closed cover of an incompletely specified machine; Zhang et al. 2026 Cor. 3.12 (max_o |C_o| symbols)",
        "elementary_facts_proved": "C* <= log2 K* per class; witness Omega_card = 1 for every prior while Omega_dyn = h_b(q); no ordering between Omega_dyn and Omega_card; the two zero-premium conditions are inequivalent",
        "mechanized": "B_cardinality"},
    "C_multistep_reduction": {
        "terminal": "PARENT_OWNED",
        "parent": "right congruence / Nerode; Subramanian et al. 2022 P2a; Zhang et al. 2026 stable quotient; JOINT_DYNAMIC_STATE_OPTIMIZATION_V1 J3",
        "proved": "Pi recursively compatible <=> Pi right-congruent and one-step compatible at every node; rc_closure preserves node compatibility; injective zero-mass chain: word compatibility <=> recursive extension",
        "counterexamples": "dormant_two_step (N1 holds, W_2 fails, k=2 needed); shared_successor (non-injective delta: word-compatible initial partition with no recursive extension)",
        "mechanized": "C_multistep"},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--json-out", type=Path)
    ap.add_argument("--seed", type=int, default=20260902)
    ap.add_argument("--cap", type=int, default=None,
                    help="max terminal machines per family (deterministic stride subsample)")
    args = ap.parse_args()
    receipt = run(args.full, args.seed, args.cap)
    result = {"schema": "orion-v2.h-ext4-result.v1", "hypothesis": "H-EXT-4",
              "terminals": TERMINALS, "mechanized_receipt": receipt}
    text = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    summary = {k: v for k, v in receipt.items() if k.endswith("verdict")}
    summary["A_C1"] = receipt["A_C1_no_nontrivial_lower_bound_on_omega"]["verdict"]
    summary["A_T2_nonpc"] = receipt["A_T2_upper_bound_without_pc"]["verdict"]
    summary["B"] = receipt["B_cardinality"]["verdict"]
    summary["C"] = receipt["C_multistep"]["verdict"]
    summary["C3"] = receipt["C3_multistep_fano_ub_depth2"]["verdict"]
    print(json.dumps(summary, indent=2))
    bad = [k for k, v in summary.items() if v.startswith("FAIL")]
    return 3 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
