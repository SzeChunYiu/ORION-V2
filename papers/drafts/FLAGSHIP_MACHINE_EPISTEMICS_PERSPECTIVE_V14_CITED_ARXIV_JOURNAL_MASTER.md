# Machine Epistemics
## Toward a Science of AI-Driven Inquiry and Scientific Change

## Abstract

Artificial intelligence is moving from isolated prediction toward persistent research systems that retrieve evidence, construct models, choose experiments, operate tools and revise scientific claims. The relevant knowledge is distributed across epistemology, statistics, causal inference, control, metareasoning, measurement, formal methods, assurance and scientific practice. We use **Machine Epistemics** as a provisional label for a falsifiable higher-order programme studying the scientific transitions connecting these local competencies. Its candidate object is not a universal reasoning algorithm or a globally optimal intelligence architecture, but changes in evidence, representations, methods, experiments, problems and commitments, together with constraints on when those changes are warranted, transported, preserved or reopened. A distinct field is justified only if such cross-transition constraints preserve parent-native validity and add scientifically useful decisions beyond strongest parent composition. Otherwise the proposal should contract, merge or be renamed.

## From scientific outputs to scientific transitions

AI is changing the unit of scientific evaluation. A model may once have been judged mainly by a prediction or generated answer. Emerging systems can search literature, propose hypotheses, write and execute code, choose experiments, control scientific instruments, interpret observations and draft research outputs [@kramer2023automated; @lu2026endtoend; @ghareeb2026multiagent; @boiko2023autonomous; @szymanski2023autonomous].

The scientific question is consequently no longer only whether a generated answer is correct. It is whether a **sequence of state-changing actions** is warranted. A genuine paper can be attached to the wrong claim. Several agents can agree because they share a model or retrieval corpus. A numerically stable program can solve the wrong scientific model. A reproducible benchmark can be insensitive to the error denied by a conclusion. An abstraction can preserve today's decision but lose information needed after tomorrow's evidence. A formally correct proof can certify a mistaken empirical specification. Strong evidence can still fail to confer permission to act.

These failures are distributed across mature disciplines. Formal learning theory studies reliable inquiry [@kelly1996reliable; @sep2026formallearning]. Belief revision and truth maintenance study changing commitments [@doyle1979tms; @dekleer1986atms]. Decision theory, metareasoning and experimental design study action under uncertainty and cost [@russell1991metareasoning; @chaloner1995design; @settles2009active]. Causal inference formalizes identification and transport [@bareinboim2016transport]. Metrology studies comparability and traceability [@jcgm2012vim]. Formal methods study abstraction and refinement [@cousot1977abstract]. Provenance exposes lineage [@moreau2013provenance], while severe testing and argumentation address evidential challenge and structured support [@mayo1996error; @dung1995argument]. No higher-order proposal earns scientific credit merely by placing these subjects in one diagram.

We therefore use **Machine Epistemics** only as a provisional label for the following question:

> **Under what conditions may a machine-mediated research process change a scientific commitment, representation, method, experiment or problem—and what must be preserved, reopened or left unresolved when it does?**

The name carries no novelty claim. *Machine epistemology* is prior terminology [@wheeler2017machine], epistemic engineering has existing programmes [@cowley2023epistemic], and recent work addresses epistemic responsibility in human--AI collaboration [@lloyd2025responsibility], epistemic control in AI-assisted empirical research [@wojarnik2026spec; @ratti2026control], verification-centred engineering of science [@ma2026engineering], social and pragmatist evaluation of AI science [@lee2026pragmatism; @koskinen2023social], closed-loop AI science [@zenil2026closedloop], comparative epistemology of AI models [@pasquinelli2026comparative] and epistemic drift in human--model systems [@sogaard2026drift]. The compound should survive only if it demarcates a useful scientific object more clearly than existing language. Renaming is a legitimate outcome.

## What Machine Epistemics is---and is not

