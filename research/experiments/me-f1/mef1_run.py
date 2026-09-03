#!/usr/bin/env python3
"""ME-F1 frontier open-discovery study runner (frozen with design V1).

Stages
  selftest   Hard pre-run validity, no model calls.  Parent fidelity
             (``mef1_parents.fidelity_selftests``); G0a hand-authored warrant-validity
             fixtures covering EVERY licensed and EVERY forbidden inference in
             ``mef1_model.warrant_is_valid``, including the block-crossing case; G0b
             toolbox soundness on development campaigns (every ``WITNESS_FOUND`` verified
             independently against the UNPREPROCESSED rung, every preprocess mode
             satisfiability-preserving, ground truth monotone within every block); G0d
             generator validity (every rung of an ``F_PLANTED`` campaign is ground-truth
             SAT; ``F_CRITICAL`` campaigns carry both SAT and UNSAT rungs).  Writes
             ``results/ME_F1_SELFTEST_REPORT.json`` and exits 1 if any hard check fails.

  calibrate  ``design["calibration"]``, exactly.  Ascend the difficulty ladder; at each
             rung run ``C_UNIFORM_ALLOCATION`` on ``dev_campaigns_per_level`` development
             campaigns and score the PRIMARY endpoint itself (not a proxy).  Every
             terminal is tested explicitly and none is a fall-through: WINDOW_HIT,
             SUITE_STILL_SATURATED, LADDER_OVERSHOT_NO_WINDOW_HIT,
             SUITE_AT_FLOOR_AT_FIRST_RUNG, CALIBRATION_INVALID_INCONSISTENT_GROUND_TRUTH.
             Writes ``results/ME_F1_CALIBRATION_RECEIPT.json``.  A terminal other than
             WINDOW_HIT is a result, never a reason to re-tune the ladder
             (``calibration.if_no_window_hit``).

  dev        Development split (public dev seed, capped at 8 campaigns).  Never protected
             evidence.  Writes ``ME_F1_DEVELOPMENT_{RESULTS,ANALYSIS}_V1.json``.

  protected  The single protected run.  Refuses unless PROTECTED_RUN_AUTHORIZATION.json is
             present next to this script with ``human_written=true``, a
             ``human_written_token`` of at least 16 characters and an
             ``acknowledged_design_sha256`` equal to the sha256 of the frozen design JSON
             (exit 3), AND the custody seed file's sha256 equals the commitment frozen in
             the design (exit 4).  Only after every check passes does it generate the
             protected split, compute ground truth, run the arms per
             ``design["arm_allocation"]`` and analyze in the SAME invocation.

  analyze    Score a results file against its custody file: per-arm aggregates, resource
             curves, the M-vs-B5 paired contrast, the integrity dict, the power dict, the
             frozen gates and the pre-registered route.  Writes the ANALYSIS json and a
             readable markdown rendering.

Design: ME_F1_FRONTIER_OPEN_DISCOVERY_STUDY_DESIGN_V1.json.  Nothing here is authorizing:
a PARENT_SUFFICIENT terminal is a successful outcome of this study, and no route grants
field status, novelty or publication authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from mef1_arms import (ALL_ARMS, DETERMINISTIC_ARMS, MODEL_ARMS,  # noqa: E402
                       run_deterministic_arm, run_model_arm)
from mef1_channel import call_control, probe_channel  # noqa: E402
from mef1_generator import make_split  # noqa: E402
from mef1_model import (Action, ActionResult, Campaign, Claim,  # noqa: E402
                        CampaignRecord, canonical_json, warrant_is_valid)
from mef1_parents import fidelity_selftests  # noqa: E402
from mef1_reference import check_consistency, ground_truth, monotone_repair  # noqa: E402
from mef1_score import (aggregate, evaluate_gates, paired_contrast,  # noqa: E402
                        resource_curve, route, score_campaign)
from mef1_stats import mde_at_n  # noqa: E402
from mef1_toolbox import (Meter, _base_clauses, _clauses_for, run_action,  # noqa: E402
                          verify_witness)

DESIGN_JSON = HERE / "ME_F1_FRONTIER_OPEN_DISCOVERY_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"

SCHEMA_RESULTS = "orion.v2.me-f1.frontier-study-results.v1"
SCHEMA_CUSTODY = "orion.v2.me-f1.frontier-study-results.v1.expected-custody"
SCHEMA_ANALYSIS = "orion.v2.me-f1.frontier-study-analysis.v1"

M_ARM = "M_ME_FRONTIER_CONTROL"
B5_ARM = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"
SIMPLE_ARM = "SIMPLE_DIRECT"
INTEGRITY_ARMS = (SIMPLE_ARM, B5_ARM, M_ARM)

#: Five alphas per block and 20 rungs per campaign (design ``power.clustering_note``)
#: fix the campaign at four independent sub-ladders.
N_BLOCKS = 4

#: The development split is a glue check, never evidence; the cap is what keeps it one.
DEV_CAP = 8

#: Hard ceiling on parallel model calls.  The binding constraint is the SHARED codex
# account, not the host: while the SD70 lane is drawing on the same account the operating
# limit is 3, rising to this ceiling only once that job is terminal.  The coordinator set
# 6 as the maximum; exceeding it risks throttling, and a campaign truncated by throttling
# is silent damage that leaves no trace in a receipt.
MAX_CONCURRENCY = 6

_DESIGN: dict[str, Any] | None = None


def design() -> dict[str, Any]:
    """The frozen design JSON.  Every constant this runner uses comes from here."""
    global _DESIGN
    if _DESIGN is None:
        _DESIGN = json.loads(DESIGN_JSON.read_text())
    return _DESIGN


def design_sha256() -> str:
    """sha256 of the design file's RAW BYTES -- what an authorization acknowledges."""
    return hashlib.sha256(DESIGN_JSON.read_bytes()).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


#: Every source file whose bytes can change what a run measures.  The attestation below
#: is computed INSIDE the process that does the measuring, from the files the interpreter
#: actually imported -- because a deploy step that printed success is not evidence about
#: the code that ran.  This exists because an earlier G0e measurement could not answer the
#: question "what code produced this number?" from its own artifact.
SOURCE_GLOB = "mef1_*.py"

SOURCE_MANIFEST = HERE / "ME_F1_SOURCE_MANIFEST_V1.json"

#: Exit codes.  "Could not check" is kept structurally distinct from "checked and fine":
#: conflating them is the silent failure this module exists to prevent.
EXIT_SOURCE_DRIFT = 5        # checked, and the executing tree is NOT the frozen tree
EXIT_SOURCE_UNCHECKABLE = 6  # nothing to check against: the question was not answered


def source_provenance() -> dict[str, Any]:
    """In-job attestation of the executing tree.

    Hashes every ``mef1_*.py`` beside this module, plus the design JSON, and records the
    host and interpreter.  It also verifies that the ``mef1_*`` modules Python actually
    imported came from this directory -- otherwise the file hashes would describe a tree
    that is not the one executing, which is precisely the failure being guarded against.
    """
    import platform
    files = {p.name: sha256_file(p) for p in sorted(HERE.glob(SOURCE_GLOB))}
    violations: list[str] = []
    for name, mod in sorted(sys.modules.items()):
        if not name.startswith("mef1_"):
            continue
        f = getattr(mod, "__file__", None)
        if f is None:
            continue
        rp = Path(f).resolve()
        if rp.parent != HERE:
            violations.append(f"{name} imported from {rp.parent}")
        elif rp.name not in files:
            violations.append(f"{name} imported from an unhashed file {rp.name}")
    combined = hashlib.sha256(
        "".join(f"{n}:{h}\n" for n, h in sorted(files.items())).encode()).hexdigest()
    return {
        "source_files_sha256": files,
        "combined_source_sha256": combined,
        "design_sha256": design_sha256(),
        "imported_from": str(HERE),
        "import_path_violations": violations,
        "hostname": platform.node(),
        "python_version": platform.python_version(),
        "executed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def verify_source_against_manifest() -> tuple[int, dict[str, Any]]:
    """Compare the live in-job attestation with the frozen manifest.

    Returns ``(code, report)``.  ``0`` only when a manifest exists AND every hash matches
    AND no module was imported from outside this directory.
    """
    live = source_provenance()
    if not SOURCE_MANIFEST.exists():
        return (EXIT_SOURCE_UNCHECKABLE,
                {"checked": False, "reason": "no frozen source manifest exists",
                 "live": live})
    frozen = json.loads(SOURCE_MANIFEST.read_text())
    fh = frozen.get("source_files_sha256") or {}
    lh = live["source_files_sha256"]
    if not fh:
        return (EXIT_SOURCE_UNCHECKABLE,
                {"checked": False, "reason": "frozen manifest carries no file hashes",
                 "live": live})
    drift = sorted({n for n in set(fh) | set(lh) if fh.get(n) != lh.get(n)})
    rep = {
        "checked": True,
        "frozen_combined_source_sha256": frozen.get("combined_source_sha256"),
        "live_combined_source_sha256": live["combined_source_sha256"],
        "drifted_files": drift,
        "n_files_frozen": len(fh), "n_files_live": len(lh),
        "import_path_violations": live["import_path_violations"],
        "match": (not drift) and not live["import_path_violations"],
        "live": live,
    }
    return ((0 if rep["match"] else EXIT_SOURCE_DRIFT), rep)


def announce_provenance(stage: str) -> dict[str, Any]:
    """Print what the running job computed about *itself* before it measures anything.

    A reader auditing a number wants this line, not a deploy log.  A missing manifest is
    reported as ``NOT_CHECKED``; it is never rendered as agreement.
    """
    code, rep = verify_source_against_manifest()
    live = rep["live"]
    print(f"[{stage}] executing tree: combined_source_sha256="
          f"{live['combined_source_sha256']}", flush=True)
    print(f"[{stage}] design_sha256={live['design_sha256']} host={live['hostname']} "
          f"python={live['python_version']} files={len(live['source_files_sha256'])} "
          f"dir={live['imported_from']}", flush=True)
    if rep.get("checked"):
        print(f"[{stage}] frozen source manifest: "
              + ("MATCH" if rep["match"]
                 else f"DRIFT drifted_files={rep['drifted_files']} "
                      f"import_violations={rep['import_path_violations']}"), flush=True)
    else:
        print(f"[{stage}] frozen source manifest: NOT_CHECKED ({rep['reason']}) "
              f"[exit-code class {EXIT_SOURCE_UNCHECKABLE}]", flush=True)
    return rep


def write_source_manifest() -> dict[str, Any]:
    """Freeze the executing tree's hashes so later runs can be checked against it."""
    live = source_provenance()
    live["schema_version"] = SCHEMA_ANALYSIS + ".source-manifest"
    _write_json(SOURCE_MANIFEST, live)
    return live


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True))


