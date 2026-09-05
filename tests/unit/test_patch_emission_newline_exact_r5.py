"""R5 instrument repair (revival backlog #308, row R5): newline-exact hunk counts at emission.

Planted miscount: a context line that CONTAINS a form feed (``\\x0c``, a page break in a Python
file).  ``str.splitlines()`` -- used by the frozen canonicalizer -- breaks that line in two, the
canonicalizer rewrites the empty second half as a blank context marker and its recomputed hunk
count is one too large; ``git apply --check`` then rejects the "canonical" patch as corrupt.  The
emission layer shields the eight non-newline terminators for the whole pipeline and restores them,
so the emitted patch applies.  No-alarm: an ordinary diff round-trips byte-identical to the frozen
canonicalizer's own output with an empty ``nonstandard_line_terminators_shielded`` list.

Also covered: the GC2 evaluator's header-exact endpoint reads the emission receipt when present
(post-E80 arms emit canonical diffs, so the archived content is vacuously header-exact) and falls
back to the syntax audit of the archived content on legacy responses.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from orion_v2.patch_emission import (
    NONSTANDARD_LINE_TERMINATORS,
    PatchEmissionError,
    emit_apply_clean_patch,
    shield_nonstandard_line_terminators,
    unshield_nonstandard_line_terminators,
)
from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff

HAS_GIT = shutil.which("git") is not None


def _workspace(tmp_path: Path, content: str) -> Path:
    ws = tmp_path / "ws"
    ws.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=ws, check=True)
    (ws / "mod.py").write_text(content, encoding="utf-8")
    return ws


FF_BEFORE = "import os\n\x0c\ndef page_two():\n    return 1\n"
FF_PATCH = (
    "diff --git a/mod.py b/mod.py\n"
    "--- a/mod.py\n"
    "+++ b/mod.py\n"
    "@@ -1,4 +1,4 @@\n"
    " import os\n"
    " \x0c\n"
    " def page_two():\n"
    "-    return 1\n"
    "+    return 2\n"
)


def test_frozen_canonicalizer_miscounts_form_feed_context_line_planted() -> None:
    """The defect is real: the frozen canonicalizer inflates the hunk count by one."""
    audit = audit_and_canonicalize_unified_diff(FF_PATCH)
    assert audit.valid_or_canonicalizable
    assert audit.changed
    assert any(r.startswith("normalized hunk counts") for r in audit.reasons)
    assert "@@ -1,5 +1,5 @@" in (audit.canonical_diff or "")  # one too many on both sides


@pytest.mark.skipif(not HAS_GIT, reason="git required")
def test_emission_recounts_newline_exact_and_applies(tmp_path: Path) -> None:
    ws = _workspace(tmp_path, FF_BEFORE)
    # planted: the frozen canonicalizer's own output does NOT apply
    frozen = audit_and_canonicalize_unified_diff(FF_PATCH).canonical_diff or ""
    rejected = subprocess.run(["git", "apply", "--check", "-"], cwd=ws, input=frozen, text=True, capture_output=True)
    assert rejected.returncode != 0
    # repaired: emission shields the form feed, counts are newline-exact, the patch applies
    em = emit_apply_clean_patch(FF_PATCH, workspace=ws)
    assert em.receipt["nonstandard_line_terminators_shielded"] == ["FF"]
    assert "@@ -1,4 +1,4 @@" in em.patch and "\x0c" in em.patch
    assert em.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"
    assert em.receipt["extracted_was_header_exact"] is True
    accepted = subprocess.run(["git", "apply", "--check", "-"], cwd=ws, input=em.patch, text=True, capture_output=True)
    assert accepted.returncode == 0, accepted.stderr


def test_no_alarm_ordinary_diff_is_byte_identical_to_frozen_canonicalizer() -> None:
    plain = (
        "diff --git a/mod.py b/mod.py\n--- a/mod.py\n+++ b/mod.py\n"
        "@@ -1,2 +1,2 @@\n import os\n-x = 1\n+x = 2\n"
    )
    em = emit_apply_clean_patch(plain)
    assert em.receipt["nonstandard_line_terminators_shielded"] == []
    assert em.patch == (audit_and_canonicalize_unified_diff(plain).canonical_diff or plain)
    assert em.receipt["extracted_was_header_exact"] is True


@pytest.mark.parametrize("char,name", NONSTANDARD_LINE_TERMINATORS)
def test_every_registered_terminator_round_trips(char: str, name: str) -> None:
    text = f"a{char}b\n"
    shielded, mapping = shield_nonstandard_line_terminators(text)
    assert char not in shielded and len(mapping) == 1
    assert shielded.splitlines() == [shielded.rstrip("\n")]  # the shield really stops the split
    assert unshield_nonstandard_line_terminators(shielded, mapping) == text


def test_sentinel_collision_is_cannot_check_not_a_pass() -> None:
    with pytest.raises(PatchEmissionError, match="CANNOT_CHECK"):
        shield_nonstandard_line_terminators(" line\n")


def test_gc2_evaluator_header_exact_endpoint_prefers_emission_receipt(tmp_path: Path) -> None:
    """Receipt-aware endpoint: a post-E80 response whose archived content is canonical but whose
    receipt records a miscounted extraction must NOT score header-exact; a legacy response without
    a receipt keeps the audit-of-content behaviour (no-alarm)."""
    import importlib.util
    import sys

    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("gc2_suite_r5", root / "scripts" / "run_orion_generated_composition_gc2_suite.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    src = mod.evaluate_one.__code__.co_consts
    assert "patch_emission_receipt.extracted_was_header_exact" in src
    assert "syntax_audit_of_archived_content" in src
    # newline-exact reference patches: a form feed inside a context line does not inflate counts
    ws = tmp_path / "ws"
    ws.mkdir()
    (ws / "f.py").write_text("x\n\x0c\ny\n", encoding="utf-8")
    patch = mod.rooted_patch(ws, {"f.py": "x\n\x0c\nz\n"})
    assert "@@ -1,3 +1,3 @@" in patch and " \x0c\n" in patch
    assert patch.count("\n") == 8  # diff/---/+++/@@ + 4 body lines: no line was split at the form feed
