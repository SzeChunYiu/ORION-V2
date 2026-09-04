#!/usr/bin/env python3
"""SD70-V3 frozen statistical procedures (stdlib only, deterministic).

- Wilson score interval for a proportion.
- Paired difference in exact accuracy with a deterministic percentile bootstrap.
- Exact one-sided McNemar mid-p on discordant pairs.
- Holm step-down multiplicity correction.
- Prospective paired-binary power / sample size (Connor 1987 normal approximation).
"""
from __future__ import annotations

import math
import random
from typing import Sequence

Z975 = 1.959963984540054
Z95 = 1.6448536269514722
Z80 = 0.8416212335729143


def wilson(k: int, n: int, z: float = Z975) -> tuple[float, float, float]:
    if n <= 0:
        return (0.0, 0.0, 1.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def paired_difference(a: Sequence[bool], b: Sequence[bool], bootstrap: int = 10000, seed: int = 20260902,
                      level: float = 0.95) -> dict:
    """Difference acc(a) - acc(b) over the same tasks, with percentile bootstrap CI."""
    if len(a) != len(b):
        raise ValueError("paired sequences differ in length")
    n = len(a)
    if n == 0:
        return {"n": 0, "point": 0.0, "ci_low": 0.0, "ci_high": 0.0, "b": 0, "c": 0}
    diffs = [int(bool(x)) - int(bool(y)) for x, y in zip(a, b)]
    point = sum(diffs) / n
    rng = random.Random(seed)
    stats = []
    for _ in range(bootstrap):
        s = 0
        for _i in range(n):
            s += diffs[rng.randrange(n)]
        stats.append(s / n)
    stats.sort()
    lo_idx = int(math.floor((1 - level) / 2 * bootstrap))
    hi_idx = int(math.ceil((1 + level) / 2 * bootstrap)) - 1
    lo_idx = min(max(lo_idx, 0), bootstrap - 1)
    hi_idx = min(max(hi_idx, 0), bootstrap - 1)
    b_ = sum(1 for d in diffs if d == 1)  # a correct, b wrong
    c_ = sum(1 for d in diffs if d == -1)  # a wrong, b correct
    return {"n": n, "point": point, "ci_low": stats[lo_idx], "ci_high": stats[hi_idx], "b": b_, "c": c_,
            "bootstrap": bootstrap, "seed": seed, "level": level}


def mcnemar_midp_one_sided(b: int, c: int) -> float:
    """P(X >= b) - 0.5 P(X = b), X ~ Binomial(b + c, 1/2). Tests a > b direction."""
    n = b + c
    if n == 0:
        return 1.0
    total = 0.0
    for k in range(b, n + 1):
        total += math.comb(n, k)
    at = math.comb(n, b)
    return (total - 0.5 * at) / (2 ** n)


def holm(pvalues: dict[str, float], alpha: float = 0.05) -> dict[str, dict]:
    items = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(items)
    out: dict[str, dict] = {}
    rejected_so_far = True
    for rank, (name, p) in enumerate(items):
        threshold = alpha / (m - rank)
        reject = rejected_so_far and p <= threshold
        if not reject:
            rejected_so_far = False
        out[name] = {"p": p, "holm_threshold": threshold, "reject": reject, "rank": rank + 1}
    return out


def paired_sample_size(delta: float, discordance: float, alpha_one_sided: float = 0.025, power: float = 0.80) -> int:
    """Connor (1987) normal-approximation sample size for a paired binary
    comparison with difference `delta` and total discordance proportion
    `discordance` (= p10 + p01)."""
    if delta <= 0 or discordance <= delta:
        raise ValueError("delta must be positive and below the discordance proportion")
    z_a = _z(1 - alpha_one_sided)
    z_b = _z(power)
    num = (z_a * math.sqrt(discordance) + z_b * math.sqrt(discordance - delta * delta)) ** 2
    return int(math.ceil(num / (delta * delta)))


def paired_power(n: int, delta: float, discordance: float, alpha_one_sided: float = 0.025) -> float:
    if discordance <= delta * delta:
        return 1.0
    z_a = _z(1 - alpha_one_sided)
    num = delta * math.sqrt(n) - z_a * math.sqrt(discordance)
    return _phi(num / math.sqrt(discordance - delta * delta))


def _phi(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _z(p: float) -> float:
    # inverse normal CDF by bisection (deterministic, stdlib only)
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if _phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
