#!/usr/bin/env python3
"""Materialize gold-blind solver workspaces for frozen ORION tasks.

Run after:

    python scripts/run_orion_real_problem_suite.py prepare --benchmarks bugsinpy --install

The script updates frozen_tasks.json with buggy, solver-visible workspaces. It
never checks out the fixed version and never exposes a gold patch.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


class MaterializationError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MaterializationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise MaterializationError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def venv_binary(venv: Path, name: str) -> Path:
    directory = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" else ""
    return venv / directory / f"{name}{suffix}"


def run(command: list[str], *, cwd: Path | None = None, timeout: int = 2700) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument("--tasks", default="", help="comma-separated task ids; default all")
    parser.add_argument("--timeout-seconds", type=int, default=2700)
    parser.add_argument("--verify-baseline", action="store_true")
    args = parser.parse_args(argv)

    frozen_path = args.workdir / "frozen_tasks.json"
    frozen = read_json(frozen_path)
    selected = {item.strip() for item in args.tasks.split(",") if item.strip()}
    benchmark_records = {
        item["benchmark_id"]: item for item in frozen.get("benchmarks", [])
    }
    record = benchmark_records.get("bugsinpy")
    if not record:
        print("No BugsInPy benchmark is frozen; nothing to materialize.")
        return 0

    repository = Path(record["repository_path"])
    venv = Path(record["venv_path"])
    checkout = venv_binary(venv, "bugsinpy-checkout")
    compile_command = venv_binary(venv, "bugsinpy-compile")
    test_command = venv_binary(venv, "bugsinpy-test")
    if not checkout.exists():
        raise MaterializationError(
            "bugsinpy-checkout is absent; rerun prepare with --install"
        )

    count = 0
    baseline_records: list[dict[str, Any]] = []
    for task in frozen.get("tasks", []):
        if task.get("benchmark_id") != "bugsinpy":
            continue
        task_id = str(task["task_id"])
        if selected and task_id not in selected:
            continue
        workspace = args.workdir / "solver_workspaces" / task_id
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.parent.mkdir(parents=True, exist_ok=True)
        checkout_result = run(
            [
                str(checkout),
                "-p",
                str(task["project"]),
                "-v",
                str(task.get("buggy_version", 0)),
                "-i",
                str(task["bug_id"]),
                "-w",
                str(workspace),
            ],
            cwd=repository,
            timeout=args.timeout_seconds,
        )
        if checkout_result.returncode != 0:
            raise MaterializationError(
                f"checkout failed for {task_id}: {checkout_result.stderr[-4000:]}"
            )
        task["solver_workspace"] = str(workspace.resolve())
        task["workspace_contains_gold"] = False
        task["solver_may_return"] = "unified_diff_only"
        task["network_allowed_during_solution"] = False
        task["workspace_commit"] = run(
            ["git", "rev-parse", "HEAD"], cwd=workspace, timeout=60
        ).stdout.strip()

        baseline: dict[str, Any] = {
            "task_id": task_id,
            "checkout_returncode": checkout_result.returncode,
            "gold_visible": False,
        }
        if args.verify_baseline:
            compile_result = run([str(compile_command)], cwd=workspace, timeout=args.timeout_seconds)
            test_result = None
            if compile_result.returncode == 0:
                test_result = run([str(test_command)], cwd=workspace, timeout=args.timeout_seconds)
            baseline.update(
                {
                    "compile_returncode": compile_result.returncode,
                    "test_returncode": test_result.returncode if test_result else None,
                    "bug_reproduced": bool(test_result and test_result.returncode != 0),
                    "stdout_tail": test_result.stdout[-3000:] if test_result else "",
                    "stderr_tail": (
                        test_result.stderr[-3000:]
                        if test_result
                        else compile_result.stderr[-3000:]
                    ),
                }
            )
        baseline_records.append(baseline)
        count += 1

    write_json(frozen_path, frozen)
    write_json(
        args.workdir / "baseline" / "bugsinpy_materialization.json",
        {
            "schema_version": "orion.v2.bugsinpy-materialization.v1",
            "task_count": count,
            "records": baseline_records,
            "gold_or_fixed_version_access": "NONE",
            "scientific_truth_authorized": False,
        },
    )
    print(f"materialized {count} gold-blind solver workspaces")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (MaterializationError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
