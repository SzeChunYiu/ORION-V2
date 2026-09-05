"""Real merged-delivery baseline plus local refusal controls; no fake acceptance."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import accept as A


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.observation=A.V.load(A.HERE/'packet','MERGED_DELIVERY_OBSERVATION_V1.json')

    def test_actual_merged_delivery_and_nonconsequences(self):
        result=A.verify(A.HERE/'packet')
        self.assertEqual((result['accepted_tasks'],result['total_tasks'],result['unchanged_tasks']),(9,231,222))
        self.assertEqual((result['original_events'],result['appended_events'],result['source_check_count']),(19,9,11))
        self.assertEqual(result['pre_acceptance_hostile_tests'],14)
        self.assertFalse(result['independent_review_satisfied'])
        self.assertFalse(result['master_issue_197_closed'])
        self.assertFalse(result['issue_checkbox_mutation_performed'])

    def test_exact_prefix_and_only_nine_delivered_engineering_tasks(self):
        prefix=A.blob(A.PREFIX+'TASK_EVENTS_V1.jsonl')
        events=(A.HERE/'packet/TASK_EVENTS_WITH_ACCEPTANCE_V1.jsonl').read_bytes()
        self.assertTrue(events.startswith(prefix))
        additions=[A.V.parse(x) for x in events[len(prefix):].splitlines()]
        self.assertEqual([x['task_id'] for x in additions],A.IDS)
        original=A.read_original('OCM_EXECUTION_BACKLOG_V1.json')
        self.assertEqual(sum(t['status']=='READY_FOR_REVIEW' for t in original['tasks']),9)
        self.assertEqual(sum(t['status']=='COMPLETE' for t in original['tasks']),0)

    def test_pending_delivery_cannot_materialize_any_packet(self):
        self.observation['pull_request']['merged']=False
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'must-not-exist'
            with patch.object(A,'observe',return_value=self.observation):
                with self.assertRaisesRegex(A.V.CannotCheck,'DELIVERY_NOT_MERGED'):
                    A.materialize(Path(tmp),output)
            self.assertFalse(output.exists())

    def test_actual_ci_receipt_refusal_controls(self):
        cases=[('wrong_head','WRONG_CHECK_HEAD'),('pending_check','CHECK_NOT_COMPLETED'),
               ('skipped_check','CHECK_NOT_SUCCESSFUL'),('failed_check','CHECK_NOT_SUCCESSFUL'),
               ('omitted_check','INCOMPLETE_CHECK_INVENTORY'),('wrong_tree','WRONG_MERGE_OBJECT'),
               ('wrong_branch','WRONG_DEFAULT_BRANCH')]
        for kind,expected in cases:
            with self.subTest(kind=kind):
                candidate=copy.deepcopy(self.observation)
                if kind=='wrong_head':candidate['checks'][0]['head_sha']='0'*40
                elif kind=='pending_check':candidate['checks'][0]['status']='in_progress'
                elif kind=='skipped_check':candidate['checks'][0]['conclusion']='skipped'
                elif kind=='failed_check':candidate['checks'][0]['conclusion']='failure'
                elif kind=='omitted_check':candidate['checks'].pop()
                elif kind=='wrong_tree':candidate['merged_git_object']['tree']='0'*40
                elif kind=='wrong_branch':candidate['default_branch']='unrelated'
                with self.assertRaisesRegex((A.V.Defect,A.V.CannotCheck),expected):
                    A.validate_observation(candidate)

    def mutated_packet(self,change):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'packet';shutil.copytree(A.HERE/'packet',output)
            change(output)
            # Re-sealing a forged payload cannot defeat semantic derivation checks.
            manifest=A.V.load(output,'MANIFEST_V1.json')
            for name in manifest['files']:
                manifest['files'][name]=A.V.sha((output/name).read_bytes())
            (output/'MANIFEST_V1.json').write_bytes(A.V.canonical(manifest)+b'\n')
            return A.verify(output)

    def test_rehashed_external_review_promotion_refused(self):
        def change(directory):
            path=directory/'BACKLOG_ACCEPTANCE_OVERLAY_V1.json';value=A.V.parse(path.read_bytes())
            value['WP0_010_status']='COMPLETE';path.write_bytes(A.V.canonical(value)+b'\n')
        with self.assertRaisesRegex(A.V.Defect,'ACCEPTANCE_DERIVATION_DRIFT'):
            self.mutated_packet(change)

    def test_rehashed_original_history_rewrite_refused(self):
        def change(directory):
            path=directory/'TASK_EVENTS_WITH_ACCEPTANCE_V1.jsonl'
            lines=path.read_bytes().splitlines();event=A.V.parse(lines[0]);event['authority_delta']='SCIENCE'
            lines[0]=A.V.canonical(event);path.write_bytes(b'\n'.join(lines)+b'\n')
        with self.assertRaisesRegex(A.V.Defect,'ACCEPTANCE_DERIVATION_DRIFT'):
            self.mutated_packet(change)

    def test_rehashed_acceptance_event_reordering_refused(self):
        def change(directory):
            path=directory/'TASK_EVENTS_WITH_ACCEPTANCE_V1.jsonl';lines=path.read_bytes().splitlines()
            lines[19],lines[20]=lines[20],lines[19];path.write_bytes(b'\n'.join(lines)+b'\n')
        with self.assertRaisesRegex(A.V.Defect,'ACCEPTANCE_DERIVATION_DRIFT'):
            self.mutated_packet(change)

    def test_wrong_preacceptance_receipt_identity_refused(self):
        original=A.blob
        def changed(path):
            raw=original(path)
            return raw+b'\n' if path==A.RECEIPT_PATH else raw
        with patch.object(A,'blob',side_effect=changed):
            with self.assertRaisesRegex(A.V.Defect,'WRONG_PREACCEPTANCE_RECEIPT'):
                A.derive(self.observation)


if __name__=='__main__':unittest.main()
