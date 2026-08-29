# ORION-V2 Wave 03 — Generalization Compiler and Target Adaptation V0

**Status:** formal research specification and transparent finite reference semantics. No novelty, scientific truth, framework admission, or publication authority is granted.

## 1. Why another wave is necessary

Wave 01 discovered remote structural neighbours. Wave 02 introduced conservative transports from native theories into context-indexed generalized envelopes. The remaining gap is operational:

> Given a fully reconstructed domain theory, what is the smallest reusable machine theory that preserves the scientific decisions we care about, and what additional work is required before that theory may be used in another domain?

Merely renaming an industry theory is not generalization. Removing its industry vocabulary is also not generalization if that deletion erases assumptions, actions, costs, counterexamples, authority, or time dependence.

Wave 03 therefore separates two transformations:

```text
VERTICAL GENERALIZATION
native theory -> smallest decision-preserving envelope

HORIZONTAL ADAPTATION
source envelope -> target-native roles, calibrations, actions and tests
```

A common envelope is evidence of a structural relation. It is not permission to run the source-domain method in the target domain.

## 2. Expert cell

### Formal semantics and abstraction lead

Background: institution theory, conservative extension, abstract interpretation, model reduction, automata minimization and causal abstraction.

Role: derive the coarsest decision- and transition-preserving finite envelope and state exactly what its quotient forgets.

Veto: no object may be called general if a smaller equivalent envelope exists or if a mapped result is stronger than the native result.

### Statistics and decision theory lead

Background: Blackwell comparison of experiments, sufficient statistics, rough sets, active learning and formal identification.

Role: make information comparison relative to registered decisions and probes rather than lexical or embedding distance.

Veto: equivalence on a small task family may not be reported as universal informational equivalence.

### Physics, Earth systems and causal abstraction lead

Background: local-to-global methods, contextuality, scale changes, coarse graining, causal macro-models and aggregation effects.

Role: distinguish safe abstraction, observable underdetermination and genuine local/global obstruction.

Veto: current-query preservation does not establish future-query safety.

### Evidence and reliability lead

Background: dependent-effect meta-analysis, survey design effects, common-cause failures, epidemiological interference and validator diversity.

Role: replace source/agent counts with explicit dependence structures and conservative effective-information calculations.

Veto: correlated agreement may not be promoted as independent corroboration.

### Provenance and historical-transmission lead

Background: W3C PROV, workflow lineage, SBOMs, stemmatology, phylogenetic networks and multi-parent inheritance.

Role: represent component-level reticulate inheritance, semantic transport and selective downstream invalidation.

Veto: tree ancestry or a valid digest cannot by itself establish semantic validity.

### Economics, institutions and evaluation lead

Background: the Lucas critique, mechanism design, performative prediction, strategic classification, organizational incentives and policy evaluation.

Role: model how deployment or evaluation changes the process being measured.

Veto: static pre-deployment ranking may not be used after a material response without revalidation.

### Innovation and frontier-portfolio lead

Background: R&D portfolio management, exploration/exploitation, quality-diversity, option value, problem finding and agenda governance.

Role: preserve non-scalar research opportunities and choose portfolios rather than one novelty score.

Veto: novelty, surprise or diversity alone cannot make an opportunity scientifically admissible.

## 3. Native theory package

Wave 03 retains the Wave 02 native package but makes its decision interface explicit:

```text
T_D = (
  signature,
  admissible_models,
  states,
  actions,
  transitions,
  judgments,
  registered_decisions,
  probes_and_interventions,
  assumptions,
  resources_and_capacity,
  validity_and_authority,
  provenance_history_epoch
)
```

A coordinate is included only when it changes a registered judgment, action, transition, reachability result, transport status, cost/risk bound, authority ceiling, or reopening footprint.

`UNKNOWN` and `NOT_APPLICABLE` remain distinct.

## 4. The generalization compiler

### 4.1 Decision registry

Before compression, the native expert declares the exact judgment family to preserve. Examples include:

- a workflow completion or soundness verdict;
- a diagnosis set;
- a policy or experiment decision;
- a safety/viability result;
- a measurement comparison;
- a certificate-transport verdict;
- a legal or institutional authority decision.

No decision registry means the compiler returns `CANNOT_CHECK_EMPTY_REGISTRY`.

### 4.2 Initial observational partition

Native states are grouped only when every registered judgment agrees. This is the weakest quotient compatible with the declared decisions before dynamics are considered.

### 4.3 Transition-stable refinement

The partition is iteratively refined until states in the same block have the same action-indexed successor-block structure. For nondeterministic systems, the complete set of reachable blocks is preserved.

The resulting quotient is the coarsest finite envelope that preserves:

1. all registered judgment values; and
2. the registered action-labelled transition behaviour.

The reference implementation is a finite partition-refinement algorithm. It is parent-owned by automata minimization, bisimulation and abstract interpretation traditions; ORION does not claim the algorithm.

### 4.4 Envelope statuses

```text
COMPILED_EXACT
COMPILED_DECISION_RELATIVE
CANNOT_CHECK_MISSING_JUDGMENT
CANNOT_CHECK_EMPTY_REGISTRY
```

`COMPILED_DECISION_RELATIVE` means at least one native distinction was merged. It is not future-universal.

## 5. Finite propositions under study

