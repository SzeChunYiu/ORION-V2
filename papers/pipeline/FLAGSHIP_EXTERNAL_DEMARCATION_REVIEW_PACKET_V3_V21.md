# Independent Demarcation Review Packet V3 — Machine Epistemics (bound to manuscript V21)

**Packet date:** 2026-09-02  
**Manuscript binding:** *Machine Epistemics: Toward a Science of AI-Driven Inquiry and Scientific Change*, Perspective V21 (NMI reader-hardened)  
**Manuscript file:** `v2-papers/FLAGSHIP-machine-epistemics/manuscript/public/FLAGSHIP_MACHINE_EPISTEMICS_PERSPECTIVE_V21_NMI_READER_HARDENED.md`  
**Manuscript sha256:** `e6796fbfed8a1b1f1880d8d2cff4fecfd498badc420a806c28ae1a1fe30d83eb`  
**Manuscript source:** repository `SzeChunYiu/ORION-paper`, branch `codex/machine-epistemics-hardening-wave`, commit `f6854d84b45708e4cc5f4aac1628fd1977633dcb` (2026-09-02); figures `figure-1-transition-unit-nmi.svg`, `figure-2-control-escalation-nmi.svg`, `figure-3-atlas-horizon-nmi.svg`  
**Supersedes:** `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V2.md` (sha256 `4e3d7bcd7d4879893c92e09a8c9ddf11772f4ce95176bc4336df2dc9594f4517`, bound to V14) for all new reviewers  
**Review status:** outcome-blind packet. Reviewer questions D1–D12 are reproduced verbatim from V2 and remain frozen; questions D13–D18 are appended in this version and are frozen from this date. No question is reordered, weakened or removed.  
**Purpose:** blinded-as-feasible external assessment of whether the proposed object, scientific residual, field boundary and working label are coherent, useful and nonredundant.

> **POST-OUTCOME ADDENDUM, 2026-09-02 — read this packet with `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V3_RESULT_ADDENDUM_ME_X_SERIES.md`.**
> The three protected studies whose outcomes §10 withheld (ME-X4, ME-X1, ME-X2) have now run, and all three went against the proposal — one of them not as a tie but as a loss. Withholding them would now be the defect rather than the discipline, so they are supplied in that addendum in full terminal form, together with one added question, D19.
> **Everything in this packet below this line is frozen and unrewritten:** questions D1–D18 are reproduced exactly as they were before any outcome existed, §10's withholding language is left standing as the record of what was withheld and when, and no section is reinterpreted or re-scored in the light of the outcomes. You may answer before reading the addendum, after, or both.

This packet deliberately omits repository-development history, internal issue/PR chronology, simulated editor and reviewer outcomes, clean-room internal reads, every protected or development study outcome, and any preferred field terminal. It includes adverse/null evidence that was already bounded and disclosed in V2 and that materially bears on the proposed boundary.

---

## 0. What the reviewer receives, and what is asked

You receive exactly three things: the V21 manuscript (with its three figures), this packet, and the independence declaration in §14. Nothing else from the project is supplied.

Expected effort: 2–3 hours. Please read the manuscript once, answer D1–D18 in writing and independently (before any discussion with other reviewers), and end with exactly one terminal from §12. Answers of the form `CANNOT CHECK` are valid and useful. No answer is preferred.

---

## 1. Proposed object (as stated in V21)

AI and hybrid research systems increasingly participate in extended scientific processes: literature search, model/hypothesis construction, proof or computation, experiment/measurement selection, tool execution, evaluation, revision and scientific output.

The proposed object is **not the AI model or agent alone**, and it is **not the world**. It is the controlled transition from one scientific state to another inside a bounded machine-mediated research episode, made under partial observation of an external target.

V21 states the object in one Box. An external target has state \(\omega_t\); the machine sees it only through an observation channel that depends on a declared context and instrument. The bounded episode state carries the problem and its criterion, plural commitments and alternatives, unresolved obligations, admissible actions, resources, evidence with provenance and dependence, evaluator contracts, accumulated observations, history and an external authority boundary; when decision-relevant it is extended by a generative regime and a bounded atlas. The elementary object is the transition

\[
T_t:(\widetilde E_t, a_t, x_t)\mapsto(\widetilde E_{t+1}, \rho_t),
\]

with a **non-authorizing receipt** \(\rho_t\) recording evidence, obligation and commitment deltas, replay and witness identities, still-active falsification and evaluator conditions, and an authority ceiling. A receipt supports inspection and later revision; it does not make its interpretation true. Receipts are not witnesses. A witness is an independent evidence record able to change the decision at hand.

