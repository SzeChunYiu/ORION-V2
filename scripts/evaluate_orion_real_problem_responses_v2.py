#!/usr/bin/env python3
"""Fail-closed evaluator wrapper for ORION real-problem agent responses.

This wrapper preserves missing-agent, missing-data and execution failures as
CANNOT_CHECK instead of converting them into scientific losses or successes.
Eligible BugsInPy proposals are delegated to the native fresh-workspace
evaluator in run_orion_real_problem_suite.py.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_orion_real_problem_suite.py"
SPEC = importlib.util.spec_from_file_location("orion_real_problem_runner", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import runner: {RUNNER_PATH}")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class EvaluationError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvaluationError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def response_is_uncheckable(response: dict[str, Any]) -> bool:
    status = str(response.get("status", "")).upper()
    if status.startswith("CANNOT_CHECK") or status.startswith("EXECUTION_FAILED"):
        return True
    if response.get("proposed_patch_or_artifact") is None:
        return True
    return False


def uncheckable_evaluation(
    task: dict[str, Any], response: dict[str, Any], arm_id: str
) -> dict[str, Any]:
    return {
        "schema_version": "orion.v2.task-evaluation.v1",
        "task_id": task["task_id"],
        "arm_id": arm_id,
        "benchmark_id": task["benchmark_id"],
        "status": "CANNOT_CHECK_AGENT_OR_ARTIFACT_UNAVAILABLE",
        "agent_status": response.get("status", "UNKNOWN"),
        "reason": response.get("diagnosis", "No executable proposal was supplied."),
        "full_regression_suite_passed": None,
        "critical_new_failure_count": None,
        "scientific_truth_authorized": False,
        "field_status_authorized": False,
        "publication_readiness_authorized": False,
    }


def evaluate(
    workdir: Path,
    *,
    arms: set[str] | None,
    tasks: set[str] | None,
    timeout_seconds: int,
) -> int:
    frozen = read_json(workdir / "frozen_tasks.json")
    task_map = {item["task_id"]: item for item in frozen.get("tasks", [])}
    count = 0
    for response_path in sorted((workdir / "responses").glob("*/*.json")):
        arm_id = response_path.parent.name
        task_id = response_path.stem
        if arms and arm_id not in arms:
            continue
        if tasks and task_id not in tasks:
            continue
        task = task_map.get(task_id)
        if task is None:
            raise EvaluationError(f"response refers to unknown task: {task_id}")
        response = read_json(response_path)
        if response_is_uncheckable(response):
            result = uncheckable_evaluation(task, response, arm_id)
        elif task.get("adapter") == "bugsinpy":
            try:
                result = runner._evaluate_bugsinpy(
                    frozen,
                    workdir,
                    task,
                    response,
                    arm_id,
                    timeout_seconds=timeout_seconds,
                )
            except (runner.RunnerError, OSError, subprocess.SubprocessError) as exc:
                result = {
                    "schema_version": "orion.v2.task-evaluation.v1",
                    "task_id": task_id,
                    "arm_id": arm_id,
                    "benchmark_id": task["benchmark_id"],
                    "status": "CANNOT_CHECK_EVALUATOR_FAILURE",
                    "reason": str(exc),
                    "full_regression_suite_passed": None,
                    "critical_new_failure_count": None,
                    "scientific_truth_authorized": False,
                    "field_status_authorized": False,
                    "publication_readiness_authorized": False,
                }
        else:
            bound = workdir / "native_evaluations" / arm_id / f"{task_id}.json"
            if bound.exists():
                result = read_json(bound)
                result.setdefault("task_id", task_id)
                result.setdefault("arm_id", arm_id)
                result.setdefault("benchmark_id", task["benchmark_id"])
                result["scientific_truth_authorized"] = False
                result["field_status_authorized"] = False
                result["publication_readiness_authorized"] = False
            else:
                result = {
                    "schema_version": "orion.v2.task-evaluation.v1",
                    "task_id": task_id,
                    "arm_id": arm_id,
                    "benchmark_id": task["benchmark_id"],
                    "status": "CANNOT_CHECK_NATIVE_EVALUATION_NOT_BOUND",
                    "reason": "Register a content-bound native benchmark evaluation artifact.",
                    "full_regression_suite_passed": None,
                    "critical_new_failure_count": None,
                    "scientific_truth_authorized": False,
                    "field_status_authorized": False,
                    "publication_readiness_authorized": False,
                }
        write_json(workdir / "evaluations" / arm_id / f"{task_id}.json", result)
        count += 1
    return count


def parse_ids(value: str) -> set[str] | None:
    result = {item.strip() for item in value.split(",") if item.strip()}
    return result or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument("--arms", default="")
    parser.add_argument("--tasks", default="")
    parser.add_argument("--timeout-seconds", type=int, default=2700)
    args = parser.parse_args(argv)
    try:
        count = evaluate(
            args.workdir,
            arms=parse_ids(args.arms),
            tasks=parse_ids(args.tasks),
            timeout_seconds=args.timeout_seconds,
        )
    except (EvaluationError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"evaluated {count} responses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
