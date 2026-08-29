#!/usr/bin/env python3
"""Summarize convergent anti-copy controls across historical and fresh tasks."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


class AntiCopyError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AntiCopyError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AntiCopyError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_evaluations(workdir: Path) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in (workdir / "evaluations").glob("*/*.json"):
        item = read_json(path)
        result[path.parent.name].append(item)
    return dict(result)


def success_rate(items: list[dict[str, Any]]) -> tuple[int, int, float | None]:
    observed = [
        item.get("native_success", item.get("full_regression_suite_passed"))
        for item in items
    ]
    binary = [value for value in observed if isinstance(value, bool)]
    return len(binary), sum(binary), sum(binary) / len(binary) if binary else None


def summarize(historical_workdir: Path, fresh_workdir: Path) -> dict[str, Any]:
    generation = read_json(fresh_workdir / "aggregate" / "counterfactual_generation.json")
    fresh = load_evaluations(fresh_workdir)
    historical = load_evaluations(historical_workdir) if historical_workdir.exists() else {}
    arms = sorted(set(fresh) | set(historical))
    arm_results: dict[str, Any] = {}
    for arm in arms:
        fresh_count, fresh_pass, fresh_rate = success_rate(fresh.get(arm, []))
        historical_count, historical_pass, historical_rate = success_rate(historical.get(arm, []))
        critical = sum(
            int(bool(item.get("critical_false_completion")))
            for item in fresh.get(arm, [])
            if item.get("critical_false_completion") is not None
        )
        arm_results[arm] = {
            "fresh_counterfactual_count": fresh_count,
            "fresh_counterfactual_passed": fresh_pass,
            "fresh_counterfactual_pass_rate": fresh_rate,
            "historical_count": historical_count,
            "historical_passed": historical_pass,
            "historical_pass_rate": historical_rate,
            "fresh_critical_false_completion_count": critical,
        }

    f2 = arm_results.get("F2_ORION_METABOLIC_FULL", {})
    f2_count = int(f2.get("fresh_counterfactual_count", 0) or 0)
    f2_pass = int(f2.get("fresh_counterfactual_passed", 0) or 0)
    f2_critical = int(f2.get("fresh_critical_false_completion_count", 0) or 0)
    supported = bool(
        generation.get("generated_count", 0) >= 5
        and generation.get("gold_exposed_to_solver") is False
        and f2_count >= 5
        and f2_pass > 0
        and f2_critical == 0
    )
    return {
        "schema_version": "orion.v2.anti-copy-controls.v1",
        "counterfactual_generation": generation,
        "arm_results": arm_results,
        "control_status": {
            "post_freeze_generation": generation.get("generated_count", 0) > 0,
            "gold_withheld": generation.get("gold_exposed_to_solver") is False,
            "execution_scoring": True,
            "fresh_counterfactual_results_present": bool(fresh),
            "historical_results_present": bool(historical),
        },
        "counterfactual_success_supported": supported,
        "interpretation": (
            "bounded convergent evidence of active problem solving"
            if supported
            else "anti-copy evidence incomplete, negative or underpowered"
        ),
        "non_claims": [
            "does not prove absence of all related training data",
            "does not establish general intelligence",
            "does not establish F2 superiority or field status",
        ],
        "scientific_truth_authorized": False,
        "field_status_authorized": False,
        "publication_readiness_authorized": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--historical-workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument("--fresh-workdir", type=Path, default=Path(".orion-fresh-counterfactual-suite"))
    parser.add_argument("--output-workdir", type=Path, default=Path(".orion-real-problem-suite"))
    args = parser.parse_args(argv)
    try:
        result = summarize(args.historical_workdir, args.fresh_workdir)
        write_json(args.output_workdir / "aggregate" / "anti_copy_controls.json", result)
    except (AntiCopyError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
