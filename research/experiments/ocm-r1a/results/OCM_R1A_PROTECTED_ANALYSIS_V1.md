# OCM-R1A — PROTECTED analysis

Route: **PARENT_OWNED__CONTROLLER_BEATS_SEQUENTIAL_FEDERATION_BY_INTERACTION_TERM**

| class | worlds | M worst | B5 worst (order) | I | M mean | B5 mean | random mean | LB | worlds M<B5 / B5<M / tie | sign p |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|---:|
| LINEAR_F2^2 | 32 | 5 | 5 (B-first) | 0 | 5.000 | 5.000 | 5.100 | 5 | 0 / 0 / 32 | 1 |
| MONO_CONJ_2 | 32 | 5 | 5 (B-first) | 0 | 5.000 | 5.000 | 5.494 | 5 | 0 / 0 / 32 | 1 |
| LTF_2 | 224 | 8 | 8 (B-first) | 0 | 7.857 | 7.857 | 8.278 | 8 | 0 / 0 / 224 | 1 |
| SINGLETONS_4 | 64 | 7 | 7 (B-first) | 0 | 6.078 | 6.250 | 6.723 | 6 | 22 / 11 / 31 | 0.0801 |
| SINGLETONS_5 | 160 | 8 | 9 (B-first) | 1 | 7.438 | 7.800 | 8.140 | 8 | 84 / 42 / 34 | 0.00023 |
| SINGLETONS_6 | 384 | 10 | 11 (B-first) | 1 | 8.729 | 9.333 | 9.503 | 9 | 226 / 96 / 62 | 3.12e-13 |

| gate | pass | detail |
|---|---|---|
| G0a_KNOWN_ANSWER | True | {"registered": {"D_joint": 8, "B_first": 9, "Z_first": 9}, "observed": {"D_joint": 8, "B_first": 9, "Z_first": 9}} |
| G0b_SOLVERS_AGREE | True | {"classes_cross_checked": ["LINEAR_F2^2", "MONO_CONJ_2", "SINGLETONS_4"]} |
| G0c_PLANTED_MUTATION_FIRES | True | {"exact_cost": 11, "fired": true, "formula_cost": 12, "mutation": "M1_sequential_cost_formula"} |
| G0d_NO_ALARM_ON_DECOMPOSABLE | True | {"classes": {"LINEAR_F2^2": 0, "MONO_CONJ_2": 0, "LTF_2": 0, "SINGLETONS_4": 0}} |
| G1_CONTROLLER_BEATS_SEQUENTIAL_ON_REGISTERED_INSTANCE | True | {"interaction_term": 1} |
| G2_PARENT_OWNED_IDENTITY | True | {"note": "identity by containment (adaptive parent \u2287 joint learner); disclosed, never a comparator"} |
| G3_SINGLETONS_6_ATTEMPT | None | {"status": "OK", "interaction_term": 1, "reason": null, "note": "pre-registered attempt; CANNOT_CHECK on the time budget is a permitted outcome and is not a negative"} |
| G4_RANDOM_CONTROL_ABOVE_CONTROLLER | True | {} |

Authority: grants nothing — no field status, no novelty, no residual claim. `NO NOVELTY OR BREAKTHROUGH CLAIM`.
