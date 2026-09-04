# ME-X6 V2 DEVELOPMENT analysis

- instances: 56
- route: `PARENT_SUFFICIENT` — terminal `TYPING_NOT_SEPARATED_AT_MATCHED_CAPACITY`
- reason: a LEARNED untyped comparator whose weight class contains zero reproduces M's capability verdict on every instance. The separation V1 measured is attributable to the comparator's capacity, not to typing. ME-X6 contracts to an interpretive framework -- the protocol's own contraction rule, and a legitimate result, not a failure

Only the CAPABILITY half is scored. V1 computes the activity direction from the same channels by the same call for every arm, so an activity agreement is equal by construction and is not evidence.

## Gates

| gate | pass | n_evaluated |
|---|---|---|
| `G0a_KNOWN_ANSWER` | True | 12 |
| `G0b_GENERATOR_VALIDITY` | True | 56 |
| `G0c_NULL_CALIBRATION` | True | 56 |
| `G0d_M_EXACT_BY_CONSTRUCTION` | True | 56 |
| `G0e_CAPACITY_MATCHING_BIT` | True | 16 |
| `G1a_M_AHEAD_OF_CAPACITY_MATCHED_PARENT` | False | 56 |
| `G1b_TIE_AT_MATCHED_CAPACITY` | True | 56 |
| `G2_CAPACITY_IS_THE_SEPARATOR` | True | 56 |
| `G6_CROSS_SCALE_CONSISTENCY` | True | 56 |
| `G8_VERDICT_CONSTANCY_WITHIN_CELL` | True | 28 |

## Arms (capability)

| arm | correct | rate | n |
|---|---|---|---|
| `B6_GREEDY_SUBSET_UNTYPED` | 56 | 1.0000 | 56 |
| `B7_L1_PATH_UNTYPED` | 56 | 1.0000 | 56 |
| `B8_CAPACITY_MATCHED_BEST` | 56 | 1.0000 | 56 |
| `M_TYPED_COLLECTIVE_STATE` | 56 | 1.0000 | 56 |
| `C_ALWAYS_FLAT` | 32 | 0.5714 | 56 |
| `B4X_FITTED_UNTYPED_UNIT_SIGN_LEARNED_CONTROL` | 28 | 0.5000 | 56 |
| `B4X_INFORMATION_MATCHED_UNTYPED_EQUAL_WEIGHT` | 28 | 0.5000 | 56 |
| `C_ALWAYS_RISE` | 16 | 0.2857 | 56 |
| `C_ALWAYS_FALL` | 8 | 0.1429 | 56 |

## Coverage

- cells exercised: 28 / 28
- never exercised: none
