# Machine Epistemics: The Control Science of AI-Driven Discovery

**Manuscript type:** field-defining Perspective / synthesis draft.

**Preferred Tier-1 target:** Nature Machine Intelligence — Perspective.

**Tier-2 fallback:** npj Artificial Intelligence — Perspective or Review.

**Status:** working V1 draft. No new-field, novelty, scientific-truth, publication, or adoption authority.

## Abstract

AI systems are moving from isolated scientific assistance toward long-horizon research processes that retrieve literature, generate hypotheses, design experiments, call tools, prove or simulate, analyze results, revise plans, and draft scientific outputs. This transition exposes a systems problem that is not captured by task performance alone: when is a machine-mediated change in scientific belief, representation, search space, or conclusion actually warranted? We propose **Machine Epistemics**, the provisional study and engineering of how AI and hybrid research systems acquire, transform, compare, test, preserve, revise, reopen, and close scientific commitments under explicit evidence, uncertainty, provenance, resource, and authority constraints. We organize the field around a bounded Machine-Epistemic Episode and ten candidate foundation laws separating execution from evidence, integrity from correctness, similarity from typed transport, repetition from independence, stopping from completeness, and scientific support from authority. We relate these objects to AI for Science, agentic and autonomous science, metareasoning, active experimentation, truth maintenance and belief revision, model-based diagnosis, formal methods, provenance systems, evidence synthesis, control theory, and philosophy of science. The field hypothesis is deliberately falsifiable: if straightforward compositions of these parent disciplines reproduce the same protected scientific decisions, Machine Epistemics should contract to integration engineering rather than claim a new science. We conclude with a quantitative research programme for epistemic observability, justified reachability, evidence dependence, selective reopening, minimum sufficient escalation, context-relative transport, evaluator stability, and bounded epistemic closure.

## 1. AI is becoming part of the scientific method

Scientific AI has progressed from prediction and pattern recognition toward systems that participate in the research loop itself. Contemporary work on AI for Science, scientific agents, agentic science, autonomous laboratories and fully automated research systems increasingly treats literature, hypotheses, experiments, code, analysis and writing as components of an executable process.

That progress creates a new failure surface. A research system can execute every software step successfully and still be scientifically wrong. It can retrieve real papers and still misbind evidence. It can reproduce a result and still lack an independent validator. It can show stable performance and still have searched the wrong universe. It can preserve an identifier while silently changing the meaning of the represented object. It can correctly detect a local failure yet overreact by changing an entire framework. It can generate a high-confidence answer that exceeds the authority of its evidence.

These are not only model-accuracy problems. They are failures in **scientific state transition control**.

## 2. The proposed field

We use the working term **Machine Epistemics** for the science and engineering of machine-mediated scientific-state transitions.

Machine Epistemics asks:

> When may an AI or hybrid research system legitimately move from one scientific commitment state to another, what evidence and invariants must travel with that transition, what becomes invalid, what must reopen, and what authority does the resulting state possess?

The short description is:

> **the control science of AI-driven discovery.**

“Control” here is broader than control theory. It includes semantic, evidential, provenance, resource, verification, validation and authority constraints that do not reduce naturally to one scalar utility.

## 3. Why existing labels are not enough

### AI for Science

AI for Science is the broad parent umbrella for AI methods that advance scientific discovery. Machine Epistemics is not a replacement. It targets the cross-domain validity and control layer of the scientific process itself.

### Agentic Science

Agentic Science studies or builds agents that reason, plan, use tools and conduct scientific workflows. Machine Epistemics asks how the resulting scientific commitments are warranted and repaired, including in systems that are not agentic.

### Autonomous Science

Autonomous Science and self-driving laboratories emphasize closed-loop experimentation, robotics, adaptive design and instrumentation. Machine Epistemics includes those systems but also literature, proofs, simulations, heterogeneous evidence, changing representations, evaluation and non-experimental research.

### Epistemology of AI

The epistemology of AI asks foundational questions about machine knowledge, testimony, trust and epistemic agency. Machine Epistemics borrows normative distinctions but focuses on executable state, transition guards, measurements, benchmarks and systems failures in scientific work.

### Metareasoning and decision/control theory

