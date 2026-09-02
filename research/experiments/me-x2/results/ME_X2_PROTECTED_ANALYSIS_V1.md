# ME-X2 analysis — PROTECTED

Results sha256 `33961a3df74711d9e3bd080a141bcab4b436005600aca74d28ebfe86e5260cd9`; custody sha256 `19f4656232a38c893a72c0cd4808660521dd17363e872a2143f2fb78c3834919`; instances 1200.

## Per-arm outcomes (S5)

| arm | decision (min-level) | class | locus | success | false esc. | missed esc. | false CI | correct CI | recur. | spec dmg | false world | mean regret | mean cost | Brier | ECE5 | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_RETRY_SEARCH | 0.218 | 0.102 | 0.312 | 0.223 | 15 | 798 | 0 | 0/140 | 2766 | 0 | 0 | -3.345 | 4.721 | n/a | n/a | 10.8 |
| B1_UNCERTAINTY_ABSTENTION | 0.593 | 0.752 | 0.800 | 0.478 | 1 | 487 | 487 | 139/140 | 0 | 0 | 9 | 2.105 | 9.858 | 0.117 | 0.117 | 44.0 |
| B2_FAILURE_TAXONOMY_DIAGNOSIS | 0.356 | 0.476 | 0.468 | 0.606 | 517 | 389 | 0 | 0/140 | 1670 | 18 | 63 | 3.593 | 11.658 | n/a | n/a | 17.2 |
| B3_MODEL_BASED_DIAGNOSIS_VOI | 0.777 | 0.789 | 0.792 | 0.830 | 116 | 107 | 5 | 20/140 | 257 | 5 | 34 | 2.978 | 10.836 | 0.127 | 0.117 | 76.9 |
| B3_EQUAL_EXTRA_SEARCH_1_5X | 0.854 | 0.857 | 0.857 | 0.969 | 163 | 1 | 0 | 1/140 | 228 | 8 | 35 | 4.471 | 12.999 | 0.117 | 0.106 | 83.4 |
| B4_MDA_MODEL_EXPANSION | 0.772 | 0.794 | 0.792 | 0.828 | 128 | 112 | 5 | 19/140 | 271 | 6 | 19 | 2.992 | 10.857 | 0.127 | 0.113 | 65.7 |
| B5_R1_VERDICT_ONLY | 0.690 | 0.693 | 0.694 | 0.719 | 93 | 229 | 0 | 0/140 | 207 | 7 | 29 | 2.043 | 9.783 | n/a | n/a | 26.1 |
| B5_R2_PLUS_CANDIDATE_SET | 0.800 | 0.838 | 0.855 | 0.702 | 18 | 223 | 223 | 135/140 | 245 | 4 | 10 | 1.590 | 9.104 | 0.141 | 0.138 | 28.0 |
| B5_R3_PLUS_DISCRIMINATOR_TABLES | 0.858 | 0.848 | 0.868 | 0.762 | 20 | 151 | 151 | 134/140 | 852 | 3 | 14 | 1.731 | 9.158 | 0.136 | 0.132 | 712.9 |
| B5_R4_PLUS_DISPOSITION_RECORDS | 0.945 | 0.911 | 0.891 | 0.867 | 37 | 31 | 4 | 121/140 | 884 | 13 | 28 | 3.155 | 10.487 | 0.142 | 0.137 | 583.9 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 0.983 | 0.949 | 0.932 | 0.887 | 21 | 0 | 0 | 135/140 | 829 | 0 | 28 | 3.474 | 10.607 | 0.121 | 0.115 | 563.6 |
| B5_NO_ABSTENTION_GATE | 0.897 | 0.887 | 0.873 | 0.922 | 123 | 3 | 3 | 91/140 | 884 | 6 | 32 | 3.328 | 11.214 | 0.118 | 0.110 | 1762.9 |
| M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | 0.963 | 0.923 | 0.902 | 0.846 | 0 | 45 | 45 | 140/140 | 470 | 0 | 20 | 3.054 | 10.265 | 0.117 | 0.117 | 1155.6 |
| M_MINUS_LOCUS_DIAGNOSIS | 0.483 | 0.492 | 0.479 | 0.367 | 0 | 620 | 620 | 140/140 | 990 | 0 | 15 | -5.254 | 2.560 | 0.117 | 0.117 | 336.0 |
| M_LOCUS_LABELS_SHUFFLED | 0.300 | 0.150 | 0.241 | 0.210 | 70 | 808 | 290 | 111/140 | 664 | 0 | 31 | -1.432 | 6.166 | 0.718 | 0.718 | 2439.5 |
| M_MINUS_DIAGNOSTIC_EVALUATOR_GATE | 0.910 | 0.882 | 0.873 | 0.894 | 79 | 25 | 24 | 85/140 | 542 | 2 | 22 | 3.551 | 11.384 | 0.114 | 0.114 | 1172.2 |
| M_MINUS_LOWER_LEVEL_DISPOSITION | 0.895 | 0.884 | 0.880 | 0.892 | 98 | 30 | 30 | 100/140 | 266 | 7 | 24 | 4.050 | 11.811 | 0.121 | 0.114 | 862.4 |
| M_MINUS_PROSPECTIVE_DISCRIMINATOR | 0.843 | 0.834 | 0.843 | 0.733 | 7 | 181 | 181 | 140/140 | 229 | 0 | 6 | 4.482 | 11.928 | 0.117 | 0.117 | 1222.4 |
| M_ALWAYS_ESCALATE_WHEN_STUCK | 0.253 | 0.635 | 0.652 | 0.592 | 848 | 431 | 431 | 59/140 | 1249 | 115 | 30 | 6.855 | 15.006 | 0.140 | 0.121 | 886.4 |
| M_NEVER_ESCALATE | 0.568 | 0.923 | 0.919 | 0.452 | 0 | 518 | 518 | 140/140 | 470 | 0 | 0 | -3.220 | 4.723 | 0.117 | 0.117 | 1169.0 |
| C_RANDOM_POLICY | 0.207 | 0.072 | 0.092 | 0.237 | 285 | 790 | 405 | 61/140 | 750 | 70 | 114 | 0.601 | 8.541 | 0.315 | 0.391 | 53.9 |
| C_NEVER_INTERVENE | 0.117 | 0.117 | 0.129 | 0.000 | 0 | 1060 | 1060 | 140/140 | 0 | 0 | 0 | -7.837 | 0.000 | 0.117 | 0.117 | 3.3 |

