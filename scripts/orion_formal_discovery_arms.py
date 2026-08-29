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
        "answer":{"type":"object","additionalProperties":True},
        "reasoning_summary":{"type":"string"},
        "falsifier":{"type":"string"},
      },
      "required":["answer","reasoning_summary","falsifier"],
      "additionalProperties":False,
    }

def arm_instruction(arm:str)->str:
    if arm in {"TARGET_ONLY_DIRECT","CURRENT_FORMALISM_ONLY"}:
        return "Solve directly using only the task representation; do not invent extra structure unless logically required."
    if "FIXED" in arm:
        return "Use only simple fixed/general textbook heuristics; do not perform open-ended representation invention."
    if "PARENT" in arm or arm.startswith("F0"):
        return "Use the strongest applicable native formal parent method first; prefer an exact parent solution and refuse unnecessary new formalism."
    if "STATIC" in arm:
        return "Use the existing integrated ORION concepts but do not perform open-ended transfer discovery, conceptual revision, or formalism genesis."
    if "FULL" in arm or arm.startswith("F2"):
        return "Use full ORION formal discovery: inspect structural relations, invariants, counterexamples, parent sufficiency, and only invent/revise representation when simpler routes fail."
    return "Use the smallest justified formal method."

def prompt(req:dict[str,Any])->str:
    task=req["task"]
    return f"""You are a protected gold-blind formal-reasoning experimental arm.
No network retrieval. The private oracle is unavailable. Solve only from the public task.
ARM: {req['arm_id']}
ARM PROCEDURE: {arm_instruction(str(req['arm_id']))}

PUBLIC TASK:
{json.dumps(task,indent=2,sort_keys=True)}

Return JSON matching the schema. `answer` MUST contain exactly the keys described by `answer_contract`, with concrete values (not type names). Do not add extra answer keys.
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
    answer=data["answer"]
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
    try: out=execute(req)
    except Exception as exc:
        out={"schema_version":"orion.v2.formal-discovery-response.v1","task_id":req.get("task_id"),"arm_id":req.get("arm_id"),
             "status":"EXECUTION_FAILED_MODEL_RESPONSE","answer":None,"reasoning_summary":str(exc),
             "falsifier":"repair execution binding and rerun under a new identity","resource_receipt":{"model_calls":0},
             "scientific_truth_authorized":False,"new_mathematical_theory_authorized":False,"publication_readiness_authorized":False}
    a.response.parent.mkdir(parents=True,exist_ok=True); a.response.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    return 0
if __name__=="__main__": raise SystemExit(main())
