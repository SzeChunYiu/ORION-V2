from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Iterable


class TeachingScope(str, Enum):
    EXHAUSTIVE = "EXHAUSTIVE"
    NONEXHAUSTIVE = "NONEXHAUSTIVE"
    UNSPECIFIED = "UNSPECIFIED"
    SAFETY_BOUNDED = "SAFETY_BOUNDED"


class PedagogicalStatus(str, Enum):
    EXHAUSTIVE_SCOPE_VALID = "EXHAUSTIVE_SCOPE_VALID"
    EXHAUSTIVE_SCOPE_CONTRADICTED = "EXHAUSTIVE_SCOPE_CONTRADICTED"
    EXPLORATION_PRESERVED = "EXPLORATION_PRESERVED"
    INSTRUCTION_INDUCED_SEARCH_SUPPRESSION = "INSTRUCTION_INDUCED_SEARCH_SUPPRESSION"
    SAFETY_RESTRICTION_RESPECTED = "SAFETY_RESTRICTION_RESPECTED"
    SAFETY_RESTRICTION_VIOLATED = "SAFETY_RESTRICTION_VIOLATED"
    NO_HIDDEN_ALTERNATIVE = "NO_HIDDEN_ALTERNATIVE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class PedagogicalSampleReceipt:
    sample_id: str
    teacher_id: str
    demonstrated_items: frozenset[str]
    available_valid_items: frozenset[str]
    teaching_scope: TeachingScope
    authorized_exploration_items: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.sample_id.strip() or not self.teacher_id.strip():
            raise ValueError("pedagogical samples require sample and teacher identity")
        if not self.demonstrated_items:
            raise ValueError("at least one demonstrated item is required")
        object.__setattr__(self, "teaching_scope", TeachingScope(self.teaching_scope))
        if not self.demonstrated_items <= self.available_valid_items:
            raise ValueError("demonstrated items must be valid items")
        if self.authorized_exploration_items - self.available_valid_items:
            raise ValueError("authorized exploration items must be valid items")


@dataclass(frozen=True, slots=True)
class PedagogicalAssessment:
    status: PedagogicalStatus
    hidden_valid_items: tuple[str, ...]
    claim_authorized: bool = False
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.claim_authorized or self.authority_granted:
            raise ValueError("pedagogical sampling cannot authorize truth or agenda authority")


def assess_pedagogical_sample(
    receipt: PedagogicalSampleReceipt,
    learner_considered_items: frozenset[str],
) -> PedagogicalAssessment:
    hidden = receipt.available_valid_items - receipt.demonstrated_items
    if receipt.teaching_scope is TeachingScope.EXHAUSTIVE:
        status = (
            PedagogicalStatus.EXHAUSTIVE_SCOPE_VALID
            if not hidden
            else PedagogicalStatus.EXHAUSTIVE_SCOPE_CONTRADICTED
        )
        return PedagogicalAssessment(status, tuple(sorted(hidden)))
    if receipt.teaching_scope is TeachingScope.SAFETY_BOUNDED:
        outside = learner_considered_items - (
            receipt.demonstrated_items | receipt.authorized_exploration_items
        )
        status = (
            PedagogicalStatus.SAFETY_RESTRICTION_VIOLATED
            if outside
            else PedagogicalStatus.SAFETY_RESTRICTION_RESPECTED
        )
        return PedagogicalAssessment(status, tuple(sorted(hidden)))
    if not hidden:
        return PedagogicalAssessment(PedagogicalStatus.NO_HIDDEN_ALTERNATIVE, ())
    if learner_considered_items & hidden:
        return PedagogicalAssessment(
            PedagogicalStatus.EXPLORATION_PRESERVED, tuple(sorted(hidden))
        )
    return PedagogicalAssessment(
        PedagogicalStatus.INSTRUCTION_INDUCED_SEARCH_SUPPRESSION,
        tuple(sorted(hidden)),
    )


class ReviewStage(str, Enum):
    BLIND_INITIAL = "BLIND_INITIAL"
    AFTER_COMMUNICATION = "AFTER_COMMUNICATION"
    EDITOR_SYNTHESIS = "EDITOR_SYNTHESIS"


class PanelIndependenceStatus(str, Enum):
    INDEPENDENT_INITIAL_PANEL = "INDEPENDENT_INITIAL_PANEL"
    DEPENDENT_INITIAL_PANEL = "DEPENDENT_INITIAL_PANEL"
    INSUFFICIENT_BLIND_INITIAL = "INSUFFICIENT_BLIND_INITIAL"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class ReviewerJudgment:
    judgment_id: str
    reviewer_id: str
    stage: ReviewStage
    conclusion: str
    dependencies: frozenset[str]
    messages_seen: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (self.judgment_id, self.reviewer_id, self.conclusion)
        ):
            raise ValueError("reviewer judgments require identities and conclusion")
        object.__setattr__(self, "stage", ReviewStage(self.stage))


