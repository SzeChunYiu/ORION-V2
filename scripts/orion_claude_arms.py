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
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

from orion_v2.patch_emission import PatchEmissionError, emit_apply_clean_patch

FULL_STAGES = (
    "INGEST", "DECOMPOSE", "SORT", "NATIVE_RECONSTRUCT", "REDUCE", "ABSORB",
    "RECOMBINE", "CHALLENGE", "ASSIMILATE_OR_RECYCLE",
)


class ServedModelMismatch(RuntimeError):
    """The provider served a different model than the one this run is pinned to.

    Anthropic-compatible gateways can silently substitute a model: the z.ai endpoint
    answers a ``glm-5.2`` request with ``glm-5.3`` at HTTP 200 with no warning, so
    pinning the *requested* id does not pin the model that produced the text. A run
    that mixes served models cannot support a paired contrast, so this failure is
    fatal by design: it is re-raised out of :func:`run_arm` instead of being folded
    into an ``EXECUTION_FAILED_MODEL_RESPONSE`` envelope, and the arm exits non-zero.
    """


def assert_served_model(served: str) -> None:
    """Fail closed unless the served model id matches the pinned one exactly.

    A run is pinned by setting ``ORION_ARM_SERVED_MODEL``. When it is unset the
    assertion is inactive (unpinned exploratory runs keep working), but a pinned run
    rejects every substitution, including an empty id, a differently-cased id and a
    neighbouring model in the same family.
    """
    expected = os.environ.get("ORION_ARM_SERVED_MODEL", "").strip()
    if not expected:
        return
    if served != expected:
        raise ServedModelMismatch(
            f"served model {served!r} != pinned ORION_ARM_SERVED_MODEL {expected!r}"
        )


def _json_object(text: str) -> dict[str, Any]:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("model did not return a JSON object")
    # strict=False: the model emits literal newlines inside JSON string values, which
    # the default strict decoder rejects ("Invalid control character at line N") even
    # though it decodes to the identical object.  E30-R11 diagnosed this as one of two
    # execution-lane failure signatures and repaired it campaign-locally
    # (E30_R11_EXECUTION_LANE_THINKING_BUDGET_JSON_STRICT_REPAIR, 4 of 13 stuck cells);
    # the repair never reached main, so every later run inherits the defect.  It is a
    # decoder tolerance only: same bytes, same Python object, and prompts, schema,
    # model, temperature, arm structure and scoring are untouched.
    value = json.loads(text[start : end + 1], strict=False)
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


def _parse_patch(text: str, workspace: Path | None = None) -> tuple[Any, str, list[str], Any, list[str], str]:
    """Parse the model JSON and emit an apply-clean unified diff.

    The diff is canonicalized at emission (see ``orion_v2.patch_emission``) so the
    harness measures reasoning rather than hunk-header arithmetic. The emission is
    gold-blind: only the solver workspace the arm already reads is consulted.
    """
    data = _json_object(text)
    patch = data.get("patch")
    if not isinstance(patch, str):
        raise ValueError("model JSON lacks a unified diff patch")
    try:
        emission = emit_apply_clean_patch(patch, workspace=workspace)
    except PatchEmissionError as exc:
        raise ValueError(f"model JSON lacks a unified diff patch: {exc}") from exc
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
    return emission, diagnosis, assumptions, data.get("uncertainty", "UNRESOLVED"), tests, falsifier


def arm_call_count(arm: str) -> int:
    if arm in {"F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"} or arm.startswith("F2_"):
        return 3
    if arm == "SAME_MODEL_REFLECTION":
        return 2
    return 1


def _solver_workspace(request: dict[str, Any]) -> Path | None:
    raw = str(request.get("task", {}).get("solver_workspace", "")).strip()
    if not raw:
        return None
    workspace = Path(raw)
    return workspace if workspace.is_dir() else None


