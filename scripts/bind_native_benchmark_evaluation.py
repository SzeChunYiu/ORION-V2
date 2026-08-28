#!/usr/bin/env python3
"""Bind an external native benchmark result into the ORION experiment ledger.

Use for CausalBench, Matbench Discovery or another native evaluator that runs
outside the provider-neutral dispatcher. The result remains non-authorizing and
must include exact data, command, evaluator and resource identities.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


class BindingError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BindingError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BindingError(f"expected JSON object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def non_blank_strings(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise BindingError(f"{label} must be a non-empty list")
    items = tuple(str(item).strip() for item in value)
    if any(not item for item in items):
        raise BindingError(f"{label} may not contain blanks")
    return items


def bind(
    workdir: Path,
    result_path: Path,
    *,
    task_id: str,
    arm_id: str,
    artifact_paths: tuple[Path, ...],
) -> dict[str, Any]:
    frozen = read_json(workdir / "frozen_tasks.json")
    task = next((item for item in frozen.get("tasks", []) if item.get("task_id") == task_id), None)
    if task is None:
        raise BindingError(f"unknown task_id: {task_id}")
    result = read_json(result_path)

    for key in (
        "status",
        "command_identity",
        "evaluator_identity",
        "resource_receipt",
        "primary_metrics",
    ):
        if key not in result:
            raise BindingError(f"missing native result field: {key}")
    data_ids = non_blank_strings(result.get("data_identity_ids"), "data_identity_ids")
    source_ids = non_blank_strings(result.get("source_ids"), "source_ids")
    if not isinstance(result["resource_receipt"], dict):
        raise BindingError("resource_receipt must be an object")
    if not isinstance(result["primary_metrics"], dict):
        raise BindingError("primary_metrics must be an object")
    native_success = result.get("native_success")
    if native_success is not None and not isinstance(native_success, bool):
        raise BindingError("native_success must be boolean or null")
    critical = result.get("critical_false_completion")
    if critical is not None and not isinstance(critical, bool):
        raise BindingError("critical_false_completion must be boolean or null")

    artifacts = []
    for path in artifact_paths:
        if not path.exists() or not path.is_file():
            raise BindingError(f"artifact does not exist: {path}")
        artifacts.append(
            {
                "path": str(path.resolve()),
                "sha256": file_digest(path),
                "size_bytes": path.stat().st_size,
            }
        )

    bound = {
        "schema_version": "orion.v2.task-evaluation.v1",
        "task_id": task_id,
        "arm_id": arm_id,
        "benchmark_id": task["benchmark_id"],
        "status": result["status"],
        "native_success": native_success,
        "protected_decision_correct": result.get("protected_decision_correct"),
        "critical_false_completion": critical,
        "critical_new_failure_count": int(bool(critical)) if critical is not None else None,
        "primary_metrics": result["primary_metrics"],
        "secondary_metrics": result.get("secondary_metrics", {}),
        "command_identity": result["command_identity"],
        "evaluator_identity": result["evaluator_identity"],
        "data_identity_ids": data_ids,
        "source_ids": source_ids,
        "assumptions": result.get("assumptions", []),
        "uncertainty": result.get("uncertainty", "UNRESOLVED"),
        "resource_receipt": result["resource_receipt"],
        "artifact_receipts": artifacts,
        "independent_adjudication_id": result.get("independent_adjudication_id"),
        "scientific_truth_authorized": False,
        "field_status_authorized": False,
        "publication_readiness_authorized": False,
    }
    if result.get("scientific_truth_authorized") is True:
        raise BindingError("native result may not authorize scientific truth")
    if result.get("field_status_authorized") is True:
        raise BindingError("native result may not authorize field status")
    if result.get("publication_readiness_authorized") is True:
        raise BindingError("native result may not authorize publication readiness")

    write_json(workdir / "native_evaluations" / arm_id / f"{task_id}.json", bound)
    return bound


def parse_paths(values: list[str]) -> tuple[Path, ...]:
    return tuple(Path(value) for value in values)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--arm-id", required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--artifact", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        bound = bind(
            args.workdir,
            args.result,
            task_id=args.task_id,
            arm_id=args.arm_id,
            artifact_paths=parse_paths(args.artifact),
        )
    except (BindingError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(bound, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
