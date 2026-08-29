# ORION-V2 Component Value, Efficiency and Removal Protocol — Wave 06 V1

**Status:** mandatory pre-freeze evaluation protocol. It is designed to answer whether every framework concept improves the scientific harness, merely adds overhead, duplicates a mature parent, helps only in a narrow context, or actively harms performance. It grants no component survival, kernel freeze or scientific authority before the protected interventions are run.

## 1. Why an ordinary ablation table is insufficient

A framework component can matter in several different ways:

- it can prevent a rare but critical false completion while changing no average score;
- it can reduce compute or latency without changing scientific decisions;
- it can be useful only when another component is present;
- it can be replaceable by a mature parent implementation;
- it can help one task family and hurt another;
- it can add logging language without changing any protected decision;
- it can increase the implementation and failure surface enough to outweigh a small gain.

Therefore ORION-V2 will not use one blended “performance score” to decide component ownership. Critical scientific/integrity failures are non-compensatory. Quality and cost are represented as a Pareto vector. Individual and interaction effects are evaluated separately.

## 2. Evaluation cell

Six roles are required for each component family:

1. **scientific-decision owner** — states the exact downstream decision the component is supposed to change;
2. **strongest-parent reviewer** — supplies a mature replacement rather than a deliberately weak ablation;
3. **causal/experimental-design reviewer** — freezes matched intervention arms and prevents outcome-conditioned redesign;
4. **systems-efficiency reviewer** — measures latency, compute, memory, annotation and implementation/failure burden;
5. **hostile safety/authority reviewer** — protects rare non-compensatory cases and looks for fail-open behaviour;
6. **independent semantic evaluator** — adjudicates cases that do not have an exact known answer.

The component author may define the hypothesis but may not be the sole final semantic evaluator.

## 3. Unit of evaluation

A **component** can be:

- a stable interface candidate;
- a policy or diagnosis mechanism;
- a metadata coordinate;
- a human-epistemics research object;
- a parent adapter;
- a compatibility layer;
- a benchmark-only fixture.

The protocol evaluates a component at the smallest intervention boundary that can be disabled or replaced without silently changing unrelated information, resources or criteria.

A component is never credited merely because its name appears in the full configuration.

## 4. Frozen arms

For each component `c`, run matched cases under at least:

1. **FULL** — current candidate configuration containing `c`;
2. **MINUS-c** — `c` removed while all other information, tools, budgets and criteria remain fixed;
3. **PARENT-c** — `c` replaced by the strongest practical mature parent implementation under matched information/resources;
4. **MERGED-c** — where relevant, the functionality is absorbed into an adjacent interface rather than kept as a separate component;
5. **SIMPLE CONTROL** — the smallest direct method capable of solving the case;
6. **NEGATIVE CONTROL** — a case in which `c` should add no value and should not force extra work;
7. **HOSTILE CONTROL** — a case in which removal should expose the exact failure the component claims to prevent.

For interacting components, run the 2×2 intervention:

`FULL`, `MINUS-a`, `MINUS-b`, `MINUS-{a,b}`.

Higher-order interactions are tested only when pair results or theory show that pairwise analysis is insufficient; exhaustive powerset ablation is not assumed feasible.

## 5. Protected outputs

### Non-compensatory coordinates

- false completion;
- unsafe transport/reuse;
- authority violation;
- evidence/source corruption;
- criterion drift;
- protected capability loss.

Any new critical failure blocks a claim of improvement regardless of speed or average score.

### Scientific-quality coordinates

Depending on the paper/case:

- justified-terminal rate;
- correct `CANNOT_CHECK` rate;
- remote-parent recall and false-analogy rate;
- relation/native-verdict preservation;
- diagnosis/probe value;
- selective-reopen correctness;
- calibration and review-trigger utility;
- prospective opportunity value;
- unnecessary refusal/escalation;
- recurrence after failure;
- transfer under changed context.

### Cost vector

`Cost = (latency, compute, memory, annotation, implementation)`.

The implementation coordinate includes maintenance burden, interface complexity, extra failure modes and evaluator burden. It is not reduced to lines of code alone.

### Pareto rule

A configuration dominates another only when it is no worse on hard scientific validity, no worse on scientific quality and no worse on every declared cost coordinate, with at least one strict improvement. Hard-valid configurations can dominate faster invalid ones; invalid speed cannot purchase scientific permission.

## 6. Component dispositions

The executable reference object uses the following statuses:

- `NECESSARY` — removal causes a protected scientific regression not recovered by a strongest parent replacement;
- `PARENT_REPLACEABLE` — removal hurts, but a mature parent replacement preserves the protected decision at no greater cost;
- `EFFICIENCY_IMPROVING` — inclusion preserves science and strictly improves at least one cost coordinate without worsening another;
- `CONTEXTUAL` — the component helps some declared strata and harms or adds material cost in others; it must be gated rather than universally active;
- `REDUNDANT_DRAG` — removal preserves protected decisions/quality and strictly reduces cost or failure surface;
- `HARMFUL` — removal repairs a critical failure or materially improves scientific quality;
- `NO_MEASURABLE_VALUE` — matched evidence finds no material decision or cost difference;
- `CANNOT_CHECK` — matched interventions, independent outcomes or required identities are unavailable.

