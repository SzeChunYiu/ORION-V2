# External Editorial Review Packet V1

**Issue:** #51  
**Purpose:** obtain the one genuinely external judgment still blocking venue selection: whether the Prospective Revision Audit is independently paper-scale and JMLR-distinct after the strongest-parent contraction.

This packet is designed so an external reviewer does **not** need to reconstruct ORION-V2 history.

## 1. Material to send the reviewer

Minimum packet:

1. `MANUSCRIPT_DRAFT_V8_CITED.md`
2. `SUBMISSION_FRONTMATTER_V1.md`
3. `REVIEWER_TABLES_V1.md`
4. `CLAIM_LEDGER_V5.json`
5. `PROOF_APPENDIX_V1.md`
6. `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V2.md`
7. `CITATION_COVERAGE_MATRIX_V1.md`
8. `HOSTILE_EDITOR_REVIEW_V3_SUBMISSION_SURFACE.md`

Optional if requested:

- mechanical receipt corpus;
- parent theorem matrix;
- full nearest-work passes.

## 2. Reviewer role

Ask the reviewer to adopt one of these lenses:

- senior ML theory / information-state researcher;
- LLM memory/evaluation researcher;
- ML journal Action-Editor-level generalist with sequential decision expertise.

The reviewer should **not** be asked whether Machine Epistemics is a new field or whether ORION as a whole is valuable. The only object is this manuscript.

## 3. Scientific statement being reviewed

The paper does **not** claim new minimal predictive/decision/recurrent state mathematics.

It claims:

> After two representations have been matched on the declared current language-prediction target and registered current decision, later common evidence can expose a revision difference caused by historical information retained by one representation but not the other. Therefore current prediction+decision tests do not generally certify prospective revision adequacy. The paper formalizes this gap and defines a controlled representation audit.

Canonical finite witness:

```text
C_stat^* = 0 bits
C_dyn^*  = 1 bit
Omega_dyn = 1 bit
```

with a unique current action.

## 4. Mandatory strongest parents already conceded

The reviewer should assume the manuscript **does not own**:

- causal states / PSR;
- decisional states / Blackwell decision sufficiency;
- R-PSR secondary-target insufficiency;
- IB/DIB and value-aware compression;
- POMDP/AIS recurrent sufficient state;
- compatible/right-congruent FSM minimization;
- stable quotient / minimal Markovization;
- retentive memory theory;
- LLM belief revision after evidence;
- LLM context/state compression;
- prospective-intention memory;
- decision-aware/bounded agent memory.

A recommendation should not depend on giving the manuscript novelty credit for these.

## 5. Exact distinctness question

Please answer:

> **Is the following assessment object a sufficiently non-obvious and useful synthesis to justify an independent paper at JMLR scale?**
>
> `present language matched + present responsibility matched + retained-history representation manipulated/compared + identical later evidence + update AND maintain/selective-reopening scored + acquisition/alternate-channel controls`.

The question is deliberately stricter than “is every component new?”

## 6. Required reviewer decisions

### D1 — Correctness

Choose exactly one:

- `CORRECT_WITHIN_STATED_SCOPE`
- `MINOR_TECHNICAL_REPAIR`
- `MATERIAL_TECHNICAL_DEFECT`
- `CANNOT_CHECK`

State the strongest defect if not correct.

### D2 — Parent absorption

Choose exactly one:

- `FULLY_ABSORBED_BY_ONE_PARENT`
- `FULLY_ABSORBED_BY_OBVIOUS_PARENT_COMPOSITION`
- `PARTIALLY_PARENT_OWNED_WITH_RESIDUAL`
- `CANNOT_CHECK`

If fully absorbed, name the exact source(s) and theorem/protocol that reproduce the matched-current prospective audit, not just adjacent memory/revision work.

### D3 — JMLR distinctness/significance

Choose exactly one:

- `JMLR_SCALE_CLEAR`
- `JMLR_BORDERLINE_SUBMIT`
- `JMLR_TOO_THIN__TMLR_OR_FIELD`
- `NOT_STANDALONE_PAPER`

### D4 — ML audience utility

Choose exactly one:

- `CLEAR_ACTIONABLE_AUDIT_VALUE`
- `INTERESTING_BUT_NICHE`
- `MOSTLY_REPACKAGING`
- `NO_CLEAR_ML_USE`

### D5 — empirical necessity

Choose exactly one:

- `THEORY_ASSESSMENT_PAPER_CAN_STAND_WITHOUT_REAL_LLM_RUN`
- `REAL_LLM_BRIDGE_NEEDED_FOR_JMLR_BUT_NOT_SCIENTIFIC_VALIDITY`
- `REAL_LLM_RESULT_NEEDED_FOR_ANY_STANDALONE_PUBLICATION`

The reviewer should distinguish venue strength from correctness.

## 7. Hostile questions to answer explicitly

1. Is the no-certification theorem too immediate from a standard fibre/decision argument to support a paper, even when the paper claims the **audit** rather than the theorem as the main contribution?
2. Does Belief-R + MEMENTO + information-state theory already imply the complete registered audit in an obvious way?
3. Does the present-equivalence gate materially change the question compared with ordinary before/after evidence evaluation?
4. Is the alternate-channel retention gate a substantive causal-control improvement or merely good experimental hygiene?
5. Are update **and** maintain/selective-reopening jointly necessary to distinguish revision from indiscriminate updating?
6. Would this framework change how you evaluate context compression, memory summaries, retrieval memory, or hidden-state interventions?
7. Is the manuscript understandable without ORION/Machine-Epistemics context?
8. Which single section would you delete first if the paper feels over-engineered?

## 8. Reviewer output template

```text
CORRECTNESS =
PARENT_ABSORPTION =
JMLR_DISTINCTNESS =
ML_UTILITY =
EMPIRICAL_NECESSITY =

STRONGEST_PARENT_MISSED =
STRONGEST_REASON_TO_ACCEPT_AS_STANDALONE =
STRONGEST_REASON_TO_REJECT_AS_STANDALONE =
MANDATORY_MANUSCRIPT_CHANGE =
OPTIONAL_MANUSCRIPT_CHANGE =
```

## 9. Venue-routing rule after external review

```text
IF PARENT_ABSORPTION in {FULLY_ABSORBED_BY_ONE_PARENT, FULLY_ABSORBED_BY_OBVIOUS_PARENT_COMPOSITION}:
    standalone = MERGE_OR_DROP

ELSE IF JMLR_DISTINCTNESS == JMLR_SCALE_CLEAR:
    JMLR_route = OPEN_SUBJECT_TO_AUTHORSHIP/FILING_GATES

ELSE IF JMLR_DISTINCTNESS == JMLR_BORDERLINE_SUBMIT:
    authors decide risk tolerance; claims cannot expand

ELSE IF JMLR_DISTINCTNESS == JMLR_TOO_THIN__TMLR_OR_FIELD:
    TMLR only if AI/authorship policy gate passes; otherwise choose compatible field venue/flagship merge

ELSE IF JMLR_DISTINCTNESS == NOT_STANDALONE_PAPER:
    merge into flagship or drop
```

No external review outcome authorizes retroactive theorem invention under issue #51.

## 10. Independence boundary

An external review should come from a person who did not generate the theory/manuscript and is not being instructed to agree with the desired venue. Same-model critique, another prompt to the same assistant, or a mechanical checker does **not** satisfy this gate.
