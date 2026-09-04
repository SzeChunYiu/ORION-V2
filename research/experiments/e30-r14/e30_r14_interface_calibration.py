#!/usr/bin/env python3
"""E30-R14 interface calibration -- instrument measurement, NOT an endpoint read.

E30-R13 completed every envelope under a registered channel contract and still could
not test repair: 346 of 480 emitted diffs did not apply.  The read-only attribution of
those envelopes (``results/E30_R14_R13_APPLY_FAILURE_ATTRIBUTION_V1.json``) split the
failure between two halves of the arm<->workspace interface: *presentation* (the model
edits code the 30 000-character per-file snapshot never showed it) and *emission* (the
model cannot reproduce verbatim context and line arithmetic, and emits diff forms the
frozen canonicalizer refuses).

This probe crosses the two axes on the cheapest arm so that E30-R14's registered
interface is a MEASURED choice with the attribution archived, exactly as E30-R13's
request-body contract was chosen from a measured three-way contrast:

    edit interface     x  presentation policy
    unified_diff          per_file_cap            (E30-R13's condition)
    unified_diff          mentioned_files_full
    anchored_edits        per_file_cap
    anchored_edits        mentioned_files_full    (the candidate R14 condition)

Per call it records: condition, emission status, apply-check outcome, edit counts and
match modes, unlocated-edit reasons, the presentation summary (files shown, mentioned
files truncated, context chars), the channel receipt (contract sha256, stop reason,
tokens), served model id and wall time.

What it deliberately does NOT do:

* it never writes into a campaign ``run/`` tree -- output goes only to ``--out``;
* it never evaluates a patch, never runs a test, never touches a gold tree, never reads
  an endpoint;
* it discards the model's patch text, diagnosis and every other response field, keeping
  only the receipts and an apply-ability boolean.  Apply-ability is a property of the
  interface, not of the repair, and it is the only thing measured here.

The apply check inside the arms (``git apply --check``) is non-mutating and runs against
the frozen gold-blind solver workspaces the requests already name.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import importlib.util
import json
import os
import statistics
import sys
import time
from pathlib import Path
from typing import Any

CONDITIONS: tuple[tuple[str, str], ...] = (
    ("unified_diff", "per_file_cap"),
    ("unified_diff", "mentioned_files_full"),
    ("anchored_edits", "per_file_cap"),
    ("anchored_edits", "mentioned_files_full"),
)

DISCARDED_FIELDS = ("proposed_patch_or_artifact", "diagnosis", "assumptions", "uncertainty",
                    "discriminator_or_tests", "falsifier", "metabolic_stages")


def load_arms(source: Path):
    sys.path.insert(0, str(source / "src"))
    spec = importlib.util.spec_from_file_location("orion_claude_arms_calibration",
                                                  source / "scripts" / "orion_claude_arms.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def one_call(arms, request: dict[str, Any], interface: str, presentation: str) -> dict[str, Any]:
    os.environ["ORION_EDIT_INTERFACE"] = interface
    os.environ["ORION_PRESENTATION_POLICY"] = presentation
    started = time.time()
    context = arms._context(request)
    context_chars = len(context)
    try:
        response = arms.run_arm(request, call=arms._provider_call, workspace_context=context)
    except Exception as exc:  # a served-model mismatch is fatal in the campaign; here it is recorded
        return {"task_id": request["task_id"], "arm_id": request["arm_id"], "interface": interface,
                "presentation": presentation, "status": "CALL_RAISED", "error": f"{type(exc).__name__}: {exc}"[:500],
                "wall_seconds": round(time.time() - started, 2), "context_chars": context_chars}
    receipt = response.get("patch_emission_receipt") or {}
    record = {
        "task_id": request["task_id"], "arm_id": request["arm_id"],
        "interface": interface, "presentation": presentation,
        "status": response.get("status"),
        "emission_status": receipt.get("emission_status"),
        "emitted_apply_check": receipt.get("emitted_apply_check"),
        "applies": receipt.get("emission_status") == "APPLY_CLEAN_BY_CONSTRUCTION",
        "edit_interface": receipt.get("edit_interface", "unified_diff"),
        "edit_count": receipt.get("edit_count"),
        "edits_located": receipt.get("edits_located"),
        "edit_origins": receipt.get("edit_origins"),
        "match_modes": receipt.get("match_modes"),
        "unlocated_reasons": sorted({str(f.get("reason")) for f in receipt.get("unlocated_edits", [])}),
        "canonicalizer_rejection_reasons": receipt.get("canonicalizer_rejection_reasons"),
        "apply_check_error_head": (receipt.get("emitted_apply_check_error") or "")[:160],
        "interface_receipt": response.get("interface_receipt"),
        "channel_receipt": response.get("channel_receipt"),
        "resource_receipt": response.get("resource_receipt"),
        "envelope_failure": response.get("diagnosis") if response.get("status") != "COMPLETED_PROPOSAL_ONLY" else None,
        "wall_seconds": round(time.time() - started, 2),
        "context_chars": context_chars,
    }
    for key in DISCARDED_FIELDS:
        response.pop(key, None)
    return record


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for interface, presentation in CONDITIONS:
        rows = [r for r in records if r["interface"] == interface and r["presentation"] == presentation]
        done = [r for r in rows if r.get("status") == "COMPLETED_PROPOSAL_ONLY"]
        applied = [r for r in done if r.get("applies")]
        outs = [int((r.get("resource_receipt") or {}).get("output_tokens", 0)) for r in done]
        ins = [int((r.get("resource_receipt") or {}).get("input_tokens", 0)) for r in done]
        statuses: dict[str, int] = {}
        for r in rows:
            key = str(r.get("emission_status") or r.get("status"))
            statuses[key] = statuses.get(key, 0) + 1
        reasons: dict[str, int] = {}
        for r in done:
            for reason in r.get("unlocated_reasons") or []:
                reasons[reason] = reasons.get(reason, 0) + 1
        out[f"{interface}|{presentation}"] = {
            "calls": len(rows), "completed_envelopes": len(done),
            "applied": len(applied),
            "apply_rate": (len(applied) / len(done)) if done else None,
            "apply_failure_rate": (1 - len(applied) / len(done)) if done else None,
            "emission_statuses": statuses,
            "unlocated_reasons": reasons,
            "stop_reasons": _count(r.get("channel_receipt", {}).get("stop_reasons", []) for r in done),
            "contract_sha256s": _count(r.get("channel_receipt", {}).get("contract_sha256s", []) for r in done),
            "served_model_ids": _count((r.get("resource_receipt") or {}).get("served_model_ids", []) for r in done),
            "interface_sha256s": sorted({(r.get("interface_receipt") or {}).get("edit_interface_sha256", "") for r in done}),
            "mentioned_files_truncated_envelopes": sum(
                1 for r in done if ((r.get("interface_receipt") or {}).get("presentation") or {}).get("mentioned_files_truncated", 0) > 0),
            "output_tokens": _dist(outs), "input_tokens": _dist(ins),
            "context_chars": _dist([r["context_chars"] for r in rows]),
            "wall_seconds": _dist([r["wall_seconds"] for r in rows]),
        }
    return out


def _count(seqs) -> dict[str, int]:
    counts: dict[str, int] = {}
    for seq in seqs:
        for value in seq:
            counts[str(value)] = counts.get(str(value), 0) + 1
    return counts


def _dist(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    return {"n": len(values), "min": min(values), "median": statistics.median(values), "max": max(values)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--requests-root", type=Path, required=True, help="a confirmatory-rN/requests directory")
    ap.add_argument("--tasks", required=True, help="comma-separated task ids, or ALL (every request under the arm)")
    ap.add_argument("--arm", default="SIMPLE_DIRECT")
    ap.add_argument("--conditions", default="ALL", help="comma-separated interface|presentation pairs, or ALL")
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    for required in ("ORION_ARM_CHANNEL_CONTRACT", "ORION_ARM_SERVED_MODEL", "ORION_ARM_MAX_TOKENS"):
        if not os.environ.get(required):
            print(f"MISSING_ENV {required}: the calibration must run under the registered channel condition", file=sys.stderr)
            return 2
    arms = load_arms(args.source)
    conditions = list(CONDITIONS) if args.conditions == "ALL" else [
        tuple(c.split("|")) for c in args.conditions.split(",")]
    root = args.requests_root / args.arm
    if args.tasks == "ALL":
        tasks = sorted(p.stem for p in root.glob("*.json"))
    else:
        tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    requests = {t: json.loads((root / f"{t}.json").read_text()) for t in tasks}
    jobs = [(t, i, p) for (i, p) in conditions for t in tasks]
    records: list[dict[str, Any]] = []
    # Conditions are selected through process environment, so each worker is a
    # separate process: threads would race on os.environ.
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.concurrency) as pool:
        futures = {pool.submit(_worker, str(args.source), requests[t], i, p): (t, i, p) for t, i, p in jobs}
        for future in concurrent.futures.as_completed(futures):
            record = future.result()
            records.append(record)
            print(f"{record['interface']}|{record['presentation']} {record['task_id']} "
                  f"status={record.get('status')} emission={record.get('emission_status')} "
                  f"applies={record.get('applies')} ctx={record.get('context_chars')} "
                  f"wall={record.get('wall_seconds')}", flush=True)
            _write(args, arms, conditions, tasks, records)
    _write(args, arms, conditions, tasks, records)
    print(f"CALIBRATION_WRITTEN {args.out} calls={len(records)}")
    return 0


def _worker(source: str, request: dict[str, Any], interface: str, presentation: str) -> dict[str, Any]:
    arms = load_arms(Path(source))
    return one_call(arms, request, interface, presentation)


def _write(args, arms, conditions, tasks, records) -> None:
    payload = {
        "schema_version": "orion.v2.e30-r14-interface-calibration.v1",
        "purpose": "choose E30-R14's registered arm<->workspace interface from a measured 2x2 contrast",
        "is_an_endpoint_read": False,
        "wrote_into_a_campaign_run_tree": False,
        "response_text_retained": False,
        "tests_executed": False,
        "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "parameters": {
            "source": str(args.source), "requests_root": str(args.requests_root),
            "arm": args.arm, "tasks": tasks, "conditions": [f"{i}|{p}" for i, p in conditions],
            "channel_contract": os.environ.get("ORION_ARM_CHANNEL_CONTRACT"),
            "channel_contract_sha256": arms.channel_contract_sha256(os.environ["ORION_ARM_CHANNEL_CONTRACT"]),
            "pinned_served_model": os.environ.get("ORION_ARM_SERVED_MODEL"),
            "per_call_max_tokens": int(os.environ["ORION_ARM_MAX_TOKENS"]),
        },
        "interface_definitions": {
            f"{i}|{p}": _fingerprint(arms, i, p) for i, p in conditions
        },
        "summary": summarize(records),
        "calls": sorted(records, key=lambda r: (r["interface"], r["presentation"], r["task_id"])),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _fingerprint(arms, interface: str, presentation: str) -> dict[str, str]:
    os.environ["ORION_EDIT_INTERFACE"] = interface
    os.environ["ORION_PRESENTATION_POLICY"] = presentation
    return {"edit_interface_sha256": arms.edit_interface_sha256(interface), "presentation": presentation}


if __name__ == "__main__":
    raise SystemExit(main())
