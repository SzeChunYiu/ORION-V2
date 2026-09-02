# FM50 analysis — DEVELOPMENT

Instances: 24; results sha256 `ed6b1faa8e4f756499bc31545b9c8a694e544a234959afd06fb965a3b69d5bec`.


## Per-arm exactness

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| P0_NAME_SIMILARITY | 3/24 | 0.125 | 12 | 6 |
| P1_GRAPH_HOMOMORPHISM | 12/24 | 0.500 | 12 | 0 |
| P2_CATEGORY_LAW_FUNCTOR | 21/24 | 0.875 | 3 | 0 |
| P3_DIAGRAM_CHASE | 11/24 | 0.458 | 12 | 0 |
| P4_FAITHFULNESS | 12/24 | 0.500 | 12 | 0 |
| P5_FIXED_LESSON_INJECTION | 12/24 | 0.500 | 9 | 0 |
| F0_PARENT_FEDERATION | 24/24 | 1.000 | 0 | 0 |
| M_F2_FUNCTORIAL_TRANSFER_FULL | 24/24 | 1.000 | 0 | 0 |
| M_MINUS_ENDPOINT_DISCIPLINE | 21/24 | 0.875 | 0 | 0 |
| M_MINUS_IDENTITY_CHECK | 18/24 | 0.750 | 3 | 0 |
| M_MINUS_COMPOSITION_CHECK | 18/24 | 0.750 | 3 | 0 |
| M_MINUS_FAITHFULNESS_RECOVERY | 21/24 | 0.875 | 3 | 0 |
| C_ALWAYS_TRANSFER | 9/24 | 0.375 | 15 | 0 |
| C_ALWAYS_BLOCK | 3/24 | 0.125 | 0 | 9 |
| C_RANDOM_DISPOSITION | 4/24 | 0.167 | 3 | 8 |

## Per-family exact rate

| arm | VALID_FUNCTOR | SURFACE_NAME_DECOY | LICENSED_COLLAPSE | ENDPOINT_VIOLATION | IDENTITY_NOT_PRESERVED | COMPOSITION_NOT_PRESERVED | MIXED_LAW_OBSTRUCTION | FALSE_EQUIVALENCE |
|---|---|---|---|---|---|---|---|---|
| P0_NAME_SIMILARITY | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P1_GRAPH_HOMOMORPHISM | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P2_CATEGORY_LAW_FUNCTOR | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| P3_DIAGRAM_CHASE | 1.00 | 1.00 | 1.00 | 0.67 | 0.00 | 0.00 | 0.00 | 0.00 |
| P4_FAITHFULNESS | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| P5_FIXED_LESSON_INJECTION | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| F0_PARENT_FEDERATION | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_F2_FUNCTORIAL_TRANSFER_FULL | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_ENDPOINT_DISCIPLINE | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_IDENTITY_CHECK | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 |
| M_MINUS_COMPOSITION_CHECK | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 |
| M_MINUS_FAITHFULNESS_RECOVERY | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| C_ALWAYS_TRANSFER | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_BLOCK | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| C_RANDOM_DISPOSITION | 0.00 | 0.33 | 0.00 | 0.33 | 0.00 | 0.00 | 0.67 | 0.00 |

## Gates (verdict, violations / instances evaluated)

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | **PASS** | 0 | 11 | True |
| G0b_ORACLE_SELF_AGREEMENT | **PASS** | 0 | 24 | True |
| G0c_NULL_CALIBRATION | **PASS** | 0 | 4 | True |
| G0d_DECOY_COVERAGE | **PASS** | 0 | 4 | True |
| G0e_PLANTED_POSITIVES | **PASS** | 0 | 6 | True |
| G0f_FAMILY_DISCRIMINATION | **PASS** | 0 | 2 | True |
| G1a_PARENT_REPRODUCES_M | **PASS** | 0 | 24 | True |
| G1b_M_ADVANTAGE | **NOT_FIRED** | 1 | 24 | False |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | 15 | True |
| G3_MECHANISM_BY_OMISSION | **NOT_APPLICABLE** | 0 | 0 | False |

## Route

`PARENT_SUFFICIENT` — F0_PARENT_FEDERATION reproduces M_F2_FUNCTORIAL_TRANSFER_FULL's dispositions (identity 1.0000). Cost flag: `COST_ADVANTAGE_M`.

