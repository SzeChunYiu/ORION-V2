# Beyond Predictive Sufficiency: Cross-Channel and Prospective Epistemic State for Autoregressive Models

**Pre-mechanization manuscript draft V4**  
**Issue:** #51  
**Supersedes:** manuscript drafts V1–V3.  
**Status:** candidate theory under formal and strongest-parent audit.  
**Empirical LLM training evidence:** none required or claimed.  
**Primary venue aspiration if all gates pass:** JMLR.

---

## Abstract

A state sufficient for language prediction need not contain every variable required by a system's later epistemic decisions. Yet this statement alone is not new: predictive-state, reward-predictive-state, multi-task, information-bottleneck and decisional-state theories already establish strong forms of target-relative sufficiency. We study a narrower representation question for autoregressive systems. Let \(S_P\) be the minimal state sufficient for the **complete linguistic future**. An epistemic responsibility is a separate decision contract whose optimal action may depend on source identity, evidence dependence, scope, lineage, evaluator state or other information not measurable from the linguistic future. For `ANY_OPTIMAL_ACTION`, the minimum exact static state beyond \(S_P\) is the minimum, over Bayes-optimal selectors \(d\), of \(H(d(H)\mid S_P)\). If some optimal policy is already a function of \(S_P\), this cost is zero—a regime closely related to Brodu's causal/decisional states, where utility-defined decisions coarsen predictive causal states. Positive cost therefore identifies a **cross-channel responsibility obstruction** rather than generic decision complexity. We then impose future updateability. Static admissible state partitions refine \(S_P\) and admit a common optimal responsibility action; dynamic admissible partitions additionally satisfy transition congruence. Their minimum conditional entropies \(C_{\mathrm{stat}}^\*\) and \(C_{\mathrm{dyn}}^\*\) define a dynamic optionality premium \(\Omega_{\mathrm{dyn}}=C_{\mathrm{dyn}}^\*-C_{\mathrm{stat}}^\*\). Equivalently, the dynamic optimum is obtained by minimizing, over Bayes-optimal selectors, the entropy of the coarsest right-congruent refinement of the predictive-policy state. A canonical provenance process has zero current extra state but a one-bit dynamic premium: source identity is irrelevant to present prediction and action yet becomes necessary after a later retraction. We organize exact finite systems into predictive-decisional, static cross-channel, and prospective-refinement phases and define a monotone horizon-indexed state-cost curve. We also distinguish acquisition, current compression and prospective revision deficits, and show that unrestricted exact responsibility families eliminate nontrivial compression. The finite-state minimization substrate is strongly parent-owned by decision theory, causal/decisional states, information-state control and incompletely specified FSM minimization. The proposed residual is the **cross-channel, responsibility-relative, horizon-relative state accounting and prospective representation audit** for language-model-like systems. We do not claim that current LLMs are minimal predictive states, lack belief-like representations, or necessarily discard epistemic information.

---

# 1. Introduction

The phrase “the model knows” often compresses several distinct questions.

A language model may have enough information to predict its next or future text accurately. A deployment may additionally require it to decide whether a claim should be answered, left unresolved, reopened after a source correction, or supported by further evidence. Those decisions can depend on information that is irrelevant to the distribution of future language itself.

Consider two histories with the same complete linguistic future distribution and the same current answer. One answer rests on source \(A\), the other on source \(B\). Suppose source identity has no effect on future token probabilities. Then a minimal linguistic predictive state may collapse the histories. If a later observation reports that \(A\) has been retracted, a system that retained only the linguistic predictive state cannot necessarily determine which conclusion to reopen.

This scenario is intentionally **not** a claim that ordinary LLMs behave this way. Their hidden states are large and may retain far more information than a minimal predictive statistic. The theoretical point is that linguistic prediction and epistemic responsibility are different channels of relevance.

That distinction has strong prior art. Computational mechanics defines causal states sufficient for the future. Predictive State Representations and Reward-Predictive State Representations show that a state sufficient for one predictive target may omit information required by another decision target. Information Bottleneck and multi-task representation theory formalize task-relative compression. Brodu's decisional-state framework is especially direct: causal states are grouped by user-provided utility into iso-prediction, iso-utility and decisional states, with an entropy-like decisional complexity and transitions between decision states. POMDP belief states and Approximate Information State theory already address recurrent sufficient state for future control. Incompletely specified FSM minimization already studies compatible outputs and minimal recurrent state when several outputs/actions are acceptable.

These parents change what can legitimately be claimed. If an epistemic decision is computed entirely from the same future distribution represented by \(S_P\), Brodu-like theory already implies that decision state is a coarsening of the causal state; no additional information beyond \(S_P\) is needed. Our positive state cost therefore arises only when the responsibility uses information **not measurable from the declared linguistic predictive state**.

