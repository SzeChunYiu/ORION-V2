# ME-X1 analysis — PROTECTED

Results sha256 `f3065bfee46c6326079a17b55af373fa752c3333c8861c90f894545e9606012f`; custody sha256 `387cec102ff843a9e0c024cb766d7ce763c583f3d1756e58af3aed14aefe223f`; instances 1000.

## Per-arm outcome vector (S7)

| arm | exact | false upd. | missed warr. | over-reopen | under-reopen | inv. transport | false closure | eval. laund. | prob/spec laund. | auth. laund. | correct unres. | warr. recall | unnec. defer | ops | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_DIRECT | 0.384 | 492 | 0 | 0 | 133 | 50 | 180 | 50 | 86 | 50 | 0.00 | 1.000 | 0.000 | 1000 | 0.7 |
| B1_CALIBRATED_ABSTENTION | 0.347 | 55 | 118 | 0 | 133 | 0 | 5 | 0 | 35 | 15 | 0.97 | 0.465 | 0.731 | 2321 | 7.4 |
| B2_PROVENANCE_PLUS_VERIFIER | 0.434 | 362 | 18 | 60 | 45 | 18 | 160 | 34 | 51 | 50 | 0.00 | 0.843 | 0.000 | 1704 | 121.7 |
| B3_PARENT_NATIVE_ASSURANCE | 0.498 | 0 | 12 | 143 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 | 0.816 | 0.000 | 17229 | 129.3 |
| B4_PARENT_MODULES_WITH_SHARED_STATE | 0.837 | 163 | 0 | 0 | 0 | 0 | 62 | 0 | 51 | 50 | 0.66 | 1.000 | 0.000 | 191262 | 321.3 |
| B5_R1_VERDICT_ONLY | 0.971 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 153404 | 367.6 |
| B5_R2_PROV | 0.971 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 200488 | 513.8 |
| B5_R3_PROV+DEP | 0.971 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 191680 | 455.7 |
| B5_R4_PROV+DEP+TRANS+EVAL | 0.971 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 186165 | 422.8 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 193052 | 312.9 |
| M_ME_TRANSITION_CONTROL | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 80650 | 146.1 |
| M_MINUS_PROBLEM_IDENTITY | 0.889 | 111 | 0 | 0 | 0 | 0 | 25 | 0 | 86 | 0 | 0.86 | 1.000 | 0.000 | 76670 | 138.8 |
| M_MINUS_DEPENDENCE | 0.930 | 16 | 0 | 0 | 45 | 0 | 20 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 | 76806 | 119.5 |
| M_MINUS_EVALUATOR_CONTRACT | 0.946 | 54 | 0 | 0 | 0 | 0 | 20 | 34 | 0 | 0 | 0.89 | 1.000 | 0.000 | 79758 | 138.5 |
| M_MINUS_TRANSPORT | 0.930 | 70 | 0 | 0 | 0 | 50 | 20 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 | 79411 | 135.3 |
| M_MINUS_SUPPORT_REOPENING | 0.935 | 0 | 0 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 0.849 | 0.000 | 78096 | 142.3 |
| M_MINUS_AUTHORITY | 0.930 | 70 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 50 | 0.89 | 1.000 | 0.000 | 77872 | 136.4 |
| M_MINUS_UNRESOLVED_TERMINAL | 0.820 | 140 | 0 | 0 | 0 | 0 | 180 | 0 | 0 | 0 | 0.00 | 1.000 | 0.000 | 72139 | 137.3 |
| M_MINUS_MEASUREMENT_COMPARABILITY | 0.930 | 70 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 | 73483 | 137.9 |
| M_MINIMAL_RECEIPT | 0.900 | 100 | 0 | 0 | 0 | 0 | 48 | 0 | 29 | 0 | 0.73 | 1.000 | 0.000 | 54011 | 135.5 |
| C_ALWAYS_UPDATE | 0.370 | 506 | 0 | 0 | 133 | 50 | 180 | 50 | 100 | 50 | 0.00 | 1.000 | 0.000 | 0 | 0.3 |
| C_ALWAYS_DEFER | 0.180 | 0 | 270 | 0 | 133 | 0 | 0 | 0 | 0 | 0 | 1.00 | 0.000 | 1.000 | 0 | 0.2 |
| C_RANDOM_ACTION | 0.097 | 67 | 242 | 208 | 127 | 6 | 46 | 6 | 7 | 1 | 0.08 | 0.103 | 0.199 | 0 | 1.3 |

