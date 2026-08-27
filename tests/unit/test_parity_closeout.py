from __future__ import annotations

import copy
import json
from pathlib import Path

from orion_v2.parity_closeout import validate_parity_protocol


ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "research" / "evaluation" / "V1_PARITY_CAMPAIGN_PROTOCOL_WAVE06_V1.json"
CENSUS = ROOT / "provenance" / "V1_CAPABILITY_CENSUS_V1.json"


def _load() -> tuple[dict, dict]:
    return (
        json.loads(PROTOCOL.read_text(encoding="utf-8")),
        json.loads(CENSUS.read_text(encoding="utf-8")),
    )


def test_frozen_parity_design_covers_all_59_capabilities_exactly_once() -> None:
    protocol, census = _load()
    result = validate_parity_protocol(protocol, census)
    assert result.valid, result.errors
    assert result.campaign_count == 9
    assert result.capability_count == 59
    assert result.terminal == "PARITY_PROTOCOL_READY_TO_BIND_V2_SUBJECT"


def test_missing_capability_fails_closed() -> None:
    protocol, census = _load()
    mutated = copy.deepcopy(protocol)
    mutated["campaigns"][0]["capability_ids"].pop()
    result = validate_parity_protocol(mutated, census)
    assert not result.valid
    assert any("missing" in error or "denominator" in error for error in result.errors)


def test_duplicate_capability_across_campaigns_fails_closed() -> None:
    protocol, census = _load()
    mutated = copy.deepcopy(protocol)
    duplicated = mutated["campaigns"][0]["capability_ids"][0]
    mutated["campaigns"][1]["capability_ids"].append(duplicated)
    result = validate_parity_protocol(mutated, census)
    assert not result.valid
    assert any("multiple campaigns" in error for error in result.errors)


def test_invented_capability_fails_closed() -> None:
    protocol, census = _load()
    mutated = copy.deepcopy(protocol)
    mutated["campaigns"][0]["capability_ids"][0] = "V2.FORGED.CAPABILITY"
    result = validate_parity_protocol(mutated, census)
    assert not result.valid
    assert any("invented" in error for error in result.errors)


def test_family_average_cannot_replace_per_cell_noncompensation() -> None:
    protocol, census = _load()
    mutated = copy.deepcopy(protocol)
    mutated["comparison_contract"]["aggregation_rule"] = "AVERAGE_BY_CAMPAIGN"
    result = validate_parity_protocol(mutated, census)
    assert not result.valid
    assert any("non-compensatory" in error for error in result.errors)


def test_design_freeze_cannot_self_authorize_execution() -> None:
    protocol, census = _load()
    mutated = copy.deepcopy(protocol)
    mutated["run_gate"]["allowed_now"] = True
    result = validate_parity_protocol(mutated, census)
    assert not result.valid
    assert any("self-authorize" in error for error in result.errors)


def test_scientific_authority_cannot_be_minted_by_parity_design() -> None:
    protocol, census = _load()
    mutated = copy.deepcopy(protocol)
    mutated["authority"]["grants_scientific_truth"] = True
    result = validate_parity_protocol(mutated, census)
    assert not result.valid
    assert any("grants_scientific_truth" in error for error in result.errors)


def test_v1_subject_drift_is_rejected() -> None:
    protocol, census = _load()
    mutated = copy.deepcopy(protocol)
    mutated["frozen_v1"]["freeze_commit"] = "0" * 40
    result = validate_parity_protocol(mutated, census)
    assert not result.valid
    assert any("different V1 commits" in error for error in result.errors)
