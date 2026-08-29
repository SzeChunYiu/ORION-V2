from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "render_orion_paper_result_tables.py"
SPEC = importlib.util.spec_from_file_location("orion_paper_renderer", SCRIPT)
assert SPEC and SPEC.loader
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_renderer_writes_tables_without_editing_or_authorizing(tmp_path: Path) -> None:
    write_json(
        tmp_path / "aggregate" / "analysis.json",
        {
            "arm_summaries": {
                "F2_ORION_METABOLIC_FULL": {
                    "task_count": 2,
                    "success_count": 1,
                    "success_rate": 0.5,
                    "critical_failure_count": 0,
                    "critical_failure_rate": 0.0,
                    "mean_wall_time_seconds": 2.0,
                    "median_wall_time_seconds": 2.0,
                    "status_counts": {"NATIVE_EVALUATION_COMPLETE": 2},
                }
            },
            "primary_comparisons": [],
            "component_effects": {},
        },
    )
    write_json(
        tmp_path / "aggregate" / "paper_claim_updates.json",
        {
            "claim_updates": [
                {
                    "claim_id": "KM-C3",
                    "paper_mapping": ["P_C", "P_G"],
                    "proposed_status": "PILOT_OR_UNDERPOWERED",
                    "reason": "two tasks only",
                    "evidence_artifacts": ["aggregate/analysis.json"],
                    "requires_independent_review": True,
                }
            ]
        },
    )
    artifact_map = tmp_path / "artifact-map.json"
    write_json(
        artifact_map,
        {
            "papers": [
                {
                    "paper_id": "P_G",
                    "manuscript": "papers/prospectuses/P_G.md",
                    "required_artifacts": ["aggregate/analysis.json", "independent review"],
                    "kill_terminal": "MERGE",
                }
            ]
        },
    )
    result = renderer.render(tmp_path, artifact_map)
    assert result["automatic_manuscript_editing"] is False
    assert result["publication_readiness_authorized"] is False
    assert (tmp_path / "paper_exports" / "arm_summary.md").exists()
    readiness = (tmp_path / "paper_exports" / "paper_readiness.md").read_text()
    assert "NOT_SUBMISSION_READY" in readiness
    assert "independent review" in readiness
