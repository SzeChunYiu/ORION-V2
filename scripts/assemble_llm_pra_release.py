#!/usr/bin/env python3
"""Assemble mechanical arXiv/JMLR release candidates for the PRA paper.

Scientific prose is read from the frozen V12 Markdown master.  This script may
format, validate, and package that prose, but it must not invent or strengthen
scientific claims.  Human-only authorship/legal fields remain explicit
placeholders in generated candidates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from check_render_bibliography_integrity import enforce_package

TITLE = "Prospective Revision Adequacy: Auditing Autoregressive Representations Beyond Current Prediction and Decision"
SHORT_TITLE = "Prospective Revision Adequacy"

CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]+)\}")
BIB_KEY_RE = re.compile(r"(?m)^@\w+\s*\{\s*([^,\s]+)\s*,")
NUMERIC_HEADING_RE = re.compile(r"^(#{2,4})\s+\d+(?:\.\d+)*\.?\s+(.+)$", re.MULTILINE)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], *, cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture,
    )


def split_master(text: str) -> tuple[str, str, str]:
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("V12 master must begin with a single H1 title")
    title = lines[0][2:].strip()
    if title != TITLE:
        raise ValueError(f"unexpected public title: {title!r}")

    try:
        abstract_idx = lines.index("## Abstract")
    except ValueError as exc:
        raise ValueError("V12 master lacks ## Abstract") from exc

    next_h2 = None
    for idx in range(abstract_idx + 1, len(lines)):
        if lines[idx].startswith("## "):
            next_h2 = idx
            break
    if next_h2 is None:
        raise ValueError("V12 master lacks body after abstract")

    abstract = "\n".join(lines[abstract_idx + 1 : next_h2]).strip()
    body = "\n".join(lines[next_h2:]).strip() + "\n"
    return title, abstract, body


def citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for match in CITE_RE.finditer(text):
        keys.update(k.strip() for k in match.group(1).split(",") if k.strip())
    return keys


def bib_keys(text: str) -> list[str]:
    return BIB_KEY_RE.findall(text)


def merge_bibliographies(paths: list[Path], out: Path) -> dict[str, object]:
    seen: dict[str, Path] = {}
    parts: list[str] = []
    duplicate_keys: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for key in bib_keys(text):
            if key in seen:
                duplicate_keys.append(key)
            else:
                seen[key] = path
        parts.append(f"% ---- source: {path.name} ----\n{text.strip()}\n")
    if duplicate_keys:
        raise ValueError(f"duplicate bibliography keys: {sorted(set(duplicate_keys))}")
    out.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return {"entry_count": len(seen), "keys": sorted(seen)}


def audit_surface(master: Path, proof_appendix: Path, bib_paths: list[Path]) -> dict[str, object]:
    manuscript = master.read_text(encoding="utf-8")
    proof = proof_appendix.read_text(encoding="utf-8") if proof_appendix.exists() else ""
    source = manuscript + "\n" + proof

    all_bib_keys: list[str] = []
    for path in bib_paths:
        all_bib_keys.extend(bib_keys(path.read_text(encoding="utf-8")))
    duplicates = sorted({k for k in all_bib_keys if all_bib_keys.count(k) > 1})
    cited = sorted(citation_keys(source))
    available = set(all_bib_keys)
    missing = sorted(set(cited) - available)

    forbidden_patterns = {
        "issue_or_pr_narrative": r"(?i)\b(?:issue|pull request|PR)\s*#\d+",
        "branch_narrative": r"(?i)\bbranch\s+[`\w/.-]+",
        "ci_narrative": r"(?i)\bCI\s+(?:job|workflow|run)\b",
        "repository_path": r"(?m)(?:^|\s)(?:papers|research|scripts|src|tests|\.github)/[\w./-]+",
    }
    forbidden_hits = {
        name: re.findall(pattern, manuscript)
        for name, pattern in forbidden_patterns.items()
        if re.search(pattern, manuscript)
    }

    required_phrases = [
        "Theorem 1 — one-step compatibility characterization",
        "Corollary 1 — current adequacy is not a prospective certificate",
        "The paper does not establish that deployed LLMs generally exhibit this failure.",
        "joint acceptable-action intersection",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in manuscript]

    result = {
        "schema": "orion-v2.llm-pra-release-audit.v1",
        "citation_key_count": len(cited),
        "bibliography_key_count": len(available),
        "missing_citation_keys": missing,
        "duplicate_bibliography_keys": duplicates,
        "forbidden_surface_hits": forbidden_hits,
        "missing_required_phrases": missing_phrases,
        "pass": not (missing or duplicates or forbidden_hits or missing_phrases),
    }
    if not result["pass"]:
        raise ValueError(json.dumps(result, indent=2, sort_keys=True))
    return result


def figure_one() -> str:
    return r"""\begin{figure}[t]
