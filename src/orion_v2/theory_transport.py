from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Hashable, Mapping

State = Hashable
JudgmentValue = Hashable | frozenset[Hashable]


def _nonblank(value: str, *, field_name: str) -> str:
    if not value.strip():
        raise ValueError(f"{field_name} must be non-blank")
    return value


def _as_value_set(value: JudgmentValue) -> frozenset[Hashable]:
    return value if isinstance(value, frozenset) else frozenset({value})


class InterpretationKind(str, Enum):
    EXACT = "EXACT"
    CONSERVATIVE_EXTENSION = "CONSERVATIVE_EXTENSION"
    DECISION_RELATIVE = "DECISION_RELATIVE"
    SOUND_ABSTRACTION = "SOUND_ABSTRACTION"


class AssumptionDisposition(str, Enum):
    PRESERVED = "PRESERVED"
    CALIBRATED = "CALIBRATED"
    RELAXED = "RELAXED"
    DROPPED = "DROPPED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class InterpretationStatus(str, Enum):
    EXACT_INTERPRETATION = "EXACT_INTERPRETATION"
    CONSERVATIVE_EXTENSION = "CONSERVATIVE_EXTENSION"
    DECISION_RELATIVE_ADAPTATION = "DECISION_RELATIVE_ADAPTATION"
    SOUND_ABSTRACTION = "SOUND_ABSTRACTION"
    INVALID_IDENTITY_OR_EPOCH = "INVALID_IDENTITY_OR_EPOCH"
    INVALID_INCOMPLETE_MAPPING = "INVALID_INCOMPLETE_MAPPING"
    INVALID_ASSUMPTION_TREATMENT = "INVALID_ASSUMPTION_TREATMENT"
    INVALID_TRANSITION_SIMULATION = "INVALID_TRANSITION_SIMULATION"
    INVALID_BACKWARD_REFLECTION = "INVALID_BACKWARD_REFLECTION"
    INVALID_JUDGMENT_PRESERVATION = "INVALID_JUDGMENT_PRESERVATION"
    INVALID_UNDECLARED_INFORMATION_LOSS = "INVALID_UNDECLARED_INFORMATION_LOSS"
    INVALID_ROUND_TRIP = "INVALID_ROUND_TRIP"
    INVALID_RESOURCE_CALIBRATION = "INVALID_RESOURCE_CALIBRATION"
    INVALID_AUTHORITY_AMPLIFICATION = "INVALID_AUTHORITY_AMPLIFICATION"
    INVALID_COUNTEREXAMPLE_REFLECTION = "INVALID_COUNTEREXAMPLE_REFLECTION"
    CANNOT_CHECK = "CANNOT_CHECK"


class ValidityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED_SOURCE_EPOCH = "EXPIRED_SOURCE_EPOCH"
    EXPIRED_TARGET_EPOCH = "EXPIRED_TARGET_EPOCH"
    EXPIRED_ASSUMPTIONS = "EXPIRED_ASSUMPTIONS"
    EXPIRED_CALIBRATION = "EXPIRED_CALIBRATION"
    EXPIRED_EVALUATOR = "EXPIRED_EVALUATOR"
    EXPIRED_RESOURCE_MODEL = "EXPIRED_RESOURCE_MODEL"
    EXPIRED_AUTHORITY_POLICY = "EXPIRED_AUTHORITY_POLICY"
    MULTIPLE_EXPIRATIONS = "MULTIPLE_EXPIRATIONS"
    CANNOT_CHECK = "CANNOT_CHECK"


class AdaptationStatus(str, Enum):
    READY_FOR_PROTECTED_TARGET_EVALUATION = "READY_FOR_PROTECTED_TARGET_EVALUATION"
    INVALID_SOURCE_INTERPRETATION = "INVALID_SOURCE_INTERPRETATION"
    INVALID_TARGET_INTERPRETATION = "INVALID_TARGET_INTERPRETATION"
    NO_SHARED_REGISTERED_DECISION = "NO_SHARED_REGISTERED_DECISION"
    INVALID_TARGET_REALIZATION = "INVALID_TARGET_REALIZATION"
    MISSING_TARGET_CALIBRATION = "MISSING_TARGET_CALIBRATION"
    MISSING_TARGET_VALIDATION = "MISSING_TARGET_VALIDATION"
    CANNOT_CHECK = "CANNOT_CHECK"


class CompositionStatus(str, Enum):
    COMPOSED_EXACT = "COMPOSED_EXACT"
    COMPOSED_CONSERVATIVE = "COMPOSED_CONSERVATIVE"
    COMPOSED_DECISION_RELATIVE = "COMPOSED_DECISION_RELATIVE"
    COMPOSED_SOUND_ABSTRACTION = "COMPOSED_SOUND_ABSTRACTION"
    INVALID_NONCONTIGUOUS_CHAIN = "INVALID_NONCONTIGUOUS_CHAIN"
    INVALID_JUDGMENT_CHAIN = "INVALID_JUDGMENT_CHAIN"
    INVALID_INPUT_CERTIFICATE = "INVALID_INPUT_CERTIFICATE"
    CANNOT_CHECK = "CANNOT_CHECK"


_VALID_INTERPRETATION_STATUSES = frozenset(
    {
        InterpretationStatus.EXACT_INTERPRETATION,
        InterpretationStatus.CONSERVATIVE_EXTENSION,
        InterpretationStatus.DECISION_RELATIVE_ADAPTATION,
        InterpretationStatus.SOUND_ABSTRACTION,
    }
)


@dataclass(frozen=True, slots=True)
class ResourceInterval:
    dimension_id: str
    unit_id: str
    lower: float
    upper: float

    def __post_init__(self) -> None:
        _nonblank(self.dimension_id, field_name="resource dimension")
        _nonblank(self.unit_id, field_name="resource unit")
        if self.lower < 0 or self.upper < self.lower:
            raise ValueError("resource intervals require 0 <= lower <= upper")


