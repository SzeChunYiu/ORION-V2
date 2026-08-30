# Machine Epistemics
## Toward a Science of AI-Driven Inquiry and Scientific Change

## Abstract

Artificial intelligence is moving from isolated prediction toward persistent research systems that retrieve evidence, construct models, choose experiments, operate tools and revise scientific claims. The relevant knowledge is distributed across epistemology, statistics, causal inference, control, metareasoning, measurement, formal methods, assurance, security and scientific practice. We propose **Machine Epistemics** as a falsifiable higher-order programme for studying the scientific transitions connecting these local competencies. Its candidate object is not one universal reasoning algorithm but changes in evidence, representations, methods, experiments, research agendas and commitments, together with constraints on when those changes are warranted, transported, preserved or reopened. Four foundations compete: strongest parent federation, selective interfield theories, an absorptive transition theory and plural/domain federation. A distinct field is justified only if cross-transition constraints preserve parent-native validity and add scientifically useful decisions beyond strongest parent composition. Otherwise the proposal should contract, merge or be renamed.

## From scientific outputs to scientific transitions

AI is changing the unit of scientific evaluation. A model may once have been judged mainly by a prediction or generated answer. Emerging systems can search literature, propose hypotheses, write and execute code, choose experiments, control scientific instruments, interpret observations and draft research outputs. Autonomous chemistry, materials laboratories, end-to-end AI-research systems and multi-agent scientific assistants already demonstrate parts of this loop [1–5].

The scientific question is consequently no longer only whether a generated answer is correct. It is whether a **sequence of state-changing actions** is warranted. A genuine paper can be attached to the wrong claim. Several agents can agree because they share a model or retrieval corpus. A numerically stable program can solve the wrong scientific model. A reproducible benchmark can be insensitive to the error denied by a conclusion. An abstraction can preserve today's decision but lose information needed after tomorrow's evidence. A formally correct proof can certify a mistaken empirical specification. Strong evidence can still fail to confer permission to act.

These failures are distributed across mature disciplines. Formal learning studies reliable inquiry. Belief revision and truth maintenance study changing commitments. Decision theory, metareasoning and experimental design study action under uncertainty and cost. Control and cybernetics study feedback and observability. Causal inference formalizes identification and transport. Metrology studies comparability and traceability. Formal methods study abstraction, refinement and behavioural equivalence. Provenance and reproducibility expose lineage. Statistics and evidence synthesis address dependence and uncertainty. Assurance, security, social epistemology and data governance add further constraints [6–20].

This density of parents is not an embarrassment to the proposal. It is its strongest falsifier.

We use **Machine Epistemics** as a provisional label for a higher-order question:

> **Under what conditions may a machine-mediated research process change a scientific commitment, representation, method, experiment or agenda—and what must be preserved, reopened or left unresolved when it does?**

The term itself carries no novelty claim. *Epistemics* has historical disciplinary uses; *machine epistemology* predates this programme; and recent work already discusses epistemic responsibility in human–AI collaboration, architectures of epistemic control for empirical AI research, verification-centred engineering of science, social and pragmatist evaluation of AI science, and the epistemology of closed-loop scientific AI [21–27]. The exact compound should therefore survive only if it demarcates a scientific object more clearly than existing language. Renaming is a legitimate outcome.

## What Machine Epistemics is—and is not

Neighboring “machine-X” terms mix mechanisms, processing architectures, capability evaluations, design orientations and application settings. Treating them as one ladder would create a category error. We therefore use the following **operational demarcation for this Perspective**; it is not a claim that the surrounding literatures already share one universal taxonomy.

| Term | Role in this Perspective | Central question |
|---|---|---|
| **Machine learning** | learning/update mechanism | How does a machine update from data, feedback or experience? |
| **Machine reasoning/planning** | process family | How does it derive, search, predict or select actions? |
| **Machine cognition** | processing architecture | How are representation, memory, attention, search, planning and communication organized? |
| **Machine metacognition** | self-monitoring/control mechanism | What can the system estimate about the adequacy or reliability of its own processes? |
| **Machine intelligence** | context-relative capability profile | How capable is a system under a declared ecology of tasks and constraints? |
| **Machine-native intelligence** | design orientation | Which strategies exploit machine-specific affordances without requiring human imitation? |
| **Machine scientific intelligence** | science-scoped capability | How capable is the system at making progress on scientific problems? |
| **Machine Epistemics** | epistemic/scientific control | When may machine-mediated inquiry change commitments, evidence state, representations, methods, problems or evaluators? |
| **AI for Science / agentic science** | application and autonomy ecosystem | How are AI methods and integrated systems deployed across scientific work? |

