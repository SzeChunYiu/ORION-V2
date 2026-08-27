from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from types import MappingProxyType
from typing import Iterable, Mapping


class OutcomeSource(str, Enum):
    SELF = "SELF"
    DEPENDENT = "DEPENDENT"
    INDEPENDENT = "INDEPENDENT"
    DELAYED = "DELAYED"
    KNOWN_ANSWER = "KNOWN_ANSWER"


class CalibrationStatus(str, Enum):
    CALIBRATED_ON_BOUND_SET = "CALIBRATED_ON_BOUND_SET"
    MISCALIBRATED_ON_BOUND_SET = "MISCALIBRATED_ON_BOUND_SET"
    INSUFFICIENT_INDEPENDENT_CASES = "INSUFFICIENT_INDEPENDENT_CASES"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class CalibrationCase:
    case_id: str
    predicted_probability: float
    observed_outcome: bool | None
    outcome_source: OutcomeSource
    predictor_dependencies: frozenset[str] = frozenset()
    outcome_dependencies: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("calibration cases require identity")
        if not isfinite(self.predicted_probability) or not 0 <= self.predicted_probability <= 1:
            raise ValueError("predicted probability must be finite and within [0, 1]")
        object.__setattr__(self, "outcome_source", OutcomeSource(self.outcome_source))

    @property
    def independently_checkable(self) -> bool:
        valid_source = self.outcome_source in {
            OutcomeSource.INDEPENDENT,
            OutcomeSource.DELAYED,
            OutcomeSource.KNOWN_ANSWER,
        }
        return (
            self.observed_outcome is not None
            and valid_source
            and not bool(self.predictor_dependencies & self.outcome_dependencies)
        )


@dataclass(frozen=True, slots=True)
class CalibrationAssessment:
    status: CalibrationStatus
    independent_case_ids: tuple[str, ...]
    excluded_case_ids: tuple[str, ...]
    brier_score: float | None
    mean_predicted_probability: float | None
    observed_frequency: float | None
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("self-model calibration cannot grant scientific authority")


def assess_binary_calibration(
    cases: Iterable[CalibrationCase],
    *,
    minimum_independent_cases: int = 3,
    maximum_brier_score: float = 0.25,
) -> CalibrationAssessment:
    if minimum_independent_cases < 1:
        raise ValueError("minimum independent cases must be positive")
    if not 0 <= maximum_brier_score <= 1:
        raise ValueError("maximum Brier score must be within [0, 1]")
    frozen = tuple(cases)
    if not frozen:
        return CalibrationAssessment(CalibrationStatus.CANNOT_CHECK, (), (), None, None, None)
    ids = tuple(case.case_id for case in frozen)
    if len(ids) != len(set(ids)):
        raise ValueError("calibration case identities must be unique")
    independent = tuple(case for case in frozen if case.independently_checkable)
    excluded = tuple(case for case in frozen if not case.independently_checkable)
    if len(independent) < minimum_independent_cases:
        return CalibrationAssessment(
            CalibrationStatus.INSUFFICIENT_INDEPENDENT_CASES,
            tuple(case.case_id for case in independent),
            tuple(case.case_id for case in excluded),
            None,
            None,
            None,
        )
    outcomes = tuple(float(bool(case.observed_outcome)) for case in independent)
    brier = sum(
        (case.predicted_probability - outcome) ** 2
        for case, outcome in zip(independent, outcomes, strict=True)
    ) / len(independent)
    status = (
        CalibrationStatus.CALIBRATED_ON_BOUND_SET
        if brier <= maximum_brier_score
        else CalibrationStatus.MISCALIBRATED_ON_BOUND_SET
    )
    return CalibrationAssessment(
        status,
        tuple(case.case_id for case in independent),
        tuple(case.case_id for case in excluded),
        brier,
        sum(case.predicted_probability for case in independent) / len(independent),
        sum(outcomes) / len(outcomes),
    )


