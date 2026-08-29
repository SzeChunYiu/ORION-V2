# Beyond Predictive Sufficiency: Static and Prospective Epistemic State Requirements for Autoregressive Models

**Pre-mechanization manuscript draft V2**  
**Issue:** #51  
**Supersedes:** `MANUSCRIPT_DRAFT_V1.md` for scientific argument and theorem wording.  
**Status:** theory manuscript; all load-bearing statements remain candidate until the registered formal and nearest-work checks complete.  
**Empirical LLM performance claims:** none.  
**Primary venue aspiration if the residual survives:** Journal of Machine Learning Research.

---

## Abstract

Autoregressive models are optimized for linguistic prediction but are increasingly used in systems that must also make and revise epistemically consequential decisions: answer or abstain, retain or reopen a conclusion, request evidence, distinguish independent from dependent support, or preserve scope conditions. These responsibilities impose information requirements on internal state that need not coincide with the requirements of language prediction. We develop a finite-state framework for quantifying this difference while explicitly separating our contribution from classical sufficient-statistic, predictive-state, information-state, rate-distortion and automata theory. Let \(S_P\) be the minimal state sufficient for the complete linguistic future. We model an epistemic responsibility as a decision contract specifying a target, admissible actions, loss, and exact decision semantics. For the common case in which any Bayes-optimal action is acceptable, the minimum exact additional deterministic state entropy beyond \(S_P\) is the minimum, over Bayes-optimal selectors \(d\), of \(H(d(H)\mid S_P)\); exact recovery of a target \(Q\) is the special case \(H(Q\mid S_P)\). This decision-relative formulation avoids preserving distinctions that never change the system's registered epistemic action. We then show why static sufficiency is not enough for a continually used autoregressive state. Even a representation that preserves the complete linguistic predictive state and a registered current optimal policy can discard information needed to update that policy after later evidence. For a fixed responsibility policy, the minimal exact recursively updateable state is the coarsest right-congruent refinement of the current predictive-policy state, and the conditional entropy of that refinement defines a dynamic epistemic optionality cost. A canonical construction has zero current responsibility overhead yet requires one additional bit solely for correct future revision. We further separate acquisition deficit, current compression deficit, and prospective revision deficit, and show that unrestricted exact future responsibility families eliminate nontrivial compression by eventually separating every history within a predictive fibre. The mathematical substrate is intentionally parent-aware: basic predictive-state separation is already represented in reward-predictive state work, recurrent sufficient-state theory is strongly occupied by information-state/POMDP theory, and log-loss frontiers are classical. The proposed residual is a responsibility-relative, horizon-relative internal-state formulation and evaluation target for autoregressive representations. We do not claim that present LLMs are minimal predictive states, lack belief-like structure, or require a particular neural architecture.

---

# 1. Introduction

A language model can give the right answer now and still be in the wrong state for the next piece of evidence.

Suppose two histories lead to exactly the same distribution over the model's complete linguistic future and the same epistemic action today. In one history, however, the current conclusion ultimately depends on source \(A\); in the other it depends on source \(B\). If that provenance distinction has no effect on present language prediction or present action, a compressed state may legitimately merge the histories. Now suppose a later observation reports that source \(A\) has been retracted. Correct revision requires reopening one conclusion while leaving the other unchanged. If the earlier compression discarded which source supported which conclusion, the future observation does not necessarily reconstruct the missing relation.

This example exposes three distinct failure mechanisms.

1. **Acquisition failure.** The accessible history never contained enough information to resolve the responsibility.
2. **Current representation failure.** The information was accessible but the internal state discarded it even though it was needed now.
3. **Prospective representation failure.** The state was sufficient for today's prediction and today's action but discarded a currently dormant distinction needed for a future revision.

These are not interchangeable forms of “uncertainty”. They imply different interventions: obtain new evidence, preserve more current state, or retain future-option information over a declared revision horizon.

This distinction is especially important for language models because their primary training/evaluation objective is linguistic prediction while deployed systems are commonly asked to support additional decisions about evidence, abstention, provenance, revision and scope. Hidden-state research already shows that language models can encode factual, confidence, recall and belief-like variables, sometimes in causally usable form. Our theory therefore does **not** begin from the claim that LLMs have no internal epistemic structure. Instead it asks a representation question:

> **Given a state sufficient for the complete linguistic future, what additional information is required for a declared family of epistemic decisions now and under a declared future responsibility horizon?**

The answer must be responsibility-relative. An arbitrary auxiliary label can contain much more information than the system actually needs to act correctly. If two posterior states imply the same permitted epistemic action, requiring the model to preserve their exact target values overstates the necessary state. Conversely, preserving the current action may still be insufficient for future revision.

## 1.1 Relation to existing theory

The constituent mathematics has strong owners.

- Statistical sufficiency and Blackwell-style decision theory own the principle that an information-losing statistic can increase Bayes risk.
- Computational mechanics and Predictive State Representations own minimal state relative to a future prediction process.
- Reward-Predictive State Representations already demonstrate that an observation-predictive state can be insufficient for a secondary reward target.
- Information Bottleneck, Deterministic Information Bottleneck and multi-task representation learning study compressed task-sufficient states.
- Minimal-sufficient representation work has already shown that compression for one learning target can discard information relevant to downstream tasks.
- POMDP belief states and Approximate Information State theory already formalize recurrent history compression sufficient for future control/prediction.
- Myhill–Nerode/right-congruence and automata minimization own generic deterministic recursive-state minimization.
- Logarithmic-loss rate-distortion theory owns the basic entropy-minus-distortion frontier.

Accordingly, our paper cannot succeed by renaming these results “epistemic”. The proposed residual lies in the **relative state accounting** induced by explicit epistemic decision contracts and in the distinction between current decision sufficiency and future revision sufficiency when the linguistic predictive quotient is treated as the base state.

## 1.2 Contributions under test

The registered contribution package is:

1. **Decision-relative epistemic state.** We formalize an epistemic responsibility as a target, action set, loss, and exact decision semantics. Under `ANY_OPTIMAL_ACTION`, the exact state requirement is governed by the cheapest Bayes-optimal action selector rather than the full target or full optimal-action set.
2. **Static state price beyond language prediction.** With \(S_P\) retained, the minimum exact additional deterministic state cost for one responsibility is
   
   \[
   \min_{d(h)\in A^*(h)} H(d(H)\mid S_P),
   \]
   
   with corresponding fixed-signature formulas for canonical actions, full option sets, calibrated action+risk, and exact targets.
3. **Prospective revision gap.** A representation can preserve the complete linguistic future and all registered current decisions while still losing information required to update those decisions after future evidence.
4. **Dynamic optionality cost.** For a fixed registered responsibility policy, the coarsest exact recursively updateable state is the coarsest right-congruent refinement of the current predictive-policy state. We measure the extra state needed solely for future update correctness by \(H(S_\infty\mid S_0)\).
5. **Typed deficits.** We distinguish information absent from accessible history, information lost by current compression, and information lost only with respect to future revision.
6. **Bounded-responsibility limit.** As a declared responsibility family becomes rich enough to separate every pair of histories within predictive fibres, its state requirement approaches full retention of the non-predictive history. There is therefore no meaningful nontrivial exact compression that is “sufficient for every possible future epistemic responsibility.”
7. **Falsifiable publication boundary.** We preregister parent ownership and formal counterexample checks. If Approximate Information State/POMDP/PSR/decision-theory parents reproduce the full static-plus-dynamic result with no non-obvious residual, the standalone paper contracts.

---

# 2. Predictive state

Let \(H\) be a finite positive-support random variable representing all history/information accessible to the model at a declared time. Let \(Y^+\) be the complete future linguistic sequence under the declared process.

A deterministic internal representation is

\[
Z=f(H).
\]

## Definition 1 — predictive sufficiency

\(Z\) is linguistically predictive-sufficient if

\[
Y^+\perp H\mid Z.
\]

Define

