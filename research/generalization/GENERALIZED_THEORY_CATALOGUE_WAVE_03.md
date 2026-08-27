# Generalized Theory Catalogue — Wave 03

**Status:** adapted cross-domain theories with finite machine semantics. Every entry remains owned substantially by its parent fields and requires target-native validation.

## Catalogue admission rule

An entry requires:

1. at least two materially different native donor domains;
2. independent native reconstructions;
3. explicit registered decisions and actions;
4. a conservative or decision-relative transport;
5. a list of native coordinates deliberately not generalized;
6. a known-answer and hostile suite;
7. a strongest-parent contraction statement.

---

## G03-1 — Decision-Relative Information Order

### Native donors

- Blackwell comparison of statistical experiments;
- Le Cam deficiency and comparison of experiments;
- sufficient statistics and information-preserving compression;
- rough-set indiscernibility;
- active learning and formal query identification;
- causal observational/interventional equivalence.

### Shared problem

When may one information source replace another for a declared family of scientific decisions, and what decision loss results from the substitution?

### Generalized object

```text
DRIO = (
  latent_states,
  signals,
  experiment_kernel,
  registered_decision_problems,
  utility_or_loss,
  resource_budget,
  garbling_or_simulation_witness,
  deficiency_or_value_gap
)
```

### Rules

- `E1 >= E2` when E2 is a validated garbling of E1;
- equivalence on registered tasks is weaker than Blackwell equivalence;
- no registered decision family yields `CANNOT_CHECK`, not equality;
- directional dominance and incomparability are first-class;
- information value must be computed under the target task and resource model.

### Native coordinates retained outside the envelope

- experimental sampling designs;
- clinical or engineering loss functions;
- causal intervention semantics;
- population and prior assumptions;
- observation cost and latency.

### Reference terminals

```text
EQUIVALENT
LEFT_BLACKWELL_DOMINATES
RIGHT_BLACKWELL_DOMINATES
DECISION_EQUIVALENT_ON_REGISTERED_TASKS
INCOMPARABLE_ON_REGISTERED_TASKS
CANNOT_CHECK
```

### Parent contraction

Comparison-of-experiments theory owns the mathematical core. ORION's possible residual is integration with typed scientific obligations, authority, resource constraints and adaptive probe selection.

---

## G03-2 — Contextual Scale-and-Gluing System

### Native donors

- sheaf-theoretic local/global obstruction;
- relational database consistency;
- distributed-state consistency;
- causal abstraction and exact transformations;
- coarse graining, homogenization and model reduction;
- geographical aggregation and scale effects;
- multiresolution measurement.

### Shared problem

Can locally admissible descriptions be combined into one global scientific state, and does a scale change preserve the observations, interventions and decisions registered for the target?

### Generalized objects

```text
ContextualModel = (
  variables,
  value_domains,
  contexts,
  locally_allowed_assignments
)

ScaleMap = (
  micro_states,
  macro_states,
  state_map,
  action_map,
  registered_observables,
  future_observables,
  transition_relation
)
```

### Rules

- local nonemptiness does not imply a global section;
- a global obstruction is different from a locally inconsistent context;
- current-observable preservation is not future-query safety;
- interventional/action transitions must commute with the scale map;
- redundant representations and unresolved alternatives require separate native interpretation.

### Native coordinates retained outside the envelope

- physical length/time scales;
- spatial zoning and aggregation rules;
- causal intervention sets;
- database keys and integrity constraints;
- measurement covers and compatibility rules.

### Reference terminals

```text
GLOBAL_SECTION_EXISTS
GLOBAL_OBSTRUCTION
LOCAL_CONTEXT_EMPTY
EXACT_SCALE_EQUIVALENCE
SAFE_FOR_REGISTERED_TARGETS
SAFE_CURRENT_FUTURE_UNSAFE
INVALID_OBSERVABLE_DRIFT
INVALID_TRANSITION_DRIFT
CANNOT_CHECK
```

### Parent contraction

Sheaf/local-global methods and causal abstraction own core special cases. The ORION residual would be a scientific-state interface tying gluing, scale, evidence, correspondence and reopening to one problem contract.

