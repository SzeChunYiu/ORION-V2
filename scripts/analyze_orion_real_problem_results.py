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
from typing import Any

F2 = "F2_ORION_METABOLIC_FULL"
PRIMARY_COMPARATORS = (
    "SIMPLE_DIRECT",
    "SAME_MODEL_REFLECTION",
    "F0_PARENT_FEDERATION",
)
COMPONENT_ARMS = (
    "F2_MINUS_DECOMPOSITION",
    "F2_MINUS_NATIVE_RECOVERY",
    "F2_MINUS_COUNTERPROBE",
    "F2_MINUS_SELECTIVE_REOPEN",
)


class AnalysisError(RuntimeError):
    pass


class RepetitionLayout:
    """Frozen repetition identity discovered before outcome analysis."""

    def __init__(self, *, workdirs: dict[str, Path], mode: str) -> None:
        self.workdirs = workdirs
        self.mode = mode

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(self.workdirs)


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
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def discover_repetitions(workdir: Path) -> RepetitionLayout:
    """Find either the E20 layout or nested E30 ``confirmatory-rN`` lanes.

    When a run identity declares a repetition count, absent lanes are retained
    as empty expected repetitions.  This prevents a partially materialised E30
    campaign from silently becoming a smaller experiment after outcomes exist.
    """

    direct = workdir / "evaluations"
    nested: dict[int, Path] = {}
    for path in sorted(workdir.glob("confirmatory-r*")):
        if not path.is_dir():
            continue
        suffix = path.name.removeprefix("confirmatory-r")
        if suffix.isdigit():
            nested[int(suffix)] = path
    if direct.is_dir() and nested:
        raise AnalysisError("ambiguous direct and nested repetition layouts")
    if nested:
        declared = 0
        identity_path = workdir / "RUN_IDENTITY.json"
        if identity_path.exists():
            identity = read_json(identity_path)
            value = identity.get("repetitions")
            if isinstance(value, int) and value > 0:
                declared = value
        count = max(declared, max(nested))
        return RepetitionLayout(
            workdirs={
                str(index): workdir / f"confirmatory-r{index}"
                for index in range(1, count + 1)
            },
            mode="NESTED_WITHIN_TASK",
        )
    return RepetitionLayout(
        workdirs={"1": workdir}, mode="SINGLE_REPETITION_COMPATIBILITY"
    )


def load_task_metadata(layout: RepetitionLayout) -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}
    for repetition_workdir in layout.workdirs.values():
        path = repetition_workdir / "frozen_tasks.json"
        if not path.exists():
            continue
        frozen = read_json(path)
        tasks = frozen.get("tasks", [])
        if not isinstance(tasks, list):
            raise AnalysisError(f"invalid tasks list in {path}")
        for task in tasks:
            if not isinstance(task, dict) or not isinstance(task.get("task_id"), str):
                raise AnalysisError(f"invalid task entry in {path}")
            task_id = task["task_id"]
            existing = metadata.get(task_id)
            identifying = {
                key: task.get(key)
                for key in ("task_id", "benchmark_id", "project", "domain")
            }
            if existing is not None and any(
                existing.get(key) != value
                for key, value in identifying.items()
                if value is not None
            ):
                raise AnalysisError(
                    f"task metadata changed across repetitions: {task_id}"
                )
            metadata.setdefault(task_id, dict(task))
    return metadata


