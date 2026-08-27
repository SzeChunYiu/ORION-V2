# Beyond Fixed Research Pipelines
## Obligation-Driven Scientific Problem Solving with Witnessed Minimum Escalation

**P-C manuscript V0**

**Status:** draft candidate; no novelty/publication authority. Absorbs C04 + C05 under the frozen paper contraction.

## Abstract

Autonomous-science systems increasingly orchestrate literature retrieval, analysis, experiment design, code execution and scientific writing. Many systems nevertheless encode research as a fixed or weakly adaptive workflow: a sequence of roles or stages whose progression is determined more by orchestration state than by the changing scientific obligations of the problem. We test a different control object. An obligation-driven scientific solver maintains plural hypotheses, unresolved obligations, evidence/dependence, resource state, authority boundaries and a repertoire of parent-owned actions. It chooses actions according to the obligations they can discharge, diagnoses why progress is blocked, and escalates representation/method/search space only when lower-level insufficiency is witnessed. The proposal does not claim ownership of retrieval, Bayesian experiment design, workflow systems, diagnosis, theorem proving or autonomous laboratory methods; these remain parent adapters. The scientific question is whether obligation-driven coordination yields more justified terminal states, lower false completion and less unnecessary escalation than the strongest donor-composed adaptive solver while preserving frozen V1 capabilities. We define the state/action model, minimum-escalation discipline, non-compensatory gates, hostile controls and protected mixed-task evaluation required to answer that question.

## 1. Why fixed pipelines are insufficient

Research episodes do not fail in one way. A stalled problem may be caused by missing evidence, wrong representation, non-identifying observations, insufficient model capacity, a bad search route, invalid assumptions, resource limitations, tool failure, or multiple interacting causes.

A fixed workflow often reacts to these situations by moving to the next stage or retrying the same class of action. An unconstrained agent may react by adding tools, larger models or new representations. Both approaches can waste resources and, more importantly, can create scientific overreach.

P-C asks whether the solver should instead be controlled by **active scientific obligations**.

Examples:

- acquire evidence for a named claim;
- discriminate between two responsibility hypotheses;
- preserve an invariant while changing representation;
- independently review a high-authority transition;
- resolve an unresolved source identity;
- refute a lower-level sufficiency control before escalating;
- reopen claims affected by a changed premise;
- expose a censored route before declaring bounded saturation.

## 2. State model

Let solver state be:

`S = (P, K, H, O, U, M, R, A, C)`

where:

- `P` — problem contract;
- `K` — current knowledge/claims and evidence;
- `H` — plural hypothesis/responsibility portfolio;
- `O` — active obligations;
- `U` — uncertainty and identifiability state;
- `M` — memory/provenance/dependence;
- `R` — resource/capacity state;
- `A` — authority state;
- `C` — available action/control repertoire.

Actions are supplied by parent components. The P-C claim, if any, concerns **coordination and escalation semantics**.

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
- external-review obligation.

Hard obligations cannot be traded away for average utility.

## 4. Action families

P-C may select among parent-owned actions such as:

- direct reasoning/analysis;
- retrieval/search route;
- formal check/proof/synthesis;
- computation/simulation;
- experimental measurement;
- discriminating probe;
- model fitting/optimization;
- representation change;
- decomposition change;
- method change;
- external review/benchmark;
- local repair;
- selective reopening;
- bounded stop.

The solver should expose why each action is admissible and which obligations it targets.

## 5. Responsibility diagnosis

A failed attempt should update a plural responsibility portfolio rather than force one cause.

Candidate responsibility classes:

- `EVIDENCE_MISSING`;
- `SEARCH_COVERAGE`;
- `REPRESENTATION_LIMIT`;
- `MODEL_OR_METHOD_CAPACITY`;
- `ASSUMPTION_INVALID`;
- `NON_IDENTIFYING_BENCHMARK`;
- `RESOURCE_LIMIT`;
- `AUTHORITY_BLOCK`;
- `EXECUTION_FAILURE`;
- `INTERACTION_ONLY`;
- `MULTIPLE_INDEPENDENT`;
- `CANNOT_IDENTIFY`.

When evidence does not identify the cause, the preferred action may be a discriminator rather than a repair.

## 6. Witnessed minimum escalation

Escalation changes the scientific action/search space. P-C uses an ordered ladder, whose exact domain instantiation can vary:

- J0 direct/local action;
- J1 search/query change;
- J2 local algorithm/parameter repair;
- J3 decomposition change;
- J4 model/method expansion;
- J5 representation change;
- J6 new instrument/data source;
- J7 objective/problem-contract revision;
- J8 external adoption/new programme.

The ladder is not a universal ontology. What matters is the control law:

1. identify the currently blocked obligation;
2. enumerate lower-level admissible actions;
3. test whether they are sufficient or non-identifying;
4. require an insufficiency/ceiling witness when possible;
5. choose the lowest level predicted to discharge the obligation;
6. bind preservation/reopen obligations;
7. evaluate post-change consequences.

### False Jump

A higher-level change occurs while a lower-level repair was sufficient.

### Missed Jump

Repeated local actions continue despite evidence that the current action space cannot resolve the obstruction.

