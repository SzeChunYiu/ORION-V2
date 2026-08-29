# Foundation Saturation Pass 01 — Statistical Workflow, Severe Testing, Robustness, Assurance and Resilience

**Status:** first unified changed-vocabulary pass under issue #41. It adds material parent pressure and therefore resets the post-material-addition no-new-coordinate counter to zero. It grants no new kernel coordinate, law or paper identity.

## 1. Search question

What important foundations of reliable scientific control remain invisible when the programme speaks mainly in the language of evidence objects, provenance, verification, relations, diagnosis and agent workflows?

This pass deliberately changed vocabulary toward:

- analysis workflow and model checking;
- test sensitivity and severity;
- robustness and triangulation;
- assurance arguments;
- resilience and adaptive capacity;
- structured analytic techniques;
- information-theoretic model selection.

## 2. Review cell

1. statistician/computational-method reviewer;
2. philosophy-of-statistics and severe-testing reviewer;
3. robustness/triangulation reviewer;
4. assurance-case and safety-engineering reviewer;
5. resilience-engineering reviewer;
6. intelligence-analysis/method-efficacy reviewer;
7. ORION component-value reviewer.

Every finding was reduced against K0–K6 and the strongest mature parent rather than treated as new terminology.

---

# A. Statistical workflow is part of the scientific episode

## Native reconstruction

Applied Bayesian analysis is not one inference call. Gelman et al.'s *Bayesian Workflow* describes a tangled iterative process involving model construction, computational implementation, model checking, validation, troubleshooting, understanding and comparison. In practice several models may be fitted even when only a subset appears in the final scientific conclusion.

Talts et al.'s simulation-based calibration (SBC) addresses a distinct problem: whether an inference algorithm and model implementation produce the posterior they are supposed to produce under simulated generative cases. Later work emphasizes that the choice of SBC test quantities changes which defects the check can detect.

## ORION collision

ORION already separates execution from evidence and records provenance. That is not sufficient to reconstruct **analysis-decision provenance**:

- which model family was considered;
- which prior/parameterization/preprocessing was selected;
- which diagnostics failed;
- which computational algorithm/version was used;
- which alternative models were discarded and why;
- which check was capable of detecting which implementation/model defects;
- whether the final conclusion survived sensitivity and predictive checks.

A replay-perfect analysis can reproduce both the final code and the wrong scientific choice.

## Candidate object under test

`AnalysisWorkflowReceipt = (`
`problem_id, data_identity, preprocessing, candidate_models, model_decisions, computation_identity, diagnostics, predictive_checks, calibration_checks, sensitivity_routes, comparisons, discarded_routes, final_claims, unresolved_failures, authority)`.

This object is not admitted to the kernel. It first competes with existing workflow/provenance systems and paper-specific statistical reporting.

## Benchmark consequences

- same final estimate, different hidden model-checking failures;
- correct model, biased/incorrect inference implementation exposed by SBC;
- passing SBC on insensitive test quantities while a material defect remains;
- several analysis paths sharing preprocessing/model assumptions;
- final result robust to one choice but not another;
- outcome-conditioned model changes that invalidate prospective comparison identity.

## Disposition

`MATERIAL_BENCHMARK_AND_RECEIPT_PRESSURE`

`NEW_KERNEL_COORDINATE = NO`

---

# B. A pass is weak evidence when the test could not have exposed the error

## Native reconstruction

Severe-testing/error-statistical traditions ask whether a hypothesis passed a test that would probably have produced a less concordant result if a specified error were present. The epistemic meaning of a test result therefore depends on the test's capability to detect the error, not only on its pass/fail label.

This aligns with but is not identical to statistical power. The registered error class, procedure, assumptions, selection and post-data inference all matter.

## ORION collision

Current verification receipts bind evaluator/criterion identity, but can still be too weak if they do not expose:

- the error/failure class targeted;
- the cases under which the evaluator is sensitive;
- blind spots and untested regions;
- whether the observed pass was selected after trying multiple tests;
- whether a route was unable to distinguish the live alternatives.

