"""ME-X5 cross-domain field residual study: end-to-end tests of every runner stage
on planted-signal and null fixtures, in all three native epistemic modes.
Development fixtures only; nothing here is protected evidence."""
from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEX5 = ROOT / "research" / "experiments" / "me-x5"
if str(MEX5) not in sys.path:
    sys.path.insert(0, str(MEX5))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, MEX5 / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mex5_model = _load("mex5_model")
for _m in ("mex5_native_formal", "mex5_native_measurement", "mex5_native_synthesis"):
    _load(_m)
mex5_oracle = _load("mex5_oracle")
mex5_generator = _load("mex5_generator")
mex5_parents = _load("mex5_parents")
mex5_arms = _load("mex5_arms")
mex5_vocab = _load("mex5_vocab")
mex5_run = _load("mex5_run")

MODES = mex5_model.MODES
STRATA = mex5_model.STRATA


# ---- protocol shape: three materially distinct native modes ------------------------

def test_at_least_three_native_modes_with_complete_review_records() -> None:
    assert len(MODES) >= 3
    for m in MODES:
        rec = mex5_run.NATIVE_REVIEWS[m]
        for key in mex5_run.NATIVE_REVIEW_REQUIRED_KEYS:
            assert rec.get(key), (m, key)
        assert rec["mode"] == m


def test_the_three_modes_disagree_on_identity_dependence_and_scope() -> None:
    """Materially distinct means the rules give different answers, not different labels."""
    NF = mex5_oracle.RULES["FORMAL"]
    NM = mex5_oracle.RULES["MEASUREMENT"]
    NS = mex5_oracle.RULES["SYNTHESIS"]
    # identity: a fiducial restriction narrows in the measurement mode only
    assert NM.narrowed_variant(NM.BASE_SIGNATURE) is not None
    assert NF.narrowed_variant(NF.BASE_SIGNATURE) is None
    # a different population is still the same question in the synthesis mode
    other_pop = ("pop_B",) + tuple(NS.BASE_SIGNATURE[1:])
    unit = mex5_model.Unit(uid="u", kind="primary_study", signature=other_pop, context="ctx0",
                           coverage=("h1",), ancestry=(), validator=None)
    target = mex5_model.Target(tid="t", signature=NS.BASE_SIGNATURE, coverage=("h1",),
                               asserted_failure_class=NS.FAILURE_CLASSES[0], requested_authority="BELIEF",
                               context="ctx0")
    assert NS.identity(target, unit) == "EXACT"
    # only the formal mode has no numeric layer
    assert (NF.NUMERIC, NM.NUMERIC, NS.NUMERIC) == (False, True, True)


# ---- parents: every baseline passes its own native known-answer tests ----------------

def test_every_parent_passes_its_native_known_answer_tests() -> None:
    results = mex5_parents.fidelity_selftests()
    failed = [r for r in results if not r["passed"]]
    assert not failed, failed
    assert len(results) >= 15
    assert {"PROVENANCE_REVOCATION", "TMS_SELECTIVE_REOPENING", "DEPENDENCE_ASSESSMENT", "TYPED_TRANSPORT",
            "EVALUATOR_COVERAGE_CONTRACT", "APPARATUS_VALIDITY", "UNCERTAINTY_AGGREGATION",
            "EVIDENCE_SYNTHESIS_POOLING", "SCOPE_BOOKKEEPING", "ASSURANCE_GLOBAL_WITNESS"} <= {r["parent"] for r in results}


# ---- oracle validity ------------------------------------------------------------------

def test_hand_authored_fixtures_reproduced_by_the_oracle() -> None:
    fixtures = mex5_generator.known_answer_fixtures()
    assert len(fixtures) == 9
    for f in fixtures:
        got = mex5_oracle.oracle_trajectory(f["episode"])[-1].decision.as_dict()
        assert got == f["expected"], (f["name"], got)


def test_every_stratum_in_every_mode_reproduces_its_declared_invariant() -> None:
    for mode in MODES:
        for stratum in STRATA:
            ep, traj = mex5_generator.generate_instance("t", "UNIT-SEED", mode, stratum, 0)
            assert ep.mode == mode and ep.stratum == stratum
            assert mex5_oracle.valid_at_v0(ep), (mode, stratum)
            assert mex5_oracle.permutation_invariant(ep), (mode, stratum)
            assert len(mex5_oracle.censored_facts(mex5_arms.final_state(ep))) <= mex5_oracle.MAX_CENSORED_FACTS
            exp_a, exp_l = mex5_generator.STRATUM_INVARIANT[stratum]
            d = traj[-1].decision
            if exp_a is not None:
                assert d.action == exp_a, (mode, stratum, d)
            if exp_l is not None:
                assert d.locus == exp_l, (mode, stratum, d)


