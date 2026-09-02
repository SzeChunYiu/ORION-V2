from __future__ import annotations

import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.run_orion_generated_composition_gc2_suite import (
    LADDER, LEVEL_ORDER, DESIGN_PATH, analyze, apply_patch, evaluate, evaluate_one, generate, generate_spec,
    hidden_checks, find_public_examples, normalize_x, oracle, oracle_batch, power_analysis, read_json,
    reference_solution, rooted_patch, exact_two_sided, holm, main,
)

ROOT = Path(__file__).resolve().parents[2]
FAKE_ARM = ROOT / "tests/unit/fixtures_gc2_fake_arm.py"
DESIGN = read_json(DESIGN_PATH)
NONCE = "test-nonce-0123456789abcdef"


def _design(tmp_path: Path, **overrides) -> Path:
    design = json.loads(json.dumps(DESIGN))
    design["protected"]["ladder_level"] = "L2"
    design["protected"]["task_count"] = 3
    design["calibration"]["dev_tasks_per_level"] = 4
    design["power"]["n_grid"] = [8, 16]
    design["power"]["simulations_per_n"] = 30
    for key, value in overrides.items():
        design[key] = value
    path = tmp_path / "design.json"
    path.write_text(json.dumps(design))
    return path


def test_design_is_prospective_and_frozen() -> None:
    assert DESIGN["status"] == "PROSPECTIVE_SECONDARY_ANTI_COPY_PROTOCOL_NO_RESULTS"
    assert DESIGN["arms"] == ["SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"]
    assert DESIGN["difficulty_ladder"]["order"] == list(LEVEL_ORDER)
    assert DESIGN["calibration"]["window"] == [0.3, 0.7]
    assert DESIGN["calibration"]["dev_seed"] != DESIGN["protected"]["seed"]
    assert DESIGN["endpoints"]["primary"]["name"] == "count_robust_hidden_oracle_success"
    assert all(v is False for v in DESIGN["authority"].values())
    for level in LEVEL_ORDER:
        assert DESIGN["difficulty_ladder"][level]["editable_files"] == LADDER[level]["editable_files"]


@pytest.mark.parametrize("level", LEVEL_ORDER)
def test_oracle_precedence_and_ladder_mechanics(level: str) -> None:
    spec = generate_spec(random.Random(3), 0, level)
    labels = spec["labels"]
    valid = spec["primary_authority"]
    # authority before everything, incl. the revoked source from the erratum
    assert oracle({"x": 100, "y": 100, "unit": spec["unit_primary"], "source": "NOPE", "counterexample": True}, spec) == labels["unknown"]
    assert oracle({"x": 1, "y": 1, "unit": spec["unit_primary"], "source": spec["revoked_source"], "counterexample": False}, spec) == labels["unknown"]
    assert spec["revoked_source"] in spec["doc_authorized_sources"] and spec["revoked_source"] not in spec["allowed_sources"]
    # unit contract
    assert normalize_x(3, spec["unit_scaled"], spec) == 3 * spec["scale_factor"]
    assert normalize_x(3, spec["unit_offset"], spec) == 3 * spec["offset_scale"] + spec["offset_shift"]
    assert normalize_x(3, "BAD", spec) is None
    if spec["unit_alias"]:
        assert normalize_x(-2, spec["unit_alias"], spec) == -2 * spec["scale_factor"]
        assert normalize_x(-2, spec["unit_deprecated"], spec) is None
    # counterexample beats thresholds; erratum threshold differs from documented
    assert oracle({"x": 5, "y": 3, "unit": spec["unit_primary"], "source": valid, "counterexample": True}, spec) == labels["review"]
    assert spec["high"] != spec["high_doc"]
    if level == "L3":
        batch = [{"x": 0, "y": 0, "unit": spec["unit_primary"], "source": valid, "counterexample": False}] * 10
        out = oracle_batch(batch, spec)
        assert len(out) == 10 and out.count(labels["accept"]) <= spec["batch_quota"]


