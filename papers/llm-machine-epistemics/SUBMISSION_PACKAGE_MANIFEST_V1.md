# Submission Package Manifest V1

**Issue:** #51  
**Purpose:** define one authoritative source package for mechanical JMLR/TMLR conversion.  
**Scientific content may contract after external review; formatting tools may not invent or strengthen claims.**

## 1. Authoritative scientific sources

Use these, not older development drafts:

```text
papers/llm-machine-epistemics/
  MANUSCRIPT_DRAFT_V9_CURRENT.md
  SUBMISSION_FRONTMATTER_V2.md
  CLAIM_LEDGER_V6.json
  PROOF_APPENDIX_V1.md
  REVIEWER_TABLES_V1.md
  FIGURE_AND_DISPLAY_SPEC_V1.md
  PAGE_AND_SECTION_BUDGET_V1.md
  CITATION_COVERAGE_MATRIX_V1.md
  REFERENCES_V1.bib
  REFERENCES_CLASSICS_SUPPLEMENT_V1.bib
  AI_USE_AUTHORSHIP_AND_REPRODUCIBILITY_V1.md
  HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW_V1.md
  EXTERNAL_EDITORIAL_REVIEW_PACKET_V1.md
  HOSTILE_EDITOR_REVIEW_V3_SUBMISSION_SURFACE.md
  SUBMISSION_READINESS_CONTRACT_V1.md
  JMLR_COVER_LETTER_DRAFT_V1.md
  TMLR_ANONYMIZED_PACKAGE_PLAN_V1.md

research/llm-machine-epistemics/
  CURRENT_RESEARCH_STATUS_V9.md
  PREDICTION_CHANNEL_AND_INTERVENTION_SCOPE_V1.md
  PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V3.md
  PROSPECTIVE_REVISION_COMPATIBILITY_CRITERION_V1.md
  PROSPECTIVE_REVISION_COLLISION_DIAGNOSTIC_V1.md
  NEAREST_WORK_PASS_04_FINAL_RECONSTRUCTION.md
  NEAREST_WORK_PASS_05_LLM_MEMORY_AND_REVISION.md
  PARENT_THEOREM_CLAIM_MATRIX_V2.md
  NONCOMPUTE_CLOSEOUT_V1.md
  mechanical_execution/
```

`MANUSCRIPT_DRAFT_V9_CURRENT.md` already integrates the prior V8 correction register. The correction register and V1–V8 manuscripts remain provenance, not assembly inputs unless an external review explicitly asks for history.

## 2. Submission manuscript assembly

The mechanical converter must:

1. take body text from `MANUSCRIPT_DRAFT_V9_CURRENT.md`;
2. use the 157-word abstract, full title, five keywords, and running title from `SUBMISSION_FRONTMATTER_V2.md`;
3. use `CLAIM_LEDGER_V6.json` for final claim-status validation;
4. preserve every citation/parent concession required by `CITATION_COVERAGE_MATRIX_V1.md`;
5. insert selected displays according to `FIGURE_AND_DISPLAY_SPEC_V1.md` and `PAGE_AND_SECTION_BUDGET_V1.md`;
6. materialize Protocol V3 semantics exactly;
7. incorporate reproducibility, bounded ethics, and truthful AI-use text from `AI_USE_AUTHORSHIP_AND_REPRODUCIBILITY_V1.md`;
8. keep the no-certification theorem and one-bit witness in the main body;
9. keep registered-channel scope, empirical nonclaims, alternate-channel limitation, parametric-reconstruction control, and complete one-step compatibility criterion in the main body;
10. keep proof appendix/source available even if detailed proof moves outside main text.

Assembly terminal required before any venue-specific PDF is called scientifically current:

`V9_ASSEMBLED__SUBMISSION_SCIENCE_CURRENT`.

## 3. Main-paper required elements

Regardless of venue, main paper must include:

- research question and three audit axes;
- prediction reference protocol/channel `rho` and distinct future evidence-intervention family;
- strongest-parent contraction;
- responsibility contract definition;
- `C_stat^*` and `C_dyn^*` as audit coordinates with parent ownership explicit;
- `Omega_dyn` as a derived metric, not a new universal information law;
- one-bit witness;
- channel-relative no-certification theorem;
- P0/P1/P2 taxonomy;
- complete one-step compatibility via joint acceptable-action intersection;
- pairwise collision only as a sufficient failure witness;
- Prospective Revision Audit V3;
- alternate-channel retention and parametric-reconstruction gates;
- prospectively frozen present-equivalence margins;
- deterministic/stochastic decoding policy rule if empirical mode is discussed;
- controlled-future stronger-state positive control;
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
- extra finite fixtures;
- log-loss calibration detail.

The one-bit construction, theorem intuition, prediction-channel scope, joint compatibility correction, and Protocol-V3 causal gates may not be appendix-only.

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
- future compatibility checker including the three-history pairwise-overlap/joint-empty control;
- README with deterministic rerun commands.

No generated table may report a result absent from its receipt. Until the new compatibility checker lands, C19 must remain `NOT_YET_SEPARATELY_MECHANIZED__ELEMENTARY_PROOF_WRITTEN` in any mechanization-status display.

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
- 3–5 reviewers;
- human intellectual-ownership review.

## 7. TMLR package

Only if TMLR policy-fit gate passes:

```text
tmlr_submission/
  anonymous_manuscript.tex
  official TMLR style/template, unmodified
  references.bib
  figures/
  anonymous_supplement.zip
  anonymization_receipt.json
```

Human-only unresolved inputs remain in OpenReview rather than the anonymous PDF.

The first page must carry the truthful AI-assistance disclosure required by current TMLR guidance, and the human intellectual-ownership/policy-fit gate must pass before filing.

## 8. Source-status refresh immediately before filing

Must refresh:

- all 2026 arXiv preprints;
- MEMENTO proceedings status;
- AgenticSTS review/publication status;
- the public double-blind RLC/RLJ manuscript;
- working-paper status;
- JMLR/TMLR author/ethics/LLM-use policies;
- venue LaTeX templates/style files.

Metadata refresh may change bibliographic status but not scientific ownership unless a new version contains a materially stronger theorem.

## 9. Publication-byte binding after assembly

After target PDF/source exist, freeze:

- source commit SHA;
- manuscript source hash;
- Protocol-V3 hash;
- Claim-Ledger-V6 hash;
- bibliography hashes;
- figure hashes;
- supplement hashes;
- final PDF hash;
- citation-coverage result;
- claim-ledger validation result;
- page count;
- file size;
- venue policy check date.

A later source edit invalidates package binding and requires regeneration.

## 10. Current package state

```text
SCIENTIFIC_SOURCE = V9_READY
CITED_MANUSCRIPT = V9_READY
BIBLIOGRAPHY = READY_WITH_PRE_SUBMISSION_REFRESH_CLASS
CLAIM_LEDGER = V6_CANONICAL
REVIEWER_TABLES = READY_PROTOCOL_V3_ALIGNED
FIGURE_SPEC = READY_PROTOCOL_V3_ALIGNED
PROOF_APPENDIX = READY
AUDIT_PROTOCOL = V3_CANONICAL
COMPATIBILITY_CRITERION = COMPLETE_IN_PROOF__SEPARATE_MECHANIZATION_OPEN
REPRODUCIBILITY_DISCLOSURE = READY
AI_USE_POLICY_GATE = READY
JMLR_COVER_LETTER = READY_EXCEPT_HUMAN_FIELDS
TMLR_ANONYMIZATION_PLAN = READY_BUT_POLICY_GATED
TARGET_LATEX = NOT_YET_GENERATED
FINAL_PDF = NOT_YET_GENERATED
EXTERNAL_EDITORIAL_JUDGMENT = OPEN
```
