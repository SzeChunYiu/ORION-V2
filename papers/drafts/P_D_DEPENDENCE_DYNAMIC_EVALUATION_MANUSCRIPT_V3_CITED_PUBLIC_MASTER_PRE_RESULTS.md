# When Agreement Is Not Independent and Evaluation Changes the System
## Dependence-Aware Evidence and Dynamic Evaluation in AI-Assisted Science

## Abstract

AI-assisted science increasingly aggregates evidence from multiple agents, models, datasets, retrieval systems and evaluators. Apparent agreement can overstate evidence when these routes share hidden common causes, while an evaluator that is valid before deployment can become invalid after optimization or strategic response changes the data-generating environment. Both problems already have mature parents: dependence-aware statistics, provenance, measurement validation, performative prediction and adaptive evaluation. We therefore test a narrower hypothesis: whether an explicit validity interface combining dependence topology, evaluator sensitivity and environment-response state changes protected scientific decisions beyond applying the strongest parent methods separately. The benchmark includes duplicate/shared-source, shared-model/data/instrument, genuinely independent, mis-specified-dependence, evaluator-blindness, static-environment and performative-response cases. Primary outcomes are false corroboration, over-conservative rejection, evaluator invalidation, selective reopening, joint-decision residual and resource cost. A unified paper is supported only if the joint interface adds decision value beyond the strongest separate dependence and dynamic-evaluation pipelines. Dependence-only benefit, performativity-only benefit, two-parent sufficiency, over-conservatism and `CANNOT_CHECK` are prespecified outcomes.

## 1. Introduction

Scientific evidence is often counted as though distinct observations, papers, models or reviewers were independent. In machine-mediated research that assumption is increasingly unsafe. Ten agents can share one foundation model. Independent-looking literature summaries can originate from the same source or retrieval corpus. Different validators can share training data, a benchmark oracle or an instrument calibration. Consensus can therefore increase without a corresponding increase in independent information.

This concern is not new. Statistical methods already address clustered and correlated observations, common causes and dependent evidence; provenance exposes shared ancestry [@moreau2013provenance]. Recent LLM multi-agent theory makes the limit especially clear: without new exogenous signals, delegated multi-agent networks cannot manufacture new decision information from a shared information state [@ao2026reliability]. Empirical work likewise shows that answer-level agreement can conceal reasoning misalignment [@wang2026consistency].

A second failure arises when evaluation affects what it evaluates. Performative prediction formalizes feedback in which deployment changes the data distribution [@perdomo2020performative]. Recent theory treats reward hacking under finite evaluation as a structural consequence of incomplete evaluative coverage under optimization [@wang2026rewardhacking], and production-oriented benchmarks such as AlphaEval explicitly address evolving, heterogeneous evaluation criteria for agent systems [@lu2026alphaeval].

Accordingly, this paper does not claim that consensus can be dependent or that evaluators can be gamed. It asks:

> **Does explicitly representing dependence topology, evaluator sensitivity and environment response improve scientific validity and reopening decisions beyond the strongest separate parent pipelines?**

A positive unified result must outperform the product of strong dependence-aware and dynamic-evaluation methods. Otherwise the two problems should remain separate.

## 2. Dependence-aware evidence

Let evidence item `e_i` support or attack scientific claim `q`. Represent the evidence collection as

\[
\mathcal E_q=(E,G,U,S,P,T,K),
\]

where `E` are evidence items, `G` observed dependence/provenance relations, `U` registered uncertainty about latent/common causes, `S` support/attack relations, `P` a probabilistic/statistical parent model where scientifically justified, `T` source/epoch and `K` authority/governance constraints.

The graph is not a confidence score. Its scientific use is parent-specific.

### 2.1 Registered dependence classes

Benchmark cases include:

- exact duplicate/copy;
- shared source document;
- shared retrieval corpus;
- shared model/checkpoint;
- shared training or evaluation data;
- shared instrument/calibration;
- shared analyst/laboratory/institution;
- bridge dependence through a common intermediate result;
- genuinely independent support;
- partial or unknown dependence.

