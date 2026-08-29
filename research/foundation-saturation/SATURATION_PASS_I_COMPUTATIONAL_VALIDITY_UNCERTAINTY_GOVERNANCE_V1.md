# Saturation Pass I — Computational Validity, Uncertainty Plurality, Semantics and Governed Data V1

**Canonical parent:** issue #41  
**Pass owner:** issue #44  
**Predecessor material pass:** issue #42 / Pass H

**Status:** changed-vocabulary material-finding pass. It resets the canonical post-material clean-pass counter to zero. It grants no new kernel family, law, paper identity, field status or publication authority.

## 1. Search question

Which foundations remain invisible when Machine Epistemics is described mainly through evidence, models, experiments, relations, review and authority at a high semantic level?

Pass I deliberately searched the lower and surrounding layers where a machine-mediated scientific transition can fail:

- problem conditioning, approximation and finite-precision arithmetic;
- numerical stability, forward/backward error and validated numerics;
- scientific-software verification when no exact output oracle exists;
- imprecise probability, partial ignorance, ambiguity and conflicting information;
- semantic interoperability when ontologies omit local context;
- machine-actionable data versus legitimate data control and reuse;
- credibility allocation, question-setting and participatory knowledge production;
- ML underspecification, data cascades and weak-baseline inflation.

The pass did not ask whether ORION can add more metadata. It asked which mature parent theories already own these problems and which scientific decisions remain unsafe without their native distinctions.

## 2. Expert cell and delegated review

1. **Numerical-analysis and validated-computation reviewer** — reconstructs conditioning, stability, finite precision, interval enclosures and computer-assisted proof.
2. **Scientific-software testing reviewer** — reconstructs exact, partial, differential, statistical and metamorphic oracles and their adequacy limits.
3. **Probability/UQ/decision reviewer** — separates precise probability, sets of probabilities, interval bounds, ignorance, conflict, model uncertainty and decision rules.
4. **Semantic-interoperability reviewer** — tests ontology/context mappings and prohibited inferences under incomplete semantics.
5. **Indigenous data-governance and participatory-research reviewer** — separates machine accessibility from collective authority, consent, benefit and question-setting.
6. **ML credibility and deployment reviewer** — tests underspecification, data cascades, leakage and weak baselines.
7. **Hostile parent/component-value reviewer** — attempts to absorb every candidate into K0–K6 plus mature adapters, and rejects structures that add no protected decision value.

### Joint deliberation rule

A candidate survives the pass only when:

- its native distinction changes a protected scientific transition or benchmark;
- a simpler existing receipt cannot express the failure without semantic loss;
- it remains explicitly parent-owned until incremental value is demonstrated;
- negative controls exist where the candidate should stay inactive.

---

## 3. Finding I1 — scientific computation has several independent validity layers

### Native reconstruction

Numerical analysis distinguishes at least:

- **problem conditioning** — sensitivity of the mathematical problem to perturbations in its input;
- **algorithmic stability** — whether the algorithm introduces or amplifies errors beyond what the problem itself requires;
- **forward error** — distance between computed and exact output;
- **backward error** — smallest perturbation of the input/problem for which the computed output is exact;
- **rounding/arithmetic semantics** — finite precision, exception handling, operation order and hardware/compiler behavior;
- **validated enclosure** — a mathematically guaranteed set containing the exact result;
- **model adequacy** — whether the mathematical problem represents the intended scientific system.

A numerically stable algorithm can accurately solve the wrong model. An unstable algorithm can corrupt an otherwise adequate model. A reproducible floating-point computation can reproduce the same inaccurate answer. A validated enclosure proves a statement about the encoded mathematical problem, not automatically about nature.

### ORION collision

The current episode records computation identity, evidence, evaluator and provenance, but can still treat a computation as one undifferentiated execution. Scientific claims based on simulation, optimization, inverse problems, numerical proof or ML-accelerated PDE solvers need the validity chain to remain visible.

