# E40-M1 Dispatch Receipt V1 — Matched F0/F2 Around the Native Causal Learner

**Lane:** E40 T3a (owner issue #45) · **Design:** `E40_MATCHED_F0_F2_PROSPECTIVE_DESIGN_V1` (PR #90, frozen 2026-08-30)
**Dispatched:** 2026-08-30, before any campaign outcome was read.

## 1. Jobs (LUNARC, account lu2026-2-51, partition lu48)

| Job | Type | Scope |
|---|---|---|
| **3554313** | array `0-35%6` (`o2-e40m1-chain`), 8 cpus / 64G / 2d | one `chain --task $TASK_ID` per array index; 36 tasks = 3 arms × 2 datasets × 6 reps |
| **3554314** | single (`o2-e40m1-eval`), `--dependency=afterok:3554313` | `control-planted → control-nullcal → control-uninformative → audit → rollup` (audit failure aborts before any verdict) |

Logs: `/projects/hep/fs9/users/scyiu/orion-v2-e45/logs/e40m1-chain-*`, `e40m1-eval-*`.
Campaign root: `/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-m1/` (dry-runs used the separate `campaign-e40-m1-dryrun/` root; the real `run/` was absent/empty at dispatch).

## 2. Frozen artifacts

- **Runner** `e40_matched_runner.py`, sha256
  `90842cee05f3ecb24c6536c3674b6ae271f57a445a1f967348fbe7ce6bfd9224`
  (LUNARC `campaign-e40-m1/e40_matched_runner.py` = repo `scripts/e40_matched_runner.py`).
- **Substrate**: CausalBench commit `1a2143cffdc85f835b41ce8d52034be1bf903e71` (`campaign-e40-r3/causalbench`), venv `campaign-e40-r3/run/venv`, model `pc`, datasets `weissmann_k562` / `weissmann_rpe1` with sha256s by reference to `research/experiments/results/issue45/e40/RUN_IDENTITY.json`. Fixed flags `--do_filter --subset_data 0.05 --max_path_length -1` as in E40 R1–R3.
- **Decision channel** (all arms): the E60 Anthropic-compatible lane (`/v1/messages`, `x-api-key` from `ANTHROPIC_AUTH_TOKEN`, `anthropic-version: 2023-06-01`), temperature 0, max_tokens 6000, `ORION_ARM_HTTP_RETRIES=10`. Native-substrate invocations only — no exchange/network contact beyond this established channel.
- **exp_id namespace**: `500000 + task*4 + slot` (chains), `500200 + idx` (uninformative-control blind runs); disjoint from the existing 400000-range. `results/<exp_id>/arguments.json` is cross-checked per run (custody).

## 3. Documented resolutions against the frozen design

1. **`subset_data` and `max_path_length` are PINNED** (0.05 / −1) although the design's `orchestratable_knobs` lists them. Rationale: varying `subset_data` changes the data volume and runtime per invocation (breaks matched native compute); varying `max_path_length` alters the statistical evaluator itself. The free-knob surface is the remaining five: `training_regime`, `fraction_partial_intervention`, `partial_intervention_seed`, `model_seed`, `omission_estimation_size` (the runner's validator rejects pinned-knob overrides; the audit re-checks every persisted `config_*.json`).
2. **SIMPLE arm config** = E40 R1 default verbatim: `partial_interventional`, `fraction_partial_intervention 0.5`, `partial_intervention_seed 0`, `omission_estimation_size 500`, `model_seed = rep` (6 seeds → 12 chains; compute floor, not matched ceiling).

## 4. Controls (as executed by job 3554314, in order, before rollup)

| Control | Operationalization | Pre-dispatch validation |
|---|---|---|
| planted-feedback recovery | 9-cycle replay; plant = `partial_interventional @ frac 0.8`, quality `regime_factor × exp(−((frac−0.8)/0.45)²)`, factors 1.0/0.7/0.55; PASS = last 3 cycles ≥ 0.9 quality AND no post-arrival dip < 0.8 | **PASS** (dry-run: blind probe q=0.35 → optimum by cycle 2 → pinned; 8/8 in basin, terminal 1.0) |
| permutation-null calibration | 400 reps of N(0,1) 12-pair diffs; rejection rate at α=0.05 must lie in [0.02, 0.09] | **PASS** (rate 0.055) |
| uninformative / no-fabrication | 12 blind chains whose cycle feedback is drawn ONLY from other-dataset runs (real redacted metrics, never the chain's own data); 4 decision calls + 1 blind native run each; gate (applied only if the ADVANTAGE gate is reached): `median(blind − informed) ≥ 0 AND perm_p(blind vs F0_best) ≥ 0.05` | machinery validated in dry-run; executes for real in job 3554314 |

## 5. Checker-validation history (pre-outcome; no campaign outcome data touched)

- v1 narrow-basin plant (`exp(−|frac−0.5|/0.15)`, hard regime gate ×0.05, 5 cycles, ≥3/4 within 0.15) **failed its own dry-run twice**: the loop followed the gradient correctly (~0.1 fraction-steps, one wasted probe) but the needle peak is not identifiable from the feedback channel within the counted budget — a plant-construction defect w.r.t. the design's "identifiable from the feedback channel alone" clause, not a channel defect.
- v3 off-anchor plant exposed that the hard regime gate flattens the fraction gradient for wrong-regime probes (all far-field feedback reads as noise), and that an `observational@0.8` optimum is semantically incoherent (`fraction_partial_intervention` is inert under observational — the model correctly refuses).
- v4 (final): soft regime factors, wide basin (σ 0.45), target off the default anchor (`partial@0.8`), 9 cycles, PASS = terminal residence. **PASS** on the real decision channel.
- Prompt-semantics fix (applied identically to every arm): the substrate header now states that within each external-knowledge evaluation higher `true_positives` mean better recovery of known interactions, and the F2 task text states that re-using a previous config is allowed. These are factual statements about the admissible feedback channel; the held-out `quantitative_test_evaluation` stays redacted and forbidden-substring-audited in every arm-visible artifact.

## 6. Pre-dispatch validation log (final runner sha256)

- `selftest`: 0 failures (validator accept/reject cases; redaction canary; exact permutation-p tie-inclusive expectations).
- Dry-run chains (scratch root): task 0 (SIMPLE), 12 (F0), 24 (F2) → all `COMPLETE`.
- `audit`: 32 artifacts (prompts + redacted feedback + persisted configs, chains and controls), **0 violations** (no forbidden substrings, no pinned-knob drift).
- Rollup shape on partial scratch data correctly returned `CANNOT_CHECK__TOO_FEW_COMPLETE_PAIRS`.

## 7. Verdict path

Terminal vocabulary per design §7 (`F2_METABOLIC_ADVANTAGE_MATCHED_NATIVE` / `NO_DETECTED_ADVANTAGE_MATCHED_NATIVE` / `METABOLIC_DRAG_MATCHED_NATIVE` / `CHECKER_INVALID__NO_VERDICT` / `BLOCKED_PENDING_CONTROLS` / `CANNOT_CHECK__*`). Primary: F2_final vs F0_best held-out Wasserstein (`output_graph`), exact paired sign-flip permutation p (2^12 enumeration, tie-inclusive); secondary both_best / both_final; per-dataset collapse check vs SIMPLE. Terminal receipt with gates + controls after job 3554314 completes.

skills-applied: none (dispatch receipt, no manuscript content)
