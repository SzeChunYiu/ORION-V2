# Foundation Saturation Pass 02 — Distributed State, Defeasible Argument, Deep Uncertainty and Evidence-to-Decision

**Status:** second unified changed-vocabulary pass under issue #41. This pass found four mature parent lanes that were not explicit in Atlas V1. It therefore records a **material addition**, resets the post-material no-new-coordinate counter to zero, and keeps synthesis blocked. It grants no new kernel coordinate, foundation law, field status or paper identity.

## 1. Search question

What foundations remain invisible if Machine Epistemics is described primarily through epistemology, statistics, control, provenance, cognition and scientific workflow vocabulary?

This pass deliberately changed vocabulary toward:

- replicated state machines, distributed consensus and Byzantine fault tolerance;
- defeasible argumentation, argument attacks, multiple extensions and preferences;
- robust/adaptive decision-making under deep or model uncertainty;
- evidence-grading and evidence-to-decision methodology.

These routes were chosen because they challenge four central ORION intuitions:

1. a controlled scientific transition resembles a replicated state transition;
2. evidence supports claims through defeasible arguments, not only lineage;
3. action selection may occur when probabilities or models are not credibly known;
4. evidence certainty is not the same object as a recommendation or authorized decision.

## 2. Expert review cell and delegation

Six independent roles cross-examined every proposed finding.

1. **Distributed-systems and formal-methods reviewer** — reconstructs ordering, state-machine replication, safety, liveness, fault models, impossibility and recovery.
2. **Argumentation and assurance reviewer** — reconstructs abstract/structured argumentation, strict versus defeasible inference, attack/defeat, preferences and assurance metamodels.
3. **Statistics and model-credibility reviewer** — tests whether new vocabulary is already recovered by workflow, severity, robustness, VVUQ or existing K2–K6 receipts.
4. **Deep-uncertainty decision reviewer** — reconstructs robust decision making, minimax regret, adaptive pathways, signposts, triggers and lock-in.
5. **Evidence-to-decision and institutional-method reviewer** — reconstructs evidence certainty, recommendation strength, values, resources, equity, acceptability, feasibility and contextual adoption.
6. **Hostile parent/editor reviewer** — attempts to contract every finding to mature parents, rejects analogies that do not preserve protected scientific decisions, and prevents lane creation from becoming kernel or paper inflation.

### Deliberation rule

A lane is added only when at least one reviewer identifies a mature native problem that:

- is not explicit enough in Atlas V1 to support reliable parent recovery;
- changes a benchmark, strongest-parent product, non-claim or failure analysis;
- cannot be represented honestly as just another citation inside an existing row.

Adding a lane does **not** imply that ORION owns any mechanism in it.

---

# A. Distributed state consistency is a direct remote parent

## A1. Native problem

Distributed-systems theory asks how multiple processes can maintain a consistent ordered state despite concurrency, delay, crash faults or arbitrary/Byzantine faults.

Lamport's event-ordering work distinguishes causal partial order from imposed total order and shows how ordered requests can implement a distributed state machine. State-machine replication then uses consensus or atomic broadcast so non-faulty deterministic replicas apply the same transition sequence. Paxos, Raft and PBFT solve different variants under different synchrony and fault assumptions.

The FLP result supplies an essential negative parent: in a fully asynchronous deterministic system, consensus cannot guarantee termination in the presence of even one crash failure. Distributed systems therefore separate:

- **safety** — no two correct processes decide inconsistently;
- **liveness/termination** — progress eventually occurs;
- **validity** — the decided value satisfies a protocol-defined input condition;
- **application correctness** — the replicated transition is the right transition for the real task.

## A2. ORION collision

Machine Epistemics uses append-only history, transition receipts, replay identity, multiple agents/evaluators and controlled state change. Those ideas collide directly with:

- causal and total event ordering;
- replicated logs/state machines;
- consensus assumptions and impossibility;
- Byzantine/common-mode faults;
- safety versus liveness separation;
- reconfiguration and recovery.

The scientific residual cannot be "agents agree on a transition" or "all replicas hold the same state." Distributed agreement can reproduce the same scientifically invalid claim perfectly.

## A3. Material donation

Atlas V1 does not expose distributed state consistency as a standalone parent lane. The omission matters because it adds explicit benchmark obligations:

- distinguish **agreement**, **consistency**, **availability**, **validity** and **scientific correctness**;
- state the synchrony and fault model behind any multi-agent consensus claim;
- treat network partition or evaluator unavailability as a possible liveness failure rather than forcing a scientific decision;
- represent common-mode faults when all replicas share one model, dataset, prompt or evaluator;
- test recovery/reconfiguration without silently changing scientific authority;
- allow safe nontermination or `CANNOT_CHECK` when the protocol cannot guarantee progress.

## A4. Candidate benchmark families

### Consensus on a false scientific claim

All replicas receive the same corrupted calibration and agree exactly. Replication safety passes; scientific known-answer validity fails.

### Scientific disagreement with a consistent log

Agents record one ordered evidence history but valid scientific interpretations remain plural. The system must not infer epistemic consensus from log consistency.

### Partition and authority

The authorized evaluator is unavailable. A quorum of lower-authority agents agrees. Expected terminal: no authority promotion.

### Byzantine reviewer

One reviewer sends different conclusions to different peers. Compare naive majority, authenticated replicated protocols and source/dependence-aware evaluation.

### Common-mode model fault

Several "independent" agents are replicas of one defective model. Byzantine tolerance aimed at independent replica faults may not protect against the common cause.

## A5. Reduction

Distributed consensus and state-machine replication are parent-owned implementation methods. The Machine Epistemics residual, if any, is the scientific interface between:

`protocol consistency -> evidence interpretation -> scientific validity -> authority`.

No new kernel coordinate is justified because K0/K1/K3/K4/K6 can represent identity, state, dependence, action and evaluation. But the strongest parent baseline for multi-agent scientific state must now include distributed-systems protocols and impossibility constraints where relevant.

## A6. Disposition

`NEW_ATLAS_LANE = L31_DISTRIBUTED_STATE_CONSENSUS_FAULT_TOLERANCE`

`MECHANISM_OWNERSHIP = DISTRIBUTED_SYSTEMS`

`NEW_KERNEL_COORDINATE = NO`

---

# B. Defeasible argumentation is a direct parent of scientific assurance

## B1. Native problem

Formal argumentation studies how claims can be accepted when arguments attack one another and inference is defeasible rather than monotonic.

Dung's abstract argumentation framework represents arguments and an attack relation, then defines semantics such as grounded, preferred and stable extensions. Different semantics can produce different accepted sets, and several extensions may coexist.

Structured systems such as ASPIC+ recover the internal form of arguments:

- premises;
- strict inference rules;
- defeasible inference rules;
- conclusions;
- attacks on premises, inferences or conclusions;
- preferences that determine whether attacks succeed as defeats.

Assurance-case metamodels such as SACM add structured claims, arguments, evidence and artifact relationships for system assurance.

## B2. ORION collision

Pass 01 identified assurance cases because evidence and provenance do not interpret themselves. The new pressure is deeper:

- multiple internally acceptable argument sets may remain;
- an argument can attack a premise, inference step or conclusion;
- strict and defeasible support must not be conflated;
- hidden preferences can change which argument wins;
- circular or self-supporting argument graphs can look complete;
- formal acceptability does not establish truth of premises or scientific validity.

A `ScientificAssuranceCase` without a native argumentation parent would risk reinventing this field.

## B3. Material donation

Atlas V1 has assurance and social criticism lanes, but not a sufficiently explicit lane for formal argumentation semantics. This matters for:

- criticism uptake;
- competing support families;
- defeaters and counterclaims;
- unresolved plural extensions;
- argument circularity;
- preference/authority separation;
- explaining why a claim is supported rather than merely listing evidence.

## B4. Candidate benchmark families

### Same evidence, different inference rules

Two assurance cases cite identical evidence. One uses a valid domain inference; the other uses an unjustified bridge. Provenance is equal; support validity differs.

### Multiple preferred extensions

Two internally coherent scientific interpretations remain after all attacks. The system must retain plural state rather than select arbitrarily.

### Hidden preference

An evaluator's preference ordering silently determines which argument defeats another. Expected: preference/authority identity must be explicit.

### Circular assurance

Claim A supports B and B supports A through intermediate nodes. The diagram is connected but not independently grounded.

### Defeasible versus strict overreach

A defeasible empirical inference is exported as a strict proof. Expected: authority and modality conservation failure.

### Argument accepted, premise false

