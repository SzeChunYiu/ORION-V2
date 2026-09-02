# ME-X5 — Parent Fidelity, Native Review and Development Split (Receipt V1)

Companion to `ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_EXACT_STUDY_DESIGN_V1.{md,json}`. **No protected outcome exists.** 
Every number below is from the public development seed `ME-X5-DEV-20260902` or the public dry-run seed `ME-X5-PUBLIC-DRYRUN-NOT-PROTECTED`, and is development evidence only.

## 1. Code and design hashes (sha256)

| file | sha256 |
|---|---|
| `mex5_model.py` | `f63ec0df71787c16ebcd5f726bc0c91d6cf96ce58980dbf66bb7bdbb2c985bcb` |
| `mex5_native_formal.py` | `5a599dd156ec8a430ebb568be058c980d7fd119aa97f207d72d0ac2020f405a9` |
| `mex5_native_measurement.py` | `4be419e11099bc05afe8bebe083be2e192a4e9f21b0d03280f2908fb3443ec84` |
| `mex5_native_synthesis.py` | `93a249119e2c6f5729115b3290bc4abc22a1c60791d32293fbafc42b2836e6a5` |
| `mex5_oracle.py` | `6db93074a2aa4c480f47444211c95fe0f9cfc17a9a94c0ab3f215d59ff191f4e` |
| `mex5_generator.py` | `2abf1c117786057e04b421056ddfa665b2800984dd08fa86bb8664471e209412` |
| `mex5_parents.py` | `f96814a0c0db4f60e12b4adce83b7c386f28c877d30c050459be46e60efdd0f4` |
| `mex5_arms.py` | `d255edf95ac94ed1dcdf18e885e2e6569c32e73bc4079a3508889881bd84c4ba` |
| `mex5_vocab.py` | `0c5e1a3b49a981b232c50290df50a950d8b5f8ba67c3aac32be640b1662d28f2` |
| `mex5_run.py` | `e7bb3fe1252a0924ee2be1731d9cd4c04a84bdbd6c3daacfd44c8fcd8a9df299` |
| `ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_EXACT_STUDY_DESIGN_V1.md` | `99834e888bc1de3df7120c7c70c867422354e67727d0100445a6be40335616d4` |
| `ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_EXACT_STUDY_DESIGN_V1.json` | `d8c765dbfc58ac3687e380f1a34528badb59b5e6ff33a8abfbb6dbdc575eb416` |

Protected seed commitment (design §3.6): `132c47826e40f57dfd873848a82d160e2f0de114827b1155c015dce60b19467a`; 
custody `~/.orion-custody/me-x5/PROTECTED_SEED_V1.txt` (mode 600). The seed value is not in the repository and is revealed only in the outcome receipt.

## 2. Parent fidelity (G0a): every baseline passes its own native known-answer test

No baseline may be used before it reproduces its own native semantics; a strawman baseline would make any residual meaningless.

| parent | test | result |
|---|---|---|
| `PROVENANCE_REVOCATION` | revocation descendants reach exactly the derived family | PASS — defeated=['F1'] |
| `TMS_SELECTIVE_REOPENING` | an alternative support family preserves the commitment | PASS — surviving=['F2'] |
| `TMS_SELECTIVE_REOPENING` | losing every family reopens the commitment | PASS |
| `DEPENDENCE_ASSESSMENT` | shared confirmed ancestry defeats a k=2 family | PASS |
| `DEPENDENCE_ASSESSMENT` | the same ancestry leaves a k=1 family standing | PASS |
| `DEPENDENCE_ASSESSMENT` | suspected ancestry censors rather than defeats | PASS |
| `TYPED_TRANSPORT` | a ported lemma needs an isomorphism, not a mere embedding | PASS |
| `TYPED_TRANSPORT` | an isomorphism licenses the reuse | PASS |
| `TYPED_TRANSPORT` | an unchecked morphism censors | PASS |
| `TYPED_TRANSPORT` | ranks follow the parent-owned RelationType order | PASS |
| `EVALUATOR_COVERAGE_CONTRACT` | a checker blind to the asserted class defeats every family that uses it | PASS |
| `EVALUATOR_COVERAGE_CONTRACT` | uncertain coverage censors rather than defeats | PASS |
| `APPARATUS_VALIDITY` | a calibration is valid inside its range | PASS |
| `APPARATUS_VALIDITY` | and invalid outside it, with nothing else changed | PASS |
| `UNCERTAINTY_AGGREGATION` | a fully correlated systematic does not shrink with more channels | PASS — sigma_correlated=1.0000 |
| `UNCERTAINTY_AGGREGATION` | independent systematics do shrink | PASS — sigma_uncorrelated=0.7071 |
| `EVIDENCE_SYNTHESIS_POOLING` | two reports of one cohort give the precision of one study | PASS — sigma_dup=0.2000 |
| `EVIDENCE_SYNTHESIS_POOLING` | two genuine cohorts give more precision | PASS — sigma_ind=0.1414 |
| `SCOPE_BOOKKEEPING` | a registered scope no artefact covers defeats every family | PASS |
| `ASSURANCE_GLOBAL_WITNESS` | pairwise agreement without the gluing witness is an obstruction | PASS |

