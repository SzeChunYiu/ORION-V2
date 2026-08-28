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
    assert result["repetition_layout"] == "SINGLE_REPETITION_COMPATIBILITY"
    assert result["expected_repetition_ids"] == ["1"]
    component = result["component_effects"]["F2_MINUS_DECOMPOSITION"]
    assert component["paired_task_count"] == 20
    assert component["component_disposition"] in {
        "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE",
        "PARENT_REPLACEABLE_OR_CONTEXTUAL_CANNOT_DISTINGUISH",
    }


def test_exact_discordant_pair_probability_is_symmetric() -> None:
    assert analyzer.exact_two_sided_discordant_p(
        3, 1
    ) == analyzer.exact_two_sided_discordant_p(1, 3)
    assert analyzer.exact_two_sided_discordant_p(0, 0) is None
    cannot_check = {
        "status": "CANNOT_CHECK_EVALUATOR_INFRASTRUCTURE",
        "native_success": False,
        "critical_new_failure_count": None,
    }
    assert analyzer.success(cannot_check) is None
    assert analyzer.critical_failure(cannot_check) is None


def test_confirmatory_repetitions_are_nested_then_holm_adjusted(tmp_path: Path) -> None:
    tasks = [
        {
            "task_id": f"bugsinpy-{'pandas' if index <= 4 else 'scrapy'}-{index}",
            "benchmark_id": "bugsinpy",
            "project": "pandas" if index <= 4 else "scrapy",
        }
        for index in range(1, 9)
    ]
    write_json(tmp_path / "RUN_IDENTITY.json", {"repetitions": 3})
    arms = (
        "F2_ORION_METABOLIC_FULL",
        "SIMPLE_DIRECT",
        "SAME_MODEL_REFLECTION",
        "F0_PARENT_FEDERATION",
    )
    for repetition in range(1, 4):
        lane = tmp_path / f"confirmatory-r{repetition}"
        write_json(lane / "frozen_tasks.json", {"tasks": tasks})
        for arm in arms:
            for task in tasks:
                task_id = task["task_id"]
                if arm == "F2_ORION_METABOLIC_FULL":
                    native_success = (
                        repetition < 3
                    )  # 2/3 strict majority -> task success
                    elapsed = {1: 1.0, 2: 2.0, 3: 100.0}[repetition]
                elif arm == "SAME_MODEL_REFLECTION":
                    native_success = repetition == 1  # 1/3 -> task failure
                    elapsed = 1.0
                elif arm == "F0_PARENT_FEDERATION" and task_id.endswith("-8"):
                    if repetition == 3:
                        continue  # T/F/missing -> CANNOT_CHECK, not a loss
                    native_success = repetition == 1
                    elapsed = 1.0
                else:
                    native_success = False
                    elapsed = 1.0
                write_json(
                    lane / "evaluations" / arm / f"{task_id}.json",
                    {
                        "task_id": task_id,
                        "arm_id": arm,
                        "benchmark_id": "bugsinpy",
                        "native_success": native_success,
                        "critical_new_failure_count": 0,
                        "wall_time_seconds": elapsed,
                        "status": (
                            "NATIVE_SUCCESS" if native_success else "NATIVE_FAILURE"
                        ),
                    },
                )

    result = analyzer.analyze(tmp_path)
    assert result["repetition_layout"] == "NESTED_WITHIN_TASK"
    assert result["expected_repetition_ids"] == ["1", "2", "3"]
    assert result["independent_task_count"] == 8
    assert result["arm_summaries"]["F2_ORION_METABOLIC_FULL"]["task_count"] == 8
    assert result["arm_summaries"]["F2_ORION_METABOLIC_FULL"]["success_count"] == 8
    assert (
        result["arm_summaries"]["F2_ORION_METABOLIC_FULL"][
            "success_instability_task_count"
        ]
        == 8
    )
    assert (
        result["repetition_audit"]["F2_ORION_METABOLIC_FULL"]["evaluation_count"] == 24
    )

    comparisons = result["primary_comparisons"]
    assert [item["right_arm"] for item in comparisons] == [
        "SIMPLE_DIRECT",
        "SAME_MODEL_REFLECTION",
        "F0_PARENT_FEDERATION",
    ]
    simple = comparisons[0]
    assert simple["paired_task_count"] == 8  # never 24 repetitions
    assert simple["success"]["paired_table"]["left_only"] == 8
    assert simple["success"]["exact_discordant_p"] == 0.0078125
    assert simple["success"]["holm_adjusted_p"] == 0.0234375
    assert simple["success"]["holm_reject_at_alpha_0_05"] is True
    assert set(simple["project_strata"]) == {"pandas", "scrapy"}
    assert simple["wall_time_seconds"]["estimate"] == 1.0

    f0 = comparisons[2]
    missing_id = "bugsinpy-scrapy-8"
    assert f0["paired_task_count"] == 8
    assert f0["success"]["checkable_task_count"] == 7
    assert f0["success"]["missing_task_ids"] == [missing_id]
    assert result["repetition_audit"]["F0_PARENT_FEDERATION"][
        "missing_repetitions_by_task"
    ] == {missing_id: ["3"]}
    assert result["primary_multiplicity"]["registered_family_size"] == 3

    paired = json.loads(
        (tmp_path / "aggregate" / "paired_comparisons.json").read_text()
    )
    assert paired["repetitions_nested_within_task"] is True
    assert paired["multiplicity"]["method"] == "HOLM_STEP_DOWN"
