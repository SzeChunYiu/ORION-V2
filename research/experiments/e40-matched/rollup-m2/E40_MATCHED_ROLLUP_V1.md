# E40_MATCHED_ROLLUP_V1

- gate: `METABOLIC_DRAG_MATCHED_NATIVE`
- schema: `orion.v2.e40-matched.rollup.v2` (v2 = NaN-policy repair of the rollup aggregation; no native run, arm prompt, or gate criterion changed)
- pairs complete: 12/12
- pairs CANNOT_CHECK no-defined-primary: 0
- degenerate (NaN-primary) runs: {"simple_nan_runs_over_total": [0, 12], "f0_nan_runs_over_total": [0, 48], "f2_nan_runs_over_total": [0, 48]}
- primary contrast: {
 "contrast": "F2_final vs F0_best (conservative)",
 "mean_d": -0.008979257925700411,
 "perm_p_exact": 0.9990234375,
 "wins_f2": 1,
 "wins_f0": 11
}
- controls: planted=PASS, nullcal=PASS, uninformative=present

## Pairs

| dataset | rep | d_primary (F0best−F2final) |
|---|---|---|
| weissmann_k562 | 0 | +0.005588 |
| weissmann_k562 | 1 | -0.023383 |
| weissmann_k562 | 2 | -0.010112 |
| weissmann_k562 | 3 | -0.006934 |
| weissmann_k562 | 4 | -0.009594 |
| weissmann_k562 | 5 | -0.015253 |
| weissmann_rpe1 | 0 | -0.007600 |
| weissmann_rpe1 | 1 | -0.006480 |
| weissmann_rpe1 | 2 | -0.007687 |
| weissmann_rpe1 | 3 | -0.003257 |
| weissmann_rpe1 | 4 | -0.001657 |
| weissmann_rpe1 | 5 | -0.021381 |
