#!/usr/bin/env python3
"""E30-R13 evaluation lane: the PC-R6 full-regression evaluator, one new cell.

Derived from ``research/experiments/e30-r12/e30_r12_fullreg_eval.py`` by substituting
the cell name and the design id, and nothing else.  E30-R12's copy is frozen terminal
and is not edited; the R13 lane must present its own cell because pooling two campaign
identities in one cell is exactly the mixing the R12 receipt refused.

Registered in ``E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1`` section 9.  This module contains
**no evaluation logic of its own**.  It imports
``research/experiments/pc-r6/pc_r6_fullreg_eval.py`` (which in turn imports the frozen
E30-R11 adapter verbatim), registers an ``e30r13`` cell on it, and delegates every stage.
That is deliberate: the design's apply-rate diagnostic (D1) compares R13's apply rate to
PC-R6's measured per-arm rates, and the comparison is only apples-to-apples if the same
code computes both.  Forking the evaluator would silently break that.

Two places in the PC-R6 runner are keyed to its own two cell names, and this wrapper
adapts around them without editing the imported module:

``manifest``
    PC-R6's manifest stage is genuinely its own study's: it stamps a
    ``campaign-pc-r6-fullreg-e30r11-e60-…`` id, records PC-R6's in-repo truth anchors as
    inputs, and keys every ledger label to its cell names.  Reusing it under a name alias
    would label R13's own ``run/`` tree as ``e30r11/…`` -- a provenance lie in the one
    artifact whose job is provenance.  The wrapper therefore builds R13's input manifest
    itself.  This stage performs no measurement: it only hashes inputs, so implementing it
    here costs none of the evaluator-identity property that matters for D1.

``gr0a``
    PC-R6 read its truth vector from the in-repo E30-R11 rollup.  R13 has no prior
    vector, so its GR0a is *self-consistency*: the campaign's own frozen-lane
    ``evaluations/`` records are the truth and the full-regression lane must reproduce
    them bit-exactly.  That is exactly what the runner's non-``e30r11`` branch already
    does (``frozen_vector_from_records``), so the cell simply must not be named
    ``e30r11``.  The E60-specific external anchor does not apply and is disabled.

``gr0b``
    The gold known-answer control selects its cell by the literal name ``e30r11``.  Its
    body is otherwise cell-generic -- its scratch record paths are a hardcoded string
    rather than the cell name -- so the wrapper passes a cell whose ``name`` attribute is
    aliased for selection only, and the measurement runs verbatim.  The campaign root,
    tasks and gold patches are R13's throughout.  One consequence is cosmetic and
    recorded here rather than papered over: the stage labels its evaluator_private reads
    ``e30r11/evaluator_private/<task>``.  For R13 that label is accidentally accurate,
    because ``$R13/evaluator_private`` is a symlink to R11's frozen oracle tree; it would
    be a provenance defect if this wrapper were ever reused against a campaign with its
    own private tree, and the alias must then be revisited.

Stages, all delegated: ``manifest``, ``gr0a`` (``--execute`` per index, then collect),
``gr0b``, ``gr0`` (combine), ``suite`` (``--execute`` per index), ``rollup``,
``list-indices``.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from typing import Any

DESIGN_ID = "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1"
CELL_NAME = "e30r13"
ARMS = ["F2_ORION_METABOLIC_FULL", "F0_PARENT_FEDERATION",
        "SAME_MODEL_REFLECTION", "SIMPLE_DIRECT"]
REPS = ["1", "2", "3"]
EXPECTED_EVALUATIONS = 480
# Set by --e30r13-campaign; the cell's campaign-name check is bound to the actual
# directory name at load time because R13's campaign id carries a run-time manifest8.
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
    """Add the ``e30r13`` cell; PC-R6's own cells stay registered but unused."""
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
    parser.add_argument("--e30r13-campaign", type=Path, required=True,
                        help="the E30-R13 campaign directory (contains run/confirmatory-r*)")
    parser.add_argument("--pc-r6-runner", type=Path, default=DEFAULT_PC_R6_RUNNER)
    return parser