@dataclass(frozen=True, slots=True)
class ResourceCalibration:
    native_dimension_id: str
    generalized_dimension_id: str
    native_unit_id: str
    generalized_unit_id: str
    scale: float = 1.0
    offset: float = 0.0
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name, value in (
            ("native resource dimension", self.native_dimension_id),
            ("generalized resource dimension", self.generalized_dimension_id),
            ("native resource unit", self.native_unit_id),
            ("generalized resource unit", self.generalized_unit_id),
        ):
            _nonblank(value, field_name=field_name)
        if self.scale <= 0:
            raise ValueError("resource calibration scale must be positive")
        if (
            self.native_dimension_id != self.generalized_dimension_id
            or self.native_unit_id != self.generalized_unit_id
            or self.scale != 1.0
            or self.offset != 0.0
        ) and not self.evidence_ids:
            raise ValueError("non-identity resource calibration requires evidence")
        if any(not evidence_id.strip() for evidence_id in self.evidence_ids):
            raise ValueError("resource calibration evidence ids may not be blank")

    def map_interval(self, interval: ResourceInterval) -> ResourceInterval:
        if (
            interval.dimension_id != self.native_dimension_id
            or interval.unit_id != self.native_unit_id
        ):
            raise ValueError("resource interval does not match calibration source")
        lower = self.scale * interval.lower + self.offset
        upper = self.scale * interval.upper + self.offset
        if lower < 0:
            raise ValueError("resource calibration produced a negative lower bound")
        return ResourceInterval(
            self.generalized_dimension_id,
            self.generalized_unit_id,
            min(lower, upper),
            max(lower, upper),
        )


@dataclass(frozen=True, slots=True)
class ScientificTheory:
    theory_id: str
    domain_id: str
    epoch_id: str
    states: frozenset[State]
    actions: frozenset[str]
    transitions: frozenset[tuple[State, str, State]]
    judgments: Mapping[str, Mapping[State, JudgmentValue]]
    assumptions: tuple[str, ...]
    action_resources: Mapping[str, tuple[ResourceInterval, ...]]
    judgment_authority_ceiling: Mapping[str, int]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("theory id", self.theory_id),
            ("domain id", self.domain_id),
            ("epoch id", self.epoch_id),
        ):
            _nonblank(value, field_name=field_name)
        if not self.states or not self.actions:
            raise ValueError("scientific theories require non-empty states and actions")
        if any(not action.strip() for action in self.actions):
            raise ValueError("action ids may not be blank")
        if len(self.assumptions) != len(set(self.assumptions)) or any(
            not assumption.strip() for assumption in self.assumptions
        ):
            raise ValueError("assumption ids must be unique and non-blank")
        for source, action, target in self.transitions:
            if source not in self.states or target not in self.states:
                raise ValueError("transitions must use declared states")
            if action not in self.actions:
                raise ValueError("transitions must use declared actions")
        for judgment_id, table in self.judgments.items():
            _nonblank(judgment_id, field_name="judgment id")
            if not set(table) <= set(self.states):
                raise ValueError("judgments may be defined only on declared states")
        if set(self.action_resources) != set(self.actions):
            raise ValueError("every action requires a resource declaration")
        for action, intervals in self.action_resources.items():
            dimensions = [interval.dimension_id for interval in intervals]
            if len(dimensions) != len(set(dimensions)):
                raise ValueError(f"action {action} repeats a resource dimension")
        if set(self.judgment_authority_ceiling) != set(self.judgments):
            raise ValueError("every judgment requires an authority ceiling")
        if any(level < 0 for level in self.judgment_authority_ceiling.values()):
            raise ValueError("authority ceilings must be non-negative")


@dataclass(frozen=True, slots=True)
class AssumptionTreatment:
    assumption_id: str
    disposition: AssumptionDisposition
    evidence_ids: tuple[str, ...] = ()
    revalidation_obligation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _nonblank(self.assumption_id, field_name="assumption id")
        object.__setattr__(self, "disposition", AssumptionDisposition(self.disposition))
        if any(not item.strip() for item in self.evidence_ids):
            raise ValueError("assumption evidence ids may not be blank")
        if any(not item.strip() for item in self.revalidation_obligation_ids):
            raise ValueError("revalidation obligation ids may not be blank")
        if self.disposition is not AssumptionDisposition.PRESERVED:
            if not self.evidence_ids or not self.revalidation_obligation_ids:
                raise ValueError(
                    "non-preserved assumptions require evidence and revalidation obligations"
                )


@dataclass(frozen=True, slots=True)
class CounterexampleWitness:
    witness_id: str
    native_state: State
    native_judgment_id: str
    refuting_value: JudgmentValue
    decisive_reflection_required: bool = True
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _nonblank(self.witness_id, field_name="counterexample witness id")
        _nonblank(self.native_judgment_id, field_name="counterexample judgment id")
        if any(not source_id.strip() for source_id in self.source_ids):
            raise ValueError("counterexample source ids may not be blank")


