"""E40 channel information bound: the checker must be able to see a signal and must not
invent one, and its constants must be the frozen ones."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
E40 = ROOT / "research/experiments/e40-matched"
if str(E40) not in sys.path:
    sys.path.insert(0, str(E40))

import e40_channel_information_bound as IB  # noqa: E402


def _synthetic(n_chains: int, informative: bool, seed: int = 7):
    """36-chain shaped fixture: truth per row; feedback either tracks truth or is noise."""
    rng = random.Random(seed)
    chains = {}
    for i in range(n_chains):
        camp = "campaign-e40-m2" if i < 24 else "campaign-e40-m3"
        arm = "f0" if i < 12 else "f2"
        rows = []
        for cyc in range(1, 5):
            truth = rng.uniform(0.12, 0.20)
            fb = {f: rng.uniform(0, 100) for f in IB.FEEDBACK_FIELDS}
            if informative:
                fb["corum_evaluation"] = 1000.0 * truth + rng.gauss(0, 1.0)
            rows.append({"campaign": camp, "chain": f"{i:02d}_{arm}_ds_{i % 6}", "arm": arm,
                         "dataset": "ds", "rep": i % 6, "cycle": cyc,
                         "regime": rng.choice(IB.REGIMES), "frac": rng.choice([0.0, 0.5, 0.8]),
                         "model_seed": 0, "pi_seed": 0, "feedback": fb,
                         "truth_wasserstein": truth, "truth_tp": 0, "truth_fp": 0, "exp_id": "0"})
        chains[(camp, rows[0]["chain"])] = rows
    return chains


def test_spearman_and_ranks_known_values():
    assert IB.spearman([1, 2, 3, 4], [1, 2, 3, 4]) == pytest.approx(1.0)
    assert IB.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)
    assert IB.spearman([1, 1, 1, 1], [1, 2, 3, 4]) is None      # constant -> undefined, not 0
    assert IB._ranks([10.0, 20.0, 20.0, 5.0]) == [2.0, 3.5, 3.5, 1.0]


def test_ridge_recovers_a_linear_target():
    x = [[float(i), float(i * i % 7)] for i in range(40)]
    y = [3.0 * a - 2.0 * b + 1.0 for a, b in x]
    w, ym, mu, sd = IB._ridge_fit(x, y, 1e-6)
    pred = IB._ridge_predict(w, ym, mu, sd, x)
    assert max(abs(p - t) for p, t in zip(pred, y)) < 1e-3


def test_ranker_sees_a_planted_signal_and_not_noise():
    inf = IB.pooled(IB.loco_rho(_synthetic(36, True), "FB8"))
    noise = IB.pooled(IB.loco_rho(_synthetic(36, False), "FB8"))
    assert inf["mean_rho"] > 0.8
    assert inf["top1_hit_rate"] > 0.8
    assert abs(noise["mean_rho"]) < 0.3
    p_inf, _ = IB.perm_p(_synthetic(36, True), "FB8", inf["mean_rho"], 60, 1)
    p_noise, _ = IB.perm_p(_synthetic(36, False), "FB8", noise["mean_rho"], 60, 1)
    assert p_inf <= 0.05
    assert p_noise > 0.05


def test_gates_consume_controls_and_refuse_on_a_failed_control():
    ib = {"FB8": {"mean_rho": 0.9, "perm_p": 0.001}, "CFG": {"mean_rho": 0.9, "perm_p": 0.001},
          "FB8+CFG_minus_CFG": {"mean_diff": 0.5, "signflip_p": 0.001}}
    good = [{"control": "A", "pass": True}]
    bad = [{"control": "A", "pass": True}, {"control": "B", "pass": False}]
    assert IB.evaluate_gates(good, ib)["terminal"] == "OOS_RANKER_EXISTS__PROSPECTIVE_M5PP_WARRANTED"
    g = IB.evaluate_gates(bad, ib)
    assert g["terminal"] == "CANNOT_CHECK__CONTROL_FAILED" and g["failed_controls"] == ["B"]
    assert g["IB1"] is None


def test_routing_covers_every_row():
    def ib(fb, cfg):
        return {"FB8": {"mean_rho": fb[0], "perm_p": fb[1]}, "CFG": {"mean_rho": cfg[0], "perm_p": cfg[1]},
                "FB8+CFG_minus_CFG": {"mean_diff": 0.0, "signflip_p": 1.0}}
    ok = [{"control": "A", "pass": True}]
    assert IB.evaluate_gates(ok, ib((0.5, 0.01), (0.5, 0.01)))["terminal"].startswith("OOS_RANKER_EXISTS")
    assert IB.evaluate_gates(ok, ib((0.0, 0.5), (0.5, 0.01)))["terminal"].endswith("PRIOR_OVER_CONFIGS_IS_THE_ONLY_OOS_SIGNAL")
    assert IB.evaluate_gates(ok, ib((0.0, 0.5), (0.0, 0.5)))["terminal"].endswith("NO_OOS_SIGNAL_IN_FEEDBACK_OR_CONFIG")
    # a positive rho with an insignificant p does NOT fire
    assert IB.evaluate_gates(ok, ib((0.3, 0.2), (0.0, 0.5)))["terminal"].endswith("NO_OOS_SIGNAL_IN_FEEDBACK_OR_CONFIG")


def test_script_constants_equal_the_frozen_design():
    d = json.loads((E40 / "E40_CHANNEL_INFORMATION_BOUND_DESIGN_V1.json").read_text())
    assert d["ranker"]["lambda"] == IB.RIDGE_LAMBDA
    assert d["nulls"]["IB1_IB2"]["n_perm"] == IB.N_PERM
    assert d["nulls"]["IB1_IB2"]["seed"] == IB.PERM_SEED
    assert d["nulls"]["IB3"]["n"] == IB.SIGNFLIP_N
    assert d["inputs"]["tuples_sha256"] == IB.sha256_file(IB.TUPLES)
    assert d["inputs"]["rows"] == len(IB.load_rows())
    assert list(d["inputs"]["feedback_fields"]) == list(IB.FEEDBACK_FIELDS)


def test_frozen_tuples_reproduce_m4_and_m2_m3_numbers():
    chains = IB.chains_of(IB.load_rows())
    c1 = IB.control_m4_reproduced(chains)
    c2 = IB.control_m2_m3_reproduced(chains)
    assert c1["pass"], c1
    assert c2["pass"], c2


def test_load_rows_refuses_a_short_cohort(tmp_path):
    d = json.loads(IB.TUPLES.read_text())
    d["rows"] = d["rows"][:-1]
    p = tmp_path / "t.json"
    p.write_text(json.dumps(d))
    with pytest.raises(IB.CannotCheck):
        IB.load_rows(p)
