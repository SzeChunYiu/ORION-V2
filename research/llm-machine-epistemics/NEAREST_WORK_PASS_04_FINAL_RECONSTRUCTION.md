# Nearest Work Pass 04 — Final Strongest-Parent Reconstruction

**Issue:** #51  
**Status:** non-computational theorem/claim ownership audit after mechanical batches #56–#59.  
**Purpose:** decide what remains scientifically defensible after reconstructing the strongest *product* of existing theories, rather than comparing #51 against each parent in isolation.

## Executive verdict

The mechanical work has made the finite theory substantially more trustworthy, but the final literature pass makes the novelty boundary **narrower**.

The strongest-parent product now reconstructs almost all of the underlying state-minimization mathematics:

```text
complete-future predictive state
  -> causal states / PSRs

current utility/decision state
  -> statistical decision theory / Brodu decisional states / R-PSR

minimum current memory for an acceptable continuation policy
  -> decision sufficiency + retentive-complexity / compatibility formulations

recursive current+future decision state
  -> information states / POMDP belief states
     + right congruence / incomplete-FSM closed-cover minimization
     + 2026 stable-quotient Markovization results

capacity-vs-decision-quality tradeoff
  -> value equivalence / value-equivalent sampling / rate-distortion

revision after new evidence in LMs
  -> Belief-R and related belief-updating evaluation work
```

Accordingly, #51 should **not** claim a new generic theory of minimal decision state, minimal recurrent state, decision-aware compression, belief revision, or finite-memory control.

The strongest remaining standalone candidate is instead an **analytical representation-audit framework** specialized to an autoregressive linguistic predictive reference state:

> A representation may be adequate for the complete linguistic prediction target and for the registered current epistemic decision while still being inadequate for a future evidence-triggered revision. #51 makes those three obligations separately measurable, conditions the added state cost on the linguistic predictive quotient, and defines a prospective audit that distinguishes current decision retention from dormant revision-relevant information.

This is a potentially useful synthesis/formal assessment task. It is **not currently supported as a new core state-minimization theorem family**.

---

# 1. Strongest parent A — predictive state

## Computational mechanics / causal states

Parent ownership:

- equivalence of histories by complete future conditional law;
- a minimal sufficient predictive state under standard assumptions;
- recursively calculable predictive-state machinery in appropriate processes.

#51 consequence:

- `S_P` is parent-owned.
- no novelty for full-future predictive partition, its minimality, or the proposition that exact predictive-sufficient refinements contain at least that information.

## Predictive State Representations

Parent ownership:

- history represented through future-test predictions;
- controlled dynamical prediction without requiring the analyst's latent state.

#51 consequence:

- “language state as a future-prediction statistic” is an application/specialization, not a new state ontology.

---

# 2. Strongest parent B — decisions may require a different state

## Brodu (2011), decisional states

Nicolas Brodu, *Reconstruction of Epsilon-Machines in Predictive Frameworks and Decisional States*, Advances in Complex Systems 14(5), 761–794, DOI `10.1142/S0219525911003347`.

The published framework applies a user-provided utility/payoff to predictive causal states and defines iso-prediction, iso-utility and decisional partitions. The decisional states are explicitly a coarser layer of causal states when the decision is fully determined by the predictive distribution; transitions between decisional states correspond to changes in the preferred decision.

Primary sources:

- `https://nicolas.brodu.net/recherche/decisional_states/index.html`
- DOI above.

Ownership effect:

- C03 is parent-owned.
- C05 (zero extra state when an optimal decision factors through `S_P`) is a mandatory control, not novelty.
- generic “entropy/complexity of a decision state” is not a #51 invention.

Important boundary for #51:

A **positive** added-state cost can only be meaningful when the registered responsibility uses information not measurable from the declared linguistic future. This is why the manuscript uses “cross-channel responsibility” as a scoped shorthand rather than treating every downstream decision as an epistemic refinement.

## Baisero & Amato (IJCAI 2021), Reward-Predictive State Representations

Andrea Baisero and Christopher Amato, *Reconciling Rewards with Predictive State Representations*, IJCAI 2021, pp. 2170–2176, DOI `10.24963/ijcai.2021/299`.

