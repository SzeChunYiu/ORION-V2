from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class ResponsiveEvaluationStatus(str, Enum):
    STABLE_UNDER_RESPONSE = "STABLE_UNDER_RESPONSE"
    WINNER_REVERSAL = "WINNER_REVERSAL"
    PROXY_IMPROVES_TARGET_WORSENS = "PROXY_IMPROVES_TARGET_WORSENS"
    RESPONSE_DETECTED_CAUSE_CANNOT_CHECK = "RESPONSE_DETECTED_CAUSE_CANNOT_CHECK"
    PROTECTED_TARGET_UNMEASURED = "PROTECTED_TARGET_UNMEASURED"
    EVALUATOR_OR_EPOCH_DRIFT = "EVALUATOR_OR_EPOCH_DRIFT"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class CandidateResponseRecord:
    candidate_id: str
    static_proxy_score: float
    static_target_score: float
    deployed_proxy_score: float | None
    deployed_target_score: float | None
    response_control_id: str = ""

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ValueError("candidate identity must be non-blank")


@dataclass(frozen=True, slots=True)
class ResponsiveEvaluationSystem:
    evaluation_id: str
    evaluator_id: str
    evaluator_epoch_id: str
    records: tuple[CandidateResponseRecord, ...]
    higher_proxy_is_better: bool = True
    higher_target_is_better: bool = True

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (
                self.evaluation_id,
                self.evaluator_id,
                self.evaluator_epoch_id,
            )
        ):
            raise ValueError("evaluation, evaluator and epoch ids must be non-blank")
        candidate_ids = [record.candidate_id for record in self.records]
        if not candidate_ids or len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("candidate identities must be non-empty and unique")


@dataclass(frozen=True, slots=True)
class ResponsiveEvaluationAssessment:
    evaluation_id: str
    status: ResponsiveEvaluationStatus
    static_proxy_winner_ids: tuple[str, ...]
    static_target_winner_ids: tuple[str, ...]
    deployed_proxy_winner_ids: tuple[str, ...]
    deployed_target_winner_ids: tuple[str, ...]
    proxy_gaming_candidate_ids: tuple[str, ...]
    response_control_bound: bool
    violations: tuple[str, ...]
    scientific_progress_granted: bool = False
    adoption_authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.scientific_progress_granted or self.adoption_authority_granted:
            raise ValueError("responsive evaluation is non-authorizing")


def _winner_ids(
    values: Mapping[str, float],
    *,
    higher_is_better: bool,
) -> tuple[str, ...]:
    if not values:
        return ()
    optimum = max(values.values()) if higher_is_better else min(values.values())
    return tuple(
        sorted(candidate_id for candidate_id, value in values.items() if value == optimum)
    )


def _improves(before: float, after: float, *, higher_is_better: bool) -> bool:
    return after > before if higher_is_better else after < before


def _worsens(before: float, after: float, *, higher_is_better: bool) -> bool:
    return after < before if higher_is_better else after > before


def assess_responsive_evaluation(
    system: ResponsiveEvaluationSystem,
    *,
    expected_evaluator_id: str | None = None,
    expected_evaluator_epoch_id: str | None = None,
) -> ResponsiveEvaluationAssessment:
    if (
        expected_evaluator_id is not None and expected_evaluator_id != system.evaluator_id
    ) or (
        expected_evaluator_epoch_id is not None
        and expected_evaluator_epoch_id != system.evaluator_epoch_id
    ):
        return ResponsiveEvaluationAssessment(
            system.evaluation_id,
            ResponsiveEvaluationStatus.EVALUATOR_OR_EPOCH_DRIFT,
            (),
            (),
            (),
            (),
            (),
            False,
            ("evaluator or epoch differs from the frozen evaluation",),
        )

    static_proxy = {
        record.candidate_id: record.static_proxy_score for record in system.records
    }
    static_target = {
        record.candidate_id: record.static_target_score for record in system.records
    }
    static_proxy_winners = _winner_ids(
        static_proxy, higher_is_better=system.higher_proxy_is_better
    )
    static_target_winners = _winner_ids(
        static_target, higher_is_better=system.higher_target_is_better
    )

    if any(
        record.deployed_proxy_score is None or record.deployed_target_score is None
        for record in system.records
    ):
        return ResponsiveEvaluationAssessment(
            system.evaluation_id,
            ResponsiveEvaluationStatus.PROTECTED_TARGET_UNMEASURED,
            static_proxy_winners,
            static_target_winners,
            (),
            (),
            (),
            False,
            ("deployed proxy and protected target are required for every candidate",),
        )

    deployed_proxy = {
        record.candidate_id: float(record.deployed_proxy_score)
        for record in system.records
    }
    deployed_target = {
        record.candidate_id: float(record.deployed_target_score)
        for record in system.records
    }
    deployed_proxy_winners = _winner_ids(
        deployed_proxy, higher_is_better=system.higher_proxy_is_better
    )
    deployed_target_winners = _winner_ids(
        deployed_target, higher_is_better=system.higher_target_is_better
    )

    proxy_gaming = tuple(
        sorted(
            record.candidate_id
            for record in system.records
            if _improves(
                record.static_proxy_score,
                float(record.deployed_proxy_score),
                higher_is_better=system.higher_proxy_is_better,
            )
            and _worsens(
                record.static_target_score,
                float(record.deployed_target_score),
                higher_is_better=system.higher_target_is_better,
            )
        )
    )
    changes = any(
        record.static_proxy_score != record.deployed_proxy_score
        or record.static_target_score != record.deployed_target_score
        for record in system.records
    )
    control_bound = all(record.response_control_id.strip() for record in system.records)

    if proxy_gaming:
        status = ResponsiveEvaluationStatus.PROXY_IMPROVES_TARGET_WORSENS
        violations = (
            "proxy improvement accompanies protected-target regression for: "
            + ", ".join(proxy_gaming),
        )
    elif set(static_target_winners) != set(deployed_target_winners):
        status = ResponsiveEvaluationStatus.WINNER_REVERSAL
        violations = (
            "the protected-target winner changes after deployment/response",
        )
    elif changes and not control_bound:
        status = ResponsiveEvaluationStatus.RESPONSE_DETECTED_CAUSE_CANNOT_CHECK
        violations = (
            "evaluation changed after deployment but no response/control identity is bound",
        )
    else:
        status = ResponsiveEvaluationStatus.STABLE_UNDER_RESPONSE
        violations = ()

    return ResponsiveEvaluationAssessment(
        system.evaluation_id,
        status,
        static_proxy_winners,
        static_target_winners,
        deployed_proxy_winners,
        deployed_target_winners,
        proxy_gaming,
        control_bound,
        violations,
    )
