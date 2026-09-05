"""Read-only custody and fresh-process replay for the integrated Foundation studies.

Exit 0: requested finite checks passed; 1: defect; 2: missing/unavailable evidence.
These research checks do not grant scientific truth, novelty or OCM authority.
"""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
THEORY = "research/machine-epistemics-theory"
CANONICAL = f"{THEORY}/MACHINE_EPISTEMICS_FOUNDATION_V1.json"
SUPPORTING = f"{THEORY}/ME_FOUNDATION_V1.json"
EXPECTED_PRS = {320, 321, 322, 323, 324, 325, 326, 327, 328, 331}
SOURCE_INVENTORY_SHA256 = "6be8f8c531b3881dd4b53b99b5b7620f975d3f42b6a9d290f0738a4a7df951d0"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def scoped(root: Path, relative: str) -> Path:
    p = Path(relative)
    require(not p.is_absolute() and ".." not in p.parts, "unscoped provenance path")
    path = root / p
    require(path.resolve().is_relative_to(root.resolve()), "provenance path escapes root")
    return path


def verify(manifest: dict, root: Path = ROOT) -> dict:
    require(manifest.get("schema") == "ME_FOUNDATION_INTEGRATION_V1", "manifest schema")
    require(manifest.get("canonical_registry") == CANONICAL, "canonical registry substituted")
    require(manifest.get("supporting_registry") == SUPPORTING, "supporting registry substituted")
    require(manifest.get("scientific_completion") is False, "unearned scientific completion")
    require(manifest.get("ocm_adoption_authorized") is False, "unearned OCM adoption")
    require(manifest.get("independent_external_review") == "NOT_OBTAINED", "unearned external review")
    sources = manifest["sources"]
    require(len(sources) == len(EXPECTED_PRS) and {s["pr"] for s in sources} == EXPECTED_PRS,
            "source PR coverage")
    # This separately acquired source inventory is anchored outside the editable
    # relocation manifest. Source hashes alone do not establish commit identity
    # or completeness: deleting a file or forging a head must not pass custody.
    inventory_bytes = scoped(root, f"{THEORY}/foundation_integration_v1/SOURCE_INVENTORY.json").read_bytes()
    require(sha256(inventory_bytes).hexdigest() == SOURCE_INVENTORY_SHA256, "source inventory digest drift")
    inventory = json.loads(inventory_bytes)
    require(inventory["schema"] == "ME_FOUNDATION_SOURCE_INVENTORY_V1", "source inventory schema")
    registered = {s["pr"]: s for s in inventory["sources"]}
    require(set(registered) == EXPECTED_PRS, "source inventory PR coverage")
    seen = set()
    count = relocated = adapted = 0
    for source in sources:
        require(len(source["head_sha"]) == 40 and all(c in "0123456789abcdef" for c in source["head_sha"]),
                "invalid source commit")
        require(source["files"], "empty source package")
        expected = registered[source["pr"]]
        require(source["head_sha"] == expected["head_sha"], "source inventory commit mismatch")
        observed_files = {e["source_path"]: e["source_git_blob_sha1"] for e in source["files"]}
        require(len(observed_files) == len(source["files"]) and observed_files == expected["files"],
                "source inventory path/blob coverage mismatch")
        for entry in source["files"]:
            target = entry["integrated_path"]
            require(target not in seen, "colliding integration targets")
            seen.add(target)
            integrated = scoped(root, target).read_bytes()
            original = scoped(root, entry["source_bytes_path"]).read_bytes()
            require(sha256(original).hexdigest() == entry["source_sha256"], "source-byte drift: " + target)
            require(sha1(b"blob " + str(len(original)).encode() + b"\0" + original).hexdigest()
                    == entry["source_git_blob_sha1"], "source blob drift: " + target)
            require(sha256(integrated).hexdigest() == entry["integrated_sha256"], "integrated-byte drift: " + target)
            if original != integrated:
                adapted += 1
                require(entry["adaptation"] == "PATH_ONLY_CALLER_RELOCATION", "undeclared source adaptation")
                require(entry["source_bytes_path"] != target, "adaptation erased its source")
                require(entry["source_path"] in {
                    "tests/unit/test_me_foundation_revision_v1.py",
                    ".github/workflows/me-foundation-typed-lifecycle.yml"}, "unexpected adapted source")
                successor = "foundation_revision_v1" if source["pr"] == 323 else "foundation_typed_lifecycle_v1"
                require(original.replace(b"machine-epistemics-theory/foundation_v1",
                                         ("machine-epistemics-theory/" + successor).encode()) == integrated,
                        "adaptation changed more than package path")
            else:
                require(entry["adaptation"] == "NONE", "spurious adaptation declaration")
            relocated += target != entry["source_path"]
            count += 1
    # The historical #323 receipt remains byte-identical and is interpreted in
    # its original source namespace, never falsely rebound to the adapted test.
    source = next(s for s in sources if s["pr"] == 323)
    by_path = {e["source_path"]: e for e in source["files"]}
    receipt_entry = by_path[f"{THEORY}/foundation_v1/RECEIPT.json"]
    receipt = json.loads(scoped(root, receipt_entry["source_bytes_path"]).read_text())
    for name, binding in receipt["bound_files"].items():
        entry = by_path[name]
        original = scoped(root, entry["source_bytes_path"]).read_bytes()
        require(sha256(original).hexdigest() == binding["sha256"], "historical receipt drift: " + name)
        require(len(original) == binding["bytes"], "historical receipt size: " + name)
        require(entry["source_git_blob_sha1"] == binding["git_blob_sha1"], "historical receipt blob: " + name)
    require(CANONICAL in seen and SUPPORTING in seen, "registry absent from source custody")
    return {"source_prs": len(sources), "source_files": count, "relocated_files": relocated,
            "adapted_callers": adapted, "historical_receipt_bindings": len(receipt["bound_files"])}


