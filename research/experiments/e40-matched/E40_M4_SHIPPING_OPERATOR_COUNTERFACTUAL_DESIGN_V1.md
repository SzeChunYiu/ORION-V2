# E40-m4 — Shipping-Operator Counterfactual Re-Analysis (Registered Design V1)

**Class:** registered re-analysis. Pure deterministic re-scoring of frozen m2/m3
chain artifacts — **zero model calls, zero native runs**. It can attribute and
select the next prospective lever; it **cannot by itself convert any m2/m3
negative into a positive** (no-rescue clause, §8).

**Parent verdict:** m3 `METABOLIC_DRAG_ROBUST_TO_ANCHOR` (receipt PR #101,
main `1f7e969`), whose mechanism decomposition localized the entire deficit to
the shipping rule: `both_final` d̄=+0.0009 (p=0.388) and `both_best`
d̄=−0.0012 (p=0.696) are both null; only `F0_best − F2_final` separates
(−0.0074, p=0.986). F0 ships max-of-4 selected by true score; F2 ships its
single sequential terminal selected by the cycle-visible proxy. m3 §4 names
the next lever class (feedback-channel design) and leaves opening it to the
operator; this design splits that lever class into its two separable halves —
**selection operator** (m4, compute-free) and **feedback channel** (m5', needs
new runs) — and measures the first.

## 1. Cohorts (frozen inputs, read-only)

