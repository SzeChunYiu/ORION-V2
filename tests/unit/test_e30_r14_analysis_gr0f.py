"""GR0f INTERFACE_HOMOGENEITY can pass, can fail on each registered failure mode, and
reports COULD_NOT_CHECK -- never PASS -- when no envelope carries a receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
R14 = ROOT / "research" / "experiments" / "e30-r14"


@pytest.fixture(scope="module")
def analysis():
    spec = importlib.util.spec_from_file_location("e30_r14_analysis_t", R14 / "e30_r14_analysis.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _envelopes(tmp_path: Path, receipts: dict[tuple[str, str, str], dict | None]) -> tuple[Path, callable]:
    campaign = tmp_path / "campaign"
    for (rep, arm, task), receipt in receipts.items():
        path = campaign / "run" / f"confirmatory-r{rep}" / "responses" / arm / f"{task}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        body = {"status": "COMPLETED_PROPOSAL_ONLY"}
        if receipt is not None:
            body["interface_receipt"] = receipt
        path.write_text(json.dumps(body))

    def iter_envelopes(campaign_root, arms, reps, task_ids):
        for rep in reps:
            for arm in arms:
                for task in task_ids:
                    yield rep, arm, task, campaign_root / "run" / f"confirmatory-r{rep}" / "responses" / arm / f"{task}.json"
    return campaign, iter_envelopes


GOOD = {"edit_interface": "anchored_edits", "edit_interface_sha256": "abc",
        "presentation": {"presentation_policy": "mentioned_files_full", "mentioned_files_truncated": 0}}
ARMS, REPS, TASKS = ["A", "B"], ["1"], ["t1", "t2"]


def _run(analysis, tmp_path, receipts):
    campaign, it = _envelopes(tmp_path, receipts)
    return analysis.interface_homogeneity(campaign, ARMS, REPS, TASKS, "anchored_edits", "abc",
                                          "mentioned_files_full", it)


def test_clean_campaign_passes(analysis, tmp_path):
    gate = _run(analysis, tmp_path, {("1", a, t): dict(GOOD) for a in ARMS for t in TASKS})
    assert gate["status"] == "PASS" and gate["offender_count"] == 0
    assert gate["envelopes_with_an_interface_receipt"] == 4


def test_absent_receipt_fails(analysis, tmp_path):
    receipts = {("1", a, t): dict(GOOD) for a in ARMS for t in TASKS}
    receipts[("1", "A", "t1")] = None
    gate = _run(analysis, tmp_path, receipts)
    assert gate["status"] == "FAIL"
    assert any(o["reason"] == "INTERFACE_RECEIPT_ABSENT" for o in gate["offenders"])


def test_two_fingerprints_fail(analysis, tmp_path):
    receipts = {("1", a, t): dict(GOOD) for a in ARMS for t in TASKS}
    receipts[("1", "B", "t2")] = {**GOOD, "edit_interface_sha256": "def"}
    gate = _run(analysis, tmp_path, receipts)
    assert gate["status"] == "FAIL" and len(gate["interface_sha256_counts"]) == 2
    assert any(o["reason"] == "INTERFACE_SHA256_MISMATCH" for o in gate["offenders"])


def test_truncated_mentioned_file_under_full_policy_fails(analysis, tmp_path):
    receipts = {("1", a, t): dict(GOOD) for a in ARMS for t in TASKS}
    receipts[("1", "A", "t2")] = {**GOOD, "presentation": {"presentation_policy": "mentioned_files_full",
                                                           "mentioned_files_truncated": 1}}
    gate = _run(analysis, tmp_path, receipts)
    assert gate["status"] == "FAIL"
    assert any(o["reason"] == "MENTIONED_FILE_TRUNCATED_UNDER_FULL_POLICY" for o in gate["offenders"])


def test_wrong_policy_fails(analysis, tmp_path):
    receipts = {("1", a, t): dict(GOOD) for a in ARMS for t in TASKS}
    receipts[("1", "A", "t1")] = {**GOOD, "presentation": {"presentation_policy": "per_file_cap", "mentioned_files_truncated": 0}}
    gate = _run(analysis, tmp_path, receipts)
    assert gate["status"] == "FAIL"
    assert any(o["reason"] == "PRESENTATION_POLICY_MISMATCH" for o in gate["offenders"])


def test_no_receipts_is_could_not_check_not_pass(analysis, tmp_path):
    gate = _run(analysis, tmp_path, {("1", a, t): None for a in ARMS for t in TASKS})
    assert gate["status"] == "COULD_NOT_CHECK"


def test_design_builder_refuses_an_incomplete_calibration(tmp_path):
    """The archived first attempt (three failed calls, no measured cell) must never freeze a design."""
    import subprocess
    import sys
    attempt = {
        "schema_version": "orion.v2.e30-r14-interface-calibration.v1",
        "is_an_endpoint_read": False, "response_text_retained": False,
        "parameters": {"tasks": ["t1", "t2"]},
        "summary": {"unified_diff|per_file_cap": {"calls": 2, "completed_envelopes": 0, "applied": 0,
                                                  "apply_failure_rate": None, "emission_statuses": {},
                                                  "interface_sha256s": [""]}},
    }
    cal = tmp_path / "cal.json"
    cal.write_text(json.dumps(attempt))
    cp = subprocess.run([sys.executable, str(R14 / "e30_r14_build_design.py"), str(ROOT), str(cal)],
                        text=True, capture_output=True, check=False,
                        env={"PATH": "/usr/bin:/bin", "HOME": str(tmp_path)})
    assert cp.returncode in (3, 5), cp.stderr
    if cp.returncode == 5:
        assert "CALIBRATION_INCOMPLETE" in cp.stderr
