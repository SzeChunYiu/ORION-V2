from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Hashable, Mapping

State = Hashable
JudgmentValue = Hashable | frozenset[Hashable]


class AssumptionDisposition(str, Enum):
    PRESERVED = "PRESERVED"
    CALIBRATED = "CALIBRATED"
    RELAXED = "RELAXED"
    DROPPED = "DROPPED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class PreservationMode(str, Enum):
    EXACT = "EXACT"
    DECISION_RELATIVE = "DECISION_RELATIVE"
    SOUND_OVER_APPROXIMATION = "SOUND_OVER_APPROXIMATION"


class GeneralizationStatus(str, Enum):
    EXACT_INTERPRETATION = "EXACT_INTERPRETATION"
    CONSERVATIVE_GENERALIZATION = "CONSERVATIVE_GENERALIZATION"
    DECISION_RELATIVE_ADAPTATION = "DECISION_RELATIVE_ADAPTATION"
    SOUND_ABSTRACTION = "SOUND_ABSTRACTION"
    INVALID_TRANSITION_DRIFT = "INVALID_TRANSITION_DRIFT"
    INVALID_NATIVE_JUDGMENT_DRIFT = "INVALID_NATIVE_JUDGMENT_DRIFT"
    INVALID_ASSUMPTION_ERASURE = "INVALID_ASSUMPTION_ERASURE"
    INVALID_RESOURCE_UNDERSTATEMENT = "INVALID_RESOURCE_UNDERSTATEMENT"
    INVALID_AUTHORITY_AMPLIFICATION = "INVALID_AUTHORITY_AMPLIFICATION"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class FiniteTheory:
    theory_id: str
    domain_id: str
    states: frozenset[State]
    actions: frozenset[str]
    transitions: frozenset[tuple[State, str, State]]
    judgments: Mapping[str, Mapping[State, JudgmentValue]]
    assumptions: tuple[str, ...]
    action_cost_upper_bounds: Mapping[str, float]
    judgment_authority_ceiling: Mapping[str, int]

    def __post_init__(self) -> None:
        if not self.theory_id.strip() or not self.domain_id.strip():
            raise ValueError("theory and domain identities must be non-blank")
        if not self.states or not self.actions:
            raise ValueError("finite theories require non-empty states and actions")
        if any(not action.strip() for action in self.actions):
            raise ValueError("actions must be non-blank")
        if len(self.assumptions) != len(set(self.assumptions)) or any(
            not assumption.strip() for assumption in self.assumptions
        ):
            raise ValueError("assumptions must be unique non-blank identities")
        for source, action, target in self.transitions:
            if source not in self.states or target not in self.states or action not in self.actions:
                raise ValueError("transitions must use declared states and actions")
        for judgment_id, table in self.judgments.items():
            if not judgment_id.strip() or not set(table) <= set(self.states):
                raise ValueError("judgments must be named and defined only on declared states")
        if set(self.action_cost_upper_bounds) != set(self.actions):
            raise ValueError("every action requires a cost upper bound")
        if any(cost < 0 for cost in self.action_cost_upper_bounds.values()):
            raise ValueError("action costs must be non-negative")
        if set(self.judgment_authority_ceiling) != set(self.judgments):
            raise ValueError("every judgment requires an authority ceiling")
        if any(level < 0 for level in self.judgment_authority_ceiling.values()):
            raise ValueError("authority ceilings must be non-negative")


@dataclass(frozen=True, slots=True)
class AssumptionRecord:
    assumption_id: str
    disposition: AssumptionDisposition
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.assumption_id.strip():
            raise ValueError("assumption identities must be non-blank")
        object.__setattr__(self, "disposition", AssumptionDisposition(self.disposition))
        if any(not evidence_id.strip() for evidence_id in self.evidence_ids):
            raise ValueError("assumption evidence identities may not be blank")
        if self.disposition in {
            AssumptionDisposition.CALIBRATED,
            AssumptionDisposition.RELAXED,
            AssumptionDisposition.DROPPED,
            AssumptionDisposition.NOT_APPLICABLE,
        } and not self.evidence_ids:
            raise ValueError("non-preserved assumptions require evidence")