### Candidate research object

`ComputationalValidityReceipt = (`
`scientific_claim, mathematical_problem, input_identity, conditioning_or_sensitivity, numerical_method, implementation_identity, arithmetic_environment, precision, forward_error, backward_error, truncation_or_discretization_error, solver_termination, validated_enclosure_or_bound, cross_implementation_checks, model_adequacy_status, unresolved_error, claim_scope, epoch)`.

Not every field is mandatory in every task. The receipt is enabled when a scientific transition materially depends on approximate computation.

### Candidate failures

- `ILL_CONDITIONED_PROBLEM_LAUNDERED_AS_ALGORITHM_FAILURE`;
- `STABLE_ALGORITHM_LAUNDERED_AS_MODEL_VALIDITY`;
- `REPRODUCIBLE_NUMERICAL_ERROR`;
- `FLOATING_POINT_ENVIRONMENT_UNBOUND`;
- `APPROXIMATION_ERROR_OUTSIDE_CLAIM_TOLERANCE`;
- `VALIDATED_MATHEMATICS_OVERGENERALIZED_TO_NATURE`;
- `WEAK_NUMERICAL_BASELINE_LAUNDERED_AS_MACHINE_GAIN`.

### Reduction

Numerical analysis, IEEE floating-point standards, interval/validated numerics and VVUQ own the mechanisms. The object is an adapter-facing K0/K2/K3/K6 receipt candidate, not a new kernel family.

### Materiality

**Material.** It creates a distinct benchmark and parent-product obligation that was not explicit enough in F04–F06.

---

## 4. Finding I2 — computational tests need an oracle model, not only an evaluator identity

### Native reconstruction

Software testing assumes some way to determine whether an execution is correct. In scientific software, the exact answer is frequently unavailable or too expensive. Parent strategies include:

- exact known-answer or proof oracle;
- partial oracle checking necessary properties;
- differential oracle comparing independent implementations;
- statistical oracle checking distributional properties;
- metamorphic oracle checking relations across transformed inputs/outputs;
- residual, invariant or conservation-law checks;
- no usable oracle / unresolved.

Metamorphic testing can alleviate the oracle problem by testing necessary relations between executions, but its strength depends on the chosen metamorphic relations and source cases. A relation can be true of both correct and defective programs, or test only a narrow behavior.

### ORION collision

`TestSensitivityProfile` from Pass H asks whether an evaluator can expose an error class. The new donation is an explicit **oracle construction and adequacy** layer for computational evidence.

### Candidate research object

`OracleAdequacyProfile = (`
`program_or_computation, claim, oracle_type, oracle_identity, metamorphic_or_invariant_relations, independence_from_subject, covered_input_region, target_fault_classes, known_blind_spots, adequacy_evidence, selection_history, cost, terminal)`.

### Candidate failures

- `NO_ORACLE_LAUNDERED_AS_PASS`;
- `METAMORPHIC_RELATION_SHARED_BY_FAULTY_IMPLEMENTATIONS`;
- `DIFFERENTIAL_ORACLE_COMMON_MODE`;
- `PARTIAL_ORACLE_OVERGENERALIZED`;
- `ORACLE_RELATION_SELECTED_AFTER_OUTCOME`;
- `CONSERVATION_CHECK_PASSES_WRONG_SCIENTIFIC_MODEL`.

### Reduction

This is a specialization of test sensitivity and computational validation. It belongs to scientific-software testing parents and K6/P-D evaluation, not a new foundation law.

### Materiality

**Material benchmark addition; no new coordinate.**

---

## 5. Finding I3 — uncertainty cannot always be represented by one probability distribution

### Native reconstruction

The usual aleatory/epistemic split does not exhaust scientific uncertainty. Parent theories represent:

