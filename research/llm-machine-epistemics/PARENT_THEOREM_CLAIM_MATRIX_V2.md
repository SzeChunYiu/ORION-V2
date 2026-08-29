# Parent Theorem / Claim Matrix V2

**Issue:** #51  
**Status:** substantive parent ownership decisions closed; only mechanical bibliography-format/hash verification remains.  
**Purpose:** bind #51 claims to exact parent results/locations so no execution AI must invent novelty judgments.

## Verdict vocabulary

- `DIRECT_PARENT` — parent result already contains the same essential mathematical/assessment pattern.
- `STRONG_PARENT` — not identical object, but reconstructs the core mechanism with a routine specialization/composition.
- `PARENT_AREA` — mature literature owns the principle but not the exact #51 specialization.
- `DISTINCT_ASSESSMENT_DELTA` — no direct parent found for the registered three-stage matched representation audit.
- `PUBLIC_PREPRINT_NEIGHBOR` — current public work relevant to novelty, but publication metadata is not archival/final.
- `CANNOT_CHECK_FULL_TEXT` — no claim beyond metadata/abstract should be made.

---

# Matrix

| #51 object | Parent | Exact location / parent statement | Ownership verdict | Final #51 disposition |
|---|---|---|---|---|
| Minimal state for complete future prediction `S_P` | computational mechanics / causal states; PSRs | causal-state equivalence groups histories by conditional future law; causal states are minimal predictive sufficient statistics under their assumptions | `DIRECT_PARENT` | definition/reference channel only |
| A prediction-sufficient state may miss another task/target | Baisero & Amato, **R-PSR**, IJCAI 2021 | Sec. 3, **Proposition 1**: for a finite POMDP and its PSR, a function from PSR state/action to POMDP reward need not exist. **Theorem 1**: exact linear PSR reward representation exists iff POMDP reward columns lie in the span of core outcome vectors. | `DIRECT_PARENT` | C02 parent-owned; predictive!=responsibility cannot be headline novelty |
| Decision state from predictive state using utility/loss | Brodu 2011 decisional states | framework defines utility-driven iso-prediction / iso-utility / decisional states from predictive causal states, with decisional complexity and transitions between decision states | `DIRECT_PARENT` | C03/C05 parent-owned/control; zero extra state when decision factors through predictive future |
| Current decision sufficiency / Bayes-risk ordering | Blackwell/statistical decision theory | more informative experiment/statistic can emulate decisions from a less informative statistic; sufficient information preserves decision risks for the declared decision family | `DIRECT_PARENT` | C04/C06 decision-theory specializations; no independent theorem credit |
| Decision-aware model abstraction and bounded capacity | Grimm et al. **Value Equivalence**; Grimm et al. **Proper Value Equivalence**; Arumugam & Van Roy **Value-Equivalent Sampling** | VE/PVE retain only dynamics needed for planning over a value/policy family; VES uses rate-distortion to find a simple approximately value-equivalent model and gives a Bayesian regret bound, including simplest-model-for-gap / best-model-for-capacity views | `STRONG_PARENT` | state/capacity tradeoff is parent-owned principle |
| “Epistemic state abstraction” / information horizon terminology | Arumugam & Singh, NeurIPS 2022 | paper explicitly introduces an **epistemic state abstraction** for Bayes-adaptive MDP planning and an information-horizon complexity measure | `PARENT_AREA` + naming collision | do not use “epistemic state abstraction” as proprietary/new term |
| Information state sufficient for current performance and future state evolution | Subramanian et al., JMLR 2022 AIS | **Definition 3**: information-state generator is a history compression satisfying **P1** current performance/reward sufficiency and **P2** sufficiency to predict its next value. | `DIRECT_PARENT` | generic current+future sufficient state parent-owned |
| Recursive update + next-observation sufficiency as stronger information-state characterization | Subramanian et al., JMLR 2022 AIS | Sec. 2.3 **P2a**: state-like recursive update; **P2b**: sufficient for predicting next observation; **Proposition 4**: P2a + P2b imply P2. | `DIRECT_PARENT` | generic recursive-state construction not #51 novelty |
| Information state yields optimal DP | Subramanian et al., JMLR 2022 AIS | **Theorem 5**: dynamic program on information state reproduces history-based Q/value functions and optimal policies. | `DIRECT_PARENT` | C09 generic decision sufficiency/updateability owned |
| Belief state as recursively sufficient POMDP state | classical POMDP theory, also AIS examples | AIS discussion explicitly lists posterior belief `B_t=P(S_t|H_t)` with filtering update as an information state and standard POMDP DP as a Theorem-5 special case | `DIRECT_PARENT` | no generic claim that #51 invented history-to-state Markovization |
| Current compatibility + successor closure / right congruence | incompletely specified FSM minimization, automata/right-congruence theory | ISFSM exact minimization uses compatible state classes plus **closed cover** successor constraints; minimal cover/minimization is a longstanding combinatorial problem | `STRONG_PARENT` | C08–C10 minimization substrate parent-owned/specialization |
| Coarsest stable recursively updateable quotient | Zhang, Chen, Imani & Lan 2026, **Minimal Markovization via Stable Quotients...** | Introduction summarizes: **Lemma 3.5** monotone finite refinement stabilizes; **Proposition 3.7** exactness criterion; **Theorem 3.8** every exact observation-wise abstraction refines stable quotient; **Theorem 3.9** observation + stable class is an exact value-preserving finite Markov state; **Corollary 3.12** exactly `max_o |C_o|` reusable memory symbols are necessary/sufficient under its assumptions. | `DIRECT/VERY_STRONG_PARENT` | C09/C10/C14 cannot carry new generic state-minimization claim |
| Finite right congruence as memory abstraction | Zhang et al. 2026 appendix + automata parents | paper explicitly relates arbitrary finite-memory history abstraction to a finite right congruence; stable quotient is the minimal class in its HCDP setting | `STRONG_PARENT` | #51 right-congruence language is inherited substrate |
| Minimum present memory for acceptable continuation decisions | **History, Hypergraphs, and Memory: The Exact Complexity of Deviation-Rational Control**, public double-blind RLC/RLJ 2026 manuscript, OpenReview `oNLGDwZo5d` | public manuscript states an exact retentive-complexity law via history-indexed low-regret continuation sets / hypergraph transversal complexity and shows pairwise compatibility can be insufficient | `PUBLIC_PREPRINT_NEIGHBOR / VERY_STRONG_PARENT` | present-memory/control compatibility cannot be sold as new; qualify anonymous/current-review status |
| Space complexity of retaining belief state across iterated revisions | Paolo Liberatore, **Representing states in iterated belief revision**, Artificial Intelligence 336 (2024), 104200, DOI `10.1016/j.artint.2024.104200` | paper explicitly studies how large doxastic states become under iterated revision and compares four exact representations; lexicographic histories are most succinct among the four while all represent every doxastic state | `STRONG_PARENT` for revision-state storage | reinforces that revision-state memory/space is established; #51 must focus on matched autoregressive representation audit |
| Rate/capacity versus decision-quality tradeoff | information bottleneck / conditional rate-distortion / VES | generic lossy representation tradeoff and log-loss entropy-minus-distortion relations | `DIRECT_PARENT` | T8 parent-owned benchmark only |
| Belief revision after new evidence in LMs | Wilie et al., **Belief-R**, EMNLP 2024 | abstract: Belief-R tests LM belief-revision ability when given new evidence; ~30 LMs evaluated; models struggle to update and updating ability trades off against cases where updates are unnecessary | `DIRECT_PARENT` for output-level revision evaluation | do not claim first LLM belief-revision test |
| Current decision-aware LLM memory selection/compression | recent 2026 decision-aware memory and bounded-memory agent work | current papers explicitly select/compress memory based on decision utility or enforce bounded typed retrieval | `PARENT_AREA` | “decision-aware LLM memory” not novelty |
| Predictor behavior does not identify arbitrary hidden representation properties | 2026 representation-identifiability work | predictor-equivalent factorizations can vary in representation properties unless the property is constant over the relevant fibers | `DIRECT_PARENT` | same language loss cannot prove equal epistemic representation; illustration only |
| LLM internal belief/truth/uncertainty signals | Herrmann & Levinstein; ACL/EMNLP 2025–26 belief/truth work | existing standards require more than decodability (including use/causal relevance); empirical work finds belief-like or factuality/recall signals | `PARENT_AREA` | no claim that LLMs lack internal epistemic structure |
| #51 `Omega_dyn = C_dyn^*-C_stat^*` | constructed from parent-owned optimization values | no direct parent found in Pass 04 expressing this exact conditional-entropy **difference relative to a separate complete-linguistic predictive quotient** for a registered future revision responsibility | `DISTINCT_ASSESSMENT_DELTA` but weak math novelty | C11 = derived audit metric, not new information law |
| #51 P0/P1/P2 taxonomy | assembled from current-vs-prospective state costs | no direct parent found using these exact three audit phases for autoregressive representation assessment; phase inequalities themselves are routine consequences of parent state theory | `DISTINCT_ASSESSMENT_DELTA` | C13 = analytical taxonomy only |
| #51 horizon audit `C_k^*, Omega_k` | finite refinement / information horizon / state abstraction parents | monotonicity/stabilization parent-style; no direct parent found using it as a matched-current autoregressive revision-retention profile | `DISTINCT_ASSESSMENT_DELTA` with strong parent pressure | C14 = audit curve, not new finite-state theorem |
| #51 no-certification witness | mechanically checked one-bit provenance fixture | exact existence example: equal language predictive state + equal unique present optimal action, but later evidence requires different successor decisions; compressed vs augmented states differ only in dormant bit | `#51_KNOWN_ANSWER_WITNESS` | supports assessment necessity, not empirical LLM frequency |
| #51 prospective representation audit | #51 protocol vs Belief-R / information-state parents | **registered difference**: freeze/match present language prediction and current responsibility first; intervene on retained representation; only then reveal later evidence; measure update **and** maintain/selective-reopening success | `DISTINCT_ASSESSMENT_DELTA` | strongest standalone candidate, C18/I01 |

