# ME-X2 V2 revival analysis — PROTECTED

Results sha256 `3503863a7292f77978026b230604f43a16c652324293bc75cf35c722ea1781bb`; custody sha256 `f71aba5dac2427754852a91a4b8d38e1bfdc59e32bb867fa90f98fe527425daf`; instances 1200.

## Per-arm outcomes (S5)

| arm | decision (min-level) | class | locus | success | false esc. | missed esc. | false CI | correct CI | recur. | spec dmg | mean regret | mean cost | Brier | ECE5 | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_RETRY_SEARCH | 0.217 | 0.111 | 0.324 | 0.217 | 14 | 788 | 0 | 0/151 | 2776 | 0 | -3.602 | 4.595 | n/a | n/a | 12.7 |
| B1_UNCERTAINTY_ABSTENTION | 0.624 | 0.769 | 0.806 | 0.498 | 0 | 451 | 451 | 151/151 | 0 | 0 | 2.255 | 10.099 | 0.126 | 0.126 | 50.8 |
| B2_FAILURE_TAXONOMY_DIAGNOSIS | 0.374 | 0.476 | 0.480 | 0.602 | 500 | 381 | 0 | 0/151 | 1680 | 26 | 3.857 | 12.044 | n/a | n/a | 22.1 |
| B3_MODEL_BASED_DIAGNOSIS_VOI | 0.787 | 0.787 | 0.794 | 0.822 | 90 | 97 | 3 | 23/151 | 252 | 7 | 2.869 | 10.682 | 0.133 | 0.126 | 83.5 |
| B3_EQUAL_EXTRA_SEARCH_1_5X | 0.846 | 0.850 | 0.845 | 0.970 | 173 | 0 | 0 | 2/151 | 195 | 7 | 4.533 | 13.311 | 0.122 | 0.114 | 92.8 |
| B4_MDA_MODEL_EXPANSION | 0.774 | 0.787 | 0.785 | 0.813 | 102 | 110 | 4 | 24/151 | 251 | 7 | 2.831 | 10.643 | 0.127 | 0.112 | 74.1 |
| B5_R1_VERDICT_ONLY | 0.684 | 0.686 | 0.695 | 0.708 | 93 | 224 | 0 | 0/151 | 201 | 15 | 2.059 | 9.929 | n/a | n/a | 31.2 |
| B5_R2_PLUS_CANDIDATE_SET | 0.816 | 0.830 | 0.844 | 0.705 | 16 | 206 | 205 | 148/151 | 221 | 5 | 1.666 | 9.154 | 0.154 | 0.151 | 30.5 |
| B5_R3_PLUS_DISCRIMINATOR_TABLES | 0.867 | 0.841 | 0.863 | 0.757 | 15 | 146 | 146 | 146/151 | 825 | 5 | 1.561 | 9.002 | 0.151 | 0.144 | 877.7 |
| B5_R4_PLUS_DISPOSITION_RECORDS | 0.949 | 0.899 | 0.884 | 0.851 | 27 | 36 | 4 | 134/151 | 875 | 22 | 2.987 | 10.320 | 0.152 | 0.151 | 791.6 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 0.991 | 0.940 | 0.926 | 0.876 | 11 | 0 | 0 | 149/151 | 824 | 0 | 3.429 | 10.532 | 0.128 | 0.125 | 692.4 |
| B5_NO_ABSTENTION_GATE | 0.911 | 0.884 | 0.868 | 0.903 | 105 | 6 | 6 | 110/151 | 888 | 9 | 3.314 | 11.171 | 0.127 | 0.125 | 2094.4 |
| M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | 0.966 | 0.912 | 0.893 | 0.840 | 0 | 41 | 41 | 151/151 | 441 | 0 | 2.998 | 10.143 | 0.126 | 0.126 | 1275.3 |
| M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS | 0.985 | 0.938 | 0.923 | 0.859 | 0 | 18 | 18 | 151/151 | 413 | 0 | 3.448 | 10.568 | 0.126 | 0.126 | 807.8 |
| M2_L1_LOOKAHEAD_ONLY | 0.971 | 0.913 | 0.897 | 0.845 | 0 | 35 | 35 | 151/151 | 408 | 0 | 3.135 | 10.264 | 0.126 | 0.126 | 706.7 |
| M2_L2_BEST_HYPOTHESIS_ONLY | 0.914 | 0.938 | 0.924 | 0.788 | 0 | 103 | 103 | 151/151 | 489 | 0 | 2.057 | 9.352 | 0.126 | 0.126 | 592.9 |
| M2_MINUS_LOCUS_DIAGNOSIS | 0.615 | 0.646 | 0.659 | 0.491 | 2 | 460 | 460 | 151/151 | 1472 | 0 | -3.897 | 3.966 | 0.126 | 0.126 | 452.6 |
| M2_LOCUS_LABELS_SHUFFLED | 0.342 | 0.133 | 0.226 | 0.277 | 77 | 717 | 154 | 83/151 | 792 | 0 | -0.381 | 7.289 | 0.884 | 0.884 | 2384.0 |
| M2_MINUS_DIAGNOSTIC_EVALUATOR_GATE | 0.922 | 0.874 | 0.863 | 0.885 | 65 | 18 | 18 | 100/151 | 450 | 6 | 3.448 | 11.226 | 0.121 | 0.121 | 891.1 |
| M2_MINUS_LOWER_LEVEL_DISPOSITION | 0.906 | 0.878 | 0.872 | 0.870 | 76 | 37 | 37 | 119/151 | 199 | 7 | 3.951 | 11.672 | 0.131 | 0.126 | 629.4 |
| M2_MINUS_PROSPECTIVE_DISCRIMINATOR | 0.669 | 0.904 | 0.901 | 0.547 | 5 | 392 | 392 | 151/151 | 278 | 0 | 3.514 | 11.147 | 0.126 | 0.126 | 641.8 |
| M2_ALWAYS_ESCALATE_WHEN_STUCK | 0.271 | 0.613 | 0.637 | 0.600 | 847 | 427 | 427 | 53/151 | 1207 | 101 | 6.892 | 15.173 | 0.140 | 0.123 | 626.8 |
| M2_NEVER_ESCALATE | 0.589 | 0.938 | 0.933 | 0.463 | 0 | 493 | 493 | 151/151 | 413 | 0 | -3.139 | 4.809 | 0.126 | 0.126 | 797.6 |
| C_RANDOM_POLICY | 0.185 | 0.062 | 0.089 | 0.199 | 296 | 825 | 420 | 58/151 | 808 | 75 | 1.029 | 8.987 | 0.336 | 0.432 | 64.9 |
| C_NEVER_INTERVENE | 0.126 | 0.126 | 0.138 | 0.000 | 0 | 1049 | 1049 | 151/151 | 0 | 0 | -7.962 | 0.000 | 0.126 | 0.126 | 3.9 |

