# Native Donor Reconstructions — Wave 01

**Status:** mechanism-level reconstructions for research reduction. Exact theorem conditions and strongest successors must still be checked against primary full text before protocol freeze.  
**Rule:** donor objects are stated first in native vocabulary. ORION mapping appears only afterward.

---

# D01 — Blackwell comparison of statistical experiments

## Native problem

Given two experiments about the same unknown state, determine whether every decision maker can do at least as well with one experiment as with the other for every decision problem in a declared class.

## Formal object

For finite state set `Theta`, an experiment is a channel from states to observations. Experiment `E` Blackwell-dominates `F` when there exists a state-independent stochastic garbling kernel `K` such that:

`F = E K`.

Then any decision rule based on `F` can be reproduced by observing `E`, applying `K`, and using the `F` rule. Equivalence is mutual dominance. Approximate comparison motivates deficiency-type quantities.

## What the donor owns

- directional informativeness rather than symmetric similarity;
- decision-relative comparison;
- stochastic simulation/garbling witness;
- partial order/equivalence rather than mandatory total ranking.

## Native limitations

The comparison presumes a common state/decision framework. It does not establish semantic identity, causal transport, authority or cross-generation construct equivalence.

## Candidate V2 absorption

Use Blackwell/deficiency machinery wherever knowledge structures can be expressed as experiments for the same scientific decision family. Do not replace it with cosine distance.

## Known-answer case

One experiment reveals the state exactly; another reports the exact observation after independent bit-flip noise. The exact experiment dominates through the noise kernel; reverse dominance fails unless noise is zero.

## V2 residual question

How should decision comparison interact with changing state semantics, scientific authority, evidence provenance, resources and future responsibilities?

---

# D02 — Rough-set indiscernibility

## Native problem

Characterize a target concept when available attributes cannot distinguish every object.

## Formal object

An information system induces an equivalence relation `IND(B)` from attribute subset `B`. For target set `X`:

- lower approximation: union of equivalence classes wholly contained in `X`;
- upper approximation: union of equivalence classes intersecting `X`;
- boundary: upper minus lower.

Objects in one class are indiscernible relative to `B`, not necessarily identical.

## What the donor owns

- probe/attribute-relative equivalence;
- definite versus possible membership;
- explicit unresolved boundary;
- refinement when attributes are added.

## Native limitations

Classical rough sets use an equivalence induced by an information table; extensions handle tolerance, probability and dominance. They do not by themselves provide scientific evidence authority or intervention semantics.

## Candidate V2 absorption

Represent `UNKNOWN` as a structured indiscernibility class when appropriate, and retain lower/upper bounds instead of one confidence score.

## Known-answer case

Two hypotheses have identical values on registered attributes `q1,q2` but differ on `q3`. Under `{q1,q2}` they are indiscernible; adding `q3` refines the class.

## V2 residual question

Which new query/intervention should be acquired, and when is the missing attribute family itself unavailable or unauthorized?

---

# D03 — Bisimulation and behavioural equivalence

## Native problem

Determine whether two transition systems exhibit the same observable behaviour under every allowed action, despite different internal identities or structures.

## Formal object

A relation `R` is a bisimulation when related states have compatible observations and every transition from either state can be matched by a same-labelled transition to another related pair. Bisimilarity is membership in the greatest such relation.

## What the donor owns

- observer/action-relative behavioural sameness;
- coinductive/fixed-point reasoning;
- explicit distinguishing transition when the relation fails;
- invariance under state renaming.

## Native limitations

The allowed action and observation alphabet must be declared. Bisimilarity is not semantic identity outside that interface and does not handle scientific evidence/authority automatically.

## Candidate V2 absorption

Use exact bisimulation-style solvers for finite scientific-process or workflow structures. Require context/epoch in every behavioural-equivalence receipt.

## Known-answer case

A state that advances to a terminal state is not bisimilar to a same-labelled state that loops forever under `advance`.

## V2 residual question

How do evidence identity, cost, uncertainty, partial observation and protected scientific consequences refine the interface?

---

# D04 — Markov equivalence of causal DAGs

## Native problem

Determine which causal directed acyclic graphs encode the same conditional-independence constraints and therefore cannot be distinguished from observational data alone under standard assumptions.

## Formal object

