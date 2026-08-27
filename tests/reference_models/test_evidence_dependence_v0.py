"""Known-answer tests for conservative evidence dependence V0."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "evidence_dependence_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "evidence_dependence_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_evidence_dependence_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    FIXTURES = json.load(handle)


def test_declared_dependence_components() -> None:
    for case in FIXTURES["cases"]:
        actual = module.declared_independent_component_count(case["evidence"])
        assert actual == case["expected_components"], case["case_id"]


def test_equicorrelated_effective_sample_size() -> None:
    for case in FIXTURES["equicorrelation_cases"]:
        actual = module.equicorrelated_effective_n(case["n"], case["rho"])
        assert abs(actual - case["expected_effective_n"]) < 1e-12, case["case_id"]


def test_transitive_bridge_merges_components() -> None:
    case = next(item for item in FIXTURES["cases"] if item["case_id"] == "bridge-dependence-merges-two-apparent-clusters")
    components = module.declared_dependence_components(case["evidence"])
    assert components == (frozenset({"a", "bridge", "c"}),)
