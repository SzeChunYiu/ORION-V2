# ME-X3 — Protected outcome receipt

**State date:** 2026-09-03
**Study:** ME-X3, formal mathematical discovery and regime change
**Design:** `ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.{md,json}`, sha256
`d13b7a7a30bb932afc899f2993dbf64ce4a15c4fb8f3041a50f48cd9c8d82ae9`
**Protected instances:** 540 (8 families x 60; F8_TRANSFER contributes
60 source/target *pairs* = 120 scored instances, so its 120 rows are not independent
and its held-out reuse rate is scored over the 60 pairs, not over 120)
**Results sha256:** `6a68271c62982f55d06085154d9b3716b530f26c14776bfc05f5a8c424a03bf2`
**Custody sha256:** `27574873f463a05274405801d4378e27f94fc2dffe44f0bd9a5095c1759492bf`
**Analysis sha256:** `bd2c9a620db3b7b5827bb27f874ff0256ff078794b12d44e2b056ae1f71ad0a6`
**Selftest sha256:** `23e22773a606f630e03bfcacc0ee0f441a043f1b2698acf2a944c44f5fb15ce6`
**Verification sha256:** `0a61e7b594398a6fca1f3cb44fa527e0f8d9b381ddc0130295339a857d4c68d4`

**Seed reveal.** The commitment `cb799f89499cea4a088c6df071e9ce12bff2fceb02c4adc06ab7ce4eecdbb3f8` was published in
the frozen design before the split existed. The seed is now revealed:

```text
ME-X3-PROTECTED-5c3e5ecb553e127a575e0e9d64612659939d55e0b7b49145
```

sha256 of the custody seed file equals the commitment, and the 540-instance split
regenerates from this seed with an identical, order-sensitive task sequence. Both
statements were executed, not asserted -- see section 11.

# ROUTE: PARENT_SUFFICIENT

M 0.944 vs B5 0.944, paired exact p=1: no protected decision advantage over the strongest faithful federation (cost 421 vs 427 expansions, -1.5%)

Ladder terminal (H-EXT-3): `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`

## 1. Authorization and custody

The protected stage ran **once**, and `analyze` ran **once** on its output.

- Authority: coordinator, under the operator's standing authorization of 2026-09-02
- Verbatim instruction: "run all the computation tasks.. finish all the researxh asap"
- Recorded: 2026-09-03 by ME-X3 lane (Claude Fable 5.1), ORION-V2
- Design sha256 at authorization: `d13b7a7a30bb932afc899f2993dbf64ce4a15c4fb8f3041a50f48cd9c8d82ae9`
- Custody seed sha256: `cb799f89499cea4a088c6df071e9ce12bff2fceb02c4adc06ab7ce4eecdbb3f8` (matches the commitment frozen
  in the design before the split was generated)
- The seed itself remains in `~/.orion-custody/me-x3/` and is not in the repository.
- Authorization state: ARCHIVED to `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json`; the runner's guard is re-armed and a second protected run requires a new explicit authorization
- Authorization sha256: `cdea0081b321782cbc8f8bbef8c93851c057f419d9038794ae94cdbf88db0f9c` (equals the
  `authorization_sha256` recorded inside the protected results, so the file that
  gated the run is the file archived here)

The runner refuses to generate the protected split unless both the authorization
file is present and the custody seed's sha256 equals the frozen commitment.

## 2. Outcome vector, per arm (pooled)

