# ORION-V2 Wave 06 — Unified Generalization Stack V0

**Status:** reconciliation and composition protocol over Waves 03–05 and parallel PR #29. No new mathematical novelty or scientific authority is claimed.

## 1. Why reconciliation is required

Two Wave-03 lanes independently attacked the same problem from different directions:

- **decision-envelope lane** (`PR #26`): derive the smallest registered-decision and transition-preserving envelope, then require target-native adaptation;
- **conservative-adaptation lane** (`PR #29`): certify exact, conservative, decision-relative and sound interpretations using round trips, backward reflection, assumptions, resource calibration, counterexamples, expiry and composition.

Both are valuable. Treating them as competing framework cores would create duplicated identities, inconsistent terminals and unclear paper ownership.

Wave 06 assigns one ordered stack.

## 2. Ownership stack

### L0 — native theory reconstruction

Owner: native-domain card and source ledger.

Contains native states, actions, transitions, judgments, assumptions, resources, validity/authority, history and epoch.

### L1 — minimal envelope derivation

Owner: `generalization_compiler.py` from PR #26.

Question:

> What is the coarsest finite state partition preserving the registered judgments and action-indexed successor-block structure?

Output:

```text
COMPILED_EXACT
COMPILED_DECISION_RELATIVE
CANNOT_CHECK_MISSING_JUDGMENT
CANNOT_CHECK_EMPTY_REGISTRY
```

This layer discovers/constructs a candidate generalized carrier. It does not certify a full scientific interpretation.

### L2 — interpretation and transport laws

Owner: `theory_transport.py` and `meta_formalization.py` imported from PR #29.

Question:

> Does a declared source-to-envelope interpretation satisfy the required exact, conservative, decision-relative or sound-abstraction laws?

Checks include:

- identity and epoch;
- total mappings;
- forward transition simulation;
- backward reflection where required;
- native/generalized round trips;
- judgment preservation and declared information loss;
- assumption treatment and revalidation;
- resource calibration;
- authority non-amplification;
- counterexample reflection;
- certificate validity and composition;
- target-native realization.

Parent-law references include finite satisfaction conditions, Galois connections, abstract-transformer soundness, lens laws and conservative extensions.

### L3 — independent native recovery

Owner: Wave 04 `native_recovery.py` and strict expectation corpus.

Question:

> Does the generalized mechanism actually reproduce independently frozen native decisions and native counterexamples on declared cases?

This layer is empirically/logically independent of the interpretation's own expected outputs.

### L4 — stochastic/approximate transport

Owner: Wave 05 `stochastic_transport.py`.

Question:

> When exact laws do not hold, are transition and observable errors bounded, epochs connected, uncertainty propagation declared and protected decisions stable?

This layer is optional for exact theories and mandatory for approximate/stochastic claims.

### L5 — target realization and target-native validation readiness

Owner: PR #29 target adaptation certificate plus Wave-03 target role/calibration/test contract.

Question:

> Are target roles, calibrations, registered decisions, native tests, authority and epochs sufficiently bound to run protected target validation?

Strongest pre-evaluation terminal:

```text
READY_FOR_PROTECTED_TARGET_EVALUATION
```

This is not target success.

### L6 — protected target evaluation and adoption

Owner: external/protected evaluation and adoption authority.

No internal layer can self-promote to L6.

## 3. Unified stack statuses

```text
READY_FOR_PROTECTED_TARGET_EVALUATION
BLOCKED_MINIMAL_ENVELOPE
BLOCKED_INTERPRETATION_LAWS
BLOCKED_NATIVE_RECOVERY
BLOCKED_APPROXIMATE_TRANSPORT
BLOCKED_TARGET_REALIZATION
CANNOT_CHECK
```

The status is the first unresolved/invalid layer in order. Later success cannot compensate for an earlier failure.

## 4. Identity discipline

A unified receipt must bind:

- native theory identity and epoch;
- envelope identity;
- interpretation identity;
- native recovery case identities;
- stochastic transport identity when present;
- target adaptation identity;
- source/evidence identities;
- authority ceiling;
- unresolved assumptions;
- failure and counterexample receipts.

A list of green statuses with no shared identities is not a stack.

## 5. Theory relationships

```text
minimal envelope derivation
    !=
interpretation certification
    !=
native recovery
    !=
approximate transport
    !=
target validation
```

The layers answer different questions and must not be collapsed into one `GENERALIZED` boolean.

## 6. Integration findings

1. PR #26 and PR #29 are complementary.
2. PR #29 owns richer transport/certificate laws; PR #26 owns the minimal-envelope compiler and six domain-neutral families.
3. Wave 04 supplies an independent falsifier missing from both Wave-03 lanes.
4. Wave 05 supplies error-bounded semantics missing from both exact lanes.
5. C11 should own at most the stack/interface and empirical reduction; parent fields own most individual laws.
6. Duplicate `AdaptationStatus` names should remain namespace-qualified until one reviewed interface is frozen.
7. No code path should silently convert `READY_FOR_PROTECTED_TARGET_EVALUATION` into scientific success or adoption.

## 7. Required migration work

- replace duplicate research schemas with one versioned envelope/certificate family;
- adapt Wave-04 cases to PR-29 `ScientificTheory` and `TheoryInterpretation` objects;
- connect Wave-05 stochastic errors to PR-29 uncertainty/resource/certificate composition;
- bind identity continuity across all layers;
- run all tests from PR #26, PR #29, Waves 04 and 05 in one branch;
- construct cross-layer hostile cases;
- compare the unified stack with the strongest parent-composed implementation;
- keep PR #26 and PR #29 open until reconciliation review accepts every migrated object.

## 8. Paper ownership

- **C01/C03:** donor discovery and machine reduction.
- **C02:** structural relation/envelope families.
- **C04:** solver consumption of admitted generalized objects.
- **C06:** temporal/semantic comparability and expiry.
- **C07:** uncertainty/dependence composition.
- **C11:** unified generalization/adaptation stack only if distinct incremental value survives.
- **Possible C12:** stochastic scientific transport only if independently separated.

## 9. Current terminal

```text
PARALLEL_WAVE_03_LANES = RECONCILED_BY_LAYER_OWNERSHIP
PR29_REFERENCE_LAWS = IMPORTED
WAVES_03_TO_05_TEST_INTEGRATION = RUNNING
PROTECTED_GENERALIZATION_VALUE = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```