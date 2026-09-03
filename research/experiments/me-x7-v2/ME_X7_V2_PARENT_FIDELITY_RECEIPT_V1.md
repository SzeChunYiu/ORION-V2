# ME-X7 V2 — Parent Fidelity and Development-Split Receipt (V1)

**State date:** 2026-09-03. **Status:** frozen V2 design + parent baselines +
development split. **No V2 protected outcome exists or has been inspected.**
Design: `ME_X7_V2_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V2.{md,json}`,
design-JSON sha256
`799db760e87ae7ddc28ad2d12ad1a41622502314c7bfb2c42a0984d44e00dbf2`.

**Why V2 exists.** The V1 protected run routed `CANNOT_CHECK` on a hard-gate
failure (G0b `ORACLE_SELF_AGREEMENT`, 1244/1250) and issued no arm verdict; see
`research/experiments/me-x7/ME_X7_OUTCOME_RECEIPT.md`. V2 carries the two
registered semantic corrections that receipt's §7 prescribes as repair 3, a
label-only third correction from its §2.6, and a new protected seed commitment.
Nothing else changes. Design §0 states the corrections; §1.1 below states which
files they touch.

## 1. Code freeze (sha256), against V1

| file | V2 sha256 | changed from V1 |
|---|---|---|
| `mex7_model.py` | `b45b0edad0591aa08a91b3248b6ff8bcce843dc664d1f07ebaea9535346d75c0` | **no — byte-identical** |
| `mex7_parents.py` | `18bd7a0c5a774db5415ce33ede74eea6a856d740ece0184548121b45dd0e859e` | **no — byte-identical** |
| `mex7_oracle.py` | `14fc59100a15b623200c1c70c6825cb35be610257f120498b22777c1f23b8533` | yes — corrections 1 and 2 |
| `mex7_generator.py` | `ad204fd0f3347d6dd975daa7fad62b0fef16a14a8a11ccaeef500b5f44657961` | yes — correction 2 (passes the drawn variant; import-time cross-check) |
| `mex7_arms.py` | `44ebdb59b6395baffa7abe2b366c4282f5a39a24b5c6008380848c1fcb691d71` | yes — correction 1 and its declared A0 consequence |
| `mex7_run.py` | `9a2325a74021d3ae6b681c535e23c50d3fae03d5e1bbbde2eea951b855c01c85` | yes — correction 2 (passes the drawn variant), correction 3 (label), V2 design/custody paths and schema strings |

### 1.1 Every hunk, and nothing else

`diff -u` between the V1 and V2 modules is carried in full in the freeze PR
body. Counted as added/removed lines, headers excluded:

| file | added | removed | what |
|---|---|---|---|
| `mex7_arms.py` | 18 | 0 | the recoverability guard, the A0 abstention, and the comments that register both |
| `mex7_generator.py` | 14 | 2 | one import, one import-time cross-check, one call site |
| `mex7_oracle.py` | 107 | 7 | the digest check's censored branch, the declared table and its accessor, the set-equality invariant, and the module docstring that registers both corrections |
| `mex7_run.py` | 25 | 14 | one call site, one dictionary key and its rule string, one rendered line, and the design/custody/schema path rebindings |

Most of the oracle's 107 added lines are the module docstring and the declared
table's comments; the executable change there is one `if` in
`check_artifact_digest`, one dict comprehension plus one override, one accessor,
and the replacement of a length test by a set comparison. **No gate threshold,
stratum weight, arm field set, surface definition, ladder rung, locus weight or
statistic appears in any hunk**, and the measurements of §1.2 are what make that
claim checkable rather than asserted.

Protected seed commitment
`08631e5fa419e350a2c4d71bcee487fdebb166875ed8647a79f76f2519f02cfd`
(`~/.orion-custody/me-x7-v2/PROTECTED_SEED_V1.txt`, mode 600). The seed value is
not in this repository and is revealed only in the V2 outcome receipt. **The V1
protected seed is burned**: it was revealed in the V1 outcome receipt §1 and is
used here only as a public validation seed, and only for G0-relevant
quantities.