| arm | validity | fidelity | minimal action | joint | false change | false defer | drift missed | false drift alarm | held-out reuse | mean expansions |
|---|---|---|---|---|---|---|---|---|---|---|
| `A0_DIRECT` | 0.396 | 0.930 | 0.263 | 0.263 | 0.000 | 0.000 | 1.000 | 0.000 | 0.250 | 97 |
| `A1_RETRIEVAL` | 0.420 | 0.930 | 0.387 | 0.387 | 0.000 | 0.000 | 1.000 | 0.000 | 0.350 | 275 |
| `A2_SELF_REFLECT` | 0.352 | 0.930 | 0.320 | 0.320 | 0.000 | 0.000 | 1.000 | 0.000 | 0.167 | 220 |
| `A3_DISCOVER_AND_PROVE_PARENT` | 0.569 | 0.930 | 0.498 | 0.498 | 0.000 | 0.000 | 1.000 | 0.000 | 0.350 | 248 |
| `A4_LEMMA_ABSTRACTION_PARENT` | 0.604 | 0.930 | 0.574 | 0.548 | 0.000 | 0.000 | 1.000 | 0.000 | 0.933 | 478 |
| `B5_R1_VERDICT_ONLY` | 0.826 | 0.993 | 0.952 | 0.804 | 0.000 | 0.026 | 0.000 | 0.000 | 0.933 | 493 |
| `B5_R2_SATURATION` | 0.826 | 0.993 | 0.952 | 0.804 | 0.000 | 0.026 | 0.000 | 0.000 | 0.933 | 427 |
| `B5_R3_FRONTIER` | 0.826 | 0.993 | 0.952 | 0.804 | 0.000 | 0.026 | 0.000 | 0.000 | 0.933 | 427 |
| `B5_R4_SEMANTIC` | 0.972 | 0.993 | 0.952 | 0.944 | 0.000 | 0.026 | 0.000 | 0.000 | 0.933 | 427 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 0.972 | 0.993 | 0.952 | 0.944 | 0.000 | 0.026 | 0.000 | 0.000 | 0.933 | 427 |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | 0.983 | 0.993 | 0.952 | 0.944 | 0.000 | 0.015 | 0.000 | 0.000 | 0.967 | 421 |

## 3. Per family — the primary report

| family | n | M joint | B5 joint | M-only | B5-only | diff | exact p | route |
|---|---|---|---|---|---|---|---|---|
| `F1_DIRECT_SEARCH` | 60 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F2_MISSING_LEMMA` | 60 | 0.950 | 0.950 | 0 | 0 | +0.000 | 1 | TIED |
| `F3_REPRESENTATION_CHANGE` | 60 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F4_DECEPTIVE_CHANGE` | 60 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F5_PROBE_OR_COUNTEREXAMPLE_NEEDED` | 60 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F6_UNDERDETERMINED_OR_CANNOT_CHECK` | 60 | 1.000 | 1.000 | 0 | 0 | +0.000 | 1 | TIED |
| `F7_SPECIFICATION_MISMATCH` | 60 | 0.933 | 0.933 | 0 | 0 | +0.000 | 1 | TIED |
| `F8_TRANSFER` | 120 | 0.808 | 0.808 | 0 | 0 | +0.000 | 1 | TIED |

A pooled average may not hide a family-specific failure. The table above is the
primary report; the pooled row in §2 is secondary. The ladder in §5 is likewise
reported per rung and never argmaxed across steps separated by a few instances.

### The tie is established by a POSITIVE test, not by failing to find a gap

This distinction decides what may be quoted. A tie asserted by "the difference was
not significant" is a negated gap and carries the power of the test with it. That is
not what happened here.

- Paired discordance is **0 of 540**, and **0 in every one of the eight
  families** -- there is no instance on which one of M and B5 achieved the joint
  endpoint and the other did not.
- The two arms are nevertheless **not the same arm**: they emit differing
  `(validity, fidelity, action)` triples on **6** of 540 rows, and they differ on
  components -- validity 531 vs 525, false-defer
  8 vs 14, missed-escalation
  6 vs 0.

So a discordant pair was reachable and none occurred. M solves a handful of
instances the federation does not and misses escalation on a comparable handful;
the trades cancel exactly on the registered joint endpoint. This is the ME-X5
pattern and it is quotable on its own.

### Where the parents are optimal by construction

The oracle is exhaustive over a finite equational theory, and its caps
(40000 expansions, word length 8) strictly dominate the caps every
arm runs under (5000 total, 250 per search). On the families the parents
already solve exactly there is therefore **no room for any controller to win**, and
a tie there is a property of the problem, not evidence about M. This receipt states
that plainly rather than banking the tie as a result.

## 4. Specification fidelity by realized drift subtype

| subtype | n | M | B5 | A0 (proof only) | M drift missed |
|---|---|---|---|---|---|
| `ABSTRACTION_ELEVATION` | 19 | 0.842 | 0.842 | 0.000 | 0.000 |
| `DEGENERATE_TRIVIALIZATION` | 14 | 1.000 | 1.000 | 0.000 | 0.000 |
| `FAITHFUL` | 22 | 1.000 | 1.000 | 1.000 | 0.000 |
| `MATERIALLY_STRENGTHENED` | 1 | 0.000 | 0.000 | 0.000 | 0.000 |
| `MATERIALLY_WEAKENED` | 2 | 1.000 | 1.000 | 0.000 | 0.000 |
| `NOTATIONAL_COLLAPSE` | 2 | 1.000 | 1.000 | 0.000 | 0.000 |