Working field label:

> **Machine Epistemics** — provisional label for a falsifiable programme that asks when machine-mediated inquiry may change scientific commitments, representations, methods, experiments, evaluators and problems.

The label carries **no naming novelty claim** and **no priority claim**. The earlier tagline "the control science of AI-driven discovery" is not used in V21 as a demarcation claim, because *epistemic control* is explicit prior terminology.

The proposal survives only if that object remains scientifically useful beyond a faithful composition of its strongest parent disciplines. V21 states that parent sufficiency is a successful outcome.

---

## 2. The world is not the machine (correction adopted in V21)

Earlier drafts allowed a reading in which the target of inquiry and the epistemic machine shared one transition structure. V21 rejects that reading and separates four kinds of change that must not be conflated:

1. **Target (ontic) change** — the external system really changed. Not epistemic learning; not evidence that nature computes.
2. **Observation-channel change** — the target may be unchanged while sensing, sampling, calibration or the measurement relation changed or failed.
3. **Epistemic revision** — new evidence, a discovered dependence, an evaluator flaw or a retrieved record changes what the machine should commit to, with the target held fixed.
4. **Generative-regime change** — the machine's representation language, operators, tools or search regime is revised. This is machine self-revision, not a change in the world.

Two non-implications follow from the definitions and are stated in V21 as such, not as results:

```text
successful execution   !=>  warranted scientific transition
machine state changed  !=>  target changed          (and conversely)
```

The framework explicitly does **not** claim that the universe is a machine, that nature computes, that a machine can access target state directly, or that a learned representation becomes identical to reality. Reviewers are asked in D14 whether this separation carries any content beyond the ordinary partial-observation setting, and whether any V21 sentence or figure still slips.

---

## 3. Relationship to neighboring machine-X concepts

V21 uses the following operational taxonomy (its Table 1) to avoid a false superiority ladder. Reviewers should challenge it if the distinctions are misleading or already standard under clearer terminology.

| Object | Role in V21 | Central question |
|---|---|---|
| Machine learning | update mechanism | How does a system update from data or feedback? |
| Reasoning, planning and cognition | processing organization | How does it represent, derive, search, remember and choose? |
| Machine intelligence | context-relative capability | What can it do under a declared ecology of tasks and resources? |
| Machine scientific intelligence | science-scoped capability | How capable is it at producing progress on scientific tasks? |
| Machine Epistemics | scientific-transition control | When is a change in scientific state warranted, transportable, replayable and revisable? |
| AI for Science | application ecosystem | How are AI methods and integrated systems deployed in research? |

V21 states that Machine Epistemics "is higher-order only in responsibility for scientific change; it is not a ranking above learning or intelligence and does not require a monolithic controller". The proposal explicitly rejects

```text
Machine Learning < Machine Intelligence < Machine Epistemics
```

as a total order. `governs a scientific transition` does not mean `is more intelligent than`.

---

## 4. Direct parent boundary

### 4.1 Epistemology parents

The proposal does **not** claim to invent executable or mathematical epistemology. Direct parents include mainstream epistemology; formal epistemology; formal learning / computational epistemology (reliable inquiry, learnability, convergence under stated assumptions); social epistemology; philosophy of science and metascience; and AI epistemology / epistemic agency and responsibility.

Formal learning theory is an especially strong parent: it already provides a mathematical normative theory of reliable inquiry. A reviewer may therefore conclude that the proposed object is a subproblem, engineering layer or federation of existing epistemology/control traditions rather than a distinct field.

### 4.2 Component parents named in V21

Formal learning; truth maintenance and belief revision (JTMS/ATMS, AGM); rational metareasoning and Bayesian experimental design / active learning; causal transport; metrology; abstraction and refinement; provenance; severe testing and argumentation; decision theory's inference/decision separation; POMDP belief state; comparison of experiments; independent verification and validation and assurance cases; structure mapping; interfield theory.

### 4.3 Contemporary parents that narrow the boundary further (2026)

V21 concedes all of the following as parent-owned and cites them: epistemic control in ML-based science and in LLM-assisted research evaluation; spec-driven architectures of epistemic control for empirical research; provenance-first, re-openable records for autonomous science; typed scientific execution graphs that encode admissible state transitions and provenance; model-discovery agents that detect hypothesis-class inadequacy, expand model families and choose informative experiments; self-revising discovery systems that formalize verified representational-regime transitions; workflow-level research automation foregrounding evidence preservation, validation and accountable closure; the long-established automated-scientific-discovery lineage; and the demonstration that formal validity can coexist with semantic drift of the specification.

