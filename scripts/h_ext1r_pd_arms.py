#!/usr/bin/env python3
"""H-EXT-1R model arms over the registered Anthropic-compatible channel.

One process per request, the same envelope as ``scripts/orion_pd_arms.py`` (which is
imported READ-ONLY for its prompt and arm procedures, so every arm sees byte-identical
task text and differs only in its registered ARM PROCEDURE sentence).  What this
executor adds is the channel discipline E30-R13 registered and H-EXT-1 could not
have: the request body is a frozen contract (``ORION_ARM_CHANNEL_CONTRACT``), the
served model id is asserted against a pin (``ORION_ARM_SERVED_MODEL``, fail closed),
and every response carries a channel receipt (contract sha256, stop reason, text
length, tokens) so a homogeneity gate can read the condition off the envelopes.

Nothing here reads the private oracle: the dispatcher removes it before any call and
the request carries the public task only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PD = _load("orion_pd_arms_ro", ROOT / "scripts" / "orion_pd_arms.py")
CH = _load("orion_claude_arms_ro", ROOT / "scripts" / "orion_claude_arms.py")

SYSTEM_PROMPT = "You are a bounded experimental evidence-evaluation arm."
JSON_INSTRUCTION = (
    "\nReturn only one JSON object with keys answer, reasoning_summary, falsifier and no "
    "Markdown fence. `answer` may be the JSON-encoded string described above or the "
    "decoded object itself; either way it must carry EXACTLY the keys of answer_contract."
)


def prompt(req: dict[str, Any]) -> str:
    return PD.prompt(req) + JSON_INSTRUCTION


def _normalise_answer(raw: Any) -> Any:
    if isinstance(raw, str):
        return json.loads(raw)
    return raw


def execute(req: dict[str, Any]) -> dict[str, Any]:
    if str(req["arm_id"]) in PD.OFFLINE_ARMS:
        raise RuntimeError("offline parents are not registered in H-EXT-1R")
    for required in ("ORION_ARM_CHANNEL_CONTRACT", "ORION_ARM_SERVED_MODEL", "ANTHROPIC_MODEL",
                     "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ORION_ARM_MAX_TOKENS"):
        if not os.environ.get(required):
            raise RuntimeError(f"MISSING_ENV {required}: the registered channel condition is not set")
    CH.ARM_SYSTEM_PROMPT = SYSTEM_PROMPT
    started = time.time()
    text, usage = CH._anthropic_compatible_call(prompt(req))
    data = CH._json_object(text)
    contract = req["task"].get("answer_contract", {})
    answer = _normalise_answer(data.get("answer"))
    if not isinstance(answer, dict):
        raise ValueError("decoded answer is not an object")
    if set(answer) != set(contract):
        raise ValueError(f"answer keys {sorted(answer)} do not match contract {sorted(contract)}")
    return {
        "schema_version": "orion.v2.dependence-evidence-response.v1",
        "task_id": req["task_id"], "arm_id": req["arm_id"], "status": "COMPLETED_PROPOSAL_ONLY",
        "answer": answer,
        "reasoning_summary": str(data.get("reasoning_summary", "")),
        "falsifier": str(data.get("falsifier", "")),
        "resource_receipt": {
            "model_calls": 1, "wall_time_seconds": time.time() - started,
            "executor": "anthropic-compatible-http",
            "requested_model": os.environ["ANTHROPIC_MODEL"],
            "served_model_ids": [str(usage.get("_served_model", ""))],
            "input_tokens": int(usage.get("input_tokens", 0)),
            "output_tokens": int(usage.get("output_tokens", 0)),
        },
        "channel_receipt": {
            "contract_id": str(usage.get("_channel_contract_id", "")),
            "contract_sha256": str(usage.get("_channel_contract_sha256", "")),
            "stop_reason": str(usage.get("_stop_reason", "")),
            "text_chars": int(usage.get("_text_chars", 0)),
            "system_prompt": SYSTEM_PROMPT,
            "max_tokens": int(os.environ["ORION_ARM_MAX_TOKENS"]),
        },
        "scientific_truth_authorized": False, "legitimate_authority_authorized": False,
        "publication_readiness_authorized": False,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--request", type=Path, required=True)
    p.add_argument("--response", type=Path, required=True)
    a = p.parse_args()
    req = json.loads(a.request.read_text())
    try:
        out = execute(req)
    except Exception as exc:  # the failure envelope is data, never a verdict
        out = {"schema_version": "orion.v2.dependence-evidence-response.v1", "task_id": req.get("task_id"),
               "arm_id": req.get("arm_id"), "status": "EXECUTION_FAILED_MODEL_RESPONSE", "answer": None,
               "reasoning_summary": f"{type(exc).__name__}: {exc}"[:2000],
               "falsifier": "repair execution binding and rerun under a new identity",
               "resource_receipt": {"model_calls": 0},
               "scientific_truth_authorized": False, "legitimate_authority_authorized": False,
               "publication_readiness_authorized": False}
    a.response.parent.mkdir(parents=True, exist_ok=True)
    a.response.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
