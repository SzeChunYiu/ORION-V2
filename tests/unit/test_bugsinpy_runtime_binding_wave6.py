from __future__ import annotations

from scripts.bugsinpy_runtime import compile_environment
from scripts.bootstrap_bugsinpy_environment import wrapper_text


def test_compile_environment_binds_project_python_before_existing_path() -> None:
    environment = compile_environment(
        project_python_bin="/opt/python38/bin",
        compiler_compat_cflags="",
        base_environment={"PATH": "/usr/bin"},
    )
    assert environment["PATH"] == "/opt/python38/bin:/usr/bin"


def test_compile_environment_records_narrow_compatibility_flags() -> None:
    environment = compile_environment(
        project_python_bin="",
        compiler_compat_cflags="-Wno-error=array-bounds",
        base_environment={"PATH": "/usr/bin", "CFLAGS": "-O2"},
    )
    assert environment["CFLAGS"] == "-O2 -Wno-error=array-bounds"


def test_framework_wrapper_does_not_shadow_declared_project_python(tmp_path) -> None:
    text = wrapper_text(
        tmp_path / "BugsInPy",
        tmp_path / "framework-venv",
        tmp_path / "BugsInPy/framework/bin/bugsinpy-compile",
    )
    assert 'export PATH="$PATH":' in text
    assert "export PATH='" not in text
