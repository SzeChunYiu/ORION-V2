# Machine-X Demarcation and Frontier Operation V1

**Status:** cross-cutting field/framework clarification after the generative-regime and epistemic-locality hardenings. This document does **not** create a new K0–K6 family, define a universal intelligence metric, rank fields by superiority, or change frozen P-A–P-D endpoints.

## 1. Why this clarification is needed

Terms such as *machine learning*, *machine cognition*, *machine intelligence*, *machine-native intelligence*, *scientific intelligence*, *Machine Epistemics* and *AI for Science* answer different questions. Treating them as one ladder creates two errors:

1. a **category error** — a learning algorithm, a cognitive architecture, a capability evaluation and an application domain are not the same kind of object;
2. a **superiority error** — saying that one object controls or evaluates another does not imply that it is a universally stronger form of intelligence.

Machine Epistemics therefore uses a local terminology contract and tests the scientific residual of that contract. External fields retain their native definitions and authority.

## 2. Operational terminology ledger

| Term | Local role | Primary question | Scientific object |
|---|---|---|---|
| **Machine learning** | learning mechanism | How does a machine update from data, feedback or experience? | update/learning algorithms and objectives |
| **Machine reasoning / planning** | reasoning process | How does a machine derive, search, predict or select actions? | inference, search and planning procedures |
| **Machine cognition** | processing architecture | How are representation, memory, attention, search, planning and communication organized? | organization of information-processing processes |
| **Machine metacognition** | self-monitoring/control mechanism | What can the system estimate about the adequacy, reliability or resource needs of its own processes? | self-models, confidence/failure prediction and control signals |
| **Machine intelligence** | capability profile | How capable is a system under a declared ecology of tasks and constraints? | context-relative performance/capability |
| **Machine-native intelligence** | design orientation | Which useful strategies exploit machine-specific affordances without requiring human imitation? | substrate-oriented architecture/design hypothesis |
| **Machine scientific intelligence** | scientific capability profile | How capable is the system at making progress on scientific problems? | science-scoped capability |
| **Machine Epistemics** | epistemic/scientific control | When may machine-mediated inquiry change commitments, representations, methods, problems, evaluators or evidence state? | warranted scientific-transition control |
| **AI for Science** | application ecosystem | How are AI methods and systems used in scientific research? | scientific applications, workflows and infrastructures |
| **Agentic/autonomous science** | autonomy/system configuration | How much of a scientific loop is delegated to integrated AI systems? | autonomous or semi-autonomous research systems |

The table is a **working demarcation for this programme**, not a claim that all neighboring literatures use one canonical taxonomy.

## 3. No total-order rule

The framework forbids an interpretation such as

```text
Machine Learning < Machine Cognition < Machine Intelligence < Machine Epistemics
```

because the terms do not share one comparison axis.

A machine can be highly capable and epistemically unreliable. A cautious epistemic controller can be reliable yet scientifically weak because its native solvers are poor. A machine-native strategy can be powerful, useless or harmful. A machine-learning system can be the correct minimum-sufficient tool for a scientific problem without activating any higher-level transition machinery.

Useful relations are instead typed:

```text
learning_mechanism --may implement--> cognitive_process
cognitive_architecture --helps realize--> system capability
capability --is evaluated under--> locality/context
machine_native --constrains/designs--> architecture or process
scientific_intelligence --scopes capability to--> scientific tasks
machine_epistemics --governs warranted scientific use/change across--> mechanisms + processes + tools + humans
AI_for_science --contains deployments of--> any of the above
```

`governs` means responsibility for a transition, not ontological or intellectual superiority.

## 4. Capability is context-bound

A machine-intelligence claim must bind its evaluation ecology. One useful interface is

```text
CapabilityContext = (
    environment,
    task_family,
    resource_regime,
    system_boundary,
    substrate_or_interface,
    timescale,
    criterion
)
```

and a capability report is interpreted as

\[
I(\mathcal M\mid E,T,R,B,\Sigma,\tau,Q),
\]

not as a context-free scalar declaration that one system is globally more intelligent.

This is an application of the Epistemic Locality principle. The formalism does not deny that broad or universal intelligence measures may be scientifically useful; it prevents a bounded benchmark result from silently inheriting universal scope.

## 5. Machine Epistemics as a cross-cutting control object

A machine-mediated scientific system may contain learning, reasoning, planning, memory, tools, humans, instruments and machine-native internal representations. Machine Epistemics is concerned with the **scientific transition** caused by their outputs.

For a bounded episode

\[
E_t=(P,S,O,A,R,M,V,X,H,K,\Gamma,\Pi),
\]

where `Gamma` is optional generative-regime state and `Pi` optional perspective/locality state, the control problem is

\[
(E_t,a_t,x_t)\rightarrow(E_{t+1},\rho_t).
\]

