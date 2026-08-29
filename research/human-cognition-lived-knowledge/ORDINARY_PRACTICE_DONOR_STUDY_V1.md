# Ordinary Practice Donor Study V1 — Recipes, Repair, Checklists, Debugging and Lessons Learned

**Status:** deliberate non-academic source-mode pass required by issue #40. This study does not treat everyday practice as automatically scientific evidence. It asks which reusable knowledge structures appear when we stop equating knowledge with papers, equations and datasets.

## Question

What does an autonomous scientific framework miss if its donor universe contains only codified academic knowledge?

This pass deliberately samples five practical knowledge ecologies:

1. bread baking and recipes;
2. repair guides;
3. surgical safety checklists;
4. software debugging practice;
5. engineering lessons learned after real failures.

These were chosen because they differ in consequence, formality and source authority. The objective is not to claim that cooking and surgery are epistemically interchangeable. The objective is to identify **structural distinctions** that recur across unlike practices and to preserve their native authority boundaries.

---

## 1. Bread baking: a recipe is not a complete policy

### Source observations

King Arthur Baking's public bread guidance combines written recipes with state-dependent tests. Proofing time is explicitly treated as context-sensitive because temperature and humidity change the rate; bakers inspect dough height, elasticity and the “poke test.” Doneness can be judged through smell, sound, touch and visual structure, with temperature used as one confirming measurement rather than a universal single proxy. Over-proofed dough may admit a recovery action rather than an immediate terminal failure.

### Native structure

A recipe contains at least:

`Recipe = (ingredients, quantities, ordered operations, nominal times/temperatures, intermediate targets, endpoint)`.

Competent execution contains more:

`PracticalPolicy = Recipe + state_perception + context_adjustment + checkpoints + recovery + stop_judgment`.

The recipe says “rise for a range”; the skilled policy says “the clock is only a prior; test the material state.” The material itself supplies observations.

### Machine donation

1. **Nominal schedule is not state.** A workflow stage cannot be assumed complete because its timer or action count elapsed.
2. **Multi-modal checkpoints can dominate a scalar proxy.** A single thermometer/score may be misleading outside its calibration range.
3. **Thresholds are context-conditioned.** The same appearance/time can mean different things under changed materials/environment.
4. **Recovery is part of competence.** A deviation can trigger reshaping/reproofing rather than restart or silent continuation.
5. **Skill improves through episode-conditioned cue learning.** “Use your senses” is not magic; repeated episodes calibrate cue-to-state mappings.

### Candidate benchmark

`RECIPE_TO_COMPETENCE`:

- train one arm on text instructions only;
- train one on instructions + demonstrations/intermediate state observations + correction episodes;
- perturb temperature/material/tool conditions;
- evaluate state recognition, correct intervention timing, recovery and final outcome.

### Framework disposition

Absorb into K1/K4. No “recipe module.” Add `PracticalCompetence`/`TacitDependency` only when protected decisions change.

---

## 2. Repair guides: procedure plus warnings, tools and visual state

### Source observations

The iFixit guide-authoring standard asks for a summary, warnings, estimated difficulty/time, required tools, explicit steps and one-to-three photographs per step. The guide is designed for a global audience and warns against relying on text alone.

### Native structure

A competent repair guide binds:

- target component and device state;
- prerequisite tools;
- difficulty/time estimates;
- warnings/hazards;
- ordered state-changing actions;
- visual referents and localization;
- implicit reversibility/reassembly assumptions;
- points where the observed state should be compared with the expected state.

### Machine donation

1. **Action validity depends on affordances/resources.** Knowing the next action without the right tool/access is not executable knowledge.
2. **Representation is often multimodal.** Spatial correspondence in an image can be essential to a safe action.
3. **Warnings are non-compensatory gates.** A high expected repair value cannot purchase permission to ignore a hazard.
4. **Difficulty is not scientific value.** Resource estimates belong beside, not inside, correctness.
5. **Procedure identity includes object version.** A visually similar device can require a different internal path.

