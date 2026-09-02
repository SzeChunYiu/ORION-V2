# ME-X2 V2 revival analysis — DEVELOPMENT

**DEVELOPMENT split: not protected evidence. Numbers below cannot support any confirmatory claim.**

Results sha256 `533b38af3f8965b3ae34f43f21a66bdfa5073b6502ed6465790fcd452f209485`; custody sha256 `cb7d75876ae4a5169ab301689e07db1a6bedace83d1e077a3fc1292c64b03131`; instances 48.

## Per-arm outcomes (S5)

| arm | decision (min-level) | class | locus | success | false esc. | missed esc. | false CI | correct CI | recur. | spec dmg | mean regret | mean cost | Brier | ECE5 | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_RETRY_SEARCH | 0.208 | 0.083 | 0.271 | 0.208 | 1 | 30 | 0 | 0/8 | 111 | 0 | -2.650 | 5.521 | n/a | n/a | 0.5 |
| B1_UNCERTAINTY_ABSTENTION | 0.708 | 0.854 | 0.854 | 0.542 | 0 | 14 | 14 | 8/8 | 0 | 0 | 2.975 | 10.667 | 0.167 | 0.167 | 1.8 |
| B2_FAILURE_TAXONOMY_DIAGNOSIS | 0.292 | 0.458 | 0.521 | 0.625 | 24 | 12 | 0 | 0/8 | 64 | 1 | 4.900 | 12.604 | n/a | n/a | 0.7 |
| B3_MODEL_BASED_DIAGNOSIS_VOI | 0.729 | 0.750 | 0.771 | 0.792 | 4 | 4 | 0 | 1/8 | 5 | 0 | 2.375 | 10.125 | 0.157 | 0.151 | 3.8 |
| B3_EQUAL_EXTRA_SEARCH_1_5X | 0.792 | 0.792 | 0.812 | 0.938 | 8 | 0 | 0 | 0/8 | 2 | 0 | 4.725 | 13.375 | 0.130 | 0.130 | 3.7 |
| B4_MDA_MODEL_EXPANSION | 0.708 | 0.729 | 0.729 | 0.750 | 3 | 6 | 0 | 1/8 | 4 | 0 | 2.250 | 10.021 | 0.131 | 0.138 | 2.6 |
| B5_R1_VERDICT_ONLY | 0.729 | 0.729 | 0.729 | 0.750 | 1 | 5 | 0 | 0/8 | 2 | 0 | 2.250 | 9.812 | n/a | n/a | 1.3 |
| B5_R2_PLUS_CANDIDATE_SET | 0.896 | 0.896 | 0.896 | 0.729 | 0 | 5 | 5 | 8/8 | 2 | 0 | 2.250 | 9.583 | 0.167 | 0.167 | 1.0 |
| B5_R3_PLUS_DISCRIMINATOR_TABLES | 0.917 | 0.896 | 0.896 | 0.750 | 0 | 4 | 4 | 8/8 | 28 | 0 | 1.775 | 9.062 | 0.172 | 0.177 | 22.4 |
| B5_R4_PLUS_DISPOSITION_RECORDS | 0.979 | 0.875 | 0.875 | 0.833 | 1 | 0 | 0 | 8/8 | 29 | 0 | 2.825 | 9.917 | 0.177 | 0.167 | 19.6 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 0.979 | 0.875 | 0.875 | 0.833 | 1 | 0 | 0 | 8/8 | 29 | 0 | 2.875 | 9.958 | 0.177 | 0.167 | 19.9 |
| B5_NO_ABSTENTION_GATE | 0.896 | 0.833 | 0.833 | 0.875 | 5 | 0 | 0 | 6/8 | 31 | 0 | 2.750 | 10.562 | 0.177 | 0.167 | 43.0 |
| M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | 1.000 | 0.896 | 0.896 | 0.833 | 0 | 0 | 0 | 8/8 | 12 | 0 | 3.250 | 10.250 | 0.167 | 0.167 | 40.1 |
| M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS | 1.000 | 0.896 | 0.896 | 0.833 | 0 | 0 | 0 | 8/8 | 11 | 0 | 3.225 | 10.250 | 0.167 | 0.167 | 26.9 |
| M2_L1_LOOKAHEAD_ONLY | 1.000 | 0.896 | 0.896 | 0.833 | 0 | 0 | 0 | 8/8 | 11 | 0 | 3.225 | 10.250 | 0.167 | 0.167 | 25.6 |
| M2_L2_BEST_HYPOTHESIS_ONLY | 0.917 | 0.896 | 0.896 | 0.750 | 0 | 4 | 4 | 8/8 | 13 | 0 | 1.650 | 8.917 | 0.167 | 0.167 | 18.6 |
| M2_MINUS_LOCUS_DIAGNOSIS | 0.625 | 0.646 | 0.667 | 0.458 | 0 | 18 | 18 | 8/8 | 58 | 0 | -4.675 | 3.646 | 0.167 | 0.167 | 14.1 |
| M2_LOCUS_LABELS_SHUFFLED | 0.354 | 0.125 | 0.188 | 0.292 | 2 | 26 | 4 | 3/8 | 29 | 0 | -0.050 | 7.688 | 0.902 | 0.902 | 81.6 |
| M2_MINUS_DIAGNOSTIC_EVALUATOR_GATE | 0.938 | 0.833 | 0.833 | 0.875 | 3 | 0 | 0 | 5/8 | 12 | 0 | 3.225 | 10.896 | 0.167 | 0.167 | 27.0 |
| M2_MINUS_LOWER_LEVEL_DISPOSITION | 0.896 | 0.854 | 0.854 | 0.833 | 3 | 2 | 2 | 6/8 | 1 | 0 | 3.425 | 11.188 | 0.151 | 0.156 | 19.4 |
| M2_MINUS_PROSPECTIVE_DISCRIMINATOR | 0.750 | 0.917 | 0.917 | 0.583 | 0 | 12 | 12 | 8/8 | 8 | 0 | 4.125 | 11.500 | 0.167 | 0.167 | 21.8 |
| M2_ALWAYS_ESCALATE_WHEN_STUCK | 0.208 | 0.646 | 0.604 | 0.625 | 37 | 15 | 15 | 3/8 | 40 | 6 | 7.700 | 15.667 | 0.179 | 0.153 | 19.9 |
| M2_NEVER_ESCALATE | 0.604 | 0.896 | 0.896 | 0.438 | 0 | 19 | 19 | 8/8 | 11 | 0 | -3.675 | 4.500 | 0.167 | 0.167 | 26.3 |
| C_RANDOM_POLICY | 0.271 | 0.021 | 0.125 | 0.229 | 8 | 30 | 14 | 7/8 | 25 | 2 | -1.150 | 7.208 | 0.309 | 0.414 | 2.3 |
| C_NEVER_INTERVENE | 0.167 | 0.167 | 0.167 | 0.000 | 0 | 40 | 40 | 8/8 | 0 | 0 | -8.075 | 0.000 | 0.167 | 0.167 | 0.2 |

