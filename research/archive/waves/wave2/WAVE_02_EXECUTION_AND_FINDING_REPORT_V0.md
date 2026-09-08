# ORION-V2 Wave-02 Execution and Finding Report V0

## 1. Scope

Wave-02 changes the donor programme from “collect and compare theories” into a formal **generalization-and-adaptation layer**.

The wave starts from the user’s correction that a theory designed for one industry cannot simply be copied into ORION. The reusable content must be extracted, generalized, and then revalidated without erasing the native theory’s assumptions or decisions.

## 2. Branch and base

```text
branch: research/wave2-generalized-domain-theories-20260827
base branch: research/wave1-core-20260827
base commit: 9774af22dc25dd8d2ce6a565f40fd87d74b309e5
```

Wave-02 does not alter ORION V1.

## 3. Added formal reference objects

### Conservative theory transport

- `FiniteTheory`
- `AssumptionRecord`
- `TheoryTransport`
- `GeneralizationAssessment`
- `SharedEnvelopeAssessment`
- `assess_theory_transport`
- `assess_shared_envelope`

### Adapted generalized theories

- `ObligationProcessNetwork`
- `ProcessTask`
- `ProcessMarking`
- `assess_process_soundness`
- `ResponsibilityHypothesis`
- `DiagnosticProbe`
- `assess_responsibility`
- `FiniteViabilitySystem`
- `viability_kernel`
- `justified_capture_kernel`
- `CorrespondenceLink`
- `assess_correspondence_chain`

### Machine schema

- `GENERALIZATION_RECEIPT_SCHEMA_V0.json`

Every object is non-authorizing.

## 4. Reference test execution

The isolated Wave-02 suite was executed with the new modules under a temporary package surface:

```text
20 passed
0 failed
runtime approximately 0.05 seconds
network/model dependencies: none
```

The tests cover:

- exact interpretation;
- decision-relative adaptation;
- sound over-approximation;
- transition drift;
- assumption erasure;
- resource understatement;
- authority amplification;
- native judgment drift;
- shared remote-domain envelope without semantic identity;
- process soundness;
- absent authority;
- unrecoverable process branches;
- interaction-only failure;
- multiple diagnoses and discriminating probes;
- contradictory diagnoses;
- unsafe high-value shortcuts;
- existential versus robust viability;
- accumulated correspondence uncertainty;
- identity without anchors;
- required-invariant violation.

## 5. Implementation defect found and corrected

The first process-network model allowed a task to fire repeatedly whenever its prerequisites remained fulfilled. A review task could therefore consume the same resource more than once and manufacture a false failure.

The marking now binds `executed_task_ids`. Wave-02’s finite semantics treats a task as one occurrence. Recurrent workflows require explicit occurrence identities or a different cyclic-process theory.

This finding is retained because it exposes a generalization hazard: event occurrence semantics cannot be inferred from task labels.

## 6. Principal scientific findings

### F1 — Generalization is not representation similarity

A theory is generalized only when a declared transport preserves registered native judgments and dynamics. Lexical, embedding, or ontology similarity can retrieve candidates but cannot validate them.

### F2 — Generalization has several grades

Exact interpretation, conservative generalization, decision-relative adaptation, and sound abstraction are scientifically different. One untyped “mapping success” terminal is invalid.

### F3 — Assumptions are first-class

An omitted assumption can reverse a target decision while every mapped state and label still appears plausible. Every native assumption therefore requires a typed disposition.

### F4 — Resource and authority semantics must survive

An abstraction that understates cost can choose an infeasible plan. An abstraction that raises authority can convert internal evidence into an unauthorized conclusion. Both fail closed.

### F5 — Remote domains share envelopes, not identities

Management stage gates and engineering V&V can inhabit the same obligation-process envelope for registered release decisions. This does not make management and engineering semantically identical.

### F6 — Four adapted theory families are currently useful

- obligation processes;
- plural responsibility diagnosis;
- calibrated correspondence chains;
- justified viability.

These connect directly to solver obligations, diagnosis, regime transport, and frontier reachability.

### F7 — Parent ownership is substantial

Institution theory, abstract interpretation, theory morphisms, workflow nets, diagnosis, viability, metrology, equating, political linking, causal transportability, and semantic-change research already own the component ideas. ORION’s strict residual is unresolved.

## 7. Framework implications

The candidate V2 core should expose:

```text
native theory adapter
transport assessment
shared envelope assessment
target-native revalidation
mapping-expiration and selective-reopen hooks
```

It should not contain one universal domain embedding that silently decides equivalence.

A solver should treat an imported theory as a proposal with a scope, preservation grade, assumptions, cost relation, authority ceiling, epoch, and falsifiers.

## 8. Paper implications

Wave-02 opens provisional candidate **V2-C11 — Conservative Generalization and Adaptation of Domain Theories for Machine Scientific Reasoning**.

C11 remains standalone only if a protected benchmark shows incremental value over the strongest parent composition. Otherwise its method and artifacts merge into:

- C01/C03 donor hunting and machine donor reduction;
- C02 context-relative structural knowledge space;
- C04 solver integration;
- C06 cross-generation comparability.

## 9. Unfinished work

- full repository test and CI execution;
- property-based and exhaustive finite-model expansion;
- full-text native donor cards;
- institution/theory-morphism strongest-product implementation;
- target-native adapters beyond the finite examples;
- counterexample-reflection and mapping-expiration code;
- provenance/dependence integration;
- protected cross-domain benchmark;
- exact V1 collision audit for each generalized object;
- independent domain-expert review.

## 10. Honest terminal

```text
WAVE_02_FORMALIZATION = BUILT_FOR_REVIEW
ISOLATED_REFERENCE_TESTS = 20_PASS
FULL_REPOSITORY_REGRESSION = NOT_YET_EXECUTED
PROTECTED_EXTERNAL_EVALUATION = NOT_EXECUTED
STRICT_ORION_RESIDUAL = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```
