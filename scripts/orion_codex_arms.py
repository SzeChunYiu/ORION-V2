#!/usr/bin/env python3
"""Gold-blind ORION arm executable backed by the authenticated Codex CLI."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from orion_v2.patch_emission import (
    PatchEmissionError,
    emit_apply_clean_patch,
    extract_unified_diff,
    synthesize_diff_git_headers,
)


STAGES = (
    "INGEST", "DECOMPOSE", "SORT", "NATIVE_RECONSTRUCT", "REDUCE", "ABSORB",
    "RECOMBINE", "CHALLENGE", "ASSIMILATE_OR_RECYCLE",
)


def _schema() -> dict[str, Any]:
    stage_properties = {stage: {"type": "string"} for stage in STAGES}
    return {
        "type": "object",
        "properties": {
            "patch": {"type": "string"},
            "diagnosis": {"type": "string"},
            "assumptions": {"type": "array", "items": {"type": "string"}},
            "uncertainty": {"type": "string"},
            "discriminator_or_tests": {"type": "array", "items": {"type": "string"}},
            "falsifier": {"type": "string"},
            "stage_receipts": {
                "type": "object", "properties": stage_properties,
                "required": list(STAGES), "additionalProperties": False,
            },
        },
        "required": [
            "patch", "diagnosis", "assumptions", "uncertainty",
            "discriminator_or_tests", "falsifier", "stage_receipts",
        ],
        "additionalProperties": False,
    }


def _arm_instructions(arm: str) -> str:
    if arm == "SIMPLE_DIRECT":
        return "Solve directly using the smallest justified repair. Do not add reflection or lifecycle stages."
    if arm == "SAME_MODEL_REFLECTION":
        return "Form a direct repair, then perform one same-model critique and revise once."
    if arm == "F0_PARENT_FEDERATION":
        return "Federate native debugging parents: failing-test interpretation, source tracing, static reasoning, and regression-risk review. Prefer their strongest consensus."
    removed = {
        "F2_MINUS_DECOMPOSITION": "Do not decompose or source-sort; execute the remaining lifecycle.",
        "F2_MINUS_NATIVE_RECOVERY": "Do not perform native-parent reconstruction; execute the remaining lifecycle.",
        "F2_MINUS_COUNTERPROBE": "Do not perform challenge/counterprobe generation; execute the remaining lifecycle.",
        "F2_MINUS_SELECTIVE_REOPEN": "Use a flat update and do not selectively reopen support families.",
    }
    if arm in removed:
        return "Execute the ORION lifecycle with this registered component removal: " + removed[arm]
    if arm == "F2_ORION_METABOLIC_FULL":
        return "Execute all nine registered ORION lifecycle stages before selecting the smallest final repair."
    return "Use the smallest machine-native debugging strategy justified by the visible workspace."


def _prompt(request: dict[str, Any]) -> str:
    task = request.get("task", {})
    arm = str(request["arm_id"])
    baseline = task.get("baseline_observation", {})
    return f"""You are a protected, gold-blind software-repair experimental arm.
Inspect only the current workspace and the supplied failure observation. The workspace has no fixed solution or Git history. Do not use network retrieval. Do not edit files and do not claim a test passed unless you actually ran it. Return only the schema-conforming JSON object.

ARM: {arm}
ARM PROCEDURE: {_arm_instructions(arm)}
TASK METADATA: {json.dumps({k: v for k, v in task.items() if k != 'solver_workspace'}, sort_keys=True)}
FAILURE OBSERVATION: {json.dumps(baseline, sort_keys=True)}

