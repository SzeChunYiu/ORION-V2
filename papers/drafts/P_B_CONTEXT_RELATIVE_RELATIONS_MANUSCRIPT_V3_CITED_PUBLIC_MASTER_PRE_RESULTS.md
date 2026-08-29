# Scientific Relations Are Context-Relative
## Typed Transport, Obstruction and Selective Reopening Across Heterogeneous Scientific Representations

## Abstract

Scientific representations can be “the same” in fundamentally different senses: observationally indistinguishable yet interventionally different, decision-equivalent yet information-different, comparable under one measurement standard but not another, or safe for one query while unsafe for future reuse. Mature disciplines already formalize many of these relations. We therefore do not seek a universal equivalence relation. Instead, we test whether a common typed interface can coordinate native relation families without replacing their mathematics. The interface binds each relation to a declared context, direction, witnesses, preserved decisions, approximation or measurement loss, counter-probes and revalidation consequences. We prove four bounded propositions—context refinement, exact registered-decision-preserving composition, selective reopening under sufficient-support-family semantics and monotone invalidation under the same semantics—and treat them as parent-style consequences rather than new general mathematics. The protected benchmark compares the interface with strongest parent-specific relation methods and their composition on cross-family known-answer and hostile cases. Standalone value is earned only if the shared interface changes valid reuse or reopening decisions while preserving native judgments. Parent sufficiency, administrative interoperability and formal contraction are prespecified outcomes.

## 1. Introduction

“Are these two things equivalent?” is not a complete scientific question.

Causal models can agree observationally yet disagree under intervention. Statistical experiments can support the same current decision while retaining different information. Measurements can be traceable yet unsuitable for a particular comparison. Programs can be behaviourally equivalent under one interface and distinct under another. Abstractions can preserve today's query while losing information needed tomorrow.

These distinctions are already mature science. Causal transportability is context- and intervention-dependent [@bareinboim2016transport]. Blackwell comparison treats informativeness as decision-relative [@blackwell1953equivalent]. Measurement invariance and metrology formalize when measurements can be compared under declared assumptions [@meredith1993measurement; @jcgm2012vim]. Formal methods distinguish behavioural equivalence, abstraction and refinement [@milner1989communication; @cousot1977abstract], and finite-state theory studies safe aggregation and lumpability [@kemeny1976finite]. Rough sets make indiscernibility explicitly attribute-relative [@pawlak1991rough]. Recent work also emphasizes that identical predictor behaviour does not identify arbitrary internal representation properties [@sevetlidis2026fiber] and that minimal recursively updateable quotients are model-class specific [@zhang2026minimal].

The problem for machine-mediated science is therefore not a shortage of relation theories. It is **coordination among them**. A generic similarity surface can silently promote one relation family into another: semantic similarity into scientific transport, predictive equivalence into causal equivalence, shared provenance into redundancy, or exact equality into approximate comparability.

We ask:

> **Can a shared typed relation interface coordinate heterogeneous scientific notions of sameness, comparability and transport while preserving parent-native judgments—and does that coordination change scientific reuse or reopening decisions beyond the strongest parent composition?**

The null is strong. If careful routing among mature parents already makes the same decisions, the shared interface is useful engineering but not an independent scientific contribution.

## 2. Relation object

Let a scientific context be

\[
C=(Q,I,D,B,K,T,\epsilon),
\]

where `Q` denotes registered queries or predictions, `I` interventions or transformations, `D` decisions, `B` budgets/resources, `K` authority constraints, `T` target/epoch and `epsilon` tolerance/error semantics.

A relation receipt is

\[
R=(S_1,S_2,\mathcal F,C,W,L,X,E,A),
\]

where `S1,S2` are native scientific objects, `F` the parent relation family, `W` witnesses, `L` loss or deficiency terms, `X` counter-probes/obstructions, `E` epoch/expiry state and `A` provenance/authority boundary.

The receipt does not create validity. It records **which parent relation is being invoked and under what conditions it may be used**.

Candidate families include exact isomorphism, behavioural or contextual equivalence, observational equivalence, decision comparison, rough indiscernibility, safe abstraction/lumpability, measurement comparability, causal transportability, approximate relations with explicit error and incomparability.

## 3. Typed mapping and obstruction

When a relation is represented through an explicit partial mapping,

\[
\phi=(\phi_V,\phi_R):\mathcal S_S\rightharpoonup\mathcal S_T,
\]

we record a violation vector

\[
\mathbf e(\phi)=
(e_{type},e_{rel},e_{direction},e_{inv},e_{approx},e_{measurement},e_{scope},e_{authority}).
\]

A critical violation blocks the corresponding transport disposition even when a generic similarity score is high.

For a registered decision `J`, a transformation may preserve the decision exactly,

\[
J(gx)=J(x),
\]

or obey an explicitly registered equivariance relation. Exact composition of such decision-preserving mappings is straightforward; it does not imply causal or measurement validity that was never assumed.

## 4. Bounded propositions

These results are included because they make the interface auditable. They are elementary or parent-style and are not presented as a new universal calculus.

### Proposition 1 — context refinement

Let `~_C` mean agreement on every registered judgment in context `C`. If `C_2` refines `C_1` by adding obligations while preserving the semantics of shared obligations, then

\[
x\sim_{C_2}y\Rightarrow x\sim_{C_1}y.
\]

