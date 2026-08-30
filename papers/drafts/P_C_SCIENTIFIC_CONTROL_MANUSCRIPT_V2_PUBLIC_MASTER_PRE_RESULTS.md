# Scientific Control by Minimum Sufficient Intervention
## Adaptive Action Selection, Escalation and Abstention in AI-Driven Inquiry

## Abstract

AI research agents are usually evaluated by end-task success, but scientific problem solving also requires deciding *what kind of intervention is warranted*: direct calculation, more evidence, a stronger evaluator, model expansion, representation change, method invention, problem reformulation or abstention. We formulate scientific problem solving as control over a plural state of claims, unresolved obligations, evidence, evaluators and resources rather than as one mandatory reasoning pipeline. The central diagnostic is **minimum sufficient intervention**: among actions capable of resolving a registered blocker while preserving relevant constraints, choose an intervention that is minimal in an episode-specific partial preorder rather than the most elaborate available procedure. The study compares simple/direct control, strongest parent federation, selective bridge control and full integrated control under matched information and resources. It measures capability parity, justified scientific terminals, false completion, over- and under-escalation, selective reopening and resource cost across software repair, hidden-world discovery, diagnosis, formal synthesis and governed scientific tasks. Simple methods, parent composition, abstention and component contraction are predeclared possible winners.

## 1. Introduction

A scientific problem-solving system must decide more than *what answer to output*. It must decide whether the target is currently identifiable, what evidence is missing, whether a tool actually executed, whether an evaluator can detect the relevant failure, whether a model is inadequate, whether the current representation is too coarse, and whether the appropriate next move is to search, measure, prove, reformulate or stop.

The same observable symptom can require different interventions. A failed simulation may reflect code execution, numerical failure, model mismatch or insufficient resources. Conflicting evidence may reflect hidden dependence, measurement error or real scientific ambiguity. Failure to solve a formal problem may justify another search action, a counterexample, a stronger method, a representation change—or no scientific conclusion because the current evidence cannot distinguish the alternatives.

Modern AI-scientist and autonomous-research systems already use planning, reflection, retrieval, tool routing, experiment selection and iterative revision. The present paper does not claim that adaptive control is new or that contemporary systems are rigid pipelines. It asks a narrower question:

> **Can scientific agents improve justified outcomes by diagnosing the current blocker and selecting the smallest sufficient intervention, while preserving existing capability and avoiding unnecessary escalation?**

This framing turns scientific problem solving into a control problem over unresolved responsibility. The candidate system may choose direct/native methods, a federation of mature parent methods, selective interfield control, a more integrated scientific-state controller, or abstention. Full integration is therefore one regime, not the presumed winner.

The paper contributes an operational scientific-control object, an episode-relative partial preorder over interventions, explicit over- and under-escalation measures, parity and simple-task non-regression gates, and a protected comparison against strong direct and parent-composed adaptive controls. Conceptual and formalism change are included only as late actions after lower-level insufficiency has been established.

## 2. Relation to prior work

Several parent fields already formalize action selection under uncertainty and computational limits. Bayesian experimental design and active learning choose informative observations. Metareasoning and value-of-information/computation methods decide which computation or query is worth performing. POMDPs and robust control optimize actions over uncertain state. Diagnosis and truth-maintenance systems identify responsibility for inconsistency. CEGIS/CEGAR and theorem-proving systems iteratively refine candidate solutions. Modern AI-scientist and laboratory-agent systems combine planning, retrieval, tools, experiments and revision.

These parents set the claim ceiling. The present paper does not introduce uncertainty-aware control, planning, tool use, self-reflection, experiment selection or model search. Its possible residual is a **scientific evaluation/control problem** in which the action family itself may need to change and success is judged by the validity of the terminal, the sufficiency of the intervention and the preservation of earlier valid commitments.

The strongest null is that a direct/simple method or an information-matched composition of existing controls already makes the same decisions at lower cost. In that case explicit integrated scientific-state control is unnecessary for the tested scope.

## 3. Scientific episodes and obligations

Represent a bounded scientific episode as

\[
E=(P,S,O,A,R,M,V,X,H,K),
\]

