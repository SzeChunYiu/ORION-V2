# Conceptual Development and Transfer Discovery — Formal Mechanics V1

**Role:** candidate mathematical mechanics for ORION-V2 conceptual development and transfer discovery.  
**Scientific status:** formal interface and testable hypotheses; not a theorem that all science has one representation.  
**Parent rule:** use the strongest applicable native formalism first. The constructions below are a federation of parent mechanisms, not a claim that graph maps, lattices, categories or MDL universally subsume scientific concepts.

## 1. Typed scientific structure

Represent a source-bound donor or target, when this representation is adequate, as a typed relational structure

\[
\mathcal S=(V,\,\mathcal R,\,\tau,\,\mathcal I,\,\mathcal X,\,\mathcal K),
\]

where `V` is a set of entities/objects, `R` typed relations or hyperedges, `tau` type information, `I` registered invariants, `X` counterexamples/obstructions and `K` authority/provenance constraints. This is a comparison interface, not a universal ontology. A domain may supply another native structure and expose only a projection into this interface.

## 2. Candidate transfer as a partial typed homomorphism

A candidate donor-to-target transfer is a partial map

\[
\phi=(\phi_V,\phi_R):\mathcal S_D\rightharpoonup \mathcal S_T.
\]

For every mapped donor relation

\[
r(v_1,\ldots,v_k),
\]

relation preservation requires

\[
\phi_R(r)(\phi_V(v_1),\ldots,\phi_V(v_k))\in\mathcal R_T,
\]

whenever all mapped arguments are defined. Type, direction and arity must also be preserved unless the proposal explicitly binds a lawful type-changing bridge.

The mapping carries a non-compensatory violation vector

\[
\mathbf e(\phi)=
(e_{type},e_{rel},e_{inv},e_{counter},e_{measurement},e_{authority}).
\]

A critical non-zero component cannot be purchased by high average similarity. This is the formal version of `FALSE_ANALOGY_REJECTED`.

## 3. Invariance and equivariance

For a registered scientific judgment `J` and admissible transformation `g`, an invariance claim is

\[
J(g\cdot x)=J(x).
\]

When the output itself has a lawful transformation `rho(g)`, use equivariance:

\[
J(g\cdot x)=\rho(g)J(x).
\]

The transformation family must be domain-owned. Renaming identifiers, changing units, changing coordinates, permuting source order or changing representation are not automatically invariances; each is a hypothesis with a native witness or protected test.

This gives a direct benchmark: generate transformations that should preserve a decision, transformations that should change it, and misleading surface transformations. Measure invariance recall jointly with false invariance.

## 4. Abstraction induction rather than fixed lessons

For symbolic structures, anti-unification / least-general generalization is an explicit parent mechanism. If donor descriptions are terms `s_1,...,s_n`, an abstraction candidate may be

\[
A=\operatorname{lgg}(s_1,\ldots,s_n),
\]

when the applicable anti-unification theory supplies a least general generalization.

For more general structured cases, use an MDL-style candidate objective

\[
A^*\in\arg\min_A\left[L(A)+\sum_{i=1}^{n}L(\mathcal S_i\mid A)\right],
\]

subject to native-recovery, source-identity and counterexample constraints. Compression is a candidate discovery heuristic, not scientific truth: a compact abstraction that loses a critical native distinction fails.

The essential comparison is therefore

`FIXED_LESSON_INJECTION` vs `PARENT_GENERALIZATION` vs `F2_TRANSFER_DISCOVERY`.

If a fixed lesson or mature anti-unification/MDL parent matches the protected result at lower cost, the ORION mechanism contracts.

## 5. Formal Concept Analysis as one concept-formation parent

For a formal context

\[
K=(G,M,I),
\]

with objects `G`, attributes `M` and incidence `I`, define

\[
A'=\{m\in M:\forall g\in A,(g,m)\in I\},
\qquad
B'=\{g\in G:\forall m\in B,(g,m)\in I\}.
\]

A formal concept satisfies

