import pytest

from orion_v2.epistemic_architecture import EpistemicAction
from orion_v2.ontic_epistemic_boundary import (
    DiscrepancyLocus,
    LocusDiagnosisEvidence,
    LocusDiagnosisReceipt,
    LocusDiagnosisStatus,
    LocusHypothesis,
    OnticEpistemicDelta,
    WorldObservationBoundary,
    assess_discrepancy_locus,
)


def _hypothesis(hypothesis_id: str, locus: DiscrepancyLocus) -> LocusHypothesis:
    return LocusHypothesis(
        hypothesis_id=hypothesis_id,
        locus=locus,
        witness_ids=(f"witness:{hypothesis_id}",),
        discriminator_ids=(f"probe:{hypothesis_id}",),
        falsifier_ids=(f"falsifier:{hypothesis_id}",),
    )


def test_world_boundary_is_observation_interface_not_direct_world_access() -> None:
    boundary = WorldObservationBoundary(
        boundary_id="boundary:lab",
        target_id="target:sample",
        observation_channel_ids=("channel:spectrometer",),
        instrument_or_interface_ids=("instrument:spec-1",),
        context_ids=("context:temperature-298K",),
    )
    assert boundary.target_id == "target:sample"
    assert boundary.observation_channel_ids == ("channel:spectrometer",)


def test_static_target_can_coexist_with_epistemic_learning() -> None:
    delta = OnticEpistemicDelta(
        transition_id="transition:new-evidence",
        target_changed=False,
        observation_channel_changed=False,
        epistemic_state_changed=True,
        generative_regime_changed=False,
        process_or_tool_changed=False,
    )
    assert delta.target_changed is False
    assert delta.epistemic_state_changed is True


def test_target_change_record_does_not_self_authorize_machine_knowledge() -> None:
    target = _hypothesis("h:target", DiscrepancyLocus.TARGET_WORLD)
    model = _hypothesis("h:model", DiscrepancyLocus.EPISTEMIC_MODEL)
    receipt = assess_discrepancy_locus(
        (target, model),
        LocusDiagnosisEvidence(
            discrepancy_witness_ids=("witness:disagreement",),
            supported_hypothesis_ids=("h:target",),
            defeated_hypothesis_ids=(),
            unresolved_hypothesis_ids=("h:model",),
            evaluator_adequate=True,
        ),
    )
    assert receipt.status is LocusDiagnosisStatus.MULTIPLE_LIVE_LOCUS_HYPOTHESES
    assert receipt.target_change_authorized is False


def test_measurement_drift_is_distinct_from_model_failure() -> None:
    measurement = _hypothesis("h:measurement", DiscrepancyLocus.OBSERVATION_MEASUREMENT)
    model = _hypothesis("h:model", DiscrepancyLocus.EPISTEMIC_MODEL)
    receipt = assess_discrepancy_locus(
        (measurement, model),
        LocusDiagnosisEvidence(
            discrepancy_witness_ids=("witness:calibration-shift",),
            supported_hypothesis_ids=("h:measurement",),
            defeated_hypothesis_ids=("h:model",),
            evaluator_adequate=True,
        ),
    )
    assert receipt.status is LocusDiagnosisStatus.ACTIONABLE_LOCUS_HYPOTHESIS
    assert receipt.live_loci == (DiscrepancyLocus.OBSERVATION_MEASUREMENT,)
    assert EpistemicAction.MEASURE in receipt.candidate_actions
    assert EpistemicAction.CHANGE_MODEL not in receipt.candidate_actions


def test_representation_locus_only_suggests_existing_escalation_family() -> None:
    representation = _hypothesis("h:representation", DiscrepancyLocus.REPRESENTATION_REGIME)
    search = _hypothesis("h:process", DiscrepancyLocus.PROCESS_TOOL_WORKFLOW)
    receipt = assess_discrepancy_locus(
        (representation, search),
        LocusDiagnosisEvidence(
            discrepancy_witness_ids=("witness:expressive-ceiling",),
            supported_hypothesis_ids=("h:representation",),
            defeated_hypothesis_ids=("h:process",),
            evaluator_adequate=True,
        ),
    )
    assert receipt.status is LocusDiagnosisStatus.ACTIONABLE_LOCUS_HYPOTHESIS
    assert EpistemicAction.CHANGE_REPRESENTATION in receipt.candidate_actions
    assert receipt.action_adoption_authorized is False


