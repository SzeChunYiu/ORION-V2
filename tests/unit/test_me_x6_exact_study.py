"""ME-X6 — collective epistemics exact known-answer study: unit tests."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[2] / "research" / "experiments" / "me-x6"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mex6_model = _load("mex6_model")
mex6_generator = _load("mex6_generator")
mex6_oracle = _load("mex6_oracle")
mex6_arms = _load("mex6_arms")
mex6_run = _load("mex6_run")

DEV = mex6_generator.generate_split("dev", mex6_run.DEV_SEED, 1)


@pytest.fixture(scope="module", autouse=True)
def _frozen_signs():
    mex6_arms.load_fitted_signs(mex6_arms.fit_signs(DEV))


def _arm(name):
    return {s.name: s for s in mex6_arms.arm_specs()}[name]


# ---- generator / oracle --------------------------------------------------------

def test_every_cell_reproduces_its_declared_effect() -> None:
    for inst in DEV:
        ok, why = mex6_oracle.planter_agrees(inst.window, inst.stratum)
        assert ok, f"{inst.instance_id}: {why}"


def test_every_instance_is_decidable_from_its_fit_window() -> None:
    for inst in DEV:
        assert mex6_oracle.decidable_from_fit_window(inst.window), inst.instance_id


def test_the_planter_rejects_a_stratum_with_a_different_declared_effect() -> None:
    strata = mex6_generator.STRATA
    for inst in DEV:
        other = next(s for s in sorted(strata) if strata[s] != strata[inst.stratum])
        assert not mex6_oracle.planter_agrees(inst.window, other)[0]


def test_generator_is_deterministic() -> None:
    a = mex6_generator.generate_split("dev", mex6_run.DEV_SEED, 1)
    b = mex6_generator.generate_split("dev", mex6_run.DEV_SEED, 1)
    assert [i.instance_id for i in a] == [i.instance_id for i in b]
    assert [mex6_oracle.oracle(i.window).as_tuple() for i in a] == \
           [mex6_oracle.oracle(i.window).as_tuple() for i in b]


def test_no_arm_can_reach_a_latent_coordinate_or_a_holdout_period() -> None:
    """The oracle must not be reachable from any arm's surface."""
    src = (HERE / "mex6_arms.py").read_text()
    assert ".latent" not in src, "an arm must never read a latent coordinate"
    assert "holdout_periods" not in src, "an arm must never read a holdout period"
    assert "mex6_oracle" not in src.replace("from mex6_oracle import oracle\n", "x"), \
        "arms may only touch the oracle inside the declared fitting routine"


def test_the_two_scales_are_both_generated() -> None:
    assert {i.scale for i in DEV} == set(mex6_model.SCALES)


# ---- arms ----------------------------------------------------------------------

def test_M_is_exact_on_every_hand_authored_cell() -> None:
    m = _arm(mex6_arms.M_ARM)
    for inst in DEV:
        got = mex6_arms.run_arm(m, inst.window, random.Random(0)).as_dict()
        assert got == mex6_oracle.oracle(inst.window).as_dict(), inst.instance_id


def test_every_arm_holding_the_activity_channels_reads_activity_correctly() -> None:
    """No arm is crippled on the half it plainly has the information for."""
    for spec in mex6_arms.arm_specs():
        if not set(mex6_model.ACTIVITY_CHANNELS) <= set(spec.channels):
            continue
        if spec.name.startswith("C_"):
            continue
        for inst in DEV:
            got = mex6_arms.run_arm(spec, inst.window, random.Random(0))
            assert got.activity == mex6_oracle.oracle(inst.window).activity


def test_the_matched_parent_receives_every_channel_M_receives() -> None:
    m = _arm(mex6_arms.M_ARM)
    p = _arm(mex6_arms.B4X_FITTED_ARM)
    assert set(m.channels) <= set(p.channels), "M must never hold information the comparator lacks"


def test_the_fitted_parent_refuses_to_run_before_its_signs_are_frozen() -> None:
    saved = dict(mex6_arms.FITTED_SIGNS)
    mex6_arms.FITTED_SIGNS.clear()
    try:
        with pytest.raises(RuntimeError):
            mex6_arms.run_arm(_arm(mex6_arms.B4X_FITTED_ARM), DEV[0].window, random.Random(0))
    finally:
        mex6_arms.load_fitted_signs(saved)


def test_each_ablation_degrades_exactly_the_strata_declared_to_depend_on_it() -> None:
    m = _arm(mex6_arms.M_ARM)
    for abl, predicted in mex6_run.ABLATION_PREDICTION.items():
        broke = set()
        for inst in DEV:
            truth = mex6_oracle.oracle(inst.window).as_dict()
            base = mex6_arms.run_arm(m, inst.window, random.Random(0)).as_dict()
            got = mex6_arms.run_arm(_arm(abl), inst.window, random.Random(0)).as_dict()
            if base == truth and got != truth:
                broke.add(inst.stratum)
        assert broke == set(predicted), f"{abl}: degraded {sorted(broke)}, predicted {sorted(predicted)}"


