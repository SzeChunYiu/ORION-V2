#!/usr/bin/env python3
"""Assemble E70_GC2_CALIBRATION_RECEIPT_DEV.json from a fetched calibration campaign dir.

Usage: assemble_gc2_calibration_receipt.py <fetched_campaign_dir> <infra_bindings.txt> <out.json>
Copies the generator's CALIBRATION_RECEIPT verbatim, adds host/binary bindings, per-rung
custody receipts (commitment/restoration hashes), per-cell evaluation rows (no hidden
cases, no response bodies) and sha256 of every non-response file in the campaign.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path


def main() -> int:
    root, infra, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    receipt = json.loads((root / "CALIBRATION_RECEIPT.json").read_text())
    bindings = dict(item.split("=", 1) for item in infra.read_text().split() if "=" in item)
    rungs = {}
    manifest = {}
    for level_dir in sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("L")):
        frozen = json.loads((level_dir / "FROZEN_TASKS.json").read_text())
        commit = json.loads((level_dir / "PRIVATE_ORACLE_COMMITMENT.json").read_text())
        restore = json.loads((level_dir / "PRIVATE_ORACLE_RESTORATION.json").read_text())
        rollup = json.loads((level_dir / "EVALUATION_ROLLUP.json").read_text())
        rows = []
        for r in rollup["records"]:
            rows.append({k: r.get(k) for k in ("task_id", "arm_id", "rep", "status", "syntax_audit_status", "count_robust_patch_apply_success",
                                                "count_robust_hidden_oracle_success", "count_robust_hidden_accuracy", "raw_patch_apply_success",
                                                "raw_hidden_oracle_success", "count_robust_family_accuracy", "patch_paths", "model_tokens",
                                                "model_wall_time_seconds", "patch_size_bytes")})
        rungs[level_dir.name] = {
            "task_count": frozen["task_count"], "reps": frozen["reps"], "seed": frozen["seed"], "nonce_sha256": frozen["nonce_sha256"],
            "design_sha256": frozen["design_sha256"], "generator_self_check": frozen["generator_self_check"],
            "custody": {"commitment_status": commit["status"], "private_file_count": commit["private_file_count"],
                        "private_directory_removed_before_child_process": commit["private_directory_removed_before_child_process"],
                        "restoration_hashes_match_commitment": restore["hashes_match_commitment"], "dispatch_returncode": restore["dispatch_returncode"]},
            "cells": rows,
        }
        for f in sorted(level_dir.rglob("*")):
            if f.is_file() and "/responses/" not in f.as_posix():
                manifest[f.relative_to(root).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    out.write_text(json.dumps({
        "schema_version": "orion.v2.gc2-calibration-receipt-dev.v1",
        "receipt_id": "E70_GC2_CALIBRATION_RECEIPT_DEV",
        "host_bindings": bindings,
        "calibration": receipt,
        "rungs": rungs,
        "non_response_manifest_sha256": manifest,
        "authority": {"grants_scientific_truth": False, "grants_field_status": False, "grants_submission_readiness": False},
    }, indent=1) + "\n")
    print(json.dumps({"decision": receipt["decision"], "selected_level": receipt["selected_level"], "rungs": list(rungs)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