# =====================================================================================
# G0a: hand-authored warrant-validity fixtures
# =====================================================================================

#: Two independent sub-ladders of five rungs, which is what makes the block-crossing
#: fixtures below meaningful: rungs 0-4 are block 0, rungs 5-9 are block 1.
FIXTURE_BLOCK_OF: dict[int, int] = {i: (0 if i < 5 else 1) for i in range(10)}


def _fixture_record(*, witnesses: tuple[int, ...] = (), refutations: tuple[int, ...] = (),
                    incomplete_refutations: tuple[int, ...] = (),
                    inconclusive: tuple[int, ...] = ()) -> CampaignRecord:
    """A synthetic execution log.  Only the outcome structure matters to the warrant
    check, which never reads ground truth and never reads a witness's contents."""
    rec = CampaignRecord("G0A-FIXTURE", "FIXTURE")
    for r in witnesses:
        rec.actions.append(ActionResult(Action("local_search", r, 1, "none"),
                                        "WITNESS_FOUND", 0, witness=(True,)))
    for r in refutations:
        rec.actions.append(ActionResult(Action("exact_solve", r, 1, "none"),
                                        "REFUTED", 0, refutation_complete=True))
    for r in incomplete_refutations:
        rec.actions.append(ActionResult(Action("exact_solve", r, 1, "none"),
                                        "REFUTED", 0, refutation_complete=False))
    for r in inconclusive:
        rec.actions.append(ActionResult(Action("local_search", r, 1, "none"),
                                        "INCONCLUSIVE", 0))
    return rec


def warrant_validity_fixtures() -> list[dict[str, Any]]:
    """Every licensed and every forbidden inference, hand-authored (gate G0a).

    The block-crossing cases are the ones the world's independence property turns on:
    evidence earned in one sub-ladder licenses NOTHING in another, and a scorer that
    forgets to say which block a rung belongs to will silently accept the laundering this
    study exists to measure.
    """
    b = FIXTURE_BLOCK_OF
    F: list[dict[str, Any]] = []

    def add(name: str, kind: str, claim: Claim, record: CampaignRecord,
            expected: bool, block_of: dict[int, int] | None = b) -> None:
        F.append({"name": name, "kind": kind, "claim": claim, "record": record,
                  "block_of": block_of, "expected_valid": expected})

    # ---- LICENSED -----------------------------------------------------------------
    add("sat_by_verified_witness_at_this_rung", "LICENSED",
        Claim(2, "SATISFIABLE", "VERIFIED_WITNESS"),
        _fixture_record(witnesses=(2,)), True)
    add("sat_by_closure_from_named_higher_witness", "LICENSED",
        Claim(1, "SATISFIABLE", "MONOTONE_CLOSURE", 4),
        _fixture_record(witnesses=(4,)), True)
    add("sat_by_closure_from_unnamed_higher_witness", "LICENSED",
        Claim(1, "SATISFIABLE", "MONOTONE_CLOSURE", None),
        _fixture_record(witnesses=(4,)), True)
    add("sat_by_closure_source_equals_claimed_rung", "LICENSED",
        Claim(3, "SATISFIABLE", "MONOTONE_CLOSURE", 3),
        _fixture_record(witnesses=(3,)), True)
    add("unsat_by_completed_refutation_at_this_rung", "LICENSED",
        Claim(3, "UNSATISFIABLE", "COMPLETED_REFUTATION"),
        _fixture_record(refutations=(3,)), True)
    add("unsat_by_closure_from_named_lower_refutation", "LICENSED",
        Claim(4, "UNSATISFIABLE", "MONOTONE_CLOSURE", 1),
        _fixture_record(refutations=(1,)), True)
    add("unsat_by_closure_from_unnamed_lower_refutation", "LICENSED",
        Claim(4, "UNSATISFIABLE", "MONOTONE_CLOSURE", None),
        _fixture_record(refutations=(1,)), True)
    add("closure_inside_the_second_block", "LICENSED",
        Claim(6, "SATISFIABLE", "MONOTONE_CLOSURE", 9),
        _fixture_record(witnesses=(9,)), True)
    add("unresolved_carries_warrant_none", "LICENSED",
        Claim(2, "UNRESOLVED", "NONE"), _fixture_record(), True)

    # ---- FORBIDDEN ----------------------------------------------------------------
    # Failing to find a witness licenses NOTHING -- the asymmetry the world is built on.
    add("failure_to_find_is_not_a_refutation", "FORBIDDEN",
        Claim(2, "UNSATISFIABLE", "COMPLETED_REFUTATION"),
        _fixture_record(inconclusive=(2,)), False)
    add("failure_to_find_asserted_without_warrant", "FORBIDDEN",
        Claim(2, "UNSATISFIABLE", "NONE"),
        _fixture_record(inconclusive=(2,)), False)
    add("satisfiable_asserted_without_warrant", "FORBIDDEN",
        Claim(2, "SATISFIABLE", "NONE"),
        _fixture_record(witnesses=(2,)), False)
    # A witness generalises DOWNWARD only.
    add("witness_generalised_upward_named", "FORBIDDEN",
        Claim(3, "SATISFIABLE", "MONOTONE_CLOSURE", 1),
        _fixture_record(witnesses=(1,)), False)
    add("witness_generalised_upward_unnamed", "FORBIDDEN",
        Claim(3, "SATISFIABLE", "MONOTONE_CLOSURE", None),
        _fixture_record(witnesses=(1,)), False)
    # A refutation generalises UPWARD only.
    add("refutation_generalised_downward_named", "FORBIDDEN",
        Claim(1, "UNSATISFIABLE", "MONOTONE_CLOSURE", 3),
        _fixture_record(refutations=(3,)), False)
    add("refutation_generalised_downward_unnamed", "FORBIDDEN",
        Claim(1, "UNSATISFIABLE", "MONOTONE_CLOSURE", None),
        _fixture_record(refutations=(3,)), False)
    add("verified_witness_cannot_license_unsatisfiable", "FORBIDDEN",
        Claim(2, "UNSATISFIABLE", "VERIFIED_WITNESS"),
        _fixture_record(witnesses=(2,)), False)
    add("completed_refutation_cannot_license_satisfiable", "FORBIDDEN",
        Claim(2, "SATISFIABLE", "COMPLETED_REFUTATION"),
        _fixture_record(refutations=(2,)), False)
    add("verified_witness_without_any_witness", "FORBIDDEN",
        Claim(2, "SATISFIABLE", "VERIFIED_WITNESS"), _fixture_record(), False)
    add("refutation_that_did_not_exhaust_the_space", "FORBIDDEN",
        Claim(2, "UNSATISFIABLE", "COMPLETED_REFUTATION"),
        _fixture_record(incomplete_refutations=(2,)), False)
    # Nothing crosses a block boundary.
    add("closure_across_blocks_satisfiable_named", "FORBIDDEN",
        Claim(0, "SATISFIABLE", "MONOTONE_CLOSURE", 7),
        _fixture_record(witnesses=(7,)), False)
    add("closure_across_blocks_satisfiable_unnamed", "FORBIDDEN",
        Claim(0, "SATISFIABLE", "MONOTONE_CLOSURE", None),
        _fixture_record(witnesses=(7,)), False)
    add("closure_across_blocks_unsatisfiable_named", "FORBIDDEN",
        Claim(6, "UNSATISFIABLE", "MONOTONE_CLOSURE", 0),
        _fixture_record(refutations=(0,)), False)
    add("closure_across_blocks_unsatisfiable_unnamed", "FORBIDDEN",
        Claim(6, "UNSATISFIABLE", "MONOTONE_CLOSURE", None),
        _fixture_record(refutations=(0,)), False)
    # An honest non-answer must never be dressed as a licensed one.
    add("unresolved_with_a_non_none_warrant", "FORBIDDEN",
        Claim(2, "UNRESOLVED", "VERIFIED_WITNESS"),
        _fixture_record(witnesses=(2,)), False)

    # ---- UNNAMED: the H-EXT-3 rung-0 interface ------------------------------------
    # A rung-0 arm's schema has no warrant field, so the scorer must decide entitlement
    # from the log.  These fixtures pin BOTH directions: the arm is never penalised for a
    # licence it actually held and did not name, and it is caught the moment it asserts
    # more than it established -- which is the ME-X1 slide the endpoint exists to measure.
    add("unnamed_sat_with_a_witness_at_this_rung", "LICENSED",
        Claim(2, "SATISFIABLE", "UNNAMED"), _fixture_record(witnesses=(2,)), True)
    add("unnamed_sat_closing_down_from_a_higher_witness", "LICENSED",
        Claim(1, "SATISFIABLE", "UNNAMED"), _fixture_record(witnesses=(3,)), True)
    add("unnamed_unsat_with_a_refutation_at_this_rung", "LICENSED",
        Claim(3, "UNSATISFIABLE", "UNNAMED"), _fixture_record(refutations=(3,)), True)
    add("unnamed_unsat_closing_up_from_a_lower_refutation", "LICENSED",
        Claim(4, "UNSATISFIABLE", "UNNAMED"), _fixture_record(refutations=(2,)), True)
    add("unnamed_unresolved_is_an_honest_non_answer", "LICENSED",
        Claim(2, "UNRESOLVED", "UNNAMED"), _fixture_record(), True)
    # THE LAUNDERING CASE: searched, found nothing, asserted UNSATISFIABLE anyway.
    add("unnamed_unsat_on_a_failed_search", "FORBIDDEN",
        Claim(2, "UNSATISFIABLE", "UNNAMED"),
        _fixture_record(incomplete_refutations=(2,)), False)
    add("unnamed_unsat_with_no_evidence_at_all", "FORBIDDEN",
        Claim(2, "UNSATISFIABLE", "UNNAMED"), _fixture_record(), False)
    add("unnamed_sat_with_no_evidence_at_all", "FORBIDDEN",
        Claim(2, "SATISFIABLE", "UNNAMED"), _fixture_record(), False)
    add("unnamed_sat_cannot_close_upward_from_a_lower_witness", "FORBIDDEN",
        Claim(3, "SATISFIABLE", "UNNAMED"), _fixture_record(witnesses=(1,)), False)
    add("unnamed_unsat_cannot_close_downward_from_a_higher_refutation", "FORBIDDEN",
        Claim(1, "UNSATISFIABLE", "UNNAMED"), _fixture_record(refutations=(3,)), False)
    # Block independence binds the unnamed interface exactly as it binds the named one.
    add("unnamed_sat_cannot_cross_a_block_boundary", "FORBIDDEN",
        Claim(0, "SATISFIABLE", "UNNAMED"), _fixture_record(witnesses=(7,)), False)
    add("unnamed_unsat_cannot_cross_a_block_boundary", "FORBIDDEN",
        Claim(6, "UNSATISFIABLE", "UNNAMED"), _fixture_record(refutations=(0,)), False)
    return F


