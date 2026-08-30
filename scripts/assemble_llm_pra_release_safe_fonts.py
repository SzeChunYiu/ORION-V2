#!/usr/bin/env python3
"""Packaging-safe wrapper for the frozen PRA release assembler.

The scientific master and generated scientific prose are unchanged. The wrapper
only adjusts serialization/toolchain details needed for reliable PDF builds:

- disable pdfTeX microtype font expansion on hosted runners;
- preserve the frozen master's `\\[ ... \\]` / `\\( ... \\)` math delimiters as
  TeX math instead of escaping their contents as ordinary text; and
- shift body headings one level upward after the standalone manuscript title is
  removed, so top-level sections render as 1, 2, ... rather than 0.1, 0.2, ....
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import assemble_llm_pra_release as base


def _patch_writer(writer):
    def wrapped(out: Path, *args, **kwargs):
        writer(out, *args, **kwargs)
        text = out.read_text(encoding="utf-8")
        text = text.replace(
            r"\usepackage{microtype}",
            r"\usepackage[expansion=false]{microtype}",
        )
        out.write_text(text, encoding="utf-8")
    return wrapped


def _pandoc_fragment(markdown_path: Path) -> str:
    completed = base.run(
        [
            "pandoc",
            str(markdown_path),
            "--from=markdown+raw_tex+tex_math_dollars+tex_math_single_backslash+pipe_tables+fenced_code_blocks",
            "--to=latex",
            "--shift-heading-level-by=-1",
            "--wrap=none",
        ],
        capture=True,
    )
    return completed.stdout


base.write_arxiv_tex = _patch_writer(base.write_arxiv_tex)
base.write_jmlr_tex = _patch_writer(base.write_jmlr_tex)
base.pandoc_fragment = _pandoc_fragment


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
    receipt = base.assemble(root, out_root, args.jmlr_style, args.compile)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
