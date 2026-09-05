# Foundation study integration V1

This package integrates the ten existing Foundation PR heads below as scoped,
runnable research studies. It resolves the conflicting `foundation_v1` paths,
retains original evidence, and adds cross-study semantic and custody checks.
It does not claim that every atlas question, protected experiment, independent
review, or OCM implementation is complete.

The authoritative programme registry is
`../MACHINE_EPISTEMICS_FOUNDATION_V1.json` from #324, as designated in #319.
`../ME_FOUNDATION_V1.json` from #321 is a supporting theorem-batch ledger.
Its 28/35 dispositions are scoped claims from that ledger; they neither replace
the canonical registry's 36-row vocabulary nor authorize automatic promotion of
its open rows. Supporting registries and study-specific terminals remain
addressable rather than being flattened to a common success label.

| PR | Integrated package or study | Source head |
| --- | --- | --- |
| #320 | `decision_frontier_v1` | `b373b0ad5865580c68166c5babeca5b3d1347c3f` |
| #321 | Foundation batches 2–4 and supporting ledger | `71683e577ed811eaf77b25dfad1666d3924b4856` |
| #322 | `certificate_lifecycle_v1` | `89124cd6dcf50dd7cdb2f76019fa3df85e553e38` |
| #323 | `foundation_revision_v1` | `c5cc48058a554461f9e07b1302ea2db96853ebe6` |
| #324 | Canonical registry and identity/nogood checker | `1b42d4669bdd000d4c997582ffb2fe3b5306890c` |
| #325 | `causal_verifier_v1` | `06c3b5ca6abd822ddecf6dcd2f9b569ba740214c` |
| #326 | `revision_consistency_v1`, including `temporal_v2` | `fc354f8a0ec7b913c33b80fc34ab3e3a2f2197dc` |
| #327 | `causal_transport_v1` | `f752a602ad2c4119912ef5ef2b6f859f9c9fcf54` |
| #328 | `foundation_typed_lifecycle_v1` | `2ade489db9b4dca382c68e7e049bcf2f68b96fe5` |
| #331 | `certificate_transport_v1` | `529e282e4c1e6fa0c40f4135b930b4eef2db17f3` |

## Reproduce

From the repository root, with the repository test dependencies installed:

```sh
python research/machine-epistemics-theory/foundation_integration_v1/check_integration.py
python research/machine-epistemics-theory/foundation_integration_v1/check_integration.py --replay
```

The first command verifies all source/integration identities, the relocation
contract, and the historical #323 receipt. The second additionally runs 19
explicit read-only commands in separate processes, including imported tests,
cross-study conformance, exact archived calibration replay, and intended hostile
controls. Individual finite outcomes and original proof-scope limitations remain
in their source packages. The causal-transport `python -O` control must exit 2;
that expected refusal is never counted as successful optimized proof execution.

The separate Lean route is:

```sh
python research/machine-epistemics-theory/foundation_typed_lifecycle_v1/verify_lean.py
```

It requires the original pinned Lean 4.19.0 environment. Missing Lean is
`CANNOT_CHECK`, not a passed proof. The eight-lemma bridge does not mechanize the
probability or matrix theorems. `--include-lean` makes that route a required
additional gate for the integration runner.

## Custody and path reconciliation

`MANIFEST.json` is a successor relocation/provenance manifest covering 130 source
files. It records each exact source PR head, Git blob identity, SHA-256, original
path, integrated path, and current digest. Twenty-four package files moved from
the competing `foundation_v1` namespace into two distinct packages. All their
source bytes, including both different original receipts, remain unchanged.

Exactly two callers needed path substitutions: the #323 root test and the #328
workflow. Their original bytes are retained under `source_artifacts/323` and
`source_artifacts/328`. The checker verifies that the only adaptation is the
declared package-path substitution. It evaluates the old #323 receipt against
the preserved original test, never pretending its digest binds the adapted test.
The successor manifest separately binds that adapted test. Source READMEs still
show their historical paths; the commands above and `RELOCATION.md` provide the
current entry points.

`REPLAY_RECEIPT.json`, when present, records actual local replay of this
integration. Original study receipts are historical source artifacts and have
not been rewritten to impersonate this session or a protected host.

## What the integration checks establish

The new conformance tests cover 1,344 three-evidence warrant intervals with an
explicit available/revoked polarity conversion, 2,000 joint nogood products,
324 exact rational fixed points, and common-alphabet TV/risk interfaces. The
tests retain the empty-event exception to a generic risk bound and reject a
missing evidence-polarity conversion. Custody controls reject source deletion,
duplicate destinations, byte drift, path escape, canonical-registry substitution,
and unearned external authority. These are finite reference checks, not
all-size proofs or independent external replication.

The study packages retain their native judgment types, dependency assumptions,
registered query/model families, and resource bounds. Read `COMMON_CONTRACT.md`
before proposing an OCM adapter. The parent-owned exact mechanisms offer bounded
optimization opportunities; no combination of successful local checkers grants
an unstated global theorem, real-world closure assumption, or external action.

Open obligations include independent assumption review, unavailable proof
mechanization, scalable synthesis/certification beyond the finite bounds,
empirical model/channel validity, explicit V2-to-OCM parity and admission, and
the registry's remaining open scientific questions. These obligations cannot be
closed by treating an imported study's `PASS` as a global foundation terminal.
