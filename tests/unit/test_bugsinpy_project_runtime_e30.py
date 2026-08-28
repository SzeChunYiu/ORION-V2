from __future__ import annotations

import codecs
import hashlib
import importlib.util
import json
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


def offline_cache(tmp_path: Path, filename: str = "pytest-8.0-py3-none-any.whl"):
    cache = tmp_path / "offline-cache"
    cache.mkdir()
    artifact = cache / filename
    artifact.write_bytes(b"frozen distribution bytes")
    manifest = cache / "manifest.json"
    manifest.write_text(json.dumps({
        "schema_version": runtime.OFFLINE_CACHE_SCHEMA,
        "artifacts": [{
            "filename": artifact.name,
            "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        }],
    }), encoding="utf-8")
    return cache, manifest


FROZEN_LINUX = {
    "python_version": "3.8.3",
    "python_implementation": "CPython",
    "sys_platform": "linux",
    "platform_system": "Linux",
    "platform_machine": "x86_64",
}


def write_binding(tmp_path: Path, project: str, **updates):
    value = {
        "schema_version": runtime.PROSPECTIVE_BINDING_SCHEMA,
        "project": project,
        "dependency_pins": {},
        "requirement_dispositions": {},
        "marker_decisions": {},
        "legacy_build": {},
        "distribution_overrides": {},
        "distribution_override_prerequisites": {},
    }
    value.update(updates)
    path = tmp_path / f"{project}-prospective-binding.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def prepare_workspace(tmp_path: Path, requirements: str) -> Path:
    (tmp_path / "bugsinpy_requirements.txt").write_text(requirements, encoding="utf-8")
    (tmp_path / "bugsinpy_run_test.sh").write_text("pytest -q\n", encoding="utf-8")
    python = tmp_path / "python3"
    python.write_text("", encoding="utf-8")
    return python


def successful_capture(command, **kwargs):
    if "platform.python_version" in " ".join(command):
        stdout = json.dumps(FROZEN_LINUX) + "\n"
    elif "show" in command:
        package = command[-1]
        stdout = f"Name: {package}\nVersion: 1.0\n"
    else:
        stdout = "ok"
    return {"command": list(command), "returncode": 0, "stdout_tail": stdout,
            "stderr_tail": "", "timed_out": False}


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
    cache, manifest = offline_cache(tmp_path)

    def fake_capture(command, **kwargs):
        commands.append(list(command))
        stdout = "Name: pytest\nVersion: 8.0\n" if "show" in command else "ok"
        return {"command": list(command), "returncode": 0, "stdout_tail": stdout, "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", fake_capture)
    receipt = runtime.compile_workspace(
        tmp_path, project="fastapi", project_python=project_python,
        offline_cache=cache, offline_cache_manifest=manifest,
    )
    assert receipt["status"] == "PASS"
    assert receipt["declared_setup_present"] is False
    assert receipt["native_extension_count_assumption"] == "NONE"
    assert receipt["requirement_returncodes"][0]["status"] == "SKIP_REDUNDANT_SELF_EDITABLE"
    assert not any(any("git+" in token for token in command) for command in commands)
    install = next(command for command in commands if "install" in command)
    assert "--no-index" in install
    assert "--no-deps" in install
    assert "--no-build-isolation" in install
    assert receipt["dependencies"] == [{
        "extras": [], "installed_name": "pytest", "installed_version": "8.0",
        "marker_present": False, "name": "pytest", "requested_version": "8.0",
        "requirement_sha256": hashlib.sha256(b"pytest==8.0").hexdigest(),
        "version_source": "FROZEN_REQUIREMENTS",
    }]


def test_support_decoder_is_bom_aware_and_refuses_arbitrary_binary(tmp_path: Path) -> None:
    requirements = tmp_path / "bugsinpy_requirements.txt"
    requirements.write_bytes(codecs.BOM_UTF8 + b"pytest==8.0\n")
    text, receipt = runtime._read_support_text(requirements)
    assert text == "pytest==8.0\n"
    assert receipt["encoding"] == "utf-8-sig"

    setup = tmp_path / "bugsinpy_setup.sh"
    setup.write_bytes(codecs.BOM_UTF16_LE + "python setup.py build\n".encode("utf-16-le"))
    text, receipt = runtime._read_support_text(setup)
    assert text == "python setup.py build\n"
    assert receipt["encoding"] == "utf-16-le"

    test_script = tmp_path / "bugsinpy_run_test.sh"
    test_script.write_bytes(codecs.BOM_UTF16_BE + "pytest -q\n".encode("utf-16-be"))
    text, receipt = runtime._read_support_text(test_script)
    assert text == "pytest -q\n"
    assert receipt["encoding"] == "utf-16-be"

    binary = tmp_path / "payload.bin"
    binary.write_bytes(b"\xff\xfe\x00\x00")
    try:
        runtime._read_support_text(binary)
    except runtime.RuntimeBindingError as exc:
        assert "non-support file" in str(exc)
    else:
        raise AssertionError("arbitrary binary was decoded")


def test_compile_fails_closed_without_explicit_hashed_cache(tmp_path: Path) -> None:
    (tmp_path / "bugsinpy_requirements.txt").write_text("pytest==8.0\n", encoding="utf-8")
    (tmp_path / "bugsinpy_run_test.sh").write_text("pytest -q\n", encoding="utf-8")
    python = tmp_path / "python3"
    python.write_text("", encoding="utf-8")
    receipt = runtime.compile_workspace(tmp_path, project="fastapi", project_python=python)
    assert receipt["status"] == "CANNOT_CHECK_OFFLINE_CACHE_NOT_BOUND"
    assert receipt["terminal_stage"] == "preflight"


def test_historical_distribution_unavailable_is_not_upgraded(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / "bugsinpy_requirements.txt").write_text(
        "ansible-base==2.10.0.dev0\n", encoding="utf-8"
    )
    (tmp_path / "bugsinpy_run_test.sh").write_text("pytest -q\n", encoding="utf-8")
    python = tmp_path / "python3"
    python.write_text("", encoding="utf-8")
    cache, manifest = offline_cache(tmp_path, "unrelated-1.0-py3-none-any.whl")
    commands = []

    def fake_capture(command, **kwargs):
        commands.append(list(command))
        if "install" in command:
            return {"command": list(command), "returncode": 1, "stdout_tail": "",
                    "stderr_tail": "No matching distribution found for ansible-base==2.10.0.dev0",
                    "timed_out": False}
        return {"command": list(command), "returncode": 0, "stdout_tail": "ok",
                "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", fake_capture)
    receipt = runtime.compile_workspace(
        tmp_path, project="ansible", project_python=python,
        offline_cache=cache, offline_cache_manifest=manifest,
    )
    assert receipt["status"] == "CANNOT_CHECK_HISTORICAL_DISTRIBUTION_UNAVAILABLE"
    install = next(command for command in commands if "install" in command)
    assert install[-1] == "ansible-base==2.10.0.dev0"
    assert "--no-index" in install
    assert "--upgrade" not in install


def test_legacy_compatibility_requires_project_binding(tmp_path: Path) -> None:
    (tmp_path / "bugsinpy_requirements.txt").write_text("# none\n", encoding="utf-8")
    (tmp_path / "bugsinpy_run_test.sh").write_text("pytest -q\n", encoding="utf-8")
    python = tmp_path / "python3"
    python.write_text("", encoding="utf-8")
    receipt = runtime.compile_workspace(
        tmp_path, project="tornado", project_python=python,
        compiler_compat_cflags="-Wno-error=implicit-function-declaration",
    )
    assert receipt["status"] == "CANNOT_CHECK_UNBOUND_LEGACY_COMPATIBILITY"
    assert "-Wno-error=implicit-function-declaration" not in json.dumps(receipt)


def test_project_binding_receipts_legacy_setup_rewrite(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / "bugsinpy_requirements.txt").write_text("# none\n", encoding="utf-8")
    setup_line = "python setup.py build"
    (tmp_path / "bugsinpy_setup.sh").write_text(setup_line + "\n", encoding="utf-8")
    (tmp_path / "bugsinpy_run_test.sh").write_text("pytest -q\n", encoding="utf-8")
    python = tmp_path / "python3"
    python.write_text("", encoding="utf-8")
    binding = tmp_path / "tornado-prospective-binding.json"
    binding.write_text(json.dumps({
        "schema_version": runtime.PROSPECTIVE_BINDING_SCHEMA,
        "project": "tornado",
        "dependency_pins": {},
        "requirement_dispositions": {},
        "marker_decisions": {},
        "legacy_build": {
            "compiler_compat_cflags": "-Wno-error=implicit-function-declaration",
            "setup_command_rewrites": {
                hashlib.sha256(setup_line.encode("utf-8")).hexdigest(): [
                    "{python}", "setup.py", "build_ext", "--inplace",
                ],
            },
        },
    }), encoding="utf-8")

    def fake_capture(command, **kwargs):
        return {"command": list(command), "returncode": 0, "stdout_tail": "ok",
                "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", fake_capture)
    receipt = runtime.compile_workspace(
        tmp_path, project="tornado", project_python=python,
        compiler_compat_cflags="-Wno-error=implicit-function-declaration",
        prospective_binding_path=binding,
    )
    assert receipt["status"] == "PASS"
    assert receipt["prospective_binding"]["sha256"] == hashlib.sha256(
        binding.read_bytes()
    ).hexdigest()
    assert [item["kind"] for item in receipt["compatibility_interventions"]] == [
        "BOUND_COMPILER_CFLAGS", "BOUND_SETUP_COMMAND_REWRITE",
    ]
    assert receipt["setup_returncodes"][0]["command"] == [
        str(tmp_path / ".orion-e30-env/bin/python"),
        "setup.py", "build_ext", "--inplace",
    ]


def test_known_self_and_placeholder_dispositions_are_hash_bound(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(runtime, "_capture", successful_capture)
    cases = [
        ("ansible", "ansible-base==2.10.0.dev0",
         "SKIP_REDUNDANT_SELF_DISTRIBUTION", "FROZEN_WORKSPACE_PROVIDES_DISTRIBUTION"),
        ("cookiecutter", "pkg-resources==0.0.0",
         "SKIP_NON_DISTRIBUTION_PLACEHOLDER", "FROZEN_EXPORT_PLACEHOLDER_NOT_DISTRIBUTION"),
    ]
    for project, requirement, action, reason in cases:
        workspace = tmp_path / project
        workspace.mkdir()
        python = prepare_workspace(workspace, requirement + "\n")
        digest = hashlib.sha256(requirement.encode("utf-8")).hexdigest()
        name, version = requirement.split("==")
        binding = write_binding(workspace, project, requirement_dispositions={
            digest: {"name": name, "version": version, "action": action, "reason": reason},
        })
        receipt = runtime.compile_workspace(
            workspace, project=project, project_python=python,
            prospective_binding_path=binding,
        )
        assert receipt["status"] == "PASS"
        assert receipt["requirement_returncodes"][0]["status"] == action
        assert receipt["requirement_decisions"][0]["binding_sha256"] == hashlib.sha256(
            binding.read_bytes()
        ).hexdigest()
        assert "offline_cache" not in receipt


def test_pywin32_227_platform_disposition_is_linux_only(
    tmp_path: Path, monkeypatch
) -> None:
    requirement = "pywin32==227"
    python = prepare_workspace(tmp_path, requirement + "\n")
    digest = hashlib.sha256(requirement.encode("utf-8")).hexdigest()
    binding = write_binding(tmp_path, "fastapi", requirement_dispositions={
        digest: {
            "name": "pywin32", "version": "227",
            "action": "SKIP_PLATFORM_INAPPLICABLE",
            "reason": "FROZEN_PLATFORM_EXCLUDES_DISTRIBUTION",
            "environment": FROZEN_LINUX,
        },
    })
    monkeypatch.setattr(runtime, "_capture", successful_capture)
    receipt = runtime.compile_workspace(
        tmp_path, project="fastapi", project_python=python,
        prospective_binding_path=binding,
    )
    assert receipt["status"] == "PASS"
    assert receipt["requirement_returncodes"][0]["status"] == "SKIP_PLATFORM_INAPPLICABLE"
    assert receipt["requirement_decisions"][0]["frozen_environment"] == FROZEN_LINUX

    hostile = json.loads(binding.read_text(encoding="utf-8"))
    hostile["requirement_dispositions"][digest]["environment"] = {
        **FROZEN_LINUX, "sys_platform": "win32", "platform_system": "Windows",
    }
    binding.write_text(json.dumps(hostile), encoding="utf-8")
    rejected = runtime.compile_workspace(
        tmp_path, project="fastapi", project_python=python,
        prospective_binding_path=binding,
    )
    assert rejected["status"] == "CANNOT_CHECK_PROSPECTIVE_BINDING_INVALID"


def test_marker_include_and_skip_are_frozen_environment_bound(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(runtime, "_capture", successful_capture)
    for decision in ("INCLUDE", "SKIP"):
        workspace = tmp_path / decision.casefold()
        workspace.mkdir()
        requirement = "typing-extensions==1.0; python_version < '3.9'"
        python = prepare_workspace(workspace, requirement + "\n")
        digest = hashlib.sha256(requirement.encode("utf-8")).hexdigest()
        binding = write_binding(workspace, "fastapi", marker_decisions={
            digest: {
                "name": "typing-extensions", "version": "1.0",
                "decision": decision, "reason": runtime.MARKER_REASONS[decision],
                "environment": FROZEN_LINUX,
            },
        })
        kwargs = {}
        if decision == "INCLUDE":
            cache, manifest = offline_cache(
                workspace, "typing_extensions-1.0-py3-none-any.whl"
            )
            kwargs = {"offline_cache": cache, "offline_cache_manifest": manifest}
        receipt = runtime.compile_workspace(
            workspace, project="fastapi", project_python=python,
            prospective_binding_path=binding, **kwargs,
        )
        assert receipt["status"] == "PASS"
        assert receipt["requirement_decisions"][0]["decision"] == f"MARKER_{decision}"
        assert receipt["requirement_decisions"][0]["frozen_environment"] == FROZEN_LINUX
        if decision == "SKIP":
            assert receipt["requirement_returncodes"][0]["status"] == "SKIP_MARKER_FALSE"
            assert "offline_cache" not in receipt
        else:
            assert receipt["dependencies"][0]["installed_version"] == "1.0"


def test_unbound_marker_and_hostile_dispositions_fail_closed(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(runtime, "_capture", successful_capture)
    marker = "typing-extensions==1.0; python_version < '3.9'"
    python = prepare_workspace(tmp_path, marker + "\n")
    unbound = runtime.compile_workspace(tmp_path, project="fastapi", project_python=python)
    assert unbound["status"] == "CANNOT_CHECK_MARKER_DECISION_NOT_BOUND"

    requirement = "ansible-base==2.10.0.dev0"
    (tmp_path / "bugsinpy_requirements.txt").write_text(requirement + "\n", encoding="utf-8")
    digest = hashlib.sha256(requirement.encode("utf-8")).hexdigest()
    for mutation in (
        {"name": "ansible-base", "version": "2.10.0.dev0", "action": "SKIP_ARBITRARY",
         "reason": "FROZEN_WORKSPACE_PROVIDES_DISTRIBUTION"},
        {"name": "ansible-base", "version": "9.9", "action": "SKIP_REDUNDANT_SELF_DISTRIBUTION",
         "reason": "FROZEN_WORKSPACE_PROVIDES_DISTRIBUTION"},
        {"name": "donor", "version": "2.10.0.dev0", "action": "SKIP_REDUNDANT_SELF_DISTRIBUTION",
         "reason": "FROZEN_WORKSPACE_PROVIDES_DISTRIBUTION"},
    ):
        binding = write_binding(tmp_path, "ansible", requirement_dispositions={digest: mutation})
        rejected = runtime.compile_workspace(
            tmp_path, project="ansible", project_python=python,
            prospective_binding_path=binding,
        )
        assert rejected["status"] == "CANNOT_CHECK_PROSPECTIVE_BINDING_INVALID"

    valid_disposition = {
        "name": "ansible-base", "version": "2.10.0.dev0",
        "action": "SKIP_REDUNDANT_SELF_DISTRIBUTION",
        "reason": "FROZEN_WORKSPACE_PROVIDES_DISTRIBUTION",
    }
    wrong_hash = "0" * 64 if digest != "0" * 64 else "1" * 64
    binding = write_binding(
        tmp_path, "ansible", requirement_dispositions={wrong_hash: valid_disposition}
    )
    rejected = runtime.compile_workspace(
        tmp_path, project="ansible", project_python=python,
        prospective_binding_path=binding,
    )
    assert rejected["status"] == "CANNOT_CHECK_PROSPECTIVE_BINDING_MISMATCH"


def test_bound_distribution_override_installs_exact_artifact(
    tmp_path: Path, monkeypatch
) -> None:
    requirement = "cryptography==2.9.2"
    python = prepare_workspace(tmp_path, requirement + "\n")
    digest = hashlib.sha256(requirement.encode("utf-8")).hexdigest()
    cache, manifest = offline_cache(tmp_path, "cryptography-2.9.2.tar.gz")
    commands = []

    def fake_capture(command, **kwargs):
        commands.append(list(command))
        stdout = "Name: cryptography\nVersion: 2.9.2\n" if "show" in command else "ok"
        return {"command": list(command), "returncode": 0, "stdout_tail": stdout,
                "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", fake_capture)
    binding = write_binding(
        tmp_path, "ansible",
        requirement_dispositions={},
        distribution_overrides={digest: "cryptography-2.9.2.tar.gz"},
    )
    receipt = runtime.compile_workspace(
        tmp_path, project="ansible", project_python=python,
        offline_cache=cache, offline_cache_manifest=manifest,
        prospective_binding_path=binding,
    )
    assert receipt["status"] == "PASS"
    install = next(command for command in commands if "install" in command)
    assert str(cache / "cryptography-2.9.2.tar.gz") in install
    assert "--find-links" not in install
    assert receipt["requirement_returncodes"][0]["status"] == "INSTALL_OFFLINE_BOUND_ARTIFACT"


def test_bound_distribution_override_installs_with_prerequisites(
    tmp_path: Path, monkeypatch
) -> None:
    requirements = "cryptography==2.9.2\npycparser==2.20\n"
    python = prepare_workspace(tmp_path, requirements)
    crypto_digest = hashlib.sha256(b"cryptography==2.9.2").hexdigest()
    cache, manifest = offline_cache(tmp_path, "cryptography-2.9.2.tar.gz")
    (cache / "pycparser-2.20-py2.py3-none-any.whl").write_bytes(b"pycparser")
    manifest.write_text(json.dumps({
        "schema_version": runtime.OFFLINE_CACHE_SCHEMA,
        "artifacts": [
            {"filename": "cryptography-2.9.2.tar.gz",
             "sha256": hashlib.sha256((cache / "cryptography-2.9.2.tar.gz").read_bytes()).hexdigest()},
            {"filename": "pycparser-2.20-py2.py3-none-any.whl",
             "sha256": hashlib.sha256((cache / "pycparser-2.20-py2.py3-none-any.whl").read_bytes()).hexdigest()},
        ],
    }), encoding="utf-8")
    commands = []

    def fake_capture(command, **kwargs):
        commands.append(list(command))
        stdout = "Name: cryptography\nVersion: 2.9.2\n" if "show" in command else "ok"
        if "pycparser" in " ".join(command) and "show" in command:
            stdout = "Name: pycparser\nVersion: 2.20\n"
        return {"command": list(command), "returncode": 0, "stdout_tail": stdout,
                "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", fake_capture)
    binding = write_binding(
        tmp_path, "ansible",
        distribution_overrides={crypto_digest: "cryptography-2.9.2.tar.gz"},
        distribution_override_prerequisites={crypto_digest: ["pycparser==2.20"]},
    )
    receipt = runtime.compile_workspace(
        tmp_path, project="ansible", project_python=python,
        offline_cache=cache, offline_cache_manifest=manifest,
        prospective_binding_path=binding,
    )
    assert receipt["status"] == "PASS"
    assert any("pycparser==2.20" in " ".join(command) for command in commands)


def test_utf16_test_support_is_normalized_before_execution(
    tmp_path: Path, monkeypatch
) -> None:
    script = tmp_path / "bugsinpy_run_test.sh"
    script.write_bytes(codecs.BOM_UTF16_LE + "pytest -q\n".encode("utf-16-le"))
    python = tmp_path / "env/bin/python"
    python.parent.mkdir(parents=True)
    python.write_text("", encoding="utf-8")

    def fake_capture(command, **kwargs):
        return {"command": list(command), "returncode": 0, "stdout_tail": "ok",
                "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", fake_capture)
    receipt = runtime.execute_test_binding(
        tmp_path, project="fastapi", environment_python=python,
        stage="registered_failing_test",
    )
    assert receipt["status"] == "PASS"
    normalized = tmp_path / ".orion-e30-support/bugsinpy_run_test.sh"
    assert normalized.read_text(encoding="utf-8") == "pytest -q\n"
    assert receipt["command"] == ["bash", str(normalized)]
    assert receipt["support_files"][0]["normalized_sha256"] == hashlib.sha256(
        normalized.read_bytes()
    ).hexdigest()


def test_bound_setup_dependency_install_and_rewrite(tmp_path: Path, monkeypatch) -> None:
    setup_line = "pip install Pillow"
    (tmp_path / "bugsinpy_requirements.txt").write_text("# none\n", encoding="utf-8")
    (tmp_path / "bugsinpy_setup.sh").write_text(setup_line + "\n", encoding="utf-8")
    (tmp_path / "bugsinpy_run_test.sh").write_text("pytest -q\n", encoding="utf-8")
    python = tmp_path / "python3"
    python.write_text("", encoding="utf-8")
    line_digest = hashlib.sha256(setup_line.encode("utf-8")).hexdigest()
    cache, manifest = offline_cache(tmp_path, "Pillow-7.2.0-cp38-cp38-manylinux1_x86_64.whl")
    binding = write_binding(
        tmp_path,
        "scrapy",
        legacy_build={
            "setup_dependency_installs": {line_digest: "Pillow==7.2.0"},
            "setup_command_rewrites": {
                line_digest: ["{python}", "-c", "from PIL import Image"],
            },
        },
    )

    def capture(command, **kwargs):
        if "show" in command and command[-1] == "pillow":
            stdout = "Name: Pillow\nVersion: 7.2.0\n"
        else:
            stdout = successful_capture(command, **kwargs)["stdout_tail"]
        return {"command": list(command), "returncode": 0, "stdout_tail": stdout,
                "stderr_tail": "", "timed_out": False}

    monkeypatch.setattr(runtime, "_capture", capture)
    receipt = runtime.compile_workspace(
        tmp_path,
        project="scrapy",
        project_python=python,
        offline_cache=cache,
        offline_cache_manifest=manifest,
        prospective_binding_path=binding,
    )
    assert receipt["status"] == "PASS"
    assert receipt["setup_dependency_returncodes"][0]["pinned_requirement"] == "Pillow==7.2.0"
    assert any(item["kind"] == "BOUND_SETUP_DEPENDENCY_INSTALL"
               for item in receipt["compatibility_interventions"])


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