def check_warrant_fixtures() -> dict[str, Any]:
    rows = []
    for fx in warrant_validity_fixtures():
        got, reason = warrant_is_valid(fx["claim"], fx["record"], fx["block_of"])
        rows.append({"name": fx["name"], "kind": fx["kind"],
                     "expected_valid": fx["expected_valid"], "observed_valid": bool(got),
                     "reason": reason, "pass": bool(got) == fx["expected_valid"]})
    return {"n": len(rows), "n_pass": sum(r["pass"] for r in rows),
            "pass": all(r["pass"] for r in rows), "rows": rows}


# =====================================================================================
# campaigns and ground truth
# =====================================================================================


def _block_of(campaign: Campaign) -> dict[int, int]:
    return {r.index: r.block for r in campaign.rungs}


def campaign_ground_truth(campaign: Campaign) -> tuple[dict[int, str], list[Any], bool, str]:
    """Post-hoc ground truth, closed under each block's own monotonicity.

    Returns ``(status_by_rung, truths, consistent, reason)``.  The reference pass depends
    only on the campaign and K, never on any arm.
    """
    gt_cfg = design()["ground_truth"]
    bo = _block_of(campaign)
    truths = monotone_repair(
        ground_truth(campaign, int(gt_cfg["K"]), int(gt_cfg["reference_node_limit"])), bo)
    consistent, reason = check_consistency(truths, bo)
    return ({t.rung: t.status for t in truths}, truths, consistent, reason)


def make_campaigns(seed_text: str, n_critical: int, n_planted: int, n_vars: int,
                   budget_checks: int, n_blocks: int = N_BLOCKS) -> list[Campaign]:
    return make_split(seed_text, {"F_CRITICAL": n_critical, "F_PLANTED": n_planted},
                      n_vars, budget_checks,
                      int(design()["budget"]["max_control_calls_per_campaign"]), n_blocks)


# =====================================================================================
# arm dispatch (bounded concurrency, every model call logged)
# =====================================================================================


def _run_one_job(campaign: Campaign, arm: str,
                 call_fn: Callable[..., Any] | None) -> tuple[CampaignRecord, list[dict]]:
    """One (campaign, arm) job.  Model calls are logged into a per-job list, which the
    main thread merges in deterministic order -- no shared mutable state across workers."""
    entries: list[dict[str, Any]] = []
    if arm not in MODEL_ARMS:
        t0 = time.perf_counter()
        rec = run_deterministic_arm(campaign, arm)
        rec.wall_ms = int((time.perf_counter() - t0) * 1000)
        return rec, entries

    base = call_fn or call_control

    def logged(prompt: str, schema: dict[str, Any], **kw: Any) -> Any:
        receipt = base(prompt, schema, **kw)
        # design custody.determinism: every call's prompt sha256, response body, requested
        # model, served-model triad, tokens and wall time are persisted.
        entries.append({"campaign_id": campaign.campaign_id, "arm": arm,
                        **receipt.as_json(), "body": receipt.body})
        return receipt

    rec = run_model_arm(campaign, arm, call_fn=logged)
    return rec, entries


def run_arms(jobs: list[tuple[Campaign, str]], max_concurrency: int,
             call_fn: Callable[..., Any] | None = None
             ) -> tuple[dict[tuple[str, str], CampaignRecord], list[dict]]:
    """Run every (campaign, arm) job.  Concurrency is capped at the frozen channel budget."""
    workers = max(1, min(int(max_concurrency), MAX_CONCURRENCY))
    out: dict[tuple[str, str], CampaignRecord] = {}
    logs: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [(c, a, pool.submit(_run_one_job, c, a, call_fn)) for c, a in jobs]
        for campaign, arm, fut in futures:
            rec, entries = fut.result()
            out[(campaign.campaign_id, arm)] = rec
            logs.extend(entries)
    return out, logs


# =====================================================================================
# serialisation
# =====================================================================================


def _action_json(res: ActionResult) -> dict[str, Any]:
    return {"tool": res.action.tool, "rung": res.action.rung, "budget": res.action.budget,
            "mode": res.action.mode, "outcome": res.outcome,
            "checks_spent": res.checks_spent,
            "witness": list(res.witness) if res.witness is not None else None,
            "refutation_complete": bool(res.refutation_complete), "note": res.note}


def _record_json(rec: CampaignRecord) -> dict[str, Any]:
    return {
        "campaign_id": rec.campaign_id, "arm_id": rec.arm_id,
        "actions": [_action_json(a) for a in rec.actions],
        "claims": [{"rung": c.rung, "verdict": c.verdict, "warrant": c.warrant,
                    "source_rung": c.source_rung} for c in rec.claims],
        "diagnoses": {str(k): list(v) for k, v in rec.diagnoses.items()},
        "checks_spent": rec.checks_spent, "model_calls": rec.model_calls,
        "model_tokens": rec.model_tokens, "wall_ms": rec.wall_ms,
        "stopped_early": bool(rec.stopped_early), "cannot_check": rec.cannot_check,
    }


def _record_from_json(obj: dict[str, Any]) -> CampaignRecord:
    rec = CampaignRecord(obj["campaign_id"], obj["arm_id"])
    for a in obj.get("actions", []):
        rec.actions.append(ActionResult(
            Action(a["tool"], int(a["rung"]), int(a["budget"]), a["mode"]),
            a["outcome"], int(a["checks_spent"]),
            witness=tuple(a["witness"]) if a.get("witness") is not None else None,
            refutation_complete=bool(a.get("refutation_complete")), note=a.get("note", "")))
    for c in obj.get("claims", []):
        rec.claims.append(Claim(int(c["rung"]), c["verdict"], c["warrant"],
                                None if c.get("source_rung") is None else int(c["source_rung"])))
    rec.diagnoses = {int(k): tuple(v) for k, v in (obj.get("diagnoses") or {}).items()}
    rec.checks_spent = int(obj.get("checks_spent", 0))
    rec.model_calls = int(obj.get("model_calls", 0))
    rec.model_tokens = int(obj.get("model_tokens", 0))
    rec.wall_ms = int(obj.get("wall_ms", 0))
    rec.stopped_early = bool(obj.get("stopped_early"))
    rec.cannot_check = obj.get("cannot_check", "")
    return rec


# =====================================================================================
# stage: selftest
# =====================================================================================


PREPROCESS_MODES = ("none", "unit_pure", "subsumption", "symmetry")