The argumentation semantics accept an argument relative to the graph; a known-answer test falsifies its premise. Acceptance is not scientific truth.

## B5. Reduction

Formal and structured argumentation are parent-owned. ORION may require an argument interface or adapter, but does not own attack semantics or defeasible reasoning.

The candidate composition-level question is whether scientific-state transitions require additional binding among:

- argument acceptability;
- evidence/source validity;
- dependence;
- context/transport;
- evaluator custody;
- authority.

That residual must be tested against ASPIC+/SACM/assurance products, not asserted.

## B6. Disposition

`NEW_ATLAS_LANE = L32_FORMAL_DEFEASIBLE_ARGUMENTATION`

`SCIENTIFIC_ASSURANCE_OBJECT = STRONGLY_PARENT_THREATENED`

`NEW_KERNEL_COORDINATE = NO`

---

# C. Decision making under deep uncertainty changes the action-selection parent space

## C1. Native problem

Ordinary decision theory and POMDPs often assume a specified probability model or credal structure over states and outcomes. Deep uncertainty arises when parties do not know or agree on:

- the relevant models;
- probability distributions;
- system boundaries;
- future conditions;
- objectives or trade-offs.

Robust Decision Making (RDM) reverses a forecast-optimize workflow. Candidate strategies are stress-tested across large ensembles of plausible futures; vulnerabilities and trade-offs are identified rather than relying on one best forecast.

Dynamic Adaptive Policy Pathways (DAPP) represents sequences of actions, adaptation tipping points, signposts and triggers. A short-term action can preserve options while monitoring evidence that determines when to switch pathways.

Minimax regret and robust MDP methods optimize worst-case opportunity loss or performance under uncertain models.

## C2. ORION collision

K4/K5 action selection, minimum escalation, exploration and problem-frame change currently rely heavily on:

- expected scientific value;
- probability of adequacy/failure;
- value of computation/information;
- resource-aware control.

These remain valid when probabilities are credible. But deep uncertainty adds different decision objects:

- vulnerability across model ensembles;
- robustness rather than expected optimality;
- regret;
- option preservation;
- lock-in and path dependence;
- monitoring/signposts;
- adaptive triggers;
- objective disagreement.

## C3. Material donation

Atlas V1 includes decision theory, metareasoning, control and frontier policy, but not a distinct deep-uncertainty lane. The omission matters because the strongest P-C/P-E parents may be DMDU methods rather than expected-utility controllers in some scientific programmes.

It also creates a hostile control against premature scientific closure: a system can be unable to identify the correct model yet still choose a reversible, robust action or measurement strategy.

## C4. Candidate benchmark families

### Brittle optimum versus robust alternative

The expected-optimal policy under one model fails catastrophically in plausible alternatives. Compare expected utility, minimax regret and robust/adaptive pathways.

### Option-preserving experiment

One action yields lower immediate information but preserves future instruments/samples; another creates irreversible lock-in.

### Signpost-triggered representation change

A representation remains adequate until a monitored signpost crosses a threshold. Compare static Jump, overreactive Jump and adaptive trigger policies.

### Unknown probabilities, known catastrophic region

Exact probabilities are not credible, but a severe failure region is identified. Test robust constraint handling without fabricated posterior precision.

### Objective disagreement

Several legitimate scientific/institutional objectives remain. The machine can expose Pareto/robust consequences but cannot select the value weights or authority.

### Over-conservatism control

A robust policy wastes resources in a stable well-characterized environment. Contextual activation must beat universal conservatism.

## C5. Reduction

DMDU, robust control, minimax regret and adaptive pathways are mature parent methods. ORION's residual cannot be generic robustness, option value or adaptive planning.

The composition-level question is narrower: can a scientific controller bind robust/adaptive action to evidence identity, representation changes, selective reopening and authority across heterogeneous scientific tasks?

This is a P-C/P-E baseline requirement, not a new law.

## C6. Disposition

`NEW_ATLAS_LANE = L33_DECISION_MAKING_UNDER_DEEP_UNCERTAINTY`

`P_C_P_E_BASELINE_EXPANSION = REQUIRED`

`NEW_KERNEL_COORDINATE = NO`

---

# D. Evidence grading and evidence-to-decision frameworks are a direct authority parent

## D1. Native problem