class MetaAction(str, Enum):
    PROCEED_PROVISIONALLY = "PROCEED_PROVISIONALLY"
    MORE_COMPUTE = "MORE_COMPUTE"
    EXTERNAL_REVIEW = "EXTERNAL_REVIEW"
    CHANGE_METHOD = "CHANGE_METHOD"
    CHANGE_REPRESENTATION = "CHANGE_REPRESENTATION"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class InquiryEstimate:
    probability_correct: float
    probability_method_adequate: float
    expected_value_more_compute: float
    expected_value_external_review: float
    calibration_status: CalibrationStatus

    def __post_init__(self) -> None:
        for name in ("probability_correct", "probability_method_adequate"):
            value = getattr(self, name)
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must be finite and within [0, 1]")
        for name in ("expected_value_more_compute", "expected_value_external_review"):
            if not isfinite(getattr(self, name)):
                raise ValueError(f"{name} must be finite")
        object.__setattr__(self, "calibration_status", CalibrationStatus(self.calibration_status))


@dataclass(frozen=True, slots=True)
class MetaActionReceipt:
    action: MetaAction
    reason: str
    evidence_obligation_discharged: bool = False
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.evidence_obligation_discharged or self.authority_granted:
            raise ValueError("meta-action selection cannot self-discharge evidence or authority")


def choose_meta_action(
    estimate: InquiryEstimate,
    *,
    hard_external_check_required: bool = False,
    external_review_available: bool = True,
    representation_limit_witnessed: bool = False,
    more_compute_cost: float = 0,
    proceed_probability: float = 0.8,
    adequate_method_probability: float = 0.7,
) -> MetaActionReceipt:
    if more_compute_cost < 0:
        raise ValueError("compute cost must be non-negative")
    if representation_limit_witnessed:
        return MetaActionReceipt(
            MetaAction.CHANGE_REPRESENTATION,
            "a protected insufficiency witness shows that local action cannot expose the required distinction",
        )
    if hard_external_check_required:
        action = MetaAction.EXTERNAL_REVIEW if external_review_available else MetaAction.CANNOT_CHECK
        return MetaActionReceipt(action, "the obligation requires an external check")
    if estimate.calibration_status is not CalibrationStatus.CALIBRATED_ON_BOUND_SET:
        if external_review_available and estimate.expected_value_external_review > 0:
            return MetaActionReceipt(MetaAction.EXTERNAL_REVIEW, "the inquiry self-model is not independently calibrated")
        return MetaActionReceipt(MetaAction.CANNOT_CHECK, "the inquiry self-model is not independently calibrated")
    compute_value = estimate.expected_value_more_compute - more_compute_cost
    if estimate.probability_method_adequate < adequate_method_probability:
        if external_review_available and estimate.expected_value_external_review >= max(compute_value, 0) and estimate.expected_value_external_review > 0:
            return MetaActionReceipt(MetaAction.EXTERNAL_REVIEW, "method adequacy is doubtful and external review has highest value")
        return MetaActionReceipt(MetaAction.CHANGE_METHOD, "the calibrated self-model predicts method inadequacy")
    if compute_value > 0:
        return MetaActionReceipt(MetaAction.MORE_COMPUTE, "additional computation has positive expected value")
    if external_review_available and estimate.expected_value_external_review > max(compute_value, 0):
        return MetaActionReceipt(MetaAction.EXTERNAL_REVIEW, "external review has higher positive expected value")
    if estimate.probability_correct >= proceed_probability:
        return MetaActionReceipt(MetaAction.PROCEED_PROVISIONALLY, "calibrated correctness supports provisional continuation")
    return MetaActionReceipt(MetaAction.CANNOT_CHECK, "no admissible action closes the remaining uncertainty")


class AttributionStatus(str, Enum):
    ESTABLISHED = "ESTABLISHED"
    PLAUSIBLE = "PLAUSIBLE"
    UNRESOLVED = "UNRESOLVED"
    CONTRADICTED = "CONTRADICTED"


