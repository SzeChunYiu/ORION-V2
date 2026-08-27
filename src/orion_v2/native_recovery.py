from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Hashable, Mapping

Judgment = Hashable | frozenset[Hashable]


class RecoveryMode(str, Enum):
    EXACT = "EXACT"
    SOUND_OVER_APPROXIMATION = "SOUND_OVER_APPROXIMATION"


class NativeRecoveryStatus(str, Enum):
    EXACT_NATIVE_RECOVERY = "EXACT_NATIVE_RECOVERY"
    SOUND_NATIVE_RECOVERY = "SOUND_NATIVE_RECOVERY"
    INVALID_DECISION_DRIFT = "INVALID_DECISION_DRIFT"
    INVALID_ASSUMPTION_ERASURE = "INVALID_ASSUMPTION_ERASURE"
    INVALID_COUNTEREXAMPLE_LOSS = "INVALID_COUNTEREXAMPLE_LOSS"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class NativeRecoveryCase:
    case_id: str
    domain_id: str
    theory_family_id: str
    native_judgment: Hashable
    generalized_judgment: Judgment
    native_to_generalized: Mapping[Hashable, Judgment]
    native_assumption_ids: tuple[str, ...]
    mapped_assumption_ids: tuple[str, ...]
    native_counterexample_ids: tuple[str, ...]
    reflected_counterexample_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    mode: RecoveryMode = RecoveryMode.EXACT

    def __post_init__(self) -> None:
        object.__setattr__(self, "mode", RecoveryMode(self.mode))
        if any(
            not value.strip()
            for value in (self.case_id, self.domain_id, self.theory_family_id)
        ):
            raise ValueError("recovery identities must be non-blank")
        for values in (
            self.native_assumption_ids,
            self.mapped_assumption_ids,
            self.native_counterexample_ids,
            self.reflected_counterexample_ids,
            self.source_ids,
        ):
            if any(not value.strip() for value in values):
                raise ValueError("recovery identity collections may not contain blanks")


@dataclass(frozen=True, slots=True)
class NativeRecoveryAssessment:
    case_id: str
    status: NativeRecoveryStatus
    expected_generalized_judgment: Judgment | None
    observed_generalized_judgment: Judgment
    missing_assumption_ids: tuple[str, ...]
    missing_counterexample_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    grants_scientific_truth: bool = False
    grants_novelty: bool = False
    grants_target_adoption: bool = False

    def __post_init__(self) -> None:
        if (
            self.grants_scientific_truth
            or self.grants_novelty
            or self.grants_target_adoption
        ):
            raise ValueError("native recovery assessments are non-authorizing")


@dataclass(frozen=True, slots=True)
class NativeRecoverySuiteAssessment:
    assessment_ids: tuple[str, ...]
    exact_count: int
    sound_count: int
    invalid_decision_count: int
    assumption_erasure_count: int
    counterexample_loss_count: int
    cannot_check_count: int

    @property
    def all_valid(self) -> bool:
        return (
            self.invalid_decision_count
            + self.assumption_erasure_count
            + self.counterexample_loss_count
            + self.cannot_check_count
            == 0
        )


def assess_native_recovery(
    case: NativeRecoveryCase,
) -> NativeRecoveryAssessment:
    if not case.source_ids:
        return NativeRecoveryAssessment(
            case.case_id,
            NativeRecoveryStatus.CANNOT_CHECK,
            None,
            case.generalized_judgment,
            (),
            (),
            ("source-bound native reconstruction is required",),
        )
    missing_assumptions = tuple(
        sorted(set(case.native_assumption_ids) - set(case.mapped_assumption_ids))
    )
    if missing_assumptions:
        return NativeRecoveryAssessment(
            case.case_id,
            NativeRecoveryStatus.INVALID_ASSUMPTION_ERASURE,
            case.native_to_generalized.get(case.native_judgment),
            case.generalized_judgment,
            missing_assumptions,
            (),
            ("one or more native assumptions were erased",),
        )
    missing_counterexamples = tuple(
        sorted(
            set(case.native_counterexample_ids)
            - set(case.reflected_counterexample_ids)
        )
    )
    if missing_counterexamples:
        return NativeRecoveryAssessment(
            case.case_id,
            NativeRecoveryStatus.INVALID_COUNTEREXAMPLE_LOSS,
            case.native_to_generalized.get(case.native_judgment),
            case.generalized_judgment,
            (),
            missing_counterexamples,
            ("one or more native counterexamples are not reflected",),
        )
    if case.native_judgment not in case.native_to_generalized:
        return NativeRecoveryAssessment(
            case.case_id,
            NativeRecoveryStatus.CANNOT_CHECK,
            None,
            case.generalized_judgment,
            (),
            (),
            ("native terminal map is incomplete",),
        )
    expected = case.native_to_generalized[case.native_judgment]
    if case.mode is RecoveryMode.SOUND_OVER_APPROXIMATION:
        valid = (
            isinstance(case.generalized_judgment, frozenset)
            and expected in case.generalized_judgment
        )
        status = (
            NativeRecoveryStatus.SOUND_NATIVE_RECOVERY
            if valid
            else NativeRecoveryStatus.INVALID_DECISION_DRIFT
        )
    else:
        valid = expected == case.generalized_judgment
        status = (
            NativeRecoveryStatus.EXACT_NATIVE_RECOVERY
            if valid
            else NativeRecoveryStatus.INVALID_DECISION_DRIFT
        )
    return NativeRecoveryAssessment(
        case.case_id,
        status,
        expected,
        case.generalized_judgment,
        (),
        (),
        () if valid else ("generalized judgment does not recover the native judgment",),
    )


def assess_native_recovery_suite(
    cases: tuple[NativeRecoveryCase, ...],
) -> tuple[tuple[NativeRecoveryAssessment, ...], NativeRecoverySuiteAssessment]:
    assessments = tuple(assess_native_recovery(case) for case in cases)
    count = lambda status: sum(item.status is status for item in assessments)
    summary = NativeRecoverySuiteAssessment(
        tuple(item.case_id for item in assessments),
        count(NativeRecoveryStatus.EXACT_NATIVE_RECOVERY),
        count(NativeRecoveryStatus.SOUND_NATIVE_RECOVERY),
        count(NativeRecoveryStatus.INVALID_DECISION_DRIFT),
        count(NativeRecoveryStatus.INVALID_ASSUMPTION_ERASURE),
        count(NativeRecoveryStatus.INVALID_COUNTEREXAMPLE_LOSS),
        count(NativeRecoveryStatus.CANNOT_CHECK),
    )
    return assessments, summary
