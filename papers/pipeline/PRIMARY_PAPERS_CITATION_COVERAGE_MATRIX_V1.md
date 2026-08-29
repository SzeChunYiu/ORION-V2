# Primary Papers Citation Coverage Matrix V1

**Papers:** P-A, P-B, P-C, P-D  
**Purpose:** make citation placement and parent concessions auditable during final manuscript assembly.  
**Authority:** scientific related-work contract; exact BibTeX serialization is mechanical.

## Global rule

Every load-bearing sentence that assigns ownership, defines the nearest system, or motivates a current limitation must carry at least one direct source in the final manuscript. A parent may be removed only if the corresponding sentence/claim is also removed or contracted.

Human authors must directly read the load-bearing sources before submission.

---

# P-A

| Manuscript assertion | Citation role | Required sources / source family |
|---|---|---|
| relational structure can matter beyond surface similarity | `OWNERSHIP` | Gentner 1983; Gentner & Markman 1997 |
| remote connections across disjoint literatures are an established discovery problem | `OWNERSHIP` | Swanson 1986 + current LBD review/original systems |
| symbolic generalization/abstraction already exists | `OWNERSHIP` | Plotkin 1970; FCA; MDL; relevant ILP parent |
| LLMs are already used for scientific analogical reasoning | `DIRECT_NEIGHBOR` | Shen, Druckmann & Zou 2026, arXiv:2605.11258 |
| scientific inspiration retrieval/hypothesis decomposition has a current benchmark | `DIRECT_NEIGHBOR` | ResearchBench, Findings ACL 2026, DOI 10.18653/v1/2026.findings-acl.644 |
| mechanism-aware historical analogy/deep-research systems already exist | `VERY_STRONG_NEIGHBOR` | Analogical Deep Research/CANA, arXiv:2607.13602 |
| far structure-preserving transfer evaluation already exists | `DIRECT_NEIGHBOR` | ReTRE, ACL 2026, DOI 10.18653/v1/2026.acl-long.2048 |
| current LLM analogy theory/generalization literature is mature enough to block first-work claims | `BOUNDARY` | Stevenson et al. TACL 2026; Petersen et al. TACL 2026 |
| donor-native reconstruction + challenge + novelty contraction is the tested residual | `P-A_INTERNAL_METHOD` | manuscript Methods + protected result, no external novelty laundering |

### Mandatory nearest-work paragraph

The final manuscript must say, in substance:

> Current systems already retrieve or generate structural analogies for scientific discovery and benchmark scientific inspiration retrieval and far-transfer robustness. P-A therefore tests a narrower question: whether remote donor discovery becomes scientifically more reliable when candidate donors must also recover their native judgments, survive explicit negative-transfer probes and support correct target/novelty disposition under strongest-parent comparison.

---

# P-B

| Manuscript assertion | Citation role | Required parent family |
|---|---|---|
| observational equivalence differs from intervention/causal transport | `OWNERSHIP` | Pearl/causal Markov equivalence + Bareinboim/Pearl transportability |
| decision equivalence/informativeness is task-relative | `OWNERSHIP` | Blackwell; Le Cam where used |
| measurement comparability/invariance is parent-owned | `OWNERSHIP` | Meredith measurement invariance; JCGM/BIPM metrology |
| formal behavioral/contextual equivalence is parent-owned | `OWNERSHIP` | Milner/bisimulation/contextual equivalence parent |
| safe abstraction/refinement is parent-owned | `OWNERSHIP` | Cousot & Cousot abstract interpretation |
| stable/right-congruent/minimal state quotienting is current active parent theory | `OWNERSHIP/BOUNDARY` | stable quotient 2026 + automata/ISFSM parent if invoked |
| output/predictor equality does not identify arbitrary representation properties | `BOUNDARY` | current representation-identifiability work |
| context refinement proposition is not new mathematics | `PARENT_STYLE` | cite decision/contextual-equivalence parent around proposition |
| exact decision-preserving composition proposition is not empirical transport | `PARENT_STYLE` | cite formal composition/abstraction parent and causal/measurement boundary |
| selective reopening proposition depends on declared sufficient-support-family semantics | `BOUNDARY` | truth-maintenance/assurance/support parent + manuscript proof |
| standalone residual is protected cross-parent reuse/reopening value | `P-B_INTERNAL_METHOD` | protected result only |

### Mandatory nearest-work paragraph

> The paper does not seek one universal relation of scientific sameness. Causal, decision-theoretic, measurement and formal parents already supply distinct validity notions. The shared object is tested only as a coordination interface: can it select and compose those native relations, expose loss/obstruction and improve protected reuse/reopening decisions without changing parent-native judgments?

---

# P-C