These roles are related but not totally ordered. A learning algorithm may implement part of a cognitive architecture; an architecture helps realize a system's capability; capability must be evaluated relative to the environment, task family, resources, boundary, substrate/interface, timescale and criterion under which it was established. *Machine-native* describes a design orientation, not an authority status. *Scientific intelligence* scopes capability to science. Machine Epistemics instead asks whether outputs from any of these mechanisms or systems may legitimately change scientific state.

Accordingly, we do not claim

\[
\text{Machine Learning}<\text{Machine Intelligence}<\text{Machine Epistemics}.
\]

The objects are not measured on one axis. A highly capable scientific system can be epistemically unreliable if it launders dependent evidence, silently changes criteria or cannot detect an invalid evaluator. Conversely, a conservative epistemic controller can be reliable yet scientifically weak because its native solvers are poor. Machine Epistemics is therefore **higher-order in responsibility for scientific change**, not a claim of universal performance superiority.

Machine metacognition illustrates the boundary. A self-model can estimate confidence, likely failure class, method adequacy or the value of more computation, but those estimates do not establish source independence, instrument validity, causal transport, evaluator sensitivity or external authority. Metacognition can inform an epistemic action; it does not replace the evidence and validation system that determines what the resulting scientific transition may warrant.

### Relation to epistemology and its formal descendants

Machine Epistemics should not be understood as “epistemology performed by machines,” nor as a replacement for epistemology. Epistemology already studies the nature, sources, limits and value of knowledge and justification; formal epistemology uses logic, probability and other mathematical tools to sharpen those questions; formal learning theory and computational epistemology ask when methods of inquiry can reliably converge to truth under stated possible-world and computability assumptions; and social epistemology studies testimony, disagreement, groups, institutions and the organization of collective inquiry. Contemporary work on the epistemology of artificial intelligence adds a further question: whether AI systems themselves can count as knowers or epistemic agents, and how epistemic responsibility should be distributed when humans rely on them.

The proposed object here is narrower in subject matter but more operational in form. Machine Epistemics studies **machine-mediated scientific transitions**: versioned changes in claims, evidence state, representations, models, methods, experiments, problems, evaluators and authority-relevant commitments. Its unit of analysis is therefore not a belief alone but an executable research episode with registered actions, observations, provenance, resources, validation and reopening conditions. A machine may use Bayesian updating, formal learning, theorem proving, active experimentation or another mature epistemic parent internally; Machine Epistemics asks what scientific transition those operations license, what they leave unresolved, and what must be preserved when the investigation changes its own representational or experimental machinery.

This distinction sets a strict claim ceiling. Formal learning theory already supplies a mathematical normative epistemology of reliable inquiry, and social/formal epistemology already extend beyond isolated human belief. Machine Epistemics earns a distinct scientific identity only if cross-parent transition constraints change prospective scientific decisions beyond a faithful federation of these parents and adjacent methods in control, identifiability, provenance, formal verification and scientific methodology. Otherwise the correct outcome is integration engineering or a narrower parent-owned theory rather than a new field.

### Frontier problems expose the distinction

On mature tasks, the problem representation, objective and admissible method family may already be well specified. Machine learning can then be exactly the right tool. A frontier problem is harder because the missing object may itself be unknown: more data may be needed, but so might a different model class, representation, scale, system boundary, measurement channel, operator, tool or problem formulation.

We therefore treat **frontier obstruction diagnosis** as a candidate operational primitive: before asking for a clever answer, ask what currently prevents a warranted answer and what observation or counterexample could discriminate among responsibility hypotheses. The sequence is obstruction-first rather than novelty-first: bind the current problem and locality; retain plural alternatives; test the strongest existing/native actions; diagnose incumbent insufficiency; and only then consider changing the solving space.

