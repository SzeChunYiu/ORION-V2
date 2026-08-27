# Same Position, Different Worlds
## Context-Relative Scientific Relations, Comparability and Transport

**P-B manuscript V0**

**Status:** draft candidate; no novelty/publication authority. Absorbs C02 + C06 + C08 + Wave-05/C12 transport by the frozen paper contraction.

## Abstract

Scientific objects can be equivalent for one purpose and non-equivalent for another. Two models may agree observationally yet differ causally; two measurements may be linkable only under anchors and uncertainty; two framework versions may preserve a decision while changing representation; an approximate abstraction may be safe for bounded control but unsafe for exact scientific claims. Mature parent fields already provide specialized relation theories, including bisimulation, statistical experiment comparison, causal and Markov equivalence, measurement invariance, metrological traceability, abstract interpretation, robust/stochastic simulation, ontology alignment and provenance. We investigate whether a shared scientific interface can coordinate these relations without collapsing their native semantics. The proposed receipt `Relation(left,right|context)` binds relation type, native witnesses, preserved and lost judgments, uncertainty/error, counter-probes, epoch/expiry, authority and selective-reopening consequences. The paper explicitly rejects a universal embedding distance. Its survival gate is a protected cross-parent benchmark demonstrating that typed coordination prevents unsafe reuse or unnecessary reopening beyond the strongest parent-specific composition while preserving native judgments.

## 1. Motivation

Scientific reuse increasingly crosses contexts:

- versions of a model or dataset;
- institutions/instruments/calibrations;
- simulation and physical experiment;
- source and target domains;
- old and new taxonomies;
- deterministic and stochastic abstractions;
- multiple representations of the same underlying system.

Persistent identity is insufficient. A DOI, hash, object ID or provenance chain can tell us that objects are related historically, not whether the same scientific claim remains valid.

Likewise, generic similarity is insufficient. High embedding similarity does not tell us whether predictions, interventions, decisions or authority transfer.

P-B therefore treats relation claims as **typed and context-relative scientific objects**.

## 2. Parent relation families

The paper begins by reconstructing, not replacing, parent theories:

- exact/behavioral equivalence and bisimulation;
- testing/simulation relations;
- Markov and causal equivalence;
- Blackwell/Le Cam comparison of experiments;
- sufficient statistics;
- abstract interpretation and sound abstraction;
- lumpability and computational mechanics;
- measurement invariance/equating/linking;
- metrological traceability and uncertainty;
- causal transportability;
- ontology/model evolution;
- provenance and version lineage;
- stochastic/approximate simulation and robust control.

Each family answers a different question. The P-B hypothesis is that scientific systems need a **coordination layer** that makes those differences machine-visible.

## 3. Relation receipt

For objects `K1`, `K2` and context `C`, define:

`R = Relation(K1, K2 | C)`

with fields:

- object identities and source projections;
- relation family/type;
- context/purpose/registered judgments;
- witness/certificate;
- required assumptions/anchors;
- preserved judgments;
- lost or unresolved distinctions;
- error/uncertainty/tolerance;
- counter-probes;
- directionality;
- composition rules;
- epoch/validity interval;
- recoverability mapping;
- affected commitments on invalidation;
- authority ceiling;
- terminal status.

Candidate statuses include exact, conservative, approximate, partial, unresolved and incomparable.

## 4. Core hypotheses

### H1 — Context necessity

A relation valid for one registered judgment need not be valid for another. Systems that erase context will generate false transport.

### H2 — Loss visibility

Approximate or decision-relative mappings can be useful if removed distinctions and error are explicit. Hidden loss drives false equivalence.

### H3 — Cross-generation comparability is more than identity

Objects can retain persistent identity while becoming scientifically non-comparable due to calibration, representation, population, criterion or authority drift.

### H4 — Relation composition must be conservative

A chain of exact and approximate links inherits the weakest valid semantics; uncertainty and unresolved assumptions cannot disappear through composition.

### H5 — Invalidated relations trigger selective reopening

When a link expires or an anchor fails, only commitments that depend on that relation without alternative support should reopen.

## 5. Known-answer parent suites

Before any cross-parent claim, P-B must pass native suites from the parent theories.

Examples:

- bisimulation-equivalent and non-equivalent transition systems;
- observationally equivalent but interventionally distinct causal models;
- measurement-linking cases with anchor failure;
- exact vs approximate abstraction cases;
- provenance-related objects with changed semantics;
- stochastic transport chains with accumulating error.

