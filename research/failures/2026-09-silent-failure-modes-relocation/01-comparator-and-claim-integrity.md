# 01 — Comparator and claim integrity

Detail file of `2026-09-silent-failure-modes-relocation`. Read `README.md` first.

Records here share one shape: **the arm a result is measured against, or the sentence that reports
it, claims more than the procedure that produced it.**

---

## D1 — Vacuous comparison: two arms on one code path

**Class** `VACUOUS_CONTRAST` · **Status** `REALISED_IN_A_DEVELOPMENT_ARTIFACT`

`research/experiments/me-x7/ME_X7_PARENT_FIDELITY_RECEIPT_V1.md` lines 119-120:

```text
| `M_CLAIM_SUFFICIENT_WITNESS`         | 1.000 | 0 | 0 | 43.5 |
| `B5_STRONGEST_FAITHFUL_AUDIT_PARENT` | 1.000 | 0 | 0 | 43.5 |
```

The two arms are provably bit-identical, not merely observed to agree: same `kind`, `native=None`,
the same fields, one `MODULE_CHECK` table, zero `b5_*` functions. The same receipt §6 states the
constraint in advance — *"M and B5 hold the same fields and the same registry visibility, so the
comparison is a cross-implementation test, not an information test: it can catch a bug in either
side's four distinct checks and it cannot detect a residual that does not exist."*

**Units.** `ME_X7_OUTCOME_RECEIPT.md` §8: *"'eight of eleven gates' is a unit mismatch, the true
figure being 8 vacuous comparison items spanning 6 of 11 gates, 4 fully vacated and 2 partially"*.
The frozen receipt states the units correctly; only a commit message mixed them. No protected
artifact ever existed. Repair verified: 4 of 11 checks now run different code, the other 7 are
reported as shared.

**Why this one needs its own vocabulary.** A gate that never ran reports `0`, which becomes
suspicious the moment the denominator is demanded. A comparator with no contrast reports `1.000`,
which reads as strength, and **there is no denominator to ask for**. The catching question differs
in kind — *could these two arms ever have differed?* The admission assessment §8 makes the same
point prospectively: *"The denominator question does not catch this."*

**Second instance, found by the admission assessment's own verification (§2.3).** The
cross-`PYTHONHASHSEED` guard written against `NONREPRODUCIBLE_FROZEN_ARTIFACT` is parametrized over
`0`, `1` and `12345` against a run at `0`, so the `0` case compares a process against itself and
passes unconditionally, **including on the unfixed code**. The guard against vacuity contained a
vacuous parametrization. Found by a verifier asked whether the test could fail, not by review.

---

## D2 — Prompt asymmetry disadvantaging the comparator (ME-F1)

**Class** `HANDICAPPED_COMPARATOR` · **Status** `NEAR_MISS`, with the headline repair numbers
`CANNOT_VERIFY`

**Verified.** `research/experiments/me-f1/ME_F1_G0E_OUTCOME_RECEIPT_V1.md:49` records
`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` at `0.3000`; the mechanism arm leads by `0.106` in R1
(`0.40625 − 0.3`) and by `0.206` in R2 (`0.45 − 0.24375`). The asymmetry itself is verified on
branch `research/me-f1-b5-prompt-code-parity-20260903`, `ME_F1_ARM_PARITY_V1.json`: the mechanism
arm carries `"names_tool_switch_action": true` with matched forms `["switch tool class",
"local_search <-> exact_solve"]`, while the probe note records that *"the shared preamble already
carries the INFORMATION; the claim under test is about the procedural rule, not the information"*.

**Four corrections the artifacts force.**

