import pytest

from orion_v2.human_epistemics import (
    AttributionStatus,
    CalibrationCase,
    CalibrationStatus,
    CompetenceReceipt,
    CompetenceTransferStatus,
    CriticismOutcome,
    CriticismReceipt,
    DistributedEpisode,
    DistributedStateStatus,
    EncounterCandidate,
    EncounterStatus,
    FailureLesson,
    InquiryEstimate,
    LessonTransferStatus,
    MetaAction,
    OutcomeSource,
    ReviewIndependence,
    SurpriseVector,
    assess_binary_calibration,
    assess_competence_transfer,
    assess_criticism,
    assess_distributed_state,
    assess_encounter,
    assess_failure_lesson_transfer,
    choose_meta_action,
)


def test_dependent_outcomes_do_not_calibrate_self_model() -> None:
    result = assess_binary_calibration(
        (
            CalibrationCase(
                "shared", 0.99, True, OutcomeSource.INDEPENDENT,
                frozenset({"model-A"}), frozenset({"model-A"}),
            ),
            CalibrationCase("k1", 0.8, True, OutcomeSource.KNOWN_ANSWER),
            CalibrationCase("k2", 0.2, False, OutcomeSource.KNOWN_ANSWER),
            CalibrationCase("k3", 0.7, True, OutcomeSource.KNOWN_ANSWER),
        )
    )
    assert result.status is CalibrationStatus.CALIBRATED_ON_BOUND_SET
    assert result.independent_case_ids == ("k1", "k2", "k3")
    assert result.excluded_case_ids == ("shared",)


def test_miscalibrated_self_model_is_detected() -> None:
    result = assess_binary_calibration(
        tuple(CalibrationCase(f"c{i}", 0.95, False, OutcomeSource.KNOWN_ANSWER) for i in range(4))
    )
    assert result.status is CalibrationStatus.MISCALIBRATED_ON_BOUND_SET
    assert result.brier_score == pytest.approx(0.9025)


def test_uncalibrated_self_model_cannot_self_authorize_proceeding() -> None:
    result = choose_meta_action(
        InquiryEstimate(0.99, 0.99, 0, 0, CalibrationStatus.CANNOT_CHECK),
        external_review_available=False,
    )
    assert result.action is MetaAction.CANNOT_CHECK
    assert not result.evidence_obligation_discharged
    assert not result.authority_granted


def test_required_external_review_beats_high_self_confidence() -> None:
    result = choose_meta_action(
        InquiryEstimate(0.99, 0.99, 0, 0.1, CalibrationStatus.CALIBRATED_ON_BOUND_SET),
        hard_external_check_required=True,
    )
    assert result.action is MetaAction.EXTERNAL_REVIEW


def test_representation_insufficiency_witness_triggers_representation_change() -> None:
    result = choose_meta_action(
        InquiryEstimate(0.2, 0.2, 1, 1, CalibrationStatus.CALIBRATED_ON_BOUND_SET),
        representation_limit_witnessed=True,
    )
    assert result.action is MetaAction.CHANGE_REPRESENTATION


def test_positive_value_of_more_compute_selects_more_compute() -> None:
    result = choose_meta_action(
        InquiryEstimate(0.75, 0.9, 0.6, 0.1, CalibrationStatus.CALIBRATED_ON_BOUND_SET),
        more_compute_cost=0.2,
    )
    assert result.action is MetaAction.MORE_COMPUTE


def test_unreproduced_failure_is_not_a_lesson() -> None:
    result = assess_failure_lesson_transfer(
        FailureLesson("lesson", False, AttributionStatus.ESTABLISHED, "cause", "fix", True, "source"),
        "source",
    )
    assert result.status is LessonTransferStatus.CANNOT_CHECK


def test_explicit_counterexample_blocks_failure_lesson_transfer() -> None:
    lesson = FailureLesson(
        "lesson", True, AttributionStatus.ESTABLISHED, "cause", "fix", True, "source",
        explicit_transfer_scope=frozenset({"near"}), counterexample_contexts=frozenset({"counter"}),
    )
    assert assess_failure_lesson_transfer(lesson, "counter").status is LessonTransferStatus.REJECT_TRANSFER


def test_out_of_scope_failure_lesson_requires_revalidation() -> None:
    lesson = FailureLesson("lesson", True, AttributionStatus.ESTABLISHED, "cause", "fix", True, "source")
    assert (
        assess_failure_lesson_transfer(lesson, "new", cause_preserved=True).status
        is LessonTransferStatus.REVALIDATE_BEFORE_USE
    )


def test_noisy_surprise_is_not_serendipity() -> None:
    result = assess_encounter(
        EncounterCandidate(
            "noise", "sensor", SurpriseVector(predictive=1, state_transition=1),
            cross_problem_relevance=0.2, noise_risk=0.95, reproducible=False,
            discriminator_available=False, estimated_followup_cost=0,
        ),
        followup_budget=10,
    )
    assert result.status is EncounterStatus.IGNORE_AS_NOISE
    assert not result.claim_authorized and not result.agenda_authorized


def test_useful_event_is_retained_for_test_not_accepted_as_truth() -> None:
    result = assess_encounter(
        EncounterCandidate(
            "anomaly", "experiment-7", SurpriseVector(causal=0.9, semantic=0.8),
            cross_problem_relevance=0.85, noise_risk=0.1, reproducible=True,
            discriminator_available=True, estimated_followup_cost=2,
        ),
        followup_budget=3,
    )
    assert result.status is EncounterStatus.RETAIN_FOR_TEST
    assert not result.claim_authorized and not result.agenda_authorized


