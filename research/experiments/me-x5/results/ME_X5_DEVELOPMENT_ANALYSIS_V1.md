# ME-X5 analysis — DEVELOPMENT

**DEVELOPMENT split: not protected evidence. Nothing below supports a confirmatory claim.**

Results sha256 `79edc394b7a4ebf3aa9a86289f7fc3690604e4ceecf86fa626806554d01b4a6b`; custody sha256 `6568bbde8da9bc81107bb5bd3f8319c34e6f5f07d9b5f6af7a742912bf4afc9a`; instances 36.

## Decision-exact rate per mode (§6: reported per mode; a pooled average may not hide a mode failure)

| arm | FORMAL | MEASUREMENT | SYNTHESIS | POOLED | false trans. | unnec. abst. | auth. viol. | wall ms |
|---|---|---|---|---|---|---|---|---|
| B0_DIRECT_NATIVE_PIPELINE | 0.250 | 0.250 | 0.167 | 0.222 | 20 | 0 | 3 | 0.1 |
| B1_CALIBRATED_ABSTENTION | 0.250 | 0.250 | 0.167 | 0.222 | 20 | 0 | 3 | 0.1 |
| B2_PROVENANCE_VERIFIER_RUNTIME | 0.333 | 0.333 | 0.333 | 0.333 | 17 | 0 | 3 | 0.7 |
| B3_DIAGNOSIS_METAREASONING | 0.417 | 0.333 | 0.333 | 0.361 | 12 | 0 | 3 | 0.5 |
| B4_TMS_ASSURANCE_FEDERATION | 0.417 | 0.417 | 0.333 | 0.389 | 14 | 0 | 3 | 1.1 |
| B5_R1_VERDICT_ONLY | 0.917 | 0.833 | 0.833 | 0.861 | 0 | 0 | 0 | 2.2 |
| B5_R2_PROVENANCE | 0.917 | 0.833 | 0.917 | 0.889 | 0 | 0 | 0 | 2.3 |
| B5_R3_PLUS_DEPENDENCE_ANCESTRY | 0.917 | 0.833 | 0.917 | 0.889 | 0 | 0 | 0 | 2.2 |
| B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR | 1.000 | 0.917 | 0.917 | 0.944 | 0 | 0 | 0 | 2.0 |
| B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | 1.000 | 1.000 | 1.000 | 1.000 | 0 | 0 | 0 | 1.6 |
| M_ME_CROSS_TRANSITION_CONTROL | 1.000 | 1.000 | 1.000 | 1.000 | 0 | 0 | 0 | 1.0 |
| M_MINUS_IDENTITY | 0.917 | 0.833 | 0.917 | 0.889 | 3 | 0 | 0 | 0.7 |
| M_MINUS_APPARATUS | 0.917 | 0.917 | 0.917 | 0.917 | 3 | 0 | 0 | 0.7 |
| M_MINUS_EVALUATOR | 0.917 | 0.917 | 0.917 | 0.917 | 3 | 0 | 0 | 0.7 |
| M_MINUS_DEPENDENCE | 0.917 | 0.917 | 0.917 | 0.917 | 3 | 0 | 0 | 0.7 |
| M_MINUS_TRANSPORT | 0.833 | 0.833 | 0.917 | 0.861 | 3 | 0 | 0 | 0.7 |
| M_MINUS_SCOPE | 0.917 | 1.000 | 0.917 | 0.944 | 1 | 0 | 0 | 0.7 |
| M_MINUS_GLOBAL | 0.917 | 0.917 | 0.917 | 0.917 | 3 | 0 | 0 | 0.7 |
| M_MINUS_NUMERIC | 1.000 | 1.000 | 0.917 | 0.972 | 1 | 0 | 0 | 0.8 |
| M_MINUS_FAMILIES | 0.917 | 0.833 | 0.750 | 0.833 | 4 | 0 | 0 | 0.8 |
| M_MINUS_AUTHORITY | 0.917 | 0.917 | 0.917 | 0.917 | 0 | 0 | 3 | 0.7 |
| M_MINUS_UNRESOLVED | 0.917 | 0.917 | 0.917 | 0.917 | 0 | 0 | 0 | 0.6 |
| M_ABSTAIN_WHENEVER_CENSORED | 0.917 | 0.917 | 0.917 | 0.917 | 0 | 0 | 0 | 0.6 |
| C_ALWAYS_COMMIT | 0.167 | 0.167 | 0.167 | 0.167 | 25 | 0 | 0 | 0.0 |
| C_NEVER_COMMIT | 0.167 | 0.167 | 0.167 | 0.167 | 0 | 0 | 0 | 0.0 |
| C_ALWAYS_UNRESOLVED | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 33 | 0 | 0.0 |
| C_RANDOM_DECISION | 0.000 | 0.000 | 0.000 | 0.000 | 11 | 9 | 17 | 0.1 |

## Per-stratum decision-exact rate (pooled over modes)

