"""ME-X2 V3 checker discipline: τ = 1.0 is M2 (identity, no-alarm); τ = 0 fires (the lever is live);
the planted G2 mutation is caught; the frozen design binds the calibration and τ*; protected refuses without authorization."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "research" / "experiments" / "me-x2-v3" / "mex2v3_run.py"


def load():
    spec = importlib.util.spec_from_file_location("mex2v3_run", RUNNER)
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


M = load()


def test_selftest_identity_lever_live_and_planted_mutation(tmp_path: Path) -> None:
    assert M.stage_selftest(tmp_path) == 0
    rep = json.loads((tmp_path / "ME_X2_V3_SELFTEST_REPORT_V1.json").read_text())
    assert rep["tau_1_identity_with_M2"] and rep["tau_1_trajectory_identity"]
    assert rep["tau_0_threshold_activity"]["instances_committed"] >= 1
    assert rep["planted_g2_fires"]


def test_frozen_design_binds_calibration_and_pins() -> None:
    d = json.loads(M.DESIGN_JSON.read_text())
    assert d["calibration_sha256"] == M.sha256_file(M.CALIBRATION_JSON)
    assert d["substrate_pins_sha256"] == M.pins()
    cal = json.loads(M.CALIBRATION_JSON.read_text())
    assert (d["tau_star"], d["selector_star"]) == (cal["tau_star"], cal["selector_star"])
    tau, sel, _ = M.calibration_rule(cal["table"], cal["table"][M.B5_ARM])
    assert (tau, sel) == (cal["tau_star"], cal["selector_star"])  # the frozen rule reproduces the frozen choice


def test_calibration_rule_planted_admissible_point_is_selected() -> None:
    cal = json.loads(M.CALIBRATION_JSON.read_text())
    table = json.loads(json.dumps(cal["table"]))
    table[M.arm_name(0.5)]["false_escalation"] = 0; table[M.arm_name(0.5)]["spec_damage"] = 0; table[M.arm_name(0.5)]["decision_rate"] = 0.999
    tau, sel, _ = M.calibration_rule(table, table[M.B5_ARM])
    assert (tau, sel) == (0.5, "MINRANK")


def test_protected_refuses_without_authorization(tmp_path: Path) -> None:
    assert not M.AUTH_FILE.exists()
    assert M.stage_protected(tmp_path, tmp_path / "no-seed", 1) == 3
