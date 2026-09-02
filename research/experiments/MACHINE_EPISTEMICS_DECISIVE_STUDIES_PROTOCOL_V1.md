# Machine Epistemics — Decisive Studies Protocol V1

**State date:** 2026-09-01  
**Status:** prospective design only; no protected outcome has been inspected under this protocol  
**Branch:** `codex/machine-epistemics-hardening-wave`  
**Base evidence/mechanics head:** `4165dd2d3c621d9f60e0ff492560baf3afbf7c5f`

## 0. Non-authority and pre-registration rule

This protocol does not grant field status, novelty, scientific truth, architecture adoption or publication authority. It exists to make the next Machine Epistemics claims *harder to obtain*.

Before any protected execution for a study below, freeze:

- exact task/case identities and train/development/protected partitions;
- base model/provider/version and inference settings;
- tool/library/data snapshots;
- information available to every arm;
- evaluator identities and adjudication rules;
- wall-clock/token/tool-call/resource budgets;
- primary and secondary outcomes;
- tie/contraction rule;
- missing/censored outcome handling;
- randomization/seeds where applicable;
- acceptable pilot-only tuning surface;
- independent custody of protected labels/results.

No success threshold may be chosen after protected outcomes are inspected.

## 1. Scientific hypothesis under test

### H_ME

There exist recurring scientific decisions for which **cross-transition epistemic control**—coupling evidence/provenance, evaluator validity, dependence, representation/model state, transport, obligations, selective reopening, stopping and authority—changes protected decisions beyond the strongest faithful parent composition under matched information and resources.

### H0 — strongest-parent sufficiency

An information-matched composition of mature parents makes the same protected decisions with equal or better reliability/cost.

**Programme contraction rule:** if H0 ties or wins on the protected quality-cost frontier after reasonable prespecified repair, do not reinterpret the result as Machine Epistemics superiority. Contract the claimed residual.

---

## 2. Baseline hierarchy

Every applicable study should include the strongest feasible members of this hierarchy.

### B0 — direct task system

Same base model/tools, no explicit ME control layer.

### B1 — calibrated uncertainty / abstention

Adds confidence/calibration or selective prediction without ME-specific state semantics.

### B2 — provenance + verifier runtime

Typed execution/provenance/verification controls comparable to contemporary scientific-agent runtimes and verification-first systems.

### B3 — diagnosis/metareasoning/VoI

Model-based diagnosis, rational metareasoning, active experiment design and, where appropriate, M-open model discovery/hypothesis expansion.

### B4 — truth-maintenance/assurance federation

TMS/ATMS or belief revision + provenance + assurance/validation + parent-specific transport/measurement/evidence modules.

### B5 — strongest faithful parent federation

The union/composition of parent mechanisms required by the task. It receives no less task information, evaluator access or tool access than the ME arm.

### M — Machine Epistemics candidate

ORION-V2 reference semantics as needed: explicit bounded state, obligations, witnessed obstruction, minimum-sufficient escalation, transition receipt, typed transfer, selective reopening, atlas/horizon and/or regime-change contracts.

**No weak-baseline victory counts.** The field claim compares M primarily with B5.

---

## 3. ME-X1 — Transition Coupling Benchmark

### 3.1 Question

Can every local operation be correct under its local contract while the resulting scientific-state transition is still wrong or unwarranted, and does explicit cross-transition control prevent that error beyond B5?

### 3.2 Case families

Each family must contain positive, negative and ambiguity/CANNOT_CHECK instances.

1. **Claim-binding error:** valid output attached to the wrong registered claim/problem identity.
2. **Measurement-calibration break:** computation is correct for a measurement whose calibration/comparability has become invalid.
3. **Hidden dependence:** apparently independent supports share data/source/model/instrument ancestry.
4. **Invalid transport:** donor/local result is valid but target context relation does not license reuse.
5. **Defeated prerequisite:** downstream result remains locally valid but a sufficient prerequisite/support family has failed.
6. **Blind evaluator:** evaluator cannot expose the failure class asserted by the conclusion.
7. **Authority mismatch:** evidence warrants belief revision but not the requested operational/action authority.
8. **Formal proof / wrong specification:** proof checker accepts a theorem that does not faithfully encode the intended scientific/mathematical question.
9. **Local compatibility / global obstruction:** registered local pieces agree pairwise but no separate global witness exists or an obstruction is present.
10. **Fully warranted controls:** all relevant contracts are satisfied; conservative systems must not manufacture uncertainty/reopening.

### 3.3 Arms

`B0`, `B2`, `B4`, `B5`, `M`, plus field-level ablations of M:

- `M_MINUS_PROVENANCE_DEPENDENCE`
- `M_MINUS_EVALUATOR_CONTRACT`
- `M_MINUS_TRANSPORT`
- `M_MINUS_REOPENING`
- `M_MINUS_AUTHORITY`
- `M_MINUS_UNRESOLVED_TERMINAL`
- `M_MINIMAL_RECEIPT` chosen prospectively from development cases only.

