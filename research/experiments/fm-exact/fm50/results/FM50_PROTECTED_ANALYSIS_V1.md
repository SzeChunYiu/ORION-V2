# FM50 analysis — PROTECTED

Instances: 104; results sha256 `e99bd75710a0445524f940e4a395ebd77a902ae104ee0b70e287dda5ff8e0cd0`.


## Per-arm exactness

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| P0_NAME_SIMILARITY | 13/104 | 0.125 | 52 | 26 |
| P1_GRAPH_HOMOMORPHISM | 52/104 | 0.500 | 52 | 0 |
| P2_CATEGORY_LAW_FUNCTOR | 91/104 | 0.875 | 13 | 0 |
| P3_DIAGRAM_CHASE | 59/104 | 0.567 | 43 | 0 |
| P4_FAITHFULNESS | 52/104 | 0.500 | 52 | 0 |
| P5_FIXED_LESSON_INJECTION | 52/104 | 0.500 | 39 | 0 |
| F0_PARENT_FEDERATION | 104/104 | 1.000 | 0 | 0 |
| M_F2_FUNCTORIAL_TRANSFER_FULL | 104/104 | 1.000 | 0 | 0 |
| M_MINUS_ENDPOINT_DISCIPLINE | 91/104 | 0.875 | 0 | 0 |
| M_MINUS_IDENTITY_CHECK | 78/104 | 0.750 | 13 | 0 |
| M_MINUS_COMPOSITION_CHECK | 78/104 | 0.750 | 13 | 0 |
| M_MINUS_FAITHFULNESS_RECOVERY | 91/104 | 0.875 | 13 | 0 |
| C_ALWAYS_TRANSFER | 39/104 | 0.375 | 65 | 0 |
| C_ALWAYS_BLOCK | 13/104 | 0.125 | 0 | 39 |
| C_RANDOM_DISPOSITION | 20/104 | 0.192 | 8 | 29 |

## Per-family exact rate

| arm | VALID_FUNCTOR | SURFACE_NAME_DECOY | LICENSED_COLLAPSE | ENDPOINT_VIOLATION | IDENTITY_NOT_PRESERVED | COMPOSITION_NOT_PRESERVED | MIXED_LAW_OBSTRUCTION | FALSE_EQUIVALENCE |
|---|---|---|---|---|---|---|---|---|
| P0_NAME_SIMILARITY | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P1_GRAPH_HOMOMORPHISM | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P2_CATEGORY_LAW_FUNCTOR | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| P3_DIAGRAM_CHASE | 1.00 | 1.00 | 1.00 | 0.77 | 0.00 | 0.77 | 0.00 | 0.00 |
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
| C_RANDOM_DISPOSITION | 0.15 | 0.23 | 0.38 | 0.15 | 0.08 | 0.23 | 0.15 | 0.15 |

## Gates (verdict, violations / instances evaluated)

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | **PASS** | 0 | 11 | True |
| G0b_ORACLE_SELF_AGREEMENT | **PASS** | 0 | 104 | True |
| G0c_NULL_CALIBRATION | **PASS** | 0 | 4 | True |
| G0d_DECOY_COVERAGE | **PASS** | 0 | 4 | True |
| G0e_PLANTED_POSITIVES | **PASS** | 0 | 6 | True |
| G0f_FAMILY_DISCRIMINATION | **PASS** | 0 | 2 | True |
| G1a_PARENT_REPRODUCES_M | **PASS** | 0 | 104 | True |
| G1b_M_ADVANTAGE | **NOT_FIRED** | 1 | 104 | False |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | 65 | True |
| G3_MECHANISM_BY_OMISSION | **NOT_APPLICABLE** | 0 | 0 | False |

## Route

`PARENT_SUFFICIENT` — F0_PARENT_FEDERATION reproduces M_F2_FUNCTORIAL_TRANSFER_FULL's dispositions (identity 1.0000). Cost flag: `COST_ADVANTAGE_M`.

