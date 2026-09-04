import json,glob,collections,re,subprocess,os,sys
C="/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r13-channelcontract-core4-rep3-20260903-427bfc90"
files=sorted(glob.glob(C+"/run/confirmatory-r*/responses/*/*.json"))
ws_root=C+"/prepared/solver_public"
print(os.listdir(ws_root)[:5])
tm=json.load(open(C+"/TASKMAP.json")); print("taskmap keys", list(tm.keys())[:5] if isinstance(tm,dict) else type(tm))
def ws_for(task):
    for cand in (os.path.join(ws_root,task),):
        if os.path.isdir(cand): return cand
    return None
shown=collections.Counter()
outcomes=collections.Counter()
for f in files:
    d=json.load(open(f)); pe=d["patch_emission_receipt"]; s=pe["emission_status"]
    if s=="APPLY_CLEAN_BY_CONSTRUCTION": continue
    content=d["proposed_patch_or_artifact"]["content"]
    task=d["task_id"]; ws=ws_for(task)
    # classify raw text shape
    lines=content.splitlines()
    first=[l for l in lines[:6]]
    key=(s, pe["canonicalizer_rejection_reasons"][0].split(":")[0][:40] if pe["canonicalizer_rejection_reasons"] else "-", (pe["emitted_apply_check_error"] or "").splitlines()[0][:40] if pe["emitted_apply_check_error"] else "-")
    # try levers in workspace
    lev={}
    if ws:
        for name,args in (("plain",[]),("recount",["--recount"]),("recount_C1",["--recount","-C1"]),("recount_C0",["--recount","-C0"]),("recount_ignorews",["--recount","--ignore-whitespace"]),("recount_C1_ignorews",["--recount","-C1","--ignore-whitespace"]),("unidiff_zero",["--recount","--unidiff-zero"])):
            r=subprocess.run(["git","apply","--check","--whitespace=nowarn",*args,"-"],cwd=ws,input=content,text=True,capture_output=True)
            lev[name]=r.returncode==0
    outcomes[(s,)+tuple(sorted(k for k,v in lev.items() if v))]+=1
    if shown[key]<1:
        shown[key]+=1
        print("="*100); print(f, "| task",task,"| ws",bool(ws)); print("KEY",key); print("levers",lev)
        print("--- content head ---"); print("\n".join(l[:160] for l in lines[:14]))
        print("--- err ---"); print((pe["emitted_apply_check_error"] or "")[:400]); print("normalizations",pe["normalizations"][:4])
print("\nOUTCOMES (status, levers that pass):")
for k,v in outcomes.most_common(): print(v,k)
