# V2-C07 Research and Manuscript Plan V0

**Working title:** *Dependence-Aware Scientific Evidence and Validator Diversity*  
**Status:** candidate paper; all claims `CANNOT_CHECK`.

## 1. Scientific problem

Scientific systems often report confidence from the number of sources, models, reviewers, replications or agents. These units may share data, training, source lineage, instrumentation, prompts, incentives, retrieval corpora or failure modes. Nominal plurality can therefore provide little independent assurance.

## 2. Parent fields

- dependent-effect meta-analysis;
- clustered/survey sampling and design effects;
- graphical models and latent common causes;
- epidemiological interference;
- reliability/common-cause failures;
- ensemble diversity and correlated error;
- Byzantine/distributed agreement;
- social diffusion and copied testimony;
- provenance and multi-instrument metrology;
- V1 evidence, authority and execution integrity.

## 3. Candidate thesis

A source-bound dependence model can improve calibration and prevent false scientific-authority promotion over source count, majority vote and naive ensembles while retaining useful independent evidence and explicitly reporting dependence-identification limits.

## 4. Candidate objects

### `EvidenceDependenceGraph`

Nodes are observations, sources, experiments, validators or derived claims. Typed hyperedges encode shared source, data, model, training, prompt, instrument, calibration, personnel, institution, incentive, computation, derivation or environmental cause.

### `ValidationDiversityReceipt`

Binds:

- nominal validator/evidence count;
- declared dependence components;
- quantitative correlation/common-cause estimates where identifiable;
- unidentified dependence routes;
- effective-information or conservative bound;
- target failure mode;
- sensitivity analysis;
- authority impact;
- expiration conditions.

## 5. Formal questions

### Q1 — Component and correlation models

When is a conservative connected-component bound appropriate, and when is a probabilistic covariance/latent model required?

### Q2 — Target-relative independence

Evidence can be independent for one error mode but dependent for another. Define independence relative to a target claim/failure mechanism.

### Q3 — Provenance versus statistical dependence

Shared provenance is evidence of possible dependence, not a complete correlation model. Conversely, independent provenance does not guarantee independent systematic error.

### Q4 — Validator diversity

Which model/data/tool/instrument differences actually reduce target error rather than create cosmetic diversity?

### Q5 — Unidentified dependence

How should scientific terminals behave when common causes cannot be observed or estimated?

## 6. Benchmark families

1. independent measurements;
2. copied secondary sources;
3. shared model and training data;
4. different models using one retrieval corpus;
5. independent instruments with common calibration;
6. same instrument under independent operators;
7. clustered laboratories/institutions;
8. correlated reviewers and shared benchmark leakage;
9. strategic collusion or copied reasoning;
10. transitive bridge linking apparent clusters;
11. negative controls with genuinely independent support;
12. dependence structure changing across epochs.

## 7. Baselines

- nominal source/agent count;
- majority vote;
- independent Bernoulli evidence model;
- provenance deduplication;
- simple cluster count;
- equicorrelation/design-effect adjustment;
- graphical/latent common-cause model;
- reliability common-cause model;
- strongest parent product;
- candidate target-relative interface.

## 8. Outcomes

- calibration/Brier/log loss for claim support where probabilities are valid;
- false-authority promotion;
- effective-evidence estimation error;
- common-cause detection;
- useful-evidence retention and over-conservatism;
- target-relative dependence classification;
- sensitivity to unidentified dependence;
- provenance-native fidelity;
- compute/annotation cost;
- fresh-domain transfer.

## 9. Hostile cases

- three copied sources reported as three confirmations;
- three agents with one shared model/data;
- independent models with one contaminated benchmark;
- different instruments with one faulty calibration chain;
- same lab and protocol with hidden common operator;
- independent evidence incorrectly merged due superficial similarity;
- dependence graph used to deny all evidence;
- consensus treated as truth despite shared failure;
- independence certificate surviving an epoch/data change.

## 10. Relationship to V1 and other V2 candidates

- V1 P4/P8/P15 retain ownership of scientific promotion, authority and execution distinctions.
- C02 supplies context-relative relation semantics.
- C08 may supply reticulate lineage but cannot replace statistical dependence.
- C04 consumes dependence state for action selection and validation.

C07 must not claim provenance, ensemble diversity or common-cause analysis individually.

## 11. Figures and tables

- Figure 1: nominal plurality versus dependence graph;
- Figure 2: target-relative failure/dependence;
- Figure 3: benchmark generation and hidden common causes;
- Figure 4: calibration/retention frontier;
- Table 1: parent mechanisms;
- Table 2: benchmark cases;
- Table 3: effective information/common-cause results;
- Table 4: false promotion and retention;
- Table 5: sensitivity, ablations and transfer.

## 12. Honest terminals

- `EXISTING_DEPENDENCE_MODEL_SUFFICIENT`;
- `DEPENDENCE_NOT_IDENTIFIABLE`;
- `OVERCONSERVATIVE_EVIDENCE_REJECTION`;
- `NO_INCREMENTAL_AUTHORITY_PROTECTION`;
- `CANNOT_CHECK`.

## 13. Immediate pre-freeze work

- complete full-text cards across meta-analysis, survey, reliability, ensemble, distributed and sociological parents;
- define target-error taxonomy;
- expand V0 component/correlation fixtures;
- specify hidden common-cause generators;
- bind V1 P4/P8/P15 ownership;
- design protected authority-promotion experiment;
- specify how unidentified dependence changes terminals;
- do not run candidate outcome studies before handoff/protocol freeze.