from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "research/evaluation"


def _load(name: str) -> dict:
    return json.loads((EVAL / name).read_text(encoding="utf-8"))


def test_parent_candidate_version_audit_has_all_nine_campaigns_and_no_open_version_pin() -> None:
    audit = _load("PARENT_BASELINE_VERSION_AUDIT_WAVE06_V1.json")
    rows = audit["campaign_candidates"]
    assert {row["campaign_id"] for row in rows} == {f"PARITY-{letter}" for letter in "ABCDEFGHI"}
    assert audit["current_result"]["version_identity_progress"] == "COMPLETE_FOR_CURRENT_CANDIDATE_SET"
    assert audit["current_result"]["remaining_version_pins"] == []
    for row in rows:
        assert row["candidates"]
        for candidate in row["candidates"]:
            assert candidate["implementation"]
            assert candidate["version"]
            assert "TO_PIN" not in candidate["version"]
    assert audit["current_result"]["strongest_parent_binding"] is False


def test_fit_audit_has_one_non_authorizing_campaign_disposition_per_parity_campaign() -> None:
    audit = _load("PARENT_BASELINE_FIT_AUDIT_WAVE06_V1.json")
    rows = audit["campaigns"]
    assert {row["campaign_id"] for row in rows} == {f"PARITY-{letter}" for letter in "ABCDEFGHI"}
    for row in rows:
        assert row["candidate_composition"]
        assert row["native_strengths"]
        assert row["required_adapter_semantics"]
        assert row["known_gap"]
        assert "NOT_YET_BOUND" in row["fit_disposition"] or "REVIEW_REQUIRED" in row["fit_disposition"]
    assert audit["authority"]["grants_strongest_parent_binding"] is False


def test_adapter_contract_is_thin_and_forbids_orion_scientific_laundering() -> None:
    contract = _load("PARENT_BASELINE_ADAPTER_CONTRACT_WAVE06_V1.json")
    assert {row["campaign_id"] for row in contract["campaign_contracts"]} == {
        f"PARITY-{letter}" for letter in "ABCDEFGHI"
    }
    prohibited = "\n".join(contract["global_prohibited_operations"]).lower()
    assert "orion-v2 scientific modules" in prohibited
    assert "change the problem" in prohibited
    assert "promote missing/failed/censored output" in prohibited
    assert contract["authority"]["grants_parent_binding"] is False
    assert contract["authority"]["grants_parent_supremacy"] is False


def test_baseline_registry_remains_unbound_until_configuration_adapter_fit_receipts_exist() -> None:
    registry = _load("V1_PARITY_BASELINE_REGISTRY_WAVE06_V1.json")
    assert registry["implementation_bindings"]["bound"] is False
    assert registry["run_gate"]["allowed_now"] is False
    required = set(registry["implementation_bindings"]["required_per_campaign"])
    assert {
        "implementation_or_product_id",
        "version_or_commit",
        "source_or_package_identity",
        "configuration_digest",
        "why_this_is_the_strongest_practical_comparator_under_the_frozen_role",
        "known_limitations",
        "matched_resource_adapter_digest",
    } <= required
