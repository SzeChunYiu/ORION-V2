#!/usr/bin/env python3
"""Versioned Anthropic-compatible ORION-V2 arm executables.

The runner is deliberately proposal-only: it receives a gold-blind request and
returns a schema-valid unified-diff proposal. Native evaluation remains outside
this process.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

FULL_STAGES = (
    "INGEST", "DECOMPOSE", "SORT", "NATIVE_RECONSTRUCT", "REDUCE", "ABSORB",
    "RECOMBINE", "CHALLENGE", "ASSIMILATE_OR_RECYCLE",
)


def _json_object(text: str) -> dict[str, Any]:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("model did not return a JSON object")
    value = json.loads(text[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("model JSON result is not an object")
    return value


def _final_prompt(context: str, prior: str = "") -> str:
    return """Return only one JSON object with keys patch, diagnosis, assumptions, uncertainty, discriminator_or_tests, falsifier.
`patch` must be one syntactically valid unified diff, rooted at repository paths (diff --git ...), with no Markdown fence.
You are operating only in the gold-blind buggy workspace. Never claim success, novelty, scientific truth, field status, or publication readiness.
Do not use network retrieval and do not invent test results. Propose the smallest patch justified by the supplied evidence.

GOLD-BLIND TASK CONTEXT:
""" + context + ("\n\nPRIOR DELIBERATION:\n" + prior if prior else "")


def _stage_prompt(label: str, context: str, prior: str = "") -> str:
    return f"""You are the {label} stage of a gold-blind ORION-V2 debugging arm.
Do not emit a patch yet. Inspect only the supplied context; state uncertainty, a discriminator, and a falsifier. Do not claim execution success.

TASK CONTEXT:
{context}

