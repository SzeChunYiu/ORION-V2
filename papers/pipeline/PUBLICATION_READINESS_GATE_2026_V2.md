# ORION-V2 Publication Readiness Gate — 2026 V2

**Status:** submission-governance and evidence gate. Journal targets are aspirations, not acceptance forecasts. No paper is `SUBMISSION_READY` merely because its manuscript is complete, a local test suite passes, or a venue appears well matched.

## 1. Current official format constraints

Format facts were rechecked on 28 August 2026 against the journals’ official pages.

| Venue and type | Current format | Consequence for ORION |
|---|---|---|
| Nature Machine Intelligence Article | main text up to 3,500 words; abstract up to 150; up to 6 display items; around 50 references; Introduction/Results/Discussion/Methods | Specialist papers must concentrate on one decisive empirical or formal result. Parent atlases and full audit ledgers stay supplementary/repository-side. |
| Nature Machine Intelligence Perspective | 3,000–4,000 words; up to 100 references; peer reviewed; balanced, scholarly and forward-looking | The flagship cannot reproduce the full foundation atlas or present a large set of unpublished ORION experiments. It needs a small, selective evidence spine. |
| Nature Computational Science Article | main text up to 3,500 words; abstract up to 150; up to 6 display items; around 50 references | P-B/P-E need broad computational-science relevance and multi-domain evidence, not only ORION fixtures. |
| Nature Computational Science Perspective | up to 4,000 words; up to 100 references; peer reviewed | Possible fallback for a computational-science-focused foundation, but only if the argument is broader than one framework. |
| npj Artificial Intelligence Perspective | normally up to 3,000 words; guideline up to 70 references; peer reviewed | Tier-2 flagship fallback requires stronger contraction than NMI, not claim inflation. |
| npj Artificial Intelligence Review | normally 3,000–4,000 words; typically up to 100 references; peer reviewed | Appropriate only if the result is a balanced field review rather than a founded-field claim. |

Official pages:

- https://www.nature.com/natmachintell/content
- https://www.nature.com/natcomputsci/content
- https://www.nature.com/npjai/content-types

Nature Portfolio policy also states that large language models do not qualify as authors and substantive LLM use should be documented in Methods or another suitable section; human authors retain accountability. This must be handled explicitly in every manuscript using the ORION research/writing pipeline.

## 2. Readiness ladder

### R0 — Research prospectus

- central question and falsifier exist;
- strongest parents are preliminary;
- no protected result;
- manuscript identity can still merge or disappear.

### R1 — Design manuscript

- target archetype and central thesis are clear;
- parent ownership and strongest comparator are specified;
- protocol, endpoints, negative controls and kill conditions are frozen in principle;
- decisive outcomes remain open.

### R2 — Reference semantics and pilots

- known-answer or constructed hostile cases pass;
- code/receipts are replayable;
- no naturalistic or externally protected value is inferred;
- effect estimates and evaluator independence remain incomplete.

### R3 — Protected cross-domain evidence

- frozen prospective protocol executed;
- strongest information/resource-matched parents included;
- independent or blinded semantic evaluation completed where required;
- at least one remote or naturalistic domain included;
- statistical uncertainty, failures, parent wins and `CANNOT_CHECK` retained;
- code/data/receipt package frozen where legally possible.

### R4 — Submission-ready

All R3 requirements plus:

- one defensible paper-scale thesis;
- every central claim has an evidence unit and source identity;
- journal format, word count and display-item limits passed;
- title/abstract understandable without ORION vocabulary;
- source-by-source reference audit complete;
- author contributions, competing interests, data/code availability and AI-use disclosure drafted;
- independent hostile editor review finds no unresolved fatal correctness, ownership or scope issue;
- venue-specific cover letter and fallback framing prepared without changing frozen science.

Only R4 permits `SUBMISSION_READY`. Editorial acceptance remains external.

## 3. Current research landscape pressure

Recent systems demonstrate increasingly long executable research loops, including multi-agent experimental biology, autonomous computational-biology analysis, collaborative scientific machine learning and self-correcting laboratory agents. Current full-cycle benchmarks, however, still report substantial failures and variance in rediscovery and scientific-literature coverage. The publication burden is therefore not to show that an agent can emit a plausible paper; it is to show controlled, evidence-bound scientific transitions under strong baselines.

Current baseline examples to reconstruct and compare include:

- Ghareeb et al., multi-agent scientific discovery, *Nature* (2026), DOI 10.1038/s41586-026-10652-y;
- Alber et al., CellVoyager, *Nature Methods* (2026), DOI 10.1038/s41592-026-03029-6;
- Jiang & Karniadakis, AgenticSciML, *npj Artificial Intelligence* (2026), DOI 10.1038/s44387-026-00102-5;
- Panapitiya et al., AutoLabs, *Scientific Reports* (2026), DOI 10.1038/s41598-026-45593-z;
- FIRE-Bench, arXiv:2602.02905;
- AutoResearchBench, arXiv:2604.25256;
- the Nature Machine Intelligence editorial “Multi-agent AI systems need transparency”, DOI 10.1038/s42256-026-01183-2.

## 4. Shared top-tier gate

Every Article candidate must have:

1. **one result-scale thesis** — no paper attempts to prove the entire field;
2. **strongest parent federation** — not a weak isolated baseline;
3. **prospective identity** — case, subject, criteria, budgets and primary outcomes frozen before access;
4. **non-compensatory failures** — scientific integrity and authority cannot be averaged away;
5. **simple-control losses** — cases where ORION complexity should lose;
6. **component attribution** — FULL/MINUS/PARENT/MERGED and interaction analyses;
7. **resource curves** — compute, time, memory, expert effort and implementation burden;
8. **cross-domain restoration** — at least two materially different domains for universal claims;
9. **independent adjudication** — not only same-model reviewers;
10. **complete failure reporting** — negative, tie, parent-win and unresolved cases;
11. **reproducibility package** — source, code, data, configuration, receipts and statistical analysis;
12. **no field-authority laundering** — publication venue is not evidence of theory truth.

## 5. Paper-by-paper readiness

### Flagship — Machine Epistemics Perspective

**Target:** Nature Machine Intelligence Perspective.  
**Fallback:** npj Artificial Intelligence Perspective or Review.

**Current level:** `R1_PROVISIONAL_FIELD_HYPOTHESIS`.

**Before R4:**

- foundation saturation and F0–F3 synthesis reach an honest internal terminal;
- field residual supported by frozen specialist results or clearly framed as hypothesis;
- parent recovery and four-candidate comparison are visible;
- at least two cross-domain demonstrations exist;
- public argument fits 3,000–4,000 words and at most four major figures;
- no substantial unpublished result is used to carry the Perspective;
- external parent-field demarcation review completed.

**Kill/contraction:** retitle as an integration Perspective on reliable agentic science if F0/F1/F3 remains sufficient.

### P-A — Structural donor discovery

**Target:** Nature Machine Intelligence Article.  
**Fallback:** Artificial Intelligence journal; a methods/resource venue if the residual contracts.

**Current level:** `R1_DESIGN_MANUSCRIPT`.

**Before R4:** hidden parent benchmark; remote-domain recall; false-analogy and native-verdict hard gates; source/custody correctness; expert reproduction; strongest retrieval/analogy/MDL federation; resource attribution.

### P-B — Context-relative relations and transport

**Target:** Nature Computational Science Article.  
**Fallback:** Artificial Intelligence journal or another rigorous computational-method venue.

**Current level:** `R1_DESIGN_MANUSCRIPT`.

**Before R4:** native parent suites; formal composition/reopening results; computational and uncertainty-form preservation; competence/authority transport; naturalistic representation changes in two sciences; strongest parent relation product.

### P-C — Obligation-driven scientific solver

**Target:** Nature Machine Intelligence Article.  
**Fallback:** npj Artificial Intelligence Article or a high-standard ML/AI venue appropriate to the final method.

**Current level:** `R1_TO_R2_REFERENCE_DESIGN`.

**Before R4:** V1 parity; strongest adaptive parent federation; self-model calibration; false/missed escalation; exploratory/constructive action modes; computational/oracle diagnosis; resilience; simple-control and component-drag cases; fresh expert-adjudicated scientific tasks.

### P-D — Dependence-aware evidence and dynamic evaluation

**Target:** Nature Machine Intelligence Article.  
**Fallback:** npj Artificial Intelligence Article or a reliability/evaluation venue.

**Current level:** `R1_TO_R2_REFERENCE_DESIGN`.

**Before R4:** dependence positive/negative controls; test/oracle adequacy; robustness/discordance; assurance/argumentation parent product; governed-data and participation boundaries; performative evaluation; blinded evaluator study.

### P-E — Opportunity discovery

**Target if it survives:** Nature Computational Science Article.  
**Fallback:** npj Artificial Intelligence Article; default merge into P-C.

**Current level:** `R0_TO_R1_CONTINGENT`.

**Before R4:** prospective time-sliced evaluation; expert queue-admission; independent future-value evidence; severe discriminator quality; false novelty/noise controls; source authorization; opportunity authority separation.

### P-F — Machine-native scientific intelligence

**Target if it survives:** Nature Machine Intelligence Article.  
**Fallback:** TMLR, Artificial Intelligence journal or another venue matching the eventual empirical contribution.

**Current level:** `R0_PROSPECTUS`.

**Before R4:** human-positive/neutral/trap strata; strongest domain-native algorithm; compute/resource curves; causal mechanism ablation; external witness sufficiency; numerical/oracle validity; leakage/underspecification controls; cross-domain transfer.

## 6. Field-foundation gate versus publication gate

A field can be scientifically plausible before every paper is published, but it is not responsibly described as founded inside this programme until:

- F0–F3 have been instantiated and compared;
- at least one cross-parent proposition has prospective and cross-domain support beyond F0;
- native parent recovery passes;
- the result survives external hostile demarcation;
- a reproducible benchmark/curriculum/research object exists;
- the flagship presents a bounded claim and explicit contraction terminal.

Even then, “founded” is a scholarly community outcome, not a local Boolean generated by ORION.

## 7. Current programme terminal

```text
FLAGSHIP = R1_PROVISIONAL_FIELD_HYPOTHESIS
P_A = R1_DESIGN
P_B = R1_DESIGN
P_C = R1_TO_R2_REFERENCE_DESIGN
P_D = R1_TO_R2_REFERENCE_DESIGN
P_E = R0_TO_R1_CONTINGENT
P_F = R0_PROSPECTUS
TOP_TIER_SUBMISSION_READY = NONE
SECOND_TIER_SUBMISSION_READY = NONE
FIELD_FOUNDED = NO
EXTERNAL_ACCEPTANCE_AUTHORITY = NONE
```
