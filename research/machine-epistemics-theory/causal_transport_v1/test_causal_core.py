"""Exact calibrations and hostile controls. No empirical or independent-review authority."""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations, product
import unittest

from causal_core import (CannotCheck, Equation, SCM, Query, binary_counterfactual_bounds,
                         binding_status, conditional_distribution, conditional_tv_bound,
                         digest, distribution, history_distance, identified_interval, mix,
                         restrict_by_law, restrict_by_observed_event, total_variation,
                         transcript_law, transcript_tv_bound, transport_bound, verify_joint_marginals)


HALF = F(1, 2)
Y1 = (("Y", 1),)
DO1 = (("X", 1),)


def binary_scm(x: tuple[int, ...], y: tuple[int, ...], prior=(HALF, HALF)) -> SCM:
    return SCM(("X", "Y"), ((0, 1), (0, 1)), prior,
               (Equation("X", (), x), Equation("Y", ("X",), y)))


def confounded_pair() -> tuple[SCM, SCM]:
    # Same X=U, different Y: structural X or latent U.
    return binary_scm((0, 1), (0, 1, 0, 1)), binary_scm((0, 1), (0, 0, 1, 1))


def crossworld_pair() -> tuple[SCM, SCM]:
    # Latent U=(treatment coin, response coin); both observed and all X-do laws agree.
    x = (0, 0, 1, 1)
    constant = (0, 0, 1, 1, 0, 0, 1, 1)
    flipping = (0, 1, 1, 0, 0, 1, 1, 0)
    prior = (F(1, 4),) * 4
    return binary_scm(x, constant, prior), binary_scm(x, flipping, prior)


def simplex_grid(size: int, denominator: int) -> tuple[tuple[F, ...], ...]:
    def counts(k: int, left: int):
        if k == 1:
            yield (left,)
        else:
            for a in range(left + 1):
                for tail in counts(k - 1, left - a):
                    yield (a,) + tail
    return tuple(tuple(F(x, denominator) for x in row) for row in counts(size, denominator))


def subsets(n: int):
    for k in range(n + 1):
        yield from combinations(range(n), k)