\centering
\small
\begin{tabular}{p{0.46\linewidth}p{0.46\linewidth}}
\toprule
\textbf{Full / augmented state} & \textbf{Compressed present state}\\
\midrule
$h_A$: $S_{P,u}=s$, RETAIN, provenance $A$ & $Z_c(h_A)=Z_c(h_B)=s$\\
$h_B$: $S_{P,u}=s$, RETAIN, provenance $B$ & current action: RETAIN\\[0.4em]
\multicolumn{2}{c}{same controlled later event: $\operatorname{RETRACT}(A)$}\\[0.4em]
$h_A'\rightarrow$ REOPEN; $h_B'\rightarrow$ RETAIN & one identical $(z,x)$ input cannot map deterministically to both actions\\
\bottomrule
\end{tabular}
\vspace{0.5em}
\[C_{\mathrm{stat}}^*=0,\qquad C_{\mathrm{dyn}}^*=1\ \mathrm{bit},\qquad \Omega_{\mathrm{dyn}}=1\ \mathrm{bit}.\]
\caption{\textbf{A present-equivalent pair can require a dormant distinction for later revision.} Under the registered reference protocol, the two equiprobable histories share the declared predictive state and unique present action. A common later controlled event makes their correct successor decisions incompatible. The construction is a finite no-certification witness, not evidence that deployed LLMs generally behave this way.}
\label{fig:one-bit-witness}
\end{figure}
"""


def figure_three() -> str:
    return r"""\begin{figure}[t]
\centering
\small
\fbox{\begin{minipage}{0.93\linewidth}
\centering
\textbf{REGISTER} prediction reference, current responsibility, future evidence family, future responsibility\\
$\downarrow$\\
\textbf{PRESENT-EQUIVALENCE GATE} prediction margin + current action/risk + matched resources\\
$\downarrow$\\
\textbf{REPRESENTATION INTERVENTION / STATE COMPARISON}\\
$\downarrow$\\
\textbf{ALTERNATE-CHANNEL + PARAMETRIC-RECONSTRUCTION GATE}\\
$\downarrow$\\
\textbf{COMMON LATER EVIDENCE}\\
$\downarrow$\\
\textbf{JOINT FUTURE-ACTION COMPATIBILITY} $\mathcal I(z,x)=\bigcap_h A_x^*(h)$\\
$\downarrow$\\
\textbf{SCORE UPDATE + MAINTAIN / SELECTIVE REOPENING}\\
$\downarrow$\\
P0 / P1 / P2 / ACQUISITION / RECONSTRUCTED / CONTROLLED-TARGET-CONTRACTION / CANNOT CHECK
\end{minipage}}
\caption{\textbf{Prospective Revision Audit.} Future revision is assessed only after present equivalence and state-removal/reconstruction controls are established. Exact one-step compatibility is governed by the joint acceptable-action intersection over the whole merged representation/evidence cell.}
\label{fig:pra-flow}
\end{figure}
"""


def validation_table() -> str:
    return r"""\begin{table}[t]
\centering
\small
\begin{tabular}{p{0.31\linewidth}p{0.43\linewidth}p{0.17\linewidth}}
\toprule
\textbf{Group} & \textbf{Scope} & \textbf{Result}\\
\midrule
Static partitions & all partitions $n=1\ldots7$; Bell verified & PASS\\
Responsibility semantics & registered responsibility suite + tie control & PASS\\
Deficit identities & rational finite worlds + controls & PASS\\
Dynamic equivalence & direct vs. selector/refinement fixtures & PASS\\
One-bit witness & canonical provenance fixture & $0/1/1$ bits\\
Phase/horizon & P0/P1/P2 + finite-horizon controls & PASS\\
Mutation battery & registered assumption mutations & bounded mixed outcomes\\
Mixed-P2 search & 5,826 small machines & CANNOT CHECK\\
Complete one-step compatibility & $\{a,b\}/\{b,c\}/\{a,c\}$ & PASS\\
\bottomrule
\end{tabular}
\caption{Mechanical validation summary. The three-history control confirms that pairwise overlap does not imply a nonempty joint acceptable-action intersection. CANNOT CHECK is retained rather than promoted to PASS.}
\label{tab:mechanical-validation}
\end{table}
"""


def prepare_markdown(body: str) -> str:
    body = body.replace("∎", r"$\square$")
    body = body.replace(
        "## 4. A one-bit sharp witness\n",
        "## 4. A one-bit sharp witness\n\n\\input{figures/figure1.tex}\n\n",
        1,
    )
    body = body.replace(
        "## 6. Prospective Revision Audit\n",
        "## 6. Prospective Revision Audit\n\n\\input{figures/figure3.tex}\n\n",
        1,
    )
    return NUMERIC_HEADING_RE.sub(r"\1 \2", body)


def pandoc_fragment(markdown_path: Path) -> str:
    completed = run(
        [
            "pandoc",
            str(markdown_path),
            "--from=markdown+raw_tex+tex_math_dollars+pipe_tables+fenced_code_blocks",
            "--to=latex",
            "--wrap=none",
        ],
        capture=True,
    )
    return completed.stdout


def latex_escape_title(text: str) -> str:
    return text.replace("&", r"\&").replace("_", r"\_")


def write_arxiv_tex(out: Path, title: str, abstract_tex: str, body_tex: str) -> None:
    tex = rf"""\documentclass[11pt]{{article}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{amsmath,amssymb,mathtools}}
