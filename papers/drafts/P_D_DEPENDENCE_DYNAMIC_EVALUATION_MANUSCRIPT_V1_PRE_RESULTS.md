# When Agreement Is Not Independent and Evaluation Changes the System
## Dependence-Aware Evidence and Dynamic Evaluation in AI-Assisted Science

**Paper ID:** P-D  
**Status:** science/method manuscript complete before protected dependence/performative outcomes.  
**Primary target hypothesis:** Nature Machine Intelligence Article.  
**Fallback:** npj Artificial Intelligence Article.  
**Unification status:** hypothesis only; dependence and performativity may split/contract.

## Abstract

AI-assisted science increasingly aggregates evidence from multiple agents, models, datasets, retrieval systems and evaluators. Apparent agreement can overstate evidence when these routes share hidden common causes, while an evaluator that is valid before deployment can become invalid after optimization or strategic response changes the data-generating environment. We study these as two candidate scientific-assurance problems and test whether a common validity interface adds protected decision value beyond strongest dependence, provenance, calibration and performative-evaluation parents. The proposed interface represents support topology, known and unknown dependence, evaluator sensitivity, environment epoch/response and authority separately. The protected study includes copied-source, shared-model/data/instrument, genuinely independent, mis-specified-dependence, static-environment and performative-response cases. Primary outcomes are false corroboration, calibration, over-conservative rejection, evaluator invalidation, selective reopening and resource cost. The manuscript explicitly allows three null outcomes: mature dependence methods suffice, mature performative-evaluation methods suffice, or the two problems should remain separate. No empirical prevalence or unified-theory claim is made before protected results.

---

# 1. Introduction

Scientific evidence is often counted as though distinct observations, papers, models or reviewers were independent. In machine-mediated research this assumption is increasingly unsafe.

Ten agents can share a foundation model. Independent-looking literature summaries can originate from the same source or retrieval corpus. Different validators can share training data or a benchmark oracle. Separate laboratories can share calibration standards, instruments or protocols. A consensus score can therefore grow without a corresponding increase in independent information.

A second failure appears when evaluation affects what it evaluates. A benchmark, policy, scoring rule or deployment decision can alter the population, behavior or data-generating process. The evaluator that was valid before optimization may no longer measure the same scientific object afterwards.

P-D asks two questions:

1. **Can dependence-aware evidence control improve scientific calibration without discarding genuinely independent support?**
2. **Can response-aware evaluation detect when the evaluator/environment relationship has changed?**

A stronger third question is deliberately uncertain:

> **Do these problems benefit from one common scientific-validity interface, or should they remain separate parent theories?**

The paper survives only if a protected residual exists beyond strongest existing methods. A clean split into two parent-sufficient results is a valid outcome.

---

# 2. Parent theories and claim ceiling

## 2.1 Dependence and correlated evidence

Statistics already studies correlated observations, clustered data, dependent effect sizes, hierarchical models, common-method bias and robust variance. Graphical models and latent-variable models formalize common causes. Ensemble and multi-agent research studies diversity and correlation. Provenance systems identify shared ancestry. Evidence synthesis and meta-analysis explicitly handle dependence in many settings.

P-D therefore cannot claim that “agreement is not independence” is new.

## 2.2 Provenance and lineage

Provenance exposes where evidence came from but does not automatically specify the statistical or scientific consequence of shared lineage. Two results can share a source without being fully redundant, or arise from different sources while sharing a hidden model or calibration.

The contribution, if any, must therefore be a decision-level use of dependence information, not a new provenance format.

## 2.3 Calibration and evaluator adequacy

Measurement theory, software testing, severe testing, validation and assurance already ask whether an evaluator can expose the relevant failure. Benchmark identity alone does not establish sensitivity to every claim.

## 2.4 Performative and strategic response

Performative prediction, Goodhart-like effects, distribution shift, strategic classification and adaptive systems already study feedback between models/evaluators and the environments they influence. P-D cannot claim novelty for evaluator-induced distribution change.

## 2.5 Authority

Statistical evidence and evaluator scores do not create permission to act or publish. Authority remains externally supplied and must not be conflated with evidence aggregation.

## 2.6 Claim ceiling

P-D does **not** claim:

- distinct agents imply independent evidence;
- all shared provenance implies full redundancy;
- unknown dependence equals dependence or independence;
- every evaluator is performative;
- a statistical evidence model creates institutional authority;
- dependence and performativity necessarily form one theory.

The possible residual is a protected **scientific assurance interface** that improves decisions across these problems beyond the strongest parent composition.

---

# 3. Dependence-aware evidence object

Let evidence item `e_i` support or attack scientific claim `q`. Represent the evidence collection as

\[
\mathcal E_q=(E,G,U,S,P,T,K),
\]

where:

- `E` — evidence items;
- `G` — observed dependence/provenance graph;
- `U` — registered latent/common-cause uncertainty or unknown-dependence variables;
- `S` — support/attack relations to claims;
- `P` — probabilistic/statistical parent model where justified;
- `T` — epoch/source version;
- `K` — authority/governance boundary.

