# FM30 analysis — PROTECTED

Instances: 100; results sha256 `15f4895d7309b3ea8ed529a599b53e0e7712b9aab042444d2b0a159fc6d98fb0`.


## Per-arm exactness

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| P0_FIXED_LESSON_INJECTION | 40/100 | 0.400 | 0 | 0 |
| P1_GALOIS_CLOSURE | 40/100 | 0.400 | 0 | 0 |
| P2_LATTICE_ORDER_GEOMETRY | 60/100 | 0.600 | 0 | 0 |
| P3_ATTRIBUTE_EXPLORATION | 40/100 | 0.400 | 0 | 0 |
| F0_PARENT_FEDERATION | 100/100 | 1.000 | 0 | 0 |
| M_F2_CONCEPTUAL_DEVELOPMENT_FULL | 92/100 | 0.920 | 0 | 0 |
| M_MINUS_EXTENT_GEOMETRY | 60/100 | 0.600 | 0 | 0 |
| M_MINUS_BRIDGE_DETECTION | 77/100 | 0.770 | 0 | 0 |
| M_MINUS_CLOSURE_RECOMPUTATION | 72/100 | 0.720 | 0 | 0 |
| M_MINUS_OLD_CASE_RETENTION | 64/100 | 0.640 | 36 | 0 |
| C_ALWAYS_NO_CHANGE | 12/100 | 0.120 | 36 | 0 |
| C_ALWAYS_SPECIALIZE | 20/100 | 0.200 | 36 | 0 |
| C_RANDOM_TRANSITION | 7/100 | 0.070 | 23 | 0 |

## Per-family exact rate

| arm | NO_CHANGE | SPECIALIZE | SPLIT | MERGE | BRIDGE |
|---|---|---|---|---|---|
| P0_FIXED_LESSON_INJECTION | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| P1_GALOIS_CLOSURE | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| P2_LATTICE_ORDER_GEOMETRY | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 |
| P3_ATTRIBUTE_EXPLORATION | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| F0_PARENT_FEDERATION | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_F2_CONCEPTUAL_DEVELOPMENT_FULL | 0.95 | 1.00 | 1.00 | 0.90 | 0.75 |
| M_MINUS_EXTENT_GEOMETRY | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 |
| M_MINUS_BRIDGE_DETECTION | 0.95 | 1.00 | 1.00 | 0.90 | 0.00 |
| M_MINUS_CLOSURE_RECOMPUTATION | 0.95 | 0.00 | 1.00 | 0.90 | 0.75 |
| M_MINUS_OLD_CASE_RETENTION | 0.75 | 1.00 | 0.50 | 0.45 | 0.50 |
| C_ALWAYS_NO_CHANGE | 0.60 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_SPECIALIZE | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| C_RANDOM_TRANSITION | 0.05 | 0.10 | 0.10 | 0.10 | 0.00 |

## Gates (verdict, violations / instances evaluated)

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | **PASS** | 0 | 9 | True |
| G0b_ORACLE_SELF_AGREEMENT | **PASS** | 0 | 100 | True |
| G0c_NULL_CALIBRATION | **PASS** | 0 | 4 | True |
| G0d_DECOY_COVERAGE | **PASS** | 0 | 4 | True |
| G0e_PLANTED_POSITIVES | **PASS** | 0 | 6 | True |
| G0f_FAMILY_DISCRIMINATION | **PASS** | 0 | 2 | True |
| G1a_PARENT_REPRODUCES_M | **FAIL** | 1 | 100 | True |
| G1b_M_ADVANTAGE | **NOT_FIRED** | 1 | 100 | False |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | 36 | True |
| G3_MECHANISM_BY_OMISSION | **NOT_APPLICABLE** | 0 | 0 | False |

## Route

`PARENT_SUFFICIENT` — no significant M advantage over the strongest faithful parent. Cost flag: `COST_ADVANTAGE_M`.

