# ORION-V2 Failure Ledger

This ledger begins before implementation because research-process failures are scientific evidence. Failure history is append-only: a repaired defect remains visible, and a later green result may not erase how it was obtained.

## Retained failure classes

These are **failure vocabularies to keep detecting**, not a claim that every class currently has an open critical defect.

- `COVERAGE_GAP` — a declared knowledge-taxonomy branch lacks adequate native and changed-vocabulary search.
- `REPO_COLLISION` — a proposed omission or novelty was already represented in ORION V1.
- `DONOR_RECONSTRUCTION_FAILURE` — the native parent cannot yet be reproduced faithfully.
- `FALSE_STRUCTURAL_ANALOGY` — apparent cross-domain proximity disappears when assumptions or semantics are restored.
- `DONOR_PRODUCT_TIE` — the strongest donor composition matches the candidate ORION mechanism.
- `NONIDENTIFIABLE` — the intended distinction cannot be learned under the current probe/intervention family.
- `CENSORED_ROUTE` — a required source or evaluation route was unavailable and cannot be counted as a negative search result.
- `V1_PARITY_RISK` — a proposed V2 factorization may lose a frozen V1 capability.
- `PREMATURE_IMPLEMENTATION` — code or outcome-generating execution begins before the V1 freeze gate.
- `AUTHORITY_LAUNDERING` — local research or engineering evidence is used as scientific/novelty/adoption authority.
- `SILENT_MODEL_SUBSTITUTION` — a model endpoint serves a different model than the one requested, with a success status and no warning, so artifacts carry an unrecorded producing-model identity. Guard: log the **served** model id on every call and assert it against a frozen pin (fail closed); where an earlier campaign lacks that record, its artifacts may be reused only as a labelled non-gating panel. First observed 2026-09-02 (E40-m5′ Stage-2b/2c: `glm-5.2` → `glm-5.3`, `glm-4.6` → `glm-5.3-flash`; the m2/m3 served model is unrecoverable — 0 hits across 1,810 artifact files).
- `DEGENERATE_PROBE_STATISTIC` — a proposed statistic lacks the shared structure it needs to rank anything, so a null result measures the statistic rather than the hypothesis. A specialization of `NONIDENTIFIABLE` for constructed proxies. Guard: establish the statistic's dynamic range on the substrate **before** using it as a truth proxy. First observed 2026-09-02 (E40-m5′ Stage-2c: replica-consensus Jaccard J = 0.028 mean, range 0.009–0.052 — independent seed-replicas of the same cell share ≈3 % of their edges).
- `MANDATE_EXPLORATION_COLLAPSE` — a binding cycle-1 prompt mandate anchors an iterative arm on its mandated first config, which it then keeps re-choosing, so the search never samples the axis the objective varies along and a feedback-following control fails. Severity tracks mandate specificity and is model-dependent. Guard: run any mandated design alongside an unmandated planted control on the same channel before reading its trajectories. First measured 2026-09-02 (E40-m5′ Stage-2d: unmandated PASS 0.9877 reaching the optimum by cycle 2; regime anchor FAIL 0.9518; exact-seed mandate FAIL 0.0233 with `frac` never leaving 0.0 across nine cycles).
- `UNGATED_CONTROL_VERDICT` — an analysis records control verdicts without consuming them, so it can emit a scientific verdict while a registered control is failing. Guard: `evaluate_gates()` takes the control verdicts as input and refuses every gate when one fails, with a fixture proving the refusal fires. First observed 2026-09-02 (E40-m5′ Stage-2c analysis emitted a routing terminal while its planted control failed; repaired in the Stage-2d freeze, not retrofitted to the frozen Stage-2c script).
- `NONREPRODUCIBLE_FROZEN_ARTIFACT` — a "frozen" artifact is regenerated from its committed seed through iteration over an unordered container, so per-process hash randomisation yields a different artifact from the same commitment while every seed record, sha256 and freeze receipt remains internally consistent and correct: the custody chain is honest and the artifact is still not reproducible. Guard: regenerate the frozen artifact in a fresh process under at least two `PYTHONHASHSEED` values and compare hashes, and forbid RNG draws ordered by an unordered container (the reproducible-builds practice of rebuilding in a deliberately varied environment and comparing bit-for-bit, applied to a research split). **Near miss, not a realised defect** — unlike every other class in this list, no contaminated result was produced: it was caught before any protected artifact existed. Found by regenerating the split from a second process and comparing digests, not by a review or an auditor. First observed 2026-09-02 (FG70 `ORION-FG-L5-EXACT-V1`, PR #181: three generator planters drew decision assignments while iterating `set(...)` of signature tuples; fixed at the root and guarded by a cross-`PYTHONHASHSEED` behavioural test and a source-level test).

- `FORECLOSED_FAILURE_MODE` — a world is built so that the failure its primary endpoint measures **cannot occur in it**, so a hard validity gate fails and the study cannot be rescued without degrading an arm. Distinct from `NONIDENTIFIABLE`: the effect is not merely unlearnable under the probe family, it is absent by construction. The tell is a validity gate that survives a full revival attempt while every arm reads a clean zero on a detector proven to fire on the same records. The operative variable is **not** how expensive the evidence is to obtain — in ME-F1, finding a witness is exactly what the budget buys — but whether *"do I have warrant for this?"* is ever a **judgment call for the agent**. Guard: before freezing an endpoint, establish that its failure mode has dynamic range in the world as built, and specifically that the agent's own warrant status is **not** already unambiguous to it. A tool that returns `WITNESS_FOUND` versus `INCONCLUSIVE` in plain text, with an abstention option at no extra cost, leaves a competent agent no ambiguity to exploit and no self-deception channel — so over-assertion has nothing to arise from. First observed 2026-09-03 (ME-F1 G0e: `SIMPLE_DIRECT` laundered 0 of 121 claims, then 0 of 106 **bare verdicts** after the warrant field was removed from its interface entirely; ME-X1's 492 laundered updates arose where warrant status was itself a judgment. Routed `CANNOT_CHECK`; no protected campaign dispatched).

