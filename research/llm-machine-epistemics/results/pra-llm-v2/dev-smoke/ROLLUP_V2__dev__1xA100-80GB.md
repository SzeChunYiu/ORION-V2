# PRA real-LLM audit rollup V2 — split `dev`

design `ORION51.PRA_REAL_LLM_AUDIT.design.v2` · runner sha256 `e42c5adc9521544e…` · suite sha256 `a8c58107bd53f9f5…`

**Overall terminal:** `REGISTERED_NEGATIVE_OR_BOUNDARY__CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE|INCOMPLETE__CONTROL_FAMILIES_MISSING`

**Routing:** reported as a registered negative or boundary result under the mapped terminal; P0-dominated suite is a valid negative; no family, prompt, threshold or gate may change post-outcome (no-rescue clause)

| model | GP0 | GP1 | GP2 | GP3 | terminal |
|---|---|---|---|---|---|
| mistral-small-24b-instruct-2501 | False | False | False | None | `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` |
| qwen2.5-32b-instruct | True | False | False | None | `INCOMPLETE__CONTROL_FAMILIES_MISSING` |

## mistral-small-24b-instruct-2501

- Contrast B (R2→R3, P2 canonical): acc 0.375 → 1.000 (n=8, discordant 0/5, exact p=0.062)
- GP0 present equivalence: per-unit pass 0.500; TOST mean Δlogprob 0.000 (equivalent=True)
- Probe max test acc: R0=0.750, R1=0.750, R2=0.750, R2_TEXT_REMOVED_KV_RETAINED=1.000, R2_TRUE_REMOVAL=0.750, R3=0.750
- Contrast D (true removal → KV retained): acc 0.375 → 1.000 (exact p=0.062); terminal `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`
- Incompatible-cell rate by condition: R0=0.000, R1=0.500, R2=0.500, R3=0.000, R4=0.000

| family | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| F1_P0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F3_P2_CANON | 1.000 | 0.500 | 0.375 | 1.000 | 1.000 |

## qwen2.5-32b-instruct

- Contrast B (R2→R3, P2 canonical): acc 0.000 → 1.000 (n=8, discordant 0/8, exact p=0.008)
- GP0 present equivalence: per-unit pass 1.000; TOST mean Δlogprob 0.000 (equivalent=True)
- Probe max test acc: R0=1.000, R1=0.750, R2=0.750, R2_TEXT_REMOVED_KV_RETAINED=0.750, R2_TRUE_REMOVAL=0.750, R3=0.750
- Contrast D (true removal → KV retained): acc 0.000 → 1.000 (exact p=0.008); terminal `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`
- Incompatible-cell rate by condition: R0=0.000, R1=0.500, R2=0.500, R3=0.000, R4=0.000

| family | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| F1_P0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F3_P2_CANON | 1.000 | 0.375 | 0.000 | 1.000 | 1.000 |

Three-history joint-intersection control passes: True

No scientific authority is granted by this file; routing requires a new manuscript version and freeze.
