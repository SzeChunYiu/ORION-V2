# ME-X6 V2 PROTECTED analysis

- instances: 1400
- route: `PARENT_SUFFICIENT` — terminal `TYPING_NOT_SEPARATED_AT_MATCHED_CAPACITY`
- reason: a LEARNED untyped comparator whose weight class contains zero reproduces M's capability verdict on every instance. The separation V1 measured is attributable to the comparator's capacity, not to typing. ME-X6 contracts to an interpretive framework -- the protocol's own contraction rule, and a legitimate result, not a failure

Only the CAPABILITY half is scored. V1 computes the activity direction from the same channels by the same call for every arm, so an activity agreement is equal by construction and is not evidence.

## Gates

| gate | pass | n_evaluated |
|---|---|---|
| `G0a_KNOWN_ANSWER` | True | 12 |
| `G0b_GENERATOR_VALIDITY` | True | 1400 |
| `G0c_NULL_CALIBRATION` | True | 1400 |
| `G0d_M_EXACT_BY_CONSTRUCTION` | True | 1400 |
| `G0e_CAPACITY_MATCHING_BIT` | True | 16 |
| `G1a_M_AHEAD_OF_CAPACITY_MATCHED_PARENT` | False | 1400 |
| `G1b_TIE_AT_MATCHED_CAPACITY` | True | 1400 |
| `G2_CAPACITY_IS_THE_SEPARATOR` | True | 1400 |
| `G6_CROSS_SCALE_CONSISTENCY` | True | 1400 |
| `G8_VERDICT_CONSTANCY_WITHIN_CELL` | True | 28 |

## Arms (capability)

| arm | correct | rate | n |
|---|---|---|---|
| `B6_GREEDY_SUBSET_UNTYPED` | 1400 | 1.0000 | 1400 |
| `B7_L1_PATH_UNTYPED` | 1400 | 1.0000 | 1400 |
| `B8_CAPACITY_MATCHED_BEST` | 1400 | 1.0000 | 1400 |
| `M_TYPED_COLLECTIVE_STATE` | 1400 | 1.0000 | 1400 |
| `C_ALWAYS_FLAT` | 800 | 0.5714 | 1400 |
| `B4X_FITTED_UNTYPED_UNIT_SIGN_LEARNED_CONTROL` | 700 | 0.5000 | 1400 |
| `B4X_INFORMATION_MATCHED_UNTYPED_EQUAL_WEIGHT` | 700 | 0.5000 | 1400 |
| `C_ALWAYS_RISE` | 400 | 0.2857 | 1400 |
| `C_ALWAYS_FALL` | 200 | 0.1429 | 1400 |

## Coverage

- cells exercised: 28 / 28
- never exercised: none
