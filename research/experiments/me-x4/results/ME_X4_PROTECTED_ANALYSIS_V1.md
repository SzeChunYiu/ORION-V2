# ME-X4 analysis — PROTECTED

Results sha256 `7bd0f8c20c037a2000ffafe2fe1809287b2dbdb0e299125c99b72df554a87117`; custody sha256 `5ac9d3521d557220ef987d69b593c163a8e0863710af4e25b85e680ec856e708`; instances 1200.

## Per-arm outcomes (§5)

| arm | instance exact | final exact | over | under | invalid pres. | false unres. | missed unres. | recovery | engine ops | module ops | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A0_PROVENANCE_ONLY_INVALIDATION | 0.229 | 0.298 | 2398 | 67 | 147 | 0 | 176 | 0.787 (n=239) | 17011 | 0 | 392.3 |
| A1_JTMS_CLASSICAL | 0.766 | 0.766 | 318 | 118 | 198 | 0 | 176 | 1.000 (n=239) | 312248 | 71745 | 548.2 |
| A2_ATMS_CLASSICAL | 0.818 | 0.818 | 318 | 118 | 122 | 0 | 73 | 1.000 (n=239) | 9273 | 71745 | 305.8 |
| A3_AGM_KERNEL_CONTRACTION | 0.763 | 0.763 | 324 | 118 | 198 | 0 | 176 | 1.000 (n=239) | 211959 | 71745 | 144.1 |
| A4_BAYES_NOISY_OR | 0.805 | 0.805 | 334 | 111 | 115 | 3 | 73 | 0.996 (n=239) | 34820 | 71745 | 130.0 |
| A5_ASSURANCE_CASE_UPDATE | 0.237 | 0.306 | 2414 | 44 | 124 | 0 | 176 | 0.787 (n=239) | 14573 | 87646 | 128.8 |
| B5_R1_VERDICT_ONLY | 0.968 | 0.971 | 0 | 43 | 47 | 0 | 4 | 1.000 (n=239) | 238855 | 60211 | 744.3 |
| B5_R2_PROV | 0.993 | 0.993 | 0 | 9 | 10 | 0 | 1 | 1.000 (n=239) | 266982 | 60211 | 805.4 |
| B5_R3_PROV+DEP | 0.993 | 0.993 | 0 | 9 | 10 | 0 | 1 | 1.000 (n=239) | 249738 | 60211 | 725.5 |
| B5_R4_PROV+DEP+TRANS+EVAL | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=239) | 254404 | 60211 | 722.3 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=239) | 323618 | 60211 | 738.5 |
| M_ME_SELECTIVE_REOPENING | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=239) | 114689 | 60211 | 357.0 |
| M_MINUS_DEPENDENCE_ANCESTRY | 0.978 | 0.978 | 0 | 44 | 48 | 0 | 4 | 1.000 (n=239) | 114488 | 56665 | 296.7 |
| M_MINUS_TYPED_TRANSPORT | 0.988 | 0.988 | 25 | 0 | 0 | 0 | 0 | 1.000 (n=239) | 114689 | 60211 | 338.7 |
| M_MINUS_EVALUATOR_CONTRACT | 0.894 | 0.894 | 296 | 2 | 2 | 0 | 69 | 1.000 (n=239) | 112338 | 60211 | 350.4 |
| M_MINUS_SUPPORT_FAMILIES | 0.254 | 0.323 | 2100 | 0 | 0 | 167 | 0 | 0.787 (n=239) | 106744 | 60211 | 349.2 |
| M_GLOBAL_RESET_CONTROL | 0.054 | 0.098 | 6928 | 0 | 0 | 0 | 176 | 0.389 (n=239) | 0 | 60211 | 287.4 |
| M_PROVENANCE_ONLY_CONTROL | 0.229 | 0.298 | 2398 | 67 | 147 | 0 | 176 | 0.787 (n=239) | 17011 | 0 | 371.6 |
| C_NEVER_REOPEN | 0.361 | 0.481 | 0 | 1266 | 1442 | 0 | 176 | 1.000 (n=239) | 0 | 0 | 0.6 |
| C_RANDOM_DISPOSITION | 0.003 | 0.003 | 2598 | 846 | 516 | 2959 | 116 | 0.343 (n=239) | 0 | 0 | 3.9 |

## Per-stratum instance-exact rate

