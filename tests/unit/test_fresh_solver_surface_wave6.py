from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "sanitize_fresh_counterfactual_solver_surface.py"
SPEC = importlib.util.spec_from_file_location("orion_fresh_surface", SCRIPT)
assert SPEC and SPEC.loader
surface = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(surface)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_sanitizer_removes_test_and_framework_access(tmp_path: Path) -> None:
    write_json(
        tmp_path / "frozen_tasks.json",
        {
            "tasks": [
                {
                    "task_id": "fresh-001",
                    "solver_test_command": "/private/bugsinpy-test",
                    "solver_compile_command": "/private/bugsinpy-compile",
                    "solver_support_mounts": ["/private/framework"],
                }
            ]
        },
    )
    write_json(
        tmp_path / "private_evaluation_registry.json",
        {
            "records": [
                {
                    "task_id": "fresh-001",
                    "mutation": {
                        "failing_stdout_tail": "FAILED test_value",
                        "failing_stderr_tail": "assertion failed",
                    },
                }
            ]
        },
    )
    receipt = surface.sanitize(tmp_path)
    public = json.loads((tmp_path / "frozen_tasks.json").read_text())
    task = public["tasks"][0]
    assert task["observed_failure_stdout_tail"] == "FAILED test_value"
    assert task["native_test_execution"] == "PRIVATE_EVALUATOR_ONLY"
    assert task["solver_support_mounts"] == []
    assert "solver_test_command" not in task
    assert "solver_compile_command" not in task
    assert receipt["gold_or_fixed_history_exposed"] is False