## Per-stratum decision-correct rate (stratum = oracle class)

| stratum | n | B0_RETRY_SEARCH | B1_UNCERTAINTY_ABSTENTION | B2_FAILURE_TAXONOMY_DIAGNOSIS | B3_MODEL_BASED_DIAGNOSIS_VOI | B3_EQUAL_EXTRA_SEARCH_1_5X | B4_MDA_MODEL_EXPANSION | B5_R1_VERDICT_ONLY | B5_R2_PLUS_CANDIDATE_SET | B5_R3_PLUS_DISCRIMINATOR_TABLES | B5_R4_PLUS_DISPOSITION_RECORDS | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | B5_NO_ABSTENTION_GATE | M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | M_MINUS_LOCUS_DIAGNOSIS | M_LOCUS_LABELS_SHUFFLED | M_MINUS_DIAGNOSTIC_EVALUATOR_GATE | M_MINUS_LOWER_LEVEL_DISPOSITION | M_MINUS_PROSPECTIVE_DISCRIMINATOR | M_ALWAYS_ESCALATE_WHEN_STUCK | M_NEVER_ESCALATE | C_RANDOM_POLICY | C_NEVER_INTERVENE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SEARCH_INSUFFICIENT | 123 | 0.79 | 0.67 | 0.50 | 0.96 | 0.96 | 0.98 | 0.98 | 1.00 | 1.00 | 0.98 | 0.98 | 0.97 | 0.99 | 0.77 | 0.24 | 1.00 | 0.96 | 0.73 | 0.09 | 0.99 | 0.28 | 0.00 |
| MISSING_PREMISE_OR_DATA | 91 | 0.55 | 0.71 | 0.37 | 0.93 | 0.95 | 0.91 | 0.92 | 0.98 | 1.00 | 0.99 | 0.99 | 0.96 | 1.00 | 0.69 | 0.19 | 1.00 | 0.97 | 0.74 | 0.14 | 1.00 | 0.24 | 0.00 |
| MODEL_FAMILY_INADEQUATE | 113 | 0.07 | 0.66 | 0.63 | 0.92 | 0.96 | 0.96 | 0.91 | 0.68 | 0.58 | 0.88 | 0.92 | 0.93 | 0.98 | 0.24 | 0.21 | 0.99 | 0.99 | 0.85 | 0.42 | 0.00 | 0.19 | 0.00 |
| REPRESENTATION_INSUFFICIENT | 69 | 0.00 | 0.36 | 1.00 | 0.91 | 1.00 | 0.93 | 0.74 | 0.70 | 0.78 | 1.00 | 1.00 | 1.00 | 0.97 | 0.10 | 0.29 | 1.00 | 1.00 | 0.97 | 0.28 | 0.00 | 0.28 | 0.00 |
| PROBE_ACTION_INSUFFICIENT | 71 | 0.32 | 0.65 | 0.45 | 1.00 | 1.00 | 1.00 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.94 | 0.75 | 0.17 | 0.99 | 1.00 | 0.59 | 0.00 | 0.94 | 0.17 | 0.00 |
| MEASUREMENT_OR_EVALUATOR_BLIND | 63 | 0.00 | 0.21 | 0.00 | 0.75 | 1.00 | 0.75 | 0.25 | 0.25 | 0.44 | 0.57 | 1.00 | 1.00 | 0.89 | 0.06 | 0.27 | 0.90 | 0.90 | 0.89 | 0.59 | 0.00 | 0.14 | 0.00 |
| FORMALISM_OR_OPERATOR_INSUFFICIENT | 55 | 0.02 | 0.47 | 0.22 | 0.91 | 1.00 | 0.89 | 0.69 | 0.65 | 0.76 | 1.00 | 1.00 | 1.00 | 1.00 | 0.09 | 0.15 | 1.00 | 1.00 | 1.00 | 0.13 | 0.00 | 0.20 | 0.00 |
| PROBLEM_OBJECTIVE_MISSPECIFIED | 80 | 0.00 | 0.28 | 0.05 | 0.82 | 1.00 | 0.78 | 0.65 | 0.59 | 0.71 | 1.00 | 1.00 | 1.00 | 0.90 | 0.07 | 0.26 | 0.91 | 0.95 | 0.89 | 0.29 | 0.00 | 0.15 | 0.00 |
| TOOL_INSTRUMENT_INADEQUATE | 68 | 0.00 | 0.51 | 0.00 | 0.84 | 1.00 | 0.75 | 0.81 | 0.76 | 0.81 | 1.00 | 1.00 | 1.00 | 0.91 | 0.04 | 0.34 | 0.97 | 0.94 | 0.93 | 0.60 | 0.00 | 0.10 | 0.00 |
| WORKFLOW_INADEQUATE | 50 | 0.00 | 0.18 | 1.00 | 0.70 | 1.00 | 0.68 | 0.62 | 0.52 | 0.84 | 1.00 | 1.00 | 1.00 | 1.00 | 0.02 | 0.32 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.12 | 0.00 |
| NO_ESCALATION_NEEDED | 277 | 0.30 | 0.63 | 0.34 | 0.82 | 0.92 | 0.82 | 0.77 | 0.89 | 0.98 | 0.99 | 0.99 | 0.96 | 0.95 | 0.64 | 0.22 | 0.97 | 0.90 | 0.78 | 0.20 | 0.95 | 0.21 | 0.00 |
| CANNOT_IDENTIFY | 140 | 0.00 | 0.99 | 0.00 | 0.06 | 0.00 | 0.06 | 0.00 | 0.91 | 0.92 | 0.86 | 0.96 | 0.31 | 1.00 | 1.00 | 0.79 | 0.41 | 0.46 | 1.00 | 0.00 | 1.00 | 0.26 | 1.00 |

