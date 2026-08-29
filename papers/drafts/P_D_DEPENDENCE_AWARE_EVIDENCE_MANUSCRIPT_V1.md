# When Agreement Is Not Independence
## Dependence-Aware Scientific Evidence, Distributed Review and Dynamic Evaluation

**P-D manuscript V1 — design manuscript; protected results open**

**Status:** revised after the human-thinking/lived-knowledge saturation reopen. No novelty/publication authority.

## Abstract

Scientific assurance often counts apparently distinct observations, reviewers, models, replications or validators as cumulative evidence. This is badly calibrated when they share data, models, prompts, instruments, teachers, source traditions, transformations or evaluation criteria. A second problem arises when scientific cognition is distributed: a decision can depend on a model, human, instrument, database and procedural convention, so process identity alone does not reveal where support or failure originated. A third arises when evaluation is performative: publication, deployment, benchmark disclosure or the evaluation act itself changes the data-generating or strategic environment. We study an integrated evidence-control object in which support is represented by typed support families and dependence/provenance relations; source and acquisition mode are explicit when scientifically material; criticism is tracked through **uptake** rather than vote count; evaluator identities and criteria are bound before outcome access; and observer coupling can trigger revalidation or selective reopening. The proposal does not claim ownership of correlated meta-analysis, graphical/common-cause models, provenance, social epistemology, distributed cognition, strategic classification or performative prediction. It survives only if the integrated model prevents false corroboration/authority or improves calibration beyond strongest parent composition on protected cases.

## 1. Why more reviewers can mean less than more evidence

AI-mediated research increasingly aggregates outputs from automated pipelines:

- several model agents review one claim;
- multiple analyses reuse one dataset;
- different papers inherit one benchmark or preprocessing stack;
- replicated experiments share calibration or instrument conditions;
- evaluators use the same foundation model, rubric or corpus;
- a human expert teaches several agents the same procedure;
- a benchmark is published and then optimized against;
- deployment changes participant or population behaviour.

Counting these as independent can produce false confidence. Perfect provenance helps expose lineage but does not itself tell us the scientific consequence of the lineage. A replay-identical result can still be scientifically wrong.

The human/practice reopen adds a further warning: the relevant cognitive unit can be a **distributed system**. If a critical state is carried by a human, tool, diagram, instrument calibration or procedural convention, attributing the whole episode to the base model hides both support and failure dependencies.

P-D therefore studies scientific support under explicit **dependence, distributed episode structure and evaluator response**.

## 2. Core distinctions

### 2.1 Provenance versus corroboration

A custody-valid artifact can be reproduced exactly and still support a wrong scientific conclusion. Provenance proves lineage under a contract; corroboration requires claim-relevant evidence semantics.

### 2.2 Distinct identities versus independence

Different process IDs, model instances or human reviewers do not imply independent evidence. Independence is a scientific relation among information-generating processes.

### 2.3 Criticism count versus criticism uptake

A review system can collect many objections while never changing the claim or exposing why an objection was rejected. Critical scrutiny has epistemic value only when the process makes the targeted assumption, response and warranted state consequence inspectable.

### 2.4 Agent performance versus distributed-episode performance

A scientific conclusion can depend on several agents, tools and artifacts. The support/failure topology belongs to the episode, not to one actor by default.

### 2.5 Static versus performative evaluation

An evaluator valid in environment `E_t` may become invalid after publication, deployment or the measurement/evaluation intervention changes that environment.

### 2.6 Support versus authority

High posterior confidence, reviewer agreement or independent evidence does not grant publication/adoption/execution authority beyond externally valid roots.

## 3. Evidence object V1

For evidence item `e`, bind where material:

- content identity;
- source/data identity;
- source/acquisition mode;
- generating model/instrument/person/process;
- demonstration/teacher/source-tradition identity;
- transformations;
- assumptions;
- evaluator/criterion identity;
- time/epoch;
- target claim and support role;
- dependence edges/common-cause family;
- provenance lineage;
- observer/intervention coupling;
- authority ceiling.

A claim `q` is supported by one or more sufficient **support families**:

`F(q) = {S1, ..., Sk}`.

A claim remains supported after revocation only if at least one complete valid family survives and every relevant relation/evaluator predicate remains valid.

## 4. Dependence taxonomy

Candidate dependence types include:

- exact duplicate;
- shared raw data;
- shared preprocessing/code;
- shared model/checkpoint;
- shared prompt/system instructions;
- shared retrieval corpus;
- shared instrument/calibration;
- shared human expert/teacher;
- shared testimony/source tradition;
- shared demonstration trajectory;
- shared hidden assumption;
- sequential derivation;
- common benchmark/evaluator;
- common institutional incentive;
- communication/social influence among reviewers;
- unknown dependence.

