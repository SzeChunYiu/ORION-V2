# Discovering Remote Scientific Structure Without Losing Native Meaning

## Abstract

Scientific advances often reuse structure from remote domains, but retrieval systems are usually optimized for topical or semantic proximity. We study a stricter problem: whether a machine can identify a scientifically relevant donor when surface vocabulary differs, reconstruct the donor in its native terms, project only the structure relevant to a declared target decision, expose losses and counterexamples, and recognize when an apparent novelty is already explained by a mature parent method. We define a source-bound donor representation, typed partial mappings, native-recovery and counter-probe requirements, and an evaluation that separates remote discovery from false analogy and scientific-fidelity loss. The study compares the resulting workflow with strong lexical/citation and embedding retrieval, literature-based discovery, analogical and formal parents, fixed transferable lessons, expert search, and their strongest information-matched federation. Hidden donor identities and target consequences are withheld from solver arms. Method superiority is not assumed: parent sufficiency, false-analogy trade-offs and no residual are predeclared scientific outcomes.

## 1. Introduction

Scientific discovery often depends on recognizing that a problem has already been solved in another language. A decomposition developed in numerical analysis may illuminate a biological inference problem; an invariant from mathematics may reveal why a physical representation is too coarse; an experimental design from one field may expose a failure mode in another. The useful donor need not be close in vocabulary, citation graph or disciplinary taxonomy.

This creates a difficult search problem for AI-assisted science. Conventional information retrieval is effective when the target and relevant source share terms, citations or semantic neighborhoods. Foundation-model embeddings can also recover broad conceptual resemblance. Yet a scientifically useful donor can be remote on all of these surfaces while preserving a relation that matters to a target judgment. Conversely, systems designed to seek surprising analogies can over-transfer: a relation may look elegant while violating a native assumption, reversing direction, ignoring a counterexample, or supporting a different decision from the one required by the target problem.

Recent work already attacks parts of this problem through scientific analogical reasoning, literature-based discovery, automated research inspiration, retrieval-augmented scientific agents and benchmarked scientific ideation. These are direct parents. The contribution of the present study is therefore not the claim that machines can find analogies, nor the idea that relations can matter more than words. We ask a narrower question:

> **Can a machine discover remote scientific structure while preserving the native scientific judgments that make the structure valid—and can it distinguish useful transfer from false analogy and parent sufficiency?**

We separate five operations that are often entangled.

1. **Candidate discovery** finds potentially relevant donors without access to hidden donor labels.
2. **Native reconstruction** checks whether the system can reproduce the donor's own objects, assumptions and known-answer judgments.
3. **Structural reduction** states a bounded relation between donor and target rather than a generic similarity score.
4. **Challenge** searches for counterexamples, obstruction conditions and negative-transfer cases.
5. **Scientific disposition** decides whether the donor supports bounded reuse, a contextual analogy, a parent-sufficiency conclusion, novelty contraction, rejection, or unresolvedness.

The central hypothesis is conditional. Explicit separation of these operations may improve remote-donor recovery or correct novelty contraction while controlling false analogy and native-verdict loss. The strongest null is that an information-matched federation of mature retrieval, analogy, formal and expert methods already makes the same decisions at equal or lower cost. If that null holds, the integrated workflow is useful engineering rather than a new scientific mechanism.

## 2. Relation to prior work

### 2.1 Analogy and structure mapping

Structure-mapping theory and computational analogy distinguish relational correspondence from surface resemblance. Modern language models can also generate and retrieve scientific analogies. The present study treats such systems as strong comparators and does not claim novelty for relational matching itself.

### 2.2 Literature-based discovery and scientific inspiration

Literature-based discovery searches for latent connections across separated literatures, while recent systems automate scientific inspiration, analogy generation and research-question discovery. A gain over ordinary semantic search is therefore insufficient. The relevant question is whether the additional native-recovery and challenge stages improve **scientific decisions** beyond these parents.

### 2.3 Formal abstraction

Anti-unification, least-general generalization, inductive logic programming, Formal Concept Analysis, invariant methods, algebraic constructions and description-length criteria already provide formal tools for abstraction. Where one of these parents fits the native problem, the study routes to it rather than replacing it with a generic transfer calculus.

### 2.4 Expert scientific judgment

Experts can recognize remote structure through accumulated disciplinary experience. Expert-local and expert-federated search therefore provide substantive controls. An AI system does not receive scientific credit for reconstructing a donor relation that was already supplied by the evaluator.

## 3. Formalizing conservative transfer

Let a target scientific problem be

\[
T=(P_T,J_T,C_T,E_T),
\]

