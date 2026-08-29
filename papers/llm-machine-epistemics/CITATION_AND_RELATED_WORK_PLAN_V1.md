# Citation and Related-Work Plan V1

**Issue:** #51  
**Manuscript:** `MANUSCRIPT_DRAFT_V5.md`  
**Status:** scientific citation roles/placements decided; exact BibTeX serialization remains mechanical.  
**Rule:** citations are not decoration. Every load-bearing prior-art sentence should either bind to the exact owning parent or be removed.

## 1. Citation strategy

The paper should not present a long general survey. Related work has one job:

> establish exactly which state/decision/revision ideas are parent-owned and isolate the remaining assessment-task delta.

Use four citation roles:

- **OWNERSHIP** — citation removes novelty credit from a claim.
- **BOUNDARY** — citation defines what the paper is *not* claiming.
- **MOTIVATION** — citation shows practical relevance without establishing the theorem.
- **NEAREST_ASSESSMENT** — citation is a baseline the proposed audit must directly distinguish itself from.

---

# 2. Core bibliography with verified metadata

## P01 — causal-state predictive minimality

**Cosma Rohilla Shalizi, James P. Crutchfield.**  
*Computational Mechanics: Pattern and Prediction, Structure and Simplicity.*  
Journal of Statistical Physics / canonical computational-mechanics paper; arXiv `cond-mat/9907176`.

Verified content role:

- causal-state representation is the minimal one consistent with accurate prediction;
- optimality/uniqueness and comparison to alternative representations.

Role: `OWNERSHIP` for `S_P`.

Final metadata action:

mechanically verify journal volume/pages/DOI from Crossref/JSP before BibTeX freeze.

## P02 — Predictive State Representations

**Michael L. Littman, Richard S. Sutton, Satinder Singh.**  
*Predictive Representations of State.*  
Advances in Neural Information Processing Systems 14, pp. 1555–1561; conference NIPS/NeurIPS 2001 proceedings (commonly cited as 2002 publication).

Verified content role:

- state represented by multi-step, action-conditional predictions of future observations;
- any system has a linear PSR no larger than its minimal POMDP state representation in the paper's sense.

Role: `OWNERSHIP/MOTIVATION` for predictive-state reference.

Final metadata action:

use official NeurIPS BibTeX to resolve conference-year convention.

## P03 — decisional states

**Nicolas Brodu.**  
*Reconstruction of Epsilon-Machines in Predictive Frameworks and Decisional States.*  
Advances in Complex Systems **14**(5), 761–794 (2011).  
DOI `10.1142/S0219525911003347`.

Verified content role:

- decisional states group internal predictive/causal states by user-supplied utility/payoff and resulting decision;
- utility is external to the predictive system;
- transitions between decisional states correspond to changes in decision.

Role: `DIRECT_OWNERSHIP` for generic predictive→decision state and P0 zero-cost control.

## P04 — R-PSR

**Andrea Baisero, Christopher Amato.**  
*Reconciling Rewards with Predictive State Representations.*  
IJCAI 2021, pp. 2170–2176.  
DOI `10.24963/ijcai.2021/299`.

Exact locations:

- Sec. 3 opening: PSR state is sufficient for future observations but not necessarily future rewards.
- Proposition 1: reward mapping from PSR state/action need not exist.
- Theorem 1: exact linear reward conversion iff the POMDP reward columns lie in the span of core outcome vectors.

Role: `DIRECT_OWNERSHIP` for “prediction can miss another decision target”.

## P05 — Information Bottleneck

**Naftali Tishby, Fernando C. Pereira, William Bialek.**  
*The Information Bottleneck Method.*  
37th Annual Allerton Conference on Communication, Control, and Computing (1999), pp. 368–377.

Role:

`OWNERSHIP` for target-relevant compression framing.

## P06 — Deterministic Information Bottleneck

**D. J. Strouse, David J. Schwab.**  
*The Deterministic Information Bottleneck.*  
Neural Computation **29**(6), 1611–1630 (2017).  
DOI `10.1162/NECO_a_00961`.

Role:

`OWNERSHIP` for entropy-constrained deterministic compression/hard clustering.

## P07 — Approximate Information State

**Jayakumar Subramanian, Amit Sinha, Raihan Seraj, Aditya Mahajan.**  
*Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems.*  
Journal of Machine Learning Research **23**(12), 1–83 (2022).

Exact locations:

- Definition 3, p.6: P1 current expected-reward/performance sufficiency; P2 next-information-state prediction.
- P2a/P2b and Proposition 4, p.7: recursive update + next-observation prediction imply P2.
- Theorem 5, p.8: dynamic programming on information state recovers history-state values and optimal policy.
- POMDP example: belief/filtering state is a special case.

Role:

`DIRECT_OWNERSHIP` for generic recursively updateable decision-sufficient state.

## P08 — Value Equivalence

**Christopher Grimm, André Barreto, Satinder P. Singh, David Silver.**  
*The Value Equivalence Principle for Model-Based Reinforcement Learning.*  
NeurIPS 2020, Advances in Neural Information Processing Systems 33.

Verified role:

- value-equivalent models need retain only aspects needed for Bellman/value-based planning;
- adding functions/policies shrinks the equivalence class, eventually to the true model in the registered limit considered there.

Role: `OWNERSHIP` for decision-family-relative model/state retention.

## P09 — Proper Value Equivalence

**Christopher Grimm, André Barreto, Gregory Farquhar, David Silver, Satinder Singh.**  
*Proper Value Equivalence.*  
NeurIPS 2021, Advances in Neural Information Processing Systems 34.

Verified role:

- order-k VE family;
- PVE can retain multiple models sufficient for optimal planning even when irrelevant environment aspects are ignored.

Role: `OWNERSHIP` for bounded decision-family sufficiency.

## P10 — Value-Equivalent Sampling

**Dilip Arumugam, Benjamin Van Roy.**  
*Deciding What to Model: Value-Equivalent Sampling for Reinforcement Learning.*  
NeurIPS 2022, Advances in Neural Information Processing Systems 35.  
DOI `10.52202/068431-0656`.

Verified role:

- rate-distortion tradeoff between model simplicity/capacity and decision quality;
- Bayesian regret bound;
- simplest model for a desired suboptimality or best model under capacity limit.

Role: `OWNERSHIP` for generic state/capacity versus decision-quality tradeoff.

## P11 — epistemic state abstraction / information horizon

**Dilip Arumugam, Satinder P. Singh.**  
*Planning to the Information Horizon of BAMDPs via Epistemic State Abstraction.*  
NeurIPS 2022, Advances in Neural Information Processing Systems 35.

Verified role:

- introduces a complexity measure tied to an information horizon in Bayes-adaptive planning;
- explicitly uses the term `epistemic state abstraction` to reduce BAMDP complexity.

Role:

`BOUNDARY` for terminology; #51 should not present that phrase as new.

## P12 — log-loss rate distortion

**Thomas A. Courtade, Tsachy Weissman.**  
*Multiterminal Source Coding under Logarithmic Loss.*  
IEEE Transactions on Information Theory **60**(1), 740–761 (2014).  
DOI `10.1109/TIT.2013.2288257`.

Role:

`OWNERSHIP` for log-loss entropy/rate-distortion benchmark.

## P13 — iterated belief-revision state storage

**Paolo Liberatore.**  
*Representing States in Iterated Belief Revision.*  
Artificial Intelligence **336**, 104200 (2024).  
DOI `10.1016/j.artint.2024.104200`.

Verified role:

- iterated revision requires a doxastic state carrying more than current beliefs;
- studies storage/succinctness of explicit preorder, level, natural-history and lexicographic-history representations;
- all considered forms can represent every doxastic state, with strict differences in succinctness.

Role:

`STRONG_BOUNDARY` for claims about state/storage needed for future belief revision.

## P14 — Belief-R

**Bryan Wilie, Samuel Cahyawijaya, Etsuko Ishii, Junxian He, Pascale Fung.**  
*Belief Revision: The Adaptability of Large Language Models Reasoning.*  
EMNLP 2024, pp. 10480–10496.  
DOI `10.18653/v1/2024.emnlp-main.586`.

Verified role:

- introduces Belief-R to test LMs' belief revision after new evidence;
- evaluates about 30 LMs;
- reports struggle with appropriate revision and a tradeoff where models good at updating can perform worse when no update is needed.

Role:

`NEAREST_ASSESSMENT`.

Mandatory distinction sentence:

> Belief-R tests whether an output should update after new evidence; the Prospective Revision Audit first matches present language/current-decision behavior across representation conditions and then asks whether retained historical state causally changes later update/maintain performance.

## P15 — standards for belief representation