## Per-stratum decision-correct rate (stratum = oracle class)

| stratum | n | B0_RETRY_SEARCH | B1_UNCERTAINTY_ABSTENTION | B2_FAILURE_TAXONOMY_DIAGNOSIS | B3_MODEL_BASED_DIAGNOSIS_VOI | B3_EQUAL_EXTRA_SEARCH_1_5X | B4_MDA_MODEL_EXPANSION | B5_R1_VERDICT_ONLY | B5_R2_PLUS_CANDIDATE_SET | B5_R3_PLUS_DISCRIMINATOR_TABLES | B5_R4_PLUS_DISPOSITION_RECORDS | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | B5_NO_ABSTENTION_GATE | M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS | M2_L1_LOOKAHEAD_ONLY | M2_L2_BEST_HYPOTHESIS_ONLY | M2_MINUS_LOCUS_DIAGNOSIS | M2_LOCUS_LABELS_SHUFFLED | M2_MINUS_DIAGNOSTIC_EVALUATOR_GATE | M2_MINUS_LOWER_LEVEL_DISPOSITION | M2_MINUS_PROSPECTIVE_DISCRIMINATOR | M2_ALWAYS_ESCALATE_WHEN_STUCK | M2_NEVER_ESCALATE | C_RANDOM_POLICY | C_NEVER_INTERVENE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SEARCH_INSUFFICIENT | 4 | 0.75 | 0.50 | 0.25 | 1.00 | 1.00 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.50 | 0.00 |
| MISSING_PREMISE_OR_DATA | 3 | 0.00 | 1.00 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 1.00 | 1.00 | 0.67 | 0.33 | 1.00 | 0.00 | 0.00 |
| MODEL_FAMILY_INADEQUATE | 4 | 0.00 | 1.00 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 0.75 | 0.75 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | 0.00 | 1.00 | 1.00 | 0.50 | 0.25 | 0.00 | 0.25 | 0.00 |
| REPRESENTATION_INSUFFICIENT | 2 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 0.50 | 1.00 | 0.50 | 0.00 | 0.50 | 0.00 | 0.00 | 0.00 |
| PROBE_ACTION_INSUFFICIENT | 5 | 0.40 | 0.60 | 0.20 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.60 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.40 | 0.00 |
| MEASUREMENT_OR_EVALUATOR_BLIND | 2 | 0.00 | 0.50 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| FORMALISM_OR_OPERATOR_INSUFFICIENT | 3 | 0.00 | 0.67 | 0.00 | 1.00 | 1.00 | 0.67 | 0.67 | 0.67 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.00 | 0.33 | 1.00 | 1.00 | 0.33 | 0.33 | 0.00 | 0.00 | 0.00 |
| PROBLEM_OBJECTIVE_MISSPECIFIED | 3 | 0.00 | 0.00 | 0.33 | 0.67 | 1.00 | 0.67 | 0.67 | 0.67 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.00 | 0.67 | 1.00 | 0.67 | 0.33 | 0.00 | 0.00 | 0.00 | 0.00 |
| TOOL_INSTRUMENT_INADEQUATE | 3 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.67 | 1.00 | 1.00 | 0.67 | 0.67 | 0.00 | 0.00 | 0.00 |
| WORKFLOW_INADEQUATE | 2 | 0.00 | 0.50 | 1.00 | 0.50 | 1.00 | 0.50 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.50 | 0.00 |
| NO_ESCALATION_NEEDED | 9 | 0.56 | 0.78 | 0.33 | 0.89 | 0.78 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.22 | 1.00 | 1.00 | 0.78 | 0.00 | 1.00 | 0.22 | 0.00 |
| CANNOT_IDENTIFY | 8 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.38 | 0.62 | 0.62 | 1.00 | 0.00 | 1.00 | 0.62 | 1.00 |

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
- **G5_LEVER_ATTRIBUTION**: pass=False — (a) paired M2 - M_V1 > 0 at exact p <= 0.05 [routes the lever verdict]; (b) neither single-lever arm improves on M_V1 by more than the conjunction does [reported diagnostic]; (c) >= 80% of M2-only-correct instances are ones where V1 declared a false CANNOT_IDENTIFY AND M2's EXECUTED lever receipts show an L2-only-admissible action or an L1-changed choice [routes the lever verdict: failing it gives LEVERS_NOT_ATTRIBUTED]; (d) M2 loses fewer instances to V1 than it gains: the revival must not move the failure [routes the lever verdict: failing it gives LEVERS_MOVE_THE_FAILURE]

## Route

`PARENT_SUFFICIENT` — no M2 advantage over B5 (discordance without significance).

Lever verdict: `LEVERS_NULL` (M2 1.000, V1's M 1.000, B5 0.979). Ladder terminal: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. Cost: `COST_PARITY`.