where \(P_T\) is its native problem representation, \(J_T\) the registered target judgment or decision, \(C_T\) the scientific context and \(E_T\) the source/evidence state.

When a relational representation is appropriate, represent a donor or target as

\[
\mathcal S=(V,\mathcal R,\tau,\mathcal I,\mathcal X,\mathcal K),
\]

with native entities \(V\), relations or hyperedges \(\mathcal R\), type map \(\tau\), registered invariants \(\mathcal I\), counterexamples or obstructions \(\mathcal X\), and provenance/authority constraints \(\mathcal K\). This representation is optional: a donor that cannot be projected faithfully remains with its native method.

A candidate donor mapping is a partial typed relation

\[
\phi=(\phi_V,\phi_R):\mathcal S_D\rightharpoonup\mathcal S_T.
\]

Rather than assign one analogy score, evaluate a violation profile

\[
\mathbf e(\phi)=
(e_{type},e_{rel},e_{direction},e_{inv},e_{counter},e_{scope},e_{authority}).
\]

A registered critical violation rejects the proposed transfer even when semantic similarity is high.

### 3.1 Native recovery

Before a donor can support transfer, the system must recover preregistered native judgments, including at least one boundary or negative case. For donor test set \(K_D\), define

\[
F_{native}
=\frac{1}{|K_D|}\sum_{k\in K_D}
\mathbf 1[\hat J_D(k)=J_D(k)],
\]

while retaining critical cases as non-compensatory requirements rather than averaging them away.

Native recovery serves two purposes. It checks that the system has not replaced the donor with a convenient caricature, and it separates discovery from evaluator-supplied knowledge. A donor relation that cannot reproduce the donor's own decisive cases is not admitted merely because it appears useful for the target.

### 3.2 Remote structure

Remoteness is registered on several surfaces: lexical/topic distance, citation distance, disciplinary taxonomy, embedding distance and structural relation. A benchmark donor is considered remote when conventional proximity cues are deliberately weak but an independently specified structural relation changes a target judgment.

This definition avoids equating obscurity with value. A donor that is remote but irrelevant is a negative example, not evidence of creativity.

### 3.3 Conservative disposition

The system's output is a bounded scientific disposition rather than a statement that two domains are broadly analogous. The output records donor identity, native donor judgment, relation type and direction, preserved target consequence, non-mapped structure, counter-probes and scope. Permitted dispositions include bounded reuse, contextual transfer, false analogy, parent sufficiency, novelty contraction and unresolvedness.

## 4. Study design

### 4.1 Case families

The study uses four transfer directions:

- mathematics to mathematics;
- mathematics to empirical science;
- empirical science to mathematics or formalization;
- science to science.

Cases are constructed so that donor identities and target consequences are withheld from solver arms. Each case contains semantically near distractors, structurally tempting invalid donors, donor-native known-answer checks and at least one counter-probe capable of exposing false transfer.

### 4.2 Controls against leakage and surface matching

The evaluation includes renamed entities where semantics permit, same-vocabulary/different-structure controls, different-vocabulary/same-structure controls, citation-neighbor distractors, hidden assumptions and remote-domain holdouts. These controls test whether a method relies on the intended relation rather than a benchmark surface cue.

A post-result leakage analysis can qualify or invalidate a conclusion; it cannot retroactively promote the method.

### 4.3 Comparator arms

All methods receive matched target information and prospectively defined resource budgets. Comparators include:

- direct target-only reasoning;
- lexical/citation retrieval;
- embedding retrieval and reranking;
- literature-based discovery;
- structure-mapping/analogy methods;
- fixed lesson injection;
- the strongest applicable formal parent;
- expert-local or expert-federated search where feasible;
- the strongest information-matched parent federation.

The integrated workflow is compared against the strongest parent federation, not only against weak retrieval.

## 5. Evaluation

The primary unit is the registered case, not retrieved documents, generated candidates, model samples or repeated seeds.

The study reports a vector of outcomes rather than a single weighted score:

\[
V=(R_{remote},1-F_{analogy},F_{native},F_{target},Q_{contract},-C_{resource}),
\]

where \(R_{remote}\) measures remote-donor recovery, \(F_{analogy}\) critical false analogy, \(F_{native}\) native fidelity, \(F_{target}\) target consequence fidelity, \(Q_{contract}\) correct parent-sufficiency/novelty contraction, and \(C_{resource}\) resource cost.

Critical false analogy or native-fidelity failure is non-compensatory. A method cannot earn the headline result by increasing donor recall while degrading a registered critical scientific judgment.

Paired comparisons use the case as the independent unit. Task-family heterogeneity is reported explicitly. When the registered case set is treated as a finite census, descriptive quantities are distinguished from inferential uncertainty over a broader task population.

