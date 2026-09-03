# ME-X6 — Comparator Provenance, and Why There Is No Parent-Fidelity Receipt (V1)

**This file is deliberately NOT named `ME_X6_PARENT_FIDELITY_RECEIPT_V1.md`.**
Seventeen files in this programme carry that name and all of them mean the same
thing: *native known-answer tests were executed against a published method
before that method was used inside any arm* (ME-X1: 51/51 PASS, parents named to
source — JTMS/Doyle 1979, GSN change impact, design-by-contract). ME-X6 has no
such tests and cannot have them. Giving this file that name would let an absence
pass as a pass. "Could not check" keeps its own code here, exactly as the study's
own refusal codes do (exit 3 / 4 / 5).

**Applies to:** `ME_X6_OUTCOME_RECEIPT.md`,
`ME_X6_COLLECTIVE_EPISTEMICS_EXACT_STUDY_DESIGN_V1.{md,json}` §1.2–§1.4,
`mex6_arms.py`, PRs #227 / #232 / #234, all on main `517a47e`.

**Effect on the frozen result: none.** `ROUTE = MECHANISM_ESTABLISHED_NOT_A_RESIDUAL`;
every gate verdict, denominator, rate, ablation, ladder count and both registered
predictions stand exactly as receipted. Nothing was re-run, no comparator was
re-fitted, no gate was touched, no protected artifact was regenerated. §5 proposes
a **wording** qualification to the terminal string and to two claims made *about*
the comparator; it changes nothing that was shown.

## 1. What ME-X6's comparator actually is

`B4X_FITTED_UNTYPED` (`mex6_arms.py` sha256 `a72d7de2…`; **comment-only change
since V1's `39311407…`, AST-identical, behaviour unchanged — §10**) is:

- a **linear functional of the fit-window channel half-difference** — `_dir_of`
  computes `sign(Σ_k w_k · (Σ_{late half} c_k − Σ_{early half} c_k))`;
- with **one weight per channel constrained to {−1, 0, +1}**;
- whose weights are learned by **univariate marginal screening**: `fit_signs`
  scores each channel independently by whether its own direction agrees or
  opposes the oracle capability direction, then takes the sign of that score. A
  weight of `0` arises only from an **exact tie** in that per-channel tally;
- fitted once on the public development split and frozen into the design JSON
  (`comparator.frozen_fitted_signs`) before any protected instance existed;
- **constructed for this study.** It is not a re-implementation of any published
  estimator, and no source is named for it anywhere in the design, the code or
  the receipt.

`M_TYPED_COLLECTIVE_STATE` is the **same function** `_dir_of`, over the same
channels, with a different weight dictionary — `TYPED_SIGNS`, declared a priori,
with weights in {−2, −1, 0, +1} (`retractions = −2`; zero on eight channels).

The frozen weight vectors, side by side:

| channel | M | `B4X_FITTED_UNTYPED` | |
|---|---|---|---|
| `preprints` | 0 | +1 | M zeroes; parent forced nonzero |
| `journal_papers` | 0 | +1 | M zeroes; parent forced nonzero |
| `authors` | 0 | +1 | M zeroes; parent forced nonzero |
| `citations` | 0 | −1 | M zeroes; parent forced nonzero |
| `semantic_novelty` | 0 | −1 | M zeroes; parent forced nonzero |
| `disruption` | 0 | +1 | M zeroes; parent forced nonzero |
| `topic_spread` | 0 | 0 | |
| `concentration` | 0 | 0 | |
| `formal_artifacts` | +1 | +1 | |
| `replications_passed` | +1 | +1 | |
| `downstream_reuse` | +1 | +1 | |
| `independent_rederivations` | +1 | +1 | |
| `corrections` | −1 | −1 | |
| `solution_cost` | −1 | −1 | |
| `replications_failed` | −1 | 0 | |
| `retractions` | **−2** | −1 | magnitude differs |

**Information-matching holds and is not in question.** The comparator receives
every channel M receives (asserted by
`test_the_matched_parent_receives_every_channel_M_receives`). What differs is
not information but **representational capacity**: M's weight vector is not a
member of the class the comparator is fitted over.

## 2. Why no parent-fidelity receipt of the ME-X1 kind is possible here

This is a property of the substrate, established by reading
`mex6_generator.py` (sha256 `9f510b54fe23c0e7c4413859fd981ca8486d16cf615a1273cc73ac38c80eb718`)
and `mex6_model.py` (`c0a7298265eaf34bd496a32c74ed29fc3d60c415b295ec5cda669eda09d07d9b`):

1. **The generator emits no bibliographic substrate.** A `FieldWindow` is
   twelve `Period`s, each a mapping from sixteen channel names to integers.
   There are no papers, no reference lists, no citation edges, no author
   records, no venues, no dates beyond the period index. Published
   science-of-science estimators are defined over exactly those objects, so
   **none of them is natively computable on this input** — there is nothing for
   a faithful re-implementation to consume.
2. **The outputs of those method families are handed to every arm as inputs.**
   `disruption`, `semantic_novelty`, `concentration` and `topic_spread` are
   *planted channels*, not quantities any arm derives. The published index
   families are therefore already present in the study at matched information —
   as channel values, available identically to M and to the parent.
3. **What remains is a weighting procedure, and a weighting procedure has no
   known-answer semantics.** ME-X1 could test "retraction propagates OUT" against
   Doyle 1979 because a JTMS has a specified behaviour on a specified input.
   There is no analogous known-answer test for "how should a panel of indicators
   be combined": the answer is fitted, not specified. So even a perfectly cited
   published weighting scheme could not receive a fidelity receipt of the ME-X1
   kind.

**Conclusion — recorded as a design fact, not a gap:** ME-X6's comparator class
admits no native known-answer fidelity establishment. The absence of a
`ME_X6_PARENT_FIDELITY_RECEIPT_V1.md` is correct. What was missing is the
*statement* of that, which this file supplies, together with the capacity check
of §3 which is the thing that can be established in its place.

## 3. What was established instead: a capacity check, with denominators

**Claim under test.** Is M's decision rule outside the reach of an untyped
weighted aggregate of the same channels?

**Method.** Load M's weight vector, expressed as a plain per-channel weight
dictionary, into the **untyped** arm's code path (`_cap_fitted`, the comparator's
own function) and compare it with M arm-for-arm on the public development split
(seed `ME-X6-DEV-20260903`, `per_cell = 2`). No protected instance is touched;
no comparator is re-fitted; nothing is written to the study's results directory.

