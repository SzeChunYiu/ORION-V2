"""ME-X7 exact external-witness study: end-to-end tests of every runner stage on
planted-signal and null fixtures. Development fixtures only; nothing here is
protected evidence."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEX7 = ROOT / "research" / "experiments" / "me-x7"
if str(MEX7) not in sys.path:
    sys.path.insert(0, str(MEX7))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, MEX7 / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mex7_model = _load("mex7_model")
mex7_parents = _load("mex7_parents")
mex7_oracle = _load("mex7_oracle")
mex7_generator = _load("mex7_generator")
mex7_arms = _load("mex7_arms")
mex7_run = _load("mex7_run")

DESIGN_JSON = MEX7 / "ME_X7_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V1.json"


# ---- parents: native known-answer tests must pass before use -----------------

def test_every_parent_passes_its_native_known_answer_tests() -> None:
    results = mex7_parents.fidelity_selftests()
    failed = [r for r in results if not r["passed"]]
    assert not failed, failed
    assert {r["parent"] for r in results} == set(mex7_parents.PARENT_NAMES)
    # every parent must contribute more than one case: a single-case "suite"
    # is the shape that reports zero violations because it never ran.
    for name in mex7_parents.PARENT_NAMES:
        assert sum(1 for r in results if r["parent"] == name) >= 2, name


def test_resolution_checker_rejects_an_unsound_step_and_accepts_a_sound_one() -> None:
    rc = mex7_parents.ResolutionChecker()
    assert rc.check([frozenset({1}), frozenset({-1})], [(0, 1, frozenset())])
    assert not rc.check([frozenset({1, 2}), frozenset({-1, 3})], [(0, 1, frozenset({2}))])


# ---- oracle: hand-authored fixtures, exhaustive agreement, planted positives --

def test_hand_authored_known_answer_fixtures_reproduced_by_oracle() -> None:
    fixtures = mex7_generator.known_answer_fixtures()
    assert len(fixtures) == len(mex7_model.CELLS) == 25
    for f in fixtures:
        exp = mex7_oracle.oracle(f["instance"].episode)
        assert exp.verdict == f["expected"]["verdict"], f["name"]
        assert exp.defect_class == f["expected"]["defect_class"], f["name"]
        assert exp.exhaustive_agrees, f["name"]


def test_oracle_direct_rule_equals_exhaustive_enumeration_on_every_cell() -> None:
    for stratum, mode in mex7_model.CELLS:
        for i in range(2):
            inst = mex7_generator.generate_instance("t", "UNIT-SEED", stratum, mode, i)
            exp = mex7_oracle.oracle(inst.episode)
            assert exp.exhaustive_agrees, (stratum, mode, i)
            ok, why = mex7_oracle.planter_agrees(inst.episode, stratum)
            assert ok, (stratum, mode, i, why)


def test_planted_positives_trip_the_no_alarm_assertions() -> None:
    """Every no-alarm assertion is paired with a case that must trip it."""
    probes = mex7_generator.planted_positives()
    assert len(probes) >= 4
    tripped = 0
    for probe in probes:
        agreed, _ = mex7_oracle.planter_agrees(probe["episode"], probe["claimed_stratum"])
        if probe["must_be_rejected"]:
            assert not agreed, probe["name"]
            tripped += 1
        else:
            assert agreed, probe["name"]
    assert tripped >= 3, "the G0b assertion must be demonstrably trippable"


def test_generator_is_deterministic_and_round_trips_json() -> None:
    a = mex7_generator.generate_instance("t", "UNIT-SEED", "HIDDEN_DEPENDENCE", "MODE_FORMAL", 1)
    b = mex7_generator.generate_instance("t", "UNIT-SEED", "HIDDEN_DEPENDENCE", "MODE_FORMAL", 1)
    ja = mex7_model.canonical_json(mex7_model.instance_to_json(a))
    jb = mex7_model.canonical_json(mex7_model.instance_to_json(b))
    assert ja == jb
    back = mex7_model.instance_from_json(json.loads(ja))
    assert mex7_model.canonical_json(mex7_model.instance_to_json(back)) == ja
    c = mex7_generator.generate_instance("t", "OTHER-SEED", "HIDDEN_DEPENDENCE", "MODE_FORMAL", 1)
    assert mex7_model.canonical_json(mex7_model.instance_to_json(c)) != ja


def test_the_episode_schema_carries_no_answer_key() -> None:
    """No arm may see the stratum, the injected class or the oracle verdict."""
    banned = set(mex7_model.INJECTION_CLASSES) | set(mex7_model.CONTROL_STRATA) | {
        mex7_model.REJECT, mex7_model.ACCEPT,
    }
    for stratum, mode in mex7_model.CELLS:
        inst = mex7_generator.generate_instance("t", "UNIT-SEED", stratum, mode, 0)
        blob = mex7_model.canonical_json(mex7_model.episode_to_json(inst.episode))
        # the evaluator contract legitimately names the classes it requires;
        # everything else in the episode must be free of the vocabulary.
        blob = blob.replace(
            mex7_model.canonical_json(list(inst.episode.contract.decision_relevant_classes)), ""
        )
        for word in banned:
            assert word not in blob, (stratum, mode, word)
        assert stratum not in blob or stratum in mex7_model.INJECTION_CLASSES


def test_arms_never_import_the_oracle() -> None:
    text = (MEX7 / "mex7_arms.py").read_text(encoding="utf-8")
    code = [ln for ln in text.splitlines() if ln.startswith(("import ", "from "))]
    assert not [ln for ln in code if "mex7_oracle" in ln], code
    assert "mex7_oracle" not in text.split('"""', 2)[-1]


