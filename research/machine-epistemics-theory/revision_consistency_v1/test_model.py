"""Synthetic hostile controls. No production endpoint, credential or exploit is used."""
from dataclasses import replace
from itertools import product
import copy
import unittest

from model import (Cell, State, Spec, Verdict, CheckerRecord, certificate, checkpoint,
                   model_check, validate, parent_validate, validation_cost, commit_record,
                   read_view, evaluate, write_skew, schedules, build_log, replay,
                   closed_cut, ancestor_cut, descriptor_sufficient)


def fixture():
    values = {"evidence": "LIVE", "implementation": "i1", "model": "m1", "prompt": "p1",
              "decoder": "d1", "checker": "k1", "schema": "s1", "assumptions": "a1",
              "policy": "r1", "scope": "x", "authority:commit": "GRANTED"}
    spec = Spec("claim:1", "payload:1", tuple(sorted((k, v) for k, v in values.items()
                                                  if k != "authority:commit")))
    state = State.of(values)
    record = model_check(spec, state)
    return spec, state, certificate(spec, state, record), {record.identifier: record}


class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.spec, self.initial, self.cert, self.records = fixture()

    def verdict(self, current=None, **kwargs):
        opts = {"current_cut_known": True, "budget": validation_cost(self.spec)}
        opts.update(kwargs)
        return validate(self.cert, self.spec, self.initial,
                        current or self.initial, self.records, **opts)

    def test_unchanged_commits_at_a_named_cut(self):
        row = commit_record(self.cert, self.spec, self.initial, self.initial, self.records,
                            current_cut_known=True, budget=validation_cost(self.spec))
        self.assertTrue(row["committed"])
        self.assertEqual(row["linearization_sequence"], 0)
        self.assertEqual(row["effect"], "NONE_MODEL_ONLY")

    def test_every_influential_coordinate_reopens(self):
        for key in self.spec.required:
            with self.subTest(key=key):
                changed = self.initial.change(key, "CHANGED")
                self.assertNotEqual(changed, self.initial)
                self.assertEqual(self.verdict(changed), Verdict.REOPEN)

    def test_unrelated_changes_are_no_alarm(self):
        changed = self.initial.change("unrelated", "new")
        self.assertNotEqual(changed.fingerprint, self.initial.fingerprint)
        self.assertEqual(self.verdict(changed), Verdict.PASS)

    def test_aba_requires_revalidation_not_reuse(self):
        changed = self.initial.change("evidence", "REVOKED").change("evidence", "LIVE")
        self.assertEqual(evaluate(self.spec, changed), Verdict.PASS)
        self.assertEqual(self.verdict(changed), Verdict.REOPEN)

    def test_revalidated_aba_is_usable_with_new_lineage(self):
        state = self.initial.change("evidence", "REVOKED").change("evidence", "LIVE")
        rec = model_check(self.spec, state)
        cert = certificate(self.spec, state, rec)
        self.assertNotEqual(cert.identifier, self.cert.identifier)
        self.assertEqual(validate(cert, self.spec, state, state, {rec.identifier: rec},
                                 current_cut_known=True, budget=validation_cost(self.spec)), Verdict.PASS)

    def test_new_negative_dependency_is_a_phantom(self):
        changed = self.initial.change("conflict/new", "BLOCK")
        old_positive = tuple(x for x in read_view(self.spec, self.initial) if x[0] == "cell")
        new_positive = tuple(x for x in read_view(self.spec, changed) if x[0] == "cell")
        self.assertEqual(old_positive, new_positive)  # planted positive-reads-only mutant
        self.assertEqual(evaluate(self.spec, changed), Verdict.FAIL)
        self.assertEqual(self.verdict(changed), Verdict.REOPEN)

    def test_unknown_predicate_generation_cannot_check(self):
        state = replace(self.initial, predicates=())
        rec = model_check(self.spec, state)
        self.assertEqual(rec.verdict, Verdict.CANNOT_CHECK)

    def test_unknown_conflict_is_not_absence(self):
        self.assertEqual(evaluate(self.spec, self.initial.change("conflict/new", None)), Verdict.CANNOT_CHECK)

    def test_absence_predicate_no_alarm(self):
        self.assertEqual(evaluate(self.spec, self.initial.change("conflict/new", "CLEARED")), Verdict.PASS)

    def test_no_checker_record_cannot_check(self):
        self.assertEqual(validate(self.cert, self.spec, self.initial, self.initial, {},
                                 current_cut_known=True, budget=validation_cost(self.spec)), Verdict.CANNOT_CHECK)

    def test_missing_history_cannot_check(self):
        self.assertEqual(validate(self.cert, self.spec, None, self.initial, self.records,
                                 current_cut_known=True, budget=validation_cost(self.spec)), Verdict.CANNOT_CHECK)

    def test_checker_cannot_check_does_not_promote(self):
        rec = model_check(self.spec, self.initial, available=False)
        cert = certificate(self.spec, self.initial, rec)
        self.assertEqual(validate(cert, self.spec, self.initial, self.initial,
                                 {rec.identifier: rec}, current_cut_known=True,
                                 budget=validation_cost(self.spec)), Verdict.CANNOT_CHECK)

    def test_checker_failure_is_preserved(self):
        state = self.initial.change("evidence", "REVOKED")
        rec = model_check(self.spec, state)
        cert = certificate(self.spec, state, rec)
        self.assertEqual(validate(cert, self.spec, state, self.initial, {rec.identifier: rec},
                                 current_cut_known=True, budget=validation_cost(self.spec)), Verdict.FAIL)

    def test_missing_authority_is_not_created_by_receipt(self):
        state = self.initial.change("authority:commit", None)
        self.assertEqual(evaluate(self.spec, state), Verdict.CANNOT_CHECK)
        state = self.initial.change("authority:commit", "DENIED")
        rec = model_check(self.spec, state)
        row = commit_record(certificate(self.spec, state, rec), self.spec, state, state,
                            {rec.identifier: rec}, current_cut_known=True,
                            budget=validation_cost(self.spec))
        self.assertFalse(row["committed"])

    def test_historical_success_without_fresh_cut_is_unknown(self):
        self.assertEqual(self.verdict(current_cut_known=False), Verdict.CANNOT_CHECK)

    def test_budget_cannot_be_omitted_or_boolean(self):
        self.assertEqual(self.verdict(budget=0), Verdict.CANNOT_CHECK)
        self.assertEqual(self.verdict(budget=validation_cost(self.spec)-1), Verdict.CANNOT_CHECK)
        with self.assertRaises(ValueError):
            self.verdict(budget=True)

    def test_subject_and_payload_are_bound(self):
        for changed in (replace(self.spec, subject="claim:2"), replace(self.spec, payload="payload:2")):
            self.assertEqual(validate(self.cert, changed, self.initial, self.initial, self.records,
                                     current_cut_known=True, budget=100), Verdict.FAIL)

    def test_incomplete_certificate_view_fails(self):
        bad = replace(self.cert, reads=self.cert.reads[:-1])
        self.assertNotEqual(bad, self.cert)
        self.assertEqual(validate(bad, self.spec, self.initial, self.initial, self.records,
                                 current_cut_known=True, budget=100), Verdict.FAIL)

    def test_checker_record_binding_and_identity(self):
        rec = next(iter(self.records.values()))
        for bad in (replace(rec, specification="wrong"), replace(rec, historical_state="wrong")):
            records = {self.cert.checker_record: bad}
            self.assertEqual(validate(self.cert, self.spec, self.initial, self.initial, records,
                                     current_cut_known=True, budget=100), Verdict.FAIL)

    def test_invalid_checker_terminal_rejected(self):
        with self.assertRaises(ValueError):
            CheckerRecord("s", "h", "NEUTRAL")

    def test_shallow_descriptor_omits_backend(self):
        self.assertFalse(descriptor_sufficient((0, 0), (True, False)))
        self.assertTrue(descriptor_sufficient((0, 1), (True, False)))
        self.assertTrue(descriptor_sufficient((0, 0), (True, True)))

    def test_write_skew_and_serial_control(self):
        cases = schedules()
        self.assertEqual(len(cases), 6)
        self.assertEqual(sum(not any(write_skew(s, validate_full_read_set=False)) for s in cases), 4)
        self.assertTrue(all(any(write_skew(s, validate_full_read_set=True)) for s in cases))
        self.assertTrue(any(write_skew(("r0", "w0", "r1", "w1"), validate_full_read_set=False)))

    def test_check_use_race_is_not_atomic_commit(self):
        checked = self.verdict() is Verdict.PASS
        current = self.initial.change("evidence", "REVOKED")
        self.assertTrue(checked)  # cached approval is the planted separated-step mutant
        self.assertEqual(evaluate(self.spec, current), Verdict.FAIL)
        self.assertEqual(self.verdict(current), Verdict.REOPEN)

    def test_log_replay_and_unknown_anchor(self):
        changes = (("evidence", "REVOKED"), ("evidence", "LIVE"))
        log = build_log(self.initial, changes)
        verdict, state = replay(self.initial, log, checkpoint(self.initial, log))
        self.assertEqual(verdict, Verdict.PASS)
        expected = self.initial
        for key, value in changes:
            expected = expected.change(key, value)
        self.assertEqual(state, expected)
        self.assertEqual(replay(self.initial, log, None)[0], Verdict.CANNOT_CHECK)

    def test_truncated_prefix_requires_external_anchor(self):
        log = build_log(self.initial, (("evidence", "REVOKED"), ("scope", "other")))
        self.assertEqual(replay(self.initial, log[:1], checkpoint(self.initial, log))[0], Verdict.FAIL)
        self.assertEqual(replay(self.initial, log[:1], checkpoint(self.initial, log[:1]))[0], Verdict.PASS)
        # The latter is a valid OLD prefix; it is not the current complete history.

    def test_log_mutations_are_applied_and_detected(self):
        log = build_log(self.initial, (("evidence", "REVOKED"), ("scope", "other")))
        bad = copy.deepcopy(log)
        bad[0]["value"] = "LIVE"
        self.assertNotEqual(bad, log)
        self.assertEqual(replay(self.initial, bad, checkpoint(self.initial, log))[0], Verdict.FAIL)
        self.assertEqual(replay(self.initial, tuple(reversed(log)), checkpoint(self.initial, log))[0], Verdict.FAIL)
        changed = build_log(self.initial, (("evidence", "LIVE"), ("scope", "other")))
        self.assertEqual(replay(self.initial, changed, checkpoint(self.initial, log))[0], Verdict.FAIL)

    def test_log_genesis_binds_initial_snapshot(self):
        log = build_log(self.initial, (("evidence", "REVOKED"),))
        other = self.initial.change("model", "wrong")
        self.assertEqual(replay(other, log, checkpoint(self.initial, log))[0], Verdict.FAIL)
        self.assertEqual(replay(other, (), checkpoint(self.initial, ()))[0], Verdict.FAIL)

    def test_sequence_boolean_is_not_sequence_one(self):
        log = build_log(self.initial, (("evidence", "REVOKED"),))
        bad = copy.deepcopy(log)
        bad[0]["sequence"] = True
        self.assertEqual(replay(self.initial, bad, checkpoint(self.initial, log))[0], Verdict.FAIL)

    def test_causal_cut_and_joint_invariant_are_distinct(self):
        self.assertFalse(closed_cut(((), (0,)), frozenset({1})))
        self.assertTrue(closed_cut(((), (0,)), frozenset({0, 1})))
        self.assertTrue(closed_cut(((), ()), frozenset({0, 1})))
        self.assertFalse(any(write_skew(("r0", "r1", "w0", "w1"), validate_full_read_set=False)))

    def test_bad_causal_input_not_silently_true(self):
        with self.assertRaises(ValueError):
            closed_cut(((1,), (0,)), frozenset())
        with self.assertRaises(ValueError):
            closed_cut(((),), frozenset({4}))

    def test_post_effect_crash_has_two_indistinguishable_histories(self):
        histories = [(('intent:1',), False), (('intent:1',), True)]
        self.assertEqual(histories[0][0], histories[1][0])
        self.assertNotEqual(histories[0][1], histories[1][1])
        self.assertEqual(len({effect for log, effect in histories if log == ('intent:1',)}), 2)

    def test_schema_and_canonicalization(self):
        self.assertEqual(State.of({"b": "1", "a": "2"}), State.of({"a": "2", "b": "1"}))
        with self.assertRaises(ValueError):
            Cell("x", True)
        with self.assertRaises(ValueError):
            State((("a", Cell("1")), ("a", Cell("2"))))
        with self.assertRaises(ValueError):
            Spec("s", "p", (("x", "1"), ("x", "2")))

    def test_candidate_and_parent_agree_on_all_small_states(self):
        spec = Spec("s", "p", (("a", "LIVE"), ("b", "LIVE")))
        states = [State.of(dict(zip(("a", "b", "authority:commit"), values)))
                  for values in product(("LIVE", "GRANTED", None), repeat=3)]
        for old, now in product(states, repeat=2):
            rec = model_check(spec, old)
            cert = certificate(spec, old, rec)
            args = (cert, spec, old, now, {rec.identifier: rec})
            for known in (False, True):
                kw = {"current_cut_known": known, "budget": 20}
                self.assertEqual(validate(*args, **kw), parent_validate(*args, **kw))


    def test_unknown_freshness_string_is_not_a_true_oracle(self):
        for bad in ("UNKNOWN", 1, None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.verdict(current_cut_known=bad)

    def test_boolean_event_id_is_not_integer_identity(self):
        with self.assertRaises(ValueError):
            closed_cut(((), ()), frozenset({True}))

    def test_nonstring_subject_is_not_a_certificate_subject(self):
        for subject, payload in ((True, "p"), ("s", 1)):
            with self.subTest(subject=subject), self.assertRaises(ValueError):
                Spec(subject, payload, ())

    def test_nonstring_predicate_is_a_typed_rejection(self):
        with self.assertRaises(ValueError):
            Spec("s", "p", (), absent_prefix=4)


if __name__ == "__main__":
    unittest.main()
