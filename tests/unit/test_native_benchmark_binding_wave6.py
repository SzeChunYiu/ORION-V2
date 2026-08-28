from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "bind_native_benchmark_evaluation.py"
SPEC = importlib.util.spec_from_file_location("orion_native_binder", SCRIPT)
assert SPEC and SPEC.loader
binder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(binder)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def frozen(tmp_path: Path) -> None:
    write_json(
        tmp_path / "frozen_tasks.json",
        {
            "tasks": [
                {
                    "task_id": "causalbench-variant-01",
                    "benchmark_id": "causalbench",
                    "adapter": "native_command",
                }
            ]
        },
    )


def native_result() -> dict[str, object]:
    return {
        "status": "NATIVE_EVALUATION_COMPLETE",
        "native_success": True,
        "protected_decision_correct": True,
        "critical_false_completion": False,
        "command_identity": "command-sha",
        "evaluator_identity": "causalbench-native-evaluator-v1",
        "data_identity_ids": ["data-sha"],
        "source_ids": ["causalbench-commit"],
        "resource_receipt": {"wall_time_seconds": 1.0},
        "primary_metrics": {"auroc": 0.8},
        "uncertainty": {"bootstrap_ci": [0.7, 0.9]},
    }


def test_native_result_is_content_bound_and_non_authorizing(tmp_path: Path) -> None:
    frozen(tmp_path)
    result_path = tmp_path / "result.json"
    artifact = tmp_path / "metrics.csv"
    write_json(result_path, native_result())
    artifact.write_text("metric,value\nauroc,0.8\n", encoding="utf-8")
    bound = binder.bind(
        tmp_path,
        result_path,
        task_id="causalbench-variant-01",
        arm_id="F2_ORION_METABOLIC_FULL",
        artifact_paths=(artifact,),
    )
    assert bound["native_success"] is True
    assert len(bound["artifact_receipts"][0]["sha256"]) == 64
    assert bound["scientific_truth_authorized"] is False
    assert bound["field_status_authorized"] is False
    assert bound["publication_readiness_authorized"] is False


def test_native_result_cannot_self_authorize(tmp_path: Path) -> None:
    frozen(tmp_path)
    value = native_result()
    value["field_status_authorized"] = True
    result_path = tmp_path / "result.json"
    write_json(result_path, value)
    with pytest.raises(binder.BindingError):
        binder.bind(
            tmp_path,
            result_path,
            task_id="causalbench-variant-01",
            arm_id="F2_ORION_METABOLIC_FULL",
            artifact_paths=(),
        )