These fields own resource-rational action selection, uncertainty, observability, controllability and experiment choice. Machine Epistemics adds non-compensatory scientific coordinates such as exact source identity, claim scope, dependence, criterion binding, selective invalidation and authority ceiling.

### Formal methods and knowledge representation

They own proof, specification, model checking, abstraction, logical revision and many equivalence notions. Machine Epistemics studies mixed formal/empirical scientific episodes where the important relation itself may change with context, evidence or epoch.

### Workflow, provenance and reproducibility

These fields own durable execution and lineage. Replayable provenance is necessary for Machine Epistemics, but provenance integrity does not prove scientific correctness.

## 4. Primitive object: the Machine-Epistemic Episode

We represent a bounded research episode as

`E = (P, S, O, A, R, M, V, X, H, K)`.

`P` is the problem and criterion contract. `S` is a plural scientific state containing claims, alternatives, representations and uncertainty. `O` contains unresolved scientific obligations. `A` is the set of admissible actions. `R` describes resource and tool access. `M` stores evidence identity, provenance, dependence and memory. `V` binds validation and evaluator contracts. `X` contains observations and execution outputs. `H` is append-only transition history. `K` is the authority boundary.

An action does not create truth directly. It creates an observation or candidate transformation. A separate interpretation decides what scientific transition, if any, is warranted.

## 5. Ten candidate foundation laws

### 5.1 Criterion conservation

A benchmark or research conclusion cannot remain “the same result” after a silent success-criterion change.

### 5.2 Execution/evidence separation

Tool success is not scientific support. Tool failure is not scientific refutation unless explicitly evidential.

### 5.3 Evidence identity

Support must bind to the actual source, content and execution identity used.

### 5.4 Non-amplifying authority

Evidence or validators cannot create more authority than their valid roots allow.

### 5.5 Context-relative transport

Equivalence and comparability are typed, contextual and expiring; approximate transport cannot silently become exact identity.

### 5.6 Selective reopening

When support is invalidated, only commitments lacking surviving independent support must reopen.

### 5.7 Dependence visibility

Duplicated or shared-source evidence is not independent support merely because it appears multiple times.

### 5.8 Censoring visibility

Unsearched or unavailable routes cannot become evidence of absence.

### 5.9 Bounded epistemic closure

Stopping requires a declared searched basis and omission challenge; flat output is not completeness.

### 5.10 Honest unresolved terminals

Missing evidence, identity, evaluator or authority can terminate as `CANNOT_CHECK` without being averaged into success.

## 6. A quantitative science of scientific control

A field requires mathematical and empirical questions, not only vocabulary.

### Epistemic observability

Which latent scientific states or failure causes are distinguishable from available receipts and observations? What is the minimum discriminating intervention?

### Justified reachability

Which warranted scientific states can be reached from the current episode under finite resources without violating authority or preservation constraints?

### Requisite epistemic variety

How rich must the available search, representation, model and experiment families be to resolve a class of scientific residuals?

### Minimum sufficient escalation

When ordinary repair is insufficient, what is the lowest intervention level that can resolve the obstruction while preserving prior valid commitments?

### Dependence-aware support

How should evidential value change under shared data, models, prompts, instruments, authors, sources or hidden assumptions?

### Selective reopening

How can a support hypergraph identify the minimal set of scientific commitments requiring revalidation after a premise or representation changes?

### Context-relative relation and transport

When do two scientific objects remain behaviorally, observationally, predictively, decisionally or approximately equivalent under a declared context?

### Epistemic stopping

What finite stopping rules minimize false closure while maintaining tractable cost under heterogeneous search routes and changed vocabulary?

### Evaluator dynamics

When does publishing, deploying or optimizing against an evaluator change the environment sufficiently that the prior evaluation is no longer valid?

## 7. Why cross-domain donor research matters

Many components of Machine Epistemics are already deeply developed—but under domain-specific names. Statistical experiment comparison, model-based diagnosis, truth-maintenance systems, psychometric invariance, metrology, workflow soundness, causal transportability, robust control, systematic-review stopping and provenance standards solve nearby structural problems.

The scientific opportunity is therefore not to rename each donor. It is to discover whether their domain-specific structures can be conservatively generalized into a smaller set of machine-executable scientific-control decisions while preserving native semantics.