Consequently the following are **not** claimed as novelties: scientific-state-transition language; provenance and reopenability; verification/admissibility gates on workflow state; model-family inadequacy triggering hypothesis expansion; representational-regime change with preservation obligations; epistemic control as the central concern of AI-mediated science.

The candidate residual, if any, is narrower:

> **system-level control of versioned machine-mediated scientific transitions where mutable state includes not only belief/credence but evidence lineage, representations, models, tools, experiments, problems, evaluators, resources, generative regimes and authority boundaries — and, more narrowly still, whatever changes a pre-registered decision when parent modules exchange structure rather than verdicts (see §7).**

---

## 5. Four competing foundations

Please assess these as real competitors rather than treating F2 as the preferred answer.

### F0 — strongest parent federation

Mature methods remain native: formal learning governs reliable inquiry; causal inference causal claims; measurement science comparability; metareasoning action choice; truth maintenance/revision commitment change; provenance lineage; formal methods abstraction/refinement; scientific methodology and domain science substantive validity. Ordinary engineering interfaces connect them. If F0 makes the same scientific-transition decisions at equal or lower cost, the distinct-field claim should contract.

### F1 — selective interfield (bridge) theories

Only specific interfaces deserve reusable theories — for example execution→evidence, measurement→transport, support→authority or uncertainty→action — without supporting a broad field.

### F2 — absorptive transition theory

Several scientific-transition classes share nontrivial constraints representable in one higher-order transition theory that recovers and defers to parent sciences locally. F2 earns credit only when the higher representation changes a pre-registered scientific decision, preservation/reopening obligation or action choice beyond information-matched parents.

### F3 — plural/domain federation

No stable higher theory exists. Domains remain linked by typed translations, boundary objects and provenance while preserving incompatible native semantics. F3 should win whenever common abstractions erase distinctions that matter scientifically.

V21 adds: a higher layer that ties a parent while consuming more resources should be withdrawn.

---

## 6. Discrepancy locus and minimum-sufficient escalation (interface adopted in V21)

Before deciding how to revise itself, the system keeps distinct candidate **loci** for a witnessed discrepancy:

```text
TARGET_WORLD | OBSERVATION_MEASUREMENT | EPISTEMIC_MODEL | REPRESENTATION_REGIME |
PROBLEM_CRITERION | EVALUATOR_VALIDATION | PROCESS_TOOL_WORKFLOW | CANNOT_IDENTIFY
```

`CANNOT_IDENTIFY` is first-class whenever the evidence cannot discriminate live hypotheses. V21 presents this as the Duhem–Quine problem of locating error made operational, with severe testing supplying the standard for a discriminating probe, and it claims only the placement of this object inside the transition loop.

Two further commitments:

- **No evaluator self-certification.** If the scientific evaluator is itself a candidate locus, the evaluator used to discriminate locus hypotheses must be logically distinct from it; otherwise the system certifies its own evaluator circularly. V21 places this as continuous with independent verification and validation and assurance-case practice.
- **Two gates in sequence (Figure 2).** Gate 1: does a registered direct or parent-native action resolve the discrepancy without any higher-level change? Only if not, Gate 2: is a higher-level change *eligible*, which requires on record a witnessed blocker, a prospective discriminator (declared before its outcome) and a lower-level disposition. Eligibility is not adoption. Withdrawal of an escalation is a valid outcome.

The category-error interventions this is meant to prevent: sensor drift triggering theory revision; model failure misread as target change; a wrong specification prompting representation search; a blind evaluator mistaken for success or failure; ordinary search insufficiency triggering an unnecessary new regime.

The locus family is **not** claimed as a universal ontology. Native-domain review may merge, split or reject a locus; its value must come from better intervention decisions, not taxonomy. Reviewers are asked in D15 whether this interface is anything more than model-based diagnosis, metareasoning and IV&V renamed.

---

## 7. The residual as V21 states it: the interface-information hypothesis

V21 replaces the earlier "the residual, if any, lies in the decisions across transitions" with a specific registered hypothesis, argued through the running example (three studies supporting \(H\); two share a dataset; the third rests on a contested calibration):

- Let the parent disciplines run as a federation whose modules exchange **verdicts only**. Provenance reports shared ancestry; measurement reports contested calibration. Neither verdict is bound to the identities of the support routes registered for \(H\). Belief revision, receiving them separately, finds one route still standing, preserves \(H\), and experimental design keeps the planned experiment.
- Let the modules exchange **structure** (dependence ancestry; calibration dependency). Under the registered dependence rule the two defects jointly defeat every registered route; \(H\) is reopened and the experiment reconsidered.

