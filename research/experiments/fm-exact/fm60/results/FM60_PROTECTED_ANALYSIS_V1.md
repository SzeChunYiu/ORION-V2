# FM60 analysis — PROTECTED

Instances: 125; results sha256 `20041fd5ed96b4286ca2382ff7acac837af27950cb64d0bf468033cc64713ffd`.


## Per-arm exactness

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| P0_INDUCTIVE_CONFIRMATION | 24/125 | 0.192 | 0 | 0 |
| P1_FIXED_LESSON_TABLE | 25/125 | 0.200 | 0 | 0 |
| P2_EXHAUSTIVE_MODEL_SEARCH | 100/125 | 0.800 | 0 | 0 |
| P3_DERIVATION_PROOF_SEARCH | 25/125 | 0.200 | 0 | 0 |
| P4_SMALL_SCOPE_BOUNDED_CHECK | 91/125 | 0.728 | 0 | 0 |
| F0_PARENT_FEDERATION | 125/125 | 1.000 | 0 | 0 |
| M_F2_OBSTRUCTION_DISCOVERY_FULL | 124/125 | 0.992 | 0 | 0 |
| M_MINUS_OBSTRUCTION_SEARCH | 24/125 | 0.192 | 0 | 0 |
| M_MINUS_PROOF_WITNESS | 100/125 | 0.800 | 0 | 0 |
| M_MINUS_MINIMALITY_ESCALATION | 96/125 | 0.768 | 0 | 0 |
| M_MINUS_MULTIPLICITY_CHECK | 99/125 | 0.792 | 0 | 0 |
| C_ALWAYS_ACCEPT | 25/125 | 0.200 | 100 | 0 |
| C_ALWAYS_BLOCK | 25/125 | 0.200 | 0 | 0 |
| C_RANDOM_DISPOSITION | 20/125 | 0.160 | 12 | 0 |

## Per-family exact rate

| arm | no_obstruction | single_hidden_obstruction | multiple_obstruction | minimal_counterexample | misleading_surface_support |
|---|---|---|---|---|---|
| P0_INDUCTIVE_CONFIRMATION | 0.00 | 0.96 | 0.00 | 0.00 | 0.00 |
| P1_FIXED_LESSON_TABLE | 0.00 | 0.40 | 0.28 | 0.00 | 0.32 |
| P2_EXHAUSTIVE_MODEL_SEARCH | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| P3_DERIVATION_PROOF_SEARCH | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P4_SMALL_SCOPE_BOUNDED_CHECK | 0.00 | 1.00 | 0.92 | 0.84 | 0.88 |
| F0_PARENT_FEDERATION | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_F2_OBSTRUCTION_DISCOVERY_FULL | 0.96 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_OBSTRUCTION_SEARCH | 0.96 | 0.00 | 0.00 | 0.00 | 0.00 |
| M_MINUS_PROOF_WITNESS | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_MINIMALITY_ESCALATION | 0.96 | 1.00 | 1.00 | 0.00 | 0.88 |
| M_MINUS_MULTIPLICITY_CHECK | 0.96 | 1.00 | 0.00 | 1.00 | 1.00 |
| C_ALWAYS_ACCEPT | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_BLOCK | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| C_RANDOM_DISPOSITION | 0.20 | 0.20 | 0.04 | 0.20 | 0.16 |

## Gates (verdict, violations / instances evaluated)

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | **PASS** | 0 | 12 | True |
| G0b_ORACLE_SELF_AGREEMENT | **PASS** | 0 | 125 | True |
| G0c_NULL_CALIBRATION | **PASS** | 0 | 4 | True |
| G0d_DECOY_COVERAGE | **PASS** | 0 | 3 | True |
| G0e_PLANTED_POSITIVES | **PASS** | 0 | 7 | True |
| G0f_FAMILY_DISCRIMINATION | **PASS** | 0 | 2 | True |
| G1a_PARENT_REPRODUCES_M | **FAIL** | 1 | 125 | True |
| G1b_M_ADVANTAGE | **NOT_FIRED** | 1 | 125 | False |
| G2_ANTI_PERMISSIVENESS | **PASS** | 0 | 100 | True |
| G3_MECHANISM_BY_OMISSION | **NOT_APPLICABLE** | 0 | 0 | False |

## Route

`PARENT_SUFFICIENT` — no significant M advantage over the strongest faithful parent. Cost flag: `COST_ADVANTAGE_PARENT`.

