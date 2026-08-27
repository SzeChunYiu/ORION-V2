# Beyond Fixed Research Pipelines
## Obligation-Driven Scientific Problem Solving with Calibrated Self-Monitoring and Witnessed Minimum Escalation

**P-C manuscript V1 — design manuscript; protected results open**

**Status:** materially revised after the human-thinking/lived-knowledge saturation reopen. No novelty/publication authority. No result described below is established until the protected studies are executed.

## Abstract

Autonomous-science systems increasingly orchestrate retrieval, analysis, experiment design, code execution and scientific writing, but many remain organized as fixed or weakly adaptive workflows. Research failures are more heterogeneous: evidence may be missing; observations may be non-identifying; a representation may omit the decisive variable; a solver may be confidently wrong about its own adequacy; a useful anomaly may arrive outside the active query; or repeated local repairs may become a degenerating programme. We test an **obligation-driven scientific solver** that maintains plural hypotheses, unresolved obligations, evidence/dependence, resources, authority boundaries and parent-owned actions. It learns a calibrated inquiry self-model for effort/review decisions, converts reproduced failures into scoped lesson objects, retains typed unexpected events without treating surprise as evidence, and escalates representation, method or problem frame only when lower-level insufficiency is witnessed. The proposal does not claim ownership of metareasoning, Bayesian experimental design, workflow systems, diagnosis, formal refinement, metacognition, curiosity, continual learning, creativity or autonomous laboratories. Its scientific question is whether this coordination yields more justified terminal states, better calibrated review/action decisions, lower false completion and less unnecessary escalation than the strongest composed parents under matched resources. Protected controls include self-critique dependence, framing lock-in versus criterion gaming, useful surprise versus noisy novelty, instruction versus competence, failure-lesson transfer and progressive versus degenerating repair.

## 1. Why a pipeline is not enough

Research episodes do not fail in one way. A stalled task can reflect missing evidence, a bad search route, insufficient method capacity, invalid assumptions, non-identifying observations, a representation that hides a relevant distinction, tool failure, resource limits or several causes at once.

A fixed workflow can respond by progressing to the next stage despite unresolved scientific obligations. An unconstrained agent can react by increasing model size, adding tools or reformulating the task without proving that the change is needed. Both patterns can create false completion or unnecessary scientific disruption.

Human inquiry adds two further failures. First, the research process can be wrong **about itself**: confidence, critique or repeated reflection may be poorly calibrated. Second, the initial problem formulation can itself be the obstruction. A scientifically serious solver therefore needs both object-level and process-level uncertainty while preserving the distinction between legitimate reframing and criterion gaming.

P-C asks whether active **scientific obligations** provide a better control object.

## 2. State model

Let solver state be

`S = (P, F, K, H, O, U, M, R, A, C, Q, E)`

where:

- `P` — immutable problem/criterion identity for the current comparison;
- `F` — current problem/representation frame;
- `K` — claims/evidence/current knowledge state;
- `H` — plural hypothesis/responsibility portfolio;
- `O` — active scientific obligations;
- `U` — uncertainty and identifiability state;
- `M` — memory/provenance/dependence and failure history;
- `R` — resources/capacity/access;
- `A` — authority state;
- `C` — available parent-owned action repertoire;
- `Q` — calibrated inquiry self-model state where enabled;
- `E` — retained encounter/anomaly state where enabled.

The paper's claim, if any, concerns **coordination**, not the native algorithms supplying the actions.

## 3. Obligation types

A minimal vocabulary includes:

- evidence obligation;
- verification obligation;
- criterion-binding obligation;
- source/provenance obligation;
- independence/dependence obligation;
- discriminating-experiment obligation;
- preservation/transport obligation;
- selective-reopen obligation;
- authority obligation;
- resource/capacity obligation;
- coverage/censoring obligation;
- external-review obligation;
- competence-demonstration obligation;
- frame/representation-adequacy obligation.

Hard obligations cannot be traded away for average utility.

## 4. Action families

Parent-owned actions may include:

- direct reasoning/analysis;
- retrieval/search route;
- formal check/proof/synthesis;
- computation/simulation;
- measurement/experiment;
- discriminating probe;
- model fitting/optimization;
- representation restructuring;
- decomposition change;
- method change;
- problem-frame reformulation proposal;
- external review/benchmark;
- human/tool escalation;
- demonstration acquisition;
- local repair;
- selective reopening;
- bounded exploration;
- bounded stop.

The solver exposes why an action is admissible, which obligations it targets and which prior commitments it may disturb.

## 5. Inquiry self-model: reflection without self-authentication

A capable agent should estimate not only uncertainty about the world but also the adequacy of its own current method. Define a working predictor:

`InquirySelfModel_t = P(outcome, method_adequacy, failure_class, value_of_more_compute, value_of_external_review | episode_features, history, domain, source_mode, epoch)`.

### Requirements

1. Predictions are frozen before the target outcome/evaluator is observed.
2. Calibration is measured on held-out, delayed or independently adjudicated outcomes where possible.
3. Domain/task/source-mode conditional calibration is reported.
4. Training/evaluator dependencies are tracked.
5. Self-model uncertainty remains explicit.
6. Confidence cannot grant evidence or adoption authority.
7. Major model/representation/domain changes expire or revalidate old self-model calibrations.

The key baseline is **naive reflection**: repeated same-model critique or confidence without independent calibration. This is intentionally strong enough to test whether a structured self-model adds value over ordinary uncertainty/confidence methods.

### Protected hypothesis

Does failure-type/method-adequacy calibration improve choices about more computation, tool use, external review and stopping **at equal or similar task accuracy**?

## 6. Failure memory versus failure lessons

A raw failure record says what happened. A reusable lesson requires causal and transfer structure:

`FailureLesson = (expected, observed, reproduction_identity, candidate_causes, discriminators, selected_attribution, confidence, correction, regression_check, transfer_scope, counterexample, authority)`.

The lesson remains unresolved when available probes cannot identify the cause.

### Research hypothesis

Typed failure lessons may reduce recurrence or improve transfer more efficiently than raw error replay or loss-prioritized replay, especially for high-confidence and repeated topology failures.

### Hostile control

A memorable failure is spuriously generalized to a context where its cause is absent. The lesson representation should refuse or revalidate transfer.

## 7. Responsibility diagnosis

Candidate classes include:

- `EVIDENCE_MISSING`;
- `SEARCH_COVERAGE`;
- `REPRESENTATION_LIMIT`;
- `MODEL_OR_METHOD_CAPACITY`;
- `ASSUMPTION_INVALID`;
- `NON_IDENTIFYING_BENCHMARK`;
- `RESOURCE_LIMIT`;
- `AUTHORITY_BLOCK`;
- `EXECUTION_FAILURE`;
- `COMPETENCE_GAP`;
- `INTERACTION_ONLY`;
- `MULTIPLE_INDEPENDENT`;
- `CANNOT_IDENTIFY`.

These are benchmark labels, not a claim that one universal taxonomy covers all sciences.

When the cause is not identified, the preferred action may be a discriminator rather than a repair.

## 8. Witnessed minimum escalation

Escalation changes the action/search space. A domain may instantiate a partially ordered hierarchy such as:

- J0 direct/local action;
- J1 search/query change;
- J2 local algorithm/parameter repair;
- J3 decomposition change;
- J4 model/method expansion;
- J5 representation change;
- J6 new instrument/data/source mode;
- J7 problem-frame/criterion proposal;
- J8 external programme/adoption change.

The ladder is not universal. The proposed control discipline is:

1. identify the blocked obligation;
2. enumerate lower-level admissible actions;
3. test whether they are sufficient or non-identifying;
4. require an insufficiency/ceiling witness when possible;
5. choose the lowest level predicted to discharge the obligation;
6. bind preservation/reopen consequences;
7. evaluate the result under the original or explicitly changed comparison identity.

### False Jump

A higher-level change occurs while a lower-level action was sufficient.

### Missed Jump

The solver continues local actions despite evidence that the current action/representation space cannot resolve the obstruction.

### Framing lock-in

The current formulation excludes a variable, relation or objective needed to state the discriminator. Local optimization cannot solve the scientific problem as represented.

### Criterion gaming