Evidence-grading systems distinguish confidence in an evidence body from the decision or recommendation made using it.

GRADE separates:

- certainty/quality of evidence;
- magnitude and balance of desirable/undesirable effects;
- values and preferences;
- resource use/cost;
- equity;
- acceptability;
- feasibility;
- recommendation strength or decision.

Evidence-to-Decision (EtD) frameworks make these criteria explicit and support context-specific judgments, justification, monitoring and revision.

The key point is not that GRADE should govern all science. It is a mature operational example of a separation Machine Epistemics often claims abstractly:

`evidence certainty != recommendation != legitimate authority`.

## D2. ORION collision

K3/K6 already preserve evidence and authority ceilings. Pass 02 shows that the parent landscape includes practical decision frameworks with much more detailed separation of:

- evidence certainty;
- effects/benefits/harms;
- thresholds;
- values/preferences;
- resources;
- equity;
- acceptability/feasibility;
- conditional recommendation;
- monitoring/updating.

Low certainty does not mechanically entail "do nothing". A legitimate authority may make a conditional action under low certainty when consequences, values and reversibility justify it. Conversely, high-certainty evidence does not automatically authorize action.

## D3. Material donation

Atlas V1's law/evidence and authority lanes need a distinct evidence-to-decision parent. This changes protected cases for P-D/P-E and the flagship:

- same evidence, different legitimate contexts/values;
- high certainty but no adoption authority;
- low certainty with urgent reversible conditional action;
- strong recommendation based on values/benefits despite moderate evidence;
- no recommendation because values or feasibility remain unresolved;
- machine reports evidence and consequences but cannot choose social values or mandate.

## D4. Candidate benchmark families

### Same evidence, different contexts

Two institutions receive identical evidence but face different resources or baseline risks. Different recommendations can both be legitimate if context and authority are explicit.

### High certainty, no authority

The system has strong evidence but no permission to allocate resources or alter policy.

### Low certainty, conditional action

Potential harm is large and action is reversible. A legitimate decision-maker authorizes monitoring and conditional adoption. The machine records uncertainty and conditions without pretending the evidence became stronger.

### Value-weight ambiguity

Evidence and effects are clear, but stakeholder values differ. Expected terminal: expose conditional consequences/decision frontier, not a self-selected recommendation.

### Feasibility failure

Scientifically effective action is unavailable or infeasible. Evidence remains valid; implementation decision changes.

### Framework ritualization

Completing every EtD cell does not improve decision quality and creates overhead in a simple exact case. Direct control should win.

## D5. Reduction

GRADE/EtD is domain-developed and not a universal scientific constitution. The general separation among evidence, values, feasibility, recommendation and authority is nevertheless a strong parent of Machine Epistemics.

The residual, if any, is whether a domain-neutral machine interface can preserve those separations across sciences without flattening their native decision/authority practices.

## D6. Disposition

`NEW_ATLAS_LANE = L34_EVIDENCE_GRADING_AND_EVIDENCE_TO_DECISION`

`EVIDENCE_AUTHORITY_SEPARATION = STRONG_PARENT_OWNED_EXAMPLE`

`NEW_KERNEL_COORDINATE = NO`

---

# E. Pass-01 lane reconstruction strengthened

Pass 02 also deepened the newly identified Pass-01 lanes rather than merely creating new ones.

## E1. Statistical workflow and computational credibility

### Expanded parent product

A strongest parent product should include:

- Bayesian/statistical workflow with prior/model construction, fitting, predictive checks and sensitivity;
- implementation validation through SBC/posterior SBC when a generative model is available;
- VVUQ/model-credibility frameworks for simulation-based evidence;
- multiverse/specification-curve controls when analytical degrees of freedom are material;
- selection/optional-stopping history.

NASA's model/simulation credibility framework and Sandia's Predictive Capability Maturity Model make the lifecycle nature of modelling credibility explicit: conceptual model, code verification, solution verification, validation and uncertainty/sensitivity must be assessed separately.

### New hostile distinction

`VALID_INFERENCE_IMPLEMENTATION` does not imply `ADEQUATE_SCIENTIFIC_MODEL`, and vice versa.

A Bayesian computation can be calibrated for the coded model while the model is scientifically inappropriate. A scientifically adequate model can be implemented incorrectly.

## E2. Severe testing and sequential validity

