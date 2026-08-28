import pytest

from orion_v2.foundation_saturation import (
    REQUIRED_CLEAN_PASSES,
    FindingKind,
    FoundationSaturationStatus,
    RouteDisposition,
    SaturationPassReceipt,
    SearchRouteReceipt,
    assess_foundation_saturation,
)


def _complete_route(route_id: str, family: str = "F1") -> SearchRouteReceipt:
    return SearchRouteReceipt(
        route_id,
        family,
        RouteDisposition.COMPLETE,
        ("source",),
    )


def _clean_pass(
    pass_id: str,
    families: frozenset[str] = frozenset({"F1"}),
) -> SaturationPassReceipt:
    return SaturationPassReceipt(
        pass_id,
        families,
        True,
        True,
        True,
        (FindingKind.NONE,),
    )


def test_canonical_rule_requires_three_clean_passes() -> None:
    assert REQUIRED_CLEAN_PASSES == 3
    result = assess_foundation_saturation(
        {"F1"},
        (_complete_route("r"),),
        (_clean_pass("p1"), _clean_pass("p2")),
    )
    assert result.status is FoundationSaturationStatus.OPEN_COVERAGE
    assert result.consecutive_no_material_passes == 2
    assert result.required_no_material_passes == 3


def test_three_clean_full_passes_allow_internal_synthesis() -> None:
    result = assess_foundation_saturation(
        {"F1"},
        (_complete_route("r"),),
        (_clean_pass("p1"), _clean_pass("p2"), _clean_pass("p3")),
    )
    assert result.status is FoundationSaturationStatus.READY_FOR_INTERNAL_SYNTHESIS
    assert result.consecutive_no_material_passes == 3
    assert result.internal_synthesis_allowed
    assert not result.external_demarcation_ready
    assert not result.field_authority_granted


def test_complete_route_requires_source_identity() -> None:
    with pytest.raises(ValueError):
        SearchRouteReceipt("r", "F1", RouteDisposition.COMPLETE)


def test_censored_route_requires_reason() -> None:
    with pytest.raises(ValueError):
        SearchRouteReceipt("r", "F1", RouteDisposition.CENSORED)


def test_none_cannot_mix_with_material_finding() -> None:
    with pytest.raises(ValueError):
        SaturationPassReceipt(
            "p",
            frozenset({"F1"}),
            True,
            True,
            True,
            (FindingKind.NONE, FindingKind.COORDINATE),
        )


def test_material_finding_reopens_and_resets_clean_counter() -> None:
    material = SaturationPassReceipt(
        "p3",
        frozenset({"F1"}),
        True,
        True,
        True,
        (FindingKind.COORDINATE, FindingKind.BENCHMARK),
    )
    result = assess_foundation_saturation(
        {"F1"},
        (_complete_route("r"),),
        (_clean_pass("p1"), _clean_pass("p2"), material),
    )
    assert result.status is FoundationSaturationStatus.REOPENED_MATERIAL_FINDING
    assert result.consecutive_no_material_passes == 0
    assert result.latest_material_findings == (
        FindingKind.COORDINATE,
        FindingKind.BENCHMARK,
    )
    assert not result.internal_synthesis_allowed


def test_open_route_blocks_internal_synthesis() -> None:
    routes = (
        _complete_route("r1"),
        SearchRouteReceipt("r2", "F1", RouteDisposition.OPEN),
    )
    result = assess_foundation_saturation(
        {"F1"},
        routes,
        (_clean_pass("p1"), _clean_pass("p2"), _clean_pass("p3")),
    )
    assert result.status is FoundationSaturationStatus.OPEN_COVERAGE
    assert result.open_route_ids == ("r2",)


def test_uncovered_family_blocks_internal_synthesis() -> None:
    families = frozenset({"F1", "F2"})
    result = assess_foundation_saturation(
        families,
        (_complete_route("r1", "F1"),),
        (
            _clean_pass("p1", families),
            _clean_pass("p2", families),
            _clean_pass("p3", families),
        ),
    )
    assert result.status is FoundationSaturationStatus.OPEN_COVERAGE
    assert result.open_family_ids == ("F2",)


def test_external_review_advances_demarcation_but_never_authority() -> None:
    result = assess_foundation_saturation(
        {"F1"},
        (_complete_route("r"),),
        (_clean_pass("p1"), _clean_pass("p2"), _clean_pass("p3")),
        external_review_complete=True,
    )
    assert result.status is FoundationSaturationStatus.READY_FOR_EXTERNAL_DEMARCATION
    assert result.external_demarcation_ready
    assert result.internal_synthesis_allowed
    assert not result.field_authority_granted


def test_censored_routes_remain_visible_without_becoming_negative_evidence() -> None:
    routes = (
        _complete_route("r1"),
        SearchRouteReceipt(
            "r-censored",
            "F1",
            RouteDisposition.CENSORED,
            censor_reason="custodial access unavailable",
        ),
    )
    result = assess_foundation_saturation(
        {"F1"},
        routes,
        (_clean_pass("p1"), _clean_pass("p2"), _clean_pass("p3")),
    )
    assert result.status is FoundationSaturationStatus.READY_FOR_INTERNAL_SYNTHESIS
    assert result.censored_route_ids == ("r-censored",)


def test_missing_evidence_returns_cannot_check() -> None:
    result = assess_foundation_saturation({"F1"}, (), ())
    assert result.status is FoundationSaturationStatus.CANNOT_CHECK
    assert not result.internal_synthesis_allowed
