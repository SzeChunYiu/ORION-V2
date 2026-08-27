"""Known-answer tests for the fail-closed V0 solver-policy reference model."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "solver_policy_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "solver_lifecycle_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_solver_policy_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    CASES = json.load(handle)["cases"]


def test_solver_lifecycle_known_answers() -> None:
    for case in CASES:
        decision = module.decide(case["state"])
        expected = case["expected"]
        assert decision.action == expected["action"], case["case_id"]
        if "terminal" in expected:
            assert decision.terminal == expected["terminal"], case["case_id"]
        if "responsibility" in expected:
            assert decision.responsibility == expected["responsibility"], case["case_id"]
        if "jump_level" in expected:
            assert decision.jump_level == expected["jump_level"], case["case_id"]