### Candidate benchmark

`REPAIR_GUIDE_TRANSPORT`:

- same component, same device version;
- same component, changed revision;
- visually similar but structurally different device;
- missing tool;
- ambiguous photo/text alignment;
- successful disassembly with unsafe condition.

Evaluate whether the agent refuses or asks for a discriminator rather than transferring an apparently matching guide.

### Framework disposition

K0 identity, K2 relation/transport, K4 action/recovery. Strong P-B test case.

---

## 3. Surgical safety checklist: verification gates at phase boundaries

### Source observations

The WHO Surgical Safety Checklist was developed to reduce errors/adverse events and improve teamwork and communication. It places checks at three natural workflow boundaries: before anaesthesia, before incision and before leaving the operating room. WHO also emphasizes local adaptation and implementation conditions rather than presenting the checklist as an exhaustive universal procedure.

### Native structure

A safety checklist is not a plan for performing surgery. It is a **small set of high-value verification gates inserted into a richer skilled process**.

`ChecklistGate = (phase_boundary, must_check_items, team_confirmation, exception/escalation, local_adaptation)`.

### Machine donation

1. **Checklists complement expertise; they do not replace it.** A controller should not confuse a small mandatory gate set with the full domain policy.
2. **Phase boundaries are epistemically useful.** Some facts should be re-confirmed when the cost of proceeding rises.
3. **Team communication is part of the mechanism.** The check is partly a distributed-state synchronization operation.
4. **Local adaptation can be legitimate if identity is explicit.** Modified criteria must not inherit the authority/identity of an unmodified original silently.
5. **Completion evidence should bind who/what was checked.** A Boolean `checklist_complete=true` is weak if the item identities and confirmations are not recoverable.

### Candidate benchmark

`PHASE_GATE_CUSTODY`:

Inject cases where:

- all work is technically correct but a required identity check is skipped;
- one team member has a critical state not propagated to the others;
- a locally adapted checklist is mislabeled as the canonical one;
- the checklist passes but the underlying scientific/clinical claim is wrong.

### Framework disposition

K0/K3/K4/K6. Useful hostile control against “workflow correctness = scientific correctness.”

---

## 4. Software debugging: expected versus observed, minimal reproduction and one-change-at-a-time discrimination

### Source observations

GitHub's debugging-tutor guidance emphasizes reproducing the issue, reading errors, tracing execution, comparing expected with observed behavior, identifying recent changes, constructing a minimal reproduction and testing one change at a time.

### Native structure

Debugging is a practical form of causal discrimination:

`FailureLessonEpisode = (expected, observed, reproduction, candidate_causes, discriminating_change, result, repair, regression_check)`.

### Machine donation

1. **Reproducibility comes before explanation.** A one-off failure with uncertain identity should not support a strong causal lesson.
2. **Minimal examples are representation-reduction tools.** They isolate what must remain for the failure to occur.
3. **One-change-at-a-time is a dependence-control heuristic.** Bundled fixes destroy causal attribution.
4. **Recent-change reasoning uses temporal provenance as a prior, not proof.**
5. **A fix without a regression check is incomplete learning.**

### Candidate benchmark

`FAILURE_LESSON_TRANSFER`:

Compare raw error replay with structured lesson records containing expected/observed state, causal attribution confidence, discriminator, correction and transfer scope. Test on near but non-identical future failures.

### Framework disposition

K3/K4. Strengthens `FailureLesson` but does not create a new kernel primitive.

---

## 5. NASA lessons learned: failure becomes useful only after reviewed transformation

### Source observations

NASA's Lessons Learned system stores official, reviewed lessons from programmes/projects. Each lesson links an original driving event with recommendations intended to change training, best practice, policy or procedure.

### Native structure

A failure log and a lesson are different objects:

`FailureEvent = what_happened`.

`Lesson = (driving_event, causal_interpretation, evidence/review, recommendation, applicability_scope, institutional_uptake)`.

### Machine donation

