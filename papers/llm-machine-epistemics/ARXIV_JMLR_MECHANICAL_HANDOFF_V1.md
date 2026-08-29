# arXiv / JMLR Mechanical Handoff V1 — Prospective Revision Adequacy

**Scientific source:** `MANUSCRIPT_V12_ARXIV_JMLR_FINAL.md`  
**Public title:** **Prospective Revision Adequacy: Auditing Autoregressive Representations Beyond Current Prediction and Decision**  
**Rule:** no new scientific reasoning is delegated to this handoff.

## A. Remaining theorem/reproducibility check

1. implement the three-history exact compatibility fixture:

```text
A1={a,b}
A2={b,c}
A3={a,c}
```

Expected:

```text
all_pairwise_intersections_nonempty = true
joint_intersection = empty
one_step_compatible = false
```

2. add a result receipt and include it in the mechanization table;
3. do not change theorem wording unless the checker contradicts the written proof.

## B. Citation assembly

1. merge `REFERENCES_V1.bib` and `REFERENCES_CLASSICS_SUPPLEMENT_V1.bib` with duplicate-key detection;
2. extract every citation key from V12;
3. fail if any key is missing;
4. fail if any duplicate/ambiguous key points to a different work;
5. refresh status of all 2026 preprints/public-review manuscripts immediately before release;
6. run the existing citation-coverage matrix and record pass/fail.

No citation may be deleted merely because it weakens novelty.

## C. Figures/tables

Generate only the displays specified in `FIGURE_AND_DISPLAY_SPEC_V1.md`:

- one-bit witness;
- Prospective Revision Audit flow;
- strongest-parent/direct-neighbor tables;
- tied-action compatibility control if page budget permits;
- receipt validation summary.

Use proof/receipt data only. No simulated LLM performance plot.

## D. arXiv package

Create:

```text
papers/llm-machine-epistemics/release/arxiv_v1/
  manuscript.tex
  references.bib
  figures/
  supplement_or_appendix/
  README_RELEASE.md
```

Requirements:

- use V12 scientific prose;
- include proof/appendix sufficient for independent theory evaluation;
- include reproducibility + AI-assistance disclosure;
- remove internal repo paths/PR/issue identifiers from manuscript surfaces;
- keep author metadata human-supplied;
- do not choose arXiv category or license automatically.

Run manuscript-surface QA and compile until clean.

## E. JMLR package

After the arXiv scientific bytes are stable, create:

```text
papers/llm-machine-epistemics/release/jmlr_v1/
  manuscript.tex
  jmlr2e.sty
  references.bib
  figures/
  cover_letter_draft.md
  release_receipt.json
```

Requirements:

- current official JMLR style;
- PDF <5 MB;
- abstract <=200 words;
- running title <=50 characters;
- exactly five keywords;
- target <=35 pages including appendix where feasible;
- no science changes from the arXiv scientific version except explicit corrections/contractions;
- human-only fields remain unresolved until provided.

## F. Final byte binding

For each release candidate record:

```text
source_commit
manuscript_hash
proof_hash
bibliography_hash
figure_hashes
supplement_hash
compiled_pdf_hash
page_count
pdf_size
citation_audit_result
atomic_claim_audit_result
surface_qa_result
policy_check_date
```

## G. Stop conditions

Stop and report rather than repair scientifically if:

- a theorem checker contradicts a load-bearing claim;
- a citation source does not entail its manuscript sentence;
- a new direct parent fully absorbs the registered assessment object;
- the final bytes contain a scientific claim absent from V12/claim ledger;
- required author/legal/COI fields are requested.

Those return to human/scientific governance; the mechanical agent must not improvise.

## Current terminal

`NEXT_AI_JOB = MECHANICAL_VERIFICATION + ARXIV/JMLR ASSEMBLY ONLY`.
