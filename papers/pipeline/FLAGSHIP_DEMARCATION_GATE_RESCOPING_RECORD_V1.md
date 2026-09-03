# Flagship External Demarcation Gate — Re-scoping Record V1

**State date:** 2026-09-03
**Gate:** issue #38, external dependency `X05_FIELD_DEMARCATION`
**Trigger:** the flagship was retitled and contracted (PR #43, squash `446f522`) to *Warranted Scientific-State Transitions — An interface standard and benchmark for reliable agentic science*. The gate's registered question, its frozen reviewer questions and its reviewer shortlist were all built against a **field** claim the manuscript no longer makes.
**Authority:** none. This record establishes state and re-scopes a question. It adjudicates nothing, marks nothing passed, contacts no one, and grants no field, novelty or publication status.

---

## 1. The defect being recorded

A gate whose machinery runs correctly and returns a verdict about a claim that has been withdrawn is not a failed gate — it is a gate whose **scope no longer covers what it is trusted to cover**. It sits one level above a vacuous check: nothing malfunctions, and the answer is about nothing. Left alone it fails in the worst available way, by being quietly treated as satisfied because nobody re-read it.

This record establishes the gate's actual state from artifacts, marks per criterion what is stale and what is not, and hands the re-scoped question to packet V4.

## 2. Established state (from artifacts, not from the issue title)

| Item | Registered artifact | State on `origin/main` at 2026-09-03 |
|---|---|---|
| Reviewer packet in force | `papers/pipeline/FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V3_V21.md` | bound to manuscript **V21**, sha256 `e6796fbf…0d83eb`; `REVIEW_STATUS = READY_TO_BIND_GENUINELY_INDEPENDENT_REVIEWERS` |
| Frozen questions | packet §13 | D1–D12 verbatim from V2, D13–D18 appended 2026-09-02 |
| Post-outcome addendum | `…_V3_RESULT_ADDENDUM_ME_X_SERIES.md` | adds D19; discloses the contraction; states the packet's binding manuscript **remains V21** and D1–D18 remain the object |
| Allowed terminals | packet §12 | seven field-shaped terminals, plus the rename qualifiers |
| Reviewer criteria and shortlist | `papers/pipeline/FLAGSHIP_DEMARCATION_REVIEWER_SELECTION_V1.md` | serves the V21 packet; 18 named candidates over 3 lenses; `PANEL_SELECTED = NONE`, `CONTACT_DETAILS_RECORDED = NONE` |
| External dependency | `research/closure/EXTERNAL_DEPENDENCY_REGISTER_WAVE06_V1.json` → `X05_FIELD_DEMARCATION` | `state: OPEN`; three required roles, all field-lens shaped |
| Reviewer answers on file | — | **none** |
| Current manuscript | `ORION-paper:v2-papers/FLAGSHIP-machine-epistemics/manuscript/public/FLAGSHIP_MACHINE_EPISTEMICS_PERSPECTIVE_V23_CONTRACTED.md` | sha256 `3a8805f696329261cef075fdf493197dab4febbe21fc9c84547f40e71a47d3ed` (coherence-corrected master, four studies) |

### 2.1 No reviewer verdict exists — with the scope of that claim justified

Item 4 of the re-scoping brief — mark any verdict given against the withdrawn claim `SUPERSEDED__ANSWERED_A_WITHDRAWN_CLAIM` — is **honestly vacuous**. The register below is created empty rather than skipped, so that a later answer has a place to land.

Searches run, each shaped differently, both repositories:

1. the seven field terminals (`CANDIDATE_FIELD_DEMARCATION_SUPPORTED`, `INTEGRATION_ENGINEERING_ONLY`, `CANNOT_CHECK_FIELD_SEPARATION`) — hits only in packets, claim gates, audits and superseded manuscripts;
2. the answer-shaped terminals a reviewer would actually write (`RESIDUAL_IS_INTERFACE_STANDARD_AT_MOST`, `HYPOTHESIS_EMPTY_AS_STATED`, `NO_SUPERIORITY_IMPLICATION_FOUND`, `RENAME__OBJECT_SURVIVES`, and D19's four) — same file classes, no answer file;
3. a basename `find` for `*review*response*`, `*reviewer*`, `*declaration*`, `*panel*` across both trees — the only flagship-demarcation hit is the selection document itself;
4. `X05_FIELD_DEMARCATION` in the external dependency register — `OPEN`, no answers;
5. all six comments on issue #38 — all authored by the operator, all instructions to the gate, none a reviewer answer.

Each pass was run with a control pattern that had to match and did (`Machine Epistemics`: 202 files in ORION-V2, 165 in ORION-paper; `D19`: 3 files).

**Two near-misses, recorded because their proximity to the gate is itself a mislabelling risk.** `papers/pipeline/FLAGSHIP_SIMULATED_REVIEW_ROUND_V1.md` and `ORION-paper:…/reviews/FLAGSHIP_HOSTILE_DEMARCATION_STRESS_TEST_V3.md` contain field-shaped terminals and reviewer-shaped prose. They are **internal simulations**, explicitly excluded from this gate by packet V3 §10 and by the register's `internal_ai_cannot_self_grant_external_authority` rule. They are not gate evidence and must never be counted as an answer.

```text
SUPERSEDED__ANSWERED_A_WITHDRAWN_CLAIM register
entries = 0
reason  = no external reviewer was ever bound; PANEL_SELECTED = NONE
scope   = five independently shaped passes over both repositories, above
status  = OPEN — any pre-2026-09-03 answer that later surfaces is filed here, not in the V4 gate
```

## 3. What is stale, per criterion

Judged against the V23 bytes named in §2. **Fifteen of nineteen questions retain content; four are dead.** Manufacturing staleness where none exists would be the mirror of the defect this record names, so the unaffected ones are marked unaffected.

### 3.1 Survives; re-point to the V23 bytes only (8)

| Q | Why it survives |
|---|---|
| D1 object coherence | Box 1 survives V23 intact, with the receipt/witness distinction |
| D2 strongest parents | unchanged, and **more** load-bearing: the standard must now be measured against a named parent, not merely distinguished from one |
| D8 atlas / horizon | retained in V23 and now carries measured support (17 false closures by the strongest truth-maintenance federation, recovered once an atlas module was present) |
| D12 publication value and omitted literature | live in both halves; the article is now a negative-result Perspective, which changes the answer's difficulty, not the question |
| D14 world ≠ machine | the separation survives in the Box 1 non-implications; quoted passages must be re-checked because some V21 prose was cut |
| D15 discrepancy-locus interface | retained, and now priced by ablation (79 / 98 / 181 false escalations or missed escalations) |
| D18 superiority-ladder audit | figure files are unchanged; Table 1's row is renamed, so the audit must run on V23 bytes |
| D19 does the standard survive its own negative | correctly scoped from the day it was written; **becomes the gate's primary question** |

### 3.2 Partly stale — one clause withdrawn, the rest live (7)

| Q | Withdrawn clause | Surviving clause |
|---|---|---|
| D3 epistemology boundary | "does the proposal draw a **boundary** from formal learning / formal / social epistemology" — V23 draws none, it states an interface between them | does the specification add anything those parents do not already specify |
| D4 machine-X taxonomy | "does **Machine Epistemics** invite a superiority reading" — the label is withdrawn from title, abstract and body | is the taxonomy itself useful, misleading or redundant; the row is now *Scientific-transition control* |
| D6 frontier / invention | "warranted possibility-space transformation" — the `Generative regimes` section is **cut** and Γ_t retired; a reviewer would be judging text that no longer exists | obstruction-first action routing survives as one clause of the escalation gate |
| D7 locality / diverse intelligence | donor categories, anthropomorphism, `evolution = cognition` (EL20) have no counterpart in V23 | the locality principle survives as a V23 section |
| D11 falsifiability and cross-domain burden | "what would make you abandon the **distinct-field** claim" — abandoned by the authors | the cross-domain pair burden survives, partly and only partly discharged: ME-X5 ran three native modes under one authorship, and its own receipt records that no independent-adjudication rung is grantable from it |
| D13 interface standard versus control | the counterfactual form, "**suppose** the registered prediction resolves as branch (a)" — it resolved, four times | the hostile third clause (construct a case where structure exchange is unavailable, or trivially available) survives verbatim and is sharper now |
| D17 name relative to adjacent vocabulary | "does the compound *Machine Epistemics* improve demarcation" — the compound is gone | the rename machinery and the `RENAME__OBJECT_SURVIVES` / `RENAME_AND_CONTRACT` qualifiers apply to the new title |

### 3.3 Wholly superseded (4)

| Q | Why it is about nothing |
|---|---|
| **D5** composition residual, asked as a pre-outcome plausibility judgement | four exact-oracle studies answered it: 1,200 / 1,000 / 1,440 identical, 1,200 in the federation's favour. A reviewer cannot supply a pre-outcome plausibility estimate for a question with a measured answer in the abstract |
| **D9** field versus integration status, explicitly "**before AH20 outcome disclosure**" | dead twice over: the field claim is withdrawn by the authors, and outcome-blindness no longer exists |
| **D10** "without seeing naming history, what does **Machine Epistemics** mean to you?" | the label appears in V23 only in repository file names and the availability register |
| **D16** pre-commitment before outcome disclosure | structurally impossible: V23 reports the outcomes in sentence three of its abstract. No future reviewer can be outcome-blind |

## 4. The property the gate has permanently lost

Packet V3's core discipline was **outcome-blindness**: reviewers judged before knowing what the studies found. That is now unavailable, not by choice but by construction — the manuscript leads with the outcomes. This is recorded as a **loss**, not a satisfied condition. Packet V4 replaces it with the only device still available: a written pre-commitment on the **unrun** families V23 itself names open — formal mathematical discovery, collective inquiry, and witness sufficiency — registered before those families report.

## 5. The reviewer-selection problem, stated as a requirement

Selection V1's first criterion was *native ownership of a parent*, on the reasoning that "the strongest reviewers are those the programme would have to lose to." That is the right criterion for a **field** claim. Under V23 the programme has already lost to the parents, by its own measurement. The decisive question is no longer who could subsume it but whether what survives adds to an existing standard, and whether the negative is safe.

Consequences are recorded in `FLAGSHIP_DEMARCATION_REVIEWER_SELECTION_V2.md`. The load-bearing one: **no candidate on the eighteen-name list holds benchmark-validity or empirical-evaluation-methodology expertise**, and the second deliverable is an executable benchmark whose headline is a negative. Without that lens the gate can bless the standard or downgrade it, but cannot tell the authors their negative is unsafe. A fourth lens is therefore a **requirement**, not a preference, and reviewers must be re-selected rather than carried across.

## 6. Three drift instances found while establishing state

Each is the same defect class, and each is repaired by this lane rather than left standing.

1. **Issue #38's body** still names `papers/drafts/FLAGSHIP_MACHINE_EPISTEMICS_MANUSCRIPT_V4.md` as the current manuscript and `…PACKET_V1.md` as the reviewer packet. Both were superseded twice before the contraction. Repaired in the issue update accompanying this record.
2. **Terminal-set drift.** Issue comment 2026-08-29 registered a seven-terminal set including `RENAME__OBJECT_SURVIVES`, `RENAME_AND_CONTRACT` and `CANNOT_CHECK`; packet V3 §12 froze a different seven, with the renames demoted to qualifiers of one terminal. Reconciled explicitly in V4 §4.
3. **The addendum is one study stale.** `…_RESULT_ADDENDUM_ME_X_SERIES.md` reports three studies; V23 reports four (ME-X5, cross-domain, 1,440 instances, receipt `024d97f`, positive equivalence test in all three modes). V4 supersedes both V3 and its addendum for new reviewers and binds the four-study count.

## Terminal

```text
GATE = X05_FIELD_DEMARCATION (issue #38)
GATE_STATE = OPEN__RESCOPED
QUESTIONS_ASSESSED = 19
RE_POINT_ONLY = 8 | PARTLY_STALE = 7 | WHOLLY_SUPERSEDED = 4
REVIEWER_ANSWERS_ON_FILE = 0
SUPERSEDED__ANSWERED_A_WITHDRAWN_CLAIM = 0 (register created, scope justified in §2.1)
OUTCOME_BLINDNESS = LOST_PERMANENTLY
PANEL_SELECTED = NONE
NEW_LENS_REQUIRED = L4_BENCHMARK_VALIDITY
SUCCESSOR_PACKET = FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V4_V23.md
GATE_PASSED = FALSE (this lane may not and does not adjudicate)
AUTHORITY = NONE
```
