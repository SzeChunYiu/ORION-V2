"""Known-answer tests for the fail-closed donor reduction assessor V0."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "donor_reduction_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "donor_reduction_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_donor_reduction_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    FIXTURES = json.load(handle)


def _case(fixture: dict[str, object]) -> dict[str, object]:
    result = copy.deepcopy(FIXTURES["defaults"])
    result["case_id"] = fixture["case_id"]
    result.update(fixture["overrides"])
    return result


def test_donor_reduction_known_answers() -> None:
    for fixture in FIXTURES["cases"]:
        result = module.assess_donor_reduction(_case(fixture))
        assert result.verdict == fixture["expected"], fixture["case_id"]
        assert result.grants_scientific_truth is False
        assert result.grants_novelty is False
        assert result.grants_v2_admission is False


def test_ideal_donor_product_tie_contracts_superiority() -> None:
    fixture = next(item for item in FIXTURES["cases"] if item["case_id"] == "ideal-product-ties")
    result = module.assess_donor_reduction(_case(fixture))
    assert result.verdict == "IDEAL_DONOR_PRODUCT_EQUIVALENCE"
    assert any("ties" in reason for reason in result.reasons)


def test_candidate_strict_envelope_still_does_not_self_authorize() -> None:
    fixture = next(item for item in FIXTURES["cases"] if item["case_id"] == "candidate-strict-envelope")
    result = module.assess_donor_reduction(_case(fixture))
    assert result.verdict == "CANDIDATE_STRICT_ENVELOPE"
    assert result.grants_scientific_truth is False
    assert result.grants_novelty is False
    assert result.grants_v2_admission is False