1. **Memory is not learning.** Storing a failure does not establish a transferable correction.
2. **Attribution is reviewable.** The causal story can be wrong even when event history is immutable.
3. **Transfer scope matters.** A recommendation derived from one context needs applicability conditions.
4. **Institutional uptake is a state transition.** A lesson that never changes practice is not equivalent to one embedded into policy/training.
5. **Negative history is valuable only if retrieval connects it to future decisions.**

### Candidate benchmark

`LOG_VS_LESSON`:

- raw historical archive;
- semantic retrieval of similar failures;
- structured lesson record;
- lesson + independently validated causal attribution + applicability checks.

Measure recurrence prevention, false transfer and appropriate `CANNOT_CHECK`.

### Framework disposition

K1 negative knowledge, K3 provenance/dependence, K4 recovery, K6 programme learning.

---

# Cross-practice synthesis

Across baking, repair, checklists, debugging and engineering lessons, the same seven structures recur even though the domains are not equivalent:

1. **State beats schedule.** Nominal time/stage is often only a prior over readiness.
2. **Instructions underdetermine competent action.** Application requires perception, context, tools, timing and correction.
3. **Intermediate checkpoints matter.** Good practice tests the world before irreversible or expensive progression.
4. **Multi-modal evidence is common.** Text alone can omit spatial, sensory or state information essential to action.
5. **Recovery is epistemic competence.** Knowing how to notice and correct deviation is different from executing the happy path.
6. **Failure is not a lesson until attribution and transfer are checked.**
7. **Distributed synchronization matters.** Teams, artifacts and tools jointly carry state.

These structures are general enough to enter the Machine Epistemics donor atlas, but their **authority remains native**. A baking heuristic is not evidence for clinical practice; a surgical checklist is not a theorem about scientific discovery. The transferable object is the abstract distinction, which must be revalidated in the target context.

# Consequences for autonomous discovery

A paper-centric autonomous scientist is structurally biased toward what humans have already made explicit. A broader agent should be able to learn from:

- demonstrations and intermediate states;
- manuals/recipes/checklists plus execution traces;
- incident and repair histories;
- oral testimony with source/custody identity;
- environmental observations;
- artifact/tool interactions;
- negative outcomes and recoveries.

This does **not** imply indiscriminate web ingestion. Every source mode needs a source identity, epistemic access mode, authority ceiling, context and translation-loss record.

# Proposed source-mode tensor extension

For bounded saturation, sample at least:

`Domain × SourceMode × KnowledgeForm × AcquisitionMode × Context × Epoch`.

Where:

- `SourceMode ∈ {scholarly, institutional, manual/recipe, demonstration, oral/testimonial, artifact, incident record, environmental}`;
- `KnowledgeForm ∈ {declarative, causal, procedural, perceptual, tacit/skill, social, normative/authority, negative}`;
- `AcquisitionMode ∈ {reading, observation, experiment, intervention, imitation, dialogue, accident/encounter, play/exploration, participation}`.

# Terminal

`ORDINARY_PRACTICE_PASS_1 = MATERIAL_STRUCTURAL_DONATIONS_FOUND`

`ACADEMIC_PAPER_ONLY_DONOR_UNIVERSE = REJECTED`

`NEW_KERNEL_FAMILY = NOT_JUSTIFIED`

`ISSUE_40_ORDINARY_PRACTICE_REQUIREMENT = FIRST_PASS_SATISFIED_NOT_CLOSURE`

## Public sources inspected

- King Arthur Baking, bread-learning guidance, proofing and doneness articles (state/sensory checkpoints and recovery).
- iFixit, “Creating a Repair Guide” (warnings, tools, multimodal step structure).
- World Health Organization, Surgical Safety Checklist and implementation resources (phase gates, teamwork, local adaptation).
- GitHub Docs, systematic debugging tutor (reproduction, expected/observed, minimal examples, one-change-at-a-time isolation).
- NASA Lessons Learned (driving events, reviewed lessons and recommendations feeding continual improvement).
