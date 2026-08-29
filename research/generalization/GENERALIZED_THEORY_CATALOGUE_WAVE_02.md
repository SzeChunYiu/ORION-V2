# Generalized Theory Catalogue — Wave 02

**Status:** adapted/generalized research theories with finite reference semantics. Every theory remains subject to parent reduction and target-native validation.

## Catalogue rule

A generalized theory is admitted to this catalogue only when:

1. at least two materially different native domains motivate it;
2. each native theory is reconstructed independently;
3. an explicit transport preserves registered native decisions and behavior;
4. assumptions, costs, authority, context, and epoch are not erased;
5. hostile cases distinguish valid transport from superficial analogy;
6. the strongest native parent remains the default implementation unless a protected residual survives.

The catalogue is not a claim that ORION owns the underlying theories.

---

## G02-1 — Generalized Obligation Process Network

### Native donors

- workflow nets and process soundness;
- stage-gate and project governance;
- systems-engineering verification, validation, and change control;
- legal and administrative procedure;
- laboratory and scientific workflow systems;
- reliability recovery and compensation paths.

### Shared problem

Given a set of obligations, resources, evidence, authority constraints, and possible reopenings, determine whether an admissible process can reach a declared terminal and whether every reachable nonterminal state retains a completion path.

### Generalized object

```text
OPN = (
  obligations,
  marking,
  tasks,
  requirements,
  productions,
  reopenings,
  resources,
  evidence,
  authority,
  terminal_obligations
)
```

A task may fire only when prerequisites, evidence, authority, and resources are available. It produces obligations, may reopen earlier obligations, consumes resources, and leaves an immutable task occurrence.

### Candidate soundness conditions

- terminal obligations are reachable;
- every reachable state can still reach a valid completion;
- no required task is dead;
- no unapproved authority transition is enabled;
- resources never become negative;
- a completion contains no hidden unresolved hard obligation;
- compensation and reopening do not delete adverse history.

### Industry-specific details not generalized away

- manufacturing capacity units;
- regulatory signatory roles;
- legal deadlines and appeal rights;
- laboratory instrument constraints;
- domain-specific verification and validation predicates.

These remain adapter parameters or native judgments.

### Reference terminals

```text
SOUND
DEADLOCK
COMPLETION_NOT_REACHABLE_FROM_ALL_STATES
REQUIRED_TASK_DEAD
CANNOT_CHECK
```

### ORION use

This is a candidate owner for workflow control, decomposition interfaces, selective reopening, execution planning, and bounded stopping. It does not justify one universal fixed workflow.

### Parent contraction

Generic process soundness is parent-owned. The only possible ORION residual is the integration of scientific obligations, evidence, authority, provenance, and reopening.

---

## G02-2 — Plural Responsibility Diagnosis System

### Native donors

- Reiter-style model-based diagnosis;
- multiple-fault reliability diagnosis;
- FMEA and fault-tree analysis;
- differential diagnosis in medicine;
- causal responsibility and incident analysis;
- distributed control and common-cause failure analysis.

### Shared problem

Given observations and a set of competing causal hypotheses, retain all minimal explanations consistent with the evidence and choose probes that discriminate them. Do not force a single cause when the failure is distributed or interaction-only.

### Generalized object

```text
PRDS = (
  observations,
  responsibility_hypotheses,
  cause_sets,
  topology,
  predicted_observations,
  diagnostic_probes,
  probe_costs,
  preference_or_minimality_order
)
```

Supported topologies include:

```text
SINGLE
SERIAL_UPSTREAM
MULTIPLE_INDEPENDENT
DISTRIBUTED
INTERACTION_ONLY
UNRESOLVED
```

### Candidate rules

- inconsistent hypotheses are removed;
- explanations are minimized only under a declared preference order;
- an interaction-only explanation cannot be replaced by either member alone;
- multiple surviving explanations yield non-identifiability unless a probe separates them;
- diagnosis does not grant blame, authority, or repair permission.

### Industry-specific details not generalized away

- medical disease ontologies and intervention risks;
- engineering component failure rates;
- organizational accountability rules;
- legal standards of responsibility;
- causal-model assumptions.

### Reference terminals

```text
IDENTIFIED
MULTIPLE_DISCRIMINABLE
STRUCTURALLY_NONIDENTIFIABLE
CONTRADICTION
CANNOT_CHECK
```

### ORION use

This pressures V1-style single or earliest-stage attribution. A future solver should carry a responsibility topology and probe plan rather than one root label.

### Parent contraction

Diagnosis and set-cover probe design are parent-owned. The possible residual is evidence-, authority-, and workflow-aware scientific diagnosis.

---

## G02-3 — Calibrated Correspondence Chain

