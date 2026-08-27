from __future__ import annotations

import copy
import json
from pathlib import Path

from orion_v2.parity_sources import validate_parity_case_source_audit


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "research" / "evaluation" / "V1_PARITY_CASE_SOURCE_AUDIT_WAVE06_V1.json"


def _load() -> dict:
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_v1_native_case_source_audit_is_valid_but_protected_selection_stays_open() -> None:
    result = validate_parity_case_source_audit(_load())
    assert result.valid, result.errors
    assert result.covered_campaign_count == 9
    assert result.source_count >= 10
    assert result.partial_campaign_ids == ("PARITY-C", "PARITY-D")
    assert result.run_authorized is False
    assert result.terminal == "V1_NATIVE_CASE_SOURCES_VALID_PROTECTED_SELECTION_OPEN"


def test_unknown_campaign_mapping_fails_closed() -> None:
    mutated = copy.deepcopy(_load())
    mutated["audited_sources"][0]["campaign_ids"].append("PARITY-Z")
    result = validate_parity_case_source_audit(mutated)
    assert not result.valid
    assert any("unknown campaigns" in error for error in result.errors)


def test_duplicate_source_identity_fails_closed() -> None:
    mutated = copy.deepcopy(_load())
    mutated["audited_sources"][1]["source_id"] = mutated["audited_sources"][0]["source_id"]
    result = validate_parity_case_source_audit(mutated)
    assert not result.valid
    assert any("source identities" in error for error in result.errors)


def test_source_without_falsifier_is_not_valid_provenance() -> None:
    mutated = copy.deepcopy(_load())
    mutated["audited_sources"][0]["falsifiers"] = []
    result = validate_parity_case_source_audit(mutated)
    assert not result.valid
    assert any("lacks explicit falsifiers" in error for error in result.errors)


def test_missing_campaign_status_fails_closed() -> None:
    mutated = copy.deepcopy(_load())
    mutated["campaign_source_status"].pop()
    result = validate_parity_case_source_audit(mutated)
    assert not result.valid
    assert any("PARITY-A through PARITY-I" in error for error in result.errors)


def test_public_source_audit_cannot_self_authorize_protected_run() -> None:
    mutated = copy.deepcopy(_load())
    mutated["run_gate"]["allowed_now"] = True
    result = validate_parity_case_source_audit(mutated)
    assert not result.valid
    assert any("cannot authorize" in error for error in result.errors)


def test_public_source_audit_cannot_claim_v1_parity() -> None:
    mutated = copy.deepcopy(_load())
    mutated["authority"]["grants_v1_parity"] = True
    result = validate_parity_case_source_audit(mutated)
    assert not result.valid
    assert any("grants_v1_parity" in error for error in result.errors)
