#!/usr/bin/env python3
"""Dispatch E70-GC1 while hidden-oracle bytes are absent from disk.

The private task payloads are loaded into this orchestrator's memory, hashed,
removed from the filesystem, and restored byte-for-byte only after the dispatch
subprocess exits. Child model processes receive no private bytes or private-path
environment variable. A crash may require deterministic task regeneration; that
is preferable to leaving the hidden oracle visible during model execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


class BlindDispatchError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--arms", required=True)
    parser.add_argument("--max-concurrency", type=int, default=2)
    parser.add_argument("--overwrite-responses", action="store_true")
    parser.add_argument(
        "--runner-script", type=Path,
        default=Path(__file__).resolve().parent / "run_orion_generated_composition_suite.py",
        help="suite runner exposing a `dispatch` action (default: GC1; E70-GC2 passes its own runner)",
    )
    args = parser.parse_args()
    if not args.runner_script.is_file():
        raise BlindDispatchError(f"runner script not found: {args.runner_script}")

    private_root = (args.workdir / "private").resolve()
    if not private_root.is_dir():
        raise BlindDispatchError(f"missing private oracle directory: {private_root}")
    payloads: dict[str, bytes] = {}
    for path in sorted(private_root.glob("*.json")):
        payloads[path.name] = path.read_bytes()
    if not payloads:
        raise BlindDispatchError("private oracle directory is empty")

    commitment = {
        "schema_version": "orion.v2.gc1-private-disk-absence.v1",
        "status": "COMMITTED_BEFORE_MODEL_DISPATCH",
        "private_file_count": len(payloads),
        "private_files": {name: digest(data) for name, data in payloads.items()},
        "private_directory_removed_before_child_process": True,
        "private_path_forwarded_to_model": False,
        "authority": {
            "grants_scientific_truth": False,
            "grants_training_data_absence_proof": False,
        },
    }
    write_json(args.workdir / "PRIVATE_ORACLE_COMMITMENT.json", commitment)

    shutil.rmtree(private_root)
    if private_root.exists():
        raise BlindDispatchError("failed to remove private oracle directory before dispatch")

    environment = os.environ.copy()
    for name in list(environment):
        if "PRIVATE" in name.upper() or "GOLD" in name.upper() or "ORACLE" in name.upper():
            if name.startswith(("ORION_GC1_", "ORION_GC2_", "ORION_GOLD")):
                environment.pop(name, None)
    environment["ORION_GOLD_ACCESS"] = "NONE"
    environment["ORION_OUTCOME_ACCESS"] = "NONE"

    command = [
        sys.executable,
        str(args.runner_script.resolve()),
        "dispatch",
        "--workdir",
        str(args.workdir),
        "--arms",
        args.arms,
        "--max-concurrency",
        str(args.max_concurrency),
    ]
    if args.overwrite_responses:
        command.append("--overwrite-responses")

    returncode = 99
    try:
        completed = subprocess.run(command, env=environment, check=False)
        returncode = completed.returncode
    finally:
        if private_root.exists():
            raise BlindDispatchError("private oracle directory unexpectedly reappeared during dispatch")
        private_root.mkdir(parents=True, exist_ok=False)
        for name, data in payloads.items():
            (private_root / name).write_bytes(data)
        restored = {path.name: digest(path.read_bytes()) for path in sorted(private_root.glob("*.json"))}
        expected = {name: digest(data) for name, data in payloads.items()}
        restoration = {
            "schema_version": "orion.v2.gc1-private-restoration.v1",
            "dispatch_returncode": returncode,
            "restored_file_count": len(restored),
            "hashes_match_commitment": restored == expected,
            "restored_files": restored,
        }
        write_json(args.workdir / "PRIVATE_ORACLE_RESTORATION.json", restoration)
        if restored != expected:
            raise BlindDispatchError("private oracle restoration hash mismatch")

    if returncode != 0:
        raise BlindDispatchError(f"model dispatch failed with return code {returncode}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BlindDispatchError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
