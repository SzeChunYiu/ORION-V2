"""ME-X1 exact cross-transition coupling study: end-to-end tests of every
runner stage on planted-signal and null fixtures. Development fixtures only;
nothing here is protected evidence."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEX1 = ROOT / "research" / "experiments" / "me-x1"
if str(MEX1) not in sys.path:
    sys.path.insert(0, str(MEX1))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, MEX1 / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mex1_model = _load("mex1_model")
mex1_oracle = _load("mex1_oracle")
mex1_generator = _load("mex1_generator")
mex1_parents = _load("mex1_parents")
mex1_arms = _load("mex1_arms")
mex1_run = _load("mex1_run")

FIXTURES = ROOT / "research" / "experiments" / "ME_X1_X2_DEVELOPMENT_KNOWN_ANSWER_FIXTURES_V1.json"


# ---- parents: native known-answer tests must pass before use ----------------

def test_every_parent_passes_its_native_known_answer_tests() -> None:
    results = mex1_parents.fidelity_selftests()
    failed = [r for r in results if not r["passed"]]
    assert not failed, failed
    assert {r["parent"] for r in results} == {"JTMS", "ASSURANCE", "PROVENANCE", "CONTRACT_BINDING", "REFINEMENT_FIDELITY", "INDEPENDENCE", "TRANSPORT_LICENSE", "COMPARABILITY", "EVALUATOR_COVERAGE", "ATLAS", "AUTHORITY"}


# ---- oracle: the 14 public development fixtures and exhaustive agreement -----

def test_public_development_fixtures_are_reproduced_as_known_answers() -> None:
    public = {c["case_id"]: c for c in json.loads(FIXTURES.read_text())["x1_transition_cases"]}
    bound = {f["case_id"]: f for f in mex1_generator.known_answer_fixtures()}
    assert set(bound) == set(public), "every public X1 fixture must be bound to a registered world"
    for cid, f in bound.items():
        pub = public[cid]
        assert f["expected"] == pub["expected_action"], cid
        assert mex1_oracle.all_accepted_supported_at_v0(f["world"]), cid
        _w, exp = mex1_oracle.expected_for(f["world"], f["events"], f["request"])
        assert exp.action == pub["expected_action"], (cid, exp.action)
        assert exp.action not in pub.get("forbidden_actions", []), cid
        assert exp.exhaustive_agrees, cid
        if "expected_reopened" in f:
            assert list(exp.reopened) == f["expected_reopened"], cid
        if pub.get("preserve_unaffected_commitments"):
            assert set(f["preserved"]).isdisjoint(exp.reopened)


def test_public_fixture_file_invariants_hold() -> None:
    d = json.loads(FIXTURES.read_text())
    allowed = set(d["allowed_transition_actions"])
    assert allowed <= set(mex1_model.ACTIONS)
    for c in d["x1_transition_cases"]:
        assert c["expected_action"] in allowed
    assert any(c["expected_action"] == "DEFER_CANNOT_CHECK" for c in d["x1_transition_cases"])
    assert any(c.get("negative_control") for c in d["x1_transition_cases"])


def test_oracle_walk_equals_exhaustive_on_generated_instances() -> None:
    for family in mex1_model.FAMILIES:
        for i in range(3):   # POSITIVE, NEGATIVE, AMBIGUITY
            inst, exp = mex1_generator.generate_instance("t", "UNIT-SEED", family, i)
            assert inst.family == family and inst.variant == mex1_model.VARIANT_CYCLE[i]
            assert exp.exhaustive_agrees
            assert len(exp.unknown_atoms) <= mex1_generator.MAX_UNKNOWN_ATOMS
            assert mex1_oracle.all_accepted_supported_at_v0(inst.world_v0)
            if inst.variant == "AMBIGUITY" and family != "X1-J_FULLY_WARRANTED":
                assert exp.action == "DEFER_CANNOT_CHECK"
            if inst.variant == "NEGATIVE":
                assert exp.action in ("UPDATE", "PRESERVE")


def test_generator_is_deterministic_and_round_trips_json() -> None:
    a, _ = mex1_generator.generate_instance("t", "UNIT-SEED", "X1-C_HIDDEN_DEPENDENCE", 0)
    b, _ = mex1_generator.generate_instance("t", "UNIT-SEED", "X1-C_HIDDEN_DEPENDENCE", 0)
    ja = mex1_model.canonical_json(mex1_model.instance_to_json(a)); jb = mex1_model.canonical_json(mex1_model.instance_to_json(b))
    assert ja == jb
    back = mex1_model.instance_from_json(json.loads(ja))
    assert mex1_model.canonical_json(mex1_model.instance_to_json(back)) == ja
    c, _ = mex1_generator.generate_instance("t", "OTHER-SEED", "X1-C_HIDDEN_DEPENDENCE", 0)
    assert mex1_model.canonical_json(mex1_model.instance_to_json(c)) != ja


# ---- arms ---------------------------------------------------------------------------

def _run_arm(name: str, w0, events, request):
    return mex1_run._decision_of(name, w0, events, request)


def test_m_and_b5_exact_on_public_fixtures() -> None:
    for f in mex1_generator.known_answer_fixtures():
        _w, exp = mex1_oracle.expected_for(f["world"], f["events"], f["request"])
        for arm in (mex1_run.M_ARM, mex1_run.B5_ARM):
            d = _run_arm(arm, f["world"], f["events"], f["request"])
            assert (d.action, tuple(d.reopened)) == (exp.action, exp.reopened), (f["case_id"], arm, d)


def test_separation_pair_verdict_only_blind_structure_exchange_exact() -> None:
    p, q = mex1_generator.separation_pair()
    v1 = [_run_arm(mex1_run.LADDER[0], c["world"], c["events"], c["request"]) for c in (p, q)]
    assert v1[0] == v1[1], "verdict-only federation must be blind to the P/Q difference"
    for arm in (mex1_run.B5_ARM, mex1_run.M_ARM):
        dp = _run_arm(arm, p["world"], p["events"], p["request"]); dq = _run_arm(arm, q["world"], q["events"], q["request"])
        assert dp.action == "SELECTIVELY_REOPEN" and tuple(dp.reopened) == ("c",)
        assert dq.action == "PRESERVE"


def test_baselines_break_where_their_semantics_predict() -> None:
    fx = {f["case_id"]: f for f in mex1_generator.known_answer_fixtures()}
    run = lambda arm, cid: _run_arm(arm, fx[cid]["world"], fx[cid]["events"], fx[cid]["request"])  # noqa: E731
    assert run("B0_DIRECT", "X1-DEV-001").action == "UPDATE"                       # binding laundered
    assert run("B1_CALIBRATED_ABSTENTION", "X1-DEV-007").action == "DEFER_CANNOT_CHECK"   # unnecessary defer
    assert run("B2_PROVENANCE_PLUS_VERIFIER", "X1-DEV-001").action == "REVALIDATE"  # lineage catches binding
    assert run("B2_PROVENANCE_PLUS_VERIFIER", "X1-DEV-006").action == "REVALIDATE"  # no typed transport vocabulary
    assert run("B3_PARENT_NATIVE_ASSURANCE", "X1-DEV-007").action == "SELECTIVELY_REOPEN"   # AND semantics over-reopens
    assert run("B4_PARENT_MODULES_WITH_SHARED_STATE", "X1-DEV-010").action == "UPDATE"      # authority laundered
    assert run("B4_PARENT_MODULES_WITH_SHARED_STATE", "X1-DEV-012").action == "UPDATE"      # pairwise taken as global
    assert run("B4_PARENT_MODULES_WITH_SHARED_STATE", "X1-DEV-004").action == "SELECTIVELY_REOPEN"


def test_omission_ablations_restore_their_own_family_error() -> None:
    fx = {f["case_id"]: f for f in mex1_generator.known_answer_fixtures()}
    run = lambda arm, cid: _run_arm(arm, fx[cid]["world"], fx[cid]["events"], fx[cid]["request"])  # noqa: E731
    assert run("M_MINUS_PROBLEM_IDENTITY", "X1-DEV-001").action == "UPDATE"
    assert run("M_MINUS_PROBLEM_IDENTITY", "X1-DEV-011").action == "UPDATE"
    assert run("M_MINUS_DEPENDENCE", "X1-DEV-004").action == "PRESERVE"
    assert run("M_MINUS_TRANSPORT", "X1-DEV-006").action == "UPDATE"
    assert run("M_MINUS_SUPPORT_REOPENING", "X1-DEV-007").action == "SELECTIVELY_REOPEN"
    assert run("M_MINUS_EVALUATOR_CONTRACT", "X1-DEV-009").action == "UPDATE"
    assert run("M_MINUS_AUTHORITY", "X1-DEV-010").action == "UPDATE"
    assert run("M_MINUS_UNRESOLVED_TERMINAL", "X1-DEV-012").action == "UPDATE"
    assert run("M_MINUS_MEASUREMENT_COMPARABILITY", "X1-DEV-003").action == "UPDATE"
    # the unaffected fixture stays exact under every ablation
    for abl in ("M_MINUS_PROBLEM_IDENTITY", "M_MINUS_DEPENDENCE", "M_MINUS_TRANSPORT", "M_MINUS_AUTHORITY", "M_MINUS_EVALUATOR_CONTRACT"):
        assert run(abl, "X1-DEV-013").action == "UPDATE"


def test_no_arm_imports_the_oracle() -> None:
    for name in ("mex1_arms", "mex1_parents", "mex1_model"):
        text = (MEX1 / f"{name}.py").read_text()
        assert "import mex1_oracle" not in text and "from mex1_oracle" not in text


# ---- runner stages end-to-end ------------------------------------------------------

def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert mex1_run.main(["selftest", "--out", str(tmp_path)]) == 0
    rep = json.loads((tmp_path / "ME_X1_SELFTEST_REPORT.json").read_text())
    assert rep["passed"] is True
    assert rep["separation"]["passed"] is True and rep["separation"]["verdict_only_identical_on_P_and_Q"]
    assert rep["null_calibration"]["pass"] is True
    assert all(k["passed"] for k in rep["known_answer"]) and len(rep["known_answer"]) == 14


def test_dev_stage_end_to_end_labelled_development(tmp_path: Path) -> None:
    assert mex1_run.main(["dev", "--out", str(tmp_path), "--per-family", "1"]) == 0
    res = json.loads((tmp_path / "ME_X1_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert res["label"] == "DEVELOPMENT" and len(res["instances"]) == 10
    assert "expected" not in res["instances"][0]
    ana = json.loads((tmp_path / "ME_X1_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    assert ana["label"] == "DEVELOPMENT"
    assert ana["gates"]["ROUTE"]["route"] in {"PARENT_SUFFICIENT", "ME_X1_RESIDUAL_CANDIDATE", "M_OVER_CONSERVATIVE", "CANNOT_CHECK"}
    assert (tmp_path / "ME_X1_DEVELOPMENT_ANALYSIS_V1.md").read_text().startswith("# ME-X1 analysis — DEVELOPMENT")
    assert (tmp_path / "ME_X1_DEVELOPMENT_MINIMAL_RECEIPT_V1.json").exists()


def test_dev_stage_refuses_more_than_five_per_family(tmp_path: Path) -> None:
    assert mex1_run.main(["dev", "--out", str(tmp_path), "--per-family", "6"]) == 2


def test_analyze_stage_on_planted_signal_and_null(tmp_path: Path) -> None:
    assert mex1_run.main(["selftest", "--out", str(tmp_path)]) == 0   # G0a source for analyze
    pairs = mex1_generator.generate_split("t", "UNIT-ANALYZE", {f: 2 for f in mex1_model.FAMILIES})
    res, cus = mex1_run.run_instances(pairs, "DEVELOPMENT", "UNIT-ANALYZE")
    rp = tmp_path / "ME_X1_T_RESULTS_V1.json"; cp = tmp_path / "c.json"
    res.pop("_timing_wall_ns", None)
    rp.write_text(json.dumps(res)); cp.write_text(json.dumps(cus))
    assert mex1_run.main(["analyze", "--results", str(rp), "--custody", str(cp), "--out", str(tmp_path)]) == 0
    ana = json.loads((tmp_path / "ME_X1_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    per = ana["score"]["per_arm"]
    assert per[mex1_run.M_ARM]["instance_exact_rate"] == 1.0
    assert per[mex1_run.B5_ARM]["instance_exact_rate"] == 1.0
    assert per["C_RANDOM_ACTION"]["instance_exact_rate"] <= 0.2
    assert per["C_ALWAYS_DEFER"]["unnecessary_defer_rate"] == 1.0
    assert per[mex1_run.M_ARM]["unnecessary_defer_rate"] == 0.0 and per[mex1_run.M_ARM]["warranted_recall"] == 1.0
    g = ana["gates"]
    assert g["G0a_KNOWN_ANSWER"]["pass"] and g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] and g["G0c_NULL_CALIBRATION"]["pass"]
    assert g["G1a_B5_REPRODUCES_M"]["pass"] is True and g["G1b_M_ADVANTAGE"]["pass"] is False
    assert g["G2_ANTI_CONSERVATISM"]["pass"] is True
    assert g["G3_MECHANISM"]["applicable"] is False
    rates = list(g["G4_INTERFACE_LADDER"]["rung_exact_rates"].values())
    assert rates == sorted(rates), rates
    assert g["ROUTE"]["route"] == "PARENT_SUFFICIENT"
    assert g["ROUTE"]["ladder_terminal"] == "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL"


def test_protected_stage_refuses_without_authorization(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert not mex1_run.AUTH_FILE.exists(), "PROTECTED_RUN_AUTHORIZATION.json must be absent in the repository"
    assert mex1_run.main(["protected", "--out", str(tmp_path)]) == 3
    assert not list(tmp_path.glob("ME_X1_PROTECTED_*"))
    monkeypatch.setattr(mex1_run, "AUTH_FILE", tmp_path / "PROTECTED_RUN_AUTHORIZATION.json")
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": False, "human_written_token": ""}))
    assert mex1_run.main(["protected", "--out", str(tmp_path)]) == 3
    design_sha = mex1_run.sha256_file(mex1_run.DESIGN_JSON)
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": True, "human_written_token": "unit-test-token-not-a-real-authorization", "acknowledged_design_sha256": design_sha}))
    seed = tmp_path / "seed.txt"; seed.write_text("NOT-THE-COMMITTED-SEED\n")
    assert mex1_run.main(["protected", "--out", str(tmp_path), "--seed-file", str(seed)]) == 4
    assert not list(tmp_path.glob("ME_X1_PROTECTED_*"))


def test_design_json_freezes_commitment_families_and_arms() -> None:
    d = json.loads(mex1_run.DESIGN_JSON.read_text())
    assert d["schema_version"] == "orion.v2.me-x1.exact-study-design.v1"
    assert len(d["seed_commitment"]["protected_seed_sha256"]) == 64
    assert set(d["families"]) == set(mex1_model.FAMILIES)
    assert sum(v["protected_n"] for v in d["families"].values()) == 1000
    assert all(v["dev_n"] <= 5 for v in d["families"].values())
    assert set(d["arms"]) == {s.name for s in mex1_arms.arm_specs()}
    assert set(d["transition_actions"]) == set(mex1_model.ACTIONS)
    assert set(d["m_minimal_receipt"]["dropped_atom_kinds"]) <= set(mex1_arms.ATOM_KINDS)
