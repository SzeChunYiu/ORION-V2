# When Can One Scientific Result Stand for Another?
## Context-Relative Relations, Conservative Transport and Selective Reopening

**P-B manuscript V3 — top-tier pre-results Article draft**  
**Primary target archetype:** multidisciplinary computational-science Article  
**Status:** evidence-independent manuscript, formal obligations, protected result slots, figures and contraction outcomes are complete. No universal relation calculus, theorem, empirical gain or submission readiness is claimed before execution.

## Abstract

Scientific automation repeatedly reuses results across models, datasets, instruments, populations, software versions and representational levels. Such reuse is often justified by a generic similarity score, shared identifier or informal claim that two objects are “equivalent”. Yet the relation needed to preserve a causal conclusion can differ from that needed to preserve a measurement, prediction, proof, procedure or authorized action. We study a typed interface for **context-relative scientific relations**. A relation receipt binds the source and target, the decision to be transported, relation family and direction, assumptions, approximation and uncertainty, computational realization, local semantics, authority and counter-probes. Composition is permitted only when native parent conditions remain valid; an invalidated relation selectively reopens downstream claims whose sufficient support is lost. We compare the interface with universal similarity metrics, persistent-identifier matching and the strongest federation of causal, measurement, formal-abstraction, behavioural, procedural and semantic-interoperability parents. Protected evaluations include known-answer parent suites, calibration iteration, approximate numerical realization, competence transport, boundary-interface cases and naturalistic representation changes in two sciences. The proposal survives only if it preserves native judgments or improves decisions beyond parent-specific routing without imposing harmful universal structure.

## Introduction

A scientific result rarely moves unchanged through an entire research programme. A measurement is recalibrated. A model is simplified. A biological finding is applied to a new population. A simulation replaces a physical experiment. A proof is implemented in floating-point software. An ontology aligns two databases. An expert procedure is converted into instructions for another person or machine. Each transition relies on a relation between a source and a target.

The word “similarity” hides the diversity of these relations. Two experiments may have similar outputs while answering different causal questions. Two models may be behaviourally equivalent for one policy but not another. A mathematical abstraction can preserve a safety property while erasing the intervention distinction needed for scientific interpretation. A procedure can be textually reproduced without transporting competence. A data object can remain scientifically comparable while its permitted use changes. The correct relation is therefore indexed by a context and a decision.

Mature sciences already provide strong relation theories: causal transportability, measurement invariance, metrological traceability, statistical experiment comparison, abstraction and simulation relations, formal refinement, ontology matching, robustness, procedural transfer and more. P-B does not claim these mechanisms. Its question is whether a small typed interface can preserve their native verdicts, expose when relations do not compose, and control downstream reopening when a relation later fails.

We test three claims. First, context-relative typing prevents errors produced by universal similarity or identifier-based reuse. Second, conservative composition exposes exact, approximate and obstructed transport across heterogeneous relation families. Third, relation-specific invalidation enables selective rather than global reopening. The strongest lower bound is an expert-routed federation of the native parent theories.

## Results architecture

### Different scientific decisions require different relations

The benchmark registers a source, target and decision before any relation is selected. Relation families include:

- causal/transport;
- measurement/comparability;
- behavioural or policy equivalence;
- formal abstraction/refinement;
- statistical experiment/information comparison;
- semantic/ontology correspondence;
- procedural or competence transport;
- computational/numerical realization;
- provenance/identity;
- authority/custody.

No family is assumed reducible to another. The same pair can be related for one decision and unrelated for another.

`RelationReceipt = (`
`source, target, registered_decision, family, direction, assumptions, scope, approximation, uncertainty_form, implementation, local_semantics, authority, preserved_judgments, lost_judgments, counter_probes, evaluator, epoch)`.

**Primary result slot PB-R1.** Report relation-selection accuracy and native-verdict preservation for universal similarity, identifier matching, embedding distance, strongest parent routing and P-B.

**Required sentence form:**

> Across [n] known-answer cases, P-B selected the native relation family in [x]% of cases and preserved [y]% of registered judgments. The largest error reduction occurred when [same pair/different decision condition], whereas [parent/federation] remained superior in [stratum].

### Conservative composition exposes exact, approximate and blocked chains

A chain of relations is not automatically a relation of the same strength. Direction can reverse, approximation can accumulate, uncertainty form can change, semantic context can be lost and authority may not transport at all.

For a chain `r_1; ...; r_k`, the composition procedure returns:

- `EXACT_COMPOSITION`;
- `APPROXIMATE_WITH_BOUND`;
- `DECISION_STABLE_WITHIN_SCOPE`;
- `RELATION_FAMILY_CHANGE_REQUIRED`;
- `LOCAL_OR_GLOBAL_OBSTRUCTION`;
- `AUTHORITY_NOT_TRANSPORTABLE`;
- `CANNOT_CHECK`.

A composition receipt contains the native parent proof/certificate or explicit reason no valid composition exists.

**Primary result slot PB-R2.** Report false-exact composition, missed-valid composition and downstream decision error. Formal subfamilies additionally report theorems, proof obligations or countermodels.

**Required sentence form:**

> P-B prevented [n] false-exact compositions and retained [m] valid chains. Approximation bounds [were/were not] decision-stable under the frozen tolerance; the dominant obstruction was [type].

### Calibration and evaluator iteration require cross-epoch relations

Scientific standards and instruments can improve. The old and new results should not be silently merged or globally discarded. A calibration-iteration case binds the old standard/instrument, discrepancy, revision, independent constraints, uncertainty and affected claims.

`CalibrationIterationReceipt = (`
`construct_or_quantity, standard_before, instrument_or_evaluator_before, discrepancy, revision, standard_after, instrument_or_evaluator_after, invariants, uncertainty, independent_constraints, affected_claims, comparison_identity)`.

**Primary result slot PB-R3.** Report whether systems correctly preserve, translate or reopen historical claims after a legitimate iteration and after an outcome-conditioned criterion change.

**Required sentence form:**

> Following the frozen calibration revision, P-B preserved [claims], translated [claims] with [bounds] and reopened [claims]. The [baseline] incorrectly [globalized/silently inherited] the revision in [n] cases.

### Semantic and procedural transport test non-formal relations

A shared label or successful data query does not prove shared scientific meaning. A procedure or demonstration can likewise contain competence not preserved by text. Boundary-interface cases record local projections, common invariants, translation rules and prohibited inferences. Competence cases compare instruction-only, demonstration, supervised practice and native expert execution.

**Primary result slot PB-R4.** Report local-semantic preservation, prohibited-inference detection and competence-transport success under independent native adjudication.

**Required sentence form:**

> The shared interface preserved [invariants] but left [local meanings] unresolved. P-B blocked [n] unsafe cross-projection inferences. In competence cases, [transport mode] was necessary for [decision], while explicit instructions were sufficient in [negative-control stratum].

### Invalid relations selectively reopen downstream commitments

Claims can depend on alternative sufficient support families. Revoking one relation should reopen only claims for which no complete valid family survives.

Given relation `r`, the system computes affected support paths and returns:

- claims remaining supported;
- claims requiring revalidation;
- claims reverting to unresolved;
- claims whose authority changes independently of scientific support.

**Primary result slot PB-R5.** Report selective-reopening precision and recall versus global invalidation, no reopening and native parent procedures.

**Required sentence form:**

> When [relation class] failed, P-B reopened [x] of [y] claims requiring revalidation and preserved [z] independently supported claims. False reopening cost was [value], compared with [baselines].

### Naturalistic cross-domain restoration and efficiency

The interface is tested in at least two sciences with materially different native semantics. Candidate families include computational modelling plus measurement-heavy experimental science, or causal population transport plus formal/numerical model transformation. Domain experts define native judgments before seeing system outcomes.

FULL, MINUS-family-typing, MINUS-counter-probes, MINUS-selective-reopen, PARENT-replacement, F0 federation and SIMPLE controls are evaluated with compute, expert labour and implementation burden.

**Primary result slot PB-R6.** Report cross-domain validity and the quality–cost Pareto frontier.

**Required sentence form:**

> P-B [did/did not] remain on the Pareto frontier after native semantics were restored. The integrated interface added [decision gain] at [cost], while [parent] remained locally preferable for [case family].

## Discussion

Scientific reuse is not a single operation. The same model pair can support one prediction and fail another; the same dataset can be comparable yet governed differently; the same proof can survive abstraction while its floating-point implementation fails. P-B is valuable only if it makes these distinctions operational without replacing mature relation sciences.

A positive result would support a federated view. Native parents remain the source of valid relation semantics and certificates. The shared interface binds their context, direction, uncertainty, approximation and authority so that cross-parent systems can reason about reuse, composition and invalidation. This is an interfield contribution rather than a claim to a universal metric.

Approximation is a central test. Machine-mediated systems often pass results through long chains, and each local approximation can appear modest. Scientific safety depends on whether the cumulative relation preserves the registered decision. A chain can be mathematically bounded but scientifically useless because the relevant threshold is crossed. Conversely, exact identity of an artifact may not imply transport of a claim to a different population or instrument.

