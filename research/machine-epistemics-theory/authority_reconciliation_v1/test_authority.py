"""Contract refusals and mathematical countermodels; finite tests are not new proof authority."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import resolve as authority

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / authority.PACKAGE


def profile(supports):
    supports = {frozenset(s) for s in supports}
    return frozenset(s for s in supports if not any(t < s for t in supports))


def product(left, right):
    return profile(a | b for a in left for b in right)


def alive(p, revoked):
    return any(not (s & revoked) for s in p)


class AuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = authority.load(ROOT)
        cls.manifest = json.loads((PACKAGE / 'SOURCES_V1.json').read_text())
        cls.sources = {s['path']: (ROOT / s['path']).read_bytes() for s in cls.manifest['files']}

    def check(self, data):
        return authority.validate_overlay(data, self.manifest, self.sources)

    def request(self, rule):
        return {'schema': 'ME_RULE_SELECTION_V1', 'rule_id': rule['id'], 'rule_sha256': rule['rule_sha256'],
                'scope_sha256': authority.sha256(rule['scope'].encode()), 'source_snapshot': authority.SNAPSHOT,
                'source_manifest_sha256': authority.MANIFEST_SHA256}

    def test_complete_source_bound_registry(self):
        self.assertEqual(self.check(self.data), {'rows': 56, 'rules': 36, 'corrections': 18})
        self.assertEqual(len(self.manifest['files']), 43)

    def test_every_legacy_row_is_not_a_selection(self):
        for row in self.data['rows']:
            with self.subTest(row=row['id']), self.assertRaises(authority.CannotCheck):
                authority.select(ROOT, {'id': row['id'], **row['historical_records']['canonical']})

    def test_every_scoped_rule_is_identified_without_authority(self):
        # The real custody check ran in setUpClass. Isolate selection behavior.
        with patch.object(authority, 'load', return_value=self.data):
            for rule in self.data['rules']:
                with self.subTest(rule=rule['id']):
                    result = authority.select(ROOT, self.request(rule))
                    self.assertIs(result['ocm_adoption_authorized'], False)
                    self.assertIs(result['scientific_truth_authorized'], False)
                    self.assertEqual(result['rule']['excluded_claims'], rule['excluded_claims'])

    def test_every_refuted_or_unsupported_clause_is_refused(self):
        with patch.object(authority, 'load', return_value=self.data):
            for correction in self.data['corrections']:
                request = self.request(self.data['rules'][0]); request['rule_id'] = correction['id']
                with self.subTest(correction=correction['id']), self.assertRaises(authority.CannotCheck):
                    authority.select(ROOT, request)

    def test_selection_binding_drift(self):
        with patch.object(authority, 'load', return_value=self.data):
            for field in self.request(self.data['rules'][5]):
                request = self.request(self.data['rules'][5]); request[field] += ':drift'
                with self.subTest(field=field), self.assertRaises(authority.CannotCheck):
                    authority.select(ROOT, request)

    def test_rule_must_be_listed_by_available_row(self):
        for status in ['OPEN', 'SCOPED_FRAGMENT_WITH_OPEN_BOUNDARY']:
            data = copy.deepcopy(self.data); data['rows'][5]['effective_status'] = status; data['rows'][5]['candidate_rules'] = []
            with patch.object(authority, 'load', return_value=data), self.assertRaises(authority.CannotCheck):
                authority.select(ROOT, self.request(data['rules'][5]))

    def test_ambiguous_clause_heading_refused(self):
        with self.assertRaises(authority.CannotCheck):
            authority.clause_section('## F09 one\nbody\n## F09 two\nbody\n', 'F09')
        self.assertEqual(authority.clause_section('## F09 one\na\n### sub\nb\n## F10 next\n', 'F09'), b'## F09 one\na\n### sub\nb\n')

    def test_duplicate_and_missing_rows(self):
        for collection in ['rows', 'rules', 'corrections']:
            for change in ['duplicate', 'missing']:
                data = copy.deepcopy(self.data)
                data[collection].append(copy.deepcopy(data[collection][0])) if change == 'duplicate' else data[collection].pop()
                with self.subTest(collection=collection, change=change), self.assertRaises(authority.CannotCheck):
                    self.check(data)

    def test_unknown_statuses_terminals_and_authority(self):
        changes = [('rows', 'effective_status', 'MAGIC_PROVED'), ('rows', 'terminal', 'PROVED'),
                   ('rules', 'status', 'PROVED'), ('rules', 'terminal', 'FROZEN'),
                   ('rules', 'ocm_adoption_authorized', True), ('rules', 'scientific_truth_authorized', 0),
                   ('corrections', 'disposition', 'ACCEPTED'), ('corrections', 'authority', 'PARITY')]
        for collection, field, value in changes:
            data = copy.deepcopy(self.data); data[collection][0][field] = value
            with self.subTest(collection=collection, field=field), self.assertRaises(authority.CannotCheck):
                self.check(data)

    def test_open_primitive_cannot_supply_candidate(self):
        data = copy.deepcopy(self.data); row = next(r for r in data['rows'] if r['effective_status'] == 'OPEN')
        row['candidate_rules'] = [data['rules'][0]['id']]
        with self.assertRaises(authority.CannotCheck): self.check(data)

    def test_exclusion_cannot_be_omitted_even_with_new_local_digest(self):
        data = copy.deepcopy(self.data); rule = next(r for r in data['rules'] if r['atlas_id'] == 'MEG-06')
        rule['excluded_claims'] = []
        rule['rule_sha256'] = authority.sha256(authority.canonical({k: v for k, v in rule.items() if k != 'rule_sha256'}))
        with self.assertRaises(authority.CannotCheck): self.check(data)

    def test_changed_parent_scope_statement_or_resources(self):
        for field in ['parent', 'scope', 'resources', 'statement']:
            data = copy.deepcopy(self.data); data['rules'][0][field] = '' if field != 'statement' else {'path': 'unbound', 'clause': 'F03'}
            with self.subTest(field=field), self.assertRaises(authority.CannotCheck): self.check(data)

    def test_historical_terminal_not_silently_rewritten(self):
        for field in ['status', 'terminal', 'authority', 'source']:
            data = copy.deepcopy(self.data); data['rows'][5]['historical_records']['canonical'][field] = 'REPAIRED'
            with self.subTest(field=field), self.assertRaises(authority.CannotCheck): self.check(data)

    def test_malformed_nested_values_fail_closed(self):
        for field in ['historical_records', 'candidate_rules', 'atlas_entries']:
            data = copy.deepcopy(self.data); data['rows'][0][field] = None
            with self.subTest(field=field), self.assertRaises(authority.CannotCheck): self.check(data)

    def test_duplicate_json_keys_and_nonfinite_numbers(self):
        for text in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}']:
            with self.subTest(text=text), self.assertRaises(authority.CannotCheck): authority.read_json(text)

    def test_scope_and_clause_pair_not_interchangeable(self):
        request = self.request(self.data['rules'][5]); request['rule_id'] = self.data['rules'][4]['id']
        with patch.object(authority, 'load', return_value=self.data), self.assertRaises(authority.CannotCheck):
            authority.select(ROOT, request)

    def test_result_mutation_does_not_edit_registry(self):
        with patch.object(authority, 'load', return_value=self.data):
            result = authority.select(ROOT, self.request(self.data['rules'][0]))
        result['rule']['scope'] = 'unbounded'
        self.assertNotEqual(self.data['rules'][0]['scope'], 'unbounded')

    def test_path_escape_and_internal_symlink_refused(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); (root / 'regular').write_text('x'); (root / 'link').symlink_to(root / 'regular')
            for path in ['../regular', '/tmp/a', './regular', 'link', 'a//b', 'missing']:
                with self.subTest(path=path), self.assertRaises(authority.CannotCheck): authority.regular(root, path)

    def test_unrelated_ancestor_symlink_is_allowed(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); (root / 'real').mkdir(); (root / 'real' / 'a').write_text('x'); (root / 'alias').symlink_to(root / 'real', target_is_directory=True)
            self.assertEqual(authority.regular(root / 'alias', 'a').read_text(), 'x')

    def test_reviewed_seal_blocks_recomputed_scope_digest(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / 'clone'
            subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--quiet', str(ROOT), str(root)], check=True, capture_output=True)
            subprocess.run(['git', '-C', str(root), 'checkout', authority.SNAPSHOT, '--', *self.sources], check=True, capture_output=True)
            (root / authority.PACKAGE).mkdir(parents=True)
            shutil.copyfile(PACKAGE / 'SOURCES_V1.json', root / authority.PACKAGE / 'SOURCES_V1.json')
            target = root / authority.PACKAGE / 'EFFECTIVE_AUTHORITY_V1.json'
            shutil.copyfile(PACKAGE / 'EFFECTIVE_AUTHORITY_V1.json', target)
            self.assertEqual(len(authority.load(root)['rows']), 56)
            data = copy.deepcopy(self.data); data['rules'][5]['scope'] = 'Every arbitrary navigation system'
            rule = data['rules'][5]; rule['rule_sha256'] = authority.sha256(authority.canonical({k: v for k, v in rule.items() if k != 'rule_sha256'}))
            target.write_text(json.dumps(data))
            with self.assertRaisesRegex(authority.CannotCheck, 'catalogue seal'): authority.load(root)
            shutil.copyfile(PACKAGE / 'EFFECTIVE_AUTHORITY_V1.json', target)
            source = next(iter(self.sources)); (root / source).write_bytes(self.sources[source] + b'\n')
            with self.assertRaisesRegex(authority.CannotCheck, 'source bytes drift'): authority.load(root)
            (root / source).unlink()
            with self.assertRaisesRegex(authority.CannotCheck, 'absent/nonregular'): authority.load(root)


class CounterexampleTests(unittest.TestCase):
    def test_old_width_does_not_give_earliest_decision(self):
        lower = lambda k: 1 - F(1, 2) ** (k + 1)
        width = lambda k: F(1, 2) ** (k + 1)
        theta = F(3, 5)
        self.assertEqual(next(k for k in range(10) if width(k) < theta - lower(0)), 3)
        self.assertEqual(next(k for k in range(10) if lower(k) >= theta), 1)
        for k in range(21): self.assertLess(lower(k), 1); self.assertEqual(lower(k) + width(k), 1)

    def test_equality_can_be_finitely_decided(self):
        # P is the nilpotent x->y transition and restart=1/2.
        seed = (F(1), F(0)); a0 = (F(1, 2), F(0)); a1 = (F(1, 2), F(1, 4))
        fixed = (F(1, 2), F(1, 4))
        self.assertNotEqual(a0, fixed); self.assertEqual(a1, fixed)
        self.assertGreaterEqual(a1[1], F(1, 4))

    def test_normalization_change_need_not_change_output(self):
        # At alpha=1, F(a)=s for both old/new P, independent of denominators.
        alpha = F(1); seed = (F(1), F(0))
        old = ((F(0), F(1)), (F(0), F(0)))
        new = ((F(0), F(1, 2)), (F(0), F(0)))
        def step(matrix): return tuple(alpha * seed[i] + (1-alpha) * sum(matrix[j][i] * seed[j] for j in range(2)) for i in range(2))
        self.assertNotEqual(old, new); self.assertEqual(step(old), step(new))

    def test_antichain_product_footprint_is_not_union(self):
        p, q = profile([{'a'}]), profile([{'a'}, {'b'}]); pq = product(p, q)
        self.assertEqual(pq, profile([{'a'}]))
        self.assertEqual(set().union(*p, *q), {'a', 'b'})
        self.assertEqual(set().union(*pq), {'a'})
        self.assertFalse(set().union(*pq) & {'b'}); self.assertTrue(set().union(*q) & {'b'})
        # Exact intervals have L=U=p or q. Truth-product identity still holds.
        for revoked in [set(), {'a'}, {'b'}, {'a', 'b'}]:
            self.assertEqual(alive(pq, revoked), alive(p, revoked) and alive(q, revoked))

    def test_shared_certificate_can_survive_alternative_support(self):
        model, certificate = profile([{'a'}]), profile([{'a'}, {'b'}])
        self.assertTrue(set().union(*model) & set().union(*certificate))
        self.assertFalse(alive(model, {'a'})); self.assertTrue(alive(certificate, {'a'}))

    def test_individually_live_supports_can_be_jointly_inconsistent(self):
        p, q = profile([{'a'}]), profile([{'b'}]); nogood = {'a', 'b'}
        self.assertTrue(alive(p, set()) and alive(q, set()))
        filtered = profile(s for s in product(p, q) if not nogood <= s)
        self.assertFalse(alive(filtered, set()))

    def test_snapshot_write_skew_is_not_serializable(self):
        # Invariant at least one of a,b is 1. Both writers read (1,1).
        snapshot = {'a': 1, 'b': 1}
        write_a = {'a': 0} if snapshot['b'] else {}
        write_b = {'b': 0} if snapshot['a'] else {}
        combined = {**snapshot, **write_a, **write_b}
        self.assertEqual(combined, {'a': 0, 'b': 0})
        serial = {'a': 0, 'b': 1}  # b-writer then sees a=0 and refuses.
        self.assertNotEqual(combined, serial)


if __name__ == '__main__': unittest.main()
