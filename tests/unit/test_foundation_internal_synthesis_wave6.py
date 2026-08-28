import json
from pathlib import Path

from orion_v2.foundation_saturation import (
    FindingKind,
    FoundationSaturationStatus,
    RouteDisposition,
    SaturationPassReceipt,
    SearchRouteReceipt,
    assess_foundation_saturation,
)


FAMILIES = frozenset(f"F{index:02d}" for index in range(1, 23))


def _complete_family_routes() -> tuple[SearchRouteReceipt, ...]:
    receipts: list[SearchRouteReceipt] = []
    for family_id in sorted(FAMILIES):
        receipts.append(
            SearchRouteReceipt(
                f"{family_id}-native",
                family_id,
                RouteDisposition.COMPLETE,
                (f"source:{family_id}",),
            )
        )
    receipts.extend(
        (
            SearchRouteReceipt(
                "F12-community-custodial",
                "F12",
                RouteDisposition.CENSORED,
                censor_reason="community-specific or custodially governed access unavailable",
            ),
            SearchRouteReceipt(
                "F14-proprietary-model-history",
                "F14",
                RouteDisposition.CENSORED,
                censor_reason="closed training and experiment histories unavailable",
            ),
            SearchRouteReceipt(
                "F15-proprietary-evaluation-data",
                "F15",
                RouteDisposition.CENSORED,
                censor_reason="closed journal/provider evaluation data unavailable",
            ),
            SearchRouteReceipt(
                "F16-confidential-deliberation",
                "F16",
                RouteDisposition.CENSORED,
                censor_reason="confidential legal or regulatory deliberation unavailable",
            ),
            SearchRouteReceipt(
                "F17-proprietary-infrastructure",
                "F17",
                RouteDisposition.CENSORED,
                censor_reason="closed laboratory/platform infrastructure unavailable",
            ),
            SearchRouteReceipt(
                "F22-security-sensitive-incidents",
                "F22",
                RouteDisposition.CENSORED,
                censor_reason="red-team and incident evidence is security-sensitive",
            ),
        )
    )
    return tuple(receipts)


def _clean_pass(pass_id: str) -> SaturationPassReceipt:
    return SaturationPassReceipt(
        pass_id,
        FAMILIES,
        True,
        True,
        True,
        (FindingKind.NONE,),
    )


def test_pass_k_then_l_m_n_earns_internal_synthesis_only() -> None:
    material_k = SaturationPassReceipt(
        "K",
        FAMILIES,
        True,
        True,
        True,
        (FindingKind.COORDINATE, FindingKind.FAILURE, FindingKind.BENCHMARK),
    )
    result = assess_foundation_saturation(
        FAMILIES,
        _complete_family_routes(),
        (material_k, _clean_pass("L"), _clean_pass("M"), _clean_pass("N")),
    )
    assert result.status is FoundationSaturationStatus.READY_FOR_INTERNAL_SYNTHESIS
    assert result.consecutive_no_material_passes == 3
    assert result.internal_synthesis_allowed
    assert not result.external_demarcation_ready
    assert not result.field_authority_granted
    assert result.open_family_ids == ()
    assert result.open_route_ids == ()
    assert len(result.censored_route_ids) == 6


def test_internal_synthesis_receipt_is_bounded_and_non_authorizing() -> None:
    receipt = json.loads(
        Path(
            "research/foundation-saturation/FOUNDATION_INTERNAL_SYNTHESIS_RECEIPT_V1.json"
        ).read_text(encoding="utf-8")
    )
    assert receipt["status"] == "BOUNDED_INTERNAL_FOUNDATION_CANDIDATE_COMPLETE"
    assert receipt["clean_pass_count"] == 3
    assert receipt["bounded_universe"]["broad_family_count"] == 22
    assert receipt["bounded_universe"]["open_internal_routes"] == 0
    assert receipt["authority"]["bounded_conceptual_foundation_complete"] is True
    assert receipt["authority"]["protected_F2_over_F0_gain"] is False
    assert receipt["authority"]["absorptive_supertheory_status"] is False
    assert receipt["authority"]["field_founded"] is False
    assert receipt["authority"]["publication_ready"] is False


def test_route_ledger_has_all_families_routes_and_no_open_route() -> None:
    ledger = json.loads(
        Path(
            "research/foundation-saturation/FOUNDATION_FAMILY_ROUTE_AND_SOURCE_DEPENDENCE_LEDGER_V1.json"
        ).read_text(encoding="utf-8")
    )
    required_routes = set(ledger["required_routes"])
    assert required_routes == {"N", "C", "V", "H", "P", "R", "I", "X"}
    assert ledger["declared_family_count"] == 22
    assert ledger["open_route_count"] == 0
    assert ledger["required_route_coverage_complete"] is True
    assert {item["id"] for item in ledger["families"]} == FAMILIES
    for family in ledger["families"]:
        dispositions = set(family.get("completed_routes", ())) | {
            item["route"] for item in family.get("censored_routes", ())
        }
        assert dispositions == required_routes
        assert family["sources"]
        assert family["dependence"]


def test_candidate_commitments_are_not_promoted_to_laws() -> None:
    ledger = json.loads(
        Path(
            "research/foundation-saturation/BOUNDED_FOUNDATION_PROPOSITION_LEDGER_V1.json"
        ).read_text(encoding="utf-8")
    )
    assert ledger["current_terminal"]["candidate_commitment_count"] == 7
    assert ledger["current_terminal"]["commitments_frozen_as_universal_laws"] == 0
    assert ledger["current_terminal"]["internal_conceptual_synthesis_complete"] is True
    assert ledger["current_terminal"]["absorptive_supertheory_status"] == "UNEARNED_CANDIDATE"
    assert ledger["current_terminal"]["field_founded"] is False
    assert ledger["current_terminal"]["publication_ready"] is False
