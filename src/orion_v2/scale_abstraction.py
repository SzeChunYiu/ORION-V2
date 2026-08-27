from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Hashable, Mapping

State = Hashable
QueryValue = Hashable


class ScaleAbstractionStatus(str, Enum):
    EXACT_SCALE_EQUIVALENCE = "EXACT_SCALE_EQUIVALENCE"
    CONTEXT_SAFE_ABSTRACTION = "CONTEXT_SAFE_ABSTRACTION"
    OBSERVATION_SAFE_INTERVENTION_UNSAFE = "OBSERVATION_SAFE_INTERVENTION_UNSAFE"
    INVALID_OBSERVABLE = "INVALID_OBSERVABLE"
    INVALID_INTERVENTION = "INVALID_INTERVENTION"
    UNDECLARED_INFORMATION_LOSS = "UNDECLARED_INFORMATION_LOSS"
    FUTURE_QUERY_UNSAFE = "FUTURE_QUERY_UNSAFE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class ScaleContext:
    context_id: str
    registered_observable_ids: tuple[str, ...]
    registered_intervention_ids: tuple[str, ...] = ()
    allowed_lost_query_ids: tuple[str, ...] = ()
    future_query_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.context_id.strip():
            raise ValueError("scale context identity must be non-blank")
        for field_name, values in (
            ("observable", self.registered_observable_ids),
            ("intervention", self.registered_intervention_ids),
            ("allowed lost query", self.allowed_lost_query_ids),
            ("future query", self.future_query_ids),
        ):
            if any(not item.strip() for item in values):
                raise ValueError(f"{field_name} ids may not be blank")
            if len(values) != len(set(values)):
                raise ValueError(f"{field_name} ids must be unique")
        if not self.registered_observable_ids:
            raise ValueError("a scale context requires at least one observable")
        if set(self.future_query_ids) & set(self.allowed_lost_query_ids):
            raise ValueError("future queries cannot simultaneously be declared allowed loss")


@dataclass(frozen=True, slots=True)
class ScaleIndexedAbstraction:
    abstraction_id: str
    micro_scale_id: str
    macro_scale_id: str
    micro_states: frozenset[State]
    macro_states: frozenset[State]
    abstraction_map: Mapping[State, State]
    micro_observables: Mapping[str, Mapping[State, float]]
    macro_observables: Mapping[str, Mapping[State, float]]
    observable_tolerances: Mapping[str, float]
    micro_interventions: Mapping[str, Mapping[State, State]]
    macro_interventions: Mapping[str, Mapping[State, State]]
    micro_queries: Mapping[str, Mapping[State, QueryValue]]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("abstraction id", self.abstraction_id),
            ("micro scale id", self.micro_scale_id),
            ("macro scale id", self.macro_scale_id),
        ):
            if not value.strip():
                raise ValueError(f"{field_name} must be non-blank")
        if not self.micro_states or not self.macro_states:
            raise ValueError("scale abstractions require micro and macro states")
        if set(self.abstraction_map) != set(self.micro_states):
            raise ValueError("abstraction map must cover every micro state")
        if any(value not in self.macro_states for value in self.abstraction_map.values()):
            raise ValueError("abstraction map reaches an undeclared macro state")
        if set(self.micro_observables) != set(self.macro_observables):
            raise ValueError("micro and macro observable identities must agree")
        if set(self.observable_tolerances) != set(self.micro_observables):
            raise ValueError("every observable requires a tolerance")
        if any(value < 0 for value in self.observable_tolerances.values()):
            raise ValueError("observable tolerances must be non-negative")
        for table in self.micro_observables.values():
            if set(table) != set(self.micro_states):
                raise ValueError("micro observables must cover every micro state")
        for table in self.macro_observables.values():
            if set(table) != set(self.macro_states):
                raise ValueError("macro observables must cover every macro state")
        if set(self.micro_interventions) != set(self.macro_interventions):
            raise ValueError("micro and macro intervention identities must agree")
        for table in self.micro_interventions.values():
            if set(table) != set(self.micro_states) or any(
                value not in self.micro_states for value in table.values()
            ):
                raise ValueError("micro interventions must be total endomaps")
        for table in self.macro_interventions.values():
            if set(table) != set(self.macro_states) or any(
                value not in self.macro_states for value in table.values()
            ):
                raise ValueError("macro interventions must be total endomaps")
        for query_id, table in self.micro_queries.items():
            if not query_id.strip() or set(table) != set(self.micro_states):
                raise ValueError("micro queries must be named and total")


@dataclass(frozen=True, slots=True)
class ScaleAbstractionAssessment:
    abstraction_id: str
    status: ScaleAbstractionStatus
    observation_errors: tuple[tuple[str, State, float], ...]
    intervention_mismatches: tuple[tuple[str, State], ...]
    collapsed_query_ids: tuple[str, ...]
    violations: tuple[str, ...]
    authority_granted: bool = False
    scientific_equivalence_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("scale assessment cannot grant authority")
        if (
            self.scientific_equivalence_granted
            and self.status is not ScaleAbstractionStatus.EXACT_SCALE_EQUIVALENCE
        ):
            raise ValueError("only exact scale equivalence may carry equivalence flag")


