"""Separate exhaustive tree enumerator, Bellman-certificate checks and hostile fixtures."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations, product
import unittest

from frontier import (CannotCheck, ContractError, Model, Plan, Query, Solver,
                      action_cover, key, masks, memory_frontier, observed_memory_frontier, partitions,
                      replay, verify_certificate, verify_plan)


def model(rows, queries=(), **kwargs):
    return Model(tuple(frozenset(a) for a in rows), tuple(queries),
                 kwargs.get("contract_id", "exact-fixture"), kwargs.get("epoch", "e1"),
                 kwargs.get("closure_id", "finite-enumeration-scope"))


def query(name, outcomes, cost=1):
    return Query(name, tuple(str(o) for o in outcomes), F(cost), "synthetic-channel:" + name)


def tree_costs(m, worlds, remaining):
    """Enumerate costs of all undominated finite test trees, without Solver/cache.

    A deterministic positive-cost test constant on the current world set cannot
    improve an optimum. Once a common action exists, continuing is dominated.
    Every other remaining test and combination of child trees is enumerated.
    """
    if any(all(a in m.allowed[w] for w in worlds) for a in set().union(*m.allowed)):
        return {F(0)}
    costs = set()
    for index in remaining:
        q = m.queries[index]
        groups = {}
        for w in worlds:
            groups.setdefault(q.outcomes[w], []).append(w)
        if len(groups) < 2:
            continue
        children = [tree_costs(m, tuple(ws), remaining - {index}) for ws in groups.values()]
        if all(children):
            costs.update(q.cost + max(cs) for cs in product(*children))
    return costs


def corpus():
    """5488 complete tables: 3 worlds, 3 actions, 2 labelled binary tests (costs 1,2).

    All 7 nonempty allowed-action subsets per world. All binary partitions with
    first-world outcome 0 (outcome-renaming symmetry removed), independently per test.
    This is exhaustive ONLY in this explicitly stated universe, not all models.
    """
    acts = tuple(frozenset(c) for k in range(1, 4) for c in combinations("abc", k))
    outcomes = tuple(("0",) + rest for rest in product("01", repeat=2))
    for rows in product(acts, repeat=3):
        for left, right in product(outcomes, repeat=2):
            yield model(rows, (query("left", left, 1), query("right", right, 2)))


def calibrate():
    counts = {"models": 0, "bellman_cells": 0, "tree_equalities": 0,
              "finite_models": 0, "impossible_models": 0, "world_replays": 0,
              "subset_monotonicity_checks": 0, "cover_frontier_equalities": 0}
    for m in corpus():
        counts["models"] += 1
        s = Solver(m)
        v, p = s.solve()
        costs = tree_costs(m, tuple(m.worlds), frozenset(range(len(m.queries))))
        expected = min(costs) if costs else None
        if v != expected:
            raise AssertionError((m, v, expected))
        counts["tree_equalities"] += 1
        counts["bellman_cells"] += verify_certificate(m, s.certificate())
        if v is None:
            if m.obstruction() is None:
                raise AssertionError("infinity lacks observation obstruction")
            counts["impossible_models"] += 1
        else:
            if m.obstruction() is not None or p is None or verify_plan(m, p) != v:
                raise AssertionError("policy cost/soundness mismatch")
            for w in m.worlds:
                a, c, trace = replay(m, p, w)
                if a not in m.allowed[w] or c > v:
                    raise AssertionError("unsafe/excess-cost replay")
                counts["world_replays"] += 1
            counts["finite_models"] += 1
        for b in masks(m.worlds):
            vb = s.solve(b)[0]
            for c in masks(b):
                vc = s.solve(c)[0]
                if not m.safe(b) <= m.safe(c) or (vb is not None and (vc is None or vc > vb)):
                    raise AssertionError("information monotonicity violated")
                counts["subset_monotonicity_checks"] += 1
        cover = action_cover(m)
        zero_k = min(int(k) for k, v0 in memory_frontier(m)["cost_by_cells"].items() if v0 == "0")
        if cover is None or len(cover) != zero_k:
            raise AssertionError("action-cover theorem violated")
        counts["cover_frontier_equalities"] += 1
    return counts


class FrontierTests(unittest.TestCase):
    def setUp(self):
        self.bit = model(("a", "b"), (query("bit", (0, 1), 2),))

    def test_complete_finite_corpus(self):
        c = calibrate()
        self.assertEqual(c["models"], 5488)
        self.assertEqual(c["bellman_cells"], 38416)
        self.assertEqual(c["tree_equalities"], 5488)

    def test_empty_belief_is_not_vacuous_success(self):
        with self.assertRaises(ContractError):
            self.bit.safe(())

    def test_missing_closure_cannot_check(self):
        with self.assertRaises(CannotCheck):
            Solver(replace(self.bit, closure_id=None)).solve()

    def test_missing_outcome_is_not_negative_evidence(self):
        with self.assertRaises(ContractError):
            self.bit.observe((0, 1), "bit", "missing")

    def test_bad_or_unknown_world(self):
        for world in (-1, 2, True):
            with self.assertRaises(ContractError):
                self.bit.belief((world,))

    def test_budget_is_not_obstruction(self):
        self.assertEqual(Solver(self.bit).decide(F(1))["status"], "BUDGET_INSUFFICIENT")
        self.assertEqual(Solver(self.bit).decide(F(2))["status"], "QUERY_POLICY_READY")
        self.assertIsNone(self.bit.obstruction())

    def test_known_action_needs_no_positive_query_budget(self):
        m = model(("ab", "ac"))
        self.assertEqual(Solver(m).decide(F(0))["status"], "DECISION_READY")

    def test_interface_obstruction(self):
        m = model(("a", "b"), (query("constant", (0, 0)),))
        self.assertEqual(Solver(m).decide(F(100))["status"], "OBSTRUCTION_WITNESSED")
        self.assertEqual(m.obstruction(), frozenset({0, 1}))

    def test_reference_cap_is_not_obstruction(self):
        with self.assertRaises(CannotCheck):
            Solver(self.bit, max_worlds=1)

    def test_unsafe_leaf_mutant(self):
        with self.assertRaises(ContractError):
            verify_plan(self.bit, Plan(action="a"))

    def test_missing_branch_mutant(self):
        bad = Plan(query="bit", branches=(("0", Plan(action="a")),))
        with self.assertRaises(ContractError):
            verify_plan(self.bit, bad)

    def test_duplicate_branch_mutant(self):
        bad = Plan(query="bit", branches=(("0", Plan(action="a")), ("0", Plan(action="a")),
                                          ("1", Plan(action="b"))))
        with self.assertRaises(ContractError):
            verify_plan(self.bit, bad)

    def test_certificate_optimism_mutant(self):
        c = Solver(self.bit).certificate()
        c["values"]["0,1"] = "0"
        with self.assertRaises(ContractError):
            verify_certificate(self.bit, c)

    def test_certificate_empty_denominator_mutant(self):
        c = Solver(self.bit).certificate()
        del c["values"]["0"]
        with self.assertRaises(ContractError):
            verify_certificate(self.bit, c)

    def test_certificate_drift_in_every_semantic_coordinate(self):
        cert = Solver(self.bit).certificate()
        q = self.bit.queries[0]
        changes = (replace(self.bit, contract_id="other"), replace(self.bit, epoch="e2"),
                   replace(self.bit, closure_id="new-closure"),
                   replace(self.bit, allowed=(frozenset("b"), frozenset("b"))),
                   replace(self.bit, queries=(replace(q, outcomes=("1", "0")),)),
                   replace(self.bit, queries=(replace(q, cost=F(3)),)),
                   replace(self.bit, queries=(replace(q, source_id="other"),)))
        for changed in changes:
            with self.assertRaises(ContractError):
                verify_certificate(changed, cert)

    def test_no_unique_coarsest_partition(self):
        m = model(("ab", "bc", "ac"))
        self.assertTrue(all(m.safe(pair) for pair in combinations(m.worlds, 2)))
        self.assertFalse(m.safe())
        adequate = [p for p in partitions(m.worlds) if all(m.safe(c) for c in p)]
        optimal = [p for p in adequate if len(p) == 2]
        self.assertEqual(len(optimal), 3)
        self.assertEqual(len(action_cover(m)), 2)
        self.assertEqual(memory_frontier(m)["cost_by_cells"], {"1": "INFINITY", "2": "0", "3": "0"})

    def test_full_memory_query_frontier(self):
        m = model(( ("00",), ("01",), ("10",), ("11",)),
                  (query("x", (0, 0, 1, 1), 2), query("y", (0, 1, 0, 1), 3)))
        self.assertEqual(memory_frontier(m)["cost_by_cells"], {"1": "5", "2": "2", "3": "2", "4": "0"})

    def test_direct_sum_and_correlated_counterexample(self):
        independent = model((("00",), ("01",), ("10",), ("11",)),
                            (query("x", (0, 0, 1, 1), 2), query("y", (0, 1, 0, 1), 3)))
        coupled = model((("00",), ("11",)), (query("x", (0, 1), 2), query("y", (0, 1), 3)))
        self.assertEqual(Solver(independent).solve()[0], F(5))
        self.assertEqual(Solver(coupled).solve()[0], F(2))
        self.assertEqual(Solver(self.bit).solve()[0] + F(3), F(5))

    def test_revocation_reopens_answer(self):
        before = self.bit.observe(self.bit.worlds, "bit", "0")
        self.assertEqual(self.bit.safe(before), frozenset({"a"}))
        self.assertFalse(self.bit.safe(self.bit.worlds))
        self.assertEqual(Solver(self.bit).solve(before)[0], F(0))
        self.assertEqual(Solver(self.bit).solve()[0], F(2))

    def test_omit_true_world_mutant(self):
        # A closure assumption is load-bearing: the narrowed family says a is safe,
        # but omitted world 1 refutes it. No theorem certifies real-world closure.
        self.assertEqual(self.bit.safe((0,)), frozenset({"a"}))
        self.assertNotIn("a", self.bit.allowed[1])

    def test_empty_allowed_row_proves_no_registered_solution(self):
        m = model(((),))
        self.assertIsNone(Solver(m).solve()[0])
        self.assertIsNone(action_cover(m))

    def test_fail_closed_types_and_costs(self):
        for cost in (F(0), F(-1), 1.0, True):
            with self.assertRaises(ContractError):
                Query("q", ("0",), cost, "source")
        with self.assertRaises(ContractError):
            model(("a", "b"), (query("q", (0,)),))
        with self.assertRaises(ContractError):
            model(("a", "b"), (query("q", (0, 1)), query("q", (1, 0))))

    def test_pairwise_compatibility_false_green_mutant(self):
        m = model(("ab", "bc", "ac"))
        mutant_accepts = all(m.safe(pair) for pair in combinations(m.worlds, 2))
        self.assertTrue(mutant_accepts)
        self.assertFalse(m.safe())

    def test_exact_fractional_cost(self):
        m = model(("a", "b"), (query("q", (0, 1), F(1, 3)),))
        s = Solver(m)
        self.assertEqual(s.solve()[0], F(1, 3))
        self.assertEqual(s.decide(F(1, 4))["status"], "BUDGET_INSUFFICIENT")
        self.assertEqual(verify_certificate(m, s.certificate()), 3)

    def test_shared_information_uses_matched_interface(self):
        common = (query("x", (0, 1), 2), query("y", (0, 1), 3))
        left = model(("a", "b"), common)
        right = model(("c", "d"), common)
        joint = model((("ac",), ("bd",)), common)
        v1, v2, v12 = (Solver(m).solve()[0] for m in (left, right, joint))
        self.assertEqual((v1, v2, v12), (F(2), F(2), F(2)))
        self.assertLessEqual(max(v1, v2), v12)
        self.assertLessEqual(v12, v1 + v2)

    def test_product_sum_bound_with_common_interface(self):
        common = (query("x", (0, 0, 1, 1), 2), query("y", (0, 1, 0, 1), 3))
        left = model(("a", "a", "b", "b"), common)
        right = model(("c", "d", "c", "d"), common)
        joint = model((("ac",), ("ad",), ("bc",), ("bd",)), common)
        self.assertEqual(tuple(Solver(m).solve()[0] for m in (left, right, joint)), (F(2), F(3), F(5)))

    def test_new_channel_can_remove_obstruction(self):
        old = model(("a", "b"), (query("constant", (0, 0)),))
        new = replace(old, queries=old.queries + (query("new", (0, 1), 4),))
        self.assertIsNotNone(old.obstruction())
        self.assertIsNone(new.obstruction())
        self.assertEqual(Solver(new).solve()[0], F(4))

    def test_bad_certificate_types(self):
        with self.assertRaises(ContractError):
            verify_certificate(self.bit, None)
        cert = Solver(self.bit).certificate()
        cert["values"] = []
        with self.assertRaises(ContractError):
            verify_certificate(self.bit, cert)
        with self.assertRaises(ContractError):
            verify_plan(self.bit, None)

    def test_noiseless_channel_assumption_not_noise_guarantee(self):
        # Model-perfect observations are assumed. A wrong registered outcome
        # gives a false belief and can invalidate the decision in the actual world.
        wrong_belief = self.bit.observe((0, 1), "bit", "0")
        self.assertIn("a", self.bit.safe(wrong_belief))
        self.assertNotIn("a", self.bit.allowed[1])

    def test_encoder_cannot_read_unobserved_world(self):
        no_queries = model(("a", "b"))
        self.assertEqual(memory_frontier(no_queries)["cost_by_cells"]["2"], "0")
        observed = observed_memory_frontier(no_queries, ("same", "same"))
        self.assertEqual(observed["cost_by_cells"], {"1": "INFINITY"})
        self.assertIsNone(observed["zero_query_cover"])
        self.assertEqual(observed_memory_frontier(self.bit, ("same", "same"))["cost_by_cells"], {"1": "2"})

    def test_observed_encoder_identity_recovers_full_frontier(self):
        m = model((("00",), ("01",), ("10",), ("11",)),
                  (query("x", (0, 0, 1, 1), 2), query("y", (0, 1, 0, 1), 3)))
        full = observed_memory_frontier(m, ("00", "01", "10", "11"))
        partial = observed_memory_frontier(m, ("0", "1", "0", "1"))
        self.assertEqual(full["cost_by_cells"], memory_frontier(m)["cost_by_cells"])
        self.assertEqual(partial["cost_by_cells"], {"1": "5", "2": "2"})
        self.assertIsNone(partial["zero_query_cover"])

    def test_observed_encoder_bad_signal_and_cap(self):
        for signal in ((), ("0",), ["0", "1"], (0, 1)):
            with self.assertRaises(ContractError):
                observed_memory_frontier(self.bit, signal)
        with self.assertRaises(CannotCheck):
            observed_memory_frontier(self.bit, ("0", "1"), max_signals=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
