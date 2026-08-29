# Nearest-Work Pass 02 — Dynamic State and Downstream-Task Threats

**Issue:** #51  
**Date:** 2026-08-29  
**Purpose:** perform scientific parent adjudication before the mechanical bibliography sweep. This pass materially narrows the claims after identifying stronger direct parents for recurrent sufficient state and downstream-task loss.

## 1. Executive decision

The literature found in this pass makes two corrections mandatory.

### Correction A — generic recurrent sufficiency is already strongly occupied

Subramanian, Sinha, Seraj & Mahajan, **Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems**, JMLR 23 (2022), develops an information-state framework in which a history statistic can be recursively updated and be sufficient for expected reward and prediction of next observations/state. It also develops approximate information states with bounded control-performance loss.

Primary source:

- https://jmlr.org/papers/volume23/20-1165/20-1165.pdf
- https://www.jmlr.org/beta/papers/v23/20-1165.html

A later informed-POMDP treatment states a closely related sufficient condition: recurrent state plus predictive sufficiency for reward and next information given action.

**Consequence:** #51 cannot claim novelty for the generic proposition

> recurrent + predictive/decision sufficient state supports future decisions.

The dynamic residual, if any, must be specifically the **relative state requirement beyond a linguistic predictive quotient**, prospective epistemic-optionality diagnostic, and responsibility-family/horizon interpretation.

### Correction B — minimal state for one learned target losing future downstream information is already occupied

Wang, Guo, Deng & Lu, **Rethinking Minimal Sufficient Representation in Contrastive Learning**, CVPR 2022, explicitly argues/theoretically analyzes that a minimal sufficient representation for the contrastive/shared training target can lose non-shared information relevant to downstream tasks.

Primary sources:

- https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.html
- https://arxiv.org/abs/2203.07004

**Consequence:** the broad claim

> minimal sufficiency for the training target may harm unregistered downstream tasks

is not a #51 novelty.

This strengthens the need for `RESPONSIBILITY_UNIVERSALITY_BOUND_V1.md`: the paper should ask how the **declared responsibility family** controls the extra state required beyond linguistic prediction, not claim discovery of generic downstream-task insufficiency.

---

# 2. Parent-by-parent adjudication

## P1 — Computational mechanics / causal states

**Owns:**

- equivalence of histories by complete future law;
- minimal predictive state;
- uniqueness/minimality under standard assumptions;
- recursive calculability of causal state.

**#51 credit after subtraction:** none for the base predictive quotient.

## P2 — Predictive State Representations / Reward-Predictive State Representations

Baisero & Amato, IJCAI 2021:

- https://www.ijcai.org/proceedings/2021/299
- https://arxiv.org/abs/2106.03926

**Owns:**

- observation-predictive state can be insufficient for reward;
- necessary/sufficient reward accuracy condition;
- augmenting state to preserve reward;
- downstream policy consequences of reward-inaccurate predictive state.

**#51 credit after subtraction:** T1 is background; raw “prediction ≠ secondary target sufficiency” is not novel.

## P3 — Information Bottleneck / Deterministic Information Bottleneck

Strouse & Schwab, Neural Computation 2017:

- DOI `10.1162/NECO_a_00961`.

**Owns:** minimal deterministic task-sufficient representation/compression ideas.

**#51 credit after subtraction:** entropy-minimal predictive representation logic is bridge/background; not main novelty.

## P4 — Minimal sufficient representation versus downstream tasks

Wang et al., CVPR 2022:

**Owns:** theoretical risk that minimal sufficiency for the representation-learning target drops non-shared downstream task-relevant information.

**#51 credit after subtraction:** generic future-task vulnerability of minimal compression is parent-owned.

## P5 — Multi-task information-theoretic sufficiency

Hu et al., AAAI 2025, **An Information-theoretic Multi-task Representation Learning Framework for Natural Language Understanding**:

- https://ojs.aaai.org/index.php/AAAI/article/view/33899

**Owns:** shared representations designed to be sufficient for multiple tasks and task-specific compression considerations.

**#51 credit after subtraction:** “add multiple tasks to preserve multiple task signals” is not novel.

## P6 — Approximate information state / recurrent sufficient statistics

Subramanian et al., JMLR 2022:

**Owns:**

- information state as history compression for sequential decisions;
- recursively updateable sufficient state;
- reward and next-observation predictive conditions;
- approximate information-state theory with performance bounds.

This is the strongest newly identified threat.

**#51 credit after subtraction:** generic dynamic/recurrent sufficiency is not novel. Any dynamic claim must emphasize:

1. a **linguistic predictive state as the explicit base quotient**;
2. the **relative extra state** required by an epistemic responsibility family;
3. a distinction between current decision sufficiency and known future responsibility schedules;
4. acquisition/compression/prospective deficit separation;
5. responsibility-family universality bound.

Even these remain provisional until full-theorem comparison.

## P7 — POMDP belief/information state

Classical POMDP theory treats the belief state as a sufficient statistic for future control under a known model. This is a broader historical parent of P6.