Neighboring ``machine-X'' terms mix mechanisms, process architectures, capability evaluations, design orientations and application settings. Treating them as one ladder creates a category error. For this Perspective we use the following operational demarcation; it is not a claim that the surrounding literatures share one universal taxonomy.

| Term | Role here | Central question |
|---|---|---|
| **Machine learning** | learning/update mechanism | How does a machine update from data, feedback or experience? |
| **Machine reasoning/planning** | process family | How does it derive, search, predict or select actions? |
| **Machine cognition** | processing architecture | How are representation, memory, attention, search and planning organized? |
| **Machine metacognition** | self-monitoring/control mechanism | What can the system estimate about the adequacy of its own processes? |
| **Machine intelligence** | context-relative capability profile | How capable is a system under a declared ecology of tasks and constraints? |
| **Machine-native intelligence** | design orientation | Which strategies exploit machine-specific affordances without requiring human imitation? |
| **Machine scientific intelligence** | science-scoped capability | How capable is the system at making progress on scientific problems? |
| **Machine Epistemics** | scientific-transition control | When may machine-mediated inquiry change commitments, evidence state, representations, methods, problems or evaluators? |
| **AI for Science / agentic science** | application/autonomy ecosystem | How are AI methods and integrated systems deployed across scientific work? |

These roles are related but not totally ordered. A learning algorithm may implement part of a cognitive architecture; an architecture helps realize capability; and capability is always evaluated under assumptions about environments, tasks, resources, boundaries, timescales and criteria. Formal attempts to define broad machine intelligence make these reference choices explicit rather than eliminating them [@legg2007universal], while No-Free-Lunch results remind us that algorithmic advantage depends on the problem distribution being privileged [@wolpert1997nfl]. Machine Epistemics is therefore **higher-order in responsibility for scientific change**, not a claim that it is ``more intelligent'' than machine learning or machine intelligence.

### Relation to epistemology and its formal descendants

Machine Epistemics is not ``epistemology performed by machines'' and does not replace epistemology. Epistemology studies knowledge, justification and cognitive success [@sep2024epistemology]; formal epistemology uses mathematical and logical tools to sharpen related questions [@sep2021formalepistemology]; formal learning theory asks when methods of inquiry can reliably converge under stated possible-world and computability assumptions [@sep2026formallearning; @kelly1989convergence]; and social epistemology studies testimony, groups, institutions and the organization of collective inquiry [@sep2024socialepistemology].

The proposed object here is narrower in subject matter but more operational in form. Machine Epistemics studies **machine-mediated scientific transitions**: versioned changes in claims, evidence state, representations, models, methods, experiments, problems, evaluators and authority-relevant commitments. Its unit is not a belief alone but an executable research episode with registered actions, observations, provenance, resources, validation and reopening conditions. A machine may use Bayesian updating, formal learning, theorem proving or active experimentation internally; Machine Epistemics asks what scientific transition those operations license and what remains unresolved.

This distinction sets a strict claim ceiling. Formal learning already supplies a mathematical normative epistemology of reliable inquiry, and formal/social epistemology already extend beyond isolated human belief. Machine Epistemics earns a distinct scientific identity only if cross-parent transition constraints change prospective scientific decisions beyond a faithful federation of these parents and adjacent methods in control, identifiability, provenance, formal verification and scientific methodology.

### Frontier problems expose the distinction

On mature tasks, the problem representation, objective and admissible method family may already be well specified; machine learning may then be exactly the right tool. Frontier problems are harder because the missing object may itself be unknown: more data may be needed, but so might a different model class, representation, scale, measurement channel, operator, tool or problem formulation.

We therefore treat **frontier obstruction diagnosis** as a candidate operational primitive. Before asking for a clever answer, ask what currently prevents a warranted answer and what observation or counterexample could discriminate among responsibility hypotheses. Learning becomes one admissible action among retrieval, reasoning, proof, simulation, measurement, experiment and challenge. Only after a witnessed obstruction survives lower-level routes should the system propose model expansion, representation or perspective change, problem reformulation, tool construction, workflow revision or a broader regime transformation. Such a proposal must predict new reachable consequences and predecessor obligations before protected outcome access. Refutation, non-identifiability, parent sufficiency and `CANNOT_CHECK` remain valid outcomes.

