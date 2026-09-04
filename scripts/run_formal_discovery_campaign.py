#!/usr/bin/env python3
"""Orchestrate the frozen generated FM/FG campaign study-by-study.

This script is plumbing, not an outcome generator by itself. `prepare` materializes
prospective task identities from the frozen campaign plan; `dispatch` runs the
registered model arms gold-blind through the shared generated-suite harness;
`evaluate` reveals private exact answers only after model termination.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json"
DEFAULT_ROOT = ROOT / ".orion-formal-discovery-campaign"
SUITE_PATH = ROOT / "scripts/run_formal_discovery_generated_suite.py"


class CampaignError(RuntimeError):
    pass


def load_suite():
    spec = importlib.util.spec_from_file_location("orion_formal_generated_suite", SUITE_PATH)
    if spec is None or spec.loader is None:
        raise CampaignError("cannot load generated-suite harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CampaignError(f"expected JSON object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_studies(plan: dict[str, Any], raw: str | None) -> list[str]:
    available = list(plan["studies"])
    if not raw:
        return available
    requested = [item.strip() for item in raw.split(",") if item.strip()]
    unknown = sorted(set(requested) - set(available))
    if unknown:
        raise CampaignError("unknown study ids: " + ", ".join(unknown))
    return requested


def study_seed(base_seed: int, study_id: str) -> int:
    digest = hashlib.sha256(f"{base_seed}:{study_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def prepare(plan_path: Path, campaign_root: Path, studies: list[str], force: bool) -> None:
    plan = load_json(plan_path)
    suite = load_suite()
    manifest_rows = []
    for study_id in studies:
        spec = plan["studies"][study_id]
        workdir = campaign_root / study_id
        suite.prepare(
            workdir,
            [study_id],
            int(spec["tasks"]),
            study_seed(int(plan["seed"]), study_id),
            list(spec["arms"]),
            force,
        )
        freeze = load_json(workdir / "FROZEN_SUITE.json")
        manifest_rows.append(
            {
                "study_id": study_id,
                "workdir": str(workdir),
                "task_count": freeze["task_count"],
                "arms": freeze["arms"],
                "seed": freeze["seed"],
                "freeze_sha256": sha256_path(workdir / "FROZEN_SUITE.json"),
                "public_tasks_sha256": sha256_path(workdir / "public_tasks.json"),
                "private_oracle_sha256": sha256_path(workdir / "private_oracle.json"),
            }
        )
    write_json(
        campaign_root / "CAMPAIGN_FREEZE_MANIFEST.json",
        {
            "schema_version": "orion.v2.formal-discovery-campaign-freeze.v1",
            "plan_path": str(plan_path),
            "plan_sha256": sha256_path(plan_path),
            "suite_harness_sha256": sha256_path(SUITE_PATH),
            "studies": manifest_rows,
            "private_oracle_visible_to_solver": False,
            "authority": {
                "grants_scientific_truth": False,
                "grants_F2_superiority": False,
                "grants_new_mathematical_theory": False,
            },
        },
    )


def dispatch(plan_path: Path, campaign_root: Path, studies: list[str], concurrency: int, overwrite: bool) -> None:
    plan = load_json(plan_path)
    suite = load_suite()
    rows = []
    for study_id in studies:
        workdir = campaign_root / study_id
        if not (workdir / "FROZEN_SUITE.json").exists():
            raise CampaignError(f"study has not been prepared: {study_id}")
        arms = list(plan["studies"][study_id]["arms"])
        suite.dispatch(workdir, arms, concurrency, overwrite)
        receipt = load_json(workdir / "DISPATCH_RECEIPT.json")
        rows.append(
            {
                "study_id": study_id,
                "all_returncodes_zero": receipt["all_returncodes_zero"],
                "oracle_restored_hash_match": receipt["oracle_restored_hash_match"],
                "jobs": len(receipt["jobs"]),
            }
        )
    write_json(
        campaign_root / "CAMPAIGN_DISPATCH_RECEIPT.json",
        {
            "schema_version": "orion.v2.formal-discovery-campaign-dispatch.v1",
            "studies": rows,
            "all_dispatches_zero": all(row["all_returncodes_zero"] for row in rows),
            "all_oracles_restored": all(row["oracle_restored_hash_match"] for row in rows),
        },
    )


def executed_arms(workdir: Path, registered: list[str]) -> list[str]:
    """Arm ids with a responses/ directory on disk - evidence, not intent.

    Reads the filesystem rather than the requested arm list so an arm that was
    registered and never dispatched is detected here instead of vanishing from the
    denominator.
    """
    responses = workdir / "responses"
    if not responses.exists():
        return []
    # A bare directory is not evidence of an arm: a .tmp leftover, __pycache__ or a scratch
    # dir would otherwise become a phantom executed arm, inflating ran_dispatches and
    # fabricating an unregistered-arm finding. Require at least one response file.
    found = {
        path.name
        for path in responses.iterdir()
        if path.is_dir() and any(path.glob("*.json"))
    }
    return sorted(found)


def evaluate(plan_path: Path, campaign_root: Path, studies: list[str]) -> None:
    plan = load_json(plan_path)
    suite = load_suite()
    aggregate: dict[str, Any] = {}
    coverage: dict[str, Any] = {}
    for study_id in studies:
        workdir = campaign_root / study_id
        arms = list(plan["studies"][study_id]["arms"])
        # The registered denominator comes from the PLAN, never from whatever was
        # dispatched. Passing `arms` for both would make coverage self-certifying.
        executed = executed_arms(workdir, arms)
        suite.evaluate(workdir, executed, arms)
        summary = load_json(workdir / "EVALUATION_SUMMARY.json")
        aggregate[study_id] = summary["summary"]
        coverage[study_id] = summary["coverage"]
    all_valid = all(
        all(arm_summary.get("run_valid", True) for arm_summary in study_summary.values())
        for study_summary in aggregate.values()
    )
    totals = {
        key: sum(row[key] for row in coverage.values())
        for key in (
            "registered_dispatches",
            "ran_dispatches",
            "valid_dispatches",
            "registered_never_ran_dispatches",
            "ran_but_unregistered_dispatches",
        )
    }
    totals["coverage_complete"] = all(row["coverage_complete"] for row in coverage.values())
    totals["studies_with_unrun_registered_arms"] = sorted(
        sid for sid, row in coverage.items() if row["registered_arms_never_run"]
    )
    write_json(
        campaign_root / "CAMPAIGN_EVALUATION_SUMMARY.json",
        {
            "schema_version": "orion.v2.formal-discovery-campaign-evaluation.v2",
            "all_runs_valid": all_valid,
            # registered / ran / valid, always together. `all_runs_valid` alone is a
            # statement about the executed subset and is not a coverage claim.
            "coverage_totals": totals,
            "coverage": coverage,
            "studies": aggregate,
            "authority": {
                "grants_scientific_truth": False,
                "grants_F2_superiority": False,
                "grants_new_mathematical_theory": False,
                "grants_R3": False,
                "grants_R4": False,
            },
        },
    )


def status(plan_path: Path, campaign_root: Path, studies: list[str]) -> dict[str, Any]:
    plan = load_json(plan_path)
    rows = []
    for study_id in studies:
        workdir = campaign_root / study_id
        frozen = (workdir / "FROZEN_SUITE.json").exists()
        dispatched = (workdir / "DISPATCH_RECEIPT.json").exists()
        evaluated = (workdir / "EVALUATION_SUMMARY.json").exists()
        spec = plan["studies"][study_id]
        registered = list(spec["arms"])
        ran = executed_arms(workdir, registered) if workdir.exists() else []
        never_ran = [arm for arm in registered if arm not in set(ran)]
        unregistered = [arm for arm in ran if arm not in set(registered)]
        rows.append(
            {
                "study_id": study_id,
                "registered_tasks": spec["tasks"],
                "registered_arms": len(registered),
                "executed_arms": len(ran),
                "registered_dispatches": spec["tasks"] * len(registered),
                "ran_dispatches": spec["tasks"] * len(ran),
                "registered_never_ran_dispatches": spec["tasks"] * len(never_ran),
                "ran_but_unregistered_dispatches": spec["tasks"] * len(unregistered),
                "registered_arms_never_run": never_ran,
                "executed_arms_not_registered": unregistered,
                "prepared": frozen,
                "dispatched": dispatched,
                "evaluated": evaluated,
            }
        )
    result = {
        "schema_version": "orion.v2.formal-discovery-campaign-status.v2",
        "registered_dispatches": sum(row["registered_dispatches"] for row in rows),
        "ran_dispatches": sum(row["ran_dispatches"] for row in rows),
        "registered_never_ran_dispatches": sum(row["registered_never_ran_dispatches"] for row in rows),
        "ran_but_unregistered_dispatches": sum(row["ran_but_unregistered_dispatches"] for row in rows),
        "studies": rows,
        "excluded_from_generated_campaign": plan.get("excluded_from_generated_campaign", {}),
    }
    write_json(campaign_root / "CAMPAIGN_STATUS.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "dispatch", "evaluate", "status", "all"):
        command = sub.add_parser(name)
        command.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
        command.add_argument("--campaign-root", type=Path, default=DEFAULT_ROOT)
        command.add_argument("--studies", default=None, help="optional comma-separated subset")
        if name in {"prepare", "all"}:
            command.add_argument("--force", action="store_true")
        if name in {"dispatch", "all"}:
            command.add_argument("--max-concurrency", type=int, default=2)
            command.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    plan = load_json(args.plan)
    studies = selected_studies(plan, args.studies)
    if args.command == "prepare":
        prepare(args.plan, args.campaign_root, studies, args.force)
    elif args.command == "dispatch":
        dispatch(args.plan, args.campaign_root, studies, args.max_concurrency, args.overwrite)
    elif args.command == "evaluate":
        evaluate(args.plan, args.campaign_root, studies)
    elif args.command == "status":
        print(json.dumps(status(args.plan, args.campaign_root, studies), indent=2, sort_keys=True))
    else:
        prepare(args.plan, args.campaign_root, studies, args.force)
        dispatch(args.plan, args.campaign_root, studies, args.max_concurrency, args.overwrite)
        evaluate(args.plan, args.campaign_root, studies)
        print(json.dumps(status(args.plan, args.campaign_root, studies), indent=2, sort_keys=True))
    if args.command not in {"evaluate", "all"}:
        # prepare/dispatch/status write no campaign evaluation summary. Reading one
        # unconditionally made every `prepare` exit on a FileNotFoundError traceback
        # after having done its work correctly.
        return 0
    campaign_summary = load_json(args.campaign_root / "CAMPAIGN_EVALUATION_SUMMARY.json")
    if not campaign_summary.get("all_runs_valid", True):
        print(
            "CAMPAIGN INVALID: execution failures present - responses are missing, "
            "the accuracies above are not verdicts. Re-dispatch with a working model backend.",
            file=sys.stderr,
        )
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
