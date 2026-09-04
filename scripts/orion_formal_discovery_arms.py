#!/usr/bin/env python3
"""Gold-blind Codex executable for fresh FM/FG formal-discovery tasks."""
from __future__ import annotations
import argparse, json, os, subprocess, tempfile, time
from pathlib import Path
from typing import Any

def schema() -> dict[str,Any]:
    return {
      "type":"object",
      "properties":{
        "answer":{"type":"string"},
        "reasoning_summary":{"type":"string"},
        "falsifier":{"type":"string"},
      },
      "required":["answer","reasoning_summary","falsifier"],
      "additionalProperties":False,
    }

class UnregisteredArm(RuntimeError):
    """Arm id is not in ARM_PROCEDURE_CLASS. Never fall back to a generic default."""


class UnspecifiedArmProcedure(RuntimeError):
    """Arm id is registered by a campaign plan but has no distinct procedure designed.

    Running it would execute a *generic* instruction under a *specific* arm label -
    a contrast that could not exist. Designing the missing procedure is the owning
    lane's design act, not this executable's; the only honest behaviour here is to
    refuse loudly so the arm surfaces as a named failure rather than as a plausible
    row in a results table.
    """


# Procedure text, keyed by procedure class. Text is byte-identical to the
# pre-2026-09-04 substring-dispatch implementation so the frozen FM/FG R2 lane
# remains reproducible for every arm id it actually executed.
PROCEDURE_TEXT = {
    "DIRECT": "Solve directly using only the task representation; do not invent extra structure unless logically required.",
    "FIXED": "Use only simple fixed/general textbook heuristics; do not perform open-ended representation invention.",
    "PARENT_GENERIC": "Use the strongest applicable native formal parent method first; prefer an exact parent solution and refuse unnecessary new formalism.",
    "F2_STATIC": "Use the existing integrated ORION concepts but do not perform open-ended transfer discovery, conceptual revision, or formalism genesis.",
    "F2_FULL": "Use full ORION formal discovery: inspect structural relations, invariants, counterexamples, parent sufficiency, and only invent/revise representation when simpler routes fail.",
}

# Exact-id registry. `None` = registered by a plan, no distinct procedure designed.
#
# Two arms sharing a procedure class are a COLLAPSE: they are the same arm wearing
# two labels, and any contrast between them is uninterpretable. Collapses are not
# fatal at dispatch time (that gate would be unsatisfiable on the current design),
# but scripts/audit_formal_campaign_coverage.py reports them under its own exit
# code so they can never be silent.
ARM_PROCEDURE_CLASS = {
    # --- direct / no-transfer floors ---
    "TARGET_ONLY_DIRECT": "DIRECT",
    "CURRENT_FORMALISM_ONLY": "DIRECT",
    # --- fixed-lesson controls ---
    "FIXED_LESSON_INJECTION": "FIXED",
    "FIXED_FORMALISM_LESSON_INJECTION": "FIXED",
    # --- parent baselines (ALL currently collapsed onto PARENT_GENERIC) ---
    "STRONGEST_DOMAIN_FORMAL_PARENT": "PARENT_GENERIC",
    "F0_PARENT_FEDERATION": "PARENT_GENERIC",
    "F0_FORMAL_PARENT_FEDERATION": "PARENT_GENERIC",
    "STRUCTURE_MAPPING_PARENT": "PARENT_GENERIC",
    "ANTI_UNIFICATION_OR_MDL_PARENT_WHEN_APPLICABLE": "PARENT_GENERIC",
    "FCA_PARENT_WHEN_APPLICABLE": "PARENT_GENERIC",
    # --- integrated static arms ---
    "F2_STATIC_NO_TRANSFER_DISCOVERY": "F2_STATIC",
    "F2_STATIC_NO_FORMALISM_GENESIS": "F2_STATIC",
    # --- integrated full arms ---
    "F2_TRANSFER_DISCOVERY_FULL": "F2_FULL",
    "F2_FORMALISM_GENESIS_FULL": "F2_FULL",
    # --- registered, procedure NOT designed: refuse loudly, do not invent ---
    "SEMANTIC_RETRIEVAL": None,
    "SEMANTIC_RETRIEVAL_OF_EXISTING_FORMALISM": None,
    "LOCAL_PATCH_OR_EXTRA_VARIABLE": None,
    # --- legacy ids executed by the FM/FG R2 campaign; registered by NO study.
    #     Retained solely so the frozen lane stays reproducible. ---
    "F2_STATIC_NO_FORMAL_DISCOVERY": "F2_STATIC",
    "F2_FORMAL_DISCOVERY_FULL": "F2_FULL",
}

LEGACY_UNREGISTERED_ARMS = frozenset({
    "F2_STATIC_NO_FORMAL_DISCOVERY",
    "F2_FORMAL_DISCOVERY_FULL",
})


