"""H-EXT-2 runner: end-to-end `main()` on a synthetic tree (dry-run native driver).

Lesson from m5' Stage-1 (receipt §5): unit tests that never exercise `main()` miss
runtime defects. Every CLI command the design invokes is driven here through
`main()` with `sys.argv`, on a temporary campaign tree, with the model channel
stubbed at `anthropic_call`.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "h_ext2_salience_runner.py"
M2_RUNNER = ROOT / "scripts" / "e40_matched_runner.py"
M3_RUNNER = ROOT / "scripts" / "e40_matched_runner_m3.py"

TEMPLATE_METRICS = {
    "corum_evaluation": {"true_positives": 30.0}, "ligand_receptor_evaluation": {"true_positives": 2.0},
    "quantitative_test_evaluation": {"output_graph": {"wasserstein_distance": {"mean": 0.17},
                                                      "true_positives": 100, "false_positives": 300},
                                     "false_omission_rate": 0.1, "negative_mean_wasserstein": 0.2},
    "string_network_evaluation": {"true_positives": 40.0}, "string_physical_evaluation": {"true_positives": 12.0},
    "chipseq_evaluation": {"true_positives": 5}, "pooled_biological_evaluation": {"true_positives": 60.0},
    "pooled_biological_sigificant_evaluation": {"true_positives": 20}, "run_time": 100.0,
}


def _load(path: Path, name: str, env: dict[str, str]):
    saved = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    try:
        spec = importlib.util.spec_from_file_location(name, path)
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


def _tree(tmp_path: Path) -> Path:
    base = tmp_path / "base"
    tpl = base / "campaign-e40-r3/run/results/400000"
    tpl.mkdir(parents=True)
    (tpl / "metrics.json").write_text(json.dumps(TEMPLATE_METRICS))
    return base


def _stub_model(mod, regimes: list[str]):
    """Deterministic decision stub: cycles through the given regimes, varying model_seed."""
    calls = {"n": 0}

    def fake_call(prompt: str):
        i = calls["n"]
        calls["n"] += 1
        regime = regimes[i % len(regimes)]
        cfg = {"training_regime": regime,
               "fraction_partial_intervention": 0.5 if regime == "partial_interventional" else 0.0,
               "partial_intervention_seed": 3, "model_seed": 10 + i, "omission_estimation_size": 500}
        return json.dumps({"config": cfg, "rationale": "stub", "uncertainty": "stub"}), {"input_tokens": 1, "output_tokens": 1}

    mod.anthropic_call = fake_call
    return calls


def _env(base: Path, **over: str) -> dict[str, str]:
    env = {"E40M_BASE": str(base), "E40M_ROOT": str(base / "campaign-h-ext2-rprime"),
           "E40M_REF": str(base / "campaign-e40-m2"), "E40M_MODEL": "DCDFG-LIN",
           "E40M_CYCLE1_ANCHOR": "0", "E40M_EXP_BASE": "505000", "E40M_REPLICA_SEED_OFFSET": "7919",
           "ANTHROPIC_BASE_URL": "http://stub", "ANTHROPIC_MODEL": "stub", "ANTHROPIC_AUTH_TOKEN": "stub"}
    env.update(over)
    return env


def _run_main(mod, argv: list[str]) -> int:
    saved = sys.argv
    sys.argv = ["h_ext2_salience_runner.py", *argv]
    try:
        return mod.main()
    finally:
        sys.argv = saved


def test_rprime_chain_through_main_with_replicas(tmp_path: Path):
    base = _tree(tmp_path)
    mod = _load(RUNNER, "hext2_runner_rprime", _env(base))
    _stub_model(mod, ["partial_interventional", "interventional", "observational", "partial_interventional"])
    assert mod.PINNED["model_name"] == "DCDFG-LIN" and mod.CYCLE1_ANCHOR is False
    assert mod.EXP_BASE_M3 == 505000 and mod.REPLICA_SEED_OFFSET == 7919

    assert _run_main(mod, ["chain", "--task", "0", "--dry-run"]) == 0
    chain = base / "campaign-h-ext2-rprime/run/chains/00_f2_weissmann_k562_0"
    assert (chain / "CHAIN_COMPLETE.json").exists()
    for c in range(1, 5):
        cdir = chain / f"cycle{c}"
        exp = int((cdir / "exp_id").read_text())
        rep = int((cdir / "replica_exp_id").read_text())
        assert exp == 505000 + (c - 1) and rep == 505100 + (c - 1)
        fb = (cdir / "redacted_feedback.json").read_text()
        for s in mod.FORBIDDEN_SUBSTRINGS:
            assert s not in fb
        orig = json.loads((base / f"campaign-h-ext2-rprime/run/results/{exp}/arguments.json").read_text())
        repl = json.loads((base / f"campaign-h-ext2-rprime/run/results/{rep}/arguments.json").read_text())
        assert orig["model_name"] == repl["model_name"] == "DCDFG-LIN"
        assert repl["model_seed"] == (orig["model_seed"] + 7919) % 2147483648
        for k in ("training_regime", "fraction_partial_intervention", "partial_intervention_seed", "dataset_name"):
            assert orig[k] == repl[k]
        cfg = json.loads((cdir / "config_1.json").read_text())
        assert cfg["model_name"] == "DCDFG-LIN"
    # cycle-1 accepted an interior regime on the first ask: no mandate transcript, no rule text
    dec1 = json.loads((chain / "cycle1/decision.json").read_text())
    assert dec1["configs"][0]["training_regime"] == "partial_interventional"
    assert not any("mandate" in c for c in dec1["call_log"])
    prompt1 = (chain / "cycle1/prompt.txt").read_text()
    assert "CYCLE-1 RULE" not in prompt1
    # prompts byte-identical to the frozen m2 F2 arm (anchor off), every cycle
    m2 = _load(M2_RUNNER, "e40_m2_ref", _env(base))
    history = []
    for c in range(1, 5):
        dec = json.loads((chain / f"cycle{c}/decision.json").read_text())
        assert (chain / f"cycle{c}/prompt.txt").read_text() == m2.f2_prompt("weissmann_k562", 0, c, history)
        history.append({"cycle": c, "config": dec["configs"][0],
                        "feedback": json.loads((chain / f"cycle{c}/redacted_feedback.json").read_text())})
    # remaining CLI paths the design invokes
    assert _run_main(mod, ["audit"]) == 0
    assert _run_main(mod, ["control-nullcal"]) == 0
    assert json.loads((base / "campaign-h-ext2-rprime/run/controls/nullcal.json").read_text())["verdict"] == "PASS"
    assert _run_main(mod, ["rollup"]) == 2  # m3 drag rollup is not applicable to a fresh learner
    assert _run_main(mod, ["selftest"]) == 0
    # idempotent re-entry
    assert _run_main(mod, ["chain", "--task", "0", "--dry-run"]) == 0


def test_pprime_anchor_on_matches_m3_prompt_and_records_mandate(tmp_path: Path):
    base = _tree(tmp_path)
    env = _env(base, E40M_ROOT=str(base / "campaign-h-ext2-pprime"), E40M_CYCLE1_ANCHOR="1",
               E40M_EXP_BASE="505200", E40M_REPLICA_SEED_OFFSET="0")
    mod = _load(RUNNER, "hext2_runner_pprime", env)
    # first reply interior (violation), then extreme
    _stub_model(mod, ["partial_interventional", "interventional", "partial_interventional", "observational", "interventional"])
    assert mod.CYCLE1_ANCHOR is True and mod.REPLICA_SEED_OFFSET == 0
    assert _run_main(mod, ["chain", "--task", "7", "--dry-run"]) == 0
    chain = base / "campaign-h-ext2-pprime/run/chains/07_f2_weissmann_rpe1_1"
    assert (chain / "CHAIN_COMPLETE.json").exists()
    dec1 = json.loads((chain / "cycle1/decision.json").read_text())
    assert dec1["configs"][0]["training_regime"] == "interventional"
    mandate = [c for c in dec1["call_log"] if "mandate" in c]
    assert mandate and mandate[-1]["asked"] == 2 and mandate[-1]["violations"] == 1
    assert int((chain / "cycle1/exp_id").read_text()) == 505200 + 7 * 4
    assert not (chain / "cycle1/replica_exp_id").exists()
    m3 = _load(M3_RUNNER, "e40_m3_ref", _env(base))
    assert (chain / "cycle1/prompt.txt").read_text().startswith(m3.f2_prompt("weissmann_rpe1", 1, 1, []))
    assert "CYCLE-1 RULE" in (chain / "cycle1/prompt.txt").read_text()
    assert _run_main(mod, ["audit"]) == 0


def test_pinned_to_parent_learner_fails_selftest(tmp_path: Path):
    base = _tree(tmp_path)
    mod = _load(RUNNER, "hext2_runner_gies", _env(base, E40M_MODEL="gies"))
    assert _run_main(mod, ["selftest"]) == 1


def test_pin_drift_is_an_audit_violation(tmp_path: Path):
    base = _tree(tmp_path)
    mod = _load(RUNNER, "hext2_runner_drift", _env(base))
    _stub_model(mod, ["observational"])
    assert _run_main(mod, ["chain", "--task", "0", "--dry-run"]) == 0
    cfg = base / "campaign-h-ext2-rprime/run/chains/00_f2_weissmann_k562_0/cycle2/config_1.json"
    d = json.loads(cfg.read_text())
    d["model_name"] = "gies"
    cfg.write_text(json.dumps(d))
    assert _run_main(mod, ["audit"]) == 1


def test_validator_refuses_orchestrating_the_learner(tmp_path: Path):
    base = _tree(tmp_path)
    mod = _load(RUNNER, "hext2_runner_validate", _env(base))
    good = {"training_regime": "observational", "fraction_partial_intervention": 0.0,
            "partial_intervention_seed": 1, "model_seed": 2, "omission_estimation_size": 500}
    assert mod.validate_config(good, rep=0) == good
    with pytest.raises(ValueError):
        mod.validate_config(dict(good, model_name="gies"), rep=0)
