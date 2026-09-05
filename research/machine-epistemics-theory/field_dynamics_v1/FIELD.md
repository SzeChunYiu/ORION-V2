# Machine Epistemics as a state-and-dynamics theory

## 1. Definition

**Machine Epistemics studies the governed evolution of machine-usable claims, procedures, representations and actions under incomplete evidence, dependence, revision, resource limits and self-modification.**

The scientific object is a **typed epistemic state plus admissible transitions** whose outputs retain evidence, authority, scope, dependency and resource obligations.

A registered state is

`Ξ = (K, Λ, D, N, A, S, P, H, O, 𝔠, B, X)`.

- `K` — typed hypergraph of claims, procedures, constraints, representations, observations, dialogue objects and self-model records.
- `Λ` — warrant interval / minimal-support map.
- `D` — dependency and provenance relation.
- `N` — nogoods / registered inconsistent assumption sets.
- `A` — authority coordinates. World-truth, speaker, task-contract and external-commit authority are separate.
- `S` — scope: task, population, environment, epoch, conversation and other applicability coordinates.
- `P` — fast navigation/firing/extraction operators, registered configuration, and a separately typed transient runtime (activation, trace and candidates). A transient result is not registered warrant.
- `H` — compatible hypothesis/model family and uncertainty state.
- `O` — organisation: fibres, exports, transport maps, router, learned procedure library, abstractions and caches.
- `𝔠` — external constitution `(Check, Authority, Meter, Commit)` plus content-bound certificates.
- `B` — cumulative resource expenditure, instantaneous resource stocks and remaining budgets, stored as distinct vectors. Only expenditure is coordinatewise nondecreasing.
- `X` — environment/revision envelope, observation history and external state information that is actually registered.

An implementation may use different data structures. A claimed implementation of this theory must provide a refinement map into these semantic coordinates.

Write `π_sem(Ξ)` for the semantic projection that omits audit history, cumulative
cost and transient execution traces. Equality of this projection is weaker than
equality of the complete state. Fast inference preserves registered semantic
coordinates while updating `P.runtime`, the `B` meter and `X` execution history;
it does not leave the complete tuple literally unchanged.

The transition labels denote primary purpose, not disjoint effects. An external
evidence admission uses the E interface and its registered external receipt;
an internal F derivation cannot fabricate that receipt. A G action may request
an E/L/R transition, but each component must satisfy its own invariant. The
finite checker evaluates these contracts on supplied models; it does not enact
world actions or certify completeness of an environment model.

## 2. Fundamental distinctions

The field is invalid if it collapses any of these pairs:

1. truth warrant ≠ score/confidence;
2. truth warrant ≠ risk-bounded actionability;
3. actionability ≠ permission/authority to act;
4. source identity ≠ source independence;
5. repetition/consensus ≠ world-truth warrant;
6. historical replay ≠ present validity;
7. causal observation ≠ intervention ≠ counterfactual identification;
8. reinstatement ≠ relearning under a new evidence identity;
9. same current behaviour ≠ same future-revision behaviour;
10. query retrieval ≠ proof of absence;
11. model registration ≠ proof that the world lies in the model;
12. self-diagnosis ≠ self-adoption authority.

These are scientific typing constraints, not interface preferences.

## 3. Primary observables

For a registered query and revocation state, the theory exposes at least:

- three-valued liveness `LIVE / UNKNOWN / DEAD`;
- `CONTRADICTED` when registered nogoods remove the candidate support;
- activation / navigation fixed point and residual bound;
- enabled operator set;
- extracted reacting subgraph and extraction-completeness status;
- compatible answer/hypothesis set;
- minimal support / provenance alternatives;
- reopening and recheck cone;
- sufficiency/abstraction status;
- persistent-validity kernel under the registered revision envelope;
- epistemically admissible action set;
- authority and scope applicability;
- risk/actionability certificate status;
- self-model diagnosis/proposal status;
- resource consumption and remaining budget;
- typed terminal / CANNOT_CHECK reason.

## 4. Eleven subdisciplines

1. **Static Machine Epistemics** — warrant, provenance, contradiction, authority, scope.
2. **Epistemic Dynamics** — revision, temporal persistence, convergence, drift, reopening.
3. **Epistemic Control** — query/experiment/clarify/abstain/action under cost/risk/viability.
4. **Learning Epistemics** — identifiability, version spaces, certified traces, lifecycle learnability.
5. **Representation Epistemics** — sufficiency, abstraction, compression, multiscale structure, Jumps.
6. **Causal Machine Epistemics** — observation/intervention/counterfactual identification and transport.
7. **Social/Distributed Machine Epistemics** — testimony, dependence, replica/freshness/order, common/distributed knowledge.
8. **Language Epistemics** — meaning candidates, grounding, dialogue commitment, rendering/non-laundering, prefix commitment.
9. **Self/Meta Epistemics** — self-model, diagnosis, proposal, shadow assurance, external adoption.
10. **Resource Epistemics** — memory/time/communication/verifier/information tradeoffs and lower bounds.
11. **Evaluation Epistemics** — parent subtraction, equivalence, protected evidence, reproducibility and authority.

## 5. What the field does not claim

The unified object is useful even if every mathematical primitive is parent-owned. The following remain separate claims: academic-field recognition; architecture novelty; OCM superiority; natural-language competence; real-world reliability; safety of an unregistered environment; novelty of the component mathematics.

A legitimate global terminal is therefore `FORMALISM_USEFUL_NO_ARCHITECTURE_RESIDUAL` or `PARENT_SUFFICIENT`.

## 6. Why a dynamics layer is needed after the gap atlas

The MEG atlas is primarily a theorem-obligation inventory. Batches 1–5 have proved, tightened or parent-owned many individual obligations. A field theory additionally needs one state object, named transition classes, commutation/non-commutation laws, fast/slow coupling, reversible versus irreversible update theory, persistence/viability under exogenous change, explicit control actions, multi-agent/self boundaries, and a frontier not tied to one OCM milestone.

`GENERAL_NOVELTY = NOT_ESTABLISHED`. `FIELD_STATUS = NOT_ESTABLISHED`.
