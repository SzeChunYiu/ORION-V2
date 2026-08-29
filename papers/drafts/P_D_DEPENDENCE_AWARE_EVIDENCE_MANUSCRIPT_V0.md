# When Agreement Is Not Independence
## Dependence-Aware Scientific Evidence and Dynamic Evaluation

**P-D manuscript V0**

**Status:** draft candidate; no novelty/publication authority. Absorbs C07 + C09 and relevant C08 provenance components under the frozen paper contraction.

## Abstract

Scientific assurance often counts apparently distinct observations, reviewers, models, replications or validators as cumulative evidence. This can be badly calibrated when those items share data, models, prompts, instruments, transformations, authors, assumptions or evaluation criteria. A second problem arises when evaluation is performative: publication, deployment, benchmark disclosure or policy adoption changes the data-generating or strategic environment, invalidating the assumption that an evaluator is passive. We study a combined evidence-control object in which support is represented by typed support families and dependence/provenance relations, evaluation criteria and evaluator identities are frozen before outcome access, and post-deployment response can trigger revalidation or selective reopening. The method distinguishes provenance integrity from scientific corroboration and scientific support from authority. We compare against dependent meta-analysis, graphical/common-cause models, ensemble-diversity methods, provenance systems, performative prediction, strategic classification, mechanism design and causal policy evaluation. The paper survives only if the integrated dependence + dynamic-evaluation model prevents false authority or improves calibration beyond the strongest parent composition on protected cases.

## 1. Motivation

Scientific systems increasingly aggregate evidence produced by automated pipelines:

- multiple model agents review one claim;
- several analyses reuse the same dataset;
- different papers inherit the same benchmark or preprocessing code;
- replicated experiments share calibration/instrument conditions;
- evaluators use the same foundation model or reference corpus;
- benchmark publication changes model training and participant behavior;
- policy deployment changes the population it is evaluated on.

Counting these items as independent can create false confidence. Keeping perfect provenance still does not solve the problem unless the scientific meaning of the dependence is represented.

P-D therefore studies **evidence support under explicit dependence and response structure**.

## 2. Core distinctions

### 2.1 Provenance vs corroboration

A digest/provenance record can establish that two artifacts were produced reproducibly or share lineage. It does not establish that either artifact is scientifically correct.

### 2.2 Distinct source labels vs independence

Two validators can be different processes but depend on the same data/model/rubric. Independence is a scientific relation, not a count of identities.

### 2.3 Static evaluation vs performative evaluation

A benchmark or policy evaluator can change the environment once published/deployed. A result validated in the pre-response environment may not remain valid afterward.

### 2.4 Support vs authority

High agreement or posterior confidence does not authorize a claim beyond the valid evaluator/support roots.

## 3. Evidence object

For evidence item `e`, bind:

- content identity;
- source/data identity;
- generating model/instrument/process;
- transformations;
- assumptions;
- evaluator/criterion identity;
- time/epoch;
- target claim and support role;
- dependence edges/common-cause family;
- provenance lineage;
- authority ceiling.

A claim `q` is supported by one or more **support families**. Each family is a set/hyperedge of premises sufficient under the declared criterion.

A claim remains supported after revocation only if at least one complete valid support family survives.

## 4. Dependence taxonomy

Candidate dependence types:

- exact duplicate;
- shared raw data;
- shared preprocessing/code;
- shared model/checkpoint;
- shared prompt/system instructions;
- shared retrieval corpus;
- shared instrument/calibration;
- shared human expert/source;
- shared hidden assumption;
- sequential derivation;
- common benchmark/evaluator;
- institutional incentive coupling;
- unknown dependence.

The taxonomy is not itself the contribution. The scientific task is to determine which dependence relations materially change the support/evaluation decision.

## 5. Dynamic/performative evaluation

Let evaluator environment be `E_t`. A scientific action/publication/deployment `a_t` can change it:

`E_{t+1} ~ F(E_t, a_t)`.

A static evaluation assumes `F(E_t,a_t) = E_t` or that changes are irrelevant. P-D explicitly allows response.

Examples:

- a benchmark is released and models are trained on it;
- a clinical/policy rule changes behavior and therefore outcome distribution;
- publication causes strategic adaptation;
- a research metric becomes a target and is gamed;
- an automated reviewer changes what authors optimize.

A validation receipt should therefore state whether it assumes passive evaluation, models response, or cannot assess post-deployment validity.

## 6. Hypotheses

### H1 — Dependence-aware support reduces false corroboration

Explicit common-source/support families should prevent multiple dependent items from being counted as independent corroboration.

### H2 — Provenance-only corroboration is insufficient

A custody-valid, replay-identical artifact can still be scientifically defective. The evaluator must inspect claim-relevant semantics/evidence, not only digests.

### H3 — Revocation should be support-family selective

