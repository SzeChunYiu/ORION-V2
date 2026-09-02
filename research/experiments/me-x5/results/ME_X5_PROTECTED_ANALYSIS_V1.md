# ME-X5 analysis — PROTECTED

Results sha256 `4bdad48135334844ab12578dc61046081b51a6b8244637e79d198d8a9aac6b91`; custody sha256 `f35428b4044c5452fa7eb8ec78739ccff6e608f6b081281b051c444273f12200`; instances 1440.

## Decision-exact rate per mode (§6: reported per mode; a pooled average may not hide a mode failure)

| arm | FORMAL | MEASUREMENT | SYNTHESIS | POOLED | false trans. | unnec. abst. | auth. viol. | wall ms |
|---|---|---|---|---|---|---|---|---|
| B0_DIRECT_NATIVE_PIPELINE | 0.250 | 0.219 | 0.198 | 0.222 | 800 | 0 | 120 | 2.5 |
| B1_CALIBRATED_ABSTENTION | 0.250 | 0.219 | 0.198 | 0.222 | 800 | 0 | 120 | 3.8 |
| B2_PROVENANCE_VERIFIER_RUNTIME | 0.344 | 0.312 | 0.296 | 0.317 | 680 | 0 | 120 | 22.2 |
| B3_DIAGNOSIS_METAREASONING | 0.365 | 0.350 | 0.369 | 0.361 | 480 | 0 | 120 | 16.9 |
| B4_TMS_ASSURANCE_FEDERATION | 0.417 | 0.385 | 0.365 | 0.389 | 560 | 0 | 120 | 40.2 |
| B5_R1_VERDICT_ONLY | 0.865 | 0.850 | 0.869 | 0.861 | 0 | 0 | 0 | 74.4 |
| B5_R2_PROVENANCE | 0.875 | 0.860 | 0.883 | 0.873 | 0 | 0 | 0 | 77.0 |
| B5_R3_PLUS_DEPENDENCE_ANCESTRY | 0.890 | 0.883 | 0.898 | 0.890 | 0 | 0 | 0 | 65.8 |
| B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR | 0.948 | 0.933 | 0.952 | 0.944 | 0 | 0 | 0 | 65.4 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 1.000 | 1.000 | 1.000 | 1.000 | 0 | 0 | 0 | 72.2 |
| M_ME_CROSS_TRANSITION_CONTROL | 1.000 | 1.000 | 1.000 | 1.000 | 0 | 0 | 0 | 41.1 |
| M_MINUS_IDENTITY | 0.917 | 0.881 | 0.917 | 0.905 | 120 | 0 | 0 | 34.6 |
| M_MINUS_APPARATUS | 0.896 | 0.890 | 0.896 | 0.894 | 120 | 0 | 0 | 34.4 |
| M_MINUS_EVALUATOR | 0.892 | 0.902 | 0.896 | 0.897 | 120 | 0 | 0 | 34.0 |
| M_MINUS_DEPENDENCE | 0.902 | 0.894 | 0.902 | 0.899 | 120 | 0 | 0 | 31.9 |
| M_MINUS_TRANSPORT | 0.904 | 0.908 | 0.904 | 0.906 | 120 | 0 | 0 | 32.9 |
| M_MINUS_SCOPE | 0.917 | 0.952 | 0.917 | 0.928 | 40 | 0 | 0 | 31.7 |
| M_MINUS_GLOBAL | 0.917 | 0.917 | 0.917 | 0.917 | 120 | 0 | 0 | 32.8 |
| M_MINUS_NUMERIC | 1.000 | 0.969 | 0.948 | 0.972 | 40 | 0 | 0 | 30.2 |
| M_MINUS_FAMILIES | 0.850 | 0.796 | 0.802 | 0.816 | 160 | 0 | 0 | 32.5 |
| M_MINUS_AUTHORITY | 0.917 | 0.917 | 0.917 | 0.917 | 0 | 0 | 120 | 33.0 |
| M_MINUS_UNRESOLVED | 0.917 | 0.917 | 0.917 | 0.917 | 0 | 0 | 0 | 20.7 |
| M_ABSTAIN_WHENEVER_CENSORED | 0.917 | 0.917 | 0.917 | 0.917 | 0 | 0 | 0 | 19.7 |
| C_ALWAYS_COMMIT | 0.167 | 0.167 | 0.167 | 0.167 | 1000 | 0 | 0 | 0.5 |
| C_NEVER_COMMIT | 0.167 | 0.167 | 0.167 | 0.167 | 0 | 0 | 0 | 0.4 |
| C_ALWAYS_UNRESOLVED | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 1320 | 0 | 0.4 |
| C_RANDOM_DECISION | 0.019 | 0.017 | 0.015 | 0.017 | 495 | 306 | 725 | 2.4 |

