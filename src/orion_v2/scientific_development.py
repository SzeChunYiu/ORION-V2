"""Reference semantics for population-scale scientific-development learning.

This module is deliberately non-authorizing. It represents source-bound research
trajectories, audits important observation biases, discovers transparent candidate
operator regularities, and evaluates whether a candidate principle has progressed
from historical association to protected prospective evidence.

Citation impact, prizes, fame, disruption metrics, and model confidence are never
interpreted as scientific truth labels by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from itertools import combinations
from typing import Iterable


def _unique(values: Iterable[str], *, name: str, allow_empty: bool = True) -> tuple[str, ...]:
    result = tuple(values)
    if not allow_empty and not result:
        raise ValueError(f"{name} must not be empty")
    if any(not value.strip() for value in result):
        raise ValueError(f"{name} may not contain blank identities")
    if len(result) != len(set(result)):
        raise ValueError(f"{name} identities must be unique")
    return result


class DevelopmentOutcomeClass(StrEnum):
    VALIDATED_SUCCESS = "VALIDATED_SUCCESS"
    VALIDATED_FAILURE = "VALIDATED_FAILURE"
    PARTIAL = "PARTIAL"
    REDIRECTED = "REDIRECTED"
    ABANDONED = "ABANDONED"
    UNKNOWN = "UNKNOWN"


class ScientificDevelopmentStatus(StrEnum):
    BLOCKED_CORPUS_BIAS_AUDIT = "BLOCKED_CORPUS_BIAS_AUDIT"
    POPULATION_REGULARITY_ONLY = "POPULATION_REGULARITY_ONLY"
    PARENT_SUFFICIENT = "PARENT_SUFFICIENT"
    NO_PROTECTED_RESIDUAL = "NO_PROTECTED_RESIDUAL"
    PROTECTED_META_PRINCIPLE_RESIDUAL = "PROTECTED_META_PRINCIPLE_RESIDUAL"
    PROSPECTIVE_META_POLICY_RESIDUAL = "PROSPECTIVE_META_POLICY_RESIDUAL"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class DevelopmentStep:
    step_id: str
    ordinal: int
    state_feature_ids: tuple[str, ...]
    action_feature_ids: tuple[str, ...]
    result_feature_ids: tuple[str, ...] = ()
    failure_feature_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    validation_ids: tuple[str, ...] = ()
    resource_cost: float = 0.0

    def __post_init__(self) -> None:
        if not self.step_id.strip():
            raise ValueError("development steps require an identity")
        if self.ordinal < 0:
            raise ValueError("step ordinal must be non-negative")
        if self.resource_cost < 0:
            raise ValueError("resource cost cannot be negative")
        for name in (
            "state_feature_ids",
            "action_feature_ids",
            "result_feature_ids",
            "failure_feature_ids",
            "source_ids",
            "validation_ids",
        ):
            object.__setattr__(self, name, _unique(getattr(self, name), name=name))
        if not self.action_feature_ids:
            raise ValueError("development steps require at least one action feature")


@dataclass(frozen=True, slots=True)
class ScientificDevelopmentEpisode:
    episode_id: str
    domain_id: str
    epoch_id: str
    outcome_class: DevelopmentOutcomeClass
    steps: tuple[DevelopmentStep, ...]
    source_mode_ids: tuple[str, ...]
    team_id: str = ""
    institution_ids: tuple[str, ...] = ()
    outcome_witness_ids: tuple[str, ...] = ()
    proxy_metrics: tuple[tuple[str, float], ...] = ()
    bias_flag_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "outcome_class", DevelopmentOutcomeClass(self.outcome_class))
        for value in (self.episode_id, self.domain_id, self.epoch_id):
            if not value.strip():
                raise ValueError("episodes require episode/domain/epoch identities")
        if not self.steps:
            raise ValueError("episodes require at least one development step")
        if tuple(step.ordinal for step in self.steps) != tuple(sorted(step.ordinal for step in self.steps)):
            raise ValueError("episode steps must be ordered by ordinal")
        object.__setattr__(self, "source_mode_ids", _unique(self.source_mode_ids, name="source_mode_ids", allow_empty=False))
        object.__setattr__(self, "institution_ids", _unique(self.institution_ids, name="institution_ids"))
        object.__setattr__(self, "outcome_witness_ids", _unique(self.outcome_witness_ids, name="outcome_witness_ids"))
        object.__setattr__(self, "bias_flag_ids", _unique(self.bias_flag_ids, name="bias_flag_ids"))
        metric_names = [name for name, _ in self.proxy_metrics]
        if any(not name.strip() for name in metric_names) or len(metric_names) != len(set(metric_names)):
            raise ValueError("proxy metric names must be non-blank and unique")

    def action_features(self) -> frozenset[str]:
        return frozenset(feature for step in self.steps for feature in step.action_feature_ids)

    def transition_features(self) -> frozenset[str]:
        features: set[str] = set()
        for step in self.steps:
            features.update(f"ACTION:{item}" for item in step.action_feature_ids)
            features.update(f"RESULT:{item}" for item in step.result_feature_ids)
            features.update(f"FAIL:{item}" for item in step.failure_feature_ids)
        return frozenset(features)

    @property
    def total_resource_cost(self) -> float:
        return sum(step.resource_cost for step in self.steps)


@dataclass(frozen=True, slots=True)
class CorpusBiasAudit:
    survivorship_model_bound: bool
    publication_bias_model_bound: bool
    citation_bias_model_bound: bool
    field_epoch_bias_model_bound: bool
    language_geography_bias_model_bound: bool
    team_institution_bias_model_bound: bool
    missing_failure_censoring_explicit: bool
    multiple_source_modes_present: bool
    unresolved_critical_bias_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "unresolved_critical_bias_ids", _unique(self.unresolved_critical_bias_ids, name="unresolved_critical_bias_ids"))

    @property
    def passes_for_population_claims(self) -> bool:
        required = (
            self.survivorship_model_bound,
            self.publication_bias_model_bound,
            self.citation_bias_model_bound,
            self.field_epoch_bias_model_bound,
            self.language_geography_bias_model_bound,
            self.team_institution_bias_model_bound,
            self.missing_failure_censoring_explicit,
            self.multiple_source_modes_present,
        )
        return all(required) and not self.unresolved_critical_bias_ids


@dataclass(frozen=True, slots=True)
class DevelopmentOperatorCandidate:
    operator_id: str
    feature_ids: tuple[str, ...]
    supporting_episode_ids: tuple[str, ...]
    contradicting_episode_ids: tuple[str, ...]
    positive_rate: float
    negative_rate: float
    rate_difference: float
    source_domain_ids: tuple[str, ...]
    source_epoch_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.operator_id.strip():
            raise ValueError("operator candidates require an identity")
        for name in (
            "feature_ids",
            "supporting_episode_ids",
            "contradicting_episode_ids",
            "source_domain_ids",
            "source_epoch_ids",
        ):
            object.__setattr__(self, name, _unique(getattr(self, name), name=name, allow_empty=name not in {"feature_ids", "supporting_episode_ids"}))
        for value in (self.positive_rate, self.negative_rate):
            if not 0.0 <= value <= 1.0:
                raise ValueError("operator rates must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class MetaPrincipleEvidence:
    corpus_bias_audit_pass: bool
    matched_failure_controls_executed: bool
    strongest_parent_executed: bool
    strongest_parent_sufficient: bool | None
    heldout_field_pass: bool | None
    heldout_epoch_pass: bool | None
    prospective_task_pass: bool | None
    critical_loss_observed: bool
    resource_accounted: bool
    independent_adjudication_complete: bool = False


@dataclass(frozen=True, slots=True)
class ScientificDevelopmentReceipt:
    candidate_id: str
    status: ScientificDevelopmentStatus
    reasons: tuple[str, ...]
    scientific_truth_authorized: bool = False
    causal_law_authorized: bool = False
    field_status_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", ScientificDevelopmentStatus(self.status))
        if self.scientific_truth_authorized or self.causal_law_authorized or self.field_status_authorized:
            raise ValueError("scientific-development receipts are non-authorizing")


def _episodes_by_outcome(episodes: Iterable[ScientificDevelopmentEpisode]) -> tuple[tuple[ScientificDevelopmentEpisode, ...], tuple[ScientificDevelopmentEpisode, ...]]:
    values = tuple(episodes)
    positive = tuple(ep for ep in values if ep.outcome_class is DevelopmentOutcomeClass.VALIDATED_SUCCESS)
    negative = tuple(ep for ep in values if ep.outcome_class in {DevelopmentOutcomeClass.VALIDATED_FAILURE, DevelopmentOutcomeClass.ABANDONED})
    return positive, negative


def discover_operator_contrasts(
    episodes: Iterable[ScientificDevelopmentEpisode],
    *,
    minimum_positive_support: int = 2,
    maximum_feature_order: int = 2,
    minimum_rate_difference: float = 0.0,
) -> tuple[DevelopmentOperatorCandidate, ...]:
    """Discover transparent success/failure regularities without granting causality."""

    if minimum_positive_support < 1:
        raise ValueError("minimum_positive_support must be positive")
    if maximum_feature_order not in {1, 2, 3}:
        raise ValueError("maximum_feature_order must be 1, 2 or 3")
    positive, negative = _episodes_by_outcome(episodes)
    if not positive or not negative:
        return ()
    feature_universe = sorted({feature for ep in positive + negative for feature in ep.transition_features()})
    candidates: list[DevelopmentOperatorCandidate] = []
    for order in range(1, maximum_feature_order + 1):
        for combo in combinations(feature_universe, order):
            combo_set = set(combo)
            supporting = tuple(ep for ep in positive if combo_set.issubset(ep.transition_features()))
            if len(supporting) < minimum_positive_support:
                continue
            contradicting = tuple(ep for ep in negative if combo_set.issubset(ep.transition_features()))
            p_rate = len(supporting) / len(positive)
            n_rate = len(contradicting) / len(negative)
            diff = p_rate - n_rate
            if diff < minimum_rate_difference:
                continue
            digest = sha256("|".join(combo).encode("utf-8")).hexdigest()[:20]
            candidates.append(
                DevelopmentOperatorCandidate(
                    operator_id=f"devop-{digest}",
                    feature_ids=combo,
                    supporting_episode_ids=tuple(ep.episode_id for ep in supporting),
                    contradicting_episode_ids=tuple(ep.episode_id for ep in contradicting),
                    positive_rate=p_rate,
                    negative_rate=n_rate,
                    rate_difference=diff,
                    source_domain_ids=tuple(sorted({ep.domain_id for ep in supporting})),
                    source_epoch_ids=tuple(sorted({ep.epoch_id for ep in supporting})),
                )
            )
    return tuple(sorted(candidates, key=lambda item: (-item.rate_difference, -item.positive_rate, len(item.feature_ids), item.operator_id)))


def assess_meta_principle(candidate_id: str, evidence: MetaPrincipleEvidence) -> ScientificDevelopmentReceipt:
    """Classify a candidate meta-principle without converting association into causality."""

    if not evidence.corpus_bias_audit_pass or not evidence.matched_failure_controls_executed:
        return ScientificDevelopmentReceipt(candidate_id, ScientificDevelopmentStatus.BLOCKED_CORPUS_BIAS_AUDIT, ("population bias audit or matched failure controls are incomplete",))
    if evidence.critical_loss_observed:
        return ScientificDevelopmentReceipt(candidate_id, ScientificDevelopmentStatus.NO_PROTECTED_RESIDUAL, ("candidate creates a registered critical loss",))
    if not evidence.strongest_parent_executed:
        return ScientificDevelopmentReceipt(candidate_id, ScientificDevelopmentStatus.CANNOT_CHECK, ("strongest parent explanation has not executed",))
    if evidence.strongest_parent_sufficient is True:
        return ScientificDevelopmentReceipt(candidate_id, ScientificDevelopmentStatus.PARENT_SUFFICIENT, ("strongest parent reproduces the protected decision",))
    unresolved = []
    if evidence.strongest_parent_sufficient is None:
        unresolved.append("parent sufficiency unresolved")
    if evidence.heldout_field_pass is None:
        unresolved.append("held-out field test not executed")
    if evidence.heldout_epoch_pass is None:
        unresolved.append("held-out epoch test not executed")
    if not evidence.resource_accounted:
        unresolved.append("resource accounting incomplete")
    if unresolved:
        return ScientificDevelopmentReceipt(candidate_id, ScientificDevelopmentStatus.POPULATION_REGULARITY_ONLY, tuple(unresolved))
    if not evidence.heldout_field_pass or not evidence.heldout_epoch_pass:
        return ScientificDevelopmentReceipt(candidate_id, ScientificDevelopmentStatus.NO_PROTECTED_RESIDUAL, ("candidate failed held-out field or epoch transfer",))
    if evidence.prospective_task_pass is None:
        return ScientificDevelopmentReceipt(candidate_id, ScientificDevelopmentStatus.POPULATION_REGULARITY_ONLY, ("cross-field/epoch regularity survives, but prospective intervention is untested",))
    if not evidence.prospective_task_pass:
        return ScientificDevelopmentReceipt(candidate_id, ScientificDevelopmentStatus.NO_PROTECTED_RESIDUAL, ("candidate did not improve the prospectively frozen research episode",))
    status = ScientificDevelopmentStatus.PROSPECTIVE_META_POLICY_RESIDUAL if evidence.independent_adjudication_complete else ScientificDevelopmentStatus.PROTECTED_META_PRINCIPLE_RESIDUAL
    return ScientificDevelopmentReceipt(candidate_id, status, ("candidate survived matched failures, strongest parent, held-out fields/epochs and prospective evaluation",))


def corpus_summary(episodes: Iterable[ScientificDevelopmentEpisode]) -> dict[str, object]:
    values = tuple(episodes)
    return {
        "episodes": len(values),
        "domains": len({ep.domain_id for ep in values}),
        "epochs": len({ep.epoch_id for ep in values}),
        "source_modes": len({mode for ep in values for mode in ep.source_mode_ids}),
        "validated_success": sum(ep.outcome_class is DevelopmentOutcomeClass.VALIDATED_SUCCESS for ep in values),
        "validated_failure_or_abandoned": sum(ep.outcome_class in {DevelopmentOutcomeClass.VALIDATED_FAILURE, DevelopmentOutcomeClass.ABANDONED} for ep in values),
        "unknown_or_partial": sum(ep.outcome_class in {DevelopmentOutcomeClass.UNKNOWN, DevelopmentOutcomeClass.PARTIAL, DevelopmentOutcomeClass.REDIRECTED} for ep in values),
        "total_resource_cost": sum(ep.total_resource_cost for ep in values),
    }
