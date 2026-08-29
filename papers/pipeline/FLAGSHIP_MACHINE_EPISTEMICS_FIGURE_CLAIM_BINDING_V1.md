# Machine Epistemics Flagship — Figure Claim Binding V1 (Stages 1+2)

**Inputs:** `/tmp/figplan.md` (frozen plan, authoritative), `/tmp/flagship_v8.md` (manuscript, 73 refs, 6 audit corrections already applied), `/tmp/genealogy.md` (parent genealogy ledger), `/tmp/FLAGSHIP_SENTENCE_LEVEL_CITATION_AUDIT_V1.md` (53-ref identity audit, 2026-08-29).

**Rule enforced:** no unpublished ORION-V2 result appears as a quantitative figure element. Every quantitative-looking token in the rendered figures is a *definition of a measurable quantity* (a name, never a value); every factual row/anchor traces to a published reference that is VERIFIED in the citation audit or in the V8 live-web pass (receipt `FLAGSHIP_CITATION_VERIFICATION_RECEIPT_V1.md`, refs 1–9, 21, 37, 54, 59–65, 67, 68, 71–73). Elements the figplan itself declares conceptual ("conceptual known-answer distinction", "prospective methodological/falsification schematic") are bound as CONCEPTUAL_ONLY.

**Disclaimer markers (Stage 2 rule).** † = row's canonical source received a WRONG verdict or an UNVERIFIED detail in the audit (correction applied to the manuscript or detail explicitly unpinned); † rows appear in Figure 2 / Table 1 only with the footnote. ‡ = MINOR_FIX applied (recorded, no disclaimer mandated).

---

## Figure 1 — Scientific-state transitions in an executable research episode

| # | Visual element | Atomic claim text | Claim ID | Evidence basis | Status |
|---|----------------|-------------------|----------|----------------|--------|
| 1 | Main episode band (problem/criterion contract + plural initial state → admissible actions → outputs → typed interpretation/transition gate → updated state + reopened obligations) | AI/hybrid research processes increasingly consist of persistent sequences of search, computation, experiment, interpretation and revision | ME-FIG1-persistent-sequences | Published autonomous-research systems: refs [2] Lu et al., Nature 651 (2026); [3] Ghareeb et al., Nature (2026); [4] Boiko et al., Nature 624 (2023); [5] Szymanski et al., Nature 624 (2023) — all live-web verified in the V8 citation pass | BOUND |
| 2 | Same band — separation of "Outputs" node from "Updated scientific state" node | Execution output and scientific-state transition are distinct objects | ME-FIG1-output-vs-state | Conceptual known-answer distinction (figplan); consistent with manuscript §"failures of scientific-state transition" | CONCEPTUAL_ONLY |
| 3 | Gate drawn as a typed decision point (what changed / warrant / reopen) with two consequence exits | The same execution can produce different scientific consequences under different evidence, semantic or authority conditions | ME-FIG1-conditional-consequence | Conceptual known-answer distinction (figplan) | CONCEPTUAL_ONLY |
| 4 | Gate label "what changed: subject · problem · criterion · source · evidence · representation · evaluator · authority" | A scientific transition must state what changed; silent mutation cannot inherit the old decision | ME-FIG1-gate-typing | Manuscript constraint "Bind the identity of the transition"; local precedent published: belief revision/TMS [11] Doyle AIJ 12 (VERIFIED web), [12] de Kleer AIJ 28 (MINOR_FIX applied ‡), [13] AGM JSL 50 (WRONG→corrected †) | BOUND (schema; local precedent published) |
| 5 | Right-hand "reopened obligations / history" panel | When a warrant root fails, only commitments without surviving valid support reopen | ME-FIG1-selective-reopening | Manuscript "Reopen selectively"; published anchors [11,12] TMS/AGM, [34] Mayo severe testing (VERIFIED canonical), [38] assurance cases (UNVERIFIED detail †) | BOUND (schema; anchors published) |
| 6 | Hostile example 1 — execution succeeds, evidence link invalid (✗ marker) | A retrieval system returns genuine papers but binds a claim to the wrong passage | ME-FIG1-ex1-evidence-link | Conceptual known-answer distinction (figplan: "not claimed empirical prevalence estimates") | CONCEPTUAL_ONLY |
| 7 | Hostile example 2 — provenance/replay exact, scientific analysis wrong | Provenance and reproducibility reveal lineage but do not establish scientific correctness | ME-FIG1-ex2-provenance | [35] Moreau & Groth PROV (VERIFIED web); [36] Stodden et al. (VERIFIED canonical); [54] MacKnight et al. Nat. Comput. Sci. (V8 web pass); contested-claim terrain [6] Standaert Nature News | BOUND |
| 8 | Hostile example 3 — three agreeing validators share a hidden source | Dependent confirmations cannot become independent through reviewer or agent count | ME-FIG1-ex3-shared-source | [37] Hedges, Tipton & Johnson JEBS 35 (V8 web pass); agreement ≠ application truth [40] Lamport et al. TOPLAS 4, [41] FLP JACM 32 (both VERIFIED web) | BOUND |
| 9 | Hostile example 4 — local search flat but a route is censored | Closure is relative to a declared search universe; censored routes can invalidate terminal claims | ME-FIG1-ex4-censored-route | [65] van de Schoot et al., ASReview, Nat. Mach. Intell. 3 (2021) (V8 web pass); route-level stopping owns censoring for one route class | BOUND |
| 10 | Bottom contrast strip: plain workflow arrow terminating in "output" vs episode with gate + obligations | A generic workflow arrow ends in output; the episode inserts a scientifically typed interpretation/transition gate and obligations/reopening after the action | ME-FIG1-workflow-discriminator | Conceptual known-answer distinction (figplan visual discriminator) | CONCEPTUAL_ONLY |

