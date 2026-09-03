# ME-X6 — Collective Epistemics: Protected-Run Outcome Receipt

> **QUALIFICATION — read `ME_X6_COMPARATOR_PROVENANCE_AND_NON_FIDELITY_RECEIPT_V1.md`
> before quoting this receipt or its terminal.** **No number, denominator, gate
> verdict or route changes**; nothing was re-run and no comparator was re-fitted.
> Two things are narrowed. (1) The terminal string
> `UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION` is a
> *representation* claim that reaches past what was shown: `M`'s own rule is
> itself an untyped per-channel weighted aggregate of the same channels, so an
> untyped aggregate at matched information that recovers the conjunction exactly
> **exists** (exhibited, 56/56 capability-half on the public development split,
> control 28/56). What was shown is that the *registered* comparator does not
> recover it: read the terminal as
> `FITTED_UNIT_SIGN_UNTYPED_AGGREGATE_DOES_NOT_RECOVER_THE_CONJUNCTION_AT_MATCHED_INFORMATION`.
> (2) `B4X_FITTED_UNTYPED` is **constructed for this study, not a published-method
> parent**, and no parent-fidelity receipt of the ME-X1 kind is possible for it —
> stated there as a design fact, with the reason. The comparator's failure is
> attributed to a single cause: it cannot set a channel weight to zero.

**Run date:** 2026-09-03
**Design:** `ME_X6_COLLECTIVE_EPISTEMICS_EXACT_STUDY_DESIGN_V1.json`,
sha256 `c8feaaafb244d4f80f0640631830d8a2b3b8c914362e9ebc10d25273820931fa`,
frozen in PR #227 and corrected **pre-run** in PR #232, both merged before this run.

## 0. Route

```text
ME_X6_PROTECTED_ROUTE = MECHANISM_ESTABLISHED_NOT_A_RESIDUAL
TERMINAL              = UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION
ME_X6_RESIDUAL        = NOT CLAIMED (no routing path awards one)
FLAGSHIP_GATE         = FALSE
FIELD_STATUS_AUTHORITY = NONE
```

**What is claimed.** On the registered family of decision problems, the typed
reading of the observable channels is exact, and an information-matched untyped
aggregate — one fitted global sign per channel, holding **every** channel the
typed arm holds — is not. It fails on exactly the seven strata predicted in
advance and nowhere else, and the typed channel responsible for each invariance
is exhibited by ablation.

**What is not claimed.** **M's exactness is by construction and is not
evidence.** M's typed score reads exactly the channels this generator uses to
encode capability; design §1.3 said so before the run, and no routing path
awards an ME-X6 residual on the strength of that gap. Nothing here is a claim
about any real scientific field, corpus, database or time period.

**The honest null**, had the parent tied: *no residual detectable in the
registered decision problems the untyped aggregate already solves exactly*, and
X6 would have contracted to an interpretive framework under the protocol's own
§6 rule. That terminal existed and was reachable; it did not fire.

## 1. Seed reveal (post-run half of the pre-published commitment)

```text
committed pre-run : c0889a1c6919294d74e35534aaee4cc609af349ef973862cc069c12b8292584a
PROTECTED_SEED_V1 : ME-X6-PROTECTED-15559daa704c6dc63ed6167ca668dc8f2d35682f472e74d5
```

```console
$ printf '%s' 'ME-X6-PROTECTED-15559daa704c6dc63ed6167ca668dc8f2d35682f472e74d5' | shasum -a 256
c0889a1c6919294d74e35534aaee4cc609af349ef973862cc069c12b8292584a  -
```

Custody file `~/.orion-custody/me-x6/PROTECTED_SEED_V1.txt`, mode 0600, 64 bytes,
hashed to the commitment **before** the authorization file was written.

## 2. What kind of result this is

**A constructive separation, not a sampling study.** Every arm's decision is a
strict integer sign comparison, so an arm's verdict is **constant across the
instances of a cell**. That is measured, not assumed:

```text
G8_VERDICT_CONSTANCY_WITHIN_CELL   pass = true
  instances_per_cell = 50   n_cells = 28   varying_arm_cells = []
```