## Four foundations should compete

A new field cannot be justified by assembling a long list of concerns. It needs comparison against simpler explanations.

**F0: strongest parent federation.** Mature methods remain native. Causal inference governs causal claims; measurement science governs comparability; metareasoning chooses actions; assurance and severe testing govern evidential challenge; domain science governs substantive validity. Interfaces connect them. If careful federation makes the same scientific decisions at equal or lower cost, no higher field is needed.

**F1: selective interfield theories.** Some recurring interfaces may deserve theories of their own---execution to evidence, measurement to transport, uncertainty to action, support to authority---without supporting a broad new discipline. Science already contains successful interfield theories [@darden1977interfield] and boundary objects that coordinate heterogeneous practices without eliminating their differences [@star1989boundary].

**F2: absorptive transition theory.** The strongest Machine-Epistemics hypothesis is that multiple scientific changes share constraints that can be represented in one higher-order transition theory while recovering and deferring to parent disciplines locally. F2 earns credit only when cross-parent structure changes a scientific conclusion, intervention or reopening decision.

**F3: plural/domain federation.** There may be no stable higher theory. Different domains can remain connected by local translation, provenance and boundary objects while preserving incompatible native semantics. F3 should win whenever common abstractions erase distinctions that matter scientifically.

These are competitors, not rhetorical alternatives surrounding a preferred F2.

## A transition ecology

The proposed object is broader than belief revision. Scientific systems alter different parts of an investigation, and the validity conditions for those alterations differ.

**Knowledge and source transitions.** A paper, dataset, observation, expert statement or instrument output enters the investigation. Retrieval is not validation. Scientific use depends on source identity, semantic binding, provenance, dependence and scope.

**Relation and transfer transitions.** Structure from one domain is reused in another. But ``same'' is plural: isomorphism, behavioural equivalence, causal transport, measurement comparability, decision sufficiency, safe approximation and rough analogy impose different conditions. Structure mapping [@gentner1983structure], causal transport [@bareinboim2016transport], abstract interpretation [@cousot1977abstract], anti-unification [@plotkin1970generalization] and Formal Concept Analysis [@ganter1999fca] already own much of this space.

**Concept and representation transitions.** Progress can require a new distinction rather than a new answer. If two cases merged by the current representation require different registered scientific decisions, the collision licenses a search for a missing variable, scope condition or representation repair; it does not by itself license invention of a new theory.

**Method, experiment and evaluator transitions.** A system may change method, instrument, query, proof, simulation, measurement or evaluator. Successful execution is not scientific support; a test supports only failure classes it could have exposed. If a source or evaluator fails, earlier commitments should reopen selectively when their sufficient support is defeated.

**Agenda and problem transitions.** Research systems also change what they work on. They may search for a remote donor, build an instrument, reformulate a problem or abandon a non-identifiable question. Novelty and surprise are proposal signals, not scientific authority.

### Generative-regime and invention transitions

A broader change occurs when a system alters not only scientific state inside a fixed repertoire but the **repertoire itself**. One candidate interface is a versioned *generative regime*: representation language, generative rules, operator repertoire, active constraints, problem portfolio, traversal policy and tool/affordance environment. Ordinary problem solving searches within this regime; an invention proposal changes what can subsequently be represented, generated, done or asked.

Computational creativity, novelty search, quality-diversity and open-ended learning already supply direct parent theories and algorithms [@wiggins2006creative; @lehman2011novelty; @mouret2015mapelites; @hughes2024openended]. Machine Epistemics receives no credit for rediscovering them. Its possible residual is narrower: **when** a possibility-space transformation is warranted in a scientific process, which predecessor obligations must be preserved, how the transform is validated, and when a successor regime may affect scientific commitments. A mutation is not automatically an invention, and invention is not automatically scientific progress.

