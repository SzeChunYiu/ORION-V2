"""Known-answer checks for performative evaluation V0."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "performative_evaluation_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "performative_evaluation_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_performative_evaluation_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    CASES = json.load(handle)["cases"]


def test_static_and_performative_policy_selection() -> None:
    for case in CASES:
        assert module.best_policy_static(
            case["baseline_distribution"], case["policies"]
        ) == case["expected"]["static_winner"], case["case_id"]
        assert module.best_policy_performative(case["policies"]) == case["expected"][
            "performative_winner"
        ], case["case_id"]


def test_transportability_depends_on_response_magnitude() -> None:
    reversal = next(item for item in CASES if item["case_id"] == "static-winner-reverses-after-response")
    assert module.static_evaluation_transportable(
        reversal["baseline_distribution"],
        reversal["policies"]["A"]["induced_distribution"],
        tolerance=0.1,
    ) is reversal["expected"]["transportable_A_at_0_1"]
    assert module.static_evaluation_transportable(
        reversal["baseline_distribution"],
        reversal["policies"]["B"]["induced_distribution"],
        tolerance=0.1,
    ) is reversal["expected"]["transportable_B_at_0_1"]

    stable = next(item for item in CASES if item["case_id"] == "stable-negative-control")
    for policy_id in ("A", "B"):
        assert module.static_evaluation_transportable(
            stable["baseline_distribution"],
            stable["policies"][policy_id]["induced_distribution"],
            tolerance=0.01,
        ) is True


def test_static_winner_can_be_performatively_worse() -> None:
    case = next(item for item in CASES if item["case_id"] == "static-winner-reverses-after-response")
    assert module.best_policy_static(case["baseline_distribution"], case["policies"]) == "A"
    assert module.best_policy_performative(case["policies"]) == "B"
