# Scientific Warrant Factorization
## A Contingent Formal and Empirical Paper on the Weakest Necessary Link in Machine-Mediated Science

**P-G prospectus V0 — not admitted to the primary portfolio**  
**Candidate archetype:** formal/empirical AI reliability or computational-science Article  
**Status:** distinct research hypothesis under hostile parent review. P-G becomes a paper only if it produces a nontrivial formal result or protected cross-domain decision gain that cannot be carried cleanly by P-D or the flagship.

## 1. Motivation

A machine-mediated scientific claim can depend on a chain of qualitatively different warrants:

1. the source or observation is the one claimed;
2. its semantic interpretation is appropriate;
3. the scientific model represents the target adequately;
4. the mathematical problem and numerical/software implementation are valid enough;
5. the test, oracle or evaluator can expose the relevant error;
6. the evidence routes have the declared dependence structure;
7. the argument actually connects the evidence to the bounded claim;
8. the result transports to the target context;
9. the proposed action has legitimate authority.

These links are handled by mature fields. They are nevertheless often collapsed into one confidence score or passed through a pipeline in which one successful layer silently authenticates another. Reproducible computation is treated as scientific correctness; provenance as truth; benchmark success as deployment validity; confidence as permission.

P-G asks whether there is a formal and empirically useful theory of **warrant factorization** across heterogeneous scientific layers.

## 2. Candidate object

For a proposed transition `τ`, define a directed typed warrant structure:

`W(τ) = (N, E, T, A, U, D, C)`

where:

- `N` are warrant nodes;
- `E` are support, dependence, attack, transport and authority edges;
- `T` assigns a native warrant type;
- `A` assigns assumptions, scope and expiry;
- `U` assigns uncertainty/approximation semantics;
- `D` states the registered scientific decision;
- `C` states the context and criterion identity.

Candidate native node types include:

- source/observation identity;
- semantic interpretation;
- scientific model adequacy;
- mathematical/numerical/software validity;
- test/oracle sensitivity;
- evidence dependence/robustness;
- argument/premise validity;
- transport/comparability;
- authority/custody.

A sufficient warrant family is a typed subgraph that supports the transition under native parent rules.

## 3. Candidate propositions

These are conjectures, not laws.

### G1 — Necessary-link scope ceiling

If a transition requires warrant nodes `n_1, ..., n_k`, its justified scope cannot exceed the intersection of their valid scopes without an additional warrant.

Informally:

`scope(τ) <= meet_i scope(n_i)`.

This is not necessarily a numerical minimum. Scope can be a partial order over claim classes, contexts, populations, approximations or authorities.

### G2 — Non-amplification by composition

Composing warrant links cannot strengthen relation precision, independence, evidence authority or error-detection capacity unless a new independent warrant explicitly supplies the strengthening.

Examples:

- approximate transport does not become exact through a longer chain;
- dependent evidence does not become independent through agent count;
- a partial oracle does not become complete through repeated use;
- restricted authority does not become general permission through local computation.

### G3 — Heterogeneous invalidation locality

When one warrant node or edge fails, only transitions whose every sufficient family includes the invalid element must reopen. Alternative valid families survive.

### G4 — Cross-type authentication prohibition

A warrant of type `t_i` cannot establish a claim requiring native type `t_j` solely because both are represented by the same scalar confidence or proof-like artifact.

A cryptographic signature can establish identity, not scientific truth. A formal proof can establish a theorem relative to a specification, not empirical model adequacy. A calibrated prediction does not establish intervention authority.

### G5 — Decision-relative minimality

A warrant representation is sufficient only relative to the registered decision. Removing a node is valid when all protected decisions and counter-probes are preserved; generic compression is not enough.

## 4. Strongest parent threats

P-G faces unusually strong parents:

- safety/assurance cases and claim–argument–evidence models;
- formal/defeasible argumentation;
- Bayesian networks and probabilistic graphical models;
- Dempster–Shafer and imprecise-probability evidence systems;
- provenance and workflow lineage;
- proof-carrying code and refinement;
- weakest-link reliability and fault-tree analysis;
- causal transportability and measurement traceability;
- truth-maintenance/support hypergraphs;
- evidence-to-decision frameworks;
- type systems and information-flow security.

P-G is not admitted if it merely redraws these parents with scientific labels.

## 5. Distinct residual test

A standalone residual requires at least one of:

1. a formal theorem applying across two or more native warrant families that is not already a direct parent theorem;
2. a non-composition or impossibility result showing why a common assurance federation is unsound;
3. a decision procedure that detects a protected scientific error missed by the strongest F0 assurance product;
4. a minimal cross-domain witness calculus that preserves parent-native verdicts and reduces assurance burden;
5. a new benchmark demonstrating systematic cross-type authentication failures.

If the value is only explanatory organization, keep the proposition in the flagship. If it is only evidence assurance, merge into P-D.

## 6. Candidate formal programme

### 6.1 Typed semilattice or category of scopes

Investigate whether selected warrant scopes admit:

- partial order and meet operations;
- typed morphisms for transport;
- monotonicity/non-amplification results;
- explicit non-composable pairs;
- approximation and authority modalities.

Do not force all native relations into one algebra if their semantics do not support it.

### 6.2 Hypergraph support semantics

Represent alternative sufficient warrant families as hyperedges. Prove conditions for selective invalidation and minimal witness extraction.

### 6.3 Countermodels

Construct cases where:

- every node has high local confidence but the cross-type transition is invalid;
- a stronger-looking aggregate has weaker support because of dependence;
- an exact computational certificate supports the wrong scientific model;
- a valid scientific claim lacks authority;
- two valid parent proofs cannot be composed because their contexts differ.

### 6.4 Parent recovery

For each formal sublanguage, recover native parent verdicts on known-answer suites. A unified theorem cannot override a parent counterexample.

## 7. Candidate empirical programme

### Case family G-C1 — provenance-perfect semantic error

The exact artifact and process are authenticated, but the source passage or scientific interpretation is wrong.

### G-C2 — numerically validated wrong model

Validated computation proves a bound for an encoded model whose target-world adequacy is false.

### G-C3 — partial oracle overreach

A test checks a necessary property but not the fault class implied by the scientific claim.

### G-C4 — dependent assurance inflation

Several evidence routes and reviewers share a hidden source or assumption.

### G-C5 — transport and authority split

A result is scientifically transportable, but data/action authority does not transport.

### G-C6 — alternative warrant survives

One support family fails while an independent family remains valid.

### G-C7 — simple native parent suffices

A negative control in which the factorized structure adds cost but no decision value.

### Arms

- untyped confidence aggregation;
- provenance-only;
- native assurance/argumentation parent;
- fault-tree/reliability parent where applicable;
- strongest F0 assurance federation;
- P-D integrated assurance;
- P-G factorized calculus;
- SIMPLE direct control.

## 8. Primary outcomes

- cross-type authentication error;
- false scientific completion;
- native-verdict preservation;
- selective-reopening correctness;
- witness minimality and review burden;
- calibration under dependence;
- authority violation;
- formal proof/countermodel coverage;
- resource-adjusted decision quality.

Hard failures cannot be averaged away.

## 9. Candidate figures

1. typed warrant graph and alternative sufficient families;
2. cross-type authentication failures;
3. formal non-amplification/selective invalidation results;
4. F0/P-D/P-G protected quality–cost comparison.

## 10. Expert cell

1. assurance/safety-case theorist;
2. formal argumentation/logics researcher;
3. formal methods/type-systems researcher;
4. statistics/causal/measurement methodologist;
5. numerical and scientific-software reviewer;
6. evidence/governance scholar;
7. hostile “this is a relabelled assurance case” reviewer;
8. cross-domain scientific adjudicators.

## 11. Admission and kill rules

### Admit P-G only when

- a nontrivial theorem, impossibility or algorithm is independently checked;
- native parent recovery passes;
- F0 and P-D are fully specified competitors;
- at least one cross-domain protected decision improves;
- the paper has one result-scale thesis independent from the flagship;
- resource and review burden are reported.

### Kill or merge when

- assurance cases/argumentation already own the formal result;
- the weakest-link statement remains only a metaphor;
- scalar confidence is replaced by a graph but decisions do not change;
- P-D carries the empirical contribution more cleanly;
- formal unification erases native semantics;
- costs create redundant drag.

## 12. Current terminal

```text
P_G_STATUS = CONTINGENT_NOT_ADMITTED
CENTRAL_IDEA = SCIENTIFIC_WARRANT_FACTORIZATION
FORMAL_THEOREM = OPEN
PARENT_RECOVERY = OPEN
PROTECTED_CROSS_DOMAIN_RESIDUAL = OPEN
DISTINCTNESS_FROM_P_D_AND_FLAGSHIP = CANNOT_CHECK
NEW_PAPER_IDENTITY_GRANTED = NO
TOP_TIER_SUBMISSION_READY = NO
```