V21 is explicit that "nothing in this walk-through is a result; both federations are easy to build, and the difference lies entirely in what crosses the module boundary."

The **registered interface-information hypothesis** is that this residual changes pre-registered decisions as exchange is enriched along the ladder

```text
verdict only -> + provenance -> + dependence ancestry -> + typed transport status -> full structure
```

and the prediction is registered **both ways**:

- (a) the advantage vanishes at full-structure exchange — **parent sufficiency at the interface level**. Machine Epistemics then narrows to an **interface standard** for what parent modules must exchange, a successful outcome that keeps the interface and drops the field;
- (b) the advantage persists — a genuine **control** residual.

A flat or non-monotone ladder, or an advantage that depends on information the federation cannot be given at any rung, falsifies the hypothesis as stated.

This is the framing reviewers are asked to attack in D13: is the entire defensible residual an interface standard rather than control, and would (a) still justify any field-level vocabulary?

---

## 8. Frontier, invention, atlas and horizon (retained hardenings)

### 8.1 Frontier obstruction / minimum sufficient action

A frontier problem may be difficult because the **kind of missing object** is unknown. Candidate principle: diagnose the witnessed obstruction and choose a minimum sufficient action rather than defaulting to more reasoning or novelty generation. Strongest parent threats: metareasoning, active experiment design, diagnosis, CEGAR/CEGIS-style refinement, and modern adaptive scientific and model-discovery agents.

### 8.2 Generative regime / invention

A generative regime records the current representation language, generative rules, operators, constraints and tools within which candidates are produced; an invention proposal replaces it by a successor regime. Verified representational-regime transition with predecessor transport is already formalized by contemporary work; creativity and open-ended search own generative exploration. The candidate residual is only whether evidence, preservation, evaluator, locus and authority conditions correctly decide when such a change may alter scientific commitments.

### 8.3 Atlas / horizon

Observed contexts and practices are treated as local samples, not as observations of a complete global space. The atlas records represented and tested contexts, typed maps and registered overlaps, not the external target. Central non-implication:

```text
pairwise compatibility  !=>  a global section has been witnessed
```

Compatible overlaps without a separate global witness form a matching family only; incompatible overlaps are obstructions; a missing correspondence is unresolved. Sheaf-theoretic sensor integration and contextuality are named as direct parents. A new probe expands the **horizon** only when it strictly refines the decision-relevant observational partition of the candidate family — presented as a bounded form of the comparison of experiments and of distinguishability in formal learning theory. There is no empirical `ABSOLUTE_GLOBAL` terminal.

---

## 9. Epistemic locality and diverse adaptive systems; bounded evidence already disclosed

Competence is treated as context-relative to a declared ecology. The programme enforces

```text
COGNITION != COLLECTIVE/CULTURAL ADAPTATION != EVOLUTIONARY ADAPTATION != MACHINE ADAPTATION
FITNESS != TRUTH
SURVIVAL != NORMATIVE AUTHORITY
```

**EL10 (disclosed in V2; retained).** An exact 48-task locality benchmark compared a context-free global ranking, strongest parent federation, current integrated control and an explicit locality-interface arm. Context-free global ranking failed strongly; strongest parent/current integrated controls already eliminated false universalization on the critical cases; the explicit locality interface produced no statistically protected improvement over F0/F2 and added wrapper cost; the dedicated runtime locality object contracted to a documentation/analysis convention. This is **parent-sufficiency/null evidence**, not evidence for F2.

**EL20 (disclosed in V2; retained).** A source-bound audit reconstructed six adaptive-system donor families with native mechanisms, boundaries, timescales, retention channels, transfer conditions and explicit anti-analogy cases; unsourceable claims were left `CANNOT_SOURCE/CANNOT_CHECK`. This supports category-error discipline and genealogy only.

**AH10 (disclosed in V2; retained).** Reference atlas/horizon semantics passed exact tests: compatible overlaps without a global witness → matching family only; incompatible overlaps → obstruction; explicit separate witness required for global coherence; a new probe may strictly refine a partition; no empirical `ABSOLUTE_GLOBAL` terminal. This establishes implementation fidelity of the reference semantics only.

---

## 10. Pre-registered studies that exist — outcomes withheld

The following study designs exist and are frozen. **Their outcomes, where any exist, are withheld from this packet**, so that the judgement requested here is a pre-outcome judgement. Reviewers who have seen any of them must say so in §14.

