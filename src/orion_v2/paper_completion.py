"""Fail-closed paper-completion and submission-readiness semantics.

This module distinguishes a fully written manuscript from completed science and
from a journal-ready submission package.  It deliberately cannot grant field
truth, journal acceptance, authorship, authority, or novelty.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Iterable


class EvidenceState(StrEnum):
    OPEN = "OPEN"
    REFERENCE_ONLY = "REFERENCE_ONLY"
    PROTECTED_RESULT = "PROTECTED_RESULT"
    INDEPENDENTLY_ADJUDICATED = "INDEPENDENTLY_ADJUDICATED"
    REPLICATED_OR_TRANSFERRED = "REPLICATED_OR_TRANSFERRED"
    CANNOT_CHECK = "CANNOT_CHECK"


class ReadinessLevel(IntEnum):
    R0_PROSPECTUS = 0
    R1_DESIGN_MANUSCRIPT = 1
    R2_REFERENCE_SEMANTICS = 2
    R3_PROTECTED_CROSS_DOMAIN_EVIDENCE = 3
    R4_SUBMISSION_READY = 4


class PaperDisposition(StrEnum):
    CONTINUE = "CONTINUE"
    SUBMISSION_CANDIDATE = "SUBMISSION_CANDIDATE"
    MERGE = "MERGE"
    PARENT_CONTRACTION = "PARENT_CONTRACTION"
    RESOURCE_OR_BENCHMARK = "RESOURCE_OR_BENCHMARK"
    REDUNDANT_DRAG = "REDUNDANT_DRAG"
    HARMFUL = "HARMFUL"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class PaperEvidenceUnit:
    unit_id: str
    state: EvidenceState
    central: bool = True
    independent: bool = False
    cross_domain_or_replication: bool = False
    retained_negative_or_parent_win: bool = True

    def __post_init__(self) -> None:
        if not self.unit_id.strip():
            raise ValueError("evidence units require a non-empty identity")
        object.__setattr__(self, "state", EvidenceState(self.state))
        if self.state is EvidenceState.INDEPENDENTLY_ADJUDICATED and not self.independent:
            raise ValueError("independently adjudicated evidence must be marked independent")
        if self.state is EvidenceState.REPLICATED_OR_TRANSFERRED:
            if not self.independent or not self.cross_domain_or_replication:
                raise ValueError(
                    "replicated/transferred evidence requires independent and cross-domain/replication flags"
                )


@dataclass(frozen=True, slots=True)
class PaperCompletionRecord:
    paper_id: str
    thesis_frozen: bool
    explicit_nonclaim: bool
    falsifier_or_kill_condition: bool
    strongest_parent_federation_specified: bool
    protocol_and_primary_estimands_frozen: bool
    result_slots_and_figure_spine_complete: bool
    manuscript_surface_complete: bool
    reference_semantics_replayable: bool
    strongest_parent_executed: bool
    resources_matched_or_curves_reported: bool
    independent_evaluation_complete: bool
    cross_domain_or_replication_complete: bool
    uncertainty_and_failure_analysis_complete: bool
    component_attribution_complete: bool
    reproducibility_package_complete: bool
    source_and_claim_audit_complete: bool
    target_format_audit_complete: bool
    disclosures_complete: bool
    hostile_editor_clear: bool
    unresolved_fatal_issue: bool
    evidence_units: tuple[PaperEvidenceUnit, ...] = ()
    disposition: PaperDisposition = PaperDisposition.CONTINUE
    journal_acceptance_granted: bool = False
    field_truth_granted: bool = False

    def __post_init__(self) -> None:
        if not self.paper_id.strip():
            raise ValueError("paper records require a non-empty identity")
        object.__setattr__(self, "disposition", PaperDisposition(self.disposition))
        if self.journal_acceptance_granted:
            raise ValueError("an internal completion record cannot grant journal acceptance")
        if self.field_truth_granted:
            raise ValueError("an internal completion record cannot grant field truth")


@dataclass(frozen=True, slots=True)
class PaperReadinessAssessment:
    paper_id: str
    level: ReadinessLevel
    blockers: tuple[str, ...]
    central_open_units: tuple[str, ...]
    disposition: PaperDisposition
    manuscript_complete: bool
    science_complete: bool
    submission_ready: bool
    journal_acceptance_granted: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "level", ReadinessLevel(self.level))
        object.__setattr__(self, "disposition", PaperDisposition(self.disposition))
        if self.journal_acceptance_granted:
            raise ValueError("readiness assessment cannot grant journal acceptance")
        if self.submission_ready and self.level is not ReadinessLevel.R4_SUBMISSION_READY:
            raise ValueError("submission_ready requires R4")
        if self.science_complete and self.level < ReadinessLevel.R3_PROTECTED_CROSS_DOMAIN_EVIDENCE:
            raise ValueError("science_complete requires at least R3")


def _central_open_units(
    units: Iterable[PaperEvidenceUnit],
) -> tuple[str, ...]:
    open_states = {
        EvidenceState.OPEN,
        EvidenceState.REFERENCE_ONLY,
        EvidenceState.CANNOT_CHECK,
    }
    return tuple(
        sorted(unit.unit_id for unit in units if unit.central and unit.state in open_states)
    )


def assess_paper_readiness(record: PaperCompletionRecord) -> PaperReadinessAssessment:
    """Return the highest evidence-backed readiness level.

    Fluent prose, a complete manuscript surface, and passing reference tests may
    reach R2 but can never substitute for protected results, independent review,
    cross-domain evidence, or a reproducibility package.
    """

    blockers: list[str] = []
    central_open = _central_open_units(record.evidence_units)

    r1 = all(
        (
            record.thesis_frozen,
            record.explicit_nonclaim,
            record.falsifier_or_kill_condition,
            record.strongest_parent_federation_specified,
            record.protocol_and_primary_estimands_frozen,
            record.result_slots_and_figure_spine_complete,
            record.manuscript_surface_complete,
        )
    )
    if not r1:
        level = ReadinessLevel.R0_PROSPECTUS
        for name, value in (
            ("thesis_frozen", record.thesis_frozen),
            ("explicit_nonclaim", record.explicit_nonclaim),
            ("falsifier_or_kill_condition", record.falsifier_or_kill_condition),
            ("strongest_parent_federation_specified", record.strongest_parent_federation_specified),
            ("protocol_and_primary_estimands_frozen", record.protocol_and_primary_estimands_frozen),
            ("result_slots_and_figure_spine_complete", record.result_slots_and_figure_spine_complete),
            ("manuscript_surface_complete", record.manuscript_surface_complete),
        ):
            if not value:
                blockers.append(name)
        return PaperReadinessAssessment(
            record.paper_id,
            level,
            tuple(blockers),
            central_open,
            record.disposition,
            record.manuscript_surface_complete,
            False,
            False,
        )

    level = ReadinessLevel.R1_DESIGN_MANUSCRIPT

    if record.reference_semantics_replayable:
        level = ReadinessLevel.R2_REFERENCE_SEMANTICS
    else:
        blockers.append("reference_semantics_replayable")

    r3_requirements = {
        "strongest_parent_executed": record.strongest_parent_executed,
        "resources_matched_or_curves_reported": record.resources_matched_or_curves_reported,
        "independent_evaluation_complete": record.independent_evaluation_complete,
        "cross_domain_or_replication_complete": record.cross_domain_or_replication_complete,
        "uncertainty_and_failure_analysis_complete": record.uncertainty_and_failure_analysis_complete,
        "component_attribution_complete": record.component_attribution_complete,
        "central_evidence_units_closed": not central_open,
        "negative_parent_win_retention": all(
            unit.retained_negative_or_parent_win for unit in record.evidence_units
        ),
        "no_unresolved_fatal_issue": not record.unresolved_fatal_issue,
    }
    if all(r3_requirements.values()):
        level = ReadinessLevel.R3_PROTECTED_CROSS_DOMAIN_EVIDENCE
    else:
        blockers.extend(name for name, value in r3_requirements.items() if not value)

    r4_requirements = {
        "reproducibility_package_complete": record.reproducibility_package_complete,
        "source_and_claim_audit_complete": record.source_and_claim_audit_complete,
        "target_format_audit_complete": record.target_format_audit_complete,
        "disclosures_complete": record.disclosures_complete,
        "hostile_editor_clear": record.hostile_editor_clear,
    }
    if level is ReadinessLevel.R3_PROTECTED_CROSS_DOMAIN_EVIDENCE:
        if all(r4_requirements.values()):
            level = ReadinessLevel.R4_SUBMISSION_READY
        else:
            blockers.extend(name for name, value in r4_requirements.items() if not value)

    science_complete = level >= ReadinessLevel.R3_PROTECTED_CROSS_DOMAIN_EVIDENCE
    submission_ready = level is ReadinessLevel.R4_SUBMISSION_READY

    return PaperReadinessAssessment(
        record.paper_id,
        level,
        tuple(dict.fromkeys(blockers)),
        central_open,
        record.disposition,
        record.manuscript_surface_complete,
        science_complete,
        submission_ready,
    )
