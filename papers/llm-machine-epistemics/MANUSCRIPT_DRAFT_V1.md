# Beyond Predictive Sufficiency: Static and Prospective Epistemic State Requirements for Autoregressive Models

**Pre-mechanization manuscript draft — ORION-V2.LLM-MACHINE-EPISTEMICS.THEORY.V1**  
**Issue:** #51  
**Status:** theory manuscript whose theorem wording remains candidate until the registered formal/countermodel checks complete.  
**Empirical performance claims:** none.  
**Primary target if the residual survives:** Journal of Machine Learning Research.

---

## Abstract

Autoregressive models are trained and evaluated primarily through prediction of linguistic continuations, yet deployed systems are also asked to make and revise epistemically consequential decisions: distinguish supported from unresolved claims, track source dependence, abstain under non-identifiability, preserve scope conditions, and reopen conclusions when later evidence defeats their support. These requirements concern the information carried by internal state, not only predictive accuracy. We develop a finite-state theory that separates **linguistic predictive sufficiency** from **epistemic responsibility sufficiency**. Let \(S_P\) denote the minimal state sufficient for the complete linguistic future. A responsibility is represented by a registered decision contract, rather than an arbitrary auxiliary label. In the deterministic exact setting, the coarsest state sufficient for both language prediction and a responsibility family is the common refinement of \(S_P\) and the responsibility-decision quotient; its additional average state cost is the corresponding conditional entropy. Thus maximal compression to a minimal predictive state can be incompatible with a responsibility whenever responsibility-relevant distinctions vary inside predictive fibres. More importantly, static joint sufficiency need not support future revision. We characterize the minimal exact recursively updateable state as the coarsest right-congruent refinement of the current predictive–responsibility state and define its additional entropy as a **dynamic epistemic optionality cost**. A canonical construction has zero current responsibility overhead yet requires one bit solely to revise correctly after a later observation. We further distinguish acquisition deficit, representation-compression deficit, and prospective revision deficit. The underlying results draw deliberately on classical sufficient-statistic, predictive-state, information-theoretic, decision-theoretic and automata theory; the proposed contribution is a responsibility-relative internal-state formulation for autoregressive models and a testable separation between current and prospective epistemic adequacy. We do not claim that present LLMs are minimal predictive states, lack belief-like internal structure, or require a particular neural architecture.

---

# 1. Introduction

A language model can answer a question correctly today and still be in the wrong internal state for tomorrow.

Consider two histories that lead to the same present answer and the same distribution over future linguistic continuations relevant to a prediction objective. In one history, the answer ultimately depends on source \(A\); in the other, it depends on source \(B\). Suppose the source distinction changes neither today's wording nor today's registered decision. A representation optimized only for current prediction and current decision may therefore collapse the histories. If a later observation reports that source \(A\) has been retracted, however, the system must reopen one conclusion and retain the other. Once the source distinction has been discarded, the new observation alone may be insufficient to reconstruct which commitment depended on which source.

This example separates three questions that are often conflated in discussions of language-model knowledge.

1. **Was the required information available at all?** If the accessible history contains no information capable of distinguishing the relevant epistemic states, no internal computation can manufacture the missing observation.
2. **Was available information retained by the representation?** A compressed state may be perfectly sufficient for the language prediction target while discarding information required for a separate responsibility.
3. **Was apparently irrelevant information retained for future revision?** A distinction may have no current predictive or decision value yet acquire value after a later observation.

The first is an acquisition problem. The second is a representation problem. The third is a sequential-state or optionality problem.

The distinction matters because modern language models are routinely evaluated along all three axes while being described through one vocabulary of “knowledge”, “confidence”, “truthfulness” or “hallucination”. Hidden-state work has found representations correlated with factuality, confidence, knowledge recall and belief-like variables, and recent studies have gone beyond linear decoding to causal interventions. Those findings make a strong negative thesis—“LLMs contain no internal epistemic structure”—untenable. They leave a different theoretical question open:

> **What information must an internal state retain before it is sufficient for a declared epistemic responsibility, and what additional information is required if the state must remain correct under future evidence?**

