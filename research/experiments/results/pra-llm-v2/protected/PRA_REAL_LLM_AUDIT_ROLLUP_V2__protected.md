# PRA real-LLM audit rollup V2 — split `protected`

design `ORION51.PRA_REAL_LLM_AUDIT.design.v2` · runner sha256 `198626238170df48…` · suite sha256 `526b47b8c2f93cf8…`

**Overall terminal:** `P2_SINGLE_MODEL_ONLY__REGISTERED_BOUNDARY_RESULT`

**Routing:** reported as a registered negative or boundary result under the mapped terminal; P0-dominated suite is a valid negative; no family, prompt, threshold or gate may change post-outcome (no-rescue clause)

| model | GP0 | GP1 | GP2 | GP3 | terminal |
|---|---|---|---|---|---|
| mistral-small-24b-instruct-2501 | False | True | True | True | `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` |
| qwen2.5-32b-instruct | True | True | True | True | `P2_PROSPECTIVE_REVISION_STATE_REQUIRED` |

## mistral-small-24b-instruct-2501

- Contrast B (R2→R3, P2 canonical): acc 0.250 → 1.000 (n=240, discordant 0/180, exact p=0.000)
- Contrast B-SF (R2→R3, same-successor-fibre variant, secondary): acc 0.004 → 1.000 (n=240, exact p=0.000; instance-level p=0.000)
- GP0 present equivalence: per-unit pass 0.296; TOST mean Δlogprob 0.000 (equivalent=True)
- Probe max test acc: R0=0.844, R1=0.521, R2=0.552, R2_TEXT_REMOVED_KV_RETAINED=0.990, R2_TRUE_REMOVAL=0.552, R3=0.573
- Contrast D (true removal → KV retained): acc 0.250 → 1.000 (exact p=0.000); terminal `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION__KV_SURVIVAL_CONTROL_CONFIRMED`
- Incompatible-cell rate by condition: R0=0.000, R1=0.529, R2=0.405, R3=0.000, R4=0.000

| family | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| F0_ACQ | 0.600 | 0.025 | 0.600 | 0.475 | 0.625 |
| F1_P0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F2_P1 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 |
| F3_P2_CANON | 1.000 | 0.500 | 0.250 | 1.000 | 1.000 |
| F3_P2_MIRROR | 1.000 | 1.000 | 0.033 | 1.000 | 1.000 |
| F3_P2_INDEP | 1.000 | 0.500 | 0.242 | 1.000 | 1.000 |
| F3_P2_RECON | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F3_P2_TIE | 1.000 | 0.887 | 1.000 | 1.000 | 1.000 |
| F3_P2_CANON_SF | 1.000 | 0.433 | 0.004 | 1.000 | 1.000 |

## qwen2.5-32b-instruct

- Contrast B (R2→R3, P2 canonical): acc 0.079 → 1.000 (n=240, discordant 0/221, exact p=0.000)
- Contrast B-SF (R2→R3, same-successor-fibre variant, secondary): acc 0.242 → 1.000 (n=240, exact p=0.000; instance-level p=0.000)
- GP0 present equivalence: per-unit pass 1.000; TOST mean Δlogprob -0.000 (equivalent=True)
- Probe max test acc: R0=1.000, R1=0.552, R2=0.562, R2_TEXT_REMOVED_KV_RETAINED=0.990, R2_TRUE_REMOVAL=0.562, R3=0.573
- Contrast D (true removal → KV retained): acc 0.079 → 1.000 (exact p=0.000); terminal `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION__KV_SURVIVAL_CONTROL_CONFIRMED`
- Incompatible-cell rate by condition: R0=0.000, R1=0.529, R2=0.405, R3=0.000, R4=0.000

| family | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| F0_ACQ | 0.850 | 0.075 | 0.850 | 0.250 | 0.950 |
| F1_P0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F2_P1 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 |
| F3_P2_CANON | 1.000 | 0.483 | 0.079 | 1.000 | 1.000 |
| F3_P2_MIRROR | 1.000 | 1.000 | 0.142 | 1.000 | 1.000 |
| F3_P2_INDEP | 1.000 | 0.467 | 0.092 | 1.000 | 1.000 |
| F3_P2_RECON | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F3_P2_TIE | 1.000 | 0.725 | 0.950 | 1.000 | 1.000 |
| F3_P2_CANON_SF | 1.000 | 0.471 | 0.242 | 1.000 | 1.000 |

Three-history joint-intersection control passes: True

No scientific authority is granted by this file; routing requires a new manuscript version and freeze.