Zero of 28 cells showed a varying verdict for any arm (`C_RANDOM` excluded by
construction). **So no gate but G0c reports a p-value.** An exact paired test
over 1 400 instances would report an effective *n* of **28 cells** at an
inflated denominator — the failure this study's own taxonomy names. G1a, G1b,
G4 and G6 are deterministic comparisons over cells. Every gate below carries
**both** denominators.

The 50 instances per cell bought **structural coverage, not power**: each cell's
verdict is now shown invariant under 50 different baselines, step magnitudes and
step onsets.

**G0c is the one exception** and keeps exact binomial tails, because `C_RANDOM`
draws per instance and the shuffled-label null permutes across instances — real
sampling quantities even here. Those tails are computed in exact rational
arithmetic; the float form raises `OverflowError` at n = 1400, which would have
crashed this run under the design as first merged (§7).

## 3. Gates — every one, both denominators

| gate | pass | instances | cells |
|---|---|---|---|
| G0a `KNOWN_ANSWER` (hard) | **true** | 33 | 28 |
| G0b `ORACLE_SELF_AGREEMENT` (hard) | **true** | 1400 | 28 |
| G0c `NULL_CALIBRATION` (hard) | **true** | 1400 | 28 |
| G8 `VERDICT_CONSTANCY_WITHIN_CELL` (hard) | **true** | 1400 | 28 |
| G1a `M_AHEAD_OF_MATCHED_PARENT` | **true** | 1400 | 28 |
| G1b `MATCHED_PARENT_AHEAD` | did not fire | 1400 | 28 |
| G2 `ANTI_CONSERVATISM` | **true** | 200 | 28 |
| G3 `MECHANISM_BY_OMISSION` | **true** | 1400 | 28 |
| G4 `INFORMATION_LADDER` | **true** | 1400 | 28 |
| G5 `HOSTILE_INVARIANCE_SUITE` | **true** | 1400 | 28 |
| G6 `CROSS_SCALE_TRANSFER` | **true** | 1400 | 28 |
| G7 `REGISTERED_PREDICTION` | **true** | 1400 | 28 |
| COVERAGE_LEDGER (reported) | all 28 cells exercised, `never_exercised: []` | 1400 | 28 |

G0a's denominator is **33 = 28 cells checked + 5 planted positives**, read from
the selftest report rather than recomputed — a hardcoded `len(CELLS) + 4` had
silently stopped matching when the fifth positive was added (§7).

**G1a and G1b are separate positive tests and neither is the other's negation.**
G1a fired; G1b did not. A tie would have fired neither.

### 3.1 Null calibration, with the positives that trip it

| control | result | denominator |
|---|---|---|
| `C_ALWAYS_RISE` exact where capability is not RISE | **0** | 1000 |
| `C_ALWAYS_FLAT` exact where capability moves | **0** | 600 |
| `C_RANDOM` capability hits vs derived 1/3 | 491, upper-tail p = **0.0887** | 1400 |
| M on shuffled labels vs majority-class rate | 0.2236 vs 0.5714, p = **1.0** | 1400 |

Both reference values are **derived, not chosen**: 1/3 because every arm reads
the activity half directly so the joint match reduces to a three-way capability
guess, and the majority-class rate computed from the split. This gate carries no
threshold constant.

`C_ALWAYS_FLAT`'s overall exact rate is **0.5714**, printed beside the
majority-class capability rate of **0.5714**, so a degenerate control's score
cannot be read as skill.

The two zeros are the no-alarm case, and the selftest pairs each assertion with
a planted positive that must trip it — **5/5**, including one that flips I4's
typed capability by giving the channels per-channel step magnitudes, which
demonstrates the constancy gate G8 is able to fire at all.

## 4. The separation, per cell

```text
M_TYPED_COLLECTIVE_STATE     exact on 28 / 28 cells
B4X_FITTED_UNTYPED           exact on 14 / 28 cells
cells M wins and the parent loses : 14
cells the parent wins and M loses : 0
```

The 14 are exactly the seven predicted strata × both scales.

### 4.1 Hostile-invariance suite (G5), each its own positive test

