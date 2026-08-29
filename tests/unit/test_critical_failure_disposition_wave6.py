from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOSURE = ROOT / "research/closure"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def test_all_retained_failure_record_blobs_are_bound() -> None:
    receipt = _load(CLOSURE / "CRITICAL_FAILURE_DISPOSITION_WAVE06_V1.json")
    for row in receipt["reviewed_failure_records"]:
        path = ROOT / row["path"]
        assert path.exists()
        assert _git_blob_sha(path) == row["git_blob_sha"]
        assert row["critical_open"] is False


def test_local_critical_defect_gate_is_scoped_and_zero() -> None:
    receipt = _load(CLOSURE / "CRITICAL_FAILURE_DISPOSITION_WAVE06_V1.json")
    gate = receipt["gate_disposition"]
    assert gate["G7_CRITICAL_FAILURES"] == "LOCALLY_SATISFIED_NO_KNOWN_OPEN_CRITICAL_DEFECTS"
    assert gate["open_critical_failures"] == 0
    assert gate["historical_failure_records_deleted"] is False
    assert receipt["status"] == "NO_KNOWN_OPEN_CRITICAL_LOCAL_DEFECTS_OTHER_EVIDENCE_GATES_REMAIN"


def test_unresolved_scientific_evidence_is_not_laundered_as_repaired_defect() -> None:
    receipt = _load(CLOSURE / "CRITICAL_FAILURE_DISPOSITION_WAVE06_V1.json")
    text = "\n".join(receipt["not_classified_as_g7_critical_defects"])
    for token in ("semantic evaluator", "parent-composed", "parity", "prospective", "publication"):
        assert token in text.lower()
    assert receipt["authority"]["grants_v1_parity"] is False
    assert receipt["authority"]["grants_protected_scientific_value"] is False
    assert receipt["authority"]["grants_v2_closeout"] is False


def test_current_verification_receipt_requires_four_successful_convergence_lanes() -> None:
    receipt = _load(CLOSURE / "CRITICAL_FAILURE_DISPOSITION_WAVE06_V1.json")
    workflows = receipt["current_verification"]["workflows"]
    assert {row["name"] for row in workflows} == {
        "wave3-generalization-reference",
        "wave4-native-recovery",
        "wave5-stochastic-generalization",
        "wave6-unified-generalization",
    }
    assert all(row["conclusion"] == "success" for row in workflows)


def test_failure_ledger_no_longer_labels_failure_vocabulary_as_open_defects() -> None:
    text = (ROOT / "FAILURE_LEDGER.md").read_text(encoding="utf-8")
    assert "## Retained failure classes" in text
    assert "not a claim that every class currently has an open critical defect" in text
    assert "CRITICAL_FAILURE_DISPOSITION_WAVE06_V1.json" in text
