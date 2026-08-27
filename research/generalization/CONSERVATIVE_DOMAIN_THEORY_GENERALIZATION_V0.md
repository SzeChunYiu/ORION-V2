# Conservative Domain-Theory Generalization for ORION-V2 V0

**Status:** Wave-02 research theory and transparent finite reference model. This document is not a final V2 ontology, novelty verdict, or adoption authority.

## 1. Research question

How can ORION learn from an industry- or discipline-specific theory without either copying it into a context where its assumptions fail, or stripping away so much native meaning that the resulting “general theory” preserves only a verbal resemblance?

Wave-02 treats generalization as a **proved transport problem**.

A native theory is reconstructed first in its own language. It may enter an ORION envelope only through a mapping that preserves a declared family of judgments, transitions, assumptions, resource semantics, authority ceilings, counterexamples, provenance, and epoch restrictions. Application to another field requires an independent target-native transport and target-native validation.

The intended geometry is a cospan:

```text
native source theory --source transport--> generalized envelope
native target theory --target transport--> generalized envelope
```

It is not an unchecked direct analogy from source to target. A common envelope establishes neither semantic identity nor scientific authority.

## 2. Expert cell and veto roles

### Formal-semantics lead

Background: institution theory, theory morphisms, abstract interpretation, model theory, and formal specification.

Role: define exact interpretation, conservative generalization, decision-relative adaptation, and sound abstraction.

Veto: no transport when preservation is merely asserted, or when a many-to-one map silently changes an exact statement into an approximation.

### Rotating native-domain lead

Background rotates among management and operations, systems engineering, diagnosis and reliability, metrology and psychometrics, political methodology, linguistics, control, ecology, law, medicine, and the arts.

Role: reconstruct the field’s native objects, admissible models, actions, assumptions, failure modes, decisions, and quantitative semantics before ORION mapping.

Veto: no generic object may erase a native assumption or replace a native judgment with an ORION-friendly proxy.

### Scientific-control lead

Background: sequential decision theory, experiment design, control, viability, workflow, and resource systems.

Role: test whether a proposed coordinate changes solving, discrimination, reachability, stopping, or reopening.

Veto: no coordinate enters the generalized state merely because it can be represented.

### Measurement and comparability lead

Background: metrology, measurement invariance, test equating, latent scaling, causal transport, and diachronic semantics.

Role: bind anchors, invariants, uncertainty, tolerance, scale, context, and epoch.

Veto: persistent identifiers and lexical similarity cannot stand in for comparability.

### Reliability and diagnosis lead

Background: model-based diagnosis, FMEA, fault trees, multiple faults, interaction faults, medicine, and incident analysis.

Role: preserve plural responsibility and require discriminating probes.

Veto: no universal single-root-cause or earliest-stage rule.

### Scientific-governance lead

Background: evidence governance, publication claims, authority, performative evaluation, and hostile benchmark design.

Role: prevent authority amplification, donor laundering, post-outcome mapping changes, and novelty inflation.

Veto: no transport receipt grants truth, novelty, publication, or adoption.

## 3. Parent reduction

The programme does not claim to invent cross-domain formalization.

Institution theory already supplies logic-independent signatures, sentences, models, satisfaction, and notation-change invariance. Theory morphisms and related specification work already own formal translations and modular reuse.

Abstract interpretation already owns sound abstraction, over-approximation, abstract transformers, and the proof obligation connecting concrete and abstract semantics.

Conservative-extension and theory-morphism traditions already own the idea that new structure may be added without changing old-language consequences.

Blackwell-style comparison already owns decision-relative comparison of information structures rather than syntactic similarity.

Workflow nets, model-based diagnosis, viability theory, metrological traceability, psychometric invariance and equating, political scale linking, causal transportability, and diachronic semantics already own major special cases.

The only possible ORION residual is a machine-replayable **scientific operational transport receipt** that binds all of the following together:

- native judgment or satisfaction preservation;
- actions and transition behavior;
- registered probes, interventions, and decisions;
- assumptions and calibrations;
- resource and capacity bounds;
- evidence and validator dependence;
- authority non-amplification;
- provenance, history, context, and epoch;
- counterexample reflection;
- selective reopening after mapping failure;
- strongest-donor-product reduction.

