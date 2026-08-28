#!/usr/bin/env python3
"""Fail-closed E30 runtime bindings for the eight frozen BugsInPy projects.

This module does not checkout BugsInPy versions and never opens bug.info,
fixed commits, or gold patch files.  It operates only on an already-frozen
buggy workspace and its gold-blind BugsInPy runtime files.
"""
from __future__ import annotations

import codecs
import hashlib
import json
import os
import re
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
SUPPORT_FILENAMES = frozenset(
    {"bugsinpy_requirements.txt", "bugsinpy_setup.sh", "bugsinpy_run_test.sh"}
)
MAX_SUPPORT_FILE_BYTES = 2 * 1024 * 1024
OFFLINE_CACHE_SCHEMA = "orion.v2.bugsinpy-offline-distribution-cache.v1"
PROSPECTIVE_BINDING_SCHEMA = "orion.v2.bugsinpy-prospective-runtime-binding.v1"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+!-]*$")
_CFLAG_RE = re.compile(r"^-[A-Za-z0-9_=,+./:-]+$")
_REQUIREMENT_RE = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)"
    r"(?P<extras>\[[A-Za-z0-9._,-]+\])?\s*(?P<tail>.*)$"
)


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


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_support_text(path: Path) -> tuple[str, dict[str, Any]]:
    """Decode only named BugsInPy support files using a deterministic BOM policy."""
    if path.name not in SUPPORT_FILENAMES:
        raise RuntimeBindingError(f"refusing to decode non-support file: {path.name}")
    if path.is_symlink() or not path.is_file():
        raise RuntimeBindingError(f"support file is missing or symlinked: {path.name}")
    payload = path.read_bytes()
    if len(payload) > MAX_SUPPORT_FILE_BYTES:
        raise RuntimeBindingError(f"support file exceeds {MAX_SUPPORT_FILE_BYTES} bytes: {path.name}")
    if payload.startswith(codecs.BOM_UTF8):
        encoding = "utf-8-sig"
    elif payload.startswith(codecs.BOM_UTF16_LE):
        encoding = "utf-16-le"
        payload = payload[len(codecs.BOM_UTF16_LE):]
    elif payload.startswith(codecs.BOM_UTF16_BE):
        encoding = "utf-16-be"
        payload = payload[len(codecs.BOM_UTF16_BE):]
    else:
        encoding = "utf-8"
    try:
        text = payload.decode(encoding)
    except UnicodeDecodeError as exc:
        raise RuntimeBindingError(f"unsupported support-file encoding for {path.name}") from exc
    if "\x00" in text:
        raise RuntimeBindingError(f"NUL character in support file: {path.name}")
    return text, {
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": _sha256_file(path),
        "encoding": encoding,
    }


def _canonical_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).casefold()


def _dependency_binding(requirement: str) -> dict[str, Any]:
    """Return a secret-free dependency identity; reject paths, URLs, and pip options."""
    if requirement.startswith("-") or " @ " in requirement or "://" in requirement:
        raise RuntimeBindingError("requirement is not a direct named distribution")
    body, marker_separator, _marker = requirement.partition(";")
    match = _REQUIREMENT_RE.fullmatch(body.strip())
    if not match:
        raise RuntimeBindingError("requirement cannot be safely identified")
    name = match.group("name")
    tail = match.group("tail").strip()
    version: str | None = None
    exact = re.fullmatch(r"==\s*([A-Za-z0-9][A-Za-z0-9._+!-]*)", tail)
    if exact:
        version = exact.group(1)
    elif tail:
        # Ranges and compatible-release selectors can silently select newer artifacts.
        raise RuntimeBindingError("requirement is not exactly version pinned")
    extras = match.group("extras") or ""
    return {
        "name": _canonical_name(name),
        "requested_version": version,
        "extras": sorted(
            _canonical_name(item) for item in extras.strip("[]").split(",") if item
        ),
        "marker_present": bool(marker_separator),
    }


