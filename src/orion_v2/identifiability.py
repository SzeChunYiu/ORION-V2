from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Hashable, Mapping

Outcome = Hashable


class ProbeKind(str, Enum):
    OBSERVATION = "OBSERVATION"
    INTERVENTION = "INTERVENTION"
    COMPUTATION = "COMPUTATION"
    EXPERT_JUDGMENT = "EXPERT_JUDGMENT"


class IdentifiabilityStatus(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    DISCRIMINABLE = "DISCRIMINABLE"
    STRUCTURALLY_NONIDENTIFIABLE = "STRUCTURALLY_NONIDENTIFIABLE"
    RESOURCE_BOUND = "RESOURCE_BOUND"
    AUTHORITY_REQUIRED = "AUTHORITY_REQUIRED"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class DiagnosticProbe:
    probe_id: str
    kind: ProbeKind
    cost: float
    required_authority_id: str = ""

    def __post_init__(self) -> None:
        if not self.probe_id.strip():
            raise ValueError("probe identity must be non-blank")
        object.__setattr__(self, "kind", ProbeKind(self.kind))
        if self.cost < 0:
            raise ValueError("probe cost must be non-negative")


@dataclass(frozen=True, slots=True)
class IdentifiabilityAndProbeSystem:
    system_id: str
    hypothesis_ids: frozenset[str]
    probes: tuple[DiagnosticProbe, ...]
    outcome_by_probe: Mapping[str, Mapping[str, Outcome]]

    def __post_init__(self) -> None:
        if not self.system_id.strip() or len(self.hypothesis_ids) < 2:
            raise ValueError("identifiability systems require identity and >=2 hypotheses")
        if any(not item.strip() for item in self.hypothesis_ids):
            raise ValueError("hypothesis ids may not be blank")
        probe_ids = [probe.probe_id for probe in self.probes]
        if not probe_ids or len(probe_ids) != len(set(probe_ids)):
            raise ValueError("probe identities must be non-empty and unique")
        if set(self.outcome_by_probe) != set(probe_ids):
            raise ValueError("every probe requires an outcome table")
        for probe_id, table in self.outcome_by_probe.items():
            if set(table) != set(self.hypothesis_ids):
                raise ValueError(f"probe {probe_id} must cover every hypothesis")


@dataclass(frozen=True, slots=True)
class IdentifiabilityAssessment:
    system_id: str
    status: IdentifiabilityStatus
    equivalence_classes: tuple[tuple[str, ...], ...]
    selected_probe_ids: tuple[str, ...]
    minimum_additional_probe_ids: tuple[str, ...]
    minimum_additional_cost: float | None
    blocking_authority_ids: tuple[str, ...]
    violations: tuple[str, ...]
    scientific_truth_granted: bool = False

    def __post_init__(self) -> None:
        if self.scientific_truth_granted:
            raise ValueError("identifiability assessment cannot grant scientific truth")


def equivalence_classes(
    system: IdentifiabilityAndProbeSystem,
    probe_ids: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    known = {probe.probe_id for probe in system.probes}
    if not set(probe_ids) <= known:
        raise ValueError("unknown probe identity")
    cells: dict[tuple[Outcome, ...], list[str]] = {}
    for hypothesis_id in sorted(system.hypothesis_ids):
        signature = tuple(
            system.outcome_by_probe[probe_id][hypothesis_id] for probe_id in probe_ids
        )
        cells.setdefault(signature, []).append(hypothesis_id)
    return tuple(sorted(tuple(values) for values in cells.values()))


def _is_identified(classes: tuple[tuple[str, ...], ...]) -> bool:
    return all(len(cell) == 1 for cell in classes)


def _probe_lookup(
    system: IdentifiabilityAndProbeSystem,
) -> dict[str, DiagnosticProbe]:
    return {probe.probe_id: probe for probe in system.probes}


def minimum_separating_probe_set(
    system: IdentifiabilityAndProbeSystem,
    *,
    existing_probe_ids: tuple[str, ...] = (),
    admissible_probe_ids: tuple[str, ...] | None = None,
    available_authority_ids: tuple[str, ...] = (),
    resource_budget: float | None = None,
) -> tuple[tuple[str, ...], float] | None:
    if resource_budget is not None and resource_budget < 0:
        raise ValueError("resource budget must be non-negative")
    lookup = _probe_lookup(system)
    candidate_ids = (
        tuple(admissible_probe_ids)
        if admissible_probe_ids is not None
        else tuple(sorted(lookup))
    )
    if not set(candidate_ids) <= set(lookup):
        raise ValueError("unknown admissible probe identity")
    if not set(existing_probe_ids) <= set(lookup):
        raise ValueError("unknown existing probe identity")
    available_authority = set(available_authority_ids)
    candidates = [
        probe_id
        for probe_id in candidate_ids
        if probe_id not in existing_probe_ids
        and (
            not lookup[probe_id].required_authority_id
            or lookup[probe_id].required_authority_id in available_authority
        )
    ]
    if len(candidates) > 20:
        raise ValueError("finite exact probe search is capped at twenty candidates")

    best: tuple[tuple[str, ...], float] | None = None
    for size in range(len(candidates) + 1):
        for subset in combinations(candidates, size):
            cost = sum(lookup[probe_id].cost for probe_id in subset)
            if resource_budget is not None and cost > resource_budget:
                continue
            if best is not None and cost > best[1]:
                continue
            combined = tuple(dict.fromkeys(existing_probe_ids + subset))
            if _is_identified(equivalence_classes(system, combined)):
                candidate = (tuple(sorted(subset)), cost)
                if best is None or (cost, len(subset), candidate[0]) < (
                    best[1],
                    len(best[0]),
                    best[0],
                ):
                    best = candidate
        if best is not None and best[1] == 0:
            break
    return best


def assess_identifiability(
    system: IdentifiabilityAndProbeSystem,
    *,
    selected_probe_ids: tuple[str, ...] = (),
    admissible_probe_ids: tuple[str, ...] | None = None,
    available_authority_ids: tuple[str, ...] = (),
    resource_budget: float | None = None,
) -> IdentifiabilityAssessment:
    lookup = _probe_lookup(system)
    if not set(selected_probe_ids) <= set(lookup):
        return IdentifiabilityAssessment(
            system.system_id,
            IdentifiabilityStatus.CANNOT_CHECK,
            (),
            selected_probe_ids,
            (),
            None,
            (),
            ("selected probe is undeclared",),
        )
    classes = equivalence_classes(system, selected_probe_ids)
    if _is_identified(classes):
        return IdentifiabilityAssessment(
            system.system_id,
            IdentifiabilityStatus.IDENTIFIED,
            classes,
            selected_probe_ids,
            (),
            0.0,
            (),
            (),
        )

    candidate_ids = (
        tuple(admissible_probe_ids)
        if admissible_probe_ids is not None
        else tuple(sorted(lookup))
    )
    if not set(candidate_ids) <= set(lookup):
        return IdentifiabilityAssessment(
            system.system_id,
            IdentifiabilityStatus.CANNOT_CHECK,
            classes,
            selected_probe_ids,
            (),
            None,
            (),
            ("admissible probe is undeclared",),
        )

    all_authority = tuple(
        sorted(
            {
                probe.required_authority_id
                for probe in system.probes
                if probe.required_authority_id
            }
        )
    )
    unconstrained = minimum_separating_probe_set(
        system,
        existing_probe_ids=selected_probe_ids,
        admissible_probe_ids=candidate_ids,
        available_authority_ids=all_authority,
        resource_budget=None,
    )
    if unconstrained is None:
        return IdentifiabilityAssessment(
            system.system_id,
            IdentifiabilityStatus.STRUCTURALLY_NONIDENTIFIABLE,
            classes,
            selected_probe_ids,
            (),
            None,
            (),
            ("no registered probe family separates all live hypotheses",),
        )

    available_authority = set(available_authority_ids)
    blocking_authority = tuple(
        sorted(
            {
                lookup[probe_id].required_authority_id
                for probe_id in unconstrained[0]
                if lookup[probe_id].required_authority_id
                and lookup[probe_id].required_authority_id not in available_authority
            }
        )
    )
    if blocking_authority:
        return IdentifiabilityAssessment(
            system.system_id,
            IdentifiabilityStatus.AUTHORITY_REQUIRED,
            classes,
            selected_probe_ids,
            unconstrained[0],
            unconstrained[1],
            blocking_authority,
            ("a separating probe requires unavailable authority",),
        )

    constrained = minimum_separating_probe_set(
        system,
        existing_probe_ids=selected_probe_ids,
        admissible_probe_ids=candidate_ids,
        available_authority_ids=available_authority_ids,
        resource_budget=resource_budget,
    )
    if constrained is None:
        return IdentifiabilityAssessment(
            system.system_id,
            IdentifiabilityStatus.RESOURCE_BOUND,
            classes,
            selected_probe_ids,
            unconstrained[0],
            unconstrained[1],
            (),
            ("a separating probe plan exists but exceeds the current resource bound",),
        )

    return IdentifiabilityAssessment(
        system.system_id,
        IdentifiabilityStatus.DISCRIMINABLE,
        classes,
        selected_probe_ids,
        constrained[0],
        constrained[1],
        (),
        (),
    )


def structural_information_gain_of_repetition(
    system: IdentifiabilityAndProbeSystem,
    *,
    selected_probe_ids: tuple[str, ...],
    repeated_probe_id: str,
) -> int:
    """Return reduction in deterministic structural equivalence classes.

    Repeating an unchanged deterministic probe cannot refine the partition.
    This does not deny statistical precision gains under a stochastic model;
    it only prevents precision from being misreported as structural identification.
    """

    if repeated_probe_id not in {probe.probe_id for probe in system.probes}:
        raise ValueError("unknown repeated probe")
    before = equivalence_classes(system, selected_probe_ids)
    after = equivalence_classes(
        system, tuple(dict.fromkeys(selected_probe_ids + (repeated_probe_id,)))
    )
    return len(after) - len(before)