No quantitative element appears in Figure 1. UNBOUND elements: none.

---

## Figure 2 — Parent ownership and the composition gap (matrix)

Legend of cell marks (all symbol-encoded, grayscale-safe): ● = native core ownership (solid dark); ◑ = partial/contributing ownership (hatched); blank = not a native object; ◆ = candidate composition gap (open diamond) with the standing note "parent composition may suffice".

Column headers are decision categories, numbered C1–C11: C1 reliable learning & identifiability · C2 action & experiment selection · C3 belief dependency & revision · C4 diagnosis & discrimination · C5 exact/approximate relation & transport · C6 measurement & linking · C7 provenance & replay · C8 evidence combination · C9 evaluator response · C10 institutional/normative authority · C11 end-to-end scientific automation.

### Row bindings (18 rows; all "parent field owns column natively" claims)

| Row | Parent field (public label) | Claim ID | ● cells | ◑ cells | Canonical source(s) | Audit verdict → marker |
|---|---|---|---|---|---|---|
| 1 | Formal learning & computational epistemology | ME-FIG2-r1-ownership | C1 | C4 | [10] Kelly, *The Logic of Reliable Inquiry* (OUP 1996) | VERIFIED (canonical) — none |
| 2 | Cybernetics, control & resilience engineering | ME-FIG2-r2-ownership | — | C2, C4 | [18] Wiener *Cybernetics* 1948; [19] Ashby 1956; [20] Hollnagel et al. 2006 | all VERIFIED (canonical; ref 18 optional "(Wiley, 1948)" note) — none |
| 3 | Metareasoning, experimental design & active learning | ME-FIG2-r3-ownership | C2 | — | [15] Russell & Wefald (book + AIJ 49) †; [16] Chaloner & Verdinelli Stat. Sci. 10; [17] Settles TR 1648 | [16],[17] VERIFIED (web); [15] WRONG (phantom title)→**correction applied** → † |
| 4 | Belief revision, truth maintenance & model-based diagnosis | ME-FIG2-r4-ownership | C3, C4 | — | [11] Doyle AIJ 12; [12] de Kleer AIJ 28 ‡; [13] AGM †; [14] Reiter AIJ 32 | [11],[14] VERIFIED (web); [12] MINOR_FIX applied → ‡; [13] WRONG→**corrected** → † |
| 5 | Formal abstraction & behavioural equivalence | ME-FIG2-r5-ownership | C5 | — | [24] Cousot & Cousot POPL 1977; [25] Milner *Comm. & Concurrency* 1989 | both VERIFIED (canonical) — none |
| 6 | Causal transportability & measurement invariance | ME-FIG2-r6-ownership | C5, C6 | — | [21] Bareinboim & Pearl JAIR 56 (V8 web pass); [22] Meredith Psychometrika 58 | [22] VERIFIED (web); [21] verified V8 pass — none |
| 7 | Metrology & traceability | ME-FIG2-r7-ownership | C6 | — | [23] JCGM VIM 3rd edn JCGM 200:2012 | VERIFIED (canonical) — none; ledger metrology warning preserved (traceability ≠ fitness) |
| 8 | Statistical workflow & calibration | ME-FIG2-r8-ownership | C9 | C4, C8 | [27] Gelman et al. arXiv:2011.01808; [28] Gelman, Meng & Stern Stat. Sin. 6; [29] Talts et al. SBC ‡ | [27],[28] VERIFIED (web); [29] MINOR_FIX (arXiv 1804.06788) applied → ‡ |
| 9 | Software testing & oracles | ME-FIG2-r9-ownership | C4, C9 | — | [32] Barr et al. IEEE TSE 41; [33] Chen et al. metamorphic review † | [32] VERIFIED (web); [33] WRONG→**corrected** (ACM Comput. Surv. 51(1), 2018) → † |
| 10 | Numerical analysis & validated computation | ME-FIG2-r10-ownership | — | C4, C5 | [30] Higham SIAM 2002; [31] Moore *Interval Analysis* 1966 | both VERIFIED (canonical) — none |
| 11 | Provenance & reproducibility | ME-FIG2-r11-ownership | C7 | — | [35] Moreau & Groth 2013; [36] Stodden et al. 2014; [54] MacKnight et al. 2026 | [35] VERIFIED (web); [36] VERIFIED (canonical); [54] V8 web pass — none |
| 12 | Dependent evidence synthesis & severe testing | ME-FIG2-r12-ownership | C8, C9 | — | [34] Mayo 1996; [37] Hedges, Tipton & Johnson JEBS 35 (2010) | [34] VERIFIED (canonical); [37] V8 web pass — none |
| 13 | Assurance cases, argumentation & distributed consensus | ME-FIG2-r13-ownership | C8 | C9, C10 | [38] Kelly PhD thesis York †; [39] Dung AIJ 77; [40] Lamport et al. TOPLAS 4; [41] Fischer, Lynch & Paterson JACM 32 | [39],[40],[41] VERIFIED (web); [38] UNVERIFIED detail (title variant/year unpinned) → † |
| 14 | Social epistemology & philosophy of inquiry | ME-FIG2-r14-ownership | C10 | C3, C8 | [42] Dewey; [43] Peirce; [49] Goldman; [50] Coady (+ [44–48]) | [43] VERIFIED (web); [42],[44–50] VERIFIED (canonical) — none |
| 15 | Sociology of science & Indigenous data governance | ME-FIG2-r15-ownership | C10 | C6 | [51] Knorr Cetina 1999; [52] Kukutai & Taylor 2016; [53] Carroll et al. CARE 2020; [7] FAIR | [51],[52],[53],[7] all VERIFIED — none |
| 16 | Systematic review, metascience & performative evaluation | ME-FIG2-r16-ownership | C9 | C11 | [65] van de Schoot et al. NMI 3 (2021); [66] Fortunato et al. Science 359 (2018); [69] Perdomo et al. ICML PMLR 119 (2020) | [65] V8 web pass; [66],[69] VERIFIED (web) — none |
| 17 | AI for Science & autonomous laboratories | ME-FIG2-r17-ownership | C11 | C2, C7 | [1] Kramer & King survey; [2] Lu et al.; [3] Ghareeb et al.; [4] Boiko et al.; [5] Szymanski et al. | [1]–[5] V8 web pass — none |
| 18 | Epistemic control & spec-driven architectures (2026 convergence) | ME-FIG2-r18-ownership | C10 | C7, C9 | [59] Ratti; [60] Wojarnik; [61] Kim & Park | V8 web pass (Round-04 neighbor absorption, 5/5 verified) — none |

