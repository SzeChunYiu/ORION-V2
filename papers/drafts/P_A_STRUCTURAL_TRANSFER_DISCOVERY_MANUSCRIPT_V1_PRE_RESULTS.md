# Discovering Remote Scientific Structure Without Losing Native Meaning
## A Protected Study of Structural Donor Discovery, Reduction and Conservative Transfer

**Paper ID:** P-A  
**Status:** science/method manuscript complete before protected outcomes.  
**Primary target hypothesis:** Nature Machine Intelligence Article.  
**Fallback:** Artificial Intelligence.  
**Result authority:** none until protected P-A execution is imported.

## Abstract

Scientific advances often reuse structure from remote domains, yet retrieval systems are usually optimized for topical or semantic proximity. We study a stricter problem: whether a machine can identify a structurally relevant scientific donor when surface vocabulary differs, reconstruct the donor in its native terms, project only the decision-relevant structure, expose losses and counterexamples, and correctly conclude when an apparent novelty is already explained by a known parent. We define a source-bound donor representation, typed partial mappings, native-recovery and counter-probe requirements, and a non-compensatory evaluation separating remote discovery from false analogy and scientific-fidelity loss. The protected experiment compares the integrated process with lexical/citation/embedding retrieval, literature-based discovery, fixed lesson injection, structure-mapping and applicable formal parents, expert-local search, and their strongest information-matched composition. Hidden donors and native judgments are withheld from solver arms and adjudicated independently. The manuscript does not assume the integrated method is superior: parent sufficiency, false-analogy trade-offs and no residual are predeclared outcomes. Protected numerical results remain to be inserted from frozen receipts.

---

# 1. Introduction

Science routinely advances by reusing an idea that was developed elsewhere: an invariant, decomposition, representation, optimization principle, mathematical object, experimental design or failure mode. But the useful donor may be lexically remote from the target problem. A search for papers about the target topic can therefore miss a source whose scientific role is relevant while its terminology is not.

The converse failure is equally serious. Analogy systems can return remote material that appears structurally evocative yet changes the target's native scientific judgment. High analogy recall is not scientific value if it produces false transfers, hides donor assumptions or encourages the declaration of novelty where a mature parent already explains the result.

These two errors motivate a protected problem:

> **Can a machine discover a remote scientific donor and use it conservatively without replacing native scientific meaning with generic similarity?**

We separate five tasks that are often collapsed:

1. **candidate discovery** — finding potentially relevant donors;
2. **native reconstruction** — reproducing the donor's own objects, assumptions and known-answer judgments;
3. **structural reduction** — identifying a bounded relation between donor and target;
4. **challenge** — constructing counter-probes, obstructions or negative-transfer cases;
5. **scientific disposition** — reuse, contextual transfer, false analogy, parent sufficiency, novelty contraction or `CANNOT_CHECK`.

The central hypothesis is not that one structural representation is universally correct. It is that explicitly separating these tasks may improve remote-donor discovery or correct novelty contraction under matched information and resources while controlling false analogy and native-verdict loss.

The strongest null is important: a mature retrieval/analogy/formal-parent composition may already do everything needed. In that case the correct result is **parent sufficiency**, not a more elaborate ORION mechanism.

## Contributions frozen before outcomes

This paper contributes, before protected results:

- an operational definition of remote scientific donor discovery;
- a donor-faithful representation and mapping contract;
- a benchmark construction that separates semantic distance from structural relevance;
- explicit false-analogy, native-recovery and novelty-contraction outcomes;
- matched-resource comparisons against strong retrieval, analogy and formal parents;
- a preregistered non-compensatory analysis and negative-result logic.

The paper will claim method superiority only if the protected study supports it.

---

# 2. Parent theories and the novelty ceiling

## 2.1 Analogy and structure mapping

Structure-mapping theory distinguishes relational correspondence from surface feature matching and provides a mature cognitive account of analogy. Graph matching, case-based reasoning and analogical retrieval extend this computationally. P-A therefore cannot claim novelty for the idea that relations matter more than words.

## 2.2 Literature-based discovery

Literature-based discovery identifies latent connections across disjoint literatures and is a direct parent for remote knowledge discovery. A P-A gain over simple semantic retrieval is scientifically uninteresting if an information-matched LBD or related scientific-discovery method reproduces it.

## 2.3 Symbolic generalization and formal abstraction

