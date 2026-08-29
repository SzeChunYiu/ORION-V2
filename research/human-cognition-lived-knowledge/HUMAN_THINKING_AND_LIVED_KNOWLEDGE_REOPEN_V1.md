# Human Thinking and Lived Knowledge — Saturation Reopen V1

**Status:** material search-universe extension. This document reopens the previous bounded saturation terminal. It grants no new ORION-V2 component, novelty, field status, or scientific authority.

## Why saturation reopens

The earlier all-domain programme searched broadly across academic disciplines and then repeated changed-vocabulary passes. That was not enough. Its effective search universe was still biased toward **explicit, codified, academically indexed knowledge**.

Human inquiry also depends on knowledge that is:

- tacit or only partly articulable;
- procedural and embodied;
- learned through apprenticeship and participation;
- distributed across people, tools and environments;
- triggered by surprise, anomaly, error or accidental encounter;
- guided by curiosity without an immediate external objective;
- shaped by self-monitoring, confidence and reflection on one's own thinking;
- preserved in recipes, craft routines, troubleshooting habits, field notes, oral traditions, casebooks, diaries, manuals, repair practices and everyday expertise.

This is not merely another domain list. It adds a new coordinate to the knowledge-search universe: **mode of knowing and mode of acquisition**.

Previous terminal `BOUNDED_POST_CONTRACTION_SATURATION` is therefore reopened for this scope.

## Review cell

Six adversarial lenses are used:

1. philosophy of inquiry and philosophy of science;
2. cognitive neuroscience, metacognition and cognitive control;
3. creativity, insight and serendipity research;
4. anthropology of skill, apprenticeship and everyday practice;
5. history/sociology of scientific discovery and innovation;
6. machine learning, continual learning and open-ended exploration.

Each donor is reconstructed in native terms before any ORION/Machine-Epistemics mapping.

---

# A. Reflexive cognition — thinking about one's own thinking

## A1. Dewey: inquiry into inquiry

John Dewey treated logic as an empirical theory of inquiry and explicitly described it as **inquiry into inquiry**. Reflective thinking is not passive introspection: a problematic situation triggers investigation, possible interpretations are generated, consequences are reasoned through, and action/observation transform the situation.

### Structural donation

A scientific solver needs a state not only for the external problem but also for the **quality and adequacy of its own inquiry process**.

Candidate machine object:

`InquirySelfModel = (current_strategy, monitored_signals, confidence, known_failure_modes, resource_use, unresolved_process_hypotheses, intervention_options)`.

This is stronger than a generic runtime trace because it supports intervention on the reasoning process itself.

## A2. Metacognition and meta-reasoning

Modern metacognition research distinguishes object-level cognition from meta-level monitoring/control. Confidence is itself an inference and can be miscalibrated relative to task accuracy. Meta-reasoning studies how people monitor the progress of reasoning, decide whether to invest more effort, give up, seek help, or switch strategy.

### Structural donation

ORION-V2 should not equate:

- confidence with correctness;
- progress feeling with progress;
- repeated reflection with better reasoning;
- self-generated critique with independent review.

Candidate coordinates:

- `performance_estimate`;
- `metacognitive_confidence`;
- `confidence_calibration`;
- `reasoning_progress_estimate`;
- `self-model_source`;
- `self-review_dependence`;
- `meta_action` such as continue / allocate effort / seek external evidence / change method / stop.

A meta-controller can therefore be wrong about the object-level controller. That error itself must be observable and correctable.

## A3. Error monitoring and learning from failure

Cognitive neuroscience treats performance/error monitoring as an executive function. Educational and organizational research shows that error prevention alone is insufficient; error management, feedback and explicit analysis of failed reasoning can produce learning and innovation. High-confidence errors can be especially informative when corrective feedback is available.

### Structural donation

A failure receipt should carry more than `FAILED`:

`FailureLesson = (expected_state, observed_state, prediction_error, causal_candidates, confidence_before, corrective_evidence, repair, changed_policy, transfer_scope)`.

The system should test whether the lesson transfers rather than automatically generalize from one failure.

## A4. Second-order cybernetics

