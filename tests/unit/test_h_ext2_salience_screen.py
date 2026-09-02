"""H-EXT-2 screen: end-to-end `main()` on a synthetic two-cohort campaign tree.

Fixture plants (a) sig_purity anti-ranking truth (higher purity <-> higher
wasserstein) and (b) a replica-consensus signal that ranks truth, so the frozen
gates must read G0 PASS, G1 PASS, G2 PASS on the positive tree; then exercises
the CANNOT_CHECK / fallback / pin-violation paths. Draw counts are reduced via
the test-only env overrides; the frozen defaults are asserted separately.
"""
from __future__ import annotations

import importlib.util
import json
import os
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCREEN = ROOT / "research" / "experiments" / "h-ext2" / "h_ext2_salience_screen.py"
DATASETS = ["weissmann_k562", "weissmann_rpe1"]


def _load(name: str, env: dict[str, str]):
    saved = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    try:
        spec = importlib.util.spec_from_file_location(name, SCREEN)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return mod


def _edges(prefix: str, n: int) -> set[tuple[str, str]]:
    return {(f"{prefix}s{i}", f"{prefix}t{i}") for i in range(n)}


def _write_run(results: Path, exp_id: int, *, truth: float, purity_num: float, edges: set, model: str,
               regime: str, seed: int) -> None:
    d = results / str(exp_id)
    d.mkdir(parents=True)
    metrics = {
        "corum_evaluation": {"true_positives": 30.0 + seed}, "ligand_receptor_evaluation": {"true_positives": 2.0},
        "quantitative_test_evaluation": {"output_graph": {"wasserstein_distance": {"mean": truth},
                                                          "true_positives": 100, "false_positives": 300},
                                         "false_omission_rate": 0.1, "negative_mean_wasserstein": 0.2},
        "string_network_evaluation": {"true_positives": 40.0}, "string_physical_evaluation": {"true_positives": 12.0},
        "chipseq_evaluation": {"true_positives": 5}, "pooled_biological_evaluation": {"true_positives": 100.0},
        "pooled_biological_sigificant_evaluation": {"true_positives": purity_num}, "run_time": 100.0 + seed,
    }
    (d / "metrics.json").write_text(json.dumps(metrics))
    (d / "arguments.json").write_text(json.dumps({"model_name": model, "dataset_name": "x", "model_seed": seed,
                                                  "training_regime": regime, "partial_intervention_seed": 0,
                                                  "fraction_partial_intervention": 0.0, "exp_id": str(exp_id)}))
    rows = [",0,1"] + [f"{i},{s},{t}" for i, (s, t) in enumerate(sorted(edges))]
    (d / "output_network.csv").write_text("\n".join(rows) + "\n")


def _cohort(root: Path, *, exp_base: int, replicas: bool, model: str = "DCDFG-LIN", rng: random.Random,
            pin_break: bool = False, constant_purity_chains: int = 0) -> None:
    chains = root / "run/chains"
    results = root / "run/results"
    task = 0
    for ds in DATASETS:
        for rep in range(6):
            cdir = chains / f"{task:02d}_f2_{ds}_{rep}"
            cdir.mkdir(parents=True)
            (cdir / "CHAIN_COMPLETE.json").write_text("{}")
            truths = [0.10 + 0.02 * c + rng.uniform(-0.004, 0.004) for c in range(4)]
            rng.shuffle(truths)
            for c in range(4):
                cyc = cdir / f"cycle{c + 1}"
                cyc.mkdir()
                exp = exp_base + task * 4 + c
                # planted: purity rises with wasserstein (anti-ranking); replica agreement falls with it
                purity_num = 20.0 if (task < constant_purity_chains) else 100.0 * truths[c] * 3 + rng.uniform(0, 0.5)
                k = max(1, min(9, int(round(10 - 40 * (truths[c] - 0.10)))))  # shared edges with the replica
                orig = _edges("a", 10)
                repl = set(sorted(orig)[:k]) | _edges("b", 10 - k)
                bad = pin_break and task == 3 and c == 2
                _write_run(results, exp, truth=truths[c], purity_num=purity_num, edges=orig,
                           model=("gies" if bad else model), regime="Observational", seed=c)
                fb = {k2: v for k2, v in json.loads((results / str(exp) / "metrics.json").read_text()).items()
                      if k2 != "quantitative_test_evaluation"}
                (cyc / "redacted_feedback.json").write_text(json.dumps(fb, sort_keys=True))
                (cyc / "exp_id").write_text(str(exp))
                if replicas:
                    rid = exp_base + 100 + task * 4 + c
                    _write_run(results, rid, truth=truths[c], purity_num=purity_num, edges=repl, model=model,
                               regime="Observational", seed=c + 7919)
                    (cyc / "replica_exp_id").write_text(str(rid))
            task += 1
    ctl = root / "run/controls"
    (ctl / "planted").mkdir(parents=True)
    (ctl / "planted/planted.json").write_text(json.dumps({"verdict": "PASS"}))
    (ctl / "nullcal.json").write_text(json.dumps({"verdict": "PASS"}))


