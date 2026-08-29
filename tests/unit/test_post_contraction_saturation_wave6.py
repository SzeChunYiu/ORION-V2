from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOSURE = ROOT / "research/closure"


def _load(name: str) -> dict:
    return json.loads((CLOSURE / name).read_text(encoding="utf-8"))


def _git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def test_two_independent_changed_vocabulary_passes_are_bound() -> None:
    receipt = _load("POST_CONTRACTION_SATURATION_RECEIPT_WAVE06_V1.json")
    assert receipt["required_qualifying_passes"] == 2
    assert receipt["qualifying_passes"] == 2
    assert len(receipt["passes"]) == 2
    assert len({row["vocabulary"] for row in receipt["passes"]}) == 2
    assert receipt["status"] == "TWO_PASS_BOUNDED_SATURATION_REACHED"


def test_each_pass_is_complete_and_has_no_censored_or_failed_route() -> None:
    for name in (
        "SATURATION_PASS_A_FRONTIER_APPLICATION_VOCABULARY_2026-08-27_V1.json",
        "SATURATION_PASS_B_FORMAL_HISTORICAL_VOCABULARY_2026-08-27_V1.json",
    ):
        row = _load(name)
        completion = row["route_completion"]
        assert row["status"] == "COMPLETE_NO_MATERIAL_CHANGE"
        assert completion["declared_routes"] == 8
        assert completion["completed_routes"] == 8
        assert completion["censored_routes"] == []
        assert completion["failed_routes"] == []
        assert completion["all_declared_routes_dispositioned"] is True


def test_pass_blobs_match_saturation_receipt() -> None:
    receipt = _load("POST_CONTRACTION_SATURATION_RECEIPT_WAVE06_V1.json")
    for entry in receipt["passes"]:
        path = ROOT / entry["path"]
        assert _git_blob_sha(path) == entry["git_blob_sha"]


def test_no_qualifying_pass_adds_a_material_programme_object() -> None:
    forbidden_true = {
        "new_kernel_coordinate",
        "new_relation_type",
        "new_obstruction",
        "new_failure_mode",
        "new_parent_contraction",
        "new_benchmark_family",
        "new_paper_identity",
    }
    for name in (
        "SATURATION_PASS_A_FRONTIER_APPLICATION_VOCABULARY_2026-08-27_V1.json",
        "SATURATION_PASS_B_FORMAL_HISTORICAL_VOCABULARY_2026-08-27_V1.json",
    ):
        check = _load(name)["material_change_check"]
        for key in forbidden_true:
            assert check[key] is False
        assert check["bibliographic_or_parent_ownership_refinement_only"] is True


def test_saturation_receipt_is_scoped_and_non_authorizing() -> None:
    receipt = _load("POST_CONTRACTION_SATURATION_RECEIPT_WAVE06_V1.json")
    assert receipt["gate_disposition"]["G6_POST_CONTRACTION_SATURATION"] == "LOCALLY_SATISFIED"
    assert receipt["gate_disposition"]["no_material_change_passes"] == 2
    assert receipt["gate_disposition"]["all_declared_routes_dispositioned"] is True
    assert receipt["authority"]["grants_global_literature_completeness"] is False
    assert receipt["authority"]["grants_v1_parity"] is False
    assert receipt["authority"]["grants_v2_closeout"] is False
    assert receipt["authority"]["grants_novelty"] is False
