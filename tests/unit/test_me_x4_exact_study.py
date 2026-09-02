"""ME-X4 exact selective-reopening study: end-to-end tests of every runner
stage on planted-signal and null fixtures. Development fixtures only; nothing
here is protected evidence."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEX4 = ROOT / "research" / "experiments" / "me-x4"
if str(MEX4) not in sys.path:
    sys.path.insert(0, str(MEX4))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, MEX4 / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mex4_model = _load("mex4_model")
mex4_oracle = _load("mex4_oracle")
mex4_generator = _load("mex4_generator")
mex4_parents = _load("mex4_parents")
mex4_arms = _load("mex4_arms")
mex4_run = _load("mex4_run")


# ---- parents: native known-answer tests must pass before use ----------------

def test_every_parent_passes_its_native_known_answer_tests() -> None:
    results = mex4_parents.fidelity_selftests()
    failed = [r for r in results if not r["passed"]]
    assert not failed, failed
    parents = {r["parent"] for r in results}
    assert parents == {"JTMS", "ATMS", "AGM", "NOISY_OR", "ASSURANCE", "PROVENANCE_ONLY"}


# ---- oracle: hand-authored fixtures and exhaustive agreement ------------------

def test_hand_authored_known_answer_fixtures_reproduced_by_oracle() -> None:
    for f in mex4_generator.known_answer_fixtures():
        w = f["world"]; acc = w.accepted_ids()
        assert mex4_oracle.all_accepted_supported_at_v0(w), f["name"]
        traj = mex4_oracle.expected_trajectory(w, f["events"], acc)
        got = traj[-1].as_dict()
        for k in ("reopened", "preserved", "unresolved"):
            assert got[k] == f["expected"][k], (f["name"], k, got[k], f["expected"][k])
        assert all(t.exhaustive_agrees for t in traj)


def test_oracle_kleene_equals_exhaustive_on_generated_instances() -> None:
    for stratum in mex4_model.STRATA:
        inst, traj = mex4_generator.generate_instance("t", "UNIT-SEED", stratum, 0)
        assert inst.stratum == stratum
        assert all(t.exhaustive_agrees for t in traj)
        assert all(len(t.unknown_atoms) <= mex4_generator.MAX_UNKNOWN_ATOMS for t in traj)
        assert mex4_oracle.all_accepted_supported_at_v0(inst.world_v0)


def test_generator_is_deterministic_and_round_trips_json() -> None:
    a, _ = mex4_generator.generate_instance("t", "UNIT-SEED", "SOURCE_RETRACTED", 1)
    b, _ = mex4_generator.generate_instance("t", "UNIT-SEED", "SOURCE_RETRACTED", 1)
    ja = mex4_model.canonical_json(mex4_model.instance_to_json(a)); jb = mex4_model.canonical_json(mex4_model.instance_to_json(b))
    assert ja == jb
    back = mex4_model.instance_from_json(json.loads(ja))
    assert mex4_model.canonical_json(mex4_model.instance_to_json(back)) == ja
    c, _ = mex4_generator.generate_instance("t", "OTHER-SEED", "SOURCE_RETRACTED", 1)
    assert mex4_model.canonical_json(mex4_model.instance_to_json(c)) != ja


# ---- arms: M and B5 exact on fixtures; separation pair ---------------------------

def _run_arm(name: str, w0, events):
    spec = {s.name: s for s in mex4_arms.arm_specs()}[name]
    r = mex4_arms.ArmRunner(spec, 7); w = w0; hist = []; out = None
    for ev in events:
        w = mex4_model.apply_event(w, ev); hist.append(ev)
        out, _ = r.run_version(mex4_arms.ArmView(w0, w, list(hist), w0.accepted_ids()))
    return out


def test_m_and_b5_exact_on_hand_authored_fixtures() -> None:
    for f in mex4_generator.known_answer_fixtures():
        for arm in (mex4_run.M_ARM, mex4_run.B5_ARM):
            out = _run_arm(arm, f["world"], f["events"])
            got = {"reopened": sorted(c for c, d in out.items() if d == "REOPENED"), "preserved": sorted(c for c, d in out.items() if d == "PRESERVED"), "unresolved": sorted(c for c, d in out.items() if d == "UNRESOLVED")}
            assert got == f["expected"], (f["name"], arm, got)


def test_separation_pair_verdict_only_fails_structure_exchange_succeeds() -> None:
    p, q = mex4_generator.separation_pair()
    v1 = [_run_arm(mex4_run.LADDER[0], c["world"], c["events"]) for c in (p, q)]
    assert v1[0] == v1[1], "verdict-only federation must be blind to the P/Q difference"
    assert v1[0]["c"] != "REOPENED" or v1[1]["c"] != "PRESERVED"
    for arm in (mex4_run.B5_ARM, mex4_run.M_ARM):
        assert _run_arm(arm, p["world"], p["events"])["c"] == "REOPENED"
        assert _run_arm(arm, q["world"], q["events"])["c"] == "PRESERVED"


def test_single_parents_break_where_their_semantics_predict() -> None:
    fx = {f["name"]: f for f in mex4_generator.known_answer_fixtures()}
    # provenance-only over-reopens the redundantly supported claim c0 in KA-01
    out = _run_arm("A0_PROVENANCE_ONLY_INVALIDATION", fx["KA-01-SOURCE_RETRACTED"]["world"], fx["KA-01-SOURCE_RETRACTED"]["events"])
    assert out["c0"] == "REOPENED"
    # untyped JTMS ignores dependence discovery (under-reopens) in KA-02
    out = _run_arm("A1_JTMS_CLASSICAL", fx["KA-02-DEPENDENCE_DISCOVERED"]["world"], fx["KA-02-DEPENDENCE_DISCOVERED"]["events"])
    assert out["c0"] == "PRESERVED"
    # untyped evaluator semantics over-reopens the sibling in KA-05
    out = _run_arm("A1_JTMS_CLASSICAL", fx["KA-05-EVALUATOR_BLIND"]["world"], fx["KA-05-EVALUATOR_BLIND"]["events"])
    assert out["c1"] == "REOPENED"
    # two-valued JTMS cannot express the censored case in KA-11; ATMS can
    out = _run_arm("A1_JTMS_CLASSICAL", fx["KA-11-CANNOT_CHECK_EDGE"]["world"], fx["KA-11-CANNOT_CHECK_EDGE"]["events"])
    assert "UNRESOLVED" not in out.values()
    out = _run_arm("A2_ATMS_CLASSICAL", fx["KA-11-CANNOT_CHECK_EDGE"]["world"], fx["KA-11-CANNOT_CHECK_EDGE"]["events"])
    assert out["c0"] == "UNRESOLVED" and out["c1"] == "PRESERVED"


def test_agm_arm_incision_cuts_rules_not_evidence() -> None:
    f = {x["name"]: x for x in mex4_generator.known_answer_fixtures()}["KA-10-ALL_SUFFICIENT_SUPPORT_FAILED"]
    spec = {s.name: s for s in mex4_arms.arm_specs()}["A3_AGM_KERNEL_CONTRACTION"]
    r = mex4_arms.ArmRunner(spec, 7); w0 = f["world"]; w = w0; hist = []
    for ev in f["events"]:
        w = mex4_model.apply_event(w, ev); hist.append(ev)
        out, _ = r.run_version(mex4_arms.ArmView(w0, w, list(hist), w0.accepted_ids()))
    assert out["c0"] == "REOPENED" and out["c1"] == "REOPENED" and out["c2"] == "PRESERVED"
    kb = r.agm.kb
    assert {"ev:e1", "ev:e2", "ev:e3"} <= kb.atoms, "evidence atoms must survive the Levi revision"
    assert "rule:c0.F1" not in kb.rules and "rule:c0.F2" not in kb.rules, "family rules of the contradicted claim must be cut"
    assert r.agm.present <= kb.atoms


def test_ablation_minus_support_families_over_reopens_partial_failure() -> None:
    f = {x["name"]: x for x in mex4_generator.known_answer_fixtures()}["KA-09-PARTIAL_SUPPORT_FAILURE"]
    assert _run_arm("M_MINUS_SUPPORT_FAMILIES", f["world"], f["events"])["c0"] == "REOPENED"
    assert _run_arm(mex4_run.M_ARM, f["world"], f["events"])["c0"] == "PRESERVED"


# ---- runner stages end-to-end ------------------------------------------------------

def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert mex4_run.main(["selftest", "--out", str(tmp_path)]) == 0
    rep = json.loads((tmp_path / "ME_X4_SELFTEST_REPORT.json").read_text())
    assert rep["passed"] is True
    assert rep["separation"]["passed"] is True
    assert rep["null_calibration"]["pass"] is True
    assert all(k["passed"] for k in rep["known_answer"])


def test_dev_stage_end_to_end_labelled_development(tmp_path: Path) -> None:
    assert mex4_run.main(["dev", "--out", str(tmp_path), "--per-stratum", "1"]) == 0
    res = json.loads((tmp_path / "ME_X4_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert res["label"] == "DEVELOPMENT" and len(res["instances"]) == 12
    assert "expected" not in res["instances"][0]
    ana = json.loads((tmp_path / "ME_X4_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    assert ana["label"] == "DEVELOPMENT"
    assert ana["gates"]["ROUTE"]["route"] in {"PARENT_SUFFICIENT", "ME_X4_RESIDUAL_CANDIDATE", "M_OVER_REOPENS", "CANNOT_CHECK"}
    assert (tmp_path / "ME_X4_DEVELOPMENT_ANALYSIS_V1.md").read_text().startswith("# ME-X4 analysis — DEVELOPMENT")


def test_dev_stage_refuses_more_than_forty_instances(tmp_path: Path) -> None:
    assert mex4_run.main(["dev", "--out", str(tmp_path), "--per-stratum", "4"]) == 2


def test_analyze_stage_on_planted_signal_and_null(tmp_path: Path) -> None:
    pairs = mex4_generator.generate_split("t", "UNIT-ANALYZE", {s: 1 for s in mex4_model.STRATA})
    res, cus = mex4_run.run_instances(pairs, "DEVELOPMENT", "UNIT-ANALYZE")
    rp = tmp_path / "ME_X4_T_RESULTS_V1.json"; cp = tmp_path / "c.json"
    res.pop("_timing_wall_ns", None)
    rp.write_text(json.dumps(res)); cp.write_text(json.dumps(cus))
    assert mex4_run.main(["analyze", "--results", str(rp), "--custody", str(cp), "--out", str(tmp_path)]) == 0
    ana = json.loads((tmp_path / "ME_X4_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    per = ana["score"]["per_arm"]
    # planted signal: M and B5 exact; nulls at floor
    assert per[mex4_run.M_ARM]["instance_exact_rate"] == 1.0
    assert per[mex4_run.B5_ARM]["instance_exact_rate"] == 1.0
    assert per["C_RANDOM_DISPOSITION"]["instance_exact_rate"] <= 0.1
    g = ana["gates"]
    assert g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] and g["G0c_NULL_CALIBRATION"]["pass"]
    assert g["G1a_B5_REPRODUCES_M"]["pass"] is True and g["G1b_M_ADVANTAGE"]["pass"] is False
    assert g["G2_ANTI_CONSERVATISM"]["pass"] is True
    assert g["G3_MECHANISM"]["applicable"] is False
    rates = list(g["G4_INTERFACE_LADDER"]["rung_exact_rates"].values())
    assert rates == sorted(rates), rates
    assert g["ROUTE"]["ladder_terminal"] == "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL"


def test_protected_stage_refuses_without_authorization(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert not mex4_run.AUTH_FILE.exists(), "PROTECTED_RUN_AUTHORIZATION.json must be absent in the repository"
    assert mex4_run.main(["protected", "--out", str(tmp_path)]) == 3
    assert not list(tmp_path.glob("ME_X4_PROTECTED_*"))
    # an authorization file without a human-written token is also refused
    monkeypatch.setattr(mex4_run, "AUTH_FILE", tmp_path / "PROTECTED_RUN_AUTHORIZATION.json")
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": False, "human_written_token": ""}))
    assert mex4_run.main(["protected", "--out", str(tmp_path)]) == 3
    # a well-formed authorization with a seed that does not match the commitment is refused before any generation
    design_sha = mex4_run.sha256_file(mex4_run.DESIGN_JSON)
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps({"human_written": True, "human_written_token": "unit-test-token-not-a-real-authorization", "acknowledged_design_sha256": design_sha}))
    seed = tmp_path / "seed.txt"; seed.write_text("NOT-THE-COMMITTED-SEED\n")
    assert mex4_run.main(["protected", "--out", str(tmp_path), "--seed-file", str(seed)]) == 4
    assert not list(tmp_path.glob("ME_X4_PROTECTED_*"))


def test_design_json_freezes_commitment_and_strata() -> None:
    d = json.loads(mex4_run.DESIGN_JSON.read_text())
    assert d["schema_version"] == "orion.v2.me-x4.exact-study-design.v1"
    assert len(d["seed_commitment"]["protected_seed_sha256"]) == 64
    assert set(d["strata"]) == set(mex4_model.STRATA)
    assert sum(v["protected_n"] for v in d["strata"].values()) == 1200
    assert sum(v["dev_n"] for v in d["strata"].values()) <= 40
    assert set(d["arms"]) == {s.name for s in mex4_arms.arm_specs()}
