"""ME-X2 V2 revival study: the two registered levers, the V1-provenance gate and
every runner stage. Development fixtures only; nothing here is protected evidence."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEX2 = ROOT / "research" / "experiments" / "me-x2"
MEX2V2 = ROOT / "research" / "experiments" / "me-x2-v2"
for _p in (str(MEX2), str(MEX2V2)):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load(name: str, where: Path):
    spec = importlib.util.spec_from_file_location(name, where / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mex2_model = _load("mex2_model", MEX2)
mex2_catalogue = _load("mex2_catalogue", MEX2)
mex2_oracle = _load("mex2_oracle", MEX2)
mex2_generator = _load("mex2_generator", MEX2)
mex2_parents = _load("mex2_parents", MEX2)
mex2_arms = _load("mex2_arms", MEX2)
mex2_run = _load("mex2_run", MEX2)
mex2v2_provenance = _load("mex2v2_provenance", MEX2V2)
mex2v2_levers = _load("mex2v2_levers", MEX2V2)
mex2v2_arms = _load("mex2v2_arms", MEX2V2)
mex2v2_run = _load("mex2v2_run", MEX2V2)

SPECS = {s.name: s for s in mex2v2_arms.arm_specs()}
M2 = mex2v2_levers.M2_ARM
M_V1 = mex2v2_arms.M_V1_ARM
B5 = mex2v2_arms.B5_ARM


def _run_arm(name: str, inst):
    return mex2_oracle.Environment(inst).run(mex2v2_arms.make_policy(SPECS[name], "unit"))


def _score(name: str, inst, orc) -> dict:
    return mex2_run.score_trajectory(_run_arm(name, inst).as_dict(), orc, mex2_model.instance_to_json(inst))


# ---- G0d: the V1 lane is imported, never edited -------------------------------

def test_v1_lane_is_byte_identical_to_its_published_hashes() -> None:
    r = mex2v2_provenance.check()
    assert r["all_match"] is True, [k for k, v in r["files"].items() if not v["matches"]]
    assert set(r["files"]) >= {"mex2_generator.py", "mex2_oracle.py", "mex2_arms.py", "mex2_parents.py", "mex2_catalogue.py", "mex2_model.py"}


def test_comparator_arms_are_the_frozen_v1_classes_not_reimplementations() -> None:
    frozen = {
        "B0_RETRY_SEARCH": mex2_arms.B0RetrySearch, "B3_MODEL_BASED_DIAGNOSIS_VOI": mex2_arms.B3ModelBasedDiagnosisVoI,
        "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION": mex2_arms.Federation, "B5_R1_VERDICT_ONLY": mex2_arms.B5R1,
        M_V1: mex2_arms.MLocusMinimumEscalation, "C_RANDOM_POLICY": mex2_arms.CRandomPolicy,
        "C_NEVER_INTERVENE": mex2_arms.CNeverIntervene,
    }
    for name, cls in frozen.items():
        assert SPECS[name].factory is cls, name


def test_m2_inherits_every_orion_semantics_method_from_v1_m() -> None:
    """The levers change two orderings; the ORION calls are inherited, not re-rendered."""
    v1 = mex2_arms.MLocusMinimumEscalation
    for meth in ("_receipt", "_dispositions", "_escalate", "_apply", "_disposition_action", "act", "live", "declare", "cannot_identify"):
        assert getattr(mex2v2_levers.M2LookaheadBestHypothesis, meth) is getattr(v1, meth), meth
    src = (MEX2V2 / "mex2v2_levers.py").read_text()
    assert "oracle_targets" not in src and "per_cause_targets" not in src
    assert "import orion_v2" not in src and "from orion_v2" not in src, "the levers must reach ORION only through the inherited V1 code"
    for name in ("assess_discrepancy_locus", "route_frontier_action", "assess_jump", "minimum_level"):
        assert f"{name}(" not in src, f"{name} must be called by the inherited V1 code, not re-called by the levers"


def test_no_v2_module_imports_the_oracle_targets() -> None:
    for f in ("mex2v2_levers.py", "mex2v2_arms.py"):
        src = (MEX2V2 / f).read_text()
        assert "oracle_targets" not in src, f


# ---- the levers ---------------------------------------------------------------

def test_m2_with_both_levers_off_reproduces_v1_m_exactly() -> None:
    """The lookahead key's tail is V1's total order and L2 reduces to V1's rule: with both
    switches off the arm under test is V1's M, trajectory for trajectory."""
    class M2Off(mex2v2_levers.M2LookaheadBestHypothesis):
        lookahead = False
        best_hypothesis_reachability = False

    for stratum in mex2_model.STRATA:
        for inst, _orc in mex2_generator.generate_pair("t", "UNIT-REDUCES", stratum, 0):
            a = mex2_oracle.Environment(inst).run(M2Off("unit")).as_dict()
            b = mex2_oracle.Environment(inst).run(mex2_arms.MLocusMinimumEscalation("unit")).as_dict()
            assert [(s["kind"], s["target"], s["outcome"]) for s in a["steps"]] == [(s["kind"], s["target"], s["outcome"]) for s in b["steps"]], inst.instance_id