This is a direct threat to false closure and evaluator-authority claims.

## Candidate object under test

`TestSeverityReceipt = (`
`claim, error_class, test_identity, assumptions, detection_capability, test_quantities, selection_history, observed_result, blind_spots, scope, terminal)`.

The object may be implemented by native statistical/formal parents. ORION's residual, if any, is cross-mode enforcement that a weak pass cannot be promoted into a strong scientific transition.

## Hostile cases

- validator always passes both correct and defective artifacts;
- benchmark does not contain the distinction required by the claim;
- a simulation suite samples no hard region;
- test quantity cannot reveal a known implementation bug;
- many checks are tried and only the passing one is reported;
- a formal proof verifies the wrong specification.

## Disposition

`PARENT_OWNED_TEST_SENSITIVITY`

`K6_AND_P_D_ASSURANCE_CHANGE_REQUIRED`

---

# C. Robustness and triangulation require independence and discordance visibility

## Native reconstruction

Robustness analysis systematically varies modelling assumptions to identify whether a result depends on a harmful idealization or choice. Triangulation seeks agreement across methods or evidence routes whose different error structures can reduce concern about procedure-specific artifacts.

However, diversity of labels or materials is not automatically sufficient independence. Multiple routes can share assumptions or probabilistic dependence, and collective evidence can in some circumstances confirm less strongly than one route alone. Conversely, valid discordance can reveal scope differences, model failure or unresolved alternatives.

## ORION collision

P-D already models evidence dependence. The new pressure is to represent **assumption-level route diversity and discordance**, not only source lineage:

`RobustnessRoute = (method, assumptions, data, instrument, model, error_profile, result, scope)`.

Agreement is useful only after dependence and shared assumptions are inspected. Disagreement cannot be repaired automatically by averaging, majority vote or a preferred evaluator.

## Benchmark consequences

- nominally different methods share one preprocessing defect;
- methods vary implementation but not the decisive assumption;
- one route is genuinely independent and corroborative;
- two valid routes disagree because they answer different scoped questions;
- robustness across models hides common measurement error;
- one result collapses under a minor plausible assumption change.

## Disposition

`PARENT_OWNED_ROBUSTNESS_AND_TRIANGULATION`

`P_D_DEPENDENCE_MODEL_EXPANDED_TO_ASSUMPTION_ROUTES`

---

# D. Evidence does not interpret itself: assurance cases as a parent

## Native reconstruction

Safety and assurance cases organize a bounded claim, the argument supporting it, the assumptions/context and the evidence. Goal Structuring Notation and Claims–Argument–Evidence approaches make the reasoning structure inspectable. Incremental assurance work further treats confidence as revisable when new evidence arrives.

The important donation is not a diagram syntax. It is the distinction:

`evidence + provenance != adequate argument for the claim`.

## ORION collision

ORION receipts contain claims, evidence, assumptions, dependence, transport and authority fields, but the programme has not yet shown that it can reconstruct the **argument graph** connecting them or attack missing inference steps systematically.

Candidate:

`ScientificAssuranceCase = (`
`bounded_claim, argument_graph, evidence, assumptions, contexts, defeaters, uncertainties, counterclaims, revalidation_plan, authority_ceiling)`.

This is a strong parent threat. If existing assurance-case methods plus ORION evidence/transport receipts make the same decision, no new component survives.

## Hostile cases

- strong evidence supports a different claim than the one asserted;
- valid components do not imply system-level validity;
- assurance argument omits a shared dependency;
- evidence expires after a context/version change;
- assurance notation is complete but the argument is circular;
- additional field evidence weakens rather than strengthens the case.

## Disposition

`SCIENTIFIC_ASSURANCE_CASE = RESEARCH_OBJECT_ONLY`

`PARENT_REPLACEMENT_REQUIRED_BEFORE_ANY_ORION_OWNERSHIP`

---

# E. Structured reasoning methods can increase inconsistency

## Native reconstruction

