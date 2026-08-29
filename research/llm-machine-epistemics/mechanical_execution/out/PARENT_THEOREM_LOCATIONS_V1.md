# PARENT_THEOREM_LOCATIONS_V1 — theorem-to-receipt provenance map

Mechanical map from `MECHANICAL_EXECUTION_SPEC_V4.md` §1 theorem IDs (+ V5 additions)
to the audit receipts in `out/`. Every SUPPORTED row was re-validated against its
receipt JSON at generation time by `llm_epistemics_theorem_locations.py`.

| Group | Theorem ID | Spec | Receipt | Evidence | Verdict |
|---|---|---|---|---|---|
| Predictive base | `L1_PREDICTIVE_SUFFICIENT_REFINES_SP` | V4 §3 | `PARTITION_ENUMERATION_RECEIPT_V1.json` | verdicts.L1_PREDICTIVE_SUFFICIENT_REFINES_SP | PASS |
| Predictive base | `T2_ENTROPY_MINIMAL_PREDICTIVE_ISOMORPHIC_SP` | V4 §3 | `PARTITION_ENUMERATION_RECEIPT_V1.json` | verdicts.T2_...__structural_partition_layer | PASS |
| Predictive base | `T2b_D4_cardinality_minimal_corollary` | V4 §3 | `PARTITION_ENUMERATION_RECEIPT_V1.json` | verdicts.T2b_D4_cardinality_minimal_corollary | PASS |
| Static responsibility | `R21_ANY_OPTIMAL_MIN_SELECTOR_ENTROPY` | V4 §4 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.R21_ANY_OPTIMAL_MIN_SELECTOR_ENTROPY | PASS |
| Static responsibility | `R22_CANONICAL_ACTION_COST` | V4 §4 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.R22_CANONICAL_ACTION_COST | PASS |
| Static responsibility | `R23_OPTIMAL_ACTION_SET_COST` | V4 §4 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.R23_OPTIMAL_ACTION_SET_COST | PASS |
| Static responsibility | `R24_ACTION_AND_RISK_COST` | V4 §4 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.R24_ACTION_AND_RISK_COST | PASS |
| Static responsibility | `R25_EXACT_TARGET_SPECIAL_CASE` | V4 §4 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.R25_EXACT_TARGET_SPECIAL_CASE | PASS |
| Static responsibility | `R26_JOINT_ANY_OPTIMAL_SELECTOR_COST` | V4 §4 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.R26_JOINT_ANY_OPTIMAL_SELECTOR_COST | PASS |
| Static responsibility | `R27_ZERO_COST_COMMON_OPTIMAL_ACTION` | V4 §4 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.R27_ZERO_COST_COMMON_OPTIMAL_ACTION | PASS |
| Static responsibility | `TIE_SEMANTICS_FIXTURE` | V4 §4 tie fixture | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.TIE_SEMANTICS_FIXTURE | PASS |
| Deficit identities | `D1_ACQUISITION_COMPRESSION_DECOMPOSITION` | V4 §10 | `EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json` | verdicts.D1 | PASS |
| Deficit identities | `D2_NEW_OBSERVATION_GAIN` | V4 §10 | `EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json` | verdicts.D2 | PASS |
| Deficit identities | `D3_PROSPECTIVE_DEFICIENCY_IDENTITY` | V4 §10 | `EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json` | verdicts.D3 | PASS |
| Deficit identities | `D-CONTROLS_all_five_mandatory_controls` | V4 §10 | `EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json` | verdicts.CONTROLS | PASS |
| Classical benchmarks | `T8A_SINGLE_LOGLOSS_FRONTIER` | V4 §11 | `LOGLOSS_PARENT_BENCHMARK_V1.json` | verdicts.A_achievability_shared_r + verdicts.A_registered_class_tightness | PASS |
| Classical benchmarks | `T8B_INDEPENDENT_RESPONSIBILITY_FRONTIER` | V4 §11 | `LOGLOSS_PARENT_BENCHMARK_V1.json` | verdicts.B_cond_independent_product_sum | PASS |
| Classical benchmarks | `T8C_SHARED_EXACT_STATE_SAVING` | V4 §11 | `LOGLOSS_PARENT_BENCHMARK_V1.json` | part_b_product (shared-Theta joint erasure within check B) | PASS (shared-Theta certificate inside check B) |
| Classical benchmarks | `T8D_WORST_FIBRE_CARDINALITY` | V4 §11 | `—` | no distinct check mechanized; gap for theory lane | NOT_MECHANIZED_NO_DISTINCT_CHECK |
| Joint dynamic | `J1_STATIC_PARTITION_SELECTOR_EQUIVALENCE` | V4 §4 | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | verdicts.R21_ANY_OPTIMAL_MIN_SELECTOR_ENTROPY (identity content) | PASS |
| Joint dynamic | `J2_DYNAMIC_ADMISSIBLE_PARTITION_OPTIMUM` | V4 §5 | `DYNAMIC_RESPONSIBILITY_OPTIMIZATION_V1.json` | fixtures[*].impl_equivalence_direction | PASS (5/5 fixtures, both directions) |
| Joint dynamic | `J3_SELECTOR_REFINEMENT_DYNAMIC_OPTIMUM_EQUIVALENCE` | V4 §6 | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | fixtures[*].j3_expr_equal | PASS (5/5 selectors, exact equality) |
| Joint dynamic | `J4_OPTIONALITY_PREMIUM_NONNEGATIVE` | V4 §7 | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | j4_j5.fixtures[*].omega_dyn.nonnegative | PASS (5/5 omega-rows nonnegative + 1 canonical row(s)) |
| Joint dynamic | `J5_CANONICAL_ONE_BIT_PREMIUM` | V4 §7 canonical fixture | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | j4_j5.fixtures[check==J5].expected==observed | PASS (spec fixture: expected==observed, omega=1 bit) |
| Joint dynamic | `TIE_SENSITIVE_DYNAMIC_SELECTOR_SEARCH` | V4 §7 tie search | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | tie_search.verdict + witness | PASS (smallest witness frozen) |
| Universality | `U1_RESPONSIBILITY_OVERHEAD_BOUND` | V4 §12 | `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json` | verdicts.U1_SANDWICH | PASS |
| Universality | `U2_FIBRE_SEPARATING_SATURATION` | V4 §12 | `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json` | verdicts.U2_SEPARATING | PASS |
| Universality | `U3_UNRESTRICTED_RESPONSIBILITY_FULL_HISTORY` | V4 §12 | `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json` | verdicts.U3_COLLIDED_PAIR_ERROR | PASS |
| Universality | `U4_NONINJECTIVE_FAILING_BINARY_RESPONSIBILITY` | V4 §12 | `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json` | verdicts.U4_FULL_HISTORY_ZERO_ERROR | PASS |
| Universality | `U5_RESPONSIBILITY_FAMILY_MONOTONICITY` | V4 §12 | `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json` | verdicts.U5_NESTED_MONOTONE | PASS |
| V5 state phases | `DS1_P0_PREDICTIVE_DECISIONAL` | V5 | `RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json` | fixtures[P0].verdict | PASS |
| V5 state phases | `DS2_P1_STATIC_CROSS_CHANNEL` | V5 | `RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json` | fixtures[P1].verdict | PASS |
| V5 state phases | `P2_CANONICAL_PROSPECTIVE` | V5 | `RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json` | fixtures[P2].verdict | PASS |
| V5 state phases | `MIXED_P2_WITNESS_SEARCH` | V5 | `RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json` | mixed_p2.verdict | CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS (n=5826 searched) |
| V5 horizon | `PH1_HORIZON_COST_MONOTONICITY` | V5 | `RESPONSIBILITY_HORIZON_CURVE_V1.json` | fixtures[*].ph1_monotone | PASS (6/6 curves monotone) |
| V5 horizon | `PH2_FINITE_HORIZON_STABILIZATION` | V5 | `RESPONSIBILITY_HORIZON_CURVE_V1.json` | fixtures[*].curve[-1]==c_inf + literal_equals_iterative_k | PASS (6/6 stabilize; literal==iterative) |
| V5 horizon | `PH3_RESPONSIBILITY_FAMILY_MONOTONICITY` | V5 | `RESPONSIBILITY_HORIZON_CURVE_V1.json` | ph3.checks | PASS (4/4 family-monotonicity sub-checks) |
| Mutation battery | `M1-M6_PREDICTIVE_COMPRESSION_ASSUMPTIONS` | V4 §9 | `—` | audit running at map-generation time | PENDING_RUN_IN_PROGRESS |

## Known gaps

- T8D_WORST_FIBRE_CARDINALITY: no distinct check mechanized in any receipt to date.
- MIXED_P2_WITNESS_SEARCH: CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS after 5826 machines (spec-mandated preserved negative, not a theorem).
- Section-11 converse holds exactly within the registered per-fibre erasure class only; Q-dependent-erasure counterexample frozen in LOGLOSS_PARENT_BENCHMARK_V1.json part_a_converse.scope_counterexample.
