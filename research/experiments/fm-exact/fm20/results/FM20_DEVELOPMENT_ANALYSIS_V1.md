# FM20 analysis — DEVELOPMENT

Instances: 15; results sha256 `735f7ebfdd01c6d8d03a167780324c59b67334ac8419d4a3e086c7aedfe29604`.


## Per-arm exactness

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| P0_FIXED_LESSON_INJECTION | 12/15 | 0.800 | 3 | 0 |
| P1_PLOTKIN_LGG | 9/15 | 0.600 | 6 | 0 |
| P2_CANDIDATE_ELIMINATION | 12/15 | 0.800 | 2 | 0 |
| P3_MDL_COMPRESSION | 11/15 | 0.733 | 3 | 0 |
| F0_PARENT_FEDERATION | 15/15 | 1.000 | 0 | 0 |
| M_F2_ABSTRACTION_INDUCTION_FULL | 15/15 | 1.000 | 0 | 0 |
| M_MINUS_VARIABLE_IDENTITY | 13/15 | 0.867 | 0 | 2 |
| M_MINUS_NEGATIVE_CHALLENGE | 12/15 | 0.800 | 3 | 0 |
| M_MINUS_COMPRESSION_CRITERION | 12/15 | 0.800 | 2 | 0 |
| M_MINUS_LEAST_GENERALITY | 5/15 | 0.333 | 6 | 0 |
| C_ALWAYS_ACCEPT | 0/15 | 0.000 | 6 | 0 |
| C_ALWAYS_REJECT | 0/15 | 0.000 | 0 | 9 |
| C_RANDOM_DISPOSITION | 1/15 | 0.067 | 2 | 7 |

## Per-family exact rate

| arm | LEAST_GENERAL_PATTERN | DISTRACTOR_REGULARITY | OVER_GENERALIZATION | UNDER_GENERALIZATION | NO_VALID_COMMON_ABSTRACTION |
|---|---|---|---|---|---|
| P0_FIXED_LESSON_INJECTION | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 |
| P1_PLOTKIN_LGG | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 |
| P2_CANDIDATE_ELIMINATION | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| P3_MDL_COMPRESSION | 1.00 | 0.67 | 0.00 | 1.00 | 1.00 |
| F0_PARENT_FEDERATION | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_F2_ABSTRACTION_INDUCTION_FULL | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_VARIABLE_IDENTITY | 1.00 | 0.33 | 1.00 | 1.00 | 1.00 |
| M_MINUS_NEGATIVE_CHALLENGE | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 |
| M_MINUS_COMPRESSION_CRITERION | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| M_MINUS_LEAST_GENERALITY | 0.00 | 0.67 | 0.00 | 1.00 | 0.00 |
| C_ALWAYS_ACCEPT | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_REJECT | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_RANDOM_DISPOSITION | 0.00 | 0.00 | 0.33 | 0.00 | 0.00 |

## Gates (verdict, violations / instances evaluated)

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | **PASS** | 0 | 10 | True |
| G0b_ORACLE_SELF_AGREEMENT | **PASS** | 0 | 15 | True |
| G0c_NULL_CALIBRATION | **PASS** | 0 | 4 | True |
| G0d_DECOY_COVERAGE | **PASS** | 0 | 4 | True |
| G0e_PLANTED_POSITIVES | **PASS** | 0 | 6 | True |
| G0f_FAMILY_DISCRIMINATION | **PASS** | 0 | 2 | True |
| G1a_PARENT_REPRODUCES_M | **PASS** | 0 | 15 | True |
| G1b_M_ADVANTAGE | **NOT_FIRED** | 1 | 15 | False |
| G2_ANTI_PERMISSIVENESS | **CANNOT_CHECK** | 0 | 6 | True |
| G3_MECHANISM_BY_OMISSION | **NOT_APPLICABLE** | 0 | 0 | False |

## Route

`PARENT_SUFFICIENT` — F0_PARENT_FEDERATION reproduces M_F2_ABSTRACTION_INDUCTION_FULL's dispositions (identity 1.0000); NOTE 1 hard gate(s) could not be evaluated on this split and are NOT reported as passing: ['G2_ANTI_PERMISSIVENESS']. Cost flag: `COST_PARITY_WITHIN_2X`.

