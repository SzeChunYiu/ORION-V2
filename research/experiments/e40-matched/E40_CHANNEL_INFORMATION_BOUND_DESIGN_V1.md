# E40 — Channel Information Bound: registered re-analysis, Design V1 (frozen before any computation)

**Class:** registered re-analysis over the frozen m2/m3 chain artifacts. **Zero model calls, zero
native runs.** Pure Python (the project environment carries no numpy); every sum is `math.fsum`;
every RNG draw is seeded from this design and consumed in a fixed order.
**Machine-readable twin:** `E40_CHANNEL_INFORMATION_BOUND_DESIGN_V1.json` (the constants there are
the constants in `e40_channel_information_bound.py`; the test asserts they agree).
**Lineage:** m2 (`METABOLIC_DRAG_MATCHED_NATIVE`, no cycle-1 mandate, F0 wins 11/12), m3 (drag robust
to the anchor; `both_final`/`both_best` null → the deficit is the selection operator), m4 (proxy
channel uninformative, proxy shipping does not eliminate the drag), m5′ Stage-1 (no frozen composite
of the 8 visible fields ranks truth in-sample), Stage-2d (`PROMPT_IMPLICATED`, model exonerated),
Stage-2e (closure lane, PR #277: seed-only replica Jaccard 0.030 ≈ config-only 0.027 — the knobs move
the output graph less than the seed does).

## 1. Why this design exists, and what it is not

Every E40 revival lever named so far has been pulled and has failed: exploration prior (m3), shipping
operator (m4), any of twelve visible composites (m5′), the mandate (Stage-2d, and m2 was mandate-free
from the start), and replica consensus (Stage-2c degenerate, Stage-2e precondition unmet). The m5′
screen answered *"does any **frozen composite** rank truth **in-sample**?"* — no. The question that
saturates the feedback-channel lever class is one step wider and one step stricter: **does any linear
function of the eight visible fields rank truth *out of sample***, fitted on chains the ranker never
sees? If not, no feedback-following controller of this class can beat an upfront federation on this
substrate, whatever its prompt, mandate or model — the channel carries nothing to follow.

The design also separates two sources of information a controller could use: the **feedback** (what
the metabolic loop adds) and the **prior over configurations** (what an upfront federation uses
without feedback). Both receipts observed that regime extremes score better than the interior on 11/12
pairs; if configuration alone predicts truth out of sample and feedback adds nothing, then the whole
of F0's advantage is prior knowledge plus oracle selection, and the loop's sequential information is
void by construction — a **structural** negative for the mechanism class, not an operational one.

**This is not a revival.** It cannot revive the E40 line, cannot authorize m6, and alters no prior
disposition. It files a channel-information reading at exactly the strength its gates earn, so the
paper can say *what the feedback contains* rather than only *that the loop lost*.

## 2. Frozen inputs

