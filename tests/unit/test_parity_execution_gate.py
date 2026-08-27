from __future__ import annotations

import copy
import json
from pathlib import Path

from orion_v2.parity_execution_gate import (
    ParityExecutionStatus,
    assess_parity_execution_readiness,
)


ROOT = Path(__file__).resolve().parents[2]


def _load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _artifacts() -> dict[str, dict]:
    return {
        "protocol": _load("research/evaluation/V1_PARITY_CAMPAIGN_PROTOCOL_WAVE06_V1.json"),
        "subject_binding": _load("research/evaluation/V1_PARITY_SUBJECT_BINDING_WAVE06_V1.json"),
        "case_source_audit": _load("research/evaluation/V1_PARITY_CASE_SOURCE_AUDIT_WAVE06_V1.json"),
        "resource_protocol": _load("research/evaluation/V1_PARITY_RESOURCE_MATCHING_PROTOCOL_WAVE06_V1.json"),
        "custody_protocol": _load("research/evaluation/V1_PARITY_CUSTODY_PROTOCOL_WAVE06_V1.json"),
        "baseline_registry": _load("research/evaluation/V1_PARITY_BASELINE_REGISTRY_WAVE06_V1.json"),
    }


def test_current_preflight_stops_at_evaluator_custody() -> None:
    result = assess_parity_execution_readiness(**_artifacts())
    assert result.status is ParityExecutionStatus.BLOCKED_EVALUATOR_CUSTODY
    assert result.run_authorized is False
    assert result.grants_v1_parity is False
    assert result.grants_v2_closeout is False


def test_removing_case_binding_regresses_to_protected_case_selection() -> None:
    artifacts = _artifacts()
    custody = copy.deepcopy(artifacts["custody_protocol"])
    custody["protected_case_registry"]["bound"] = False
    artifacts["custody_protocol"] = custody
    result = assess_parity_execution_readiness(**artifacts)
    assert result.status is ParityExecutionStatus.BLOCKED_PROTECTED_CASE_SELECTION


def test_evaluator_binding_advances_to_parent_baseline_binding() -> None:
    artifacts = _artifacts()
    custody = copy.deepcopy(artifacts["custody_protocol"])
    custody["evaluator_registry"]["bound"] = True
    artifacts["custody_protocol"] = custody
    result = assess_parity_execution_readiness(**artifacts)
    assert result.status is ParityExecutionStatus.BLOCKED_PARENT_BASELINE_BINDING


def test_baseline_binding_advances_to_resource_budget_binding() -> None:
    artifacts = _artifacts()
    custody = copy.deepcopy(artifacts["custody_protocol"])
    custody["evaluator_registry"]["bound"] = True
    baselines = copy.deepcopy(artifacts["baseline_registry"])
    baselines["implementation_bindings"]["bound"] = True
    artifacts["custody_protocol"] = custody
    artifacts["baseline_registry"] = baselines
    result = assess_parity_execution_readiness(**artifacts)
    assert result.status is ParityExecutionStatus.BLOCKED_RESOURCE_BUDGET_BINDING


def test_all_bindings_only_authorize_run_not_parity_or_scientific_truth() -> None:
    artifacts = _artifacts()
    custody = copy.deepcopy(artifacts["custody_protocol"])
    custody["evaluator_registry"]["bound"] = True
    baselines = copy.deepcopy(artifacts["baseline_registry"])
    baselines["implementation_bindings"]["bound"] = True
    resources = copy.deepcopy(artifacts["resource_protocol"])
    resources["case_budget_manifest"]["bound"] = True
    artifacts["custody_protocol"] = custody
    artifacts["baseline_registry"] = baselines
    artifacts["resource_protocol"] = resources
    result = assess_parity_execution_readiness(**artifacts)
    assert result.status is ParityExecutionStatus.READY_FOR_PROTECTED_PARITY_RUN
    assert result.run_authorized is True
    assert result.grants_v1_parity is False
    assert result.grants_v2_closeout is False
    assert result.grants_scientific_truth is False
    assert result.grants_novelty is False


def test_invalid_or_self_authorizing_design_fails_before_all_other_gates() -> None:
    artifacts = _artifacts()
    protocol = copy.deepcopy(artifacts["protocol"])
    protocol["run_gate"]["allowed_now"] = True
    artifacts["protocol"] = protocol
    result = assess_parity_execution_readiness(**artifacts)
    assert result.status is ParityExecutionStatus.INVALID_PROTOCOL
    assert result.run_authorized is False
