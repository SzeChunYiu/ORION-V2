#!/usr/bin/env python3
"""CITATION_BINDING_AUDIT_V1 — mechanical check of MANUSCRIPT_DRAFT_V8_CITED.md
against REFERENCES_V1.bib + REFERENCES_CLASSICS_SUPPLEMENT_V1.bib and the frozen
policy in CITATION_COVERAGE_MATRIX_V1.md (section F gate).

This script has NO editorial authority. It mechanically verifies, at key level:

  F1  every citation key used in the manuscript resolves to a bib entry;
  F2  every OWNERSHIP / DIRECT_NEIGHBOR matrix row has >=1 of its required
      keys cited (partial-key coverage is reported, not failed);
  F3  every section-D mandatory-paragraph key is cited;
  F4  the section-D residual sentence appears verbatim;
  F5  bib files parse, no duplicate keys across files;
  E1  every key named in section-E status classes exists in the bib.

Recorded as CANNOT_CHECK (honest marks, never silently passed):
  - sentence-level binding of a key to its classified assertion
    (key-level presence is what is checked);
  - decorative-bibliography-padding relevance (F6, editorial);
  - blind-review identity and preprint-status refresh (needs external
    metadata evidence).

Exit 0 = PASS (`CITATION_COVERAGE_COMPLETE__PARENT_CONCESSIONS_BOUND`),
exit 3 = any F/E rule violated, exit 2 = usage.
"""

import argparse
import json
import re
import sys
from pathlib import Path

MANDATED_ROLES = {"OWNERSHIP", "DIRECT_NEIGHBOR"}
KEY_SHAPE = re.compile(r"^[a-zA-Z]+[0-9]{4}[a-zA-Z0-9]*$")
CITE_CMD = re.compile(r"\\cite[a-zA-Z]*\{([^}]*)\}")
CITE_TOKEN = re.compile(r"\\cite[a-zA-Z]*")
BIB_ENTRY = re.compile(r"^@\w+\{([^,\s]+)\s*,")


def extract_cited_keys(text: str) -> tuple[set[str], list[str]]:
    """Return (keys, malformed_tokens) from \\cite*{...} commands."""
    keys: set[str] = set()
    for group in CITE_CMD.findall(text):
        for key in group.split(","):
            key = key.strip()
            if not key:
                continue
            if not KEY_SHAPE.match(key):
                # a cite command whose content is not a bib-key shape is a
                # transcription defect, not an honest CANNOT_CHECK
                return keys, [f"malformed cite content {key!r}"]
            keys.add(key)
    # tokens without a following {...} group are malformed
    spans = [(m.start(), m.end()) for m in CITE_TOKEN.finditer(text)]
    malformed = []
    for start, end in spans:
        if end < len(text) and text[end] == "{":
            # find closing brace; unclosed also malformed
            close = text.find("}", end)
            if close == -1:
                malformed.append(f"unclosed cite at offset {start}")
        else:
            malformed.append(f"cite without brace group at offset {start}")
    return keys, malformed


def parse_bib(path: Path) -> tuple[set[str], list[str]]:
    keys: set[str] = []
    for i, line in enumerate(path.read_text().splitlines(), 1):
        m = BIB_ENTRY.match(line.strip())
        if m:
            keys.append(m.group(1))
    dups = sorted({k for k in keys if keys.count(k) > 1})
    return set(keys), [f"duplicate bib key {k}" for k in dups]


