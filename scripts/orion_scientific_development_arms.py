#!/usr/bin/env python3
"""Gold-blind Codex executable for SD70 scientific-development meta-policy tasks."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any


def _schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "selected_action": {"type": "string"},
            "principle_summary": {"type": "string"},
            "preconditions": {"type": "array", "items": {"type": "string"}},
            "contraindications": {"type": "array", "items": {"type": "string"}},
            "failure_modes": {"type": "array", "items": {"type": "string"}},
            "uncertainty": {"type": "string"},
            "falsifier": {"type": "string"},
        },
        "required": ["selected_action", "principle_summary", "preconditions", "contraindications", "failure_modes", "uncertainty", "falsifier"],
        "additionalProperties": False,
    }


def _arm_instruction(arm: str) -> str:
    table = {
        "TARGET_ONLY_DIRECT": "Choose one visible candidate action using only the held-out context. Do not infer a general rule from the trajectory population.",
        "FIXED_META_HEURISTIC": "Use only a fixed population heuristic: prefer actions with the strongest overall validated-success minus validated-failure frequency. Do not invent a context-specific latent rule.",
        "F0_PARENT_FEDERATION": "Use mature parent reasoning only: matched-case comparison, conditional empirical frequencies, simple rule induction, and explicit failure controls. Prefer the simplest parent explanation that fits the visible training trajectories.",
        "F2_STATIC_NO_RECURSION": "Use one level of ORION transfer/conceptual abstraction over the visible trajectories, but do not recursively abstract operators into higher-order policies.",
        "F2_RECURSIVE_META_DISCOVERY_FULL": "Infer a bounded development policy from success and failure trajectories, test it against contradictions, distinguish preconditions from contraindications, and select one candidate action for the held-out context. Do not assume any named breakthrough recipe.",
    }
    return table.get(arm, "Use the visible trajectories conservatively and select exactly one candidate action.")


def _prompt(request: dict[str, Any]) -> str:
    task = request["task"]
    arm = str(request["arm_id"])
    return f"""You are a protected, gold-blind scientific-development experimental arm.
The task contains synthetic source-bound research trajectories with arbitrary codewords. The hidden generator rule and correct held-out action are not available. Do not use network retrieval. Do not claim scientific truth, a causal law, field status, or publication readiness.

ARM: {arm}
ARM PROCEDURE: {_arm_instruction(arm)}
TRAINING TRAJECTORIES: {json.dumps(task['training_episodes'], sort_keys=True)}
HELD-OUT CONTEXT: {json.dumps(task['query_context_features'], sort_keys=True)}
CANDIDATE ACTIONS: {json.dumps(task['candidate_actions'], sort_keys=True)}

Return exactly one candidate action. Your principle summary must be bounded to the visible task and must mention failure/contraindication evidence when relevant. The selected action MUST exactly equal one of the candidate action strings.
"""


def execute(request: dict[str, Any]) -> dict[str, Any]:
    start = time.time()
    with tempfile.TemporaryDirectory(prefix="orion-sd70-") as temp:
        temp_path = Path(temp)
        schema_path = temp_path / "schema.json"
        output_path = temp_path / "output.json"
        schema_path.write_text(json.dumps(_schema()), encoding="utf-8")
        command = [
            os.environ.get("ORION_CODEX_BIN", "codex"), "exec", "--ephemeral",
            "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check",
            "--sandbox", "read-only", "--model", os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra"),
            "--output-schema", str(schema_path), "--output-last-message", str(output_path),
            _prompt(request),
        ]
        completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=int(os.environ.get("ORION_SD70_TIMEOUT", "1800")), check=False)
        if completed.returncode != 0 or not output_path.exists():
            raise RuntimeError(f"Codex CLI failed ({completed.returncode}): {completed.stdout[-1600:]}")
        data = json.loads(output_path.read_text(encoding="utf-8"))
    candidates = set(request["task"]["candidate_actions"])
    if data["selected_action"] not in candidates:
        raise ValueError("selected_action is outside the frozen candidate set")
    return {
        "schema_version": "orion.v2.sd70-agent-response.v1",
        "task_id": request["task_id"],
        "arm_id": request["arm_id"],
        "status": "COMPLETED_PROPOSAL_ONLY",
        "selected_action": data["selected_action"],
        "principle_summary": data["principle_summary"],
        "preconditions": data["preconditions"],
        "contraindications": data["contraindications"],
        "failure_modes": data["failure_modes"],
        "uncertainty": data["uncertainty"],
        "falsifier": data["falsifier"],
        "resource_receipt": {"model_calls": 1, "wall_time_seconds": time.time() - start, "executor": "codex-cli", "model": os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra")},
        "scientific_truth_authorized": False,
        "causal_law_authorized": False,
        "field_status_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    try:
        response = execute(request)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        response = {
            "schema_version": "orion.v2.sd70-agent-response.v1",
            "task_id": request.get("task_id"), "arm_id": request.get("arm_id"),
            "status": "EXECUTION_FAILED_MODEL_RESPONSE", "selected_action": None,
            "principle_summary": "", "preconditions": [], "contraindications": [], "failure_modes": [],
            "uncertainty": "UNRESOLVED", "falsifier": str(exc),
            "resource_receipt": {"model_calls": 0, "executor": "codex-cli"},
            "scientific_truth_authorized": False, "causal_law_authorized": False, "field_status_authorized": False,
        }
    args.response.parent.mkdir(parents=True, exist_ok=True)
    args.response.write_text(json.dumps(response, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