def _load_offline_cache(cache: Path, manifest_path: Path) -> dict[str, Any]:
    if cache.is_symlink() or manifest_path.is_symlink():
        raise RuntimeBindingError("offline cache directory and manifest cannot be symlinks")
    cache = cache.resolve()
    manifest_path = manifest_path.resolve()
    if not cache.is_dir() or not manifest_path.is_file():
        raise RuntimeBindingError("offline cache directory or manifest is missing")
    manifest = _read_json(manifest_path)
    if manifest.get("schema_version") != OFFLINE_CACHE_SCHEMA:
        raise RuntimeBindingError("unexpected offline-cache schema_version")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise RuntimeBindingError("offline-cache manifest must contain artifacts")
    verified: list[dict[str, Any]] = []
    declared: set[str] = set()
    for entry in artifacts:
        if not isinstance(entry, dict):
            raise RuntimeBindingError("offline-cache artifact must be an object")
        filename, expected = entry.get("filename"), entry.get("sha256")
        if not isinstance(filename, str) or Path(filename).name != filename:
            raise RuntimeBindingError("offline-cache artifact filename must be a basename")
        if not isinstance(expected, str) or not _SHA256_RE.fullmatch(expected):
            raise RuntimeBindingError("offline-cache artifact needs a lowercase SHA-256")
        if filename in declared:
            raise RuntimeBindingError("duplicate offline-cache artifact")
        if not filename.casefold().endswith(
            (".whl", ".zip", ".tar.gz", ".tar.bz2", ".tar.xz", ".tgz")
        ):
            raise RuntimeBindingError("offline-cache artifact is not a wheel or sdist")
        artifact = cache / filename
        if artifact.is_symlink() or not artifact.is_file():
            raise RuntimeBindingError(f"offline-cache artifact is missing or symlinked: {filename}")
        actual = _sha256_file(artifact)
        if actual != expected:
            raise RuntimeBindingError(f"offline-cache hash mismatch: {filename}")
        declared.add(filename)
        verified.append({"filename": filename, "bytes": artifact.stat().st_size, "sha256": actual})
    actual_files = {
        item.name for item in cache.iterdir()
        if item.is_file() and item.resolve() != manifest_path
    }
    if actual_files != declared:
        raise RuntimeBindingError("offline cache contains unmanifested or missing regular files")
    return {
        "directory": str(cache),
        "manifest": str(manifest_path),
        "manifest_sha256": _sha256_file(manifest_path),
        "artifacts": sorted(verified, key=lambda item: item["filename"]),
    }


def _load_prospective_binding(path: Path, project: str) -> dict[str, Any]:
    binding = _read_json(path)
    if binding.get("schema_version") != PROSPECTIVE_BINDING_SCHEMA:
        raise RuntimeBindingError("unexpected prospective-binding schema_version")
    if binding.get("project") != project:
        raise RuntimeBindingError("prospective binding is not for this project")
    dependency_pins = binding.get("dependency_pins", {})
    if not isinstance(dependency_pins, dict):
        raise RuntimeBindingError("dependency_pins must be an object")
    for digest, pin in dependency_pins.items():
        if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
            raise RuntimeBindingError("dependency pin key must be a requirement SHA-256")
        if not isinstance(pin, dict) or not _NAME_RE.fullmatch(str(pin.get("name", ""))):
            raise RuntimeBindingError("dependency pin needs a safe distribution name")
        if not _VERSION_RE.fullmatch(str(pin.get("version", ""))):
            raise RuntimeBindingError("dependency pin needs an exact safe version")
    legacy = binding.get("legacy_build", {})
    if not isinstance(legacy, dict):
        raise RuntimeBindingError("legacy_build must be an object")
    flags = legacy.get("compiler_compat_cflags", "")
    if not isinstance(flags, str):
        raise RuntimeBindingError("unsafe compiler compatibility flags")
    try:
        flag_tokens = shlex.split(flags)
    except ValueError as exc:
        raise RuntimeBindingError("unsafe compiler compatibility flags") from exc
    if any(not _CFLAG_RE.fullmatch(token) for token in flag_tokens):
        raise RuntimeBindingError("unsafe compiler compatibility flags")
    rewrites = legacy.get("setup_command_rewrites", {})
    if not isinstance(rewrites, dict):
        raise RuntimeBindingError("setup_command_rewrites must be an object")
    for digest, command in rewrites.items():
        if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
            raise RuntimeBindingError("setup rewrite key must be a line SHA-256")
        if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
            raise RuntimeBindingError("setup rewrite must be a non-empty argv list")
        if any(token in {";", "&&", "||", "|", ">", ">>", "<"} for token in command):
            raise RuntimeBindingError("shell operators are not allowed in setup rewrites")
    binding["_receipt"] = {
        "path": str(path.resolve()),
        "sha256": _sha256_file(path),
        "project": project,
    }
    return binding


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
    if any(
        token in {"-U", "--upgrade", "--index-url", "--extra-index-url"}
        or "://" in token
        or any(prefix in token.casefold() for prefix in FORBIDDEN_VCS_PREFIXES)
        for token in tokens
    ):
        raise RuntimeBindingError("network and upgrade setup operations are not allowed")
    executable = Path(tokens[0]).name
    if executable in {"python", "python3", "python3.8"}:
        tokens[0] = str(environment_python)
    elif executable in {"pip", "pip3"}:
        tokens = [str(environment_python), "-m", "pip", *tokens[1:]]
    return tokens


