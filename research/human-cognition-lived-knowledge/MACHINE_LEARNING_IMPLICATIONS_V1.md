# Human Epistemics → Machine Learning Implications V1

**Status:** research hypothesis map. This document proposes ML consequences of the human-thinking/lived-knowledge reopen. It does not claim new ML algorithms or benchmark superiority.

## Thesis

Machine Epistemics should not remain a governance wrapper around a fixed learner. If its state variables are real, they should eventually alter **what the machine learns, what data it seeks, how it represents uncertainty, when it changes representation, which failures it stores, and how it decides that its own learning procedure is inadequate**.

The most important consequence is to split learning into at least three coupled loops:

1. **world learning** — learn predictions/models/policies about the external problem;
2. **self learning** — learn the reliability, blind spots, calibration and failure modes of the learner/reasoner itself;
3. **search-space learning** — learn when the current representation, objective, data source or action family should expand or change.

These loops must have separate evidence and authority because a learner cannot validate a self-change merely by benefiting from it on the same data.

---

# 1. Metacognitive learning

## Current ML analogue

Calibration, uncertainty estimation, verifier models, confidence prediction, meta-learning and metacognitive architectures already cover parts of this space. Recent work also reports that LLMs can be poor at metacognitive adjustment in high-stakes reasoning.

## Machine-Epistemics extension

Learn an explicit `SelfModel_t` that predicts:

- probability an answer/reasoning path is correct;
- probability the current method is sufficient;
- expected value of additional computation/search;
- probability a failure is execution vs model vs representation vs evidence;
- expected benefit of asking an external reviewer/tool;
- calibration conditional on domain, source type and task structure;
- known blind-spot classes and their expiry.

### Training signal

Use independent or delayed outcomes, held-out verifiers, counterexamples, expert adjudication and cross-domain transfer. Self-generated critique is treated as dependent evidence, not an independent target.

### ML research question

Does training the self-model on **failure-type prediction and intervention selection**, rather than only answer confidence, reduce false completion and wasted reasoning?

---

# 2. Error-centric continual learning

## Human donor

Humans learn from prediction error, explicit corrective feedback, high-confidence mistakes, post-action review and error-management culture. Organizational error research distinguishes preventing errors from managing errors after they occur.

## Machine learning change

A replay buffer should not be only a sample of past data. Maintain a typed **failure memory**:

`FailureMemory = {input, prediction, confidence, error_type, cause_hypotheses, corrective_evidence, repair, later_transfer_result}`.

Sampling priorities can depend on:

- high-confidence errors;
- rare failure topology;
- repeated cause pattern;
- changed environment/epoch;
- unresolved causal attribution;
- disagreement between self-model and external evaluation.

### Research hypothesis

Failure-type replay may improve continual adaptation more efficiently than loss-based replay alone because it preserves *why* the learner failed, not only which sample produced high loss.

---

# 3. Surprise as a vector, not a scalar reward

Curiosity-driven RL often uses prediction error as intrinsic reward, but naive prediction-error curiosity can be attracted to stochastic/noisy states. Human/neuroscience research distinguishes novelty, information seeking, uncertainty reduction and richer prediction-error signals.

Machine Epistemics suggests a vector:

`Surprise = (value, state_transition, semantic, causal, source, social, evaluator, model_class)`.

Different coordinates should trigger different learning updates.

Examples:

- high `value_surprise`, low `state_surprise` → update reward/value estimate;
- high `state_transition_surprise` → update world dynamics/hidden-state model;
- high `semantic_surprise` → inspect representation/ontology mapping;
- high `causal_surprise` → search alternative mechanism/intervention;
- high `source_surprise` → audit provenance/dependence;
- high `model_class_surprise` → consider model/representation expansion.

### Research hypothesis

Typed surprise should avoid both underreaction (treat every anomaly as noise) and overreaction (treat every prediction error as reward-worthy novelty).

---

# 4. Serendipitous exploration

## Problem

Most ML exploration remains objective-conditioned: maximize reward, reduce uncertainty, improve learning progress, or solve a known task. Human discovery also involves encounters whose relevance is recognized **to a different or not-yet-active problem**.

