"""Arm-side emission of apply-clean unified diffs.

Two independent frozen studies localized the entire raw-endpoint variance between
solver arms to unified-diff *serialization* rather than reasoning:

* ``research/experiments/results/issue45/e70-gc1-r1`` — raw success held if and only
  if the syntax-only canonicalizer left the hunk header unchanged
  (``success_iff_header_unchanged = true`` for all four arms); the normalized lane
  was 24/24 for every arm.
* ``research/experiments/e70-gc2`` — raw header-exact success was 0/16 at every one
  of three difficulty rungs (48/48 diffs needed syntax-only canonicalization) while
  count-robust accuracy was 1.000 on every applied cell.

This module moves that repair to the *emission* side, so an arm returns a diff that
is already canonical instead of one the harness has to normalize downstream. It is
strictly an interface layer:

* it never reads a gold, fixed or reference patch — the only file it may consult is
  the gold-blind solver workspace the arm already reads;
* it never invents a file path, and never adds, removes, reorders or rewrites an
  added/removed/context line;
* it never relocates a hunk. ``git apply`` already searches the whole file for a
  hunk's context regardless of the declared start line (the sole exception is a hunk
  declaring ``old_start = 1``, which git forces to match at the beginning of the
  file), so a residual apply failure means the emitted *context* is wrong. Repairing
  that would be semantic inference, which is forbidden; it is detected and reported
  instead.

The canonicalization itself is delegated verbatim to
``orion_v2.unified_diff_interface``, which is pinned by sha256 in
``research/experiments/E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1.json`` and is not
modified by this module.

The receipt returned alongside the patch preserves the raw interface-fidelity
endpoint (``extracted_was_header_exact``, ``extracted_was_apply_clean``, the artifact
hashes and the list of normalizations applied), so a future run can still report the raw
header-exact lane from the response alone even though arms now emit canonical form.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import hashlib
import re
import shutil
import subprocess

from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff

EMISSION_SCHEMA_VERSION = "orion.v2.patch-emission.v1"

_FENCE_RE = re.compile(r"^\s*```+[A-Za-z0-9_+-]*\s*$")
_DIFF_GIT_RE = re.compile(r"^diff --git a/(?P<a>.+) b/(?P<b>.+)$")
_BODY_PREFIXES = (" ", "+", "-", "\\", "@@ ", "diff --git ", "index ", "old mode ", "new mode ")

# ``str.splitlines()`` -- used by this module's extractor, by the header synthesizer and by the
# frozen canonicalizer -- also breaks lines on eight characters that ``git`` does not treat as
# line terminators (VT, FF, FS, GS, RS, NEL, LS, PS).  A context line that merely CONTAINS one of
# them (a form feed page break in a Python file is the common case) is therefore split in two:
# the second half is an empty line, the canonicalizer rewrites it as a blank context marker, and
# the recomputed hunk count is one too large -- an instrument miscount ``git apply`` then rejects
# as a corrupt patch.  Emission shields those characters behind private-use sentinels for the
# whole pipeline and restores them afterwards, so every line count is newline-exact.  The frozen
# canonicalizer itself is not modified (it is sha256-pinned by
# ``E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1.json``).
NONSTANDARD_LINE_TERMINATORS: tuple[tuple[str, str], ...] = (
    ("\x0b", "VT"), ("\x0c", "FF"), ("\x1c", "FS"), ("\x1d", "GS"),
    ("\x1e", "RS"), ("\x85", "NEL"), ("\u2028", "LS"), ("\u2029", "PS"),
)
_SENTINEL_BASE = 0xE000  # Unicode private-use area; asserted absent from the raw text


def shield_nonstandard_line_terminators(text: str) -> tuple[str, dict[str, str]]:
    """Replace every non-newline line terminator by a private-use sentinel.

    Returns the shielded text and a ``{sentinel: original}`` map (empty when nothing was
    shielded).  Raises ``PatchEmissionError`` -- the could-not-check route, never a silent
    pass -- if a sentinel character is already present in the text.
    """

    if not isinstance(text, str):
        raise PatchEmissionError("patch is not a string")
    mapping: dict[str, str] = {}
    out = text
    for index, (char, _name) in enumerate(NONSTANDARD_LINE_TERMINATORS):
        sentinel = chr(_SENTINEL_BASE + index)
        if sentinel in text:
            raise PatchEmissionError(
                f"CANNOT_CHECK: private-use sentinel U+{ord(sentinel):04X} already present in the model output"
            )
        if char in out:
            out = out.replace(char, sentinel)
            mapping[sentinel] = char
    return out, mapping


def unshield_nonstandard_line_terminators(text: str, mapping: dict[str, str]) -> str:
    for sentinel, char in mapping.items():
        text = text.replace(sentinel, char)
    return text


def shielded_terminator_names(mapping: dict[str, str]) -> list[str]:
    names = dict(NONSTANDARD_LINE_TERMINATORS)
    return [names[char] for _s, char in mapping.items()]



class PatchEmissionError(ValueError):
    """The model output does not contain an extractable unified diff."""


@dataclass(frozen=True, slots=True)
class PatchEmission:
    """An emitted patch plus the audit trail of how it was produced."""

    patch: str
    receipt: dict[str, Any] = field(repr=False)

    @property
    def apply_clean_by_construction(self) -> bool:
        return self.receipt["emission_status"] == "APPLY_CLEAN_BY_CONSTRUCTION"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _is_body_line(line: str) -> bool:
    return line.startswith(_BODY_PREFIXES)


def extract_unified_diff(text: str) -> str:
    """Return the unified-diff body embedded in raw model output.

    Handles Markdown fences and leading prose, and drops trailing prose that cannot
    be a diff line. A trailing line beginning with ``-``/``+``/space stops the trim
    immediately, so a real edit line is never discarded. Raises
    ``PatchEmissionError`` when no diff is present.
    """

    if not isinstance(text, str):
        raise PatchEmissionError("patch is not a string")

    lines = text.splitlines()

    # A fenced block wins outright: take exactly what is between the fences.
    fences = [index for index, line in enumerate(lines) if _FENCE_RE.match(line)]
    if len(fences) >= 2:
        lines = lines[fences[0] + 1 : fences[1]]
    elif len(fences) == 1:
        lines = lines[fences[0] + 1 :] if fences[0] == 0 else lines[: fences[0]]

    start = None
    for index, line in enumerate(lines):
        if line.startswith("diff --git "):
            start = index
            break
        if (
            line.startswith("--- ")
            and index + 1 < len(lines)
            and lines[index + 1].startswith("+++ ")
        ):
            start = index
            break
    if start is None:
        raise PatchEmissionError("model output contains no unified diff")

    body = lines[start:]
    while body and not _is_body_line(body[-1]) and body[-1] != "":
        body.pop()
    if not body:
        raise PatchEmissionError("model output contains no unified diff")
    return "\n".join(body) + "\n"


def synthesize_diff_git_headers(patch: str) -> str:
    """Insert the ``diff --git`` header implied by an adjacent ``---``/``+++`` pair.

    The path is copied out of the ``---``/``+++`` lines the model already wrote; no
    path is ever guessed. Renames are rejected rather than represented.
    """

    lines = patch.splitlines(keepends=True)
    output: list[str] = []
    saw_file = False
    for index, line in enumerate(lines):
        if line.startswith("--- ") and index + 1 < len(lines) and lines[index + 1].startswith("+++ "):
            previous = output[-1] if output else ""
            old = line[4:].strip().removeprefix("a/")
            new = lines[index + 1][4:].strip().removeprefix("b/")
            if new != "/dev/null" and old != "/dev/null" and old != new:
                raise PatchEmissionError("diff renames a path; rename patches are outside this runner")
            path = new if old == "/dev/null" else old
            if not previous.startswith("diff --git "):
                output.append(f"diff --git a/{path} b/{path}\n")
            saw_file = True
        output.append(line)
    if not saw_file and not patch.startswith("diff --git "):
        raise PatchEmissionError("result is not a repository-rooted unified diff")
    return "".join(output)


def _git_apply_check(patch: str, workspace: Path) -> tuple[str, str]:
    """Return ``(status, stderr)`` for a non-mutating ``git apply --check``."""

    if shutil.which("git") is None:
        return "NOT_VERIFIED_NO_GIT", ""
    try:
        completed = subprocess.run(
            ["git", "apply", "--check", "--whitespace=nowarn", "-"],
            cwd=str(workspace),
            input=patch,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return "NOT_VERIFIED_GIT_FAILED", str(exc)[-2000:]
    return ("PASSED", "") if completed.returncode == 0 else ("FAILED", completed.stderr[-2000:])


def emit_apply_clean_patch(raw_text: str, *, workspace: Path | str | None = None) -> PatchEmission:
    """Canonicalize model-emitted patch text into an apply-clean unified diff.

    Returns the canonical patch when the frozen syntax-only canonicalizer accepts it,
    and otherwise the header-synthesized raw patch unchanged — emission never degrades
    an artifact it cannot canonicalize, and never silently drops one. ``workspace``,
    when it is an existing directory, is used only for a non-mutating
    ``git apply --check`` of both the raw and the emitted patch.
    """

    shielded_text, shield_map = shield_nonstandard_line_terminators(raw_text)
    extracted = extract_unified_diff(shielded_text)
    headed = synthesize_diff_git_headers(extracted)

    audit = audit_and_canonicalize_unified_diff(headed)
    canonicalizable = audit.valid_or_canonicalizable and audit.canonical_diff is not None
    emitted = audit.canonical_diff if canonicalizable else headed

    # Restore the shielded characters: every artifact hashed, checked or returned below is the
    # model's own bytes with newline-exact hunk counts, never the sentinel form.
    extracted = unshield_nonstandard_line_terminators(extracted, shield_map)
    headed = unshield_nonstandard_line_terminators(headed, shield_map)
    emitted = unshield_nonstandard_line_terminators(emitted, shield_map)

    directory = Path(workspace) if workspace is not None else None
    verifiable = directory is not None and directory.is_dir()

    def check(patch: str) -> tuple[str, str]:
        if directory is None or not verifiable:
            return "NOT_VERIFIED_NO_WORKSPACE", ""
        return _git_apply_check(patch, directory)

    raw_status, raw_error = check(headed)
    emitted_status, emitted_error = (raw_status, raw_error) if emitted == headed else check(emitted)

    if not canonicalizable:
        emission_status = "NOT_CANONICALIZABLE_EMITTED_UNCHANGED"
    elif emitted_status == "PASSED":
        emission_status = "APPLY_CLEAN_BY_CONSTRUCTION"
    elif emitted_status == "FAILED":
        emission_status = "CANONICAL_BUT_APPLY_CHECK_FAILED"
    else:
        emission_status = "CANONICAL_APPLY_CHECK_NOT_VERIFIED"

    receipt: dict[str, Any] = {
        "schema_version": EMISSION_SCHEMA_VERSION,
        "emission_status": emission_status,
        "raw_sha256": _sha256(raw_text),
        "extracted_sha256": _sha256(headed),
        "emitted_sha256": _sha256(emitted),
        "extraction_changed_raw": headed != raw_text,
        "diff_git_header_synthesized": headed != extracted,
        # Interface-fidelity endpoint, preserved so future runs can still report the
        # header-exact lane from the response alone. These three describe the
        # *extracted* artifact (``extracted_sha256``: post-extraction, post-header
        # synthesis, pre-canonicalization) — not ``raw_sha256``, which is the model
        # text before extraction. Extracted is the artifact directly comparable to
        # the archived GC1/GC2 raw lane, whose responses were likewise stored after
        # header synthesis.
        "extracted_was_header_exact": canonicalizable and not audit.changed,
        "extracted_was_apply_clean": {"PASSED": True, "FAILED": False}.get(raw_status),
        "extracted_apply_check": raw_status,
        "emitted_apply_check": emitted_status,
        "emitted_apply_check_error": emitted_error,
        "normalizations": list(audit.reasons),
        # R5 instrument repair (2026-09-05): line terminators git does not recognise were shielded
        # so that hunk counts are newline-exact.  Empty on every ordinary diff (the no-alarm case).
        "nonstandard_line_terminators_shielded": shielded_terminator_names(shield_map),
        "canonicalizer_rejection_reasons": [] if canonicalizable else list(audit.reasons),
        "authority": {
            "gold_or_fixed_patch_access": "FORBIDDEN_NOT_USED",
            "may_change_semantic_edit": False,
            "may_guess_paths": False,
            "may_relocate_hunks": False,
            "may_rescore_a_frozen_campaign": False,
        },
    }
    return PatchEmission(patch=emitted, receipt=receipt)
