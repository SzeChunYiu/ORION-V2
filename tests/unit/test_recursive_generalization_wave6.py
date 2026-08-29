from orion_v2.recursive_generalization import (
    GeneralizationEvidence,
    RecursiveGeneralizationStatus,
    RecursiveStabilityEvidence,
    assess_higher_abstraction,
    assess_recursive_stability,
)


def test_higher_level_requires_material_residual():
    receipt = assess_higher_abstraction(
        "L2-to-L3",
        from_level=2,
        evidence=GeneralizationEvidence(
            strongest_parent_executed=True,
            strongest_parent_sufficient=False,
            heldout_prediction_gain=0.0,
            heldout_transfer_gain=0.0,
            compression_gain=0.0,
            critical_information_loss=False,
            prospective_decision_gain=0.0,
            resource_delta=0.0,
            hostile_omission_challenge_pass=True,
        ),
    )
    assert receipt.status is RecursiveGeneralizationStatus.NO_HIGHER_LEVEL_RESIDUAL


def test_critical_loss_blocks_even_when_prediction_gain_is_large():
    receipt = assess_higher_abstraction(
        "bad-compression",
        from_level=3,
        evidence=GeneralizationEvidence(
            strongest_parent_executed=True,
            strongest_parent_sufficient=False,
            heldout_prediction_gain=1.0,
            heldout_transfer_gain=1.0,
            compression_gain=1.0,
            critical_information_loss=True,
            prospective_decision_gain=1.0,
            resource_delta=-1.0,
            hostile_omission_challenge_pass=True,
        ),
    )
    assert receipt.status is RecursiveGeneralizationStatus.BLOCKED_CRITICAL_LOSS


def test_prospective_higher_level_residual_is_not_ultimate_truth():
    receipt = assess_higher_abstraction(
        "good-meta",
        from_level=4,
        evidence=GeneralizationEvidence(
            strongest_parent_executed=True,
            strongest_parent_sufficient=False,
            heldout_prediction_gain=0.1,
            heldout_transfer_gain=0.2,
            compression_gain=0.1,
            critical_information_loss=False,
            prospective_decision_gain=0.15,
            resource_delta=0.0,
            hostile_omission_challenge_pass=True,
        ),
    )
    assert receipt.status is RecursiveGeneralizationStatus.PROSPECTIVE_HIGHER_LEVEL_RESIDUAL
    assert not receipt.ultimate_truth_authorized


def test_recursive_stability_requires_another_failed_generalization_pass_and_challenges():
    receipt = assess_recursive_stability(
        RecursiveStabilityEvidence(
            latest_level=7,
            attempted_next_level=True,
            material_next_level_residual=False,
            new_domain_challenge_pass=True,
            new_epoch_challenge_pass=True,
            hostile_omission_challenge_pass=True,
            unresolved_route_ids=("unpublished-negative-results",),
        )
    )
    assert receipt.status is RecursiveGeneralizationStatus.RECURSIVE_STABILITY_CANDIDATE
    assert "unpublished-negative-results" in " ".join(receipt.reasons)
