# Discovering Remote Scientific Structure Without Losing Native Meaning
## Structural Donor Discovery, Reduction and Conservative Transfer

## Abstract

Scientific problem solving often reuses structure from remote domains, yet retrieval systems are usually optimized for topical or semantic proximity. We study a stricter problem: whether a machine can identify a structurally relevant donor when surface vocabulary differs, reconstruct that donor in native terms, project only decision-relevant structure, expose losses and counterexamples, and correctly conclude when an apparent novelty is already explained by a known parent. Existing analogy, literature-discovery and transfer systems already address important parts of this problem. We therefore test a narrower residual: **remote donor discovery coupled to donor-native recovery, explicit negative-transfer challenge, target-verdict preservation and parent/novelty contraction**. The study compares the integrated procedure with lexical/citation search, semantic retrieval, literature-based discovery, structure-mapping and modern LLM analogy systems, applicable formal parents, expert search and their strongest information-matched composition. Hidden donor identities and target consequences are withheld from solver arms. Results are evaluated at the case level using donor recovery, native fidelity, false analogy, target decision accuracy, novelty contraction and resource cost. Positive, parent-sufficient, recall–fidelity trade-off and `CANNOT_CHECK` outcomes are all prespecified.

## 1. Introduction

Scientific advances frequently reuse an idea developed elsewhere: an invariant, decomposition, representation, optimization principle, mathematical object, experimental design or failure mode. The useful donor can be remote in vocabulary, citation graph and disciplinary taxonomy. A query about the target topic may therefore miss a source whose scientific role is relevant while its terminology is not.

Remote analogy is not itself a new problem. Structure-mapping theory distinguishes relational correspondence from surface feature matching [@gentner1983structure]. Literature-based discovery explicitly searches for latent connections across disjoint literatures [@swanson1986undiscovered]. Symbolic generalization, Formal Concept Analysis and minimum-description approaches provide mature abstraction machinery [@plotkin1970generalization; @ganter1999fca; @rissanen1989stochastic]. More recently, LLM-based systems have used cross-domain analogy for scientific solution generation [@shen2026analogical], benchmarked inspiration retrieval and hypothesis construction [@liu2026researchbench], introduced mechanism-aware analogical research [@chen2026adr] and tested transfer robustness under structure-preserving transformations [@li2026retre].

These advances make a weak claim—“LLMs can find useful analogies”—uninteresting. The scientific difficulty is the **disposition after retrieval**. A remote source can be structurally evocative but scientifically invalid for the target. It can preserve a high-level relation while violating a native invariant. It can suggest an attractive explanation while hiding a donor assumption. Or it can reveal that what appeared novel in the target is already a known consequence of a mature parent.

We therefore ask:

> **Can a machine discover a remote scientific donor and use it conservatively without replacing native scientific meaning with generic similarity?**

The integrated hypothesis separates five tasks that are often collapsed:

1. candidate discovery;
2. donor-native reconstruction;
3. bounded structural reduction;
4. explicit challenge through counter-probes and obstructions;
5. scientific disposition: reuse, contextual transfer, false analogy, parent sufficiency, novelty contraction or `CANNOT_CHECK`.

The strongest null is deliberately competitive: current retrieval, analogy and formal-parent systems may already perform these functions when combined carefully. If so, the integrated method has no scientific residual.

## 2. Problem formulation

Let a target scientific problem be

\[
T=(P_T,J_T,C_T,E_T),
\]

where `P_T` is its native representation, `J_T` a registered target decision or prediction, `C_T` context and `E_T` its source/evidence state.

A candidate donor `D` is eligible only if its source can be bound and its native scientific objects reconstructed. When relational projection is appropriate, donor and target may be represented as typed structures

\[
\mathcal S=(V,\mathcal R,\tau,\mathcal I,\mathcal X,\mathcal K),
\]

where `V` are native objects, `R` relations, `tau` types, `I` invariants/constraints, `X` counterexamples or obstructions and `K` provenance/authority conditions.

A candidate partial mapping

\[
\phi=(\phi_V,\phi_R):\mathcal S_D\rightharpoonup\mathcal S_T
\]

is evaluated with a non-compensatory violation profile

\[
\mathbf e(\phi)=
(e_{type},e_{rel},e_{direction},e_{inv},e_{counter},e_{scope},e_{authority}).
\]

A critical violation blocks transfer even when a similarity score is high.

### 2.1 Donor-native recovery

A donor is considered recovered only if the reconstructed representation reproduces a preregistered set of donor-native known-answer judgments, including negative or boundary cases. Define

\[
F_{native}=
\frac{1}{|K_D|}\sum_{k\in K_D}
\mathbf 1[\hat J_D(k)=J_D(k)],
\]

with critical known-answer failures scored separately and non-compensatorily.

This condition prevents an analogy system from receiving scientific credit for a useful-sounding paraphrase that changes the donor's own judgments.

### 2.2 Remote structure

“Remote” is not equivalent to lexical distance. Each benchmark case records lexical/topic, citation-graph, disciplinary-taxonomy and embedding distance separately from structural relevance and target-decision relevance. A remote donor is deliberately weak on conventional proximity signals while independently adjudicated as relevant to a frozen target consequence.

### 2.3 Conservative transfer

The output of a transfer arm is not the sentence “the domains are analogous.” It must expose:

- donor identity and source;
- donor-native judgment;
- relation type and direction;
- mapped and unmapped structure;
- preserved target decision;
- losses and assumptions;
- counter-probes;
- scope/expiry conditions;
- final scientific disposition.

## 3. Benchmark design

The evaluation contains mathematical/formal and empirical/computational cases, including within-domain and cross-domain transfer. Each case contains a target problem, one or more eligible donors, semantically near distractors, structurally tempting but invalid donors, donor-native known-answer checks, a hidden target consequence and one or more counter-probes.