`rollup-e40-channel-ib/E40_CHANNEL_IB_TUPLES_V1.json`
(sha256 `b96d7f7857ed7740e65e95eab9a7c7ad1219874ce75895bb0cd8cb49dbc6d0d6`): 144 rows, 36 chains × 4,
three cohorts of 12 chains — m2 F0 (`run0..run3`, treated as four cycles), m2 F2, m3 F2 — each row
carrying the eight visible feedback fields (`redacted_feedback.json`, asserted byte-equal to the
run's `metrics.json` minus `quantitative_test_evaluation`), the executed config
(`results/<exp_id>/arguments.json`, regime canonicalised across the upstream spelling variants and
asserted against `config_1.json` where present) and the truth (`wasserstein_distance.mean`). A
576-file sha256 manifest of the LUNARC sources is inside the tuples file. The m2 F2 decisions were
produced by an **unrecoverable served model** (no per-call id); it is labelled INFERRED, never as
`glm-5.3`.

## 3. Feature sets, ranker, statistic

| set | features |
|---|---|
| `FB8` | the eight visible feedback fields |
| `CFG` | regime one-hot (3) + `frac` + `frac²` |
| `FB8+CFG` | both |

Ranker: ridge regression, λ = 1.0, columns standardised on the training fold, target centred. Fold:
**leave-one-chain-out** over all 36 chains. Per held-out chain: Spearman(prediction, truth) over its
4 rows (positive = ranks truth correctly) and `top1_hit` (argmin prediction = argmin truth; chance
0.25). Pooled statistic: arithmetic mean of per-chain Spearman.

## 4. Controls — evaluated first and consumed by the gates

| control | rule |
|---|---|
| `M4_M1_REPRODUCED` | per-chain raw Spearman(`pooled_biological_evaluation`, wasserstein), mean over the 12 F2 chains per cohort, equals m4's frozen `pooled_rho_arithmetic` (P = m3 F2, R = m2 F2) to 1e-9 — ties this table to the frozen artifacts bit-for-bit |
| `M2_M3_PRIMARY_AND_CENSUS_REPRODUCED` | `F0_best − F2_final` over 12 pairs reproduces the m2 receipt (−0.008979) and the m3 receipt (−0.007414) to 1e-6; the m2 F0 best-of-4 regime census reproduces interventional 5 / observational 4 / partial 3 |
| `PLANTED_SIGNAL_DETECTED` | `run_time` replaced on a copy by truth + N(0, 0.25·sd) (seed 20260904); the `FB8` ranker must reach mean ρ ≥ 0.5 with permutation p ≤ 0.05 (400 perms) — proves the pipeline can see an informative channel |
| `NULL_CALIBRATION` | 100 within-chain truth shuffles, each tested at 200 permutations; rejection rate at α = 0.05 ∈ [0.02, 0.09] (seed 20260903) |

A failed control refuses every gate (`CANNOT_CHECK__CONTROL_FAILED`, exit 5). `evaluate_gates()` takes
the control verdicts as an argument — the `UNGATED_CONTROL_VERDICT` guard.

## 5. Gates (frozen)

- **IB0 `CONTROLS_VALID`** — all four controls PASS and all 144 envelopes valid.
- **IB1 `FEEDBACK_RANKS_TRUTH_OOS`** — pooled mean ρ(`FB8`) > 0 and within-chain permutation p ≤ 0.05
  (2000 permutations with full LOCO refit, seed 20260904, one-sided).
- **IB2 `CONFIG_RANKS_TRUTH_OOS`** — the same for `CFG`.
- **IB3 `FEEDBACK_ADDS_TO_CONFIG`** — mean over chains of ρ(`FB8+CFG`) − ρ(`CFG`) > 0 with sign-flip
  p ≤ 0.05 (4000 flips, seed 20260904).

## 6. Registered routing

| outcome | terminal |
|---|---|
| IB0 fail | `CANNOT_CHECK__CONTROL_FAILED` — could-not-check, filed as such |
| IB1 fires | `OOS_RANKER_EXISTS__PROSPECTIVE_M5PP_WARRANTED` — contradicts m5′; licenses **only** a prospective campaign under its own freeze; no revival claim |
| IB1 not fired, IB2 fires | `CHANNEL_INFORMATION_BOUND__PRIOR_OVER_CONFIGS_IS_THE_ONLY_OOS_SIGNAL` |
| neither | `CHANNEL_INFORMATION_BOUND__NO_OOS_SIGNAL_IN_FEEDBACK_OR_CONFIG` |

IB3 is reported alongside whichever terminal fires.

## 7. Pre-run reachability audit

- **Seed does something:** yes — permutations, sign flips, the plant and the null-calibration draws.
- **Hard gate at scale:** 36 chains × 2000 permutations × 3 sets in pure Python; no crash path.
- **Contrast could exist:** per-chain ρ ranges over {−1, …, +1}; the plant must reach ≥ 0.5 and the
  shuffled null must sit near 0 — both verdicts of every gate are reachable under the frozen inputs.
- **Comparator isolation:** not applicable — no arm is run; F0 and F2 rows are pooled as substrate
  samples, not contrasted.
- **Clause scope:** the runner evaluates exactly the three gates above; the test asserts the
  constants in the script equal those in the JSON twin.

## 8. No-rescue clause

No design constant, gate, threshold, seed, feature set or routing row may change after the rollup is
computed. A defect found afterwards is recorded in the receipt and repaired under a new identity.

skills-applied: none (frozen design, no manuscript content)
