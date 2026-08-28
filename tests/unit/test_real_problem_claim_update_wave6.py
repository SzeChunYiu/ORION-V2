from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "update_paper_claims_from_real_results.py"
SPEC = importlib.util.spec_from_file_location("orion_claim_updater", SCRIPT)
assert SPEC and SPEC.loader
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def ledger() -> dict[str, object]:
    return {
        "claims": [
            {"claim_id": f"KM-C{index}", "paper_mapping": ["P_G"], "current_terminal": "OPEN"}
            for index in range(1, 9)
        ]
    }


def analysis(*, paired: int = 40, estimate: float = 0.1, lower: float = 0.02) -> dict[str, object]:
    return {
        "hard_gate_state": "PASS_DESCRIPTIVE_ONLY",
        "primary_comparisons": [
            {
                "left_arm": "F2_ORION_METABOLIC_FULL",
                "right_arm": "F0_PARENT_FEDERATION",
                "paired_task_count": paired,
                "success": {
                    "risk_difference": {
                        "estimate": estimate,
                        "ci95": [lower, 0.18],
                    }
                },
            }
        ],
        "component_effects": {
            "F2_MINUS_DECOMPOSITION": {
                "component_disposition": "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE"
            },
            "F2_MINUS_NATIVE_RECOVERY": {
                "component_disposition": "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE"
            },
            "F2_MINUS_COUNTERPROBE": {
                "component_disposition": "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE"
            },
            "F2_MINUS_SELECTIVE_REOPEN": {
                "component_disposition": "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE"
            },
        },
    }


def test_underpowered_run_cannot_support_primary_claim(tmp_path: Path) -> None:
    result = updater.update_claims(ledger(), analysis(paired=10), tmp_path)
    primary = next(item for item in result["claim_updates"] if item["claim_id"] == "KM-C3")
    assert primary["proposed_status"] == "PILOT_OR_UNDERPOWERED"
    assert result["field_status"] == "NOT_ESTABLISHED"
    assert result["publication_readiness"] == "NOT_ESTABLISHED"


def test_positive_bounded_debugging_result_still_does_not_found_field(tmp_path: Path) -> None:
    for benchmark in ("bugsinpy", "causalbench"):
        write_json(
            tmp_path / "evaluations" / "F2_ORION_METABOLIC_FULL" / f"{benchmark}.json",
            {
                "task_id": benchmark,
                "arm_id": "F2_ORION_METABOLIC_FULL",
                "benchmark_id": benchmark,
            },
        )
    result = updater.update_claims(ledger(), analysis(), tmp_path)
    primary = next(item for item in result["claim_updates"] if item["claim_id"] == "KM-C3")
    paper = next(item for item in result["claim_updates"] if item["claim_id"] == "KM-C8")
    assert primary["proposed_status"] == "SUPPORTED_IN_BOUNDED_DEBUGGING_TRANCHE"
    assert paper["proposed_status"] == "P_G_STANDALONE_CANDIDATE_FOR_INDEPENDENT_REVIEW"
    assert result["authority"]["submission_readiness"] is False
    assert result["automatic_manuscript_editing_authorized"] is False


def test_parent_tie_or_win_is_retained(tmp_path: Path) -> None:
    result = updater.update_claims(ledger(), analysis(estimate=-0.02, lower=-0.1), tmp_path)
    primary = next(item for item in result["claim_updates"] if item["claim_id"] == "KM-C3")
    assert primary["proposed_status"] == "PARENT_TIE_OR_WIN"
