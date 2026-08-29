# Hostile Editor Review V3 — Citation-Bound Submission Surface

**Issue:** #51  
**Reviewed surface:** `MANUSCRIPT_DRAFT_V8_CITED.md` plus proof/protocol/reviewer tables and frozen receipts.  
**Role:** simulated internal top-tier editorial review; **not independent peer review and grants no submission authority**.

## Executive verdict

```text
TECHNICAL_CORRECTNESS = STRONG_WITHIN_REGISTERED_FINITE_SCOPE
PARENT_ACKNOWLEDGMENT = STRONG
CLAIM_CALIBRATION = STRONG
PRACTICAL_ASSESSMENT_DESIGN = STRONG
GENERIC_MATHEMATICAL_NOVELTY = LOW_BY_DESIGN
ASSESSMENT_FRAMEWORK_DISTINCTNESS = PLAUSIBLE_BUT_DEBATABLE
JMLR_EDITORIAL_SCALE = BORDERLINE_HIGH_RISK
TMLR_AUDIENCE_INTEREST = PLAUSIBLE_STRONG_IF_POLICY_FIT
REAL_LLM_EMPIRICAL_SUPPORT = ABSENT_BY_DESIGN
```

The paper is substantially stronger as an **assessment-framework paper** than as a theorem paper. Any editorial presentation that foregrounds `C_stat^*`, `C_dyn^*`, or state minimization as the central novelty will make the paper easier to reject because the strongest parents already own that substrate.

The defensible center is:

> **A representation can be matched on the declared linguistic target and the present decision yet remain uncertified for later evidence-triggered revision; the paper formalizes this no-certification gap and supplies a protocol that tests it only after current-equivalence, acquisition, and alternate-channel controls pass.**

---

# Reviewer A — information theory / state abstraction

## Objection

“The mathematical ingredients are causal states, decision sufficiency, right congruence, conditional entropy, and a two-history fibre counterexample. Why is this a new JMLR paper?”

## Best response already available

Do **not** argue that the state mathematics is new. The manuscript already concedes causal states, Brodu, R-PSR, AIS, POMDP state, ISFSM minimization, stable quotients, IB/DIB, VE/PVE/VES, and Blackwell.

The response is instead:

1. the theorem is a **no-certification result for a particular evaluation protocol**;
2. the state machinery is used to define matched present adequacy and future revision adequacy on one common scale;
3. the scientific object is the assessment sequence, not the quotient/minimizer;
4. the direct LLM neighbors do not make present-equivalence + retention intervention + common later evidence their primary certification object.

## Remaining vulnerability

A reviewer may still view the no-certification theorem as an immediate fibre corollary with an application-specific story.

### Disposition

`NON_FATAL_TO_SCIENCE__POTENTIALLY_FATAL_TO_JMLR_SIGNIFICANCE`

The manuscript must never imply that mathematical cleverness alone carries the JMLR case.

---

# Reviewer B — LLM memory / agents

## Objection

“Belief-R already tests update versus maintain. MEMENTO and multiple 2026 papers study state/memory compression and downstream loss. Why not just run those benchmarks?”

## Best response already available

The paper needs a one-paragraph contrast, not a broad claim of novelty:

- Belief-R changes evidence and scores output revision, but does not condition the comparison on a registered representation-retention intervention after matching present language/current-decision behavior.
- MEMENTO is a memory/compression method and, importantly, demonstrates why visible deletion is not evidence of actual information removal.
- relay compression studies show generic downstream degradation, but do not require the compressed and retained states to be present-equivalent before a common later evidence event.
- Router-Mem asks whether memory is sufficient now; the P2 case is sufficient now and fails only after later evidence.
- selected/omitted-evidence studies change observed input; the P2 attribution instead holds initial evidence fixed and changes retained state.

## Remaining vulnerability

No deployed/open-weight LLM is actually tested. A practical reviewer may ask whether the distinction survives real implementation channels.

### Disposition

`THEORY_PAPER_ACCEPTABLE_WITHOUT_LLM_RUN__JMLR_EDITOR_MAY_REQUEST_EMPIRICAL_BRIDGE`

Do not add an empirical claim unless Protocol V2 is executed prospectively. If a reviewer requires an experiment, the honest route is revise-and-resubmit or TMLR/flagship contraction, not simulation.

---

# Reviewer C — methodology / causal representation

## Objection

“How do you know a removed source/provenance bit was actually removed from the model rather than re-encoded in KV cache or another memory channel?”

## Current answer

