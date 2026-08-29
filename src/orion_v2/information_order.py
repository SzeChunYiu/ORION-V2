from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Hashable, Mapping

State = Hashable
Signal = Hashable
Action = Hashable
Distribution = Mapping[Hashable, float]


def _validate_distribution(distribution: Distribution) -> None:
    if not distribution:
        raise ValueError("distribution must be non-empty")
    if any(value < 0 for value in distribution.values()):
        raise ValueError("distribution weights must be non-negative")
    if abs(sum(distribution.values()) - 1.0) > 1e-9:
        raise ValueError("distribution weights must sum to one")


class ExperimentComparison(str, Enum):
    EQUIVALENT = "EQUIVALENT"
    LEFT_BLACKWELL_DOMINATES = "LEFT_BLACKWELL_DOMINATES"
    RIGHT_BLACKWELL_DOMINATES = "RIGHT_BLACKWELL_DOMINATES"
    DECISION_EQUIVALENT_ON_REGISTERED_TASKS = (
        "DECISION_EQUIVALENT_ON_REGISTERED_TASKS"
    )
    INCOMPARABLE_ON_REGISTERED_TASKS = "INCOMPARABLE_ON_REGISTERED_TASKS"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class FiniteExperiment:
    experiment_id: str
    states: tuple[State, ...]
    signals: tuple[Signal, ...]
    kernel: Mapping[State, Mapping[Signal, float]]

    def __post_init__(self) -> None:
        if not self.experiment_id.strip() or not self.states or not self.signals:
            raise ValueError("experiment identity, states and signals are required")
        if set(self.kernel) != set(self.states):
            raise ValueError("kernel must define every state")
        for distribution in self.kernel.values():
            if set(distribution) != set(self.signals):
                raise ValueError(
                    "kernel distributions must use the declared signal set"
                )
            _validate_distribution(distribution)


@dataclass(frozen=True, slots=True)
class DecisionProblem:
    problem_id: str
    states: tuple[State, ...]
    actions: tuple[Action, ...]
    prior: Mapping[State, float]
    utility: Mapping[tuple[State, Action], float]

    def __post_init__(self) -> None:
        if not self.problem_id.strip() or not self.actions:
            raise ValueError("decision problem identity and actions are required")
        if set(self.prior) != set(self.states):
            raise ValueError("prior must cover the declared states")
        _validate_distribution(self.prior)
        if set(self.utility) != {
            (state, action) for state in self.states for action in self.actions
        }:
            raise ValueError("utility table must cover every state-action pair")


def decision_value(experiment: FiniteExperiment, problem: DecisionProblem) -> float:
    if set(experiment.states) != set(problem.states):
        raise ValueError(
            "experiment and decision problem must share the state set"
        )
    best = float("-inf")
    for chosen_actions in product(
        problem.actions, repeat=len(experiment.signals)
    ):
        rule = dict(zip(experiment.signals, chosen_actions, strict=True))
        value = 0.0
        for state in problem.states:
            for signal in experiment.signals:
                value += (
                    problem.prior[state]
                    * experiment.kernel[state][signal]
                    * problem.utility[(state, rule[signal])]
                )
        best = max(best, value)
    return best


def validates_garbling(
    source: FiniteExperiment,
    target: FiniteExperiment,
    garbling: Mapping[Signal, Mapping[Signal, float]],
    *,
    tolerance: float = 1e-9,
) -> bool:
    if set(source.states) != set(target.states) or set(garbling) != set(
        source.signals
    ):
        return False
    for distribution in garbling.values():
        if set(distribution) != set(target.signals):
            return False
        try:
            _validate_distribution(distribution)
        except ValueError:
            return False
    for state in source.states:
        for target_signal in target.signals:
            induced = sum(
                source.kernel[state][source_signal]
                * garbling[source_signal][target_signal]
                for source_signal in source.signals
            )
            if abs(induced - target.kernel[state][target_signal]) > tolerance:
                return False
    return True


def compare_experiments(
    left: FiniteExperiment,
    right: FiniteExperiment,
    *,
    left_to_right_garbling: Mapping[Signal, Mapping[Signal, float]] | None = None,
    right_to_left_garbling: Mapping[Signal, Mapping[Signal, float]] | None = None,
    registered_problems: tuple[DecisionProblem, ...] = (),
    tolerance: float = 1e-9,
) -> ExperimentComparison:
    if set(left.states) != set(right.states):
        return ExperimentComparison.CANNOT_CHECK
    left_dominates = (
        left_to_right_garbling is not None
        and validates_garbling(
            left, right, left_to_right_garbling, tolerance=tolerance
        )
    )
    right_dominates = (
        right_to_left_garbling is not None
        and validates_garbling(
            right, left, right_to_left_garbling, tolerance=tolerance
        )
    )
    if left_dominates and right_dominates:
        return ExperimentComparison.EQUIVALENT
    if left_dominates:
        return ExperimentComparison.LEFT_BLACKWELL_DOMINATES
    if right_dominates:
        return ExperimentComparison.RIGHT_BLACKWELL_DOMINATES
    if not registered_problems:
        return ExperimentComparison.CANNOT_CHECK
    deltas = [
        decision_value(left, problem) - decision_value(right, problem)
        for problem in registered_problems
    ]
    if all(abs(delta) <= tolerance for delta in deltas):
        return ExperimentComparison.DECISION_EQUIVALENT_ON_REGISTERED_TASKS
    return ExperimentComparison.INCOMPARABLE_ON_REGISTERED_TASKS
