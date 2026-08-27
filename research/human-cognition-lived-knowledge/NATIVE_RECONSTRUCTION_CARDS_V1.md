# Philosophy, Cognition and Human Practice — Native Reconstruction Cards V1

**Status:** executed first deep-reconstruction tranche for issue #40. This is not a claim that the books below have all been read cover-to-cover in this pass, and it does not close human-knowledge saturation. Each card records the evidence level used. Where a complete primary text was not available in the research pass, the disposition is provisional and the full-book obligation remains open.

## Review cell

This pass was cross-examined through five roles rather than one literature voice:

1. **Epistemology and history-of-science reviewer** — reconstructs the author's native problem and rejects anachronistic translation into ORION vocabulary.
2. **Cognitive-neuroscience and metacognition reviewer** — asks which proposed human mechanism has modern empirical/computational support and which is only philosophical analogy.
3. **Situated-practice and anthropology reviewer** — tests whether propositions, plans and documents omit competent action distributed across body, environment, artifacts and other people.
4. **Machine-learning and control reviewer** — accepts only consequences that can change a state variable, action, benchmark, failure class or falsifiable learning hypothesis.
5. **Hostile field/editorial reviewer** — asks whether a parent already owns the claimed idea, whether the addition is necessary for a protected decision, and whether it belongs in a flagship paper rather than a citation catalogue.

A candidate survives only when the native reconstruction remains recognizable after the other four reviews.

## Evidence scale

- **P1 — primary text inspected directly** in this pass (full text or substantial primary essay/chapter available).
- **P2 — authoritative scholarly reconstruction inspected** (for example Stanford Encyclopedia of Philosophy, publisher material and primary-linked scholarship) but full monograph not verified end-to-end.
- **E — modern empirical/formal cross-check inspected.**
- **OPEN — deeper primary/full-book reconstruction still required before closure.**

---

## Card A1 — Charles S. Peirce: inquiry, doubt, abduction and pragmatic consequence

**Evidence:** P1 for *The Fixation of Belief*, *How to Make Our Ideas Clear* and the historical Peircean abduction tradition; P2 for later reconstruction of abduction. **OPEN:** complete selected-writings reconstruction.

### Native problem

Peirce is not primarily offering a recipe for “creative AI.” His problem is how inquiry moves from the irritation of genuine doubt toward beliefs whose meaning and consequences can be made public and testable. His logic of science treats hypothesis formation, deduction of consequences and inductive testing as different inferential roles.

### Distinctions worth preserving

- belief versus genuine doubt;
- clarification of a concept through conceivable practical consequences versus truth itself;
- abduction/hypothesis generation versus deduction of consequences versus induction/testing;
- private tenacity/authority/a-priori fixation versus inquiry exposed to an external reality and community correction.

### Positive mechanism

Unexpected or surprising observations create a reason to search for explanatory hypotheses. Candidate explanations are not thereby accepted. They generate consequences that can be probed, and those probes can revise the belief state.

### Strongest ORION collision

P-C and P-E currently treat hypothesis/action selection more explicitly than **problem-formulation change induced by surprise**. A solver can be locally correct yet epistemically poor if it treats an anomalous observation as noise merely because the observation was not requested by the active workflow.

### Machine-executable reduction

Do not add `ABDUCTION` as a new kernel primitive. Add a typed path:

`unexpected_observation -> anomaly/surprise classification -> abductive portfolio -> discriminator obligations -> external test -> selective update`.

The abductive portfolio is proposal state, not evidence. A model's own fluency about why its hypothesis is plausible is dependent evidence.

### Hostile non-application

Routine deterministic transformations with a complete specification do not benefit from abductive branching. Forced “creative hypotheses” would be overreach.

### Disposition

**Absorb into K1/K4/K5; parent-owned inferential family.** Material for P-C/P-E and the flagship genealogy, not a new kernel coordinate.

---

## Card A2 — John Dewey: reflective inquiry and problematic situations

**Evidence:** P1 for the public-domain full text of *How We Think*; P2 for *Logic: The Theory of Inquiry*. **OPEN:** full *Logic* reconstruction.