Analysis of Competing Hypotheses (ACH) was designed to reduce confirmation bias by structuring evidence across alternative hypotheses. A randomized study of intelligence analysts found mixed evidence for bias reduction and reported that ACH may increase judgment inconsistency and error; analysts also did not consistently execute all prescribed steps.

This finding is structurally important beyond ACH. A method can improve transparency and auditability while degrading accuracy or internal consistency.

## ORION collision

ORION itself favors explicit obligations, alternatives, receipts and decomposition. These should not be presumed beneficial merely because they make reasoning legible.

Every reasoning structure—including plural hypotheses, assurance cases, self-critique, counterexample matrices and decomposition—must pass:

- direct/simple controls;
- negative cases where structure should remain inactive;
- user/executor adherence checks;
- consistency and accuracy endpoints;
- latency/annotation/implementation costs;
- strongest parent replacement.

## Candidate failure

`METHOD_RITUALIZATION = prescribed structure is completed or displayed without improving the protected decision and may introduce inconsistencies`.

This is a benchmark/failure hypothesis, not a new kernel enum.

## Disposition

`COMPONENT_VALUE_PROTOCOL_STRENGTHENED`

`STRUCTURED_METHOD_PRESTIGE = NO_EVIDENCE_OF_VALUE`

---

# F. Scientific control must be evaluated under disturbance and recovery

## Native reconstruction

Resilience engineering studies how systems adapt when conditions exceed nominal design assumptions. Work on adaptive capacity and graceful extensibility emphasizes access to additional capabilities and the ability to continue or recover under unexpectedly severe events.

## ORION collision

Current ORION evaluation strongly protects correctness, authority and selective recovery, but most benchmarks are still episode-level. A scientific harness can be accurate on nominal cases while becoming brittle under:

- tool/provider loss;
- evaluator failure;
- changed resource budgets;
- novel severity or interacting faults;
- delayed/censored evidence;
- representation or policy expiry;
- overload from excessive framework checks.

## Candidate object under test

`ResilienceProfile = (`
`nominal_capability, disturbance_class, degraded_capability, critical_failures, recovery_actions, recovery_time, adaptive_capacity_sources, borrowed_capacity, residual_uncertainty, cost)`.

## Benchmark consequences

- graceful degradation versus false completion;
- safe `CANNOT_CHECK` versus total refusal;
- local recovery versus unnecessary global reset;
- adaptive borrowing of a tool/human reviewer versus hidden authority escalation;
- framework overhead causing collapse under constrained resources;
- restoration of full capability after revalidation.

## Disposition

`MATERIAL_SYSTEM_EVALUATION_PRESSURE`

`NO_NEW_KERNEL_FAMILY`

---

# G. MDL and information-theoretic model selection threaten ORION minimality claims

## Native reconstruction

Minimum Description Length treats a model as a code and balances the description length of the model with the description length of the data under it. It supplies a principled family of model-selection and representation-comparison methods across heterogeneous model classes.

## ORION collision

P-A and K2 discuss minimal decision envelopes and conservative reduction. They cannot claim generic minimal representation, complexity–fit balance or compression-based model choice.

The residual question is narrower: does a decision-relative, source-bound reduction preserve registered scientific judgments and counter-probes in cases where a generic MDL/compression criterion selects an unsafe or scientifically irrelevant representation?

## Hostile controls

- shortest model destroys the intervention distinction;
- compression improves while calibration or causal adequacy worsens;
- two encodings change description length without changing the scientific object;
- brute computational cost makes exact MDL impractical;
- domain-native sufficient statistics already solve the problem;
- decision-relative envelope matches parent output with no residual.

## Disposition

`MDL_AND_ALGORITHMIC_COMPLEXITY = STRONG_PARENT_BASELINE`

`MINIMAL_ENVELOPE_NOVELTY = OPEN_AND_THREATENED`

---

## 3. Cross-cutting foundation change

The unified pass changes the proposed machine-epistemic episode from a collection of evidence/actions into a more explicit **claim–workflow–test–argument–recovery system**.

