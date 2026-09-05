"""SD70-V4 checker discipline: the XOR-square theorem's no-alarm control (V3's linear family: zero certificates),
V4 tasks certified, the planted label-ignoring mutant caught, gated-parent fidelity, and the frozen design pins."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "research" / "experiments" / "sd70-v4" / "sd70v4_run.py"


def load():
    spec = importlib.util.spec_from_file_location("sd70v4_run", RUNNER)
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


M = load()


def test_theorem_no_alarm_on_linear_family_and_certificates_on_v4() -> None:
    _, priv = M.G4.build_suite(11, 15, 16, "lin", linear_control=True)
    assert all(t["xor_square_certificates"] == 0 for t in priv["tasks"])
    _, priv4 = M.G4.build_suite(11, 15, 16, "v4")
    assert all(t["xor_square_certificates"] >= 1 for t in priv4["tasks"])
    # hand certificate: 2 features, XOR labelling {01->a, 10->a, 11->b} is not an aabb square (00 outside the domain) -> 0
    assert M.xor_square_certificates(lambda c: 0 if c != (1, 1) else 1, 2) == []
    # 3 features: base bit 1 makes the square 100/101/110/111 admissible; plant aabb
    lab = {(1, 0, 0): 0, (1, 0, 1): 1, (1, 1, 0): 1, (1, 1, 1): 0}
    assert len(M.xor_square_certificates(lambda c: lab.get(c, 2), 3)) >= 1


def test_planted_mutant_fires_on_linear_and_is_caught_by_selftest(tmp_path: Path) -> None:
    _, priv = M.G3.build_suite(5, 5, 16, "v3")
    t = priv["tasks"][0]
    assert M.xor_square_certificates(lambda c, w=t["latent_weights"]: M.G3.best_action(c, w), len(t["latent_feature_tokens"]), mutant_ignore_labels=True)
    assert M.stage_selftest(tmp_path) == 0
    rep = json.loads((tmp_path / "SD70_V4_SELFTEST_V1.json").read_text())
    assert rep["planted_mutant_caught"]["pass"] and rep["gated_parent_fidelity"]["pass"]


def test_dev_smoke_runs_controls(tmp_path: Path) -> None:
    assert M.stage_dev(tmp_path, 1, 6) == 0
    res = json.loads((tmp_path / "SD70_V4_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert res["task_total"] == 6 and res["certificates_per_task"]["min"] >= 1
    assert "GATED_MAXMARGIN_PARENT" in res["arms"] and "F0_PLUS_FEDERATION" in res["arms"]


def test_design_pins_current_substrate() -> None:
    d = json.loads(M.DESIGN_JSON.read_text())
    assert d["substrate_pins_sha256"] == M.pins()