### 3.4 Primary outcomes

Per case, adjudicate the exact transition action among a finite registered set such as:

- `UPDATE`
- `PRESERVE`
- `SELECTIVELY_REOPEN`
- `REVALIDATE`
- `REQUEST_NEW_EVIDENCE`
- `BLOCK_TRANSPORT`
- `DEFER_CANNOT_CHECK`
- `ABSTAIN_AUTHORITY`

Measure:

- exact transition-decision accuracy;
- false update rate;
- over-/under-reopening;
- invalid transport rate;
- false closure rate;
- correct unresolved/authority abstention;
- resource use.

### 3.5 Required mechanistic evidence

A field-level residual requires at least one pre-registered case family where:

1. B5 has all necessary local parents;
2. B5 makes a systematic composition error;
3. M avoids the error because of a named cross-transition condition;
4. removing that condition in the matched ablation restores the error;
5. the result transfers to at least one independently authored/native-domain case family.

Otherwise ME-X1 is at most a benchmark/integration result.

### 3.6 Kill conditions

- B5 ties/wins across protected case families and resource frontier;
- M only wins because it receives extra labels/state not available to B5;
- M becomes uniformly conservative and avoids errors mainly by refusing valid updates;
- no individual ME field has omission-specific causal value.

---

## 4. ME-X2 — Obstruction Classification and Minimum Escalation

### 4.1 Question

Can the system distinguish *what blocks progress* and choose the smallest intervention level capable of resolving it?

### 4.2 Registered obstruction families

- `SEARCH_INSUFFICIENT`
- `MISSING_PREMISE_OR_DATA`
- `MODEL_FAMILY_INADEQUATE`
- `REPRESENTATION_INSUFFICIENT`
- `PROBE_ACTION_INSUFFICIENT`
- `MEASUREMENT_OR_EVALUATOR_BLIND`
- `FORMALISM_OR_OPERATOR_INSUFFICIENT`
- `PROBLEM_OBJECTIVE_MISSPECIFIED`
- `TOOL_INSTRUMENT_INADEQUATE`
- `WORKFLOW_INADEQUATE`
- `NO_ESCALATION_NEEDED`
- `CANNOT_IDENTIFY`

### 4.3 Intervention levels

Use the existing Jump lattice, but do not presume it is correct. Register the oracle minimal responsible level per known-answer case before model execution:

0. action/parameter;
1. local repair/composition;
2. model/hypothesis expansion;
3. representation regime transition;
4. problem/objective reformulation;
5. method/tool/instrument invention;
6. workflow/meta-skill revision;
7. framework revision;
8. constitution proposal only where an external-authority test makes sense.

### 4.4 Task construction

Create paired cases with similar observed symptoms but different causes. At least one hostile decoy per obstruction family must reward a simpler lower-level repair so that “escalate when stuck” is penalized.

Where exact ground truth is unavailable, register a blinded adjudication packet and allow `CANNOT_IDENTIFY` rather than forcing a label.

### 4.5 Arms

- B0 repeated search;
- B1 uncertainty threshold;
- B3 diagnosis/metareasoning/VoI;
- MDA-style model-family expansion where applicable;
- B5 strongest federation;
- M witnessed obstruction + discriminator + lower-level disposition + minimum-level policy.

### 4.6 Outcomes

- obstruction classification accuracy/calibration;
- minimal-intervention level accuracy;
- false escalation;
- missed escalation;
- verified task success;
- intervention cost;
- regret relative to oracle minimal responsible intervention;
- recurrence after an incorrect intervention.

### 4.7 Mechanistic mediation

A claimed ME gain must be statistically/mechanistically associated with correct obstruction identification. If M wins while obstruction labels are wrong/uninformative, the proposed mechanism is not supported.

### 4.8 Kill conditions

- B3/B5 matches routing and resource frontier;
- gains are explained by more retries/search;
- false escalation cost offsets success gains;
- obstruction taxonomy is unstable under changed vocabulary/native-domain review.

---

## 5. ME-X3 — Formal Mathematical Discovery and Regime Change

### 5.1 Purpose

Use formal mathematics because proof checking supplies an unusually strong local verifier, while still preserving the crucial distinction between a valid proof and a faithful formalization of the intended problem.

### 5.2 Environment

- Lean version and mathlib commit frozen;
- no network access during protected solving unless a retrieval arm is explicitly registered;
- theorem names/metadata scrubbed where leakage is plausible;
- exact model and inference budget bound;
- proof checker result separated from specification-intent adjudication.

### 5.3 Problem strata