## Per-variant decision-correct rate

| variant | n | B0_RETRY_SEARCH | B1_UNCERTAINTY_ABSTENTION | B2_FAILURE_TAXONOMY_DIAGNOSIS | B3_MODEL_BASED_DIAGNOSIS_VOI | B3_EQUAL_EXTRA_SEARCH_1_5X | B4_MDA_MODEL_EXPANSION | B5_R1_VERDICT_ONLY | B5_R2_PLUS_CANDIDATE_SET | B5_R3_PLUS_DISCRIMINATOR_TABLES | B5_R4_PLUS_DISPOSITION_RECORDS | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | B5_NO_ABSTENTION_GATE | M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | M_MINUS_LOCUS_DIAGNOSIS | M_LOCUS_LABELS_SHUFFLED | M_MINUS_DIAGNOSTIC_EVALUATOR_GATE | M_MINUS_LOWER_LEVEL_DISPOSITION | M_MINUS_PROSPECTIVE_DISCRIMINATOR | M_ALWAYS_ESCALATE_WHEN_STUCK | M_NEVER_ESCALATE | C_RANDOM_POLICY | C_NEVER_INTERVENE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CI | 50 | 0.00 | 1.00 | 0.00 | 0.10 | 0.00 | 0.08 | 0.00 | 0.90 | 0.92 | 0.86 | 1.00 | 0.08 | 1.00 | 1.00 | 1.00 | 0.00 | 0.14 | 1.00 | 0.00 | 1.00 | 0.14 | 1.00 |
| PARTIAL | 126 | 0.10 | 0.00 | 0.52 | 0.94 | 0.99 | 0.94 | 0.45 | 0.37 | 0.42 | 0.92 | 0.98 | 0.97 | 0.98 | 0.37 | 0.17 | 0.99 | 0.96 | 0.76 | 0.49 | 0.33 | 0.25 | 0.00 |
| PARTNER_OF_CI | 50 | 0.22 | 0.76 | 0.08 | 0.44 | 0.48 | 0.42 | 0.46 | 0.88 | 0.94 | 0.92 | 1.00 | 0.52 | 1.00 | 0.82 | 0.66 | 0.60 | 0.52 | 1.00 | 0.02 | 0.84 | 0.20 | 0.42 |
| PARTNER_OF_PARTIAL | 126 | 0.33 | 0.48 | 0.44 | 0.87 | 0.91 | 0.87 | 0.67 | 0.88 | 0.96 | 0.96 | 0.99 | 0.97 | 0.97 | 0.59 | 0.33 | 0.99 | 0.90 | 0.79 | 0.19 | 0.76 | 0.25 | 0.03 |
| PARTNER_OF_PLAIN | 412 | 0.31 | 0.79 | 0.28 | 0.76 | 0.82 | 0.76 | 0.76 | 0.90 | 0.92 | 0.96 | 0.98 | 0.92 | 0.95 | 0.53 | 0.30 | 0.93 | 0.94 | 0.86 | 0.14 | 0.72 | 0.23 | 0.16 |
| PARTNER_OF_SAME_FIX | 12 | 0.00 | 0.42 | 0.58 | 0.83 | 0.83 | 0.92 | 0.92 | 0.58 | 0.50 | 0.92 | 0.92 | 0.83 | 1.00 | 0.83 | 0.17 | 1.00 | 0.92 | 0.58 | 0.33 | 0.42 | 0.33 | 0.00 |
| PLAIN | 412 | 0.17 | 0.56 | 0.41 | 0.83 | 0.97 | 0.82 | 0.80 | 0.80 | 0.91 | 0.94 | 0.98 | 0.97 | 0.95 | 0.31 | 0.21 | 0.98 | 0.96 | 0.85 | 0.36 | 0.37 | 0.16 | 0.00 |
| SAME_FIX | 12 | 0.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.42 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 0.00 | 1.00 | 1.00 | 0.33 | 0.67 | 0.00 | 0.25 | 0.00 |