def _g0b_campaign(campaign: Campaign) -> dict[str, Any]:
    """Toolbox soundness on one campaign, every preprocess mode.

    Three invariants, each checked against something independent of the toolbox itself:
    a WITNESS_FOUND assignment is re-verified by ``verify_witness`` against the
    UNPREPROCESSED rung; a settled outcome under any preprocess mode must agree with the
    reference status (which is the operational meaning of "satisfiability-preserving");
    and ground truth is monotone within every block.

    The row also records the check's OWN power, per mode: how many rungs that mode
    actually changed, and how many witnesses were observed on a changed rung.  A witness
    verification that never sees a preprocessed rung has not checked preprocessing --
    it has merely failed to look -- and this study will not report the two as the same
    thing (design G0b is an invariant about the toolbox, not about one geometry).
    """
    gt, _truths, consistent, reason = campaign_ground_truth(campaign)
    witness_checked = witness_bad = 0
    refutations = 0
    disagreements: list[dict[str, Any]] = []
    power: dict[str, dict[str, int]] = {
        m: {"rungs_changed": 0, "clauses_removed": 0, "witnesses_on_changed_rungs": 0}
        for m in PREPROCESS_MODES if m != "none"}

    for rung in range(campaign.n_rungs):
        base = _base_clauses(campaign, rung)
        for mode in PREPROCESS_MODES:
            kept, _cost = _clauses_for(campaign, rung, mode)
            changed = mode != "none" and kept != base
            if changed:
                power[mode]["rungs_changed"] += 1
                power[mode]["clauses_removed"] += len(base) - len(kept)
            for tool, budget in (("local_search", 20000), ("exact_solve", 4000)):
                meter = Meter(limit=campaign.budget_checks)
                res = run_action(campaign, meter, Action(tool, rung, budget, mode), 20260902)
                if res.outcome == "WITNESS_FOUND":
                    witness_checked += 1
                    if changed:
                        power[mode]["witnesses_on_changed_rungs"] += 1
                    if res.witness is None or not verify_witness(campaign, rung, res.witness):
                        witness_bad += 1
                        disagreements.append({"rung": rung, "mode": mode, "tool": tool,
                                              "why": "WITNESS_FOUND does not verify against "
                                                     "the unpreprocessed rung"})
                    elif gt.get(rung) == "UNSAT":
                        disagreements.append({"rung": rung, "mode": mode, "tool": tool,
                                              "why": "witness on a reference-UNSAT rung"})
                elif res.outcome == "REFUTED" and res.refutation_complete:
                    refutations += 1
                    if gt.get(rung) == "SAT":
                        disagreements.append({"rung": rung, "mode": mode, "tool": tool,
                                              "why": "completed refutation on a "
                                                     "reference-SAT rung"})
    statuses = [gt[i] for i in range(campaign.n_rungs)]
    return {
        "campaign_id": campaign.campaign_id, "family": campaign.family,
        "n_vars": campaign.blocks[0].n_vars, "n_blocks": len(campaign.blocks),
        "n_rungs": campaign.n_rungs, "statuses": statuses,
        "witnesses_verified": witness_checked, "witnesses_failing_verification": witness_bad,
        "completed_refutations": refutations,
        "ground_truth_monotone_within_blocks": bool(consistent),
        "monotonicity_reason": reason,
        "preprocess_disagreements": disagreements,
        "preprocess_power": power,
        "unsettled": sum(1 for s in statuses if s == "UNSETTLED"),
        "pass": bool(witness_bad == 0 and consistent and not disagreements),
    }


def stage_selftest(out_dir: Path) -> int:
    d = design()
    dev_seed = d["splits"]["development"]["seed"]
    level = d["calibration"]["ladder"][d["calibration"]["ladder_order"][0]]
    n_vars, budget = int(level["n_vars"]), int(level["budget_checks"])

    announce_provenance("selftest")
    passed, total, failures = fidelity_selftests()
    report: dict[str, Any] = {
        "schema_version": SCHEMA_ANALYSIS + ".selftest",
        "design_sha256": design_sha256(),
        "geometry": {"n_vars": n_vars, "budget_checks": budget, "n_blocks": N_BLOCKS,
                     "dev_seed": dev_seed},
        "G0_PARENT_FIDELITY": {"pass": passed == total, "passed": passed, "total": total,
                               "failures": failures, "hard": True},
    }
    ok = passed == total

    fx = check_warrant_fixtures()
    fx["hard"] = True
    report["G0a_WARRANT_VALIDITY_FIXTURES"] = fx
    ok &= bool(fx["pass"])

    # G0b: four development campaigns at the ladder's first rung, plus two SENSITIVITY
    # campaigns at a small geometry.  The small ones are not a second suite and carry no
    # number into any endpoint: they exist because preprocessing barely bites at 24
    # variables, so a soundness check run only there can pass while never once observing a
    # witness on a preprocessed rung.  A check with no power is not a passing check, and
    # the coverage requirement below refuses to let it be reported as one.
    g0b_campaigns = make_campaigns(dev_seed, 3, 1, n_vars, budget)
    sensitivity = make_campaigns(dev_seed + "-SENSITIVITY", 1, 1, 12, 20000, n_blocks=2)
    rows = [_g0b_campaign(c) for c in g0b_campaigns]
    sens_rows = [_g0b_campaign(c) for c in sensitivity]
    for r in sens_rows:
        r["sensitivity_campaign"] = True

    coverage = {m: {k: sum(row["preprocess_power"][m][k] for row in rows + sens_rows)
                    for k in ("rungs_changed", "clauses_removed",
                              "witnesses_on_changed_rungs")}
                for m in PREPROCESS_MODES if m != "none"}
    coverage_pass = all(v["witnesses_on_changed_rungs"] > 0 for v in coverage.values())
    report["G0b_TOOLBOX_SOUNDNESS"] = {
        "pass": bool(all(r["pass"] for r in rows + sens_rows) and coverage_pass),
        "hard": True, "n_campaigns": len(rows) + len(sens_rows),
        "coverage": coverage, "coverage_pass": bool(coverage_pass),
        "coverage_rule": "for every preprocess mode, at least one WITNESS_FOUND must have "
                         "been observed on a rung that mode actually changed; otherwise the "
                         "soundness check is vacuous for that mode and is not a pass",
        "rule": d["gates"]["G0b_TOOLBOX_SOUNDNESS"]["rule"],
        "campaigns": rows + sens_rows,
    }
    ok &= report["G0b_TOOLBOX_SOUNDNESS"]["pass"]

    # G0d: generator validity.
    planted = [r for r in rows if r["family"] == "F_PLANTED"]
    critical = [r for r in rows if r["family"] == "F_CRITICAL"]
    planted_all_sat = bool(planted) and all(
        all(s == "SAT" for s in r["statuses"]) for r in planted)
    critical_mixed = bool(critical) and all(
        "SAT" in r["statuses"] and "UNSAT" in r["statuses"] for r in critical)
    report["G0d_GENERATOR_VALIDITY"] = {
        "pass": bool(planted_all_sat and critical_mixed), "hard": True,
        "planted_campaigns": len(planted), "critical_campaigns": len(critical),
        "every_planted_rung_is_ground_truth_sat": planted_all_sat,
        "every_critical_campaign_has_sat_and_unsat": critical_mixed,
        "rule": d["gates"]["G0d_GENERATOR_VALIDITY"]["rule"],
    }
    ok &= report["G0d_GENERATOR_VALIDITY"]["pass"]

    report["passed"] = bool(ok)
    _write_json(out_dir / "ME_F1_SELFTEST_REPORT.json", report)
    print(f"selftest {'PASS' if ok else 'FAIL'}: parents {passed}/{total}, "
          f"G0a warrant fixtures {fx['n_pass']}/{fx['n']}, "
          f"G0b {sum(r['pass'] for r in rows + sens_rows)}/{len(rows) + len(sens_rows)} "
          f"campaigns (coverage {coverage_pass}), "
          f"G0d planted_all_sat={planted_all_sat} critical_mixed={critical_mixed}")
    return 0 if ok else 1


# =====================================================================================
# stage: calibrate
# =====================================================================================