1. `DIRECT_SEARCH`: existing representation and library are sufficient.
2. `MISSING_LEMMA`: useful intermediate abstraction/lemma is needed.
3. `REPRESENTATION_CHANGE`: alternative encoding/change of variables/dual view materially reduces proof complexity.
4. `DECEPTIVE_CHANGE`: representation change looks attractive but adds cost; direct route is sufficient.
5. `UNDERDETERMINED`: current probes/lemmas do not distinguish candidate routes.
6. `SPECIFICATION_MISMATCH`: a provable statement differs materially from the intended natural-language problem.
7. `TRANSFER`: an invented lemma/representation should help a held-out related family.

### 5.4 Baselines

- direct LLM + Lean search;
- retrieval/library search;
- self-reflection/retry;
- existing lemma-generation/abstraction parent method;
- strongest proof-search system available under the same tool budget;
- M obstruction diagnosis + minimum escalation + versioned representation/lemma transition.

### 5.5 Outcomes

- formally verified solve rate;
- specification-intent match;
- proof/search cost;
- false representation-change rate;
- useful invented lemma/abstraction reuse on held-out tasks;
- transfer gain;
- calibration of `CANNOT_CHECK`/unsolved cases.

### 5.6 Contamination controls

- time-sliced/newly generated theorem families with machine-checkable provenance;
- theorem-name/string search audit;
- paraphrase controls;
- hidden transformations not exposed in problem text;
- compare against retrieval-only gains.

### 5.7 Kill conditions

- gains vanish against matched lemma/abstraction parents;
- gains are solely extra compute or library exposure;
- “representation changes” are post-hoc descriptions of ordinary proof search;
- specification mismatch rises enough to dominate verified-solve gains.

---

## 6. ME-X4 — Selective Reopening under Dynamic Evidence

### 6.1 Question

When evidence, calibration, transport or evaluator validity changes, can the system reopen exactly the affected commitments while preserving independent support?

### 6.2 Known-answer graph generator

Generate versioned support graphs containing:

- multiple sufficient support families;
- shared ancestors/dependence;
- retractions/corrections;
- calibration invalidation;
- context-transport invalidation;
- evaluator replacement/failure-class changes;
- independently supported downstream claims;
- unresolved/censored edges.

The generator must expose exact expected reopening sets before protected agent execution.

### 6.3 Arms

- TMS/ATMS;
- Bayesian/support graph;
- provenance-only invalidation;
- assurance-case update;
- B5 strongest federation;
- M transition receipt + support-family dependence + selective reopening.

### 6.4 Outcomes

Exact reopened set, exact preserved-valid set, over-/under-reopening, recovery after corrective evidence and runtime cost.

### 6.5 Kill

If B5 exactly recovers the same reopening semantics and M adds no protected decision or cost advantage, selective reopening is parent-owned and remains only an interface convention.

---

## 7. ME-X5 — Cross-Domain Field Residual Test

### 7.1 Purpose

This is the **field-level** discriminator. No single synthetic benchmark can establish a cross-disciplinary residual.

### 7.2 Minimum epistemic modes

At least three independently authored/native-reviewed modes:

1. formal verification/mathematics;
2. computational or experimental physical science;
3. evidence synthesis/measurement/revision.

A fourth observational/social domain is optional but preferred if the outcome and evaluator contracts can be made sufficiently crisp.

### 7.3 Native ownership rule

Each domain receives a rotating native-domain reviewer who reconstructs:

- native objects;
- native strongest methods;
- native failure classes;
- native decision outcomes;
- which ORION abstractions are lossy or invalid.

Cases may enter the protected suite only after native recovery passes.

### 7.4 Parent federation construction

B5 is not a strawman. Build it by giving each parent mechanism its native best role, with ordinary engineering glue allowed. The federation may share state when scientifically required. The ME residual cannot be defined as “parents were kept artificially separate.”

### 7.5 Primary outcome

Pre-register a vector, not only a pooled scalar:

- false scientific transition;
- missed warranted transition;
- invalid transport;
- false closure;
- wrong reopening;
- unnecessary escalation;
- unresolved-state calibration;
- resource cost.

Report per-domain and per-failure-class outcomes. A pooled average cannot hide a domain in which M is clearly inferior.

### 7.6 Field support rule

Evidence for an emerging-field residual requires:

- a stable transition object independently recognizable across domains;
- at least one nontrivial cross-transition mechanism with causal ablation;
- protected residual beyond B5 in more than one epistemic mode;
- no explanation by additional information/resources;
- independent adjudication;
- fresh prior-art/demarcation audit.

Even this supports only an **emerging-field hypothesis**, not an established field.

### 7.7 Field kill

If B5 ties/wins or the common object dissolves under native semantics, contract to integration/bridge/benchmark programme.

---

## 8. ME-X6 — Collective Epistemics / Scientific Output as Noisy Sensor

