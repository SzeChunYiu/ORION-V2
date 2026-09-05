from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
CHECKER=ROOT/'research/machine-epistemics-theory/machine_epistemics_foundation_v1_check_v2.py'
REG=ROOT/'research/machine-epistemics-theory/MACHINE_EPISTEMICS_FOUNDATION_V1.json'
@pytest.fixture(scope='module')
def m():
 spec=importlib.util.spec_from_file_location('mef_v1',CHECKER); x=importlib.util.module_from_spec(spec); sys.modules[spec.name]=x; spec.loader.exec_module(x); return x
def test_truth_action_and_identity(m):
 r=m.check_meg02_identity(); assert r['truth']=='UNKNOWN' and r['action']=='AUTHORIZED_RISK_BOUNDED' and r['drift_fields']==9 and r['score_to_truth_mutant']==1
def test_corrected_nogoods(m):
 r=m.check_meg16(); assert r['profiles']==20 and r['choice']==2800 and r['product']==2800 and r['associativity']==2401 and r['conditional_kleene']==1147 and r['cross_nogood']=='CONTRADICTED' and r['atlas_unconditional_refuted']==1
def test_registry(m):
 d=json.loads(REG.read_text()); assert m.validate_registry(d)=={'primitives':20,'atlas':36,'merged_pr317':11,'pending':0,'bindings':6}; assert m.registry_mutants(d)==5
def test_cli(m,monkeypatch):
 assert m.main(['--registry',str(REG)])==0
 monkeypatch.setattr(m,'run',lambda *a,**k: (_ for _ in ()).throw(AssertionError('x'))); assert m.main([])==1
 monkeypatch.setattr(m,'run',lambda *a,**k: (_ for _ in ()).throw(m.CannotCheck('x'))); assert m.main([])==2
