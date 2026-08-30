# E60 R1 component ablation — outcome receipt (issue #45)

**Terminal: `CANNOT_CHECK` hard gate (honest) + component block delivered.**
`field_status=NOT_ESTABLISHED`, `publication_readiness=NOT_ESTABLISHED`,
`analysis_status=CONFIRMATORY_TASK_LEVEL_ANALYSIS`. The component block — the E60
deliverable — is computed and frozen below; no component shows a certified effect on
executable native success at this scale.

## 1. Run identity and custody

| field | value |
|---|---|
| Campaign | `campaign-e60-r1-component-ablation-20260829-38aedc50` (LUNARC, account lu2026-2-51) |
| Suite | frozen manifest 38aedc50; 5 arms × 40 tasks × 3 reps = 600 responses, all `COMPLETED_PROPOSAL_ONLY` |
| Arms | F2_ORION_METABOLIC_FULL vs F2_MINUS_{DECOMPOSITION, NATIVE_RECOVERY, COUNTERPROBE, SELECTIVE_REOPEN} |
| Evaluator | frozen-lane `e30_r11_arm_eval_frozen_lane.py`, R11 source sha-asserted read-only in every job |
| Executor ceiling | PROPOSAL_ONLY throughout (no arm executed code; success = evaluator-applied patch passes native tests) |
| Analysis | 3556325 (`component_effects.json` hard-gated present) |
| Jobs | array 3554050 (600/600), chain 3554051; repairs 3555162, 3555633, eval600 3555894, repair3 3556322 → analysis 3556325 |

## 2. Execution narrative (chain repairs, all infra-level, zero science-surface change)

1. **Empty-text failure mode (3555162).** 36 envelopes failed deterministically: the arm
   model exhausts the per-call output cap on reasoning before any text block →
   `stop_reason=max_tokens`, `text=""` → `EXECUTION_FAILED_MODEL_RESPONSE`. Repair used the
   patched executor copy `repair/orion_claude_arms_empty_retry.py` (sha df0fe596…) with a
   max_tokens-doubling ladder. 598/600 after 3 passes.
2. **3555162 defects (fixed in 3555633):** final-gate shell arithmetic on captured text
   ("integer expression expected" let an incomplete stock through) → replaced by a python
   exit-code gate; ladder ceiling 16000 < designed 24000 on 2 residual items →
   `ORION_ARM_EMPTY_RETRIES=6`. 600/600 COMPLETED_PROPOSAL_ONLY.
3. **Eval ENOSPC (3555629, 1 s):** worker `mktemp /tmp/...` on a full node `/tmp`; worker
   path moved under the E60 logs dir (original preserved `.orig-enospc`).
4. **eval600 (3555894) COMPLETED 49:47** — 600/600 frozen-lane evaluations, resumable
   (`evaluation_lane` marker), deterministic local recompute, responses untouched.
5. **Single-cell falsifier repair (3556322 → analysis 3556325).** The chained analysis
   3555895 exited 2 at rep3 validation: exactly one response
   (rep3 `F2_MINUS_DECOMPOSITION/bugsinpy-scrapy-5`) was `COMPLETED_PROPOSAL_ONLY` with an
   **empty top-level `falsifier`** ("checkable response requires a falsifier"). Same draw
   class as the empty-text gate — the ladder catches empty text, not an empty falsifier
   field. Repair: old response + its stale evaluation record superseded (sha256-logged,
   `repair/superseded-r3-falsifier/`, never deleted), regenerated from the frozen rep3
   request envelope (draw 1: 708-char falsifier, cell valid), single-cell re-eval via the
   frozen-lane driver, full-stock gate `final_stock_bad=0`, analysis re-chained.

## 3. Component ablation block (success endpoint, left = F2_FULL vs right = F2_MINUS_X)

40 paired tasks per contrast, analysis unit TASK after within-task rep aggregation
(majority), bootstrap 10 000, PROJECT-stratified, seed 20260828. Arm success rates:
FULL 5/40 (0.125); MINUS_DECOMPOSITION 7/40 (0.175); MINUS_NATIVE_RECOVERY 5/40;
MINUS_COUNTERPROBE 4/40 (0.100); MINUS_SELECTIVE_REOPEN 5/40.

| contrast | paired table (both_F/both_T/L-only/R-only) | risk difference [CI95] | exact p | wall-time Δ (p) |
|---|---|---|---|---|
| vs MINUS_COUNTERPROBE | 35 / 4 / 1 / 0 | **+0.025** [0.000, 0.075] | 1.0 | +5.79 s (0.039) |
| vs MINUS_DECOMPOSITION | 33 / 5 / 0 / 2 | **−0.050** [−0.125, 0.000] | 0.5 | −3.13 s (0.006) |
| vs MINUS_NATIVE_RECOVERY | 35 / 5 / 0 / 0 | 0.000 [0, 0] | — (0 discordant) | +5.71 s (0.154) |
| vs MINUS_SELECTIVE_REOPEN | 35 / 5 / 0 / 0 | 0.000 [0, 0] | — (0 discordant) | +1.03 s (0.636) |

Reading (descriptive, no certification): removing native-recovery or selective-reopen
changes **zero** task outcomes — exactly outcome-neutral components at this scale;
counterprobe's removal loses one task the full arm solves (underpowered, p=1.0);
decomposition's removal nominally **gains** two tasks (7/40 vs 5/40, p=0.5 — the
decomposition component is if anything anti-productive here, not significant). Wall-time:
the full configuration is slower than the counterprobe-ablated arm and faster than the
decomposition-ablated arm; both other contrasts null.

## 4. Why the hard gate is CANNOT_CHECK (two registered reasons, both executed)

1. **Critical-failure endpoint unascertainable on the frozen evaluator surface.** Every
   evaluation record carries `critical_new_failure_count=null`
   (`full_regression_suite_status=CANNOT_CHECK_NOT_RUN`): the frozen lane runs the task's
   native tests, never the full regression suite, so critical new failures are never
   observed. **Parent-verified, not an E60 regression**: 120/120 sampled E30-R11
   evaluations (same frozen evaluator) are also null. The analyzer's ANY_TRUE aggregation
   therefore returns None on all 40 tasks in all five arms
   (`critical_failure_cannot_check_task_count=40` everywhere), and
   `component_disposition=CANNOT_CHECK_MISSING_OUTCOMES` on all four contrasts.
2. **Primary comparison family untestable by design.** The registered family (size 3,
   Holm) is F2 vs SIMPLE_DIRECT-style comparators, absent in this campaign by design;
   `testable_comparison_count=0, untestable=3`, `missing_tests_are_not_rejected=true`.

## 5. What this run licenses (non-claims)

Component-ablation evidence only, at the PROPOSAL_ONLY executor ceiling and 12.5% base
success rate. No component certified; no component removal recommended; the two
zero-discordant components are outcome-neutral **at this scale**, not proven inert. No
field status, no publication readiness, no naturalistic claim. P-C's open question —
whether the controller improves, harms or merely redistributes the quality-resource
frontier — remains open; this run bounds it (no component effect detectable at n=40×3).

## 6. Artifacts

`component_effects.json` (terminal artifact, hard-gated), `E60_R1_COMPONENT_ABLATION_ANALYSIS.json`
(full analysis), `summary_terminal600_r{1,2,3}.json`, `supersede.sha256` (repair-3 custody),
`PREP_RECEIPT.json`, `JOB_IDS.env` (updated chain), campaign tree on LUNARC
(`campaign-e60-r1-component-ablation-20260829-38aedc50/`).