def test_relevant_event_without_discriminator_remains_unresolved() -> None:
    result = assess_encounter(
        EncounterCandidate(
            "link", "notebook", SurpriseVector(semantic=0.9),
            cross_problem_relevance=0.8, noise_risk=0.2, reproducible=True,
            discriminator_available=False, estimated_followup_cost=0,
        ),
        followup_budget=10,
    )
    assert result.status is EncounterStatus.RETAIN_UNRESOLVED


def test_instruction_identity_alone_does_not_establish_competence() -> None:
    result = assess_competence_transfer(
        CompetenceReceipt("r", "baking", "recipe-v1"),
        target_task_family="baking", target_context="humid-kitchen",
    )
    assert result.status is CompetenceTransferStatus.TEXT_ONLY_UNVERIFIED


def test_demonstrated_context_supports_bounded_competence_only() -> None:
    receipt = CompetenceReceipt(
        "r", "repair", "guide-v1", demonstrated_contexts=frozenset({"device-v1"}),
        state_discriminators=frozenset({"connector-shape", "battery-state"}),
        recovery_cases=frozenset({"stuck-connector"}),
    )
    exact = assess_competence_transfer(receipt, target_task_family="repair", target_context="device-v1")
    changed = assess_competence_transfer(
        receipt, target_task_family="repair", target_context="device-v2", context_relation_certified=True,
    )
    assert exact.status is CompetenceTransferStatus.VERIFIED_WITHIN_DEMONSTRATED_RANGE
    assert changed.status is CompetenceTransferStatus.REVALIDATE_CONTEXT_CHANGE


def test_observed_failure_context_blocks_competence_transfer() -> None:
    receipt = CompetenceReceipt(
        "r", "procedure", "instruction", demonstrated_contexts=frozenset({"lab-a"}),
        state_discriminators=frozenset({"temperature"}), failure_contexts=frozenset({"lab-b"}),
    )
    result = assess_competence_transfer(receipt, target_task_family="procedure", target_context="lab-b")
    assert result.status is CompetenceTransferStatus.NOT_TRANSFERRED


def test_dependent_review_with_state_change_is_uptake_but_not_independent() -> None:
    result = assess_criticism(
        CriticismReceipt(
            "crit", "claim", "critic", "shared dataset may duplicate evidence", "independence assumption",
            critic_dependencies=frozenset({"model-A", "dataset-X"}),
            subject_dependencies=frozenset({"model-A"}), state_delta=frozenset({"claim-narrowed"}),
        )
    )
    assert result.independence is ReviewIndependence.DEPENDENT
    assert result.outcome is CriticismOutcome.UPTAKE


def test_logged_objection_without_response_is_review_theatre() -> None:
    result = assess_criticism(
        CriticismReceipt(
            "crit", "claim", "critic", "objection", "assumption",
            critic_dependencies=frozenset({"critic-source"}),
            subject_dependencies=frozenset({"subject-source"}),
        )
    )
    assert result.independence is ReviewIndependence.INDEPENDENT
    assert result.outcome is CriticismOutcome.REVIEW_THEATRE


def test_evidence_based_rejection_of_criticism_is_not_theatre() -> None:
    result = assess_criticism(
        CriticismReceipt(
            "crit", "claim", "critic", "objection", "assumption",
            critic_dependencies=frozenset({"critic-source"}),
            subject_dependencies=frozenset({"subject-source"}),
            response_evidence_ids=frozenset({"known-answer"}),
            reason_no_change="known-answer evidence contradicts the objection",
        )
    )
    assert result.outcome is CriticismOutcome.EVIDENCE_BASED_REJECTION


def test_distributed_state_missing_at_decision_is_handoff_loss() -> None:
    result = assess_distributed_state(
        DistributedEpisode(
            "episode", "final-agent", frozenset({"calibration-warning", "sample-id"}),
            {
                "instrument": frozenset({"calibration-warning"}),
                "lab-notebook": frozenset({"sample-id"}),
                "final-agent": frozenset({"sample-id"}),
            },
        )
    )
    assert result.status is DistributedStateStatus.HANDOFF_LOSS
    assert result.missing_state == ("calibration-warning",)
    assert result.source_components == ("instrument",)


def test_state_missing_from_entire_episode_is_not_handoff_loss() -> None:
    result = assess_distributed_state(
        DistributedEpisode(
            "episode", "final-agent", frozenset({"unknown-calibration"}),
            {"final-agent": frozenset(), "instrument": frozenset({"raw-reading"})},
        )
    )
    assert result.status is DistributedStateStatus.SOURCE_STATE_MISSING
    assert result.missing_state == ("unknown-calibration",)


def test_complete_distributed_state_passes_without_authority() -> None:
    result = assess_distributed_state(
        DistributedEpisode(
            "episode", "final-agent", frozenset({"sample-id"}),
            {"final-agent": frozenset({"sample-id"})},
        )
    )
    assert result.status is DistributedStateStatus.COMPLETE_AT_DECISION
    assert not result.authority_granted


def test_missing_decision_component_returns_cannot_check() -> None:
    result = assess_distributed_state(
        DistributedEpisode(
            "episode", "missing-agent", frozenset({"sample-id"}),
            {"instrument": frozenset({"sample-id"})},
        )
    )
    assert result.status is DistributedStateStatus.CANNOT_CHECK