def calibrate() -> dict[str, int]:
    """Enumerated family sizes are part of the output; arbitrary-size proofs live in THEORY.md."""
    if not __debug__:
        raise CannotCheck("OPTIMIZED_CHECKS_NOT_ALLOWED")
    counts = {k: 0 for k in ("scm_models", "structural_solutions", "normalized_marginals",
                             "counterfactual_queries", "undefined_conditions", "sharp_bound_cells",
                             "response_distributions", "tv_event_checks", "transport_checks",
                             "conditional_checks", "adaptive_laws", "testing_rules", "selective_testing_rules",
                             "sharp_transcript_witnesses")}
    interventions = ({}, {"X": 0}, {"X": 1}, {"Y": 0}, {"Y": 1},
                     {"X": 0, "Y": 0}, {"X": 0, "Y": 1}, {"X": 1, "Y": 0}, {"X": 1, "Y": 1})
    for x in product((0, 1), repeat=2):
        for y in product((0, 1), repeat=4):
            model = binary_scm(x, y)
            counts["scm_models"] += 1
            for do in interventions:
                for u in (0, 1):
                    xx = do.get("X", x[u])
                    yy = do.get("Y", y[2 * u + xx])
                    assert model.solve(u, do) == {"X": xx, "Y": yy}
                    counts["structural_solutions"] += 1
                assert sum(model.marginal(("X", "Y"), intervene=do).values()) == 1
                counts["normalized_marginals"] += 1
            for intervention in ((), (("X", 0),), DO1):
                for factual in product((0, 1), repeat=2):
                    matching = [u for u in (0, 1) if (x[u], y[2 * u + x[u]]) == factual]
                    for wanted in (0, 1):
                        q = Query("CF", (("Y", wanted),), intervention,
                                  (("X", factual[0]), ("Y", factual[1])))
                        if not matching:
                            try:
                                q.evaluate(model)
                            except CannotCheck:
                                counts["undefined_conditions"] += 1
                            else:
                                raise AssertionError("zero-probability CF must be CANNOT_CHECK")
                        else:
                            do = dict(intervention)
                            success = sum(y[2*u + do.get("X", x[u])] == wanted for u in matching)
                            assert q.evaluate(model) == F(success, len(matching))
                            counts["counterfactual_queries"] += 1
    for denominator in range(1, 9):
        cells: dict[tuple[F, F], list[F]] = {}
        for w in simplex_grid(4, denominator):
            # Response types (Y0,Y1): 00,01,10,11, computed independently of SCM/Query.
            p0, p1 = w[2] + w[3], w[1] + w[3]
            counts["response_distributions"] += 1
            if p0 != 1:
                cells.setdefault((p0, p1), []).append(w[1] / (1-p0))
        for (p0, p1), values in cells.items():
            assert binary_counterfactual_bounds(p0, p1) == (min(values), max(values))
            counts["sharp_bound_cells"] += 1
    grid = simplex_grid(3, 4)
    for p, q in product(grid, repeat=2):
        tv = total_variation(p, q)
        for event in subsets(3):
            assert abs(sum(p[i] for i in event) - sum(q[i] for i in event)) <= tv
            counts["tv_event_checks"] += 1
            if sum(p[i] for i in event) and sum(q[i] for i in event):
                lhs = total_variation(conditional_distribution(p, event), conditional_distribution(q, event))
                assert lhs <= conditional_tv_bound(p, q, event)
                counts["conditional_checks"] += 1
    small = simplex_grid(2, 2)
    kernels = tuple(product(small, repeat=2))
    for p, q, k, l in product(simplex_grid(2, 4), simplex_grid(2, 4), kernels, kernels):
        assert total_variation(mix(p, k), mix(q, l)) <= transport_bound(p, q, k, l)
        counts["transport_checks"] += 1
    policy = lambda h: (F(1), F(0)) if not h or h[-1][1] == 0 else (F(0), F(1))
    for a, b in product((F(i, 4) for i in range(5)), repeat=2):
        def channel(theta):
            return lambda h, action: (1-theta, theta) if action == 0 else (theta, 1-theta)
        for horizon in range(5):
            pa, pb = transcript_law(policy, channel(a), horizon), transcript_law(policy, channel(b), horizon)
            tv = history_distance(pa, pb)
            assert tv <= transcript_tv_bound((abs(a-b),) * horizon)
            counts["adaptive_laws"] += 1
            if horizon == 2:
                keys = sorted(set(pa) | set(pb))
                risks = []
                for predictions in product((0, 1), repeat=len(keys)):
                    # Equal-prior binary testing: prediction 1 is an error under model 0.
                    risk = (sum(pa.get(h, F(0)) for h, y in zip(keys, predictions) if y == 1)
                            + sum(pb.get(h, F(0)) for h, y in zip(keys, predictions) if y == 0)) / 2
                    risks.append(risk)
                    assert risk >= (1-tv)/2
                    counts["testing_rules"] += 1
                assert min(risks) == (1-tv)/2
                for decisions in product((0, 1, 2), repeat=len(keys)):
                    # 2 denotes abstention; no false-error bound without a coverage charge.
                    errors = (sum(pa.get(h, F(0)) for h, y in zip(keys, decisions) if y == 1)
                              + sum(pb.get(h, F(0)) for h, y in zip(keys, decisions) if y == 0)) / 2
                    abstain = sum(pa.get(h, F(0)) + pb.get(h, F(0))
                                  for h, y in zip(keys, decisions) if y == 2) / 2
                    assert 2 * errors + abstain >= 1 - tv
                    counts["selective_testing_rules"] += 1
    for epsilon in (F(0), F(1, 4), HALF, F(1)):
        for horizon in range(5):
            same_policy = lambda h: (F(1),)
            c0 = lambda h, a: (1-epsilon, epsilon, F(0))
            c1 = lambda h, a: (1-epsilon, F(0), epsilon)
            tv = history_distance(transcript_law(same_policy, c0, horizon),
                                  transcript_law(same_policy, c1, horizon))
            assert tv == transcript_tv_bound((epsilon,) * horizon)
            counts["sharp_transcript_witnesses"] += 1
    return counts