Counts are the realized draw after oracle-verified rejection sampling, not the
generator's proposal weights. The realized mixture is heavily unbalanced, and
**no claim is made from the thin cells** -- `MATERIALLY_STRENGTHENED` (n=1), `MATERIALLY_WEAKENED` (n=2), `NOTATIONAL_COLLAPSE` (n=2) carry too few instances to
support any comparison, and they are printed only so the denominators are visible
rather than hidden. The rows that carry weight are `FAITHFUL`,
`ABSTRACTION_ELEVATION` and `DEGENERATE_TRIVIALIZATION`.

The `A0 (proof only)` column is the control that shows this table is measuring
something: the proof-only parent scores 0.000 fidelity on every drift subtype
while scoring 1.000 on `FAITHFUL`. It reports alignment it never checked.

## 5. Gates

| gate | result | reading |
|---|---|---|
| G0 oracle and parent fidelity | PASS | the oracle, fixtures, parent fidelity and null calibration all hold |
| G1 M vs top-rung federation | NOT MET | **this is the finding, not a defect.** G1 asks whether M beats the strongest faithful parent federation. It does not. That is what `PARENT_SUFFICIENT` means, and it is a registered, publishable terminal |
| G2 anti-conservatism | PASS | M does not buy its score by escalating or deferring more than B5 |
| G3 mechanism by omission | PASS on the 6 families it can bind | **not a global pass**: 6 families gated and all degrade; 2 families have no registered ablation and are NOT gated (see below) |
| G4 interface ladder | PASS | the ladder is monotone and terminates at the top rung |

G1 is reported as **NOT MET** rather than FAIL because the gate is a test for a
residual, and the study is designed so that finding no residual is a real answer.
A gate that can only be reported as `FAIL` would make the pre-registered
`PARENT_SUFFICIENT` route unreportable.

### G3 detail

| family | ablation | M − ablation | exact p | degrades |
|---|---|---|---|---|
| `F1_DIRECT_SEARCH` | — | — | — | not gated: control family: nothing should escalate, so no omission can break it; gated by G2 instead |
| `F2_MISSING_LEMMA` | `M_MINUS_LEMMA_LEVEL` | +0.950 | 1.39e-17 | yes |
| `F3_REPRESENTATION_CHANGE` | `M_NEVER_CHANGE_REPRESENTATION` | +1.000 | 1.73e-18 | yes |
| `F4_DECEPTIVE_CHANGE` | `M_MINUS_FALSE_CHANGE_PENALTY` | +1.000 | 1.73e-18 | yes |
| `F5_PROBE_OR_COUNTEREXAMPLE_NEEDED` | `M_MINUS_COUNTEREXAMPLE_PROBE` | +1.000 | 1.73e-18 | yes |
| `F6_UNDERDETERMINED_OR_CANNOT_CHECK` | `M_MINUS_UNRESOLVED_TERMINAL` | +1.000 | 1.73e-18 | yes |
| `F7_SPECIFICATION_MISMATCH` | `M_MINUS_SPECIFICATION_PRESERVATION` | +0.567 | 1.16e-10 | yes |
| `F8_TRANSFER` | — | — | — | not gated: the held-out target admits independent re-invention as well as reuse, so the transfer ablation cannot degrade it by construction |

### G4: the H-EXT-3 interface-information ladder

| rung | joint rate |
|---|---|
| `B5_R1_VERDICT_ONLY` | 0.804 |
| `B5_R2_SATURATION` | 0.804 |
| `B5_R3_FRONTIER` | 0.804 |
| `B5_R4_SEMANTIC` | 0.944 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 0.944 |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | 0.944 |

**The pooled ladder above is secondary.** Pooling hides where the rung actually
binds, so the same ladder is reported per family, which is the primary form:

| family | n | R1 verdict | R2 saturation | R3 frontier | R4 semantic | B5 top rung | M |
|---|---|---|---|---|---|---|---|
| `F1_DIRECT_SEARCH` | 60 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `F2_MISSING_LEMMA` | 60 | 0.950 | 0.950 | 0.950 | 0.950 | 0.950 | 0.950 |
| `F3_REPRESENTATION_CHANGE` | 60 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `F4_DECEPTIVE_CHANGE` | 60 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `F5_PROBE_OR_COUNTEREXAMPLE_NEEDED` | 60 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| `F6_UNDERDETERMINED_OR_CANNOT_CHECK` | 60 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `F7_SPECIFICATION_MISMATCH` | 60 | 0.667 | 0.667 | 0.667 | 0.933 | 0.933 | 0.933 |
| `F8_TRANSFER` | 120 | 0.808 | 0.808 | 0.808 | 0.808 | 0.808 | 0.808 |

