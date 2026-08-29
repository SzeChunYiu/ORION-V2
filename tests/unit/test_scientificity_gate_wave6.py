from orion_v2.scientificity_gate import (
    ScientificityEvidence,
    ScientificityLevel,
    assess_claim_promotion,
)


def test_metaphor_cannot_be_promoted_to_result() -> None:
    result = assess_claim_promotion(
        ScientificityEvidence(ScientificityLevel.S0_INSPIRATION_OR_METAPHOR),
        ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT,
    )
    assert not result.allowed
    assert result.maximum_level is ScientificityLevel.S0_INSPIRATION_OR_METAPHOR
    assert not result.field_status_granted


def test_unfrozen_confirmatory_claim_falls_back_to_hypothesis() -> None:
    result = assess_claim_promotion(
        ScientificityEvidence(
            ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT,
            strongest_parent_compared=True,
            negative_control_present=True,
        ),
        ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT,
    )
    assert not result.allowed
    assert result.maximum_level is ScientificityLevel.S2_DISCRIMINATING_HYPOTHESIS


def test_result_requires_parent_and_negative_control() -> None:
    result = assess_claim_promotion(
        ScientificityEvidence(
            ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT,
            preregistered_or_frozen=True,
        ),
        ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT,
    )
    assert not result.allowed
    assert result.maximum_level is ScientificityLevel.S2_DISCRIMINATING_HYPOTHESIS


def test_valid_bounded_result_can_reach_s3() -> None:
    evidence = ScientificityEvidence(
        ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT,
        preregistered_or_frozen=True,
        strongest_parent_compared=True,
        negative_control_present=True,
    )
    result = assess_claim_promotion(evidence, ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT)
    assert result.allowed
    assert result.maximum_level is ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT
    assert not result.superiority_granted


def test_same_study_without_independence_cannot_reach_s4() -> None:
    evidence = ScientificityEvidence(
        ScientificityLevel.S4_INDEPENDENTLY_REPLICATED_OR_CROSS_DOMAIN,
        preregistered_or_frozen=True,
        strongest_parent_compared=True,
        negative_control_present=True,
        independent_evaluation=False,
        cross_domain_or_replication=True,
        robustness_audit=True,
    )
    result = assess_claim_promotion(
        evidence,
        ScientificityLevel.S4_INDEPENDENTLY_REPLICATED_OR_CROSS_DOMAIN,
    )
    assert not result.allowed
    assert result.maximum_level is ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT


def test_cross_domain_without_robustness_audit_cannot_reach_s4() -> None:
    evidence = ScientificityEvidence(
        ScientificityLevel.S4_INDEPENDENTLY_REPLICATED_OR_CROSS_DOMAIN,
        preregistered_or_frozen=True,
        strongest_parent_compared=True,
        negative_control_present=True,
        independent_evaluation=True,
        cross_domain_or_replication=True,
        robustness_audit=False,
    )
    result = assess_claim_promotion(
        evidence,
        ScientificityLevel.S4_INDEPENDENTLY_REPLICATED_OR_CROSS_DOMAIN,
    )
    assert not result.allowed
    assert result.maximum_level is ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT


def test_full_independent_cross_domain_evidence_can_reach_s5_candidate() -> None:
    evidence = ScientificityEvidence(
        ScientificityLevel.S5_FOUNDATION_PROPOSITION_CANDIDATE,
        preregistered_or_frozen=True,
        strongest_parent_compared=True,
        negative_control_present=True,
        independent_evaluation=True,
        cross_domain_or_replication=True,
        robustness_audit=True,
        critical_failure_open=False,
    )
    result = assess_claim_promotion(
        evidence,
        ScientificityLevel.S5_FOUNDATION_PROPOSITION_CANDIDATE,
    )
    assert result.allowed
    assert result.maximum_level is ScientificityLevel.S5_FOUNDATION_PROPOSITION_CANDIDATE
    assert not result.field_status_granted
    assert not result.publication_readiness_granted


def test_open_critical_failure_blocks_empirical_promotion() -> None:
    evidence = ScientificityEvidence(
        ScientificityLevel.S4_INDEPENDENTLY_REPLICATED_OR_CROSS_DOMAIN,
        preregistered_or_frozen=True,
        strongest_parent_compared=True,
        negative_control_present=True,
        independent_evaluation=True,
        cross_domain_or_replication=True,
        robustness_audit=True,
        critical_failure_open=True,
    )
    result = assess_claim_promotion(
        evidence,
        ScientificityLevel.S3_PROSPECTIVELY_TESTED_RESULT,
    )
    assert not result.allowed
    assert result.maximum_level is ScientificityLevel.S2_DISCRIMINATING_HYPOTHESIS