The taxonomy is not the contribution. The question is which relations materially change the scientific support decision and which can be ignored safely.

## 5. Criticism receipts and uptake

For a review or objection:

`CriticismReceipt = (claim, critic_identity, critic_dependence, objection, target_assumption, evidence, response, state_delta_or_reason_no_change, authority)`.

Possible outcomes include:

- claim revised;
- support weakened;
- assumption made explicit;
- counter-probe created;
- criticism rejected with evidence;
- `CANNOT_CHECK`;
- logged without action.

The last outcome should not count as “successful independent review” merely because a reviewer existed.

### Protected hypothesis

Does tracking targeted assumptions and uptake improve the detection/correction of scientific defects compared with reviewer vote, free-form critique count or provenance-only review logs?

## 6. Distributed cognitive episode

When a scientific decision depends on several components, represent the episode as a transformation/dependence topology:

`DCE = (actors, tools, artifacts, observations, transformations, communications, local_states, support_edges, authority_edges, time)`.

The object is deliberately neutral about whether cognition is “really” in a person, model or group. It exposes where information enters, changes, is lost, is checked and becomes authoritative.

Candidate failures:

- `DISTRIBUTED_STATE_LOSS` — a critical state exists in one component but is unavailable at the decision point;
- `TACIT_INTERFACE_LOSS` — competent performance is lost across a handoff despite preserved explicit instructions;
- `COMMON_SOURCE_REVIEW` — several critics depend on the same hidden source/model;
- `PROVENANCE_PERFECT_SEMANTIC_BUG` — lineage is exact, scientific interpretation wrong.

## 7. Dynamic/performative evaluation

Let evaluator environment be `E_t`. A publication, deployment or evaluation action `a_t` may change it:

`E_{t+1} ~ G(E_t, a_t)`.

A validation receipt states whether it assumes:

- passive/stable evaluation;
- bounded modeled response;
- observed response requiring transport/revalidation;
- response unknown / `CANNOT_CHECK`.

Examples:

- benchmark release changes training data;
- policy deployment changes behaviour/outcomes;
- review criteria become targets and are gamed;
- measurement changes the process being measured;
- an automated reviewer changes author optimization;
- a query/experiment perturbs the scientific object.

P-D does not assume performativity everywhere. Stable negative controls are mandatory.

## 8. Core hypotheses

### H1 — Dependence-aware support reduces false corroboration

Explicit common-source/support families prevent dependent items from being counted as independent support.

### H2 — Provenance-only assurance is insufficient

Replay/custody can pass while claim-relevant semantic evaluation fails.

### H3 — Revocation is support-family selective

A claim reopens only when no complete valid support family remains.

### H4 — Self-review is dependent by default

Critiques generated by the same underlying model/context are not independent evidence simply because they appear in separate agent roles.

### H5 — Criticism needs uptake

A review system with no observable path from objection to warranted state change can produce review theatre without scientific correction.

### H6 — Distributed episode structure can expose otherwise hidden failure/support paths

A model-only view may misattribute evidence or overlook lost state at human/tool/artifact boundaries.

### H7 — Performative/observer response can invalidate static passes

Where the evaluation action changes the relevant environment, frozen static validity does not automatically transport.

### H8 — Evaluation authority does not self-amplify

Agreement or confidence cannot grant authority absent required roots.

## 9. Parent threats

- dependent/correlated meta-analysis;
- Bayesian networks/common-cause reliability;
- evidence combination under dependence;
- epidemiological interference;
- ensemble diversity/correlation;
- W3C PROV and reproducible workflow systems;
- reproducibility/replication methodology;
- performative prediction;
- strategic classification and Goodhart-style response;
- mechanism design;
- causal policy evaluation/interference;
- preregistration/registered reports;
- benchmark governance;
- social epistemology and testimony;
- distributed cognition and human–computer interaction.

P-D's residual, if any, is the composition-level scientific consequence: support-family validity + dependence + criticism uptake + distributed episode topology + evaluator response + selective reopen + authority.

## 10. Protected benchmark families

### B1 — Duplicate-source reviewers

Several apparently independent reviewers share one hidden base model/reference source.

### B2 — Truly independent positive control

Independent sources agree. A conservative system must not erase legitimate support gain.

### B3 — Provenance-perfect scientific bug

Deterministic replay reproduces a wrong result exactly. Provenance passes; semantic known-answer check fails.

### B4 — Alternative support survives

Two sufficient support families; one revoked. Claim remains supported under the other.

### B5 — Hidden common calibration

Several experiments share one incorrect calibration.

### B6 — Teacher dependence

Multiple learned procedures trace to one demonstration/teacher assumption. Count the common source.

