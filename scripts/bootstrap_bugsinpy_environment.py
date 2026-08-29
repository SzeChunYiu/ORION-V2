#!/usr/bin/env python3
"""Bootstrap the pinned BugsInPy framework into the ORION work directory.

BugsInPy is framework-style rather than a conventional editable Python
package. This script creates a virtual environment, installs its declared
requirements when present, and writes wrappers for the native framework/bin
commands with BUGSINPY_HOME and PATH bound explicitly.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


class BootstrapError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BootstrapError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BootstrapError(f"expected JSON object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def run(command: list[str], *, timeout: int = 1800) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def venv_python(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def venv_bin(venv: Path) -> Path:
    return venv / ("Scripts" if os.name == "nt" else "bin")


def wrapper_text(repository: Path, venv: Path, source: Path) -> str:
    if os.name == "nt":
        return (
            "@echo off\r\n"
            f"set BUGSINPY_HOME={repository}\r\n"
            f"set PATH={venv_bin(venv)};%PATH%\r\n"
            f'"{source}" %*\r\n'
        )
    return (
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        f"export BUGSINPY_HOME={str(repository)!r}\n"
        f"export PATH=\"$PATH\":{str(venv_bin(venv))!r}\n"
        f"exec {str(source)!r} \"$@\"\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--skip-requirements", action="store_true")
    args = parser.parse_args(argv)

    frozen_path = args.workdir / "frozen_tasks.json"
    frozen = read_json(frozen_path)
    record = next(
        (
            item
            for item in frozen.get("benchmarks", [])
            if item.get("benchmark_id") == "bugsinpy"
        ),
        None,
    )
    if record is None:
        raise BootstrapError("BugsInPy is not present in frozen_tasks.json")

    repository = Path(record["repository_path"]).resolve()
    venv = Path(record["venv_path"]).resolve()
    framework_bin = repository / "framework" / "bin"
    if not framework_bin.is_dir():
        raise BootstrapError(f"BugsInPy framework/bin not found: {framework_bin}")

    python = venv_python(venv)
    if not python.exists():
        result = run([sys.executable, "-m", "venv", str(venv)], timeout=args.timeout_seconds)
        if result.returncode != 0:
            raise BootstrapError(result.stderr[-4000:])

    install_receipts: list[dict[str, Any]] = []
    if not args.skip_requirements:
        requirement_candidates = (
            repository / "requirements.txt",
            repository / "framework" / "requirements.txt",
        )
        for requirements in requirement_candidates:
            if not requirements.exists():
                continue
            result = run(
                [str(python), "-m", "pip", "install", "-r", str(requirements)],
                timeout=args.timeout_seconds,
            )
            install_receipts.append(
                {
                    "requirements": str(requirements),
                    "returncode": result.returncode,
                    "stdout_tail": result.stdout[-3000:],
                    "stderr_tail": result.stderr[-3000:],
                }
            )
            if result.returncode != 0:
                raise BootstrapError(
                    f"requirement installation failed for {requirements}: {result.stderr[-4000:]}"
                )

    required_commands = (
        "bugsinpy-checkout",
        "bugsinpy-compile",
        "bugsinpy-test",
    )
    wrappers: list[str] = []
    destination_bin = venv_bin(venv)
    destination_bin.mkdir(parents=True, exist_ok=True)
    for name in required_commands:
        source = framework_bin / name
        if not source.exists():
            raise BootstrapError(f"missing BugsInPy command: {source}")
        destination = destination_bin / (f"{name}.cmd" if os.name == "nt" else name)
        destination.write_text(wrapper_text(repository, venv, source), encoding="utf-8")
        if os.name != "nt":
            destination.chmod(
                destination.stat().st_mode
                | stat.S_IXUSR
                | stat.S_IXGRP
                | stat.S_IXOTH
            )
        wrappers.append(str(destination))

    record["installed"] = True
    record["bootstrap_method"] = "explicit_framework_wrappers"
    record["framework_bin_path"] = str(framework_bin)
    write_json(frozen_path, frozen)
    write_json(
        args.workdir / "baseline" / "bugsinpy_bootstrap.json",
        {
            "schema_version": "orion.v2.bugsinpy-bootstrap.v1",
            "repository": str(repository),
            "venv": str(venv),
            "wrappers": wrappers,
            "requirements": install_receipts,
            "gold_or_fixed_version_access": "NONE",
            "scientific_truth_authorized": False,
        },
    )
    print("BugsInPy environment bootstrapped")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BootstrapError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
