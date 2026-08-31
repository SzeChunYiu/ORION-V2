# ME-X2 — Discrepancy Locus Diagnosis and Minimum-Sufficient Escalation V1

**State date:** 2026-09-01  
**Status:** prospective protocol; no protected outcomes inspected  
**Parent protocol:** `MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.*`  
**Framework object:** `src/orion_v2/ontic_epistemic_boundary.py`

## 1. Scientific correction

ME-X2 is not merely a taxonomy of why an agent failed. It tests a harder two-axis control problem:

1. **Where is the discrepancy located?** Target/world, observation/measurement, epistemic model, representation/generative regime, process/tool/workflow, or unresolved.
2. **What is the minimum scientifically responsible intervention?** Continue ordinary action, local repair, model expansion, representation change, problem reformulation, tool/instrument invention, workflow revision, framework revision, or externally governed constitution change.

The first axis must not be collapsed into the second. The same surface symptom can arise from different loci and therefore warrant different actions.

## 2. Ontic–epistemic separation

The target/world is not the epistemic machine. Let the relevant external state be represented schematically by `omega_t`, with observations generated through a registered context/instrument channel. The acting system does not receive privileged access to `omega_t`.

A registered case may independently establish that the target changed, the observation channel changed, the machine's epistemic state changed, or its generative regime changed. These are distinct events:

- target change is an ontic transition;
- observation-channel change is a measurement/interface transition;
- epistemic-state change is learning/revision;
- generative-regime change is machine self-revision;
- process/tool/workflow change is a research-system transition.

Static-target cases with valid epistemic learning and changing-target cases with no detectable observation are mandatory controls.

## 3. Locus labels

Protected known-answer cases use the following registered locus set only when the evidence supports such a label:

- `TARGET_WORLD`
- `OBSERVATION_MEASUREMENT`
- `EPISTEMIC_MODEL`
- `REPRESENTATION_REGIME`
- `PROCESS_TOOL_WORKFLOW`
- `CANNOT_IDENTIFY`

`CANNOT_IDENTIFY` is required when the protected evaluator cannot discriminate the remaining loci. It is not scored as a failure when the ground-truth/adjudication contract itself is indeterminate.

## 4. Intervention ladder

The intervention axis inherits the existing ORION-V2 Jump levels without presuming that the ladder is scientifically superior:

0. `ACTION_PARAMETER`
1. `LOCAL_REPAIR_COMPOSITION`
2. `MODEL_HYPOTHESIS_EXPANSION`
3. `REPRESENTATION_REGIME_TRANSITION`
4. `PROBLEM_OBJECTIVE_REFORMULATION`
5. `METHOD_TOOL_INSTRUMENT_INVENTION`
6. `WORKFLOW_META_SKILL_REVISION`
7. `FRAMEWORK_REVISION`
8. `CONSTITUTION_PROPOSAL` — only under an explicit external-authority test.

A correct locus diagnosis does not by itself authorize the corresponding intervention. Higher-level actions remain subject to witnessed obstruction, prospective discrimination, lower-level disposition, preservation/falsifier contracts and parent-sufficiency checks.

## 5. Paired hostile case families

Every major symptom family should contain pairs or triplets whose observable surface is deliberately similar while the responsible locus differs.

### X2-A — prediction residual

- target truly changes;
- sensor/calibration drifts while target is stable;
- model family is misspecified while sensor and target are stable.

### X2-B — repeated theorem/proof failure

- ordinary search budget is insufficient;
- a missing lemma/model expansion is sufficient;
- the current representation is the blocker;
- the intended formal specification is wrong.

### X2-C — experimental non-discrimination

- more samples under the same probe are sufficient;
- the measurement/evaluator is blind to the relevant failure class;
- a new intervention/probe is required;
- candidate hypotheses are genuinely indistinguishable under the declared experiment class.

### X2-D — workflow failure

- individual scientific methods are adequate but orchestration loses a dependency;
- a tool/instrument is defective;
- the target model is wrong despite a correct workflow;
- no higher-level change is needed because a local repair resolves the issue.

### X2-E — representation temptation negative control

Cases are deliberately constructed so that an attractive representation/model/workflow change adds cost or semantic drift while a lower-level repair is sufficient.

