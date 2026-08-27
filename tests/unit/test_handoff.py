import json
from pathlib import Path

from orion_v2.handoff import load_and_validate, validate_handoff_receipt


ROOT = Path(__file__).resolve().parents[2]


def test_bound_repository_handoff_receipt_is_valid() -> None:
    result = load_and_validate(ROOT / "provenance" / "ORION_V1_HANDOFF_RECEIPT_V1.json")
    assert result.valid, result.errors


def test_handoff_cannot_authorize_scientific_claims() -> None:
    path = ROOT / "provenance" / "ORION_V1_HANDOFF_RECEIPT_V1.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    receipt["permissions"]["scientific_claim_promotion_authorized"] = True
    result = validate_handoff_receipt(receipt)
    assert result.valid is False
    assert any("scientific claim promotion" in error for error in result.errors)