def arm_instruction(arm: str) -> str:
    """Exact-id lookup. Raises rather than silently returning a generic default.

    The previous implementation dispatched by substring and ended in an
    unconditional ``return "Use the smallest justified formal method."``, so an
    unknown or undesigned arm id produced a plausible response under a generic
    procedure with no signal anywhere that the named arm had never been built.
    """
    if arm not in ARM_PROCEDURE_CLASS:
        raise UnregisteredArm(
            f"arm id {arm!r} has no registered procedure; "
            "add it to ARM_PROCEDURE_CLASS or fix the dispatching plan"
        )
    procedure = ARM_PROCEDURE_CLASS[arm]
    if procedure is None:
        raise UnspecifiedArmProcedure(
            f"arm id {arm!r} is registered but its procedure has not been designed; "
            "refusing to execute it under a generic instruction"
        )
    return PROCEDURE_TEXT[procedure]


def collapse_classes(arms):
    """Map procedure class -> sorted arm ids, for arms sharing one instruction."""
    groups: dict[str, list[str]] = {}
    for arm in arms:
        cls = ARM_PROCEDURE_CLASS.get(arm, "__UNREGISTERED__")
        groups.setdefault("__UNSPECIFIED__" if cls is None else cls, []).append(arm)
    return {key: sorted(value) for key, value in sorted(groups.items())}


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

def prompt(req:dict[str,Any])->str:
    task=req["task"]
    return f"""You are a protected gold-blind formal-reasoning experimental arm.
No network retrieval. The private oracle is unavailable. Solve only from the public task.
ARM: {req['arm_id']}
ARM PROCEDURE: {arm_instruction(str(req['arm_id']))}

PUBLIC TASK:
{json.dumps(task,indent=2,sort_keys=True)}

{answer_encoding_instruction(req['task'].get('answer_contract', {}))}
Do not claim scientific truth, a new mathematical theory, ORION superiority, field status, or publication readiness.
"""

def execute(req:dict[str,Any])->dict[str,Any]:
    start=time.time()
    with tempfile.TemporaryDirectory(prefix="orion-formal-") as td:
        td=Path(td); sp=td/"schema.json"; op=td/"out.json"; sp.write_text(json.dumps(schema()))
        cmd=[os.environ.get("ORION_CODEX_BIN","codex"),"exec","--ephemeral","--ignore-user-config","--ignore-rules",
             "--skip-git-repo-check","--sandbox","read-only","--model",os.environ.get("ORION_CODEX_MODEL","gpt-5.6-terra"),
             "--output-schema",str(sp),"--output-last-message",str(op),prompt(req)]
        cp=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False,
                          timeout=int(os.environ.get("ORION_FORMAL_TIMEOUT","1800")))
        if cp.returncode!=0 or not op.exists(): raise RuntimeError(f"Codex failed ({cp.returncode}): {cp.stdout[-2000:]}")
        data=json.loads(op.read_text())
    contract=req["task"].get("answer_contract",{})
    raw=data["answer"]
    answer=json.loads(raw) if isinstance(raw,str) else raw
    if not isinstance(answer,dict): raise ValueError("decoded answer is not an object")
    if set(answer)!=set(contract): raise ValueError(f"answer keys {sorted(answer)} do not match contract {sorted(contract)}")
    return {
      "schema_version":"orion.v2.formal-discovery-response.v1",
      "task_id":req["task_id"],"arm_id":req["arm_id"],"status":"COMPLETED_PROPOSAL_ONLY",
      "answer":answer,"reasoning_summary":data["reasoning_summary"],"falsifier":data["falsifier"],
      "resource_receipt":{"model_calls":1,"wall_time_seconds":time.time()-start,
                          "executor":"codex-cli","model":os.environ.get("ORION_CODEX_MODEL","gpt-5.6-terra")},
      "scientific_truth_authorized":False,"new_mathematical_theory_authorized":False,
      "publication_readiness_authorized":False,
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument("--request",type=Path,required=True); p.add_argument("--response",type=Path,required=True); a=p.parse_args()
    req=json.loads(a.request.read_text())
    # An arm that cannot be CONSTRUCTED is a different failure from a model call that
    # did not land. Give each its own status so a downstream evaluator can never file
    # "this arm was never built" under "the backend was flaky".
    def _fail(status, exc, falsifier):
        return {"schema_version":"orion.v2.formal-discovery-response.v1","task_id":req.get("task_id"),"arm_id":req.get("arm_id"),
                "status":status,"answer":None,"reasoning_summary":str(exc),
                "falsifier":falsifier,"resource_receipt":{"model_calls":0},
                "scientific_truth_authorized":False,"new_mathematical_theory_authorized":False,"publication_readiness_authorized":False}
    try: out=execute(req)
    except UnregisteredArm as exc:
        out=_fail("EXECUTION_FAILED_ARM_UNREGISTERED", exc,
                  "register the arm id or correct the dispatching plan, then rerun")
    except UnspecifiedArmProcedure as exc:
        out=_fail("EXECUTION_FAILED_ARM_PROCEDURE_UNSPECIFIED", exc,
                  "the owning lane must design this arm's procedure before it can be dispatched")
    except Exception as exc:
        out=_fail("EXECUTION_FAILED_MODEL_RESPONSE", exc,
                  "repair execution binding and rerun under a new identity")
    a.response.parent.mkdir(parents=True,exist_ok=True); a.response.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    return 0
if __name__=="__main__": raise SystemExit(main())