`patch` must be a syntactically valid unified diff rooted at workspace-relative paths. Fill every stage receipt; use `NOT_APPLICABLE` for stages excluded by the arm. Never claim scientific truth, novelty, superiority, field status, or publication readiness.
"""


def _normalize_patch(patch: str) -> str:
    """Extract the diff from model output and add any implied ``diff --git`` header.

    Header synthesis only; canonicalization happens in :func:`emit_apply_clean_patch`,
    which ``execute`` calls directly. Retained as the named entry point for that stage
    so it stays independently testable.
    """
    try:
        return synthesize_diff_git_headers(extract_unified_diff(patch))
    except PatchEmissionError as exc:
        raise ValueError(str(exc)) from exc


def execute(request: dict[str, Any]) -> dict[str, Any]:
    task = request.get("task", {})
    workspace = Path(str(task.get("solver_workspace", "")))
    if not workspace.is_dir():
        raise ValueError(f"solver workspace is unavailable: {workspace}")
    start = time.time()
    with tempfile.TemporaryDirectory(prefix="orion-codex-") as temp:
        temp_path = Path(temp)
        schema_path = temp_path / "schema.json"
        output_path = temp_path / "output.json"
        schema_path.write_text(json.dumps(_schema()))
        command = [
            os.environ.get("ORION_CODEX_BIN", "codex"), "exec", "--ephemeral",
            "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check",
            "--sandbox", "read-only", "--cd", str(workspace), "--model",
            os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra"),
            "--output-schema", str(schema_path), "--output-last-message", str(output_path),
            _prompt(request),
        ]
        completed = subprocess.run(
            command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=int(os.environ.get("ORION_CODEX_TIMEOUT", "2700")), check=False,
        )
        if completed.returncode != 0 or not output_path.exists():
            raise RuntimeError(f"Codex CLI failed ({completed.returncode}): {completed.stdout[-2000:]}")
        data = json.loads(output_path.read_text())
    try:
        emission = emit_apply_clean_patch(str(data["patch"]), workspace=workspace)
    except PatchEmissionError as exc:
        raise ValueError(str(exc)) from exc
    token_matches = re.findall(r"tokens used\s*\n\s*([0-9,]+)", completed.stdout)
    total_tokens = int(token_matches[-1].replace(",", "")) if token_matches else None
    arm = str(request["arm_id"])
    return {
        "schema_version": "orion.v2.agent-response.v1",
        "task_id": request["task_id"], "arm_id": arm,
        "status": "COMPLETED_PROPOSAL_ONLY",
        "proposed_patch_or_artifact": {"type": "unified_diff", "content": emission.patch},
        "patch_emission_receipt": emission.receipt,
        "diagnosis": str(data["diagnosis"]),
        "source_ids_used": ["gold-blind-solver-workspace"],
        "assumptions": [str(item) for item in data["assumptions"]],
        "uncertainty": data["uncertainty"],
        "discriminator_or_tests": [str(item) for item in data["discriminator_or_tests"]],
        "falsifier": str(data["falsifier"]),
        "metabolic_stages": data["stage_receipts"],
        "requested_authority": "EXECUTION_TEST_ONLY",
        "scientific_truth_authorized": False, "field_status_authorized": False,
        "publication_readiness_authorized": False,
        "resource_receipt": {
            "model_calls": 1, "total_tokens_reported_by_cli": total_tokens,
            "wall_time_seconds": time.time() - start,
            "executor": "codex-cli", "model": os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text())
    try:
        response = execute(request)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        response = {
            "schema_version": "orion.v2.agent-response.v1", "task_id": request["task_id"],
            "arm_id": request["arm_id"], "status": "EXECUTION_FAILED_MODEL_RESPONSE",
            "proposed_patch_or_artifact": None, "diagnosis": str(exc), "source_ids_used": [],
            "assumptions": [], "uncertainty": "UNRESOLVED", "discriminator_or_tests": [],
            "falsifier": "repair the Codex CLI binding and rerun under a new identity",
            "requested_authority": "NONE", "scientific_truth_authorized": False,
            "field_status_authorized": False, "publication_readiness_authorized": False,
            "resource_receipt": {"model_calls": 0, "executor": "codex-cli"},
        }
    args.response.parent.mkdir(parents=True, exist_ok=True)
    args.response.write_text(json.dumps(response, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
