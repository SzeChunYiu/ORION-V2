# Primary Papers Master Assembly Contract V1

**Papers:** P-A, P-B, P-C, P-D  
**Purpose:** eliminate scientific/editorial discretion from the post-computation manuscript assembly step.

## Global assembly order

For each paper:

1. read the pre-results science manuscript;
2. apply the paper's section of `PRIMARY_PAPERS_NEAREST_WORK_2026_PASS_V1.md` and `PRIMARY_PAPERS_CITATION_AND_PARENT_BINDING_V1.md` to Related Work/Introduction;
3. validate every headline claim against `PRIMARY_PAPERS_ATOMIC_CLAIM_GATE_V2.json`;
4. populate only fields in `PRIMARY_RESULTS_INSERTION_SCHEMA_V1.json`;
5. replace the pre-results abstract's result slot according to `PRIMARY_ARTICLE_FRONTMATTER_V1.md`;
6. select the pre-written Discussion branch matching the primary terminal;
7. preserve adverse/null/parent/CANNOT_CHECK outputs;
8. contract to live target-journal word/display/reference limits;
9. run overlap, human-adoption and AI-policy gates;
10. bind source/data/figure hashes.

A formatter may improve sentence-level clarity but may not invent or strengthen scientific claims.

---

# P-A assembly

```text
SCIENCE_MASTER = papers/drafts/P_A_STRUCTURAL_TRANSFER_DISCOVERY_MANUSCRIPT_V1_PRE_RESULTS.md
FRONTMATTER = P-A section of PRIMARY_ARTICLE_FRONTMATTER_V1.md
CURRENT_NEAREST_WORK = P-A section of PRIMARY_PAPERS_NEAREST_WORK_2026_PASS_V1.md
CLAIMS = P-A section of PRIMARY_PAPERS_ATOMIC_CLAIM_GATE_V2.json
RESULT_SCHEMA = P-A section of PRIMARY_RESULTS_INSERTION_SCHEMA_V1.json
TARGET = Nature Machine Intelligence Article
FALLBACK = Artificial Intelligence
```

### Mandatory current-neighbor insertion

Related Work must explicitly discuss:

- Analogical Reasoning in Science (Shen et al. 2026);
- ResearchBench (ACL Findings 2026);
- Analogical Deep Research / CANA (2026);
- ReTRE (ACL 2026);
- current TACL analogy-generalization/theory papers.

The P-A residual sentence from the citation binding file must appear in the Introduction/Related Work.

### Results branch mapping

```text
PROTECTED_TRANSFER_RESIDUAL -> positive bounded Discussion
CONTEXTUAL_TRANSFER_ONLY -> contextual/scope Discussion
PARENT_SUFFICIENT -> parent-win Discussion
FIXED_LESSON_SUFFICIENT -> adaptive discovery contraction
REMOTE_RECALL_GAIN_FALSE_ANALOGY_TOO_HIGH -> safety/false-transfer negative Discussion
NO_SCIENTIFIC_RESIDUAL -> no-residual Discussion
CANNOT_CHECK -> limitation/measurement terminal
```

---

# P-B assembly

```text
SCIENCE_MASTER = papers/drafts/P_B_CONTEXT_RELATIVE_RELATIONS_MANUSCRIPT_V1_PRE_RESULTS.md
FRONTMATTER = P-B section of PRIMARY_ARTICLE_FRONTMATTER_V1.md
CURRENT_NEAREST_WORK = P-B section of PRIMARY_PAPERS_NEAREST_WORK_2026_PASS_V1.md
CLAIMS = P-B section of PRIMARY_PAPERS_ATOMIC_CLAIM_GATE_V2.json
RESULT_SCHEMA = P-B section of PRIMARY_RESULTS_INSERTION_SCHEMA_V1.json
TARGET = Nature Computational Science Article
FALLBACK = Artificial Intelligence
```

### Formal rule

Propositions PB-C4A–D remain explicitly parent-style/bounded. A successful proof is not sufficient for the Article headline.

