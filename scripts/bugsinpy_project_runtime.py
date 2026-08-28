#!/usr/bin/env python3
"""Fail-closed E30 runtime bindings for the eight frozen BugsInPy projects.

This module does not checkout BugsInPy versions and never opens bug.info,
fixed commits, or gold patch files.  It operates only on an already-frozen
buggy workspace and its gold-blind BugsInPy runtime files.
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "research/experiments/BUGSINPY_E30_RUNTIME_REGISTRY_V1.json"
EXPECTED_PROJECTS = frozenset(
    {"ansible", "black", "cookiecutter", "fastapi", "pandas", "scrapy", "tornado", "tqdm"}
)
FORBIDDEN_VCS_PREFIXES = ("git+", "hg+", "svn+", "bzr+")


class RuntimeBindingError(RuntimeError):
    """The runtime registry or frozen workspace is not safely executable."""


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeBindingError(f"expected JSON object: {path}")
    return value


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    registry = _read_json(path)
    errors = validate_registry(registry)
    if errors:
        raise RuntimeBindingError("; ".join(errors))
    return registry


def validate_registry(registry: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != "orion.v2.bugsinpy-e30-runtime-registry.v1":
        errors.append("unexpected schema_version")
    projects = registry.get("projects")
    if not isinstance(projects, dict) or set(projects) != EXPECTED_PROJECTS:
        errors.append("registry must bind exactly the eight frozen projects")
        projects = {}
    compile_binding = registry.get("compile_binding")
    if not isinstance(compile_binding, dict):
        errors.append("compile_binding must be an object")
    elif compile_binding.get("native_extension_count_assumption") != "NONE":
        errors.append("project runtime must not assume a native-extension count")
    for project, binding in projects.items():
        if not isinstance(binding, dict):
            errors.append(f"{project}: binding must be an object")
            continue
        registered = binding.get("registered_failing_test")
        if not isinstance(registered, list) or not registered or not all(isinstance(x, str) and x for x in registered):
            errors.append(f"{project}: registered failing-test command is not bound")
        full = binding.get("full_regression")
        state = binding.get("full_regression_status")
        if full is None:
            if state != "CANNOT_CHECK_NOT_BOUND" or not str(binding.get("full_regression_reason", "")).strip():
                errors.append(f"{project}: unbound full regression needs an explicit CANNOT_CHECK reason")
        elif not isinstance(full, list) or not full or state != "BOUND":
            errors.append(f"{project}: malformed full-regression binding")
        if not isinstance(binding.get("import_module"), str) or not binding["import_module"]:
            errors.append(f"{project}: import_module is not bound")
    authority = registry.get("authority", {})
    if any(value is True for value in authority.values()):
        errors.append("runtime registry cannot grant authority or gold access")
    return errors


def _capture(command: Sequence[str], *, cwd: Path, env: Mapping[str, str], timeout: int) -> dict[str, Any]:
    try:
        result = subprocess.run(list(command), cwd=str(cwd), env=dict(env), text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout, check=False)
        return {"command": list(command), "returncode": result.returncode,
                "stdout_tail": result.stdout[-4000:], "stderr_tail": result.stderr[-4000:],
                "timed_out": False}
    except subprocess.TimeoutExpired as exc:
        return {"command": list(command), "returncode": 124,
                "stdout_tail": str(exc.stdout or "")[-4000:],
                "stderr_tail": str(exc.stderr or "")[-4000:], "timed_out": True}


def _requirement_kind(requirement: str, project: str) -> str:
    lowered = requirement.casefold()
    vcs = any(prefix in lowered for prefix in FORBIDDEN_VCS_PREFIXES)
    if not vcs:
        return "INSTALL"
    egg_match = f"#egg={project.casefold()}"
    normalized_project = project.casefold().replace("-", "_")
    if egg_match in lowered or f"#egg={normalized_project}" in lowered:
        return "SKIP_REDUNDANT_SELF_EDITABLE"
    return "FORBIDDEN_VCS"


def _rewrite_setup_command(line: str, environment_python: Path) -> list[str]:
    tokens = shlex.split(line)
    if not tokens:
        raise RuntimeBindingError("empty setup command")
    if any(token in {";", "&&", "||", "|", ">", ">>", "<"} for token in tokens):
        raise RuntimeBindingError("shell operators are not allowed in setup bindings")
    executable = Path(tokens[0]).name
    if executable in {"python", "python3", "python3.8"}:
        tokens[0] = str(environment_python)
    elif executable in {"pip", "pip3"}:
        tokens = [str(environment_python), "-m", "pip", *tokens[1:]]
    return tokens


def compile_workspace(
    workspace: Path,
    *,
    project: str,
    project_python: Path,
    compiler_compat_cflags: str = "",
    registry_path: Path = DEFAULT_REGISTRY,
    receipt_path: Path | None = None,
    timeout_seconds: int = 7200,
) -> dict[str, Any]:
    """Install requirements and run declared setup line-by-line, failing closed."""
    registry = load_registry(registry_path)
    binding = registry["projects"][project]
    workspace = workspace.resolve()
    receipt: dict[str, Any] = {
        "schema_version": "orion.v2.bugsinpy-project-compile.v1",
        "project": project, "status": "IN_PROGRESS", "workspace": str(workspace),
        "gold_or_fixed_solution_accessed": False,
        "native_extension_count_assumption": "NONE",
        "requirement_returncodes": [], "setup_returncodes": [],
    }

    def finish(status: str, stage: str) -> dict[str, Any]:
        receipt["status"] = status
        receipt["terminal_stage"] = stage
        if receipt_path:
            _write_json(receipt_path, receipt)
        return receipt

    required = registry["compile_binding"]["required_workspace_files"]
    missing = [name for name in required if not (workspace / name).is_file()]
    if missing:
        receipt["missing_files"] = missing
        return finish("CANNOT_CHECK_MISSING_RUNTIME_FILES", "preflight")
    if not project_python.is_file():
        return finish("CANNOT_CHECK_PROJECT_PYTHON_MISSING", "preflight")
    base_env = os.environ.copy()
    if compiler_compat_cflags:
        base_env["CFLAGS"] = " ".join(x for x in (base_env.get("CFLAGS", ""), compiler_compat_cflags) if x)
    python_probe = _capture([str(project_python), "--version"], cwd=workspace, env=base_env, timeout=60)
    compiler = shutil.which("gcc", path=base_env.get("PATH")) or shutil.which("cc", path=base_env.get("PATH"))
    compiler_probe = (_capture([compiler, "--version"], cwd=workspace, env=base_env, timeout=60)
                      if compiler else {"command": [], "returncode": 127, "stdout_tail": "", "stderr_tail": "compiler not found", "timed_out": False})
    receipt["python_version"] = python_probe
    receipt["compiler_version"] = compiler_probe
    if python_probe["returncode"] != 0 or compiler_probe["returncode"] != 0:
        return finish("CANNOT_CHECK_TOOLCHAIN_PREFLIGHT", "preflight")

    environment_dir = workspace / ".orion-e30-env"
    if environment_dir.exists():
        shutil.rmtree(environment_dir)
    created = _capture([str(project_python), "-m", "venv", str(environment_dir)], cwd=workspace, env=base_env, timeout=600)
    receipt["venv_returncode"] = created["returncode"]
    if created["returncode"] != 0:
        return finish("CANNOT_CHECK_VENV_CREATION", "create_environment")
    environment_python = environment_dir / "bin/python"
    env = base_env.copy()
    env["VIRTUAL_ENV"] = str(environment_dir)
    env["PATH"] = str(environment_dir / "bin") + os.pathsep + env.get("PATH", "")

    for raw in (workspace / "bugsinpy_requirements.txt").read_text(encoding="utf-8").splitlines():
        requirement = raw.strip()
        if not requirement or requirement.startswith("#"):
            continue
        digest = hashlib.sha256(requirement.encode("utf-8")).hexdigest()
        kind = _requirement_kind(requirement, project)
        if kind == "FORBIDDEN_VCS":
            receipt["requirement_returncodes"].append({"sha256": digest, "status": kind, "returncode": None})
            return finish("CANNOT_CHECK_FORBIDDEN_VCS_REQUIREMENT", "install_requirements")
        if kind == "SKIP_REDUNDANT_SELF_EDITABLE":
            receipt["requirement_returncodes"].append({"sha256": digest, "status": kind, "returncode": None})
            continue
        installed = _capture([str(environment_python), "-m", "pip", "install", "--disable-pip-version-check", requirement],
                             cwd=workspace, env=env, timeout=timeout_seconds)
        receipt["requirement_returncodes"].append({"sha256": digest, "status": "INSTALL", "returncode": installed["returncode"], "stderr_tail": installed["stderr_tail"]})
        if installed["returncode"] != 0:
            return finish("CANNOT_CHECK_REQUIREMENT_INSTALL_FAILED", "install_requirements")

    setup_path = workspace / "bugsinpy_setup.sh"
    setup_lines = setup_path.read_text(encoding="utf-8").splitlines() if setup_path.is_file() else []
    receipt["declared_setup_present"] = setup_path.is_file()
    for raw in setup_lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            command = _rewrite_setup_command(line, environment_python)
        except (ValueError, RuntimeBindingError) as exc:
            receipt["setup_binding_error"] = str(exc)
            return finish("CANNOT_CHECK_UNSAFE_SETUP_COMMAND", "declared_setup")
        executed = _capture(command, cwd=workspace, env=env, timeout=timeout_seconds)
        receipt["setup_returncodes"].append({"command": command, "returncode": executed["returncode"], "stderr_tail": executed["stderr_tail"]})
        if executed["returncode"] != 0:
            return finish("FAIL_DECLARED_COMPILE", "declared_setup")

    imported = _capture([str(environment_python), "-c", f"import {binding['import_module']} as m; print(getattr(m, '__file__', ''))"],
                        cwd=workspace, env=env, timeout=300)
    receipt["import_returncode"] = imported["returncode"]
    receipt["import_stdout_tail"] = imported["stdout_tail"]
    receipt["import_stderr_tail"] = imported["stderr_tail"]
    if imported["returncode"] != 0:
        return finish("FAIL_PROJECT_IMPORT", "import_gate")
    receipt["environment_python"] = str(environment_python)
    return finish("PASS", "complete")


def execute_test_binding(
    workspace: Path,
    *,
    project: str,
    environment_python: Path,
    stage: str,
    registry_path: Path = DEFAULT_REGISTRY,
    timeout_seconds: int = 7200,
) -> dict[str, Any]:
    """Execute the registered failing test or honestly bound full regression."""
    if stage not in {"registered_failing_test", "full_regression"}:
        raise RuntimeBindingError(f"unsupported stage: {stage}")
    binding = load_registry(registry_path)["projects"][project]
    command = binding[stage]
    base = {
        "schema_version": "orion.v2.bugsinpy-project-test.v1",
        "project": project, "stage": stage,
        "gold_or_fixed_solution_accessed": False,
        "python_version": _capture([str(environment_python), "--version"], cwd=workspace, env=os.environ, timeout=60),
    }
    compiler = shutil.which("gcc") or shutil.which("cc")
    base["compiler_version"] = (_capture([compiler, "--version"], cwd=workspace, env=os.environ, timeout=60)
                                if compiler else {"returncode": 127, "stderr_tail": "compiler not found"})
    if command is None:
        base.update({"status": "CANNOT_CHECK_NOT_BOUND", "returncode": None,
                     "reason": binding["full_regression_reason"]})
        return base
    rendered = [str(environment_python) if token == "{python}" else token for token in command]
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(environment_python.parent.parent)
    env["PATH"] = str(environment_python.parent) + os.pathsep + env.get("PATH", "")
    result = _capture(rendered, cwd=workspace, env=env, timeout=timeout_seconds)
    base.update({"status": "PASS" if result["returncode"] == 0 else "FAIL",
                 "returncode": result["returncode"], "command": rendered,
                 "stdout_tail": result["stdout_tail"], "stderr_tail": result["stderr_tail"],
                 "timed_out": result["timed_out"]})
    return base
