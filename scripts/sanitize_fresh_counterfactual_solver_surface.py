#!/usr/bin/env python3
"""Restrict fresh counterfactual tasks to public code and failing output only.

The script copies the generated failing-test tails into the public task contract
while removing native test commands and framework support mounts. Native tests,
fixed histories and reverse patches remain private to the evaluator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class SanitizationError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SanitizationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SanitizationError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def sanitize(workdir: Path) -> dict[str, Any]:
    public_path = workdir / "frozen_tasks.json"
    public = read_json(public_path)
    private = read_json(workdir / "private_evaluation_registry.json")
    private_by_task = {item["task_id"]: item for item in private.get("records", [])}
    sanitized = 0
    for task in public.get("tasks", []):
        task_id = task.get("task_id")
        record = private_by_task.get(task_id)
        if record is None:
            raise SanitizationError(f"private record missing for {task_id}")
        mutation = record.get("mutation")
        if not isinstance(mutation, dict):
            raise SanitizationError(f"mutation receipt missing for {task_id}")
        task["observed_failure_stdout_tail"] = mutation.get("failing_stdout_tail", "")
        task["observed_failure_stderr_tail"] = mutation.get("failing_stderr_tail", "")
        task["solver_may_run_private_native_tests"] = False
        task["native_test_execution"] = "PRIVATE_EVALUATOR_ONLY"
        task["solver_support_mounts"] = []
        task["historical_framework_metadata_exposed"] = False
        task.pop("solver_compile_command", None)
        task.pop("solver_test_command", None)
        sanitized += 1
    write_json(public_path, public)
    receipt = {
        "schema_version": "orion.v2.fresh-solver-surface.v1",
        "task_count": sanitized,
        "public_fields_added": [
            "observed_failure_stdout_tail",
            "observed_failure_stderr_tail",
            "native_test_execution",
        ],
        "removed_from_solver_surface": [
            "private native test commands",
            "benchmark framework support mounts",
            "fixed source history",
            "reverse patch",
            "private mutation token receipt",
        ],
        "gold_or_fixed_history_exposed": False,
        "native_test_execution_private": True,
        "scientific_truth_authorized": False,
    }
    write_json(workdir / "aggregate" / "fresh_solver_surface.json", receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-fresh-counterfactual-suite"))
    args = parser.parse_args(argv)
    try:
        result = sanitize(args.workdir)
    except (SanitizationError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
