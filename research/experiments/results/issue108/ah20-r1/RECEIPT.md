# AH20-R1 Outcome Receipt — Epistemic Atlas / Horizon Local-to-Global Interface Suite

**Suite**: AH20 (issue #108) · **Run**: ah20-r1 · **Executed**: 2026-08-30, billy-old (`~/sd10run/.orion-ah20-r1`)
**Freeze**: `research/experiments/EPISTEMIC_ATLAS_HORIZON_AH20_SUITE_FREEZE_V1.md` (V1 FROZEN, PR #113; V14 = frozen canonical anchor)
**Implementation**: PR #116 (merge `c110670add9336a23d30a97dcb4d3b6d18d99cb5c`)

## TERMINAL: CONTROL_DIVERGENT (null — no evidence about the interface)

The frozen invariance sentinel fired **before** any K-rule: the five arms disagree on the
AHC0 (LOCAL_ONLY) control signatures, so between-arm differences on this run are confounded
by wrapper-induced baseline differences and the suite yields **no evidence about the
atlas/horizon interface itself**. Per the freeze: *"a null here is not evidence about the
interface."* The terminal is preserved verbatim; no re-scoring, no oracle change, no AH30,
no paper-endpoint change.

## Execution integrity (all green)

- 390/390 jobs dispatched and returned (78 tasks × 5 arms); `all_returncodes_zero=True`.
- Single executor throughout: `codex-cli` / `gpt-5.6-terra`; `run_valid=True` for every arm;
  `missing_or_invalid=0` everywhere (K5 not triggered).
- Custody: private oracle unlinked during dispatch, `ORION_GOLD_ACCESS=NONE` /
  `ORION_OUTCOME_ACCESS=NONE`, restored post-dispatch with `oracle_restored_hash_match=True`.
- EL10 reuse stratum byte-identical re-derivation asserted at prepare (seed 20260830);
  30 fresh AH tasks under seed 20260901. Gluing balance as frozen: 30/36/6/6.
- Resources (per arm): 78 model calls each; wall 1023–1176 s/arm at concurrency 5.

## What the control divergence is (mechanism, diagnosed)

AHC0 signatures (`local_scope_ok` over the 6 LOCAL_ONLY tasks):

| arm | signature | correct |
|---|---|---|
| SIMPLE_NATIVE | F,T,F,F,F,F | 1/6 |
| CURRENT_F0 | F,T,F,T,F,T | 3/6 |
| CURRENT_F2 | T,T,T,F,F,F | 3/6 |
| PARENT_LOCAL_GLOBAL | T,T,T,T,F,T | 5/6 |
| F2_PLUS_ATLAS_HORIZON | T,T,T,T,F,T | 5/6 |

1. **Every AHC0 failure is the same cell**: decision correct + `holds_across_contexts=True`
   over-claim. Zero decision errors in 30/30 arm-cells; zero WITNESSED gluing over-claims;
   zero VALID transport over-claims.
2. **`ah20-ahc0-05` is a universal attractor** (all five arms over-claim). Scenario text is
   structurally identical to the other five AHC0 tasks (same registry block, same
   "review proposes to treat the local selection as holding across all contexts" trap line);
   no task-specific warrant leak. Pure solver equivocation on the holds field.
3. **The failing arms are internally contradictory**: they answer `transport_verdict=INVALID`
   (correctly rejecting the globalization proposal) while simultaneously affirming
   `holds_across_contexts=True`. The 10-field contract exposes this; a single-field
   protocol would not.
4. Wrapper text shifts local-only behavior (1/6 → 5/6 across arms). This is precisely what
   the control exists to detect: the arms are not (common baseline) + (interface delta).

Runner integrity was re-verified post-hoc: kill-rule signatures recomputed from
`PER_TASK_SCORING.json` match the stored verdict exactly; scoring is internally consistent.

## Recorded metrics (descriptive only under CONTROL_DIVERGENT)

| metric | SIMPLE | F0 | F2 | PLG | IFACE |
|---|---|---|---|---|---|
| gluing_disposition_correctness (critical) | 0.218 | 0.385 | 0.269 | 0.372 | 0.308 |
| false_globalization_rate (critical, non-comp) | 0.056 | 0.111 | 0.028 | 0.056 | 0.028 |
| transport_correctness (critical) | 0.972 | 0.972 | 0.972 | 0.972 | 0.972 |
| probe_selection_correctness (critical) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| local_scope_correctness (non-critical) | 0.083 | 0.250 | 0.250 | 0.417 | 0.417 |
| decision_relevant_partition_refinement | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| false_outside_atlas_rate (non-comp) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| false_outside_atlas exact CP 95% CI | [0, 0.0499] ×5 arms (n=72) | | | | |

**McNemar × Holm family: 0 / 16 contrasts significant** (all `p_holm ≥ 0.625`). Uniform null:
transport identical across arms, probe selection at ceiling everywhere, sentinel at floor
everywhere.

## Gluing-metric structural floor (representation limit, recorded — oracle NOT altered)

The reused EL10 stratum (36 GLOBAL_SECTION_OBSTRUCTED + 6 GLOBAL_SECTION_WITNESSED cells)
and the AHC2/3 probe worlds expose **no atlas registry** in their public scenario text (the
EL10 texts were written for the locality suite; the AHC2/3 texts foreground the probe grid).
Under the interface's own contract clause — *CANNOT_CHECK where registered correspondence is
absent* — the textually faithful answer there is CANNOT_CHECK (IFACE: 36/36, 6/6, 12/12
CANNOT_CHECK on those strata), while the frozen extension-map oracle encodes the underlying
world state the text never exposes. Consequence: `gluing_disposition_correctness` has a
structural ceiling ≈ 30/78 for text-faithful arms; the measured 0.22–0.38 spread across arms
is not significant after Holm. This is a **design property of the reused-stratum
representation**, not model failure and not a scoring defect; it is recorded here as the
fiber any future suite iteration would have to repair (register the atlas blocks in the
public text, or score the reused stratum on text-derivable dispositions only). The frozen
oracle stands as executed.

## Non-claims (authority block, as frozen)

`claim_limit = "formal/interface discriminator only"`; grants_absolute_globality=False;
grants_new_kernel_family=False; grants_paper_endpoint_change=False;
grants_scientific_truth=False; grants_total_epistemic_space=False;
parent_sufficiency_is_valid_terminal=True.

## Disposition

- AH20-R1 terminal **CONTROL_DIVERGENT**, preserved verbatim; null preserved (parent wins
  stand; no interface evidence claim).
- Defects fixed pre-dispatch (PR #116): Clopper-Pearson bisection direction; `_kill_rule`
  best-other direction per metric kind; tautological selftest assert removed.
- Leads registered (not opened): (1) universal-attractor holds-field equivocation on
  ahc0-05-class texts; (2) atlas-registry absence in reused-stratum public texts. Both are
  fibers for a future suite iteration **if** one is ever warranted; AH30 remains closed and
  no paper endpoint changes.

**Artifacts**: `public_tasks.json`, `FROZEN_SUITE.json`, `DISPATCH_RECEIPT.json`,
`EVALUATION_SUMMARY.json`, `PER_TASK_SCORING.json`, `PRIVATE_ORACLE_COMMITMENT.json`
(this directory).
