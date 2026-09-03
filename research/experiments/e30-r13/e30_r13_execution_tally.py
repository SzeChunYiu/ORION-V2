#!/usr/bin/env python3
"""E30-R13 execution tally -- descriptive transcription, no endpoint arithmetic.

Written so the figures in the outcome receipt are machine-generated rather than
hand-typed. It reads the campaign's response envelopes and reports what is in them:
statuses, served model ids, channel receipts, stop reasons, token and wall-time
distributions, and the per-arm/per-rep denominators.

It computes **no endpoint, no contrast and no gate**. Everything a terminal depends on
comes from ``e30_r13_analysis.py``, which was frozen before dispatch; this module exists
only so the receipt does not have to quote numbers a human read off a log.

Denominators are published everywhere: a count is always reported against the number of
envelopes it was computed over, so no line here can read as "0 problems" when the real
statement is "0 envelopes examined".
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

ARMS = ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION",
        "F2_ORION_METABOLIC_FULL"]
REPS = ["1", "2", "3"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)

    run = args.campaign / "run"
    tasks = [t["task_id"] for t in json.loads(
        (run / "confirmatory-r1" / "frozen_tasks.json").read_text())["tasks"]]
    expected = len(REPS) * len(ARMS) * len(tasks)

    statuses: Counter[str] = Counter()
    served: Counter[str] = Counter()
    contracts: Counter[str] = Counter()
    stop_reasons: Counter[str] = Counter()
    per_arm: Counter[str] = Counter()
    per_rep: Counter[str] = Counter()
    written = 0
    with_channel_receipt = 0
    calls_total = 0
    calls_reporting_a_contract = 0
    envelopes_with_a_zero_text_call = 0
    output_tokens: list[int] = []
    wall_times: list[float] = []
    max_call_output_tokens: list[int] = []
    failures: list[dict[str, Any]] = []

    for rep in REPS:
        for arm in ARMS:
            for task in tasks:
                path = run / f"confirmatory-r{rep}" / "responses" / arm / f"{task}.json"
                if not path.is_file():
                    statuses["MISSING"] += 1
                    continue
                written += 1
                per_arm[arm] += 1
                per_rep[rep] += 1
                envelope = json.loads(path.read_text())
                status = str(envelope.get("status"))
                statuses[status] += 1
                resource = envelope.get("resource_receipt") or {}
                for value in resource.get("served_model_ids", []) or []:
                    served[str(value)] += 1
                if "output_tokens" in resource:
                    output_tokens.append(int(resource["output_tokens"] or 0))
                if "wall_time_seconds" in resource:
                    wall_times.append(float(resource["wall_time_seconds"]))
                channel = envelope.get("channel_receipt")
                if isinstance(channel, dict):
                    with_channel_receipt += 1
                    calls_total += int(channel.get("model_calls", 0) or 0)
                    calls_reporting_a_contract += int(channel.get("calls_reporting_a_contract", 0) or 0)
                    for value in channel.get("contract_sha256s", []) or []:
                        contracts[str(value)] += 1
                    for value in channel.get("stop_reasons", []) or []:
                        stop_reasons[str(value)] += 1
                    if int(channel.get("calls_with_zero_text_chars", 0) or 0):
                        envelopes_with_a_zero_text_call += 1
                    max_call_output_tokens.append(int(channel.get("max_output_tokens_observed", 0) or 0))
                if status != "COMPLETED_PROPOSAL_ONLY":
                    failures.append({"rep": rep, "arm": arm, "task_id": task,
                                     "status": status,
                                     "diagnosis": str(envelope.get("diagnosis", ""))[:200],
                                     "output_tokens": resource.get("output_tokens"),
                                     "channel_receipt": channel})

    def spread(values: list[Any]) -> dict[str, Any] | None:
        if not values:
            return None
        return {"n": len(values), "min": min(values),
                "median": statistics.median(values), "max": max(values)}

    payload = {
        "schema_version": "orion.v2.e30-r13-execution-tally.v1",
        "computes_no_endpoint_no_contrast_no_gate": True,
        "campaign": str(args.campaign),
        "envelopes_expected": expected,
        "envelopes_written": written,
        "statuses": dict(statuses),
        "per_arm_envelopes": dict(per_arm),
        "per_repetition_envelopes": dict(per_rep),
        "served_model_ids": dict(served),
        "channel_receipts": {
            "envelopes_with_a_channel_receipt": with_channel_receipt,
            "envelopes_expected": expected,
            "model_calls_seen": calls_total,
            "model_calls_reporting_a_contract": calls_reporting_a_contract,
            "contract_sha256_counts": dict(contracts),
            "stop_reason_counts": dict(stop_reasons),
            "envelopes_with_at_least_one_zero_text_call": envelopes_with_a_zero_text_call,
            "largest_single_call_output_tokens": spread(max_call_output_tokens),
        },
        "envelope_output_tokens": spread(output_tokens),
        "envelope_wall_seconds": spread(wall_times),
        "non_completed_envelopes": failures[:50],
        "non_completed_envelope_count": len(failures),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in payload.items() if k != "non_completed_envelopes"},
                     indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