@dataclass(frozen=True, slots=True)
class GeneralizationContext:
    context_id: str
    registered_judgment_ids: tuple[str, ...]
    registered_action_ids: tuple[str, ...]
    allowed_lost_judgment_ids: tuple[str, ...] = ()
    required_counterexample_ids: tuple[str, ...] = ()
    resource_tolerance: float = 0.0

    def __post_init__(self) -> None:
        _nonblank(self.context_id, field_name="generalization context id")
        for field_name, values in (
            ("registered judgment", self.registered_judgment_ids),
            ("registered action", self.registered_action_ids),
            ("allowed lost judgment", self.allowed_lost_judgment_ids),
            ("required counterexample", self.required_counterexample_ids),
        ):
            if any(not value.strip() for value in values):
                raise ValueError(f"{field_name} ids may not be blank")
            if len(values) != len(set(values)):
                raise ValueError(f"{field_name} ids must be unique")
        if not self.registered_judgment_ids or not self.registered_action_ids:
            raise ValueError("a context requires registered judgments and actions")
        if set(self.registered_judgment_ids) & set(self.allowed_lost_judgment_ids):
            raise ValueError("registered judgments cannot simultaneously be declared lost")
        if self.resource_tolerance < 0:
            raise ValueError("resource tolerance must be non-negative")


@dataclass(frozen=True, slots=True)
class TheoryInterpretation:
    interpretation_id: str
    native_theory_id: str
    generalized_theory_id: str
    source_epoch_id: str
    generalized_epoch_id: str
    kind: InterpretationKind
    context: GeneralizationContext
    state_map: Mapping[State, State]
    reverse_state_map: Mapping[State, frozenset[State]]
    action_map: Mapping[str, str]
    reverse_action_map: Mapping[str, frozenset[str]]
    judgment_map: Mapping[str, str]
    assumption_treatments: tuple[AssumptionTreatment, ...]
    resource_calibrations: tuple[ResourceCalibration, ...] = ()
    counterexamples: tuple[CounterexampleWitness, ...] = ()
    uncertainty_bound: float = 0.0
    semantic_loss_bound: float = 0.0
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name, value in (
            ("interpretation id", self.interpretation_id),
            ("native theory id", self.native_theory_id),
            ("generalized theory id", self.generalized_theory_id),
            ("source epoch id", self.source_epoch_id),
            ("generalized epoch id", self.generalized_epoch_id),
        ):
            _nonblank(value, field_name=field_name)
        object.__setattr__(self, "kind", InterpretationKind(self.kind))
        if self.uncertainty_bound < 0 or self.semantic_loss_bound < 0:
            raise ValueError("uncertainty and semantic loss bounds must be non-negative")
        if not self.source_ids or any(not source_id.strip() for source_id in self.source_ids):
            raise ValueError("interpretations require non-blank source identities")
        treatment_ids = [item.assumption_id for item in self.assumption_treatments]
        if len(treatment_ids) != len(set(treatment_ids)):
            raise ValueError("assumption treatments may not repeat an assumption")
        witness_ids = [item.witness_id for item in self.counterexamples]
        if len(witness_ids) != len(set(witness_ids)):
            raise ValueError("counterexample witnesses must have unique ids")


@dataclass(frozen=True, slots=True)
class InterpretationAssessment:
    interpretation_id: str
    status: InterpretationStatus
    violations: tuple[str, ...]
    warnings: tuple[str, ...]
    preserved_transition_count: int
    reflected_transition_count: int
    preserved_judgment_cell_count: int
    round_trip_state_count: int
    reflected_counterexample_ids: tuple[str, ...]
    collapsed_judgment_ids: tuple[str, ...]
    authority_granted: bool = False
    novelty_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted or self.novelty_granted:
            raise ValueError("interpretation assessments are non-authorizing")

    @property
    def valid(self) -> bool:
        return self.status in _VALID_INTERPRETATION_STATUSES


def _resources_by_dimension(
    intervals: tuple[ResourceInterval, ...],
) -> dict[str, ResourceInterval]:
    return {interval.dimension_id: interval for interval in intervals}


def _find_calibration(
    native_interval: ResourceInterval,
    generalized_intervals: tuple[ResourceInterval, ...],
    calibrations: tuple[ResourceCalibration, ...],
) -> ResourceCalibration | None:
    for calibration in calibrations:
        if (
            calibration.native_dimension_id == native_interval.dimension_id
            and calibration.native_unit_id == native_interval.unit_id
            and any(
                generalized.dimension_id == calibration.generalized_dimension_id
                and generalized.unit_id == calibration.generalized_unit_id
                for generalized in generalized_intervals
            )
        ):
            return calibration
    for generalized in generalized_intervals:
        if (
            generalized.dimension_id == native_interval.dimension_id
            and generalized.unit_id == native_interval.unit_id
        ):
            return ResourceCalibration(
                native_interval.dimension_id,
                generalized.dimension_id,
                native_interval.unit_id,
                generalized.unit_id,
            )
    return None


def _preserves_value(
    native_value: JudgmentValue,
    generalized_value: JudgmentValue,
    kind: InterpretationKind,
) -> bool:
    if kind is InterpretationKind.SOUND_ABSTRACTION:
        return _as_value_set(native_value) <= _as_value_set(generalized_value)
    return native_value == generalized_value


def _status_for_kind(kind: InterpretationKind) -> InterpretationStatus:
    return {
        InterpretationKind.EXACT: InterpretationStatus.EXACT_INTERPRETATION,
        InterpretationKind.CONSERVATIVE_EXTENSION: InterpretationStatus.CONSERVATIVE_EXTENSION,
        InterpretationKind.DECISION_RELATIVE: InterpretationStatus.DECISION_RELATIVE_ADAPTATION,
        InterpretationKind.SOUND_ABSTRACTION: InterpretationStatus.SOUND_ABSTRACTION,
    }[kind]


