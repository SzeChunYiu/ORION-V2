# Before the Hypothesis
## Prospective Scientific Opportunity Discovery from Anomalies, Encounters and Missing Capabilities

**P-E manuscript V4 — contingent top-tier pre-results Article draft**  
**Primary target archetype if it survives:** multidisciplinary computational-science Article  
**Status:** full evidence-independent manuscript and prospective result structure are complete. Standalone identity remains contingent and merges into P-C by default unless independently measured prospective value survives strongest parents.

## Abstract

Most scientific automation is evaluated after a question has already been chosen. A harder upstream task is deciding which problems, anomalies and unexpected encounters deserve investigation. Existing problem-finding, abduction, literature-based discovery, active learning, anomaly detection, curiosity, open-ended search and research-priority methods already address major parts of this problem, while retrospective stories of famous discoveries create severe hindsight leakage. We study a source-bound opportunity process evaluated prospectively. Candidate opportunities must originate from a contradiction, residual, non-identifiability, unmet need, failed procedure, remote donor, evaluator failure, performative response or unexpected encounter. Novelty, importance, tractability, falsifiability, information gain, option value, noise risk and agenda authority remain separate. A bounded encounter buffer retains off-path events only when the system can state why they are unexpected, connect them to an unresolved problem and propose a discriminator. Candidates are generated under frozen source and tool dates and independently adjudicated before later outcomes are known. The method is compared with expert brainstorming and strongest parent methods. It survives as a standalone paper only if it improves prospective useful-action or result rates without increasing false novelty, noise fixation or authority violations; otherwise it becomes an action-selection component of P-C.

## Introduction

Scientific progress depends not only on solving problems but on selecting, reformulating and sometimes discovering them. An agent can answer a question accurately and still contribute little if the question is duplicate, trivial, unfalsifiable, intractable with available resources or poorly connected to the actual scientific obstruction.

Human and machine accounts of discovery repeatedly show that valuable questions can arise from contradiction, unexplained residuals, measurement failure, practical need, unexpected encounter or a remote structural analogy. Yet these sources are easy to romanticize. Once a discovery is famous, earlier events can be reconstructed as obviously significant. Surprise can be confused with stochastic noise. Topic novelty can be mistaken for scientific importance. A language model can generate endless “interesting directions” with no source-bound problem or decisive follow-up.

Mature parent fields include problem finding, abductive reasoning, literature-based discovery, anomaly detection, Bayesian experimental design, curiosity and intrinsic motivation, novelty search, open-ended learning, R&D portfolio methods, research-priority setting and science-of-science forecasting. P-E does not claim these mechanisms. It asks whether a typed opportunity record plus prospective evaluation improves the decision to open a scientific problem.

The system separates three stages:

`trigger or encounter -> opportunity formulation -> discriminator or preserving action`.

A trigger is not evidence for its explanation. An opportunity is not automatically an agenda item. A high score cannot authorize resource allocation.

## Results architecture

### Source-bound opportunities expose why a problem should exist

Each candidate binds:

`OpportunityRecord = (`
`source_problem, trigger, source_identity, acquisition_mode, current_model_or_practice, inadequacy, candidate_question, alternatives, nearest_parents, novelty_status, importance_hypothesis, tractability, falsifiability, independence, expected_information_gain, option_value, serendipity_value, noise_risk, resources, authority, reasons_not_to_pursue, expiry)`.

Trigger classes include:

- contradiction;
- structured residual/model inadequacy;
- non-identifiability;
- missing source/representation;
- remote structural donor;
- unmet need or capability gap;
- evaluator/benchmark failure;
- performative response;
- unexpected encounter;
- failure residue.

**Primary result slot PE-R1.** Report candidate validity, source-boundness, duplicate rate and actionable-discriminator rate relative to generic LLM questions, expert brainstorming and strongest parent methods.

**Required sentence form:**

> Under the frozen information cutoff, P-E generated [n] candidates, of which [x]% were independently judged source-bound and [y]% contained an actionable discriminator. Duplicate/known-problem rate was [value] versus [comparators].

