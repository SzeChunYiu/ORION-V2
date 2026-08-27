from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Hashable, Mapping

State = Hashable
Distribution = Mapping[State, float]


def _validate_distribution(
    distribution: Distribution, states: frozenset[State]
) -> None:
    if set(distribution) != set(states):
        raise ValueError("distribution must cover exactly the declared states")
    if any(value < 0 for value in distribution.values()):
        raise ValueError("probabilities must be non-negative")
    if abs(sum(distribution.values()) - 1.0) > 1e-9:
        raise ValueError("probabilities must sum to one")


def total_variation(left: Distribution, right: Distribution) -> float:
    if set(left) != set(right):
        raise ValueError("total variation requires a common support")
    return 0.5 * sum(abs(left[item] - right[item]) for item in left)


class StochasticTransportStatus(str, Enum):
    EXACT_STOCHASTIC_TRANSPORT = "EXACT_STOCHASTIC_TRANSPORT"
    EPSILON_BOUNDED_STOCHASTIC_TRANSPORT = (
        "EPSILON_BOUNDED_STOCHASTIC_TRANSPORT"
    )
    INVALID_TRANSITION_ERROR = "INVALID_TRANSITION_ERROR"
    INVALID_OBSERVABLE_ERROR = "INVALID_OBSERVABLE_ERROR"
    CANNOT_CHECK = "CANNOT_CHECK"


class DecisionRobustnessStatus(str, Enum):
    DECISION_PRESERVED_BY_MARGIN = "DECISION_PRESERVED_BY_MARGIN"
    DECISION_NOT_CERTIFIED_MARGIN_TOO_SMALL = (
        "DECISION_NOT_CERTIFIED_MARGIN_TOO_SMALL"
    )
    DECISION_CHANGED = "DECISION_CHANGED"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class FiniteStochasticTheory:
    theory_id: str
    states: frozenset[State]
    actions: frozenset[str]
    transition_kernel: Mapping[tuple[State, str], Distribution]
    observables: Mapping[str, Mapping[State, float]]
    epoch: str

    def __post_init__(self) -> None:
        if not self.theory_id.strip() or not self.states or not self.actions:
            raise ValueError("theory identity, states and actions are required")
        if not self.epoch.strip():
            raise ValueError("theory epoch is required")
        expected = {(state, action) for state in self.states for action in self.actions}
        if set(self.transition_kernel) != expected:
            raise ValueError("transition kernel must define every state-action pair")
        for distribution in self.transition_kernel.values():
            _validate_distribution(distribution, self.states)
        for table in self.observables.values():
            if set(table) != set(self.states):
                raise ValueError("every observable must cover every state")


@dataclass(frozen=True, slots=True)
class StochasticTransport:
    transport_id: str
    state_map: Mapping[State, State]
    action_map: Mapping[str, str]
    registered_observable_ids: tuple[str, ...]
    transition_epsilon: float
    observable_epsilon: float
    source_epoch: str
    target_epoch: str
    authority_ceiling: int

    def __post_init__(self) -> None:
        if not self.transport_id.strip():
            raise ValueError("transport identity is required")
        if not 0 <= self.transition_epsilon <= 1:
            raise ValueError("transition epsilon must lie in [0,1]")
        if self.observable_epsilon < 0 or self.authority_ceiling < 0:
            raise ValueError("observable epsilon and authority ceiling must be non-negative")


@dataclass(frozen=True, slots=True)
class StochasticTransportAssessment:
    status: StochasticTransportStatus
    observed_transition_error: float | None
    observed_observable_error: float | None
    authority_ceiling: int
    warnings: tuple[str, ...] = ()
    grants_scientific_truth: bool = False
    grants_novelty: bool = False
    grants_target_adoption: bool = False

    def __post_init__(self) -> None:
        if self.grants_scientific_truth or self.grants_novelty or self.grants_target_adoption:
            raise ValueError("stochastic transport assessment is non-authorizing")


def _pushforward(
    distribution: Distribution,
    state_map: Mapping[State, State],
    target_states: frozenset[State],
) -> dict[State, float]:
    result = {state: 0.0 for state in target_states}
    for source_state, probability in distribution.items():
        result[state_map[source_state]] += probability
    return result


