# Scientific Agents Should Know What Remains Unresolved
## Obligation-Driven Problem Solving with Calibrated Escalation, Exploration and Recovery

**P-C manuscript V4 — top-tier pre-results Article draft**  
**Primary target archetype:** broad AI/scientific-agent Article  
**Status:** complete evidence-independent manuscript with frozen result identities, Methods, figures and contraction rules. Reference semantics do not establish naturalistic superiority or publication readiness.

## Abstract

Scientific agents increasingly combine retrieval, modelling, computation, experimentation and tool use, yet they often optimize local task completion without an explicit representation of what is known, what remains unresolved, which failure is responsible, or when a more powerful method is justified. We study an **obligation-driven scientific controller** that represents scientific state, alternative hypotheses, unresolved proof or evidence obligations, calibrated self-knowledge, action mode and authority. The controller selects the minimum sufficient action, diagnoses failure, escalates only when cheaper valid routes are inadequate, and can perform exploratory or constructive actions when the current hypothesis space is insufficient. Machine-native internal computation is unrestricted, but adoption of a scientific transition requires an external witness proportionate to the claim. We prospectively compare the controller with direct methods, human experts and the strongest federation of metareasoning, active learning, diagnosis, workflow, robust-decision and scientific-agent parents. Primary outcomes are justified-terminal rate, critical false completion, false and missed escalation, scientific quality–resource Pareto dominance, resilience and parent-native non-regression. The architecture survives only if its control structure—not additional compute or hidden expert labour—prevents protected scientific failures without becoming a drag on simple tasks.

## Introduction

A scientific agent can complete many steps while failing to know whether the scientific problem has been solved. It may produce code that runs, a model that fits, a plausible explanation, a review that agrees with itself or a paper-like report. None necessarily identifies the unresolved claim, the missing discriminator, the weakest computational or evidential link, or the authority required for the next action.

Mature parent fields address parts of this problem. Metareasoning and value of computation allocate effort. POMDPs and active learning select actions under uncertainty. Bayesian experimental design chooses informative observations. Model-based diagnosis identifies faults. Truth-maintenance systems track support and revision. Robust decision-making preserves options under deep uncertainty. Workflow and autonomous-laboratory systems coordinate tools and experiments. Scientific-software verification distinguishes computation from a scientific model. Human inquiry research adds problem framing, metacognition, exploratory experimentation, failure learning and competence.

P-C does not claim these mechanisms. It asks whether an integrated control state changes scientific decisions when a research episode crosses their boundaries.

The controller represents:

`ScientificControlState = (`
`problem_identity, criterion, current_commitments, alternatives, obligations, evidence_and_sources, model_and_computation_status, uncertainty_form, self_model, action_mode, resources, permissions, history, terminal_status)`.

An obligation is not simply a to-do item. It states a condition that must be discharged, falsified, revised, escalated or left unresolved before a particular scientific transition is warranted. Examples include identifying a causal discriminator, validating a numerical implementation, obtaining an adequate oracle, checking a transport relation, resolving dependence among evidence routes or obtaining permission for an action.

The system is deliberately not closed around the current obligation vocabulary. Exploratory and constructive actions may create the observations, instruments, representations or concepts needed to formulate a better obligation. This protects against efficient optimization of the wrong problem.

We test four claims. First, explicit scientific state and obligations improve justified terminals beyond output-oriented workflows. Second, calibrated self-models and responsibility diagnosis improve minimum sufficient escalation. Third, typed exploratory/constructive action prevents hypothesis-space lock-in without uncontrolled search. Fourth, contextual activation preserves simple-case efficiency and resilience.

## Results architecture

### Explicit obligations distinguish task completion from scientific completion

The benchmark includes cases in which local components succeed while a necessary scientific condition remains open. Examples include:

- a model fits but an alternative mechanism is not discriminated;
- computation converges but is numerically or scientifically invalid;
- a proof establishes the wrong specification;
- several reviewers share a source/model;
- a transport relation is assumed but not checked;
- data are accessible but the proposed use is unauthorized;
- an experiment is completed but its evaluator cannot reveal the relevant error.

Each case has a frozen terminal set:

- `SUPPORTED_OR_VERIFIED`;
- `FALSIFIED_OR_REFUTED`;
- `REVISE_MODEL_OR_FRAME`;
- `ESCALATE_WITH_REASON`;
- `STOP_FOR_RESOURCE_OR_AUTHORITY`;
- `CANNOT_CHECK`.

**Primary result slot PC-R1.** Report justified-terminal rate and critical false completion for SIMPLE, workflow/agent baselines, strongest F0 controller, human expert and P-C.

**Required sentence form:**

> P-C reached a justified terminal in [x]% of protected cases versus [comparators]. It reduced critical false completion by [effect/uncertainty], with [n] remaining failures concentrated in [obligation/failure family].

A higher completion count with more false scientific closure is not considered an improvement.