def stage_manifest(pc, args, cell) -> int:
    """R13's own sha256 input ledger (see the module docstring for why not PC-R6's)."""
    manifest = pc.Manifest()
    for rep in cell.reps:
        manifest.record(cell.run / f"confirmatory-r{rep}" / "frozen_tasks.json",
                        f"{CELL_NAME}/run/confirmatory-r{rep}/frozen_tasks.json")
        for arm in cell.arms:
            for task_id in cell.task_ids:
                manifest.record(cell.response_path(rep, arm, task_id),
                                f"{CELL_NAME}/run/confirmatory-r{rep}/responses/{arm}/{task_id}.json")
                evaluation = cell.evaluation_path(rep, arm, task_id)
                if evaluation.is_file():
                    manifest.record(evaluation,
                                    f"{CELL_NAME}/run/confirmatory-r{rep}/evaluations/{arm}/{task_id}.json")
                request = (cell.run / f"confirmatory-r{rep}" / "requests" / arm / f"{task_id}.json")
                if request.is_file():
                    manifest.record(request,
                                    f"{CELL_NAME}/run/confirmatory-r{rep}/requests/{arm}/{task_id}.json")
    for task_id in cell.task_ids:
        workspace = cell.workspace(task_id)
        for name in ("bugsinpy_run_test.sh", "bugsinpy_bug.info", "bugsinpy_requirements.txt"):
            if (workspace / name).is_file():
                manifest.record(workspace / name,
                                f"{CELL_NAME}/evaluator_private/{task_id}/{name}")
        identity = pc.workspace_identity(workspace)
        manifest.entries[f"{CELL_NAME}/evaluator_private/{task_id}/@HEAD"] = identity["head"]
        manifest.entries[f"{CELL_NAME}/evaluator_private/{task_id}/@STATUS"] = \
            identity["status_sha256"]
        for rel, digest in sorted(identity["deviating_files"].items()):
            manifest.entries[f"{CELL_NAME}/evaluator_private/{task_id}/{rel}"] = digest
    for path, label in (
        (cell.root / "SETUP_RECEIPT.json", f"{CELL_NAME}/SETUP_RECEIPT.json"),
        (cell.root / "RUN_IDENTITY.json", f"{CELL_NAME}/RUN_IDENTITY.json"),
        (args.adapter, "frozen_lane_adapter"),
    ):
        if Path(path).is_file():
            manifest.record(Path(path), label)
    for task_id, gold in pc.select_gr0b_tasks(cell, args):
        manifest.record(gold, f"gold/{task_id}/bug_patch.txt")
    digest = manifest.write(args.out / "E30_R13_INPUT_MANIFEST.sha256")
    campaign_id = f"campaign-e30-r13-fullreg-{args.date}-{digest[:8]}"
    pc.write_json(args.out / "E30_R13_INPUT_MANIFEST.json", {
        "schema_version": "orion.v2.e30-r13-input-manifest.v1",
        "lane_version": pc.LANE_VERSION, "design": DESIGN_ID,
        "generated_utc": pc.utc_now(), "entry_count": len(manifest.entries),
        "manifest_sha256": digest, "manifest8": digest[:8], "campaign_id": campaign_id,
        "cells": {CELL_NAME: {"root": str(cell.root), "arms": cell.arms, "reps": cell.reps,
                              "tasks": len(cell.task_ids),
                              "expected_evaluations": cell.expected_evaluations()}},
        "frozen_lane_adapter_sha256": manifest.entries.get("frozen_lane_adapter"),
        "imported_runner": str(args.pc_r6_runner),
        "imported_runner_sha256": pc.sha256_file(Path(args.pc_r6_runner)),
    })
    print(json.dumps({"campaign_id": campaign_id, "entries": len(manifest.entries)}))
    return 0


def _receipt_alias(out: Path, source: str, target: str) -> None:
    src = out / source
    if src.is_file():
        shutil.copyfile(src, out / target)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # The runner path must be known before its parser exists, so read it first.
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--pc-r6-runner", type=Path, default=DEFAULT_PC_R6_RUNNER)
    pre.add_argument("--e30r13-campaign", type=Path)
    known, _ = pre.parse_known_args(argv)
    if known.e30r13_campaign is None:
        print("LANE_ERROR: --e30r13-campaign is required", file=sys.stderr)
        return 2
    pc = load_pc_r6(known.pc_r6_runner)
    register_cell(pc, known.e30r13_campaign)

    args = build_parser(pc).parse_args(argv)
    args.out = args.out.resolve()
    args.cells = CELL_NAME
    # R13's cell carries no external anchor: its truth is its own campaign records.
    args.skip_e60_anchor = True
    manifest = pc.Manifest()
    try:
        if args.stage == "gr0":
            rc = pc.stage_gr0_combine(args)
            _receipt_alias(args.out, "PC_R6_GR0_RECEIPT.json", "E30_R13_GR0_RECEIPT.json")
            return rc
        cell = pc.Cell(CELL_NAME, args.e30r13_campaign, manifest,
                       allow_partial=args.allow_partial_cells)
        cells = [cell]
        if args.adapter is None:
            args.adapter = args.e30r13_campaign / "run" / "e30_r11_arm_eval_frozen_lane.py"
        args.adapter = args.adapter.resolve()
        if args.expect_adapter_sha256 and pc.sha256_file(args.adapter) != args.expect_adapter_sha256:
            raise pc.LaneError(
                f"adapter sha256 mismatch at {args.adapter}; expected {args.expect_adapter_sha256}")
        if args.stage == "list-indices":
            for index, (cell_name, task_id) in enumerate(pc.plan_indices(cells)):
                print(f"{index}\t{cell_name}\t{task_id}")
            return 0
        if args.stage == "manifest":
            return stage_manifest(pc, args, cell)
        if args.stage == "gr0a":
            if args.execute:
                return pc.stage_execute(args, cells, manifest, kind="records_gr0a")
            rc = pc.stage_gr0a_collect(args, cells, manifest)
            _receipt_alias(args.out, "PC_R6_GR0A_RECEIPT.json", "E30_R13_GR0A_RECEIPT.json")
            return rc
        if args.stage == "gr0b":
            # Selection alias only -- see the module docstring.  Every path, task and
            # gold patch the stage touches comes from the R13 campaign root.
            cell.name = "e30r11"
            rc = pc.stage_gr0b(args, cells, manifest)
            cell.name = CELL_NAME
            _receipt_alias(args.out, "PC_R6_GR0B_RECEIPT.json", "E30_R13_GR0B_RECEIPT.json")
            return rc
        if args.stage == "suite":
            return pc.stage_execute(args, cells, manifest, kind="records")
        if args.stage == "rollup":
            rc = pc.stage_rollup(args, cells, manifest)
            _receipt_alias(args.out, "PC_R6_FULLREG_RAW_ROLLUP_V1.json",
                           "E30_R13_FULLREG_RAW_ROLLUP_V1.json")
            return rc
        raise pc.LaneError(f"unknown stage {args.stage}")
    except pc.LaneError as exc:
        print(f"LANE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
