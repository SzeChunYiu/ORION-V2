"""E40-m5' Stage-2c: single-delta prompts, served-model pin, in-campaign F0, analysis controls."""
from __future__ import annotations

import importlib.util
import inspect
import json
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


s2c = _load("e40_s2c_runner", "scripts/e40_matched_runner_m5p_stage2c.py")
m3 = _load("e40_m3_runner_for_2c", "scripts/e40_matched_runner_m3.py")
an = _load("e40_s2c_analysis", "research/experiments/e40-matched/e40_m5p_stage2c_analysis.py")

M3_RULE = ("\nCYCLE-1 RULE (binding): cycle 1 has no feedback yet, so spend it on\n"
           "coverage rather than refinement — training_regime MUST be an axis\n"
           "extreme: \"observational\" or \"interventional\" (NOT \"partial_interventional\").\n"
           "Interior partial-intervention fractions are reserved for cycles 2+,\n"
           "once feedback exists.\n")

OK_CFG = {"training_regime": "interventional", "fraction_partial_intervention": 0.0,
          "partial_intervention_seed": 13, "model_seed": 11, "omission_estimation_size": 1000}
HIST = [{"cycle": 1, "config": OK_CFG,
         "feedback": {"pooled_biological_evaluation": {"true_positives": 240.0},
                      "pooled_biological_sigificant_evaluation": {"true_positives": 108},
                      "run_time": 149.5}}]


@pytest.mark.parametrize("cycle", [2, 3, 4])
def test_cycles_2_to_4_prompt_byte_identical_to_m2_f2(cycle: int) -> None:
    hist = HIST + [dict(HIST[0], cycle=c) for c in range(2, cycle)]
    for ds in s2c.DATASETS:
        m3_prompt = m3.f2_prompt(ds, 4, cycle, hist)
        assert M3_RULE not in m3_prompt
        for replica in s2c.REPLICAS:
            assert s2c.f2_prompt(ds, 4, cycle, hist, replica) == m3_prompt


def test_cycle1_prompt_is_m2_base_plus_seed_rule_only() -> None:
    for ds in s2c.DATASETS:
        for rep in range(s2c.REPS):
            m3_p1 = m3.f2_prompt(ds, rep, 1, [])
            m2_base = m3_p1.replace(M3_RULE, "")
            for replica in s2c.REPLICAS:
                p1 = s2c.f2_prompt(ds, rep, 1, [], replica)
                rule = s2c.cycle1_rule(replica)
                assert p1 == m3_p1.replace(M3_RULE, rule) and p1.replace(rule, "") == m2_base
                assert replica not in p1


def test_f0_prompt_byte_identical_to_m2_m3() -> None:
    for ds in s2c.DATASETS:
        for rep in range(s2c.REPS):
            assert s2c.f0_prompt(ds, rep) == m3.f0_prompt(ds, rep)


def test_shared_mechanics_verbatim_from_m3() -> None:
    assert inspect.getsource(s2c.substrate_header) == inspect.getsource(m3.substrate_header)
    assert inspect.getsource(s2c.validate_config) == inspect.getsource(m3.validate_config)
    assert s2c.PINNED == m3.PINNED and s2c.KNOB_DOMAINS == m3.KNOB_DOMAINS
    assert s2c.FORBIDDEN_SUBSTRINGS == m3.FORBIDDEN_SUBSTRINGS == an.FORBIDDEN_SUBSTRINGS
    assert s2c.SEED_TABLE == an.SEED_TABLE
    assert s2c.SERVED_MODEL == an.SERVED_MODEL == "glm-5.3"


def test_served_model_pin_fails_closed() -> None:
    s2c.assert_served_model(s2c.SERVED_MODEL)  # frozen id passes
    for other in ("glm-5.2", "glm-5.3-flash", "GLM-5.3", ""):
        with pytest.raises(s2c.ChainCannotCheck) as exc:
            s2c.assert_served_model(other)
        assert "!= frozen SERVED_MODEL" in str(exc.value)