- `UNGUARDED_DEPENDENT_CHECK` — a registered condition makes one check undecidable, and the recoverability guard is written on the check whose *semantics* name that condition but not on a different check that also consumes the erased field. The second check re-derives from absent state and reports a definite verdict, so **"I could not check this" is silently converted into a substantive finding**. The tell is a three-way oracle-versus-implementations gate failing on one (cell, check) pair with no spread, while an arm-versus-arm concordance diagnostic reads 100 % — an arm-vs-arm comparison is structurally incapable of seeing a defect in an implementation the two arms *share*. Guard: for every censoring condition, declare the **set** of checks it makes undecidable — not the one check it is named for — and assert observed-equals-declared as a generator-validity invariant; keep the three-way comparison against the oracle as the hard gate and never let arm-vs-arm concordance stand in for it. Its repair carries a second trap, `REPAIR_THAT_DELETES_ITS_OWN_EVIDENCE`: extending the check table while leaving a "exactly one censored check" count invariant in force makes the generator re-draw every episode the fix was written for, so the gate goes green because the hard cases left the split. First observed 2026-09-03 (ME-X7 V1 protected run: G0b `ORACLE_SELF_AGREEMENT` 1244/1250 and G5 `S2_REPLAY_SUPPORT` 1244/1250, the same 6 instances, all `CENSORED_UNDECIDABLE × MODE_COMPUTATIONAL × DIRECT × C_ARTIFACT_DIGEST`, symmetric between the arms; routed `CANNOT_CHECK`, no arm verdict issued, re-frozen as ME-X7 V2 with both halves of the repair. Measured counterfactual: the table extension alone drops `CENSOR_ENV` from 8 draws to 2 and removes all six).