## Per-family exact-transition rate

| family | B0_DIRECT | B1_CALIBRATED_ABSTENTION | B2_PROVENANCE_PLUS_VERIFIER | B3_PARENT_NATIVE_ASSURANCE | B4_PARENT_MODULES_WITH_SHARED_STATE | B5_R1_VERDICT_ONLY | B5_R2_PROV | B5_R3_PROV+DEP | B5_R4_PROV+DEP+TRANS+EVAL | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | M_ME_TRANSITION_CONTROL | M_MINUS_PROBLEM_IDENTITY | M_MINUS_DEPENDENCE | M_MINUS_EVALUATOR_CONTRACT | M_MINUS_TRANSPORT | M_MINUS_SUPPORT_REOPENING | M_MINUS_AUTHORITY | M_MINUS_UNRESOLVED_TERMINAL | M_MINUS_MEASUREMENT_COMPARABILITY | M_MINIMAL_RECEIPT | C_ALWAYS_UPDATE | C_ALWAYS_DEFER | C_RANDOM_ACTION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| X1-A_CLAIM_PROBLEM_IDENTITY | 0.30 | 0.28 | 0.65 | 0.65 | 0.71 | 0.85 | 0.85 | 0.85 | 0.85 | 1.00 | 1.00 | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 | 0.73 | 0.30 | 0.20 | 0.13 |
| X1-B_MEASUREMENT_CALIBRATION | 0.30 | 0.30 | 0.40 | 0.77 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 0.30 | 0.67 | 0.30 | 0.20 | 0.11 |
| X1-C_HIDDEN_DEPENDENCE | 0.30 | 0.20 | 0.30 | 0.43 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.30 | 1.00 | 1.00 | 0.79 | 1.00 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 | 0.04 |
| X1-D_INVALID_TRANSPORT | 0.30 | 0.45 | 0.29 | 0.30 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.30 | 1.00 | 1.00 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 | 0.09 |
| X1-E_DEFEATED_PREREQUISITE | 0.30 | 0.20 | 0.46 | 0.46 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.66 | 1.00 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 | 0.07 |
| X1-F_EVALUATOR_BLINDNESS | 0.30 | 0.36 | 0.30 | 0.21 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.46 | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 | 0.13 |
| X1-G_AUTHORITY_MISMATCH | 0.30 | 0.36 | 0.30 | 0.30 | 0.30 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.30 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 | 0.11 |
| X1-H_PROOF_WRONG_SPECIFICATION | 0.44 | 0.30 | 0.44 | 0.66 | 0.53 | 0.86 | 0.86 | 0.86 | 0.86 | 1.00 | 1.00 | 0.53 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 | 0.77 | 0.30 | 0.20 | 0.11 |
| X1-I_LOCAL_COMPAT_GLOBAL_OBSTRUCTION | 0.30 | 0.41 | 0.30 | 0.30 | 0.83 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 | 0.83 | 0.30 | 0.20 | 0.09 |
| X1-J_FULLY_WARRANTED | 1.00 | 0.61 | 0.90 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.09 |

## Per-variant exact-transition rate

