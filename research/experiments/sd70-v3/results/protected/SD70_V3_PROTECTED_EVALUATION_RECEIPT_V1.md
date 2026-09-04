# SD70-V3 protected evaluation receipt (guards lane) — V1

**State date:** 2026-09-04  
**Lane:** guards (mechanical evaluation under the frozen design; no interpretation)  
**Route as computed by the frozen evaluator (run of record, Mac, CPython 3.13.12 — the design's registered interpreter):** `PARENT_SUFFICIENT`  
**Design sha256 bound into FROZEN_SUITE and re-checked by evaluate:** `662837355020658ab77fc6067060df1b105e54ad757caf0378925178a7723138`  
**Study:** `SD70-V3` · tasks 240 · strongest generator-faithful parent `MAXMARGIN_PARENT`

## 0. Two recorded deviations from the design, and what they did and did not touch

`CUSTODY_DEVIATION: seed copied to billy-old post-CHANNEL_END under operator directive 2026-09-04 ("run on laptop/billy-old/lunarc"); channel closed before transfer; seed sha verified both sides` — see `../SD70_V3_CUSTODY_SUPERSESSION_NOTE_V1.md`.

`INTERPRETER_CROSSCHECK` (coordinator decision, 2026-09-04): the run of record is the Mac run under the design's registered CPython 3.13.12 (§13), completed before the off-Mac directive arrived; the billy-old run under CPython 3.14.4 — forced by that directive — is kept beside it as a cross-interpreter control, not as a deviation of record. Future SD70 designs register billy-old's interpreter so directive and design agree. The design's §13 prediction — a near-tie in a float-accumulating parent can flip ≈1 task in 600 between interpreters and cannot flip a registered gate — was **observed exactly**: one task, `sd70v3-0230`, is scored correct by `FIXED_META_LESSON` under 3.14.4 and incorrect under 3.13.12, and its LP control `sd70v3-0230-LP` the reverse. Everything registered is invariant (§2 below). The billy-old run is committed beside this one as `protected-crosscheck-billyold-py3.14.4/`; nothing was recomputed for the designation.

## 1. What this is, and the design's own receipt

This receipt records that the SD70-V3 protected responses (dispatched on billy-old 2026-09-03, model gpt-5.5, effort medium, repeats 3) were evaluated under the frozen design and what the frozen evaluator returned. The design's own outcome receipt, `SD70_V3_OUTCOME_RECEIPT.md`, is rendered beside it by `make_outcome_receipt.py` from the record rollup. That renderer requires `PROTECTED_RUN_AUTHORIZATION.json`, which no stage of `sd70v3_run.py` mints and which did not exist anywhere after the 2026-09-03 dispatch; on the coordinator's decision (2026-09-04) it was written from the operator's verbatim chat authorization of 2026-09-02 (reaffirmed 2026-09-04), which precedes the dispatch, with a `disclosure` field stating exactly that and naming the missing-mint as a design defect for the next SD70 version (the dispatcher must refuse without it). Its `timestamp_utc` is null because the message time-of-day is not on record.

## 2. Freeze assertions (held on BOTH hosts, before evaluation)

- `prepare` from the custody seed (never printed): seed sha256 `d032efa9a570c5ba…` = design `seed_commitment.seed_sha256`. Regenerated `REQUEST_SURFACE_MANIFEST.json` **byte-identical** to the one the dispatcher consumed (`manifest_sha256` `0e6e5da4a54eb750…`, 40 arms, 9060 requests) — on billy-old (3.14.4) and on the Mac (3.13.12) alike: generation is interpreter-invariant here.
- `FROZEN_SUITE.design_sha256` `662837355020658a…` = sha256 of the design on main.
- Responses billy-old → Mac by rsync with md5 manifests both sides (1144/1144); every one of the 1140 model-arm responses validated `VALID` against the regenerated requests before dispatch.
- `dispatch`: 7920 deterministic-arm jobs, **0 model jobs** (`ORION_SD70V2_MODEL_COMMAND=/usr/bin/false` on the Mac, `/bin/false` on billy-old, as a belt); private oracle deleted and hash-exactly restored. Integrity {'ARM_FAILURE': 0, 'INTEGRITY_VIOLATION': 0, 'VALID': 9060}, `dispatch_integrity_passed` = True. A first billy-old attempt at `--max-concurrency 4` was **refused by the design's frozen-budget guard** before touching anything and re-run at the frozen 2 (attempt log kept on billy-old).
- Channel contract `CHANNEL_CONTRACT_OK` (canaries 9/9 both ends; payload verification 9060/9060 on the dispatch host); envelope homogeneity OK; arm divergence passed; missingness {"global_failure_rate": 0.0, "model_arm_failures": 0, "model_arm_tasks": 1140, "per_arm_exceeding_threshold": []}; `cannot_check_reasons` = [].

## 3. Frozen evaluator output — run of record (Mac, CPython 3.13.12)

Route: **`PARENT_SUFFICIENT`**

| primary outcome | contrast | point [95% CI] |
|---|---|---|
| protected_decision_quality | F2_FULL_vs_SP | -0.0083 [-0.0500, +0.0333] (b=13, c=15, n=240, mid-p=0.644) |
| critical_false_direction | F2_FULL_vs_SP | -0.0042 [-0.0250, +0.0125] (b=2, c=3, n=240, mid-p=0.656) |
| protected_decision_quality | F2_STATIC_vs_SP | +0.0000 [-0.0458, +0.0458] (b=15, c=15, n=240, mid-p=0.500) |
| critical_false_direction | F2_STATIC_vs_SP | -0.0042 [-0.0250, +0.0167] (b=3, c=4, n=240, mid-p=0.637) |

Holm: {"F2_FULL_vs_SP": {"holm_threshold": 0.05, "p": 0.644464448094368, "rank": 2, "reject": false}, "F2_STATIC_vs_SP": {"holm_threshold": 0.025, "p": 0.5, "rank": 1, "reject": false}}  
Parent non-regression: {"delta_ci_low": -0.05, "holds": false, "margin": 0.05}  
Gates: `cost_within_budget`=True, `critical_false_direction`=True, `effect_minimum`=False, `effect_significant_holm`=False, `mechanism_recursion`=False, `model_negative_controls_behave`=True, `no_ablation_beats_full`=True, `non_regression`=False, `parent_ties_or_exceeds_f2`=True

Negative controls (accuracy vs chance → `behaves`): `F2_RECURSIVE_META_DISCOVERY_FULL__LP` 0.300 vs 0.271 → True; `F2_RECURSIVE_META_DISCOVERY_FULL__QS` 0.283 vs 0.271 → True; `STRONGEST_GENERATOR_FAITHFUL_PARENT__LP` 0.212 vs 0.261 → True; `STRONGEST_GENERATOR_FAITHFUL_PARENT__QS` 0.287 vs 0.261 → True; `TARGET_ONLY_DETERMINISTIC` 0.250 vs 0.261 → True; `TARGET_ONLY_NEGATIVE_CONTROL` 0.317 vs 0.271 → True

## 4. Cross-interpreter comparison (Mac 3.13.12 run of record vs billy-old 3.14.4 cross-check)

Identical: route, all nine gates, both primary-outcome tables, Holm, parent non-regression, all negative controls, all ablations, all model-arm records (the 1140 responses are the same bytes; only deterministic arms recompute). Different: 132 wall-time fields (expected), and **one deterministic task**:

| arm | task | 3.13.12 (record) | 3.14.4 (cross-check) |
|---|---|---|---|
| `FIXED_META_LESSON` | `sd70v3-0230` | incorrect → 155/240 = 0.6458 | correct → 156/240 = 0.6500 |
| `FIXED_META_LESSON__LP` | `sd70v3-0230-LP` | correct → 60/240 = 0.2500 | incorrect → 59/240 = 0.2458 |
| secondary `FIXED_vs_F2_FULL` | — | -0.0375 [-0.1042, +0.0250], c=34 | -0.0333 [-0.0958, +0.0292], c=33 |

This is the §13 mechanism (float-score near-tie resolved by summation order), at the §13 magnitude (1 task in 240 per arm ≈ 0.4 %), in a **secondary** contrast that no registered gate reads. Rollup sha256: record `862fce884a916c16…`, cross-check `a7a11ff9e4033a38…`.

## 5. Custody of what is and is not committed

`protected/` (record, Mac 3.13.12): rollup json+md, arm records, dispatch receipt (9060 validations), FROZEN_SUITE, request-surface manifest, CHANNEL_START/END, oracle commitment/restoration, remote dispatcher log, sha256 custody manifests of the 9060 requests and 9060 responses. `protected-crosscheck-billyold-py3.14.4/`: the same set from the billy-old run. **Not committed** on either side: `private_oracle.json`, `public_tasks.json`, raw `requests/`, `responses/` (bound by the custody manifests; raw trees on billy-old `~/sd70v3-eval/workdir`, `~/sd70v3-protected` and the Mac inbound dir). Seed-leak assertion (custody seed bytes absent from every committed file) passed on both packages.

## 6. Authority

Grants nothing. The route is the frozen evaluator's output, reported verbatim. Whether `PARENT_SUFFICIENT` with `non_regression=false` and `effect_minimum=false` is read as the design's terminal is the study lane's reading under design §10; which manuscript cites it is lane-paper-2's / lane-paper-3's call. The design's outcome receipt is rendered (§1); the designation of record is the coordinator's 2026-09-04 decision.