def _render_bound_setup_command(command: Sequence[str], environment_python: Path,
                                offline_cache: Path | None) -> list[str]:
    replacements = {
        "{python}": str(environment_python),
        "{offline_cache}": str(offline_cache) if offline_cache else "",
    }
    rendered = [replacements.get(token, token) for token in command]
    if any(not token for token in rendered):
        raise RuntimeBindingError("setup rewrite requires an offline cache that is not bound")
    # Reuse the same argv safety policy without reparsing through a shell.
    if any(
        token in {";", "&&", "||", "|", ">", ">>", "<", "-U", "--upgrade",
                  "--index-url", "--extra-index-url"}
        or "://" in token
        or any(prefix in token.casefold() for prefix in FORBIDDEN_VCS_PREFIXES)
        for token in rendered
    ):
        raise RuntimeBindingError("unsafe prospective setup rewrite")
    if len(rendered) >= 4 and rendered[1:4] == ["-m", "pip", "install"]:
        raise RuntimeBindingError("setup rewrites cannot bypass the hashed dependency installer")
    return rendered


def _pip_show_identity(output: str) -> tuple[str, str] | None:
    fields: dict[str, str] = {}
    for line in output.splitlines():
        key, separator, value = line.partition(":")
        if separator and key in {"Name", "Version"}:
            fields[key] = value.strip()
    name, version = fields.get("Name", ""), fields.get("Version", "")
    if not _NAME_RE.fullmatch(name) or not _VERSION_RE.fullmatch(version):
        return None
    return _canonical_name(name), version