We call such a responsibility *cross-channel* as shorthand. This does not mean statistically independent. It means the optimal responsibility decision is not implementable from the linguistic predictive quotient alone.

The second distinction is temporal. Even after the optimal current responsibility state has been compressed as aggressively as possible, future observations may require distinctions that are irrelevant today. This creates a potential state cost that is neither current prediction information nor current decision information.

The paper asks:

> **How much extra state is required beyond complete linguistic prediction for a declared epistemic decision, and how much additional state is required for some Bayes-optimal decision policy to remain updateable over a declared future horizon?**

## 1.1 Contributions under test

The paper's candidate residual is a package rather than ownership of its classical pieces.

1. **Cross-channel static state cost.** Under an explicit responsibility decision contract, quantify the minimum extra state beyond \(S_P\). For any-optimal-action semantics this is the minimum conditional entropy of a Bayes-optimal selector.
2. **Brodu-like zero-cost regime.** If some Bayes-optimal responsibility policy is a function of \(S_P\), extra static cost is zero. Positive cost therefore has a precise interpretation: no current optimal responsibility policy factors through the linguistic predictive state.
3. **Joint policy/recurrent-state optimization.** Define current state through action-compatible partitions and future state through action-compatible right-congruent partitions; optimize tied Bayes actions and state jointly.
4. **Dynamic optionality premium.** Compare optimal static and dynamic state costs after policy optimization.
5. **State phases and horizon curve.** Classify systems into predictive-decisional, static cross-channel and prospective-refinement regimes and define \(C_k^\*\) over a future responsibility horizon.
6. **Typed deficits and bounded responsibility.** Separate missing evidence, current compression and future revision loss, and show why unrestricted exact future responsibilities force history-retaining state.
7. **Representation evaluation consequence.** Propose a prospective hidden-state/compression audit: matched linguistic performance and matched current responsibility performance can still conceal loss of revision capability after controlled future evidence.

Whether this package is sufficient for a standalone top-tier theory paper is itself an explicit falsifiable question.

---

# 2. Predictive and decisional parents

Let \(H\) be finite history and \(Y^+\) the complete linguistic future. Define

\[
h\sim_P h'\iff P(Y^+\mid h)=P(Y^+\mid h')
\]

and let \(S_P\) be the resulting predictive quotient. We attribute its minimality/sufficiency to classical causal/predictive-state theory.

Brodu's decisional states supply a crucial control case. Given a fixed utility over outcomes predicted from the causal state, one can group causal states according to the same optimal prediction and maximal expected utility. The resulting decision partition is coarser than the causal-state partition. In the discrete case, the entropy of the decisional state quantifies its decision complexity.

Therefore:

> **If the epistemic decision is fully determined by the linguistic future distribution, no additional state beyond the complete linguistic predictive state is needed.**

This negative control is mandatory in every interpretation of our theory.

The paper only needs a refinement of \(S_P\) when responsibility decisions depend on additional history-side variables. Examples can include source/evidence topology, scope lineage, obligation identity, evaluator version, or another non-linguistic information channel.

---

# 3. Epistemic responsibility contracts

A responsibility is

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where \(Q\) is an externally/mechanically specified epistemic target, \(\mathcal A\) the admissible action set, \(\ell\) a loss, and \(\sigma\) exact decision semantics.

We distinguish:

- `ANY_OPTIMAL_ACTION`;
- `CANONICAL_ACTION`;
- `OPTIMAL_ACTION_SET`;
- `ACTION_AND_RISK`;
- `EXACT_TARGET`.

For history \(h\), let

\[
A^\*(h)=\arg\min_a \mathbb E[\ell(a,Q)\mid h].
\]

Under `ANY_OPTIMAL_ACTION`, any selector \(d(h)\in A^\*(h)\) is permitted. This matters under ties: if two histories have optimal sets \(\{a,b\}\) and \(\{b,c\}\), one common action \(b\) makes them decision-compatible even though their full option sets differ.

The target \(Q\) therefore need not itself be stored unless exact target recovery is part of the responsibility.

---

# 4. Static cross-channel state

Let \(\mathcal D\) be all Bayes-optimal selectors. The minimum exact additional deterministic state entropy beyond retained \(S_P\) is

\[
\boxed{
C_{\mathrm{stat}}^\*
=
\min_{d\in\mathcal D}H(d(H)\mid S_P).
}
\]

Equivalently, partition histories into blocks that:

1. lie inside one \(S_P\) fibre;
2. have a nonempty intersection of Bayes-optimal action sets.

Minimize partition conditional entropy given \(S_P\).

The equivalence follows because a selector induces the partition \((S_P,d)\), while any action-compatible block partition permits one common optimal action per block and may merge further when equal chosen actions allow it.

## 4.1 Zero-cost regime

\[
C_{\mathrm{stat}}^\*=0
\]

