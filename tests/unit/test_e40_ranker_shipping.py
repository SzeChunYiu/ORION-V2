"""E40-RS: the ranker-shipping re-analysis -- constants, routing, and the synthetic plant."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[2] / "research" / "experiments" / "e40-matched"


def _load():
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    spec = importlib.util.spec_from_file_location("e40_ranker_shipping", HERE / "e40_ranker_shipping.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RS = _load()


def test_design_twin_constants_agree_with_the_script():
    dc = json.loads(RS.DESIGN_JSON.read_text())["constants"]
    assert tuple(dc["kinds"]) == RS.KINDS
    assert dc["primary_kind"] == RS.PRIMARY_KIND
    assert dc["ridge_lambda"] == RS.RIDGE_LAMBDA
    assert dc["signflip_n"] == RS.SIGNFLIP_N and dc["signflip_seed"] == RS.SIGNFLIP_SEED
    assert dc["plant_seed"] == RS.PLANT_SEED and dc["plant_noise_sd_fraction"] == RS.PLANT_NOISE_SD_FRACTION
    assert dc["plant_min_recovered_fraction"] == RS.PLANT_MIN_RECOVERED_FRACTION
    assert dc["nullcal"] == {"reps": RS.NULLCAL_REPS, "flips": RS.NULLCAL_FLIPS, "seed": RS.NULLCAL_SEED, "band": list(RS.NULLCAL_BAND)}
    assert dc["alpha"] == RS.ALPHA and dc["rs2_min_recovered_fraction"] == RS.RS2_MIN_RECOVERED_FRACTION


def test_ship_index_is_argmin_with_earliest_tie():
    assert RS.ship_index([0.3, 0.1, 0.2, 0.4]) == 1
    assert RS.ship_index([0.2, 0.1, 0.1, 0.4]) == 1
    assert RS.ship_index([0.5, 0.5, 0.5, 0.5]) == 0


def _prim(mean_p2, p_pos, frac):
    return {"pooled": {"P2_improvement_f2final_minus_f2ship": {"mean_d": mean_p2, "p_pos": p_pos},
                       "recovered_fraction": frac,
                       "P1_f0best_minus_f2ship": {"mean_d": -0.005, "p_neg": 0.99},
                       "P3_fair_f0ship_minus_f2ship": {"mean_d": 0.0, "p_neg": 0.5, "p_pos": 0.5}}}


def test_routing_rows_are_all_reachable_and_controls_are_consumed():
    ok = [{"control": "c", "pass": True}]
    bad = [{"control": "c", "pass": False}]
    assert RS.evaluate_gates(bad, _prim(0.01, 0.001, 0.9))["terminal"] == "CANNOT_CHECK__CONTROL_FAILED"
    assert RS.evaluate_gates(ok, _prim(0.01, 0.001, 0.9))["terminal"].startswith("SHIPPING_OPERATOR_RECOVERS_HALF")
    assert RS.evaluate_gates(ok, _prim(0.004, 0.01, 0.3))["terminal"].startswith("SHIPPING_OPERATOR_HELPS_BUT")
    assert RS.evaluate_gates(ok, _prim(0.001, 0.4, 0.1))["terminal"].startswith("SHIPPING_LEVER_EXHAUSTED")


def test_rs2_cannot_fire_without_rs1():
    ok = [{"control": "c", "pass": True}]
    g = RS.evaluate_gates(ok, _prim(-0.001, 0.9, 0.9))
    assert g["RS1_SHIPPING_LEVER_HELPS"] is False and g["RS2_RECOVERS_HALF_OR_MORE"] is False


def test_selftest_passes():
    assert RS.selftest() == 0


@pytest.mark.skipif(not RS.ROLLUP.exists(), reason="rollup not computed yet")
def test_committed_rollup_matches_its_design_and_inputs():
    roll = json.loads(RS.ROLLUP.read_text())
    assert roll["design_json_sha256"] == RS.sha256_file(RS.DESIGN_JSON)
    assert roll["tuples_sha256"] == RS.sha256_file(RS.IB.TUPLES)
    assert roll["n_pairs"] == 24
    assert all(c["pass"] for c in roll["controls"]) == roll["gates"]["RS0_CONTROLS_VALID"]