Unknown dependence is not silently treated as independence. When dependence matters but cannot be identified, the valid outcome is a sensitivity analysis or `CANNOT_CHECK_DEPENDENCE`.

## 3. Evidence adequacy versus source count

A naive corroboration score

\[
N_q=|\{e_i:e_i\text{ supports }q\}|
\]

is used only as a baseline.

Where a statistical dependence model is justified, the strongest appropriate parent model estimates the relevant evidence quantity using the declared clustering/common-cause structure. Where such a model is not justified, the benchmark preserves partial-order, sensitivity or unknown-dependence states rather than inventing an “effective sample size.”

The proposed interface contributes no new estimator merely by recording provenance.

## 4. Evaluator sensitivity

Let an evaluator be

\[
V=(v,\mathcal F,\mathcal D,\eta,t,s),
\]

where `v` is identity/version, `F` detectable failure classes, `D` domain/operating region, `eta` known sensitivity/specificity or partial adequacy information, `t` epoch and `s` source/custody state.

A pass supports absence only for the failure classes the evaluator can detect with warranted sensitivity. A benchmark can be reproducible and still be scientifically inadequate for the claim it is used to certify. Severe-testing logic motivates this restriction [@mayo1996error].

## 5. Dynamic and performative evaluation

Let the environment at epoch `t` be

\[
\mathcal P_t.
\]

A deployed system or policy can induce

\[
\mathcal P_{t+1}=\Gamma(\mathcal P_t,a_t,\theta_t),
\]

where `a_t` is action/deployment and `theta_t` relevant system/population state.

An evaluator calibrated under `P_t` is not automatically valid under `P_{t+1}`. This is a direct parent problem of performative/adaptive evaluation [@perdomo2020performative], not a new Machine-Epistemics theorem.

The benchmark records:

- old environment/evaluator identity;
- deployment/intervention;
- observed or modelled response;
- new environment identity;
- estimands that remain invariant;
- tests requiring revalidation;
- conclusions requiring reopening.

## 6. Candidate joint validity context

The strongest synthesis hypothesis represents

\[
A_t=(\mathcal E_t,V_t,\mathcal P_t,D_t,R_t,K_t),
\]

where `E_t` is evidence/dependence state, `V_t` evaluator state, `P_t` environment state, `D_t` registered scientific decision, `R_t` reopening/revalidation obligations and `K_t` authority boundary.

This object earns standalone scientific credit only if it changes protected decisions beyond applying the strongest dependence and dynamic-evaluation methods separately. Otherwise it is bookkeeping.

## 7. Selective reopening

A conclusion can require re-evaluation when a shared source is retracted, a hidden dependency is discovered, evaluator sensitivity was overstated or the evaluated environment changes. Reopening should nevertheless be selective. If an independently sufficient support family survives under a still-valid evaluator/context, the conclusion may remain.

The sufficient-support semantics are explicit and bounded. This paper does not claim a new universal belief-revision theorem.

## 8. Benchmark design

### 8.1 Dependence cases

Known-answer cases include copied evidence, shared hidden source, shared model/checkpoint, shared dataset, shared calibration, clustered laboratories, one bridge result reused by several claims, genuine independence, partial dependence and unknown dependence.

### 8.2 Mis-specified dependence

Dependence-aware methods can be harmful when the dependence model is wrong. Cases therefore include false positive dependence edges, missing common causes, mis-specified dependence strength, scientifically irrelevant provenance overlap and independent evidence wrongly collapsed.

### 8.3 Evaluator-sensitivity cases

The suite includes exact/complete oracles, partial oracles, metamorphic/invariant evaluators, an evaluator blind to one critical failure class, evaluator version/epoch changes and unavailable evaluators.

### 8.4 Static-environment controls

Some deployments do not change the relevant generating process. Response-aware methods must not invent performativity.

### 8.5 Performative-response cases

Other cases change case mix, user behaviour, data collection, strategic response, model inputs, measurement process or research incentives. The response mechanism is frozen before outcomes.