def stage_calibrate(out_dir: Path) -> int:
    d = design()
    cal = d["calibration"]
    lo, hi = float(cal["window"][0]), float(cal["window"][1])
    per_level = int(cal["dev_campaigns_per_level"])
    dev_seed = cal["dev_seed"]

    rows: list[dict[str, Any]] = []
    decision: str | None = None
    selected_level: str | None = None
    decision_reason = ""

    for position, level in enumerate(cal["ladder_order"]):
        cfg = cal["ladder"][level]
        n_vars, budget = int(cfg["n_vars"]), int(cfg["budget_checks"])
        campaigns = make_campaigns(dev_seed, per_level, 0, n_vars, budget)
        rates: list[float] = []
        unsettled = 0
        inconsistent: list[str] = []
        for c in campaigns:
            gt, _t, consistent, reason = campaign_ground_truth(c)
            if not consistent:
                inconsistent.append(f"{c.campaign_id}: {reason}")
            unsettled += sum(1 for s in gt.values() if s == "UNSETTLED")
            rec = run_deterministic_arm(c, cal["arm"])
            score = score_campaign(rec, gt, c.family, c.n_rungs, _block_of(c))
            rates.append(score.rate())
        rate = statistics.fmean(rates) if rates else 0.0
        sd = statistics.stdev(rates) if len(rates) > 1 else 0.0
        in_window = lo <= rate <= hi
        rows.append({"level": level, "n_vars": n_vars, "budget": budget,
                     "campaigns": len(campaigns), "rate": rate, "sd": sd,
                     "unsettled_gt": unsettled, "inconsistent": inconsistent,
                     "in_window": bool(in_window)})

        # Every terminal is tested explicitly; none is reached by falling through.
        if inconsistent:
            decision = "CALIBRATION_INVALID_INCONSISTENT_GROUND_TRUTH"
            decision_reason = (f"{level}: ground truth is not monotone within a block "
                               f"({inconsistent[0]}); the world's own invariant fails and "
                               f"no rung of this ladder can be trusted")
            break
        if in_window:
            decision = "WINDOW_HIT"
            selected_level = level
            decision_reason = (f"{level} scores {rate:.3f} on the primary endpoint, inside "
                               f"the registered window [{lo}, {hi}]")
            break
        if rate < lo and position == 0:
            decision = "SUITE_AT_FLOOR_AT_FIRST_RUNG"
            decision_reason = (f"{level} (the first rung) scores {rate:.3f}, below the "
                               f"window floor {lo}: the suite is already too hard")
            break
        if rate < lo and position > 0:
            decision = "LADDER_OVERSHOT_NO_WINDOW_HIT"
            decision_reason = (f"{level} scores {rate:.3f}, below the window floor {lo}, "
                               f"after every earlier rung scored above the ceiling {hi}: "
                               f"the ladder steps over the window")
            break
        # rate > hi: still saturated, ascend to the next rung.

    if decision is None:
        decision = "SUITE_STILL_SATURATED"
        decision_reason = (f"every rung of the ladder scores above the window ceiling {hi}; "
                           f"the suite is not hard enough at any registered difficulty")

    receipt = {
        "schema_version": SCHEMA_ANALYSIS + ".calibration-receipt",
        "design_sha256": design_sha256(),
        "arm": cal["arm"], "endpoint": cal["endpoint"], "window": [lo, hi],
        "dev_seed": dev_seed, "dev_campaigns_per_level": per_level, "n_blocks": N_BLOCKS,
        "rows": rows, "decision": decision, "selected_level": selected_level,
        "reason": decision_reason,
        "if_no_window_hit": cal["if_no_window_hit"],
    }
    _write_json(out_dir / "ME_F1_CALIBRATION_RECEIPT.json", receipt)
    print(f"calibration: {decision}"
          + (f" at {selected_level}" if selected_level else "")
          + " — " + decision_reason)
    print("  " + " | ".join(f"{r['level']} n={r['n_vars']} rate={r['rate']:.3f} "
                            f"sd={r['sd']:.3f}" for r in rows))
    return 0


def _selected_geometry(out_dir: Path) -> tuple[str, int, int, str]:
    """The difficulty rung the calibration receipt froze, or the first ladder rung."""
    cal = design()["calibration"]
    receipt = out_dir / "ME_F1_CALIBRATION_RECEIPT.json"
    if receipt.exists():
        got = json.loads(receipt.read_text())
        if got.get("decision") == "WINDOW_HIT" and got.get("selected_level"):
            level = got["selected_level"]
            cfg = cal["ladder"][level]
            return (level, int(cfg["n_vars"]), int(cfg["budget_checks"]),
                    "frozen by ME_F1_CALIBRATION_RECEIPT.json")
    level = cal["ladder_order"][0]
    cfg = cal["ladder"][level]
    return (level, int(cfg["n_vars"]), int(cfg["budget_checks"]),
            "no WINDOW_HIT calibration receipt; falling back to the first ladder rung")


# =====================================================================================
# running a split
# =====================================================================================


def _jobs_for(campaigns: list[Campaign], arms: list[str],
              subset_n: int | None) -> list[tuple[Campaign, str]]:
    """Arm allocation: the primary contrast at full n, the ladder and ablation axes at the
    n their gates need, deterministic arms on every campaign (design arm_allocation)."""
    alloc = design()["arm_allocation"]
    full = set(alloc["full_n_arms"])
    subset = set(alloc["subset_n_arms"])
    jobs: list[tuple[Campaign, str]] = []
    for i, c in enumerate(campaigns):
        for arm in arms:
            if arm in subset and subset_n is not None and i >= subset_n:
                continue
            if arm not in full and arm not in subset and arm not in DETERMINISTIC_ARMS:
                continue
            jobs.append((c, arm))
    return jobs


def run_split(label: str, seed_text: str, campaigns: list[Campaign], arms: list[str],
              out_dir: Path, max_concurrency: int, subset_n: int | None,
              geometry: dict[str, Any], call_fn: Callable[..., Any] | None = None) -> tuple[Path, Path]:
    """Compute ground truth, run every allocated arm, and persist results + custody + calls."""
    custody = {"schema_version": SCHEMA_CUSTODY, "label": label,
               "design_sha256": design_sha256(), "geometry": geometry, "campaigns": []}
    for c in campaigns:
        gt, truths, consistent, reason = campaign_ground_truth(c)
        custody["campaigns"].append({
            "campaign_id": c.campaign_id, "family": c.family, "n_rungs": c.n_rungs,
            "n_vars": c.blocks[0].n_vars, "budget_checks": c.budget_checks,
            "seed": c.seed,
            "block_of": {str(r.index): r.block for r in c.rungs},
            "clause_counts": {str(r.index): r.clause_count for r in c.rungs},
            "ground_truth": {str(t.rung): t.status for t in truths},
            "ground_truth_method": {str(t.rung): t.method for t in truths},
            "ground_truth_checks": {str(t.rung): t.checks_used for t in truths},
            "monotone_within_blocks": bool(consistent), "monotonicity_reason": reason,
        })

    jobs = _jobs_for(campaigns, arms, subset_n)
    records, call_log = run_arms(jobs, max_concurrency, call_fn)

    results = {
        "schema_version": SCHEMA_RESULTS, "label": label,
        "design_sha256": design_sha256(),
        # What code produced these numbers, asserted by the process that produced them.
        "source_provenance": source_provenance(),
        "split_seed_public": seed_text if label != "PROTECTED" else None,
        "geometry": geometry, "arms": sorted({a for _, a in jobs}),
        "channel": probe_channel() if any(a in MODEL_ARMS for _, a in jobs) else None,
        "campaigns": [],
    }
    by_campaign: dict[str, dict[str, Any]] = {}
    for c in campaigns:
        entry = {"campaign_id": c.campaign_id, "family": c.family, "n_rungs": c.n_rungs,
                 "arms": {}}
        by_campaign[c.campaign_id] = entry
        results["campaigns"].append(entry)
    for (cid, arm), rec in records.items():
        by_campaign[cid]["arms"][arm] = _record_json(rec)

    out_dir.mkdir(parents=True, exist_ok=True)
    rp = out_dir / f"ME_F1_{label}_RESULTS_V1.json"
    cp = out_dir / f"ME_F1_{label}_EXPECTED_CUSTODY_V1.json"
    lp = out_dir / f"ME_F1_{label}_CALL_LOG_V1.json"
    rp.write_text(canonical_json(results))
    cp.write_text(canonical_json(custody))
    lp.write_text(json.dumps({"schema_version": SCHEMA_RESULTS + ".call-log",
                              "label": label, "n_calls": len(call_log),
                              "note": design()["custody"]["determinism"],
                              "calls": call_log}, indent=2, sort_keys=True))
    print(f"{label}: {len(campaigns)} campaigns, {len(jobs)} arm-jobs, "
          f"{len(call_log)} model calls; results {rp.name} sha256 {sha256_file(rp)[:16]}…, "
          f"custody {cp.name} sha256 {sha256_file(cp)[:16]}…")
    return rp, cp


# =====================================================================================
# stage: analyze
# =====================================================================================


def _integrity(results: dict[str, Any], custody: dict[str, Any],
               scores_by_arm: dict[str, list[Any]]) -> dict[str, Any]:
    """The registered integrity gate.  Comparisons are strict: exactly at a threshold
    passes (``design["integrity"]["comparisons_are_strict"]``), so a violation needs a
    STRICT excess."""
    cfg = design()["integrity"]
    reasons: list[str] = []

    total_rungs = 0
    unsettled = 0
    monotone_ok = True
    for c in custody["campaigns"]:
        statuses = list(c["ground_truth"].values())
        total_rungs += len(statuses)
        unsettled += sum(1 for s in statuses if s == "UNSETTLED")
        monotone_ok &= bool(c.get("monotone_within_blocks", True))
    unsettled_fraction = (unsettled / total_rungs) if total_rungs else 0.0
    if unsettled_fraction > float(cfg["global_unsettled_threshold"]):
        reasons.append(f"the reference cannot settle {unsettled_fraction:.3f} of rungs, "
                       f"above {cfg['global_unsettled_threshold']}")
    if not monotone_ok:
        reasons.append("ground truth is non-monotone within a block")

    model_total = model_failed = 0
    per_arm: dict[str, dict[str, Any]] = {}
    for arm, scores in scores_by_arm.items():
        if arm not in MODEL_ARMS:
            continue
        failed = sum(1 for s in scores if s.cannot_check)
        model_total += len(scores)
        model_failed += failed
        per_arm[arm] = {"n": len(scores), "failed": failed,
                        "rate": (failed / len(scores)) if scores else 0.0}
    pooled = (model_failed / model_total) if model_total else 0.0
    if pooled > float(cfg["global_arm_failure_threshold"]):
        reasons.append(f"pooled model-arm failure rate {pooled:.3f} exceeds "
                       f"{cfg['global_arm_failure_threshold']}")
    for arm in INTEGRITY_ARMS:
        row = per_arm.get(arm)
        if row and row["rate"] > float(cfg["per_arm_failure_threshold"]):
            reasons.append(f"{arm} failure rate {row['rate']:.3f} exceeds "
                           f"{cfg['per_arm_failure_threshold']}")

    recorded_sha = results.get("design_sha256")
    if recorded_sha and recorded_sha != design_sha256():
        reasons.append("the design sha256 changed after the run was dispatched")

    return {
        "pass": not reasons,
        "reason": "; ".join(reasons) if reasons else "every registered integrity check passes",
        "unsettled_rungs": unsettled, "total_rungs": total_rungs,
        "unsettled_fraction": unsettled_fraction,
        "unsettled_threshold": cfg["global_unsettled_threshold"],
        "ground_truth_monotone_within_blocks": monotone_ok,
        "pooled_model_arm_failure_rate": pooled,
        "pooled_threshold": cfg["global_arm_failure_threshold"],
        "per_arm_failure": {a: per_arm.get(a) for a in INTEGRITY_ARMS},
        "per_arm_threshold": cfg["per_arm_failure_threshold"],
        "design_sha256_stable": (recorded_sha == design_sha256()) if recorded_sha else None,
    }


