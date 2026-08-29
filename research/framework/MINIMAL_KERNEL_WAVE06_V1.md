# ORION-V2 Minimal Kernel Candidate — Wave 06 V1

**Status:** convergence candidate after the human-thinking/lived-knowledge saturation reopen. This revision does not add a new kernel family. It expands interface semantics only where issue #40 produced a material protected-decision hypothesis.

## Design principle

The kernel contains only obligations that remain necessary when the best domain/native algorithm is swapped out. Philosophy, cognitive science, practical know-how and cultural epistemologies are donors and hostile controls, not automatic kernel owners.

A coordinate survives only if removing or merging it changes a protected scientific decision after strongest-parent reduction.

---

## K0 — Identity, contract, framing and receipt boundary

Required objects:

- immutable object/run/epoch identifiers;
- `ProblemContract` / criterion contract;
- current `ProblemFrame` / representation frame;
- typed obligations and blockers;
- resource/capacity declarations;
- authority requirements;
- source/acquisition-mode identity when material;
- immutable step/evidence/execution receipts.

### New distinction

A research system may legitimately discover that its current problem formulation is inadequate. That does **not** permit silent criterion drift.

`ProblemContract` binds the comparison/authority identity. `ProblemFrame` is a revisable scientific representation of what is being investigated. A frame change that alters registered decisions or success criteria creates a new comparison identity unless an explicit relation receipt proves continuity.

### Invariants

- An identifier that is declared but not compared against its expected identity is not a binding gate.
- Reframing cannot launder a failed criterion into a passing one.
- Local adaptation of a procedure/checklist/evaluator must preserve its own identity rather than inherit the canonical identity silently.

---

## K1 — Plural scientific and inquiry state

Required state families:

- source-bound observations/evidence;
- live hypotheses/models/designs/solutions;
- support, defeaters and unresolved alternatives;
- uncertainty and identifiability;
- history and negative knowledge;
- current representation/model/workflow epoch;
- current problem frame;
- unresolved anomalies/surprises when decision-relevant.

Optional knowledge-form annotations when they affect a decision:

- declarative/propositional;
- causal/mechanistic;
- procedural/policy;
- perceptual/state-recognition;
- tacit/skill dependency;
- social/testimonial;
- institutional/authority;
- negative/failure knowledge.

Optional working `InquirySelfModel` state may estimate the adequacy of the current reasoning process. It is a fallible model, not an authority root.

### Invariants

- Lack of a unique winner must not be repaired by silently deleting alternatives.
- A representation that preserves text/propositions but destroys a protected competence, perceptual discriminator or authority condition is not fidelity-preserving for that context.
- Immutable history and adaptive retrieval priority are separate objects; learning may reorganize access without deleting protected negative history.

---

## K2 — Relation and transport request/receipt

Required interface:

```text
RelationRequest = (
    source,
    target,
    context,
    registered_queries,
    interventions_or_actions,
    decisions,
    tolerance,
    epoch,
    required_relation_family,
    optional_knowledge_form,
    optional_competence_or_affordance_conditions,
)
```

A parent implementation returns a typed receipt containing relation status, witnesses, counter-probes, preserved/lost judgments, loss/error bounds, assumptions, translation loss where relevant, and expiry conditions.

The kernel does **not** require one universal metric or embedding. Exact finite bisimulation, Blackwell comparison, causal transport, rough-set relations, psychometric linking, metrological traceability, stochastic simulation and other native methods remain adapters/reference baselines.

### New hostile distinctions

`TEXT_EQUIVALENT` does not imply:

- `PROCEDURALLY_EQUIVALENT`;
- `PERCEPTUALLY_EQUIVALENT`;
- `CAUSALLY_EQUIVALENT`;
- `AUTHORITY_EQUIVALENT`;
- `COMPETENCE_TRANSFERRED`.

### Invariants

- Relation semantics are context- and decision-bound.
- Lost/tacit/underspecified distinctions remain visible when they can affect the registered decision.
- Changed source mode or cultural/linguistic representation never grants automatic translation fidelity.

---

## K3 — Evidence, dependence, provenance, criticism and revalidation

Required interface:

- evidence unit identity and support role;
- dependence/common-cause links;
- component-level parentage;
- assumptions and native counterexamples;
- source/acquisition mode when material;
- evaluator/teacher/reviewer dependence;
- authority ceiling;
- affected commitment/reopen reach;
- transport/revalidation status.

Optional objects when required:

- oral/testimonial/community source identity and custody;
- demonstration/teacher dependence;
- `TacitDependency` marker;
- `DistributedCognitiveEpisode` topology across agents, humans, tools, instruments and artifacts;
- `CriticismReceipt = (claim, critic, dependence, objection, target_assumption, response, state_delta_or_reason_no_change, authority)`;
- observer/intervention coupling when evidence collection changes the observed system.

### Invariants

- Count of sources/agents/replications is never interpreted as independence without a dependence model or explicit `CANNOT_CHECK`.
- Self-critique generated from the same model/context is dependent evidence unless a validated independence argument establishes otherwise.
- Recording criticism is not equivalent to epistemic uptake; a review mechanism must expose whether and why the state changed.
- A failure log is historical evidence, not yet a transferable lesson.

---

## K4 — Action, execution, diagnosis, self-control and recovery

Required interface:

- admissible action proposal;
- mandatory gate vector;
- scientific value / distinguishing power / cost / risk / option-value coordinates;
- execution binding and receipt;
- plural responsibility hypotheses;
- workflow/precedence constraints;
- retry, compensation, repair and selective reopen.

Optional action families supplied by parents may include:

- external review;
- discriminating probe;
- problem/frame reformulation proposal;
- representation restructuring;
- procedural demonstration acquisition;
- attentional capture of an unexpected event;
- offline/incubation candidate generation;
- ask-for-help / human escalation.

### Inquiry self-model

A working self-model may predict:

`P(outcome, method_adequacy, failure_class, value_of_more_compute, value_of_external_review | episode_features, history, domain, source_mode, epoch)`.

Its outputs must be calibrated on delayed/held-out/independent evidence where possible. Self-reflection can select an action; it cannot by itself discharge an evidence or authority obligation about its own correctness.

### Failure lesson

A transferable lesson may be represented as:

`FailureLesson = (expected, observed, reproduction_identity, candidate_causes, discriminators, selected_attribution, confidence, correction, regression_check, transfer_scope, counterexample, authority)`.

Attribution remains unresolved when the available probes do not identify the cause.

### Candidate experimental failure classes

These are benchmark hypotheses, not mandatory universal enums:

- `SELF_MODEL_MISCALIBRATION`;
- `FRAMING_LOCK_IN`;
- `INSTRUCTION_COMPETENCE_CONFUSION`;
- `PLAN_REALITY_CONFUSION`;
- `DISTRIBUTED_STATE_LOSS`;
- `TACIT_INTERFACE_LOSS`;
- `DEGENERATING_REPAIR_LOOP`;
- `METHOD_MONOCULTURE`.

### Invariants

- Hard scientific/authority/integrity gates are non-compensatory.
- Successful introspection is not external validation.
- A correct written procedure is not automatically evidence of executable competence.
- A fix without reproduction/regression evidence does not automatically become a general lesson.

---

## K5 — Frontier, encounter, opportunity and escalation

Required interface:

- research-opportunity proposal with falsifier and agenda-authority boundary;
- portfolio/Pareto relation;
- witnessed incumbent insufficiency;
- minimum sufficient escalation level;
- correspondence/preservation/reopen obligations for regime changes.

Optional frontier state may include:

- typed surprise coordinates;
- low-bandwidth encounter buffer;
- serendipity candidates;
- exploration budget;
- plural model/method portfolios;
- information-gain, learning-progress, novelty and future-option-value estimates.

Candidate object:

`SerendipityCandidate = (encounter, unexpected_relative_to, source_identity, anomaly_type, candidate_cross_problem_value, recognition_reason, discriminator, cost, authority)`.

Candidate surprise vector:

`Surprise = (predictive, semantic, causal, source, evaluator, model_class, value, state_transition)`.

### Candidate experimental failures

- `SURPRISE_SUPPRESSION`;
- `NOISE_CURIOSITY_TRAP`;
- `EXPLORATION_COLLAPSE`.

### Invariants

- Poor score, timeout, novelty language or censored search alone cannot trigger a higher-level Jump.
- Novelty, surprise and curiosity are proposal-selection signals, never scientific support or agenda authority.
- Random novelty is not serendipity; encounter must be followed by value recognition and a testable follow-up path.
- Representation/problem change must preserve or explicitly reopen prior commitments.

---

## K6 — Evaluation, parity, bounded saturation and authority

Required interface:

- V1 capability disposition and parity receipt;
- protected benchmark/evaluator identity;
- strongest donor-product comparison;
- coverage/saturation declaration;
- failure/negative-result ledger linkage;
- adoption/publication authority state.

### Expanded bounded-saturation object

