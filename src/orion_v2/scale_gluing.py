from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Hashable, Mapping

Value = Hashable
State = Hashable


class GluingStatus(str, Enum):
    GLOBAL_SECTION_EXISTS = "GLOBAL_SECTION_EXISTS"
    GLOBAL_OBSTRUCTION = "GLOBAL_OBSTRUCTION"
    LOCAL_CONTEXT_EMPTY = "LOCAL_CONTEXT_EMPTY"
    CANNOT_CHECK = "CANNOT_CHECK"


class ScaleStatus(str, Enum):
    EXACT_SCALE_EQUIVALENCE = "EXACT_SCALE_EQUIVALENCE"
    SAFE_FOR_REGISTERED_TARGETS = "SAFE_FOR_REGISTERED_TARGETS"
    SAFE_CURRENT_FUTURE_UNSAFE = "SAFE_CURRENT_FUTURE_UNSAFE"
    INVALID_OBSERVABLE_DRIFT = "INVALID_OBSERVABLE_DRIFT"
    INVALID_TRANSITION_DRIFT = "INVALID_TRANSITION_DRIFT"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class ContextualModel:
    model_id: str
    variables: tuple[str, ...]
    value_domains: Mapping[str, tuple[Value, ...]]
    contexts: Mapping[str, tuple[str, ...]]
    allowed_assignments: Mapping[str, frozenset[tuple[Value, ...]]]

    def __post_init__(self) -> None:
        if not self.model_id.strip() or not self.variables:
            raise ValueError(
                "contextual model identity and variables are required"
            )
        if set(self.value_domains) != set(self.variables):
            raise ValueError("every variable requires a value domain")
        if set(self.contexts) != set(self.allowed_assignments):
            raise ValueError(
                "contexts and assignment tables must share identities"
            )
        for context_id, variables in self.contexts.items():
            if not variables or not set(variables) <= set(self.variables):
                raise ValueError(f"invalid context {context_id}")
            for assignment in self.allowed_assignments[context_id]:
                if len(assignment) != len(variables):
                    raise ValueError("assignment arity must match context")
                for variable, value in zip(
                    variables, assignment, strict=True
                ):
                    if value not in self.value_domains[variable]:
                        raise ValueError("assignment uses an undeclared value")


def global_sections(
    model: ContextualModel,
) -> tuple[Mapping[str, Value], ...]:
    if any(
        not assignments for assignments in model.allowed_assignments.values()
    ):
        return ()
    sections: list[Mapping[str, Value]] = []
    domains = [model.value_domains[variable] for variable in model.variables]
    for values in product(*domains):
        candidate = dict(zip(model.variables, values, strict=True))
        valid = True
        for context_id, variables in model.contexts.items():
            restricted = tuple(candidate[variable] for variable in variables)
            if restricted not in model.allowed_assignments[context_id]:
                valid = False
                break
        if valid:
            sections.append(candidate)
    return tuple(sections)


def assess_gluing(model: ContextualModel) -> GluingStatus:
    if any(
        not assignments for assignments in model.allowed_assignments.values()
    ):
        return GluingStatus.LOCAL_CONTEXT_EMPTY
    return (
        GluingStatus.GLOBAL_SECTION_EXISTS
        if global_sections(model)
        else GluingStatus.GLOBAL_OBSTRUCTION
    )


@dataclass(frozen=True, slots=True)
class FiniteScaleModel:
    model_id: str
    states: frozenset[State]
    actions: frozenset[str]
    transitions: frozenset[tuple[State, str, State]]
    observables: Mapping[str, Mapping[State, Value]]

    def __post_init__(self) -> None:
        if not self.model_id.strip() or not self.states:
            raise ValueError("scale model identity and states are required")
        for source, action, target in self.transitions:
            if (
                source not in self.states
                or target not in self.states
                or action not in self.actions
            ):
                raise ValueError("transition uses undeclared state or action")
        for table in self.observables.values():
            if set(table) != set(self.states):
                raise ValueError("observables must cover every state")


@dataclass(frozen=True, slots=True)
class ScaleMap:
    map_id: str
    state_map: Mapping[State, State]
    action_map: Mapping[str, str]
    registered_observable_ids: tuple[str, ...]
    future_observable_ids: tuple[str, ...] = ()


def assess_scale_map(
    micro: FiniteScaleModel,
    macro: FiniteScaleModel,
    mapping: ScaleMap,
) -> ScaleStatus:
    if set(mapping.state_map) != set(micro.states) or set(
        mapping.action_map
    ) != set(micro.actions):
        return ScaleStatus.CANNOT_CHECK
    if any(value not in macro.states for value in mapping.state_map.values()):
        return ScaleStatus.CANNOT_CHECK
    if any(value not in macro.actions for value in mapping.action_map.values()):
        return ScaleStatus.CANNOT_CHECK
    for observable_id in mapping.registered_observable_ids:
        if (
            observable_id not in micro.observables
            or observable_id not in macro.observables
        ):
            return ScaleStatus.CANNOT_CHECK
        for state in micro.states:
            if (
                micro.observables[observable_id][state]
                != macro.observables[observable_id][mapping.state_map[state]]
            ):
                return ScaleStatus.INVALID_OBSERVABLE_DRIFT
    macro_transitions = set(macro.transitions)
    for source, action, target in micro.transitions:
        mapped = (
            mapping.state_map[source],
            mapping.action_map[action],
            mapping.state_map[target],
        )
        if mapped not in macro_transitions:
            return ScaleStatus.INVALID_TRANSITION_DRIFT
    future_safe = True
    for observable_id in mapping.future_observable_ids:
        if (
            observable_id not in micro.observables
            or observable_id not in macro.observables
        ):
            future_safe = False
            break
        if any(
            micro.observables[observable_id][state]
            != macro.observables[observable_id][mapping.state_map[state]]
            for state in micro.states
        ):
            future_safe = False
            break
    if not future_safe:
        return ScaleStatus.SAFE_CURRENT_FUTURE_UNSAFE
    bijective = (
        set(mapping.state_map.values()) == set(macro.states)
        and len(set(mapping.state_map.values())) == len(micro.states)
    )
    return (
        ScaleStatus.EXACT_SCALE_EQUIVALENCE
        if bijective
        else ScaleStatus.SAFE_FOR_REGISTERED_TARGETS
    )
