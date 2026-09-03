# Independent Review Packet V4 — Warranted Scientific-State Transitions (bound to manuscript V23)

**Packet date:** 2026-09-03
**Manuscript binding:** *Warranted Scientific-State Transitions — An interface standard and benchmark for reliable agentic science*, V23 contracted
**Manuscript file:** `ORION-paper:v2-papers/FLAGSHIP-machine-epistemics/manuscript/public/FLAGSHIP_MACHINE_EPISTEMICS_PERSPECTIVE_V23_CONTRACTED.md`
**Manuscript sha256:** `3a8805f696329261cef075fdf493197dab4febbe21fc9c84547f40e71a47d3ed`
**Supersedes for all new reviewers:** `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V3_V21.md` (bound to V21, sha256 `e6796fbf…0d83eb`) **and** its post-outcome addendum `…_V3_RESULT_ADDENDUM_ME_X_SERIES.md` (which reports three studies where V23 reports four).
**Neither is rewritten.** V3's questions D1–D18 and the addendum's D19 stand exactly as frozen. What changes is which question this gate asks, and of whom.
**Authority:** none. This packet proposes and asks. It contacts no one, binds no one, and grants no field, novelty, submission or publication status. `GATE_PASSED = FALSE`.

---

## 1. Why the question changed, and what that says about the gate

Packet V3 asked independent reviewers to judge whether a **new field** was being claimed. Between V3 and this packet the manuscript withdrew that claim. Its own registered discriminator fired against it: four pre-registered exact-oracle studies found that once mature parent modules exchange typed structure, an information-matched federation reproduces every decision the proposed controller makes, and on one registered problem decides better. The manuscript was retitled and contracted; the label *Machine Epistemics* was withdrawn from title, abstract and body; the generative-regime section, Γ_t, the implementation-requirements section, the F2 foundation and the prospective-families section were cut or demoted.

A gate left pointed at the old claim would have run correctly and answered a question nobody is asking. That is a defect of **scope**, not of machinery, and it is the defect this programme exists to name. It is recorded, with the per-criterion assessment behind this re-scoping, in `FLAGSHIP_DEMARCATION_GATE_RESCOPING_RECORD_V1.md`.

**Superseded question** (V3, frozen, still answerable *about the withdrawn claim*):

> Are the proposed object, scientific residual, field boundary and working label *Machine Epistemics* coherent, useful and nonredundant — and is a distinct field being claimed?

**Registered question from this date:**

> Is the **interface standard** a genuine scientific contribution distinct from the nearest existing standard or practice; is the reported **negative** earned by a null strong enough to support it; and is the article **named honestly** for what it actually delivers?

The claim under review is narrower and more defensible than a field claim. That does not make the gate easier. A narrow claim can be checked exactly, so this packet is written so that it can **fail in three independent directions**: the standard may be ordinary integration engineering; the negative may be unearned or overstated; and the deliverables may be misnamed.

## 2. One property this gate has permanently lost

V3's discipline was outcome-blindness. It is gone, and not by choice: V23 reports its outcomes in sentence three of its abstract, so no future reviewer can supply a pre-outcome judgement. This is recorded as a loss, never as a satisfied condition. Its replacement is **S12**, a written pre-commitment on the three families V23 itself leaves open, registered before those families report. A reviewer who has already read the outcome receipts is fully admissible here; that was disqualifying under V3 and is not under V4.

## 3. What the reviewer receives

The V23 manuscript with its three figures, and this packet. On request: the four outcome receipts in `SzeChunYiu/ORION-V2` (`research/experiments/me-x{4,1,2,5}/…_OUTCOME_RECEIPT.md`), the deposited designs, and V3 with its addendum. Nothing else from the project is supplied; repository development history, issue and PR chronology, internal simulated reviews and internal clean-room reads remain withheld, as under V3.

Expected effort: 2–3 hours. Answer S1–S13 in writing, independently, before discussing with any other reviewer, and end with exactly one primary terminal from §4. `CANNOT CHECK` is valid, useful and preferred over a guess. No answer is preferred.

## 4. Terminals

### 4.1 Primary set — bound to the V23 claim. Choose exactly one.