@dataclass(frozen=True, slots=True)
class PanelIndependenceAssessment:
    status: PanelIndependenceStatus
    blind_initial_judgment_ids: tuple[str, ...]
    excluded_later_judgment_ids: tuple[str, ...]
    dependency_clusters: tuple[tuple[str, ...], ...]
    independent_support_count: int
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("panel independence cannot grant scientific authority")


def _dependency_clusters(
    judgments: tuple[ReviewerJudgment, ...],
) -> tuple[tuple[str, ...], ...]:
    remaining = set(range(len(judgments)))
    clusters: list[tuple[str, ...]] = []
    while remaining:
        seed = remaining.pop()
        component = {seed}
        frontier = [seed]
        while frontier:
            current = frontier.pop()
            current_dependencies = judgments[current].dependencies
            connected = {
                other
                for other in remaining
                if current_dependencies & judgments[other].dependencies
            }
            remaining -= connected
            component |= connected
            frontier.extend(connected)
        clusters.append(
            tuple(sorted(judgments[index].judgment_id for index in component))
        )
    return tuple(sorted(clusters))


def assess_panel_independence(
    judgments: Iterable[ReviewerJudgment],
) -> PanelIndependenceAssessment:
    frozen = tuple(judgments)
    if not frozen:
        return PanelIndependenceAssessment(
            PanelIndependenceStatus.CANNOT_CHECK, (), (), (), 0
        )
    ids = tuple(judgment.judgment_id for judgment in frozen)
    if len(ids) != len(set(ids)):
        raise ValueError("judgment identities must be unique")
    initial = tuple(
        judgment
        for judgment in frozen
        if judgment.stage is ReviewStage.BLIND_INITIAL
    )
    later = tuple(
        judgment
        for judgment in frozen
        if judgment.stage is not ReviewStage.BLIND_INITIAL
    )
    if len(initial) < 2:
        return PanelIndependenceAssessment(
            PanelIndependenceStatus.INSUFFICIENT_BLIND_INITIAL,
            tuple(judgment.judgment_id for judgment in initial),
            tuple(judgment.judgment_id for judgment in later),
            _dependency_clusters(initial) if initial else (),
            len(initial),
        )
    clusters = _dependency_clusters(initial)
    blind_violation = any(judgment.messages_seen for judgment in initial)
    status = (
        PanelIndependenceStatus.DEPENDENT_INITIAL_PANEL
        if blind_violation or len(clusters) < len(initial)
        else PanelIndependenceStatus.INDEPENDENT_INITIAL_PANEL
    )
    return PanelIndependenceAssessment(
        status,
        tuple(judgment.judgment_id for judgment in initial),
        tuple(judgment.judgment_id for judgment in later),
        clusters,
        len(clusters),
    )


class MemoryRevisionStatus(str, Enum):
    WORKING_STATE_REVISED_ARCHIVE_PRESERVED = (
        "WORKING_STATE_REVISED_ARCHIVE_PRESERVED"
    )
    ARCHIVE_HISTORY_MUTATED = "ARCHIVE_HISTORY_MUTATED"
    CLAIM_CHANGED_WITHOUT_NEW_EVIDENCE = "CLAIM_CHANGED_WITHOUT_NEW_EVIDENCE"
    CLAIM_CHANGED_WITHOUT_REVALIDATION = "CLAIM_CHANGED_WITHOUT_REVALIDATION"
    NO_MATERIAL_CHANGE = "NO_MATERIAL_CHANGE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class MemoryRevisionReceipt:
    receipt_id: str
    archive_before_digest: str
    archive_after_digest: str
    working_state_before_digest: str
    working_state_after_digest: str
    retrieved_item_ids: frozenset[str] = frozenset()
    new_evidence_ids: frozenset[str] = frozenset()
    changed_claim_ids: frozenset[str] = frozenset()
    revalidated_claim_ids: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        values = (
            self.receipt_id,
            self.archive_before_digest,
            self.archive_after_digest,
            self.working_state_before_digest,
            self.working_state_after_digest,
        )
        if not all(value.strip() for value in values):
            raise ValueError("memory revision receipts require identities and digests")
        if self.revalidated_claim_ids - self.changed_claim_ids:
            raise ValueError("only changed claims can be marked revalidated")


@dataclass(frozen=True, slots=True)
class MemoryRevisionAssessment:
    status: MemoryRevisionStatus
    unresolved_claim_ids: tuple[str, ...]
    scientific_truth_granted: bool = False

    def __post_init__(self) -> None:
        if self.scientific_truth_granted:
            raise ValueError("memory revision cannot grant scientific truth")