We answer this question in a finite/discrete setting, with deliberately limited claims. The base predictive object is not new: we use the classical equivalence relation that groups histories inducing identical laws over the full linguistic future, yielding a minimal predictive state \(S_P\) under standard assumptions. The decision-theoretic fact that a less informative statistic cannot outperform a more informative one is also classical. So are conditional mutual-information identities, deterministic information bottleneck ideas, log-loss rate-distortion results, right-congruence/automaton minimization, and belief-state recursion.

Our goal is not to rename these foundations. It is to use them to make a specific representation question precise for autoregressive systems that are expected to carry epistemic responsibilities in addition to predicting text.

## 1.1 Contributions

Subject to the registered proof and nearest-work checks, this paper develops the following package.

**Predictive versus responsibility state.** We distinguish the minimal state sufficient for the entire linguistic future from the state sufficient for a declared family of epistemic **decision contracts**. A responsibility contract specifies an epistemic target, admissible epistemic actions and a loss. This makes state requirements decision-relative rather than equating epistemic competence with full recovery of every auxiliary variable.

**Exact static state overhead.** In the finite deterministic setting, the coarsest state preserving both linguistic predictive sufficiency and exact responsibility decisions is their common refinement. The minimum extra average state entropy beyond \(S_P\) is

\[
H(C_{\mathcal R}\mid S_P),
\]

where \(C_{\mathcal R}\) is the joint responsibility-decision signature. Exact recovery of a target \(Q\) is the special case \(C_{\mathcal R}=Q\), giving \(H(Q\mid S_P)\).

**Compression consequence.** Every entropy-minimal deterministic representation that is exactly sufficient for the complete linguistic future is isomorphic to the minimal predictive state. Therefore, if a declared responsibility is not measurable from that state, **maximal prediction-preserving compression cannot simultaneously preserve the responsibility**. We treat the minimal-sufficiency mathematics as classical and use the result as a design consequence, not as a claim that ordinary transformer pretraining produces an entropy-minimal state.

**Static versus prospective sufficiency.** A state can preserve both the complete linguistic predictive state and all current epistemic decisions while still being insufficient for correct future revision. We define a finite-horizon refinement and show that its stable limit is the coarsest right-congruent refinement of the current predictive–responsibility partition. The resulting

\[
H(S_\infty\mid S_0)
\]

is the additional average state required solely for exact recursive update of the declared future responsibilities. The underlying right-congruence theorem is classical automata/state-minimization structure; the proposed contribution is the **prospective epistemic interpretation and state-cost formulation**.

**Three typed deficits.** Under logarithmic loss we distinguish acquisition deficit \(H(Q\mid H)\), compression deficit \(I(Q;H\mid Z)\), and prospective deficit

\[
I(Q_{t+k};H_t\mid Z_t,X_{t+1:t+k}).
\]

The identities are classical; the point is that the deficits require different interventions and should not be collapsed into a scalar confidence score.

**Mechanically falsifiable boundaries.** Every exact theorem is accompanied by a finite countermodel/partition-refinement programme, and every novelty claim is pre-registered against causal states, Predictive State Representations, Reward-Predictive State Representations, statistical sufficiency/Blackwell comparison, deterministic information bottleneck, multi-task sufficient representation, log-loss rate distortion, POMDP/information-state theory, and Myhill–Nerode/right-congruence theory.

## 1.2 What we do not claim

We do not claim that current LLMs are stochastic parrots, that they fail to learn internal world or belief structure, or that a cross-entropy objective forces all non-predictive information out of a transformer. Actual hidden states are high-dimensional, redundant and generally far from entropy-minimal sufficient statistics. Prediction behavior also does not identify arbitrary internal representation properties.

We therefore make a weaker but cleaner statement:

> **Linguistic predictive sufficiency, current epistemic responsibility sufficiency, and prospective epistemic revision sufficiency are distinct representation requirements. None follows in general from the preceding one.**

We also do not claim that an internal state can manufacture institutional authority. Scientific or institutional permission remains external to the model.

---

# 2. Related foundations and ownership boundaries

