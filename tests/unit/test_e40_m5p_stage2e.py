"""E40-m5' Stage-2e: the replica-overlap precondition probe.

The load-bearing test here is byte-identity of the edge/Jaccard primitives with the
Stage-2c analysis. Stage-2e is a precondition for Stage-2c's statistic, so "same
statistic" must be verified character-for-character, not asserted in prose.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


s2e = _load("e40_s2e", "research/experiments/e40-matched/e40_m5p_stage2e_overlap_precondition.py")
s2c = _load("e40_s2c_for_2e", "research/experiments/e40-matched/e40_m5p_stage2c_analysis.py")

ALL_PASS = {k: {"verdict": "PASS"} for k in
            ("jaccard", "edge_roundtrip", "nullcal", "determinism")}
CLEAN_STATS = {"envelopes_ok": True, "seed_only_mean_J": 0.6,
               "perm": {"status": "OK", "t_obs": 0.4, "p_one_sided": 0.001}}


def test_edge_and_jaccard_primitives_are_byte_identical_to_stage2c():
    for fn in ("parse_edges", "write_edges", "jaccard", "consensus_j"):
        assert inspect.getsource(getattr(s2e, fn)) == inspect.getsource(getattr(s2c, fn)), fn


def test_control_that_must_match_the_primitives_actually_discriminates():
    """A control that cannot fail proves nothing: check the comparison has teeth."""
    assert inspect.getsource(s2e.parse_edges) != inspect.getsource(s2c.jaccard)


def test_grid_is_the_frozen_34_run_shape_with_unique_ids():
    sl = s2e.slots()
    assert len(sl) == 34
    assert len({s["exp_id"] for s in sl}) == 34
    assert len({s["key"] for s in sl}) == 34
    assert min(s["exp_id"] for s in sl) == 505000
    assert max(s["exp_id"] for s in sl) == 505033
    assert sum(1 for s in sl if s["repeat"] == 1) == 2


def test_seed_table_is_inherited_verbatim_from_stage2c():
    """The Stage-2c replica seed table, read out of the Stage-2c runner itself."""
    runner = _load("e40_s2c_runner_for_2e", "scripts/e40_matched_runner_m5p_stage2c.py")
    src = inspect.getsource(runner)
    for _name, ms, ps in s2e.SEEDS:
        assert f"{ms}" in src and f"{ps}" in src
    assert [(m, p) for _n, m, p in s2e.SEEDS] == [(11, 13), (29, 31), (47, 53), (71, 79)]


def test_zero_model_calls_by_construction():
    src = inspect.getsource(s2e)
    for forbidden in ("anthropic_call", "urlopen", "requests.", "ANTHROPIC", "api_key"):
        assert forbidden not in src, f"a model-channel symbol leaked in: {forbidden}"


def test_failed_or_absent_control_voids_an_otherwise_perfect_result():
    for name in ("jaccard", "edge_roundtrip", "nullcal", "determinism"):
        broken = {**ALL_PASS, name: {"verdict": "FAIL"}}
        assert s2e.evaluate_gates(CLEAN_STATS, broken)["disposition"] == "CANNOT_CHECK"
        absent = {k: v for k, v in ALL_PASS.items() if k != name}
        g = s2e.evaluate_gates(CLEAN_STATS, absent)
        assert g["disposition"] == "CANNOT_CHECK"
        assert g["controls_gate"]["status"] == "CONTROLS_UNAVAILABLE"
    assert s2e.evaluate_gates(CLEAN_STATS, None)["disposition"] == "CANNOT_CHECK"


def test_no_alarm_clean_run_routes_precondition_met():
    g = s2e.evaluate_gates(CLEAN_STATS, ALL_PASS)
    assert g["disposition"] == "PROBE_PRECONDITION_MET"
    assert g["gates_admissible"] is True


def test_both_p1_boundaries_are_live_and_route_to_distinct_terminals():
    cases = {0.0: "E40_PROBE_PRECONDITION_UNMET__REPLICAS_DISJOINT",
             0.199: "E40_PROBE_PRECONDITION_UNMET__REPLICAS_DISJOINT",
             0.20: "PROBE_PRECONDITION_MET",
             0.98: "PROBE_PRECONDITION_MET",
             0.981: "E40_PROBE_PRECONDITION_UNMET__REPLICATION_DEGENERATE",
             1.0: "E40_PROBE_PRECONDITION_UNMET__REPLICATION_DEGENERATE"}
    for j, expect in cases.items():
        got = s2e.evaluate_gates({**CLEAN_STATS, "seed_only_mean_J": j}, ALL_PASS)
        assert got["disposition"] == expect, (j, got["disposition"])


def test_precondition_terminal_is_never_the_registered_e40_terminal():
    """Closing the line on non-testability must not be dressed as the registered
    E40_TERMINAL, which requires a valid G0-pass / G1-G4-fail probe run."""
    for j in (0.0, 1.0):
        g = s2e.evaluate_gates({**CLEAN_STATS, "seed_only_mean_J": j}, ALL_PASS)
        assert g["disposition"] != "E40_TERMINAL"
        assert "NOT the registered E40_TERMINAL" in g["preregistered_route"]


def test_non_discriminating_statistic_is_reported_as_ambiguous_in_those_words():
    g = s2e.evaluate_gates({**CLEAN_STATS, "perm": {"status": "OK", "t_obs": -0.1,
                                                    "p_one_sided": 0.9}}, ALL_PASS)
    assert g["disposition"] == "AMBIGUOUS__PRECONDITION_MET_STATISTIC_NON_DISCRIMINATING"
    assert "ambiguous" in g["preregistered_route"]


def test_permutation_is_exhaustive_and_deterministic():
    so = {"weissmann_k562": [0.9, 0.8, 0.85, 0.88], "weissmann_rpe1": [0.7, 0.75, 0.72, 0.71]}
    co = {"weissmann_k562": [0.1, 0.2, 0.15, 0.12], "weissmann_rpe1": [0.3, 0.25, 0.22, 0.21]}
    a, b = s2e.strat_perm_p(so, co), s2e.strat_perm_p(so, co)
    assert a == b
    assert a["exhaustive"] is True and a["draws"] == 4900
    assert a["p_one_sided"] == 1 / 4900


def test_permutation_null_is_calibrated_on_the_registered_settings():
    r = s2e.control_permutation_null()
    assert r["reps"] == 400
    assert 0.02 <= r["rejection_rate"] <= 0.09
    assert r["verdict"] == "PASS"


def test_inhomogeneous_envelope_is_detected_field_by_field():
    s = s2e.slots()[5]
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        g = s2e.__dict__
        saved = g["RESULTS"]
        g["RESULTS"] = root
        try:
            d = root / str(s["exp_id"])
            d.mkdir(parents=True)
            (d / "metrics.json").write_text("{}")
            (d / "output_network.csv").write_text(",0,1\n0,A,B\n")
            (d / "arguments.json").write_text(json.dumps({**s["cfg"], "model_seed": 999}))
            st = s2e.envelope_status(s)
            assert st["status"] == "INHOMOGENEOUS"
            assert "model_seed" in st["detail"]
            (d / "arguments.json").write_text(json.dumps(s["cfg"]))
            assert s2e.envelope_status(s)["status"] == "COMPLETE"   # no-alarm twin
        finally:
            g["RESULTS"] = saved


def test_design_json_matches_the_code_constants():
    d = json.loads((REPO / "research/experiments/e40-matched"
                    / "E40_M5P_STAGE2E_OVERLAP_PRECONDITION_DESIGN_V1.json").read_text())
    assert d["exp_ids"] == [505000, 505033]
    assert d["n_native_runs"] == len(s2e.slots()) == 34
    assert d["n_model_calls"] == 0
    assert d["gates"]["P1_SEED_REPLICATION_INFORMATIVE"]["seed_only_mean_J_in"] == \
        [s2e.P1_J_FLOOR, s2e.P1_J_CEILING]
    assert d["gates"]["P2_CONSENSUS_DISCRIMINATES"]["alpha"] == s2e.P2_ALPHA
    assert {k: list(v) for k, v in d["seed_table_inherited_from_stage2c"].items()} == \
        {n: [m, p] for n, m, p in s2e.SEEDS}
