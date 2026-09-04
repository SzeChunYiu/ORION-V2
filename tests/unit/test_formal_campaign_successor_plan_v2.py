"""The successor plan and the pre-registration gate that makes its claim checkable.

PR #269 repaired the harness and deferred two acts to this lane (owner issue #48):
amending the affected receipts, and designing a successor arm set that satisfies
CONSTRUCTIBILITY. These tests pin the second.

The auditor from #269 requires executed evidence, so a *prospective* plan — exactly
what needs auditing before it is frozen — returned COULD NOT CHECK. CONSTRUCTIBILITY
is a property of the plan and the arm table alone; --pre-registration checks it.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDITOR = ROOT / "scripts/audit_formal_campaign_coverage.py"
ARMS = ROOT / "scripts/orion_formal_discovery_arms.py"
PLAN_V1 = ROOT / "research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json"
PLAN_V2 = ROOT / "research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V2.json"
ROLLUP = ROOT / "research/experiments/fmfg-r2/rollup-r2"

EXIT_OK = 0
EXIT_COVERAGE = 2
EXIT_CONSTRUCTIBILITY = 4
EXIT_COULD_NOT_CHECK = 8


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def audit_cli(*args: str):
    completed = subprocess.run([sys.executable, str(AUDITOR), *args], text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return completed.returncode, completed.stdout


def test_pre_registration_passes_the_successor_plan():
    code, out = audit_cli("--pre-registration", "--plan", str(PLAN_V2))
    assert code == EXIT_OK, out
    assert "SATISFIED" in out
    # COVERAGE must never read as a pass when nothing has run.
    assert "NOT APPLICABLE" in out


def test_pre_registration_fails_the_superseded_plan():
    code, out = audit_cli("--pre-registration", "--plan", str(PLAN_V1))
    assert code == EXIT_CONSTRUCTIBILITY, out
    assert "VIOLATED" in out
    for arm in ("STRUCTURE_MAPPING_PARENT", "FCA_PARENT_WHEN_APPLICABLE",
                "ANTI_UNIFICATION_OR_MDL_PARENT_WHEN_APPLICABLE"):
        assert arm in out
    for arm in ("SEMANTIC_RETRIEVAL", "LOCAL_PATCH_OR_EXTRA_VARIABLE"):
        assert arm in out


def test_pre_registration_refuses_evidence_rather_than_ignoring_it(tmp_path):
    """Supplying a run alongside --pre-registration is a request the flag cannot honour."""
    code, out = audit_cli("--pre-registration", "--plan", str(PLAN_V2),
                          "--campaign-root", str(ROLLUP))
    assert code == EXIT_COULD_NOT_CHECK, out


def test_evidence_mode_is_unchanged_by_the_new_flag():
    """The archived R2 evidence must still fire both clauses (exit 6), as CI asserts."""
    code, _ = audit_cli("--campaign-root", str(ROLLUP))
    assert code == EXIT_COVERAGE | EXIT_CONSTRUCTIBILITY
    assert audit_cli()[0] == EXIT_COULD_NOT_CHECK


def test_v2_registers_exactly_one_arm_id_per_procedure_class():
    arms = load(ARMS, "arms")
    v2 = json.loads(PLAN_V2.read_text())
    for name, spec in v2["studies"].items():
        classes = [arms.ARM_PROCEDURE_CLASS[arm] for arm in spec["arms"]]
        assert None not in classes, f"{name} registers an arm with no procedure designed"
        assert len(set(classes)) == len(classes), f"{name} registers two ids for one procedure"
    # Campaign-wide, not merely per study: V1's FM/FG naming split is the same defect.
    every = {arm for spec in v2["studies"].values() for arm in spec["arms"]}
    every_class = [arms.ARM_PROCEDURE_CLASS[arm] for arm in every]
    assert len(set(every_class)) == len(every_class)


def test_v2_keeps_v1s_task_counts_and_defers_rather_than_deletes():
    v1 = json.loads(PLAN_V1.read_text())
    v2 = json.loads(PLAN_V2.read_text())
    assert set(v2["studies"]) == set(v1["studies"])
    assert {k: s["tasks"] for k, s in v2["studies"].items()} == \
           {k: s["tasks"] for k, s in v1["studies"].items()}
    dropped = {a for s in v1["studies"].values() for a in s["arms"]}
    dropped -= {a for s in v2["studies"].values() for a in s["arms"]}
    assert dropped == set(v2["deferred_arms_pending_procedure_design"]), dropped
    assert v2["status"] == "PROSPECTIVE_EXECUTION_PLAN_NO_RESULTS"
    assert v2["owner_issue"] == 48
    assert all(value is False for value in v2["authority"].values())
    assert v2["registered_dispatches"] == \
           sum(s["tasks"] * len(s["arms"]) for s in v2["studies"].values())


def test_the_campaign_orchestrator_prepares_v2_unmodified(tmp_path):
    runner = load(ROOT / "scripts/run_formal_discovery_campaign.py", "campaign")
    plan = json.loads(PLAN_V2.read_text())["studies"]
    root = tmp_path / "campaign"
    runner.prepare(PLAN_V2, root, ["FM50", "FG80"], False)
    manifest = json.loads((root / "CAMPAIGN_FREEZE_MANIFEST.json").read_text())
    rows = {row["study_id"]: row for row in manifest["studies"]}
    for study in ("FM50", "FG80"):
        assert rows[study]["task_count"] == plan[study]["tasks"]
        assert rows[study]["arms"] == plan[study]["arms"]


def test_prepare_exits_cleanly_without_a_campaign_evaluation_summary(tmp_path):
    """main() read CAMPAIGN_EVALUATION_SUMMARY.json for every command, so prepare
    finished its work and then died on a FileNotFoundError traceback."""
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_formal_discovery_campaign.py"), "prepare",
         "--plan", str(PLAN_V2), "--campaign-root", str(tmp_path / "c"), "--studies", "FM50"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    assert completed.returncode == 0, completed.stdout
    assert "Traceback" not in completed.stdout
    assert (tmp_path / "c" / "CAMPAIGN_FREEZE_MANIFEST.json").exists()