\usepackage{{booktabs,longtable,array}}
\makeatletter\@ifundefined{{c@none}}{{\newcounter{{none}}}}{{}}\makeatother
\usepackage{{calc}}
\usepackage{{graphicx}}
\usepackage[round]{{natbib}}
\usepackage{{microtype}}
\usepackage{{xurl}}
\usepackage[hidelinks]{{hyperref}}
\providecommand{{\tightlist}}{{\setlength{{\itemsep}}{{0pt}}\setlength{{\parskip}}{{0pt}}}}
\title{{{latex_escape_title(title)}}}
\author{{Author metadata pending human release}}
\date{{}}
\begin{{document}}
\maketitle
\begin{{abstract}}
{abstract_tex}
\end{{abstract}}

{body_tex}

\clearpage
\appendix
\section{{Mechanical validation summary}}
\input{{figures/table3_validation.tex}}

\bibliographystyle{{plainnat}}
\bibliography{{references}}
\end{{document}}
"""
    out.write_text(tex, encoding="utf-8")


def write_jmlr_tex(out: Path, title: str, abstract_tex: str, body_tex: str) -> None:
    tex = rf"""\documentclass[twoside,11pt]{{article}}
\usepackage[preprint]{{jmlr2e}}
\usepackage{{amsmath,mathtools}}
\usepackage{{booktabs,longtable,array}}
\makeatletter\@ifundefined{{c@none}}{{\newcounter{{none}}}}{{}}\makeatother
\usepackage{{calc}}
\usepackage{{microtype}}
\providecommand{{\tightlist}}{{\setlength{{\itemsep}}{{0pt}}\setlength{{\parskip}}{{0pt}}}}
\ShortHeadings{{{SHORT_TITLE}}}{{Author metadata pending}}
\firstpageno{{1}}
\begin{{document}}
\title{{{latex_escape_title(title)}}}
\author{{\name Author metadata pending human release}}
\maketitle
\begin{{abstract}}
{abstract_tex}
\end{{abstract}}
\begin{{keywords}}
representation sufficiency, belief revision, memory compression, decision sufficiency, language models
\end{{keywords}}

{body_tex}

\clearpage
\appendix
\section{{Mechanical validation summary}}
\input{{figures/table3_validation.tex}}