### Serendipity requires recognition and follow-up, not surprise alone

`SerendipityCandidate = (`
`encounter, unexpected_relative_to, source_identity, anomaly_type, cross_problem_value, recognition_reason, discriminator, cost, authority)`.

A bounded `EncounterBuffer` stores only a predeclared number of off-path events. Repeated noise is compressed. An event receives no truth authority and no priority merely because it is surprising.

Protected pairs include:

- highly surprising but irreproducible noise;
- an inexpensive reproducible anomaly with a useful cross-problem link;
- a famous retrospective case reconstructed after outcome disclosure;
- a genuine prospective encounter frozen before follow-up;
- an apparatus/software artifact;
- a useful practical donor that does not establish scholarly novelty.

**Primary result slot PE-R2.** Report useful encounter recognition, false surprise/noise fixation and retrospective leakage.

**Required sentence form:**

> P-E retained [x] of [y] prospectively useful encounters and discarded [n] noise events at [cost]. Hindsight-exposed cases inflated apparent serendipity by [effect] and were excluded from primary evidence.

### Opportunity value remains multidimensional

The system does not collapse:

- novelty;
- importance;
- tractability;
- falsifiability/discriminability;
- independence;
- information gain;
- option value;
- serendipity value;
- risk and authority.

Candidates can be important but intractable, tractable but trivial, surprising but noisy, or valuable to preserve without immediate execution. The output is a typed portfolio or Pareto surface, not one universal rank.

**Primary result slot PE-R3.** Report calibration and decision reproducibility for each coordinate and compare scalar-rank versus typed-portfolio decisions.

**Required sentence form:**

> Scalar ranking selected [error class] in [n] cases, whereas the typed portfolio preserved [trade-off]. Expert agreement was highest for [coordinates] and lowest for [coordinates].

### Prospective evaluation avoids outcome-conditioned opportunity claims

Before candidate generation, freeze:

- literature/source cutoff;
- source modes and access restrictions;
- models/tools;
- search and encounter-buffer budget;
- parent baselines;
- candidate algorithm;
- expert rubrics;
- follow-up horizon and outcomes.

Experts blinded to system identity independently judge known/duplicate status, scientific importance, tractability, falsifiability, independence, resource requirements and whether the problem should enter a real queue.

Bounded follow-up records whether a candidate leads to a useful scientific action, discriminator, dataset, measurement, theory revision, negative result or explicit blockage. Unresolved and failed candidates remain in the denominator.

**Primary result slot PE-R4.** Report queue-admission, later useful-action/result rate and prospective calibration.

**Required sentence form:**

> At initial blinded review, [x]% of P-E candidates entered the research queue. After the frozen horizon, [y]% produced a useful action or result, compared with [arms]. Negative, duplicate, blocked and unresolved candidates comprised [distribution].

### Strongest parent and expert controls decide standalone survival

Arms include:

- random/frontier sampling;
- expert brainstorming;
- literature-based discovery;
- anomaly/active-learning parent;
- curiosity/open-ended parent;
- science-of-science/portfolio parent;
- generic LLM research questions;
- strongest F0 union;
- P-E without encounter buffer;
- P-E FULL;
- P-C action-selection implementation using the same opportunity record.

**Primary result slot PE-R5.** Test whether P-E adds value beyond P-C and F0.

**Required sentence form:**

> P-E [did/did not] produce prospective value beyond F0 and P-C. The distinct contribution was [mechanism/effect], or the paper contracted because [parent/action-selection sufficiency].

### Cost, agenda authority and component attribution

Track search cost, expert review, buffer burden, time to first decisive action, exploration budget consumed by noise and protected-resource use. A recommendation can enter a queue only under externally supplied agenda authority.

**Primary result slot PE-R6.** Report quality–cost frontier, false agenda actions and component status.

## Discussion

P-E addresses the stage before ordinary hypothesis generation: recognizing that a scientific opportunity exists and deciding whether it deserves a bounded investigation. A positive result would not automate scientific agendas. It would provide a more auditable and prospectively calibrated proposal process.

