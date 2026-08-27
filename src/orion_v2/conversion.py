from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class MonotoneDirection(str, Enum):
    NONINCREASING = "NONINCREASING"
    NONDECREASING = "NONDECREASING"
    PRESERVED = "PRESERVED"


class ConversionStatus(str, Enum):
    CONVERSION_CERTIFIED = "CONVERSION_CERTIFIED"
    TARGET_NOT_REACHED = "TARGET_NOT_REACHED"
    INVALID_PATH = "INVALID_PATH"
    UNADMITTED_OPERATION = "UNADMITTED_OPERATION"
    PROTECTED_MONOTONE_VIOLATION = "PROTECTED_MONOTONE_VIOLATION"
    AUTHORITY_AMPLIFICATION = "AUTHORITY_AMPLIFICATION"
    RESOURCE_BOUND_EXCEEDED = "RESOURCE_BOUND_EXCEEDED"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class MonotoneSpec:
    monotone_id: str
    direction: MonotoneDirection
    tolerance: float = 0.0

    def __post_init__(self) -> None:
        if not self.monotone_id.strip():
            raise ValueError("monotone identity must be non-blank")
        object.__setattr__(self, "direction", MonotoneDirection(self.direction))
        if self.tolerance < 0:
            raise ValueError("monotone tolerance must be non-negative")


@dataclass(frozen=True, slots=True)
class ConversionTransition:
    source_state_id: str
    operation_id: str
    target_state_id: str
    resource_cost: float = 0.0
    certificate_id: str = ""

    def __post_init__(self) -> None:
        if any(
            not item.strip()
            for item in (self.source_state_id, self.operation_id, self.target_state_id)
        ):
            raise ValueError("conversion transitions require non-blank identities")
        if self.resource_cost < 0:
            raise ValueError("conversion resource cost must be non-negative")


@dataclass(frozen=True, slots=True)
class ConstrainedConversionSystem:
    system_id: str
    domain_id: str
    state_ids: frozenset[str]
    admitted_operation_ids: frozenset[str]
    transitions: tuple[ConversionTransition, ...]
    monotones: tuple[MonotoneSpec, ...]
    monotone_values: Mapping[str, Mapping[str, float]]
    authority_ceiling_by_state: Mapping[str, int]

    def __post_init__(self) -> None:
        if not self.system_id.strip() or not self.domain_id.strip():
            raise ValueError("conversion system/domain identities must be non-blank")
        if not self.state_ids or not self.admitted_operation_ids:
            raise ValueError("conversion systems require states and admitted operations")
        if any(not item.strip() for item in (*self.state_ids, *self.admitted_operation_ids)):
            raise ValueError("conversion identities may not be blank")
        for transition in self.transitions:
            if (
                transition.source_state_id not in self.state_ids
                or transition.target_state_id not in self.state_ids
            ):
                raise ValueError("conversion transition references an unknown state")
        monotone_ids = [item.monotone_id for item in self.monotones]
        if len(monotone_ids) != len(set(monotone_ids)):
            raise ValueError("monotone identities must be unique")
        if set(self.monotone_values) != set(monotone_ids):
            raise ValueError("every monotone requires a value table")
        for monotone_id, values in self.monotone_values.items():
            if set(values) != set(self.state_ids):
                raise ValueError(f"monotone {monotone_id} must cover every state")
        if set(self.authority_ceiling_by_state) != set(self.state_ids):
            raise ValueError("every state requires an authority ceiling")
        if any(level < 0 for level in self.authority_ceiling_by_state.values()):
            raise ValueError("authority ceilings must be non-negative")


@dataclass(frozen=True, slots=True)
class ConversionAssessment:
    system_id: str
    status: ConversionStatus
    path_state_ids: tuple[str, ...]
    operation_ids: tuple[str, ...]
    total_resource_cost: float
    violations: tuple[str, ...]
    authority_granted: bool = False
    scientific_success_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted or self.scientific_success_granted:
            raise ValueError("conversion assessments are non-authorizing")


def _monotone_holds(
    spec: MonotoneSpec,
    source_value: float,
    target_value: float,
) -> bool:
    if spec.direction is MonotoneDirection.NONINCREASING:
        return target_value <= source_value + spec.tolerance
    if spec.direction is MonotoneDirection.NONDECREASING:
        return target_value + spec.tolerance >= source_value
    return abs(target_value - source_value) <= spec.tolerance


def assess_conversion_path(
    system: ConstrainedConversionSystem,
    *,
    source_state_id: str,
    target_state_id: str,
    operation_ids: tuple[str, ...],
    resource_budget: float | None = None,
) -> ConversionAssessment:
    if source_state_id not in system.state_ids or target_state_id not in system.state_ids:
        return ConversionAssessment(
            system.system_id,
            ConversionStatus.CANNOT_CHECK,
            (),
            operation_ids,
            0.0,
            ("source or target state is undeclared",),
        )
    if resource_budget is not None and resource_budget < 0:
        raise ValueError("resource budget must be non-negative")

    by_source_operation: dict[tuple[str, str], list[ConversionTransition]] = {}
    for transition in system.transitions:
        by_source_operation.setdefault(
            (transition.source_state_id, transition.operation_id), []
        ).append(transition)

    current = source_state_id
    states = [current]
    total_cost = 0.0
    violations: list[str] = []
    for operation_id in operation_ids:
        if operation_id not in system.admitted_operation_ids:
            return ConversionAssessment(
                system.system_id,
                ConversionStatus.UNADMITTED_OPERATION,
                tuple(states),
                operation_ids,
                total_cost,
                (f"operation {operation_id} is not admitted",),
            )
        candidates = by_source_operation.get((current, operation_id), [])
        if len(candidates) != 1:
            return ConversionAssessment(
                system.system_id,
                ConversionStatus.INVALID_PATH,
                tuple(states),
                operation_ids,
                total_cost,
                (
                    f"expected exactly one transition from {current} under {operation_id}; found {len(candidates)}",
                ),
            )
        transition = candidates[0]
        next_state = transition.target_state_id
        total_cost += transition.resource_cost
        for spec in system.monotones:
            source_value = system.monotone_values[spec.monotone_id][current]
            target_value = system.monotone_values[spec.monotone_id][next_state]
            if not _monotone_holds(spec, source_value, target_value):
                violations.append(
                    f"monotone {spec.monotone_id} violated: {source_value} -> {target_value}"
                )
        if (
            system.authority_ceiling_by_state[next_state]
            > system.authority_ceiling_by_state[current]
        ):
            violations.append(
                f"authority amplified: {system.authority_ceiling_by_state[current]} -> {system.authority_ceiling_by_state[next_state]}"
            )
        current = next_state
        states.append(current)

    if any(item.startswith("monotone") for item in violations):
        status = ConversionStatus.PROTECTED_MONOTONE_VIOLATION
    elif any(item.startswith("authority") for item in violations):
        status = ConversionStatus.AUTHORITY_AMPLIFICATION
    elif resource_budget is not None and total_cost > resource_budget:
        status = ConversionStatus.RESOURCE_BOUND_EXCEEDED
        violations.append(
            f"resource budget exceeded: cost={total_cost}, budget={resource_budget}"
        )
    elif current != target_state_id:
        status = ConversionStatus.TARGET_NOT_REACHED
        violations.append(f"path ended at {current}, not {target_state_id}")
    else:
        status = ConversionStatus.CONVERSION_CERTIFIED

    return ConversionAssessment(
        system.system_id,
        status,
        tuple(states),
        operation_ids,
        total_cost,
        tuple(violations),
    )
