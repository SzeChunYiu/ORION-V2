# E30 R11 Terminal Results Receipt

**Receipt ID:** `E30_R11_TERMINAL_RESULTS_RECEIPT`
**Date (executed):** 2026-08-30 (redispatch job 3554274 04:27Z → eval 3554282 → analysis 3554283, all COMPLETED on LUNARC)
**Campaign:** `campaign-e30-r11-disposition-offline-core4-rep3-deficit-topup-20260828-ffcc8ed6` — 4 arms × 40 frozen BugsInPy tasks × 3 repetitions = 480 responses.
**Supersedes:** the interim `E30_R11_TERMINAL_ANALYSIS_480.json` committed with the deficit-state analysis (receipt #62: 286/480 stock, F2 5/15 checkable). The JSON in this commit is the definitive terminal analysis (F2 5/40 checkable — same successes, full denominator).

## 1. Terminal execution state

| Check | Value |
|---|---|
| Responses | **480/480** across all arms/reps; `missing_repetitions_by_task = {}` for every arm |
| Deficit repair | 13-cell redispatch (job 3554274, 43m37s): 11 cells pass 1, 1 pass 2, 2 cells pass 4 |
| Raw statuses | 480 × `COMPLETED_PROPOSAL_ONLY`; evaluations 480/480 written |
| Authority | `field_status_authorized = false`, `scientific_truth_authorized = false` ×480 |
| Analysis | `analysis_status = CONFIRMATORY_TASK_LEVEL_ANALYSIS` (40 independent frozen tasks, nested reps, Holm family size 3) |

**Endpoint nondeterminism record (binding):** the two persistently-failing cells (`F0_PARENT_FEDERATION` / `bugsinpy-pandas-5`, rep1 + rep3) failed 4 consecutive passes, then completed on pass 4 of the 12-pass re-roll loop. A spy-probe attributed the failure mode to the final synthesis call drowning in thinking past the per-call output-token cap (`stop_reason=max_tokens`, thinking-only block, zero text) — endpoint nondeterminism at temperature 0. The 12-pass design recovered it without lane changes; this supersedes any determinism framing in earlier lane-repair receipts.

## 2. Evaluable endpoint — task-level native success (registered failing test fixed)

| Arm | Success | Rate |
|---|---|---|
| `F2_ORION_METABOLIC_FULL` | 5/40 | 0.125 |
| `F0_PARENT_FEDERATION` | 5/40 | 0.125 |
| `SAME_MODEL_REFLECTION` | 4/40 | 0.100 |
| `SIMPLE_DIRECT` | 6/40 | 0.150 |

Primary comparisons (task-level, within-task majority aggregation, exact discordant test, Holm step-down α=0.05):

| Comparison | Discordants (L/R) | Exact p | Holm p | Reject |
|---|---|---|---|---|
| F2 vs SIMPLE_DIRECT | 1 / 2 | 1.0 | 1.0 | no |
| F2 vs SAME_MODEL_REFLECTION | 2 / 1 | 1.0 | 1.0 | no |
| F2 vs F0_PARENT_FEDERATION | 1 / 1 | 1.0 | 1.0 | no |

**No arm separation.** F2 does not beat any control; SIMPLE_DIRECT is numerically first. Repetition instability: 6/4/2/4 tasks flip success across the 3 reps (F0/F2/REFLECTION/SIMPLE) — endpoint noise is non-trivial at n=3.

## 3. Hard gate — `CANNOT_CHECK` (structural, not a data deficit)

`hard_gate_state = CANNOT_CHECK` with the full 480 in place. Root cause (verified in `run/e30_r11_arm_eval_frozen_lane.py`): the frozen-lane adapter — introduced 2026-08-29 to work around the stock eval lane's inability to reproduce the frozen baseline runtimes (`E30_R11_EVALUATION_LANE_DEFECT_AND_ADAPTER`) — executes **only the registered failing-test binding** (`stage="registered_failing_test"`) and writes `full_regression_suite_status = CANNOT_CHECK_NOT_RUN`, `critical_new_failure_count = None` for every task (×480). The critical-failure non-inferiority gate (F2 ≤ F0 + 0.02) is therefore **unevaluable in this lane by construction**; the analyzer correctly refuses to check it rather than imputing zeros.

## 4. Honest verdict

1. **Execution is complete and custody-clean**: 480/480 model responses, frozen oracle discipline maintained, no missing repetitions.
2. **The evaluable confirmatory endpoint is null**: no significant difference between the full metabolic architecture and any control (all Holm p = 1.0, ≤3 discordant tasks per comparison), at low absolute success (10–15%) for every arm including the strongest parent federation.
3. **The registered critical-failure hard gate remains structurally CANNOT_CHECK**: no prose may claim critical-failure safety or non-inferiority from this cell. Making the gate checkable requires a new frozen-lane stage that runs each project's full regression suite — a named follow-up, not a re-analysis.
4. `publication_readiness`, `supertheory_status`, `field_status`: `NOT_ESTABLISHED`.

**Verdict class:** `EXECUTION_COMPLETE_480_OF_480__SUCCESS_ENDPOINT_NULL_NO_ARM_SEPARATION__HARD_GATE_STRUCTURALLY_CANNOT_CHECK`

## 5. Downstream bindings

- **E60** (component ablation, array 3554276 running): released on the mechanical redispatch afterok. Its interpretation must inherit this receipt's boundary — no critical-failure endpoint claims downstream of an unchecked hard gate.
- **Paper imports** (P-C / FLAGSHIP per the E-series playbook): this cell imports as a completed-execution null with a structurally unchecked safety gate; it does not license any F2-superiority or safety claim.
- **Named follow-ups** (from `required_next` + this receipt): full-regression-suite lane extension for the hard gate; resource normalization and Pareto analysis; independent statistical/domain review; cross-domain native evaluation.

skills-applied: none (receipt, no manuscript content)