Previous discipline-only coverage is insufficient after issue #40. A stronger declared universe is:

`Coverage = Discipline × SourceMode × KnowledgeForm × AcquisitionMode × Context × HistoricalEpoch × EpistemicPractice`.

The full Cartesian product need not be enumerated. A saturation receipt must instead expose:

- sampled strata and why they matter;
- omitted/censored regions;
- source-mode and acquisition-mode coverage;
- changed-vocabulary/adversarial passes;
- material additions produced by each pass;
- explicit finite stopping basis;
- conditions that reopen the terminal.

### Longitudinal programme evaluation

When relevant, evaluate:

- prospective prediction/obligation creation versus post-hoc accommodation;
- exploration/exploitation balance;
- recurrence after lessons learned;
- criticism uptake;
- self-model calibration and external-review trigger value;
- method diversity where parent uncertainty remains.

### Invariants

- Passing a local test suite grants no scientific truth, novelty or publication authority.
- No finite research programme may claim literal saturation of all human civilization.
- The strongest valid terminal is bounded saturation over an explicit, adversarially varied search universe.
- `CANNOT_CHECK` remains a valid terminal for inaccessible/censored/custodially restricted knowledge.

---

## Explicit adapter / non-kernel families

The following remain parent-owned unless protected evidence proves the boundary insufficient:

- search engines and retrievers;
- optimization/scheduling/queueing solvers;
- workflow engines;
- theorem provers/synthesizers;
- causal inference/discovery libraries;
- stochastic abstraction/control algorithms;
- statistical estimators and psychometric linkers;
- metrology/calibration packages;
- provenance graph storage;
- diagnosis/reliability engines;
- experiment-design algorithms;
- lab/instrument drivers;
- domain ontologies and simulators;
- metacognitive/confidence models;
- curiosity/intrinsic-motivation algorithms;
- creativity/abduction engines;
- procedural/imitation-learning algorithms;
- knowledge-practice taxonomies.

No kernel component named `CONSCIOUSNESS`, `SELF`, `CREATIVITY`, `TACIT_STORE`, `PHILOSOPHY`, `CULTURE`, or universal `NOVELTY_REWARD` is justified by current evidence.

---

## Cross-cutting reflexive guardrails

1. **No self-authentication:** reflection is evidence from a dependent source unless independently grounded.
2. **No silent reframing:** changing the problem/criterion changes identity unless continuity is certified.
3. **No instruction/competence conflation:** capability must be demonstrated under the context claimed.
4. **No surprise/truth conflation:** surprise opens an obligation or opportunity; it never grants acceptance.
5. **No agent-only evaluation when cognition is distributed:** follow the information/support topology across tools, humans and artifacts.
6. **No civilizational saturation claim:** state the bounded universe and reopening condition.

## Candidate de-duplication map

Existing Wave-06 ownership remains:

- structural/comparability/generalization/correspondence/stochastic transport/etc. -> **K2**;
- evidence/provenance/inheritance/reopening -> **K3**;
- policy/workflow/responsibility/probes/solver -> **K4**;
- opportunity/frontier/jump -> **K5**;
- evaluation/parity/donor/saturation -> **K6**.

Issue #40 does not create a new family; it strengthens these existing owners.

## Kernel-freeze questions

A coordinate survives only if at least one protected downstream decision changes when it is removed or merged. Otherwise it becomes parent adapter, compatibility layer, reference baseline, research fixture, paper-specific method or deprecated duplicate.

`MINIMAL_KERNEL_FROZEN` remains blocked until:

1. V1 capability map has no orphan capability;
2. each kernel coordinate has a downstream sufficiency witness;
3. duplicate APIs are dispositioned;
4. strongest parent adapters are registered;
5. parity/simple-control tests show no material regression;
6. authority boundaries remain fail-closed;
7. issue #40 benchmark additions are either absorbed, falsified, parent-owned or explicitly deferred;
8. bounded saturation is re-earned over the expanded source/knowledge/acquisition universe.

## Current terminal

```text
KERNEL_FAMILIES = K0_TO_K6_UNCHANGED
HUMAN_EPISTEMICS_INTERFACE_PRESSURE = MATERIAL
NEW_KERNEL_FAMILY = NOT_JUSTIFIED
REFLEXIVE_SELF_AUTHORITY = FORBIDDEN
ACADEMIC_ONLY_SATURATION = INVALIDATED
EXPANDED_BOUNDED_SATURATION = OPEN
MINIMAL_KERNEL_FROZEN = NOT_YET_EARNED
```
