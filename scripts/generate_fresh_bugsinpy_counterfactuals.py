#!/usr/bin/env python3
"""Generate fresh, gold-blind counterfactual repair tasks from fixed BugsInPy cases.

The generator mutates production-code tokens *after* protocol freeze, retains the
reverse patch in a private registry, strips original Git history from the solver
workspace, and accepts only mutations that make a previously passing fixed case
fail its native test suite. These tasks supplement real historical bugs; they do
not replace naturalistic evaluation.
"""

from __future__ import annotations

import argparse
import difflib
import io
import json
import os
import random
import shutil
import stat
import subprocess
import sys
import time
import tokenize
from pathlib import Path
from typing import Any, Iterable


OPERATOR_REPLACEMENTS = {
    "==": "!=",
    "!=": "==",
    "<": "<=",
    "<=": "<",
    ">": ">=",
    ">=": ">",
    "+": "-",
    "-": "+",
}
NAME_REPLACEMENTS = {"True": "False", "False": "True", "and": "or", "or": "and"}
EXCLUDED_PARTS = {
    ".git",
    ".tox",
    ".venv",
    "venv",
    "env",
    "site-packages",
    "tests",
    "test",
    "testing",
    "docs",
    "examples",
}


class CounterfactualError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CounterfactualError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CounterfactualError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 2700,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def venv_bin(venv: Path, name: str) -> Path:
    directory = "Scripts" if os.name == "nt" else "bin"
    suffix = ".cmd" if os.name == "nt" else ""
    return venv / directory / f"{name}{suffix}"


def source_files(workspace: Path) -> list[Path]:
    result: list[Path] = []
    for path in workspace.rglob("*.py"):
        relative = path.relative_to(workspace)
        lowered = {part.casefold() for part in relative.parts}
        if lowered & EXCLUDED_PARTS:
            continue
        if path.name.startswith("test_") or path.name.endswith("_test.py"):
            continue
        if path.stat().st_size > 300_000:
            continue
        result.append(path)
    return sorted(result)


def mutation_candidates(path: Path) -> list[tuple[int, str, str]]:
    try:
        text = path.read_text(encoding="utf-8")
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (OSError, UnicodeDecodeError, tokenize.TokenError, IndentationError):
        return []
    candidates: list[tuple[int, str, str]] = []
    for index, token in enumerate(tokens):
        replacement = None
        if token.type == tokenize.OP:
            replacement = OPERATOR_REPLACEMENTS.get(token.string)
        elif token.type == tokenize.NAME:
            replacement = NAME_REPLACEMENTS.get(token.string)
        if replacement is not None:
            candidates.append((index, token.string, replacement))
    return candidates


def apply_mutation(path: Path, token_index: int, replacement: str) -> tuple[str, str]:
    original = path.read_text(encoding="utf-8")
    tokens = list(tokenize.generate_tokens(io.StringIO(original).readline))
    token = tokens[token_index]
    tokens[token_index] = tokenize.TokenInfo(
        token.type,
        replacement,
        token.start,
        token.end,
        token.line,
    )
    mutated = tokenize.untokenize(tokens)
    compile(mutated, str(path), "exec")
    path.write_text(mutated, encoding="utf-8")
    return original, mutated


def reverse_patch(relative: Path, original: str, mutated: str) -> str:
    return "".join(
        difflib.unified_diff(
            mutated.splitlines(keepends=True),
            original.splitlines(keepends=True),
            fromfile=f"a/{relative.as_posix()}",
            tofile=f"b/{relative.as_posix()}",
        )
    )


def copy_without_git(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".git"))
    run(["git", "init", "-q"], cwd=destination, timeout=60)
    run(["git", "config", "user.email", "orion-counterfactual@example.invalid"], cwd=destination, timeout=60)
    run(["git", "config", "user.name", "ORION Counterfactual Generator"], cwd=destination, timeout=60)
    run(["git", "add", "-A"], cwd=destination, timeout=120)
    commit = run(["git", "commit", "-q", "-m", "counterfactual solver state"], cwd=destination, timeout=120)
    if commit.returncode != 0:
        raise CounterfactualError(commit.stderr[-3000:])


def choose_tasks(frozen: dict[str, Any], selected: set[str] | None) -> list[dict[str, Any]]:
    tasks = [task for task in frozen.get("tasks", []) if task.get("benchmark_id") == "bugsinpy"]
    if selected:
        tasks = [task for task in tasks if task.get("task_id") in selected]
    return tasks