# ---- arms: cross-implementation agreement, M and B5 exact --------------------

def test_arm_modules_independently_reproduce_the_oracle_check_table() -> None:
    n = 0
    for stratum, mode in mex7_model.CELLS:
        for i in range(2):
            inst = mex7_generator.generate_instance("t", "UNIT-SEED", stratum, mode, i)
            vis = mex7_arms.visible_nodes(inst.episode, full_registry=True)
            for check in mex7_model.CHECKS:
                assert mex7_oracle.CHECK_FN[check](inst.episode, vis) == mex7_arms.MODULE_CHECK[check](
                    inst.episode, vis
                ), (check, stratum, mode, i)
                n += 1
    assert n == len(mex7_model.CELLS) * 2 * len(mex7_model.CHECKS)


def _arm(name: str, episode):
    import random

    spec = {s.name: s for s in mex7_arms.arm_specs()}[name]
    return mex7_arms.run_arm(spec, episode, random.Random(0))


def test_m_and_b5_are_exact_on_every_hand_authored_fixture() -> None:
    for f in mex7_generator.known_answer_fixtures():
        for name in (mex7_arms.M_ARM, mex7_arms.B5_ARM):
            out = _arm(name, f["instance"].episode)
            assert out.verdict == f["expected"]["verdict"], (f["name"], name)
            if out.verdict == mex7_model.REJECT:
                assert out.detected_class == f["expected"]["defect_class"], (f["name"], name)


def test_separation_pair_self_contained_witness_is_blind_identity_exporting_is_not() -> None:
    p, q = mex7_generator.separation_pair()
    ep_p, ep_q = mex7_oracle.oracle(p.episode), mex7_oracle.oracle(q.episode)
    assert ep_p.verdict == mex7_model.REJECT and ep_p.defect_class == "HIDDEN_DEPENDENCE"
    assert ep_q.verdict == mex7_model.ACCEPT
    sc = [_arm("M_MINUS_REGISTRY_RESOLUTION", c.episode) for c in (p, q)]
    assert sc[0].verdict == sc[1].verdict, "a self-contained witness cannot separate P from Q"
    assert sc[0].verdict != ep_p.verdict or sc[1].verdict != ep_q.verdict
    for name in (mex7_arms.M_ARM, mex7_arms.B5_ARM):
        assert _arm(name, p.episode).verdict == mex7_model.REJECT
        assert _arm(name, q.episode).verdict == mex7_model.ACCEPT


