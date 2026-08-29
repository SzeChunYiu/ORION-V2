# JMLR Mechanical-Only Handoff V1

**Issue:** #51  
**Rule:** this file is the successor-AI execution contract. Scientific redesign is prohibited unless a checker, new source or external reviewer creates a registered successor issue.

## 1. Scientific inputs are frozen

Use:

- `MANUSCRIPT_DRAFT_V9_CURRENT.md` for manuscript body;
- final title/abstract/keywords from `JMLR_PRIMARY_ROUTE_V1.md`;
- `CLAIM_LEDGER_V6.json`;
- `PROOF_APPENDIX_V1.md`;
- `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V3.md`;
- `PROSPECTIVE_REVISION_COMPATIBILITY_CRITERION_V1.md`;
- `REFERENCES_V1.bib` + `REFERENCES_CLASSICS_SUPPLEMENT_V1.bib`;
- `CITATION_COVERAGE_MATRIX_V1.md`;
- `FIGURE_AND_DISPLAY_SPEC_V1.md`;
- `PAGE_AND_SECTION_BUDGET_V1.md`;
- `JMLR_COVER_LETTER_SCIENCE_V2.md`.

Do not use older V1–V8 manuscripts/protocols/ledgers where superseded.

## 2. Remaining computation/checking

### M1 — one-step compatibility checker

Mechanize/exhaustively verify the registered criterion:

```text
A1={a,b}
A2={b,c}
A3={a,c}
```

Expected:

```text
all pairwise intersections nonempty
joint intersection empty
one_step_compatible = false
```

Also verify singleton canonical case:

```text
{REOPEN} intersect {RETAIN} = empty
```

No new theorem interpretation is allowed.

### M2 — citation-key integrity

- combine the two `.bib` sources;
- assert every citation key in V9 exists;
- assert every mandatory parent/direct-neighbor row in the citation-coverage matrix is cited;
- flag duplicate keys/DOIs/titles;
- refresh preprint/public-review status immediately before filing.

### M3 — figures/tables

Generate only from `FIGURE_AND_DISPLAY_SPEC_V1.md` and frozen receipts:

1. one-bit witness;
2. Protocol-V3 audit flow;
3. parent-ownership table;
4. direct-neighbor table;
5. optional compatibility inset;
6. mechanical-validation summary.

Do not invent real-LLM performance plots.

### M4 — JMLR LaTeX assembly

- official unmodified current JMLR style;
- title/abstract/keywords from `JMLR_PRIMARY_ROUTE_V1.md`;
- page target 27–33 including appendix;
- first move parent-owned proof detail/receipt detail to appendix if >35 pages;
- never cut claim ceilings, alternate-channel control, channel scope, direct-neighbor comparison or empirical nonclaim to save pages.

### M5 — compile/package checks

- PDF <5 MB;
- abstract <=200 words;
- running title <=50 characters;
- exactly 5 keywords;
- page count recorded;
- bibliography clean;
- all figures legible/grayscale-safe;
- no missing references/cross-references;
- source and final PDF hashes recorded.

## 3. Human/external fields the executor must not fill

- author names/order;
- corresponding-author address/e-mail;
- COI declarations;
- overlapping-publication disclosure;
- co-author consent;
- final AE/reviewer suggestions before COI screening;
- human scientific-adoption decision;
- external editor/peer-review verdict.

## 4. Forbidden executor behavior

- invent a new theorem after a checker failure;
- reclassify parent-owned mathematics as paper novelty;
- add real-LLM claims without an executed registered study;
- delete negative controls to shorten the paper;
- alter the prediction channel/intervention boundary;
- treat no pairwise collision as sufficiency under ties;
- hide or minimize AI assistance;
- select favorable reviewers based on expected verdict;
- change the primary endpoint after seeing a result.

## 5. Completion receipt

The executor should emit:

```text
COMPATIBILITY_CHECK = PASS/FAIL
CITATION_INTEGRITY = PASS/FAIL
FIGURES = PASS/FAIL
JMLR_LATEX_BUILD = PASS/FAIL
PAGE_COUNT = n
PDF_SIZE_MB = x
ABSTRACT_WORDS = n
KEYWORD_COUNT = 5/other
RUNNING_TITLE_CHARS = n
SOURCE_COMMIT = sha
PDF_SHA256 = ...

MECHANICAL_JMLR_PACKAGE = READY / NOT_READY
```

No `SUBMISSION_AUTHORIZED` field may be set by the executor.

## 6. Current terminal

```text
NONCOMPUTE_SCIENCE = COMPLETE
JMLR_PRIMARY_ROUTE = FROZEN
MECHANICAL_PACKAGE = OPEN
HUMAN_AUTHORSHIP_COI = OPEN
EXTERNAL_DISTINCTNESS = OPEN
SUBMISSION_AUTHORIZED = NO
```