Anti-unification/least-general generalization, inductive logic programming, Formal Concept Analysis and MDL-style model selection already supply principled forms of abstraction. Category-theoretic, algebraic or invariant-based methods may be the correct native parent for particular mathematical structures. P-A may route to these parents; it cannot relabel them as a new universal transfer calculus.

## 2.4 Retrieval and foundation-model representation

Embedding retrieval and foundation-model reranking provide powerful semantic and sometimes structural signals. Their performance is an empirical baseline, not a strawman. If large-model semantic retrieval plus a strong reranker identifies the donors at the same scientific fidelity and cost, a special transfer mechanism has no protected discovery residual.

## 2.5 Human experts

Domain experts can recognize remote structure through training and experience. Expert-local and expert-federated conditions are therefore genuine controls. A machine result is not superior merely because it automates a reconstruction already supplied by the evaluator.

## 2.6 Claim ceiling

This paper does **not** claim that:

- remote analogy is new;
- graph/relational matching is new;
- anti-unification, FCA or MDL are Machine-Epistemics inventions;
- any one structural representation applies to all sciences;
- retrieval failure proves lack of machine understanding;
- a found analogy is scientifically valid before native recovery and challenge.

The possible residual is narrower: a protected **selection, reconstruction, challenge and disposition process** that improves scientific decisions beyond the strongest parent composition.

---

# 3. Problem formulation

Let a target scientific problem be

\[
T=(P_T, J_T, C_T, E_T),
\]

where `P_T` is its native problem representation, `J_T` the registered target decision or prediction, `C_T` the scientific context and `E_T` source/evidence state.

A candidate donor `D` is eligible only if it has a source-bound native reconstruction. When useful, represent donor and target as typed relational structures

\[
\mathcal S=(V,\mathcal R,\tau,\mathcal I,\mathcal X,\mathcal K),
\]

where:

- `V` — native entities/objects;
- `R` — relations or hyperedges;
- `tau` — types;
- `I` — registered invariants/constraints;
- `X` — counterexamples, failure cases or obstructions;
- `K` — provenance and authority constraints.

This representation is optional. A domain that cannot be projected without losing native meaning remains with its native parent.

## 3.1 Candidate structural relation

A candidate relation may use a partial typed mapping

\[
\phi=(\phi_V,\phi_R):\mathcal S_D\rightharpoonup\mathcal S_T.
\]

For mapped relations, type/direction/invariant constraints are checked explicitly. Define a violation profile

\[
\mathbf e(\phi)=
(e_{type},e_{rel},e_{direction},e_{inv},e_{counter},e_{scope},e_{authority}).
\]

Critical violations are non-compensatory. High similarity cannot cancel a failed scientific invariant.

## 3.2 Native recovery

A donor is not considered correctly reconstructed unless the donor representation can reproduce a preregistered set of native known-answer judgments, including at least one negative/boundary case.

Define native fidelity

\[
F_{native}
=\frac{1}{|K_D|}\sum_{k\in K_D}
\mathbf 1[\hat J_D(k)=J_D(k)]
\]

for the frozen donor known-answer set `K_D`, with critical cases separately non-compensatory.

## 3.3 Remote structure

“Remote” is not defined only by different keywords. Benchmark construction records several distances:

- lexical/topic distance;
- citation-graph distance;
- disciplinary taxonomy distance;
- embedding distance;
- structural relation;
- native decision relevance.

A remote donor is one deliberately weak on conventional proximity signals yet independently judged structurally relevant to a frozen target decision.

## 3.4 Conservative transfer

A candidate transfer is admitted only for a bounded target consequence. The required output is not “these domains are analogous,” but:

```text
donor identity
native donor judgment
relation type and direction
mapped objects/relations
preserved target decision
losses / non-mapped structure
counter-probes
scope / expiry condition
scientific disposition
```

---

# 4. Benchmark design

## 4.1 Task families

The protected corpus combines:

1. **mathematics → mathematics** structural donors;
2. **mathematics → empirical science** donors;
3. **science → mathematics/formalization** donors;
4. **science → science** donors.

The intended generated/fresh suite contains at least 72 cases, balanced between mathematical/formal and empirical/computational tasks, with separate naturalistic prospective cases if independent adjudication is available.

## 4.2 Hidden-parent construction

Each task contains:

- a target problem;
- one or more eligible remote donors/parents;
- semantically near distractors;
- structurally tempting but invalid donors;
- donor-native known-answer checks;
- target hidden consequence or decision;
- counter-probe(s) that distinguish valid from false transfer.

Gold donor identities and target consequences are unavailable to solver arms.

