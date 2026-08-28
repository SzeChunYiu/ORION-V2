from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


evaluator = load_script(
    "orion_real_problem_evaluator_v2",
    "scripts/evaluate_orion_real_problem_responses_v2.py",
)
analyzer = load_script(
    "orion_real_problem_analyzer",
    "scripts/analyze_orion_real_problem_results.py",
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_uncheckable_response_remains_missing_not_failure(tmp_path: Path) -> None:
    frozen = {
        "tasks": [
            {
                "task_id": "task-a",
                "benchmark_id": "bugsinpy",
                "adapter": "bugsinpy",
            }
        ],
        "benchmarks": [],
    }
    write_json(tmp_path / "frozen_tasks.json", frozen)
    write_json(
        tmp_path / "responses" / "SIMPLE_DIRECT" / "task-a.json",
        {
            "task_id": "task-a",
            "arm_id": "SIMPLE_DIRECT",
            "status": "CANNOT_CHECK_MISSING_AGENT_COMMAND",
            "proposed_patch_or_artifact": None,
            "diagnosis": "agent command missing",
        },
    )
    count = evaluator.evaluate(
        tmp_path,
        arms={"SIMPLE_DIRECT"},
        tasks={"task-a"},
        timeout_seconds=1,
    )
    assert count == 1
    result = json.loads(
        (tmp_path / "evaluations" / "SIMPLE_DIRECT" / "task-a.json").read_text()
    )
    assert result["status"] == "CANNOT_CHECK_AGENT_OR_ARTIFACT_UNAVAILABLE"
    assert result["full_regression_suite_passed"] is None
    assert result["critical_new_failure_count"] is None


def test_analyzer_computes_paired_effects_without_authority_promotion(
    tmp_path: Path,
) -> None:
    for index in range(1, 21):
        task_id = f"task-{index:02d}"
        full_success = index <= 15
        minus_success = index <= 13
        write_json(
            tmp_path / "evaluations" / "F2_ORION_METABOLIC_FULL" / f"{task_id}.json",
            {
                "task_id": task_id,
                "arm_id": "F2_ORION_METABOLIC_FULL",
                "benchmark_id": "bugsinpy",
                "full_regression_suite_passed": full_success,
                "critical_new_failure_count": 0 if full_success else 1,
                "wall_time_seconds": 2.0,
            },
        )
        write_json(
            tmp_path / "evaluations" / "F2_MINUS_DECOMPOSITION" / f"{task_id}.json",
            {
                "task_id": task_id,
                "arm_id": "F2_MINUS_DECOMPOSITION",
                "benchmark_id": "bugsinpy",
                "full_regression_suite_passed": minus_success,
                "critical_new_failure_count": 0 if minus_success else 1,
                "wall_time_seconds": 1.0,
            },
        )
        write_json(
            tmp_path / "evaluations" / "F0_PARENT_FEDERATION" / f"{task_id}.json",
            {
                "task_id": task_id,
                "arm_id": "F0_PARENT_FEDERATION",
                "benchmark_id": "bugsinpy",
                "full_regression_suite_passed": index <= 14,
                "critical_new_failure_count": 0 if index <= 14 else 1,
                "wall_time_seconds": 1.5,
            },
        )
    result = analyzer.analyze(tmp_path)
    assert result["field_status"] == "NOT_ESTABLISHED"
    assert result["supertheory_status"] == "NOT_ESTABLISHED"
    assert result["publication_readiness"] == "NOT_ESTABLISHED"
    component = result["component_effects"]["F2_MINUS_DECOMPOSITION"]
    assert component["paired_task_count"] == 20
    assert component["component_disposition"] in {
        "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE",
        "PARENT_REPLACEABLE_OR_CONTEXTUAL_CANNOT_DISTINGUISH",
    }


def test_exact_discordant_pair_probability_is_symmetric() -> None:
    assert analyzer.exact_two_sided_discordant_p(3, 1) == analyzer.exact_two_sided_discordant_p(1, 3)
    assert analyzer.exact_two_sided_discordant_p(0, 0) is None