### Epistemic locality, diverse intelligence and perspective

Human scientific cognition is an unusually rich donor but not a neutral definition of intelligence. Ecological-rationality research shows that decision mechanisms can be strong because they fit particular environment structures [@todd2012ecological]. Octopus neurobiology illustrates sophisticated embodied organization with a very different nervous-system/body architecture [@hochner2012octopus]. Honeybee nest-site decisions show that useful group-level information processing can arise through distributed mechanisms [@seeley2004quorum]. Major-transition research further shows that the scientifically relevant unit of organization can itself change [@west2015majortransitions].

These donors do **not** justify equating cognition, collective adaptation, cultural accumulation and evolutionary adaptation. Similar abstract structures---variation, retention, feedback, selection or distributed coordination---can arise through different mechanisms, timescales and units. In particular, evolutionary fitness is neither scientific truth nor normative authority.

We therefore adopt an **Epistemic Locality** constraint: competence should be interpreted relative to a declared environment, task family, resource regime, system boundary, substrate/interface, timescale and criterion. A system that dominates in one ecology is not thereby globally superior. Cross-context claims require transport or robustness witnesses rather than rhetorical generalization.

### From local epistemics to an expanding atlas

Locality creates a second problem: every observed intelligence or epistemic practice is only a local sample. Humans, non-human animals, collectives, cultures, evolutionary processes, synthetic agents and future machine-native systems reveal structures under different environments and interfaces. Even an extraterrestrial intelligence would supply another local chart rather than a view from outside all possible intelligence.

We therefore replace the idea of a known **global epistemic space** with a time-indexed **epistemic atlas**. At time \(t\), the atlas contains registered local contexts, the epistemic states meaningful in them, typed relations permitting restricted transport, probes available to discriminate alternatives, and explicit obstructions where local descriptions cannot be combined. A local result may be valid without transporting elsewhere. Even compatible results on pairwise overlaps do not establish one global description; a global claim needs a separate gluing or transport witness. Sheaf-theoretic local-to-global mathematics provides a direct parent for this pattern [@robinson2017sheaves; @abramsky2011sheaf], but sheaf or cohomological machinery is appropriate only where the relevant cover, restriction and gluing structure is actually defined.

The atlas also needs an **epistemic horizon**. Current probes can render distinct candidates observationally equivalent even when they would require different decisions. New experiments, measurements, environments or representations are useful when they split such a decision-relevant equivalence class. Open-world recognition makes a simpler but important version of the same point: unknown inputs are not merely low-confidence known inputs [@boult2019unknown]. More radically, a residual may survive all registered model, representation, probe and formalism classes. The responsible state is then `OUTSIDE_CURRENT_ATLAS`: evidence that the present representational system cannot classify the residual, with no positive claim about what lies beyond it.

This yields a graded notion of globality: local to one context; compatible across a declared cover; stable under specified transports; robust to fresh hostile chart/probe challenges over the current atlas; or universal by theorem inside an explicitly axiomatized formal universe. There is no empirical state meaning ``true for every possible epistemic system.'' Formal universality is also not equivalent to executable universal intelligence: strong idealized universal-learning constructions can be incomputable [@leike2018computability].

The constructive target is therefore not a final ontology but an increasingly powerful, stress-tested atlas whose boundary remains explicit.

## Candidate constraints---and reasons to doubt them

A field-level theory becomes interesting only if constraints recur across multiple transition classes. The following remain hypotheses rather than laws.

**Bind identity before inheriting validity.** A changed problem, criterion, source, representation, method, evaluator or epoch should not silently inherit the old conclusion.

**Do not amplify warrant across layers.** Provenance does not prove the scientific model. Numerical stability does not prove target-world adequacy. Formal derivation does not validate an empirical specification. Statistical support does not manufacture authority.

