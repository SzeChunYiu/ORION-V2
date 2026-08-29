# Scientific Problem Solving as Obligation-Driven Control
## Minimum Sufficient Intervention in AI-Assisted Inquiry

## Abstract

AI research agents are increasingly capable of literature search, planning, reflection, tool construction, experiment execution and end-to-end research automation. The remaining control problem is narrower: **what kind of intervention is scientifically warranted next?** A failed simulation, missing result or conflicting observation can call for more evidence, a stronger evaluator, model expansion, representation change, method change, problem reformulation or abstention. We formulate scientific problem solving as control over unresolved obligations and compare an explicit controller with simple methods, strongest parent federation, modern adaptive AI-scientist systems and a frozen predecessor under matched non-compensatory evaluation. The central diagnostic is **minimum sufficient intervention**: among interventions capable of resolving the registered blocker while preserving protected constraints, choose a minimal element of a prospectively defined partial preorder rather than the most elaborate procedure available. The study measures parity, justified-terminal rate, false completion, over- and under-intervention, selective reopening and resource cost across software, hidden-world, formal and governed scientific tasks. Current adaptive AI-scientist systems are treated as strong parents, not strawmen. Simple control, predecessor parity, parent sufficiency and component contraction are all prespecified outcomes.

## 1. Introduction

A scientific problem-solving system must do more than produce an answer. It must decide whether an answer is currently identifiable, whether a tool actually executed, which evidence is missing, whether an evaluator can detect the relevant failure, whether the model is inadequate, whether the current representation is too coarse, and when changing the problem or method is justified.

Many of these ingredients are mature. Computational metareasoning studies how to allocate reasoning effort [@russell1991metareasoning]. Bayesian experimental design and active learning choose information-gathering actions [@chaloner1995design; @settles2009active]. Partially observed control formalizes decision making through information states [@smallwood1973optimal]. Truth-maintenance and diagnosis systems track changing commitments and failure explanations [@doyle1979tms; @dekleer1986atms; @reiter1987diagnosis], while counterexample-guided refinement formalizes iterative repair in verification [@clarke2000cegar].

Contemporary AI-scientist systems are also adaptive rather than simple fixed pipelines. The AI Scientist automates much of the research lifecycle [@lu2026aiscientist]. Robin links literature, hypotheses and experimental data analysis [@ghareeb2026robin]. Co-Scientist uses generation, critique, ranking and evolutionary refinement [@gottweis2026coscientist]. SPARK constructs and evaluates analytical tools for pathology [@trost2026spark], and an agentic X-ray scientist has demonstrated adaptive operation on a real synchrotron beamline [@chen2026xray].

Accordingly, this paper does **not** test whether agents can plan, reflect, use tools or automate research workflows. It tests a stricter question:

> **Does an explicit scientific-control layer improve justified terminal and intervention decisions beyond strong adaptive parent systems, while preserving simple/native cases and avoiding unnecessary escalation?**

The null is strong. If a simple controller or strongest parent federation matches the integrated control layer at lower cost, no special orchestration mechanism is warranted.

## 2. Scientific episode

Represent a bounded scientific episode as

\[
E=(P,S,O,A,R,M,V,X,H,K),
\]

where `P` is the problem/criterion contract, `S` plural scientific alternatives/state, `O` unresolved obligations, `A` admissible action families, `R` resource state, `M` evidence/provenance/dependence/memory, `V` evaluators or validation contracts, `X` observations/action results, `H` append-only history and `K` external authority constraints.

An action produces an observation or candidate transformation. It does not create truth merely because a tool returned successfully.

The controller selects either a next action or a scientifically typed terminal.

## 3. Registered blocker classes

Benchmark cases specify the blocker needed to score intervention quality. Representative classes include:

- execution failure;
- missing evidence;
- evaluator inadequacy;
- non-identifiability;
- model/hypothesis inadequacy;
- representation too coarse;
- method inadequacy;
- problem/criterion misframing;
- resource limitation;
- authority unavailable.

These are evaluation labels, not a claim that all scientific difficulty decomposes uniquely into this ontology.

## 4. Action families

The candidate controller can choose among:

- direct solve/calculation;
- retrieve/source-check;
- reproduce/verify execution;
- obtain observation/measurement;
- construct counterexample or falsifying probe;
- strengthen evaluator/oracle;
- compare/expand models or hypotheses;
- search a remote donor/parent;
- change representation/concept;
- change method/instrument;
- reformulate the problem/criterion;
- allocate resources or delegate;
- propose a new research opportunity;
- defer/abstain/`CANNOT_CHECK`.

Opportunity discovery is therefore treated as one action family inside scientific control rather than a separate paper claim unless prospective value is independently established.

## 5. Contextual regime selection

Let pre-outcome episode features be `z`. A policy chooses among

\[
\pi(z)\in\{\mathrm{SIMPLE},F0,F1,F2,\mathrm{ABSTAIN}\},
\]

where `SIMPLE` is direct/native low-overhead control, `F0` the strongest parent federation, `F1` selective interfield bridging, `F2` the full candidate integrated controller and `ABSTAIN` a justified no-action state.

The policy is frozen before held-out outcomes. Always-SIMPLE, always-F0 and always-F2 are explicit controls.

Where calibrated probabilities/utilities are scientifically warranted, an action can be assessed by expected decision-loss reduction net of cost. When such probabilities are not justified, the controller must use robust/adaptive parent methods rather than manufacture numerical confidence.

## 6. Minimum sufficient intervention

A single global ladder from “simple” to “advanced” is not assumed.

For episode `E`, let `A_E` be admissible interventions. Define a prospectively registered preorder