This is why remote-domain donor hunting and native recovery are central methods rather than an introductory literature survey.

## 8. ORION-V2 as one experimental system

ORION-V2 is an experimental framework derived through this donor process. Its contracted interface currently contains seven families: contracts, plural state, relations/transport, evidence/provenance/revalidation, action/diagnosis, frontier/escalation, and evaluation/parity/saturation/authority.

Machine Epistemics must not depend on those exact module names. A field survives only if other systems can instantiate the same scientific objects differently.

## 9. Falsifying the field

The strongest criticism of a proposed new field is that it is merely an integration layer over established disciplines. We make that an explicit test.

Machine Epistemics should contract if:

1. the strongest parent composition makes the same protected scientific decisions;
2. cross-domain commonality disappears when native semantics are restored;
3. its formal abstractions do not transfer across materially different sciences;
4. its measurable gains reduce to more logging, more compute or more human expert labour;
5. it does not reduce false closure, false authority or harmful escalation;
6. independent reviewers cannot agree on a stable nonredundant object of study.

A negative result would still be valuable: it would establish a disciplined integration map for reliable AI-driven science.

## 10. What evidence would support the field?

We propose six minimum criteria.

1. **Cross-domain recurrence:** at least two materially distinct scientific domains instantiate the same transition abstraction.
2. **Formal residue:** at least one theorem, impossibility result or falsifiable systems law is not a direct restatement of a parent result.
3. **Protected decision value:** an integrated method changes a justified scientific decision versus the strongest parent-composed baseline under matched resources.
4. **Non-regression:** reliability and authority do not worsen on protected predecessor capabilities.
5. **Independent demarcation:** external reviewers can identify the field boundary without ORION-specific terminology.
6. **Negative controls:** there are documented domains/tasks in which Machine Epistemics adds no value and contracts to the parent method.

## 11. A basic Machine Epistemics curriculum

A future curriculum would combine scientific reasoning and AI systems rather than treat either as background.

- scientific claims, uncertainty and evidence;
- AI agents and autonomous research systems;
- decision theory, active experimentation and metareasoning;
- truth maintenance, belief revision and diagnosis;
- formal equivalence, abstraction and transport;
- provenance, dependence and selective invalidation;
- verification, validation and measurement;
- evaluator design and performativity;
- epistemic stopping and saturation;
- reproducible machine-epistemic experiments;
- authority, delegation and scientific governance;
- cross-domain practicum.

## 12. Research agenda

Near-term work should prioritize protected benchmarks and theory rather than building larger agents.

The most decisive studies are:

- remote structural parent discovery and novelty contraction;
- context-relative scientific relation/transport;
- obligation-driven scientific control versus strongest donor-composed solvers;
- dependence-aware scientific evaluation;
- prospective scientific opportunity discovery;
- independent cross-domain tests of the Machine-Epistemic Episode abstraction.

## 13. Publication architecture

The field proposal should be supported by primary papers, not substitute for them.

P-A studies cross-domain donor discovery and conservative generalization. P-B studies relation and transport. P-C studies end-to-end scientific control and minimum escalation. P-D studies evidence dependence and dynamic evaluation. P-E remains contingent on measurable prospective opportunity value.

This flagship manuscript then asks whether the surviving results constitute a coherent field.

Our preferred target is a **Nature Machine Intelligence Perspective**, whose format is designed for balanced but forward-looking discussions of fast-moving or emerging topics. The planned fallback is an **npj Artificial Intelligence Perspective or Review**.

## 14. Conclusion

AI-driven discovery will not become scientifically reliable merely by making agents longer-lived, better tooled or more autonomous. Future research systems need explicit machinery for knowing what changed, why a conclusion is warranted, what evidence is independent, what assumptions still hold, what must reopen, when a search is genuinely saturated, and who or what has authority to declare the result.

We propose **Machine Epistemics** as the provisional field concerned with those questions.

The proposal is intentionally conditional. If existing fields already supply the complete answer in straightforward composition, Machine Epistemics should remain an integration discipline. If a stable composition-level science survives formal reduction and protected cross-domain evaluation, then machine-mediated scientific discovery may require not only better AI scientists, but a science of how those machines are allowed to know.