def test_problem_criterion_misspecification_suggests_reformulation_not_model_change() -> None:
    problem = _hypothesis("h:problem", DiscrepancyLocus.PROBLEM_CRITERION)
    model = _hypothesis("h:model", DiscrepancyLocus.EPISTEMIC_MODEL)
    receipt = assess_discrepancy_locus(
        (problem, model),
        LocusDiagnosisEvidence(
            discrepancy_witness_ids=("witness:wrong-specification",),
            supported_hypothesis_ids=("h:problem",),
            defeated_hypothesis_ids=("h:model",),
            evaluator_adequate=True,
        ),
    )
    assert receipt.status is LocusDiagnosisStatus.ACTIONABLE_LOCUS_HYPOTHESIS
    assert EpistemicAction.REFORMULATE_PROBLEM in receipt.candidate_actions
    assert EpistemicAction.CHANGE_MODEL not in receipt.candidate_actions


def test_evaluator_failure_is_not_silently_collapsed_into_measurement_or_model() -> None:
    evaluator = _hypothesis("h:evaluator", DiscrepancyLocus.EVALUATOR_VALIDATION)
    measurement = _hypothesis("h:measurement", DiscrepancyLocus.OBSERVATION_MEASUREMENT)
    receipt = assess_discrepancy_locus(
        (evaluator, measurement),
        LocusDiagnosisEvidence(
            discrepancy_witness_ids=("witness:blind-oracle",),
            supported_hypothesis_ids=("h:evaluator",),
            defeated_hypothesis_ids=("h:measurement",),
            evaluator_adequate=True,
        ),
    )
    assert receipt.status is LocusDiagnosisStatus.ACTIONABLE_LOCUS_HYPOTHESIS
    assert receipt.live_loci == (DiscrepancyLocus.EVALUATOR_VALIDATION,)
    assert EpistemicAction.CHALLENGE in receipt.candidate_actions
    assert EpistemicAction.CHANGE_MODEL not in receipt.candidate_actions


def test_ambiguous_loci_remain_plural_instead_of_forcing_one_cause() -> None:
    measurement = _hypothesis("h:measurement", DiscrepancyLocus.OBSERVATION_MEASUREMENT)
    model = _hypothesis("h:model", DiscrepancyLocus.EPISTEMIC_MODEL)
    receipt = assess_discrepancy_locus(
        (measurement, model),
        LocusDiagnosisEvidence(
            discrepancy_witness_ids=("witness:residual",),
            supported_hypothesis_ids=("h:measurement", "h:model"),
            evaluator_adequate=True,
        ),
    )
    assert receipt.status is LocusDiagnosisStatus.MULTIPLE_LIVE_LOCUS_HYPOTHESES
    assert set(receipt.live_loci) == {
        DiscrepancyLocus.OBSERVATION_MEASUREMENT,
        DiscrepancyLocus.EPISTEMIC_MODEL,
    }


def test_blind_evaluator_returns_cannot_identify() -> None:
    target = _hypothesis("h:target", DiscrepancyLocus.TARGET_WORLD)
    measurement = _hypothesis("h:measurement", DiscrepancyLocus.OBSERVATION_MEASUREMENT)
    receipt = assess_discrepancy_locus(
        (target, measurement),
        LocusDiagnosisEvidence(
            discrepancy_witness_ids=("witness:drift",),
            unresolved_hypothesis_ids=("h:target", "h:measurement"),
            evaluator_adequate=False,
        ),
    )
    assert receipt.status is LocusDiagnosisStatus.CANNOT_IDENTIFY


def test_no_discrepancy_witness_blocks_locus_diagnosis() -> None:
    model = _hypothesis("h:model", DiscrepancyLocus.EPISTEMIC_MODEL)
    receipt = assess_discrepancy_locus(
        (model,),
        LocusDiagnosisEvidence(
            discrepancy_witness_ids=(),
            supported_hypothesis_ids=("h:model",),
            evaluator_adequate=True,
        ),
    )
    assert receipt.status is LocusDiagnosisStatus.NO_DISCREPANCY_WITNESSED
    assert receipt.candidate_actions == ()


def test_locus_receipt_cannot_authorize_truth_or_adoption() -> None:
    with pytest.raises(ValueError, match="non-authorizing"):
        LocusDiagnosisReceipt(
            status=LocusDiagnosisStatus.ACTIONABLE_LOCUS_HYPOTHESIS,
            live_hypothesis_ids=("h:model",),
            live_loci=(DiscrepancyLocus.EPISTEMIC_MODEL,),
            candidate_actions=(EpistemicAction.CHANGE_MODEL,),
            reasons=("test",),
            scientific_truth_authorized=True,
        )
