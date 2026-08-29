# Beyond Predictive Sufficiency: Static and Prospective Epistemic State Requirements for Autoregressive Models

**Pre-mechanization manuscript draft V3**  
**Issue:** #51  
**Supersedes:** manuscript drafts V1–V2 for scientific argument.  
**Status:** candidate theory pending the registered formal and theorem-level parent audits.  
**Empirical LLM training evidence:** none required or claimed.  
**Primary venue aspiration if all gates pass:** Journal of Machine Learning Research.

---

## Abstract

Autoregressive models are optimized for linguistic prediction but are increasingly used in systems that must also make and revise epistemically consequential decisions: answer or abstain, retain or reopen a conclusion, request evidence, distinguish independent from dependent support, or preserve scope conditions. These responsibilities impose internal-state requirements that need not coincide with the requirements of language prediction. We develop a finite-state framework for measuring the difference while explicitly conceding its classical foundations in statistical decision theory, predictive-state representations, information-state control, rate-distortion theory and finite-state-machine minimization. Let \(S_P\) be the minimal state sufficient for the complete linguistic future. We model an epistemic responsibility as a decision contract specifying a target, admissible actions, loss and exact decision semantics. When any Bayes-optimal action is acceptable, the minimum exact additional deterministic state entropy beyond \(S_P\) is the minimum over Bayes-optimal action selectors \(d\) of \(H(d(H)\mid S_P)\); exact recovery of a target \(Q\) is the special case \(H(Q\mid S_P)\). We then study a continually updated state. A static partition is admissible when it refines \(S_P\) and every state block admits a common Bayes-optimal action. A dynamic partition additionally satisfies transition congruence. Minimizing conditional state entropy over these two feasible sets yields \(C_{\mathrm{stat}}^\*\) and \(C_{\mathrm{dyn}}^\*\); their difference

\[
\Omega_{\mathrm{dyn}}=C_{\mathrm{dyn}}^\*-C_{\mathrm{stat}}^\*\ge0
\]

is a **dynamic epistemic optionality premium**: state information unnecessary for an optimally compressed current responsibility policy but irreducibly required for some Bayes-optimal policy to remain recursively implementable after future observations. Equivalently, \(C_{\mathrm{dyn}}^\*\) is obtained by minimizing, over Bayes-optimal selectors, the entropy of the coarsest right-congruent refinement of the predictive-policy state. A canonical provenance construction has \(C_{\mathrm{stat}}^\*=0\) and \(C_{\mathrm{dyn}}^\*=1\) bit even after policy ties are optimized. We also distinguish acquisition deficit, current compression deficit and prospective revision deficit, and show that responsibility families rich enough to separate every history inside predictive fibres force retention of all non-predictive history. The underlying compatible-state/right-congruence optimization is closely related to classical minimization of incompletely specified finite-state machines, and generic recurrent sufficiency is strongly represented by POMDP/information-state theory. The proposed residual is therefore not state minimization itself, but a responsibility-relative, horizon-relative state-cost formulation and representation-evaluation target for autoregressive systems. We do not claim that current LLMs are minimal predictive states, lack belief-like internal structure, or require a particular neural architecture.

---

# 1. Introduction

A model can answer correctly today and still have forgotten what it must remember to revise correctly tomorrow.

Imagine two histories that induce the same distribution over the complete linguistic future and the same epistemic action at the present time. One current conclusion, however, depends on source \(A\), while the other depends on source \(B\). If the source distinction changes neither present language prediction nor present action, a compact internal state can merge the histories. Later the system receives a retraction of source \(A\). Correct revision now requires reopening one conclusion while preserving the other. If the earlier representation erased the source relation, the new observation may not reconstruct which conclusion depended on which source.

Three failures are possible:

1. the information was never available in the accessible history;
2. it was available and needed now but was compressed away;
3. it was not needed now but was compressed away even though a known future responsibility could make it relevant.

The first calls for new evidence. The second calls for a better current representation. The third calls for preserving **future epistemic option value**.

These distinctions are particularly relevant to language models. A linguistic prediction objective does not specify every downstream responsibility that a deployed system may later be asked to fulfill. Yet the simple statement that “prediction is insufficient for another task” is not new. Predictive State Representation work has long studied state relative to future observations; Reward-Predictive State Representations show directly that an observation-predictive state can fail a reward target. Information Bottleneck and multi-task representation theory formalize compressed state for task variables, and contrastive-representation work has explicitly analyzed how minimal sufficiency for one training target can discard downstream-relevant information. POMDP belief states and Approximate Information State theory already address recurrent sufficient history compression for future control. Right-congruence and incompletely specified finite-state-machine minimization provide classical machinery for compatible recurrent state reduction.

