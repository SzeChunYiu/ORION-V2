# ME-X5 — Cross-Domain Field Residual across Three Native Epistemic Modes: Protected-Run Outcome Receipt (V1)

**Design:** `ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_EXACT_STUDY_DESIGN_V1.{md,json}` (PR #177, main `a5ee8a6`), design-JSON sha256 `d8c765dbfc58ac3687e380f1a34528badb59b5e6ff33a8abfbb6dbdc575eb416`.

**Authorization:** operator, in chat, 2026-09-02, verbatim *"run all the computation tasks.. finish all the researxh asap"*, relayed to this lane as coordinator authorization and recorded in `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` (sha256 `279194c75676d911cd42ef0df16058dda14651e1e1d0b16dd2877c397059c60d`; carries the design sha256, the seed commitment and the main sha `a5ee8a609e69578e2df088d04b0268ce87ecdebc`). The same instruction is the primary record for the sibling ME-X1, ME-X2 and ME-X4 protected runs. The file was archived under a new name immediately after the run so the runner's guard is re-armed and the unit test asserting the refusal path continues to hold; a second protected run requires a new explicit authorization.

**Run:** Mac (local), 2026-09-02, `python3.12 mex5_run.py protected --out results` from the merged tree, **executed exactly once**, exit 0, 1.6 s for 1 440 instances × 27 arms. The runner verified sha256(custody seed) = the frozen commitment `132c47826e40f57dfd873848a82d160e2f0de114827b1155c015dce60b19467a` before generating; `analyze` ran once inside the same invocation. Every code file hashed identical to the parent-fidelity receipt table before the run. **No post-outcome change to any design constant, gate, threshold, margin, arm policy, oracle rule, generator rule or seed.**

**Seed reveal (design §3.6):** `ME-X5-PROTECTED-20366f5147a609093bb7f6edecd1c4d03be2dd4a250461a0` — sha256 equals the commitment above; the 1 440-instance split regenerates byte-for-byte from it.

**Artifacts (sha256):** results `4bdad48135334844ab12578dc61046081b51a6b8244637e79d198d8a9aac6b91`; expected-custody `f35428b4044c5452fa7eb8ec78739ccff6e608f6b081281b051c444273f12200`; timing `5eee91ef9336025ad82d859f6a248c5c8474cae30f1d1183ba3537a3363fad23`; analysis json `277bcfbfb642c85039e49ef8500fc3cd96946af4ee14d710cc5dc2130324670e`, md `035b18f92a706524b0c74b4e6d93f3a3c136901e3b7820089340bb5533c7fb98`; selftest report (G0a/G0b source) `3348d22e4f21ad8615d2b8f2689a91d83cec61affb54089350bbcc7c95c34014`.

## 1. Terminal

```text
ME_X5_STATUS              = EXECUTED_PROTECTED
ROUTE                     = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL
                            (by the POSITIVE test of design §6.5, in every mode)
FIELD_SUPPORT_LADDER      = R1_BENCHMARK_INTEGRATION_VALUE
R2_EMERGING_RESIDUAL      = NOT_GRANTABLE_INDEPENDENT_ADJUDICATION_ABSENT
R3_ESTABLISHED_FIELD      = NOT_GRANTABLE_BY_ANY_EXPERIMENT
PRIMARY_ENDPOINT          = decision triple (action, responsibility locus, authority)
M  decision-exact         = 1.0000 / 1.0000 / 1.0000   (FORMAL / MEASUREMENT / SYNTHESIS)
B5 decision-exact         = 1.0000 / 1.0000 / 1.0000
PAIRED DISCORDANCE        = 0 in every mode; 95% CI [0.0000, 0.0000] within the +-0.02 margin
DECISION IDENTITY M vs B5 = 1.000 in every mode
CROSS_MODE_MECHANISMS     = 11 of 11 ablations load-bearing in >= 2 native modes
DECISIVE LADDER RUNG      = FORMAL R3->R4 | MEASUREMENT R4->R5 | SYNTHESIS R3->R4  (varies)
COST_FLAG                 = COST_PARITY_WITHIN_2X (B5 72.2 ms vs M 41.1 ms wall)
PRIMARY_COMPARATOR        = B5_STRONGEST_FAITHFUL_PARENT_FEDERATION
FIELD_STATUS_AUTHORITY    = NONE
```

**The strongest faithful parent federation reproduces every decision M makes, in all three native epistemic modes, with zero discordant instances out of 1 440.** This is the fourth `PARENT_SUFFICIENT`-class terminal of the hardening wave and it was the pre-registered expectation (design §1.2). It is reported here in its interface-standard form because the *positive* test of §6.5 fired — see §5 for why that is a weaker statement than it sounds.

## 2. Gates (frozen pre-outcome; every number from `results/ME_X5_PROTECTED_ANALYSIS_V1.json`)

| gate | verdict | numbers |
|---|---|---|
| **G0a NATIVE_KNOWN_ANSWER** (hard) | **PASS** | parents 20/20 native tests; 9/9 hand-authored fixtures reproduced; separation pair as designed; 3/3 native-review records complete |
| **G0b ORACLE_VALIDITY** (hard) | **PASS** | 36/36 selftest instances valid at v0, stratum invariant reproduced, censored facts within the cap, decision invariant under a full relabelling of every element identifier |
| **G0c NULL_CALIBRATION** (hard) | **PASS** | `C_ALWAYS_COMMIT` 0.167, `C_NEVER_COMMIT` 0.167, `C_ALWAYS_UNRESOLVED` 0.000, `C_RANDOM_DECISION` 0.0167 (rule ≤ 0.05); M against within-mode shuffled oracle decisions 0.081 / 0.113 / 0.092 against its own 1.000 (rule ≥ 0.50 below) |
| **G1a B5_REPRODUCES_M** | **PASS** | decision identity 1.000 / 1.000 / 1.000 |
| **G1b M_ADVANTAGE_PER_MODE** | **not fired** | 0 discordant pairs in every mode; p = 1.0 |
| **G1c B5_ADVANTAGE_PER_MODE** | **not fired** | the symmetric test is likewise null — this is a tie, not a federation win (contrast ME-X2) |
| **G2 ANTI_CONSERVATISM** | **PASS** | M 0 vs B5 0 manufactured doubt on the three negative-control strata, in every mode |
| **G3a MECHANISM_ATTRIBUTION** | not applicable | no M advantage to attribute |
| **G3b CROSS_MODE_MECHANISM_IDENTIFIABILITY** | **PASS** | 11/11 ablations Holm-significantly load-bearing in ≥ 2 modes; 10/11 in all three |
| **G4 INTERFACE_LADDER** | **PASS** (monotone, per mode) | no violation at any step in any mode; the decisive rung **differs across modes** |
| **G5 CHANGED_VOCABULARY** | **PASS** | recovery 1.000 / 0.961 / 1.000; shuffled-label null 0.116 / 0.141 / 0.141 |
| COST | flag only | B5 72.2 ms vs M 41.1 ms wall (ratio 1.76); engine ops M 15 840 vs B5 7 200, not commensurable |

## 3. Per-arm decision-exact rate, per mode (design §5: never pooled into one claim)

| arm | FORMAL | MEASUREMENT | SYNTHESIS | pooled |
|---|---|---|---|---|
| `B0_DIRECT_NATIVE_PIPELINE` | 0.2500 | 0.2188 | 0.1979 | 0.2222 |
| `B1_CALIBRATED_ABSTENTION` | 0.2500 | 0.2188 | 0.1979 | 0.2222 |
| `B2_PROVENANCE_VERIFIER_RUNTIME` | 0.3438 | 0.3125 | 0.2958 | 0.3174 |
| `B3_DIAGNOSIS_METAREASONING` | 0.3646 | 0.3500 | 0.3688 | 0.3611 |
| `B4_TMS_ASSURANCE_FEDERATION` | 0.4167 | 0.3854 | 0.3646 | 0.3889 |
| `B5_R1_VERDICT_ONLY` | 0.8646 | 0.8500 | 0.8688 | 0.8611 |
| `B5_R2_PROVENANCE` | 0.8750 | 0.8604 | 0.8833 | 0.8729 |
| `B5_R3_PLUS_DEPENDENCE_ANCESTRY` | 0.8896 | 0.8833 | 0.8979 | 0.8903 |
| `B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR` | 0.9479 | 0.9333 | 0.9521 | 0.9444 |
| **`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| **`M_ME_CROSS_TRANSITION_CONTROL`** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| `M_MINUS_IDENTITY` | 0.9167 | 0.8812 | 0.9167 | 0.9049 |
| `M_MINUS_APPARATUS` | 0.8958 | 0.8896 | 0.8958 | 0.8938 |
| `M_MINUS_EVALUATOR` | 0.8917 | 0.9021 | 0.8958 | 0.8965 |
| `M_MINUS_DEPENDENCE` | 0.9021 | 0.8938 | 0.9021 | 0.8993 |
| `M_MINUS_TRANSPORT` | 0.9042 | 0.9083 | 0.9042 | 0.9056 |
| `M_MINUS_SCOPE` | 0.9167 | 0.9521 | 0.9167 | 0.9285 |
| `M_MINUS_GLOBAL` | 0.9167 | 0.9167 | 0.9167 | 0.9167 |
| `M_MINUS_NUMERIC` | **1.0000** | 0.9688 | 0.9479 | 0.9722 |
| `M_MINUS_FAMILIES` | 0.8500 | 0.7958 | 0.8021 | 0.8160 |
| `M_MINUS_AUTHORITY` | 0.9167 | 0.9167 | 0.9167 | 0.9167 |
| `M_MINUS_UNRESOLVED` | 0.9167 | 0.9167 | 0.9167 | 0.9167 |
| `M_ABSTAIN_WHENEVER_CENSORED` | 0.9167 | 0.9167 | 0.9167 | 0.9167 |
| `C_ALWAYS_COMMIT` | 0.1667 | 0.1667 | 0.1667 | 0.1667 |
| `C_NEVER_COMMIT` | 0.1667 | 0.1667 | 0.1667 | 0.1667 |
| `C_ALWAYS_UNRESOLVED` | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `C_RANDOM_DECISION` | 0.0187 | 0.0167 | 0.0146 | 0.0167 |

## 4. The interface ladder, per mode — the decisive rung is not the same in all three

| mode | R1 verdict-only | R2 +provenance | R3 +dependence ancestry | R4 +typed transport/evaluator | R5 full structure | significant steps (exact two-sided p) | decisive rung |
|---|---|---|---|---|---|---|---|
| `FORMAL` | 0.8646 | 0.8750 | 0.8896 | 0.9479 | 1.0000 | R2→R3 (0.0156), R3→R4 (<1e-6), R4→R5 (<1e-6) | **R3→R4** (+0.058) |
| `MEASUREMENT` | 0.8500 | 0.8604 | 0.8833 | 0.9333 | 1.0000 | R2→R3 (0.00098), R3→R4 (<1e-6), R4→R5 (<1e-6) | **R4→R5** (+0.067) |
| `SYNTHESIS` | 0.8688 | 0.8833 | 0.8979 | 0.9521 | 1.0000 | R1→R2 (0.0156), R2→R3 (0.0156), R3→R4 (<1e-6), R4→R5 (<1e-6) | **R3→R4** (+0.054) |

Monotone everywhere; every step non-negative; no violation. **R1→R2 is significant only in the synthesis mode** (p = 0.0156 against p = 0.0625 in the other two), and the **largest** step is R4→R5 in the measurement mode but R3→R4 in the other two. Under a *balanced* design — the twelve strata are planted identically in all three modes, so the only thing that varies is the native semantics (design §10.5) — the ladder profile is nevertheless not identical. The variation is small and sits at the boundary of what n = 480 per mode resolves; the honest statement is that **the decisive rung is not established to be mode-invariant, and the cross-*study* variation remains much larger**: ME-X1's single significant step was at R4→R5, ME-X4's were at R1→R2 and R3→R4 (verified directly against `ME_X4_PROTECTED_ANALYSIS_V1.json`, not taken on report). The decisive rung is primarily *generator*-dependent.

**What every rung below 5 gets wrong** is legible in the outcome vector: rungs 1–4 carry 63 missed warranted transitions and 17 narrowing errors, all of them in `SCOPE_OVERREACH` (0.33 exact at every rung below 5, 1.00 at rung 5). The scope/identity witness — the same *identity/criterion/specification* witness that ME-X1 found decisive — is what rung 5 adds and no lower rung can reconstruct. `B5_R1` also carries 120 false closures over an unresolved terminal and 16 invalid transports accepted; those are closed at R4.

## 5. Reading (within the frozen gates; no reinterpretation)

- **H0 (strongest-parent sufficiency) holds, in every mode, in its exact form.** An information-matched federation of provenance revocation, truth maintenance over support families, dependence assessment, typed transport, evaluator-coverage contracts, scope bookkeeping, assurance/global-witness checking and native numeric aggregation — composed by ordinary engineering glue, never artificially isolated — reproduces **every one of M's 1 440 decisions**. Zero discordant pairs; the 95% interval on the paired difference is [0.0000, 0.0000] in all three modes, inside the ±0.02 equivalence margin registered before the run. Unlike ME-X2 this is a genuine tie, not a federation win: `G1c` is null too.

- **The interface-standard terminal fired on its own positive test, and that is exactly what it says.** All three conditions of design §6.5 hold in all three modes: the ladder is monotone; rung 1 is significantly worse than rung 5 (0.85–0.87 against 1.000, p < 1e-6); and M and B5 are statistically equivalent at full structure within the margin. ME-X2's version of this terminal was ¬G1b and fired on a federation win as well as a tie, and could not be quoted alone. **This one can** — but what it claims is narrow: *what the interface carries decides the outcome; who holds the control layer does not.* That is a standards claim, not a mechanism claim.

- **A mechanism is identifiable across modes; it is just not a residual.** Protocol §7(1) asks whether a predeclared mechanism is identifiable in ≥ 2 native modes. Eleven of eleven omission ablations are Holm-significantly load-bearing in ≥ 2 modes and ten of eleven in all three: removing the support-family structure costs 0.15–0.20, removing the apparatus contract 0.10–0.11, the evaluator contract 0.10, dependence ancestry 0.10, typed transport 0.09, the authority boundary 0.083 (120 authority violations), the unresolved terminal 0.083 (120 false closures). §7(1) is satisfied; §7(2) — *a protected quality-cost residual beyond B5* — is not, and without it §7 is not met. **The mechanism recurs; the residual does not.** That is the whole content of `R1_BENCHMARK_INTEGRATION_VALUE`.

- **The one ablation that is mode-specific is the one the native rules say should be.** `M_MINUS_NUMERIC` costs exactly **0.0000** in the formal mode and 0.031 / 0.052 in the two numeric modes. The formal mode has no numeric layer, so the ablation is inert there by construction; that it measures exactly zero is a validity check on the mode separation, not a finding. In the two numeric modes it is a real 40-instance loss — and it is the place where the Boolean parents visibly fail: `B4_TMS_ASSURANCE_FEDERATION`, given a body of evidence with nothing structurally broken whose pooled estimate has fallen below the registered threshold, commits.

- **Where the single parents break (attribution), per stratum.** `B0` 0.222 with 800 false transitions and 120 authority violations — the native pipeline commits to anything whose artefacts are still present. `B1` adds abstention and gains nothing (0.222): it abstains where nothing was censored-decisive and still commits everywhere else, which is the registered warning that abstention is not a control layer. `B2` (provenance + apparatus) is exact on `APPARATUS_INVALID` and `SINGLE_PARENT_SUFFICIENT` and 0.00 on dependence, transport, evaluator coverage, identity and global obstruction. `B3` (diagnosis over identity/apparatus/evaluator/scope) is exact on `TARGET_IDENTITY_DRIFT` and `BLIND_EVALUATOR` and 0.00 on `HIDDEN_DEPENDENCE`, `INVALID_TRANSPORT`, `LOCAL_COMPATIBILITY_GLOBAL_OBSTRUCTION` and `DEFEATED_SUPPORT`. `B4` (TMS + dependence + assurance) is the best single parent at 0.389, exact on dependence and global obstruction, 0.00 on identity, apparatus, evaluator coverage and transport, and cannot express the unresolved terminal at all. **No single parent exceeds 0.42; the federation reaches 1.000. It is the composition that reproduces M, not any one parent** — the same shape ME-X2 reported.

- **The common object is recoverable without ORION vocabulary, with one honest hole.** One mode-blind rule set written in ordinary scientific English, reading native fields through per-mode adapters, recovers the responsibility class on 1 303 of 1 320 decidable instances: 440/440 formal, 423/440 measurement, 440/440 synthesis, against a within-mode shuffled-label null of 0.116 / 0.141 / 0.141. **All 17 misses are one variant** — the measurement mode's `FIDUCIAL_RESTRICTION`, where a channel measures the registered observable in a strictly smaller phase space. The neutral vocabulary has a predicate for *does it answer the registered question* and one for *is the claim broader than the coverage*, and neither captures "it answers a strictly narrower version of the question". That is a real lossiness of the mode-neutral vocabulary at exactly the point the measurement mode's native-review record flagged: the fiducial-versus-total distinction is native and quantitative, and the abstraction only partly carries it. The 3 × 3 cross-adapter diagnostic is reported in the analysis JSON and is *not* a gate: the measurement and synthesis adapters read the native surfaces similarly enough that swapping them barely degrades recovery (0.886, 0.909), while swapping in the formal adapter collapses it (0.091).

- **Cost.** M is *faster* in wall-clock (41.1 ms against 72.2 ms for the federation across 1 440 instances) and charges more engine-native operations (15 840 against 7 200). The two disagree because they measure different things and neither routes anything: engine op counts are engine-native and not commensurable, and the ratio 1.76 is inside the 2× flag. There is no cost claim here.

- **What this study does *not* license.** The registered information determines the decision in all three modes and every arm can compute it exactly, so an information-complete federation is optimal **by construction** (design §10.3). The numeric modes remove *Boolean-parent* optimality — and that is visible, `B4` commits where the pooled estimate has fallen — but they do not remove *exact-computability* optimality. The honest terminal is therefore **"no ME residual is detectable in registered decision problems the parents already solve exactly, in any of three native epistemic modes"**, not "no residual exists". The one separation this design can and did exhibit is finite-information, not computational: the H-EXT-3 ladder. Further: the common decision object is a **design input**, the three modes share authorship, and no independent native reviewer participated — so `R2` is not grantable here whatever the numbers, and the changed-vocabulary result bounds circularity without removing it.

## 6. Protocol ME-X5 kill conditions (§12) — status

| condition | outcome |
|---|---|
| B5 ties or wins the protected frontier | **yes — B5 ties exactly, at equal quality and comparable cost.** Contract the ME-X5 field residual |
| the common object is unstable under native reconstruction | no: recovered in 1 303/1 320 decidable instances by an ORION-free rule set, against a 0.12–0.14 null; the 17 exceptions are one measurement-mode variant |
| only one domain shows a residual | no domain shows one |
| targeted ablations fail to support the claimed mechanism | not applicable: no advantage to attribute. The ablations *do* show the mechanism is load-bearing in ≥ 2 modes (§7(1) satisfied, §7(2) not) |
| M gains come from extra information, resources or over-abstention | no gains; M and B5 are information-matched and M abstains exactly when the oracle does (0 unnecessary abstentions, 0 missed necessary abstentions) |
| changed-vocabulary reviewers cannot recover a common object | not triggered — but the reviewer is a formal surrogate, not independent, so protocol §8 is only partly discharged |
| integration costs or failure surface dominate benefits | no: parity within 2× |

## 7. Programme consequence

`ME_X5_STATUS = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`, field-support ladder `R1_BENCHMARK_INTEGRATION_VALUE`.

The principal field discriminator returns the same answer as its three siblings, now across three native epistemic modes at once and with the interface-standard reading resting on a positive test rather than on the absence of a gap. On registered, exactly adjudicable scientific-transition decisions, **ORION's cross-transition control layer produces no residual beyond an information-matched parent federation in the formal, measurement or evidence-synthesis mode.** What it does produce, in all three, is a *specification of what an inter-module interface must carry*: family identity, dependence ancestry, typed transport, evaluator coverage, and — the step no lower rung recovers — the scope/identity witness. A federation given that interface is exact; a federation given family-anonymous verdicts is not, and no amount of parent quality repairs it.

Consistent with decisive-studies §1 ("if H0 ties or wins on the protected quality-cost frontier after reasonable prespecified repair, do not reinterpret the result as Machine Epistemics superiority; contract the claimed residual") and ME-X5 protocol §12, the field claim contracts here to a bridge/integration/benchmark programme with an interface standard, not a control-layer residual. `R2` remains ungranted and requires independent adjudication; `R3` is not grantable by any experiment.

Registered as *not* discharged by this study, and left open: protocol §7's naturalistic cell with independent native reviewers; protocol §8's independent changed-vocabulary reviewer; and a decision problem the parents do **not** already solve exactly, which is the only place a computational — as opposed to finite-information — separation could appear. No field status, novelty or publication authority is granted or implied.

## 8. Custody

`results/ME_X5_PROTECTED_*` are force-added past the `.gitignore` that guards against unauthorized commits. The custody seed file remains in operator custody at `~/.orion-custody/me-x5/PROTECTED_SEED_V1.txt` (mode 600); its value is now public (above) and the split is reproducible by anyone from the frozen code on main `a5ee8a6`. Determinism was verified byte-for-byte on the **development** split; the protected split is a single run by design and was not re-run.