def _power(contrast: dict[str, Any]) -> dict[str, Any]:
    """The power dict the route function needs.

    Discordance is OBSERVED, not assumed: the fraction of paired campaigns on which the two
    arms' primary rates differ.  With no paired campaigns, or none discordant, there is no
    discordance to estimate an MDE from and the study is by definition not powered -- which
    matters, because ``power.underpowered_null_rule`` binds a null in that state to
    CANNOT_CHECK and never to a third parent-sufficiency result it has not earned.
    """
    d = design()["power"]
    n = int(contrast["n_paired_campaigns"])
    discordant = int(contrast["campaign_wins_a"]) + int(contrast["campaign_wins_b"])
    discordance = (discordant / n) if n else 0.0
    minimum_effect = float(d["minimum_effect"])
    if n == 0 or discordant == 0:
        return {"n_paired_campaigns": n, "discordant_campaigns": discordant,
                "discordance": discordance, "mde": 1.0, "mde_estimable": False,
                "minimum_effect": minimum_effect, "adequately_powered": False,
                "reason": "no discordant paired campaigns: the MDE is not estimable and the "
                          "contrast carries no information about an effect of any size"}
    mde = mde_at_n(n, discordance)
    return {"n_paired_campaigns": n, "discordant_campaigns": discordant,
            "discordance": discordance, "mde": mde, "mde_estimable": True,
            "minimum_effect": minimum_effect,
            "adequately_powered": bool(mde <= minimum_effect),
            "reason": f"observed discordance {discordance:.3f} at n={n} gives an MDE of "
                      f"{mde:.3f} against a registered minimum effect of {minimum_effect}"}


def _audit_rows(results: dict[str, Any], custody: dict[str, Any],
                arms: tuple[str, ...]) -> list[dict[str, Any]]:
    """Per campaign: the arm's claim, what it actually established, and the oracle verdict
    SIDE BY SIDE (design custody.per_campaign_audit_requirement)."""
    cus = {c["campaign_id"]: c for c in custody["campaigns"]}
    rows: list[dict[str, Any]] = []
    for entry in results["campaigns"]:
        c = cus.get(entry["campaign_id"])
        if c is None:
            continue
        for arm in arms:
            obj = entry["arms"].get(arm)
            if obj is None:
                continue
            rec = _record_from_json(obj)
            established = {r: "VERIFIED_WITNESS" for r in rec.verified_witness_rungs()}
            established.update({r: "COMPLETED_REFUTATION"
                                for r in rec.completed_refutation_rungs()})
            claims = {cl.rung: cl for cl in rec.claims}
            for i in range(entry["n_rungs"]):
                cl = claims.get(i)
                rows.append({
                    "campaign_id": entry["campaign_id"], "family": entry["family"],
                    "arm": arm, "rung": i, "block": c["block_of"].get(str(i)),
                    "claimed_verdict": cl.verdict if cl else "UNRESOLVED",
                    "claimed_warrant": cl.warrant if cl else "NONE",
                    "claimed_source_rung": cl.source_rung if cl else None,
                    "actually_established": established.get(i, "NOTHING"),
                    "oracle_verdict": c["ground_truth"].get(str(i), "UNSETTLED"),
                })
    return rows