The prospective requirement is decisive. Retrospective discovery stories are scientifically useful for mechanism reconstruction but weak evidence that a method would have recognized the event at the time. P-E therefore freezes the information surface and candidate record before later outcomes. This design will produce many negative and unresolved cases; excluding them would recreate hindsight bias.

The encounter buffer is another high-risk component. It aims to preserve inexpensive off-path evidence that a task-focused agent would discard. But unpredictable environments contain unlimited surprise. Without a retention budget, noise model and discriminator requirement, curiosity becomes a resource sink. The negative-control cases are therefore central to the thesis.

P-E also distinguishes practical discovery from novelty. A recipe or repair manual can expose a useful control structure. A local community can identify an omitted phenomenon or harm. These can create important scientific opportunities without proving that the underlying theory is new or authorizing use of the source. Source identity, custody and scientific-parent ownership remain explicit.

The strongest likely outcome is contraction. If the opportunity record improves next-action selection inside an existing problem but does not prospectively discover better problems, the mechanism belongs in P-C. A standalone P-E Article requires a genuinely upstream, reproducible and prospectively measured gain.

## Methods

### Study design

Several active research areas are selected with independent domain experts. Candidate generation operates under frozen source/tool dates. Historical time-sliced cases are used only when leakage audits show that later outcomes are unavailable to the system. A subset uses genuinely prospective follow-up.

### Source and authority

Sources include scholarly literature, code/data, standards, practical documents and authorized community/testimonial material where appropriate. Technical accessibility does not imply permission. Restricted or censored routes remain recorded.

### Arms and resource matching

Every arm receives the same source universe, model/tool access and declared search budget. Human experts receive matched time and source access where feasible. Additional hidden expert labour is logged. Follow-up resources are authorized separately from proposal generation.

### Outcomes

Primary:

- independent queue-admission;
- duplicate/known-problem rate;
- actionable-discriminator rate;
- prospective useful-action/result rate;
- false novelty;
- useful encounter recognition;
- noise fixation;
- agenda/authority violation;
- incremental value over P-C and F0.

Secondary:

- importance/tractability/falsifiability calibration;
- time to decisive action;
- candidate diversity;
- deferred option value;
- blocked-resource frequency;
- expert reproducibility;
- search/review cost.

### Leakage and hindsight controls

Bind source cutoffs, model training/retrieval access, prompts and target events. Evaluate famous cases as secondary stress tests, never primary prospective evidence. Candidate text and ranking are content-hashed before outcome access.

### Analysis

Primary estimands compare arms on the frozen candidate set and horizon. Cases are clustered by source/domain. Survival/follow-up models may be used for delayed outcomes. Unresolved candidates are retained. Coordinate-specific uncertainty is reported rather than one opportunity score.

## Limitations frozen before results

- scientific value can take longer than the evaluation horizon;
- experts can disagree and share agenda biases;
- historical cases can leak through model training;
- prospective studies are costly;
- opportunity value is context- and authority-dependent;
- chance may remain irreducible;
- a useful problem can still fail for external reasons;
- buffer/search methods can privilege machine-accessible knowledge.

## Availability and disclosure slots

- **Candidates and timestamps:** `[release or controlled audit statement]`.
- **Sources and cutoff:** `[ledger identity]`.
- **Code/configuration:** `[commit and environment]`.
- **Follow-up data:** `[release/custody statement]`.
- **AI assistance and human accountability:** `[complete before submission]`.

## Honest terminal

```text
P_E_MANUSCRIPT_SURFACE = COMPLETE_PRE_RESULTS
STANDALONE_IDENTITY = CONTINGENT
PROSPECTIVE_CANDIDATES_AND_FOLLOWUP = OPEN
INCREMENTAL_VALUE_OVER_P_C_AND_F0 = OPEN
DEFAULT_IF_NO_DISTINCT_GAIN = MERGE_INTO_P_C
TOP_TIER_SUBMISSION_READY = NO
POSSIBLE_TERMINALS = ARTICLE__P_C_COMPONENT__BENCHMARK_RESOURCE__CANNOT_CHECK
```