This makes learning one admissible epistemic action among retrieval, reasoning, proof, simulation, measurement, experiment and challenge. If a witnessed obstruction survives those lower-level routes, the system may propose model expansion, representation or perspective change, problem reformulation, tool construction, workflow revision or a broader regime transformation. Such a proposal must predict new reachable consequences and predecessor obligations before protected outcome access. The scientific result can still be lower-level sufficiency, refutation, non-identifiability or `CANNOT_CHECK` rather than a “creative” transition.

This frontier formulation is testable. Hidden-obstruction cases can compare direct generation, ML-only optimization, same-model reflection, strongest parent federation and explicit scientific-control routing on obstruction diagnosis, action-family choice, false/missed escalation, justified reach and resource cost. Until such evidence exists beyond the strongest parents, the frontier lifecycle remains an operational hypothesis rather than evidence that Machine Epistemics is a superior form of intelligence.

## Four foundations should compete

A new field cannot be justified by assembling a long list of concerns. It needs comparison against simpler explanations.

**F0: strongest parent federation.** Mature methods remain native. Causal inference governs causal claims; measurement science governs comparability; metareasoning chooses actions; assurance governs structured arguments; security governs adversarial channels; domain science governs substantive validity. Interfaces connect them. F0 is the lower bound: if careful federation makes the same scientific decisions at equal or lower cost, no higher field is needed.

**F1: selective interfield theories.** Some recurring interfaces may deserve theories of their own—execution to evidence, measurement to transport, uncertainty to action, support to authority—without supporting a broad new discipline. Science already contains successful interfield theories.

**F2: absorptive transition theory.** The strongest Machine-Epistemics hypothesis is that multiple scientific changes share constraints that can be represented in one higher-order transition theory while recovering and deferring to parent disciplines locally. F2 earns credit only when cross-parent structure changes a scientific conclusion, intervention or reopening decision.

**F3: plural/domain federation.** There may be no stable higher theory. Different domains can remain connected by local translation, provenance and boundary objects while preserving incompatible native semantics. F3 should win whenever common abstractions erase distinctions that matter scientifically.

These are competitors, not rhetorical alternatives surrounding a preferred F2.

## A transition ecology

The proposed object is broader than belief revision. Scientific systems alter different parts of an investigation, and the validity conditions for those alterations differ. A useful candidate abstraction is a **transition ecology**.

### Knowledge and source transitions

A paper, dataset, observation, expert statement or instrument output enters the investigation. Retrieval is not validation. Scientific use depends on source identity, semantic binding, provenance, dependence, scope and sometimes permission. A retrieved item is an observation to interpret, not a truth token.

### Relation and transfer transitions

Structure from one domain is reused in another. But “same” is plural: isomorphism, behavioural equivalence, causal transport, measurement comparability, decision sufficiency, safe approximation and rough analogy impose different conditions. Structure mapping, causal transport, abstract interpretation, anti-unification and Formal Concept Analysis already own much of this space [28–32]. A higher theory would have to coordinate these parents without turning generic similarity into scientific transport.

### Concept and representation transitions

Progress can require a new distinction rather than a new answer. A representation is demonstrably too coarse for a registered decision family when two cases it identifies require different scientific decisions. Such a **representation collision** licenses searching for a missing variable, scope condition, representation split or other repair; it does not by itself license invention of a new theory.

### Method and formalism transitions

When local repair is insufficient, a system can change method, instrument, operator or formal language. Formalism invention should be a late escalation: strongest parent first, then missing observation, local scope repair, representation change and only then a candidate new primitive, relation, operation or calculus. A useful formalism should recover valid predecessor cases, provide semantic models, generate checkable consequences and survive counterexamples. New vocabulary is not new science.

### Action and experiment transitions

A system selects a query, proof, simulation, measurement, intervention or construction. Metareasoning, active learning, Bayesian design and control already formalize much of this [10–13]. The higher-order problem arises when the *kind of blocker* is uncertain: missing evidence, invalid evaluator, non-identifiability, wrong model, wrong representation and unavailable authority require different interventions.

### Evidence and evaluator transitions

A result changes scientific force when support, dependence, calibration or evaluator scope changes. Ten agents sharing a model, corpus and evaluator do not create ten independent confirmations. A test result supports only failures the evaluator could have exposed. If a source or evaluator fails, earlier conclusions should reopen selectively rather than globally when independent sufficient support survives.

### Agenda and meta-policy transitions

