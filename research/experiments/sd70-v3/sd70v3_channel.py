#!/usr/bin/env python3
"""SD70-V3 channel/request-body contract: canaries and drift verdicts.

Why this module exists
----------------------
Pinning a served model id does NOT pin an experimental condition. In the
E30-R12 campaign every envelope recorded the correct served model id and the
campaign still failed: provider-side channel behaviour drifted between runs,
and an identical frozen prompt that had completed in 763 output tokens hit a
6,000-token cap on re-run, the budget consumed by a reasoning block the arm
never reads. Registering a channel contract ONCE at freeze would not have
caught that, because the drift happened BETWEEN runs and nothing re-measured.

So the contract is measured at campaign START and again at campaign END, on
byte-frozen canary prompts that carry no task surface and no oracle. Because
they touch nothing protected, their tolerance bands may legitimately be
calibrated by repeated pre-freeze dispatch; that calibration is part of the
frozen design and is not a post-outcome change.

Verdicts are deliberately three-valued. `CHANNEL_CONTRACT_UNOBSERVABLE` is
NOT `CHANNEL_CONTRACT_OK`: the served-model manifest is only visible as a
side effect of this CLI failing to decode it, so a server-side fix would make
the scrape go silent. A silent scrape reporting "no drift" would be exactly
the taxonomy-1 failure (a counter that never ran).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

SCHEMA = "orion.v2.sd70-v3.channel-contract.v1"

CONTRACT_OK = "CHANNEL_CONTRACT_OK"
CONTRACT_DRIFT = "CHANNEL_DRIFT_DETECTED"
CONTRACT_UNOBSERVABLE = "CHANNEL_CONTRACT_UNOBSERVABLE"
CONTRACT_FAILED = "CHANNEL_CANARY_DISPATCH_FAILED"

# Byte-frozen canary prompts. Fixed text, no task surface, no oracle content.
CANARY_PROMPTS: dict[str, str] = {
    "CANARY_MINIMAL": (
        "Return the single word OK as the value of the field `token`, and the empty string "
        "as the value of the field `note`. Do not reason beyond what is required.\n"
    ),
    "CANARY_STRUCTURED": (
        "You are a frozen channel canary. Set `token` to the exact string CANARY-STRUCTURED-1 "
        "and set `note` to a single sentence stating that this prompt carries no task data.\n"
    ),
    "CANARY_DELIBERATIVE": (
        "You are a frozen channel canary. Consider the following closed arithmetic statement and "
        "decide whether it is true: the sum of the first ten positive integers equals the product "
        "of five and eleven. Set `token` to TRUE if it is true and FALSE otherwise, and set `note` "
        "to the numeric value of the left-hand side.\n"
    ),
}

CANARY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"token": {"type": "string"}, "note": {"type": "string"}},
    "required": ["token", "note"],
    "additionalProperties": False,
}


def canary_prompt_hashes() -> dict[str, str]:
    return {k: hashlib.sha256(v.encode()).hexdigest() for k, v in sorted(CANARY_PROMPTS.items())}


def dispatch_canary(name: str, model: str, effort: str, timeout: int = 300) -> dict[str, Any]:
    """Dispatch one byte-frozen canary through the identical call form."""
    import sd70v3_model_arm as MA

    prompt = CANARY_PROMPTS[name]
    start = time.time()
    with tempfile.TemporaryDirectory(prefix="orion-sd70v3-canary-") as temp:
        tp = Path(temp)
        cwd = tp / "empty"
        cwd.mkdir()
        schema_path = tp / "schema.json"
        out_path = tp / "output.json"
        schema_path.write_text(json.dumps(CANARY_SCHEMA), encoding="utf-8")
        command = [
            os.environ.get("ORION_CODEX_BIN", "codex"), "exec", "--ephemeral",
            "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check",
            "--sandbox", "read-only", "-C", str(cwd), "--model", model,
            "-c", f'model_reasoning_effort="{effort}"', "--json",
            "--output-schema", str(schema_path), "--output-last-message", str(out_path),
            prompt,
        ]
        completed = subprocess.run(command, text=True, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   timeout=timeout, check=False)
        usage = MA.parse_events(completed.stdout)
        channel = MA.parse_channel_observation(completed.stderr)
        answer = None
        if out_path.exists():
            try:
                answer = json.loads(out_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                answer = None
    return {
        "canary": name,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "prompt_bytes": len(prompt.encode()),
        "model_requested": model,
        "reasoning_effort": effort,
        "returncode": completed.returncode,
        "dispatch_ok": completed.returncode == 0 and answer is not None,
        "answer": answer,
        "wall_time_seconds": time.time() - start,
        "usage": {k: usage.get(k) for k in ("input_tokens", "cached_input_tokens", "output_tokens",
                                            "reasoning_output_tokens", "total_tokens", "usage_source",
                                            "turn_completed", "turn_failed")},
        "channel_observation": channel,
        "observed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def measure(model: str, effort: str, repeats: int = 1) -> dict[str, Any]:
    """One channel measurement: every canary, `repeats` times each."""
    obs = []
    for name in sorted(CANARY_PROMPTS):
        for _ in range(repeats):
            obs.append(dispatch_canary(name, model, effort))
    return {"schema_version": SCHEMA, "model_requested": model, "reasoning_effort": effort,
            "repeats": repeats, "observations": obs,
            "observed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def _by_canary(measurement: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for o in measurement["observations"]:
        out.setdefault(o["canary"], []).append(o)
    return out


def verdict(start: dict[str, Any], end: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    """Compare a start and an end measurement against the frozen contract.

    Returns one of CONTRACT_OK / CONTRACT_DRIFT / CONTRACT_UNOBSERVABLE /
    CONTRACT_FAILED, with the denominator of every check reported alongside
    it so that a zero is never reported without the count it came from.
    """
    checks: list[dict[str, Any]] = []
    unobservable: list[str] = []

    def add(name: str, passed: bool, denominator: int, detail: Any) -> None:
        checks.append({"check": name, "passed": bool(passed), "denominator": denominator, "detail": detail})

    # -- dispatch success --------------------------------------------------
    all_obs = start["observations"] + end["observations"]
    failed = [o["canary"] for o in all_obs if not o["dispatch_ok"]]
    add("canary_dispatch_succeeded", not failed, len(all_obs), {"failed": failed})
    if failed:
        return {"schema_version": SCHEMA, "verdict": CONTRACT_FAILED, "checks": checks,
                "unobservable": unobservable}

    # -- prompt identity (the canaries must be byte-identical across time) --
    frozen_hashes = contract["canary_prompt_sha256"]
    bad = [o["canary"] for o in all_obs if frozen_hashes.get(o["canary"]) != o["prompt_sha256"]]
    add("canary_prompts_byte_identical_to_frozen", not bad, len(all_obs), {"mismatched": bad})

    # -- served manifest identity / observability --------------------------
    obs_with_manifest = [o for o in all_obs if o["channel_observation"]["observable"]]
    if not obs_with_manifest:
        unobservable.append("served_model_manifest_never_observable_in_any_canary")
        add("served_manifest_observable", False, len(all_obs), {"observable_count": 0})
    else:
        add("served_manifest_observable", True, len(all_obs), {"observable_count": len(obs_with_manifest)})
        comps = sorted({o["channel_observation"]["gpt_5_5_comp_hash"] for o in obs_with_manifest})
        add("comp_hash_matches_frozen", comps == [contract["expected_comp_hash"]],
            len(obs_with_manifest), {"observed": comps, "expected": contract["expected_comp_hash"]})
        slugsets = sorted({tuple(o["channel_observation"]["served_slugs_prefix"]) for o in obs_with_manifest})
        add("served_slug_prefix_matches_frozen",
            [list(s) for s in slugsets] == [contract["expected_served_slugs_prefix"]],
            len(obs_with_manifest), {"observed": [list(s) for s in slugsets],
                                     "expected": contract["expected_served_slugs_prefix"]})
        add("target_model_still_advertised",
            all(contract["model"] in o["channel_observation"]["served_slugs_prefix"] for o in obs_with_manifest),
            len(obs_with_manifest), {"model": contract["model"]})

    # -- token-behaviour stability start vs end ----------------------------
    s_by, e_by = _by_canary(start), _by_canary(end)
    bands = contract["canary_bands"]
    drift_rows = []
    for name in sorted(set(s_by) & set(e_by)):
        for field, band_key in (("input_tokens", "input_tokens_abs_tolerance"),
                                ("output_tokens", "output_tokens_abs_tolerance"),
                                ("reasoning_output_tokens", "reasoning_output_tokens_abs_tolerance")):
            sv = [o["usage"][field] for o in s_by[name] if o["usage"][field] is not None]
            ev = [o["usage"][field] for o in e_by[name] if o["usage"][field] is not None]
            if not sv or not ev:
                unobservable.append(f"{name}:{field}:usage_absent")
                drift_rows.append({"canary": name, "field": field, "status": "USAGE_ABSENT"})
                continue
            sm, em = sum(sv) / len(sv), sum(ev) / len(ev)
            tol = bands[name][band_key]
            drift_rows.append({"canary": name, "field": field, "start_mean": sm, "end_mean": em,
                               "abs_delta": abs(em - sm), "tolerance": tol, "within": abs(em - sm) <= tol})
    measured = [r for r in drift_rows if r.get("status") != "USAGE_ABSENT"]
    add("canary_token_behaviour_stable", all(r["within"] for r in measured) and bool(measured),
        len(measured), {"rows": drift_rows})

    # -- canary answers unchanged (behavioural, not just numeric) -----------
    ans_rows = []
    for name in sorted(set(s_by) & set(e_by)):
        st = sorted({o["answer"]["token"] for o in s_by[name]})
        et = sorted({o["answer"]["token"] for o in e_by[name]})
        ans_rows.append({"canary": name, "start_tokens": st, "end_tokens": et, "same": st == et})
    add("canary_answer_tokens_unchanged", all(r["same"] for r in ans_rows), len(ans_rows), {"rows": ans_rows})

    failed_checks = [c["check"] for c in checks if not c["passed"]]
    if unobservable and not [c for c in failed_checks if c != "served_manifest_observable"]:
        v = CONTRACT_UNOBSERVABLE
    elif failed_checks:
        v = CONTRACT_DRIFT
    else:
        v = CONTRACT_OK
    return {"schema_version": SCHEMA, "verdict": v, "checks": checks,
            "failed_checks": failed_checks, "unobservable": unobservable}