- a precise probability model;
- a set of plausible probability models or credal set;
- lower/upper probabilities or expectations;
- interval/validated numerical bounds;
- possibility/belief functions;
- partial ignorance with no warranted distribution;
- conflict among sources;
- model-class or structural uncertainty;
- semantic ambiguity about the event/variable;
- decision/value uncertainty.

Dempster's upper/lower probabilities and later imprecise-probability work show that incomplete information and conflict need not be collapsed into a single posterior. Conditioning, independence and decision rules become model-specific. A precise number can therefore be an unjustified artifact of the representation rather than additional knowledge.

### ORION collision

ORION already retains uncertainty and `CANNOT_CHECK`, and Pass 02 added deep-uncertainty decision parents. The missing interface pressure is to bind the **form and semantics of uncertainty** before aggregation, propagation or value-of-information computation.

### Candidate research object

`UncertaintyFormReceipt = (`
`target_quantity_or_claim, uncertainty_form, event_or_variable_semantics, model_or_credal_set, lower_upper_bounds, ignorance_state, conflict_state, dependence, elicitation_or_generation_process, conditioning_rule, propagation_rule, decision_rule_if_any, calibration_or_coverage_evidence, unresolved_scope, epoch)`.

### Candidate failures

- `IGNORANCE_LAUNDERED_AS_UNIFORM_PRIOR`;
- `SOURCE_CONFLICT_AVERAGED_AWAY`;
- `CREDAL_SET_COLLAPSED_WITHOUT_DECISION_AUTHORITY`;
- `INTERVAL_BOUND_INTERPRETED_AS_PROBABILITY`;
- `ALEATORY_EPISTEMIC_BINARY_OVERCLAIMED`;
- `UNCERTAINTY_FORM_CHANGED_DURING_COMPOSITION`;
- `PRECISE_CONFIDENCE_WITH_UNIDENTIFIED_MODEL_CLASS`.

### Reduction

Imprecise probability, robust Bayesian analysis, interval analysis, evidence theory and DMDU own the native mechanisms. K1/K3/K4/K6 require a typed interface only when the uncertainty form changes the scientific decision.

### Materiality

**Material interface and benchmark pressure.** It expands F03/F08/F18 but does not create K7.

---

## 6. Finding I4 — semantic interoperability is context reconstruction, not label matching

### Native reconstruction

Ontology/schema matching seeks semantic interoperability across representations. A persistent problem is that ontologies are often incomplete relative to the local context in which they were designed; external background knowledge is then required to align them. Similar labels can denote different roles, scales or relations, and low lexical similarity can hide exact decision-relevant correspondences.

### ORION collision

Pass H's `BoundaryInterfaceReceipt` already captures shared identity, local projections, common invariants and prohibited cross-projection inferences. The ontology-matching route adds an implementation parent and a sharper source of failure:

- mapping confidence may depend on hidden background knowledge;
- the background source itself has provenance, expiry and cultural/domain scope;
- one-to-one mappings can erase local constraints;
- machine interoperability can succeed syntactically while failing scientifically.

### Candidate specialization

`SemanticContextReceipt = (`
`source_ontology, target_ontology, source_context, target_context, mapping, background_knowledge_identity, preserved_queries, lost_constraints, ambiguity, counterexamples, prohibited_inferences, adjudicator, epoch)`.

### Candidate failures

- `SYNTACTIC_INTEROPERABILITY_LAUNDERED_AS_SEMANTIC_EQUIVALENCE`;
- `BACKGROUND_KNOWLEDGE_UNBOUND`;
- `CONTEXT_INCOMPLETE_MAPPING`;
- `LOCAL_CONSTRAINT_DROPPED`;
- `TRANSLATION_CONFIDENCE_LAUNDERED_AS_NATIVE_VERDICT`.

### Reduction

This is an implementation specialization of K2 and `BoundaryInterfaceReceipt`. No new coordinate is admitted.

### Materiality

**No new coordinate; strongest-parent and hostile-case expansion.**

---

## 7. Finding I5 — machine-actionable data and legitimately governed data are different achievements

