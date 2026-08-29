# Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations

**Citation-ready manuscript draft V6**  
**Issue:** #51  
**Status:** post-mechanization, post-parent-contraction; exact bibliography serialization and generated figures remain mechanical.  
**Empirical claim about current LLM hidden states:** none.

---

## Abstract

Autoregressive models are optimized for language prediction but are increasingly expected to make decisions that must later change when evidence, sources, or assumptions change. Existing work already provides minimal predictive states, utility-defined decisional states, task-aware predictive representations, information states, and minimal recursively updateable memory. We therefore do not propose another generic state-minimization theory. Instead, we formalize a representation-assessment problem specific to long-lived autoregressive systems. Taking a state sufficient for the complete declared linguistic future as a reference, we distinguish three obligations: linguistic predictive adequacy, current responsibility-decision adequacy, and prospective evidence-triggered revision adequacy. We define conditional state-cost coordinates for the latter two and a dynamic optionality premium measuring state required solely for later revision after optimizing the present acceptable action. A mechanically verified finite construction has zero extra current-decision state but a one-bit prospective premium. Hence matched language prediction and matched current decisions do not, in general, certify future revision capability. We organize representations into predictive-decisional, current cross-channel, and prospective-refinement regimes and define a horizon-indexed audit. The proposed contribution is a formal prospective revision assessment task and diagnostic framework, not a claim that current language models necessarily discard the relevant information.

---

# 1. Introduction

A model can give the right answer today and still be in the wrong internal state for tomorrow.

Suppose two histories lead to the same language-prediction behavior and the same present decision. In one history, a conclusion depends on source `A`; in the other, it depends on source `B`. Source identity may be irrelevant to both the declared linguistic future and the current decision, so a compressed representation can merge the histories without current observable loss. Later, however, an observation may report that source `A` was retracted. Correct behavior now requires reopening one conclusion while retaining the other. A representation that discarded the support-source distinction cannot necessarily perform that update even though it was adequate at the previous time step.

The underlying state-representation problem has deep prior art. Computational mechanics constructs causal states that are minimal for prediction under its assumptions (Shalizi and Crutchfield, 2001), and Predictive State Representations encode dynamical state through predictions of future observations (Littman, Sutton, and Singh, 2002). Brodu's decisional states partition causal states using a user-supplied utility or payoff function (Brodu, 2011). Reward-Predictive State Representations show directly that a representation sufficient for future observations need not determine future rewards (Baisero and Amato, 2021). POMDP belief states and information-state theory formalize recursively updateable history statistics sufficient for future decision making; Approximate Information State theory gives a particularly broad formulation and approximation guarantees (Subramanian et al., 2022). Compatible-state and right-congruence constructions are classical in finite-state control, and recent stable-quotient work gives a close 2026 characterization of a coarsest exact recursively updateable Markov state and minimal memory in a structured POMDP class (Zhang et al., 2026). Decision-aware compression is also well established through the Information Bottleneck, deterministic variants, Value Equivalence, and rate-distortion formulations for bounded agents (Tishby, Pereira, and Bialek, 1999; Strouse and Schwab, 2017; Grimm et al., 2020, 2021; Arumugam and Van Roy, 2022).

These results rule out a broad novelty claim. The paper does **not** introduce a new generic minimal state construction.

The remaining question is narrower:

> **After two representations are already matched on the declared linguistic prediction target and the registered current decision, can later evidence expose a revision failure caused by information that one representation discarded?**

This is a representation-assessment question. Belief-R already evaluates whether language models update or maintain conclusions after new evidence (Wilie et al., 2024). Our proposed audit adds a different control: before future evidence is revealed, the representations must be matched on current language and current decision behavior; the experiment then manipulates or compares what historical information is retained. The target is therefore **prospective representation adequacy**, not belief revision in general.

## 1.1 Contributions after strongest-parent subtraction

The paper makes four deliberately bounded contributions.

**A three-stage representation audit.** We distinguish (i) linguistic predictive adequacy, (ii) current responsibility-decision adequacy, and (iii) prospective evidence-triggered revision adequacy. The third is not inferred from the first two.

