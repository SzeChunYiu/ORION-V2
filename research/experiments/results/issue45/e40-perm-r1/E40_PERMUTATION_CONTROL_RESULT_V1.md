# E40 label-permutation validity control — result receipt V1 (2026-08-29)

**Study:** `campaign-e40-perm-r1` (SLURM 3553121, 12/12 completed), successor to the
adjudicated e40-r3 native characterization. Freeze (`E40_PERMUTATION_CONTROL_FREEZE_V1.json`,
sha256 `750b7056…`) was written BEFORE any run; this receipt applies its
pre-declared interpretation unchanged.

## Outcome

| Cell | Native TP | Permuted TPs (seeds 1/2/3) | Median | Ratio to native | Verdict |
|---|---|---|---|---|---|
| weissmann_k562 observational | 137 | 21 / 30 / 13 | 21 | 0.153 | VALIDITY_PASS (<0.5) |
| weissmann_rpe1 observational | 41 | 5 / 7 / 9 | 7 | 0.171 | VALIDITY_PASS (<0.5) |
| weissmann_k562 partial-interventional | 0 (empty) | 0 / 0 / 0 (empty) | — | — | AMBIGUOUS_EMPTY |
| weissmann_rpe1 partial-interventional | 0 (empty) | 0 / 0 / 0 (empty) | — | — | AMBIGUOUS_EMPTY |

Metric path `quantitative_test_evaluation/output_graph/{true,false}_positives` — identical
to the adjudicated native numbers (TP 137/FP 272 K562-obs; TP 41/FP 128 RPE1-obs), verified
against `campaign-e40-r3/run/results/400000`.

## Interpretation (frozen criteria applied verbatim)

- The native observational chain is **signal-sensitive**: shuffling the per-sample
  perturbation labels (marginal preserved, expression bytes untouched) collapses TP to
  15–17% of native in both datasets. The adjudicated native TP metrics are not produced
  by pipeline artifacts.
- Permuted FP counts remain high (K562 435–490; RPE1 179–201) and exceed native FP —
  descriptive only per freeze; consistent with FP level being density-driven, not signal-driven.
- The natively-empty partial-interventional cells remain empty under all permutations:
  **AMBIGUOUS_EMPTY** — this control cannot distinguish signal absence from pipeline
  failure there, exactly as pre-declared; the adverse native interventional result stands
  with its existing interpretation unchanged.

## What this does and does not close

- Closes the "label-permutation/control study" gap listed in
  `EXECUTION_PARTIAL_SCIENTIFIC_ADJUDICATION_2026-08-28_V1.md` for E40.
- Does NOT close: matched F0/F2 control, independent native-domain adjudicator,
  cross-domain ORION transition claim. `E40_ORION_CROSS_DOMAIN_STUDY = OPEN` stands.
- No paper is promoted; this is a validity control, not decisive evidence.

## Data integrity

- Raw npz never modified; 6 permuted copies (2 datasets × 3 seeds) sha-receipted in
  `PREP_RECEIPT.json`; label marginals asserted identical element-wise; expression
  matrices and var_names byte-preserved.
- Invocation identical to `e40_compute_native_r3.sbatch` except `--data_directory`
  (permuted copy) and `--exp_id` (500000 + cell*3 + seed_idx); pinned args unchanged
  (pc, subset 0.05, both seeds 0).

## Terminal

```text
E40_PERMUTATION_CONTROL = COMPLETE_VALIDITY_PASS (observational cells, ratios 0.153/0.171)
E40_PERM_PARTIAL_INTERVENTIONAL = AMBIGUOUS_EMPTY (pre-declared, uninterpreted)
E40_NATIVE_CHAIN_SIGNAL_SENSITIVITY = ESTABLISHED_OBSERVATIONAL_ONLY
E40_ORION_CROSS_DOMAIN_STUDY = OPEN (unchanged)
PAPER_PROMOTION = NONE (validity control, not decisive)
```