First-order control studies an observed system. Second-order cybernetics makes the observer part of the system and asks how observing/intervening changes both system and observer.

### Structural donation

Machine Epistemics already models performative evaluators; this donor generalizes the point:

> an epistemic system must sometimes model **how its own representation, probe, intervention, benchmark or publication changes the process it is trying to know**.

Candidate object:

`ObserverCoupling = (observer_model, observed_system, observation_action, induced_change, self_model_update)`.

This pressures any architecture that assumes a neutral external evaluator.

---

# B. Philosophy of discovery and scientific change

## B1. Peirce: surprise → abduction → deduction → induction

Peirce integrated abduction, deduction and induction into a cycle of inquiry. A surprising/puzzling phenomenon motivates a provisional explanatory hypothesis; deduction derives consequences; induction/experiment tests them. He also treated the economy of research as part of the method.

### Structural donation

The important state transition is not `anomaly -> accept explanation` but:

`surprise -> abductive portfolio -> predicted discriminators -> experiment/search -> update`.

A surprise should create an **opportunity to hypothesize**, not an authority-bearing claim.

## B2. Popper: falsification is methodologically mediated

Popper's logical falsification is simple, but actual scientific falsification is not: an apparent counterexample can reflect measurement or observation problems.

### Structural donation

A counterexample must be classified as:

- target-theory failure;
- measurement failure;
- auxiliary-assumption failure;
- representation mismatch;
- execution failure;
- unresolved.

This reinforces plural responsibility before reopening a theory/framework.

## B3. Kuhn: normal puzzle solving, anomaly, crisis, representation change

Kuhn distinguishes normal science from revolutionary changes in the disciplinary matrix. Anomalies accumulate inside a paradigm; crises can induce changes in concepts, instruments, exemplars and standards. Kuhn also emphasizes learned exemplars and similarity judgments rather than explicit rules alone.

### Structural donation

This is a major parent threat to V2 Jump. A useful Jump theory must distinguish:

- unsolved puzzle inside adequate regime;
- persistent anomaly;
- local auxiliary failure;
- regime-level insufficiency;
- changed standards/lexicon that affect cross-generation comparability.

It also suggests that scientific competence may depend on **exemplar-based recognition** not reducible to explicit rule lists.

## B4. Lakatos and Feyerabend: programmes and pluralism

Lakatos evaluates evolving research programmes rather than isolated hypotheses; programmes can be progressive or degenerating. Feyerabend's mature work attacks universal methodological rules and argues for theoretical pluralism and alternative worldviews.

### Structural donation

V2 needs portfolio-level history:

`ResearchProgramme = (hard_or_protected_commitments, adjustable_auxiliaries, problemshifts, novel_predictions, failures, progressive_or_degenerating_evidence)`.

And it needs a **methodological pluralism guard**: failure under one representation/method family must not automatically define the entire search universe.

---

# C. Tacit, procedural, embodied and situated knowledge

## C1. Ryle: knowing-how versus knowing-that

Ryle's challenge to intellectualism shows why possessing propositions/instructions is not the same as being able to perform intelligently. Recipes and maxims can guide action, but intelligent performance is not exhausted by consulting propositions.

### Structural donation

Knowledge state should distinguish:

- declarative proposition;
- procedural ability;
- perceptual discrimination skill;
- policy/strategy;
- demonstrated competence envelope;
- textual instruction.

A recipe is therefore not just a paragraph. It is a **partial action policy** with omitted context that a skilled actor supplies.

## C2. Polanyi: tacit and personal knowledge

Polanyi argues that scientific knowing is rooted in tacit capacities and personal participation, not wholly explicit impersonal rules.

### Structural donation

A scientific system should record when a claim or procedure depends on tacit expertise that has not been operationalized.

Candidate status:

`TACIT_DEPENDENCY_PRESENT`.

A method cannot be declared reproducible merely because textual instructions exist if competent execution relies on unbound skilled judgment.

## C3. Embodied and ecological cognition

Embodied cognition and ecological psychology challenge the idea that cognition is only manipulation of detached internal symbols. Gibsonian affordances emphasize action possibilities relative to an organism/environment relation; phenomenological traditions emphasize embodied perception and skill.

