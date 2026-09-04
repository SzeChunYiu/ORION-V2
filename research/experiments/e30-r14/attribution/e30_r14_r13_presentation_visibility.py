"""Attribution: did the model's failing patch target code it was never shown?
Replicates scripts/orion_claude_arms._context() truncation exactly (120000 total / 30000 per file,
priority = mentioned-in-baseline < test < other, then size, then path). Read-only."""
import json,glob,collections,re,os
C="/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r13-channelcontract-core4-rep3-20260903-427bfc90"
WS=C+"/prepared/solver_public"
diag=json.load(open("/tmp/r13_anchor_diag_v2.json"))
files=sorted(glob.glob(C+"/run/confirmatory-r*/responses/*/*.json"))
def snapshot_map(task, baseline_json):
    ws=WS+"/"+task
    cands=[]
    for dp,dn,fs in os.walk(ws):
        for fn in fs:
            if fn.endswith(".py"):
                p=os.path.join(dp,fn); rel=os.path.relpath(p,ws)
                parts=rel.split("/")
                if ".git" in parts or any(x in {"venv",".venv","site-packages"} for x in parts): continue
                cands.append((p,rel))
    def priority(pr):
        p,rel=pr; name=os.path.basename(p)
        mentioned = rel in baseline_json or name in baseline_json
        is_test=bool(re.search(r"(^|/)(tests?|test_[^/]*)($|/)", rel))
        try: size=os.path.getsize(p)
        except OSError: size=10**12
        return (0 if mentioned else 1 if is_test else 2, size, rel)
    remaining=120000; per_file=30000; seen={}
    for p,rel in sorted(cands,key=priority):
        if remaining<=0: break
        try: content=open(p,encoding="utf-8",errors="replace").read()
        except OSError: continue
        content=content[:min(per_file,remaining)]
        seen[rel]=len(content); remaining-=len(content)
    return seen
cache={}
res=collections.Counter(); per_arm=collections.defaultdict(collections.Counter); per_cls=collections.defaultdict(collections.Counter)
req_cache={}
for f in files:
    d=json.load(open(f)); pe=d["patch_emission_receipt"]; s=pe["emission_status"]; arm=d["arm_id"]; task=d["task_id"]
    rep=f.split("/")[-4]
    rq=json.load(open(f"{C}/run/{rep}/requests/{arm}/{task}.json"))
    baseline=json.dumps(rq["task"].get("baseline_observation",{}),sort_keys=True)
    if task not in cache: cache[task]=snapshot_map(task,baseline)
    seen=cache[task]
    content=d["proposed_patch_or_artifact"]["content"]
    # target files and declared starts from the model's own patch text
    targets=[]; cur=None
    for line in content.splitlines():
        m=re.match(r"^diff --git a/(.+) b/(.+)$",line) or re.match(r"^\+\+\+ b/(.+)$",line)
        if m: cur=m.group(1) if m.re.pattern.startswith("^diff") else m.group(1); continue
        h=re.match(r"^@@ -(\d+)",line)
        if h and cur: targets.append((cur,int(h.group(1))))
    vis=[]
    for path,start in targets:
        fp=os.path.join(WS,task,path)
        if not os.path.exists(fp): vis.append("PATH_MISSING"); continue
        chars_seen=seen.get(path,0)
        if chars_seen==0: vis.append("FILE_NOT_SHOWN"); continue
        lines=open(fp,encoding="utf-8",errors="replace").read().splitlines(keepends=True)
        off=sum(len(x) for x in lines[:max(0,start-1)])
        fsize=sum(len(x) for x in lines)
        if chars_seen>=fsize: vis.append("FULLY_SHOWN")
        elif off<chars_seen: vis.append("SHOWN_REGION_OF_TRUNCATED_FILE")
        else: vis.append("BEYOND_TRUNCATION")
    if not targets: v="NO_NUMBERED_HUNKS"
    elif all(x=="FULLY_SHOWN" for x in vis): v="ALL_TARGETS_FULLY_SHOWN"
    elif any(x in("BEYOND_TRUNCATION","FILE_NOT_SHOWN") for x in vis): v="SOME_TARGET_UNSEEN"
    else: v="TARGETS_IN_SHOWN_REGION_OF_TRUNCATED_FILE"
    res[(s,v)]+=1; per_arm[arm][v]+=1
# join with anchor classes via the detail list is per-hunk; instead recompute env class quickly from diag per_arm? not keyed by file. So print status x visibility.
print("STATUS x VISIBILITY")
for k,c in sorted(res.items()): print(c,k)
print("PER ARM"); [print(a,dict(c)) for a,c in per_arm.items()]
# how often is the target file fully shown at all, over all 480?
tot=collections.Counter(v for (s,v),c in res.items() for _ in range(c)); print("TOTAL",dict(tot))
