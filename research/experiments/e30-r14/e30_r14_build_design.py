#!/usr/bin/env python3
"""Emit E30_R14_INTERFACE_CONTRACT_RERUN_DESIGN_V1.json from the measured calibration.

Run once, before freeze, AFTER the 2x2 interface calibration has a measurement in every
cell.  The selection rule below is written before any cell is measured and is the only
rule this script applies:

  * the registered interface is the calibration cell with the LOWEST apply-failure rate
    (ties broken toward the historical ``unified_diff``/``per_file_cap`` cell, so that a
    change of interface must be earned);
  * registration REQUIRES that cell's apply-failure rate to be at most the GR1 ceiling
    (0.40) on the calibration itself: an interface that cannot clear the ceiling on one
    call per task will not clear it on three, and R14 would be R13 under a new name.  If
    no cell clears it the script writes NO design and exits 4 with terminal
    ``INTERFACE_CALIBRATION_ABOVE_CEILING`` -- a CANNOT_CHECK-class outcome for R14, and a
    negative for the interface lever that goes back to attribution;
  * every cell must have completed on every task (a cell with envelope failures is
    ``COULD_NOT_CHECK`` and the script exits 5): a calibration the channel did not answer
    is not a calibration.

Everything else -- the request-body contract, the per-call cap, the served-model pin, the
40 tasks, the four arms, three repetitions, the endpoints, the Holm families, GR1's
ceiling -- is inherited verbatim from E30-R13's frozen design by reading it, not retyping
it, and the interface fingerprint is computed by the arms executable under the chosen
condition rather than copied from the calibration file.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
CALIBRATION = Path(sys.argv[2]).resolve()
R14 = ROOT / "research" / "experiments" / "e30-r14"
R13 = ROOT / "research" / "experiments" / "e30-r13"
OUT = R14 / "E30_R14_INTERFACE_CONTRACT_RERUN_DESIGN_V1.json"
GR1_CEILING = 0.40
HISTORICAL = "unified_diff|per_file_cap"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if OUT.exists():
        print(f"REFUSED: {OUT.name} exists; a design is frozen once", file=sys.stderr)
        return 3
    cal = json.loads(CALIBRATION.read_text())
    assert cal["schema_version"] == "orion.v2.e30-r14-interface-calibration.v1"
    assert cal["is_an_endpoint_read"] is False and cal["response_text_retained"] is False
    summary = cal["summary"]
    n_tasks = len(cal["parameters"]["tasks"])
    incomplete = {k: v for k, v in summary.items() if v["completed_envelopes"] != n_tasks or v["calls"] != n_tasks}
    if incomplete:
        print("CALIBRATION_INCOMPLETE:", json.dumps({k: {"calls": v["calls"], "completed": v["completed_envelopes"]}
                                                     for k, v in incomplete.items()}), file=sys.stderr)
        return 5
    ranked = sorted(summary.items(), key=lambda kv: (kv[1]["apply_failure_rate"], kv[0] != HISTORICAL))
    chosen, chosen_summary = ranked[0]
    if chosen_summary["apply_failure_rate"] > GR1_CEILING:
        print(f"INTERFACE_CALIBRATION_ABOVE_CEILING: best cell {chosen} apply-failure "
              f"{chosen_summary['apply_failure_rate']:.4f} > {GR1_CEILING}; no design written", file=sys.stderr)
        return 4
    interface, presentation = chosen.split("|")

    spec = importlib.util.spec_from_file_location("arms", ROOT / "scripts" / "orion_claude_arms.py")
    arms = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(arms)
    os.environ["ORION_EDIT_INTERFACE"] = interface
    os.environ["ORION_PRESENTATION_POLICY"] = presentation
    assert arms.edit_interface_id() == interface and arms.presentation_policy() == presentation
    interface_sha = arms.edit_interface_sha256(interface)
    assert interface_sha in chosen_summary["interface_sha256s"], (interface_sha, chosen_summary["interface_sha256s"])

    r13 = json.loads((R13 / "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json").read_text())
    attribution = json.loads((R14 / "results" / "E30_R14_R13_APPLY_FAILURE_ATTRIBUTION_V1.json").read_text())
    design = {
        "schema_version": "orion.v2.e30-r14-design.v1",
        "study_id": "E30-R14",
        "title": "Confirmatory BugsInPy re-run under a registered arm<->workspace interface contract",
        "state_date": "2026-09-04",
        "status": "PROSPECTIVE_REGISTERED_DESIGN_NO_RESULTS",
        "class": "new prospective confirmatory study under a NEW campaign identity; not a re-analysis and "
                 "not a repair of E30-R13's campaign",
        "anchor_commit": r13["anchor_commit"],
        "question": r13["question"],
        "why_this_study_exists": {
            "e30_r13_terminal": "INTERFACE_STILL_BROKEN",
            "attributed_stage": attribution["attribution"]["stage"],
            "attribution_artifact": "results/E30_R14_R13_APPLY_FAILURE_ATTRIBUTION_V1.json",
            "attribution_sha256": sha256_file(R14 / "results" / "E30_R14_R13_APPLY_FAILURE_ATTRIBUTION_V1.json"),
            "sub_stage_presentation": attribution["attribution"]["sub_stage_presentation"],
            "sub_stage_emission": attribution["attribution"]["sub_stage_emission"],
            "emission_only_ceiling": attribution["attribution"]["apply_rate_ceiling_of_an_emission_only_lever_on_archived_text"],
        },
        "interface_binding": {
            "edit_interface": interface,
            "presentation_policy": presentation,
            "edit_interface_sha256": interface_sha,
            "emission_module": arms.EDIT_INTERFACES[interface]["emission"],
            "selection_rule": "lowest calibration apply-failure among the four cells, ties toward the historical "
                              "cell; registration requires apply-failure <= 0.40 on the calibration",
            "selected_from_calibration": {k: {"apply_failure_rate": v["apply_failure_rate"], "applied": v["applied"],
                                              "completed_envelopes": v["completed_envelopes"],
                                              "emission_statuses": v["emission_statuses"]} for k, v in summary.items()},
            "calibration_artifact": str(CALIBRATION.name),
            "calibration_sha256": sha256_file(CALIBRATION),
            "calibration_is_an_endpoint_read": False,
            "recorded_per_envelope_as": "interface_receipt",
        },
        "model_binding": r13["model_binding"],
        "execution_lane_contract": r13["execution_lane_contract"],
        "arms": r13["arms"], "substrate": r13["substrate"], "repetitions": r13["repetitions"],
        "task_dispositions_registered_pre_dispatch": r13["task_dispositions_registered_pre_dispatch"],
        "expected_responses": r13["expected_responses"], "expected_evaluations": r13["expected_evaluations"],
        "statistics": r13["statistics"], "power_note": r13["power_note"],
        "endpoints": r13["endpoints"], "gates": {
            **r13["gates"],
            "GR0f_INTERFACE_HOMOGENEITY": {
                "status": "HARD", "reads": "interface_receipt on every envelope",
                "pass": "480/480 receipts; one interface id and one sha256 equal to interface_binding; zero "
                        "mentioned files truncated under mentioned_files_full",
                "fail_terminal": "INTERFACE_CONTRACT_VIOLATION",
                "could_not_check_terminal": "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ",
                "position": "ahead of GR0c/GR0d/GR0e and every endpoint",
            },
        },
        "routing_precedence": ["INTERFACE_CONTRACT_VIOLATION (GR0f)", *r13["routing_precedence"]],
        "inherited_verbatim_from_e30_r13": ["model_binding", "execution_lane_contract", "arms", "substrate",
                                            "repetitions", "task_dispositions_registered_pre_dispatch",
                                            "expected_responses", "expected_evaluations", "statistics", "power_note",
                                            "endpoints", "gates (all but GR0f)", "routing_precedence"],
        "e30_r13_design_sha256": sha256_file(R13 / "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json"),
        "analysis": {"module": "research/experiments/e30-r14/e30_r14_analysis.py",
                     "imports": "research/experiments/e30-r13/e30_r13_analysis.py under a sha256 pin, which imports "
                                "e30_r12_analysis.py under its own pin"},
        "no_rescue": True,
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "grants_publication_readiness": False, "changes_e30_r13": False},
    }
    OUT.write_text(json.dumps(design, indent=2, sort_keys=True) + "\n")
    print(f"frozen design: {OUT.name} sha256 {sha256_file(OUT)} interface={interface}|{presentation} sha={interface_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
