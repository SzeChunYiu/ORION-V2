"""Known-answer checks for frontier-opportunity screening V0."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "frontier_opportunity_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "frontier_opportunity_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_frontier_opportunity_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    FIXTURES = json.load(handle)


def test_opportunity_classification_separates_novelty_from_scientific_value() -> None:
    for case in FIXTURES["cases"]:
        actual = module.classify_opportunity(case, FIXTURES["budget"])
        assert actual == case["expected_status"], case["id"]


def test_pareto_frontier_preserves_incomparable_opportunities() -> None:
    actual = module.pareto_frontier(FIXTURES["pareto_candidates"])
    assert list(actual) == sorted(FIXTURES["expected_pareto_ids"])


def test_novelty_alone_cannot_create_an_opportunity() -> None:
    case = next(item for item in FIXTURES["cases"] if item["id"] == "surprising-without-decisive-probe")
    assert case["novelty"] > 0.9
    assert module.classify_opportunity(case, FIXTURES["budget"]) == "INTERESTINGNESS_WITHOUT_SCIENTIFIC_TEST"


def test_agenda_proposal_is_not_agenda_adoption() -> None:
    case = next(item for item in FIXTURES["cases"] if item["id"] == "agenda-authority-pending")
    assert module.classify_opportunity(case, FIXTURES["budget"]) == "AGENDA_AUTHORITY_REQUIRED"
