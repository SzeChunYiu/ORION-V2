# Primary Papers Citation and Parent Binding V1

**Papers:** P-A, P-B, P-C, P-D  
**Status:** non-computational related-work/claim-role plan.  
**Rule:** every load-bearing parent claim in the final manuscripts must cite a source the human authors have directly checked; generated summaries are not sufficient for submission.

## Citation roles

- `OWNERSHIP` — removes novelty credit.
- `DIRECT_NEIGHBOR` — closest current system/benchmark.
- `CONTROL` — method/system that should appear in comparator design.
- `BOUNDARY` — source that narrows interpretation/terminology.
- `MOTIVATION` — relevance only, not ownership.

---

# P-A — structural donor discovery

## Classical ownership

- Gentner — structure mapping / relational analogy — `OWNERSHIP`.
- Swanson — literature-based discovery — `OWNERSHIP` for hidden cross-literature linkage.
- Plotkin — anti-unification/inductive generalization — `OWNERSHIP` where symbolic LGG applies.
- Formal Concept Analysis — `OWNERSHIP` for lattice-based concept abstraction.
- MDL / Rissanen — `OWNERSHIP` for compression/model-selection abstraction criteria.
- case-based reasoning / graph matching / ILP / scientific literature discovery — include strongest applicable sources after final saturation.

## Mandatory 2026 direct neighbors

### Analogical Reasoning in Science

Shen, Druckmann & Zou, *Unlocking LLM Creativity in Science through Analogical Reasoning*, arXiv:2605.11258.

Role: `DIRECT_NEIGHBOR + CONTROL`.

Final text must concede that cross-domain relational analogy for scientific solution generation is current prior work.

### ResearchBench

Liu et al., Findings ACL 2026, DOI `10.18653/v1/2026.findings-acl.644`.

Role: `DIRECT_NEIGHBOR + CONTROL` for scientific inspiration retrieval/hypothesis decomposition.

### Analogical Deep Research / CANA

Chen et al., arXiv:2607.13602.

Role: `VERY_STRONG_DIRECT_NEIGHBOR`; explicit structure/mechanism-aware analogy retrieval and integration.

### ReTRE

Li et al., ACL 2026, DOI `10.18653/v1/2026.acl-long.2048`.

Role: `BOUNDARY + BENCHMARK_PARENT` for controlled near/far structure-preserving transfer.

### TACL 2026 analogy papers

Stevenson et al., DOI `10.1162/tacl.a.614`; Petersen et al., DOI `10.1162/tacl.a.632`.

Role: `BOUNDARY` for LLM analogical transfer limitations and current cognitive/NLP analogy theory mapping.

## P-A required residual sentence

> The contribution, if supported, is not cross-domain analogy or inspiration retrieval itself, but a protected process that couples remote donor discovery to donor-native reconstruction, explicit negative-transfer challenge, native-verdict preservation and correct parent/novelty contraction under strongest-parent comparison.

---

# P-B — relation/transport interface

## Mandatory ownership families

Final related work should cite original/strong sources for:

- causal Markov equivalence and transportability;
- Blackwell/Le Cam decision comparison;
- measurement invariance/metrology comparability;
- bisimulation/contextual equivalence;
- abstract interpretation/Galois-style sound abstraction;
- Markov-chain lumpability;
- rough-set indiscernibility;
- value/policy equivalence where used;
- local-to-global obstruction/sheaf methods only if actually invoked;
- category theory only for cases with genuine categorical semantics.

## Current parent pressure

- stable quotient / minimal Markovization 2026 — `OWNERSHIP` for coarsest stable recursively updateable quotient in its model class;
- representation-identifiability 2026 — `BOUNDARY` that behavior/output equality does not identify arbitrary internal representation properties;
- ReTRE 2026 — `MOTIVATION/BOUNDARY` for target/context-relative transfer robustness.

## Proposition citations

The bounded P-B propositions should be presented as elementary/parent-style consequences, not citation-free novelty claims. Cite the parent family surrounding each proposition even when the proof is included.

## P-B required residual sentence

> The paper tests whether a common typed coordination interface changes cross-parent reuse or reopening decisions while preserving each parent’s native semantics; it does not propose a universal equivalence relation.

---

# P-C — scientific control

## Classical/direct ownership

Cite strongest original/current sources for:

