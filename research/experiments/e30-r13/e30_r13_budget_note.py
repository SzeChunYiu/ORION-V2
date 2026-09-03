#!/usr/bin/env python3
"""E30-R13 budget and feasibility arithmetic -- derived from measurement, no outcome input.

E30-R12's registered budgets (6000 primary, 36 000 escalated) came from E30-R11's
history plus a *single* pre-dispatch smoke measurement, and both turned out to be
inadequate: 116 of 116 execution failures sat at or above the primary cap, and the
escalated budget closed the same cell only marginally, at 35 937 output tokens and
786 s.  This module exists so E30-R13's budget is a function of a measured
distribution over every call shape the campaign issues, with the derivation rule
fixed in code rather than chosen after seeing the number it produces.

It reads only ``e30_r13_channel_calibration.py`` output -- token accounting, stop
reasons and wall times.  It reads no evaluation, no endpoint and no gate.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------- registered constants
#: 4 arms issue 1 + 2 + 3 + 3 = 9 model calls per (task, repetition).
CALLS_PER_TASK_REPETITION = 9
TASKS = 40
REPETITIONS = 3
TOTAL_CALLS = CALLS_PER_TASK_REPETITION * TASKS * REPETITIONS  # 1080, not 480

#: The derivation rule, fixed before the numbers are known: the registered per-call
#: cap is the observed maximum times this multiple, rounded up to the next 1000.
#: A cap derived this way is intended to be NON-BINDING -- the gate that matters is
#: that no envelope stops at ``max_tokens``, not that the cap has a particular value.
SAFETY_MULTIPLE = 4
ROUNDING = 1000

#: SLURM wall clock the campaign's agents job may request, in hours.
SLURM_TIME_LIMIT_HOURS = 24

#: E30-R12's measured provider-default behaviour on the frozen prompt, for the
#: feasibility contrast.  Both figures are transcribed from R12's archived probes.
R12_PROVIDER_DEFAULT_ESCALATED = {
    "source": "research/experiments/e30-r12/results/E30_R12_ESCALATED_BUDGET_BLOCK_PROBE_V1.json",
    "max_tokens": 36000,
    "output_tokens": 35937,
    "wall_seconds": 785.810107,
    "text_chars": 5895,
    "thinking_chars": 161644,
}
R12_PROVIDER_DEFAULT_PRIMARY = {
    "source": "research/experiments/e30-r12/results/E30_R12_CHANNEL_BEHAVIOUR_PROBE_V1.json",
    "max_tokens": 6000,
    "output_tokens": 6000,
    "wall_seconds": 71.00170421600342,
    "text_chars": 0,
    "stop_reason": "max_tokens",
}


def load_calls(paths: list[Path], contract: str) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for path in paths:
        payload = json.loads(path.read_text())
        for record in payload.get("calls", []):
            if record.get("contract_id") == contract and "transport_error" not in record:
                calls.append(record)
    return calls


def derive(calls: list[dict[str, Any]]) -> dict[str, Any]:
    """The budget derivation.  Refuses rather than guessing when it cannot check."""
    if not calls:
        return {"status": "COULD_NOT_DERIVE", "reason": "no successful calls for this contract"}
    truncated = [c for c in calls if c.get("stop_reason") == "max_tokens"]
    if truncated:
        # Any observation that hit the headroom is a censored draw: the observed
        # maximum is then a floor on the true maximum, and multiplying a floor by a
        # safety factor produces a number with no known relation to what is needed.
        return {
            "status": "COULD_NOT_DERIVE",
            "reason": f"{len(truncated)} of {len(calls)} calibration calls stopped at max_tokens; "
                      "the output-length distribution is censored and no cap can be derived from it",
            "calls": len(calls),
        }
    outs = sorted(c["output_tokens"] for c in calls)
    calibration_max = outs[-1]
    per_call = ROUNDING * math.ceil(SAFETY_MULTIPLE * calibration_max / ROUNDING)
    by_stage: dict[str, dict[str, Any]] = {}
    for stage in sorted({c["stage_id"] for c in calls}):
        rows = [c["output_tokens"] for c in calls if c["stage_id"] == stage]
        by_stage[stage] = {"calls": len(rows), "max": max(rows), "median": statistics.median(rows)}
    by_arm: dict[str, dict[str, Any]] = {}
    for arm in sorted({c["arm_id"] for c in calls}):
        rows = [c["output_tokens"] for c in calls if c["arm_id"] == arm]
        by_arm[arm] = {"calls": len(rows), "max": max(rows), "median": statistics.median(rows)}
    finals = [c for c in calls if c["stage_id"] in {"final", "challenge"}]
    return {
        "status": "DERIVED",
        "calls_measured": len(calls),
        "tasks_measured": sorted({c["task_id"] for c in calls}),
        "arms_measured": sorted({c["arm_id"] for c in calls}),
        "replicates": sorted({c["replicate"] for c in calls}),
        "stop_reasons": {s: sum(1 for c in calls if c["stop_reason"] == s)
                         for s in sorted({str(c["stop_reason"]) for c in calls})},
        "output_tokens": {
            "min": outs[0], "median": statistics.median(outs), "max": calibration_max,
            "p90": outs[max(0, math.ceil(0.9 * len(outs)) - 1)],
        },
        "output_tokens_by_stage": by_stage,
        "output_tokens_by_arm": by_arm,
        "calls_with_zero_text_chars": sum(1 for c in calls if c["text_chars"] == 0),
        "json_object_parseable_on_final_calls": f"{sum(1 for c in finals if c['json_object_parseable'])}/{len(finals)}",
        "derivation_rule": f"per_call_cap = {ROUNDING} * ceil({SAFETY_MULTIPLE} * calibration_max / {ROUNDING})",
        "registered_per_call_max_tokens": per_call,
        "cap_is_intended_to_be_non_binding": True,
        "wall_seconds": {
            "min": min(c["wall_seconds"] for c in calls),
            "median": statistics.median([c["wall_seconds"] for c in calls]),
            "max": max(c["wall_seconds"] for c in calls),
        },
    }


def feasibility(seconds_per_call: float, concurrency: int) -> dict[str, Any]:
    serial_hours = TOTAL_CALLS * seconds_per_call / 3600.0
    return {
        "total_model_calls": TOTAL_CALLS,
        "seconds_per_call": round(seconds_per_call, 2),
        "serial_hours": round(serial_hours, 1),
        "concurrency": concurrency,
        "wall_hours_at_concurrency": round(serial_hours / concurrency, 1),
        "slurm_time_limit_hours": SLURM_TIME_LIMIT_HOURS,
        "fits_in_one_slurm_allocation": (serial_hours / concurrency) < SLURM_TIME_LIMIT_HOURS,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", type=Path, nargs="+", required=True)
    ap.add_argument("--contract", default="thinking_disabled")
    ap.add_argument("--concurrency", type=int, nargs="+", default=[2, 4, 6])
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)

    calls = load_calls(list(args.calibration), args.contract)
    derived = derive(calls)

    registered_contract_feasibility = None
    if derived["status"] == "DERIVED":
        registered_contract_feasibility = {
            f"concurrency_{c}": feasibility(derived["wall_seconds"]["median"], c)
            for c in args.concurrency
        }

    payload = {
        "schema_version": "orion.v2.e30-r13-budget-note.v1",
        "purpose": "derive the registered per-call output-token cap and the campaign's wall-time feasibility",
        "reads_no_endpoint": True,
        "campaign_arithmetic": {
            "arms": 4,
            "model_calls_per_task_repetition": CALLS_PER_TASK_REPETITION,
            "calls_per_task_repetition_by_arm": {
                "SIMPLE_DIRECT": 1, "SAME_MODEL_REFLECTION": 2,
                "F0_PARENT_FEDERATION": 3, "F2_ORION_METABOLIC_FULL": 3,
            },
            "tasks": TASKS, "repetitions": REPETITIONS,
            "response_envelopes": TASKS * REPETITIONS * 4,
            "total_model_calls": TOTAL_CALLS,
            "note": "the campaign issues 1080 model calls, not 480; a per-envelope count "
                    "understates the dispatch by a factor of 2.25",
        },
        "registered_contract": {"contract_id": args.contract, "derivation": derived},
        "registered_contract_feasibility": registered_contract_feasibility,
        "provider_default_counterfactual": {
            "why": "E30-R12's registered escalated budget under the provider default, costed "
                   "against the same 1080-call campaign",
            "escalated_36000": R12_PROVIDER_DEFAULT_ESCALATED
            | {f"concurrency_{c}": feasibility(R12_PROVIDER_DEFAULT_ESCALATED["wall_seconds"], c)
               for c in args.concurrency},
            "primary_6000": R12_PROVIDER_DEFAULT_PRIMARY
            | {"note": "this path completes in ~71 s per call but emits zero text characters, "
                       "so it is a guaranteed-failure path rather than a cheap one",
               **{f"concurrency_{c}": feasibility(R12_PROVIDER_DEFAULT_PRIMARY["wall_seconds"], c)
                  for c in args.concurrency}},
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload["registered_contract"]["derivation"], indent=2, sort_keys=True))
    print(json.dumps(payload["registered_contract_feasibility"], indent=2, sort_keys=True))
    print(f"BUDGET_NOTE_WRITTEN {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