### Calibrated self-models and diagnosis control escalation

The controller maintains claim-specific estimates of its capability, uncertainty and failure responsibility. Self-assessment cannot be validated by the same model’s reflection alone. Calibration uses known-answer cases, independent evaluators, historical receipts and out-of-distribution strata.

Responsibility classes include:

- missing information or observation;
- model inadequacy or non-identifiability;
- ill-conditioning or numerical instability;
- implementation or software fault;
- oracle/test inadequacy;
- semantic or transport mismatch;
- source/dependence failure;
- authority or custody blockage;
- resource limitation;
- unknown/multiple cause.

Escalation actions include higher precision, independent implementation, stronger oracle, new experiment, representation change, expert review or authorized human decision.

**Primary result slot PC-R2.** Report calibration, responsibility classification, minimum-sufficient escalation, false escalation, missed escalation and escalation cost.

**Required sentence form:**

> P-C selected the minimum sufficient escalation in [x]% of cases and avoided [y] unnecessary escalations. Self-model calibration error was [value]; replacing independent calibration with same-model reflection changed [outcome] by [effect].

### Exploration and construction operate under typed authority

The system distinguishes:

- `CONFIRMATORY`;
- `DISCRIMINATIVE`;
- `EXPLORATORY`;
- `CONSTRUCTIVE`;
- `CALIBRATIVE`;
- `REPLICATIVE` actions.

Exploratory output can open or revise obligations but does not inherit confirmatory evidence status. Constructive actions can create an instrument, dataset, model system, representation or search space. Their artifact and target-transport assumptions are explicit.

Protected pairs include one case in which exploration is necessary and a matched case in which it wastes resources or amplifies noise.

**Primary result slot PC-R3.** Report representation/problem-space expansion success, exploration-to-discriminator conversion, false confirmation and unnecessary exploration cost.

**Required sentence form:**

> Typed exploration enabled a usable discriminator in [n] otherwise blocked cases while adding [cost] in negative controls. The controller incorrectly promoted exploratory observations to confirmatory support in [n] cases.

### Machine-native internal strategies are judged at the scientific boundary

P-C does not require every internal computation to be expressed as a human verbal chain. A system may use latent representations, programs, parallel search, graphs or populations. A proposed scientific transition must nevertheless return an external witness containing the claim-relevant source, evidence, assumptions, uncertainty, validation, relation to prior commitments and authority.

Protected arms include human-mimetic, machine-native, hybrid and strongest-parent systems under matched resources.

**Primary result slot PC-R4.** Report whether non-human internal strategies improve quality–resource outcomes and whether the external witness remains sufficient for independent adjudication.

**Required sentence form:**

> The machine-native arm achieved [gain] at [resource difference]. Requiring a claim-sufficient witness changed [quality/cost]. The gain [did/did not] survive mechanism ablation, leakage control and second-domain evaluation.

### Component interventions identify value and drag

The architecture is evaluated using:

- FULL;
- MINUS-obligations;
- MINUS-self-model;
- MINUS-diagnosis;
- MINUS-action-mode typing;
- MINUS-escalation gate;
- MINUS-external-witness requirement;
- PARENT replacements;
- pair interactions;
- SIMPLE and F0 controls.

**Primary result slot PC-R5.** Classify every component as:

- necessary core;
- synergistic;
- contextual;
- parent-replaceable;
- redundant drag;
- harmful;
- `CANNOT_CHECK`.

**Required sentence form:**

> [Component] prevented [critical failure] in [stratum] at [cost] but was unnecessary/harmful in [stratum]. Contextual activation [did/did not] recover the Pareto frontier.

### Resilience and recovery test the controller beyond nominal tasks

Disturbances include tool failure, evaluator outage, censored evidence, reduced compute, changed numerical environment, adversarial input, conflicting uncertainty and expired authority. Outcomes include capability degradation, false completion, safe refusal, local recovery, global reset and recovery time.

**Primary result slot PC-R6.** Report nominal versus disturbed quality, graceful degradation, recovery and adaptive-capacity sources.

**Required sentence form:**

> Under [disturbance], P-C retained [capability] and recovered in [time/cost], compared with [baseline]. The principal brittleness arose from [component/assumption].

## Discussion

P-C treats scientific agents as controllers of epistemic commitments rather than generators of plausible outputs. Its strongest potential contribution is not the vocabulary of obligations but an experimentally demonstrated improvement in which scientific transitions are accepted, rejected, escalated or left unresolved.

The architecture should lose often. A direct calculation, native domain algorithm or single test should outperform the full controller when the task is exact and simple. A scientific-control layer that activates everywhere would impose cost, create new failure modes and reduce trust. Contextual gating and parent deference are therefore part of the thesis, not implementation details.

Self-reflection is similarly constrained. A model can produce persuasive explanations of its own uncertainty without being calibrated. The self-model must be trained and evaluated against independent outcomes and failure strata. `I am uncertain` is not evidence of accurate metacognition; `I am confident` is not authority.