def test_lever_caches_do_not_change_the_underlying_predicates() -> None:
    seen: dict = {}

    class Capture(mex2v2_levers.M2LookaheadBestHypothesis):
        def act(self, view):
            seen.setdefault("view", view)
            return super().act(view)

    inst, _orc = mex2_generator.generate_pair("t", "UNIT-CACHE", "MODEL_FAMILY_INADEQUATE", 0)[0]
    pol = Capture("unit")
    mex2_oracle.Environment(inst).run(pol)
    view = seen["view"]
    live = pol.live(view)
    assert pol._est_cache, "the memo must actually be used"
    uncached = mex2_arms.MLocusMinimumEscalation("unit")
    for c in live:
        assert pol._establishable(view, live, c) == mex2_arms.MLocusMinimumEscalation._establishable(uncached, view, live, c), c


def test_l2_is_strictly_more_permissive_than_v1_reachability() -> None:
    """L2 demotes the fail-closed rule to a preference: it never refuses an action V1 admits,
    and on the frozen lever fixtures it admits at least one action V1 refuses."""
    doc = mex2v2_run.lever_fixtures()
    admitted_only_under_l2 = 0
    for fx in doc["fixtures"]:
        inst = mex2_model.instance_from_json(fx["instance"])
        pol = mex2v2_arms.make_policy(SPECS[M2], "unit")
        mex2_oracle.Environment(inst).run(pol)
        admitted_only_under_l2 += sum(1 for r in pol.lever_receipts if r["l2_only_admissible"])
    assert admitted_only_under_l2 >= 1


def test_lever_known_answer_fixtures_reproduce_the_diagnosed_failure_and_its_repair() -> None:
    doc = mex2v2_run.lever_fixtures()
    fixtures = doc["fixtures"]
    assert len(fixtures) == 6 and doc["search_seed_public"] == "ME-X2-V2-FIXTURE-SEARCH-20260902"
    recovered = limits = 0
    for fx in fixtures:
        inst = mex2_model.instance_from_json(fx["instance"])
        orc = mex2_oracle.oracle_targets(inst)
        assert {k: orc[k] for k in fx["expected_oracle"]} == fx["expected_oracle"], fx["name"]
        assert orc["exhaustive_agrees"], fx["name"]
        s_v1 = _score(M_V1, inst, orc)
        s_m2 = _score(M2, inst, orc)
        # every fixture is an instance of the diagnosed V1 signature: a false CANNOT_IDENTIFY
        assert s_v1["false_ci"] and not s_v1["decision_correct"] and not s_v1["false_escalation"], fx["name"]
        if fx["registered_limit"]:
            limits += 1
            assert not s_m2["decision_correct"], f"{fx['name']}: a registered limit was rescued — re-freeze the lane"
        else:
            recovered += 1
            assert s_m2["decision_correct"] and not s_m2["false_escalation"], fx["name"]
    assert (recovered, limits) == (4, 2)


