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
