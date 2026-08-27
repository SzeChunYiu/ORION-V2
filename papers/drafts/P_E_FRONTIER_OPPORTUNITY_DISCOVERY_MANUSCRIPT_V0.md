# Before the Hypothesis
## Scientific Frontier Opportunity Discovery Under Source, Value and Authority Constraints

**P-E manuscript V0 — contingent**

**Status:** draft contingent candidate; no novelty/publication authority. Corresponds to C10. P-E is dropped/merged into P-C unless protected prospective value is demonstrated.

## Abstract

Scientific automation is increasingly evaluated on answering questions, generating hypotheses, or optimizing experiments. A harder upstream problem is deciding **which scientific problems are worth opening at all**. Existing problem-finding, abductive discovery, literature-based discovery, anomaly detection, open-ended exploration, portfolio/R&D management and science-of-science methods already address parts of this problem. We study a narrower controlled opportunity object: a source-bound candidate research opportunity derived from a concrete anomaly, contradiction, model inadequacy, unmet need, unexplained residual, remote donor or missing capability, with novelty, importance, tractability, falsifiability, independence, option value and agenda authority represented separately. The system is not permitted to infer novelty from failed retrieval, importance from model enthusiasm, or research authority from an opportunity score. P-E is deliberately prospective: its primary endpoint is future expert/scientific value under a frozen selection protocol, not retrospective storytelling after a successful result. If prospective value cannot be measured independently of outcome knowledge, the paper should be merged into solver methods rather than published separately.

## 1. Problem

Most research systems assume a question already exists. But scientific productivity depends heavily on problem selection. Bad problem selection wastes experimental, computational and human attention even if downstream execution is excellent.

An automated opportunity finder faces especially severe Goodhart and leakage risks:

- select topics that resemble historically successful papers;
- rank by apparent novelty when search was incomplete;
- optimize for reviewer excitement rather than tractability or falsifiability;
- rediscover problems already solved under remote terminology;
- prefer questions that are easy for the current model rather than scientifically valuable;
- generate broad “interesting directions” with no source-bound obstruction;
- use future outcome information implicitly during retrospective evaluation.

P-E therefore requires a typed **Opportunity Record** and prospective evaluation.

## 2. Opportunity record

Each candidate opportunity binds:

- source problem/context;
- triggering observation/residual/anomaly;
- exact source references/evidence;
- current explanatory/model state;
- why current state is inadequate;
- candidate question;
- alternative formulations;
- nearest known parents/donors;
- novelty/search status;
- scientific importance hypothesis;
- tractability/resources;
- falsifiability/discriminator;
- expected information/value;
- dependence on existing agenda;
- option value if unresolved;
- safety/authority constraints;
- known reasons not to pursue;
- expiry/revisit conditions.

No scalar opportunity score may erase these coordinates.

## 3. Opportunity sources

Candidate generation can be triggered by:

### 3.1 Contradiction

Two supported claims or model predictions cannot both hold under the declared scope.

### 3.2 Model inadequacy

Residual structure remains after a model fit or explanation.

### 3.3 Non-identifiability

Current observations cannot distinguish scientifically different hypotheses. The opportunity may be a new measurement/experiment rather than a new theory.

### 3.4 Search gap

A decisive source/domain/representation is unexamined.

### 3.5 Remote structural donor

Another field exposes a method or missing distinction not represented in the current problem.

### 3.6 Unmet need / capability gap

A declared scientific task cannot be executed because a measurement, representation, dataset or method is missing.

### 3.7 Evaluation failure

A benchmark or validation protocol cannot distinguish important alternatives.

### 3.8 Performative/strategic response

Deployment changes the environment, creating a new scientific question.

## 4. Core separations

### Novelty

Whether the opportunity is already known. `NO_PRIOR_ART_FOUND` under bounded search is not proof of novelty.

### Importance

Potential scientific consequence if resolved.

### Tractability

Likelihood that available resources/methods can make progress.

### Falsifiability

Whether a discriminator or decisive observation is conceivable.

### Independence

Whether the opportunity adds a genuinely new decision/relation rather than repackaging an existing agenda item.

### Option value

Whether preserving the opportunity for later has value even if immediate execution is low priority.

### Authority

Whether the system may add, prioritize, fund, execute or publish the opportunity. A model-generated opportunity has no self-granting agenda authority.

