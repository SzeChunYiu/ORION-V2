# Current Research Status V8 — Prospective Revision Audit

**Issue:** #51  
**Branch:** `research/llm-epistemic-sufficiency-theory-20260829`  
**Status date:** 2026-08-29  
**Supersedes:** `CURRENT_RESEARCH_STATUS_V1.md` through V7 for current execution/publication handoff.

## 1. Frozen scientific object

Title:

> **Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations**

Question:

> **After a representation is already matched on the declared linguistic prediction target and the registered current responsibility decision, can later evidence expose a revision failure caused by historical information that the representation failed to retain?**

The paper is a **formal assessment task / analytical framework**. Generic predictive/decision/recurrent state theory is parent-owned and not claimed as novelty.

## 2. Primary supported theorem

There exists a finite process and two representations with:

1. equal adequacy for the declared complete linguistic prediction target;
2. equal zero-regret current responsibility decision;
3. unequal future evidence-triggered revision adequacy.

Canonical exact witness:

```text
C_stat^* = 0 bits
C_dyn^*  = 1 bit
Omega_dyn = 1 bit
```

with a unique current action.

Therefore:

> **present prediction + present decision cannot, in general, certify prospective revision adequacy.**

The theorem is supported by a human-readable proof and exact mechanical witness. It does not establish empirical frequency in deployed LLMs.

## 3. Compatibility correction after V7

The prior pairwise revision-collision diagnostic remains a valid **sufficient failure witness**, but it is not a complete test when three or more histories share one representation/evidence cell and future acceptable-action sets contain ties.

Complete exact one-step `ANY_OPTIMAL_ACTION` criterion:

\[
\mathcal I(z,x)
=
\bigcap_{h: Z(h)=z,\;\delta(h,x)\text{ defined}}
A_x^*(h).
\]

A deterministic future decision rule using only `(z,x)` exists for the entire cell iff

\[
\mathcal I(z,x)\neq\varnothing.
\]

Mandatory counterexample to pairwise completeness:

```text
A1={a,b}
A2={b,c}
A3={a,c}
```

Every pair overlaps but the three-way intersection is empty.

The canonical one-bit witness is unchanged because its future acceptable-action sets are singleton `REOPEN` and `RETAIN`.

Sources:

- `PROSPECTIVE_REVISION_COMPATIBILITY_CRITERION_V1.md`
- `papers/llm-machine-epistemics/MANUSCRIPT_CORRECTION_REGISTER_V1.md`
- `papers/llm-machine-epistemics/CLAIM_LEDGER_V6.json`

This is a diagnostic completeness correction, not a new novelty claim.

## 4. Strongest-parent contraction

No novelty is defended for generic:

- causal states / PSR;
- decisional states / Blackwell sufficiency;
- R-PSR;
- IB/DIB/task-aware compression;
- VE/PVE/VES;
- POMDP belief/information state;
- AIS;
- incomplete-FSM compatible/closed-cover state reduction;
- stable quotient/minimal Markovization;
- retentive finite memory;
- BAMDP epistemic-state abstraction;
- log-loss rate distortion;
- iterated belief-revision storage;
- LLM belief revision after new evidence;
- LLM context/state compression;
- prospective-intention memory;
- decision-aware/bounded memory;
- generic downstream failure after compression;
- evidence-informed/selected-evidence belief updating;
- representation identifiability;
- pairwise fibre/collision logic.

This contraction is irreversible under #51 unless a parent result is factually misread.

## 5. Direct LLM-neighbor boundary

Current direct neighbors include Belief-R, MEMENTO, PM-Bench, state-compression relays, Router-Mem, Decision-Aware Memory Cards, AgenticSTS, evidence-informed scientific LLM beliefs, and selected/omitted-evidence updating.

Bounded surviving audit sequence:

