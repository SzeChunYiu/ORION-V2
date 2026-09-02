#!/usr/bin/env python3
"""Prospective power / MDE arithmetic for E30-R12 (registered before dispatch).

The registered primary test is an exact two-sided McNemar (sign-binomial) test on
task-level discordant pairs, with Holm step-down over a family of three F2-vs-control
contrasts.  Power therefore depends on two quantities and nothing else:

* ``psi``   -- the proportion of tasks that are *discordant* between the two arms
              (one arm succeeds, the other does not).  Concordant tasks carry no
              information for this test.
* ``delta`` -- the true task-level risk difference, ``P(F2 only) - P(control only)``.

with ``P(F2 only) = (psi + delta) / 2`` and ``P(control only) = (psi - delta) / 2``.

Everything below is exact enumeration -- no normal approximation, no simulation, so
the numbers are reproducible bit-for-bit.  This module is pure arithmetic; it reads
no experimental outcome and is safe to freeze pre-dispatch.
"""
from __future__ import annotations

import argparse
import json
from functools import lru_cache
from math import comb, exp, lgamma, log, log1p

NEG_INF = float("-inf")


# Holm step-down over a family of three: the *smallest* p-value in the family is
# compared against alpha/3, so a single contrast can only reject at that level.
FAMILY_SIZE = 3
ALPHA = 0.05


def holm_first_step_alpha(alpha: float = ALPHA, family_size: int = FAMILY_SIZE) -> float:
    return alpha / family_size


@lru_cache(maxsize=None)
def exact_mcnemar_p(discordant: int, favouring: int) -> float:
    """Two-sided exact binomial (sign) p-value on the discordant pairs."""
    if discordant == 0:
        return 1.0
    lo = min(favouring, discordant - favouring)
    tail = sum(comb(discordant, k) for k in range(lo + 1)) / (2.0 ** discordant)
    return min(1.0, 2.0 * tail)


@lru_cache(maxsize=None)
def min_discordant_for_rejection(alpha_level: float) -> int:
    """Smallest all-one-directional discordant count that can clear ``alpha_level``.

    With every discordant pair pointing the same way the p-value is ``2 * 0.5**d``;
    below the returned ``d`` the test is *arithmetically incapable* of rejecting,
    however large the true effect.
    """
    d = 1
    while d <= 4096:
        if exact_mcnemar_p(d, d) <= alpha_level:
            return d
        d += 1
    raise ValueError("no discordant count clears the level")


def _log_binom_pmf(n: int, k: int, p: float) -> float:
    if k < 0 or k > n:
        return NEG_INF
    if p <= 0.0:
        return 0.0 if k == 0 else NEG_INF
    if p >= 1.0:
        return 0.0 if k == n else NEG_INF
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
            + k * log(p) + (n - k) * log1p(-p))


def _binom_pmf(n: int, k: int, p: float) -> float:
    lp = _log_binom_pmf(n, k, p)
    return 0.0 if lp == NEG_INF else exp(lp)


@lru_cache(maxsize=None)
def _critical_k(discordant: int, alpha_level: float) -> int:
    """Largest ``k`` with two-sided exact p at ``min(a, d-a) == k`` still <= alpha.

    Returns -1 when no split of ``discordant`` pairs can reject at this level.
    """
    if discordant == 0:
        return -1
    cumulative = 0.0
    best = -1
    for k in range((discordant // 2) + 1):
        cumulative += _binom_pmf(discordant, k, 0.5)
        if min(1.0, 2.0 * cumulative) <= alpha_level:
            best = k
        else:
            break
    return best


def power(n_tasks: int, psi: float, delta: float, alpha_level: float) -> float:
    """Exact power of the registered two-sided exact test.

    Conditioning on the discordant count keeps this stable at any ``n``: the number
    of discordant tasks is ``Binomial(n, psi)`` and, given it, the number favouring
    F2 is ``Binomial(d, (psi + delta) / (2 * psi))``.
    """
    if psi <= 0.0 or abs(delta) > psi:
        return 0.0
    q = (psi + delta) / (2.0 * psi)
    total = 0.0
    for d in range(n_tasks + 1):
        weight = _binom_pmf(n_tasks, d, psi)
        if weight < 1e-18:
            continue
        k = _critical_k(d, alpha_level)
        if k < 0:
            continue
        lower = sum(_binom_pmf(d, a, q) for a in range(0, k + 1))
        upper = sum(_binom_pmf(d, a, q) for a in range(max(k + 1, d - k), d + 1))
        total += weight * (lower + upper)
    return total


def mde(n_tasks: int, psi: float, alpha_level: float, target_power: float = 0.80,
        step: float = 0.0005) -> float | None:
    """Smallest ``delta`` reaching ``target_power`` at this ``n`` and ``psi``."""
    delta = step
    while delta <= psi:
        if power(n_tasks, psi, delta, alpha_level) >= target_power:
            return round(delta, 4)
        delta += step
    return None


def required_n(psi: float, delta: float, alpha_level: float, target_power: float = 0.80,
               n_max: int = 4000) -> int | None:
    """Smallest task count reaching ``target_power`` for this true effect."""
    lo, hi = 1, n_max
    if power(n_max, psi, delta, alpha_level) < target_power:
        return None
    while lo < hi:                                    # power is monotone in n here
        mid = (lo + hi) // 2
        if power(mid, psi, delta, alpha_level) >= target_power:
            hi = mid
        else:
            lo = mid + 1
    return lo


def build_note(n_tasks: int = 40, psis: tuple[float, ...] = (0.10, 0.20, 0.30, 0.40),
               registered_mid: float = 0.05) -> dict:
    alpha_level = holm_first_step_alpha()
    d_min = min_discordant_for_rejection(alpha_level)
    return {
        "schema_version": "orion.v2.e30-r12-power-note.v1",
        "test": "exact two-sided McNemar / sign-binomial on task-level discordant pairs",
        "multiplicity": f"Holm step-down, family size {FAMILY_SIZE}, alpha {ALPHA}",
        "first_step_alpha": alpha_level,
        "n_tasks": n_tasks,
        "registered_minimum_important_difference": registered_mid,
        "arithmetic_floor": {
            "min_all_one_directional_discordant_tasks": d_min,
            "implied_minimum_observable_risk_difference": round(d_min / n_tasks, 4),
            "meaning": (
                f"with fewer than {d_min} discordant tasks all pointing the same way the "
                f"exact test cannot reach {alpha_level:.5f} at any effect size"
            ),
        },
        "mde_at_n": [
            {"discordance_psi": psi,
             "mde_risk_difference": mde(n_tasks, psi, alpha_level),
             "power_at_registered_mid": round(power(n_tasks, psi, registered_mid, alpha_level), 4)}
            for psi in psis
        ],
        "required_n_for_registered_mid": [
            {"discordance_psi": psi,
             "tasks_for_80pct_power": required_n(psi, registered_mid, alpha_level)}
            for psi in psis
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-tasks", type=int, default=40)
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    note = build_note(n_tasks=args.n_tasks)
    text = json.dumps(note, indent=2)
    if args.out:
        from pathlib import Path
        Path(args.out).write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