| invariance | M | matched parent | n |
|---|---|---|---|
| I1 duplicates | 1.000 | **0.000** | 100 |
| I2 paraphrase | 1.000 | **0.000** | 100 |
| I3 mass low-information | 1.000 | **0.000** | 100 |
| I4 retracted work | 1.000 | **0.000** | 100 |
| I5 citation ring | 1.000 | **0.000** | 100 |
| I6 venue migration | 1.000 | 1.000 | 100 |
| I7 field-size scaling | 1.000 | **0.000** | 100 |
| I8 fashion/concentration | 1.000 | **0.000** | 100 |
| I9 delayed validation | 1.000 | 1.000 | 100 |
| I10 independent rediscovery | 1.000 | 1.000 | 100 |
| X6-I7 one breakthrough | 1.000 | 1.000 | 100 |

The parent's failures are **0.000, not partial** — a mechanism, not a rate,
which is what verdict constancy means.

### 4.2 Mechanism by omission (G3): declared, then measured

| ablation | degraded | predicted |
|---|---|---|
| `M_MINUS_CORRECTION_RETRACTION` | `I4_RETRACTED_WORK` | `I4_RETRACTED_WORK` |
| `M_MINUS_REPLICATION` | `I9_DELAYED_VALIDATION` | `I9_DELAYED_VALIDATION` |
| `M_MINUS_REDERIVATION` | `I10_INDEPENDENT_REDISCOVERY` | `I10_INDEPENDENT_REDISCOVERY` |
| `M_MINUS_FORMAL` | `X6I7_ONE_BREAKTHROUGH` | `X6I7_ONE_BREAKTHROUGH` |
| `M_MINUS_REUSE` | none | none |
| `M_MINUS_COST` | none | none |

Every ablation blinds **exactly** the stratum declared to depend on it. The two
non-carriers blind nothing, which is the assertion that stops this being a gate
that could not fail.

## 5. Ladders, per scale, never pooled

| rung | SCALE_SUBFIELD exact cells | SCALE_PROBLEM_FAMILY exact cells |
|---|---|---|
| `L1_ACTIVITY_ONLY` | 6 / 14 | 6 / 14 |
| `L2_PLUS_ATTENTION` | **5 / 14** | **5 / 14** |
| `L3_PLUS_SEMANTIC` | 5 / 14 | 5 / 14 |
| `L4_PLUS_NETWORK` | 6 / 14 | 6 / 14 |
| `L5_PLUS_VALIDATION` | 7 / 14 | 7 / 14 |

**The ladder is not monotone, and that is the finding, not a defect.** Every
rung is fitted on its own channel set, and L2 is *still* worse than L1: one
global sign per channel cannot **ignore** a channel that moves without
capability, so the attention channel destroys `I5_CITATION_RING`, which L1 gets
right precisely by not holding it. G4's positive test is the count comparison
top-vs-bottom (7 > 6, both scales), and it passes.

**No argmax is taken over rungs**, and the two scales are reported separately
throughout.

## 6. Both registered predictions, confirmed exactly

**P-MEX6-1** — the matched untyped parent fails exactly where the true
capability direction contradicts a channel it must give one global sign to:

```text
predicted support : I1, I2, I3, I4, I5, I7, I8
observed inside   : I1, I2, I3, I4, I5, I7, I8
observed outside  : []          <- the falsifier
predicted but not observed : [] <- the other falsifier
```

**P-MEX6-2** — the fitted untyped ladder is not monotone:

```text
predicted regressions : ["L1_ACTIVITY_ONLY -> L2_PLUS_ATTENTION"]
observed regressions  : ["L1_ACTIVITY_ONLY -> L2_PLUS_ATTENTION"]
```

Both were registered from the public development split before any protected
instance existed, both had explicit falsifiers, and both held.

## 7. Two defects, and where they were caught

Neither reached a protected outcome; both are receipted because the near-miss is
the point.

**A hard gate that would have crashed this run.** `binom_upper_tail` multiplied
`comb(n, i)` by a float and raises `OverflowError` at n = 1400. G0c is hard, so
the protected run would have died — and had the exception been caught it would
have returned `inf`, and `inf > 0.05` would have made a null-calibration gate
**incapable of failing**. Reproduced against `main` as merged, then fixed to
exact rational arithmetic in PR #232.

