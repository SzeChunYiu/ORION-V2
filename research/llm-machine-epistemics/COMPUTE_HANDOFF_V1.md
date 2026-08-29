# Compute Handoff V1 — LLM Machine Epistemics Theory

**Issue:** #51  
**Branch:** `research/llm-epistemic-sufficiency-theory-20260829`  
**Rule:** the conceptual object is already defined. An AI picking this up should verify, falsify and calculate; it should not restart the research programme or silently replace the theorem identity after seeing results.

## 0. What is already done

Do **not** spend a new session rediscovering these items:

- research question and paper identity;
- predictive-state versus responsibility-state distinction;
- five-role expert panel and veto boundaries;
- operational responsibility family boundary;
- finite/discrete formal setup;
- Lemma 1 and T1–T7 candidate theorem statements/proof sketches;
- exact deterministic overhead candidate `H(Q|S_P)`;
- log-loss deficiency identity `I(Q;H|Z)`;
- post-processing and new-observation information identities;
- known-answer fixtures CE1–CE5;
- nearest-work parent families and direct 2026 representation-identifiability collision;
- manuscript architecture, nonclaims, journal target and contraction conditions.

The remaining queue is intentionally computational / independent-audit work.

---

# P0 — Independent formal verification of T1–T7

## Task P0.1 — mechanize the finite probability objects

Implement a small finite probability-space model in Lean 4 + Mathlib if feasible. If Lean probability formalization becomes disproportionately expensive, use Isabelle/HOL or Coq, or provide two independent executable symbolic checkers plus a human-readable proof ledger. Do not weaken theorem statements merely to fit a tool without recording the loss.

Required objects:

- finite history set `H` with positive-mass support;
- future conditional law `P(Y|H=h)`;
- predictive equivalence classes;
- deterministic representation `Z=f(H)`;
- deterministic/stochastic responsibility variables as required by each theorem;
- entropy / conditional entropy / mutual information for finite rational distributions.

### Output

`research/llm-machine-epistemics/formal/` containing proof source, toolchain/version pin, build command and theorem-name map back to `THEORY_V1.md`.

### Pass

Every formal theorem statement is semantically equivalent to the paper statement under its declared finite assumptions.

### Fail / revise

If the formal checker requires an assumption absent from `THEORY_V1.md`, add the smallest explicit assumption and record it in a `FORMAL_ASSUMPTION_DELTA.md`. Never silently strengthen premises.

---

## Task P0.2 — verify Lemma 1 / T1

Mechanically check:

1. any deterministic predictive-sufficient `Z` refines the predictive quotient;
2. predictive-equivalent histories with different `Q` laws force responsibility insufficiency of `S_P`;
3. positive-mass conditional-law disagreement yields positive conditional mutual information under the stated support conditions.

### Hostile mutations

- zero-probability history endpoints;
- histories with equal MAP `Q` but unequal full `Q` law;
- one-step-equal but full-future-different histories;
- full-future-equal histories.

The main theorem must use the full declared future, not accidentally only the next token.

---

## Task P0.3 — verify T2 maximal predictive compression

Target statement in finite deterministic case:

- predictive sufficiency gives `H(S_P|Z)=0`;
- `H(Z)=H(S_P)+H(Z|S_P)`;
- entropy minimality forces `H(Z|S_P)=0`;
- hence `Z` and `S_P` are almost-surely isomorphic;
- any `Q` not sufficient from `S_P` remains insufficient from an entropy-minimal predictive `Z`.

### Countermodel search

Exhaustively search what fails when each assumption is removed independently:

- `Z` stochastic rather than deterministic;
- predictive sufficiency approximate rather than exact;
- state minimality measured by cardinality instead of entropy;
- continuous/non-finite spaces;
- support contains zero-mass nominal states;
- `H(Z)=H(S_P)` replaced by `H(Z)<=H(S_P)+delta`.

### Required output

A theorem-assumption table with one minimal counterexample for every assumption that is genuinely necessary.

---

## Task P0.4 — verify T3 exact deterministic overhead

For finite deterministic `Q=q(H)`, independently prove/check

`inf_U H(U|S_P) = H(Q|S_P)`

subject to `H(Q|S_P,U)=0`.

### Attack variants

- allow stochastic `U`;
- constrain `U` cardinality;
- require a single code across several responsibility distributions;
- require separate exact recovery of components versus joint responsibility vector;
- allow epsilon error rather than exact recovery.

The exact theorem can remain finite/deterministic; variants belong to T8 unless they yield a clean stronger theorem.

---

## Task P0.5 — verify T4–T7

Mechanically check:

- `H(Q|Z)-H(Q|H)=I(Q;H|Z)` under the correct Markov condition;
- post-processing monotonicity for `Q-H-Z-W`;
- new observation gain `H(Q|Z)-H(Q|Z,X)=I(Q;X|Z)`;
- responsibility-family refinement and entropy monotonicity;
- strictness iff added responsibility vector has positive conditional entropy given the smaller joint state.

### Mandatory negative controls

- responsibility already measurable from `S_P` gives zero overhead;
- an evidence-free computation may improve a **restricted decoder's** performance even though Bayes-optimal information does not increase;
- correlated responsibilities make joint overhead smaller than the sum of individual overheads.

---

# P1 — Exhaustive finite countermodel battery

Build a deterministic enumerator over small finite spaces rather than relying only on hand examples.

Suggested scale:

- history support sizes `|H| = 2..6`;
- future alphabets `|Y| = 2..4`;
- deterministic responsibilities `|Q| = 2..4`;
- all set partitions as candidate deterministic representations where tractable;
- rational probability masses with a bounded denominator grid for stochastic-law tests.

For each generated world:

1. compute predictive equivalence exactly;
2. enumerate candidate representations/partitions;
3. classify predictive sufficiency;
4. classify responsibility sufficiency;
5. calculate state entropy, `H(Q|S_P)`, `I(Q;H|Z)`;
6. verify T1–T7 identities/inequalities;
7. emit the smallest counterexample whenever a mutated theorem fails.

### Outputs

- machine-readable `FINITE_COUNTERMODEL_BATTERY_V1.json`;
- exact-source generator;
- `COUNTERMODEL_SUMMARY_V1.md`;
- frozen seed/version even if enumeration is deterministic;
- hashes of all headline fixtures.

### Scientific rule

A found counterexample narrows the theorem. It does not get discarded because it harms the paper.

---

# P2 — Solve one nontrivial approximate predictive–epistemic frontier

T8 is the main unfinished mathematical strengthening.

## Candidate family A — binary hidden responsibility through a predictive fibre

Construct a model with:

- predictive state `S_P`;
- within each predictive fibre, binary responsibility `Q` with fibre-dependent Bernoulli parameter;
- stochastic encoder `U` carrying a rate budget beyond `S_P`;
- epistemic log-loss or error constraint.

Attempt to derive

`R_epi(epsilon) = inf I(H;U|S_P)`

or reduce it exactly to a conditional binary rate-distortion / information bottleneck form, then identify any LLM-responsibility-specific endpoint or strict-separation consequence.

## Candidate family B — multiple correlated responsibilities

Use two correlated binary responsibilities inside a predictive fibre and characterize the difference between:

- preserving each marginal responsibility to error tolerance;
- preserving the joint responsibility vector;
- allocating state rate to one responsibility versus the other.

This may yield a more genuinely ORION-like non-compensatory frontier.

### Kill rule

If the entire derivation is exactly a standard named conditional rate-distortion theorem with no new consequence, mark T8 `PARENT_OWNED` and do not manufacture terminology.

### Positive gate

At least one closed-form or sharp computable frontier with a result that a language-model representation researcher could not obtain by reading a single parent theorem and substituting variable names.

---

# P3 — Reproducible nearest-work theorem matrix

This is a literature-computation task, not free-form essay writing.

Search at least:

- Crossref/OpenAlex for metadata and citation linkage;
- Semantic Scholar where available;
- arXiv for current theory/preprints;
- ACL Anthology for NLP/LLM internal-state papers;
- JMLR/PMLR/NeurIPS/ICLR archives for representation/sufficiency work.

Deduplicate by DOI, arXiv id and normalized title.

## Search families

1. `minimal predictive state sufficient statistic future`
2. `causal states secondary task sufficient representation`
3. `predictive state reward predictive representation`
4. `minimal sufficient representation multiple tasks`
5. `conditional sufficient statistic task family`
6. `multi-task information bottleneck state complexity`
7. `conditional rate distortion side information sufficient statistic`
8. `language model internal representation sufficiency`
9. `LLM belief representation causal use`
10. `LLM truth uncertainty hidden state`
11. `representation identifiability predictor fibre`
12. `epistemic representation neural network`

## Required columns

- citation id;
- title/authors/year/venue;
- stable identifier;
- exact theorem/proposition/section if known;
- predictive-state minimality?;
- secondary responsibility/task sufficiency?;
- exact entropy overhead?;
- multi-responsibility refinement?;
- approximate rate region?;
- autoregressive/LLM specialization?;
- internal causal-use criterion?;
- closest T1–T9 overlap;
- verdict: `PARENT_OWNED`, `PARTIAL_OVERLAP`, `NO_DIRECT_OVERLAP`, `CANNOT_CHECK_FULL_TEXT`.

### Output

`NEAREST_THEOREM_CLAIM_MATRIX_V1.csv` plus a short generated markdown summary. Do not infer theorem contents from abstracts when the full theorem is unavailable; use `CANNOT_CHECK_FULL_TEXT`.

---

# P4 — Generate publication figures/tables only from checked artifacts

After P0–P3 close:

1. theorem ownership table;
2. predictive-fibre / responsibility-refinement schematic generated from CE1/CE4 data;
3. exact-overhead table over enumerated fixtures;
4. assumption/counterexample matrix for T2;
5. approximate `R_epi(epsilon)` curve if T8 survives.

No decorative figure should appear in the paper unless it answers a scientific question.

---

# P5 — Hostile reviewer simulation

After mechanization and theorem matrix:

Run at least five independent critique lenses:

- information theorist: “this is conditional RD with new nouns”;
- causal-state theorist: “reward-predictive states already own this”;
- LLM theorist: “real transformers are not entropy-minimal causal states”;
- epistemologist: “your `Q` variables are benchmark labels, not epistemic responsibility”;
- JMLR editor: “correct theorem, insufficient ML consequence.”

For each critique, emit:

- exact challenged claim;
- strongest parent/reference;
- whether the criticism is fatal, narrows scope or is answered;
- manuscript change required;
- resulting paper terminal.

The review process is not allowed to self-award independent human review authority.

---

# Final computation-only completion checklist

- [ ] P0 formal verification T1–T7 complete.
- [ ] Every changed/missing theorem assumption surfaced in the manuscript.
- [ ] P1 exhaustive countermodel battery complete.
- [ ] At least one negative-control fixture verifies zero epistemic overhead.
- [ ] P2 one approximate frontier solved or honestly contracted as parent-owned.
- [ ] P3 bibliographic theorem matrix complete and deduplicated.
- [ ] Direct 2026 collisions fully integrated.
- [ ] P4 tables/figures regenerated from frozen checker outputs.
- [ ] P5 hostile reviewer matrix complete.
- [ ] Final terminal assigned without requiring LLM training.

No GPU-scale LLM training belongs in this handoff.
