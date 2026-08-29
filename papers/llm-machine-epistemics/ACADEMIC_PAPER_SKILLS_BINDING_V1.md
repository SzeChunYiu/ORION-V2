# Academic Paper Skills Binding V1 — LLM Prospective Revision Audit

**Issue:** #51  
**Bound repository:** `SzeChunYiu/academic-paper-skills`  
**Bound commit:** `d2cac7bd0d3152369acee5c3859059dc87fcd24d`  
**Pipeline:** `academic-paper-pipeline` v1.6.0  
**Writing router:** `academic-writing`

This binding supersedes any older manuscript-development method for the #51 paper. It changes paper-development governance, not scientific results.

## Required pipeline state

The manuscript is developed through the following immutable order:

`target/archetype -> evidence freeze -> protocol/conduct -> data lifecycle -> inference/uncertainty -> atomic claims -> figure/display contracts -> prose logic -> surface QA -> editor triage -> independent review -> editor synthesis -> minimum-sufficient revision -> targeted re-review -> closure`.

For a theory-first paper, protocol/data/inference contracts are applied to the finite audit evidence and mechanical receipts rather than forced into an empirical-study template.

## Current archetype

```text
PRIMARY = theory / proof / analytical-framework paper
SECONDARY = method / evaluation-framework paper
TARGET_1 = arXiv public preprint
TARGET_2 = JMLR regular article
```

The paper is **not** treated as a systems paper, philosophical manifesto, or new generic state theory.

## Argument spine

```text
current prediction/current decision do not certify later revision
-> finite no-certification theorem and one-bit witness
-> strongest-parent subtraction
-> complete one-step compatibility criterion
-> Prospective Revision Audit V3
-> practical representation-assessment consequences
-> explicit empirical and channel-scope boundaries
```

## Atomic-claim release rule

A public arXiv master must not contain an in-scope manuscript assertion whose current status is `UNRESOLVED`, `CONTRADICTED`, or `BLOCKED`. Mechanically checked finite claims may be `VERIFIED`; parent-owned statements require source entailment; interpretation statements require bounded-inference wording. Human author identity/COI fields can remain outside the manuscript body until journal filing.

The journal package adds exact JMLR compliance but may not strengthen claims beyond the arXiv scientific master.

## Preprint/journal identity rule

The arXiv paper and JMLR paper are one scientific object with versioned exposition, not two scientific studies.

Allowed journal-only changes:

- JMLR style/metadata;
- page allocation and appendix placement;
- cover letter;
- final bibliography-status refresh;
- response to external reviewer/editor concerns;
- claim contraction/correction;
- additional already-valid explanatory material.

Not allowed merely for journal submission:

- stronger novelty language;
- hiding adverse/CANNOT_CHECK results;
- changing theorem assumptions after outcome access;
- deleting direct parents;
- introducing an empirical LLM result that was not executed;
- representing the arXiv version as a different scientific study.

## Current release boundary

The finite theorem/evidence package is strong enough for an arXiv/JMLR theory manuscript. The following remain outside the AI's authority:

- human authors/order/corresponding author;
- human intellectual-ownership adoption;
- conflicts/funding/overlap disclosures;
- final JMLR AE/reviewer suggestions after COI screening;
- real editorial acceptance.

Current internal target state:

`ARXIV_SCIENTIFIC_MASTER__READY_AFTER_FINAL_ATOMIC_SURFACE_CHECK`

Journal state:

`JMLR_PRIMARY_ROUTE__SCIENTIFIC_PACKAGE_COMPLETE__HUMAN_AND_EXTERNAL_GATES_OPEN`.
