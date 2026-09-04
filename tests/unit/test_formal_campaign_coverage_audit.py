"""Coverage/constructibility auditor for formal-discovery campaigns.

Guards the R2 defect: a uniform hardcoded arm set silently overrode the plan's
per-study arm lists, and the receipt published a rate over the executed subset
("8,560/8,560 valid") with the registered denominator absent.

Every clause here is tested in BOTH directions - it must be able to fire, and it
must be able to stay quiet - because a checker that can only fire is as useless as
one that can only stay silent, and a gate whose clauses are jointly unsatisfiable
terminates on vocabulary rather than on evidence.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDITOR = ROOT / "scripts/audit_formal_campaign_coverage.py"
SUITE = ROOT / "scripts/run_formal_discovery_generated_suite.py"
ARMS = ROOT / "scripts/orion_formal_discovery_arms.py"
PLAN = ROOT / "research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json"
ROLLUP = ROOT / "research/experiments/fmfg-r2/rollup-r2"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_plan(tmp_path: Path, studies: dict) -> Path:
    path = tmp_path / "plan.json"
    path.write_text(json.dumps({"seed": 1, "studies": studies}))
    return path


def write_summary(tmp_path: Path, name: str, arms: dict[str, tuple[int, int]]) -> Path:
    """arms: arm_id -> (tasks, missing_or_invalid)."""
    path = tmp_path / name
    path.write_text(json.dumps({
        "summary": {
            arm: {"tasks": tasks, "missing_or_invalid": missing,
                  "correct": tasks - missing, "run_valid": missing == 0}
            for arm, (tasks, missing) in arms.items()
        }
    }))
    return path


def run_auditor(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(AUDITOR), *args], capture_output=True, text=True)


# --------------------------------------------------------------------------
# The recorded defect, reproduced from the archived R2 evidence
# --------------------------------------------------------------------------

def test_reproduces_the_r2_registered_scale_shortfall():
    result = run_auditor("--campaign-root", str(ROLLUP))
    assert result.returncode == 2 | 4, result.stdout + result.stderr
    auditor = load(AUDITOR, "auditor")
    report = auditor.audit(
        auditor.load_plan(PLAN),
        auditor.executed_from_summaries(sorted(ROLLUP.rglob("EVALUATION_SUMMARY*.json"))),
        auditor.load_arms_module(),
    )
    three = report["three_numbers"]
    assert three["registered_dispatches"] == 13_168
    assert three["ran_dispatches"] == 8_560
    assert three["valid_dispatches"] == 8_560
    coverage = report["coverage"]
    assert coverage["registered_and_ran_dispatches"] == 3_056
    assert coverage["registered_never_ran_dispatches"] == 10_112
    assert coverage["ran_but_unregistered_dispatches"] == 5_504
    # the arithmetic must close in both directions
    assert coverage["registered_and_ran_dispatches"] + coverage["registered_never_ran_dispatches"] == 13_168
    assert coverage["registered_and_ran_dispatches"] + coverage["ran_but_unregistered_dispatches"] == 8_560
    # the named parent baselines are among the arms that never ran
    never = set(coverage["registered_arm_ids_never_run"])
    assert {"STRUCTURE_MAPPING_PARENT", "ANTI_UNIFICATION_OR_MDL_PARENT_WHEN_APPLICABLE",
            "FCA_PARENT_WHEN_APPLICABLE"} <= never


def test_two_executed_arm_ids_were_registered_for_no_study():
    auditor = load(AUDITOR, "auditor")
    report = auditor.audit(
        auditor.load_plan(PLAN),
        auditor.executed_from_summaries(sorted(ROLLUP.rglob("EVALUATION_SUMMARY*.json"))),
        auditor.load_arms_module(),
    )
    assert report["coverage"]["executed_arm_ids_registered_for_no_study"] == [
        "F2_FORMAL_DISCOVERY_FULL", "F2_STATIC_NO_FORMAL_DISCOVERY",
    ]


# --------------------------------------------------------------------------
# Clause 1: coverage - must fire, and must stay quiet
# --------------------------------------------------------------------------

def test_coverage_clause_fires_on_a_deliberately_wrong_arm_list(tmp_path):
    plan = write_plan(tmp_path, {"S1": {"tasks": 10, "arms": ["A", "B", "C"]}})
    summary = write_summary(tmp_path, "EVALUATION_SUMMARY_s1.json", {"A": (10, 0)})
    result = run_auditor("--plan", str(plan), "--summary", str(summary))
    assert result.returncode & 2, "coverage clause failed to fire on a known shortfall"
    assert "registered, never ran : 20" in result.stdout


def test_coverage_clause_is_quiet_when_the_plan_was_honoured(tmp_path):
    """The no-alarm case. A checker that cries wolf on its first real run gets switched off."""
    plan = write_plan(tmp_path, {"S1": {"tasks": 10, "arms": ["A", "B"]}})
    summary = write_summary(tmp_path, "EVALUATION_SUMMARY_s1.json", {"A": (10, 0), "B": (10, 0)})
    result = run_auditor("--plan", str(plan), "--summary", str(summary))
    assert not (result.returncode & 2), result.stdout
    assert "CLAUSE 1 COVERAGE .......... SATISFIED" in result.stdout
    assert "registered, never ran : 0" in result.stdout


def test_valid_is_reported_separately_from_ran(tmp_path):
    """registered/ran/valid are three numbers; a failed dispatch moves only `valid`."""
    plan = write_plan(tmp_path, {"S1": {"tasks": 10, "arms": ["A", "B"]}})
    summary = write_summary(tmp_path, "EVALUATION_SUMMARY_s1.json", {"A": (10, 0), "B": (10, 4)})
    auditor = load(AUDITOR, "auditor")
    report = auditor.audit(auditor.load_plan(plan),
                           auditor.executed_from_summaries([summary]),
                           auditor.load_arms_module())
    assert report["three_numbers"] == {
        "registered_dispatches": 20, "ran_dispatches": 20, "valid_dispatches": 16,
    }


# --------------------------------------------------------------------------
# Clause 2: constructibility - must fire, and must stay quiet
# --------------------------------------------------------------------------

def test_constructibility_clause_fires_on_the_real_arm_table():
    result = run_auditor("--campaign-root", str(ROLLUP))
    assert result.returncode & 4
    assert "COLLAPSE [PARENT_GENERIC] 6 arms share one instruction" in result.stdout


def test_constructibility_clause_is_quiet_when_every_arm_is_distinct(tmp_path):
    plan = write_plan(tmp_path, {"S1": {"tasks": 4, "arms": ["TARGET_ONLY_DIRECT", "FIXED_LESSON_INJECTION"]}})
    summary = write_summary(tmp_path, "EVALUATION_SUMMARY_s1.json",
                            {"TARGET_ONLY_DIRECT": (4, 0), "FIXED_LESSON_INJECTION": (4, 0)})
    result = run_auditor("--plan", str(plan), "--summary", str(summary))
    assert not (result.returncode & 4), result.stdout
    assert "CLAUSE 2 CONSTRUCTIBILITY .. SATISFIED" in result.stdout


def test_arms_registered_but_never_designed_are_named_not_silently_passed(tmp_path):
    plan = write_plan(tmp_path, {"S1": {"tasks": 4, "arms": ["TARGET_ONLY_DIRECT", "SEMANTIC_RETRIEVAL"]}})
    summary = write_summary(tmp_path, "EVALUATION_SUMMARY_s1.json",
                            {"TARGET_ONLY_DIRECT": (4, 0), "SEMANTIC_RETRIEVAL": (4, 0)})
    result = run_auditor("--plan", str(plan), "--summary", str(summary))
    assert result.returncode & 4
    assert "UNSPECIFIED PROCEDURE: SEMANTIC_RETRIEVAL" in result.stdout


# --------------------------------------------------------------------------
# Reachability: the clauses are separable AND jointly satisfiable
# --------------------------------------------------------------------------

def test_both_clauses_can_be_satisfied_together(tmp_path):
    """The gate must be satisfiable at all, or it terminates on vocabulary."""
    plan = write_plan(tmp_path, {"S1": {"tasks": 4, "arms": ["TARGET_ONLY_DIRECT", "FIXED_LESSON_INJECTION"]}})
    summary = write_summary(tmp_path, "EVALUATION_SUMMARY_s1.json",
                            {"TARGET_ONLY_DIRECT": (4, 0), "FIXED_LESSON_INJECTION": (4, 0)})
    result = run_auditor("--plan", str(plan), "--summary", str(summary))
    assert result.returncode == 0, result.stdout


def test_coverage_can_fail_while_constructibility_passes(tmp_path):
    plan = write_plan(tmp_path, {"S1": {"tasks": 4, "arms": ["TARGET_ONLY_DIRECT", "FIXED_LESSON_INJECTION"]}})
    summary = write_summary(tmp_path, "EVALUATION_SUMMARY_s1.json", {"TARGET_ONLY_DIRECT": (4, 0)})
    assert run_auditor("--plan", str(plan), "--summary", str(summary)).returncode == 2


def test_constructibility_can_fail_while_coverage_passes(tmp_path):
    plan = write_plan(tmp_path, {"S1": {"tasks": 4, "arms": ["TARGET_ONLY_DIRECT", "CURRENT_FORMALISM_ONLY"]}})
    summary = write_summary(tmp_path, "EVALUATION_SUMMARY_s1.json",
                            {"TARGET_ONLY_DIRECT": (4, 0), "CURRENT_FORMALISM_ONLY": (4, 0)})
    assert run_auditor("--plan", str(plan), "--summary", str(summary)).returncode == 4


# --------------------------------------------------------------------------
# "Could not check" is never "checked and fine"
# --------------------------------------------------------------------------

def test_missing_evidence_exits_could_not_check_not_clean(tmp_path):
    plan = write_plan(tmp_path, {"S1": {"tasks": 4, "arms": ["TARGET_ONLY_DIRECT"]}})
    result = run_auditor("--plan", str(plan))
    assert result.returncode == 8
    assert result.returncode not in (0, 2, 4, 6)
    assert "COULD NOT CHECK" in result.stderr


def test_unreadable_plan_exits_could_not_check(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text("{not json")
    assert run_auditor("--plan", str(broken), "--campaign-root", str(ROLLUP)).returncode == 8


def test_absent_campaign_root_exits_could_not_check(tmp_path):
    assert run_auditor("--campaign-root", str(tmp_path / "nope")).returncode == 8


# --------------------------------------------------------------------------
# The runner can no longer inherit an arm set nobody chose
# --------------------------------------------------------------------------

def test_suite_refuses_to_run_without_an_explicit_arm_list():
    for command in ("prepare", "dispatch", "evaluate"):
        result = subprocess.run([sys.executable, str(SUITE), command, "--workdir", "/tmp/unused"],
                                capture_output=True, text=True)
        assert result.returncode != 0
        assert "--arms" in result.stderr


def test_suite_exposes_no_default_arm_constant():
    suite = load(SUITE, "suite")
    assert not hasattr(suite, "DEFAULT_ARMS")


def test_evaluate_publishes_registered_ran_and_valid(tmp_path):
    suite = load(SUITE, "suite")
    workdir = tmp_path / "suite"
    suite.prepare(workdir, ["FM10"], 3, 5, ["A", "B", "C"], False)
    answers = json.loads((workdir / "private_oracle.json").read_text())["answers"]
    for task_id, answer in answers.items():  # only arm A is ever dispatched
        path = workdir / "responses" / "A" / f"{task_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"answer": answer}))
    suite.evaluate(workdir, ["A"])
    coverage = json.loads((workdir / "EVALUATION_SUMMARY.json").read_text())["coverage"]
    assert coverage["registered_dispatches"] == 9
    assert coverage["ran_dispatches"] == 3
    assert coverage["valid_dispatches"] == 3
    assert coverage["registered_never_ran_dispatches"] == 6
    assert coverage["registered_arms_never_run"] == ["B", "C"]
    assert coverage["coverage_complete"] is False


def test_evaluate_denominator_is_the_frozen_list_not_the_executed_one(tmp_path):
    """The R2 shape: N/N valid while two thirds of the registered arms never ran."""
    suite = load(SUITE, "suite")
    workdir = tmp_path / "suite"
    suite.prepare(workdir, ["FM10"], 3, 5, ["A", "B", "C"], False)
    answers = json.loads((workdir / "private_oracle.json").read_text())["answers"]
    for task_id, answer in answers.items():
        path = workdir / "responses" / "A" / f"{task_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"answer": answer}))
    suite.evaluate(workdir, ["A"])
    summary = json.loads((workdir / "EVALUATION_SUMMARY.json").read_text())
    assert summary["summary"]["A"]["run_valid"] is True  # true of what ran ...
    assert summary["coverage"]["coverage_complete"] is False  # ... and no longer the whole story


# --------------------------------------------------------------------------
# Arm construction: loud, and frozen-lane reproducible
# --------------------------------------------------------------------------

def test_unknown_arm_raises_instead_of_returning_a_generic_default():
    arms = load(ARMS, "arms")
    try:
        arms.arm_instruction("TOTALLY_MADE_UP_ARM_ZZZ")
    except arms.UnregisteredArm:
        return
    raise AssertionError("unknown arm id silently produced an instruction")


def test_registered_but_undesigned_arm_raises_its_own_exception():
    arms = load(ARMS, "arms")
    for arm in ("SEMANTIC_RETRIEVAL", "SEMANTIC_RETRIEVAL_OF_EXISTING_FORMALISM",
                "LOCAL_PATCH_OR_EXTRA_VARIABLE"):
        try:
            arms.arm_instruction(arm)
        except arms.UnspecifiedArmProcedure:
            continue
        raise AssertionError(f"{arm} silently produced an instruction")


def test_unconstructible_arms_get_a_status_distinct_from_a_failed_model_call(tmp_path):
    arms_dir = tmp_path / "req"
    arms_dir.mkdir()
    cases = {
        "SEMANTIC_RETRIEVAL": "EXECUTION_FAILED_ARM_PROCEDURE_UNSPECIFIED",
        "TOTALLY_MADE_UP_ARM_ZZZ": "EXECUTION_FAILED_ARM_UNREGISTERED",
    }
    for arm, expected in cases.items():
        request = arms_dir / f"{arm}.json"
        request.write_text(json.dumps({
            "task_id": "t1", "arm_id": arm,
            "task": {"task_id": "t1", "answer_contract": {"x": "str"}},
        }))
        response = arms_dir / f"{arm}.out.json"
        subprocess.run([sys.executable, str(ARMS), "--request", str(request),
                        "--response", str(response)], capture_output=True, text=True)
        status = json.loads(response.read_text())["status"]
        assert status == expected
        assert status != "EXECUTION_FAILED_MODEL_RESPONSE"


def test_every_arm_the_frozen_r2_lane_executed_is_byte_reproducible():
    """The repair must not retro-change the instruction text of the frozen campaign."""
    arms = load(ARMS, "arms")
    expected = {
        "TARGET_ONLY_DIRECT":
            "Solve directly using only the task representation; do not invent extra structure unless logically required.",
        "STRONGEST_DOMAIN_FORMAL_PARENT":
            "Use the strongest applicable native formal parent method first; prefer an exact parent solution and refuse unnecessary new formalism.",
        "F0_PARENT_FEDERATION":
            "Use the strongest applicable native formal parent method first; prefer an exact parent solution and refuse unnecessary new formalism.",
        "F2_STATIC_NO_FORMAL_DISCOVERY":
            "Use the existing integrated ORION concepts but do not perform open-ended transfer discovery, conceptual revision, or formalism genesis.",
        "F2_FORMAL_DISCOVERY_FULL":
            "Use full ORION formal discovery: inspect structural relations, invariants, counterexamples, parent sufficiency, and only invent/revise representation when simpler routes fail.",
    }
    for arm, text in expected.items():
        assert arms.arm_instruction(arm) == text


def test_f0_and_strongest_parent_were_the_same_arm_in_the_frozen_lane():
    """Two of R2's five executed arms shared one instruction - a contrast that could not exist."""
    arms = load(ARMS, "arms")
    assert arms.arm_instruction("F0_PARENT_FEDERATION") == arms.arm_instruction("STRONGEST_DOMAIN_FORMAL_PARENT")
    assert arms.ARM_PROCEDURE_CLASS["F0_PARENT_FEDERATION"] == arms.ARM_PROCEDURE_CLASS["STRONGEST_DOMAIN_FORMAL_PARENT"]


def test_every_arm_in_the_registered_plan_is_present_in_the_arm_table():
    """A registered arm absent from the table would fail only at dispatch, hours in."""
    arms = load(ARMS, "arms")
    plan = json.loads(PLAN.read_text())
    registered = {arm for spec in plan["studies"].values() for arm in spec["arms"]}
    assert registered <= set(arms.ARM_PROCEDURE_CLASS)