**#51 credit after subtraction:** no novelty for the idea that historical information needed for future decisions must be retained in a recursively updated state.

## P8 — Myhill–Nerode / right congruence / automata minimization

**Owns:** coarsest recursively updateable deterministic state respecting an output partition and partition refinement.

**#51 credit after subtraction:** T10–T12 mathematical substrate is not independently novel.

## P9 — Log-loss rate-distortion

Courtade & Weissman, IEEE TIT 2014:

- DOI `10.1109/TIT.2013.2288257`.

**Owns:** log-loss rate-distortion structure and multiterminal regions.

**#51 credit after subtraction:** T8A/T8B are benchmarks/background, not abstract claims.

## P10 — Current LLM hidden-state epistemics

Cheang et al., Findings ACL 2026:

- https://aclanthology.org/2026.findings-acl.34/

shows hidden states may track knowledge recall rather than truthfulness in important hallucination regimes.

Other 2025/2026 belief/factuality work shows internal signals and, in some cases, causal use.

**#51 credit after subtraction:** do not claim LLM hidden states are epistemically empty; instead define stronger current/prospective sufficiency tests.

---

# 3. Revised theorem-credit table

| Result | Pass-02 disposition |
|---|---|
| minimal full-future predictive state | `PARENT_OWNED` |
| predictive state may miss epistemic responsibility | `PARENT_OWNED_PATTERN` via R-PSR/task sufficiency |
| entropy-minimal predictive representation | `PARENT_OWNED_OR_DIRECT_COROLLARY` |
| exact `H(Q|S_P)` full-target overhead | `CLEAN_COROLLARY / PACKAGE_COMPONENT` |
| responsibility-decision quotient `H(C_R|S_P)` | `CANDIDATE_RELATIVE_STATE_FORMULATION` |
| acquisition/compression log-loss decomposition | `PARENT_OWNED_IDENTITY / DIAGNOSTIC_ONLY` |
| recurrent sufficient state / right congruence | `PARENT_OWNED_SUBSTRATE` |
| current-sufficient but future-revision-insufficient distinction | `CANDIDATE_INTERPRETIVE_RESIDUAL_HIGH_PARENT_PRESSURE` |
| dynamic optionality cost relative to current predictive-responsibility state | `PRIMARY_CANDIDATE_RELATIVE_STATE_QUANTITY` |
| prospective deficiency `I(Q_future;H_now|Z_now,X_future)` | `PARENT_IDENTITY / CANDIDATE_DIAGNOSTIC_USE` |
| unrestricted responsibility family forces full-history retention | `CANDIDATE_NEGATIVE_DESIGN_THEOREM / LIKELY_CLASSICAL_COROLLARY` |
| responsibility-family growth curve | `CANDIDATE_ANALYTICAL_FRAMEWORK` |

---

# 4. Strongest surviving paper question after Pass 02

The paper should no longer ask merely:

> Is prediction sufficient for epistemic state?

That is too close to existing task-state theory.

The sharper question is:

> **Given a state already sufficient for the complete linguistic future, what additional information must be retained for a declared family of epistemic decisions now and under a declared future responsibility horizon; how much of the non-predictive history does that family make load-bearing; and how can failure be separated into missing evidence, current compression loss, and lost future revision optionality?**

This is now the governing paper identity.

---

# 5. JMLR viability after Pass 02

JMLR remains possible but **high risk**.

Why it remains possible:

- JMLR explicitly accepts new analytical frameworks and theoretical studies that change understanding of learning-system design;
- the responsibility-relative, prospective-state audit may provide a useful evaluation framework for compressed/distilled/continually used language models;
- no expensive LLM training is required if the theory is independently complete and its ML consequence is clear.

Why it may fail:

- P6 (Approximate Information State) already occupies a large part of recurrent sufficient-state theory at JMLR depth;
- P2/P4 already occupy prediction-target versus downstream-target insufficiency;
- P3/P5 occupy compression and multi-task sufficiency;
- P8 owns state recursion/minimization.

Thus the final paper must demonstrate that the **relative epistemic responsibility/horizon formulation gives a non-obvious theorem or evaluation consequence not already obtained by simply declaring responsibility variables as rewards/information state.**

If it cannot, route to `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY` or merge into the ORION-V2 foundation.

---

# 6. What the mechanical bibliography AI is still allowed to do

The remaining literature executor has no discretion over the scientific argument. It should only:

1. fetch complete citation metadata;
2. locate exact theorem/proposition numbers and assumptions in the parents above;
3. search for missing direct parents using the frozen search terms;
4. mark each registered #51 claim as `PARENT_OWNED`, `PARTIAL_OVERLAP`, or `NO_DIRECT_OVERLAP`;
5. return exact source passages/theorem references within copyright limits;
6. never upgrade novelty merely because keyword search finds no identical phrase.

The scientific response to each parent is already frozen in `HOSTILE_REVIEW_DECISION_MATRIX_V1.md`.
