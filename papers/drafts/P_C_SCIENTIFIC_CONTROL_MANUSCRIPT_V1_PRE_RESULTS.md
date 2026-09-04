# Scientific Problem Solving as Obligation-Driven Control
## A Protected Test of Minimum Sufficient Escalation in AI-Assisted Inquiry

**Paper ID:** P-C  
**Status:** science/method manuscript complete before protected V1 parity and solver outcomes.  
**Primary target hypothesis:** Nature Machine Intelligence Article.  
**Fallback:** npj Artificial Intelligence Article.  
**Absorbs for current closeout:** P-E frontier opportunity discovery; parts of P-F machine-native control and P-G knowledge-metabolism process.

## Abstract

AI research agents are often evaluated by end-task success, yet scientific problem solving also requires deciding *what kind of intervention is warranted*: direct calculation, more evidence, a stronger evaluator, model expansion, representation change, method invention, problem reformulation or abstention. We formulate a candidate controller over plural scientific state and unresolved obligations rather than one fixed reasoning pipeline. The controller is compared prospectively with direct/simple methods, strongest parent federation, strongest donor-composed adaptive control and frozen V1 under matched non-compensatory evaluation. Its central diagnostic is **minimum sufficient escalation**: among interventions capable of resolving a registered blocker while preserving protected constraints, choose a minimal intervention in a prospectively defined partial order rather than the most elaborate available procedure. The study measures V1 capability parity, justified-terminal rate, false completion, over/under-escalation, selective reopening and resource cost across software repair, hidden-world discovery, multi-fault diagnosis, formal synthesis and governed scientific tasks. The manuscript explicitly allows simple controls, V1 or parent composition to win. Protected numerical outcomes and independent semantic parity judgments remain open.

---

# 1. Introduction

A scientific problem-solving system must do more than produce an answer. It must decide whether an answer is currently identifiable, what evidence is missing, whether a tool actually executed, whether the evaluator can detect the relevant failure, whether a model is inadequate, whether the current representation is too coarse, and when a problem or method should change.

This makes scientific problem solving a **control problem over unresolved responsibility**, not merely a longer reasoning trace.

The same symptom can imply different next actions. A failed simulation can mean code failure, model mismatch or inadequate resources. Conflicting evidence can mean measurement error, dependence or genuine scientific uncertainty. Lack of progress can call for more search, a counterexample, a new observation, a representation change—or no action because the target is not currently checkable.

P-C asks:

> **Does obligation-driven scientific control improve justified scientific outcomes over simple and strongest parent-composed adaptive controls, while preserving frozen capabilities and avoiding unnecessary escalation?**

The null is intentionally strong. Existing agents already use planning, reflection, tool routing, retrieval, experiment selection and adaptive control. If a strongest parent composition matches the candidate under equal information and lower cost, ORION-specific orchestration is redundant.

## Frozen contributions before outcomes

- a plural scientific-state/control object;
- typed blockers and responsibility classes;
- a contextual regime-selection hypothesis;
- a partial-order definition of minimum sufficient escalation;
- explicit false/missed/over-escalation metrics;
- integration of conceptual and formalism change without treating them as default actions;
- parity and simple-task non-regression gates;
- result-independent component contraction rules;
- a protected comparison that permits V1, SIMPLE or parent federation to win.

---

# 2. Parent theories and claim ceiling

P-C is not the first adaptive scientific or agent-control framework.

Relevant parents include:

- Bayesian experimental design and active learning;
- metareasoning and value of computation/information;
- POMDP and belief-state control;
- blackboard/cognitive architectures;
- truth maintenance and diagnosis;
- CEGIS/CEGAR and theorem-proving search;
- model-based systems engineering and fault management;
- workflow/process management;
- planning and adaptive tool-use agents;
- autonomous laboratories and AI-scientist systems;
- robust control and decision making under ambiguity.

P-C therefore does **not** claim:

- that scientific agents are currently fixed pipelines;
- that planning/tool use is new;
- that uncertainty-aware action selection is new;
- that J0–J8 labels are universal scientific natural kinds;
- that more explicit state necessarily improves performance;
- that a task solved by an agent is scientifically validated merely because the workflow completed.

The possible residual is a bounded scientific-control mechanism that improves **justified terminals and intervention choice** beyond strongest parent composition while preserving simple/native cases.

---

# 3. Scientific episode

Let a bounded scientific episode be