@dataclass(frozen=True, slots=True)
class TheoryTransport:
    transport_id: str
    native_theory_id: str
    generalized_theory_id: str
    state_map: Mapping[State, State]
    action_map: Mapping[str, str]
    judgment_map: Mapping[str, str]
    registered_judgment_ids: tuple[str, ...]
    assumption_records: tuple[AssumptionRecord, ...]
    preservation_mode: PreservationMode = PreservationMode.EXACT
    resource_tolerance: float = 0.0
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (
                self.transport_id,
                self.native_theory_id,
                self.generalized_theory_id,
            )
        ):
            raise ValueError("transport identities must be non-blank")
        object.__setattr__(self, "preservation_mode", PreservationMode(self.preservation_mode))
        if self.resource_tolerance < 0:
            raise ValueError("resource tolerance must be non-negative")
        if not self.registered_judgment_ids or any(
            not value.strip() for value in self.registered_judgment_ids
        ):
            raise ValueError("at least one registered native judgment is required")
        if any(not source_id.strip() for source_id in self.source_ids):
            raise ValueError("source identities may not be blank")


@dataclass(frozen=True, slots=True)
class GeneralizationAssessment:
    transport_id: str
    status: GeneralizationStatus
    violations: tuple[str, ...]
    warnings: tuple[str, ...]
    preserved_transition_count: int
    preserved_judgment_cells: int
    authority_granted: bool = False
    novelty_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted or self.novelty_granted:
            raise ValueError("generalization assessments are non-authorizing")


def _value_preserved(
    native_value: JudgmentValue,
    generalized_value: JudgmentValue,
    mode: PreservationMode,
) -> bool:
    if mode is PreservationMode.SOUND_OVER_APPROXIMATION:
        if isinstance(generalized_value, frozenset):
            return native_value in generalized_value
        return native_value == generalized_value
    return native_value == generalized_value


def _exact_bijection(mapping: Mapping[Hashable, Hashable], codomain: frozenset[Hashable]) -> bool:
    return set(mapping.values()) == set(codomain) and len(set(mapping.values())) == len(mapping)