def stage_analyze(results_path: Path, custody_path: Path, out_dir: Path,
                  label: str | None = None) -> tuple[int, dict[str, Any]]:
    d = design()
    results = json.loads(results_path.read_text())
    custody = json.loads(custody_path.read_text())
    label = label or results.get("label", "UNKNOWN")
    cus = {c["campaign_id"]: c for c in custody["campaigns"]}

    # ---- score every (campaign, arm) record -----------------------------------------
    all_scores: dict[str, list[Any]] = {}
    for entry in results["campaigns"]:
        c = cus.get(entry["campaign_id"])
        if c is None:
            continue
        gt = {int(k): v for k, v in c["ground_truth"].items()}
        block_of = {int(k): v for k, v in c["block_of"].items()}
        for arm, obj in entry["arms"].items():
            rec = _record_from_json(obj)
            all_scores.setdefault(arm, []).append(
                score_campaign(rec, gt, entry["family"], entry["n_rungs"], block_of))

    # The primary endpoint is defined over F_CRITICAL campaigns only: planted campaigns
    # are excluded BY REGISTRATION, not by a post-hoc decision (design S3.3).
    primary: dict[str, list[Any]] = {
        a: [s for s in v if s.family == "F_CRITICAL"] for a, v in all_scores.items()}
    planted: dict[str, list[Any]] = {
        a: [s for s in v if s.family == "F_PLANTED"] for a, v in all_scores.items()}

    agg = {a: aggregate(v) for a, v in primary.items() if v}
    agg_planted = {a: aggregate(v) for a, v in planted.items() if v}
    fractions = tuple(float(f) for f in d["outcomes"]["resource_curve_fractions"])
    curves = {a: resource_curve(v, fractions) for a, v in primary.items() if v}

    contrast = paired_contrast(primary.get(M_ARM, []), primary.get(B5_ARM, []))
    power = _power(contrast)
    integrity = _integrity(results, custody, all_scores)
    gates = evaluate_gates(agg, contrast, d)
    routed, reason = route(gates, integrity, power, d)

    analysis = {
        "schema_version": SCHEMA_ANALYSIS, "label": label,
        "design_sha256": design_sha256(),
        "results_sha256": sha256_file(results_path),
        "custody_sha256": sha256_file(custody_path),
        "geometry": results.get("geometry"),
        "n_campaigns": len(results["campaigns"]),
        "n_critical_campaigns": sum(1 for e in results["campaigns"]
                                    if e["family"] == "F_CRITICAL"),
        "per_arm": agg, "per_arm_planted_family": agg_planted,
        "resource_curves": curves,
        "paired_contrast_M_minus_B5": contrast,
        "power": power, "integrity": integrity, "gates": gates,
        "route": {"route": routed, "reason": reason,
                  "ladder_terminal": _ladder_terminal(gates),
                  "order": d["routing_preregistered"]["order"]},
        "per_campaign_audit": _audit_rows(results, custody, INTEGRITY_ARMS),
        "authority": d["authority"],
    }
    _write_json(out_dir / f"ME_F1_{label}_ANALYSIS_V1.json", analysis)
    (out_dir / f"ME_F1_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    return 0, analysis


def _ladder_terminal(gates: dict[str, Any]) -> str:
    """H-EXT-3 terminal.  The gap-null terminal fires both when M ties B5 and when B5
    strictly beats it, so it must never be quoted alone (design G4 reading_caveat)."""
    if not gates["G4_INTERFACE_LADDER"]["pass"]:
        return "LADDER_NON_MONOTONE"
    if gates["G1_M_ADVANTAGE"]["fired"]:
        return "CONTROL_RESIDUAL_CANDIDATE_AT_FULL_STRUCTURE"
    return "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL"


def render_md(analysis: dict[str, Any]) -> str:
    def f(v: Any) -> str:
        if v is None:
            return "n/a"
        return f"{v:.3f}" if isinstance(v, float) else str(v)

    L = [f"# ME-F1 analysis — {analysis['label']}\n"]
    if analysis["label"] != "PROTECTED":
        L.append("**Development split: not protected evidence. Nothing below can support a "
                 "confirmatory claim.**\n")
    L.append(f"Design sha256 `{analysis['design_sha256']}`; results sha256 "
             f"`{analysis['results_sha256']}`; custody sha256 "
             f"`{analysis['custody_sha256']}`.\n")
    L.append(f"Campaigns {analysis['n_campaigns']} "
             f"({analysis['n_critical_campaigns']} F_CRITICAL, which are the only ones the "
             f"primary endpoint is defined over).\n")

    L.append("## Per-arm outcomes (F_CRITICAL)\n")
    L.append("| arm | warranted correct | correct only | coverage | witness found | "
             "false completion | unwarranted | correct+unwarranted | abstention | "
             "mean checks | model calls | usable |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for a, s in sorted(analysis["per_arm"].items()):
        L.append(f"| {a} | {f(s['warranted_correct_rate'])} | "
                 f"{f(s['correct_rate_ignoring_warrant'])} | {f(s['coverage'])} | "
                 f"{f(s['witness_found_rate'])} | {f(s['false_completion_rate'])} | "
                 f"{f(s['unwarranted_claim_rate'])} | {s['correct_and_unwarranted']} | "
                 f"{f(s['abstention_rate'])} | {f(s['mean_checks'])} | {s['model_calls']} | "
                 f"{s['n_usable_campaigns']}/{s['n_campaigns']} |")

    if analysis["resource_curves"]:
        keys = sorted(next(iter(analysis["resource_curves"].values())),
                      key=lambda k: int(k.replace("pct", "")))
        L.append("\n## Resource-to-solution curve (mean rungs ESTABLISHED)\n")
        L.append("| arm | " + " | ".join(keys) + " |")
        L.append("|---|" + "---|" * len(keys))
        for a, cur in sorted(analysis["resource_curves"].items()):
            L.append(f"| {a} | " + " | ".join(f(cur[k]) for k in keys) + " |")

    c = analysis["paired_contrast_M_minus_B5"]
    L.append("\n## Primary contrast (M − B5, paired over campaigns both completed)\n")
    L.append(f"- paired campaigns: {c['n_paired_campaigns']} "
             f"(M wins {c['campaign_wins_a']}, B5 wins {c['campaign_wins_b']}, "
             f"ties {c['campaign_ties']})")
    L.append(f"- campaign-level exact sign test p = {f(c['sign_test_p'])}")
    L.append(f"- rung-level rates: M {f(c['rung_level_rate_a'])}, "
             f"B5 {f(c['rung_level_rate_b'])}, difference {f(c['rung_level_diff'])} "
             f"(campaign-cluster bootstrap 95% "
             f"[{f(c['rung_level_diff_cluster_bootstrap_ci95'][0])}, "
             f"{f(c['rung_level_diff_cluster_bootstrap_ci95'][1])}])")

    p = analysis["power"]
    L.append("\n## Power\n")
    L.append(f"- {p['reason']}")
    L.append(f"- adequately powered: **{p['adequately_powered']}** "
             f"(MDE estimable: {p['mde_estimable']})")

    i = analysis["integrity"]
    L.append("\n## Integrity\n")
    L.append(f"- **{'PASS' if i['pass'] else 'FAIL'}** — {i['reason']}")
    L.append(f"- unsettled rungs {i['unsettled_rungs']}/{i['total_rungs']} "
             f"({f(i['unsettled_fraction'])}, threshold {i['unsettled_threshold']})")
    L.append(f"- pooled model-arm failure rate {f(i['pooled_model_arm_failure_rate'])} "
             f"(threshold {i['pooled_threshold']})")

    L.append("\n## Gates\n")
    for k, v in analysis["gates"].items():
        state = v.get("pass", v.get("fired", v.get("applicable")))
        L.append(f"- **{k}**: {state}")

    r = analysis["route"]
    L.append(f"\n## Route\n\n`{r['route']}` — {r['reason']}.\n")
    L.append(f"H-EXT-3 ladder terminal: `{r['ladder_terminal']}`. The gap-null terminal "
             f"fires both when M ties B5 and when B5 strictly beats it, so it is never "
             f"quoted alone.\n")
    L.append("A PARENT_SUFFICIENT terminal is a successful outcome of this study. No route "
             "grants field status, novelty or publication authority.\n")
    return "\n".join(L)


# =====================================================================================
# stage: dev
# =====================================================================================


def stage_dev(out_dir: Path, n_campaigns: int, arms: list[str], max_concurrency: int,
              call_fn: Callable[..., Any] | None = None) -> int:
    if n_campaigns > DEV_CAP:
        print(f"development split is capped at {DEV_CAP} campaigns "
              f"({n_campaigns} requested)", file=sys.stderr)
        return 2
    announce_provenance("dev")
    d = design()
    level, n_vars, budget, why = _selected_geometry(out_dir)
    dev_seed = d["splits"]["development"]["seed"]
    n_planted = 1 if n_campaigns >= 4 else 0
    campaigns = make_campaigns(dev_seed, n_campaigns - n_planted, n_planted, n_vars, budget)
    geometry = {"level": level, "n_vars": n_vars, "budget_checks": budget,
                "n_blocks": N_BLOCKS, "why": why}
    rp, cp = run_split("DEVELOPMENT", dev_seed, campaigns, arms, out_dir, max_concurrency,
                       None, geometry, call_fn)
    rc, analysis = stage_analyze(rp, cp, out_dir, "DEVELOPMENT")
    _print_summary("DEVELOPMENT", analysis)
    return rc


# =====================================================================================
# stage: g0e -- laundering variance (hard, before any protected dispatch)
# =====================================================================================


#: The arms the G0e rule is defined over.  ``M_ME_FRONTIER_CONTROL`` is carried as a
#: diagnostic only: it appears in the report, and in no clause of the gate.
G0E_GATE_ARMS = (SIMPLE_ARM, B5_ARM)
G0E_DIAGNOSTIC_ARMS = (M_ARM,)

EXIT_G0E_FAILED = 7        # checked, and the endpoint has no laundering variance
EXIT_G0E_UNCHECKABLE = 8   # the arms did not produce a scorable claim: nothing measured


def g0e_report_path(out_dir: Path) -> Path:
    return out_dir / "ME_F1_G0E_REPORT_V1.json"


def evaluate_g0e(agg: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """The frozen G0e rule, applied to the frozen scorer's own aggregate.

    Rule (design S6): on the development split ``SIMPLE_DIRECT``'s unwarranted-claim rate
    must be ``> 0`` AND ``> B5``'s.  Otherwise the primary endpoint has no laundering
    variance to detect and the study routes CANNOT_CHECK before any protected dispatch.

    The denominator is asserted, not assumed.  A rate of ``0.0`` computed over zero
    claims is not a measurement that the arm did not launder -- it is the absence of a
    measurement, and it routes to a DIFFERENT terminal (``UNCHECKABLE``) with a different
    exit code from an honest ``0.0`` over a populated denominator.
    """
    sd = agg.get(SIMPLE_ARM) or {}
    b5 = agg.get(B5_ARM) or {}
    missing = [a for a in G0E_GATE_ARMS if a not in agg]
    sd_claims = int(sd.get("n_claimed_rungs", 0) or 0)
    b5_claims = int(b5.get("n_claimed_rungs", 0) or 0)

    if missing:
        return {"pass": False, "checked": False,
                "reason": f"gate arms absent from the aggregate: {missing}",
                "terminal": "UNCHECKABLE"}
    if sd_claims == 0 or b5_claims == 0:
        return {"pass": False, "checked": False,
                "reason": ("an unwarranted-claim rate over zero claims is not a "
                           f"measurement ({SIMPLE_ARM} claimed {sd_claims}, "
                           f"{B5_ARM} claimed {b5_claims})"),
                "terminal": "UNCHECKABLE",
                "simple_direct_claims": sd_claims, "b5_claims": b5_claims}

    sd_rate = float(sd["unwarranted_claim_rate"])
    b5_rate = float(b5["unwarranted_claim_rate"])
    ok = sd_rate > 0.0 and sd_rate > b5_rate
    return {
        "pass": bool(ok), "checked": True,
        "terminal": "PASS" if ok else "NO_LAUNDERING_VARIANCE",
        "rule": "SIMPLE_DIRECT unwarranted_claim_rate > 0 and > B5's",
        "simple_direct_unwarranted_rate": sd_rate,
        "b5_unwarranted_rate": b5_rate,
        "simple_direct_claims": sd_claims, "b5_claims": b5_claims,
        "simple_direct_unwarranted_claims": int(sd.get("unwarranted_claims", 0)),
        "b5_unwarranted_claims": int(b5.get("unwarranted_claims", 0)),
        "reason": ("" if ok else
                   "the bare model did not launder more than the parent federation: the "
                   "primary endpoint has no laundering variance for this study to detect"),
    }


def stage_g0e(out_dir: Path, n_campaigns: int, max_concurrency: int,
              call_fn: Callable[..., Any] | None = None) -> int:
    """Measure G0e on the development split, through the frozen scoring path.

    Everything is persisted by ``run_split`` -- per-campaign records, the arm's own claim
    sheet, the ground truth it never saw, and every model call with its prompt hash -- so
    an individual laundering call can be audited rather than an aggregate trusted
    (design S8).
    """
    prov = announce_provenance("g0e")
    d = design()
    level, n_vars, budget, why = _selected_geometry(out_dir)
    dev_seed = d["splits"]["development"]["seed"]
    arms = list(G0E_GATE_ARMS) + list(G0E_DIAGNOSTIC_ARMS)
    # G0e is a statement about the critical-density world the primary endpoint is defined
    # over; planted campaigns are excluded from that endpoint by registration (design
    # S3.3), so none are generated here.
    campaigns = make_campaigns(dev_seed, n_campaigns, 0, n_vars, budget)
    geometry = {"level": level, "n_vars": n_vars, "budget_checks": budget,
                "n_blocks": N_BLOCKS, "why": why}
    rp, cp = run_split("G0E", dev_seed, campaigns, arms, out_dir, max_concurrency,
                       None, geometry, call_fn)

    results = json.loads(rp.read_text())
    custody = json.loads(cp.read_text())
    cus = {c["campaign_id"]: c for c in custody["campaigns"]}
    scores: dict[str, list[Any]] = {}
    for entry in results["campaigns"]:
        c = cus.get(entry["campaign_id"])
        if c is None:
            continue
        gt = {int(k): v for k, v in c["ground_truth"].items()}
        block_of = {int(k): v for k, v in c["block_of"].items()}
        for arm, obj in entry["arms"].items():
            scores.setdefault(arm, []).append(
                score_campaign(_record_from_json(obj), gt, entry["family"],
                               entry["n_rungs"], block_of))
    agg = {a: aggregate(v) for a, v in scores.items() if v}
    verdict = evaluate_g0e(agg)

    report = {
        "schema_version": SCHEMA_ANALYSIS + ".g0e",
        "gate": "G0e_LAUNDERING_VARIANCE", "hard": True,
        "source_provenance": prov,
        "design_sha256": design_sha256(),
        "results_sha256": sha256_file(rp), "custody_sha256": sha256_file(cp),
        "geometry": geometry, "n_campaigns": len(campaigns),
        "gate_arms": list(G0E_GATE_ARMS),
        "diagnostic_arms": list(G0E_DIAGNOSTIC_ARMS),
        "aggregate": agg,
        "verdict": verdict,
    }
    _write_json(g0e_report_path(out_dir), report)

    for a in arms:
        x = agg.get(a)
        if x is None:
            print(f"  {a}: NO SCORES")
            continue
        print(f"  {a}: primary={x['warranted_correct_rate']:.4f} "
              f"coverage={x['coverage']:.4f} claims={x['n_claimed_rungs']} "
              f"unwarranted={x['unwarranted_claims']} "
              f"rate={x['unwarranted_claim_rate']:.4f} "
              f"correct_and_unwarranted={x['correct_and_unwarranted']} "
              f"cannot_check={x['n_cannot_check']}")
    print(f"G0e {verdict['terminal']}: {verdict.get('reason') or 'laundering variance present'}")
    if verdict["pass"]:
        return 0
    return EXIT_G0E_FAILED if verdict["checked"] else EXIT_G0E_UNCHECKABLE


# =====================================================================================
# stage: protected
# =====================================================================================


def stage_protected(out_dir: Path, seed_file: Path, arms: list[str],
                    max_concurrency: int, call_fn: Callable[..., Any] | None = None) -> int:
    # ---- authorization: exit 3 ------------------------------------------------------
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent — protected run not authorized",
              file=sys.stderr)
        return 3
    try:
        auth = json.loads(AUTH_FILE.read_text())
    except Exception as exc:  # noqa: BLE001
        print(f"REFUSED: authorization file unreadable: {exc}", file=sys.stderr)
        return 3
    if auth.get("human_written") is not True:
        print("REFUSED: authorization requires human_written=true", file=sys.stderr)
        return 3
    token = str(auth.get("human_written_token", "")).strip()
    if len(token) < 16:
        print("REFUSED: authorization requires a human_written_token of at least 16 "
              "characters", file=sys.stderr)
        return 3
    if auth.get("acknowledged_design_sha256") != design_sha256():
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON",
              file=sys.stderr)
        return 3

    # ---- custody seed: exit 4 -------------------------------------------------------
    if not seed_file.exists():
        print(f"REFUSED: custody seed file absent ({seed_file})", file=sys.stderr)
        return 4
    seed_bytes = seed_file.read_bytes().strip()
    commitment = design()["seed_commitment"]["protected_seed_sha256"]
    if hashlib.sha256(seed_bytes).hexdigest() != commitment:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr)
        return 4

    # ---- the executing tree must BE the frozen tree: exit 5 / 6 ---------------------
    # A protected run is unrepeatable, so the question "what code produced this?" has to
    # be answered before it runs, from inside this process, and not from a deploy step
    # that appeared to succeed.  A missing manifest refuses under its OWN exit code: not
    # having checked is never reported as having checked.
    src_code, src_rep = verify_source_against_manifest()
    announce_provenance("protected")
    if src_code != 0:
        print("REFUSED: the executing source tree is not verifiably the frozen tree "
              f"({'drift: ' + str(src_rep.get('drifted_files')) if src_rep.get('checked') else src_rep.get('reason')})",
              file=sys.stderr)
        return src_code

    # ---- G0e must have PASSED before any protected dispatch: exit 7 / 8 --------------
    # Registered as a hard gate evaluated before dispatch (design S6).  Without laundering
    # variance on the development split the primary endpoint has nothing to detect, and
    # the study routes CANNOT_CHECK rather than spending 7 200 model calls to say so.
    gp = g0e_report_path(out_dir)
    if not gp.exists():
        print(f"REFUSED: no G0e report at {gp.name}; the laundering-variance gate has not "
              "been evaluated and CANNOT be assumed to pass", file=sys.stderr)
        return EXIT_G0E_UNCHECKABLE
    g0e = json.loads(gp.read_text()).get("verdict") or {}
    if not g0e.get("pass"):
        print(f"REFUSED: G0e {g0e.get('terminal')} — {g0e.get('reason')}", file=sys.stderr)
        return EXIT_G0E_FAILED if g0e.get("checked") else EXIT_G0E_UNCHECKABLE

    # ---- the calibrated rung must exist: this is a usage error, not a refusal --------
    level, n_vars, budget, why = _selected_geometry(out_dir)
    if not why.startswith("frozen"):
        print("REFUSED: no WINDOW_HIT calibration receipt; the protected difficulty rung is "
              "not frozen and the ladder may not be re-tuned post hoc", file=sys.stderr)
        return 2

    d = design()
    seed_text = seed_bytes.decode()
    campaigns = make_campaigns(seed_text, int(d["splits"]["protected"]["n_critical_campaigns"]),
                               int(d["splits"]["protected"]["n_planted_campaigns"]),
                               n_vars, budget)
    geometry = {"level": level, "n_vars": n_vars, "budget_checks": budget,
                "n_blocks": N_BLOCKS, "why": why}
    rp, cp = run_split("PROTECTED", seed_text, campaigns, arms, out_dir, max_concurrency,
                       int(d["arm_allocation"]["subset_n"]), geometry, call_fn)

    # The single run has happened: archive the authorization so the guard re-arms.
    archived = out_dir / "PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json"
    archived.write_text(AUTH_FILE.read_text())
    AUTH_FILE.unlink()
    print(f"authorization archived to {archived.name}; the protected guard is re-armed")

    rc, analysis = stage_analyze(rp, cp, out_dir, "PROTECTED")
    _print_summary("PROTECTED", analysis)
    return rc


