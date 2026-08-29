# Scientific Relations Are Context-Relative
## Typed Transport, Obstruction and Selective Reopening Across Heterogeneous Representations

## Abstract

Scientific representations can be “the same” in fundamentally different senses: observationally indistinguishable yet interventionally different, decision-equivalent yet information-different, comparable under one measurement standard but not another, or exactly related for one query while unsafe for future use. We study whether a common typed interface can coordinate these relations without replacing their native mathematics. The representation binds a relation family to a declared context, direction, witnesses, preserved decisions, approximation or measurement loss, counter-probes, epoch and revalidation consequences. We give bounded propositions for context refinement, exact decision-preserving composition and selective reopening under explicit support-family semantics; these propositions are supporting semantics rather than a new universal calculus. The empirical/formal benchmark compares the interface with the strongest parent-specific relation methods and parent compositions on cross-family known-answer and hostile cases. Standalone value is earned only if the shared interface changes valid reuse or reopening decisions while preserving native judgments. Parent sufficiency, administrative interoperability and formal contraction are legitimate outcomes.

## 1. Introduction

“Are these two things equivalent?” is not a complete scientific question.

Two causal models can match every observed distribution yet imply different interventions. Two statistical representations can support the same current decision while retaining different information. Two measurements can be traceable to standards but incomparable for the intended use. Two programs can be behaviorally equivalent at one interface and different at another. An abstraction can preserve today's query while deleting a distinction needed by a future query.

These examples are not exceptions to one master notion of similarity. They are different scientific relations, each defined by a context, a set of judgments and a native parent theory. Treating them as values on a generic similarity scale can therefore license invalid scientific reuse. A machine may turn “close in embedding space” into “transportable,” “predictively equivalent” into “causally interchangeable,” or “traceable” into “fit for this measurement decision.” The representation can be internally consistent while the scientific reuse is wrong.

Mature disciplines already supply much of the necessary mathematics. Causal inference distinguishes observational, interventional and transport relations. Statistical decision theory distinguishes information from decision sufficiency. Metrology and psychometrics study traceability, comparability and measurement invariance. Formal methods study bisimulation, contextual equivalence, abstraction, refinement and safe quotienting. Markov aggregation, rough sets, category theory and local-to-global methods provide further relation families and composition principles under their own assumptions.

The present paper therefore does not propose one new equivalence relation. It asks a coordination question:

> **Can a shared typed interface select and compose heterogeneous scientific relations while preserving parent-native judgments, exposing losses and obstructions, and improving downstream reuse or reopening decisions beyond the strongest parent composition?**

The null is strong. If a scientific system can simply call the correct parent method at each step and make the same protected decisions at equal or lower cost, then a common relation interface is infrastructure rather than a new scientific contribution.

## 2. A context-relative relation object

Let a scientific context be

\[
C=(Q,I,D,B,K,T,\epsilon),
\]

where \(Q\) denotes registered queries or predictions, \(I\) interventions or transformations, \(D\) decisions or actions, \(B\) resource constraints, \(K\) authority/governance constraints, \(T\) target and epoch or anchor, and \(\epsilon\) the registered approximation or error semantics.

A relation receipt is

\[
R=(S_1,S_2,\mathcal F,C,W,L,X,E,A),
\]

where \(S_1,S_2\) are native scientific objects, \(\mathcal F\) identifies the parent relation family, \(W\) contains witnesses, \(L\) records loss/deficiency/approximation terms, \(X\) counter-probes or obstructions, \(E\) epoch/expiry/revalidation state and \(A\) provenance/authority boundary.

The receipt does not create a relation. It states which parent theory supplies the relation and under which conditions the relation is being used.

This distinction is important in machine-mediated science because “similarity” often arrives before its semantics. A generic representation can propose a possible relation, but scientific reuse requires the relation family and the decision context to be explicit.

## 3. Relation families remain plural

The evaluation treats at least the following as distinct parent families rather than numerical settings of one method:

- exact equality or isomorphism;
- behavioral or bisimulation-style equivalence;
- interface/contextual equivalence;
- observational or predictive equivalence;
- decision comparison or sufficiency;
- rough indiscernibility;
- abstraction, safe quotient or lumpability;
- measurement invariance and comparability;
- causal transportability;
- viability or reachability equivalence;
- local compatibility and global obstruction;
- explicitly approximate relations with an error or deficiency term;
- incomparability.

A relation system may select among these parents or report that the requested relation cannot be established. Disagreement among parents is not itself evidence for inventing a new relation.

