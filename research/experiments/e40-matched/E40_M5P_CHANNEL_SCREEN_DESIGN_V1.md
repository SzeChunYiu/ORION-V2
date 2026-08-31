# E40-m5′ Stage 1 — Truth-Calibration Channel Screen (Registered Design V1)

**Class:** registered re-analysis. Pure deterministic re-scoring of the frozen
m2/m3 F2 chain artifacts — **zero model calls, zero native runs**. It selects
which feedback-channel candidate (if any) is worth a prospective
interventional campaign (m5″); it **cannot by itself convert any m2/m3/m4
negative into a positive** (no-rescue clause, §7).

**Parent verdict:** m4 `G2 ∧ ¬G1` route (receipt PR #130, main `7b8f52f`):
the cycle-visible proxy (pooled TP) is uninformative about truth (pooled ρ
P +0.191 ns / R −0.0007 ns; per-chain sign-flip; selection at chance) and its
argmax anti-selects (TP ↑ p=0.0007 while wasserstein ↓ p=0.9995). m4
authorized drafting the m5′ feedback-channel design: *calibrated
extreme-resident probes / proxy-truth calibration feedback*.

## 1. Question and logic

m4 measured ONE channel (`pooled_biological_evaluation.true_positives`). The
redacted feedback actually exposes **8 visible fields** per cycle (schema
frozen below). Before designing a probe that costs new native runs, the
compute-free question is: **does any frozen composite of the already-visible
quantities rank truth?** If yes → the m5′ prospective intervention swaps the
channel (and ships by its argmax). If no → the channel cannot be repaired
from visible quantities, and the only remaining truth-anchor computable
without modifying the pinned substrate is a seed-replica stability probe
(new native runs; Stage 2b design).

Selection discipline: candidates are selected on cohort **R (frozen m2 F2
chains)** and confirmed on the disjoint cohort **P (frozen m3 F2 chains)** —
the two cohorts are independent executions (different prompts: m3 carries the
cycle-1 anchor), so R-selection → P-confirmation is an out-of-sample check
within frozen data. A P-pass still authorizes only a **prospective** m5″
campaign with its own gates; no revival claim issues from this screen.

## 2. Frozen inputs and visible-channel schema (per cycle)

`cycle{N}/redacted_feedback.json` — exactly these keys (verified against the
frozen artifacts; enumeration only, no value inspection went into candidate
design):

```
chipseq_evaluation.true_positives                  (int)
corum_evaluation.true_positives                    (float)
ligand_receptor_evaluation.true_positives          (float)
pooled_biological_evaluation.true_positives        (float)   [m4's channel]
pooled_biological_sigificant_evaluation.true_positives (int) [never analyzed]
run_time                                           (float)
string_network_evaluation.true_positives           (float)
string_physical_evaluation.true_positives          (float)
```

Truth = `primary` (raw `wasserstein_distance.mean`, lower better) from the
cycle's own `metrics.json` — used ONLY by this scoring analysis, never by any
decision artifact (structural redaction unchanged).

Cohorts: P = `campaign-e40-m3/run/chains/*_f2_{ds}_{rep}` (12 chains × 4
cycles, exp_ids 501000–501047); R = `campaign-e40-m2/run/chains/{24..35}_f2_*
{ds}_{rep}` (12 × 4). `DATASETS={weissmann_k562, weissmann_rpe1} × REPS=6`.

## 3. Frozen candidate family (12; no additions after unblinding)

Direction d(c): +1 if higher score should mean better, −1 for run_time.
Per-chain scores are computed on the 4 cycle values of that chain (z-scores
and ranks are within-chain, so no cross-chain scale mixing).

| id | definition | d |
|---|---|---|
| `pooled_tp` | pooled_biological_evaluation.true_positives (m4 baseline) | +1 |
| `pooled_sig_tp` | pooled_biological_sigificant_evaluation.true_positives | +1 |
| `corum_tp` | corum_evaluation.true_positives | +1 |
| `string_net_tp` | string_network_evaluation.true_positives | +1 |
| `string_phys_tp` | string_physical_evaluation.true_positives | +1 |
| `chipseq_tp` | chipseq_evaluation.true_positives | +1 |
| `ligand_tp` | ligand_receptor_evaluation.true_positives | +1 |
| `fast_runtime` | run_time | −1 |
| `zmean_tp` | mean over the 6 TP channels of within-chain z-scores | +1 |
| `rankmean_tp` | mean over the 6 TP channels of within-chain ranks | +1 |
| `sig_purity` | pooled_sig_tp / max(pooled_tp, 1) | +1 |
| `efficiency` | within-chain z(pooled_tp) − within-chain z(run_time) | +1 |

## 4. Statistics (m4 conventions verbatim)

- Per chain: Spearman ρ(directed candidate score, truth) over the chain's
  cycles with finite truth (NaN-primary cycles dropped pairwise; a chain with
  <3 finite pairs is excluded for that candidate and counted).
- Pooled: arithmetic mean of per-chain ρ (m4's `pooled_rho_arithmetic`;
  Fisher-z reference reported, gate evaluates arithmetic).
- Permutation: within-chain cycle-shuffle of the candidate's 4 scores,
  two-sided |mean ρ| comparison, seed 20260831 (m4's M1 seed, so GS0's perm_p
  reproduces exactly), 10,000 draws.
- Selection census: true-rank (1=best of 4, average ranks on ties) of the
  candidate-argmax cycle; m4-CT3-style TP delta of the candidate-argmax cycle
  vs f0_best (does the winner retain the anti-selection?).

## 5. Gates (frozen before computing)

- **GS0 `M4_REPRODUCED` (hard):** the script must reproduce, from raw
  artifacts, the m4 rollup's M1 numbers for `pooled_tp` on both cohorts
  (pooled_rho_arithmetic and perm_p_two_sided, |Δ| ≤ 1e-9), reading the
  archived m4 rollup whose sha256 must equal
  `b8d2554097b43299a3aff8e200c580476baded8150b057e997a5f9898a732817`.
- **GS1 `SELECTION_AVAILABLE_ON_R`:** ≥1 candidate (other than the m4
  baseline `pooled_tp`) with R perm p ≤ 0.05 and directed pooled ρ > 0.
  Winner = max directed pooled ρ among those. If none → no winner.
- **GS2 `WINNER_CONFIRMED_ON_P` (the route gate):** winner's P directed
  pooled ρ ≥ 0.4 AND P perm p ≤ 0.05.

## 6. Pre-registered routing

| Outcome | Route |
|---|---|
| GS2 pass | draft **m5″ prospective interventional** (fresh 12×4 F2 campaign; feedback channel + prompt surface the winner composite; shipping = winner-argmax; m-series gates incl. planted/uninformative controls) |
| GS1 pass, GS2 fail | channel family not confirmable out-of-sample → draft **Stage-2b seed-replica stability-probe design** (the remaining truth-anchor without substrate modification; needs new native runs) |
| GS1 fail | no visible composite ranks truth even in-sample → same Stage-2b route; strengthens the terminal reading if Stage-2b also fails |

All 24 cohort×candidate rows are reported in full (no cherry-picking); the
winner additionally carries a leave-one-chain-out ρ stability table on P.

## 7. Non-goals / no-rescue clause

This screen attributes and selects. Whatever it shows: no positive F2 claim,
no component claim, no revival of any frozen negative. Every revival requires
the prospective m5″ (or Stage-2b) execution at matched scale under its own
freeze and the m-series gate battery.

## 8. Custody

- Script sha256 frozen in the PR carrying this design; input manifest = sha256
  of every file read (96 cycle feedback files + exp_ids + metrics + the m4
  rollup); deterministic re-run byte-identical; only RNG is the frozen-seed
  shuffle.
- Output `E40_M5P_CHANNEL_SCREEN_ROLLUP_V1.{json,md}` under
  `campaign-e40-m5p/stage1/rollup` on LUNARC, archived in-repo under
  `rollup-m5p-stage1/` with the outcome receipt.