Gold donor identities and hidden target consequences are unavailable to solver arms. Case construction records whether donors are remote by vocabulary, citation graph, discipline or embedding geometry, avoiding a single arbitrary distance definition.

### 3.1 Leakage and surface controls

Cases include post-freeze renaming where semantics permit, same-words/different-structure controls, different-words/same-registered-structure controls, citation-neighbour distractors, hidden assumptions and invalid donor composition. Any leakage diagnostic discovered after outcome access can only qualify or invalidate a result; it cannot promote one.

### 3.2 Scientific unit

The independent evaluation unit is the **case**, not the retrieved document, model sample or reasoning trace. Repeated samples within one case measure within-case stochasticity and cannot inflate the scientific sample size.

## 4. Comparator arms

The comparison includes:

- target-only/direct reasoning;
- lexical/citation search;
- embedding/semantic retrieval;
- literature-based discovery;
- structure-mapping/analogy parents;
- modern LLM scientific analogy and inspiration-retrieval systems [@shen2026analogical; @liu2026researchbench; @chen2026adr];
- applicable native formal parents such as anti-unification or FCA [@plotkin1970generalization; @ganter1999fca];
- frozen human-authored transferable lessons;
- expert-local or expert-federated search where feasible;
- the strongest information-matched parent federation.

ReTRE provides an important transfer-robustness boundary: strong performance on a base task does not imply robustness to structure-preserving variants [@li2026retre]. The integrated method must therefore earn value through scientific fidelity, not merely through a higher retrieval hit rate.

## 5. Outcomes and inference

Primary outcomes are reported separately.

### 5.1 Remote donor recovery

Whether at least one eligible hidden donor is recovered within the frozen source/resource budget.

### 5.2 Native fidelity

Whether the recovered donor passes its native known-answer set, especially critical negative/boundary cases.

### 5.3 False analogy

Whether an ineligible or scientifically invalid donor is promoted to a target transfer that changes the registered target disposition.

### 5.4 Target decision preservation

Whether the transfer preserves or correctly changes the frozen target decision.

### 5.5 Novelty contraction

Whether the system correctly recognizes that an apparent target novelty is already explained by an eligible donor or parent.

### 5.6 Resource-adjusted performance

Search calls, model/tool calls, expert time and other registered costs are reported rather than hidden behind accuracy.

The main analysis is case-level and paired where the same cases are evaluated by several methods. Heterogeneity is preserved across task families rather than reduced to a single grand mean. No non-significant difference is interpreted as equivalence without a preregistered margin.

## 6. Results

**[RESULTS BLOCK — populate only from frozen P-A receipts.]**

The public Results section must appear in this order:

1. donor recovery relative to strongest parents;
2. native scientific fidelity;
3. false-analogy and critical-failure rate;
4. target-decision accuracy and novelty contraction;
5. resource-adjusted performance;
6. heterogeneity and boundary cases.

Allowed paper-level terminals are:

- `PROTECTED_TRANSFER_RESIDUAL`;
- `CONTEXTUAL_TRANSFER_ONLY`;
- `PARENT_SUFFICIENT`;
- `FIXED_LESSON_SUFFICIENT`;
- `REMOTE_RECALL_GAIN_FALSE_ANALOGY_TOO_HIGH`;
- `NO_SCIENTIFIC_RESIDUAL`;
- `CANNOT_CHECK`.

No result sentence may be written before the corresponding receipt exists.

## 7. Interpretation branches

If the integrated method improves donor recovery while preserving native judgments and false-analogy control, the supported claim is a bounded benefit of coupling discovery to reconstruction and challenge. It is not evidence for a universal transfer calculus.

If recall improves but false analogy or native-verdict loss rises materially, the result is a **recall–fidelity trade-off**, not a positive transfer result.

If the strongest parent federation matches the integrated method, the appropriate conclusion is **parent sufficiency**. The benchmark and negative result can still be useful because they delimit what a special transfer layer does not add.

If fixed lessons match adaptive discovery, adaptive donor search is unnecessary at the tested scope.

## 8. Limitations

The benchmark can only test the registered donor universe and target decisions. Expert adjudication may itself be fallible or dependent on benchmark construction. Remote structure is multi-dimensional and no single distance measure is authoritative. A source recovered from the literature is not scientifically valid merely because it passes the benchmark's relation contract. The method also does not establish that a discovered donor will produce novel empirical science outside the registered tasks.

Most importantly, cross-domain transfer can be domain-specific. Failure to compress a donor into the shared representation is not evidence that the donor is unusable; it may indicate that a native parent representation should be retained.

## 9. Conclusion

Current systems already retrieve scientific inspirations, generate cross-domain analogies and test transfer under controlled structural transformations [@shen2026analogical; @liu2026researchbench; @chen2026adr; @li2026retre]. The remaining scientific question is narrower: can remote discovery be made **conservative enough for scientific use** by requiring donor-native recovery, explicit challenge and correct target/novelty disposition?

This study is designed to answer that question without assuming the integrated method wins. If mature parent methods already recover the donors and preserve the native decisions at lower cost, they should be preferred. If a residual survives, it is a bounded result about the value of coupling discovery to scientific fidelity—not a claim that one representation captures the structure of science.

## Transparency

Large language model tools contributed materially to literature discovery, formalization, critique, software and drafting. AI systems are not authors. Human authors must directly inspect the load-bearing sources, protected receipts and final manuscript and take responsibility for all released claims.

## Bibliography source

Use `papers/primary/PRIMARY_PAPERS_REFERENCES_V1.bib`. Refresh all 2026 preprint/publication statuses immediately before arXiv upload and again before journal submission.