def _env(tmp: Path, **over: str) -> dict[str, str]:
    env = {"HEXT2_RPRIME_ROOT": str(tmp / "rprime"), "HEXT2_PPRIME_ROOT": str(tmp / "pprime"),
           "HEXT2_OUT": str(tmp / "out"), "HEXT2_MODEL": "DCDFG-LIN"}
    env.update(over)
    return env


def _fast(monkeypatch) -> None:
    """Test-only draw budget (read by main() at call time); frozen defaults are asserted separately."""
    monkeypatch.setenv("HEXT2_NULLCAL_REPS", "120")
    monkeypatch.setenv("HEXT2_NULLCAL_DRAWS", "40")
    monkeypatch.setenv("HEXT2_DRAWS", "60")


def test_frozen_constants():
    mod = _load("hext2_screen_constants", {})
    assert (mod.SHUFFLE_SEED, mod.DRAWS, mod.P_GATE) == (20260903, 10000, 0.05)
    assert mod.DIRECTIONS["sig_purity"] == -1 and mod.PRIMARY == "sig_purity"
    assert {k: v for k, v in mod.DIRECTIONS.items() if k not in ("sig_purity", "replica_J", "within_J")} == {
        "pooled_tp": 1, "pooled_sig_tp": 1, "corum_tp": 1, "string_net_tp": 1, "string_phys_tp": 1,
        "chipseq_tp": 1, "ligand_tp": 1, "fast_runtime": -1, "zmean_tp": 1, "rankmean_tp": 1, "efficiency": 1}
    assert mod.selftest_edges()["verdict"] == "PASS"
    assert mod.route(False, True, "PASS").startswith("CANNOT_CHECK")
    assert mod.route(True, False, "PASS").startswith("SALIENCE_ANTI_RANKING_NOT_REPLICATED")
    assert mod.route(True, True, "PASS").startswith("SALIENCE_ANTI_RANKING_REPLICATED_CROSS_LEARNER")
    assert mod.route(True, True, "FAIL").startswith("ANTI_RANKING_NOT_CHANNEL_SPECIFIC")
    assert mod.route(True, True, "CANNOT_CHECK").startswith("G2_CANNOT_CHECK")