Header claim for the whole matrix: *most component mechanisms are mature parents; the proposed field owns none of the listed columns natively* — ME-FIG2-parents-mature (BOUND; every ● cell above is the published, audited row).

### Composition-gap panel (final column; each entry carries ◆ "parent composition may suffice")

| Gap entry (public label) | Claim ID | Requires rows | Evidence basis | Status |
|---|---|---|---|---|
| provenance → scientific validity | ME-FIG2-gap-provenance-validity | 9, 11, 12, 13 | Gap is a *relation among* published parents ([35,36,54] provenance; [32,34] error-detection adequacy; [38,39] assurance); no parent claims the cross-link | CONCEPTUAL (gap definition; parents BOUND) |
| relation → downstream reuse/reopening | ME-FIG2-gap-relation-reuse | 4, 5, 6 | [11–13] revision/TMS; [24,25] abstraction; [21] transport — each local, none composes transport×reopening | CONCEPTUAL (parents BOUND) |
| evidence → authority-bounded adoption | ME-FIG2-gap-evidence-authority | 12, 14, 15 | [34,37] evidence; [49,50,52,53,7] authority/permission — manuscript: evidence does not manufacture permission [53] | CONCEPTUAL (parents BOUND) |
| route stop → scientific closure | ME-FIG2-gap-route-closure | 4, 16, 18 | [65] route-level stopping owns one route class only; [11–13] reopening; [59–61] epistemic control | CONCEPTUAL (parents BOUND) |
| local repair → search-space escalation | ME-FIG2-gap-repair-escalation | 2, 3, 4 | [11,12] contradiction-driven repair; [14] diagnosis; [15–17] metareasoning/control | CONCEPTUAL (parents BOUND) |

