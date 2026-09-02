# ME-X7 — Parent Fidelity and Development-Split Receipt (V1)

**State date:** 2026-09-02. **Status:** frozen design + parent baselines +
development split. **No protected outcome exists or has been inspected.**
Design: `ME_X7_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V1.{md,json}`,
design-JSON sha256
`1895b4388f832b121695ba1d64c688b0a9df44264e4a3284f0d73e8684b54022`.

## 1. Code freeze (sha256)

| file | sha256 |
|---|---|
| `mex7_model.py` | `b45b0edad0591aa08a91b3248b6ff8bcce843dc664d1f07ebaea9535346d75c0` |
| `mex7_oracle.py` | `21f26a44b5f137f3bf8a27a8e95746a8c210212204bcc72cd5b89b2209f2de0f` |
| `mex7_generator.py` | `4a8e3e18c6c43464febed1e645772717e2bfdd713b97c0e2356063723e685ea7` |
| `mex7_parents.py` | `18bd7a0c5a774db5415ce33ede74eea6a856d740ece0184548121b45dd0e859e` |
| `mex7_arms.py` | `3afe7763cfc21dd9b9dde698ec8a457369a10610ad22160bc7d4afec560fa6aa` |
| `mex7_run.py` | `ac1d61982ead0520b0b56c084bc8d4a3727eebef99d500eb11f75851c1c3f0f1` |

Protected seed commitment
`2c8a3d774cab1fcae49fae5876d9ed314ea771563fa31ff44784c3dd3e2cf4b2`
(`~/.orion-custody/me-x7/PROTECTED_SEED_V1.txt`, mode 600). The seed value is
not in this repository and is revealed only in the outcome receipt.

## 2. Parent fidelity — 23/23 native known-answer tests

Every parent passes its own native tests before it is used as a comparator
(ME-X1 shipped 51/51, ME-X2 21/21). Source of truth:
`results/ME_X7_SELFTEST_REPORT.json`, key `parent_fidelity`.