**Denominator: 56 development instances (28 cells × 2).**

| quantity | result |
|---|---|
| M vs untyped-arm-loaded-with-M's-weights — **capability half** | **56 / 56** |
| M vs untyped-arm-loaded-with-M's-weights — joint | 56 / 56 |
| M exact against the oracle | 56 / 56 |
| untyped-arm-with-M's-weights exact against the oracle | **56 / 56** |
| **CONTROL** — untyped arm with all-+1 weights, capability half vs M | **28 / 56** |

**Self-audit of this check (silent-failure taxonomy).** The *activity* half of
the verdict tuple **could not have differed** between these two arms: both hold
`ACTIVITY_CHANNELS`, and `run_arm` computes the activity direction from the same
keys by the same call for both. Its 56/56 is equal by construction and is **not
evidence**; it is published here only so that no reader mistakes it for some.
The load-bearing number is the **capability** half, and the all-+1 control at
28/56 shows that comparison can fail.

**What this establishes.** M is itself an untyped per-channel weighted aggregate
of exactly the channels the comparator holds. There therefore **exists** an
untyped aggregate at matched information that recovers the conjunction exactly —
constructively, by exhibition. What ME-X6 shows is that the *particular* untyped
aggregate it registered does not.

## 4. Single-stage attribution of the parent's failure

Diagnostic on the same 56 development instances. Each variant is a **hand-set**
weight vector, not a fitted model and not a comparator; it exists only to
attribute the failure to one stage.

