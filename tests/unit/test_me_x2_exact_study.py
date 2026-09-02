"""ME-X2 exact locus-diagnosis / minimum-escalation study: end-to-end tests of
every runner stage on planted-signal and null fixtures. Development fixtures
only; nothing here is protected evidence."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEX2 = ROOT / "research" / "experiments" / "me-x2"
if str(MEX2) not in sys.path:
    sys.path.insert(0, str(MEX2))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, MEX2 / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mex2_model = _load("mex2_model")
mex2_catalogue = _load("mex2_catalogue")
mex2_oracle = _load("mex2_oracle")
mex2_generator = _load("mex2_generator")
mex2_parents = _load("mex2_parents")
mex2_arms = _load("mex2_arms")
mex2_run = _load("mex2_run")

FIXTURES = mex2_generator.known_answer_fixtures()
BY_NAME = {f["name"]: f for f in FIXTURES}


def _run_arm(name: str, inst):
    spec = {s.name: s for s in mex2_arms.arm_specs()}[name]
    return mex2_oracle.Environment(inst).run(mex2_arms.make_policy(spec, "unit"))


def _score(name: str, fixture) -> dict:
    inst = fixture["instance"]
    return mex2_run.score_trajectory(_run_arm(name, inst).as_dict(), mex2_oracle.oracle_targets(inst), mex2_model.instance_to_json(inst))


# ---- parents: native known-answer tests must pass before use ------------------

def test_every_parent_passes_its_native_known_answer_tests() -> None:
    results = mex2_parents.fidelity_selftests()
    assert not [r for r in results if not r["passed"]], [r for r in results if not r["passed"]]
    assert {r["parent"] for r in results} == {"GDE", "VOI", "PLANNER", "TEST_SEQUENCING", "ABSTENTION", "TAXONOMY", "MDA"}


def test_catalogue_cross_references_resolve_and_cover_every_class() -> None:
    seen = set()
    for name, tpl in mex2_catalogue.TEMPLATES.items():
        causes = {c[0] for c in tpl["causes"]}
        assert len(tpl["probes"]) <= mex2_model.MAX_PROBES
        assert len([i for i in tpl["interventions"] if i[1] <= 1]) <= mex2_model.MAX_CHEAP_INTERVENTIONS
        for p in tpl["probes"]:
            assert set(p[4]) <= causes, (name, p[0])
        for i in tpl["interventions"]:
            assert set(i[2]) | set(i[3]) <= causes, (name, i[0])
        for c in tpl["causes"]:
            seen.add(c[1])
            assert any(i[0] == c[3] and c[0] in i[2] for i in tpl["interventions"]), (name, c)
    assert seen == set(mex2_model.CLASSES) - {"CANNOT_IDENTIFY"}
    assert mex2_catalogue.TAXONOMY_PATTERNS["UNMAPPED_AGENT_LOOP_PATTERN"]["orion_mapping"] == "NO_MAPPING"


# ---- oracle -------------------------------------------------------------------

def test_hand_authored_known_answer_fixtures_reproduced_by_oracle() -> None:
    assert len(FIXTURES) == 14
    for f in FIXTURES:
        orc = mex2_oracle.oracle_targets(f["instance"])
        for k, v in f["expected"].items():
            assert orc[k] == v, (f["name"], k, orc[k], v)
        assert orc["exhaustive_agrees"], f["name"]


def test_oracle_enumeration_equals_branch_and_bound_on_generated_instances() -> None:
    for stratum in mex2_model.STRATA:
        for inst, orc in mex2_generator.generate_pair("t", "UNIT-SEED", stratum, 0):
            assert orc["exhaustive_agrees"], inst.instance_id
            assert orc.get("uniformly_decidable") is True
            assert mex2_oracle.uniformly_decidable(inst)
        assert orc["oracle_class"] in mex2_model.CLASSES


def test_evaluator_mediated_probe_is_laundered_by_a_blind_evaluator() -> None:
    inst = BY_NAME["KA-06-MEASUREMENT_OR_EVALUATOR_BLIND"]["instance"]
    ppc = inst.probe("ppc_via_evaluator")
    assert ppc.evaluator_mediated
    assert ppc.designed_outcome("EVALUATOR_BLIND") == "REJECT"      # what a valid evaluator would report
    assert ppc.outcome("EVALUATOR_BLIND") == ppc.nominal            # what the blind evaluator does report


def test_same_fix_pair_identifies_class_and_level_but_not_locus() -> None:
    orc = mex2_oracle.oracle_targets(BY_NAME["KA-13-SAME_FIX_LOCUS_UNRESOLVED"]["instance"])
    assert orc["oracle_class"] == "MODEL_FAMILY_INADEQUATE" and orc["oracle_level"] == 2
    assert orc["oracle_locus"] == "CANNOT_IDENTIFY" and len(orc["indistinguishable_set"]) == 2


def test_generator_is_deterministic_and_round_trips_json() -> None:
    a = mex2_generator.generate_pair("t", "UNIT-SEED", "SEARCH_INSUFFICIENT", 1)[0][0]
    b = mex2_generator.generate_pair("t", "UNIT-SEED", "SEARCH_INSUFFICIENT", 1)[0][0]
    ja = mex2_model.canonical_json(mex2_model.instance_to_json(a))
    assert ja == mex2_model.canonical_json(mex2_model.instance_to_json(b))
    assert mex2_model.canonical_json(mex2_model.instance_to_json(mex2_model.instance_from_json(json.loads(ja)))) == ja
    c = mex2_generator.generate_pair("t", "OTHER-SEED", "SEARCH_INSUFFICIENT", 1)[0][0]
    assert mex2_model.canonical_json(mex2_model.instance_to_json(c)) != ja


def test_paired_instances_share_everything_except_the_hidden_truth() -> None:
    (a, _), (b, _) = mex2_generator.generate_pair("t", "UNIT-SEED", "MODEL_FAMILY_INADEQUATE", 0)
    ja = mex2_model.instance_to_json(a, include_truth=False); jb = mex2_model.instance_to_json(b, include_truth=False)
    for k in ("symptom", "pattern", "apparent_class", "causes", "probes", "interventions", "budget"):
        assert ja[k] == jb[k], k
    assert a.truth != b.truth and a.partner_instance_id == b.instance_id


def test_public_view_and_results_file_never_expose_the_truth() -> None:
    inst = mex2_generator.generate_pair("t", "UNIT-SEED", "WORKFLOW_INADEQUATE", 0)[0][0]
    assert not hasattr(mex2_oracle.public_of(inst), "truth")
    assert "truth" not in mex2_model.instance_to_json(inst, include_truth=False)


# ---- arms ---------------------------------------------------------------------

def test_m_and_b5_are_decision_correct_on_every_hand_authored_fixture() -> None:
    for f in FIXTURES:
        for arm in (mex2_run.M_ARM, mex2_run.B5_ARM):
            assert _score(arm, f)["decision_correct"], (f["name"], arm)


def test_separation_pair_verdict_only_fails_structure_exchange_succeeds() -> None:
    p, q = mex2_generator.separation_pair()
    v = [_score(mex2_run.LADDER[0], c) for c in (p, q)]
    assert v[0]["decision_seq"] == v[1]["decision_seq"], "verdict-only exchange must be blind to the P/Q difference"
    assert not (v[0]["decision_correct"] and v[1]["decision_correct"])
    for arm in (mex2_run.B5_ARM, mex2_run.M_ARM):
        assert _score(arm, p)["decision_correct"] and _score(arm, q)["decision_correct"], arm


def test_taxonomy_arm_over_escalates_on_the_decoy_and_b0_cannot_reach_level_two() -> None:
    decoy = BY_NAME["KA-11-NO_ESCALATION_NEEDED_DECOY"]
    s = _score("B2_FAILURE_TAXONOMY_DIAGNOSIS", decoy)
    assert s["false_escalation"] and not s["decision_correct"]
    assert _score(mex2_run.M_ARM, decoy)["decision_correct"]
    hard = BY_NAME["KA-04-REPRESENTATION_INSUFFICIENT"]
    assert not _score("B0_RETRY_SEARCH", hard)["decision_correct"]


def test_mda_arm_expands_the_model_family_where_a_lower_repair_suffices() -> None:
    # SEP-P: the only probe is evaluator-mediated and rejects under both live causes, so criticism-driven
    # expansion fires although the level-1 repair is the oracle minimum
    p, _q = mex2_generator.separation_pair()
    s = _score("B4_MDA_MODEL_EXPANSION", p)
    assert s["max_level"] is not None and s["max_level"] >= 2 and s["false_escalation"] and not s["decision_correct"]
    assert _score(mex2_run.M_ARM, p)["decision_correct"]


def test_abstention_arm_declares_cannot_identify_where_the_oracle_does() -> None:
    s = _score("B1_UNCERTAINTY_ABSTENTION", BY_NAME["KA-12-CANNOT_IDENTIFY"])
    assert s["correct_ci"] and not s["false_ci"]


def test_m_declares_cannot_identify_and_never_escalates_there() -> None:
    s = _score(mex2_run.M_ARM, BY_NAME["KA-12-CANNOT_IDENTIFY"])
    assert s["correct_ci"] and s["decision_correct"] and not s["false_escalation"]


def test_m_ablations_break_where_their_omission_predicts() -> None:
    # without the diagnostic-evaluator gate, an undiscriminated locus is converted into a forced
    # attribution: the arm escalates first and only then reports CANNOT_IDENTIFY
    s = _score("M_MINUS_DIAGNOSTIC_EVALUATOR_GATE", BY_NAME["KA-12-CANNOT_IDENTIFY"])
    assert s["false_escalation"] and not s["decision_correct"]
    assert _score(mex2_run.M_ARM, BY_NAME["KA-12-CANNOT_IDENTIFY"])["decision_correct"]
    # always-escalate fails the hostile decoy; never-escalate fails the warranted level-3 case
    assert _score("M_ALWAYS_ESCALATE_WHEN_STUCK", BY_NAME["KA-11-NO_ESCALATION_NEEDED_DECOY"])["false_escalation"]
    assert not _score("M_NEVER_ESCALATE", BY_NAME["KA-04-REPRESENTATION_INSUFFICIENT"])["decision_correct"]
    # shuffled locus labels destroy the mapping from hypothesis to minimal fix
    shuffled = [_score("M_LOCUS_LABELS_SHUFFLED", f)["decision_correct"] for f in FIXTURES]
    assert sum(shuffled) < sum(_score(mex2_run.M_ARM, f)["decision_correct"] for f in FIXTURES)


def test_no_arm_module_imports_the_oracle_targets() -> None:
    src = (MEX2 / "mex2_arms.py").read_text()
    assert "oracle_targets" not in src and "per_cause_targets" not in src
    assert "from mex2_oracle import ArmView" in src


# ---- runner stages ------------------------------------------------------------

def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert mex2_run.main(["selftest", "--out", str(tmp_path)]) == 0
    rep = json.loads((tmp_path / "ME_X2_SELFTEST_REPORT.json").read_text())
    assert rep["passed"] is True and rep["separation"]["passed"] is True
    assert rep["null_calibration"]["pass"] is True
    assert all(k["passed"] for k in rep["known_answer"]) and len(rep["known_answer"]) == 14


def test_dev_stage_end_to_end_labelled_development(tmp_path: Path) -> None:
    assert mex2_run.main(["dev", "--out", str(tmp_path), "--pairs-per-stratum", "1"]) == 0
    res = json.loads((tmp_path / "ME_X2_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert res["label"] == "DEVELOPMENT" and len(res["instances"]) == 24
    assert all("truth" not in r["public"] for r in res["instances"])
    ana = json.loads((tmp_path / "ME_X2_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    assert ana["gates"]["ROUTE"]["route"] in {"PARENT_SUFFICIENT", "ME_X2_RESIDUAL_CANDIDATE", "M_OVER_ESCALATES", "QUALITY_COST_TRADEOFF_NO_DOMINANCE", "CANNOT_CHECK"}
    assert (tmp_path / "ME_X2_DEVELOPMENT_ANALYSIS_V1.md").read_text().startswith("# ME-X2 analysis — DEVELOPMENT")


def test_dev_stage_refuses_more_than_the_cap(tmp_path: Path) -> None:
    assert mex2_run.main(["dev", "--out", str(tmp_path), "--pairs-per-stratum", "3"]) == 2


def test_analyze_stage_on_planted_signal_and_null(tmp_path: Path) -> None:
    pairs = mex2_generator.generate_split("t", "UNIT-ANALYZE", {s: 1 for s in mex2_model.STRATA})
    res, cus = mex2_run.run_instances(pairs, "DEVELOPMENT", "UNIT-ANALYZE")
    res.pop("_timing_wall_ns", None)
    rp = tmp_path / "ME_X2_T_RESULTS_V1.json"; cp = tmp_path / "c.json"
    rp.write_text(json.dumps(res)); cp.write_text(json.dumps(cus))
    assert mex2_run.main(["analyze", "--results", str(rp), "--custody", str(cp), "--out", str(tmp_path)]) == 0
    ana = json.loads((tmp_path / "ME_X2_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    per = ana["score"]["per_arm"]; g = ana["gates"]
    # planted signal: M and B5 solve it; nulls at floor
    assert per[mex2_run.M_ARM]["decision_rate"] >= 0.9 and per[mex2_run.B5_ARM]["decision_rate"] >= 0.9
    assert per["C_RANDOM_POLICY"]["decision_rate"] <= mex2_run.RANDOM_MAX
    assert per["C_NEVER_INTERVENE"]["decision_rate"] < per[mex2_run.M_ARM]["decision_rate"]
    assert g["G0b_ORACLE_SELF_AGREEMENT"]["exhaustive_agrees_all"] and g["G0b_ORACLE_SELF_AGREEMENT"]["variant_invariants_hold"]
    assert g["G0c_NULL_CALIBRATION"]["never_intervene_correct_on_identifiable"] == 0
    assert g["G1b_M_ADVANTAGE"]["pass"] is False and g["G3_MEDIATION"]["applicable"] is False
    assert g["G4_INTERFACE_LADDER"]["terminal"] in {"RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL", "CONTROL_RESIDUAL_CANDIDATE_AT_FULL_STRUCTURE", "LADDER_NON_MONOTONE"}


def test_protected_stage_refuses_without_authorization(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert mex2_run.main(["protected", "--out", str(tmp_path)]) == 3
    assert not list(tmp_path.glob("ME_X2_PROTECTED_*"))
    monkeypatch.setattr(mex2_run, "AUTH_FILE", tmp_path / "PROTECTED_RUN_AUTHORIZATION.json")
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": False, "human_written_token": ""}))
    assert mex2_run.main(["protected", "--out", str(tmp_path)]) == 3
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": True, "human_written_token": "short"}))
    assert mex2_run.main(["protected", "--out", str(tmp_path)]) == 3
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": True, "human_written_token": "unit-test-token-not-a-real-authorization", "acknowledged_design_sha256": "0" * 64}))
    assert mex2_run.main(["protected", "--out", str(tmp_path)]) == 3
    design_sha = mex2_run.sha256_file(mex2_run.DESIGN_JSON)
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": True, "human_written_token": "unit-test-token-not-a-real-authorization", "acknowledged_design_sha256": design_sha}))
    seed = tmp_path / "seed.txt"; seed.write_text("NOT-THE-COMMITTED-SEED\n")
    assert mex2_run.main(["protected", "--out", str(tmp_path), "--seed-file", str(seed)]) == 4
    assert mex2_run.main(["protected", "--out", str(tmp_path), "--seed-file", str(tmp_path / "absent.txt")]) == 4
    assert not list(tmp_path.glob("ME_X2_PROTECTED_*"))


def test_design_json_freezes_commitment_strata_and_arms() -> None:
    d = json.loads(mex2_run.DESIGN_JSON.read_text())
    assert d["schema_version"] == "orion.v2.me-x2.exact-study-design.v1"
    assert len(d["seed_commitment"]["protected_seed_sha256"]) == 64
    assert d["splits"]["protected"]["instances"] == 1200 and d["splits"]["development"]["instances"] <= mex2_run.DEV_CAP
    assert set(d["arms"]) == {s.name for s in mex2_arms.arm_specs()}
    assert set(d["vocabularies"]["obstruction_classes"]) == set(mex2_model.CLASSES)
    assert d["primary_endpoint"].startswith("INTERVENTION_DECISION_AND_OUTCOME")