def test_single_parents_break_where_their_native_semantics_predict() -> None:
    fx = {f["name"]: f["instance"].episode for f in mex7_generator.known_answer_fixtures()}
    # a proof checker accepts a sound derivation of the wrong statement
    ep = fx["KA-WRONG_PROBLEM_OR_SPECIFICATION-MODE_FORMAL"]
    assert _arm("A0_PROOF_CERTIFICATE_ONLY", ep).verdict == mex7_model.ACCEPT
    assert _arm(mex7_arms.M_ARM, ep).verdict == mex7_model.REJECT
    # two-valued provenance treats a disputed ancestor as a revoked one
    ep = mex7_generator.plant_censored(
        mex7_generator.build_base(__import__("random").Random(3), "MODE_COMPUTATIONAL"),
        __import__("random").Random(3),
        "CENSOR_SOURCE",
    )
    assert mex7_oracle.oracle(ep).verdict == mex7_model.CANNOT_CHECK
    assert _arm("A1_PROVENANCE_ONLY", ep).verdict == mex7_model.REJECT
    assert _arm(mex7_arms.M_ARM, ep).verdict == mex7_model.CANNOT_CHECK
    # provenance-only and replay-only are blind to authority overreach
    ep = fx["KA-AUTHORITY_OVERREACH-MODE_COMPUTATIONAL"]
    for name in ("A1_PROVENANCE_ONLY", "A2_REPLAY_ONLY", "A4_DEPENDENCE_AUDIT"):
        assert _arm(name, ep).verdict == mex7_model.ACCEPT, name


def test_dropping_the_evaluator_contract_turns_abstention_into_false_acceptance() -> None:
    ep = {f["name"]: f["instance"].episode for f in mex7_generator.known_answer_fixtures()}[
        "KA-EVALUATOR_BLIND_SPOT-MODE_COMPUTATIONAL"
    ]
    assert _arm(mex7_arms.M_ARM, ep).verdict == mex7_model.REJECT
    assert _arm("M_MINUS_EVALUATOR_CONTRACT", ep).verdict == mex7_model.ACCEPT


def test_each_omission_blinds_exactly_the_classes_whose_check_needs_that_field() -> None:
    field_to_arm = {fld: name for name, fld in mex7_arms.ABLATION_FIELDS}
    for cls in mex7_model.INJECTION_CLASSES:
        check = mex7_model.CHECK_FOR_CLASS[cls]
        needed = {field_to_arm[f] for f in mex7_model.REQUIRED_FIELDS[check] if f in field_to_arm}
        for mode in mex7_model.MODES:
            if not mex7_model.cell_applicable(cls, mode):
                continue
            ep = mex7_generator.generate_instance("t", "UNIT-SEED", cls, mode, 0).episode
            for name, _ in mex7_arms.ABLATION_FIELDS:
                out = _arm(name, ep)
                detected = out.verdict == mex7_model.REJECT and out.detected_class == cls
                assert detected == (name not in needed), (cls, mode, name)


# ---- runner stages ------------------------------------------------------------

def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert mex7_run.stage_selftest(tmp_path) == 0
    report = json.loads((tmp_path / "ME_X7_SELFTEST_REPORT.json").read_text())
    assert report["passed"] is True
    assert report["separation"]["passed"] is True
    assert all(p["passed"] for p in report["planted_positives"])
    assert len(report["known_answer"]) == len(mex7_model.CELLS)