### Native problem

Dewey treats reflective thought as disciplined inquiry arising from an indeterminate or problematic situation, not as detached manipulation of propositions. Inquiry changes the relation among problem, possible explanations, observations and action until the situation becomes sufficiently determinate for the purpose at hand.

### Distinctions worth preserving

- thought in the broad sense versus reflective thought;
- felt/recognized difficulty versus a well-formulated problem;
- suggestion/hypothesis versus reasoning about implications versus experimental testing;
- education into habits of inquiry versus possession of isolated facts.

### Positive mechanism

A problem is not always given correctly at the beginning. Inquiry can reformulate what the problem is. Reflection also applies to the conduct of inquiry itself: what evidence is missing, what operation failed, and what way of thinking is producing the impasse.

### Strongest ORION collision

A `ProblemContract` is necessary for custody, but treating the current contract as ontologically final would suppress legitimate scientific reframing. K4/J7 already permits problem-contract revision, yet V2 lacks a sufficiently explicit distinction between **authorized criterion change** and **scientifically motivated problem reformulation**.

### Machine-executable reduction

Represent `ProblemFrame_t` separately from immutable comparison identity. The machine may propose a new frame when evidence indicates that the old one is non-identifying, contradictory or excludes a material variable. Adoption of the new frame creates a new comparison identity unless a pre-bound relation proves continuity.

Candidate failure: `FRAMING_LOCK_IN` — the agent exhausts actions inside a frame despite a witnessed representation/problem-formulation insufficiency.

### Hostile non-application

A failed result is not by itself evidence that the problem statement should change. Reframing must not become criterion gaming.

### Disposition

**Absorb into K0/K4/K5 with strict identity semantics.** Direct parent pressure on P-C.

---

## Card A3 — Michael Polanyi: tacit and personal knowing

**Evidence:** P2 from University of Chicago Press reconstructions of *Personal Knowledge* and *The Tacit Dimension*. **OPEN:** full monograph reconstruction.

### Native problem

Polanyi challenges an ideal of scientific knowing as wholly explicit, impersonal rule following. Skilled judgment, tradition, participation and tacit integration are part of how scientists perceive patterns and act competently; one can know more than one can fully state.

### Distinctions worth preserving

- focal explicit content versus subsidiary/tacit awareness;
- formal rule versus skilled judgment in applying it;
- impersonal statement versus personal commitment in discovery;
- teachable statement versus competence acquired through participation/practice.

### Positive mechanism

Competence integrates many cues without requiring every cue to be separately represented in an explicit proposition. This does not make tacit judgment infallible; it makes **explicit text an incomplete carrier of some skills**.

### Strongest ORION collision

P-A/P-B can reconstruct theories from documents and transport registered judgments, but two systems can preserve propositions while failing to preserve the procedural competence needed to use them. Textual equivalence is not competence equivalence.

### Machine-executable reduction

Add optional `TacitDependency` metadata to a relation/evidence record only when demonstrated performance depends on contextual cues not captured by the explicit representation. Test with procedural episodes, demonstrations, checkpoints, corrections and changed materials/tools.

`CompetenceReceipt = (task_family, context, action_trace, checkpoints, correction_behavior, demonstrated_range, failure_boundary, source_mode)`.

### Hostile non-application

Do not use “tacit knowledge” as an excuse to waive explicit evidence, reproducibility or safety requirements. Where a task is completely formalized and parent solvers are sufficient, tacit metadata adds nothing.

### Disposition

**Absorb into K1/K2/K3; benchmark rather than new law.** Strong pressure on P-B and ML training design.

---

## Card A4 — Gilbert Ryle: knowing-how, intelligence and the intellectualist regress

**Evidence:** P2 through the current Stanford Encyclopedia reconstruction of Ryle and knowing-how debates. **OPEN:** full *Concept of Mind* primary reconstruction.

### Native problem

Ryle attacks the idea that intelligent action is always explained by a prior hidden theoretical act that states the rules for action. Following a rule, recipe, instruction or calculation is itself an intelligent performance that can go wrong and can require training and correction; invoking another proposition merely pushes the explanatory problem backwards.

