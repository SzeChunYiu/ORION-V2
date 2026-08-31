# ME-X2 — Discrepancy Locus Diagnosis and Minimum-Sufficient Escalation V2

**State date:** 2026-09-01  
**Status:** prospective protocol; no protected outcomes inspected  
**Supersedes design:** `ME_X2_LOCUS_DIAGNOSIS_PROTOCOL_V1.md` for future execution; V1 remains immutable history  
**Reference semantics:** `src/orion_v2/ontic_epistemic_boundary.py`

## Central discriminator

ME-X2 asks whether a machine can use evidence to distinguish **where a scientific discrepancy is located** and whether that distinction improves the choice of the **minimum scientifically responsible intervention**, beyond the strongest faithful combination of failure diagnosis, measurement diagnostics, metareasoning, model discovery and domain-native controls.

The target/world is not the epistemic machine. The acting system never receives a hidden oracle stating what actually changed.

## Axis A — discrepancy locus

Register competing hypotheses only when meaningful in the native domain:

1. `TARGET_WORLD` — the external target/system materially changed;
2. `OBSERVATION_MEASUREMENT` — sampling, sensing, calibration or measurement relation changed/failed;
3. `EPISTEMIC_MODEL` — the current scientific/model family is inadequate;
4. `REPRESENTATION_REGIME` — the representational/operator regime blocks warranted progress;
5. `PROBLEM_CRITERION` — the registered problem, objective, success criterion or formal specification is wrong/inadequate;
6. `EVALUATOR_VALIDATION` — the scientific test/oracle/evaluator is blind, invalid or mis-scoped;
7. `PROCESS_TOOL_WORKFLOW` — the implementation, tool, orchestration or workflow is responsible;
8. `CANNOT_IDENTIFY` — evidence does not discriminate the live hypotheses.

This is an operational interface, not a universal ontology. Native-domain review may contract, split or reject a locus before protected use.

## Meta-evaluator separation

A scientific evaluator can itself be the object under diagnosis. Therefore ME-X2 distinguishes:

- the **scientific evaluator/validation contract** that may be defective; from
- the **diagnostic evaluator** used to decide whether evidence discriminates competing locus hypotheses.

If the diagnostic evaluator is inadequate, the correct result is `CANNOT_IDENTIFY`; the system cannot use a failing scientific evaluator to certify its own validity.

## Axis B — minimum responsible intervention

Use the existing Jump ladder as a comparator/interface, not assumed truth:

0. action/parameter;
1. local repair/composition;
2. model/hypothesis expansion;
3. representation-regime transition;
4. problem/objective reformulation;
5. method/tool/instrument invention;
6. workflow/meta-skill revision;
7. framework revision;
8. constitution proposal only under an explicit external-authority test.

A locus diagnosis suggests candidate action families only. It does not authorize adoption. Higher-level change still requires witnessed obstruction, prospective discriminator, lower-level disposition, preservation/falsifier contracts and strongest-parent comparison.

## Paired hostile families

### A. Same prediction residual, different cause

- target changes while measurement and model are stable;
- sensor/calibration drifts while target is stable;
- model family is inadequate while sensor and target are stable;
- evaluator is blind to the relevant failure class.

### B. Same proof failure, different cause

- more ordinary search is sufficient;
- missing lemma/model expansion is sufficient;
- representation change is needed;
- natural-language/formal problem specification is wrong;
- proof checker/evaluator is valid but the semantic-intent evaluator cannot establish alignment.

### C. Same experimental non-discrimination, different cause

- additional samples under the same experiment resolve the uncertainty;
- measurement channel is insensitive;
- current hypothesis family is inadequate;
- a new intervention/probe is needed;
- problem criterion asks an unidentifiable question;
- evidence cannot distinguish the live loci, making `CANNOT_IDENTIFY` correct.

### D. Same research-workflow failure, different cause

- local tool bug;
- orchestration/dependency loss;
- invalid evaluator;
- wrong model;
- wrong problem criterion;
- no escalation needed because a local repair is sufficient.

Each family requires false-escalation decoys where a more sophisticated intervention is attractive but wrong.

## Baselines

- `B0_RETRY_SEARCH`
- `B1_UNCERTAINTY_ABSTENTION`
- `B2_FAILURE_TAXONOMY_DIAGNOSIS` — includes the AutoResearch frontier failure benchmark family (arXiv:2608.14905) as a parent benchmark, not ME evidence
- `B3_MODEL_BASED_DIAGNOSIS_PLUS_METAREASONING`
- `B4_MODEL_DISCOVERY_AGENT_STYLE`
- `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`
- `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION`

All arms receive matched task information, tool/evaluator access and budgets. The protected target/locus oracle is never exposed to the acting system.

## Primary outcome vector

- locus accuracy/calibration and confusion matrix;
- target-change false attribution;
- scientific-evaluator versus measurement/model confusion;
- problem/specification versus representation confusion;
- correct `CANNOT_IDENTIFY` rate;
- minimal intervention-level accuracy;
- false and missed escalation;
- verified scientific/task terminal;
- semantic/specification damage;
- intervention and total resource cost;
- regret relative to the registered minimal responsible intervention;
- recurrence after intervention.

No pooled success score may compensate for systematically wrong target-change attribution, evaluator laundering or semantic/specification damage.

## Mechanistic requirement

A Machine-Epistemics residual requires all of:

1. locus information is calibrated and adds a protected distinction beyond B5;
2. the locus predicts which intervention succeeds;
3. removing or shuffling locus information degrades routing prospectively;
4. matched extra search/tool access does not recover the gain;
5. at least one effect survives independently authored/native-reviewed transfer.

If M succeeds while its locus diagnosis is wrong or unused, the proposed mechanism is not supported.

## Required ablations

- `M_MINUS_LOCUS_DIAGNOSIS`
- `M_LOCUS_LABELS_SHUFFLED`
- `M_MINUS_DIAGNOSTIC_EVALUATOR_GATE`
- `M_MINUS_LOWER_LEVEL_DISPOSITION`
- `M_MINUS_PROSPECTIVE_DISCRIMINATOR`
- `M_ALWAYS_ESCALATE_WHEN_STUCK`
- `M_NEVER_ESCALATE`
- `M_EQUAL_EXTRA_SEARCH`

## Kill / contraction conditions

Contract the ME-X2 residual if:

- B3/B5 matches or exceeds the locus/routing quality-cost frontier;
- failure taxonomy + metareasoning reproduces the same interventions;
- the locus family is unstable under native-domain reconstruction;
- gains rely on protected oracle information;
- diagnostic evaluator failure is silently converted into a forced causal attribution;
- target, measurement, model, problem, evaluator or process labels cannot be discriminated at useful calibration;
- false escalation or semantic damage offsets gains;
- representation/model changes lose against strongest specialized parents.

Parent sufficiency is a successful scientific terminal.

## Terminal

```text
ME_X2_STATUS = PROSPECTIVE_UNEXECUTED
WORLD_IS_MACHINE = FALSE
LOCUS_AXIS = TARGET__OBSERVATION__MODEL__REPRESENTATION__PROBLEM__EVALUATOR__PROCESS__UNRESOLVED
SCIENTIFIC_EVALUATOR_EQUALS_DIAGNOSTIC_EVALUATOR = FALSE
PROTECTED_LOCUS_ORACLE_VISIBLE_TO_AGENT = FALSE
PRIMARY_COMPARATOR = STRONGEST_FAITHFUL_PARENT_FEDERATION
PARENT_SUFFICIENCY = VALID_TERMINAL
FIELD_STATUS_AUTHORITY = NONE
```
