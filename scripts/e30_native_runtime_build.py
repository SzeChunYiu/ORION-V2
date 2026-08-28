#!/usr/bin/env python3
"""Build one exact CPython runtime natively on a LUNARC compute node."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import time
from datetime import datetime, timezone
from pathlib import Path

SPECS = (
    {"version": "3.6.9", "source": "Python-3.6.9.tar.xz", "source_sha256": "5e2f5f554e3f8f7f0296f7e73d8600c4e9acbaee6b2555b83206edf5153870da", "get_pip": "get-pip-3.6.py", "get_pip_sha256": "7e2d052458c1802dc0a9a97b98ffcc33c5e89cc203247f8e2d5451998f012092"},
    {"version": "3.7.0", "source": "Python-3.7.0.tar.xz", "source_sha256": "0382996d1ee6aafe59763426cf0139ffebe36984474d0ec4126dd1c40a8b3549", "get_pip": "get-pip-3.7.py", "get_pip_sha256": "5b9e2f9bb476ce76f84942bb7247dec8d6c0bb9dbc8c62ba2543b81fd7a4243c"},
    {"version": "3.8.3", "source": "Python-3.8.3.tar.xz", "source_sha256": "dfab5ec723c218082fe3d5d7ae17ecbdebffa9a1aea4d64aa3a2ecdd2e795864", "get_pip": "get-pip-3.8.py", "get_pip_sha256": "6ed6e98282a504ee0a6632856e16c39f222d313fc38be33de216d4afb6ac12f7"},
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def run(command: list[str], *, cwd: Path, env: dict[str, str], log: Path, timeout: int) -> int:
    with log.open("wb") as stream:
        result = subprocess.run(command, cwd=str(cwd), env=env, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=timeout, check=False)
    return result.returncode


def capture(command: list[str], *, cwd: Path, env: dict[str, str], timeout: int = 300) -> dict[str, object]:
    result = subprocess.run(command, cwd=str(cwd), env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=timeout, check=False)
    return {"command": command, "returncode": result.returncode,
            "stdout": result.stdout[-4000:], "stderr": result.stderr[-4000:]}


def safe_extract(archive: Path, destination: Path) -> None:
    root = destination.resolve()
    with tarfile.open(archive, "r:xz") as bundle:
        for member in bundle.getmembers():
            if not (root / member.name).resolve().is_relative_to(root):
                raise RuntimeError(f"unsafe source archive member: {member.name}")
        bundle.extractall(destination)


def write_tree_manifest(root: Path, destination: Path) -> tuple[int, str]:
    records = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            records.append(f"SYMLINK {os.readlink(path)}  {relative}\n")
        elif path.is_file():
            records.append(f"{sha(path)}  {relative}\n")
    destination.write_text("".join(records), encoding="utf-8")
    return len(records), sha(destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--index", type=int, required=True)
    args = parser.parse_args()
    spec = SPECS[args.index]
    version = spec["version"]
    base = args.base.resolve()
    source_root = base / "e30-runtime-sources"
    runtime_root = base / "e30-exact-runtimes"
    receipt_root = base / "e30-runtime-receipts"
    log_root = base / "logs"
    prefix = runtime_root / f"cpython-{version}"
    receipt_path = receipt_root / f"cpython-{version}.json"
    manifest_path = receipt_root / f"cpython-{version}.manifest.sha256"
    job_id = os.environ.get("SLURM_ARRAY_JOB_ID", os.environ.get("SLURM_JOB_ID", "local"))
    work = base / "e30-runtime-build-work" / f"{job_id}_{args.index}_{version}"
    started = time.perf_counter()
    receipt = {
        "schema_version": "orion.v2.e30-native-runtime-build.v1",
        "version": version, "status": "IN_PROGRESS",
        "job_id": os.environ.get("SLURM_JOB_ID"), "array_job_id": os.environ.get("SLURM_ARRAY_JOB_ID"),
        "array_task_id": os.environ.get("SLURM_ARRAY_TASK_ID"),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "source_url": f"https://www.python.org/ftp/python/{version}/{spec['source']}",
        "source_sha256": spec["source_sha256"], "get_pip_sha256": spec["get_pip_sha256"],
        "prefix": str(prefix), "ensurepip_at_install": "no",
        "cflags": "-O2 -fPIC -fno-tree-slp-vectorize -fno-strict-aliasing -Wno-error=incompatible-pointer-types -Wno-error=implicit-function-declaration -Wno-error=int-conversion",
        "scientific_jobs_launched": False, "model_calls_launched": False,
    }

    def finish(status: str, reason: str = "") -> int:
        receipt.update({"status": status, "reason": reason,
                        "finished_at": datetime.now(timezone.utc).isoformat(),
                        "wall_time_seconds": time.perf_counter() - started})
        write_json(receipt_path, receipt)
        return 0 if status == "PASS" else 1

    try:
        if prefix.exists() or receipt_path.exists():
            return finish("CANNOT_CHECK_DUPLICATE_RUNTIME_STATE", "prefix or receipt already exists")
        runtime_root.mkdir(parents=True, exist_ok=True)
        receipt_root.mkdir(parents=True, exist_ok=True)
        log_root.mkdir(parents=True, exist_ok=True)
        work.mkdir(parents=True)
        source_archive = source_root / spec["source"]
        get_pip = source_root / spec["get_pip"]
        if sha(source_archive) != spec["source_sha256"] or sha(get_pip) != spec["get_pip_sha256"]:
            return finish("CANNOT_CHECK_SOURCE_HASH", "official source or get-pip hash mismatch")
        safe_extract(source_archive, work)
        source = work / f"Python-{version}"
        openssl_root = Path(os.environ.get("EBROOTOPENSSL", ""))
        if not (openssl_root / "include/openssl/ssl.h").is_file():
            return finish("CANNOT_CHECK_OPENSSL_MODULE", f"invalid EBROOTOPENSSL={openssl_root}")
        sqlite_root = Path(os.environ.get("EBROOTSQLITE", ""))
        if not (sqlite_root / "include/sqlite3.h").is_file():
            return finish("CANNOT_CHECK_SQLITE_MODULE", f"invalid EBROOTSQLITE={sqlite_root}")
        libdir = openssl_root / "lib"
        sqlite_libdir = sqlite_root / "lib"
        env = os.environ.copy()
        env["CFLAGS"] = receipt["cflags"]
        env["CPPFLAGS"] = f"-I{openssl_root / 'include'} -I{sqlite_root / 'include'}"
        env["LDFLAGS"] = (
            f"-L{libdir} -Wl,-rpath,{libdir} "
            f"-L{sqlite_libdir} -Wl,-rpath,{sqlite_libdir}"
        )
        receipt["sqlite_root"] = str(sqlite_root)
        sinpi_probe = capture(["bash", "-lc", "printf '#define _GNU_SOURCE 1\\n#include <math.h>\\n' | gcc -E -dD -x c - | grep -E '(^|[[:space:]])sinpi[[:space:]]*\\('"], cwd=source, env=env)
        receipt["sinpi_declaration_probe"] = sinpi_probe
        if sinpi_probe["returncode"] == 0 and version in {"3.6.9", "3.7.0"}:
            mathmodule = source / "Modules/mathmodule.c"
            text = mathmodule.read_text(encoding="utf-8")
            if text.count("sinpi") != 4:
                return finish("CANNOT_CHECK_SINPI_PATCH_PRECONDITION", "expected exactly four sinpi occurrences")
            before_sha = sha(mathmodule)
            mathmodule.write_text(text.replace("sinpi", "_orion_cpython_sinpi"), encoding="utf-8")
            receipt["sinpi_patch"] = {"status": "APPLIED_COMPILER_DECLARATION_CONFLICT", "before_sha256": before_sha,
                                      "after_sha256": sha(mathmodule), "replacement_count": 4}
        else:
            receipt["sinpi_patch"] = {"status": "NOT_REQUIRED_NO_COMPILER_DECLARATION"}
        configure = [str(source / "configure"), f"--prefix={prefix}", "--with-ensurepip=no"]
        if version != "3.6.9":
            configure.append(f"--with-openssl={openssl_root}")
        configure_log = log_root / f"e30-runtime-{version}-{job_id}-configure.log"
        make_log = log_root / f"e30-runtime-{version}-{job_id}-make.log"
        install_log = log_root / f"e30-runtime-{version}-{job_id}-install.log"
        rc = run(configure, cwd=source, env=env, log=configure_log, timeout=1800)
        receipt["configure"] = {"returncode": rc, "log": str(configure_log), "log_sha256": sha(configure_log)}
        if rc:
            return finish("CANNOT_CHECK_CONFIGURE_FAILED")
        rc = run(["make", "-j4"], cwd=source, env=env, log=make_log, timeout=7200)
        receipt["make"] = {"returncode": rc, "log": str(make_log), "log_sha256": sha(make_log)}
        if rc:
            return finish("CANNOT_CHECK_BUILD_FAILED")
        destroot = work / "destroot"
        destroot.mkdir()
        rc = run(["make", "altinstall", f"DESTDIR={destroot}"], cwd=source, env=env, log=install_log, timeout=3600)
        receipt["install"] = {"returncode": rc, "log": str(install_log), "log_sha256": sha(install_log)}
        if rc:
            return finish("CANNOT_CHECK_INSTALL_FAILED")
        staged_prefix = Path(str(destroot) + str(prefix))
        version_xy = ".".join(version.split(".")[:2])
        staged_python = staged_prefix / "bin" / f"python{version_xy}"
        if not staged_python.is_file():
            return finish("CANNOT_CHECK_INSTALLED_PYTHON_MISSING", str(staged_python))
        (staged_prefix / "bin/python3").symlink_to(staged_python.name)
        (staged_prefix / "bin/python").symlink_to(staged_python.name)
        staged_prefix.replace(prefix)
        python = prefix / "bin/python3"
        probes = {
            "version": capture([str(python), "--version"], cwd=prefix, env=env),
            "stdlib": capture(
                [str(python), "-c",
                 "import hashlib,math,sqlite3,ssl,venv; print(ssl.OPENSSL_VERSION); print(math.sin(0.5)); print(sqlite3.sqlite_version)"],
                cwd=prefix, env=env,
            ),
        }
        receipt["pre_bootstrap_probes"] = probes
        if probes["version"]["returncode"] or probes["version"]["stdout"].strip() != f"Python {version}" or probes["stdlib"]["returncode"]:
            return finish("CANNOT_CHECK_RUNTIME_SMOKE_FAILED")
        pip_log = log_root / f"e30-runtime-{version}-{job_id}-get-pip.log"
        rc = run([str(python), str(get_pip), "--disable-pip-version-check"], cwd=prefix, env=env, log=pip_log, timeout=1800)
        receipt["pip_bootstrap"] = {"returncode": rc, "log": str(pip_log), "log_sha256": sha(pip_log)}
        if rc:
            return finish("CANNOT_CHECK_PIP_BOOTSTRAP_FAILED")
        smoke_venv = work / "smoke-venv"
        venv_probe = capture([str(python), "-m", "venv", str(smoke_venv)], cwd=prefix, env=env, timeout=900)
        receipt["venv_creation_probe"] = venv_probe
        if venv_probe["returncode"]:
            return finish("CANNOT_CHECK_VENV_CREATION_FAILED")
        venv_python = smoke_venv / "bin/python"
        final_probes = {
            "runtime": capture(
                [str(python), "-c", "import hashlib,math,sqlite3,ssl,venv; print('PASS')"],
                cwd=prefix, env=env,
            ),
            "sqlite": capture([str(python), "-c", "import _sqlite3,sqlite3; print(sqlite3.sqlite_version)"],
                              cwd=prefix, env=env),
            "pip": capture([str(python), "-m", "pip", "--version"], cwd=prefix, env=env),
            "venv": capture([str(venv_python), "-c", "import ssl; print('PASS')"], cwd=smoke_venv, env=env),
            "venv_pip": capture([str(venv_python), "-m", "pip", "--version"], cwd=smoke_venv, env=env),
        }
        receipt["final_probes"] = final_probes
        if any(item["returncode"] for item in final_probes.values()):
            return finish("CANNOT_CHECK_FINAL_RUNTIME_PROBE_FAILED")
        count, manifest_sha = write_tree_manifest(prefix, manifest_path)
        receipt["runtime_manifest"] = {"path": str(manifest_path), "sha256": manifest_sha, "record_count": count}
        return finish("PASS")
    except Exception as exc:
        return finish("CANNOT_CHECK_RUNTIME_BUILDER_EXCEPTION", f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    raise SystemExit(main())