## Gates

- **G0a_KNOWN_ANSWER**: pass=True — 14 hand-authored fixtures (oracle targets; M and B5 decision-correct) + separation pair reproduced in selftest
- **G0b_ORACLE_SELF_AGREEMENT**: pass=True — enumeration == branch-and-bound and a truth-agnostic decision-correct policy exists on every instance; variant invariants hold; >= min decoys per apparent class (typical level >= 1) and >= min inverse decoys per level-0 class and apparent-CANNOT_IDENTIFY
- **G0c_NULL_CALIBRATION**: pass=True — NEVER_INTERVENE decision-correct = 0 on identifiable instances; RANDOM <= 0.25; M scored against the partner's oracle <= M's true rate - 0.30
- **G1a_B5_REPRODUCES_M**: pass=False — intervention/declaration sequences identical on >= 99.5% of instances and no stratum > 5% discordant
- **G1b_M_ADVANTAGE**: pass=False — minimal-level decision-correct diff (M - B5) > 0, exact two-sided p <= 0.05, >= 1 stratum with >= 5 M-only-correct
- **G1c_B5_ADVANTAGE**: pass=True — symmetric: diff < 0 with p <= 0.05 (B5 dominates)
- **G2_ANTI_ESCALATION**: pass=True — M false escalations <= B5's and M specification damage <= B5's
- **G3_MEDIATION**: pass=None — (a) M's class correct on >= 80% of M-only-correct instances; (b) on each advantaged stratum both locus ablations <= B5; (c) B3 with 1.5x budget does not reach M (paired p <= 0.05)
- **G4_INTERFACE_LADDER**: pass=True — no rung k+1 significantly worse than rung k (exact p <= 0.05); rung-5 gap = G1 paired test
- **COST**: pass=None — paired sign test on per-instance regret (registered cost units) at p <= 0.05; wall-clock reported only

## Route

`PARENT_SUFFICIENT` — B5 dominates M on minimal-level decisions (B5_DOMINATES). Ladder terminal: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. Cost: `COST_ADVANTAGE_B5`.