def assess_memory_revision(
    receipt: MemoryRevisionReceipt,
) -> MemoryRevisionAssessment:
    if receipt.archive_before_digest != receipt.archive_after_digest:
        return MemoryRevisionAssessment(
            MemoryRevisionStatus.ARCHIVE_HISTORY_MUTATED, ()
        )
    if receipt.changed_claim_ids and not receipt.new_evidence_ids:
        return MemoryRevisionAssessment(
            MemoryRevisionStatus.CLAIM_CHANGED_WITHOUT_NEW_EVIDENCE,
            tuple(sorted(receipt.changed_claim_ids)),
        )
    unresolved = receipt.changed_claim_ids - receipt.revalidated_claim_ids
    if unresolved:
        return MemoryRevisionAssessment(
            MemoryRevisionStatus.CLAIM_CHANGED_WITHOUT_REVALIDATION,
            tuple(sorted(unresolved)),
        )
    if receipt.working_state_before_digest != receipt.working_state_after_digest:
        return MemoryRevisionAssessment(
            MemoryRevisionStatus.WORKING_STATE_REVISED_ARCHIVE_PRESERVED, ()
        )
    return MemoryRevisionAssessment(MemoryRevisionStatus.NO_MATERIAL_CHANGE, ())


class IncubationStatus(str, Enum):
    PROPOSAL_ONLY = "PROPOSAL_ONLY"
    EXTERNAL_EVIDENCE_CONTAMINATED = "EXTERNAL_EVIDENCE_CONTAMINATED"
    PROTECTED_STATE_CHANGED_WITHOUT_EVIDENCE = (
        "PROTECTED_STATE_CHANGED_WITHOUT_EVIDENCE"
    )
    EXTERNALLY_TESTED = "EXTERNALLY_TESTED"
    NO_CANDIDATE = "NO_CANDIDATE"


@dataclass(frozen=True, slots=True)
class IncubationReceipt:
    receipt_id: str
    frozen_input_digest: str
    protected_claims_before: frozenset[str]
    protected_claims_after: frozenset[str]
    candidate_ids: frozenset[str] = frozenset()
    external_evidence_during_interval: frozenset[str] = frozenset()
    external_test_ids_after_interval: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.receipt_id.strip() or not self.frozen_input_digest.strip():
            raise ValueError("incubation receipts require identity and frozen input")


@dataclass(frozen=True, slots=True)
class IncubationAssessment:
    status: IncubationStatus
    candidate_ids: tuple[str, ...]
    candidate_authorized_as_evidence: bool = False

    def __post_init__(self) -> None:
        if self.candidate_authorized_as_evidence:
            raise ValueError("incubation cannot make internal candidates evidence")


def assess_incubation(receipt: IncubationReceipt) -> IncubationAssessment:
    candidates = tuple(sorted(receipt.candidate_ids))
    if receipt.external_evidence_during_interval:
        return IncubationAssessment(
            IncubationStatus.EXTERNAL_EVIDENCE_CONTAMINATED, candidates
        )
    if receipt.protected_claims_before != receipt.protected_claims_after:
        return IncubationAssessment(
            IncubationStatus.PROTECTED_STATE_CHANGED_WITHOUT_EVIDENCE, candidates
        )
    if not candidates:
        return IncubationAssessment(IncubationStatus.NO_CANDIDATE, ())
    if receipt.external_test_ids_after_interval:
        return IncubationAssessment(IncubationStatus.EXTERNALLY_TESTED, candidates)
    return IncubationAssessment(IncubationStatus.PROPOSAL_ONLY, candidates)


class PolicyHabitStatus(str, Enum):
    CONTEXT_CURRENT = "CONTEXT_CURRENT"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"
    REVALUATED_AND_ADAPTED = "REVALUATED_AND_ADAPTED"
    POLICY_HABIT_OUTLIVED_CONTEXT = "POLICY_HABIT_OUTLIVED_CONTEXT"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class PolicyHabitReceipt:
    receipt_id: str
    policy_id: str
    original_context_epoch: str
    current_context_epoch: str
    training_repetitions: int
    outcome_devalued: bool
    revaluation_test_run: bool
    policy_response_changed: bool

    def __post_init__(self) -> None:
        values = (
            self.receipt_id,
            self.policy_id,
            self.original_context_epoch,
            self.current_context_epoch,
        )
        if not all(value.strip() for value in values):
            raise ValueError("policy habit receipts require identities and epochs")
        if self.training_repetitions < 0:
            raise ValueError("training repetitions must be non-negative")


@dataclass(frozen=True, slots=True)
class PolicyHabitAssessment:
    status: PolicyHabitStatus
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("habit assessment cannot grant authority")


