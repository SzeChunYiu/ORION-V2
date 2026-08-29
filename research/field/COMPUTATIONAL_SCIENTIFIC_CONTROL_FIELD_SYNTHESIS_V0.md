# Computational Scientific Control — Provisional Field Synthesis V0

**Status:** provisional field hypothesis; no novelty, disciplinary, scientific-truth, or publication authority.

**Working label:** **Computational Scientific Control (CSC)**.

**One-line object:** the study and engineering of controlled transitions from scientific uncertainty to warranted, replayable, authority-bounded claims in human/machine research systems.

This document is deliberately stronger than a software architecture note and weaker than a claim that a new discipline has been established. It asks whether ORION-V2 and its neighboring literature reveal a stable scientific object with its own state variables, invariants, failure modes, theoretical questions, empirical programme, and engineering practice.

## 1. Why test a field hypothesis now?

AI can now automate large portions of scientific work: literature search, hypothesis generation, experiment design, code execution, analysis, manuscript production, review, and closed-loop laboratory operation. Recent AI-scientist, agentic-science, multi-agent discovery, and self-driving-laboratory work makes the scientific process itself an increasingly executable object. At the same time, recent work on epistemic infrastructure, epistemic control, provenance, verification, and research-software trust argues that generation capacity can outrun reliable validation.

The resulting technical gap is not merely “make a better scientist agent.” A scientific system may generate a plausible result while still failing because:

- the problem or criterion changed silently;
- a source route was censored and absence was inferred anyway;
- two representations were treated as equivalent outside their valid context;
- provenance integrity was mistaken for scientific correctness;
- evidence depended on the same hidden source multiple times;
- a repair invalidated downstream claims without reopening them;
- an evaluator changed after outcome access;
- a tool/process failure was interpreted as a scientific negative;
- a system stopped because output was flat although search coverage was incomplete;
- a correct result exceeded its authority ceiling.

CSC studies those coupled failures as one controlled epistemic process.

## 2. Neighboring fields and what they already own

CSC is not permitted to claim topics already owned by mature fields.

### 2.1 AI for Science / agentic science

Owns domain-facing AI methods, scientific agents, autonomous discovery workflows, foundation models for science, and increasingly end-to-end research automation.

CSC residual: the cross-domain control semantics governing when a scientific state transition is warranted, what it invalidates, what authority it has, and when the process may stop.

### 2.2 Self-driving laboratories and active learning

Owns closed-loop experimental design, robotics, Bayesian optimization, adaptive measurement, and laboratory automation.

CSC residual: a general theory that includes non-experimental routes, heterogeneous sources, changing representations, provenance/dependence, authority, selective reopening, and epistemic stopping.

### 2.3 Science of Science / metascience

Owns empirical study of scientific institutions, scholarly behavior, reproducibility, incentives, publication, collaboration, and the large-scale dynamics of science.

CSC residual: the design and verification of an individual or distributed research process as an executable control system. SciSci studies science; CSC attempts to make a scientific episode controllable and auditable.

### 2.4 Philosophy of science / social epistemology

Owns evidence, explanation, confirmation, realism, pluralism, epistemic authority, scientific reasoning, and normative questions about machine-mediated science.

CSC residual: operational and computational realizations of these distinctions as state variables, transition guards, receipts, tests, and measurable failure modes. Philosophy remains a parent, not a component to be replaced.

### 2.5 Control theory, POMDPs, active inference and metareasoning

Owns dynamical systems, feedback, observability, controllability, optimal control, decision-making under uncertainty, experiment selection, and resource-aware metareasoning.

CSC residual: scientific state contains non-compensatory semantic and authority coordinates that ordinary utility/state formulations often collapse: evidence identity, provenance, claim scope, criterion binding, independent support, authority ceilings, censored routes, and `CANNOT_CHECK`.

### 2.6 Knowledge representation, formal methods and theorem proving

Owns logics, ontologies, proof systems, model checking, abstract interpretation, bisimulation, specification, refinement, and mechanized verification.

CSC residual: mixed formal/empirical scientific episodes in which claims may be partially formal, uncertain, source-bound, experimentally grounded, socially reviewed, or not yet identifiable.

### 2.7 Workflow/provenance/reproducible-computing systems

Owns durable execution, workflow orchestration, data/version lineage, provenance models, experiment tracking, and reproducibility infrastructure.

CSC residual: provenance and replay are necessary but do not by themselves establish scientific correctness; CSC asks how lineage interacts with evidence, dependence, invalidation, selective reopening, evaluation and authority.

### 2.8 Research methodology, preregistration and evidence synthesis

Owns study design, preregistration, systematic review, reporting standards, bias reduction, and evidence synthesis.

CSC residual: general controlled adaptation when the research process must change framing, search universe, method, representation, or experiment while preserving the validity of earlier commitments.