class LessonTransferStatus(str, Enum):
    APPLY_WITHIN_SCOPE = "APPLY_WITHIN_SCOPE"
    REVALIDATE_BEFORE_USE = "REVALIDATE_BEFORE_USE"
    REJECT_TRANSFER = "REJECT_TRANSFER"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class FailureLesson:
    lesson_id: str
    reproduced: bool
    attribution_status: AttributionStatus
    cause: str
    correction: str
    regression_check_passed: bool
    source_context: str
    explicit_transfer_scope: frozenset[str] = frozenset()
    counterexample_contexts: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.lesson_id, self.cause, self.correction, self.source_context)):
            raise ValueError("failure lessons require identity, cause, correction and source context")
        object.__setattr__(self, "attribution_status", AttributionStatus(self.attribution_status))


@dataclass(frozen=True, slots=True)
class LessonTransferAssessment:
    status: LessonTransferStatus
    reason: str
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("a failure lesson cannot grant external authority")


def assess_failure_lesson_transfer(
    lesson: FailureLesson,
    target_context: str,
    *,
    cause_preserved: bool | None = None,
) -> LessonTransferAssessment:
    if not target_context.strip():
        raise ValueError("target context is required")
    if not lesson.reproduced or not lesson.regression_check_passed:
        return LessonTransferAssessment(LessonTransferStatus.CANNOT_CHECK, "the failure or correction was not independently reproduced")
    if lesson.attribution_status in {AttributionStatus.UNRESOLVED, AttributionStatus.CONTRADICTED}:
        return LessonTransferAssessment(LessonTransferStatus.CANNOT_CHECK, "causal attribution is not established")
    if target_context in lesson.counterexample_contexts or cause_preserved is False:
        return LessonTransferAssessment(LessonTransferStatus.REJECT_TRANSFER, "a counterexample or changed cause blocks transfer")
    if target_context == lesson.source_context or target_context in lesson.explicit_transfer_scope:
        return LessonTransferAssessment(LessonTransferStatus.APPLY_WITHIN_SCOPE, "target is inside the validated transfer scope")
    return LessonTransferAssessment(LessonTransferStatus.REVALIDATE_BEFORE_USE, "target lies outside the validated transfer scope")


@dataclass(frozen=True, slots=True)
class SurpriseVector:
    predictive: float = 0
    semantic: float = 0
    causal: float = 0
    source: float = 0
    evaluator: float = 0
    model_class: float = 0
    value: float = 0
    state_transition: float = 0

    def __post_init__(self) -> None:
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError("surprise coordinates must be finite and within [0, 1]")

    @property
    def maximum(self) -> float:
        return max(getattr(self, name) for name in self.__dataclass_fields__)


