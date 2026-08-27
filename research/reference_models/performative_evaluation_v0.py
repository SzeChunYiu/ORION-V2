"""Performative scientific-evaluation reference model V0.

The functions expose a minimal distinction between evaluating a policy under a
fixed baseline distribution and evaluating it under the distribution induced by
its deployment. They are not a general strategic-behaviour model.
"""

from __future__ import annotations

from typing import Mapping, Sequence


class PerformativeInputError(ValueError):
    pass


def _validate_distribution(values: Sequence[float]) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if not result or any(value < 0 for value in result):
        raise PerformativeInputError("distribution must be non-empty and non-negative")
    if abs(sum(result) - 1.0) > 1e-12:
        raise PerformativeInputError("distribution must sum to one")
    return result


def expected_loss(distribution: Sequence[float], losses: Sequence[float]) -> float:
    probabilities = _validate_distribution(distribution)
    losses_tuple = tuple(float(value) for value in losses)
    if len(probabilities) != len(losses_tuple):
        raise PerformativeInputError("losses must align with outcomes")
    return sum(probability * loss for probability, loss in zip(probabilities, losses_tuple, strict=True))


def total_variation(left: Sequence[float], right: Sequence[float]) -> float:
    left_values = _validate_distribution(left)
    right_values = _validate_distribution(right)
    if len(left_values) != len(right_values):
        raise PerformativeInputError("distributions must have equal support")
    return 0.5 * sum(abs(a - b) for a, b in zip(left_values, right_values, strict=True))


def best_policy_static(
    baseline_distribution: Sequence[float], policies: Mapping[str, Mapping[str, Sequence[float]]]
) -> str:
    if not policies:
        raise PerformativeInputError("at least one policy is required")
    scored = [
        (expected_loss(baseline_distribution, policy["losses"]), policy_id)
        for policy_id, policy in policies.items()
    ]
    return min(scored)[1]


def best_policy_performative(
    policies: Mapping[str, Mapping[str, Sequence[float]]]
) -> str:
    if not policies:
        raise PerformativeInputError("at least one policy is required")
    scored = [
        (
            expected_loss(policy["induced_distribution"], policy["losses"]),
            policy_id,
        )
        for policy_id, policy in policies.items()
    ]
    return min(scored)[1]


def static_evaluation_transportable(
    baseline_distribution: Sequence[float],
    induced_distribution: Sequence[float],
    *,
    tolerance: float,
) -> bool:
    if tolerance < 0:
        raise PerformativeInputError("tolerance must be non-negative")
    return total_variation(baseline_distribution, induced_distribution) <= tolerance


__all__ = [
    "PerformativeInputError",
    "best_policy_performative",
    "best_policy_static",
    "expected_loss",
    "static_evaluation_transportable",
    "total_variation",
]
