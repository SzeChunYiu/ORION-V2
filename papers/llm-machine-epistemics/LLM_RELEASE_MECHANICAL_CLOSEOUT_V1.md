# Prospective Revision Adequacy — Mechanical Release Closeout V1

**Scientific source:** `MANUSCRIPT_V12_ARXIV_JMLR_FINAL.md`  
**Scope:** release engineering only. No new theorem, empirical LLM claim, endpoint, novelty claim or scientific reinterpretation is authorized.

## Closed by this branch

The release job must:

1. execute the exact three-history compatibility fixture `{a,b}/{b,c}/{a,c}`;
2. verify nonempty pairwise intersections, empty joint intersection and exact one-step incompatibility;
3. validate every V12 citation key against the two frozen bibliography sources with duplicate-key failure;
4. reject manuscript-facing issue/PR/branch/CI/repository-path narrative;
5. generate the mandatory no-certification witness display and Prospective Revision Audit flow mechanically from the frozen display specification;
6. retain the mixed-P2 `CANNOT_CHECK` state in the mechanical-validation table;
7. assemble an arXiv LaTeX/PDF candidate from V12;
8. assemble a JMLR-format LaTeX/PDF candidate using the current official `jmlr2e.sty` fetched from the JMLR-maintained repository;
9. record exact source/bibliography/display/PDF hashes, PDF sizes and page counts;
10. upload the candidate packages as a CI artifact.

## Human-only fields deliberately unresolved

- final author list/order and affiliations;
- final human scientific-adoption approval;
- arXiv category/cross-list and license;
- acknowledgments/funding choices;
- journal COI/reviewer/AE decisions;
- actual submission authorization.

## Failure boundary

If the exact checker contradicts the theorem, a citation key is absent/ambiguous, a PDF does not compile, or a generated surface changes the scientific claim, the release remains blocked. The mechanical layer must report rather than repair the science.

## Intended terminal

```text
LLM_PRA_SCIENCE = FROZEN_READY
LLM_PRA_THREE_HISTORY_CONTROL = PENDING_CI
LLM_PRA_ARXIV_PACKAGE = PENDING_CI
LLM_PRA_JMLR_PACKAGE = PENDING_CI
NEW_SCIENTIFIC_COMPUTE_REQUIRED = FALSE
HUMAN_RELEASE_AUTHORITY = OPEN
```
