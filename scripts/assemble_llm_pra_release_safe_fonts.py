#!/usr/bin/env python3
"""Font-safe wrapper for the frozen PRA release assembler.

The scientific master and generated scientific prose are unchanged.  The
wrapper only changes the TeX microtype option in generated venue templates to
avoid pdfTeX font-expansion failures on hosted runners with non-scalable font
variants.
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


base.write_arxiv_tex = _patch_writer(base.write_arxiv_tex)
base.write_jmlr_tex = _patch_writer(base.write_jmlr_tex)


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
