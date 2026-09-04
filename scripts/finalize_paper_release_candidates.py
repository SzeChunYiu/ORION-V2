#!/usr/bin/env python3
"""Build author-facing paper candidates under the academic-skill PR17 gates.

The PRA V12 scientific master already exposes its required formal spine and is
not scientifically rewritten here. The flagship release is a versioned V15
composite: frozen V14 prose/citations plus a compact formal-spine fragment whose
content already exists in the programme's formal records. AH20-R2 is not
backfilled into the Perspective.
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

from check_render_bibliography_integrity import enforce_package

AUTHOR = "Sze Chun Yiu"
EMAIL = "sze-chun.yiu@fysik.su.se"
JOURNAL_STATUS = "Independent researcher"
AI_DISCLOSURE = (
    "AI tools assisted with literature search, drafting/editing, formalization, "
    "critique and code development. The author is responsible for all scientific content."
)
SKILL_PR17_HEAD = "ef47c81101e1e1b97864019dde143456a581de1c"
SKILL_PR16_HEAD = "087e47330826295a0b114563ec33238951ac56a9"
FLAGSHIP_RELEASE_COMPOSITE = "V15_FORMAL_SPINE_COMPOSITE"
FLAGSHIP_FORMAL_MARKER = r"\hypertarget{frontier-problems-expose-the-distinction}{%"


def run(cmd: list[str], *, cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=capture)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def patch_once(text: str, pattern: str, replacement: str, label: str, *, flags: int = 0) -> str:
    out, count = re.subn(pattern, lambda _m: replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"expected one {label} replacement, got {count}")
    return out


def prose_word_count_from_tex(text: str) -> int:
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\\subsection\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\label\{[^}]*\}", " ", text)
    text = re.sub(r"\\text\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[A-Za-z]+\*?", " ", text)
    text = re.sub(r"[{}$\\_^~]", " ", text)
    return len(re.findall(r"\b[A-Za-z0-9][A-Za-z0-9'’-]*\b", text))


def strip_internal_bibliography_source(text: str) -> str:
    """Remove the frozen PRA master's packaging instruction from public LaTeX only."""
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


def stabilize_validation_table(package: Path, *, jmlr: bool) -> None:
    """Keep the appendix heading before its table; widen JMLR's first column."""
    tex_path = package / "manuscript.tex"
    tex = tex_path.read_text(encoding="utf-8")
    if r"\usepackage{float}" not in tex:
        anchor = r"\usepackage{booktabs,longtable,array}"
        if anchor not in tex:
            raise RuntimeError(f"cannot add float package in {tex_path}")
        tex = tex.replace(anchor, anchor + "\n" + r"\usepackage{float}", 1)
    tex_path.write_text(tex, encoding="utf-8")

    table_path = package / "figures/table3_validation.tex"
    table = table_path.read_text(encoding="utf-8")
    if r"\begin{table}[t]" not in table:
        raise RuntimeError(f"unexpected validation table placement in {table_path}")
    table = table.replace(r"\begin{table}[t]", r"\begin{table}[H]", 1)
    if jmlr:
        old = r"\begin{tabular}{p{0.31\linewidth}p{0.43\linewidth}p{0.17\linewidth}}"
        new = r"\begin{tabular}{p{0.37\linewidth}p{0.37\linewidth}p{0.17\linewidth}}"
        if old not in table:
            raise RuntimeError("unexpected JMLR validation-table column contract")
        table = table.replace(old, new, 1)
    table_path.write_text(table, encoding="utf-8")


def inject_flagship_formal_spine(tex_path: Path, formal_spine_path: Path) -> dict[str, object]:
    text = tex_path.read_text(encoding="utf-8")
    if "Formal object of Machine Epistemics" in text:
        raise RuntimeError("flagship formal spine already present before PR17 injection")
    if FLAGSHIP_FORMAL_MARKER not in text:
        raise RuntimeError("cannot locate flagship formal-spine insertion point")
    fragment = formal_spine_path.read_text(encoding="utf-8").strip()
    text = text.replace(FLAGSHIP_FORMAL_MARKER, fragment + "\n\n" + FLAGSHIP_FORMAL_MARKER, 1)
    tex_path.write_text(text, encoding="utf-8")
    return {
        "fragment_sha256": sha256(formal_spine_path),
        "added_prose_words_mechanical": prose_word_count_from_tex(fragment),
    }


