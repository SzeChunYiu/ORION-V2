#!/usr/bin/env python3
"""Freeze the corrected E30 task identities and sanitize solver workspaces.

Discovery uses BugsInPy directory names only.  This module never opens
``bug.info`` or any fixed/gold/solution patch metadata.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PreparationError(RuntimeError):
    """The protected E30 input surface could not be frozen safely."""


FORBIDDEN_DIRECTORIES = {
    ".git",
    ".pytest_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "env",
    "venv",
}
FORBIDDEN_METADATA = {
    "bug.info",
    "bugsinpy_compile_flag",
    "bugsinpy_bug.info",
    "bugsinpy_patchfile.info",
    "e20_failfast_compile.log",
    "e20_failfast_compile_receipt.json",
    "fixed.patch",
    "gold.patch",
    "solution.patch",
}
FORBIDDEN_BUILD_SUFFIXES = {".a", ".dll", ".dylib", ".o", ".pyc", ".pyo", ".so"}


def _forbidden(path: Path) -> bool:
    name = path.name.casefold()
    return (
        name in FORBIDDEN_DIRECTORIES
        or name.endswith(".egg-info")
        or name in FORBIDDEN_METADATA
        or path.suffix.casefold() in FORBIDDEN_BUILD_SUFFIXES
        or any(f"{word}.patch" in name for word in ("gold", "fixed", "solution"))
        or (name.endswith(".patch") and any(word in name for word in ("gold", "fixed", "solution")))
    )


def audit_public_workspace(workspace: Path) -> None:
    """Reject a solver-public tree containing any prohibited path surface."""
    for path in workspace.rglob("*"):
        if path.is_symlink():
            raise PreparationError(f"solver-public symlink is forbidden: {path.relative_to(workspace)}")
        if _forbidden(path):
            raise PreparationError(f"solver-public forbidden path: {path.relative_to(workspace)}")


def sanitize_workspace(private: Path, public: Path) -> dict[str, Any]:
    """Copy allowed files without opening or following forbidden private paths."""
    private = private.resolve()
    public = public.resolve()
    if private == public or private in public.parents or public in private.parents:
        raise PreparationError("private and solver-public workspace roots must be separate")
    if not private.is_dir():
        raise PreparationError(f"private workspace is missing: {private}")
    if public.exists():
        raise PreparationError(f"solver-public destination already exists: {public}")
    public.mkdir(parents=True)
    copied = forbidden = symlinks = 0
    pending = [(private, public)]
    while pending:
        source_dir, destination_dir = pending.pop()
        for source in sorted(source_dir.iterdir(), key=lambda item: item.name):
            if source.is_symlink():
                symlinks += 1
                continue
            if _forbidden(source):
                forbidden += 1
                continue
            destination = destination_dir / source.name
            if source.is_dir():
                destination.mkdir()
                pending.append((source, destination))
            elif source.is_file():
                shutil.copy2(source, destination, follow_symlinks=False)
                copied += 1
    audit_public_workspace(public)
    return {
        "schema_version": "orion.v2.e30-workspace-sanitization.v1",
        "copied_file_count": copied,
        "excluded_forbidden_count": forbidden,
        "excluded_symlink_count": symlinks,
        "gold_or_fixed_content_read": False,
        "audit_status": "PASS",
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_public_manifest(public_root: Path, destination: Path) -> int:
    records = []
    for path in sorted(item for item in public_root.rglob("*") if item.is_file()):
        relative = path.relative_to(public_root.parent).as_posix()
        records.append(f"{sha256(path)}  {relative}\n")
    destination.write_text("".join(records), encoding="utf-8")
    return len(records)


def prepare(
    *,
    repository: Path,
    private_root: Path,
    output_root: Path,
    correction_path: Path,
    orion_source_sha: str,
    observed_bugsinpy_commit: str,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Freeze identities and construct a content-bound solver-public surface."""
    repository = repository.resolve()
    private_root = private_root.resolve()
    output_root = output_root.resolve()
    correction_path = correction_path.resolve()
    if output_root.exists():
        raise PreparationError(f"output root already exists: {output_root}")
    correction = json.loads(correction_path.read_text(encoding="utf-8"))
    expected_commit = str(correction["bugsinpy_commit"])
    if observed_bugsinpy_commit != expected_commit:
        raise PreparationError(
            f"BugsInPy identity mismatch: expected {expected_commit}, got {observed_bugsinpy_commit}"
        )
    selection = discover_and_correct(repository, correction)
    output_root.mkdir(parents=True)
    public_root = output_root / "solver_public"
    public_root.mkdir()
    frozen_tasks = []
    private_records = []
    sanitization_records = []
    for task in selection["tasks"]:
        task_id = str(task["task_id"])
        private_workspace = private_root / task_id
        public_workspace = public_root / task_id
        receipt = sanitize_workspace(private_workspace, public_workspace)
        frozen_task = dict(task)
        frozen_task.update(
            {
                "solver_workspace": str(public_workspace),
                "workspace_contains_gold": False,
                "workspace_contains_git_history": False,
                "network_allowed_during_solution": False,
                "solver_may_return": "unified_diff_only",
            }
        )
        frozen_tasks.append(frozen_task)
        private_records.append(
            {
                "task_id": task_id,
                "evaluator_private_workspace": str(private_workspace),
                "solver_public_workspace": str(public_workspace),
                "private_content_hash_status": "NOT_COMPUTED_TO_AVOID_GOLD_OR_FIXED_ACCESS",
                "gold_or_fixed_content_read": False,
            }
        )
        sanitization_records.append({"task_id": task_id, **receipt})

    audit_public_workspace(public_root)
    manifest_path = output_root / "PUBLIC_WORKSPACES_MANIFEST.sha256"
    public_file_count = write_public_manifest(public_root, manifest_path)
    correction_sha = sha256(correction_path)
    script_sha = sha256(Path(__file__).resolve())
    frozen = {
        "schema_version": "orion.v2.frozen-real-problem-tasks.v1",
        "suite_id": "orion-v2-real-problem-confirmatory-2026-08-28",
        "orion_source_sha": orion_source_sha,
        "bugsinpy_commit": observed_bugsinpy_commit,
        "task_correction_sha256": correction_sha,
        "tasks": frozen_tasks,
        "outcome_access": "NONE",
        "authority": {
            "scientific_truth": False,
            "field_status": False,
            "publication_readiness": False,
        },
    }
    private_registry = {
        "schema_version": "orion.v2.e30-private-evaluator-registry.v1",
        "records": private_records,
        "solver_access_authorized": False,
        "gold_or_fixed_content_read": False,
    }
    actual_run_id = run_id or f"e45-e30-r1-protected-{orion_source_sha[:8]}"
    identity = {
        "schema_version": "orion.v2.execution-run-identity.v1",
        "run_id": actual_run_id,
        "phase": "E30",
        "orion_source_sha": orion_source_sha,
        "bugsinpy_commit": observed_bugsinpy_commit,
        "preparer_sha256": script_sha,
        "task_correction_sha256": correction_sha,
        "original_task_count": selection["original_task_count"],
        "corrected_task_count": selection["corrected_task_count"],
        "added_task_ids": selection["added_task_ids"],
        "outcome_access": "NONE",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    sanitization = {
        "schema_version": "orion.v2.e30-sanitization-summary.v1",
        "task_count": len(sanitization_records),
        "records": sanitization_records,
        "public_forbidden_path_audit": "PASS",
        "gold_or_fixed_content_read": False,
    }
    write_json(output_root / "frozen_tasks.json", frozen)
    write_json(output_root / "PRIVATE_EVALUATOR_REGISTRY.json", private_registry)
    write_json(output_root / "RUN_IDENTITY.json", identity)
    write_json(output_root / "SANITIZATION_RECEIPT.json", sanitization)
    custody = {
        "schema_version": "orion.v2.e30-input-custody.v1",
        "status": "PASS",
        "task_count": len(frozen_tasks),
        "public_file_count": public_file_count,
        "public_manifest_sha256": sha256(manifest_path),
        "frozen_tasks_sha256": sha256(output_root / "frozen_tasks.json"),
        "private_registry_sha256": sha256(output_root / "PRIVATE_EVALUATOR_REGISTRY.json"),
        "run_identity_sha256": sha256(output_root / "RUN_IDENTITY.json"),
        "sanitization_receipt_sha256": sha256(output_root / "SANITIZATION_RECEIPT.json"),
        "preparer_sha256": script_sha,
        "task_correction_sha256": correction_sha,
        "private_and_solver_public_trees_separate": True,
        "gold_or_fixed_content_read": False,
        "arm_outcomes_accessed": False,
        "scientific_truth_authorized": False,
        "field_status_authorized": False,
        "publication_readiness_authorized": False,
    }
    write_json(output_root / "INPUT_CUSTODY.json", custody)
    return custody


def discover_and_correct(repository: Path, correction: dict[str, Any]) -> dict[str, Any]:
    projects = tuple(correction["projects_in_frozen_order"])
    per_project = int(correction["original_bugs_per_project"])
    available: dict[str, list[int]] = {}
    original: list[dict[str, Any]] = []
    for project in projects:
        bugs = repository / "projects" / project / "bugs"
        ids = sorted(
            int(child.name)
            for child in bugs.iterdir()
            if child.is_dir() and child.name.isdigit() and (child / "bug.info").is_file()
        )
        available[project] = ids
        for bug_id in ids[:per_project]:
            original.append(
                {
                    "task_id": f"bugsinpy-{project}-{bug_id}",
                    "benchmark_id": "bugsinpy",
                    "adapter": "bugsinpy",
                    "project": project,
                    "bug_id": bug_id,
                    "buggy_version": 0,
                    "gold_withheld": True,
                }
            )

    tasks = list(original)
    observed_counts = {project: min(per_project, len(available[project])) for project in projects}
    expected_counts = {
        str(project): int(count)
        for project, count in correction["observed_project_counts"].items()
    }
    if observed_counts != expected_counts:
        raise PreparationError("original project counts disagree with frozen correction")
    selected = {(item["project"], item["bug_id"]) for item in tasks}
    required = int(correction["required_task_count"])
    for project in projects:
        for bug_id in available[project]:
            if len(tasks) >= required:
                break
            if (project, bug_id) in selected:
                continue
            tasks.append(
                {
                    "task_id": f"bugsinpy-{project}-{bug_id}",
                    "benchmark_id": "bugsinpy",
                    "adapter": "bugsinpy",
                    "project": project,
                    "bug_id": bug_id,
                    "buggy_version": 0,
                    "gold_withheld": True,
                }
            )
            selected.add((project, bug_id))
        if len(tasks) >= required:
            break

    added = [item["task_id"] for item in tasks[len(original) :]]
    expected_added = list(correction["added_task_ids"])
    if len(original) != int(correction["original_discovered_task_count"]):
        raise PreparationError("original task count disagrees with frozen correction")
    if len(tasks) != required or added != expected_added:
        raise PreparationError("deterministic deficit correction did not match the frozen identity")
    return {
        "schema_version": "orion.v2.e30-corrected-task-selection.v1",
        "bugsinpy_commit": correction["bugsinpy_commit"],
        "original_task_count": len(original),
        "corrected_task_count": len(tasks),
        "added_task_ids": added,
        "tasks": tasks,
        "outcome_access": "NONE",
        "gold_or_fixed_content_accessed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bugsinpy-repo", type=Path, required=True)
    parser.add_argument("--private-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--correction", type=Path, required=True)
    parser.add_argument("--orion-source-sha", required=True)
    parser.add_argument("--observed-bugsinpy-commit", required=True)
    parser.add_argument("--run-id")
    args = parser.parse_args(argv)
    try:
        result = prepare(
            repository=args.bugsinpy_repo,
            private_root=args.private_root,
            output_root=args.output_root,
            correction_path=args.correction,
            orion_source_sha=args.orion_source_sha,
            observed_bugsinpy_commit=args.observed_bugsinpy_commit,
            run_id=args.run_id,
        )
    except (PreparationError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
