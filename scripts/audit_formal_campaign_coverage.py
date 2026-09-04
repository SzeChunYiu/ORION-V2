#!/usr/bin/env python3
"""Reconcile a formal-discovery campaign's EXECUTED evidence against its REGISTERED plan.

Why this exists
---------------
The FM/FG R2 registered-scale campaign (2026-08-30) was dispatched through the
low-level harness `run_formal_discovery_generated_suite.py` with a uniform hardcoded
5-arm set, bypassing the plan-reading orchestrator `run_formal_discovery_campaign.py`.
Nothing detected the bypass. The terminal receipt reported **"8,560/8,560 valid"** - a
rate over the executed subset, presented as coverage, with the registered denominator
absent. It was not false; it answered a question nobody asked.

This auditor publishes **registered / ran / valid** as three numbers and names the set
differences, so the shortfall cannot be a silent omission from a denominator.

Two independently-failable clauses
----------------------------------
1. COVERAGE       - every registered dispatch ran, and nothing ran that was not registered.
2. CONSTRUCTIBILITY - every registered arm resolves to its own distinct procedure.

They are separate on purpose. A single gate demanding both is currently unsatisfiable
(the FM/FG arm table collapses 17 registered ids onto 6 instructions), and an
unsatisfiable gate terminates on vocabulary rather than on evidence.

Exit codes (bitwise, so several can be read at once)
----------------------------------------------------
    0  both clauses satisfied
    2  COVERAGE violated
    4  CONSTRUCTIBILITY violated
    6  both violated
    8  COULD NOT CHECK - plan unreadable, evidence absent, arm table unimportable.
       Distinct from every "checked and fine" and every "checked and failed" code.

--pre-registration audits a prospective plan that has no run: CONSTRUCTIBILITY is a
property of the plan and the arm table alone, so it is checkable before dispatch and is
the gate a successor plan must pass before it is frozen. COVERAGE is reported
NOT_APPLICABLE and never contributes to the exit code - it is not a pass.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json"
ARMS_MODULE = ROOT / "scripts/orion_formal_discovery_arms.py"

EXIT_OK = 0
EXIT_COVERAGE = 2
EXIT_CONSTRUCTIBILITY = 4
EXIT_COULD_NOT_CHECK = 8


class CouldNotCheck(RuntimeError):
    """Distinct from a failed check. Never report this as 'clean'."""


def load_plan(path: Path) -> dict[str, Any]:
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise CouldNotCheck(f"cannot read campaign plan {path}: {exc}") from exc
    if not isinstance(plan, dict) or not isinstance(plan.get("studies"), dict) or not plan["studies"]:
        raise CouldNotCheck(f"campaign plan has no studies: {path}")
    for study_id, spec in plan["studies"].items():
        if not isinstance(spec, dict) or not spec.get("arms") or not spec.get("tasks"):
            raise CouldNotCheck(f"study {study_id} has no registered tasks/arms")
    return plan


def load_arms_module():
    spec = importlib.util.spec_from_file_location("orion_formal_discovery_arms", ARMS_MODULE)
    if spec is None or spec.loader is None:
        raise CouldNotCheck(f"cannot import arm table {ARMS_MODULE}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise CouldNotCheck(f"cannot import arm table {ARMS_MODULE}: {exc}") from exc
    if not hasattr(module, "ARM_PROCEDURE_CLASS"):
        raise CouldNotCheck("arm table exposes no ARM_PROCEDURE_CLASS registry")
    return module


def executed_from_summaries(paths: list[Path]) -> dict[str, dict[str, int]]:
    """Read per-arm executed/valid counts out of archived EVALUATION_SUMMARY files."""
    if not paths:
        raise CouldNotCheck("no evidence supplied (--summary / --campaign-root)")
    executed: dict[str, dict[str, int]] = {}
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            summary = data["summary"]
        except Exception as exc:
            raise CouldNotCheck(f"cannot read evaluation summary {path}: {exc}") from exc
        for arm, row in summary.items():
            bucket = executed.setdefault(arm, {"ran": 0, "valid": 0})
            bucket["ran"] += int(row["tasks"])
            bucket["valid"] += int(row["tasks"]) - int(row.get("missing_or_invalid", 0))
    if not executed:
        raise CouldNotCheck("evaluation summaries contained no arms")
    return executed


def audit(plan: dict[str, Any], executed: dict[str, dict[str, int]], arms_module) -> dict[str, Any]:
    studies = plan["studies"]
    registered_ids = sorted({arm for spec in studies.values() for arm in spec["arms"]})
    executed_ids = sorted(executed)
    tasks_total = sum(int(spec["tasks"]) for spec in studies.values())

    registered_dispatches = sum(int(spec["tasks"]) * len(spec["arms"]) for spec in studies.values())
    ran_dispatches = sum(row["ran"] for row in executed.values())
    valid_dispatches = sum(row["valid"] for row in executed.values())

    # Identity rule: exact arm-id match. Stated, because it decides the numbers.
    executed_set = set(executed_ids)
    both = sum(
        int(spec["tasks"]) * len([a for a in spec["arms"] if a in executed_set])
        for spec in studies.values()
    )
    never_ran = registered_dispatches - both
    unregistered_ran = ran_dispatches - both

    per_study = []
    for study_id, spec in sorted(studies.items()):
        registered = list(spec["arms"])
        matched = [a for a in registered if a in executed_set]
        missing = [a for a in registered if a not in executed_set]
        per_study.append(
            {
                "study_id": study_id,
                "tasks": int(spec["tasks"]),
                "registered_arms": registered,
                "registered_arms_never_run": missing,
                "registered_dispatches": int(spec["tasks"]) * len(registered),
                "registered_and_ran_dispatches": int(spec["tasks"]) * len(matched),
                "registered_never_ran_dispatches": int(spec["tasks"]) * len(missing),
            }
        )

    # --- clause 2: constructibility --------------------------------------------
    groups: dict[str, list[str]] = {}
    unregistered_in_table, unspecified = [], []
    for arm in registered_ids:
        if arm not in arms_module.ARM_PROCEDURE_CLASS:
            unregistered_in_table.append(arm)
            continue
        procedure = arms_module.ARM_PROCEDURE_CLASS[arm]
        if procedure is None:
            unspecified.append(arm)
            continue
        groups.setdefault(procedure, []).append(arm)
    collapses = {k: sorted(v) for k, v in sorted(groups.items()) if len(v) > 1}
    collapsed_arms = sorted(a for v in collapses.values() for a in v)

    coverage_ok = never_ran == 0 and unregistered_ran == 0
    constructible_ok = not collapses and not unspecified and not unregistered_in_table

    return {
        "schema_version": "orion.v2.formal-campaign-coverage-audit.v1",
        "identity_rule": "EXACT_ARM_ID_MATCH",
        "registered_arm_ids": registered_ids,
        "executed_arm_ids": executed_ids,
        "tasks": tasks_total,
        "three_numbers": {
            "registered_dispatches": registered_dispatches,
            "ran_dispatches": ran_dispatches,
            "valid_dispatches": valid_dispatches,
        },
        "coverage": {
            "clause_satisfied": coverage_ok,
            "registered_and_ran_dispatches": both,
            "registered_never_ran_dispatches": never_ran,
            "ran_but_unregistered_dispatches": unregistered_ran,
            "registered_arm_ids_never_run": [a for a in registered_ids if a not in executed_set],
            "executed_arm_ids_registered_for_no_study": [
                a for a in executed_ids if a not in set(registered_ids)
            ],
            "per_study": per_study,
        },
        "constructibility": {
            "clause_satisfied": constructible_ok,
            "registered_arm_ids": len(registered_ids),
            "distinct_procedures": len(groups),
            "collapse_classes": collapses,
            "collapsed_arm_ids": collapsed_arms,
            "registered_but_procedure_unspecified": unspecified,
            "registered_but_absent_from_arm_table": unregistered_in_table,
        },
        "authority": {
            "grants_scientific_truth": False,
            "grants_F2_superiority": False,
            "grants_new_mathematical_theory": False,
        },
    }


def render(report: dict[str, Any]) -> str:
    three = report["three_numbers"]
    cov, con = report["coverage"], report["constructibility"]
    lines = [
        "FORMAL CAMPAIGN COVERAGE AUDIT",
        f"identity rule: {report['identity_rule']}",
        "",
        "THREE NUMBERS (never one ratio over the executed subset)",
        f"  registered dispatches : {three['registered_dispatches']:,}",
        f"  ran dispatches        : {three['ran_dispatches']:,}",
        f"  valid dispatches      : {three['valid_dispatches']:,}",
        "",
        f"CLAUSE 1 COVERAGE .......... {'SATISFIED' if cov['clause_satisfied'] else 'VIOLATED'}",
        f"  registered and ran    : {cov['registered_and_ran_dispatches']:,}",
        f"  registered, never ran : {cov['registered_never_ran_dispatches']:,}",
        f"  ran, not registered   : {cov['ran_but_unregistered_dispatches']:,}",
    ]
    if cov["registered_arm_ids_never_run"]:
        lines.append(f"  registered arm ids never run ({len(cov['registered_arm_ids_never_run'])}):")
        lines += [f"      - {a}" for a in cov["registered_arm_ids_never_run"]]
    if cov["executed_arm_ids_registered_for_no_study"]:
        lines.append("  executed arm ids registered for NO study:")
        lines += [f"      - {a}" for a in cov["executed_arm_ids_registered_for_no_study"]]
    lines += [
        "",
        f"CLAUSE 2 CONSTRUCTIBILITY .. {'SATISFIED' if con['clause_satisfied'] else 'VIOLATED'}",
        f"  {con['registered_arm_ids']} registered arm ids -> {con['distinct_procedures']} distinct procedures",
    ]
    for procedure, members in con["collapse_classes"].items():
        lines.append(f"  COLLAPSE [{procedure}] {len(members)} arms share one instruction:")
        lines += [f"      - {a}" for a in members]
    for arm in con["registered_but_procedure_unspecified"]:
        lines.append(f"  UNSPECIFIED PROCEDURE: {arm}")
    for arm in con["registered_but_absent_from_arm_table"]:
        lines.append(f"  ABSENT FROM ARM TABLE: {arm}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--summary", type=Path, action="append", default=[],
                        help="an EVALUATION_SUMMARY json (repeatable)")
    parser.add_argument("--campaign-root", type=Path, default=None,
                        help="directory searched recursively for EVALUATION_SUMMARY*.json")
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--pre-registration", action="store_true",
                        help="check CONSTRUCTIBILITY alone, with no executed evidence. For a "
                             "prospective plan being frozen: whether every registered arm "
                             "resolves to its own procedure is a property of the plan and the "
                             "arm table, and needs no run. COVERAGE is reported NOT_APPLICABLE "
                             "and never contributes to the exit code.")
    args = parser.parse_args()

    try:
        summaries = list(args.summary)
        if args.campaign_root is not None:
            if not args.campaign_root.exists():
                raise CouldNotCheck(f"campaign root does not exist: {args.campaign_root}")
            summaries += sorted(args.campaign_root.rglob("EVALUATION_SUMMARY*.json"))
        if args.pre_registration:
            if summaries:
                raise CouldNotCheck(
                    "--pre-registration audits a plan with no run; evidence was supplied. "
                    "Drop --summary/--campaign-root, or drop --pre-registration to audit both clauses."
                )
            report = audit(load_plan(args.plan), {}, load_arms_module())
            report["coverage"] = {"clause_satisfied": None, "mode": "NOT_APPLICABLE_PRE_REGISTRATION"}
            report["mode"] = "PRE_REGISTRATION"
        else:
            report = audit(load_plan(args.plan), executed_from_summaries(summaries), load_arms_module())
    except CouldNotCheck as exc:
        print(f"COULD NOT CHECK: {exc}", file=sys.stderr)
        print("This is NOT a clean result. Exit 8 is distinct from exit 0.", file=sys.stderr)
        return EXIT_COULD_NOT_CHECK

    if args.pre_registration:
        con = report["constructibility"]
        print("FORMAL CAMPAIGN PRE-REGISTRATION AUDIT (CONSTRUCTIBILITY only)")
        print(f"  plan ........................ {args.plan}")
        print(f"  registered arm ids .......... {con['registered_arm_ids']}")
        print(f"  distinct procedures ......... {con['distinct_procedures']}")
        print(f"  CLAUSE 2 CONSTRUCTIBILITY ... {'SATISFIED' if con['clause_satisfied'] else 'VIOLATED'}")
        print("  CLAUSE 1 COVERAGE ........... NOT APPLICABLE (no run; this is not a pass)")
        for cls, ids in sorted((con["collapse_classes"] or {}).items()):
            print(f"    COLLAPSE {cls}: {', '.join(ids)}")
        for arm in con["registered_but_procedure_unspecified"]:
            print(f"    NO PROCEDURE DESIGNED: {arm}")
        for arm in con["registered_but_absent_from_arm_table"]:
            print(f"    ABSENT FROM ARM TABLE: {arm}")
    else:
        print(render(report))
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    code = EXIT_OK
    if not args.pre_registration and not report["coverage"]["clause_satisfied"]:
        code |= EXIT_COVERAGE
    if not report["constructibility"]["clause_satisfied"]:
        code |= EXIT_CONSTRUCTIBILITY
    return code


if __name__ == "__main__":
    raise SystemExit(main())