### Native reconstruction

FAIR focuses on findability, accessibility, interoperability and reusability of digital research objects, with particular attention to machine actionability. FAIRness does not itself determine whether a use is legitimate, beneficial, consented to or governed by the people represented in the data.

The CARE Principles for Indigenous Data Governance add Collective Benefit, Authority to Control, Responsibility and Ethics. CARE was developed to complement FAIR and to direct data actors toward Indigenous Peoples' rights, governance protocols and self-determination rather than treating openness/reuse as an overriding default.

### ORION collision

A source can be technically accessible, well-provenanced and semantically interoperable while its use remains unauthorized, harmful or inconsistent with collective governance. A machine-mediated research process must not derive reuse permission from retrievability or scientific utility.

### Candidate research object

`GovernedDataReceipt = (`
`data_or_knowledge_identity, represented_people_or_collective, stewardship_identity, FAIR_properties, access_conditions, permitted_purposes, collective_benefit_hypothesis, authority_to_control, consent_or_protocol, responsibility_obligations, ethics_constraints, attribution, benefit_or_harm_monitoring, reuse_request, decision, expiry)`.

### Candidate failures

- `FAIR_LAUNDERED_AS_FREE_TO_USE`;
- `ACCESS_LAUNDERED_AS_CONSENT`;
- `SCIENTIFIC_VALUE_OVERRIDES_COLLECTIVE_AUTHORITY`;
- `DEIDENTIFICATION_LAUNDERED_AS_NO_GROUP_HARM`;
- `COMMUNITY_PROTOCOL_REDUCED_TO_METADATA`;
- `FUTURE_REUSE_OUTSIDE_ORIGINAL_PURPOSE`;
- `CENSORED_ROUTE_COUNTED_AS_NO_KNOWLEDGE`.

### Reduction

CARE, Indigenous data sovereignty, research ethics, law and governance own the normative/institutional mechanisms. ORION can bind externally supplied authority and restrictions; it cannot compute or mint legitimate collective authority.

### Materiality

**Material authority/custody benchmark and source-mode pressure; no scientific evidence law.**

---

## 8. Finding I6 — credibility and participation affect what evidence enters the system

### Native reconstruction

Epistemic-injustice and participatory-research traditions show that inquiry can fail before evidence aggregation:

- a speaker/source receives an unjustified credibility deficit;
- a community lacks shared interpretive resources for articulating an experience;
- research questions, variables or quality criteria exclude affected knowers;
- nominal participation occurs only after the agenda, instrument and interpretation are fixed;
- diverse participation is confused with automatic truth.

Citizen-science and participatory quality work additionally show that quality criteria are context-dependent and may need co-creation, transparent implementation and revision.

### ORION collision

Dependence-aware evidence models can accurately evaluate the evidence that was admitted while remaining blind to systematic **source exclusion and question-space construction**. Conversely, forcing equal evidential weight regardless of competence, access or source quality would be another error.

### Candidate research object

`EpistemicParticipationReceipt = (`
`problem_frame, affected_knowers, source_roles, access_to_question_setting, instrument_or_variable_design_role, evidence_submission_route, credibility_rule, dependence_and_competence, criticism_uptake, interpretation_authority, exclusions_and_reasons, appeal_or_reopen_route, outcome)`.

### Candidate failures

- `SOURCE_EXCLUDED_BEFORE_EVIDENCE_GRAPH`;
- `IDENTITY_BASED_CREDIBILITY_DEFICIT`;
- `PARTICIPATION_AFTER_AGENDA_FREEZE`;
- `DIVERSITY_LAUNDERED_AS_INDEPENDENCE_OR_TRUTH`;
- `EXPERTISE_ERASED_BY_FORMAL_EQUALITY`;
- `COMMUNITY_INTERPRETATION_OVERRIDDEN_WITHOUT_AUTHORITY`;
- `QUALITY_CRITERION_IMPOSED_AS_CULTURALLY_NEUTRAL`.

