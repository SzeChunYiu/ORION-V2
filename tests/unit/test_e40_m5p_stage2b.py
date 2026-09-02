"""E40-m5' Stage-2b: runner single-delta + analysis controls (small, local)."""
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


s2b = _load("e40_s2b_runner", "scripts/e40_matched_runner_m5p_stage2b.py")
m3 = _load("e40_m3_runner", "scripts/e40_matched_runner_m3.py")
an = _load("e40_s2b_analysis", "research/experiments/e40-matched/e40_m5p_stage2b_analysis.py")

# The m3 cycle-1 rule, verbatim from scripts/e40_matched_runner_m3.py. m3 minus
# this string is the frozen m2 F2 cycle-1 prompt (m2 runner = m1 runner + gies pin).
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
                      "run_time": 149.5}},
        {"cycle": 2, "config": dict(OK_CFG, model_seed=3),
         "feedback": {"pooled_biological_evaluation": {"true_positives": 250.0},
                      "pooled_biological_sigificant_evaluation": {"true_positives": 110},
                      "run_time": 140.0}}]


@pytest.mark.parametrize("ds", s2b.DATASETS)
@pytest.mark.parametrize("cycle", [2, 3, 4])
def test_cycles_2_to_4_prompt_byte_identical_to_m2_f2(ds: str, cycle: int) -> None:
    hist = HIST[:cycle - 1] if cycle <= 3 else HIST + [dict(HIST[1], cycle=3)]
    m3_prompt = m3.f2_prompt(ds, 4, cycle, hist)
    assert M3_RULE not in m3_prompt  # m3 renders m2-identical prompts for cycles 2+
    for replica in s2b.REPLICAS:
        assert s2b.f2_prompt(ds, 4, cycle, hist, replica) == m3_prompt


def test_cycle1_prompt_is_m2_base_plus_seed_rule_only() -> None:
    for ds in s2b.DATASETS:
        for rep in range(s2b.REPS):
            m3_p1 = m3.f2_prompt(ds, rep, 1, [])
            assert m3_p1.count(M3_RULE) == 1
            m2_base = m3_p1.replace(M3_RULE, "")
            for replica in s2b.REPLICAS:
                p1 = s2b.f2_prompt(ds, rep, 1, [], replica)
                rule = s2b.cycle1_rule(replica)
                assert p1.count(rule) == 1
                assert p1.replace(rule, "") == m2_base
                assert p1 == m3_p1.replace(M3_RULE, rule)  # same insertion point as the m3 delta
                ms, ps = s2b.SEED_TABLE[replica]
                assert f"model_seed MUST be {ms}" in rule and f"partial_intervention_seed MUST be {ps}" in rule
                assert replica not in p1


def test_header_and_native_invocation_verbatim_from_m3() -> None:
    assert inspect.getsource(s2b.substrate_header) == inspect.getsource(m3.substrate_header)
    assert inspect.getsource(s2b.native_run) == inspect.getsource(m3.native_run).replace(
        '"""Run one pinned-native invocation; returns the run\'s metrics.json path."""',
        '"""Run one pinned-native invocation (m2/m3 verbatim); returns metrics.json path."""')
    assert inspect.getsource(s2b.validate_config) == inspect.getsource(m3.validate_config)
    assert s2b.PINNED == m3.PINNED == {"model_name": "gies", "subset_data": 0.05,
                                       "max_path_length": -1, "do_filter": True}
    assert s2b.KNOB_DOMAINS == m3.KNOB_DOMAINS
    assert s2b.FORBIDDEN_SUBSTRINGS == m3.FORBIDDEN_SUBSTRINGS == an.FORBIDDEN_SUBSTRINGS
    assert s2b.SEED_TABLE == an.SEED_TABLE == {"f2r0": (11, 13), "f2r1": (29, 31),
                                               "f2r2": (47, 53), "f2r3": (71, 79)}