## Per-stratum decision-exact rate (pooled over modes)

| stratum | B0_DIRECT_NATIVE_PIPELINE | B1_CALIBRATED_ABSTENTION | B2_PROVENANCE_VERIFIER_RUNTIME | B3_DIAGNOSIS_METAREASONING | B4_TMS_ASSURANCE_FEDERATION | B5_R1_VERDICT_ONLY | B5_R2_PROVENANCE | B5_R3_PLUS_DEPENDENCE_ANCESTRY | B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | M_ME_CROSS_TRANSITION_CONTROL | M_MINUS_IDENTITY | M_MINUS_APPARATUS | M_MINUS_EVALUATOR | M_MINUS_DEPENDENCE | M_MINUS_TRANSPORT | M_MINUS_SCOPE | M_MINUS_GLOBAL | M_MINUS_NUMERIC | M_MINUS_FAMILIES | M_MINUS_AUTHORITY | M_MINUS_UNRESOLVED | M_ABSTAIN_WHENEVER_CENSORED | C_ALWAYS_COMMIT | C_NEVER_COMMIT | C_ALWAYS_UNRESOLVED | C_RANDOM_DECISION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TARGET_IDENTITY_DRIFT | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.04 |
| APPARATUS_INVALID | 0.00 | 0.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.02 |
| BLIND_EVALUATOR | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HIDDEN_DEPENDENCE | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.01 |
| INVALID_TRANSPORT | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.02 |
| DEFEATED_SUPPORT | 0.67 | 0.67 | 0.67 | 0.00 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.67 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.03 |
| SCOPE_OVERREACH | 0.00 | 0.00 | 0.00 | 0.33 | 0.00 | 0.33 | 0.33 | 0.33 | 0.33 | 1.00 | 1.00 | 0.86 | 1.00 | 1.00 | 1.00 | 1.00 | 0.14 | 1.00 | 1.00 | 0.33 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.03 |
| LOCAL_COMPATIBILITY_GLOBAL_OBSTRUCTION | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.03 |
| AUTHORITY_MISMATCH | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.01 |
| CENSORED_UNRESOLVED | 0.00 | 0.00 | 0.14 | 0.00 | 0.00 | 0.00 | 0.14 | 0.35 | 1.00 | 1.00 | 1.00 | 1.00 | 0.72 | 0.76 | 0.79 | 0.87 | 1.00 | 1.00 | 1.00 | 0.79 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| FULLY_WARRANTED_CONTROL | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| SINGLE_PARENT_SUFFICIENT | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.02 |

## Gates

