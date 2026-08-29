# Dependence-Aware Evidence and Dynamic Evaluation for AI-Driven Science
## Correlated Support, Evaluator Sensitivity and Environment Response

## Abstract

AI-assisted science increasingly aggregates evidence from multiple agents, models, datasets, retrieval systems and evaluators. Apparent agreement can overstate evidence when these routes share hidden common causes, while an evaluator that is valid before deployment can become invalid after optimization or strategic response changes the data-generating environment. We study these as two scientific-assurance problems and test whether a common validity interface adds decision value beyond strong dependence, provenance, calibration and performative-evaluation methods. The representation keeps support topology, known and unknown dependence, evaluator sensitivity, environment epoch and response, reopening obligations and authority distinct. The study includes copied-source, shared-model/data/instrument, genuinely independent, misspecified-dependence, static-environment and performative-response cases. Primary outcomes are false corroboration, calibration or decision error, over-conservative rejection, evaluator invalidation, selective reopening and resource cost. The unified account is a hypothesis rather than an assumption: mature dependence methods, mature performative-evaluation methods, or a split into separate theories are predeclared scientific outcomes.

## 1. Introduction

Scientific evidence is often summarized by how many sources, models, agents or experiments agree. In machine-mediated research, that count can be deeply misleading.

Ten agents may share the same foundation model. Separate literature summaries may trace back to the same paper or retrieval corpus. Different validators can depend on the same benchmark oracle. Independent-looking laboratories can share calibration standards, analysis software or a common upstream dataset. Agreement can therefore increase without a corresponding increase in independent information.

A second problem appears when evaluation changes the system being evaluated. A benchmark, scoring rule, policy or deployment decision can alter behavior, sampling, data collection or incentives. An evaluator that was appropriate before optimization may no longer measure the same scientific object after the environment responds.

Neither problem is new. Statistics has mature theories for clustered and correlated evidence, hierarchical modeling and dependent effect sizes. Provenance records shared ancestry. Measurement, testing and assurance theory ask which failures an evaluator can detect. Performative prediction, strategic classification, distribution shift and Goodhart-like effects study feedback between evaluation and behavior. Multi-agent reliability research likewise analyzes correlated agents and shared failure modes.

The open question is narrower:

> **Can a scientific-assurance system use explicit dependence, evaluator sensitivity and environment response to improve validity and reopening decisions—and does representing these together add value beyond applying the strongest parent methods separately?**

The paper therefore has two primary lanes and one optional synthesis. The dependence lane asks whether apparently redundant evidence is counted appropriately without discarding genuinely independent support. The dynamic lane asks whether evaluator validity is rechecked when deployment or optimization changes the environment. The joint lane survives only if their interaction changes a protected scientific decision beyond the two parent pipelines run separately.

## 2. Dependence-aware evidence

Let evidence for a claim \(q\) be represented as

\[
\mathcal E_q=(E,G,U,S,P,T,K),
\]

where \(E\) contains evidence items, \(G\) observed provenance/dependence relations, \(U\) unresolved or latent dependence information, \(S\) support or attack relations, \(P\) a statistical parent model when justified, \(T\) source/epoch state and \(K\) an external authority boundary.

The graph \(G\) is not itself a confidence score. Different dependence structures require different scientific treatment. An exact duplicate, a shared dataset, a common model checkpoint, a shared instrument calibration and a partially shared assumption do not imply the same loss of information.

### 2.1 Dependence classes

The evaluation distinguishes:

- exact duplicate or copied evidence;
- shared source document;
- shared retrieval corpus;
- shared model or checkpoint;
- shared training or evaluation data;
- shared instrument or calibration;
- shared laboratory, analyst or institution;
- common assumptions or bridge results;
- partial dependence;
- genuinely independent support;
- unknown or unidentifiable dependence.

Unknown dependence is not silently mapped to either independence or full dependence. It is represented as an unresolved state or sensitivity range when it can materially change the decision.

### 2.2 Source count is a baseline, not assurance

A simple corroboration count is

\[
N_q=|\{e_i:e_i\text{ supports }q\}|.
\]

This quantity can be useful descriptively but does not encode shared information. Where a probabilistic model is warranted, the analysis uses the strongest appropriate hierarchical, clustered or common-cause parent. Where such a model is not justified, the system retains partial ordering, sensitivity analysis or unresolved dependence rather than inventing an “effective number of independent sources.”

The proposed interface contributes no new statistical estimator by itself. Its purpose is to bind dependence evidence to the scientific decision and reopening consequences.