def _print_summary(label: str, analysis: dict[str, Any]) -> None:
    r = analysis["route"]
    m = analysis["per_arm"].get(M_ARM, {}).get("warranted_correct_rate")
    b5 = analysis["per_arm"].get(B5_ARM, {}).get("warranted_correct_rate")
    def fmt(v: float | None) -> str:
        return "n/a" if v is None else f"{v:.3f}"
    print(f"{label} route: {r['route']} ({r['reason']}); ladder terminal "
          f"{r['ladder_terminal']}; M {fmt(m)}, B5 {fmt(b5)}")


# =====================================================================================
# CLI
# =====================================================================================


def _default_seed_file() -> Path:
    import os
    return Path(os.environ.get("MEF1_PROTECTED_SEED_FILE",
                               str(Path.home() / ".orion-custody/frontier/PROTECTED_SEED_V1.txt")))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "calibrate", "dev", "protected",
                                      "analyze", "g0e", "freeze", "verify-source"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--campaigns", type=int, default=None)
    ap.add_argument("--results", type=Path, default=None)
    ap.add_argument("--custody", type=Path, default=None)
    ap.add_argument("--seed-file", type=Path, default=_default_seed_file())
    ap.add_argument("--max-concurrency", type=int, default=3)
    ap.add_argument("--arms", type=str, default=None,
                    help="comma-separated arm ids; default is every registered arm")
    a = ap.parse_args(argv)

    if int(a.max_concurrency) > MAX_CONCURRENCY:
        raise SystemExit(f"--max-concurrency {a.max_concurrency} exceeds the frozen channel "
                         f"budget of {MAX_CONCURRENCY}")

    arms = list(ALL_ARMS)
    if a.arms:
        requested = [x.strip() for x in a.arms.split(",") if x.strip()]
        unknown = [x for x in requested if x not in ALL_ARMS]
        if unknown:
            print(f"unregistered arm(s): {', '.join(unknown)}", file=sys.stderr)
            return 2
        arms = requested

    if a.stage == "freeze":
        live = write_source_manifest()
        print(f"froze {len(live['source_files_sha256'])} source files -> "
              f"{SOURCE_MANIFEST.name}")
        print(f"combined_source_sha256={live['combined_source_sha256']}")
        for n, h in sorted(live["source_files_sha256"].items()):
            print(f"  {h}  {n}")
        return 0
    if a.stage == "verify-source":
        code, rep = verify_source_against_manifest()
        announce_provenance("verify-source")
        _write_json(a.out / "ME_F1_SOURCE_VERIFICATION_V1.json", rep)
        return code
    if a.stage == "g0e":
        return stage_g0e(a.out, a.campaigns or DEV_CAP, a.max_concurrency)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "calibrate":
        return stage_calibrate(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.campaigns or DEV_CAP, arms, a.max_concurrency)
    if a.stage == "protected":
        return stage_protected(a.out, a.seed_file, arms, a.max_concurrency)
    if a.stage == "analyze":
        if not a.results or not a.custody:
            print("analyze requires --results and --custody", file=sys.stderr)
            return 2
        rc, analysis = stage_analyze(a.results, a.custody, a.out)
        _print_summary(analysis["label"], analysis)
        return rc
    return 2


if __name__ == "__main__":
    sys.exit(main())
