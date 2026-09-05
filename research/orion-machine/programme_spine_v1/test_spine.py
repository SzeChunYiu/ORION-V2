"""Hostile mutations exercise real validation paths, with explicit non-vacuous controls."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import validate as V
import run_checks as R

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

class SpineTests(unittest.TestCase):
    def setUp(self):
        self.backlog=V.load(HERE,'OCM_EXECUTION_BACKLOG_V1.json')
        self.schema=V.load(HERE,'OCM_EXECUTION_BACKLOG_V1.schema.json')
        self.source=V.load(HERE,'SOURCE_ISSUES_V1.json')
        self.snapshot=V.load(HERE,'SOURCE_SNAPSHOT_V1.json')
        self.events=[V.parse(x) for x in V.read(HERE,'TASK_EVENTS_V1.jsonl').splitlines()]
        self.by_id={t['task_id']:t for t in self.backlog['tasks']}

    def rehash(self,events):
        for i,event in enumerate(events):
            event['sequence']=i
            event['previous_hash']=events[i-1]['event_hash'] if i else '0'*64
            event['event_hash']=V.sha(V.canonical({k:v for k,v in event.items() if k!='event_hash'}))

    def basic(self):
        return V.validate_backlog(self.backlog,self.schema,self.source)

    def event_check(self):
        return V.validate_events(self.events,self.by_id,self.snapshot['genesis_hash'])

    def temporary_change(self,name,change):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            for path in HERE.iterdir():
                if path.is_file(): shutil.copyfile(path,target/path.name)
            payload=V.load(target,name)
            change(payload)
            (target/name).write_text(json.dumps(payload))
            return V.validate(ROOT,target)

    def mutate(self,ident):
        t=self.backlog['tasks'][0]
        if ident=='invalid_status': t['status']='PASS'; return self.basic()
        if ident=='dangling_dependency': t['dependencies']=['NO_SUCH_TASK']; return self.basic()
        if ident=='duplicate_id': self.backlog['tasks'][1]['task_id']=t['task_id']; return self.basic()
        if ident=='checked_without_evidence': t['status']='COMPLETE'; return self.basic()
        if ident=='cycle': t['dependencies']=[t['task_id']]; return self.basic()
        if ident=='omitted_task': self.backlog['tasks'].pop(); return self.basic()
        if ident=='altered_task_statement': t['description']+=' silently stronger'; return self.basic()
        if ident=='false_green_with_related_evidence':
            t=next(x for x in self.backlog['tasks'] if x['evidence'])
            t['status']='COMPLETE'; t['terminal']='PASS'; return self.basic()
        if ident=='cannot_check_terminal_laundering': t['terminal']='CANNOT_CHECK'; return self.basic()
        if ident=='zero_denominator': return V.check_denominator({'numerator':0,'denominator':0})
        if ident=='boolean_denominator': return V.check_denominator({'numerator':0,'denominator':True})
        if ident=='stale_evidence_pointer':
            def change(payload):
                next(x for x in payload['tasks'] if x['evidence'])['evidence'][0]['sha256']='0'*64
            return self.temporary_change('OCM_EXECUTION_BACKLOG_V1.json',change)
        if ident=='proof_hash_drift':
            binding=self.snapshot['source_bindings'][0]
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/binding['path']; path.parent.mkdir(parents=True)
                path.write_bytes(V.read(ROOT,binding['path'])+b'changed')
                return V.validate_binding(binding,Path(tmp))
        if ident=='unrecorded_theorem_mutation':
            return self.temporary_change('THEOREM_CANDIDATE_SNAPSHOT_V1.json',lambda p:p['theorems'][0].update(title='Stronger statement'))
        if ident=='unrecorded_status_transition':
            self.by_id['OPS-001']['status']='IN_PROGRESS'; return self.event_check()
        if ident=='event_task_substitution':
            self.events[1]['task_id']='OM-WP0-002'; self.rehash(self.events); return self.event_check()
        if ident=='event_chain_break': self.events[1]['previous_hash']='f'*64; return self.event_check()
        if ident=='event_history_reset':
            self.events[0]['authority_delta']='NONE_CHANGED'; self.rehash(self.events); return self.event_check()
        if ident=='event_tail_truncation': self.events.pop(); return self.event_check()
        if ident=='authority_escalation':
            self.events[1]['authority_delta']='SCIENTIFIC_ADMISSION'; self.rehash(self.events); return self.event_check()
        if ident=='free_parser': return V.check_measurement({'status':'UNKNOWN','value':0})
        if ident=='free_verifier': return V.check_measurement({'status':'MEASURED','value':0,'numerator':0,'denominator':10})
        if ident=='unjustified_nonapplicability': return V.check_measurement({'status':'NOT_APPLICABLE','value':None})
        if ident=='unsupported_schema_keyword':
            self.schema['unrecognizedValidationKeyword']=True; return self.basic()
        if ident=='duplicate_json_key': return V.parse('{"status":"OPEN","status":"COMPLETE"}')
        if ident=='nan_json': return V.parse('{"denominator":NaN}')
        if ident=='missing_source': return V.read(HERE,'does-not-exist-proof.lean')
        if ident=='missing_git_object':
            binding=copy.deepcopy(self.snapshot['source_bindings'][0]); binding['commit']='f'*40
            return V.validate_binding(binding,ROOT)
        if ident=='symlink_source':
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); (root/'alias').symlink_to(HERE/'README.md')
                return V.read(root,'alias')
        if ident=='missing_optional_tool':
            # A fabricated zero exit still cannot turn an unregistered tool into PASS.
            result=R.classify(0,tool_registered=False)
            self.assertEqual(result,'CANNOT_CHECK')
            raise V.CannotCheck(result)
        raise AssertionError('Fixture has no mutation implementation: '+ident)

    def test_real_shipped_checkpoint(self):
        result=V.validate()
        self.assertEqual((result['tasks'],result['source_bindings'],result['accepted_tasks']),(231,32,0))
        self.assertEqual(result['event_count'],19)
        self.assertFalse(result['scientific_admission'])

    def test_hostile_fixture_corpus(self):
        corpus=V.load(HERE,'fixtures/invalid_cases.json')
        self.assertEqual(len(corpus),30)
        self.assertEqual(len({x['id'] for x in corpus}),30)
        for fixture in corpus:
            with self.subTest(fixture=fixture['id']):
                self.setUp()
                with self.assertRaisesRegex((V.Defect,V.CannotCheck),fixture['expected']):
                    self.mutate(fixture['id'])

    def test_all_source_checkboxes_accounted(self):
        expected=V.source_tasks(self.source['197']['body'])
        self.assertEqual(len(expected),231)
        self.assertEqual(sum(x.startswith('OM-CLOSE-') for x in expected),17)
        self.assertEqual(sum(not x.startswith('OM-CLOSE-') for x in expected),214)
        self.assertEqual(set(expected),set(self.by_id))

    def test_no_alarm_counts_and_resources(self):
        V.check_denominator({'numerator':0,'denominator':100})
        V.check_measurement({'status':'UNKNOWN','value':None})
        V.check_measurement({'status':'NOT_APPLICABLE','value':None,'reason':'No quantum operator in this classical model.'})
        V.check_measurement({'status':'MEASURED','value':0,'unit':'operation','source':'explicit observation','numerator':0,'denominator':100})
        self.assertEqual(R.classify(0),'PASS')
        self.assertEqual(R.classify(1),'FAIL')
        self.assertEqual(R.classify(2),'CANNOT_CHECK')

    def test_unchanged_event_chain_and_ready_states(self):
        result=self.event_check()
        self.assertEqual(result['event_tip'],self.snapshot['event_tip'])
        self.assertEqual(sum(t['status']=='READY_FOR_REVIEW' for t in self.by_id.values()),9)

    def test_engineering_completion_is_representable_in_a_successor(self):
        t=self.by_id['OM-WP0-001']
        t['status']='COMPLETE'; t['terminal']='PASS'
        t['evidence']=[{'kind':'ENGINEERING_VERIFICATION','path':'future/receipt.json','sha256':'a'*64,'scope':'Routine engineering; no scientific admission.','commit':'b'*40,'git_blob':'c'*40,'verified_checkpoint_sha256':V.SNAPSHOT_SHA256}]
        self.basic() # Structural support is not receipt authentication or acceptance.
        event={'sequence':19,'previous_hash':self.events[-1]['event_hash'],'kind':'STATUS_TRANSITION','task_id':t['task_id'],'task_identity_sha256':V.task_identity(t),'from_status':'READY_FOR_REVIEW','to_status':'COMPLETE','authority_delta':'NONE','verification_receipt_sha256':'a'*64,'verified_checkpoint_sha256':V.SNAPSHOT_SHA256}
        event['event_hash']=V.sha(V.canonical(event)); self.events.append(event)
        self.event_check() # The current immutable V1 checkpoint would still refuse this unanchored extension.

    def test_completion_event_order_must_respect_dependencies(self):
        for ident in ('OM-WP0-001','OM-WP0-002'):
            task=self.by_id[ident];task['status']='COMPLETE';task['terminal']='PASS'
            task['evidence']=[{'kind':'ENGINEERING_VERIFICATION','path':'future/receipt.json','sha256':'a'*64,'scope':'Routine engineering.','verified_checkpoint_sha256':V.SNAPSHOT_SHA256}]
        self.basic() # Both final statuses complete, so the graph alone cannot catch wrong order.
        prefix=copy.deepcopy(self.events)
        def append_completion(ident):
            e={'sequence':len(self.events),'previous_hash':self.events[-1]['event_hash'],'kind':'STATUS_TRANSITION','task_id':ident,'task_identity_sha256':V.task_identity(self.by_id[ident]),'from_status':'READY_FOR_REVIEW','to_status':'COMPLETE','authority_delta':'NONE','verification_receipt_sha256':'a'*64,'verified_checkpoint_sha256':V.SNAPSHOT_SHA256}
            e['event_hash']=V.sha(V.canonical(e));self.events.append(e)
        append_completion('OM-WP0-001');append_completion('OM-WP0-002');self.event_check()
        self.events=prefix
        append_completion('OM-WP0-002');append_completion('OM-WP0-001')
        with self.assertRaisesRegex(V.Defect,'INCOMPLETE_EVENT_DEPENDENCY'):self.event_check()

    def test_dependency_deletion_cannot_change_reviewed_graph(self):
        def change(payload):
            next(t for t in payload['tasks'] if t['task_id']=='OM-WP0-002')['dependencies']=[]
        with self.assertRaisesRegex(V.Defect,'DEPENDENCY_GRAPH_DRIFT'):
            self.temporary_change('OCM_EXECUTION_BACKLOG_V1.json',change)

    def test_completion_requires_completed_dependency(self):
        t=self.by_id['OM-WP0-004'];t['status']='COMPLETE';t['terminal']='PASS'
        t['evidence']=[{'kind':'ENGINEERING_VERIFICATION','path':'future/receipt.json','sha256':'a'*64,'scope':'Routine engineering.'}]
        with self.assertRaisesRegex(V.Defect,'INCOMPLETE_DEPENDENCY'): self.basic()

    def receipt_fixture(self):
        task_ids=[f'OM-WP0-{n:03d}' for n in range(1,10)]
        rows=[]
        previous=V.SNAPSHOT_SHA256
        for ident in ['SPINE','HOSTILES','TRACE_PARENT','REPRESENTATION','COMPILER_CORRECTION','SUBSTRATE','PROOF_ASSISTANT']:
            row={'check_id':ident,'required':ident!='PROOF_ASSISTANT','status':'PASS' if ident!='PROOF_ASSISTANT' else 'CANNOT_CHECK','exit_code':0 if ident!='PROOF_ASSISTANT' else None,'previous_hash':previous,'result':{}}
            if ident=='SPINE': row['result']={'tasks':231,'accepted_tasks':0}
            if ident=='HOSTILES': row['result']={'tests':10,'skips':0}
            row['receipt_hash']=V.sha(V.canonical(row));previous=row['receipt_hash'];rows.append(row)
        return {'engineering_scope':{'task_ids':task_ids,'task_identity_sha256':{x:V.task_identity(self.by_id[x]) for x in task_ids},'source_body_sha256':self.backlog['source_body_sha256'],'checkpoint_phase':'PRE_ACCEPTANCE'},'source_snapshot_sha256':V.SNAPSHOT_SHA256,'terminal':'PASS_REQUIRED_ENGINEERING_CHECKS','scientific_admission':False,'independent_review_satisfied':False,'protected_outcomes_accessed':False,'required_checks':6,'required_passes':6,'rows':rows,'final_receipt_hash':previous,'all_checks_pass':False}

    def check_receipt(self,receipt):
        V.validate_engineering_receipt(receipt,'OM-WP0-001',self.by_id,V.SNAPSHOT_SHA256,self.backlog['source_body_sha256'])

    def test_preacceptance_receipt_exact_subject_and_chain(self):
        receipt=self.receipt_fixture();self.check_receipt(receipt)
        cases=[('wrong_subject','ENGINEERING_RECEIPT_WRONG_SUBJECT'),('wrong_checkpoint','ENGINEERING_RECEIPT_WRONG_CHECKPOINT'),('missing_check','ENGINEERING_RECEIPT_CHECK_INVENTORY'),('false_count','ENGINEERING_RECEIPT_FALSE_GREEN'),('changed_chain','ENGINEERING_RECEIPT_CHAIN'),('wrong_tip','ENGINEERING_RECEIPT_TIP')]
        for kind,expected in cases:
            with self.subTest(kind=kind):
                mutant=copy.deepcopy(receipt)
                if kind=='wrong_subject':mutant['engineering_scope']['task_identity_sha256']['OM-WP0-001']='0'*64
                elif kind=='wrong_checkpoint':mutant['source_snapshot_sha256']='0'*64
                elif kind=='missing_check':mutant['rows'].pop()
                elif kind=='false_count':mutant['required_checks']=5;mutant['required_passes']=5
                elif kind=='changed_chain':mutant['rows'][1]['result']['tests']=0
                elif kind=='wrong_tip':mutant['final_receipt_hash']='0'*64
                with self.assertRaisesRegex(V.Defect,expected):self.check_receipt(mutant)

    def test_scientific_completion_does_not_borrow_engineering_receipt(self):
        t=self.by_id['OM-T09']; t['status']='COMPLETE'; t['terminal']='PASS'
        t['evidence']=[{'kind':'ENGINEERING_VERIFICATION','path':'future/receipt.json','sha256':'a'*64,'scope':'Fake scientific closure.'}]
        with self.assertRaisesRegex(V.Defect,'UNAUTHORIZED_COMPLETION'): self.basic()

    def test_extra_property_and_numeric_boolean_are_invalid(self):
        self.backlog['tasks'][0]['command']='arbitrary command'
        with self.assertRaisesRegex(V.Defect,'SCHEMA_ADDITIONAL_PROPERTY'): self.basic()
        self.backlog['tasks'][0].pop('command'); self.backlog['tasks'][0]['source_line']=True
        with self.assertRaisesRegex(V.Defect,'SCHEMA_TYPE'): self.basic()

    def test_runner_refuses_zero_tests_and_skips(self):
        with self.assertRaisesRegex(V.Defect,'EMPTY_HOSTILE_TEST_RUN'):
            R.check_output('HOSTILES','','Ran 0 tests in 0.0s\n\nOK')
        with self.assertRaisesRegex(V.Defect,'SKIPPED_HOSTILE_TEST'):
            R.check_output('HOSTILES','','Ran 10 tests in 0.0s\n\nOK (skipped=1)')

    def test_path_parent_traversal(self):
        with self.assertRaisesRegex(V.Defect,'UNSAFE_PATH'):
            V.read(HERE,'../OCM_FAILURE_LEDGER.md')

if __name__=='__main__':
    unittest.main()