### Reduction

Social epistemology, participatory science, citizen science, research ethics and governance own the mechanisms. The candidate object belongs to F11/F12/F16 and K0/K3/K6 research interfaces, not the universal kernel.

### Materiality

**Material omission and benchmark pressure.** It changes source-coverage and question-framing evaluation.

---

## 9. Finding I7 — equivalent benchmark performance can conceal materially different systems

### Native reconstruction

ML underspecification occurs when a pipeline admits many predictors with similarly strong in-domain validation performance but materially different behavior under deployment or stress tests. Data cascades describe compounding downstream failures produced by undervalued data work. Studies of ML PDE solvers further show that weak numerical baselines and selective reporting can inflate claims of speed or superiority.

### ORION collision

A protected evaluator can be bound correctly and still identify an equivalence class that is too coarse for the scientific use. Strong result custody cannot repair:

- non-identifying benchmark design;
- hidden variation among equally scoring systems;
- data leakage or data-generation defects;
- weak parent baselines;
- outcome-reporting bias;
- unexplored deployment strata.

### Candidate research object

`PipelineUnderspecificationProfile = (`
`pipeline_identity, training_and_validation_distribution, equivalently_scoring_models, stress_dimensions, deployment_contexts, data_generation_and_label_process, leakage_checks, parent_baselines, numerical_accuracy_and_cost, reporting_surface, divergence_across_strata, unresolved_equivalence_class)`.

### Candidate failures

- `BENCHMARK_EQUIVALENCE_LAUNDERED_AS_SCIENTIFIC_EQUIVALENCE`;
- `DATA_CASCADE_HIDDEN_BY_MODEL_SCORE`;
- `LEAKAGE_LAUNDERED_AS_GENERALIZATION`;
- `WEAK_PARENT_BASELINE_LAUNDERED_AS_ADVANCE`;
- `OUTCOME_REPORTING_BIAS`;
- `RESOURCE_MISMATCH_LAUNDERED_AS_EFFICIENCY`;
- `DEPLOYMENT_STRESS_ROUTE_OMITTED`.

### Reduction

ML credibility, statistics, data-centric AI, software validation and domain-native numerical science own the mechanisms. The profile expands K6/component-value testing and P-C/P-F benchmarks.

### Materiality

**Material benchmark family; no new kernel coordinate.**

---

## 10. Integrated scientific computation chain

The pass exposes a chain that must remain separable when material:

`source/data governance`
`-> semantic/context interpretation`
`-> scientific model/problem`
`-> conditioning and uncertainty form`
`-> algorithm`
`-> implementation and arithmetic`
`-> oracle/test sensitivity`
`-> computed output`
`-> scientific interpretation and transport`
`-> evidence-to-decision`
`-> legitimate authority`.

No layer validates the next by default:

- FAIRness does not grant permission;
- semantic mapping does not establish native equivalence;
- mathematical correctness does not establish model adequacy;
- numerical stability does not establish scientific truth;
- reproducibility does not establish correctness;
- a partial/metamorphic oracle does not establish complete validity;
- precise output does not eliminate model or semantic uncertainty;
- strong evidence does not select values or authority.

This chain is a synthesis aid and benchmark topology. It is not admitted as a new ontology or kernel family.

---

## 11. Reduction matrix