Exploratory action addresses a deeper limitation of fixed workflows. Scientific discovery can require constructing the variables or instruments with which a useful hypothesis is expressed. Yet open-ended exploration is easy to romanticize. P-C gives exploration an explicit budget, source identity, expected discriminating path and negative controls. Surprise opens investigation; it does not prove an explanation.

The machine-native boundary is intentionally asymmetric. Internal processes can differ radically from human reasoning, while external scientific transitions remain constrained by evidence and validity. This avoids building a human-mimicking machine without treating opacity or difference as automatic intelligence.

Negative terminals remain publication-worthy. F0 may match P-C. Only one or two components may survive. The architecture may help in high-complexity episodes but become drag elsewhere. These outcomes define a contextual scientific method rather than a universal agent architecture.

## Methods

### Case families

Protected suites span:

1. exact/simple tasks where direct methods should win;
2. hidden multiple-fault diagnosis;
3. mechanistic alternatives requiring discrimination;
4. numerical/implementation/oracle failures;
5. relation and transport failures;
6. evidence dependence and false review agreement;
7. exploratory or constructive discovery;
8. deep/imprecise uncertainty and reversible action;
9. governed data and authority;
10. machine-native strategy and external witness;
11. disturbance, recovery and resource pressure.

Constructed known-answer cases establish semantics. Naturalistic value requires fresh tasks and independent domain adjudication.

### Arms and matching

- SIMPLE direct control;
- representative workflow/agent baseline;
- strongest parent-specific method;
- expert-configured F0 federation;
- human expert/team where feasible;
- P-C FULL;
- component, pair and parent replacements;
- machine-native and hybrid variants.

Bind sources, tools, model identities, compute, wall time, memory, precision, human interventions, evaluator access and authorized actions. Report Pareto curves when exact matching is impossible.

### Policy

Candidate action value is a vector, not one unrestricted scalar:

- expected scientific progress;
- probability of discharging a necessary obligation;
- information/discrimination value;
- reversibility and option value;
- resource cost;
- risk/critical failure;
- authority and safety feasibility.

Hard authority and integrity gates are non-compensatory. Under deep uncertainty, robust/adaptive parent policies replace unjustified expected-value calculation.

### Self-model calibration

Capability estimates are evaluated across task and failure strata. Same-model critique is marked dependent. Calibration outcomes include reliability curves, proper scoring where valid, selective accuracy, escalation calibration and false-confidence rates. Non-probabilistic uncertainty remains typed.

### Terminal semantics

A terminal receipt binds:

- problem and criterion identity;
- commitments and unresolved alternatives;
- discharged and open obligations;
- evidence/source status;
- computation/test/relation validity;
- uncertainty;
- authority;
- resource basis;
- reasons for closure or `CANNOT_CHECK`;
- reopen conditions.

### Outcomes

Primary:

- justified-terminal rate;
- critical false completion;
- parent-native non-regression;
- minimum sufficient escalation;
- resource-adjusted scientific quality;
- resilience under disturbance.

Secondary:

- diagnosis accuracy;
- self-model calibration;
- false/missed escalation;
- exploration conversion and noise cost;
- witness sufficiency;
- human/expert burden;
- implementation/failure surface.

### Analysis

Primary estimands and minimum important differences are frozen by case family. Critical failures are analysed separately and cannot be averaged into an overall score. Stochastic systems receive repeated runs with seed/model-instance identities. Evaluator dependence is modelled. All negative and parent-win results remain.

## Limitations frozen before results

- obligation design may encode author preferences;
- state representation can become burdensome;
- full diagnosis can be intractable;
- naturalistic ground truth can be contested;
- independent experts may be expensive and dependent;
- machine-native mechanisms may resist causal interpretation;
- robust refusal can become over-conservatism;
- tool/security/governance constraints can prevent open replication.

## Availability and disclosure slots

- **Code and configurations:** `[release commit/environment]`.
- **Cases and receipts:** `[release/custody statement]`.
- **Models and compute:** `[identities and resource accounting]`.
- **AI assistance:** `[roles, verification and human accountability]`.
- **Author contributions/competing interests:** `[complete before submission]`.

## Honest terminal

```text
P_C_MANUSCRIPT_SURFACE = COMPLETE_PRE_RESULTS
REFERENCE_SEMANTICS = PARTIAL_GREEN_OR_OPEN
V1_NON_REGRESSION = OPEN
F0_PARENT_FEDERATION_COMPARISON = OPEN
CROSS_DOMAIN_PROTECTED_RESULTS = OPEN
COMPONENT_VALUE_AND_DRAG = OPEN
TOP_TIER_SUBMISSION_READY = NO
POSSIBLE_TERMINALS = ARTICLE__CONTEXTUAL_CONTROLLER__PARENT_SUFFICIENCY__REDUNDANT_DRAG__CANNOT_CHECK
```