---

# Exact parent locations frozen for the manuscript

## Baisero & Amato 2021 R-PSR

**Paper:** Andrea Baisero, Christopher Amato, *Reconciling Rewards with Predictive State Representations*, IJCAI 2021, pp. 2170–2176, DOI `10.24963/ijcai.2021/299`.

Use:

- Sec. 3 opening: PSR state is sufficient for future observation probabilities but not necessarily future rewards.
- **Proposition 1**: for any finite POMDP and respective PSR, a reward mapping from PSR state/action need not exist.
- **Theorem 1 (Accurate Linear PSR Rewards)**: exact linear PSR reward conversion iff every POMDP reward column is linearly dependent on the core outcome vectors.
- **Corollary 1**: reverse result for representing PSR rewards by POMDP rewards.

Primary URL:

`https://www.ijcai.org/proceedings/2021/0299.pdf`

## Subramanian et al. 2022 AIS

**Paper:** Jayakumar Subramanian, Amit Sinha, Raihan Seraj, Aditya Mahajan, *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems*, JMLR 23(12):1–83, 2022.

Use:

- **Definition 3** (paper p.6): history compression `sigma_t(H_t)` is information state if **P1** suffices for expected reward/performance and **P2** predicts next information state.
- **P2a/P2b + Proposition 4** (paper p.7): recursive state-like update plus sufficiency for the next observation imply P2.
- **Theorem 5** (paper p.8): dynamic program on information state equals history-state Q/value functions and yields an optimal policy.
- Sec. 2.5 examples: POMDP belief state with filtering recursion is a special case.