def assess_interpretation(
    native: ScientificTheory,
    generalized: ScientificTheory,
    interpretation: TheoryInterpretation,
) -> InterpretationAssessment:
    violations: list[str] = []
    warnings: list[str] = []
    preserved_transitions = 0
    reflected_transitions = 0
    preserved_judgments = 0
    round_trip_states = 0
    reflected_counterexamples: list[str] = []
    collapsed_judgments: set[str] = set()

    def result(status: InterpretationStatus) -> InterpretationAssessment:
        return InterpretationAssessment(
            interpretation.interpretation_id,
            status,
            tuple(violations),
            tuple(warnings),
            preserved_transitions,
            reflected_transitions,
            preserved_judgments,
            round_trip_states,
            tuple(sorted(reflected_counterexamples)),
            tuple(sorted(collapsed_judgments)),
        )

    if (
        interpretation.native_theory_id != native.theory_id
        or interpretation.generalized_theory_id != generalized.theory_id
        or interpretation.source_epoch_id != native.epoch_id
        or interpretation.generalized_epoch_id != generalized.epoch_id
    ):
        violations.append("theory or epoch identity mismatch")
        return result(InterpretationStatus.INVALID_IDENTITY_OR_EPOCH)

    if not set(interpretation.context.registered_judgment_ids) <= set(native.judgments):
        violations.append("context registers undeclared native judgments")
    if not set(interpretation.context.registered_action_ids) <= set(native.actions):
        violations.append("context registers undeclared native actions")
    if not set(interpretation.context.registered_judgment_ids) <= set(
        interpretation.judgment_map
    ):
        violations.append("registered judgments are not fully mapped")
    if set(native.states) != set(interpretation.state_map):
        violations.append("state map must cover exactly the native state scope")
    if set(native.actions) != set(interpretation.action_map):
        violations.append("action map must cover exactly the native action scope")
    if any(state not in generalized.states for state in interpretation.state_map.values()):
        violations.append("state map reaches undeclared generalized state")
    if any(action not in generalized.actions for action in interpretation.action_map.values()):
        violations.append("action map reaches undeclared generalized action")
    if violations:
        return result(InterpretationStatus.INVALID_INCOMPLETE_MAPPING)

    treatments = {
        treatment.assumption_id: treatment
        for treatment in interpretation.assumption_treatments
    }
    if set(treatments) != set(native.assumptions):
        violations.append("assumption treatment ledger does not match native assumptions")
        return result(InterpretationStatus.INVALID_ASSUMPTION_TREATMENT)
    if interpretation.kind in {
        InterpretationKind.EXACT,
        InterpretationKind.CONSERVATIVE_EXTENSION,
    } and any(
        item.disposition is not AssumptionDisposition.PRESERVED
        for item in treatments.values()
    ):
        violations.append("exact/conservative interpretation cannot relax native assumptions")
        return result(InterpretationStatus.INVALID_ASSUMPTION_TREATMENT)
    if any(
        item.disposition is not AssumptionDisposition.PRESERVED
        for item in treatments.values()
    ):
        warnings.append("non-preserved assumptions require target-native revalidation")

    for native_state, generalized_state in interpretation.state_map.items():
        preimage = interpretation.reverse_state_map.get(generalized_state, frozenset())
        if native_state not in preimage:
            violations.append(f"state round-trip loses native state {native_state!r}")
        elif any(
            source not in native.states
            or interpretation.state_map.get(source) != generalized_state
            for source in preimage
        ):
            violations.append(f"reverse state map for {generalized_state!r} is inconsistent")
        else:
            round_trip_states += 1
    for native_action, generalized_action in interpretation.action_map.items():
        preimage = interpretation.reverse_action_map.get(generalized_action, frozenset())
        if native_action not in preimage:
            violations.append(f"action round-trip loses native action {native_action}")
        elif any(
            source not in native.actions
            or interpretation.action_map.get(source) != generalized_action
            for source in preimage
        ):
            violations.append(f"reverse action map for {generalized_action} is inconsistent")
    if violations:
        return result(InterpretationStatus.INVALID_ROUND_TRIP)

    states_by_image: dict[State, list[State]] = {}
    for native_state, generalized_state in interpretation.state_map.items():
        states_by_image.setdefault(generalized_state, []).append(native_state)
    for group in states_by_image.values():
        for left, right in combinations(group, 2):
            for judgment_id, table in native.judgments.items():
                if left in table and right in table and table[left] != table[right]:
                    collapsed_judgments.add(judgment_id)
    undeclared_loss = collapsed_judgments - set(
        interpretation.context.allowed_lost_judgment_ids
    ) - set(interpretation.context.registered_judgment_ids)
    if undeclared_loss:
        violations.append(
            "collapsed native distinctions were not declared: "
            + ", ".join(sorted(undeclared_loss))
        )
        return result(InterpretationStatus.INVALID_UNDECLARED_INFORMATION_LOSS)
    registered_loss = collapsed_judgments & set(
        interpretation.context.registered_judgment_ids
    )
    if registered_loss and interpretation.kind is not InterpretationKind.SOUND_ABSTRACTION:
        violations.append(
            "registered native judgments differ inside a generalized state: "
            + ", ".join(sorted(registered_loss))
        )
        return result(InterpretationStatus.INVALID_JUDGMENT_PRESERVATION)
    if collapsed_judgments:
        warnings.append("transport is unsafe for future contexts that register collapsed judgments")

    generalized_transition_set = set(generalized.transitions)
    native_transition_set = set(native.transitions)
    for source, action, target in native.transitions:
        if action not in interpretation.context.registered_action_ids:
            continue
        mapped = (
            interpretation.state_map[source],
            interpretation.action_map[action],
            interpretation.state_map[target],
        )
        if mapped not in generalized_transition_set:
            violations.append(f"native transition is not simulated: {source!r}-{action}->{target!r}")
        else:
            preserved_transitions += 1
    if violations:
        return result(InterpretationStatus.INVALID_TRANSITION_SIMULATION)

    if interpretation.kind is not InterpretationKind.SOUND_ABSTRACTION:
        image_states = set(interpretation.state_map.values())
        image_actions = set(interpretation.action_map.values())
        for source, action, target in generalized.transitions:
            if source not in image_states or target not in image_states or action not in image_actions:
                continue
            native_witnesses = [
                (ns, na, nt)
                for ns in interpretation.reverse_state_map.get(source, frozenset())
                for na in interpretation.reverse_action_map.get(action, frozenset())
                for nt in interpretation.reverse_state_map.get(target, frozenset())
                if (ns, na, nt) in native_transition_set
            ]
            if not native_witnesses:
                violations.append(f"generalized transition has no native witness: {source!r}-{action}->{target!r}")
            else:
                reflected_transitions += 1
        if violations:
            return result(InterpretationStatus.INVALID_BACKWARD_REFLECTION)

    for native_judgment_id in interpretation.context.registered_judgment_ids:
        generalized_judgment_id = interpretation.judgment_map.get(native_judgment_id)
        if generalized_judgment_id not in generalized.judgments:
            violations.append(f"mapped generalized judgment is undeclared: {native_judgment_id}")
            continue
        if (
            generalized.judgment_authority_ceiling[generalized_judgment_id]
            > native.judgment_authority_ceiling[native_judgment_id]
        ):
            violations.append(f"authority amplification for judgment {native_judgment_id}")
        native_table = native.judgments[native_judgment_id]
        generalized_table = generalized.judgments[generalized_judgment_id]
        for native_state, native_value in native_table.items():
            generalized_state = interpretation.state_map[native_state]
            if generalized_state not in generalized_table:
                violations.append(f"generalized judgment {generalized_judgment_id} undefined at {generalized_state!r}")
                continue
            if not _preserves_value(native_value, generalized_table[generalized_state], interpretation.kind):
                violations.append(f"native judgment drift for {native_judgment_id} at {native_state!r}")
            else:
                preserved_judgments += 1
    if any("authority amplification" in item for item in violations):
        return result(InterpretationStatus.INVALID_AUTHORITY_AMPLIFICATION)
    if violations:
        return result(InterpretationStatus.INVALID_JUDGMENT_PRESERVATION)

    calibrations = interpretation.resource_calibrations
    for native_action, generalized_action in interpretation.action_map.items():
        native_intervals = native.action_resources[native_action]
        generalized_intervals = generalized.action_resources[generalized_action]
        generalized_by_dimension = _resources_by_dimension(generalized_intervals)
        for native_interval in native_intervals:
            calibration = _find_calibration(native_interval, generalized_intervals, calibrations)
            if calibration is None:
                violations.append(f"no resource calibration for {native_action}:{native_interval.dimension_id}")
                continue
            mapped = calibration.map_interval(native_interval)
            generalized_interval = generalized_by_dimension.get(mapped.dimension_id)
            if generalized_interval is None or generalized_interval.unit_id != mapped.unit_id:
                violations.append(f"generalized resource dimension missing for {native_action}:{mapped.dimension_id}")
                continue
            tolerance = interpretation.context.resource_tolerance
            if (
                generalized_interval.lower > mapped.lower + tolerance
                or generalized_interval.upper + tolerance < mapped.upper
            ):
                violations.append(
                    f"generalized resource interval does not conservatively contain native interval for {native_action}:{mapped.dimension_id}"
                )
    if violations:
        return result(InterpretationStatus.INVALID_RESOURCE_CALIBRATION)

    witnesses = {witness.witness_id: witness for witness in interpretation.counterexamples}
    if not set(interpretation.context.required_counterexample_ids) <= set(witnesses):
        violations.append("required counterexample witnesses are missing")
        return result(InterpretationStatus.INVALID_COUNTEREXAMPLE_REFLECTION)
    for witness_id in interpretation.context.required_counterexample_ids:
        witness = witnesses[witness_id]
        if (
            witness.native_state not in native.states
            or witness.native_judgment_id not in native.judgments
            or _as_value_set(native.judgments[witness.native_judgment_id].get(witness.native_state))
            != _as_value_set(witness.refuting_value)
        ):
            violations.append(f"native counterexample is not reproduced: {witness_id}")
            continue
        generalized_judgment_id = interpretation.judgment_map.get(witness.native_judgment_id)
        if generalized_judgment_id not in generalized.judgments:
            violations.append(f"counterexample judgment is not mapped: {witness_id}")
            continue
        generalized_state = interpretation.state_map[witness.native_state]
        generalized_value = generalized.judgments[generalized_judgment_id].get(generalized_state)
        if generalized_value is None:
            violations.append(f"counterexample is undefined in generalized theory: {witness_id}")
            continue
        if witness.decisive_reflection_required:
            reflected = _as_value_set(generalized_value) == _as_value_set(witness.refuting_value)
        else:
            reflected = _as_value_set(witness.refuting_value) <= _as_value_set(generalized_value)
        if not reflected:
            violations.append(f"counterexample is hidden or weakened: {witness_id}")
        else:
            reflected_counterexamples.append(witness_id)
    if violations:
        return result(InterpretationStatus.INVALID_COUNTEREXAMPLE_REFLECTION)

    if interpretation.kind is InterpretationKind.EXACT:
        state_bijective = (
            len(set(interpretation.state_map.values())) == len(native.states)
            and set(interpretation.state_map.values()) == set(generalized.states)
        )
        action_bijective = (
            len(set(interpretation.action_map.values())) == len(native.actions)
            and set(interpretation.action_map.values()) == set(generalized.actions)
        )
        all_judgments = set(interpretation.context.registered_judgment_ids) == set(native.judgments)
        judgment_bijective = (
            set(interpretation.judgment_map) == set(native.judgments)
            and len(set(interpretation.judgment_map.values())) == len(interpretation.judgment_map)
            and set(interpretation.judgment_map.values()) == set(generalized.judgments)
        )
        assumptions_exact = set(native.assumptions) == set(generalized.assumptions)
        authority_exact = all(
            generalized.judgment_authority_ceiling[interpretation.judgment_map[judgment_id]]
            == native.judgment_authority_ceiling[judgment_id]
            for judgment_id in native.judgments
        )
        resources_exact = True
        for native_action, generalized_action in interpretation.action_map.items():
            native_intervals = native.action_resources[native_action]
            generalized_intervals = generalized.action_resources[generalized_action]
            generalized_by_dimension = _resources_by_dimension(generalized_intervals)
            mapped_intervals: list[ResourceInterval] = []
            for native_interval in native_intervals:
                calibration = _find_calibration(native_interval, generalized_intervals, interpretation.resource_calibrations)
                if calibration is None:
                    resources_exact = False
                    break
                mapped_intervals.append(calibration.map_interval(native_interval))
            if not resources_exact:
                break
            if {
                (item.dimension_id, item.unit_id, item.lower, item.upper)
                for item in mapped_intervals
            } != {
                (item.dimension_id, item.unit_id, item.lower, item.upper)
                for item in generalized_by_dimension.values()
            }:
                resources_exact = False
                break
        if not (
            state_bijective
            and action_bijective
            and all_judgments
            and judgment_bijective
            and assumptions_exact
            and authority_exact
            and resources_exact
        ):
            violations.append(
                "exact interpretation requires bijective states/actions/judgments, exact assumptions, authority, and calibrated resources"
            )
            return result(InterpretationStatus.INVALID_ROUND_TRIP)

    if interpretation.kind is InterpretationKind.CONSERVATIVE_EXTENSION:
        if len(set(interpretation.state_map.values())) != len(native.states):
            violations.append("conservative extension requires injective state map")
        if len(set(interpretation.action_map.values())) != len(native.actions):
            violations.append("conservative extension requires injective action map")
        if set(interpretation.context.registered_judgment_ids) != set(native.judgments):
            violations.append("conservative extension must preserve all native judgments")
        if len(set(interpretation.judgment_map.values())) != len(interpretation.judgment_map):
            violations.append("conservative extension requires injective judgment map")
        if violations:
            return result(InterpretationStatus.INVALID_ROUND_TRIP)

    if interpretation.kind is InterpretationKind.DECISION_RELATIVE:
        if set(interpretation.context.registered_judgment_ids) == set(native.judgments):
            warnings.append("all native judgments are registered; a stronger interpretation kind may apply")

    return result(_status_for_kind(interpretation.kind))


