# E30 R11 deficit-state analysis receipt (2026-08-29)

## What ran

LUNARC job **3553274** (`drivers/e30_analysis_r11_terminal.sbatch`), 2026-08-29T14:05:29–14:05:32Z:
validate → summarize for `confirmatory-r{1,2,3}` → cross-rep task-level analysis → raw rollup,
against the frozen campaign
`campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6`
(source commit `ffcc8ed613a6e75ce4ae530f1d25be21bd25dd3b`, sensitivity freeze sha256 prefix `4663435c3036cc18d5b6`).

## Input state (unchanged from the dispatch-deficit receipt)

This analysis consumed the **deficit-state stock**: 286/480 requests hold real model
responses (`COMPLETED_PROPOSAL_ONLY`); 194/480 are dispatch-infrastructure failure
envelopes (HTTP 429, no model output) that the frozen lane resolves to
`CANNOT_CHECK_AGENT_OR_ARTIFACT_UNAVAILABLE`. No aggregate mixes completed responses
with dispatch-failed envelopes — the failures stay in the denominator as CANNOT_CHECK.

## Results (registered pipeline output, deficit state)

- `analysis_status = CONFIRMATORY_TASK_LEVEL_ANALYSIS`; 40 frozen tasks, 3 nested repetitions,
  one weight per task; repetition audit: no missing repetitions at the file level.
- **Success endpoint** (primary, Holm α=0.05, family size 3):
  - `F2_ORION_METABOLIC_FULL_vs_SIMPLE_DIRECT`: 11/40 checkable pairs, exact discordant p=1.0, Holm p=1.0 — not rejected.
  - `F2_vs_SAME_MODEL_REFLECTION`: 9/40 checkable, exact discordant p=1.0, Holm p=1.0 — not rejected.
  - `F2_vs_F0_PARENT_FEDERATION`: 8/40 checkable, untestable (no discordant pairs) — not rejected.
- **Critical-failure endpoint**: 0 checkable tasks in every comparison — fully `CANNOT_CHECK`.
- **Wall time (secondary, descriptive)**: F2 is slower against every comparator —
  median difference +22.2 s vs SIMPLE_DIRECT (exact sign p=0.0022), +6.6 s vs SAME_MODEL_REFLECTION
  (p=0.017), +4.5 s vs F0_PARENT_FEDERATION (p=0.15); 10k bootstrap, project-stratified, seed 20260828.
- `hard_gate_state = CANNOT_CHECK`; `supertheory_status = field_status = publication_readiness = NOT_ESTABLISHED`.

## Classification

**DEFICIT_STATE_INTERIM — pipeline validation executed; NO terminal claim.**

- The registered analysis chain runs end-to-end on real deficit-state data and emits honest
  CANNOT_CHECK marks where the 429 envelopes censor the endpoint. Nothing here promotes,
  demotes, or contracts any arm: the underpowered nulls are a property of the censoring,
  not evidence of parity or of F2 harm (the wall-time cost signal is the only comparison
  with near-complete pairs, 40/40).
- The R11 terminal disposition remains **DEFERRED** exactly as recorded in
  `E30_R11_MODEL_DISPATCH_DEFICIT_RECEIPT.json`: the 194 failed requests are re-dispatched
  under the SAME frozen identity by LUNARC job **3553183** (`o2-e30r11-redis`, scheduled
  2026-09-04T13:00), after which the terminal analysis is re-run on the completed stock.

## Outcome-access statement

Deficit-state aggregates were accessed while producing this receipt. After this access no
frozen endpoint, gate, threshold, task set, or analysis parameter was modified. The
re-dispatch legitimacy argument (infrastructure failures carry no model output, same
identity, no selection on outcomes) is the one already accepted in #55.

## Artifacts

| File | sha256 |
|---|---|
| `E30_R11_TERMINAL_ANALYSIS_480.json` | `0506c8ab772ad64cc7887cc461a9de7efe3fb90fb633603df00bfefa2047bc3e` |
| `E30_R11_TERMINAL_RAW_ROLLUP.json` | `d2c030b1f934c7b04ac8acdf72ef0d4d31796ee469d3e549d9d3def54dea5dcd` |

Resolved statuses across the 480 evaluations (raw rollup): SIMPLE_DIRECT 13,
SAME_MODEL_REFLECTION 8, F0_PARENT_FEDERATION 10, F2_ORION_METABOLIC_FULL 17
(task-level resolved-success counts; see the JSON for the full tables).