The nine classes below were relocated on 2026-09-04 from a refused standalone-paper candidate
(`DO_NOT_OPEN`, merge `323894f`, `papers/prospectuses/SILENT_FAILURE_MODES_ADMISSION_ASSESSMENT_V1.md`),
whose disposition named this ledger and the owning lane PRs as the durable homes for the findings.
They are **process-failure vocabularies, not a scientific result and not a novelty claim**: the
unification of vacuity and coverage as one mutation framework is Kupferman, CONCUR 2006, and the
empirical census slot — roughly a fifth of formulas trivially valid on a new design's first runs —
is Beer, Ben-David, Eisner and Rodeh, FMSD 18(2):141-163, 2001, p. 141, an IBM RuleBase experience
report rather than a methodologically specified census. Records, evidence grades and search scopes:
`research/failures/2026-09-silent-failure-modes-relocation/`.

- `VACUOUS_CONTRAST` — a treatment arm and its comparator dispatch to the same code with identical
  fields, so a reported agreement is `x == x`. **Not caught by the denominator question**, which is
  the reason it needs its own vocabulary rather than folding into a counter-never-ran class: a gate
  that never ran reports `0`, which invites "out of how many?"; a comparator with no contrast reports
  `1.000`, which reads as strength and has no denominator to interrogate. The catching question
  differs in kind — *could these two arms ever have differed?* Guard: assert the arms' code paths
  diverge, and report shared-implementation comparisons as shared rather than counting them as
  independent evidence. First observed 2026-09-03 (ME-X7 parent-fidelity: 8 vacuous comparison
  *items* spanning 6 of 11 gates, 4 fully vacated and 2 partially — items, not gates; development
  artifact only, no protected artifact ever existed). Second instance in the same window, found by
  a verifier asked whether a test could fail: the cross-`PYTHONHASHSEED` guard written against
  `NONREPRODUCIBLE_FROZEN_ARTIFACT` compares a run at `0` against parametrizations `0`, `1`, `12345`,
  so the `0` case compares a process against itself and passes on the unfixed code — the guard
  against vacuity contained a vacuous parametrization.
- `STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE` — a registered clause whose verdict is fixed by the
  construction of the stimulus, in either direction, so its result is a property of the design and
  not a measurement. Distinct from `NONIDENTIFIABLE` (a distinction unlearnable under the probe
  family) and from `DEGENERATE_PROBE_STATISTIC` (a statistic with no dynamic range): here the
  clause's own pass/fail is determined before any model is run. Both directions read as results —
  an unsatisfiable clause as an empirical negative, an unfailable one as a clean pass — and neither
  has a denominator. Guard: before freezing a clause, establish that both of its verdicts are
  reachable under the frozen stimulus, and check the exchangeability of the arms as a generator
  invariant. First observed 2026-09-04 (PRA GP2a: under R3 the two arms of all 120 frozen
  `F3_P2_CANON` instances are an exact source-exchange of one another while the label flips, so
  expected accuracy of any classifier is exactly 0.5 — **implementing the clause as registered would
  have produced a permanently unpassable gate reading like an empirical negative**; and two sibling
  clauses are unfailable because the two arms render identically, one of which ran and reported
  `probe_R2_true_removal_at_chance = True`, a zero-violation pass that could never have been
  otherwise).
- `HANDICAPPED_COMPARATOR` — a comparator is isolated by an asymmetry in the harness — a procedural
  rule its prompt omits, or a budget below the one its procedure needs — rather than by the mechanism
  under test. Distinct from `DONOR_RECONSTRUCTION_FAILURE`, which is an inability to reproduce the
  parent at all: here the parent is reproduced and then disadvantaged. Guard: assert prompt and
  budget parity between arms as a precondition on the comparison, and refuse the comparison until it
  holds. First observed 2026-09-03 (ME-F1: the mechanism's prompt names a procedural switch-tool
  rule the parent's does not while both hold the same information; the lane routed `CANNOT_CHECK`
  and made parity a hard precondition before any protected dispatch). **The repair magnitudes
  nominated for this class are `CANNOT_VERIFY` and must not be quoted**; the budget instance was
  additionally attributed to the wrong arm as nominated. The class is warranted on the mechanism
  and the precondition, not on a measured inversion.
