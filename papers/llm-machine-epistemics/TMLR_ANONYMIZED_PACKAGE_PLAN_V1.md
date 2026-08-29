# TMLR Anonymized Package Plan V1

**Issue:** #51  
**Status:** filing plan only; TMLR route remains policy-gated by `AI_USE_AUTHORSHIP_AND_REPRODUCIBILITY_V1.md`.

## 1. Policy gate before formatting

Current TMLR policy permits LLMs as assistive tools, requires authors to remain responsible, prohibits LLM authorship, and requires explicit first-page disclosure of LLM use. Current FAQ also states the venue's expectation that ideas, claims, and results are human-sourced.

Therefore:

```text
IF HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW != COMPLETE:
    DO_NOT_BUILD_TMLR_SUBMISSION

IF actual workflow cannot be truthfully reconciled with TMLR's current human-sourced expectation:
    TMLR_ROUTE = CLOSED_FOR_POLICY_FIT
```

No anonymization or wording change may conceal the actual AI-assistance workflow.

## 2. Manuscript surface

Use:

- scientific text from `MANUSCRIPT_DRAFT_V8_CITED.md` or verified successor;
- 157-word abstract from `SUBMISSION_FRONTMATTER_V1.md`;
- TMLR unmodified LaTeX style/template;
- no author names, affiliations, acknowledgments, or identifying correspondence in the review PDF.

The first-page AI-use footnote must remain visible while preserving author anonymity.

Candidate anonymized footnote, conditional on policy gate passing:

> **AI assistance disclosure.** Large language model tools were used extensively as research assistants for literature discovery, formalization, adversarial critique, software generation, and manuscript drafting/editing. The human authors reviewed and adopted the final scientific claims, proofs, citations, and reported results and take responsibility for the work. AI systems are not authors.

## 3. Double-blind hazards specific to this project

The submission/supplement must not expose identity through:

- `SzeChunYiu/ORION-V2` URLs or repository owner names;
- Git commit author fields;
- local usernames or e-mail addresses in receipts;
- hostnames such as personal machines or named cluster accounts where they identify an author;
- acknowledgments/funding text that reveals authors prematurely;
- file metadata that directly embeds author identity;
- links to issue #51 / PR #52 during anonymous review;
- generated PDF metadata containing author names.

If reproducibility files are submitted during review, create an anonymous bundle whose internal identifiers preserve scientific identity but remove personal identity.

Do not rewrite the scientific receipt values merely for anonymity. Instead create an anonymity-preserving derivative package and record a mapping kept outside the reviewer bundle.

## 4. Main-body content that cannot be relegated to appendix

Current TMLR guidance says reviewers are not obligated to read appendices/supplement. Therefore main text must contain:

1. strongest-parent contraction;
2. exact statement of the no-certification theorem;
3. one-bit witness;
4. Prospective Revision Audit definition;
5. present-equivalence gate;
6. update + maintain/selective-reopening metrics;
7. alternate-channel retention gate;
8. direct-neighbor comparison, especially Belief-R and MEMENTO;
9. claim ceilings and empirical nonclaim;
10. enough proof intuition to understand why the theorem holds.

Full derivations, exhaustive receipts and mutation matrices may move to appendix/supplement.

## 5. Supplement package if TMLR route passes

Recommended anonymized supplement:

```text
supplement/
  README.md
  proof_appendix.pdf or source
  mechanical_execution/
    common finite-audit library
    static audit
    dynamic audit
    universality audit
    mutation audit
    claim-receipt crosscheck
    frozen JSON receipts
  reviewer_tables/
  bibliography_status_receipt.md
  ANONYMIZATION_RECEIPT.json
```

Supplement must be <=100 MB under current TMLR guidance and use PDF/ZIP format.

## 6. Broader-impact paragraph

TMLR ethics guidance expects applicable ethical/societal consequences to be discussed. Suggested bounded paragraph:

> The proposed audit is intended to reveal cases where an AI system cannot revise decisions correctly after evidence changes. Its main misuse risk is overinterpreting a bounded audit pass as proof of truth, safety, or universal epistemic adequacy. The protocol therefore fixes responsibility and horizon scope, separates missing evidence from representation loss, includes maintain/selective-reopening controls, and returns `CANNOT_CHECK` when alternate information channels cannot be ruled out. Internal representation adequacy does not confer institutional authority to make high-stakes decisions.

## 7. OpenReview author metadata

The review PDF is anonymous, but OpenReview requires exact author profiles/metadata. Human authors must supply/confirm:

- final author set;
- active OpenReview profiles;
- affiliations;
- conflicts;
- funding;
- competing interests;
- human-subject fields if relevant;
- Action Editor recommendations when requested.

No AI may infer these from repository metadata.

## 8. TMLR readiness terminal

```text
SCIENTIFIC_SOUNDNESS = READY_PENDING_FINAL_EDITORIAL_PACKAGE
ANONYMIZED_PACKAGE_DESIGN = READY
AI_DISCLOSURE_TEXT = READY
HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW = OPEN
TMLR_HUMAN_SOURCED_POLICY_FIT = OPEN_DECISIVE
TMLR_SUBMISSION_AUTHORIZED = NO
```
