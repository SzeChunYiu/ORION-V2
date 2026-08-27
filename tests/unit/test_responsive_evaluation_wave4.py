from orion_v2.responsive_evaluation import (
    CandidateResponseRecord,
    ResponsiveEvaluationStatus,
    ResponsiveEvaluationSystem,
    assess_responsive_evaluation,
)


def test_lucas_style_policy_response_can_reverse_static_winner() -> None:
    system = ResponsiveEvaluationSystem(
        "policy-eval",
        "welfare-evaluator",
        "2026",
        (
            CandidateResponseRecord(
                "policy-a", 0.9, 0.9, 0.7, 0.6, "natural-control:1"
            ),
            CandidateResponseRecord(
                "policy-b", 0.8, 0.8, 0.8, 0.85, "natural-control:1"
            ),
        ),
    )
    result = assess_responsive_evaluation(system)
    assert result.status is ResponsiveEvaluationStatus.WINNER_REVERSAL
    assert result.static_target_winner_ids == ("policy-a",)
    assert result.deployed_target_winner_ids == ("policy-b",)


def test_benchmark_gaming_proxy_gain_with_target_loss_fails_noncompensatorily() -> None:
    system = ResponsiveEvaluationSystem(
        "benchmark",
        "scientific-target",
        "v1",
        (
            CandidateResponseRecord("agent", 0.7, 0.8, 0.95, 0.6, "deployment:ab"),
            CandidateResponseRecord(
                "baseline", 0.6, 0.7, 0.6, 0.7, "deployment:ab"
            ),
        ),
    )
    result = assess_responsive_evaluation(system)
    assert result.status is ResponsiveEvaluationStatus.PROXY_IMPROVES_TARGET_WORSENS
    assert result.proxy_gaming_candidate_ids == ("agent",)
    assert result.scientific_progress_granted is False


def test_changed_results_without_control_are_cannot_attribute() -> None:
    system = ResponsiveEvaluationSystem(
        "institution",
        "review-score",
        "v1",
        (
            CandidateResponseRecord("a", 0.8, 0.8, 0.82, 0.82),
            CandidateResponseRecord("b", 0.7, 0.7, 0.72, 0.72),
        ),
    )
    result = assess_responsive_evaluation(system)
    assert (
        result.status
        is ResponsiveEvaluationStatus.RESPONSE_DETECTED_CAUSE_CANNOT_CHECK
    )
    assert result.response_control_bound is False


def test_stable_control_case_is_not_forced_to_fail() -> None:
    system = ResponsiveEvaluationSystem(
        "stable",
        "target",
        "v1",
        (
            CandidateResponseRecord("a", 0.8, 0.8, 0.8, 0.8, "control"),
            CandidateResponseRecord("b", 0.7, 0.7, 0.7, 0.7, "control"),
        ),
    )
    result = assess_responsive_evaluation(system)
    assert result.status is ResponsiveEvaluationStatus.STABLE_UNDER_RESPONSE


def test_missing_deployed_target_is_unmeasured_not_stable() -> None:
    system = ResponsiveEvaluationSystem(
        "missing",
        "target",
        "v1",
        (
            CandidateResponseRecord("a", 0.8, 0.8, 0.9, None, "control"),
            CandidateResponseRecord("b", 0.7, 0.7, 0.7, 0.7, "control"),
        ),
    )
    assert (
        assess_responsive_evaluation(system).status
        is ResponsiveEvaluationStatus.PROTECTED_TARGET_UNMEASURED
    )


def test_evaluator_epoch_drift_invalidates_comparison() -> None:
    system = ResponsiveEvaluationSystem(
        "drift",
        "target-v2",
        "epoch-2",
        (
            CandidateResponseRecord("a", 0.8, 0.8, 0.8, 0.8, "control"),
            CandidateResponseRecord("b", 0.7, 0.7, 0.7, 0.7, "control"),
        ),
    )
    result = assess_responsive_evaluation(
        system,
        expected_evaluator_id="target-v1",
        expected_evaluator_epoch_id="epoch-1",
    )
    assert result.status is ResponsiveEvaluationStatus.EVALUATOR_OR_EPOCH_DRIFT