Research systems also change what they work on. They may redirect a project, search for a remote donor, build an instrument, reformulate a problem or abandon a non-identifiable question. Novelty and surprise are not scientific authority; machine-generated opportunities remain proposals until a scientific or institutional process adopts them.

### Generative-regime and invention transitions

A still broader change occurs when the system alters not only a scientific state inside a fixed repertoire, but the **repertoire itself**. One candidate interface is a versioned `GenerativeRegime`: the current representation language, generative rules, operator repertoire, active constraints, problem portfolio, traversal policy and tool/affordance environment. Ordinary problem solving searches within this regime; an invention proposal changes one or more of these coordinates and therefore changes what can subsequently be represented, generated, done or asked.

This distinction is motivated by invention across many human practices, not only formal science. New scientific instruments, mathematical representations, engineering mechanisms, athletic movements, musical grammars, artistic techniques and design procedures can all be described as bounded transformations from a predecessor possibility space to a successor. But a regime mutation is not automatically an invention, and an invention is not automatically a scientific advance. The successor should make a registered capability, discriminator or decision newly reachable, preserve required predecessor competence or expose the loss, and remain subject to domain-native validation. Later fame or adoption is a separate social state rather than a validity oracle.

Computational creativity, novelty/non-objective search, quality-diversity, open-ended learning, design/problem-framing and cumulative cultural evolution are direct parent families for this question. Machine Epistemics would receive no credit for rediscovering their algorithms. The possible residual is narrower: whether a machine-mediated scientific process needs explicit responsibility for **when a possibility-space transformation is warranted, what predecessor obligations it must preserve, how the transform is validated, and when the new regime may affect scientific commitments**. A separate prospective benchmark is required before this candidate transition class can become a result-bearing mechanism.

### Epistemic locality and perspective transitions

Human scientific cognition is a powerful donor, but it is not a neutral definition of intelligence. Comparative cognition emphasizes mechanism-level comparison rather than treating human-like performance as the sole summit; ecological-rationality research shows that decision mechanisms can be strong because they fit particular environmental structures; collective-behavior studies show that useful information processing can be distributed across groups; and major-transitions theory shows that the scientifically relevant unit of organization can itself change [40–43]. These parents motivate a boundary condition rather than a new intelligence metric.

We therefore propose an **Epistemic Locality** hypothesis: competence should be interpreted relative to a declared environment, task family, resource regime, system boundary, substrate/interface, timescale and criterion. A system that dominates in one such ecology is not thereby globally superior. Human cognition is one historically realized solution; machine-native systems need not imitate it, but neither may machine-specific performance be universalized from one benchmark ecology.

This extension deliberately does **not** equate cognition, within-lifetime learning, collective adaptation, cultural accumulation and evolutionary adaptation. They may share abstract structures—variation, retention, feedback, selection, recombination or distributed coordination—while differing in mechanism, timescale, agency and evidential meaning. In particular, evolutionary fitness is neither scientific truth nor normative authority. Natural adaptation supplies donors and hostile controls, not a warrant root.

The corresponding perspective problem is operational. A scientific conclusion may change when the relevant boundary, organizational scale, temporal scale, environment or evaluator frame changes. When two admissible frames yield different registered judgments, the system should expose `PERSPECTIVE_DEPENDENCE` or establish a lawful transport relation rather than silently promoting one local conclusion to a universal claim. This is a candidate cross-cutting interface and remains falsifiable against ordinary context-conditioned metareasoning and domain-native parents.

### From local epistemics to an expanding atlas

The Epistemic Locality principle creates a second problem: every observed intelligence or epistemic practice is only a local sample. Human cognition, non-human cognition, collective inference, cultural accumulation, evolutionary adaptation and machine-native systems reveal different structures under different embodiments, resources, environments and timescales. Even an imagined extraterrestrial intelligence would supply another local chart rather than a view from outside the total space of possible intelligence. The astronomy analogy is therefore methodological rather than literal: broader structure can be inferred from limited observations only through explicit assumptions and independent probes; unlike cosmology, the programme does not assume an epistemic analogue of large-scale homogeneity or isotropy.

