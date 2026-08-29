# Submission Readiness Contract V1

**Issue:** #51  
**Checked:** 2026-08-29 against current official JMLR and TMLR pages.  
**Purpose:** separate scientific readiness from filing/formatting readiness and prevent venue-driven claim inflation.

## 1. Venue-neutral scientific gate

No venue submission is authorized unless:

- [x] the generic state-theory novelty route has been contracted to strongest parents;
- [x] the no-certification theorem has a human-readable proof and mechanical witness;
- [x] direct LLM revision/memory neighbors are explicitly engaged;
- [x] Prospective Revision Audit Protocol V2 is frozen;
- [x] alternate-channel retention is a mandatory causal-attribution gate;
- [x] claim ceilings and negative/CANNOT_CHECK terminals are frozen;
- [x] citation database and citation-coverage contract are materialized;
- [x] citation-bound manuscript and reviewer-facing tables exist;
- [x] venue-specific abstract/running-title/keywords are frozen;
- [x] AI-use/authorship/reproducibility gate is documented;
- [ ] final receipt-derived figures/displays and LaTeX conversion complete;
- [ ] final bibliography/status refresh completes immediately before filing;
- [ ] human intellectual-ownership review completes;
- [ ] an external editorial judgment chooses the venue route without changing the science.

The venue choice may change presentation, anonymity and page allocation. It may not change the theorem or parent concessions.

---

# 2. JMLR route

Official current sources:

- Author information: `https://jmlr.org/author-info.html`
- Reviewer guide: `https://jmlr.org/reviewer-guide.html`
- Formatting: `https://jmlr.org/format/format.html`

## 2.1 Scope fit

Current JMLR scope explicitly includes:

- theoretical studies yielding new insight into the design/behavior of learning in intelligent systems;
- formalization of new learning tasks and methods for assessing those tasks;
- development of analytical frameworks that advance theoretical studies of practical learning methods.

**#51 route:** only the **formal assessment task / analytical framework** route is eligible. The new-core-state-theory route is abandoned.

## 2.2 Reviewer-facing requirements relevant to this paper

The current JMLR reviewer guide asks whether:

- theoretical results discuss practical utility;
- evaluation is theoretically and/or empirically adequate for all claims;
- the contribution is significant and sufficiently different from prior work;
- predecessor contributions are clearly acknowledged;
- the work is understandable to an ML reader without special subject knowledge;
- examples and sufficient detail permit replication.

Current #51 status:

```text
PRACTICAL_UTILITY = PASS_PROTOCOL_V2
THEORETICAL_SUPPORT = PASS_CORE
PARENT_ACKNOWLEDGMENT = PASS_SUBSTANTIVE
ML_READABILITY = PASS_CITATION_BOUND_DRAFT
EXAMPLES = PASS_ONE_BIT_WITNESS_AND_CONTROLS
SIGNIFICANCE_DISTINCTNESS = OPEN_EXTERNAL_EDITORIAL_RISK
```

## 2.3 JMLR filing requirements

Current official requirements include:

- submission PDF typeset with the JMLR LaTeX style file; non-JMLR-style submissions may be rejected without review;
- submission file under 5 MB;
- title page with corresponding-author name/address/e-mail;
- running title <= 50 characters;
- exactly five keywords;
- abstract <= 200 words;
- cover letter;
- cover letter disclosure of significantly overlapping publications;
- confirmation all co-authors know/consent to JMLR review;
- conflict-of-interest declaration, including recently collaborating action editors;
- suggestions of 3–5 JMLR Action Editors with no author COI;
- suggestions of 3–5 reviewers with no author COI;
- keyword list in the cover letter;
- papers over 35 pages (appendix included) may be slower/harder to place with reviewers;
- papers over 50 pages require a cover-letter justification and may be desk rejected.

### Frozen JMLR packaging target

```text
MAIN_PLUS_APPENDIX_TARGET <= 35 pages
HARD_AVOID > 50 pages
RUNNING_TITLE = Prospective Revision Audit
RUNNING_TITLE_CHARACTERS = 26
KEYWORDS = 5
ABSTRACT_WORDS = 157
PDF_SIZE_TARGET < 5 MB
```

The 157-word abstract is frozen in `SUBMISSION_FRONTMATTER_V1.md`.

## 2.4 JMLR information that cannot be responsibly invented

Before filing, the human author group must supply/confirm:

- exact author list and ordering;
- corresponding-author postal/e-mail details;
- overlapping publications by the same authors, if any;
- co-author consent;
- author COIs;
- 3–5 non-conflicted Action Editors;
- 3–5 non-conflicted reviewers.

These fields depend on personal collaboration histories and authorship decisions. A future AI must not guess them from citations, GitHub, affiliations or model memory.

## 2.5 JMLR AI-use posture

A search of the current official JMLR author/reviewer pages on 2026-08-29 did not surface a dedicated LLM-use policy analogous to TMLR's. This is not a license to conceal AI assistance.

Use the truthful broad disclosure in `AI_USE_AUTHORSHIP_AND_REPRODUCIBILITY_V1.md` unless refreshed JMLR guidance specifies another placement.

Refresh the policy immediately before filing.

## 2.6 JMLR go/no-go

JMLR submission remains blocked until an independent editorial-style judgment answers YES to:

> Is the matched-current prospective-revision assessment framework sufficiently different from the strongest parent product to constitute a significant JMLR-scale advance in understanding/evaluation?

If `YES`: prepare JMLR package without changing claim scope.

If `NO` or `BORDERLINE_WEAK`: route to TMLR only if its AI/authorship policy gate passes, otherwise flagship merge/another compatible venue.

---

# 3. TMLR route

Official current sources:

- Author guide: `https://jmlr.org/tmlr/author-guide.html`
- Submission instructions: `https://jmlr.org/tmlr/submissions.html`
- Acceptance criteria: `https://jmlr.org/tmlr/acceptance-criteria.html`
- Editorial policies: `https://jmlr.org/tmlr/editorial-policies.html`
- FAQ: `https://jmlr.org/tmlr/faq.html`
- Ethics: `https://jmlr.org/tmlr/ethics.html`

## 3.1 TMLR scientific fit

TMLR's acceptance criteria prioritize:

1. whether claims are supported by accurate, convincing and clear evidence;
2. whether some part of the TMLR audience would be interested in the findings.

The criteria explicitly avoid requiring a new state of the art or treating method novelty/significance as necessary conditions.

This makes TMLR an editorially strong route if the framework remains technically sound/useful but JMLR distinctness is judged insufficient.

## 3.2 TMLR AI-use / authorship gate

Current TMLR policy permits LLMs as general-purpose assistive tools, makes human authors fully responsible, and prohibits LLM authorship. Current FAQ requires authors to disclose LLM use explicitly in a first-page footnote and states an expectation that ideas, claims and results are human-sourced.

The #51 workflow involved substantial AI assistance in literature discovery, theorem/formalization development, adversarial critique, software generation and drafting.

Therefore TMLR is **not** an automatic fallback.

```text
IF HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW != COMPLETE:
    TMLR_SUBMISSION_AUTHORIZED = NO

IF final human authors cannot truthfully reconcile the actual workflow with TMLR's current human-sourced expectation:
    TMLR_ROUTE = CLOSED_FOR_POLICY_FIT
```

The exact disclosure and ownership checklist are frozen in `AI_USE_AUTHORSHIP_AND_REPRODUCIBILITY_V1.md`.

No wording may be used to portray extensive scientific AI assistance as grammar-only support.

## 3.3 TMLR filing requirements relevant here

Current requirements include:

- double-blind review;
- anonymized submission;
- complete/active OpenReview profiles for all authors;
- author information, conflicts, funding and related metadata supplied through OpenReview but hidden from reviewers during review;
- mandatory unmodified TMLR LaTeX style/template for standard PDF submissions;
- appendix may be included after references, but reviewers are not obligated to read it;
- supplementary material up to 100 MB, in PDF or ZIP, anonymized;
- reproducibility-supporting code/data in supplement is encouraged where possible;
- manuscript main bodies over 12 pages may take longer to review;
- exact author set must be registered at submission and cannot normally be changed during review.

### Frozen TMLR packaging target

Because reviewers need not read appendices/supplements, every load-bearing statement should remain in the main body:

- theorem statement and one-bit construction;
- strongest parent contraction;
- prospective-revision audit definition;
- alternate-channel gate;
- direct-neighbor comparison;
- claim ceilings.

Proof details and mechanical receipts may be moved to appendix/supplement, but the paper must remain understandable if those are not opened.

## 3.4 Anonymization obligations

A TMLR package must not expose author identity through:

- names/affiliations in manuscript;
- repository-owner names in visible links;
- local host/user names in receipts;
- acknowledgments that identify the authors;
- non-anonymized supplemental file metadata where avoidable.

The public ORION-V2 repository may remain public, but the submission itself must not link to a version that reveals author identity in a way that breaks TMLR double blind.

---

# 4. Deterministic venue route

```text
IF external_distinctness >= JMLR_BORDERLINE_SUBMIT
AND all JMLR filing gates pass:
    ROUTE = JMLR
ELSE IF claims_sound
AND audience_interest_plausible
AND TMLR_POLICY_FIT == PASS:
    ROUTE = TMLR
ELSE IF audit_useful_but_not_standalone_scale:
    ROUTE = MERGE_INTO_MACHINE_EPISTEMICS_FLAGSHIP
ELSE:
    ROUTE = FIND_POLICY_COMPATIBLE_FIELD_VENUE_OR_DROP
```

No branch in this decision tree changes the underlying theory result.

---

# 5. Remaining packaging tasks

Mechanical/editorial only:

- [ ] convert `MANUSCRIPT_DRAFT_V8_CITED.md` to the chosen LaTeX template using `SUBMISSION_FRONTMATTER_V1.md`;
- [ ] use/merge the two frozen bibliography files;
- [ ] insert receipt-derived reviewer tables/figures;
- [ ] run citation-key completeness and bibliography-status checks;
- [ ] run page count and PDF-size checks;
- [ ] run TMLR anonymization scan if TMLR route;
- [ ] run JMLR title-page/cover-letter field check if JMLR route;
- [ ] update preprint/public-review metadata immediately before submission;
- [ ] archive exact submission bytes and source commit.

Current scientific terminal remains:

`THEORY_PAPER_RESIDUAL_SUPPORTED_AS_PROSPECTIVE_REVISION_ASSESSMENT__SUBMISSION_NOT_YET_AUTHORIZED`.