Read per family, the pooled step from `R3` to `R4_SEMANTIC` is not a diffuse
gain spread over the corpus. It comes from exactly two families:
`F5_PROBE_OR_COUNTEREXAMPLE_NEEDED` (0.000 -> 1.000) and
`F7_SPECIFICATION_MISMATCH` (0.667 -> 0.933), each n=60. Every other family is
flat across the whole ladder. These are whole-family steps on 60 instances, not
an argmax over a handful, which is why the step is quoted at all; no claim is
made about the ordering of `R1`, `R2` and `R3`, which are indistinguishable in
every family.

`F8_TRANSFER` is flat at 0.808 for a different reason than `F1`, `F3`, `F4` and
`F6` are flat at 1.000: nothing in the ladder touches transfer, so no rung can move
it. Combined with its lack of a bindable ablation under G3, `F8_TRANSFER` contributes
120 rows to the pooled denominator while contributing **no discriminating signal to
either G3 or G4**. That is a real limitation of this study and is stated rather than
left to be inferred; it is also why the per-family tables above are the primary
report.

The top rung and M coincide in **every family**, not merely on average. That is
the content of `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`: once the
federation's internal channel carries semantic content, the federation already
does what M does, so the residual is a statement about the interface standard
and not about M's control policy.

## 6. Ablations

| arm | validity | fidelity | minimal action | joint | false change | false defer | drift missed | false drift alarm | held-out reuse | mean expansions |
|---|---|---|---|---|---|---|---|---|---|---|
| `M_ALWAYS_CHANGE_REPRESENTATION_WHEN_STUCK` | 0.983 | 0.993 | 0.952 | 0.944 | 0.000 | 0.015 | 0.000 | 0.000 | 0.967 | 384 |
| `M_EQUAL_EXTRA_SEARCH_INSTEAD_OF_TRANSFORM` | 0.983 | 0.993 | 0.867 | 0.859 | 0.000 | 0.015 | 0.000 | 0.000 | 0.967 | 367 |
| `M_LOCUS_LABELS_SHUFFLED` | 0.983 | 0.993 | 0.867 | 0.859 | 0.000 | 0.015 | 0.000 | 0.000 | 0.967 | 358 |
| `M_MINUS_COUNTEREXAMPLE_PROBE` | 0.837 | 0.993 | 0.841 | 0.804 | 0.000 | 0.126 | 0.000 | 0.000 | 0.967 | 484 |
| `M_MINUS_FALSE_CHANGE_PENALTY` | 0.983 | 0.993 | 0.841 | 0.833 | 0.111 | 0.015 | 0.000 | 0.000 | 0.967 | 385 |
| `M_MINUS_LEMMA_INVENTION` | 0.852 | 0.993 | 0.791 | 0.783 | 0.000 | 0.146 | 0.000 | 0.000 | 0.517 | 294 |
| `M_MINUS_LEMMA_LEVEL` | 0.763 | 0.993 | 0.667 | 0.657 | 0.000 | 0.233 | 0.000 | 0.000 | 0.250 | 135 |
| `M_MINUS_LOWER_LEVEL_DISPOSITION` | 0.983 | 0.993 | 0.952 | 0.944 | 0.000 | 0.015 | 0.000 | 0.000 | 0.967 | 384 |
| `M_MINUS_OBSTRUCTION_CLASS` | 0.983 | 0.993 | 0.867 | 0.859 | 0.000 | 0.015 | 0.000 | 0.000 | 0.967 | 367 |
| `M_MINUS_PRESERVATION_CONTRACT` | 0.983 | 0.993 | 0.952 | 0.944 | 0.000 | 0.015 | 0.000 | 0.000 | 0.967 | 421 |
| `M_MINUS_SPECIFICATION_PRESERVATION` | 0.985 | 0.930 | 0.881 | 0.881 | 0.000 | 0.015 | 1.000 | 0.000 | 0.967 | 415 |
| `M_MINUS_TRANSFER_REUSE_TRACKING` | 0.974 | 0.993 | 0.965 | 0.957 | 0.000 | 0.024 | 0.000 | 0.000 | 0.883 | 451 |
| `M_MINUS_UNRESOLVED_TERMINAL` | 0.872 | 0.993 | 0.841 | 0.833 | 0.000 | 0.000 | 0.000 | 0.000 | 0.967 | 421 |
| `M_NEVER_CHANGE_REPRESENTATION` | 0.872 | 0.993 | 0.841 | 0.833 | 0.000 | 0.126 | 0.000 | 0.000 | 0.967 | 415 |