Selective reopening provides the practical reason to model support and relation structure. Global invalidation is safe but destructive; no reopening is efficient but unsound. A relation-aware support graph should preserve valid alternatives and localize revalidation. Yet the bookkeeping cost could exceed its value in simple workflows, so contextual activation and parent deference are required.

The paper also rejects semantic imperialism. Shared machine interfaces should coordinate science without forcing every domain into one ontology. Local projections and prohibited inferences are not defects to be eliminated automatically. They can be the scientifically correct representation of plural practices.

## Methods

### Parent-known-answer suites

For each relation family, native specialists construct cases with exact verdicts or strong adjudication:

- transportable versus non-transportable causal effects;
- invariant versus non-invariant measurement structures;
- behavioural equivalence relative to policies/properties;
- sound/unsound abstractions and refinements;
- exact/approximate numerical implementations;
- semantically aligned and deceptively aligned schemas;
- instruction-sufficient and tacit/competence-dependent procedures;
- scientifically equivalent but differently authorized uses.

The native verdict and decision context are frozen before integrated system development.

### Arms

1. persistent identifier/exact artifact match;
2. lexical or embedding similarity;
3. universal learned relation metric;
4. strongest single native parent;
5. expert-routed F0 parent federation;
6. P-B FULL;
7. component removals and native parent replacements;
8. SIMPLE direct method where one relation is sufficient.

### Composition semantics

Composition functions are family-specific. The common layer only records the result, proof/certificate, assumptions, error/uncertainty and prohibited inference. The system cannot manufacture a generic composition when the native parent has no valid rule.

Formal propositions are stated with explicit domains. Candidate results include:

- conservation of direction and scope;
- monotonic non-improvement of approximation without a new warrant;
- authority non-transport absent an external root;
- selective reopening under alternative sufficient support;
- countermodels for mixed-family composition.

A proposition becomes a theorem only after proof and independent checking.

### Approximation and uncertainty

Numerical tolerances, probabilistic uncertainty, interval bounds, credal sets and semantic ambiguity remain typed. An interval enclosure is not interpreted as a probability. An approximate relation cannot be promoted to exact by composition. Decision stability is evaluated against a frozen threshold or native criterion.

### Naturalistic cases

Domain cases bind:

- source and target identities;
- native problem and decision;
- instruments/models/software;
- relation parent;
- expert adjudicator and dependence;
- data/custody permissions;
- success and failure criteria.

Domain teams receive both native and P-B outputs without being required to adopt P-B terminology.

### Outcomes

Primary:

- relation-family selection;
- native-verdict preservation;
- false-exact and missed-valid composition;
- downstream decision correctness;
- selective-reopening precision/recall;
- critical unsafe transport;
- resource-adjusted Pareto status.

Secondary:

- annotation and proof burden;
- semantic ambiguity retained;
- expert disagreement;
- unnecessary refusal/reopening;
- relation/evaluator expiry detection.

Authority and custody violations are hard failures rather than weighted errors.

### Statistical and formal analysis

Formal cases use proof or exhaustive/model-checking evidence where feasible. Empirical cases use pre-registered estimands with clustering for shared parent, domain or evaluator. Family-level results are reported rather than pooled into a misleading universal score when semantics differ.

## Limitations frozen before results

- relation families may proliferate;
- a common interface may still bias native semantics;
- expert adjudication can be contested or dependent;
- composition may be undecidable or computationally expensive;
- approximation bounds can be unavailable;
- competence and authority relations can resist open benchmarking;
- naturalistic domains may support only local conclusions.

## Availability and disclosure slots

- **Formal artifacts:** `[proof assistant/model checker/repository identity]`.
- **Data and cases:** `[release and custody statement]`.
- **Code:** `[commit, environment and replay instructions]`.
- **AI assistance:** `[models, roles, verification and human accountability]`.
- **Competing interests:** `[complete before submission]`.

## Honest terminal

```text
P_B_MANUSCRIPT_SURFACE = COMPLETE_PRE_RESULTS
PARENT_KNOWN_ANSWER_SUITES = PARTIAL_OR_OPEN
FORMAL_COMPOSITION_RESULTS = OPEN
NATURALISTIC_CROSS_DOMAIN_RESULTS = OPEN
SELECTIVE_REOPENING_VALUE = OPEN
TOP_TIER_SUBMISSION_READY = NO
POSSIBLE_TERMINALS = ARTICLE__INTEROPERABILITY_RESOURCE__PARENT_CONTRACTION__CANNOT_CHECK
```