We therefore replace the idea of a known **global epistemic space** with a time-indexed **epistemic atlas**. At time \(t\), the atlas contains registered local contexts, the epistemic states or regimes meaningful in those contexts, typed relations that permit restricted transport between them, the probes available to discriminate alternatives, and explicit obstructions where local descriptions cannot be combined. A local result may be valid without transporting to another chart. Even compatible results on pairwise overlaps do not by themselves establish one globally coherent description; a global claim needs a separate gluing or transport witness. Local-to-global mathematics such as sheaf theory provides a direct parent for this pattern, but the programme should use sheaf or cohomological machinery only where the relevant cover, restriction and gluing structure is actually defined.

The atlas also needs an **epistemic horizon**. Current probes can render distinct candidate regimes observationally equivalent: two possibilities may produce indistinguishable observations even though they would require different scientific decisions. New experiments, measurements, environments or representations are useful when they split such a decision-relevant equivalence class. More radically, a persistent residual may survive all currently registered model, representation, probe and formalism classes. The correct state is then not a fabricated account of the missing mechanism but an explicit `OUTSIDE_CURRENT_ATLAS` boundary: evidence that the present representational system is insufficient, with no positive claim about what lies beyond it.

This yields a graded notion of globality. A claim may be local to one context; compatible across a declared cover; stable under a registered family of context transports; robust to fresh hostile chart/probe challenges over the current atlas; or universal by theorem inside an explicitly axiomatized formal universe. The programme does not admit an empirical state corresponding to “true for every possible epistemic system.” A finite collection of humans, animals, machines or synthetic worlds can strengthen an invariant, but cannot identify the observed atlas with the total space of possible epistemic mechanisms.

The practical consequence is constructive rather than skeptical. Machine Epistemics should actively expand the atlas: search for new charts that break current invariants, construct probes that refine observational equivalence, preserve failed gluing attempts as obstructions, and allow representation, tool or formalism changes when a witnessed horizon cannot be crossed within the incumbent regime. The long-run target is therefore not a final universal ontology of intelligence but an increasingly powerful, increasingly stress-tested map of epistemic possibilities whose boundary remains explicit.

The transition classes need not share one implementation. The field hypothesis concerns responsibility for change across implementations.

## Candidate constraints—and reasons to doubt them

A field-level theory becomes interesting only if some constraints recur across multiple transition classes. The following remain hypotheses rather than laws.

**Bind identity before inheriting validity.** A changed problem, criterion, source, representation, method, evaluator or epoch should not silently inherit the old conclusion.

**Do not amplify warrant across layers.** Provenance does not prove the scientific model. Numerical stability does not prove target-world adequacy. Formal derivation does not validate an empirical specification. Statistical support does not manufacture authority. A claim should not outrun a materially necessary weak link without a new warrant repairing it.

**Preserve relation type, uncertainty and dependence.** Approximate transport does not become exact through composition without an additional theorem. Unknown dependence does not become independence because agents have different names. Ignorance does not become a calibrated probability by formatting it as one.

**Require evaluator sensitivity.** A pass supports only error classes the evaluator could detect with warranted sensitivity. An unavailable or invalid oracle supports unresolvedness, not success.

**Reopen selectively.** When a source, relation, computation or evaluator is defeated, reopen commitments only when every sufficient valid support route has failed. This connects truth maintenance, provenance, assurance and severe testing without replacing any of them.

**Recover parents and defer locally.** A higher theory should preserve native judgments and prefer a mature parent whenever it solves a case with stronger guarantees or lower cost. Always doing more work is not a scientific virtue.

**Permit machine-native cognition but require external witness.** Scientific computation need not imitate human verbal reasoning. Programs, latent structures, large-scale search and non-human representations are acceptable when adopted scientific transitions have external tests, proofs, measurements or behavioural consequences proportionate to the claim [33–36].

**Do not universalize local competence.** Superiority, intelligence and method claims should bind the environment, task distribution, system boundary, scale, timescale, resource regime and criterion on which they were established. A cross-context claim requires a transport or robustness witness rather than rhetorical generalization.

**Do not identify the atlas with the territory.** No finite collection of observed epistemic systems, environments or probes establishes the total space of possible epistemic mechanisms. Empirical globality must remain bounded to a declared atlas; theorem-level universality remains relative to an explicit formal universe.

**Do not infer global coherence from local agreement.** Pairwise or overlap compatibility can support a matching family but not a global section without an additional gluing/transport witness. A local-to-global obstruction is a legitimate scientific outcome.