Parent result:

- an observation-predictive PSR can fail to model a reward target;
- a necessary/sufficient accuracy condition is derived;
- R-PSR augments the state so observations and rewards are both modeled and optimal policies match the corresponding POMDP.

Primary source:

- `https://www.ijcai.org/proceedings/2021/299`

Ownership effect:

- the broad pattern “state sufficient for prediction may omit another decision-relevant target” is direct prior art.
- C02 is parent-owned.
- C04/C06 cannot earn novelty from target separation alone.

---

# 3. Strongest parent C — recursively updateable decision-sufficient state

## Subramanian et al. (JMLR 2022), Approximate Information State

Jayakumar Subramanian, Amit Sinha, Raihan Seraj and Aditya Mahajan, *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems*, JMLR 23(12):1–83, 2022.

The framework defines an information state as a function of history sufficient for current performance/reward and prediction of its next value; an equivalent stronger construction uses a recursively updateable state sufficient for current performance and the next observation. Information states induce dynamic programming; approximate information states obtain bounded approximate-planning guarantees.

Primary source:

- `https://jmlr.org/papers/v23/20-1165.html`

Ownership effect:

- generic “current decision sufficiency is not enough; state must also support future update/prediction” is strongly parent-owned.
- generic recurrent-state sufficiency is not #51 novelty.
- C09/C10 must be treated as a specialization/finite exact realization unless a narrower residual survives.

## POMDP belief/information states

Classical POMDP theory already supplies a recursively updated history statistic sufficient for future control.

Ownership effect:

- no claim that #51 invented maintaining history information solely because current observation/action is insufficient.

## Incompletely specified finite-state machine minimization

Classical ISFSM minimization constructs compatible state sets and requires a **closed cover**: current output compatibility plus closure of implied successor compatibility. Exact minimization is a longstanding combinatorial problem and is NP-hard/NP-complete in standard formulations.

Useful sources:

- Kam, Villa, Brayton & Sangiovanni-Vincentelli, *Synthesis of Finite State Machines: Functional Optimization*, state minimization chapters.
- Rho, Hachtel, Somenzi & Jacoby, exact/heuristic ISFSM minimization work.
- survey/algorithm literature describing cover + closure and minimal closed cover.

Ownership effect:

- the static-compatible + successor-closure structure of #51's dynamic partition is not a new minimization principle.
- joint choice among compatible actions/outputs and recurrent state has a direct classical analogue.

---

# 4. Strongest 2026 parent — stable quotient / minimal Markovization

## Zhang, Chen, Imani & Lan (2026)

*Minimal Markovization via Stable Quotients in Holonomy-Cover Decision Processes*, arXiv:2607.27132, 29 July 2026.

This is a particularly important current neighbor. For a structured partially observed decision-process class it:

- initializes a partition with immediate reward/control consequences;
- repeatedly refines it by successor compatibility;
- proves finite stabilization;
- proves the resulting stable quotient is the coarsest exact abstraction;
- proves the observation + stable class is an exact value-preserving finite Markov state;
- derives a minimal exact class-tracking memory cardinality under its assumptions.

Primary source:

- `https://arxiv.org/abs/2607.27132`

The paper explicitly describes finite controller memory as inducing a finite right congruence over histories. Its stable-partition operator propagates present reward distinctions backward through future continuations until no future distinction requires a split.

Ownership effect:

- this is very close structurally to #51's P1→P2 refinement.
- the generic statement “start from current decision distinctions, refine until future transitions preserve them, obtain a minimal recursively updateable class” cannot be claimed as novel.
- `Omega_dyn` remains a convenient **relative accounting quantity**, but its component optimization problems now have a very direct 2026 parent.

Difference that remains:

- the HCDP paper studies a structured POMDP family and minimizes Markov/control state;
- #51 fixes a **separate complete-linguistic predictive quotient** as the reference channel and asks how much *additional* state a registered cross-channel responsibility and later revision require;
- #51's proposed empirical interface is a representation audit for autoregressive models, not an HCDP learning algorithm.

This is a synthesis/application distinction, not yet evidence of deep theorem novelty.