A frame/criterion change creates an apparent success without resolving the original obligation. Expected terminal: new comparison identity, not a pass on the old one.

## 9. Surprise, exploration and serendipity

A research process should not restrict its epistemic inputs to events requested by the current plan. But naive novelty maximization is equally unsafe.

Represent surprise as a vector when useful:

`Surprise = (predictive, semantic, causal, source, evaluator, model_class, value, state_transition)`.

Unexpected events may create an anomaly obligation, a source-quality warning, a representation-change proposal, a serendipity candidate or no action if they are diagnosed as uninformative noise.

A low-bandwidth encounter buffer can retain events that are:

- surprising relative to the current model;
- poorly explained;
- structurally novel;
- side effects of failed experiments;
- potentially relevant to another unresolved problem.

Periodically:

`encounter × unresolved_problem_graph -> candidate_relevance`.

A `SerendipityCandidate` remains a proposal. The encounter does not support the explanation and does not grant agenda authority.

### Hostile controls

- **Noisy-TV:** stochastic unpredictability produces endless novelty but no reusable structure.
- **Surprise suppression:** an off-task anomaly is discarded despite a cheap discriminator and later cross-problem value.
- **Famous accident hindsight:** retrospective outcome knowledge makes an event look obviously important. Prospective recognition must be frozen before outcome access.

## 10. Procedural competence and situated recovery

Correct instructions are not equivalent to competent execution. Add protected tasks in which:

- the nominal procedure is unchanged;
- material/tool/environment state changes;
- the successful agent must recognize an intermediate state, adjust timing, request help or recover from deviation.

Compare text-only instruction following with demonstrations/intermediate-state/recovery evidence. Penalize both unsafe continuation and unnecessary refusal.

P-C does not claim a universal theory of tacit knowledge. The question is whether the solver correctly identifies when an explicit procedure is an insufficient action specification.

## 11. Progressive versus degenerating repair

An autonomous system can produce many local fixes while making no real scientific progress. Track a longitudinal programme state:

- prospective obligations/predictions created before outcomes;
- fraction independently corroborated;
- post-hoc accommodations;
- recurrence of the same failure topology;
- protected capabilities gained/lost;
- exploration routes abandoned;
- resource spent preserving the current method.

Candidate failure: `DEGENERATING_REPAIR_LOOP` — repeated patches discharge observed failures but create no independently testable progress and repeatedly encounter related defects.

This is a diagnostic, not an automatic rule to abandon the programme.

## 12. Parent threats

P-C is strongly threatened by:

- POMDPs and rational metareasoning;
- expected value of control and metacognitive monitoring;
- Bayesian experimental design and active learning;
- adaptive workflow/BPM/operations systems;
- blackboard and multi-agent architectures;
- model-based diagnosis and multiple-fault diagnosis;
- CEGIS/CEGAR and formal refinement;
- theorem proving/program repair;
- continual/meta-learning;
- intrinsic motivation, curiosity and open-ended learning;
- creativity/problem-finding and insight research;
- situated/distributed cognition;
- self-driving laboratories and scientific agents.

P-C must compare against **composed parents**, not weak isolated baselines.

## 13. Protected benchmark programme

### B1 — Simple direct controls

One obvious action solves the task. Added diagnosis/reflection/escalation is overreach.

### B2 — Hidden mechanistic discovery

Several hypotheses require sequential evidence and targeted probes.

### B3 — Multiple-fault diagnosis

Independent faults plus interaction-only case.

### B4 — Formal proof/synthesis

Distinguish proof gap, model gap and execution/tool gap.

### B5 — Governed experiment

Scientifically useful action lacks required authority. Derivation is not execution permission.

### B6 — Representation insufficiency

Current variables make two live hypotheses indistinguishable; representation restructuring is necessary.

### B7 — Lower-level sufficiency control

Local repair solves the obstruction; a Jump is penalized.

### B8 — Non-identifying benchmark

Failure is compatible with representation or capacity failure; a discriminator is required.

### B9 — Self-model calibration

Task accuracy is held similar while confidence/failure-type/review-trigger calibration differs.

### B10 — Self-critique dependence

