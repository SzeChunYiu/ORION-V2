#!/usr/bin/env python3
"""Build final author-facing release candidates from frozen scientific masters.

This layer changes only release metadata and public-surface packaging. It must not
change scientific claims, results, citations, theorem text, or AH20 custody.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

AUTHOR = "Sze Chun Yiu"
EMAIL = "sze-chun.yiu@fysik.su.se"
JOURNAL_STATUS = "Independent researcher"
AI_DISCLOSURE = (
    "AI tools assisted with literature search, drafting/editing, formalization, "
    "critique and code development. The author is responsible for all scientific content."
)


def run(cmd: list[str], *, cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=capture)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def patch_once(text: str, pattern: str, replacement: str, label: str, *, flags: int = 0) -> str:
    out, count = re.subn(pattern, lambda _m: replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"expected one {label} replacement, got {count}")
    return out


def strip_internal_bibliography_source(text: str) -> str:
    """Remove the frozen master's packaging instruction from public LaTeX only."""
    pattern = (
        r"\\hypertarget\{bibliography-source\}\{%\s*"
        r"\\section\{Bibliography source\}\\label\{bibliography-source\}\}\s*"
        r"Use \\texttt\{REFERENCES\\_V1\.bib\} together with "
        r"\\texttt\{REFERENCES\\_CLASSICS\\_SUPPLEMENT\\_V1\.bib\}\. "
        r"Refresh 2026 preprint/publication statuses before arXiv and journal release\.\s*"
    )
    out, count = re.subn(pattern, "", text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"expected one internal bibliography-source block, got {count}")
    return out


def patch_flagship(tex_path: Path) -> None:
    text = tex_path.read_text(encoding="utf-8")
    text = patch_once(
        text,
        re.escape(r"\author{Author metadata pending human release}"),
        r"\author{Sze Chun Yiu\\\texttt{sze-chun.yiu@fysik.su.se}}",
        "flagship author",
    )
    text = patch_once(
        text,
        r"Large language model tools contributed materially.*?before public release\.",
        AI_DISCLOSURE,
        "flagship AI disclosure",
        flags=re.S,
    )
    tex_path.write_text(text, encoding="utf-8")


def patch_llm_arxiv(tex_path: Path) -> None:
    text = tex_path.read_text(encoding="utf-8")
    text = patch_once(
        text,
        re.escape(r"\author{Author metadata pending human release}"),
        r"\author{Sze Chun Yiu\\\texttt{sze-chun.yiu@fysik.su.se}}",
        "LLM arXiv author",
    )
    text = patch_once(
        text,
        r"Large language model systems were used extensively.*?released work\.",
        AI_DISCLOSURE,
        "LLM arXiv AI disclosure",
        flags=re.S,
    )
    text = strip_internal_bibliography_source(text)
    tex_path.write_text(text, encoding="utf-8")


def patch_llm_jmlr(tex_path: Path) -> None:
    text = tex_path.read_text(encoding="utf-8")
    text = patch_once(
        text,
        re.escape(r"\ShortHeadings{Prospective Revision Adequacy}{Author metadata pending}"),
        r"\ShortHeadings{Prospective Revision Adequacy}{Sze Chun Yiu}",
        "JMLR short author",
    )
    text = patch_once(
        text,
        re.escape(r"\author{\name Author metadata pending human release}"),
        "\\author{\\name Sze Chun Yiu \\email sze-chun.yiu@fysik.su.se\n\\addr Independent researcher}",
        "JMLR author",
    )
    text = patch_once(
        text,
        r"Large language model systems were used extensively.*?released work\.",
        AI_DISCLOSURE,
        "JMLR AI disclosure",
        flags=re.S,
    )
    text = strip_internal_bibliography_source(text)
    tex_path.write_text(text, encoding="utf-8")


def compile_package(package: Path) -> dict[str, object]:
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "manuscript.tex"], cwd=package)
    pdf = package / "manuscript.pdf"
    info = run(["pdfinfo", str(pdf)], capture=True).stdout
    m = re.search(r"(?m)^Pages:\s+(\d+)$", info)
    return {
        "page_count": int(m.group(1)) if m else None,
        "pdf_size_bytes": pdf.stat().st_size,
        "pdf_sha256": sha256(pdf),
        "manuscript_tex_sha256": sha256(package / "manuscript.tex"),
    }


def assert_release_surface(tex_path: Path) -> None:
    text = tex_path.read_text(encoding="utf-8")
    forbidden = [
        "Author metadata pending",
        "used extensively as research-assistance tools",
        "contributed materially to literature discovery",
        "Bibliography source",
        "REFERENCES_V1.bib",
        "REFERENCES\\_V1.bib",
        "REFERENCES_CLASSICS_SUPPLEMENT_V1.bib",
        "REFERENCES\\_CLASSICS\\_SUPPLEMENT\\_V1.bib",
    ]
    hits = [x for x in forbidden if x in text]
    if hits:
        raise RuntimeError(f"unresolved release placeholders/internal instructions: {hits}")
    if AUTHOR not in text or EMAIL not in text:
        raise RuntimeError(f"author metadata missing from {tex_path}")
    if AI_DISCLOSURE not in text:
        raise RuntimeError(f"minimal truthful AI disclosure missing from {tex_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out-root", type=Path, required=True)
    parser.add_argument("--jmlr-style", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    out = args.out_root.resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    flagship = out / "flagship_arxiv"
    llm = out / "llm"

    run([
        sys.executable,
        str(root / "scripts/assemble_flagship_v14_release.py"),
        "--root", str(root),
        "--out-dir", str(flagship),
    ])
    run([
        sys.executable,
        str(root / "scripts/assemble_llm_pra_release_safe_fonts.py"),
        "--root", str(root),
        "--out-root", str(llm),
        "--jmlr-style", str(args.jmlr_style.resolve()),
    ])

    llm_arxiv = llm / "arxiv_v1"
    llm_jmlr = llm / "jmlr_v1"
    patch_flagship(flagship / "manuscript.tex")
    patch_llm_arxiv(llm_arxiv / "manuscript.tex")
    patch_llm_jmlr(llm_jmlr / "manuscript.tex")

    for package in (flagship, llm_arxiv, llm_jmlr):
        assert_release_surface(package / "manuscript.tex")

    metrics = {
        "flagship_arxiv": compile_package(flagship),
        "llm_arxiv": compile_package(llm_arxiv),
        "llm_jmlr": compile_package(llm_jmlr),
    }

    metadata_src = root / "papers/release/FINAL_AUTHOR_AND_AI_METADATA_V1.json"
    for package in (flagship, llm_arxiv, llm_jmlr):
        shutil.copy2(metadata_src, package / "AUTHOR_AND_AI_METADATA.json")

    receipt = {
        "schema": "orion-v2.final-paper-release.v1",
        "author": {
            "name": AUTHOR,
            "email": EMAIL,
            "institutional_affiliation_claimed": False,
            "journal_status_label": JOURNAL_STATUS,
        },
        "ai_disclosure": AI_DISCLOSURE,
        "scientific_master_changed": False,
        "scientific_claims_changed": False,
        "internal_release_instructions_stripped": True,
        "ah20_result_backfilled_into_arxiv": False,
        "submission_authorized": False,
        "packages": metrics,
    }
    (out / "FINAL_RELEASE_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