Falsifiability element: every gap entry is drawn with the ◆ symbol plus the standing note "a parent composition may suffice; the field hypothesis contracts if it does" — ME-FIG2-falsifiable-design (CONCEPTUAL_ONLY by figplan design; the figure is built to permit field falsification).

UNBOUND elements: none. Quantitative content: none (no numbers, no effect sizes).

---

## Figure 3 — Four control problems of Machine Epistemics

Markers per element type (shape, not color): ▪ parent method (with ref) · ✗ cross-layer failure example · ◇ measurable research quantity (a *definition*, never a value). Center node: one bounded research episode.

### Quadrant 1 — Observe epistemic state ("What is distinguishable?")

| Element | Atomic claim text | Claim ID | Evidence basis | Status |
|---|---|---|---|---|
| Parent method a | Formal learning studies identifiability, convergence and limits of inquiry | ME-FIG3-q1-limitsofinquiry | [10] Kelly (VERIFIED canonical) | BOUND |
| Parent method b | Model-based diagnosis supplies explanations for discrepancies and discriminating measurements | ME-FIG3-q1-diagnosis | [14] Reiter (VERIFIED web) | BOUND |
| Parent method c | Measurement invariance states when constructs survive group/instrument change | ME-FIG3-q1-invariance | [22] Meredith (VERIFIED web) | BOUND |
| Failure example | Apparent independent agreement is produced through a shared hidden source | ME-FIG3-q1-failure-sharedsource | [37] Hedges et al. dependence (V8 web pass); [40,41] agreement ≠ truth | BOUND |
| Quantity 1 | State/failure distinguishability; minimum probe cost (definition) | ME-FIG3-q1-quantity-distinguishability | figplan candidate quantity list | CONCEPTUAL_ONLY (definition, no value) |
| Quantity 2 | Structural non-identifiability rate (definition) | ME-FIG3-q1-quantity-nonidentifiability | figplan candidate quantity list | CONCEPTUAL_ONLY |

### Quadrant 2 — Control and transport transitions ("What may change, what survives, what reopens?")