def parse_matrix(path: Path) -> dict:
    """Parse sections A/B tables, D list + residual, E class lists."""
    lines = path.read_text().splitlines()
    section = ""
    rows_ab: list[dict] = []          # {assertion, role, keys}
    d_keys: set[str] = set()
    residual_sentence = None
    e_classes: dict[str, set[str]] = {}
    for line in lines:
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if line.startswith("# "):
            section = line[2:].strip()
            continue
        if section.startswith(("A.", "B.")) and line.strip().startswith("|"):
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) >= 4 and cols[1].strip("` ") not in ("Role", "") \
                    and not set(cols[1]) <= {"-", " "}:
                role = cols[1].strip("` ").strip()
                keys = [t for t in re.findall(r"`([^`]+)`", cols[2])
                        if KEY_SHAPE.match(t)]
                rows_ab.append(
                    {"assertion": cols[0][:100], "role": role, "keys": keys})
        elif section.startswith("D."):
            if re.match(r"\d+\.\s", line.strip()):
                for t in re.findall(r"`([^`]+)`", line):
                    if KEY_SHAPE.match(t):
                        d_keys.add(t)
            if line.strip().startswith("> **"):
                residual_sentence = line.strip().lstrip("> ").strip("*").strip()
        elif section.startswith("E."):
            if line.strip().startswith("###"):
                current_class = line.strip()[4:]
                e_classes[current_class] = set()
            elif e_classes and line.strip():
                for t in re.findall(r"`([^`]+)`", line):
                    if KEY_SHAPE.match(t):
                        last = list(e_classes)[-1] if e_classes else None
                        if last:
                            e_classes[last].add(t)
    return {
        "rows_ab": rows_ab,
        "d_keys": sorted(d_keys),
        "residual_sentence": residual_sentence,
        "e_classes": {k: sorted(v) for k, v in e_classes.items()},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manuscript", required=True)
    ap.add_argument("--bib", action="append", required=True)
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--output", required=True, help="output .json path (.md/.csv siblings)")
    args = ap.parse_args()

    ms_path = Path(args.manuscript)
    matrix_path = Path(args.matrix)
    out_json = Path(args.output)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    warnings: list[str] = []
    cannot_check: list[str] = [
        "sentence-level binding of citation keys to their classified "
        "assertions (key-level presence only is checked)",
        "F6 decorative-bibliography relevance (editorial judgement)",
        "blind-review identity integrity and preprint-status refresh "
        "(require external metadata evidence)",
    ]

    ms_text = ms_path.read_text()
    cited, cite_malformed = extract_cited_keys(ms_text)
    for m in cite_malformed:
        failures.append(f"F1 {m}")

    bib_keys: set[str] = set()
    for bib_arg in args.bib:
        bk, bib_errs = parse_bib(Path(bib_arg))
        for e in bib_errs:
            failures.append(f"F5 {bib_arg}: {e}")
        overlap = bib_keys & bk
        if overlap:
            failures.append(f"F5 duplicate keys across bib files: {sorted(overlap)}")
        bib_keys |= bk

    # F1
    unresolved = sorted(cited - bib_keys)
    if unresolved:
        failures.append(f"F1 cited keys missing from bib: {unresolved}")

    matrix = parse_matrix(matrix_path)

    # F2 — mandated roles need >=1 cited key
    row_report = []
    for row in matrix["rows_ab"]:
        rk = set(row["keys"])
        hit = rk & cited
        entry = {
            "role": row["role"],
            "assertion": row["assertion"][:60],
            "required_keys": sorted(rk),
            "cited_of_required": sorted(hit),
        }
        row_report.append(entry)
        if row["role"] in MANDATED_ROLES and not hit:
            failures.append(
                f"F2 {row['role']} row {row['assertion'][:60]!r}: none of "
                f"{sorted(rk)} cited")
        elif row["role"] in MANDATED_ROLES and hit != rk:
            warnings.append(
                f"F2 partial {row['role']}: cited {sorted(hit)} of {sorted(rk)} "
                f"({row['assertion'][:50]!r})")

    # F3 — section D keys all cited
    d_missing = sorted(set(matrix["d_keys"]) - cited)
    if d_missing:
        failures.append(f"F3 section-D mandatory keys not cited: {d_missing}")

    # F4 — residual sentence verbatim
    residual = matrix["residual_sentence"]
    if not residual:
        failures.append("F4 residual sentence not found in matrix (parse defect)")
    else:
        norm = re.sub(r"\s+", " ", residual)
        if norm not in re.sub(r"\s+", " ", ms_text):
            failures.append("F4 residual sentence not present verbatim in manuscript")

    # E1 — every class-listed key exists in bib
    for cls, keys in matrix["e_classes"].items():
        missing = sorted(set(keys) - bib_keys)
        if missing:
            failures.append(f"E1 class {cls!r} names non-bib keys: {missing}")

    # informational: cited keys outside the matrix universe
    matrix_universe = set(matrix["d_keys"])
    for row in matrix["rows_ab"]:
        matrix_universe |= set(row["keys"])
    for keys in matrix["e_classes"].values():
        matrix_universe |= set(keys)
    extra = sorted(cited - matrix_universe)
    if extra:
        warnings.append(f"cited keys outside matrix universe (editor-added): {extra}")

    overall = "PASS" if not failures else "FAIL"
    receipt = {
        "schema": "orion.51.citation-binding-audit.v1",
        "inputs": {
            "manuscript": str(ms_path),
            "bib": [str(b) for b in args.bib],
            "matrix": str(matrix_path),
        },
        "counts": {
            "cite_commands": len(CITE_CMD.findall(ms_text)),
            "cited_keys": len(cited),
            "bib_keys": len(bib_keys),
            "unused_bib_keys": len(bib_keys - cited),
            "matrix_rows_ab": len(matrix["rows_ab"]),
            "mandated_rows": sum(
                1 for r in matrix["rows_ab"] if r["role"] in MANDATED_ROLES),
            "section_d_keys": len(matrix["d_keys"]),
        },
        "unused_bib_keys": sorted(bib_keys - cited),
        "row_report": row_report,
        "e_classes": matrix["e_classes"],
        "warnings": warnings,
        "cannot_check": cannot_check,
        "failures": failures,
        "terminal_mark": ("CITATION_COVERAGE_COMPLETE__PARENT_CONCESSIONS_BOUND"
                          if overall == "PASS" else None),
        "overall": overall,
    }
    out_json.write_text(json.dumps(receipt, indent=1) + "\n")

    md = [
        "# CITATION_BINDING_AUDIT_V1",
        "",
        f"Manuscript `{ms_path.name}` vs bibs {[Path(b).name for b in args.bib]} "
        f"vs matrix `{matrix_path.name}`.",
        "",
        f"- cite commands: {receipt['counts']['cite_commands']}; unique cited "
        f"keys: {receipt['counts']['cited_keys']}; bib keys: "
        f"{receipt['counts']['bib_keys']}; unused bib keys: "
        f"{receipt['counts']['unused_bib_keys']}",
        f"- matrix A/B rows: {receipt['counts']['matrix_rows_ab']} "
        f"({receipt['counts']['mandated_rows']} mandated); section-D keys: "
        f"{receipt['counts']['section_d_keys']}",
        f"- warnings: {len(warnings)}; CANNOT_CHECK: {len(cannot_check)}",
        "",
        "| Rule | Result |",
        "|---|---|",
    ]
    for rule in ("F1", "F2", "F3", "F4", "F5", "E1"):
        rule_fail = [f for f in failures if f.startswith(rule)]
        md.append(f"| {rule} | {'FAIL: ' + '; '.join(rule_fail) if rule_fail else 'PASS'} |")
    md += ["", f"OVERALL {overall}", ""]
    if overall == "PASS":
        md.append("Terminal mark: `CITATION_COVERAGE_COMPLETE__"
                  "PARENT_CONCESSIONS_BOUND`")
    out_json.with_suffix(".md").write_text("\n".join(md) + "\n")

    print(f"cited={len(cited)} bib={len(bib_keys)} rows_ab="
          f"{len(matrix['rows_ab'])} d_keys={len(matrix['d_keys'])}")
    print(f"OVERALL {overall}")
    for f in failures:
        print(f"FAIL {f}")
    for w in warnings:
        print(f"WARN {w}")
    for c in cannot_check:
        print(f"CANNOT_CHECK {c}")
    return 0 if not failures else 3


if __name__ == "__main__":
    sys.exit(main())
