"""Syntax-only audit/canonicalization for unified-diff agent artifacts.

This module deliberately does not infer edits, inspect gold patches, change file names,
or repair semantic content. It can only normalize representation details recoverable
from the patch itself: a/b file-header prefixes, blank context markers, and hunk line
counts. Use it as an arm-blind sensitivity interface, never to rewrite a protected
primary outcome after the fact.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

_DIFF_RE = re.compile(r"^diff --git a/(?P<a>.+) b/(?P<b>.+)$")
_HUNK_RE = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@(?P<tail>.*)$"
)


@dataclass(frozen=True, slots=True)
class UnifiedDiffAudit:
    valid_or_canonicalizable: bool
    changed: bool
    reasons: tuple[str, ...]
    canonical_diff: str | None


def _safe_relative_path(path: str) -> bool:
    return bool(path) and not path.startswith("/") and ".." not in path.split("/") and "\x00" not in path


def audit_and_canonicalize_unified_diff(text: str) -> UnifiedDiffAudit:
    """Return a syntax-only canonical form, or fail closed.

    Allowed normalizations are intentionally narrow:
    * ``--- path`` / ``+++ path`` -> ``--- a/path`` / ``+++ b/path`` only when
      the preceding ``diff --git`` header already binds the exact same path;
    * an empty hunk line -> one-space blank context line;
    * hunk old/new counts -> counts implied by the unchanged hunk body.

    Start line numbers, paths, added/removed/context text, and file multiplicity are
    never inferred or modified.
    """

    lines = text.splitlines()
    if not lines:
        return UnifiedDiffAudit(False, False, ("empty diff",), None)

    out: list[str] = []
    reasons: list[str] = []
    changed = False
    index = 0

    while index < len(lines):
        diff_match = _DIFF_RE.match(lines[index])
        if not diff_match:
            return UnifiedDiffAudit(
                False, changed, (f"expected diff --git header at line {index + 1}",), None
            )
        old_path = diff_match.group("a")
        new_path = diff_match.group("b")
        if old_path != new_path or not _safe_relative_path(old_path):
            return UnifiedDiffAudit(
                False, changed, (f"unsafe or mismatched file path at line {index + 1}",), None
            )
        out.append(lines[index])
        index += 1

        while index < len(lines) and not lines[index].startswith("--- "):
            if lines[index].startswith("diff --git "):
                return UnifiedDiffAudit(False, changed, ("missing ---/+++ headers",), None)
            out.append(lines[index])
            index += 1
        if index >= len(lines):
            return UnifiedDiffAudit(False, changed, ("missing --- header",), None)

        observed_old = lines[index][4:]
        if observed_old == old_path:
            observed_old = f"a/{old_path}"
            changed = True
            reasons.append(f"normalized old file header: {old_path}")
        elif observed_old != f"a/{old_path}":
            return UnifiedDiffAudit(
                False, changed, (f"old file header does not match diff header: {observed_old}",), None
            )
        out.append(f"--- {observed_old}")
        index += 1

        if index >= len(lines) or not lines[index].startswith("+++ "):
            return UnifiedDiffAudit(False, changed, ("missing +++ header",), None)
        observed_new = lines[index][4:]
        if observed_new == new_path:
            observed_new = f"b/{new_path}"
            changed = True
            reasons.append(f"normalized new file header: {new_path}")
        elif observed_new != f"b/{new_path}":
            return UnifiedDiffAudit(
                False, changed, (f"new file header does not match diff header: {observed_new}",), None
            )
        out.append(f"+++ {observed_new}")
        index += 1

        saw_hunk = False
        while index < len(lines) and not lines[index].startswith("diff --git "):
            hunk = _HUNK_RE.match(lines[index])
            if not hunk:
                return UnifiedDiffAudit(
                    False, changed, (f"expected hunk header at line {index + 1}",), None
                )
            saw_hunk = True
            header_index = len(out)
            out.append("")
            old_start = int(hunk.group("old_start"))
            new_start = int(hunk.group("new_start"))
            declared_old = int(hunk.group("old_count") or "1")
            declared_new = int(hunk.group("new_count") or "1")
            tail = hunk.group("tail")
            index += 1

            old_count = 0
            new_count = 0
            while (
                index < len(lines)
                and not lines[index].startswith("@@ ")
                and not lines[index].startswith("diff --git ")
            ):
                line = lines[index]
                if line == "":
                    line = " "
                    changed = True
                    reasons.append(f"normalized blank context marker at line {index + 1}")
                if line.startswith(" "):
                    old_count += 1
                    new_count += 1
                elif line.startswith("-"):
                    old_count += 1
                elif line.startswith("+"):
                    new_count += 1
                elif line.startswith("\\"):
                    pass
                else:
                    return UnifiedDiffAudit(
                        False, changed, (f"invalid hunk body line at {index + 1}",), None
                    )
                out.append(line)
                index += 1

            if (declared_old, declared_new) != (old_count, new_count):
                changed = True
                reasons.append(
                    "normalized hunk counts "
                    f"-{old_start}/+{new_start}: "
                    f"{declared_old},{declared_new}->{old_count},{new_count}"
                )
            out[header_index] = (
                f"@@ -{old_start},{old_count} +{new_start},{new_count} @@{tail}"
            )

        if not saw_hunk:
            return UnifiedDiffAudit(False, changed, (f"no hunks for {old_path}",), None)

    canonical = "\n".join(out) + ("\n" if text.endswith("\n") else "")
    return UnifiedDiffAudit(True, changed, tuple(reasons), canonical)
