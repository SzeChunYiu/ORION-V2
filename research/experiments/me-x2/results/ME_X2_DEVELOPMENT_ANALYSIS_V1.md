# ME-X2 analysis — DEVELOPMENT

**DEVELOPMENT split: not protected evidence. Numbers below cannot support any confirmatory claim.**

Results sha256 `fb6c55e058a857ad37f3972fb0cc2d0f34bf3d3cf45349f197f400aed281a520`; custody sha256 `451eb5b4d997bd550585c52df9c66c34e9238e82dc724524a811bb786100b3eb`; instances 48.

## Per-arm outcomes (S5)

| arm | decision (min-level) | class | locus | success | false esc. | missed esc. | false CI | correct CI | recur. | spec dmg | false world | mean regret | mean cost | Brier | ECE5 | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_RETRY_SEARCH | 0.188 | 0.146 | 0.250 | 0.188 | 1 | 32 | 0 | 0/7 | 117 | 0 | 0 | -2.341 | 5.583 | n/a | n/a | 0.4 |
| B1_UNCERTAINTY_ABSTENTION | 0.729 | 0.875 | 0.875 | 0.583 | 0 | 13 | 13 | 7/7 | 0 | 0 | 0 | 3.537 | 10.896 | 0.146 | 0.146 | 1.5 |
| B2_FAILURE_TAXONOMY_DIAGNOSIS | 0.250 | 0.500 | 0.562 | 0.479 | 25 | 19 | 0 | 0/7 | 80 | 1 | 1 | 3.732 | 11.896 | n/a | n/a | 0.7 |
| B3_MODEL_BASED_DIAGNOSIS_VOI | 0.812 | 0.812 | 0.812 | 0.854 | 5 | 2 | 0 | 0/7 | 8 | 0 | 2 | 3.268 | 11.188 | 0.152 | 0.152 | 2.8 |
| B3_EQUAL_EXTRA_SEARCH_1_5X | 0.854 | 0.854 | 0.854 | 0.938 | 5 | 0 | 0 | 0/7 | 5 | 0 | 1 | 4.415 | 12.979 | 0.109 | 0.109 | 2.9 |
| B4_MDA_MODEL_EXPANSION | 0.750 | 0.771 | 0.771 | 0.812 | 8 | 4 | 0 | 0/7 | 11 | 0 | 2 | 3.707 | 11.562 | 0.168 | 0.163 | 2.4 |
| B5_R1_VERDICT_ONLY | 0.688 | 0.688 | 0.688 | 0.708 | 5 | 8 | 0 | 0/7 | 6 | 0 | 2 | 2.244 | 9.833 | n/a | n/a | 1.0 |
| B5_R2_PLUS_CANDIDATE_SET | 0.875 | 0.917 | 0.917 | 0.729 | 0 | 6 | 6 | 7/7 | 3 | 0 | 0 | 2.244 | 9.312 | 0.167 | 0.167 | 0.9 |
| B5_R3_PLUS_DISCRIMINATOR_TABLES | 0.979 | 0.958 | 0.958 | 0.833 | 0 | 1 | 1 | 7/7 | 29 | 0 | 0 | 3.146 | 9.938 | 0.167 | 0.167 | 14.4 |
| B5_R4_PLUS_DISPOSITION_RECORDS | 0.979 | 0.958 | 0.958 | 0.833 | 0 | 1 | 0 | 7/7 | 32 | 0 | 0 | 3.146 | 9.938 | 0.167 | 0.167 | 11.9 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 1.000 | 0.979 | 0.979 | 0.854 | 0 | 0 | 0 | 7/7 | 31 | 0 | 0 | 3.098 | 9.896 | 0.146 | 0.146 | 11.3 |
| B5_NO_ABSTENTION_GATE | 0.875 | 0.875 | 0.875 | 0.896 | 6 | 0 | 0 | 5/7 | 36 | 0 | 1 | 2.976 | 10.938 | 0.146 | 0.146 | 29.9 |
| M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | 1.000 | 0.938 | 0.938 | 0.854 | 0 | 0 | 0 | 7/7 | 16 | 0 | 0 | 3.488 | 10.417 | 0.146 | 0.146 | 34.5 |
| M_MINUS_LOCUS_DIAGNOSIS | 0.583 | 0.625 | 0.583 | 0.438 | 0 | 20 | 20 | 7/7 | 46 | 0 | 0 | -4.244 | 3.188 | 0.146 | 0.146 | 10.1 |
| M_LOCUS_LABELS_SHUFFLED | 0.250 | 0.146 | 0.250 | 0.125 | 3 | 35 | 9 | 6/7 | 29 | 0 | 0 | -1.293 | 5.958 | 0.818 | 0.818 | 78.2 |
| M_MINUS_DIAGNOSTIC_EVALUATOR_GATE | 0.917 | 0.854 | 0.854 | 0.896 | 4 | 0 | 0 | 5/7 | 19 | 0 | 1 | 3.488 | 11.292 | 0.146 | 0.146 | 36.3 |
| M_MINUS_LOWER_LEVEL_DISPOSITION | 0.917 | 0.854 | 0.854 | 0.896 | 4 | 0 | 0 | 5/7 | 7 | 0 | 1 | 4.171 | 11.854 | 0.146 | 0.146 | 26.0 |
| M_MINUS_PROSPECTIVE_DISCRIMINATOR | 0.938 | 0.875 | 0.875 | 0.792 | 0 | 3 | 3 | 7/7 | 4 | 0 | 0 | 5.463 | 12.333 | 0.146 | 0.146 | 39.0 |
| M_ALWAYS_ESCALATE_WHEN_STUCK | 0.271 | 0.604 | 0.625 | 0.625 | 34 | 16 | 16 | 2/7 | 46 | 5 | 0 | 7.024 | 15.417 | 0.146 | 0.146 | 27.2 |
| M_NEVER_ESCALATE | 0.646 | 0.938 | 0.938 | 0.500 | 0 | 17 | 17 | 7/7 | 16 | 0 | 0 | -2.707 | 5.125 | 0.146 | 0.146 | 32.9 |
| C_RANDOM_POLICY | 0.208 | 0.104 | 0.104 | 0.333 | 17 | 27 | 13 | 4/7 | 29 | 3 | 3 | 1.268 | 9.417 | 0.378 | 0.470 | 1.9 |
| C_NEVER_INTERVENE | 0.146 | 0.146 | 0.146 | 0.000 | 0 | 41 | 41 | 7/7 | 0 | 0 | 0 | -7.634 | 0.000 | 0.146 | 0.146 | 0.1 |