**Preserve relation type, uncertainty and dependence.** Approximate transport does not become exact through composition without an additional theorem. Unknown dependence does not become independence because agents have different names.

**Require evaluator sensitivity and reopen selectively.** A pass supports only error classes the evaluator could detect. When support is defeated, reopen commitments whose sufficient valid support routes have failed, not every descendant indiscriminately [@doyle1979tms; @dekleer1986atms; @mayo1996error; @dung1995argument].

**Recover parents and defer locally.** A higher theory should prefer a mature parent whenever it solves the case with stronger guarantees or lower cost. Always doing more work is not a scientific virtue.

**Permit machine-native cognition but require external witness.** Programs, latent structures, large-scale search and non-human representations need not imitate human verbal reasoning, but adopted scientific transitions require tests, proofs, measurements or behavioural consequences proportionate to the claim [@silver2017alphagozero; @mathlib2020; @gulwani2017synthesis].

**Do not universalize local competence or identify the atlas with the territory.** Superiority claims must bind the ecology in which they were established. No finite donor set or benchmark establishes the total space of possible epistemic mechanisms.

**Do not infer global coherence from local agreement.** Pairwise compatibility can support a matching family without a global section. A local-to-global obstruction is a legitimate outcome.

**Separate adaptation from warrant and close only relative to a declared universe.** Survival, popularity or persistence can identify mechanisms worth studying but cannot establish truth or authority. No finite search establishes universal exhaustion.

Each constraint has an obvious objection: it may restate a parent discipline, add costly bureaucracy, be too conservative or erase domain meaning. That is why comparison against F0, F1 and F3 is more important than conceptual elegance.

## Can machines learn scientific development itself?

A further frontier is whether machines can learn reusable **operators of scientific development** rather than only domain knowledge. Science-of-science studies population regularities in novelty, teams, citation and interdisciplinarity [@fortunato2018science], but popularity and historical impact are not truth criteria. Successful, failed, partial and abandoned trajectories are also observed with different probabilities.

A defensible hierarchy begins with source-bound research episodes; infers candidate development operators with preconditions, contraindications, failures and costs; learns policies for selecting or sequencing them; and retains higher abstractions only when they improve held-out prediction, transfer, prospective research decisions, resource use or compression without critical loss. Invention episodes add a harder requirement: reconstruct the predecessor possibility space before a historical change, freeze solver-visible information to that epoch, infer the transformation rather than merely the famous artifact, and compare successful cases with failed, ignored, near-miss and rediscovered alternatives. Retrospective historical fit remains observational; an operator claim requires prospective or otherwise independently identified testing.

The same programme should vary the **unit and ecology of adaptation** across human individual reasoning, non-human cognition, collective coordination, cultural accumulation, evolutionary adaptation and machine-native systems without assuming shared mechanism. A recurring pattern is scientifically interesting only if native distinctions remain recoverable and the transfer improves a held-out decision or formal explanation.

## How the proposal should be falsified

Machine Epistemics should be founded, contracted or abandoned through prospective tests rather than manifesto.

**Parent recovery.** Known-answer suites should test whether a higher representation preserves the parent science it claims to absorb. A failed bridge does not invalidate the parent.

**Cross-transition decisions.** Cases should require more than one scientific mode: reproducible but scientifically wrong computation; calibration change that selectively invalidates earlier results; hidden dependence among apparent confirmations; representation change before a hypothesis is expressible; strong evidence without authority; or machine-native search requiring a non-linguistic witness. F2 earns credit only if it changes a registered scientific decision beyond information-matched parents without critical regression.

**Frontier-action challenge.** Cases should hide the kind of missing object rather than merely hide an answer. Explicit control earns credit only if it identifies the obstruction and routes to the correct minimum action family beyond direct generation, ML-only optimization, same-model reflection and strongest parent federation.

**Locality challenge.** Cases should include contexts in which rankings are preserved, reversed or invalid to compare. A dedicated locality interface earns credit only if it reduces false universalization beyond strongest context-conditioned parents; parent sufficiency is a valid contraction result.

