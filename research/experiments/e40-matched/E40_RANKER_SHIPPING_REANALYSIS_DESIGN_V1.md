# E40-RS — the shipping operator re-tested with the ranker the channel bound found (Design V1, frozen before computing)

**Class:** registered re-analysis over the frozen m2/m3 chain tuples. **Zero model calls, zero
native runs.** Pure Python; `math.fsum`; every draw seeded from this design and consumed in order.
**Machine-readable twin:** `E40_RANKER_SHIPPING_REANALYSIS_DESIGN_V1.json` (the selftest and the
unit test assert its constants equal the script's). **Runner:** `e40_ranker_shipping.py`.
**Lineage:** m3 (the drag is the selection operator), m4 (proxy shipping fails), the channel
information bound (`E40_CHANNEL_INFORMATION_BOUND_DESIGN_V1`, rollup committed at `68e2246`), and
the E40 line closure (PR #277), which this design does not reopen.

## 1. Why this design exists

The line's every routed primary reads `F0_best − F2_final < 0`: an upfront federation's **oracle
best-of-four** beats the loop's **last cycle**. m3 decomposed it: `both_final` and `both_best` are
null — cycle for cycle the loop is as good as the federation, and oracle for oracle so is it. The
whole drag is the *selection* the loop performs at the end: it ships its last configuration; the
parent is credited with its best. m4 pulled the obvious lever — ship by a visible proxy instead of
by recency — with the one field the receipts had singled out, and the drag stayed.

The information bound then asked the stricter question and got the answer m4 needed: a ridge
ranker over the eight visible fields **ranks truth out of sample** (`FB8` ρ 0.220, p 0.019;
`FB8+CFG` ρ 0.392, p 0.0005; top-1 0.39–0.42 against 0.25 chance), while feedback adds nothing
demonstrable to the configuration prior (IB3 not fired, +0.067, p 0.205). So a shipping operator
strictly better than m4's single proxy exists, it is out-of-sample, and it has never been used as
the shipping operator. That is the one lever in the shipping class left unpulled. This design
pulls it.

**What it is not.** It cannot revive E40 (closed on the seed-replica precondition), cannot
authorize m6, and alters nothing routed. Its strongest outcome licenses only a prospectively
frozen new line whose shipping operator is the ranker.

## 2. Frozen inputs and pairing

The IB tuples (sha256 `b96d7f78…`): 36 chains × 4 rows — m2 F0 (12), m2 F2 (12), m3 F2 (12) —
each row with the eight visible fields, the executed config and the truth. Every F2 chain pairs to
the m2 F0 chain of the same `(dataset, rep)`; the control reproduces the m2 (−0.008979) and m3
(−0.007414) primaries to 1e-6 from exactly this pairing, so the pairing is the receipts'.

## 3. The operator

For each chain, a ridge ranker (λ = 1.0, inherited from the IB design, not re-tuned) is fitted on
the **other 35 chains** and predicts the four cycles of the held-out chain; the shipped cycle is
the argmin of the prediction (ties to the earliest cycle — a loop cannot un-run a cycle). Three
feature sets are computed; **`FB8+CFG` is primary** because it is the controller's full visible
information — the feedback it received plus the configuration it chose. `FB8` and `CFG` are
reported and bear on no gate. The same operator is applied to the F0 chains for the fair contrast.

## 4. Contrasts (m-series convention: `d = F0_x − F2_y`, negative ⇒ F2 worse)

| id | contrast | role |
|---|---|---|
| P0 | `F0_best − F2_final` | the registered primary; reproduced as a control |
| **P1** | `F0_best − F2_ship` | the drag under ranker shipping |
| **P2** | `F2_final − F2_ship` (> 0 ⇒ lever helped) | **gate-bearing** |
| P3 | `F0_ship − F2_ship` | both arms shipped by the same operator |
| P4 | `F0_best − F2_best` | oracle both sides — the ceiling of any shipping operator |
| — | `F2_final − F2_best` | the recoverable improvement; `recovered_fraction = mean(P2)/mean(recoverable)` |

Statistic: mean over 12 pairs per cohort and 24 pooled; one-sided sign-flip permutation p (4000
flips, seed 20260904) in the direction each gate names; wins/ties published.

## 5. Controls — consumed by the gates

| control | rule |
|---|---|
| `M2_M3_PRIMARY_AND_CENSUS_REPRODUCED` | P0 = −0.008979 / −0.007414 to 1e-6; F0 best-of-4 census 5/4/3 |
| `RECOVERABLE_IMPROVEMENT_EXISTS` | pooled mean recoverable > 0 and ≥ 12 of 24 chains have a better earlier cycle (the contrast could exist) |
| `PLANTED_SIGNAL_SHIPS` | `run_time := truth + N(0, 0.25·sd)` on a copy (seed 20260904); `FB8` ranker shipping recovers ≥ 0.75 of the recoverable (the pipeline can ship on an informative field) |
| `NULL_CALIBRATION` | 100 within-chain truth shuffles (seed 20260903), RS1's own statistic on the primary kind at 400 flips; rejection rate ∈ [0.02, 0.09] |

A failed control refuses every gate (`CANNOT_CHECK__CONTROL_FAILED`, exit 4). `evaluate_gates()`
takes the control verdicts as an argument — the `UNGATED_CONTROL_VERDICT` guard.

## 6. Gates and routing

- **RS0** all controls PASS.
- **RS1 `SHIPPING_LEVER_HELPS`** — pooled mean(P2) > 0, p ≤ 0.05.
- **RS2 `RECOVERS_HALF_OR_MORE`** — RS1 fired and `recovered_fraction ≥ 0.5` (cannot fire without RS1; asserted).
- RS3 / RS4 reported alongside: is P1 still significantly negative; the P3 matched-operator contrast.

| outcome | terminal |
|---|---|
| RS0 fails | `CANNOT_CHECK__CONTROL_FAILED` |
| RS1 ∧ RS2 | `SHIPPING_OPERATOR_RECOVERS_HALF_OR_MORE_OF_THE_DRAG__PROSPECTIVE_SHIPPING_LINE_WARRANTED` |
| RS1 ∧ ¬RS2 | `SHIPPING_OPERATOR_HELPS_BUT_THE_DRAG_STANDS__PARTIAL` (intermediate; residual attributed to per-cycle configuration choice) |
| ¬RS1 | `SHIPPING_LEVER_EXHAUSTED__NO_OOS_RANKER_ON_VISIBLE_FIELDS_SHIPS_BETTER_THAN_THE_LOOPS_FINAL` |

## 7. Pre-run reachability audit

Seed does something (flips, plant, shuffles). No crash path at scale (36 fits per kind; 3 600 fits
for the null). Contrast could exist — asserted by a must-match control. Clause scope — the runner
evaluates exactly §6; constants asserted equal to the twin. Parent isolation — none: P3 applies
one operator to both arms; P1 keeps the registered oracle parent so the claim stays comparable
with m2/m3/m4. Unfailable clause — RS2 is guarded by RS1.

## 8. Pre-run expectation, disclosed

The IB rollup's top-1 rates were seen before this design was written; they suggest partial
recovery. Stated so that neither `PARTIAL` nor `EXHAUSTED` can be read afterwards as a surprise.

## 9. No-rescue clause

No constant, kind, gate, threshold, seed, pairing or routing row changes after the rollup is
computed. A defect found afterwards is recorded in the receipt and repaired under a new identity.

skills-applied: none (frozen design, no manuscript content)