def test_the_registered_prediction_support_is_where_the_parent_actually_fails() -> None:
    """P-MEX6-1's support, checked on the split it was registered from."""
    p = _arm(mex6_arms.B4X_FITTED_ARM)
    failing = {inst.stratum for inst in DEV
               if mex6_arms.run_arm(p, inst.window, random.Random(0)).as_dict()
               != mex6_oracle.oracle(inst.window).as_dict()}
    assert failing == set(mex6_run.DECOUPLED_STRATA)


def test_an_untyped_reading_cannot_separate_the_decoupled_strata() -> None:
    """The mechanism claim: one global sign per channel is not enough."""
    for inst in DEV:
        if inst.stratum not in mex6_run.DECOUPLED_STRATA:
            continue
        untyped = mex6_arms._cap_untyped(inst.window, mex6_model.CHANNELS, random.Random(0))
        assert untyped != mex6_oracle.oracle(inst.window).capability


# ---- stages and custody --------------------------------------------------------

def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert mex6_run.stage_selftest(tmp_path) == 0
    rep = json.loads((tmp_path / "ME_X6_SELFTEST_REPORT.json").read_text())
    assert rep["passed"] is True
    for name, v in rep["planted_positives"].items():
        assert v["n"] > 0 and v["tripped"] == v["n"], f"{name} never fired"