| variant | capability-exact | failing strata |
|---|---|---|
| `PARENT_AS_FROZEN` (the registered comparator) | 28 / 56 | I1, I2, I3, I4, I5, I7, I8 |
| `PARENT_PLUS_MAGNITUDES_ONLY` (`retractions −2`, `replications_failed −1`) | 32 / 56 | I1, I2, I3, I5, I7, I8 |
| `PARENT_PLUS_ZEROING_ONLY` (the six M-zeroed channels set to 0, parent's own validation weights kept) | **56 / 56** | none |
| `M_WEIGHTS` | 56 / 56 | none |
| M (typed arm, reference) | 56 / 56 | none |

`PARENT_AS_FROZEN`'s 28/56 instances = 14/28 cells, failing on exactly the seven
predicted strata — the protected receipt's own numbers, reproduced on the public
split, which is the cross-check that this diagnostic is measuring the same object.

**Attribution: the comparator fails because it cannot set a weight to zero.**
Restoring M's magnitudes alone recovers only `I4_RETRACTED_WORK`; zeroing alone
recovers all seven, *keeping the parent's own weaker validation weights*
(`retractions = −1`, `replications_failed = 0`). The `−2` on retractions is not
load-bearing for the separation.

The design already names this mechanism — §5 of the outcome receipt: *"one
global sign per channel cannot **ignore** a channel that moves without
capability"*. What it does not draw is the consequence: a comparator class that
permits zeros is strictly stronger, and **M's own rule is a member of it**.

## 5. The terminal, qualified

Every gate stands. G1a fired, n = 1400 over 28 cells, 14 cells where M wins and
the parent loses and 0 the other way. The separation is real and the study is
honest about M's exactness being by construction and about claiming no residual.

Two statements nevertheless reach past what was shown:

1. **The terminal string.**
   `UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION`
   is a **representation** claim, and §3 exhibits a counterexample: an untyped
   aggregate at matched information that represents the conjunction exactly. The
   modality and the class both need narrowing. Proposed reading, which is what
   the run actually shows:

   ```text
   TERMINAL (as receipted) = UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION
   TERMINAL (qualified)    = FITTED_UNIT_SIGN_UNTYPED_AGGREGATE_DOES_NOT_RECOVER_THE_CONJUNCTION_AT_MATCHED_INFORMATION
   COMPARATOR_CLASS        = ONE WEIGHT PER CHANNEL IN {-1,0,+1}; LEARNED BY UNIVARIATE MARGINAL SCREENING
   COMPARATOR_PROVENANCE   = CONSTRUCTED_FOR_THIS_STUDY; NOT A PUBLISHED-METHOD PARENT; NO FIDELITY RECEIPT IS POSSIBLE (§2)
   REPRESENTATION_NOTE     = M's rule is itself an untyped weighted aggregate of the same channels (§3)
   FAILURE_ATTRIBUTION     = THE COMPARATOR CANNOT ZERO A CHANNEL (§4)
   CAPACITY_MATCHED_PARENT = NOT TESTED — scoped as ME-X6 V2 (§7)
   ```

   `CANNOT_REPRESENT` → `DOES_NOT_RECOVER` is the load-bearing edit.

2. **"The strongest faithful untyped parent"** — the section header in
   `mex6_arms.py`, and design §1.2's *"a real science-of-science modeller given
   the validation channels would fit the combination"*. The implementation does
   not meet that rationale: `fit_signs` screens **per-channel marginals** and
   then sums them with **unit** weights; it never fits a combination. This is
   rationale overreach, **not undisclosed behaviour** — design §1.2 states
   plainly that the parent "**fits one sign per channel**", and the frozen signs
   are published in the design JSON. The disclosure is honest; the superlative is
   not earned. `B4X_FITTED_UNTYPED` is the strongest untyped parent **in the
   unit-sign class**.

**The study's strongest defence, kept here rather than dropped.** One may read
"typing" as *being the a-priori assignment of signed roles, including the
assignment of zero to channels theory says are irrelevant*. Under that reading
design §1.2's "the only difference between them is typing" is exactly true, and
the separation is precisely between a typed weighted reading and an untyped
learned one. A reader will find this defence; it is a good one. It does not
rescue `CANNOT_REPRESENT`, because representation is a property of the function
computed, not of where its weights came from — and the untyped class's range
demonstrably contains an exact member.

## 6. Scope of the absence, stated precisely

Seventeen `*PARENT_FIDELITY*` receipts exist on main. Within the exact-oracle
parent-federation family — the studies that ship a `*_parents.py` module or a
fidelity receipt (`me-x1`, `me-x2`, `me-x2-v2`, `me-x3`, `me-x4`, `me-x5`,
`me-x7`, `me-x7-v2`, `me-f1`, `fg`, `fm-exact`, `sd70-v2`) — **ME-X6 is the only
member with neither**, and the only one whose routed gate turns on an M-vs-parent
comparison without one.

The broader claim that ME-X6 is *the only study in the programme* without
comparator-fidelity establishment is **false and should not be repeated**:
`e30-r12`, `e40-matched`, `h-ext1`, `h-ext1-naturalistic`, `h-ext2`, `pc-r6`,
`pc-r7`, `fm70`, `fmfg-r2` and `sd80` also carry none. Those are a different
study class (agent/LLM empirical designs, not exact-oracle known-answer studies
with registered parent arms), so the absence there is expected and is not
evidence about ME-X6 either way. Checked by name-search over all 1 864 tracked
files with a control pattern that matched (`me-x1`: 15 files contain "fidelity").

## 7. ME-X6 V2 — scoped, not started

A **capacity-matched** untyped comparator is a new study with its own frozen
design and seed. It is **not** an edit to ME-X6, whose V1 result is immutable.

- **Comparator:** an untyped model over the same channels whose weight class
  contains zero and non-unit magnitudes — i.e. any fitter that can *drop* a
  channel (subset selection, an L1 penalty, or a jointly fitted linear/ordinal
  model), learned on the public development split and frozen before any
  protected instance, exactly as V1 froze its signs.
- **The open question V1 cannot answer, and this file does not answer:** §4
  shows a **hand-set** zeroing suffices. Whether a *learned* capacity-matched
  parent would discover that zeroing from the development split is unknown and
  must be measured, not assumed. Nothing here licenses the guess.
- **A tie is a registered success, not a refutation.** ME-X6's own design §1.3
  and §6 already route it: `PARENT_SUFFICIENT` / `TYPING_NOT_SEPARATED`, the
  protocol's contraction to an interpretive framework, "a legitimate publishable
  result and not a failure". V2 must adopt that routing unchanged.
- **Out of scope:** re-running V1, re-fitting `B4X_FITTED_UNTYPED`, or any
  change to a V1 gate, number or authorization.

## 8. Provenance of this audit

Worktree cut from `origin/main` `517a47e`; `/usr/bin/git` for every decision.
Checks run with `/opt/homebrew/bin/python3.12` (the vendored dataclass `slots=`
requires ≥ 3.10; `/usr/bin/python3` is 3.9 and cannot import `mex6_model`).
Every count above is published with its denominator. Absence claims were made
only after a control pattern that **had** to match did match; the `rtk` grep
proxy was caught under-reporting on this very file set (when this audit ran, it returned no match for the
retired `"strongest faithful"` superlative in `mex6_arms.py`, which was then
present at the section header above `B4X_FITTED`; §10 has since retired that
label, so the phrase is genuinely absent now and the anecdote is preserved here
rather than re-runnable), so every absence was re-checked by reading bytes in Python.

**The two checks above are committed as executable assertions**, not prose:
`tests/unit/test_me_x6_exact_study.py::test_M_is_itself_an_untyped_weighted_aggregate_of_the_same_channels`
and `::test_the_comparator_fails_because_it_cannot_zero_a_channel`. They assert
the same facts on the module's own development split (`per_cell = 1`, n = 28
instances / 28 cells); the tables above are the `per_cell = 2` run (n = 56). The
whole file passes at **41 passed, exit status 0**, read directly from `$?` with no
pipe (`python3.13 -m pytest tests/unit/test_me_x6_exact_study.py -q`).