Two DAGs are observationally Markov equivalent when they share the same undirected skeleton and the same unshielded collider structures. They may differ in edge directions and interventional consequences.

## What the donor owns

- observational equivalence classes of causal structures;
- graph-theoretic characterization;
- separation of observational and interventional identification.

## Native limitations

The result depends on acyclicity and Markov/faithfulness-style assumptions for empirical interpretation. Hidden variables, selection and distributional equivalences require richer formalisms.

## Candidate V2 absorption

Never promote observational equivalence to causal identity. Generate or request interventions only when they can orient decision-relevant distinctions.

## Known-answer case

`A -> B -> C` and `A <- B -> C` have the same skeleton and no unshielded collider, so they are observationally Markov equivalent but structurally distinct.

## V2 residual question

How should intervention selection, resource bounds, authority and representation change be integrated with the equivalence class?

---

# D05 — Computational-mechanics causal states

## Native problem

Construct the minimal predictive state representation of a stochastic process from its observable histories.

## Formal object

Past histories are equivalent when they induce the same conditional distribution over futures. Equivalence classes are causal states. The induced state process yields an epsilon-machine representation under the framework’s conditions.

## What the donor owns

- predictive equivalence defined by future distributions;
- state as sufficient predictive information rather than full history;
- minimality/simplicity questions for predictive representations;
- explicit statistical complexity and entropy-rate objects.

## Native limitations

Predictive equivalence is target/process relative and does not imply causal/interventional equivalence or semantic identity. Estimation from finite data is nontrivial.

## Candidate V2 absorption

Use predictive sufficiency to challenge maximal scientific-state schemas. Retain only distinctions that support declared future decisions, while recording future-query exposure.

## Known-answer case

Two different past strings belonging to the same process regime induce the same next-symbol/future distribution and therefore occupy one predictive state.

## V2 residual question

How should predictive state coexist with evidence provenance, changing objectives, interventions and authority?

---

# D06 — Viability theory

## Native problem

Find states from which at least one admissible trajectory can remain inside constraints over time and possibly reach a target.

## Formal object

For dynamics and constraint set `K`, the viability kernel is the set of initial states for which there exists at least one admissible evolution remaining in `K`. Capture basins add reachability to a target while respecting constraints.

## What the donor owns

- feasibility before optimization;
- hard state/path constraints;
- existence of safe/admissible futures;
- reachability and controlled invariance.

## Native limitations

Generic viability does not encode scientific evidence, claim authority, representation semantics or open-world coverage.

## Candidate V2 absorption

Use viability as the parent geometry for hard-gated scientific reachability. A high immediate score that destroys all valid future paths is inadmissible.

## Known-answer case

An action gives a higher immediate reward but moves outside the safe set; a lower-reward action remains in the viability kernel and preserves access to the target.

## V2 residual question

What makes a trajectory scientifically justified rather than only dynamically feasible?

---

# D07 — Knowledge and learning spaces

## Native problem

Represent feasible knowledge states and learning paths when mastery of items has prerequisite structure and cannot be reduced to one scalar score.

## Formal object

A knowledge structure is a family of feasible subsets of items. Learning-space/antimatroid conditions support accessible, well-graded paths in which items can be added through feasible intermediate states.

## What the donor owns

- set-valued competence/knowledge states;
- prerequisite-sensitive reachability;
- feasible learning sequences;
- adaptive assessment from state uncertainty.

## Native limitations

The objects concern knowledge-item mastery under a domain model, not scientific evidence/provenance/authority generally.

## Candidate V2 absorption

Use learning-space machinery for prerequisite-closed method/skill/obligation states and adaptive probing where the assumptions fit.

## Known-answer case

If item `c` requires `a` or `b`, states containing `c` alone are infeasible while paths through an allowed prerequisite are feasible.

## V2 residual question

Can scientific obligation states be modelled without flattening competing models, representation changes and defeaters?

---

# D08 — Workflow nets and sound processes

## Native problem

Model business/organizational workflows with concurrency, choice and synchronization, and determine whether cases can complete correctly without dead tasks or residual tokens.

## Formal object

A workflow net is a Petri-net structure with a distinguished source and sink and participation of all nodes in the process path. Soundness-style properties require proper completion, option to complete and absence of dead transitions under stated variants.

## What the donor owns

- partial-order/concurrent workflow semantics;
- liveness, deadlock and completion analysis;
- explicit gateways/synchronization;
- event traces and conformance.