def assess_policy_habit(
    receipt: PolicyHabitReceipt,
) -> PolicyHabitAssessment:
    changed_context = (
        receipt.original_context_epoch != receipt.current_context_epoch
        or receipt.outcome_devalued
    )
    if not changed_context:
        return PolicyHabitAssessment(PolicyHabitStatus.CONTEXT_CURRENT)
    if not receipt.revaluation_test_run:
        return PolicyHabitAssessment(PolicyHabitStatus.REVALIDATION_REQUIRED)
    if receipt.policy_response_changed:
        return PolicyHabitAssessment(PolicyHabitStatus.REVALUATED_AND_ADAPTED)
    return PolicyHabitAssessment(
        PolicyHabitStatus.POLICY_HABIT_OUTLIVED_CONTEXT
    )


class CounterfactualStatus(str, Enum):
    PROPOSAL_ONLY = "PROPOSAL_ONLY"
    SIMULATION_OBSERVATION_LAUNDERING = "SIMULATION_OBSERVATION_LAUNDERING"
    EXTERNALLY_TESTED = "EXTERNALLY_TESTED"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class CounterfactualProposal:
    proposal_id: str
    model_id: str
    intervention: str
    predicted_outcome: str
    assumptions: frozenset[str]
    represented_as_observation: bool = False
    external_observation_ids: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        values = (
            self.proposal_id,
            self.model_id,
            self.intervention,
            self.predicted_outcome,
        )
        if not all(value.strip() for value in values):
            raise ValueError("counterfactual proposals require identities and prediction")


@dataclass(frozen=True, slots=True)
class CounterfactualAssessment:
    status: CounterfactualStatus
    scientific_truth_granted: bool = False

    def __post_init__(self) -> None:
        if self.scientific_truth_granted:
            raise ValueError("counterfactual assessment cannot grant truth")


def assess_counterfactual(
    proposal: CounterfactualProposal,
) -> CounterfactualAssessment:
    if proposal.represented_as_observation:
        return CounterfactualAssessment(
            CounterfactualStatus.SIMULATION_OBSERVATION_LAUNDERING
        )
    if not proposal.assumptions:
        return CounterfactualAssessment(CounterfactualStatus.CANNOT_CHECK)
    if proposal.external_observation_ids:
        return CounterfactualAssessment(CounterfactualStatus.EXTERNALLY_TESTED)
    return CounterfactualAssessment(CounterfactualStatus.PROPOSAL_ONLY)


class ObserverCouplingStatus(str, Enum):
    COUPLING_CANDIDATE = "COUPLING_CANDIDATE"
    STABLE_CONTROL = "STABLE_CONTROL"
    PERFORMATIVITY_UNSUPPORTED = "PERFORMATIVITY_UNSUPPORTED"
    CONFOUNDED_CHANGE = "CONFOUNDED_CHANGE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class ObserverCouplingReceipt:
    receipt_id: str
    observer_action_id: str
    causal_pathway: str
    target_before: float
    target_after: float
    stable_control_before: float
    stable_control_after: float
    minimum_material_change: float

    def __post_init__(self) -> None:
        if not self.receipt_id.strip() or not self.observer_action_id.strip():
            raise ValueError("observer coupling receipts require identity")
        for name in (
            "target_before",
            "target_after",
            "stable_control_before",
            "stable_control_after",
            "minimum_material_change",
        ):
            if not isfinite(getattr(self, name)):
                raise ValueError(f"{name} must be finite")
        if self.minimum_material_change < 0:
            raise ValueError("minimum material change must be non-negative")


@dataclass(frozen=True, slots=True)
class ObserverCouplingAssessment:
    status: ObserverCouplingStatus
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("observer coupling cannot grant authority")


def assess_observer_coupling(
    receipt: ObserverCouplingReceipt,
) -> ObserverCouplingAssessment:
    if not receipt.causal_pathway.strip():
        return ObserverCouplingAssessment(ObserverCouplingStatus.CANNOT_CHECK)
    target_change = abs(receipt.target_after - receipt.target_before)
    control_change = abs(
        receipt.stable_control_after - receipt.stable_control_before
    )
    target_material = target_change >= receipt.minimum_material_change
    control_material = control_change >= receipt.minimum_material_change
    if target_material and not control_material:
        return ObserverCouplingAssessment(
            ObserverCouplingStatus.COUPLING_CANDIDATE
        )
    if not target_material and not control_material:
        return ObserverCouplingAssessment(ObserverCouplingStatus.STABLE_CONTROL)
    if not target_material and control_material:
        return ObserverCouplingAssessment(
            ObserverCouplingStatus.PERFORMATIVITY_UNSUPPORTED
        )
    return ObserverCouplingAssessment(ObserverCouplingStatus.CONFOUNDED_CHANGE)