## 7. F8 held-out reuse: carry versus no-carry

- M, carrying its own invention: 0.967
  (58/60)
- M minus transfer tracking, no carry: 0.883
  (53/60)

The held-out target admits independent re-invention from the registered candidate
pool as well as reuse of the source artefact, so F8 measures held-out reach at the
lemma level, not reuse gain, and does not support a strong reusability claim. The
counterfactual is printed so the reading is visible rather than inferred.

## 8. External proof-checker cross-check

Lean 4.33.1 (commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`) re-checked 40 files emitted from the **protected** corpus (`PROTECTED`; every task_id in the protected split and none in development): **20** accepted as proof terms with `#print axioms` certifying axiom-freedom, **20** corrupted files rejected with the registered `Derives` type mismatch, **0** `CANNOT_CHECK`, and **0** disagreements with the exhaustive oracle.

Both arms of the control are non-empty: 20 accepts and 20 rejections. A checker that accepted everything would show 0 rejections, and one that rejected everything would show 0 accepts; neither is what happened, so the `0 disagreements` figure is a measurement and not an unrun counter.

**Path note.** The frozen `mex3_lean.py` defaults to `--dir lean/` and writes
`lean/LEAN_RECEIPT.json`. That directory holds the **development** build and is
untracked, so re-running the frozen defaults would produce a development receipt at
the registered default path. The protected receipt therefore lives at
`results/ME_X3_LEAN_RECEIPT_PROTECTED_V1.json`, and
`verify_receipt_claims.py` asserts the default path stays empty so the two can never
be confused.

The encoding is an inductive `Derives` proposition with an explicit proof term per
derivation, not a Boolean function proved `true` by `rfl`; a corrupted derivation
counts as correctly rejected only when it fails with a type mismatch on a
`Derives` term, and any other failure is `CANNOT_CHECK`.

## 9. What this does and does not establish

Established, within a finite equational theory with an exhaustive oracle:
the separation between proof validity and specification fidelity; the behaviour
of the registered arms on the minimum-escalation decision; the ablation structure;
the interface ladder; the cost frontier.

**The null, stated precisely.** The correct reading of `PARENT_SUFFICIENT` here is
*no residual is detectable in the registered decision problems the parents already
solve exactly*. It is **not** "no residual exists". The registered problems are
drawn from a finite equational theory with an exhaustive oracle whose caps dominate
every arm's budget; that is the regime in which the parents are optimal by
construction, and it is the only regime this study observed.

**Not** established: anything about controller behaviour at Mathlib scale, where
no exhaustive oracle exists and proof search dominates cost. Mathlib was excluded
because an unbounded library makes the minimum-escalation oracle uncomputable, not
because of resources. Any reading of this receipt as evidence about frontier Lean
theorem proving is a misreading.

## 10. No rescue

No threshold, family, arm, budget, generator constant or gate was changed after
these outcomes were inspected, and none may be. The route above is terminal for
ME-X3 V1. A further question requires a new prospective identity.

## 11. Verification of this receipt's own claims

Every reproduction and no-alarm claim above is executed by
`verify_receipt_claims.py`, which writes
`results/ME_X3_RECEIPT_VERIFICATION_PROTECTED_V1.json`. It distinguishes three
states -- `PASS`, `FAIL` and `COULD_NOT_CHECK` -- and exits 0, 1 and 3
respectively, so "could not check" can never be read as "checked and fine".
Every check that could pass by never running carries a **control**: an input that
must produce the opposite verdict. A check whose control does not fire is
reported `COULD_NOT_CHECK`, never `PASS`.

| check | state | detail | control that fires |
|---|---|---|---|
| `frozen_bytes_bind_to_the_run` | PASS | 8 code files + design + authorization | a one-byte edit to any hashed file flips this to FAIL |
| `seed_reveal_matches_commitment` | PASS | sha256(seed file bytes) == frozen commitment | a perturbed seed does not match the commitment |
| `split_regenerates_from_revealed_seed` | PASS | 540 tasks, order-sensitive, 14 custody-retained fields, 0 mismatches | perturbed seed yields a different split (['F1-0004-1ee8c0', 'F1-0005-dd518f']) |
| `selftest_reproduces` | PASS | 16/16 tests, byte-equal to the committed report | the report carries per-test verdicts; a regressed oracle flips one to failed |
| `G1_headline_recomputed_from_raw` | PASS | M 510/540, B5 510/540, discordant 0 | M and B5 emit differing (validity,fidelity,action) on 6 rows, so a discordant pair was reachable |
| `tie_is_positive_not_a_negated_gap` | PASS | 0 discordant of 540; the arms are not the same arm (6 rows differ) | if the two arms were identical by construction, differ would be 0 and this check FAILs |
| `drift_counters_are_not_vacuous` | PASS | drift_n=38, faithful_n=502; M drift_missed_rate=0.000 | A0_DIRECT (proof-only parent) scores drift_missed_rate=1.000 on the same denominator |
| `G3_scope_is_declared` | PASS | 6 families gated and all degrade; 2 NOT gated (F1_DIRECT_SEARCH, F8_TRANSFER) | each not-gated family carries an explicit reason; no ablation is scored where none exists |
| `lean_crosscheck_on_protected_corpus` | PASS | 40 files, 20 kernel-accepted, 20 negative controls rejected, 0 CANNOT_CHECK, 0 disagreements; 20 task_ids all in PROTECTED, 0 in DEVELOPMENT | 20 corrupted derivations were rejected for the registered Derives mismatch, so the checker is not accept-everything |
| `registered_default_lean_path_is_not_stale` | PASS | lean/LEAN_RECEIPT.json absent; the protected receipt is results/ME_X3_LEAN_RECEIPT_PROTECTED_V1.json; lean/ holds a DEVELOPMENT build and is untracked | creating that file would flip this check to FAIL |

Totals: **10 PASS, 0 FAIL, 0 COULD_NOT_CHECK.**

The four silent-failure modes this is written against, and where each is refuted:

1. *A counter that never ran, reporting 0 violations.* The drift counters run on
   `drift_n`=38 and `faithful_n`=502 nonzero denominators, and `A0_DIRECT`
   scores 1.000 missed drift on the same denominator where M and B5 score
   0.000. The counter discriminates.
2. *A contrast that could not exist, reporting 1.000 vs 1.000.* M and B5 differ on
   6 rows, so the discordance statistic had somewhere to land.
3. *A sentence nobody executed.* The seed reveal, the split regeneration, the
   selftest reproduction and the design's own byte-identical regeneration were run,
   with a wrong-seed control for the regeneration.
4. *A rendered status trusted in place of the thing itself.* The Lean cross-check
   was rebuilt from the protected corpus and re-run; the pre-existing `lean/`
   directory held the **development** corpus and was not reused. Its 20 negative
   controls were rejected, so the checker is not accept-everything.

## Terminal

```text
ME_X3_STATUS = EXECUTED_ONCE
ROUTE = PARENT_SUFFICIENT
LADDER_TERMINAL = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL
PRIMARY_ENDPOINT = joint (validity AND fidelity AND minimal action)
M  joint = 0.9444   (510/540)
B5 joint = 0.9444   (510/540)
PAIRED_DISCORDANCE = 0 of 540, and 0 in every one of the 8 families
TIE_ESTABLISHED_BY = POSITIVE_TEST (6 of 540 rows differ, so a discordant pair was reachable)
G0 = PASS
G1 = NOT_MET   (no residual over the strongest faithful parent; this is the finding)
G2 = PASS
G3 = PASS_ON_6_OF_8_FAMILIES   (2 families carry no registered ablation and are NOT gated)
G4 = PASS
LEAN_CROSSCHECK = PROTECTED_CORPUS 20_ACCEPTED 20_CONTROLS_REJECTED 0_DISAGREEMENTS
RECEIPT_SELF_VERIFICATION = 10_PASS 0_FAIL 0_COULD_NOT_CHECK
NULL_READING = no residual detectable in registered decision problems the parents
               already solve exactly; NOT "no residual exists"
MATHLIB_SCALE_GENERALITY = OUT_OF_SCOPE
FIELD_STATUS_AUTHORITY = NONE
```