**A finite no-certification result.** We construct and mechanically verify a process with equal language-prediction state and equal unique current optimal action, yet with a one-bit state distinction required solely for the correct later revision. This proves that present prediction plus present decision cannot certify prospective revision adequacy over a process class containing the construction.

**Conditional state-accounting coordinates.** We measure state required by the present responsibility relative to the linguistic predictive reference, and separately measure additional state required only for future recursive revision. The difference is called the dynamic optionality premium. The underlying minimization machinery is parent-owned; the quantity is used as an audit coordinate rather than advertised as a new information law.

**A prospective revision assessment protocol.** We specify present-equivalence gates, update and maintain controls, representation interventions, selective-reopening tests, negative controls, and a collision certificate. The protocol can be applied to a frozen LLM or agent memory without training a new model, though no such empirical result is claimed here.

---

# 2. Parent theory and claim ceiling

## 2.1 Predictive state

Let `H` be a finite history variable and `Y^+` the declared complete linguistic future. Define

\[
h\sim_P h'
\iff
P(Y^+\mid H=h)=P(Y^+\mid H=h').
\]

Let

\[
S_P=[H]_{\sim_P}.
\]

This quotient is an application of classical predictive-state sufficiency. Causal states are defined from equivalence of predictive futures and enjoy minimality properties under the computational-mechanics assumptions (Shalizi and Crutchfield, 2001). Predictive State Representations provide a related observable-history formulation for controlled stochastic systems (Littman, Sutton, and Singh, 2002). We claim no novelty for `S_P` or its predictive minimality.

## 2.2 Decision-relative state

A state needed for a decision can be coarser than a fully predictive state. Brodu (2011) explicitly defines decisional states by applying a user-specified utility to predictive causal states; transitions between decisional states correspond to changes of decision. More generally, statistical decision theory formalizes task-relative sufficiency and the effect of information loss on achievable risk.

Conversely, a representation that is sufficient for one predictive target can omit another target. Baisero and Amato (2021) show that a PSR can be sufficient for future observation probabilities while failing to represent rewards; their Proposition 1 establishes that a reward function over the PSR state need not exist, and their Theorem 1 characterizes when exact linear reward conversion is possible.

Therefore

\[
\text{prediction sufficiency}
\not\Rightarrow
\text{arbitrary secondary-decision sufficiency}
\]

is prior art, not the contribution of this paper.

## 2.3 Recursively updateable state

Long-lived decision systems need more than a present action label. Subramanian et al. (2022) define an information state as a history compression sufficient for current performance and prediction of its next value. Their stronger characterization combines recursive state update with prediction of the next observation, and their Theorem 5 gives the corresponding dynamic program. Standard POMDP belief states are a special case.

Finite-state compatibility and right-congruence theory provides another route to the same structural idea: states that are compatible now may still need to split if equal current labels lead to incompatible successors. Recent work by Zhang et al. (2026) is especially close. It constructs a finite stable quotient through monotone refinement, proves a coarsest exact observation-wise abstraction, shows that observation plus stable class is an exact value-preserving Markov state, and derives a minimal exact class-tracking memory result in its structured HCDP model class.

We therefore treat our recursive refinement as inherited machinery. The paper's distinctive object is **what is conditioned out** before measuring the revision requirement: a separate linguistic predictive state and an already matched current responsibility.

## 2.4 Capacity and decision relevance

The Information Bottleneck formalizes a short representation that preserves task-relevant information (Tishby, Pereira, and Bialek, 1999), while the Deterministic Information Bottleneck replaces mutual-information compression with an entropy-based deterministic encoding objective (Strouse and Schwab, 2017). Value Equivalence argues that a model need preserve only aspects of an environment relevant to value-based planning (Grimm et al., 2020), Proper Value Equivalence develops a stronger planning-sufficiency family (Grimm et al., 2021), and Value-Equivalent Sampling uses rate-distortion theory to trade model simplicity against bounded decision loss (Arumugam and Van Roy, 2022). Log-loss rate-distortion results provide the parent benchmark for our simple finite probabilistic examples (Courtade and Weissman, 2014).

These literatures own the generic principle that limited representation capacity should be allocated to decision-relevant information.

## 2.5 Revision state and language models

Belief revision itself also has extensive theory. Liberatore (2024) studies the storage complexity of several exact representations of doxastic state under iterated belief revision, demonstrating that future revision can impose substantial representation requirements and that different representations have different succinctness.

For LLMs, Belief-R directly tests revision after additional evidence and distinguishes cases where an initial inference should change from cases where it should be retained (Wilie et al., 2024). The latter distinction is important because a system that changes every answer after new text has not demonstrated reliable revision.

The literature on internal LLM belief-like states further prevents a simplistic premise that language models contain no relevant internal structure. Herrmann and Levinstein (2025) propose Accuracy, Coherence, Uniformity, and Use as criteria for belief-like representations. Corona Mendozza and Søgaard (2026) find truth-sensitive and causally usable signals in residual and attention-head activations, while Cheang et al. (2026) show that some internal signals associated with apparent self-knowledge can primarily track parametric recall rather than truthfulness. Finally, predictor-equivalent behavior does not in general identify arbitrary representation properties (Sevetlidis, 2026).

Our audit therefore asks neither “does the model have beliefs?” nor “is truth linearly decodable?” It asks whether a declared retained state supports a registered revision responsibility under controlled future evidence.

---

# 3. Responsibility contracts

A responsibility is an operational decision contract

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where `Q` is a mechanically or externally specified target, `\mathcal A` a finite action/terminal set, `\ell(a,q)` a registered loss, and `\sigma` an exact semantic requirement.

We use five possible exact semantics:

- `ANY_OPTIMAL_ACTION`;
- `CANONICAL_ACTION`;
- `OPTIMAL_ACTION_SET`;
- `ACTION_AND_RISK`;
- `EXACT_TARGET`.

For a present history `h`, let

\[
A^*(h)
=
\arg\min_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h]
\]