\[
h\sim_P h'
\iff
P(Y^+\mid H=h)=P(Y^+\mid H=h').
\]

and write

\[
S_P=[H]_{\sim_P}.
\]

This is the standard finite predictive quotient. Any deterministic predictive-sufficient \(Z\) refines \(S_P\). We make no novelty claim for this fact.

An important implication is purely negative: linguistic prediction only constrains distinctions that affect the linguistic future. Distinctions inside one \(S_P\) fibre are free to be preserved or discarded unless another requirement makes them load-bearing.

---

# 3. Epistemic responsibility contracts

Calling every secondary task “epistemic” would make the theory vacuous. We therefore require an operational decision contract.

## Definition 2 — responsibility

A responsibility is

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where:

- \(Q\) is an externally/mechanically specified state relevant to the epistemic management of a claim, model or inquiry;
- \(\mathcal A\) is the admissible action/terminal set;
- \(\ell(a,q)\) is a registered loss;
- \(\sigma\) specifies what exact decision information must be preserved.

Examples include:

- `ANSWER` versus `ABSTAIN` under an identifiability rule;
- `RETAIN` versus `REOPEN` after a support change;
- `ADMIT`, `REJECT`, `UNRESOLVED` under a fixed evidence contract;
- `RETRIEVE`, `COMPUTE`, `DEFER` under a declared information-acquisition problem.

Institutional permission to execute an action is not generated by this internal state and remains outside the responsibility contract.

## 3.1 Bayes-optimal decisions

For history \(h\), define

\[
A_r^*(h)=
\operatorname*{argmin}_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h]
\]

and Bayes risk

\[
\rho_r(h)=
\min_a\mathbb E[\ell(a,Q)\mid H=h].
\]

We distinguish five exact semantics.

### ANY_OPTIMAL_ACTION
The representation need only support **some** action in \(A_r^*(h)\).

### CANONICAL_ACTION
The contract supplies a deterministic tie selector \(	au\) and requires \(d_r^\tau(h)=\tau(A_r^*(h))\).

### OPTIMAL_ACTION_SET
The complete set \(A_r^*(h)\) must be recoverable. This is appropriate only when preserving all epistemically acceptable options is itself part of the responsibility.

### ACTION_AND_RISK
A registered action plus the Bayes risk value must be recoverable, for example when calibrated unresolved risk is load-bearing.

### EXACT_TARGET
The target \(Q\) itself must be recovered exactly.

This distinction matters. If

\[
A^*(h_1)=\{a,b\},\qquad
A^*(h_2)=\{b,c\},
\]

the histories may be merged under `ANY_OPTIMAL_ACTION` because action \(b\) is correct for both. Requiring the full optimal-action set would unnecessarily force them apart.

---

# 4. Exact static state cost

We now quantify the additional deterministic state beyond \(S_P\).

## 4.1 ANY_OPTIMAL_ACTION

Let

\[
\mathcal D_r=
\{d:\mathrm{supp}(H)\to\mathcal A:
 d(h)\in A_r^*(h)\ \forall h\}.
\]

A representation is exact action-sufficient if some decoder outputs a Bayes-optimal action at every history.

## Theorem 1 — minimum exact action-state entropy

Subject to retaining \(S_P\), the minimum exact additional average state entropy is

\[
\boxed{
C_{r,\mathrm{any}}^0
=
\min_{d\in\mathcal D_r} H(d(H)\mid S_P).
}
\]

### Proof sketch

If \(Z\) is action-sufficient, choose its decoder \(g\) and define \(d(h)=g(Z(h))\). Then \(d\in\mathcal D_r\), \(d(H)\) is a deterministic function of \(Z\), and

\[
H(d(H)\mid S_P)\le H(Z\mid S_P).
\]

Conversely, store \(S_P\) together with an entropy-minimizing valid selector \(d^*(H)\). The stored action is Bayes-optimal at every history. The bound is attained. ∎

The theorem says that the state price of the responsibility is the cheapest Bayes-optimal **policy information** that must survive beyond language prediction.

## 4.2 Fixed semantics

For `CANONICAL_ACTION`, the exact extra cost is

\[
H(d_r^\tau(H)\mid S_P).
\]

For `OPTIMAL_ACTION_SET`, it is

\[
H(A_r^*(H)\mid S_P).
\]

For `ACTION_AND_RISK`, it is the conditional entropy of the registered action/risk signature.

For deterministic `EXACT_TARGET` with zero-one loss, the unique Bayes action is \(Q\), giving

\[
H(Q\mid S_P).
\]

Thus the familiar exact-target formula is a special case rather than the definition of epistemic state.

## 4.3 Responsibility families

If the signatures are fixed by the contracts, joint cost is the conditional entropy of the joint signature. If several responsibilities use `ANY_OPTIMAL_ACTION`, selectors should be optimized jointly:

\[
\boxed{
C_{\mathcal R,\mathrm{any}}^0
=
\min_{d_i\in\mathcal D_{r_i}}
H(d_1(H),\ldots,d_m(H)\mid S_P).
}
\]

The joint minimization allows correlated responsibilities to share state.

This formulation is intentionally closer to statistical decision theory than to a bespoke ORION ontology. The nearest-work audit must decide whether the package has any independent theorem residual.

---

# 5. Compression consequence

Classical minimal-sufficiency theory provides the following bridge.

If deterministic \(Z\) is exactly predictive-sufficient, \(S_P\) is a deterministic function of \(Z\). Therefore

\[
H(Z)=H(S_P)+H(Z\mid S_P)\ge H(S_P).
\]

Equality makes \(Z\) and \(S_P\) mutually recoverable almost surely.

The LLM representation consequence is:

> **Maximal exact prediction-preserving compression is safe for a fixed epistemic responsibility only if a valid Bayes-optimal policy for that responsibility can already be implemented from \(S_P\).**

Under `ANY_OPTIMAL_ACTION`, zero extra cost occurs exactly when every predictive fibre admits at least one common Bayes-optimal action.

This is a design limit, not a claim that ordinary transformer pretraining actually compresses hidden state to \(S_P\).

---

# 6. Acquisition versus compression

Let \(Q\) be a target evaluated under log loss and \(Z\) a representation generated from \(H\). The minimum Bayes log loss from \(Z\) is \(H(Q\mid Z)\), and

\[
H(Q\mid Z)
=
H(Q\mid H)+I(Q;H\mid Z).
\]

We use this classical identity to define two operationally distinct deficits.

## Acquisition deficit

\[
A_Q=H(Q\mid H).
\]

This uncertainty remains even with the complete accessible history. Better compression cannot remove it; some new observation, source, measurement or assumption is needed.

## Compression deficit

\[
C_Q(Z)=I(Q;H\mid Z).
\]

This is information available in history but absent from the representation.

If a new observation \(X\) arrives, its genuine acquisition value given the full history is \(I(Q;X\mid H)\). Its value given a compressed state can be larger because it may redundantly re-supply information that was present in \(H\) but discarded from \(Z\). Thus tool/retrieval use can operationally mask internal state insufficiency.

Neither identity is claimed as new information theory. Their purpose is to prevent different failure mechanisms from being collapsed into one confidence score.

---

# 7. Static decision sufficiency does not imply future revision sufficiency

The preceding sections concern the present time. A continually used autoregressive system must update its state after later observations.

Fix a registered Bayes-optimal policy selector for each current/future responsibility. We deliberately use a **fixed-policy route** for the exact dynamic theorem; jointly optimizing policy selection and recursive state is a stronger problem that this paper does not claim to solve.

Let \(\mathcal H\) be a finite set of histories with partial extension

\[
(h,x)\mapsto hx,
\]

where \(x\) is a future observation/event. Let the current base label be

\[
B(h)=(S_P(h),D(h)),
\]

where \(D(h)\) collects the registered fixed responsibility decisions/required risk signatures.

A recursively updateable state \(R(h)\) must recover \(B(h)\) and admit a deterministic update

\[
R(hx)=\delta(R(h),x).
\]

## 7.1 Horizon partitions

Define

