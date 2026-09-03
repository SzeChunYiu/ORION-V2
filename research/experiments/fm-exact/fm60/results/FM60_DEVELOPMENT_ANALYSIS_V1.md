# FM60 analysis — DEVELOPMENT

Instances: 15; results sha256 `a97a9bd211a246866cf55633c5e8fce64514ad207a7e4eba20d10f367228dc46`.


## Per-arm exactness

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| P0_INDUCTIVE_CONFIRMATION | 3/15 | 0.200 | 3 | 3 |
| P1_FIXED_LESSON_TABLE | 1/15 | 0.067 | 8 | 1 |
| P2_EXHAUSTIVE_MODEL_SEARCH | 12/15 | 0.800 | 0 | 0 |
| P3_DERIVATION_PROOF_SEARCH | 3/15 | 0.200 | 9 | 0 |
| P4_SMALL_SCOPE_BOUNDED_CHECK | 9/15 | 0.600 | 3 | 0 |
| F0_PARENT_FEDERATION | 15/15 | 1.000 | 0 | 0 |
| M_F2_OBSTRUCTION_DISCOVERY_FULL | 15/15 | 1.000 | 0 | 0 |
| M_MINUS_OBSTRUCTION_SEARCH | 3/15 | 0.200 | 9 | 0 |
| M_MINUS_PROOF_WITNESS | 12/15 | 0.800 | 0 | 0 |
| M_MINUS_MINIMALITY_ESCALATION | 10/15 | 0.667 | 0 | 0 |
| M_MINUS_MULTIPLICITY_CHECK | 12/15 | 0.800 | 0 | 3 |
| C_ALWAYS_ACCEPT | 3/15 | 0.200 | 9 | 0 |
| C_ALWAYS_BLOCK | 3/15 | 0.200 | 9 | 0 |
| C_RANDOM_DISPOSITION | 0/15 | 0.000 | 8 | 2 |

## Per-family exact rate

| arm | no_obstruction | single_hidden_obstruction | multiple_obstruction | minimal_counterexample | misleading_surface_support |
|---|---|---|---|---|---|
| P0_INDUCTIVE_CONFIRMATION | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| P1_FIXED_LESSON_TABLE | 0.00 | 0.33 | 0.00 | 0.00 | 0.00 |
| P2_EXHAUSTIVE_MODEL_SEARCH | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| P3_DERIVATION_PROOF_SEARCH | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| P4_SMALL_SCOPE_BOUNDED_CHECK | 0.00 | 1.00 | 1.00 | 0.67 | 0.33 |
| F0_PARENT_FEDERATION | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_F2_OBSTRUCTION_DISCOVERY_FULL | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_OBSTRUCTION_SEARCH | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| M_MINUS_PROOF_WITNESS | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M_MINUS_MINIMALITY_ESCALATION | 1.00 | 1.00 | 1.00 | 0.00 | 0.33 |
| M_MINUS_MULTIPLICITY_CHECK | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 |
| C_ALWAYS_ACCEPT | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| C_ALWAYS_BLOCK | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| C_RANDOM_DISPOSITION | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Gates (verdict, violations / instances evaluated)

| gate | verdict | violations | n evaluated | hard |
|---|---|---|---|---|
| G0a_KNOWN_ANSWER | **PASS** | 0 | 12 | True |
| G0b_ORACLE_SELF_AGREEMENT | **PASS** | 0 | 15 | True |
| G0c_NULL_CALIBRATION | **PASS** | 0 | 4 | True |
| G0d_DECOY_COVERAGE | **PASS** | 0 | 3 | True |
| G0e_PLANTED_POSITIVES | **PASS** | 0 | 7 | True |
| G0f_FAMILY_DISCRIMINATION | **PASS** | 0 | 2 | True |
| G1a_PARENT_REPRODUCES_M | **PASS** | 0 | 15 | True |
| G1b_M_ADVANTAGE | **NOT_FIRED** | 1 | 15 | False |
| G2_ANTI_PERMISSIVENESS | **CANNOT_CHECK** | 0 | 9 | True |
| G3_MECHANISM_BY_OMISSION | **NOT_APPLICABLE** | 0 | 0 | False |

## Route

`PARENT_SUFFICIENT` — F0_PARENT_FEDERATION reproduces M_F2_OBSTRUCTION_DISCOVERY_FULL's dispositions (identity 1.0000); NOTE 1 hard gate(s) could not be evaluated on this split and are NOT reported as passing: ['G2_ANTI_PERMISSIVENESS']. Cost flag: `COST_ADVANTAGE_PARENT`.