@pytest.mark.parametrize("level", LEVEL_ORDER)
def test_hidden_checks_cover_every_registered_family(level: str) -> None:
    rng = random.Random(11)
    spec = generate_spec(rng, 1, level)
    examples = find_public_examples(rng, spec)
    checks = hidden_checks(rng, spec, examples)
    families = {str(c["family"]).split(":")[0] for c in checks}
    expected = {"regression", "edge_revoked_source", "edge_unknown_unit", "edge_counterexample", "edge_threshold_high_eff",
                "edge_threshold_high_doc_trap", "random", "counterfactual_base", "counterfactual_twin", "surface_trap_revoked_source",
                "surface_trap_modulus_shift", "normalize_contract"}
    if level != "L1":
        expected |= {"edge_alias_unit", "edge_deprecated_alias", "edge_tiebreak_even_y", "edge_ambiguity_primary_authority", "codebook_contract"}
    if level == "L3":
        expected |= {"batch_quota"}
    assert expected <= families
    twins = [c for c in checks if str(c["family"]).startswith("counterfactual_twin")]
    assert len(twins) == LADDER[level]["counterfactual_pairs"]
    assert len(checks) > LADDER[level]["hidden_random"] + 2 * LADDER[level]["counterfactual_pairs"]


@pytest.mark.parametrize("level", LEVEL_ORDER)
def test_generation_selfcheck_custody_and_reference_passes(tmp_path: Path, level: str) -> None:
    workdir = tmp_path / level
    freeze = generate(DESIGN, workdir, level=level, count=2, seed=1, reps=2, arms=["SIMPLE_DIRECT", "F2_ORION_METABOLIC_FULL"],
                      nonce=NONCE, force=False, split="dev")
    assert freeze["private_gold_mounted_to_solver"] is False
    assert NONCE not in json.dumps(freeze)
    assert freeze["nonce_sha256"] and all(row["reference_accuracy"] == 1.0 and row["baseline_accuracy"] < 1.0 for row in freeze["generator_self_check"])
    assert len(list((workdir / "requests" / "SIMPLE_DIRECT").glob("*.json"))) == 4  # 2 tasks x 2 reps
    for task in freeze["tasks"]:
        ws = Path(task["solver_workspace"])
        assert (ws / "solver.py").exists() and (ws / "normalize.py").exists() and (ws / "tests/test_public.py").exists()
        assert ("codebook.py" in task["editable_files"]) == (ws / "codebook.py").exists()
        assert len(list((ws / "sources").glob("*.md"))) == DESIGN["difficulty_ladder"][level]["fragments"]
        text = "\n".join(p.read_text() for p in ws.rglob("*") if p.is_file())
        private = read_json(workdir / "private" / f"{task['task_id']}.json")
        assert '"checks"' not in text and "counterfactual_twin" not in text and '"expected"' not in text
        assert private["spec"]["labels"]["unknown"] not in (ws / "solver.py").read_text() or level == "L1"
    request = read_json(workdir / "requests" / "F2_ORION_METABOLIC_FULL" / "gc2-001-r2.json")
    assert request["rep"] == 2 and "private/gc2-" not in json.dumps(request) and "\"checks\"" not in json.dumps(request) and "expected_from_public_sources" in json.dumps(request)


def test_count_robust_primary_lane_recovers_miscounted_headers_and_fails_closed(tmp_path: Path) -> None:
    workdir = tmp_path / "suite"
    arm = "F2_ORION_METABOLIC_FULL"
    generate(DESIGN, workdir, level="L2", count=1, seed=5, reps=1, arms=[arm], nonce=NONCE, force=False, split="dev")
    private = read_json(workdir / "private" / "gc2-001.json")
    ws = workdir / "public" / "gc2-001"
    patch = rooted_patch(ws, reference_solution(private["spec"]))
    assert patch.count("diff --git") == 3
    bad, n = re.subn(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", lambda m: f"@@ -{m.group(1)},{int(m.group(2)) + 4} +{m.group(3)},{int(m.group(4)) + 9} @@", patch, count=1)
    assert n == 1

    def respond(text: str) -> dict:
        path = workdir / "responses" / arm / "gc2-001-r1.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"status": "COMPLETED_PROPOSAL_ONLY", "proposed_patch_or_artifact": {"type": "unified_diff", "content": text},
                                    "resource_receipt": {"total_tokens_reported_by_cli": 7}}))
        return evaluate_one(workdir, arm, "gc2-001", 1)

    ok = respond(patch)
    assert ok["count_robust_hidden_oracle_success"] and ok["raw_hidden_oracle_success"] and ok["syntax_audit_status"] == "VALID_UNCHANGED"
    assert ok["count_robust_hidden_accuracy"] == 1.0 and ok["count_robust_family_accuracy"]["codebook_contract"] == 1.0
    rec = respond(bad)
    assert rec["raw_patch_apply_success"] is False and rec["raw_hidden_oracle_success"] is False
    assert rec["syntax_audit_status"] == "VALID_AFTER_SYNTAX_ONLY_CANONICALIZATION" and rec["count_robust_hidden_oracle_success"] is True
    # a patch that touches a non-editable file fails closed on both lanes
    leak = patch + "diff --git a/README.md b/README.md\n--- a/README.md\n+++ b/README.md\n@@ -1,1 +1,1 @@\n-# x\n+# y\n"
    closed = respond(leak)
    assert closed["count_robust_hidden_oracle_success"] is False and "editable" in closed["count_robust_patch_apply_error"]
    # semantic damage is NOT repaired by canonicalization
    wrong = patch.replace("+    return None\n", "+    return 0\n", 1)
    assert wrong != patch
    sem = respond(wrong)
    assert sem["count_robust_patch_apply_success"] and not sem["count_robust_hidden_oracle_success"] and sem["count_robust_family_accuracy"]["normalize_contract"] < 1.0
    # garbage artifact
    assert respond("not a diff")["count_robust_hidden_oracle_success"] is False