where \(P\) is the problem and criterion, \(S\) a plural scientific state, \(O\) unresolved obligations or blockers, \(A\) admissible action families, \(R\) resources, \(M\) evidence/provenance/dependence and memory, \(V\) evaluators or oracles, \(X\) observations and action results, \(H\) append-only history and \(K\) an external authority boundary.

An action produces an observation or candidate transformation. Execution alone does not turn the action into truth. For example, successful code execution does not establish that the scientific model is adequate; a proof does not validate an empirical specification; a retrieved source does not establish correct claim binding.

The controller chooses a next action or terminal while preserving the registered problem, valid evidence lineage and relevant earlier commitments.

## 4. Blocker classes

The evaluation uses typed blockers so that intervention quality can be scored. Representative classes include:

- execution failure;
- missing evidence;
- evaluator inadequacy;
- non-identifiability;
- model or hypothesis inadequacy;
- representation too coarse;
- method inadequacy;
- problem or criterion misframing;
- resource limitation;
- unavailable authority.

These labels are benchmark/evaluation objects rather than a universal ontology of scientific difficulty. Real episodes can involve multiple blockers or uncertainty about the blocker itself.

The distinction matters because different blockers imply different actions. Missing evidence should not be “solved” by more internal reasoning. An inadequate evaluator should not be treated as evidence against the hypothesis it failed to test. A representation collision calls for a missing distinction, not automatically a new formalism.

## 5. Action families and regimes

The admissible action space can include direct calculation, source checking, execution verification, measurement, counterexample construction, evaluator strengthening, hypothesis expansion, remote-donor search, representation change, method/instrument change, problem reformulation, resource allocation, delegation and abstention.

Let pre-outcome episode features be \(z\). A contextual regime policy may choose

\[
\pi(z)\in\{\mathrm{SIMPLE},F0,F1,F2,\mathrm{ABSTAIN}\}.
\]

Here `SIMPLE` denotes a direct or native low-overhead solution, \(F0\) the strongest parent federation, \(F1\) selective bridge control, \(F2\) the full integrated controller and `ABSTAIN` a justified refusal or defer decision.

The regime policy is evaluated on held-out episodes. Routing chosen after observing the answer is not evidence of adaptive control.

Where a calibrated decision model is scientifically justified, an action \(a\) can be evaluated by expected reduction in registered decision loss net of resource cost,

\[
\operatorname{EVI}(a)
=
\mathbb E[L(d\mid S)-L(d\mid S,X_a)]-\lambda C(a).
\]

When the probabilities or utilities required by that expression are not justified, the system must use an appropriate robust/adaptive parent policy rather than manufacture calibrated numbers.

## 6. Minimum sufficient intervention

The paper does not assume one total ladder from “simple” to “creative.” Different interventions can change different scientific coordinates and may be incomparable.

For episode \(E\), let \(A_E\) be the available interventions. Define a prospectively specified preorder

\[
a\preceq_E b
\]

when intervention \(a\) changes no more of the registered scientific state than \(b\). This order may be partial. For example, obtaining a new measurement and switching to a stronger proof method can be incomparable.

Let

\[
\mathcal F(E)\subseteq A_E
\]

be the set of interventions that the known-answer construction or independent adjudication identifies as sufficient to discharge the registered blocker without violating protected constraints. Define

\[
\operatorname{MinSuff}(E)
=
\{a\in\mathcal F(E):
\nexists b\in\mathcal F(E)\text{ with }b\prec_E a\}.
\]

The controller is minimum-sufficient on an episode when its selected action belongs to this set. The evaluation oracle may know \(\mathcal F(E)\); the agent is not assumed to know it online.

### 6.1 Over-escalation

An intervention over-escalates when it is sufficient but is strictly dominated by a smaller sufficient intervention. This detects systems that solve simple cases by activating expensive or scientifically disruptive machinery unnecessarily.

### 6.2 Under-escalation

An intervention under-escalates when the chosen action cannot resolve the registered blocker despite an available sufficient intervention and the system fails to change course.

### 6.3 Appropriate abstention

If no admissible intervention can support a justified decision under the available evidence, resources or authority, abstention or `CANNOT_CHECK` is correct rather than a failure to be creative.

