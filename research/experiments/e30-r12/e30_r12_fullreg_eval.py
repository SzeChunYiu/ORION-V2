#!/usr/bin/env python3
"""E30-R12 evaluation lane: the PC-R6 full-regression evaluator, one new cell.

Registered in ``E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1`` section 8.  This module contains
**no evaluation logic of its own**.  It imports
``research/experiments/pc-r6/pc_r6_fullreg_eval.py`` (which in turn imports the frozen
E30-R11 adapter verbatim), registers an ``e30r12`` cell on it, and delegates every stage.
That is deliberate: the design's apply-rate diagnostic (D1) compares R12's apply rate to
PC-R6's measured per-arm rates, and the comparison is only apples-to-apples if the same
code computes both.  Forking the evaluator would silently break that.

Two places in the PC-R6 runner are keyed to its own two cell names, and this wrapper
adapts around them without editing the imported module:

``gr0a``
    PC-R6 read its truth vector from the in-repo E30-R11 rollup.  R12 has no prior
    vector, so its GR0a is *self-consistency*: the campaign's own frozen-lane
    ``evaluations/`` records are the truth and the full-regression lane must reproduce
    them bit-exactly.  That is exactly what the runner's non-``e30r11`` branch already
    does (``frozen_vector_from_records``), so the cell simply must not be named
    ``e30r11``.  The E60-specific external anchor does not apply and is disabled.

``gr0b``
    The gold known-answer control selects its cell by the literal name ``e30r11``.  The
    stage body is otherwise cell-generic (its record paths are a hardcoded string, not
    the cell name), so the wrapper passes a cell whose ``name`` attribute is aliased for
    selection only.  The campaign root, tasks and gold patches are R12's throughout.

Stages, all delegated: ``manifest``, ``gr0a`` (``--execute`` per index, then collect),
``gr0b``, ``gr0`` (combine), ``suite`` (``--execute`` per index), ``rollup``,
``list-indices``.
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path
from typing import Any

DESIGN_ID = "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1"
CELL_NAME = "e30r12"
ARMS = ["F2_ORION_METABOLIC_FULL", "F0_PARENT_FEDERATION",
        "SAME_MODEL_REFLECTION", "SIMPLE_DIRECT"]
REPS = ["1", "2", "3"]
EXPECTED_EVALUATIONS = 480
# Set by --e30r12-campaign; the cell's campaign-name check is bound to the actual
# directory name at load time because R12's campaign id carries a run-time manifest8.
DEFAULT_PC_R6_RUNNER = (
    Path(__file__).resolve().parents[1] / "pc-r6" / "pc_r6_fullreg_eval.py"
)


def load_pc_r6(path: Path):
    """Import the PC-R6 runner by path (it is a script, not an installed module)."""
    spec = importlib.util.spec_from_file_location("pc_r6_fullreg_eval", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import the PC-R6 runner at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pc_r6_fullreg_eval"] = module
    spec.loader.exec_module(module)
    return module


def register_cell(pc, campaign_dir: Path) -> None:
    """Add the ``e30r12`` cell; PC-R6's own cells stay registered but unused."""
    pc.CELLS[CELL_NAME] = {
        "campaign": campaign_dir.resolve().name,
        "arms": list(ARMS),
        "reps": list(REPS),
        "evaluations": EXPECTED_EVALUATIONS,
        "truth": ("the campaign's own frozen-lane evaluation records "
                  "(run/confirmatory-r{1,2,3}/evaluations/<ARM>/<task>.json); GR0a is "
                  "self-consistency between the two evaluators over the same 480 proposals"),
    }
    if CELL_NAME not in pc.CELL_ORDER:
        pc.CELL_ORDER.append(CELL_NAME)


def build_parser(pc) -> argparse.ArgumentParser:
    parser = pc.build_parser()
    parser.add_argument("--e30r12-campaign", type=Path, required=True,
                        help="the E30-R12 campaign directory (contains run/confirmatory-r*)")
    parser.add_argument("--pc-r6-runner", type=Path, default=DEFAULT_PC_R6_RUNNER)
    return parser


def _receipt_alias(out: Path, source: str, target: str) -> None:
    src = out / source
    if src.is_file():
        shutil.copyfile(src, out / target)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # The runner path must be known before its parser exists, so read it first.
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--pc-r6-runner", type=Path, default=DEFAULT_PC_R6_RUNNER)
    pre.add_argument("--e30r12-campaign", type=Path)
    known, _ = pre.parse_known_args(argv)
    if known.e30r12_campaign is None:
        print("LANE_ERROR: --e30r12-campaign is required", file=sys.stderr)
        return 2
    pc = load_pc_r6(known.pc_r6_runner)
    register_cell(pc, known.e30r12_campaign)

    args = build_parser(pc).parse_args(argv)
    args.out = args.out.resolve()
    args.cells = CELL_NAME
    # R12's cell carries no external anchor: its truth is its own campaign records.
    args.skip_e60_anchor = True
    manifest = pc.Manifest()
    try:
        if args.stage == "gr0":
            rc = pc.stage_gr0_combine(args)
            _receipt_alias(args.out, "PC_R6_GR0_RECEIPT.json", "E30_R12_GR0_RECEIPT.json")
            return rc
        cell = pc.Cell(CELL_NAME, args.e30r12_campaign, manifest,
                       allow_partial=args.allow_partial_cells)
        cells = [cell]
        if args.adapter is None:
            args.adapter = args.e30r12_campaign / "run" / "e30_r11_arm_eval_frozen_lane.py"
        args.adapter = args.adapter.resolve()
        if args.expect_adapter_sha256 and pc.sha256_file(args.adapter) != args.expect_adapter_sha256:
            raise pc.LaneError(
                f"adapter sha256 mismatch at {args.adapter}; expected {args.expect_adapter_sha256}")
        if args.stage == "list-indices":
            for index, (cell_name, task_id) in enumerate(pc.plan_indices(cells)):
                print(f"{index}\t{cell_name}\t{task_id}")
            return 0
        if args.stage == "manifest":
            rc = pc.stage_manifest(args, cells, manifest)
            _receipt_alias(args.out, "PC_R6_INPUT_MANIFEST.json", "E30_R12_INPUT_MANIFEST.json")
            return rc
        if args.stage == "gr0a":
            if args.execute:
                return pc.stage_execute(args, cells, manifest, kind="records_gr0a")
            rc = pc.stage_gr0a_collect(args, cells, manifest)
            _receipt_alias(args.out, "PC_R6_GR0A_RECEIPT.json", "E30_R12_GR0A_RECEIPT.json")
            return rc
        if args.stage == "gr0b":
            # Selection alias only -- see the module docstring.  Every path, task and
            # gold patch the stage touches comes from the R12 campaign root.
            cell.name = "e30r11"
            rc = pc.stage_gr0b(args, cells, manifest)
            cell.name = CELL_NAME
            _receipt_alias(args.out, "PC_R6_GR0B_RECEIPT.json", "E30_R12_GR0B_RECEIPT.json")
            return rc
        if args.stage == "suite":
            return pc.stage_execute(args, cells, manifest, kind="records")
        if args.stage == "rollup":
            rc = pc.stage_rollup(args, cells, manifest)
            _receipt_alias(args.out, "PC_R6_FULLREG_RAW_ROLLUP_V1.json",
                           "E30_R12_FULLREG_RAW_ROLLUP_V1.json")
            return rc
        raise pc.LaneError(f"unknown stage {args.stage}")
    except pc.LaneError as exc:
        print(f"LANE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