class CausalTests(unittest.TestCase):
    def test_observation_is_not_intervention(self):
        a, b = confounded_pair()
        self.assertEqual(a.marginal(("X", "Y")), b.marginal(("X", "Y")))
        observed = Query("OBS", Y1, condition=DO1)
        self.assertEqual((observed.evaluate(a), observed.evaluate(b)), (1, 1))
        causal = Query("DO", Y1, DO1)
        self.assertEqual((causal.evaluate(a), causal.evaluate(b)), (1, HALF))
        self.assertEqual(identified_interval((a, b), causal).status, "PARTIAL")

    def test_all_interventions_still_do_not_fix_counterfactual(self):
        a, b = crossworld_pair()
        self.assertEqual(a.marginal(("X", "Y")), b.marginal(("X", "Y")))
        for xv, yv in product((None, 0, 1), repeat=2):
            do = {k: v for k, v in (("X", xv), ("Y", yv)) if v is not None}
            self.assertEqual(a.marginal(("X", "Y"), intervene=do), b.marginal(("X", "Y"), intervene=do))
        q = Query("CF", Y1, DO1, (("X", 0), ("Y", 0)))
        self.assertEqual((q.evaluate(a), q.evaluate(b)), (0, 1))
        self.assertEqual(identified_interval((a, b), q).status, "PARTIAL")

    def test_wrong_world_conditioning_mutant(self):
        _, b = crossworld_pair()
        cf = Query("CF", Y1, DO1, (("Y", 0),))
        mutant = Query("DO", Y1, DO1, (("Y", 0),))
        self.assertEqual(cf.evaluate(b), HALF)
        self.assertEqual(mutant.evaluate(b), 0)

    def test_empty_models_are_conflict_not_vacuous_truth(self):
        r = identified_interval((), Query("DO", Y1, DO1))
        self.assertEqual((r.status, r.lower, r.upper), ("CONFLICT", None, None))
        self.assertTrue(all([]))  # Explicit contrast: generic all(empty) is unsafe here.

    def test_zero_condition_model_is_not_silently_dropped(self):
        a, _ = confounded_pair()
        zero = binary_scm((0, 0), (0, 0, 0, 0))
        q = Query("CF", Y1, DO1, (("Y", 1),))
        self.assertEqual(identified_interval((a, zero), q).status, "CANNOT_CHECK")

    def test_revoking_constraint_reopens_interval(self):
        a, b = confounded_pair()
        q = Query("DO", Y1, DO1)
        restricted = restrict_by_law((a, b), q, F(1))
        before, after = identified_interval(restricted, q), identified_interval((a, b), q)
        self.assertEqual((before.lower, before.upper), (1, 1))
        self.assertEqual((after.lower, after.upper), (HALF, 1))

    def test_duplicate_constraint_adds_no_information(self):
        a, b = confounded_pair()
        q = Query("DO", Y1, DO1)
        once = restrict_by_law((a, b), q, F(1))
        self.assertEqual(once, restrict_by_law(once, q, F(1)))

    def test_single_success_is_not_population_probability_one(self):
        a, b = confounded_pair()
        q = Query("DO", Y1, DO1)
        self.assertEqual(len(restrict_by_observed_event((a, b), q)), 2)
        self.assertEqual(len(restrict_by_law((a, b), q, F(1))), 1)

    def test_sharp_binary_bounds(self):
        self.assertEqual(binary_counterfactual_bounds(HALF, HALF), (0, 1))
        self.assertEqual(binary_counterfactual_bounds(F(1, 4), F(3, 4)), (F(2, 3), 1))
        self.assertEqual(binary_counterfactual_bounds(F(0), HALF), (HALF, HALF))

    def test_impossible_counterfactual_condition(self):
        with self.assertRaises(CannotCheck):
            binary_counterfactual_bounds(F(1), HALF)

    def test_invariance_without_population_match_fails(self):
        k = ((F(1), F(0)), (F(0), F(1)))
        p, q = (F(1), F(0)), (F(0), F(1))
        self.assertEqual(total_variation(mix(p, k), mix(q, k)), 1)
        self.assertEqual(transport_bound(p, q, k, k), 1)

    def test_same_population_without_mechanism_match_fails(self):
        p = (F(1),)
        k, l = ((F(1), F(0)),), ((F(0), F(1)),)
        self.assertEqual(transport_bound(p, p, k, l), 1)
        self.assertEqual(total_variation(mix(p, k), mix(p, l)), 1)

    def test_transport_common_mass_bound_is_sharp(self):
        for eps, eta in product((F(0), F(1, 4), HALF, F(1)), repeat=2):
            p, q = (1-eps, eps, F(0)), (1-eps, F(0), eps)
            k = ((1-eta, eta, F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
            l = ((1-eta, F(0), eta), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
            self.assertEqual(total_variation(mix(p, k), mix(q, l)), 1-(1-eps)*(1-eta))
            self.assertEqual(transport_bound(p, q, k, l), 1-(1-eps)*(1-eta))

    def test_transport_no_alarm(self):
        p = (HALF, HALF)
        k = ((F(1), F(0)), (F(0), F(1)))
        self.assertEqual(transport_bound(p, p, k, k), 0)

    def test_rare_condition_amplification_and_sharpness(self):
        p, q = (F(1, 4), F(0), F(3, 4)), (F(0), F(1, 4), F(3, 4))
        self.assertEqual(total_variation(p, q), F(1, 4))
        self.assertEqual(conditional_tv_bound(p, q, (0, 1)), 1)
        self.assertEqual(total_variation(conditional_distribution(p, (0, 1)), conditional_distribution(q, (0, 1))), 1)

    def test_condition_zero_requires_unknown(self):
        with self.assertRaises(CannotCheck):
            conditional_tv_bound((F(1), F(0)), (HALF, HALF), (1,))

    def test_adaptive_product_not_independence_assumption(self):
        self.assertEqual(transcript_tv_bound((F(1, 4),) * 2), F(7, 16))
        self.assertEqual(transcript_tv_bound(()), 0)

    def test_same_policy_is_load_bearing(self):
        c = lambda h, a: (F(1),)
        p = transcript_law(lambda h: (F(1), F(0)), c, 1)
        q = transcript_law(lambda h: (F(0), F(1)), c, 1)
        self.assertEqual(history_distance(p, q), 1)  # Channel equal, policies different.

    def test_horizon_bound_cannot_be_bypassed(self):
        with self.assertRaises(CannotCheck):
            transcript_law(lambda h: (F(1),), lambda h, a: (F(1),), 9)

    def test_irreversible_action_has_no_general_inverse(self):
        f = {0: 1, 1: 1}
        for g0, g1 in product((0, 1), repeat=2):
            inverse = {0: g0, 1: g1}
            self.assertFalse(all(inverse[f[x]] == x for x in (0, 1)))

    def test_retraction_is_not_world_rollback(self):
        world, log = 0, []
        world = 1
        log.append("set_world_1")
        log.clear()
        self.assertEqual(world, 1)

    def test_model_fingerprint_binds_functions_and_population(self):
        a, b = confounded_pair()
        self.assertNotEqual(a.fingerprint, b.fingerprint)
        self.assertNotEqual(a.fingerprint, replace(a, prior=(F(1, 4), F(3, 4))).fingerprint)
        self.assertEqual(a.fingerprint, replace(a).fingerprint)

    def test_query_fingerprint_binds_causal_kind(self):
        self.assertNotEqual(Query("DO", Y1, DO1).fingerprint, Query("CF", Y1, DO1).fingerprint)

    def test_query_order_is_canonical(self):
        self.assertEqual(Query("OBS", (("Y", 1), ("X", 0))).fingerprint,
                         Query("OBS", (("X", 0), ("Y", 1))).fingerprint)

    def test_model_payload_is_immutable_from_input_lists(self):
        xs = [0, 1]
        equation = Equation("X", [], xs)
        model = SCM(["X"], [[0, 1]], [HALF, HALF], [equation])
        before = model.fingerprint
        xs[0] = 1
        self.assertEqual(model.fingerprint, before)

    def test_dependency_drift_revalidates(self):
        self.assertEqual(binding_status({"policy": "v1"}, {"policy": "v2"}), "REVALIDATE")
        self.assertEqual(binding_status({"policy": "v1"}, {}), "CANNOT_CHECK")
        self.assertEqual(binding_status({}, {}), "CANNOT_CHECK")
        self.assertEqual(binding_status({"policy": "v1"}, {"policy": "v1", "ui": "v2"}), "MATCH")

    def test_digest_does_not_pretend_floats_are_exact(self):
        with self.assertRaises(TypeError):
            digest({"p": 0.1})

    def test_invalid_distributions(self):
        for p in ((), (HALF,), (F(-1), F(2)), (0.5, 0.5)):
            with self.assertRaises(ValueError):
                distribution(p)

    def test_unknown_interventions_rejected(self):
        a, _ = confounded_pair()
        for do in ({"Z": 0}, {"X": 2}, {"X": True}):
            with self.assertRaises(ValueError):
                a.solve(0, do)

    def test_cyclic_equation_rejected(self):
        with self.assertRaises(ValueError):
            SCM(("X",), ((0, 1),), (F(1),), (Equation("X", ("X",), (0, 1)),))

    def test_missing_function_rows_rejected(self):
        with self.assertRaises(ValueError):
            binary_scm((0, 1), (0, 1))

    def test_query_duplicate_fields_rejected(self):
        with self.assertRaises(ValueError):
            Query("OBS", (("Y", 1), ("Y", 0)))

    def test_observation_cannot_smuggle_do(self):
        with self.assertRaises(ValueError):
            Query("OBS", Y1, DO1)

    def test_model_is_not_population_truth(self):
        a, b = confounded_pair()
        q = Query("DO", Y1, DO1)
        # Same perfect data, a singleton class yields certainty; omitted model refutes universal certainty.
        self.assertEqual(identified_interval((a,), q).status, "IDENTIFIED")
        self.assertEqual(identified_interval((a, b), q).status, "PARTIAL")

    def test_pairwise_optimal_couplings_do_not_glue(self):
        domains = ((0, 1), (0, 2), (1, 2))
        # Each pair is TV distance 1/2 apart, but every triple differs in at least two pairs.
        for x, y, z in product(*domains):
            self.assertGreaterEqual(int(x != y) + int(x != z) + int(y != z), 2)
        proposed_sum_of_mismatch = 3 * HALF
        self.assertLess(proposed_sum_of_mismatch, 2)
        # Each requested pair-law is separately normalized with the stated one-variable marginals.
        self.assertTrue(verify_joint_marginals(((0, 1), (0, 2)),
                         {(0, 0): HALF, (1, 2): HALF},
                         {(0,): {(0,): HALF, (1,): HALF}, (1,): {(0,): HALF, (2,): HALF}}))

    def test_global_marginal_witness_positive_and_rejection(self):
        joint = {(0, 0): HALF, (1, 1): HALF}
        marginals = {(0,): {(0,): HALF, (1,): HALF}, (1,): {(0,): HALF, (1,): HALF}}
        self.assertTrue(verify_joint_marginals(((0, 1), (0, 1)), joint, marginals))
        wrong = {(0,): {(0,): F(1)}}
        self.assertFalse(verify_joint_marginals(((0, 1), (0, 1)), joint, wrong))

    def test_joint_witness_invalid_support_rejected(self):
        with self.assertRaises(ValueError):
            verify_joint_marginals(((0, 1),), {(2,): F(1)}, {})

    def test_exact_calibration(self):
        counts = calibrate()
        self.assertEqual(counts["scm_models"], 64)
        self.assertEqual(counts["structural_solutions"], 1152)
        self.assertEqual(counts["transport_checks"], 2025)
        self.assertTrue(all(n > 0 for n in counts.values()))


if __name__ == "__main__":
    unittest.main()