## Per-stratum decision-correct rate (stratum = oracle class)

| stratum | n | B0_RETRY_SEARCH | B1_UNCERTAINTY_ABSTENTION | B2_FAILURE_TAXONOMY_DIAGNOSIS | B3_MODEL_BASED_DIAGNOSIS_VOI | B3_EQUAL_EXTRA_SEARCH_1_5X | B4_MDA_MODEL_EXPANSION | B5_R1_VERDICT_ONLY | B5_R2_PLUS_CANDIDATE_SET | B5_R3_PLUS_DISCRIMINATOR_TABLES | B5_R4_PLUS_DISPOSITION_RECORDS | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | B5_NO_ABSTENTION_GATE | M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS | M2_L1_LOOKAHEAD_ONLY | M2_L2_BEST_HYPOTHESIS_ONLY | M2_MINUS_LOCUS_DIAGNOSIS | M2_LOCUS_LABELS_SHUFFLED | M2_MINUS_DIAGNOSTIC_EVALUATOR_GATE | M2_MINUS_LOWER_LEVEL_DISPOSITION | M2_MINUS_PROSPECTIVE_DISCRIMINATOR | M2_ALWAYS_ESCALATE_WHEN_STUCK | M2_NEVER_ESCALATE | C_RANDOM_POLICY | C_NEVER_INTERVENE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SEARCH_INSUFFICIENT | 133 | 0.80 | 0.71 | 0.56 | 0.95 | 0.95 | 0.94 | 0.98 | 0.95 | 1.00 | 0.99 | 0.99 | 0.99 | 0.99 | 1.00 | 0.99 | 1.00 | 0.98 | 0.31 | 1.00 | 0.95 | 0.80 | 0.14 | 1.00 | 0.19 | 0.00 |
| MISSING_PREMISE_OR_DATA | 79 | 0.47 | 0.81 | 0.46 | 0.96 | 0.95 | 0.91 | 0.94 | 0.97 | 1.00 | 1.00 | 1.00 | 0.97 | 0.97 | 1.00 | 0.97 | 1.00 | 0.96 | 0.32 | 1.00 | 0.97 | 0.77 | 0.09 | 1.00 | 0.16 | 0.00 |
| MODEL_FAMILY_INADEQUATE | 93 | 0.04 | 0.63 | 0.70 | 0.92 | 0.97 | 0.96 | 0.90 | 0.74 | 0.70 | 0.96 | 0.96 | 0.96 | 0.96 | 0.99 | 0.96 | 0.97 | 0.38 | 0.25 | 0.99 | 0.97 | 0.41 | 0.56 | 0.00 | 0.22 | 0.00 |
| REPRESENTATION_INSUFFICIENT | 64 | 0.02 | 0.41 | 1.00 | 0.89 | 1.00 | 0.88 | 0.78 | 0.75 | 0.81 | 1.00 | 1.00 | 1.00 | 0.97 | 0.98 | 0.97 | 0.88 | 0.12 | 0.25 | 0.98 | 0.97 | 0.53 | 0.25 | 0.00 | 0.11 | 0.00 |
| PROBE_ACTION_INSUFFICIENT | 70 | 0.33 | 0.66 | 0.43 | 0.99 | 1.00 | 0.99 | 0.84 | 0.99 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 1.00 | 0.99 | 1.00 | 1.00 | 0.33 | 1.00 | 1.00 | 0.83 | 0.00 | 1.00 | 0.17 | 0.00 |
| MEASUREMENT_OR_EVALUATOR_BLIND | 68 | 0.00 | 0.29 | 0.00 | 0.76 | 1.00 | 0.74 | 0.25 | 0.21 | 0.32 | 0.49 | 1.00 | 0.99 | 0.93 | 0.96 | 0.93 | 0.63 | 0.04 | 0.26 | 0.96 | 0.96 | 0.26 | 0.66 | 0.00 | 0.15 | 0.00 |
| FORMALISM_OR_OPERATOR_INSUFFICIENT | 63 | 0.00 | 0.49 | 0.17 | 0.94 | 1.00 | 0.90 | 0.76 | 0.71 | 0.78 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 | 0.98 | 0.90 | 0.11 | 0.25 | 1.00 | 1.00 | 0.71 | 0.29 | 0.00 | 0.13 | 0.00 |
| PROBLEM_OBJECTIVE_MISSPECIFIED | 86 | 0.00 | 0.28 | 0.13 | 0.77 | 1.00 | 0.76 | 0.59 | 0.53 | 0.72 | 1.00 | 1.00 | 0.99 | 0.87 | 0.90 | 0.88 | 0.67 | 0.06 | 0.28 | 0.90 | 0.81 | 0.51 | 0.22 | 0.00 | 0.22 | 0.00 |
| TOOL_INSTRUMENT_INADEQUATE | 65 | 0.00 | 0.52 | 0.02 | 0.83 | 1.00 | 0.80 | 0.75 | 0.74 | 0.83 | 1.00 | 1.00 | 1.00 | 0.97 | 0.98 | 0.98 | 0.75 | 0.06 | 0.45 | 0.98 | 0.97 | 0.32 | 0.49 | 0.00 | 0.14 | 0.00 |
| WORKFLOW_INADEQUATE | 51 | 0.00 | 0.33 | 1.00 | 0.73 | 1.00 | 0.73 | 0.69 | 0.67 | 0.76 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.78 | 0.02 | 0.57 | 1.00 | 1.00 | 0.29 | 1.00 | 0.00 | 0.16 | 0.00 |
| NO_ESCALATION_NEEDED | 277 | 0.32 | 0.66 | 0.38 | 0.89 | 0.93 | 0.87 | 0.81 | 0.94 | 0.99 | 0.99 | 0.99 | 0.96 | 0.96 | 0.99 | 0.97 | 0.98 | 0.89 | 0.30 | 0.99 | 0.95 | 0.77 | 0.24 | 0.99 | 0.19 | 0.00 |
| CANNOT_IDENTIFY | 151 | 0.00 | 1.00 | 0.00 | 0.11 | 0.00 | 0.11 | 0.00 | 0.95 | 0.93 | 0.89 | 0.99 | 0.43 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.55 | 0.50 | 0.58 | 1.00 | 0.00 | 1.00 | 0.25 | 1.00 |

