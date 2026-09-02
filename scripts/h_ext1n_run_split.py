#!/usr/bin/env python3
"""Dispatch + evaluate one H-EXT-1N split (N1-DEV or N1-EVAL) with the model arms.

Reuses the FM/FG harness dispatch()/evaluate() UNCHANGED (private oracle hash-committed,
deleted for the whole child dispatch, restored and re-hashed; missing/failed responses
scored as MISSING rows, never as wrong) and scripts/orion_pd_arms.py as the arm command,
exactly as the H-EXT-1 prospective cell did. One codex call per (task, arm).

Environment (as in the H-EXT-1 prospective cell on billy-old):
  ORION_CODEX_BIN=/home/billy/.npm-global/bin/codex   ORION_CODEX_MODEL=gpt-5.5
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = ROOT / "scripts/run_formal_discovery_generated_suite.py"
PD_ARMS_PATH = ROOT / "scripts/orion_pd_arms.py"
ARMS = ["P_D_FULL", "P_D_MINUS_DEPENDENCE", "STRONGEST_ASSURANCE_FEDERATION"]


def load_suite():
    spec = importlib.util.spec_from_file_location("orion_formal_generated_suite", SUITE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load FM/FG harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--study-dir", type=Path, required=True)
    p.add_argument("--max-concurrency", type=int, default=3)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--evaluate-only", action="store_true")
    args = p.parse_args(argv)
    suite = load_suite()
    os.environ.setdefault("ORION_FORMAL_ARM_COMMAND", " ".join(shlex.quote(x) for x in [sys.executable, str(PD_ARMS_PATH)]))
    if not args.evaluate_only:
        suite.dispatch(args.study_dir, ARMS, args.max_concurrency, args.overwrite)
        receipt = suite.read_json(args.study_dir / "DISPATCH_RECEIPT.json")
        print(json.dumps({"jobs": len(receipt["jobs"]), "all_returncodes_zero": receipt["all_returncodes_zero"],
                          "oracle_restored_hash_match": receipt["oracle_restored_hash_match"]}))
    suite.evaluate(args.study_dir, ARMS)
    summary = suite.read_json(args.study_dir / "EVALUATION_SUMMARY.json")["summary"]
    print(json.dumps({arm: {k: v[k] for k in ("correct", "tasks", "accuracy", "missing_or_invalid", "run_valid")} for arm, v in summary.items()}, indent=1))
    return 0 if all(v["run_valid"] for v in summary.values()) else 3


if __name__ == "__main__":
    raise SystemExit(main())