be the Bayes-optimal action set.

Under `ANY_OPTIMAL_ACTION`, an implementation need preserve only enough information to choose **some** member of `A^*(h)`. This matters when optimal action sets overlap. If two histories have sets `\{a,b\}` and `\{b,c\}`, the same action `b` is acceptable for both; storing the two complete sets would overstate the decision's actual state requirement.

Institutional authority is outside this internal decision contract. A representation may encode support or uncertainty; it does not create legitimate permission to deploy or publish.

---

# 4. Current responsibility adequacy

Let `\mathcal D` denote the set of acceptable Bayes-optimal selectors `d(h)\in A^*(h)`.

In the registered finite exact setting, define

\[
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}H(d(H)\mid S_P).
\]

An equivalent partition formulation groups histories only when they lie in one `S_P` fibre and have at least one common acceptable action. The equivalence between the selector and compatible-partition forms is proved in Appendix B and independently checked by exhaustive finite enumeration.

This conditional entropy is not proposed as a new decision-theoretic complexity. It is an **accounting coordinate**: how much state beyond the declared linguistic predictive reference is required by the present responsibility?

## 4.1 P0 — no additional current state

\[
C_{\mathrm{stat}}^*=0
\]

if and only if some acceptable Bayes-optimal selector is a function of `S_P` on positive-probability support. Thus the framework assigns zero augmentation when the linguistic predictive state already supports the decision. This is a mandatory negative control consistent with decisional-state theory.

## 4.2 Current cross-channel refinement

If

\[
C_{\mathrm{stat}}^*>0,
\]

then no acceptable current policy factors through `S_P` alone. At least one distinction inside a predictive fibre matters to the registered decision.

We call such a distinction **cross-channel** only as a scoped shorthand: it is not measurable from the declared linguistic predictive quotient. It need not be statistically independent of text or carried by a separate physical channel. Candidate variables include source identity, evidence dependence, scope epoch, evaluator identity, or lineage.

---

# 5. Prospective revision adequacy

Let `x` be a registered future observation and `\delta(h,x)` the successor history when defined. A representation that is sufficient for the current action may still be impossible to update recursively.