### Distinctions worth preserving

- competent performance versus possession/recitation of facts;
- disposition/ability displayed across appropriate situations versus one successful output;
- instruction following versus intelligence in interpreting and correcting instruction use.

### Strongest ORION collision

A scientific agent can have a correct procedure text yet fail to recognize when the procedure applies, when the material state has departed from assumptions, or how to recover after deviation.

### Machine-executable reduction

Evaluate procedural knowledge under perturbation. A recipe/manual is a **partial policy specification**, not proof of competence. Require demonstrations of state recognition, timing, recovery and transfer.

Candidate failure: `INSTRUCTION_COMPETENCE_CONFUSION` — treating correct textual instruction or verbal explanation as evidence of executable skill.

### Hostile non-application

Do not infer that all procedural competence is irreducible to representations. Modern ML can learn procedures and policies; the test is whether the chosen representation preserves the relevant competence.

### Disposition

**Parent-owned distinction; absorb into P-B/P-C evaluation semantics.**

---

## Card B1 — Thomas Kuhn: exemplars, anomaly, crisis and conceptual change

**Evidence:** P2 through the 2025 Stanford Encyclopedia reconstruction of *The Structure of Scientific Revolutions*. **OPEN:** full primary monograph reread.

### Native problem

Kuhn explains scientific development through periods of normal puzzle solving organized by a disciplinary matrix and exemplars, punctuated by crises and conceptual change. Scientific training relies partly on exemplary problem solutions and learned similarity judgments rather than an exhaustive rule book.

### Distinctions worth preserving

- normal puzzle versus anomaly;
- anomaly versus crisis;
- theory/rules versus exemplars and trained similarity;
- cumulative change versus revolutionary change with possible loss/non-comparability;
- lexical/semantic change versus simple version change.

### Positive mechanism

A stable framework enables efficient puzzle solving until some anomalies undermine confidence in its capacity. A replacement can reorganize terms, standards and exemplars rather than simply append one more proposition.

### Strongest ORION collision

Kuhn is a direct parent threat to V2's `Jump`, representation epoch, transport and preservation semantics. It also warns that **regime change may alter the space in which old and new claims are compared**, making naive cross-generation parity impossible.

### Machine-executable reduction

Do not encode “paradigm shift” as a magic Jump level. Require explicit diagnostics:

`puzzle -> anomaly -> repeated/witnessed insufficiency -> representation/programme proposal -> relation/translation attempt -> preserved/lost capability receipt`.

Track exemplar competence as demonstrated problem-solving cases where useful.

### Hostile non-application

A benchmark failure, surprising observation or fashionable new model is not a Kuhnian crisis. Escalation requires protected insufficiency evidence.

### Disposition

**Strong parent ownership of representation/regime change; already largely absorbed by K2/K4/K5.** Add exemplar/practice warning to P-C/flagship.

---

## Card B2 — Imre Lakatos: research programmes and progressive versus degenerating change

**Evidence:** P2 from the substantively revised 2026 Stanford Encyclopedia entry. **OPEN:** primary MSRP volume reconstruction.

### Native problem

Lakatos shifts evaluation from isolated theories to sequences of theories inside competing research programmes. A programme is progressive when theoretical changes generate excess/novel empirical content and at least some is corroborated; it degenerates when modifications mainly accommodate known failures without independent success.

### Strongest ORION collision

ORION currently evaluates individual problem episodes and framework generations, but it needs a longitudinal warning against **repair activity that looks busy while producing no new discriminating success**. This is especially relevant to repeated framework revisions and autonomous self-improvement.

### Machine-executable reduction

Add programme-level metrics outside the kernel:

- prospective predictions/obligations created before outcomes;
- fraction independently corroborated;
- anomaly accommodations that produce no new test;
- protected capabilities gained/lost;
- resource spent maintaining the current hard core.

Candidate failure: `DEGENERATING_REPAIR_LOOP` — repeated post-hoc patches discharge local failures without generating independently testable progress.

### Hostile non-application

