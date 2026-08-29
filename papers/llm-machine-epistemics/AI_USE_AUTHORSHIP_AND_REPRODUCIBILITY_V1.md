# AI Use, Authorship, Reproducibility and Ethics V1

**Issue:** #51  
**Checked:** 2026-08-29 against current official venue guidance.  
**Purpose:** record the actual research-assistance workflow and prevent a submission disclosure from overstating human-only origin or understating AI involvement.

## 1. Actual workflow that must not be hidden

This research programme has used large language model systems extensively as research-assistance tools, including for:

- literature discovery and nearest-work searching;
- strongest-parent reconstruction and novelty subtraction;
- formal-definition development;
- candidate theorem and counterexample formulation;
- hostile-review reasoning;
- protocol design;
- manuscript drafting and editing;
- code generation for mechanical finite audits;
- deterministic mechanical checking through separate AI-assisted execution sessions.

The human research direction supplied the overarching Machine-Epistemics/LLM question, publication objective, constraints, acceptance boundaries, and repeated instructions to contract unsupported novelty. The repository deliberately distinguishes AI-generated candidate reasoning from mechanically checked results and external parent ownership.

No LLM or software system is an author. Human authors remain responsible for every scientific claim that is ultimately submitted.

## 2. Human intellectual-ownership gate

Before any submission, every human listed as an author who takes responsibility for the paper must independently review the final manuscript and be able to:

1. explain the governing research question without relying on generated text;
2. explain the no-certification construction and why it works;
3. explain `C_stat^*`, `C_dyn^*`, and `Omega_dyn`, including which parts are parent-owned;
4. explain the strongest direct parents and why the paper contracted away generic state-theory novelty;
5. explain the Prospective Revision Audit and its P0/P1/P2 controls;
6. explain why the alternate-channel retention gate is necessary;
7. inspect the mechanical receipts supporting all registered theorem statements;
8. inspect the nearest-work/citation matrix and agree with the parent concessions;
9. decide that each surviving claim is one they personally endorse and are willing to defend;
10. correct or remove any claim they cannot independently justify.

Completion should be recorded as:

`HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW = COMPLETE`

This is not a claim that all ideas were independently conceived without AI. It is a responsibility/adoption gate: the submitting humans must understand, verify and own the final scientific content rather than merely submit generated text.

## 3. TMLR-specific policy gate

Current TMLR editorial policy permits LLMs as general-purpose assistive tools and states that authors remain fully responsible; LLMs are not eligible for authorship. Current TMLR FAQ additionally says transparency is required and that authors should explicitly mention LLM use in a first-page footnote. The FAQ also states an expectation that the ideas, claims and results in submissions are human-sourced.

Official pages checked:

- `https://jmlr.org/tmlr/editorial-policies.html`
- `https://jmlr.org/tmlr/faq.html`

Because the #51 workflow involved substantial AI assistance in scientific ideation/formalization, **TMLR submission is not authorized merely by inserting a generic “AI assisted writing” footnote.** The human author group must first decide, in good faith, whether its actual contribution/ownership satisfies TMLR's current human-sourced expectation.

Fail-closed route:

```text
IF HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW != COMPLETE:
    TMLR_SUBMISSION_AUTHORIZED = NO

IF authors cannot truthfully reconcile the actual workflow with TMLR's human-sourced expectation:
    TMLR_ROUTE = CLOSED_FOR_POLICY_FIT
```

No wording trick may be used to obscure the actual research workflow.

## 4. Candidate TMLR first-page disclosure

Only use after the human ownership/policy gate passes:

> **AI assistance disclosure.** Large language model tools were used extensively as research assistants for literature discovery, formalization, adversarial critique, software generation, and manuscript drafting/editing. All scientific claims, proofs, citations, and reported results were independently reviewed and adopted by the human authors, who take full responsibility for the work. AI systems are not authors.

This disclosure is intentionally broader than “used for grammar.” Shorten only if the substantive scope of AI assistance remains clear.

## 5. JMLR disclosure posture

A search of the current official JMLR author/reviewer pages on 2026-08-29 did not surface a dedicated LLM-use policy analogous to TMLR's. This should **not** be interpreted as permission to hide AI assistance.

For JMLR, use a transparent disclosure in the manuscript acknowledgments/reproducibility statement or cover letter unless updated journal guidance specifies another placement.

Candidate text:

> **AI assistance disclosure.** Large language model tools were used as research assistants for literature discovery, formalization, adversarial critique, software generation, and manuscript drafting/editing. The human authors reviewed the final scientific arguments, citations, proofs, and mechanical evidence and take responsibility for the submitted work. AI systems are not authors.

Refresh JMLR policy immediately before submission.

## 6. Reproducibility statement

The paper is theory-first and makes no empirical claim about current LLM hidden states. Its computational support consists of deterministic finite audits and frozen receipts.

The submission should state:

> The core finite claims are accompanied by executable deterministic audit scripts and committed machine-readable receipts. The static partition layer exhaustively enumerates set partitions through seven states with Bell-number completeness checks. Dynamic-state, selector-equivalence, horizon, universality, information-identity and mutation audits use frozen fixtures and exact/rational decision paths with independent high-precision cross-checks where appropriate. The paper's primary no-certification construction also has a human-readable proof independent of the software. No LLM training or model benchmark result is required for the theoretical claim.

If a venue is double-blind, repository paths/links must be anonymized in the submitted surface and provided through appropriately anonymized supplementary material or later camera-ready links.

## 7. Data / human-subject / privacy statement

Current #51 core theory:

- uses no human-subject experiment;
- uses no private/sensitive personal dataset;
- makes no empirical inference about individuals or protected groups;
- uses public scholarly metadata only for literature review;
- uses synthetic/finite known-answer constructions for theorem validation.

Therefore no IRB/human-subject approval is implicated by the current core paper. If the optional real-LLM protocol is later executed using human-derived/private data, this statement must be reopened.

## 8. Societal/ethical impact statement

The work proposes an evaluation framework intended to detect when an AI system cannot revise decisions correctly after evidence changes. Potential benefit is improved auditing of long-lived AI memory and evidence-responsive behavior.

Potential risks include:

- treating an audit pass as proof of truth, safety, or general intelligence;
- using a bounded responsibility audit to claim universal epistemic adequacy;
- attributing a failure to state removal when the information remained in an unchecked channel;
- using the framework to justify automation of high-stakes decisions without appropriate domain evidence or human/institutional authority.

Mitigations built into the protocol include bounded responsibility/horizon claims, acquisition controls, maintain/selective-reopening controls, alternate-channel checks, explicit `CANNOT_CHECK` terminals, and a prohibition on converting internal state adequacy into institutional authority.

## 9. Authorship fields requiring human input

A future AI must not infer:

- who qualifies as an author;
- author ordering;
- corresponding author;
- author contributions;
- conflicts of interest;
- funding disclosures;
- whether an individual's intellectual contribution satisfies a venue's authorship/AI-use policy.

Those are human governance decisions.

## Current terminal

```text
AI_USE_TRANSPARENCY = REQUIRED
AI_AUTHORSHIP = FORBIDDEN
HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW = OPEN
TMLR_POLICY_FIT = OPEN_HIGH_IMPORTANCE
JMLR_AI_POLICY_REFRESH = REQUIRED_PRE_SUBMISSION
REPRODUCIBILITY_NARRATIVE = READY
CORE_HUMAN_SUBJECTS = NONE
```