## 3. Proposed primitive object

A **Scientific Control Episode** is a tuple

`E = (P, S, O, A, R, M, V, X, H)`

where:

- `P` — problem contract: question, scope, criterion, target authority, protected constraints;
- `S` — plural scientific state: claims, alternatives, uncertainty, search universe, representations;
- `O` — active obligations: evidence, verification, comparison, preservation, review, resource and authority obligations;
- `A` — admissible scientific actions;
- `R` — resources and capacities: tools, providers, time, compute, experimental access;
- `M` — memory/provenance/dependence state;
- `V` — validation and evaluator contracts;
- `X` — external world observations/results;
- `H` — append-only transition history.

A scientific action does not directly create truth. It proposes a state transition. A transition is **admissible** only if its preconditions, evidence, provenance, authority and preservation obligations are satisfied under the current contract.

This object is broader than an agent trace and narrower than “science as a whole.”

## 4. Basic dynamics

At time `t`:

1. observe current state and unresolved obligations;
2. generate admissible actions;
3. select an action under scientific and resource constraints;
4. execute via a tool, model, experiment, retrieval route, proof/checker, or human process;
5. bind the result to exact execution identity;
6. interpret the result under a frozen semantic contract;
7. update evidence/uncertainty/provenance/dependence;
8. test whether prior claims must reopen;
9. test stopping/saturation criteria;
10. emit a typed terminal or continue.

The loop differs from ordinary workflow execution because a successful task execution can yield a scientific failure, a scientific success, no scientific information, or an invalid/uninterpretable result.

## 5. Core distinctions

A CSC system must preserve at least these distinctions:

1. **execution success vs scientific support**;
2. **provenance integrity vs scientific correctness**;
3. **uncertainty vs falsity**;
4. **missing evidence vs contradiction**;
5. **route stop vs task stop**;
6. **flat output vs bounded saturation**;
7. **semantic similarity vs registered relation**;
8. **exact equivalence vs approximation**;
9. **local repair vs representation/method escalation**;
10. **scientific support vs authority to adopt/act/publish**;
11. **single-source repetition vs independent support**;
12. **criterion-preserving evaluation vs criterion churn**;
13. **persistent identity vs actual comparability across versions**;
14. **a generated candidate vs a verified scientific commitment**.

A proposed field is useful only if these distinctions lead to predictions, algorithms, tests, and engineering outcomes that are not captured sufficiently by parent fields in isolation.

## 6. Candidate invariants

### I1 — Contract conservation

Question, success criterion, case identity and evaluator criterion cannot change silently. A disclosed change creates a new comparison identity unless a frozen deviation contract permits it.

### I2 — Evidence/source binding

Scientific support must bind to the content/source/execution identity actually used, not only a human-readable label.

### I3 — Non-amplifying authority

A result cannot grant more scientific/operational authority than the valid support and issuing roots permit.

### I4 — Conservative transport

Relations across representations, contexts or epochs are context-relative. Approximate links cannot silently promote an exact terminal.

### I5 — Reopen on invalidated support

When a support premise changes or is revoked, every dependent commitment without an independent surviving support family must reopen.

### I6 — Failure separation

Provider, tool, timeout, parser, sandbox, infrastructure or orchestration failure cannot become evidence against a scientific hypothesis unless the scientific contract explicitly makes that execution event evidential.

### I7 — Censoring visibility

Unsearched or censored routes remain visible and cannot be converted into evidence of absence.

### I8 — Bounded stopping

A stop terminal must state the searched basis, residual uncertainty, censored routes and omission challenge. Flatness under an incomplete basis is not saturation.

### I9 — Replay identity

A scientific episode has a content-bound identity sufficient to determine whether a replay is actually the same case, criterion, resources, evaluator and subject.

### I10 — Honest unresolved terminal

If required evidence, identity, relation, authority or evaluator conditions cannot be established, `CANNOT_CHECK` is a valid terminal and cannot be converted into a pass by aggregation.

## 7. Candidate mathematical programme

CSC should become a science, not a vocabulary project. Candidate formal questions include:

### 7.1 Epistemic observability

Given outputs and receipts, which latent scientific-state coordinates can be identified? When are competing failure causes non-identifiable without a discriminating intervention?

### 7.2 Scientific controllability

From a bounded state and resource set, which justified scientific states are reachable without violating authority, preservation or evidence constraints?

### 7.3 Requisite epistemic variety

How rich must the action/representation/search family be to diagnose and repair a class of scientific residuals? When does failure justify expanding the action space itself?

### 7.4 Minimal sufficient escalation

Given a hierarchy of interventions, identify the lowest level that can resolve the current obstruction under preserved commitments. Characterize false escalation and missed escalation.