- **G0a_NATIVE_KNOWN_ANSWER**: pass=True — every parent passes its own native known-answer tests; the nine hand-authored fixtures and the H-EXT-3 separation pair are reproduced; the three native-review records are complete
- **G0b_ORACLE_VALIDITY**: pass=True — every instance: valid at v0, stratum invariant reproduced, censored facts within the frozen cap, decision invariant under a full relabelling of every element identifier
- **G0c_NULL_CALIBRATION**: pass=True — every truth-agnostic control <= 0.25 decision-exact; C_RANDOM_DECISION <= 0.05; M scored against within-mode shuffled oracle decisions is at least 0.50 below M's own rate in every mode
- **G1a_B5_REPRODUCES_M**: pass=True — M and B5 emit the identical decision on >= 99.5% of instances in every mode
- **G1b_M_ADVANTAGE_PER_MODE**: pass=[] — paired decision-exact difference M - B5 > 0 with an exact two-sided McNemar p surviving Holm correction across the three modes
- **G1c_B5_ADVANTAGE_PER_MODE**: pass=[] — the symmetric test: B5 strictly better than M in a mode, Holm-corrected
- **G2_ANTI_CONSERVATISM**: pass=True — on the negative-control strata M's manufactured doubt (false withholding, unnecessary abstention, missed warranted transitions) does not exceed B5's, in every mode
- **G3a_MECHANISM_ATTRIBUTION**: pass=None — each stratum with a claimed M advantage: the matching omission ablation's exact rate <= B5's on that stratum
- **G3b_CROSS_MODE_MECHANISM_IDENTIFIABILITY**: pass=True — protocol §7(1): at least one predeclared mechanism is load-bearing (Holm-corrected paired loss when omitted) in at least two native modes. Reported whether or not any residual over B5 exists.
- **G4_INTERFACE_LADDER**: pass=True — monotonicity: no rung k+1 significantly worse than rung k. The interface-standard terminal is a POSITIVE test, not the negation of the gap gate: it requires (i) monotonicity, (ii) rung 1 significantly worse than rung 5 (the interface information is demonstrably load-bearing) and (iii) a two-sided equivalence of M and B5 at full structure within the pre-registered margin, in every mode.
- **G5_CHANGED_VOCABULARY**: pass=True — one mode-blind rule set, written without ORION vocabulary and reading native fields through a per-mode adapter, recovers the responsibility class in >= 90% of decidable instances in every mode, while the same classifier scored against within-mode shuffled oracle labels stays <= 35% (evaluated only where a mode has at least 100 decidable instances; below that the null is reported NOT_ESTIMABLE, never passed). FORMAL SURROGATE ONLY: no independent native reviewer participated, so protocol §11 R2 is not grantable by this study.
- **COST**: pass=None — wall-clock ratio with a 2x flag; reported, never a route by itself

## Route

`RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL` — no gap at full structure (equivalence established within the pre-registered margin) while the interface information is demonstrably load-bearing across the ladder in every mode.

Field-support ladder: `R1_BENCHMARK_INTEGRATION_VALUE`; R3 grantable: False; cross-mode mechanisms: ['M_MINUS_IDENTITY', 'M_MINUS_APPARATUS', 'M_MINUS_EVALUATOR', 'M_MINUS_DEPENDENCE', 'M_MINUS_TRANSPORT', 'M_MINUS_SCOPE', 'M_MINUS_GLOBAL', 'M_MINUS_NUMERIC', 'M_MINUS_FAMILIES', 'M_MINUS_AUTHORITY', 'M_MINUS_UNRESOLVED']; cost: `COST_PARITY_WITHIN_2X`.


## Interface ladder, reported per mode (never pooled)

| mode | B5_R1_VERDICT_ONLY | B5_R2_PROVENANCE | B5_R3_PLUS_DEPENDENCE_ANCESTRY | B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | significant steps | decisive rung |
|---|---|---|---|---|---|---|---|
| FORMAL | 0.865 | 0.875 | 0.890 | 0.948 | 1.000 | PRO→PLU, PLU→PLU, PLU→ONG | B5_R3_PLUS_DEPENDENCE_ANCESTRY->B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR |
| MEASUREMENT | 0.850 | 0.860 | 0.883 | 0.933 | 1.000 | PRO→PLU, PLU→PLU, PLU→ONG | B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR->B5_STRONGEST_FAITHFUL_PARENT_FEDERATION |
| SYNTHESIS | 0.869 | 0.883 | 0.898 | 0.952 | 1.000 | VER→PRO, PRO→PLU, PLU→PLU, PLU→ONG | B5_R3_PLUS_DEPENDENCE_ANCESTRY->B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR |

Decisive rung varies across modes: **True**.