The paper sits at an intersection where overclaiming is easy. We therefore organize related work by **theorem ownership**.

## 2.1 Statistical sufficiency and comparison of experiments

Classical sufficient-statistic theory asks when a statistic preserves all information relevant to a target family. Blackwell comparison and Le Cam-style decision theory formalize relative informativeness through achievable risks across decision problems. These theories own the central principle that information discarded by a statistic can create irreducible decision loss.

Our responsibility-risk definition is a direct use of this machinery. The proposed residual is not Bayes-risk monotonicity but its specialization to an autoregressive **linguistic predictive state plus epistemic responsibility state**, and especially the prospective revision requirement developed below.

## 2.2 Computational mechanics and predictive-state representations

Computational mechanics defines causal states by grouping histories that induce the same conditional law over the future. Under its assumptions, causal states are minimal sufficient statistics for prediction and recursively calculable. Predictive State Representations provide related observable-history states for controlled dynamical systems.

We grant this ownership completely. Our \(S_P\) is an application of the predictive-state idea to the declared full linguistic future. No novelty is claimed for the quotient or its minimality.

A closer threat is Reward-Predictive State Representations. Baisero and Amato show that a PSR sufficient for observations need not represent rewards correctly and construct R-PSRs that model both. This directly owns the broad observation that “a state sufficient for one target can be insufficient for another.” Consequently our basic predictive-versus-epistemic separation is foundation, not the sole paper contribution.

The question left for this paper is whether epistemic responsibilities introduce a useful **state-cost and prospective-update** structure when language prediction is the base target.

## 2.3 Information bottleneck and minimal sufficient representation

The Information Bottleneck and Deterministic Information Bottleneck formalize task-relevant representation compression. Multi-task representation learning similarly studies states sufficient for several targets. These areas own the idea that compressing task-irrelevant information can harm an unregistered secondary task.

Our compression theorem should therefore be read as a corollary with a specific implication: if one compresses all the way to a minimal state for the linguistic future, a responsibility distinction not measurable from that state cannot survive. This becomes scientifically interesting only when combined with decision-relative responsibility cost and prospective revision.

## 2.4 Log-loss rate distortion

For probabilistic prediction under logarithmic loss, entropy-minus-distortion relations are classical; Courtade and Weissman give major multiterminal results under log loss. We use the corresponding conditional log-loss frontier as a closed-form benchmark. It is not claimed as new information theory.

## 2.5 Automata, right congruence and recursive state

The coarsest recursively updateable finite state respecting an output partition is classical automata/state-minimization territory: Myhill–Nerode equivalence, right congruence, partition refinement and related notions such as bisimulation. Computational mechanics likewise studies recursively calculable predictive states.

Our dynamic theorem uses this substrate. The possible residual is the **epistemic optionality interpretation**: a state already sufficient for current prediction and current epistemic decisions may require further refinement solely because future evidence can make a currently dormant distinction relevant to revision.

## 2.6 Internal belief, truth and uncertainty representations in LLMs

Recent work reports hidden-state representations linked to belief, factuality, knowledge recall and uncertainty. Herrmann and Levinstein propose standards for belief representation that go beyond decodability; work such as *LLM Beliefs Are in Their Heads* provides evidence of causally usable internal structure, while other studies caution that apparent self-knowledge signals can track parametric recall rather than truthfulness.

These findings motivate rather than contradict our theory. We do not ask whether some direction in activation space correlates with a label. We ask whether an internal state is **sufficient for a declared decision responsibility now and after future evidence**.

## 2.7 Representation identifiability

Recent representation-identifiability work formalizes the fact that predictor behavior need not determine internal representation properties. This blocks a tempting but invalid inference: two models with equal language loss need not have equal epistemic state. Our theory therefore concerns state requirements and impossibility under declared compression constraints; it does not infer hidden epistemic properties from behavior alone.

---

# 3. Formal setting

We begin with a finite setting to make every theorem mechanically checkable.

Let \(H\) be the random variable representing the history/information accessible to the model at a declared time. Let \(Y^+\) denote the **complete linguistic future** relevant to the predictive process. Let

\[
Z=f(H)
\]