Whether that integration is distinct from the strongest parent composition remains `CANNOT_CHECK`.

## 4. Native theory package

A domain theory package is provisionally represented as:

```text
T_D = (
  signature,
  admissible_models,
  native_sentences,
  satisfaction,
  operational_states,
  actions,
  transitions,
  probes,
  native_judgments,
  uncertainty_and_identifiability,
  resources_and_capacity,
  authority_and_validity,
  provenance_history_epoch
)
```

The package is not an ontology checklist. A field may mark a coordinate `NOT_APPLICABLE`; unavailable information is `UNKNOWN`. Those terminals are different.

A coordinate is retained only when it changes a registered decision, action, reachability result, transport verdict, or reopening footprint.

## 5. Generalized envelope

A generalized envelope has corresponding operational roles, but it is indexed by a declared context `C` containing at least:

- registered queries and interventions;
- target decision family;
- resource limits and tolerances;
- protected scientific constitution;
- population, scale, and epoch;
- permitted approximation class.

The envelope is therefore written conceptually as `G_C`, not as one universal ORION ontology.

## 6. Transport object

A domain transport contains explicit maps for:

```text
signatures
models and states
actions
sentences and claims
probes and interventions
native judgments
resource quantities or bounds
authority classes
provenance, history, and epoch
```

### 6.1 Exact judgment preservation

For every registered native state and decision, the native judgment must equal the generalized judgment at the mapped state. For logical theories, the analogous requirement is satisfaction preservation.

### 6.2 Sound abstraction

When exact equality is impossible, a generalized result may be set-valued only when it contains the native result. This supports one-sided safety reasoning and must not be reported as exact equivalence.

### 6.3 Transition simulation

Every registered native transition must have a corresponding generalized transition under the action and state maps. Matching labels without matching behavior is invalid.

### 6.4 Complete assumption ledger

Every native assumption receives exactly one disposition:

```text
PRESERVED
CALIBRATED
RELAXED
DROPPED
NOT_APPLICABLE
```

Every disposition other than `PRESERVED` requires evidence. An unlisted assumption is treated as erasure, not as a harmless omission.

### 6.5 Resource conservatism

For an upper-bound interpretation, the generalized cost of a mapped action must not be lower than the native upper bound, except within a declared tolerance. Lower bounds, stochastic costs, and interval costs require separately typed relations.

A generic theory that makes a native operation appear cheaper is invalid for planning.

### 6.6 Authority non-amplification

The generalized authority ceiling must not exceed the authority of the native judgment. Translation cannot convert an internal estimate into an externally authorized scientific conclusion.

### 6.7 Counterexample reflection

A native counterexample inside the declared transport domain must remain representable and addressable. A generalization that hides native falsifiers is invalid even when all positive examples map successfully.

### 6.8 Epoch and reopening

Every transport binds source and target epochs. Changed assumptions, signatures, calibrations, evaluators, resources, or authority may expire the transport and reopen affected conclusions.

## 7. Transport grades

The finite reference implementation emits:

```text
EXACT_INTERPRETATION
CONSERVATIVE_GENERALIZATION
DECISION_RELATIVE_ADAPTATION
SOUND_ABSTRACTION
INVALID_TRANSITION_DRIFT
INVALID_NATIVE_JUDGMENT_DRIFT
INVALID_ASSUMPTION_ERASURE
INVALID_RESOURCE_UNDERSTATEMENT
INVALID_AUTHORITY_AMPLIFICATION
CANNOT_CHECK
```

### Exact interpretation

The declared finite state and action structures are bijective; transitions, costs, and all native judgments match.

### Conservative generalization

The generalized theory may add structure or merge distinctions irrelevant to the registered decisions, while preserving all declared native judgments and transitions.

### Decision-relative adaptation

Only a declared subset of native judgments is preserved. The mapping is valid for that decision family and says nothing about unregistered future questions.

### Sound abstraction

The generalized theory safely over-approximates the native result. It supports sound one-sided reasoning but not exact identity.

## 8. Shared position of remote domains