def test_positive_tree_replicates_and_is_specific(tmp_path: Path, monkeypatch):
    rng = random.Random(1)
    _cohort(tmp_path / "rprime", exp_base=505000, replicas=True, rng=rng)
    _cohort(tmp_path / "pprime", exp_base=505200, replicas=False, rng=rng)
    mod = _load("hext2_screen_pos", _env(tmp_path))
    _fast(monkeypatch)
    assert mod.main() == 0
    roll = json.loads((tmp_path / "out/H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.json").read_text())
    g = roll["gates"]
    assert g["G0_CAMPAIGN_VALID"] is True and g["G1_ANTI_RANKING_REPLICATES"] is True
    assert g["G2_MECHANISM_SPECIFIC"] == "PASS" and g["G2_source"] == "replica_J"
    assert g["preregistered_route"].startswith("SALIENCE_ANTI_RANKING_REPLICATED_CROSS_LEARNER")
    r = roll["table"]["R_prime"]["sig_purity"]
    assert r["raw_pooled_rho"] > 0.8 and r["directed_pooled_rho"] == -(-1) * r["raw_pooled_rho"]
    assert roll["table"]["R_prime"]["replica_J"]["raw_pooled_rho"] < 0  # consensus ranks truth, no anti-ranking
    assert roll["table"]["P_prime"]["replica_J"]["chains_used"] == 0  # P' carries no replicas
    assert roll["table"]["POOLED_24"]["sig_purity"]["chains_used"] == 24
    assert roll["screen_controls"]["nullcal_rho"]["verdict"] == "PASS"
    assert roll["manifest"]["n_files"] > 24 * 4 * 4
    md = (tmp_path / "out/H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.md").read_text()
    for coh in ("## R_prime", "## P_prime", "## POOLED_24"):
        assert coh in md
    assert md.count("| sig_purity |") == 3 and md.count("| replica_J |") == 3
    assert "wasserstein" not in json.dumps(roll["cohorts"])  # truth never surfaces in the cohort summary


def test_pin_violation_is_g0_fail_exit2(tmp_path: Path, monkeypatch):
    rng = random.Random(2)
    _cohort(tmp_path / "rprime", exp_base=505000, replicas=True, rng=rng, pin_break=True)
    _cohort(tmp_path / "pprime", exp_base=505200, replicas=False, rng=rng)
    mod = _load("hext2_screen_pin", _env(tmp_path))
    _fast(monkeypatch)
    assert mod.main() == 2
    roll = json.loads((tmp_path / "out/H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.json").read_text())
    assert roll["gates"]["G0_CAMPAIGN_VALID"] is False
    assert roll["gates"]["G0_detail"]["R_prime"]["pin_violations"]
    assert roll["gates"]["preregistered_route"].startswith("CANNOT_CHECK")


def test_no_replicas_falls_back_to_within_j(tmp_path: Path, monkeypatch):
    rng = random.Random(3)
    _cohort(tmp_path / "rprime", exp_base=505000, replicas=False, rng=rng)
    _cohort(tmp_path / "pprime", exp_base=505200, replicas=False, rng=rng)
    mod = _load("hext2_screen_fb", _env(tmp_path))
    _fast(monkeypatch)
    mod.main()
    roll = json.loads((tmp_path / "out/H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.json").read_text())
    assert roll["G2_detail"]["replica_J"]["verdict"] == "CANNOT_CHECK"
    assert roll["gates"]["G2_source"] == "within_J"
    # within_J is constant on this fixture (identical edge sets every cycle) -> also CANNOT_CHECK
    assert roll["gates"]["G2_MECHANISM_SPECIFIC"] == "CANNOT_CHECK"
    assert roll["gates"]["preregistered_route"].startswith("G2_CANNOT_CHECK")


def test_degenerate_purity_is_g0_fail(tmp_path: Path, monkeypatch):
    rng = random.Random(4)
    _cohort(tmp_path / "rprime", exp_base=505000, replicas=True, rng=rng, constant_purity_chains=6)
    _cohort(tmp_path / "pprime", exp_base=505200, replicas=False, rng=rng)
    mod = _load("hext2_screen_degen", _env(tmp_path))
    _fast(monkeypatch)
    assert mod.main() == 2
    roll = json.loads((tmp_path / "out/H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.json").read_text())
    assert roll["gates"]["G0_detail"]["R_prime"]["chains_purity_distinct3"] == 6


def test_parent_learner_is_refused(tmp_path: Path, monkeypatch):
    rng = random.Random(5)
    _cohort(tmp_path / "rprime", exp_base=505000, replicas=True, rng=rng, model="gies")
    _cohort(tmp_path / "pprime", exp_base=505200, replicas=False, rng=rng, model="gies")
    mod = _load("hext2_screen_gies", _env(tmp_path, HEXT2_MODEL="gies"))
    _fast(monkeypatch)
    assert mod.main() == 2