---

## G03-3 — Dependence-Corrected Evidence Network

### Native donors

- dependent-effect meta-analysis and robust variance estimation;
- survey design effects and intracluster correlation;
- common-cause reliability failures;
- epidemiological interference and clustered experiments;
- ensemble error correlation;
- Byzantine and distributed-validator dependence;
- sociology of diffusion and copied-source lineage.

### Shared problem

How much independent scientific information is present when several evidence items or validators share models, data, instruments, laboratories, retrieval corpora, social influence or ancestry?

### Generalized object

```text
DCEN = (
  evidence_items,
  signed_or_directional_support,
  item_weights,
  dependence_clusters_or_covariance,
  dependence_basis,
  authority_ceilings,
  target_claim
)
```

### Finite quantitative reference

For a disjoint equicorrelated cluster of size `m` and intracluster correlation `rho`, the reference model uses the standard design-effect form:

```text
design_effect = 1 + (m - 1) * rho
effective_count = m / design_effect
```

This is a limited quantitative adapter, not a universal evidence calculus. Overlapping clusters require a richer covariance model and return `CANNOT_CHECK` in the finite implementation.

### Rules

- source count is not effective independent count;
- unknown dependence is not independence;
- contradiction survives dependence adjustment;
- authority ceiling cannot exceed the weakest required evidence class;
- a dependence correction does not grant truth.

### Native coordinates retained outside the envelope

- effect-size estimators and sampling variance;
- laboratory calibration;
- causal interference graphs;
- validator model/data lineage;
- domain-specific evidence quality and authority.

### Reference terminals

```text
INDEPENDENCE_SUPPORTED
DEPENDENCE_ADJUSTED
CONTRADICTORY_EVIDENCE
DEPENDENCE_UNIDENTIFIED
CANNOT_CHECK
```

### Parent contraction

Statistical dependence modelling is parent-owned. ORION's potential residual is claim-relative dependence tracking across evidence, validators, provenance, authority and epochs.

---

## G03-4 — Component-Level Reticulate Inheritance System

### Native donors

- W3C PROV and workflow provenance;
- software bills of materials and build graphs;
- version control and derivation tracking;
- stemmatology and contaminated manuscript transmission;
- phylogenetic networks, hybridization and horizontal transfer;
- data/model fusion and composite scientific artifacts.

### Shared problem

A scientific artifact may inherit its representation, method, evidence, calibration, semantics and evaluator from different parents. Which descendant components are affected when one parent changes or becomes invalid?

### Generalized object

```text
CLRIS = (
  component_nodes,
  artifact_roles,
  inheritance_edges,
  relation_type,
  semantic_transport_receipts,
  authority_ceilings,
  epochs,
  support_routes
)
```

Supported edge types:

```text
COPY
TRANSFORM
CALIBRATE
MERGE
COMPOSE
```

### Rules

- non-copy inheritance requires validated semantic transport;
- component graphs must be acyclic for ordinary derivation;
- child authority cannot exceed the contributing parent ceiling;
- multi-parent inheritance is legal only when every contribution is explicit;
- invalidation propagates through component descendants, not automatically through unrelated artifacts;
- digest/replay identity establishes custody, not scientific correctness.

### Native coordinates retained outside the envelope

- biological inheritance probabilities;
- manuscript scribal mechanisms;
- build-system semantics;
- data licenses and legal lineage;
- scientific meaning and certificate-specific transport rules.

### Reference terminals

```text
EXACT_SINGLE_PARENT
VALIDATED_RETICULATE
INVALID_CYCLE
INVALID_UNVALIDATED_TRANSPORT
INVALID_AUTHORITY_AMPLIFICATION
MISSING_COMPONENT_LINEAGE
CANNOT_CHECK
```

### Parent contraction

General provenance graphs already represent multi-parent derivation. Standalone ORION value requires better selective reopening or invalid-transport detection than the strongest provenance product.

---

## G03-5 — Performative Evaluation Dynamics

### Native donors

