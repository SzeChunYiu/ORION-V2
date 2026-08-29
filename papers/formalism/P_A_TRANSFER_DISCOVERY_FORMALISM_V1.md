# P-A Formal Methods Insert V1 — Structural Transfer Discovery

**Intended placement:** P-A Methods after `Structural signatures`; equations are candidate mechanics pending protected execution.

Represent an eligible donor or target as a source-bound typed relational structure

\[
\mathcal S=(V,\mathcal R,\tau,\mathcal I,\mathcal X,\mathcal K),
\]

with entities `V`, relations/hyperedges `R`, type map `tau`, registered invariants `I`, counterexamples/obstructions `X` and provenance/authority constraints `K`. The representation is optional: a native domain that cannot be faithfully projected remains with its native parent method.

A candidate donor mapping is a partial typed homomorphism

\[
\phi=(\phi_V,\phi_R):\mathcal S_D\rightharpoonup\mathcal S_T.
\]

For a mapped relation `r(v1,...,vk)`, P-A requires

\[
\phi_R(r)(\phi_V(v_1),\ldots,\phi_V(v_k))\in \mathcal R_T,
\]

plus preserved type, direction and registered invariant constraints. The failure profile is

\[
\mathbf e(\phi)=(e_{type},e_{rel},e_{inv},e_{counter},e_{authority}).
\]

Any registered critical violation rejects the analogy regardless of semantic similarity.

Abstractions are not drawn from a fixed cross-domain lesson table. Symbolic cases use the strongest applicable anti-unification/least-general-generalization parent. More general candidate abstractions can be ranked by

\[
A^*\in\arg\min_A [L(A)+\sum_i L(\mathcal S_i\mid A)],
\]

subject to source identity, native recovery and counterexample retention. This MDL expression is a search criterion, not proof that the abstraction is scientifically valid.

P-A reports the non-compensatory profile

\[
V=(R_{remote},1-F_{analogy},F_{native},Q_{hidden},R_{old},-C_{resource}),
\]

rather than one similarity score. The new Transfer Discovery mechanism earns an independent residual only if it improves hidden target decisions or remote-donor recovery beyond semantic retrieval, fixed lesson injection, structure mapping, applicable anti-unification/MDL parents and the strongest parent federation without worsening critical false analogy or native fidelity.

### Formal falsifiers

- a structurally high-scoring mapping with a hidden critical obstruction is a false analogy;
- a fixed lesson or strongest parent reproducing the same protected decisions at lower cost implies `PARENT_SUFFICIENT` or `FIXED_LESSON_SUFFICIENT`;
- an induced abstraction that does not improve future held-out retrieval has no discovery residual;
- surface-permutation sensitivity without relation preservation rejects the claimed structural mechanism.