\[
a\preceq_E b
\]

when `a` changes no more scientific structure than `b` relative to the registered episode coordinates. The relation can be partial: a new measurement and a new theorem-proving method can be incomparable.

Let

\[
\mathcal F(E)\subseteq A_E
\]

be the set of interventions known by the benchmark oracle or protected adjudication to discharge the registered blocker without violating protected constraints. Define

\[
\operatorname{MinSuff}(E)=
\{a\in\mathcal F(E):\nexists b\in\mathcal F(E)\text{ with }b\prec_E a\}.
\]

A selected action is minimum-sufficient when it belongs to this set.

The system is **not** assumed to know `F(E)` online. It is an evaluation object used on known-answer or adjudicated cases.

### 6.1 Error classes

**Over-intervention:** the chosen action is sufficient but strictly dominated by a smaller sufficient intervention.

**Under-intervention:** the selected action cannot resolve the blocker despite an available sufficient action under the registered resources.

**Appropriate abstention:** if no admissible sufficient action exists, `CANNOT_CHECK` or defer can be correct.

**Incomparable minima:** when several sufficient interventions are minimal but incomparable, report a Pareto set rather than forcing one “correct level.”

## 7. Concept and formalism change

Representation or concept change is justified only after lower-level insufficiency is witnessed. A proposed change must identify the motivating collision/blocker, preserve earlier valid cases or state the loss, recover the predecessor within its valid scope, improve a frozen decision/prediction or establish checked formal necessity, and survive counterexample search.

Formalism genesis is later still. The registered search order is:

```text
existing parent formalism
-> missing observation/variable
-> local scope repair
-> representation change
-> candidate new primitive/relation/operation/axiom/calculus
```

False formalism invention is over-intervention.

## 8. Benchmark and comparators

The study spans tasks such as software repair, hidden-world discovery, multi-fault diagnosis, formal synthesis and governed scientific decisions. Cases include simple tasks, cases where a mature parent is sufficient, cases with missing evidence, representation collisions, evaluator failures and tasks requiring abstention.

Comparator families include:

- direct/simple control;
- strongest parent federation;
- frozen predecessor architecture;
- contextual controller without full state;
- full candidate controller;
- current end-to-end or multi-agent scientific systems as strong practical parents [@lu2026aiscientist; @ghareeb2026robin; @gottweis2026coscientist; @trost2026spark; @chen2026xray].

Comparisons are matched on candidate-visible information, tools and resource accounting. A larger controller does not earn credit merely by making more calls.

## 9. Outcomes

Primary scientific outcomes are:

1. critical parity/non-regression against the frozen predecessor;
2. justified-terminal accuracy;
3. critical false-completion rate;
4. correct blocker diagnosis;
5. minimum-sufficient intervention rate;
6. over-intervention and under-intervention rates;
7. correct abstention/`CANNOT_CHECK` calibration;
8. selective reopening where dependencies are registered;
9. resource cost and Pareto efficiency.

The independent unit is the registered task/case, not an internal model call or repeated sample.

## 10. Results

**[RESULTS BLOCK — populate only from frozen P-C receipts.]**

Main Results must be reported in this order:

1. critical V1 parity/non-regression;
2. performance on simple/native controls;
3. justified scientific outcomes versus strongest parents;
4. minimum-sufficient intervention behaviour;
5. false completion and abstention;
6. resource Pareto;
7. component heterogeneity and contraction decisions.

Allowed result terminals include bounded integrated-control residual, strongest-parent sufficiency, simple-control sufficiency, parity failure, over-intervention without outcome gain, component-only residual and `CANNOT_CHECK`.

A paper cannot lead with aggregate success if critical parity fails.

## 11. Interpretation branches

A positive result would support a bounded control claim: explicit scientific state/obligation management changes justified intervention or terminal decisions beyond strong adaptive parents while preserving predecessor capability and simple cases.

If F0 or another parent matches the full controller, use that parent. If always-SIMPLE matches on the tested tasks, the complexity is unnecessary. If aggregate outcomes improve only by spending materially more resources without a Pareto gain, the claimed scientific-control residual contracts.

If one component helps while others drag, keep only that component. The paper is designed to permit the integrated architecture to shrink.

## 12. Limitations

Minimum sufficiency is relative to the registered intervention preorder, available evidence and benchmark adjudication. Different scientific contexts can legitimately induce different partial orders. Known-answer tasks may be easier to score than frontier research. Blocker labels can be ambiguous or multi-causal. Resource costs are context-dependent, and human authority cannot be inferred from a machine control state.

Most importantly, a system that produces better benchmark terminals has not thereby established scientific truth. The claims remain bounded to the registered evaluation and evidence.

## 13. Conclusion

Modern AI-scientist systems already plan, reflect, construct tools, analyse experiments and operate physical instruments [@lu2026aiscientist; @ghareeb2026robin; @gottweis2026coscientist; @trost2026spark; @chen2026xray]. The remaining question is not whether an agent can execute a longer workflow. It is whether it can choose **the right kind of scientific intervention**, stop when enough has been done, and abstain when the problem is not currently resolvable.

This study tests that control problem under strong parent and parity constraints. If an explicit obligation-driven controller adds no protected decision value, it should contract. If it does, the residual is about scientific control—not generic agent autonomy.

## Transparency

Large language model tools contributed materially to literature discovery, formalization, critique, software and drafting. AI systems are not authors. Human authors must inspect the protected receipts, direct-parent literature and final claims before public release.

## Bibliography source

Use `papers/primary/PRIMARY_PAPERS_REFERENCES_V1.bib`. Refresh all 2026 source statuses before arXiv and journal release.
