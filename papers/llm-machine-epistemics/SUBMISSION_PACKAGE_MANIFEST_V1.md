# Submission Package Manifest V1

**Issue:** #51  
**Purpose:** define one authoritative source package for mechanical JMLR/TMLR conversion.  
**Scientific content may contract after external review; formatting tools may not invent or strengthen claims.**

## 1. Authoritative scientific sources

Use these, not older development drafts:

```text
papers/llm-machine-epistemics/
  MANUSCRIPT_DRAFT_V8_CITED.md
  SUBMISSION_FRONTMATTER_V1.md
  CLAIM_LEDGER_V5.json
  PROOF_APPENDIX_V1.md
  REVIEWER_TABLES_V1.md
  CITATION_COVERAGE_MATRIX_V1.md
  REFERENCES_V1.bib
  REFERENCES_CLASSICS_SUPPLEMENT_V1.bib
  AI_USE_AUTHORSHIP_AND_REPRODUCIBILITY_V1.md
  SUBMISSION_READINESS_CONTRACT_V1.md
  JMLR_COVER_LETTER_DRAFT_V1.md
  TMLR_ANONYMIZED_PACKAGE_PLAN_V1.md

research/llm-machine-epistemics/
  PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V2.md
  PROSPECTIVE_REVISION_COLLISION_DIAGNOSTIC_V1.md
  NEAREST_WORK_PASS_04_FINAL_RECONSTRUCTION.md
  NEAREST_WORK_PASS_05_LLM_MEMORY_AND_REVISION.md
  PARENT_THEOREM_CLAIM_MATRIX_V2.md
  NONCOMPUTE_CLOSEOUT_V1.md
  mechanical_execution/
```

## 2. Submission manuscript assembly

The mechanical converter must:

1. take body text from `MANUSCRIPT_DRAFT_V8_CITED.md`;
2. replace its research-draft abstract with the 157-word submission abstract from `SUBMISSION_FRONTMATTER_V1.md`;
3. use the full title and five frozen keywords from that frontmatter file;
4. use running title `Prospective Revision Audit` for JMLR;
5. preserve every citation/parent concession required by `CITATION_COVERAGE_MATRIX_V1.md`;
6. insert selected tables from `REVIEWER_TABLES_V1.md` based only on scientific usefulness/page budget;
7. incorporate the reproducibility and bounded ethics text from `AI_USE_AUTHORSHIP_AND_REPRODUCIBILITY_V1.md`;
8. keep the no-certification theorem and one-bit witness in the main body;
9. keep empirical nonclaims and alternate-channel limitation in the main body;
10. keep proof appendix/source available even if detailed proof moves outside main text.

## 3. Main-paper required elements

Regardless of venue, main paper must include:

- research question and three audit axes;
- strongest-parent contraction;
- responsibility contract definition;
- `C_stat^*` and `C_dyn^*` as audit coordinates, with parent ownership explicit;
- `Omega_dyn` as a derived metric, not a new universal information law;
- one-bit witness;
- no-certification theorem;
- P0/P1/P2 taxonomy;
- collision-certificate definition;
- Prospective Revision Audit procedure;
- alternate-channel retention gate;
- Belief-R/MEMENTO/direct-neighbor comparison;
- limitations and claim ceilings;
- reproducibility statement;
- AI-assistance disclosure in venue-appropriate placement;
- bounded ethical/societal-impact paragraph where required/applicable.

## 4. Appendix candidates

May move to appendix subject to venue/page budget:

- full static selector/partition proof;
- full dynamic selector/refinement proof;
- horizon proof details;
- bounded-responsibility proof;
- mutation assumption matrix;
- extended direct-neighbor table;
- complete claim/receipt table;
- extra finite fixtures.

The one-bit construction and proof intuition may not be appendix-only.

## 5. Supplement/repository evidence

Mechanical support package should contain:

- exact finite partition enumerator;
- responsibility selector audit;
- deficit audit;
- dynamic phase audit;
- universality audit;
- log-loss parent benchmark;
- mutation audit;
- theorem-location validator;
- claim/receipt crosscheck;
- frozen JSON receipts;
- README with deterministic rerun commands.

No generated table may report a result that is absent from its receipt.

## 6. JMLR package

Target:

```text
jmlr_submission/
  manuscript.tex
  jmlr2e.sty (official, unmodified)
  references.bib
  figures/
  cover_letter.txt or .pdf
  [online appendix/supplement if used]
```

Rules from current official guidance are frozen in `SUBMISSION_READINESS_CONTRACT_V1.md`.

Human-only unresolved inputs:

- authors/order;
- corresponding-author contact;
- overlap disclosure;
- coauthor consent;
- COIs;
- 3–5 AEs;
- 3–5 reviewers.

## 7. TMLR package

Only if TMLR policy-fit gate passes:

```text
tmlr_submission/
  anonymous_manuscript.tex
  official TMLR style/template, unmodified
  references.bib
  figures/
  anonymous_supplement.zip  # optional, <= current venue cap
  anonymization_receipt.json
```

Human-only unresolved inputs remain in OpenReview rather than the anonymous PDF.

The first page must carry the truthful AI-assistance disclosure required by current TMLR guidance.

## 8. Source-status refresh immediately before filing

Must refresh status of:

- all 2026 arXiv preprints;
- MEMENTO proceedings status;
- AgenticSTS review/publication status;
- the public double-blind RLC/RLJ manuscript;
- any working-paper status;
- JMLR/TMLR author/ethics/LLM-use policies;
- venue LaTeX templates/style files.

Metadata refresh may change bibliographic status but not scientific ownership unless a new version contains a materially stronger theorem.

## 9. Publication-byte binding after assembly

After target PDF/source exist, freeze:

- source commit SHA;
- manuscript source hashes;
- bibliography hashes;
- figure hashes;
- supplement hashes;
- final PDF hash;
- citation-coverage check result;
- page count;
- file size;
- venue policy check date.

A later source edit invalidates the package binding and requires regeneration.

## 10. Current package state

```text
SCIENTIFIC_SOURCE = READY
CITED_MANUSCRIPT = READY
BIBLIOGRAPHY = READY_WITH_PRE_SUBMISSION_REFRESH_CLASS
REVIEWER_TABLES = READY
PROOF_APPENDIX = READY
AUDIT_PROTOCOL = READY
REPRODUCIBILITY_DISCLOSURE = READY
JMLR_COVER_LETTER = READY_EXCEPT_HUMAN_FIELDS
TMLR_ANONYMIZATION_PLAN = READY_BUT_POLICY_GATED
TARGET_LATEX = NOT_YET_GENERATED
FINAL_PDF = NOT_YET_GENERATED
EXTERNAL_EDITORIAL_JUDGMENT = OPEN
```