### Structural donation

A knowledge representation may need:

`Affordance(state, actor_capability, environment) -> admissible_action_set`.

This differs from a generic action list: an action can exist abstractly but not be *available* to a particular system in a particular material context.

## C4. Situated and distributed cognition

Lave/Wenger treat learning as participation in social practice; Hutchins shows cognitive/computational properties distributed across a navigation team, artifacts and procedures rather than located in one person's head.

### Structural donation

Scientific cognition may be distributed across:

- AI model;
- notebook/database;
- instrument;
- workflow;
- human expert;
- laboratory convention;
- material setup;
- social authority.

The correct unit of analysis can therefore be a **cognitive system**, not an agent.

Candidate object:

`DistributedCognitiveEpisode = (participants, artifacts, role_graph, information_transformations, coordination_rules, failure_dependencies)`.

This is particularly important for apparent independent validators that are actually coupled through shared artifacts/practices.

## C5. Apprenticeship, craft and everyday expertise

Anthropology shows knowledge transmission through pottery, tailoring, midwifery, subsistence, construction and many other practices. Expertise is enacted through socialization, evaluation, institutionalization, objects and culturally learned attention.

### Structural donation

The donor universe must include **practice records**, not only scholarly documents:

- instructional demonstrations;
- recipes;
- repair sequences;
- checklists;
- apprenticeship traces;
- oral descriptions;
- expert critiques;
- embodied measurements;
- before/after artifacts;
- failure cases.

A source can be scientifically useful even if it is not a paper, theorem or dataset.

---

# D. Serendipity, surprise and accidental discovery

## D1. Serendipity is not random luck alone

Research on serendipity distinguishes multiple types and mechanisms, including theory-led, observer-led, error-borne and network-emergent routes. Information-science research emphasizes both unexpected encounter and the capacity to recognize potential value.

### Structural donation

The discovery system needs two separate functions:

1. **encounter generation** — expose the system to non-target information/events;
2. **sagacity/value recognition** — detect that the encounter may matter to a different problem than the one currently pursued.

A system that only optimizes the current query can suppress both.

Candidate object:

`SerendipityCandidate = (encounter, current_task_distance, surprise, plausible_relevance_graph, candidate_new_problem, evidence_source, followup_cost, authority)`.

## D2. Surprise as a learning signal

Neuroscience and reinforcement-learning traditions treat prediction error as a major learning signal. Recent neuroscience work also suggests prediction-error signals can encode richer feature/state information beyond scalar reward.

### Structural donation

Do not reduce surprise to `bad score`.

Represent at least:

- reward/value surprise;
- state-transition surprise;
- feature/semantic surprise;
- causal surprise;
- model-class surprise;
- social/source surprise;
- evaluator surprise.

Different surprises imply different updates.

## D3. Insight as representation restructuring

Insight research emphasizes restructuring: the solution becomes available because the problem is represented differently, not merely because more local search was performed.

### Structural donation

Jump diagnosis should include a measurable `representation_restructuring` hypothesis and compare it against ordinary search/model expansion.

## D4. Curiosity and active sampling

Neuroscience distinguishes task-directed information sampling from more open-ended search for novel tasks/information. Organisms sometimes seek information or novelty even without immediate extrinsic reward.

### Structural donation

A frontier solver needs a bounded **curiosity budget** distinct from task utility. Candidate policy coordinates:

- expected information gain;
- learning progress;
- novelty;
- controllability;
- future option value;
- task relevance;
- opportunity cost;
- noise/unpredictability risk.

Curiosity must not become a scalar that rewards noisy distraction.

---

# E. Knowledge beyond science/engineering/mathematics

## E1. The donor universe is not identical to the academic literature

Candidate source classes now include:

### Codified scholarly

papers, books, monographs, theses, standards, patents, datasets, proofs.

### Codified non-scholarly

recipes, repair manuals, field guides, safety procedures, operator handbooks, design patterns, legal forms, craft instructions, military/aviation checklists, incident reports, software issue threads.

### Semi-codified practice