**PR #227 was merged while its revision was in flight**, so five prepared
corrections did not land with it. They were landed as an explicit **pre-run**
correction (#232): no protected outcome existed, so the design's no-rescue
clause was not engaged, and the seed commitment was unchanged and unused. The
other four: the frozen comparator signs were refit at run time rather than read
from the design; the all-pass route never read G7, so a failed P-MEX6-1 would
still have received the terminal claiming it held; G4 failed on a reversal that
is real; and G0a's denominator was hardcoded and had stopped counting what was
checked.

**Provenance.** Four were raised by Cursor Bugbot, whose check reported
**NEUTRAL** rather than a failure — green-adjacent and easy to merge past. Each
was reproduced before being acted on, and the ladder finding was **reframed
rather than patched**, because measurement showed the implicit premise (that
fitting the rungs would restore monotonicity) was wrong.

**One process failure of my own:** `pytest` was piped to `tail`, so the shell
reported the pipe's exit status and a red suite read as green; a broken test was
committed before it was caught. Exit status read directly thereafter.

## 8. Custody and determinism — executed, not asserted

| step | evidence |
|---|---|
| guard armed before the run | `mex6_run.py protected` → **exit 3** |
| seed vs pre-published commitment | matched **before** the authorization was written |
| design digest | taken from the `origin/main` blob, equal to the worktree file |
| token | the operator's standing authorization, quoted verbatim, not composed by the lane |
| instance count | printed exactly **1400**; no `--per-cell` |
| authorization archived | `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` |
| guard re-armed | **exit 3** again, and no output directory created |
| results file | **byte-identical** across two runs (`46525b94736780bc…`) |
| custody file | **byte-identical** across two runs (`83d4e1ce41778127…`) |
| analysis file | **not** byte-identical; identical **modulo `wall_ms`** |
| selftest | 28/28 known-answer, 28/28 fit-window-decidable, 28/28 M-exact, **5/5** planted positives |

Refusal codes are distinct: **exit 3** for authorization, **exit 4** for the
seed, **exit 5** for drifted frozen signs. All three were exercised before the
run. "Could not check" never shares a code with "checked and fine".

## 9. Scope, stated as a limit

The registered protocols require temporal predictive validation over a real
corpus. **This design contracts that to synthetic time** — a planted latent
trajectory with a fit window and a holdout — and the contraction is declared in
design §1.1, not absorbed. The real-corpus route carries the dateless
current-state-field hazard (item 11 of the silent-failure assessment) for which
no build exists.

`decidable_from_fit_window` held on **1400/1400** instances, so the known-answer
property is asserted per instance rather than in prose.

The result is a statement about a constructed family. It says what an untyped
aggregate **cannot represent** given these channels; it does not say that any
real bibliometric aggregate behaves this way.

## Terminal

```text
ME_X6_STATUS                      = PROTECTED_RUN_COMPLETE
ROUTE                             = MECHANISM_ESTABLISHED_NOT_A_RESIDUAL
TERMINAL                          = UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION
RESULT_CLASS                      = CONSTRUCTIVE_SEPARATION_NOT_A_SAMPLING_STUDY
M_OPTIMAL_BY_CONSTRUCTION         = TRUE (declared pre-run; the gap is not the finding)
ME_X6_RESIDUAL_CLAIMED            = FALSE
HARD_GATES                        = G0a, G0b, G0c, G8 -- all pass
REGISTERED_PREDICTIONS            = P-MEX6-1 CONFIRMED, P-MEX6-2 CONFIRMED
INFERENTIAL_STATISTICS            = G0c ONLY
TEMPORAL_HOLDOUT                  = SYNTHETIC_TIME_DECLARED_SCOPE_CONTRACTION
SEED_REVEALED                     = TRUE
FLAGSHIP_GATE                     = FALSE
FIELD_STATUS_AUTHORITY            = NONE
PUBLICATION_AUTHORITY             = NONE
```
