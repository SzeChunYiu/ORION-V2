"""Read-only diagnostic over the archived E30-R13 envelopes: what would an anchored
(search/replace) edit interface recover? Computes apply-ability ONLY; runs no test,
scores no endpoint, writes nothing into the campaign tree."""
import json,glob,collections,re,subprocess,os,sys,tempfile
C="/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r13-channelcontract-core4-rep3-20260903-427bfc90"
WS=C+"/prepared/solver_public"
files=sorted(glob.glob(C+"/run/confirmatory-r*/responses/*/*.json"))
HUNK=re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")
HUNK_ANY=re.compile(r"^@@")
def lenient_parse(text):
    """Return list of (path, is_new, hunks[(old_start|None, body_lines)]) and a list of syntax notes."""
    lines=text.splitlines(); notes=set(); files=[]; cur=None; i=0
    def newfile(p): 
        nonlocal cur
        cur={"path":p,"new":False,"hunks":[]}; files.append(cur)
    while i<len(lines):
        l=lines[i]
        m=re.match(r"^diff --git a/(.+) b/(.+)$",l)
        if m:
            if cur and cur["path"]==m.group(1) and not cur["hunks"]: notes.add("duplicate_diff_git_header")
            else: newfile(m.group(1))
            i+=1; continue
        if l.startswith("--- "):
            p=l[4:].strip()
            if p in("/dev/null","a/dev/null","dev/null"):
                notes.add("new_file_dev_null")
                if cur is None: newfile(None)
                cur["new"]=True
            else:
                p=p.removeprefix("a/")
                if cur is None or cur["path"]!=p:
                    if cur is None or cur["hunks"] or cur["path"] is not None: newfile(p)
                    else: cur["path"]=p
            i+=1; continue
        if l.startswith("+++ "):
            p=l[4:].strip().removeprefix("b/")
            if cur is not None and cur["path"] is None: cur["path"]=p
            i+=1; continue
        if l.startswith(("index ","new file mode","deleted file mode","old mode","new mode","similarity","rename ")):
            notes.add("git_metadata_line"); i+=1; continue
        if HUNK_ANY.match(l):
            hm=HUNK.match(l)
            if not hm: notes.add("numberless_hunk_header")
            old_start=int(hm.group(1)) if hm else None
            body=[]; i+=1
            while i<len(lines) and not HUNK_ANY.match(lines[i]) and not lines[i].startswith(("diff --git ","--- ","+++ ")):
                b=lines[i]
                if b=="" : b=" "
                if b[0] in " +-\\": body.append(b)
                else:
                    notes.add("unprefixed_body_line"); body.append(" "+b)  # treat as context (model dropped the leading space)
                i+=1
            if cur is None: newfile(None); notes.add("hunk_before_any_header")
            cur["hunks"].append((old_start,body)); continue
        notes.add("stray_line"); i+=1
    return files,notes
def norm(s): return re.sub(r"\s+"," ",s.strip())
def find_block(filelines, block, mode):
    n=len(block)
    if n==0: return []
    if mode=="exact": key=lambda x:x
    elif mode=="rstrip": key=lambda x:x.rstrip()
    else: key=norm
    tgt=[key(b) for b in block]
    hits=[]
    for s in range(len(filelines)-n+1):
        if all(key(filelines[s+j])==tgt[j] for j in range(n)): hits.append(s)
    return hits
def rebuild_hunk(filelines, start, body_old, body_new, ctx=3):
    """Produce canonical hunk text with fresh counts from the file at `start` (0-based)."""
    old_count=len(body_old); new_count=len(body_new)
    return start, old_count, new_count
