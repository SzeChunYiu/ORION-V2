import json,glob,collections,re,sys
C="/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e30-r13-channelcontract-core4-rep3-20260903-427bfc90"
files=sorted(glob.glob(C+"/run/confirmatory-r*/responses/*/*.json"))
print("responses",len(files))
d=json.load(open(files[0])); print("top keys",list(d.keys()))
ppa=d.get("proposed_patch_or_artifact",{}); print("ppa keys",list(ppa.keys()) if isinstance(ppa,dict) else type(ppa))
st=collections.Counter(); errk=collections.Counter(); norm=collections.Counter(); hdr=collections.Counter(); rawclean=collections.Counter()
per_arm=collections.defaultdict(collections.Counter)
examples={}
for f in files:
    d=json.load(open(f))
    pe=d.get("patch_emission_receipt") or (d.get("proposed_patch_or_artifact") or {}).get("patch_emission_receipt")
    arm=f.split("/")[-2]
    if not pe: st["NO_RECEIPT"]+=1; per_arm[arm]["NO_RECEIPT"]+=1; continue
    s=pe["emission_status"]; st[s]+=1; per_arm[arm][s]+=1
    hdr[pe.get("extracted_was_header_exact")]+=1; rawclean[pe.get("extracted_was_apply_clean")]+=1
    for n in pe.get("normalizations",[]): norm[n.split(":")[0][:60]]+=1
    e=pe.get("emitted_apply_check_error","") or ""
    for line in e.splitlines():
        line=re.sub(r'\d+','N',line); line=re.sub(r'\S+\.py','FILE.py',line)
        errk[line.strip()[:120]]+=1
    if s not in examples and s!="APPLY_CLEAN_BY_CONSTRUCTION": examples[s]=(f,e[:1500])
print("emission_status",dict(st))
for a,c in per_arm.items(): print(a,dict(c))
print("header_exact",dict(hdr)); print("extracted_apply_clean",dict(rawclean))
print("normalizations",norm.most_common(15))
print("error lines",errk.most_common(25))
for s,(f,e) in examples.items(): print("=== EXAMPLE",s,f); print(e)
# evaluations
ev=sorted(glob.glob(C+"/run/confirmatory-r*/evaluations/*/*.json"))
print("evaluations",len(ev))
d=json.load(open(ev[0])); print("eval keys",list(d.keys()))
ek=collections.Counter(); ap=collections.Counter()
for f in ev:
    d=json.load(open(f))
    s=json.dumps(d)
    for k in ("patch_applied","apply_status","patch_apply","none_reason","outcome_reason"):
        if k in d: ek[(k,str(d[k])[:60])]+=1
print(ek.most_common(20))
