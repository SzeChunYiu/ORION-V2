# SD70-V3 protected evaluation receipt (guards lane) — V1

**State date:** 2026-09-04  
**Lane:** guards (mechanical evaluation under the frozen design; no interpretation)  
**Route as computed by the frozen evaluator:** `PARENT_SUFFICIENT`  
**Design sha256 bound into FROZEN_SUITE and re-checked by evaluate:** `662837355020658ab77fc6067060df1b105e54ad757caf0378925178a7723138`  
**Study:** `SD70-V3` · tasks 240 · strongest generator-faithful parent `MAXMARGIN_PARENT`

## 1. What this is and is not

This receipt records that the SD70-V3 protected responses (dispatched on billy-old 2026-09-03) were evaluated on the Mac, where the oracle lives, under the frozen design, and what the frozen evaluator returned. It is **not** the design's outcome receipt: `make_outcome_receipt.py` requires `PROTECTED_RUN_AUTHORIZATION.json` (the ME-X-shaped record of a verbatim operator authorization with `state`), no stage of `sd70v3_run.py` mints one, and none exists on any repository ref, on billy-old, or in the Mac custody directory. **The protected dispatch of 2026-09-03 therefore has no authorization record.** The guards lane does not fabricate one; the design's outcome receipt is pending that record and is the study lane's / operator's act.

## 2. Freeze assertions made before evaluation (all held)

- `prepare` re-run on the Mac from the custody seed (never printed, never copied): seed sha256 `d032efa9a570c5ba…` = design `seed_commitment.seed_sha256`.
- Regenerated `REQUEST_SURFACE_MANIFEST.json` byte-identical to the manifest billy-old consumed; `manifest_sha256` `0e6e5da4a54eb750…` (40 arms, 9060 request files). Prepare is deterministic from the seed.
- `FROZEN_SUITE.design_sha256` `662837355020658a…` = sha256 of `SD70_V3_EXECUTION_DESIGN_V1.json` on main.
- Responses transferred billy-old → Mac by rsync, md5 manifests built on both sides: 1144 files, 0 only-remote, 0 only-local, 0 mismatch.
- Every one of the 1140 model-arm responses validated `VALID` against the regenerated requests before dispatch; `dispatch` executed 7920 deterministic-arm jobs locally and **0 model jobs** (`ORION_SD70V2_MODEL_COMMAND=/usr/bin/false` as a belt). Private oracle deleted and hash-exactly restored around the deterministic arms (`PRIVATE_ORACLE_RESTORATION.json`).
- Dispatch integrity: {'ARM_FAILURE': 0, 'INTEGRITY_VIOLATION': 0, 'VALID': 9060} · `dispatch_integrity_passed` = True.
- Channel contract from CHANNEL_START/END (canaries 9/9 both ends, payload verification 9060/9060 on the dispatch host): `CHANNEL_CONTRACT_OK`; envelope homogeneity `CHANNEL_CONTRACT_OK`; arm divergence passed = True.
- Missingness: {"global_failure_rate": 0.0, "model_arm_failures": 0, "model_arm_tasks": 1140, "per_arm_exceeding_threshold": []}. `cannot_check_reasons`: [].

## 3. Frozen evaluator output (transcribed programmatically from `SD70_V3_ROLLUP.json`)

Route: **`PARENT_SUFFICIENT`**

| primary outcome | contrast | point [95% CI] |
|---|---|---|
| protected_decision_quality | F2_FULL_vs_SP | -0.0083 [-0.0500, +0.0333] (b=13, c=15, n=240, mid-p one-sided=0.644) |
| critical_false_direction | F2_FULL_vs_SP | -0.0042 [-0.0250, +0.0125] (b=2, c=3, n=240, mid-p one-sided=0.656) |
| protected_decision_quality | F2_STATIC_vs_SP | +0.0000 [-0.0458, +0.0458] (b=15, c=15, n=240, mid-p one-sided=0.500) |
| critical_false_direction | F2_STATIC_vs_SP | -0.0042 [-0.0250, +0.0167] (b=3, c=4, n=240, mid-p one-sided=0.637) |

Holm: {"F2_FULL_vs_SP": {"holm_threshold": 0.05, "p": 0.644464448094368, "rank": 2, "reject": false}, "F2_STATIC_vs_SP": {"holm_threshold": 0.025, "p": 0.5, "rank": 1, "reject": false}}  
Parent non-regression: {"delta_ci_low": -0.05, "holds": false, "margin": 0.05}

Gates: `cost_within_budget`=True, `critical_false_direction`=True, `effect_minimum`=False, `effect_significant_holm`=False, `mechanism_recursion`=False, `model_negative_controls_behave`=True, `no_ablation_beats_full`=True, `non_regression`=False, `parent_ties_or_exceeds_f2`=True

Negative controls (accuracy vs chance, `behaves`): `F2_RECURSIVE_META_DISCOVERY_FULL__LP` 0.300 vs 0.271 → True; `F2_RECURSIVE_META_DISCOVERY_FULL__QS` 0.283 vs 0.271 → True; `STRONGEST_GENERATOR_FAITHFUL_PARENT__LP` 0.212 vs 0.261 → True; `STRONGEST_GENERATOR_FAITHFUL_PARENT__QS` 0.287 vs 0.261 → True; `TARGET_ONLY_DETERMINISTIC` 0.250 vs 0.261 → True; `TARGET_ONLY_NEGATIVE_CONTROL` 0.317 vs 0.271 → True

Ablations / secondary / resource cost: see `SD70_V3_ROLLUP.json` and `SD70_V3_ROLLUP.md` beside this file.

## 4. Custody of what is and is not committed

Committed here: rollup (json+md), arm records, dispatch receipt (9060 validations), FROZEN_SUITE, request-surface manifest, CHANNEL_START/END, private-oracle commitment/restoration, the remote dispatcher log, and sha256 custody manifests of the 9060 requests and 9060 responses. **Not committed:** `private_oracle.json`, `public_tasks.json`, `requests/`, `responses/` (the raw trees stay on the Mac inbound dir and billy-old `~/sd70v3-protected`; their custody manifests bind them). A seed-leak assertion (custody seed bytes absent from every committed file) passed before commit.

## 5. Authority

Grants nothing. The route is the frozen evaluator's output, reported verbatim; which manuscript cites it, and whether a `PARENT_SUFFICIENT` route with `non_regression=false` and `effect_minimum=false` gates is read as the design's terminal, is the study lane's reading under the design's §10 decision rules — not this receipt's. The design's outcome receipt remains blocked as stated in §1.