def commands():
    """Explicit bounded replay routes; no outcome-writing mode or shell evaluation."""
    suites = [
        ("foundation_unit_and_conformance", ".", ["-m", "pytest", "-q",
            "tests/unit/test_me_foundation_registry.py", "tests/unit/test_meg_foundation_batch2.py",
            "tests/unit/test_meg_foundation_batch3.py", "tests/unit/test_meg_foundation_batch4_parent_adoptions.py",
            "tests/unit/test_me_foundation_revision_v1.py", "tests/unit/test_machine_epistemics_foundation_v1_v2.py",
            "tests/unit/test_me_causal_verifier_v1.py", "tests/unit/test_me_foundation_integration_v1.py"], 0),
        ("decision_frontier_tests", "decision_frontier_v1", ["-m", "unittest", "-v", "test_frontier"], 0),
        ("decision_frontier_receipt", "decision_frontier_v1", ["run_checks.py", "--verify"], 0),
        ("certificate_lifecycle", "certificate_lifecycle_v1", ["check.py"], 0),
        ("causal_verifier_receipt", "causal_verifier_v1", ["verify_receipt.py"], 0),
        ("revision_consistency", "revision_consistency_v1", ["verify_package.py", "--verify"], 0),
        ("revision_consistency_hostile", "revision_consistency_v1", ["verify_package.py", "--selftest"], 0),
        ("temporal_validity", "revision_consistency_v1/temporal_v2", ["run.py", "--verify"], 0),
        ("temporal_validity_hostile", "revision_consistency_v1/temporal_v2", ["run.py", "--selftest"], 0),
        ("causal_transport", "causal_transport_v1", ["run_checks.py", "--verify"], 0),
        ("causal_transport_optimized_refusal", "causal_transport_v1", ["-O", "run_checks.py", "--verify"], 2),
        ("typed_lifecycle", "foundation_typed_lifecycle_v1", ["verify_bundle.py", "--hostile"], 0),
        ("typed_lifecycle_optimized", "foundation_typed_lifecycle_v1", ["-O", "verify_bundle.py"], 0),
        ("revision_stopping_counterexample", "foundation_revision_v1", ["stopping_counterexample.py"], 0),
        ("certificate_transport_tests", "certificate_transport_v1", ["-m", "unittest", "-v", "test_transport"], 0),
        ("certificate_transport", "certificate_transport_v1", ["checks.py", "--verify", "RESULTS.json"], 0),
        ("certificate_transport_extensions", "certificate_transport_v1", ["extensions.py", "--verify", "EXTENSION_RESULTS.json"], 0),
        ("certificate_transport_sampling", "certificate_transport_v1", ["sampling.py", "--verify", "SAMPLING_RESULTS.json"], 0),
        ("certificate_transport_receipt", "certificate_transport_v1", ["verify_package.py"], 0),
    ]
    return [(name, "." if cwd == "." else f"{THEORY}/{cwd}", args, expected)
            for name, cwd, args, expected in suites]


def replay(include_lean=False):
    records = []
    suite = commands()
    if include_lean:
        suite.append(("lean_logical_bridge", f"{THEORY}/foundation_typed_lifecycle_v1", ["verify_lean.py"], 0))
    for name, cwd, args, expected in suite:
        command = [sys.executable, *args]
        try:
            proc = subprocess.run(command, cwd=ROOT / cwd, capture_output=True, text=True,
                                  check=False, timeout=180)
        except subprocess.TimeoutExpired as exc:
            raise OSError("bounded replay timed out: " + name) from exc
        record = {"name": name, "cwd": cwd, "argv": ["python", *args],
                  "expected_exit": expected, "actual_exit": proc.returncode,
                  "stdout": proc.stdout, "stderr": proc.stderr}
        records.append(record)
        print(json.dumps({"check": name, "expected_exit": expected,
                          "actual_exit": proc.returncode}), file=sys.stderr, flush=True)
        if proc.returncode != expected:
            print(json.dumps(record, sort_keys=True), file=sys.stderr)
            if proc.returncode == 2:
                raise OSError("replay cannot check: " + name)
            raise ValueError("replay failed: " + name)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--include-lean", action="store_true", help="Require the separately scoped Lean bridge")
    args = parser.parse_args()
    try:
        manifest = json.loads((HERE / "MANIFEST.json").read_text())
        result = {"schema": "ME_FOUNDATION_INTEGRATION_REPLAY_V1", "custody": verify(manifest),
                  "environment": {"python": platform.python_version(), "system": platform.system()},
                  "scientific_completion": False, "independent_external_review": "NOT_OBTAINED",
                  "ocm_adoption_authorized": False,
                  "lean_bridge": "REQUESTED" if args.include_lean else "NOT_RUN"}
        if args.replay or args.include_lean:
            result["commands"] = replay(args.include_lean)
            result["post_replay_custody"] = verify(manifest)
        result["terminal"] = "REQUESTED_INTEGRATION_CHECKS_PASS"
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0
    except (OSError, ImportError) as exc:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"terminal": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
