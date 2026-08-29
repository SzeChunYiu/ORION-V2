#!/usr/bin/env python3
"""Bind public BugsInPy test-support mounts to generated counterfactual tasks."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


class EnrichmentError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EnrichmentError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EnrichmentError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def venv_command(venv: Path, name: str) -> Path:
    directory = "Scripts" if os.name == "nt" else "bin"
    suffix = ".cmd" if os.name == "nt" else ""
    return venv / directory / f"{name}{suffix}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument("--fresh-workdir", type=Path, default=Path(".orion-fresh-counterfactual-suite"))
    args = parser.parse_args(argv)

    source = read_json(args.source_workdir / "frozen_tasks.json")
    fresh_path = args.fresh_workdir / "frozen_tasks.json"
    fresh = read_json(fresh_path)
    benchmark = next(
        (item for item in source.get("benchmarks", []) if item.get("benchmark_id") == "bugsinpy"),
        None,
    )
    if benchmark is None:
        raise EnrichmentError("source BugsInPy benchmark is missing")
    venv = Path(benchmark["venv_path"]).resolve()
    repository = Path(benchmark["repository_path"]).resolve()
    compile_command = venv_command(venv, "bugsinpy-compile")
    test_command = venv_command(venv, "bugsinpy-test")
    for path in (venv, repository, compile_command, test_command):
        if not path.exists():
            raise EnrichmentError(f"required support path is absent: {path}")

    for task in fresh.get("tasks", []):
        task["solver_compile_command"] = str(compile_command)
        task["solver_test_command"] = str(test_command)
        task["solver_support_mounts"] = [str(venv), str(repository)]
        task["solver_support_contains_historical_framework_metadata"] = True
        task["fresh_gold_is_not_in_support_mounts"] = True
    write_json(fresh_path, fresh)
    print(f"enriched {len(fresh.get('tasks', []))} counterfactual tasks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EnrichmentError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
