#!/usr/bin/env python3
"""Check whether FM80 §9.1 and §9.2 are jointly satisfiable at a given sample size.

FM80 (`research/experiments/FM80_NATURALISTIC_TRANSFER_DECISIVE_PROTOCOL_V1.md`) is the
registered standalone survival gate for papers P-A and P-B. Its §9 promotes them beyond HOLD
only if

    §9.1  A3 improves the protected endpoint by >= 10 percentage points in >= 2 of 3 domains
    §9.2  the paired 95% interval for those improvements excludes zero, Holm-adjusted over the
          three domain-level primary tests

and §8 sets the sample at "90 eligible cases, at least 30 per domain" with "exact paired tests".

Under an exact paired test only discordant pairs carry information, so a clause pair can be
unsatisfiable by construction: an effect exactly on the §9.1 bar may be undetectable at the
registered n no matter how the pairing falls. That is not low power — it is a design that
cannot return the result it declares meaningful, and it would read as an empirical negative.

Exit codes:
    0  SATISFIABLE      a bare 10pp effect can clear §9.2 at this n
    1  UNSATISFIABLE    it cannot, under the most favourable possible pairing
    2  CANNOT_CHECK     inputs are outside the range this analysis covers

--self-test asserts all three verdicts are reachable, including the no-alarm case.
"""
from __future__ import annotations

import argparse
import sys
from math import ceil, comb

SATISFIABLE, UNSATISFIABLE, CANNOT_CHECK = 0, 1, 2
NAME = {SATISFIABLE: "SATISFIABLE", UNSATISFIABLE: "UNSATISFIABLE", CANNOT_CHECK: "CANNOT_CHECK"}

REGISTERED_N_PER_DOMAIN = 30      # §8
REGISTERED_EFFECT_PP = 10.0       # §9.1
DOMAINS = 3                       # §2
ALPHA = 0.05                      # §8


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p from the discordant cells."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2**n)


def holm_thresholds(alpha: float, m: int) -> list[float]:
    """Holm's step-down ladder: alpha/m, alpha/(m-1), ..., alpha."""
    return [alpha / (m - i) for i in range(m)]


def best_case_p(n: int, effect_pp: float) -> tuple[int, float]:
    """Net favouring pairs at `effect_pp`, and the smallest exact p any consistent table gives.

    The most favourable table is zero adverse discordance: every discordant pair favours A3.
    Any real table has u >= 0 adverse pairs and a strictly larger p, so a failure here is
    structural rather than a matter of luck.
    """
    t = ceil(effect_pp / 100.0 * n)
    return t, mcnemar_exact(t, 0)


def evaluate(n: int, effect_pp: float = REGISTERED_EFFECT_PP, alpha: float = ALPHA,
             domains: int = DOMAINS, holm: bool = True) -> tuple[int, dict]:
    if n <= 0:
        return CANNOT_CHECK, {"reason": "sample size must be positive"}
    if not 0 < effect_pp <= 100:
        return CANNOT_CHECK, {"reason": "effect must lie in (0, 100] percentage points"}
    if domains < 1:
        return CANNOT_CHECK, {"reason": "at least one domain is required"}

    t, p = best_case_p(n, effect_pp)
    ladder = holm_thresholds(alpha, domains)
    # §9.1 needs >= 2 of 3 domains, so the binding thresholds are the two most stringent rungs.
    threshold = ladder[min(1, len(ladder) - 1)] if holm else alpha
    strictest = ladder[0] if holm else alpha

    facts = {
        "n_per_domain": n,
        "effect_pp": effect_pp,
        "net_favouring_pairs_at_that_effect": t,
        "best_case_exact_p": p,
        "alpha": alpha,
        "holm_applied": holm,
        "holm_ladder": ladder if holm else None,
        "binding_threshold_for_the_second_passing_domain": threshold,
        "strictest_threshold_for_the_first": strictest,
        "assumption": "zero adverse discordance — a strict upper bound on achievable significance",
    }
    if p < threshold:
        facts["reason"] = "a bare effect at the stated bar can clear the significance clause"
        return SATISFIABLE, facts
    facts["reason"] = ("an effect exactly at the stated bar cannot clear the significance clause "
                       "under any consistent pairing")
    return UNSATISFIABLE, facts