def test_generator_is_deterministic_and_round_trips_json() -> None:
    a, _ = mex5_generator.generate_instance("t", "UNIT-SEED", "FORMAL", "HIDDEN_DEPENDENCE", 1)
    b, _ = mex5_generator.generate_instance("t", "UNIT-SEED", "FORMAL", "HIDDEN_DEPENDENCE", 1)
    ja = mex5_model.canonical_json(mex5_model.episode_to_json(a))
    assert ja == mex5_model.canonical_json(mex5_model.episode_to_json(b))
    back = mex5_model.episode_from_json(json.loads(ja))
    assert mex5_model.canonical_json(mex5_model.episode_to_json(back)) == ja
    c, _ = mex5_generator.generate_instance("t", "OTHER-SEED", "FORMAL", "HIDDEN_DEPENDENCE", 1)
    assert mex5_model.canonical_json(mex5_model.episode_to_json(c)) != ja


def test_unresolved_is_not_a_monotone_envelope_in_the_numeric_modes() -> None:
    """The design's reason for enumerating: adding a censored study can move a pooled
    estimate either way, so an optimistic/pessimistic bracket is unsound."""
    NM = mex5_oracle.RULES["MEASUREMENT"]
    ep, _ = mex5_generator.generate_instance("t", "UNIT-SEED", "MEASUREMENT", "CENSORED_UNRESOLVED", 0)
    st = mex5_arms.final_state(ep)
    assert mex5_oracle.oracle_version(st).decision.action == "UNRESOLVED"
    assert NM.aggregate(st, sorted(st.units)) is not None


# ---- arms ------------------------------------------------------------------------------

def _run(name: str, ep):
    spec = {s.name: s for s in mex5_arms.arm_specs()}[name]
    return mex5_arms.run_arm(spec, mex5_arms.final_state(ep), random.Random(7))[0]


def test_no_arm_imports_the_oracle_decision_procedure() -> None:
    src = (MEX5 / "mex5_arms.py").read_text()
    assert "decide_resolved" not in src
    assert "oracle_version" not in src and "oracle_trajectory" not in src


def test_m_and_b5_are_exact_on_every_stratum_in_every_mode() -> None:
    for mode in MODES:
        for stratum in STRATA:
            ep, traj = mex5_generator.generate_instance("t", "UNIT-SEED", mode, stratum, 0)
            exp = traj[-1].decision
            for arm in (mex5_arms.M_ARM, mex5_arms.B5_ARM):
                assert _run(arm, ep).as_tuple() == exp.as_tuple(), (mode, stratum, arm)


def test_separation_pair_verdict_only_is_blind_where_witness_exchange_is_exact() -> None:
    p, q = mex5_generator.separation_pair()
    v1 = [_run(mex5_arms.LADDER[0], c["episode"]).as_dict() for c in (p, q)]
    assert v1[0] == v1[1], "a family-anonymous channel cannot separate P from Q"
    assert any(v1[i] != c["expected"] for i, c in enumerate((p, q))), "and must therefore err on one of them"
    for arm in (mex5_arms.B5_ARM, mex5_arms.M_ARM):
        for c in (p, q):
            assert _run(arm, c["episode"]).as_dict() == c["expected"], (arm, c["name"])


def test_single_parents_break_where_their_semantics_predict() -> None:
    # provenance + apparatus alone cannot see a dependence defeat
    ep, traj = mex5_generator.generate_instance("t", "UNIT-SEED", "FORMAL", "HIDDEN_DEPENDENCE", 0)
    assert traj[-1].decision.action == "WITHHOLD"
    assert _run("B2_PROVENANCE_VERIFIER_RUNTIME", ep).action == "COMMIT"
    # the diagnostic parent has no typed-transport model
    ep, traj = mex5_generator.generate_instance("t", "UNIT-SEED", "MEASUREMENT", "INVALID_TRANSPORT", 0)
    assert _run("B3_DIAGNOSIS_METAREASONING", ep).action == "COMMIT"
    # a two-valued TMS/assurance federation cannot express the unresolved terminal
    ep, traj = mex5_generator.generate_instance("t", "UNIT-SEED", "SYNTHESIS", "CENSORED_UNRESOLVED", 0)
    assert traj[-1].decision.action == "UNRESOLVED"
    assert _run("B4_TMS_ASSURANCE_FEDERATION", ep).action != "UNRESOLVED"
    # a parent with no authority boundary grants operational authority it does not have
    ep, traj = mex5_generator.generate_instance("t", "UNIT-SEED", "FORMAL", "AUTHORITY_MISMATCH", 0)
    assert traj[-1].decision.authority == "BELIEF_ONLY"
    assert _run("B0_DIRECT_NATIVE_PIPELINE", ep).authority == "BELIEF_AND_ACTION"