def test_the_two_levers_are_complementary_neither_alone_is_both() -> None:
    """Registered before the protected run: L2 is the recovering lever and L1 the protecting one.
    On the frozen failure-shape fixtures the lookahead alone recovers nothing; on a development
    split the best-hypothesis rule alone loses instances the conjunction keeps."""
    tally = {M2: 0, mex2v2_levers.M2_L1_ARM: 0, mex2v2_levers.M2_L2_ARM: 0}
    for fx in mex2v2_run.lever_fixtures()["fixtures"]:
        inst = mex2_model.instance_from_json(fx["instance"])
        orc = mex2_oracle.oracle_targets(inst)
        for arm in tally:
            tally[arm] += _score(arm, inst, orc)["decision_correct"]
    assert tally[M2] == 4 and tally[mex2v2_levers.M2_L1_ARM] == 0

    protected_by_l1 = 0
    for inst, orc in mex2_generator.generate_split("dev", mex2v2_run.DEV_SEED, {s: 1 for s in mex2_model.STRATA}):
        both = _score(M2, inst, orc)["decision_correct"]
        l2_only = _score(mex2v2_levers.M2_L2_ARM, inst, orc)["decision_correct"]
        assert both or not l2_only, inst.instance_id
        protected_by_l1 += bool(both and not l2_only)
    assert protected_by_l1 >= 1


def test_m2_does_not_over_escalate_on_the_hand_authored_fixtures() -> None:
    for fx in mex2_generator.known_answer_fixtures():
        inst = fx["instance"]; orc = mex2_oracle.oracle_targets(inst)
        s = _score(M2, inst, orc)
        assert s["decision_correct"] and not s["false_escalation"] and not s["spec_damage"], fx["name"]


def test_m2_ablations_break_where_their_omission_predicts() -> None:
    fixtures = mex2_generator.known_answer_fixtures()
    base = sum(_score(M2, f["instance"], mex2_oracle.oracle_targets(f["instance"]))["decision_correct"] for f in fixtures)
    for arm in ("M2_MINUS_LOCUS_DIAGNOSIS", "M2_LOCUS_LABELS_SHUFFLED", "M2_ALWAYS_ESCALATE_WHEN_STUCK", "M2_NEVER_ESCALATE"):
        got = sum(_score(arm, f["instance"], mex2_oracle.oracle_targets(f["instance"]))["decision_correct"] for f in fixtures)
        assert got < base, arm
    esc = sum(_score("M2_ALWAYS_ESCALATE_WHEN_STUCK", f["instance"], mex2_oracle.oracle_targets(f["instance"]))["false_escalation"] for f in fixtures)
    assert esc > 0


# ---- runner stages ------------------------------------------------------------

def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert mex2v2_run.main(["selftest", "--out", str(tmp_path)]) == 0
    rep = json.loads((tmp_path / "ME_X2_V2_SELFTEST_REPORT.json").read_text())
    assert rep["passed"] is True and rep["separation"]["passed"] is True
    assert rep["v1_provenance"]["all_match"] is True
    assert len(rep["known_answer"]) == 14 and all(k["passed"] for k in rep["known_answer"])
    assert len(rep["lever_known_answer"]) == 6 and all(k["passed"] for k in rep["lever_known_answer"])
    assert rep["null_calibration"]["pass"] is True


