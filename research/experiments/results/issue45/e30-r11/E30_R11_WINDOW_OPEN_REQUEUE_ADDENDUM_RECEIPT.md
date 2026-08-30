# E30 R11 / E60 R1 Window-Open Requeue Addendum Receipt

**Receipt ID:** `E30_R11_WINDOW_OPEN_REQUEUE_ADDENDUM_RECEIPT`
**Date (executed):** 2026-08-30
**Supersedes:** the re-anchored chain table (§3) and queue-discipline rows 3–4 of
`E30_R11_EARLY_REDISPATCH_TERMINAL_AND_REANCHOR_RECEIPT.{md,json}` (jobs 3554177 /
3554178 / 3554179, `--begin=2026-09-04T13:00`). All other content of that receipt
(the 3553440 terminal state, the 3554050/3554051 cancellation, the 22-envelope
deficit characterization) remains governing.
**Scientific status:** UNCHANGED — R11 remains `terminal_evaluation: DEFERRED`. No
results, no evaluation, no claims. PROSPECTIVE.

## 1. Trigger: the availability window opened ~4 days early

A direct probe of the model channel (glm-5.2, 2026-08-30 ~02:15 LUNARC local)
returned HTTP 200 with a normal completion — the Sep 3–4 availability assumption no
longer held. Per the standing rule (never park dispatchable work behind a closed
window that has opened), the deferred chain was replaced immediately.

## 2. Cancellation of the deferred chain (verified from sacct)

| Job | Role | State |
|---|---|---|
| `3554177` | R11 deferred re-dispatch (`--begin=2026-09-04T13:00`) | CANCELLED by 6350 @ 2026-08-30T02:25:32 |
| `3554178_[0-23%2]` | E60 agent array | CANCELLED by 6350 @ 2026-08-30T02:25:32 |
| `3554179` | E60 terminal | CANCELLED by 6350 @ 2026-08-30T02:25:32 |

All three were PENDING (BeginTime/Dependency) at cancellation — zero envelopes
dispatched under them; stock state unchanged (R11 458/480 completed, E60 0/600
pristine).

## 3. Replacement chain (live)

| New job | Script | Gating | State @ verify |
|---|---|---|---|
| `3554200` | `e30_agents_r11_redispatch_deferred.sbatch` (begin-hold removed) | probe-confirm loop on the exact R11 channel; re-dispatches only the 22 `EXECUTION_FAILED_MODEL_RESPONSE` envelopes under the SAME frozen R11 identity; on 480/480 self-chains `e30_eval_r11_core480_single.sbatch` then (afterok) `e30_analysis_r11_terminal.sbatch` | **RUNNING since 2026-08-30T02:27:06** |
| `3554201_[0-23%2]` | `e60_agents_r1.sbatch` | `afterok:3554200` | PENDING (Dependency) |
| `3554202` | `e60_redispatch_terminal_r1.sbatch` | `afterany:3554201`; envelope recovery then eval→analysis only on full 600/600 stock, exit 3 otherwise | PENDING (Dependency) |

Guard semantics carried over unchanged from the superseded submission
(envelope-status guard, eval completeness gate, E60 full-stock gate re-read from the
submitted scripts).

## 4. Queue discipline (live squeue)

SD70 `3553181` (begin 2026-09-03T18:35) and E70-GC1 `3553088` (begin
2026-09-04T08:00) keep their begin times — no contention: the R11→E60 chain is
expected to finish well before Sep 3. Single-consumer discipline on the shared
channel is preserved by the same begin-time separation.

## 5. Next actions on terminal states

- `3554200` COMPLETED + children → `E30_R11_TERMINAL_ANALYSIS_480.json` → results
  receipt PR → P-C/Flagship import.
- `3554202` terminal → fetch `component_effects.json`, verify 600/600, results
  receipt PR → P-C lane import.
- `3554200` FAILED again → classify (channel re-closed vs new defect), deficit-state
  note, corrected re-defer; never loop-resubmit against a closed window.

skills-applied: none (receipt, no manuscript content)
