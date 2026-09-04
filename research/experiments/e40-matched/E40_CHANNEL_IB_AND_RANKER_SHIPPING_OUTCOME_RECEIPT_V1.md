# E40 — channel information bound and ranker shipping: outcome receipt (V1)

```text
E40_CHANNEL_IB_TERMINAL      = OOS_RANKER_EXISTS__PROSPECTIVE_M5PP_WARRANTED   (IB1 fired, IB2 fired, IB3 NOT fired)
E40_RS_TERMINAL              = SHIPPING_LEVER_EXHAUSTED__NO_OOS_RANKER_ON_VISIBLE_FIELDS_SHIPS_BETTER_THAN_THE_LOOPS_FINAL
E40_LINE                     = CLOSED (PR #277) -- unchanged by this receipt
REVIVES_E40 = false   AUTHORIZES_M6 = false   GRANTS_FIELD_STATUS = false   GRANTS_SCIENTIFIC_TRUTH = false
```

**Scope.** Two registered re-analyses over the frozen m2/m3 chain tuples, each frozen (design +
machine-readable twin + runner + tests) in a commit **before** its rollup was computed, each with
zero model calls and zero native runs: the channel information bound (`E40_CHANNEL_INFORMATION_BOUND_DESIGN_V1`,
freeze `f207f2e`, rollup `68e2246`) and the ranker-shipping re-test (`E40_RANKER_SHIPPING_REANALYSIS_DESIGN_V1`,
freeze `972016d`, rollup `e7e5796`). Both rollups carry the sha256 of their design twin, their
script and the tuples file; the unit tests assert the committed rollups match those inputs.
Interpreter CPython 3.13.12 for both.