## 4.3 Leakage controls

Controls include:

- post-freeze renaming of variables/entities where semantics permit;
- same words / different native structure;
- different words / same registered structure;
- citation-neighbour distractors;
- hidden assumptions;
- invalid donor composition;
- surface-template traps;
- remote-domain holdout from representation or signature construction.

A leakage diagnostic performed after outcomes cannot promote a result; it can only qualify or invalidate it.

---

# 5. Experimental arms

All arms receive matched target information and prospectively defined budgets.

## B0 — target-only/direct reasoning

No cross-domain retrieval beyond the target materials.

## B1 — lexical/citation retrieval

Strong conventional search using query expansion and citation neighbourhood where available.

## B2 — embedding/semantic retrieval

State-of-practice semantic search/reranking under the same source universe.

## B3 — literature-based discovery

Strongest feasible LBD/bridge-discovery parent.

## B4 — structure-mapping / analogy parent

Strongest applicable relational analogy method.

## B5 — fixed lesson injection

Human-authored candidate transferable lessons, frozen before target outcomes. This tests whether adaptive discovery is needed at all.

## B6 — formal parent

Applicable anti-unification, FCA, invariant, algebraic, categorical, MDL or other native formal method. Use only when its semantics are valid for the case.

## B7 — expert-local / expert federation

Experts search using the same source/time budget where feasible. Expert reconstruction used to create a benchmark cannot be double-counted as machine output.

## B8 — strongest parent federation

Best prospectively selected combination of the parents above, with no hidden P-A-specific judgment.

## M — integrated structural transfer process

The candidate process performs:

```text
candidate retrieval
-> native reconstruction
-> structural relation proposal
-> parent/formal reduction
-> counter-probe/obstruction search
-> bounded target projection
-> scientific disposition
```

The process is allowed to return `PARENT_SUFFICIENT`, `FALSE_ANALOGY`, `NO_TRANSFER` or `CANNOT_CHECK`.

---

# 6. Outcomes

No single similarity score is primary.

## 6.1 Remote donor recovery

Depending on corpus structure, report:

- top-k eligible donor recall;
- mean reciprocal rank or preregistered ranking metric;
- case-level exact discovery.

## 6.2 False analogy

A proposed donor is false when it fails a registered critical target/native constraint or hidden counter-probe.

Report false-transfer rate and severe/critical false-transfer rate separately.

## 6.3 Native fidelity

Measure donor-native known-answer preservation, with critical cases non-compensatory.

## 6.4 Target consequence quality

Did the donor lead to the correct frozen target decision/prediction without leakage?

## 6.5 Novelty contraction

For candidate “new” mechanisms or explanations, report whether the process correctly identifies:

- known parent sufficient;
- bounded residual remains;
- invalid proposed relation;
- unresolved/CANNOT_CHECK.

## 6.6 Resource cost

Report model/tool calls, tokens/compute, wall time, expert minutes and implementation burden separately.

---

# 7. Primary estimand and non-compensatory decision rule

Define the result vector

\[
V=(R_{remote},1-F_{analogy},F_{native},Q_{target},R_{contraction},-C_{resource}).
\]

P-A earns an independent mechanism residual only if the integrated process improves remote donor recovery **or** target/contraction decisions over the strongest parent federation while satisfying frozen critical thresholds for false analogy and native fidelity.

A recall gain that materially worsens critical false analogy does not count.

A tie in scientific quality with higher cost supports parent sufficiency or simplification.

---

# 8. Analysis plan

The independent unit is the scientific case, not model samples. Repeated seeds are nested within case.

Primary comparisons are paired wherever arms operate on the same task. Report:

- case-level outcome tables;
- paired effect estimates with uncertainty;
- domain-family stratification;
- remote-distance strata;
- false-analogy severity;
- resource Pareto comparisons.

Reasonable-specification analysis should vary only choices frozen as defensible before outcomes, including:

- ranking cutoff;
- valid-task rules;
- missing-arm treatment;
- domain stratification;
- resource normalization;
- evaluator sensitivity where multiple native checks exist.

If reasonable specifications disagree, report the disagreement.

---

# 9. Results insertion contract

This section is intentionally outcome-empty before protected execution.

A mechanical importer may insert only values bound to frozen receipts for:

1. task/sample flow;
2. remote donor recovery;
3. false analogy and critical failures;
4. native fidelity;
5. target consequence quality;
6. novelty contraction;
7. resource comparison;
8. subgroup/robustness results.

