# Cognitive Science Omission Pass V2

**Status:** second changed-vocabulary omission pass for issue #40. It asks which mechanisms remain absent after the first metacognition, memory, attention, skill and serendipity pass. Material additions were found. No new kernel family is admitted.

## Review cell

- cognitive neuroscience / memory;
- learning and developmental cognition;
- social/collective cognition;
- reinforcement learning and habit;
- creativity/incubation;
- hostile machine-learning/control reduction.

Every empirical result is treated as bounded to its design. Human findings are donors and falsifiers, not proof that a machine should imitate human cognition.

---

## 1. Retrieval can change memory: immutable history must be separated from revisable working memory

Nader, Schafe and LeDoux (Nature, 2000; DOI `10.1038/35021052`) showed in a fear-learning model that reactivated consolidated memories could return to a labile state requiring protein synthesis for later retention. The scientific claim is bounded to the experimental paradigm; it does not imply that all recall freely rewrites every memory.

### Machine implication

A learning system needs at least three different memory identities:

- **Archive history** — immutable scientific/evidence receipts;
- **working retrieval structure** — mutable indices, summaries and associations used to access history;
- **reconsolidated hypothesis/skill state** — a revised model created after retrieval and new evidence.

The architecture must permit learning and reorganization without rewriting what evidence originally existed or what the system originally predicted.

Candidate object:

`MemoryRevisionReceipt = (archive_roots, retrieved_items, new_evidence, working_state_before, working_state_after, claims_changed, support_revalidated, archive_unchanged)`.

Candidate failure:

`HISTORY_RECONSOLIDATION_LAUNDERING` — a revised memory/model silently replaces the historical record and makes the earlier error or criterion disappear.

### Reduction

Absorb into K1 immutable history versus working state and K3 selective revalidation. No neuroscience-specific memory primitive.

---

## 2. Offline incubation can restructure a trained representation—but is not independent evidence

Wagner et al. (Nature, 2004; DOI `10.1038/nature02223`) reported that sleep after initial training increased later discovery of a hidden rule relative to wake controls; sleep did not produce the same effect without initial training. Baird et al. (Psychological Science, 2012; DOI `10.1177/0956797612446024`) found improved performance on previously encountered creativity problems after an undemanding task associated with more mind wandering, relative to several comparison conditions.

### Machine implication

An offline process can reorganize candidate relations, replay unresolved cases or search alternative representations without taking external scientific action.

`IncubationReceipt = (frozen_input_state, no_external_evidence_interval, internal_transformations, candidate_output, dependency_on_prior_training, required_external_test)`.

The output is proposal-only. The machine may not count internal recombination, sleep-like replay or repeated sampling from itself as independent corroboration.

Candidate failures:

- `INCUBATION_SELF_CONFIRMATION` — internally generated agreement is counted as new evidence;
- `RETROSPECTIVE_INSIGHT_STORY` — the system narrates a sudden insight after seeing the answer without a frozen pre-answer candidate;
- `OFFLINE_STATE_DRIFT` — protected commitments change during incubation without a receipt.

### Reduction

Absorb into K4 proposal generation and K3 dependence; benchmark against ordinary search/replay.

---

## 3. Teaching data are selected data and can suppress exploration

Bonawitz et al. (Cognition, 2011; DOI `10.1016/j.cognition.2010.10.001`) found that direct pedagogical demonstration led preschoolers to explore a multifunction toy more narrowly than several non-pedagogical controls. The result is not a universal condemnation of teaching; it shows that learners make inferences about why a teacher selected a demonstration.

### Machine implication

Instruction traces, curated demonstrations, benchmark examples and chain-of-thought exemplars are not i.i.d. samples from the environment. They are selected by a teacher, dataset designer or policy.

Candidate distinctions:

- demonstration of one valid action;
- assertion that the demonstrated set is exhaustive;
- safety-constrained instruction intentionally restricting exploration;
- learner inference of exhaustiveness not actually warranted by the teacher;
- exploration preserved outside the taught scope.

Candidate failure:

`INSTRUCTION_INDUCED_SEARCH_SUPPRESSION`.

