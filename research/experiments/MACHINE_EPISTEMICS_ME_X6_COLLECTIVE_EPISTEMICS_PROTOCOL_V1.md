# ME-X6 — Collective Epistemics / Scientific Artifacts as Noisy Sensors Protocol V1

**State date:** 2026-09-01  
**Status:** exploratory/prospective; not a gate for the current flagship Perspective  
**Parent protocol:** `MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md`

## 0. Motivation and contraction

The motivating intuition is useful only after a major contraction:

- **Rejected:** `number of arXiv papers = human knowledge growth`.
- **Rejected:** `peer-reviewed papers = ground-truth knowledge`.
- **Retained hypothesis:** scientific communities can be modeled as distributed epistemic systems with latent state; papers/preprints/citations/formal artifacts are noisy, selected and institutionally mediated observations of that state.

Science-of-science already treats science as a dynamical multiscale network of people, institutions, ideas and artifacts, and explicitly warns that exponentially growing publication volume should not be equated with idea growth. Large-field work also shows that publication deluge can coincide with canonical ossification. A 2026 Nature study reports that AI-using scientists publish/cite more while collective topical focus narrows. Therefore X6 is a **measurement-validity** problem, not a publication-count exercise.

---

## 1. Central question

> **Can a latent, typed model of collective epistemic capability inferred from multiple observable scientific-artifact channels predict later validated scientific capability or structural change better than simple publication, citation, impact and semantic-novelty baselines?**

A positive answer would support a collective-epistemics measurement programme. It would **not** by itself establish Machine Epistemics as a field.

---

## 2. System-identification framing

Let the unobserved collective epistemic state be

`K_t`.

Observable channels are

`Y_t = {Y_t^preprint, Y_t^journal, Y_t^citation, Y_t^formal, Y_t^software, Y_t^data, Y_t^replication, Y_t^correction, ...}`.

A measurement model takes the schematic form

`Y_t = g(K_t, institutions_t, incentives_t, channel_rules_t, noise_t)`.

The channel/institution terms are explicit because publication artifacts are not transparent readouts of knowledge.

The target is not to recover an unknowable total human epistemic state. All inference is bounded to a declared domain, time interval, artifact universe and validation target.

---

## 3. Unit of analysis

Run the programme at more than one scale; do not assume one aggregation is privileged.

Candidate units:

- subfield × quarter/year;
- problem family × time window;
- theorem/concept cluster × time;
- method/instrument family × time;
- citation/semantic community × time;
- externally curated historical discovery episode.

The primary confirmatory unit must be fixed before model fitting and chosen for adequate temporal resolution and validation data.

---

## 4. Latent state vector

Do not scalarize prematurely. Begin with a typed vector such as

`K_t = (R_t, C_t, V_t, D_t, T_t, G_t, U_t, E_t)`

where candidate dimensions are:

### R — validated reach

Which registered problem/task families can the community reliably solve or explain at time `t`?

### C — cost/efficiency

What resources are required to reproduce/solve/verify registered tasks?

### V — verification/reproducibility depth

How much independent checking, replication, formal verification or calibration backs important claims?

### D — epistemic diversity

How broad is the active hypothesis/representation/problem portfolio after controlling for publication volume?

### T — transport/reuse

Do results/methods transfer to new contexts, problems or domains?

### G — generative/representational repertoire

Are new reusable concepts, methods, representations, instruments or formal abstractions entering and surviving downstream use?

### U — unresolved frontier

Which important distinctions/problems remain unresolved, contested or unmeasurable?

### E — dependence/concentration

How concentrated are evidence sources, data, models, institutions, authors or citation attention?

These coordinates are hypotheses. Each must be dropped if it cannot be operationalized independently enough to validate.

---

## 5. Observable channels

### 5.1 Preprints

Examples: arXiv and field-specific servers.

Treat as **rapid, relatively lightly filtered artifact streams**, not validated knowledge.

Observables may include:

- submissions/versions;
- textual/semantic structure;
- references;
- author/institution networks;
- category labels;
- subsequent curation/publication;
- later corrections/withdrawals;
- code/data/formal-artifact links.

### 5.2 Peer-reviewed publications

A separate selection channel with delay, editorial/venue incentives and field-specific norms. Peer review is a filter, not a truth oracle.

### 5.3 Citation network

