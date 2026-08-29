# JMLR Editor Decision Brief V1

**Paper:** Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations  
**Archetype:** theory/proof + analytical assessment framework  
**Target:** Journal of Machine Learning Research, regular article  
**Stage:** pre-submission scientific triage

## Editor-facing decision proof

### Question

A representation may be adequate for the language-prediction target on which it is evaluated and for the current decision required by a task. Does that current adequacy certify that the representation also retains what will be needed to revise correctly after later evidence?

### Bounded answer

No, not in general. Under a registered prediction protocol, the paper constructs a finite process in which two representations are equally adequate for the current linguistic target and the same unique current action, yet only the augmented representation supports the correct pair of future actions after the same later evidence. The exact construction has

`C_stat^* = 0`, `C_dyn^* = 1 bit`, and `Omega_dyn = 1 bit`.

### Decisive evidence

1. human-readable finite proof;
2. independently implemented deterministic finite audits and countermodel searches;
3. explicit assumption-mutation analysis;
4. a practical Prospective Revision Audit V3 turning the separation into an evaluation protocol.

### Strongest alternative interpretation

The theorem may be viewed as a direct consequence of classical decision sufficiency, predictive/information-state theory and finite-state compatibility. The manuscript accepts that ownership. Its standalone residual is the **representation-assessment task**: first match current prediction and decision, then manipulate/compare retained historical state, exclude alternate reconstruction routes, present common later evidence, and score update plus maintain/selective reopening.

### Why the advance matters to ML

Modern language-model and agent systems increasingly compress context, summarize memory, route retrieval, use KV/hidden-state memory and make decisions over long-lived interactions. Current evaluation can show that a compressed state preserves present loss/performance while remaining silent about evidence-responsive behavior that becomes distinguishable only later. The paper provides a formal reason and a concrete audit for that blind spot.

### Boundary

The manuscript does not establish that deployed LLMs generally have this failure, does not introduce a universal epistemic-state calculus, and does not claim priority for predictive-state, decisional-state, information-state or memory-minimization theory.

## Target-criterion map

| JMLR criterion | Current paper evidence | Status |
|---|---|---|
| New insight into learning-system behavior | current adequacy cannot certify future revision adequacy | supported finite theorem |
| Formalization of new assessment task | Prospective Revision Audit V3 | primary candidate contribution |
| Analytical framework for practical methods | prediction/current/prospective axes + collision/compatibility diagnostics | supported framework |
| Practical utility of theory | memory/compression/agent-state evaluation prescription | bounded inference |
| Clear predecessor acknowledgement | strongest-parent contraction + citation matrix | strong |
| Broader ML interest | long-lived LLM/agent representations, memory/compression | editorial-risk item |
| Reproducibility | deterministic finite audit + proof + receipts | strong |

## Major concern ledger

### C-JMLR-01 — “This is classical state sufficiency with new terminology.”

**Severity:** blocking if the manuscript is presented as new state theory.  
**Resolution test:** generic mathematics is explicitly parent-owned; title/abstract/contributions lead with the assessment problem; contribution survives deletion of `Machine Epistemics` terminology.  
**Current state:** resolved by claim contraction.

### C-JMLR-02 — “The finite witness is too trivial for JMLR.”

**Severity:** target-significance risk, not correctness defect.  
**Resolution test:** paper must show why the witness changes an evaluation question for practical representation compression/memory and provide an operational audit unavailable from present-only evaluation.  
**Current state:** partially resolved by Protocol V3; external editorial judgment remains decisive.

### C-JMLR-03 — “Belief-R or memory-compression papers already test this.”

**Severity:** novelty blocker if exact sequence is reproduced by a direct parent.  
**Resolution test:** compare the full registered audit sequence against direct neighbors: present-equivalence gate, state-retention intervention, common later evidence, alternate-channel/parametric reconstruction gate, update+maintain/selective reopening, joint compatibility.  
**Current state:** no direct full match found through 2026-08-29 search frontier; bounded claim only.

### C-JMLR-04 — “You do not demonstrate the effect in a real LLM.”

**Severity:** potentially blocking for impact, not for theorem validity.  
**Resolution test:** establish that JMLR can evaluate the work as a theoretical/assessment-framework paper; keep all empirical LLM claims absent. Optional frozen-model execution can strengthen but is not allowed to become a hidden prerequisite post hoc.  
**Current state:** external editorial risk remains open.

### C-JMLR-05 — “The prediction target was chosen weakly so the witness is artificial.”

**Severity:** technical interpretation blocker.  
**Resolution test:** register reference input protocol `rho`; add stronger controlled-target condition in which the intervention family is included and the premium may contract.  
**Current state:** resolved in V9/Protocol V3.

### C-JMLR-06 — “Removing context does not prove information was removed.”

**Severity:** causal-attribution blocker for empirical extensions.  
**Resolution test:** alternate-channel and parametric-reconstruction gates; `CANNOT_CHECK` when absence cannot be established.  
**Current state:** resolved protocol design; no empirical claim made.

### C-JMLR-07 — “Pairwise collisions miss tied-action incompatibility.”

**Severity:** formal diagnostic defect.  
**Resolution test:** use full joint acceptable-action intersection for each representation/evidence cell.  
**Current state:** resolved in compatibility criterion; simple checker remains mechanical.

## Editorial triage terminal

```text
SCOPE = PLAUSIBLE_JMLR
SCIENCE_CORRECTNESS = STRONG_WITHIN_SCOPE
NEW_GENERIC_THEORY = NO
ASSESSMENT_FRAMEWORK_RESIDUAL = PLAUSIBLE
BROADER_ML_SIGNIFICANCE = BORDERLINE_EXTERNAL_JUDGMENT
REAL_LLM_EMPIRICAL_RESULT = NOT_REQUIRED_BY_CURRENT_CLAIM__MAY_AFFECT_EDITORIAL_PRIORITY
TRIAGE_STATE = SCIENTIFICALLY_MATURE_FOR_ARXIV__JMLR_SUBMISSION_AFTER_HUMAN_AND_FORMAT_GATES
```
