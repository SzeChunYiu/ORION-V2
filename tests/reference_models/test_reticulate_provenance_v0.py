"""Known-answer checks for reticulate provenance and alternative support V0."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "reticulate_provenance_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "reticulate_provenance_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_reticulate_provenance_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    FIXTURES = json.load(handle)


def test_single_declared_parent_is_incomplete_for_component_inheritance() -> None:
    artifact = FIXTURES["artifact"]
    assert module.declared_single_parent_is_complete(
        artifact["components"], artifact["declared_single_parent"]
    ) is artifact["expected_single_parent_complete"]
    assert sorted(module.artifact_parent_ids(artifact["components"])) == artifact["expected_parent_ids"]


def test_revocation_propagates_through_alternative_support_families() -> None:
    for case in FIXTURES["revocation_cases"]:
        actual = module.classify_claims_after_revocation(
            FIXTURES["claims"], case["revoked_parent_ids"]
        )
        assert actual == case["expected"], case["case_id"]


def test_shared_semantic_parent_can_invalidate_multiple_alternative_paths() -> None:
    case = next(item for item in FIXTURES["revocation_cases"] if item["case_id"] == "revoke-shared-semantic-parent")
    actual = module.classify_claims_after_revocation(
        FIXTURES["claims"], case["revoked_parent_ids"]
    )
    assert actual["claim:primary"] == "INVALIDATED"