def test_boolean_parents_cannot_see_the_numeric_defeat_that_M_sees() -> None:
    """The registered reason the two numeric modes are not Boolean-parent territory."""
    found = False
    for i in range(20):
        ep, traj = mex5_generator.generate_instance("t", "UNIT-SEED", "SYNTHESIS", "DEFEATED_SUPPORT", i)
        if ep.features.get("variant") != "NUMERIC_AGGREGATE_FALLS_BELOW_THRESHOLD":
            continue
        found = True
        assert traj[-1].decision.as_tuple() == ("WITHHOLD", "SUPPORT_DEFEAT", "BELIEF_ONLY")
        assert _run("B4_TMS_ASSURANCE_FEDERATION", ep).action == "COMMIT"
        assert _run("M_MINUS_NUMERIC", ep).action == "COMMIT"
        assert _run(mex5_arms.M_ARM, ep).action == "WITHHOLD"
        break
    assert found, "the numeric-defeat variant must be reachable in the synthesis mode"


def test_every_ablation_loses_something_somewhere() -> None:
    pairs = mex5_generator.generate_split("t", "UNIT-ABL", 1)
    rng = random.Random(3)
    specs = {s.name: s for s in mex5_arms.arm_specs()}
    for abl in mex5_run.ABLATIONS:
        losses = 0
        for ep, traj in pairs:
            got = mex5_arms.run_arm(specs[abl], mex5_arms.final_state(ep), rng)[0]
            losses += int(got.as_tuple() != traj[-1].decision.as_tuple())
        assert losses > 0, abl


# ---- changed vocabulary -----------------------------------------------------------------

def test_changed_vocabulary_rule_set_is_mode_blind_and_free_of_orion_terms() -> None:
    src = (MEX5 / "mex5_vocab.py").read_text()
    for banned in ("selective_reopen", "ProblemContract", "orion_v2", "epistemic transition"):
        assert banned not in src, banned
    assert set(mex5_vocab.ADAPTERS) == set(MODES)
    assert set(mex5_vocab.NEUTRAL_RULES) <= set(mex5_model.LOCI)


def test_changed_vocabulary_recovers_the_class_in_every_mode() -> None:
    for mode in MODES:
        n = ok = 0
        for stratum in STRATA:
            for i in range(2):
                ep, traj = mex5_generator.generate_instance("t", "UNIT-VOCAB", mode, stratum, i)
                d = traj[-1].decision
                if d.action == "UNRESOLVED":
                    continue
                n += 1
                ok += int(mex5_vocab.classify(mex5_arms.final_state(ep)) == d.locus)
        assert n >= 15 and ok / n >= 0.90, (mode, ok, n)


# ---- runner stages -----------------------------------------------------------------------

def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert mex5_run.main(["selftest", "--out", str(tmp_path)]) == 0
    rep = json.loads((tmp_path / "ME_X5_SELFTEST_REPORT.json").read_text())
    assert rep["passed"] is True
    assert rep["parent_fidelity_passed"] and rep["known_answer_passed"] and rep["separation_passed"]
    assert rep["native_review_complete"] is True
    assert rep["native_review"]["independent_reviewer"] is False
    assert rep["oracle_validity"]["pass"] is True


