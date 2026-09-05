from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import pytest

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
    Prev=[[x if i>=2 and j>=2 else m.Fraction(0) for j,x in enumerate(row)] for i,row in enumerate(P)]
    Ps={'none':P,'rev':Prev}
    live_good={'none':[m.LIVE]*4,'rev':[m.DEAD,m.DEAD,m.LIVE,m.LIVE]}
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


def test_fibre_constant_warrant_cannot_relabel_ungated_navigation():
    F,P=base_fixture()
    assert m.validate_multiscale_certificate({'r':P},{'r':[m.DEAD]*4},{'r':['A']*4},F,('r',)) == 'CANNOT_CHECK_WARRANT_KERNEL_MISMATCH'
    zero=[[0]*4 for _ in range(4)]
    assert m.validate_multiscale_certificate({'r':zero},{'r':[m.DEAD]*4},{'r':['A']*4},F,('r',)) == 'CERTIFIED'


def test_cli_preserves_parent_sufficiency_and_non_novelty():
    p=subprocess.run([sys.executable,str(MOD)],capture_output=True,text=True,check=False)
    assert p.returncode==0,p.stdout+p.stderr
    d=json.loads(p.stdout); assert d['status']=='PASS'
    assert d['result']['answer_nonfactoring_refine_required']==1
    assert d['result']['missing_registered_state_cannot_check']==1
    assert d['result']['GENERAL_NOVELTY']=='NOT_ESTABLISHED'


@pytest.mark.parametrize("blocks", [(), ((), (0,1,2,3)), ((0,1),), ((0,1),(1,2,3)), ((0,1),(2,4)), ((0,True),(2,3))])
def test_malformed_partitions_cannot_prove_lumpability(blocks):
    _, P = base_fixture()
    with pytest.raises(m.CannotCheck):
        m.strong_lumpable(P, blocks)


@pytest.mark.parametrize("kernel", [[], [[1,0]], [[-1,1],[0,1]], [[2,0],[0,1]], [[float("nan"),0],[0,1]], [[0.5,0.5],[0,1]], [[True,0],[0,1]]])
def test_invalid_exact_kernels_are_cannot_check(kernel):
    with pytest.raises(m.CannotCheck):
        m.cemetery_embed(kernel)


def test_all_basis_seeds_commute_but_one_seed_does_not_prove_lumpability():
    F, P = base_fixture()
    Q = m.quotient(P, F)
    for alpha in (m.Fraction(1), m.Fraction(1,2), m.Fraction(1,3)):
        for i in range(4):
            seed = [int(j == i) for j in range(4)]
            assert m.push(m.fixed_point(P, seed, alpha), F) == m.fixed_point(Q, m.push(seed, F), alpha)
    bad = [row[:] for row in P]
    bad[1] = [0,m.Fraction(3,4),0,m.Fraction(1,4)]
    seed = [0,1,0,0]
    assert m.push(m.fixed_point(bad,seed),F) != m.fixed_point(Q,m.push(seed,F))
    # At alpha=1 every kernel just returns the seed: equality gives no lumpability evidence.
    assert m.push(m.fixed_point(bad,seed,m.Fraction(1)),F) == m.fixed_point(Q,m.push(seed,F),m.Fraction(1))


def test_empty_scope_bad_labels_and_dimension_drift_are_cannot_check():
    F, P = base_fixture()
    assert m.validate_multiscale_certificate({}, {}, {}, (), ()) == "CANNOT_CHECK_MALFORMED_REGISTERED_SCOPE"
    assert m.validate_multiscale_certificate({"r":P}, {"r":["MAYBE"]*4}, {"r":["a"]*4}, F, ("r",)) == "CANNOT_CHECK_MALFORMED_REGISTERED_STATE"
    assert m.validate_multiscale_certificate({"r":P}, {"r":[m.LIVE]*3}, {"r":["a"]*4}, F, ("r",)) == "CANNOT_CHECK_MALFORMED_REGISTERED_STATE"


@pytest.mark.parametrize("alpha", [0, -1, 2, True, 0.5])
def test_restart_parameter_must_meet_theorem_hypotheses(alpha):
    _, P = base_fixture()
    with pytest.raises(m.CannotCheck):
        m.fixed_point(P,[1,0,0,0],alpha)


def test_cli_has_distinct_failure_and_cannot_check(monkeypatch, capsys):
    def fail():
        raise AssertionError("planted commutation failure")
    monkeypatch.setattr(m, "check_meg09", fail)
    assert m.main() == 1
    assert json.loads(capsys.readouterr().out)["status"] == "FAIL"
    def cannot():
        raise m.CannotCheck("kernel unavailable")
    monkeypatch.setattr(m, "check_meg09", cannot)
    assert m.main() == 2
    assert json.loads(capsys.readouterr().out)["status"] == "CANNOT_CHECK"
    p = subprocess.run([sys.executable,"-O",str(MOD)],capture_output=True,text=True)
    assert p.returncode == 2