**Daniel A. Herrmann, Benjamin A. Levinstein.**  
*Standards for Belief Representations in LLMs.*  
Minds & Machines **35**(1), Article 5 (2025).  
DOI `10.1007/s11023-024-09709-6`.

Verified role:

- criteria: Accuracy, Coherence, Uniformity, and Use;
- warns against identifying belief representations from one isolated external criterion.

Role:

`BOUNDARY/MOTIVATION` for requiring causal use rather than linear decodability alone.

## P16 — belief-like internal representations

**Alessandro Corona Mendozza, Anders Søgaard.**  
*LLM Beliefs Are in Their Heads.*  
ACL 2026 Long Papers, pp. 41033–41067.  
DOI `10.18653/v1/2026.acl-long.1905`.

Verified role:

- probes residual/head activations under Herrmann-Levinstein standards;
- reports strong truth sensitivity and causal-use evidence via activation steering, with more moderate coherence/uniformity.

Role:

`BOUNDARY/MOTIVATION`: real LLMs can contain causally useful belief-like structure, so #51 must not assume epistemic emptiness.

## P17 — recall versus truthfulness warning

**Chi Seng Cheang, Hou Pong Chan, Wenxuan Zhang, Yang Deng.**  
*Do LLMs Really Know What They Don’t Know? Internal States Mainly Reflect Knowledge Recall Rather Than Truthfulness.*  
Findings of ACL 2026, pp. 713–730.  
DOI `10.18653/v1/2026.findings-acl.34`.

Verified role:

- hidden states can primarily track parametric recall rather than truthfulness;
- associated hallucinations can overlap hidden-state geometry with factual outputs.

Role:

`MOTIVATION` for typed responsibilities instead of one “truth/confidence state”.

## P18 — representation identifiability

**Vasileios Sevetlidis.**  
*A Fiber Criterion for Representation Identifiability in Supervised Learning.*  
arXiv:2606.01092 (2026).

Verified role:

- predictor behavior constrains the composite predictor but does not identify arbitrary representation/head factorization properties;
- representation property is behaviorally identifiable only when constant on predictor-factorization fibres;
- predictor-preserving augmentation gives canonical obstruction.

Role:

`DIRECT_BOUNDARY`: matched language behavior cannot by itself establish matched hidden epistemic state.

## P19 — stable quotient minimal Markovization

**Zuyuan Zhang, Yongshan Chen, Mahdi Imani, Tian Lan.**  
*Minimal Markovization via Stable Quotients in Holonomy-Cover Decision Processes.*  
arXiv:2607.27132v1 (29 July 2026).

Exact locations:

- Lemma 3.5 — finite refinement stabilizes;
- Proposition 3.7 — exact abstraction criterion;
- Theorem 3.8 — every exact observation-wise abstraction refines the stable quotient;
- Theorem 3.9 — observation + stable class is an exact value-preserving finite Markov state;
- Proposition 3.11 — posterior over stable classes when initial class unknown;
- Corollary 3.12 — minimal exact reusable memory symbols under the paper's conditions.

Role:

`DIRECT/STRONG_OWNERSHIP` for coarsest stable recursively updateable quotient/minimal memory in its model class.

## P20 — retentive complexity public 2026 neighbor

**Anonymous during current public double-blind review.**  
*History, Hypergraphs, and Memory: The Exact Complexity of Deviation-Rational Control.*  
Public RLC 2026 / RLJ submission, OpenReview id `oNLGDwZo5d`.

Verified public role:

- exact memory/retentive-complexity characterization for acceptable continuation behavior;
- history-indexed low-regret continuation sets / hypergraph-transversal formulation;
- pairwise compatibility can be insufficient.

Role:

`PUBLIC_PREPRINT_NEIGHBOR / STRONG_PARENT_PRESSURE`.

Do not invent author names while blind. At final submission, re-check review/publication status and cite according to the then-public identity.

## P21 — current decision-aware LLM memory

**Xinyu Guan, Qianyang Zhao, Yuming Deng.**  
*Decision-Aware Memory Cards: Counterfactual-Inspired Context Selection and Compression for Tool-Using LLM Agents.*  
arXiv:2606.08151 (2026).

Role:

`PRACTICAL_NEIGHBOR`: decision utility/action shift already used to choose/compress LLM-agent context.

## P22 — bounded-memory LLM agent testbed

**Xiangchen Cheng et al.**  
*AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents.*  
arXiv:2607.02255 (2026).

Verified role:

- treats memory as a bounded contract controlling which prior information each future decision sees;
- typed retrieval and memory ablations support causal study of memory layers.

Role:

`PRACTICAL_NEIGHBOR`: bounded memory contracts for long-horizon LLM agents are already active research.

---

# 3. Sentence-level placement plan for Manuscript V5

## Abstract

Do not overload with citations. If target style permits abstract citations, use only:

- causal/predictive-state parent;
- AIS/stable quotient parent;
- Belief-R.

Otherwise leave citations to Introduction.

## Introduction paragraph 2 — strongest parents

Sentence groups and citations:

- “predictive/causal states” -> P01/P02.
- “decision-relative state” -> P03/P04.
- “recursively updateable information state” -> P07/P19.
- “decision-aware capacity” -> P08–P12.
- “belief revision already evaluated in LMs” -> P14.

## Introduction contribution paragraph

No parent citation necessary for #51's registered assessment definitions, but append a sentence:

> These definitions use parent-owned sufficiency/minimization machinery; their claimed contribution is the matched three-stage assessment task rather than a new generic state abstraction.

Cite P03/P07/P19.

## Related work 2.1 predictive state

P01/P02.

## Related work 2.2 current decision

P03/P04/P08/P09.

Explicitly state Brodu decisional states can be *coarser* than predictive causal states when utility depends only on predicted futures.

## Related work 2.3 recurrent state

P07 + P19 + classical POMDP/ISFSM anchors.

This paragraph should contain the strongest concession in the paper.

## Related work 2.4 bounded capacity

P05/P06/P10/P12.

## Related work 2.5 belief revision / LLM internal state

P14/P15/P16/P17/P18/P21/P22.

Ordering:

1. Belief-R output revision;
2. belief representation criteria/causal use;
3. truth-vs-recall warning;
4. representation-identifiability boundary;
5. decision-aware/bounded-memory practical neighbors.

## Current responsibility section

Cite P03/P04 and say the conditional-entropy form is an accounting specialization, not a new decision-theory result.

## Prospective revision section

Cite P07/P19 and incomplete-FSM parent.

Use wording:

> The recursively updateable-state construction is inherited; the paper's audit quantity is relative to a separate linguistic-prediction reference and a registered current-decision baseline.

## Dynamic optionality section

No claim of theorem novelty. Add parent citation after the sentence saying the two component optima are inherited constructions: P07/P19/ISFSM.

## Belief-revision audit section

Lead with P14. Then explicitly contrast:

- output revision benchmark;
- representation intervention after present-equivalence matching.

Cite P18 for why behavior alone does not identify representation properties.

## LLM internal-state interpretation

Cite P15/P16/P17.

Do not write “LLMs lack belief state”.

## Limitations

Cite P13 for prior storage/succinctness of iterated doxastic states when discussing revision memory.

---

# 4. Citations explicitly **not** to use as novelty evidence

The following may motivate the topic but cannot support an originality sentence:

- P01/P02/P03/P04/P07/P19 for generic state construction;
- P05/P06/P10/P12 for capacity tradeoff;
- P14 for belief revision generally;
- P21/P22 for decision-aware/bounded LLM memory.

They are parents/neighbors, not “evidence that #51 is new”.

---

# 5. Required negative related-work paragraph

The final paper should contain a paragraph substantially equivalent to:

> The present framework does not introduce a new generic minimal state construction. Causal-state and PSR theory own predictive state, Brodu and statistical decision theory own utility-relative decision state, R-PSR demonstrates that one predictive target can omit another decision target, information-state/POMDP/finite-state-control theory owns recursive history compression, and recent stable-quotient work gives an especially close coarsest exact recurrent-state result. Belief-R already evaluates language-model revision after new evidence. The proposed residual is instead a matched representation assessment: use linguistic prediction and current decision as controls, intervene on retained state, and ask whether later evidence exposes a revision distinction that the representation discarded.

This paragraph is a publication safeguard. Do not remove it for rhetorical strength.

---

# 6. Mechanical bibliography handoff

The execution/editorial AI may now perform only:

1. official BibTeX export / DOI normalization;
2. spelling/diacritics validation;
3. conference-year convention normalization;
4. page/volume verification;
5. current-status check for the double-blind RLC manuscript;
6. duplicate BibTeX-key resolution;
7. insertion into manuscript according to the placement map above.

It may not change the ownership roles or omit a direct parent because it makes the paper look less novel.
