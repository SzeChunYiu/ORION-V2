# ORION-V2 Real-Problem Analysis Plan V1

**Status:** prospective statistical and decision-analysis plan. No outcome has been inspected or encoded.

## 1. Primary question

Does `F2_ORION_METABOLIC_FULL` improve justified real-problem performance beyond `F0_PARENT_FEDERATION`, `SIMPLE_DIRECT` and `SAME_MODEL_REFLECTION` while preserving non-compensatory scientific-integrity and authority constraints and exposing its resource cost?

## 2. Experimental units

- Primary unit: frozen real task.
- Repeated stochastic model runs are nested within task and arm.
- Benchmark/domain is a prespecified stratum, not an interchangeable replicate.
- Human-expert runs are separately identified and never silently pooled with model runs.

## 3. Tranches

### T0 — reference semantics

Unit tests and manifest validation. No empirical inference.

### T1 — execution pilot

Three gold-blind BugsInPy tasks across selected arms. Purpose:

- confirm checkout, agent protocol, patch application and evaluator execution;
- identify pre-outcome infrastructure defects;
- estimate runtime for the confirmatory budget.

T1 cannot establish superiority or paper-level value.

### T2 — debugging confirmation

At least 40 frozen BugsInPy tasks across at least eight projects, with paired arm coverage and at least three stochastic repetitions where model nondeterminism is material.

A smaller completed set is reported but marked underpowered relative to this plan.

### T3 — cross-domain confirmation

CausalBench and Matbench Discovery native evaluations, with exact data/checkpoint/metric identities and at least one independent domain adjudicator per domain.

General Machine Epistemics or P-G claims require at least two materially different domains beyond reference fixtures.

## 4. Primary outcomes

### O1 — executable/native success

Binary or native benchmark success under a frozen evaluator.

### O2 — critical false completion

The arm reports success or scientific closure while native evaluation fails, a hard authority/source condition fails, or a materially necessary test/oracle is absent.

### O3 — protected decision quality

Domain-specific quality vector including unsafe transport, invalid causal/material decision, selective reopening and calibrated `CANNOT_CHECK`.

### O4 — resource use

Wall time, compute, memory, model tokens, external tool calls, human minutes and implementation/evaluator burden.

## 5. Primary estimands

For paired tasks:

- risk difference in executable/native success: `F2_FULL − comparator`;
- risk difference in critical false completion;
- median and mean paired wall-time/compute difference;
- success per normalized resource unit;
- task-level Pareto dominance count;
- proportion of tasks on which the simple or parent method is locally preferable.

For cross-domain outcomes, report each domain separately before any aggregate.

## 6. Non-compensatory gate

F2 cannot be labelled a dominance candidate when any of these materially regress beyond the frozen tolerance:

- critical false completion;
- source/evidence integrity;
- criterion identity;
- unsafe transport;
- native-parent critical fidelity;
- authority/custody;
- outcome leakage;
- hidden resource advantage.

An average gain cannot offset a critical gate failure.

## 7. Minimum important differences

These are design thresholds, not guaranteed detectable effects:

- absolute executable-success improvement: 5 percentage points over F0;
- critical-failure non-inferiority margin: no more than 2 percentage points worse than F0, with zero tolerance for authority/source corruption events;
- efficiency advance: at least 20% reduction in a registered resource coordinate at non-inferior scientific quality;
- component necessity: removal causes at least a 5-point success loss, 2-point critical-failure increase, or a material native-fidelity/authority regression on the component’s designated stratum.

Exact confidence intervals and observed uncertainty remain primary; thresholds do not convert weak evidence into success.

## 8. Statistical methods

### Binary paired outcomes

- report paired 2×2 tables;
- exact two-sided McNemar/sign-binomial test on discordant pairs;
- paired task bootstrap confidence interval with a frozen random seed;
- task-level results remain visible.

### Continuous resource outcomes

- report median, interquartile range and paired differences;
- bootstrap confidence intervals stratified by benchmark/project;
- show full quality–resource Pareto curves rather than one weighted score.