Our question is therefore narrower:

> **Starting from the complete-linguistic predictive state, what is the extra state price of a declared epistemic decision responsibility, and what further price is imposed when that responsibility must remain correctly updateable under future observations?**

The answer must be decision-relative. An auxiliary target may distinguish cases that never change the system's required epistemic action. Preserving the whole target can therefore overstate the state requirement. At the same time, optimizing only the current action can be too aggressive because tied or currently irrelevant histories may diverge after future evidence.

## 1.1 Candidate contribution package

Subject to the registered proof and parent audits, the paper contributes the following **formulation and consequences**, not new ownership of the classical substrates.

**Decision-semantic responsibility state.** A responsibility contract specifies an epistemic target, action set, loss and exact semantics: any optimal action, canonical action, full optimal-action set, action plus calibrated risk, or exact target. Under `ANY_OPTIMAL_ACTION`, static state cost is the cheapest Bayes-optimal action information beyond \(S_P\), not the entropy of every latent label.

**Joint current-policy/recurrent-state optimization.** We define static admissible partitions as predictive-refining blocks with a common Bayes-optimal action, and dynamic admissible partitions as those static partitions that are also right congruences for future observations. This avoids fixing an arbitrary tie-breaking policy before measuring memory cost.

**Dynamic epistemic optionality premium.** We define

\[
C_{\mathrm{stat}}^\*=\min_{\Pi\in\mathfrak P_{\mathrm{stat}}}H(\Pi(H)\mid S_P),
\]

\[
C_{\mathrm{dyn}}^\*=\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}H(\Pi(H)\mid S_P),
\]

and

\[
\Omega_{\mathrm{dyn}}=C_{\mathrm{dyn}}^\*-C_{\mathrm{stat}}^\*.
\]

The premium is nonnegative because dynamic admissibility is an additional constraint. It measures the irreducible state price of preserving future revision capability **after optimizing over currently tied Bayes-optimal actions**.

**Selector/refinement equivalence.** The joint dynamic optimum is equivalently obtained by selecting a Bayes-optimal policy \(d\), computing the coarsest right-congruent refinement of \((S_P,d)\), and minimizing its entropy over all valid selectors. This turns the earlier fixed-policy construction into an exact optimization route rather than an arbitrary modeling choice.

**Typed deficits and bounded universality.** We separate information absent at ingress, information lost for a current responsibility, and information lost only for future revision. We also show that an unrestricted exact responsibility family forces a compressed state toward full history within each predictive fibre, so “universally epistemically sufficient compression” is not meaningful without a responsibility family/horizon.

**LLM evaluation consequence.** Prediction quality and static hidden-state probes are insufficient to certify prospective epistemic state. A stronger representation audit supplies controlled future evidence and checks whether the state supports the correct history-dependent revision at matched linguistic prediction.

## 1.2 Nonclaims

We do not claim that present language models are minimal predictive statistics, that next-token training necessarily erases responsibility information, or that hidden states contain no belief/truth/uncertainty structure. Recent empirical work provides evidence for several such signals, sometimes with causal-use evidence.

We also do not claim a novel general state-minimization algorithm. Compatible-state minimization for incompletely specified FSMs is classical and computationally difficult; generic recurrent sufficient-state theory has strong owners in control and information-state research. The paper survives only if the **relative responsibility/state-cost interpretation and learning-system consequence** remain non-obvious after these parents are fully reconstructed.

---

# 2. Predictive base state

Let \(H\) be a finite positive-support history variable and \(Y^+\) the complete linguistic future under the declared process.

A deterministic state \(Z=f(H)\) is predictive-sufficient when

\[
Y^+\perp H\mid Z.
\]

Define

