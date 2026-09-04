# ME-X6 V3 DEVELOPMENT analysis

- instances: 72
- route: `PARENT_SUFFICIENT_AT_FULL_COVERAGE` — terminal `TYPING_IS_A_COVERAGE_PRIOR`
- reason: M is ahead of the coverage-unmatched frozen comparator on the held-out roles; the coverage-matched refit ties M everywhere and is itself ahead of the frozen vector on the held-out roles.  The a-priori typed assignment buys exactly what development coverage would have bought: robustness to roles the fitter never saw exercised, and nothing at full coverage

Only the CAPABILITY half is scored (the activity half is equal by construction).

## Gates

| gate | pass | verdict | n_evaluated |
|---|---|---|---|
| `G0a_KNOWN_ANSWER` | True |  | 25 |
| `G0b_GENERATOR_VALIDITY` | True |  | 72 |
| `G0c_NULL_CALIBRATION` | True |  | 72 |
| `G0d_M_EXACT_BY_CONSTRUCTION_ON_V1_STRATA` | True |  | 56 |
| `G0e_COVERAGE_AND_CAPACITY_BITS` | True |  | 16 |
| `G0d2_M_ON_HELD_OUT_ROLES` | True |  | 16 |
| `G1_M_VS_B8_V2_FROZEN_ON_HELD_OUT_4` | True | X_AHEAD | 16 |
| `G2_M_VS_B8_V3_REFIT_ON_ALL_18` | True | TIE | 72 |
| `G3_B8_V3_REFIT_VS_B8_V2_FROZEN_ON_HELD_OUT_4` | True | X_AHEAD | 16 |
| `G6_CROSS_SCALE_CONSISTENCY` | True |  | 72 |
| `G8_VERDICT_CONSTANCY_WITHIN_CELL` | True |  | 36 |

## Arms (capability), per scale

| arm | all-18 SUBFIELD | all-18 PROBLEM_FAMILY | held-out-4 SUBFIELD | held-out-4 PROBLEM_FAMILY | pooled |
|---|---|---|---|---|---|
| `B7_V3_L1_PATH_UNTYPED` | 36/36 | 36/36 | 8/8 | 8/8 | 72/72 |
| `B8_V3_REFIT_COVERAGE_MATCHED` | 36/36 | 36/36 | 8/8 | 8/8 | 72/72 |
| `B9_EXHAUSTIVE_UNTYPED_IDENTITY_CHECK` | 36/36 | 36/36 | 8/8 | 8/8 | 72/72 |
| `M_TYPED_COLLECTIVE_STATE` | 36/36 | 36/36 | 8/8 | 8/8 | 72/72 |
| `B6_V3_GREEDY_SUBSET_UNTYPED` | 32/36 | 32/36 | 6/8 | 6/8 | 64/72 |
| `B8_V2_FROZEN_COVERAGE_UNMATCHED` | 28/36 | 28/36 | 0/8 | 0/8 | 56/72 |
| `B4X_V1_UNIT_SIGN_LEARNED_CONTROL` | 20/36 | 20/36 | 6/8 | 6/8 | 40/72 |
| `C_ALWAYS_FLAT` | 16/36 | 16/36 | 0/8 | 0/8 | 32/72 |
| `C_ALWAYS_RISE` | 12/36 | 12/36 | 4/8 | 4/8 | 24/72 |
| `C_ALWAYS_FALL` | 8/36 | 8/36 | 4/8 | 4/8 | 16/72 |

## Coverage

- cells exercised: 36 / 36
- never exercised: none
- scope binding equal: True
