from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from orion_v2.parity_closeout import (
    validate_parity_protocol,
    validate_parity_subject_binding,
)


ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "research" / "evaluation" / "V1_PARITY_CAMPAIGN_PROTOCOL_WAVE06_V1.json"
BINDING = ROOT / "research" / "evaluation" / "V1_PARITY_SUBJECT_BINDING_WAVE06_V1.json"
CENSUS = ROOT / "provenance" / "V1_CAPABILITY_CENSUS_V1.json"
KERNEL = ROOT / "src" / "orion_v2" / "kernel.py"
KERNEL_DISPOSITION = ROOT / "research" / "framework" / "KERNEL_COMPONENT_DISPOSITION_WAVE06_V1.json"
PACKAGE_ROOT = ROOT / "src" / "orion_v2" / "__init__.py"
EXPECTED_SUBJECT = "f33d2f45554583f9e612f7a186b7d92e6bc8d01a"


def _git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def _load() -> tuple[dict, dict]:
    return (
        json.loads(PROTOCOL.read_text(encoding="utf-8")),
        json.loads(CENSUS.read_text(encoding="utf-8")),
    )


def _load_binding() -> dict:
    return json.loads(BINDING.read_text(encoding="utf-8"))


def test_frozen_parity_design_covers_all_59_capabilities_exactly_once() -> None:
    protocol, census = _load()
    result = validate_parity_protocol(protocol, census)
    assert result.valid, result.errors
    assert result.campaign_count == 9
    assert result.capability_count == 59
    assert result.terminal == "PARITY_PROTOCOL_READY_TO_BIND_V2_SUBJECT"


def test_subject_binding_is_valid_but_cannot_authorize_run() -> None:
    protocol, _ = _load()
    binding = _load_binding()
    result = validate_parity_subject_binding(
        binding,
        protocol,
        expected_subject_commit=EXPECTED_SUBJECT,
        expected_protocol_blob_sha=_git_blob_sha(PROTOCOL),
    )
    assert result.valid, result.errors
    assert result.subject_commit == EXPECTED_SUBJECT
    assert result.ci_check_count == 4
    assert result.run_authorized is False
    assert result.terminal == "PARITY_SUBJECT_BINDING_VALID_RUN_NOT_AUTHORIZED"


def test_subject_binding_blobs_match_current_contracted_boundary() -> None:
    binding = _load_binding()
    subject = binding["v2_subject"]
    assert subject["kernel_facade_blob_sha"] == _git_blob_sha(KERNEL)
    assert subject["kernel_disposition_blob_sha"] == _git_blob_sha(KERNEL_DISPOSITION)
    assert subject["package_root_blob_sha"] == _git_blob_sha(PACKAGE_ROOT)


def test_subject_drift_is_rejected() -> None:
    protocol, _ = _load()
    mutated = copy.deepcopy(_load_binding())
    mutated["v2_subject"]["commit"] = "0" * 40
    result = validate_parity_subject_binding(
        mutated,
        protocol,
        expected_subject_commit=EXPECTED_SUBJECT,
        expected_protocol_blob_sha=_git_blob_sha(PROTOCOL),
    )
    assert not result.valid
    assert any("subject commit differs" in error for error in result.errors)


def test_outcome_access_before_binding_is_rejected() -> None:
    protocol, _ = _load()
    mutated = copy.deepcopy(_load_binding())
    mutated["custody"]["outcome_access_before_binding"] = True
    result = validate_parity_subject_binding(
        mutated,
        protocol,
        expected_subject_commit=EXPECTED_SUBJECT,
        expected_protocol_blob_sha=_git_blob_sha(PROTOCOL),
    )
    assert not result.valid
    assert any("outcome_access_before_binding=false" in error for error in result.errors)


def test_binding_cannot_self_authorize_execution() -> None:
    protocol, _ = _load()
    mutated = copy.deepcopy(_load_binding())
    mutated["run_gate"]["allowed_now"] = True
    result = validate_parity_subject_binding(
        mutated,
        protocol,
        expected_subject_commit=EXPECTED_SUBJECT,
        expected_protocol_blob_sha=_git_blob_sha(PROTOCOL),
    )
    assert not result.valid
    assert any("cannot authorize" in error for error in result.errors)


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