Do not terminate a programme simply because it is temporarily degenerating; Lakatos's own account allows reversals. The machine should represent the diagnosis and opportunity cost, not grant automatic abandonment authority.

### Disposition

**Absorb as K6 longitudinal evaluation / paper-programme governance, not a new kernel primitive.**

---

## Card B3 — Paul Feyerabend and methodological pluralism

**Evidence:** P2 via scholarly reconstructions of Feyerabend and philosophy-of-science literature. **OPEN:** full *Against Method* reconstruction.

### Native problem

Feyerabend's mature target is the claim that one universal methodological rule can explain or govern successful science across history. His pluralism is a warning against converting a historically contingent method into a timeless constitution.

### Strongest ORION collision

ORION is especially vulnerable to **over-formalization**: once a control interface exists, the framework may mistake its own explicit vocabulary for the whole space of good inquiry.

### Machine-executable reduction

The safe donation is not “anything goes.” It is a hostile requirement:

- maintain multiple parent methods when evidence does not justify collapse;
- include a simple/direct control and at least one method outside the framework's preferred representation;
- treat method choice as context-relative;
- allow `PARENT_METHOD_SUFFICIENT` and negative results.

Candidate failure: `METHOD_MONOCULTURE` — the controller excludes a scientifically admissible route solely because it does not fit its favored internal method representation.

### Hostile non-application

Pluralism does not waive evidence, safety, authority or falsifiability obligations.

### Disposition

**Hostile control on K4/K5/K6 and paper design; no new component.**

---

## Card B4 — Helen Longino: transformative criticism and social objectivity

**Evidence:** P2 from Stanford Encyclopedia treatments of social scientific knowledge and scientific objectivity. **OPEN:** full *Science as Social Knowledge* / *The Fate of Knowledge* reconstruction.

### Native problem

Longino argues that evidential relations rely on background assumptions and that objectivity is not secured by an isolated knower purging all values. Scientific communities can improve objectivity through effective critical interaction: venues for criticism, uptake, public standards and appropriately distributed intellectual authority.

### Strongest ORION collision

V2 models evaluator identity and dependence, but an “independent reviewer” is not epistemically useful merely because its process identity differs. A review system also needs **criticism uptake**: evidence that counterarguments can change the state rather than being logged and ignored.

### Machine-executable reduction

Add evaluation metadata:

`CriticismReceipt = (claim, critic/source, dependence, objection, target_assumption, response, state_delta_or_reason_no_change, authority)`.

Measure reviewer-source diversity and **uptake**, not only vote counts. Self-critique from the same model/context is dependent evidence by default.

### Hostile non-application

Do not convert social diversity or disagreement into automatic truth. The scientific contribution remains the quality of criticism and warranted update.

### Disposition

**Absorb into K3/K6 evaluation and P-D.** Strong parent threat to any novelty claim around multi-agent review.

---

## Card C1 — Hutchins, Suchman and Schön: cognition in practice

**Evidence:** P2 from MIT Press description/reconstruction of Hutchins, Cambridge summary of Suchman, and scholarship on Schön. **OPEN:** complete native cards for each monograph separately.

### Native problems

- **Hutchins:** cognitive work can be distributed across people, representations, instruments and socially organized routines; ship navigation is a system-level cognitive achievement.
- **Suchman:** plans do not fully determine situated action; they often function as resources used in practical deliberation as circumstances unfold.
- **Schön:** expert practice contains reflection-in-action and competent responses to surprising situations that exceed a simple application of explicit technical rules.

### Strongest ORION collision

The natural evaluation unit for an autonomous scientist is often not the base model. It is `agents + tools + memory + humans + instruments + interfaces + conventions`. A textual plan can be correct while the distributed system fails, or the system can succeed through situated recovery not represented in the initial plan.

### Machine-executable reduction

Represent a `DistributedCognitiveEpisode` as a provenance/dependence topology of transformations and decisions. Evaluate where information is created, lost, corrected and authorized. Plans are expected trajectories, not immutable descriptions of actual action.

Candidate failures:

- `PLAN_REALITY_CONFUSION` — treating the planned route as evidence of the route actually executed;
- `DISTRIBUTED_STATE_LOSS` — a critical state exists in an artifact/person/tool boundary but is unavailable to the decision-maker;
- `TACIT_INTERFACE_LOSS` — competence is lost across a handoff even though explicit instructions transfer.

### Disposition

**Absorb into K1/K3/K4 and P-D; benchmark at system level.**

---

## Card F1 — Metacognition, confidence and expected control

**Evidence:** E from Fleming, Dolan & Frith (2012) on metacognition and Shenhav, Botvinick & Cohen (2013) on expected value of control, plus modern confidence/error-monitoring literature.

### Native empirical problem

Task performance and monitoring of performance are separable. A system can be accurate but poorly calibrated about when it is accurate, or wrong but appropriately uncertain. Cognitive control also incurs costs; allocating additional effort depends on expected benefit and demand.

### Strongest ORION collision

Repeated “reflection” is not a sufficient self-improvement mechanism. If the same model generates an answer, critique and confidence without independent calibration, the system may only amplify one dependency chain.

### Machine-executable reduction

Maintain a learned `InquirySelfModel` that predicts at least:

- probability current answer/claim is correct;
- probability current method/representation is adequate;
- expected value of more computation/search;
- likely failure class;
- expected value of external review/tool use;
- calibration conditional on domain/task/source mode;
- known blind-spot classes with epoch/expiry.

Train/evaluate it on delayed or independent outcomes, held-out evaluators, counterexamples and transfer. Keep its output below the authority of its evidence roots.

Candidate failure: `SELF_MODEL_MISCALIBRATION`.

### Disposition

**High-priority K4 working state and P-C benchmark. No consciousness claim.**

---

## Card F2 — Insight and representation restructuring

**Evidence:** E from Kounios & Beeman's cognitive-neuroscience review and modern problem-solving literature.

### Native empirical problem

Some problems are not solved by more search in the same representation. Insight can involve a sudden reinterpretation that makes a previously inaccessible solution visible.

### Machine-executable reduction

Representation change becomes an explicit proposal action:

- split/merge a latent variable;
- introduce a hidden state/object;
- change coordinate system or scale;
- change causal graph family;
- alter problem decomposition;
- add/remove a relation;
- re-express the objective/problem frame.

A representation proposal is rewarded only if it unlocks held-out obligations while preserving or explicitly reopening protected prior decisions.

### Hostile non-application

Random reformulation is not insight. If lower-level search/repair is sufficient, restructuring is a false Jump.

### Disposition

**Absorb into K4/K5; strengthens P-C representation-insufficiency tests.**

---

## Card F3 — Curiosity, attention and exploration–exploitation

**Evidence:** E from Gottlieb et al. (2013), Oudeyer/Kaplan computational work, March (1991) organizational learning, and ML exploration literature.

### Native problem

Exploration can be driven by novelty, surprise, uncertainty, information gain or learning progress; these are not identical. Adaptive exploitation can become short-run efficient while destroying long-run exploratory capacity. Unpredictable noise can also attract naive curiosity signals without producing learnable structure.

### Machine-executable reduction

Use a typed exploration state rather than one novelty score:

`ExplorationSignal = (novelty, predictive_surprise, uncertainty, information_gain, learning_progress, option_value, cross_problem_relevance, noise_risk)`.

Budget exploration explicitly. Preserve a controlled attentional-capture route for high-salience unexpected events. Learn to suppress repeatedly uninformative stochastic novelty.

Candidate failures:

- `EXPLORATION_COLLAPSE` — exploitation removes routes needed to discover future material distinctions;
- `NOISE_CURIOSITY_TRAP` — unpredictability consumes exploration without reusable learning;
- `SURPRISE_SUPPRESSION` — an unexpected, potentially discriminating event is discarded only because it is off-task.

### Disposition

**K5 policy/benchmark change, not a new law.**

---

## Card F4 — Serendipity as encounter plus recognition

**Evidence:** E/P2 from Yaqub's 2018 taxonomy of scientific serendipity and historical scholarship. Yaqub distinguishes multiple mechanisms, including theory-led, observer-led, error-borne and network-emergent routes.