The graph alone is not a confidence score. Its scientific use is parent-specific.

## 3.1 Dependence classes

Benchmark cases include:

- exact duplicate/copy;
- shared source document;
- shared retrieval corpus;
- shared model/checkpoint;
- shared training or evaluation data;
- shared instrument/calibration;
- shared analyst/laboratory/institution;
- partial/shared assumption;
- bridge dependence through a common intermediate result;
- genuinely independent control;
- unknown/unidentifiable dependence.

## 3.2 Unknown dependence

If dependence is scientifically relevant but cannot be identified from available information, the correct state is not “independent.” Use an explicit uncertainty/`CANNOT_CHECK_DEPENDENCE` terminal or sensitivity range.

---

# 4. Evidence adequacy versus source count

A naive corroboration score may use

\[
N_q=|\{e_i:e_i\text{ supports }q\}|.
\]

P-D treats this only as a baseline.

The scientifically relevant object is the support under a registered dependence model or sensitivity set. Where a probabilistic model is justified, estimate the target quantity using the strongest appropriate hierarchical/cluster/common-cause parent. Where it is not, retain partial order/sensitivity or unknown-dependence state rather than invent an “effective sample size.”

The candidate ORION-specific interface contributes no new estimator by itself.

---

# 5. Evaluator and test-sensitivity state

Let an evaluator be

\[
V=(v,\mathcal F,\mathcal D,\eta,t,s),
\]

where:

- `v` — evaluator identity/version;
- `F` — detectable failure/error classes;
- `D` — domain/operating region;
- `eta` — known sensitivity/specificity or partial adequacy information;
- `t` — epoch;
- `s` — source/custody/provenance state.

A pass supports absence only for the registered failure classes the evaluator can detect with warranted sensitivity.

If the evaluator is insensitive to a critical failure mode, `PASS` does not justify the broader absence claim.

---

# 6. Dynamic / performative environment

Let the data-generating environment at epoch `t` be

\[
\mathcal P_t.
\]

An evaluated system, policy or publication may induce an environment response

\[
\mathcal P_{t+1}=\Gamma(\mathcal P_t,a_t,\theta_t),
\]

where `a_t` is deployment/action and `theta_t` relevant system or population state.

A static evaluator calibrated under `P_t` is not automatically valid under `P_{t+1}`.

Define an evaluator-transition receipt

```text
old environment/evaluator identity
intervention/deployment
observed or modeled response
new environment identity
which estimands remain invariant
which tests require revalidation
which conclusions must reopen
```

This is an interface for parent methods, not a new theory of performativity.

---

# 7. Candidate joint assurance object

The strongest synthesis hypothesis is that dependence and evaluator response can be represented as a common **validity context**

\[
A_t=(\mathcal E_t,V_t,\mathcal P_t,D_t,R_t,K_t),
\]

where:

- `E_t` — evidence/dependence state;
- `V_t` — evaluator state;
- `P_t` — environment/generating state;
- `D_t` — registered scientific decision;
- `R_t` — reopening/revalidation obligations;
- `K_t` — authority boundary.

A scientific decision is evaluated relative to this context. The unification earns scientific credit only if it changes protected decisions beyond applying dependence and performative parent methods separately.

If not, `A_t` is only a bookkeeping product and P-D should split or contract.

---

# 8. Selective reopening under evidence/evaluator change

A conclusion may need re-evaluation when:

- a shared source is retracted;
- a model/data dependency is discovered;
- evaluator sensitivity was overstated;
- the evaluated environment changes;
- a calibration epoch expires.

But reopening should be selective. If an independently sufficient support family survives under a still-valid evaluator/context, the conclusion may remain.

P-D reuses the explicit sufficient-support-family semantics from the P-B interface where applicable; it does not claim a new universal belief-revision theorem.

---

# 9. Protected benchmark design

## 9.1 Dependence known-answer cases

Synthetic/exact cases include:

- copied evidence;
- shared hidden source;
- shared model/checkpoint;
- shared dataset;
- shared calibration;
- clustered laboratories;
- one bridge result reused by several claims;
- genuinely independent evidence;
- partial dependence;
- unknown dependence.

Where possible, ground-truth generative structures are known to the evaluator but hidden from solver arms.

## 9.2 Mis-specified-dependence cases

Dependence-aware methods can be harmful when the dependence model is wrong. Include:

- false positive dependence edges;
- missing common cause;
- dependence strength mis-specified;
- provenance correlation that is scientifically irrelevant;
- independent evidence wrongly collapsed.

## 9.3 Evaluator-sensitivity cases

- exact/complete oracle;
- partial oracle;
- metamorphic/invariant oracle;
- evaluator blind to one critical failure;
- evaluator version/epoch change;
- invalid or unavailable evaluator.

## 9.4 Static-environment negative controls

Deployment/action does not change the relevant generating process. Response-aware methods should not invent performativity.

## 9.5 Performative-response cases

The evaluated system or policy changes:

- case mix;
- user behavior;
- data collection;
- strategic response;
- model inputs;
- measurement process;
- research incentives.

The exact mechanism is frozen before outcomes.