def compile_workspace(
    workspace: Path,
    *,
    project: str,
    project_python: Path,
    compiler_compat_cflags: str = "",
    offline_cache: Path | None = None,
    offline_cache_manifest: Path | None = None,
    prospective_binding_path: Path | None = None,
    registry_path: Path = DEFAULT_REGISTRY,
    receipt_path: Path | None = None,
    timeout_seconds: int = 7200,
) -> dict[str, Any]:
    """Install requirements and run declared setup line-by-line, failing closed."""
    registry = load_registry(registry_path)
    binding = registry["projects"][project]
    workspace = workspace.resolve()
    receipt: dict[str, Any] = {
        "schema_version": "orion.v2.bugsinpy-project-compile.v2",
        "project": project, "status": "IN_PROGRESS", "workspace": str(workspace),
        "gold_or_fixed_solution_accessed": False,
        "native_extension_count_assumption": "NONE",
        "requirement_returncodes": [], "setup_returncodes": [],
        "support_files": [], "dependencies": [], "compatibility_interventions": [],
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

    support_text: dict[str, str] = {}
    support_names = [*required]
    if (workspace / "bugsinpy_setup.sh").is_file():
        support_names.append("bugsinpy_setup.sh")
    try:
        for name in support_names:
            text, support_receipt = _read_support_text(workspace / name)
            support_text[name] = text
            receipt["support_files"].append(support_receipt)
    except (OSError, RuntimeBindingError) as exc:
        receipt["support_decode_error"] = str(exc)
        return finish("CANNOT_CHECK_SUPPORT_FILE_DECODE", "preflight")

    prospective: dict[str, Any] | None = None
    if prospective_binding_path is not None:
        try:
            prospective = _load_prospective_binding(prospective_binding_path, project)
        except (OSError, ValueError, RuntimeBindingError) as exc:
            receipt["prospective_binding_error"] = str(exc)
            return finish("CANNOT_CHECK_PROSPECTIVE_BINDING_INVALID", "preflight")
        receipt["prospective_binding"] = prospective["_receipt"]

    legacy = prospective.get("legacy_build", {}) if prospective else {}
    bound_cflags = str(legacy.get("compiler_compat_cflags", ""))
    if compiler_compat_cflags and compiler_compat_cflags != bound_cflags:
        receipt["unbound_compiler_compat_cflags_sha256"] = hashlib.sha256(
            compiler_compat_cflags.encode("utf-8")
        ).hexdigest()
        return finish("CANNOT_CHECK_UNBOUND_LEGACY_COMPATIBILITY", "preflight")
    compiler_compat_cflags = bound_cflags
    if compiler_compat_cflags:
        receipt["compatibility_interventions"].append({
            "kind": "BOUND_COMPILER_CFLAGS",
            "binding_sha256": prospective["_receipt"]["sha256"],
            "value_sha256": hashlib.sha256(compiler_compat_cflags.encode("utf-8")).hexdigest(),
        })

    requirement_lines = []
    for raw in support_text["bugsinpy_requirements.txt"].splitlines():
        requirement = raw.strip()
        if requirement and not requirement.startswith("#"):
            requirement_lines.append(requirement)
    needs_cache = any(_requirement_kind(line, project) == "INSTALL" for line in requirement_lines)
    cache_receipt: dict[str, Any] | None = None
    if needs_cache:
        if offline_cache is None or offline_cache_manifest is None:
            return finish("CANNOT_CHECK_OFFLINE_CACHE_NOT_BOUND", "preflight")
        try:
            cache_receipt = _load_offline_cache(offline_cache, offline_cache_manifest)
        except (OSError, ValueError, RuntimeBindingError) as exc:
            receipt["offline_cache_error"] = str(exc)
            return finish("CANNOT_CHECK_OFFLINE_CACHE_INVALID", "preflight")
        receipt["offline_cache"] = cache_receipt
    base_env = os.environ.copy()
    for key in ("CFLAGS", "CXXFLAGS", "PYTHONHOME", "PYTHONPATH"):
        inherited = base_env.pop(key, "")
        if inherited:
            receipt.setdefault("ignored_inherited_environment", {})[key] = hashlib.sha256(
                inherited.encode("utf-8")
            ).hexdigest()
    if compiler_compat_cflags:
        base_env["CFLAGS"] = compiler_compat_cflags
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
    env["PIP_NO_INDEX"] = "1"
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    env["PIP_CONFIG_FILE"] = os.devnull
    env["PIP_INDEX_URL"] = ""
    env["PIP_EXTRA_INDEX_URL"] = ""
    if offline_cache is not None:
        env["PIP_FIND_LINKS"] = str(offline_cache.resolve())
    pip_tmp = workspace / ".orion-e30-pip-tmp"
    pip_tmp.mkdir(parents=True, exist_ok=True)
    env["TMPDIR"] = str(pip_tmp)

    for requirement in requirement_lines:
        digest = hashlib.sha256(requirement.encode("utf-8")).hexdigest()
        kind = _requirement_kind(requirement, project)
        if kind == "FORBIDDEN_VCS":
            receipt["requirement_returncodes"].append({"sha256": digest, "status": kind, "returncode": None})
            return finish("CANNOT_CHECK_FORBIDDEN_VCS_REQUIREMENT", "install_requirements")
        if kind == "SKIP_REDUNDANT_SELF_EDITABLE":
            receipt["requirement_returncodes"].append({"sha256": digest, "status": kind, "returncode": None})
            continue
        try:
            dependency = _dependency_binding(requirement)
        except RuntimeBindingError as exc:
            receipt["requirement_returncodes"].append({
                "sha256": digest, "status": "UNSAFE_OR_UNPINNED", "returncode": None,
                "reason": str(exc),
            })
            return finish("CANNOT_CHECK_UNSAFE_OR_UNPINNED_REQUIREMENT", "install_requirements")
        if dependency["marker_present"]:
            receipt["dependencies"].append({**dependency, "requirement_sha256": digest})
            return finish("CANNOT_CHECK_REQUIREMENT_MARKER_UNSUPPORTED", "install_requirements")
        pin = prospective.get("dependency_pins", {}).get(digest) if prospective else None
        if dependency["requested_version"] is None:
            if not pin:
                receipt["dependencies"].append({**dependency, "requirement_sha256": digest})
                return finish("CANNOT_CHECK_UNPINNED_REQUIREMENT", "install_requirements")
            if _canonical_name(str(pin["name"])) != dependency["name"]:
                return finish("CANNOT_CHECK_PROSPECTIVE_BINDING_MISMATCH", "install_requirements")
            dependency["requested_version"] = str(pin["version"])
            dependency["version_source"] = "PROSPECTIVE_BINDING"
        else:
            dependency["version_source"] = "FROZEN_REQUIREMENTS"
            if pin and (
                _canonical_name(str(pin["name"])) != dependency["name"]
                or str(pin["version"]) != dependency["requested_version"]
            ):
                return finish("CANNOT_CHECK_PROSPECTIVE_BINDING_MISMATCH", "install_requirements")
        dependency["requirement_sha256"] = digest
        receipt["dependencies"].append(dependency)
        extras = f"[{','.join(dependency['extras'])}]" if dependency["extras"] else ""
        install_requirement = (
            f"{dependency['name']}{extras}=={dependency['requested_version']}"
        )
        installed = _capture([
            str(environment_python), "-m", "pip", "install",
            "--disable-pip-version-check", "--no-index", "--no-deps", "--no-cache-dir",
            "--no-build-isolation", "--find-links", str(offline_cache.resolve()),
            install_requirement,
        ],
                             cwd=workspace, env=env, timeout=timeout_seconds)
        receipt["requirement_returncodes"].append({
            "sha256": digest, "name": dependency["name"],
            "requested_version": dependency["requested_version"],
            "status": "INSTALL_OFFLINE_HASHED", "returncode": installed["returncode"],
            "stderr_tail": installed["stderr_tail"],
        })
        if installed["returncode"] != 0:
            combined = installed["stdout_tail"] + "\n" + installed["stderr_tail"]
            if ("No matching distribution found" in combined
                    or "Could not find a version that satisfies" in combined):
                return finish("CANNOT_CHECK_HISTORICAL_DISTRIBUTION_UNAVAILABLE", "install_requirements")
            return finish("CANNOT_CHECK_REQUIREMENT_INSTALL_FAILED", "install_requirements")
        shown = _capture(
            [str(environment_python), "-m", "pip", "show", dependency["name"]],
            cwd=workspace, env=env, timeout=300,
        )
        identity = _pip_show_identity(shown["stdout_tail"]) if shown["returncode"] == 0 else None
        if identity != (dependency["name"], dependency["requested_version"]):
            receipt["requirement_returncodes"][-1]["version_probe_returncode"] = shown["returncode"]
            return finish("CANNOT_CHECK_DEPENDENCY_VERSION_UNVERIFIED", "install_requirements")
        dependency["installed_name"] = identity[0]
        dependency["installed_version"] = identity[1]

    setup_path = workspace / "bugsinpy_setup.sh"
    setup_lines = support_text.get("bugsinpy_setup.sh", "").splitlines()
    receipt["declared_setup_present"] = setup_path.is_file()
    for raw in setup_lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line_digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
        try:
            rewrite = legacy.get("setup_command_rewrites", {}).get(line_digest)
            if rewrite:
                command = _render_bound_setup_command(rewrite, environment_python, offline_cache)
                receipt["compatibility_interventions"].append({
                    "kind": "BOUND_SETUP_COMMAND_REWRITE",
                    "source_sha256": line_digest,
                    "binding_sha256": prospective["_receipt"]["sha256"],
                    "rendered_argv_sha256": hashlib.sha256(
                        "\0".join(command).encode("utf-8")
                    ).hexdigest(),
                })
            else:
                command = _rewrite_setup_command(line, environment_python)
                if len(command) >= 4 and command[1:4] == ["-m", "pip", "install"]:
                    raise RuntimeBindingError("setup-time pip install requires a prospective binding")
        except (ValueError, RuntimeBindingError) as exc:
            receipt["setup_binding_error"] = str(exc)
            return finish("CANNOT_CHECK_UNBOUND_OR_UNSAFE_SETUP_COMMAND", "declared_setup")
        executed = _capture(command, cwd=workspace, env=env, timeout=timeout_seconds)
        receipt["setup_returncodes"].append({
            "command": command, "source_sha256": line_digest,
            "returncode": executed["returncode"], "stderr_tail": executed["stderr_tail"],
        })
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
        "schema_version": "orion.v2.bugsinpy-project-test.v2",
        "project": project, "stage": stage,
        "gold_or_fixed_solution_accessed": False,
        "python_version": _capture([str(environment_python), "--version"], cwd=workspace, env=os.environ, timeout=60),
        "support_files": [],
    }
    compiler = shutil.which("gcc") or shutil.which("cc")
    base["compiler_version"] = (_capture([compiler, "--version"], cwd=workspace, env=os.environ, timeout=60)
                                if compiler else {"returncode": 127, "stderr_tail": "compiler not found"})
    if command is None:
        base.update({"status": "CANNOT_CHECK_NOT_BOUND", "returncode": None,
                     "reason": binding["full_regression_reason"]})
        return base
    rendered = [str(environment_python) if token == "{python}" else token for token in command]
    for index, token in enumerate(rendered):
        if Path(token).name != "bugsinpy_run_test.sh":
            continue
        support_path = workspace / token
        try:
            support_text, support_receipt = _read_support_text(support_path)
        except (OSError, RuntimeBindingError) as exc:
            base.update({
                "status": "CANNOT_CHECK_SUPPORT_FILE_DECODE", "returncode": None,
                "support_decode_error": str(exc),
            })
            return base
        base["support_files"].append(support_receipt)
        if support_receipt["encoding"] != "utf-8":
            normalized_dir = workspace / ".orion-e30-support"
            normalized_dir.mkdir(parents=True, exist_ok=True)
            normalized = normalized_dir / "bugsinpy_run_test.sh"
            normalized.write_text(support_text, encoding="utf-8", newline="\n")
            rendered[index] = str(normalized)
            support_receipt["normalized_sha256"] = _sha256_file(normalized)
            support_receipt["normalized_path"] = str(normalized)
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(environment_python.parent.parent)
    env["PATH"] = str(environment_python.parent) + os.pathsep + env.get("PATH", "")
    result = _capture(rendered, cwd=workspace, env=env, timeout=timeout_seconds)
    base.update({"status": "PASS" if result["returncode"] == 0 else "FAIL",
                 "returncode": result["returncode"], "command": rendered,
                 "stdout_tail": result["stdout_tail"], "stderr_tail": result["stderr_tail"],
                 "timed_out": result["timed_out"]})
    return base
