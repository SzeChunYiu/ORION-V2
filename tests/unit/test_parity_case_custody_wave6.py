from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "research/evaluation"


def _load(name: str) -> dict:
    return json.loads((EVAL / name).read_text(encoding="utf-8"))


def _git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def test_case_registry_covers_exact_protocol_capability_set() -> None:
    protocol = _load("V1_PARITY_CAMPAIGN_PROTOCOL_WAVE06_V1.json")
    registry = _load("V1_PARITY_CASE_REGISTRY_WAVE06_V1.json")

    protocol_ids = {
        capability
        for campaign in protocol["campaigns"]
        for capability in campaign["capability_ids"]
    }
    registry_ids = {
        capability
        for campaign in registry["campaigns"]
        for case in campaign["cases"]
        for capability in case["capability_ids"]
    }
    assert len(protocol_ids) == 59
    assert registry_ids == protocol_ids
    assert registry["paired_outcomes_accessed"] is False


def test_case_selection_receipt_binds_current_registry_blob() -> None:
    registry_path = EVAL / "V1_PARITY_CASE_REGISTRY_WAVE06_V1.json"
    receipt = _load("V1_PARITY_CASE_SELECTION_RECEIPT_WAVE06_V1.json")
    actual = _git_blob_sha(registry_path)
    assert actual == "79f5e9d47d65994bae77695f37718c0c86079257"
    assert receipt["protected_case_manifest_digest"] == f"git-sha1:{actual}"
    assert receipt["paired_outcomes_accessed_before_binding"] is False


def test_semantic_gap_cases_are_explicit_and_cannot_substitute_for_v1_native_parity() -> None:
    registry = _load("V1_PARITY_CASE_REGISTRY_WAVE06_V1.json")
    campaigns = {row["campaign_id"]: row for row in registry["campaigns"]}
    for campaign_id in ("PARITY-C", "PARITY-D"):
        row = campaigns[campaign_id]
        assert row["source_status"].startswith("PARTIAL_V1_NATIVE")
        assert "cannot alone establish V1-native" in row["non_substitution_rule"]


def test_scoring_partitions_every_case_into_deterministic_or_semantic() -> None:
    registry = _load("V1_PARITY_CASE_REGISTRY_WAVE06_V1.json")
    scoring = _load("V1_PARITY_SCORING_ADJUDICATION_WAVE06_V1.json")
    case_ids = {
        case["case_id"]
        for campaign in registry["campaigns"]
        for case in campaign["cases"]
    }
    deterministic = set(scoring["deterministic_case_ids"])
    semantic = set(scoring["semantic_case_ids"])
    assert deterministic.isdisjoint(semantic)
    assert deterministic | semantic == case_ids
    assert scoring["capability_cell_rule"]["no_family_average"] is True
    assert scoring["semantic_adjudication"]["reviewer_minimum"] == 2


def test_evaluator_registry_binds_mechanical_scorer_but_not_semantic_authority() -> None:
    evaluators = _load("V1_PARITY_EVALUATOR_REGISTRY_WAVE06_V1.json")
    assert evaluators["paired_outcomes_accessed"] is False
    assert evaluators["registry_bound"] is False
    by_id = {row["evaluator_id"]: row for row in evaluators["evaluators"]}
    assert by_id["PARITY-DET-FROZEN-INVARIANT-SCORER-V1"]["bound"] is True
    for evaluator_id in (
        "PARITY-C-SEMANTIC-REVIEWER-1",
        "PARITY-C-SEMANTIC-REVIEWER-2",
        "PARITY-D-RECONSTRUCTION-REVIEWER-1",
        "PARITY-D-RECONSTRUCTION-REVIEWER-2",
    ):
        assert by_id[evaluator_id]["bound"] is False


def test_budget_manifest_covers_each_case_once_and_forbids_live_network() -> None:
    registry = _load("V1_PARITY_CASE_REGISTRY_WAVE06_V1.json")
    budgets = _load("V1_PARITY_CASE_BUDGETS_WAVE06_V1.json")
    case_ids = {
        case["case_id"]
        for campaign in registry["campaigns"]
        for case in campaign["cases"]
    }
    assert set(budgets["case_to_profile"]) == case_ids
    required = {
        "wall_clock_ceiling_seconds",
        "provider_call_ceiling_by_capability",
        "retrieval_query_ceiling",
        "retrieved_item_or_byte_ceiling",
        "local_process_timeout_ceiling_seconds",
        "local_process_output_ceiling_bytes",
        "max_solver_or_control_iterations",
        "retry_ceiling_by_failure_class",
        "context_or_input_byte_ceiling",
        "random_seed_or_determinism_binding",
        "network_access_policy",
        "side_effect_permission_policy",
    }
    for profile in budgets["profiles"].values():
        assert required <= set(profile)
        assert "DENY_LIVE_NETWORK" in profile["network_access_policy"]


def test_custody_protocol_advances_case_and_scoring_only() -> None:
    custody = _load("V1_PARITY_CUSTODY_PROTOCOL_WAVE06_V1.json")
    resources = _load("V1_PARITY_RESOURCE_MATCHING_PROTOCOL_WAVE06_V1.json")
    assert custody["protected_case_registry"]["bound"] is True
    assert custody["scoring_registry"]["bound"] is True
    assert custody["evaluator_registry"]["bound"] is False
    assert resources["case_budget_manifest"]["bound"] is True
    assert custody["authority"]["grants_v1_parity"] is False
    assert resources["authority"]["grants_v2_closeout"] is False