## 9. Comparator arms

Dependence lane:

- source count/majority;
- provenance deduplication;
- identity-diversity heuristics;
- strongest statistical dependence model;
- strongest evidence-synthesis parent;
- parent federation;
- candidate interface.

Dynamic-evaluation lane:

- static evaluator;
- periodic recalibration;
- strongest performative/adaptive-evaluation parent;
- production-style heterogeneous evaluation control [@lu2026alphaeval];
- candidate interface.

Multi-agent reliability limits [@ao2026reliability] and consensus/reasoning divergence [@wang2026consistency] are treated as direct parent pressure, not evidence for the candidate interface.

## 10. Outcomes

Primary outcomes are case-level:

1. false corroboration rate;
2. over-conservative rejection of genuinely independent evidence;
3. dependence sensitivity/calibration;
4. evaluator invalidation detection;
5. false performativity alerts under static controls;
6. missed performative response;
7. selective reopening accuracy;
8. incremental decision value of the joint interface over strongest separate parent pipelines;
9. resource cost.

Unknown-dependence and unavailable-evaluator cases retain explicit `CANNOT_CHECK` outcomes rather than being forced into binary success/failure.

## 11. Results

**[RESULTS BLOCK — populate only from frozen P-D receipts.]**

Results must be reported separately for:

1. dependence-known cases;
2. mis-specified-dependence cases;
3. evaluator-sensitivity cases;
4. static-environment controls;
5. performative-response cases;
6. joint-interface versus strongest separate parent pipelines;
7. resource costs.

Allowed paper-level terminals include:

- `JOINT_ASSURANCE_RESIDUAL`;
- `DEPENDENCE_ONLY_RESIDUAL`;
- `PERFORMATIVITY_ONLY_RESIDUAL`;
- `TWO_PARENT_PIPELINES_SUFFICIENT`;
- `OVERCONSERVATIVE_DEPENDENCE_CONTROL`;
- `NO_SCIENTIFIC_RESIDUAL`;
- `CANNOT_CHECK`.

Separate positive dependence and performativity results do **not** justify a unified paper unless the joint comparator also adds decision value.

## 12. Interpretation

A positive dependence result would show that explicit topology prevents false corroboration without collapsing independent evidence. A positive dynamic-evaluation result would show that response-aware evaluation catches evaluator/environment invalidation beyond static calibration. Neither result alone establishes a unified theory.

The unified claim survives only if the joint validity context makes a scientifically relevant decision that the strongest separate parent pipelines miss. If not, the paper should split or contract.

If dependence modelling improves calibration but causes substantial over-conservative rejection under mis-specified graphs, the result is a trade-off rather than a clean win.

## 13. Limitations

Dependence is often only partially observable. Provenance can be incomplete, and shared ancestry does not imply a known correlation magnitude. Evaluator sensitivity is itself an empirical object and may drift. Performative responses can be slow, strategic or non-identifiable. A benchmark can encode only a subset of real institutional and social feedback mechanisms.

The joint interface also risks becoming a vocabulary for things already handled by separate mature methods. The study is designed so this possibility can win.

## 14. Conclusion

Multi-agent agreement is not independent evidence, and optimization against finite evaluation can distort what an evaluator measures [@ao2026reliability; @wang2026consistency; @wang2026rewardhacking]. Those are parent facts, not the contribution of this paper.

The open question is whether dependence topology, evaluator sensitivity and environment response form a **jointly useful scientific validity state**. If strongest separate parent methods already produce the same decisions, they should remain separate. If a residual survives, it is a bounded result about coordinating evidence and evaluation under change—not a universal theory of trust.

## Transparency

Large language model tools contributed materially to literature discovery, formalization, critique, software and drafting. AI systems are not authors. Human authors must inspect the parent literature, protected results and final claims before public release.

## Bibliography source

Use `papers/primary/PRIMARY_PAPERS_REFERENCES_V1.bib`. Refresh all 2026 source statuses before arXiv and journal release.