### Results branch mapping

```text
CROSS_PARENT_RELATION_RESIDUAL -> bounded coordination-interface claim
FORMAL_INTERFACE_ONLY -> resource/formal-method contraction
PARENT_ORCHESTRATION_RESOURCE -> engineering/interoperability route
PARENT_SUFFICIENT -> no independent mechanism
FORMAL_CLAIM_CONTRACTED -> narrowed formal + empirical result only if supported
CANNOT_CHECK -> unresolved
```

If no protected cross-parent decision residual exists, do not force an NCS Article merely because the propositions are correct.

---

# P-C assembly

```text
SCIENCE_MASTER = papers/drafts/P_C_SCIENTIFIC_CONTROL_MANUSCRIPT_V1_PRE_RESULTS.md
FRONTMATTER = P-C section of PRIMARY_ARTICLE_FRONTMATTER_V1.md
CURRENT_NEAREST_WORK = P-C section of PRIMARY_PAPERS_NEAREST_WORK_2026_PASS_V1.md
CLAIMS = P-C section of PRIMARY_PAPERS_ATOMIC_CLAIM_GATE_V2.json
RESULT_SCHEMA = P-C section of PRIMARY_RESULTS_INSERTION_SCHEMA_V1.json
TARGET = Nature Machine Intelligence Article
FALLBACK = npj Artificial Intelligence Article
```

### Mandatory current-neighbor insertion

Introduction/Related Work must represent at minimum:

- The AI Scientist;
- Robin;
- Co-Scientist;
- SPARK;
- agentic X-ray scientist;
- strongest relevant lab-agent benchmarks.

Do not describe these as rigid fixed pipelines.

### Results ordering

Main Results should answer in this order:

1. V1 critical parity/non-regression;
2. simple/control quality;
3. protected scientific outcomes;
4. minimum-sufficient intervention behavior;
5. resource Pareto;
6. component dispositions/heterogeneity.

A paper cannot lead with aggregate task score if critical parity failed.

---

# P-D assembly

```text
SCIENCE_MASTER = papers/drafts/P_D_DEPENDENCE_DYNAMIC_EVALUATION_MANUSCRIPT_V1_PRE_RESULTS.md
FRONTMATTER = P-D section of PRIMARY_ARTICLE_FRONTMATTER_V1.md
CURRENT_NEAREST_WORK = P-D section of PRIMARY_PAPERS_NEAREST_WORK_2026_PASS_V1.md
CLAIMS = P-D section of PRIMARY_PAPERS_ATOMIC_CLAIM_GATE_V2.json
RESULT_SCHEMA = P-D section of PRIMARY_RESULTS_INSERTION_SCHEMA_V1.json
TARGET = Nature Machine Intelligence Article
FALLBACK = npj Artificial Intelligence Article
```

### Mandatory current-neighbor insertion

Discuss as direct current parent pressure:

- reliability limits of shared-information LLM multi-agent planning;
- consensus/reasoning misalignment;
- finite-evaluator/reward-hacking theory;
- production/evolving agent evaluation.

### Joint-unification rule

The paper may claim a unified assurance object only if the registered joint comparator is positive. Separate dependence and performativity gains do **not** sum into a unified result.

If the joint discriminator fails, use the preauthorized dependence-only / performative-only / two-parent-sufficient branches.

---

# Top-tier contraction rule

Nature Articles currently allow 3,500 main-text words, 150-word abstracts and six display items. Pre-results master manuscripts are intentionally more complete than final main text.

After Results arrive:

- protect actual Results, negative controls and direct-parent discussion;
- move detailed theory/proofs/benchmark construction to Methods/Supplement as appropriate;
- shorten repeated programme motivation;
- never shorten away the strongest parent/control that makes the result look less novel;
- never move the primary negative result entirely to Supplement.

## Current terminal

`PRIMARY_ARTICLE_SCIENCE_ASSEMBLY = FROZEN__RESULT_IMPORT_AND_FORMATTING_ONLY`.