- `TERMINAL_OVERSTATES_ITS_PROCEDURE` — a terminal string or receipt sentence claims more than the
  procedure that produced it: an impossibility where the evidence supports only non-recovery by one
  fitting procedure, or a margin borrowing the authority of a null that tested a different contrast.
  Distinct from `AUTHORITY_LAUNDERING`, which imports authority from outside the result. Guard: for
  each terminal, name the procedure that would have to fail for it to be false, and check that the
  registered statistic actually covers the comparison the prose draws. First observed 2026-09-03
  (ME-X6: `UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION` falsified by
  exhibition, 56/56 on the capability half against a 28/56 control, the comparator differing from
  the mechanism only in a weight dict it cannot set to zero; H-EXT-1: a +2.1 pp parent margin decided
  by 11 tasks under a registered bare threshold, beside a 0/2000 permutation null that tests the
  gated-versus-always-on contrast and not that margin).
- `REGISTERED_SCOPE_DIVERGENCE` — a runner evaluates a narrower clause than the one registered, and
  the clause passes on the half it evaluated. Guard: bind the machine-readable registration to the
  runner and assert clause-by-clause that observed scope equals registered scope; a narrowed clause
  is `CANNOT_CHECK`, never `pass`. First observed 2026-09-03 (PRA GP2a registered under R0 *and* R3
  in the design JSON, evaluated under R0 only; the rollup recorded `pass: true` while probing R3 all
  along at 0.594 and 0.542 against a 0.80 threshold).
- `UNPINNED_SUBSTRATE_CONDITION` — the served-model pin is satisfied by every artifact and the
  experimental condition still changes underneath a frozen prompt, because the pin certifies
  *identity* and not *behaviour*. A strengthening of `SILENT_MODEL_SUBSTITUTION`, not a duplicate:
  that class's guard fired correctly and was insufficient. Guard: record and gate on the behavioural
  envelope as well as the identity — output-token distribution against the prior run, the
  content-block types actually parsed, and the fraction of calls at the cap. First observed
  2026-09-03 (E30-R12: all 119 envelopes record the frozen served id `glm-5.3`; the identical frozen
  prompt at 61,557 input tokens completed in 763 output tokens five days earlier and hit the 6,000
  cap on 116 of the re-runs, the budget consumed by a `thinking` block the arm's parser never reads;
  `EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ`, 0 of 480 evaluations produced).
- `CHECKER_STAGED_ON_THE_WRONG_SUBSTRATE` — a cross-check's argument defaults point at a development
  corpus or an absent toolchain, so the check runs against something other than the thing it
  certifies. Guard: make the staged path and the toolchain identity assertions inside the receipt
  verifier, so that creating the stale artifact flips a check to FAIL. First observed 2026-09-03
  (ME-X3: the default `--dir` holds 20 development task_ids disjoint from the protected ids —
  contamination additionally requires an explicit `--report` pinned to the protected slot, which is
  the accurate and weaker form; and a bare-name toolchain default that on this machine exits 1 with
  "no default toolchain configured". Both near-misses; the toolchain one is **fail-loud** and is
  retained for the staging error, not as a silent mode).
- `CHECK_THAT_RUNS_AND_CANNOT_FIRE` — a check executes, on the right file, for the right string, and
  is incapable of reporting the defect it exists to catch. Guard: a CI job that **proves the gate can
  fail** against a fixture of genuine violations, with the fixture asserted to carry the real-world
  form of the defect. First observed 2026-09-03 (log-wrap blindness: pdflatex wraps its transcript at
  column 79 mid-word, so `Citation .* undefined` returns a clean log — measured 0 raw matches on a
  planted key with `grep -c LaTeX` at 20 as the control, and the committed verbatim fixtures break at
  exactly 68+11 and 69+10 characters; repaired sites proven by real pdflatex runs, and the blindness
  is **site-specific to three workflow gates**, since every other checker also accepts the unwrapped
  `There were undefined references.`). The class's sharpest member is the apparatus itself: the
  meta-gate built to prove those gates could fail planted **only unwrapped fixtures**, so all eight
  registered sites read green while the deployed gates were blind to the only form the defect takes —
  measured from the historical blobs as 8 site-policy entries and zero occurrences of `wrap` at
  `fbe647c`. Repairing the pattern alone would have left the gates exactly as inert. Two further
  members are recorded at reduced strength and must be quoted at it: an assertion that matched the
  very log line saying the file was **not** found, because the failure message contains the filename
  (a genuine inversion, never on `main`, and the consequence it would have licensed was blocked one
  layer up); and a vacuous-loop mechanism — a `continue` past every non-matching case, so a filter
  matching everything skips every assertion — verified by re-execution (unguarded exit 0 under the
  mutation, guarded exit 1) with the guarded exemplar present since its first commit and **no
  realised instance found**.