```text
INTERFACE_STANDARD_IS_A_SCIENTIFIC_CONTRIBUTION
STANDARD_AND_BENCHMARK_BOTH_CONTRIBUTE
BENCHMARK_IS_THE_ONLY_CONTRIBUTION
INTERFACE_STANDARD_IS_ORDINARY_INTEGRATION_ENGINEERING
NEITHER_SURVIVES
NEGATIVE_NOT_EARNED__NULL_TOO_WEAK
NEGATIVE_OVERSTATED__NULL_OPTIMAL_BY_CONSTRUCTION
CONTRACTION_INSUFFICIENT__RESIDUAL_CLAIM_STILL_OVERSTATED
RENAME_REQUIRED__DELIVERABLE_MISNAMED
CANNOT_CHECK_STANDARD_CONTRIBUTION
```

The first four extend D19's set. The next three are new and are the reason this gate is harder than V3's: they let a reviewer rule that the authors' **own negative** is unsafe — that the federation was built too weak for the negative to mean anything, that it was optimal by construction so the comparison was never fair, or that the contraction did not go far enough. A field-shaped gate could not return any of these.

### 4.2 Secondary set — retained, and scoped to the withdrawn claim

The seven terminals frozen by V3 §12 are **not removed**; the addendum promised none would be, and `INTEGRATION_ENGINEERING_ONLY` is now plausibly correct.

```text
CANDIDATE_FIELD_DEMARCATION_SUPPORTED   USEFUL_INTERDISCIPLINARY_RESEARCH_PROGRAMME
INTEGRATION_ENGINEERING_ONLY            SUBFIELD_OF_EXISTING_PARENT
RENAME_SCIENTIFIC_PROGRAMME (…__OBJECT_SURVIVES | …_AND_CONTRACT)
FIELD_BOUNDARY_TOO_FRAGMENTED           CANNOT_CHECK_FIELD_SEPARATION
```

They adjudicate **the withdrawn field claim only**. A secondary terminal may not be used to grant or deny anything about V23, and a reviewer may decline the secondary set entirely. *Reconciliation of a drift found while establishing state:* issue #38's 2026-08-29 comment registered a variant list in which the two rename qualifiers were standalone terminals and `CANNOT_CHECK` was unqualified. Packet V3 §12's list, reproduced above, is the one in force; the variant is superseded.

## 5. Questions, frozen from 2026-09-03

Where a question re-points a V3 question, that is named. Answer against the V23 bytes whose sha256 is on this packet's header, not against V21.

**S1 — Object under contraction** *(re-points D1)*. State the object of Box 1 in your own words from V23 alone, without naming ORION or any implementation. Give the narrowest definition you consider defensible. `YES, STABLE OBJECT` / `PARTLY, NEEDS REDEFINITION` / `NO, TOO HETEROGENEOUS`.

**S2 — Nearest existing standard, row by row** *(sharpens D19; admissibility rule in §6)*. V23's interface standard is a table of nine requirements. For **each row**, name the nearest existing standard or practice you would measure it against — W3C PROV, assurance cases, IV&V, ATMS/JTMS label semantics, contract-based design, interface control documents, metrological traceability, or another you name — and answer `ADDS <what>` / `SUBSUMED_BY <named standard>` / `CANNOT_CHECK`. A row you cannot attach a comparator to is recorded as such; it is not a pass.

**S3 — The two rows the paper itself weakens**. V23 concedes that *Execution and evidence separation* is "asserted from Box 1, not measured", and that *Bounded closure* is "parent-owned once representable". Should either be deleted from the standard, kept as an untested requirement, or kept with its status printed? If a nine-row table survives review with two rows nobody can defend, say so.

**S4 — Is the null the strongest faithful composition?** *(new; lens L4 and L3)*. The federation B5 routes each case to a mature method — provenance, dependence assessment, typed transport, measurement comparability, evaluator coverage, an authority lattice, truth-maintenance propagation, consistency-based diagnosis, expected-cost test sequencing. Is it genuinely the strongest faithful composition an expert would build, or is some component a strawman, mis-parameterized, or given information the fair version would not have? Name the specific component and the fair replacement.