## 4. Typed mapping, invariance and obstruction

When source and target admit relational representations, a candidate structural mapping can be written

\[
\phi=(\phi_V,\phi_R):\mathcal S_S\rightharpoonup\mathcal S_T.
\]

We track a violation vector

\[
\mathbf e(\phi)=
(e_{type},e_{rel},e_{direction},e_{inv},e_{approx},e_{measurement},e_{scope},e_{authority}).
\]

Registered critical violations are non-compensatory. A high semantic or structural match cannot turn a direction reversal, invalid measurement relation, failed invariant or unauthorized use into exact transport.

For transformations \(g\) that should preserve a registered decision \(J\), an exact invariance test has the form

\[
J(gx)=J(x),
\]

or, where the output transforms lawfully,

\[
J(gx)=\rho(g)J(x).
\]

Categorical or commuting-diagram tests are used only where the native objects genuinely support that structure. Formal commutation can show that a formal mapping preserves what it claims to preserve; it cannot establish an empirical transport assumption by itself.

Define an obstruction set

\[
\Omega(\phi)=\{c\in C(\phi):c\text{ fails in the target}\}.
\]

A critical obstruction blocks the corresponding exact reuse disposition.

## 5. Bounded propositions

The following propositions clarify the interface semantics. They are elementary consequences of explicit definitions or parent theories and are not presented as new general mathematics.

### Proposition 1 — context refinement

Let \(x\sim_C y\) mean that \(x\) and \(y\) agree on every registered judgment in context \(C\). If context \(C_2\) contains every obligation in \(C_1\) with identical semantics for shared obligations, then

\[
x\sim_{C_2}y\Rightarrow x\sim_{C_1}y.
\]

**Proof.** Agreement on every judgment in the larger context implies agreement on each judgment in its subset. ∎

The converse need not hold. A relation sufficient for a current task can become insufficient after the context is enriched.

### Proposition 2 — exact registered-decision-preserving composition

Let \(f:S_1\to S_2\) and \(g:S_2\to S_3\). Suppose

\[
J_2(f(x))=J_1(x)
\]

for every relevant \(x\), and

\[
J_3(g(y))=J_2(y)
\]

for every relevant \(y\). Then

\[
J_3(g(f(x)))=J_1(x).
\]

**Proof.** Substitute \(y=f(x)\) into the second equality and use the first. ∎

This result is deliberately narrow. It says nothing about causal, measurement, semantic or authority validity not encoded in the registered decision. Approximate relations require the relevant parent's error-composition rule.

### Proposition 3 — selective reopening under sufficient-support-family semantics

Let a claim \(q\) have complete sufficient support families

\[
\mathcal H_q=\{H_1,\ldots,H_m\}.
\]

After an event invalidates a set of supports \(I\), \(q\) must reopen exactly when every complete sufficient family has lost at least one required member:

\[
\operatorname{Reopen}(q,I)=1
\quad\Longleftrightarrow\quad
\forall H_j\in\mathcal H_q,
\;H_j\cap I\neq\varnothing.
\]

**Proof.** If some complete sufficient support family remains disjoint from \(I\), that family remains valid and suffices for \(q\); reopening is not required. If every complete sufficient family intersects \(I\), no complete valid support family remains, so the claim must be reopened under the stated semantics. ∎

### Proposition 4 — monotone invalidation under fixed support semantics

If \(I_1\subseteq I_2\) and a claim reopens under \(I_1\), then it also reopens under \(I_2\), provided the sufficient-support-family semantics themselves have not changed.

**Proof.** Every support family that intersects \(I_1\) also intersects its superset \(I_2\). ∎

This proposition does not cover the appearance of new independent support, a change in what counts as sufficient support, or a changed authority/measurement epoch. Those events create a new support state rather than a simple superset invalidation.

## 6. Benchmark design

The study combines known-answer and hostile cases across relation families. Each case contains native objects, the relevant parent relation or known-answer oracle, a registered downstream reuse or reopening decision, and at least one adversarial condition capable of exposing overgeneralization.

Case families include examples where:

- observational equivalence does not imply intervention equivalence;
- current decision equivalence hides information needed by a later decision;
- exact formal equivalence fails under an enriched interface;
- measurement comparability depends on the declared target and epoch;
- approximate transport is safe only below a registered tolerance;
- relation composition accumulates or changes a parent-defined error;
- a locally plausible mapping has a global obstruction;
- invalidated support should reopen some but not all dependent commitments.

The primary independent unit is the registered relation/reuse case. Multiple checks inside one case are dependent components rather than independent samples.

