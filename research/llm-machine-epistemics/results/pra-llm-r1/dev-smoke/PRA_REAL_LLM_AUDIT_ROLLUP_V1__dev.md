# PRA real-LLM audit rollup V1 — split `dev`

design `ORION51.PRA_REAL_LLM_AUDIT.design.v1` · runner sha256 `6e7018963391df06…` · suite sha256 `98c8cbb54e5560d9…`

**Overall terminal:** `REGISTERED_NEGATIVE_OR_BOUNDARY__INCOMPLETE__CONTROL_FAMILIES_MISSING`

**Routing:** reported as a registered negative or boundary result under the mapped terminal; P0-dominated suite is a valid negative; no family, prompt, threshold or gate may change post-outcome (no-rescue clause)

| model | GP0 | GP1 | GP2 | GP3 | terminal |
|---|---|---|---|---|---|
| mistral-7b-instruct-v0.3 | True | False | False | None | `INCOMPLETE__CONTROL_FAMILIES_MISSING` |
| qwen2.5-7b-instruct | True | False | False | None | `INCOMPLETE__CONTROL_FAMILIES_MISSING` |

## mistral-7b-instruct-v0.3

- Contrast B (R2→R3, P2 canonical): acc 0.375 → 0.500 (n=8, discordant 0/1, exact p=1.000)
- GP0 present equivalence: per-unit pass 1.000; TOST mean Δlogprob -0.000 (equivalent=True)
- Probe max test acc: R0=1.000, R1=0.750, R2=0.750, R2_TEXT_REMOVED_KV_RETAINED=1.000, R2_TRUE_REMOVAL=0.750, R3=0.750
- Contrast D (true removal → KV retained): acc 0.375 → 0.500 (exact p=1.000); terminal `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`
- Incompatible-cell rate by condition: R0=0.000, R1=0.500, R2=0.500, R3=0.000, R4=0.000

| family | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| F1_P0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F3_P2_CANON | 0.500 | 0.500 | 0.375 | 0.500 | 0.500 |

## qwen2.5-7b-instruct

- Contrast B (R2→R3, P2 canonical): acc 0.500 → 0.750 (n=8, discordant 0/2, exact p=0.500)
- GP0 present equivalence: per-unit pass 1.000; TOST mean Δlogprob 0.000 (equivalent=True)
- Probe max test acc: R0=1.000, R1=0.750, R2=0.500, R2_TEXT_REMOVED_KV_RETAINED=0.750, R2_TRUE_REMOVAL=0.500, R3=1.000
- Contrast D (true removal → KV retained): acc 0.500 → 0.500 (exact p=1.000); terminal `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`
- Incompatible-cell rate by condition: R0=0.000, R1=0.500, R2=0.500, R3=0.000, R4=0.000

| family | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| F1_P0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| F3_P2_CANON | 0.625 | 0.500 | 0.500 | 0.750 | 0.625 |

Three-history joint-intersection control passes: True

No scientific authority is granted by this file; routing requires a new manuscript version and freeze.