## 6. Baselines

All arms receive matched task information, tools, evaluators and resource accounting.

- `B0_RETRY_SEARCH` — direct system with additional matched search/retry.
- `B1_UNCERTAINTY_ABSTENTION` — confidence/calibration plus abstention.
- `B2_ARFT_STYLE_FAILURE_DIAGNOSIS` — failure-pattern diagnosis without ME-specific locus/intervention coupling.
- `B3_MODEL_BASED_DIAGNOSIS_METAREASONING` — mature diagnosis + rational metareasoning/VoI.
- `B4_MDA_STYLE_MODEL_EXPANSION` — predictive-check model-family inadequacy and expansion where applicable.
- `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` — strongest applicable composition with ordinary engineering glue.
- `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION` — explicit locus hypotheses plus existing witnessed Jump routing.

Weak-baseline victories do not support a Machine Epistemics residual.

## 7. Primary outcomes

Report a vector, not a single pooled score:

- exact/partial locus classification and calibration;
- `CANNOT_IDENTIFY` calibration;
- minimum intervention-level accuracy;
- false escalation and missed escalation;
- target-change false attribution;
- sensor/model/representation confusion matrix;
- verified task/scientific-transition success;
- intervention cost and total resource cost;
- regret relative to the registered minimal responsible intervention;
- recurrence after intervention;
- semantic/specification damage caused by unnecessary transformation.

## 8. Mechanistic requirement

A claimed ME-X2 gain requires all of the following:

1. locus diagnosis is better calibrated than the strongest parent federation or provides a nonredundant protected distinction;
2. locus information predicts the intervention that actually succeeds under the registered cost/validity criterion;
3. removing or scrambling locus information reduces routing quality in a prospective ablation;
4. the gain is not explained by more retries, more tool access, extra protected labels or a more permissive evaluator;
5. at least one effect transfers to an independently authored/native-reviewed domain.

If the ME arm succeeds while its locus diagnosis is wrong or unused, the proposed mechanism is not supported.

## 9. Required ablations

- `M_MINUS_LOCUS_DIAGNOSIS`
- `M_LOCUS_LABELS_SHUFFLED`
- `M_MINUS_LOWER_LEVEL_DISPOSITION`
- `M_MINUS_PROSPECTIVE_DISCRIMINATOR`
- `M_ALWAYS_ESCALATE_WHEN_STUCK`
- `M_NEVER_ESCALATE`

## 10. Kill and contraction conditions

Contract the ME-X2 residual if any of these holds on protected evidence:

- B3/B5 matches or exceeds the locus/routing quality-cost frontier;
- ARFT-style failure diagnosis plus metareasoning reproduces the same intervention decisions;
- the locus taxonomy is unstable under native-domain or changed-vocabulary reconstruction;
- gains disappear after matching retry/search/tool budgets;
- false escalation or semantic damage offsets success gains;
- the system systematically converts uncertainty into a forced causal locus;
- target/world-change labels rely on privileged oracle information unavailable to the acting system;
- representation-change advantage disappears against the strongest representation/lemma/model-discovery parent.

Parent sufficiency is a successful scientific terminal.

## 11. Evidence custody

Before protected execution freeze exact case IDs, observable information, hidden adjudication labels, target/observation/model/process intervention identities, evaluator contracts, budgets, seeds, primary outcomes and tie/contraction rules. The acting system must never receive protected locus/oracle labels.

## Terminal

```text
ME_X2_STATUS = PROSPECTIVE_UNEXECUTED
WORLD_IS_MACHINE = FALSE
LOCUS_AXIS = TARGET__OBSERVATION__MODEL__REPRESENTATION__PROCESS__UNRESOLVED
INTERVENTION_AXIS = EXISTING_JUMP_LADDER_AS_COMPARATOR_NOT_ASSUMED_TRUTH
B5_STRONGEST_PARENT = PRIMARY_COMPARATOR
TARGET_CHANGE_ORACLE_VISIBLE_TO_AGENT = FALSE
PARENT_SUFFICIENCY = VALID_TERMINAL
FIELD_STATUS_AUTHORITY = NONE
```
