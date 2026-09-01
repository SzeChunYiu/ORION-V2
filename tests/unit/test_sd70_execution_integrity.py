from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "scripts" / "run_scientific_development_meta_suite.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("sd70_runner", RUNNER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixture(workdir: Path, arm: str = "F2_RECURSIVE_META_DISCOVERY_FULL") -> None:
    request = workdir / "requests" / arm / "sd70-0000.json"
    request.parent.mkdir(parents=True)
    request.write_text(
        json.dumps(
            {
                "schema_version": "orion.v2.sd70-agent-request.v1",
                "task_id": "sd70-0000",
                "arm_id": arm,
                "task": {
                    "task_id": "sd70-0000",
                    "training_episodes": [],
                    "query_context_features": ["ctx-a"],
                    "candidate_actions": ["act-a", "act-b"],
                },
                "gold_access": "NONE",
                "outcome_access": "NONE",
                "scientific_truth_authorized": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (workdir / "private_oracle.json").write_text(
        json.dumps(
            {
                "schema_version": "orion.v2.sd70-generated-meta-policy.private.v1",
                "seed": 1,
                "task_count": 1,
                "tasks": [{"task_id": "sd70-0000", "correct_action": "act-a"}],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_stub(path: Path, *, status: str, selected_action: str | None, assert_oracle_absent: bool = True) -> None:
    path.write_text(
        f"""#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--request', type=Path, required=True)
parser.add_argument('--response', type=Path, required=True)
args = parser.parse_args()
request = json.loads(args.request.read_text(encoding='utf-8'))
if {assert_oracle_absent!r} and (args.request.parents[3] / 'private_oracle.json').exists():
    raise SystemExit(9)
args.response.parent.mkdir(parents=True, exist_ok=True)
args.response.write_text(json.dumps({{
    'schema_version': 'orion.v2.sd70-agent-response.v1',
    'task_id': request['task_id'],
    'arm_id': request['arm_id'],
    'status': {status!r},
    'selected_action': {selected_action!r},
    'principle_summary': 'synthetic fixture',
    'preconditions': [],
    'contraindications': [],
    'failure_modes': [],
    'uncertainty': 'fixture',
    'falsifier': 'fixture mismatch',
    'resource_receipt': {{'model_calls': {1 if status == 'COMPLETED_PROPOSAL_ONLY' else 0}, 'executor': 'synthetic'}},
    'scientific_truth_authorized': False,
    'causal_law_authorized': False,
    'field_status_authorized': False,
}}, indent=2, sort_keys=True) + '\\n', encoding='utf-8')
""",
        encoding="utf-8",
    )


def _set_arm(monkeypatch: pytest.MonkeyPatch, script: Path) -> None:
    monkeypatch.setenv("ORION_SD70_ARM_COMMAND", f"{sys.executable} {script}")


def test_dispatch_rejects_zero_exit_failed_model_response_and_restores_oracle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runner = _load_runner()
    arm = "F2_RECURSIVE_META_DISCOVERY_FULL"
    _fixture(tmp_path, arm)
    private_before = (tmp_path / "private_oracle.json").read_bytes()
    stub = tmp_path / "failed_arm.py"
    _write_stub(stub, status="EXECUTION_FAILED_MODEL_RESPONSE", selected_action=None)
    _set_arm(monkeypatch, stub)

    with pytest.raises(RuntimeError, match="responses failed integrity validation"):
        runner.dispatch(tmp_path, [arm], max_concurrency=1, overwrite=False)

    assert (tmp_path / "private_oracle.json").read_bytes() == private_before
    receipt = json.loads((tmp_path / "DISPATCH_RECEIPT.json").read_text())
    assert receipt["all_returncodes_zero"] is True
    assert receipt["all_responses_completed"] is False
    assert receipt["dispatch_integrity_passed"] is False
    assert receipt["responses"][0]["error"] == "NONCOMPLETED_RESPONSE_STATUS"


def test_dispatch_accepts_valid_gold_blind_response_and_evaluate_scores_known_answer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runner = _load_runner()
    arm = "F2_RECURSIVE_META_DISCOVERY_FULL"
    _fixture(tmp_path, arm)
    stub = tmp_path / "valid_arm.py"
    _write_stub(stub, status="COMPLETED_PROPOSAL_ONLY", selected_action="act-a")
    _set_arm(monkeypatch, stub)

    runner.dispatch(tmp_path, [arm], max_concurrency=1, overwrite=False)
    runner.evaluate(tmp_path, [arm])

    receipt = json.loads((tmp_path / "DISPATCH_RECEIPT.json").read_text())
    summary = json.loads((tmp_path / "EVALUATION_SUMMARY.json").read_text())
    assert receipt["dispatch_integrity_passed"] is True
    assert summary["arms"][arm] == {"accuracy": 1.0, "completed": 1, "correct": 1}


def test_dispatch_validates_preexisting_responses_instead_of_empty_all_true(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runner = _load_runner()
    arm = "F2_RECURSIVE_META_DISCOVERY_FULL"
    _fixture(tmp_path, arm)
    unused_stub = tmp_path / "unused.py"
    _write_stub(unused_stub, status="COMPLETED_PROPOSAL_ONLY", selected_action="act-a")
    _set_arm(monkeypatch, unused_stub)
    response = tmp_path / "responses" / arm / "sd70-0000.json"
    response.parent.mkdir(parents=True)
    response.write_text(
        json.dumps(
            {
                "task_id": "sd70-0000",
                "arm_id": arm,
                "status": "EXECUTION_FAILED_MODEL_RESPONSE",
                "selected_action": None,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="responses failed integrity validation"):
        runner.dispatch(tmp_path, [arm], max_concurrency=1, overwrite=False)

    receipt = json.loads((tmp_path / "DISPATCH_RECEIPT.json").read_text())
    assert receipt["executed_job_count"] == 0
    assert receipt["all_returncodes_zero"] is True
    assert receipt["all_responses_completed"] is False


def test_evaluate_rejects_failed_or_missing_response(tmp_path: Path) -> None:
    runner = _load_runner()
    arm = "F2_RECURSIVE_META_DISCOVERY_FULL"
    _fixture(tmp_path, arm)

    with pytest.raises(RuntimeError, match="response integrity failed"):
        runner.evaluate(tmp_path, [arm])