**This study is exploratory/prospective and does not gate the current flagship.**

### 8.1 Measurement model

Let `K_t` be an unobserved collective epistemic-capability state and `Y_t^j` observable channels:

`Y_t^arXiv`, peer-reviewed papers, citations, formal-library changes, software/data releases, benchmark capability, replications, corrections/retractions, downstream reuse.

Do not define `K_t` as publication count.

### 8.2 Candidate state dimensions

- validated problem reach;
- solution/verification cost;
- independent evidence depth;
- representation/concept repertoire;
- transport scope;
- calibration/reproducibility;
- unresolved frontier;
- diversity/concentration of exploration.

### 8.3 Hostile invariance tests

A candidate metric should be approximately invariant or appropriately penalized under:

- exact duplicates;
- semantic paraphrases;
- citation-ring/popularity shocks;
- mass low-information AI generation;
- later retracted/invalidated papers;
- field-specific publication-rate changes.

### 8.4 Predictive validation

Fit only on past windows. Test whether the latent state predicts later verified capability/reuse/replication better than activity, citation and text-novelty baselines on held-out future windows.

### 8.5 Interpretation boundary

arXiv is a noisy observation channel of epistemic activity; it is not a ground-truth knowledge ledger. Peer review is another imperfect channel, not an oracle.

---

## 9. ME-X7 — Claim-Sufficient External Witnesses

### 9.1 Question

Can scientific accountability be preserved with a compact external witness even when the internal machine computation is not human-mimetic or fully trace-exposed?

### 9.2 Arms

- final answer only;
- provenance-only record;
- full natural-language reasoning trace where available;
- claim-sufficient structured witness;
- proof/verification artifact where appropriate.

### 9.3 Outcomes

Failure detection, replay/reconstruction, independent audit agreement, privacy/trace exposure where relevant, latency/storage and task capability.

### 9.4 Kill

Witness compression is rejected if it systematically hides decision-critical failure classes or if its overhead removes the claimed machine-native advantage.

---

## 10. Formal targets coupled to the experiments

### FT-1 — Composition counterexample

Find an exact finite episode where every parent-local action is valid but naive composition is scientifically invalid. Bind the missing cross-transition condition. If no nontrivial example survives ordinary interface engineering, weaken H_ME.

### FT-2 — Receipt recoverability

For a declared decision family, determine which state/receipt fields are necessary to recover the decision. No universal minimality claim without proof.

### FT-3 — Escalation regret

Define over-/under-escalation regret relative to a registered intervention lattice and oracle minimal responsible intervention.

### FT-4 — Reopening boundary

Prove or countermodel the bounded sufficient-support reopening rule; explicitly separate support-defeat reopening from contradiction, scope change and other causes.

### FT-5 — Horizon consequence

Separate `DISTINGUISHABILITY_GAIN` from `DECISION_RELEVANT_EPISTEMIC_GAIN`. Strict partition refinement alone is not progress.

### FT-6 — Regime-transition parent mapping

Map ORION generative-regime/Jump/concept-transition semantics to Wang & Buehler's 2026 categorical regime-transition framework. Equivalent objects are marked parent-recovered before any residual claim.

---

## 11. Global integrity rules

1. Preserve all adverse P-A/P-B/P-C/P-D/P-F history.
2. Do not revive a failed architecture through a narrower study unless the new claim/protocol is prospectively frozen.
3. Do not pool away domain-specific harm.
4. Do not let abstention manufacture apparent accuracy without coverage/cost accounting.
5. Do not use LLM-as-judge alone for a claim whose correctness can be checked formally or by native evidence.
6. Do not use author-created synthetic cases as the only evidence for a field-level residual.
7. Search absence is not novelty evidence.
8. A complete receipt is non-authorizing.
9. A representation change is not progress merely because it is novel.
10. A successful proof is not a faithful formalization merely because Lean accepts it.
11. Publication/citation volume is not knowledge growth.
12. External scientific/community authority is required for established-field status.

## 12. Current terminal

```text
PROTOCOL_STATUS = PROSPECTIVE_UNEXECUTED
PROTECTED_OUTCOMES_INSPECTED = FALSE
FIELD_HYPOTHESIS = OPEN
STRONGEST_PARENT_NULL = ACTIVE
PRIMARY_DECISIVE_STUDIES = ME_X1__ME_X2__ME_X5
FORMAL_MATH_STUDY = ME_X3
DYNAMIC_REOPENING_STUDY = ME_X4
COLLECTIVE_EPISTEMICS = ME_X6_EXPLORATORY
EXTERNAL_WITNESS_STUDY = ME_X7
NEGATIVE_HISTORY = IMMUTABLE_INPUT
PARENT_SUFFICIENCY = VALID_SUCCESSFUL_TERMINAL
FIELD_ESTABLISHED = FALSE
```