\[
E=(P,S,O,A,R,M,V,X,H,K),
\]

where:

- `P` — problem/criterion contract;
- `S` — plural scientific state and alternatives;
- `O` — unresolved obligations/blockers;
- `A` — admissible action families;
- `R` — resource state;
- `M` — evidence/provenance/dependence/memory;
- `V` — evaluators/oracles/validation contracts;
- `X` — observations/action results;
- `H` — append-only history;
- `K` — external authority boundary.

An action creates an observation or candidate transformation; it does not create truth by execution alone.

The controller's job is to choose a next action or terminal while preserving the problem criterion and relevant lineage.

---

# 4. Obligation and blocker classes

The formal state does not require one universal ontology, but the benchmark registers the type of blocker needed to score intervention quality. Representative classes include:

- `EXECUTION_FAILURE`;
- `MISSING_EVIDENCE`;
- `EVALUATOR_INADEQUATE`;
- `NON_IDENTIFIABLE`;
- `MODEL_HYPOTHESIS_INADEQUATE`;
- `REPRESENTATION_TOO_COARSE`;
- `METHOD_INADEQUATE`;
- `PROBLEM_OR_CRITERION_MISFRAMED`;
- `RESOURCE_LIMIT`;
- `AUTHORITY_UNAVAILABLE`.

These are evaluation labels for benchmark cases, not claims that all scientific difficulty decomposes uniquely into this list.

---

# 5. Action families

The candidate controller can choose heterogeneous actions:

- direct solve/calculation;
- retrieve/source-check;
- reproduce/verify execution;
- obtain observation/measurement;
- construct counterexample or falsifying probe;
- strengthen evaluator/oracle;
- compare or expand hypotheses/models;
- search remote donor/parent;
- change representation/concept;
- change method/operator/instrument;
- reformulate problem/criterion;
- allocate resources or delegate;
- propose frontier/opportunity action;
- abstain/defer/`CANNOT_CHECK`.

P-E opportunity discovery is therefore absorbed as a **prospective problem/agenda action family**. It does not become a standalone paper without prospective future-value evidence.

Machine-native internal computation may populate any action family, but its scientific output remains subject to the same external evaluation/authority boundary.

---

# 6. Contextual regime selector

Let pre-outcome episode features be `z`. A regime policy selects

\[
\pi(z)\in
\{\mathrm{SIMPLE},F0,F1,F2,\mathrm{ABSTAIN}\}.
\]

Here:

- `SIMPLE` — direct/native low-overhead solution;
- `F0` — strongest parent federation;
- `F1` — selective bridge/interfield control;
- `F2` — full candidate integrated control;
- `ABSTAIN` — no justified action under current state/resources.

The selector is frozen before held-out outcomes. Post-outcome routing is not evidence.

Primary controls include always-SIMPLE, always-F0 and always-F2.

If calibrated probabilities/utilities are available, a candidate action `a` may be ranked by expected decision-loss reduction net of resource cost,

\[
\mathrm{EVI}(a)
=
\mathbb E[L(d\mid S)-L(d\mid S,X_a)]
-\lambda C(a).
\]

If such quantities are not scientifically warranted, the candidate must use the strongest applicable robust/adaptive parent rather than manufacture probabilities.

---

# 7. Minimum sufficient escalation

A total “more sophisticated” ladder is not assumed.

Let `A_E` be candidate interventions for episode `E`. Define a prospectively registered **intervention preorder**

\[
a\preceq_E b
\]

when `a` changes no more scientific structure than `b` relative to the registered episode coordinates. The order may be partial: a new measurement and a new theorem-proving method can be incomparable.

Let

\[
\mathcal F(E)
\subseteq A_E
\]

be the set of actions known by the benchmark oracle or protected adjudication to be sufficient to discharge the registered blocker without violating protected constraints.

The **minimum sufficient set** is

\[
\mathrm{MinSuff}(E)
=
\{a\in\mathcal F(E):
\nexists b\in\mathcal F(E)
\text{ with } b\prec_E a\}.
\]

A selected action is minimum-sufficient when it belongs to this set.

This definition does not assert that the agent can know `F(E)` online. `F(E)` is an evaluation object on known-answer or adjudicated cases.

## 7.1 Escalation metrics

### False/over escalation

The selected intervention is scientifically sufficient but is dominated by a strictly smaller sufficient intervention:

\[
a_{sel}\in\mathcal F(E),
\quad
\exists b\in\mathcal F(E):b\prec_E a_{sel}.
\]

