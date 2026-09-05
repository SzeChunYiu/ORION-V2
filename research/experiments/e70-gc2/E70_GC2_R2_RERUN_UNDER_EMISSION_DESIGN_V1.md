# E70-GC2 R2 — re-run of the frozen calibration ladder through the repaired instrument (frozen design V1)

**Identity:** `E70-GC2-R2`. **Parent design (unchanged, byte-frozen):** `E70_GC2_OFFCEILING_DESIGN_V1.json`
— ladder L1→L3, calibration window [0.30, 0.70] on the `SIMPLE_DIRECT` point estimate, 16 dev tasks
per rung, primary endpoint count-robust native success. **Reason for R2:**
`E70_GC2_INSTRUMENT_SUSPECT_RERUN_PENDING_V1.md` (instrument defects D1–D3). **Frozen:** 2026-09-05,
before any R2 model call. Channel-dependent: dispatch waits for the frozen channel's window.

## Design deltas versus the GC2 calibration run (exhaustive)

1. **Arm executable = `scripts/orion_codex_arms.py` with E80 emission** (already the runner's arm;
   the calibration run pre-dated E80). The response carries `patch_emission_receipt`.
2. **Evaluator = receipt-aware header-exact endpoint** (this PR). Nothing else in the evaluator
   changes; count-robust scoring is byte-identical.
3. **Fresh secret nonce** (design §custody): the hidden set is regenerated under a new nonce, so no
   R2 task is a GC2 task; the nonce's sha256 is committed at dispatch, the value revealed after.
4. Host **billy-old**; channel **codex-cli pinned binary / `gpt-5.6-terra`** as GC2 used; window
   opens 2026-09-07 16:25 (codex). If the served model at dispatch is not `gpt-5.6-terra`, the
   dispatcher exits 6 and retries; a mid-run drop is retried idempotently (responses on disk skipped).

No rung, count, window, endpoint, seed rule or arm set is changed. Adding rungs, re-tuning the
window or reading a contrast from the dev split is forbidden by the parent design and stays so.

## Pre-registered expectation and routing

Expectation: every rung above the window on count-robust success (saturation confirmed);
header-exact endpoint reported per rung and routes nothing. Routing = the parent's calibration
routing verbatim (`WINDOW_HIT` → protected generation under the parent design;
`CALIBRATION_INVALID_UNSCORABLE_CELLS`; all rungs outside → `SUITE_STILL_SATURATED`, re-labelled
`INSTRUMENT_REPAIRED__SATURATION_CONFIRMED` for the R5 row).

## Authorization and dispatch

`PROTECTED_RUN_AUTHORIZATION.json` (ME-X shape) minted from the operator's standing verbatim
authorization ("run all the computation tasks.. finish all the researxh asap", 2026-09-02;
reaffirmed 2026-09-04 "i sign off everything…") is written on the dispatch host immediately before
`run_orion_generated_composition_gc2_pilot.sh` is invoked and archived after. The deferred dispatcher
is `~/sd10run/e70_gc2_r2_deferred_dispatch.sh` on billy-old (log
`~/sd10run/logs-fmfg/e70-gc2-r2-deferred.log`); it refuses to start without the authorization file.

## Authority

Calibration evidence only. Grants no arm comparison, no scientific truth, no P-C terminal change.
`NO NOVELTY OR BREAKTHROUGH CLAIM`.

skills-applied: none (frozen design, no manuscript content)