**S5 — Is the negative earned?** *(new; supersedes D5's pre-outcome form)*. Four exact-oracle studies in known-answer worlds with finite registered action sets, no naturalistic cell run in any of them. One study's world has uniform decidability and strictly increasing cost bands, which V23 concedes make an exact expected-cost planner optimal by construction. Does the reported parent sufficiency support the contraction, or is it an artifact of the generators? `NEGATIVE_EARNED` / `NULL_TOO_WEAK` / `OPTIMAL_BY_CONSTRUCTION` / `CANNOT_CHECK`, with the decisive reason.

**S6 — Generator dependence of the ladder**. The rung at which exchange starts changing decisions differs **across the four studies** — rungs 2 and 4 in one, a single step from 4 to 5 in another, every step in the remaining two. Does that variation undermine writing one standard, or is it exactly what a standard should absorb? *Precision, because two different scales are easy to conflate:* the cross-study variation above is the claim. Within one study, the same manuscript's own erratum withdraws a cross-mode "decisive rung varies" flag as a mechanical argmax over steps separated by three instances of 480, establishing neither variation nor invariance. Do not read the withdrawn one as support for the live one.

**S7 — Naming honesty** *(re-points D10 and D17 onto the title that now exists)*. Does *interface standard* oversell a nine-row table of requirements, two of them unmeasured? Does *benchmark* oversell four synthetic known-answer worlds with no naturalistic cell executed? Is *Warranted Scientific-State Transitions* the honest name for what is delivered? If a rename is needed, propose the title a parent-field reader would recognize without explanation, and say whether the object survives it (`RENAME__OBJECT_SURVIVES`) or must contract further (`RENAME_AND_CONTRACT`).

**S8 — Strongest parents and omitted literature** *(re-points D2, D3, D12)*. Name the 1–3 traditions that most nearly subsume the surviving contribution, and any omitted work whose absence would make the article misleading. State whether the specification adds anything those parents do not already specify.

**S9 — Overclaim audit against the V23 bytes** *(re-points D14 and D18)*. Read Table 1 and the paragraph after it, Box 1, the three figures and their captions, and the Conclusion. Does any sentence or diagram element still imply a rank above learning or intelligence, that the target and the machine share one transition structure, that nature computes, that a representation can be identified with its target, or that the standard is settled rather than proposed? Quote it. If none, `NO_OVERCLAIM_FOUND`.

**S10 — Does the locus and escalation interface survive its own loss?** *(re-points D15, absorbs what remains of D6)*. The escalation study went **against** the controller: 0.983 to 0.963, exact p = 0.0032, and all 43 instances the federation won are the controller declaring *cannot yet identify* on a decidable episode. Ablations still price the interface's parts — 79 false escalations without the diagnostic-evaluator gate, 98 without the lower-level disposition, 181 warranted escalations missed without the prospective discriminator. Is the interface anything more than model-based diagnosis, impasse-triggered metareasoning, Duhem–Quine error localization and IV&V renamed? Which loci would you merge, split or delete? Is *cannot yet identify* an honest terminal or a refusal that hides underperformance?

**S11 — Local-to-global witness** *(re-points D8)*. V23 reports the one non-implication with direct measured support: the strongest truth-maintenance federation closed 17 cases it should have left open, taking pairwise compatibility for a global section, and recovered them as soon as an atlas module was present at all. Is this a useful interface requirement or a renaming of identifiability, model pluralism and sheaf-theoretic local-to-global parents? What evidence would justify deleting it?

**S12 — Pre-commitment on the unrun families** *(replaces D16; the replacement for lost blindness)*. Three registered families have not run: formal mathematical discovery, collective inquiry, and witness sufficiency. State now, in writing, which **specific outcome** of which family would move your primary terminal, and to which terminal. If no outcome would move it, say so and why. This answer is compared against any later post-outcome review and may not be revised retroactively.

**S13 — Publication value of a negative** *(re-points D12)*. Independent of the standard's status: is a Perspective whose headline is its own contraction sufficiently important and timely for a broad AI-science venue? `YES` / `YES AFTER MAJOR NARROWING` / `SPECIALIST ONLY` / `NO`.

## 6. Admissibility guards — how this gate refuses to be passed vacuously

A gate that cannot fail is not a gate. Each guard has its own outcome, distinct from a pass; **"could not check" is never recorded as "checked and fine."**

- **G1 — Lens coverage.** A primary terminal may be recorded only when at least one written answer is on file for **each** required lens L1–L4 (§7). Otherwise the gate state is `CANNOT_CHECK__LENS_MISSING`, naming the missing lens. Missing L4 in particular means the negative was never checked by anyone competent to check it.
- **G2 — Named comparator.** `INTERFACE_STANDARD_IS_A_SCIENTIFIC_CONTRIBUTION` or `STANDARD_AND_BENCHMARK_BOTH_CONTRIBUTE` is admissible only from a reviewer who named a specific existing standard for **every** row in S2 and stated the delta. A positive without named comparators is recorded as `CANNOT_CHECK_STANDARD_CONTRIBUTION`.
- **G3 — Binding.** Every answer records the sha256 of the bytes it was given. An answer against any other bytes is filed with its own binding and is not counted for this gate.
- **G4 — No self-adjudication.** No ORION lane, agent, contributor or simulated review may supply an answer. `FLAGSHIP_SIMULATED_REVIEW_ROUND_V1.md` and `FLAGSHIP_HOSTILE_DEMARCATION_STRESS_TEST_V3.md` contain reviewer-shaped prose and field-shaped terminals; they are internal and are **not** gate evidence.
- **G5 — Reachable adverse terminal.** At least two adverse primary terminals must be reachable on the current bytes, or the gate has been loosened and must be re-scoped again. On V23 they are: `NEGATIVE_OVERSTATED__NULL_OPTIMAL_BY_CONSTRUCTION`, reachable because the manuscript concedes one world's planner is optimal by construction, and `CONTRACTION_INSUFFICIENT__RESIDUAL_CLAIM_STILL_OVERSTATED`, reachable because no naturalistic cell has been run and three of seven families are unexecuted.
- **G6 — Blindness declared lost, not satisfied.** §2 stands as the record. S12 is the replacement device and is not equivalent.
- **G7 — Adjudication.** No vote count selects a terminal; arguments are synthesized by concern class, as in V3 §15, with the classes extended by *null too weak*, *comparison unfair by construction*, *deliverable misnamed* and *unmeasured requirement*. Disagreement between reviewers is retained, never averaged.

## 7. Reviewer lenses required

Four, one answer minimum each. Criteria, the re-weighting of the three existing lenses and the reason the fourth is new are in `FLAGSHIP_DEMARCATION_REVIEWER_SELECTION_V2.md`. **No reviewer selected under V1 carries across automatically**: that shortlist was built to find who could subsume a field claim, which is a different question from whether this standard adds to an existing one.

```text
L1  formal / computational epistemology, philosophy of science, social epistemology   (supporting)
L2  AI for science, agentic and autonomous science, scientific ML                     (retained)
L3  standards, provenance, assurance cases, IV&V, formal methods, contract-based design (primary)
L4  benchmark validity and empirical evaluation methodology                           (new, required)
```

## 8. Independence declaration

As V3 §14, with three changes. Exposure to the four outcome receipts is **no longer disqualifying** and is recorded for interpretation only. Authorship or co-authorship of any standard named as a comparator in S2 is a **qualification**, disclosed, not a conflict. Retained unchanged: no contribution to the framework, manuscript, repositories or study designs; no material shared model, data, tool or adjudication process with another panel member; no current co-authorship, supervision or same-group relation across the panel; citation in the bibliography disclosed. Independence is not inferred from the number of names.

## Packet terminal

```text
CANONICAL_MANUSCRIPT = FLAGSHIP_V23_CONTRACTED
MANUSCRIPT_SHA256 = 3a8805f696329261cef075fdf493197dab4febbe21fc9c84547f40e71a47d3ed
PACKET_VERSION = V4_POST_OUTCOME__CLAIM_RESCOPED
SUPERSEDES = PACKET_V3_V21 + ME_X_SERIES_ADDENDUM (for new reviewers; neither rewritten)
QUESTIONS_S1_S13 = FROZEN_2026_09_03
QUESTIONS_D1_D19 = FROZEN_AND_UNMODIFIED__SCOPED_TO_THE_WITHDRAWN_CLAIM
PRIMARY_TERMINALS = 10 (3 of them adverse to the authors' own negative)
SECONDARY_TERMINALS = the 7 field terminals, retained, withdrawn-claim scope only
OUTCOME_BLINDNESS = LOST_PERMANENTLY__REPLACED_BY_S12_PRECOMMITMENT
LENSES_REQUIRED = 4 (L4 new)
PANEL_SELECTED = NONE
ANSWERS_ON_FILE = 0
FIELD_STATUS = WITHDRAWN_BY_THE_AUTHORS
GATE_STATE = OPEN__RESCOPED
GATE_PASSED = FALSE
AUTHORITY = NONE
```