def min_n_for(effect_pp: float, alpha: float, domains: int, holm: bool, cap: int = 5000) -> int | None:
    for n in range(1, cap + 1):
        if evaluate(n, effect_pp, alpha, domains, holm)[0] == SATISFIABLE:
            return n
    return None


def min_effect_at(n: int, alpha: float, domains: int, holm: bool) -> float | None:
    for t in range(1, n + 1):
        if evaluate(n, 100.0 * t / n, alpha, domains, holm)[0] == SATISFIABLE:
            return 100.0 * t / n
    return None


def self_test() -> bool:
    ok = True

    def case(label: str, got: int, want: int, extra: str = "") -> None:
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: want {NAME[want]}, got {NAME[got]} {extra}")

    # The alarm case: the registered design.
    code, rep = evaluate(30)
    case("registered §8 sample n=30 with the §9.1 10pp bar", code, UNSATISFIABLE,
         f"(best-case p={rep['best_case_exact_p']:.4f})")
    # The no-alarm case, asserted not assumed — a checker that always alarms is worthless.
    code, rep = evaluate(120)
    case("no-alarm control: n=120, same 10pp bar", code, SATISFIABLE,
         f"(best-case p={rep['best_case_exact_p']:.5f})")
    code, rep = evaluate(30, effect_pp=40.0)
    case("no-alarm control: n=30 with a large 40pp bar", code, SATISFIABLE,
         f"(best-case p={rep['best_case_exact_p']:.5f})")
    # Refusals must be distinct from a negative.
    case("cannot-check: n=0", evaluate(0)[0], CANNOT_CHECK)
    case("cannot-check: effect 0pp", evaluate(30, effect_pp=0.0)[0], CANNOT_CHECK)
    case("cannot-check: effect >100pp", evaluate(30, effect_pp=101.0)[0], CANNOT_CHECK)
    # Monotonicity: raising n must never turn SATISFIABLE back into UNSATISFIABLE.
    seen_sat = False
    mono = True
    for n in range(1, 400):
        c = evaluate(n)[0]
        if c == SATISFIABLE:
            seen_sat = True
        elif seen_sat and c == UNSATISFIABLE:
            mono = False
            break
    ok &= mono
    print(f"  [{'PASS' if mono else 'FAIL'}] monotone in n: once satisfiable, stays satisfiable")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--n-per-domain", type=int, default=REGISTERED_N_PER_DOMAIN)
    ap.add_argument("-e", "--effect-pp", type=float, default=REGISTERED_EFFECT_PP)
    ap.add_argument("--alpha", type=float, default=ALPHA)
    ap.add_argument("--domains", type=int, default=DOMAINS)
    ap.add_argument("--no-holm", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    print(f"interpreter: python {sys.version.split()[0]}")
    if a.self_test:
        print("self-test (checker validated before any verdict is trusted):")
        good = self_test()
        print("self-test:", "PASS" if good else "FAIL")
        return 0 if good else 2

    holm = not a.no_holm
    code, rep = evaluate(a.n_per_domain, a.effect_pp, a.alpha, a.domains, holm)
    print(f"FM80 §9.1 x §9.2 joint reachability: {NAME[code]} (exit {code})")
    for k in ("n_per_domain", "effect_pp", "net_favouring_pairs_at_that_effect",
              "best_case_exact_p", "binding_threshold_for_the_second_passing_domain",
              "assumption", "reason"):
        print(f"  {k}: {rep[k]}")

    if code == UNSATISFIABLE:
        need_n = min_n_for(a.effect_pp, a.alpha, a.domains, holm)
        need_e = min_effect_at(a.n_per_domain, a.alpha, a.domains, holm)
        print("  repair options, both stated because they differ:")
        print(f"    raise the sample : n >= {need_n} per domain "
              f"({need_n * a.domains} total) to keep the {a.effect_pp:g}pp bar")
        print(f"    raise the bar    : {need_e:.1f}pp is the detectable effect at n={a.n_per_domain} "
              f"({need_e / a.effect_pp:.1f}x the stated bar)")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