**Atlas/horizon challenge.** Exact cases should separate local validity, overlap compatibility, witnessed global coherence and genuine obstruction, and include probes that do or do not refine decision-relevant observational equivalence. `OUTSIDE_CURRENT_ATLAS` must be penalized when used as a speculative escape from an ordinary explanation.

**Cross-domain recurrence, resource adjustment and external demarcation.** One-domain improvement is scoped engineering. A higher layer that ties a parent while consuming substantially more resources should contract. Reviewers from parent disciplines---not framework developers---should judge whether the surviving object is best described as a distinct field, an interdisciplinary programme, an existing subfield, integration engineering or a differently named object.

Valid outcomes therefore include rename, parent sufficiency and integration engineering. Those are necessary controls on a field proposal.

## What would a machine-epistemic system require?

The programme implies interfaces, not a monolith: stable problem/criterion identity; plural alternatives and obligations; evidence/provenance/dependence state; typed relations and representations; actions with execution receipts; controlled concept and method revision; evaluator and reopening state; learning of reusable procedures; optional versioned generative-regime state when the possibility space itself is under revision; optional boundary/scale/timescale state when conclusions are perspective-sensitive; optional atlas/horizon state when local-to-global or observability limits are decision-relevant; and an external authority boundary.

LLMs, theorem provers, causal models, retrieval systems, simulators, program synthesis, laboratory controllers and humans can occupy these interfaces. None is Machine Epistemics by itself.

## Conclusion

AI-driven science makes an old epistemological problem executable: not merely *what should we believe?*, but *what may a machine-mediated investigation change, on what warrant, and what follows from that change?*

Mature sciences already answer pieces of this question. Machine Epistemics deserves a distinct identity only if the relationships among those pieces form a stable and useful scientific object. The strongest current hypothesis is a transition ecology covering knowledge acquisition, structural transfer, conceptual and formal change, action, evaluation, changes to the generative regime from which new representations, tools, operators and problems become reachable, the locality conditions under which apparently general capabilities remain valid, and the atlas/horizon conditions under which local epistemic structures may---or may not---support broader claims.

That hypothesis should be easy to kill. If strongest parent federation handles the same cases, use it. If selective bridge theories suffice, prefer them. If common abstractions erase domain meaning, choose plural federation. If explicit perspective or atlas state adds nothing beyond ordinary context conditioning, formal learning, identifiability, experiment design and existing transport machinery, remove it. If invention control adds nothing beyond creativity/open-endedness parents, remove it. If the name collides with clearer existing language, rename it.

But if cross-transition constraints repeatedly preserve parent competence, diagnose failures that local methods miss, prevent false universalization, distinguish local compatibility from genuine global coherence, choose useful probes at current epistemic horizons, and support machine-native inquiry without surrendering external warrant, the object may merit a field of its own.

The task is therefore not to declare Machine Epistemics or a completed global epistemology. It is to make the partial map precise enough that science can test where it holds, where it fails and how its horizon can be expanded.

## Transparency and versioning note

This Perspective is a research-programme proposal and synthesis. It does not claim that a distinct field has already been established. Empirical examples from the associated programme must be labeled according to their actual evidential status, including negative and parent-sufficient results. Large language model tools contributed materially to literature discovery, formalization, critique, software and drafting; AI systems are not authors, and human authors must independently review and adopt every scientific claim and citation before public release.

## Bibliography source

Use `papers/flagship/FLAGSHIP_REFERENCES_V14_CORRECTED.bib`, `papers/flagship/FLAGSHIP_REFERENCES_V15_NEIGHBOR_SUPPLEMENT.bib`, and `papers/flagship/FLAGSHIP_REFERENCES_V16_FOUNDATION_SUPPLEMENT.bib`. The status of 2026 preprints/forthcoming works must be refreshed immediately before arXiv upload and again before journal submission.
