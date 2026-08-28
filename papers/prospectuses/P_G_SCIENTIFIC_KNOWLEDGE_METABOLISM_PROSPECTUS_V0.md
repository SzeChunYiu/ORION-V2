# Scientific Knowledge Metabolism
## Decomposing, Recovering and Recombining Knowledge for Machine Discovery

**P-G prospectus V0 — contingent Article candidate**  
**Primary target if evidence survives:** Nature Machine Intelligence Article  
**Fallbacks:** Artificial Intelligence; npj Artificial Intelligence; merge into P-A/P-C/flagship  
**Status:** experiment-ready prospectus, not an admitted publication identity and not a results paper.

## Abstract

Retrieval-augmented and agentic AI systems can quote, summarize and combine information while still failing to preserve the native assumptions, counterexamples, validity conditions and authority boundaries of their sources. We investigate a different lifecycle, provisionally called **scientific knowledge metabolism**: source-bound material is decomposed into typed epistemic units, sorted by provenance, dependence and authority, reconstructed in its native parent theory, reduced against the strongest existing solution, selectively absorbed, recombined into a new proposal, challenged by discriminators and falsifiers, and either assimilated into a bounded scientific state or recycled as negative knowledge. The biological and recycling metaphors are design intuitions, not scientific evidence. The scientific claim is narrower: does this typed decomposition–recovery–recombination lifecycle improve real problem solving, valid transfer, generativity or selective failure recovery beyond direct language-model generation, retrieval, same-model reflection and the strongest parent federation under matched information and resources? We define executable reference semantics, component ablations and a real-problem programme spanning software debugging, causal-network inference and materials-discovery decisions. The paper survives only if the full lifecycle yields protected value beyond its strongest parents and simpler controls; otherwise its components return to the donor-discovery and solver papers.

## 1. Problem

Current machine knowledge systems often operate at the level of documents, passages, messages or latent embeddings. These units are convenient for retrieval but poor scientific atoms. One passage can contain:

- an observation;
- an inferential claim;
- an assumption;
- a procedure;
- a causal relation;
- a counterexample;
- an authority or consent constraint;
- a failure lesson.

Combining passages without separating these roles can produce fluent but scientifically invalid synthesis. A model can preserve the words of a result while losing its calibration, intervention semantics, scope, competence requirements or source authority.

P-G asks whether a source-bound decomposition and recovery lifecycle produces measurable scientific value.

## 2. The metabolism analogy and its limit

### Biological inspiration

An organism does not ordinarily use dietary protein as one intact object. Digestion breaks it into smaller constituents; the organism selectively absorbs, transforms and recombines them into structures serving its own current needs. Some material is rejected, stored or converted to waste.

### Recycling inspiration

A recycling centre separates heterogeneous material, identifies reusable fractions, removes contamination and recombines recovered material into new products. A mixed object is not treated as one reusable semantic unit.

### Scientific translation

The proposed lifecycle is:

```text
INGEST
→ DECOMPOSE
→ SORT
→ NATIVE_RECONSTRUCT
→ REDUCE AGAINST PARENTS
→ ABSORB
→ RECOMBINE
→ CHALLENGE
→ ASSIMILATE OR RECYCLE
```

The analogies do not establish that this pipeline is correct, efficient or novel. They only suggest a decomposition architecture. Every stage remains subject to parent ownership, component removal and real-problem evaluation.

## 3. Executable object

The reference implementation is:

`src/orion_v2/knowledge_metabolism.py`.

### Source fragment

A source fragment binds:

- source and content identity;
- source mode;
- custody/licence state;
- authority ceiling;
- structured native units.

### Knowledge atom

An atom binds:

- epistemic kind;
- canonical content;
- source and fragment identities;
- native terms;
- assumptions;
- counterexamples;
- dependence;
- authority ceiling.

Equivalent atoms merge only when their kind, canonical content, native terms and assumptions match. Provenance is unioned and authority is capped at the weakest contributing source.

### Recombination proposal

A proposal binds:

- absorbed atoms;
- bridge relations;
- intended scientific decisions;
- discriminator;
- falsifier;
- requested authority.

A proposal with unknown atoms, missing native recovery, absent challenge or amplified authority is blocked.

## 4. Candidate hypotheses

### H1 — Decomposition fidelity

Typed decomposition reduces category errors relative to passage-level retrieval, especially when one source contains claims, assumptions and procedures with different scientific roles.

### H2 — Native recovery

Explicit recovery of native parent judgments, assumptions and counterexamples reduces false analogy and unsafe cross-domain transfer.

### H3 — Recombination generativity

Source-bound atom recombination can produce executable solutions or scientific discriminators not obtained by direct retrieval or summarization.

### H4 — Challenge value

A mandatory discriminator/falsifier stage reduces false completion and brittle patches beyond same-model reflection.

### H5 — Selective assimilation

Support-family selective assimilation and reopening retain valid knowledge more accurately than flat overwrite, global restart or indiscriminate memory retention.

### H6 — Cost/context dependence

The full lifecycle is valuable mainly on heterogeneous, cross-source or failure-sensitive problems and becomes redundant drag on simple direct tasks.

### H7 — Independent machine problem solving

Performance on gold-blind executable tasks, seeded counterfactual variants and hidden tests can demonstrate problem-solving behaviour not explained by verbal reproduction alone, although no experiment can prove complete absence of training-data influence.

## 5. Strongest parent threats

P-G does not own generic decomposition, knowledge graphs or analogy. Strong parents include:

- literature-based discovery;
- case-based reasoning;
- computational analogy and structure mapping;
- knowledge compilation and modular knowledge representation;
- truth-maintenance and belief revision;
- argumentation and assurance cases;
- ontology alignment and data integration;
- program synthesis and automated repair;
- retrieval-augmented generation and agent memory;
- cognitive memory consolidation/reconsolidation;
- design-by-analogy and morphological analysis;
- scientific workflow and provenance systems.

The strongest comparator is a federation of these parents with expert routing, not an isolated retrieval baseline.

## 6. Real-problem study

The frozen registry is:

`research/experiments/ORION_REAL_PROBLEM_SUITE_V1.json`.

### Domain A — real software debugging

BugsInPy supplies reproducible Python bugs. Solvers receive a gold-blind buggy workspace. Proposed patches are evaluated in fresh checkouts using native compilation and regression tests.

Arms:

- direct solver;
- retrieval-only;
- same-model reflection;
- strongest parent federation;
- full metabolism lifecycle;
- stage ablations;
- machine-native strategy;
- human expert.

### Domain B — causal-network inference

CausalBench tests observational and perturbational causal discovery. Protected variants use held-out interventions, seeded label permutations, uncertainty-form checks and common-preprocessing dependence.

Potential P-G outcomes include better model selection, invalid-transfer detection or experiment choice; a new causal algorithm is not assumed.

### Domain C — materials discovery decisions

Matbench Discovery supports model evaluation under accuracy, robustness and computational-cost trade-offs. Protected contracts vary resource limits, false-discovery tolerance, held-out material families and uncertainty requirements.

The question is whether knowledge metabolism improves scientific selection and adaptation, not whether it can repeat published leaderboard facts.

## 7. Anti-copy design

The study does not use “different wording” as evidence of intelligence. It uses converging controls:

- fixed/gold solutions withheld;
- solver network disabled where feasible;
- newly generated identifier, label and unit permutations;
- hidden tests and interventions;
- counterfactual variants produced after protocol freeze;
- execution/native scientific outcomes as primary metrics;
- source-use receipts;
- retrieval-off/no-memory controls;
- textual similarity measured only after outcome scoring;
- cases whose surface templates are misleading.

A novel-looking failure is not intelligent. A correct solution that survives hidden counterfactual tests is stronger evidence of active problem solving.

## 8. Primary outcomes

- executable or native-domain success;
- critical false-completion rate;
- unsafe-transfer rate;
- native-parent judgment preservation;
- diagnosis and discriminator quality;
- selective-reopening correctness;
- prospective generativity;
- component attribution;
- wall time, compute, memory, tokens, expert labour and implementation burden;
- robustness under source, representation and problem perturbation.

Hard scientific and authority failures remain non-compensatory.

## 9. Causal component design

Run:

```text
FULL
MINUS_DECOMPOSITION
MINUS_NATIVE_RECOVERY
MINUS_COUNTERPROBE
MINUS_SELECTIVE_REOPEN
PARENT_REPLACEMENT
MERGED_SIMPLIFICATION
SIMPLE_DIRECT
```

Add pair interventions where stage synergy is suspected. A component is:

- necessary;
- parent-replaceable;
- contextual;
- redundant drag;
- harmful;
- `CANNOT_CHECK`.

The paper must report cases in which the simple or parent method wins.

## 10. Formal directions

### 10.1 Conservative atom merge

Characterize when two source units may be merged without losing a registered judgment, assumption or counterexample.

### 10.2 Authority monotonicity

Show that recombination cannot raise authority above the weakest necessary absorbed source or external decision root.

### 10.3 Recovery-preserving recombination

Define conditions under which a recombined proposal permits parent-native recovery on registered subproblems.

### 10.4 Minimal challenge sets

Characterize the smallest discriminator/falsifier family sufficient to expose a declared class of unsafe recombinations.

### 10.5 Metabolic efficiency frontier

Study when finer decomposition yields scientific gains and when its computational/annotation cost dominates.

## 11. Figure plan

1. **The lifecycle:** document/workspace → typed atoms → native recovery → recombination → challenge → assimilation/recycling.
2. **False synthesis examples:** same words/different scientific role; same claim/different assumptions; preserved text/lost competence.
3. **Real-problem results:** full versus F0/direct/reflection and stage ablations on success–critical-failure–cost axes.
4. **Anti-copy evidence:** hidden counterfactual and execution outcomes versus text similarity.
5. **Component map:** necessary, contextual, parent-replaceable and drag stages.

## 12. Paper survival rule

P-G becomes a standalone Article only if:

1. the full lifecycle produces a protected scientific or generative gain beyond the strongest parent federation;
2. native-parent and authority hard gates do not regress;
3. at least two materially different real domains support the residual;
4. component interventions identify the mechanism;
5. the gain survives resource matching and counterfactual anti-copy tests;
6. independent reviewers can reproduce the semantic judgments.

Otherwise:

- decomposition/native-recovery findings merge into P-A/P-B;
- solver/challenge findings merge into P-C/P-D;
- the field-level metaphor remains a compact flagship explanation;
- P-G terminates as `MERGE_INTO_EXISTING_PAPERS`.

## Current terminal

```text
P_G = CONTINGENT_EXPERIMENT_READY_PROSPECTUS
KNOWLEDGE_METABOLISM_REFERENCE_SEMANTICS = IMPLEMENTED
REAL_PROBLEM_RESULTS = OPEN
DISTINCT_RESIDUAL_BEYOND_F0 = CANNOT_CHECK
TOP_TIER_ARTICLE_STATUS = NOT_EARNED
DEFAULT_NO_GAIN_TERMINAL = MERGE_INTO_P_A_P_B_P_C_P_D
```
