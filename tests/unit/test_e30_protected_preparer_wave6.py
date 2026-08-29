from __future__ import annotations

import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "prepare_e30_protected_workspaces.py"
CORRECTION = ROOT / "research" / "experiments" / "E30_TASK_DEFICIT_CORRECTION_V1.json"


def load_preparer():
    assert SCRIPT.is_file(), "protected E30 preparer is not implemented"
    spec = importlib.util.spec_from_file_location("orion_e30_preparer", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fake_bugsinpy(repo: Path) -> None:
    counts = {
        "ansible": 6,
        "black": 5,
        "cookiecutter": 4,
        "fastapi": 5,
        "pandas": 5,
        "scrapy": 5,
        "tornado": 5,
        "tqdm": 5,
    }
    for project, count in counts.items():
        for bug_id in range(1, count + 1):
            marker = repo / "projects" / project / "bugs" / str(bug_id) / "bug.info"
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text("contents must never be read\n", encoding="utf-8")


def test_frozen_deficit_correction_retains_39_and_adds_ansible_6(tmp_path: Path) -> None:
    preparer = load_preparer()
    fake_bugsinpy(tmp_path)
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))

    selection = preparer.discover_and_correct(tmp_path, correction)

    assert selection["original_task_count"] == 39
    assert selection["corrected_task_count"] == 40
    assert selection["added_task_ids"] == ["bugsinpy-ansible-6"]
    task_ids = [task["task_id"] for task in selection["tasks"]]
    assert len(task_ids) == len(set(task_ids)) == 40
    assert "bugsinpy-cookiecutter-5" not in task_ids


def test_correction_rejects_project_count_drift_even_when_total_stays_39(
    tmp_path: Path,
) -> None:
    preparer = load_preparer()
    fake_bugsinpy(tmp_path)
    (tmp_path / "projects" / "black" / "bugs" / "5" / "bug.info").unlink()
    replacement = tmp_path / "projects" / "cookiecutter" / "bugs" / "5" / "bug.info"
    replacement.parent.mkdir(parents=True)
    replacement.write_text("contents must never be read\n", encoding="utf-8")
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))

    with pytest.raises(preparer.PreparationError, match="project counts"):
        preparer.discover_and_correct(tmp_path, correction)