### 1.2 The corrections, measured against the V1 seed

Executed, not asserted (`tests/unit/test_me_x7_v2_exact_study.py`):

| claim | result |
|---|---|
| V1 and V2 generate the same 1250-instance protected split under the burned V1 seed | **identical** — canonical-JSON digest `462e6a0bbb46a301e12aefe285424276f520ca959c200184cbbc0c92917b34c9` on both |
| `CENSOR_ENV` draws in that split | **8** under V1 and **8** under V2 — 6 computational, 2 formal |
| the six computational instances the V1 receipt §2.2 names | still drawn, same indices 0002, 0011, 0015, 0019, 0042, 0045 |
| their `C_ARTIFACT_DIGEST` status | V1: oracle `VALID` vs both arms `INVALID`. V2: oracle `CENSORED` = M `CENSORED` = B5 `CENSORED` |
| correction 1 without correction 2 (counterfactual, measured) | `CENSOR_ENV` falls **8 → 2**, all six computational instances leave the split |
| V2 development split vs V1's | results, expected-custody and selftest report **identical in every field except `schema_version`** |

The first and last rows are the provenance argument: the two corrections are
inert everywhere except the one cell they were written for, and that cell is
still in the split. This is a G0-only validation — no arm verdict, ladder rung
or G1/G4/G5/G7 number is read off the burned seed, so the V2 protected run
stays blind.

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
is printed in the analysis (`ARM_VS_ARM_IMPLEMENTATION_AGREEMENT`, renamed by
V2 correction 3); on the development split it is 25/25 on all eleven. **It is
arm against arm and never either against the oracle**, so it cannot see a
defect in one of the seven shared implementations — which is exactly what V1
had, and why it read 1250/1250 on all eleven checks in the run where G0b found
six disagreements. G0b is the three-way comparison that can. A unit test asserts the two tables really are
distinct where the design says they are, and a planted positive shows they can
disagree when one side's registry resolution is broken.

**A generator-validity check, not a third implementation.** `planter_agrees`
compares the planter's declared defect with a full-structure recomputation that
runs through the oracle's own code. It validates the *generator* — a planter
that fails to plant, plants twice, or turns a decoy into a defect cannot enter a
split — and the four planted positives show it is trippable. It is not evidence
about the semantics, and the design and PR text say so.

**V2 correction 2 inside that check.** For the `CENSORED_UNDECIDABLE` stratum
the drawn variant is now required and its censored set must equal the set
declared for that `(variant, mode)` pair. The declared table is total over the
19 drawable pairs, an unregistered pair raises rather than defaulting, and the
generator asserts at import time that its variant registry and the declared
table agree. A parametrised unit test checks *observed == declared* on every one
of the 19 pairs — proving as a measurement, not an assertion, that the new
invariant is behaviourally identical to V1's `len == 1` everywhere except
`(CENSOR_ENV, MODE_COMPUTATIONAL)`. A further test makes the new invariant
trippable: with the declaration reduced to one check, the same episode is
rejected and names `C_ARTIFACT_DIGEST` in the reason, which is precisely how a
partial repair would have deleted the six instances.

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
commitment. All six refusal paths — the sixth being the burned V1 seed, which
must not open the V2 protected stage — are covered by
`tests/unit/test_me_x7_v2_exact_study.py`, which also asserts that a refused run
creates no output directory. Exit 3 and exit 4 are deliberately distinct from
each other and from the exit 1 a broken interpreter gives, so "not authorized",
"no seed" and "crashed" are never confused.

## 8. What this receipt does not establish

No V2 protected outcome exists. The V1 route was `CANNOT_CHECK` with witness
terminal `NONE`, and **no part of it is carried forward**: V2 does not inherit
`PARENT_SUFFICIENT`, does not inherit
`WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT`, and does not inherit any residual.
The question ME-X7 asks is open until the V2 protected run is executed and
receipted. No field status, novelty or publication authority attaches to
anything here.