Two remote domains occupy the same generalized position only when both independently pass transport checks into the same context-indexed envelope and share a registered generalized decision or behavior.

The shared-envelope assessment emits:

```text
SHARED_EXACT_ENVELOPE
SHARED_CONSERVATIVE_ENVELOPE
DECISION_RELATIVE_NEIGHBORS
NO_SHARED_REGISTERED_DECISION
INVALID_TRANSPORT
CANNOT_CHECK
```

This gives a rigorous meaning to the idea that politics, quantum computation, management, engineering, linguistics, medicine, or art may be near in ORION space. They are near under a declared role, probe, and decision structure—not because their prose embeddings are close.

The assessment explicitly refuses semantic identity.

## 9. Adaptation into a target field

A source-domain method cannot be executed in a target merely because both map into the same envelope. The required sequence is:

1. reconstruct source and target theories independently;
2. verify both transports;
3. identify the generalized operation and all retained assumptions;
4. instantiate target-native parameters and calibrations;
5. translate the operation into target-native action space;
6. run target-native known-answer and hostile checks;
7. measure resource and authority changes;
8. preserve failures and `CANNOT_CHECK` outcomes;
9. compare against the target field’s strongest native method.

Source success alone never determines the target terminal.

## 10. Adapted theory families in Wave-02

Wave-02 defines four candidate generalized families:

1. **Generalized Obligation Process Network** — adapts workflow nets, stage gates, systems verification and validation, legal procedure, and scientific obligation control.
2. **Plural Responsibility Diagnosis System** — adapts model-based diagnosis, FMEA, medicine, incident analysis, and scientific failure attribution.
3. **Calibrated Correspondence Chain** — adapts metrological traceability, psychometric equating, political scale linking, causal transport, and diachronic semantics.
4. **Justified Viability System** — adapts control, ecology, learning spaces, operations, and frontier-science reachability under hard constraints.

The catalogue records which native semantics survive and which industry-specific assumptions remain outside the shared object.

## 11. Hostile controls

A generalization protocol must include at least:

- same words but different native judgments;
- different words but exact structural preservation;
- an omitted native assumption;
- a many-to-one map that destroys a future decision;
- a native transition with no generalized simulation;
- native resource cost understated by the generic theory;
- internal evidence promoted to external authority;
- an approximate map reported as exact;
- source-domain success followed by target-native failure;
- a generalized result tied by the strongest parent composition;
- a mapping changed after protected outcomes;
- two domains with no shared registered decision despite superficial similarity.

## 12. Machine objects

Wave-02 adds non-authorizing reference objects:

```text
FiniteTheory
AssumptionRecord
TheoryTransport
GeneralizationAssessment
SharedEnvelopeAssessment
ObligationProcessNetwork
ResponsibilityHypothesis
CorrespondenceLink
FiniteViabilitySystem
```

The known-answer suite covers exact transport, decision-relative transport, sound abstraction, transition drift, assumption erasure, resource understatement, authority amplification, decision drift, process soundness, missing authority, unrecoverable branches, interaction-only responsibility, non-identifiability, robust versus existential viability, uncertainty accumulation, and invariant violation.

Passing those tests establishes only the finite reference semantics.

## 13. Paper implication

A provisional paper candidate is opened as **V2-C11 — Conservative Generalization and Adaptation of Domain Theories for Machine Scientific Reasoning**.

Its parent-subsumption risk is very high. Institution theory, theory morphisms, abstract interpretation, conservative extension, model-driven engineering, and formal ontology alignment may absorb most of the candidate.

A standalone paper survives only if the operational receipt and cross-domain benchmark improve native-decision preservation, false-analogy rejection, assumption/resource/authority violation detection, useful remote transfer, novelty contraction, or machine replay over the strongest parent union.

Otherwise C11 becomes methodology and infrastructure inside C01/C03 and C02.

## 14. Current terminal

```text
CONSERVATIVE_DOMAIN_THEORY_GENERALIZATION = FORMAL_REFERENCE_CANDIDATE
PARENT_OWNERSHIP = SUBSTANTIAL
STRICT_ORION_RESIDUAL = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```