| Study | What it is | Status disclosed here |
|---|---|---|
| AH20 | prospective atlas/horizon benchmark, 78 tasks, five arms, including a strongest local-to-global/experiment-design parent control and an explicit atlas/horizon interface arm | frozen and executed; result addenda to the V2 packet exist and are **not supplied**; V2's pre-outcome questions remain frozen |
| AH30 | naturalistic atlas/horizon transfer | gated; not authorized by default |
| ME-X1 | cross-transition coupling benchmark: ten known-answer case families (claim/problem identity mismatch; calibration break; hidden evidence dependence; invalid transport; defeated support family; evaluator blindness; authority mismatch; proof of the wrong specification; local compatibility with global obstruction; fully warranted transition), finite registered action set, baseline hierarchy up to the strongest faithful federation | protocol frozen; prospective; development fixtures exist and are **not supplied** |
| ME-X4 | selective reopening under dynamic evidence: exact-oracle, zero-model-call, deterministic known-answer study against a JTMS/ATMS, belief-revision, provenance, dependence-aware synthesis, typed-transport and assurance-update federation; carries the §7 interface-information ladder as a pre-registered secondary axis with its own gate and a finite separation example | design frozen; parent-fidelity receipt exists; development split exists; **development analysis and results are withheld**; protected stage not run at packet date |
| H-EXT-1 | conditional activation of epistemic-control machinery through a cheap, input-computable, channel-external gate, tested for Pareto dominance over always-on and always-off arms and a strongest assurance-federation reference, with a shuffle-equal-n gate null | design frozen before any gated evaluation; **no numbers, strata, or arm results are supplied** |
| H-EXT-2, H-EXT-3, H-EXT-4 | extension hypotheses register: internal-salience Goodhart replication; the interface-information residual (§7); a quantitative prospective-revision bound | S1/S2 hypotheses only; no results |
| ME-X2, ME-X3, ME-X5, ME-X6, ME-X7 | locus + minimum escalation; formal mathematics (Lean) representation change; cross-domain residual; collective epistemics as noisy channel; external witness sufficiency | protocols at synthesis level; no protected outcomes |

Two disclosures about the ME-X4 design that are part of its pre-registration, not outcomes: (i) the design records its own **pre-registered expectation**, namely that on acyclic registered support graphs the parent federation and the coupled controller compute the same semantics once typed information crosses the module boundary, so that the expected route is parent sufficiency with the ladder terminal `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`; (ii) the decisive content is whether any generated stratum breaks that expectation, where single parents break, the ladder, and cost. Reviewers should treat (i) as an author prior, not as evidence in either direction.

**Explicitly withheld from this packet (not to be inferred from anything above):** AH20 R1/R2 outcomes and terminals; H-EXT-1 gate numbers, strata and frontier results; ME-X4 development analysis and results; ME-X1/ME-X2 development fixture outcomes; all P-D, PC, E-series, SD and PRA outcomes; the simulated review rounds; the internal clean-room read and its verdicts; issue and PR chronology.

---

## 11. Candidate transition constraints (V21 Table 2)

These are proposed as falsifiable hypotheses, not laws. Each row carries its own parent-sufficiency falsifier in V21.

| Candidate constraint | Operational content | Parent-sufficiency falsifier |
|---|---|---|
| Identity and criterion conservation | a changed problem, criterion, source, representation or evaluator does not silently inherit the old conclusion | native bookkeeping prevents all pre-registered errors |
| Ontic and epistemic responsibility separation | target, observation, model, representation, problem, evaluator and process remain distinct until discriminated | diagnosis and metareasoning parents make the same decisions |
| No evaluator self-certification | a scientific evaluator under diagnosis cannot certify its own adequacy | parent validation already guarantees the distinction |
| Execution and evidence separation | successful execution is not support without a bound evidence interpretation | execution status alone is sufficient in pre-registered cases |
| Non-amplifying authority | inference and evidence cannot create authority above registered roots | parent governance handles every decision |
| Typed transport | relation kind, loss, uncertainty and dependence remain explicit | native transport and measurement theory match decisions |
| Selective reopening | only commitments whose sufficient support fails are reopened | truth-maintenance and domain dependency handling are sufficient |
| Bounded closure | unresolvedness is valid under declared evaluators, resources and candidate class | a simpler parent matches closure decisions |

A reviewer should identify which are already fully parent-owned, which are useful interface principles and which — if any — form a nontrivial common scientific object. V21 binds its wager most tightly to the selective-reopening and typed-transport rows through the running example; the other rows are candidate constraints.

