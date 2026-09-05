# ME-X2-V3 — PROTECTED analysis

Route: **PARENT_SUFFICIENT (parity within power)** · lever verdict: **THRESHOLD_NULL** · n = 1200

| arm | decision | false esc. | missed esc. | spec dmg | false CI | correct CI |
|---|---:|---:|---:|---:|---:|---:|
| B3_EQUAL_EXTRA_SEARCH_1_5X | 0.8500 | 168 | 1 | 11 | 0 | 6 |
| B3_MODEL_BASED_DIAGNOSIS_VOI | 0.7850 | 114 | 91 | 10 | 2 | 22 |
| B5_R1_VERDICT_ONLY | 0.6867 | 98 | 225 | 18 | 0 | 0 |
| B5_R2_PLUS_CANDIDATE_SET | 0.8217 | 16 | 202 | 4 | 202 | 144 |
| B5_R3_PLUS_DISCRIMINATOR_TABLES | 0.8692 | 20 | 140 | 4 | 140 | 140 |
| B5_R4_PLUS_DISPOSITION_RECORDS | 0.9508 | 31 | 31 | 14 | 9 | 126 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 0.9883 | 14 | 0 | 0 | 0 | 140 |
| C_NEVER_INTERVENE | 0.1217 | 0 | 1054 | 0 | 1054 | 146 |
| C_RANDOM_POLICY | 0.2117 | 286 | 792 | 63 | 388 | 62 |
| M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS | 0.9900 | 0 | 12 | 0 | 12 | 146 |
| M3_MINRANK_TAU_000 | 0.9292 | 73 | 12 | 12 | 12 | 112 |
| M3_MINRANK_TAU_100 | 0.9900 | 0 | 12 | 0 | 12 | 146 |
| M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | 0.9742 | 1 | 30 | 0 | 30 | 145 |

| gate | pass | detail |
|---|---|---|
| G0a_SELFTEST | True | {} |
| G0b_ORACLE_SELF_AGREEMENT | True | {} |
| G0c_NULL_CALIBRATION | True | {"never_intervene_on_identifiable": 0, "random": 0.21166666666666667} |
| G1b_M3_ADVANTAGE_OVER_B5 | False | {"n": 1200, "x_only": 14, "y_only": 12, "discordant": 26, "diff_x_minus_y": 0.0016666666666666668, "wald_ci95": [-0.006661197983387969, 0.009994531316721303], "exact_p_two_sided": 0.8450189828872681} |
| G1c_B5_ADVANTAGE_OVER_M3 | False | {} |
| G2_ANTI_ESCALATION_VS_B5 | True | {"M3_false_escalation": 0, "B5_false_escalation": 14, "M3_spec_damage": 0, "B5_spec_damage": 0} |
| G2b_OVER_ESCALATION_COUNT | None | {"M3": 0, "M2": 0, "M_V1": 1, "B5": 14, "M3_missed_escalation": 12, "M2_missed_escalation": 12, "B5_missed_escalation": 0, "note": "co-primary, reported in absolute counts; G2 gates on B5's harm"} |
| G5_LEVER_ATTRIBUTION | False | {"M3_minus_M2": {"n": 1200, "x_only": 0, "y_only": 0, "discordant": 0, "diff_x_minus_y": 0.0, "wald_ci95": [0.0, 0.0], "exact_p_two_sided": 1.0}, "M3_only_correct": 0, "M2_only_correct": 0, "mechanism_rate_on_M3_only": null, "threshold_activity": {"instances_t |
| G4_INTERFACE_LADDER | None | {"rates": {"B5_R1_VERDICT_ONLY": 0.6866666666666666, "B5_R2_PLUS_CANDIDATE_SET": 0.8216666666666667, "B5_R3_PLUS_DISCRIMINATOR_TABLES": 0.8691666666666666, "B5_R4_PLUS_DISPOSITION_RECORDS": 0.9508333333333333, "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION": 0.98833 |

Authority: grants nothing. `NO NOVELTY OR BREAKTHROUGH CLAIM`.