### 6.4 Incomparable sufficient actions

When several interventions are minimal but incomparable, the evaluation reports the Pareto set and resource consequences instead of forcing one ordinal “level.”

## 7. Conceptual and formalism change as late escalation

Representation change can be necessary when the current representation merges cases that require different registered judgments. A representation collision is evidence that the current state description is too coarse for that decision family; it is not evidence that a new theory is required.

The evaluation therefore searches in the following order:

1. apply the strongest existing parent method;
2. seek a missing observation or variable;
3. add a local scope condition or repair;
4. change representation;
5. only then consider a new primitive, relation, operation, axiom or calculus.

A proposed concept or formalism change must identify the blocker, preserve valid predecessor cases or state its losses, recover the predecessor in its valid scope, improve a held-out decision or establish formal necessity, and survive counterexample search.

False formalism invention is counted as over-escalation rather than creativity.

### 7.1 Regime transformation as a bounded umbrella action

The same logic applies when the insufficiency is broader than one concept or formalism. For prospective work, a `TRANSFORM_REGIME` proposal can bind a change to the current representation language, generative rules, operator repertoire, active constraints, problem portfolio, traversal policy, coordination pattern or tool/affordance environment. This is an interface description, not a new algorithm or mandatory component.

A regime transform is warranted only when the predecessor repertoire is demonstrably insufficient for a registered obligation and the successor makes a capability, discriminator or scientific decision newly reachable while preserving protected predecessor competence or explicitly documenting the loss. Random novelty, a more elaborate workflow or similarity to a famous historical invention is not evidence of sufficiency.

This extension does **not** alter the present paper's frozen primary endpoints, comparator regimes or Results order. A result-bearing claim that explicit regime-transform control improves scientific decisions requires a separate prospective transfer study after an exact synthetic benchmark and strongest-parent comparison. Until then, regime transformation is a clarification of the existing representation/method/instrument/problem action families, and false invention remains over-escalation.

### 7.2 Perspective change and local sufficiency

Minimum sufficiency is also relative to the registered **perspective**. A method can be sufficient at one environmental distribution, system boundary, organizational scale, timescale or resource regime and insufficient at another. When the current frame itself is a witnessed blocker, a parent-owned `CHANGE_PERSPECTIVE`, `CHANGE_BOUNDARY` or `CHANGE_SCALE` proposal may therefore be admissible.

This does not create a universal “overview” stage. The controller should change perspective only when a registered discriminator or obligation depends on the frame. If two admissible frames support different decisions, the correct terminal may be `PERSPECTIVE_DEPENDENCE` plus explicit scope rather than a globally ranked winner. Conversely, manufacturing perspective dependence on invariant cases is an error.

The present paper's endpoints remain unchanged. A separate low-cost exact verification study tests whether explicit locality/perspective binding reduces false universalization or wrong method routing beyond existing context-conditioned parents before it can become a result-bearing P-C mechanism.

## 8. Study design

The evaluation combines task families in which different blocker/action types are genuinely required, including software repair, hidden-world discovery, multi-fault diagnosis, formal synthesis and governed scientific decisions. Some cases are deliberately simple so that activating a larger controller can be measured as unnecessary work.

The primary independent unit is the registered episode or task. Repeated model calls and seeds are nested execution variability, not additional scientific cases.

### 8.1 Comparator regimes

All conditions receive matched solver-visible information and prospectively specified resource/evaluator access. The principal comparators are:

- direct/simple methods;
- strongest native/parent federation \(F0\);
- selective bridge control \(F1\) where applicable;
- full integrated control \(F2\);
- a contextual regime selector;
- frozen V1 capabilities on the parity registry;
- modern adaptive agent/scientist baselines where the registered task surface permits fair comparison.

### 8.2 Capability parity

A new control architecture is not credited for solving new cases if it silently loses capabilities already possessed by the frozen predecessor. The parity suite is therefore non-compensatory: a failed required cell cannot be averaged away by stronger performance elsewhere.

### 8.3 Outcome terminals

The evaluation distinguishes validated solution, bounded/partial result, refutation, non-identifiability, more evidence required, execution or evaluator failure, representation/method transition, resource defer, authority block and `CANNOT_CHECK`. A single “success” label would hide scientifically different outcomes.

