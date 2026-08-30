# E40_MATCHED_ROLLUP_V1

- gate: `METABOLIC_DRAG_MATCHED_NATIVE`
- schema: `orion.v2.e40-matched.rollup.v2` (v2 = NaN-policy repair of the rollup aggregation; no native run, arm prompt, or gate criterion changed)
- pairs complete: 12/12
- pairs CANNOT_CHECK no-defined-primary: 0
- degenerate (NaN-primary) runs: {"simple_nan_runs_over_total": [12, 12], "f0_nan_runs_over_total": [36, 48], "f2_nan_runs_over_total": [21, 48]}
- primary contrast: {
 "contrast": "F2_final vs F0_best (conservative)",
 "mean_d": -0.0009676610255547729,
 "perm_p_exact": 0.625,
 "wins_f2": 2,
 "wins_f0": 4
}
- controls: planted=PASS, nullcal=PASS, uninformative=present

## Pairs

| dataset | rep | d_primary (F0best−F2final) |
|---|---|---|
| weissmann_k562 | 0 | +0.000000 |
| weissmann_k562 | 1 | -0.000000 |
| weissmann_k562 | 2 | -0.006495 |
| weissmann_k562 | 3 | +0.000000 |
| weissmann_k562 | 4 | +0.000000 |
| weissmann_k562 | 5 | +0.000000 |
| weissmann_rpe1 | 0 | +0.000000 |
| weissmann_rpe1 | 1 | +0.014562 |
| weissmann_rpe1 | 2 | -0.024480 |
| weissmann_rpe1 | 3 | +0.000000 |
| weissmann_rpe1 | 4 | -0.007059 |
| weissmann_rpe1 | 5 | +0.011861 |
