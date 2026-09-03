# Flagship Independent Review — Reviewer Selection V2 (re-scoped to the V23 claim)

**State date:** 2026-09-03
**Serves:** `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V4_V23.md` (manuscript V23, sha256 `3a8805f6…7d3ed`)
**Supersedes for selection:** `FLAGSHIP_DEMARCATION_REVIEWER_SELECTION_V1.md` (served packet V3/V21). V1 is **not edited**: its eighteen verified rows, its cluster map and its verification ledger remain the record of what was checked on 2026-09-02, and they stay usable. What changes is which of them the question needs.
**Authority:** none. This document proposes. It contacts, binds and represents no one, records no contact details, and naming a person is not a claim that they have agreed to anything or hold any view of the programme.

---

## 1. Why the shortlist has to be re-selected, not carried across

V1's first criterion read: *native ownership of a parent … the strongest reviewers are those the programme would have to lose to.* That is the correct criterion when the claim is **a new field**, because the way a field claim dies is that a parent discipline turns out to own it.

The programme has now lost to the parents, by its own measurement, and said so in the manuscript. The claim under V4 is that what survives the loss — a specification of what must cross a module boundary, and an executable benchmark — is a contribution. Two different questions follow, and neither is the one V1 optimized for:

1. **Does this add to a standard you already own?** The decisive expertise is whoever maintains the nearest existing standard, not whoever could have subsumed the field.
2. **Is the negative safe?** The decisive expertise is benchmark validity — whether the null was strong enough, whether the generators make the comparison unfair, whether a five-rung exchange ladder is an instrument or a free parameter.

Selecting a panel for question (1) from a list built for field subsumption gives a panel that can only bless or downgrade. Question (2) has **no candidate on the list at all**.

## 2. Lens re-weighting

| Lens | V1 role | V4 role | Why |
|---|---|---|---|
| **L1** formal / computational epistemology, philosophy of science, social epistemology | co-primary; owned the strongest subsumption threat | **supporting** | D1, D3, D9, D10, D11 and D17's field-and-name content is largely withdrawn. L1 remains required for naming honesty (S7), for whether a negative-result Perspective is worth publishing (S13), and for the Duhem–Quine and severe-testing grounding the locus interface rests on (S10). The single sharpest V1 threat, formal learning theory as a mathematical normative epistemology, is much less decisive now: its question has been answered in the parents' favour |
| **L2** AI for science, agentic / autonomous science, scientific ML | primary | **retained, re-pointed** | from "does a working robot scientist already make these decisions?" to "would this exchange specification change anything in the system you actually run, and is the federation you would build stronger than B5?" (S2, S4) |
| **L3** systems / control, formal methods, metareasoning, assurance, provenance | third lens | **primary** | this lens owns every comparator the claim must now beat. V23's own text names W3C PROV as the nearest standard and concedes it already covers derivation and lineage. S2 is largely an L3 question, and so is half of S4 |
| **L4** benchmark validity and empirical evaluation methodology | **absent** | **new, required** | the second deliverable is an executable benchmark whose headline result is a negative. Without L4 the gate cannot return `NEGATIVE_NOT_EARNED__NULL_TOO_WEAK` or `NEGATIVE_OVERSTATED__NULL_OPTIMAL_BY_CONSTRUCTION`, which means it cannot tell the authors their contraction is unsupported. A gate that can only agree with the authors' negative is not checking it |

## 3. L4 — what the lens must be able to do

Native competence in the design and critique of empirical evaluation: known-answer and oracle-based benchmarks, baseline strength and strawman detection, construct validity, generator-induced artifacts, pre-registration and protocol adherence, multiple-comparison and ablation discipline, and the reading of a null result.

It must be able to answer, from its own expertise and without taking the authors' word:

- whether B5 is the strongest faithful composition an expert would build, or whether a component is mis-parameterized, under-informed or a strawman (S4);
- whether a world with uniform decidability and strictly increasing cost bands makes an exact expected-cost planner optimal by construction, and what that does to the comparison (S5);
- whether four known-answer worlds with no naturalistic cell executed license a contraction of this size (S5);
- whether the five-rung exchange ladder is a valid instrument or a free parameter re-registered per study, given that the decisive rung differs across the four studies (S6);
- whether an ablation priced by removal (79 / 98 / 181) supports the requirement it is quoted for (S10).

**No names are recorded for L4.** This lane verified nobody to V1's standard — one affiliation URL and one publication URL consulted — and recording an unverified name here would be exactly the kind of unbacked specific the programme forbids. Selecting L4 is an open operator task, and until an L4 answer is on file the gate's state is `CANNOT_CHECK__LENS_MISSING`, not a pass.

## 4. What carries over from V1, and what does not

**Carries over unchanged:** criteria 2–7 (no prior involvement; no shared dependence across the panel; written answer in 2–3 hours ending in one terminal including the negative ones; hostile is fine and advocacy is disclosed; institutional and geographic diversity), the cluster map, and the verification ledger with its stated limits.

**Amended.** Criterion 1 becomes: *native ownership of a comparator or of the evaluation method*, i.e. the reviewer maintains, authored or routinely applies the standard or practice the claim must be measured against, or is competent to judge the benchmark. Criterion 3 (no access to internal outcomes) is **retired** — the outcomes are public and in the manuscript's abstract; exposure is now a recorded interpretive fact, not a disqualification.

**Effect on V1's rows, by lens.** These are re-weightings of already-verified rows, not new verifications, and no row is deleted.

- *L3 becomes the primary lens.* The provenance rows are now the most decisive on the list, because V23 names PROV as the nearest standard in its own text; the assurance rows carry "evaluator independence", "non-amplifying authority" and "witness" as existing practice, which is the exact content of two interface rows. Cluster P and cluster A both still bind at **one member each**, and that constraint bites harder now that both clusters sit on the primary lens rather than the third.
- *L2 rows remain apt* and are re-pointed to S2 and S4; a builder of agentic scientific runtimes with typed execution and provenance is now judging whether the specification changes their own system, not whether they already own the field.
- *L1 rows narrow.* The candidates who owned epistemic control as prior terminology and the social epistemology of AI-based science remain decisive, the first for S7 and the second for the collective-inquiry family V23 says its negative constrains least. The formal-learning subsumption row loses most of its decisiveness with the field claim.

## 5. Panel admissibility under V4

Four lenses, at least one written answer each, one reviewer assigned to exactly one lens even where competent across several. No two panel members from one V1 cluster. At most one reviewer who has authored a standard named as a comparator in S2 per lens, so that the panel is not a single standard's committee reviewing whether the claim adds to that standard.

A panel missing L4 is **not** a reduced panel; it is a gate that has not checked its own negative, and it is recorded as `CANNOT_CHECK__LENS_MISSING` rather than as a weaker pass.

## Terminal

```text
SERVES = PACKET_V4_V23
LENSES = 4 (L1 supporting, L2 retained, L3 primary, L4 new and required)
V1_ROWS_DELETED = 0 (re-weighted; V1 unedited and still the verification record)
CRITERION_1 = AMENDED (comparator or evaluation-method ownership)
CRITERION_3 = RETIRED (outcome-blindness is structurally unavailable)
L4_NAMED_CANDIDATES = 0 (none verified by this lane; open operator task)
PANEL_SELECTED = NONE
CONTACT_DETAILS_RECORDED = NONE
AUTHORITY = NONE
```
