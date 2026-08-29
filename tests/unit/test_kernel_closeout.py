from __future__ import annotations

import copy
import json
from pathlib import Path

from orion_v2.kernel_closeout import validate_kernel_disposition


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "research" / "framework" / "KERNEL_COMPONENT_DISPOSITION_WAVE06_V1.json"
SRC = ROOT / "src" / "orion_v2"


def _load() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_current_kernel_candidate_is_coherent_and_ready_for_parity_not_frozen() -> None:
    result = validate_kernel_disposition(_load(), source_root=SRC)
    assert result.valid, result.errors
    assert result.family_count == 7
    assert result.unresolved_duplicate_count == 0
    assert result.terminal == "KERNEL_CANDIDATE_READY_FOR_PROTECTED_FREEZE_RECEIPT"


def test_missing_kernel_family_fails_closed() -> None:
    mutated = _load()
    mutated["families"] = mutated["families"][:-1]
    result = validate_kernel_disposition(mutated, source_root=SRC)
    assert not result.valid
    assert any("K0..K6" in error for error in result.errors)


def test_interface_cannot_have_two_kernel_owners() -> None:
    mutated = _load()
    shared = mutated["families"][0]["interface_candidates"][0]
    mutated["families"][1]["interface_candidates"].append(shared)
    result = validate_kernel_disposition(mutated, source_root=SRC)
    assert not result.valid
    assert any("multiple owners" in error for error in result.errors)


def test_parent_reference_implementation_cannot_masquerade_as_stable_interface() -> None:
    mutated = _load()
    mutated["families"][5]["interface_candidates"].append("frontier_portfolio")
    result = validate_kernel_disposition(mutated, source_root=SRC)
    assert not result.valid
    assert any("parent/reference" in error for error in result.errors)


def test_open_duplicate_groups_prevent_kernel_freeze() -> None:
    mutated = _load()
    mutated["unresolved_duplicate_groups"] = [
        {
            "group_id": "FORGED-DUPLICATE",
            "modules": ["structural", "correspondence"],
            "required_disposition": "choose one stable owner",
        }
    ]
    mutated["kernel_frozen"] = True
    result = validate_kernel_disposition(mutated, source_root=SRC)
    assert not result.valid
    assert any("cannot be frozen" in error for error in result.errors)


def test_planning_manifest_cannot_self_freeze_after_duplicates_are_dispositioned() -> None:
    mutated = _load()
    mutated["kernel_frozen"] = True
    result = validate_kernel_disposition(mutated, source_root=SRC)
    assert not result.valid
    assert any("cannot self-freeze" in error for error in result.errors)


def test_authority_minting_is_invalid() -> None:
    mutated = _load()
    mutated["grants_architecture_authority"] = True
    result = validate_kernel_disposition(mutated, source_root=SRC)
    assert not result.valid
    assert any("grants_architecture_authority" in error for error in result.errors)


def test_interface_module_must_exist() -> None:
    mutated = _load()
    mutated["families"][0]["interface_candidates"] = ["does_not_exist"]
    result = validate_kernel_disposition(mutated, source_root=SRC)
    assert not result.valid
    assert any("no source module" in error for error in result.errors)