PRIOR STAGE OUTPUT:
{prior}
"""


def _parse_patch(text: str) -> tuple[str, str, list[str], Any, list[str], str]:
    data = _json_object(text)
    patch = data.get("patch")
    if not isinstance(patch, str) or not patch.lstrip().startswith("diff --git "):
        raise ValueError("model JSON lacks a unified diff patch")
    diagnosis = str(data.get("diagnosis", "model-proposed patch"))
    assumptions = data.get("assumptions", [])
    tests = data.get("discriminator_or_tests", [])
    if not isinstance(assumptions, list):
        assumptions = [str(assumptions)]
    if not isinstance(tests, list):
        tests = [str(tests)]
    assumptions = [str(x) for x in assumptions if str(x).strip()] or ["gold and fixed version remain unavailable"]
    tests = [str(x) for x in tests if str(x).strip()] or ["run native BugsInPy evaluator"]
    falsifier = str(data.get("falsifier", "native evaluator rejects the patch"))
    return patch, diagnosis, assumptions, data.get("uncertainty", "UNRESOLVED"), tests, falsifier


def run_arm(
    request: dict[str, Any],
    *,
    call: Callable[[str], tuple[str, dict[str, int]]],
    workspace_context: str,
) -> dict[str, Any]:
    arm = str(request["arm_id"])
    calls: list[dict[str, int]] = []

    def ask(prompt: str) -> str:
        text, usage = call(prompt)
        calls.append({"input_tokens": int(usage.get("input_tokens", 0)), "output_tokens": int(usage.get("output_tokens", 0))})
        return text

    stages: dict[str, str] | None = None
    try:
        if arm == "SIMPLE_DIRECT":
            final = ask(_final_prompt(workspace_context))
        elif arm == "SAME_MODEL_REFLECTION":
            draft = ask(_stage_prompt("same-model draft diagnosis", workspace_context))
            final = ask(_final_prompt(workspace_context, draft))
        elif arm == "F0_PARENT_FEDERATION":
            first = ask(_stage_prompt("native parent diagnosis A", workspace_context))
            second = ask(_stage_prompt("native parent diagnosis B", workspace_context))
            final = ask(_final_prompt(workspace_context, first + "\n\n" + second))
        elif arm.startswith("F2_"):
            ingest = ask(_stage_prompt("INGEST/DECOMPOSE/SORT", workspace_context))
            reconstruct = ask(_stage_prompt("NATIVE_RECONSTRUCT/REDUCE/ABSORB/RECOMBINE", workspace_context, ingest))
            challenge = ask(_final_prompt(workspace_context, ingest + "\n\n" + reconstruct))
            final = challenge
            if arm == "F2_ORION_METABOLIC_FULL":
                stages = {
                    "INGEST": ingest, "DECOMPOSE": ingest, "SORT": ingest,
                    "NATIVE_RECONSTRUCT": reconstruct, "REDUCE": reconstruct,
                    "ABSORB": reconstruct, "RECOMBINE": reconstruct,
                    "CHALLENGE": challenge, "ASSIMILATE_OR_RECYCLE": challenge,
                }
        else:
            final = ask(_final_prompt(workspace_context))
        patch, diagnosis, assumptions, uncertainty, tests, falsifier = _parse_patch(final)
        response: dict[str, Any] = {
            "schema_version": "orion.v2.agent-response.v1", "task_id": request["task_id"], "arm_id": arm,
            "status": "COMPLETED_PROPOSAL_ONLY", "proposed_patch_or_artifact": {"type": "unified_diff", "content": patch},
            "diagnosis": diagnosis, "source_ids_used": ["gold-blind-solver-workspace"], "assumptions": assumptions,
            "uncertainty": uncertainty, "discriminator_or_tests": tests, "falsifier": falsifier,
            "requested_authority": "EXECUTION_TEST_ONLY", "scientific_truth_authorized": False,
            "field_status_authorized": False, "publication_readiness_authorized": False,
            "resource_receipt": {"model_calls": len(calls), "input_tokens": sum(x["input_tokens"] for x in calls), "output_tokens": sum(x["output_tokens"] for x in calls)},
        }
        if stages is not None:
            response["metabolic_stages"] = stages
        return response
    except (ValueError, RuntimeError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return {
            "schema_version": "orion.v2.agent-response.v1", "task_id": request["task_id"], "arm_id": arm,
            "status": "EXECUTION_FAILED_MODEL_RESPONSE", "proposed_patch_or_artifact": None, "diagnosis": str(exc),
            "source_ids_used": [], "assumptions": [], "uncertainty": "UNRESOLVED", "discriminator_or_tests": [],
            "falsifier": "repair the bound provider response and rerun under a new identity", "requested_authority": "NONE",
            "scientific_truth_authorized": False, "field_status_authorized": False, "publication_readiness_authorized": False,
            "resource_receipt": {"model_calls": len(calls), "input_tokens": sum(x["input_tokens"] for x in calls), "output_tokens": sum(x["output_tokens"] for x in calls)},
        }


def _provider_call(prompt: str) -> tuple[str, dict[str, int]]:
    base = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
    url = base + ("/messages" if base.endswith("/v1") else "/v1/messages")
    body = json.dumps({"model": os.environ["ANTHROPIC_MODEL"], "max_tokens": int(os.environ.get("ORION_ARM_MAX_TOKENS", "6000")), "temperature": 0, "system": "You are a bounded experimental software-debugging arm.", "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(url, data=body, headers={"x-api-key": os.environ["ANTHROPIC_AUTH_TOKEN"], "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=int(os.environ.get("ORION_ARM_HTTP_TIMEOUT", "1800"))) as raw:
        data = json.load(raw)
    text = "".join(str(x.get("text", "")) for x in data.get("content", []) if isinstance(x, dict))
    return text, dict(data.get("usage", {}))


def _context(request: dict[str, Any]) -> str:
    task = request.get("task", {})
    workspace = Path(str(task.get("solver_workspace", "")))
    listing: list[str] = []
    if workspace.is_dir():
        listing = [p.relative_to(workspace).as_posix() for p in sorted(workspace.rglob("*.py"))[:80]]
    return json.dumps({"task": task, "python_files": listing, "gold_access": "NONE", "network_allowed_during_solution": False}, indent=2, sort_keys=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text())
    start = time.time()
    response = run_arm(request, call=_provider_call, workspace_context=_context(request))
    response["resource_receipt"]["wall_time_seconds"] = time.time() - start
    args.response.parent.mkdir(parents=True, exist_ok=True)
    args.response.write_text(json.dumps(response, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