| Element | Atomic claim text | Claim ID | Evidence basis | Status |
|---|---|---|---|---|
| Parent method a | Metareasoning values computations and actions for bounded agents | ME-FIG3-q2-metareasoning | [15] Russell & Wefald † (WRONG→corrected); [16,17] (VERIFIED web) | BOUND († footnote) |
| Parent method b | Causal transportability gives formal conditions for transporting effects across contexts | ME-FIG3-q2-transport | [21] Bareinboim & Pearl (V8 web pass) | BOUND |
| Parent method c | Abstract interpretation supplies sound relations among representations with computable recovery | ME-FIG3-q2-abstraction | [24] Cousot & Cousot (VERIFIED canonical); [25] Milner | BOUND |
| Failure example | An approximate transport silently inherits a decision that was warranted only for the exact relation | ME-FIG3-q2-failure-silenttransport | Manuscript constraint; published anchors [21,24] | BOUND (conceptual instance of published distinctions) |
| Quantity 1 | False/unsafe transport rate (definition) | ME-FIG3-q2-quantity-unsafetransport | figplan candidate quantity list | CONCEPTUAL_ONLY |
| Quantity 2 | Reopened-obligation precision (definition) | ME-FIG3-q2-quantity-reopenprecision | figplan candidate quantity list | CONCEPTUAL_ONLY |

### Quadrant 3 — Assure evidence and authority ("Which support is independent; which evaluator remains valid?")

| Element | Atomic claim text | Claim ID | Evidence basis | Status |
|---|---|---|---|---|
| Parent method a | Severe testing asks whether a method could have exposed the error a claim denies | ME-FIG3-q3-severetesting | [34] Mayo (VERIFIED canonical) | BOUND |
| Parent method b | The oracle problem classifies what classes of error a check can and cannot reveal | ME-FIG3-q3-oracles | [32] Barr et al. (VERIFIED web); [33] Chen et al. † (WRONG→corrected) | BOUND († footnote) |
| Parent method c | Argumentation/assurance frameworks connect claims, premises, evidence, attacks and defeaters | ME-FIG3-q3-assurance | [38] † UNVERIFIED detail; [39] Dung (VERIFIED web) | BOUND († footnote) |
| Failure example | Multiple evaluators reach consensus on a reproducible but scientifically wrong computation | ME-FIG3-q3-failure-consensuswrong | [35,36] reproducible ≠ correct (VERIFIED); [40,41] consensus ≠ truth (VERIFIED) | BOUND |
| Quantity 1 | Support calibration under dependence (definition) | ME-FIG3-q3-quantity-calibration | figplan candidate quantity list | CONCEPTUAL_ONLY |
| Quantity 2 | Evaluator false-pass rate (definition) | ME-FIG3-q3-quantity-falsepass | figplan candidate quantity list | CONCEPTUAL_ONLY |

### Quadrant 4 — Govern escalation and closure ("Repair, escalate, or stop — on what evidence?")

| Element | Atomic claim text | Claim ID | Evidence basis | Status |
|---|---|---|---|---|
| Parent method a | Truth maintenance / belief revision owns contradiction-driven local repair and selective reopening | ME-FIG3-q4-reopening | [11] Doyle (VERIFIED); [12] de Kleer ‡; [13] AGM † | BOUND (†/‡ footnote) |
| Parent method b | Route-level stopping research owns censoring-aware stopping for one route class | ME-FIG3-q4-routestopping | [65] van de Schoot et al. (V8 web pass) | BOUND |
| Parent method c | Metascience empirically studies discovery and evaluation systems | ME-FIG3-q4-metascience | [66] Fortunato et al. (VERIFIED web) | BOUND |
| Failure example | Closure is declared while a search route is censored | ME-FIG3-q4-failure-falseclosure | Manuscript "Close only relative to a declared universe"; [65] | BOUND (conceptual instance) |
| Quantity 1 | False closure rate under censored routes (definition) | ME-FIG3-q4-quantity-falseclosure | figplan candidate quantity list | CONCEPTUAL_ONLY |
| Quantity 2 | Unnecessary refusal / over-conservatism rate (definition) | ME-FIG3-q4-quantity-overconservatism | figplan candidate quantity list | CONCEPTUAL_ONLY |

