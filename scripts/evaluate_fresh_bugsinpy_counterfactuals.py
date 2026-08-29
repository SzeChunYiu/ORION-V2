#!/usr/bin/env python3
"""Evaluate post-freeze BugsInPy counterfactual repair proposals privately."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_orion_agent_responses.py"
SPEC = importlib.util.spec_from_file_location("orion_response_validator", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import validator: {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class CounterfactualEvaluationError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CounterfactualEvaluationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CounterfactualEvaluationError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def run(command: list[str], *, cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def run_native_relevant_test(workspace: Path, *, timeout: int) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    env_bin = workspace / ("env/Scripts" if os.name == "nt" else "env/bin")
    environment["PATH"] = str(env_bin) + os.pathsep + environment.get("PATH", "")
    environment["VIRTUAL_ENV"] = str(workspace / "env")
    return subprocess.run(
        ["bash", "bugsinpy_run_test.sh"], cwd=str(workspace), env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=timeout, check=False,
    )


def extract_patch(response: dict[str, Any]) -> str | None:
    artifact = response.get("proposed_patch_or_artifact")
    if isinstance(artifact, str):
        return artifact
    if isinstance(artifact, dict):
        if artifact.get("type") == "unified_diff" and isinstance(artifact.get("content"), str):
            return artifact["content"]
        if artifact.get("type") == "path" and isinstance(artifact.get("path"), str):
            path = Path(artifact["path"])
            if path.exists():
                return path.read_text(encoding="utf-8")
    return None


def cannot_check(task_id: str, arm_id: str, reason: Any) -> dict[str, Any]:
    return {
        "schema_version": "orion.v2.task-evaluation.v1",
        "task_id": task_id,
        "arm_id": arm_id,
        "benchmark_id": "fresh_bugsinpy_counterfactual",
        "status": "CANNOT_CHECK",
        "reason": reason,
        "full_regression_suite_passed": None,
        "critical_new_failure_count": None,
        "scientific_truth_authorized": False,
        "field_status_authorized": False,
        "publication_readiness_authorized": False,
    }


def evaluate(
    workdir: Path,
    manifest_path: Path,
    *,
    arms: set[str] | None,
    tasks: set[str] | None,
    timeout_seconds: int,
) -> int:
    manifest = read_json(manifest_path)
    required_fields = tuple(manifest["agent_protocol"]["required_response_fields"])
    public = read_json(workdir / "frozen_tasks.json")
    private = read_json(workdir / "private_evaluation_registry.json")
    public_tasks = {item["task_id"]: item for item in public.get("tasks", [])}
    private_tasks = {item["task_id"]: item for item in private.get("records", [])}
    count = 0

    for response_path in sorted((workdir / "responses").glob("*/*.json")):
        arm_id = response_path.parent.name
        task_id = response_path.stem
        if arms and arm_id not in arms:
            continue
        if tasks and task_id not in tasks:
            continue
        public_task = public_tasks.get(task_id)
        private_task = private_tasks.get(task_id)
        if public_task is None or private_task is None:
            raise CounterfactualEvaluationError(f"task registry mismatch: {task_id}")
        response = read_json(response_path)
        errors = validator.validate_response(
            response,
            expected_task_id=task_id,
            expected_arm_id=arm_id,
            required_fields=required_fields,
        )
        status = str(response.get("status", ""))
        patch = extract_patch(response)
        if errors:
            result = cannot_check(task_id, arm_id, errors)
            result["status"] = "CANNOT_CHECK_INVALID_RESPONSE"
        elif status.startswith(("CANNOT_CHECK", "EXECUTION_FAILED")) or patch is None:
            result = cannot_check(task_id, arm_id, response.get("diagnosis", status))
        else:
            template = Path(private_task["private_mutated_template"])
            workspace = workdir / "evaluation_runs" / arm_id / task_id
            if workspace.exists():
                shutil.rmtree(workspace)
            shutil.copytree(template, workspace)
            patch_result = subprocess.run(
                ["git", "apply", "--whitespace=nowarn", "-"],
                cwd=str(workspace),
                input=patch,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            compile_result = None
            test_result = None
            start = time.perf_counter()
            if patch_result.returncode == 0:
                compile_environment = os.environ.copy()
                public_python_bin = str(public_task.get("project_python_bin") or "").strip()
                if public_python_bin:
                    compile_environment["PATH"] = public_python_bin + os.pathsep + compile_environment.get("PATH", "")
                compile_result = subprocess.run(
                    [str(private_task["compile_command"])], cwd=str(workspace),
                    env=compile_environment, text=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, timeout=timeout_seconds, check=False,
                )
                if compile_result.returncode == 0:
                    test_result = run_native_relevant_test(workspace, timeout=timeout_seconds)
            elapsed = time.perf_counter() - start
            passed = bool(test_result and test_result.returncode == 0)
            result = {
                "schema_version": "orion.v2.task-evaluation.v1",
                "task_id": task_id,
                "arm_id": arm_id,
                "benchmark_id": "fresh_bugsinpy_counterfactual",
                "status": "NATIVE_EVALUATION_COMPLETE",
                "patch_apply_returncode": patch_result.returncode,
                "compile_returncode": compile_result.returncode if compile_result else None,
                "test_returncode": test_result.returncode if test_result else None,
                "full_regression_suite_passed": None,
                "native_success": passed,
                "full_regression_suite_status": "CANNOT_CHECK_NOT_RUN",
                "native_success": passed,
                "critical_new_failure_count": 0 if passed else 1,
                "critical_false_completion": bool(not passed and "SUCCESS" in status.upper()),
                "wall_time_seconds": elapsed,
                "patch_size_bytes": len(patch.encode("utf-8")),
                "source_case_id": public_task["source_case_id"],
                "mutation_generated_after_protocol_freeze": True,
                "gold_patch_exposed_to_solver": False,
                "gold_similarity": "WITHHELD_UNTIL_PRIMARY_SCORING_COMPLETE",
                "scientific_truth_authorized": False,
                "field_status_authorized": False,
                "publication_readiness_authorized": False,
                "stdout_tail": test_result.stdout[-3000:] if test_result else "",
                "stderr_tail": (
                    test_result.stderr[-3000:]
                    if test_result
                    else compile_result.stderr[-3000:]
                    if compile_result
                    else patch_result.stderr[-3000:]
                ),
            }
        write_json(workdir / "evaluations" / arm_id / f"{task_id}.json", result)
        count += 1
    return count


def parse_ids(value: str) -> set[str] | None:
    result = {item.strip() for item in value.split(",") if item.strip()}
    return result or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-fresh-counterfactual-suite"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("research/experiments/ORION_FRESH_COUNTERFACTUAL_REPAIR_SUITE_V1.json"),
    )
    parser.add_argument("--arms", default="")
    parser.add_argument("--tasks", default="")
    parser.add_argument("--timeout-seconds", type=int, default=2700)
    args = parser.parse_args(argv)
    try:
        count = evaluate(
            args.workdir,
            args.manifest,
            arms=parse_ids(args.arms),
            tasks=parse_ids(args.tasks),
            timeout_seconds=args.timeout_seconds,
        )
    except (CounterfactualEvaluationError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"evaluated {count} counterfactual responses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