**20/20 pass.**

## 3. Hand-authored known-answer fixtures (G0a)

Nine episodes, three per mode, whose correct decision is written by hand in `mex5_generator.known_answer_fixtures`. They exercise the shell's corners: a partial family failure that must **not** defeat the target; a censored fact that must **not** produce `UNRESOLVED`; the narrowing route.

| fixture | expected | oracle | result |
|---|---|---|---|
| `KA-a-FORMAL-PARTIAL_FAILURE_DOES_NOT_DEFEAT` | COMMIT/NONE/BELIEF_ONLY | COMMIT/NONE/BELIEF_ONLY | PASS |
| `KA-b-FORMAL-CENSORING_THAT_CANNOT_FLIP_THE_DECISION` | COMMIT/NONE/BELIEF_ONLY | COMMIT/NONE/BELIEF_ONLY | PASS |
| `KA-c-FORMAL-NARROWED_COMMITMENT` | COMMIT_NARROWED/SCOPE/BELIEF_ONLY | COMMIT_NARROWED/SCOPE/BELIEF_ONLY | PASS |
| `KA-a-MEASUREMENT-PARTIAL_FAILURE_DOES_NOT_DEFEAT` | COMMIT/NONE/BELIEF_ONLY | COMMIT/NONE/BELIEF_ONLY | PASS |
| `KA-b-MEASUREMENT-CENSORING_THAT_CANNOT_FLIP_THE_DECISION` | COMMIT/NONE/BELIEF_ONLY | COMMIT/NONE/BELIEF_ONLY | PASS |
| `KA-c-MEASUREMENT-NARROWED_COMMITMENT` | COMMIT_NARROWED/SCOPE/BELIEF_ONLY | COMMIT_NARROWED/SCOPE/BELIEF_ONLY | PASS |
| `KA-a-SYNTHESIS-PARTIAL_FAILURE_DOES_NOT_DEFEAT` | COMMIT/NONE/BELIEF_ONLY | COMMIT/NONE/BELIEF_ONLY | PASS |
| `KA-b-SYNTHESIS-CENSORING_THAT_CANNOT_FLIP_THE_DECISION` | COMMIT/NONE/BELIEF_ONLY | COMMIT/NONE/BELIEF_ONLY | PASS |
| `KA-c-SYNTHESIS-NARROWED_COMMITMENT` | COMMIT_NARROWED/SCOPE/BELIEF_ONLY | COMMIT_NARROWED/SCOPE/BELIEF_ONLY | PASS |

## 4. H-EXT-3 finite separation pair

| case | oracle | `B5_R1_VERDICT_ONLY` | `B5` (rung 5) | `M` |
|---|---|---|---|---|
| SEP-P | WITHHOLD/TRANSPORT | WITHHOLD/DEPENDENCE | WITHHOLD/TRANSPORT | WITHHOLD/TRANSPORT |
| SEP-Q | COMMIT/NONE | WITHHOLD/DEPENDENCE | COMMIT/NONE | COMMIT/NONE |

Verdict-only outputs identical on P and Q: **True**; it errs on at least one: **True**; witness-level exchange exact on both: **True**. 
This is the finite-information separation H-EXT-3 asks for, and the only separation this design can exhibit (design §10.3).

## 5. Native-domain ownership records (protocol §3)

| mode | record complete | independent reviewer |
|---|---|---|
| `FORMAL` | True | **no** |
| `MEASUREMENT` | True | **no** |
| `SYNTHESIS` | True | **no** |

The reviewer is the study author. Protocol §8's independent changed-vocabulary reviewer and §11's independent adjudication are **not** satisfied; `R2_EMERGING_INTERDISCIPLINARY_RESIDUAL` is therefore not grantable by this study (design §0, §10.2). Each record names which ME abstractions the mode considers lossy, redundant or invalid — for example the formal mode records that the numeric aggregation layer has no deductive counterpart, and the measurement mode records that treating a discovered dependence as a *defeat* misdescribes what physics does with a correlated systematic.

## 6. Oracle validity on the public selftest split (G0b)

36 instances (one per mode × stratum): valid at v0 36/36; stratum invariant reproduced 36/36; decision invariant under a full relabelling of every element identifier 36/36; censored facts within the frozen cap 36/36.

## 7. Development split (36 instances, public seed) — not protected evidence