## Per-stratum decision-correct rate (stratum = oracle class)

| stratum | n | B0_RETRY_SEARCH | B1_UNCERTAINTY_ABSTENTION | B2_FAILURE_TAXONOMY_DIAGNOSIS | B3_MODEL_BASED_DIAGNOSIS_VOI | B3_EQUAL_EXTRA_SEARCH_1_5X | B4_MDA_MODEL_EXPANSION | B5_R1_VERDICT_ONLY | B5_R2_PLUS_CANDIDATE_SET | B5_R3_PLUS_DISCRIMINATOR_TABLES | B5_R4_PLUS_DISPOSITION_RECORDS | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | B5_NO_ABSTENTION_GATE | M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | M_MINUS_LOCUS_DIAGNOSIS | M_LOCUS_LABELS_SHUFFLED | M_MINUS_DIAGNOSTIC_EVALUATOR_GATE | M_MINUS_LOWER_LEVEL_DISPOSITION | M_MINUS_PROSPECTIVE_DISCRIMINATOR | M_ALWAYS_ESCALATE_WHEN_STUCK | M_NEVER_ESCALATE | C_RANDOM_POLICY | C_NEVER_INTERVENE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SEARCH_INSUFFICIENT | 7 | 0.71 | 0.86 | 0.14 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 0.71 | 0.00 | 1.00 | 0.14 | 0.00 |
| MISSING_PREMISE_OR_DATA | 4 | 0.25 | 0.25 | 0.50 | 1.00 | 1.00 | 1.00 | 0.50 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| MODEL_FAMILY_INADEQUATE | 2 | 0.00 | 1.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 0.50 | 0.00 |
| REPRESENTATION_INSUFFICIENT | 2 | 0.00 | 0.00 | 1.00 | 0.50 | 1.00 | 0.50 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 0.00 | 0.00 |
| PROBE_ACTION_INSUFFICIENT | 3 | 0.00 | 1.00 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.00 | 1.00 | 1.00 | 0.67 | 0.00 | 1.00 | 0.00 | 0.00 |
| MEASUREMENT_OR_EVALUATOR_BLIND | 2 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 | 0.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.50 | 0.00 |
| FORMALISM_OR_OPERATOR_INSUFFICIENT | 4 | 0.25 | 1.00 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.25 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 0.25 | 0.00 |
| PROBLEM_OBJECTIVE_MISSPECIFIED | 3 | 0.00 | 0.33 | 0.00 | 0.67 | 1.00 | 0.67 | 0.67 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.00 | 0.00 | 0.00 |
| TOOL_INSTRUMENT_INADEQUATE | 2 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.50 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 0.50 | 0.00 |
| WORKFLOW_INADEQUATE | 2 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| NO_ESCALATION_NEEDED | 10 | 0.20 | 0.90 | 0.20 | 1.00 | 1.00 | 0.70 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.60 | 0.20 | 1.00 | 1.00 | 1.00 | 0.20 | 1.00 | 0.40 | 0.00 |
| CANNOT_IDENTIFY | 7 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.14 | 1.00 | 1.00 | 0.86 | 0.43 | 0.43 | 1.00 | 0.00 | 1.00 | 0.14 | 1.00 |