Attention/reuse signal with prestige, visibility, strategic and field-size confounding. Preprints themselves are increasingly autonomous citation objects, so `published later` cannot be assumed to define citation legitimacy.

### 5.4 Formal artifacts

For mathematics/software/formal science:

- theorem-library additions;
- proof dependencies;
- verified benchmark solves;
- mechanized formalizations;
- verified reusable lemmas.

This channel is attractive because local correctness is machine-checkable, though formal specification fidelity remains separate.

### 5.5 Software/data/instrument artifacts

Versioned software, datasets, benchmarks, protocols and instrument/calibration standards where persistent identities exist.

### 5.6 Correction/negative channels

Retractions, errata, benchmark invalidations, failed replications, superseded formalizations and calibration changes. A collective epistemic metric must be able to move *backward* on some coordinates.

---

## 6. Baselines

A latent ME-style model must beat simple strong alternatives.

### B0 — publication volume

Papers/preprints per unit time.

### B1 — citation/impact

Raw and field-normalized citation/impact measures.

### B2 — semantic novelty/diversity

Embedding/text novelty, topic count/coverage and semantic-network expansion.

### B3 — disruption/attention turnover

Citation-network disruption/canonical turnover style metrics.

### B4 — science-of-science multivariate baseline

A strong combination of output, citation, semantic, network, team and field-size covariates.

### M — latent collective-epistemic state model

Adds typed validation/reproducibility, capability, cost, dependence, formal/reuse/correction channels as available.

If B4 predicts the validation targets as well as M, X6 contracts to an interpretive framework.

---

## 7. Hostile invariance and falsification suite

A candidate metric/model must be attacked with synthetic and natural perturbations.

### I1 — duplicate invariance

Copy identical papers/artifacts many times without new validation/reuse. Epistemic-state gain should be approximately zero apart from legitimate dissemination effects explicitly modeled separately.

### I2 — paraphrase invariance

Semantic restatement of known content should not create large capability/representation gain.

### I3 — mass low-information generation

A burst of low-information AI-authored papers should primarily move an **activity** channel unless independent capability/verification/reuse changes.

### I4 — false/retracted work

Novel but later invalidated work must not permanently inflate validated epistemic state. The model must support negative revision.

### I5 — citation-ring/popularity shock

Artificial or prestige-driven attention should not be interpreted as equivalent validated capability.

### I6 — venue migration

Moving the same work between preprint/journal channels should not create duplicate epistemic gain.

### I7 — field-size scaling

A field doubling its author/publication population without proportionate change in capability/repertoire should not automatically double epistemic state.

### I8 — fashion/concentration shock

More papers within a shrinking topic manifold may increase output while decreasing/diverging on diversity/reach coordinates. The 2026 AI-and-science result motivates this control.

### I9 — delayed validation

A preprint may initially be uncertain then later gain/lose support. State estimates must update without rewriting the historical observation stream.

### I10 — independent rediscovery

Two genuinely independent derivations may increase robustness/dependence structure even if semantic novelty is low. Duplicate detection must not erase epistemically relevant independence.

---

## 8. Validation targets

A latent state gains scientific meaning only through **future/out-of-sample consequences**.

Potential targets, frozen per domain:

### V1 — future benchmark/problem reach

Does the state at `t` predict which problem families become solvable/verifiable in `t+1...t+k`?

### V2 — downstream reuse

Does a claimed representation/method transition predict reuse in independently authored later work beyond citation count alone?

### V3 — replication/verification survival

Do high-state claims survive later replication/formalization/calibration challenge?

### V4 — solution-cost reduction

Does the community become able to reach the same validated result more cheaply/quickly?

### V5 — cross-domain transfer

Does a method/concept begin to generate validated consequences outside the donor cluster?

### V6 — later canonical replacement/expansion

Use cautiously and only as a secondary target because attention is not truth.

---

## 9. Historical backtest design

### Phase H0 — calibration cases

Use historically well-studied discovery episodes only to test data plumbing and qualitative face validity. They are not confirmatory because retrospective labels are contaminated by hindsight.

### Phase H1 — rolling-origin prediction

Choose a historical cutoff `t`. Fit using only information timestamped <= `t`; predict validation targets in future windows. Roll forward repeatedly.

### Phase H2 — locked modern holdout

Freeze the model before a later time interval and evaluate without retraining on its outcomes.