### P3.1 — Coarsest registered-decision envelope

For a finite labelled transition system with total registered judgments, partition refinement terminates. The final partition preserves registered judgments and action-indexed successor blocks. Any other partition preserving the same information refines it.

Wave 03 implements and tests this finite proposition. A mechanized general proof remains open.

### P3.2 — No lossy envelope is future-query universal

If a compiled block contains two distinct native states, then a future query exists that distinguishes those states. Therefore no non-injective decision-relative envelope can guarantee preservation for every future scientific question.

This is why every envelope binds a decision family and expiration conditions.

### P3.3 — Shared envelope does not imply target executability

Even when source and target theories independently transport into one envelope, a source operation remains blocked until all required target roles, calibrations, target-native tests, authority bindings and epochs are present.

### P3.4 — Authority and uncertainty compose conservatively

For a chain of valid transports:

- authority ceiling is bounded above by the minimum link ceiling;
- unresolved assumptions and violated invariants accumulate by union;
- exactness is lost when any link is approximate;
- uncertainty and semantic loss accumulate under the registered composition rule.

A source with greater prestige cannot raise the target conclusion above the weakest valid link.

## 6. Target adaptation contract

A target adaptation is represented by:

```text
AdaptationContract = (
  source_roles,
  target_role_map,
  required_calibrations,
  bound_calibrations,
  target_native_tests,
  authority_binding,
  source_epoch,
  target_epoch
)
```

The finite assessor emits:

```text
READY_FOR_TARGET_NATIVE_VALIDATION
BLOCKED_ROLE_MAP
BLOCKED_CALIBRATION
BLOCKED_TARGET_TESTS
BLOCKED_AUTHORITY
BLOCKED_EPOCH
```

`READY_FOR_TARGET_NATIVE_VALIDATION` is still proposal-side. It means the adaptation package is complete enough to run its target-native tests; it does not mean the method works.

## 7. New generalized families

Wave 03 adds six adapted families:

1. **Decision-Relative Information Order**
2. **Contextual Scale-and-Gluing System**
3. **Dependence-Corrected Evidence Network**
4. **Component-Level Reticulate Inheritance System**
5. **Performative Evaluation Dynamics**
6. **Frontier Portfolio and Option System**

Their detailed native recoveries and non-generalized coordinates are recorded in the Wave 03 catalogue.

## 8. Hostile controls

The compiler and families must reject at least:

- a registered judgment missing on one native state;
- same vocabulary but different transition behaviour;
- a quotient safe for the present decision but unsafe for a future query;
- locally nonempty descriptions with no global realization;
- source and target experiments equal on one task but unequal on another;
- four validators sharing one model counted as four independent validators;
- a multi-parent artifact with one unvalidated semantic transform;
- authority amplification through inheritance or transport;
- a static winner that becomes worse after deployment response;
- repeated retraining that cycles rather than converges;
- a high-novelty research idea with no falsifier or downstream decision;
- a portfolio collapsed to one scalar despite Pareto incomparability;
- a target adaptation with no target-native calibration or test.

## 9. What remains domain-specific

A generalized theory must not erase:

- the domain's native state variables and admissibility rules;
- units, calibrations, populations and scale;
- physical, clinical, legal or organizational intervention semantics;
- native resource and risk models;
- standards of evidence and authority;
- deadlines, epochs, institutional roles and rights;
- target-native counterexamples and harm definitions.

These remain adapter-bound native objects.

## 10. Machine artifacts

Wave 03 adds transparent reference modules for:

```text
generalization_compiler
information_order
scale_gluing
evidence_network
inheritance
performative_dynamics
frontier_portfolio
```

They use finite exact enumeration or deterministic graph/partition algorithms and have no model or network dependency.

## 11. Paper implications

### C02 — structural knowledge space

Decision-relative information order and scale/gluing become formal relation families rather than descriptive examples.

### C04 — solver

The solver should consume compiled envelopes and adaptation contracts, not raw donor theories or untyped analogies.

### C06 — comparability

Future-query unsafety and composition rules strengthen the comparability-certificate programme.

### C07 — evidence dependence

The dependence network gains a quantitative equicorrelation/design-effect reference model, while retaining `DEPENDENCE_UNIDENTIFIED` when the correlation basis is absent.

### C08 — reticulate provenance

Component-level lineage and authority-preserving transport are now explicit. Standalone paper status still requires incremental decision value over general provenance.

### C09 — performative evaluation

The reference theory now distinguishes static optima, performative optima, stable policies, convergence and cycles.

### C10 — frontier opportunity discovery

Opportunity selection becomes a constrained Pareto portfolio problem; novelty and diversity are coordinates, not terminals.

### C11 — conservative generalization

C11 becomes the owner candidate for the compiler and target adaptation protocol, with default merge into C01/C02/C03 unless a distinct theorem or protected benchmark survives.

## 12. Current terminal

```text
WAVE_03_GENERALIZATION_COMPILER = FINITE_REFERENCE_IMPLEMENTED
TARGET_ADAPTATION_PROTOCOL = SPECIFIED
GENERALIZED_FAMILIES_ADDED = 6
FULL_NATIVE_VALIDATION = OPEN
MECHANIZED_GENERAL_PROOFS = OPEN
PROTECTED_CROSS_DOMAIN_VALUE = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```