def patch_flagship(tex_path: Path, formal_spine_path: Path) -> dict[str, object]:
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
    return inject_flagship_formal_spine(tex_path, formal_spine_path)


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
    # These three packages are compiled here, after the .tex is patched, so the
    # assemblers' own checks never see this build tree.  Read its transcripts.
    integrity = enforce_package(package, label=package.name)
    return {
        "page_count": int(m.group(1)) if m else None,
        "pdf_size_bytes": pdf.stat().st_size,
        "pdf_sha256": sha256(pdf),
        "manuscript_tex_sha256": sha256(package / "manuscript.tex"),
        "bibliography_item_count": integrity["bibliography"]["bibitem_count"],
        "render_integrity": integrity,
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


def assert_flagship_formal_spine(tex_path: Path) -> None:
    text = tex_path.read_text(encoding="utf-8")
    required = [
        "Formal object of Machine Epistemics",
        r"E_t=(P_t,S_t,O_t,A_t,R_t,M_t,V_t,X_t,H_t,K_t)",
        r"\widetilde E_t=(E_t;\Gamma_t,\Pi_t,\mathcal A_t)",
        r"T_t:(\widetilde E_t,a_t,x_t)\mapsto(\widetilde E_{t+1},\rho_t)",
        r"\mathcal A_t\neq\mathfrak E^{\star}",
        r"\not\Rightarrow\text{warranted scientific transition}",
        "candidate constraints to test, not established universal axioms",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"PR17 formal-spine recovery failed: {missing}")


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

    flagship_base_receipt = json.loads((flagship / "release_receipt.json").read_text(encoding="utf-8"))
    formal_spine_path = root / "papers/flagship/FLAGSHIP_FORMAL_SPINE_MAIN_TEXT_V1.tex"
    flagship_formal = patch_flagship(flagship / "manuscript.tex", formal_spine_path)

    llm_arxiv = llm / "arxiv_v1"
    llm_jmlr = llm / "jmlr_v1"
    patch_llm_arxiv(llm_arxiv / "manuscript.tex")
    patch_llm_jmlr(llm_jmlr / "manuscript.tex")
    stabilize_validation_table(llm_arxiv, jmlr=False)
    stabilize_validation_table(llm_jmlr, jmlr=True)

    for package in (flagship, llm_arxiv, llm_jmlr):
        assert_release_surface(package / "manuscript.tex")
    assert_flagship_formal_spine(flagship / "manuscript.tex")

    estimated_flagship_words = (
        int(flagship_base_receipt["main_text_word_count_mechanical"])
        + int(flagship_formal["added_prose_words_mechanical"])
    )
    if not 3000 <= estimated_flagship_words <= 4000:
        raise RuntimeError(f"PR17 flagship formal-spine repair leaves Perspective target: {estimated_flagship_words}")

    metrics = {
        "flagship_arxiv": compile_package(flagship),
        "llm_arxiv": compile_package(llm_arxiv),
        "llm_jmlr": compile_package(llm_jmlr),
    }

    shutil.copy2(formal_spine_path, flagship / "FORMAL_SPINE_MAIN_TEXT.tex")
    metadata_src = root / "papers/release/FINAL_AUTHOR_AND_AI_METADATA_V1.json"
    for package in (flagship, llm_arxiv, llm_jmlr):
        shutil.copy2(metadata_src, package / "AUTHOR_AND_AI_METADATA.json")

    receipt = {
        "schema": "orion-v2.final-paper-release.v2-pr17",
        "academic_skill_state": {
            "formal_spine_pr17_head": SKILL_PR17_HEAD,
            "research_integrity_pr16_head": SKILL_PR16_HEAD,
        },
        "author": {
            "name": AUTHOR,
            "email": EMAIL,
            "institutional_affiliation_claimed": False,
            "journal_status_label": JOURNAL_STATUS,
        },
        "ai_disclosure": AI_DISCLOSURE,
        "flagship": {
            "base_scientific_master": "V14_CITED_ARXIV_JOURNAL_MASTER",
            "release_composite": FLAGSHIP_RELEASE_COMPOSITE,
            "formal_spine_status": "PASS_RESTORED_IN_MAIN_TEXT",
            "formal_spine_fragment_sha256": flagship_formal["fragment_sha256"],
            "formal_spine_added_prose_words_mechanical": flagship_formal["added_prose_words_mechanical"],
            "estimated_main_text_word_count": estimated_flagship_words,
            "base_master_edited": False,
            "scientific_manuscript_delta": "RESTORE_EXISTING_PROGRAMME_FORMAL_SPINE",
            "new_scientific_result_added": False,
            "ah20_r2_backfilled_into_perspective": False,
        },
        "pra": {
            "scientific_master": "V12_ARXIV_JMLR_FINAL",
            "formal_spine_status": "PASS_NO_SCIENTIFIC_REWRITE_REQUIRED",
            "scientific_manuscript_changed": False,
        },
        "internal_release_instructions_stripped": True,
        "appendix_table_placement_stabilized": True,
        "research_integrity_independent_verification_complete": False,
        "submission_authorized": False,
        "packages": metrics,
    }
    (out / "FINAL_RELEASE_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