## Native limitations

Process soundness is not scientific validity. Data semantics, evidence, uncertainty and authority require extensions.

## Candidate V2 absorption

Use established workflow/process tools to analyse candidate scientific control flows. Keep scientific state and audit history distinct from process tokens alone.

## Known-answer case

Two parallel branches require a join, but one branch is unreachable; the workflow cannot properly complete.

## V2 residual question

How does changing the workflow affect prior scientific closures, provenance and adoption authority?

---

# D09 — Systems-engineering requirements and V&V

## Native problem

Transform stakeholder needs into operational concepts, requirements, architecture, implementation and lifecycle evidence while managing interfaces, risk and change.

## Formal object

Trace networks connect needs, requirements, functions, components/interfaces, verification methods, validation targets and configuration baselines. Verification asks whether specified requirements are met; validation asks whether the resulting system satisfies intended use/need.

## What the donor owns

- recursive requirements decomposition;
- requirements-to-test traceability;
- architecture/interface control;
- trade studies and lifecycle reviews;
- verification/validation separation;
- configuration and change control.

## Native limitations

Scientific problems can be open-world and may require changing the problem formulation, evidence semantics or validation constitution. Standard engineering processes do not automatically solve epistemic authority.

## Candidate V2 absorption

Make ProblemContract traceability and V&V explicit. Do not claim lifecycle decomposition or trace matrices.

## Known-answer case

A system exactly meets a frozen requirement but the requirement omits the actual stakeholder/scientific need: verification passes while validation fails.

## V2 residual question

How can scientific obligations themselves be responsibly diagnosed, reframed and reopened?

---

# D10 — Multiple-fault model-based diagnosis

## Native problem

Explain abnormal observations using models of normal/abnormal component behaviour when one or several faults may coexist and effects can mask or interact.

## Formal object

A diagnosis is a set of component abnormality assumptions consistent with the system description and observations, often restricted to minimal diagnoses. Additional measurements can discriminate candidates.

## What the donor owns

- set-valued competing diagnoses;
- multiple simultaneous faults;
- minimality and consistency;
- discriminating measurements;
- masking/cancellation and interaction pressure.

## Native limitations

Component models and fault languages are assumed; scientific representation/method/framework failure may require changing the diagnostic language itself.

## Candidate V2 absorption

Generalize V1 serial earliest-stage attribution only where native causal topology demands multiple/distributed responsibility. Use exact diagnosis parents for finite worlds.

## Known-answer case

Two faults together reproduce an observation while neither fault alone does; a one-fault solver returns no diagnosis or the wrong cause.

## V2 residual question

When should failure of the diagnosis language itself trigger a higher-level Jump?

---

# D11 — Organizational exploration and exploitation

## Native problem

Balance refinement/use of existing knowledge and routines against exploration of uncertain alternatives, with learning, turnover, socialization and organizational adaptation.

## Formal object

Formal organizational-learning models couple individual beliefs, organizational codes and adaptation rates; excessive exploitation can lock in inferior knowledge while excessive exploration reduces short-run performance and convergence.

## What the donor owns

- exploration/exploitation tension;
- organizational memory/routines;
- path dependence and lock-in;
- multi-level learning dynamics.

## Native limitations

Organizational performance criteria and models do not by themselves establish scientific truth, evidence or protected self-modification.

## Candidate V2 absorption

Treat diversity, option value, routine reuse and framework escalation as parent-owned organizational problems. Evaluate frontier breadth alongside validity and cost.

## Known-answer case

A fast-learning organization converges quickly on an initially common but inferior belief and loses exploratory alternatives that could reveal the better state.

## V2 residual question

Can a scientific solver preserve useful exploration without rewarding useless dispersion or fabricated novelty?

---

# D12 — Structure mapping and C-K design theory

## Native problem

Transfer relational structure across domains and expand design concepts beyond currently known objects/solutions.

## Formal objects

Structure-mapping aligns relational systems while prioritizing higher-order relational consistency over surface attributes. C-K theory separates a concept space of partially undecided propositions from a knowledge space of established propositions and models operators that expand both.

## What the donors own

- analogy based on relational structure;
- mapping correspondences and systematicity;
- concept/knowledge co-expansion;
- design-space expansion beyond known objects.