\[
h\sim_P h'
\iff
P(Y^+\mid H=h)=P(Y^+\mid H=h')
\]

and let \(S_P=[H]_{\sim_P}\).

This is classical predictive-state/sufficient-statistic structure. Every deterministic predictive-sufficient \(Z\) refines \(S_P\). An entropy-minimal exact predictive state is therefore isomorphic to \(S_P\) on support. We use these facts as base assumptions/corollaries, not as headline novelty.

The key freedom is inside predictive fibres: linguistic prediction places no constraint on whether distinctions among histories with the same \(S_P\) value are retained.

---

# 3. Epistemic responsibilities as decisions

A responsibility is

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where \(Q\) is an externally or mechanically defined epistemic target, \(\mathcal A\) the admissible action/terminal set, \(\ell\) a loss, and \(\sigma\) the exact decision semantics.

For history \(h\), define the Bayes-optimal action set

\[
A_r^\*(h)=
\operatorname*{argmin}_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

Examples of epistemic actions include answer/abstain, admit/reject/unresolved, retain/reopen, or retrieve/compute/defer under declared evidence conditions. An arbitrary sentiment or topic label is not an epistemic responsibility unless tied to an epistemic decision contract.

We distinguish:

- **ANY_OPTIMAL_ACTION:** any action in \(A_r^\*(h)\) is acceptable;
- **CANONICAL_ACTION:** a registered tie rule chooses one action;
- **OPTIMAL_ACTION_SET:** all optimal options must be preserved;
- **ACTION_AND_RISK:** action plus Bayes risk/calibrated residual uncertainty is required;
- **EXACT_TARGET:** \(Q\) itself must be recovered.

The distinction changes the minimum state. If two histories have optimal sets \(\{a,b\}\) and \(\{b,c\}\), they can be merged under `ANY_OPTIMAL_ACTION` by choosing \(b\) for both, even though their full option sets differ.

---

# 4. Minimum static responsibility state

For `ANY_OPTIMAL_ACTION`, let

\[
\mathcal D_r=
\{d:d(h)\in A_r^\*(h)\ \forall h\}
\]

be all Bayes-optimal selectors.

## Proposition 1 — selector form

The minimum exact additional deterministic state entropy beyond retained \(S_P\) is

\[
\boxed{
C_{r,\mathrm{any}}^0
=
\min_{d\in\mathcal D_r}H(d(H)\mid S_P).
}
\]

Any sufficient state plus decoder induces a valid selector whose action is a deterministic function of the state, giving the lower bound. Conversely, storing an entropy-minimizing selector action alongside \(S_P\) achieves it.

Under canonical action the selector is fixed. Under full option-set semantics the cost is \(H(A_r^\*(H)\mid S_P)\). Under exact deterministic target recovery with zero-one loss it reduces to \(H(Q\mid S_P)\).

For several `ANY_OPTIMAL_ACTION` responsibilities, the selectors should be optimized jointly:

\[
\min_{d_i\in\mathcal D_{r_i}}
H(d_1(H),\ldots,d_m(H)\mid S_P).
\]

Correlated responsibilities can therefore share state even when their decisions remain logically non-compensatory.

---

# 5. Equivalent partition formulation

A partition \(\Pi\) of histories is **static responsibility-admissible** when:

1. it refines \(S_P\);
2. every block \(B\) has

\[
\bigcap_{h\in B}A_r^\*(h)\ne\varnothing.
\]

One common optimal action can then be decoded for the whole block.

Let \(\mathfrak P_{\mathrm{stat}}\) denote all such partitions and define

\[
C_{\mathrm{stat}}^\*
=
\min_{\Pi\in\mathfrak P_{\mathrm{stat}}}
H(\Pi(H)\mid S_P).
\]

## Proposition 2 — selector/partition equivalence

\[
C_{\mathrm{stat}}^\*
=
\min_{d\in\mathcal D_r}H(d(H)\mid S_P).
\]

A selector induces the partition by \((S_P,d)\). Conversely, choose a common action per admissible block; if equal chosen actions permit additional merging inside a predictive fibre, the selector partition can only reduce conditional entropy.

This formulation is useful because it extends directly to sequential state.

---

# 6. Dynamic responsibility state

Let \(\mathcal X\) be a finite future observation alphabet and \(\delta(h,x)\) a deterministic partial transition on histories, with undefined transitions represented explicitly.

A static-admissible partition is **dynamically admissible** if equivalent histories have matched transition definedness and, whenever transitions exist, their successors remain in the same partition block. In other words, the partition is a right congruence for the registered history extension process.

Let \(\mathfrak P_{\mathrm{dyn}}\subseteq\mathfrak P_{\mathrm{stat}}\) be the dynamically admissible partitions and define

\[
C_{\mathrm{dyn}}^\*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_P).
\]

Any deterministic recurrent state with an optimal-action decoder induces such a partition: equal states share the predictive state, share one decoded Bayes-optimal action, and must update to equal next states under the same input. Conversely, a dynamic-admissible partition can be used as the recurrent state; choose a common optimal action per block and use right congruence to define its transition function.

Thus \(C_{\mathrm{dyn}}^\*\) is the exact finite minimum state cost of **joint policy choice and recurrent representation** under `ANY_OPTIMAL_ACTION`.

## 6.1 Selector-refinement route

For each Bayes-optimal selector \(d\), label histories by \((S_P,d)\) and compute the coarsest right-congruent refinement \(S_\infty^d\). Then

\[
\boxed{
C_{\mathrm{dyn}}^\*
=
\min_{d\in\mathcal D_r}H(S_\infty^d\mid S_P).
}
\]

The forward inequality follows because each refined fixed-selector state is dynamically admissible. For the reverse inequality, choose one common action per block of any optimal dynamic partition; that selector's coarsest right-congruent refinement is no finer than the original dynamic partition.

This equivalence is the exact bridge between Bayes tie selection and recurrent state minimization.

### Parent boundary

The compatible-output/right-congruence problem is closely related to classical incompletely specified FSM minimization, where compatible states and closed covers are standard, compatibility is not generally transitive, minimum machines may not be unique, and exact minimization is computationally hard. We do not claim novelty for that substrate.

---

# 7. Dynamic epistemic optionality premium

Since every dynamic-admissible partition is static-admissible,

\[
C_{\mathrm{dyn}}^\*
\ge
C_{\mathrm{stat}}^\*.
\]

Define

\[
\boxed{
\Omega_{\mathrm{dyn}}
=C_{\mathrm{dyn}}^\*-C_{\mathrm{stat}}^\*
\ge0.
}
\]

This is the additional average state cost imposed **solely by the requirement that a Bayes-optimal epistemic policy remain recursively implementable under future observations**, after optimizing over tied current actions.

The premium is zero when an entropy-minimal static responsibility state can be realized dynamically at the same cost. It is positive when every static-optimal compression merges histories that future responsibility dynamics must distinguish.

## 7.1 Canonical one-bit example

Let two current histories \(h_0,h_1\) be equally likely, share one predictive state and have the same unique current optimal action \(a\). Therefore a one-block static state is admissible and

\[
C_{\mathrm{stat}}^\*=0.
\]

A future observation \(x\) sends the histories to successor states requiring distinct unique actions \(b_0\ne b_1\). If the current histories were merged dynamically, right congruence would force their successors into one block, but that block has no common optimal action. Hence the current histories must already be separated.

Under the equal prior,

\[
C_{\mathrm{dyn}}^\*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit}.
\]

