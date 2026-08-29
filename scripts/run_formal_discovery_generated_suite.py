#!/usr/bin/env python3
"""Fresh generated formal-discovery suite for FM10-FM60 and FG10-FG80.

This harness creates exact/mechanically scored calibration/benchmark tasks only.
Private oracle answers are absent from child/model processes during dispatch.
It does not grant scientific truth, F2 superiority, or a new mathematical theory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKDIR = ROOT / ".orion-formal-discovery-suite"
STUDIES = ("FM10","FM20","FM30","FM40","FM50","FM60","FG10","FG20","FG30","FG40","FG50","FG60","FG70","FG80")
DEFAULT_ARMS = (
    "TARGET_ONLY_DIRECT",
    "STRONGEST_DOMAIN_FORMAL_PARENT",
    "F0_PARENT_FEDERATION",
    "F2_STATIC_NO_FORMAL_DISCOVERY",
    "F2_FORMAL_DISCOVERY_FULL",
)

class SuiteError(RuntimeError):
    pass

def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def answer_shape(value: Any) -> Any:
    if isinstance(value, dict): return {k: answer_shape(v) for k,v in value.items()}
    if isinstance(value, list): return ["array-item"]
    if isinstance(value, bool): return "boolean"
    if isinstance(value, (int,float)): return "number"
    return "string"

def token(rng: random.Random, prefix: str) -> str:
    return prefix + "_" + "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(6))

def gen_fm10(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    n = rng.randint(3, 5)
    types = [f"T{i}" for i in range(n)]
    donor = [token(rng, "D") for _ in range(n)]
    target = [token(rng, "Q") for _ in range(n)]
    perm = list(range(n)); rng.shuffle(perm)
    mapping = {donor[i]: target[perm[i]] for i in range(n)}
    donor_nodes = [{"id": donor[i], "type": types[i]} for i in range(n)]
    target_nodes = [{"id": target[perm[i]], "type": types[i]} for i in range(n)]
    facts = [["R", donor[i], donor[i+1]] for i in range(n-1)]
    target_facts = [["R", mapping[a], mapping[b]] for _, a, b in facts]
    if rng.random() < .3:
        target_facts[-1] = ["R", target_facts[-1][2], target_facts[-1][1]]
        answer = {"status":"NO_VALID_MAPPING"}
    else:
        answer = {"status":"VALID_MAPPING","node_map":mapping}
    public = {"study_id":"FM10","donor":{"nodes":donor_nodes,"facts":facts},
              "target":{"nodes":target_nodes,"facts":target_facts},
              "task":"Return the unique type-preserving relation-preserving map, or NO_VALID_MAPPING."}
    return public, answer

def gen_fm20(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    width = rng.randint(3, 6)
    base = [token(rng, "C") for _ in range(width)]
    varying = sorted(rng.sample(range(width), rng.randint(1, min(2,width))))
    examples=[]
    for _ in range(5):
        row=base.copy()
        for i in varying: row[i]=token(rng,"V")
        examples.append(row)
    pattern=[("?X"+str(i)) if i in varying else base[i] for i in range(width)]
    if rng.random()<.2:
        examples=[[token(rng,"V") for _ in range(width)] for _ in range(5)]
        pattern=["?X"+str(i) for i in range(width)]
    public={"study_id":"FM20","terms":examples,
            "task":"Return the least-general coordinate pattern; constants remain exact and varying positions use ?X<index>."}
    return public, {"pattern":pattern}

def closure(objects, attrs, incidence, seed_attrs):
    extent=[o for o in objects if all((o,a) in incidence for a in seed_attrs)]
    intent=[a for a in attrs if all((o,a) in incidence for o in extent)] if extent else list(attrs)
    extent2=[o for o in objects if all((o,a) in incidence for a in intent)]
    return sorted(extent2), sorted(intent)

def gen_fm30(rng):
    objects=[token(rng,"O") for _ in range(5)]
    attrs=[token(rng,"A") for _ in range(5)]
    incidence=set()
    for o in objects:
        incidence.update((o,a) for a in rng.sample(attrs,rng.randint(1,4)))
    seed=[rng.choice(attrs)]
    ext,intent=closure(objects,attrs,incidence,seed)
    public={"study_id":"FM30","objects":objects,"attributes":attrs,
            "incidence":[list(x) for x in sorted(incidence)],"seed_attributes":seed,
            "task":"Compute exact Formal Concept Analysis closure (extent and intent)."}
    return public,{"extent":ext,"intent":intent}

def gen_fm40(rng):
    states=list(range(6))
    transforms=[[(i,(i+1)%6) for i in states],[(i,(5-i)) for i in states]]
    features={}; invariant_ids=[]
    for j in range(5):
        fid=token(rng,"F")
        if j<2:
            val=rng.randint(0,9); table={str(i):val for i in states}; invariant_ids.append(fid)
        else:
            table={str(i):rng.randint(0,9) for i in states}
            if len(set(table.values()))==1: table["0"] += 1
        features[fid]=table
    public={"study_id":"FM40","states":states,"transformations":transforms,"features":features,
            "task":"Return feature IDs invariant under every registered transformation."}
    return public,{"invariant_feature_ids":sorted(invariant_ids)}

def gen_fm50(rng):
    A,B=token(rng,"A"),token(rng,"B"); X,Y=token(rng,"X"),token(rng,"Y")
    source={"objects":[A,B],"morphisms":[f"id_{A}",f"id_{B}","f"],
            "endpoints":{f"id_{A}":[A,A],f"id_{B}":[B,B],"f":[A,B]},
            "identities":{A:f"id_{A}",B:f"id_{B}"},
            "composition":[[f"id_{A}","f","f"],["f",f"id_{B}","f"]]}
    target={"objects":[X,Y],"morphisms":[f"id_{X}",f"id_{Y}","g"],
            "endpoints":{f"id_{X}":[X,X],f"id_{Y}":[Y,Y],"g":[X,Y]},
            "identities":{X:f"id_{X}",Y:f"id_{Y}"},
            "composition":[[f"id_{X}","g","g"],["g",f"id_{Y}","g"]]}
    valid=rng.random()<.6
    if valid:
        cand={"objects":{A:X,B:Y},"morphisms":{f"id_{A}":f"id_{X}",f"id_{B}":f"id_{Y}","f":"g"}}
        answer={"valid_functor":True,"violation":"NONE"}
    else:
        cand={"objects":{A:Y,B:X},"morphisms":{f"id_{A}":f"id_{Y}",f"id_{B}":f"id_{X}","f":"g"}}
        answer={"valid_functor":False,"violation":"ENDPOINT"}
    public={"study_id":"FM50","source_category":source,"target_category":target,"candidate_functor":cand,
            "task":"Check functor validity. Return valid_functor and first violation class ENDPOINT/IDENTITY/COMPOSITION/NONE."}
    return public,answer

def gen_fm60(rng):
    a,b,c=token(rng,"N"),token(rng,"N"),token(rng,"N")
    facts=[["R",a,b],["R",b,c]]; target=[["R","x","y"],["R","y","z"]]
    mapping={a:"x",b:"y",c:"z"}; mode=rng.choice(["NONE","DIRECTION","MISSING_RELATION","TYPE"])
    node_types={a:"T0",b:"T1",c:"T2"}; target_types={"x":"T0","y":"T1","z":"T2"}
    if mode=="DIRECTION": target[1]=["R","z","y"]
    elif mode=="MISSING_RELATION": target=target[:1]
    elif mode=="TYPE": target_types["z"]="T9"
    public={"study_id":"FM60","donor":{"facts":facts,"types":node_types},
            "target":{"facts":target,"types":target_types},"candidate_map":mapping,
            "task":"Find the first critical obstruction to transfer, or NONE."}
    return public,{"obstruction":mode}

def gen_fg10(rng):
    features=[token(rng,"P") for _ in range(4)]
    necessary=sorted(rng.sample(features,rng.randint(1,2))); cases=[]
    for idx,f in enumerate(necessary):
        values0={x:"0" for x in features}; values1=values0.copy(); values1[f]="1"
        cases.append({"id":f"c{idx}a","signature":["S"],"decision":"A","features":values0})
        cases.append({"id":f"c{idx}b","signature":["S"],"decision":"B","features":values1})
    public={"study_id":"FG10","cases":cases,
            "task":"Return a minimum set of candidate feature IDs that resolves every representational collision."}
    return public,{"minimal_feature_ids":necessary}

def gen_fg20(rng):
    base=["A","B","C"]; observations=[]; outside_count=0
    for _ in range(10):
        x,y=rng.choice(base),rng.choice(base); out=rng.choice(base)
        if rng.random()<.35: out="G"; outside_count+=1
        observations.append([x,y,out])
    decision="GENERALIZE_OBJECT_CLASS" if outside_count>=3 else ("LOCAL_EXCEPTION" if outside_count else "NO_CHANGE")
    public={"study_id":"FG20","current_object_class":base,"operation_observations":observations,
            "decision_rule":"GENERALIZE_OBJECT_CLASS iff >=3 outputs leave the current class; LOCAL_EXCEPTION iff 1-2; else NO_CHANGE.",
            "task":"Classify the minimum justified response to non-closure."}
    return public,{"decision":decision}

def gen_fg30(rng):
    mod=rng.choice([5,7,11]); law=rng.choice(["ADD_MOD","MUL_MOD","XOR"])
    def apply(name,x,y):
        return (x+y)%mod if name=="ADD_MOD" else ((x*y)%mod if name=="MUL_MOD" else x^y)
    examples=[]
    for _ in range(8):
        x,y=rng.randrange(mod),rng.randrange(mod); examples.append([x,y,apply(law,x,y)])
    public={"study_id":"FG30","modulus":mod,"candidate_operation_ids":["ADD_MOD","MUL_MOD","XOR"],"examples":examples,
            "task":"Return the candidate operation law exactly consistent with all observations."}
    return public,{"operation_id":law}

def gen_fg40(rng):
    feature_ids=[token(rng,"Q") for _ in range(5)]; required=sorted(rng.sample(feature_ids,rng.randint(1,2)))
    positives=[]; negatives=[]
    for _ in range(6): positives.append({f:(1 if f in required else rng.randint(0,1)) for f in feature_ids})
    for _ in range(6):
        row={f:rng.randint(0,1) for f in feature_ids}; row[rng.choice(required)]=0; negatives.append(row)
    public={"study_id":"FG40","feature_ids":feature_ids,"positive_models":positives,"negative_countermodels":negatives,
            "task":"Return a minimum conjunction of feature IDs true in every positive model and false in every negative countermodel."}
    return public,{"axiom_feature_ids":required}

def gen_fg50(rng):
    n=4; left=[token(rng,"L") for _ in range(n)]; right=[token(rng,"R") for _ in range(n)]
    perm=list(range(n)); rng.shuffle(perm); map_lr={left[i]:right[perm[i]] for i in range(n)}
    left_edges=[[left[i],left[(i+1)%n]] for i in range(n)]; right_edges=[[map_lr[a],map_lr[b]] for a,b in left_edges]
    equivalent=rng.random()<.65
    if not equivalent: right_edges[-1]=[right_edges[-1][1],right_edges[-1][0]]
    public={"study_id":"FG50","left":{"nodes":left,"edges":left_edges},"right":{"nodes":right,"edges":right_edges},
            "candidate_translation":map_lr,
            "task":"Determine whether the candidate translation is a structure-preserving equivalence on the supplied finite relation."}
    return public,{"equivalent":equivalent}

def gen_fg60(rng):
    old_cases=[{"x":i,"decision":("A" if i%2==0 else "B")} for i in range(8)]; new_cases=[dict(c) for c in old_cases]
    conservative=rng.random()<.7
    if not conservative: new_cases[rng.randrange(len(new_cases))]["decision"]="C"
    new_cases += [{"x":100+i,"decision":"C"} for i in range(3)]
    public={"study_id":"FG60","predecessor_cases":old_cases,"extension_cases":new_cases,
            "task":"Return whether the extension is conservative on every predecessor-valid case."}
    return public,{"conservative":conservative}

def gen_fg70(rng):
    flags={"parent_sufficient":rng.random()<.2,"missing_observation":rng.random()<.2,
           "local_patch_sufficient":rng.random()<.25,"registered_collision":rng.random()<.35}
    if flags["parent_sufficient"]: terminal="PARENT_FORMALISM"
    elif flags["missing_observation"]: terminal="MORE_DATA"
    elif flags["local_patch_sufficient"]: terminal="LOCAL_PATCH"
    elif flags["registered_collision"]: terminal="NEW_FORMALISM_CANDIDATE"
    else: terminal="NO_CHANGE"
    public={"study_id":"FG70","diagnostic_flags":flags,
            "priority_rule":["PARENT_FORMALISM","MORE_DATA","LOCAL_PATCH","NEW_FORMALISM_CANDIDATE","NO_CHANGE"],
            "task":"Choose the minimum justified terminal using the registered priority."}
    return public,{"terminal":terminal}

def gen_fg80(rng):
    feature_ids=[token(rng,"H") for _ in range(4)]; key=rng.choice(feature_ids); demos=[]
    for _ in range(12):
        row={f:rng.randint(0,1) for f in feature_ids}; row["decision"]="YES" if row[key] else "NO"; demos.append(row)
    target={f:rng.randint(0,1) for f in feature_ids}
    public={"study_id":"FG80","demonstrations":demos,"target":target,
            "task":"Infer the single intermediate representation feature explaining every demonstration, then decide the target."}
    return public,{"representation_feature":key,"target_decision":"YES" if target[key] else "NO"}

GENERATORS={"FM10":gen_fm10,"FM20":gen_fm20,"FM30":gen_fm30,"FM40":gen_fm40,"FM50":gen_fm50,"FM60":gen_fm60,
            "FG10":gen_fg10,"FG20":gen_fg20,"FG30":gen_fg30,"FG40":gen_fg40,"FG50":gen_fg50,"FG60":gen_fg60,"FG70":gen_fg70,"FG80":gen_fg80}

def prepare(workdir: Path, studies: list[str], per_study: int, seed: int, arms: list[str], force: bool) -> None:
    if workdir.exists():
        if not force: raise SuiteError(f"workdir exists: {workdir}")
        shutil.rmtree(workdir)
    rng=random.Random(seed); public_tasks=[]; private_answers={}
    for study in studies:
        if study not in GENERATORS: raise SuiteError(f"unsupported study {study}")
        for index in range(per_study):
            trng=random.Random(rng.getrandbits(64)); public,answer=GENERATORS[study](trng); task_id=f"{study.lower()}-{index+1:04d}"
            public["task_id"]=task_id; public["answer_contract"]=answer_shape(answer); public_tasks.append(public); private_answers[task_id]=answer
            for arm in arms:
                write_json(workdir/"requests"/arm/f"{task_id}.json",{
                    "schema_version":"orion.v2.formal-discovery-request.v1","task_id":task_id,"arm_id":arm,"task":public,
                    "scientific_truth_authorized":False,"publication_readiness_authorized":False})
    write_json(workdir/"public_tasks.json",{"schema_version":"orion.v2.formal-discovery-public.v1","tasks":public_tasks})
    write_json(workdir/"private_oracle.json",{"schema_version":"orion.v2.formal-discovery-private.v1","answers":private_answers})
    write_json(workdir/"FROZEN_SUITE.json",{"schema_version":"orion.v2.formal-discovery-freeze.v1","seed":seed,"studies":studies,
        "per_study":per_study,"task_count":len(public_tasks),"arms":arms,"private_oracle_visible_to_solver":False,
        "authority":{"grants_scientific_truth":False,"grants_F2_superiority":False,"grants_new_mathematical_theory":False}})

def command_prefix() -> list[str]:
    override=os.environ.get("ORION_FORMAL_ARM_COMMAND","").strip()
    if override:
        import shlex; return shlex.split(override)
    return [sys.executable,str(ROOT/"scripts/orion_formal_discovery_arms.py")]

def dispatch(workdir: Path, arms: list[str], concurrency: int, overwrite: bool) -> None:
    private=workdir/"private_oracle.json"
    if not private.exists(): raise SuiteError("missing private oracle")
    data=private.read_bytes(); write_json(workdir/"PRIVATE_ORACLE_COMMITMENT.json",{"sha256":digest(data),"private_removed_before_dispatch":True}); private.unlink()
    env=os.environ.copy(); env["ORION_GOLD_ACCESS"]="NONE"; env["ORION_OUTCOME_ACCESS"]="NONE"; jobs=[]
    for arm in arms:
        for req in sorted((workdir/"requests"/arm).glob("*.json")):
            resp=workdir/"responses"/arm/req.name
            if resp.exists() and not overwrite: continue
            jobs.append((arm,req,resp))
    prefix=command_prefix()
    def one(job):
        arm,req,resp=job; resp.parent.mkdir(parents=True,exist_ok=True); t=time.time()
        cp=subprocess.run(prefix+["--request",str(req),"--response",str(resp)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False,
                          timeout=int(os.environ.get("ORION_FORMAL_TIMEOUT","1800")))
        return {"arm":arm,"task":req.stem,"returncode":cp.returncode,"seconds":time.time()-t,"output_tail":cp.stdout[-1000:]}
    rows=[]
    try:
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futures=[ex.submit(one,j) for j in jobs]
            for f in as_completed(futures): rows.append(f.result())
    finally:
        if private.exists(): raise SuiteError("private oracle reappeared during dispatch")
        private.write_bytes(data)
    write_json(workdir/"DISPATCH_RECEIPT.json",{"jobs":rows,"all_returncodes_zero":all(r["returncode"]==0 for r in rows),
        "oracle_restored_hash_match":digest(private.read_bytes())==digest(data)})

def evaluate(workdir: Path, arms: list[str]) -> None:
    answers=read_json(workdir/"private_oracle.json")["answers"]; rows=[]; summary={}
    for arm in arms:
        correct=0; total=0; failures=0
        for task_id, expected in answers.items():
            path=workdir/"responses"/arm/f"{task_id}.json"; total+=1
            if not path.exists(): failures+=1; continue
            try: response=read_json(path); actual=response.get("answer")
            except Exception: failures+=1; continue
            ok=canon(actual)==canon(expected); correct+=int(ok); rows.append({"arm":arm,"task_id":task_id,"correct":ok,"expected":expected,"actual":actual})
        summary[arm]={"correct":correct,"tasks":total,"accuracy":correct/total if total else 0.0,"missing_or_invalid":failures}
    write_json(workdir/"EVALUATION_ROWS.json",rows)
    write_json(workdir/"EVALUATION_SUMMARY.json",{"summary":summary,
      "authority":{"grants_scientific_truth":False,"grants_F2_superiority":False,"grants_new_mathematical_theory":False}})

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    q=sub.add_parser("prepare"); q.add_argument("--workdir",type=Path,default=DEFAULT_WORKDIR); q.add_argument("--studies",default=",".join(STUDIES))
    q.add_argument("--per-study",type=int,default=8); q.add_argument("--seed",type=int,default=20260829); q.add_argument("--arms",default=",".join(DEFAULT_ARMS)); q.add_argument("--force",action="store_true")
    q=sub.add_parser("dispatch"); q.add_argument("--workdir",type=Path,default=DEFAULT_WORKDIR); q.add_argument("--arms",default=",".join(DEFAULT_ARMS)); q.add_argument("--max-concurrency",type=int,default=2); q.add_argument("--overwrite",action="store_true")
    q=sub.add_parser("evaluate"); q.add_argument("--workdir",type=Path,default=DEFAULT_WORKDIR); q.add_argument("--arms",default=",".join(DEFAULT_ARMS))
    a=p.parse_args(); arms=[x for x in a.arms.split(",") if x]
    if a.cmd=="prepare": prepare(a.workdir,[x for x in a.studies.split(",") if x],a.per_study,a.seed,arms,a.force)
    elif a.cmd=="dispatch": dispatch(a.workdir,arms,a.max_concurrency,a.overwrite)
    else: evaluate(a.workdir,arms)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
