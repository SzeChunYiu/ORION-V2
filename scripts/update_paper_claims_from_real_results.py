#!/usr/bin/env python3
"""Generate a non-authorizing paper-claim update from real-problem results.

The script never edits manuscript prose or the canonical claim ledger. It writes
an outcome-bound proposal under WORKDIR/aggregate/paper_claim_updates.json for
independent scientific and editorial review.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class ClaimUpdateError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ClaimUpdateError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ClaimUpdateError(f"expected object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def primary_comparison(analysis: dict[str, Any], right_arm: str) -> dict[str, Any] | None:
    for item in analysis.get("primary_comparisons", []):
        if item.get("left_arm") == "F2_ORION_METABOLIC_FULL" and item.get("right_arm") == right_arm:
            return item
    return None


def represented_domains(workdir: Path) -> set[str]:
    domains: set[str] = set()
    for path in (workdir / "evaluations").glob("*/*.json"):
        item = read_json(path)
        benchmark = str(item.get("benchmark_id", ""))
        if benchmark:
            domains.add(benchmark)
    return domains


def update_claims(
    ledger: dict[str, Any], analysis: dict[str, Any], workdir: Path
) -> dict[str, Any]:
    f0 = primary_comparison(analysis, "F0_PARENT_FEDERATION")
    domains = represented_domains(workdir)
    updates: list[dict[str, Any]] = []

    f2_f0_status = "CANNOT_CHECK"
    f2_f0_reason = "paired F2/F0 confirmatory evidence is unavailable"
    paired_count = 0
    effect = None
    interval = [None, None]
    if f0:
        paired_count = int(f0.get("paired_task_count", 0))
        risk = f0.get("success", {}).get("risk_difference", {})
        effect = risk.get("estimate")
        interval = risk.get("ci95", [None, None])
        hard_gate = analysis.get("hard_gate_state")
        if paired_count < 40:
            f2_f0_status = "PILOT_OR_UNDERPOWERED"
            f2_f0_reason = f"only {paired_count} paired tasks; 40 required by the analysis plan"
        elif hard_gate != "PASS_DESCRIPTIVE_ONLY":
            f2_f0_status = "HARD_GATE_NOT_PASSED"
            f2_f0_reason = f"hard gate state is {hard_gate}"
        elif effect is None:
            f2_f0_status = "CANNOT_CHECK"
            f2_f0_reason = "success effect is missing"
        elif effect > 0 and interval[0] is not None and interval[0] > 0:
            f2_f0_status = "SUPPORTED_IN_BOUNDED_DEBUGGING_TRANCHE"
            f2_f0_reason = "paired success interval is above zero and descriptive hard gate passed"
        elif effect <= 0:
            f2_f0_status = "PARENT_TIE_OR_WIN"
            f2_f0_reason = "F2 did not improve paired success over F0"
        else:
            f2_f0_status = "INCONCLUSIVE_INTERVAL"
            f2_f0_reason = "point estimate is positive but uncertainty crosses zero"

    component_effects = analysis.get("component_effects", {})
    counterprobe = component_effects.get("F2_MINUS_COUNTERPROBE", {})
    selective = component_effects.get("F2_MINUS_SELECTIVE_REOPEN", {})
    decomposition = component_effects.get("F2_MINUS_DECOMPOSITION", {})
    recovery = component_effects.get("F2_MINUS_NATIVE_RECOVERY", {})

    for claim in ledger.get("claims", []):
        claim_id = claim["claim_id"]
        status = claim.get("current_terminal", "OPEN")
        reason = "no automatic update rule; independent review required"
        evidence: list[str] = []

        if claim_id == "KM-C1":
            status = "SUPPORTED_AS_REFERENCE_SEMANTICS_ONLY"
            reason = "unit/reference semantics exist; naturalistic atomization evidence remains open"
            evidence = claim.get("current_evidence", [])
        elif claim_id == "KM-C2":
            disposition = recovery.get("component_disposition")
            if disposition == "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE":
                status = "COMPONENT_VALUE_CANDIDATE_IN_BOUNDED_TRANCHE"
                reason = "native-recovery ablation shows a registered effect candidate"
                evidence = ["aggregate/component_effects.json#F2_MINUS_NATIVE_RECOVERY"]
            else:
                status = disposition or "CANNOT_CHECK"
                reason = "native-recovery residual is not established"
        elif claim_id == "KM-C3":
            status = f2_f0_status
            reason = f2_f0_reason
            evidence = ["aggregate/paired_comparisons.json#F2_vs_F0"] if f0 else []
        elif claim_id == "KM-C4":
            status = counterprobe.get("component_disposition", "CANNOT_CHECK")
            reason = "derived from the frozen counterprobe ablation"
            evidence = ["aggregate/component_effects.json#F2_MINUS_COUNTERPROBE"]
        elif claim_id == "KM-C5":
            status = selective.get("component_disposition", "CANNOT_CHECK")
            reason = "derived from the frozen selective-reopen ablation"
            evidence = ["aggregate/component_effects.json#F2_MINUS_SELECTIVE_REOPEN"]
        elif claim_id == "KM-C6":
            if f2_f0_status in {
                "SUPPORTED_IN_BOUNDED_DEBUGGING_TRANCHE",
                "PARENT_TIE_OR_WIN",
            } and decomposition and recovery:
                status = "SCOPE_AND_DRAG_ANALYSIS_AVAILABLE"
                reason = "full, parent and ablation results exist for bounded activation analysis"
                evidence = ["aggregate/resource_pareto.json", "aggregate/component_effects.json"]
            else:
                status = "CANNOT_CHECK_ACTIVATION_POLICY"
                reason = "matched quality-cost and ablation evidence is incomplete"
        elif claim_id == "KM-C7":
            anti_copy_path = workdir / "aggregate" / "anti_copy_controls.json"
            if anti_copy_path.exists():
                anti_copy = read_json(anti_copy_path)
                if anti_copy.get("counterfactual_success_supported") is True:
                    status = "CONVERGENT_ANTI_COPY_EVIDENCE_IN_BOUNDED_TRANCHE"
                    reason = "gold-blind executable and newly generated counterfactual controls passed"
                    evidence = ["aggregate/anti_copy_controls.json"]
                else:
                    status = "ANTI_COPY_EVIDENCE_INCOMPLETE_OR_NEGATIVE"
                    reason = "counterfactual or access controls do not support the bounded hypothesis"
            else:
                status = "CANNOT_CHECK_ANTI_COPY_CONTROLS_NOT_RUN"
                reason = "anti-copy control artifact is absent"
        elif claim_id == "KM-C8":
            distinct_components = {
                item.get("component_disposition")
                for item in (decomposition, recovery, counterprobe, selective)
            }
            if (
                f2_f0_status == "SUPPORTED_IN_BOUNDED_DEBUGGING_TRANCHE"
                and len(domains) >= 2
                and "NECESSARY_OR_CONTEXTUAL_VALUE_CANDIDATE" in distinct_components
            ):
                status = "P_G_STANDALONE_CANDIDATE_FOR_INDEPENDENT_REVIEW"
                reason = "bounded F0 residual, cross-domain evidence and component attribution are present"
                evidence = [
                    "aggregate/paired_comparisons.json",
                    "aggregate/component_effects.json",
                    "aggregate/resource_pareto.json",
                ]
            else:
                status = "P_G_MERGE_OR_CANNOT_CHECK"
                reason = "standalone residual or cross-domain component evidence is absent"

        updates.append(
            {
                "claim_id": claim_id,
                "paper_mapping": claim.get("paper_mapping", []),
                "proposed_status": status,
                "reason": reason,
                "evidence_artifacts": evidence,
                "requires_independent_review": True,
            }
        )

    return {
        "schema_version": "orion.v2.paper-claim-update.v1",
        "source_ledger": "papers/verification/KNOWLEDGE_METABOLISM_CLAIM_EXPERIMENT_LEDGER_V1.json",
        "source_analysis": "aggregate/analysis.json",
        "represented_domains": sorted(domains),
        "f2_vs_f0": {
            "status": f2_f0_status,
            "paired_task_count": paired_count,
            "success_risk_difference": effect,
            "ci95": interval,
            "reason": f2_f0_reason,
        },
        "claim_updates": updates,
        "automatic_manuscript_editing_authorized": False,
        "field_status": "NOT_ESTABLISHED",
        "publication_readiness": "NOT_ESTABLISHED",
        "authority": {
            "scientific_truth": False,
            "novelty": False,
            "field_status": False,
            "submission_readiness": False,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path(
            "papers/verification/KNOWLEDGE_METABOLISM_CLAIM_EXPERIMENT_LEDGER_V1.json"
        ),
    )
    args = parser.parse_args(argv)
    try:
        ledger = read_json(args.ledger)
        analysis = read_json(args.workdir / "aggregate" / "analysis.json")
        result = update_claims(ledger, analysis, args.workdir)
        write_json(args.workdir / "aggregate" / "paper_claim_updates.json", result)
    except (ClaimUpdateError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