### 7.5 Dependence-aware evidence accumulation

How should support combine when observations share data, models, prompts, instruments, authors, transformations or hidden parent assumptions?

### 7.6 Selective reopening

Given a dependency/support hypergraph and changed premises, compute the minimal set of commitments that must reopen while preserving those with independent valid support.

### 7.7 Context-relative relation calculus

Characterize when two scientific objects are equivalent, comparable, approximately transportable, decision-equivalent, or incomparable under a declared context.

### 7.8 Epistemic stopping

Under bounded search and changing vocabularies, what stopping conditions minimize false closure while keeping cost finite?

### 7.9 Authority-safe delegation

How can a distributed human/model/tool system allocate execution and reasoning while preventing unverified outputs from inheriting decision or publication authority?

### 7.10 Prospective value of new scientific problems

Can a system predict which unresolved frontier opportunities will produce independent scientific value, rather than merely selecting topics that resemble past successes?

## 8. Empirical programme

A field claim needs benchmarks that cross domains and failure types.

### Benchmark family A — contract and criterion integrity

- unchanged criterion;
- disclosed and justified change;
- hidden criterion relaxation;
- evaluator mutation after outcome access;
- correct answer without authority.

### Benchmark family B — heterogeneous search

- lexical parent obvious;
- remote structural parent;
- censored route;
- synonymous structure;
- same words/different structure;
- source lineage corruption.

### Benchmark family C — semantic absorption

- atomic claims;
- ambiguous referents;
- context-dependent quantities;
- source projection recovery;
- multiple native representations;
- apparent extraction success with wrong scientific scope.

### Benchmark family D — reconstruction and gluing

- locally compatible/global inconsistent systems;
- multiple justified portraits;
- new representation opening a new search route;
- structural obstruction;
- stale state after changed evidence.

### Benchmark family E — diagnosis and experiment selection

- single fault;
- multiple faults;
- interaction-only fault;
- non-identifying evidence;
- optimal discriminator under cost;
- infrastructure failure control.

### Benchmark family F — repair and reopening

- local repair sufficient;
- representation expansion required;
- method expansion required;
- alternative support survives;
- unaffected claims remain closed;
- improper global reset.

### Benchmark family G — saturation and stopping

- full coverage/no material change;
- flatness with censored route;
- vocabulary-shift omission challenge;
- repeated near-duplicate search;
- expensive low-yield route;
- premature global stop.

### Benchmark family H — evaluation and authority

- same-source reviewer dependence;
- blinded independent adjudication;
- provenance-only false corroboration;
- criterion churn;
- high score with authority violation;
- evaluator leakage.

### Benchmark family I — real execution and memory

- retries and timeouts;
- bounded output;
- process-tree cleanup;
- exact request/result replay;
- negative experience retention;
- mandatory context under budget pressure;
- invalid-content recovery.

## 9. Candidate metrics

CSC evaluation should be non-compensatory on safety/validity coordinates.

Primary:

- justified-terminal rate;
- false-completion rate;
- `CANNOT_CHECK` calibration;
- criterion-integrity failure rate;
- semantic-preservation rate;
- authority/integrity violation rate;
- selective-reopen precision/recall;
- censored-route accounting accuracy;
- replay-identity correctness.

Secondary:

- cost to decisive evidence;
- experiment/query efficiency;
- unnecessary work;
- unnecessary escalation;
- latency;
- useful reachability gain;
- reviewer burden;
- verification cost per warranted claim.

## 10. Relationship to ORION-V2

ORION-V2 is **one candidate reference architecture and experimental instrument** for CSC, not the definition of the field.

A genuine field must admit competing systems, including parent-composed systems that outperform ORION-V2. If the proposed CSC benchmarks can only be passed by ORION-specific vocabulary or artifacts, the field hypothesis has failed.

The contracted ORION-V2 kernel maps naturally to CSC coordinates:

- K0 contracts/identities/obligations;
- K1 plural scientific state;
- K2 context-relative relations/transport;
- K3 evidence/dependence/provenance/revalidation;
- K4 action selection and plural responsibility;
- K5 opportunity + minimum witnessed escalation;
- K6 evaluation/parity/saturation/authority.

This mapping is a hypothesis about sufficiency, not ownership of the underlying mathematics.

## 11. Proposed basic curriculum

A graduate-level CSC core could contain:

1. **Scientific reasoning and philosophy of evidence** — claims, models, explanation, underdetermination, severe testing, scientific pluralism.
2. **Probability and uncertainty** — Bayesian inference, calibration, decision theory, robust statistics.
3. **Control and sequential decision systems** — state estimation, feedback, observability, controllability, POMDPs, metareasoning.
4. **Experimental design and active learning** — Bayesian optimization, causal interventions, discriminating experiments.
5. **Knowledge representation and formal methods** — typed relations, constraints, model checking, refinement, abstraction.
6. **Information retrieval and evidence synthesis** — heterogeneous search, screening, source identity, systematic-review methods.
7. **Provenance and reproducible computing** — W3C PROV, versioning, workflow execution, research software engineering.
8. **Scientific dependence and validation** — correlated evidence, leakage, evaluator independence, reproducibility and replication.
9. **AI-for-science systems** — scientific agents, self-driving laboratories, domain foundation models, tool-using systems.
10. **Epistemic governance** — authority, human responsibility, preregistration, protected evaluation, publication/adoption boundaries.
11. **Scientific-control laboratory** — build and adversarially evaluate a research controller in at least two unrelated domains.

## 12. Field-defining flagship paper hypothesis

A single synthesis paper can test the field without adding a fifth/sixth ORION paper identity:

**Working title:** *Computational Scientific Control: A Systems Science of Machine-Mediated Inquiry*.

It should:

- define the object and state-transition view;
- reconstruct neighboring ownership honestly;
- state 8–12 falsifiable invariants;
- provide a minimal formalism;
- show ORION-V2 and at least two non-ORION parent-composed implementations;
- introduce a cross-domain benchmark taxonomy;
- report protected V1 parity/non-regression;
- include at least one prospective scientific-control case in a fresh domain;
- measure verification cost and false-completion, not only task success;
- explain conditions under which the “new field” claim should be rejected.

This flagship is a **programme synthesis format**. It does not create an additional standalone V2 paper slot. Publication architecture can later choose either (a) four specialist papers plus a non-novel overview/monograph, or (b) one flagship that absorbs multiple specialist papers. The paper-contraction gate must not be bypassed.

## 13. Rejection criteria for the field hypothesis

CSC should **not** be claimed as a distinct subject if any of the following survives strong review:

1. AI-for-Science + workflow/provenance + control theory already reproduces all protected decisions without material loss;
2. the proposed invariants reduce to ordinary software correctness plus established experimental-design practice;
3. cross-domain benchmarks cannot be constructed without ORION-specific assumptions;
4. semantic/authority distinctions cannot be operationalized reproducibly;
5. no protected case shows benefit over strongest parent-composed baselines;
6. the subject has no predictive theory, only descriptive taxonomy;
7. the required controls make research slower without reducing false completion or increasing justified reach;
8. independent reviewers judge the object to be an engineering integration rather than a scientific field.

A negative result can still justify an **engineering discipline / methods programme** without a new-science claim.

## 14. Current panel disposition

- **Systems/control lens:** coherent candidate object; strongest opportunity is constrained state-transition theory, especially observability, escalation and stopping.
- **Metascience/philosophy lens:** meaningful only if it keeps normative authority/evidence distinctions visible and does not claim philosophy as new machinery.
- **AI-for-science lens:** plausible missing horizontal layer across agentic science and self-driving labs, but must demonstrate value beyond domain-native closed loops.
- **Evaluation/governance lens:** strongest differentiator is non-compensatory integrity/authority + selective reopening + evaluator custody.
- **Publication lens:** field synthesis is worth drafting, but should not reopen paper proliferation before protected evidence.

**Current terminal:** `FIELD_HYPOTHESIS_WORTH_PROTECTED_TESTING`.

Not: `NEW_SCIENCE_FIELD_ESTABLISHED`.

## 15. Literature anchors for the next review

- Canty & Abolhasani (2026), *The past, present and future of self-driving laboratories*, Nature Reviews Chemistry.
- *Towards end-to-end automation of AI research* (2026), Nature.
- *A multi-agent system for automating scientific discovery* (2026), Nature.
- Wei et al. (2025), *From AI for Science to Agentic Science: A Survey on Autonomous Scientific Discovery*, arXiv:2508.14111.
- Ma (2026), *Toward an Engineering of Science: Rebalancing Generation and Verification in the Age of AI*, arXiv:2605.10425.
- Ratti (2026), *Epistemic Control and the Normativity of Machine Learning-Based Science*, arXiv:2601.11202.
- Wojarnik (2026), *Spec-Driven AI for Empirical Research: A Scoping Review and an Architecture of Epistemic Control*, SSRN 7073778.
- Liu et al. (2026), *AI Agents for the Science of Science: A Survey of Tasks, Architectures, Evaluations, and Challenges*, Findings of ACL 2026.
- W3C PROV family of recommendations and notes.
- Graßhoff & May (1995), *From Historical Case Studies to Systematic Methods of Discovery* / Epistemic Systems programme.

## Authority boundary

Nothing in this document establishes a new field, a priority claim, scientific truth, novelty, external adoption, publication authority, or final naming. Those remain dependent on protected empirical separation and independent disciplinary review.
