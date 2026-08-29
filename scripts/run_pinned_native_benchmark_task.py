#!/usr/bin/env python3
"""Execute a frozen native benchmark task and record a non-authorizing receipt.

The script substitutes only registered placeholders, runs under the pinned
benchmark virtual environment, and records commands and output. It does not
infer scientific success; metrics must be populated and bound separately with
bind_native_benchmark_evaluation.py.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


class NativeRunError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NativeRunError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise NativeRunError(f"expected JSON object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def benchmark_record(frozen: dict[str, Any], benchmark_id: str) -> dict[str, Any]:
    for item in frozen.get("benchmarks", []):
        if item.get("benchmark_id") == benchmark_id:
            return item
    raise NativeRunError(f"missing benchmark record: {benchmark_id}")


def substitute(command: str, values: dict[str, str]) -> str:
    result = command
    for key, value in values.items():
        result = result.replace("{" + key + "}", shlex.quote(value))
    unresolved = [token for token in ("{repo}", "{data_dir}", "{output_dir}", "{run_name}") if token in result]
    if unresolved:
        raise NativeRunError("unresolved command placeholders: " + ", ".join(unresolved))
    return result


def run_task(
    workdir: Path,
    *,
    task_id: str,
    arm_id: str,
    data_dir: Path,
    output_dir: Path,
    run_name: str,
    timeout_seconds: int,
    skip_install_commands: bool,
) -> dict[str, Any]:
    frozen = read_json(workdir / "frozen_tasks.json")
    task = next((item for item in frozen.get("tasks", []) if item.get("task_id") == task_id), None)
    if task is None:
        raise NativeRunError(f"unknown task: {task_id}")
    benchmark = benchmark_record(frozen, str(task["benchmark_id"]))
    repository = Path(benchmark["repository_path"]).resolve()
    venv = Path(benchmark["venv_path"]).resolve()
    if not repository.is_dir():
        raise NativeRunError(f"repository missing: {repository}")
    if not venv.is_dir():
        raise NativeRunError(f"virtual environment missing: {venv}")
    if not data_dir.exists():
        raise NativeRunError(f"data directory missing: {data_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    path_directory = venv / ("Scripts" if os.name == "nt" else "bin")
    environment = os.environ.copy()
    environment["PATH"] = str(path_directory) + os.pathsep + environment.get("PATH", "")
    environment["VIRTUAL_ENV"] = str(venv)
    environment["ORION_TASK_ID"] = task_id
    environment["ORION_ARM_ID"] = arm_id
    environment["ORION_OUTCOME_ACCESS"] = "NATIVE_COMMAND_ONLY"

    values = {
        "repo": str(repository),
        "data_dir": str(data_dir.resolve()),
        "output_dir": str(output_dir.resolve()),
        "run_name": run_name,
    }
    command_receipts: list[dict[str, Any]] = []
    overall_returncode = 0
    start_total = time.perf_counter()
    for raw in task.get("native_commands", []):
        if skip_install_commands and "pip install" in raw:
            command_receipts.append(
                {
                    "raw_command": raw,
                    "status": "SKIPPED_ALREADY_PREPARED",
                    "returncode": None,
                }
            )
            continue
        command = substitute(str(raw), values)
        start = time.perf_counter()
        result = subprocess.run(
            ["bash", "-lc", command],
            cwd=str(repository),
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
        elapsed = time.perf_counter() - start
        command_receipts.append(
            {
                "raw_command": raw,
                "resolved_command": command,
                "command_sha256": sha256_text(command),
                "returncode": result.returncode,
                "wall_time_seconds": elapsed,
                "stdout": result.stdout[-10000:],
                "stderr": result.stderr[-10000:],
            }
        )
        if result.returncode != 0:
            overall_returncode = result.returncode
            break
    total_elapsed = time.perf_counter() - start_total
    receipt = {
        "schema_version": "orion.v2.native-command-execution.v1",
        "task_id": task_id,
        "arm_id": arm_id,
        "benchmark_id": task["benchmark_id"],
        "task_variant": task.get("variant"),
        "repository": str(repository),
        "repository_commit": benchmark.get("commit"),
        "virtual_environment": str(venv),
        "data_directory": str(data_dir.resolve()),
        "output_directory": str(output_dir.resolve()),
        "run_name": run_name,
        "commands": command_receipts,
        "overall_returncode": overall_returncode,
        "wall_time_seconds": total_elapsed,
        "native_metrics_interpreted": False,
        "next_required": "populate native-result input and bind result artifacts",
        "scientific_truth_authorized": False,
        "field_status_authorized": False,
        "publication_readiness_authorized": False,
    }
    write_json(workdir / "native_execution" / arm_id / task_id / "execution.json", receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--arm-id", required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=86400)
    parser.add_argument("--run-install-commands", action="store_true")
    args = parser.parse_args(argv)
    try:
        receipt = run_task(
            args.workdir,
            task_id=args.task_id,
            arm_id=args.arm_id,
            data_dir=args.data_dir,
            output_dir=args.output_dir,
            run_name=args.run_name,
            timeout_seconds=args.timeout_seconds,
            skip_install_commands=not args.run_install_commands,
        )
    except (NativeRunError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["overall_returncode"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