## 7. Parent threats

P-C is strongly threatened by mature fields:

- POMDPs and metareasoning;
- Bayesian experimental design and active learning;
- adaptive workflow/BPM/operations systems;
- blackboard and multi-agent architectures;
- model-based diagnosis and multiple-fault diagnosis;
- CEGIS/CEGAR and formal synthesis;
- systems engineering/change control;
- self-driving laboratories;
- scientific agent frameworks;
- automated theorem proving and program repair.

The paper must compare against **composed parents**, not isolated weak baselines.

## 8. Protected task families

### 8.1 Simple direct controls

Problems solvable by one obvious action. Added decomposition, diagnosis or Jump is overreach.

### 8.2 Hidden mechanistic discovery

Multiple hypotheses require sequential evidence and targeted experiments.

### 8.3 Multiple-fault diagnosis

Two independent faults and an interaction-only case test plural responsibility.

### 8.4 Formal proof/synthesis

The solver must distinguish a proof gap, model gap and execution/tool gap.

### 8.5 Governed experiment

An experiment is scientifically useful but requires authority or safety permission. Correct science without authority must not self-execute.

### 8.6 Representation insufficiency

The current language cannot separate surviving alternatives; a representation change is genuinely required.

### 8.7 Lower-level sufficiency control

A local repair solves the problem. Escalation is penalized.

### 8.8 Non-identifying benchmark

A benchmark failure is compatible with representation or capacity failure. A discriminator is required.

### 8.9 Frontier opportunity

The solver identifies a new problem but must not confuse interestingness with authority or novelty.

## 9. Baselines

1. fixed research pipeline;
2. unconstrained agentic planner;
3. direct/simple control;
4. strongest parent-composed adaptive controller;
5. frozen V1;
6. contracted P-C solver.

All arms receive matched external tools/data/resources where possible.

## 10. Evaluation

Primary:

- justified-terminal rate;
- false completion;
- V1 per-cell non-regression;
- responsibility correctness;
- discriminating-probe value;
- false Jump rate;
- missed Jump rate;
- minimum-level accuracy;
- authority/integrity violations;
- preservation/reopen correctness;
- `CANNOT_CHECK` calibration.

Secondary:

- cost to decisive evidence;
- total actions;
- latency;
- unnecessary work;
- justified reachability gain;
- expert intervention burden.

No average can compensate a critical integrity/authority regression.

## 11. Hostile controls

### H1 — Correct answer, wrong authority

The solver derives the correct result but lacks adoption authority. Expected terminal: scientifically supported but not self-adopted.

### H2 — Infrastructure failure masquerading as science

Tool execution fails. Expected: execution failure, not hypothesis refutation.

### H3 — Coupled decomposition

Naive decomposition breaks a global constraint. The solver should preserve coupling or avoid decomposition.

### H4 — Multiple valid repair orders

Two repair sequences are both scientifically valid. Strict path agreement is not required if final obligations and invariants match.

### H5 — False Jump lure

A larger model/representation is available but unnecessary. The lower-level fix should win.

### H6 — Missed Jump lure

Repeated searches cannot distinguish hypotheses because the representation lacks a required variable. Continued local search is overreach.

### H7 — Criterion gaming

A changed success criterion makes an apparent pass. Contract binding must detect it.

## 12. Formal directions

### 12.1 Obligation reachability

Given obligation set `O` and action transition system, characterize whether all hard obligations are dischargeable under resource/authority constraints.

### 12.2 Minimal escalation theorem

Under a partially ordered intervention hierarchy and sufficient diagnostic conditions, characterize when choosing the minimal feasible level is optimal among policies that satisfy hard preservation constraints.

### 12.3 Responsibility observability

Define conditions under which candidate failure causes are distinguishable by available probes.

### 12.4 Non-compensatory planning

Study policies that optimize secondary utility only inside the feasible region defined by scientific/authority predicates.

## 13. Relationship to CSC

P-C is the most direct implementation of the CSC control loop: state, obligations, action selection, diagnosis, escalation and stopping.

But CSC should not be used to inflate P-C. If parent metareasoning + workflow + diagnosis already reproduce its protected decisions, P-C must contract.

## 14. Planned figures

1. Obligation-driven loop vs fixed pipeline.
2. Responsibility hypothesis set and discriminating-probe transition.
3. J0–J8 minimum escalation with lower-level sufficiency controls.
4. Non-compensatory evaluation plane: scientific validity/authority vs cost/reach.
5. Selective reopening after a representation change.

## 15. Honest negative terminals

- `USE_DONOR_COMPOSED_SOLVER`;
- `V1_NONINFERIOR`;
- `MULTI_POLICY_NO_SINGLE_ARCHITECTURE`;
- `V2_OVERREACH`;
- `JUMP_TRIGGER_NOT_CALIBRATABLE`;
- `CANNOT_CHECK`.

## 16. Survival gate

P-C survives only if protected mixed-task evaluation shows material incremental justified reach, lower false completion, better diagnosis, or better calibrated minimum escalation than the strongest parent-composed adaptive solver **without** mandatory-coordinate or V1 parity regression.
