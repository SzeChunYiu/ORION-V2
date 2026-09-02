#!/usr/bin/env python3
"""SD70-V2 gold-blind model executable (Codex CLI) for the contested arms.

The prompt is built ONLY from `request["surface"]`; keys absent from the
surface are physically absent from the prompt. One model call per arm-task
(no in-process retry); resource receipt parsed from the Codex `--json` event
stream. The child runs in an empty temporary working directory.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

RESPONSE_SCHEMA = "orion.v2.sd70-v2.response.v1"

ARM_PROCEDURES: dict[str, str] = {
    "TARGET_ONLY_NEGATIVE_CONTROL": (
        "No trajectories are provided. Select exactly one candidate action for the held-out context."
    ),
    "F2_STATIC_NO_RECURSION": (
        "Use ONE level of abstraction over the visible trajectories: induce a bounded action-selection rule "
        "(which context features favour which action) from SUCCESS and FAILURE trajectories, check it against every "
        "visible contradiction, and select one candidate action for the held-out context. Do NOT recursively abstract "
        "the induced rules into higher-order policies; do not revise the rule set after the first induction pass. "
        "The parent advisory block, when present, is the output of deterministic mature parents on this same evidence; "
        "you may use it as evidence but you must reach your own decision."
    ),
    "F2_RECURSIVE_META_DISCOVERY_FULL": (
        "Apply the full recursive meta-discovery procedure: (1) induce candidate action-selection rules from SUCCESS and "
        "FAILURE trajectories; (2) abstract the rule set into a higher-order policy (which feature combinations govern "
        "which action, with preconditions and contraindications); (3) recursively re-apply the induction to the policy "
        "itself, testing it against every visible contradiction and revising until no visible contradiction remains or "
        "the policy is bounded; (4) select one candidate action for the held-out context. The parent advisory block, "
        "when present, is the output of deterministic mature parents on this same evidence; treat it as one more source "
        "to be tested and revised, not as authority."
    ),
}
ARM_PROCEDURES["F2_FULL_MINUS_FAILURE_EVIDENCE"] = ARM_PROCEDURES["F2_RECURSIVE_META_DISCOVERY_FULL"]
ARM_PROCEDURES["F2_FULL_MINUS_PARENT_FEDERATION"] = ARM_PROCEDURES["F2_RECURSIVE_META_DISCOVERY_FULL"]


def base_arm(arm_id: str) -> str:
    return arm_id.split("__", 1)[0]


def output_schema() -> dict[str, Any]:
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


def build_prompt(request: dict[str, Any]) -> str:
    surface = request["surface"]
    arm = str(request["arm_id"])
    procedure = ARM_PROCEDURES.get(base_arm(arm))
    if procedure is None:
        raise ValueError(f"no registered model procedure for arm {arm}")
    lines = [
        "You are a protected, gold-blind scientific-development experimental arm.",
        "The task contains synthetic research trajectories with arbitrary codewords. The hidden generator rule and the correct held-out action are not available to you or to anyone in this process. Do not use network retrieval. Do not execute shell commands or read files; answer from the prompt alone. Do not claim scientific truth, a causal law, field status, or publication readiness.",
        "",
        f"ARM: {arm}",
        f"ARM PROCEDURE: {procedure}",
        f"TASK INSTRUCTION: {surface['instruction']}",
    ]
    if "training_episodes" in surface:
        lines.append(f"TRAINING TRAJECTORIES: {json.dumps(surface['training_episodes'], sort_keys=True)}")
    if "parent_advisory" in surface:
        lines.append(f"PARENT ADVISORY (deterministic parents on the same evidence): {json.dumps(surface['parent_advisory'], sort_keys=True)}")
    lines += [
        f"HELD-OUT CONTEXT: {json.dumps(surface['query_context_features'], sort_keys=True)}",
        f"CANDIDATE ACTIONS: {json.dumps(surface['candidate_actions'], sort_keys=True)}",
        "",
        "Return exactly one candidate action. The selected action MUST exactly equal one of the candidate action strings. Keep the principle summary bounded to the visible task.",
    ]
    return "\n".join(lines) + "\n"


def parse_events(text: str) -> dict[str, Any]:
    usage: dict[str, Any] = {"input_tokens": None, "output_tokens": None, "total_tokens": None, "tool_calls": 0, "event_count": 0}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        usage["event_count"] += 1
        _scan_usage(ev, usage)
        blob = json.dumps(ev)
        if '"command_execution"' in blob and ("item.started" in blob or "item.completed" in blob):
            usage["tool_calls"] += 1 if "item.completed" in blob else 0
    if usage["total_tokens"] is None and usage["input_tokens"] is not None and usage["output_tokens"] is not None:
        usage["total_tokens"] = usage["input_tokens"] + usage["output_tokens"]
    return usage


def _scan_usage(obj: Any, usage: dict[str, Any]) -> None:
    if isinstance(obj, dict):
        if "input_tokens" in obj and isinstance(obj.get("input_tokens"), int):
            usage["input_tokens"] = obj["input_tokens"]
        if "output_tokens" in obj and isinstance(obj.get("output_tokens"), int):
            usage["output_tokens"] = obj["output_tokens"]
        if "total_tokens" in obj and isinstance(obj.get("total_tokens"), int):
            usage["total_tokens"] = obj["total_tokens"]
        for v in obj.values():
            _scan_usage(v, usage)
    elif isinstance(obj, list):
        for v in obj:
            _scan_usage(v, usage)


def execute(request: dict[str, Any]) -> dict[str, Any]:
    start = time.time()
    model = os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra")
    effort = os.environ.get("ORION_SD70_REASONING_EFFORT", "medium")
    timeout = int(os.environ.get("ORION_SD70_TIMEOUT", "600"))
    prompt = build_prompt(request)
    with tempfile.TemporaryDirectory(prefix="orion-sd70v2-") as temp:
        temp_path = Path(temp)
        cwd = temp_path / "empty"
        cwd.mkdir()
        schema_path = temp_path / "schema.json"
        output_path = temp_path / "output.json"
        schema_path.write_text(json.dumps(output_schema()), encoding="utf-8")
        command = [
            os.environ.get("ORION_CODEX_BIN", "codex"), "exec", "--ephemeral",
            "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check",
            "--sandbox", "read-only", "-C", str(cwd), "--model", model,
            "-c", f'model_reasoning_effort="{effort}"', "--json",
            "--output-schema", str(schema_path), "--output-last-message", str(output_path),
            prompt,
        ]
        completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   timeout=timeout, check=False)
        usage = parse_events(completed.stdout)
        if completed.returncode != 0 or not output_path.exists():
            raise RuntimeError(f"Codex CLI failed ({completed.returncode}): {completed.stderr[-1200:]} {completed.stdout[-400:]}")
        data = json.loads(output_path.read_text(encoding="utf-8"))
    candidates = set(request["surface"]["candidate_actions"])
    wall = time.time() - start
    receipt = {"model_calls": 1, "wall_time_seconds": wall, "executor": "codex-cli", "model": model,
               "reasoning_effort": effort, "timeout_seconds": timeout, **usage}
    if data["selected_action"] not in candidates:
        return _failed(request, "SELECTED_ACTION_OUTSIDE_CANDIDATES", receipt, raw=data)
    return {
        "schema_version": RESPONSE_SCHEMA,
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
        "resource_receipt": receipt,
        "scientific_truth_authorized": False,
        "causal_law_authorized": False,
        "field_status_authorized": False,
    }


def _failed(request: dict[str, Any], reason: str, receipt: dict[str, Any] | None = None, raw: Any = None) -> dict[str, Any]:
    return {
        "schema_version": RESPONSE_SCHEMA,
        "task_id": request.get("task_id"), "arm_id": request.get("arm_id"),
        "status": "EXECUTION_FAILED_MODEL_RESPONSE", "failure_reason": reason, "selected_action": None,
        "principle_summary": "", "preconditions": [], "contraindications": [], "failure_modes": [],
        "uncertainty": "UNRESOLVED", "falsifier": "", "raw_model_output": raw,
        "resource_receipt": receipt or {"model_calls": 1, "executor": "codex-cli"},
        "scientific_truth_authorized": False, "causal_law_authorized": False, "field_status_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    try:
        response = execute(request)
    except subprocess.TimeoutExpired as exc:
        response = _failed(request, f"TIMEOUT:{exc.timeout}")
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, json.JSONDecodeError, KeyError) as exc:
        response = _failed(request, f"{type(exc).__name__}:{str(exc)[:800]}")
    args.response.parent.mkdir(parents=True, exist_ok=True)
    args.response.write_text(json.dumps(response, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
