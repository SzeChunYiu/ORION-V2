# ME-X2 — Ontic/Epistemic Diagnostic Addendum V1

**State date:** 2026-09-01  
**Status:** prospective protocol refinement; no protected outcomes inspected

## 1. Why ME-X2 needs a second diagnostic axis

A single symptom such as “the model no longer matches observations” can arise because:

- the target world changed;
- the observation/measurement process changed;
- the model is inadequate;
- the representation is inadequate;
- a tool/workflow failed;
- the registered objective/problem is wrong;
- available evidence cannot distinguish these possibilities.

Treating all of these as “the machine should learn/change its model” confounds ontic and epistemic dynamics.

## 2. Locus-of-discrepancy axis

Before selecting an intervention, register a diagnosis over:

- `TARGET_WORLD_OR_CONTEXT_CHANGED`
- `OBSERVATION_MEASUREMENT_CHANNEL_CHANGED`
- `MODEL_OR_BELIEF_STATE_INADEQUATE`
- `REPRESENTATION_OR_GENERATIVE_REGIME_INADEQUATE`
- `TOOL_INSTRUMENT_WORKFLOW_FAILURE`
- `PROBLEM_OR_OBJECTIVE_MISSPECIFIED`
- `NO_MATERIAL_DISCREPANCY`
- `CANNOT_IDENTIFY_LOCUS`

This locus label is distinct from the existing obstruction/intervention label. For example, `PROBE_ACTION_INSUFFICIENT` may occur because the world and model hypotheses are currently observationally indistinguishable; it does not itself say which is false.

## 3. Minimal causal distinctions

### Case A — world changed, model was valid before

The target distribution/mechanism genuinely changes after an external intervention. The old model may need updating, but the causal explanation is `TARGET_WORLD_OR_CONTEXT_CHANGED`, not automatically `MODEL_FAMILY_INADEQUATE` in the earlier regime.

### Case B — sensor changed, world did not

The measurement calibration drifts while the underlying target remains stable. Correct action is measurement/evaluator repair or revalidation, not theory invention.

### Case C — machine learned, world did not change

A new observation, recovered evidence or corrected dependence structure changes `E_t` while the relevant target state remains fixed.

### Case D — representation changed, world did not

The machine discovers that its current feature/language/lemma basis collapses decision-relevant distinctions. `Gamma_t` changes even though the target did not.

### Case E — cannot tell

Observed discrepancy is compatible with world change, sensor drift and model failure, and no available probe discriminates them. Correct terminal may be `CANNOT_IDENTIFY_LOCUS` rather than arbitrary escalation.

## 4. New paired hostile fixtures required

ME-X2 protected generation should include matched-symptom pairs such as:

1. **distribution shift vs sensor drift** — identical residual pattern, different locus and intervention;
2. **model inadequacy vs preprocessing bug** — predictive failure in both, only one licenses model expansion;
3. **representation insufficiency vs missing lemma/data** — repeated failure in both, only one licenses regime change;
4. **real world change vs stale cached evidence** — apparent temporal drift in both;
5. **world changed but evaluator blind** — ontic change occurred, yet machine cannot warrant that conclusion from current observations;
6. **machine belief changed while world static** — explicit counterexample to world-change = learning.

## 5. Evaluation

Report separately:

- locus-of-discrepancy accuracy/calibration;
- obstruction/intervention classification;
- minimum-intervention accuracy;
- false world-change attribution;
- false model-change attribution;
- false representation-change attribution;
- `CANNOT_IDENTIFY_LOCUS` calibration;
- task outcome and resource cost.

The causal/mechanistic chain for a strong result is:

`evidence -> locus diagnosis -> obstruction diagnosis -> intervention -> protected outcome`.

If correct intervention occurs without meaningful locus diagnosis, do not claim the ontic/epistemic separation as the mechanism.

## 6. Strong baselines

Parent comparators should include change-point/distribution-shift detection, model-based diagnosis, measurement/calibration checks, predictive model criticism, MDA-style model expansion and ordinary workflow error detection as applicable.

The ontic/epistemic distinction is conceptual hygiene unless it adds decision value beyond these parents.

## 7. Kill condition

Contract this diagnostic layer if:

- locus labels are not reliably identifiable from available evidence;
- parent diagnosis systems produce the same intervention decisions;
- the extra axis adds annotation complexity without improving false-escalation/attribution outcomes;
- native-domain reviewers reject the locus categories as scientifically inappropriate for their cases.

## Terminal

```text
WORLD_IS_MACHINE = FALSE_IN_ME_FRAMEWORK
Locus_Diagnosis = PROSPECTIVE_SECOND_AXIS
ONTIC_CHANGE = DISTINCT_FROM_MACHINE_LEARNING
ME_X2_MUST_TEST_FALSE_WORLD_MODEL_REPRESENTATION_ATTRIBUTION = TRUE
PROTECTED_OUTCOMES_INSPECTED = FALSE
```
