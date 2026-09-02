# FM10 analysis — DEVELOPMENT

Instances: 21; results sha256 `100c5718d99aa39dbfc8a03d48fec5329b4fff1dc70a24a6568e8c75da2ec1cd`.


## Per-arm exactness

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| P0_SURFACE_SIMILARITY | 11/21 | 0.524 | 2 | 4 |
| P1_SME_STRUCTURE_MAPPING | 18/21 | 0.857 | 3 | 0 |
| P2_COMPLETE_HOMOMORPHISM | 18/21 | 0.857 | 3 | 0 |
| P3_FIXED_LESSON_INJECTION | 9/21 | 0.429 | 3 | 3 |
| P4_INVARIANCE_PARENT | 9/21 | 0.429 | 10 | 0 |
| F0_PARENT_FEDERATION | 21/21 | 1.000 | 0 | 0 |
| M_F2_TRANSFER_DISCOVERY_FULL | 21/21 | 1.000 | 0 | 0 |
| M_MINUS_RELATIONAL_MAPPING | 12/21 | 0.571 | 0 | 3 |
| M_MINUS_INVARIANCE_TEST | 18/21 | 0.857 | 3 | 0 |
| M_MINUS_OBSTRUCTION_SEARCH | 8/21 | 0.381 | 0 | 5 |
| M_MINUS_TYPE_DISCIPLINE | 21/21 | 1.000 | 0 | 0 |
| C_ALWAYS_TRANSFER | 6/21 | 0.286 | 15 | 0 |
| C_ALWAYS_BLOCK | 6/21 | 0.286 | 0 | 6 |
| C_RANDOM_DISPOSITION | 2/21 | 0.095 | 6 | 5 |

## Per-family exact rate

| arm | ISOMORPHIC_TRANSFER | PARTIAL_HOMOMORPHISM | NON_HOMOMORPHISM | SURFACE_DECOY | DIRECTION_REVERSAL | RELATION_TYPE_MISMATCH | INVARIANT_BREAKING_EMBEDDING |
|---|---|---|---|---|---|---|---|
| P0_SURFACE_SIMILARITY | 0.67 | 1.00 | 1.00 | 0.00 | 0.67 | 0.33 | 0.00 |
| P1_SME_STRUCTURE_MAPPING | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| P2_COMPLETE_HOMOMORPHISM | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| P3_FIXED_LESSON_INJECTION | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P4_INVARIANCE_PARENT | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 |
| F0_PARENT_FEDERATION | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_F2_TRANSFER_DISCOVERY_FULL | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_RELATIONAL_MAPPING | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| M_MINUS_INVARIANCE_TEST | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| M_MINUS_OBSTRUCTION_SEARCH | 0.00 | 1.00 | 1.00 | 0.33 | 0.00 | 0.33 | 0.00 |
| M_MINUS_TYPE_DISCIPLINE | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| C_ALWAYS_TRANSFER | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_BLOCK | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_RANDOM_DISPOSITION | 0.00 | 0.33 | 0.00 | 0.33 | 0.00 | 0.00 | 0.00 |

## Gates (verdict, violations / instances evaluated)

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | **PASS** | 0 | 11 | True |
| G0b_ORACLE_SELF_AGREEMENT | **PASS** | 0 | 21 | True |
| G0c_NULL_CALIBRATION | **PASS** | 0 | 4 | True |
| G0d_DECOY_COVERAGE | **PASS** | 0 | 4 | True |
| G0e_PLANTED_POSITIVES | **PASS** | 0 | 5 | True |
| G0f_FAMILY_DISCRIMINATION | **PASS** | 0 | 2 | True |
| G1a_PARENT_REPRODUCES_M | **PASS** | 0 | 21 | True |
| G1b_M_ADVANTAGE | **NOT_FIRED** | 1 | 21 | False |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | 15 | True |
| G3_MECHANISM_BY_OMISSION | **NOT_APPLICABLE** | 0 | 0 | False |

## Route

`PARENT_SUFFICIENT` — F0_PARENT_FEDERATION reproduces M_F2_TRANSFER_DISCOVERY_FULL's dispositions (identity 1.0000). Cost flag: `COST_ADVANTAGE_PARENT`.