def assess_theory_transport(
    native: FiniteTheory,
    generalized: FiniteTheory,
    transport: TheoryTransport,
) -> GeneralizationAssessment:
    violations: list[str] = []
    warnings: list[str] = []
    preserved_transitions = 0
    preserved_judgments = 0

    if transport.native_theory_id != native.theory_id or transport.generalized_theory_id != generalized.theory_id:
        return GeneralizationAssessment(
            transport.transport_id,
            GeneralizationStatus.CANNOT_CHECK,
            ("transport theory identities do not match supplied theories",),
            (),
            0,
            0,
        )
    if not transport.source_ids:
        return GeneralizationAssessment(
            transport.transport_id,
            GeneralizationStatus.CANNOT_CHECK,
            ("source-bound native reconstruction is required",),
            (),
            0,
            0,
        )

    missing_states = set(native.states) - set(transport.state_map)
    missing_actions = set(native.actions) - set(transport.action_map)
    if missing_states:
        violations.append(f"unmapped native states: {sorted(map(repr, missing_states))}")
    if missing_actions:
        violations.append(f"unmapped native actions: {sorted(missing_actions)}")
    if any(target not in generalized.states for target in transport.state_map.values()):
        violations.append("state map reaches undeclared generalized states")
    if any(target not in generalized.actions for target in transport.action_map.values()):
        violations.append("action map reaches undeclared generalized actions")

    assumption_by_id = {record.assumption_id: record for record in transport.assumption_records}
    if set(assumption_by_id) != set(native.assumptions):
        missing = set(native.assumptions) - set(assumption_by_id)
        extra = set(assumption_by_id) - set(native.assumptions)
        details = []
        if missing:
            details.append(f"missing={sorted(missing)}")
        if extra:
            details.append(f"extra={sorted(extra)}")
        return GeneralizationAssessment(
            transport.transport_id,
            GeneralizationStatus.INVALID_ASSUMPTION_ERASURE,
            tuple(violations + ["assumption ledger mismatch " + " ".join(details)]),
            tuple(warnings),
            0,
            0,
        )

    generalized_transition_set = set(generalized.transitions)
    for source, action, target in native.transitions:
        if source not in transport.state_map or target not in transport.state_map or action not in transport.action_map:
            continue
        mapped = (
            transport.state_map[source],
            transport.action_map[action],
            transport.state_map[target],
        )
        if mapped not in generalized_transition_set:
            violations.append(f"native transition is not simulated: {source!r}-{action}->{target!r}")
        else:
            preserved_transitions += 1
    if any("transition" in violation for violation in violations):
        return GeneralizationAssessment(
            transport.transport_id,
            GeneralizationStatus.INVALID_TRANSITION_DRIFT,
            tuple(violations),
            tuple(warnings),
            preserved_transitions,
            preserved_judgments,
        )

    for native_action, generalized_action in transport.action_map.items():
        if native_action not in native.action_cost_upper_bounds or generalized_action not in generalized.action_cost_upper_bounds:
            continue
        native_cost = native.action_cost_upper_bounds[native_action]
        generalized_cost = generalized.action_cost_upper_bounds[generalized_action]
        if generalized_cost + transport.resource_tolerance < native_cost:
            violations.append(
                f"resource understatement for {native_action}: native={native_cost}, generalized={generalized_cost}"
            )
    if any("resource understatement" in violation for violation in violations):
        return GeneralizationAssessment(
            transport.transport_id,
            GeneralizationStatus.INVALID_RESOURCE_UNDERSTATEMENT,
            tuple(violations),
            tuple(warnings),
            preserved_transitions,
            preserved_judgments,
        )

    for native_judgment_id in transport.registered_judgment_ids:
        generalized_judgment_id = transport.judgment_map.get(native_judgment_id)
        if native_judgment_id not in native.judgments or generalized_judgment_id not in generalized.judgments:
            violations.append(f"unmapped or undeclared judgment: {native_judgment_id}")
            continue
        native_authority = native.judgment_authority_ceiling[native_judgment_id]
        generalized_authority = generalized.judgment_authority_ceiling[generalized_judgment_id]
        if generalized_authority > native_authority:
            violations.append(
                f"authority amplification for {native_judgment_id}: native={native_authority}, generalized={generalized_authority}"
            )
        for native_state, native_value in native.judgments[native_judgment_id].items():
            if native_state not in transport.state_map:
                continue
            generalized_state = transport.state_map[native_state]
            generalized_table = generalized.judgments[generalized_judgment_id]
            if generalized_state not in generalized_table:
                violations.append(
                    f"generalized judgment {generalized_judgment_id} is undefined at mapped state {generalized_state!r}"
                )
                continue
            if not _value_preserved(
                native_value,
                generalized_table[generalized_state],
                transport.preservation_mode,
            ):
                violations.append(
                    f"native judgment drift for {native_judgment_id} at {native_state!r}"
                )
            else:
                preserved_judgments += 1

    if any("authority amplification" in violation for violation in violations):
        return GeneralizationAssessment(
            transport.transport_id,
            GeneralizationStatus.INVALID_AUTHORITY_AMPLIFICATION,
            tuple(violations),
            tuple(warnings),
            preserved_transitions,
            preserved_judgments,
        )
    if violations:
        return GeneralizationAssessment(
            transport.transport_id,
            GeneralizationStatus.INVALID_NATIVE_JUDGMENT_DRIFT,
            tuple(violations),
            tuple(warnings),
            preserved_transitions,
            preserved_judgments,
        )

    if set(transport.registered_judgment_ids) != set(native.judgments):
        warnings.append("transport is justified only for the registered decision family")
        status = GeneralizationStatus.DECISION_RELATIVE_ADAPTATION
    elif transport.preservation_mode is PreservationMode.SOUND_OVER_APPROXIMATION:
        status = GeneralizationStatus.SOUND_ABSTRACTION
    else:
        state_exact = _exact_bijection(transport.state_map, generalized.states)
        action_exact = _exact_bijection(transport.action_map, generalized.actions)
        mapped_native_transitions = {
            (transport.state_map[source], transport.action_map[action], transport.state_map[target])
            for source, action, target in native.transitions
        }
        costs_exact = all(
            native.action_cost_upper_bounds[action]
            == generalized.action_cost_upper_bounds[transport.action_map[action]]
            for action in native.actions
        )
        if state_exact and action_exact and mapped_native_transitions == set(generalized.transitions) and costs_exact:
            status = GeneralizationStatus.EXACT_INTERPRETATION
        else:
            status = GeneralizationStatus.CONSERVATIVE_GENERALIZATION

    return GeneralizationAssessment(
        transport.transport_id,
        status,
        (),
        tuple(warnings),
        preserved_transitions,
        preserved_judgments,
    )