Revoking one premise invalidates a certificate only when no independent complete support remains.

### H4 — Performative response can invalidate static passes

A system should detect or at least flag when deployment/publication changes the environment enough that the frozen static evaluator no longer supports the same claim.

### H5 — Evaluation authority must not self-amplify

A high automated score or reviewer agreement cannot grant scientific/publication authority absent the required authority roots.

## 7. Parent threats

- dependent/correlated meta-analysis;
- graphical models and common-cause reliability;
- evidence combination under dependence;
- epidemiological interference;
- ensemble diversity/correlation analysis;
- W3C PROV and provenance systems;
- reproducibility/replication methodology;
- performative prediction;
- strategic classification and Goodhart-style metric response;
- mechanism design;
- causal policy evaluation/interference;
- preregistration/registered reports;
- benchmark governance.

The P-D residual is the integrated scientific-control consequence: support-family validity, evaluator custody, dynamic response, selective reopening and authority.

## 8. Protected benchmark families

### 8.1 Duplicate-source reviewers

Three “independent” reviewers use the same hidden base model/reference data. Compare naive vote, dependence-aware vote and truly independent review.

### 8.2 Provenance-perfect scientific bug

A deterministic replay exactly reproduces a wrong scientific result. Provenance checks pass. Semantic/known-answer evaluation must fail.

### 8.3 Alternative support survives

A claim has two complete support families. One is revoked. The claim remains valid under the other.

### 8.4 Hidden common calibration

Several experiments share one wrong calibration. Naive replicate count overstates support.

### 8.5 Benchmark publication response

A frozen evaluator predicts good performance before benchmark disclosure; after disclosure, systems adapt to the benchmark without improving the target scientific property.

### 8.6 Policy-induced winner reversal

Deployment changes behavior so the previously best policy/model becomes worse or incomparable.

### 8.7 Stable negative control

A case where response is negligible ensures the model does not invent performativity everywhere.

### 8.8 Authority lure

A highly confident, independently supported result lacks publication/adoption authority. The system must preserve the boundary.

## 9. Baselines

1. naive source/reviewer count;
2. provenance-only validation;
3. standard dependent evidence/meta-analysis parent;
4. static evaluation;
5. strongest composed dependence + performative-evaluation parent;
6. P-D integrated model.

## 10. Metrics

Primary:

- false corroboration rate;
- calibration under dependence;
- effective-support classification;
- support-family revocation correctness;
- selective-reopen precision/recall;
- post-response invalidity detection;
- false performativity alarms;
- evaluator/criterion mutation detection;
- authority violation rate.

Secondary:

- evaluator burden;
- provenance/dependence annotation cost;
- revalidation cost;
- decision latency;
- robustness across dependence misspecification.

## 11. Formal directions

### 11.1 Support hypergraph semantics

Let claim support be a family of sufficient premise sets `F(q) = {S1,...,Sk}`. Under revoked set `R`, claim support survives iff there exists `Si` with `Si ∩ R = ∅` and all other validity predicates hold.

Study minimal reopening and dependence-aware variants where premises are not Boolean independent.

### 11.2 Dependence-adjusted evidence

Develop a general interface that accepts parent-specific dependence models rather than inventing one universal formula. Compare covariance, graphical/common-cause and qualitative dependence certificates.

### 11.3 Dynamic evaluator validity

Let `V(E, q)` be evaluator validity in environment `E`. Characterize interventions `a` for which `V(E,q)` is not transportable to `F(E,a)` without revalidation.

### 11.4 Criterion/evaluator custody

Formalize run identity under immutable subject, case, criterion and evaluator. Mutation after output access creates a new evaluation identity.

## 12. Relationship to CSC

P-D supplies CSC's **assurance dynamics**: what evidence actually counts, how support survives changes, and when evaluation itself changes the world.

It also supplies the strongest argument that scientific control cannot be reduced to workflow correctness: provenance-perfect execution can be scientifically wrong.

## 13. Planned figures

1. Evidence/provenance/dependence graph with alternative support families.
2. Naive reviewer count vs dependence-aware support.
3. Selective reopening after one support family fails.
4. Static vs performative evaluator loop.
5. Authority ceiling independent of evidence confidence.

## 14. Honest negatives

- dependent meta-analysis/common-cause parents already solve the support problem;
- performative effects are too domain-specific for a shared model;
- dependence annotation is too costly or unidentifiable;
- the integrated interface improves traceability but not scientific decisions;
- post-deployment revalidation cannot be operationalized prospectively;
- only a governance resource, not a scientific result, survives.

## 15. Survival gate

P-D survives only if protected evaluation shows materially better calibration, false-authority prevention, selective reopening, or response-induced invalidity detection than strongest dependence + performative-evaluation parent composition without increasing critical false-negative/false-positive errors beyond the frozen criterion.
