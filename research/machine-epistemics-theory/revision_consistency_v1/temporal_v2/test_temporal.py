"""Finite synthetic tests; no external state, effects, credentials or production API."""
from dataclasses import FrozenInstanceError, replace
import unittest

from temporal import (Envelope, Verdict, Witness, classify, completion_reference,
                      kernel, parent_kernel, path_reference, verify_witness, witness)


class TemporalTests(unittest.TestCase):
    def env(self, lower=(), upper=None, good=(0, 1), n=3):
        return Envelope(n, frozenset(lower), frozenset(lower if upper is None else upper),
                        frozenset(good), "synthetic-v2")

    def test_safe_cycle(self):
        e = self.env(((0, 1), (1, 0)))
        self.assertEqual(classify(e, frozenset({0})), Verdict.PERSISTENT)
        self.assertEqual(kernel(e.n, e.upper, e.good).safe, frozenset({0, 1}))

    def test_dead_end_quiescence(self):
        self.assertEqual(classify(self.env(), frozenset({0})), Verdict.PERSISTENT)

    def test_zero_step_bad_state(self):
        e = self.env()
        w = witness(e, 2, "lower")
        self.assertEqual(w.path, (2,))
        self.assertTrue(verify_witness(e, w, 2))
        self.assertEqual(classify(e, frozenset({2})), Verdict.REFUTED)

    def test_current_validity_is_not_persistence(self):
        e = self.env(((0, 1), (1, 2)))
        self.assertIn(0, e.good)
        self.assertEqual(classify(e, frozenset({0})), Verdict.REFUTED)

    def test_one_step_only_mutant_is_wrong(self):
        e = self.env(((0, 1), (1, 2)))
        one_step = all(t in e.good for s, t in e.upper if s == 0)
        self.assertTrue(one_step)
        self.assertNotIn(0, kernel(e.n, e.upper, e.good).safe)

    def test_shortest_counterexample(self):
        e = self.env(((0, 1), (1, 2), (0, 2)))
        w = witness(e, 0, "upper")
        self.assertEqual(w.path, (0, 2))
        self.assertEqual(len(w.path), len(path_reference(e.n, e.upper, e.good, 0)))

    def test_refuted_does_not_mean_all_paths_fail(self):
        e = self.env(((0, 0), (0, 2)))
        self.assertEqual(classify(e, frozenset({0})), Verdict.REFUTED)
        self.assertIn((0, 0), e.lower)  # staying safe is possible; guarantee is false

    def test_optional_edge_has_two_disagreeing_completions(self):
        e = self.env((), ((0, 2),))
        self.assertEqual(classify(e, frozenset({0})), Verdict.CANNOT_CHECK)
        self.assertIn(0, parent_kernel(e.n, e.lower, e.good))
        self.assertNotIn(0, parent_kernel(e.n, e.upper, e.good))

    def test_missing_optional_is_not_proof_of_absence(self):
        e = self.env((), ((0, 2),))
        mutant = replace(e, upper=e.lower)
        self.assertEqual(classify(mutant, frozenset({0})), Verdict.PERSISTENT)
        self.assertEqual(classify(e, frozenset({0})), Verdict.CANNOT_CHECK)

    def test_optional_is_not_required(self):
        e = self.env((), ((0, 2),))
        mutant = replace(e, lower=e.upper)
        self.assertEqual(classify(mutant, frozenset({0})), Verdict.REFUTED)
        self.assertEqual(classify(e, frozenset({0})), Verdict.CANNOT_CHECK)

    def test_optional_safe_edges_no_alarm(self):
        e = self.env((), ((0, 1), (1, 0)))
        self.assertEqual(classify(e, frozenset({0, 1})), Verdict.PERSISTENT)

    def test_known_adverse_path_refutes_every_completion(self):
        e = self.env(((0, 2),), ((0, 2), (0, 1), (1, 0)))
        self.assertEqual(classify(e, frozenset({0})), Verdict.REFUTED)
        self.assertEqual(completion_reference(e, frozenset({0})), Verdict.REFUTED)

    def test_belief_is_universal_not_existential(self):
        e = self.env(((1, 2),))
        self.assertEqual(classify(e, frozenset({0})), Verdict.PERSISTENT)
        self.assertEqual(classify(e, frozenset({0, 1})), Verdict.REFUTED)

    def test_empty_belief_is_not_proof(self):
        self.assertEqual(classify(self.env(), frozenset()), Verdict.CANNOT_CHECK)

    def test_unbound_model_is_not_complete(self):
        self.assertEqual(classify(None, frozenset({0})), Verdict.CANNOT_CHECK)

    def test_refinement_resolves_unknown_both_ways(self):
        e = self.env((), ((0, 2),))
        self.assertEqual(classify(e, frozenset({0})), Verdict.CANNOT_CHECK)
        self.assertEqual(classify(replace(e, upper=e.lower), frozenset({0})), Verdict.PERSISTENT)
        self.assertEqual(classify(replace(e, lower=e.upper), frozenset({0})), Verdict.REFUTED)

    def test_refinement_cannot_flip_decisive_case(self):
        e = self.env((), ((0, 1),))
        self.assertEqual(classify(e, frozenset({0})), Verdict.PERSISTENT)
        self.assertEqual(classify(replace(e, lower=e.upper), frozenset({0})), Verdict.PERSISTENT)

    def test_witness_is_bound_to_scope_and_model(self):
        e = self.env(((0, 2),))
        w = witness(e, 0, "lower")
        self.assertFalse(verify_witness(replace(e, scope="other-scope"), w, 0))
        self.assertFalse(verify_witness(replace(e, good=frozenset({0, 1, 2})), w, 0))

    def test_missing_edge_witness_rejected(self):
        e = self.env(((0, 2),))
        w = Witness(e.fingerprint, "lower", (0, 1, 2))
        self.assertFalse(verify_witness(e, w, 0))

    def test_malformed_and_wrong_start_witness_rejected(self):
        e = self.env(((0, 2),))
        for path in ((), (True, 2), [0, 2], (0, 0, 2), (0, 3), (0,)):
            with self.subTest(path=path):
                self.assertFalse(verify_witness(e, Witness(e.fingerprint, "lower", path), 0))
        self.assertFalse(verify_witness(e, witness(e, 0, "lower"), 1))

    def test_upper_witness_is_not_a_lower_witness(self):
        e = self.env((), ((0, 2),))
        w = witness(e, 0, "upper")
        self.assertTrue(verify_witness(e, w, 0))
        self.assertFalse(verify_witness(e, replace(w, relation="lower"), 0))

    def test_boolean_ids_rejected(self):
        for n, lower, good in ((True, frozenset(), frozenset()),
                               (3, frozenset({(True, 2)}), frozenset({0})),
                               (3, frozenset(), frozenset({True}))):
            with self.subTest(n=n, lower=lower), self.assertRaises(ValueError):
                Envelope(n, lower, lower, good, "x")
        with self.assertRaises(ValueError):
            classify(self.env(), frozenset({True}))

    def test_mutable_nested_inputs_rejected(self):
        with self.assertRaises(ValueError):
            Envelope(3, set(), frozenset(), frozenset({0}), "x")
        with self.assertRaises(ValueError):
            Envelope(3, frozenset(), frozenset(), {0}, "x")
        with self.assertRaises(ValueError):
            classify(self.env(), {0})

    def test_invalid_model_rejected(self):
        with self.assertRaises(ValueError):
            Envelope(0, frozenset(), frozenset(), frozenset(), "x")
        with self.assertRaises(ValueError):
            self.env(((0, 3),))
        with self.assertRaises(ValueError):
            self.env(((0, 1),), ())
        with self.assertRaises(ValueError):
            replace(self.env(), scope="")

    def test_immutability_and_fingerprint(self):
        e = self.env(((0, 1), (1, 2)))
        with self.assertRaises(FrozenInstanceError):
            e.scope = "changed"
        self.assertEqual(e.fingerprint, self.env(((1, 2), (0, 1))).fingerprint)
        self.assertNotEqual(e.fingerprint, self.env(((1, 2),)).fingerprint)

    def test_more_permitted_revisions_cannot_expand_safe_kernel(self):
        e = self.env((), ((0, 1), (1, 2)))
        self.assertLessEqual(kernel(e.n, e.upper, e.good).safe, kernel(e.n, e.lower, e.good).safe)

    def test_all_good_and_all_bad(self):
        e = self.env(((0, 1), (1, 2), (2, 0)), good=(0, 1, 2))
        self.assertEqual(classify(e, frozenset({0})), Verdict.PERSISTENT)
        self.assertEqual(classify(replace(e, good=frozenset()), frozenset({0})), Verdict.REFUTED)

    def test_graph_work_counter_is_bounded(self):
        e = self.env(((0, 1), (1, 2), (2, 0), (1, 0)))
        k = kernel(e.n, e.upper, e.good)
        self.assertEqual(k.edge_reads, len(e.upper))
        self.assertLessEqual(k.reverse_edge_visits, len(e.upper))


if __name__ == "__main__":
    unittest.main()