### Missed escalation / under-intervention

The chosen action cannot discharge the blocker and the system fails to move to a sufficient family despite available evidence/resources.

### Appropriate abstention

If `F(E)` is empty under the registered information/resources/authority, `CANNOT_CHECK` or defer may be the correct terminal.

### Incomparable sufficient actions

When several minimal sufficient actions are incomparable, report a Pareto set and resource profile rather than forcing one correct level.

---

# 8. Conceptual and formalism escalation

Concept/representation change is warranted only after lower-level insufficiency is witnessed.

Let a concept state be

\[
C_t=(\Sigma_t,R_t,S_t,O_t,I_t,E_t,X_t,P_t,K_t)
\]

with primitives, relations, scope, operational links, invariants, exemplars, counterexamples/anomalies, parents and provenance/authority.

A proposed transition

\[
\tau:C_t\to C_{t+1}
\]

must:

1. identify the blocker/collision motivating change;
2. preserve old-valid hidden cases or explicitly mark losses;
3. recover the predecessor in its valid scope;
4. improve a frozen decision/prediction or establish checked formal necessity;
5. survive counterexample search.

New vocabulary alone earns no credit.

Formalism genesis is later still. The registered search order is:

```text
existing parent formalism
-> one missing observation/variable
-> local scope/patch
-> representation change
-> only then candidate new primitive/relation/operation/axiom/calculus
```

False formalism invention is scored as over-escalation.

---

# 9. Terminal ontology

The controller may return:

- validated solution;
- bounded/partial result;
- refutation;
- non-identifiable;
- more evidence required;
- execution/evaluator failure;
- representation/method transition proposal;
- deferred on resources;
- blocked on authority;
- `CANNOT_CHECK`.

A broad “SUCCESS” label is insufficient for scientific evaluation.

---

# 10. Protected benchmark

## 10.1 V1 parity

All frozen V1 capability cells are evaluated non-compensatorily. A mean improvement cannot hide a lost critical capability.

Four semantic cases require independent blinded evaluator custody before paired output access.

## 10.2 Simple controls

Tasks deliberately solvable by direct/native methods test whether F2 overworks or over-escalates.

## 10.3 Adaptive scientific cases

Families include:

- real software/debugging tasks with executable validation;
- hidden-world discovery;
- multi-fault diagnosis;
- formal synthesis/proof/countermodel tasks;
- causal/scientific-model-control cases;
- governed computational experiments;
- representation-collision cases;
- prospectively frozen expert-owned tasks.

## 10.4 Frontier/problem-selection cases

P-E-style opportunity/problem finding appears as one action family. Without genuine pre-outcome future follow-up, it cannot support an independent opportunity-discovery result.

---

# 11. Experimental arms

Minimum:

- `SIMPLE_DIRECT`;
- `SAME_MODEL_REFLECTION`;
- `F0_PARENT_FEDERATION`;

**Disclosure — the strongest-parent arm is built from this project's own modules.** In the executed sibling studies (ME-X1, ME-X4, FM10) the corresponding strongest-parent arm is not assembled solely from third-party implementations: per its pre-registered information-matching field it holds this project's own typed `orion_v2` modules, at the mechanism's registry visibility and behind the same frozen adjudicator. It is therefore an information-matched **ceiling control** bounding what any faithful composition could reach, not a measurement of prior work; agreement with it is not evidence that published methods suffice.
- strongest donor-composed adaptive solver;
- `F2_FULL`.

Where feasible:

- retrieval-only;
- component removals;
- machine-native proposal/search arm;
- fixed workflow;
- contextual regime selector.

All receive matched or explicitly modeled information, tool and resource budgets.

---

# 12. Primary outcomes

## Scientific quality

- justified-terminal rate;
- critical false-completion rate;
- correct `CANNOT_CHECK`/non-identifiability;
- semantic/native fidelity;
- selective reopening;
- executable/native success where available.

## Escalation

- minimum-sufficient selection rate;
- false/over escalation;
- missed escalation;
- wrong blocker diagnosis;
- unnecessary formalism/representation invention.

## Resources

- tokens/model calls;
- wall time;
- tool calls;
- compute/memory where measurable;
- human minutes;
- implementation burden.

Results are non-compensatory: lower false completion cannot be traded away silently for higher task score, and a quality tie at far higher cost supports contraction.

---

# 13. Component decision rules

