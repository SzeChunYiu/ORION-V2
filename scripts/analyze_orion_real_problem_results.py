#!/usr/bin/env python3
"""Analyze paired ORION-V2 real-problem outcomes without promoting authority.

The script produces descriptive and pre-registered paired comparisons. It does
not declare a field founded, a theory superior or a manuscript submission-ready.
Those decisions remain governed by the protected protocols and independent
review.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


F2 = "F2_ORION_METABOLIC_FULL"
PRIMARY_COMPARATORS = (
    "F0_PARENT_FEDERATION",
    "SIMPLE_DIRECT",
    "SAME_MODEL_REFLECTION",
)
COMPONENT_ARMS = (
    "F2_MINUS_DECOMPOSITION",
    "F2_MINUS_NATIVE_RECOVERY",
    "F2_MINUS_COUNTERPROBE",
    "F2_MINUS_SELECTIVE_REOPEN",
)


class AnalysisError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AnalysisError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AnalysisError(f"expected JSON object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_evaluations(workdir: Path) -> dict[str, dict[str, dict[str, Any]]]:
    by_arm: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for path in sorted((workdir / "evaluations").glob("*/*.json")):
        item = read_json(path)
        arm_id = str(item.get("arm_id", path.parent.name))
        task_id = str(item.get("task_id", path.stem))
        if task_id in by_arm[arm_id]:
            raise AnalysisError(f"duplicate evaluation for {arm_id}/{task_id}")
        by_arm[arm_id][task_id] = item
    return dict(by_arm)


def load_responses(workdir: Path) -> dict[str, dict[str, dict[str, Any]]]:
    by_arm: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for path in sorted((workdir / "responses").glob("*/*.json")):
        item = read_json(path)
        by_arm[path.parent.name][path.stem] = item
    return dict(by_arm)


def success(item: dict[str, Any]) -> bool | None:
    for key in (
        "full_regression_suite_passed",
        "native_success",
        "protected_decision_correct",
    ):
        if key in item and isinstance(item[key], bool):
            return item[key]
    return None


def critical_failure(item: dict[str, Any]) -> bool | None:
    if "critical_new_failure_count" in item:
        try:
            return int(item["critical_new_failure_count"] or 0) > 0
        except (TypeError, ValueError):
            return None
    value = item.get("critical_false_completion")
    return value if isinstance(value, bool) else None


def wall_time(item: dict[str, Any], response: dict[str, Any] | None) -> float | None:
    value = item.get("wall_time_seconds")
    if isinstance(value, (int, float)) and math.isfinite(value):
        return float(value)
    if response:
        resource = response.get("resource_receipt")
        if isinstance(resource, dict):
            value = resource.get("wall_time_seconds")
            if isinstance(value, (int, float)) and math.isfinite(value):
                return float(value)
    return None


def percentile(values: list[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    location = probability * (len(ordered) - 1)
    low = math.floor(location)
    high = math.ceil(location)
    if low == high:
        return ordered[low]
    fraction = location - low
    return ordered[low] * (1 - fraction) + ordered[high] * fraction


def paired_bootstrap_difference(
    pairs: list[tuple[float, float]],
    *,
    repetitions: int = 10000,
    seed: int = 20260828,
) -> dict[str, Any]:
    if not pairs:
        return {
            "estimate": None,
            "ci95": [None, None],
            "pair_count": 0,
            "bootstrap_repetitions": repetitions,
            "seed": seed,
        }
    differences = [left - right for left, right in pairs]
    estimate = statistics.fmean(differences)
    generator = random.Random(seed)
    bootstraps: list[float] = []
    for _ in range(repetitions):
        sample = [differences[generator.randrange(len(differences))] for _ in differences]
        bootstraps.append(statistics.fmean(sample))
    return {
        "estimate": estimate,
        "ci95": [percentile(bootstraps, 0.025), percentile(bootstraps, 0.975)],
        "pair_count": len(pairs),
        "bootstrap_repetitions": repetitions,
        "seed": seed,
    }


def exact_two_sided_discordant_p(n10: int, n01: int) -> float | None:
    n = n10 + n01
    if n == 0:
        return None
    lower = min(n10, n01)
    tail = sum(math.comb(n, k) for k in range(lower + 1)) / (2**n)
    return min(1.0, 2.0 * tail)


def paired_binary_comparison(
    left: dict[str, dict[str, Any]],
    right: dict[str, dict[str, Any]],
    extractor,
) -> dict[str, Any]:
    task_ids = sorted(set(left) & set(right))
    pairs: list[tuple[float, float]] = []
    n11 = n10 = n01 = n00 = 0
    missing: list[str] = []
    for task_id in task_ids:
        a = extractor(left[task_id])
        b = extractor(right[task_id])
        if a is None or b is None:
            missing.append(task_id)
            continue
        pairs.append((float(a), float(b)))
        if a and b:
            n11 += 1
        elif a and not b:
            n10 += 1
        elif not a and b:
            n01 += 1
        else:
            n00 += 1
    return {
        "paired_table": {"both_true": n11, "left_only": n10, "right_only": n01, "both_false": n00},
        "risk_difference": paired_bootstrap_difference(pairs),
        "exact_discordant_p": exact_two_sided_discordant_p(n10, n01),
        "missing_task_ids": missing,
    }


def paired_continuous_comparison(
    left: dict[str, dict[str, Any]],
    right: dict[str, dict[str, Any]],
    left_responses: dict[str, dict[str, Any]],
    right_responses: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    pairs: list[tuple[float, float]] = []
    for task_id in sorted(set(left) & set(right)):
        a = wall_time(left[task_id], left_responses.get(task_id))
        b = wall_time(right[task_id], right_responses.get(task_id))
        if a is not None and b is not None:
            pairs.append((a, b))
    result = paired_bootstrap_difference(pairs)
    differences = [a - b for a, b in pairs]
    result["median_difference"] = statistics.median(differences) if differences else None
    return result


def compare_arms(
    evaluations: dict[str, dict[str, dict[str, Any]]],
    responses: dict[str, dict[str, dict[str, Any]]],
    left_id: str,
    right_id: str,
) -> dict[str, Any]:
    left = evaluations.get(left_id, {})
    right = evaluations.get(right_id, {})
    return {
        "left_arm": left_id,
        "right_arm": right_id,
        "paired_task_count": len(set(left) & set(right)),
        "success": paired_binary_comparison(left, right, success),
        "critical_failure": paired_binary_comparison(left, right, critical_failure),
        "wall_time_seconds": paired_continuous_comparison(
            left,
            right,
            responses.get(left_id, {}),
            responses.get(right_id, {}),
        ),
    }


def arm_summary(
    evaluations: dict[str, dict[str, dict[str, Any]]],
    responses: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for arm_id, tasks in sorted(evaluations.items()):
        success_values = [value for item in tasks.values() if (value := success(item)) is not None]
        critical_values = [
            value for item in tasks.values() if (value := critical_failure(item)) is not None
        ]
        times = [
            value
            for task_id, item in tasks.items()
            if (value := wall_time(item, responses.get(arm_id, {}).get(task_id))) is not None
        ]
        result[arm_id] = {
            "task_count": len(tasks),
            "success_count": sum(success_values),
            "success_rate": statistics.fmean(success_values) if success_values else None,
            "critical_failure_count": sum(critical_values),
            "critical_failure_rate": statistics.fmean(critical_values) if critical_values else None,
            "mean_wall_time_seconds": statistics.fmean(times) if times else None,
            "median_wall_time_seconds": statistics.median(times) if times else None,
            "status_counts": dict(
                Counter(
                    str(item.get("status", item.get("agent_status", "UNKNOWN")))
                    for item in tasks.values()
                )
            ),
        }
    return result


def component_disposition(comparison: dict[str, Any]) -> str:
    success_effect = comparison["success"]["risk_difference"]["estimate"]
    critical_effect = comparison["critical_failure"]["risk_difference"]["estimate"]
    time_effect = comparison["wall_time_seconds"]["estimate"]
    pair_count = comparison["paired_task_count"]
    if pair_count < 20:
        return "CANNOT_CHECK_UNDERPOWERED"
    if success_effect is None or critical_effect is None:
        return "CANNOT_CHECK_MISSING_OUTCOMES"
    # left is FULL and right is MINUS: positive success or lower critical failure
    # indicates value from the removed component.
    if critical_effect > 0.02:
        return "HARMFUL_OR_CRITICAL_REGRESSION_IN_FULL"
    if success_effect >= 0.05 or critical_effect <= -0.02:
        return "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE"
    if time_effect is not None and time_effect > 0 and abs(success_effect) < 0.01:
        return "REDUNDANT_DRAG_CANDIDATE"
    return "PARENT_REPLACEABLE_OR_CONTEXTUAL_CANNOT_DISTINGUISH"


def analyze(workdir: Path) -> dict[str, Any]:
    evaluations = load_evaluations(workdir)
    responses = load_responses(workdir)
    if not evaluations:
        raise AnalysisError("no evaluation artifacts found")

    summaries = arm_summary(evaluations, responses)
    primary = [
        compare_arms(evaluations, responses, F2, comparator)
        for comparator in PRIMARY_COMPARATORS
    ]
    components: dict[str, Any] = {}
    for arm_id in COMPONENT_ARMS:
        comparison = compare_arms(evaluations, responses, F2, arm_id)
        comparison["component_disposition"] = component_disposition(comparison)
        components[arm_id] = comparison

    f2_summary = summaries.get(F2, {})
    f0_summary = summaries.get("F0_PARENT_FEDERATION", {})
    hard_gate_state = "CANNOT_CHECK"
    if f2_summary and f0_summary:
        f2_critical = f2_summary.get("critical_failure_rate")
        f0_critical = f0_summary.get("critical_failure_rate")
        if f2_critical is not None and f0_critical is not None:
            hard_gate_state = (
                "PASS_DESCRIPTIVE_ONLY"
                if f2_critical <= f0_critical + 0.02
                else "FAIL_CRITICAL_NONINFERIORITY"
            )

    result = {
        "schema_version": "orion.v2.real-problem-analysis.v1",
        "analysis_status": "DESCRIPTIVE_PROSPECTIVE_PLAN_IMPLEMENTATION",
        "arm_summaries": summaries,
        "primary_comparisons": primary,
        "component_effects": components,
        "hard_gate_state": hard_gate_state,
        "minimum_confirmatory_paired_tasks": 40,
        "field_status": "NOT_ESTABLISHED",
        "supertheory_status": "NOT_ESTABLISHED",
        "publication_readiness": "NOT_ESTABLISHED",
        "required_next": [
            "independent statistical and domain review",
            "Holm adjustment across primary confirmatory tests",
            "resource normalization and Pareto analysis",
            "cross-domain native evaluation",
            "complete missing and failure audit",
        ],
    }

    aggregate = workdir / "aggregate"
    write_json(aggregate / "paired_comparisons.json", {"primary": primary})
    write_json(aggregate / "component_effects.json", components)
    write_json(aggregate / "analysis.json", result)
    write_json(
        aggregate / "failure_ledger.json",
        {
            "schema_version": "orion.v2.real-problem-failure-ledger.v1",
            "statuses": {
                arm: summary["status_counts"] for arm, summary in summaries.items()
            },
            "hard_gate_state": hard_gate_state,
        },
    )
    write_json(
        aggregate / "resource_pareto.json",
        {
            "schema_version": "orion.v2.real-problem-resource-pareto.v1",
            "arms": {
                arm: {
                    "success_rate": summary["success_rate"],
                    "critical_failure_rate": summary["critical_failure_rate"],
                    "mean_wall_time_seconds": summary["mean_wall_time_seconds"],
                }
                for arm, summary in summaries.items()
            },
            "weighted_total_score": "FORBIDDEN_NOT_COMPUTED",
        },
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-real-problem-suite"))
    args = parser.parse_args(argv)
    try:
        result = analyze(args.workdir)
    except (AnalysisError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