---

## 12. Strongest field falsifier and allowed terminals

The distinct-field hypothesis should contract if an information- and resource-matched composition of mature parents makes the same pre-registered scientific-transition decisions across materially different domains without a nontrivial residual.

Specific contraction triggers include:

- locality/atlas/frontier/locus interfaces add no decision value beyond current context conditioning, identifiability, experiment design, diagnosis or metareasoning;
- the interface-information ladder is flat, non-monotone, or the advantage vanishes at full-structure exchange (§7, branch (a));
- the common abstraction disappears when native domain semantics are restored;
- purported cross-domain recurrence is vocabulary-level only;
- measured benefit is logging/provenance overhead rather than scientific decision quality;
- resource cost dominates any gain;
- independent parent-field reviewers cannot articulate a stable object distinct from existing fields;
- the label `Machine Epistemics` predictably denotes a different established object.

### Allowed terminals (the seven frozen by the external-review gate)

Choose exactly one:

```text
CANDIDATE_FIELD_DEMARCATION_SUPPORTED
USEFUL_INTERDISCIPLINARY_RESEARCH_PROGRAMME
INTEGRATION_ENGINEERING_ONLY
SUBFIELD_OF_EXISTING_PARENT
RENAME_SCIENTIFIC_PROGRAMME
FIELD_BOUNDARY_TOO_FRAGMENTED
CANNOT_CHECK_FIELD_SEPARATION
```

If you choose `RENAME_SCIENTIFIC_PROGRAMME`, please qualify it as `RENAME__OBJECT_SURVIVES` (the scientific object is stable but the label should change) or `RENAME_AND_CONTRACT` (the label should change and the object should narrow). Name success and scientific-object success are judged separately. No vote count automatically selects a terminal.

---

## 13. Reviewer questions

### 13.1 Frozen questions D1–D12 (verbatim from packet V2; do not answer with reference to any outcome)

Please answer independently before seeing other reviewers' arguments.

#### D1 — Object coherence

Can you explain the proposed scientific object in your own words without naming ORION or any software implementation?

- `YES, STABLE OBJECT`
- `PARTLY, NEEDS REDEFINITION`
- `NO, TOO HETEROGENEOUS`

Give the narrowest definition you consider defensible.

#### D2 — Strongest parent(s)

Name the strongest 1–3 existing fields/traditions that most nearly subsume the object. Identify omitted work that would materially change the claim.

#### D3 — Epistemology boundary

Does the proposal draw a scientifically meaningful boundary from formal learning/computational epistemology, formal/social epistemology and philosophy of science?

If not, state the parent-owned description you would prefer.

#### D4 — Machine-X taxonomy

Is the distinction among learning mechanism, cognition/architecture, context-relative capability and scientific-transition control useful, misleading or redundant? Does `Machine Epistemics` invite an incorrect superiority interpretation despite the manuscript's caveat?

#### D5 — Composition residual

Is there a plausible scientific residual in cross-parent scientific-transition decisions?

- `PLAUSIBLE RESIDUAL`
- `PARENT COMPOSITION LIKELY SUFFICIENT`
- `CANNOT CHECK`

Name the decisive example/counterexample.

#### D6 — Frontier / invention boundary

Do obstruction-first action routing and warranted possibility-space transformation constitute a useful cross-parent problem, or are they adequately owned by metareasoning, diagnosis, computational creativity/open-endedness and domain-specific methodology?

#### D7 — Locality / diverse-intelligence boundary

Does the locality principle add useful scientific discipline after the EL10 parent-sufficiency result, or is it simply an existing context-conditioning/ecological-rationality principle? Are the donor categories separated strongly enough to avoid anthropomorphism or `evolution = cognition` rhetoric?

#### D8 — Atlas / horizon boundary

Is the atlas/horizon formulation a useful scientific interface for local-to-global inference and unknown representational limits, or an unnecessary renaming of identifiability, model pluralism, formal learning and sheaf/local-to-global parents?

What evidence would justify keeping or deleting this interface?

#### D9 — Field versus integration programme

What is the strongest defensible status **before AH20 outcome disclosure**?

- `CANDIDATE DISTINCT SCIENTIFIC FIELD`
- `USEFUL INTERDISCIPLINARY RESEARCH PROGRAMME`
- `INTEGRATION/ASSURANCE ENGINEERING AREA`
- `SUBFIELD OF EXISTING PARENT`
- `LABEL NOT USEFUL`
- `CANNOT CHECK`

#### D10 — Name interpretation

