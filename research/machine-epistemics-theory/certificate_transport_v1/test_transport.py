"""Fast boundary tests; checks.py owns the separately frozen exhaustive grid."""
from fractions import Fraction as Q
import unittest
from transport import *


class TransportTests(unittest.TestCase):
    def test_empty_and_full_events(self):
        self.assertEqual(fixed_event((1,), 0, 1).risk, 0)
        self.assertEqual(fixed_event((1,), 1, 1).risk, 1)

    def test_exact_witness(self):
        p = (Q(1, 4), Q(3, 4))
        result = fixed_event(p, 1, Q(1, 4))
        self.assertEqual(result.attaining_distribution, (Q(1, 2), Q(1, 2)))
        self.assertEqual(tv(p, result.attaining_distribution), Q(1, 4))

    def test_zero_mass_is_not_impossible(self):
        self.assertEqual(fixed_event((1, 0), 2, Q(1, 4)).risk, Q(1, 4))

    def test_no_event_change_is_identity(self):
        self.assertEqual(joint_frontier((Q(1,4), Q(3,4)), 1, 0, 0, 0).bound.risk, Q(1,4))

    def test_granularity(self):
        self.assertEqual(joint_frontier((Q(2,5), Q(3,5)), 0, 3, 0, Q(1,2)).bound.risk, Q(2,5))

    def test_mutable_scope(self):
        self.assertEqual(joint_frontier((Q(1,4), Q(3,4)), 0, 1, 0, 1).bound.risk, Q(1,4))

    def test_audit_revocation(self):
        p = (Q(1,4), Q(3,4))
        self.assertEqual(audit_bound(p, 0, 3, 3, 0).risk, 0)
        self.assertEqual(audit_bound(p, 0, 3, 2, 0).risk, Q(1,4))

    def test_parent_zero_mass_tie(self):
        before = audit_knapsack((1,0), 0, 2, Q(1,4), (1,1), 0)
        after = audit_knapsack((1,0), 0, 2, Q(1,4), (1,1), 1)
        self.assertEqual((before.bound.risk, after.bound.risk), (Q(1,4), Q(0)))

    def test_parent_does_not_spend_on_plateau(self):
        result = audit_knapsack((Q(1,2),Q(1,2)), 3, 3, 1, (1,1), 2)
        self.assertEqual((result.bound.risk, result.cost), (Q(1), 0))

    def test_bad_inputs(self):
        for p in ((), (Q(1,2),), (-1,2), (True,0), (0.5,0.5)):
            with self.subTest(p=p), self.assertRaises(ValueError):
                fixed_event(p, 0, 0)
        for b in (-1, 4, True):
            with self.assertRaises(ValueError): fixed_event((1,0), b, 0)
        with self.assertRaises(ValueError): fixed_event((1,0), 1, "nan")
        with self.assertRaises(ValueError): audit_bound((1,0), 0, 1, 2, 0)

    def test_caps_are_cannot_check(self):
        with self.assertRaises(CannotCheck): fixed_event((1,)+(0,)*MAX_ATOMS, 0, 0)
        with self.assertRaises(CannotCheck): audit_knapsack((1,), 0, 1, 0, (1,), MAX_DP_BUDGET+1)

    def test_integer_cost_contract(self):
        for costs in ((0,1), (-1,1), (1.0,1), (True,1), (1,)):
            with self.assertRaises(ValueError): audit_knapsack((1,0), 0, 3, 0, costs, 2)
        with self.assertRaises(ValueError): audit_knapsack((1,0), 0, 3, 0, (1,1), True)

    def test_binding_is_not_validity(self):
        m = {k: "id:"+k for k in MANIFEST_FIELDS}; m["claim_kind"] = "RISK_BOUND"
        self.assertEqual(binding_status(m,m,["e"]), "BINDING_MATCH_ONLY")
        self.assertEqual(binding_status(m,m,["e"],["e"]), "REVALIDATE")
        self.assertEqual(binding_status(m,m,[]), "CANNOT_CHECK")
        for key in MANIFEST_FIELDS:
            changed = dict(m); changed[key] += "-changed"
            self.assertNotEqual(manifest_digest(m), manifest_digest(changed))
            self.assertNotEqual(binding_status(m,changed,["e"]), "BINDING_MATCH_ONLY")
        missing = dict(m); del missing["checker_artifact"]
        self.assertEqual(binding_status(m,missing,["e"]), "CANNOT_CHECK")

    def test_claim_kind_not_coerced(self):
        m = {k: "id:"+k for k in MANIFEST_FIELDS}; m["claim_kind"] = "EXACT_TRUTH"
        self.assertEqual(binding_status(m,m,["e"]), "WRONG_CLAIM_KIND")


if __name__ == "__main__":
    unittest.main()