def upgrade_wave2_finite_theory(
    theory: object,
    *,
    epoch_id: str,
    resource_dimension_id: str = "cost",
    resource_unit_id: str = "native-unit",
) -> ScientificTheory:
    """Lift the Wave-02 finite theory shape into the richer Wave-03 theory.

    The migration is deliberately conservative: a Wave-02 upper bound becomes
    the interval [0, upper]. No lower bound, unit conversion, epoch, or extra
    authority is inferred.
    """

    required_attributes = (
        "theory_id",
        "domain_id",
        "states",
        "actions",
        "transitions",
        "judgments",
        "assumptions",
        "action_cost_upper_bounds",
        "judgment_authority_ceiling",
    )
    missing = tuple(attribute for attribute in required_attributes if not hasattr(theory, attribute))
    if missing:
        raise ValueError("Wave-02 finite theory is missing attributes: " + ", ".join(missing))
    _nonblank(epoch_id, field_name="epoch id")
    _nonblank(resource_dimension_id, field_name="resource dimension id")
    _nonblank(resource_unit_id, field_name="resource unit id")
    actions = frozenset(getattr(theory, "actions"))
    upper_bounds = getattr(theory, "action_cost_upper_bounds")
    return ScientificTheory(
        theory_id=getattr(theory, "theory_id"),
        domain_id=getattr(theory, "domain_id"),
        epoch_id=epoch_id,
        states=frozenset(getattr(theory, "states")),
        actions=actions,
        transitions=frozenset(getattr(theory, "transitions")),
        judgments=getattr(theory, "judgments"),
        assumptions=tuple(getattr(theory, "assumptions")),
        action_resources={
            action: (
                ResourceInterval(
                    resource_dimension_id,
                    resource_unit_id,
                    0.0,
                    float(upper_bounds[action]),
                ),
            )
            for action in actions
        },
        judgment_authority_ceiling=getattr(theory, "judgment_authority_ceiling"),
    )


