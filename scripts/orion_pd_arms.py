#!/usr/bin/env python3
"""Dependence-evidence campaign arms: deterministic offline parents + codex model arms.

One process per request. Offline arms are pure functions of the PUBLIC task (they
never read the private oracle); their decision rates are constructed calibration
ceilings, not empirical discoveries. Model arms run codex exec --ephemeral with the
same failure envelope as orion_formal_discovery_arms.py (model_calls: 0 on failure).
"""
from __future__ import annotations
import argparse, json, os, subprocess, tempfile, time
from pathlib import Path
from typing import Any

OFFLINE_ARMS = {
    "CURRENT_INDEPENDENT_COUNTING",
    "PROVENANCE_TRACKING",
    "STANDARD_DEPENDENCE_META_ANALYSIS",
    "ARGUMENT_ACCEPTABILITY",
    "SIMPLE_DIRECT_CONTROL",
}

INCONCLUSIVE = "INCONCLUSIVE_INSUFFICIENT_INDEPENDENT_SUPPORT"


# ---------------------------------------------------------------------------
# deterministic offline parents (public task -> protected decision)
# ---------------------------------------------------------------------------

def _accept_s1(count: int) -> str:
    return "ACCEPT_H" if count >= 3 else INCONCLUSIVE


def _clusters(items: list[dict[str, Any]]) -> int:
    """Union-find over shared lineage roots and declared overlap (meta-analysis pooling)."""
    parent = {item["item_id"]: item["item_id"] for item in items}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for item in items:
        for other in items:
            if item is other:
                continue
            shared_root = item["lineage_root"] == other["lineage_root"]
            declared = other["item_id"] in (item.get("declared_overlap") or [])
            if shared_root or declared:
                parent[find(item["item_id"])] = find(other["item_id"])
    return len({find(item["item_id"]) for item in items})


def _step_support_cycle(steps: list[dict[str, Any]]) -> bool:
    edges: dict[str, list[str]] = {}
    for step in steps:
        for source in step["from"]:
            edges.setdefault(source, []).append(step["id"])
    seen: dict[str, int] = {}

    def visit(node: str) -> bool:
        if seen.get(node) == 1:
            return True
        if seen.get(node) == 2:
            return False
        seen[node] = 1
        if any(visit(nxt) for nxt in edges.get(node, [])):
            return True
        seen[node] = 2
        return False

    return any(visit(step["id"]) for step in steps)


def offline_answer(arm: str, task: dict[str, Any]) -> dict[str, Any]:
    study = str(task["study_id"])
    if study.startswith("PD-S1"):
        items = task["items"]
        if arm == "CURRENT_INDEPENDENT_COUNTING" or arm == "ARGUMENT_ACCEPTABILITY":
            count = len(items)
        elif arm == "PROVENANCE_TRACKING":
            count = len({item["lineage_root"] for item in items})
        elif arm == "STANDARD_DEPENDENCE_META_ANALYSIS":
            count = _clusters(items)
        elif arm == "SIMPLE_DIRECT_CONTROL":
            count = len({item["source_type"] for item in items})
        else:
            raise ValueError(f"arm {arm} has no offline implementation for {study}")
        return {"decision": _accept_s1(count), "independent_support_family_count": count}
    if study.startswith("PD-S2"):
        if arm == "ARGUMENT_ACCEPTABILITY":
            verdict = "DEFECT_CIRCULAR" if _step_support_cycle(task["steps"]) else "SUPPORTED"
        elif arm == "CURRENT_INDEPENDENT_COUNTING":
            verdict = "SUPPORTED" if len(task["evidence"]) >= 3 else "CANNOT_CHECK_TEST_INADEQUATE"
        elif arm == "PROVENANCE_TRACKING":
            verdict = "SUPPORTED" if len({e["lineage_root"] for e in task["evidence"]}) >= 3 else "CANNOT_CHECK_TEST_INADEQUATE"
        elif arm == "STANDARD_DEPENDENCE_META_ANALYSIS":
            verdict = "SUPPORTED" if _clusters(task["evidence"]) >= 3 else "CANNOT_CHECK_TEST_INADEQUATE"
        elif arm == "SIMPLE_DIRECT_CONTROL":
            verdict = "SUPPORTED" if len({e["source_type"] for e in task["evidence"]}) >= 3 else "CANNOT_CHECK_TEST_INADEQUATE"
        else:
            raise ValueError(f"arm {arm} has no offline implementation for {study}")
        return {"verdict": verdict}
    if study.startswith("PD-S3"):
        if "objections" in task:
            return {"objection_outcomes": {obj["objection_id"]: "LOGGED_WITHOUT_CHANGE" for obj in task["objections"]}}
        target = task["failure_event"]["target_item_id"]
        failed_root = next(item["lineage_root"] for item in task["items"] if item["item_id"] == target)
        reopened, preserved = [], []
        for claim in task["claims"]:
            cites_failed_item = target in claim["cited_item_ids"]
            cites_failed_root = failed_root in [
                item["lineage_root"] for item in task["items"] if item["item_id"] in claim["cited_item_ids"]
            ]
            if arm in {"CURRENT_INDEPENDENT_COUNTING", "ARGUMENT_ACCEPTABILITY"} and cites_failed_item:
                reopened.append(claim["claim_id"])
            elif arm in {"PROVENANCE_TRACKING", "STANDARD_DEPENDENCE_META_ANALYSIS"} and cites_failed_root:
                reopened.append(claim["claim_id"])
            else:
                preserved.append(claim["claim_id"])
        return {"reopened_claim_ids": sorted(reopened), "preserved_claim_ids": sorted(preserved)}
    if study.startswith("PD-S4"):
        if task["task_kind"] == "AUTHORITY":
            if arm == "SIMPLE_DIRECT_CONTROL":
                decision = "REPORT_ONLY"
            elif arm == "ARGUMENT_ACCEPTABILITY":
                decision = "CONDITIONAL_ACTION_AUTHORIZED"
            else:
                decision = "CONDITIONAL_ACTION_AUTHORIZED" if len(task["evidence_items"]) >= 3 else "REPORT_ONLY"
            return {"authority_decision": decision, "response_status": "NOT_APPLICABLE"}
        return {"authority_decision": "NOT_APPLICABLE", "response_status": "REMAINS_VALID"}
    raise ValueError(f"unknown study {study}")