def run_arm(
    request: dict[str, Any],
    *,
    call: Callable[[str], tuple[str, dict[str, int]]],
    workspace_context: str,
) -> dict[str, Any]:
    arm = str(request["arm_id"])
    workspace = _solver_workspace(request)
    calls: list[dict[str, int]] = []
    served_models: set[str] = set()

    def ask(prompt: str) -> str:
        if calls:
            delay = float(os.environ.get("ORION_MIN_SECONDS_BETWEEN_CALLS", "0"))
            if delay > 0:
                time.sleep(delay)
        text, usage = call(prompt)
        calls.append({"input_tokens": int(usage.get("input_tokens", 0)), "output_tokens": int(usage.get("output_tokens", 0))})
        served = str(usage.get("_served_model", "")).strip()
        if served:
            served_models.add(served)
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
            ingest_label = (
                "INGEST only; decomposition and source-bound sorting are removed"
                if arm == "F2_MINUS_DECOMPOSITION"
                else "INGEST/DECOMPOSE/SORT"
            )
            reconstruct_label = (
                "REDUCE/ABSORB/RECOMBINE without native-parent reconstruction"
                if arm == "F2_MINUS_NATIVE_RECOVERY"
                else "NATIVE_RECONSTRUCT/REDUCE/ABSORB/RECOMBINE"
            )
            ingest = ask(_stage_prompt(ingest_label, workspace_context))
            reconstruct = ask(_stage_prompt(reconstruct_label, workspace_context, ingest))
            final_prior = ingest + "\n\n" + reconstruct
            if arm == "F2_MINUS_COUNTERPROBE":
                final_prior += "\n\nABLATION: produce the final proposal without a challenge/counterprobe cycle."
            elif arm == "F2_MINUS_SELECTIVE_REOPEN":
                final_prior += "\n\nABLATION: use a flat global update; do not selectively reopen a rejected support family."
            challenge = ask(_final_prompt(workspace_context, final_prior))
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
        emission, diagnosis, assumptions, uncertainty, tests, falsifier = _parse_patch(final, workspace)
        response: dict[str, Any] = {
            "schema_version": "orion.v2.agent-response.v1", "task_id": request["task_id"], "arm_id": arm,
            "status": "COMPLETED_PROPOSAL_ONLY", "proposed_patch_or_artifact": {"type": "unified_diff", "content": emission.patch},
            "patch_emission_receipt": emission.receipt, "diagnosis": diagnosis, "source_ids_used": ["gold-blind-solver-workspace"], "assumptions": assumptions,
            "uncertainty": uncertainty, "discriminator_or_tests": tests, "falsifier": falsifier,
            "requested_authority": "EXECUTION_TEST_ONLY", "scientific_truth_authorized": False,
            "field_status_authorized": False, "publication_readiness_authorized": False,
            "resource_receipt": {"model_calls": len(calls), "input_tokens": sum(x["input_tokens"] for x in calls), "output_tokens": sum(x["output_tokens"] for x in calls), "served_model_ids": sorted(served_models)},
        }
        if stages is not None:
            response["metabolic_stages"] = stages
        if arm.startswith("F2_MINUS_"):
            response["component_removal"] = {
                "F2_MINUS_DECOMPOSITION": ["DECOMPOSE", "SORT"],
                "F2_MINUS_NATIVE_RECOVERY": ["NATIVE_RECONSTRUCT"],
                "F2_MINUS_COUNTERPROBE": ["CHALLENGE", "COUNTERPROBE"],
                "F2_MINUS_SELECTIVE_REOPEN": ["SELECTIVE_REOPEN"],
            }.get(arm, [])
        return response
    except ServedModelMismatch:
        # Fatal by design: a mixed-served-model campaign cannot support a paired
        # contrast, so this propagates and the arm exits non-zero rather than
        # writing an envelope that a later stage might treat as merely retryable.
        raise
    except (ValueError, RuntimeError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return {
            "schema_version": "orion.v2.agent-response.v1", "task_id": request["task_id"], "arm_id": arm,
            "status": "EXECUTION_FAILED_MODEL_RESPONSE", "proposed_patch_or_artifact": None, "diagnosis": str(exc),
            "source_ids_used": [], "assumptions": [], "uncertainty": "UNRESOLVED", "discriminator_or_tests": [],
            "falsifier": "repair the bound provider response and rerun under a new identity", "requested_authority": "NONE",
            "scientific_truth_authorized": False, "field_status_authorized": False, "publication_readiness_authorized": False,
            "resource_receipt": {"model_calls": len(calls), "input_tokens": sum(x["input_tokens"] for x in calls), "output_tokens": sum(x["output_tokens"] for x in calls), "served_model_ids": sorted(served_models)},
        }


def _urlopen_with_retry(req: urllib.request.Request, *, timeout: int) -> Any:
    attempts = int(os.environ.get("ORION_ARM_HTTP_RETRIES", "8"))
    for attempt in range(attempts):
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as exc:
            if exc.code in {429, 503} and attempt + 1 < attempts:
                time.sleep(min(120.0, 2.0 ** attempt))
                continue
            raise
    raise RuntimeError("HTTP retries exhausted")


def _anthropic_compatible_call(prompt: str) -> tuple[str, dict[str, int]]:
    base = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
    url = base + ("/messages" if base.endswith("/v1") else "/v1/messages")
    body = json.dumps({"model": os.environ["ANTHROPIC_MODEL"], "max_tokens": int(os.environ.get("ORION_ARM_MAX_TOKENS", "6000")), "temperature": 0, "system": "You are a bounded experimental software-debugging arm.", "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(url, data=body, headers={"x-api-key": os.environ["ANTHROPIC_AUTH_TOKEN"], "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with _urlopen_with_retry(req, timeout=int(os.environ.get("ORION_ARM_HTTP_TIMEOUT", "1800"))) as raw:
        data = json.load(raw)
    text = "".join(str(x.get("text", "")) for x in data.get("content", []) if isinstance(x, dict))
    served = str(data.get("model", ""))
    assert_served_model(served)  # fail closed on silent model substitution
    usage = dict(data.get("usage", {}))
    usage["_served_model"] = served
    return text, usage


def _gemini_call(prompt: str) -> tuple[str, dict[str, int]]:
    """Call the versioned Google Generative Language API without an SDK."""
    model = os.environ["ORION_GEMINI_MODEL"].removeprefix("models/")
    key = os.environ["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    max_tokens = int(os.environ.get("ORION_ARM_MAX_TOKENS", "6000"))
    generation_config: dict[str, Any] = {
        "temperature": 0,
        "maxOutputTokens": max_tokens,
        "thinkingConfig": {"thinkingBudget": min(1024, max(0, max_tokens // 3))},
    }
    if "Return only one JSON object" in prompt:
        generation_config["responseMimeType"] = "application/json"
    body = json.dumps({
        "systemInstruction": {"parts": [{"text": "You are a bounded experimental software-debugging arm."}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": generation_config,
    }).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"content-type": "application/json", "x-goog-api-key": key},
    )
    with _urlopen_with_retry(req, timeout=int(os.environ.get("ORION_ARM_HTTP_TIMEOUT", "1800"))) as raw:
        data = json.load(raw)
    text = "".join(
        str(part.get("text", ""))
        for candidate in data.get("candidates", []) if isinstance(candidate, dict)
        for part in candidate.get("content", {}).get("parts", []) if isinstance(part, dict)
    )
    usage = data.get("usageMetadata", {})
    return text, {
        "input_tokens": int(usage.get("promptTokenCount", 0)),
        "output_tokens": int(usage.get("candidatesTokenCount", 0)),
    }


def _provider_call(prompt: str) -> tuple[str, dict[str, int]]:
    provider = os.environ.get("ORION_MODEL_PROVIDER", "anthropic_compatible").strip().lower()
    if provider == "gemini":
        return _gemini_call(prompt)
    if provider == "anthropic_compatible":
        return _anthropic_compatible_call(prompt)
    raise ValueError(f"unsupported ORION_MODEL_PROVIDER: {provider}")


def _context(request: dict[str, Any]) -> str:
    task = request.get("task", {})
    workspace = Path(str(task.get("solver_workspace", "")))
    listing: list[str] = []
    snapshots: list[dict[str, str]] = []
    if workspace.is_dir():
        candidates = [
            path for path in workspace.rglob("*.py")
            if ".git" not in path.parts and not any(part in {"venv", ".venv", "site-packages"} for part in path.parts)
        ]
        listing = [path.relative_to(workspace).as_posix() for path in sorted(candidates)]
        baseline = json.dumps(task.get("baseline_observation", {}), sort_keys=True)

        def priority(path: Path) -> tuple[int, int, str]:
            relative = path.relative_to(workspace).as_posix()
            mentioned = relative in baseline or path.name in baseline
            is_test = bool(re.search(r"(^|/)(tests?|test_[^/]*)($|/)", relative))
            try:
                size = path.stat().st_size
            except OSError:
                size = 10**12
            return (0 if mentioned else 1 if is_test else 2, size, relative)

        remaining = int(os.environ.get("ORION_CONTEXT_MAX_CHARS", "120000"))
        per_file = int(os.environ.get("ORION_CONTEXT_MAX_FILE_CHARS", "30000"))
        for path in sorted(candidates, key=priority):
            if remaining <= 0:
                break
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            content = content[: min(per_file, remaining)]
            snapshots.append({"path": path.relative_to(workspace).as_posix(), "content": content})
            remaining -= len(content)
    return json.dumps({
        "task": task,
        "python_files": listing,
        "source_snapshots": snapshots,
        "source_snapshot_truncation": {
            "max_total_chars": int(os.environ.get("ORION_CONTEXT_MAX_CHARS", "120000")),
            "max_file_chars": int(os.environ.get("ORION_CONTEXT_MAX_FILE_CHARS", "30000")),
        },
        "gold_access": "NONE",
        "network_allowed_during_solution": False,
    }, indent=2, sort_keys=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text())
    total = os.environ.get("ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET", "").strip()
    if total:
        os.environ["ORION_ARM_MAX_TOKENS"] = str(max(1, int(total) // arm_call_count(str(request["arm_id"]))))
    start = time.time()
    response = run_arm(request, call=_provider_call, workspace_context=_context(request))
    response["resource_receipt"]["wall_time_seconds"] = time.time() - start
    args.response.parent.mkdir(parents=True, exist_ok=True)
    args.response.write_text(json.dumps(response, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