The result survives optimization over current ties because there are no current ties. It isolates future revision memory from current action information.

---

# 8. Information deficits

The state-cost formulation is complemented by a standard information-theoretic diagnostic.

For target \(Q\) evaluated under log loss and representation \(Z=f(H)\),

\[
H(Q\mid Z)=H(Q\mid H)+I(Q;H\mid Z).
\]

We call the first term **acquisition deficit** and the second **current compression deficit**. The names are diagnostic, not new information identities.

For future target \(Q_{t+k}\), current history \(H_t\), retained state \(Z_t\), and future observations \(X_{t+1:t+k}\), define prospective deficit

\[
\Delta_k
=
I(Q_{t+k};H_t\mid Z_t,X_{t+1:t+k}).
\]

Under log loss it is the excess future Bayes loss caused by retaining \(Z_t\) rather than the full past after both see the same future observations.

These deficits distinguish:

- missing evidence;
- information available but discarded for a current responsibility;
- information irrelevant now but discarded before future revision.

The dynamic optionality premium and prospective mutual information are not identical objects: the former is an exact deterministic state-minimization cost for a registered action process, while the latter is an average predictive deficiency for a future target under a joint distribution.

---

# 9. Bounded responsibility families

No compressed state can be exactly sufficient for unrestricted future responsibilities.

For a fixed-signature responsibility family \(C_{\mathcal R}(H)\),

\[
0\le H(C_{\mathcal R}\mid S_P)\le H(H\mid S_P).
\]

If the family separates every pair of histories within each predictive fibre, then \((S_P,C_{\mathcal R})\) determines the full history on support and the upper bound is attained.

More generally, any non-injective state merges two positive-mass histories. Construct an exact binary responsibility assigning different required outputs/actions to the collided pair. Full history solves it exactly; the compressed state cannot.

Therefore “epistemically sufficient state” must always specify its responsibility family and future horizon. If every conceivable exact responsibility is admitted, the only universally sufficient state is effectively history-recoverable.

This is likely a classical sufficiency/no-free-compression corollary. Its role is to prevent the framework from quietly demanding universal memory while advertising compression.

---

# 10. Approximate benchmark

For deterministic exact target \(Q=q(H)\), retain \(S_P\) and allow stochastic augmentation \(U\). Under logarithmic loss,

\[
R(D)=
\inf I(H;U\mid S_P)
\quad\mathrm{s.t.}\quad
H(Q\mid S_P,U)\le D
\]

has the classical solution