---

# 10. Comparator arms

Dependence lane:

- source count/majority;
- provenance deduplication;
- diversity by agent/model identity;
- strongest statistical dependence model;
- strongest evidence-synthesis parent;
- parent federation;
- candidate interface.

Evaluator/performativity lane:

- static evaluator;
- distribution-shift/recalibration parent;
- performative/strategic parent;
- strongest federation;
- candidate interface.

Unified lane:

- two independent parent pipelines;
- one shared candidate validity context.

All receive information-matched evidence and frozen resources.

---

# 11. Outcomes

## Dependence

- false corroboration / over-counting;
- calibration or decision error;
- genuinely independent evidence retained;
- over-conservative rejection;
- unknown-dependence calibration;
- support/reopening decision.

## Evaluator/performativity

- detection of invalid evaluator scope;
- false performativity flag;
- missed environment response;
- post-response calibration/decision error;
- correct revalidation/reopening.

## Unified assurance

Primary discriminator:

> Does the joint interface make a protected scientific validity/reopening decision that the strongest separate dependence + provenance + performative-evaluation parents do not, under the same information/resources?

If no, PD-C4 fails and the paper should split/contract.

## Resources

Report compute/tool calls, evaluator cost, human adjudication, latency and implementation burden.

---

# 12. Analysis plan

The independent unit is the case or scientific decision, not evidence items within one dependence cluster.

Report paired comparisons, calibration curves where appropriate, case-level critical errors, dependence-strength strata, unknown-dependence outcomes, stable-versus-performative strata, and resource Pareto fronts.

Sensitivity analysis is mandatory for:

- dependence graph errors;
- dependence strength;
- evaluator sensitivity assumptions;
- environment response strength;
- missingness/invalid cases;
- resource normalization.

A favorable result under one dependence graph is insufficient if reasonable alternatives reverse it.

---

# 13. Results insertion contract

Protected Results may populate only:

1. sample/case flow;
2. dependence calibration and false corroboration;
3. over-conservative rejection;
4. unknown-dependence outcomes;
5. evaluator adequacy;
6. static/performative outcomes;
7. unified-versus-separate parent decisions;
8. reopening decisions;
9. resource outcomes;
10. robustness.

No importer may write “unified theory supported” from separate positive lane results without the registered joint discriminator.

---

# 14. Outcome-conditioned Discussion branches

## Unified residual survives

Claim only the tested assurance residual: explicit dependence, evaluator state and environment response jointly changed protected scientific decisions beyond strongest separate parents. Do not generalize to all scientific evidence.

## Dependence lane positive, performativity lane parent-sufficient

Contract P-D to dependence-aware scientific evidence or merge dynamic-evaluation material into the flagship/P-C.

## Performativity lane positive, dependence lane parent-sufficient

Contract to dynamic scientific evaluation or merge dependence background into strongest parent discussion.

## Both lanes parent-sufficient

Conclude that the shared interface is engineering/bookkeeping only. Do not maintain a standalone scientific paper.

## Dependence-aware method becomes overconservative

Report this as a scientific failure. Preventing false corroboration by discarding genuinely independent evidence is not a successful assurance mechanism.

## Dependence not identifiable

Preserve `CANNOT_CHECK` or sensitivity ranges; do not impute independence for convenience.

---

# 15. Limitations

1. Dependence structures may be only partially observable.
2. Statistical dependence is not identical to epistemic dependence or common scientific assumptions.
3. Provenance edges can be scientifically irrelevant, and distinct provenance can still conceal shared causes.
4. Performative response may be slow, strategic or confounded.
5. Evaluator sensitivity is itself uncertain and can change.
6. Authority remains separate from statistical support.
7. A unified state object can create false coherence if the two lanes have no shared decision mechanism.

---

# 16. Reproducibility and AI-use

Release synthetic generative cases, frozen dependence/evaluator graphs, parent model specifications, arm identities, exact/native evaluators, analysis scripts, sensitivity analyses, invalid-case ledger and resource accounting where permitted.

AI systems have been used extensively for research assistance in the ORION-V2 programme. Human authors must verify the statistical, causal, evaluation and literature claims and comply with the target journal's current AI-use policy.

---

# 17. Current paper terminal

```text
P_D_SCIENCE_CONTENT = COMPLETE_PRE_RESULTS
PD_C1 = PARENT_THEORY
PD_C2 = PARENT_THEORY
PD_C3 = BLOCKED_PROTECTED_RESULTS
PD_C4 = EXPLICIT_UNIFICATION_HYPOTHESIS_WITH_TWO_PIPELINE_CONTROL
RESULTS = NOT_YET_AUTHORIZED
SPLIT_OR_CONTRACTION = PREAUTHORIZED_IF_NO_JOINT_RESIDUAL
PRIMARY_TARGET = NATURE_MACHINE_INTELLIGENCE_ARTICLE_HYPOTHESIS
FALLBACK = NPJ_ARTIFICIAL_INTELLIGENCE_ARTICLE
```

The paper survives as one Article only if the joint validity object adds protected decision value beyond strongest separate parents.
