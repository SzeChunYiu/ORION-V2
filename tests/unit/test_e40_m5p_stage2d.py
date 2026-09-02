"""E40-m5' Stage-2d: arm prompts byte-equal to their frozen sources; control-gating refuses."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


s2d = _load("e40_s2d", "research/experiments/e40-matched/e40_m5p_stage2d_plant_discrimination.py")
m2 = _load("e40_m2_for_2d", "scripts/e40_matched_runner.py")          # m2 form (pin-only delta)
m3 = _load("e40_m3_for_2d", "scripts/e40_matched_runner_m3.py")       # regime anchor
s2c = _load("e40_s2c_for_2d", "scripts/e40_matched_runner_m5p_stage2c.py")  # seed mandate

HIST = [{"cycle": 1,
         "config": {"training_regime": "interventional", "fraction_partial_intervention": 0.0,
                    "partial_intervention_seed": 13, "model_seed": 11,
                    "omission_estimation_size": 1000},
         "feedback": {"pooled_biological_evaluation": {"true_positives": 24.0}, "run_time": 3536.4}}]


@pytest.mark.parametrize("cycle", list(range(1, 10)))
def test_arm_prompts_byte_equal_to_frozen_sources(cycle: int) -> None:
    """The ONLY inter-arm difference is the cycle-1 rule string (design §2)."""
    hist = [] if cycle == 1 else HIST
    ds, rep = s2d.PLANT_DATASET, s2d.PLANT_REP
    assert s2d.f2_prompt(ds, rep, cycle, hist, "A_NO_MANDATE") == m2.f2_prompt(ds, rep, cycle, hist)
    assert s2d.f2_prompt(ds, rep, cycle, hist, "B_REGIME_ANCHOR") == m3.f2_prompt(ds, rep, cycle, hist)
    assert s2d.f2_prompt(ds, rep, cycle, hist, "C_SEED_MANDATE") == s2c.f2_prompt(ds, rep, cycle, hist, "f2r0")


def test_arms_differ_only_by_the_cycle1_rule() -> None:
    ds, rep = s2d.PLANT_DATASET, s2d.PLANT_REP
    p = {a: s2d.f2_prompt(ds, rep, 1, [], a) for a in s2d.ARMS}
    assert p["A_NO_MANDATE"] == p["B_REGIME_ANCHOR"].replace(s2d.RULE_B, "")
    assert p["A_NO_MANDATE"] == p["C_SEED_MANDATE"].replace(s2d.RULE_C, "")
    # cycles 2+ are identical across all three arms
    for cycle in range(2, 10):
        rendered = {s2d.f2_prompt(ds, rep, cycle, HIST, a) for a in s2d.ARMS}
        assert len(rendered) == 1


def test_plant_and_pass_rule_inherited_verbatim() -> None:
    assert s2d.REGIME_FACTOR == {"partial_interventional": 1.0, "observational": 0.7,
                                 "interventional": 0.55}
    assert s2d.planted_quality({"training_regime": "partial_interventional",
                                "fraction_partial_intervention": 0.8}) == 1.0
    # known answer: m3's recorded planted trajectory replays exactly and PASSES
    ci = s2d.control_plant_integrity()
    assert ci["verdict"] == "PASS" and ci["max_abs_delta_vs_m3_recorded"] <= 1e-12
    # the Stage-2c-shaped trajectory (frac never off 0.5) FAILS the inherited rule
    q = [s2d.planted_quality({"training_regime": r, "fraction_partial_intervention": f})
         for r, f in s2d.FAIL_TRAJ]
    assert s2d.plant_verdict(q) == "FAIL"
    assert abs(q[-1] - 0.6411803884299545) <= 1e-12  # equals Stage-2c's observed terminal quality


def test_mandate_predicates() -> None:
    ok_c = {"model_seed": 11, "partial_intervention_seed": 13, "training_regime": "partial_interventional"}
    assert s2d.mandate_ok(ok_c, "C_SEED_MANDATE")
    assert not s2d.mandate_ok({**ok_c, "model_seed": 0}, "C_SEED_MANDATE")
    assert s2d.mandate_ok({"training_regime": "interventional"}, "B_REGIME_ANCHOR")
    assert not s2d.mandate_ok({"training_regime": "partial_interventional"}, "B_REGIME_ANCHOR")
    assert s2d.mandate_ok({"training_regime": "partial_interventional"}, "A_NO_MANDATE")


def test_served_model_pin_fails_closed() -> None:
    s2d.assert_served_model(s2d.SERVED_MODEL)
    for other in ("glm-5.2", "glm-5.3-flash", ""):
        with pytest.raises(s2d.ArmCannotCheck):
            s2d.assert_served_model(other)


def test_control_gating_refuses_every_gate(tmp_path: Path) -> None:
    """A failed registered control must refuse to file any D-gate (design §5)."""
    g = vars(s2d)
    saved = (s2d.ROOT, s2d.OUT_DIR)
    g["ROOT"], g["OUT_DIR"] = tmp_path / "run", tmp_path / "out"
    try:
        for arm in s2d.ARMS:
            s2d._fixture_arm(arm, s2d.FAIL_TRAJ,
                             served="glm-5.2" if arm == "C_SEED_MANDATE" else s2d.SERVED_MODEL)
        rc, doc = s2d.analyze(write=True)
    finally:
        g["ROOT"], g["OUT_DIR"] = saved
    gates = doc["gates"]
    assert gates["disposition"] == "CHECKER_INVALID__NO_VERDICT"
    assert gates["failed_controls"] == ["SERVED_MODEL_PIN"]
    for k in ("D0_ARMS_VALID", "D1_MODEL_CHANNEL_CAUSE", "D2_PROMPT_IMPLICATED",
              "D3_STAGE2C_FAILURE_NOT_REPRODUCED"):
        assert gates[k] == s2d.NOT_EVALUATED
    assert gates["ambiguous"] is True and rc == 3


def test_gate_patterns_are_exclusive_and_exhaustive(tmp_path: Path) -> None:
    g = vars(s2d)
    saved = (s2d.ROOT, s2d.OUT_DIR)
    outcomes = {}
    try:
        for name, traj in (("all_fail", {a: s2d.FAIL_TRAJ for a in s2d.ARMS}),
                           ("prompt", {"A_NO_MANDATE": s2d.PASS_TRAJ,
                                       "B_REGIME_ANCHOR": s2d.FAIL_TRAJ,
                                       "C_SEED_MANDATE": s2d.FAIL_TRAJ}),
                           ("not_repro", {a: s2d.PASS_TRAJ for a in s2d.ARMS})):
            g["ROOT"], g["OUT_DIR"] = tmp_path / name / "run", tmp_path / name / "out"
            for arm in s2d.ARMS:
                s2d._fixture_arm(arm, traj[arm])
            outcomes[name] = s2d.analyze(write=False)[1]["gates"]
    finally:
        g["ROOT"], g["OUT_DIR"] = saved
    assert outcomes["all_fail"]["disposition"] == "MODEL_CHANNEL_CAUSE"
    assert outcomes["all_fail"]["ambiguous"] is False
    assert outcomes["prompt"]["disposition"] == "PROMPT_IMPLICATED"
    assert outcomes["not_repro"]["disposition"] == "STAGE2C_FAILURE_NOT_REPRODUCED"
    assert outcomes["not_repro"]["ambiguous"] is True  # ambiguity reported, not resolved
    for o in outcomes.values():
        fired = [o[k] for k in ("D1_MODEL_CHANNEL_CAUSE", "D2_PROMPT_IMPLICATED",
                                "D3_STAGE2C_FAILURE_NOT_REPRODUCED")]
        assert sum(1 for f in fired if f is True) == 1


def test_selftest_passes() -> None:
    assert s2d.selftest() == 0


def test_no_native_run_path_exists() -> None:
    src = (REPO / "research/experiments/e40-matched/e40_m5p_stage2d_plant_discrimination.py").read_text()
    for forbidden in ("causalscbench", "subprocess", "output_network", "metrics.json"):
        assert forbidden not in src, f"diagnostic must not touch native runs ({forbidden})"