### Native donors

- metrological traceability and calibration chains;
- psychometric equating and measurement invariance;
- political ideal-point scale linking;
- causal transportability;
- ontology and schema evolution;
- diachronic semantic alignment;
- ORION V1 certificate lifting and regime transport.

### Shared problem

Determine whether an object, score, meaning, judgment, certificate, or scientific commitment remains comparable across changed representations or epochs.

### Generalized object

```text
CCC = (
  source_epoch,
  target_epoch,
  mappings,
  anchors,
  preserved_invariants,
  violated_invariants,
  unresolved_invariants,
  context,
  uncertainty_bound,
  semantic_loss,
  exactness
)
```

Multiple links compose only when epochs are contiguous. Uncertainty accumulates conservatively. Preserved invariants across a chain are the intersection of link-level invariants; violations and unresolved obligations accumulate by union.

### Candidate rules

- identifiers without mappings and anchors are insufficient;
- a required violated invariant produces non-comparability;
- unresolved invariants produce `CANNOT_CHECK`;
- semantic loss or excessive uncertainty produces partial comparability;
- exactness requires exact links and zero accumulated uncertainty;
- context change may expire a previously valid chain.

### Industry-specific details not generalized away

- SI unit realizations and calibration procedures;
- psychometric item parameters and population assumptions;
- political anchor legislators or common items;
- causal selection diagrams;
- linguistic corpus and sense-alignment assumptions.

### Reference terminals

```text
EXACT
COMPARABLE_WITHIN_TOLERANCE
PARTIALLY_COMPARABLE
NONCOMPARABLE
CANNOT_CHECK
```

### ORION use

This may become the quantitative core of cross-generation epistemic comparability. It should remain separate from mere provenance: lineage shows where an object came from; correspondence shows whether it still means the same thing for a target decision.

### Parent contraction

Each linking mechanism is parent-owned. A standalone ORION result requires an integrated cross-domain interface and incremental decision value.

---

## G02-4 — Justified Viability System

### Native donors

- viability theory and controlled invariance;
- robust and stochastic control;
- ecological safe operating spaces;
- learning and knowledge spaces;
- operations and project feasibility;
- safety engineering;
- scientific reachability under evidence and authority constraints.

### Shared problem

From which states can an agent remain inside hard scientific constraints, and from which states can it reach a declared target without leaving that safe region?

### Generalized object

```text
JVS = (
  states,
  actions,
  nondeterministic_transitions,
  admissible_actions,
  safe_states,
  target_states,
  mode
)
```

Two modes are distinguished:

- `EXISTENTIAL`: at least one successor remains in the candidate set;
- `ROBUST`: every possible successor remains in the candidate set.

### Candidate rules

- unsafe high-reward shortcuts do not enter justified reachability;
- robust and existential kernels must not be conflated;
- target capture is computed inside the viability kernel;
- unavailable actions, missing transition semantics, and unbound safety predicates yield `CANNOT_CHECK` at a higher protocol layer;
- a viable state need not be target-reachable, and a target-reachable state need not be robustly viable.

### Industry-specific details not generalized away

- physical safety margins;
- ecosystem constraints;
- educational prerequisite semantics;
- operational capacity and deadlines;
- scientific authority and evidence admissibility.

### ORION use

This gives a parent-grounded interpretation of justified reachability and frontier planning. It can constrain the action policy before expected value is considered.

### Parent contraction

Viability and capture kernels are parent-owned. The possible residual is their combination with typed scientific obligations, evidence, provenance, and authority.

---

## 5. Relations among the four families

The theories compose, but they are not interchangeable.

```text
Obligation process network
  -> defines admissible procedural transitions

Plural responsibility diagnosis
  -> explains why an obligation or transition failed

Calibrated correspondence chain
  -> determines whether states and commitments survive a regime change

Justified viability system
  -> determines which future paths remain admissible and target-reaching
```

A solver may therefore move through the loop:

```text
process residual
-> plural diagnosis
-> minimum discriminating probe
-> repair or regime transition
-> correspondence and reopening
-> recomputed viability and action set
```

This loop is a candidate solver architecture, not a theorem that every problem requires every component.

## 6. Current dispositions

| Generalized theory | Parent ownership | ORION residual | Current disposition |
|---|---|---|---|
| Obligation Process Network | very high | scientific obligations, evidence, authority, reopening | conservative candidate |
| Plural Responsibility Diagnosis | very high | scientific-state and authority integration | conservative candidate |
| Calibrated Correspondence Chain | distributed across several fields | common cross-generation interface | high-priority candidate |
| Justified Viability System | very high | epistemic/authority constrained reachability | conservative candidate |

No catalogue entry currently carries novelty or adoption authority.
