# FM/FG R1 Suite Terminal Results Receipt

**Receipt ID:** `FMFG_R1_SUITE_TERMINAL_RESULTS_RECEIPT`
**Date (executed):** 2026-08-30 (dispatch 02:43:02 → 03:23:06 +02:00, billy-old)
**Campaign:** `.orion-formal-discovery-suite` (14 studies FM10–FM60/FG10–FG80 × 5 arms ×
8 tasks = 560 dispatches), seed 20260829, model `gpt-5.6-terra` via codex-cli 0.147.0.
**Preceded by:** `FMFG_R1_CHANNEL_REOPEN_AND_DISPATCH_BINDING_REPAIR_RECEIPT` (launch +
PR #77 repair). This receipt records the terminal execution state and the evaluated
arm table. Authority grants remain **false** — this is a recorded mixed/null cell,
not a superiority claim.

## 1. Terminal execution state

| Check | Value |
|---|---|
| Responses | **560/560** |
| Status | 560 `COMPLETED_PROPOSAL_ONLY`, 0 failures |
| run_valid | **True for all 5 arms** (missing_or_invalid = 0 everywhere) |
| Elapsed | 40 min 04 s (concurrency 2) |
| Determinism | FROZEN `d680c358…` / public `0d48bbf6…` / oracle `3cc97cf2…` (unchanged; oracle restored in `finally`) |

## 2. Evaluated arm table (112 tasks/arm, private-oracle scored)

| Arm | Accuracy | Correct |
|---|---|---|
| `TARGET_ONLY_DIRECT` | **0.8929** | 100/112 |
| `F2_STATIC_NO_FORMAL_DISCOVERY` | **0.8929** | 100/112 |
| `F2_FORMAL_DISCOVERY_FULL` | 0.8839 | 99/112 |
| `STRONGEST_DOMAIN_FORMAL_PARENT` | 0.8750 | 98/112 |
| `F0_PARENT_FEDERATION` | 0.8661 | 97/112 |

**Aggregate verdict: F2_FORMAL_DISCOVERY_FULL does NOT beat the static/no-formal
control** (−1 task of 112; the two top arms are the target-only and static controls).
`EVALUATION_SUMMARY.json.authority` = `grants_F2_superiority: false`,
`grants_new_mathematical_theory: false`, `grants_scientific_truth: false`.

## 3. Per-study structure (F2_FULL vs F2_STATIC)

- **11/14 studies tied** — and most ties sit at the 8/8 ceiling (FM10/20/40/50,
  FG10/20/30/40, FG70 at 8/8 for both; FM30 6/6, FM60 3/3 on shared failures).
  Task difficulty is low relative to all arms at n=8/study; the suite has limited
  headroom to separate arms on aggregate accuracy.
- **1 win:** FG80 F2 6/8 vs STATIC 4/8 (+2).
- **2 losses:** FG50 F2 6/8 vs STATIC 8/8 (−2); FG60 F2 7/8 vs STATIC 8/8 (−1).
- FM60 is hard for every arm (3/8 both F2 and STATIC) — a shared blind-spot study,
  useful as a difficulty anchor, not an arm separator.

## 4. Interpretation discipline (binding for imports)

1. The P-B/P-A imports must carry this cell as **CONDITIONAL/MIXED with an aggregate
   null**: no formal-discovery advantage on aggregate oracle accuracy at this design;
   one study-level positive (FG80) at +2/8; two study-level negatives.
2. The ceiling structure (11 ties) means "no difference detected" ≠ "no difference
   exists": the discriminative power of the 8-task-per-study aggregate is low. Any
   follow-up claim needs harder/larger task samples per study, not re-analysis of
   this frozen cell.
3. `grants_F2_superiority: false` in the summary is the machine-checked authority
   record; no prose may upgrade it.

## 5. Chained state

The PD dependence-evidence campaign auto-started at 03:23:06 (driver chain, `set -euo
pipefail` — evaluate exited 0) and is running (857+ response files at receipt time).
Its terminal receipt will follow separately.

## 6. Artifacts

- `~/sd10run/ORION-V2/.orion-formal-discovery-suite/EVALUATION_SUMMARY.json`
- `…/EVALUATION_ROWS.json` (per-task: task_id, arm, expected, actual, correct)
- `…/DISPATCH_RECEIPT.json`, `…/FROZEN_SUITE.json`, `…/PRIVATE_ORACLE_COMMITMENT.json`

skills-applied: none (receipt, no manuscript content)
