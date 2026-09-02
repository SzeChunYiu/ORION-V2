"""Regression tests for arm-side apply-clean patch emission.

The fixtures are drawn from the archived failures of two frozen studies:

* E20 (``research/evaluation/E20_PATCH_SERIALIZATION_CONFOUND_AUDIT_V1.md``) —
  ``pandas-1`` emitted ``--- path`` without the ``a/`` prefix; ``pandas-3`` declared
  ``7 -> 8`` hunks whose bodies implied ``8 -> 9``.
* E70-GC1 (``.../results/issue45/e70-gc1-r1``) — an over-counted ``N`` makes
  ``git apply`` reject the patch, an under-counted ``N`` makes it silently truncate.
* E70-GC2 (``research/experiments/e70-gc2``) — multi-file patches (47 of 48 cells)
  carry more hunks and miscount more often; the two residual failures were context
  mismatches at ``normalize.py:5`` and ``solver.py:3``, which are NOT repairable.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest

from orion_v2.patch_emission import (
    PatchEmissionError,
    emit_apply_clean_patch,
    extract_unified_diff,
    synthesize_diff_git_headers,
)
from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff

REPO_ROOT = Path(__file__).resolve().parents[2]

SOLVER = "def decide(record):\n    value = record['value']\n    if value > 10:\n        return 'HIGH'\n    return 'LOW'\n"
NORMALIZE = "UNITS = {'m': 1.0}\n\n\ndef to_metres(value, unit):\n    return value * UNITS[unit]\n"


def _workspace(root: Path) -> Path:
    workspace = root / "solver-workspace"
    workspace.mkdir()
    (workspace / "solver.py").write_text(SOLVER)
    (workspace / "normalize.py").write_text(NORMALIZE)
    return workspace


def _applies(workspace: Path, patch: str) -> bool:
    completed = subprocess.run(
        ["git", "apply", "--check", "--whitespace=nowarn", "-"],
        cwd=str(workspace), input=patch, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return completed.returncode == 0


# --- the keystone: downstream normalization becomes a no-op ---------------------

MISCOUNTED_SINGLE = (
    "diff --git a/solver.py b/solver.py\n"
    "--- a/solver.py\n"
    "+++ b/solver.py\n"
    "@@ -2,3 +2,3 @@\n"
    "     value = record['value']\n"
    "-    if value > 10:\n"
    "+    if value >= 10:\n"
    "         return 'HIGH'\n"
)
E20_PANDAS_1_MISSING_PREFIXES = (
    "diff --git a/solver.py b/solver.py\n"
    "--- solver.py\n"
    "+++ solver.py\n"
    "@@ -2,3 +2,3 @@\n"
    "     value = record['value']\n"
    "-    if value > 10:\n"
    "+    if value >= 10:\n"
    "         return 'HIGH'\n"
)
E20_PANDAS_3_UNDERCOUNT = (
    "diff --git a/solver.py b/solver.py\n"
    "--- a/solver.py\n"
    "+++ b/solver.py\n"
    "@@ -1,3 +1,4 @@\n"
    " def decide(record):\n"
    "     value = record['value']\n"
    "-    if value > 10:\n"
    "+    if value is None:\n"
    "+        raise TypeError('value is required')\n"
    "+    if value >= 10:\n"
    "         return 'HIGH'\n"
)
GC1_OVERCOUNT = (
    "diff --git a/solver.py b/solver.py\n"
    "--- a/solver.py\n"
    "+++ b/solver.py\n"
    "@@ -2,9 +2,9 @@\n"
    "     value = record['value']\n"
    "-    if value > 10:\n"
    "+    if value >= 10:\n"
    "         return 'HIGH'\n"
)
GC2_MULTI_FILE_MULTI_HUNK = (
    "diff --git a/solver.py b/solver.py\n"
    "--- a/solver.py\n"
    "+++ b/solver.py\n"
    "@@ -1,2 +1,3 @@\n"
    " def decide(record):\n"
    "+    record = dict(record)\n"
    "     value = record['value']\n"
    "@@ -3,2 +4,2 @@\n"
    "-    if value > 10:\n"
    "+    if value >= 10:\n"
    "         return 'HIGH'\n"
    "diff --git a/normalize.py b/normalize.py\n"
    "--- normalize.py\n"
    "+++ normalize.py\n"
    "@@ -1,3 +1,3 @@\n"
    "-UNITS = {'m': 1.0}\n"
    "+UNITS = {'m': 1.0, 'km': 1000.0}\n"
    " \n"
    "@@ -4,2 +4,3 @@\n"
    " def to_metres(value, unit):\n"
    "+    unit = unit.lower()\n"
    "     return value * UNITS[unit]\n"
)
FENCED_WITH_PROSE = (
    "Here is the smallest justified repair.\n\n"
    "```diff\n" + MISCOUNTED_SINGLE + "```\n"
    "This restores the documented inclusive threshold.\n"
)

APPLY_CLEAN_FIXTURES = {
    "single-hunk miscount": MISCOUNTED_SINGLE,
    "E20 pandas-1 missing a/b prefixes": E20_PANDAS_1_MISSING_PREFIXES,
    "E20 pandas-3 undercount": E20_PANDAS_3_UNDERCOUNT,
    "GC1 overcount": GC1_OVERCOUNT,
    "GC2 multi-file multi-hunk": GC2_MULTI_FILE_MULTI_HUNK,
    "fenced with surrounding prose": FENCED_WITH_PROSE,
}


@pytest.mark.parametrize("label", sorted(APPLY_CLEAN_FIXTURES))
def test_downstream_canonicalization_is_a_no_op(label: str, tmp_path: Path) -> None:
    """The deliverable: what an arm emits needs no downstream normalization."""
    emission = emit_apply_clean_patch(APPLY_CLEAN_FIXTURES[label], workspace=_workspace(tmp_path))
    audit = audit_and_canonicalize_unified_diff(emission.patch)
    assert audit.valid_or_canonicalizable
    assert audit.changed is False, f"{label} still needs downstream normalization: {audit.reasons}"
    assert audit.canonical_diff == emission.patch


@pytest.mark.parametrize("label", sorted(APPLY_CLEAN_FIXTURES))
def test_emitted_patch_applies_cleanly(label: str, tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    emission = emit_apply_clean_patch(APPLY_CLEAN_FIXTURES[label], workspace=workspace)
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert emission.receipt["emitted_apply_check"] == "PASSED"
    assert _applies(workspace, emission.patch)


# --- the specific archived failure mechanisms ----------------------------------

def test_gc1_overcount_rejected_raw_but_apply_clean_after_emission(tmp_path: Path) -> None:
    """An over-counted N makes git apply reject the patch ('corrupt patch')."""
    workspace = _workspace(tmp_path)
    assert not _applies(workspace, GC1_OVERCOUNT)
    emission = emit_apply_clean_patch(GC1_OVERCOUNT, workspace=workspace)
    assert emission.receipt["extracted_was_apply_clean"] is False
    assert _applies(workspace, emission.patch)
    assert "@@ -2,3 +2,3 @@" in emission.patch


def test_undercount_no_longer_truncates_the_edit(tmp_path: Path) -> None:
    """An under-counted N makes git apply silently drop the tail of the hunk."""
    workspace = _workspace(tmp_path)
    emission = emit_apply_clean_patch(E20_PANDAS_3_UNDERCOUNT, workspace=workspace)
    assert "@@ -1,4 +1,6 @@" in emission.patch
    subprocess.run(
        ["git", "apply", "--whitespace=nowarn", "-"], cwd=str(workspace),
        input=emission.patch, text=True, check=True,
    )
    applied = (workspace / "solver.py").read_text()
    assert "raise TypeError('value is required')" in applied
    assert "if value >= 10:" in applied
    assert "return 'LOW'" in applied, "the file tail must survive; truncation is the GC1 failure mode"


def test_multi_file_patch_keeps_every_file_and_hunk(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    emission = emit_apply_clean_patch(GC2_MULTI_FILE_MULTI_HUNK, workspace=workspace)
    assert emission.patch.count("diff --git ") == 2
    assert emission.patch.count("@@ -") == 4
    assert "--- a/normalize.py" in emission.patch and "+++ b/normalize.py" in emission.patch
    subprocess.run(
        ["git", "apply", "--whitespace=nowarn", "-"], cwd=str(workspace),
        input=emission.patch, text=True, check=True,
    )
    assert "'km': 1000.0" in (workspace / "normalize.py").read_text()
    assert "record = dict(record)" in (workspace / "solver.py").read_text()


# --- context mismatch: detected and reported, never repaired -------------------

CONTEXT_MISMATCH_NORMALIZE = (
    "diff --git a/normalize.py b/normalize.py\n"
    "--- a/normalize.py\n"
    "+++ b/normalize.py\n"
    "@@ -5,3 +5,3 @@\n"
    " def to_metres(value, unit):\n"
    "-    return value * UNIT_TABLE[unit]\n"
    "+    return value * UNIT_TABLE[unit.lower()]\n"
)
CONTEXT_MISMATCH_SOLVER = (
    "diff --git a/solver.py b/solver.py\n"
    "--- a/solver.py\n"
    "+++ b/solver.py\n"
    "@@ -3,4 +3,4 @@\n"
    "     value = record['value']\n"
    "-    if threshold_exceeded(value):\n"
    "+    if threshold_reached(value):\n"
    "         return 'HIGH'\n"
)


@pytest.mark.parametrize(
    ("label", "patch"),
    [("gc2-003 normalize.py:5", CONTEXT_MISMATCH_NORMALIZE), ("gc2-004 solver.py:3", CONTEXT_MISMATCH_SOLVER)],
)
def test_context_mismatch_is_reported_not_repaired(label: str, patch: str, tmp_path: Path) -> None:
    """Wrong context lines are a semantic defect; emission must fail closed."""
    workspace = _workspace(tmp_path)
    emission = emit_apply_clean_patch(patch, workspace=workspace)
    assert emission.receipt["emission_status"] == "CANONICAL_BUT_APPLY_CHECK_FAILED"
    assert emission.receipt["emitted_apply_check"] == "FAILED"
    assert emission.receipt["emitted_apply_check_error"].strip(), "the failure reason must be recorded"
    assert emission.apply_clean_by_construction is False
    # No hunk was relocated and no context line was rewritten.
    for line in patch.splitlines():
        if line.startswith(("-", "+")) and not line.startswith(("---", "+++")):
            assert line in emission.patch
    assert "@@ -5," in emission.patch or "@@ -3," in emission.patch, "hunk start line must be preserved"


def test_hunks_are_never_relocated(tmp_path: Path) -> None:
    """git apply searches the whole file for context, so relocation is never needed
    and would be forbidden semantic inference if attempted."""
    workspace = _workspace(tmp_path)
    off_by_two = MISCOUNTED_SINGLE.replace("@@ -2,3 +2,3 @@", "@@ -4,3 +4,3 @@")
    emission = emit_apply_clean_patch(off_by_two, workspace=workspace)
    assert "@@ -4,3 +4,3 @@" in emission.patch
    assert emission.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"


# --- interface-fidelity endpoint is preserved, not destroyed -------------------

def test_receipt_preserves_the_raw_header_exact_endpoint(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    already_canonical = (
        "diff --git a/solver.py b/solver.py\n"
        "--- a/solver.py\n"
        "+++ b/solver.py\n"
        "@@ -2,3 +2,3 @@\n"
        "     value = record['value']\n"
        "-    if value > 10:\n"
        "+    if value >= 10:\n"
        "         return 'HIGH'\n"
    )
    clean = emit_apply_clean_patch(already_canonical, workspace=workspace)
    assert clean.receipt["extracted_was_header_exact"] is True
    assert clean.receipt["extracted_was_apply_clean"] is True
    assert clean.receipt["normalizations"] == []
    assert clean.patch == already_canonical

    dirty = emit_apply_clean_patch(GC1_OVERCOUNT, workspace=workspace)
    assert dirty.receipt["extracted_was_header_exact"] is False
    assert dirty.receipt["extracted_was_apply_clean"] is False
    assert any("normalized hunk counts" in reason for reason in dirty.receipt["normalizations"])
    assert dirty.receipt["raw_sha256"] == hashlib.sha256(GC1_OVERCOUNT.encode()).hexdigest()
    assert dirty.receipt["emitted_sha256"] != dirty.receipt["raw_sha256"]


def test_receipt_records_gold_blind_non_authority() -> None:
    receipt = emit_apply_clean_patch(MISCOUNTED_SINGLE).receipt
    assert receipt["authority"]["gold_or_fixed_patch_access"] == "FORBIDDEN_NOT_USED"
    assert receipt["authority"]["may_change_semantic_edit"] is False
    assert receipt["authority"]["may_guess_paths"] is False
    assert receipt["authority"]["may_relocate_hunks"] is False
    assert receipt["authority"]["may_rescore_a_frozen_campaign"] is False


def test_emission_degrades_honestly_without_a_workspace() -> None:
    emission = emit_apply_clean_patch(GC1_OVERCOUNT)
    assert emission.receipt["emission_status"] == "CANONICAL_APPLY_CHECK_NOT_VERIFIED"
    assert emission.receipt["emitted_apply_check"] == "NOT_VERIFIED_NO_WORKSPACE"
    assert emission.receipt["extracted_was_apply_clean"] is None
    assert audit_and_canonicalize_unified_diff(emission.patch).changed is False


# --- extraction and header synthesis ------------------------------------------

def test_extraction_strips_fences_and_surrounding_prose() -> None:
    extracted = extract_unified_diff(FENCED_WITH_PROSE)
    assert extracted.startswith("diff --git a/solver.py b/solver.py\n")
    assert "smallest justified repair" not in extracted
    assert "inclusive threshold" not in extracted


def test_extraction_keeps_a_trailing_edit_line() -> None:
    patch = "--- a/x.py\n+++ b/x.py\n@@ -1,1 +1,1 @@\n-old\n+new\n"
    assert extract_unified_diff(patch).endswith("-old\n+new\n")


def test_extraction_rejects_output_with_no_diff() -> None:
    with pytest.raises(PatchEmissionError):
        extract_unified_diff("I could not determine a repair for this failure.")


def test_header_synthesis_never_guesses_a_path() -> None:
    synthesized = synthesize_diff_git_headers("--- pkg/x.py\n+++ pkg/x.py\n@@ -1,1 +1,1 @@\n-a\n+b\n")
    assert synthesized.startswith("diff --git a/pkg/x.py b/pkg/x.py\n")
    with pytest.raises(PatchEmissionError):
        synthesize_diff_git_headers("--- a/x.py\n+++ b/y.py\n@@ -1,1 +1,1 @@\n-a\n+b\n")


def test_uncanonicalizable_patch_is_emitted_unchanged_not_dropped() -> None:
    traversal = (
        "diff --git a/../secret b/../secret\n"
        "--- a/../secret\n"
        "+++ b/../secret\n"
        "@@ -1,1 +1,1 @@\n"
        "-a\n"
        "+b\n"
    )
    emission = emit_apply_clean_patch(traversal)
    assert emission.receipt["emission_status"] == "NOT_CANONICALIZABLE_EMITTED_UNCHANGED"
    assert emission.patch == traversal
    assert emission.receipt["canonicalizer_rejection_reasons"]


# --- the frozen control must stay frozen ---------------------------------------

def test_frozen_e30_control_code_is_unmodified() -> None:
    """E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1 pins these by sha256 and forbids any
    change after outcome access. Emission is a new layer on top, never an edit."""
    pinned = {
        "src/orion_v2/unified_diff_interface.py": "654883709bb08700",
        "scripts/audit_orion_diff_interface.py": "3199877add723f0e",
        "scripts/evaluate_orion_real_problem_responses_v2.py": "e677efbf1def2c87",
        "scripts/analyze_orion_real_problem_results.py": "ef195f7b8d6edafb",
    }
    for relative, prefix in pinned.items():
        digest = hashlib.sha256((REPO_ROOT / relative).read_bytes()).hexdigest()
        assert digest.startswith(prefix), f"{relative} broke the E30 freeze pin"


# --- the response validator's own guard, checked in both directions -------------

def _validated_response(mutate=None) -> list[str]:
    from scripts.orion_claude_arms import run_arm
    from scripts.validate_orion_agent_responses import validate_response

    def call(prompt: str) -> tuple[str, dict[str, int]]:
        return (
            '{"patch":"diff --git a/a.py b/a.py\\n--- a.py\\n+++ a.py\\n'
            '@@ -1,9 +1,9 @@\\n ctx\\n-x=1\\n+x=2", "diagnosis":"constant", "falsifier":"native evaluator"}',
            {"input_tokens": 4, "output_tokens": 8},
        )

    request = {
        "task_id": "bugsinpy-demo-1", "arm_id": "SIMPLE_DIRECT",
        "task": {"project": "demo", "bug_id": 1, "solver_workspace": ""},
    }
    response = run_arm(request, call=call, workspace_context="context")
    if mutate is not None:
        mutate(response["patch_emission_receipt"])
    return validate_response(
        response,
        expected_task_id="bugsinpy-demo-1",
        expected_arm_id="SIMPLE_DIRECT",
        required_fields=("proposed_patch_or_artifact", "diagnosis", "falsifier"),
    )


def test_validator_accepts_a_real_emitting_arm_response() -> None:
    """No-alarm case: a guard that misfires on real output gets switched off."""
    assert _validated_response() == []


@pytest.mark.parametrize(
    ("label", "mutate", "expected"),
    [
        (
            "authority claiming semantic edits",
            lambda receipt: receipt["authority"].update({"may_change_semantic_edit": True}),
            "claims authority beyond serialization",
        ),
        (
            "authority claiming frozen-campaign rescoring",
            lambda receipt: receipt["authority"].update({"may_rescore_a_frozen_campaign": True}),
            "claims authority beyond serialization",
        ),
        (
            "gold access not disclaimed",
            lambda receipt: receipt["authority"].update({"gold_or_fixed_patch_access": "USED"}),
            "must record gold-blind emission",
        ),
        (
            "authority block replaced by a non-object",
            lambda receipt: receipt.__setitem__("authority", "none"),
            "must record gold-blind emission",
        ),
        (
            "unknown receipt schema version",
            lambda receipt: receipt.__setitem__("schema_version", "orion.v2.patch-emission.v9"),
            "unexpected patch_emission_receipt schema_version",
        ),
        (
            "missing fidelity endpoint",
            lambda receipt: receipt.pop("extracted_was_header_exact"),
            "missing required key: extracted_was_header_exact",
        ),
        (
            "receipt is not an object",
            None,
            "patch_emission_receipt must be an object when supplied",
        ),
    ],
)
def test_validator_rejects_a_receipt_that_oversteps(label: str, mutate, expected: str) -> None:
    if mutate is None:
        from scripts.validate_orion_agent_responses import validate_response

        errors = validate_response(
            {
                "schema_version": "orion.v2.agent-response.v1", "task_id": "t", "arm_id": "a",
                "status": "COMPLETED_PROPOSAL_ONLY", "requested_authority": "EXECUTION_TEST_ONLY",
                "proposed_patch_or_artifact": {"type": "unified_diff", "content": "diff"},
                "falsifier": "native evaluator", "uncertainty": "UNRESOLVED",
                "patch_emission_receipt": "not-an-object",
            },
            expected_task_id="t", expected_arm_id="a", required_fields=(),
        )
    else:
        errors = _validated_response(mutate)
    assert any(expected in error for error in errors), f"{label}: guard did not fire ({errors})"