| Manuscript assertion | Citation role | Required sources/families |
|---|---|---|
| computational metareasoning/action-value selection is established | `OWNERSHIP` | Russell & Wefald; value-of-computation parent |
| Bayesian experiment selection/active learning are established | `OWNERSHIP` | Chaloner & Verdinelli; Settles/current active-learning parent |
| partially observed state/action control is established | `OWNERSHIP` | POMDP/information-state sources |
| truth maintenance/diagnosis and CEGIS-style repair are established | `OWNERSHIP` | Doyle/de Kleer/Reiter; CEGIS/CEGAR parents where used |
| current AI Scientist is end-to-end/adaptive rather than rigid | `VERY_STRONG_NEIGHBOR` | Lu et al. Nature 2026, s41586-026-10265-5 |
| current multi-agent autonomous discovery exists | `VERY_STRONG_NEIGHBOR` | Robin, Nature 2026, 10.1038/s41586-026-10652-y |
| current Co-Scientist already uses generation/reflection/ranking/evolution/memory | `VERY_STRONG_NEIGHBOR` | Nature 2026, s41586-026-10644-y |
| current scientific agents can build computational strategies/tools | `DIRECT_NEIGHBOR` | SPARK, Nat Med 2026, s41591-026-04357-y |
| agents can plan/act on real scientific instruments | `DIRECT_NEIGHBOR` | agentic X-ray scientist, NMI 2026, s42256-026-01261-5 |
| minimum sufficient escalation is not claimed as a universal ladder | `P-C_SCOPE_RULE` | manuscript formalization + parent-control context |
| scientific-control residual concerns justified terminals/interventions, not generic automation | `P-C_INTERNAL_METHOD` | protected result only |

### Mandatory nearest-work paragraph

> End-to-end and multi-agent AI-scientist systems already perform literature search, planning, reflection, experimentation, tool construction and real instrument control. P-C therefore does not test whether AI can automate a scientific workflow. It tests whether an explicit scientific-control layer improves the justification of terminals and intervention choice—including abstention and representation/method change—over strong adaptive parent systems under frozen parity and resource constraints.

---

# P-D

| Manuscript assertion | Citation role | Required sources/families |
|---|---|---|
| dependent/correlated effect estimates require non-naive treatment | `OWNERSHIP` | robust variance/hierarchical/meta-analysis parents |
| provenance exposes lineage but is not itself statistical independence | `BOUNDARY` | provenance parent + dependence statistics |
| evaluator sensitivity matters to what a pass supports | `OWNERSHIP` | severe testing/testing-oracle/measurement-validation parents |
| performative/strategic response can change evaluation distribution | `OWNERSHIP` | Perdomo et al. performative prediction + Goodhart/strategic parent where used |
| multiple LLM agents sharing information do not create unlimited new decision information | `DIRECT_THEORY_NEIGHBOR` | Ao, Gao & Simchi-Levi 2026, arXiv:2603.26993 |
| answer consensus can hide reasoning misalignment | `DIRECT_NEIGHBOR` | Wang & Yang 2026, arXiv:2606.08457 |
| finite evaluation can create reward-hacking/equilibrium pressure | `DIRECT_THEORY_NEIGHBOR` | Wang & Huang 2026, arXiv:2603.28063 |
| evolving/production agent evaluation is an active benchmark problem | `DIRECT_NEIGHBOR` | AlphaEval 2026, arXiv:2604.12162 |
| unknown dependence is not silently independence | `P-D_SCOPE_RULE` | dependence/statistical parent + manuscript protocol |
| unified assurance must beat separate parent pipelines | `P-D_INTERNAL_HYPOTHESIS` | protected joint result only |

### Mandatory nearest-work paragraph

> Neither unreliable multi-agent consensus nor finite-evaluator failure is new. Recent theory and empirical work already limit reliability claims based on shared-information agent multiplicity, answer-level agreement and finite evaluation. P-D asks a narrower scientific-validity question: whether explicit dependence topology, evaluator sensitivity and environment-response state jointly improve protected validity or reopening decisions beyond applying the strongest existing dependence and dynamic-evaluation methods separately.

---

# Global final citation audit

Before submission:

- [ ] every row marked `OWNERSHIP`, `DIRECT_NEIGHBOR` or `BOUNDARY` is cited in the final paper;
- [ ] current 2026 preprint/publication status refreshed;
- [ ] no citation is used solely as decorative bibliography padding;
- [ ] contrary/limiting work included;
- [ ] exact statement read in full text for load-bearing sources;
- [ ] no abstract-only inference is presented as theorem content;
- [ ] sentence-level claim does not exceed cited evidence;
- [ ] related ORION manuscript is cited/disclosed only according to current double-submission/overlap policy.

Terminal:

`PRIMARY_PAPERS_CITATION_SCIENCE = FROZEN__BIBTEX_SERIALIZATION_AND_FINAL_STATUS_REFRESH_MECHANICAL`.
