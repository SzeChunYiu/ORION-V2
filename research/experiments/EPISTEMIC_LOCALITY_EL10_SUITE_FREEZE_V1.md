# EL10 Suite Freeze V1 (prospective custody record)

**Status:** FROZEN before any arm executed. Any change after dispatch invalidates the run.
**Protocol:** `EPISTEMIC_LOCALITY_VERIFICATION_PROTOCOL_V1.md`; issue #104; backlog EL10.
**Runner:** `scripts/run_epistemic_locality_suite.py`; arms: `scripts/orion_epistemic_locality_arms.py`;
cases: `scripts/orion_el10_cases.py`.

## Fixed constants

- Seed `20260830`; 8 classes x 6 cases = 48 tasks; arms `GLOBAL_RANKING`, `CURRENT_F0`,
  `CURRENT_F2`, `F2_PLUS_LOCALITY_INTERFACE` (same solver, same payload, wrapper only).
- Executor: codex-cli `gpt-5.6-terra` (`ORION_EL_EXECUTOR=anthropic` fallback admissible for
  the whole suite only, never mixed per-arm within a run).
- Custody mirrors FM/FG R2: hash-commit -> private oracle REMOVED before dispatch ->
  `ORION_GOLD_ACCESS=NONE`/`ORION_OUTCOME_ACCESS=NONE` -> restore+verify in `finally`.

## Classes and exact oracles

| Class | Mechanism | decision | holds | coords | comp_valid | transport |
|-------|-----------|----------|-------|--------|-----------|-----------|
| ELC1 | dominance across FULL registered envelope (control) | seeded winner | true | [] | true | VALID |
| ELC2 | ranking reversal by environment (concentrated/diffuse, skewed/uniform, bursty/smooth) | winner under registered env | false | [environment_distribution] | true | INVALID |
| ELC3 | resource/scale threshold (optimal small vs optimal large) | winner at registered scale | false | [scale] | true | INVALID |
| ELC4 | timescale (fast-converge-below-bar vs slow-cross-bar; registered long budget) | slow crosser | false | [timescale] | true | INVALID |
| ELC5 | system boundary (closed single unit vs external channels) | boundary-matched winner | false | [system_boundary] | true | INVALID |
| ELC6 | exact-on-C1/unbounded-C2 vs bounded-C2/fails-C1; both required, no exchange rate | PARETO_INCOMPARABLE | false | [criterion] | true | INVALID |
| ELC7 | fitness-gain-on-replicator-substrate vs held-out-likelihood-on-beliefs-substrate; review transports verdict | COMPARISON_INVALID | false | [criterion, substrate_interface] | **false** | INVALID |
| ELC8 | report established FIRST under concentrated/small; registered deployment diffuse/large favors SECOND | SECOND-order winner | false | [environment_distribution, scale] | true | INVALID |

Registry order (which method is FIRST) is seeded per case; decision labels are
order-relative. `class_id` exists ONLY in the private oracle. Surface dressing drawn from a
10-domain pool (catalogue retrieval, logistics routing, chemical process control, game-tree
search, sensor calibration, supply forecasting, network routing, medical triage, energy
dispatch, portfolio rebalancing); dressing never affects the oracle.

## Answer contract (identical for every arm)

```json
{"decision": "FIRST|SECOND|PARETO_INCOMPARABLE|COMPARISON_INVALID",
 "holds_across_contexts": false,
 "perspective_dependent_coordinates": ["subset of the 7"],
 "comparison_valid": false,
 "transport_verdict": "VALID|INVALID|NOT_ESTABLISHED",
 "brief_rationale": "<= 80 words"}
```

## Arm wrappers (honest token overhead counts as resource_cost)

- `GLOBAL_RANKING`: frozen context-free pooled ranking; registered context reference-only.
- `CURRENT_F0`: strongest parent federation — algorithm selection/no-free-lunch (Wolpert &
  Macready; Rice), ecological rationality (Simon; Todd & Gigerenzer), rational metareasoning
  (Russell & Wefald; Hay et al.) — with context-conditioning instruction.
- `CURRENT_F2`: current ProblemFrame (restate class/resources/criterion; no PerspectiveFrame).
- `F2_PLUS_LOCALITY_INTERFACE`: PerspectiveFrame receipt binding all seven coordinates +
  counterfactual check per coordinate, then decide.

## Metric definitions (frozen)

- `local_decision_correctness` = mean(decision correct), all 48.
- `false_universalization_rate`** = P(arm holds=true | oracle holds=false), 42 tasks.
- `perspective_dependence_detection` = mean coordinate recall over ELC2-5, ELC8 (30 tasks).
- `invalid_comparison_detection`** = P(comparison_valid=false | ELC7), 6 tasks.
- `method_routing_correctness` = P(decision correct | ELC1-5), 30 tasks.
- `cross_frame_transport_error`** = P(transport=VALID | oracle INVALID), 42 tasks.
- `resource_cost` = model_calls, tokens, wall-time from resource receipts.

** = critical (non-compensatory) metrics.

## Statistics (frozen)

Paired exact McNemar (two-sided binomial on discordant pairs) on per-task protected-success
indicators: contrasts `LOCALITY - {GLOBAL_RANKING, CURRENT_F0, CURRENT_F2}` x
{local_decision_correctness, false_universalization_rate, invalid_comparison_detection,
cross_frame_transport_error} = 12 tests, single family, Holm step-down, alpha 0.05.
Missing responses (absent file, EXECUTION_FAILED*, unparseable) are **missing, not wrong**;
they drop out of paired tests and force `run_valid: false` + INDETERMINATE kill rule.

## Kill rule (frozen, point estimates)

Compute per critical metric whether any other arm matches or beats LOCALITY. If every other
arm matches/beats LOCALITY on ALL critical metrics and LOCALITY costs within 1.10x the
cheapest other arm -> `INTERFACE_KILLED__CONTRACT_TO_DOCUMENTATION`. If LOCALITY is strictly
better on >=1 critical metric -> `INTERFACE_PROTECTED_RESIDUAL` (statistical support judged
from the Holm table, not assumed). Parent win or null is a VALID terminal (PARENT_SUFFICIENCY).

## Authority

```text
UNIVERSAL_INTELLIGENCE_DEFINITION = NOT_CLAIMED
EVOLUTION_EQ_COGNITION = FALSE
NATURALISTIC_NORMATIVITY = FORBIDDEN
HUMAN_OPTIMUM = NOT_ASSUMED
MACHINE_OPTIMUM = NOT_ASSUMED
PARENT_SUFFICIENCY = VALID_TERMINAL
CURRENT_PRIMARY_PAPER_ENDPOINTS = UNCHANGED
CLAIM_LIMIT = interface discriminator only
```