### Native problem

Serendipity is not random discovery and there is no defensible single fraction of all scientific discoveries that are “accidents.” Unexpected encounters matter only when someone recognizes possible value, connects the event to a problem or creates a new problem, and follows it with testing.

### Machine-executable reduction

Define:

`SerendipityCandidate = (encounter, unexpected_relative_to, source_identity, anomaly_type, candidate_cross_problem_value, recognition_reason, discriminator, cost, authority)`.

Maintain a low-bandwidth `EncounterBuffer` for anomalous side effects, failed experiments with structured residuals and off-query observations. Periodically compare encounters against unresolved problem graphs. Resulting hypotheses remain proposal-only.

### Hostile non-application

Do not maximize accident rate, stochasticity or novelty. A noisy random generator can create unlimited surprises with zero scientific value.

### Disposition

**Material P-E/P-C mechanism; parent-owned serendipity concept.**

---

# Cross-card reduction

The deep-reading tranche changes the framework in six durable ways without requiring a new kernel family:

1. **Problem formulation is mutable but identity-bound.** A scientific system must be able to question its own framing without laundering a changed criterion into the same comparison.
2. **Self-monitoring is distinct from task performance.** The self-model is learned, calibrated and fallible; self-reflection is dependent evidence.
3. **Knowledge is plural in form.** Propositional, procedural, perceptual, tacit, social/testimonial and institutional/authority knowledge have different failure conditions.
4. **Competence is demonstrated under context and perturbation.** Correct instructions are not sufficient evidence of skill.
5. **Discovery needs encounter channels.** Surprise, anomaly, curiosity, exploration, incubation and serendipity are proposal-generation/control mechanisms, never direct truth signals.
6. **The cognitive unit can be distributed.** Evaluation follows transformations across agents, humans, tools, artifacts and environments rather than crediting or blaming only the base model.

## Candidate benchmark additions

- `SELF_MODEL_CALIBRATION_AND_REVIEW_TRIGGER`
- `FRAMING_LOCK_IN_VS_CRITERION_GAMING`
- `INSTRUCTION_VS_COMPETENCE_TRANSFER`
- `SURPRISE_CAPTURE_VS_NOISE_FIXATION`
- `DEGENERATING_REPAIR_PROGRAMME`
- `CRITICISM_UPTAKE_VS_REVIEW_THEATRE`
- `DISTRIBUTED_COGNITION_HANDOFF`
- `SERENDIPITOUS_ENCOUNTER_RECOGNITION`

## No-new-kernel decision

All surviving structures can currently be expressed through K0–K6 interfaces. Adding a reflexivity, philosophy, creativity or tacit-knowledge kernel would duplicate existing identity/state/evidence/action/frontier/evaluation responsibilities before any protected downstream decision demonstrates necessity.

`HUMAN_COGNITION_RECONSTRUCTION_TRANCHE_1 = MATERIAL_FRAMEWORK_PRESSURE_FOUND`

`NEW_KERNEL_FAMILY = NOT_JUSTIFIED`

`FULL_BOOK_READING_CLOSURE = OPEN`

`EXPANDED_HUMAN_KNOWLEDGE_SATURATION = OPEN`

## Sources inspected in this tranche

Primary/scholarly anchors include Charles S. Peirce's *The Fixation of Belief* and *How to Make Our Ideas Clear*; John Dewey's *How We Think*; Stanford Encyclopedia entries on abduction, Thomas Kuhn, Imre Lakatos, Gilbert Ryle and the social dimensions/objectivity of scientific knowledge; University of Chicago Press descriptions of Michael Polanyi's *Personal Knowledge* and *The Tacit Dimension*; MIT Press material on Edwin Hutchins's *Cognition in the Wild*; Cambridge material on Lucy Suchman's situated actions; Fleming, Dolan & Frith (2012), Shenhav, Botvinick & Cohen (2013), Kounios & Beeman (2014), Gottlieb et al. (2013), March (1991), and Yaqub (2018).
