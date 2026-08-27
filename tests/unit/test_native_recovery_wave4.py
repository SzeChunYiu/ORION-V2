from dataclasses import replace

from orion_v2.generalization_compiler import (
    AdaptationStatus,
    assess_adaptation_contract,
)
from orion_v2.native_corpus_strict import (
    built_in_native_recovery_cases,
    built_in_target_adaptation_contracts,
)
from orion_v2.native_recovery import (
    NativeRecoveryCase,
    NativeRecoveryStatus,
    RecoveryMode,
    assess_native_recovery,
    assess_native_recovery_suite,
)


def test_seventeen_case_native_corpus_recovers_frozen_expectations() -> None:
    cases = built_in_native_recovery_cases()
    assessments, summary = assess_native_recovery_suite(cases)
    assert len(cases) == 17
    assert len({case.domain_id for case in cases}) >= 16
    assert summary.exact_count == 17
    assert summary.all_valid is True
    assert all(
        assessment.status is NativeRecoveryStatus.EXACT_NATIVE_RECOVERY
        for assessment in assessments
    )


def test_observed_result_cannot_write_its_own_answer_key() -> None:
    case = built_in_native_recovery_cases()[0]
    corrupted = replace(case, generalized_judgment="DEADLOCK")
    assessment = assess_native_recovery(corrupted)
    assert assessment.status is NativeRecoveryStatus.INVALID_DECISION_DRIFT
    assert assessment.expected_generalized_judgment == "SOUND"


def test_assumption_erasure_and_counterexample_loss_fail_closed() -> None:
    case = built_in_native_recovery_cases()[3]
    assumption_erased = replace(case, mapped_assumption_ids=())
    counterexample_lost = replace(case, reflected_counterexample_ids=())
    assert (
        assess_native_recovery(assumption_erased).status
        is NativeRecoveryStatus.INVALID_ASSUMPTION_ERASURE
    )
    assert (
        assess_native_recovery(counterexample_lost).status
        is NativeRecoveryStatus.INVALID_COUNTEREXAMPLE_LOSS
    )


def test_sound_overapproximation_is_not_reported_as_exact() -> None:
    case = NativeRecoveryCase(
        case_id="sound-set",
        domain_id="diagnosis",
        theory_family_id="G02-2",
        native_judgment="native-cause",
        generalized_judgment=frozenset({"mapped-cause", "alternative"}),
        native_to_generalized={"native-cause": "mapped-cause"},
        native_assumption_ids=("assumption",),
        mapped_assumption_ids=("assumption",),
        native_counterexample_ids=(),
        reflected_counterexample_ids=(),
        source_ids=("source",),
        mode=RecoveryMode.SOUND_OVER_APPROXIMATION,
    )
    assert (
        assess_native_recovery(case).status
        is NativeRecoveryStatus.SOUND_NATIVE_RECOVERY
    )


def test_target_adaptation_is_separate_from_native_recovery() -> None:
    complete, missing_calibration, missing_tests = (
        built_in_target_adaptation_contracts()
    )
    assert (
        assess_adaptation_contract(complete)
        is AdaptationStatus.READY_FOR_TARGET_NATIVE_VALIDATION
    )
    assert (
        assess_adaptation_contract(missing_calibration)
        is AdaptationStatus.BLOCKED_CALIBRATION
    )
    assert (
        assess_adaptation_contract(missing_tests)
        is AdaptationStatus.BLOCKED_TARGET_TESTS
    )