DETAIL=[]
res=collections.Counter(); per_arm=collections.defaultdict(collections.Counter); notes_c=collections.Counter()
examples=collections.defaultdict(list)
git_confirm=collections.Counter()
for f in files:
    d=json.load(open(f)); pe=d["patch_emission_receipt"]; s=pe["emission_status"]; arm=d["arm_id"]; task=d["task_id"]
    if s=="APPLY_CLEAN_BY_CONSTRUCTION": res["ALREADY_CLEAN"]+=1; per_arm[arm]["ALREADY_CLEAN"]+=1; continue
    content=d["proposed_patch_or_artifact"]["content"]
    fl,notes=lenient_parse(content)
    for n in notes: notes_c[n]+=1
    ws=os.path.join(WS,task)
    verdicts=[]; rebuilt=[]
    for fe in fl:
        p=fe["path"]
        if p is None: verdicts.append("NO_PATH"); continue
        fp=os.path.join(ws,p)
        if fe["new"] or not os.path.exists(fp):
            if fe["new"]:
                verdicts.append("NEW_FILE")
                body=[b for h in fe["hunks"] for b in h[1]]
                rebuilt.append((p,True,[(0,[],[b[1:] for b in body if b.startswith("+")])]))
            else: verdicts.append("PATH_NOT_IN_WORKSPACE")
            continue
        filelines=open(fp,encoding="utf-8",errors="replace").read().splitlines()
        hunks_out=[]
        for old_start,body in fe["hunks"]:
            old=[b[1:] for b in body if b[0] in " -"]; new=[b[1:] for b in body if b[0] in " +"]
            removed=[b[1:] for b in body if b[0]=="-"]
            if "..." in "".join(x for x in old if x.strip().startswith("#") or "..." in x): notes_c["ellipsis_in_context"]+=1
            v=None
            for mode in ("exact","rstrip","ws"):
                hits=find_block(filelines,old,mode)
                if len(hits)==1: v=("ANCHOR_"+mode.upper(),hits[0]); break
                if len(hits)>1:
                    # disambiguate by declared start
                    if old_start is not None:
                        best=min(hits,key=lambda h:abs(h-(old_start-1)))
                        v=("ANCHOR_"+mode.upper()+"_DISAMBIG_BY_LINE",best)
                    else: v=("AMBIGUOUS",None)
                    break
            if v is None:
                if not old: v=("PURE_INSERTION_NO_CONTEXT", (old_start-1) if old_start else None)
                elif removed:
                    for mode in ("exact","rstrip","ws"):
                        hits=find_block(filelines,removed,mode)
                        if len(hits)==1: v=("REMOVED_LINES_ONLY_"+mode.upper(),hits[0]); break
                        if len(hits)>1: v=("REMOVED_LINES_AMBIGUOUS",None); break
                    if v is None: v=("CONTEXT_AND_REMOVED_NOT_IN_FILE",None)
                else: v=("CONTEXT_NOT_IN_FILE",None)
            verdicts.append(v[0])
            hunks_out.append((v, old, new, removed, body))
            if v[0] in ("CONTEXT_NOT_IN_FILE","CONTEXT_AND_REMOVED_NOT_IN_FILE"):
                import difflib
                per_line=[]
                for ol in old[:4]:
                    cm=difflib.get_close_matches(ol, filelines, n=1, cutoff=0.6)
                    per_line.append({"old":ol[:100],"nearest":(cm[0][:100] if cm else None),"exact_in_file": ol in filelines,"ws_in_file": norm(ol) in set(map(norm,filelines))})
                DETAIL.append({"file":f.split("/")[-2:],"task":task,"path":p,"declared_start":old_start,"n_old":len(old),"n_removed":len(removed),"frac_old_lines_in_file_ws": (sum(1 for ol in old if norm(ol) in set(map(norm,filelines)))/max(1,len(old))),"lines":per_line})
        rebuilt.append((p,False,hunks_out))
    # classify envelope
    bad=[v for v in verdicts if v in("NO_PATH","PATH_NOT_IN_WORKSPACE","AMBIGUOUS","REMOVED_LINES_AMBIGUOUS","CONTEXT_AND_REMOVED_NOT_IN_FILE","CONTEXT_NOT_IN_FILE")]
    if not verdicts: cls="NO_HUNKS_PARSED"
    elif bad: cls="UNRECOVERABLE:"+sorted(set(bad))[0]
    elif any(v.startswith("REMOVED_LINES_ONLY") for v in verdicts): cls="RECOVERABLE_REMOVED_ONLY"
    elif any(v=="PURE_INSERTION_NO_CONTEXT" for v in verdicts): cls="RECOVERABLE_LINE_NUMBER_ONLY"
    elif all(v in("NEW_FILE",) or v.startswith("ANCHOR") for v in verdicts): cls="RECOVERABLE_ANCHORED"
    else: cls="OTHER:"+",".join(sorted(set(verdicts)))
    res[cls]+=1; per_arm[arm][cls]+=1
    if len(examples[cls])<2: examples[cls].append((f.split("/")[-3:], sorted(notes), verdicts[:6], content.splitlines()[:8]))
    # confirm anchored recoveries by actually building a diff and git apply --check (anchored + removed-only only)
    if cls in("RECOVERABLE_ANCHORED","RECOVERABLE_REMOVED_ONLY"):
        parts=[]
        ok=True
        for p,isnew,hunks in rebuilt:
            if isnew:
                new=hunks[0][2]
                parts.append(f"diff --git a/{p} b/{p}\nnew file mode 100644\n--- /dev/null\n+++ b/{p}\n@@ -0,0 +1,{len(new)} @@\n"+"".join("+"+x+"\n" for x in new))
                continue
            fp=os.path.join(ws,p); filelines=open(fp,encoding="utf-8",errors="replace").read().splitlines()
            # apply hunks bottom-up on a copy to produce new file, then diff with git
            edits=[]
            for (v,start),old,new,removed,body in hunks:
                if v.startswith("ANCHOR"): edits.append((start,len(old),new))
                elif v.startswith("REMOVED_LINES_ONLY"): edits.append((start,len(removed),[x for x in new if x not in old or x in removed] if False else [b[1:] for b in body if b[0]=="+"]))
            if not edits: ok=False; break
            edits.sort(reverse=True)
            newlines=list(filelines)
            for start,cnt,new in edits: newlines[start:start+cnt]=new
            with tempfile.NamedTemporaryFile("w",suffix=".py",delete=False,encoding="utf-8") as t:
                t.write("\n".join(newlines)+"\n"); tmp=t.name
            r=subprocess.run(["git","diff","--no-index","--","{}".format(fp),tmp],capture_output=True,text=True)
            os.unlink(tmp)
            dtext=r.stdout
            dtext=re.sub(r"^diff --git .*$",f"diff --git a/{p} b/{p}",dtext,flags=re.M)
            dtext=re.sub(r"^--- .*$",f"--- a/{p}",dtext,count=1,flags=re.M)
            dtext=re.sub(r"^\+\+\+ .*$",f"+++ b/{p}",dtext,count=1,flags=re.M)
            parts.append(dtext)
        if ok and parts:
            patch="".join(parts)
            r=subprocess.run(["git","apply","--check","--whitespace=nowarn","-"],cwd=ws,input=patch,text=True,capture_output=True)
            git_confirm[(cls, "GIT_APPLY_CHECK_PASS" if r.returncode==0 else "GIT_APPLY_CHECK_FAIL")]+=1
            if r.returncode!=0 and git_confirm[(cls,"GIT_APPLY_CHECK_FAIL")]<=2: print("CONFIRM-FAIL",f, r.stderr[:300])
        else: git_confirm[(cls,"NOT_REBUILT")]+=1