A candidate episode must be able to expose, when material:

- how the analysis was constructed and checked;
- which error a test could have detected;
- whether corroborating routes are genuinely diverse;
- what argument connects evidence to the claim;
- whether a structured method improves decisions;
- how capability degrades and recovers under disturbance;
- whether minimality is parent-owned compression or decision-relative preservation.

These are not seven new kernel coordinates. They are parent pressures and benchmark obligations distributed primarily across K2–K6.

## 4. Paper propagation

### Flagship

Add these parent traditions to the atlas and external review packet, but do not expand the main manuscript for citation completeness. The final synthesis decides which distinctions enter the public foundation.

### P-A

Add MDL and statistical-workflow parents; compare envelope minimality against compression/sufficiency baselines.

### P-B

Add test sensitivity and robustness conditions to relation/transport assurance.

### P-C

Add analysis-workflow diagnosis, method-ritualization negative controls and resilience endpoints.

### P-D

Add robustness-route dependence, discordance preservation and assurance-case parent comparison.

### P-E

Require severe prospective discriminators and rule out analysis-workflow artifacts as opportunity signals.

### P-F

Measure machine-native strategies under disturbance and compare non-linguistic representation selection against MDL and strongest native algorithms.

## 5. Selected primary/authoritative anchors

- Gelman, A. et al. *Bayesian Workflow*. arXiv:2011.01808.
- Talts, S., Betancourt, M., Simpson, D., Vehtari, A. & Gelman, A. *Validating Bayesian Inference Algorithms with Simulation-Based Calibration*. arXiv:1804.06788.
- Modrák, M. et al. *Simulation-Based Calibration Checking for Bayesian Computation: The Choice of Test Quantities Shapes Sensitivity*. arXiv:2211.02383.
- Mayo, D. G. & Spanos, A. Severe Testing as a Basic Concept in a Neyman–Pearson Philosophy of Induction. *British Journal for the Philosophy of Science* 57, 323–357 (2006). DOI: 10.1093/bjps/axl003.
- Kuorikoski, J., Lehtinen, A. & Marchionni, C. Economic Modelling as Robustness Analysis. *British Journal for the Philosophy of Science* 61 (2010). DOI: 10.1093/bjps/axp049.
- Stegenga, J. & Menon, T. Robustness and Independent Evidence. *Philosophy of Science* (2022).
- Kelly, T. A Systematic Approach to Safety Case Management. SAE 2004-01-1779. DOI: 10.4271/2004-01-1779.
- Diemert, S., Goodenough, J. B., Joyce, J. & Weinstock, C. B. Incremental Assurance Through Eliminative Argumentation. *Journal of System Safety* 58 (2023). DOI: 10.56094/jss.v58i1.215.
- Dhami, M. K. The “analysis of competing hypotheses” in intelligence analysis. *Applied Cognitive Psychology* 33 (2019). DOI: 10.1002/acp.3550.
- Cook, R. I. & Long, B. A. Building and revising adaptive capacity sharing for technical incident response. *Applied Ergonomics* 90, 103240 (2021). DOI: 10.1016/j.apergo.2020.103240.
- Rissanen, J. Modeling by shortest data description. *Automatica* 14, 465–471 (1978). DOI: 10.1016/0005-1098(78)90005-5.
- Grünwald, P. D. *The Minimum Description Length Principle* (MIT Press, 2007).

## Current terminal

```text
PASS_ID = FOUNDATION_SATURATION_PASS_01
MATERIAL_NEW_PARENT_PRESSURE = YES
LAST_MATERIAL_ADDITION = STATISTICAL_WORKFLOW_SEVERITY_ROBUSTNESS_ASSURANCE_RESILIENCE_MDL
POST_MATERIAL_NO_NEW_COORDINATE_COUNT = 0
NEW_KERNEL_COORDINATE = NO
NEW_FOUNDATION_LAW = NO
ATLAS_UPDATE_REQUIRED = COMPLETED_V1
FOUNDATION_SATURATION = OPEN
```
