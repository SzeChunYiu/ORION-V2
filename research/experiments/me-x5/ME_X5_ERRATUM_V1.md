# ME-X5 — Erratum V1 to the protected-run record

**Applies to:** `ME_X5_OUTCOME_RECEIPT.md`, `ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_EXACT_STUDY_DESIGN_V1.md` §4, `ME_X5_PARENT_FIDELITY_RECEIPT_V1.md`, PR #177, PR #183 and the issue #136 terminal comment — all on main `024d97f`.

**Effect on the result: none.** `ROUTE = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`, `FIELD_SUPPORT_LADDER = R1_BENCHMARK_INTEGRATION_VALUE`, M = B5 = 1.0000 in all three native modes, 0 discordant pairs of 1 440, 95% CI [0.0000, 0.0000]. Every rate, gate verdict and terminal in the outcome receipt stands unchanged. Nothing here was re-run and no frozen file was edited: the receipt's sha256 table pins the exact bytes that produced the protected result, and correcting a docstring after the fact would break that pin for no scientific gain. The corrections below are to **claims made about the code**, not to the code or the numbers.

## 1. The M-arm fidelity claim was inaccurate (the substantive item)

**Claimed** — design §4, the parent-fidelity receipt, both PR bodies and the issue comment: *"`M` — the ME arm, compiled to the ORION reference objects (`ReticulateProvenance` for revocation descendants, `assess_evidence_dependence` for independence witnesses, `RelationType` ranks for typed transport, `ProblemContract.scope` for scope, `selective_reopen` for family survival)"*, and the module docstring's *"the existing reference semantics, no new M"*.

**Actual**, verified by `grep -n "ReticulateProvenance\|assess_evidence_dependence\|ProblemContract\|RelationType\|selective_reopen" mex5_arms.py` (`mex5_arms.py` sha256 `d255edf95ac94ed1dcdf18e885e2e6569c32e73bc4079a3508889881bd84c4ba`, unchanged):

| claimed reference object | what M's `_me_family_defeats` / `_me_resolved` actually calls |
|---|---|
| `ReticulateProvenance.descendants` | `mex5_parents.provenance_invalid_units` — a plain `status == INVALID` comprehension |
| `assess_evidence_dependence` | the mode-native `R.independent_groups` |
| `RelationType` ranks | the `RELATION_RANK` dict in `mex5_model` (whose names and order are the parent-owned ones, but the enum is not imported) |
| `ProblemContract.scope` | the mode-native `R.coverage_ok` |
| `selective_reopen` | **invoked**, but its result is discarded: `preserved` feeds only `assert preserved == bool(live or narrow_ok) or True`, which is vacuously true. Family survival is decided by M's own `live` / `narrow_ok` computation |

The same dead-computation pattern appears in `_federation_exact` (`surviving = tms_surviving_families(...)` followed by `_ = surviving`).

**Correct statement.** `M_ME_CROSS_TRANSITION_CONTROL` is a **bespoke composition over the native rule layer**, not a compilation to the ORION reference objects. The five reference objects *are* genuinely used — 18 call sites in `mex5_parents.py` — by the **parent modules**, and therefore by `B5` and by the single-parent arms. The reference-implementation grounding claim holds for the federation; it does not hold for M.

**Why no number moves.** The native rule layer and the reference objects compute the same thing on this input class, which the 20 parent-fidelity known-answer tests establish independently of M: revocation descendants reach exactly the derived family; an alternative support family preserves the commitment under `selective_reopen` and losing every family reopens it; shared confirmed ancestry defeats a `k = 2` family and leaves a `k = 1` family standing; the `RelationType` rank order holds. M and B5 agreeing on 1 440 of 1 440 is a fact about the two compositions, and it is not produced by shared calls into those objects.

**It slightly strengthens, not weakens, the independence story.** Design §10.4 already disclosed that the oracle shell and the arms' compositions are two implementations of one decision format. The correction narrows what M and B5 share to the native rule layer alone — they do not even share the reference-object calls. The claim that *loses* support is the weaker one: that M is the "existing reference semantics, no new M". It is new code.