Without seeing naming history, what does **Machine Epistemics** mean to you? Would another label communicate the actual object more accurately?

#### D11 — Falsifiability and cross-domain burden

What result would make you abandon the distinct-field claim? Name two materially different scientific domains that would provide a convincing cross-domain test—or explain why no such pair can validate the abstraction.

#### D12 — Perspective publication value / omitted literature

Independent of field status, is the demarcation/research agenda sufficiently important and timely for a broad AI-science Perspective?

- `YES`
- `YES AFTER MAJOR NARROWING`
- `SPECIALIST ONLY`
- `NO`

List any omitted contrary literature whose absence would make the Perspective misleading.

---

### 13.2 Questions appended in V3 (frozen 2026-09-02)

These do not modify, reinterpret or re-weight D1–D12. Where an appended question overlaps a frozen one, answer both; the overlap is intentional so that the V21 hardening can be judged against the V2 baseline.

#### D13 — Interface standard versus control (hostile)

Read §7 and the V21 paragraph beginning "Where, then, could anything remain?". Suppose the registered prediction resolves as branch (a): once parent modules exchange full structure (dependence ancestry, calibration dependency, typed transport status), the coupled controller has no advantage.

- Is the entire defensible residual then an **interface standard** — a specification of what parent modules must exchange — rather than a control theory?
- Would branch (a) leave anything that justifies field-level vocabulary, or only a data-exchange convention comparable to a provenance or contract-based-design standard?
- Independently of the ladder outcome, can you construct a case where a *verdict-exchanging* federation is unavoidable (structure cannot be exchanged) and the difference therefore matters, or a case where structure exchange is trivially available and the hypothesis is empty?

Answer: `RESIDUAL_IS_INTERFACE_STANDARD_AT_MOST` / `CONTROL_RESIDUAL_PLAUSIBLE` / `HYPOTHESIS_EMPTY_AS_STATED` / `CANNOT CHECK`, with your decisive example.

#### D14 — World ≠ machine correction

Does the four-way separation in §2 (target change; observation-channel change; epistemic revision; generative-regime change) carry content beyond the ordinary partially-observed-system setting, in which an observer's update never by itself establishes that the observed system changed? Does any sentence, table row or figure in V21 still imply that the target of inquiry and the epistemic machine share one transition structure, that nature computes, or that a representation can be identified with its target? Quote the passage if so.

#### D15 — Discrepancy-locus interface

Is the seven-locus responsibility object with `CANNOT_IDENTIFY`, the diagnostic-evaluator independence requirement, and the two-gate escalation (§6, Figure 2) a useful cross-parent interface, or model-based diagnosis, impasse-triggered metareasoning, Duhem–Quine error localization and independent verification and validation renamed? Which loci would a native reviewer in your field merge, split or delete? Is `CANNOT_IDENTIFY` a scientifically honest terminal or a refusal that hides underperformance?

#### D16 — Pre-commitment before outcome disclosure

Pre-registered exact studies exist (§10) and their outcomes are withheld from you. State now, in writing, which **specific outcome** of the interface-information ladder (§7), of ME-X1 or of ME-X4 would move your D9 terminal, and to which terminal. If no possible outcome of these studies would move your terminal, say so and say why (for example, because the question is conceptual rather than empirical, or because the studies test the wrong object). This answer will be compared with any later post-outcome review and may not be revised retroactively.

#### D17 — Name relative to the adjacent vocabulary (the external naming question as gated)

Does the compound *Machine Epistemics* improve demarcation relative to machine epistemology, epistemic control / epistemic engineering, metascience, autonomous-science governance and AI-for-science methodology — or should the programme be renamed while retaining a bounded scientific object? If rename, propose the label you would expect a parent-field reader to recognize without explanation, and say whether the object survives your rename (`RENAME__OBJECT_SURVIVES`) or must also contract (`RENAME_AND_CONTRACT`).

#### D18 — Superiority-ladder audit of V21 prose and figures

The programme forbids any implication that `Machine Epistemics > Machine Intelligence` or `> Machine Learning`. Read Table 1, the paragraph following it, Figures 1–3 and their captions, and the Conclusion. Does any wording or diagram element still invite a ranking or "higher intelligence" reading despite the stated caveat? Quote it. If none, say `NO_SUPERIORITY_IMPLICATION_FOUND`.

---

## 14. Reviewer independence declaration

Before reviewing, record in writing:

- primary expertise and the lens you are reviewing under (formal/computational epistemology or philosophy of science; AI-for-science / agentic science; systems / control / formal methods / assurance);
- current institution/role if you wish to disclose it;
- whether you contributed to the proposed framework, the manuscript, any ORION repository, or any of the study designs in §10;
- whether you have previously seen identifiable internal experimental or review outcomes of this programme, including AH20 outcomes, ME-X4 development results, H-EXT-1 results, or any simulated review;
- whether another reviewer of this packet shares a material model, data, source, tool or adjudication process with you, or is a current co-author, supervisor, student or same-group colleague;
- whether you are cited in the V21 bibliography (this is expected for parent-field reviewers and is **not** a disqualification; it is a disclosure);
- conflicts or strong prior advocacy/opposition relevant to the field label or to any competing programme named in §4.3.

A reviewer who has seen any withheld outcome may still provide a useful post-outcome review but must not be represented as having supplied the pre-outcome demarcation judgement requested by this packet.

Reviewer independence is not inferred from number of names.

---

## 15. Adjudication rule

No majority-vote field decision is used. Arguments are synthesized by concern class:

- omitted parent / false novelty;
- incoherent object;
- redundant or misleading label;
- parent-sufficient composition;
- plausible composition residual;
- interface-standard-only residual;
- category error / anthropomorphism / world–machine conflation;
- local-to-global overclaim;
- missing evidence;
- resource/complexity drag;
- target significance;
- optional enrichment.

A positive review does not establish a field. It supplies independent evidence for a later Perspective and research programme. Journal acceptance, citation, community adoption and field recognition remain external outcomes. Reviews are quoted only with the reviewer's consent.

---

## 16. Change log: V3 relative to V2

| Area | V2 (bound to V14) | V3 (bound to V21) |
|---|---|---|
| Binding | V14 reconciled Perspective; no hash | V21 file and sha256; source commit; figure files |
| Object statement | ten-field state; residual located "in the decisions across transitions" | Box-1 object with receipt distinguished from witness; residual stated as the registered interface-information hypothesis (§7) |
| World/machine | not separated | four-way separation adopted; explicit non-claims (§2) |
| Locus interface | absent | seven loci + `CANNOT_IDENTIFY`, diagnostic-evaluator independence, two-gate escalation (§6) |
| Contemporary parents | 2026 epistemic-control work partly listed | typed execution graphs, model-discovery agents, self-revising systems, provenance-first autonomous science, workflow-level automation, formal-validity-vs-semantic-drift all conceded (§4.3) |
| Tagline | "control science of AI-driven discovery" | not used as a demarcation claim |
| Pre-registered studies | AH20 frozen, outcome withheld | AH20, ME-X1, ME-X4 (with ladder axis), H-EXT-1–4 and remaining ME-X studies listed with status; every outcome withheld (§10) |
| Terminals | V2 list | the seven gate-frozen terminals with rename qualifier (§12) |
| Questions | D1–D12 | D1–D12 verbatim + D13–D18 appended (§13) |
| Independence declaration | seven items | adds repository/study-design contribution, withheld-outcome exposure, co-author/same-group relation, bibliography citation disclosure (§14) |
| Adjudication classes | eleven | adds interface-standard-only residual; extends category-error class (§15) |

## Packet terminal

```text
CANONICAL_MANUSCRIPT = FLAGSHIP_V21_NMI_READER_HARDENED
MANUSCRIPT_SHA256 = e6796fbfed8a1b1f1880d8d2cff4fecfd498badc420a806c28ae1a1fe30d83eb
PACKET_VERSION = V3_OUTCOME_BLIND
QUESTIONS_D1_D12 = FROZEN_VERBATIM_FROM_V2
QUESTIONS_D13_D18 = APPENDED_FROZEN_2026_09_02
EL10 = PARENT_SUFFICIENCY_NULL_RETAINED
EL20 = CATEGORY_ERROR_AUDIT_PASS_RETAINED
AH10 = EXACT_REFERENCE_SEMANTICS_PASS
AH20 = OUTCOME_WITHHELD_FROM_PACKET
ME_X1 = PROTOCOL_FROZEN__NO_OUTCOME_SUPPLIED
ME_X4 = DESIGN_FROZEN__DEVELOPMENT_OUTCOME_WITHHELD
H_EXT_1 = DESIGN_FROZEN__NO_NUMBERS_SUPPLIED
H_EXT_3 = REGISTERED_HYPOTHESIS_ONLY
WORLD_IS_MACHINE = FALSE
FIELD_STATUS = HYPOTHESIS_NOT_FOUNDED
REVIEW_STATUS = READY_TO_BIND_GENUINELY_INDEPENDENT_REVIEWERS
```