# ---------------------------------------------------------------------------
# model arms
# ---------------------------------------------------------------------------

def schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "reasoning_summary": {"type": "string"},
            "falsifier": {"type": "string"},
        },
        "required": ["answer", "reasoning_summary", "falsifier"],
        "additionalProperties": False,
    }


def arm_instruction(arm: str) -> str:
    if arm == "STRONGEST_ASSURANCE_FEDERATION":
        return ("Configure the strongest assurance parent products together: provenance tracking, "
                "argumentation labelling, a dependence graph over declared correlations, and severe "
                "testing. Use only these parent capabilities; refuse any further integration concept.")
    if arm == "P_D_FULL":
        return ("Use full dependence-aware evaluation: group evidence into support families, infer "
                "dependence from shared latent assumptions/calibrations stated in method text (not just "
                "declared lineage), assess argument adequacy, test/oracle sensitivity to the registered "
                "error class, authority boundaries, and post-intervention response.")
    if arm == "P_D_MINUS_DEPENDENCE":
        return ("Use the full P-D pipeline EXCEPT dependence modelling: treat every evidence item as "
                "independent; do not infer shared latent assumptions, correlated failure modes or "
                "assumption-level dependence between items.")
    if arm == "ROBUSTNESS_TRIANGULATION_PARENT":
        return ("Use only robustness triangulation as the parent method: count genuinely differing "
                "methods/raters/instruments and decide from that alone.")
    if arm == "PERFORMATIVE_SECURITY_PARENT":
        return ("Use only static assurance plus published-response modelling: decide whether the static "
                "pass survives the post-intervention environment (optimization, adversary, policy response).")
    return "Use the smallest justified assurance method."


def answer_encoding_instruction(contract: dict) -> str:
    ex = {}
    for k, shape in (contract or {}).items():
        if isinstance(shape, list):
            ex[k] = ["<concrete-value>"]
        elif isinstance(shape, dict):
            ex[k] = {kk: "<concrete-value>" for kk in shape}
        elif isinstance(shape, bool):
            ex[k] = "<true-or-false>"
        elif isinstance(shape, int):
            ex[k] = "<concrete-integer>"
        elif isinstance(shape, float):
            ex[k] = "<concrete-number>"
        else:
            ex[k] = "<concrete-value>"
    import json as _json
    return (
        "Return JSON matching the schema. `answer` MUST be a single JSON-encoded string. "
        "Parsing that string must yield an object with EXACTLY the keys of `answer_contract`, "
        "each mapped to a concrete value of the described shape (never the placeholder itself). "
        "Do not add extra answer keys. "
        "`answer_contract` = " + _json.dumps(contract or {}, sort_keys=True) + "; "
        "so `answer` must be the string " + _json.dumps(_json.dumps(ex)) + " "
        "with every '<concrete-value>'/'<concrete-integer>'/'<concrete-number>'/'<true-or-false>' "
        "replaced by the real concrete value(s)."
    )

