from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("h_ext1n_secondary_cell", ROOT / "scripts" / "h_ext1n_secondary_cell.py")
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

FREEZE = json.loads((ROOT / "research/experiments/h-ext1-naturalistic/H_EXT1N_SECONDARY_CELL_FREEZE_V1.json").read_text())


def _rows(n_per_stratum: int, m_dep_ok: int, m_ind_ok: int, parent_delta: int = 0) -> list[dict]:
    rows = []
    i = 0
    for stratum in ("NS1A", "NS1C", "NS1B", "NS1D"):
        dependent = stratum in ("NS1A", "NS1C")
        ok_budget = m_dep_ok if dependent else m_ind_ok
        for k in range(n_per_stratum):
            i += 1
            m_ok = k < ok_budget
            off_ok = not dependent
            parent_ok = m_ok if k >= parent_delta else False
            rows.append({
                "task_id": f"n1-{i:04d}", "topic": "hypertension", "study_id": "N1-K3",
                "oracle_stratum_reporting_only": stratum,
                "features": {"w_dup_hash": dependent, "w_shared_root": dependent, "w_declared_overlap": False,
                             "w_xref_root": dependent, "w_shared_token": True, "n_records": 3,
                             "n_roots": 2 if dependent else 3, "root_ratio": 1.5 if dependent else 1.0},
                "arms": {mod.ARM_M: {"present": True, "correct": m_ok, "actual": {"independent_support_family_count": 2 if dependent else 3}},
                         mod.ARM_OFF: {"present": True, "correct": off_ok, "actual": {"independent_support_family_count": 3}},
                         mod.ARM_PARENT: {"present": True, "correct": parent_ok, "actual": {}}},
            })
    return rows


def _instances(rows: list[dict]) -> dict:
    return {"split": "EVAL", "corpus_freeze_sha256": FREEZE["corpus_freeze_sha256"], "rows": rows}


def _answers(rows: list[dict]) -> dict:
    return {r["task_id"]: {"independent_support_family_count": 2 if r["oracle_stratum_reporting_only"] in ("NS1A", "NS1C") else 3}
            for r in rows}


def test_detection_and_preservation_pass_routes_recoverable() -> None:
    rows = _rows(20, m_dep_ok=19, m_ind_ok=20)
    res = mod.analyze(_instances(rows), FREEZE, set(), _answers(rows), {"selected_gate": None})
    assert res["validity"]["pass"] is True
    assert res["terminal"] == "DEPENDENCE_STRUCTURE_RECOVERABLE_FROM_NATURALISTIC_RECORDS"
    a = res["endpoints"]["A_DETECTION"]
    assert a["pass"] is True and a["acc_M_dependent"] == 0.95 and a["mcnemar_exact_p"] < 0.01
    assert res["endpoints"]["B_PRESERVATION"]["pass"] is True
    # witness informativeness is reported for every candidate gate, never routed on
    w = res["reporting_only"]["witness_informativeness_vs_oracle"]
    assert set(w) == set(mod.G.CANDIDATE_GATES)
    assert w["G_A_PROVENANCE_WITNESS"]["recall"] == 1.0 and w["G_A_PROVENANCE_WITNESS"]["precision"] == 1.0


def test_low_detection_routes_not_detected() -> None:
    rows = _rows(20, m_dep_ok=10, m_ind_ok=20)
    res = mod.analyze(_instances(rows), FREEZE, set(), _answers(rows), None)
    assert res["terminal"] == "DEPENDENCE_NOT_DETECTED_IN_NATURALISTIC_RECORDS"
    assert res["endpoints"]["A_DETECTION"]["pass"] is False


def test_over_triggering_routes_over_triggers() -> None:
    rows = _rows(20, m_dep_ok=20, m_ind_ok=15)
    res = mod.analyze(_instances(rows), FREEZE, set(), _answers(rows), None)
    assert res["terminal"] == "DEPENDENCE_MODELLING_OVER_TRIGGERS_ON_NATURALISTIC_RECORDS"


def test_parent_axis_routes_independently() -> None:
    rows = _rows(20, m_dep_ok=19, m_ind_ok=20, parent_delta=0)
    res = mod.analyze(_instances(rows), FREEZE, set(), _answers(rows), None)
    assert res["endpoints"]["C_PARENT_SUFFICIENCY"]["terminal"] == "STRONGEST_PARENT_SUFFICIENT_ON_NATURALISTIC_RECORDS"
    rows = _rows(20, m_dep_ok=20, m_ind_ok=20, parent_delta=12)
    res = mod.analyze(_instances(rows), FREEZE, set(), _answers(rows), None)
    c = res["endpoints"]["C_PARENT_SUFFICIENCY"]
    assert c["terminal"] == "DEPENDENCE_AWARE_ARM_BEATS_STRONGEST_PARENT_ON_NATURALISTIC_RECORDS"
    assert c["mcnemar_exact_p"] < 0.05


def test_missing_or_overlap_routes_cannot_check() -> None:
    rows = _rows(20, m_dep_ok=19, m_ind_ok=20)
    rows[0]["arms"][mod.ARM_M]["present"] = False
    res = mod.analyze(_instances(rows), FREEZE, set(), _answers(rows), None)
    assert res["terminal"] == "CANNOT_CHECK_RUN_INVALID" and "endpoints" not in res
    rows = _rows(20, m_dep_ok=19, m_ind_ok=20)
    res = mod.analyze(_instances(rows), FREEZE, {"n1-0001"}, _answers(rows), None)
    assert res["terminal"] == "CANNOT_CHECK_RUN_INVALID"
    inst = _instances(_rows(20, m_dep_ok=19, m_ind_ok=20))
    inst["corpus_freeze_sha256"] = "0" * 64
    res = mod.analyze(inst, FREEZE, set(), _answers(inst["rows"]), None)
    assert res["terminal"] == "CANNOT_CHECK_RUN_INVALID"


def test_family_count_error_distribution() -> None:
    rows = _rows(20, m_dep_ok=20, m_ind_ok=20)
    res = mod.analyze(_instances(rows), FREEZE, set(), _answers(rows), None)
    assert res["reporting_only"]["family_count_error_M"] == {"+0": 80}
    assert res["reporting_only"]["family_count_error_OFF"]["+1"] == 40
