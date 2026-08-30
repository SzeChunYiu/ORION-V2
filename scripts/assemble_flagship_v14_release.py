#!/usr/bin/env python3
"""Mechanical arXiv release assembler for the frozen Machine Epistemics V14 Perspective."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

TITLE = "Machine Epistemics"
SUBTITLE = "Toward a Science of AI-Driven Inquiry and Scientific Change"
PANDOC_CITE_RE = re.compile(r"\[@([^\]]+)\]")
BIB_KEY_RE = re.compile(r"(?m)^@\w+\s*\{\s*([^,\s]+)\s*,")
NUMERIC_HEADING_RE = re.compile(r"^(#{2,4})\s+\d+(?:\.\d+)*\.?\s+(.+)$", re.MULTILINE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd: list[str], *, cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=capture)


def bib_keys(text: str) -> list[str]:
    return BIB_KEY_RE.findall(text)


def citation_keys(text: str) -> set[str]:
    out: set[str] = set()
    for group in PANDOC_CITE_RE.findall(text):
        for token in group.split(";"):
            token = token.strip()
            if token.startswith("@"):
                token = token[1:]
            token = token.split(",", 1)[0].strip()
            if token:
                out.add(token)
    return out


def merge_bibs(paths: list[Path], out: Path) -> dict[str, object]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    chunks: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        keys = bib_keys(text)
        for key in keys:
            if key in seen:
                duplicates.add(key)
            seen.add(key)
        chunks.append(f"% ---- {path.name} ----\n{text.strip()}\n")
    if duplicates:
        raise ValueError(f"duplicate bibliography keys: {sorted(duplicates)}")
    out.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    return {"entry_count": len(seen), "keys": sorted(seen)}


def split_master(text: str) -> tuple[str, str, str]:
    lines = text.splitlines()
    if len(lines) < 4 or lines[0].strip() != f"# {TITLE}" or lines[1].strip() != f"## {SUBTITLE}":
        raise ValueError("unexpected V14 title/subtitle surface")
    try:
        abstract_i = lines.index("## Abstract")
    except ValueError as exc:
        raise ValueError("V14 lacks Abstract heading") from exc
    next_h2 = None
    for i in range(abstract_i + 1, len(lines)):
        if lines[i].startswith("## "):
            next_h2 = i
            break
    if next_h2 is None:
        raise ValueError("V14 lacks body after abstract")
    abstract = "\n".join(lines[abstract_i + 1 : next_h2]).strip()
    body = "\n".join(lines[next_h2:]).strip() + "\n"
    return TITLE, abstract, body


def count_main_words(text: str) -> int:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = PANDOC_CITE_RE.sub(" ", text)
    text = re.sub(r"(?m)^#+\s+", "", text)
    text = re.sub(r"[|*_`>#]", " ", text)
    return len(re.findall(r"\b[A-Za-z0-9][A-Za-z0-9'’-]*\b", text))


def pandoc_fragment(path: Path) -> str:
    return run(
        [
            "pandoc",
            str(path),
            "--from=markdown+raw_tex+tex_math_dollars+pipe_tables+fenced_code_blocks+citations",
            "--to=latex",
            "--natbib",
            "--shift-heading-level-by=-1",
            "--wrap=none",
        ],
        capture=True,
    ).stdout


def compile_pdf(package: Path) -> dict[str, object]:
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "manuscript.tex"], cwd=package)
    pdf = package / "manuscript.pdf"
    page_count = None
    if shutil.which("pdfinfo"):
        info = run(["pdfinfo", str(pdf)], capture=True).stdout
        m = re.search(r"(?m)^Pages:\s+(\d+)$", info)
        if m:
            page_count = int(m.group(1))
    bbl = package / "manuscript.bbl"
    bbl_text = bbl.read_text(encoding="utf-8") if bbl.exists() else ""
    return {
        "pdf_sha256": sha256(pdf),
        "pdf_size_bytes": pdf.stat().st_size,
        "page_count": page_count,
        "bibliography_rendered": "\\bibitem" in bbl_text,
        "bibliography_item_count": bbl_text.count("\\bibitem"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--compile", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    out = args.out_dir.resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    master = root / "papers/drafts/FLAGSHIP_MACHINE_EPISTEMICS_PERSPECTIVE_V14_CITED_ARXIV_JOURNAL_MASTER.md"
    bib_paths = [
        root / "papers/flagship/FLAGSHIP_REFERENCES_V14_CORRECTED.bib",
        root / "papers/flagship/FLAGSHIP_REFERENCES_V15_NEIGHBOR_SUPPLEMENT.bib",
        root / "papers/flagship/FLAGSHIP_REFERENCES_V16_FOUNDATION_SUPPLEMENT.bib",
    ]
    source = master.read_text(encoding="utf-8")
    cited = citation_keys(source)
    available: list[str] = []
    for path in bib_paths:
        available.extend(bib_keys(path.read_text(encoding="utf-8")))
    duplicate_keys = sorted({k for k in available if available.count(k) > 1})
    missing_keys = sorted(cited - set(available))
    if duplicate_keys or missing_keys:
        raise ValueError(json.dumps({"duplicate_keys": duplicate_keys, "missing_keys": missing_keys}, indent=2))

    forbidden = {
        "issue_pr": r"(?i)\b(?:issue|pull request|PR)\s*#\d+",
        "repo_path": r"(?m)(?:^|\s)(?:papers|research|scripts|src|tests|\.github)/[\w./-]+",
        "ci_narrative": r"(?i)\bCI\s+(?:job|workflow|run)\b",
    }
    hits = {k: re.findall(v, source) for k, v in forbidden.items() if re.search(v, source)}
    if hits:
        raise ValueError(f"manuscript-facing internal narrative found: {hits}")

    word_count = count_main_words(source)
    title, abstract_md, body_md = split_master(source)
    body_md = NUMERIC_HEADING_RE.sub(r"\1 \2", body_md)

    build = out / "_build"
    build.mkdir()
    (build / "abstract.md").write_text(abstract_md + "\n", encoding="utf-8")
    (build / "body.md").write_text(body_md, encoding="utf-8")
    abstract_tex = pandoc_fragment(build / "abstract.md").strip()
    body_tex = pandoc_fragment(build / "body.md")
    if "[@" in abstract_tex or "[@" in body_tex:
        raise ValueError("Pandoc citation markup leaked into generated LaTeX")
    if cited and "\\cite" not in body_tex and "\\cite" not in abstract_tex:
        raise ValueError("citation keys exist but generated LaTeX has no natbib citation commands")
    if re.search(r"\\subsection\{From scientific outputs", body_tex):
        raise ValueError("top-level manuscript headings were not promoted to LaTeX sections")

    bib_summary = merge_bibs(bib_paths, out / "references.bib")
    tex = rf"""\documentclass[11pt]{{article}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{amsmath,amssymb,mathtools}}
