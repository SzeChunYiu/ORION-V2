#!/usr/bin/env python3
"""E30-R14 registered analysis: E30-R13's analysis plus one hard gate on the interface.

E30-R13 registered the served model (GR0c), the request-body contract (GR0d) and the
channel's behaviour (GR0e), and still could not test repair: the arm<->workspace
INTERFACE was unregistered, and 346 of 480 emitted diffs did not apply.  E30-R14
registers the interface -- the edit contract the model is asked for and the
presentation policy the workspace is shown under -- and gates on it per envelope.

``GR0f  INTERFACE_HOMOGENEITY``
    Every envelope carries an ``interface_receipt``; one interface id and one
    interface sha256 across the campaign, equal to the registered pair; and, under
    the ``mentioned_files_full`` presentation policy, no envelope reports a truncated
    baseline-mentioned file.  Reachable failure modes: a receipt absent (an arm built
    from the wrong source), two fingerprints (drift mid-campaign), a truncated
    mentioned file (the presentation policy silently reverted to the per-file cap).

Everything else -- GR0c/GR0d/GR0e, GR1 apply-rate diagnostic, the E1/E2 endpoint
arithmetic, bootstrap, Holm families and routing -- is **imported from
E30-R13's analysis module by path under a sha256 pin**, exactly as R13 imported R12's.
GR0f is evaluated with the other hard gates BEFORE any endpoint is read, and a
failure writes the refusal artifact and nothing else.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "orion.v2.e30-r14-analysis.v1"
DESIGN_ID = "E30_R14_INTERFACE_CONTRACT_RERUN_DESIGN_V1"
R13_ANALYSIS_RELATIVE = Path("..") / "e30-r13" / "e30_r13_analysis.py"
EXIT_PRECONDITION_REFUSED = 3
EXIT_GATE_FAIL = 4
EXIT_GATE_CANNOT_CHECK = 5


class AnalysisRefused(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pinned(path: Path, expected_sha256: str | None, name: str):
    if not path.is_file():
        raise AnalysisRefused(f"{name} not found at {path}")
    got = sha256_file(path)
    if expected_sha256 and got != expected_sha256:
        raise AnalysisRefused(f"{name} sha256 {got} != pinned {expected_sha256}; "
                              "the imported arithmetic is not the registered arithmetic")
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, got


def interface_homogeneity(campaign: Path, arms: list[str], reps: list[str], task_ids: list[str],
                          expected_interface: str, expected_interface_sha256: str,
                          expected_presentation: str, iter_envelopes) -> dict[str, Any]:
    """GR0f: one registered interface across the campaign, and the presentation it promises."""
    offenders: list[dict[str, Any]] = []
    id_counts: dict[str, int] = {}
    sha_counts: dict[str, int] = {}
    policy_counts: dict[str, int] = {}
    envelopes_read = 0
    envelopes_with_a_receipt = 0
    mentioned_truncated_total = 0
    for rep, arm, task_id, path in iter_envelopes(campaign, arms, reps, task_ids):
        where = {"rep": rep, "arm": arm, "task_id": task_id}
        if not path.is_file():
            offenders.append(where | {"reason": "RESPONSE_MISSING"})
            continue
        envelopes_read += 1
        envelope = json.loads(path.read_text())
        receipt = envelope.get("interface_receipt")
        if not isinstance(receipt, dict):
            offenders.append(where | {"reason": "INTERFACE_RECEIPT_ABSENT"})
            continue
        envelopes_with_a_receipt += 1
        iface = str(receipt.get("edit_interface", ""))
        sha = str(receipt.get("edit_interface_sha256", ""))
        presentation = receipt.get("presentation") if isinstance(receipt.get("presentation"), dict) else {}
        policy = str(presentation.get("presentation_policy", ""))
        id_counts[iface] = id_counts.get(iface, 0) + 1
        sha_counts[sha] = sha_counts.get(sha, 0) + 1
        policy_counts[policy] = policy_counts.get(policy, 0) + 1
        if iface != expected_interface:
            offenders.append(where | {"reason": "INTERFACE_ID_MISMATCH", "observed": iface})
        if sha != expected_interface_sha256:
            offenders.append(where | {"reason": "INTERFACE_SHA256_MISMATCH", "observed": sha})
        if policy != expected_presentation:
            offenders.append(where | {"reason": "PRESENTATION_POLICY_MISMATCH", "observed": policy})
        truncated = int(presentation.get("mentioned_files_truncated", 0) or 0)
        mentioned_truncated_total += truncated
        if expected_presentation == "mentioned_files_full" and truncated:
            offenders.append(where | {"reason": "MENTIONED_FILE_TRUNCATED_UNDER_FULL_POLICY",
                                      "mentioned_files_truncated": truncated})
    if envelopes_with_a_receipt == 0:
        status = "COULD_NOT_CHECK"
    elif offenders or len(sha_counts) != 1:
        status = "FAIL"
    else:
        status = "PASS"
    return {
        "gate_id": "GR0f", "name": "INTERFACE_HOMOGENEITY",
        "expected_interface": expected_interface,
        "expected_interface_sha256": expected_interface_sha256,
        "expected_presentation_policy": expected_presentation,
        "envelopes_expected": len(reps) * len(arms) * len(task_ids),
        "envelopes_read": envelopes_read,
        "envelopes_with_a_channel_receipt": envelopes_with_a_receipt,   # the key the shared renderer reads
        "envelopes_with_an_interface_receipt": envelopes_with_a_receipt,
        "interface_id_counts": id_counts,
        "interface_sha256_counts": sha_counts,
        "presentation_policy_counts": policy_counts,
        "mentioned_files_truncated_total": mentioned_truncated_total,
        "offenders": offenders[:50],
        "offender_count": len(offenders),
        "status": status,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rollup", type=Path, required=True)
    parser.add_argument("--gr0", type=Path, required=True)
    parser.add_argument("--gr0b", type=Path)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--analyzer", type=Path, required=True)
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--r13-analysis", type=Path,
                        default=(Path(__file__).resolve().parent / R13_ANALYSIS_RELATIVE).resolve())
    parser.add_argument("--r13-analysis-sha256")
    parser.add_argument("--r12-analysis", type=Path, required=True)
    parser.add_argument("--r12-analysis-sha256", required=True)
    parser.add_argument("--served-model", default="glm-5.3")
    parser.add_argument("--channel-contract", required=True)
    parser.add_argument("--channel-contract-sha256", required=True)
    parser.add_argument("--edit-interface", required=True)
    parser.add_argument("--edit-interface-sha256", required=True)
    parser.add_argument("--presentation-policy", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        r13, r13_sha = load_pinned(args.r13_analysis, args.r13_analysis_sha256, "e30_r13_analysis_imported")
        r12, r12_sha = r13.load_r12_analysis(args.r12_analysis, args.r12_analysis_sha256)
    except (AnalysisRefused, RuntimeError) as exc:
        print(f"ANALYSIS_REFUSED: {exc}", file=sys.stderr)
        return EXIT_PRECONDITION_REFUSED

    design = json.loads(args.design.read_text())
    registered = design["interface_binding"]
    if (registered["edit_interface"] != args.edit_interface
            or registered["edit_interface_sha256"] != args.edit_interface_sha256
            or registered["presentation_policy"] != args.presentation_policy):
        print("ANALYSIS_REFUSED: the interface the analysis was told to gate on is not the one the "
              "design registers", file=sys.stderr)
        return EXIT_PRECONDITION_REFUSED

    rollup = json.loads(args.rollup.read_text())
    cell = rollup["cells"][r13.CELL_NAME]
    gr0f = interface_homogeneity(args.campaign, cell["arms"], cell["reps"], cell["task_ids"],
                                 args.edit_interface, args.edit_interface_sha256,
                                 args.presentation_policy, r13._iter_envelopes)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "E30_R14_GR0F_INTERFACE_HOMOGENEITY_V1.json").write_text(json.dumps(gr0f, indent=2, sort_keys=True) + "\n")

    if gr0f["status"] != "PASS":
        terminal = ("EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ" if gr0f["status"] == "COULD_NOT_CHECK"
                    else "INTERFACE_CONTRACT_VIOLATION")
        refusal = {
            "schema_version": SCHEMA, "design": DESIGN_ID,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "status": "HALTED_BEFORE_ENDPOINT_READ",
            "inputs": {"rollup_sha256": sha256_file(args.rollup), "design_sha256": sha256_file(args.design),
                       "e30_r13_analysis_sha256": r13_sha, "e30_r12_analysis_sha256": r12_sha,
                       "campaign": str(args.campaign)},
            "gates": {"GR0f": gr0f},
            "routing": {"terminal": terminal,
                        "detail": f"GR0f INTERFACE_HOMOGENEITY {gr0f['status']} with {gr0f['offender_count']} "
                                  f"offenders over {gr0f['envelopes_with_an_interface_receipt']} envelopes carrying "
                                  "an interface receipt; no endpoint may be read"},
            "endpoints_read": [], "endpoint_tables_computed": False,
            "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                          "grants_publication_readiness": False},
        }
        (args.out / "E30_R14_OUTCOME_ROLLUP_V1.json").write_text(json.dumps(refusal, indent=2, sort_keys=True) + "\n")
        (args.out / "E30_R14_OUTCOME_ROLLUP_V1.md").write_text(
            "# E30-R14 — halted before any endpoint was read\n\n"
            f"**Terminal: `{terminal}`.** {refusal['routing']['detail']}\n")
        print(f"GR0f {gr0f['status']}: {terminal}")
        return EXIT_GATE_CANNOT_CHECK if gr0f["status"] == "COULD_NOT_CHECK" else EXIT_GATE_FAIL

    # GR0f passed: hand over to E30-R13's analysis, which evaluates GR0c/d/e first and then
    # the registered endpoints, routing and rendering, writing E30_R13_* names into --out.
    rc = r13.main([
        "--rollup", str(args.rollup), "--gr0", str(args.gr0),
        *(["--gr0b", str(args.gr0b)] if args.gr0b else []),
        "--campaign", str(args.campaign), "--analyzer", str(args.analyzer), "--design", str(args.design),
        "--r12-analysis", str(args.r12_analysis), "--r12-analysis-sha256", args.r12_analysis_sha256,
        "--served-model", args.served_model,
        "--channel-contract", args.channel_contract, "--channel-contract-sha256", args.channel_contract_sha256,
        "--out", str(args.out),
    ])
    # Re-label the artifacts under the R14 identity and attach GR0f, so no file in the R14
    # tree carries another campaign's name.
    for suffix in ("json", "md"):
        src = args.out / f"E30_R13_OUTCOME_ROLLUP_V1.{suffix}"
        if src.is_file():
            dst = args.out / f"E30_R14_OUTCOME_ROLLUP_V1.{suffix}"
            if suffix == "json":
                payload = json.loads(src.read_text())
                payload["schema_version"] = SCHEMA
                payload["design"] = DESIGN_ID
                payload.setdefault("gates", {})["GR0f"] = gr0f
                payload.setdefault("inputs", {})["e30_r13_analysis_sha256"] = r13_sha
                payload["interface_binding"] = registered
                dst.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            else:
                text = src.read_text().replace("E30-R13", "E30-R14", 1)
                text += ("\n\n## GR0f INTERFACE_HOMOGENEITY\n\n"
                         f"**{gr0f['status']}** — {gr0f['envelopes_with_an_interface_receipt']}/"
                         f"{gr0f['envelopes_expected']} envelopes carry an interface receipt; "
                         f"interface ids {gr0f['interface_id_counts']}; sha256s {gr0f['interface_sha256_counts']}; "
                         f"presentation policies {gr0f['presentation_policy_counts']}; mentioned files truncated "
                         f"{gr0f['mentioned_files_truncated_total']}; offenders {gr0f['offender_count']}.\n")
                dst.write_text(text)
            src.unlink()
    return rc


if __name__ == "__main__":
    sys.exit(main())