@dataclass(frozen=True, slots=True)
class TransportValidityBinding:
    interpretation_id: str
    source_epoch_id: str
    target_epoch_id: str
    assumptions_digest: str
    calibration_digest: str
    evaluator_digest: str
    resource_model_digest: str
    authority_policy_digest: str

    def __post_init__(self) -> None:
        for field_name, value in (
            ("interpretation id", self.interpretation_id),
            ("source epoch id", self.source_epoch_id),
            ("target epoch id", self.target_epoch_id),
            ("assumptions digest", self.assumptions_digest),
            ("calibration digest", self.calibration_digest),
            ("evaluator digest", self.evaluator_digest),
            ("resource model digest", self.resource_model_digest),
            ("authority policy digest", self.authority_policy_digest),
        ):
            _nonblank(value, field_name=field_name)


@dataclass(frozen=True, slots=True)
class ValidityAssessment:
    status: ValidityStatus
    expired_coordinates: tuple[str, ...]
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("validity assessment does not grant authority")


def assess_transport_validity(
    frozen: TransportValidityBinding,
    current: TransportValidityBinding,
) -> ValidityAssessment:
    if frozen.interpretation_id != current.interpretation_id:
        return ValidityAssessment(ValidityStatus.CANNOT_CHECK, ("interpretation_id",))
    checks = (
        ("source_epoch_id", ValidityStatus.EXPIRED_SOURCE_EPOCH),
        ("target_epoch_id", ValidityStatus.EXPIRED_TARGET_EPOCH),
        ("assumptions_digest", ValidityStatus.EXPIRED_ASSUMPTIONS),
        ("calibration_digest", ValidityStatus.EXPIRED_CALIBRATION),
        ("evaluator_digest", ValidityStatus.EXPIRED_EVALUATOR),
        ("resource_model_digest", ValidityStatus.EXPIRED_RESOURCE_MODEL),
        ("authority_policy_digest", ValidityStatus.EXPIRED_AUTHORITY_POLICY),
    )
    expired = tuple(
        field_name
        for field_name, _ in checks
        if getattr(frozen, field_name) != getattr(current, field_name)
    )
    if not expired:
        return ValidityAssessment(ValidityStatus.ACTIVE, ())
    if len(expired) > 1:
        return ValidityAssessment(ValidityStatus.MULTIPLE_EXPIRATIONS, expired)
    status = next(status for field_name, status in checks if field_name == expired[0])
    return ValidityAssessment(status, expired)