The action may be ordinary:

```text
RETRIEVE
LEARN
REASON
PROVE
SIMULATE
MEASURE
EXPERIMENT
CHALLENGE
```

or may change the space in which solving occurs:

```text
CHANGE_MODEL
CHANGE_REPRESENTATION
CHANGE_PERSPECTIVE
REFORMULATE_PROBLEM
BUILD_TOOL
CHANGE_WORKFLOW
TRANSFORM_REGIME
```

or may be `ABSTAIN` / `CANNOT_CHECK` when no warranted route exists.

Machine Epistemics does not own the algorithms implementing these actions. It owns, if the field hypothesis survives, the cross-parent obligations governing when their results may change scientific state.

## 6. Why machine metacognition is not enough

Machine metacognition can estimate quantities such as:

- confidence or calibration;
- method adequacy;
- likely failure class;
- value of additional computation;
- need for external review.

Those signals are useful K1/K4 state. They do not by themselves establish:

- source identity or independence;
- measurement validity;
- evaluator sensitivity;
- causal transport;
- external authority;
- whether another representation preserves an earlier scientific decision;
- whether a changed problem is still the same registered comparison.

Thus metacognition may be a component used by Machine Epistemics, while the latter remains an external scientific-control question about the full evidence/action system.

## 7. Frontier problems: obstruction before solution

A mature problem often supplies the representation, objective, data modality and admissible methods. A frontier problem may not. The missing object can itself be unknown.

The default frontier question is therefore not

> `What is the answer?`

but

> **`What currently prevents a warranted answer, and what is the minimum intervention capable of removing that obstruction?`**

Candidate object:

```text
FrontierObstruction = (
    problem_id,
    witnesses,
    responsibility_hypotheses,
    discriminators,
    lower_level_dispositions
)
```

Possible responsibility classes include missing evidence, invalid evaluator, non-identifiability, model-class inadequacy, representation collision, wrong scale/boundary, method/operator inadequacy, problem misframing, missing tool/measurement channel, resource limitation or authority block.

## 8. Generic FrontierEpisode lifecycle

The existing K0–K6 interfaces and Jump machinery can be composed into a generic frontier loop.

### F0 — bind the scientific object

Freeze the current problem/criterion identity, admissible evidence, scope, system boundary, perspective, resource budget and authority ceiling.

### F1 — construct plural state

Retain competing hypotheses/models, known results, counterexamples, negative history, uncertainties, available methods and unresolved obligations. Do not begin by choosing one narrative.

### F2 — diagnose the obstruction

Seek a witness showing *why* a warranted conclusion is unavailable. Generate responsibility hypotheses and discriminating probes. Failure, poor score or timeout alone is not an obstruction witness.

### F3 — test minimum existing actions first

Use the strongest applicable native and parent methods. Depending on the obstruction, the right action may be ordinary machine learning, retrieval, proof, simulation, measurement or experiment.

If an ordinary method is sufficient, stop escalating.

### F4 — search remote donors when useful

Search mathematical, scientific, engineering, practical, biological, collective, cultural and other source families by mechanism/structure rather than vocabulary alone. Donor capability receives donor credit; only a protected residual can remain an ORION hypothesis.

### F5 — transform the solving space only after witnessed insufficiency

If lower levels are dispositioned and the obstruction remains, propose the minimum responsible Jump:

```text
J2 model/hypothesis expansion
J3 representation / perspective / regime change
J4 problem/objective reformulation
J5 method / tool / instrument invention
J6 workflow / meta-skill revision
J7 framework revision
J8 constitutional proposal requiring external authority
```

The existing `JumpTrigger`, `JumpProposal`, `assess_jump` and `minimum_level` machinery remains authoritative for this routing. `TRANSFORM_REGIME` is an umbrella proposal whose actual Jump level depends on what coordinate changes.

### F6 — predict consequences before protected outcome access

A frontier proposal states prospectively:

- which previously unreachable capability/decision should become reachable;
- which predecessor decisions must remain valid;
- what observation, theorem or counterexample would falsify the transform;
- what resource or authority costs it incurs.

### F7 — execute a decisive probe

Run the proof, experiment, measurement, simulation, learned model or other native evaluation required by the claim. Execution success is not scientific success unless the scientific contract makes it evidential.

### F8 — update selectively

Promote only commitments whose support obligations are discharged. Reopen those whose support failed; retain independently supported conclusions and unresolved alternatives.

### F9 — recurse on the residual

The remaining obstruction becomes the next research atom. Stop when lower-level sufficiency, bounded closure, refutation, non-identifiability, authority block or `CANNOT_CHECK` is the honest terminal.

## 9. Relationship to machine learning on a frontier problem

Machine learning may appear at several points:

- infer a representation or predictive model;
- learn an experiment or search policy;
- estimate a latent state;
- prioritize hypotheses or donors;
- learn a self-model/calibration function;
- generate candidate transformations.

But the Machine-Epistemic question remains:

```text
Why is learning the right action here?
What evidence can train it without leakage/dependence errors?
What decision can its output warrant?
What would show that the representation/objective itself is wrong?
When should learning defer to proof, measurement, experiment, a parent method or abstention?
```

Therefore Machine Epistemics is **higher-order in responsibility**, not a claim of universal performance superiority over machine learning.

## 10. K0–K6 ownership

No new kernel family is required.

- **K0** binds problem, criterion, locality and authority identities.
- **K1** carries plural state, self-model state, optional generative regime and perspective state.
- **K2** tests transport/comparability across representations, scales and contexts.
- **K3** binds evidence, provenance, dependence, lineage and selective revalidation.
- **K4** chooses admissible actions and diagnoses responsibility.
- **K5** owns opportunity/frontier proposals and witnessed minimum escalation.
- **K6** owns protected evaluation, parity, bounded saturation and authority separation.

`src/orion_v2/epistemic_architecture.py` is therefore a research composition layer. It must remain outside the stable kernel until protected evidence shows that a missing kernel obligation exists.

## 11. Verification programme

The demarcation itself is primarily conceptual and can be challenged by literature and hostile field review. The frontier operation has executable consequences that can be tested with existing and staged benchmarks.

### MX10 — taxonomy/category-error tests

Check that implementations do not:

- treat capability as an unconditioned global scalar;
- treat `Machine Epistemics` as a superclass/superiority level;
- turn `machine-native` into an authority claim;
- equate metacognitive confidence with external validation.

These are unit/formal interface checks rather than headline scientific experiments.

### MX20 — hidden-obstruction frontier benchmark

Construct exact/synthetic episodes in which the missing object is hidden. Correct actions vary among:

- ordinary learning/search;
- proof or measurement;
- model expansion;
- representation/perspective change;
- problem reformulation;
- tool/operator construction;
- justified abstention.

Compare direct generation, ML-only optimization, same-model reflection, strongest parent federation and current ORION control. Score obstruction diagnosis, action-family choice, false Jump, missed Jump, justified reach and resource cost.

This study should reuse GR10/EL10 cases where possible rather than create another large independent campaign.

### MX30 — naturalistic frontier transfer

Do not open by default. Only if exact hidden-obstruction tests show a protected residual beyond strongest parents should the same routing claim be tested on fresh scientific frontier cases with independent native evaluation.

## 12. Parent and falsification boundary

This programme is parent-owned by mature work in machine learning, planning, metareasoning, cognitive architectures, intelligence evaluation, AI for Science, autonomous discovery, verification, philosophy of science and scientific methodology.

Useful reference points include:

- Legg & Hutter (2007), *Universal Intelligence: A Definition of Machine Intelligence*, for one explicit environment-relative formalization of machine intelligence;
- Wang et al. (2023), *Scientific discovery in the age of artificial intelligence*, for AI methods across the scientific discovery process;
- Kramer et al. (2026), *Automated Scientific Discovery: From Equation Discovery to Autonomous Discovery Systems*, for the spectrum from discovery methods to autonomous systems;
- contemporary AI-for-science/agentic-science reviews as application/autonomy parents.

The Machine-Epistemics residual contracts if its demarcation is merely vocabulary or if strongest parent composition reproduces all decision-relevant frontier-control behavior at equal or lower cost.

## 13. Current terminal

```text
MACHINE_X_TOTAL_ORDER = REJECTED
MACHINE_LEARNING = ACTION_MECHANISM_PARENT_NOT_SUBORDINATE_FIELD
MACHINE_INTELLIGENCE = CONTEXT_RELATIVE_CAPABILITY_PROFILE
MACHINE_NATIVE_INTELLIGENCE = DESIGN_ORIENTATION_NOT_AUTHORITY
MACHINE_SCIENTIFIC_INTELLIGENCE = SCIENCE_SCOPED_CAPABILITY
MACHINE_EPISTEMICS = CROSS_CUTTING_WARRANTED_TRANSITION_CONTROL_HYPOTHESIS
AI_FOR_SCIENCE = APPLICATION_ECOSYSTEM
FRONTIER_DEFAULT = OBSTRUCTION_FIRST_MINIMUM_SUFFICIENT_INTERVENTION
NEW_KERNEL_FAMILY = NOT_JUSTIFIED
MX10 = CODE_LEVEL_HARDENING
MX20 = REUSE_EXISTING_EXACT_BENCHMARKS_WHERE_POSSIBLE
MX30 = GATED_NOT_AUTHORIZED_BY_DEFAULT
```
