"""E30-R12: power arithmetic, served-model pin, design freeze, analysis end-to-end.

Every check here is a known-answer control: the synthetic campaigns are built so the
expected verdict is derivable by hand, and the no-alarm cases are asserted alongside the
alarm cases so a gate that fires on everything fails the suite.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
R12 = ROOT / "research" / "experiments" / "e30-r12"
ANALYZER = ROOT / "scripts" / "analyze_orion_real_problem_results.py"
ARMS = ["F2_ORION_METABOLIC_FULL", "F0_PARENT_FEDERATION",
        "SAME_MODEL_REFLECTION", "SIMPLE_DIRECT"]
REPS = ["1", "2", "3"]
TASKS = [f"bugsinpy-p{p}-{i}" for p in range(1, 9) for i in range(1, 6)]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


power_note = _load("e30_r12_power_note", R12 / "e30_r12_power_note.py")
analysis = _load("e30_r12_analysis", R12 / "e30_r12_analysis.py")
arms_module = _load("orion_claude_arms_r12", ROOT / "scripts" / "orion_claude_arms.py")


# ------------------------------------------------------------------ power arithmetic
def test_arithmetic_floor_is_seven_discordant_tasks():
    alpha = power_note.holm_first_step_alpha()
    assert alpha == pytest.approx(0.05 / 3)
    assert power_note.min_discordant_for_rejection(alpha) == 7
    # 7 clears it, 6 cannot -- the boundary itself is the claim.
    assert power_note.exact_mcnemar_p(7, 7) <= alpha
    assert power_note.exact_mcnemar_p(6, 6) > alpha


def test_exact_test_matches_hand_computed_values():
    assert power_note.exact_mcnemar_p(0, 0) == 1.0
    assert power_note.exact_mcnemar_p(1, 1) == 1.0            # 2 * 0.5
    assert power_note.exact_mcnemar_p(10, 5) == pytest.approx(1.0)
    assert power_note.exact_mcnemar_p(8, 8) == pytest.approx(2 * 0.5 ** 8)


def test_power_is_calibrated_and_monotone():
    alpha = power_note.holm_first_step_alpha()
    # Under the null the rejection rate must not exceed the nominal level.
    assert power_note.power(40, 0.30, 0.0, alpha) <= alpha
    assert power_note.power(400, 0.30, 0.0, alpha) <= alpha
    # Power rises with n and with the effect.
    small = power_note.power(40, 0.30, 0.20, alpha)
    large = power_note.power(400, 0.30, 0.20, alpha)
    assert 0.0 < small < large <= 1.0
    assert power_note.power(200, 0.30, 0.05, alpha) < power_note.power(200, 0.30, 0.15, alpha)


def test_n40_cannot_detect_the_registered_five_point_mid():
    alpha = power_note.holm_first_step_alpha()
    for psi in (0.10, 0.20, 0.30, 0.40):
        assert power_note.power(40, psi, 0.05, alpha) < 0.05
    # ...and the task count that could is far beyond BugsInPy's pinned pool of 501.
    assert power_note.required_n(0.20, 0.05, alpha) > 501


def test_power_note_payload_is_deterministic_and_matches_the_design():
    first = power_note.build_note()
    assert first == power_note.build_note()
    design = json.loads((R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json").read_text())
    registered = design["power_note"]
    assert registered["arithmetic_floor_at_n40"]["min_all_one_directional_discordant_tasks"] == \
        first["arithmetic_floor"]["min_all_one_directional_discordant_tasks"]
    assert registered["arithmetic_floor_at_n40"]["implied_minimum_observable_risk_difference"] == \
        first["arithmetic_floor"]["implied_minimum_observable_risk_difference"]
    by_psi = {row["psi"]: row for row in registered["mde_at_n40_by_discordance"]}
    for row in first["mde_at_n"]:
        assert by_psi[row["discordance_psi"]]["mde"] == row["mde_risk_difference"]
    need = {row["psi"]: row["n"] for row in registered["tasks_required_for_80pct_power_at_the_registered_5pp_mid"]}
    for row in first["required_n_for_registered_mid"]:
        assert need[row["discordance_psi"]] == row["tasks_for_80pct_power"]


# --------------------------------------------------------------- served-model pin
def test_served_model_assert_accepts_the_pinned_id(monkeypatch):
    monkeypatch.setenv("ORION_ARM_SERVED_MODEL", "glm-5.3")
    arms_module.assert_served_model("glm-5.3")  # must not raise


@pytest.mark.parametrize("served", ["glm-5.2", "glm-5.3-flash", "GLM-5.3", "", "glm-5.30"])
def test_served_model_assert_rejects_every_substitution(monkeypatch, served):
    monkeypatch.setenv("ORION_ARM_SERVED_MODEL", "glm-5.3")
    with pytest.raises(arms_module.ServedModelMismatch):
        arms_module.assert_served_model(served)


def test_served_model_assert_is_inactive_when_unpinned(monkeypatch):
    monkeypatch.delenv("ORION_ARM_SERVED_MODEL", raising=False)
    arms_module.assert_served_model("anything-at-all")


def _request(arm: str = "SIMPLE_DIRECT") -> dict:
    return {"task_id": "t1", "arm_id": arm, "task": {}}


def test_mismatch_propagates_instead_of_becoming_an_envelope(monkeypatch):
    monkeypatch.setenv("ORION_ARM_SERVED_MODEL", "glm-5.3")

    def call(_prompt):
        arms_module.assert_served_model("glm-5.2")
        raise AssertionError("unreachable")

    with pytest.raises(arms_module.ServedModelMismatch):
        arms_module.run_arm(_request(), call=call, workspace_context="{}")


def test_ordinary_failures_still_become_a_failed_envelope():
    def call(_prompt):
        raise ValueError("model did not return a JSON object")

    response = arms_module.run_arm(_request(), call=call, workspace_context="{}")
    assert response["status"] == "EXECUTION_FAILED_MODEL_RESPONSE"
    assert response["resource_receipt"]["served_model_ids"] == []


def test_served_ids_are_recorded_in_the_envelope():
    patch = ("diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n"
             "@@ -1 +1 @@\n-x = 1\n+x = 2\n")
    payload = json.dumps({"patch": patch, "diagnosis": "d", "assumptions": [],
                          "uncertainty": "u", "discriminator_or_tests": [], "falsifier": "f"})

    def call(_prompt):
        return payload, {"input_tokens": 1, "output_tokens": 1, "_served_model": "glm-5.3"}

    response = arms_module.run_arm(_request(), call=call, workspace_context="{}")
    assert response["status"] == "COMPLETED_PROPOSAL_ONLY"
    assert response["resource_receipt"]["served_model_ids"] == ["glm-5.3"]


# ------------------------------------------------------------------- design freeze
def test_design_json_is_structurally_complete():
    design = json.loads((R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json").read_text())
    assert design["status"] == "PROSPECTIVE_REGISTERED_DESIGN_NO_RESULTS"
    assert design["relationship_to_e30_r11"]["r12_may_revise_them"] is False
    assert design["relationship_to_e30_r11"]["e30_r11_endpoints"] == "FROZEN_TERMINAL"
    tasks = design["substrate"]["task_ids"]
    assert len(tasks) == 40 and len(set(tasks)) == 40
    assert sorted(a["arm_id"] for a in design["arms"]) == sorted(ARMS)
    assert design["repetitions"] == 3 and design["expected_responses"] == 480
    assert set(design["endpoints"]) == {"E1_PRIMARY", "E2_CO_PRIMARY", "D1_REGISTERED_DIAGNOSTIC"}
    assert design["statistics"]["multiplicity"]["E1_family"]["size"] == 3
    assert design["statistics"]["multiplicity"]["E2_family"]["size"] == 3
    gates = {g["gate_id"] for g in design["gates"]}
    assert gates == {"GR0a", "GR0b", "GR0c", "GR1", "GR2", "GR3"}
    terminals = " ".join(r["terminal"] for r in design["routing_preregistered"])
    assert "PARENT_SUFFICIENT" in terminals and "NO_ARM_SEPARATION" in terminals
    assert design["authority"]["parent_sufficiency_is_valid_terminal"] is True
    assert design["authority"]["no_arm_separation_is_valid_terminal"] is True
    assert design["routing_precedence"][0] == "LANE_DEFECT"
    assert design["routing_precedence"].index("PARENT_SUFFICIENT") < \
        design["routing_precedence"].index("NO_ARM_SEPARATION")
    assert design["no_rescue_clause"]["a_null_is_a_result"]
    assert design["model_binding"]["frozen_served_model"] == "glm-5.3"


def test_design_task_ids_match_the_e30_r11_frozen_set():
    """R12 must reuse E30-R11's exact 40 ids, projects and per-project counts."""
    design = json.loads((R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json").read_text())
    counts: dict[str, int] = {}
    for task_id in design["substrate"]["task_ids"]:
        counts[task_id.rsplit("-", 1)[0].removeprefix("bugsinpy-")] = \
            counts.get(task_id.rsplit("-", 1)[0].removeprefix("bugsinpy-"), 0) + 1
    assert sorted(counts) == sorted(design["substrate"]["projects"])
    # E30-R11's own correction: ansible carries the sixth task, cookiecutter only four.
    assert counts["ansible"] == 6 and counts["cookiecutter"] == 4
    assert sum(counts.values()) == 40


def test_design_markdown_and_json_agree_on_the_registered_numbers():
    text = (R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.md").read_text()
    for needle in ("0.175", "430", "863", "1287", "1708", "501", "295",
                   "glm-5.3", "0.8167", "PARENT_SUFFICIENT", "NO_ARM_SEPARATION"):
        assert needle in text, needle


# ---------------------------------------------------------------- analysis harness
def _rollup(success_map, critical_map, apply_fail=0.10,
            baseline_status=None, cell="e30r12"):
    """Build a synthetic rollup. ``success_map[arm]`` is the set of tasks it fixes."""
    baseline_status = baseline_status or {}
    evaluations, arm_totals = {}, {}
    for arm in ARMS:
        applied = 0
        for task in TASKS:
            reps = {}
            for rep in REPS:
                native = task in success_map.get(arm, set())
                count = 1 if task in critical_map.get(arm, set()) else 0
                reps[f"r{rep}"] = {
                    "agent_status": "COMPLETED_PROPOSAL_ONLY", "native_success": native,
                    "critical_new_failure_count": count, "critical_new_failure_status": "COUNTED",
                    "patch_apply_returncode": 0, "project": task.rsplit("-", 2)[1],
                }
                applied += 1
            evaluations[f"{arm}/{task}"] = reps
        arm_totals[arm] = {"evaluations": 120, "patch_applied": applied,
                           "patch_apply_failure_rate": apply_fail, "compile_failure_rate": 0.0,
                           "none_reasons": {}, "checkable_rate": 1.0}
    return {"cells": {cell: {
        "arms": ARMS, "reps": REPS, "task_ids": TASKS,
        "task_projects": {t: t.rsplit("-", 2)[1] for t in TASKS},
        "baselines": {t: {"status": baseline_status.get(t, "BASELINE_OK")} for t in TASKS},
        "evaluations": evaluations, "arm_totals": arm_totals}}}


def _campaign(tmp_path: Path, served="glm-5.3", odd_one_out=None) -> Path:
    root = tmp_path / "campaign-e30-r12-test"
    for rep in REPS:
        for arm in ARMS:
            directory = root / "run" / f"confirmatory-r{rep}" / "responses" / arm
            directory.mkdir(parents=True, exist_ok=True)
            for task in TASKS:
                ids = [served]
                if odd_one_out == (rep, arm, task):
                    ids = ["glm-5.2"]
                (directory / f"{task}.json").write_text(json.dumps(
                    {"resource_receipt": {"served_model_ids": ids}}))
    return root


def _gr0(tmp_path: Path, status="PASS") -> Path:
    path = tmp_path / "GR0.json"
    path.write_text(json.dumps({"gr0_status": status, "components": {
        "PC_R6_GR0A_RECEIPT.json": {"status": status},
        "PC_R6_GR0B_RECEIPT.json": {"status": status}}}))
    return path


def _run(tmp_path: Path, rollup: dict, *, campaign: Path, gr0: Path) -> dict:
    rollup_path = tmp_path / "rollup.json"
    rollup_path.write_text(json.dumps(rollup))
    out = tmp_path / "out"
    rc = analysis.main(["--rollup", str(rollup_path), "--gr0", str(gr0),
                        "--campaign", str(campaign), "--analyzer", str(ANALYZER),
                        "--design", str(R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json"),
                        "--out", str(out)])
    assert rc == 0
    return json.loads((out / "E30_R12_ROLLUP_V1.json").read_text())


def test_analysis_refuses_without_a_passing_gr0(tmp_path):
    rollup_path = tmp_path / "rollup.json"
    rollup_path.write_text(json.dumps(_rollup({}, {})))
    rc = analysis.main(["--rollup", str(rollup_path), "--gr0", str(_gr0(tmp_path, "FAIL")),
                        "--campaign", str(_campaign(tmp_path)), "--analyzer", str(ANALYZER),
                        "--design", str(R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json"),
                        "--out", str(tmp_path / "out")])
    assert rc == 3
    assert not (tmp_path / "out" / "E30_R12_ROLLUP_V1.json").exists()


def test_concordant_null_routes_to_parent_sufficient(tmp_path):
    # Every arm fixes the same five tasks: zero discordant pairs anywhere.
    shared = set(TASKS[:5])
    result = _run(tmp_path, _rollup({arm: shared for arm in ARMS}, {}),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["gates"]["GR0c"]["status"] == "PASS"
    assert result["gates"]["GR1"]["status"] == "PASS"
    assert result["gates"]["GR2"]["status"] == "NULL"
    assert result["gates"]["GR3"]["status"] == "PASS"
    # F0 == F2 numerically, so the parent-sufficiency branch is the registered terminal.
    assert result["routing"]["terminal"] == "PARENT_SUFFICIENT"
    for block in result["E1_contrasts"]:
        assert block["discordant_count"] == 0
        assert block["holm_reject"] is False


def test_seven_one_directional_discordant_tasks_reject(tmp_path):
    """The arithmetic floor, exercised end to end rather than only in the note."""
    success = {arm: set() for arm in ARMS}
    success["F2_ORION_METABOLIC_FULL"] = set(TASKS[:7])
    result = _run(tmp_path, _rollup(success, {}),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["gates"]["GR2"]["status"] == "REJECT"
    assert result["gates"]["GR2"]["direction"] == "F2_FAVOURED"
    assert sorted(result["gates"]["GR2"]["rejected_contrasts"]) == sorted(
        ["F0_PARENT_FEDERATION", "SIMPLE_DIRECT", "SAME_MODEL_REFLECTION"])
    assert result["routing"]["terminal"] == "FIRST_REGISTERED_POSITIVE"


def test_six_discordant_tasks_cannot_reject(tmp_path):
    """The no-alarm case at the boundary: one task fewer and nothing may fire."""
    success = {arm: set() for arm in ARMS}
    success["F2_ORION_METABOLIC_FULL"] = set(TASKS[:6])
    result = _run(tmp_path, _rollup(success, {}),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["gates"]["GR2"]["status"] == "NULL"
    assert result["routing"]["terminal"] == "NO_ARM_SEPARATION"


def test_f2_disfavoured_routes_to_harmful(tmp_path):
    success = {arm: set(TASKS[:7]) for arm in ARMS}
    success["F2_ORION_METABOLIC_FULL"] = set()
    result = _run(tmp_path, _rollup(success, {}),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["gates"]["GR2"]["direction"] == "F2_DISFAVOURED"
    assert result["routing"]["terminal"] == "F2_HARMFUL"


def test_critical_regression_is_non_compensatory(tmp_path):
    """F2 wins the primary AND breaks tests: GR3 must dominate the routing."""
    success = {arm: set() for arm in ARMS}
    success["F2_ORION_METABOLIC_FULL"] = set(TASKS[:7])
    critical = {arm: set() for arm in ARMS}
    critical["F2_ORION_METABOLIC_FULL"] = set(TASKS[:20])
    result = _run(tmp_path, _rollup(success, critical),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["gates"]["GR2"]["status"] == "REJECT"
    assert result["gates"]["GR3"]["status"] == "FAIL"
    assert result["routing"]["terminal"] == "CRITICAL_REGRESSION"


def test_high_apply_failure_routes_to_interface_still_broken(tmp_path):
    result = _run(tmp_path, _rollup({}, {}, apply_fail=0.78),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["gates"]["GR1"]["status"] == "FAIL"
    assert result["routing"]["terminal"] == "INTERFACE_STILL_BROKEN"


def test_apply_rate_must_beat_the_pc_r6_comparator_not_only_the_ceiling(tmp_path):
    """0.39 clears the 0.40 ceiling; the comparator condition must still be met."""
    result = _run(tmp_path, _rollup({}, {}, apply_fail=0.39),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["gates"]["GR1"]["status"] == "PASS"
    for arm, item in result["gates"]["GR1"]["per_arm"].items():
        assert item["below_ceiling"] is True and item["below_comparator"] is True


def test_baseline_condition_code_excludes_tasks_from_e2_only(tmp_path):
    statuses = {TASKS[0]: "BASELINE_SUITE_NO_PASSING_TESTS",
                TASKS[1]: "BASELINE_SUITE_NO_PASSING_TESTS"}
    result = _run(tmp_path, _rollup({}, {}, baseline_status=statuses),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["E2_excluded_task_ids"] == sorted(statuses)
    assert result["denominators"]["E1"] == 40
    assert result["denominators"]["E2"] == 38
    for block in result["E2_contrasts"]:
        assert block["checkable_task_count"] == 38
    for block in result["E1_contrasts"]:
        assert block["checkable_task_count"] == 40


def test_served_model_heterogeneity_halts_the_study(tmp_path):
    campaign = _campaign(tmp_path, odd_one_out=("2", "SIMPLE_DIRECT", TASKS[3]))
    result = _run(tmp_path, _rollup({}, {}), campaign=campaign, gr0=_gr0(tmp_path))
    assert result["gates"]["GR0c"]["status"] == "FAIL"
    assert result["gates"]["GR0c"]["offender_count"] == 1
    assert result["routing"]["terminal"] == "LANE_DEFECT"


def test_analysis_is_deterministic(tmp_path):
    rollup = _rollup({"F2_ORION_METABOLIC_FULL": set(TASKS[:9]),
                      "F0_PARENT_FEDERATION": set(TASKS[5:11])}, {})
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    first = _run(tmp_path / "a", rollup, campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    second = _run(tmp_path / "b", rollup, campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    for key in ("E1_contrasts", "E2_contrasts", "per_arm", "gates", "routing"):
        assert first[key] == second[key]


def test_markdown_renders_the_registered_power_boundary(tmp_path):
    rollup_path = tmp_path / "rollup.json"
    rollup_path.write_text(json.dumps(_rollup({}, {})))
    out = tmp_path / "out"
    analysis.main(["--rollup", str(rollup_path), "--gr0", str(_gr0(tmp_path)),
                   "--campaign", str(_campaign(tmp_path)), "--analyzer", str(ANALYZER),
                   "--design", str(R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json"),
                   "--out", str(out)])
    text = (out / "E30_R12_ROLLUP_V1.md").read_text()
    assert "0.175" in text and "NOT evidence of equivalence" in text
    assert "PC-R6 comparator" in text


# ----------------------------------------------------------------- evaluator wrapper
def test_wrapper_registers_the_cell_without_touching_pc_r6_cells(tmp_path):
    wrapper = _load("e30_r12_fullreg_eval", R12 / "e30_r12_fullreg_eval.py")
    pc = wrapper.load_pc_r6(wrapper.DEFAULT_PC_R6_RUNNER)
    campaign = tmp_path / "campaign-e30-r12-xyz"
    campaign.mkdir()
    wrapper.register_cell(pc, campaign)
    assert pc.CELLS["e30r12"]["campaign"] == "campaign-e30-r12-xyz"
    assert pc.CELLS["e30r12"]["arms"] == ARMS
    assert pc.CELLS["e30r12"]["evaluations"] == 480
    # PC-R6's own cells must remain exactly as frozen.
    assert pc.CELLS["e30r11"]["evaluations"] == 480
    assert pc.CELLS["e60"]["evaluations"] == 600


def test_wrapper_requires_the_campaign_argument(capsys):
    wrapper = _load("e30_r12_fullreg_eval", R12 / "e30_r12_fullreg_eval.py")
    assert wrapper.main(["--stage", "rollup", "--out", "/tmp/unused"]) == 2
    assert "--e30r12-campaign is required" in capsys.readouterr().err


# ------------------------------------------------- evaluator wrapper, end to end
# The m5p precedent (and PC-R6's own suite) is that a smoke test skipping main() misses
# exactly the integration defects that cost a campaign.  This drives the wrapper through
# every stage against the synthetic, genuinely executable campaign that
# tests/unit/test_pc_r6_lane.py already knows how to build -- including the gr0b stage,
# whose cell selection goes through the wrapper's name alias and would otherwise fail
# with a bare StopIteration only after 480 model calls had been spent.
pc_r6_test = _load("test_pc_r6_lane_for_r12", Path(__file__).with_name("test_pc_r6_lane.py"))


@pytest.fixture(scope="module")
def r12_campaign(tmp_path_factory):
    base = tmp_path_factory.mktemp("e30_r12_lane")
    campaign = base / "campaign-e30-r12-applyclean-core4-rep3-20260902-deadbeef"
    pc_r6_test.build_campaign(campaign, "e30r12", pc_r6_test.E30_ARMS)
    gold = (campaign / "baseline_lanes" / pc_r6_test.TASK / "BugsInPy" / "projects"
            / pc_r6_test.PROJECT / "bugs" / "1" / "bug_patch.txt")
    gold.parent.mkdir(parents=True)
    gold.write_text(pc_r6_test.PATCHES["good"])
    truth = base / "truth"
    pc_r6_test.build_truth(truth, campaign)
    out = base / "r12-out"
    wrapper = _load("e30_r12_fullreg_eval_e2e", R12 / "e30_r12_fullreg_eval.py")
    common = ["--e30r12-campaign", str(campaign), "--adapter", str(pc_r6_test.ADAPTER),
              "--out", str(out), "--truth-dir", str(truth),
              "--allow-partial-cells", "--date", "20260902"]
    return {"campaign": campaign, "out": out, "common": common, "wrapper": wrapper}


def test_wrapper_list_indices_and_manifest(r12_campaign, capsys):
    wrapper, common, out = (r12_campaign["wrapper"], r12_campaign["common"], r12_campaign["out"])
    assert wrapper.main(["--stage", "list-indices", *common]) == 0
    rows = [line for line in capsys.readouterr().out.splitlines() if line.strip()]
    assert rows and all(row.split("\t")[1] == "e30r12" for row in rows)
    assert wrapper.main(["--stage", "manifest", *common]) == 0
    # The wrapper aliases PC-R6's output names into R12's, so downstream stages and the
    # receipt archive read as an R12 study rather than as a PC-R6 re-run.
    assert (out / "E30_R12_INPUT_MANIFEST.json").is_file()
    manifest = json.loads((out / "E30_R12_INPUT_MANIFEST.json").read_text())
    assert "e30r12" in json.dumps(manifest)


def test_wrapper_rejects_a_tampered_adapter(r12_campaign, tmp_path):
    wrapper, common = r12_campaign["wrapper"], r12_campaign["common"]
    tampered = tmp_path / "adapter.py"
    tampered.write_text(pc_r6_test.ADAPTER.read_text() + "\n# tampered\n")
    argv = [arg for arg in common]
    argv[argv.index("--adapter") + 1] = str(tampered)
    assert wrapper.main(["--stage", "list-indices", *argv]) == 2


def test_wrapper_gr0a_gr0b_gr0_suite_rollup(r12_campaign):
    wrapper, common, out = (r12_campaign["wrapper"], r12_campaign["common"], r12_campaign["out"])
    assert wrapper.main(["--stage", "gr0a", "--execute", "--index", "0", *common]) == 0
    assert wrapper.main(["--stage", "gr0a", *common]) == 0
    gr0a = json.loads((out / "E30_R12_GR0A_RECEIPT.json").read_text())
    # GR0a for R12 is self-consistency: the campaign's own frozen-lane records are truth.
    assert gr0a["status"] == "PASS"
    assert gr0a["cells"]["e30r12"]["comparison"]["bit_exact"] is True
    assert gr0a["checker_validation"]["e30r12"]["pass"] is True

    # gr0b goes through the wrapper's name alias; a StopIteration here would mean the
    # alias silently stopped applying.
    assert wrapper.main(["--stage", "gr0b", *common]) == 0
    assert (out / "E30_R12_GR0B_RECEIPT.json").is_file()
    assert wrapper.main(["--stage", "gr0", *common]) == 0
    assert json.loads((out / "E30_R12_GR0_RECEIPT.json").read_text())["gr0_status"] == "PASS"

    assert wrapper.main(["--stage", "suite", "--index", "0", *common]) == 0
    assert wrapper.main(["--stage", "rollup", *common]) == 0
    rollup = json.loads((out / "E30_R12_FULLREG_RAW_ROLLUP_V1.json").read_text())
    assert "e30r12" in rollup["cells"]
    cell = rollup["cells"]["e30r12"]
    assert cell["arm_totals"], "the rollup must carry per-arm apply/compile totals for D1"
    for totals in cell["arm_totals"].values():
        assert "patch_apply_failure_rate" in totals and "patch_applied" in totals


def test_wrapper_leaves_the_pc_r6_cell_specs_frozen(r12_campaign):
    """A wrapper run must not mutate the archived cells PC-R6's own receipts rest on."""
    wrapper = r12_campaign["wrapper"]
    pc = wrapper.load_pc_r6(wrapper.DEFAULT_PC_R6_RUNNER)
    assert pc.CELLS["e30r11"]["campaign"].startswith("campaign-e30-r11-")
    assert pc.CELLS["e60"]["campaign"].startswith("campaign-e60-r1-")
    assert pc.CELL_ORDER[:2] == ["e30r11", "e60"]


# ------------------------------------------------------- E1 sensitivity denominator
def test_e1_sensitivity_excludes_only_gold_not_applicable_tasks(tmp_path):
    receipt = tmp_path / "gr0b.json"
    receipt.write_text(json.dumps({"status": "PASS", "tasks": [
        {"task_id": "bugsinpy-ansible-1", "gold_control_status": "APPLICABLE"}],
        "not_applicable": [
        {"task_id": "bugsinpy-cookiecutter-1",
         "gold_control_status": "GOLD_NOT_APPLICABLE_MISSING_FIXTURE:tests/x.json"}]}))
    assert analysis.e1_sensitivity_exclusions(receipt) == ["bugsinpy-cookiecutter-1"]
    # No receipt, or a receipt with nothing not-applicable, excludes nothing.
    assert analysis.e1_sensitivity_exclusions(tmp_path / "absent.json") == []
    assert analysis.e1_sensitivity_exclusions(None) == []


def test_e1_sensitivity_contrast_uses_the_reduced_denominator(tmp_path):
    receipt = tmp_path / "gr0b.json"
    receipt.write_text(json.dumps({"not_applicable": [
        {"task_id": TASKS[0], "gold_control_status": "GOLD_NOT_APPLICABLE_MISSING_FIXTURE:x"}]}))
    rollup_path = tmp_path / "rollup.json"
    rollup_path.write_text(json.dumps(_rollup({}, {})))
    out = tmp_path / "out"
    assert analysis.main([
        "--rollup", str(rollup_path), "--gr0", str(_gr0(tmp_path)),
        "--gr0b", str(receipt), "--campaign", str(_campaign(tmp_path)),
        "--analyzer", str(ANALYZER),
        "--design", str(R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json"),
        "--out", str(out)]) == 0
    result = json.loads((out / "E30_R12_ROLLUP_V1.json").read_text())
    assert result["E1_sensitivity_excluded_task_ids"] == [TASKS[0]]
    assert result["denominators"]["E1"] == 40
    assert result["denominators"]["E1_sensitivity"] == 39
    for block in result["E1_contrasts"]:
        assert block["checkable_task_count"] == 40
    for block in result["E1_sensitivity_contrasts"]:
        assert block["checkable_task_count"] == 39


# --------------------------------------------------- dispatch-path guards (sbatch)
SBATCH = R12 / "sbatch"


def test_setup_has_no_silent_source_fallback():
    """A degraded source tree would dispatch pre-#168 arm code while every check passed."""
    text = (SBATCH / "e30_r12_setup.sbatch").read_text()
    assert "cp -a \"$R11/source\"" not in text
    # No swallowed failure anywhere in setup: every guard in this script exists because
    # its failure mode is invisible downstream.
    assert "2>/dev/null" not in text and "|| true" not in text
    assert "SOURCE_SHA_MISMATCH" in text
    for guard in ("IMPORT_PROVENANCE_FAIL", "ARM_EXECUTABLE_PREDATES_PR168",
                  "ARM_EXECUTABLE_LACKS_SERVED_MODEL_PIN", "ADAPTER_SHA_MISMATCH"):
        assert guard in text, guard


def test_setup_asserts_every_reused_request_has_a_readable_workspace():
    text = (SBATCH / "e30_r12_setup.sbatch").read_text()
    assert "solver_workspace" in text and "unreadable_workspaces" in text
    assert "checked == 480" in text


def test_common_pins_pythonpath_to_the_r12_source():
    text = (SBATCH / "e30_r12_common.sh").read_text()
    assert 'export PYTHONPATH="$R12SRC/src' in text
    assert "editable" in text.lower()


def test_agents_gate_on_authorization_and_import_provenance():
    text = (SBATCH / "e30_r12_agents.sbatch").read_text()
    for guard in ("E30_R12_COORDINATOR_AUTHORIZATION.json", "AUTHORIZATION_ABSENT",
                  "AUTHORIZATION_INVALID", "acknowledged_design_sha256",
                  "human_written_token", "verbatim_operator_instruction",
                  "patch_emission"):
        assert guard in text, guard
    # A completed response is never resampled (design section 12, no-rescue clause).
    assert "COMPLETED_PROPOSAL_ONLY" in text and "SKIP" in text


def test_sbatch_scripts_do_not_resolve_their_own_directory():
    """SLURM runs a spool COPY of the script, so `dirname "$0"` points at /var/spool."""
    for path in sorted(SBATCH.glob("*.sbatch")):
        text = path.read_text()
        # The comment explaining why mentions it; what must not appear is the usage.
        assert 'source "$(dirname' not in text, path.name
        assert '$(dirname "$0")/e30_r12_common.sh' not in text, path.name
        assert "e30_r12_common.sh" in text, path.name
        assert 'SBATCH_DIR="${E30R12_SBATCH_DIR:-$R12/source' in text, path.name


def test_suite_and_rollup_refuse_without_a_gr0_pass():
    for name in ("e30_r12_fullreg_suite.sbatch", "e30_r12_fullreg_gr0_verify.sbatch"):
        assert "gr0_status" in (SBATCH / name).read_text(), name


# ------------------------------------------------------- execution-lane contract
def test_json_decoder_tolerates_literal_newlines_in_string_values():
    """E30-R11's campaign-local repair, never upstreamed: 4 of its 13 stuck cells."""
    raw = 'noise {"patch": "line one\nline two", "diagnosis": "d"} trailer'
    value = arms_module._json_object(raw)
    assert value["patch"] == "line one\nline two"
    with pytest.raises(ValueError):
        arms_module._json_object("no object here")


def test_agents_escalate_the_token_budget_only_on_later_passes():
    text = (SBATCH / "e30_r12_agents.sbatch").read_text()
    assert "PRIMARY_BUDGET=${E30R12_PRIMARY_BUDGET:-6000}" in text
    assert "ESCALATED_BUDGET=${E30R12_ESCALATED_BUDGET:-36000}" in text
    assert "ESCALATE_FROM_PASS=${E30R12_ESCALATE_FROM_PASS:-3}" in text


def test_design_registers_the_execution_lane_contract():
    design = json.loads((R12 / "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json").read_text())
    contract = design["execution_lane_contract"]
    assert contract["signature_2_truncation_starved"]["primary_budget"][
        "ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET"] == 6000
    assert contract["signature_2_truncation_starved"]["escalated_budget"][
        "ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET"] == 36000
    assert "NOT resampling" in contract["signature_2_truncation_starved"]["class"]
    assert "strict=False" in contract["signature_1_strict_parse_reject"]["repair"]


def test_agents_halt_the_campaign_on_a_served_model_substitution():
    """One substituted cell must stop the run, not be retried into a mixed dataset."""
    text = (SBATCH / "e30_r12_agents.sbatch").read_text()
    assert "HALT_SERVED_MODEL_MISMATCH" in text
    assert ".served-model-mismatch" in text
    assert 'grep -q "ServedModelMismatch"' in text
    assert "exit 4" in text


# ------------------------------------------------------------- no-imputation checks
def _rollup_with_unapplied(unapplied_tasks, arm="F2_ORION_METABOLIC_FULL"):
    """Real data carries None counts wherever the patch never applied."""
    rollup = _rollup({}, {})
    cell = rollup["cells"]["e30r12"]
    unapplied = 0
    for task in unapplied_tasks:
        for rep in REPS:
            entry = cell["evaluations"][f"{arm}/{task}"][f"r{rep}"]
            entry["critical_new_failure_count"] = None
            entry["critical_new_failure_status"] = "NONE_PATCH_NOT_APPLIED"
            entry["native_success"] = False
            entry["patch_apply_returncode"] = 128
            unapplied += 1
    totals = cell["arm_totals"][arm]
    totals["patch_applied"] = 120 - unapplied
    totals["patch_apply_failure_rate"] = unapplied / 120
    return rollup


def test_unapplied_patches_are_excluded_not_imputed(tmp_path):
    dropped = TASKS[:6]
    result = _run(tmp_path, _rollup_with_unapplied(dropped),
                  campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    arm = result["per_arm"]["F2_ORION_METABOLIC_FULL"]
    # E2 loses exactly those six tasks; nothing is counted as "safe" by default.
    assert arm["E2_tasks_checkable"] == 40 - len(dropped)
    assert arm["D1_patch_applied"] == 120 - 3 * len(dropped)
    assert arm["D1_patch_apply_rate"] == pytest.approx((120 - 18) / 120)
    for block in result["E2_contrasts"]:
        assert block["checkable_task_count"] == 40 - len(dropped)
        assert sorted(block["missing_task_ids"]) == sorted(dropped)
    # E1 keeps them: a non-applying patch is a real, observed failure to fix the test.
    assert arm["E1_tasks_checkable"] == 40


def test_pc_r6_level_apply_failure_reproduces_the_interface_still_broken_terminal(tmp_path):
    """The pre-fix world, as a control: 82% apply failure must not read as a clean run."""
    rollup = _rollup_with_unapplied(TASKS[:33])
    for arm in ARMS:
        rollup["cells"]["e30r12"]["arm_totals"][arm]["patch_apply_failure_rate"] = 0.8167
    result = _run(tmp_path, rollup, campaign=_campaign(tmp_path), gr0=_gr0(tmp_path))
    assert result["gates"]["GR1"]["status"] == "FAIL"
    assert result["routing"]["terminal"] == "INTERFACE_STILL_BROKEN"


def test_rollup_sbatch_passes_the_gr0b_receipt_to_the_analysis():
    """Without it the registered E1 sensitivity denominator would silently exclude nothing."""
    text = (SBATCH / "e30_r12_rollup_and_analysis.sbatch").read_text()
    assert "--gr0b" in text and "PC_R6_GR0B_RECEIPT.json" in text