Primary URL:

`https://jmlr.org/papers/volume23/20-1165/20-1165.pdf`

## Zhang et al. 2026 stable quotient

**Paper:** Zuyuan Zhang, Yongshan Chen, Mahdi Imani, Tian Lan, *Minimal Markovization via Stable Quotients in Holonomy-Cover Decision Processes*, arXiv:2607.27132v1, 29 July 2026.

Use:

- **Lemma 3.5**: monotone finite refinement stabilizes.
- **Proposition 3.7**: exactness criterion for reward-and-successor-preserving abstraction.
- **Theorem 3.8**: every exact observation-wise abstraction refines the stable quotient.
- **Theorem 3.9**: current observation + stable quotient class is an exact value-preserving finite Markov state.
- **Proposition 3.11**: when initial class unknown, posterior over stable classes is the exact observable information state.
- **Corollary 3.12**: under the paper's assumptions, exactly the maximal number of observation-wise stable classes is necessary and sufficient for reusable exact class-tracking memory.

Primary URL:

`https://arxiv.org/html/2607.27132v1`

## Belief-R

**Paper:** Bryan Wilie, Samuel Cahyawijaya, Etsuko Ishii, Junxian He, Pascale Fung, *Belief Revision: The Adaptability of Large Language Models Reasoning*, EMNLP 2024, pp. 10480–10496, DOI `10.18653/v1/2024.emnlp-main.586`.

Use:

- task explicitly tests LM belief revision after new evidence;
- includes cases where additional information necessitates revision and cases where update is unnecessary;
- reports an update/maintain-like tradeoff: models adept at updating can underperform where no update is needed.

Primary URL:

`https://aclanthology.org/2024.emnlp-main.586/`

## Liberatore 2024 iterated belief revision storage

**Paper:** Paolo Liberatore, *Representing states in iterated belief revision*, Artificial Intelligence 336 (November 2024), 104200, DOI `10.1016/j.artint.2024.104200`.

Use:

- doxastic states retain information beyond current beliefs for iterated revision;
- the paper explicitly studies storage size/succinctness;
- compares explicit preorder, level representation, natural-revision histories, and lexicographic-revision histories;
- all four are universal for its doxastic-state class, with strict succinctness differences.

Primary DOI:

`10.1016/j.artint.2024.104200`

---

# Final parent-subtraction rule

The following claims are now frozen as **not eligible for novelty rescue** under #51:

```text
minimal_predictive_state
prediction_state_can_miss_secondary_target
generic_decision_sufficient_state
generic_decision_state_entropy
generic_recurrent_information_state
current_compatibility_plus_successor_closure
generic_minimal_right_congruent_state
generic_belief_revision_after_evidence
generic_decision_aware_memory
generic_capacity_vs_decision_quality_tradeoff
```

The execution AI may fill citation metadata or exact page/line fields, but it may **not** relabel one of these as novel because a parent uses different notation.

The only current standalone delta allowed is:

```text
PROSPECTIVE_REVISION_REPRESENTATION_AUDIT =
    complete_linguistic_reference
  + matched_current_responsibility
  + controlled_representation_retention_intervention
  + future_evidence_update_and_maintain_test
  + conditional_current_vs_prospective_state_accounting
```

Current novelty classification:

`CANDIDATE_FORMAL_ASSESSMENT_TASK / ANALYTICAL_FRAMEWORK`, not `NEW_CORE_STATE_THEORY`.