def test_analysis_served_model_custody() -> None:
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "00_f2r0_weissmann_k562_0"
        (d / "cycle1").mkdir(parents=True)
        assert "no served-model record" in (an.served_model_violation(d) or "")
        (d / "cycle1" / "decision.json").write_text(json.dumps(
            {"call_log": [{"attempt": 0, "model_id": an.SERVED_MODEL}]}))
        assert an.served_model_violation(d) is None
        (d / "cycle2").mkdir()
        (d / "cycle2" / "decision.json").write_text(json.dumps(
            {"call_log": [{"attempt": 0, "model_id": "glm-5.2"}]}))
        assert "glm-5.2" in (an.served_model_violation(d) or "")


def test_task_numbering_covers_48_replica_and_12_f0_chains() -> None:
    seen, ids = set(), []
    for task in range(s2c.N_TASKS_ALL):
        ds, rep, replica = s2c.task_split(task)
        seen.add((ds, rep, replica))
        ids += [s2c.exp_id_for(task, i) for i in range(1, s2c.K_CYCLES + 1)]
        assert s2c.chain_dir_for(task).name == f"{task:02d}_{replica}_{ds}_{rep}"
    assert s2c.N_TASKS_ALL == 60 and len(seen) == 60
    assert sum(1 for _, _, r in seen if r == "f0") == 12
    assert sorted(ids) == list(range(504000, 504240))
    with pytest.raises(ValueError):
        s2c.task_split(60)


def test_seed_mandate_reask_then_cannot_check() -> None:
    wrong = dict(OK_CFG, model_seed=0)
    seq = iter([dict(wrong), dict(OK_CFG, partial_intervention_seed=0), dict(OK_CFG)])
    cfg, dec, prompt = s2c.ask_config_f2("weissmann_k562", 0, 1, [], "f2r0",
                                         _ask=lambda p: (next(seq), {"calls": []}))
    assert cfg == OK_CFG and dec["calls"][-1]["violations"] == 2
    assert prompt.count("VIOLATION of the CYCLE-1 RULE") == 2
    with pytest.raises(s2c.ChainCannotCheck):
        s2c.ask_config_f2("weissmann_k562", 0, 1, [], "f2r1", _ask=lambda p: (dict(OK_CFG), {"calls": []}))


def test_leakage_asserts_executed() -> None:
    with tempfile.TemporaryDirectory() as td:
        fb = Path(td) / "redacted_feedback.json"
        fb.write_text(json.dumps({"x": {"false_omission_rate": 0.1}}))
        with pytest.raises(s2c.ChainCannotCheck):
            s2c.read_feedback(fb)
    with pytest.raises(s2c.ChainCannotCheck):
        s2c.ask_config("quantitative_test_evaluation", rep=0)


def test_runner_selftest_passes() -> None:
    assert s2c.selftest() == 0


def test_analysis_controls_and_conventions() -> None:
    assert an.control_jaccard_selftest()["verdict"] == "PASS"
    with tempfile.TemporaryDirectory() as td:
        assert an.control_edge_roundtrip(Path(td))["verdict"] == "PASS"
    assert an.perm_paired_p([1.0] * 12) == 1 / 4096
    assert an.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == -1.0


def test_analysis_selftest_end_to_end_through_main() -> None:
    # planted/null fixtures, refusal (F2 and in-campaign F0), CANNOT_CHECK exclusion,
    # leak abort, seed drift, served-model substitution, missing served-model record,
    # historical non-gating panel.
    assert an.selftest(fast=True) == 0


def test_analysis_refuses_on_empty_campaign() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        an.write_fixture(root / "m2", root / "unused", mode="planted")
        saved = an._with_roots(root / "m2", root / "empty", root / "out")
        try:
            assert an.main(["run"]) == 3
        finally:
            an._restore_roots(saved)
        status = json.loads((root / "out/E40_M5P_STAGE2C_STATUS.json").read_text())
        assert status["status"] == "REFUSED__CAMPAIGN_NOT_SETTLED"
        assert status["campaign"]["chains_by_status"] == {"MISSING": 60}


# --------------------------------------------------------------------------
# REPAIR R1 (E40 closure lane): the Stage-2c checker must CONSUME its registered
# control verdicts. The frozen script reported them and routed anyway, emitting
# E40_TERMINAL while the planted positive control was FAILing
# (E40_M5P_STAGE2C_OUTCOME_RECEIPT.md §5). These tests pin the repair against the
# REAL archived campaign artifacts, and assert the no-alarm case too: a checker
# that fires on a clean run is as broken as one that never fires.
# --------------------------------------------------------------------------
ARCHIVE = REPO / "research/experiments/e40-matched/rollup-m5p-stage2c"


