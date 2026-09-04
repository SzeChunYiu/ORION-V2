from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MOD=ROOT/'research'/'machine-epistemics-theory'/'meg_frontier_f2_multiscale_exact.py'
spec=importlib.util.spec_from_file_location('meg_frontier_f2_multiscale_exact',MOD)
m=importlib.util.module_from_spec(spec); assert spec.loader; sys.modules[spec.name]=m; spec.loader.exec_module(m)


def base_fixture():
    F=((0,1),(2,3))
    P=[[m.Fraction(1,2),0,m.Fraction(1,2),0],[0,m.Fraction(1,2),0,m.Fraction(1,2)],[m.Fraction(1,4),0,m.Fraction(3,4),0],[0,m.Fraction(1,4),0,m.Fraction(3,4)]]
    return F,P


def test_parent_lumpability_exactly_commutes_for_registered_witness():
    r=m.check_meg09()
    assert r['lumpable']==1
    assert r['pushforward_fixed_point_exact']==1
    assert r['full_certificate_no_alarm']==1
    assert r['registered_revocation_states']==2
    assert r['terminal']=='PARENT_LUMPABILITY_SUFFICIENT__KSO_ADDS_WARRANT_AND_ANSWER_MEASURABILITY'


def test_nonlumpable_cross_fibre_transport_is_rejected():
    F,P=base_fixture()
    bad=[row[:] for row in P]
    bad[1]=[0,m.Fraction(3,4),0,m.Fraction(1,4)]
    assert not m.strong_lumpable(bad,F)


def test_warrant_and_answer_measurability_are_independent_gates():
    F,P=base_fixture(); family=('none','rev')
    Ps={r:P for r in family}
    live_good={'none':[m.LIVE,m.LIVE,m.DEAD,m.DEAD],'rev':[m.DEAD,m.DEAD,m.LIVE,m.LIVE]}
    ans_good={'none':['A','A','B','B'],'rev':['C','C','D','D']}
    assert m.validate_multiscale_certificate(Ps,live_good,ans_good,F,family)=='CERTIFIED'
    live_bad=dict(live_good); live_bad['rev']=[m.LIVE,m.DEAD,m.LIVE,m.LIVE]
    assert m.validate_multiscale_certificate(Ps,live_bad,ans_good,F,family)=='REFINE_REQUIRED_WARRANT_NONMEASURABLE'
    ans_bad=dict(ans_good); ans_bad['rev']=['C','X','D','D']
    assert m.validate_multiscale_certificate(Ps,live_good,ans_bad,F,family)=='REFINE_REQUIRED_ANSWER_NONFACTORING'


def test_registered_revocation_family_cannot_be_silently_truncated():
    F,P=base_fixture(); family=('none','rev')
    live={'none':[m.LIVE,m.LIVE,m.DEAD,m.DEAD],'rev':[m.DEAD,m.DEAD,m.LIVE,m.LIVE]}
    ans={'none':['A','A','B','B'],'rev':['C','C','D','D']}
    assert m.validate_multiscale_certificate({'none':P},live,ans,F,family)=='CANNOT_CHECK_MISSING_REGISTERED_STATE'


def test_cli_preserves_parent_sufficiency_and_non_novelty():
    p=subprocess.run([sys.executable,str(MOD)],capture_output=True,text=True,check=False)
    assert p.returncode==0,p.stdout+p.stderr
    d=json.loads(p.stdout); assert d['status']=='PASS'
    assert d['result']['answer_nonfactoring_refine_required']==1
    assert d['result']['missing_registered_state_cannot_check']==1
    assert d['result']['GENERAL_NOVELTY']=='NOT_ESTABLISHED'
