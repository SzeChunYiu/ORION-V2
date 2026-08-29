from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "run_orion_real_problem_suite.py"
SPEC = importlib.util.spec_from_file_location("orion_real_problem_runner", SCRIPT)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def _manifest() -> dict[str, object]:
    return {
        "schema_version": "orion.v2.real-problem-suite.v1",
        "suite_id": "suite-test",
        "benchmarks": [
            {
                "benchmark_id": "bugsinpy",
                "repository": "https://example.invalid/bugsinpy.git",
                "commit": "1" * 40,
                "adapter": "bugsinpy",
            }
        ],
        "arms": [
            {"arm_id": "SIMPLE_DIRECT"},
            {"arm_id": "F2_ORION_METABOLIC_FULL"},
        ],
        "agent_protocol": {
            "required_response_fields": [
                "task_id",
                "arm_id",
                "status",
                "proposed_patch_or_artifact",
            ]
        },
        "resource_contract": {"default_wall_time_minutes_per_task": 1},
        "anti_copy_controls": ["gold withheld"],
        "authority": {
            "grants_scientific_truth": False,
            "grants_field_status": False,
        },
    }


def test_manifest_validation_is_fail_closed() -> None:
    manifest = _manifest()
    assert runner.validate_manifest(manifest) == []
    manifest["authority"]["grants_field_status"] = True
    assert "prospective suite must not grant authority" in runner.validate_manifest(manifest)


def test_issue_requests_binds_gold_blind_arm_contract(tmp_path: Path) -> None:
    frozen = {
        "schema_version": "orion.v2.frozen-real-problem-tasks.v1",
        "suite_id": "suite-test",
        "tasks": [
            {
                "task_id": "task-a",
                "benchmark_id": "bugsinpy",
                "adapter": "bugsinpy",
                "project": "pandas",
                "bug_id": 1,
            }
        ],
    }
    runner._write_json(tmp_path / "frozen_tasks.json", frozen)
    count = runner.issue_requests(
        _manifest(),
        tmp_path,
        ("F2_ORION_METABOLIC_FULL",),
        ("task-a",),
    )
    assert count == 1
    request = json.loads(
        (tmp_path / "requests" / "F2_ORION_METABOLIC_FULL" / "task-a.json").read_text()
    )
    assert request["gold_or_outcome_data_included"] is False
    assert request["requested_authority_ceiling"] == "PROPOSAL_ONLY"
    assert request["arm_contract"]["required_stages"][0] == "INGEST"
    assert "CHALLENGE" in request["arm_contract"]["required_stages"]


def test_missing_agent_command_produces_cannot_check_response(
    tmp_path: Path, monkeypatch
) -> None:
    frozen = {
        "schema_version": "orion.v2.frozen-real-problem-tasks.v1",
        "suite_id": "suite-test",
        "tasks": [
            {
                "task_id": "task-a",
                "benchmark_id": "bugsinpy",
                "adapter": "bugsinpy",
            }
        ],
    }
    runner._write_json(tmp_path / "frozen_tasks.json", frozen)
    runner.issue_requests(_manifest(), tmp_path, ("SIMPLE_DIRECT",), ("task-a",))
    monkeypatch.delenv("ORION_ARM_SIMPLE_DIRECT", raising=False)
    count = runner.dispatch_agents(
        _manifest(),
        tmp_path,
        ("SIMPLE_DIRECT",),
        ("task-a",),
        timeout_seconds=1,
    )
    assert count == 0
    response = json.loads(
        (tmp_path / "responses" / "SIMPLE_DIRECT" / "task-a.json").read_text()
    )
    assert response["status"] == "CANNOT_CHECK_MISSING_AGENT_COMMAND"
    assert response["requested_authority"] == "NONE"


def test_summary_does_not_promote_field_or_publication_status(tmp_path: Path) -> None:
    runner._write_json(
        tmp_path / "evaluations" / "F2_ORION_METABOLIC_FULL" / "task-a.json",
        {
            "task_id": "task-a",
            "arm_id": "F2_ORION_METABOLIC_FULL",
            "benchmark_id": "bugsinpy",
            "full_regression_suite_passed": True,
            "critical_new_failure_count": 0,
        },
    )
    summary = runner.summarize(tmp_path)
    assert summary["field_status"] == "NOT_ESTABLISHED"
    assert summary["publication_readiness"] == "NOT_ESTABLISHED"