## Per-variant decision-correct rate

| variant | n | B0_RETRY_SEARCH | B1_UNCERTAINTY_ABSTENTION | B2_FAILURE_TAXONOMY_DIAGNOSIS | B3_MODEL_BASED_DIAGNOSIS_VOI | B3_EQUAL_EXTRA_SEARCH_1_5X | B4_MDA_MODEL_EXPANSION | B5_R1_VERDICT_ONLY | B5_R2_PLUS_CANDIDATE_SET | B5_R3_PLUS_DISCRIMINATOR_TABLES | B5_R4_PLUS_DISPOSITION_RECORDS | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | B5_NO_ABSTENTION_GATE | M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | M_MINUS_LOCUS_DIAGNOSIS | M_LOCUS_LABELS_SHUFFLED | M_MINUS_DIAGNOSTIC_EVALUATOR_GATE | M_MINUS_LOWER_LEVEL_DISPOSITION | M_MINUS_PROSPECTIVE_DISCRIMINATOR | M_ALWAYS_ESCALATE_WHEN_STUCK | M_NEVER_ESCALATE | C_RANDOM_POLICY | C_NEVER_INTERVENE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CI | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.50 | 1.00 |
| PARTNER_OF_CI | 2 | 0.00 | 0.50 | 0.00 | 0.00 | 0.50 | 0.00 | 0.00 | 0.50 | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 | 0.50 | 0.50 | 0.50 | 0.50 | 1.00 | 0.00 | 0.50 | 0.00 | 0.50 |
| PARTNER_OF_PLAIN | 22 | 0.27 | 0.91 | 0.23 | 0.82 | 0.82 | 0.73 | 0.73 | 1.00 | 1.00 | 1.00 | 1.00 | 0.86 | 1.00 | 0.77 | 0.27 | 0.95 | 0.95 | 0.91 | 0.09 | 0.91 | 0.18 | 0.18 |
| PLAIN | 22 | 0.14 | 0.55 | 0.32 | 0.95 | 1.00 | 0.91 | 0.77 | 0.77 | 0.95 | 0.95 | 1.00 | 1.00 | 1.00 | 0.36 | 0.14 | 1.00 | 1.00 | 0.95 | 0.50 | 0.36 | 0.23 | 0.00 |

## Gates

- **G0a_KNOWN_ANSWER**: pass=True — 14 hand-authored fixtures (oracle targets; M and B5 decision-correct) + separation pair reproduced in selftest
- **G0b_ORACLE_SELF_AGREEMENT**: pass=True — enumeration == branch-and-bound and a truth-agnostic decision-correct policy exists on every instance; variant invariants hold; >= min decoys per apparent class (typical level >= 1) and >= min inverse decoys per level-0 class and apparent-CANNOT_IDENTIFY
- **G0c_NULL_CALIBRATION**: pass=True — NEVER_INTERVENE decision-correct = 0 on identifiable instances; RANDOM <= 0.25; M scored against the partner's oracle <= M's true rate - 0.30
- **G1a_B5_REPRODUCES_M**: pass=False — intervention/declaration sequences identical on >= 99.5% of instances and no stratum > 5% discordant
- **G1b_M_ADVANTAGE**: pass=False — minimal-level decision-correct diff (M - B5) > 0, exact two-sided p <= 0.05, >= 1 stratum with >= 5 M-only-correct
- **G1c_B5_ADVANTAGE**: pass=False — symmetric: diff < 0 with p <= 0.05 (B5 dominates)
- **G2_ANTI_ESCALATION**: pass=True — M false escalations <= B5's and M specification damage <= B5's
- **G3_MEDIATION**: pass=None — (a) M's class correct on >= 80% of M-only-correct instances; (b) on each advantaged stratum both locus ablations <= B5; (c) B3 with 1.5x budget does not reach M (paired p <= 0.05)
- **G4_INTERFACE_LADDER**: pass=True — no rung k+1 significantly worse than rung k (exact p <= 0.05); rung-5 gap = G1 paired test
- **COST**: pass=None — paired sign test on per-instance regret (registered cost units) at p <= 0.05; wall-clock reported only

## Route

`PARENT_SUFFICIENT` — no M advantage over B5 (discordance without significance). Ladder terminal: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. Cost: `COST_PARITY`.
