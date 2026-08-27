# ORION-V2 Framework Skeleton V0

**Status:** research architecture and interface specification only.  
**Gate:** no admitted `src/` implementation before exact V1 handoff issue #2.  
**Purpose:** make the current research compositional and implementation-ready without prematurely freezing V2 atoms or violating the V1 boundary.

## 1. Architecture principle

The framework is a typed scientific control system over obligations and evidence, not a fixed prompt chain.

```text
request or frontier observation
        |
        v
Problem/Opportunity Contract Compiler
        |
        v
Plural Scientific State <----> Structural Relation Service
        |                              |
        |                              v
        |                     Donor/Remote-Neighbour Engine
        v
Admissible Action Generator
        |
        v
Protected Action-Selection Policy
        |
        +--> acquisition / experiment / computation / proof / expert request
        +--> diagnosis / repair / reopen
        +--> witnessed Jump proposal
        |
        v
Execution + Observation Receipts
        |
        v
Interpretation / State Reconstruction
        |
        v
Verification -- Validation -- Authority/Adoption
        |
        v
Typed Terminal / Monitor / Reopen / Episode
```

A fixed V1-like sequence remains one possible policy specialization.

## 2. Immutable identity layer

Every admitted object requires a stable identity type. Candidate primitives:

- `RepositoryRevisionId`
- `ProblemId`
- `RunId`
- `EpochId`
- `SourceId`
- `EvidenceId`
- `ObservationId`
- `ClaimId`
- `ModelId`
- `RepresentationId`
- `ContextId`
- `ObligationId`
- `ActionId`
- `ExecutionReceiptId`
- `VerificationReceiptId`
- `AuthorityGrantId`
- `FrameworkRevisionId`
- `DonorId`
- `ArtifactDigest`

Strings are not proofs. Construction validates format and receipts bind exact bytes/objects.

## 3. Core scientific state

The candidate state should be factored into typed services rather than one maximal record, but the combined logical view is:

`Z = (P, X, O, H, M, Q, A, U, B, R, G, V, kappa)`.

### `P — ContractState`

- immutable problem/frontier identity;
- target decisions and scope;
- success/partial/non-success obligations;
- protected constraints;
- resource/capacity/authority bounds;
- terminal and replay requirements.

### `X — ScientificState`

- source projections;
- candidate/integrated/verified claims;
- observations and instruments;
- representations/charts and mappings;
- plural portraits and obstructions;
- exact dependencies and support families.

### `O — ObligationState`

- open mandatory obligations;
- blockers/defeaters;
- coverage/censoring obligations;
- preservation/revalidation/reopen duties;
- authority and independent-review duties.

### `H — HistoryState`

- append-only action and execution traces;
- failed paths and negative results;
- prior model/representation/framework epochs;
- applicability and expiration contexts;
- post-adoption monitoring events.

### `M — HypothesisPortfolio`

- competing explanations/models/designs/solutions;
- origin grammar/search regime;
- assumptions and predictions;
- posterior/support status where meaningful;
- diversity and option-value coordinates.

### `Q — ProbeExperimentState`

- candidate queries/observations/interventions;
- information family and coverage;
- discriminating power;
- feasibility, instrument, cost and risk;
- observed/censored/exhausted status.

### `A — ActionState`

- currently admissible actions;
- preconditions/effects;
- execution adapter and side-effect class;
- concurrency/commutation/merge status;
- authority and capacity requirements.

### `U — UncertaintyIdentificationState`

- calibrated uncertainty objects;
- live equivalence/indiscernibility classes;
- dependence/common-cause graph;
- identification status and minimum probes;
- approximation/loss bounds.

### `B — ResourceCapacityState`

- computation/time/money/tool/human budgets;
- instrument/expert queues and capacity;
- deadlines/freshness;
- shadow/opportunity costs;
- portfolio allocations.

### `R — ResponsibilityState`