### ML study

Compare instruction-only, instruction-plus-explicit-nonexhaustiveness, interrupted/partial demonstration and exploratory controls on discovery of held-out valid functions. Record safety and cost; more exploration is not automatically better.

### Reduction

K3 source/selection model, K4 learning/control and K5 exploration.

---

## 4. Communication can destroy the independence that aggregation requires

Lorenz et al. (PNAS, 2011; DOI `10.1073/pnas.1008636108`) experimentally showed that even mild social influence could narrow opinion diversity and undermine crowd accuracy in estimation tasks. Muchnik, Aral and Taylor (Science, 2013; DOI `10.1126/science.1240466`) used a randomized online experiment to show that prior ratings could create asymmetric herding effects. These are domain-bounded social results, but the structural warning directly applies to multi-agent review.

### Machine implication

Reviewer dependence is dynamic. Agents can begin independently and become dependent after reading one another's reports, a shared editor synthesis or a public benchmark score.

Represent review in phases:

1. frozen blind initial judgement;
2. communication graph and disclosed evidence;
3. revised judgement;
4. editor synthesis.

Candidate object:

`SocialInfluenceReceipt = (initial_judgements, initial_dependencies, communication_edges, information_shared, revised_judgements, diversity_delta, confidence_delta, evidence_delta)`.

Candidate failures:

- `POST_COMMUNICATION_OUTPUTS_COUNTED_AS_INDEPENDENT`;
- `CONFIDENCE_CONVERGENCE_WITHOUT_EVIDENCE_GAIN`;
- `EARLY_ANCHOR_HERDING`;
- `EDITOR_SYNTHESIS_REPLAYED_AS_NEW_REVIEW`.

### Reduction

Strengthen P-D and K3/K6 evaluator custody. Independence must be assessed at the evidence-generation phase, not inferred from the number of final messages.

---

## 5. Collective performance is a system property, not a vote count

Woolley et al. (Science, 2010; DOI `10.1126/science.1193147`) reported a group-level factor across varied tasks in their experimental groups; performance correlated with social sensitivity and more even conversational turn-taking more than with the maximum individual intelligence measure. The result has a specific sample and task ecology and does not establish one universal group-intelligence law.

### Machine implication

A multi-agent system should be evaluated as a coordinated information-processing system. Relevant coordinates can include:

- coverage of distinct evidence/routes;
- communication topology;
- domination/turn-taking or routing concentration;
- shared dependencies;
- uptake of criticism;
- integration loss;
- task heterogeneity.

A larger panel is not necessarily more capable. A homogeneous panel can repeat one error; a diverse panel can also fail if information cannot reach the decision boundary.

Candidate failure:

`PANEL_SIZE_LAUNDERED_AS_COLLECTIVE_INTELLIGENCE`.

### Reduction

Absorb into P-D distributed cognition and P-C system-level evaluation. No scalar collective-intelligence kernel field.

---

## 6. Overtraining can create policies that ignore changed outcomes

Tricomi, Balleine and O'Doherty (European Journal of Neuroscience, 2009; DOI `10.1111/j.1460-9568.2009.06796.x`) reported that extensive training in their human task reduced behavioural sensitivity to outcome devaluation. Habit research more broadly distinguishes goal-directed action from context/cue-driven repetition.

### Machine implication

A successful workflow, prompt, retrieval route or evaluator can become a cached policy that continues after its outcome, criterion or environment changes.

`PolicyHabitReceipt = (policy_identity, training_contexts, repetitions, original_outcome, current_outcome, criterion_epoch, cue_dependencies, revaluation_test, response_change)`.

Candidate failure:

`POLICY_HABIT_OUTLIVED_CONTEXT` — the policy remains active despite a materially changed outcome/criterion and fails a revaluation test.

### ML study

After overtraining a workflow, change the criterion or outcome value. Compare:

- cached policy;
- context/epoch-gated policy;
- periodic outcome-revaluation policy;
- full replanning.

Measure adaptation, unnecessary churn and retained competence.

### Reduction

