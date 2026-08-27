from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Hashable, Mapping

Outcome = Hashable
Distribution = Mapping[Outcome, float]


def _validate_distribution(distribution: Distribution) -> None:
    if not distribution or any(value < 0 for value in distribution.values()):
        raise ValueError(
            "response distributions must be non-empty and non-negative"
        )
    if abs(sum(distribution.values()) - 1.0) > 1e-9:
        raise ValueError("response distributions must sum to one")


class PerformativeDynamicsStatus(str, Enum):
    NO_MATERIAL_RESPONSE = "NO_MATERIAL_RESPONSE"
    STATIC_AND_PERFORMATIVE_OPTIMA_AGREE = (
        "STATIC_AND_PERFORMATIVE_OPTIMA_AGREE"
    )
    POLICY_WINNER_REVERSAL = "POLICY_WINNER_REVERSAL"
    RETRAINING_CONVERGES = "RETRAINING_CONVERGES"
    RETRAINING_CYCLE = "RETRAINING_CYCLE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class FinitePerformativeSystem:
    system_id: str
    policies: tuple[str, ...]
    outcomes: tuple[Outcome, ...]
    response_by_policy: Mapping[str, Distribution]
    loss: Mapping[tuple[str, Outcome], float]

    def __post_init__(self) -> None:
        if not self.system_id.strip() or not self.policies or not self.outcomes:
            raise ValueError(
                "performative system identity, policies and outcomes are required"
            )
        if set(self.response_by_policy) != set(self.policies):
            raise ValueError("every policy requires a response distribution")
        for distribution in self.response_by_policy.values():
            if set(distribution) != set(self.outcomes):
                raise ValueError(
                    "response distributions must cover declared outcomes"
                )
            _validate_distribution(distribution)
        if set(self.loss) != {
            (policy, outcome)
            for policy in self.policies
            for outcome in self.outcomes
        }:
            raise ValueError(
                "loss table must cover every policy-outcome pair"
            )


def risk(
    system: FinitePerformativeSystem,
    policy: str,
    distribution: Distribution,
) -> float:
    return sum(
        distribution[outcome] * system.loss[(policy, outcome)]
        for outcome in system.outcomes
    )


def _argmin_policies(
    system: FinitePerformativeSystem, distribution: Distribution
) -> tuple[str, ...]:
    values = {
        policy: risk(system, policy, distribution) for policy in system.policies
    }
    minimum = min(values.values())
    return tuple(
        sorted(
            policy
            for policy, value in values.items()
            if abs(value - minimum) <= 1e-12
        )
    )


def static_optima(
    system: FinitePerformativeSystem, baseline_distribution: Distribution
) -> tuple[str, ...]:
    _validate_distribution(baseline_distribution)
    if set(baseline_distribution) != set(system.outcomes):
        raise ValueError("baseline distribution must cover the outcome set")
    return _argmin_policies(system, baseline_distribution)


def performative_optima(system: FinitePerformativeSystem) -> tuple[str, ...]:
    values = {
        policy: risk(system, policy, system.response_by_policy[policy])
        for policy in system.policies
    }
    minimum = min(values.values())
    return tuple(
        sorted(
            policy
            for policy, value in values.items()
            if abs(value - minimum) <= 1e-12
        )
    )


def stable_policies(system: FinitePerformativeSystem) -> tuple[str, ...]:
    return tuple(
        policy
        for policy in sorted(system.policies)
        if policy
        in _argmin_policies(system, system.response_by_policy[policy])
    )


def retraining_trajectory(
    system: FinitePerformativeSystem,
    start_policy: str,
    *,
    max_steps: int = 50,
) -> tuple[tuple[str, ...], PerformativeDynamicsStatus]:
    if start_policy not in system.policies or max_steps < 1:
        return (), PerformativeDynamicsStatus.CANNOT_CHECK
    path: list[str] = []
    seen_at: dict[str, int] = {}
    current = start_policy
    for _ in range(max_steps):
        if current in seen_at:
            cycle = tuple(path[seen_at[current] :] + [current])
            if len(cycle) == 2:
                return (
                    tuple(path + [current]),
                    PerformativeDynamicsStatus.RETRAINING_CONVERGES,
                )
            return (
                tuple(path + [current]),
                PerformativeDynamicsStatus.RETRAINING_CYCLE,
            )
        seen_at[current] = len(path)
        path.append(current)
        current = _argmin_policies(
            system, system.response_by_policy[current]
        )[0]
    return tuple(path), PerformativeDynamicsStatus.CANNOT_CHECK


def assess_performative_dynamics(
    system: FinitePerformativeSystem,
    baseline_distribution: Distribution,
) -> PerformativeDynamicsStatus:
    responses = list(system.response_by_policy.values())
    if all(response == responses[0] for response in responses[1:]):
        return PerformativeDynamicsStatus.NO_MATERIAL_RESPONSE
    return (
        PerformativeDynamicsStatus.STATIC_AND_PERFORMATIVE_OPTIMA_AGREE
        if set(static_optima(system, baseline_distribution))
        == set(performative_optima(system))
        else PerformativeDynamicsStatus.POLICY_WINNER_REVERSAL
    )