| stratum | A0_PROVENANCE_ONLY_INVALIDATION | A1_JTMS_CLASSICAL | A2_ATMS_CLASSICAL | A3_AGM_KERNEL_CONTRACTION | A4_BAYES_NOISY_OR | A5_ASSURANCE_CASE_UPDATE | B5_R1_VERDICT_ONLY | B5_R2_PROV | B5_R3_PROV+DEP | B5_R4_PROV+DEP+TRANS+EVAL | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | M_ME_SELECTIVE_REOPENING | M_MINUS_DEPENDENCE_ANCESTRY | M_MINUS_TYPED_TRANSPORT | M_MINUS_EVALUATOR_CONTRACT | M_MINUS_SUPPORT_FAMILIES | M_GLOBAL_RESET_CONTROL | M_PROVENANCE_ONLY_CONTROL | C_NEVER_REOPEN | C_RANDOM_DISPOSITION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SOURCE_RETRACTED | 0.00 | 1.00 | 1.00 | 1.00 | 0.98 | 0.00 | 0.97 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| DEPENDENCE_DISCOVERED | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.78 | 1.00 | 1.00 | 0.15 | 0.00 | 0.78 | 0.78 | 0.01 |
| CALIBRATION_INVALIDATED | 0.17 | 1.00 | 1.00 | 1.00 | 0.98 | 0.17 | 0.96 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.17 | 0.00 | 0.17 | 0.33 | 0.00 |
| TRANSPORT_RELATION_INVALIDATED | 0.19 | 0.95 | 0.95 | 0.95 | 0.95 | 0.19 | 0.98 | 0.98 | 0.98 | 1.00 | 1.00 | 1.00 | 1.00 | 0.95 | 1.00 | 0.20 | 0.00 | 0.19 | 0.55 | 0.00 |
| EVALUATOR_BLIND_OR_REPLACED | 0.02 | 0.33 | 0.33 | 0.33 | 0.33 | 0.11 | 0.94 | 0.94 | 0.94 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 0.23 | 0.00 | 0.02 | 0.22 | 0.00 |
| PROBLEM_SCOPE_CHANGED | 0.30 | 0.45 | 0.45 | 0.45 | 0.46 | 0.30 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.30 | 0.00 | 0.30 | 0.45 | 0.00 |
| NEW_INDEPENDENT_SUPPORT | 0.56 | 1.00 | 1.00 | 1.00 | 1.00 | 0.56 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.56 | 0.21 | 0.56 | 0.56 | 0.00 |
| CORRECTION_RESTORES_SUPPORT | 0.22 | 1.00 | 1.00 | 1.00 | 0.99 | 0.22 | 0.97 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.22 | 0.00 | 0.22 | 0.00 | 0.00 |
| PARTIAL_SUPPORT_FAILURE | 0.00 | 1.00 | 1.00 | 1.00 | 0.94 | 0.00 | 0.96 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.44 | 0.01 |
| ALL_SUFFICIENT_SUPPORT_FAILED | 0.17 | 1.00 | 1.00 | 0.97 | 1.00 | 0.17 | 0.87 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.17 | 0.00 | 0.17 | 0.00 | 0.01 |
| CANNOT_CHECK_EDGE | 0.00 | 0.00 | 0.62 | 0.00 | 0.59 | 0.00 | 0.96 | 0.99 | 0.99 | 1.00 | 1.00 | 1.00 | 0.96 | 1.00 | 0.66 | 0.21 | 0.00 | 0.00 | 0.00 | 0.00 |
| NO_REOPENING_NEEDED | 0.34 | 0.68 | 0.68 | 0.68 | 0.66 | 0.34 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.91 | 0.74 | 0.84 | 0.44 | 0.34 | 1.00 | 0.00 |

## Gates

- **G0a_KNOWN_ANSWER**: pass=True — 12 hand-authored fixtures + separation pair reproduced by the oracle (selftest)
- **G0b_ORACLE_SELF_AGREEMENT**: pass=True — Kleene == exhaustive enumeration on every version of every instance
- **G0c_NULL_CALIBRATION**: pass=True — NEVER_REOPEN exact=0 on instances whose oracle reopens/censors something; GLOBAL_RESET exact=0 on instances whose oracle mixes preserved with reopened/unresolved; RANDOM exact <= 10%; M vs within-instance shuffled oracle labels exact <= 10%
- **G1a_B5_REPRODUCES_M**: pass=True — M and B5 decisions identical on >= 99.5% of instances and no stratum > 5% discordant
- **G1b_M_ADVANTAGE**: pass=False — instance-exact diff (M - B5) > 0, exact two-sided p <= 0.05, >= 1 stratum with >= 5 M-only-exact instances
- **G2_ANTI_CONSERVATISM**: pass=True — on NO_REOPENING_NEEDED and NEW_INDEPENDENT_SUPPORT, M over-reopened commitments <= B5's
- **G3_MECHANISM**: pass=None — each stratum with a claimed M advantage: the matching omission ablation's exact rate <= B5's on that stratum
- **G4_INTERFACE_LADDER**: pass=True — no rung k+1 significantly worse than rung k (exact p <= 0.05); rung-5 gap = G1 paired test
- **COST**: pass=None — wall-clock flag at 2x (only commensurable scale; engine op counts are engine-native and reported only); no route by itself (a cost-only claim needs the separate scaling cell)

## Route

`PARENT_SUFFICIENT` — B5 reproduces M's reopening/preservation/unresolved decisions. Ladder terminal: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. Cost: `COST_ADVANTAGE_M`.