**Queued as a V2 lane, not fixed here:** make `M` actually consume `ReticulateProvenance`, `assess_evidence_dependence`, `RelationType` and `ProblemContract`; remove the two vacuous asserts (`... or True`, `_ = surviving`); correct the `mex5_arms.py` docstring and design §4. A V2 must freeze its own design and seed before any protected run. This V1 result is immutable.

## 2. "Every rung below 5 fails on exactly one stratum" is false for R1–R3

The outcome receipt §4 states this correctly. The **commit message, the PR #183 body and the issue #136 comment** overstated it. Rungs 1–3 fail on *two* strata:

| rung | non-exact strata | false closures over an unresolved terminal |
|---|---|---|
| `B5_R1_VERDICT_ONLY` | `CENSORED_UNRESOLVED`, `SCOPE_OVERREACH` | 120 |
| `B5_R2_PROVENANCE` | `CENSORED_UNRESOLVED`, `SCOPE_OVERREACH` | 103 |
| `B5_R3_PLUS_DEPENDENCE_ANCESTRY` | `CENSORED_UNRESOLVED`, `SCOPE_OVERREACH` | 78 |
| `B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR` | `SCOPE_OVERREACH` only | 0 |

Only **R4** fails exactly one stratum. The correct short form: *rungs 1–3 fail on censoring and on scope; R4 closes the censoring failures and fails only on scope; R5 closes scope too.* The scope/identity witness is still what only rung 5 supplies.

## 3. `decisive_rung_varies_across_modes = True` is a mechanical argmax, not a finding

The flag is computed as an argmax over the ladder steps' effect sizes. In the formal mode the two candidates are separated by **three instances of 480** (R3→R4 exact-gain on 28 instances against R4→R5 on 25). At this n the study establishes **neither** mode-invariance **nor** mode-variation of the decisive rung. The receipt's prose hedged in one direction only ("mode-invariance is not established"); the symmetric statement is the correct one, and the boolean in the `ROUTE` block should be read as an argmax label, not as a claim of variation.

No new statistic is computed on the protected run to settle this. A difference-of-differences contrast chosen after seeing a single frozen result would be post-hoc; the fix is the wording, not the analysis. What *is* established at this n, and is unaffected: the ladder is monotone in every mode, rung 1 is significantly worse than rung 5 in every mode (p < 1e-6), and the cross-*study* variation is much larger than anything seen across modes here (ME-X1 R4→R5; ME-X4 R1→R2 and R3→R4).

## 4. Disclosure: the G5 null-estimability floor was set on development evidence

`null_floor_n = 100` — below which G5's shuffled-label null is reported `NOT_ESTIMABLE` rather than failed — was introduced **after** observing that the null failed on the 36-instance development split (FORMAL shuffled-label rate 0.364 against the 0.35 threshold, on 11 decidable instances), and **before** the full-scale public dry run. Design §8.3 states that no constant changed after the dry run, which is true but incomplete: this one changed before it, and it sits at the edge of the design's "development-only tuning surface: bug fixes to arm glue" clause rather than squarely inside it.

It did not affect the protected result. All three modes carry n = 440 decidable instances, far above the floor, and the observed nulls are 0.116 / 0.141 / 0.141 against the 0.35 threshold — the gate passes on its own terms with or without the floor, and the floor changed no threshold, only whether an unestimable cell can pass.

## 5. Summary

| item | affects the terminal? | affects any rate? |
|---|---|---|
| 1 — M is a bespoke composition, not a compilation to the reference objects | no | no |
| 2 — R1–R3 fail two strata, not one | no | no (receipt §4 was already correct) |
| 3 — the decisive-rung variation flag is an argmax | no | no |
| 4 — the G5 estimability floor was set on development evidence | no | no |

`ME_X5_STATUS = EXECUTED_PROTECTED`, `ROUTE = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`, `FIELD_SUPPORT_LADDER = R1_BENCHMARK_INTEGRATION_VALUE`, `R2` and `R3` not grantable — unchanged.