class SharedEnvelopeStatus(str, Enum):
    SHARED_EXACT_ENVELOPE = "SHARED_EXACT_ENVELOPE"
    SHARED_CONSERVATIVE_ENVELOPE = "SHARED_CONSERVATIVE_ENVELOPE"
    DECISION_RELATIVE_NEIGHBORS = "DECISION_RELATIVE_NEIGHBORS"
    NO_SHARED_REGISTERED_DECISION = "NO_SHARED_REGISTERED_DECISION"
    INVALID_TRANSPORT = "INVALID_TRANSPORT"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class SharedEnvelopeAssessment:
    status: SharedEnvelopeStatus
    left_transport_status: GeneralizationStatus
    right_transport_status: GeneralizationStatus
    shared_generalized_judgment_ids: tuple[str, ...]
    semantic_identity_claimed: bool = False
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.semantic_identity_claimed or self.authority_granted:
            raise ValueError("shared envelopes establish neither semantic identity nor authority")


def assess_shared_envelope(
    left_native: FiniteTheory,
    right_native: FiniteTheory,
    generalized: FiniteTheory,
    left_transport: TheoryTransport,
    right_transport: TheoryTransport,
) -> SharedEnvelopeAssessment:
    left = assess_theory_transport(left_native, generalized, left_transport)
    right = assess_theory_transport(right_native, generalized, right_transport)
    invalid_statuses = {
        GeneralizationStatus.INVALID_TRANSITION_DRIFT,
        GeneralizationStatus.INVALID_NATIVE_JUDGMENT_DRIFT,
        GeneralizationStatus.INVALID_ASSUMPTION_ERASURE,
        GeneralizationStatus.INVALID_RESOURCE_UNDERSTATEMENT,
        GeneralizationStatus.INVALID_AUTHORITY_AMPLIFICATION,
    }
    if left.status in invalid_statuses or right.status in invalid_statuses:
        status = SharedEnvelopeStatus.INVALID_TRANSPORT
    elif GeneralizationStatus.CANNOT_CHECK in {left.status, right.status}:
        status = SharedEnvelopeStatus.CANNOT_CHECK
    else:
        left_generalized = {
            left_transport.judgment_map[judgment_id]
            for judgment_id in left_transport.registered_judgment_ids
            if judgment_id in left_transport.judgment_map
        }
        right_generalized = {
            right_transport.judgment_map[judgment_id]
            for judgment_id in right_transport.registered_judgment_ids
            if judgment_id in right_transport.judgment_map
        }
        shared = tuple(sorted(left_generalized & right_generalized))
        if not shared:
            status = SharedEnvelopeStatus.NO_SHARED_REGISTERED_DECISION
        elif GeneralizationStatus.DECISION_RELATIVE_ADAPTATION in {left.status, right.status}:
            status = SharedEnvelopeStatus.DECISION_RELATIVE_NEIGHBORS
        elif left.status is GeneralizationStatus.EXACT_INTERPRETATION and right.status is GeneralizationStatus.EXACT_INTERPRETATION:
            status = SharedEnvelopeStatus.SHARED_EXACT_ENVELOPE
        else:
            status = SharedEnvelopeStatus.SHARED_CONSERVATIVE_ENVELOPE
        return SharedEnvelopeAssessment(status, left.status, right.status, shared)
    return SharedEnvelopeAssessment(status, left.status, right.status, ())