def test_dev_stage_end_to_end_labelled_development(tmp_path: Path) -> None:
    assert mex5_run.main(["selftest", "--out", str(tmp_path)]) == 0
    assert mex5_run.main(["dev", "--out", str(tmp_path)]) == 0
    res = json.loads((tmp_path / "ME_X5_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert res["label"] == "DEVELOPMENT" and len(res["instances"]) == 36
    assert "expected" not in res["instances"][0]
    ana = json.loads((tmp_path / "ME_X5_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    g = ana["gates"]
    assert g["G0a_NATIVE_KNOWN_ANSWER"]["pass"] and g["G0b_ORACLE_VALIDITY"]["pass"]
    assert g["G0c_NULL_CALIBRATION"]["pass"] is True
    assert g["G1a_B5_REPRODUCES_M"]["pass"] is True
    assert g["G1b_M_ADVANTAGE_PER_MODE"]["pass_modes"] == []
    assert g["ROUTE"]["route"] in {"PARENT_SUFFICIENT", "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL",
                                   "MODE_SPECIFIC_RESIDUAL", "ME_X5_FIELD_RESIDUAL_CANDIDATE", "CANNOT_CHECK"}
    assert g["ROUTE"]["R3_ESTABLISHED_FIELD_GRANTABLE"] is False
    # the ladder is reported per mode and never pooled into one claim
    assert set(g["G4_INTERFACE_LADDER"]["per_mode"]) == set(MODES)
    assert set(g["G4_INTERFACE_LADDER"]["decisive_rung_per_mode"]) == set(MODES)
    for m in MODES:
        assert set(g["G4_INTERFACE_LADDER"]["per_mode"][m]["rung_exact_rates"]) == set(mex5_arms.LADDER)
    md = (tmp_path / "ME_X5_DEVELOPMENT_ANALYSIS_V1.md").read_text()
    assert md.startswith("# ME-X5 analysis — DEVELOPMENT")
    assert "Interface ladder, reported per mode (never pooled)" in md


def test_dev_stage_refuses_more_than_forty_instances(tmp_path: Path) -> None:
    assert mex5_run.main(["dev", "--out", str(tmp_path), "--per-cell", "2"]) == 2


def test_interface_standard_terminal_is_a_positive_test_not_the_negation_of_the_gap(tmp_path: Path) -> None:
    """ME-X2's caveat (a): the terminal must not be computable as not-G1b."""
    src = (MEX5 / "mex5_run.py").read_text()
    assert "positive_interface_standard" in src
    for needed in ("interface_load_bearing", "equivalent_within_margin", "EQUIVALENCE_MARGIN_PER_MODE"):
        assert needed in src, needed
    assert mex5_run.main(["selftest", "--out", str(tmp_path)]) == 0
    assert mex5_run.main(["dev", "--out", str(tmp_path)]) == 0
    g = json.loads((tmp_path / "ME_X5_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    for m in MODES:
        v = g["G4_INTERFACE_LADDER"]["per_mode"][m]
        assert v["positive_interface_standard"] == (v["monotone"] and v["interface_load_bearing"]
                                                    and v["equivalent_within_margin"])


def test_protected_stage_refuses_without_authorization(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert not mex5_run.AUTH_FILE.exists(), "PROTECTED_RUN_AUTHORIZATION.json must be absent in the repository"
    assert mex5_run.main(["protected", "--out", str(tmp_path)]) == 3
    assert not list(tmp_path.glob("ME_X5_PROTECTED_*"))
    monkeypatch.setattr(mex5_run, "AUTH_FILE", tmp_path / "PROTECTED_RUN_AUTHORIZATION.json")
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": False, "human_written_token": ""}))
    assert mex5_run.main(["protected", "--out", str(tmp_path)]) == 3
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps(
        {"human_written": True, "human_written_token": "unit-test-token-not-a-real-authorization",
         "acknowledged_design_sha256": "0" * 64}))
    assert mex5_run.main(["protected", "--out", str(tmp_path)]) == 3
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps(
        {"human_written": True, "human_written_token": "unit-test-token-not-a-real-authorization",
         "acknowledged_design_sha256": mex5_run.sha256_file(mex5_run.DESIGN_JSON)}))
    seed = tmp_path / "seed.txt"
    seed.write_text("NOT-THE-COMMITTED-SEED\n")
    assert mex5_run.main(["protected", "--out", str(tmp_path), "--seed-file", str(seed)]) == 4
    assert not list(tmp_path.glob("ME_X5_PROTECTED_*"))


def test_design_json_freezes_the_commitment_modes_strata_and_arms() -> None:
    d = json.loads(mex5_run.DESIGN_JSON.read_text())
    assert d["schema_version"] == "orion.v2.me-x5.cross-domain-study-design.v1"
    assert len(d["seed_commitment"]["protected_seed_sha256"]) == 64
    assert set(d["modes"]) == set(MODES) and len(d["modes"]) >= 3
    assert set(d["strata"]) == set(STRATA)
    assert d["counts"]["protected_total"] == 1440 and d["counts"]["dev_total"] <= 40
    assert set(d["arms"]) == {s.name for s in mex5_arms.arm_specs()}
    assert d["ladder"] == list(mex5_arms.LADDER)
    assert d["field_support_ladder"]["R3_ESTABLISHED_FIELD"].startswith("NEVER")
    assert "NOT GRANTABLE" in d["field_support_ladder"]["R2_EMERGING_INTERDISCIPLINARY_RESIDUAL"]
    assert d["pre_registered_expectation"] == "PARENT_SUFFICIENT"
    assert d["outcomes"]["pooling_rule"].startswith("every gate is evaluated per mode")