iff there exists a Bayes-optimal selector \(d(h)=\bar d(S_P(h))\). Equivalently, every predictive fibre has at least one common Bayes-optimal responsibility action.

This includes the standard Brodu-like regime where the responsibility is computed from the same predicted future distribution.

## 4.2 Positive cross-channel regime

\[
C_{\mathrm{stat}}^\*>0
\]

iff no Bayes-optimal responsibility policy factors through \(S_P\). In at least one predictive fibre, the responsibility requires a decision distinction absent from the linguistic predictive state.

This is the precise meaning of a positive static Machine-Epistemic state cost in the paper.

---

# 5. Dynamic state and joint policy optimization

Let \(\delta(h,x)\) be a deterministic partial transition after future observation \(x\).

A static action-compatible partition is **dynamically admissible** when equivalent histories have matching transition definedness and their successors remain equivalent under every input. Such a partition defines a deterministic recurrent state and a common Bayes-optimal action per block.

Define

\[
C_{\mathrm{dyn}}^\*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_P).
\]

This minimizes state and current tie selection jointly.

For an alternative exact computation, fix each Bayes-optimal selector \(d\), form the base label \((S_P,d)\), compute its coarsest right-congruent refinement \(S_\infty^d\), and minimize:

\[
\boxed{
C_{\mathrm{dyn}}^\*
=
\min_{d\in\mathcal D}
H(S_\infty^d\mid S_P).
}
\]

This selector-refinement route is equivalent to direct dynamic partition optimization in the registered finite deterministic setting.

The underlying compatible-state/right-congruence minimization is closely related to classical incompletely specified FSM minimization. We do not claim a new minimization algorithm.

---

# 6. Dynamic epistemic optionality premium

Define

\[
\boxed{
\Omega_{\mathrm{dyn}}
=C_{\mathrm{dyn}}^\*-C_{\mathrm{stat}}^\*.
}
\]

Since every dynamic-admissible partition is static-admissible,

\[
\Omega_{\mathrm{dyn}}\ge0.
\]

The premium is the minimum additional average state required **only because an optimal current responsibility policy must remain recursively implementable under future observations**.

## 6.1 One-bit provenance witness

Two equally likely current histories:

- share one linguistic predictive state;
- share one unique current optimal responsibility action;
- differ in a provenance bit irrelevant to current action.

A future observation sends them to successor histories with distinct unique optimal actions.

Then

\[
C_{\mathrm{stat}}^\*=0,
\qquad
C_{\mathrm{dyn}}^\*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit}.
\]

The premium survives optimization over current action ties because the current action is unique. It isolates future revision optionality.

---

# 7. Responsibility state phases

Define \(C_0^\*=C_{\mathrm{stat}}^\*\) and \(C_\infty^\*=C_{\mathrm{dyn}}^\*\).

## P0 — predictive-decisional