| arm | FORMAL | MEASUREMENT | SYNTHESIS | POOLED |
|---|---|---|---|---|
| `B0_DIRECT_NATIVE_PIPELINE` | 0.250 | 0.250 | 0.167 | 0.222 |
| `B1_CALIBRATED_ABSTENTION` | 0.250 | 0.250 | 0.167 | 0.222 |
| `B2_PROVENANCE_VERIFIER_RUNTIME` | 0.333 | 0.333 | 0.333 | 0.333 |
| `B3_DIAGNOSIS_METAREASONING` | 0.417 | 0.333 | 0.333 | 0.361 |
| `B4_TMS_ASSURANCE_FEDERATION` | 0.417 | 0.417 | 0.333 | 0.389 |
| `B5_R1_VERDICT_ONLY` | 0.917 | 0.833 | 0.833 | 0.861 |
| `B5_R2_PROVENANCE` | 0.917 | 0.833 | 0.917 | 0.889 |
| `B5_R3_PLUS_DEPENDENCE_ANCESTRY` | 0.917 | 0.833 | 0.917 | 0.889 |
| `B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR` | 1.000 | 0.917 | 0.917 | 0.944 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 1.000 | 1.000 | 1.000 | 1.000 |
| `C_ALWAYS_COMMIT` | 0.167 | 0.167 | 0.167 | 0.167 |
| `C_ALWAYS_UNRESOLVED` | 0.000 | 0.000 | 0.000 | 0.000 |
| `C_NEVER_COMMIT` | 0.167 | 0.167 | 0.167 | 0.167 |
| `C_RANDOM_DECISION` | 0.000 | 0.000 | 0.000 | 0.000 |
| `M_ABSTAIN_WHENEVER_CENSORED` | 0.917 | 0.917 | 0.917 | 0.917 |
| `M_ME_CROSS_TRANSITION_CONTROL` | 1.000 | 1.000 | 1.000 | 1.000 |
| `M_MINUS_APPARATUS` | 0.917 | 0.917 | 0.917 | 0.917 |
| `M_MINUS_AUTHORITY` | 0.917 | 0.917 | 0.917 | 0.917 |
| `M_MINUS_DEPENDENCE` | 0.917 | 0.917 | 0.917 | 0.917 |
| `M_MINUS_EVALUATOR` | 0.917 | 0.917 | 0.917 | 0.917 |
| `M_MINUS_FAMILIES` | 0.917 | 0.833 | 0.750 | 0.833 |
| `M_MINUS_GLOBAL` | 0.917 | 0.917 | 0.917 | 0.917 |
| `M_MINUS_IDENTITY` | 0.917 | 0.833 | 0.917 | 0.889 |
| `M_MINUS_NUMERIC` | 1.000 | 1.000 | 0.917 | 0.972 |
| `M_MINUS_SCOPE` | 0.917 | 1.000 | 0.917 | 0.944 |
| `M_MINUS_TRANSPORT` | 0.833 | 0.833 | 0.917 | 0.861 |
| `M_MINUS_UNRESOLVED` | 0.917 | 0.917 | 0.917 | 0.917 |

Development route: `PARENT_SUFFICIENT`.

## 8. Full-scale public dry run (design §8.3) — development evidence, not protected

Run on the public seed `ME-X5-PUBLIC-DRYRUN-NOT-PROTECTED` at the protected scale (1 440 instances) to verify runtime and that the gates are estimable at n = 480 per mode. **No design constant, gate, threshold, margin, arm, oracle rule, stratum or seed was changed after it.** The protected split uses a different, committed seed.

