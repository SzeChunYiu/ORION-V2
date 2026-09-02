# ME-X1 analysis — DEVELOPMENT

**DEVELOPMENT split: not protected evidence. Numbers below cannot support any confirmatory claim.**

Results sha256 `634f33941bd59d15089bbd8b06452c4473f2b4728fe024409eab6aa9b833ac15`; custody sha256 `ff9dd17424de0a8ece8d763ac7a452662ab5a7d21c5a583ffaeb8060910ee248`; instances 40.

## Per-arm outcome vector (S7)

| arm | exact | false upd. | missed warr. | over-reopen | under-reopen | inv. transport | false closure | eval. laund. | prob/spec laund. | auth. laund. | correct unres. | warr. recall | unnec. defer | ops | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_DIRECT | 0.325 | 22 | 0 | 0 | 5 | 2 | 9 | 2 | 4 | 2 | 0.00 | 1.000 | 0.000 | 40 | 0.0 |
| B1_CALIBRATED_ABSTENTION | 0.375 | 3 | 4 | 0 | 5 | 0 | 1 | 0 | 2 | 0 | 0.89 | 0.538 | 0.690 | 93 | 0.4 |
| B2_PROVENANCE_PLUS_VERIFIER | 0.425 | 16 | 0 | 2 | 1 | 1 | 8 | 2 | 2 | 2 | 0.00 | 0.923 | 0.000 | 63 | 5.5 |
| B3_PARENT_NATIVE_ASSURANCE | 0.500 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 | 0.923 | 0.000 | 696 | 6.3 |
| B4_PARENT_MODULES_WITH_SHARED_STATE | 0.825 | 7 | 0 | 0 | 0 | 0 | 3 | 0 | 2 | 2 | 0.67 | 1.000 | 0.000 | 8215 | 15.6 |
| B5_R1_VERDICT_ONLY | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 6495 | 17.8 |
| B5_R2_PROV | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 8466 | 24.5 |
| B5_R3_PROV+DEP | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 8096 | 20.9 |
| B5_R4_PROV+DEP+TRANS+EVAL | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 7860 | 19.0 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 8288 | 15.0 |
| M_ME_TRANSITION_CONTROL | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 3436 | 7.4 |
| M_MINUS_PROBLEM_IDENTITY | 0.850 | 6 | 0 | 0 | 0 | 0 | 2 | 0 | 4 | 0 | 0.78 | 1.000 | 0.000 | 3183 | 6.7 |
| M_MINUS_DEPENDENCE | 0.925 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 | 3307 | 5.5 |
| M_MINUS_EVALUATOR_CONTRACT | 0.925 | 3 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0.89 | 1.000 | 0.000 | 3403 | 6.0 |
| M_MINUS_TRANSPORT | 0.925 | 3 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 | 3379 | 6.0 |
| M_MINUS_SUPPORT_REOPENING | 0.950 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 0.923 | 0.000 | 3326 | 6.9 |
| M_MINUS_AUTHORITY | 0.925 | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0.89 | 1.000 | 0.000 | 3292 | 7.1 |
| M_MINUS_UNRESOLVED_TERMINAL | 0.775 | 7 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0.00 | 1.000 | 0.000 | 2994 | 6.9 |
| M_MINUS_MEASUREMENT_COMPARABILITY | 0.925 | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 | 3126 | 6.7 |
| M_MINIMAL_RECEIPT | 1.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 | 2289 | 6.2 |
| C_ALWAYS_UPDATE | 0.325 | 22 | 0 | 0 | 5 | 2 | 9 | 2 | 4 | 2 | 0.00 | 1.000 | 0.000 | 0 | 0.0 |
| C_ALWAYS_DEFER | 0.225 | 0 | 10 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 1.00 | 0.000 | 1.000 | 0 | 0.0 |
| C_RANDOM_ACTION | 0.100 | 1 | 9 | 15 | 5 | 0 | 1 | 0 | 0 | 0 | 0.22 | 0.077 | 0.207 | 0 | 0.1 |

## Per-family exact-transition rate