\[
A'=B,\qquad B'=A.
\]

The resulting concept lattice supplies an exact baseline for extension/intension and hierarchical concept change. ORION's `ConceptState` is richer because it also carries relations, scope, counterexamples, operational links and authority. FCA is therefore a strongest parent in cases that reduce to formal contexts, not a universal definition of concept.

## 6. Functorial transfer when categorical structure is legitimate

When native scientific/mathematical objects and transformations form categories, a candidate transfer may be tested as a functor

\[
F:\mathcal C_D\rightarrow\mathcal C_T.
\]

The exact obligations are

\[
F(\mathrm{id}_x)=\mathrm{id}_{F(x)},
\qquad
F(g\circ f)=F(g)\circ F(f).
\]

A claimed equivalence additionally requires the appropriate inverse/equivalence witnesses rather than superficial similarity. Commuting-diagram tests become exact counterexamples to transfer.

Category theory is only activated when the native objects genuinely support the required categorical semantics. Failure to form a valid category is not a failure of the scientific domain.

## 7. Obstruction-first negative transfer

Let `C(phi)` be the registered set of required constraints for a proposed transfer. Define the obstruction set

\[
\Omega(\phi)=\{c\in C(\phi):c\text{ is violated in the target}\}.
\]

If any critical obstruction exists,

\[
\Omega_{critical}(\phi)\neq\varnothing
\Rightarrow
\mathrm{REJECT}(\phi).
\]

Counterexample search is therefore not an optional afterthought. In mathematical/formal cases, use proof assistants, SMT/SAT, finite-model search or exhaustive enumeration where appropriate. In empirical sciences, the analogous object is a prospectively frozen discriminating observation or experiment.

## 8. Conceptual development as a versioned transition

Write a concept state as

\[
C_t=(\Sigma_t,R_t,S_t,O_t,I_t,E_t,X_t,P_t,K_t),
\]

where `Sigma` is the symbol/primitive set, `R` relations, `S` scope, `O` operational links, `I` invariants, `E` exemplars, `X` counterexamples/anomalies, `P` parent concepts and `K` authority/provenance constraints.

A conceptual-development proposal is

\[
\tau:C_t\rightarrow C_{t+1},
\]

with typed operator `SPECIALIZE`, `GENERALIZE`, `SPLIT`, `MERGE`, `BRIDGE`, `REPARAMETERIZE`, `REVISE` or `DEPRECATE`.

Two gates are mandatory.

### Predecessor retention

For old-valid hidden cases `H_old`,

\[
R_{old}(\tau)=\frac{1}{|H_{old}|}\sum_{h\in H_{old}}
\mathbf 1[J_{C_{t+1}}(h)=J_{C_t}(h)].
\]

A promoted conceptual transition requires registered retention, normally exact on critical old cases.

### Scientific residual

A new concept receives no credit from vocabulary change alone. It must have either a prospectively tested decision/prediction residual

\[
\Delta Q_{hidden}=Q(C_{t+1})-Q(C_t),
\]

or a checked formal necessity/impossibility result. Otherwise the terminal is `NO_SCIENTIFIC_RESIDUAL`.

## 9. Transfer-discovery search policy

Transfer discovery is a search over candidate donors, abstractions, mappings and challenges:

\[
\mathcal H=\{(D,A,\phi,\Omega,\hat y)\}.
\]

Search may use semantic retrieval, relational matching, anti-unification, formal-concept closure, graph/hypergraph search, theorem search, learned representations or other parents. No one search method is privileged.

When a probabilistic decision model is justified, an action `a` such as retrieving another donor, proving an invariant or seeking a counterexample can be ranked by expected reduction in registered decision loss minus cost:

\[
\mathrm{EVI}(a)=
\mathbb E[L(d\mid S)-L(d\mid S,X_a)]-\lambda\,\mathrm{cost}(a).
\]

When such probabilities are not warranted, use robust/Pareto parent policies instead of fabricating a probability.

## 10. Non-compensatory transfer value

