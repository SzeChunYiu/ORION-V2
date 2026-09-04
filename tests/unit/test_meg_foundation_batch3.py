from __future__ import annotations
import importlib.util, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MOD=ROOT/'research'/'machine-epistemics-theory'/'meg_foundation_batch3_exact.py'
spec=importlib.util.spec_from_file_location('meg_foundation_batch3_exact',MOD); m=importlib.util.module_from_spec(spec); assert spec.loader; sys.modules[spec.name]=m; spec.loader.exec_module(m)

def test_meg05():
    r=m.check_meg05(); assert r['ten_speakers_world_truth']==0 and r['majority_mutant_caught']==1

def test_meg10():
    r=m.check_meg10(); assert r['profiles']==20 and r['static_leq_trace_checks']>0 and r['trace_vs_static_strict_witness']==1

def test_meg11():
    r=m.check_meg11(); assert r['status_vectors']==4**len(m.STAGES) and r['ignore_cannot_check_mutant_caught']==1

def test_meg12_13():
    r=m.check_meg12_13(); assert r['agreement_without_global_uniqueness']==1 and r['contradiction_preserved']==1

def test_meg15():
    r=m.check_meg15(); assert r['registered_observation_eliminates_soundly']==1 and r['feedback_only_warrant_unchanged']==1

def test_meg19():
    r=m.check_meg19(); assert r['factor_change_need_not_change_summary_counterexample']==1 and r['uncertified_equivalence_cannot_check']==1

def test_meg21():
    r=m.check_meg21(); assert r['registered_old_query_fixed_point_preserved']==1 and r['nonconservative_leak_mutant_caught']==1

def test_meg28():
    r=m.check_meg28(); assert r['rollback_active_state_exact']==1 and r['proposal_self_adoption_refused']==1

def test_meg33():
    r=m.check_meg33(); assert r['lower_only_never_dead_checks']>0 and r['upper_only_never_live_checks']>0

def test_cli_and_authority():
    p=subprocess.run([sys.executable,str(MOD)],capture_output=True,text=True); assert p.returncode==0,p.stdout+p.stderr
    d=json.loads(p.stdout); assert d['status']=='PASS' and d['result']['GENERAL_NOVELTY']=='NOT_ESTABLISHED'

def test_cannot_check_exit(monkeypatch):
    monkeypatch.setattr(m,'run_all',lambda:(_ for _ in ()).throw(m.CannotCheck('fixture'))); assert m.main()==2
