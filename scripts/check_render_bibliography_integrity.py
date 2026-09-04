#!/usr/bin/env python3
"""Render-integrity gate for compiled LaTeX release packages.

Motivation
----------
A ``bibliography_item_count > 0`` assertion is a *presence* test wearing a
*coverage* test's name: a bibliography that silently dropped 18 of 41 entries
still satisfies it.  This module replaces presence with three independent,
mutually non-redundant reads of the real build tree:

1. **De-wrapped ``.log`` scan.**  pdfTeX wraps its transcript at
   ``max_print_line`` (79 by default) *mid-word*, so a raw ``grep`` for
   ``Citation .* undefined`` returns a **false clean** on a long warning line.
   The log is de-wrapped before any pattern is applied, and the wrap state is
   recorded so a silent de-wrap failure is visible rather than assumed.

2. **``.blg`` scan.**  BibTeX records
   ``Warning--I didn't find a database entry for ...`` in its own transcript.
   This is the *only* signal in a stale-``.bbl`` build: when a stale ``.bbl``
   is restored after BibTeX ran, LaTeX resolves every ``\\cite`` from the stale
   file, the ``.log`` is completely silent, the page count is unchanged, and
   the build exits 0.

3. **``.aux`` -> ``.bbl`` coverage relation.**  Every key LaTeX actually cited
   must have a corresponding ``\\bibitem`` in the rendered bibliography.  This
   is the set relation that ``count > 0`` failed to express.

No check here is of the form "the log mentions X, therefore X loaded": a
failure message routinely contains the name of the thing that failed, so such
assertions invert.  Every pattern below matches a *failure*, never a success.

Exit codes
----------
0  PASS          - every requested package checked, no defect found.
1  FAIL          - a defect was found.
3  CANNOT_CHECK  - the check could not be performed (missing transcript,
                   indeterminate wrap state, no citations to check).  This is
                   deliberately distinct from FAIL: "could not check" must
                   never be reported as "checked and fine", nor as "failed".
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_CANNOT_CHECK = 3

DEFAULT_WRAP_WIDTH = 79  # pdfTeX max_print_line default

# --- failure patterns -------------------------------------------------------
# Applied to the DE-WRAPPED log only.  Each matches a failure message; none
# asserts "mentions X therefore X is fine".
LOG_FAILURE_PATTERNS: dict[str, str] = {
    "undefined_citation": r"Citation\s+[`'\"]?[^'\"\s]+['\"]?\s+(?:on page\s+\S+\s+)?undefined",
    "undefined_reference": r"Reference\s+[`'\"]?[^'\"\s]+['\"]?\s+(?:on page\s+\S+\s+)?undefined",
    "undefined_references_summary": r"There were undefined references",
    "undefined_citations_summary": r"There were undefined citations",
    "natbib_undefined": r"Package natbib Warning:\s*Citation\s+[`'\"]?[^'\"\s]+['\"]?\s+undefined",
    "no_bbl": r"No file [^\s]*\.bbl",
    "emergency_stop": r"Emergency stop",
    "latex_error": r"^! LaTeX Error:",
}

# Applied to the .blg (BibTeX transcript).  ``didn't`` is the exact BibTeX
# spelling, apostrophe included; it is matched permissively for the apostrophe
# so a Unicode-normalised transcript cannot slip through.
BLG_FAILURE_PATTERNS: dict[str, str] = {
    "missing_database_entry": r"Warning--I didn.t find a database entry for",
    "database_file_unopenable": r"I couldn.t open database file",
    "style_file_unopenable": r"I couldn.t open style file",
    "no_citation_commands": r"I found no \\citation commands",
    "no_bibdata_command": r"I found no \\bibdata command",
    "empty_field_fatal": r"Warning--empty (?:author|title) in",
    "bibtex_error_messages": r"\(There (?:were|was) \d+ error message",
}


# --- helpers ----------------------------------------------------------------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_transcript(path: Path) -> str:
    """TeX transcripts are not reliably UTF-8; decode losslessly."""
    return path.read_bytes().decode("utf-8", errors="replace")


def dewrap(text: str) -> tuple[str, dict[str, object]]:
    """Undo pdfTeX's fixed-column line wrapping.

    pdfTeX breaks the transcript at exactly ``max_print_line`` characters,
    mid-word and without a hyphen, so ``Citation `key' undefined`` can be split
    across two physical lines and evade a raw grep.  Any line whose length is
    exactly a detected wrap width is joined to its successor with no separator,
    reconstructing the logical line.

    The wrap width is *detected* rather than assumed: ``max_print_line`` is
    configurable, and a hard-coded 79 would silently reproduce the very
    blindness this gate exists to close.  Over-joining is safe -- joining lines
    can only ever add candidate matches, never erase a true one.
    """
    lines = text.split("\n")
    lengths = [len(line) for line in lines]
    max_len = max(lengths) if lengths else 0

    widths: set[int] = {DEFAULT_WRAP_WIDTH}
    # A real wrap width shows up as many lines of exactly that length.
    if max_len >= 60 and lengths.count(max_len) >= 2:
        widths.add(max_len)

    out: list[str] = []
    joins = 0
    buf: str | None = None
    for line in lines:
        buf = line if buf is None else buf + line
        if len(line) in widths:
            joins += 1
            continue
        out.append(buf)
        buf = None
    if buf is not None:
        out.append(buf)

    if max_len == 0:
        wrap_state = "EMPTY"
    elif joins > 0:
        wrap_state = "WRAPPED_AND_DEWRAPPED"
    elif max_len < DEFAULT_WRAP_WIDTH:
        wrap_state = "NOT_WRAPPED"
    else:
        # Long lines exist but none sits on a detected width boundary.
        wrap_state = "NOT_WRAPPED"

    meta = {
        "raw_line_count": len(lines),
        "dewrapped_line_count": len(out),
        "max_raw_line_length": max_len,
        "detected_wrap_widths": sorted(widths),
        "lines_at_wrap_width": sum(1 for n in lengths if n in widths),
        "dewrap_joins_applied": joins,
        "wrap_state": wrap_state,
    }
    return "\n".join(out), meta


def scan(text: str, patterns: dict[str, str]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for name, pattern in patterns.items():
        found = re.findall(pattern, text, flags=re.MULTILINE)
        if found:
            # ``findall`` returns tuples when a pattern has groups; normalise.
            hits[name] = [m if isinstance(m, str) else " ".join(m) for m in found][:50]
    return hits


def parse_aux_citations(aux_text: str) -> set[str]:
    """Collect keys LaTeX actually emitted ``\\citation{}`` for.

    ``\\nocite{*}`` emits ``\\citation{*}``, which names no key and is dropped.
    """
    keys: set[str] = set()
    for group in re.findall(r"\\citation\{([^}]*)\}", aux_text):
        for key in group.split(","):
            key = key.strip()
            if key and key != "*":
                keys.add(key)
    return keys


def parse_bibitem_keys(bbl_text: str) -> list[str]:
    """Extract ``\\bibitem`` keys with brace/bracket balancing.

    natbib emits ``\\bibitem[Ab{\\'a}s(2020)]{key}``: the optional argument can
    contain braces and the key group follows it.  A naive ``\\[[^\\]]*\\]`` regex
    mis-parses those, so the optional argument is skipped by scanning with
    depth counters instead.
    """
    keys: list[str] = []
    i = 0
    token = "\\bibitem"
    while True:
        i = bbl_text.find(token, i)
        if i < 0:
            break
        j = i + len(token)
        while j < len(bbl_text) and bbl_text[j] in " \t\r\n":
            j += 1
        if j < len(bbl_text) and bbl_text[j] == "[":  # skip optional argument
            depth = 0
            while j < len(bbl_text):
                ch = bbl_text[j]
                if ch == "[":
                    depth += 1
                elif ch == "]":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            while j < len(bbl_text) and bbl_text[j] in " \t\r\n":
                j += 1
        if j < len(bbl_text) and bbl_text[j] == "{":
            depth = 0
            start = j + 1
            while j < len(bbl_text):
                ch = bbl_text[j]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        keys.append(bbl_text[start:j].strip())
                        j += 1
                        break
                j += 1
        i = j if j > i else i + len(token)
    return keys


def parse_registry_canonical_sources(registry: Path) -> list[str]:
    """Read the canonical public source path declared for each paper.

    The index states one canonical source per surviving paper as a backticked
    repository path under a "Canonical public source" heading.
    """
    text = registry.read_text(encoding="utf-8")
    sources: list[str] = []
    for match in re.finditer(r"Canonical public source[^\n]*\n(.*?)(?=\n#{1,3} |\Z)", text, flags=re.S):
        for path in re.findall(r"`([^`]+\.(?:md|tex))`", match.group(1)):
            path = path.strip()
            # The prose in a block may also backtick non-source documents (e.g.
            # a claim gate). Only a repository path can be a canonical source,
            # and only the first one in the block is the declared source.
            if "/" in path:
                sources.append(path)
                break
    return sources


# --- per-package check ------------------------------------------------------
def check_package(
    package: Path,
    *,
    stem: str = "manuscript",
    expect_citations: bool = True,
) -> dict[str, object]:
    """Check one compiled package directory. Never raises on a build defect."""
    package = Path(package)
    result: dict[str, object] = {
        "package": str(package),
        "stem": stem,
        "status": "PASS",
        "failures": [],
        "cannot_check": [],
    }
    failures: list[str] = result["failures"]  # type: ignore[assignment]
    cannot: list[str] = result["cannot_check"]  # type: ignore[assignment]

    log_path = package / f"{stem}.log"
    blg_path = package / f"{stem}.blg"
    bbl_path = package / f"{stem}.bbl"

    # 1. de-wrapped log ------------------------------------------------------
    if not log_path.exists():
        cannot.append(f"missing LaTeX transcript: {log_path}")
        result["log"] = None
    else:
        raw = read_transcript(log_path)
        dewrapped, meta = dewrap(raw)
        raw_hits = scan(raw, LOG_FAILURE_PATTERNS)
        dew_hits = scan(dewrapped, LOG_FAILURE_PATTERNS)
        meta.update(
            {
                "sha256": sha256_file(log_path),
                "raw_scan_hits": raw_hits,
                "dewrapped_scan_hits": dew_hits,
                # Evidence that de-wrapping is load-bearing on this build, not
                # decorative: findings the raw scan missed.
                "hits_visible_only_after_dewrap": sorted(set(dew_hits) - set(raw_hits)),
            }
        )
        result["log"] = meta
        if meta["wrap_state"] == "EMPTY":
            cannot.append(f"empty LaTeX transcript: {log_path}")
        for name, hits in dew_hits.items():
            failures.append(f"log[{name}]: {len(hits)} occurrence(s), first={hits[0]!r}")

    # 2. bibtex transcript ---------------------------------------------------
    if not blg_path.exists():
        result["blg"] = None
    else:
        blg_text = read_transcript(blg_path)
        blg_hits = scan(blg_text, BLG_FAILURE_PATTERNS)
        result["blg"] = {
            "sha256": sha256_file(blg_path),
            "line_count": blg_text.count("\n"),
            "scan_hits": blg_hits,
            "warning_summary": re.findall(r"\(There (?:were|was) \d+ warning", blg_text),
        }
        for name, hits in blg_hits.items():
            failures.append(f"blg[{name}]: {len(hits)} occurrence(s), first={hits[0]!r}")

    # 3. aux -> bbl coverage relation ---------------------------------------
    aux_files = sorted(package.rglob("*.aux"))
    cited: set[str] = set()
    for aux in aux_files:
        cited |= parse_aux_citations(read_transcript(aux))

    bibitem_keys: list[str] = []
    if bbl_path.exists():
        bibitem_keys = parse_bibitem_keys(read_transcript(bbl_path))
    rendered = set(bibitem_keys)

    uncovered = sorted(cited - rendered)
    result["bibliography"] = {
        "aux_files": [str(p.relative_to(package)) for p in aux_files],
        "cited_key_count": len(cited),
        "bibitem_count": len(bibitem_keys),
        "distinct_bibitem_key_count": len(rendered),
        "duplicate_bibitem_keys": sorted({k for k in bibitem_keys if bibitem_keys.count(k) > 1}),
        "cited_keys_without_bibitem": uncovered,
        "bibitems_never_cited": sorted(rendered - cited),
        "coverage_complete": not uncovered,
    }
    if uncovered:
        failures.append(
            f"bibliography coverage: {len(uncovered)} of {len(cited)} cited key(s) "
            f"have no \\bibitem, e.g. {uncovered[:5]}"
        )

    # Anti-vacuity: a coverage relation over an empty cited set is trivially
    # satisfied.  A release manuscript with no citations at all is a defect in
    # the check's own preconditions, not a pass.
    if expect_citations and not cited:
        if not aux_files:
            cannot.append(f"no .aux files under {package}: cannot establish what was cited")
        else:
            cannot.append(
                f"no \\citation commands in {len(aux_files)} .aux file(s): "
                "coverage relation would be vacuous"
            )
    if expect_citations and cited and not blg_path.exists():
        failures.append(
            f"{len(cited)} key(s) cited but no BibTeX transcript {blg_path.name}: "
            "the bibliography was never built by BibTeX"
        )

    if failures:
        result["status"] = "FAIL"
    elif cannot:
        result["status"] = "CANNOT_CHECK"
    return result


def enforce_package(package: Path, *, stem: str = "manuscript", label: str = "") -> dict[str, object]:
    """Check a package and raise unless it PASSes.

    ``CANNOT_CHECK`` raises too, with its own message: a check that could not
    run must never be recorded as a check that passed.
    """
    result = check_package(package, stem=stem)
    tag = f" [{label}]" if label else ""
    if result["status"] == "FAIL":
        raise RuntimeError(
            f"render bibliography integrity FAILED{tag}:\n"
            + json.dumps(result, indent=2, sort_keys=True)
        )
    if result["status"] == "CANNOT_CHECK":
        raise RuntimeError(
            f"render bibliography integrity COULD NOT BE CHECKED{tag} "
            f"(this is not a pass):\n" + json.dumps(result, indent=2, sort_keys=True)
        )
    return result


# --- CLI --------------------------------------------------------------------
def _kv(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError(f"expected LABEL=VALUE, got {value!r}")
    label, rest = value.split("=", 1)
    return label.strip(), rest.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--package", action="append", type=_kv, required=True, metavar="LABEL=DIR")
    parser.add_argument("--source", action="append", type=_kv, default=[], metavar="LABEL=PATH")
    parser.add_argument("--deviation", action="append", type=_kv, default=[], metavar="LABEL=NOTE")
    parser.add_argument("--registry", type=Path, default=None)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--stem", default="manuscript")
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument(
        "--allow-no-citations",
        action="store_true",
        help="permit a package whose .aux emits no \\citation (default: CANNOT_CHECK)",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    sources = dict(args.source)
    deviations = dict(args.deviation)

    registered: list[str] = []
    registry_read = None
    if args.registry is not None:
        if not args.registry.exists():
            print(f"RENDER_INTEGRITY_CANNOT_CHECK: registry not found: {args.registry}", file=sys.stderr)
            return EXIT_CANNOT_CHECK
        registered = parse_registry_canonical_sources(args.registry)
        registry_read = {
            "path": str(args.registry),
            "sha256": sha256_file(args.registry),
            "canonical_sources": registered,
        }
        if not registered:
            print(
                f"RENDER_INTEGRITY_CANNOT_CHECK: no canonical sources parsed from {args.registry}",
                file=sys.stderr,
            )
            return EXIT_CANNOT_CHECK

    packages: dict[str, object] = {}
    for label, directory in args.package:
        entry = check_package(
            (root / directory) if not Path(directory).is_absolute() else Path(directory),
            stem=args.stem,
            expect_citations=not args.allow_no_citations,
        )
        source = sources.get(label)
        if source is not None:
            source_path = (root / source) if not Path(source).is_absolute() else Path(source)
            deviation = deviations.get(label)
            if not source_path.exists():
                entry.setdefault("cannot_check", []).append(f"declared source missing: {source}")
                if entry["status"] == "PASS":
                    entry["status"] = "CANNOT_CHECK"
                entry["source"] = source
                entry["source_sha256"] = None
                entry["renders_registered_master"] = None
            else:
                entry["source"] = source
                entry["source_sha256"] = sha256_file(source_path)
                if registered:
                    in_registry = source in registered
                    entry["source_is_registered_canonical"] = in_registry
                    entry["renders_registered_master"] = bool(in_registry and deviation is None)
                else:
                    entry["renders_registered_master"] = None
            if deviation is not None:
                entry["render_deviates_from_source_by"] = deviation
        packages[label] = entry

    statuses = [p["status"] for p in packages.values()]  # type: ignore[index]
    overall = "FAIL" if "FAIL" in statuses else ("CANNOT_CHECK" if "CANNOT_CHECK" in statuses else "PASS")
    receipt = {
        "schema": "orion-v2.render-bibliography-integrity.v1",
        "status": overall,
        "registry": registry_read,
        "packages": packages,
    }

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for label, entry in packages.items():
        log = entry.get("log") or {}  # type: ignore[union-attr]
        bib = entry.get("bibliography") or {}  # type: ignore[union-attr]
        print(
            f"[{label}] {entry['status']}"  # type: ignore[index]
            f" cited={bib.get('cited_key_count')}"
            f" bibitems={bib.get('bibitem_count')}"
            f" uncovered={len(bib.get('cited_keys_without_bibitem', []))}"
            f" wrap={log.get('wrap_state')}"
            f" dewrap_joins={log.get('dewrap_joins_applied')}"
            f" registered_master={entry.get('renders_registered_master')}"
        )
        for line in entry.get("failures", []):  # type: ignore[union-attr]
            print(f"    FAIL {line}")
        for line in entry.get("cannot_check", []):  # type: ignore[union-attr]
            print(f"    CANNOT_CHECK {line}")

    print(f"RENDER_INTEGRITY_{overall}")
    return {"PASS": EXIT_PASS, "FAIL": EXIT_FAIL, "CANNOT_CHECK": EXIT_CANNOT_CHECK}[overall]


if __name__ == "__main__":
    raise SystemExit(main())