| Finding | Candidate structure | Mature owner(s) | Current disposition |
|---|---|---|---|
| conditioning/numerical validity | `ComputationalValidityReceipt` | numerical analysis, validated numerics, IEEE arithmetic, VVUQ | parent-facing receipt candidate |
| oracle problem | `OracleAdequacyProfile` | scientific-software testing, metamorphic/differential testing | specialization of test sensitivity |
| plurality of uncertainty forms | `UncertaintyFormReceipt` | imprecise probability, UQ, evidence theory, intervals, DMDU | K1/K3/K4/K6 interface candidate |
| semantic context | `SemanticContextReceipt` | ontology matching, semantic web, domain modelling | specialization of boundary interface |
| FAIR versus CARE/governance | `GovernedDataReceipt` | data stewardship, Indigenous data sovereignty, ethics/law | authority/custody research object |
| credibility and participation | `EpistemicParticipationReceipt` | social epistemology, participatory/citizen science | source/frame benchmark object |
| ML pipeline underspecification | `PipelineUnderspecificationProfile` | ML credibility, statistics, data-centric AI, domain numerics | K6/component-value benchmark |

`NEW_KERNEL_FAMILY = NO`.

---

## 12. New knowledge-universe pressure

Pass I adds two explicit families because their native theories and implementation artifacts are too important to leave implicit:

- `F19 — numerical_computation_scientific_software_validity`;
- `F20 — uncertainty_forms_imprecise_probability_ignorance_conflict`.

Semantic interoperability and governed/participatory data strengthen existing F12, F16 and F17 rather than creating additional families.

The declared universe therefore expands from 18 to **20 families**. All three clean passes must cover the expanded universe after this material addition.

---

## 13. Contradictions added

- approximate computation versus exact-sounding scientific claims;
- precise posterior versus honest ignorance/conflict;
- machine-actionable openness versus legitimate collective control;
- semantic interoperability versus local meaning;
- inclusive participation versus competence/source-quality differentiation;
- benchmark equivalence versus deployment equivalence.

These require contextual or formal reconciliation; none is resolved by averaging.

---

## 14. Protected benchmark additions

- `CONDITIONING_VS_ALGORITHM_STABILITY`;
- `REPRODUCIBLE_WRONG_NUMERICAL_RESULT`;
- `VALIDATED_NUMERICS_WRONG_SCIENTIFIC_MODEL`;
- `METAMORPHIC_ORACLE_BLIND_FAULT`;
- `DIFFERENTIAL_ORACLE_COMMON_MODE`;
- `IGNORANCE_VS_UNIFORM_PRIOR`;
- `CONFLICT_PRESERVATION_VS_AVERAGING`;
- `SYNTACTIC_INTEROPERABILITY_CONTEXT_FAILURE`;
- `FAIR_BUT_NOT_AUTHORIZED`;
- `CARE_CUSTODY_AND_FUTURE_REUSE`;
- `SOURCE_EXCLUSION_BEFORE_EVIDENCE_GRAPH`;
- `PARTICIPATION_AFTER_AGENDA_FREEZE`;
- `UNDERSPECIFIED_EQUAL_SCORE_DIVERGENT_DEPLOYMENT`;
- `WEAK_NUMERICAL_BASELINE_EFFICIENCY_CLAIM`;
- `DATA_CASCADE_DELAYED_FAILURE`.

---

## 15. Paper propagation

### P-A

Add numerical/semantic/data-governance constraints to donor discovery. A donor retrieved from interoperable data is not automatically semantically faithful or authorized for reuse.

### P-B

Add computational validity and uncertainty-form conservation to transport. Exact textual/model relation does not preserve numerical conditioning, oracle coverage or data-use authority.

### P-C

Add uncertainty-form-aware action selection, numerical-computation recovery and oracle acquisition. Do not force a precise self-model probability when only a credal/ignorance state is warranted.

### P-D

Add oracle common causes, imprecise/conflicting evidence, participation/source exclusion and governed-data authority to dependence and assurance studies.

### P-E

Opportunity discovery must distinguish numerical/software artifacts, data cascades, semantic mismatch and unauthorized source use from real scientific anomalies.

### P-F

Machine-native gains require numerical validity, strong native baselines, leakage/underspecification stress tests and a claim-sufficient external witness. More compute or nonhuman representation does not excuse approximate-computation opacity.

### Flagship

The foundation must make the computational validity chain visible without turning the main paper into a systems checklist. Which parts become public foundation propositions is deferred to synthesis.