---

# 5. Strong 2026 parent — exact memory for rational continuation behavior

## *History, Hypergraphs, and Memory: The Exact Complexity of Deviation-Rational Control*

Public double-blind RLC 2026 / RLJ manuscript, OpenReview id `oNLGDwZo5d` (authors currently anonymous in the public review version).

The public manuscript studies the minimum number of internal memory labels needed to map histories to continuation controllers while preserving epsilon-deviation-rational behavior. It gives an exact characterization using transversal numbers of history-indexed low-regret continuation sets; in a finite controller dictionary at exact rationality this becomes a hypergraph law. It also shows pairwise compatibility can be insufficient and connects recurrent finite-state agents to the resulting memory lower bound.

Public source:

- `https://openreview.net/pdf?id=oNLGDwZo5d`

Ownership effect:

- “minimum present memory labels needed so each compressed history admits an acceptable continuation controller” is a direct current parent.
- pairwise/common-action compatibility and higher-order compatibility cannot be sold as new merely through epistemic terminology.
- #51's entropy-conditioned-on-`S_P` objective differs from cardinal memory/transversal complexity, but the conceptual state-compression problem is clearly occupied.

Because the manuscript is under double-blind review, it should be recorded as a current public neighbor with unstable author metadata, not cited as an established archival result without qualification.

---

# 6. Strongest parent D — preserve only decision-relevant environment/model information

## Grimm et al., Value Equivalence (NeurIPS 2020/2021)

The Value Equivalence principle asks which aspects of environment dynamics need to be modeled for value-based planning rather than for exact transition prediction. Proper Value Equivalence shows that multiple lossy models can remain planning-sufficient even as the function/policy set grows.

Primary sources:

- Grimm, Barreto, Singh & Silver, *The Value Equivalence Principle for Model-Based Reinforcement Learning*, NeurIPS 2020.
- Grimm, Barreto, Farquhar, Silver & Singh, *Proper Value Equivalence*, NeurIPS 2021.

Ownership effect:

- the idea that a bounded agent should retain only information required by a specified downstream decision family is well occupied.
- responsibility-family growth toward a more complete model has a strong conceptual parent.

## Arumugam & Van Roy (NeurIPS 2022), Value-Equivalent Sampling

*Deciding What to Model: Value-Equivalent Sampling for Reinforcement Learning*, NeurIPS 2022.

This work explicitly applies rate-distortion theory to the trade-off between simple model representations and decision quality, with regret guarantees.

Primary source:

- `https://proceedings.neurips.cc/paper_files/paper/2022/hash/3b18d368150474ac6fc9bb665d3eb3da-Abstract-Conference.html`

Ownership effect:

- generic “how many bits/state capacity should be retained for a decision target?” is not new.
- approximate representation cost vs decision quality belongs to an established line.

## Arumugam & Singh (NeurIPS 2022), Epistemic State Abstraction

*Planning to the Information Horizon of BAMDPs via Epistemic State Abstraction*, NeurIPS 2022.

This work defines an information horizon for Bayes-adaptive planning and introduces an **epistemic state abstraction** to reduce planning complexity.

Primary source:

- `https://proceedings.neurips.cc/paper_files/paper/2022/hash/80b7bec60081f95d900973509744a306-Abstract-Conference.html`

Ownership/naming effect:

- “epistemic state abstraction” is already an established phrase in a nearby ML literature.
- #51 should avoid presenting that phrase as proprietary terminology.
- this motivates renaming the paper around **responsibility/revision sufficiency** rather than “epistemic state abstraction”.

---

# 7. LLM-specific parent — belief revision evaluation already exists

## Wilie et al. (EMNLP 2024), Belief-R

Bryan Wilie, Samuel Cahyawijaya, Etsuko Ishii, Junxian He and Pascale Fung, *Belief Revision: The Adaptability of Large Language Models Reasoning*, EMNLP 2024.

Belief-R explicitly evaluates language models at time `t` and after new evidence at `t+1`, with separate update and maintain cases. The study reports that many tested models struggle to revise appropriately, with a tradeoff between updating and retaining conclusions.

Primary source:

- `https://aclanthology.org/2024.emnlp-main.586/`

Ownership effect:

- “evaluate whether LMs revise beliefs after new evidence” is not #51 novelty.
- C18 must be narrowed.

Remaining distinction:

Belief-R evaluates output-level revision after new premises. #51's proposed audit asks a different representation question:

1. hold linguistic predictive adequacy fixed;
2. hold the **current registered responsibility decision** fixed;
3. alter/compare the retained representation or compression;
4. introduce later evidence whose correct consequence depends on a dormant cross-channel distinction;
5. test whether revision remains correct.

Thus the audit targets **prospective representation retention**, not belief revision generally.

## Additional 2026 motivation

Recent work continues to study LLM belief updating and evidence selection. Examples include numerical updating under selected/omitted evidence and internal/observable belief-revision dynamics. These reinforce practical relevance but do not create novelty credit for the general act of updating beliefs.

---

# 8. Current LLM-agent memory neighbors

2026 agent work increasingly treats memory as a decision-relevant selection/compression problem. Examples include:

- *Decision-Aware Memory Cards: Counterfactual-Inspired Context Selection and Compression for Tool-Using LLM Agents* (arXiv:2606.08151), which selects context based on decision utility/action shifts;
- *AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents* (arXiv:2607.02255), which makes memory access a bounded typed-retrieval contract.

These works increase the practical relevance of a representation-retention audit, while also preventing a claim that “decision-aware memory for LLM agents” is itself new.

---

# 9. Strongest-parent product reconstruction

A hostile reviewer can now assemble:

```text
S_P
  = causal state / PSR predictive quotient

current acceptable decision state
  = Blackwell/Bayes decision sufficiency
    + Brodu decisional states
    + R-PSR / value-equivalence style target relevance
    + deviation-rational retentive complexity

recursive updateable decision state
  = POMDP/information state
    + AIS
    + right congruence
    + ISFSM closed cover
    + 2026 stable quotient minimal Markovization

approximate capacity tradeoff
  = information bottleneck / rate distortion
    + value-equivalent sampling

LM output revision test
  = Belief-R and belief-updating literature
```

This product is strong enough that the following #51 components should **not** be advertised as independent theorem novelty:

- C04 static cross-channel cost as generic task-relative state cost;
- C06 obstruction as generic decision-sufficiency criterion;
- C08 static compatible-state optimization as generic state minimization;
- C09 dynamic compatible/right-congruent optimization as generic state minimization;
- C10 selector/right-congruent equivalence as generic compatible-controller minimization;
- C14 finite monotone refinement/horizon stabilization as generic finite refinement behavior;
- C17 universality/no-free-compression boundary.

They remain useful formal ingredients and mechanically checked specializations.

---

# 10. What still survives as a plausible paper contribution?

## 10.1 The reference-channel construction

#51 explicitly chooses the **complete linguistic predictive state** as a reference representation and asks how much additional information is required by a different responsibility channel.

The useful object is therefore not just “minimum memory”, but a conditional decomposition:

```text
linguistic-predictive information
+ current cross-channel responsibility information
+ dormant future-revision information.
```

The parent literature contains all three ingredients in nearby forms, but no direct parent found in Pass 04 packages them as a language-model representation audit with this decomposition.

Classification:

`CANDIDATE_SYNTHESIS_RESIDUAL`, not `NEW_MINIMAL_STATE_THEOREM`.

## 10.2 Dynamic optionality as an accounting metric

`Omega_dyn = C_dyn^* - C_stat^*`

is a clean way to isolate state required **only for future updateability after optimizing present acceptable action**.

Stable quotients, information states and ISFSM theory own the refinement/minimization substrate. No direct source found in this pass uses this exact conditional-entropy *difference relative to a separate linguistic predictive quotient* as a representation audit quantity.

Classification:

`CANDIDATE_DERIVED_METRIC / ANALYTICAL_FRAMEWORK_COMPONENT`.

It should not be described as a fundamentally new information-theoretic law.

## 10.3 P0/P1/P2 as an audit taxonomy

The phases are useful for diagnosing representation failures:

- P0: predictive state already supports current and future responsibility;
- P1: extra cross-channel state needed now;
- P2: extra state is needed for later revision beyond what current action requires.

Classification:

`CANDIDATE_ANALYTICAL_TAXONOMY`.

The phase boundaries are consequences of parent-style state costs; novelty credit, if any, is in the integrated audit interpretation rather than the inequalities themselves.

## 10.4 Prospective revision adequacy as a distinct representation audit

This is now the strongest practical residual.

The mechanically checked one-bit witness establishes an **existence/no-certification result**:

> equality of complete linguistic predictive state and equality of current optimal responsibility action do not logically certify equality of future evidence-triggered revision capability.

Belief-R shows output belief revision is already an important LLM evaluation target. #51 adds a representation-level control: match present prediction and present decision, then test revision under later evidence that requires a dormant cross-channel distinction.

Classification:

`THEORETICALLY_ENTAILED_EVALUATION_PRESCRIPTION`, not `EMPIRICALLY_DEMONSTRATED_LLM_FAILURE`.

---

# 11. Recommended manuscript identity after strongest-parent subtraction

The paper should no longer lead with “a new theory of epistemic state”. A more defensible identity is:

> **a formal representation-audit framework for distinguishing linguistic predictive adequacy, current decision adequacy, and prospective revision adequacy in autoregressive systems.**

Recommended title family:

1. **Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations**
2. **Prediction Is Not Revision: Auditing Decision and Revision Sufficiency in Autoregressive Representations**
3. **Decision-Relevant and Revision-Relevant Memory Beyond Language Prediction**

Preferred: **Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations**.

This title avoids collision with the existing “epistemic state abstraction” literature and accurately describes the strongest residual.

---

# 12. JMLR implication

JMLR's current scope permits theoretical studies that yield new insight, formalization of new learning tasks/methods for assessing performance, and new analytical frameworks. Its reviewer guidance also requires practical utility for theory papers and a contribution sufficiently different from prior work.

Official sources:

- `https://www.jmlr.org/author-info.html`
- `https://jmlr.org/reviewer-guide.html`

Therefore there are two possible JMLR routes:

### Route J-A — new theorem route

Current verdict: **not supported**. The strongest-parent product owns too much of the state-minimization substrate.

### Route J-B — new assessment/analytical-framework route

Current verdict: **plausible but high risk**.

The paper must make the formal assessment task itself crisp and useful:

- define present predictive adequacy;
- define current responsibility regret/adequacy;
- define future/prospective revision regret under registered evidence interventions;
- prove that the first two do not certify the third;
- expose exact finite memory/state-cost diagnostics;
- relate the audit to Belief-R and contemporary LLM memory systems;
- make no empirical statement about real LLM hidden states without an experiment.

If this formal audit is judged too close to a straightforward specialization of information-state/decision-memory theory, JMLR should be abandoned rather than defended rhetorically.

---

# 13. Pass-04 terminal

```text
CORE_MINIMAL_STATE_THEOREM_NOVELTY = NOT_SUPPORTED
STATIC_DECISION_STATE_NOVELTY = NOT_SUPPORTED
GENERIC_RECURRENT_STATE_NOVELTY = NOT_SUPPORTED
GENERIC_BELIEF_REVISION_EVALUATION_NOVELTY = NOT_SUPPORTED

CROSS_CHANNEL_CONDITIONAL_ACCOUNTING = CANDIDATE_SYNTHESIS_RESIDUAL
DYNAMIC_OPTIONALITY_PREMIUM = CANDIDATE_DERIVED_METRIC
P0_P1_P2 = CANDIDATE_ANALYTICAL_TAXONOMY
PROSPECTIVE_REVISION_REPRESENTATION_AUDIT = STRONGEST_SURVIVING_CANDIDATE

JMLR_NEW_THEOREM_ROUTE = FAIL_CURRENTLY
JMLR_ANALYTICAL_FRAMEWORK_ROUTE = OPEN_HIGH_RISK
EMPIRICAL_LLM_CLAIM = NONE
```

This is the non-computational novelty decision. A later mechanical theorem-location check may make the ownership map more exact, but the execution AI is not authorized to reverse these concessions merely because a paper uses different notation.
