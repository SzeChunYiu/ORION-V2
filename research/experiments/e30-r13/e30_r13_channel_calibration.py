#!/usr/bin/env python3
"""E30-R13 channel calibration probe -- instrument measurement, NOT an endpoint read.

E30-R12 halted at ``EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ`` because the bound
z.ai Anthropic-compatible channel spent the entire registered output budget on a
thinking block before emitting any text, at an unchanged served model id.  Its
registered escalated budget (36 000) was derived from a *single* smoke measurement
that turned out to be an order of magnitude off.

This probe exists so E30-R13's request-body contract and its output-token budgets are
**derived from measurement over every call shape the campaign actually issues**, with
replicates, rather than inherited or inferred.

What it records, per model call: the request-body contract fingerprint, the HTTP
``stop_reason``, input/output token counts, every content block's ``type`` and
character count, whether a JSON object is parseable out of the concatenated ``text``
blocks, and wall time.

What it deliberately does NOT do:

* it never writes into a campaign ``run/`` tree -- output goes only to ``--out``;
* it never evaluates a patch, never touches a gold tree, and never reads an endpoint;
* it discards every model response body, keeping only accounting, block shape and a
  parseability boolean (plus the parsed object's key names, which carry no repair
  content).

Custody precedent: E30-R12 archived ``E30_R12_CHANNEL_BEHAVIOUR_PROBE_V1.json`` and
``E30_R12_ESCALATED_BUDGET_BLOCK_PROBE_V1.json`` the same way -- frozen prompts, run
outside the campaign tree, accounting only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# The registered contract candidates.  Each is the request body MINUS model, max_tokens
# and messages; the fingerprint below is taken over exactly this object, so a contract
# is identified by bytes rather than by a description of it.
CONTRACTS: dict[str, dict[str, Any]] = {
    "provider_default": {},
    "thinking_disabled": {"thinking": {"type": "disabled"}},
    "thinking_enabled_2048": {"thinking": {"type": "enabled", "budget_tokens": 2048}},
}

SYSTEM_PROMPT = "You are a bounded experimental software-debugging arm."

ARMS = ("SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL")


def contract_fingerprint(name: str) -> str:
    """sha256 over the canonical contract object -- the bytes, not a label for them."""
    payload = {
        "contract_id": name,
        "system": SYSTEM_PROMPT,
        "temperature": 0,
        "extra_body": CONTRACTS[name],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def call_channel(
    prompt: str, *, contract: str, max_tokens: int, model: str, timeout: int
) -> dict[str, Any]:
    """One instrumented call.  Returns accounting only; the response text is discarded."""
    base = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
    url = base + ("/messages" if base.endswith("/v1") else "/v1/messages")
    payload: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
    }
    payload.update(CONTRACTS[contract])
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "x-api-key": os.environ["ANTHROPIC_AUTH_TOKEN"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as raw:
            data = json.load(raw)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "contract_id": contract,
            "contract_sha256": contract_fingerprint(contract),
            "max_tokens_requested": max_tokens,
            "transport_error": f"{type(exc).__name__}: {exc}",
            "wall_seconds": round(time.time() - started, 2),
        }
    wall = round(time.time() - started, 2)

    blocks = [b for b in data.get("content", []) if isinstance(b, dict)]
    text = "".join(str(b.get("text", "")) for b in blocks)
    start, end = text.find("{"), text.rfind("}")
    parsed_keys: list[str] = []
    parseable = False
    if start >= 0 and end > start:
        try:
            obj = json.loads(text[start : end + 1], strict=False)
            parseable = isinstance(obj, dict)
            if parseable:
                parsed_keys = sorted(str(k) for k in obj)
        except json.JSONDecodeError:
            parseable = False
    usage = data.get("usage", {}) or {}
    return {
        "contract_id": contract,
        "contract_sha256": contract_fingerprint(contract),
        "max_tokens_requested": max_tokens,
        "served_model": str(data.get("model", "")),
        "stop_reason": data.get("stop_reason"),
        "input_tokens": int(usage.get("input_tokens", 0) or 0),
        "output_tokens": int(usage.get("output_tokens", 0) or 0),
        "blocks": [
            # A block's payload lives under a key equal to its own type: a ``text``
            # block carries ``text``, a ``thinking`` block carries ``thinking``.
            {"type": str(b.get("type", "")), "chars": len(str(b.get(str(b.get("type", "")), "") or ""))}
            for b in blocks
        ],
        "text_chars": len(text),
        "json_object_parseable": parseable,
        "parsed_top_level_keys": parsed_keys,
        "wall_seconds": wall,
    }


def build_prompts(arms_module: Any, request: dict[str, Any], arm: str) -> list[tuple[str, str]]:
    """The exact prompt sequence ``run_arm`` issues for ``arm``, without calling out.

    Prior-stage text is unavailable without actually running the arm, so multi-call
    shapes are reconstructed with a prior placeholder of the size the stage would
    plausibly carry.  Stage prompts are dominated by the workspace context (~10^5
    chars), so this changes the input size by well under a percent -- and the probe
    reports measured ``input_tokens`` per call, so the assumption is checkable rather
    than assumed.
    """
    context = arms_module._context(request)
    final = arms_module._final_prompt
    stage = arms_module._stage_prompt
    prior = "PLACEHOLDER PRIOR STAGE OUTPUT. " * 200  # ~6 kB, a realistic stage carry
    if arm == "SIMPLE_DIRECT":
        return [("final", final(context))]
    if arm == "SAME_MODEL_REFLECTION":
        return [("draft", stage("same-model draft diagnosis", context)), ("final", final(context, prior))]
    if arm == "F0_PARENT_FEDERATION":
        return [
            ("parent_a", stage("native parent diagnosis A", context)),
            ("parent_b", stage("native parent diagnosis B", context)),
            ("final", final(context, prior + "\n\n" + prior)),
        ]
    if arm == "F2_ORION_METABOLIC_FULL":
        return [
            ("ingest", stage("INGEST/DECOMPOSE/SORT", context)),
            ("reconstruct", stage("NATIVE_RECONSTRUCT/REDUCE/ABSORB/RECOMBINE", context, prior)),
            ("challenge", final(context, prior + "\n\n" + prior)),
        ]
    raise ValueError(f"unknown arm {arm}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True, help="ORION-V2 tree to import the arms from")
    ap.add_argument("--requests-root", type=Path, required=True, help="a confirmatory-rN/requests directory")
    ap.add_argument("--tasks", required=True, help="comma-separated task ids")
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--contracts", default="thinking_disabled")
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--max-tokens", type=int, default=16000, help="headroom so natural length is observed, not truncated")
    ap.add_argument("--model", default=os.environ.get("ANTHROPIC_MODEL", "glm-5.3"))
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    sys.path.insert(0, str(args.source / "scripts"))
    sys.path.insert(0, str(args.source / "src"))
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "orion_claude_arms_probe", args.source / "scripts" / "orion_claude_arms.py"
    )
    assert spec and spec.loader
    arms_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arms_module)

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    contracts = [c.strip() for c in args.contracts.split(",") if c.strip()]
    for contract in contracts:
        if contract not in CONTRACTS:
            print(f"UNKNOWN_CONTRACT {contract}", file=sys.stderr)
            return 2

    records: list[dict[str, Any]] = []
    for contract in contracts:
        for task in tasks:
            for arm in arms:
                request_path = args.requests_root / arm / f"{task}.json"
                if not request_path.is_file():
                    print(f"MISSING_REQUEST {request_path}", file=sys.stderr)
                    return 3
                request = json.loads(request_path.read_text())
                prompts = build_prompts(arms_module, request, arm)
                for rep in range(1, args.reps + 1):
                    for index, (stage_id, prompt) in enumerate(prompts):
                        record = call_channel(
                            prompt,
                            contract=contract,
                            max_tokens=args.max_tokens,
                            model=args.model,
                            timeout=args.timeout,
                        )
                        record.update(
                            {
                                "task_id": task,
                                "arm_id": arm,
                                "call_index": index,
                                "stage_id": stage_id,
                                "replicate": rep,
                                "prompt_chars": len(prompt),
                                "arm_call_count": arms_module.arm_call_count(arm),
                            }
                        )
                        records.append(record)
                        print(
                            f"{contract} {task} {arm} rep{rep} call{index}({stage_id}) "
                            f"stop={record.get('stop_reason')} out={record.get('output_tokens')} "
                            f"text={record.get('text_chars')} json={record.get('json_object_parseable')} "
                            f"wall={record.get('wall_seconds')}",
                            flush=True,
                        )

    per_contract: dict[str, Any] = {}
    for contract in contracts:
        rows = [r for r in records if r["contract_id"] == contract and "transport_error" not in r]
        if not rows:
            per_contract[contract] = {"calls": 0, "note": "no successful calls"}
            continue
        outs = [r["output_tokens"] for r in rows]
        walls = [r["wall_seconds"] for r in rows]
        final_rows = [r for r in rows if r["stage_id"] in {"final", "challenge"}]
        per_contract[contract] = {
            "contract_sha256": contract_fingerprint(contract),
            "calls": len(rows),
            "transport_errors": len([r for r in records if r["contract_id"] == contract and "transport_error" in r]),
            "stop_reasons": {s: sum(1 for r in rows if r["stop_reason"] == s) for s in sorted({str(r["stop_reason"]) for r in rows})},
            "output_tokens": {
                "min": min(outs), "median": statistics.median(outs), "max": max(outs),
                "mean": round(statistics.mean(outs), 1),
            },
            "wall_seconds": {"min": min(walls), "median": statistics.median(walls), "max": max(walls)},
            "text_chars_zero_calls": sum(1 for r in rows if r["text_chars"] == 0),
            "json_parseable_final_calls": f"{sum(1 for r in final_rows if r['json_object_parseable'])}/{len(final_rows)}",
            "served_model_ids": sorted({r["served_model"] for r in rows}),
            "per_arm_max_output_tokens": {
                arm: max([r["output_tokens"] for r in rows if r["arm_id"] == arm], default=None)
                for arm in sorted({r["arm_id"] for r in rows})
            },
        }

    payload = {
        "schema_version": "orion.v2.e30-r13-channel-calibration.v1",
        "purpose": "derive the E30-R13 request-body contract and output-token budgets from measurement",
        "is_an_endpoint_read": False,
        "wrote_into_a_campaign_run_tree": False,
        "response_text_retained": False,
        "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "parameters": {
            "source": str(args.source), "requests_root": str(args.requests_root),
            "tasks": tasks, "arms": arms, "contracts": contracts, "replicates": args.reps,
            "max_tokens_headroom": args.max_tokens, "requested_model": args.model,
        },
        "contract_definitions": {c: {"extra_body": CONTRACTS[c], "sha256": contract_fingerprint(c)} for c in contracts},
        "summary": per_contract,
        "calls": records,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"CALIBRATION_WRITTEN {args.out} calls={len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