### B7 — Self-review common cause

Separate critic agents share the same base model/system prompt/retrieval corpus. Compare with externally independent review.

### B8 — Criticism uptake versus review theatre

Both arms receive an objection. Only one identifies the target assumption and updates/rejects it under evidence.

### B9 — Distributed state handoff

A decisive warning/calibration/state is present in one tool/human artifact but not propagated to the final decision-maker.

### B10 — Benchmark publication response

Pre-release evaluator predicts good target performance; post-release optimization improves benchmark score without target improvement.

### B11 — Policy-induced winner reversal

Deployment changes behaviour so an earlier winner becomes worse or incomparable.

### B12 — Stable non-performative control

Evaluation does not materially change the environment. P-D should not invent revalidation churn.

### B13 — Observer coupling

The measurement/probe itself alters the system relevant to the claim. The receipt must represent the coupling.

### B14 — Authority lure

Strong independent evidence lacks adoption/publication authority. Preserve the boundary.

## 11. Baselines

1. naive source/reviewer count;
2. provenance-only validation;
3. standard dependent-evidence/meta-analysis parent;
4. static evaluation;
5. reviewer-majority/free-form critique;
6. strongest composed dependence + provenance + performativity parent;
7. P-D without distributed/uptake extensions;
8. P-D V1 full interface.

All arms receive matched evidence and source access.

## 12. Metrics

Primary:

- false corroboration rate;
- calibration under dependence;
- effective-support classification;
- support-family revocation correctness;
- selective-reopen precision/recall;
- hidden-common-source detection;
- criticism defect-correction rate;
- false “independent review” rate;
- distributed-state-loss detection;
- post-response invalidity detection;
- false performativity alarms;
- evaluator/criterion mutation detection;
- authority violation rate.

Secondary:

- annotation burden;
- provenance/dependence inference cost;
- reviewer burden;
- revalidation cost;
- latency;
- robustness to missing dependence edges;
- unnecessary reopening/refusal.

## 13. Formal directions

### 13.1 Support hypergraph semantics

Under revoked set `R`, support survives iff some valid sufficient family remains and all relation/evaluator predicates still hold.

### 13.2 Dependence-adjusted support

Accept parent-specific quantitative/qualitative dependence models rather than inventing one universal formula.

### 13.3 Criticism graph

Model objections as edges to claims/assumptions with evidence and state-update consequences. Study whether graph structure predicts defect resolution beyond vote count.

### 13.4 Distributed support attribution

Study minimal information/topology needed to identify which components contribute independent support or failure.

### 13.5 Dynamic evaluator validity

Characterize interventions for which `V(E,q)` cannot be transported to `V(G(E,a),q)` without revalidation.

### 13.6 Criterion/evaluator custody

Freeze subject, case, criterion and evaluator identity before outcome access; mutation creates a new evaluation identity.

## 14. Relationship to Machine Epistemics

P-D supplies the programme's **assurance dynamics**: what evidence actually counts, how criticism changes state, what survives revocation, and when evaluation itself changes the world.

The human/practice extension matters because scientific assurance is often distributed and socially mediated. But P-D should remain a testable evidence/evaluation paper even if the field label is rejected.

## 15. Figures

1. Evidence/provenance/dependence graph with alternative support families.
2. Naive reviewer count versus dependence-aware support and criticism uptake.
3. Distributed cognitive episode showing information/support loss at a handoff.
4. Static versus performative/observer-coupled evaluator loop.
5. Authority ceiling independent of evidential confidence.

## 16. Honest negatives

- dependent evidence + performative-prediction parents already solve all protected cases;
- criticism-receipt structure adds bureaucracy but no defect correction;
- distributed topology adds logging but no decision value;
- dependence annotation is too costly or unidentifiable;
- observer effects are too domain-specific;
- only a governance/traceability resource survives.

## 17. Survival gate

P-D survives only if protected evaluation shows materially better calibration, false-authority prevention, criticism uptake, selective reopening, distributed-failure detection or response-induced invalidity detection than strongest parent composition without increasing critical errors beyond the frozen criterion.

Until those results exist, this is a **design manuscript**.

```text
P_D_V1_ARCHITECTURE = COMPLETE_ENOUGH_FOR_PROTECTED_EXPERIMENT
SELF_REVIEW_INDEPENDENT_BY_DEFAULT = FALSE
CRITICISM_UPTAKE = TESTABLE_COORDINATE
DISTRIBUTED_COGNITIVE_EPISODE = TESTABLE_TOPOLOGY
PERFORMATIVITY_EVERYWHERE = REJECTED
PROTECTED_RESULTS = OPEN
PUBLICATION_READY = NO
```