**Both new tests were mutation-checked, and one mutant survived — reported
because it is informative.** Giving `citations` a nonzero weight in M's vector
kills the first test; asserting that magnitude-restoration alone recovers every
stratum kills the second. But setting `retractions` to −1 in M's weight vector
**did not** kill the first test: on this split the untyped arm still reproduces M.
That is not a weak assertion, it is §4's attribution appearing again — the `−2` is
genuinely not load-bearing here — and the first test's strength rests on its
all-+1 control (14/28 at n = 28), which does fail as required.

| pinned file | sha256 |
|---|---|
| `mex6_arms.py` (at V1) | `39311407daec527ff30d51b65a84f2d143ba9514abb39c4b5a4048471febbca0` |
| `mex6_arms.py` (now, comment-only, AST-identical — §10) | `a72d7de2557495262a2f9999f3372078310c8da8ee792a16ed2fea7f5254ea04` |
| `mex6_model.py` | `c0a7298265eaf34bd496a32c74ed29fc3d60c415b295ec5cda669eda09d07d9b` |
| `mex6_generator.py` | `9f510b54fe23c0e7c4413859fd981ca8486d16cf615a1273cc73ac38c80eb718` |
| `mex6_oracle.py` | `1d539ed60ff578606b02a0def5b90b4b0896d4e15e40c5b714ae6ff7087f26d7` |
| `mex6_run.py` | `5d1ed94db0203509708f46161d6f4c5b120c66c899a18b55a96d49dd1338dc37` |
| `ME_X6_..._DESIGN_V1.json` | `c8feaaafb244d4f80f0640631830d8a2b3b8c914362e9ebc10d25273820931fa` |
| `ME_X6_OUTCOME_RECEIPT.md` (pre-banner) | `38729aca5dd42fda71b612814caccae19e6d5f2b14d68625bfe515d4b6c62645` |