## 5. Parent threats

- problem-finding research in creativity and design;
- abductive reasoning and discovery systems;
- literature-based discovery;
- anomaly/outlier detection;
- active learning and Bayesian experimental design;
- open-ended/goal exploration;
- bandits and portfolio selection;
- R&D/innovation portfolio management;
- science-of-science forecasting/opportunity mapping;
- research-priority setting;
- technology roadmapping.

P-E survives only if the **source-bound scientific-control representation + prospective evaluation** adds value beyond these parent compositions.

## 6. Prospective protocol

Retrospective evaluation is too easy to game. The core study must be prospective.

### Phase 1 — Freeze opportunity generation

Choose several research areas with active experts. Freeze literature/source date, tool access, time budget, candidate-generation algorithm and parent baselines.

### Phase 2 — Blind initial adjudication

Experts score candidates without knowing which system generated them, on separate coordinates: known/duplicate, importance, tractability, falsifiability, independence, required resources, and whether the question should enter a real research queue.

### Phase 3 — Bounded follow-up

For candidates actually pursued, track outcomes over a predeclared horizon. Do not drop negative/blocked candidates from analysis.

### Phase 4 — Re-evaluation

Measure whether initial judgments predicted useful scientific actions/results and whether source-bound opportunity records made decisions more reproducible.

## 7. Arms

1. random/frontier baseline;
2. expert brainstorming;
3. literature-based discovery parent;
4. anomaly/active-learning parent;
5. science-of-science/portfolio parent;
6. LLM “interesting research questions” prompt;
7. strongest parent-composed opportunity method;
8. P-E typed opportunity process.

## 8. Metrics

Primary prospective:

- expert queue-admission rate;
- duplicate/known-problem rate;
- actionable discriminator rate;
- prospective scientific-value rating;
- later useful-action/result rate;
- false novelty rate;
- authority/agenda violation rate;
- inter-expert reproducibility.

Secondary:

- opportunity-generation cost;
- time to first decisive action;
- diversity across problem classes;
- option value of deferred candidates;
- fraction blocked by missing resources rather than weak science;
- rate of successful novelty contraction.

## 9. Hostile controls

### H1 — Famous-but-solved lure

A topic is important and popular but already resolved. The system must not rank it as novel.

### H2 — Retrieval censorship

Literature access fails. Novelty becomes `CANNOT_CHECK`, not high.

### H3 — Easy-but-trivial lure

A problem is tractable for the model but scientifically low value.

### H4 — Exciting-but-unfalsifiable lure

A broad speculative question has no feasible discriminator.

### H5 — Remote known parent

The opportunity appears new lexically but is a known instance in another field.

### H6 — Negative value after stronger parent search

A candidate is correctly contracted after donor discovery. This counts as a useful outcome, not failure.

### H7 — Agenda authority lure

A high-scoring opportunity cannot self-allocate protected resources.

## 10. Relationship to P-C and CSC

P-E is upstream of the solver: it changes the set of problems the scientific controller can choose to open.

If the only robust value is selecting the next action **inside** an existing problem, P-E belongs in P-C and should not survive as a paper.

Under the CSC field hypothesis, P-E corresponds to **frontier-state expansion**. This does not imply that problem finding is new.

## 11. Planned figures

1. Opportunity record with separated novelty/importance/tractability/falsifiability/authority.
2. Source types: contradiction, residual, donor, unmet need, evaluation failure.
3. Prospective blind evaluation timeline.
4. Opportunity frontier: scientific value vs tractability, colored by known/novel status.
5. Examples of successful contraction vs genuinely new queue admission.

## 12. Honest negative terminals

- `PARENT_PROBLEM_FINDING_SUFFICIENT`;
- `NO_PROSPECTIVE_VALUE_OVER_EXPERTS`;
- `NOVELTY_SIGNAL_NOT_RELIABLE`;
- `TRACTABILITY_NOT_CALIBRATABLE`;
- `RETROSPECTIVE_ONLY_VALUE`;
- `MERGE_INTO_P-C`;
- `CANNOT_CHECK`.

## 13. Survival gate

P-E remains a standalone paper only if a prospectively frozen study demonstrates useful future research value beyond strongest parent methods and expert/direct controls, with separately calibrated novelty, tractability, falsifiability and authority.

Otherwise the correct programme action is `MERGE_INTO_P-C`.