## Native limitations

Analogies can be false; design propositions are not automatically scientifically valid; evidence, provenance, donor priority, protected evaluators and adoption remain external.

## Candidate V2 absorption

C01 cannot claim cross-domain structural analogy. C05 cannot claim concept-space expansion. The possible residual is donor-faithful scientific reduction, counter-probes, evidence and authority.

## Known-answer case

Two domains share an isomorphic causal/relational pattern despite different surface objects; a third shares vocabulary but not relation structure.

## V2 residual question

Can a machine retrieve remote analogues while preserving native scientific judgments and contracting false novelty?

---

# D13 — CEGAR/CEGIS-style counterexample refinement

## Native problem

Construct a correct model/program/proof by alternating candidate generation, checking and counterexample-guided refinement.

## Formal object

A candidate satisfies a specification or a checker returns a counterexample. Counterexamples refine the abstraction, constraints or candidate search until success, impossibility, resource stop or unresolved status.

## What the donor owns

- propose–verify–counterexample–refine loops;
- exact counterexample steering;
- abstraction refinement;
- grammar/specification-constrained synthesis.

## Native limitations

Correctness depends on the specification and candidate language. A passed checker does not prove the scientific problem or specification was adequate.

## Candidate V2 absorption

Use exact checkers and counterexamples wherever available. Distinguish bad candidate, bad implementation, inadequate model class, inadequate representation and bad specification.

## Known-answer case

An abstraction produces a spurious counterexample; refinement removes it without changing the target specification.

## V2 residual question

When is refinement inside the old language exhausted, justifying method/representation Jump?

---

# D14 — Performative prediction and policy response

## Native problem

Model prediction/evaluation when deploying a model or policy changes the distribution or behaviour being predicted/evaluated.

## Formal object

A distribution map `D(theta)` depends on the deployed model/policy parameter. Performative risk evaluates loss under the induced distribution; stability and convergence depend on response regularity and update dynamics.

## What the donor owns

- endogenous distribution shift from deployment;
- fixed-point/stability questions;
- separation of static and performative risk;
- strategic-response modelling.

## Native limitations

Scientific agenda, authority, evaluator custody and broad institutional response may not fit one parametric response map.

## Candidate V2 absorption

Treat published benchmarks, policies and scientific-agent deployment as interventions on the data-generating/research process. Static evaluation requires an invariance assumption.

## Known-answer case

A classifier changes incentives, causing subjects to alter features and invalidating the pre-deployment conditional relationship.

## V2 residual question

How should protected scientific evaluation remain meaningful when agents and institutions adapt strategically?

---

# D15 — Provenance data models

## Native problem

Represent how entities were generated, used, derived and attributed through activities and agents across systems.

## Formal object

W3C PROV distinguishes entities, activities and agents with typed generation, use, derivation, attribution, association and delegation relations.

## What the donor owns

- graph-based provenance;
- entity/activity/agent separation;
- derivation and attribution;
- cross-system provenance interchange.

## Native limitations

General provenance does not decide semantic comparability, evidence validity, statistical dependence, scientific authority or which old certificates survive a change.

## Candidate V2 absorption

Use PROV-compatible lineage as a base representation. C08 survives only if typed multi-parent inheritance changes transport/reopen decisions beyond general provenance plus dependency analysis.

## Known-answer case

An output entity is generated by an analysis activity that used a dataset and was associated with an agent; deleting the dataset identity makes the derivation incomplete.

## V2 residual question

Which lineage relations are scientifically load-bearing for semantic transport and authority?

---

# Wave 01 donor-product implications

1. **C02 strongest parent product:** relation-specific exact solvers plus one context/receipt interface.
2. **C04 strongest parent product:** systems engineering + adaptive decision/control + blackboard state + diagnosis + CEGAR + workflow/execution + V&V/authority.
3. **C05 strongest parent product:** model criticism/expansion + representation/design change + synthesis + open-ended archives + protected framework revision.
4. **C06 strongest parent product:** V1 transport + psychometric/political linking + metrological traceability + semantic alignment.
5. **C07 strongest parent product:** provenance + graphical/common-cause dependence + meta-analytic effective information + authority gate.
6. **C01 strongest parent product:** native expert search + LBD + analogy/design methods + typed relation solvers.

Every candidate protocol must compare against these products, not isolated strawman parents.