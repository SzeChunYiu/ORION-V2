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


def test_parent_lumpability_exactly_commutes_for_registered_witness():
    r=m.check_meg09()
    assert r['lumpable']==1
    assert r['pushforward_fixed_point_exact']==1
    assert r['terminal']=='PARENT_LUMPABILITY_SUFFICIENT__KSO_ADDS_WARRANT_AND_ANSWER_MEASURABILITY'


def test_nonlumpable_cross_fibre_transport_is_rejected():
    F=((0,1),(2,3))
    P=[[m.Fraction(1,2),0,m.Fraction(1,2),0],[0,m.Fraction(3,4),0,m.Fraction(1,4)],[m.Fraction(1,4),0,m.Fraction(3,4),0],[0,m.Fraction(1,4),0,m.Fraction(3,4)]]
    assert not m.strong_lumpable(P,F)


def test_warrant_measurability_is_independent_gate():
    F=((0,1),(2,3))
    assert m.measurable(F,[m.LIVE,m.LIVE,m.DEAD,m.DEAD])
    assert not m.measurable(F,[m.LIVE,m.DEAD,m.DEAD,m.DEAD])


def test_cli_preserves_parent_sufficiency_and_non_novelty():
    p=subprocess.run([sys.executable,str(MOD)],capture_output=True,text=True,check=False)
    assert p.returncode==0,p.stdout+p.stderr
    d=json.loads(p.stdout); assert d['status']=='PASS'
    assert d['result']['GENERAL_NOVELTY']=='NOT_ESTABLISHED'