def test_dev_stage_end_to_end_labelled_development_and_deterministic(tmp_path: Path) -> None:
    assert mex2v2_run.main(["dev", "--out", str(tmp_path), "--pairs-per-stratum", "1"]) == 0
    rp = tmp_path / "ME_X2_V2_DEVELOPMENT_RESULTS_V2.json"
    first = rp.read_bytes()
    res = json.loads(first)
    assert res["label"] == "DEVELOPMENT" and len(res["instances"]) == 24
    assert all("truth" not in r["public"] for r in res["instances"])
    assert set(res["arms"]) == {s.name for s in mex2v2_arms.arm_specs()}
    assert mex2v2_run.main(["dev", "--out", str(tmp_path), "--pairs-per-stratum", "1"]) == 0
    assert rp.read_bytes() == first          # determinism
    ana = json.loads((tmp_path / "ME_X2_V2_DEVELOPMENT_ANALYSIS_V2.json").read_text())
    r = ana["gates"]["ROUTE"]
    assert r["route"] in {"PARENT_SUFFICIENT", "ME_X2_RESIDUAL_CANDIDATE", "M2_OVER_ESCALATES", "QUALITY_COST_TRADEOFF_NO_DOMINANCE", "CANNOT_CHECK"}
    assert r["lever_verdict"] in {"LEVERS_RECOVER_M", "LEVERS_PARTIAL_RECOVERY", "LEVERS_NOT_ATTRIBUTED", "LEVERS_MOVE_THE_FAILURE", "LEVERS_NULL", "LEVERS_HARM"}
    assert set(ana["gates"]) >= {"G0a_KNOWN_ANSWER", "G0b_ORACLE_SELF_AGREEMENT", "G0c_NULL_CALIBRATION", "G0d_V1_PROVENANCE",
                                 "G1a_B5_REPRODUCES_M2", "G1b_M2_ADVANTAGE", "G1c_B5_ADVANTAGE", "G2_ANTI_ESCALATION",
                                 "G3_MEDIATION", "G4_INTERFACE_LADDER", "G5_LEVER_ATTRIBUTION", "COST"}
    assert (tmp_path / "ME_X2_V2_DEVELOPMENT_ANALYSIS_V2.md").read_text().startswith("# ME-X2 V2 revival analysis — DEVELOPMENT")


def test_dev_stage_refuses_more_than_the_cap(tmp_path: Path) -> None:
    assert mex2v2_run.main(["dev", "--out", str(tmp_path), "--pairs-per-stratum", "3"]) == 2


def test_lever_receipts_count_only_executed_actions() -> None:
    """V1's inherited act() consults the discriminator ranking before its unique / common-fix
    branches, so a receipt can describe an action M2 never took. Attribution must not count those,
    and the filter is not inert: it removes real receipts on the registered public surfaces."""
    considered = executed = 0
    for inst, _orc in mex2_generator.generate_split("fixture", "ME-X2-V2-FIXTURE-SEARCH-20260902", {s: 6 for s in mex2_model.STRATA}):
        pol = mex2v2_arms.make_policy(SPECS[M2], "unit")
        traj = mex2_oracle.Environment(inst).run(pol).as_dict()
        for r in pol.lever_receipts:
            step = traj["steps"][r["step"]] if r["step"] < len(traj["steps"]) else None
            if step and step["kind"] == r["kind"] and step["target"] == r["action"]:
                executed += 1
            else:
                considered += 1
    assert considered >= 1, "the executed-only filter would be inert — say so rather than shipping a no-op"
    assert executed > considered


def test_gates_read_the_arm_under_test_not_v1s_m(tmp_path: Path) -> None:
    pairs = mex2_generator.generate_split("t", "UNIT-GATES", {s: 1 for s in mex2_model.STRATA})
    res, cus = mex2v2_run.run_instances(pairs, "DEVELOPMENT", "UNIT-GATES")
    res.pop("_timing_wall_ns", None)
    sc = mex2v2_run.score_v2(res, cus)
    assert "swap_null_M" not in sc and len(sc["swap_null_M2"]) == len(pairs)
    g = mex2v2_run.gates_v2(sc, res, True, "DEVELOPMENT")
    assert g["G0c_NULL_CALIBRATION"]["M2_decision_rate"] == pytest.approx(sum(r["decision_correct"] for r in sc["_rows"][M2]) / len(pairs))
    assert g["G2_ANTI_ESCALATION"]["M_V1_false_escalation"] == sc["per_arm"][M_V1]["false_escalation"]
    assert g["G5_LEVER_ATTRIBUTION"]["a_paired_M2_vs_M_V1"]["n"] == len(pairs)
    assert {"executed_steps", "considered_not_executed"} <= set(sc["lever_activity"][0])