be a deterministic internal representation unless a theorem explicitly allows stochastic augmentation.

## 3.1 Linguistic predictive sufficiency

A representation \(Z\) is linguistically predictive-sufficient when

\[
Y^+\perp H\mid Z.
\]

Define predictive equivalence

\[
h\sim_P h'
\iff
P(Y^+\mid H=h)=P(Y^+\mid H=h').
\]

Let

\[
S_P=[H]_{\sim_P}.
\]

Under the finite setup, every deterministic predictive-sufficient state refines \(S_P\): if two histories share a \(Z\) value, predictive sufficiency requires them to induce the same future law.

This is the familiar minimal predictive quotient.

---

# 4. Epistemic responsibilities are decisions, not arbitrary labels

A major danger is to call every auxiliary task “epistemic”. We instead define a responsibility through an explicit decision contract.

## Definition 1 — epistemic responsibility contract

A responsibility is

\[
r=(Q,\mathcal A,\ell),
\]

where \(Q\) is a declared epistemic target/state, \(\mathcal A\) is a finite set of admissible epistemic actions or terminals, and \(\ell(a,q)\) is the registered loss for choosing \(a\) in state \(q\).

A responsibility should be tied to the epistemic status or management of a claim/model/inquiry. Examples include:

- `ADMIT`, `REJECT`, or `UNRESOLVED` under an evidence contract;
- `REOPEN` versus `RETAIN` when support may have been defeated;
- `ABSTAIN` versus `ANSWER` under a registered identifiability criterion;
- `RETRIEVE_MORE_EVIDENCE` versus `COMPUTE` under a declared information-acquisition rule;
- reuse/revalidation decisions tied to a validity/scope state.

An arbitrary sentiment or topic label is not made epistemic by notation.

## 4.1 Bayes responsibility risk

For any information variable \(V\), define

\[
\mathcal R_r(V)
=
\mathbb E\left[
\min_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid V]
\right].
\]

If \(Z=f(H)\), then

\[
\mathcal R_r(Z)\ge \mathcal R_r(H),
\]

because a decision rule using \(H\) can emulate any rule using only \(Z\). Define responsibility regret

\[
\delta_r(Z)=\mathcal R_r(Z)-\mathcal R_r(H).
\]

We treat this as classical decision theory.

## 4.2 Exact decision signature

For exact finite-state results, define the full set of Bayes-optimal actions