K4 policy validity/epoch and K6 evaluator/criterion mutation. Parent-owned by habit/model-free-control research.

---

## 7. Counterfactual simulation and imagination must remain proposal state

Human and machine inquiry often considers actions or explanations that were not executed. Counterfactual reasoning, causal models and model-based planning are mature parent fields. The omission is architectural rather than a new psychological claim: a simulated consequence can guide action while remaining distinct from an observation.

Candidate object:

`CounterfactualProposal = (model, assumptions, intervention, predicted_outcome, alternatives, uncertainty, discriminator, observation_status=false)`.

Candidate failure:

`SIMULATION_OBSERVATION_LAUNDERING` — a model-generated counterfactual is entered into the evidence ledger as if the world had produced it.

### Reduction

K1 plural hypothesis state, K2 causal relation, K4 planning and K3 evidence identity. No new component.

---

## 8. Second-order observer effects require a stable negative control

The observer-coupling literature and von Foerster's second-order cybernetics motivate representing the participant observer. But a system that assumes every measurement or publication changes the target becomes unusably conservative.

### Machine implication

Every observer-coupling claim needs:

- a hypothesized causal pathway;
- a pre-action prediction where possible;
- a stable/passive negative control;
- a measured or bounded state change;
- a revalidation consequence.

Candidate failure:

`PERFORMATIVITY_EVERYWHERE` — all evaluator validity is discarded without evidence that the relevant environment changed.

### Reduction

Strengthen P-D stable controls and K6 revalidation rules.

---

# Material additions from this pass

1. `MemoryRevisionReceipt` — working-memory reorganization without archive rewriting.
2. `IncubationReceipt` — offline proposal generation explicitly separated from evidence.
3. `PedagogicalSampleReceipt` — teacher-selected data and exploration suppression.
4. `SocialInfluenceReceipt` — reviewer independence can decay after communication.
5. system-level panel evaluation beyond vote count.
6. `PolicyHabitReceipt` — cached policy/criterion revaluation.
7. `CounterfactualProposal` — simulation is not observation.
8. stable negative controls for observer/performativity claims.

# New benchmark candidates

- `ARCHIVE_HISTORY_VS_MEMORY_REVISION`;
- `INCUBATION_PROPOSAL_NOT_EVIDENCE`;
- `PEDAGOGICAL_SAMPLE_NONEXHAUSTIVENESS`;
- `PRE_REVIEW_INDEPENDENCE_POST_REVIEW_COUPLING`;
- `PANEL_SIZE_VS_INFORMATION_DIVERSITY`;
- `POLICY_HABIT_CONTEXT_EXPIRY`;
- `SIMULATION_NOT_OBSERVATION`;
- `STABLE_OBSERVER_NEGATIVE_CONTROL`.

# Paper propagation

- **P-A:** teacher/curator selection belongs in source ecology and donor-search coverage.
- **P-B:** memory/criterion epochs and policy/procedure context change strengthen transport cases.
- **P-C:** pedagogical search suppression, incubation, habit expiry and counterfactual proposal state become benchmark families.
- **P-D:** pre-communication reviewer independence, herding, panel topology and observer negative controls are material.
- **P-E:** encounter recognition must be evaluated prospectively and separately from hindsight/social popularity.
- **Flagship:** add one bounded point: machine inquiry must control how teaching, communication and memory change its own future search—not merely how it records static evidence.

# Terminal

```text
COGNITIVE_OMISSION_PASS_2 = MATERIAL_ADDITIONS_FOUND
MEMORY_ARCHIVE_SEPARATION = HIGH_PRIORITY
PEDAGOGICAL_SAMPLING = HIGH_PRIORITY
DYNAMIC_REVIEW_DEPENDENCE = HIGH_PRIORITY
POLICY_HABIT_EXPIRY = HIGH_PRIORITY
INCUBATION = PROPOSAL_ONLY_RESEARCH_MODE
COUNTERFACTUAL_EQ_OBSERVATION = REJECTED
NEW_KERNEL_FAMILY = NOT_JUSTIFIED
EXPANDED_HUMAN_KNOWLEDGE_SATURATION = OPEN
```