- `RENDERED_SURFACE_SUBSTITUTED_FOR_THE_FACT` — a rendered, filtered or proxied summary is read as
  the fact it summarises. The failure is **bidirectional**, which is what makes it more than a
  tooling note: toward apparent strength when it stands in for a claim ("nothing changed", "the
  suite is green"), and toward apparent failure when it stands in for a status, prompting the repair
  of a healthy artifact. Guard: before acting on a summary, execute the thing it summarises, and ask
  both what would have to run for this to be false **and** what would have to run for it to be true;
  use the unfiltered binary for any command whose result drives a decision. First observed
  2026-09-03. Its realised instances are **operational** — a command proxy returning `0` on a
  non-empty file and swallowing a requested `-c` count; `pytest` piped to `tail`, so the shell
  reported the pipe's status and a red suite read as green; `gh run list` rendering in-progress runs
  as elapsed time, which read as "timed out" would have prompted weakening a suite that was never
  failing. The programme's standing rule against asserting absence from absent printed output is
  what caught the third, which is evidence the detector was already held rather than discovered.

### Corrections to entries above, recorded rather than applied

This ledger is append-only, so two earlier entries are corrected here rather than edited in place.

- `UNGATED_CONTROL_VERDICT` above says an analysis *"records control verdicts without consuming
  them"*. The admission assessment's re-read of the artifact corrects the mechanism: `evaluate_gates()`
  **never receives** the control verdicts; the rollup writer records them as a sibling of `analysis`.
  The corrected form is the stronger one — the function cannot decline to consume what it is never
  passed — and the class, its guard and its first-observed date are unaffected. The same re-read
  found the stale-terminal consequence to be **counterfactual**: the repository contains zero
  programmatic consumers of that rollup.
- `SILENT_MODEL_SUBSTITUTION` above names two substitutions. The probe recorded **three** across
  four requests, all at HTTP 200: `glm-5.2`→`glm-5.3`, `glm-5.1`→`glm-5.3` and
  `glm-4.6`→`glm-5.3-flash`, with `glm-5.3`→`glm-5.3` as the negative control. The corollary belongs
  with the class: a run that logs **no** served id has an *inferred*, not a verified, producing
  model, and must be labelled as such.

Every concrete failure must preserve its source identities, affected claims and reopening conditions. No failure may be deleted merely because a later theory is more successful.

## Retained concrete failure records

- `research/failures/2026-08-parallel-wave3-ownership-collision/README.md`
- `research/failures/2026-08-wave4-recovery-and-ci-preterminal-defects/README.md`
- `research/failures/2026-08-wave5-epoch-and-chain-binding-defects/README.md`
- `research/failures/2026-08-parity-preflight-test-expectation-drift/README.md`
- `research/failures/2026-09-silent-failure-modes-relocation/README.md` — twenty-five relocated session records behind the nine classes above, each with its evidence grade, its corrections and the scope of any absence claim. Four are `CANNOT_VERIFY` and are recorded as such; one group (`05`) is explicitly **operational hygiene rather than a scientific failure class**, per the admission assessment §3 and §9. That group is named here rather than classed, because
  recording an operational hazard as a scientific failure class would repeat the error the refusal
  identifies — bundling unlike things because each was surprising. The hazards, with the test that
  settles each: a PR can read `state: MERGED` while its work is absent from `main`, when it was
  merged into an integration branch whose own PR had already landed
  (`git merge-base --is-ancestor <mergeCommit> origin/main`, control required); `--delete-branch`
  closes every PR stacked on the deleted branch as its base, and recovery is a new PR — the cascade
  is proven by timeline events, while the refusal to reopen rests on first-party testimony only;
  a multi-commit squash-merge makes landed work look unlanded in two mutually confirming ways, and
  the sound test is a tree-hash comparison for the path; a two-dot diff folds the other side's
  additions into the deletion column, which is where a large phantom-deletion count comes from —
  three-dot is the form that isolates a side; a pipe reports the pipe's exit status, so a red suite
  reads as green; and a command proxy can return `0` on a non-empty file, which is what authorises
  a destructive overwrite. The record states its own contamination limit: the corpus was collected while a paper was being assessed from it, which changed what lanes looked for and how they worded it — a performative-evaluation instance the programme already has a coordinate for (P-D's C09), with no model of that response, so nothing in it may be read as a prevalence or a base rate.
- `research/experiments/e40-matched/E40_M5P_STAGE2D_OUTCOME_RECEIPT.md` — E40-m5′ Stage-2d: the Stage-2c control failure is attributed to the cycle-1 mandate (D2 `PROMPT_IMPLICATED`, all controls PASS); the model channel alone is exonerated, though the m3-form arm passed under the earlier model and fails now, so the cause is an interaction whose magnitude is not estimable (the m2-era model is unrecoverable). Stage-2c stays `CHECKER_INVALID__NO_VERDICT`; the E40 line stays open.
- `research/experiments/e40-matched/E40_M5P_STAGE2C_OUTCOME_RECEIPT.md` — E40-m5′ Stage-2c: registered planted positive control FAILED (terminal quality 0.6412 vs 0.9877 in m3, 1.0 in m2), so the campaign's computed routing terminal was **not** filed; disposition `CHECKER_INVALID__NO_VERDICT` and the E40 line stays open. Carries the three classes above. Cause discrimination is frozen as Stage-2d (`E40_M5P_STAGE2D_PLANT_DISCRIMINATION_DESIGN_V1`).
- `research/experiments/me-x7/ME_X7_OUTCOME_RECEIPT.md` — ME-X7 V1: hard gate G0b failed on a lane defect (`UNGUARDED_DEPENDENT_CHECK`); routed `CANNOT_CHECK`, witness terminal `NONE`, no arm verdict, protected seed burned. Re-frozen as `research/experiments/me-x7-v2/` with the two coupled corrections its §7 prescribes, and closed there: the V2 protected run passed every hard gate with `cross_implementation_agree` 1250/1250 and `S2_REPLAY_SUPPORT` 1250/1250 **while the cell that exposed the defect was still in the split** (`CENSOR_ENV` 11 draws, 7 in `MODE_COMPUTATIONAL`) — `research/experiments/me-x7-v2/ME_X7_V2_OUTCOME_RECEIPT.md`.

Their current closure classification is machine-recorded in:

`research/closure/CRITICAL_FAILURE_DISPOSITION_WAVE06_V1.json`

That receipt may report zero **known open critical local correctness/integrity/authority defects** while protected scientific evidence remains unresolved in other gates. In particular:

- missing independent semantic evaluators are G1/G5 custody evidence;
- strongest parent comparator identity is G4 evidence;
- protected parity and naturalistic/prospective value are G1/G5 evidence;
- scientific novelty/publication/field authority is G8 external authority.

These are not silently converted into repaired defects.

## Reopening rule

The critical-failure gate reopens if current CI exposes a real correctness/integrity/authority defect, if a hostile control demonstrates fail-open behavior, if an identity/custody binding is bypassable after outcome access, or if a historical repair no longer reproduces.

It reopens equally on the three conditions the 2026-09 relocation earns, each of which is invisible
to the clauses above because each produces a *passing* artifact:

- a gate is shown to be incapable of reporting the defect it exists to catch — including a
  meta-gate whose fixtures do not carry the real-world form of that defect;
- a comparator is shown to share a code path with its treatment arm, or to be isolated by a prompt
  or budget asymmetry rather than by the mechanism under test;
- a registered clause is shown to be structurally determined — unsatisfiable or unfailable under the
  frozen stimulus — or to have been evaluated at a narrower scope than registered.

A verdict resting on any of these is withdrawn to `CANNOT_CHECK`; it is not converted into a
repaired defect, and a later green result does not erase how the earlier one was obtained.