A kernel component should normally require `NECESSARY` evidence on at least one protected cross-domain decision and no undispositioned harmful stratum. `PARENT_REPLACEABLE`, `CONTEXTUAL`, `REDUNDANT_DRAG` and `NO_MEASURABLE_VALUE` components do not earn universal kernel ownership.

## 7. Interaction dispositions

Pair interventions estimate:

`I(a,b) = u(ab) - u(a) - u(b) + u(∅)`

on bounded hard-valid scientific utility.

- positive material interaction: `SYNERGISTIC` / complementary;
- negative material interaction: `SUBSTITUTABLE` / redundant alternatives;
- near zero: `ADDITIVE`;
- different signs across strata: `CONTEXTUAL_INTERACTION`;
- invalid full reference or missing arms: `CANNOT_CHECK`.

This prevents a false conclusion that a component is useless because its substitute remains active, or that two individually valuable components deserve double credit for the same function.

Shapley/Harsanyi-style attribution may be used as a secondary analysis for larger coalitions, but it cannot replace the protected hard-failure gates and is sensitive to the declared coalition universe and replacement intervention.

## 8. Component survival gate

A concept survives as a stable interface only if the evidence bundle contains:

1. **decision witness** — a named protected decision changes when it is removed;
2. **causal intervention** — matched removal/replacement, not correlation with a successful run;
3. **strong parent comparison** — the parent receives the same information and resources;
4. **negative control** — the component stays quiet when irrelevant;
5. **interaction audit** — no hidden substitute or required partner invalidates the individual conclusion;
6. **cost profile** — latency, compute, memory, annotation and implementation burden;
7. **cross-context test** — at least one materially different domain/epoch when universality is claimed;
8. **expiry/revalidation condition** — when the component's value evidence must be rerun;
9. **independent evaluation** where no exact known answer exists;
10. **honest terminal** — removal, merging, parent replacement or `CANNOT_CHECK` is allowed.

## 9. How ORION can know that research is improving rather than merely growing

No finite programme can be certain in an absolute sense. ORION can make improvement claims increasingly difficult to fake through a layered evidence ladder:

1. **logical/known-answer tests** for invariants and fail-closed semantics;
2. **frozen hostile cases** that target the proposed failure mechanism;
3. **component interventions and parent replacements**;
4. **held-out and cross-domain cases**;
5. **prospective protocols** for future-value claims;
6. **independent blinded semantic review**;
7. **uncertainty/effect-size and negative-result reporting**;
8. **replication under changed implementation/evaluator**;
9. **longitudinal revaluation** after criteria, environments or dependencies change;
10. **contraction** when a component no longer earns its cost.

Reading more literature improves the hypothesis space; it does not prove the framework. A component becomes credible only when a frozen prediction survives an intervention and its strongest alternative.

## 10. Harness-level efficiency accounting

The full harness is evaluated against at least three comparators:

- direct/simple method;
- strongest parent-composed system;
- ORION full candidate.

Report:

- protected scientific reach;
- critical-failure counts;
- cost per justified terminal;
- cost per newly discharged obligation;
- unnecessary action/escalation count;
- reviewer/annotation burden;
- state and receipt growth;
- failure surface introduced by the harness itself.

A larger harness is rejected when it produces no protected reach beyond the parent/simple controls or when a smaller configuration Pareto-dominates it.

## 11. Current implementation

Reference module:

`src/orion_v2/component_value.py`

Known-answer tests:

`tests/unit/test_component_value_wave6.py`

The module implements:

- non-compensatory result dominance;
- per-case Pareto frontiers;
- component dispositions;
- strongest-parent replacement logic;
- pair complementarity/substitutability.

It is research infrastructure and is intentionally not exported from the candidate stable kernel facade.

## 12. Parent methods informing the protocol

Relevant parent families include controlled ablation, causal mediation/component attribution, Shapley and Harsanyi interaction analysis, data valuation, pruning/circuit discovery, sensitivity analysis, Pareto multi-objective evaluation and rational metareasoning. Recent technical examples include component modeling/COAR (ICML 2024), optimal ablation (NeurIPS 2024), causal head gating (NeurIPS 2025), interaction/dependence decompositions (AISTATS 2025) and Shapley-based data/component valuation. These methods own their native estimators; ORION uses them as candidate adapters rather than claiming a new attribution theory.

## Current terminal

```text
COMPONENT_VALUE_PROTOCOL = FROZEN_FOR_REFERENCE_CASES
COMPONENT_SURVIVAL_RESULTS = NOT_YET_PROTECTED
AVERAGE_SCORE_ONLY = REJECTED
HARD_FAILURE_COMPENSATION = FORBIDDEN
PARENT_REPLACEMENT = REQUIRED
PAIR_INTERACTION_AUDIT = REQUIRED_WHEN_MATERIAL
REDUNDANT_OR_HARMFUL_COMPONENT_REMOVAL = AUTHORIZED_BY_FUTURE_PROTECTED_RECEIPT_ONLY
KERNEL_FREEZE = BLOCKED
```