\usepackage{{booktabs,longtable,array}}
\usepackage{{graphicx}}
\usepackage[round]{{natbib}}
\usepackage{{microtype}}
\usepackage{{xurl}}
\usepackage[hidelinks]{{hyperref}}
\providecommand{{\tightlist}}{{\setlength{{\itemsep}}{{0pt}}\setlength{{\parskip}}{{0pt}}}}
\title{{Machine Epistemics\\\large Toward a Science of AI-Driven Inquiry and Scientific Change}}
\author{{Author metadata pending human release}}
\date{{}}
\begin{{document}}
\maketitle
\begin{{abstract}}
{abstract_tex}
\end{{abstract}}
{body_tex}
\bibliographystyle{{plainnat}}
\bibliography{{references}}
\end{{document}}
"""
    (out / "manuscript.tex").write_text(tex, encoding="utf-8")
    (out / "README_RELEASE.md").write_text(
        "# Flagship V14 mechanical arXiv candidate\n\n"
        "Generated from the frozen V14 cited Perspective. Human authorship, category/license, final adoption, "
        "and release approval remain unresolved by design. AH20 is not required to generate or release the arXiv "
        "Perspective and must not be backfilled into these bytes as if it preceded the conceptual manuscript.\n",
        encoding="utf-8",
    )

    result = {
        "schema": "orion-v2.flagship-v14-arxiv-package.v1",
        "master_sha256": sha256(master),
        "citation_key_count": len(cited),
        "bibliography": bib_summary,
        "main_text_word_count_mechanical": word_count,
        "nature_machine_intelligence_perspective_target_words": [3000, 4000],
        "within_nominal_target": 3000 <= word_count <= 4000,
        "manuscript_tex_sha256": sha256(out / "manuscript.tex"),
        "references_sha256": sha256(out / "references.bib"),
        "pandoc_citation_markup_absent": True,
        "natbib_commands_present": True,
        "top_level_headings_promoted": True,
        "human_release_authority": False,
        "ah20_required_for_arxiv": False,
        "scientific_claims_changed": False,
    }
    if args.compile:
        result.update(compile_pdf(out))
    (out / "release_receipt.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