def test_g0d_failure_routes_cannot_check(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pairs = mex2_generator.generate_split("t", "UNIT-PROV", {s: 1 for s in mex2_model.STRATA})
    res, cus = mex2v2_run.run_instances(pairs, "DEVELOPMENT", "UNIT-PROV")
    res.pop("_timing_wall_ns", None)
    sc = mex2v2_run.score_v2(res, cus)
    bad = {"all_match": False, "files": {"mex2_oracle.py": {"expected_sha256": "0" * 64, "sha256": "1" * 64, "matches": False}}}
    g = mex2v2_run.gates_v2(sc, res, True, "DEVELOPMENT", prov=bad)
    assert g["G0d_V1_PROVENANCE"]["pass"] is False
    assert g["ROUTE"]["route"] == "CANNOT_CHECK"


def test_protected_stage_refuses_without_authorization(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert not (MEX2V2 / "PROTECTED_RUN_AUTHORIZATION.json").exists()
    assert mex2v2_run.main(["protected", "--out", str(tmp_path)]) == 3
    monkeypatch.setattr(mex2v2_run, "AUTH_FILE", tmp_path / "PROTECTED_RUN_AUTHORIZATION.json")
    auth = tmp_path / "PROTECTED_RUN_AUTHORIZATION.json"
    auth.write_text(json.dumps({"human_written": False, "human_written_token": ""}))
    assert mex2v2_run.main(["protected", "--out", str(tmp_path)]) == 3
    auth.write_text(json.dumps({"human_written": True, "human_written_token": "short"}))
    assert mex2v2_run.main(["protected", "--out", str(tmp_path)]) == 3
    tok = "unit-test-token-not-a-real-authorization"
    auth.write_text(json.dumps({"human_written": True, "human_written_token": tok, "acknowledged_design_sha256": "0" * 64}))
    assert mex2v2_run.main(["protected", "--out", str(tmp_path)]) == 3
    auth.write_text(json.dumps({"human_written": True, "human_written_token": tok, "acknowledged_design_sha256": mex2v2_run.sha256_file(mex2v2_run.DESIGN_JSON)}))
    seed = tmp_path / "seed.txt"; seed.write_text("NOT-THE-COMMITTED-SEED\n")
    assert mex2v2_run.main(["protected", "--out", str(tmp_path), "--seed-file", str(seed)]) == 4
    assert mex2v2_run.main(["protected", "--out", str(tmp_path), "--seed-file", str(tmp_path / "absent.txt")]) == 4
    assert not list(tmp_path.glob("ME_X2_V2_PROTECTED_*"))


def test_protected_stage_refuses_when_the_v1_lane_has_moved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mex2v2_run, "AUTH_FILE", tmp_path / "PROTECTED_RUN_AUTHORIZATION.json")
    (tmp_path / "PROTECTED_RUN_AUTHORIZATION.json").write_text(json.dumps(
        {"human_written": True, "human_written_token": "unit-test-token-not-a-real-authorization",
         "acknowledged_design_sha256": mex2v2_run.sha256_file(mex2v2_run.DESIGN_JSON)}))
    monkeypatch.setattr(mex2v2_run.provenance, "check", lambda: {"all_match": False, "files": {}})
    assert mex2v2_run.main(["protected", "--out", str(tmp_path)]) == 5
    assert not list(tmp_path.glob("ME_X2_V2_PROTECTED_*"))


def test_g0scale_probe_excludes_the_v2_arms(tmp_path: Path) -> None:
    assert mex2v2_run.main(["g0scale", "--out", str(tmp_path), "--pairs-per-stratum", "1", "--public-seed", "UNIT-G0SCALE"]) in (0, 1)
    res = json.loads((tmp_path / "ME_X2_V2_G0SCALE_PROBE_V2.json").read_text())
    assert set(res["arms"]) == set(mex2v2_run.G0SCALE_ARMS)
    assert M2 not in res["arms"] and mex2v2_levers.M2_L1_ARM not in res["arms"]
    assert mex2v2_run.main(["g0scale", "--out", str(tmp_path), "--pairs-per-stratum", "1"]) == 2


# ---- the frozen design --------------------------------------------------------

def test_design_json_freezes_the_levers_commitment_arms_and_routing() -> None:
    d = json.loads(mex2v2_run.DESIGN_JSON.read_text())
    assert d["schema_version"] == "orion.v2.me-x2-v2.revival-study-design.v2"
    assert len(d["seed_commitment"]["protected_seed_sha256"]) == 64
    assert d["seed_commitment"]["protected_seed_sha256"] != json.loads((MEX2 / "ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.json").read_text())["seed_commitment"]["protected_seed_sha256"]
    assert d["seed_commitment"]["env_override"].startswith("MEX2V2_PROTECTED_SEED_FILE")
    assert set(d["arms"]) == {s.name for s in mex2v2_arms.arm_specs()}
    assert d["arm_under_test"] == M2 and d["primary_comparator"].startswith(B5)
    assert set(d["levers"]) == {"L1_ONE_STEP_LOOKAHEAD", "L2_BEST_LIVE_HYPOTHESIS_REACHABILITY"}
    assert d["parent_lane"]["v1_frozen_files_sha256"] == mex2v2_provenance.V1_FROZEN_SHA256
    assert d["parent_lane"]["v1_result_is_immutable"] is True
    assert d["strata_and_counts"]["protected_instances"] == 1200
    assert {r["route"] for r in d["routing"]["primary"]} >= {"PARENT_SUFFICIENT", "CANNOT_CHECK", "ME_X2_RESIDUAL_CANDIDATE", "M2_OVER_ESCALATES"}
    assert {r["verdict"] for r in d["routing"]["lever_verdict"]} == {"LEVERS_HARM", "LEVERS_NULL", "LEVERS_MOVE_THE_FAILURE", "LEVERS_NOT_ATTRIBUTED", "LEVERS_PARTIAL_RECOVERY", "LEVERS_RECOVER_M"}


def test_design_markdown_and_json_agree_on_the_commitment_and_seeds() -> None:
    md = (MEX2V2 / "ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.md").read_text()
    d = json.loads(mex2v2_run.DESIGN_JSON.read_text())
    assert d["seed_commitment"]["protected_seed_sha256"] in md
    for seed in ("ME-X2-V2-DEV-20260902", "ME-X2-V2-FIXTURE-SEARCH-20260902", "ME-X2-V2-G0SCALE-PUBLIC-20260902"):
        assert seed in md
    assert mex2v2_run.DEV_SEED == d["seeds"]["development_public"]
    assert "No protected outcome has been generated or inspected" in md


def test_v1_lane_artifacts_are_untouched_and_unread_by_this_lane() -> None:
    """V1's result is immutable. V1's protected run is complete (PR #164), so this lane must not
    write into the V1 directory and must not read V1's protected artifacts: the V2 comparison runs
    on its own committed seed and inherits nothing from V1's outcome."""
    assert not list(MEX2.glob("mex2v2_*")) and not list(MEX2.glob("ME_X2_V2_*"))
    for f in sorted(MEX2V2.glob("*.py")) + sorted(MEX2V2.glob("*.json")) + sorted(MEX2V2.glob("*.md")):
        src = f.read_text()
        assert "ME_X2_PROTECTED" not in src, f"{f.name} references V1's protected artifacts"
        assert "PROTECTED_SEED_V1" not in src and "MEX2_PROTECTED_SEED_FILE" not in src, f.name
    assert mex2v2_provenance.check()["all_match"], "V1's frozen code and design must be byte-identical"
