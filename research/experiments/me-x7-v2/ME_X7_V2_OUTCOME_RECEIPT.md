# ME-X7 V2 — Claim-Sufficient External Witnesses: Protected-Run Outcome Receipt

**Run date:** 2026-09-03
**Design:** `ME_X7_V2_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V2.json`,
sha256 `799db760e87ae7ddc28ad2d12ad1a41622502314c7bfb2c42a0984d44e00dbf2`,
frozen and merged to main in PR #239 before this run.
**Parent:** ME-X7 V1 (PR #217) routed `CANNOT_CHECK` on a hard-gate failure and
issued no arm verdict; `research/experiments/me-x7/ME_X7_OUTCOME_RECEIPT.md`.

## 0. Route

```text
ME_X7_V2_PROTECTED_ROUTE = PARENT_SUFFICIENT
WITNESS_TERMINAL         = WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT__REQUIRES_IDENTITY_EXPORT
REASON                   = the federation is matched, and the compact witness meets every sufficiency conjunct
HARD_GATES               = G0a PASS (31), G0b PASS (1250), G0c PASS (1050)
COST_FLAG                = COST_ADVANTAGE_M
FIELD_STATUS_AUTHORITY   = NONE
```

Every gate evaluated; none failed; no gate reported a zero denominator except
the one cell the design declared non-applicable in advance, which reports
`CANNOT_CHECK_NOT_APPLICABLE, n_evaluated = 0` and is not counted as a pass.
This is the route and the terminal the design pre-registered in §1.2, which is
worth stating plainly rather than quietly: **a confirmed prior expectation is
weaker evidence than a surprise, and §9(4) says in advance why.** What the run
adds beyond the expectation is §4 below — the ladder, the omission matrix and
the self-containment separation, which are the axes that carry content.

## 1. Seed reveal (post-run half of the pre-published commitment)

Committed in the frozen design before the run:

```text
seed_commitment.protected_seed_sha256 = 08631e5fa419e350a2c4d71bcee487fdebb166875ed8647a79f76f2519f02cfd
```

Revealed now:

```text
PROTECTED_SEED_V1 = ME-X7-V2-PROTECTED-eb9202166140d73899fa98632a57b46e336e3337e8722384
```

Recomputation (one line, executed):

```console
$ printf '%s' 'ME-X7-V2-PROTECTED-eb9202166140d73899fa98632a57b46e336e3337e8722384' | shasum -a 256
08631e5fa419e350a2c4d71bcee487fdebb166875ed8647a79f76f2519f02cfd  -
```

Custody file `~/.orion-custody/me-x7-v2/PROTECTED_SEED_V1.txt`, mode 0600,
67 bytes, hashed to the commitment **before** the authorization file was
written. It is distinct from the burned V1 seed and does not share its
prefix.

## 2. The V1 defect, closed and still in the split

V1's hard-gate failure was six instances in
`CENSORED_UNDECIDABLE × MODE_COMPUTATIONAL × DIRECT × C_ARTIFACT_DIGEST`, where
an unrecoverable environment was misread by both arms as a proof/code mismatch.
The repair had to close the semantics **without** deleting the cell that
exposed it. This split, under a seed nobody had seen, drew that variant again:

| censoring variant | draws | of which `MODE_COMPUTATIONAL` |
|---|---|---|
| `CENSOR_ENV` | 11 | 7 |

All **7** computational `CENSOR_ENV` instances (indices 0007, 0009, 0020, 0028,
0039, 0042, 0047):

| quantity | value |
|---|---|
| oracle censored set | `{C_ARTIFACT_DIGEST, C_ENV_IDENTITY}` on all 7 — the declared set for that (variant, mode) pair |
| oracle `C_ARTIFACT_DIGEST` | `CENSORED` on all 7 |
| M's and B5's `C_ARTIFACT_DIGEST` | `CENSORED` on all 7 — the three-way comparison agrees |
| oracle verdict | `CANNOT_CHECK` on all 7, direct rule = exhaustive enumeration |
| `planter_agrees` | true on all 7 (set equality against the declaration, not a count) |

The **4** formal `CENSOR_ENV` instances (0005, 0007, 0036, 0045) censor
`{C_ENV_IDENTITY}` alone and keep `C_ARTIFACT_DIGEST = VALID`, which is the
mode gate working: the formal branch runs the resolution checker over the
payload and never consults the environment. A mode-agnostic guard would have
made these four wrong.

**Under the pre-registered counterfactual, this cell would not exist.** The
check-table extension applied without the declared-set invariant re-draws every
computational `CENSOR_ENV` episode; measured against the burned V1 seed,
`CENSOR_ENV` falls from 8 draws to 2 and all six V1 instances vanish. The gate
would then have gone green because the hard cases left the split. It did not
go green that way here: the cell is live at 7 instances and agrees.

## 3. Gate table — every gate, every denominator, including the zero

| gate | status | n_evaluated |
|---|---|---|
| G0a `KNOWN_ANSWER` (hard) | PASS | 31 |
| G0b `ORACLE_SELF_AGREEMENT` (hard) | **PASS** | 1250 |
| G0c `NULL_CALIBRATION` (hard) | PASS | 1050 |
| G1a `B5_REPRODUCES_M` | PASS | 1250 |
| G1b `M_ADVANTAGE` | did not fire | 1250 |
| G1c `B5_AHEAD` | did not fire | 1250 |
| G2 `ANTI_CONSERVATISM` | PASS | 100 |
| G3 `MECHANISM_BY_OMISSION` | PASS | 1050 |
| G4 `INTERFACE_LADDER` | PASS | 1250 |
| G5 `SUFFICIENCY` | **PASS (all five conjuncts)** | 250 |
| G6 `CROSS_MODE_TRANSFER` | PASS | 1250 (600 formal / 650 computational) |
| G7 `WITNESS_SELF_CONTAINMENT` | **EVALUATED, PASS** | 43 (elsewhere 1207) |
| COVERAGE_LEDGER (reported) | all mechanisms exercised | 1250 |
| ARM_VS_ARM_IMPLEMENTATION_AGREEMENT (reported) | arm-vs-arm only, §6 | 1250 |
| COST (reported) | `COST_ADVANTAGE_M` | — |

**G0b, the gate V1 failed, with each component's own denominator:**

| component | result |
|---|---|
| `exhaustive_agree` (direct rule == exhaustive enumeration) | 1250 / 1250 |
| `planter_agree` (declared stratum == full-structure recomputation) | 1250 / 1250 |
| `cross_implementation_agree` (oracle == M's table == B5's table) | **1250 / 1250** |

**G1b and G1c both did not fire, and neither is the negation of the other.**
M − B5 = 0.0 exactly, 0 discordant pairs, exact two-sided p = 1.0, Wald
CI95 [0.0, 0.0]. Each has its own positive test, so a tie fires neither and no
terminal is claimed from the tie. Design §9(4) states in advance why: **B5 is
exact by information-completeness on this generator**, so agreement with it is
not evidence. `M exact 1.000, B5 exact 1.000` is not the headline.

**G5 conjuncts, each with its own denominator:**

| conjunct | pass | n_evaluated | detail |
|---|---|---|---|
| S1 `FAILURE_CLASS_PRESERVATION` | true | 1050 | per class *and* mode |
| S2 `REPLAY_SUPPORT` | **true** | 1250 | supported **1250 / 1250** (V1: 1244/1250) |
| S3 `SELECTIVE_REOPENING_WITHOUT_HIDDEN_HISTORY` | true | 250 | 100 + 100 + 50, all agreeing |
| S4 `FALSE_ACCEPTANCE_NONINFERIORITY` (δ = 0.01) | true | 1050 | FA(M) 0, FA(B5) 0, difference 0.0, 0 discordant either way, one-sided exact p = 1.0 |
| S5 `PREFERABLE_TO_FULL_TRACE` | true | 1250 | paired M − trace = 0.744, 930 discordant all one-directional, exact p ≈ 2.2e-280 |

S1 reports `INVALID_CALIBRATION × MODE_FORMAL` as
`status = CANNOT_CHECK_NOT_APPLICABLE, n_evaluated = 0` — the one cell the
design declared non-applicable in advance. **It is not counted as a pass.**

S5's export counts are printed and are **not** part of the test (design §9(7)):
M 43.76 mean export units against the full trace's 45.08. The conjunct turns on
accuracy dominance alone.

**Null calibration (G0c), the no-alarm assertions paired with the positives
that trip them:**

| control | result | denominator |
|---|---|---|
| `C_ALWAYS_ACCEPT` exact where the oracle rejects | 0 | 1050 |
| `C_ALWAYS_CANNOT_CHECK` exact where decidable | 0 | 1150 |
| `C_RANDOM_VERDICT` exact rate | 0.0832 (ceiling 0.15) | 1250 |
| M against shuffled labels | 0.0811 (ceiling 0.15) | 1245 |

The two zeros are the no-alarm case, and each is paired with a planted positive
that must trip it: the selftest reports **planted positives 4/4**, parents
**23/23**, known-answer **25/25**, separation pair True, G0b True, G0c True.
The selftest report re-executed for this run is **byte-identical** to the one
frozen in PR #239 (sha256 `e2c8030836a58137…`), which is why `git status`
records no change to it.

## 4. Where the content is — ladders per mode, never pooled

**G6 `CROSS_MODE_TRANSFER`, exact-match rate by rung, reported separately by
mode. No pooled ladder is reported anywhere in this receipt.**

| rung | MODE_FORMAL (n = 600) | MODE_COMPUTATIONAL (n = 650) |
|---|---|---|
| L1 `OUTPUT_ONLY` | 0.0833 | 0.0769 |
| L2 `PLUS_PROVENANCE` | 0.1800 | 0.1585 |
| L3 `PLUS_PROBLEM_ARTIFACT` | 0.3583 | 0.3323 |
| L4 `PLUS_VERSION_CALIBRATION_TRANSPORT` | 0.5350 | 0.5785 |
| L5 `PLUS_DEPENDENCE_ROUTE_AUTHORITY_PRESERVATION` | 0.9033 | 0.9123 |
| L6 `FULL_WITNESS` | **1.0000** | **1.0000** |

Monotone in both modes, `ladder_monotone = true` in each, and M non-inferior to
B5 **within each mode** (formal: diff 0.0, 0 discordant, p = 1.0, n = 600;
computational: diff 0.0, 0 discordant, p = 1.0, n = 650). Every G4 step is
one-directional with `y_only = 0` and exact p far below 0.05; the last step
L5 → L6 is +0.092 with 115 discordant, all in the correct direction,
p ≈ 4.8e-35. **No argmax is taken over rungs and no single step is claimed
decisive.** L6 reaching 1.0000 in *both* modes — where V1's computational L6
was 0.9908 because of the six defective instances — is the defect's closure
measured on the primary surface.

**G3 `MECHANISM_BY_OMISSION` (n = 1050): the set of field omissions that lowers
a class's detection recall equals exactly the set of fields its check
requires,** for all eleven injection classes. Including the design's §9(3)
prediction, which is the one that could have been wrong:
`OMITTED_FAILED_ROUTE` is blinded by `M_MINUS_ROUTE_LEDGER` **and**
`M_MINUS_ARTIFACT` and by nothing else — two ablations, as registered, because
a ledger cannot report what it omitted.

**G7 `WITNESS_SELF_CONTAINMENT`, the separating gate, with its own denominator:**

| quantity | value |
|---|---|
| undeclared-shared-upstream instances | 43 (of 1250) |
| M (identity-exporting) exact on them | **1.000** |
| `M_MINUS_REGISTRY_RESOLUTION` (self-contained) exact on them | **0.000** |
| self-contained false acceptances on them | 43 / 43 |
| the two arms identical on every other episode | **true**, n = 1207 |

The separation is total and it is the *mechanism*, not a rate: the
self-contained witness is wrong on every such instance and identical to M
everywhere else, so the finding does not depend on the locus's prevalence
(design §9(6)). This is why the terminal is qualified
`__REQUIRES_IDENTITY_EXPORT`: the compact witness is claim-sufficient **only**
when it exports identities the auditor resolves against the shared registry.
Carried as values, the same twelve fields are not sufficient.

**Per-locus coverage, all six combinations drawn:**
`HIDDEN_DEPENDENCE` 55 / 25 / 20 and `STALE_OR_WRONG_SOURCE` 51 / 26 / 23
across DIRECT / TRANSITIVE_ANCESTOR / UNDECLARED_SHARED_UPSTREAM.

**COVERAGE_LEDGER: `all_registered_mechanisms_exercised = true`, with
`never_exercised` empty for cells, censoring variants and loci.** All ten
censoring variants drew between 5 (`CENSOR_CALIBRATION`) and 15
(`CENSOR_EVALUATOR`) instances. On the development split eight of ten variants
drew zero and the ledger said so; that warning is what made V1's failure
legible in advance, and it is discharged here.

## 5. The parent whose behaviour changed, measured

`A0_PROOF_CERTIFICATE_ONLY` abstains where the environment is unrecoverable —
the declared consequence of correction 1. On this split it records
`missed_censoring = 93 / 100`: it abstains on exactly the **7** computational
`CENSOR_ENV` episodes and misses the other 93 censored episodes, which are the
censoring channels a proof checker genuinely has no access to.
`abstain_on_decidable = 0` — it never abstains where the episode is decidable,
so the change bought no conservatism. Its exact rate is 0.1656 with 950 false
acceptances out of 1050 oracle-rejects, which is the predicted native break:
blind to the intended question and to every registry class.

## 6. A reported diagnostic, correctly labelled this time

`ARM_VS_ARM_IMPLEMENTATION_AGREEMENT` reports **1250/1250 on all eleven checks**
— the same number V1's diagnostic reported in the run where G0b found six
disagreements. That is not a contradiction and it is not a gate: **it compares
M's check table against B5's, arm against arm, and never either against the
oracle**, so it is structurally incapable of seeing a defect in one of the seven
shared implementations. Here it agrees with G0b because G0b passed; in V1 it
agreed with nothing because it could not see what G0b saw. The V2 rename and
rule string say so in the artifact, which is the correction V1's receipt §2.6
owed.

## 7. Determinism — executed, not asserted

Two full protected runs into separate output directories, under one
authorization (the replicate is a reproduction check, not a second protected
result):

| file | check | result |
|---|---|---|
| `ME_X7_PROTECTED_RESULTS_V1.json` | byte-identical | **True** (sha256 `5c35249f7fa2c557fb4ce999f90b44c467da4aefc8968b6516b1615f8dfaee06`) |
| `ME_X7_PROTECTED_EXPECTED_CUSTODY_V1.json` | byte-identical | **True** (sha256 `e75f938ccecc65a11e2099f68b15817c1613a1cb4c242f4e4196a43e06d8dfe1`) |
| `ME_X7_PROTECTED_ANALYSIS_V1.json` | identical modulo the five named wall-clock fields (`wall_ms` per arm, `M_wall_ms`, `B5_wall_ms`, `wall_ratio_b5_over_m`) | **True** |

The claim is stated to exactly what was checked: the analysis file is **not**
byte-identical outright and is not claimed to be. The replicate directory was
given the selftest report before analysis, because without it `G0a` reports
`pass = null, n_evaluated = 0` rather than `pass = true, n_evaluated = 31` —
the code giving "could not check" a value distinct from "checked and fine",
working correctly.

**A determinism-claim overreach found and corrected, in the test and not in the
artifact.** The `COST` flag is a threshold on the wall-clock ratio
(`>= 2.0 → COST_ADVANTAGE_M`), so it is wall-clock-**derived** and is written in
two places, `gates.COST.flag` and `gates.ROUTE.cost_flag`. The design's §8 claim
is "identical *apart from the wall-clock fields it quotes*", which does not
cover a threshold on them; the unit test's strip set nevertheless asserted over
it, so a replicate whose ratio landed near 2.0 could fail a test the design
never claimed. This was **observed once** during this run's verification, on the
inherited V1 test, with results and expected-custody byte-identical and only the
analysis digest differing. Corrected in both the V1 and V2 test files by adding
the two derived keys to the strip set, with the reason in a comment; the study
code is untouched, and rightly so — it is frozen and the protected results file
exists. **Reported, not asserted:** the flag was `COST_ADVANTAGE_M` on both the
canonical run and the replicate, at ratios 2.277 and 2.281, and it is a
reported quantity that never routes anything by itself.

## 8. Authorization and custody discipline

| step | evidence |
|---|---|
| guard armed before the run | `mex7_run.py protected` → **exit 3**, "REFUSED: … absent" |
| distinct from a broken run | a wrong interpreter (python 3.9) gave **exit 1** with a `TypeError` traceback; the refusal is exit 3 |
| seed matched the pre-published commitment | verified before the authorization file was written (§1) |
| design digest acknowledged | `acknowledged_design_sha256` taken from the `origin/main` blob and verified equal to the worktree file |
| token | the operator's instruction for this run, quoted verbatim, not composed by the lane; the standing programme authorization it stands under is quoted in V1's archived file |
| instance count not overridden | no `--per-cell` flag; the run printed exactly **1250 instances** |
| authorization archived after use | moved to `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` |
| guard re-armed | `mex7_run.py protected` → **exit 3** again, and **no output directory was created** |

## 9. What this establishes, and what it does not

**Establishes.** Under the V2 freeze, at 1250 instances across two epistemic
modes, with every hard gate passing and every registered mechanism exercised:

- an **information-matched federation of faithful audit parents is sufficient**
  — no witness residual is detectable against a federation that already holds
  all twelve fields and the full registry, and the two independently written
  check tables agree;
- the **claim-sufficient witness is sufficient at lower export than the full
  human-style trace** (S5: strictly more accurate, 43.76 vs 45.08 mean export
  units, the export figure reported and not tested);
- and it is so **only as an identity-exporting witness** (G7): carried as
  values, the same twelve fields are wrong on every undeclared-shared-upstream
  episode.

The ladder is monotone in both modes, the omission matrix matches the check
table exactly, and the result transfers across modes.

**Does not establish.** A tie with an exact comparator is not evidence that
witnesses add nothing, and it is not evidence that they add something; design
§9(4) fixed that reading before the run. `PARENT_SUFFICIENT` is a successful
terminal of this design and is **not** a residual claim. The generator is a
constructed world with registered defect classes and standing decoys; nothing
here is a measurement of any deployed system. No field status, novelty or
publication authority attaches to this receipt.

**Does not inherit anything from V1.** V1 issued no arm verdict. Everything
above is measured on this split, under a seed committed before it was drawn.

## Terminal

```text
ME_X7_V2_STATUS                        = COMPLETE
ME_X7_V2_PROTECTED_ROUTE               = PARENT_SUFFICIENT
WITNESS_TERMINAL                       = WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT__REQUIRES_IDENTITY_EXPORT
HARD_GATES_FAILED                      = NONE
V1_DEFECT_CLOSED                       = TRUE (G0b cross_implementation 1250/1250; S2 1250/1250)
V1_DEFECT_CELL_STILL_IN_SPLIT          = TRUE (CENSOR_ENV 11 draws, 7 MODE_COMPUTATIONAL)
SEED_REVEALED                          = TRUE
V2_SEED_REUSABLE                       = FALSE
PARENT_SUFFICIENCY_ESTABLISHED         = TRUE
WITNESS_RESIDUAL_ESTABLISHED           = FALSE
WITNESS_SELF_CONTAINMENT_SEPARATED     = TRUE (n = 43; identical elsewhere, n = 1207)
FIELD_STATUS_AUTHORITY                 = NONE
PUBLICATION_AUTHORITY                  = NONE
```
