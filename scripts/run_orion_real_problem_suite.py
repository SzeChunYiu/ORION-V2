#!/usr/bin/env python3
"""Prepare, dispatch and evaluate the ORION-V2 real-problem suite.

The runner is intentionally model-provider agnostic. Each experimental arm is
bound to an executable through an environment variable:

    ORION_ARM_F2_ORION_METABOLIC_FULL='python my_agent.py'

The executable receives:

    --request REQUEST.json --response RESPONSE.json

Gold fixes and outcome data are never included in request files. The first
fully implemented native evaluator is BugsInPy; the CausalBench and Matbench
Discovery adapters are pinned and prepared but require their native data and
compute before scientific outcome scoring.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


DEFAULT_MANIFEST = Path("research/experiments/ORION_REAL_PROBLEM_SUITE_V1.json")


class RunnerError(RuntimeError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RunnerError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RunnerError(f"expected JSON object in {path}")
    return data


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )
    if check and result.returncode != 0:
        raise RunnerError(
            f"command failed ({result.returncode}): {shlex.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _unique(items: Iterable[str], label: str) -> None:
    values = tuple(items)
    if len(values) != len(set(values)):
        raise RunnerError(f"duplicate {label}: {values}")


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != "orion.v2.real-problem-suite.v1":
        errors.append("unexpected schema_version")
    benchmarks = manifest.get("benchmarks")
    arms = manifest.get("arms")
    if not isinstance(benchmarks, list) or not benchmarks:
        errors.append("benchmarks must be a non-empty list")
        benchmarks = []
    if not isinstance(arms, list) or not arms:
        errors.append("arms must be a non-empty list")
        arms = []
    try:
        _unique((item["benchmark_id"] for item in benchmarks), "benchmark ids")
        _unique((item["arm_id"] for item in arms), "arm ids")
    except (KeyError, TypeError, RunnerError) as exc:
        errors.append(str(exc))
    for benchmark in benchmarks:
        for key in ("benchmark_id", "repository", "commit", "adapter"):
            if not isinstance(benchmark.get(key), str) or not benchmark[key].strip():
                errors.append(f"benchmark missing {key}: {benchmark!r}")
        commit = benchmark.get("commit", "")
        if commit and not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append(f"benchmark commit is not a full SHA: {commit}")
    required_fields = set(manifest.get("agent_protocol", {}).get("required_response_fields", []))
    if "task_id" not in required_fields or "arm_id" not in required_fields:
        errors.append("agent response fields must include task_id and arm_id")
    authority = manifest.get("authority", {})
    if any(authority.get(key) is True for key in authority):
        errors.append("prospective suite must not grant authority")
    return errors


def _selected_ids(value: str | None, available: Iterable[str]) -> tuple[str, ...]:
    available_tuple = tuple(available)
    if not value:
        return available_tuple
    requested = tuple(item.strip() for item in value.split(",") if item.strip())
    unknown = sorted(set(requested) - set(available_tuple))
    if unknown:
        raise RunnerError(f"unknown ids: {', '.join(unknown)}")
    return requested


def _clone_pinned(repo_url: str, commit: str, destination: Path) -> None:
    if destination.exists() and not (destination / ".git").exists():
        raise RunnerError(f"destination exists but is not a git repository: {destination}")
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        _run(["git", "clone", "--no-checkout", repo_url, str(destination)], check=True)
    _run(["git", "fetch", "--depth", "1", "origin", commit], cwd=destination, check=True)
    _run(["git", "checkout", "--detach", commit], cwd=destination, check=True)
    actual = _run(["git", "rev-parse", "HEAD"], cwd=destination, check=True).stdout.strip()
    if actual != commit:
        raise RunnerError(f"commit mismatch for {destination}: expected {commit}, got {actual}")


def _venv_python(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def _venv_bin(venv: Path, command: str) -> Path:
    suffix = ".exe" if os.name == "nt" else ""
    return venv / ("Scripts" if os.name == "nt" else "bin") / f"{command}{suffix}"


def _ensure_venv(venv: Path) -> Path:
    python = _venv_python(venv)
    if not python.exists():
        _run([sys.executable, "-m", "venv", str(venv)], check=True)
    return python


def _install_editable(venv: Path, repository: Path) -> None:
    python = _ensure_venv(venv)
    _run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    _run([str(python), "-m", "pip", "install", "-e", str(repository)], check=True)


def _discover_bugsinpy_tasks(repository: Path, selection: dict[str, Any]) -> list[dict[str, Any]]:
    projects = tuple(selection.get("projects", ()))
    limit = int(selection.get("bugs_per_project", 1))
    if limit < 1:
        raise RunnerError("bugs_per_project must be positive")

    candidates: dict[str, set[int]] = defaultdict(set)
    for info_file in repository.rglob("bug.info"):
        parts = info_file.parts
        try:
            project_index = parts.index("projects") + 1
            project = parts[project_index]
        except (ValueError, IndexError):
            continue
        if projects and project not in projects:
            continue
        numeric_parts = [part for part in parts[project_index + 1 :] if part.isdigit()]
        if numeric_parts:
            candidates[project].add(int(numeric_parts[-1]))

    # Some BugsInPy layouts use directories without bug.info at the leaf.
    for project in projects:
        if candidates.get(project):
            continue
        root = repository / "projects" / project
        if root.exists():
            for child in root.rglob("*"):
                if child.is_dir() and child.name.isdigit():
                    candidates[project].add(int(child.name))

    missing = [project for project in projects if not candidates.get(project)]
    if missing:
        raise RunnerError(
            "no BugsInPy cases discovered for projects: " + ", ".join(sorted(missing))
        )

    tasks: list[dict[str, Any]] = []
    for project in projects or sorted(candidates):
        for bug_id in sorted(candidates[project])[:limit]:
            tasks.append(
                {
                    "task_id": f"bugsinpy-{project}-{bug_id}",
                    "benchmark_id": "bugsinpy",
                    "adapter": "bugsinpy",
                    "project": project,
                    "bug_id": bug_id,
                    "buggy_version": 0,
                    "fixed_version": 1,
                    "gold_withheld": True,
                    "network_allowed_during_solution": False,
                    "primary_decision": "produce an executable patch that fixes the real bug without critical regression",
                }
            )
    return tasks


def prepare_suite(
    manifest: dict[str, Any],
    workdir: Path,
    benchmark_filter: tuple[str, ...],
    *,
    install: bool,
) -> dict[str, Any]:
    benchmarks = {item["benchmark_id"]: item for item in manifest["benchmarks"]}
    selected = _selected_ids(",".join(benchmark_filter) if benchmark_filter else None, benchmarks)
    frozen_tasks: list[dict[str, Any]] = []
    frozen_benchmarks: list[dict[str, Any]] = []

    for benchmark_id in selected:
        benchmark = benchmarks[benchmark_id]
        repository = workdir / "benchmarks" / benchmark_id
        _clone_pinned(benchmark["repository"], benchmark["commit"], repository)
        venv = workdir / "venvs" / benchmark_id
        if install:
            _install_editable(venv, repository)
        frozen_benchmarks.append(
            {
                "benchmark_id": benchmark_id,
                "repository_path": str(repository.resolve()),
                "commit": benchmark["commit"],
                "adapter": benchmark["adapter"],
                "venv_path": str(venv.resolve()),
                "installed": install,
            }
        )
        if benchmark["adapter"] == "bugsinpy":
            frozen_tasks.extend(_discover_bugsinpy_tasks(repository, benchmark["selection"]))
        else:
            for index, variant in enumerate(benchmark.get("protected_variants", ()), start=1):
                frozen_tasks.append(
                    {
                        "task_id": f"{benchmark_id}-variant-{index:02d}",
                        "benchmark_id": benchmark_id,
                        "adapter": benchmark["adapter"],
                        "variant": variant,
                        "repository_path": str(repository.resolve()),
                        "execution_state": benchmark["execution_state"],
                        "native_commands": benchmark.get("native_commands", []),
                        "gold_withheld": True,
                    }
                )

    frozen = {
        "schema_version": "orion.v2.frozen-real-problem-tasks.v1",
        "suite_id": manifest["suite_id"],
        "manifest_path": str(DEFAULT_MANIFEST),
        "created_unix": time.time(),
        "benchmarks": frozen_benchmarks,
        "tasks": frozen_tasks,
        "outcome_access": "NONE",
        "authority": manifest["authority"],
    }
    _write_json(workdir / "frozen_tasks.json", frozen)
    return frozen


def _arm_contract(arm_id: str) -> dict[str, Any]:
    full_stages = [
        "INGEST",
        "DECOMPOSE",
        "SORT",
        "NATIVE_RECONSTRUCT",
        "REDUCE",
        "ABSORB",
        "RECOMBINE",
        "CHALLENGE",
        "ASSIMILATE_OR_RECYCLE",
    ]
    removed: list[str] = []
    if arm_id == "F2_MINUS_DECOMPOSITION":
        removed = ["DECOMPOSE", "SORT"]
    elif arm_id == "F2_MINUS_NATIVE_RECOVERY":
        removed = ["NATIVE_RECONSTRUCT"]
    elif arm_id == "F2_MINUS_COUNTERPROBE":
        removed = ["CHALLENGE"]
    elif arm_id == "F2_MINUS_SELECTIVE_REOPEN":
        removed = ["SELECTIVE_REOPEN"]
    return {
        "arm_id": arm_id,
        "required_stages": [stage for stage in full_stages if stage not in removed]
        if arm_id.startswith("F2_")
        else [],
        "removed_components": removed,
        "must_preserve": [
            "actual source identity",
            "assumptions and uncertainty",
            "gold and outcome blindness",
            "authority ceiling",
        ],
        "must_not_claim": [
            "scientific truth from self-consistency",
            "novelty from retrieval failure",
            "authority from confidence or utility",
        ],
    }


def issue_requests(
    manifest: dict[str, Any],
    workdir: Path,
    arm_filter: tuple[str, ...],
    task_filter: tuple[str, ...],
) -> int:
    frozen = _read_json(workdir / "frozen_tasks.json")
    arms = {item["arm_id"]: item for item in manifest["arms"]}
    selected_arms = _selected_ids(",".join(arm_filter) if arm_filter else None, arms)
    tasks = {item["task_id"]: item for item in frozen["tasks"]}
    selected_tasks = _selected_ids(",".join(task_filter) if task_filter else None, tasks)
    count = 0
    for arm_id in selected_arms:
        for task_id in selected_tasks:
            task = tasks[task_id]
            request = {
                "schema_version": "orion.v2.agent-request.v1",
                "suite_id": manifest["suite_id"],
                "task_id": task_id,
                "arm_id": arm_id,
                "task": task,
                "arm_contract": _arm_contract(arm_id),
                "resource_contract": manifest["resource_contract"],
                "anti_copy_controls": manifest["anti_copy_controls"],
                "response_requirements": manifest["agent_protocol"]["required_response_fields"],
                "gold_or_outcome_data_included": False,
                "requested_authority_ceiling": "PROPOSAL_ONLY",
            }
            _write_json(workdir / "requests" / arm_id / f"{task_id}.json", request)
            count += 1
    return count


def _arm_environment_name(arm_id: str) -> str:
    return "ORION_ARM_" + re.sub(r"[^A-Z0-9]+", "_", arm_id.upper()).strip("_")


def dispatch_agents(
    manifest: dict[str, Any],
    workdir: Path,
    arm_filter: tuple[str, ...],
    task_filter: tuple[str, ...],
    *,
    timeout_seconds: int,
) -> int:
    request_root = workdir / "requests"
    if not request_root.exists():
        raise RunnerError("requests do not exist; run the issue command first")
    arms = {item["arm_id"]: item for item in manifest["arms"]}
    selected_arms = _selected_ids(",".join(arm_filter) if arm_filter else None, arms)
    dispatched = 0
    for arm_id in selected_arms:
        command_text = os.environ.get(_arm_environment_name(arm_id), "").strip()
        requests = sorted((request_root / arm_id).glob("*.json"))
        if task_filter:
            allowed = set(task_filter)
            requests = [path for path in requests if path.stem in allowed]
        for request_path in requests:
            response_path = workdir / "responses" / arm_id / request_path.name
            log_path = workdir / "logs" / arm_id / f"{request_path.stem}.json"
            if not command_text:
                _write_json(
                    response_path,
                    {
                        "schema_version": "orion.v2.agent-response.v1",
                        "task_id": request_path.stem,
                        "arm_id": arm_id,
                        "status": "CANNOT_CHECK_MISSING_AGENT_COMMAND",
                        "proposed_patch_or_artifact": None,
                        "diagnosis": "No executable was bound through " + _arm_environment_name(arm_id),
                        "source_ids_used": [],
                        "assumptions": [],
                        "uncertainty": "UNRESOLVED",
                        "discriminator_or_tests": [],
                        "falsifier": "bind an agent executable and rerun",
                        "requested_authority": "NONE",
                    },
                )
                continue
            command = shlex.split(command_text) + [
                "--request",
                str(request_path.resolve()),
                "--response",
                str(response_path.resolve()),
            ]
            start = time.perf_counter()
            result = _run(command, timeout=timeout_seconds)
            elapsed = time.perf_counter() - start
            _write_json(
                log_path,
                {
                    "command": command,
                    "returncode": result.returncode,
                    "wall_time_seconds": elapsed,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                },
            )
            if not response_path.exists():
                _write_json(
                    response_path,
                    {
                        "schema_version": "orion.v2.agent-response.v1",
                        "task_id": request_path.stem,
                        "arm_id": arm_id,
                        "status": "EXECUTION_FAILED_NO_RESPONSE",
                        "proposed_patch_or_artifact": None,
                        "diagnosis": result.stderr[-4000:],
                        "source_ids_used": [],
                        "assumptions": [],
                        "uncertainty": "UNRESOLVED",
                        "discriminator_or_tests": [],
                        "falsifier": "agent must produce a schema-valid response",
                        "requested_authority": "NONE",
                    },
                )
            dispatched += 1
    return dispatched


def _benchmark_record(frozen: dict[str, Any], benchmark_id: str) -> dict[str, Any]:
    for item in frozen["benchmarks"]:
        if item["benchmark_id"] == benchmark_id:
            return item
    raise RunnerError(f"missing frozen benchmark record: {benchmark_id}")


def _bugsinpy_binary(record: dict[str, Any], name: str) -> str:
    venv = Path(record["venv_path"])
    candidate = _venv_bin(venv, name)
    if candidate.exists():
        return str(candidate)
    located = shutil.which(name)
    if located:
        return located
    raise RunnerError(
        f"{name} not found. Rerun prepare with --install or install BugsInPy in PATH."
    )


def _extract_patch(response: dict[str, Any]) -> str | None:
    artifact = response.get("proposed_patch_or_artifact")
    if artifact is None:
        return None
    if isinstance(artifact, str):
        return artifact
    if isinstance(artifact, dict):
        if artifact.get("type") == "unified_diff" and isinstance(artifact.get("content"), str):
            return artifact["content"]
        if artifact.get("type") == "path" and isinstance(artifact.get("path"), str):
            path = Path(artifact["path"])
            return path.read_text(encoding="utf-8") if path.exists() else None
    return None


def _run_bugsinpy_relevant_test(workspace: Path, *, timeout: int) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    env_bin = workspace / ("env/Scripts" if os.name == "nt" else "env/bin")
    environment["PATH"] = str(env_bin) + os.pathsep + environment.get("PATH", "")
    environment["VIRTUAL_ENV"] = str(workspace / "env")
    return _run(["bash", "bugsinpy_run_test.sh"], cwd=workspace, env=environment, timeout=timeout)


def _bugsinpy_test_infrastructure_error(result: subprocess.CompletedProcess[str]) -> bool:
    combined = (result.stdout + "\n" + result.stderr).casefold()
    return result.returncode in {4, 5} or any(marker in combined for marker in (
        "modulenotfounderror", "importerror while loading conftest",
        "unable to import required dependencies", "command not found",
        "no module named", "could not find a version that satisfies",
        "error: file not found:", "no tests ran", "collected 0 items",
    ))


def _evaluate_bugsinpy(
    frozen: dict[str, Any],
    workdir: Path,
    task: dict[str, Any],
    response: dict[str, Any],
    arm_id: str,
    *,
    timeout_seconds: int,
) -> dict[str, Any]:
    record = _benchmark_record(frozen, "bugsinpy")
    repository = Path(record["repository_path"])
    checkout = _bugsinpy_binary(record, "bugsinpy-checkout")
    compile_command = _bugsinpy_binary(record, "bugsinpy-compile")
    test_command = _bugsinpy_binary(record, "bugsinpy-test")
    workspace = workdir / "runs" / arm_id / task["task_id"] / "workspace"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.parent.mkdir(parents=True, exist_ok=True)

    checkout_result = _run(
        [
            checkout,
            "-p",
            str(task["project"]),
            "-v",
            str(task["buggy_version"]),
            "-i",
            str(task["bug_id"]),
            "-w",
            str(workspace),
        ],
        cwd=repository,
        timeout=timeout_seconds,
    )
    project_workspace = workspace / str(task["project"])
    patch = _extract_patch(response)
    patch_result: subprocess.CompletedProcess[str] | None = None
    if checkout_result.returncode == 0 and patch:
        patch_result = subprocess.run(
            ["git", "apply", "--whitespace=nowarn", "-"],
            cwd=str(project_workspace),
            input=patch,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    compile_result: subprocess.CompletedProcess[str] | None = None
    test_result: subprocess.CompletedProcess[str] | None = None
    start = time.perf_counter()
    if checkout_result.returncode == 0 and patch_result and patch_result.returncode == 0:
        compile_environment = os.environ.copy()
        if project_python_bin := str(task.get("project_python_bin") or "").strip():
            compile_environment["PATH"] = project_python_bin + os.pathsep + compile_environment.get("PATH", "")
        compile_result = _run(
            [compile_command], cwd=project_workspace, env=compile_environment,
            timeout=timeout_seconds,
        )
        if compile_result.returncode == 0:
            test_result = _run_bugsinpy_relevant_test(project_workspace, timeout=timeout_seconds)
    elapsed = time.perf_counter() - start

    infrastructure_error = bool(test_result and _bugsinpy_test_infrastructure_error(test_result))
    passed = bool(test_result and test_result.returncode == 0 and not infrastructure_error)
    return {
        "schema_version": "orion.v2.task-evaluation.v1",
        "task_id": task["task_id"],
        "arm_id": arm_id,
        "benchmark_id": "bugsinpy",
        "agent_status": response.get("status"),
        "checkout_returncode": checkout_result.returncode,
        "patch_present": patch is not None,
        "patch_apply_returncode": patch_result.returncode if patch_result else None,
        "compile_returncode": compile_result.returncode if compile_result else None,
        "test_returncode": test_result.returncode if test_result else None,
        "test_infrastructure_error": infrastructure_error,
        "original_failing_tests_fixed": passed,
        "native_success": passed,
        "full_regression_suite_passed": None,
        "full_regression_suite_status": "CANNOT_CHECK_NOT_RUN",
        "critical_new_failure_count": None,
        "wall_time_seconds": elapsed,
        "patch_size_bytes": len(patch.encode("utf-8")) if patch else 0,
        "metamorphic_or_mutation_test_pass_rate": "NOT_RUN",
        "gold_patch_text_similarity_diagnostic": "WITHHELD_NOT_COMPUTED",
        "scientific_truth_authorized": false,
        "field_status_authorized": false,
        "stdout_tail": test_result.stdout[-4000:] if test_result else "",
        "stderr_tail": (
            test_result.stderr[-4000:]
            if test_result
            else compile_result.stderr[-4000:]
            if compile_result
            else patch_result.stderr[-4000:]
            if patch_result
            else checkout_result.stderr[-4000:]
        ),
    }


def evaluate_responses(
    manifest: dict[str, Any],
    workdir: Path,
    arm_filter: tuple[str, ...],
    task_filter: tuple[str, ...],
    *,
    timeout_seconds: int,
) -> int:
    frozen = _read_json(workdir / "frozen_tasks.json")
    tasks = {item["task_id"]: item for item in frozen["tasks"]}
    arms = {item["arm_id"]: item for item in manifest["arms"]}
    selected_arms = _selected_ids(",".join(arm_filter) if arm_filter else None, arms)
    selected_tasks = _selected_ids(",".join(task_filter) if task_filter else None, tasks)
    count = 0
    for arm_id in selected_arms:
        for task_id in selected_tasks:
            response_path = workdir / "responses" / arm_id / f"{task_id}.json"
            if not response_path.exists():
                continue
            response = _read_json(response_path)
            task = tasks[task_id]
            if task["adapter"] == "bugsinpy":
                try:
                    evaluation = _evaluate_bugsinpy(
                        frozen,
                        workdir,
                        task,
                        response,
                        arm_id,
                        timeout_seconds=timeout_seconds,
                    )
                except (RunnerError, OSError, subprocess.SubprocessError) as exc:
                    evaluation = {
                        "schema_version": "orion.v2.task-evaluation.v1",
                        "task_id": task_id,
                        "arm_id": arm_id,
                        "benchmark_id": task["benchmark_id"],
                        "status": "CANNOT_CHECK_EVALUATOR_FAILURE",
                        "reason": str(exc),
                        "scientific_truth_authorized": False,
                        "field_status_authorized": False,
                    }
            else:
                evaluation = {
                    "schema_version": "orion.v2.task-evaluation.v1",
                    "task_id": task_id,
                    "arm_id": arm_id,
                    "benchmark_id": task["benchmark_id"],
                    "status": "CANNOT_CHECK_NATIVE_DATA_OR_COMPUTE_NOT_BOUND",
                    "native_commands": task.get("native_commands", []),
                    "reason": "Run the pinned native benchmark with its required data, then bind its result artifact to this task.",
                    "scientific_truth_authorized": False,
                    "field_status_authorized": False,
                }
            _write_json(workdir / "evaluations" / arm_id / f"{task_id}.json", evaluation)
            count += 1
    return count


def summarize(workdir: Path) -> dict[str, Any]:
    evaluations = []
    for path in sorted((workdir / "evaluations").glob("*/*.json")):
        evaluations.append(_read_json(path))
    by_arm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in evaluations:
        by_arm[str(item.get("arm_id", "UNKNOWN"))].append(item)
    arm_metrics: dict[str, Any] = {}
    for arm_id, items in sorted(by_arm.items()):
        completed = [item for item in items if item.get("benchmark_id") == "bugsinpy"]
        passed = sum(bool(item.get("full_regression_suite_passed")) for item in completed)
        critical = sum(int(item.get("critical_new_failure_count", 0) or 0) for item in completed)
        statuses = Counter(str(item.get("status", item.get("agent_status", "UNKNOWN"))) for item in items)
        arm_metrics[arm_id] = {
            "evaluation_count": len(items),
            "bugsinpy_count": len(completed),
            "bugsinpy_passed": passed,
            "bugsinpy_pass_rate": passed / len(completed) if completed else None,
            "critical_failure_count": critical,
            "status_counts": dict(statuses),
        }
    summary = {
        "schema_version": "orion.v2.real-problem-summary.v1",
        "evaluation_count": len(evaluations),
        "arm_metrics": arm_metrics,
        "component_effects": "NOT_ESTIMABLE_UNTIL_MATCHED_FULL_AND_ABLATION_RUNS_EXIST",
        "resource_pareto": "NOT_ESTIMABLE_UNTIL_RESOURCE_RECEIPTS_EXIST",
        "field_status": "NOT_ESTABLISHED",
        "publication_readiness": "NOT_ESTABLISHED",
    }
    _write_json(workdir / "aggregate" / "arm_metrics.json", summary)
    return summary


def _parse_csv(value: str | None) -> tuple[str, ...]:
    return tuple(item.strip() for item in (value or "").split(",") if item.strip())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-real-problem-suite"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate")

    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--benchmarks", default="")
    prepare.add_argument("--install", action="store_true")

    issue = subparsers.add_parser("issue")
    issue.add_argument("--arms", default="")
    issue.add_argument("--tasks", default="")

    dispatch = subparsers.add_parser("dispatch")
    dispatch.add_argument("--arms", default="")
    dispatch.add_argument("--tasks", default="")
    dispatch.add_argument("--timeout-seconds", type=int, default=2700)

    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("--arms", default="")
    evaluate.add_argument("--tasks", default="")
    evaluate.add_argument("--timeout-seconds", type=int, default=2700)

    subparsers.add_parser("summarize")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = _read_json(args.manifest)
    errors = validate_manifest(manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    workdir: Path = args.workdir

    try:
        if args.command == "validate":
            print("manifest valid")
        elif args.command == "prepare":
            frozen = prepare_suite(
                manifest,
                workdir,
                _parse_csv(args.benchmarks),
                install=args.install,
            )
            print(f"prepared {len(frozen['tasks'])} tasks")
        elif args.command == "issue":
            count = issue_requests(
                manifest,
                workdir,
                _parse_csv(args.arms),
                _parse_csv(args.tasks),
            )
            print(f"issued {count} requests")
        elif args.command == "dispatch":
            count = dispatch_agents(
                manifest,
                workdir,
                _parse_csv(args.arms),
                _parse_csv(args.tasks),
                timeout_seconds=args.timeout_seconds,
            )
            print(f"dispatched {count} agent runs")
        elif args.command == "evaluate":
            count = evaluate_responses(
                manifest,
                workdir,
                _parse_csv(args.arms),
                _parse_csv(args.tasks),
                timeout_seconds=args.timeout_seconds,
            )
            print(f"evaluated {count} responses")
        elif args.command == "summarize":
            summary = summarize(workdir)
            print(json.dumps(summary, indent=2, sort_keys=True))
        else:
            raise RunnerError(f"unsupported command: {args.command}")
    except (RunnerError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