**Separate adaptation from warrant.** Survival, selection, popularity, adoption and historical persistence can identify mechanisms worth studying; none automatically establishes scientific truth or legitimate authority.

**Close only relative to a declared universe.** No finite search establishes universal exhaustion. Closure is relative to sources, routes, evaluators, domains and resources; unresolvedness can be the correct terminal.

Each constraint has an obvious objection. It may simply restate a parent discipline; it may add costly bureaucracy; it may be too conservative; or it may erase domain meaning. That is why comparison against F0, F1 and F3 is more important than conceptual elegance.

## Can machines learn scientific development itself?

A further frontier is whether machines can learn reusable **operators of scientific development** rather than only domain knowledge. Science-of-science studies population regularities in novelty, teams, citation, interdisciplinarity and research dynamics [37–39], but popularity and historical impact are not truth criteria. Successful, failed, partial and abandoned trajectories are also observed with very different probabilities.

A defensible hierarchy begins with source-bound research episodes; infers candidate development operators with preconditions, contraindications, failures and costs; learns policies for selecting or sequencing those operators; and retains higher abstractions only when they improve held-out prediction, transfer, prospective research decisions, resource use or compression without critical loss. Field and epoch holdouts are mandatory because a “general principle” that encodes discipline or era is not general.

The invention extension adds a particularly demanding episode type: reconstruct the predecessor possibility space before an historical change, freeze solver-visible information to that epoch, infer the transformation rather than merely the later artifact, and compare successful cases with failed, ignored, near-miss and independently rediscovered alternatives. Such data can suggest reusable transformation operators, but retrospective historical fit is still observational evidence. Any claim that an operator improves scientific development requires prospective or otherwise independently identified testing.

A second hardening is to vary the **unit and ecology of adaptation**. Candidate development principles should be challenged across human individual reasoning, non-human cognition, collective coordination, cultural accumulation, evolutionary adaptation and machine-native systems without assuming that those processes implement the same mechanism. A recurring structural pattern is scientifically interesting only if the native distinctions remain recoverable and the transfer improves a held-out decision or formal explanation.

Early evidence already illustrates how easily attractive meta-rules can fail. In a bounded 2024 arXiv version-transition pilot, an initial implementation contained a labeling defect caused by missing head-version metadata. After repairing that defect and rerunning all transitions with complete metrics, the context-conditioned transition model still underperformed a simple marginal frequency model: the mean log-score difference was \(-0.0747\) nats with a 95% bootstrap interval of \([-0.0982,-0.0510]\). None of 18 evaluable disciplinary categories improved over the marginal baseline, and finer transition alphabets increased the disadvantage. Several fixed “breakthrough” heuristics were also anti-predictive. The pilot is too narrow for a programme-level conclusion—failed trajectories remain poorly observed and the source is limited—but it is useful negative calibration: more contextual structure and intuitive meta-rules do not automatically create knowledge about scientific development.

A recursive programme should stop when a new abstraction adds no material residual under new fields, epochs and hostile omissions. The strongest admissible endpoint is a scoped stability candidate, never an “ultimate law of science.”

## How the proposal should be falsified

Machine Epistemics should be founded, contracted or abandoned through prospective tests rather than manifesto.

**Parent recovery.** Known-answer suites should test whether a higher representation preserves the parent science it claims to absorb. A failed bridge does not invalidate the parent.

**Cross-transition decisions.** Cases should require more than one scientific mode: reproducible but scientifically wrong computation; a calibration change that selectively invalidates earlier results; hidden dependence among apparent confirmations; representation change before a hypothesis is expressible; strong evidence without authority; or machine-native search requiring a non-linguistic witness. F2 earns credit only if it changes a registered scientific decision beyond information-matched F0/F1 without critical regression.

**Prospective generativity.** Before outcome access, candidate foundations should propose predictions, experiments, measurements, bridge constraints or counter-probes. Retrospective explanation is not enough.

**Locality challenge.** Registered cases should include environments, boundaries, scales, resource regimes or criteria under which a ranking is preserved, reversed or invalid to compare. An explicit locality interface earns credit only if it reduces false universalization or incorrect intervention beyond strongest context-conditioned parents.

