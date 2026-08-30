# E30 R11 Early Re-dispatch Terminal State + Chain Re-anchor Receipt

**Receipt ID:** `E30_R11_EARLY_REDISPATCH_TERMINAL_AND_REANCHOR_RECEIPT`
**Date (executed):** 2026-08-30
**Campaign:** `campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6`
(LUNARC `/projects/hep/fs9/users/scyiu/orion-v2-e45/`)
**Scientific status:** UNCHANGED — R11 remains `terminal_evaluation: DEFERRED` per
`E30_R11_MODEL_DISPATCH_DEFICIT_RECEIPT.json`. This receipt records only execution state
and the recovery sequencing. No results, no evaluation, no claims. PROSPECTIVE.

## 1. Early re-dispatch job 3553440 — terminal state

| Field | Value |
|---|---|
| Job | `3553440` (`e30_agents_r11_redispatch_early.sbatch`) |
| State | FAILED, exit `3:0` (by design: completeness gate) |
| Elapsed / ended | `06:29:58` / 2026-08-30T01:55:50 (sacct, LUNARC local) |
| Guard log (final) | `FINAL response statuses: {'COMPLETED_PROPOSAL_ONLY': 458, 'EXECUTION_FAILED_MODEL_RESPONSE': 22}` |
| Chain decision | `STOCK_INCOMPLETE_PENDING_22 -- eval NOT chained` |

- The guarded loop recovered the stock substantially (started from the 194-envelope
  deficit of array 3552883) but could not clear the last 22 envelopes against the same
  model-dispatch unavailability (429-class envelope failures; no model output inside,
  so untouched completed envelopes were never at risk — the one-shot command only
  re-fires while `status==EXECUTION_FAILED_MODEL_RESPONSE`).
- Exit 3 with no chained eval is the **designed** refusal: no partial-terminal
  evaluation of a 458/480 stock can occur. The 22-task deficit is governed by
  `E30_R11_MODEL_DISPATCH_DEFICIT_RECEIPT.json` (re-dispatch exactly the remaining
  requests under the SAME frozen R11 identity, in the Sep 3–4 availability window,
  same root-cause class as SD70 job 3553181 and E70-GC1 job 3553088).
- Failure clustering of the 22 (bugsinpy-pandas-2/5, fastapi-1/4, black-5, tornado-4,
  tqdm-2, pandas-4) is dispatch-side, not content-side: identical envelope status
  across heterogeneous repos/tasks.

## 2. Stranded E60 dependency chain — cancelled and re-anchored

Consequence of 3553440 failing: the E60 R1 chain entered `DependencyNeverSatisfied`.

| Old job | Role | Action |
|---|---|---|
| `3554050` (`0-23%2`) | E60 agent array, `afterok:3553440` | **CANCELLED** (never ran; 0 shards executed) |
| `3554051` | E60 terminal chain, `afterany:3554050` | **CANCELLED first** (safe order: terminal before array, so `afterany` could not release on array cancellation) |

Both show `CANCELLED+ 2026-08-30T02:01:21`; no E60 envelopes were dispatched, so the
E60 campaign stock is untouched (0/600 → still pristine; `PREP_RECEIPT.json` remains
the governing prospective state).

## 3. Re-anchored chain (submitted 2026-08-30)

| New job | Script | Gating |
|---|---|---|
| `3554177` | `e30_agents_r11_redispatch_deferred.sbatch` | `--begin=2026-09-04T13:00`; probe-confirm loop on the exact R11 channel; re-dispatches only the 22 failed envelopes; **on 480/480 self-chains `e30_eval_r11_core480_single.sbatch` then (afterok) `e30_analysis_r11_terminal.sbatch`** |
| `3554178` | `e60_agents_r1.sbatch` (array `0-23%2`) | `afterok:3554177` (command-line override of the stale baked `afterok:3553440`) |
| `3554179` | `e60_redispatch_terminal_r1.sbatch` | `afterany:3554178`; recovers failed envelopes, chains E60 eval→analysis only on full 600/600 stock (exit 3 otherwise) |

Queue discipline (single-consumer on the shared model channel):
SD70 `3553181` (begin 2026-09-03T19:30) → E70-GC1 `3553088` (begin 2026-09-04T08:00)
→ R11 deferred re-dispatch `3554177` (begin 2026-09-04T13:00) → E60 array `3554178`.

## 4. Verification performed

1. `sacct -j 3554050,3554051` → both `CANCELLED+ 2026-08-30T02:01:21` (cancels landed;
   asserted from sacct, not from absent squeue output).
2. `squeue` post-submit → `3554177 PENDING (BeginTime)`, `3554178_[0-…] PENDING
   (Dependency)`, `3554179 PENDING (Dependency)` — dependencies resolved against live
   job ids, no `DependencyNeverSatisfied`.
3. Guard semantics re-read from the submitted scripts: envelope-status guard intact;
   eval completeness gate intact; E60 terminal full-stock gate intact.

## 5. Next actions on terminal states

- `3554177` COMPLETED + children done → `E30_R11_TERMINAL_ANALYSIS_480.json` lands in
  the campaign root → results receipt PR → P-C/Flagship import.
- `3554179` terminal → fetch `campaign-e60-r1-component-ablation-20260829-38aedc50/run/aggregate/component_effects.json`,
  verify 600/600, results receipt PR → P-C lane import.
- `3554177` FAILED again → classify (channel still walled vs new defect), deficit-state
  note, corrected re-defer; never loop-resubmit against a closed window.

skills-applied: none (receipt, no manuscript content)