def assess_stochastic_transport(
    source: FiniteStochasticTheory,
    target: FiniteStochasticTheory,
    transport: StochasticTransport,
    *,
    tolerance: float = 1e-12,
) -> StochasticTransportAssessment:
    if (
        set(transport.state_map) != set(source.states)
        or set(transport.action_map) != set(source.actions)
        or any(state not in target.states for state in transport.state_map.values())
        or any(action not in target.actions for action in transport.action_map.values())
        or not transport.source_epoch.strip()
        or not transport.target_epoch.strip()
    ):
        return StochasticTransportAssessment(
            StochasticTransportStatus.CANNOT_CHECK, None, None, transport.authority_ceiling
        )
    transition_error = 0.0
    for source_state in source.states:
        for source_action in source.actions:
            pushed = _pushforward(
                source.transition_kernel[(source_state, source_action)],
                transport.state_map,
                target.states,
            )
            target_distribution = target.transition_kernel[
                (transport.state_map[source_state], transport.action_map[source_action])
            ]
            transition_error = max(
                transition_error, total_variation(pushed, target_distribution)
            )
    observable_error = 0.0
    for observable_id in transport.registered_observable_ids:
        if observable_id not in source.observables or observable_id not in target.observables:
            return StochasticTransportAssessment(
                StochasticTransportStatus.CANNOT_CHECK,
                transition_error,
                None,
                transport.authority_ceiling,
                (f"observable {observable_id} is not defined on both theories",),
            )
        for source_state in source.states:
            observable_error = max(
                observable_error,
                abs(
                    source.observables[observable_id][source_state]
                    - target.observables[observable_id][transport.state_map[source_state]]
                ),
            )
    if transition_error > transport.transition_epsilon + tolerance:
        return StochasticTransportAssessment(
            StochasticTransportStatus.INVALID_TRANSITION_ERROR,
            transition_error,
            observable_error,
            transport.authority_ceiling,
        )
    if observable_error > transport.observable_epsilon + tolerance:
        return StochasticTransportAssessment(
            StochasticTransportStatus.INVALID_OBSERVABLE_ERROR,
            transition_error,
            observable_error,
            transport.authority_ceiling,
        )
    exact = transition_error <= tolerance and observable_error <= tolerance
    return StochasticTransportAssessment(
        StochasticTransportStatus.EXACT_STOCHASTIC_TRANSPORT
        if exact
        else StochasticTransportStatus.EPSILON_BOUNDED_STOCHASTIC_TRANSPORT,
        transition_error,
        observable_error,
        transport.authority_ceiling,
    )


@dataclass(frozen=True, slots=True)
class DecisionRobustnessAssessment:
    status: DecisionRobustnessStatus
    nominal_best_action_ids: tuple[str, ...]
    observed_best_action_ids: tuple[str, ...]
    nominal_margin: float | None
    error_bound: float


def _best_actions(values: Mapping[str, float]) -> tuple[str, ...]:
    if not values:
        return ()
    best = max(values.values())
    return tuple(sorted(action for action, value in values.items() if abs(value - best) <= 1e-12))


def assess_decision_robustness(
    nominal_values: Mapping[str, float],
    *,
    error_bound: float,
    observed_values: Mapping[str, float] | None = None,
) -> DecisionRobustnessAssessment:
    if error_bound < 0 or not nominal_values:
        return DecisionRobustnessAssessment(
            DecisionRobustnessStatus.CANNOT_CHECK, (), (), None, error_bound
        )
    nominal_best = _best_actions(nominal_values)
    observed_best = _best_actions(observed_values) if observed_values is not None else ()
    if observed_values is not None and set(observed_values) != set(nominal_values):
        return DecisionRobustnessAssessment(
            DecisionRobustnessStatus.CANNOT_CHECK,
            nominal_best,
            observed_best,
            None,
            error_bound,
        )
    if observed_values is not None and set(nominal_best) != set(observed_best):
        return DecisionRobustnessAssessment(
            DecisionRobustnessStatus.DECISION_CHANGED,
            nominal_best,
            observed_best,
            None,
            error_bound,
        )
    ordered = sorted(nominal_values.values(), reverse=True)
    margin = None if len(ordered) < 2 or len(nominal_best) != 1 else ordered[0] - ordered[1]
    if margin is not None and margin > 2 * error_bound:
        return DecisionRobustnessAssessment(
            DecisionRobustnessStatus.DECISION_PRESERVED_BY_MARGIN,
            nominal_best,
            observed_best,
            margin,
            error_bound,
        )
    return DecisionRobustnessAssessment(
        DecisionRobustnessStatus.DECISION_NOT_CERTIFIED_MARGIN_TOO_SMALL,
        nominal_best,
        observed_best,
        margin,
        error_bound,
    )


@dataclass(frozen=True, slots=True)
class StochasticTransportLink:
    link_id: str
    transition_error_bound: float
    observable_error_bound: float
    authority_ceiling: int
    unresolved_assumption_ids: tuple[str, ...] = ()
    dependence_declared: bool = True

    def __post_init__(self) -> None:
        if not self.link_id.strip():
            raise ValueError("link identity is required")
        if not 0 <= self.transition_error_bound <= 1:
            raise ValueError("transition error bound must lie in [0,1]")
        if self.observable_error_bound < 0 or self.authority_ceiling < 0:
            raise ValueError("observable error and authority must be non-negative")


@dataclass(frozen=True, slots=True)
class StochasticChainBound:
    transition_error_bound: float | None
    observable_error_bound: float | None
    authority_ceiling: int | None
    unresolved_assumption_ids: tuple[str, ...]
    exact: bool
    cannot_check: bool


def compose_stochastic_transport_bounds(
    links: tuple[StochasticTransportLink, ...],
) -> StochasticChainBound:
    if not links or any(not link.dependence_declared for link in links):
        return StochasticChainBound(None, None, None, (), False, True)
    transition = min(1.0, sum(link.transition_error_bound for link in links))
    observable = sum(link.observable_error_bound for link in links)
    assumptions = tuple(
        sorted({item for link in links for item in link.unresolved_assumption_ids})
    )
    authority = min(link.authority_ceiling for link in links)
    return StochasticChainBound(
        transition,
        observable,
        authority,
        assumptions,
        transition == 0 and observable == 0 and not assumptions,
        False,
    )
