# ME-X2-V3 — DEVELOPMENT analysis

Route: **PARENT_SUFFICIENT (parity within power)** · lever verdict: **THRESHOLD_NULL** · n = 48

| arm | decision | false esc. | missed esc. | spec dmg | false CI | correct CI |
|---|---:|---:|---:|---:|---:|---:|
| B3_EQUAL_EXTRA_SEARCH_1_5X | 0.8542 | 6 | 0 | 0 | 0 | 0 |
| B3_MODEL_BASED_DIAGNOSIS_VOI | 0.7708 | 4 | 5 | 0 | 0 | 3 |
| B5_R1_VERDICT_ONLY | 0.7292 | 3 | 6 | 0 | 0 | 0 |
| B5_R2_PLUS_CANDIDATE_SET | 0.8750 | 0 | 6 | 0 | 6 | 7 |
| B5_R3_PLUS_DISCRIMINATOR_TABLES | 0.9375 | 0 | 3 | 0 | 3 | 7 |
| B5_R4_PLUS_DISPOSITION_RECORDS | 0.9792 | 0 | 1 | 0 | 0 | 7 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 1.0000 | 0 | 0 | 0 | 0 | 7 |
| C_NEVER_INTERVENE | 0.1458 | 0 | 41 | 0 | 41 | 7 |
| C_RANDOM_POLICY | 0.1875 | 13 | 34 | 4 | 18 | 4 |
| M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS | 0.9792 | 0 | 1 | 0 | 1 | 7 |
| M3_MINRANK_TAU_000 | 0.9167 | 3 | 1 | 0 | 1 | 5 |
| M3_MINRANK_TAU_100 | 0.9792 | 0 | 1 | 0 | 1 | 7 |
| M_ME_LOCUS_PLUS_MINIMUM_ESCALATION | 0.9583 | 0 | 2 | 0 | 2 | 7 |

| gate | pass | detail |
|---|---|---|
| G0a_SELFTEST | True | {} |
| G0b_ORACLE_SELF_AGREEMENT | True | {} |
| G0c_NULL_CALIBRATION | True | {"never_intervene_on_identifiable": 0, "random": 0.1875} |
| G1b_M3_ADVANTAGE_OVER_B5 | False | {"n": 48, "x_only": 0, "y_only": 1, "discordant": 1, "diff_x_minus_y": -0.020833333333333332, "wald_ci95": [-0.06123908071283736, 0.019572414046170692], "exact_p_two_sided": 1.0} |
| G1c_B5_ADVANTAGE_OVER_M3 | False | {} |
| G2_ANTI_ESCALATION_VS_B5 | True | {"M3_false_escalation": 0, "B5_false_escalation": 0, "M3_spec_damage": 0, "B5_spec_damage": 0} |
| G2b_OVER_ESCALATION_COUNT | None | {"M3": 0, "M2": 0, "M_V1": 0, "B5": 0, "M3_missed_escalation": 1, "M2_missed_escalation": 1, "B5_missed_escalation": 0, "note": "co-primary, reported in absolute counts; G2 gates on B5's harm"} |
| G5_LEVER_ATTRIBUTION | False | {"M3_minus_M2": {"n": 48, "x_only": 0, "y_only": 0, "discordant": 0, "diff_x_minus_y": 0.0, "wald_ci95": [0.0, 0.0], "exact_p_two_sided": 1.0}, "M3_only_correct": 0, "M2_only_correct": 0, "mechanism_rate_on_M3_only": null, "threshold_activity": {"instances_thr |
| G4_INTERFACE_LADDER | None | {"rates": {"B5_R1_VERDICT_ONLY": 0.7291666666666666, "B5_R2_PLUS_CANDIDATE_SET": 0.875, "B5_R3_PLUS_DISCRIMINATOR_TABLES": 0.9375, "B5_R4_PLUS_DISPOSITION_RECORDS": 0.9791666666666666, "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION": 1.0}, "monotone": true} |

Authority: grants nothing. `NO NOVELTY OR BREAKTHROUGH CLAIM`.
