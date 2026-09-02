# ME-X4 analysis — DEVELOPMENT

**DEVELOPMENT split: not protected evidence. Numbers below cannot support any confirmatory claim.**

Results sha256 `aad8d1ac0b3e2ea3e7f2b05b7f0be50586b64e4cb0a5616f77da5cd80fe96f3d`; custody sha256 `7a37fa0be1f73b1ce5d6fd776ca42143a799e43ce78295aded10319b64829c0c`; instances 36.

## Per-arm outcomes (§5)

| arm | instance exact | final exact | over | under | invalid pres. | false unres. | missed unres. | recovery | engine ops | module ops | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A0_PROVENANCE_ONLY_INVALIDATION | 0.167 | 0.250 | 56 | 7 | 10 | 0 | 6 | 1.000 (n=5) | 395 | 0 | 11.8 |
| A1_JTMS_CLASSICAL | 0.833 | 0.833 | 4 | 4 | 7 | 0 | 6 | 1.000 (n=5) | 8584 | 1883 | 15.8 |
| A2_ATMS_CLASSICAL | 0.889 | 0.889 | 4 | 4 | 4 | 0 | 2 | 1.000 (n=5) | 251 | 1883 | 8.2 |
| A3_AGM_KERNEL_CONTRACTION | 0.833 | 0.833 | 4 | 4 | 7 | 0 | 6 | 1.000 (n=5) | 5555 | 1883 | 4.1 |
| A4_BAYES_NOISY_OR | 0.861 | 0.861 | 5 | 4 | 4 | 0 | 2 | 1.000 (n=5) | 892 | 1883 | 3.8 |
| A5_ASSURANCE_CASE_UPDATE | 0.167 | 0.250 | 59 | 4 | 7 | 0 | 6 | 1.000 (n=5) | 358 | 2294 | 3.9 |
| B5_R1_VERDICT_ONLY | 0.972 | 0.972 | 0 | 1 | 1 | 0 | 0 | 1.000 (n=5) | 6655 | 1586 | 23.6 |
| B5_R2_PROV | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=5) | 7425 | 1586 | 25.1 |
| B5_R3_PROV+DEP | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=5) | 6969 | 1586 | 20.8 |
| B5_R4_PROV+DEP+TRANS+EVAL | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=5) | 7190 | 1586 | 21.3 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=5) | 8915 | 1586 | 21.1 |
| M_ME_SELECTIVE_REOPENING | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=5) | 3021 | 1586 | 10.0 |
| M_MINUS_DEPENDENCE_ANCESTRY | 0.944 | 0.944 | 0 | 4 | 4 | 0 | 0 | 1.000 (n=5) | 3021 | 1486 | 8.1 |
| M_MINUS_TYPED_TRANSPORT | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 (n=5) | 3021 | 1586 | 9.6 |
| M_MINUS_EVALUATOR_CONTRACT | 0.944 | 0.944 | 4 | 0 | 0 | 0 | 2 | 1.000 (n=5) | 2926 | 1586 | 10.7 |
| M_MINUS_SUPPORT_FAMILIES | 0.333 | 0.417 | 49 | 0 | 0 | 5 | 0 | 1.000 (n=5) | 2830 | 1586 | 10.4 |
| M_GLOBAL_RESET_CONTROL | 0.083 | 0.139 | 174 | 0 | 0 | 0 | 6 | 0.800 (n=5) | 0 | 1586 | 8.4 |
| M_PROVENANCE_ONLY_CONTROL | 0.167 | 0.250 | 56 | 7 | 10 | 0 | 6 | 1.000 (n=5) | 395 | 0 | 10.1 |
| C_NEVER_REOPEN | 0.361 | 0.444 | 0 | 31 | 37 | 0 | 6 | 1.000 (n=5) | 0 | 0 | 0.0 |
| C_RANDOM_DISPOSITION | 0.000 | 0.000 | 60 | 23 | 12 | 89 | 4 | 0.000 (n=5) | 0 | 0 | 0.2 |

## Per-stratum instance-exact rate

| stratum | A0_PROVENANCE_ONLY_INVALIDATION | A1_JTMS_CLASSICAL | A2_ATMS_CLASSICAL | A3_AGM_KERNEL_CONTRACTION | A4_BAYES_NOISY_OR | A5_ASSURANCE_CASE_UPDATE | B5_R1_VERDICT_ONLY | B5_R2_PROV | B5_R3_PROV+DEP | B5_R4_PROV+DEP+TRANS+EVAL | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | M_ME_SELECTIVE_REOPENING | M_MINUS_DEPENDENCE_ANCESTRY | M_MINUS_TYPED_TRANSPORT | M_MINUS_EVALUATOR_CONTRACT | M_MINUS_SUPPORT_FAMILIES | M_GLOBAL_RESET_CONTROL | M_PROVENANCE_ONLY_CONTROL | C_NEVER_REOPEN | C_RANDOM_DISPOSITION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SOURCE_RETRACTED | 0.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| DEPENDENCE_DISCOVERED | 0.33 | 0.33 | 0.33 | 0.33 | 0.33 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 1.00 | 1.00 | 0.67 | 0.00 | 0.33 | 0.33 | 0.00 |
| CALIBRATION_INVALIDATED | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.00 | 0.67 | 0.00 | 0.00 |
| TRANSPORT_RELATION_INVALIDATED | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.67 | 0.00 |
| EVALUATOR_BLIND_OR_REPLACED | 0.00 | 0.67 | 0.67 | 0.67 | 0.67 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.33 | 0.00 | 0.00 | 0.00 | 0.00 |
| PROBLEM_SCOPE_CHANGED | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| NEW_INDEPENDENT_SUPPORT | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| CORRECTION_RESTORES_SUPPORT | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| PARTIAL_SUPPORT_FAILURE | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.33 | 0.00 |
| ALL_SUFFICIENT_SUPPORT_FAILED | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| CANNOT_CHECK_EDGE | 0.00 | 0.00 | 0.67 | 0.00 | 0.67 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.33 | 0.00 | 0.00 | 0.00 | 0.00 |
| NO_REOPENING_NEEDED | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |

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
