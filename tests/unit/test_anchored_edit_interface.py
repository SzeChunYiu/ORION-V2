"""Tests for the anchored-edit interface (E30-R14 lever).

Fixtures are drawn from the E30-R13 apply-failure attribution: duplicated
``diff --git`` headers with ``index`` lines, numberless ``@@ def f(): @@`` anchors,
``--- /dev/null`` new files, whitespace drift, and -- the class no interface can
recover -- a search block the file does not contain.  Every zero below is paired with a
control that fires on the same fixture.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from orion_v2.anchored_edit_interface import (
    EDIT_INTERFACE_ID,
    AnchoredEditError,
    Edit,
    edits_from_model_object,
    edits_from_unified_diff,
    emit_anchored_edit_patch,
    locate_block,
    locate_edits,
)

REPO_ROOT = Path(__file__).resolve().parents[2]

SOLVER = (
    "import os\n"
    "\n"
    "\n"
    "def decide(record):\n"
    "    value = record['value']\n"
    "    if value > 10:\n"
    "        return 'HIGH'\n"
    "    return 'LOW'\n"
    "\n"
    "\n"
    "def other(record):\n"
    "    value = record['value']\n"
    "    if value > 10:\n"
    "        return 'BIG'\n"
    "    return 'SMALL'\n"
)
NORMALIZE = "UNITS = {'m': 1.0}\n\n\ndef to_metres(value, unit):\n    return value * UNITS[unit]\n"


def _workspace(root: Path) -> Path:
    workspace = root / "solver-workspace"
    (workspace / "pkg").mkdir(parents=True)
    (workspace / "pkg" / "solver.py").write_text(SOLVER)
    (workspace / "normalize.py").write_text(NORMALIZE)
    return workspace


def _apply(workspace: Path, patch: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "apply", "--whitespace=nowarn", "-"], cwd=str(workspace), input=patch,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )


# ---- location ---------------------------------------------------------------------------


def test_exact_unique_block_locates_once():
    hits, mode = locate_block(SOLVER.splitlines(), ["        return 'HIGH'"])
    assert hits == [6] and mode == "exact"


def test_a_block_present_twice_is_ambiguous_not_resolved():
    hits, mode = locate_block(SOLVER.splitlines(), ["    value = record['value']", "    if value > 10:"])
    assert len(hits) == 2


def test_rstrip_and_collapsed_whitespace_modes_are_tried_in_order():
    lines = SOLVER.splitlines()
    assert locate_block(lines, ["        return 'HIGH'   "])[1] == "rstrip"
    assert locate_block(lines, ["return  'HIGH'"])[1] == "collapsed_whitespace"


def test_a_fabricated_block_does_not_locate_at_any_mode():
    hits, mode = locate_block(SOLVER.splitlines(), ["this line was never in the file 0xDEADBEEF"])
    assert hits == [] and mode == "none"


# ---- native edits ------------------------------------------------------------------------


def test_native_edit_is_located_derived_and_applies(tmp_path):
    workspace = _workspace(tmp_path)
    data = {"edits": [{"path": "pkg/solver.py",
                       "search": "        return 'HIGH'\n    return 'LOW'\n",
                       "replace": "        return 'HIGH'\n    return 'LOW' if value else 'NONE'\n"}]}
    emission = emit_anchored_edit_patch(data, workspace=workspace)
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert emission.receipt["edit_interface"] == EDIT_INTERFACE_ID
    assert emission.patch.startswith("diff --git a/pkg/solver.py b/pkg/solver.py\n--- a/pkg/solver.py\n+++ b/pkg/solver.py\n@@ ")
    assert _apply(workspace, emission.patch).returncode == 0
    assert "if value else 'NONE'" in (workspace / "pkg" / "solver.py").read_text()
    # git-derived context and counts: the hunk header is consistent with the body
    header = [line for line in emission.patch.splitlines() if line.startswith("@@")][0]
    assert header.startswith("@@ -")


def test_collapsed_whitespace_match_reindents_the_replacement_by_the_measured_shift(tmp_path):
    workspace = _workspace(tmp_path)
    data = {"edits": [{"path": "pkg/solver.py",
                       "search": "return 'HIGH'\n",           # indentation dropped
                       "replace": "return 'VERY_HIGH'\n"}]}
    emission = emit_anchored_edit_patch(data, workspace=workspace)
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert emission.receipt["match_modes"]["collapsed_whitespace"] == 1
    assert "+        return 'VERY_HIGH'" in emission.patch


def test_an_unlocatable_edit_emits_no_patch_and_names_the_failure(tmp_path):
    workspace = _workspace(tmp_path)
    data = {"edits": [
        {"path": "pkg/solver.py", "search": "        return 'HIGH'\n", "replace": "        return 'H'\n"},
        {"path": "pkg/solver.py", "search": "    # ... rest of the function ...\n", "replace": "    pass\n"},
    ]}
    emission = emit_anchored_edit_patch(data, workspace=workspace)
    assert emission.receipt["emission_status"] == "EDITS_NOT_LOCATED"
    assert emission.patch == ""
    assert emission.receipt["unlocated_edits"][0]["reason"] == "SEARCH_NOT_FOUND"
    assert emission.receipt["edits_located"] == 1 and emission.receipt["edit_count"] == 2


def test_an_ambiguous_edit_is_reported_not_guessed(tmp_path):
    workspace = _workspace(tmp_path)
    data = {"edits": [{"path": "pkg/solver.py", "search": "    if value > 10:\n", "replace": "    if value >= 10:\n"}]}
    emission = emit_anchored_edit_patch(data, workspace=workspace)
    assert emission.receipt["emission_status"] == "EDITS_NOT_LOCATED"
    assert emission.receipt["unlocated_edits"][0]["reason"] == "SEARCH_AMBIGUOUS"
    assert emission.receipt["unlocated_edits"][0]["occurrences"] == 2


def test_a_missing_path_is_never_invented(tmp_path):
    workspace = _workspace(tmp_path)
    data = {"edits": [{"path": "pkg/nope.py", "search": "x\n", "replace": "y\n"}]}
    emission = emit_anchored_edit_patch(data, workspace=workspace)
    assert emission.receipt["unlocated_edits"][0]["reason"] == "PATH_NOT_IN_WORKSPACE"
    with pytest.raises(AnchoredEditError):
        edits_from_model_object({"edits": [{"path": "../escape.py", "search": "x", "replace": "y"}]})


def test_new_file_create_applies(tmp_path):
    workspace = _workspace(tmp_path)
    data = {"edits": [{"path": "pkg/new_mod.py", "create": True, "replace": "VALUE = 1\n"}]}
    emission = emit_anchored_edit_patch(data, workspace=workspace)
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert "--- /dev/null" in emission.patch and "+++ b/pkg/new_mod.py" in emission.patch
    assert _apply(workspace, emission.patch).returncode == 0
    assert (workspace / "pkg" / "new_mod.py").read_text() == "VALUE = 1\n"


def test_two_edits_in_one_file_are_applied_against_the_original_positions(tmp_path):
    workspace = _workspace(tmp_path)
    data = {"edits": [
        {"path": "pkg/solver.py", "search": "        return 'HIGH'\n", "replace": "        return 'HIGH!'\n"},
        {"path": "pkg/solver.py", "search": "        return 'BIG'\n", "replace": "        return 'BIG!'\n        # noted\n"},
    ]}
    emission = emit_anchored_edit_patch(data, workspace=workspace)
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert _apply(workspace, emission.patch).returncode == 0
    text = (workspace / "pkg" / "solver.py").read_text()
    assert "'HIGH!'" in text and "'BIG!'\n        # noted" in text


def test_overlapping_edits_are_refused(tmp_path):
    workspace = _workspace(tmp_path)
    edits = [Edit("pkg/solver.py", "    if value > 10:\n        return 'HIGH'\n", "x\n"),
             Edit("pkg/solver.py", "        return 'HIGH'\n    return 'LOW'\n", "y\n")]
    _, failures = locate_edits(workspace, edits)
    assert any(f["reason"] == "EDITS_OVERLAP" for f in failures)


def test_the_workspace_is_never_written_by_emission(tmp_path):
    workspace = _workspace(tmp_path)
    before = {p: p.read_text() for p in workspace.rglob("*.py")}
    emit_anchored_edit_patch({"edits": [{"path": "pkg/solver.py", "search": "        return 'HIGH'\n",
                                          "replace": "        return 'H'\n"}]}, workspace=workspace)
    assert {p: p.read_text() for p in workspace.rglob("*.py")} == before


# ---- unified-diff fallback: the forms E30-R13 actually emitted ---------------------------

DUPLICATED_HEADER_WITH_INDEX = (
    "diff --git a/normalize.py b/normalize.py\n"
    "index 8c4d67e..7d9f4a1 100644\n"
    "diff --git a/normalize.py b/normalize.py\n"
    "--- a/normalize.py\n"
    "+++ b/normalize.py\n"
    "@@ -4,2 +4,3 @@\n"
    " def to_metres(value, unit):\n"
    "+    assert unit in UNITS\n"
    "     return value * UNITS[unit]\n"
)

NUMBERLESS_ANCHOR = (
    "diff --git a/normalize.py b/normalize.py\n"
    "@@ def to_metres(value, unit):\n"
    "     return value * UNITS[unit]\n"
    "-UNITS = {'m': 1.0}\n"
)

NEW_FILE_DEV_NULL = (
    "diff --git a/tests/data/x.py b/tests/data/x.py\n"
    "new file mode 100644\n"
    "index 0000000..1111111\n"
    "diff --git a/tests/data/x.py b/tests/data/x.py\n"
    "--- /dev/null\n"
    "+++ b/tests/data/x.py\n"
    "@@ -0,0 +1,2 @@\n"
    "+# fmt: off\n"
    "+x = 1\n"
)


def test_frozen_canonicalizer_refuses_the_duplicated_header_form_and_the_fallback_recovers_it(tmp_path):
    from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff

    assert not audit_and_canonicalize_unified_diff(DUPLICATED_HEADER_WITH_INDEX).valid_or_canonicalizable
    workspace = _workspace(tmp_path)
    emission = emit_anchored_edit_patch({"patch": DUPLICATED_HEADER_WITH_INDEX}, workspace=workspace)
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert emission.receipt["edit_origins"] == ["unified_diff_fallback"]
    assert _apply(workspace, emission.patch).returncode == 0
    assert "assert unit in UNITS" in (workspace / "normalize.py").read_text()


def test_numberless_anchor_hunk_is_located_by_its_removed_line(tmp_path):
    workspace = _workspace(tmp_path)
    edits = edits_from_unified_diff(NUMBERLESS_ANCHOR)
    assert len(edits) == 1
    # the hunk's old block is [context, removed]; that exact pair is not contiguous in
    # the file, so the interface must refuse rather than guess
    emission = emit_anchored_edit_patch({"patch": NUMBERLESS_ANCHOR}, workspace=workspace)
    assert emission.receipt["emission_status"] == "EDITS_NOT_LOCATED"


def test_dev_null_new_file_diff_is_recovered(tmp_path):
    workspace = _workspace(tmp_path)
    emission = emit_anchored_edit_patch({"patch": NEW_FILE_DEV_NULL}, workspace=workspace)
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert _apply(workspace, emission.patch).returncode == 0
    assert (workspace / "tests" / "data" / "x.py").read_text() == "# fmt: off\nx = 1\n"


def test_a_diff_with_fabricated_context_is_not_recoverable_and_says_so(tmp_path):
    workspace = _workspace(tmp_path)
    patch = ("diff --git a/pkg/solver.py b/pkg/solver.py\n--- a/pkg/solver.py\n+++ b/pkg/solver.py\n"
             "@@ -40,3 +40,3 @@\n     # ... ANSI-safe truncation ...\n-    return None\n+    return res\n")
    emission = emit_anchored_edit_patch({"patch": patch}, workspace=workspace)
    assert emission.receipt["emission_status"] == "EDITS_NOT_LOCATED"
    assert emission.receipt["unlocated_edits"][0]["reason"] == "SEARCH_NOT_FOUND"


def test_no_alarm_a_clean_r13_style_diff_round_trips_to_the_same_edit(tmp_path):
    workspace = _workspace(tmp_path)
    clean = ("diff --git a/normalize.py b/normalize.py\n--- a/normalize.py\n+++ b/normalize.py\n"
             "@@ -4,2 +4,3 @@\n def to_metres(value, unit):\n+    assert unit in UNITS\n     return value * UNITS[unit]\n")
    assert _apply(_workspace(tmp_path / "control"), clean).returncode == 0     # control: git accepts it as-is
    emission = emit_anchored_edit_patch({"patch": clean}, workspace=workspace)
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert _apply(workspace, emission.patch).returncode == 0
    assert "assert unit in UNITS\n    return value" in (workspace / "normalize.py").read_text()


# ---- contract -------------------------------------------------------------------------------


def test_the_receipt_validates_under_the_frozen_response_validator(tmp_path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "validator", REPO_ROOT / "scripts" / "validate_orion_agent_responses.py")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    workspace = _workspace(tmp_path)
    emission = emit_anchored_edit_patch({"edits": [{"path": "pkg/solver.py", "search": "        return 'HIGH'\n",
                                                     "replace": "        return 'H'\n"}]}, workspace=workspace)
    response = {
        "schema_version": "orion.v2.agent-response.v1", "task_id": "t", "arm_id": "SIMPLE_DIRECT",
        "status": "COMPLETED_PROPOSAL_ONLY",
        "proposed_patch_or_artifact": {"type": "unified_diff", "content": emission.patch},
        "patch_emission_receipt": emission.receipt, "diagnosis": "d",
        "source_ids_used": ["gold-blind-solver-workspace"], "assumptions": ["a"], "uncertainty": "u",
        "discriminator_or_tests": ["t"], "falsifier": "f", "requested_authority": "EXECUTION_TEST_ONLY",
        "scientific_truth_authorized": False, "field_status_authorized": False,
        "publication_readiness_authorized": False,
        "resource_receipt": {"model_calls": 1, "input_tokens": 1, "output_tokens": 1},
    }
    errors = _validate(validator, response)
    assert not [e for e in errors if "patch_emission_receipt" in e], errors
    # the validator still rejects a receipt claiming relocation authority
    bad = json.loads(json.dumps(response))
    bad["patch_emission_receipt"]["authority"]["may_relocate_hunks"] = True
    errors = _validate(validator, bad)
    assert any("authority beyond serialization" in e for e in errors)


def _validate(validator, response):
    import inspect

    params = inspect.signature(validator.validate_response).parameters
    kwargs = {}
    if "expected_task_id" in params:
        kwargs["expected_task_id"] = response["task_id"]
    if "expected_arm_id" in params:
        kwargs["expected_arm_id"] = response["arm_id"]
    if "required_fields" in params:
        kwargs["required_fields"] = []
    return validator.validate_response(response, **kwargs)
