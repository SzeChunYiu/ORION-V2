"""Known-answer tests for cross-generation comparability V0."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "comparability_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "comparability_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_comparability_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    CASES = json.load(handle)["cases"]


def test_comparability_known_answers() -> None:
    for case in CASES:
        assert module.classify_comparability(case["input"]) == case["expected"], case["case_id"]


def test_persistent_identifier_has_no_special_authority() -> None:
    case = next(item for item in CASES if item["case_id"] == "persistent-id-with-construct-drift")
    assert case["input"]["same_identifier"] is True
    assert module.classify_comparability(case["input"]) == "NONCOMPARABLE"


def test_content_can_transport_while_closure_reopens() -> None:
    case = next(
        item
        for item in CASES
        if item["case_id"] == "evidence-content-survives-but-closure-meaning-changes"
    )
    assert module.classify_comparability(case["input"]) == "CONTENT_COMPARABLE_CLOSURE_REOPEN"