After valid matched outcomes, every candidate component receives exactly one disposition:

```text
NECESSARY
PARENT_REPLACEABLE
CONTEXTUAL
REDUNDANT_DRAG
HARMFUL
CANNOT_CHECK
```

A component is not preserved because it has an appealing theoretical role.

If F2 ties F0 but costs more, simplify/parent-replace before further scale-up.

If F2 is worse, use prospectively frozen ablations to localize failure; any repaired successor receives a new run identity.

---

# 14. Analysis plan

The independent unit is the task/case. Repeated seeds are nested.

Report:

- per-cell V1 parity;
- paired terminal outcomes;
- false-completion and `CANNOT_CHECK` calibration;
- resource Pareto fronts;
- escalation confusion tables relative to registered minimal sufficient sets;
- domain/task-family heterogeneity;
- component effects;
- reasonable-specification robustness.

Do not claim universal minimum escalation if the intervention relation is domain-relative or partial.

---

# 15. Results insertion contract

No numerical Results are authorized before protected receipts.

The importer may populate:

1. V1 parity;
2. simple-control non-regression;
3. matched primary outcomes;
4. resource outcomes;
5. escalation outcomes;
6. component dispositions;
7. domain heterogeneity;
8. robustness.

It may not change success criteria or reclassify invalid infrastructure runs as scientific failures/successes.

---

# 16. Outcome-conditioned Discussion branches

## F2 residual survives

Claim only a bounded control residual in the tested domains. Emphasize which decisions changed beyond parent composition and which components were actually necessary/contextual.

## Contextual regime selector wins, always-F2 does not

Conclude that Machine-Epistemic control is **conditional infrastructure**, not a universal architecture. This is a scientifically strong result.

## F0/donor composition matches or wins

Conclude that explicit higher-order orchestration is unnecessary for the tested cases. Preserve useful evaluation/terminal/receipt infrastructure without claiming solver superiority.

## V1 retains critical capability lost by V2

The paper cannot promote V2. Report non-regression failure and either scope/repair prospectively or retain V1 for the affected capability.

## Minimum escalation is not stable across domains

Retain domain-specific partial orders or action policies; do not preserve a universal escalation ladder.

## F2 is harmful/overconservative

Report the failure. A system that avoids false completion by refusing solvable tasks is not automatically scientifically better.

---

# 17. Limitations

1. Scientific-action sufficiency is often hard to know prospectively; benchmark oracle/adjudication is itself a scientific object.
2. Explicit state may add overhead and can create overconservatism.
3. Domain actions need not fit one total escalation order.
4. Human expert tasks can be noisy and dependent.
5. Real physical experimentation has safety/authority constraints beyond computational benchmarks.
6. Machine-native strategies can be useful without being captured by human-interpretable policy features.
7. A controller cannot compensate for missing domain algorithms by bookkeeping alone.

---

# 18. Reproducibility, AI-use and authority

Release frozen protocols, task identities, arm bindings, evaluator custody, resource definitions, exact/native evaluation code, terminal/failure ledger and analysis where licensing permits.

The ORION-V2 programme has used LLMs extensively for literature work, formalization, software generation, critique and drafting. Human authors must independently understand and adopt final claims/results and comply with current venue AI-use rules.

The controller never self-grants publication, institutional or scientific authority.

---

# 19. Current paper terminal

```text
P_C_SCIENCE_CONTENT = COMPLETE_PRE_RESULTS
PC_C1 = ARCHITECTURE/HYPOTHESIS_DEFINED
PC_C2 = BLOCKED_V1_PARITY_CUSTODY_AND_EXECUTION
PC_C3 = BLOCKED_PROTECTED_MATCHED_RESULTS
PC_C4 = FORMALIZED_AS_PARTIAL_ORDER_EVALUATION_OBJECT__EMPIRICAL_STABILITY_BLOCKED
P_E = MERGED_INTO_P_C_UNLESS_REAL_PROSPECTIVE_FOLLOWUP
P_F_CONTROL_SURFACE = MERGED
RESULTS = NOT_YET_AUTHORIZED
PRIMARY_TARGET = NATURE_MACHINE_INTELLIGENCE_ARTICLE_HYPOTHESIS
FALLBACK = NPJ_ARTIFICIAL_INTELLIGENCE_ARTICLE
```

P-C is top-tier eligible only if protected outcomes establish a bounded scientific-control residual without critical parity, false-completion or over-escalation regressions.
