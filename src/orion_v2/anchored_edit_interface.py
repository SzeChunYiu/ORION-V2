"""Arm-side anchored-edit interface: locate-by-content edits, emitted as a canonical diff.

Why this module exists
----------------------
E30-R13 (``research/experiments/e30-r13/E30_R13_OUTCOME_RECEIPT.md``) completed 480/480
envelopes under a registered channel contract and still could not test repair: 346 of
the 480 emitted unified diffs did not apply (GR1 ``APPLY_RATE_DIAGNOSTIC`` failed on all
four arms, apply-failure 0.69-0.78 against a 0.40 ceiling).  The read-only decomposition
of those 346 archived envelopes (``research/experiments/e30-r14/results/
E30_R14_R13_APPLY_FAILURE_ATTRIBUTION_V1.json``) put the failure in the *interface*, in
two places:

* **emission** -- 141 patches were refused by the frozen syntax canonicalizer for
  forms a unified diff can carry but the canonicalizer does not accept: duplicated
  ``diff --git`` headers with ``index``/``new file mode`` lines (95), numberless
  ``@@ def f(): @@`` anchors (45), ``--- /dev/null`` new-file headers (35); and 145 of
  the 346 locate uniquely by their own context or removed lines and apply once
  relocated;
* **presentation** -- 152 of the 205 canonical-but-non-applying patches edit a region
  of a file the model was never shown, because the workspace snapshot truncates every
  file at 30 000 characters, so the context the model "quoted" was invented.

A unified diff asks the model for three things at once: the edit, verbatim context,
and line arithmetic.  Only the first is the experiment.  This interface asks for the
edit anchored by a verbatim ``search`` block, locates that block in the gold-blind
solver workspace, and *derives* the unified diff -- context and counts included -- from
the file itself.  It is the edit contract that the leading agent harnesses converged
on (search/replace blocks, ``str_replace`` editors); nothing here is novel and nothing
here is a repair mechanism.

What it may and may not do
--------------------------
* It reads only the solver workspace files the model's edits name.  It never opens a
  gold, fixed or reference patch and never invents a path.
* It never alters the replacement text the model wrote, except to shift its
  indentation by the exact offset at which the ``search`` block was found when the
  match was made with leading whitespace collapsed (recorded in the receipt).
* It never chooses between two candidate locations: an ambiguous ``search`` is an
  unlocated edit, and an unlocated edit is reported, not guessed.
* It never partially applies: if any edit of a response cannot be located, no patch is
  emitted for that response and the receipt says which edit failed and why.
* It never mutates the workspace: the diff is produced by ``git diff --no-index``
  against a temporary copy and verified with ``git apply --check``.

The response contract is preserved: ``proposed_patch_or_artifact.content`` is still a
unified diff (the evaluator's ``git apply`` invocation is untouched) and the receipt
keeps ``orion.v2.patch-emission.v1`` with additive fields, so the response validator
and every archived response are unaffected.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import hashlib
import os
import re
import shutil
import subprocess
import tempfile

from orion_v2.patch_emission import EMISSION_SCHEMA_VERSION, PatchEmission, _sha256

EDIT_INTERFACE_ID = "anchored_edits.v1"

#: Matching modes, tried in this order.  Each is a syntax-level relaxation of the one
#: before it; none reads the meaning of a line.
MATCH_MODES = ("exact", "rstrip", "collapsed_whitespace")

_HUNK_NUMBERED = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")
_DIFF_GIT = re.compile(r"^diff --git a/(.+) b/(.+)$")


class AnchoredEditError(ValueError):
    """The model output does not contain an extractable edit list."""


@dataclass(frozen=True, slots=True)
class Edit:
    path: str
    search: str | None          # None => create a new file
    replace: str
    origin: str = "edits"       # "edits" (native) or "unified_diff_fallback"


@dataclass(slots=True)
class Located:
    edit: Edit
    start: int                  # 0-based line index into the original file
    length: int                 # number of original lines replaced
    mode: str
    indent_shift: int
    replacement_lines: list[str] = field(default_factory=list)


# ---- extraction ------------------------------------------------------------------------


def _safe_relative_path(path: str) -> bool:
    return bool(path) and not path.startswith("/") and ".." not in path.split("/") and "\x00" not in path


def edits_from_model_object(data: dict[str, Any]) -> list[Edit]:
    """Read the native ``edits`` list; fall back to a unified ``patch`` string.

    The fallback exists so a model that ignores the instruction and emits a diff anyway
    is not scored as an empty response: each hunk becomes a search/replace pair and is
    located by content like any other edit.  Which path was taken is recorded.
    """

    raw_edits = data.get("edits")
    if isinstance(raw_edits, list) and raw_edits:
        out: list[Edit] = []
        for index, item in enumerate(raw_edits):
            if not isinstance(item, dict):
                raise AnchoredEditError(f"edit {index} is not an object")
            path = str(item.get("path", "")).strip().removeprefix("a/").removeprefix("b/")
            if not _safe_relative_path(path):
                raise AnchoredEditError(f"edit {index} names an unsafe or empty path")
            create = bool(item.get("create", False))
            search = item.get("search")
            replace = item.get("replace", "")
            if not isinstance(replace, str):
                raise AnchoredEditError(f"edit {index} replace is not a string")
            if create:
                out.append(Edit(path=path, search=None, replace=replace))
                continue
            if not isinstance(search, str) or not search.strip():
                raise AnchoredEditError(f"edit {index} has no search block and is not a create")
            out.append(Edit(path=path, search=search, replace=replace))
        return out
    patch = data.get("patch")
    if isinstance(patch, str) and patch.strip():
        return edits_from_unified_diff(patch)
    raise AnchoredEditError("model JSON carries neither an edits list nor a unified diff patch")


def edits_from_unified_diff(text: str) -> list[Edit]:
    """Lenient hunk reader: every hunk becomes (old block -> new block).

    Tolerates the forms E30-R13's models actually emitted -- duplicated ``diff --git``
    headers, ``index``/mode metadata lines, numberless ``@@`` anchors, ``/dev/null``
    new-file headers, Markdown fences, and body lines whose leading space was dropped.
    It reads no line's meaning: a hunk body is split by its first character only.
    """

    lines = [line for line in text.splitlines() if not re.match(r"^\s*```", line)]
    edits: list[Edit] = []
    path: str | None = None
    is_new = False
    index = 0
    while index < len(lines):
        line = lines[index]
        match = _DIFF_GIT.match(line)
        if match:
            path = match.group(2).strip()
            is_new = False
            index += 1
            continue
        if line.startswith("--- "):
            marker = line[4:].strip()
            if marker in ("/dev/null", "a/dev/null", "dev/null"):
                is_new = True
            else:
                candidate = marker.removeprefix("a/")
                if path is None or path != candidate:
                    path = candidate
            index += 1
            continue
        if line.startswith("+++ "):
            candidate = line[4:].strip().removeprefix("b/")
            if candidate not in ("/dev/null", "dev/null"):
                path = candidate
            index += 1
            continue
        if line.startswith(("index ", "new file mode", "deleted file mode", "old mode", "new mode",
                            "similarity index", "rename from", "rename to")):
            index += 1
            continue
        if line.startswith("@@"):
            index += 1
            old: list[str] = []
            new: list[str] = []
            while index < len(lines) and not lines[index].startswith(("@@", "diff --git ", "--- ", "+++ ")):
                body = lines[index]
                if body == "":
                    body = " "
                prefix, rest = body[0], body[1:]
                if prefix == " ":
                    old.append(rest)
                    new.append(rest)
                elif prefix == "-":
                    old.append(rest)
                elif prefix == "+":
                    new.append(rest)
                elif prefix == "\\":
                    pass
                else:
                    old.append(body)   # dropped leading space: context
                    new.append(body)
                index += 1
            if path is None:
                raise AnchoredEditError("hunk appears before any file header")
            if not _safe_relative_path(path):
                raise AnchoredEditError("unsafe or empty path in unified diff")
            if is_new and not old:
                edits.append(Edit(path=path, search=None, replace="\n".join(new) + "\n",
                                  origin="unified_diff_fallback"))
            elif not old:
                raise AnchoredEditError(f"hunk for {path} has no context and no removed lines; it cannot be anchored")
            else:
                edits.append(Edit(path=path, search="\n".join(old) + "\n", replace="\n".join(new) + "\n",
                                  origin="unified_diff_fallback"))
            continue
        index += 1
    if not edits:
        raise AnchoredEditError("unified diff contains no hunks")
    return edits


# ---- location ----------------------------------------------------------------------------


def _key(mode: str, line: str) -> str:
    if mode == "exact":
        return line
    if mode == "rstrip":
        return line.rstrip()
    return " ".join(line.split())


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" \t"))


def locate_block(file_lines: list[str], search_lines: list[str]) -> tuple[list[int], str]:
    """Return ``(starts, mode)`` for the first mode with at least one match.

    ``starts`` may hold more than one index: ambiguity is reported to the caller, never
    resolved here.  An empty ``search`` never matches.
    """

    if not search_lines:
        return [], "none"
    for mode in MATCH_MODES:
        target = [_key(mode, s) for s in search_lines]
        if mode == "collapsed_whitespace" and all(t == "" for t in target):
            continue
        keyed = [_key(mode, f) for f in file_lines]
        n = len(target)
        hits = [i for i in range(len(keyed) - n + 1) if keyed[i:i + n] == target]
        if hits:
            return hits, mode
    return [], "none"


def _reindent(replacement: list[str], shift: int) -> list[str]:
    if shift == 0:
        return list(replacement)
    out: list[str] = []
    for line in replacement:
        if not line.strip():
            out.append(line)
        elif shift > 0:
            out.append(" " * shift + line)
        else:
            cut = min(-shift, _indent(line))
            out.append(line[cut:])
    return out


def locate_edits(workspace: Path, edits: list[Edit]) -> tuple[list[Located], list[dict[str, Any]]]:
    """Locate every edit against the ORIGINAL file contents; report every failure."""

    located: list[Located] = []
    failures: list[dict[str, Any]] = []
    contents: dict[str, list[str] | None] = {}
    for number, edit in enumerate(edits):
        target = workspace / edit.path
        if edit.path not in contents:
            if target.is_file():
                contents[edit.path] = target.read_text(encoding="utf-8", errors="replace").splitlines()
            else:
                contents[edit.path] = None
        file_lines = contents[edit.path]
        replacement_lines = edit.replace.splitlines()
        if edit.search is None:
            if file_lines is not None:
                failures.append({"edit": number, "path": edit.path, "reason": "CREATE_TARGET_EXISTS"})
                continue
            located.append(Located(edit, 0, 0, "create", 0, replacement_lines))
            continue
        if file_lines is None:
            failures.append({"edit": number, "path": edit.path, "reason": "PATH_NOT_IN_WORKSPACE"})
            continue
        search_lines = edit.search.splitlines()
        while search_lines and search_lines[-1] == "":
            search_lines.pop()
        hits, mode = locate_block(file_lines, search_lines)
        if not hits:
            failures.append({
                "edit": number, "path": edit.path, "reason": "SEARCH_NOT_FOUND",
                "search_lines": len(search_lines),
                "search_lines_present_individually": sum(
                    1 for s in search_lines if _key("collapsed_whitespace", s) in
                    {_key("collapsed_whitespace", f) for f in file_lines}),
            })
            continue
        if len(hits) > 1:
            failures.append({"edit": number, "path": edit.path, "reason": "SEARCH_AMBIGUOUS",
                             "occurrences": len(hits), "mode": mode})
            continue
        start = hits[0]
        shift = 0
        if mode == "collapsed_whitespace":
            deltas = {
                _indent(file_lines[start + j]) - _indent(search_lines[j])
                for j in range(len(search_lines)) if search_lines[j].strip()
            }
            shift = deltas.pop() if len(deltas) == 1 else 0
        located.append(Located(edit, start, len(search_lines), mode, shift,
                               _reindent(replacement_lines, shift)))
    # overlapping edits on one file are a model error, not something to resolve
    by_path: dict[str, list[Located]] = {}
    for item in located:
        by_path.setdefault(item.edit.path, []).append(item)
    for path, items in by_path.items():
        spans = sorted((i.start, i.start + i.length, k) for k, i in enumerate(items) if i.mode != "create")
        for (a0, a1, _), (b0, b1, _) in zip(spans, spans[1:]):
            if b0 < a1:
                failures.append({"path": path, "reason": "EDITS_OVERLAP", "spans": [[a0, a1], [b0, b1]]})
                break
    return located, failures


# ---- materialization ---------------------------------------------------------------------


def _git(args: list[str], cwd: Path, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=str(cwd), input=stdin, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=120)


def render_unified_diff(workspace: Path, located: list[Located]) -> str:
    """Derive the canonical diff from the files themselves with ``git diff --no-index``.

    The workspace is never written.  Context lines and hunk counts therefore come from
    the real file, which is the whole point: the model supplied the edit, git supplies
    the serialization.
    """

    by_path: dict[str, list[Located]] = {}
    for item in located:
        by_path.setdefault(item.edit.path, []).append(item)
    parts: list[str] = []
    with tempfile.TemporaryDirectory(prefix="orion-anchored-") as tmp:
        for path in sorted(by_path):
            items = by_path[path]
            original = workspace / path
            if any(i.mode == "create" for i in items):
                new_text = "".join(line + "\n" for line in items[0].replacement_lines)
                old_text = None
            else:
                raw = original.read_text(encoding="utf-8", errors="replace")
                lines = raw.splitlines()
                for item in sorted(items, key=lambda i: i.start, reverse=True):
                    lines[item.start:item.start + item.length] = item.replacement_lines
                new_text = "\n".join(lines) + ("\n" if raw.endswith("\n") or not raw else "")
                old_text = raw
            new_file = Path(tmp) / "new" / path
            new_file.parent.mkdir(parents=True, exist_ok=True)
            new_file.write_text(new_text, encoding="utf-8")
            if old_text is None:
                completed = _git(["diff", "--no-index", "--", os.devnull, str(new_file)], cwd=Path(tmp))
            else:
                old_file = Path(tmp) / "old" / path
                old_file.parent.mkdir(parents=True, exist_ok=True)
                old_file.write_text(old_text, encoding="utf-8")
                completed = _git(["diff", "--no-index", "--", str(old_file), str(new_file)], cwd=Path(tmp))
            if completed.returncode not in (0, 1):
                raise AnchoredEditError(f"git diff failed for {path}: {completed.stderr[-500:]}")
            out = completed.stdout
            if not out.strip():
                continue    # the edit was a no-op for this file
            out_lines = out.splitlines()
            rewritten: list[str] = []
            for line in out_lines:
                if line.startswith("diff --git "):
                    rewritten.append(f"diff --git a/{path} b/{path}")
                elif line.startswith("index "):
                    continue    # blob ids of temporary copies carry no information
                elif line.startswith("--- ") and not line.startswith("--- /dev/null"):
                    rewritten.append(f"--- a/{path}")
                elif line.startswith("+++ "):
                    rewritten.append(f"+++ b/{path}")
                else:
                    rewritten.append(line)
            parts.append("\n".join(rewritten) + "\n")
    return "".join(parts)


def _git_apply_check(patch: str, workspace: Path) -> tuple[str, str]:
    if shutil.which("git") is None:
        return "NOT_VERIFIED_NO_GIT", ""
    try:
        completed = _git(["apply", "--check", "--whitespace=nowarn", "-"], cwd=workspace, stdin=patch)
    except (OSError, subprocess.SubprocessError) as exc:
        return "NOT_VERIFIED_GIT_FAILED", str(exc)[-2000:]
    return ("PASSED", "") if completed.returncode == 0 else ("FAILED", completed.stderr[-2000:])


def interface_source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def emit_anchored_edit_patch(data: dict[str, Any], *, workspace: Path | str) -> PatchEmission:
    """Locate the model's edits in ``workspace`` and emit the derived unified diff.

    Emission statuses:

    * ``APPLY_CLEAN_BY_CONSTRUCTION`` -- every edit located, diff derived, ``git apply
      --check`` passed;
    * ``EDITS_NOT_LOCATED`` -- at least one edit could not be located (not found,
      ambiguous, missing path, overlap); **no patch is emitted** and the failures are
      listed;
    * ``DERIVED_BUT_APPLY_CHECK_FAILED`` -- should not occur (the diff is derived from
      the file); kept so a defect here is reported rather than hidden;
    * ``DERIVED_APPLY_CHECK_NOT_VERIFIED`` -- git unavailable.
    """

    directory = Path(workspace)
    if not directory.is_dir():
        raise AnchoredEditError(f"solver workspace is not a directory: {directory}")
    edits = edits_from_model_object(data)
    located, failures = locate_edits(directory, edits)
    raw_text = data.get("patch") if isinstance(data.get("patch"), str) else None
    raw_sha = _sha256(raw_text if raw_text is not None else _stable_json(data.get("edits")))
    if failures:
        patch = ""
        status = "EDITS_NOT_LOCATED"
        apply_status, apply_error = "NOT_RUN_NO_PATCH", ""
    else:
        patch = render_unified_diff(directory, located)
        if not patch.strip():
            status = "EDITS_NOT_LOCATED"
            failures = [{"reason": "EDITS_ARE_A_NO_OP"}]
            apply_status, apply_error = "NOT_RUN_NO_PATCH", ""
        else:
            apply_status, apply_error = _git_apply_check(patch, directory)
            status = {"PASSED": "APPLY_CLEAN_BY_CONSTRUCTION",
                      "FAILED": "DERIVED_BUT_APPLY_CHECK_FAILED"}.get(apply_status, "DERIVED_APPLY_CHECK_NOT_VERIFIED")
    receipt: dict[str, Any] = {
        "schema_version": EMISSION_SCHEMA_VERSION,
        "emission_status": status,
        "edit_interface": EDIT_INTERFACE_ID,
        "edit_interface_source_sha256": interface_source_sha256(),
        "raw_sha256": raw_sha,
        "extracted_sha256": raw_sha,
        "emitted_sha256": _sha256(patch),
        "extraction_changed_raw": True,
        "diff_git_header_synthesized": True,
        # The raw header-exact lane has no referent when the model emits edits rather
        # than a diff; it is reported as such instead of as True or False.
        "extracted_was_header_exact": False,
        "extracted_was_apply_clean": None,
        "extracted_apply_check": "NOT_APPLICABLE_ANCHORED_EDITS",
        "emitted_apply_check": apply_status,
        "emitted_apply_check_error": apply_error,
        "normalizations": [f"{item.mode}:{item.edit.path}:{item.start}:{item.indent_shift}" for item in located],
        "canonicalizer_rejection_reasons": [],
        "edit_count": len(edits),
        "edits_located": len(located),
        "edit_origins": sorted({e.origin for e in edits}),
        "match_modes": {mode: sum(1 for i in located if i.mode == mode) for mode in (*MATCH_MODES, "create")},
        "unlocated_edits": failures,
        "authority": {
            "gold_or_fixed_patch_access": "FORBIDDEN_NOT_USED",
            "may_change_semantic_edit": False,
            "may_guess_paths": False,
            "may_relocate_hunks": False,
            "may_rescore_a_frozen_campaign": False,
            "locates_search_blocks_by_verbatim_content": True,
            "resolves_ambiguous_search_blocks": False,
            "partial_application": False,
        },
    }
    return PatchEmission(patch=patch, receipt=receipt)


def _stable_json(value: Any) -> str:
    import json
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