A dynamic state must therefore satisfy both:

1. current action compatibility; and
2. successor compatibility under every registered feasible future observation.

Let `\mathfrak P_{\mathrm{dyn}}` be the resulting dynamic-admissible finite partitions. Define

\[
C_{\mathrm{dyn}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_P).
\]

Equivalently, in the registered deterministic setting,

\[
C_{\mathrm{dyn}}^*
=
\min_{d\in\mathcal D}
H(S_\infty^d\mid S_P),
\]

where `S_\infty^d` is the stable right-congruent refinement of the present label `(S_P,d)`. The equivalence is proved in Appendix D and mechanically verified by independent direct and selector-based calculations.

The component minimization ideas are parent-owned (Subramanian et al., 2022; Zhang et al., 2026; classical finite-state compatibility theory). Their role here is to support the prospective audit.

---

# 6. Dynamic optionality premium

Define

\[
\boxed{
\Omega_{\mathrm{dyn}}
=
C_{\mathrm{dyn}}^*-C_{\mathrm{stat}}^*
}.
\]

Because dynamic-admissible states are a subset of static-admissible states,

\[
\Omega_{\mathrm{dyn}}\ge0.
\]

`Omega_dyn` measures state required **only because the current acceptable responsibility must remain correct under the registered future evidence process**. It is a derived audit metric, not a new information-theoretic law.

---

# 7. A one-bit no-certification witness

Consider two equiprobable histories, `h_A` and `h_B`, sharing one linguistic predictive state:

\[
S_P(h_A)=S_P(h_B).
\]

Suppose their unique present Bayes-optimal action is the same:

\[
A^*(h_A)=A^*(h_B)=\{\mathrm{RETAIN}\}.
\]

The histories differ only in a provenance bit indicating whether the current conclusion depends on source `A` or source `B`.

Now reveal the same later evidence event

\[
x=\mathrm{RETRACT}(A).
\]

At the successor histories, let the unique required actions be

\[
h_A'\to\mathrm{REOPEN},
\qquad
h_B'\to\mathrm{RETAIN}.
\]

Then present action compatibility permits the two histories to share one state, so

\[
C_{\mathrm{stat}}^*=0.
\]

But any recursively adequate state must distinguish them before the future event; otherwise the same current state plus the same event would have to produce the same successor decision. Since the histories are equiprobable,

\[
C_{\mathrm{dyn}}^*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit}.
\]

The mechanical suite reproduces these values exactly.

---

# 8. Present adequacy does not certify future revision

## Theorem 1 — no-certification theorem

There exists a finite process and two representations `Z_c,Z_a` such that:

1. `Z_c` and `Z_a` are equally adequate for the declared complete linguistic prediction target;
2. both support the same zero-regret current responsibility decision;
3. after the same future evidence, their achievable future responsibility risks differ.

Consequently, an evaluation observing only present linguistic prediction and present responsibility performance cannot, in general, certify prospective revision adequacy over a process class containing this construction.

### Proof sketch

Let

\[
Z_c=S_P
\]

and

\[
Z_a=(S_P,B),
\]

where `B` is the provenance bit from Section 7. The bit changes neither the declared language target nor the unique present action, so the representations are indistinguishable on those present criteria. After `RETRACT(A)`, however, the augmented state can produce distinct successor decisions while `Z_c` cannot distinguish the two histories. The full proof is in `PROOF_APPENDIX_V1.md`. ∎

The theorem is an existence/no-certification result. It does not assert that an actual LLM uses `Z_c`.

---

# 9. Prospective revision collisions

For an audited representation `Z`, a **prospective revision collision** is a tuple `(h,h',x)` such that:

1. `Z(h)=Z(h')`;
2. the histories are matched for the declared present linguistic target;
3. they admit the same present responsibility action;
4. the same future evidence event `x` is feasible;
5. the acceptable future action sets after `x` are disjoint.

A collision is a direct certificate that no deterministic future decision rule using only `(Z,x)` can be exactly sufficient for both histories. This is an ordinary decision-fibre argument, used here as an auditable witness rather than claimed as new mathematics.

