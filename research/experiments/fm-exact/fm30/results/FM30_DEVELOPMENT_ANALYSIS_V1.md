# FM30 analysis — DEVELOPMENT

Instances: 15; results sha256 `8517dab07655e83cf7bab6ccd204cf3dacdc748c522461329be7c18ecf656d92`.


## Per-arm exactness

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| P0_FIXED_LESSON_INJECTION | 6/15 | 0.400 | 0 | 0 |
| P1_GALOIS_CLOSURE | 6/15 | 0.400 | 0 | 0 |
| P2_LATTICE_ORDER_GEOMETRY | 9/15 | 0.600 | 0 | 0 |
| P3_ATTRIBUTE_EXPLORATION | 6/15 | 0.400 | 0 | 0 |
| F0_PARENT_FEDERATION | 15/15 | 1.000 | 0 | 0 |
| M_F2_CONCEPTUAL_DEVELOPMENT_FULL | 15/15 | 1.000 | 0 | 0 |
| M_MINUS_EXTENT_GEOMETRY | 9/15 | 0.600 | 0 | 0 |
| M_MINUS_BRIDGE_DETECTION | 12/15 | 0.800 | 0 | 0 |
| M_MINUS_CLOSURE_RECOMPUTATION | 12/15 | 0.800 | 0 | 0 |
| M_MINUS_OLD_CASE_RETENTION | 14/15 | 0.933 | 1 | 0 |
| C_ALWAYS_NO_CHANGE | 2/15 | 0.133 | 1 | 0 |
| C_ALWAYS_SPECIALIZE | 3/15 | 0.200 | 1 | 0 |
| C_RANDOM_TRANSITION | 1/15 | 0.067 | 0 | 0 |

## Per-family exact rate

| arm | NO_CHANGE | SPECIALIZE | SPLIT | MERGE | BRIDGE |
|---|---|---|---|---|---|
| P0_FIXED_LESSON_INJECTION | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| P1_GALOIS_CLOSURE | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| P2_LATTICE_ORDER_GEOMETRY | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 |
| P3_ATTRIBUTE_EXPLORATION | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| F0_PARENT_FEDERATION | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_F2_CONCEPTUAL_DEVELOPMENT_FULL | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_EXTENT_GEOMETRY | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 |
| M_MINUS_BRIDGE_DETECTION | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| M_MINUS_CLOSURE_RECOMPUTATION | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_OLD_CASE_RETENTION | 1.00 | 1.00 | 1.00 | 0.67 | 1.00 |
| C_ALWAYS_NO_CHANGE | 0.67 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_SPECIALIZE | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| C_RANDOM_TRANSITION | 0.00 | 0.00 | 0.00 | 0.33 | 0.00 |

## Gates (verdict, violations / instances evaluated)

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | **PASS** | 0 | 9 | True |
| G0b_ORACLE_SELF_AGREEMENT | **PASS** | 0 | 15 | True |
| G0c_NULL_CALIBRATION | **PASS** | 0 | 4 | True |
| G0d_DECOY_COVERAGE | **PASS** | 0 | 4 | True |
| G0e_PLANTED_POSITIVES | **PASS** | 0 | 6 | True |
| G0f_FAMILY_DISCRIMINATION | **PASS** | 0 | 2 | True |
| G1a_PARENT_REPRODUCES_M | **PASS** | 0 | 15 | True |
| G1b_M_ADVANTAGE | **NOT_FIRED** | 1 | 15 | False |
| G2_ANTI_PERMISSIVENESS | **CANNOT_CHECK** | 0 | 1 | True |
| G3_MECHANISM_BY_OMISSION | **NOT_APPLICABLE** | 0 | 0 | False |

## Route

`PARENT_SUFFICIENT` — F0_PARENT_FEDERATION reproduces M_F2_CONCEPTUAL_DEVELOPMENT_FULL's dispositions (identity 1.0000); NOTE 1 hard gate(s) could not be evaluated on this split and are NOT reported as passing: ['G2_ANTI_PERMISSIVENESS']. Cost flag: `COST_ADVANTAGE_M`.