The interface is invalid if its normalized output changes the native parent verdict.

## 6. Cross-parent benchmark

The discriminating benchmark contains cases that require more than one relation family.

### Case family A — Version + measurement drift

A model version changes representation while the instrument calibration also changes. Persistent identity and provenance remain intact. The question is whether an old threshold decision remains valid.

### Case family B — Causal + observational reuse

Two models agree on observed distributions but differ under intervention. A prediction transfers; a policy recommendation does not.

### Case family C — Approximate abstraction + authority

An abstraction has certified error small enough for control but not for a high-precision scientific claim. The controller must keep the lower authority ceiling.

### Case family D — Reticulate provenance

A result has multiple parents and alternative support families. One parent mapping expires. Some claims reopen; others remain supported.

### Case family E — Multi-epoch composition

A chain of mappings crosses several versions. One approximate link and one unresolved anchor prevent exact terminal promotion.

## 7. Baselines

1. persistent-ID/provenance only;
2. embedding similarity;
3. single parent relation family selected manually;
4. strongest parent-composed relation product;
5. P-B typed coordination interface.

The parent-composed product must be allowed to use the same native libraries/theories. P-B cannot win merely because it has more vocabulary.

## 8. Metrics

Primary:

- native parent verdict preservation;
- false exact-equivalence rate;
- unsafe transport rate;
- correct partial/incomparable classification;
- uncertainty/error conservation;
- silent-reuse prevention;
- selective-reopen precision/recall;
- source/recoverability preservation.

Secondary:

- useful reuse rate;
- unnecessary refusal;
- certificate size;
- adjudication burden;
- composition cost.

## 9. Hostile controls

### C1 — Same identifier, changed scientific meaning

An object keeps identity/provenance but changes population/calibration. P-B must refuse naive reuse.

### C2 — High similarity, wrong relation

Text/embeddings are nearly identical, but decision semantics differ.

### C3 — Low lexical similarity, exact registered relation

Different representations preserve all registered decisions. P-B should permit declared reuse.

### C4 — Approximate chain laundering

An approximate link inside a longer chain must prevent exact terminal promotion.

### C5 — Alternative support survives

A relation fails but a claim has independent support. Global reopening is an error.

### C6 — Context expiry

A relation certificate is valid only under a prior epoch. Reuse after expiry should be `CANNOT_CHECK`/revalidate rather than pass.

## 10. Formal directions

### 10.1 Relation partial order

Study whether relation receipts admit a refinement/strength order under fixed context: exact relation implies selected weaker relations, but not conversely.

### 10.2 Conservative composition

Define sufficient conditions for composition `R12 ∘ R23` to preserve registered judgments and correctly accumulate loss/uncertainty.

### 10.3 Reopen semantics

Given claims dependent on relation receipts, prove minimal reopening under invalidation when complete alternative support families are explicit.

### 10.4 Counter-probe completeness

For decision-relative equivalence classes, characterize when a finite probe set can expose every distinction relevant to an expanded interface.

## 11. Relationship to CSC

P-B supplies CSC's **state-transport law**. Scientific controllers regularly change model, representation, context and epoch. Without typed relation semantics, a controller cannot know what old knowledge remains valid.

However P-B must stand alone as a scientific-relations paper even if the CSC field hypothesis is rejected.

## 12. Planned figures

1. Relation-family map: observation, behavior, intervention, decision, measurement, abstraction, provenance.
2. Receipt schema and authority/loss coordinates.
3. Example where one object pair has different relation status under two contexts.
4. Approximate multi-epoch chain showing conservative error/authority propagation.
5. Selective reopening after one relation expires.

## 13. Honest negatives

- strongest parent composition already handles all benchmark cases;
- the shared schema adds bureaucracy but no decision value;
- relation selection is too expert-dependent to automate;
- cross-parent composition laws are domain-specific;
- approximate transport cannot be compared fairly across relation families;
- only a software interchange format, not a scientific result, survives.

## 14. Survival gate

P-B survives only if protected evaluation demonstrates at least one cross-parent combination in which the typed interface materially reduces unsafe reuse or unnecessary reopen/refusal relative to strongest parent composition while preserving every native parent verdict.

Otherwise use `PARENT_FAMILY_SUFFICIENT`, `ORCHESTRATION_RESOURCE_ONLY`, `NOT_FIDELITY_PRESERVING`, or `CANNOT_CHECK`.