| parent | native semantics | tests | result |
|---|---|---|---|
| `RESOLUTION_CHECKER` | propositional resolution refutation (Robinson 1965; presentation after Bachmair & Ganzinger, *Handbook of Automated Reasoning* ch. 2) | 7 | 7/7 — accepts the unit-pair and two-step refutations; rejects an unsound resolvent, a step with no complementary literal, a sound-but-incomplete derivation and an out-of-range index; the wire encoding round-trips |
| `REPLAY_MACHINE` | deterministic register machine over program × environment constant × seed | 4 | 4/4 — identical inputs reproduce the digest; changing the seed, the environment or the program each diverges |
| `PROVENANCE_LINEAGE` | `orion_v2.provenance.ReticulateProvenance` revocation descendants (the parent ME-X4's A0 arm used) | 3 | 3/3 — a transitive revocation reaches its descendant support, does not splash onto an unrelated one, and an empty revocation set hits nothing |
| `DEPENDENCE_AUDIT` | `orion_v2.evidence.assess_evidence_dependence` | 4 | 4/4 — no edges leaves every unit independent; a confirmed edge merges; a suspected edge merges only when suspected edges are included |
| `ASSURANCE_CASE` | GSN change impact through supported-by / in-context-of edges (Kelly & Weaver 2004) | 2 | 2/2 — a challenged solution makes the top goal suspect; an unrelated node does not |
| `SELECTIVE_ABSTENTION` | selective prediction at a fixed coverage threshold (Geifman & El-Yaniv 2017) | 3 | 3/3 — high, low and boundary scores map to accept, reject and abstain |

Two of these are **real engines, not flags**: the resolution checker decides
`Artifact.checker_accepts` in `MODE_FORMAL`, so a planted proof mismatch is a
checker rejection; the replay machine recomputes the output digest, so a planted
seed/version mismatch is an actual replay divergence.

## 3. G0a — known-answer fixtures, separation pair, planted positives

- **25/25 hand-authored fixtures** (one per applicable (stratum, mode) cell) are
  reproduced by the oracle: verdict, defect class and direct-rule/exhaustive
  agreement.
- **Separation pair** (design §2.6): the self-contained witness returns the
  identical verdict on P and Q and is therefore wrong on one; the
  identity-exporting witness and the federation are exact on both.
  `passed = true`.
- **4/4 planted positives.** Each no-alarm assertion is paired with a case that
  must trip it: a planter that fails to plant is rejected; a planter that plants
  twice is rejected; a "clean" episode that is not clean is rejected; a
  correctly planted episode is accepted. Without these, "G0b reported zero
  violations" would be unfalsifiable.

## 4. G0b/G0c — two implementations of the semantics, plus a generator check

The receipt is deliberately precise about what is independent of what.

**Two implementations of the verdict rule.** The direct adjudication rule and an
exhaustive enumeration over every resolution of the censored checks agree on
every instance of every split.

**Two implementations of the check table, one per side of the primary
comparison.** `M` and `B5` must not be the same computation under two names, or
G1, G2 and three of the five sufficiency conjuncts would be `x == x`. They are
adjudicated through separately written tables (design §2.4), both arm-side,
neither importing the oracle. **Four of the eleven checks run different code** —
`C_SOURCE_STATUS` (ancestor walk vs `affected_by_revocation` reachability),
`C_DEPENDENCE` (ancestor-set overlap vs descendant-walk pairs),
`C_ENV_IDENTITY` (recorded identities compared vs the replay machine actually
re-run), `C_PRESERVATION` (`assess_correspondence_chain` vs
`ComparabilityCertificate`). **The other seven are arithmetic thin enough that
two implementations would be the same three lines, and are reported as shared
rather than counted as independent.** Both tables re-run the resolution checker
and the replay machine instead of trusting a recorded flag. Per-check agreement
is printed in the analysis (`IMPLEMENTATION_AGREEMENT`); on the development
split it is 25/25 on all eleven. A unit test asserts the two tables really are
distinct where the design says they are, and a planted positive shows they can
disagree when one side's registry resolution is broken.

**A generator-validity check, not a third implementation.** `planter_agrees`
compares the planter's declared defect with a full-structure recomputation that
runs through the oracle's own code. It validates the *generator* — a planter
that fails to plant, plants twice, or turns a decoy into a defect cannot enter a
split — and the four planted positives show it is trippable. It is not evidence
about the semantics, and the design and PR text say so.

**One design invariant added by the same review.** `C_ENV_IDENTITY` has two
faithful operationalizations — comparing the recorded assumption/version
identities (M) and re-executing under them (B5). A planted mismatch where
following the record happens to reproduce the reported output would split them
for a reason that is an artifact, not a finding, and would show up as an M
advantage over the federation. The generator now rejects such candidates
outright, so the split cannot contain one; a unit test asserts both sides return
INVALID on 60 generated instances. An empirical probe found zero such instances
in 400 draws before the guard, but the guard is the control, not the probe.

**Null calibration passes:** `C_ALWAYS_ACCEPT` scores 0 where the oracle
rejects, `C_ALWAYS_CANNOT_CHECK` scores 0 where the episode is decidable,
`C_RANDOM_VERDICT` and M-against-shuffled-labels both stay under 0.15.

## 5. Development split (25 instances, public seed `ME-X7-DEV-20260902`)

**Not protected evidence.** It exists to show the machinery runs end to end and
that the pre-registered mechanisms are live. Full table:
`results/ME_X7_DEVELOPMENT_ANALYSIS_V1.md`.

| arm | exact | false acceptance (n=21) | abstains on decidable (n=23) | mean export |
|---|---|---|---|---|
| `S0_OPAQUE_OUTPUT_ONLY` | 0.080 | 21 | 0 | 1.0 |
| `S1_PROVENANCE_PLUS_OUTPUT` | 0.200 | 19 | 0 | 9.0 |
| `S2_FULL_HUMAN_STYLE_TRACE` | 0.240 | 17 | 0 | 48.0 |
| `S3_PROOF_OR_CERTIFICATE_PARENT` | 0.240 | 17 | 0 | 5.0 |
| `M_CLAIM_SUFFICIENT_WITNESS` | 1.000 | 0 | 0 | 43.5 |
| `B5_STRONGEST_FAITHFUL_AUDIT_PARENT` | 1.000 | 0 | 0 | 43.5 |
| `M_MINUS_EVALUATOR_CONTRACT` | 0.920 | 2 | 0 | 30.5 |
| `C_ALWAYS_ACCEPT` | 0.080 | 21 | 0 | 1.0 |
| `C_ALWAYS_CANNOT_CHECK` | 0.080 | 0 | 23 | 1.0 |
| `C_RANDOM_VERDICT` | 0.120 | 13 | 5 | 1.0 |

Ladder (fields only, registry resolution held constant): 0.080 → 0.200 → 0.360
→ 0.600 → 0.920 → 1.000, monotone. The per-class detection matrix is exact and
each omission ablation zeroes precisely the classes whose check needs the field
it drops (G3 passes on the development split, including the two-field
`C_ROUTE_COMPLETENESS` prediction).

**What the development split never exercised, named exhaustively.** The analysis
carries a `COVERAGE_LEDGER` listing every registered mechanism with the number
of instances that exercised it and every one at zero. At one instance per cell:
all 25 applicable cells are drawn once, but **eight of the ten censoring
variants** (`CENSOR_SPEC`, `CENSOR_DEPENDENCE`, `CENSOR_ENV`,
`CENSOR_CALIBRATION`, `CENSOR_ROUTE`, `CENSOR_EVALUATOR`, `CENSOR_AUTHORITY`,
`CENSOR_PRESERVATION`) and **three of the six locus combinations**
(`HIDDEN_DEPENDENCE|TRANSITIVE_ANCESTOR`,
`HIDDEN_DEPENDENCE|UNDECLARED_SHARED_UPSTREAM`,
`STALE_OR_WRONG_SOURCE|UNDECLARED_SHARED_UPSTREAM`) are drawn zero times.

Consequently **G7 `WITNESS_SELF_CONTAINMENT` reports
`CANNOT_CHECK_NO_UNDECLARED_INSTANCES, n_evaluated = 0` and `pass = false`**,
and the witness terminal is qualified
`WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT__SELF_CONTAINMENT_CANNOT_CHECK`
rather than reading as a clean pass. At 50 per cell the protected split is
expected to draw about 25 undeclared-upstream instances and roughly five of each
censoring variant. This is exactly the failure shape the `n_evaluated` rule
exists to expose, caught by the discipline rather than by luck.

## 6. What the development split does *not* license

No confirmatory claim. The pre-registered expectation (design §1.2) is
`PARENT_SUFFICIENT` with `WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT`; the
development split is consistent with it and is not evidence for it.

**`M exact 1.000, B5 exact 1.000` is not the headline and must not be quoted as
one.** Design §9(4) records in advance that M and B5 hold the same fields and
the same registry visibility, so the comparison is a *cross-implementation*
test, not an information test: it can catch a bug in either side's four distinct
checks and it cannot detect a residual that does not exist. The decisive axes
are the omission matrix (G3), the ladder (G4), the sufficiency conjuncts (G5),
cross-mode transfer (G6) and self-containment (G7) — and G7 is unevaluated on
the development split.

## 7. Protected-run guard (asserted by the unit tests)

`PROTECTED_RUN_AUTHORIZATION.json` is absent from this repository.
`mex7_run.py protected` exits 3 without it, 3 with a short or unacknowledged
token, 3 when `acknowledged_design_sha256` does not equal the design JSON's
sha256, and 4 when the custody seed is absent or does not hash to the frozen
commitment. All five refusal paths are covered by
`tests/unit/test_me_x7_exact_study.py`.