The importer may not change the primary outcome definition or rewrite a parent win as a mechanism gain.

### Required result terminals

Exactly one primary terminal should be assigned after evidence:

- `PROTECTED_TRANSFER_RESIDUAL`;
- `CONTEXTUAL_TRANSFER_ONLY`;
- `PARENT_SUFFICIENT`;
- `FIXED_LESSON_SUFFICIENT`;
- `REMOTE_RECALL_GAIN_FALSE_ANALOGY_TOO_HIGH`;
- `NO_SCIENTIFIC_RESIDUAL`;
- `CANNOT_CHECK`.

---

# 10. Discussion branches frozen before results

## If protected residual is positive

The claim is limited to the tested donor/source universe and decision classes. Emphasize that the contribution is not “analogy works,” but that explicit native recovery and challenge can improve scientifically useful remote transfer beyond the strongest matched parent composition.

Require replication or materially different target domains before a broad transfer-discovery claim.

## If strongest parent ties or wins

Conclude that a separate integrated mechanism is unnecessary for the tested class. Preserve any reusable benchmark, native-recovery protocol or negative-transfer analysis as infrastructure/resource contribution.

## If remote recall rises but false analogy also rises

Conclude that the discovery process is unsafe as a scientific-transfer method under the registered thresholds. A high creativity/retrieval score cannot rescue the result.

## If fixed lessons match adaptive discovery

Conclude that learner/adaptive discovery has no demonstrated residual. The simpler fixed or human-authored mechanism should be preferred until new evidence.

## If native reconstruction frequently fails

The result becomes evidence for a human-in-the-loop or parent-native reconstruction requirement rather than machine-autonomous donor reduction.

---

# 11. Limitations

1. Remote structural relevance depends on a registered target decision; there is no context-free structural-neighbour truth.
2. Expert-created donor corpora can embed expert priors and must be independently audited.
3. Generated tasks may exaggerate structural clarity relative to natural science.
4. Retrieval/source coverage can censor eligible donors.
5. Mathematical transfer can be formally checkable where empirical transfer cannot.
6. A valid relation for one target may be unsafe for future questions.
7. A large foundation model may encode donor knowledge parametrically even when retrieval is disabled; the experiment measures usable process, not provenance from training data.
8. Cost matching cannot make all human and machine resources commensurable.

---

# 12. Reproducibility and AI-use

Release, subject to licensing and review constraints:

- frozen task registry;
- source/donor identities after evaluation unlock;
- benchmark construction scripts;
- arm configurations;
- native known-answer checks;
- counter-probes;
- resource accounting;
- paired analysis;
- invalid/missing-case ledger.

AI systems have been used extensively in the ORION-V2 research programme for literature discovery, formalization, code generation, critique and drafting. The final submitting authors must verify claims, citations and results, comply with the target venue's current AI-use policy, and never list an AI system as an author.

---

# 13. Current paper terminal

```text
P_A_SCIENCE_CONTENT = COMPLETE_PRE_RESULTS
PA_C1 = MOTIVATION_SUPPORTED
PA_C2 = METHOD_DEFINED
PA_C3 = BLOCKED_PROTECTED_RESULTS
PA_C4 = BLOCKED_PA_C3_PLUS_EXTERNAL_NOVELTY_REVIEW
RESULTS = NOT_YET_AUTHORIZED
PRIMARY_TARGET = NATURE_MACHINE_INTELLIGENCE_ARTICLE_HYPOTHESIS
FALLBACK = ARTIFICIAL_INTELLIGENCE
```

No top-tier submission is authorized until protected result figures support the final article identity.

---

# Selected parent references for final bibliography binding

- Gentner, D. Structure-mapping: a theoretical framework for analogy. *Cognitive Science* 7, 155–170 (1983).
- Swanson, D. R. Fish oil, Raynaud's syndrome, and undiscovered public knowledge. *Perspectives in Biology and Medicine* 30, 7–18 (1986).
- Plotkin, G. D. A note on inductive generalization. In *Machine Intelligence 5* 153–163 (1970).
- Ganter, B. & Wille, R. *Formal Concept Analysis: Mathematical Foundations* (Springer, 1999).
- Rissanen, J. Modeling by shortest data description. *Automatica* 14, 465–471 (1978).
- Gentner, D. & Markman, A. B. Structure mapping in analogy and similarity. *American Psychologist* 52, 45–56 (1997).

Final related-work saturation must additionally bind current semantic retrieval, scientific literature-discovery and foundation-model analogy parents immediately before submission.