- metareasoning / value of computation;
- Bayesian experimental design;
- active learning;
- POMDP/information-state control;
- truth maintenance/model diagnosis;
- CEGIS/CEGAR/theorem-proving search where invoked;
- robust/ambiguity-aware decision making;
- workflow/cognitive architectures where relevant.

## Mandatory current 2025–26 AI-scientist neighbors

### The AI Scientist

Nature 2026, *Towards end-to-end automation of AI research*, article `s41586-026-10265-5`.

Role: `VERY_STRONG_DIRECT_NEIGHBOR` for end-to-end autonomous research, tree-based experimentation, scaling and automated review.

### Robin

Ghareeb et al., Nature 2026, DOI `10.1038/s41586-026-10652-y`.

Role: `VERY_STRONG_DIRECT_NEIGHBOR` for multi-agent literature→hypothesis→experimental discovery.

### Co-Scientist

Nature 2026, article `s41586-026-10644-y`.

Role: `VERY_STRONG_DIRECT_NEIGHBOR` for generation/reflection/ranking/evolution, persistent memory, ablation/test-time compute and experimental validation.

### SPARK

Nature Medicine 2026, article `s41591-026-04357-y`.

Role: `DIRECT_NEIGHBOR` for adaptive computational scientific-strategy/tool building.

### Agentic X-ray scientist

Nature Machine Intelligence 2026, article `s42256-026-01261-5`.

Role: `DIRECT_NEIGHBOR` for adaptive planning/action on a real scientific instrument.

### AFM/other lab-agent work

Use current laboratory-agent evaluations as `CONTROL/MOTIVATION`, particularly where they evaluate experimental design→action→analysis rather than single tasks.

## P-C required contraction

Do not describe current agentic science as fixed pipelines. The candidate residual must be:

- justified scientific terminal control;
- correct blocker/responsibility diagnosis;
- minimum sufficient intervention;
- representation/formalism escalation after witnessed insufficiency;
- critical false-completion and over-escalation control;
- parity/non-regression;
- parent/local deference.

## Required residual sentence

> P-C does not test whether agents can plan, reflect, use tools or execute research workflows; it tests whether an explicit scientific-control layer improves justified terminal and intervention decisions beyond strong adaptive agents under non-compensatory parity and resource controls.

---

# P-D — dependence and dynamic evaluation

## Classical ownership

Cite strongest parent sources for:

- correlated/clustered evidence and dependent meta-analysis;
- hierarchical/common-cause models;
- provenance/lineage;
- measurement/test sensitivity and validation;
- performative prediction;
- Goodhart/Campbell/strategic response where used;
- distribution shift/adaptive data collection;
- evidence synthesis and assurance;
- authority/governance boundary.

## Mandatory current 2026 neighbors

### Reliability limits of LLM multi-agent planning

Ao, Gao & Simchi-Levi, arXiv:2603.26993.

Role: `VERY_STRONG_PARENT_PRESSURE`; shared-evidence agent multiplicity cannot be sold as new information.

### The Consistency Illusion

Wang & Yang, arXiv:2606.08457.

Role: `DIRECT_NEIGHBOR` for answer-level consensus masking reasoning misalignment.

### Reward Hacking as Equilibrium under Finite Evaluation

Wang & Huang, arXiv:2603.28063.

Role: `STRONG_THEORY_NEIGHBOR` for finite evaluation/optimization distortion.

### AlphaEval

Lu et al., arXiv:2604.12162.

Role: `DIRECT_EVALUATION_NEIGHBOR` for production agent tasks, heterogeneous criteria and evolving expert standards.

## P-D required residual sentence

> The candidate residual is not the observation that consensus can be dependent or evaluators can be gamed; it is whether explicit dependence topology, evaluator sensitivity and environment-response state jointly improve protected scientific validity/reopening decisions beyond the strongest separate parent pipelines.

---

# Submission refresh gate

Immediately before submission:

1. refresh every 2026 preprint to determine current archival status;
2. inspect full theorem/Methods text for load-bearing direct neighbors;
3. search citations/recent related work from the strongest direct neighbors;
4. perform title/abstract keyword collision searches for each residual;
5. add contrary/negative sources, not only supporting ones;
6. bind sentence-level citations;
7. have human authors directly read load-bearing sources.

No bibliographic update may widen the paper's novelty claim. New stronger parents can only preserve or contract it.