### Stochastic repetitions

- aggregate within task/arm first;
- report between-run variance and failure instability;
- do not treat repeated seeds as independent tasks.

### Cross-domain synthesis

- domain-specific effects first;
- random-effects or hierarchical synthesis only after at least three suitable domains and independent statistical review;
- no universal effect inferred from software debugging alone.

## 9. Multiplicity

Primary confirmatory comparisons:

1. F2_FULL vs F0;
2. F2_FULL vs SIMPLE_DIRECT;
3. F2_FULL vs SAME_MODEL_REFLECTION.

Component comparisons are secondary mechanistic analyses. Report all registered comparisons. Use Holm correction for the three primary binary-success hypothesis tests, while retaining unadjusted effect intervals for interpretation.

## 10. Component attribution

Required interventions:

- `F2_MINUS_DECOMPOSITION`;
- `F2_MINUS_NATIVE_RECOVERY`;
- `F2_MINUS_COUNTERPROBE`;
- `F2_MINUS_SELECTIVE_REOPEN`;
- strongest-parent replacement;
- merged/simplified variant where supported;
- selected pair interventions when stage synergy was registered before full outcome inspection.

Each component receives one disposition:

```text
NECESSARY
PARENT_REPLACEABLE
CONTEXTUAL
REDUNDANT_DRAG
HARMFUL
CANNOT_CHECK
```

## 11. Activation-policy analysis

The full lifecycle is not expected to dominate every task. Estimate whether a pre-outcome activation rule can identify tasks on which ORION complexity is material.

Features may include:

- number of source/knowledge modes;
- number of live causes/hypotheses;
- dependence/authority complexity;
- need for cross-representation transport;
- evaluator/oracle uncertainty;
- failure recurrence/history;
- simple-control success estimate.

Activation-policy training and evaluation must use separate task folds. Outcome-conditioned manual gating is prohibited.

## 12. Anti-copy analysis

Report converging evidence rather than a binary “not memorized” claim:

- gold/fixed solution access audit;
- network and retrieval access;
- newly generated permutation/counterfactual identity;
- hidden-test or held-out-intervention outcome;
- patch/artifact similarity to known solution after scoring;
- correctness under changed identifiers/labels/units;
- source-use receipt;
- retrieval-off and no-memory comparisons.

Textual dissimilarity is never a primary endpoint.

## 13. Missingness and failures

- missing model credentials, unavailable data and evaluator failures are `CANNOT_CHECK`, not losses or successes;
- timeouts are reported separately from incorrect solutions;
- infrastructure failures are retained and classified;
- tasks cannot be removed after observing which arm fails;
- a benchmark task found invalid for all arms is reported and excluded only under an outcome-blind rule applied symmetrically.

## 14. Paper decision rules

### P-C/P-D bounded result

May advance when T2 yields a protected control/assurance result with matched baselines and component evidence.

### P-G standalone survival

Requires:

- protected residual beyond F0;
- component attribution to the full lifecycle or a distinctive subset;
- at least two materially different domains;
- no critical hard-gate regression;
- independent semantic evaluation;
- resource-matched value.

Otherwise P-G merges into P-A–P-D.

### Flagship field claim

Requires specialist frozen results, cross-domain survival and external parent-field demarcation. The real-problem suite alone cannot found the field.

## 15. Result-reporting template

Every table must include:

- task and benchmark counts;
- arm/checkpoint/version identities;
- resources and missingness;
- point estimate and uncertainty;
- hard failures;
- simple/parent wins;
- `CANNOT_CHECK`;
- whether the evidence is T1, T2 or T3;
- claim IDs the result can update.

## Current terminal

```text
ANALYSIS_PLAN = FROZEN_BEFORE_RESULTS
T1_PILOT = NOT_RUN
T2_CONFIRMATORY = NOT_RUN
T3_CROSS_DOMAIN = NOT_RUN
P_G_SURVIVAL = CANNOT_CHECK
SUBMISSION_READY = FALSE
```