class EncounterStatus(str, Enum):
    RETAIN_FOR_TEST = "RETAIN_FOR_TEST"
    RETAIN_UNRESOLVED = "RETAIN_UNRESOLVED"
    IGNORE_AS_NOISE = "IGNORE_AS_NOISE"
    OUT_OF_BUDGET = "OUT_OF_BUDGET"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class EncounterCandidate:
    encounter_id: str
    source_id: str
    surprise: SurpriseVector
    cross_problem_relevance: float
    noise_risk: float
    reproducible: bool
    discriminator_available: bool
    estimated_followup_cost: float

    def __post_init__(self) -> None:
        if not self.encounter_id.strip() or not self.source_id.strip():
            raise ValueError("encounters require identity and source")
        for name in ("cross_problem_relevance", "noise_risk"):
            value = getattr(self, name)
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must be finite and within [0, 1]")
        if not isfinite(self.estimated_followup_cost) or self.estimated_followup_cost < 0:
            raise ValueError("follow-up cost must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class EncounterAssessment:
    status: EncounterStatus
    reason: str
    claim_authorized: bool = False
    agenda_authorized: bool = False

    def __post_init__(self) -> None:
        if self.claim_authorized or self.agenda_authorized:
            raise ValueError("surprise cannot authorize a claim or research agenda")


def assess_encounter(
    candidate: EncounterCandidate,
    *,
    followup_budget: float,
    minimum_relevance: float = 0.6,
    maximum_noise_risk: float = 0.7,
    minimum_surprise: float = 0.5,
) -> EncounterAssessment:
    if followup_budget < 0:
        raise ValueError("follow-up budget must be non-negative")
    if candidate.noise_risk >= maximum_noise_risk and not candidate.reproducible:
        return EncounterAssessment(EncounterStatus.IGNORE_AS_NOISE, "high-noise unreproduced surprise has no reusable structure")
    if candidate.cross_problem_relevance < minimum_relevance or candidate.surprise.maximum < minimum_surprise:
        return EncounterAssessment(EncounterStatus.IGNORE_AS_NOISE, "encounter lacks bounded surprise or cross-problem relevance")
    if candidate.estimated_followup_cost > followup_budget:
        return EncounterAssessment(EncounterStatus.OUT_OF_BUDGET, "candidate exceeds the declared follow-up budget")
    if candidate.reproducible and candidate.discriminator_available:
        return EncounterAssessment(EncounterStatus.RETAIN_FOR_TEST, "candidate has a reproducible encounter and a bounded discriminator")
    return EncounterAssessment(EncounterStatus.RETAIN_UNRESOLVED, "candidate may matter but lacks reproduction or a discriminator")


class CompetenceTransferStatus(str, Enum):
    VERIFIED_WITHIN_DEMONSTRATED_RANGE = "VERIFIED_WITHIN_DEMONSTRATED_RANGE"
    TEXT_ONLY_UNVERIFIED = "TEXT_ONLY_UNVERIFIED"
    REVALIDATE_CONTEXT_CHANGE = "REVALIDATE_CONTEXT_CHANGE"
    NOT_TRANSFERRED = "NOT_TRANSFERRED"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class CompetenceReceipt:
    receipt_id: str
    task_family: str
    instruction_identity: str
    demonstrated_contexts: frozenset[str] = frozenset()
    state_discriminators: frozenset[str] = frozenset()
    recovery_cases: frozenset[str] = frozenset()
    failure_contexts: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.receipt_id, self.task_family, self.instruction_identity)):
            raise ValueError("competence receipts require receipt, task and instruction identity")


@dataclass(frozen=True, slots=True)
class CompetenceTransferAssessment:
    status: CompetenceTransferStatus
    reason: str
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("competence receipts cannot grant external authority")


def assess_competence_transfer(
    receipt: CompetenceReceipt,
    *,
    target_task_family: str,
    target_context: str,
    context_relation_certified: bool = False,
) -> CompetenceTransferAssessment:
    if not target_task_family.strip() or not target_context.strip():
        raise ValueError("target task family and context are required")
    if target_task_family != receipt.task_family:
        return CompetenceTransferAssessment(CompetenceTransferStatus.CANNOT_CHECK, "target task family differs")
    if target_context in receipt.failure_contexts:
        return CompetenceTransferAssessment(CompetenceTransferStatus.NOT_TRANSFERRED, "target is an observed failure context")
    if not receipt.demonstrated_contexts or not receipt.state_discriminators:
        return CompetenceTransferAssessment(CompetenceTransferStatus.TEXT_ONLY_UNVERIFIED, "instruction identity exists but competence has not been demonstrated")
    if target_context in receipt.demonstrated_contexts:
        return CompetenceTransferAssessment(CompetenceTransferStatus.VERIFIED_WITHIN_DEMONSTRATED_RANGE, "target lies inside demonstrated range")
    reason = "context relation is certified, but target competence still needs validation" if context_relation_certified else "target lies outside demonstrated range"
    return CompetenceTransferAssessment(CompetenceTransferStatus.REVALIDATE_CONTEXT_CHANGE, reason)


class ReviewIndependence(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    DEPENDENT = "DEPENDENT"
    UNKNOWN = "UNKNOWN"


class CriticismOutcome(str, Enum):
    UPTAKE = "UPTAKE"
    EVIDENCE_BASED_REJECTION = "EVIDENCE_BASED_REJECTION"
    REVIEW_THEATRE = "REVIEW_THEATRE"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True, slots=True)