## 7. Comparator conditions

The interface is compared against:

- direct use of the correct native parent method;
- parent-specific workflow compositions;
- generic similarity/retrieval where relevant;
- a strongest federation that routes each case to the applicable parent without the proposed shared relation object.

The strongest federation is the decisive control. A common representation earns scientific value only if it changes a protected decision or reduces a scientifically relevant error/cost beyond that parent composition.

## 8. Evaluation

The primary outcomes are:

- preservation of parent-native relation judgments;
- unsafe reuse or false-exact transport;
- missed valid reuse;
- correct approximate/incomparable/unresolved handling;
- selective reopening correctness;
- incremental protected decision value beyond strongest parent routing;
- resource and interface cost.

These quantities are reported separately. A generic interoperability gain cannot compensate for a critical native relation error.

## 9. Results

**Authoring placeholder — blocks arXiv release until receipt-bound Results are inserted.**

The final Results section will use this fixed evidence order:

1. **Native relation fidelity.** Establish whether the shared interface preserves the judgments of the relevant parent theories.
2. **Cross-family reuse.** Measure false-exact, missed-valid, approximate and incomparable dispositions.
3. **Selective reopening.** Evaluate whether invalidation changes exactly the commitments whose sufficient support was lost.
4. **Strongest-parent comparison.** Test whether the common interface changes any protected decision beyond direct parent routing/composition.
5. **Obstruction and hostile cases.** Keep failure boundaries visible in the main paper.
6. **Resource/interface cost.** Determine whether any protected benefit is dominated by a simpler parent pipeline.

No positive conclusion is selected before these results exist.

## 10. Interpretation branches

### Cross-parent coordination residual

Used only if the interface preserves native judgments and changes protected reuse/reopening decisions beyond the strongest parent composition.

### Parent routing sufficient

If direct parent routing/composition makes the same decisions at equal or lower cost, the result is that a common typed representation provides interoperability but no independent scientific residual.

### Interface introduces error

If abstraction into the shared interface loses a critical native distinction, the unified representation is rejected or narrowed to the relation families for which it is safe.

### Split result

If one subset of relation families yields a real cross-parent residual and another does not, the manuscript contracts rather than forcing one universal framework.

## 11. Discussion

Scientific equivalence is not a single property. It is a statement about which distinctions can be ignored for a declared purpose. The practical danger in AI-mediated science is not merely choosing the wrong similarity metric; it is silently moving from one relation family to another while preserving the word *same*.

A positive result would support a typed coordination layer that makes relation family, context, loss and revalidation consequences explicit while leaving the mathematics with the relevant parent. Its value would be measured by downstream scientific decisions, not by schema completeness.

A parent-sufficiency result would imply that strong routing among mature theories is enough. That outcome would favor a plural architecture rather than a new relation layer. Likewise, if the interface systematically erases native distinctions, the correct scientific response is to reduce its scope.

The bounded propositions clarify why current equivalence need not survive context refinement and why selective reopening depends on complete support families. They do not establish the empirical value of one interface. That value must come from the held-out benchmark and hostile cases.

## 12. Limitations

The common representation is only as sound as the parent relation chosen for each case. Some relation families may resist projection into a shared typed object without losing semantics. Empirical transport cannot be established by a formal diagram alone. Authority and governance conditions are externally supplied and can change independently of mathematical relation validity.

The support-family reopening semantics assume a known set of complete sufficient supports; incomplete provenance or hidden dependence can invalidate that model. Naturalistic scientific settings may also contain evolving claims and measurement standards that require explicit epoch versioning.

Finally, a successful interface does not imply one ontology of scientific sameness. Its strongest defensible role is coordination among relations that remain plural.

## 13. Conclusion

Scientific reuse depends on the relation being asserted, the context in which it is used and the decision it is expected to preserve. This study tests whether making those objects explicit can improve reuse and selective reopening across heterogeneous parent theories without replacing their native semantics.

The decisive comparison is not against generic similarity. It is against the strongest federation of the mature parent methods themselves. If that federation already makes the same decisions, use it. If the shared interface changes protected decisions while preserving native judgments, the result supports a bounded coordination layer. If it erases critical differences, contract it.

That evidence—not the elegance of a common schema—determines whether context-relative scientific relations support an independent computational-science contribution.

## Reproducibility and release note

The final public version will bind every formal statement to its proof and every benchmark result to a versioned case registry, native oracle, analysis receipt and source-data object. Internal project-development identifiers remain outside manuscript-facing prose.