Repeated same-model reflection is compared with genuinely independent review.

### B11 — Framing lock-in versus criterion gaming

One case needs a new frame; a matched case only changes the success definition.

### B12 — Failure-lesson transfer

Raw error log versus typed lesson on related and misleadingly similar future failures.

### B13 — Useful surprise versus noisy novelty

One rare off-path event is structurally useful; many stochastic events are unpredictable but irrelevant.

### B14 — Instruction versus competence

Text is sufficient in the training context but underspecified after material/tool perturbation.

### B15 — Degenerating repair

Repeated local patches versus a representation/method change that opens a prospective discriminator.

### B16 — Method monoculture

The decisive parent method lies outside the solver's favored internal representation.

## 14. Baselines

1. fixed research pipeline;
2. unconstrained agentic planner;
3. simple/direct control;
4. uncertainty/confidence baseline;
5. same-model reflection baseline;
6. strongest parent-composed adaptive controller;
7. frozen V1;
8. contracted P-C V1 solver.

All arms receive matched external tools/data/resources wherever possible.

## 15. Metrics

Primary:

- justified-terminal rate;
- false completion;
- responsibility/failure-class correctness;
- self-model calibration;
- review/action/stop decision utility;
- discriminating-probe value;
- false Jump rate;
- missed Jump rate;
- minimum-level accuracy;
- framing-lock-in resolution;
- criterion-gaming detection;
- failure recurrence and false lesson transfer;
- useful-surprise recognition versus noise fixation;
- competence-transfer safety;
- authority/integrity violations;
- preservation/reopen correctness;
- `CANNOT_CHECK` calibration.

Secondary:

- cost to decisive evidence;
- total actions/latency;
- unnecessary work;
- justified reachability gain;
- external reviewer burden;
- exploration budget cost.

No average can compensate a critical scientific-integrity or authority regression.

## 16. Formal directions

### 16.1 Obligation reachability

Characterize whether hard obligations are dischargeable under resource/authority/action constraints.

### 16.2 Minimal escalation

Under a partially ordered intervention family and sufficient diagnostics, characterize when selecting a minimal feasible intervention is optimal among policies satisfying hard preservation constraints.

### 16.3 Responsibility observability

Define when failure causes are distinguishable by available probes.

### 16.4 Self-model calibration under dependence

Study calibration when task solver, critic and self-model share parameters, data or representations.

### 16.5 Non-compensatory planning

Optimize secondary utility only inside the feasible region defined by scientific and authority predicates.

### 16.6 Frame-change identity

Formalize when a problem-frame revision preserves a registered comparison and when it necessarily creates a new problem identity.

## 17. Honest negative terminals

- `USE_DONOR_COMPOSED_SOLVER`;
- `SELF_MODEL_NO_VALUE_OVER_UNCERTAINTY`;
- `FAILURE_LESSON_NO_TRANSFER_GAIN`;
- `SURPRISE_CHANNEL_DISTRACTING`;
- `PROCEDURAL_FIELDS_NO_GAIN`;
- `V1_NONINFERIOR`;
- `MULTI_POLICY_NO_SINGLE_ARCHITECTURE`;
- `V2_OVERREACH`;
- `JUMP_TRIGGER_NOT_CALIBRATABLE`;
- `CANNOT_CHECK`.

## 18. Survival gate

P-C survives only if protected mixed-task evaluation shows material incremental justified reach, lower false completion, better calibrated self-control/diagnosis or better minimum escalation than the strongest parent-composed adaptive solver **without** V1 parity, authority or integrity regression.

Until those results exist, the scientific scope is mature enough for implementation, but the Article is not publication-ready.

```text
P_C_V1_SCOPE = MATERIALLY_REVISED
INQUIRY_SELF_MODEL = TESTABLE_WORKING_OBJECT
SELF_REFLECTION_AS_VALIDATION = REJECTED
FAILURE_LESSON = TESTABLE_WORKING_OBJECT
SURPRISE_SERENDIPITY = PROPOSAL_CHANNEL_NOT_EVIDENCE
NEW_KERNEL_REQUIRED = NO
PROTECTED_RESULTS = OPEN
PUBLICATION_READY = NO
```