@dataclass(frozen=True, slots=True)
class TransportCertificate:
    certificate_id: str
    source_theory_id: str
    target_theory_id: str
    source_epoch_id: str
    target_epoch_id: str
    status: InterpretationStatus
    judgment_map: Mapping[str, str]
    uncertainty_bound: float
    semantic_loss_bound: float
    authority_ceiling: int
    source_ids: tuple[str, ...]
    violation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name, value in (
            ("certificate id", self.certificate_id),
            ("source theory id", self.source_theory_id),
            ("target theory id", self.target_theory_id),
            ("source epoch id", self.source_epoch_id),
            ("target epoch id", self.target_epoch_id),
        ):
            _nonblank(value, field_name=field_name)
        object.__setattr__(self, "status", InterpretationStatus(self.status))
        if self.uncertainty_bound < 0 or self.semantic_loss_bound < 0:
            raise ValueError("certificate bounds must be non-negative")
        if self.authority_ceiling < 0:
            raise ValueError("certificate authority ceiling must be non-negative")
        if not self.source_ids or any(not item.strip() for item in self.source_ids):
            raise ValueError("transport certificates require source identities")
        if not self.judgment_map:
            raise ValueError("transport certificates require a judgment correspondence")

    @property
    def valid(self) -> bool:
        return self.status in _VALID_INTERPRETATION_STATUSES and not self.violation_ids


@dataclass(frozen=True, slots=True)
class CompositionAssessment:
    status: CompositionStatus
    certificate: TransportCertificate | None
    violations: tuple[str, ...]
    authority_granted: bool = False
    novelty_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted or self.novelty_granted:
            raise ValueError("composition assessments are non-authorizing")


def _composition_status(left: InterpretationStatus, right: InterpretationStatus) -> CompositionStatus:
    order = (
        InterpretationStatus.EXACT_INTERPRETATION,
        InterpretationStatus.CONSERVATIVE_EXTENSION,
        InterpretationStatus.DECISION_RELATIVE_ADAPTATION,
        InterpretationStatus.SOUND_ABSTRACTION,
    )
    worst = max((left, right), key=order.index)
    return {
        InterpretationStatus.EXACT_INTERPRETATION: CompositionStatus.COMPOSED_EXACT,
        InterpretationStatus.CONSERVATIVE_EXTENSION: CompositionStatus.COMPOSED_CONSERVATIVE,
        InterpretationStatus.DECISION_RELATIVE_ADAPTATION: CompositionStatus.COMPOSED_DECISION_RELATIVE,
        InterpretationStatus.SOUND_ABSTRACTION: CompositionStatus.COMPOSED_SOUND_ABSTRACTION,
    }[worst]


def compose_transport_certificates(
    left: TransportCertificate,
    right: TransportCertificate,
    *,
    certificate_id: str,
) -> CompositionAssessment:
    if not left.valid or not right.valid:
        return CompositionAssessment(
            CompositionStatus.INVALID_INPUT_CERTIFICATE,
            None,
            ("one or more input certificates are invalid",),
        )
    if left.target_theory_id != right.source_theory_id or left.target_epoch_id != right.source_epoch_id:
        return CompositionAssessment(
            CompositionStatus.INVALID_NONCONTIGUOUS_CHAIN,
            None,
            ("theory or epoch chain is not contiguous",),
        )
    composed_judgments: dict[str, str] = {}
    missing: list[str] = []
    for source_judgment, middle_judgment in left.judgment_map.items():
        target_judgment = right.judgment_map.get(middle_judgment)
        if target_judgment is None:
            missing.append(source_judgment)
        else:
            composed_judgments[source_judgment] = target_judgment
    if missing:
        return CompositionAssessment(
            CompositionStatus.INVALID_JUDGMENT_CHAIN,
            None,
            ("judgment chain missing: " + ", ".join(sorted(missing)),),
        )
    composed_status = _composition_status(left.status, right.status)
    certificate = TransportCertificate(
        certificate_id=certificate_id,
        source_theory_id=left.source_theory_id,
        target_theory_id=right.target_theory_id,
        source_epoch_id=left.source_epoch_id,
        target_epoch_id=right.target_epoch_id,
        status={
            CompositionStatus.COMPOSED_EXACT: InterpretationStatus.EXACT_INTERPRETATION,
            CompositionStatus.COMPOSED_CONSERVATIVE: InterpretationStatus.CONSERVATIVE_EXTENSION,
            CompositionStatus.COMPOSED_DECISION_RELATIVE: InterpretationStatus.DECISION_RELATIVE_ADAPTATION,
            CompositionStatus.COMPOSED_SOUND_ABSTRACTION: InterpretationStatus.SOUND_ABSTRACTION,
        }[composed_status],
        judgment_map=composed_judgments,
        uncertainty_bound=left.uncertainty_bound + right.uncertainty_bound,
        semantic_loss_bound=left.semantic_loss_bound + right.semantic_loss_bound,
        authority_ceiling=min(left.authority_ceiling, right.authority_ceiling),
        source_ids=tuple(dict.fromkeys(left.source_ids + right.source_ids)),
    )
    return CompositionAssessment(composed_status, certificate, ())