| variant | B0_DIRECT | B1_CALIBRATED_ABSTENTION | B2_PROVENANCE_PLUS_VERIFIER | B3_PARENT_NATIVE_ASSURANCE | B4_PARENT_MODULES_WITH_SHARED_STATE | B5_R1_VERDICT_ONLY | B5_R2_PROV | B5_R3_PROV+DEP | B5_R4_PROV+DEP+TRANS+EVAL | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | M_ME_TRANSITION_CONTROL | M_MINUS_PROBLEM_IDENTITY | M_MINUS_DEPENDENCE | M_MINUS_EVALUATOR_CONTRACT | M_MINUS_TRANSPORT | M_MINUS_SUPPORT_REOPENING | M_MINUS_AUTHORITY | M_MINUS_UNRESOLVED_TERMINAL | M_MINUS_MEASUREMENT_COMPARABILITY | M_MINIMAL_RECEIPT | C_ALWAYS_UPDATE | C_ALWAYS_DEFER | C_RANDOM_ACTION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| POSITIVE | 0.13 | 0.06 | 0.34 | 0.49 | 0.80 | 0.94 | 0.94 | 0.94 | 0.94 | 1.00 | 1.00 | 0.83 | 0.90 | 0.93 | 0.90 | 0.98 | 0.90 | 1.00 | 0.90 | 0.90 | 0.10 | 0.00 | 0.10 |
| NEGATIVE | 1.00 | 0.40 | 0.81 | 0.77 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.81 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.10 |
| AMBIGUITY | 0.10 | 0.97 | 0.10 | 0.10 | 0.69 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.88 | 0.90 | 0.90 | 0.90 | 1.00 | 0.90 | 0.10 | 0.90 | 0.76 | 0.10 | 0.90 | 0.09 |

## Gates

- **G0a_KNOWN_ANSWER**: pass=True — 14 public development fixtures + separation pair reproduced by the oracle; M and B5 exact on all of them (selftest)
- **G0b_ORACLE_SELF_AGREEMENT**: pass=True — precedence walk / Kleene support == exhaustive enumeration on every instance; every instance valid at v0; family invariants satisfied at generation
- **G0c_NULL_CALIBRATION**: pass=True — C_ALWAYS_UPDATE exact = 0 where the oracle is not UPDATE/PRESERVE; C_ALWAYS_DEFER exact = 0 where the oracle is determinate; C_RANDOM exact <= 20%; M vs permuted oracle decisions (mean over 200 permutations) exact <= 35% (chance = sum of squared action frequencies, reported)
- **G1a_B5_REPRODUCES_M**: pass=True — M and B5 transition decisions identical on >= 99.5% of instances and no family > 5% discordant
- **G1b_M_ADVANTAGE**: pass=False — paired exact-transition difference (M - B5) > 0, exact two-sided p <= 0.05, >= 1 family with >= 5 M-only-exact instances
- **G2_ANTI_CONSERVATISM**: pass=True — M's unnecessary defer/abstain count <= B5's and M's warranted-transition recall >= B5's (warranted = oracle UPDATE/PRESERVE: every NEGATIVE variant and family J)
- **G3_MECHANISM**: pass=None — each family with a claimed M advantage: the matching omission ablation's exact rate on that family <= B5's (A,H->PROBLEM_IDENTITY; B->MEASUREMENT_COMPARABILITY; C->DEPENDENCE; D->TRANSPORT; E->SUPPORT_REOPENING; F->EVALUATOR_CONTRACT; G->AUTHORITY; I,J->UNRESOLVED_TERMINAL)
- **G4_INTERFACE_LADDER**: pass=True — H-EXT-3: no rung k+1 significantly worse than rung k (paired exact p <= 0.05 in the wrong direction is a violation); rung-5 gap = the G1 paired test
- **COST**: pass=None — wall-clock flag at 2x; engine op counts engine-native and reported only; never a route by itself

## Route

`PARENT_SUFFICIENT` — B5 reproduces M's transition decisions. Ladder terminal: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. Cost: `COST_ADVANTAGE_M`.