## 9. Evaluation

The primary outcomes are:

- justified scientific-terminal correctness;
- critical false-completion rate;
- `CANNOT_CHECK` calibration;
- V1 capability parity;
- minimum-sufficient-intervention correctness;
- over-escalation;
- under-escalation;
- selective reopening/preservation where applicable;
- resource-adjusted performance;
- component/drag effects.

Task-family heterogeneity and decision-changing failures remain visible. Repeated stochastic runs are not treated as independent tasks, and multiplicity follows the prospectively frozen family/endpoint plan.

## 10. Results

**Authoring placeholder — blocks arXiv release until receipt-bound Results are inserted.**

The final Results section will follow this evidence sequence:

1. **Frozen capability parity.** Establish whether the candidate preserves all required predecessor capabilities.
2. **Simple-case control.** Test whether direct/native methods remain preferred on tasks where escalation is unnecessary.
3. **Protected scientific-control benchmark.** Compare justified terminals and critical false completion across regimes.
4. **Minimum sufficient intervention.** Report under-, over- and correct escalation relative to the episode partial preorder.
5. **Component and drag analysis.** Identify which parts change decisions and which add cost without benefit.
6. **Resource and task-family heterogeneity.** Report cost curves and where any effect recurs or fails.
7. **Adverse/null/parent-win cases.** Keep them in the main scientific interpretation.

The actual terminal is selected only from receipt-bound results.

## 11. Interpretation branches

### Integrated scientific-control residual

Supported only if the full or contextual controller improves justified terminals/intervention choice beyond strong parents while parity and critical-error gates pass at acceptable resource cost.

### Contextual control without F2 superiority

If a selector that often chooses SIMPLE or \(F0\) improves outcomes while always-\(F2\) does not, the scientific result is contextual regime selection—not superiority of the integrated theory.

### Parent or simple control sufficient

If direct/native methods or the strongest parent federation match or exceed the candidate at lower cost, the architecture contracts accordingly.

### Over-control / drag

If explicit state/control adds resource cost, false escalation or false completion without protected benefit, the paper reports that adverse result rather than interpreting extra process as rigor.

### Cannot check

When the benchmark lacks a valid oracle, semantic custody or sufficient evidence, the affected claim remains unresolved.

## 12. Discussion

Scientific agents face a routing problem that ordinary end-task accuracy obscures: what should the system do when the failure mode itself is uncertain? More reasoning, more tools or a richer representation are not universally better. They are useful only when they address the blocker that prevents a justified decision.

A positive result would support minimum-sufficient intervention as an evaluation principle for agentic science. The practical contribution would not be a fixed stage order, but a way to test whether agents choose an intervention commensurate with the problem and preserve prior valid capability.

A contextual-selector result would be equally important. It would show that the useful architecture is one that often declines to invoke its most sophisticated machinery. Such a result would favor adaptive deference to simple/native and parent methods.

A parent-win or drag result would argue that the explicit integrated controller adds insufficient scientific value for the tested tasks. This is an intended falsifier, not a failed manuscript.

Limitations include dependence on the quality of blocker/action adjudication, difficulty ordering heterogeneous interventions, the representativeness of benchmark task families, and the possibility that real scientific episodes contain multiple evolving blockers that cannot be assigned a single minimum intervention. These limitations motivate episode-relative partial orders rather than a universal escalation scale.

## 13. Conclusion

Scientific problem solving is not improved merely by adding more reasoning stages. The relevant question is whether the system identifies what prevents a justified conclusion and chooses a sufficient response without unnecessary disruption or cost.

This paper tests that question through a partial-order notion of minimum sufficient intervention, capability parity, explicit abstention and non-compensatory critical-error gates. Its strongest scientific outcome may be an integrated-control residual, a contextual regime selector, a parent/simple-method win or an adverse over-control result.

The evidence, not the complexity of the controller, determines which interpretation survives.

## Reproducibility and release note

The final public version will bind each task, arm, resource budget, semantic-parity decision, analysis receipt and figure/source-data object to the exact reported Results. Internal workflow identifiers and repository-development history remain outside manuscript-facing prose.