The design digest equals the one the outcome receipt names, so the comparator
described here is the one that ran.

**What could not be checked, kept distinct from what was checked and is fine:**
whether any *learned* capacity-matched untyped parent ties M (§7 — not run);
whether the protected split reproduces §4's attribution exactly (not run: the
protected stage is authorization-guarded and the diagnostic was confined to the
public development split by design).

## 9. Summary

| item | changes a number? | changes a gate? | changes the terminal's substance? |
|---|---|---|---|
| 1 — no fidelity receipt is possible for this comparator class (§2) | no | no | no |
| 2 — M is itself an untyped weighted aggregate at matched information (§3) | no | no | **the terminal's wording, yes — §5** |
| 3 — the failure is the inability to zero a channel, not the magnitudes (§4) | no | no | no |
| 4 — "strongest faithful untyped parent" is unearned as a superlative (§5.2) | no | no | no |
| 5 — "the only study in the programme without one" is false as stated (§6) | no | no | no |
| 6 — two labels narrowed and one vacuous-loop guard added (§10) | no | no | no |

`ME_X6_STATUS = PROTECTED_RUN_COMPLETE`, `ROUTE = MECHANISM_ESTABLISHED_NOT_A_RESIDUAL`,
`ME_X6_RESIDUAL_CLAIMED = FALSE`, `FLAGSHIP_GATE = FALSE`,
`FIELD_STATUS_AUTHORITY = NONE` — unchanged.

## 10. Follow-up landed: the same overreach, in the labels

Two labels in the study generalised past the class they covered — the same
defect as the terminal string, smaller. Both are now narrowed. **Prose and
identifiers only: no gate, no datum, no weight, no verdict, no terminal.**

1. **`mex6_arms.py`'s section header.** It called `B4X_FITTED_UNTYPED` "the
   strongest *faithful* untyped parent". Both words are unsupported: §2
   establishes there is nothing here for a parent to be faithful *to*, and §5.2
   that "strongest" holds only inside the unit-sign class. The header now names
   that class and points here. **The edit is comment-only and the module's AST is
   byte-identical to V1's** (`ast.dump` equality against the `origin/main` blob,
   executed); the file's sha256 moves and is re-pinned above with both values.

2. **`test_an_untyped_reading_cannot_separate_the_decoupled_strata`.** Its body
   asserts on `B4X_INFORMATION_MATCHED_UNTYPED`, the **equal-weight** arm — not
   the fitted comparator `G1` tests against — while its name claimed the general
   case, and it sat directly above the test that exhibits an untyped arm which
   *is* exact. Renamed to
   `test_an_equal_weight_untyped_reading_cannot_separate_the_decoupled_strata`,
   docstring corrected, **assertion untouched**.

3. **A third instance, found while renaming: that test could pass vacuously.**
   Its loop `continue`s past every non-decoupled stratum, so a filter matching
   nothing would have skipped every assertion and still reported a pass — a
   counter that never ran. **Verified, not assumed:** the pre-guard version was
   run with the filter mutated to match nothing and it **passed** (exit 0). A
   denominator guard now asserts the covered stratum set equals
   `DECOUPLED_STRATA` and that `checked == 7 × 2 scales = 14` of the 28
   development instances; the same mutant now **fails** (exit 1). This adds a
   guard; it does not change what the test asserts.

4. **The hand-set/learned distinction is now stated in the code**, not only here.
   `test_the_comparator_fails_because_it_cannot_zero_a_channel`'s docstring says
   in full that every vector in it is written down by the test, that none is
   fitted and none is a comparator, and that the rows must **not** be read as
   evidence that a capacity-matched parent would tie M. §7 remains the only place
   that question is scoped, and it remains unstarted.

§5's defence of the study stands unchanged: read "typing" as the a-priori
assignment of signed roles *including the zeros*, and design §1.2's "the only
difference between them is typing" is exactly true.

`tests/unit/test_me_x6_exact_study.py`: **41 passed, exit status 0**, read
directly from `$?`, no pipe. `ruff check` is clean on
`tests/unit/test_me_x6_exact_study.py`.

**One pre-existing lint finding is left untouched and is recorded rather than
silently carried:** `ruff` reports `F401 mex6_model.VALIDATION_CHANNELS imported
but unused` in `mex6_arms.py`. It is **not** introduced here — the same finding
reproduces on the `origin/main` blob this branch was cut from — and it is not
fixed here because removing an import changes the module's AST, which the
comment-only guarantee above forbids for frozen study code. No `ruff` step runs
in CI on this path.