\[
h\equiv_0h'
\iff B(h)=B(h').
\]

Recursively, \(h\equiv_{k+1}h'\) iff they have the same base label and every admissible one-step extension leads to histories equivalent under \(\equiv_k\), with undefined extensions matched explicitly.

Let \(S_k=[H]_{\equiv_k}\). Then

\[
S_0\preceq S_1\preceq\cdots
\]

and the sequence stabilizes on finite \(\mathcal H\).

## Theorem 2 — fixed-policy recursive state

At stabilization, \(S_\infty\) is the coarsest right-congruent refinement of the current predictive-policy partition. Every deterministic recursively updateable exact state implementing the registered policy must refine \(S_\infty\), and \(S_\infty\) itself admits a well-defined update.

This is classical right-congruence/state-minimization structure. We use it to define a relative quantity:

\[
\boxed{
C_{\mathrm{dyn}}=H(S_\infty\mid S_0).
}
\]

\(C_{\mathrm{dyn}}\) measures state that is unnecessary for the registered current prediction/action but necessary to preserve correct future policy updates.

## 7.2 Canonical one-bit witness

Let two equally likely histories \(h_0,h_1\) have the same linguistic predictive state and the same current epistemic action. They differ only in a provenance bit \(A\in\{0,1\}\), which is currently irrelevant.

A later observation \(x\) activates a responsibility for which the correct action after \(h_ax\) is \(a\). Then

\[
S_0(h_0)=S_0(h_1),
\]

but

\[
S_1(h_0)\ne S_1(h_1).
\]

Under the equal prior,

\[
H(S_0)=0,
\qquad
H(S_1)=1\text{ bit}.
\]

The provenance bit has zero current language value and zero current policy value, but one bit of future epistemic option value.

This is the central conceptual distinction of the paper.

---

# 8. Prospective deficiency

The partition result has an average information-theoretic analogue.

Let \(H_t\) be current history, \(Z_t\) retained state, \(X_{t+1:t+k}\) future observations, and \(Q_{t+k}\) a future responsibility target. Define

\[
\boxed{
\Delta_k(Z_t;Q)
=
I(Q_{t+k};H_t\mid Z_t,X_{t+1:t+k}).
}
\]

Under log loss this equals the excess future Bayes loss caused by retaining \(Z_t\) rather than the full prior history after both receive the same future observations.

A state may have zero current compression deficit and positive \(\Delta_k\). Static hidden-state probing therefore does not certify future revision adequacy.

The diagnostic triple

\[
(A_Q,C_Q,\Delta_k)
\]

separates:

- information missing at ingress;
- information lost for the current responsibility;
- information lost only for future revision.

These coordinates should not be combined by default because their remedies differ.

---

# 9. Why responsibility families must be bounded

A compressed state cannot be exactly sufficient for every possible future responsibility unless it effectively retains all relevant history.

Let \(C_\mathcal R(H)\) denote the joint fixed responsibility signature for family \(\mathcal R\). Because it is a function of \(H\),

\[
0\le H(C_\mathcal R\mid S_P)\le H(H\mid S_P).
\]

If \(\mathcal R\) separates every pair of histories inside each predictive fibre, then

\[
H(H\mid S_P,C_\mathcal R)=0
\]

and the upper bound is attained:

\[
H(C_\mathcal R\mid S_P)=H(H\mid S_P).
\]

More directly, any non-injective representation \(Z\) collides two positive-mass histories. One can construct an exact binary responsibility that assigns different required actions to the two histories, making zero-error recovery impossible from \(Z\).

Thus:

> **“Epistemically sufficient state” is meaningful only relative to a declared responsibility family and future horizon. Unrestricted exact future responsibility support eliminates nontrivial compression.**

This result is likely a classical sufficiency/no-free-lunch corollary; we use it as a hard boundary on the framework rather than as the sole novelty claim.

---

# 10. Approximate benchmark

For deterministic exact-target \(Q=q(H)\), retain \(S_P\) exactly and allow stochastic augmentation \(U\). Under log loss,

\[
R_{\mathrm{epi}}(D)
=
\inf I(H;U\mid S_P)
\quad\text{s.t.}\quad
H(Q\mid S_P,U)\le D.
\]

The classical log-loss frontier is

\[
R_{\mathrm{epi}}(D)
=
[H(Q\mid S_P)-D]_+.
\]

It is achieved by an erasure/reveal construction and is included only as a benchmark. Conditionallly independent responsibilities give the corresponding additive product frontier; correlated responsibilities can share state.

A JMLR claim cannot rest on this section alone.

---

# 11. Implications for LLM representation research

## 11.1 Prediction loss does not certify responsibility state

Equal language predictive behavior does not identify equal internal responsibility information. This follows both from task-relative sufficiency and general representation non-identifiability. Therefore a prediction-only evaluation cannot certify current or prospective epistemic adequacy.

## 11.2 Compression/distillation should be tested prospectively

A compressed model can preserve linguistic loss and even preserve a static epistemic probe while losing information required for revision after controlled future evidence. A stronger evaluation should therefore report:

1. linguistic predictive quality;
2. current registered responsibility regret/state sufficiency;
3. prospective responsibility performance after matched future evidence;
4. representation/state cost.

## 11.3 Static truth probes are only one layer

Current hidden-state work asks whether truth, factuality, confidence or belief-like variables are recoverable/causally usable. Our framework adds a different test: after a future observation, does the retained state support the **correct history-dependent revision**? A representation can pass a current probe and fail this sequential test.

## 11.4 Retrieval can compensate for bad memory

If a system repeatedly re-retrieves source identity or support lineage that was available earlier but discarded, tool performance can hide a compression deficit. The acquisition/compression decomposition distinguishes new evidence from redundant reacquisition.

## 11.5 The theory does not imply “store everything”

State is relative to a responsibility contract. Under `ANY_OPTIMAL_ACTION`, it need retain only enough policy information to choose an acceptable Bayes action; distinctions between targets or optimal-action sets that never affect the registered action can be compressed away. Future optionality is likewise bounded by a declared responsibility schedule/horizon. Only an unrestricted responsibility family forces full-history retention.

---

# 12. Strongest parent threats and contraction rule

The paper's validity is separate from its novelty.

The following are already conceded as parent-owned or near-parent-owned:

- minimal predictive state;
- observation-predictive versus secondary-target insufficiency;
- deterministic task-sufficient compression;
- multi-task representation sufficiency;
- log-loss rate distortion;
- recurrent sufficient information state for partially observed control;
- right-congruence/automata state minimization;
- Bayes-risk monotonicity;
- conditional mutual-information identities.

The most important direct dynamic threat identified so far is Subramanian et al.'s **Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems** (JMLR, 2022), which already develops recursively updateable sufficient information states and approximation bounds. R-PSR work is the corresponding direct threat to the static “prediction misses a secondary target” story.

The standalone paper survives only if theorem-level review finds a non-obvious residual in the **relative responsibility policy cost + prospective revision optionality + bounded responsibility horizon** package that is useful for learning-system representation design/evaluation.

If a strongest parent product produces the same result immediately, the valid terminal is `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP` rather than a novelty rescue.

---

# 13. Formal verification programme

The theory is intentionally finite so that the remaining work can be mechanical.

The registered executor will:

- formalize or independently check all theorem IDs;
- enumerate all set partitions for histories up to the registered finite size;
- test minimality/refinement/cardinality claims;
- search counterexamples under one-at-a-time assumption removal;
- verify the tie-semantics fixture where two different optimal-action sets share a common action;
- verify the one-bit prospective witness;
- independently enumerate right-congruent partitions in small systems;
- verify responsibility-family saturation and non-injective-state binary counterexamples;
- locate exact theorem ownership in the preregistered parent literature.

No computation is authorized to change the scientific question after results are seen. Counterexamples narrow or kill claims.

---

# 14. Limitations

The exact theory is finite/discrete. Real transformer hidden states are continuous, high-dimensional, redundant and generally not entropy-minimal statistics. The paper therefore gives information/state requirements, not a theorem that current LLMs implement or violate them.

`ANY_OPTIMAL_ACTION` dynamic theory currently uses a **fixed registered Bayes-optimal selector** before right-congruence minimization. Jointly optimizing tie selection and recurrent state is a stronger problem and is explicitly not claimed solved.

Responsibility contracts are externally declared. The framework does not derive universal epistemic values, nor does it decide institutional legitimacy.

The approximate log-loss frontier and much of the recursive-state substrate are classical. If the final novelty audit leaves only terminology or application framing, JMLR submission is not authorized.

---

# 15. Conclusion

The central claim under test is narrower than “LLMs do not understand” and more precise than “prediction is not knowledge.”

A language model state can be considered adequate only relative to what the system is responsible for doing. The minimal state for linguistic prediction need not carry the policy information required by another responsibility. Yet storing the entire responsibility target can also be unnecessarily strong: the exact state price depends on the registered decision semantics. More importantly, state adequacy is temporal. A representation that is sufficient for the complete linguistic future and for every current epistemic action can still discard a currently dormant distinction needed to revise those actions correctly after future evidence.

This leads to three separate questions for an autoregressive internal state:

1. **Was the needed information available?**
2. **Was enough retained for the current responsibility?**
3. **Was enough retained for the declared future revision horizon?**

The theory quantifies these questions in finite exact settings and treats the resulting static and dynamic state costs as responsibility-relative. Whether this package constitutes a new machine-learning theory result rather than a careful synthesis of decision theory, predictive states and information-state recursion remains deliberately unresolved until the mechanical theorem and nearest-work audits close. That uncertainty is a publication gate, not a weakness to hide.