**What this receipt does.** It files the E40 negative one stage deeper than the closure receipt
left it — from *"the loop loses to the oracle-selected federation"* to *"what the feedback channel
contains, and whether the best shipping operator it admits closes the gap"* — and reports the
shipping lever as exhausted at its registered strength. It does not reopen the closure, whose
precondition finding (seed-only replica Jaccard 0.030, PR #277) is about a different gate.

---

## 1. The negative, and the stage it was already attributed to

Every routed E40 primary reads `F0_best − F2_final < 0` (m2 −0.008979, 11–1; m3 −0.007414,
10–2; m4 CT1 −0.011271, 11–1). m3's decomposition attributed it to **one stage**: `both_final`
(+0.0009, p 0.388) and `both_best` (−0.0012, p 0.696) are null; only the registered contrast — the
federation's **oracle best-of-four** against the loop's **last cycle** — separates. The drag is the
selection the loop performs at the end, not the quality of any cycle it runs. m4 pulled the
shipping lever with a single proxy field (`pooled_biological_evaluation`) and the drag stayed.
Stage-2d exonerated the model and implicated the cycle-1 mandate for the *probe*; the closure
receipt showed the *drag* survives a mandate-free arm (m2) at the same size. So after #277 the
question left was the one m4 could not answer with one field: **does the visible channel carry
anything a controller could follow, and if so, does following it close the gap?**

## 2. The channel information bound — what the feedback contains

Registered question: does any **linear function of the eight visible fields** rank the held-out
truth **out of sample**, fitted on chains the ranker never sees (leave-one-chain-out ridge,
λ = 1.0, 36 chains × 4 rows; within-chain permutation p at 2000 full LOCO refits)? Two further
feature sets separate the two sources of information a controller could use: the configuration it
chose (`CFG`: regime one-hot + `frac` + `frac²`) and both together.

| set | pooled mean ρ (36 chains) | perm p | top-1 (chance 0.25) | gate |
|---|---|---|---|---|
| `FB8` — the feedback | **0.220** | **0.019** | 0.417 | **IB1 fired** |
| `CFG` — the configuration prior | **0.324** | **0.003** | 0.417 | **IB2 fired** |
| `FB8+CFG` | 0.392 | 0.0005 | 0.389 | — |
| `FB8+CFG` − `CFG` | +0.067 | sign-flip 0.205 | — | **IB3 not fired** |

All four registered controls PASS and were consumed by the gates: m4's M1 pooled ρ reproduced to
2.3e-17 / 0.0; the m2 and m3 primaries reproduced to 2.6e-07 / 4.8e-07 and the F0 best-of-4 regime
census to 5/4/3; a planted signal (`run_time := truth + N(0, 0.25 sd)`) detected at ρ 0.80,
p 0.0025; null calibration rejected 7/100 at α = 0.05 (band 0.02–0.09).

**Reading, at its strength.** The feedback channel is **not** empty: a ranker that never sees the
chain it scores ranks its four cycles better than chance. This is stricter than m5′ Stage-1's
in-sample screen and contradicts its no-composite reading in the only direction that matters for
a controller — there *is* something to follow. But the configuration alone ranks truth at least as
well, and adding the feedback to it does not demonstrably help at n = 36 (+0.067, p 0.205). The
registered routing fires on IB1, so the terminal reads `OOS_RANKER_EXISTS__PROSPECTIVE_M5PP_WARRANTED`;
IB3 is reported beside it and qualifies what "warranted" licenses (§5).

A descriptive census, non-gating: 11 of 12 true-best F0 cycles sit at a regime extreme, which is
what `CFG` learns. The prior over configurations is largely *"go to an extreme"*.

## 3. The revival attempt — the shipping lever pulled with the best operator the channel admits

**Attribution:** `SELECTION_OPERATOR (shipping)`. **Lever:** ship the cycle the LOCO ranker
predicts best instead of the last one; the same operator applied to F0 for the matched contrast.
**Primary kind:** `FB8+CFG`, chosen pre-run as the controller's full visible information; `FB8`
and `CFG` reported, not gate-bearing. **Re-test against the strongest parent:** the registered
oracle `F0_best`, unchanged, so the claim stays comparable with m2/m3/m4.

Controls, all PASS and consumed: the m2/m3 primaries and census reproduced; the contrast could
exist (mean recoverable `F2_final − F2_best` = +0.00596, 18 of 24 chains have a better earlier
cycle); the planted channel ships at recovered fraction 1.000; null calibration rejected 4/100.

| pooled, 24 chains | `FB8` | `CFG` | **`FB8+CFG`** |
|---|---|---|---|
| P0 `F0_best − F2_final` (registered) | −0.008196 (3–21) | same | same |
| **P1 `F0_best − F2_ship`** | −0.007192, p(F2 worse) 0.003 | −0.006802, p 0.001 | **−0.005758, p 0.005** |
| **P2 `F2_final − F2_ship`** (lever effect) | +0.001004, p 0.313 | +0.001395, p 0.199 | **+0.002439, p 0.0585** |
| recovered fraction of the recoverable | 0.17 | 0.23 | **0.41** |
| P3 `F0_ship − F2_ship` (matched operator) | −0.000789, p 0.62/0.38 | −0.001580 | −0.001666, p 0.77/0.23 |
| P4 `F0_best − F2_best` (oracle both sides) | −0.002235, p(F2 worse) 0.100 | same | same |

**RS1 did not fire** (p 0.0585 against the registered 0.05, one-sided, 4000 flips). RS2 cannot
fire without it. **Terminal: `SHIPPING_LEVER_EXHAUSTED`.** Reported at exactly that strength: a
near-miss is not a fire, and the threshold was frozen before the number existed.

What the numbers say around the gate, descriptively:

- The best operator recovers **0.41** of what an oracle shipping operator could, and the drag under
  it (**−0.0058**) is still significantly negative (p 0.005). Even at the ceiling of the shipping
  class the drag would be P4, −0.0022 (p 0.10, 7–15) — the m3 `both_best` null.
- The effect is **cohort-conditional**: m2 recovers 0.75 (P2 +0.00427, p 0.046, 6–2) while m3
  recovers 0.10 (P2 +0.00061, p 0.41). Under the doctrine a regime-conditional positive is
  intermediate, not terminal; but the registered pooled gate is what was frozen, and this receipt
  does not re-slice it into a positive. The m2/m3 split is named as the constraint for any
  successor (§5).
- `CFG` alone ships **cycle 1 in all 24 chains**: the configuration prior learned from the other
  chains prefers the loop's first choice, which is where the loop places its regime extreme.
- The matched-operator contrast P3 is null in every kind: shipped by the same operator, the
  federation and the loop are indistinguishable — the whole registered drag is the oracle.

## 4. The three hypotheses, as this evidence bears on them

| hypothesis | reading from IB + RS |
|---|---|
| (a) the controller's decision procedure is worse than the parent's | **not supported at the cycle level** — `both_final`, `both_best` and P3 are null; the loop's cycles are as good as the federation's |
| (b) it is handicapped by its own prompt / mandate / allocation | **not implicated for the drag** — the drag reproduces mandate-free (m2); the shipping operator it lacks would recover at most 0.41 of a gap whose ceiling is itself null |
| (c) the suite rewards what it does not do | **this is the finding** — the registered primary credits the parent with an oracle selection over four runs and the loop with its last; the channel carries too little OOS information (top-1 ≈ 0.4) for any follow-the-feedback operator to match an oracle |

The E40 negative is therefore **structural for the mechanism class on this substrate**: a
feedback-following controller cannot beat an oracle-selected static federation when the feedback
ranks truth at top-1 ≈ 0.4, and the residual information sits in the configuration prior the
federation already has. This is the "channel information bound" the IB design set out to read,
now with the shipping re-test behind it.

## 5. What is licensed, and what is not

- `OOS_RANKER_EXISTS__PROSPECTIVE_M5PP_WARRANTED` licenses **only** a prospectively frozen campaign
  under its own identity. Read with IB3 (feedback adds nothing to the config prior at n = 36) and
  RS (shipping exhausted at the pooled gate; m2-conditional 0.75), the honest content of that
  licence is narrow: a successor would have to make the *feedback* carry information the
  configuration does not — a substrate or channel change, which by the design's own §6 is a new
  mechanism class — or test the m2/m3 split prospectively. Nothing here authorizes m6 and nothing
  reopens the E40 line closed in #277.
- The TP-family secondary is untouched and remains unpromoted.
- No visible-field composite, in-sample (m5′) or out-of-sample (IB), and no shipping operator over
  visible fields (m4 single proxy, RS learned ranker) rescues the registered primary. **The
  shipping-lever class is saturated on this substrate.** That is the stopping criterion, and it is
  named as such.

## 6. Discipline

- Both designs frozen with twins and tests before any rollup; seeds in the twins; no constant,
  gate, kind, pairing or routing row changed after computing. The RS pre-run note disclosed that
  the IB top-1 rates had been seen before the RS design was written.
- Every control is a must-match (reproduction to tolerance, planted signal, null calibration,
  contrast-could-exist); a failed control refuses every gate with its own exit code (IB: 5; RS: 4)
  and `evaluate_gates()` takes the verdicts as an argument.
- Unfailable-clause guard: RS2 cannot fire without RS1 (unit-tested). Pairing asserted equal to the
  receipts' by reproducing both primaries to 1e-6.
- `/usr/bin/git` for every decision; rollups committed byte-for-byte as computed.
- Served model: the m2 F2 decisions came from an unrecoverable served model and are labelled
  INFERRED throughout; nothing here contrasts across model epochs.

skills-applied: none (receipt, no manuscript content)