| family | B0_DIRECT | B1_CALIBRATED_ABSTENTION | B2_PROVENANCE_PLUS_VERIFIER | B3_PARENT_NATIVE_ASSURANCE | B4_PARENT_MODULES_WITH_SHARED_STATE | B5_R1_VERDICT_ONLY | B5_R2_PROV | B5_R3_PROV+DEP | B5_R4_PROV+DEP+TRANS+EVAL | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | M_ME_TRANSITION_CONTROL | M_MINUS_PROBLEM_IDENTITY | M_MINUS_DEPENDENCE | M_MINUS_EVALUATOR_CONTRACT | M_MINUS_TRANSPORT | M_MINUS_SUPPORT_REOPENING | M_MINUS_AUTHORITY | M_MINUS_UNRESOLVED_TERMINAL | M_MINUS_MEASUREMENT_COMPARABILITY | M_MINIMAL_RECEIPT | C_ALWAYS_UPDATE | C_ALWAYS_DEFER | C_RANDOM_ACTION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| X1-A_CLAIM_PROBLEM_IDENTITY | 0.25 | 0.25 | 0.75 | 0.75 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 1.00 | 1.00 | 0.25 | 0.25 | 0.25 |
| X1-B_MEASUREMENT_CALIBRATION | 0.25 | 0.50 | 0.75 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 0.25 | 1.00 | 0.25 | 0.25 | 0.25 |
| X1-C_HIDDEN_DEPENDENCE | 0.25 | 0.25 | 0.25 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 1.00 | 1.00 | 0.25 | 0.25 | 0.00 |
| X1-D_INVALID_TRANSPORT | 0.25 | 0.50 | 0.25 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | 1.00 | 1.00 | 0.75 | 1.00 | 1.00 | 0.25 | 0.25 | 0.00 |
| X1-E_DEFEATED_PREREQUISITE | 0.25 | 0.25 | 0.25 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 | 0.75 | 1.00 | 1.00 | 0.25 | 0.25 | 0.25 |
| X1-F_EVALUATOR_BLINDNESS | 0.25 | 0.25 | 0.25 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | 1.00 | 1.00 | 1.00 | 0.75 | 1.00 | 1.00 | 0.25 | 0.25 | 0.00 |
| X1-G_AUTHORITY_MISMATCH | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | 0.75 | 1.00 | 1.00 | 0.25 | 0.25 | 0.00 |
| X1-H_PROOF_WRONG_SPECIFICATION | 0.25 | 0.25 | 0.25 | 0.75 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 1.00 | 1.00 | 0.25 | 0.25 | 0.25 |
| X1-I_LOCAL_COMPAT_GLOBAL_OBSTRUCTION | 0.25 | 0.50 | 0.25 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 1.00 | 1.00 | 0.25 | 0.25 | 0.00 |
| X1-J_FULLY_WARRANTED | 1.00 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 |

## Per-variant exact-transition rate

| variant | B0_DIRECT | B1_CALIBRATED_ABSTENTION | B2_PROVENANCE_PLUS_VERIFIER | B3_PARENT_NATIVE_ASSURANCE | B4_PARENT_MODULES_WITH_SHARED_STATE | B5_R1_VERDICT_ONLY | B5_R2_PROV | B5_R3_PROV+DEP | B5_R4_PROV+DEP+TRANS+EVAL | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | M_ME_TRANSITION_CONTROL | M_MINUS_PROBLEM_IDENTITY | M_MINUS_DEPENDENCE | M_MINUS_EVALUATOR_CONTRACT | M_MINUS_TRANSPORT | M_MINUS_SUPPORT_REOPENING | M_MINUS_AUTHORITY | M_MINUS_UNRESOLVED_TERMINAL | M_MINUS_MEASUREMENT_COMPARABILITY | M_MINIMAL_RECEIPT | C_ALWAYS_UPDATE | C_ALWAYS_DEFER | C_RANDOM_ACTION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| POSITIVE | 0.10 | 0.05 | 0.35 | 0.50 | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 0.90 | 0.90 | 0.90 | 0.95 | 0.90 | 1.00 | 0.90 | 1.00 | 0.10 | 0.00 | 0.05 |
| NEGATIVE | 1.00 | 0.50 | 0.90 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.10 |
| AMBIGUITY | 0.10 | 0.90 | 0.10 | 0.10 | 0.70 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 0.90 | 0.90 | 0.90 | 1.00 | 0.90 | 0.10 | 0.90 | 1.00 | 0.10 | 0.90 | 0.20 |

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