---

## 16. Primary and authoritative anchors inspected

- Higham, N. J. *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM (2002). DOI `10.1137/1.9780898718027`.
- IEEE. *IEEE 754-2019 Standard for Floating-Point Arithmetic*.
- Neher, M., Jackson, K. R. & Nedialkov, N. S. On Taylor Model Based Integration of ODEs. *SIAM Journal on Numerical Analysis* (2007). DOI `10.1137/050638448`.
- Johansson, F. & Mezzarobba, M. Fast and Rigorous Arbitrary-Precision Computation of Gauss–Legendre Quadrature Nodes and Weights. *SIAM Journal on Scientific Computing* (2018). DOI `10.1137/18M1170133`.
- Chen, T. Y., Cheung, S. C. & Yiu, S. M. Metamorphic Testing: A New Approach for Generating Next Test Cases (original technical report/paper lineage).
- Liu, H., Kuo, F.-C., Towey, D. & Chen, T. Y. How Effectively Does Metamorphic Testing Alleviate the Oracle Problem? *IEEE TSE* 40, 4–22 (2014). DOI `10.1109/TSE.2013.46`.
- Dempster, A. P. Upper and Lower Probabilities Induced by a Multivalued Mapping. *Annals of Mathematical Statistics* 38, 325–339 (1967). DOI `10.1214/aoms/1177698950`.
- Walley, P. Towards a Unified Theory of Imprecise Probability. *International Journal of Approximate Reasoning* 24, 125–148 (2000). DOI `10.1016/S0888-613X(00)00031-1`.
- Wilkinson, M. D. et al. The FAIR Guiding Principles for Scientific Data Management and Stewardship. *Scientific Data* 3, 160018 (2016). DOI `10.1038/sdata.2016.18`.
- Carroll, S. R. et al. The CARE Principles for Indigenous Data Governance. *Data Science Journal* 19, 43 (2020). DOI `10.5334/dsj-2020-043`.
- Portisch, J., Hladik, M. & Paulheim, H. Background Knowledge in Ontology Matching: A Survey. *Semantic Web* (2022/2024). DOI `10.3233/SW-223085`.
- Fricker, M. *Epistemic Injustice: Power and the Ethics of Knowing*. Oxford University Press (2007).
- Heigl, F. et al. Co-Creating and Implementing Quality Criteria for Citizen Science. *Citizen Science: Theory and Practice* 5, 23 (2020). DOI `10.5334/cstp.294`.
- D'Amour, A. et al. Underspecification Presents Challenges for Credibility in Modern Machine Learning. *JMLR* 23, 1–61 (2022).
- Sambasivan, N. et al. Data Cascades in High-Stakes AI. *CHI 2021*. DOI `10.1145/3411764.3445518`.
- McGreivy, N. & Hakim, A. Weak Baselines and Reporting Biases Lead to Overoptimism in ML for Fluid-Related PDEs. *Nature Machine Intelligence* 6, 1256–1269 (2024). DOI `10.1038/s42256-024-00897-5`.

## Current terminal

```text
PASS_I = MATERIAL_FOUNDATION_PRESSURE
DECLARED_FAMILIES = 20
NEW_FAMILIES = F19_F20
LATEST_MATERIAL_ADDITION = COMPUTATIONAL_VALIDITY__ORACLE_ADEQUACY__UNCERTAINTY_FORMS__GOVERNED_DATA__EPISTEMIC_PARTICIPATION__PIPELINE_UNDERSPECIFICATION
POST_PASS_I_CLEAN_FULL_PASSES = 0
CLEAN_FULL_PASSES_REQUIRED = 3
FOUNDATION_SYNTHESIS = BLOCKED
NEW_KERNEL_FAMILY = NO
NEW_FOUNDATION_LAW = NO
NEW_PAPER_IDENTITY = NO
FIELD_AUTHORITY = NONE
```
