#!/usr/bin/env python3
"""Audit agent unified-diff artifacts without gold access or semantic repair."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"response is not an object: {path}")
    return value


def _patch(response: dict[str, Any]) -> str | None:
    artifact = response.get("proposed_patch_or_artifact")
    if isinstance(artifact, dict) and artifact.get("type") == "unified_diff":
        content = artifact.get("content")
        return content if isinstance(content, str) else None
    if isinstance(artifact, str):
        return artifact
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--canonical-dir", type=Path)
    args = parser.parse_args()

    response_root = args.workdir / "responses"
    rows: list[dict[str, Any]] = []
    if not response_root.is_dir():
        raise SystemExit(f"missing response directory: {response_root}")

    for path in sorted(response_root.glob("*/*.json")):
        response = _read(path)
        patch = _patch(response)
        row: dict[str, Any] = {
            "arm_id": response.get("arm_id") or path.parent.name,
            "task_id": response.get("task_id") or path.stem,
            "response_path": str(path),
            "has_unified_diff": patch is not None,
        }
        if patch is None:
            row["interface_status"] = "NOT_APPLICABLE_NO_UNIFIED_DIFF"
        else:
            audited = audit_and_canonicalize_unified_diff(patch)
            row.update(
                {
                    "interface_status": (
                        "VALID_UNCHANGED"
                        if audited.valid_or_canonicalizable and not audited.changed
                        else "VALID_AFTER_SYNTAX_ONLY_CANONICALIZATION"
                        if audited.valid_or_canonicalizable
                        else "INVALID_NOT_CANONICALIZABLE"
                    ),
                    "original_sha256": _sha(patch),
                    "canonical_sha256": (
                        _sha(audited.canonical_diff)
                        if audited.canonical_diff is not None
                        else None
                    ),
                    "syntax_only_changed": audited.changed,
                    "reasons": list(audited.reasons),
                }
            )
            if args.canonical_dir and audited.canonical_diff is not None:
                destination = args.canonical_dir / str(row["arm_id"]) / f"{row['task_id']}.patch"
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(audited.canonical_diff, encoding="utf-8")
                row["canonical_patch_path"] = str(destination)
        rows.append(row)

    counts: dict[str, int] = {}
    for row in rows:
        status = str(row["interface_status"])
        counts[status] = counts.get(status, 0) + 1

    result = {
        "schema_version": "orion.v2.diff-interface-audit.v1",
        "status": "SENSITIVITY_ONLY_NO_PRIMARY_OUTCOME_AUTHORITY",
        "gold_or_fixed_patch_access": "FORBIDDEN_NOT_USED",
        "rows": rows,
        "counts": counts,
        "authority": {
            "may_replace_raw_primary_result": False,
            "may_change_semantic_edit": False,
            "may_guess_paths": False,
            "may_grant_scientific_truth": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