| arm | FORMAL | MEASUREMENT | SYNTHESIS | POOLED |
|---|---|---|---|---|
| `B0_DIRECT_NATIVE_PIPELINE` | 0.2500 | 0.2042 | 0.2125 | 0.2222 |
| `B1_CALIBRATED_ABSTENTION` | 0.2500 | 0.2042 | 0.2125 | 0.2222 |
| `B2_PROVENANCE_VERIFIER_RUNTIME` | 0.3458 | 0.3021 | 0.3104 | 0.3194 |
| `B3_DIAGNOSIS_METAREASONING` | 0.3625 | 0.3542 | 0.3563 | 0.3576 |
| `B4_TMS_ASSURANCE_FEDERATION` | 0.4167 | 0.3708 | 0.3792 | 0.3889 |
| `B5_R1_VERDICT_ONLY` | 0.8625 | 0.8542 | 0.8562 | 0.8576 |
| `B5_R2_PROVENANCE` | 0.8750 | 0.8688 | 0.8708 | 0.8715 |
| `B5_R3_PLUS_DEPENDENCE_ANCESTRY` | 0.8854 | 0.8792 | 0.8833 | 0.8826 |
| `B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR` | 0.9458 | 0.9375 | 0.9396 | 0.9410 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `M_ME_CROSS_TRANSITION_CONTROL` | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `M_MINUS_IDENTITY` | 0.9167 | 0.8833 | 0.9167 | 0.9056 |
| `M_MINUS_APPARATUS` | 0.9000 | 0.9083 | 0.8958 | 0.9014 |
| `M_MINUS_EVALUATOR` | 0.8938 | 0.8896 | 0.8979 | 0.8938 |
| `M_MINUS_DEPENDENCE` | 0.9062 | 0.9062 | 0.9042 | 0.9056 |
| `M_MINUS_TRANSPORT` | 0.8958 | 0.8938 | 0.9000 | 0.8965 |
| `M_MINUS_SCOPE` | 0.9167 | 0.9500 | 0.9167 | 0.9278 |
| `M_MINUS_GLOBAL` | 0.9167 | 0.9167 | 0.9167 | 0.9167 |
| `M_MINUS_NUMERIC` | 1.0000 | 0.9542 | 0.9625 | 0.9722 |
| `M_MINUS_FAMILIES` | 0.8521 | 0.7979 | 0.8063 | 0.8187 |
| `M_MINUS_AUTHORITY` | 0.9167 | 0.9167 | 0.9167 | 0.9167 |
| `M_MINUS_UNRESOLVED` | 0.9167 | 0.9167 | 0.9167 | 0.9167 |
| `M_ABSTAIN_WHENEVER_CENSORED` | 0.9167 | 0.9167 | 0.9167 | 0.9167 |
| `C_ALWAYS_COMMIT` | 0.1667 | 0.1667 | 0.1667 | 0.1667 |
| `C_NEVER_COMMIT` | 0.1667 | 0.1667 | 0.1667 | 0.1667 |
| `C_ALWAYS_UNRESOLVED` | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `C_RANDOM_DECISION` | 0.0104 | 0.0250 | 0.0187 | 0.0181 |

### Interface ladder on the dry run, per mode (never pooled)

| mode | R1_VERDICT_ONLY | R2_PROVENANCE | R3_PLUS_DEPENDENCE_ANCESTRY | R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR | STRONGEST_FAITHFUL_PARENT_FEDERATION | significant steps | decisive rung |
|---|---|---|---|---|---|---|---|
| `FORMAL` | 0.8625 | 0.8750 | 0.8854 | 0.9458 | 1.0000 | R11->R22, R33->R44, R44->5 | R3_PLUS_DEPENDENCE_ANCESTRY->R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR |
| `MEASUREMENT` | 0.8542 | 0.8688 | 0.8792 | 0.9375 | 1.0000 | R11->R22, R33->R44, R44->5 | R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR->STRONGEST_FAITHFUL_PARENT_FEDERATION |
| `SYNTHESIS` | 0.8562 | 0.8708 | 0.8833 | 0.9396 | 1.0000 | R11->R22, R22->R33, R33->R44, R44->5 | R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR->STRONGEST_FAITHFUL_PARENT_FEDERATION |

Decisive rung varies across modes: **True**. Reported per mode by design; ME-X1's single significant step was at R4→R5 and ME-X4's were at R1→R2 and R3→R4, so the decisive rung is *generator*-dependent. X5 holds the generator fixed and varies only the native semantics (design §10.5).

### Changed-vocabulary recovery on the dry run (G5)

| mode | decidable n | native-adapter recovery | shuffled-label null | scrambled-adapter (diagnostic) |
|---|---|---|---|---|
| `FORMAL` | 440 | 1.0000 | 0.1159 | 0.0909 |
| `MEASUREMENT` | 440 | 0.9636 | 0.1432 | 0.8636 |
| `SYNTHESIS` | 440 | 1.0000 | 0.1409 | 0.9091 |

The scrambled-adapter column is a **diagnostic, not a gate**: the measurement and synthesis adapters read the native surfaces similarly enough that swapping them barely degrades recovery, while swapping in the formal adapter does. The gate's null is the shuffled-label null.

### Dry-run route

```text
ROUTE = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL
FIELD_SUPPORT_LADDER = R1_BENCHMARK_INTEGRATION_VALUE
CROSS_MODE_MECHANISMS = 11 of 11 ablations load-bearing in >= 2 modes
COST_FLAG = COST_PARITY_WITHIN_2X
```

## 9. Protected-run guard

`PROTECTED_RUN_AUTHORIZATION.json` is **absent** from this PR; `mex5_run.py protected` exits 3 without it, exits 3 on a wrong `acknowledged_design_sha256`, and exits 4 on a seed whose sha256 does not match the frozen commitment — all three refusal paths are asserted by `tests/unit/test_me_x5_cross_domain_study.py`, which also asserts that no arm imports the oracle decision procedure.
