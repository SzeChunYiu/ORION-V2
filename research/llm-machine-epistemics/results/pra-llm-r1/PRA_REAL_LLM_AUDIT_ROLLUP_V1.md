# PRA real-LLM audit rollup V1 — split `protected`

design `ORION51.PRA_REAL_LLM_AUDIT.design.v1` · runner sha256 `e25d969fb20aee3e…` · suite sha256 `21b5b0f7263a4973…`

**Overall terminal:** `REGISTERED_NEGATIVE_OR_BOUNDARY__CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE`

**Routing:** reported as a registered negative or boundary result under the mapped terminal; P0-dominated suite is a valid negative; no family, prompt, threshold or gate may change post-outcome (no-rescue clause)

| model | GP0 | GP1 | GP2 | GP3 | terminal |
|---|---|---|---|---|---|
| mistral-7b-instruct-v0.3 | True | True | True | False | `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE` |
| qwen2.5-7b-instruct | True | True | True | False | `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE` |

## mistral-7b-instruct-v0.3

- Contrast B (R2→R3, P2 canonical): acc 0.246 → 0.529 (n=240, discordant 0/68, exact p=0.000)
- GP0 present equivalence: per-unit pass 1.000; TOST mean Δlogprob -0.000 (equivalent=True)
- Probe max test acc: R0=0.917, R1=0.552, R2=0.573, R2_TEXT_REMOVED_KV_RETAINED=0.896, R2_TRUE_REMOVAL=0.573, R3=0.594
- Contrast D (true removal → KV retained): acc 0.246 → 0.500 (exact p=0.000); terminal `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION__KV_SURVIVAL_CONTROL_CONFIRMED`
- Incompatible-cell rate by condition: R0=0.000, R1=0.429, R2=0.290, R3=0.000, R4=0.000

| family | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| F0_ACQ | 0.000 | 0.000 | 0.375 | 0.000 | 0.000 |
| F1_P0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F2_P1 | 1.000 | 0.500 | 0.617 | 0.708 | 0.717 |
| F3_P2_CANON | 0.500 | 0.500 | 0.246 | 0.529 | 0.500 |
| F3_P2_MIRROR | 0.000 | 0.000 | 0.000 | 0.042 | 0.033 |
| F3_P2_INDEP | 0.500 | 0.500 | 0.233 | 0.500 | 0.500 |
| F3_P2_RECON | 0.508 | 0.500 | 0.783 | 0.950 | 0.775 |
| F3_P2_TIE | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## qwen2.5-7b-instruct

- Contrast B (R2→R3, P2 canonical): acc 0.500 → 0.867 (n=240, discordant 0/88, exact p=0.000)
- GP0 present equivalence: per-unit pass 1.000; TOST mean Δlogprob 0.000 (equivalent=True)
- Probe max test acc: R0=1.000, R1=0.562, R2=0.510, R2_TEXT_REMOVED_KV_RETAINED=0.979, R2_TRUE_REMOVAL=0.510, R3=0.542
- Contrast D (true removal → KV retained): acc 0.500 → 0.508 (exact p=0.500); terminal `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION__KV_INFORMATION_RETAINED_BUT_NOT_USED`
- Incompatible-cell rate by condition: R0=0.000, R1=0.429, R2=0.290, R3=0.000, R4=0.000

| family | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| F0_ACQ | 0.225 | 0.000 | 0.000 | 0.075 | 0.125 |
| F1_P0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.992 |
| F2_P1 | 1.000 | 0.500 | 0.625 | 0.967 | 0.933 |
| F3_P2_CANON | 0.662 | 0.500 | 0.500 | 0.867 | 0.546 |
| F3_P2_MIRROR | 0.250 | 0.000 | 0.000 | 0.733 | 0.150 |
| F3_P2_INDEP | 0.558 | 0.500 | 0.500 | 0.750 | 0.508 |
| F3_P2_RECON | 0.958 | 0.975 | 0.992 | 1.000 | 0.842 |
| F3_P2_TIE | 0.988 | 1.000 | 1.000 | 1.000 | 1.000 |

Three-history joint-intersection control passes: True

No scientific authority is granted by this file; routing requires a new manuscript version and freeze.