## 3. Evaluator sensitivity

An evaluator is represented as

\[
V=(v,\mathcal F,\mathcal D,\eta,t,s),
\]

where \(v\) is evaluator identity/version, \(\mathcal F\) the failure classes it can detect, \(\mathcal D\) the operating domain, \(\eta\) known sensitivity/specificity or partial adequacy information, \(t\) the epoch and \(s\) source/custody state.

A pass supports only the error classes the evaluator had a warranted ability to expose. If a benchmark, test suite or measurement procedure is insensitive to a critical failure, passing it does not license a broad absence claim.

This distinction separates evaluator identity from evaluator adequacy. Reproducibly running the same invalid test is not independent validation.

## 4. Environment response and performativity

Let the scientific or operational environment at epoch \(t\) be \(\mathcal P_t\). Deployment or evaluation can induce

\[
\mathcal P_{t+1}
=\Gamma(\mathcal P_t,a_t,\theta_t),
\]

where \(a_t\) is the deployed action/evaluation and \(\theta_t\) the relevant system or population state.

An evaluator calibrated under \(\mathcal P_t\) is not automatically valid under \(\mathcal P_{t+1}\). The relevant question is which estimands, tests and support relations remain invariant after the response.

A transition record therefore includes the old environment/evaluator identity, the intervention or deployment, the observed or modeled response, the new environment identity, which evaluations remain valid, and which earlier conclusions require revalidation.

The paper does not propose a new generic theory of performative prediction. It asks how evaluator change interacts with scientific evidence and reopening.

## 5. A candidate joint validity context

The strongest synthesis hypothesis represents the current assurance context as

\[
A_t=(\mathcal E_t,V_t,\mathcal P_t,D_t,R_t,K_t),
\]

where \(\mathcal E_t\) is evidence/dependence state, \(V_t\) evaluator state, \(\mathcal P_t\) environment state, \(D_t\) the registered scientific decision, \(R_t\) revalidation or reopening obligations, and \(K_t\) authority boundary.

This object earns scientific credit only if the interaction among these components changes a protected decision beyond applying the strongest dependence and dynamic-evaluation parents separately. If not, \(A_t\) is merely a bookkeeping product and the unified thesis contracts.

## 6. Selective reopening

A source retraction, newly discovered common cause, evaluator failure or environment shift can weaken earlier conclusions. But invalidation should not automatically trigger global reset.

When complete sufficient support families are explicitly represented, a conclusion can remain if at least one complete valid support route survives. A conclusion reopens only when every complete sufficient support family has lost a required element under the current validity context.

This reopening rule is inherited from explicit support-family semantics and belief-revision/truth-maintenance reasoning. P-D uses it to connect evidence/evaluator changes to downstream scientific decisions; it does not claim a new general theorem of belief revision.

## 7. Study design

The study contains known-answer and hostile cases in which the evaluator has access to the true or registered dependence/environment structure while solver arms receive only their allowed observations.

The primary independent unit is the registered evidence/evaluator/environment case. Multiple sources or agents within one case are scientifically dependent objects and are not counted as independent replicates.

### 7.1 Dependence cases

Cases include copies, shared hidden sources, common models/checkpoints, shared data, shared calibration, partial dependence, bridge dependence, clustered laboratories, genuine independence and unresolved dependence.

### 7.2 Misspecified-dependence cases

Dependence-aware systems can fail when their own dependence model is wrong. The benchmark therefore includes spurious dependence edges, missing common causes, wrong dependence strength, provenance relations irrelevant to the scientific estimand and independent evidence incorrectly collapsed.

### 7.3 Evaluator cases

Evaluators include exact oracles, partial oracles, invariant/metamorphic checks, evaluators blind to one critical error, version/epoch changes and unavailable evaluators.

### 7.4 Static-environment controls

Some episodes are constructed so that deployment does not change the relevant generating process. A response-aware method should not hallucinate performativity or trigger unnecessary revalidation.

### 7.5 Performative-response cases

Other cases include prospectively specified response mechanisms affecting case mix, user behavior, data collection, strategic behavior, measurement or research incentives.

## 8. Comparator conditions

### Dependence lane

Comparators include:

- source count or majority;
- provenance deduplication;
- nominal agent/model diversity;
- strongest applicable statistical dependence model;
- strongest evidence-synthesis parent;
- a parent federation;
- the candidate interface.

### Dynamic lane

Comparators include:

- static evaluator reuse;
- periodic recalibration;
- strongest performative-prediction or response-aware parent applicable to the case;
- dynamic parent federation;
- the candidate interface.

### Joint lane

The decisive comparator applies the strongest dependence pipeline and the strongest dynamic/evaluator pipeline **separately** and composes their final scientific decisions. The unified state is credited only for incremental decision value beyond this composition.

## 9. Evaluation

Dependence outcomes include false corroboration, calibration or decision error under known dependence, sensitivity to misspecification, preservation of genuinely independent support and correct unknown-dependence handling.

Dynamic outcomes include error under static-environment controls, validity after environment response, evaluator revalidation correctness and selective reopening.

The joint outcome is the incremental protected decision value of the unified interface over the separate parent pipelines, together with resource overhead and overconservatism.

These quantities are not collapsed into one assurance score. A system that reduces false corroboration by rejecting genuinely independent evidence can be scientifically worse despite appearing conservative.

## 10. Results

**Authoring placeholder — blocks arXiv release until receipt-bound Results are inserted.**

The final Results section will use this fixed evidence order:

1. **Known-dependence calibration.** Compare naive agreement/source count, provenance controls and strong dependence parents.
2. **Misspecification and unknown dependence.** Test whether dependence-aware methods remain safe when the graph/model is wrong or incomplete.
3. **Independent-support preservation.** Verify that the method does not turn caution into blanket evidence rejection.
4. **Static-environment controls.** Establish the false-positive cost of response-aware evaluation.
5. **Performative-response cases.** Test whether evaluator validity/reopening changes correctly after a registered environment response.
6. **Joint discriminator.** Compare the unified interface with the strongest separate dependence+dynamic parent pipelines.
7. **Resource/overconservatism analysis and adverse cases.** Keep them visible in the main interpretation.

No unified-theory conclusion is selected before these results exist.

## 11. Interpretation branches

### Joint assurance residual

Supported only if the unified representation changes protected validity/reopening decisions beyond strongest separate parent methods without unacceptable overconservatism or resource cost.

### Dependence parent sufficient

If mature statistical/provenance methods resolve the dependence lane and the common interface adds no decision value, that component contracts.

### Dynamic parent sufficient

If performative/response-aware parents resolve evaluator shifts without the joint object, the dynamic component contracts.

### Split result

If both parent lanes are useful but their joint representation adds no interaction value, the manuscript should split conceptually or become a comparative assurance study rather than claim one new validity object.

### Adverse overconservatism

If the method frequently rejects genuinely independent evidence or triggers needless revalidation in stable settings, that cost is a central negative result.

## 12. Discussion

AI-assisted science makes dependence unusually easy to hide. Distinct agents, prompts or reports can share the same model, corpus, benchmark and calibration chain. Counting agreement without tracing these shared causes can create false corroboration. Yet the opposite mistake—treating all shared provenance as redundancy—throws away legitimate information.

Evaluation introduces a second time-dependent risk. Systems adapt to tests, deployment changes populations, and incentives reshape data generation. Scientific assurance therefore needs to know not only *where evidence came from* but *whether the evaluator still tests the same claim under the current environment*.

A positive joint result would support an assurance workflow that links these questions because they interact in downstream reopening. A parent-sufficiency result would be equally valuable: it would show that dependence analysis and dynamic evaluation should remain separate mature tools connected by ordinary workflow rather than a new unified theory.

The strongest limitation is model misspecification. Neither a dependence graph nor a response model is guaranteed to capture every common cause or behavioral feedback. The framework therefore treats unknown dependence, evaluator insufficiency and `CANNOT_CHECK` as scientific states rather than forcing precise confidence from incomplete structure.

## 13. Conclusion

Agreement is not independence, and evaluator validity is not permanent. Both facts are well known individually. This study asks whether representing them together improves the scientific decisions made by AI-assisted research systems.

The answer is intentionally empirical. If separate mature methods make the same decisions, use them separately. If a common validity context adds protected decision value while preserving independent evidence and avoiding false performativity, the joint interface earns a bounded contribution. If it creates blanket distrust or bookkeeping without consequence, contract it.

The paper therefore evaluates assurance by the correctness of scientific decisions and reopening—not by the amount of metadata collected about evidence or evaluators.

## Reproducibility and release note

The final public version will bind each evidence/evaluator/environment case to its frozen generative structure, solver-visible inputs, arm outputs, analysis-ready snapshot, result receipt and source-data object. Internal project-development identifiers remain outside manuscript-facing prose.
