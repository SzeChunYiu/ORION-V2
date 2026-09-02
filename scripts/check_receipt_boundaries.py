#!/usr/bin/env python3
"""Assert that receipts which mix machine output with hand-written commentary say so
machine-checkably, and that the machine-generated region is intact.

Background
----------
`PC_R6_OUTCOME_RECEIPT.md` carried a hand-written addendum below an HTML comment reading
"everything below is added at archive time and is not machine-generated". HTML comments do
not render, the boundary was not machine-readable, and two figures from the hand-written
half ("78-83%", "311/480 patch-apply rc=128") were quoted downstream as if they were
analysis output. One was wrong; the other was right but misattributed.

The convention this script enforces
-----------------------------------
A receipt that appends hand-written content to generated output declares the boundary::

    <!-- ORION-RECEIPT-BOUNDARY-V1
    generated_bytes: <N>
    generated_sha256: <64 hex>
    generator: <repo-relative path>
    checked_by: scripts/check_receipt_boundaries.py     # optional
    -->

and immediately follows it with a Markdown blockquote banner containing the phrase
``HAND-WRITTEN BELOW THIS LINE``. A blockquote renders; an HTML comment does not. The
declaration is verifiable: bytes ``[0:N]`` must hash to ``generated_sha256``, and only
whitespace or a horizontal rule may separate byte N from the marker.

What is checked
---------------
1. Every declaring file: digest, offset, and rendered banner.
2. Every ``*RECEIPT*.md`` that carries a prose boundary claim inside an HTML comment but no
   canonical marker -- the superseded, unverifiable style.

Exit codes
----------
0  checked, no violations
2  violations found
3  could not check (no candidate files, or a file could not be read) -- deliberately
   distinct from 0, so "could not check" is never reported as "checked and fine"

Self-test
---------
``--self-test`` runs positive and negative controls in a temp directory: a clean file must
pass, and a tampered digest, a missing banner, a marker at the wrong offset and a
prose-only boundary must each be caught. A checker that cannot fail is not a check.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tempfile
from pathlib import Path

MARKER_RE = re.compile(
    rb"<!--\s*ORION-RECEIPT-BOUNDARY-V1\s*\n(?P<body>.*?)-->",
    re.DOTALL,
)
FIELD_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*:\s*(\S.*?)\s*$")
BANNER_PHRASE = "HAND-WRITTEN BELOW THIS LINE"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# A fenced code block may legitimately *show* the marker (the convention doc does).
# Mask fenced regions with spaces before scanning, preserving byte offsets.
FENCE_RE = re.compile(rb"^(?P<fence>```+|~~~+)[^\n]*\n.*?^(?P=fence)[^\n]*$",
                      re.DOTALL | re.MULTILINE)


def _mask_code_fences(raw: bytes) -> bytes:
    out = bytearray(raw)
    for m in FENCE_RE.finditer(raw):
        for i in range(m.start(), m.end()):
            if out[i] != 0x0A:
                out[i] = 0x20
    return bytes(out)

# The superseded style: a boundary asserted in prose, inside an HTML comment.
LEGACY_PROSE_RE = re.compile(
    rb"<!--(?:(?!-->).)*?"
    rb"(?:is not machine-generated|not machine[- ]generated|added at archive time"
    rb"|verbatim output of)"
    rb"(?:(?!-->).)*?-->",
    re.DOTALL | re.IGNORECASE,
)

REQUIRED_FIELDS = ("generated_bytes", "generated_sha256", "generator")


class Violation(Exception):
    pass


def _parse_marker_body(body: bytes) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in body.decode("utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        m = FIELD_RE.match(line)
        if not m:
            raise Violation(f"marker line is not `key: value`: {line.strip()!r}")
        fields[m.group(1)] = m.group(2)
    return fields


def _check_declaring_file(path: Path, raw: bytes) -> list[str]:
    """Return violation messages for a file carrying the canonical marker."""
    problems: list[str] = []
    matches = list(MARKER_RE.finditer(_mask_code_fences(raw)))
    if len(matches) > 1:
        return [f"{path}: {len(matches)} ORION-RECEIPT-BOUNDARY-V1 markers; expected exactly 1"]

    match = matches[0]
    try:
        fields = _parse_marker_body(match.group("body"))
    except Violation as exc:
        return [f"{path}: {exc}"]

    missing = [f for f in REQUIRED_FIELDS if f not in fields]
    if missing:
        return [f"{path}: marker is missing required field(s): {', '.join(missing)}"]

    try:
        n = int(fields["generated_bytes"])
    except ValueError:
        return [f"{path}: generated_bytes is not an integer: {fields['generated_bytes']!r}"]
    if n <= 0:
        return [f"{path}: generated_bytes must be positive, got {n}"]

    declared = fields["generated_sha256"].lower()
    if not SHA256_RE.match(declared):
        return [f"{path}: generated_sha256 is not 64 lowercase hex digits: {declared!r}"]

    if len(raw) < n:
        return [f"{path}: generated_bytes={n} exceeds the file size ({len(raw)} bytes)"]

    actual = hashlib.sha256(raw[:n]).hexdigest()
    if actual != declared:
        problems.append(
            f"{path}: the machine-generated region has changed -- sha256 of bytes[0:{n}] "
            f"is {actual}, marker declares {declared}. Either the generated output was "
            f"hand-edited, or the marker was not updated when the generator re-ran."
        )

    start = match.start()
    if start < n:
        problems.append(
            f"{path}: the boundary marker starts at byte {start}, inside the declared "
            f"generated region [0:{n}]"
        )
    else:
        gap = raw[n:start].decode("utf-8", errors="replace")
        if gap.strip().strip("-") != "":
            problems.append(
                f"{path}: {len(raw[n:start])} bytes between the generated region and the "
                f"boundary marker are neither blank nor a horizontal rule: {gap.strip()[:80]!r}"
            )

    tail = raw[match.end():].decode("utf-8", errors="replace")
    banner = _leading_blockquote(tail)
    if banner is None:
        problems.append(
            f"{path}: no Markdown blockquote follows the boundary marker. An HTML comment "
            f"does not render; the hand-written region must be flagged in rendered output."
        )
    elif BANNER_PHRASE.lower() not in banner.lower():
        problems.append(
            f"{path}: the blockquote after the boundary marker does not contain "
            f"{BANNER_PHRASE!r}"
        )

    generator = fields["generator"]
    root = _repo_root(path)
    if root is not None and not (root / generator).exists():
        problems.append(
            f"{path}: generator {generator!r} does not resolve to a file under {root}"
        )

    return problems


def _repo_root(path: Path) -> Path | None:
    """Nearest ancestor containing `.git`, searched from the file then the cwd."""
    for start in (path.resolve().parent, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / ".git").exists():
                return candidate
    return None


def _leading_blockquote(text: str) -> str | None:
    """The first blockquote block in `text`, if only blank lines precede it."""
    lines: list[str] = []
    started = False
    for line in text.splitlines():
        if not started:
            if not line.strip():
                continue
            if not line.lstrip().startswith(">"):
                return None
            started = True
        elif not line.lstrip().startswith(">"):
            break
        lines.append(line)
    return "\n".join(lines) if started else None


def check_paths(paths: list[Path]) -> tuple[list[str], int]:
    """Return (violations, files_checked)."""
    violations: list[str] = []
    checked = 0
    for path in paths:
        raw = path.read_bytes()
        checked += 1
        masked = _mask_code_fences(raw)
        if MARKER_RE.search(masked):
            violations.extend(_check_declaring_file(path, raw))
        elif "RECEIPT" in path.name.upper() and LEGACY_PROSE_RE.search(masked):
            violations.append(
                f"{path}: declares a machine/hand-written boundary in prose inside an HTML "
                f"comment, with no ORION-RECEIPT-BOUNDARY-V1 marker. That boundary is neither "
                f"verifiable nor visible in rendered output -- see the module docstring."
            )
    return violations, checked


def _collect(roots: list[Path]) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        if root.is_file():
            out.append(root)
        else:
            out.extend(sorted(root.rglob("*.md")))
    return out


# --------------------------------------------------------------------------- self-test

_GOOD_HEAD = b"# receipt\n\nmachine output line\n"
_GOOD_BANNER = (
    "> ### HAND-WRITTEN BELOW THIS LINE\n"
    "> everything here was typed by a person.\n"
)


def _fixture(head: bytes, *, digest: str | None = None, n: int | None = None,
             banner: str = _GOOD_BANNER, gap: str = "\n---\n\n") -> bytes:
    n = len(head) if n is None else n
    digest = hashlib.sha256(head[:n]).hexdigest() if digest is None else digest
    marker = (
        "<!-- ORION-RECEIPT-BOUNDARY-V1\n"
        f"generated_bytes: {n}\n"
        f"generated_sha256: {digest}\n"
        "generator: scripts/check_receipt_boundaries.py\n"
        "-->\n\n"
    )
    return head + gap.encode() + marker.encode() + banner.encode()


def self_test() -> int:
    cases: list[tuple[str, bytes, bool]] = [
        ("clean file passes", _fixture(_GOOD_HEAD), False),
        ("tampered generated region caught",
         _fixture(_GOOD_HEAD, digest="0" * 64), True),
        ("missing rendered banner caught",
         _fixture(_GOOD_HEAD, banner="plain paragraph, not a blockquote\n"), True),
        ("banner without the required phrase caught",
         _fixture(_GOOD_HEAD, banner="> some other note\n"), True),
        ("content smuggled between region and marker caught",
         _fixture(_GOOD_HEAD, gap="\nan extra hand-written sentence\n\n"), True),
        ("generated_bytes past EOF caught",
         _fixture(_GOOD_HEAD, n=len(_GOOD_HEAD), digest=hashlib.sha256(_GOOD_HEAD).hexdigest())
         .replace(b"generated_bytes: %d" % len(_GOOD_HEAD), b"generated_bytes: 99999"), True),
        ("malformed digest caught",
         _fixture(_GOOD_HEAD, digest="not-a-digest"), True),
        ("prose-only boundary in a RECEIPT file caught",
         b"# r\n\ntext\n\n<!-- everything below is not machine-generated -->\n\nmore\n", True),
        ("marker shown inside a fenced code block does not alarm",
         b"# doc\n\n```\n<!-- ORION-RECEIPT-BOUNDARY-V1\ngenerated_bytes: <N>\n-->\n```\n",
         False),
        ("prose boundary shown inside a fenced code block does not alarm",
         b"# doc\n\n~~~\n<!-- not machine-generated -->\n~~~\n", False),
    ]
    failures = 0
    with tempfile.TemporaryDirectory() as td:
        # A self-contained fake repository, so the controls do not depend on the cwd.
        (Path(td) / ".git").mkdir()
        (Path(td) / "scripts").mkdir()
        (Path(td) / "scripts" / "check_receipt_boundaries.py").write_text("stub\n")
        for i, (name, content, should_fail) in enumerate(cases):
            p = Path(td) / f"CASE_{i}_RECEIPT.md"
            p.write_bytes(content)
            violations, checked = check_paths([p])
            got = bool(violations)
            ok = got == should_fail and checked == 1
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}"
                  + ("" if ok else f"  (expected fail={should_fail}, got {violations})"))
            failures += 0 if ok else 1

        # A prose boundary outside a RECEIPT-named file must NOT alarm: the no-alarm case
        # is asserted explicitly, so the checker cannot pass by crying wolf.
        p = Path(td) / "NOTES.md"
        p.write_bytes(b"<!-- this section is not machine-generated -->\n")
        violations, _ = check_paths([p])
        ok = not violations
        print(f"  [{'PASS' if ok else 'FAIL'}] non-receipt prose does not alarm")
        failures += 0 if ok else 1

    print(f"self-test: {failures} failure(s)")
    return 0 if failures == 0 else 2


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("roots", nargs="*", default=["research"], type=Path,
                    help="files or directories to scan (default: research)")
    ap.add_argument("--self-test", action="store_true",
                    help="run the checker's own positive and negative controls and exit")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    roots = [r for r in args.roots]
    missing = [r for r in roots if not r.exists()]
    if missing:
        print(f"COULD NOT CHECK: path(s) do not exist: {', '.join(map(str, missing))}",
              file=sys.stderr)
        return 3

    paths = _collect(roots)
    if not paths:
        print("COULD NOT CHECK: no Markdown files found under "
              f"{', '.join(map(str, roots))}", file=sys.stderr)
        return 3

    try:
        violations, checked = check_paths(paths)
    except OSError as exc:
        print(f"COULD NOT CHECK: {exc}", file=sys.stderr)
        return 3

    declaring = sum(1 for p in paths if MARKER_RE.search(_mask_code_fences(p.read_bytes())))
    if violations:
        print(f"receipt-boundary check FAILED ({len(violations)} violation(s); "
              f"{checked} file(s) scanned, {declaring} declaring the marker):")
        for v in violations:
            print(f"  - {v}")
        return 2

    print(f"receipt-boundary check OK: {checked} Markdown file(s) scanned, "
          f"{declaring} declaring ORION-RECEIPT-BOUNDARY-V1, 0 violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
