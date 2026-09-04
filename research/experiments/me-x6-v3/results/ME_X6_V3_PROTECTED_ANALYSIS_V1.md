# ME-X6 V3 PROTECTED analysis

- instances: 1800
- route: `PARENT_SUFFICIENT_AT_FULL_COVERAGE` — terminal `TYPING_IS_A_COVERAGE_PRIOR`
- reason: M is ahead of the coverage-unmatched frozen comparator on the held-out roles; the coverage-matched refit ties M everywhere and is itself ahead of the frozen vector on the held-out roles.  The a-priori typed assignment buys exactly what development coverage would have bought: robustness to roles the fitter never saw exercised, and nothing at full coverage

Only the CAPABILITY half is scored (the activity half is equal by construction).

## Gates

| gate | pass | verdict | n_evaluated |
|---|---|---|---|
| `G0a_KNOWN_ANSWER` | True |  | 25 |
| `G0b_GENERATOR_VALIDITY` | True |  | 1800 |
| `G0c_NULL_CALIBRATION` | True |  | 1800 |
| `G0d_M_EXACT_BY_CONSTRUCTION_ON_V1_STRATA` | True |  | 1400 |
| `G0e_COVERAGE_AND_CAPACITY_BITS` | True |  | 16 |
| `G0d2_M_ON_HELD_OUT_ROLES` | True |  | 400 |
| `G1_M_VS_B8_V2_FROZEN_ON_HELD_OUT_4` | True | X_AHEAD | 400 |
| `G2_M_VS_B8_V3_REFIT_ON_ALL_18` | True | TIE | 1800 |
| `G3_B8_V3_REFIT_VS_B8_V2_FROZEN_ON_HELD_OUT_4` | True | X_AHEAD | 400 |
| `G6_CROSS_SCALE_CONSISTENCY` | True |  | 1800 |
| `G8_VERDICT_CONSTANCY_WITHIN_CELL` | True |  | 36 |

## Arms (capability), per scale

| arm | all-18 SUBFIELD | all-18 PROBLEM_FAMILY | held-out-4 SUBFIELD | held-out-4 PROBLEM_FAMILY | pooled |
|---|---|---|---|---|---|
| `B7_V3_L1_PATH_UNTYPED` | 900/900 | 900/900 | 200/200 | 200/200 | 1800/1800 |
| `B8_V3_REFIT_COVERAGE_MATCHED` | 900/900 | 900/900 | 200/200 | 200/200 | 1800/1800 |
| `B9_EXHAUSTIVE_UNTYPED_IDENTITY_CHECK` | 900/900 | 900/900 | 200/200 | 200/200 | 1800/1800 |
| `M_TYPED_COLLECTIVE_STATE` | 900/900 | 900/900 | 200/200 | 200/200 | 1800/1800 |
| `B6_V3_GREEDY_SUBSET_UNTYPED` | 800/900 | 800/900 | 150/200 | 150/200 | 1600/1800 |
| `B8_V2_FROZEN_COVERAGE_UNMATCHED` | 700/900 | 700/900 | 0/200 | 0/200 | 1400/1800 |
| `B4X_V1_UNIT_SIGN_LEARNED_CONTROL` | 500/900 | 500/900 | 150/200 | 150/200 | 1000/1800 |
| `C_ALWAYS_FLAT` | 400/900 | 400/900 | 0/200 | 0/200 | 800/1800 |
| `C_ALWAYS_RISE` | 300/900 | 300/900 | 100/200 | 100/200 | 600/1800 |
| `C_ALWAYS_FALL` | 200/900 | 200/900 | 100/200 | 100/200 | 400/1800 |

## Coverage

- cells exercised: 36 / 36
- never exercised: none
- scope binding equal: True
