"""Known-answer tests for exact parent-owned finite reference methods."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "parent_methods_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "parent_method_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_parent_methods_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    FIXTURES = json.load(handle)


def test_blackwell_garbling_and_decision_value() -> None:
    case = FIXTURES["blackwell"]
    assert module.verify_blackwell_garbling(
        case["exact_experiment"],
        case["noisy_experiment"],
        case["garbling_kernel"],
    ) is case["expected"]["exact_dominates_noisy_with_witness"]
    assert module.verify_blackwell_garbling(
        case["exact_experiment"],
        case["noisy_experiment"],
        case["bad_kernel"],
    ) is (not case["expected"]["bad_witness_rejected"])

    exact_value = module.optimal_finite_decision_value(
        case["exact_experiment"], case["prior"], case["utility"]
    )
    noisy_value = module.optimal_finite_decision_value(
        case["noisy_experiment"], case["prior"], case["utility"]
    )
    assert abs(exact_value - case["expected"]["exact_optimal_value"]) < 1e-12
    assert abs(noisy_value - case["expected"]["noisy_optimal_value"]) < 1e-12
    assert exact_value > noisy_value


def test_rough_set_lower_and_upper_approximations() -> None:
    case = FIXTURES["rough_set"]
    lower_q1, upper_q1 = module.rough_approximations(
        case["attributes"], ["q1"], case["target"]
    )
    assert sorted(lower_q1) == case["expected"]["q1_lower"]
    assert sorted(upper_q1) == case["expected"]["q1_upper"]

    lower_both, upper_both = module.rough_approximations(
        case["attributes"], ["q1", "q2"], case["target"]
    )
    assert sorted(lower_both) == case["expected"]["q1_q2_lower"]
    assert sorted(upper_both) == case["expected"]["q1_q2_upper"]


def test_finite_viability_kernel() -> None:
    case = FIXTURES["viability"]
    kernel = module.finite_viability_kernel(
        case["transitions"], case["constraint_states"]
    )
    assert sorted(kernel) == case["expected_kernel"]


def test_minimal_multiple_fault_diagnoses() -> None:
    case = FIXTURES["diagnosis"]
    for observation, expected in case["expected"].items():
        diagnoses = module.minimal_consistent_diagnoses(
            case["components"], case["predictions"], observation
        )
        actual = sorted(sorted(diagnosis) for diagnosis in diagnoses)
        assert actual == sorted(expected), observation


def test_workflow_option_to_complete() -> None:
    case = FIXTURES["workflow"]
    assert module.workflow_option_to_complete(
        case["sound_graph"], start="start", end="end"
    ) is case["expected"]["sound_option_to_complete"]
    assert module.workflow_option_to_complete(
        case["unsound_graph"], start="start", end="end"
    ) is case["expected"]["unsound_option_to_complete"]