1. **`0.5125`, `0.131` and the `23/23` post-repair switch count have no artifact.** Re-searched
   2026-09-04 across every `refs/remotes/origin` ref and, separately, the lane worktree at
   `685c297` with a clean `git status` — that is, including the two commits added after the first
   verification pass. `/usr/bin/grep -rn -F` for `0.5125` and `23/23` under
   `research/experiments/me-f1/` returns **rc=1, 0 lines**, while the control `0.4875` matches in
   `ME_F1_B5_PARITY_REPAIR_RECEIPT_V1.md` and `results/ME_F1_ARM_PARITY_V1.json`. Across all origin
   refs, `0.5125` occurs only in `me-x2-v2` and `23/23` only in `me-x7*` — different studies.
   *Scope limit:* the merged receipt §1 says the post-repair tree was verified on
   `billy-laptop-old`, so a run may exist un-pulled on that host. The absence claim is scoped to
   every origin ref and every local checkout, not to "never computed".
2. **"a run-to-run spread of 0.056" is not a spread.** It is a single pairwise difference from n=2,
   and it is arm-specific: the mechanism arm's R1→R2 difference is `0.0438`, `SIMPLE_DIRECT`'s is
   `0.0937`.
3. **"the mechanism and bare-baseline arms held as internal controls" is false on the R1/R2 data.**
   The bare baseline's interface changed between runs — merged receipt §6: *"H-EXT-3 rung-0 arms
   (`SIMPLE_DIRECT`, `SAME_MODEL_REFLECTION`) now receive a claim schema with no `warrant` field at
   all."* R2 is not a replicate for that arm.
4. **"inverted the ordering" is at most the M-versus-B5 pair.** The full ranking is headed by the
   bare model in both runs: `SIMPLE_DIRECT` 0.756 > `M_ME_FRONTIER_CONTROL` 0.406 >
   `B5_..._FEDERATION` 0.300.

**Why it is a near-miss.** The lane caught and blocked it before any successor. Merged receipt
§5.1: *"Disposition: recorded, not repaired... It is a hard precondition on ME-F1 R2: no successor
may freeze `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` until its control text carries the
`INCONCLUSIVE` → switch-tool fallback... Until then, no M-versus-B5 comparison in this world is
worth running."* The study routes `CANNOT_CHECK` before any protected dispatch. No ME-F1 arm score
appears in any paper.

**The claim that survives** is the mechanism and the precondition, not a measured inversion: a
comparator whose prompt omits a procedural rule the mechanism's prompt names is isolated, and no
comparison against it is worth running until parity is restored.

---

## D3 — Budget starvation of a comparator (ME-F1)

**Class** `HANDICAPPED_COMPARATOR` · **Status** `NEAR_MISS`, **attributed to the wrong arm as
nominated**

**The single largest correction in this record.** Every number behind the nominated claim belongs to
`B5_ALGORITHMIC_CORE_NO_MODEL`, the deterministic twin — **not** to
`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`, the comparator of D2. The merged receipt §5 explicitly
forbids the pairing the nomination draws: *"These are not the same resource envelope"*, under a
heading *"Two comparisons that must not be drawn from this table"*.

Verified: `ME_F1_ARM_PARITY_V1.json` `fallback_ablation` records `"action_cap": 7`,
`"arm": "B5_ALGORITHMIC_CORE_NO_MODEL"`, `"primary": 0.4875`. The `0.9250` figure and the
~120-action natural budget are **prose-only in an uncommitted receipt**
(`ME_F1_B5_PARITY_REPAIR_RECEIPT_V1.md` §8); no JSON carries either, and `fallback_ablation` fixes
`action_cap` at 7 as its only budget, so the natural-budget number is uncomputed by construction in
the machine artifact.

**The ablation does not isolate budget.** The cap was held at 7 for *both* variants and only the
fallback varied, `0.2000 → 0.4875`. At 7 actions the fallback, not the probe budget, accounts for
the measured swing; the `0.925 → 0.4875` drop mixes two changes.

"12+ probes across 4 blocks" is *"roughly 3 probes per block across 4 blocks (~12)"* in the receipt;
`mef1_arms.py:607` reads `budgets = luby_budgets(campaign.budget_checks // 2, 12)`.

**Provenance caveat on the one committed number.** `ME_F1_ARM_PARITY_V1.json`'s own
`source_provenance` self-reports `"match": false` with `"drifted_files": ["mef1_arms.py",
"mef1_parity.py", "mef1_run.py"]`, so `0.4875` verifies against an artifact whose own drift detector
says the executing tree was not the frozen tree.