## Candidate architecture

Maintain a low-bandwidth `EncounterBuffer` of events that are:

- surprising;
- structurally novel;
- poorly explained;
- far from current query but connected to unresolved concepts;
- failed experiments with unusual side effects;
- external observations not requested by the current task.

Periodically run a **cross-problem relevance process**:

`encounter × unresolved_problem_graph -> candidate_relevance`.

The candidate can create an `OpportunityRecord`, but not change the agenda automatically.

### Key distinction

Serendipity is not “maximize novelty.” It requires both **unexpected encounter** and **recognition of potential value**.

### Hostile control

A noisy random generator produces endless surprising states. A good serendipity system must learn to ignore unpredictability that does not create reusable explanatory/action structure.

---

# 5. Learning from tacit/procedural knowledge

## Problem

Text-only pretraining over-represents declarative knowledge. Many human skills are only partly specified in words and rely on demonstrations, corrections, timing, embodied state and contextual cues.

## ML implication

Training corpora should include typed **procedural episodes**:

`ProcedureEpisode = (goal, state sequence, actions, observations, checkpoints, corrections, demonstrations, outcome, expert comments, environment/tool identity)`.

A recipe, repair video, laboratory demonstration or craft apprenticeship can be represented this way.

### Learning objectives

- next-action prediction conditional on material state;
- checkpoint/state recognition;
- intervention timing;
- recovery after deviation;
- tolerance-range estimation;
- latent skill-state inference;
- ask-for-help trigger;
- extraction of explicit rules from demonstrations *without assuming the explicit rules are complete*.

### Research hypothesis

For tasks whose instructions are systematically underspecified, procedure-state training plus uncertainty about tacit dependencies should outperform instruction-only imitation on distribution shifts in materials/tools/context.

---

# 6. Affordance-conditioned models

Humans often perceive what can be done in a situation, not merely what objects are present. For ML, represent:

`Affordance(s, capability, resources, authority) -> feasible actions`.

This separates:

- theoretically possible action;
- executable action with current tools;
- scientifically admissible action;
- authorized action.

### Example

A model may know that an experiment could distinguish hypotheses but lack the instrument, safety approval or calibration state. The action should remain conceptually useful without being executable.

---

# 7. Distributed cognition as the learning unit

Instead of training/evaluating one agent in isolation, model the cognitive system:

`System = agents + tools + memory + interfaces + humans + instruments + conventions`.

Learn where information is transformed and where errors/dependence enter.

### ML implication

Evaluation should compare **system policies and information topology**, not only base model parameters.

Potential learned objects:

- routing policy;
- delegation policy;
- shared-memory policy;
- independence/dependence predictor;
- external-review trigger;
- human escalation policy;
- artifact placement and retrieval policy.

This makes Machine Epistemics relevant to agentic systems without reducing the field to agents.

---

# 8. Representation restructuring / insight

Insight research suggests some problems require a change in representation before a solution becomes accessible.

## ML implication

Current meta-learning commonly tunes parameters or selects tools. Add explicit **representation proposal** actions:

- split a latent variable;
- introduce a hidden state/object;
- change coordinate system;
- change causal graph family;
- alter temporal/spatial scale;
- quotient irrelevant distinctions;
- unmerge previously collapsed states;
- construct a new relation/bridge between representations.

Candidate training objective:

Reward only representation changes that unlock previously unreachable held-out obligations while preserving protected prior decisions.

This is a more disciplined target than “creative rewrite.”

---

# 9. Pluralistic model portfolios

Kuhn/Feyerabend/scientific pluralism and modern model uncertainty suggest that a learner should not always collapse to one representation too early.

Maintain a portfolio where models can be:

- competing explanations;
- different scales;
- different ontology/representation;
- specialized local models;
- mutually incompatible but empirically unresolved.

The controller chooses which model is sufficient for a declared decision. `winner_take_all` is not mandatory.

### ML research question

Can decision-relative portfolio retention reduce catastrophic conceptual errors compared with premature model selection, at acceptable computational cost?

---

# 10. Observer-aware / performative learning

When an AI system's output changes the environment or the data it later learns from, the learner should model its own intervention:

`Environment_{t+1} = F(Environment_t, learner_action_t, social_response_t)`.

This generalizes performative prediction and second-order cybernetics.

### ML implication

Dataset shift is sometimes **endogenous**. Training should distinguish exogenous drift from learner-induced drift and preserve the causal history of deployment/evaluation changes.

---

# 11. A candidate new training objective

Conventional learning often minimizes expected predictive/task loss:

`min E[L_task]`.

Machine Epistemics suggests a constrained multi-objective learner:

minimize task loss and resource cost **subject to** scientific-control constraints such as:

- calibrated uncertainty;
- source/evidence integrity;
- preserved prior commitments or explicit reopening;
- dependence-aware assurance;
- representation/epoch validity;
- bounded false closure;
- authorization constraints;
- failure-history retention.

Exploration objectives can then include:

- information gain;
- learning progress;
- useful surprise;
- future option value;
- serendipitous encounter diversity;

but only inside the hard validity/authority envelope.

This resembles constrained RL/metareasoning at the optimization level; the potential research residual is the **scientific epistemic state and constraint semantics**.

---

# 12. Proposed benchmark families

## ME-ML1 — Metacognitive calibration

Same task accuracy, different confidence/failure-type calibration. Test whether the self-model chooses appropriate effort, review and stopping.

## ME-ML2 — High-confidence error learning

Inject confidently wrong cases with reliable corrective evidence. Test typed failure replay vs ordinary replay.

## ME-ML3 — Noisy-TV serendipity

Include stochastic novelty and one rare structurally useful accident. Test useful encounter recognition without noise fixation.

## ME-ML4 — Recipe/craft transfer

Train on instructions + demonstrations in one material/tool regime; test changed materials/tools requiring tacit-state recognition and adaptation.

## ME-ML5 — Representation insight

Current feature space makes two hypotheses indistinguishable; a new representation exposes the discriminator. Penalize gratuitous representation changes.

## ME-ML6 — Distributed cognition

Same base models under different tool/memory/dependence topologies. Test whether system-level epistemic modeling predicts reliability.

## ME-ML7 — Performative environment

A deployed policy changes future data. Test static vs observer-aware learning.

## ME-ML8 — Pluralism

Multiple incompatible models are locally useful; premature collapse causes downstream failure. Test decision-relative portfolio policies.

---

# 13. Relationship to the V2 papers

## P-A

Expands donor search beyond papers into practice/artifact/environmental source modes and gives serendipity a concrete retrieval/opportunity role.

## P-B

Tacit/embodied knowledge pressures relation and transport: textual equivalence does not imply procedural competence transfer.

## P-C

Metacognition, self-modeling, error learning, representation restructuring and curiosity directly pressure the solver/control architecture.

## P-D

Distributed cognition and second-order/observer coupling deepen dependence and evaluator dynamics.

## P-E

Serendipity and curiosity provide stronger parents for opportunity discovery and make prospective evaluation even more important.

## Machine Epistemics flagship

The field becomes more human-realistic: it is not only the control of formal scientific workflows, but the study of **how machine-mediated inquiry monitors itself, learns from error, uses tacit/practical knowledge, notices surprises, and changes its own search space without mistaking novelty for truth**.

---

# Current terminal

```text
MACHINE_EPISTEMICS_CAN_INFLUENCE_LEARNING_OBJECTIVES = PLAUSIBLE_RESEARCH_HYPOTHESIS
METACOGNITIVE_SELF_MODEL = HIGH_PRIORITY
TYPED_FAILURE_MEMORY = HIGH_PRIORITY
TYPED_SURPRISE_AND_SERENDIPITY = HIGH_PRIORITY
PROCEDURAL_TACIT_TRAINING = HIGH_PRIORITY
REPRESENTATION_RESTRUCTURING = HIGH_PRIORITY
DISTRIBUTED_COGNITIVE_SYSTEM_LEARNING = HIGH_PRIORITY
OBSERVER_AWARE_LEARNING = HIGH_PRIORITY
NOVEL_ML_ALGORITHM_CLAIM = NOT_ESTABLISHED
```