def test_seed_mandate_reask_then_cannot_check() -> None:
    wrong = dict(OK_CFG, model_seed=0)
    seq = iter([dict(wrong), dict(OK_CFG, partial_intervention_seed=0), dict(OK_CFG)])
    cfg, dec, prompt = s2b.ask_config_f2("weissmann_k562", 0, 1, [], "f2r0",
                                         _ask=lambda p: (next(seq), {"calls": []}))
    assert cfg == OK_CFG
    assert dec["calls"][-1] == {"mandate": "cycle1_seeds", "replica": "f2r0",
                                "mandated": {"model_seed": 11, "partial_intervention_seed": 13},
                                "asked": 3, "violations": 2}
    assert prompt.count("VIOLATION of the CYCLE-1 RULE") == 2
    with pytest.raises(s2b.ChainCannotCheck):  # f2r0's seeds are a violation for f2r1: never repaired
        s2b.ask_config_f2("weissmann_k562", 0, 1, [], "f2r1", _ask=lambda p: (dict(OK_CFG), {"calls": []}))
    cfg2, dec2, p2 = s2b.ask_config_f2("weissmann_k562", 0, 2, HIST[:1], "f2r1",
                                       _ask=lambda p: (dict(wrong), {"calls": []}))
    assert cfg2 == wrong and dec2["calls"] == [] and "CYCLE-1 RULE" not in p2


def test_task_numbering_bijective_and_exp_ids_in_own_block() -> None:
    cells = set()
    ids = []
    for task in range(s2b.N_TASKS):
        ds, rep, replica = s2b.task_split(task)
        cells.add((ds, rep, replica))
        ids += [s2b.exp_id_for(task, c) for c in range(1, s2b.K_CYCLES + 1)]
        assert s2b.chain_dir_for(task).name == f"{task:02d}_{replica}_{ds}_{rep}"
    assert len(cells) == 48 and s2b.N_TASKS == 48
    assert sorted(ids) == list(range(503000, 503192))
    with pytest.raises(ValueError):
        s2b.task_split(48)


def test_leakage_asserts_executed_on_read_and_send() -> None:
    with tempfile.TemporaryDirectory() as td:
        fb = Path(td) / "redacted_feedback.json"
        fb.write_text(json.dumps({"x": {"false_omission_rate": 0.1}}))
        with pytest.raises(s2b.ChainCannotCheck):
            s2b.read_feedback(fb)
        fb.write_text(json.dumps({"pooled_biological_evaluation": {"true_positives": 1.0}}))
        assert s2b.read_feedback(fb) == {"pooled_biological_evaluation": {"true_positives": 1.0}}
    with pytest.raises(s2b.ChainCannotCheck):
        s2b.ask_config("quantitative_test_evaluation", rep=0)


def test_runner_selftest_passes() -> None:
    assert s2b.selftest() == 0


def test_jaccard_and_edge_roundtrip_controls() -> None:
    assert an.control_jaccard_selftest()["verdict"] == "PASS"
    with tempfile.TemporaryDirectory() as td:
        assert an.control_edge_roundtrip(Path(td))["verdict"] == "PASS"
    assert an.jaccard({(1, 2)}, {(1, 2)}) == 1.0
    assert an.jaccard({(1, 2), (2, 3)}, {(2, 3), (3, 4)}) == pytest.approx(1 / 3)
    assert an.consensus_j([{(1, 2)}, {(1, 2)}, {(9, 9)}]) == pytest.approx(1 / 3)


def test_perm_and_spearman_conventions_match_m_series() -> None:
    assert an.perm_paired_p([1.0] * 12) == 1 / 4096
    assert an.perm_paired_p([-1.0] * 12) == 1.0
    assert an.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == -1.0
    assert an.spearman([1, 2, 3, 4], [1, 1, 1, 1]) == 0.0
    assert an.sig_purity({"pooled_biological_sigificant_evaluation": {"true_positives": 108},
                          "pooled_biological_evaluation": {"true_positives": 240.0}}) == 108 / 240
    assert an.sig_purity({"pooled_biological_sigificant_evaluation": {"true_positives": 3},
                          "pooled_biological_evaluation": {"true_positives": 0.0}}) == 3.0


def test_analysis_selftest_end_to_end_through_main() -> None:
    # planted fixture -> all gates pass (m6 route); null fixture -> G1 fails (TERMINAL);
    # missing/in-progress chain -> refuse; CANNOT_CHECK chains excluded+counted; leak aborts.
    assert an.selftest(fast=True) == 0


def test_analysis_main_refuses_on_empty_campaign() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        an.write_fixture(root / "m2", root / "s2b_unused", mode="planted")
        saved = an._with_roots(root / "m2", root / "empty", root / "out")
        try:
            assert an.main(["run"]) == 3
        finally:
            an._restore_roots(saved)
        assert not (root / "out/E40_M5P_STAGE2B_ROLLUP_V1.json").exists()
        status = json.loads((root / "out/E40_M5P_STAGE2B_STATUS.json").read_text())
        assert status["status"] == "REFUSED__CAMPAIGN_NOT_SETTLED"
        assert status["campaign"]["chains_by_status"] == {"MISSING": 48}
