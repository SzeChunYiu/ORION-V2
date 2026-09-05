"""Finite calibrations and hostile contract checks; not independent scientific review."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'research/machine-epistemics-theory/foundation_revision_v1'
SPEC = importlib.util.spec_from_file_location('me_foundation_v1', PACKAGE / 'foundation.py')
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


class TestFoundation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = M.checks(3)
        cls.registry = json.loads((PACKAGE / 'REGISTRY.json').read_text())

    def test_registered_denominators(self):
        c = self.result['checks']
        self.assertEqual((self.result['profiles'], self.result['intervals']), (20, 168))
        self.assertEqual(c['interval_pairs_times_revocations'], 225792)
        self.assertEqual(c['nogood_pairs_times_revocations'], 22400)
        self.assertEqual(c['selection_event_pairs'], 65280)
        self.assertEqual(c['version_space_revocation_checks'], 48)
        self.assertEqual(c['graded_dynamics_checks'], 72)

    def test_invalid_interval(self):
        with self.assertRaises(ValueError):
            M.Interval((1,), (2,))

    def test_unknown_not_false(self):
        self.assertEqual(M.Interval(M.ZERO, M.ONE).status(), 1)
        self.assertEqual(M.Interval(M.ZERO, M.ZERO).status(), 0)

    def test_refinement_exhaustive_n2(self):
        ps = M.profiles(2)
        intervals = [M.Interval(p,q) for p in ps for q in ps if M.leq(p,q)]
        for p in intervals:
            for q in intervals:
                if M.leq(p.lower,q.lower) and M.leq(q.upper,p.upper):
                    refined = p.refine(q.lower,q.upper)
                    for r in range(4):
                        if p.status(r) != 1:
                            self.assertEqual(p.status(r),refined.status(r))

    def test_nogood_semiring_n2(self):
        for ng in ((1,), (2,), (3,)):
            clean = {M.filter_ng(p,ng) for p in M.profiles(2)}
            for p in clean:
                self.assertEqual(M.ng_meet(p,M.ONE,ng),p)
                for q in clean:
                    for r in clean:
                        self.assertEqual(M.ng_meet(M.ng_meet(p,q,ng),r,ng),M.ng_meet(p,M.ng_meet(q,r,ng),ng))
                        self.assertEqual(M.ng_meet(p,M.join(q,r),ng),M.join(M.ng_meet(p,q,ng),M.ng_meet(p,r,ng)))

    def test_nogood_no_alarm(self):
        for p in M.profiles(3):
            self.assertEqual(M.filter_ng(p,()),p)

    def test_missing_derived_definition(self):
        with self.assertRaises(M.CannotCheck):
            M.substitute((1,),{})

    def test_contradiction_never_vacuous(self):
        self.assertEqual(M.agreement(((0,),(1,)),((0,0),(0,1)),0),('CONTRADICTION',None))

    def test_query_agreement_not_global_identification(self):
        self.assertEqual(M.agreement(((0,0),(0,1)),(),0),('EXACT',0))

    def test_invalid_system(self):
        for p,s,a in [(((M.F(2),),),(M.F(1),),M.F(1,2)), (((M.F(0),),),(M.F(1),),M.F(0))]:
            with self.assertRaises(ValueError):
                M.fixed(p,s,a)

    def test_sharp_perturbation_bound(self):
        alpha,d=M.F(1,3),M.F(1,4)
        a=M.fixed(((M.F(1),),),(M.F(1),),alpha)[0]
        b=M.fixed(((1-d,),),(M.F(1),),alpha)[0]
        self.assertEqual(a-b,(1-alpha)/alpha*d*b)

    def test_full_manifest_required(self):
        with self.assertRaises(ValueError):
            M.Manifest((('implementation','x'),))

    def test_exact_authorized_gate(self):
        self.assertEqual(M.action_status(M.Interval(M.ONE,M.ONE),exact_proof=True,
            binding='VALID_BINDING',authorized=True,conditional_risk=None,risk_budget=M.F(0)),
            'EXACT_ASSERTION_ALLOWED')

    def test_marginal_only_not_action_certificate(self):
        self.assertEqual(M.action_status(M.Interval(M.ZERO,M.ONE),exact_proof=False,
            binding='VALID_BINDING',authorized=True,conditional_risk=None,risk_budget=M.F(1,10)),'UNKNOWN')

    def test_stale_gate(self):
        self.assertEqual(M.action_status(M.Interval(M.ONE,M.ONE),exact_proof=True,
            binding='REVALIDATE',authorized=True,conditional_risk=M.F(0),risk_budget=M.F(1)),'REVALIDATE')

    def test_registry(self):
        M.validate_registry(self.registry)
        text=(PACKAGE/'THEORY.md').read_text()
        for row in self.registry['gaps']:
            for proof in row['proofs']:
                self.assertIn('## '+proof+'.',text)

    def test_registry_hostiles(self):
        mutations = []
        d=copy.deepcopy(self.registry);d['scientific_completion']=True;mutations.append(d)
        d=copy.deepcopy(self.registry);d['gaps'].pop();mutations.append(d)
        d=copy.deepcopy(self.registry);d['gaps'][1]['id']='MEG-01';mutations.append(d)
        d=copy.deepcopy(self.registry);d['gaps'][0]['status']='COMPLETE';mutations.append(d)
        d=copy.deepcopy(self.registry);d['gaps'][0]['proofs']=[];mutations.append(d)
        d=copy.deepcopy(self.registry);d['gaps'][0]['proofs']=['F99'];mutations.append(d)
        d=copy.deepcopy(self.registry);d['gaps'][0]['depends_on']=['MEG-99'];mutations.append(d)
        d=copy.deepcopy(self.registry);d['gaps'][0]['depends_on']=['MEG-02'];mutations.append(d)
        d=copy.deepcopy(self.registry);d['gaps'][0]['remaining']='';mutations.append(d)
        for i,d in enumerate(mutations):
            with self.subTest(mutation=i),self.assertRaises(ValueError):
                M.validate_registry(d)

    def test_cli_pass(self):
        p=subprocess.run([sys.executable,str(PACKAGE/'foundation.py'),'--n','2'],capture_output=True,text=True,check=False)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertEqual(json.loads(p.stdout)['terminal'],'FINITE_CALIBRATION_PASS')

    def test_cli_cannot_check(self):
        p=subprocess.run([sys.executable,str(PACKAGE/'foundation.py'),'--n','4'],capture_output=True,text=True,check=False)
        self.assertEqual(p.returncode,2,p.stdout+p.stderr)
        self.assertEqual(json.loads(p.stdout)['terminal'],'CANNOT_CHECK')

    def test_cli_failure(self):
        output=io.StringIO()
        with (patch.object(sys,'argv',['foundation.py']),
              patch.object(M,'checks',side_effect=M.CheckFailure('planted')),
              contextlib.redirect_stdout(output)):
            self.assertEqual(M.main(),1)
        self.assertEqual(json.loads(output.getvalue())['terminal'],'FAIL')

    def test_optimized_python_keeps_checks(self):
        p=subprocess.run([sys.executable,'-O',str(PACKAGE/'foundation.py'),'--n','2'],capture_output=True,text=True,check=False)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertGreater(json.loads(p.stdout)['checks']['selection_event_pairs'],0)


if __name__=='__main__':
    unittest.main()