Protocol V2's alternate-channel retention gate is a major strength. The manuscript explicitly uses MEMENTO as the reason visible deletion cannot establish state removal.

Strong attribution requires either:

- a registered removal test across relevant available channels; or
- an explicitly bounded `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION` terminal.

### Disposition

`ANSWERED__KEEP_IN_MAIN_BODY`

This control is differentiating and should not be shortened away.

---

# Reviewer D — formal epistemology / terminology

## Objection

“Why call an arbitrary loss-defined decision an epistemic responsibility? Isn't this generic decision theory?”

## Current answer

The underlying decision mathematics **is** generic. The manuscript should keep the operational restriction:

- the target concerns status/management of a claim, model, evidence relation, scope, support, identifiability, or revision obligation;
- the admissible action has an epistemic interpretation such as retain/reopen/abstain/retrieve evidence;
- institutional authority remains external.

The paper should say explicitly that an arbitrary auxiliary classification task does not become epistemic because it is inserted as `Q`.

### Disposition

`ANSWERED_BUT_TERMINOLOGY_DISCIPLINE_REQUIRED`

---

# Reviewer E — JMLR editor

## Likely strengths

- unusually candid strongest-parent subtraction;
- mechanized/exhaustive finite support with exact negative controls;
- clear theorem-to-protocol bridge;
- reproducible deterministic evidence;
- practical audit prescription;
- bounded/no-empirical-overclaim posture;
- direct engagement with current 2026 LLM memory work.

## Likely weaknesses

- headline theorem is intentionally simple after parent subtraction;
- analytical quantities are built from mature mathematics;
- no real-model demonstration of P2;
- “prospective revision adequacy” may be viewed as an evaluation recipe rather than a substantial new theoretical framework;
- paper can look over-engineered if all ORION-style terminology/receipts appear in the main body.

## Editorial recommendation

For a JMLR attempt, the paper should be **shorter and more assessment-centered** than the full research record:

1. abstract <=200 words (157-word frontmatter already prepared);
2. introduction leads with no-certification problem, not Machine Epistemics branding;
3. one compact parent-ownership table;
4. one theorem/witness figure/table;
5. Prospective Revision Audit protocol in main text;
6. alternate-channel causal gate in main text;
7. direct-neighbor table in main text;
8. detailed state-minimization proofs/receipts in appendix/supplement;
9. main+appendix target <=35 JMLR pages;
10. avoid more notation than required to explain the audit.

### Simulated internal verdict

`JMLR = BORDERLINE_SUBMIT_IF_EXTERNAL_EDITORIAL_READER_FINDS_ASSESSMENT_DISTINCT`

This is **not** `JMLR_SUBMISSION_AUTHORIZED`; the decisive distinctness judgment must be external to the research-generation process.

---

# TMLR editor lens

Under current TMLR acceptance criteria, the paper has a stronger fit if:

- all claims remain tightly supported;
- the audience-interest case is framed around a concrete evaluation blind spot;
- no significance/SOTA claim is needed;
- the human intellectual-ownership/AI-use policy gate is truthfully satisfied.

Technical interest proposition:

> Researchers comparing context compression, agent memory, retrieval summaries, hidden-state interventions, or persistent belief state may learn that matching current task performance is insufficient to certify behavior under later evidence, and receive a concrete protocol to test that gap.

### Simulated internal verdict

`TMLR = STRONGER_EDITORIAL_FIT__POLICY_FIT_UNRESOLVED`

---

# Required editorial changes before either venue

These are presentation changes only; none reopens scientific identity.

- [x] materialize citation database;
- [x] bind parent concessions to citation keys;
- [x] produce reviewer tables;
- [x] produce citation-bound manuscript;
- [x] prepare <=200-word abstract and running title;
- [x] prepare AI-use/authorship policy gate;
- [ ] mechanically convert to chosen venue style;
- [ ] generate receipt-derived figures/tables;
- [ ] perform final copy edit after figures are fixed;
- [ ] obtain human intellectual-ownership signoff;
- [ ] obtain genuinely external editorial/distinctness assessment.

## Current internal terminal

```text
SCIENCE = RETAIN
THEORY_PAPER = RETAIN_AS_ASSESSMENT_FRAMEWORK
JMLR = CONDITIONAL_BORDERLINE
TMLR = STRONG_FALLBACK_IF_POLICY_FIT
NO_EMPIRICAL_LLM_CLAIM = RETAIN
NO_NEW_STATE_THEORY_CLAIM = RETAIN
```
