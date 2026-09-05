# Foundation effective-authority reconciliation V1

This additive package reconciles the historical foundation registries with the
corrections that were subsequently integrated. It is an internal research
specification and import gate; it does not grant scientific truth or OCM adoption.

The source snapshot is ORION-V2
`096e6f3df1854dede3c8a0fbe63d05ec30bcb119`. Forty-three statement, registry,
checker and integration files are bound by their exact commit, Git blob and
SHA-256. No historical registry, theorem, receipt or protected outcome is edited.

`EFFECTIVE_AUTHORITY_V1.json` covers all 20 canonical primitives and all 36 atlas
rows. It preserves the canonical records, the later batch registry, both imported
foundation maps, and matching rows of the atlas's later sections. Those historical
sources use different dates and scopes. An old OPEN row is not evidence that no
later bounded result exists; an old PROVED row does not certify every clause.

There are 36 specifically named reference fragments and 18 excluded refuted or
unsupported formulations. Each fragment binds a unique Markdown theorem section,
its digest, containing source, explicit scope, parent, resource limitations and
finite package checker. Checker references identify calibrations, not proofs of
unbounded generalization. The complete containing document remains bound because
its earlier definitions and trust assumptions still apply.

New foundation imports must use `resolve.select`, then separately verify actual
premises, OCM parity and an authenticated external adoption decision. Raw canonical
or batch status labels, whole MEG ids, unavailable rows and excluded clauses are
refused. A successful selection returns only
`SCOPED_RULE_IDENTIFIED_NO_ADOPTION_AUTHORITY`; its two authorization flags remain
false. This package neither executes an OCM importer nor prevents an unrelated
caller from ignoring the contract. An importer that bypasses this route is not
conformant and must not claim absorption under this specification.

An exact selection has these fields:

```json
{
  "schema": "ME_RULE_SELECTION_V1",
  "rule_id": "MEG-06:SCOPED_FRAGMENT_V1",
  "rule_sha256": "<exact registered rule_sha256>",
  "scope_sha256": "<SHA-256 of the exact UTF-8 scope>",
  "source_snapshot": "096e6f3df1854dede3c8a0fbe63d05ec30bcb119",
  "source_manifest_sha256": "b85e2c633f96e0bf89fa757b5a8e9baf837bd181c17a5eb157e55c53febfad07"
}
```

The literal placeholder strings are deliberately invalid. Source, rule, section
and scope identities are not interchangeable. Recomputing a local hash after
broadening a statement cannot defeat the reviewed catalogue seal. Future semantic
changes require an additive reviewed successor; do not rewrite this snapshot.

Run from a full Git checkout:

```bash
python research/machine-epistemics-theory/authority_reconciliation_v1/resolve.py
python -m unittest discover -s research/machine-epistemics-theory/authority_reconciliation_v1 -p 'test_*.py'
python -O -m unittest discover -s research/machine-epistemics-theory/authority_reconciliation_v1 -p 'test_*.py'
```

Missing Git source objects or files, source drift, duplicate JSON keys, incomplete
bindings, unknown statuses and unsupported selections produce `CANNOT_CHECK`.
The tests exercise genuine mathematical countermodels and malformed imports,
including a copied checkout with modified/missing source and recomputed dishonest
scope digests. They do not execute protected evaluation outcomes.

The new exact footprint counterexample and the supported clauses are explained
in `RECONCILIATION.md`. `FND_CHECKLIST.md` states the closure scope of issue #319
and the delivered-package issues without closing programme or external-review
obligations. The new 27-test suite passes in ordinary and optimized Python;
repository CI and merge evidence are recorded separately by the publishing PR.