\bibliography{{references}}
\end{{document}}
"""
    out.write_text(tex, encoding="utf-8")


def compile_pdf(package_dir: Path) -> dict[str, object]:
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "manuscript.tex"], cwd=package_dir)
    pdf = package_dir / "manuscript.pdf"
    if not pdf.exists():
        raise RuntimeError("latexmk succeeded but manuscript.pdf is missing")
    page_count = None
    if shutil.which("pdfinfo"):
        info = run(["pdfinfo", str(pdf)], capture=True).stdout
        match = re.search(r"(?m)^Pages:\s+(\d+)$", info)
        if match:
            page_count = int(match.group(1))
    # This surface previously recorded no bibliography fact whatsoever: neither
    # the .bbl, the .log nor the .blg was read, so a silently truncated
    # bibliography compiled, exited 0 and shipped.
    integrity = enforce_package(package_dir, label=package_dir.name)
    bibliography = integrity["bibliography"]
    return {
        "compiled_pdf": str(pdf),
        "compiled_pdf_sha256": sha256(pdf),
        "pdf_size_bytes": pdf.stat().st_size,
        "page_count": page_count,
        "bibliography_rendered": bibliography["bibitem_count"] > 0,
        "bibliography_item_count": bibliography["bibitem_count"],
        "render_integrity": integrity,
    }


def write_readme(path: Path, *, venue: str) -> None:
    path.write_text(
        f"# {venue} mechanical release candidate\n\n"
        "This package is generated from the frozen V12 scientific master. It does not "
        "authorize public release or journal submission. Before release, humans must supply "
        "the final author list/order, affiliations, acknowledgments/funding where applicable, "
        "arXiv category/license or journal submission metadata, and approve the scientific bytes.\n\n"
        "No empirical deployed-LLM result is claimed. The three-history checker is a "
        "reproducibility-only control for the exact one-step intersection criterion.\n",
        encoding="utf-8",
    )


def assemble(root: Path, out_root: Path, jmlr_style: Path | None, compile_requested: bool) -> dict[str, object]:
    paper_root = root / "papers" / "llm-machine-epistemics"
    master = paper_root / "MANUSCRIPT_V12_ARXIV_JMLR_FINAL.md"
    proof_appendix = paper_root / "PROOF_APPENDIX_V1.md"
    bib_paths = [paper_root / "REFERENCES_V1.bib", paper_root / "REFERENCES_CLASSICS_SUPPLEMENT_V1.bib"]

    audit = audit_surface(master, proof_appendix, bib_paths)
    title, abstract_md, body_md = split_master(master.read_text(encoding="utf-8"))
    prepared = prepare_markdown(body_md)

    temp = out_root / "_build"
    if temp.exists():
        shutil.rmtree(temp)
    temp.mkdir(parents=True)
    body_md_path = temp / "body.md"
    abstract_md_path = temp / "abstract.md"
    body_md_path.write_text(prepared, encoding="utf-8")
    abstract_md_path.write_text(abstract_md + "\n", encoding="utf-8")
    body_tex = pandoc_fragment(body_md_path)
    abstract_tex = pandoc_fragment(abstract_md_path).strip()

    packages: dict[str, object] = {}
    for venue in ("arxiv_v1", "jmlr_v1"):
        package = out_root / venue
        if package.exists():
            shutil.rmtree(package)
        (package / "figures").mkdir(parents=True)
        (package / "supplement_or_appendix").mkdir(parents=True)

        bib_summary = merge_bibliographies(bib_paths, package / "references.bib")
        (package / "figures" / "figure1.tex").write_text(figure_one(), encoding="utf-8")
        (package / "figures" / "figure3.tex").write_text(figure_three(), encoding="utf-8")
        (package / "figures" / "table3_validation.tex").write_text(validation_table(), encoding="utf-8")
        write_readme(package / "README_RELEASE.md", venue=venue)

        if proof_appendix.exists():
            proof_temp = temp / "proof_appendix.md"
            proof_temp.write_text(proof_appendix.read_text(encoding="utf-8").replace("∎", r"$\square$"), encoding="utf-8")
            (package / "supplement_or_appendix" / "proof_appendix.tex").write_text(
                pandoc_fragment(proof_temp), encoding="utf-8"
            )

        if venue == "arxiv_v1":
            write_arxiv_tex(package / "manuscript.tex", title, abstract_tex, body_tex)
        else:
            if jmlr_style is None or not jmlr_style.exists():
                raise FileNotFoundError("JMLR assembly requires --jmlr-style pointing to official jmlr2e.sty")
            shutil.copy2(jmlr_style, package / "jmlr2e.sty")
            write_jmlr_tex(package / "manuscript.tex", title, abstract_tex, body_tex)

        package_result: dict[str, object] = {
            "bibliography": bib_summary,
            "manuscript_tex_sha256": sha256(package / "manuscript.tex"),
            "references_bib_sha256": sha256(package / "references.bib"),
            "figure_hashes": {
                p.name: sha256(p) for p in sorted((package / "figures").glob("*.tex"))
            },
        }
        if compile_requested:
            package_result.update(compile_pdf(package))
        packages[venue] = package_result

    receipt = {
        "schema": "orion-v2.llm-pra-mechanical-release.v1",
        "scientific_master": str(master.relative_to(root)),
        "scientific_master_sha256": sha256(master),
        "proof_appendix_sha256": sha256(proof_appendix) if proof_appendix.exists() else None,
        "audit": audit,
        "packages": packages,
        "human_release_authority": False,
        "scientific_claims_changed": False,
        "empirical_llm_result_added": False,
    }
    (out_root / "release_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out-root", type=Path, required=True)
    parser.add_argument("--jmlr-style", type=Path)
    parser.add_argument("--compile", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    out_root = args.out_root.resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    receipt = assemble(root, out_root, args.jmlr_style, args.compile)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