## Gates

- **G0a_KNOWN_ANSWER**: pass=True — V1's 14 hand-authored fixtures and separation pair (M2 and B5 decision-correct) plus the V2 lever known-answer fixtures, reproduced in selftest
- **G0b_ORACLE_SELF_AGREEMENT**: pass=True — enumeration == branch-and-bound and a truth-agnostic decision-correct policy exists on every instance; variant invariants hold; >= min decoys per apparent class, inverse decoys per level-0 class and apparent-CANNOT_IDENTIFY identifiable instances
- **G0c_NULL_CALIBRATION**: pass=True — NEVER_INTERVENE decision-correct = 0 on identifiable instances; RANDOM <= 0.25 (enforced on PROTECTED and G0SCALE, reported below that split size); M2 scored against the partner's oracle <= M2's true rate - 0.30
- **G0d_V1_PROVENANCE**: pass=True — every frozen V1 file (generator, oracle, catalogue, parents, arms, runner, design JSON) byte-identical to the hash published in the V1 receipt: V2 changes the arm under test and nothing else
- **G1a_B5_REPRODUCES_M2**: pass=False — intervention/declaration sequences identical on >= 99.5% of instances and no stratum > 5% discordant
- **G1b_M2_ADVANTAGE**: pass=False — minimal-level decision-correct diff (M2 - B5) > 0, exact two-sided p <= 0.05, >= 1 stratum with >= 5 M2-only-correct
- **G1c_B5_ADVANTAGE**: pass=False — symmetric: diff < 0 with p <= 0.05 (B5 dominates)
- **G2_ANTI_ESCALATION**: pass=True — M2 false escalations and specification damage <= B5's (V1's clause) AND <= V1's M: a revival may not buy decisions with escalation harm
- **G3_MEDIATION**: pass=None — (a) M2's class correct on >= 80% of M2-only-correct instances; (b) on each advantaged stratum both locus ablations <= B5; (c) B3 with 1.5x budget does not reach M2 (paired p <= 0.05)
- **G4_INTERFACE_LADDER**: pass=True — no rung k+1 significantly worse than rung k (exact p <= 0.05); rung-5 gap = the G1 paired test
- **G5_LEVER_ATTRIBUTION**: pass=True — (a) paired M2 - M_V1 > 0 at exact p <= 0.05 [routes the lever verdict]; (b) neither single-lever arm improves on M_V1 by more than the conjunction does [reported diagnostic]; (c) >= 80% of M2-only-correct instances are ones where V1 declared a false CANNOT_IDENTIFY AND M2's EXECUTED lever receipts show an L2-only-admissible action or an L1-changed choice [routes the lever verdict: failing it gives LEVERS_NOT_ATTRIBUTED]; (d) M2 loses fewer instances to V1 than it gains: the revival must not move the failure [routes the lever verdict: failing it gives LEVERS_MOVE_THE_FAILURE]

## Route

`PARENT_SUFFICIENT` — no M2 advantage over B5 (discordance without significance).

Lever verdict: `LEVERS_RECOVER_M` (M2 0.985, V1's M 0.966, B5 0.991). Ladder terminal: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. Cost: `COST_ADVANTAGE_B5`.