def test_dev_stage_is_labelled_development(tmp_path: Path) -> None:
    assert mex6_run.stage_dev(tmp_path, 1) == 0
    res = json.loads((tmp_path / "ME_X6_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert res["label"] == "DEVELOPMENT"
    assert res["split_seed"] == mex6_run.DEV_SEED


def test_dev_stage_refuses_more_than_the_cap(tmp_path: Path) -> None:
    assert mex6_run.stage_dev(tmp_path, 3) == 2


def test_every_gate_reports_the_number_of_instances_it_evaluated(tmp_path: Path) -> None:
    mex6_run.stage_selftest(tmp_path)
    mex6_run.stage_dev(tmp_path, 1)
    g = json.loads((tmp_path / "ME_X6_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    for name, gate in g.items():
        if name == "ROUTE":
            continue
        assert "n_evaluated" in gate, f"{name} has no denominator"
        if gate.get("n_evaluated") == 0:
            assert gate.get("pass") is not True, f"{name} passed on zero instances"


def test_the_coverage_ledger_names_every_unexercised_cell(tmp_path: Path) -> None:
    mex6_run.stage_dev(tmp_path, 1)
    cl = json.loads((tmp_path / "ME_X6_DEVELOPMENT_ANALYSIS_V1.json").read_text()) \
        ["gates"]["COVERAGE_LEDGER"]
    assert cl["all_registered_mechanisms_exercised"] is True
    assert cl["never_exercised"] == []


def test_no_authorization_file_is_committed() -> None:
    assert not mex6_run.AUTH_FILE.exists(), \
        "an authorization file must never be committed to the tree"


def test_protected_stage_refuses_without_authorization(tmp_path: Path, monkeypatch) -> None:
    assert mex6_run.stage_protected(tmp_path, 1, tmp_path / "absent.txt") == 3
    auth = tmp_path / "PROTECTED_RUN_AUTHORIZATION.json"
    monkeypatch.setattr(mex6_run, "AUTH_FILE", auth)

    auth.write_text("{ not json")
    assert mex6_run.stage_protected(tmp_path, 1, tmp_path / "absent.txt") == 3

    auth.write_text(json.dumps({"human_written": False, "human_written_token": "x" * 20}))
    assert mex6_run.stage_protected(tmp_path, 1, tmp_path / "absent.txt") == 3

    auth.write_text(json.dumps({"human_written": True, "human_written_token": "short"}))
    assert mex6_run.stage_protected(tmp_path, 1, tmp_path / "absent.txt") == 3

    auth.write_text(json.dumps({"human_written": True, "human_written_token": "x" * 20,
                                "acknowledged_design_sha256": "0" * 64}))
    assert mex6_run.stage_protected(tmp_path, 1, tmp_path / "absent.txt") == 3


def test_protected_stage_refuses_on_a_bad_seed_with_a_distinct_exit_code(
        tmp_path: Path, monkeypatch) -> None:
    """`could not check` and `checked and fine` must not share an exit code."""
    auth = tmp_path / "PROTECTED_RUN_AUTHORIZATION.json"
    monkeypatch.setattr(mex6_run, "AUTH_FILE", auth)
    auth.write_text(json.dumps({
        "human_written": True, "human_written_token": "x" * 20,
        "acknowledged_design_sha256": mex6_run.sha256_file(mex6_run.DESIGN_JSON)}))
    assert mex6_run.stage_protected(tmp_path, 1, tmp_path / "absent.txt") == 4
    bad = tmp_path / "seed.txt"
    bad.write_text("not-the-committed-seed")
    assert mex6_run.stage_protected(tmp_path, 1, bad) == 4


def test_the_frozen_design_json_matches_the_code_it_describes() -> None:
    d = json.loads(mex6_run.DESIGN_JSON.read_text())
    assert d["strata"].keys() == mex6_generator.STRATA.keys()
    assert d["comparator"]["frozen_fitted_signs"] == mex6_arms.fit_signs(DEV)
    assert d["registered_predictions"]["P-MEX6-1"]["support"] == list(mex6_run.DECOUPLED_STRATA)
    assert d["split_sizes"]["protected_total"] == 50 * len(mex6_generator.CELLS)


# ---- the ME-X7 regression ------------------------------------------------------

def test_every_registered_stratum_is_still_drawn_at_protected_scale() -> None:
    """ME-X7's protected run failed on a count-based generator invariant, and the
    obvious repair silently deleted the offending cell by re-drawing it away.
    This asserts the analogous failure cannot happen here: every registered cell
    must still be drawn when the split is large."""
    insts = mex6_generator.generate_split("regression", "ME-X6-REGRESSION-PROBE", 4)
    drawn = {(i.stratum, i.scale) for i in insts}
    assert drawn == set(mex6_generator.CELLS)
    for stratum in mex6_generator.STRATA:
        n = sum(1 for i in insts if i.stratum == stratum)
        assert n == 4 * len(mex6_model.SCALES), f"{stratum} drew {n}"


def test_the_generator_validity_check_is_not_a_count() -> None:
    """The invariant must compare against a declared expected effect."""
    src = (HERE / "mex6_oracle.py").read_text()
    assert "expected_effect" in src
    assert "len(" not in src.split("def planter_agrees")[1].split("def ")[0], \
        "planter_agrees must not decide on a count"


def test_the_protected_seed_actually_changes_the_windows() -> None:
    """Regression: the window must not be a pure function of (stratum, scale).

    Before this was fixed, `_levels` ignored its rng, so every instance of a cell
    was byte-identical, a 1400-instance split was 14 distinct windows replicated
    100 times, the seed commitment was ceremonial, and every paired exact p-value
    would have been computed over pseudo-replicates at an inflated denominator.
    """
    a = mex6_generator.generate_split("dev", mex6_run.DEV_SEED, 1)
    b = mex6_generator.generate_split("dev", "ME-X6-A-DIFFERENT-SEED", 1)
    ca = [dict(p.channels) for p in a[0].window.periods]
    cb = [dict(p.channels) for p in b[0].window.periods]
    assert ca != cb, "a different seed must produce a different window"


def test_instances_within_a_cell_are_distinct_windows() -> None:
    insts = mex6_generator.generate_split("probe", "ME-X6-DISTINCTNESS-PROBE", 3)

    def key(i):
        return tuple(sorted((k, v) for p in i.window.periods for k, v in p.channels.items()))

    assert len({key(i) for i in insts}) == len(insts), \
        "every instance must be its own window, not a replicate"


def test_the_scale_actually_reaches_the_window() -> None:
    """Otherwise G6 cross-scale transfer is a contrast that could not exist."""
    insts = mex6_generator.generate_split("dev", mex6_run.DEV_SEED, 1)
    by_scale = {}
    for i in insts:
        if i.stratum == "NO_CHANGE":
            by_scale[i.scale] = [dict(p.channels) for p in i.window.periods]
    assert len(by_scale) == 2
    a, b = by_scale.values()
    assert a != b, "the two units of analysis must produce different windows"


def test_no_routing_path_awards_a_residual() -> None:
    """Design 1.3 declares M exact by construction, so no terminal may claim an
    ME-X6 residual on the strength of the M-vs-parent gap."""
    src = (HERE / "mex6_run.py").read_text()
    assert "ME_X6_RESIDUAL_CANDIDATE" not in src
    d = json.loads(mex6_run.DESIGN_JSON.read_text())
    for v in d["routing"].values():
        assert "RESIDUAL_CANDIDATE" not in str(v)


def test_structural_variation_never_moves_a_direction() -> None:
    """The variation is structural only: across many instances of every stratum
    the recomputed effect must still equal the declared one, exactly."""
    insts = mex6_generator.generate_split("probe", "ME-X6-VARIATION-PROBE", 6)
    for inst in insts:
        ok, why = mex6_oracle.planter_agrees(inst.window, inst.stratum)
        assert ok, why
        assert mex6_oracle.decidable_from_fit_window(inst.window)
