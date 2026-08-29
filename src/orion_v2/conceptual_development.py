"""Reference semantics for conceptual development and transfer discovery.

This module deliberately does *not* encode domain-specific lessons.  It provides
content-neutral machinery for:

1. representing domain structure;
2. inducing relational abstractions from repeated cross-domain structure;
3. retrieving candidate transfers for a new target;
4. admitting or rejecting transfer hypotheses under native-recovery,
   counterexample and parent-sufficiency gates; and
5. versioning conceptual transitions without granting scientific truth.

Physics, biology, mathematics, chemistry, software engineering and other domains
may contribute donor cases.  Their substantive lessons must be discovered from
source-bound structures and survive protected evaluation rather than being
hard-programmed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from itertools import combinations
from typing import Iterable


def _unique_nonblank(values: Iterable[str], *, name: str) -> tuple[str, ...]:
    result = tuple(values)
    if any(not value.strip() for value in result):
        raise ValueError(f"{name} may not contain blank identities")
    if len(result) != len(set(result)):
        raise ValueError(f"{name} identities must be unique")
    return result


def _jaccard(left: Iterable[str], right: Iterable[str]) -> float:
    a, b = set(left), set(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class ConceptTransitionKind(StrEnum):
    SPECIALIZE = "SPECIALIZE"
    GENERALIZE = "GENERALIZE"
    SPLIT = "SPLIT"
    MERGE = "MERGE"
    BRIDGE = "BRIDGE"
    REPARAMETERIZE = "REPARAMETERIZE"
    REVISE = "REVISE"
    DEPRECATE = "DEPRECATE"


class TransferDiscoveryStatus(StrEnum):
    BLOCKED_NATIVE_RECOVERY = "BLOCKED_NATIVE_RECOVERY"
    BLOCKED_UNFROZEN_PREDICTION = "BLOCKED_UNFROZEN_PREDICTION"
    FALSE_ANALOGY_REJECTED = "FALSE_ANALOGY_REJECTED"
    PARENT_SUFFICIENT = "PARENT_SUFFICIENT"
    CANNOT_CHECK = "CANNOT_CHECK"
    PROTECTED_TRANSFER_RESIDUAL = "PROTECTED_TRANSFER_RESIDUAL"
    INDEPENDENTLY_ADJUDICATED_TRANSFER_RESIDUAL = (
        "INDEPENDENTLY_ADJUDICATED_TRANSFER_RESIDUAL"
    )


class ConceptTransitionStatus(StrEnum):
    BLOCKED_PARENT_RECOVERY = "BLOCKED_PARENT_RECOVERY"
    BLOCKED_NATIVE_FIDELITY = "BLOCKED_NATIVE_FIDELITY"
    BLOCKED_SCOPE_OR_LOSS_AUDIT = "BLOCKED_SCOPE_OR_LOSS_AUDIT"
    BLOCKED_MEASUREMENT_OR_AUTHORITY = "BLOCKED_MEASUREMENT_OR_AUTHORITY"
    NO_SCIENTIFIC_RESIDUAL = "NO_SCIENTIFIC_RESIDUAL"
    READY_FOR_PROTECTED_EVALUATION = "READY_FOR_PROTECTED_EVALUATION"
    PROTECTED_CONCEPTUAL_RESIDUAL = "PROTECTED_CONCEPTUAL_RESIDUAL"
    INDEPENDENTLY_ADJUDICATED_CONCEPTUAL_RESIDUAL = (
        "INDEPENDENTLY_ADJUDICATED_CONCEPTUAL_RESIDUAL"
    )


@dataclass(frozen=True, slots=True)
class DomainStructure:
    """Source-bound structural description used for transfer discovery.

    The feature identities are intentionally open-ended.  The framework does not
    define what a domain's important relations, invariants, failure topologies,
    transformations or regime variables must be.
    """

    structure_id: str
    domain_id: str
    source_ids: tuple[str, ...] = ()
    native_parent_ids: tuple[str, ...] = ()
    relation_ids: tuple[str, ...] = ()
    higher_order_relation_ids: tuple[str, ...] = ()
    invariant_ids: tuple[str, ...] = ()
    failure_topology_ids: tuple[str, ...] = ()
    transformation_ids: tuple[str, ...] = ()
    regime_variable_ids: tuple[str, ...] = ()
    surface_tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.structure_id.strip() or not self.domain_id.strip():
            raise ValueError("domain structures require bound structure and domain identities")
        for name in (
            "source_ids",
            "native_parent_ids",
            "relation_ids",
            "higher_order_relation_ids",
            "invariant_ids",
            "failure_topology_ids",
            "transformation_ids",
            "regime_variable_ids",
            "surface_tags",
        ):
            object.__setattr__(
                self,
                name,
                _unique_nonblank(getattr(self, name), name=name),
            )

    def structural_features(self) -> frozenset[str]:
        """Return typed structural features without using surface vocabulary."""

        families = (
            ("REL", self.relation_ids),
            ("HREL", self.higher_order_relation_ids),
            ("INV", self.invariant_ids),
            ("FAIL", self.failure_topology_ids),
            ("TRANS", self.transformation_ids),
            ("REGIME", self.regime_variable_ids),
        )
        return frozenset(
            f"{prefix}:{value}"
            for prefix, values in families
            for value in values
        )


@dataclass(frozen=True, slots=True)
class RelationalAbstraction:
    abstraction_id: str
    feature_ids: tuple[str, ...]
    support_structure_ids: tuple[str, ...]
    support_domain_ids: tuple[str, ...]
    surface_diversity_score: float

    def __post_init__(self) -> None:
        if not self.abstraction_id.strip():
            raise ValueError("relational abstractions require an identity")
        object.__setattr__(
            self,
            "feature_ids",
            _unique_nonblank(self.feature_ids, name="feature_ids"),
        )
        object.__setattr__(
            self,
            "support_structure_ids",
            _unique_nonblank(self.support_structure_ids, name="support_structure_ids"),
        )
        object.__setattr__(
            self,
            "support_domain_ids",
            _unique_nonblank(self.support_domain_ids, name="support_domain_ids"),
        )
        if len(self.feature_ids) < 2:
            raise ValueError("an abstraction requires at least two structural features")
        if len(self.support_domain_ids) < 2:
            raise ValueError("an abstraction requires support from at least two domains")
        if not 0.0 <= self.surface_diversity_score <= 1.0:
            raise ValueError("surface_diversity_score must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class TransferCandidate:
    candidate_id: str
    abstraction_id: str
    target_structure_id: str
    donor_structure_ids: tuple[str, ...]
    shared_feature_ids: tuple[str, ...]
    structural_coverage: float
    max_surface_similarity: float
    remote_transfer_score: float

    def __post_init__(self) -> None:
        for value in (self.candidate_id, self.abstraction_id, self.target_structure_id):
            if not value.strip():
                raise ValueError("transfer candidates require bound identities")
        object.__setattr__(
            self,
            "donor_structure_ids",
            _unique_nonblank(self.donor_structure_ids, name="donor_structure_ids"),
        )
        object.__setattr__(
            self,
            "shared_feature_ids",
            _unique_nonblank(self.shared_feature_ids, name="shared_feature_ids"),
        )
        for value in (
            self.structural_coverage,
            self.max_surface_similarity,
            self.remote_transfer_score,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("transfer candidate scores must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class TransferHypothesis:
    hypothesis_id: str
    candidate_id: str
    mapped_relation_ids: tuple[str, ...]
    predicted_target_consequence_ids: tuple[str, ...]
    prohibited_transfer_ids: tuple[str, ...]
    falsifier_ids: tuple[str, ...]
    requested_authority_level: int = 0

    def __post_init__(self) -> None:
        if not self.hypothesis_id.strip() or not self.candidate_id.strip():
            raise ValueError("transfer hypotheses require bound identities")
        if self.requested_authority_level < 0:
            raise ValueError("requested authority cannot be negative")
        for name in (
            "mapped_relation_ids",
            "predicted_target_consequence_ids",
            "prohibited_transfer_ids",
            "falsifier_ids",
        ):
            object.__setattr__(
                self,
                name,
                _unique_nonblank(getattr(self, name), name=name),
            )
        if not self.predicted_target_consequence_ids:
            raise ValueError("transfer hypotheses require a prospective target consequence")
        if not self.falsifier_ids:
            raise ValueError("transfer hypotheses require explicit falsifiers")


@dataclass(frozen=True, slots=True)
class TransferEvidence:
    donor_native_recovery_pass: bool
    target_prediction_frozen_pre_outcome: bool
    hidden_target_discrimination_pass: bool | None
    negative_decoy_rejection_pass: bool | None
    countertransfer_challenge_pass: bool | None
    parent_control_executed: bool
    parent_control_sufficient: bool | None
    resource_accounted: bool
    authority_corruption_observed: bool = False
    independent_adjudication_complete: bool = False


@dataclass(frozen=True, slots=True)
class TransferDiscoveryReceipt:
    hypothesis_id: str
    status: TransferDiscoveryStatus
    reasons: tuple[str, ...]
    scientific_truth_authorized: bool = False
    novelty_authorized: bool = False
    adoption_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", TransferDiscoveryStatus(self.status))
        if (
            self.scientific_truth_authorized
            or self.novelty_authorized
            or self.adoption_authorized
        ):
            raise ValueError("transfer-discovery receipts are non-authorizing")


@dataclass(frozen=True, slots=True)
class ConceptState:
    concept_id: str
    version: int
    primitive_ids: tuple[str, ...] = ()
    relation_ids: tuple[str, ...] = ()
    scope_condition_ids: tuple[str, ...] = ()
    operational_link_ids: tuple[str, ...] = ()
    invariant_ids: tuple[str, ...] = ()
    representation_equivalence_ids: tuple[str, ...] = ()
    exemplar_ids: tuple[str, ...] = ()
    counterexample_ids: tuple[str, ...] = ()
    parent_concept_ids: tuple[str, ...] = ()
    unresolved_anomaly_ids: tuple[str, ...] = ()
    authority_ceiling: int = 0

    def __post_init__(self) -> None:
        if not self.concept_id.strip():
            raise ValueError("concept states require an identity")
        if self.version < 1:
            raise ValueError("concept versions start at one")
        if self.authority_ceiling < 0:
            raise ValueError("authority ceiling cannot be negative")
        for name in (
            "primitive_ids",
            "relation_ids",
            "scope_condition_ids",
            "operational_link_ids",
            "invariant_ids",
            "representation_equivalence_ids",
            "exemplar_ids",
            "counterexample_ids",
            "parent_concept_ids",
            "unresolved_anomaly_ids",
        ):
            object.__setattr__(
                self,
                name,
                _unique_nonblank(getattr(self, name), name=name),
            )


@dataclass(frozen=True, slots=True)
class ConceptTransitionProposal:
    transition_id: str
    kind: ConceptTransitionKind
    before_concept_id: str
    before_version: int
    after: ConceptState
    trigger_ids: tuple[str, ...]
    predicted_decision_ids: tuple[str, ...] = ()
    predicted_hidden_case_ids: tuple[str, ...] = ()
    falsifier_ids: tuple[str, ...] = ()
    loss_ids: tuple[str, ...] = ()
    requested_authority_level: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", ConceptTransitionKind(self.kind))
        if not self.transition_id.strip() or not self.before_concept_id.strip():
            raise ValueError("concept transitions require bound identities")
        if self.before_version < 1:
            raise ValueError("before_version must be positive")
        if self.requested_authority_level < 0:
            raise ValueError("requested authority cannot be negative")
        for name in (
            "trigger_ids",
            "predicted_decision_ids",
            "predicted_hidden_case_ids",
            "falsifier_ids",
            "loss_ids",
        ):
            object.__setattr__(
                self,
                name,
                _unique_nonblank(getattr(self, name), name=name),
            )
        if not self.trigger_ids:
            raise ValueError("concept transitions require a trigger")
        if not self.falsifier_ids:
            raise ValueError("concept transitions require falsifiers")
        if self.after.concept_id == self.before_concept_id:
            if self.after.version <= self.before_version:
                raise ValueError("same-concept transitions require a higher version")


@dataclass(frozen=True, slots=True)
class ConceptTransitionEvidence:
    parent_recovery_pass: bool
    native_fidelity_pass: bool
    old_valid_cases_retained: bool
    scope_explicit: bool
    loss_audited: bool
    measurement_links_valid: bool
    authority_valid: bool
    prediction_or_decision_changed: bool
    formal_necessity: bool
    hidden_case_pass: bool | None
    independent_adjudication_complete: bool = False


@dataclass(frozen=True, slots=True)
class ConceptTransitionReceipt:
    transition_id: str
    status: ConceptTransitionStatus
    reasons: tuple[str, ...]
    scientific_truth_authorized: bool = False
    foundation_status_authorized: bool = False
    adoption_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", ConceptTransitionStatus(self.status))
        if (
            self.scientific_truth_authorized
            or self.foundation_status_authorized
            or self.adoption_authorized
        ):
            raise ValueError("concept-transition receipts are non-authorizing")


def induce_relational_abstractions(
    structures: Iterable[DomainStructure],
    *,
    minimum_support_domains: int = 2,
    minimum_feature_count: int = 2,
    maximum_pairwise_surface_similarity: float = 1.0,
) -> tuple[RelationalAbstraction, ...]:
    """Induce repeated relational structure without a domain-specific lesson table.

    Pairwise intersections are only reference semantics, not a claim that human
    or machine conceptual learning reduces to set intersection.  They make the
    core contract testable: the *content* of an abstraction must arise from
    repeated typed structure in donor records rather than a hard-coded physics,
    biology or other domain rule.
    """

    if minimum_support_domains < 2 or minimum_feature_count < 2:
        raise ValueError("abstraction support and feature minima must both be at least two")
    if not 0.0 <= maximum_pairwise_surface_similarity <= 1.0:
        raise ValueError("maximum_pairwise_surface_similarity must be in [0, 1]")

    values = tuple(structures)
    groups: dict[tuple[str, ...], dict[str, object]] = {}
    for left, right in combinations(values, 2):
        if left.domain_id == right.domain_id:
            continue
        surface_similarity = _jaccard(left.surface_tags, right.surface_tags)
        if surface_similarity > maximum_pairwise_surface_similarity:
            continue
        shared = tuple(sorted(left.structural_features() & right.structural_features()))
        if len(shared) < minimum_feature_count:
            continue
        group = groups.setdefault(
            shared,
            {"structures": set(), "domains": set(), "surface": []},
        )
        group["structures"].update((left.structure_id, right.structure_id))
        group["domains"].update((left.domain_id, right.domain_id))
        group["surface"].append(surface_similarity)

    abstractions: list[RelationalAbstraction] = []
    for feature_ids, group in groups.items():
        domains = tuple(sorted(group["domains"]))
        if len(domains) < minimum_support_domains:
            continue
        surface_scores = tuple(group["surface"])
        digest = sha256("|".join(feature_ids).encode("utf-8")).hexdigest()[:20]
        abstractions.append(
            RelationalAbstraction(
                abstraction_id=f"abstraction-{digest}",
                feature_ids=feature_ids,
                support_structure_ids=tuple(sorted(group["structures"])),
                support_domain_ids=domains,
                surface_diversity_score=1.0 - (sum(surface_scores) / len(surface_scores)),
            )
        )
    return tuple(
        sorted(
            abstractions,
            key=lambda item: (
                -len(item.feature_ids),
                -item.surface_diversity_score,
                item.abstraction_id,
            ),
        )
    )


def discover_transfer_candidates(
    target: DomainStructure,
    structures: Iterable[DomainStructure],
    abstractions: Iterable[RelationalAbstraction],
    *,
    top_k: int = 10,
    minimum_shared_features: int = 2,
) -> tuple[TransferCandidate, ...]:
    """Retrieve candidate donors through learned relational abstractions.

    Surface similarity is recorded but not required.  A remote-transfer score
    rewards structural coverage that survives surface dissimilarity.
    """

    if top_k < 1 or minimum_shared_features < 2:
        raise ValueError("top_k must be positive and minimum_shared_features >= 2")

    structure_map = {item.structure_id: item for item in structures}
    target_features = target.structural_features()
    candidates: list[TransferCandidate] = []
    for abstraction in abstractions:
        donors = tuple(
            structure_map[structure_id]
            for structure_id in abstraction.support_structure_ids
            if structure_id in structure_map
            and structure_map[structure_id].domain_id != target.domain_id
        )
        if not donors:
            continue
        shared = tuple(sorted(target_features & set(abstraction.feature_ids)))
        if len(shared) < minimum_shared_features:
            continue
        coverage = len(shared) / len(abstraction.feature_ids)
        surface_similarity = max(
            (_jaccard(target.surface_tags, donor.surface_tags) for donor in donors),
            default=0.0,
        )
        remote_score = coverage * (1.0 - surface_similarity)
        digest = sha256(
            f"{target.structure_id}|{abstraction.abstraction_id}".encode("utf-8")
        ).hexdigest()[:20]
        candidates.append(
            TransferCandidate(
                candidate_id=f"transfer-{digest}",
                abstraction_id=abstraction.abstraction_id,
                target_structure_id=target.structure_id,
                donor_structure_ids=tuple(sorted(donor.structure_id for donor in donors)),
                shared_feature_ids=shared,
                structural_coverage=coverage,
                max_surface_similarity=surface_similarity,
                remote_transfer_score=remote_score,
            )
        )
    candidates.sort(
        key=lambda item: (
            -item.structural_coverage,
            -item.remote_transfer_score,
            item.max_surface_similarity,
            item.candidate_id,
        )
    )
    return tuple(candidates[:top_k])


def assess_transfer_hypothesis(
    hypothesis: TransferHypothesis,
    evidence: TransferEvidence,
) -> TransferDiscoveryReceipt:
    """Admit transfer only after donor recovery, hidden tests and negative controls."""

    reasons: list[str] = []
    if not evidence.donor_native_recovery_pass:
        return TransferDiscoveryReceipt(
            hypothesis.hypothesis_id,
            TransferDiscoveryStatus.BLOCKED_NATIVE_RECOVERY,
            ("donor native verdicts were not recovered",),
        )
    if not evidence.target_prediction_frozen_pre_outcome:
        return TransferDiscoveryReceipt(
            hypothesis.hypothesis_id,
            TransferDiscoveryStatus.BLOCKED_UNFROZEN_PREDICTION,
            ("target consequence was not frozen before outcome access",),
        )
    if evidence.authority_corruption_observed:
        return TransferDiscoveryReceipt(
            hypothesis.hypothesis_id,
            TransferDiscoveryStatus.FALSE_ANALOGY_REJECTED,
            ("transfer corrupted a source or authority boundary",),
        )

    challenge_values = (
        evidence.hidden_target_discrimination_pass,
        evidence.negative_decoy_rejection_pass,
        evidence.countertransfer_challenge_pass,
    )
    if any(value is False for value in challenge_values):
        return TransferDiscoveryReceipt(
            hypothesis.hypothesis_id,
            TransferDiscoveryStatus.FALSE_ANALOGY_REJECTED,
            ("a hidden target, decoy or counter-transfer challenge falsified the mapping",),
        )
    if any(value is None for value in challenge_values):
        reasons.append("one or more transfer challenges remain unexecuted")
    if not evidence.parent_control_executed:
        reasons.append("strongest parent transfer control has not executed")
    if evidence.parent_control_sufficient is None:
        reasons.append("parent sufficiency is unresolved")
    if not evidence.resource_accounted:
        reasons.append("resource cost is not bound")
    if reasons:
        return TransferDiscoveryReceipt(
            hypothesis.hypothesis_id,
            TransferDiscoveryStatus.CANNOT_CHECK,
            tuple(reasons),
        )
    if evidence.parent_control_sufficient:
        return TransferDiscoveryReceipt(
            hypothesis.hypothesis_id,
            TransferDiscoveryStatus.PARENT_SUFFICIENT,
            ("strongest parent reproduced the protected transfer decision",),
        )
    status = (
        TransferDiscoveryStatus.INDEPENDENTLY_ADJUDICATED_TRANSFER_RESIDUAL
        if evidence.independent_adjudication_complete
        else TransferDiscoveryStatus.PROTECTED_TRANSFER_RESIDUAL
    )
    return TransferDiscoveryReceipt(
        hypothesis.hypothesis_id,
        status,
        ("transfer residual survived registered parent and negative controls",),
    )


def assess_concept_transition(
    before: ConceptState,
    proposal: ConceptTransitionProposal,
    evidence: ConceptTransitionEvidence,
) -> ConceptTransitionReceipt:
    """Evaluate conceptual development as a scientific transition, not vocabulary change."""

    if proposal.before_concept_id != before.concept_id or proposal.before_version != before.version:
        raise ValueError("proposal does not bind the supplied before-state identity")

    if not evidence.parent_recovery_pass:
        return ConceptTransitionReceipt(
            proposal.transition_id,
            ConceptTransitionStatus.BLOCKED_PARENT_RECOVERY,
            ("new concept state does not recover the strongest parent concept",),
        )
    if not evidence.native_fidelity_pass or not evidence.old_valid_cases_retained:
        return ConceptTransitionReceipt(
            proposal.transition_id,
            ConceptTransitionStatus.BLOCKED_NATIVE_FIDELITY,
            ("new concept state loses valid native or predecessor judgments",),
        )
    if not evidence.scope_explicit or not evidence.loss_audited:
        return ConceptTransitionReceipt(
            proposal.transition_id,
            ConceptTransitionStatus.BLOCKED_SCOPE_OR_LOSS_AUDIT,
            ("scope or conceptual-loss audit is incomplete",),
        )
    if (
        not evidence.measurement_links_valid
        or not evidence.authority_valid
        or proposal.requested_authority_level > proposal.after.authority_ceiling
    ):
        return ConceptTransitionReceipt(
            proposal.transition_id,
            ConceptTransitionStatus.BLOCKED_MEASUREMENT_OR_AUTHORITY,
            ("measurement/operational or authority boundary is invalid",),
        )
    if not (evidence.prediction_or_decision_changed or evidence.formal_necessity):
        return ConceptTransitionReceipt(
            proposal.transition_id,
            ConceptTransitionStatus.NO_SCIENTIFIC_RESIDUAL,
            ("transition changes vocabulary/representation without a protected or formal residual",),
        )
    if evidence.hidden_case_pass is None:
        return ConceptTransitionReceipt(
            proposal.transition_id,
            ConceptTransitionStatus.READY_FOR_PROTECTED_EVALUATION,
            ("transition is operationalized but hidden-case evidence is not yet executed",),
        )
    if not evidence.hidden_case_pass:
        return ConceptTransitionReceipt(
            proposal.transition_id,
            ConceptTransitionStatus.NO_SCIENTIFIC_RESIDUAL,
            ("prospective hidden cases did not support the proposed conceptual transition",),
        )
    status = (
        ConceptTransitionStatus.INDEPENDENTLY_ADJUDICATED_CONCEPTUAL_RESIDUAL
        if evidence.independent_adjudication_complete
        else ConceptTransitionStatus.PROTECTED_CONCEPTUAL_RESIDUAL
    )
    return ConceptTransitionReceipt(
        proposal.transition_id,
        status,
        ("conceptual transition survived predecessor retention and hidden-case evaluation",),
    )
