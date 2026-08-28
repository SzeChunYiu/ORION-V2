#!/usr/bin/env python3
"""Create per-task/per-arm native-result input templates from frozen tasks."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any


class TemplateError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TemplateError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise TemplateError(f"expected JSON object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def parse_ids(value: str) -> set[str] | None:
    result = {item.strip() for item in value.split(",") if item.strip()}
    return result or None


def materialize(
    workdir: Path,
    template_path: Path,
    *,
    arms: set[str] | None,
    tasks: set[str] | None,
) -> int:
    frozen = read_json(workdir / "frozen_tasks.json")
    template = read_json(template_path)
    count = 0
    for task in frozen.get("tasks", []):
        task_id = str(task["task_id"])
        if tasks and task_id not in tasks:
            continue
        task_arms = arms or {"F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"}
        for arm_id in sorted(task_arms):
            value = copy.deepcopy(template)
            value["task_id"] = task_id
            value["arm_id"] = arm_id
            value["benchmark_id"] = task["benchmark_id"]
            value["task_variant"] = task.get("variant")
            value["native_commands_frozen"] = task.get("native_commands", [])
            value["status"] = "CANNOT_CHECK_NATIVE_RUN_NOT_EXECUTED"
            write_json(
                workdir / "native_result_inputs" / arm_id / f"{task_id}.json",
                value,
            )
            count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument(
        "--template",
        type=Path,
        default=Path("research/experiments/NATIVE_BENCHMARK_RESULT_TEMPLATE_V1.json"),
    )
    parser.add_argument("--arms", default="F0_PARENT_FEDERATION,F2_ORION_METABOLIC_FULL")
    parser.add_argument("--tasks", default="")
    args = parser.parse_args(argv)
    try:
        count = materialize(
            args.workdir,
            args.template,
            arms=parse_ids(args.arms),
            tasks=parse_ids(args.tasks),
        )
    except (TemplateError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"materialized {count} native-result templates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