**What survives:** an under-budgeted comparator is isolated as surely as an under-prompted one, and
the receipt uses the ablation correctly — to size a precondition, not to score the comparator. The
quantitative claim as nominated does not survive.

---

## D4 — A representation claim falsified by exhibition (ME-X6)

**Class** `TERMINAL_OVERSTATES_ITS_PROCEDURE` · **Status** `REALISED`

`research/experiments/me-x6/mex6_run.py:590` and the protected receipt at lines 30 and 304:

```text
TERMINAL = UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION
```

`ME_X6_COMPARATOR_PROVENANCE_AND_NON_FIDELITY_RECEIPT_V1.md` §3 exhibits the counterexample: the
mechanism and the comparator are the same function differing only in a weight dict, so loading the
mechanism's weights into the untyped path scores `56 / 56` on the **capability half**, against a
control — the untyped arm with all-`+1` weights — at `28 / 56`. §4: *"Attribution: the comparator
fails because it cannot set a weight to zero."*

**Three corrections.** (i) The terminal string ends `_AT_MATCHED_INFORMATION`; the nomination
truncates it. (ii) **The terminal was not corrected to `DOES_NOT_RECOVER`.** Lines 30 and 304 still
read `CANNOT_REPRESENT`; what exists is a qualification banner and a §5 that *proposes* the wording
`FITTED_UNIT_SIGN_UNTYPED_AGGREGATE_DOES_NOT_RECOVER_THE_CONJUNCTION_AT_MATCHED_INFORMATION`.
(iii) The load-bearing `56/56` is the capability half; the receipt's own self-audit says the
activity half's `56/56` *"is not evidence; it is published here only so that no reader mistakes it
for some."*

The exhibition is on the public development split `ME-X6-DEV-20260903` (`per_cell = 2`); §8 lists
*whether the protected split reproduces §4's attribution exactly* under what could not be checked.

**Why it matters:** an impossibility was written into a terminal that a hand-built exhibition
falsifies in one run. The honest claim is about the comparator's fitting procedure, not about what
the representation can express.

---

## D5 — A threshold margin borrowing a null's authority (H-EXT-1)

**Class** `TERMINAL_OVERSTATES_ITS_PROCEDURE` · **Status** `REALISED`, corrected, contained

The defective sentence existed and its history is exact: introduced `01a70cb` (#140), corrected
`e2d5d77` (#247). Prior text: *"drag, beating the strongest parent by +2.1 pp pooled and the
always-on arm by +8.3 pp."*

`H_EXT1_OUTCOME_RECEIPT.md` item 2, verbatim: *"G3 and G3S test exactly one quantity … the
gated-versus-always-on-`M` contrast … against 2000 equal-n draws in each null, exceedance 0/2000 in
both. The parent comparison is G2, registered as a threshold … no null, no p-value, no interval,
because none was registered. The +2.1 pp margin … is therefore a registered threshold comparison
decided by 11 tasks (508 vs 497) and carries no significance claim … A reader must not borrow G3's
authority for it."*

Confirmed structurally: `H_EXT1_CELL_PROSPECTIVE.json`'s `G2_DOMINATES_ALWAYS_OFF_AND_PARENT` holds
only `acc_OFF`, `acc_PARENT`, `pass`, `pass_vs_OFF`, `pass_vs_PARENT` — no null, no p, no interval —
while `G3_BEATS_SHUFFLE_NULL` carries `draws: 2000`, `null_exceedance_fraction: 0.0`.

**The distinction the receipt draws and the nomination collapses:** *"The design registered G2 as a
threshold, so this is a correction to this receipt's prose, not a registered clause that went
unexecuted."* That is precisely what separates D5 from D6 in `02`.

**Contained.** The margins did not propagate outside the receipt: the outbound review packet
`papers/pipeline/FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V3_V21.md:241,247` supplies H-EXT-1
design only — *"no numbers, strata, or arm results are supplied"*.