The Pass-01 severity lane should include anytime-valid/sequential inference parents. A test used under optional continuation or repeated monitoring cannot inherit fixed-sample validity automatically.

Candidate receipt fields include:

- stopping rule or anytime-valid guarantee;
- test martingale/e-process or alternative justification;
- target error class;
- test quantities/coverage;
- selection history;
- model/prior dependence.

## E3. Robustness and multiverse limits

A multiverse can reveal analytical sensitivity, but only when alternatives are scientifically plausible and the target estimand remains comparable. Including absurd or non-equivalent analyses can manufacture apparent fragility; excluding defensible alternatives can manufacture robustness.

This reinforces P-B context identity and P-D route-level dependence/discordance.

## E4. Law/evidence and burden of proof

Legal evidence scholarship supplies a further separation between probability, informativeness and decision threshold. A high posterior-like probability can result from weak or uninformative evidence, and the availability of further investigation can change whether a decision should be made now.

This is not a universal scientific burden of proof. It is a parent warning that threshold crossing, evidential quality and stopping are different objects.

## E5. MDL and finite approximation

MDL/Kolmogorov-style principles face representation/coding assumptions and computational approximations. Finite approximations can change complexity rankings. Therefore an empirical "simpler representation" claim must bind:

- coding/model class;
- approximation method;
- sample regime;
- compute;
- decision/interface preserved.

Compression remains a strong parent, not truth authority.

---

# F. Cross-review deliberation

## F1. Formal reviewer

**Finding:** distributed systems and formal argumentation are genuine omitted parent lanes.

**Reason:** they contain mature impossibility results, semantics and executable mechanisms, not merely metaphors. They directly threaten multi-agent agreement and assurance claims.

**Contraction:** no new ORION primitive; require adapters/baselines.

## F2. Statistical/model-credibility reviewer

**Finding:** DMDU is material only when probability/model specification is genuinely unsettled. In well-specified stochastic cases, POMDP/Bayesian design parents remain stronger and cheaper.

**Consequence:** deep-uncertainty machinery must be contextual and carry activation evidence; otherwise it is drag.

## F3. Evidence-to-decision reviewer

**Finding:** GRADE/EtD demonstrates an operational separation ORION should respect but cannot copy uncritically across domains.

**Consequence:** model evidence, decision criteria and authority separately; test domain-native substitutes.

## F4. Hostile editor

**Finding:** four added lanes make the foundation **less ready**, not more impressive.

**Reason:** the appropriate response to newly discovered mature ownership is to reset saturation and block synthesis, not expand the flagship.

## F5. Consensus of the review cell

```text
MATERIAL_NEW_PARENT_PRESSURE = YES
NEW_KERNEL_COORDINATE = NO
NEW_FOUNDATION_LAW = NO
NEW_PAPER = NO
SYNTHESIS_MORATORIUM = CONTINUE
```

---

# G. Parent-space atlas delta

Add:

- `L31 — distributed systems, consensus, replicated state machines and fault tolerance`;
- `L32 — formal/structured defeasible argumentation`;
- `L33 — decision making under deep uncertainty and adaptive pathways`;
- `L34 — evidence grading and evidence-to-decision frameworks`.

Strengthen:

- `L09 — statistical workflow/model checking`;
- `L10 — severe testing/test sensitivity`;
- `L11 — robustness/triangulation`;
- `L12 — assurance/safety cases`;
- `L13 — resilience/adaptive capacity`;
- `L21 — law of evidence/intelligence analysis`;
- `L23 — MDL/algorithmic complexity`.

---

# H. New omission challenges

## OC-19 — consensus is not truth

Can all agents/replicas agree while the scientific state is false, invalid or unauthorized?

## OC-20 — argument semantics and hidden preferences

Does an assurance/argument graph have multiple acceptable extensions, circular support, false premises or a preference-dependent winner?

## OC-21 — deep uncertainty versus fabricated precision

Is the controller using a precise probability model where robust/adaptive reasoning is required, or using deep-uncertainty machinery unnecessarily in a well-specified case?

## OC-22 — evidence-to-decision separation

Are certainty, effect size, values, resources, feasibility, recommendation and authority being collapsed into one score?

---

# I. Strongest parent products required

## I1. Multi-agent scientific transition

`State-machine replication/consensus + authenticated provenance + dependence/common-cause model + native scientific evaluator + explicit authority root`.

