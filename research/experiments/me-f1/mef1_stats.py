"""ME-F1 statistics: prospective power and the frozen tests (stdlib only).

Same shape as ``sd70v2_stats`` so the prospective numbers in the design JSON are
reproducible by a one-line call rather than asserted in prose.  Nothing here reads
data; it is arithmetic frozen with the design.
"""
from __future__ import annotations

import math


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _z(p: float) -> float:
    """Inverse normal CDF by deterministic bisection (200 steps)."""
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if _phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def paired_sample_size(delta: float, discordance: float,
                       alpha_one_sided: float = 0.025, power: float = 0.80) -> int:
    """Connor (1987) normal-approximation sample size for a paired binary comparison.

    ``delta`` is the difference to detect and ``discordance`` the total discordant
    proportion (p10 + p01).
    """
    if delta <= 0 or discordance <= delta:
        raise ValueError("delta must be positive and below the discordance proportion")
    z_a = _z(1 - alpha_one_sided)
    z_b = _z(power)
    num = (z_a * math.sqrt(discordance) + z_b * math.sqrt(discordance - delta * delta)) ** 2
    return int(math.ceil(num / (delta * delta)))


def paired_power(n: int, delta: float, discordance: float,
                 alpha_one_sided: float = 0.025) -> float:
    if discordance <= delta * delta:
        return 1.0
    z_a = _z(1 - alpha_one_sided)
    num = delta * math.sqrt(n) - z_a * math.sqrt(discordance)
    return _phi(num / math.sqrt(discordance - delta * delta))


def mde_at_n(n: int, discordance: float, alpha_one_sided: float = 0.025,
             power: float = 0.80) -> float:
    """Smallest detectable paired difference at ``n`` -- bisection on ``paired_power``."""
    lo, hi = 1e-6, min(0.999, discordance - 1e-9)
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if paired_power(n, mid, discordance, alpha_one_sided) < power:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def exact_two_sided(b: int, c: int) -> float:
    """Exact two-sided McNemar (binomial sign test on discordant pairs)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1))
    return min(1.0, 2.0 * tail / (2.0 ** n))


def wilson95(successes: int, total: int) -> tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    z = 1.959963984540054
    p = successes / total
    d = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / d
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def paired_wald_ci(diffs: list[int]) -> tuple[float, float]:
    """95% Wald interval for the mean of per-unit paired differences in {-1,0,1}."""
    n = len(diffs)
    if n == 0:
        return (0.0, 0.0)
    mean = sum(diffs) / n
    var = sum((d - mean) ** 2 for d in diffs) / (n - 1) if n > 1 else 0.0
    se = math.sqrt(var / n)
    return (mean - 1.959963984540054 * se, mean + 1.959963984540054 * se)


def cluster_bootstrap_ci(clusters: list[tuple[int, int]], reps: int = 10000,
                         seed: int = 20260902) -> tuple[float, float]:
    """95% CI for a difference of rates when observations are clustered by campaign.

    ``clusters`` is a list of ``(m_successes, b_successes)`` ... supplied as per-campaign
    (numerator_difference, denominator) pairs; resampling is over campaigns, which is the
    unit of independence in this study.  Rung-level decisions inside a campaign share a
    budget and a trajectory and are emphatically not independent, so a rung-level interval
    that ignored clustering would be too narrow.
    """
    import random

    if not clusters:
        return (0.0, 0.0)
    rng = random.Random(seed)
    n = len(clusters)
    stats = []
    for _ in range(reps):
        num = 0
        den = 0
        for _ in range(n):
            a, b = clusters[rng.randrange(n)]
            num += a
            den += b
        stats.append(num / den if den else 0.0)
    stats.sort()
    return (stats[int(0.025 * reps)], stats[int(0.975 * reps)])
