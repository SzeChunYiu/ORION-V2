"""Reference semantics for detecting formalism insufficiency and proposing new formalisms.

This module does not claim a universal algorithm for mathematical or scientific
breakthroughs. It provides transparent finite mechanics for one important case:
a current representation aliases cases that require different registered
judgments. The system may then search for the smallest additional distinctions
that resolve those collisions, followed by fail-closed admission gates for a
candidate formalism.

Historical mathematics and physics are donor/evaluation cases only. No fixed
list of breakthrough lessons is encoded as scientific truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from itertools import combinations
from typing import Iterable


class FormalismGenesisStatus(StrEnum):
    NO_REGISTERED_DEFICIT = "NO_REGISTERED_DEFICIT"
    PARENT_SUFFICIENT = "PARENT_SUFFICIENT"
    BLOCKED_NO_SEMANTICS = "BLOCKED_NO_SEMANTICS"
    BLOCKED_CONSISTENCY = "BLOCKED_CONSISTENCY"
    BLOCKED_PARENT_RECOVERY = "BLOCKED_PARENT_RECOVERY"
    BLOCKED_OLD_CASE_RETENTION = "BLOCKED_OLD_CASE_RETENTION"
    NO_GENERATIVE_RESIDUAL = "NO_GENERATIVE_RESIDUAL"
    READY_FOR_PROTECTED_EVALUATION = "READY_FOR_PROTECTED_EVALUATION"
    PROTECTED_FORMALISM_RESIDUAL = "PROTECTED_FORMALISM_RESIDUAL"
    INDEPENDENTLY_CHECKED_FORMALISM_RESIDUAL = "INDEPENDENTLY_CHECKED_FORMALISM_RESIDUAL"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class DistinctionCase:
    """A case as seen through the current formalism plus candidate distinctions."""

    case_id: str
    current_signature: tuple[str, ...]
    required_decision_id: str
    candidate_feature_values: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.required_decision_id.strip():
            raise ValueError("cases require non-blank case and decision identities")
        if any(not value.strip() for value in self.current_signature):
            raise ValueError("current signatures may not contain blanks")
        feature_map = dict(self.candidate_feature_values)
        if len(feature_map) != len(self.candidate_feature_values):
            raise ValueError("candidate features must have unique identities")
        if any(not key.strip() or not value.strip() for key, value in self.candidate_feature_values):
            raise ValueError("candidate feature identities and values may not be blank")

    @property
    def features(self) -> dict[str, str]:
        return dict(self.candidate_feature_values)


@dataclass(frozen=True, slots=True)
class RepresentationCollision:
    left_case_id: str
    right_case_id: str
    shared_signature: tuple[str, ...]
    left_decision_id: str
    right_decision_id: str
    separating_feature_ids: tuple[str, ...]


def representation_collisions(cases: Iterable[DistinctionCase]) -> tuple[RepresentationCollision, ...]:
    """Return pairs aliased by the current representation but requiring different decisions."""

    values = tuple(cases)
    collisions: list[RepresentationCollision] = []
    for left, right in combinations(values, 2):
        if left.current_signature != right.current_signature:
            continue
        if left.required_decision_id == right.required_decision_id:
            continue
        left_features = left.features
        right_features = right.features
        common = set(left_features) & set(right_features)
        separating = tuple(sorted(feature for feature in common if left_features[feature] != right_features[feature]))
        collisions.append(
            RepresentationCollision(
                left.case_id,
                right.case_id,
                left.current_signature,
                left.required_decision_id,
                right.required_decision_id,
                separating,
            )
        )
    return tuple(collisions)


def minimal_discriminating_feature_sets(
    cases: Iterable[DistinctionCase],
) -> tuple[tuple[str, ...], ...]:
    """Exact finite oracle for the smallest features needed to resolve all collisions.

    This is a hitting-set baseline for generated/small tasks. It is not a claim
    that real mathematical concept invention reduces to feature selection.
    """

    collisions = representation_collisions(cases)
    if not collisions:
        return ((),)
    if any(not collision.separating_feature_ids for collision in collisions):
        return ()
    feature_ids = sorted({feature for collision in collisions for feature in collision.separating_feature_ids})
    for size in range(1, len(feature_ids) + 1):
        solutions = []
        for selected in combinations(feature_ids, size):
            chosen = set(selected)
            if all(chosen.intersection(collision.separating_feature_ids) for collision in collisions):
                solutions.append(tuple(selected))
        if solutions:
            return tuple(solutions)
    return ()


@dataclass(frozen=True, slots=True)
class FormalismCandidate:
    formalism_id: str
    parent_formalism_ids: tuple[str, ...]
    primitive_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]
    operation_ids: tuple[str, ...]
    axiom_ids: tuple[str, ...]
    semantic_model_ids: tuple[str, ...]
    recovery_map_ids: tuple[str, ...]
    proof_or_derivation_rule_ids: tuple[str, ...]
    intended_deficit_ids: tuple[str, ...]
    prospective_consequence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.formalism_id.strip():
            raise ValueError("formalism candidates require an identity")
        for name in (
            "parent_formalism_ids",
            "primitive_ids",
            "relation_ids",
            "operation_ids",
            "axiom_ids",
            "semantic_model_ids",
            "recovery_map_ids",
            "proof_or_derivation_rule_ids",
            "intended_deficit_ids",
            "prospective_consequence_ids",
        ):
            values = getattr(self, name)
            if any(not value.strip() for value in values):
                raise ValueError(f"{name} may not contain blank identities")
            if len(values) != len(set(values)):
                raise ValueError(f"{name} identities must be unique")


@dataclass(frozen=True, slots=True)
class FormalismGenesisEvidence:
    registered_deficit_present: bool
    strongest_parent_executed: bool
    strongest_parent_sufficient: bool | None
    expressibility_or_collision_reduction_pass: bool | None
    semantic_model_witness_pass: bool | None
    consistency_or_model_check_pass: bool | None
    parent_recovery_pass: bool | None
    old_valid_case_retention_pass: bool | None
    prospective_new_consequence_pass: bool | None
    hidden_problem_success_pass: bool | None
    minimality_or_simpler_patch_check_pass: bool | None
    resource_accounted: bool
    independent_formal_check_complete: bool = False


@dataclass(frozen=True, slots=True)
class FormalismGenesisReceipt:
    formalism_id: str
    status: FormalismGenesisStatus
    reasons: tuple[str, ...]
    scientific_truth_authorized: bool = False
    foundation_status_authorized: bool = False
    adoption_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", FormalismGenesisStatus(self.status))
        if self.scientific_truth_authorized or self.foundation_status_authorized or self.adoption_authorized:
            raise ValueError("formalism-genesis receipts are non-authorizing")


def assess_formalism_candidate(
    candidate: FormalismCandidate,
    evidence: FormalismGenesisEvidence,
) -> FormalismGenesisReceipt:
    """Fail-closed candidate admission; novelty of notation carries no credit."""

    if not evidence.registered_deficit_present:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.NO_REGISTERED_DEFICIT,
            ("no protected representational/formal deficit was registered",),
        )
    if not evidence.strongest_parent_executed:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.CANNOT_CHECK,
            ("strongest applicable parent formalism has not executed",),
        )
    if evidence.strongest_parent_sufficient is None:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.CANNOT_CHECK,
            ("parent sufficiency is unresolved",),
        )
    if evidence.strongest_parent_sufficient:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.PARENT_SUFFICIENT,
            ("strongest parent resolves the registered deficit",),
        )
    if not candidate.semantic_model_ids or evidence.semantic_model_witness_pass is False:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.BLOCKED_NO_SEMANTICS,
            ("candidate lacks a valid semantic/model witness",),
        )
    if evidence.consistency_or_model_check_pass is False:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.BLOCKED_CONSISTENCY,
            ("candidate failed its registered consistency/model check",),
        )
    if evidence.parent_recovery_pass is False:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.BLOCKED_PARENT_RECOVERY,
            ("candidate does not recover the strongest valid predecessor/parent",),
        )
    if evidence.old_valid_case_retention_pass is False:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.BLOCKED_OLD_CASE_RETENTION,
            ("candidate loses registered old-valid cases",),
        )
    required = (
        evidence.expressibility_or_collision_reduction_pass,
        evidence.semantic_model_witness_pass,
        evidence.consistency_or_model_check_pass,
        evidence.parent_recovery_pass,
        evidence.old_valid_case_retention_pass,
        evidence.minimality_or_simpler_patch_check_pass,
    )
    if any(value is None for value in required) or not evidence.resource_accounted:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.CANNOT_CHECK,
            ("one or more mandatory formalism-genesis checks remain unresolved",),
        )
    if evidence.expressibility_or_collision_reduction_pass is False:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.NO_GENERATIVE_RESIDUAL,
            ("candidate does not repair the registered formal deficit",),
        )
    if evidence.minimality_or_simpler_patch_check_pass is False:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.NO_GENERATIVE_RESIDUAL,
            ("a simpler extension/patch explains the protected improvement",),
        )
    generative = evidence.prospective_new_consequence_pass
    hidden = evidence.hidden_problem_success_pass
    if generative is False or hidden is False:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.NO_GENERATIVE_RESIDUAL,
            ("candidate did not improve a prospectively frozen consequence/hidden problem",),
        )
    if generative is None or hidden is None:
        return FormalismGenesisReceipt(
            candidate.formalism_id,
            FormalismGenesisStatus.READY_FOR_PROTECTED_EVALUATION,
            ("candidate passes structural admission but protected generativity is not complete",),
        )
    status = (
        FormalismGenesisStatus.INDEPENDENTLY_CHECKED_FORMALISM_RESIDUAL
        if evidence.independent_formal_check_complete
        else FormalismGenesisStatus.PROTECTED_FORMALISM_RESIDUAL
    )
    return FormalismGenesisReceipt(
        candidate.formalism_id,
        status,
        ("candidate repairs a registered deficit, recovers predecessors, and survives protected generativity",),
    )