## I2. Scientific assurance

`SACM/GSN/CAE + ASPIC+/argumentation semantics + evidence validity/provenance + defeater/circularity checks + authority`.

## I3. Scientific control under deep uncertainty

`RDM/DAPP/minimax-regret parent + scenario ensemble + monitoring/signposts/triggers + native domain model + resource/authority constraints`.

## I4. Evidence to decision

`evidence-quality/certainty parent + effect/claim estimate + values/resources/feasibility + recommendation method + legitimate authority and monitoring`.

These products must receive the same information and resources as any Machine Epistemics integrated arm.

---

# J. Paper propagation

## Flagship

- add these lanes to the parent atlas and external reviewer packet;
- do not produce a new flagship version until synthesis entry is earned;
- distinguish agreement, argument acceptability, robust action and evidence certainty from truth/authority.

## P-A

- compare donor-search multi-agent agreement against distributed consensus and common-mode failure;
- represent argument structure where donor ownership depends on inferential bridges;
- retain MDL/sufficiency baselines.

## P-B

- bind fault/synchrony assumptions when transport uses distributed systems;
- preserve argument semantics/preferences in assurance transport;
- represent context changes along adaptive pathways.

## P-C

- add DMDU/adaptive-pathway baselines;
- test safe nontermination/`CANNOT_CHECK` under evaluator partition;
- measure resilience and common-mode multi-agent faults.

## P-D

- compare reviewer agreement with consensus protocols but keep scientific validity separate;
- add ASPIC+/SACM strongest assurance products;
- distinguish argument acceptance from evidence certainty.

## P-E

- opportunity and agenda decisions require an EtD-like separation of evidence from values/resources/feasibility;
- stress-test opportunities across deep-uncertainty scenarios and adaptive options;
- do not infer agenda authority from robust performance alone.

## P-F

- machine-native multi-agent systems must disclose consensus/fault assumptions;
- nonhuman strategies compete with formal search and DMDU parents;
- opaque internal state is permitted only when external scientific and decision witnesses remain sufficient.

---

# I. Selected primary and authoritative anchors

## Distributed state and fault tolerance

- Lamport, L. Time, Clocks, and the Ordering of Events in a Distributed System. *Communications of the ACM* 21, 558–565 (1978). DOI: `10.1145/359545.359563`.
- Fischer, M. J., Lynch, N. A. & Paterson, M. S. Impossibility of Distributed Consensus with One Faulty Process. *PODS 1983*, 1–7. DOI: `10.1145/588058.588060`.
- Lamport, L. The Part-Time Parliament. *ACM Transactions on Computer Systems* 16, 133–169 (1998).
- Schneider, F. B. Implementing Fault-Tolerant Services Using the State Machine Approach: A Tutorial. *ACM Computing Surveys* 22, 299–319 (1990). DOI: `10.1145/98163.98167`.
- Castro, M. & Liskov, B. Practical Byzantine Fault Tolerance. *OSDI 1999*; extended in *ACM TOCS* 20, 398–461 (2002). DOI: `10.1145/571637.571640`.
- Ongaro, D. & Ousterhout, J. In Search of an Understandable Consensus Algorithm. *USENIX ATC 2014*.

## Formal argumentation and assurance

- Dung, P. M. On the Acceptability of Arguments and Its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games. *Artificial Intelligence* 77, 321–357 (1995). DOI: `10.1016/0004-3702(94)00041-X`.
- Modgil, S. & Prakken, H. The ASPIC+ Framework for Structured Argumentation: A Tutorial. *Argument & Computation* 5 (2014). DOI: `10.1080/19462166.2013.869766`.
- Object Management Group. *Structured Assurance Case Metamodel (SACM) Version 2.3* (2023).
- Goodenough, J. B., Weinstock, C. B. & Klein, A. Z. *Eliminative Argumentation: A Basis for Arguing Confidence in System Properties*. CMU/SEI-2015-TR-005 (2015).

## Deep uncertainty

