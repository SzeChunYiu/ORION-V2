"""SD70-V2: end-to-end tests of every runner stage on development fixtures.

Nothing here touches a protected seed. The model executable is replaced by
stub processes so that (a) a planted perfect solver reaches the residual
route, (b) a federation-copying solver reaches PARENT_SUFFICIENT, (c) a
failing solver trips the missingness gate, and (d) the physical information
barriers (oracle absent, public pool locked, target-only surface sanitized)
are asserted from inside the child process.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SD = ROOT / "research" / "experiments" / "sd70-v2"
if str(SD) not in sys.path:
    sys.path.insert(0, str(SD))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SD / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


G = _load("sd70v2_generator")
P = _load("sd70v2_parents")
S = _load("sd70v2_stats")
M = _load("sd70v2_model_arm")
R = _load("sd70v2_run")

DEV_SEED = R.dev_seed(0)


# ---- parents ---------------------------------------------------------------

def test_every_parent_passes_native_known_answer_tests() -> None:
    results = P.fidelity_selftests()
    failed = [r for r in results if not r["passed"]]
    assert not failed, failed
    assert len(results) >= 25


def test_v2_generator_family_is_byte_identical_to_v1_public_tasks() -> None:
    spec = importlib.util.spec_from_file_location("v1gen", ROOT / "scripts" / "generate_scientific_development_meta_benchmark.py")
    v1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v1)
    pub1, priv1 = v1.build_suite(12345, 6, 16)
    pub2, priv2 = G.build_suite(12345, 6, 16)
    assert pub1["tasks"] == pub2["tasks"]
    assert [t["correct_action"] for t in priv1["tasks"]] == [t["correct_action"] for t in priv2["tasks"]]
    assert pub2["seed_commitment"] == hashlib.sha256(b"12345").hexdigest()


def test_planted_policy_recoverable_by_strongest_parent_and_not_under_null() -> None:
    pub, priv = G.build_suite(DEV_SEED, 60, 16, task_prefix="t")
    oracle = {t["task_id"]: t for t in priv["tasks"]}
    design = R.load_design()
    sp = design["strongest_generator_faithful_parent"]
    hits = sum(P.select(sp, G.surface_for("COMMON", t, None))[0] == oracle[t["task_id"]]["correct_action"] for t in pub["tasks"])
    chance = sum(t["chance_level"] for t in priv["tasks"]) / 60
    assert hits / 60 >= chance + 0.25, (hits, chance)
    lp_pub, lp_priv = G.label_permutation_controls(pub, priv, DEV_SEED)
    lo = {t["task_id"]: t for t in lp_priv["tasks"]}
    null_hits = sum(P.select(sp, G.surface_for("COMMON", t, None))[0] == lo[t["task_id"]]["correct_action"] for t in lp_pub["tasks"])
    assert null_hits / 60 <= chance + 0.15, (null_hits, chance)
    # controls keep identities aligned
    assert [t["task_id"] for t in lp_pub["tasks"]] == [t["task_id"] for t in lp_priv["tasks"]]
    qs_pub, qs_priv = G.query_shuffle_controls(pub, priv, DEV_SEED)
    assert all(p["correct_action"] in t["candidate_actions"] for t, p in zip(qs_pub["tasks"], qs_priv["tasks"]))
    assert all(set(t["query_context_features"]) <= set(p["latent_feature_tokens"]) for t, p in zip(qs_pub["tasks"], qs_priv["tasks"]))


def test_target_only_surface_carries_no_training_information() -> None:
    pub, _ = G.build_suite(DEV_SEED, 5, 16, task_prefix="t")
    for task in pub["tasks"]:
        surf = G.surface_for("TARGET_ONLY", task, None)
        assert set(surf) == set(G.SURFACE_TARGET_ONLY)
        train_tokens = G.surface_tokens({"training_episodes": task["training_episodes"]})
        train_tokens -= set(task["candidate_actions"]) | set(task["query_context_features"])
        train_tokens -= {"SUCCESS", "FAILURE", "episode_id", "context_features", "chosen_action", "validated_outcome", "resource_cost", "training_episodes"}
        assert not (G.surface_tokens(surf) & train_tokens)
        prompt = M.build_prompt(G.build_request(task["task_id"], "TARGET_ONLY_NEGATIVE_CONTROL", surf))
        assert "TRAINING TRAJECTORIES" not in prompt and "PARENT ADVISORY" not in prompt
        succ = G.surface_for("COMMON_SUCCESS_ONLY", task, None)
        assert all(ep["validated_outcome"] == "SUCCESS" for ep in succ["training_episodes"])
        full = G.surface_for("COMMON_WITH_ADVISORY", task, P.advisory(G.surface_for("COMMON", task, None), "MAXMARGIN_PARENT"))
        assert "PARENT ADVISORY" in M.build_prompt(G.build_request(task["task_id"], "F2_RECURSIVE_META_DISCOVERY_FULL", full))


# ---- stats -----------------------------------------------------------------

def test_stats_known_answers() -> None:
    p, lo, hi = S.wilson(60, 240)
    assert abs(p - 0.25) < 1e-12 and 0.19 < lo < 0.21 and 0.30 < hi < 0.32
    assert abs(S.mcnemar_midp_one_sided(10, 3) - 0.0286865234375) < 1e-12
    assert S.mcnemar_midp_one_sided(0, 0) == 1.0
    assert S.paired_sample_size(0.10, 0.30, 0.025, 0.80) == 234
    assert abs(S.paired_power(240, 0.10, 0.30, 0.025) - 0.811) < 0.005
    h = S.holm({"a": 0.001, "b": 0.06}, alpha=0.05)
    assert h["a"]["reject"] and not h["b"]["reject"]
    d = S.paired_difference([True] * 8 + [False] * 2, [True] * 5 + [False] * 5, bootstrap=500)
    assert d["point"] == pytest.approx(0.3) and d["b"] == 3 and d["c"] == 0


# ---- end-to-end runner ----------------------------------------------------

STUB = '''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
req = json.loads(Path(args["--request"]).read_text())
mode = os.environ["SD70_STUB_MODE"]
workdir = Path(os.environ["SD70_STUB_WORKDIR"])
detail = {"oracle_absent": not (workdir / "private_oracle.json").exists()}
try:
    (workdir / "public_tasks.json").read_bytes()
    detail["public_locked"] = False
except PermissionError:
    detail["public_locked"] = True
try:
    list((workdir / "requests").iterdir())
    detail["requests_locked"] = False
except PermissionError:
    detail["requests_locked"] = True
surface = req["surface"]
detail["surface_keys"] = sorted(surface)
cands = surface["candidate_actions"]
status = "COMPLETED_PROPOSAL_ONLY"
sel = cands[0]
if mode == "fail":
    status = "EXECUTION_FAILED_MODEL_RESPONSE"; sel = None
elif mode == "federation":
    adv = surface.get("parent_advisory")
    sel = adv["federation_selected_action"] if adv else cands[0]
elif mode == "perfect":
    answers = json.loads(Path(os.environ["SD70_STUB_ANSWERS"]).read_text())
    base = req["arm_id"].split("__")[0]
    if base == "F2_STATIC_NO_RECURSION":
        sel = cands[0]
    elif req["task_id"] in answers and base != "TARGET_ONLY_NEGATIVE_CONTROL":
        sel = answers[req["task_id"]]
Path(args["--response"]).write_text(json.dumps({
    "schema_version": "orion.v2.sd70-v2.response.v1", "task_id": req["task_id"], "arm_id": req["arm_id"],
    "status": status, "selected_action": sel, "detail": detail,
    "resource_receipt": {"model_calls": 1, "input_tokens": 100, "output_tokens": 20, "total_tokens": 120, "tool_calls": 0, "wall_time_seconds": 0.01, "executor": "stub"},
}) + "\\n")
'''


def _small_design(tmp: Path) -> Path:
    design = R.load_design()
    design["power"]["task_count"] = 16
    design["controls"]["model_control_subset_size"] = 6
    path = tmp / "design.json"
    path.write_text(json.dumps(design, indent=2, sort_keys=True) + "\n")
    return path


def _run_pipeline(tmp: Path, monkeypatch: pytest.MonkeyPatch, mode: str) -> dict:
    design = _small_design(tmp)
    workdir = tmp / "campaign"
    stub = tmp / "stub.py"
    stub.write_text(STUB)
    monkeypatch.setenv("ORION_SD70V2_MODEL_COMMAND", f"{sys.executable} {stub}")
    monkeypatch.setenv("SD70_STUB_MODE", mode)
    monkeypatch.setenv("SD70_STUB_WORKDIR", str(workdir))
    assert R.main(["prepare", "--workdir", str(workdir), "--seed", str(DEV_SEED), "--design", str(design), "--development"]) == 0
    if mode == "perfect":
        private = json.loads((workdir / "private_oracle.json").read_text())
        answers = {t["task_id"]: t["correct_action"] for t in private["protected"]["tasks"]}
        (tmp / "answers.json").write_text(json.dumps(answers))
        monkeypatch.setenv("SD70_STUB_ANSWERS", str(tmp / "answers.json"))
    private_before = (workdir / "private_oracle.json").read_bytes()
    assert R.main(["dispatch", "--workdir", str(workdir), "--design", str(design), "--max-concurrency", "2"]) == 0
    assert (workdir / "private_oracle.json").read_bytes() == private_before
    assert oct(os.stat(workdir / "public_tasks.json").st_mode & 0o777) != "0o0"
    return {"workdir": workdir, "design": design}


def test_prepare_writes_sanitized_manifests_and_refuses_wrong_protected_seed(tmp_path: Path) -> None:
    design = _small_design(tmp_path)
    with pytest.raises(RuntimeError, match="does not match the committed sha256"):
        R.main(["prepare", "--workdir", str(tmp_path / "x"), "--seed", "42", "--design", str(design)])
    assert R.main(["prepare", "--workdir", str(tmp_path / "c"), "--seed", str(DEV_SEED), "--design", str(design), "--development"]) == 0
    manifest = json.loads((tmp_path / "c" / "REQUEST_SURFACE_MANIFEST.json").read_text())
    arms = manifest["arms"]
    assert arms["TARGET_ONLY_NEGATIVE_CONTROL"]["surface_keys"] == sorted(G.SURFACE_TARGET_ONLY)
    assert arms["TARGET_ONLY_NEGATIVE_CONTROL"]["training_token_leaks_into_target_only"] == 0
    assert arms["TARGET_ONLY_NEGATIVE_CONTROL"]["request_count"] == 6
    assert arms["F2_RECURSIVE_META_DISCOVERY_FULL"]["request_count"] == 16
    assert "parent_advisory" in arms["F2_RECURSIVE_META_DISCOVERY_FULL"]["surface_keys"]
    assert "parent_advisory" not in arms["F2_FULL_MINUS_PARENT_FEDERATION"]["surface_keys"]
    assert arms["F2_RECURSIVE_META_DISCOVERY_FULL__LP"]["request_count"] == 6
    assert arms["STRONGEST_GENERATOR_FAITHFUL_PARENT__QS"]["request_count"] == 16
    req = json.loads(next((tmp_path / "c" / "requests" / "F2_FULL_MINUS_FAILURE_EVIDENCE").glob("*.json")).read_text())
    assert all(ep["validated_outcome"] == "SUCCESS" for ep in req["surface"]["training_episodes"])
    # every request hash in the manifest matches the file on disk
    for arm, meta in arms.items():
        for task_id, digest in meta["request_sha256"].items():
            assert hashlib.sha256((tmp_path / "c" / "requests" / arm / f"{task_id}.json").read_bytes()).hexdigest() == digest
    frozen = json.loads((tmp_path / "c" / "FROZEN_SUITE.json").read_text())
    assert frozen["manifest_sha256"] == manifest["manifest_sha256"]
    assert frozen["development"] is True


def test_pipeline_federation_copy_reaches_parent_sufficient_and_barriers_hold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _run_pipeline(tmp_path, monkeypatch, "federation")
    workdir = ctx["workdir"]
    receipt = json.loads((workdir / "DISPATCH_RECEIPT.json").read_text())
    assert receipt["dispatch_integrity_passed"] and receipt["categories"]["ARM_FAILURE"] == 0
    for resp in (workdir / "responses" / "F2_RECURSIVE_META_DISCOVERY_FULL").glob("*.json"):
        d = json.loads(resp.read_text())["detail"]
        assert d["oracle_absent"] and d["public_locked"] and d["requests_locked"]
        assert "training_episodes" in d["surface_keys"]
    for resp in (workdir / "responses" / "TARGET_ONLY_NEGATIVE_CONTROL").glob("*.json"):
        d = json.loads(resp.read_text())["detail"]
        assert d["surface_keys"] == sorted(G.SURFACE_TARGET_ONLY)
    assert R.main(["evaluate", "--workdir", str(workdir), "--design", str(ctx["design"])]) == 0
    rollup = json.loads((workdir / "SD70_V2_ROLLUP.json").read_text())
    assert rollup["route"] == "PARENT_SUFFICIENT"
    assert rollup["arms"]["F2_RECURSIVE_META_DISCOVERY_FULL"]["exact_accuracy"] == rollup["arms"]["F0_PARENT_FEDERATION"]["exact_accuracy"]
    assert rollup["negative_controls"]["STRONGEST_GENERATOR_FAITHFUL_PARENT__LP"]["behaves"]
    assert rollup["primary_outcomes"]["resource_cost"]["F2_RECURSIVE_META_DISCOVERY_FULL"]["model_calls"] == 16
    assert rollup["primary_outcomes"]["resource_cost"]["STRONGEST_GENERATOR_FAITHFUL_PARENT"]["model_calls"] == 0
    assert (workdir / "SD70_V2_ROLLUP.md").read_text().startswith("# SD70-V2 rollup")
    # resumable: a second dispatch executes nothing new
    assert R.main(["dispatch", "--workdir", str(workdir), "--design", str(ctx["design"])]) == 0
    assert json.loads((workdir / "DISPATCH_RECEIPT.json").read_text())["model_jobs_executed"] == 0
    # design tampering after freeze is refused
    design = json.loads(ctx["design"].read_text())
    design["gates"]["minimum_effect"] = 0.0
    ctx["design"].write_text(json.dumps(design, indent=2, sort_keys=True) + "\n")
    frozen = json.loads((workdir / "FROZEN_SUITE.json").read_text())
    frozen["development"] = False
    (workdir / "FROZEN_SUITE.json").write_text(json.dumps(frozen, indent=2, sort_keys=True) + "\n")
    with pytest.raises(RuntimeError, match="design JSON changed"):
        R.main(["evaluate", "--workdir", str(workdir), "--design", str(ctx["design"])])


def test_pipeline_planted_perfect_solver_reaches_residual_route(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _run_pipeline(tmp_path, monkeypatch, "perfect")
    assert R.main(["evaluate", "--workdir", str(ctx["workdir"]), "--design", str(ctx["design"])]) == 0
    rollup = json.loads((ctx["workdir"] / "SD70_V2_ROLLUP.json").read_text())
    assert rollup["arms"]["F2_RECURSIVE_META_DISCOVERY_FULL"]["exact_accuracy"] == 1.0
    assert rollup["route"] == "PROSPECTIVE_META_POLICY_RESIDUAL", rollup["gates"]
    assert rollup["gates"]["mechanism_recursion"] and rollup["gates"]["model_negative_controls_behave"]
    assert rollup["primary_outcomes"]["holm"]["F2_FULL_vs_SP"]["reject"]


def test_pipeline_failing_solver_is_scored_as_failure_and_trips_cannot_check(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _run_pipeline(tmp_path, monkeypatch, "fail")
    receipt = json.loads((ctx["workdir"] / "DISPATCH_RECEIPT.json").read_text())
    assert receipt["dispatch_integrity_passed"] and receipt["categories"]["ARM_FAILURE"] > 0
    assert R.main(["evaluate", "--workdir", str(ctx["workdir"]), "--design", str(ctx["design"])]) == 0
    rollup = json.loads((ctx["workdir"] / "SD70_V2_ROLLUP.json").read_text())
    assert rollup["route"] == "CANNOT_CHECK"
    assert rollup["arms"]["F2_RECURSIVE_META_DISCOVERY_FULL"]["arm_failure_rate"] == 1.0
    # one bounded rerun is permitted, then the response stays a failure (attempt 2)
    assert R.main(["dispatch", "--workdir", str(ctx["workdir"]), "--design", str(ctx["design"]), "--retry-failed"]) == 0
    resp = json.loads(next((ctx["workdir"] / "responses" / "F2_RECURSIVE_META_DISCOVERY_FULL").glob("*.json")).read_text())
    assert resp["attempt"] == 2
    assert R.main(["dispatch", "--workdir", str(ctx["workdir"]), "--design", str(ctx["design"]), "--retry-failed"]) == 0
    assert json.loads((ctx["workdir"] / "DISPATCH_RECEIPT.json").read_text())["model_jobs_executed"] == 0


def test_evaluate_refuses_missing_response_as_integrity_violation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _run_pipeline(tmp_path, monkeypatch, "federation")
    victim = next((ctx["workdir"] / "responses" / "F2_STATIC_NO_RECURSION").glob("*.json"))
    victim.unlink()
    with pytest.raises(RuntimeError, match="integrity violation"):
        R.main(["evaluate", "--workdir", str(ctx["workdir"]), "--design", str(ctx["design"])])


def test_model_arm_event_parsing_and_procedures() -> None:
    events = "\n".join([
        json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": "ls"}}),
        json.dumps({"type": "turn.completed", "usage": {"input_tokens": 1500, "output_tokens": 300}}),
        "not json",
    ])
    u = M.parse_events(events)
    assert u == {"input_tokens": 1500, "output_tokens": 300, "total_tokens": 1800, "tool_calls": 1, "event_count": 2}
    assert M.base_arm("F2_RECURSIVE_META_DISCOVERY_FULL__LP") == "F2_RECURSIVE_META_DISCOVERY_FULL"
    assert "recursively" in M.ARM_PROCEDURES["F2_RECURSIVE_META_DISCOVERY_FULL"]
    assert "Do NOT recursively" in M.ARM_PROCEDURES["F2_STATIC_NO_RECURSION"]
    with pytest.raises(ValueError):
        M.build_prompt({"arm_id": "UNREGISTERED", "surface": {"instruction": "", "query_context_features": [], "candidate_actions": []}})


def test_design_freeze_matches_commitment_and_development_selection() -> None:
    design = R.load_design()
    dev = json.loads((SD / "results" / "SD70_V2_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert design["strongest_generator_faithful_parent"] == dev["strongest_generator_faithful_parent"]
    assert design["strongest_generator_faithful_parent"] in P.GENERATOR_FAITHFUL_CANDIDATES
    assert design["power"]["task_count"] >= design["power"]["required_tasks"] == S.paired_sample_size(
        design["power"]["minimum_effect"], design["power"]["assumed_discordance"], design["power"]["alpha_one_sided_per_contrast_worst_case"], design["power"]["target_power"])
    assert len(design["seed_commitment"]["seed_sha256"]) == 64
    assert design["protected_outcomes_inspected_at_freeze"] is False
    assert all(v is False for v in design["authority"].values())
