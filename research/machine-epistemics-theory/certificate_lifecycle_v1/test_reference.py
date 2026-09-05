"""Deterministic calibration and counterexamples; no protected empirical claims."""
from dataclasses import replace
import itertools
import unittest
import reference as m

COUNTS = {}

def count(name):
    COUNTS[name] = COUNTS.get(name, 0) + 1


def h(text):
    return m.digest("fixture", text)


def root(text):
    return "root:" + h(text)


def cert(name="a", kind="EXACT_OBJECT", supports=((),), bindings=()):
    return m.Certificate("cert:" + name, kind, h("statement:" + name), h("subject:" + name),
                         h("proof:" + name), h("checker"), bindings, supports)


def state(registry, roots=None, context=None):
    facts = {key: "VALID" for c in registry for key in
             (m.judgment_key(registry, c), m.trust_key(c))}
    facts.update(roots or {})
    return m.Snapshot(0, m.registry_id(registry), tuple(sorted((context or {}).items())),
                      tuple(sorted(facts.items())), h("genesis"))


def use(s, c, **change):
    data = {"certificate": c.name, "kind": c.kind, "statement": c.statement, "subject": c.subject}
    data.update(change)
    return m.prepare(s, "USE", data)


def update(registry, s, facts=None, context=None):
    event = m.prepare(s, "IMPORT_EXTERNAL", {"facts": facts or {}, "context": context or {}})
    return m.transition(registry, s, event)[0], event


