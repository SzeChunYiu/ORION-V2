from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime = load("bugsinpy_project_runtime_e30", "scripts/bugsinpy_project_runtime.py")
runner = load("real_problem_runner_e30", "scripts/run_orion_real_problem_suite.py")


def test_registry_binds_exact_eight_projects_without_pandas_extension_assumption() -> None:
    registry = runtime.load_registry()
    assert set(registry["projects"]) == runtime.EXPECTED_PROJECTS
    assert registry["compile_binding"]["native_extension_count_assumption"] == "NONE"
    assert "bugsinpy_setup.sh" not in registry["compile_binding"]["required_workspace_files"]
    assert registry["compile_binding"]["declared_setup_policy"].startswith("RUN_IF_PRESENT")
    assert runtime.validate_registry(registry) == []
    for binding in registry["projects"].values():
        assert binding["registered_failing_test"] == ["bash", "bugsinpy_run_test.sh"]


def test_full_regression_is_explicitly_bound_or_cannot_check() -> None:
    projects = runtime.load_registry()["projects"]
    assert projects["ansible"]["full_regression"] is None
    assert projects["ansible"]["full_regression_status"] == "CANNOT_CHECK_NOT_BOUND"
    for project, binding in projects.items():
        if project != "ansible":
            assert binding["full_regression_status"] == "BOUND"
            assert binding["full_regression"]


def test_vcs_requirements_are_never_retrieved_as_fixed_content() -> None:
    assert runtime._requirement_kind(
        "-e git+https://github.com/pandas-dev/pandas@fixed#egg=pandas", "pandas"
    ) == "SKIP_REDUNDANT_SELF_EDITABLE"
    assert runtime._requirement_kind(
        "git+https://example.invalid/donor@fixed#egg=donor", "pandas"
    ) == "FORBIDDEN_VCS"
    assert runtime._requirement_kind("pytest==8.0", "pandas") == "INSTALL"


def test_compile_is_fail_closed_without_requiring_project_specific_extensions(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / "bugsinpy_requirements.txt").write_text(
        "-e git+https://github.com/tiangolo/fastapi@fixed#egg=fastapi\npytest==8.0\n",
        encoding="utf-8",
    )
    (tmp_path / "bugsinpy_run_test.sh").write_text("pytest tests/test_a.py\n", encoding="utf-8")
    project_python = tmp_path / "python3"
    project_python.write_text("", encoding="utf-8")
    commands = []

    def fake_capture(command, **kwargs):
        commands.append(list(command))
        return {"command": list(command), "returncode": 0, "stdout_tail": "ok", "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", fake_capture)
    receipt = runtime.compile_workspace(
        tmp_path, project="fastapi", project_python=project_python
    )
    assert receipt["status"] == "PASS"
    assert receipt["declared_setup_present"] is False
    assert receipt["native_extension_count_assumption"] == "NONE"
    assert receipt["requirement_returncodes"][0]["status"] == "SKIP_REDUNDANT_SELF_EDITABLE"
    assert not any(any("git+" in token for token in command) for command in commands)


def test_unbound_full_regression_records_toolchain_and_cannot_check(
    tmp_path: Path, monkeypatch
) -> None:
    python = tmp_path / "env/bin/python"
    python.parent.mkdir(parents=True)
    python.write_text("", encoding="utf-8")
    calls = []

    def fake_capture(command, **kwargs):
        calls.append(command)
        return {"command": list(command), "returncode": 0, "stdout_tail": "version", "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", fake_capture)
    receipt = runtime.execute_test_binding(
        tmp_path, project="ansible", environment_python=python, stage="full_regression"
    )
    assert receipt["status"] == "CANNOT_CHECK_NOT_BOUND"
    assert receipt["returncode"] is None
    assert receipt["python_version"]["returncode"] == 0
    assert "compiler_version" in receipt
    assert calls


def test_native_success_return_has_boolean_authority_flags_not_name_error(
    tmp_path: Path, monkeypatch
) -> None:
    completed = subprocess.CompletedProcess(["stub"], 0, "", "")
    monkeypatch.setattr(runner, "_benchmark_record", lambda frozen, benchmark: {"repository_path": str(tmp_path), "venv_path": str(tmp_path)})
    monkeypatch.setattr(runner, "_bugsinpy_binary", lambda record, name: name)
    monkeypatch.setattr(runner, "compile_environment", lambda **kwargs: {})
    results = iter([completed, completed, completed])
    monkeypatch.setattr(runner, "_run", lambda *args, **kwargs: next(results))
    monkeypatch.setattr(runner.subprocess, "run", lambda *args, **kwargs: completed)
    result = runner._evaluate_bugsinpy(
        {"benchmarks": []}, tmp_path,
        {"task_id": "bugsinpy-pandas-1", "benchmark_id": "bugsinpy", "project": "pandas", "bug_id": 1, "buggy_version": 0},
        {"status": "COMPLETED_PROPOSAL_ONLY", "proposed_patch_or_artifact": {"type": "unified_diff", "content": "diff --git a/a b/a\n"}},
        "SIMPLE_DIRECT", timeout_seconds=1,
    )
    assert result["native_success"] is True
    assert result["scientific_truth_authorized"] is False
    assert result["field_status_authorized"] is False