def prompt(req: dict[str, Any]) -> str:
    task = req["task"]
    return f"""You are a protected gold-blind evidence-evaluation experimental arm.
No network retrieval. The private oracle is unavailable. Solve only from the public task.
ARM: {req['arm_id']}
ARM PROCEDURE: {arm_instruction(str(req['arm_id']))}

PUBLIC TASK:
{json.dumps(task, indent=2, sort_keys=True)}

{answer_encoding_instruction(req['task'].get('answer_contract', {}))}
Registered decision rules in the task are binding: apply them exactly.
Do not claim scientific truth, legitimate authority, field status, or publication readiness.
"""


def execute_model(req: dict[str, Any]) -> dict[str, Any]:
    start = time.time()
    with tempfile.TemporaryDirectory(prefix="orion-pd-") as td:
        td = Path(td); sp = td / "schema.json"; op = td / "out.json"
        sp.write_text(json.dumps(schema()))
        cmd = [os.environ.get("ORION_CODEX_BIN", "codex"), "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
               "--skip-git-repo-check", "--sandbox", "read-only", "--model", os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra"),
               "--output-schema", str(sp), "--output-last-message", str(op), prompt(req)]
        cp = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
                            timeout=int(os.environ.get("ORION_FORMAL_TIMEOUT", "1800")))
        if cp.returncode != 0 or not op.exists():
            raise RuntimeError(f"Codex failed ({cp.returncode}): {cp.stdout[-2000:]}")
        data = json.loads(op.read_text())
    contract = req["task"].get("answer_contract", {})
    raw = data["answer"]
    answer = json.loads(raw) if isinstance(raw, str) else raw
    if not isinstance(answer, dict): raise ValueError("decoded answer is not an object")
    if set(answer) != set(contract):
        raise ValueError(f"answer keys {sorted(answer)} do not match contract {sorted(contract)}")
    return {
        "schema_version": "orion.v2.dependence-evidence-response.v1",
        "task_id": req["task_id"], "arm_id": req["arm_id"], "status": "COMPLETED_PROPOSAL_ONLY",
        "answer": answer, "reasoning_summary": data["reasoning_summary"], "falsifier": data["falsifier"],
        "resource_receipt": {"model_calls": 1, "wall_time_seconds": time.time() - start,
                             "executor": "codex-cli", "model": os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra")},
        "scientific_truth_authorized": False, "legitimate_authority_authorized": False,
        "publication_readiness_authorized": False,
    }


def execute(req: dict[str, Any]) -> dict[str, Any]:
    arm = str(req["arm_id"])
    if arm in OFFLINE_ARMS:
        return {
            "schema_version": "orion.v2.dependence-evidence-response.v1",
            "task_id": req["task_id"], "arm_id": arm, "status": "COMPLETED_PROPOSAL_ONLY",
            "answer": offline_answer(arm, req["task"]), "reasoning_summary": "deterministic offline parent",
            "falsifier": "offline parent is a constructed calibration ceiling, not an empirical arm",
            "resource_receipt": {"model_calls": 0, "executor": "deterministic-offline"},
            "scientific_truth_authorized": False, "legitimate_authority_authorized": False,
            "publication_readiness_authorized": False,
        }
    if os.environ.get("ORION_PD_OFFLINE_ONLY", "") == "1":
        raise RuntimeError("model arm suppressed by ORION_PD_OFFLINE_ONLY=1 (offline smoke mode)")
    return execute_model(req)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--request", type=Path, required=True)
    p.add_argument("--response", type=Path, required=True)
    a = p.parse_args()
    req = json.loads(a.request.read_text())
    try:
        out = execute(req)
    except Exception as exc:
        out = {"schema_version": "orion.v2.dependence-evidence-response.v1", "task_id": req.get("task_id"),
               "arm_id": req.get("arm_id"), "status": "EXECUTION_FAILED_MODEL_RESPONSE", "answer": None,
               "reasoning_summary": str(exc), "falsifier": "repair execution binding and rerun under a new identity",
               "resource_receipt": {"model_calls": 0},
               "scientific_truth_authorized": False, "legitimate_authority_authorized": False,
               "publication_readiness_authorized": False}
    a.response.parent.mkdir(parents=True, exist_ok=True)
    a.response.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