def assess_scale_abstraction(
    abstraction: ScaleIndexedAbstraction,
    context: ScaleContext,
) -> ScaleAbstractionAssessment:
    if not set(context.registered_observable_ids) <= set(abstraction.micro_observables):
        return ScaleAbstractionAssessment(
            abstraction.abstraction_id,
            ScaleAbstractionStatus.CANNOT_CHECK,
            (),
            (),
            (),
            ("context registers undeclared observables",),
        )
    if not set(context.registered_intervention_ids) <= set(
        abstraction.micro_interventions
    ):
        return ScaleAbstractionAssessment(
            abstraction.abstraction_id,
            ScaleAbstractionStatus.CANNOT_CHECK,
            (),
            (),
            (),
            ("context registers undeclared interventions",),
        )
    if not set(context.future_query_ids) <= set(abstraction.micro_queries):
        return ScaleAbstractionAssessment(
            abstraction.abstraction_id,
            ScaleAbstractionStatus.CANNOT_CHECK,
            (),
            (),
            (),
            ("context registers undeclared future queries",),
        )

    observation_errors: list[tuple[str, State, float]] = []
    for observable_id in context.registered_observable_ids:
        micro_table = abstraction.micro_observables[observable_id]
        macro_table = abstraction.macro_observables[observable_id]
        tolerance = abstraction.observable_tolerances[observable_id]
        for micro_state in abstraction.micro_states:
            macro_state = abstraction.abstraction_map[micro_state]
            error = abs(micro_table[micro_state] - macro_table[macro_state])
            if error > tolerance:
                observation_errors.append((observable_id, micro_state, error))
    if observation_errors:
        return ScaleAbstractionAssessment(
            abstraction.abstraction_id,
            ScaleAbstractionStatus.INVALID_OBSERVABLE,
            tuple(observation_errors),
            (),
            (),
            ("registered observables do not commute within tolerance",),
        )

    intervention_mismatches: list[tuple[str, State]] = []
    for intervention_id in context.registered_intervention_ids:
        micro_map = abstraction.micro_interventions[intervention_id]
        macro_map = abstraction.macro_interventions[intervention_id]
        for micro_state in abstraction.micro_states:
            left = abstraction.abstraction_map[micro_map[micro_state]]
            right = macro_map[abstraction.abstraction_map[micro_state]]
            if left != right:
                intervention_mismatches.append((intervention_id, micro_state))
    if intervention_mismatches:
        return ScaleAbstractionAssessment(
            abstraction.abstraction_id,
            ScaleAbstractionStatus.OBSERVATION_SAFE_INTERVENTION_UNSAFE,
            (),
            tuple(intervention_mismatches),
            (),
            ("registered interventions do not commute with abstraction",),
        )

    fibres: dict[State, list[State]] = {}
    for micro_state, macro_state in abstraction.abstraction_map.items():
        fibres.setdefault(macro_state, []).append(micro_state)
    collapsed_queries: set[str] = set()
    for group in fibres.values():
        for left, right in combinations(group, 2):
            for query_id, table in abstraction.micro_queries.items():
                if table[left] != table[right]:
                    collapsed_queries.add(query_id)

    undeclared = collapsed_queries - set(context.allowed_lost_query_ids) - set(
        context.future_query_ids
    )
    if undeclared:
        return ScaleAbstractionAssessment(
            abstraction.abstraction_id,
            ScaleAbstractionStatus.UNDECLARED_INFORMATION_LOSS,
            (),
            (),
            tuple(sorted(collapsed_queries)),
            (
                "collapsed queries were not declared lost: "
                + ", ".join(sorted(undeclared)),
            ),
        )
    future_unsafe = collapsed_queries & set(context.future_query_ids)
    if future_unsafe:
        return ScaleAbstractionAssessment(
            abstraction.abstraction_id,
            ScaleAbstractionStatus.FUTURE_QUERY_UNSAFE,
            (),
            (),
            tuple(sorted(collapsed_queries)),
            (
                "future queries are not determined at the macro scale: "
                + ", ".join(sorted(future_unsafe)),
            ),
        )

    state_bijective = (
        len(set(abstraction.abstraction_map.values())) == len(abstraction.micro_states)
        and set(abstraction.abstraction_map.values()) == set(abstraction.macro_states)
    )
    status = (
        ScaleAbstractionStatus.EXACT_SCALE_EQUIVALENCE
        if state_bijective and not collapsed_queries
        else ScaleAbstractionStatus.CONTEXT_SAFE_ABSTRACTION
    )
    return ScaleAbstractionAssessment(
        abstraction.abstraction_id,
        status,
        (),
        (),
        tuple(sorted(collapsed_queries)),
        (),
        scientific_equivalence_granted=(
            status is ScaleAbstractionStatus.EXACT_SCALE_EQUIVALENCE
        ),
    )