The converse need not hold. A relation safe for a smaller context can fail in a richer one. This is the basic reason a present abstraction may require revalidation after the query/intervention set changes.

### Proposition 2 — exact registered-decision-preserving composition

Let

\[
f:S_1\to S_2,\qquad g:S_2\to S_3
\]

and suppose

\[
J_2(f(x))=J_1(x),
\qquad
J_3(g(y))=J_2(y).
\]

Then

\[
J_3(g(f(x)))=J_1(x).
\]

This is an exact decision-level composition result. It says nothing about unregistered causal, semantic, measurement or authority properties. Approximate relations require the relevant parent error-composition theorem; errors do not disappear because a receipt is typed.

### Proposition 3 — selective reopening under sufficient-support-family semantics

Let a claim `q` have explicitly registered sufficient support families

\[
\mathcal F_q=\{F_1,\ldots,F_m\},
\]

where each `F_i` is a set of currently valid support items sufficient under the registered inference contract. If a support item is invalidated, `q` must reopen **iff every sufficient family has lost at least one required member**.

This is a declared support semantics, not a universal theory of belief. It captures why a source retraction should not globally reopen a claim when an independently sufficient support route survives.

### Proposition 4 — monotone invalidation under fixed support semantics

If the set of valid support items only shrinks while `F_q` is held fixed, then once every sufficient family has been broken, removing additional support cannot restore the claim. Restoration requires a new support item, a changed support family or changed semantics—not merely further invalidation.

## 5. Benchmark

The protected benchmark contains cross-parent cases in which the correct decision depends on relation type, context or direction. Examples include:

- observational versus interventional equivalence;
- decision-equivalent but information-distinct states;
- measurement comparability under one calibration and failure under another;
- abstraction safe for one query set and unsafe for a richer one;
- exact versus approximate transport;
- relation composition with a hidden obstruction;
- selective reopening after a source, evaluator or mapping failure.

Cases include known-answer and hostile variants. Solver arms do not receive the gold parent label when that label is part of the test.

### 5.1 Comparator conditions

Comparators include:

- strongest native parent method per case;
- a simple generic similarity/embedding baseline;
- parent routing without a common typed interface;
- strongest explicit parent federation;
- the candidate typed coordination interface.

The shared interface can earn standalone scientific credit only if it changes a protected reuse/reopening decision beyond the strongest parent composition **without changing native parent judgments**.

## 6. Outcomes

Primary outcomes are case-level:

1. correct parent/relation-family selection;
2. correct direction/context binding;
3. native known-answer preservation;
4. invalid composition/obstruction detection;
5. correct scientific reuse/transport disposition;
6. correct selective reopening;
7. false transport/false reopening;
8. resource cost.

A generic “interface accuracy” score is secondary. Critical scientific errors remain non-compensatory.

## 7. Results

**[RESULTS BLOCK — populate only from frozen P-B receipts.]**

Results must distinguish:

- performance of native parents;
- performance of parent routing/federation;
- incremental value of the shared interface;
- formal proposition checks;
- invalid-composition and reopening cases;
- resource costs.

Allowed paper-level terminals:

- `CROSS_PARENT_RELATION_RESIDUAL`;
- `FORMAL_INTERFACE_ONLY`;
- `PARENT_ORCHESTRATION_RESOURCE`;
- `PARENT_SUFFICIENT`;
- `FORMAL_CLAIM_CONTRACTED`;
- `CANNOT_CHECK`.

If no protected cross-parent decision residual exists, theorem correctness alone does not justify a top-tier systems/science Article.

## 8. Interpretation

A positive result would support a bounded coordination claim: a typed common interface can reduce invalid cross-parent reuse or reopening while preserving each parent's native semantics. It would **not** establish a universal relation of scientific sameness.

If parent routing/federation matches the interface, the correct result is parent sufficiency. The shared schema may still be valuable infrastructure, but that is an engineering/resource contribution rather than evidence for new relation theory.

If the formal propositions hold but the empirical interface adds no decision value, the paper contracts to a formal/interface resource or merges into the broader programme.

## 9. Limitations

The result is only as strong as the registered contexts and parent implementations. Parent methods can be misconfigured, and the typed interface can create false confidence if its loss/obstruction fields are treated as complete. Empirical transport assumptions remain empirical even when the mapping itself is formally well typed. Selective reopening depends on the declared support-family semantics and is not a universal belief-revision law.

Most importantly, some sciences may resist a shared interface because their native relation concepts carry domain-specific meaning that should not be compressed. Such failures support pluralism, not a more elaborate universal schema.

## 10. Conclusion

Scientific “sameness” is inherently context-relative. Causal inference, decision theory, measurement science and formal methods already provide powerful but different answers to different relation questions [@bareinboim2016transport; @blackwell1953equivalent; @meredith1993measurement; @cousot1977abstract]. The open question is whether a shared typed interface adds scientific control **between** those parents.

This study is designed to let the parents win. If careful native routing already yields the same protected reuse and reopening decisions, it should be preferred. If an incremental residual survives, it is a result about coordination across relation families—not a replacement for their mathematics.

## Transparency

Large language model tools contributed materially to literature discovery, formalization, critique, software and drafting. AI systems are not authors. Human authors must inspect the proofs, parent sources, protected results and final manuscript and take responsibility for all released claims.

## Bibliography source

Use `papers/primary/PRIMARY_PAPERS_REFERENCES_V1.bib`. Refresh all 2026 source statuses before arXiv and journal release.
