# Recursive Scientific Development — Formalism V1

**Status:** candidate formalization for population-scale scientific-development meta-learning. Not a universal law of discovery.

## 1. Episode space

Let a scientific-development episode be a finite trajectory

\[
e_i=(s_{i,0},a_{i,0},x_{i,0},\ldots,s_{i,T_i}),
\]

with state coordinates drawn from the existing Machine Epistemics episode interface: problem/frame, knowledge, concept/formalism, evidence, methods, resources, actors, failures, evaluators and authority.

Let `Y(e_i)` be a typed outcome vector rather than one impact label.

## 2. Development operators

At abstraction level 1, infer candidate operators

\[
o_j:s\mapsto s'
\]

from recurring state transitions. An operator is characterized by

\[
o_j=(P_j,\Delta_j,F_j,C_j),
\]

where `P` is a precondition region, `Delta` a state transformation, `F` known failure/boundary conditions and `C` resource cost.

The operator vocabulary is open-world. Named historical operators may seed retrieval but do not constrain induction.

## 3. Higher levels

Let `A_k` be the set of accepted abstractions at level `k`. A recursive generalizer proposes

\[
A_{k+1}=G_k(A_k;D),
\]

where `D` is the source-bound episode corpus.

A level-`k+1` object must reconstruct the relevant lower-level decisions and add at least one material residual on held-out data:

\[
\Delta_k = Q_{heldout}(A_{k+1})-Q_{heldout}(A_k),
\]

or a reduction in complexity/resource burden without loss of registered critical distinctions.

No level is promoted solely because it compresses terminology.

## 4. Multi-objective admissibility

For a candidate `H`, report

\[
V(H)=(-L_{pred},-L_{recon},-L_{transfer},-L_{intervention},-C_{critical},-C_{complexity},-C_{resource}).
\]

`L_pred` is held-out trajectory prediction loss; `L_recon` lower-level reconstruction loss; `L_transfer` held-out field/epoch transfer loss; `L_intervention` prospective intervention loss when such evidence exists. Historical observational corpora cannot fill `L_intervention` by assumption.

A critical validity or authority failure is non-compensatory.

## 5. Contrastive explanation

For a candidate principle `h`, estimate not only

\[
P(Y^+\mid h),
\]

but its discrimination over matched/stratified success and failure trajectories:

\[
\Delta_h = P(Y^+\mid h,Z)-P(Y^+\mid \neg h,Z),
\]

where `Z` contains observed context such as field, epoch, problem maturity, team/resource state and knowledge availability. This is an observational estimand unless identification assumptions justify stronger interpretation.

## 6. Recursive-stability candidate

Let `G` denote another registered abstraction pass. A bounded recursive-stability candidate `A*` approximately satisfies

\[
A^* \simeq G(A^*)
\]

in the following operational sense:

1. no material higher-level residual appears on registered held-out domains/epochs;
2. hostile omission searches do not expose a missing operator family;
3. lower-level valid judgments remain recoverable;
4. another abstraction pass does not improve protected prospective decisions or resource cost materially;
5. explicit reopen conditions remain.

This is not metaphysical finality. A new source mode, scientific practice, machine substrate, domain or counterexample can reopen the candidate.

## 7. Population data and causal boundary

Bibliometric, citation, team and career data estimate regularities of the observed scientific system. They also encode publication, prestige, institutional, language and reward mechanisms. Therefore:

\[
P(\text{high impact}\mid h) \neq P(\text{scientifically valid breakthrough}\mid do(h)).
\]

A meta-principle becomes an intervention claim only after prospective or otherwise identified evidence tests whether applying it changes a protected scientific-development outcome.

## 8. Relationship to V2

The recursive layer consumes lower-level receipts rather than replacing them:

\[
\text{episodes}
\to \text{operators}
\to \text{operator families}
\to \text{meta-policies}
\to \text{higher principles}
\to \cdots
\]

while Scientific-State Transition remains the external warrant boundary.