\[
R(D)=[H(Q\mid S_P)-D]_+.
\]

Conditionally independent responsibilities yield the product sum, while correlated responsibilities share state. These results are included as exact calibration benchmarks, not as novel rate-distortion theory.

---

# 11. Implications for LLM representation research

## 11.1 Predictive quality is not a responsibility certificate

Equal linguistic prediction does not determine equal hidden-state sufficiency for another decision problem. This is already implied by task-relative sufficiency and representation-identifiability work, so the practical lesson is not that a new impossibility has been discovered; it is that responsibility tests must be declared separately.

## 11.2 Static probes can miss revision failure

A model may expose a decodable/causally usable current truth or confidence signal yet still fail to preserve source, assumption or alternative-hypothesis information required by a later evidence update. A prospective representation audit therefore needs a **controlled future observation** and a history-dependent revision target, not only a static classifier on activations.

## 11.3 Compression/distillation should report optionality

A compressed/distilled representation can be evaluated on four axes:

1. linguistic predictive quality;
2. current responsibility regret/state cost;
3. dynamic/prospective responsibility performance after controlled future evidence;
4. representation memory/rate cost.

The framework predicts a regime where axis 1 and axis 2 are unchanged but axis 3 degrades.

## 11.4 Retrieval can mask memory loss

A system may repeatedly retrieve provenance or support information that was available earlier but discarded. This can restore performance while increasing cost and dependence on source availability. The acquisition/compression distinction identifies such redundant reacquisition.

## 11.5 The result is not “store everything”

Under `ANY_OPTIMAL_ACTION`, current state stores only enough information for an acceptable Bayes action, and dynamic state stores only the additional distinctions required by the declared future responsibility process. Unrestricted future responsibility support is precisely the limiting case that forces history retention.

---

# 12. Strongest parent threats

The paper starts from a pessimistic novelty posture.

**Reward-Predictive State Representations** already own the broad observation that a predictive state can omit a secondary decision variable such as reward.

**Causal states/PSRs** own minimal future-predictive state.

**Information Bottleneck / Deterministic Information Bottleneck** own task-relevant compressed representation.

**Multi-task and contrastive minimal-sufficiency work** already cover the risk that compression for one target loses information relevant to other tasks.

**Approximate Information State (JMLR 2022)** strongly occupies recurrent sufficient history compression and approximate future-decision guarantees.

**POMDP belief/information states** are a longstanding parent for recursive sufficient state.

**Myhill–Nerode/right congruence and incompletely specified FSM minimization** own generic compatible recurrent state reduction and its algorithmic difficulty.

**Log-loss rate-distortion** owns the simple approximate frontier.

The paper survives as standalone theory only if the responsibility-semantic state cost, jointly optimized dynamic optionality premium, and LLM representation-evaluation consequence form a substantive residual rather than an obvious renaming/composition of these parents.

---

# 13. Mechanical verification and publication rule

All scientific design is preregistered before execution. The checker will:

- enumerate Bell-complete partitions on small history sets;
- enumerate Bayes-optimal action selectors;
- verify static selector/partition equivalence;
- enumerate dynamic action-compatible right-congruent partitions;
- independently verify the selector-refinement dynamic optimum;
- check the one-bit premium witness;
- run tie-sensitive selector searches;
- verify entropy/information identities;
- attack assumptions with smallest counterexamples;
- verify responsibility-family saturation constructions;
- locate exact theorem ownership in the frozen parent list.

The execution AI may delete or narrow claims forced by these results. It may not invent a replacement theorem or a post-result novelty argument under this issue identity.

JMLR submission requires every J1–J8 gate in `JMLR_SUBMISSION_GATE_V1.md`. A correct but parent-absorbed paper closes as `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`; a correct but narrow residual may close as `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY`.

---

# 14. Conclusion

The paper's thesis is not that language models lack knowledge, nor that neural learning should be replaced by a formal epistemic layer. It is a state-requirement claim:

> **Internal state should be evaluated relative to what the system is responsible for doing now and what it must remain able to do after future evidence.**

A minimal linguistic predictor can omit responsibility information. But the correct static responsibility cost is not necessarily the entropy of an entire target; it is the minimum state needed to implement the registered epistemic decision semantics. A further gap appears in sequential use: even the optimal current responsibility state can be too small to support future revision. The dynamic optionality premium measures that exact finite cost after optimizing both current Bayes-action choice and recurrent state.

Whether this formulation is itself a substantive new machine-learning theory result is deliberately left to the formal and strongest-parent audits. The result is publishable only if the relative state-cost and prospective evaluation consequence survive those audits without relying on new terminology for established theory.