def test_solver_copy_excludes_private_metadata_build_artifacts_and_symlinks(
    tmp_path: Path,
) -> None:
    preparer = load_preparer()
    private = tmp_path / "private"
    public = tmp_path / "public"
    (private / "package").mkdir(parents=True)
    (private / "package" / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    forbidden_files = (
        private / ".git" / "config",
        private / "env" / "installed.txt",
        private / "build" / "artifact.o",
        private / "bug.info",
        private / "bugsinpy_bug.info",
        private / "bugsinpy_patchfile.info",
        private / "gold.patch",
        private / "fixed.patch",
        private / "solution.patch",
        private / "package" / "module.so",
        private / "package" / "module.o",
        private / "package" / "module.pyc",
        private / "bugsinpy_compile_flag",
    )
    for path in forbidden_files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("must not be read or copied\n", encoding="utf-8")
    os.symlink(private / "package" / "module.py", private / "source-link.py")

    receipt = preparer.sanitize_workspace(private, public)

    assert (public / "package" / "module.py").read_text() == "VALUE = 1\n"
    assert sorted(path.relative_to(public).as_posix() for path in public.rglob("*")) == [
        "package",
        "package/module.py",
    ]
    assert receipt["copied_file_count"] == 1
    assert receipt["excluded_symlink_count"] == 1
    assert receipt["excluded_forbidden_count"] == len(forbidden_files)
    preparer.audit_public_workspace(public)


@pytest.mark.parametrize(
    "relative",
    (
        ".git/config",
        "env/bin/python",
        "build/module.o",
        "bug.info",
        "bugsinpy_bug.info",
        "bugsinpy_patchfile.info",
        "nested/GOLD.PATCH",
        "nested/my-fixed-output.patch",
        "nested/solution.patch",
        "nested/fixed.patch.sha256",
    ),
)
def test_public_workspace_audit_rejects_every_forbidden_path(
    tmp_path: Path, relative: str
) -> None:
    preparer = load_preparer()
    path = tmp_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("forbidden\n", encoding="utf-8")

    with pytest.raises(preparer.PreparationError, match="forbidden path"):
        preparer.audit_public_workspace(tmp_path)


def test_prepare_emits_separate_private_registry_public_manifest_and_custody(
    tmp_path: Path,
) -> None:
    preparer = load_preparer()
    repository = tmp_path / "BugsInPy"
    fake_bugsinpy(repository)
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
    selection = preparer.discover_and_correct(repository, correction)
    private_root = tmp_path / "evaluator-private"
    for task in selection["tasks"]:
        workspace = private_root / task["task_id"]
        workspace.mkdir(parents=True)
        (workspace / "source.py").write_text(
            f'TASK = "{task["task_id"]}"\n', encoding="utf-8"
        )
        (workspace / "bug.info").write_text(
            "fixed content must not be read\n", encoding="utf-8"
        )
    output = tmp_path / "prepared"
    source_sha = "647aa306260f978e0570b71016b153e9ac48d6a0"

    result = preparer.prepare(
        repository=repository,
        private_root=private_root,
        output_root=output,
        correction_path=CORRECTION,
        orion_source_sha=source_sha,
        observed_bugsinpy_commit=correction["bugsinpy_commit"],
    )

    frozen = json.loads((output / "frozen_tasks.json").read_text())
    private = json.loads((output / "PRIVATE_EVALUATOR_REGISTRY.json").read_text())
    identity = json.loads((output / "RUN_IDENTITY.json").read_text())
    custody = json.loads((output / "INPUT_CUSTODY.json").read_text())
    manifest = output / "PUBLIC_WORKSPACES_MANIFEST.sha256"
    assert result["status"] == "PASS"
    assert len(frozen["tasks"]) == len(private["records"]) == 40
    assert all("evaluator_private_workspace" not in task for task in frozen["tasks"])
    assert all(
        Path(task["solver_workspace"]).is_relative_to(output / "solver_public")
        for task in frozen["tasks"]
    )
    assert all(
        Path(record["evaluator_private_workspace"]).is_relative_to(private_root)
        for record in private["records"]
    )
    assert identity["orion_source_sha"] == source_sha
    assert identity["corrected_task_count"] == 40
    assert identity["added_task_ids"] == ["bugsinpy-ansible-6"]
    assert custody["gold_or_fixed_content_read"] is False
    assert custody["public_manifest_sha256"] == hashlib.sha256(
        manifest.read_bytes()
    ).hexdigest()
    assert len(manifest.read_text().splitlines()) == 40
    assert not list((output / "solver_public").rglob("bug.info"))


def test_cli_materializes_the_frozen_protected_surface(tmp_path: Path) -> None:
    preparer = load_preparer()
    repository = tmp_path / "BugsInPy"
    fake_bugsinpy(repository)
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
    selection = preparer.discover_and_correct(repository, correction)
    private_root = tmp_path / "private"
    for task in selection["tasks"]:
        workspace = private_root / task["task_id"]
        workspace.mkdir(parents=True)
        (workspace / "source.py").write_text("VALUE = 1\n", encoding="utf-8")
    output = tmp_path / "output"

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--bugsinpy-repo",
            str(repository),
            "--private-root",
            str(private_root),
            "--output-root",
            str(output),
            "--correction",
            str(CORRECTION),
            "--orion-source-sha",
            "647aa306260f978e0570b71016b153e9ac48d6a0",
            "--observed-bugsinpy-commit",
            correction["bugsinpy_commit"],
            "--run-id",
            "e45-e30-test",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["status"] == "PASS"
    assert (output / "RUN_IDENTITY.json").is_file()