| stratum | B0_DIRECT_NATIVE_PIPELINE | B1_CALIBRATED_ABSTENTION | B2_PROVENANCE_VERIFIER_RUNTIME | B3_DIAGNOSIS_METAREASONING | B4_TMS_ASSURANCE_FEDERATION | B5_R1_VERDICT_ONLY | B5_R2_PROVENANCE | B5_R3_PLUS_DEPENDENCE_ANCESTRY | B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | M_ME_CROSS_TRANSITION_CONTROL | M_MINUS_IDENTITY | M_MINUS_APPARATUS | M_MINUS_EVALUATOR | M_MINUS_DEPENDENCE | M_MINUS_TRANSPORT | M_MINUS_SCOPE | M_MINUS_GLOBAL | M_MINUS_NUMERIC | M_MINUS_FAMILIES | M_MINUS_AUTHORITY | M_MINUS_UNRESOLVED | M_ABSTAIN_WHENEVER_CENSORED | C_ALWAYS_COMMIT | C_NEVER_COMMIT | C_ALWAYS_UNRESOLVED | C_RANDOM_DECISION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TARGET_IDENTITY_DRIFT | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| APPARATUS_INVALID | 0.00 | 0.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| BLIND_EVALUATOR | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| HIDDEN_DEPENDENCE | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| INVALID_TRANSPORT | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| DEFEATED_SUPPORT | 0.67 | 0.67 | 0.67 | 0.00 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.67 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| SCOPE_OVERREACH | 0.00 | 0.00 | 0.00 | 0.33 | 0.00 | 0.33 | 0.33 | 0.33 | 0.33 | 1.00 | 1.00 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 1.00 | 1.00 | 0.33 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| LOCAL_COMPATIBILITY_GLOBAL_OBSTRUCTION | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| AUTHORITY_MISMATCH | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| CENSORED_UNRESOLVED | 0.00 | 0.00 | 0.33 | 0.00 | 0.00 | 0.00 | 0.33 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| FULLY_WARRANTED_CONTROL | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| SINGLE_PARENT_SUFFICIENT | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 |

## Gates

- **G0a_NATIVE_KNOWN_ANSWER**: pass=True — every parent passes its own native known-answer tests; the nine hand-authored fixtures and the H-EXT-3 separation pair are reproduced; the three native-review records are complete
- **G0b_ORACLE_VALIDITY**: pass=True — every instance: valid at v0, stratum invariant reproduced, censored facts within the frozen cap, decision invariant under a full relabelling of every element identifier
- **G0c_NULL_CALIBRATION**: pass=True — every truth-agnostic control <= 0.25 decision-exact; C_RANDOM_DECISION <= 0.05; M scored against within-mode shuffled oracle decisions is at least 0.50 below M's own rate in every mode
- **G1a_B5_REPRODUCES_M**: pass=True — M and B5 emit the identical decision on >= 99.5% of instances in every mode
- **G1b_M_ADVANTAGE_PER_MODE**: pass=[] — paired decision-exact difference M - B5 > 0 with an exact two-sided McNemar p surviving Holm correction across the three modes
- **G1c_B5_ADVANTAGE_PER_MODE**: pass=[] — the symmetric test: B5 strictly better than M in a mode, Holm-corrected
- **G2_ANTI_CONSERVATISM**: pass=True — on the negative-control strata M's manufactured doubt (false withholding, unnecessary abstention, missed warranted transitions) does not exceed B5's, in every mode
- **G3a_MECHANISM_ATTRIBUTION**: pass=None — each stratum with a claimed M advantage: the matching omission ablation's exact rate <= B5's on that stratum
- **G3b_CROSS_MODE_MECHANISM_IDENTIFIABILITY**: pass=False — protocol §7(1): at least one predeclared mechanism is load-bearing (Holm-corrected paired loss when omitted) in at least two native modes. Reported whether or not any residual over B5 exists.
- **G4_INTERFACE_LADDER**: pass=True — monotonicity: no rung k+1 significantly worse than rung k. The interface-standard terminal is a POSITIVE test, not the negation of the gap gate: it requires (i) monotonicity, (ii) rung 1 significantly worse than rung 5 (the interface information is demonstrably load-bearing) and (iii) a two-sided equivalence of M and B5 at full structure within the pre-registered margin, in every mode.
- **G5_CHANGED_VOCABULARY**: pass=True — one mode-blind rule set, written without ORION vocabulary and reading native fields through a per-mode adapter, recovers the responsibility class in >= 90% of decidable instances in every mode, while the same classifier scored against within-mode shuffled oracle labels stays <= 35% (evaluated only where a mode has at least 100 decidable instances; below that the null is reported NOT_ESTIMABLE, never passed). FORMAL SURROGATE ONLY: no independent native reviewer participated, so protocol §11 R2 is not grantable by this study.
- **COST**: pass=None — wall-clock ratio with a 2x flag; reported, never a route by itself

## Route

`PARENT_SUFFICIENT` — no M advantage over B5 in any native mode, and the positive interface-standard test does not fire.

Field-support ladder: `R1_BENCHMARK_INTEGRATION_VALUE`; R3 grantable: False; cross-mode mechanisms: []; cost: `COST_PARITY_WITHIN_2X`.


## Interface ladder, reported per mode (never pooled)

| mode | B5_R1_VERDICT_ONLY | B5_R2_PROVENANCE | B5_R3_PLUS_DEPENDENCE_ANCESTRY | B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR | B5_STRONGEST_FAITHFUL_PARENT_FEDERATION | significant steps | decisive rung |
|---|---|---|---|---|---|---|---|
| FORMAL | 0.917 | 0.917 | 0.917 | 1.000 | 1.000 | none | none |
| MEASUREMENT | 0.833 | 0.833 | 0.833 | 0.917 | 1.000 | none | none |
| SYNTHESIS | 0.833 | 0.917 | 0.917 | 0.917 | 1.000 | none | none |

Decisive rung varies across modes: **False**.