def test_end_to_end_blinded_calibration_and_protected_analysis_on_fake_arm(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    design_path = _design(tmp_path)
    monkeypatch.setenv("ORION_GC1_ARM_COMMAND", f"{sys.executable} {FAKE_ARM}")
    monkeypatch.setenv("FAKE_ARM_NONCE", NONCE)
    monkeypatch.setenv("FAKE_ARM_SUCCESS_BY_LEVEL", "L1:1.0,L2:0.5,L3:0.0")
    monkeypatch.setenv("PYTHONPATH", str(ROOT / "src"))
    cal_root = tmp_path / "cal"
    assert main(["calibrate", "--design", str(design_path), "--workdir", str(cal_root), "--nonce", NONCE, "--task-count", "6", "--max-concurrency", "2"]) == 0
    receipt = read_json(cal_root / "CALIBRATION_RECEIPT.json")
    assert receipt["decision"] == "WINDOW_HIT" and receipt["selected_level"] == "L2"
    assert [row["level"] for row in receipt["levels"]] == ["L1", "L2"]
    assert receipt["levels"][0]["rate"] == 1.0 and 0.3 <= receipt["levels"][1]["rate"] <= 0.7
    commitment = read_json(cal_root / "L2" / "PRIVATE_ORACLE_COMMITMENT.json")
    restoration = read_json(cal_root / "L2" / "PRIVATE_ORACLE_RESTORATION.json")
    assert commitment["private_directory_removed_before_child_process"] and restoration["hashes_match_commitment"]
    assert "NONCE.json" in commitment["private_files"]

    # protected run: F2 biased above F0 above SIMPLE on the fake arm -> analysis + routing
    monkeypatch.setenv("FAKE_ARM_BIAS_F2_ORION_METABOLIC_FULL", "0.45")
    monkeypatch.setenv("FAKE_ARM_BIAS_F0_PARENT_FEDERATION", "0.1")
    work = tmp_path / "protected"
    assert main(["generate", "--design", str(design_path), "--workdir", str(work), "--nonce", NONCE, "--task-count", "12"]) == 0
    frozen = read_json(work / "FROZEN_TASKS.json")
    assert frozen["ladder_level"] == "L2" and frozen["reps"] == 3 and frozen["split"] == "protected"
    cmd = [sys.executable, str(ROOT / "scripts/dispatch_orion_gc1_blinded.py"), "--workdir", str(work), "--arms", ",".join(DESIGN["arms"]),
           "--max-concurrency", "3", "--runner-script", str(ROOT / "scripts/run_orion_generated_composition_gc2_suite.py")]
    assert subprocess.run(cmd, cwd=str(ROOT), check=False).returncode == 0
    assert not (work / "private").exists() or read_json(work / "PRIVATE_ORACLE_RESTORATION.json")["hashes_match_commitment"]
    assert len(list((work / "responses").rglob("*.json"))) == 12 * 4 * 3
    assert main(["evaluate", "--design", str(design_path), "--workdir", str(work)]) == 0
    assert main(["analyze", "--design", str(design_path), "--workdir", str(work)]) == 0
    analysis = read_json(work / "aggregate" / "analysis.json")
    s = analysis["arm_summaries"]
    assert all(s[a]["cells_evaluated"] == 36 and s[a]["missing_or_unscorable"] == 0 for a in DESIGN["arms"])
    assert s["F2_ORION_METABOLIC_FULL"]["count_robust_hidden_oracle_success"]["task_level_majority_count"] > s["SIMPLE_DIRECT"]["count_robust_hidden_oracle_success"]["task_level_majority_count"]
    fam = [r for r in analysis["contrasts"]["count_robust_hidden_oracle_success"] if not r.get("descriptive_outside_family")]
    assert [r["right_arm"] for r in fam] == ["F0_PARENT_FEDERATION", "SIMPLE_DIRECT", "SAME_MODEL_REFLECTION"]
    assert fam[0]["fixed_sequence_tested"] is True and "holm_p" in fam[0]
    assert analysis["routing"]["route"] in {"POSITIVE_F2_BEATS_PARENT_AND_SIMPLE", "PARTIAL_F2_BEATS_PARENT_NOT_SIMPLE", "NEGATIVE_NO_DETECTABLE_F2_GAIN_AT_MDE"}
    assert (work / "EXECUTION_SUMMARY.md").read_text().startswith("# E70-GC2 execution summary")


def test_calibration_reports_saturation_without_protected_generation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    design_path = _design(tmp_path)
    monkeypatch.setenv("ORION_GC1_ARM_COMMAND", f"{sys.executable} {FAKE_ARM}")
    monkeypatch.setenv("FAKE_ARM_NONCE", NONCE)
    monkeypatch.setenv("FAKE_ARM_SUCCESS_BY_LEVEL", "L1:1.0,L2:1.0,L3:1.0")
    monkeypatch.setenv("PYTHONPATH", str(ROOT / "src"))
    cal_root = tmp_path / "cal"
    assert main(["calibrate", "--design", str(design_path), "--workdir", str(cal_root), "--nonce", NONCE, "--task-count", "3"]) == 0
    receipt = read_json(cal_root / "CALIBRATION_RECEIPT.json")
    assert receipt["decision"] == "SUITE_STILL_SATURATED" and receipt["selected_level"] is None
    assert [row["level"] for row in receipt["levels"]] == ["L1", "L2", "L3"]
    monkeypatch.setenv("FAKE_ARM_SUCCESS_BY_LEVEL", "L1:1.0,L2:0.0,L3:0.0")
    assert main(["calibrate", "--design", str(design_path), "--workdir", str(tmp_path / "cal2"), "--nonce", NONCE, "--task-count", "3"]) == 0
    assert read_json(tmp_path / "cal2" / "CALIBRATION_RECEIPT.json")["decision"] == "LADDER_OVERSHOT_NO_WINDOW_HIT"


def test_routing_and_stats_helpers(tmp_path: Path) -> None:
    assert exact_two_sided(0, 9) == pytest.approx(2 / 512)
    assert exact_two_sided(0, 0) is None
    assert holm([0.01, 0.04, 0.5]) == [0.03, 0.08, 0.5]
    result = power_analysis(seed=1, rd=0.15, alpha=0.05, target_power=0.8, reps=3, control_rate=0.5, concentration=4, n_grid=[8, 200], sims=20)
    assert set(result["power_by_n"]) == {8, 200} and result["power_by_n"][200]["power"] > result["power_by_n"][8]["power"]
    assert result["analytic_mcnemar_n_rep_level_independence_no_reps"] > 100


def test_generate_refuses_unknown_level_and_missing_level(tmp_path: Path) -> None:
    with pytest.raises(Exception):
        generate(DESIGN, tmp_path / "x", level="L9", count=1, seed=1, reps=1, arms=["SIMPLE_DIRECT"], nonce=NONCE, force=False, split="dev")
    design = json.loads(json.dumps(DESIGN))
    design["protected"]["ladder_level"] = None
    design["protected"]["task_count"] = 1
    path = tmp_path / "d.json"
    path.write_text(json.dumps(design))
    with pytest.raises(Exception, match="no ladder level"):
        main(["generate", "--design", str(path), "--workdir", str(tmp_path / "w"), "--nonce", NONCE])
    design["status"] = "RESULTS_PRESENT"
    path.write_text(json.dumps(design))
    with pytest.raises(Exception, match="prospective"):
        main(["generate", "--design", str(path), "--workdir", str(tmp_path / "w2"), "--nonce", NONCE, "--level", "L1"])