lab notebooks, diaries, casebooks, expert annotations, troubleshooting logs, training examples, oral histories, demonstration videos.

### Tacit/interactive

apprenticeship, observation of skilled performance, physical manipulation, interactive questioning, collaborative practice, instrument use.

### Environmental encounter

anomalies, accidents, failed experiments, material changes, unplanned events, unexpected correlations, natural observations.

A mature Machine Epistemics system needs a typed source ecology instead of one literature hierarchy.

## E2. Why a recipe can matter

A recipe contains a goal, ordered actions, ingredients/resources, quantities, timing, conditional branches and expected intermediate states. It often omits skilled discriminators such as texture, temperature feel, smell, visual appearance or how strongly to intervene.

Structurally, it can teach Machine Epistemics about:

- partial observability;
- procedural plans;
- tacit completion of underspecified instructions;
- checkpoints/intermediate state validation;
- recovery from local deviations;
- tolerance bands rather than exact states;
- adaptation to different materials/tools;
- causal sequence and non-commutativity.

The scientific point is not to treat cooking as formal science. It is to learn a general control structure from ordinary competent practice.

---

# F. Framework implications

The new research pressures the seven-family contracted kernel without yet authorizing expansion.

## F1. Add reflexive state to K1/K4 rather than a magical `SELF_REFLECT` atom

Candidate interface concepts:

- self-model;
- metacognitive confidence;
- calibration;
- process-failure hypotheses;
- meta-actions;
- external-check trigger.

The parent is metacognition/meta-reasoning/second-order control. ORION's residual, if any, is scientific-state/authority coupling.

## F2. Generalize evidence/source model to lived knowledge

Evidence/source objects should be able to identify:

- proposition source;
- procedure source;
- competence demonstration;
- tacit dependence;
- environmental observation;
- social/distributed source.

`source_type != authority` remains invariant.

## F3. Create a surprise/opportunity interface behind frontier discovery

Do not add a universal novelty reward. Candidate typed triggers include error-borne, observer-led, theory-led and network-emergent serendipity.

A surprise may open a candidate problem but cannot self-authorize agenda change.

## F4. Expand responsibility topology to include observer/system coupling

A failed scientific result can be caused by:

- world/model mismatch;
- observer/probe distortion;
- evaluator performativity;
- social coordination failure;
- tacit-skill mismatch;
- distributed artifact failure.

## F5. Preserve pluralism and exemplar learning

V2 should support both explicit rules and exemplar/case-based skills. A skill may be admitted because it reliably discriminates situations, even before every discriminating feature is verbally explicit, but authority must remain bounded and the tacit dependency visible.

---

# G. New saturation rule

Human-knowledge saturation can no longer be defined only over disciplines.

A stronger coverage product is:

`Coverage = Discipline × SourceMode × KnowledgeForm × AcquisitionMode × Context × HistoricalEpoch`.

Where, provisionally:

- `SourceMode`: scholarly / institutional / craft / oral / artifact / environmental;
- `KnowledgeForm`: declarative / procedural / perceptual / social / tacit / normative;
- `AcquisitionMode`: reading / observation / imitation / experiment / dialogue / accident / play / participation;
- `Context`: problem/task/material/social regime;
- `HistoricalEpoch`: because concepts, practices and instruments change.

No claim of saturation is permitted until at least two changed-vocabulary passes also vary these non-disciplinary axes.

## Current terminal

```text
PREVIOUS_ACADEMIC_DOMAIN_SATURATION = REOPENED
REASON = NEW_MATERIAL_SOURCE_AND_COGNITION_COORDINATES
REFLEXIVE_COGNITION = HIGH_PRIORITY_DONOR
TACIT_SITUATED_KNOWLEDGE = HIGH_PRIORITY_DONOR
SERENDIPITY_SURPRISE_CURIOSITY = HIGH_PRIORITY_DONOR
EVERYDAY_PROCEDURAL_KNOWLEDGE = ADMITTED_SEARCH_UNIVERSE
GLOBAL_HUMAN_KNOWLEDGE_SATURATION = NOT_ESTABLISHED
```

No claim is made that human civilization's knowledge-structure space is exhaustible or already saturated.