## 6. Results

**Authoring placeholder — blocks arXiv release until replaced by receipt-bound Results.**

The final Results section will follow this fixed order:

1. **Remote donor recovery under matched information and resources.** Report case-level and family-level performance of the integrated workflow and all strong parents.
2. **False analogy and native fidelity.** Test whether any retrieval gain is purchased by invalid transfer or donor caricature.
3. **Target scientific consequence.** Report whether identified donors change the registered target decision correctly.
4. **Novelty contraction and parent sufficiency.** Report cases where the correct outcome is that no independent residual remains.
5. **Resource and heterogeneity analysis.** Show where any benefit occurs and whether it is dominated by a simpler parent.
6. **Failure cases.** Keep decision-changing adverse examples in the main paper.

No narrative branch is selected before the protected receipts exist.

## 7. Interpretation logic

The manuscript has four predeclared scientific terminals.

### Integrated residual supported

This branch is used only if the integrated workflow improves remote-donor or contraction decisions beyond the strongest parent federation while preserving critical native and target judgments under matched resources.

### Parent sufficient

If the strongest parent federation reproduces the decisions at equal or lower cost, the study concludes that explicit integration adds no independent scientific residual for the tested scope.

### Recall–fidelity trade-off

If remote recall rises but false analogy or native fidelity worsens on critical cases, the study does not claim improved scientific discovery. The result becomes a failure-boundary paper or contracts to a cautionary benchmark.

### Cannot check / insufficient evidence

If donor adjudication, source identity or target consequences are not sufficiently independent or identifiable, the affected scope remains unresolved rather than being scored as a loss or win.

## 8. Discussion

The scientific value of remote structure discovery is not the production of unusual analogies. It is the ability to locate a donor, reconstruct what that donor actually establishes, transport only the warranted relation, challenge the mapping and recognize when the donor removes rather than creates a novelty claim.

A positive result would support a practical design principle for AI-assisted science: retrieval and analogy should be evaluated jointly with **native scientific fidelity and negative-transfer controls**, especially when systems search across disciplines. Such a result would not imply a universal structural language. Different domains may require different native representations and formal parents.

A parent-sufficiency result would be equally informative. It would show that sophisticated retrieval/analogy/formal compositions already provide the required control, arguing against another dedicated transfer layer. A false-analogy trade-off would show that seeking remoteness without native challenge can make scientific assistance less reliable even when retrieval metrics improve.

The main limitations are the representativeness of registered donor cases, the difficulty of independent native adjudication, the possibility that benchmark construction itself reveals structural cues, and the cost of expert/native validation. Generalization beyond the studied case families requires fresh domains whose donor relations were not used to design the representation.

### Historical invention as a donor family

A further donor class is not a scientific theory or equation but a **historical transformation of a possibility space**: a new movement, representation, generative rule, instrument, search procedure, problem formulation or coordination pattern. Such episodes occur in science and mathematics, but also in engineering, sport, music, art, design and craft. The transferable object is not the celebrated artifact itself. It is the bounded transformation from a predecessor repertoire to a successor repertoire, together with the constraints that motivated it, the predecessor capabilities it preserved or lost, and the functional discriminator by which the change could have been judged at the time.

This extension does not change the registered P-A benchmark or Results order. Historical invention cases are a prospective donor/source family for later work. They require time-sliced source cutoffs and matched failed, ignored or near-miss cases because retrospective fame can otherwise leak the answer and confuse later adoption with scientific or functional validity. A separate prospective protocol tests whether an explicit `GenerativeRegime`/`InventionEpisode` interface adds value beyond current transfer machinery and strongest creativity/open-ended-search parents before any invention-specific result is admitted to this paper.

## 9. Conclusion

Remote scientific transfer should be judged by more than whether a system retrieves a surprising source. A scientifically useful system must recover the donor's native meaning, preserve the target consequence, expose invalid mappings and contract novelty when a mature parent already suffices.

This study tests whether separating discovery, reconstruction, reduction, challenge and disposition provides value beyond the strongest parent methods. The answer is intentionally left to the held-out evidence. The paper succeeds scientifically whether that answer is an integrated residual, parent sufficiency, a recall–fidelity trade-off or a bounded unresolved result—provided the conclusion follows the registered case-level evidence rather than the desired architecture.

## Reproducibility and release note

The final public version will report the exact case registry identity, source universe, arm definitions, resource budgets, analysis-ready snapshot, independent-unit definition, analysis receipts and source-data objects needed to reproduce the reported Results. Internal repository development history is not part of the scientific narrative.