def _real_inputs():
    rollup = json.loads((ARCHIVE / "E40_M5P_STAGE2C_ROLLUP_V1.json").read_text())
    return (rollup,
            rollup["analysis"]["contrasts_primary_12cell"],
            rollup["analysis"]["rho"],
            rollup["analysis"]["strata"],
            json.loads((ARCHIVE / "planted.json").read_text()),
            json.loads((ARCHIVE / "nullcal.json").read_text()))


def test_archived_stage2c_artifacts_are_present_and_planted_really_failed():
    """Guards the tests below from becoming vacuous if the archive moves."""
    assert (ARCHIVE / "E40_M5P_STAGE2C_ROLLUP_V1.json").exists()
    _, _, _, _, planted, nullcal = _real_inputs()
    assert planted["verdict"] == "FAIL"
    assert nullcal["verdict"] == "PASS"


def test_failed_planted_control_voids_the_real_stage2c_verdict():
    rollup, ct, rho, strata, planted, nullcal = _real_inputs()
    assert rollup["analysis"]["gates"]["disposition"] == "E40_TERMINAL"  # the frozen defect
    g = an.evaluate_gates(ct, rho, strata, {"planted": planted, "nullcal": nullcal})
    assert g["disposition"] == "CHECKER_INVALID__NO_VERDICT"
    assert g["gates_admissible"] is False
    assert g["controls_gate"]["status"] == "CONTROL_FAILED"


def test_repair_does_not_alter_any_computed_gate_value():
    rollup, ct, rho, strata, planted, nullcal = _real_inputs()
    g = an.evaluate_gates(ct, rho, strata, {"planted": planted, "nullcal": nullcal})
    for k in ("G0_DRAG_PRESENT_UNDER_TERMINAL", "G1_CONSENSUS_RANKS_TRUTH",
              "G2_CONSENSUS_SHIPPING_CLOSES_DRAG", "G3_ANTI_CONTROL_DISTINGUISHES",
              "G4_SPLIT_CONSISTENT"):
        assert g[k] == rollup["analysis"]["gates"][k]


def test_no_alarm_passing_controls_leave_the_registered_routing_intact():
    _, ct, rho, strata, planted, nullcal = _real_inputs()
    g = an.evaluate_gates(ct, rho, strata,
                          {"planted": {**planted, "verdict": "PASS"}, "nullcal": nullcal})
    assert g["disposition"] == "E40_TERMINAL"
    assert g["gates_admissible"] is True


def test_absent_control_is_could_not_check_and_never_reads_as_clean():
    _, ct, rho, strata, _, nullcal = _real_inputs()
    for controls in ({"planted": None, "nullcal": nullcal}, {"nullcal": nullcal}, None):
        g = an.evaluate_gates(ct, rho, strata, controls)
        assert g["disposition"] == "CONTROLS_UNAVAILABLE__NO_VERDICT"
        assert g["gates_admissible"] is False
        assert g["controls_gate"]["status"] == "CONTROLS_UNAVAILABLE"


def test_either_registered_control_failing_voids_the_verdict():
    _, ct, rho, strata, planted, nullcal = _real_inputs()
    ok = {"planted": {**planted, "verdict": "PASS"}, "nullcal": nullcal}
    for name in an.REGISTERED_CONTROLS:
        broken = {**ok, name: {**ok[name], "verdict": "FAIL"}}
        assert an.evaluate_gates(ct, rho, strata, broken)["disposition"] \
            == "CHECKER_INVALID__NO_VERDICT"


def test_synthetic_bypass_is_named_not_silent():
    """The null-calibration harness has no real controls by construction; its bypass
    must be an explicit named sentinel, never `None` falling through as a pass."""
    _, ct, rho, strata, _, _ = _real_inputs()
    g = an.evaluate_gates(ct, rho, strata, an.SYNTHETIC_CONTROLS_OK)
    assert g["controls_gate"]["status"] == "SYNTHETIC_BYPASS"
    assert g["gates_admissible"] is True
    assert an.evaluate_gates(ct, rho, strata, None)["gates_admissible"] is False
