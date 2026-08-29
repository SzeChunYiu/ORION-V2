# ORION-V2 Recursive Development Architecture V1

**Status:** reference architecture complete; protected outcome-generating computation remains open.  
**Owner:** #50. Scientific gates remain #45/#46/#47/#48/#49.

## Central object

ORION-V2 treats scientific intelligence as control over several different kinds of development rather than one monolithic reasoning loop:

1. **scientific-state transition** — what may be accepted, rejected, reopened or left unresolved;
2. **knowledge metabolism** — what source-bound knowledge is decomposed, reconstructed, retained, recombined or recycled;
3. **transfer discovery** — what structure from another domain may apply and what must not transfer;
4. **conceptual development** — when the present distinctions/ontology should specialize, split, merge, bridge, reparameterize, revise or deprecate;
5. **formal mechanics** — the strongest applicable mathematical/formal parent used to certify a relation, invariant, abstraction, closure, equivalence or obstruction;
6. **formalism genesis** — when the current representational language is itself inadequate and a minimal new primitive/object/relation/operation/axiom/calculus is warranted;
7. **scientific-development operator discovery** — what recurring moves distinguish successful from failed/abandoned/redirected research trajectories under explicit observation-bias models;
8. **development meta-policy** — which development mode should be activated for the present episode;
9. **recursive higher-order generalization** — whether lower-level operators/policies admit a more general principle that adds held-out and prospective residual value.

The hierarchy is not a claim that every research episode traverses every level. The controller is explicitly **minimum-sufficient**: direct/native and strongest-parent methods should win whenever they are adequate.

## Cross-layer controller

Canonical implementation: `src/orion_v2/development_controller.py`.

A mode proposal chooses one of:

`NATIVE_DIRECT`, `STRONGEST_PARENT`, `TRANSFER_DISCOVERY`, `CONCEPTUAL_DEVELOPMENT`, `FORMALISM_GENESIS`, `EMPIRICAL_EXPANSION`, `RECURSIVE_META_LEARNING`, `ABSTAIN`.

Every constructive mode binds a prospective identity, target obligations, expected resource cost and mode-specific witnesses. The controller rejects escalation while an equal/lower-cost registered alternative remains sufficient or unresolved.

### Formalism-genesis anti-invention gate

A new formal language is not admissible merely because a problem is difficult. At minimum:

- a representational-deficit witness must be bound;
- semantic validation and predecessor-recovery plans must exist;
- counterexample/obstruction search must be explicit;
- strongest existing parent formalism must have been tested;
- an empirical-expansion/missing-observation alternative must have been considered;
- cheaper sufficient or unresolved alternatives block invention.

This makes **false formalism invention** a first-class error.

### Recursive-meta anti-overgeneralization gate

Recursive meta-learning cannot be triggered by one failed problem. It requires multiple source-bound development episodes, a bounded lower-level saturation/terminal receipt, and held-out routes. Historical fame, citation impact or a named breakthrough pattern is not a trigger.

## Memory

`FrameworkMemoryLedger` is append-only and source-bound. It can retain knowledge, transfers, conceptual transitions, formalisms, development operators, meta-principles and failures. Failed transfer, harmful mechanisms and rejected higher-level abstractions are retained with reopen conditions rather than deleted.

## Formal ownership

The framework does not rename mature mathematics as ORION inventions. Structure mapping, anti-unification, MDL, Formal Concept Analysis, homomorphisms, invariance/equivariance, category/functor machinery, abstract interpretation, model checking, theorem proving and domain-native methods remain parent-owned.

ORION's candidate residual is narrower: **selection, composition, challenge, escalation and learning across those parents under protected scientific-state constraints**.

## Recursive generalization

For abstraction level `A_k`, a candidate `A_{k+1}` is retained only when it adds material value beyond the strongest lower-level/parent explanation on held-out prediction/transfer/compression without critical information loss. Prospective research-decision gain is a stronger terminal than held-out structural gain.

The recursion continues whenever another material residual survives new-domain, new-epoch and hostile-omission challenges. A bounded `RECURSIVE_STABILITY_CANDIDATE` is permitted only after another abstraction pass fails to find a material residual under those challenges.

`RECURSIVE_STABILITY_CANDIDATE != ULTIMATE_TRUTH`.

## Scientific terminals

Valid outcomes throughout the hierarchy include:

- native/simple sufficiency;
- strongest-parent sufficiency;
- contextual transfer;
- false-analogy rejection;
- conceptual revision or no conceptual residual;
- formalism residual or false-formalism rejection;
- population regularity only;
- prospective meta-policy residual;
- no higher-level residual;
- bounded recursive stability candidate;
- negative result;
- harmful/redundant component;
- merge/drop/contraction;
- `CANNOT_CHECK`.

No layer is required to produce a positive F2 result.

## Implementation surfaces

- `src/orion_v2/knowledge_metabolism.py`
- `src/orion_v2/conceptual_development.py`
- `src/orion_v2/transfer_formal_mechanics.py`
- `src/orion_v2/formalism_genesis.py`
- `src/orion_v2/scientific_development.py`
- `src/orion_v2/recursive_generalization.py`
- `src/orion_v2/development_controller.py`
- `scripts/run_recursive_framework_preflight.py`
- `research/foundation-saturation/ORION_V2_RECURSIVE_DEVELOPMENT_COMPONENT_GRAPH_V1.json`

Outcome-generating computation is intentionally delegated to the frozen E/FM/FG/SD backlogs.
