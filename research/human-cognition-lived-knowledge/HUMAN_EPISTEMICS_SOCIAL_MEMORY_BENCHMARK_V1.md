# Human Epistemics Social, Memory and Learning Benchmark V1

**Status:** second transparent reference benchmark for issue #40. It converts the second philosophy/cognitive-science omission pass into executable known-answer distinctions. It does not establish psychological fidelity, real-world scientific benefit, algorithmic novelty or publication authority.

## Review cell

1. **memory and cognitive-neuroscience reviewer** — keeps archive, retrieval and reconsolidated working state distinct;
2. **developmental-learning reviewer** — treats demonstrations as selected pedagogical data rather than i.i.d. samples;
3. **social epistemology/review reviewer** — freezes initial independence before communication;
4. **control and reinforcement-learning reviewer** — tests policy revaluation after changed outcomes/epochs;
5. **causal/formal reviewer** — separates counterfactual simulation from observation and demands negative controls for observer coupling;
6. **hostile editor** — rejects any terminal that silently upgrades a proposal, internal recombination or panel convergence into scientific truth.

## Benchmark families

### HESM-1 — Pedagogical sampling and exploration

**Question:** does the learner distinguish a demonstration from a claim that the demonstrated set is exhaustive?

Known-answer cases include:

- explicitly non-exhaustive teaching followed by discovery of a hidden valid alternative;
- non-exhaustive teaching followed by search suppression;
- a teacher claiming exhaustiveness despite an undisclosed valid alternative;
- a safety-bounded teaching regime with authorized versus unauthorized exploration.

Required terminals:

- `EXPLORATION_PRESERVED`;
- `INSTRUCTION_INDUCED_SEARCH_SUPPRESSION`;
- `EXHAUSTIVE_SCOPE_CONTRADICTED`;
- `SAFETY_RESTRICTION_RESPECTED`;
- `SAFETY_RESTRICTION_VIOLATED`.

The benchmark does not reward exploration independent of safety, cost or scientific value.

### HESM-2 — Reviewer independence before and after communication

**Question:** can a system preserve the distinction between mutually blind initial judgements and later socially coupled reports?

Known-answer cases include:

- two blind initial reviewers with disjoint declared model/corpus dependencies;
- two reviewers sharing a base model;
- a purportedly blind reviewer exposed to an editor anchor;
- a later revised report after reading another review.

Required terminals:

- `INDEPENDENT_INITIAL_PANEL`;
- `DEPENDENT_INITIAL_PANEL`;
- `INSUFFICIENT_BLIND_INITIAL`;
- `CANNOT_CHECK`.

Only frozen blind initial judgements can contribute to the initial independence count. Post-communication convergence is not counted as new independent support.

### HESM-3 — Immutable archive versus revisable working memory

**Question:** can retrieval and working-state revision occur without overwriting the scientific history used to audit what was originally observed or claimed?

Known-answer cases include:

- working retrieval/index state changes while the archive digest remains fixed;
- archive digest silently changes;
- a scientific claim changes with no new evidence;
- a claim changes after new evidence but without revalidation;
- no material state change.

Required terminals:

- `WORKING_STATE_REVISED_ARCHIVE_PRESERVED`;
- `ARCHIVE_HISTORY_MUTATED`;
- `CLAIM_CHANGED_WITHOUT_NEW_EVIDENCE`;
- `CLAIM_CHANGED_WITHOUT_REVALIDATION`;
- `NO_MATERIAL_CHANGE`.

### HESM-4 — Offline incubation as proposal generation

**Question:** can an offline recombination/replay process generate candidate hypotheses without treating them as new external evidence?

Known-answer cases include:

- candidate generated under a frozen input with unchanged protected claims;
- protected claims changed during the offline interval;
- external evidence entered during the interval;
- candidate later linked to an external test;
- no candidate generated.

Required terminals:

- `PROPOSAL_ONLY`;
- `PROTECTED_STATE_CHANGED_WITHOUT_EVIDENCE`;
- `EXTERNAL_EVIDENCE_CONTAMINATED`;
- `EXTERNALLY_TESTED`;
- `NO_CANDIDATE`.

Even an externally tested candidate is not automatically true; the terminal records that a test exists rather than that the test supports the claim.

### HESM-5 — Policy habit and criterion revaluation

**Question:** does an overlearned workflow remain sensitive to changed outcomes or criterion epochs?

Known-answer cases include:

- unchanged context and outcome;
- changed context with no revaluation test;
- changed/devalued outcome followed by adaptive policy change;
- changed/devalued outcome followed by unchanged response.

Required terminals:

- `CONTEXT_CURRENT`;
- `REVALIDATION_REQUIRED`;
- `REVALUATED_AND_ADAPTED`;
- `POLICY_HABIT_OUTLIVED_CONTEXT`.

The reference object does not infer a neural or model-free habit mechanism. It records the decision-relevant failure: a policy ignored a material revaluation.

### HESM-6 — Counterfactual proposal versus observation

**Question:** can a model-generated counterfactual guide a test without entering the evidence ledger as if the predicted event had occurred?

Known-answer cases include:

- explicit assumptions and no external observation;
- a simulation marked as an observation;
- a proposal linked to a later external observation;
- missing assumptions.

Required terminals:

- `PROPOSAL_ONLY`;
- `SIMULATION_OBSERVATION_LAUNDERING`;
- `EXTERNALLY_TESTED`;
- `CANNOT_CHECK`.

### HESM-7 — Observer coupling with a stable negative control

**Question:** does an evaluator/observer action produce a target-specific material change, or is the apparent response absent or confounded?

Known-answer cases include:

- target changes materially while the matched stable control does not;
- neither target nor control changes materially;
- the control changes while the target does not;
- both target and control change materially;
- no declared causal pathway.

Required terminals:

- `COUPLING_CANDIDATE`;
- `STABLE_CONTROL`;
- `PERFORMATIVITY_UNSUPPORTED`;
- `CONFOUNDED_CHANGE`;
- `CANNOT_CHECK`.

The word *candidate* is deliberate: a difference relative to the control is not a complete causal proof.

## Cross-family invariants

1. Teaching scope is part of source identity.
2. Reviewer independence is assessed before communication, not inferred from final message count.
3. Working-memory improvement cannot rewrite protected history.
4. Internal incubation produces proposals, not corroborating observations.
5. Cached policies require epoch/outcome revaluation.
6. Counterfactuals remain model outputs until linked to external evidence.
7. Performativity claims require a causal pathway and stable negative control.
8. No result object grants scientific truth, agenda authority or adoption authority.

## Protected-study transition

The reference benchmark should feed, not replace, protected studies involving:

- instruction-only versus instruction-plus-nonexhaustiveness conditions on held-out functions;
- same-model versus independently sourced reviewer panels with frozen initial reports;
- archived scientific histories with adaptive retrieval/reconsolidation layers;
- offline model-replay/incubation arms evaluated on frozen candidates and later tests;
- overtrained agent workflows evaluated after criterion/outcome changes;
- model-generated counterfactuals linked prospectively to external tests;
- evaluator/publication interventions with matched stable controls.

## Current terminal

```text
REFERENCE_BENCHMARK_FAMILIES = 7
KNOWN_ANSWER_TESTS = 22_GREEN_LOCAL
PEDAGOGICAL_SAMPLE_EQ_IID_SAMPLE = REJECTED
POST_COMMUNICATION_CONVERGENCE_EQ_INDEPENDENT_SUPPORT = REJECTED
WORKING_MEMORY_REVISION_EQ_ARCHIVE_REWRITE = REJECTED
INCUBATION_EQ_NEW_EVIDENCE = REJECTED
SIMULATION_EQ_OBSERVATION = REJECTED
PERFORMATIVITY_WITHOUT_CONTROL = REJECTED
PROTECTED_EXTERNAL_VALUE = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
```