def load_repeated_artifacts(
    layout: RepetitionLayout,
    directory: str,
) -> dict[str, dict[str, dict[str, dict[str, Any]]]]:
    """Return arm -> task -> repetition -> artifact without pooling runs."""

    by_arm: dict[str, dict[str, dict[str, dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    for repetition_id, repetition_workdir in layout.workdirs.items():
        for path in sorted((repetition_workdir / directory).glob("*/*.json")):
            item = read_json(path)
            arm_id = str(item.get("arm_id", path.parent.name))
            task_id = str(item.get("task_id", path.stem))
            if repetition_id in by_arm[arm_id][task_id]:
                raise AnalysisError(
                    f"duplicate {directory.rstrip('s')} for {arm_id}/{task_id}/r{repetition_id}"
                )
            by_arm[arm_id][task_id][repetition_id] = item
    return {
        arm: {task: dict(repetitions) for task, repetitions in tasks.items()}
        for arm, tasks in by_arm.items()
    }


def infer_project(
    task_id: str, metadata: dict[str, Any], item: dict[str, Any] | None
) -> str:
    for source in (metadata, item or {}):
        value = source.get("project")
        if isinstance(value, str) and value:
            return value
    if task_id.startswith("bugsinpy-"):
        remainder = task_id.removeprefix("bugsinpy-")
        project, separator, _ = remainder.rpartition("-")
        if separator and project:
            return project
    benchmark = metadata.get("benchmark_id") or (item or {}).get("benchmark_id")
    return str(benchmark or "UNKNOWN")


def uncheckable(item: dict[str, Any]) -> bool:
    status = str(item.get("status", item.get("agent_status", ""))).upper()
    return (
        status.startswith("CANNOT_CHECK")
        or item.get("infrastructure_error") is True
        or item.get("test_infrastructure_error") is True
    )


def success(item: dict[str, Any]) -> bool | None:
    value = item.get("_aggregate_success")
    if isinstance(value, bool):
        return value
    if uncheckable(item):
        return None
    for key in (
        "full_regression_suite_passed",
        "native_success",
        "protected_decision_correct",
    ):
        if key in item and isinstance(item[key], bool):
            return item[key]
    return None


def critical_failure(item: dict[str, Any]) -> bool | None:
    value = item.get("_aggregate_critical_failure")
    if isinstance(value, bool):
        return value
    if uncheckable(item):
        return None
    if "critical_new_failure_count" in item:
        if item["critical_new_failure_count"] is None:
            return None
        try:
            return int(item["critical_new_failure_count"] or 0) > 0
        except (TypeError, ValueError):
            return None
    value = item.get("critical_false_completion")
    return value if isinstance(value, bool) else None


def wall_time(item: dict[str, Any], response: dict[str, Any] | None) -> float | None:
    value = item.get("_aggregate_wall_time_seconds")
    if isinstance(value, (int, float)) and math.isfinite(value):
        return float(value)
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


def frozen_majority(values: list[bool | None]) -> bool | None:
    """Strict majority over *all expected* repetitions.

    Missing/CANNOT_CHECK repetitions stay in the denominator.  Thus two equal
    valid outcomes determine a three-run task, whereas one success, one failure
    and one missing run remains CANNOT_CHECK.  A single E20 run is unchanged.
    """

    threshold = len(values) / 2
    true_count = sum(value is True for value in values)
    false_count = sum(value is False for value in values)
    if true_count > threshold:
        return True
    if false_count > threshold:
        return False
    return None


def aggregate_repetitions(
    repeated_evaluations: dict[str, dict[str, dict[str, dict[str, Any]]]],
    repeated_responses: dict[str, dict[str, dict[str, dict[str, Any]]]],
    layout: RepetitionLayout,
    task_metadata: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, Any]]:
    """Aggregate repetitions within task-arm before any between-arm analysis.

    Frozen rules:
    - success: strict majority of all expected repetitions;
    - critical failure: any observed critical failure, otherwise false only
      when every expected repetition is checkable and false;
    - wall time: median only when every expected repetition is observed;
    - missing and unstable repetitions remain explicit in the audit.
    """

    expected = layout.ids
    observed_tasks = {
        task_id for tasks in repeated_evaluations.values() for task_id in tasks
    }
    task_ids = sorted(set(task_metadata) | observed_tasks)
    aggregated: dict[str, dict[str, dict[str, Any]]] = {}
    audit: dict[str, Any] = {}
    for arm_id, observed_by_task in sorted(repeated_evaluations.items()):
        arm_tasks: dict[str, dict[str, Any]] = {}
        missing_by_task: dict[str, list[str]] = {}
        status_counts: Counter[str] = Counter()
        complete_task_count = 0
        success_instability_count = 0
        critical_instability_count = 0
        cannot_check_task_count = 0
        evaluation_count = 0
        for task_id in task_ids:
            repetitions = observed_by_task.get(task_id, {})
            evaluation_count += len(repetitions)
            items = [repetitions.get(repetition_id) for repetition_id in expected]
            missing = [
                repetition_id
                for repetition_id, item in zip(expected, items)
                if item is None
            ]
            if missing:
                missing_by_task[task_id] = missing
            else:
                complete_task_count += 1
            for item in items:
                if item is not None:
                    status_counts[
                        str(item.get("status", item.get("agent_status", "UNKNOWN")))
                    ] += 1

            successes = [success(item) if item is not None else None for item in items]
            criticals = [
                critical_failure(item) if item is not None else None for item in items
            ]
            aggregate_success = frozen_majority(successes)
            if any(value is True for value in criticals):
                aggregate_critical: bool | None = True
            elif all(value is False for value in criticals):
                aggregate_critical = False
            else:
                aggregate_critical = None
            if aggregate_success is None or aggregate_critical is None:
                cannot_check_task_count += 1

            checkable_successes = {value for value in successes if value is not None}
            checkable_criticals = {value for value in criticals if value is not None}
            success_unstable = len(checkable_successes) > 1
            critical_unstable = len(checkable_criticals) > 1
            success_instability_count += success_unstable
            critical_instability_count += critical_unstable

            times: list[float] = []
            for repetition_id, item in zip(expected, items):
                if item is None:
                    continue
                response = (
                    repeated_responses.get(arm_id, {})
                    .get(task_id, {})
                    .get(repetition_id)
                )
                value = wall_time(item, response)
                if value is not None:
                    times.append(value)
            aggregate_time = (
                statistics.median(times) if len(times) == len(expected) else None
            )
            first = next((item for item in items if item is not None), {})
            metadata = task_metadata.get(task_id, {})
            project = infer_project(task_id, metadata, first)
            benchmark = (
                metadata.get("benchmark_id") or first.get("benchmark_id") or "UNKNOWN"
            )
            if not repetitions:
                aggregate_status = "CANNOT_CHECK_MISSING_ALL_REPETITIONS"
            elif missing:
                aggregate_status = "CANNOT_CHECK_MISSING_REPETITIONS"
            else:
                statuses = {
                    str(item.get("status", item.get("agent_status", "UNKNOWN")))
                    for item in items
                    if item is not None
                }
                aggregate_status = (
                    statuses.pop()
                    if len(statuses) == 1
                    else "MIXED_REPETITION_OUTCOMES"
                )
            arm_tasks[task_id] = {
                "task_id": task_id,
                "arm_id": arm_id,
                "benchmark_id": str(benchmark),
                "project": project,
                "status": aggregate_status,
                "_aggregate_success": aggregate_success,
                "_aggregate_critical_failure": aggregate_critical,
                "_aggregate_wall_time_seconds": aggregate_time,
                "_expected_repetition_ids": list(expected),
                "_observed_repetition_ids": sorted(repetitions),
                "_missing_repetition_ids": missing,
                "_success_values": successes,
                "_critical_failure_values": criticals,
                "_success_instability": success_unstable,
                "_critical_failure_instability": critical_unstable,
                "_wall_time_values": times,
            }
        aggregated[arm_id] = arm_tasks
        audit[arm_id] = {
            "expected_repetition_ids": list(expected),
            "registered_task_count": len(task_ids),
            "evaluation_count": evaluation_count,
            "complete_task_count": complete_task_count,
            "missing_repetitions_by_task": missing_by_task,
            "success_instability_task_count": success_instability_count,
            "critical_failure_instability_task_count": critical_instability_count,
            "cannot_check_task_count": cannot_check_task_count,
            "raw_status_counts": dict(status_counts),
        }
    return aggregated, audit


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
    strata: list[str] | None = None,
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
            "bootstrap_unit": "TASK",
            "bootstrap_stratification": "PROJECT" if strata else "NONE",
        }
    differences = [left - right for left, right in pairs]
    estimate = statistics.fmean(differences)
    generator = random.Random(seed)
    bootstraps: list[float] = []
    grouped: dict[str, list[float]] = defaultdict(list)
    if strata is not None:
        if len(strata) != len(differences):
            raise AnalysisError("bootstrap strata do not match paired observations")
        for stratum, difference in zip(strata, differences):
            grouped[stratum].append(difference)
    for _ in range(repetitions):
        if grouped:
            sample = [
                values[generator.randrange(len(values))]
                for values in grouped.values()
                for _ in values
            ]
        else:
            sample = [
                differences[generator.randrange(len(differences))] for _ in differences
            ]
        bootstraps.append(statistics.fmean(sample))
    return {
        "estimate": estimate,
        "ci95": [percentile(bootstraps, 0.025), percentile(bootstraps, 0.975)],
        "pair_count": len(pairs),
        "bootstrap_repetitions": repetitions,
        "seed": seed,
        "bootstrap_unit": "TASK",
        "bootstrap_stratification": "PROJECT" if grouped else "NONE",
    }


def exact_two_sided_discordant_p(n10: int, n01: int) -> float | None:
    n = n10 + n01
    if n == 0:
        return None
    lower = min(n10, n01)
    tail = sum(math.comb(n, k) for k in range(lower + 1)) / (2**n)
    return min(1.0, 2.0 * tail)


def binomial_cdf(k: int, n: int, probability: float) -> float:
    return sum(
        math.comb(n, index) * probability**index * (1.0 - probability) ** (n - index)
        for index in range(k + 1)
    )


def exact_binomial_interval(
    successes: int, total: int, alpha: float = 0.05
) -> list[float | None]:
    """Two-sided Clopper-Pearson interval without an optional scipy dependency."""

    if total <= 0:
        return [None, None]
    if not 0 <= successes <= total:
        raise ValueError("invalid binomial counts")

    def bisect(predicate) -> float:
        low, high = 0.0, 1.0
        for _ in range(80):
            middle = (low + high) / 2
            if predicate(middle):
                high = middle
            else:
                low = middle
        return (low + high) / 2

    lower = 0.0
    if successes:
        # P_p(X >= successes) increases with p.
        lower = bisect(
            lambda p: 1.0 - binomial_cdf(successes - 1, total, p) >= alpha / 2
        )
    upper = 1.0
    if successes < total:
        # P_p(X <= successes) decreases with p; invert via the complement.
        upper = bisect(lambda p: binomial_cdf(successes, total, p) <= alpha / 2)
    return [lower, upper]


def exact_sign_p(differences: list[float]) -> float | None:
    positive = sum(value > 0 for value in differences)
    negative = sum(value < 0 for value in differences)
    return exact_two_sided_discordant_p(positive, negative)


def holm_adjust(
    comparisons: list[dict[str, Any]],
    *,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Holm-adjust registered primary success tests, retaining untestable nulls.

    The multiplier uses the full registered family size (three), even when a
    comparison is CANNOT_CHECK.  Untestable hypotheses are never rejected.
    """

    family_size = len(comparisons)
    testable = [
        (index, comparison["success"].get("exact_discordant_p"))
        for index, comparison in enumerate(comparisons)
        if comparison["success"].get("exact_discordant_p") is not None
    ]
    testable.sort(key=lambda pair: (float(pair[1]), pair[0]))
    running = 0.0
    rejection_open = True
    for rank, (index, p_value) in enumerate(testable, start=1):
        multiplier = family_size - rank + 1
        adjusted = min(1.0, max(running, float(p_value) * multiplier))
        running = adjusted
        threshold = alpha / multiplier
        reject = rejection_open and float(p_value) <= threshold
        if not reject:
            rejection_open = False
        success_result = comparisons[index]["success"]
        success_result["holm_adjusted_p"] = adjusted
        success_result["holm_reject_at_alpha_0_05"] = reject
        success_result["holm_rank"] = rank
    for comparison in comparisons:
        success_result = comparison["success"]
        if success_result.get("exact_discordant_p") is None:
            success_result["holm_adjusted_p"] = None
            success_result["holm_reject_at_alpha_0_05"] = False
            success_result["holm_rank"] = None
            success_result["multiplicity_status"] = "CANNOT_CHECK_NO_DISCORDANT_PAIRS"
        else:
            success_result["multiplicity_status"] = "HOLM_ADJUSTED"
    return {
        "method": "HOLM_STEP_DOWN",
        "endpoint": "TASK_LEVEL_AGGREGATED_EXECUTABLE_NATIVE_SUCCESS",
        "alpha": alpha,
        "registered_family_size": family_size,
        "testable_comparison_count": len(testable),
        "untestable_comparison_count": family_size - len(testable),
        "missing_tests_are_not_rejected": True,
    }


def paired_binary_comparison(
    left: dict[str, dict[str, Any]],
    right: dict[str, dict[str, Any]],
    extractor,
) -> dict[str, Any]:
    task_ids = sorted(set(left) & set(right))
    pairs: list[tuple[float, float]] = []
    strata: list[str] = []
    n11 = n10 = n01 = n00 = 0
    missing: list[str] = []
    for task_id in task_ids:
        a = extractor(left[task_id])
        b = extractor(right[task_id])
        if a is None or b is None:
            missing.append(task_id)
            continue
        pairs.append((float(a), float(b)))
        strata.append(str(left[task_id].get("project", "UNKNOWN")))
        if a and b:
            n11 += 1
        elif a and not b:
            n10 += 1
        elif not a and b:
            n01 += 1
        else:
            n00 += 1
    discordant = n10 + n01
    return {
        "paired_table": {
            "both_true": n11,
            "left_only": n10,
            "right_only": n01,
            "both_false": n00,
        },
        "risk_difference": paired_bootstrap_difference(pairs, strata=strata),
        "exact_discordant_p": exact_two_sided_discordant_p(n10, n01),
        "discordant_left_win_probability": n10 / discordant if discordant else None,
        "discordant_left_win_probability_exact_ci95": exact_binomial_interval(
            n10, discordant
        ),
        "analysis_unit": "TASK_AFTER_WITHIN_TASK_ARM_REPETITION_AGGREGATION",
        "checkable_task_count": len(pairs),
        "missing_task_ids": missing,
    }


def paired_continuous_comparison(
    left: dict[str, dict[str, Any]],
    right: dict[str, dict[str, Any]],
    left_responses: dict[str, dict[str, Any]],
    right_responses: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    pairs: list[tuple[float, float]] = []
    strata: list[str] = []
    missing: list[str] = []
    for task_id in sorted(set(left) & set(right)):
        a = wall_time(left[task_id], left_responses.get(task_id))
        b = wall_time(right[task_id], right_responses.get(task_id))
        if a is not None and b is not None:
            pairs.append((a, b))
            strata.append(str(left[task_id].get("project", "UNKNOWN")))
        else:
            missing.append(task_id)
    result = paired_bootstrap_difference(pairs, strata=strata)
    differences = [a - b for a, b in pairs]
    result["median_difference"] = (
        statistics.median(differences) if differences else None
    )
    result["difference_iqr"] = [
        percentile(differences, 0.25),
        percentile(differences, 0.75),
    ]
    result["exact_sign_p"] = exact_sign_p(differences)
    result["missing_task_ids"] = missing
    result["analysis_unit"] = "TASK_AFTER_WITHIN_TASK_ARM_REPETITION_AGGREGATION"
    return result


def compare_arms(
    evaluations: dict[str, dict[str, dict[str, Any]]],
    responses: dict[str, dict[str, dict[str, Any]]],
    left_id: str,
    right_id: str,
    *,
    include_project_strata: bool = True,
) -> dict[str, Any]:
    left = evaluations.get(left_id, {})
    right = evaluations.get(right_id, {})
    left_only = sorted(set(left) - set(right))
    right_only = sorted(set(right) - set(left))
    result = {
        "left_arm": left_id,
        "right_arm": right_id,
        "paired_task_count": len(set(left) & set(right)),
        "left_only_task_ids": left_only,
        "right_only_task_ids": right_only,
        "success": paired_binary_comparison(left, right, success),
        "critical_failure": paired_binary_comparison(left, right, critical_failure),
        "wall_time_seconds": paired_continuous_comparison(
            left,
            right,
            responses.get(left_id, {}),
            responses.get(right_id, {}),
        ),
    }
    if include_project_strata:
        projects = sorted(
            {
                str(item.get("project", "UNKNOWN"))
                for item in list(left.values()) + list(right.values())
            }
        )
        project_strata: dict[str, Any] = {}
        for project in projects:
            sub_evaluations = {
                left_id: {
                    task_id: item
                    for task_id, item in left.items()
                    if str(item.get("project", "UNKNOWN")) == project
                },
                right_id: {
                    task_id: item
                    for task_id, item in right.items()
                    if str(item.get("project", "UNKNOWN")) == project
                },
            }
            project_strata[project] = compare_arms(
                sub_evaluations,
                responses,
                left_id,
                right_id,
                include_project_strata=False,
            )
        result["project_strata"] = project_strata
    return result


def arm_summary(
    evaluations: dict[str, dict[str, dict[str, Any]]],
    responses: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, Any]:
    def summarize_tasks(
        arm_id: str,
        tasks: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        success_values = [
            value for item in tasks.values() if (value := success(item)) is not None
        ]
        critical_values = [
            value
            for item in tasks.values()
            if (value := critical_failure(item)) is not None
        ]
        times = [
            value
            for task_id, item in tasks.items()
            if (value := wall_time(item, responses.get(arm_id, {}).get(task_id)))
            is not None
        ]
        return {
            "task_count": len(tasks),
            "success_count": sum(success_values),
            "success_checkable_task_count": len(success_values),
            "success_cannot_check_task_count": len(tasks) - len(success_values),
            "success_rate": (
                statistics.fmean(success_values) if success_values else None
            ),
            "critical_failure_count": sum(critical_values),
            "critical_failure_checkable_task_count": len(critical_values),
            "critical_failure_cannot_check_task_count": len(tasks)
            - len(critical_values),
            "critical_failure_rate": (
                statistics.fmean(critical_values) if critical_values else None
            ),
            "mean_wall_time_seconds": statistics.fmean(times) if times else None,
            "median_wall_time_seconds": statistics.median(times) if times else None,
            "wall_time_checkable_task_count": len(times),
            "status_counts": dict(
                Counter(
                    str(item.get("status", item.get("agent_status", "UNKNOWN")))
                    for item in tasks.values()
                )
            ),
            "success_instability_task_count": sum(
                bool(item.get("_success_instability")) for item in tasks.values()
            ),
            "critical_failure_instability_task_count": sum(
                bool(item.get("_critical_failure_instability"))
                for item in tasks.values()
            ),
        }

    result: dict[str, Any] = {}
    for arm_id, tasks in sorted(evaluations.items()):
        summary = summarize_tasks(arm_id, tasks)
        projects = sorted(
            {str(item.get("project", "UNKNOWN")) for item in tasks.values()}
        )
        summary["project_strata"] = {
            project: summarize_tasks(
                arm_id,
                {
                    task_id: item
                    for task_id, item in tasks.items()
                    if str(item.get("project", "UNKNOWN")) == project
                },
            )
            for project in projects
        }
        result[arm_id] = summary
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
    layout = discover_repetitions(workdir)
    task_metadata = load_task_metadata(layout)
    repeated_evaluations = load_repeated_artifacts(layout, "evaluations")
    repeated_responses = load_repeated_artifacts(layout, "responses")
    if not repeated_evaluations:
        raise AnalysisError("no evaluation artifacts found")
    evaluations, repetition_audit = aggregate_repetitions(
        repeated_evaluations,
        repeated_responses,
        layout,
        task_metadata,
    )
    # Resource values have already been frozen within task-arm.  Keeping this
    # mapping empty prevents accidental cross-repetition response pooling.
    responses: dict[str, dict[str, dict[str, Any]]] = {}

    summaries = arm_summary(evaluations, responses)
    primary = [
        compare_arms(evaluations, responses, F2, comparator)
        for comparator in PRIMARY_COMPARATORS
    ]
    for comparison in primary:
        comparison["comparison_id"] = (
            f"{comparison['left_arm']}_vs_{comparison['right_arm']}"
        )
        comparison["registered_primary_comparison"] = True
    multiplicity = holm_adjust(primary)
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

    independent_tasks = len(
        {task_id for tasks in evaluations.values() for task_id in tasks}
    )
    result = {
        "schema_version": "orion.v2.real-problem-analysis.v2",
        "analysis_status": (
            "CONFIRMATORY_TASK_LEVEL_ANALYSIS"
            if layout.mode == "NESTED_WITHIN_TASK" and independent_tasks >= 40
            else "DESCRIPTIVE_OR_UNDERPOWERED_TASK_LEVEL_ANALYSIS"
        ),
        "analysis_unit": "FROZEN_TASK",
        "repetitions_nested_within_task": True,
        "repetition_layout": layout.mode,
        "expected_repetition_ids": list(layout.ids),
        "independent_task_count": independent_tasks,
        "repetition_aggregation_rule": {
            "success": "STRICT_MAJORITY_OF_ALL_EXPECTED_REPETITIONS_MISSING_STAYS_IN_DENOMINATOR",
            "critical_failure": "ANY_TRUE_ELSE_FALSE_ONLY_IF_ALL_EXPECTED_REPETITIONS_ARE_FALSE",
            "wall_time_seconds": "MEDIAN_ONLY_IF_ALL_EXPECTED_REPETITIONS_HAVE_VALUES",
            "task_weight": "ONE_PER_FROZEN_TASK_NEVER_ONE_PER_REPETITION",
        },
        "repetition_audit": repetition_audit,
        "arm_summaries": summaries,
        "primary_comparisons": primary,
        "primary_multiplicity": multiplicity,
        "component_effects": components,
        "hard_gate_state": hard_gate_state,
        "minimum_confirmatory_paired_tasks": 40,
        "field_status": "NOT_ESTABLISHED",
        "supertheory_status": "NOT_ESTABLISHED",
        "publication_readiness": "NOT_ESTABLISHED",
        "required_next": [
            "independent statistical and domain review",
            "resource normalization and Pareto analysis",
            "cross-domain native evaluation",
            "complete missing and failure audit",
        ],
    }

    aggregate = workdir / "aggregate"
    write_json(
        aggregate / "paired_comparisons.json",
        {
            "schema_version": "orion.v2.paired-comparisons.v2",
            "analysis_unit": "FROZEN_TASK",
            "repetitions_nested_within_task": True,
            "repetition_aggregation_rule": result["repetition_aggregation_rule"],
            "multiplicity": multiplicity,
            "primary": primary,
        },
    )
    write_json(aggregate / "arm_metrics.json", summaries)
    write_json(aggregate / "component_effects.json", components)
    write_json(aggregate / "analysis.json", result)
    write_json(
        aggregate / "failure_ledger.json",
        {
            "schema_version": "orion.v2.real-problem-failure-ledger.v1",
            "statuses": {
                arm: summary["status_counts"] for arm, summary in summaries.items()
            },
            "raw_repetition_audit": repetition_audit,
            "missingness_preserved": True,
            "null_and_adverse_outcomes_preserved": True,
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
    parser.add_argument(
        "--workdir", type=Path, default=Path(".orion-real-problem-suite")
    )
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
