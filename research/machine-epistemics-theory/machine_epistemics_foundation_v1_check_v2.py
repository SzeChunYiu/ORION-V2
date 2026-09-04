#!/usr/bin/env python3
"""Foundation V1 exact/hostile checker. 0=PASS, 1=FAIL, 2=CANNOT_CHECK. stdlib only."""
from __future__ import annotations
import argparse, hashlib, itertools, json
from fractions import Fraction
from pathlib import Path

LIVE,DEAD,UNKNOWN,CONTRADICTED='LIVE','DEAD','UNKNOWN','CONTRADICTED'
SETTLED={'PROVED','ADOPTED','PARENT_OWNED'}
NOAUTH={'OPEN','CANNOT_CHECK','PROPOSED_PENDING_PR'}
STATUSES=SETTLED|NOAUTH|{'FINITE_CALIBRATION'}
MAIN317='d756c086edc46ad4e5e682f69730b72c1dc26a4c'
BATCH317={1,4,6,8,18,22,26,29,30,31,35}
class CannotCheck(RuntimeError): pass

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def behavior_identity(**kw):
    names=('implementation','model','configuration','runtime','checker','calibration','assumptions','scope','epoch')
    if set(kw)!=set(names) or any(not str(kw[n]).strip() for n in names): raise CannotCheck('incomplete BehaviorIdentityV1')
    return {n:str(kw[n]) for n in names}

def certificate_reusable(bound,current):
    return bound==digest(current)

def check_meg02_identity():
    b=behavior_identity(implementation='i',model='m',configuration='c',runtime='r',checker='k',calibration='z',assumptions='exchangeable',scope='S',epoch='E')
    cert={'behavior':digest(b),'guarantee':'MARGINAL_COVERAGE','error':[1,20]}
    truth=UNKNOWN
    action='AUTHORIZED_RISK_BOUNDED' if Fraction(*cert['error'])<=Fraction(1,20) else 'NOT_AUTHORIZED'
    assert truth==UNKNOWN and action=='AUTHORIZED_RISK_BOUNDED'
    mutant_truth=LIVE if Fraction(*cert['error'])<=Fraction(1,20) else UNKNOWN
    assert mutant_truth==LIVE and truth!=mutant_truth
    strict='AUTHORIZED' if Fraction(*cert['error'])<=Fraction(1,100) else 'NOT_AUTHORIZED_RISK_BUDGET'
    assert strict=='NOT_AUTHORIZED_RISK_BUDGET'
    caught=0
    for n in b:
        x=dict(b); x[n]+=':drift'
        assert not certificate_reusable(cert['behavior'],x); caught+=1
    try:
        x=dict(b); x['configuration']=''; behavior_identity(**x)
    except CannotCheck: missing=1
    else: raise AssertionError('missing identity accepted')
    return {'truth':truth,'action':action,'score_to_truth_mutant':1,'drift_fields':caught,'missing_identity_cannot_check':missing}

# Antichain/nogood finite core.
def ac(xs):
    ys={frozenset(x) for x in xs}; out=[]
    for x in sorted(ys,key=lambda s:(len(s),tuple(sorted(s)))):
        if not any(y<=x for y in out): out.append(x)
    return tuple(out)
ZERO=tuple(); ONE=(frozenset(),)
def plus(p,q): return ac(list(p)+list(q))
def times(p,q): return ZERO if not p or not q else ac(a|b for a in p for b in q)
def filt(p,n): return ac(w for w in p if not any(z<=w for z in n))
def ntimes(p,q,n): return filt(times(filt(p,n),filt(q,n)),n)
def all_profiles():
    u=('a','b','c'); subs=[frozenset(s) for r in range(4) for s in itertools.combinations(u,r)]; out=set()
    for mask in range(1<<len(subs)): out.add(ac(subs[i] for i in range(len(subs)) if mask>>i&1))
    return list(out)
def alive(p,R=frozenset()): return any(not(w&R) for w in p)
def istat(I,R,n):
    L,U=I; lf,uf=filt(L,n),filt(U,n)
    if alive(lf,R): return LIVE
    if not alive(uf,R) and alive(U,R): return CONTRADICTED
    if not alive(uf,R): return DEAD
    return UNKNOWN
def sep(A,B,n):
    au,bu=filt(A[1],n),filt(B[1],n)
    return all(not any(z<=(x|y) for z in n) for x in au for y in bu)
def kand(a,b):
    if DEAD in (a,b): return DEAD
    if a==b==LIVE: return LIVE
    return UNKNOWN