def test_dev_stage_end_to_end_is_labelled_development(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    res = json.loads((tmp_path / "ME_X7_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert res["label"] == "DEVELOPMENT"
    assert len(res["instances"]) == len(mex7_model.CELLS)
    analysis = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    assert analysis["label"] == "DEVELOPMENT"
    assert "DEVELOPMENT split: not protected evidence" in (
        tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.md"
    ).read_text()


def test_dev_stage_refuses_more_than_forty_instances(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, 3) == 2


def test_every_gate_reports_the_number_of_instances_it_evaluated(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    gates = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    for name, g in gates.items():
        if name in ("ROUTE", "COST"):
            continue
        assert "n_evaluated" in g, name
        assert isinstance(g["n_evaluated"], int), name
    for name, c in gates["G5_SUFFICIENCY"]["conjuncts"].items():
        assert isinstance(c["n_evaluated"], int), name
    # the cross-cut whose locus may be absent from a small split must say so
    cc = gates["WITNESS_SELF_CONTAINMENT_CROSSCUT"]
    assert cc["status"].startswith("CANNOT_CHECK") or cc["n_evaluated"] > 0


def test_analyze_fires_the_federation_ahead_gate_on_a_planted_m_degradation(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    rp = tmp_path / "ME_X7_DEVELOPMENT_RESULTS_V1.json"
    cp = tmp_path / "ME_X7_DEVELOPMENT_EXPECTED_CUSTODY_V1.json"
    res = json.loads(rp.read_text())
    for rec in res["instances"]:
        rec["arms"][mex7_run.M_ARM] = {
            "verdict": mex7_model.ACCEPT, "detected_class": None, "checks_run": 11, "export_units": 40
        }
    rp.write_text(json.dumps(res))
    assert mex7_run.stage_analyze(rp, cp, tmp_path, "DEVELOPMENT") == 0
    g = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    assert g["G1c_B5_AHEAD"]["pass"] is True
    assert g["G1a_B5_REPRODUCES_M"]["pass"] is False
    assert g["ROUTE"]["witness_terminal"] == "WITNESS_INSUFFICIENT_PARENT_AHEAD"
    assert g["G5_SUFFICIENCY"]["conjuncts"]["S4_FALSE_ACCEPTANCE_NONINFERIORITY"]["pass"] is False


def test_analyze_on_the_unmodified_null_reaches_the_registered_expectation(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    g = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    assert g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] is True
    assert g["G0c_NULL_CALIBRATION"]["pass"] is True
    assert g["G1b_M_ADVANTAGE"]["pass"] is False
    assert g["G1c_B5_AHEAD"]["pass"] is False
    assert g["ROUTE"]["route"] == "PARENT_SUFFICIENT"


def test_protected_stage_refuses_without_authorization(tmp_path: Path, monkeypatch) -> None:
    assert not mex7_run.AUTH_FILE.exists(), "an authorization file must not be committed"
    assert mex7_run.stage_protected(tmp_path, 1, tmp_path / "absent-seed.txt") == 3
    auth = tmp_path / "PROTECTED_RUN_AUTHORIZATION.json"
    monkeypatch.setattr(mex7_run, "AUTH_FILE", auth)
    auth.write_text(json.dumps({"human_written": True, "human_written_token": "short"}))
    assert mex7_run.stage_protected(tmp_path, 1, tmp_path / "absent-seed.txt") == 3
    auth.write_text(
        json.dumps(
            {
                "human_written": True,
                "human_written_token": "a-sufficiently-long-token",
                "acknowledged_design_sha256": "0" * 64,
            }
        )
    )
    assert mex7_run.stage_protected(tmp_path, 1, tmp_path / "absent-seed.txt") == 3
    auth.write_text(
        json.dumps(
            {
                "human_written": True,
                "human_written_token": "a-sufficiently-long-token",
                "acknowledged_design_sha256": mex7_run.sha256_file(mex7_run.DESIGN_JSON),
            }
        )
    )
    assert mex7_run.stage_protected(tmp_path, 1, tmp_path / "absent-seed.txt") == 4
    bad = tmp_path / "seed.txt"
    bad.write_text("not-the-committed-seed")
    assert mex7_run.stage_protected(tmp_path, 1, bad) == 4


# ---- design freeze -------------------------------------------------------------

def test_design_json_freezes_the_commitment_the_cells_and_the_arm_table() -> None:
    d = json.loads(DESIGN_JSON.read_text())
    assert d["schema_version"] == "orion.v2.me-x7.exact-study-design.v1"
    assert len(d["seed_commitment"]["protected_seed_sha256"]) == 64
    assert d["seed_commitment"]["development_seed_public"] == mex7_run.DEV_SEED
    assert [tuple(c) for c in d["cells"]] == list(mex7_model.CELLS)
    assert d["strata"] == list(mex7_model.STRATA)
    assert d["witness_fields"] == list(mex7_model.FIELDS)
    assert d["checks"] == list(mex7_model.CHECKS)
    assert d["required_fields_per_check"] == {
        k: list(v) for k, v in mex7_model.REQUIRED_FIELDS.items()
    }
    assert d["field_for_class"] == mex7_model.FIELD_FOR_CLASS
    assert [a["name"] for a in d["arms"]] == [s.name for s in mex7_arms.arm_specs()]
    assert d["split_sizes"]["protected_total"] == 50 * len(mex7_model.CELLS)
    assert d["primary_comparator"] == mex7_arms.B5_ARM
    assert d["expected_route"] == "PARENT_SUFFICIENT"
    assert d["not_applicable_cells"] == [["INVALID_CALIBRATION", "MODE_FORMAL"]]


def test_the_non_applicable_cell_is_generated_zero_times() -> None:
    assert ("INVALID_CALIBRATION", "MODE_FORMAL") not in mex7_model.CELLS
    assert mex7_model.cell_applicable("INVALID_CALIBRATION", "MODE_COMPUTATIONAL")
    assert not mex7_model.cell_applicable("INVALID_CALIBRATION", "MODE_FORMAL")