### Phase H3 — cross-field transfer

Fit/choose hyperparameters on some fields, test on materially different fields. Failure is informative against a universal collective metric.

---

## 10. arXiv-specific role

arXiv is useful because it is:

- large;
- time-stamped;
- versioned;
- relatively early in the dissemination process;
- rich in references/authors/categories/text;
- heterogeneous in quality.

Its lack of universal peer review is **not a fatal flaw** for X6 because arXiv is not the ground-truth target. It is one observation channel whose noise/selection properties must be modeled.

The protocol should exploit arXiv's noise to test whether the latent model can distinguish:

`activity != novelty != impact != validation != capability`.

---

## 11. Peer review as a channel, not oracle

Later journal publication may be used as one observation/validation feature, but not as the sole label `TRUE`.

Reasons include:

- field/venue selection;
- publication delays;
- prestige and novelty preferences;
- negative-result suppression;
- correction/retraction after review;
- preprints increasingly being cited as autonomous scholarly objects.

The model must be capable of representing disagreement between preprint, peer-review, replication and later-use channels.

---

## 12. Causal limitations

A successful predictive latent model does not prove that a detected paper/concept **caused** later capability growth.

Separate:

- descriptive state reconstruction;
- predictive validity;
- causal claims about mechanisms of scientific progress.

Causal claims require quasi-experimental/natural-experiment/intervention designs and explicit confounder assumptions.

Do not infer that AI use caused contraction from association alone beyond the source study's supported design.

---

## 13. Field-specific measurement risk

Publication/citation behaviors vary heavily by field. Required controls include:

- field/venue/year normalization;
- preprint adoption rate;
- conference vs journal norms;
- author/team size;
- database coverage changes;
- language/geography/institution coverage;
- subfield taxonomy drift;
- version linking/deduplication.

A universal scalar is rejected unless it survives these shifts. Field-specific latent models may be the correct terminal.

---

## 14. Success ladder

### C0 — failure

M adds no predictive/structural value beyond B4 or fails hostile invariances.

### C1 — sensor model

M better separates activity/attention from later validation/capability within one field.

### C2 — robust latent state

C1 plus multiple hostile invariances and rolling-origin validation across several time windows.

### C3 — cross-field generalization

C2 plus useful transfer to materially different scientific fields after native normalization.

### C4 — mechanistic collective epistemics

Requires additional causal/mechanistic evidence linking specific collective structures/transitions to later epistemic capability. Not claimable from artifact prediction alone.

---

## 15. Kill criteria

Contract or abandon the collective-ME measurement claim if:

- publication/citation/topic baselines predict future targets equally well;
- duplicates/paraphrases inflate state materially;
- retractions/invalidations cannot reduce previously inferred validation;
- model mostly learns venue prestige/field size;
- results do not survive temporal holdout;
- results do not survive database-coverage/field-normalization checks;
- latent dimensions are not independently interpretable/recoverable;
- model requires hindsight labels unavailable at inference time;
- arXiv-specific results fail on another artifact channel;
- only a scalar “knowledge growth score” survives while typed components are unstable.

---

## 16. Relationship to Machine Epistemics field claim

X6 is **downstream and optional**.

A positive X6 would show that some ME-style concepts can support measurement of distributed scientific systems. It cannot rescue a failed individual-agent field residual in ME-X1/2/5.

A negative X6 does not kill the individual-agent programme either; the collective system may simply require different abstractions.

No flagship field claim should depend on X6 before this protocol is executed and independently assessed.

## Terminal

```text
ARXIV = NOISY_OBSERVATION_CHANNEL
PEER_REVIEW = SECOND_IMPERFECT_CHANNEL
PAPER_COUNT = ACTIVITY_NOT_KNOWLEDGE
CITATIONS = ATTENTION_REUSE_SIGNAL_NOT_TRUTH
COLLECTIVE_STATE = TYPED_LATENT_VECTOR_NOT_UNIVERSAL_SCALAR
TEMPORAL_PREDICTIVE_VALIDATION = REQUIRED
HOSTILE_INVARIANCES = REQUIRED
CAUSAL_PROGRESS_CLAIM = NOT_AUTHORIZED_BY_PREDICTION
FLAGSHIP_GATE = FALSE
PROTECTED_OUTCOMES_INSPECTED = FALSE
```
