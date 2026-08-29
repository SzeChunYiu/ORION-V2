# CLAIM_RECEIPT_CROSSCHECK_V1 — ledger claims vs mechanical receipts

Every MECHANICALLY_VERIFIED row was re-validated against its receipt JSON at
generation time by `llm_epistemics_claim_crosscheck.py`. Ledger status drift
between this script's snapshot and CLAIM_LEDGER_V4.json fails the run.

| Claim | Ledger status | Cross-check | Receipt | Evidence |
|---|---|---|---|---|
| C01 | `PARENT_OWNED` | **CONSISTENT_PARENT_OWNED** | `PARTITION_ENUMERATION_RECEIPT_V1.json` | L1/T2 mechanics instantiate S_P (predictive partition) exhaustively n<=7 |
| C02 | `PARENT_OWNED_PATTERN` | **CONSISTENT_PARENT_OWNED** | `RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json` | P1 fixture instantiates prediction-state-misses-secondary-target pattern |
| C03 | `PARENT_OWNED_GENERIC_FORM` | **CONSISTENT_PARENT_OWNED** | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | R22-R24 instantiate decision-state cost forms exactly |
| C04 | `CANDIDATE_CROSS_CHANNEL_STATIC_COST` | **MECHANICALLY_VERIFIED** | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | P1_STATIC_CROSS_CHANNEL witness: C_stat^*=1 bit > 0 |
| C05 | `MANDATORY_ZERO_COST_CONTROL` | **MECHANICALLY_VERIFIED** | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | R27 PASS (selector receipt) + P0 fixture C_stat^*=0 |
| C06 | `CANDIDATE_CROSS_CHANNEL_OBSTRUCTION` | **MECHANICALLY_VERIFIED** | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | R21 equivalence: zero cost iff common-optimal-action refinement exists |
| C07 | `PARENT_OWNED_OR_COROLLARY` | **CONSISTENT_PARENT_OWNED** | `PARTITION_ENUMERATION_RECEIPT_V1.json` | T2/T2b iso corollary checked exactly over Bell-complete n<=7 |
| C08 | `CANDIDATE_STATIC_OPTIMIZATION_FORMULATION` | **MECHANICALLY_VERIFIED** | `RESPONSIBILITY_SELECTOR_AUDIT_V1.json` | R21+R22+R23 PASS (min-entropy action-compatible partition + selector equality) |
| C09 | `CANDIDATE_DYNAMIC_OPTIMIZATION_FORMULATION` | **MECHANICALLY_VERIFIED** | `DYNAMIC_RESPONSIBILITY_OPTIMIZATION_V1.json` | J2: 5/5 fixtures, both implementation directions PASS |
| C10 | `CANDIDATE_SELECTOR_EQUIVALENCE` | **MECHANICALLY_VERIFIED** | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | J3: 5/5 selectors, j3_expr_equal exact |
| C11 | `PRIMARY_CANDIDATE_QUANTITY` | **MECHANICALLY_VERIFIED** | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | J4: all omega rows nonnegative + canonical row + tie-search witness |
| C12 | `KNOWN_ANSWER_WITNESS` | **MECHANICALLY_VERIFIED** | `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json` | J5 canonical fixture expected==observed (0,1,1) bits |
| C13 | `CANDIDATE_PHASE_FRAMEWORK` | **MECHANICALLY_VERIFIED** | `RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json` | P0/P1/P2 fixtures all PASS |
| C14 | `CANDIDATE_HORIZON_CURVE` | **MECHANICALLY_VERIFIED** | `RESPONSIBILITY_HORIZON_CURVE_V1.json` | PH1 6/6 monotone + PH2 stabilization with literal==iterative |
| C15 | `PARENT_OWNED_IDENTITY` | **CONSISTENT_PARENT_OWNED** | `EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json` | D1/D2/D3 + controls PASS (identity instantiated exactly, parent owns it) |
| C16 | `PARENT_OWNED_BENCHMARK` | **CONSISTENT_PARENT_OWNED** | `LOGLOSS_PARENT_BENCHMARK_V1.json` | T8A/T8B/T8C reproduced exactly within registered class (scope note in receipt) |
| C17 | `CANDIDATE_BOUNDARY_LIKELY_CLASSICAL` | **MECHANICALLY_VERIFIED** | `RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json` | U1-U5 PASS |
| C18 | `CANDIDATE_LLM_EVALUATION_CONSEQUENCE` | **NOT_MECHANICALLY_BACKED** | `—` | no empirical/LLM-lane check exists in the receipt corpus (spec forbids empirical LLM claims) |

**JMLR load-bearing claims (C11, C13, C14, C18):** C11=MECHANICALLY_VERIFIED, C13=MECHANICALLY_VERIFIED, C14=MECHANICALLY_VERIFIED, C18=NOT_MECHANICALLY_BACKED

OVERALL PASS
