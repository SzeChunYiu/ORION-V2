"""Known-answer checks for the V1 handoff manifest auditor V0."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "v1_handoff_audit_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "v1_handoff_manifest_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_v1_handoff_audit_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    FIXTURES = json.load(handle)


def _mutated_manifest(case: dict[str, object]) -> dict[str, object]:
    manifest = copy.deepcopy(FIXTURES["valid_manifest"])
    if "remove_class" in case:
        manifest["artifacts"] = [
            artifact
            for artifact in manifest["artifacts"]
            if artifact["class"] != case["remove_class"]
        ]
    if "mutate_path" in case:
        artifact = next(
            item for item in manifest["artifacts"] if item["path"] == case["mutate_path"]
        )
        artifact[case["field"]] = case["value"]
    if "manifest_field" in case:
        manifest[case["manifest_field"]] = case["value"]
    return manifest


def test_structurally_complete_manifest() -> None:
    result = module.audit_handoff_manifest(
        FIXTURES["valid_manifest"], FIXTURES["required_classes"]
    )
    assert result.passed is True
    assert result.terminal == "MANIFEST_STRUCTURALLY_COMPLETE"


def test_invalid_manifest_cases_fail_closed() -> None:
    for case in FIXTURES["invalid_cases"]:
        result = module.audit_handoff_manifest(
            _mutated_manifest(case), FIXTURES["required_classes"]
        )
        assert result.passed is False, case["case_id"]
        assert result.terminal == case["expected_terminal"], case["case_id"]


def test_structural_pass_does_not_claim_v1_frozen() -> None:
    result = module.audit_handoff_manifest(
        FIXTURES["valid_manifest"], FIXTURES["required_classes"]
    )
    assert result.terminal != "V1_FREEZE_HANDOFF_BOUND_AND_NON_RETROACTIVE"
    assert any("external verification" in reason for reason in result.reasons)