\[
C_0^\*=0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The linguistic predictive state is enough for the current responsibility and its future update process. This is the strongest Brodu-like/no-extra-state control.

## P1 — static cross-channel refinement

\[
C_0^\*>0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

Additional non-linguistic/history-side state is needed for the current responsibility, but the optimal current responsibility state is already recursively sufficient.

## P2 — prospective refinement

\[
\Omega_{\mathrm{dyn}}>0.
\]

Even the optimally compressed current responsibility state is insufficient for the registered future responsibility process.

P2 can occur with \(C_0^\*=0\) or \(C_0^\*>0\).

These phases classify representation obligations, not “levels of intelligence”.

---

# 8. Horizon-indexed state curve

For horizon \(k\), let \(\mathfrak P_k\) contain static action-compatible partitions whose equivalent histories remain in the same compressed state after every jointly defined input word of length at most \(k\).

Define

\[
C_k^\*=\min_{\Pi\in\mathfrak P_k}H(\Pi(H)\mid S_P).
\]

Then

\[
C_0^\*\le C_1^\*\le\cdots\le C_\infty^\*.
\]

Define

\[
\Omega_k=C_k^\*-C_0^\*.
\]

Finite systems stabilize. The smallest \(k\) with \(C_k^\*=C_\infty^\*\) is the registered finite **epistemic memory horizon** \(K_{\mathrm{epi}}\).

The monotonicity is a simple nested-feasible-set result. The usefulness, if any, lies in exposing when future responsibility demands become state-relevant.

---

# 9. Acquisition, compression and prospective deficiency

For target \(Q\) under log loss and representation \(Z=f(H)\):

\[
H(Q\mid Z)=H(Q\mid H)+I(Q;H\mid Z).
\]

We call these terms acquisition deficit and current compression deficit respectively.

For future target \(Q_{t+k}\) after future observations \(X_{t+1:t+k}\):

\[
\Delta_k
=
I(Q_{t+k};H_t\mid Z_t,X_{t+1:t+k}).
\]

This is the information-theoretic prospective deficit.

The identities are classical. Their role is diagnostic:

- acquisition deficit -> obtain new evidence;
- compression deficit -> preserve current responsibility information;
- prospective deficit -> preserve or re-acquire future revision information.

A system can have zero current compression deficit and positive prospective deficit.

---

# 10. Bounded responsibility universality

For a fixed-signature responsibility family \(C_{\mathcal R}(H)\):

\[
0\le H(C_{\mathcal R}\mid S_P)\le H(H\mid S_P).
\]

When the family distinguishes every history pair within predictive fibres, it determines the full history given \(S_P\) and reaches the upper bound.

Any non-injective compressed state also admits an exact binary responsibility constructed to differ on a collided pair, so unrestricted exact responsibility universality precludes nontrivial compression.

Thus all claims of “epistemically sufficient state” must be relative to a responsibility family and horizon.

---

# 11. Approximate benchmark

For deterministic exact target \(Q=q(H)\), the conditional log-loss frontier

\[
R(D)=\inf I(H;U\mid S_P)
\quad\text{s.t.}\quad
H(Q\mid S_P,U)\le D
\]

is the classical

\[
R(D)=[H(Q\mid S_P)-D]_+.
\]

It is included as a parent-owned calibration benchmark only.

---

# 12. Implications for LLM representation evaluation

The theory suggests a sequence of questions at matched linguistic predictive performance.

### Test A — acquisition
Is the responsibility identifiable from the full accessible context/history?

### Test B — cross-channel static state
Does a language-preserving representation contain enough additional information to implement a Bayes-optimal responsibility policy? If yes with zero extra state, the system is P0-like; if not, it requires P1/P2 cross-channel refinement.

### Test C — prospective revision
After controlled future evidence, can the compressed state update the responsibility correctly without reconstructing discarded history? A failure here with current responsibility preserved is the empirical analogue of P2.

### Test D — state cost
What representation memory/rate is required to preserve each capability?

This is stronger than asking whether a truth/confidence direction is linearly decodable at one time slice.

---

# 13. Parent threats and publication gate

The standalone paper faces severe parent pressure.

- Brodu 2011 owns causal-to-decisional coarsening, optimal prediction/utility states, decisional complexity and decision-state transitions.
- R-PSR owns prediction state versus reward-target insufficiency.
- DIB and multi-task representation own much task-relative compression.
- CVPR 2022 minimal-sufficient representation work owns generic downstream information loss from target-specific compression.
- Approximate Information State (JMLR 2022) owns substantial recurrent sufficient-state theory and approximation guarantees.
- POMDP belief states own classical recursive decision sufficiency.
- right congruence and incompletely specified FSM minimization own generic compatible recurrent-state reduction.
- log-loss rate distortion owns the simple approximate frontier.

Therefore JMLR submission is authorized only if theorem-level reconstruction leaves a non-obvious consequence in the **cross-channel state cost + dynamic optionality premium + phase/horizon representation audit** package.

If not, the correct terminal is parent sufficiency or field-theory/flagship integration.

---

# 14. Verification programme

No open-ended theory design remains in the execution phase.

The executor will:

- formal-check the registered static/dynamic equivalences;
- enumerate Bell-complete small partitions;
- enumerate optimal action selectors;
- compute static and dynamic minima independently;
- verify selector-refinement equality;
- verify P0/P1/P2 fixtures and the one-bit premium;
- compute horizon curves and stabilization;
- attack assumptions with minimal counterexamples;
- verify bounded-responsibility saturation;
- locate exact theorem/definition ownership including Brodu's decisional states and incomplete-FSM minimization.

The executor may narrow/delete claims forced by evidence. It may not invent a replacement theorem or novelty defense.

---

# 15. Conclusion

Predictive sufficiency is not a universal notion of state adequacy, but neither is every additional decision variable evidence for a new epistemic theory. Classical decisional-state theory shows that if a decision is determined by the same future distribution represented by a causal state, decision state can be a coarsening rather than an augmentation. Positive additional state is therefore meaningful only for responsibilities that depend on distinctions outside the linguistic predictive channel.

For such cross-channel responsibilities, the current state cost is the minimum information needed to implement an acceptable Bayes policy. Future revision can impose a further premium: current histories that are decision-equivalent may need to remain separate because later evidence makes their descendants decision-incompatible. The dynamic optionality premium measures that exact finite cost after optimizing over tied Bayes actions.

The resulting P0/P1/P2 phase framework asks a concrete question of language-model representations: **is the linguistic state enough, is additional state needed only for current epistemic action, or is further state needed solely to preserve future revision capability?** Whether this framework is novel enough for a standalone top-tier theory paper remains deliberately contingent on the formal and strongest-parent audits.