| Cohort | F2 chains | F2 true scores | F0 reference |
|---|---|---|---|
| **P (primary)** | `campaign-e40-m3/run/chains/NN_f2_{ds}_{rep}` (12 chains × 4 cycles) | `campaign-e40-m3/run/results/{exp_id}/metrics.json` (exp_ids 501000–501047) | m2 federation chains `campaign-e40-m2/run/chains/{12..23}_f0_{ds}_{rep}`, runs `run0..run3`, scored under `campaign-e40-m2/run/results` |
| **R (pre-registered replication)** | `campaign-e40-m2/run/chains/{24..35}_f2_{ds}_{rep}` | `campaign-e40-m2/run/results` | same m2 federation chains (self-reference, exactly as m2's own rollup) |

`DATASETS = {weissmann_k562, weissmann_rpe1} × REPS=6` → 12 pairs per cohort.
Metrics extraction is byte-identical to the frozen m3 runner's
`primary_score()` (raw `wasserstein_distance.mean`, lower better; TP channels).
Chain keys resolve by glob `*_{arm}_{ds}_{rep}` with a uniqueness assertion —
numbering never drives loading.

## 2. Operator counterfactual (the single frozen delta)

For each F2 chain: **ship the cycle that maximizes the cycle-visible proxy**

- proxy P = `cycle{N}/redacted_feedback.json : pooled_biological_evaluation.true_positives`
  (higher better) — the channel the m-series planted-feedback control was built
  to carry signal (planted TP = 10+80q, monotone in quality q);
- ties → earliest cycle;
- missing/non-finite P in a cycle → fall back to the terminal cycle for that
  chain, counted; **>2 fallback chains in a cohort → cohort
  `CANNOT_CHECK__PROXY_MISSING`**, no verdict issues for it.

Nothing else changes: no prompt, no substrate, no anchor, no compute. The
counterfactual ships a different existing cycle of the SAME frozen trajectory.

## 3. Contrasts and readouts (per cohort, exact/deterministic)

All paired statistics use the m3-frozen convention verbatim:
`perm_paired_p` = exhaustive sign-flip enumeration over 2^12 flips,
T = mean(diffs), p = #{T_perm ≥ T_obs}/4096.

- **CT1 (primary)** d_i = `f0_best_i − f2_ship_i` on raw wasserstein
  (negative = F0 better). Plus wins/ties census.
- **CT2 (recovery)** d_i = `f2_final_i − f2_ship_i` (negative = proxy shipping
  improves on terminal). Wins census = #chains with recovery ≥ 0.
- **CT3 (TP family)** d_i = `f2_ship_i − f0_best_i` for `true_positives`,
  `corum_tp`, `string_tp` (m3 TP orientation: negative = F2 worse).
- **M1 (mechanism)** per-chain Spearman ρ(P, raw primary) over the 4 cycles;
  pooled Fisher-z mean ρ̂; two-sided within-chain cycle-shuffle permutation p
  (seed 20260831, 10,000 draws, shuffle the 4 proxy values within each chain).
- **M2 (selection census)** true-rank of the proxy-chosen cycle per chain
  (1 = best of 4); how often proxy-chosen = cycle1 (anchor-persistence).
- **C1 (degeneracy census)** distribution of the proxy-argmax cycle index. If
  argmax lands on cycle4 in ≥11/12 chains the rule degenerates to the terminal
  rule and CT1 ≡ m3 primary by construction (reported, no special-casing).

## 4. Gates (frozen before computing; evaluated once, cohort P)

- **G0 `M3_REPRODUCED` (hard):** from raw artifacts the script must reproduce
  bit-exactly: m3 primary mean_d `−0.007413520834557391`, primary perm_p
  `0.986083984375`, TP mean_d `−13.083333333333334`, TP perm_p
  `0.995849609375`, and both_best mean_d `−0.0012099336519952111`. Any
  mismatch → `M4_CANNOT_RUN__REPRODUCTION_FAILED`; no m4 verdict issues.
- **G1 `DRAG_ELIMINATED_UNDER_PROXY_SHIPPING`:** CT1 mean_d ≥ −0.001 AND
  CT1 perm_p ≤ 0.90 AND CT2 recovery ≥ 0 in ≥ 8/12 chains. (m3 terminal:
  −0.0074 / 0.986; the −0.001 bound is the both_best null band the
  decomposition already established; ≥0.95 perm_p was the m3 drag-fire
  convention, 0.90 leaves margin.)
- **G2 `PROXY_CHANNEL_UNINFORMATIVE`:** pooled |ρ̂| < 0.2 OR M1 permutation
  p > 0.05.

## 5. Pre-registered joint routing (what m4 authorizes for DRAFTING)

| Outcome | Route authorized |
|---|---|
| G1 ∧ ¬G2 | draft **m5 prospective interventional**: shipping rule = proxy-argmax, matched scale, m-series gates (one-line operator change at mechanism level) |
| G1 ∧ G2 | same as above (G1 dominates — the rule works despite weak global correlation) |
| G2 ∧ ¬G1 | draft **m5′ feedback-channel design** (calibrated extreme-resident probes / proxy-truth calibration feedback) — the m3-named lever |
| ¬G1 ∧ ¬G2 | selection insufficient; drag lives in the trajectory distribution; E40 line stays terminal-negative pending a NEW mechanism class; neither named lever is authorized |

Cohort R is reported identically as replication strength only; no route flips
on R alone; agreement/disagreement is recorded in the receipt.

## 6. Controls

- **C2 leakage (re-checked):** every `redacted_feedback.json` read must contain
  none of the frozen FORBIDDEN_SUBSTRINGS (`quantitative_test_evaluation`,
  `wasserstein`, `false_omission_rate`, `negative_mean_wasserstein`) —
  structural, same list as the runner.
- **C3 fallback census** (§2) and **C1 degeneracy census** (§3) reported.

## 7. Custody

- Input manifest: sha256 of every file read (all 96 chain-cycle
  `redacted_feedback.json` + `exp_id` files across both cohorts, every
  `metrics.json` scored, both F0 chain dirs) + script self-sha256.
- Output: `E40_M4_SHIPPING_COUNTERFACTUAL_ROLLUP_V1.{json,md}`; archived
  in-repo under `research/experiments/e40-matched/rollup-m4/` with the run
  log. Deterministic: no RNG except the frozen-seed M1 shuffle; two runs on
  the same inputs must produce byte-identical JSON.

## 8. Non-goals / no-rescue clause

m4 is attribution on the same data that generated the selection-operator
hypothesis. Whatever it shows: no positive F2 claim, no component claim, no
revival of the m2/m3 negatives. It only selects which prospective design (m5,
m5′, or neither) is worth a fresh registered execution; every revival claim
requires that prospective re-run at matched scale under the m-series gates.
