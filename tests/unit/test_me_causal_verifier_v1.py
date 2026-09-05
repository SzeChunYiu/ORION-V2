"""Exact foundation tests and eight falsifier-sensitive, applied mutants."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HOME = ROOT / "research/machine-epistemics-theory/causal_verifier_v1"
SPEC = importlib.util.spec_from_file_location("me_causal_verifier_v1", HOME / "causal_verifier.py")
cv = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cv
SPEC.loader.exec_module(cv)
Q = cv.Q


class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.cause = cv.SCM((0, 1), (0, 0, 1, 1))
        self.confound = cv.SCM((0, 1), (0, 1, 0, 1))
        self.e = cv.law_evidence(self.cause)

    def test_model_universe(self):
        self.assertEqual(len(set(cv.models())), 64)

    def test_hierarchy_counts_and_witnesses(self):
        r = cv.check_hierarchy()
        self.assertEqual([r[k] for k in ("observational_classes", "interventional_classes",
                                        "counterfactual_response_classes")], [10, 34, 36])
        self.assertEqual(r["model_pairs"], 4096)

    def test_counterfactual_reopens_without_losing_causal_effect(self):
        rows = cv.revision_trace()
        self.assertEqual([r["P_Y0_equals_Y1_is_1"] for r in rows],
                         ["UNKNOWN", "SUPPORTED", "UNKNOWN", "SUPPORTED"])
        self.assertTrue(all(r["P_Y1_do_X1_is_half"] == "SUPPORTED" for r in rows))

    def test_two_oracle_paths(self):
        self.assertEqual(cv.check_alternate_oracle()["structural_vs_response_pushforward"], 576)

    def test_lifecycle_all_subsets(self):
        r = cv.check_lifecycle()
        self.assertEqual(r["positive_negative_retraction_checks"], 24576)
        self.assertEqual(sum(r["verdict_counts"].values()), 12288)
        self.assertGreater(r["verdict_counts"]["UNKNOWN"], 0)

    def test_supported_refuted_unknown(self):
        self.assertEqual(cv.assess((self.e[2],), "Y1_do_X1", Q(1)), "SUPPORTED")
        self.assertEqual(cv.assess((self.e[2],), "Y1_do_X1", Q(0)), "REFUTED")
        self.assertEqual(cv.assess((self.e[0],), "Y1_do_X1", Q(1)), "UNKNOWN")

    def test_inconsistent_is_not_truth(self):
        other = cv.Evidence("conflict", "EXACT_DISTRIBUTION",
                            self.confound.distribution((1, None)), (1, None))
        self.assertEqual(cv.assess((self.e[2], other), "Y1_do_X1", Q(1)), "INCONSISTENT")
        with self.assertRaisesRegex(ValueError, "INCONSISTENT_BASE"):
            cv.minimal_supports((self.e[2], other), "Y1_do_X1", Q(1))

    def test_no_model_class_is_cannot_check(self):
        with self.assertRaises(cv.CannotCheck):
            cv.compatible((), family=())

    def test_unregistered_query_is_cannot_check(self):
        with self.assertRaises(cv.CannotCheck):
            cv.assess((), "unregistered", Q(1))

    def test_scope_is_checked(self):
        with self.assertRaisesRegex(cv.CannotCheck, "SCOPE_MISMATCH"):
            cv.assess(self.e, "Y1_do_X1", Q(1), scope="target")

    def test_duplicate_id_conflict(self):
        a = cv.Evidence("same", "OBSERVED_EVENT", (0, 0))
        b = cv.Evidence("same", "OBSERVED_EVENT", (1, 1))
        with self.assertRaisesRegex(ValueError, "EVIDENCE_ID_COLLISION"):
            cv.compatible((a, b))

    def test_duplicate_same_record_is_idempotent(self):
        self.assertEqual(cv.compatible((self.e[0],)), cv.compatible((self.e[0], self.e[0])))
        self.assertEqual(cv.minimal_supports((self.e[2], self.e[2]), "Y1_do_X1", Q(1)),
                         (frozenset({"do1"}),))

    def test_alternative_support_retention(self):
        duplicate_source = cv.Evidence("other_source", "EXACT_DISTRIBUTION",
                                       self.e[2].payload, (1, None))
        supports = cv.minimal_supports((self.e[2], duplicate_source), "Y1_do_X1", Q(1))
        self.assertEqual(set(supports), {frozenset({"do1"}), frozenset({"other_source"})})
        self.assertTrue(cv.survives(supports, {"do1"}))
        self.assertFalse(cv.survives(supports, {"do1", "other_source"}))
        # Logical alternatives are not a claim of statistical independence.

    def test_illformed_scm(self):
        for f, g in [((True, 1), (0, 0, 1, 1)), ((0,), (0, 0, 1, 1)),
                     ((0, 1), (0, 2, 1, 1))]:
            with self.subTest(f=f, g=g), self.assertRaises(ValueError):
                cv.SCM(f, g)

    def test_illformed_evidence(self):
        for kind, payload in [("UNKNOWN_KIND", ()), ("OBSERVED_EVENT", (True, 1)),
                              ("EXACT_DISTRIBUTION", (Q(0),) * 4),
                              ("EXACT_DISTRIBUTION", (Q(-1), Q(2), Q(0), Q(0)))]:
            with self.subTest(kind=kind, payload=payload), self.assertRaises(ValueError):
                cv.Evidence("bad", kind, payload)

    def test_sample_law_fidelity_transport_boundaries(self):
        r = cv.check_boundaries()
        self.assertEqual(r["sample_compatible_models"], 28)
        self.assertEqual(r["full_observation_law_compatible_models"], 8)

    def test_sharp_coupling_sweep(self):
        r = cv.check_couplings()
        self.assertEqual(r["all_16_boolean_event_bound_checks"], 4544)
        self.assertEqual(r["feasible_integer_tables"], 494)

    def test_non_independent_error(self):
        self.assertEqual(cv.joint_bounds(Q(1, 20), Q(1, 20), (0, 0, 0, 1)), (0, Q(1, 20)))
        self.assertEqual(cv.coupling_table(Q(1, 20), Q(1, 20), Q(1, 20)),
                         (Q(19, 20), 0, 0, Q(1, 20)))

    def test_bad_couplings_refused(self):
        with self.assertRaises(ValueError):
            cv.coupling_table(Q(1, 2), Q(1, 2), Q(3, 4))
        with self.assertRaises(ValueError):
            cv.joint_bounds(Q(-1), Q(1, 2), (0, 0, 0, 1))
        with self.assertRaises(ValueError):
            cv.joint_bounds(Q(1, 2), Q(1, 2), (0, 0, 0, True))

    def test_no_claim_promotion(self):
        r = cv.calibration()
        self.assertFalse(r["full_foundation_closed"])
        self.assertEqual(r["independent_review"], "NOT_OBTAINED")
        self.assertFalse(r["general_causal_discovery_or_real_llm_claim"])

    def test_calibration_body_and_hash(self):
        result = cv.calibration()
        result["body_sha256"] = cv.digest(result)
        self.assertEqual(json.loads((HOME / "CALIBRATION.json").read_text()), result)

    def test_cli_fail_and_cannot_check(self):
        for control, code in [("fail", 1), ("cannot-check", 2)]:
            p = subprocess.run([sys.executable, "-O", str(HOME / "causal_verifier.py"),
                                "--control", control], capture_output=True, text=True)
            self.assertEqual(p.returncode, code, p.stdout + p.stderr)
            self.assertEqual(json.loads(p.stdout)["status"], "FAIL" if code == 1 else "CANNOT_CHECK")

    def test_cli_verification_and_drift(self):
        p = subprocess.run([sys.executable, str(HOME / "causal_verifier.py"), "--verify",
                            str(HOME / "CALIBRATION.json")], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "drift.json"
            f.write_text('{}')
            p = subprocess.run([sys.executable, str(HOME / "causal_verifier.py"), "--verify", str(f)],
                                capture_output=True, text=True)
            self.assertEqual(p.returncode, 1)
            self.assertEqual(json.loads(p.stdout)["reason"], "CALIBRATION_DRIFT")

    def test_mutant_vacuous_certainty(self):
        original = cv.classify_family
        def bad(family, query, value):
            return "SUPPORTED" if not family else original(family, query, value)
        with patch.object(cv, "classify_family", bad), self.assertRaisesRegex(ValueError, "vacuous certainty"):
            cv.check_boundaries()

    def test_mutant_scope_bypass(self):
        with patch.object(cv, "validate_evidence", lambda e, s: None):
            with self.assertRaisesRegex(ValueError, "source evidence applied to target"):
                cv.check_boundaries()

    def test_mutant_counterfactual_independence(self):
        original = cv.query_value
        def bad(model, query):
            if query == "Y0_equals_Y1":
                p, q = original(model, "Y1_do_X0"), original(model, "Y1_do_X1")
                return p * q + (1-p) * (1-q)
            return original(model, query)
        with patch.object(cv, "query_value", bad):
            with self.assertRaisesRegex(ValueError, "counterfactual separation"):
                cv.check_hierarchy()

    def test_mutant_verifier_independence(self):
        with patch.object(cv, "joint_bounds", lambda p, q, e: (p*q, p*q)):
            with self.assertRaisesRegex(ValueError, "sharp coupling bounds"):
                cv.check_couplings()

    def test_mutant_ignores_revocation(self):
        with patch.object(cv, "survives", lambda supports, revoked: bool(supports)):
            with self.assertRaisesRegex(ValueError, "retraction"):
                cv.check_lifecycle()

    def test_mutant_alternate_oracle_swaps_coordinates(self):
        original = cv.distribution_from_response_law
        def bad(law, intervention):
            return original(law, intervention)[::-1]
        with patch.object(cv, "distribution_from_response_law", bad):
            with self.assertRaisesRegex(ValueError, "ORACLE_DISAGREEMENT"):
                cv.check_alternate_oracle()

    def test_mutant_sample_mints_distribution(self):
        original = cv.Evidence.matches
        def bad(record, model):
            if record.kind == "OBSERVED_EVENT":
                x, y = record.payload
                return model.distribution(record.intervention)[2*x+y] == 1
            return original(record, model)
        with patch.object(cv.Evidence, "matches", bad):
            with self.assertRaisesRegex(ValueError, "sample/distribution distinction"):
                cv.check_boundaries()

    def test_mutant_observation_substituted_for_intervention(self):
        original = cv.Evidence.matches
        def bad(record, model):
            if record.kind == "EXACT_DISTRIBUTION":
                return model.distribution() == record.payload
            return original(record, model)
        with patch.object(cv.Evidence, "matches", bad):
            with self.assertRaisesRegex(ValueError, "INCONSISTENT_BASE_FOR_MONOTONE_PROVENANCE"):
                cv.check_lifecycle()


if __name__ == "__main__":
    unittest.main(verbosity=2)