**Frontier-action challenge.** Cases should hide the kind of missing object rather than merely hide an answer. The proposed control layer earns credit only if it identifies the obstruction and routes to the correct minimum action family more reliably than direct generation, ML-only optimization, same-model reflection and strongest parent federation under matched information/resources.

**Atlas/horizon challenge.** Exact cases should separate local validity, overlap compatibility, witnessed global coherence and genuine obstruction, and should include probes that do or do not refine decision-relevant observational equivalence. The explicit atlas/horizon interface earns credit only if it reduces false globalization, invalid transport or wrong probe selection beyond current K2/K4/K5 composition and the strongest identifiability/local-to-global parents. `OUTSIDE_CURRENT_ATLAS` must be penalized when used as a speculative escape from an ordinary explanation.

**Cross-domain recurrence.** One-domain improvement is scoped engineering. A field-level residual should recur across materially different sciences and independent evaluators.

**Resource adjustment and local deference.** A higher layer that ties a parent while consuming much more compute or expert time should contract.

**External demarcation.** Reviewers from parent disciplines—not framework developers—should judge whether the surviving object is best described as a distinct field, interdisciplinary programme, existing subfield, integration engineering or a differently named object.

Valid outcomes therefore include rename, parent sufficiency and integration engineering only. Those are not embarrassing failure modes; they are necessary controls on a field proposal.

## What would a machine-epistemic system require?

The programme implies interfaces, not a monolith: a stable problem/criterion identity; plural alternatives and obligations; evidence/provenance/dependence state; typed relations and representations; actions with execution receipts; controlled concept and method revision; evaluator and reopening state; learning of reusable procedures; optional versioned generative-regime state when the possibility space itself is under revision; optional boundary/scale/timescale perspective state when conclusions are perspective-sensitive; optional atlas/horizon state when local-to-global or observability limits are decision-relevant; and an external authority boundary.

LLMs, theorem provers, causal models, retrieval systems, simulators, program synthesis, laboratory controllers and humans can all occupy these interfaces. None is Machine Epistemics by itself.

## Conclusion

AI-driven science makes an old epistemological problem executable: not merely *what should we believe?*, but *what may a machine-mediated investigation change, on what warrant, and what follows from that change?*

Mature sciences already answer pieces of this question. Machine Epistemics deserves a distinct identity only if the relationships among those pieces form a stable and useful scientific object. The strongest current hypothesis is a transition ecology covering knowledge acquisition, structural transfer, conceptual and formal change, action, evaluation, research meta-policy, changes to the generative regime from which new representations, tools, operators and problems become reachable, the locality conditions under which apparently general capabilities or methods remain valid, and the atlas/horizon conditions under which local epistemic structures may—or may not—support broader claims. The observed atlas remains explicitly distinct from the unknown total space of possible epistemic mechanisms.

That hypothesis should be easy to kill. If strongest parent federation handles the same cases, use it. If selective bridge theories suffice, prefer them. If common abstractions erase domain meaning, choose plural federation. If explicit perspective state adds nothing beyond ordinary context conditioning, remove it. If frontier routing adds nothing beyond mature metareasoning and scientific-agent parents, remove it. If atlas/horizon state adds nothing beyond formal learning, identifiability, experiment design and current K2 transport, remove it. If recursive scientific-development learning only rediscovers population averages or publication bias, discard it. If the name collides with clearer existing language, rename it.

But if cross-transition constraints repeatedly preserve parent competence, diagnose failures that local methods miss, prevent false universalization across boundaries and scales, distinguish local compatibility from genuine global coherence, choose useful probes at current epistemic horizons, choose warranted actions when the missing object itself is unknown, generate new scientifically useful decisions across different domains and support machine-native cognition without surrendering external warrant, the object may merit a field of its own.

The task is therefore not to declare Machine Epistemics or to claim a completed global epistemology. It is to make the partial map precise enough that science can test where it holds, where it fails and how its horizon can be expanded.

## Transparency and versioning note

This Perspective is a research-programme proposal and synthesis. It does not claim that the distinct field has already been established. Empirical examples drawn from the associated research programme are labeled according to their actual evidential status, including negative and unresolved results. Large language model tools contributed materially to literature discovery, formalization, critique, software and drafting; AI systems are not authors, and human authors must independently review and adopt every scientific claim and citation before public release.