Do not compress transfer quality to a universal scalar. Report

\[
V(\phi)=
(Q_{hidden},R_{remote},1-F_{analogy},F_{native},R_{old},G_{formal},-C_{resource}),
\]

where the coordinates are hidden-target quality, remote-donor recovery, false-analogy avoidance, native fidelity, old-valid-case retention, formal witness status and resource cost.

A candidate dominates another only when it is no worse on every registered critical coordinate and strictly better on at least one, subject to hard authority/measurement/integrity gates.

## 11. Regime selection

The adverse E20 pilot motivates a separate hypothesis: a full controller need not be universally active. Let

\[
\pi(z)\in\{\mathrm{SIMPLE},F0,F1,F2,\mathrm{ABSTAIN}\}
\]

be a selector using only pre-outcome episode features `z`. The selector is scientifically useful only if it improves the protected quality-resource frontier on held-out tasks relative to always-SIMPLE, always-F0 and always-F2. Post-outcome routing is not admissible evidence.

## 12. Exact computation programme

### FM10 — finite relational mapping
Generate small typed relational structures with hidden partial homomorphisms, isomorphisms, non-isomorphisms and surface-similar decoys. Exhaustive search supplies an exact oracle. Measure mapping recovery and false transfer.

### FM20 — anti-unification/generalization
Generate symbolic term families with a hidden least-general pattern plus distractor regularities. Compare fixed lessons, syntactic anti-unification, learned abstraction and F2 discovery.

### FM30 — concept closure and revision
Generate formal contexts, concept lattices and held-out counterexamples. Require the system to identify whether the correct development is specialization, split, merge, bridge or no change while preserving old-valid concepts.

### FM40 — invariance/equivariance
Generate group/permutation actions with hidden invariant and non-invariant quantities. Require discovery of the transformation family and test on unseen transformations.

### FM50 — functoriality and diagram tests
Generate small finite categories and candidate object/morphism mappings. Hidden commuting diagrams and identity/composition checks provide exact pass/fail witnesses.

### FM60 — obstruction/counterexample discovery
Provide plausible mappings or conjectures containing one hidden obstruction. Score whether the system finds a proof/countermodel before making a transfer claim.

### FM70 — contextual regime selection
Using frozen pre-outcome features from existing ORION benchmark families, compare always-SIMPLE/F0/F2 with a prospectively trained selector. Do not train on confirmatory outcomes that are later reused for testing.

### FM80 — naturalistic mathematics ↔ science
Prospectively test discovered mathematical structure on at least two empirical sciences and test scientific cases that motivate a new formal abstraction. Mathematical claims require formal witnesses; empirical claims require independent scientific adjudication.

## 13. Paper consequences

- **P-A:** mapping discovery, remote donor retrieval, anti-unification/MDL parent comparisons and false-analogy obstruction become explicit formal components.
- **P-B:** typed partial homomorphism, invariance/equivariance, categorical composition when applicable, and obstruction/countermodels provide the formal backbone of relation transport.
- **P-C:** regime selector `pi(z)` and value-of-information search provide testable mechanics for contextual activation and exploration.
- **Flagship:** conceptual development becomes a fourth transformation alongside knowledge-state, scientific-state and self-model change, but only earns field-level status if its formal/empirical residual survives strongest parents.

## 14. Parent anchors

- Gentner (1983), structure mapping: relational rather than attribute-centered analogy and systematicity.
- Cerna & Kutsia (2023), anti-unification/generalization: computational generalization as a mature parent family.
- Ganter & Wille (2024, 2nd ed.), Formal Concept Analysis: concept lattices, closure and contextual concept logic.
- Grünwald (2000), MDL model selection: compression-based induction/model selection.
- Mac Lane, *Categories for the Working Mathematician*: functors, natural transformations and universal constructions.
- Cousot & Cousot (1977): abstraction with sound relation to a concrete semantics.

These parents are comparators and sources of formal machinery. ORION receives scientific credit only for a protected residual beyond their strongest applicable combination.
