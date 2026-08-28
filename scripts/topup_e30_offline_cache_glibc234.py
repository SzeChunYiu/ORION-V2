#!/usr/bin/env python3
"""Top up an E30 offline cache with glibc-2.34-compatible distribution artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OFFLINE_CACHE_SCHEMA = "orion.v2.bugsinpy-offline-distribution-cache.v1"
PROSPECTIVE_BINDING_SCHEMA = "orion.v2.bugsinpy-prospective-runtime-binding.v2"
USER_AGENT = "ORION-V2-E30-offline-cache-glibc234/1.0"

GLIBC234_ARTIFACTS: list[tuple[str, str, str]] = [
    ("MarkupSafe", "2.0.0a1", "MarkupSafe-2.0.0a1-cp36-cp36m-manylinux1_x86_64.whl"),
    ("MarkupSafe", "1.1.1", "MarkupSafe-1.1.1-cp36-cp36m-manylinux1_x86_64.whl"),
    ("MarkupSafe", "1.1.1", "MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl"),
    ("pydantic", "1.5.1", "pydantic-1.5.1-py36.py37.py38-none-any.whl"),
    ("numba", "0.49.1", "numba-0.49.1-cp38-cp38-manylinux1_x86_64.whl"),
    ("Pillow", "7.2.0", "Pillow-7.2.0-cp38-cp38-manylinux1_x86_64.whl"),
    ("mitmproxy", "4.0.4", "mitmproxy-4.0.4-py3-none-any.whl"),
    ("utils", "1.0.2", "utils-1.0.2.tar.gz"),
    ("leveldb", "0.201", "leveldb-0.201.tar.gz"),
    ("python-gettext", "4.0", "python-gettext-4.0.tar.gz"),
    ("pytest", "3.10.1", "pytest-3.10.1-py2.py3-none-any.whl"),
    ("atomicwrites", "1.4.0", "atomicwrites-1.4.0-py2.py3-none-any.whl"),
    ("attrs", "19.3.0", "attrs-19.3.0-py2.py3-none-any.whl"),
    ("more-itertools", "8.2.0", "more_itertools-8.2.0-py3-none-any.whl"),
    ("ruamel.yaml.clib", "0.2.0", "ruamel.yaml.clib-0.2.0-cp36-cp36m-manylinux1_x86_64.whl"),
    ("ruamel.yaml", "0.16.10", "ruamel.yaml-0.16.10-py2.py3-none-any.whl"),
    ("pytest-mock", "1.2", "pytest_mock-1.2-py2.py3-none-any.whl"),
]

PROJECT_OVERRIDES: dict[str, dict[str, str]] = {
    "ansible": {
        "0bfa78e14835a081d8a922632aec64c366bd4c166d4e2e8b4c423a7d261b4b8f":
        "MarkupSafe-2.0.0a1-cp36-cp36m-manylinux1_x86_64.whl",
    },
    "cookiecutter": {
        "61d14fea3440c5a3a60d4895db475b46d5c86f02bd1f1972c5313d91c3ba2732":
        "MarkupSafe-1.1.1-cp36-cp36m-manylinux1_x86_64.whl",
    },
    "fastapi": {
        "61d14fea3440c5a3a60d4895db475b46d5c86f02bd1f1972c5313d91c3ba2732":
        "MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl",
        "ff13748779e9728032779f6bad27dcb4bb39678f99e552aae1da9cd00380f287":
        "pydantic-1.5.1-py36.py37.py38-none-any.whl",
    },
    "pandas": {
        "a6217a709f483acee4d0f064d98d787f90bc3882ef0fce57a5f47011625ddd20":
        "numba-0.49.1-cp38-cp38-manylinux1_x86_64.whl",
    },
}

SCRAPY_SETUP_INSTALLS = {
    "c9157bd219762507ec45e008186097faf478691291cfbcaf91c4667ce7270b57": "Pillow==7.2.0",
    "4a8c43c96099c60db7a6cc9a7f12a8036a5096b416c9842c4ae2fbbf1f550c84": "utils==1.0.2",
    "7b64d9b372615eeccc268c2f7532b3e86e157137cee341df6e49169cfd8ebe37": "mitmproxy==4.0.4",
    "305ef645319d8649c26e74c6b761b27de1c4d1ac2e5c4fce039fb926555daf11": "leveldb==0.201",
}
SCRAPY_SETUP_REWRITES = {
    "c9157bd219762507ec45e008186097faf478691291cfbcaf91c4667ce7270b57": [
        "{python}", "-c", "from PIL import Image",
    ],
    "4a8c43c96099c60db7a6cc9a7f12a8036a5096b416c9842c4ae2fbbf1f550c84": [
        "{python}", "-c", "import utils",
    ],
    "7b64d9b372615eeccc268c2f7532b3e86e157137cee341df6e49169cfd8ebe37": [
        "{python}", "-c",
        "import pkg_resources; pkg_resources.get_distribution('mitmproxy')",
    ],
    "305ef645319d8649c26e74c6b761b27de1c4d1ac2e5c4fce039fb926555daf11": [
        "{python}", "-c", "import leveldb",
    ],
}

TORNADO_SETUP_INSTALLS = {
    "5a0c356fd95ce0871fff4ba67d5fdbef663a6f59be937d04aaddbafe915aefb3":
    "python-gettext==4.0",
}
TORNADO_SETUP_REWRITES = {
    "5a0c356fd95ce0871fff4ba67d5fdbef663a6f59be937d04aaddbafe915aefb3": [
        "{python}", "-c",
        "import pkg_resources; pkg_resources.get_distribution('python-gettext')",
    ],
}

ANSIBLE_SETUP_INSTALLS = {
    "0adc45477b142c1ccb86fee954bd83132c427ec00cc2f67eebfbf7772fcd7eaf": "pytest==3.10.1",
    "cb4822b2e90266a105d8b10b41266dc43dea570c43d5e0465c712a36cb7ceace": "pytest-mock==1.2",
}
ANSIBLE_SETUP_PREREQUISITES = {
    "0adc45477b142c1ccb86fee954bd83132c427ec00cc2f67eebfbf7772fcd7eaf": [
        "atomicwrites==1.4.0",
        "attrs==19.3.0",
        "more-itertools==8.2.0",
        "pluggy==0.13.1",
        "py==1.8.1",
        "packaging==20.4",
    ],
    "cb4822b2e90266a105d8b10b41266dc43dea570c43d5e0465c712a36cb7ceace": [
        "pytest==3.10.1",
    ],
}
COOKIECUTTER_DEVELOP_DIGEST = "3d7b5491b985872ef7604a0c7730a7cd6a9a20371b3697e5dff279588c2324b3"
COOKIECUTTER_TEST_PREREQUISITES = [
    "attrs==19.3.0",
    "more-itertools==8.2.0",
    "pluggy==0.13.1",
    "py==1.8.1",
    "packaging==20.4",
    "pytest==5.4.2",
]
COOKIECUTTER_SETUP_COMMAND_PREREQUISITES = {
    COOKIECUTTER_DEVELOP_DIGEST: ["ruamel.yaml.clib==0.2.0", "ruamel.yaml==0.16.10"],
}
COOKIECUTTER_SETUP_REWRITES = {
    COOKIECUTTER_DEVELOP_DIGEST: ["{python}", "setup.py", "develop", "--no-deps"],
}
ANSIBLE_SETUP_REWRITES = {
    "653b7a51d65d7409e319e29d51d5ee2af65d621ad9ef62148e7eacf99e289879": [
        "{python}", "setup.py", "install",
    ],
    "0adc45477b142c1ccb86fee954bd83132c427ec00cc2f67eebfbf7772fcd7eaf": [
        "{python}", "-c", "import pytest",
    ],
    "cb4822b2e90266a105d8b10b41266dc43dea570c43d5e0465c712a36cb7ceace": [
        "{python}", "-c", "import pytest_mock",
    ],
}


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def fetch_bytes(url: str, *, attempts: int = 5, timeout: int = 600) -> bytes:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(
                url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except (OSError, urllib.error.URLError, TimeoutError) as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(1.0 * (2 ** attempt))
    assert last is not None
    raise last


def pypi_artifact_url(project: str, version: str, filename: str) -> str:
    metadata = json.loads(
        fetch_bytes(f"https://pypi.org/pypi/{project}/{version}/json").decode("utf-8")
    )
    for artifact in metadata.get("urls", []):
        if artifact.get("filename") == filename:
            return str(artifact["url"])
    raise RuntimeError(f"artifact not found on PyPI: {filename}")


def download_artifact(cache: Path, project: str, version: str, filename: str) -> dict[str, Any]:
    destination = cache / filename
    if destination.is_file():
        return {
            "filename": filename,
            "status": "PASS",
            "computed_sha256": sha_file(destination),
            "bytes": destination.stat().st_size,
            "reused_existing": True,
        }
    payload = fetch_bytes(pypi_artifact_url(project, version, filename))
    temporary = cache / f".{filename}.part"
    temporary.write_bytes(payload)
    computed = hashlib.sha256(payload).hexdigest()
    temporary.replace(destination)
    return {
        "filename": filename,
        "status": "PASS",
        "computed_sha256": computed,
        "bytes": len(payload),
        "reused_existing": False,
    }


def patch_binding(path: Path, project: str, source_sha: str) -> str:
    binding = json.loads(path.read_text(encoding="utf-8"))
    predecessor = sha_file(path)
    binding["schema_version"] = PROSPECTIVE_BINDING_SCHEMA
    binding["source_sha"] = source_sha
    binding["predecessor_binding_sha256"] = predecessor
    overrides = dict(binding.get("distribution_overrides") or {})
    overrides.update(PROJECT_OVERRIDES.get(project, {}))
    binding["distribution_overrides"] = overrides
    legacy = dict(binding.get("legacy_build") or {})
    if project == "scrapy":
        legacy["setup_dependency_installs"] = dict(SCRAPY_SETUP_INSTALLS)
        rewrites = dict(legacy.get("setup_command_rewrites") or {})
        rewrites.update(SCRAPY_SETUP_REWRITES)
        legacy["setup_command_rewrites"] = rewrites
    if project == "tornado":
        legacy["setup_dependency_installs"] = dict(TORNADO_SETUP_INSTALLS)
        rewrites = dict(legacy.get("setup_command_rewrites") or {})
        rewrites.update(TORNADO_SETUP_REWRITES)
        legacy["setup_command_rewrites"] = rewrites
    if project == "ansible":
        legacy["setup_dependency_installs"] = dict(ANSIBLE_SETUP_INSTALLS)
        legacy["setup_dependency_install_prerequisites"] = dict(ANSIBLE_SETUP_PREREQUISITES)
        rewrites = dict(legacy.get("setup_command_rewrites") or {})
        rewrites.update(ANSIBLE_SETUP_REWRITES)
        legacy["setup_command_rewrites"] = rewrites
    if project == "cookiecutter":
        command_prereqs = dict(legacy.get("setup_command_prerequisites") or {})
        command_prereqs.update(COOKIECUTTER_SETUP_COMMAND_PREREQUISITES)
        legacy["setup_command_prerequisites"] = command_prereqs
        legacy["test_prerequisites"] = list(COOKIECUTTER_TEST_PREREQUISITES)
        rewrites = dict(legacy.get("setup_command_rewrites") or {})
        rewrites.update(COOKIECUTTER_SETUP_REWRITES)
        legacy["setup_command_rewrites"] = rewrites
    binding["legacy_build"] = legacy
    write_json(path, binding)
    return sha_file(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_cache_root", type=Path,
                        help="Existing offline cache root (contains cache/ and bindings/)")
    parser.add_argument("destination_cache_root", type=Path,
                        help="Output offline cache root")
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()
    source = args.source_cache_root.resolve()
    destination = args.destination_cache_root.resolve()
    if destination.exists():
        raise SystemExit(f"destination already exists: {destination}")
    shutil.copytree(source, destination)
    cache = destination / "cache"
    manifest_path = cache / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != OFFLINE_CACHE_SCHEMA:
        raise SystemExit("unexpected offline cache schema")
    existing = {artifact["filename"] for artifact in manifest.get("artifacts", [])}
    downloads = []
    for project, version, filename in GLIBC234_ARTIFACTS:
        if filename in existing:
            downloads.append({
                "filename": filename,
                "status": "PASS",
                "computed_sha256": sha_file(cache / filename),
                "bytes": (cache / filename).stat().st_size,
                "reused_existing": True,
            })
            continue
        downloads.append(download_artifact(cache, project, version, filename))
        print("DOWNLOAD", filename, downloads[-1]["status"], flush=True)
    for result in downloads:
        if result["status"] != "PASS":
            raise SystemExit(f"download failed: {result}")
        filename = result["filename"]
        if filename in existing:
            continue
        manifest["artifacts"].append({
            "filename": filename,
            "sha256": result["computed_sha256"],
            "bytes": result["bytes"],
            "distribution_type": "bdist_wheel" if filename.endswith(".whl") else "sdist",
            "bindings": [{"note": "glibc234_topup"}],
        })
        existing.add(filename)
    manifest["source_sha"] = args.source_sha
    manifest["glibc234_topup_at"] = datetime.now(timezone.utc).isoformat()
    manifest["glibc234_topup_artifacts"] = [filename for _project, _version, filename in GLIBC234_ARTIFACTS]
    manifest["predecessor_manifest_sha256"] = sha_file(manifest_path)
    write_json(manifest_path, manifest)
    binding_receipts = {}
    for binding_path in sorted((destination / "bindings").glob("*-prospective-binding.json")):
        project = binding_path.name.replace("-prospective-binding.json", "")
        binding_receipts[project] = {
            "path": str(binding_path),
            "sha256": patch_binding(binding_path, project, args.source_sha),
        }
    receipt = {
        "schema_version": "orion.v2.e30-offline-cache-glibc234-topup.v1",
        "source_sha": args.source_sha,
        "source_cache_root": str(source),
        "destination_cache_root": str(destination),
        "manifest": {"path": str(manifest_path), "sha256": sha_file(manifest_path)},
        "added_artifacts": [item["filename"] for item in downloads if not item.get("reused_existing")],
        "bindings": binding_receipts,
    }
    receipt_path = destination / "receipts/GLIBC234_TOPUP.json"
    write_json(receipt_path, receipt)
    print(json.dumps({
        "destination": str(destination),
        "manifest_sha256": receipt["manifest"]["sha256"],
        "added_artifacts": receipt["added_artifacts"],
        "bindings": binding_receipts,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