- competing cause/obstacle hypotheses;
- topology: single, serial-upstream, multiple, distributed, interaction-only, shared latent, unresolved;
- separating interventions;
- minimum responsible change level.

### `G — RegimeStack`

- action/method/model grammar;
- representation/abstraction and scale;
- objective/problem specification;
- workflow/control policy;
- framework schema/operator/dependency/provenance/history policy;
- semantic and evaluation epochs.

### `V — ValidationAdoptionState`

- verification/checker results;
- measurement/construct validation;
- robustness/replication;
- reviewer/evidence dependence;
- authority grants/revocations;
- adoption and publication state.

### `kappa — ProtectedConstitutionRef`

Reference to external validation, authority, integrity, safety and leakage controls. Candidate solver code cannot mutate this object.

## 4. Service boundaries

### 4.1 Contract compiler

Input: request or `ResearchOpportunityCandidate`.  
Output: versioned `ProblemContract`, unresolved specification questions, or an honest under-specified/inconsistent/authority-required terminal.

### 4.2 Native evidence and acquisition service

Adapters for literature, databases, formal libraries, computation, sensors, experiments and external experts. Each adapter exposes:

- information/evidence class;
- query/action schema;
- coverage and censoring semantics;
- costs/capacity;
- environment/instrument identity;
- side effects and authority requirements.

### 4.3 Structural relation service

Dispatches to exact or learned parent-faithful relation solvers. Returns `StructuralRelationReceipt`, never an untyped similarity score.

### 4.4 Donor reduction service

Reconstructs donors, checks V1 ownership, verifies conservative embedding, builds strongest donor products and emits non-authorizing reduction receipts.

### 4.5 Hypothesis and action generator

Produces plural candidate models/solutions and admissible actions with origin, grammar, assumptions, expected consequences, costs and falsifiers. Generation is separate from selection and authority.

### 4.6 Action-selection policy

Consumes state and returns an `ActionSelectionReceipt`. Hard gates precede value comparison. Multiple policy classes may coexist:

- deterministic known-answer/native policy;
- exact experiment-design/diagnosis policy;
- POMDP/metareasoning policy;
- robust/minimax/viability policy;
- Pareto/lexicographic portfolio policy;
- learned policy subject to constraints;
- external-human decision.

The policy must preserve incomparability and may return `ASK_EXTERNAL` or `CANNOT_CHECK`.

### 4.7 Execution service

Binds exact occurrence, environment, tool/device/model, inputs, outputs, side effects, resource use, failure and cleanup. It grants no scientific validity.

### 4.8 Interpretation and state-reconstruction service

Creates source projections, candidate interpretations, mappings, dependency updates and affected-closure proposals. It cannot promote verified authority.

### 4.9 Verification/validation service

Separate interfaces for:

- formal/content verification;
- empirical replication and sensitivity;
- measurement/construct validation;
- robustness/generalization;
- dependence-aware reviewer/validator diversity;
- protected evaluation.

### 4.10 Responsibility and recovery service

Maintains plural diagnoses, selects discriminating tests, proposes local repair/compensation/rollback/reopen and computes affected support. It cannot force one cause.

### 4.11 Jump service

Accepts only witnessed triggers. Tests lower levels, searches donors, creates J0–J8 proposals, freezes correspondence/preservation/falsifiers and sends candidates to protected evaluation/adoption.

### 4.12 Memory and meta-solver service

Stores immutable episodes, negative history, lessons and policy revisions. Learned changes remain proposals until fresh transfer and external adoption.

### 4.13 Terminal and publication service

Assembles typed terminals and communication artifacts from scientific state. Publishing cannot promote scientific truth or authority.

## 5. Mandatory invariants

