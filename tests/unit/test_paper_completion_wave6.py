import pytest

from orion_v2.paper_completion import (
    EvidenceState,
    PaperCompletionRecord,
    PaperDisposition,
    PaperEvidenceUnit,
    ReadinessLevel,
    assess_paper_readiness,
)


def _record(**overrides: object) -> PaperCompletionRecord:
    values: dict[str, object] = {
        "paper_id": "P-X",
        "thesis_frozen": True,
        "explicit_nonclaim": True,
        "falsifier_or_kill_condition": True,
        "strongest_parent_federation_specified": True,
        "protocol_and_primary_estimands_frozen": True,
        "result_slots_and_figure_spine_complete": True,
        "manuscript_surface_complete": True,
        "reference_semantics_replayable": True,
        "strongest_parent_executed": False,
        "resources_matched_or_curves_reported": False,
        "independent_evaluation_complete": False,
        "cross_domain_or_replication_complete": False,
        "uncertainty_and_failure_analysis_complete": False,
        "component_attribution_complete": False,
        "reproducibility_package_complete": False,
        "source_and_claim_audit_complete": False,
        "target_format_audit_complete": False,
        "disclosures_complete": False,
        "hostile_editor_clear": False,
        "unresolved_fatal_issue": False,
        "evidence_units": (
            PaperEvidenceUnit("central-result", EvidenceState.OPEN),
        ),
        "disposition": PaperDisposition.CONTINUE,
    }
    values.update(overrides)
    return PaperCompletionRecord(**values)  # type: ignore[arg-type]


def test_complete_prose_and_reference_semantics_stop_at_r2() -> None:
    result = assess_paper_readiness(_record())
    assert result.level is ReadinessLevel.R2_REFERENCE_SEMANTICS
    assert result.manuscript_complete
    assert not result.science_complete
    assert not result.submission_ready
    assert result.central_open_units == ("central-result",)


def test_open_central_evidence_blocks_r3() -> None:
    result = assess_paper_readiness(
        _record(
            strongest_parent_executed=True,
            resources_matched_or_curves_reported=True,
            independent_evaluation_complete=True,
            cross_domain_or_replication_complete=True,
            uncertainty_and_failure_analysis_complete=True,
            component_attribution_complete=True,
        )
    )
    assert result.level is ReadinessLevel.R2_REFERENCE_SEMANTICS
    assert "central_evidence_units_closed" in result.blockers


def test_protected_cross_domain_evidence_reaches_r3_not_r4() -> None:
    units = (
        PaperEvidenceUnit(
            "central-result",
            EvidenceState.REPLICATED_OR_TRANSFERRED,
            independent=True,
            cross_domain_or_replication=True,
        ),
    )
    result = assess_paper_readiness(
        _record(
            strongest_parent_executed=True,
            resources_matched_or_curves_reported=True,
            independent_evaluation_complete=True,
            cross_domain_or_replication_complete=True,
            uncertainty_and_failure_analysis_complete=True,
            component_attribution_complete=True,
            evidence_units=units,
        )
    )
    assert result.level is ReadinessLevel.R3_PROTECTED_CROSS_DOMAIN_EVIDENCE
    assert result.science_complete
    assert not result.submission_ready
    assert "reproducibility_package_complete" in result.blockers


def test_full_submission_package_reaches_r4_but_not_acceptance() -> None:
    units = (
        PaperEvidenceUnit(
            "central-result",
            EvidenceState.REPLICATED_OR_TRANSFERRED,
            independent=True,
            cross_domain_or_replication=True,
        ),
    )
    result = assess_paper_readiness(
        _record(
            strongest_parent_executed=True,
            resources_matched_or_curves_reported=True,
            independent_evaluation_complete=True,
            cross_domain_or_replication_complete=True,
            uncertainty_and_failure_analysis_complete=True,
            component_attribution_complete=True,
            reproducibility_package_complete=True,
            source_and_claim_audit_complete=True,
            target_format_audit_complete=True,
            disclosures_complete=True,
            hostile_editor_clear=True,
            evidence_units=units,
            disposition=PaperDisposition.SUBMISSION_CANDIDATE,
        )
    )
    assert result.level is ReadinessLevel.R4_SUBMISSION_READY
    assert result.submission_ready
    assert not result.journal_acceptance_granted


def test_unresolved_fatal_issue_blocks_r3() -> None:
    units = (
        PaperEvidenceUnit(
            "central-result",
            EvidenceState.REPLICATED_OR_TRANSFERRED,
            independent=True,
            cross_domain_or_replication=True,
        ),
    )
    result = assess_paper_readiness(
        _record(
            strongest_parent_executed=True,
            resources_matched_or_curves_reported=True,
            independent_evaluation_complete=True,
            cross_domain_or_replication_complete=True,
            uncertainty_and_failure_analysis_complete=True,
            component_attribution_complete=True,
            unresolved_fatal_issue=True,
            evidence_units=units,
        )
    )
    assert result.level is ReadinessLevel.R2_REFERENCE_SEMANTICS
    assert "no_unresolved_fatal_issue" in result.blockers


def test_hiding_negative_or_parent_win_blocks_r3() -> None:
    units = (
        PaperEvidenceUnit(
            "central-result",
            EvidenceState.REPLICATED_OR_TRANSFERRED,
            independent=True,
            cross_domain_or_replication=True,
            retained_negative_or_parent_win=False,
        ),
    )
    result = assess_paper_readiness(
        _record(
            strongest_parent_executed=True,
            resources_matched_or_curves_reported=True,
            independent_evaluation_complete=True,
            cross_domain_or_replication_complete=True,
            uncertainty_and_failure_analysis_complete=True,
            component_attribution_complete=True,
            evidence_units=units,
        )
    )
    assert result.level is ReadinessLevel.R2_REFERENCE_SEMANTICS
    assert "negative_parent_win_retention" in result.blockers


def test_internal_record_cannot_grant_acceptance_or_field_truth() -> None:
    with pytest.raises(ValueError):
        _record(journal_acceptance_granted=True)
    with pytest.raises(ValueError):
        _record(field_truth_granted=True)


def test_replicated_evidence_requires_independence_and_transfer_flag() -> None:
    with pytest.raises(ValueError):
        PaperEvidenceUnit(
            "bad",
            EvidenceState.REPLICATED_OR_TRANSFERRED,
            independent=False,
            cross_domain_or_replication=True,
        )