@dataclass(frozen=True, slots=True)
class TargetAdaptation:
    adaptation_id: str
    source_interpretation_id: str
    target_interpretation_id: str
    shared_generalized_theory_id: str
    envelope_state_to_target_state: Mapping[State, State]
    envelope_action_to_target_action: Mapping[str, str]
    registered_envelope_judgment_ids: tuple[str, ...]
    calibration_ids: tuple[str, ...]
    validation_case_ids: tuple[str, ...]
    source_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("adaptation id", self.adaptation_id),
            ("source interpretation id", self.source_interpretation_id),
            ("target interpretation id", self.target_interpretation_id),
            ("shared generalized theory id", self.shared_generalized_theory_id),
        ):
            _nonblank(value, field_name=field_name)
        for field_name, values in (
            ("registered envelope judgment", self.registered_envelope_judgment_ids),
            ("calibration", self.calibration_ids),
            ("validation case", self.validation_case_ids),
            ("source", self.source_ids),
        ):
            if any(not value.strip() for value in values):
                raise ValueError(f"{field_name} ids may not be blank")
            if len(values) != len(set(values)):
                raise ValueError(f"{field_name} ids must be unique")
        if not self.registered_envelope_judgment_ids or not self.source_ids:
            raise ValueError("target adaptations require registered decisions and source identities")


@dataclass(frozen=True, slots=True)
class TargetAdaptationAssessment:
    status: AdaptationStatus
    shared_judgment_ids: tuple[str, ...]
    violations: tuple[str, ...]
    ready_for_target_evaluation: bool
    target_success_claimed: bool = False
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.target_success_claimed or self.authority_granted:
            raise ValueError("target adaptation can authorize evaluation, not target success or authority")


def assess_target_adaptation(
    source_interpretation: TheoryInterpretation,
    source_assessment: InterpretationAssessment,
    target_interpretation: TheoryInterpretation,
    target_assessment: InterpretationAssessment,
    adaptation: TargetAdaptation,
) -> TargetAdaptationAssessment:
    if not source_assessment.valid:
        return TargetAdaptationAssessment(
            AdaptationStatus.INVALID_SOURCE_INTERPRETATION,
            (),
            ("source interpretation is invalid",),
            False,
        )
    if not target_assessment.valid:
        return TargetAdaptationAssessment(
            AdaptationStatus.INVALID_TARGET_INTERPRETATION,
            (),
            ("target interpretation is invalid",),
            False,
        )
    if (
        adaptation.source_interpretation_id != source_interpretation.interpretation_id
        or adaptation.target_interpretation_id != target_interpretation.interpretation_id
        or adaptation.shared_generalized_theory_id != source_interpretation.generalized_theory_id
        or adaptation.shared_generalized_theory_id != target_interpretation.generalized_theory_id
    ):
        return TargetAdaptationAssessment(
            AdaptationStatus.CANNOT_CHECK,
            (),
            ("adaptation identities do not match supplied interpretations",),
            False,
        )

    source_generalized_judgments = {
        source_interpretation.judgment_map[judgment_id]
        for judgment_id in source_interpretation.context.registered_judgment_ids
        if judgment_id in source_interpretation.judgment_map
    }
    target_generalized_judgments = {
        target_interpretation.judgment_map[judgment_id]
        for judgment_id in target_interpretation.context.registered_judgment_ids
        if judgment_id in target_interpretation.judgment_map
    }
    shared = tuple(
        sorted(
            source_generalized_judgments
            & target_generalized_judgments
            & set(adaptation.registered_envelope_judgment_ids)
        )
    )
    if not shared:
        return TargetAdaptationAssessment(
            AdaptationStatus.NO_SHARED_REGISTERED_DECISION,
            (),
            ("source and target share no registered generalized decision",),
            False,
        )

    violations: list[str] = []
    for envelope_state, target_state in adaptation.envelope_state_to_target_state.items():
        if target_interpretation.state_map.get(target_state) != envelope_state:
            violations.append(
                f"target state {target_state!r} does not realize envelope state {envelope_state!r}"
            )
    for envelope_action, target_action in adaptation.envelope_action_to_target_action.items():
        if target_interpretation.action_map.get(target_action) != envelope_action:
            violations.append(
                f"target action {target_action} does not realize envelope action {envelope_action}"
            )
    if violations:
        return TargetAdaptationAssessment(
            AdaptationStatus.INVALID_TARGET_REALIZATION,
            shared,
            tuple(violations),
            False,
        )
    if not adaptation.calibration_ids:
        return TargetAdaptationAssessment(
            AdaptationStatus.MISSING_TARGET_CALIBRATION,
            shared,
            ("target-native calibration is required",),
            False,
        )
    if not adaptation.validation_case_ids:
        return TargetAdaptationAssessment(
            AdaptationStatus.MISSING_TARGET_VALIDATION,
            shared,
            ("target-native known-answer or hostile validation is required",),
            False,
        )
    return TargetAdaptationAssessment(
        AdaptationStatus.READY_FOR_PROTECTED_TARGET_EVALUATION,
        shared,
        (),
        True,
    )
