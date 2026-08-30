import pytest

from orion_v2.epistemic_architecture import CapabilityContext
from orion_v2.epistemic_atlas import (
    AtlasGluingReceipt,
    EpistemicContext,
    GlobalityClaim,
    GlobalityLevel,
    GluingStatus,
    HorizonStatus,
    LocalEpistemicChart,
    OverlapAssessment,
    ProbeOutcome,
    UnknownKind,
    UnknownRecord,
    assess_atlas_gluing,
    assess_probe_expansion,
    globality_levels,
    observational_partition,
)


def _capability_context(tag: str) -> CapabilityContext:
    return CapabilityContext(
        environment_ids=(f"env:{tag}",),
        task_family_ids=(f"task:{tag}",),
        resource_regime_ids=(f"resource:{tag}",),
        system_boundary_ids=(f"boundary:{tag}",),
        substrate_or_interface_ids=(f"substrate:{tag}",),
        timescale_ids=(f"timescale:{tag}",),
        criterion_ids=(f"criterion:{tag}",),
    )


def test_epistemic_context_requires_explicit_authority_context() -> None:
    context = EpistemicContext("context:h", _capability_context("h"), ("authority:science",))
    assert context.context_id == "context:h"
    assert context.authority_context_ids == ("authority:science",)


def test_pairwise_compatibility_does_not_self_grant_global_section() -> None:
    charts = (
        LocalEpistemicChart("chart:h", "context:h", ("state:h",)),
        LocalEpistemicChart("chart:m", "context:m", ("state:m",)),
    )
    overlaps = (
        OverlapAssessment("overlap:hm", "chart:h", "chart:m", True, ("witness:translation",)),
    )
    receipt = assess_atlas_gluing(charts, overlaps)
    assert isinstance(receipt, AtlasGluingReceipt)
    assert receipt.status is GluingStatus.MATCHING_FAMILY_ONLY
    assert receipt.global_section_witness_id == ""
    assert receipt.scientific_truth_authorized is False


def test_incompatible_overlap_is_a_local_to_global_obstruction() -> None:
    charts = (
        LocalEpistemicChart("chart:a", "context:a", ("state:a",)),
        LocalEpistemicChart("chart:b", "context:b", ("state:b",)),
    )
    overlaps = (
        OverlapAssessment("overlap:ab", "chart:a", "chart:b", False, ("counterexample:ab",)),
    )
    receipt = assess_atlas_gluing(charts, overlaps)
    assert receipt.status is GluingStatus.GLOBAL_SECTION_OBSTRUCTED
    assert "overlap:ab" in receipt.reasons[0]


def test_global_section_requires_a_separate_witness() -> None:
    charts = (
        LocalEpistemicChart("chart:a", "context:a", ("state:a",)),
        LocalEpistemicChart("chart:b", "context:b", ("state:b",)),
    )
    overlaps = (
        OverlapAssessment("overlap:ab", "chart:a", "chart:b", True, ("witness:ab",)),
    )
    receipt = assess_atlas_gluing(charts, overlaps, global_section_witness_id="witness:global")
    assert receipt.status is GluingStatus.GLOBAL_SECTION_WITNESSED
    assert receipt.global_section_witness_id == "witness:global"


def test_probe_expansion_can_strictly_refine_observational_horizon() -> None:
    before = (
        ProbeOutcome("probe:p1", "candidate:a", "same"),
        ProbeOutcome("probe:p1", "candidate:b", "same"),
        ProbeOutcome("probe:p1", "candidate:c", "other"),
    )
    after = before + (
        ProbeOutcome("probe:p2", "candidate:a", "left"),
        ProbeOutcome("probe:p2", "candidate:b", "right"),
        ProbeOutcome("probe:p2", "candidate:c", "other"),
    )
    receipt = assess_probe_expansion(before, after)
    assert receipt.status is HorizonStatus.PROBE_REFINES_HORIZON
    assert observational_partition(before) == (("candidate:a", "candidate:b"), ("candidate:c",))
    assert observational_partition(after) == (("candidate:a",), ("candidate:b",), ("candidate:c",))


def test_probe_table_must_be_a_complete_candidate_by_probe_grid() -> None:
    with pytest.raises(ValueError, match="full candidate-by-probe grid"):
        observational_partition(
            (
                ProbeOutcome("p1", "a", "x"),
                ProbeOutcome("p1", "b", "x"),
                ProbeOutcome("p2", "a", "y"),
            )
        )


def test_outside_current_atlas_is_a_witnessed_sentinel_not_an_enumerated_complement() -> None:
    record = UnknownRecord(
        "unknown:residual",
        UnknownKind.OUTSIDE_CURRENT_ATLAS,
        ("obstruction:persistent-residual",),
    )
    assert record.kind is UnknownKind.OUTSIDE_CURRENT_ATLAS
    with pytest.raises(ValueError):
        UnknownRecord("unknown:empty", UnknownKind.OUTSIDE_CURRENT_ATLAS, ())


def test_globality_ladder_has_no_empirical_absolute_global_level() -> None:
    values = {level.value for level in globality_levels()}
    assert "ABSOLUTE_GLOBAL" not in values
    assert GlobalityLevel.FORMAL_UNIVERSE_THEOREM.value in values


def test_g4_universality_requires_explicit_formal_universe_and_theorem() -> None:
    with pytest.raises(ValueError, match="formal universe"):
        GlobalityClaim(
            "claim:bad",
            GlobalityLevel.FORMAL_UNIVERSE_THEOREM,
            ("context:a",),
        )
    claim = GlobalityClaim(
        "claim:formal",
        GlobalityLevel.FORMAL_UNIVERSE_THEOREM,
        ("context:a",),
        formal_universe_id="universe:finite-class",
        theorem_witness_id="proof:all-cases",
    )
    assert claim.level is GlobalityLevel.FORMAL_UNIVERSE_THEOREM


def test_atlas_robustness_requires_transport_and_hostile_challenge() -> None:
    with pytest.raises(ValueError, match="hostile"):
        GlobalityClaim(
            "claim:g3",
            GlobalityLevel.ATLAS_ROBUST,
            ("context:a", "context:b"),
            transport_relation_ids=("transport:ab",),
        )
    claim = GlobalityClaim(
        "claim:g3-ok",
        GlobalityLevel.ATLAS_ROBUST,
        ("context:a", "context:b"),
        transport_relation_ids=("transport:ab",),
        hostile_chart_or_probe_ids=("hostile:new-chart",),
    )
    assert claim.level is GlobalityLevel.ATLAS_ROBUST