\[
D_r(h)
=
\operatorname*{argmin}_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

If calibrated residual risk is itself part of the responsibility, use the stronger signature

\[
\widetilde D_r(h)=
\left(
D_r(h),
\min_a\mathbb E[\ell(a,Q)\mid h]
\right).
\]

For a family \(\mathcal R=\{r_1,\ldots,r_m\}\), let

\[
C_{\mathcal R}(h)=
(D_{r_1}(h),\ldots,D_{r_m}(h))
\]

or the registered stronger signatures.

A representation is exact decision-sufficient for \(\mathcal R\) if \(C_{\mathcal R}\) is recoverable from it.

---

# 5. Static predictive–responsibility state

## Proposition 1 — coarsest joint state

In the finite deterministic setting, the coarsest representation that is both linguistically predictive-sufficient and exact decision-sufficient for \(\mathcal R\) is the common refinement

\[
S_{P\mathcal R}
=(S_P,C_{\mathcal R})
\]

up to relabelling.

Any state satisfying both properties must refine the predictive partition and the responsibility-decision partition, hence their common refinement. The common refinement itself satisfies both.

The proposition is elementary and is not presented as a new sufficiency theorem.

## Theorem 1 — exact responsibility-decision overhead

Because \(S_P\) is a deterministic function of \(S_{P\mathcal R}\),

\[
H(S_{P\mathcal R})
=
H(S_P)+H(C_{\mathcal R}\mid S_P).
\]

Thus the minimum additional average deterministic state entropy beyond an entropy-minimal predictive state is

\[
\boxed{
C_{\mathrm{resp}}^0(\mathcal R\mid S_P)
=
H(C_{\mathcal R}\mid S_P).
}
\]

This is the static **responsibility-state price**.

If a registered responsibility literally requires exact recovery of target \(Q\), choose a decision signature that uniquely identifies \(Q\). Then

\[
C_{\mathrm{resp}}^0=H(Q\mid S_P).
\]

If \(Q\) contains distinctions that never change the registered epistemic action or required calibrated risk, storing all of \(Q\) overstates the true responsibility cost.

### Corollary 1 — marginal responsibility cost

If \(\mathcal R\) is already retained and responsibility \(r\) is added, the incremental exact average state cost is

\[
H(D_r\mid S_P,C_{\mathcal R})
\]

under the action-only signature. A new responsibility is representationally free iff its decision is already determined by the existing state.

---

# 6. Predictive compression and responsibility loss

The exact state-cost result becomes relevant to representation compression.

## Lemma 1 — predictive states refine \(S_P\)

If deterministic \(Z=f(H)\) is predictive-sufficient, then \(S_P\) is a function of \(Z\). Hence

\[
H(S_P\mid Z)=0.
\]

## Theorem 2 — entropy-minimal predictive state

For every deterministic predictive-sufficient \(Z\),

\[
H(Z)
=
H(S_P)+H(Z\mid S_P)
\ge H(S_P).
\]

Equality holds iff

\[
H(Z\mid S_P)=0,
\]

so \(Z\) and \(S_P\) determine one another almost surely.

This is a standard minimal-sufficiency consequence. The LLM-specific implication is the following.

## Corollary 2 — maximal predictive compression safety criterion

If the responsibility decision signature is not recoverable from \(S_P\), no deterministic entropy-minimal exact predictive representation can preserve it.

Equivalently, maximal compression to the complete-future predictive quotient is responsibility-safe iff

\[
H(C_{\mathcal R}\mid S_P)=0.
\]

This does **not** imply an ordinary transformer discards the responsibility. A non-minimal representation can preserve arbitrary additional information. It constrains designs or theoretical objectives that explicitly reward maximal prediction-preserving compression.

---

# 7. Static epistemic deficiency: acquisition versus compression

Let \(Q\) now denote a responsibility target predicted under logarithmic loss, and let \(Z\) be any representation generated from \(H\).

The Bayes-optimal log loss from \(Z\) is \(H(Q\mid Z)\). By the Markov structure induced by representation generation,

\[
H(Q\mid Z)
=
H(Q\mid H)
+
I(Q;H\mid Z).
\]

We define two typed deficits.

## Definition 2 — acquisition deficit

\[
A_Q=H(Q\mid H).
\]

This is uncertainty that remains even with the full accessible history. If \(A_Q>0\), improving the internal compression of the same history cannot make exact \(Q\) recovery possible.

## Definition 3 — compression deficit

\[
C_Q(Z)=I(Q;H\mid Z).
\]

This is responsibility information available in the accessible history but missing from the representation.

Then

\[
H(Q\mid Z)=A_Q+C_Q(Z).
\]

The identity is classical. The distinction matters because its interventions differ: acquisition deficit calls for new evidence; compression deficit calls for better state retention or a different representation objective.

## 7.1 New observations and redundant reacquisition

If a new observation \(X\) becomes available, its information value given the full history is

\[
I(Q;X\mid H).
\]

Its apparent value given compressed state \(Z\) is

\[
I(Q;X\mid Z).
\]

The latter can be larger because the tool/retrieval step may redundantly re-supply information that was already present in \(H\) but discarded from \(Z\). This distinction separates **genuine acquisition** from costly **reacquisition caused by state loss**.

---

# 8. Why static sufficiency is not enough

We now reach the main sequential result.

Suppose a state preserves:

1. the entire linguistic predictive state \(S_P\); and
2. all epistemic decisions required at the present time.

It can still be wrong as an internal state for an autoregressive system that must update those decisions after future observations.

The issue is not current accuracy. It is **recursive implementability**.

## 8.1 Finite history-transition system

Let \(\mathcal H\) be a finite set of admissible histories with partial extension

\[
(h,x)\mapsto hx,
\]

where \(x\in\mathcal X\) is a future observation/token/event.

At the present time define the base label

\[
B(h)=(S_P(h),C_{\mathcal R}(h)).
\]

This is exactly the information required for current prediction and current registered responsibilities.

A recursively updateable state \(R(h)\) must satisfy:

- \(B(h)\) is recoverable from \(R(h)\);
- there exists a deterministic update rule \(\delta\) such that

\[
R(hx)=\delta(R(h),x)
\]

for every admissible extension.

## 8.2 Horizon refinement

Define

\[
h\equiv_0h'
\iff B(h)=B(h').
\]

Recursively,

\[
h\equiv_{k+1}h'
\]

iff they have equal current base labels and every matching symbol extension is either jointly inadmissible or leads to histories equivalent under \(\equiv_k\).

Let

\[
S_k=[H]_{\equiv_k}.
\]

The partitions become successively finer and stabilize for finite \(\mathcal H\). Denote the stable state \(S_\infty\).

## Theorem 3 — horizon monotonicity

\[
S_0\preceq S_1\preceq\cdots\preceq S_\infty,
\]

so

\[
H(S_{k+1})\ge H(S_k).
\]

Define the horizon-\(k\) optionality cost

\[
C_{\mathrm{opt}}(k)
=H(S_k\mid S_0).
\]

This is state that has no additional role in the current base decision beyond preserving correct behavior across the next \(k\) extensions.

## Theorem 4 — minimal recursively updateable state

At stabilization, \(\equiv_\infty\) is the coarsest right congruence refining the current base-label partition. Therefore any deterministic state that recovers \(B\) and updates recursively must refine \(S_\infty\), while \(S_\infty\) itself admits a well-defined deterministic update.

Consequently

\[
\boxed{
C_{\mathrm{dyn}}
=H(S_\infty\mid S_0)
}
\]

is the minimum additional average state entropy required for exact recursive responsibility preservation beyond current static sufficiency.

The coarsest-right-congruence result is classical automata/state-minimization mathematics. The proposed conceptual contribution is to recognize \(C_{\mathrm{dyn}}\) as an **epistemic option value of internal memory** relative to future responsibilities.

---

# 9. Zero static cost, positive dynamic cost

A two-history construction makes the distinction unavoidable.

Let current histories \(h_0,h_1\) be equally likely and encode a provenance bit \(A\in\{0,1\}\). Assume:

- both histories have the same complete linguistic future law;
- both require the same current epistemic action.

Thus

\[
S_0(h_0)=S_0(h_1)
\]

and current responsibility overhead is zero.

Now let a future observation \(x\) arrive, after which the correct responsibility action depends on the old provenance bit:

\[
C_{\mathcal R}(h_ax)=a.
\]

The horizon-1 refinement must split \(h_0\) from \(h_1\). Under the equal prior,

\[
H(S_0)=0,
\qquad
H(S_1)=1\text{ bit},
\]

and

\[
C_{\mathrm{opt}}(1)=1\text{ bit}.
\]

The bit has zero current predictive value and zero current responsibility value. Its only role is to preserve the ability to revise later.

This is the formal analogue of retaining source or assumption lineage that becomes load-bearing only after a future retraction, contradiction or scope change.

---

# 10. Prospective epistemic deficiency

The exact-state partition view has an information-theoretic analogue.

Let \(H_t\) be the full history at time \(t\), \(Z_t=f(H_t)\) the retained state, \(X_{t+1:t+k}\) the future observations, and \(Q_{t+k}\) a future responsibility target.

Define

\[
\boxed{
\Delta_k(Z_t;Q)
=
I(Q_{t+k};H_t\mid Z_t,X_{t+1:t+k}).
}
\]

Under logarithmic loss,

\[
\Delta_k
=
H(Q_{t+k}\mid Z_t,X_{t+1:t+k})
-
H(Q_{t+k}\mid H_t,X_{t+1:t+k}).
\]

Thus \(\Delta_k\) measures information discarded **now** that becomes relevant after future evidence and is not reconstructed by that evidence.

A model can satisfy

\[
I(Q_t;H_t\mid Z_t)=0
\]

while having

\[
\Delta_k(Z_t;Q)>0.
\]

Static probing therefore cannot certify prospective revision adequacy.

## 10.1 Three-axis diagnostic

For a responsibility we can report

\[
\mathfrak D_Q(Z_t;k)
=
(A_Q,C_Q(Z_t),\Delta_k(Z_t;Q)).
\]

The coordinates should not be scalarized by default because their interventions differ.

| deficit | interpretation | remedy class |
|---|---|---|
| \(A_Q>0\) | responsibility information absent even from full accessible history | acquire evidence/source/measurement |
| \(C_Q>0\) | current history contains information that representation discarded | refine/preserve state |
| \(\Delta_k>0\) | current state may be adequate now but has lost future revision optionality | preserve dormant lineage/alternative state over horizon |

---

# 11. Approximate responsibility state

The exact theory is deliberately finite. We nevertheless need an approximate benchmark.

For deterministic exact-recovery responsibility \(Q=q(H)\), retain \(S_P\) exactly and add stochastic augmentation \(U\). Under log loss define

\[
R_{\mathrm{epi}}(D)
=
\inf I(H;U\mid S_P)
\quad\text{s.t.}\quad
H(Q\mid S_P,U)\le D.
\]

Classical log-loss rate-distortion machinery yields

\[
R_{\mathrm{epi}}(D)
=
[H(Q\mid S_P)-D]_+.
\]

We include this as a benchmark, not a new theorem. Independent conditionally independent responsibilities produce the additive product frontier. Correlated responsibilities can share state, and at zero error the exact shared-state saving is the conditional total correlation

\[
\sum_i H(Q_i\mid S_P)-H(Q_1,\ldots,Q_m\mid S_P).
\]

A top-tier claim cannot rest on these classical identities alone. Their role is to expose the state-rate dimension of responsibility preservation and support future approximate dynamic theory.

---

# 12. Implications for language-model representation research

The theory does not prescribe a transformer modification, but it changes several evaluation questions.

## 12.1 Predictive loss is not a certificate for another responsibility

Two representations can implement the same language predictor while differing in responsibility information. Equal language loss therefore does not certify equal epistemic capability.

This statement should not be confused with saying that next-token training necessarily removes responsibility information. It says the objective does not, by itself, certify the property.

## 12.2 Compression and distillation need secondary responsibility audits

A compression method can preserve language loss while reducing responsibility state. The correct test is not only whether a compressed model predicts text equally well, but whether it preserves the declared responsibility quotient and, for long-lived systems, prospective revision sufficiency.

## 12.3 Static truth probes are incomplete

A hidden-state probe can show that current factuality or confidence information is decodable. It does not by itself show:

- that the state supports the correct epistemic decision;
- that the signal is causally used;
- that source/dependence/scope information is retained;
- that the state can revise correctly after future evidence.

The last condition requires a sequential intervention: retain the current state, supply controlled future evidence, and test whether the correct dependent commitments change.

## 12.4 Retrieval can hide state insufficiency

A system may compensate for lost internal information by retrieving it again later. This can be operationally effective while still indicating a representation inefficiency. The acquisition/compression decomposition distinguishes genuinely new evidence from redundant reacquisition.

## 12.5 “Store everything” is not the conclusion

Raw-history retention trivially avoids many compression failures but defeats state abstraction and can be computationally impossible. The responsibility-decision quotient prevents over-retention: preserve only distinctions that change declared epistemic responsibilities, plus the extra distinctions needed for their registered future revision horizon.

---

# 13. A future empirical protocol, without making it part of this paper's evidence

The theory suggests an eventual low-cost experiment on existing open-weight models; the current paper does not require it.

A future study could construct paired histories that are matched on linguistic prediction but differ in a mechanically defined epistemic responsibility, then ask:

1. Is the responsibility decodable from hidden state?
2. Does intervening on the candidate state change the responsibility decision?
3. After a controlled future observation, can the model selectively revise the correct history-dependent conclusion?
4. Does compression/distillation preserve language loss while damaging current or prospective responsibility sufficiency?

The key comparison is not “LLM versus ORION”. It is **same linguistic predictive performance, different responsibility requirement**.

---

# 14. Limitations

The exact theorems use finite histories, finite responsibility/action sets, and deterministic base representations unless otherwise stated. Continuous high-dimensional transformer states require measure-theoretic and approximation extensions.

The minimal predictive state is an idealized information object. Real neural models are not known to implement it, and training dynamics need not minimize representation entropy. Therefore the maximal-compression theorem is a limit/design result, not a claim about normal pretrained transformer internals.

The responsibility contracts are externally declared. The framework does not derive a universal list of epistemic responsibilities, nor does it solve philosophical questions about belief, understanding or consciousness.

Right-congruence/state-minimization theory is classical. If the nearest-work audit finds that the prospective responsibility-state result already exists in equivalent learned-representation form, the standalone theory claim should contract.

The approximate log-loss frontier is classical conditional rate-distortion structure and is not claimed as independent novelty.

Finally, internal epistemic sufficiency does not create scientific authority. A model may internally preserve exactly the information needed to recommend a scientific action while still lacking legitimate authority to execute, publish or institutionalize it.

---

# 15. Verification and falsification programme

Before submission, the paper requires a mechanical package that:

- formalizes or independently checks the static theorems;
- enumerates all small partitions to attack hidden assumptions;
- verifies exact state-cardinality and entropy identities;
- confirms the zero-static/positive-dynamic witness;
- independently enumerates right-congruent refinements for small machines;
- checks prospective deficiency identities from finite joint tables;
- builds a theorem-level related-work matrix covering causal states, R-PSR, DIB, multi-task sufficiency, conditional log-loss rate distortion, POMDP information states and Myhill–Nerode/right-congruence theory.

The computational package is designed to **falsify or contract** theorem statements, not to generate favorable synthetic outcomes.

---

# 16. Conclusion

A predictive model is not specified by prediction accuracy alone when the system is expected to manage knowledge over time.

The strongest version of the paper's thesis is not that language models fail to know, nor that Machine Epistemics should replace neural learning. It is narrower:

> **An internal state sufficient for the linguistic future need not be sufficient for an epistemic responsibility; a state sufficient for both current prediction and current responsibility need not be sufficient for future epistemic revision.**

The first gap is static and decision-relative. The second is sequential and concerns optionality. In finite exact settings both can be represented as state-refinement costs. This perspective gives language-model researchers a more precise question than whether a hidden state “contains truth”: **which distinctions must the state preserve for the decisions it is responsible for now, and which dormant distinctions must survive so those decisions can be revised correctly when the world supplies new evidence?**

Whether that formulation constitutes a new theory contribution beyond its strong statistical, predictive-state and automata parents is itself treated as a falsifiable research question. The paper should survive only if the registered formal and nearest-work audits leave a substantive residual.

---

# Provisional references / theorem owners

The final bibliography must be generated and verified by the registered theorem-level literature matrix. At minimum it will include:

- Blackwell, D. — comparison/equivalence of statistical experiments.
- Shalizi, C. R. & Crutchfield, J. P. — computational mechanics / causal-state minimal predictive sufficiency and recursive calculability.
- Littman, Sutton, Singh and later PSR work — Predictive State Representations.
- Baisero, A. & Amato, C. — Reward-Predictive State Representations / reward insufficiency of ordinary PSRs.
- Tishby, Pereira & Bialek — Information Bottleneck.
- Strouse, D. & Schwab, D. — Deterministic Information Bottleneck.
- Courtade, T. & Weissman, T. — source coding under logarithmic loss.
- standard Myhill–Nerode / deterministic automaton minimization / right-congruence theory.
- POMDP belief-state / sufficient information-state literature.
- Sevetlidis, V. (2026) — representation identifiability fibre criterion.
- Herrmann & Levinstein — standards for belief representations in LLMs.
- Corona Mendozza & Søgaard (2026) — causally usable belief-like LLM internal representations.
- Cheang et al. (2026) — distinction between internal knowledge recall and truthfulness signals.
- Hu et al. (2025) — information-theoretic multi-task sufficient representation.