def check_meg16():
    P=all_profiles(); N=[ac([{x}]) for x in 'abc']+[ac([x]) for x in ({'a','b'},{'a','c'},{'b','c'},{'a','b','c'})]
    pc=tc=ass=cc=0
    for n in N:
      for p in P:
       for q in P:
        assert filt(plus(p,q),n)==filt(plus(filt(p,n),filt(q,n)),n); pc+=1
        assert filt(times(p,q),n)==ntimes(p,q,n); tc+=1
      basis=[ZERO,ONE,ac([{'a'}]),ac([{'b'}]),ac([{'c'}]),ac([{'a'},{'b'}]),ac([{'a','b'}])]
      for p in basis:
       for q in basis:
        for r in basis:
         assert ntimes(ntimes(p,q,n),r,n)==ntimes(p,ntimes(q,r,n),n); ass+=1
    n,p,q=ac([{'a','b'}]),ac([{'a'}]),ac([{'b'}])
    assert times(filt(p,n),filt(q,n))==ac([{'a','b'}]) and ntimes(p,q,n)==ZERO
    A,B=(p,p),(q,q); assert istat(A,frozenset(),n)==istat(B,frozenset(),n)==LIVE and not sep(A,B,n)
    basisI=[(ONE,ONE),(ZERO,ZERO),(ZERO,ONE),(ac([{'a'}]),ac([{'a'}])),(ZERO,ac([{'a'}])),(ac([{'b'}]),ac([{'b'}]))]
    for n in N:
     for A in basisI:
      for B in basisI:
       if not sep(A,B,n): continue
       for R in map(frozenset,[(),('a',),('b',),('c',),('a','b')]):
        sa,sb=istat(A,R,n),istat(B,R,n)
        if CONTRADICTED in (sa,sb): continue
        C=(ntimes(A[0],B[0],n),ntimes(A[1],B[1],n)); sc=istat(C,R,n)
        assert sc!=CONTRADICTED and sc==kand(sa,sb); cc+=1
    return {'profiles':len(P),'choice':pc,'product':tc,'associativity':ass,'conditional_kleene':cc,'prefilter_mutant':1,'cross_nogood':CONTRADICTED,'atlas_unconditional_refuted':1}

def validate_registry(d):
    need={'foundation_id','version','status','authority_snapshot','status_vocabulary','authority_rule','primitives','atlas','absorption','non_consequences'}
    if need-set(d): raise CannotCheck('registry missing top-level fields')
    if set(d['status_vocabulary'])!=STATUSES: raise AssertionError('status vocabulary drift')
    if d['status'] not in {'FROZEN_CANDIDATE','FROZEN'}: raise AssertionError('bad foundation status')
    ids=[]
    for r in d['primitives']:
      fields={'id','name','semantics','status','parent','scope','resources','terminal','source','reopen','authority'}
      if fields-set(r): raise CannotCheck(f"{r.get('id')} missing fields")
      ids.append(r['id']); s=r['status']; a=r['authority']
      if s not in STATUSES: raise AssertionError('unknown primitive status')
      if s in NOAUTH and a!='NONE': raise AssertionError(f"{r['id']} mints authority")
      if s in SETTLED and a!='PARITY': raise AssertionError(f"{r['id']} bypasses parity")
      if s=='FINITE_CALIBRATION' and a!='SCOPED_PARITY': raise AssertionError('finite result unscoped')
      if s in SETTLED and not r['source']: raise CannotCheck('settled source missing')
    if len(ids)!=20 or len(ids)!=len(set(ids)): raise AssertionError('primitive registry count/duplicate defect')
    expected={f'MEG-{i:02d}' for i in range(1,37)}
    if set(d['atlas'])!=expected: raise AssertionError('MEG atlas not total')
    for k,r in d['atlas'].items():
      if set(r)!={'status','terminal','source','authority'}: raise CannotCheck(f'{k} malformed')
      s=r['status']; a=r['authority']
      if s in NOAUTH and a!='NONE': raise AssertionError(f'{k} mints authority')
      if s in SETTLED and a!='PARITY': raise AssertionError(f'{k} bypasses parity')
    for i in BATCH317:
      r=d['atlas'][f'MEG-{i:02d}']
      if r['status']!='PROVED' or MAIN317 not in r['source'] or '#317' not in r['source']: raise AssertionError('merged #317 binding drift')
    if any(r['status']=='PROPOSED_PENDING_PR' for r in d['atlas'].values()): raise AssertionError('unexpected pending row after #317 merge')
    req=set(d['absorption']['required']); must={'v2_issue_or_study','theorem_or_rule','terminal','source_commit','scope_and_resource_assumptions','parity_test'}
    if not must<=req: raise AssertionError('absorption bindings incomplete')
    if not NOAUTH<=set(d['absorption']['blocked']): raise AssertionError('absorption blocklist incomplete')
    return {'primitives':20,'atlas':36,'merged_pr317':11,'pending':0,'bindings':len(req)}

def registry_mutants(d):
    import copy
    caught=0
    x=copy.deepcopy(d); x['primitives'].append(dict(x['primitives'][0]))
    try: validate_registry(x)
    except AssertionError: caught+=1
    x=copy.deepcopy(d); next(r for r in x['primitives'] if r['status']=='OPEN')['authority']='PARITY'
    try: validate_registry(x)
    except AssertionError: caught+=1
    x=copy.deepcopy(d); x['atlas']['MEG-01']['source']='b0c0337#317'
    try: validate_registry(x)
    except AssertionError: caught+=1
    x=copy.deepcopy(d); x['atlas'].pop('MEG-36')
    try: validate_registry(x)
    except AssertionError: caught+=1
    x=copy.deepcopy(d); x['absorption']['blocked']=['OPEN']
    try: validate_registry(x)
    except AssertionError: caught+=1
    if caught!=5: raise AssertionError(f'mutants caught {caught}/5')
    return caught

def run(registry=None):
    out={'meg02_identity':check_meg02_identity(),'meg16':check_meg16()}
    if registry:
      try: d=json.loads(Path(registry).read_text())
      except Exception as e: raise CannotCheck(str(e))
      out['registry']=validate_registry(d); out['registry_mutants']=registry_mutants(d)
    return out

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('--registry'); ns=ap.parse_args(argv)
    try: print(json.dumps(run(ns.registry),sort_keys=True,indent=2)); return 0
    except CannotCheck as e: print(json.dumps({'status':'CANNOT_CHECK','reason':str(e)})); return 2
    except Exception as e: print(json.dumps({'status':'FAIL','reason':f'{type(e).__name__}: {e}'})); return 1
if __name__=='__main__': raise SystemExit(main())