- the Lucas critique and structural policy evaluation;
- performative prediction;
- strategic classification and mechanism design;
- organizational incentives and audit gaming;
- Goodhart/specification gaming;
- adaptive benchmark and publication effects.

### Shared problem

Deployment, publication, incentives or policy can change the distribution or system being evaluated. Does the ranking under the pre-deployment world survive the response?

### Generalized object

```text
PED = (
  candidate_policies,
  response_distribution_by_policy,
  policy_outcome_loss,
  static_baseline_distribution,
  performative_risk,
  best_response_operator,
  retraining_dynamics,
  intervention_or_control_identity
)
```

### Rules

- static optimum and performative optimum are distinct objects;
- a policy is performatively stable when it is optimal under the distribution it induces;
- repeated retraining may converge, cycle or remain unresolved;
- proxy improvement with protected harm remains a failure;
- causal attribution requires an intervention, natural experiment or equivalent control;
- changed response mechanisms expire prior evaluation certificates.

### Native coordinates retained outside the envelope

- economic expectations and structural parameters;
- agent utility and strategic constraints;
- institutional enforcement;
- benchmark access and publication timing;
- protected outcome definitions.

### Reference terminals

```text
NO_MATERIAL_RESPONSE
STATIC_AND_PERFORMATIVE_OPTIMA_AGREE
POLICY_WINNER_REVERSAL
RETRAINING_CONVERGES
RETRAINING_CYCLE
CANNOT_CHECK
```

### Parent contraction

Performative prediction and policy evaluation own most dynamics. ORION's candidate residual is the integration with scientific validity, evaluator custody, authority, strategic response and reopening.

---

## G03-6 — Frontier Portfolio and Option System

### Native donors

- R&D and innovation portfolio management;
- exploration/exploitation in organizational learning;
- real-options reasoning;
- quality-diversity and novelty search;
- multiobjective and robust optimization;
- scientific problem finding and opportunity mapping;
- programme and agenda governance.

### Shared problem

Which set of research opportunities should remain active when scientific value is non-scalar, resources are limited, uncertainty is high, and diversity may preserve future options?

### Generalized object

```text
FPOS = (
  opportunities,
  importance,
  information_gain,
  falsifiability,
  tractability,
  option_value,
  diversity_tags,
  cost,
  risk,
  downstream_decisions,
  agenda_authority
)
```

### Rules

- unfalsifiable or decision-free interestingness is inadmissible;
- novelty and diversity are coordinates, not success terminals;
- feasible portfolios satisfy budget and risk bounds;
- non-dominated portfolios remain a Pareto set when no justified total order exists;
- programme adoption requires external agenda authority;
- protected-outcome leakage invalidates prospective opportunity evaluation.

### Native coordinates retained outside the envelope

- domain importance and harm;
- funding and personnel constraints;
- research ethics and legal permission;
- field-specific feasibility and experiment cost;
- institutional agenda authority.

### Reference terminals

```text
PARETO_PORTFOLIO_SET
NO_ADMISSIBLE_OPPORTUNITY
AGENDA_AUTHORITY_REQUIRED
CANNOT_CHECK
```

### Parent contraction

Portfolio optimization and quality-diversity are parent-owned. The possible ORION residual is a scientific opportunity object connecting anomalies, donors, discriminating probes, falsifiers, authority and downstream decision value.

---

## Relations among Wave 02 and Wave 03 families

```text
Decision-Relative Information Order
  -> ranks probes and information channels for declared decisions

Contextual Scale-and-Gluing
  -> determines whether local/scale-specific states can be safely combined

Dependence-Corrected Evidence Network
  -> adjusts assurance for common causes and shared lineage

Component-Level Reticulate Inheritance
  -> determines what changed knowledge affects

Performative Evaluation Dynamics
  -> determines whether deployment invalidates a static evaluation

Frontier Portfolio and Option System
  -> chooses a non-scalar set of research directions

Wave 02 process / diagnosis / correspondence / viability
  -> supplies execution, responsibility, temporal transport and safe reachability
```

No entry is currently admitted as a standalone ORION theorem or paper result.