class CriticismReceipt:
    criticism_id: str
    claim_id: str
    critic_id: str
    objection: str
    target_assumption: str
    critic_dependencies: frozenset[str] = frozenset()
    subject_dependencies: frozenset[str] = frozenset()
    response_evidence_ids: frozenset[str] = frozenset()
    state_delta: frozenset[str] = frozenset()
    reason_no_change: str = ""

    def __post_init__(self) -> None:
        values = (self.criticism_id, self.claim_id, self.critic_id, self.objection, self.target_assumption)
        if not all(value.strip() for value in values):
            raise ValueError("criticism receipts require identities, objection and target assumption")


@dataclass(frozen=True, slots=True)
class CriticismAssessment:
    independence: ReviewIndependence
    outcome: CriticismOutcome
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("criticism does not grant authority")


def assess_criticism(receipt: CriticismReceipt) -> CriticismAssessment:
    if not receipt.critic_dependencies or not receipt.subject_dependencies:
        independence = ReviewIndependence.UNKNOWN
    elif receipt.critic_dependencies & receipt.subject_dependencies:
        independence = ReviewIndependence.DEPENDENT
    else:
        independence = ReviewIndependence.INDEPENDENT
    if receipt.state_delta:
        outcome = CriticismOutcome.UPTAKE
    elif receipt.response_evidence_ids and receipt.reason_no_change.strip():
        outcome = CriticismOutcome.EVIDENCE_BASED_REJECTION
    elif receipt.reason_no_change.strip():
        outcome = CriticismOutcome.UNRESOLVED
    else:
        outcome = CriticismOutcome.REVIEW_THEATRE
    return CriticismAssessment(independence, outcome)


class DistributedStateStatus(str, Enum):
    COMPLETE_AT_DECISION = "COMPLETE_AT_DECISION"
    HANDOFF_LOSS = "HANDOFF_LOSS"
    SOURCE_STATE_MISSING = "SOURCE_STATE_MISSING"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class DistributedEpisode:
    episode_id: str
    decision_component_id: str
    required_state_at_decision: frozenset[str]
    available_state_by_component: Mapping[str, frozenset[str]]

    def __post_init__(self) -> None:
        if not self.episode_id.strip() or not self.decision_component_id.strip():
            raise ValueError("distributed episodes require episode and decision-component identity")
        if not self.required_state_at_decision:
            raise ValueError("at least one decision-relevant state item is required")
        frozen = {key: frozenset(value) for key, value in self.available_state_by_component.items()}
        object.__setattr__(self, "available_state_by_component", MappingProxyType(frozen))


@dataclass(frozen=True, slots=True)
class DistributedStateAssessment:
    status: DistributedStateStatus
    missing_state: tuple[str, ...]
    source_components: tuple[str, ...]
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("distributed-state assessment cannot grant authority")


def assess_distributed_state(episode: DistributedEpisode) -> DistributedStateAssessment:
    decision_state = episode.available_state_by_component.get(episode.decision_component_id)
    if decision_state is None:
        return DistributedStateAssessment(
            DistributedStateStatus.CANNOT_CHECK,
            tuple(sorted(episode.required_state_at_decision)),
            (),
        )
    missing = episode.required_state_at_decision - decision_state
    if not missing:
        return DistributedStateAssessment(
            DistributedStateStatus.COMPLETE_AT_DECISION,
            (),
            (episode.decision_component_id,),
        )
    source_components = tuple(
        sorted(
            component_id
            for component_id, state in episode.available_state_by_component.items()
            if component_id != episode.decision_component_id and bool(state & missing)
        )
    )
    union_state = frozenset().union(*episode.available_state_by_component.values())
    truly_missing = missing - union_state
    if truly_missing:
        return DistributedStateAssessment(
            DistributedStateStatus.SOURCE_STATE_MISSING,
            tuple(sorted(truly_missing)),
            source_components,
        )
    return DistributedStateAssessment(
        DistributedStateStatus.HANDOFF_LOSS,
        tuple(sorted(missing)),
        source_components,
    )