class Calibration(unittest.TestCase):
    def test_identity_all_16_coordinates(self):
        fields = {k: h(k) for k in m.OPERATOR_FIELDS}
        self.assertEqual(len(fields), 16)
        original = m.operator_identity(fields)
        self.assertEqual(original, m.operator_identity(dict(reversed(list(fields.items())))))
        for key in fields:
            with self.subTest(key=key):
                count("identity_coordinates")
                self.assertNotEqual(original, m.operator_identity(fields | {key: h("new:" + key)}))
                with self.assertRaises(ValueError):
                    m.operator_identity({k: v for k, v in fields.items() if k != key})
        with self.assertRaises(ValueError):
            m.operator_identity(fields | {"hidden": h("x")})

    def test_projection_counterexample(self):
        worlds = (("same-id", "same-version", "answer 0", 0),
                  ("same-id", "same-version", "answer 1", 1))
        self.assertEqual(worlds[0][:2], worlds[1][:2])
        self.assertNotEqual(worlds[0][-1], worlds[1][-1])
        # Complete finite calibration of factorization over 4 worlds and 2 labels.
        for projection in itertools.product(range(2), repeat=4):
            for prop in itertools.product(range(2), repeat=4):
                constant = all(projection[i] != projection[j] or prop[i] == prop[j]
                               for i in range(4) for j in range(4))
                factors = any(all(g[projection[i]] == prop[i] for i in range(4))
                              for g in itertools.product(range(2), repeat=2))
                self.assertEqual(constant, factors)
                count("factorization_models")

    def test_canonical_values_and_freezing(self):
        self.assertNotEqual(m.digest("x", ["ab", "c"]), m.digest("x", ["a", "bc"]))
        self.assertNotEqual(m.digest("x", 1), m.digest("y", 1))
        self.assertNotEqual(m.digest("x", 1), m.digest("x", True))
        for bad in (1.0, float("nan"), {1: "x"}, {"x"}):
            with self.assertRaises(ValueError):
                m.digest("test", bad)
        with self.assertRaises(ValueError):
            replace(cert(), bindings=[])
        with self.assertRaises(ValueError):
            replace(cert(), supports=(("root:mutable-alias",),))
        with self.assertRaises(ValueError):
            replace(state((cert(),)), generation=True)
        with self.assertRaises(ValueError):
            m.registry_id((cert(), cert()))
        with self.assertRaises(ValueError):
            replace(cert(), bindings=(("a", h("x")), ("a", h("y"))))

    def test_missing_judgment_and_scoped_checker_trust(self):
        c = cert()
        s = state((c,))
        s = replace(s, facts=tuple((k, v) for k, v in s.facts if k != m.judgment_key((c,), c)))
        self.assertEqual(m.evaluate((c,), s)[c.name], m.UNRESOLVED)
        self.assertTrue(any("MISSING:" in x for x in m.diagnostics((c,), s)[c.name]))
        self.assertNotEqual(m.trust_key(c), m.trust_key(replace(c, statement=h("other"))))

    def test_conflict_and_invalid_proof_are_not_claim_negation(self):
        c = cert()
        for value, expected in (("CONFLICT", m.UNRESOLVED), ("INVALID", m.UNUSABLE),
                                ("UNKNOWN", m.UNRESOLVED), ("VALID", m.APPLICABLE)):
            with self.subTest(value=value):
                s = state((c,), {m.judgment_key((c,), c): value})
                self.assertEqual(m.evaluate((c,), s)[c.name], expected)
        s = state((c,), {m.trust_key(c): "UNKNOWN"})
        self.assertEqual(m.evaluate((c,), s)[c.name], m.UNRESOLVED)

    def test_alternate_support(self):
        c = cert(supports=((root("one"),), (root("two"),)))
        s = state((c,), {root("one"): "INVALID", root("two"): "VALID"})
        self.assertEqual(m.evaluate((c,), s)[c.name], m.APPLICABLE)

    def test_all_necessary_dependencies(self):
        c = cert(supports=((root("one"), root("two")),))
        s = state((c,), {root("one"): "INVALID", root("two"): "VALID"})
        self.assertEqual(m.evaluate((c,), s)[c.name], m.UNUSABLE)

    def test_cycles_need_grounding(self):
        a, b = cert("a", supports=(("cert:b",),)), cert("b", supports=(("cert:a",),))
        r = (a, b)
        self.assertEqual(set(m.evaluate(r, state(r)).values()), {m.UNRESOLVED})
        b = replace(b, supports=(("cert:a",), (root("ground"),)))
        r = (a, b)
        self.assertEqual(set(m.evaluate(r, state(r, {root("ground"): "VALID"})).values()), {m.APPLICABLE})
        c = cert("c", supports=(("cert:absent",),))
        self.assertEqual(m.evaluate((c,), state((c,)))[c.name], m.UNRESOLVED)
        c = replace(c, supports=())
        self.assertEqual(m.evaluate((c,), state((c,)))[c.name], m.UNRESOLVED)

    def test_all_small_supports_against_completion_oracle(self):
        # For independent roots, monotone DNF Kleene evaluation equals completion bounds.
        supports = [tuple(root(str(i)) for i in range(3) if mask & (1 << i)) for mask in range(8)]
        for profile in range(256):
            alternatives = tuple(supports[i] for i in range(8) if profile & (1 << i))
            if not alternatives:  # no-derivation is explicitly UNRESOLVED, not a closed-world false claim
                continue
            c = cert(supports=alternatives)
            for assignment in itertools.product(("INVALID", "UNKNOWN", "VALID"), repeat=3):
                f = {root(str(i)): value for i, value in enumerate(assignment)}
                outcomes = []
                for complete in itertools.product((False, True), repeat=3):
                    if any(v != "UNKNOWN" and complete[i] != (v == "VALID") for i, v in enumerate(assignment)):
                        continue
                    outcomes.append(any(all(complete[i] for i in range(3) if root(str(i)) in a)
                                        for a in alternatives))
                expected = m.APPLICABLE if all(outcomes) else m.UNUSABLE if not any(outcomes) else m.UNRESOLVED
                self.assertEqual(m.evaluate((c,), state((c,), f))[c.name], expected)
                count("DNF_oracle_comparisons")

    def test_cyclic_grounded_proof_oracle(self):
        profiles = (((),), (("cert:a",),), (("cert:b",),), ((root("x"),),),
                    ((root("y"),),), (("cert:a", "cert:b"),),
                    ((root("x"), root("y")),), (("cert:a",), (root("x"),)))
        for left, right in itertools.product(profiles, repeat=2):
            r = (cert("a", supports=left), cert("b", supports=right))
            for x, y in itertools.product(("INVALID", "UNKNOWN", "VALID"), repeat=2):
                facts = {root("x"): x, root("y"): y}
                grounded = {k for k, v in facts.items() if v == "VALID"}
                while True:
                    added = {c.name for c in r if any(set(a) <= grounded for a in c.supports)}
                    if added <= grounded:
                        break
                    grounded |= added
                values = m.evaluate(r, state(r, facts))
                for c in r:
                    self.assertEqual(values[c.name] == m.APPLICABLE, c.name in grounded)
                    count("cyclic_grounding_node_comparisons")

    def test_marginal_guarantee_countermodel(self):
        correct = [True] * 19 + [False]
        self.assertEqual(sum(correct), 19)
        self.assertEqual(len(correct), 20)
        self.assertFalse(correct[-1])
        self.assertEqual(sum(correct[-1:]), 0)  # selected failing subgroup has zero coverage

    def test_scope_epoch_and_operator_drift(self):
        context = {"operator": h("v1"), "scope": h("population"), "epoch": h("e1")}
        c = cert(kind="OPERATOR_GUARANTEE", bindings=tuple(sorted(context.items())))
        s = state((c,), context=context)
        self.assertEqual(m.evaluate((c,), s)[c.name], m.APPLICABLE)
        for key in context:
            with self.subTest(key=key):
                changed, _ = update((c,), s, context={key: h("changed")})
                self.assertEqual(m.evaluate((c,), changed)[c.name], m.UNRESOLVED)
        with self.assertRaises(ValueError):
            replace(c, bindings=())

    def test_no_guarantee_to_exact_coercion(self):
        bindings = tuple(sorted((k, h(k)) for k in ("operator", "scope", "epoch")))
        c = cert(kind="OPERATOR_GUARANTEE", bindings=bindings)
        s = state((c,), context=dict(bindings))
        with self.assertRaisesRegex(ValueError, "TYPE_OR_SUBJECT"):
            m.transition((c,), s, use(s, c, kind="EXACT_OBJECT"))
        with self.assertRaises(ValueError):
            m.transition((c,), s, use(s, c, subject=h("other instance")))

    def test_immutable_proof_survives_producer_drift(self):
        c = cert()
        s = state((c,), context={"operator": h("old producer")})
        changed, _ = update((c,), s, context={"operator": h("new producer")})
        self.assertEqual(m.evaluate((c,), changed)[c.name], m.APPLICABLE)
        self.assertEqual(s.generation, 0)
        _, receipt = m.transition((c,), changed, use(changed, c))
        self.assertEqual(receipt["subject"], c.subject)

    def test_dependency_locality_and_root_retraction(self):
        a = cert("a", supports=((root("e"),),))
        b = cert("b", supports=(("cert:a",), (root("alternative"),)))
        c = cert("c")
        r = (a, b, c)
        s = state(r, {root("e"): "VALID", root("alternative"): "VALID"})
        changed, _ = update(r, s, facts={root("e"): "INVALID"})
        values = m.evaluate(r, changed)
        self.assertEqual(values, {a.name: m.UNUSABLE, b.name: m.APPLICABLE, c.name: m.APPLICABLE})

    def test_registry_name_rebinding(self):
        c = cert()
        s = state((c,))
        altered = replace(c, proof=h("different proof"))
        with self.assertRaisesRegex(ValueError, "REGISTRY_DRIFT"):
            m.evaluate((altered,), s)
        self.assertNotEqual(m.judgment_key((c,), c), m.judgment_key((altered,), altered))

    def test_stale_and_aba_intents(self):
        c = cert(supports=((root("e"),),))
        r = (c,)
        s = state(r, {root("e"): "VALID"})
        intent = use(s, c)
        revoked, _ = update(r, s, facts={root("e"): "INVALID"})
        with self.assertRaises(ValueError):
            m.transition(r, revoked, intent)
        with self.assertRaisesRegex(ValueError, "NOT_APPLICABLE"):
            m.transition(r, revoked, use(revoked, c))
        restored, _ = update(r, revoked, facts={root("e"): "VALID"})
        self.assertEqual(restored.facts, s.facts)
        with self.assertRaisesRegex(ValueError, "STALE_SNAPSHOT"):
            m.transition(r, restored, intent)
        m.transition(r, restored, use(restored, c))

    def test_import_failure_atomicity_and_bad_event(self):
        c = cert()
        r, s = (c,), state((c,))
        old = s.identity
        for event in (m.prepare(s, "IMPORT_EXTERNAL", {"context": {"x": "not-a-digest"}, "facts": {}}),
                      m.prepare(s, "IMPORT_EXTERNAL", {"context": {1: h("x")}, "facts": {}}),
                      m.prepare(s, "DELETE_HISTORY", {}), use(s, c) | {"generation": True},
                      use(s, c) | {"extra": 1}):
            with self.assertRaises(ValueError):
                m.transition(r, s, event)
            self.assertEqual(s.identity, old)

    def test_replay_checkpoint_and_receipt_identity(self):
        a, b = cert("a"), cert("b")
        r, initial = (a, b), state((a, b))
        e1 = use(initial, a)
        s1, receipt1 = m.transition(r, initial, e1)
        e2 = use(s1, b)
        s2, receipt2 = m.transition(r, s1, e2)
        replayed, receipts = m.replay(r, initial, [e1, e2], s2.identity)
        self.assertEqual((replayed, receipts), (s2, (receipt1, receipt2)))
        for events in ([e1], [e2, e1], [e1, e1], []):
            with self.assertRaises(ValueError):
                m.replay(r, initial, events, s2.identity)
        other, _ = m.transition(r, initial, use(initial, b))
        self.assertNotEqual(s1.identity, other.identity)

    def test_absorption_requires_external_evidence(self):
        record = {k: ("a" * 40 if k.endswith("_sha") else h(k)) for k in m.ABSORPTION_FIELDS}
        record["terminal"] = "SCOPED_THEORY_PARENT_OWNED"
        keys = m.absorption_keys(record)
        facts = {k: "VALID" for k in keys}
        status = lambda rec, f: m.absorption_status(rec, f, "a" * 40, "a" * 40)
        self.assertEqual(status(record, facts), m.APPLICABLE)
        self.assertEqual(status(record, {}), m.UNRESOLVED)
        for key in keys:
            self.assertEqual(status(record, {k: v for k, v in facts.items() if k != key}), m.UNRESOLVED)
            self.assertEqual(status(record, facts | {key: "CONFLICT"}), m.UNRESOLVED)
        for key in ("statement", "artifact_manifest", "parity_receipt", "review_receipt", "scope"):
            self.assertEqual(status(record | {key: h("changed")}, facts), m.UNRESOLVED)
        for key in record:
            with self.assertRaises(ValueError):
                status({k: v for k, v in record.items() if k != key}, facts)
        with self.assertRaises(ValueError):
            status(record | {"source_sha": "b" * 40}, facts)
        with self.assertRaises(ValueError):
            status(record | {"terminal": "CANNOT_CHECK"}, facts)


if __name__ == "__main__":
    unittest.main()