def generate(
    source_workdir: Path,
    output_workdir: Path,
    *,
    selected_tasks: set[str] | None,
    count: int,
    seed: int,
    maximum_candidates_per_task: int,
    timeout_seconds: int,
) -> dict[str, Any]:
    source_frozen = read_json(source_workdir / "frozen_tasks.json")
    benchmark = next(
        (
            item
            for item in source_frozen.get("benchmarks", [])
            if item.get("benchmark_id") == "bugsinpy"
        ),
        None,
    )
    if benchmark is None:
        raise CounterfactualError("source workdir has no BugsInPy benchmark")
    repository = Path(benchmark["repository_path"])
    venv = Path(benchmark["venv_path"])
    checkout = venv_bin(venv, "bugsinpy-checkout")
    compile_command = venv_bin(venv, "bugsinpy-compile")
    test_command = venv_bin(venv, "bugsinpy-test")
    for command in (checkout, compile_command, test_command):
        if not command.exists():
            raise CounterfactualError(
                f"missing {command}; bootstrap BugsInPy before generating counterfactuals"
            )

    generator = random.Random(seed)
    public_tasks: list[dict[str, Any]] = []
    private_records: list[dict[str, Any]] = []
    base_tasks = choose_tasks(source_frozen, selected_tasks)
    if not base_tasks:
        raise CounterfactualError("no eligible base tasks")

    for base_task in base_tasks:
        if len(public_tasks) >= count:
            break
        base_id = str(base_task["task_id"])
        private_workspace = output_workdir / "private_generation" / base_id
        if private_workspace.exists():
            shutil.rmtree(private_workspace)
        private_workspace.parent.mkdir(parents=True, exist_ok=True)
        checkout_result = run(
            [
                str(checkout),
                "-p",
                str(base_task["project"]),
                "-v",
                str(base_task.get("fixed_version", 1)),
                "-i",
                str(base_task["bug_id"]),
                "-w",
                str(private_workspace),
            ],
            cwd=repository,
            timeout=timeout_seconds,
        )
        if checkout_result.returncode != 0:
            continue
        project_workspace = private_workspace / str(base_task["project"])
        if not project_workspace.is_dir():
            continue
        compile_result = run([str(compile_command)], cwd=project_workspace, timeout=timeout_seconds)
        baseline = run([str(test_command)], cwd=project_workspace, timeout=timeout_seconds) if compile_result.returncode == 0 else None
        if compile_result.returncode != 0 or baseline is None or baseline.returncode != 0:
            continue

        candidates: list[tuple[Path, int, str, str]] = []
        for path in source_files(project_workspace):
            for token_index, old, new in mutation_candidates(path):
                candidates.append((path, token_index, old, new))
        generator.shuffle(candidates)
        selected_mutation: dict[str, Any] | None = None
        selected_original = ""
        selected_mutated = ""
        selected_path: Path | None = None

        for path, token_index, old, new in candidates[:maximum_candidates_per_task]:
            try:
                original, mutated = apply_mutation(path, token_index, new)
            except (OSError, SyntaxError, tokenize.TokenError, IndentationError):
                continue
            compile_mutation = run([str(compile_command)], cwd=project_workspace, timeout=timeout_seconds)
            test_mutation = run([str(test_command)], cwd=project_workspace, timeout=timeout_seconds) if compile_mutation.returncode == 0 else None
            path.write_text(original, encoding="utf-8")
            if compile_mutation.returncode == 0 and test_mutation is not None and test_mutation.returncode != 0:
                path.write_text(mutated, encoding="utf-8")
                selected_original = original
                selected_mutated = mutated
                selected_path = path
                selected_mutation = {
                    "relative_path": str(path.relative_to(project_workspace)),
                    "token_index": token_index,
                    "old_token": old,
                    "new_token": new,
                    "failing_stdout_tail": test_mutation.stdout[-3000:],
                    "failing_stderr_tail": test_mutation.stderr[-3000:],
                }
                break

        if selected_mutation is None or selected_path is None:
            continue

        task_number = len(public_tasks) + 1
        task_id = f"fresh-bugsinpy-{task_number:03d}-{base_task['project']}"
        solver_workspace = output_workdir / "solver_workspaces" / task_id
        copy_without_git(project_workspace, solver_workspace)
        relative = Path(selected_mutation["relative_path"])
        gold = reverse_patch(relative, selected_original, selected_mutated)
        gold_path = output_workdir / "private_gold" / f"{task_id}.patch"
        gold_path.parent.mkdir(parents=True, exist_ok=True)
        gold_path.write_text(gold, encoding="utf-8")
        if os.name != "nt":
            gold_path.chmod(stat.S_IRUSR | stat.S_IWUSR)

        public_tasks.append(
            {
                "task_id": task_id,
                "benchmark_id": "fresh_bugsinpy_counterfactual",
                "adapter": "fresh_bugsinpy_counterfactual",
                "project": base_task["project"],
                "source_case_id": base_id,
                "solver_workspace": str(solver_workspace.resolve()),
                "workspace_contains_gold": False,
                "network_allowed_during_solution": False,
                "gold_withheld": True,
                "primary_decision": "repair a freshly generated production-code defect under the native regression suite",
                "solver_test_command": str(test_command),
                "baseline_observation": {
                    "compile_returncode": 0,
                    "test_returncode": test_mutation.returncode,
                    "bug_reproduced": True,
                    "stdout_tail": selected_mutation["failing_stdout_tail"],
                    "stderr_tail": selected_mutation["failing_stderr_tail"],
                    "gold_or_fixed_solution_included": False,
                },
            }
        )
        private_records.append(
            {
                "task_id": task_id,
                "source_case_id": base_id,
                "private_mutated_template": str(project_workspace.resolve()),
                "gold_patch_path": str(gold_path.resolve()),
                "mutation": selected_mutation,
                "compile_command": str(compile_command),
                "test_command": str(test_command),
                "generator_seed": seed,
                "outcome_access_for_solver": "NONE",
            }
        )

    public_frozen = {
        "schema_version": "orion.v2.frozen-real-problem-tasks.v1",
        "suite_id": f"orion-fresh-counterfactual-{seed}",
        "created_unix": time.time(),
        "benchmarks": [
            {
                "benchmark_id": "fresh_bugsinpy_counterfactual",
                "adapter": "fresh_bugsinpy_counterfactual",
                "source_benchmark_commit": benchmark["commit"],
                "venv_path": str(venv.resolve()),
                "repository_path": str(repository.resolve()),
            }
        ],
        "tasks": public_tasks,
        "outcome_access": "NONE",
        "authority": {
            "scientific_truth": False,
            "field_status": False,
            "publication_readiness": False,
        },
    }
    private_registry = {
        "schema_version": "orion.v2.private-counterfactual-registry.v1",
        "suite_id": public_frozen["suite_id"],
        "records": private_records,
        "solver_access": "FORBIDDEN",
        "authority": public_frozen["authority"],
    }
    write_json(output_workdir / "frozen_tasks.json", public_frozen)
    write_json(output_workdir / "private_evaluation_registry.json", private_registry)
    write_json(
        output_workdir / "aggregate" / "counterfactual_generation.json",
        {
            "schema_version": "orion.v2.counterfactual-generation.v1",
            "requested_count": count,
            "generated_count": len(public_tasks),
            "seed": seed,
            "candidate_limit_per_task": maximum_candidates_per_task,
            "source_case_ids": [task["source_case_id"] for task in public_tasks],
            "gold_exposed_to_solver": False,
            "scientific_truth_authorized": False,
        },
    )
    return public_frozen


def parse_ids(value: str) -> set[str] | None:
    result = {item.strip() for item in value.split(",") if item.strip()}
    return result or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument("--output-workdir", type=Path, default=Path(".orion-fresh-counterfactual-suite"))
    parser.add_argument("--tasks", default="")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260828)
    parser.add_argument("--maximum-candidates-per-task", type=int, default=40)
    parser.add_argument("--timeout-seconds", type=int, default=2700)
    args = parser.parse_args(argv)
    try:
        result = generate(
            args.source_workdir,
            args.output_workdir,
            selected_tasks=parse_ids(args.tasks),
            count=args.count,
            seed=args.seed,
            maximum_candidates_per_task=args.maximum_candidates_per_task,
            timeout_seconds=args.timeout_seconds,
        )
    except (CounterfactualError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"generated {len(result['tasks'])} fresh gold-blind counterfactual tasks")
    return 0 if result["tasks"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