Cross-figure claim: *every problem ties to mature parents AND to an observable scientific decision/failure metric, instantiable without project terminology* — ME-FIG3-public-taxonomy (CONCEPTUAL_ONLY; verified in rendering: no repository terms appear).

UNBOUND elements: none.

---

## Figure 4 — Falsifying the field hypothesis (prospective decision path)

All elements are a **prospective methodological/falsification schematic, not a plot of results** (figplan evidence basis). Public labels only — no foundation-candidate codenames (the manuscript's public terms are "strongest parent federation", "selective interfield theories", "absorptive supertheory", "domain-only federation"; the figure uses the outcome vocabulary below).

| Element | Atomic claim text | Claim ID | Evidence basis | Status |
|---|---|---|---|---|
| Stage 1 — Native parent reconstruction | Each parent is rebuilt in its native representation and its native verdicts preserved before any composition is scored | ME-FIG4-stage1-reconstruction | Manuscript "Parent recovery"; [24] recovery precedent (VERIFIED canonical) | CONCEPTUAL (method step; anchor published) |
| Stage 2 — Strongest information-matched parent composition | Foundations are compared under matched sources, tools, compute, human expertise and evaluator access | ME-FIG4-stage2-matchedcomparison | Manuscript "How the field could be founded—or fail"; genealogy strongest-parent composition falsifier | CONCEPTUAL_ONLY |
| Stage 3 — Protected cross-domain transition cases | Pre-declared cases combine parent problems where the higher theory should be needed — or shown unnecessary | ME-FIG4-stage3-protectedcases | Manuscript protected-cases paragraph (e.g., consensus on reproducible-but-wrong computation [35,40,41]) | CONCEPTUAL (case classes drawn from published distinctions) |
| Stage 4 — Independent evaluation | Adjudication is independent and prospective; retrospective explanations cannot count | ME-FIG4-stage4-independent | Manuscript prospective-generativity; performative-evaluation model [69] (VERIFIED web) | CONCEPTUAL (model published) |
| Outcome A — Stable cross-domain residual → field hypothesis strengthened | A residual surviving the strongest parent composition across domains strengthens the field hypothesis | ME-FIG4-outcome-residual | figplan outcome list | CONCEPTUAL_ONLY |
| Outcome B — Parent tie / parent win → integration engineering | If parents tie or win, the work is integration engineering, not a new science | ME-FIG4-outcome-parentwin | figplan; manuscript "F0 may prove sufficient" | CONCEPTUAL_ONLY |
| Outcome C — Domain-specific only → return to native parents | If effects are domain-specific, the discipline returns to native parents | ME-FIG4-outcome-domainspecific | figplan; manuscript "F3 may be the correct pluralist architecture" | CONCEPTUAL_ONLY |
| Outcome D — Cannot independently adjudicate → field separation unresolved | If no independent adjudication exists, field separation remains unresolved | ME-FIG4-outcome-unresolved | figplan | CONCEPTUAL_ONLY |
| Underpath annotation | Non-compensatory gate: critical failures (false completion, source corruption, unsafe transport, criterion drift, authority violation) cannot be purchased by broader scope or higher average performance | ME-FIG4-noncompensatory-gate | Manuscript "Theory dominance" partial order | CONCEPTUAL_ONLY |

UNBOUND elements: none. Quantitative content: none.

---

## Table 1 — What Machine Epistemics does not rename (Stage 2 per-row citation verdicts)

Columns per figplan: Parent field | Native object/problem | Canonical source(s) | Already owned operation | Candidate ME interface/residual | Field-falsifier consequence. The rendered table text follows the manuscript's parent paragraphs; this section records the citation-entailment verdict for every canonical source the table cites. Marker rule: any row citing a WRONG- or UNVERIFIED-audit source carries † and keeps it in the published table footnote; MINOR_FIX rows carry ‡ (recorded).

| # | Parent field row | Canonical source(s) cited in row | Audit verdict | Marker |
|---|---|---|---|---|
| 1 | Computational epistemology | [10] Kelly 1996 | VERIFIED (canonical) | none |
| 2 | Machine epistemology (prior art) | [63] Wheeler, Routledge Companion ch. 38 (2017) | V8 live-web pass | none |
| 3 | Epistemic engineering / distributed cognition | [62] Cowley & Gahrn-Andersen Front. AI 5 (2023); [47] Hutchins | [62] V8 web pass; [47] VERIFIED (canonical) | none |
| 4 | Cybernetics / control / resilience | [18] Wiener; [19] Ashby; [20] Hollnagel et al. | all VERIFIED (canonical; ref 18 optional publisher note) | none |
| 5 | Rational metareasoning | [15] Russell & Wefald | WRONG (phantom title)→corrected in V8 refs | **†** |
| 6 | Bayesian experimental design / active learning | [16] Chaloner & Verdinelli; [17] Settles | both VERIFIED (web) | none |
| 7 | Truth maintenance / belief revision | [11] Doyle; [12] de Kleer; [13] AGM | [11] VERIFIED; [12] MINOR_FIX applied; [13] WRONG→corrected | **†** (13) ‡ (12) |
| 8 | Model-based diagnosis | [14] Reiter | VERIFIED (web) | none |
| 9 | Formal methods / abstraction | [24] Cousot & Cousot; [25] Milner | both VERIFIED (canonical) | none |
| 10 | Causal transportability | [21] Bareinboim & Pearl | V8 web pass | none |
| 11 | Metrology / psychometrics | [23] JCGM VIM; [22] Meredith | VERIFIED (canonical) / VERIFIED (web) | none |
| 12 | Provenance / workflows | [35] Moreau & Groth; [36] Stodden et al.; [54] MacKnight et al. | VERIFIED (web) / VERIFIED (canonical) / V8 web pass | none |
| 13 | Dependent evidence synthesis | [37] Hedges, Tipton & Johnson | V8 web pass | none |
| 14 | Performative / strategic evaluation | [69] Perdomo et al. | VERIFIED (web) | none |
| 15 | Metascience / science of science | [66] Fortunato et al. | VERIFIED (web) | none |
| 16 | Philosophy / social epistemology | [42–50] (Dewey, Peirce, Ryle, Polanyi, Suchman, Hutchins, Flavell, Goldman, Coady) | [43] VERIFIED (web); rest VERIFIED (canonical) | none |
| 17 | AI for Science / agentic / autonomous science | [1] Kramer & King; [2–5] Lu, Ghareeb, Boiko, Szymanski et al. | V8 web pass | none |

**Stage 2 verdict summary:** 4 rows carry † (metareasoning [15]; belief revision [13]; + in Figure 2 also software testing [33] and assurance [38]); 3 canonical sources carry ‡ minor-fix records ([12], [29], [55-unused-in-figures]). All † rows appear in Figure 2 / Table 1 **only with** the disclaimer footnote: "† bibliographic correction applied to this source during the 2026-08-29 citation audit, or one detail remains unpinned (thesis title variant); see manuscript reference list." No WRONG/UNVERIFIED source is drawn as an unmarked "canonical source".

---

## Binding counters

```text
FIG1_ELEMENTS_BOUND = 10          (6 BOUND, 4 CONCEPTUAL_ONLY, 0 UNBOUND)
FIG2_ROWS_BOUND = 18              (18 BOUND; 5 gap entries CONCEPTUAL w/ BOUND parents)
FIG3_ELEMENTS_BOUND = 24          (16 BOUND, 8 CONCEPTUAL_ONLY, 0 UNBOUND)
FIG4_ELEMENTS_BOUND = 10          (all CONCEPTUAL schematic w/ published anchors; 0 UNBOUND)
TABLE1_ROWS_VERDICTED = 17        (13 clean, 3 † rows, overlapping ‡ notes; 0 rows citing an uncorrected WRONG source)
UNBOUND_ELEMENTS_TOTAL = 0
QUANTITATIVE_UNPUBLISHED_ELEMENTS = 0
```