```text
match current language target
+ match current responsibility action/risk
+ intervene on / compare retained historical representation
+ validate actual removal across registered alternate channels
+ reveal identical later evidence
+ score update AND maintain/selective reopening
+ test joint future-action compatibility per representation/evidence cell
```

No universal first-work claim is authorized.

## 6. Protocol V2 + compatibility amendment

Canonical empirical protocol remains:

`research/llm-machine-epistemics/PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V2.md`

with the mandatory compatibility amendment:

`research/llm-machine-epistemics/PROSPECTIVE_REVISION_COMPATIBILITY_CRITERION_V1.md`.

The alternate-channel retention gate remains load-bearing. Visible deletion is not evidence of actual state removal when information may remain in prompt/context, KV, hidden activations, summary embeddings, retrieval keys, tool/session state, or external memory.

## 7. Mechanical evidence already complete

Merged #56–#59:

- Bell-complete static partitions through n=7: PASS;
- predictive structural checks: PASS;
- R21–R27 responsibility/tie semantics: PASS;
- acquisition/current/prospective controls: PASS;
- dynamic optimum and selector-refinement equality: PASS;
- `Omega_dyn >= 0`: PASS;
- canonical 1-bit witness: PASS;
- P0/P1/P2: PASS;
- horizon/family monotonicity/stabilization: PASS;
- U1–U5: PASS;
- registered log-loss parent benchmark reproduced with scope counterexample;
- claim/receipt crosscheck: zero mechanical failures;
- mutation battery: load-bearing assumptions exposed;
- mixed-P2: `CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS` after 5,826 machines.

The new C19 joint-intersection criterion has a human-readable elementary proof but is not yet separately mechanized. It is not publication-novelty-bearing; a future checker may add the three-history control mechanically.

## 8. Canonical publication sources

Use in this order:

1. `papers/llm-machine-epistemics/MANUSCRIPT_DRAFT_V8_CITED.md`
2. `papers/llm-machine-epistemics/MANUSCRIPT_CORRECTION_REGISTER_V1.md`
3. `papers/llm-machine-epistemics/SUBMISSION_FRONTMATTER_V1.md`
4. `papers/llm-machine-epistemics/CLAIM_LEDGER_V6.json`
5. `papers/llm-machine-epistemics/PROOF_APPENDIX_V1.md`
6. `papers/llm-machine-epistemics/REFERENCES_V1.bib`
7. `papers/llm-machine-epistemics/REFERENCES_CLASSICS_SUPPLEMENT_V1.bib`
8. `papers/llm-machine-epistemics/CITATION_COVERAGE_MATRIX_V1.md`
9. `papers/llm-machine-epistemics/REVIEWER_TABLES_V1.md`
10. `papers/llm-machine-epistemics/FIGURE_AND_DISPLAY_SPEC_V1.md`
11. `papers/llm-machine-epistemics/PAGE_AND_SECTION_BUDGET_V1.md`
12. `papers/llm-machine-epistemics/SUBMISSION_PACKAGE_MANIFEST_V1.md`
13. `papers/llm-machine-epistemics/SUBMISSION_READINESS_CONTRACT_V1.md`
14. `papers/llm-machine-epistemics/AI_USE_AUTHORSHIP_AND_REPRODUCIBILITY_V1.md`
15. `papers/llm-machine-epistemics/HOSTILE_EDITOR_REVIEW_V3_SUBMISSION_SURFACE.md`
16. `papers/llm-machine-epistemics/EXTERNAL_EDITORIAL_REVIEW_PACKET_V1.md`
17. `papers/llm-machine-epistemics/HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW_V1.md`
18. venue-specific cover/anonymization documents.

The mechanical assembler must apply the correction register; raw V8 alone is not the current final scientific surface.

## 9. Frontmatter / page budget

Frozen:

```text
SUBMISSION_ABSTRACT = 157 words
JMLR_RUNNING_TITLE = Prospective Revision Audit
RUNNING_TITLE_CHARS = 26
KEYWORDS = 5
JMLR_MAIN_PLUS_APPENDIX_TARGET = 27–33 pages
JMLR_RISK_THRESHOLD = >35 pages
JMLR_HARD_AVOID = >50 pages
```

Main text must remain assessment-centered. Parent-owned derivations/receipts move out before claim ceilings, alternate-channel controls, or direct-neighbor discussion are cut.

## 10. Venue state

### JMLR

```text
NEW_CORE_THEOREM_ROUTE = FAIL
ASSESSMENT_FRAMEWORK_ROUTE = BORDERLINE_HIGH_RISK
PRACTICAL_UTILITY = PASS
FORMAL_SUPPORT = PASS_CORE
CITATION/PARENT_BOUNDARY = PASS_SUBSTANTIVE
SUBMISSION_AUTHORIZED = NO
```

Only a genuinely external editorial distinctness judgment can open the JMLR filing route.

### TMLR

Editorial fit is stronger under soundness+audience-interest criteria, but current TMLR AI-use policy is a decisive gate. The project used LLMs extensively for literature discovery, theorem/formalization development, critique, software generation and drafting.

```text
HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW = OPEN
TMLR_HUMAN_SOURCED_POLICY_FIT = OPEN_DECISIVE
TMLR_SUBMISSION_AUTHORIZED = NO
```

No disclosure wording may hide the actual workflow.

## 11. Human/external gates now executable

External distinctness review packet:

`papers/llm-machine-epistemics/EXTERNAL_EDITORIAL_REVIEW_PACKET_V1.md`

Human ownership review:

`papers/llm-machine-epistemics/HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW_V1.md`

These gates cannot be completed by the research-generation AI itself.

## 12. Remaining tasks

### Mechanical/editorial

- [ ] apply manuscript correction register during LaTeX assembly;
- [ ] mechanically check the three-history joint-intersection fixture;
- [ ] assemble chosen venue LaTeX source;
- [ ] merge/use bibliography sources and validate citation coverage/status;
- [ ] generate figures/tables from frozen specifications/receipts;
- [ ] page-count/PDF-size/style checks;
- [ ] final copy edit after display placement;
- [ ] refresh 2026 preprint/public-review metadata before filing;
- [ ] bind final submission bytes/hashes.

### Human/external

- [ ] human intellectual-ownership review;
- [ ] final authorship/order/corresponding author;
- [ ] COIs/overlap/coauthor consent;
- [ ] external editorial distinctness review;
- [ ] JMLR AE/reviewer suggestions if route opens;
- [ ] optional real-LLM Protocol-V2 execution.

No remaining task authorizes new theorem invention, parent-concession reversal, AI-use concealment, or empirical claim fabrication under #51.

## Current terminal

```text
NONCOMPUTE_SCIENCE = CLOSED_WITHIN_CURRENT_IDENTITY
NO_CERTIFICATION_THEOREM = SUPPORTED
ONE_STEP_COMPATIBILITY = COMPLETE_AFTER_JOINT_INTERSECTION_CORRECTION
CITED_MANUSCRIPT = READY_WITH_REGISTERED_CORRECTIONS
BIBLIOGRAPHY = READY_WITH_PRE_SUBMISSION_STATUS_REFRESH
PROSPECTIVE_REVISION_AUDIT = STANDALONE_ANALYTICAL_FRAMEWORK_CANDIDATE
REAL_LLM_P2_FAILURE = NOT_ESTABLISHED
JMLR = BORDERLINE_EXTERNAL_DECISION
TMLR = POLICY_GATED
REMAINING = MECHANICAL_PACKAGE + HUMAN_AUTHORSHIP/COI + EXTERNAL_REVIEW

CURRENT_TERMINAL = THEORY_PAPER_RESIDUAL_SUPPORTED_AS_PROSPECTIVE_REVISION_ASSESSMENT__SUBMISSION_NOT_YET_AUTHORIZED
```