1. **No self-authorization:** proposal, execution, verification and adoption remain separable.
2. **Source preservation:** native evidence is never overwritten by an integrated view.
3. **Censoring is not absence:** unobserved routes remain open/censored.
4. **Plurality preservation:** unresolved alternatives are not collapsed.
5. **Context-relative relation:** every equivalence/abstraction/comparability judgment binds context and epoch.
6. **Minimum responsible change:** lower-level repair wins over higher Jump.
7. **Selective invalidation:** changed support reopens affected descendants while preserving complete independent support.
8. **Negative-history immutability:** harmful/null/failed trajectories remain addressable.
9. **Execution ≠ validity ≠ authority.**
10. **Verification ≠ validation.**
11. **Capacity/resource realism:** nominal actions are inadmissible when tools/expertise/time are unavailable.
12. **Dependence-aware assurance:** nominal vote/source count is not independence.
13. **No scalar laundering:** mandatory gates cannot be compensated by task score.
14. **V1 non-retroactivity:** V2 cannot rewrite frozen V1 evidence or terminals.
15. **Fail closed:** missing evidence, undefined mapping or unverified parent routes yield typed non-success.

## 6. Candidate package map after handoff

The exact package names are provisional.

```text
src/orion_v2/
  identities/
  contracts/
  state/
  obligations/
  relations/
  donors/
  acquisition/
  hypotheses/
  actions/
  policies/
  execution/
  interpretation/
  verification/
  diagnosis/
  recovery/
  jump/
  memory/
  governance/
  terminals/
  publication/
  adapters/
```

The research reference models under `research/reference_models/` do not automatically migrate into `src/`. Each receives parent ownership, API, test and admission review.

## 7. Post-freeze build sequence

### Build B0 — exact handoff and parity corpus

Bind V1 manifest and generate frozen capability cases. No solver code before B0.

### Build B1 — identities, immutable records and schemas

Implement validated IDs, canonical serialization, digests and append-only receipts. Run schema/round-trip/hostile identity tests.

### Build B2 — exact relation and parent-method library

Adopt finite/exact parent methods with native tests: bisimulation, Markov equivalence, rough sets, Blackwell witnesses, viability, diagnosis, workflow checks, gluing and support invalidation.

### Build B3 — contract, state and terminal kernel

Implement ProblemContract, plural state projections, obligation state and typed terminals without learned policies.

### Build B4 — execution and evidence adapters

Bind computation/search/formal-checker adapters first. Physical adapters require separate safety and authority protocols.

### Build B5 — deterministic baseline solver

Implement simple obligation-driven dispatch and prove V1 parity on finite/reference cases. No learned policy yet.

### Build B6 — donor-composed adaptive solver

Integrate strongest parent policies and compare before ORION-specific controllers.

### Build B7 — protected learned policy

Only if exact/donor policies leave a residual. Learned policy cannot bypass schemas, gates or receipts.

### Build B8 — Jump ladder

Implement J0–J8 trigger/proposal/evaluation after lower-level solver and relation services are stable.

### Build B9 — frontier opportunity and meta-solver

Add problem finding and solver revision under external agenda/adoption authority.

### Build B10 — protected scientific campaigns

Run V1 parity, simple controls, hidden worlds, formal science, governed experiments, frontier and shadow open-research studies.

## 8. Admission checklist per module

- exact scientific obligation;
- strongest parent and V1 ownership;
- machine schema/API;
- known-answer cases;
- hostile/failure cases;
- non-authorizing boundaries;
- resource/capacity semantics;
- provenance and replay;
- strongest donor-product comparison;
- protected fresh evaluation if making a performance/scientific claim;
- explicit disposition and owner.

## 9. Current status

```text
RESEARCH_ARCHITECTURE_DEFINED = true
SCHEMAS_AND_REFERENCE_MODELS_PRESENT = true
LOCAL_REFERENCE_TESTS_GREEN = true
V1_HANDOFF_BOUND = false
ADMITTED_V2_CORE_IMPLEMENTATION_STARTED = false
OUTCOME_GENERATING_V2_STUDIES_STARTED = false
```

The final architecture remains subject to all-domain donor reduction, V1 parity and protected evaluation.