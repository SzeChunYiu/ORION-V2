"""E30-R14 interface contract: the arms executable's presentation and emission plumbing.

The interface is a registered experimental condition (E30-R13 showed a served-model
pin and a request-body contract still leave it free): it must fail closed on unknown
values, be fingerprinted over bytes, and be recorded on every envelope.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture()
def arms():
    spec = importlib.util.spec_from_file_location(
        "orion_claude_arms_r14", REPO_ROOT / "scripts" / "orion_claude_arms.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BIG = "".join(f"line_{i} = {i}\n" for i in range(4000))          # ~56 kB, beyond the 30 kB cap
SMALL = "def helper():\n    return 1\n"


def _workspace(root: Path) -> Path:
    workspace = root / "ws"
    (workspace / "pkg").mkdir(parents=True)
    (workspace / "pkg" / "big_module.py").write_text(BIG)
    (workspace / "pkg" / "small.py").write_text(SMALL)
    (workspace / "tests").mkdir()
    (workspace / "tests" / "test_big.py").write_text("def test_x():\n    assert line_3999 == 3999\n")
    return workspace


def _request(workspace: Path) -> dict:
    return {"task_id": "t", "arm_id": "SIMPLE_DIRECT",
            "task": {"solver_workspace": str(workspace),
                     "baseline_observation": {"stdout_tail": "FAILED tests/test_big.py::test_x - pkg/big_module.py"}}}


def test_default_interface_is_the_historical_one_so_no_existing_lane_changes(arms, monkeypatch):
    monkeypatch.delenv("ORION_EDIT_INTERFACE", raising=False)
    monkeypatch.delenv("ORION_PRESENTATION_POLICY", raising=False)
    assert arms.edit_interface_id() == "unified_diff"
    assert arms.presentation_policy() == "per_file_cap"
    assert "`patch` must be one syntactically valid unified diff" in arms._final_prompt("CTX")


def test_unknown_interface_or_policy_fails_closed(arms, monkeypatch):
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "search_replace_v9")
    with pytest.raises(arms.EditInterfaceUnknown):
        arms.edit_interface_id()
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "anchored_edits")
    monkeypatch.setenv("ORION_PRESENTATION_POLICY", "everything")
    with pytest.raises(arms.PresentationPolicyUnknown):
        arms.presentation_policy()


def test_anchored_interface_selects_its_prompt_and_its_presentation(arms, monkeypatch):
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "anchored_edits")
    monkeypatch.delenv("ORION_PRESENTATION_POLICY", raising=False)
    assert arms.presentation_policy() == "mentioned_files_full"
    prompt = arms._final_prompt("CTX")
    assert "`edits` must be a list" in prompt and "copied VERBATIM" in prompt
    assert "unified diff, rooted at repository paths" not in prompt


def test_fingerprint_separates_interfaces_and_policies_and_is_stable(arms, monkeypatch):
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "anchored_edits")
    monkeypatch.setenv("ORION_PRESENTATION_POLICY", "mentioned_files_full")
    a = arms.edit_interface_sha256("anchored_edits")
    assert a == arms.edit_interface_sha256("anchored_edits")
    monkeypatch.setenv("ORION_PRESENTATION_POLICY", "per_file_cap")
    b = arms.edit_interface_sha256("anchored_edits")
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "unified_diff")
    c = arms.edit_interface_sha256("unified_diff")
    assert len({a, b, c}) == 3 and all(len(x) == 64 for x in (a, b, c))


def test_per_file_cap_truncates_the_mentioned_file_and_records_it(arms, monkeypatch, tmp_path):
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "unified_diff")
    monkeypatch.delenv("ORION_PRESENTATION_POLICY", raising=False)
    context = json.loads(arms._context(_request(_workspace(tmp_path))))
    trunc = context["source_snapshot_truncation"]
    assert trunc["presentation_policy"] == "per_file_cap"
    big = next(r for r in trunc["per_file"] if r["path"] == "pkg/big_module.py")
    assert big["mentioned_in_baseline"] and big["truncated"] and big["chars_shown"] == 30000
    assert trunc["mentioned_files_truncated"] == 1
    shown = next(s for s in context["source_snapshots"] if s["path"] == "pkg/big_module.py")["content"]
    assert "line_3999" not in shown        # the model would be editing code it cannot see


def test_mentioned_files_full_shows_the_whole_mentioned_file_and_keeps_the_cap_elsewhere(arms, monkeypatch, tmp_path):
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "anchored_edits")
    monkeypatch.delenv("ORION_PRESENTATION_POLICY", raising=False)
    monkeypatch.setenv("ORION_CONTEXT_MAX_FILE_CHARS", "10")
    context = json.loads(arms._context(_request(_workspace(tmp_path))))
    trunc = context["source_snapshot_truncation"]
    assert trunc["presentation_policy"] == "mentioned_files_full"
    big = next(r for r in trunc["per_file"] if r["path"] == "pkg/big_module.py")
    small = next(r for r in trunc["per_file"] if r["path"] == "pkg/small.py")
    assert not big["truncated"] and big["chars_shown"] == len(BIG)
    assert small["truncated"] and small["chars_shown"] == 10         # the cap still binds unmentioned files
    assert trunc["mentioned_files_truncated"] == 0
    shown = next(s for s in context["source_snapshots"] if s["path"] == "pkg/big_module.py")["content"]
    assert "line_3999" in shown


def test_both_envelopes_carry_the_interface_receipt(arms, monkeypatch, tmp_path):
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "anchored_edits")
    monkeypatch.delenv("ORION_PRESENTATION_POLICY", raising=False)
    monkeypatch.delenv("ORION_ARM_SERVED_MODEL", raising=False)
    workspace = _workspace(tmp_path)
    request = _request(workspace)
    context = arms._context(request)
    good = json.dumps({"edits": [{"path": "pkg/small.py", "search": "    return 1\n", "replace": "    return 2\n"}],
                       "diagnosis": "d", "assumptions": [], "uncertainty": "u", "discriminator_or_tests": [], "falsifier": "f"})

    def call_ok(prompt):
        return good, {"input_tokens": 1, "output_tokens": 1, "_served_model": "glm-5.3"}

    def call_bad(prompt):
        return "not json", {"input_tokens": 1, "output_tokens": 1}

    ok = arms.run_arm(request, call=call_ok, workspace_context=context)
    assert ok["status"] == "COMPLETED_PROPOSAL_ONLY"
    assert ok["interface_receipt"]["edit_interface"] == "anchored_edits"
    assert ok["interface_receipt"]["presentation"]["presentation_policy"] == "mentioned_files_full"
    assert ok["interface_receipt"]["presentation"]["mentioned_files_truncated"] == 0
    assert "per_file" not in ok["interface_receipt"]["presentation"]
    assert ok["patch_emission_receipt"]["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert ok["proposed_patch_or_artifact"]["content"].startswith("diff --git a/pkg/small.py b/pkg/small.py\n")
    bad = arms.run_arm(request, call=call_bad, workspace_context=context)
    assert bad["status"] == "EXECUTION_FAILED_MODEL_RESPONSE"
    assert bad["interface_receipt"]["edit_interface_sha256"] == ok["interface_receipt"]["edit_interface_sha256"]


def test_under_the_historical_interface_the_envelope_is_unchanged_in_shape(arms, monkeypatch, tmp_path):
    monkeypatch.setenv("ORION_EDIT_INTERFACE", "unified_diff")
    monkeypatch.delenv("ORION_PRESENTATION_POLICY", raising=False)
    monkeypatch.delenv("ORION_ARM_SERVED_MODEL", raising=False)
    workspace = _workspace(tmp_path)
    request = _request(workspace)
    patch = ("diff --git a/pkg/small.py b/pkg/small.py\n--- a/pkg/small.py\n+++ b/pkg/small.py\n"
             "@@ -1,2 +1,2 @@\n def helper():\n-    return 1\n+    return 2\n")
    text = json.dumps({"patch": patch, "diagnosis": "d"})
    response = arms.run_arm(request, call=lambda p: (text, {"input_tokens": 1, "output_tokens": 1}),
                            workspace_context=arms._context(request))
    assert response["status"] == "COMPLETED_PROPOSAL_ONLY"
    assert response["patch_emission_receipt"]["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert "edit_interface" not in response["patch_emission_receipt"]
    assert response["interface_receipt"]["edit_interface"] == "unified_diff"


def test_the_calibration_crosses_the_two_axes_and_keeps_no_response_text():
    spec = importlib.util.spec_from_file_location(
        "cal", REPO_ROOT / "research" / "experiments" / "e30-r14" / "e30_r14_interface_calibration.py")
    cal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cal)
    assert set(cal.CONDITIONS) == {("unified_diff", "per_file_cap"), ("unified_diff", "mentioned_files_full"),
                                   ("anchored_edits", "per_file_cap"), ("anchored_edits", "mentioned_files_full")}
    assert "proposed_patch_or_artifact" in cal.DISCARDED_FIELDS and "diagnosis" in cal.DISCARDED_FIELDS
    summary = cal.summarize([
        {"interface": "anchored_edits", "presentation": "mentioned_files_full", "status": "COMPLETED_PROPOSAL_ONLY",
         "applies": True, "emission_status": "APPLY_CLEAN_BY_CONSTRUCTION", "channel_receipt": {}, "resource_receipt": {},
         "interface_receipt": {"presentation": {"mentioned_files_truncated": 0}}, "context_chars": 10, "wall_seconds": 1.0},
        {"interface": "anchored_edits", "presentation": "mentioned_files_full", "status": "COMPLETED_PROPOSAL_ONLY",
         "applies": False, "emission_status": "EDITS_NOT_LOCATED", "unlocated_reasons": ["SEARCH_NOT_FOUND"],
         "channel_receipt": {}, "resource_receipt": {}, "interface_receipt": {"presentation": {"mentioned_files_truncated": 1}},
         "context_chars": 10, "wall_seconds": 1.0},
    ])
    cell = summary["anchored_edits|mentioned_files_full"]
    assert cell["completed_envelopes"] == 2 and cell["applied"] == 1 and cell["apply_failure_rate"] == 0.5
    assert cell["unlocated_reasons"] == {"SEARCH_NOT_FOUND": 1}
    assert summary["unified_diff|per_file_cap"]["apply_rate"] is None       # no calls: not a zero