The canonical one-bit construction is a collision: the compressed state merges the `A`-supported and `B`-supported histories, while the same retraction event requires different future actions.

A collision certificate is useful in experiments because it identifies **which distinction was lost**, rather than merely reporting an aggregate revision error.

---

# 10. P0/P1/P2 audit taxonomy

The finite exact state costs define three diagnostic regimes.

## P0 — predictive-decisional

\[
C_{\mathrm{stat}}^*=0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The linguistic predictive state already supports the current and registered future responsibility.

## P1 — current cross-channel refinement

\[
C_{\mathrm{stat}}^*>0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

Additional information is required for the current responsibility, but no extra dormant distinction is required for later update.

## P2 — prospective refinement

\[
\Omega_{\mathrm{dyn}}>0.
\]

Even an optimally compressed state for the current responsibility discards information required by some registered later evidence-triggered decision.

P2 may occur with zero or positive present cross-channel cost. These phases classify representation obligations, not levels of intelligence.

---

# 11. Horizon-indexed audit

For future horizon `k`, let `\mathfrak P_k` be the static-compatible states that remain compatible under every registered feasible observation sequence of length at most `k`. Define

\[
C_k^*
=
\min_{\Pi\in\mathfrak P_k}
H(\Pi(H)\mid S_P),
\qquad
\Omega_k=C_k^*-C_0^*.
\]

The feasible sets are nested, so

\[
C_0^*\le C_1^*\le\cdots.
\]

Finite registered systems stabilize because finite partition refinement can split only finitely often. These are classical finite-state facts. The audit interpretation asks a practical question: **how far into the registered evidence process does the retained representation remain sufficient?**

The mechanical suite verified monotonicity and stabilization in every registered finite horizon fixture.

---

# 12. Representation Audit Profile

We recommend reporting four coordinates rather than a scalar “knowledge” or “epistemic quality” score.

## 12.1 Linguistic predictive deficiency

Under log loss in the finite reference setting,

\[
\Delta_{\mathrm{pred}}(Z)
=
H(Y^+\mid Z)-H(Y^+\mid H).
\]

## 12.2 Current responsibility regret

For responsibility `r`, define

\[
\mathcal R_r(V)
=
\mathbb E\left[
\min_a\mathbb E[\ell(a,Q)\mid V]
\right],
\]

and

\[
\delta_0(Z;r)
=
\mathcal R_r(Z)-\mathcal R_r(H).
\]

## 12.3 Prospective revision regret

For later evidence `X_{1:k}` and future responsibility `r_{t+k}`,

\[
\delta^{\mathrm{rev}}_k(Z;r)
=
\mathcal R_{r_{t+k}}(Z_t,X_{1:k})
-
\mathcal R_{r_{t+k}}(H_t,X_{1:k}).
\]

## 12.4 Operational state cost

In finite exact fixtures, conditional entropy relative to `S_P` is available. Real neural systems require a registered operational capacity measure, such as retained tokens, transmitted bits under a fixed encoder, memory slots, or serialized memory bytes. Hidden-state dimension alone is not an information measure.

The audit profile is

\[
\boxed{
\operatorname{RAP}_k(Z;r)
=
(
\Delta_{\mathrm{pred}},
\delta_0,
\delta^{\mathrm{rev}}_k,
\operatorname{Cost}
).
}
\]

The coordinates are not compensatory. Better language prediction does not cancel a future-revision failure.

---

# 13. Three different failure sources

Under logarithmic loss, the framework separates three information deficits.

## Acquisition deficit

\[
H(Q\mid H).
\]

The accessible history did not contain enough information. More internal computation cannot manufacture missing evidence.

## Current compression deficit

\[
I(Q;H\mid Z).
\]

The history contained useful information, but the representation discarded it for the current responsibility.

## Prospective revision deficit

\[
I(Q_{t+k};H_t\mid Z_t,X_{1:k}).
\]

The representation discarded current historical information that becomes useful only after later evidence.

These are standard information-theoretic identities, included to route failures to different interventions rather than to claim a new decomposition theorem.

---

# 14. Bounded responsibility families

No compressed state should be called universally epistemically sufficient without naming the responsibility family it promises to support.

For any deterministic responsibility signature `C_\mathcal R(H)`,

\[
0
\le
H(C_\mathcal R\mid S_P)
\le
H(H\mid S_P).
\]

If the family separates every positive-support history pair within predictive fibres, it recovers all non-predictive history information and reaches the upper bound. Every non-injective finite state also admits some constructed binary exact responsibility on which it fails.

These are elementary/classical boundaries. Their methodological consequence is important: prospective adequacy is always relative to a **bounded responsibility family and future evidence horizon**.

---

# 15. Mechanical validation

Four mechanical-execution batches were merged into the theory branch.

## Static layer

All set partitions through `n=7` were exhaustively enumerated with Bell numbers

\[
1,2,5,15,52,203,877.
\]

The suite verified predictive-refinement structure, all registered responsibility semantics, tie behavior, selector/partition equivalence, joint state sharing, and the zero-cost common-action criterion.

## Information deficits

The acquisition/current-compression/prospective identities and mandatory controls were tested over 900 seeded rational worlds using exact log-linear arithmetic with a high-precision decimal cross-check.

## Dynamic and horizon layer

Direct dynamic-partition and selector-refinement computations agreed on all registered fixtures. The suite verified non-negative `Omega_dyn`, the exact one-bit witness, P0/P1/P2 controls, horizon monotonicity and stabilization, family monotonicity, and bounded/universality checks.

A search of 5,826 small machines did not find a registered mixed-P2 witness; this remains `CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS` and is not promoted to a theorem.

## Assumption attacks

The mutation battery found that entropy minimality and positive-probability support are load-bearing for the exact predictive-state isomorphism claim, and that near-minimal entropy provides no structural stability guarantee without additional assumptions. Registered approximate/stochastic/cardinality variants retained narrower conclusions.

One non-load-bearing worst-fibre/cardinality item lacked a distinct mechanical check and has been dropped from the publication claim set rather than defended for completeness.

---

# 16. Prospective Revision Audit protocol

The full protocol is frozen in `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V1.md`. Its central experimental logic is:

1. **Register an episode.** Bind initial history, current responsibility, future evidence classes, future responsibility, update/maintain gold, dormant variables, nuisance variables, and resources.
2. **Include negative controls.** Acquisition-limited cases, P0 cases, P1 current-state cases, and P2 prospective cases are all mandatory.
3. **Match present behavior.** Representation conditions must satisfy registered tolerances for language prediction and current decision/risk before future evidence is revealed.
4. **Intervene on retained state.** Compare full history, prediction-preserving state, current-decision-sufficient state, and prospective-augmented state where feasible.
5. **Reveal future evidence.** Measure both update and maintain/selective-reopening performance.
6. **Emit collision certificates.** When a representation merges histories that later require incompatible actions after the same evidence, record the exact matched pair and state intervention.
7. **Preserve negative terminals.** If later evidence reconstructs the dormant variable, if full history is non-identifying, or if the present state already differs, do not classify the case as a P2 retention failure.

This is stronger than simply checking whether a model changes an answer after new text because it attempts to isolate **representation retention after present equivalence has been established**.

---

# 17. Relation to Belief-R and LLM memory studies

Belief-R is the mandatory nearest LLM assessment baseline (Wilie et al., 2024). It asks whether a conclusion should update or remain after later premises. The Prospective Revision Audit asks a different causal question:

> after current language and current decision behavior have been matched, does manipulating what history a representation retains selectively change later update/maintain performance?

This distinction matters because output revision alone cannot identify which information the representation retained. Representation identifiability work shows more generally that predictor behavior does not determine arbitrary hidden representation properties (Sevetlidis, 2026).

Recent LLM-agent work also makes the memory question practically relevant. Decision-Aware Memory Cards explicitly selects and compresses context according to decision utility (Guan, Zhao, and Deng, 2026), while AgenticSTS treats long-horizon memory as a bounded typed retrieval contract that can be ablated by layer (Cheng et al., 2026). These are practical neighbors rather than novelty support: decision-aware and bounded LLM memory are already active research areas.

---

# 18. What a frozen-model experiment could test

A future empirical study need not train an LLM.

Possible representation surfaces include:

- prompt/context memory;
- deterministic summaries;
- typed external agent memory;
- KV-cache compression where accessible;
- hidden-state projection if present behavior remains matched;
- selective removal or retention of source/provenance fields.

The central load-bearing contrast is between a current-decision-sufficient condition and a prospective-augmented condition on P2 tasks. The study must distinguish:

- information never available;
- information retained but not used;
- information compressed away;
- information reconstructed from future evidence;
- ordinary reasoning failure after the correct state was retained.

A hidden-state probe alone is insufficient for a causal retention claim. Prefer an explicit memory/state intervention whose present-behavior effect can be checked before the future evidence is introduced.

---

# 19. Limitations

**Finite exact foundation.** The strongest checked statements are finite and discrete. Neural hidden states are continuous and high-dimensional.

**Idealized predictive reference.** Exact `S_P` is generally unavailable for a deployed LLM. A real study must use a registered language-prediction surrogate and must not claim exact causal-state recovery.

**Responsibility selection is external.** The framework does not determine which revision responsibilities a scientific institution or society ought to impose.

**Representation cost is implementation-dependent in real models.** Conditional entropy is exact in finite fixtures, but a neural study requires an operational capacity measure.

**The mathematical substrate is heavily parent-owned.** Predictive state, decision state, information state, right-congruent recurrent state, and capacity tradeoffs all have strong prior theory.

**Belief revision already has benchmarks.** The proposed audit is not the first test of updating after evidence; it adds a matched representation-retention intervention.

**No empirical LLM failure is established.** The current result is an existence/no-certification theorem plus a frozen assessment protocol.

**Unbounded responsibility families defeat compression.** Practical claims require bounded responsibility and evidence horizons.

---

# 20. Publication positioning

The strongest-parent reconstruction makes the paper unsuitable as a claim of a new generic state theory. A JMLR submission is defensible only through the journal's scope for formalization of new learning tasks, performance-assessment methods, and analytical frameworks for practical learning systems.

The current internal assessment is:

```text
JMLR new-core-theorem route = fail
JMLR assessment/framework route = open, high risk
TMLR route = strong fallback
```

The controlling editorial question is whether the **matched prospective revision audit** is sufficiently distinct and broadly useful relative to information-state theory, Belief-R, and contemporary decision-aware memory work. No additional theorem should be invented to force that gate.

---

# 21. Conclusion

Prediction, present decision, and future revision are different representation obligations.

Existing theory already explains much of how to compress history for prediction or decision and how to construct recursively updateable state. The contribution here is narrower: a way to **audit an autoregressive representation against three separately registered requirements**.

The exact one-bit construction proves why the third test is necessary. Two representations can be indistinguishable on the declared complete linguistic prediction target and on the current unique optimal decision, yet differ in whether they retained a dormant historical distinction that later evidence makes decisive. Present performance therefore cannot certify prospective revision adequacy in general.

For language-model and agent research, the resulting question is concrete:

> **After current language and decision behavior are matched, does the retained representation preserve the information needed for the correct update when evidence changes?**

That question can be studied in frozen models, external memories, context compression, or synthetic representations without claiming consciousness, human-like belief, or a new neural architecture. It is the bounded Machine-Epistemic contribution that survives strongest-parent subtraction.

---

# References — citation-ready metadata list

The final `.bib` should be generated mechanically from official metadata, preserving the following scientific roles.

- Arumugam, D. and Singh, S. P. (2022). *Planning to the Information Horizon of BAMDPs via Epistemic State Abstraction.* NeurIPS 35.
- Arumugam, D. and Van Roy, B. (2022). *Deciding What to Model: Value-Equivalent Sampling for Reinforcement Learning.* NeurIPS 35. DOI `10.52202/068431-0656`.
- Baisero, A. and Amato, C. (2021). *Reconciling Rewards with Predictive State Representations.* IJCAI, 2170–2176. DOI `10.24963/ijcai.2021/299`.
- Brodu, N. (2011). *Reconstruction of Epsilon-Machines in Predictive Frameworks and Decisional States.* Advances in Complex Systems 14(5), 761–794. DOI `10.1142/S0219525911003347`.
- Cheang, C. S., Chan, H. P., Zhang, W., and Deng, Y. (2026). *Do LLMs Really Know What They Don’t Know? Internal States Mainly Reflect Knowledge Recall Rather Than Truthfulness.* Findings of ACL 2026, 713–730. DOI `10.18653/v1/2026.findings-acl.34`.
- Cheng, X. et al. (2026). *AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents.* arXiv:2607.02255.
- Corona Mendozza, A. and Søgaard, A. (2026). *LLM Beliefs Are in Their Heads.* ACL 2026, 41033–41067. DOI `10.18653/v1/2026.acl-long.1905`.
- Courtade, T. A. and Weissman, T. (2014). *Multiterminal Source Coding under Logarithmic Loss.* IEEE Transactions on Information Theory 60(1), 740–761. DOI `10.1109/TIT.2013.2288257`.
- Grimm, C., Barreto, A., Singh, S. P., and Silver, D. (2020). *The Value Equivalence Principle for Model-Based Reinforcement Learning.* NeurIPS 33.
- Grimm, C., Barreto, A., Farquhar, G., Silver, D., and Singh, S. (2021). *Proper Value Equivalence.* NeurIPS 34.
- Guan, X., Zhao, Q., and Deng, Y. (2026). *Decision-Aware Memory Cards: Counterfactual-Inspired Context Selection and Compression for Tool-Using LLM Agents.* arXiv:2606.08151.
- Herrmann, D. A. and Levinstein, B. A. (2025). *Standards for Belief Representations in LLMs.* Minds & Machines 35(1), Article 5. DOI `10.1007/s11023-024-09709-6`.
- Liberatore, P. (2024). *Representing States in Iterated Belief Revision.* Artificial Intelligence 336, 104200. DOI `10.1016/j.artint.2024.104200`.
- Littman, M. L., Sutton, R. S., and Singh, S. (2002 / NeurIPS 14 proceedings). *Predictive Representations of State.* Advances in Neural Information Processing Systems 14, 1555–1561. Final year convention to follow official NeurIPS BibTeX.
- Sevetlidis, V. (2026). *A Fiber Criterion for Representation Identifiability in Supervised Learning.* arXiv:2606.01092.
- Shalizi, C. R. and Crutchfield, J. P. *Computational Mechanics: Pattern and Prediction, Structure and Simplicity.* Final journal metadata to be normalized mechanically from the canonical record; arXiv `cond-mat/9907176`.
- Strouse, D. J. and Schwab, D. J. (2017). *The Deterministic Information Bottleneck.* Neural Computation 29(6), 1611–1630. DOI `10.1162/NECO_a_00961`.
- Subramanian, J., Sinha, A., Seraj, R., and Mahajan, A. (2022). *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems.* JMLR 23(12), 1–83.
- Tishby, N., Pereira, F. C., and Bialek, W. (1999). *The Information Bottleneck Method.* 37th Annual Allerton Conference on Communication, Control, and Computing, 368–377.
- Wilie, B., Cahyawijaya, S., Ishii, E., He, J., and Fung, P. (2024). *Belief Revision: The Adaptability of Large Language Models Reasoning.* EMNLP 2024, 10480–10496. DOI `10.18653/v1/2024.emnlp-main.586`.
- Zhang, Z., Chen, Y., Imani, M., and Lan, T. (2026). *Minimal Markovization via Stable Quotients in Holonomy-Cover Decision Processes.* arXiv:2607.27132v1.
- *History, Hypergraphs, and Memory: The Exact Complexity of Deviation-Rational Control.* Public double-blind RLC 2026 / RLJ manuscript, OpenReview `oNLGDwZo5d`; author/publication identity must be rechecked at bibliography freeze.