# planted control: a fabricated block must not anchor
ctrl_ws=os.path.join(WS,sorted(os.listdir(WS))[0]); anyfile=next(os.path.join(dp,fn) for dp,dn,fs in os.walk(ctrl_ws) for fn in fs if fn.endswith(".py"))
fll=open(anyfile,encoding="utf-8",errors="replace").read().splitlines()
print("CONTROL fabricated block anchors:",find_block(fll,["this line was fabricated by the diagnostic 0xDEADBEEF"],"ws"),"| real block anchors:",len(find_block(fll,fll[10:13],"exact")))
print("RESULT CLASSES",json.dumps(res,indent=1))
json.dump({"classes":res,"per_arm":{a:dict(c) for a,c in per_arm.items()},"syntax_notes":dict(notes_c),"git_confirm":{str(k):v for k,v in git_confirm.items()},"detail":DETAIL},open("/tmp/r13_anchor_diag_v2.json","w"),indent=1)
# summarize detail
fr=[d["frac_old_lines_in_file_ws"] for d in DETAIL]
import statistics
print("DETAIL n",len(DETAIL),"frac_old_lines_present median",statistics.median(fr) if fr else None, "all-absent",sum(1 for x in fr if x==0),"all-present",sum(1 for x in fr if x==1.0))
for a,c in per_arm.items(): print(a,dict(c))
print("SYNTAX NOTES",dict(notes_c))
print("GIT CONFIRM",{str(k):v for k,v in git_confirm.items()})
for cls,ex in examples.items():
    for e in ex: print("EX",cls,e[0],e[1],e[2]); print("   "+"\n   ".join(x[:140] for x in e[3]))