- Lempert, R. J., Popper, S. W. & Bankes, S. C. Confronting Surprise. *Social Science Computer Review* 20 (2002). DOI: `10.1177/089443902237320`.
- Haasnoot, M., Kwakkel, J. H., Walker, W. E. & ter Maat, J. Dynamic Adaptive Policy Pathways. *Global Environmental Change* 23, 485–498 (2013). DOI: `10.1016/j.gloenvcha.2012.12.006`.
- Kwakkel, J. H., Haasnoot, M. & Walker, W. E. Comparing Robust Decision-Making and Dynamic Adaptive Policy Pathways. *Environmental Modelling & Software* 86, 168–183 (2016). DOI: `10.1016/j.envsoft.2016.09.017`.
- Lempert, R. J. & Collins, M. T. Managing the Risk of Uncertain Threshold Responses. *Risk Analysis* 27, 1009–1026 (2007). DOI: `10.1111/j.1539-6924.2007.00940.x`.
- Rigter, M., Lacerda, B. & Hawes, N. Minimax Regret Optimisation for Robust Planning in Uncertain MDPs. *AAAI 2021*. DOI: `10.1609/aaai.v35i13.17417`.

## Evidence to decision

- GRADE Working Group. Grading Quality of Evidence and Strength of Recommendations. *BMJ* 328, 1490 (2004). DOI: `10.1136/bmj.328.7454.1490`.
- Hultcrantz, M. et al. The GRADE Working Group Clarifies the Construct of Certainty of Evidence. *Journal of Clinical Epidemiology* 87, 4–13 (2017). DOI: `10.1016/j.jclinepi.2017.05.006`.
- Moberg, J. et al. The GRADE Evidence to Decision Framework for Health System and Public Health Decisions. *Health Research Policy and Systems* 16, 45 (2018). DOI: `10.1186/s12961-018-0320-2`.
- Core GRADE 7: Principles for Moving from Evidence to Recommendations and Decisions. *BMJ* 389, e083867 (2025). DOI: `10.1136/bmj-2024-083867`.

## Pass-01 lane strengthening

- Gelman, A. et al. Bayesian Workflow. arXiv:`2011.01808`.
- Modrák, M. et al. Simulation-Based Calibration Checking for Bayesian Computation: The Choice of Test Quantities Shapes Sensitivity. *Bayesian Analysis* 20, 461–488 (2025). DOI: `10.1214/23-BA1404`.
- Säilynoja, T. et al. Posterior SBC: Simulation-Based Calibration Checking Conditional on Data. *Statistics and Computing* 36, 78 (2026). DOI: `10.1007/s11222-026-10825-9`.
- NASA. *NASA-STD-7009B: Standard for Models and Simulations* (2024).
- Pilch, M., Oberkampf, W. L. & Trucano, T. G. *Predictive Capability Maturity Model for Computational Modeling and Simulation*. SAND2007-5948. DOI: `10.2172/976951`.
- Del Giudice, M. & Gangestad, S. W. A Traveler's Guide to the Multiverse. *Advances in Methods and Practices in Psychological Science* (2021). DOI: `10.1177/2515245920954925`.
- Ramdas, A., Grünwald, P., Vovk, V. & Shafer, G. Game-Theoretic Statistics and Safe Anytime-Valid Inference. arXiv:`2210.01948`.
- Cheng, E. K. Reconceptualizing the Burden of Proof. *Yale Law Journal* 122, 1254–1279 (2013).
- Dahlman, C. & Nordgaard, A. Information Economics in the Criminal Standard of Proof. *Law, Probability and Risk* 21, 137–162 (2023). DOI: `10.1093/lpr/mgad004`.
- Rissanen, J. Stochastic Complexity. *JRSS B* 49, 223–239 (1987). DOI: `10.1111/j.2517-6161.1987.tb01694.x`.

---

## Current terminal

```text
PASS_ID = FOUNDATION_SATURATION_PASS_02
MATERIAL_NEW_PARENT_PRESSURE = YES
NEW_ATLAS_LANES = L31_L32_L33_L34
LATEST_MATERIAL_ADDITION = DISTRIBUTED_CONSENSUS__FORMAL_ARGUMENTATION__DEEP_UNCERTAINTY__EVIDENCE_TO_DECISION
POST_MATERIAL_NO_NEW_COORDINATE_COUNT = 0
NEW_KERNEL_COORDINATE = NO
NEW_FOUNDATION_LAW = NO
NEW_PAPER_IDENTITY = NO
FOUNDATION_SYNTHESIS = BLOCKED
FLAGSHIP_FINAL_REWRITE = BLOCKED
FOUNDATION_SATURATION = OPEN
```
