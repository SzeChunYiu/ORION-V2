# JMLR Primary Route V1 — Prospective Revision Adequacy

**Issue:** #51  
**Primary venue:** Journal of Machine Learning Research (JMLR)  
**Status:** final non-computational venue decision; submission remains blocked on mechanical assembly, human authorship/COI and external editorial judgment.

## 1. Final submission identity

### Full title

> **Prospective Revision Adequacy: Auditing Autoregressive Representations Beyond Current Prediction and Decision**

### Running title

> **Prospective Revision Adequacy**

### Five keywords

1. representation learning
2. language models
3. sequential decision making
4. memory compression
5. belief revision

### Submission abstract

Autoregressive representations are commonly evaluated by current predictive performance, yet long-lived systems must also revise decisions after later evidence. We formalize **prospective revision adequacy** relative to a registered prediction protocol and responsibility. A finite construction shows that two representations can be equally adequate for the current linguistic target and the same unique current decision while only one retains a one-bit distinction needed for correct revision after a common later intervention. Thus present prediction and decision adequacy do not, in general, certify future revision adequacy. Building on predictive-state, decision-sufficiency, information-state and memory-compression theory, we define a Prospective Revision Audit that matches current behavior, intervenes on retained historical state, rules out alternate-channel and parametric reconstruction, presents identical later evidence, and scores both updating and maintaining/selective reopening. The contribution is an assessment framework and non-certification result, not a new generic state-minimization theory or an empirical claim that current language models necessarily discard revision-relevant information.

## 2. Why JMLR is the primary route

Current JMLR scope explicitly includes:

- theoretical studies yielding new insight into learning-system design/behavior;
- formalization of new learning tasks and methods for assessing them;
- analytical frameworks for practical learning methods.

The paper is therefore submitted, if at all, through the **new assessment task / analytical framework** route.

It is **not** submitted as:

- a new generic theorem of state minimality;
- a new information-bottleneck/rate-distortion result;
- a new belief-revision benchmark in general;
- empirical evidence that real LLMs fail prospective revision.

## 3. Editorial thesis

The one-sentence thesis for an editor is:

> **A representation can be fully adequate for the registered current prediction target and current decision yet be inadequate for evidence-triggered revision; therefore prospective revision is an independent assessment axis that current prediction/decision evaluation cannot certify.**

The mathematical witness exists to justify the need for the assessment axis. The main contribution is the audit object and its causal controls.

## 4. Four contribution claims allowed in title/abstract/introduction

1. **No-certification:** current prediction + current decision do not generally certify later revision under a distinct registered evidence intervention.
2. **One-bit witness:** in the canonical finite process, `C_stat^*=0`, `C_dyn^*=1 bit`, `Omega_dyn=1 bit`, with a unique current action.
3. **Three-axis audit:** predictive adequacy, current responsibility adequacy and prospective revision adequacy are reported separately.
4. **Prospective Revision Audit V3:** present-equivalence, state intervention, alternate-channel/parametric-reconstruction control, common later evidence, complete future-action compatibility, and update+maintain/selective-reopening scoring.

## 5. Claims explicitly excluded

- no universal first-work claim;
- no “Machine Epistemics” field claim in the JMLR paper;
- no claim that predictive compression usually loses epistemic information;
- no claim that `Omega_dyn` is a new universal information law;
- no claim that deployed LLMs exhibit P2 failure;
- no claim that one hidden dimension/neuron corresponds to one epistemic variable;
- no claim that authority can be generated from a neural representation;
- no claim that pairwise collisions are a complete sufficiency test under tied actions.

## 6. Why the paper can stand without training a model

The central contribution is logical/analytical:

1. demonstrate a class in which two present-equivalent representations have different prospective revision capability;
2. prove the failure is not detectable from present prediction/current decision alone;
3. specify an assessment protocol that would expose the missing capability in any system where suitable representation interventions are available.

An empirical LLM run would strengthen practical relevance but is not logically necessary for the assessment task to exist.

### If an editor insists on a real-model bridge

The response is contraction, not theorem inflation:

- keep the theory correct;
- execute frozen Protocol V3 on an open/frozen model or explicit agent-memory system;
- add no new success criterion after seeing the result.

## 7. JMLR-specific package target

```text
manuscript source = MANUSCRIPT_DRAFT_V9_CURRENT.md
frontmatter = this file / SUBMISSION_FRONTMATTER_V2.md
claim ledger = CLAIM_LEDGER_V6.json
proof appendix = PROOF_APPENDIX_V1.md
protocol = PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V3.md
bibliography = REFERENCES_V1.bib + REFERENCES_CLASSICS_SUPPLEMENT_V1.bib
displays = FIGURE_AND_DISPLAY_SPEC_V1.md
page target = 27–33 JMLR pages including appendix
hard review-risk threshold = >35 pages
hard avoid = >50 pages
```

## 8. Venue fallback order

1. **JMLR**, if external distinctness/significance review returns at least `JMLR_BORDERLINE_SUBMIT`.
2. **TMLR**, only if the human intellectual-ownership/LLM-policy gate can be satisfied truthfully under the then-current FAQ/editorial policy.
3. **Artificial Intelligence (AIJ)** or another compatible theory/AI journal if the analytical contribution is sound but JMLR/TMLR policy/fit is poor.
4. merge into the Machine Epistemics flagship if external review says the assessment is useful but not independently paper-scale.

No fallback permits stronger claims.

## 9. Current authority

```text
JMLR_SCIENCE_ARGUMENT = COMPLETE
JMLR_SCOPE_FIT = PLAUSIBLE_AS_ASSESSMENT_FRAMEWORK
JMLR_DISTINCTNESS = EXTERNAL_JUDGMENT_OPEN
REAL_LLM_RESULT = OPTIONAL_NOT_ESTABLISHED
MECHANICAL_PACKAGE = OPEN
HUMAN_AUTHORSHIP_COI = OPEN
SUBMISSION_AUTHORIZED = NO
```
