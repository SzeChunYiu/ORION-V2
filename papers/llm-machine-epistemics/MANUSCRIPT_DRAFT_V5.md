# Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations

**Post-mechanization manuscript draft V5**  
**Issue:** #51  
**Supersedes:** V1–V4 for scientific positioning.  
**Status:** mechanically supported analytical-framework candidate under final publication routing.  
**Empirical claim about current LLM hidden states:** none.  
**Primary venue aspiration:** JMLR analytical-framework / new-assessment-task route only; new-core-theorem route is withdrawn.

---

## Abstract

Autoregressive models are optimized for language prediction but are increasingly expected to make decisions that must later change when evidence, sources, or assumptions change. Existing theory already provides minimal predictive states, utility-defined decisional states, reward-predictive representations, information states, and minimal recursively updateable memory. We therefore do not propose another generic state-minimization theory. Instead, we formalize a representation-audit problem specific to this deployment pattern. Taking the minimal state sufficient for the complete linguistic future as a reference, we distinguish three obligations: linguistic predictive adequacy, current responsibility-decision adequacy, and prospective evidence-triggered revision adequacy. We define conditional state-cost coordinates for the latter two and a dynamic optionality premium measuring memory required solely for later revision after optimizing the present acceptable action. Exact finite audits verify a canonical case with zero extra current-decision state but a one-bit prospective premium. Thus matched linguistic prediction and matched current decisions do not logically certify future revision capability. We organize representations into predictive-decisional, current cross-channel, and prospective-refinement regimes and give a horizon-indexed audit. The contribution is a prospective representation-assessment framework, not a claim that current LLMs necessarily lose such information.

---

# 1. Introduction

A model can give the right answer today and still be in the wrong internal state for tomorrow.

Suppose two histories lead to the same linguistic continuation distribution and the same present decision. In one history, the present conclusion depends on source `A`; in the other, it depends on source `B`. If source identity is irrelevant to current language prediction and the present decision, a compressed representation may merge the histories without observable current loss. Later, however, an observation may report that source `A` was retracted. Correct behavior now requires reopening one conclusion while retaining the other. A representation that discarded the source distinction cannot necessarily perform that update even though it was perfectly adequate at the previous time step.

The example sounds like a statement about “epistemic memory”, but most of its mathematical ingredients are not new. Computational mechanics and predictive-state theory provide future-sufficient states. Statistical decision theory and Brodu's decisional states formalize decision-relative information. Reward-Predictive State Representations show that an observation-predictive state can omit a reward target. POMDP belief states and information-state theory formalize recursively updateable history statistics for control. Incompletely specified finite-state-machine minimization uses current compatibility plus successor closure. Recent stable-quotient work characterizes a coarsest exact recursively updateable Markov state in a structured partially observed class. Value-equivalence and rate-distortion work study what a bounded agent should retain for downstream decisions. Belief-R already evaluates whether language models revise conclusions after new evidence.

These parents rule out a broad novelty claim. The question left open for this paper is narrower and operational:

> **If a representation is already adequate for the complete linguistic prediction target and the registered current decision, has it retained the information required to revise that decision correctly after later evidence?**

We call this **prospective revision adequacy**. The term denotes an evaluation obligation, not a new ontology of cognition.

The central methodological point is that three tests should not be conflated:

1. **Prediction:** does the representation retain the information needed for the declared linguistic future?
2. **Current decision:** does it retain the information needed for the registered decision now?
3. **Prospective revision:** after a later evidence event, does it retain enough dormant information to update the decision correctly?

The third does not follow from the first two. The finite exact construction in this paper makes that failure explicit and quantifies its memory cost.

## 1.1 Contributions after strongest-parent subtraction

The paper claims a formal assessment framework rather than ownership of the classical minimization substrate.

**Reference-channel decomposition.** We take the complete linguistic predictive quotient as the reference channel and measure additional representation requirements relative to it. This separates linguistic prediction information from responsibility-specific information rather than treating all history information as one state variable.

**Decision-relative current-state accounting.** A responsibility is a registered decision contract, not an arbitrary auxiliary label. Under permissive `ANY_OPTIMAL_ACTION` semantics, the representation need preserve only enough information to implement some Bayes-optimal action, not the full target or the full set of tied actions.

**Prospective revision accounting.** We distinguish the minimum state needed for a present acceptable decision from the minimum recursively updateable state that can continue satisfying the responsibility under registered future observations. Their difference is a dynamic optionality premium.

**No-certification result.** An exact finite witness has zero additional current-decision state but requires one bit solely for correct later revision. Consequently, an evaluation that checks linguistic prediction and current decision performance alone cannot certify prospective revision adequacy over the declared process class.

**P0/P1/P2 audit taxonomy and horizon curve.** We separate cases in which linguistic predictive state already suffices, cases requiring current cross-channel refinement, and cases requiring extra dormant state only for future revision. A horizon-indexed cost identifies how far into the declared evidence process additional distinctions become necessary.

**LLM representation-audit prescription.** We formalize how a future frozen-model study could distinguish ordinary belief revision from representation retention: match current linguistic and decision behavior, alter or compare retained state, and then supply evidence whose correct revision depends on a previously dormant cross-channel distinction.

We do **not** claim a new generic minimal state theorem, a new finite-state minimization algorithm, a new belief-revision benchmark in general, or empirical failure of current LLM hidden states.

---

# 2. Parent theory and the claim ceiling

The paper is easiest to understand by stating what is already known.

## 2.1 Complete-future predictive state

Let `H` be a finite history variable and `Y^+` the declared complete linguistic future. Define

\[
h\sim_P h'
\iff
P(Y^+\mid h)=P(Y^+\mid h').
\]

Let

\[
S_P=[H]_{\sim_P}.
\]

This is an application of classical predictive/causal-state sufficiency. We claim no novelty for the quotient or its minimality.

## 2.2 Decision-relative states

Given a utility/loss, classical decision theory asks which information is needed to achieve an optimal decision. Brodu's decisional-state framework applies a user-supplied utility to causal states and creates coarser decision partitions. If the decision is entirely determined by the predictive distribution represented by `S_P`, no extra representation is required.

That zero-cost case is a mandatory control in our framework.

## 2.3 A predictive state can omit another target

Reward-Predictive State Representation work establishes a direct precedent: a state accurate for observation prediction need not be accurate for rewards, while an augmented representation can preserve both.

Therefore the statement

\[
\text{predictive sufficiency}
\not\Rightarrow
\text{secondary-target sufficiency}
\]

is background, not our headline result.

## 2.4 Recursively updateable decision state

POMDP belief states, information states, Approximate Information State theory, right-congruence constructions, incomplete-FSM closed-cover minimization, and recent stable-quotient Markovization all formalize versions of the requirement that a current decision-relevant state must also evolve correctly under future observations.

In particular, recent stable-quotient work starts from immediate reward/control distinctions and iteratively propagates them backwards through possible successor transitions until a stable recursively sufficient quotient is reached. This is structurally close to the dynamic refinement we use below.

Our contribution is therefore **not** the refinement algorithm. It is the conditional accounting and representation-audit interpretation relative to a distinct linguistic predictive reference state.

## 2.5 Decision-aware capacity tradeoffs

Value Equivalence, Proper Value Equivalence, Value-Equivalent Sampling, information bottleneck, and rate-distortion theory all support the broader lesson that limited representation capacity should be allocated to information relevant to downstream decisions rather than to exact reconstruction of the environment.

Again, we claim no ownership of that principle.

## 2.6 Belief revision in language models

Belief-R (Wilie et al., EMNLP 2024) explicitly presents additional evidence to language models and measures whether an initial conclusion should be updated or retained. Other recent studies analyze LLM numerical belief updating and evidence-selection effects.

Our proposed audit differs in what is controlled. It does not merely ask whether the model can revise an output when a new premise appears. It asks whether **two representations that are already matched on the present prediction and present decision can differ in their ability to use later evidence because one retained a dormant cross-channel distinction and the other did not**.

---

# 3. Responsibility contracts

An epistemic responsibility in this paper is an operational decision contract

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where:

- `Q` is a mechanically or externally specified target relevant to the inquiry;
- `\mathcal A` is a finite set of admissible actions or terminals;
- `\ell(a,q)` is a registered loss;
- `\sigma` declares what exact information the implementation must preserve.

We distinguish five exact semantics:

- `ANY_OPTIMAL_ACTION`;
- `CANONICAL_ACTION`;
- `OPTIMAL_ACTION_SET`;
- `ACTION_AND_RISK`;
- `EXACT_TARGET`.

This distinction matters because storing a full target can be unnecessarily expensive.

For history `h`, define the Bayes-optimal action set

\[
A^*(h)
=
\arg\min_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

Under `ANY_OPTIMAL_ACTION`, any selector

\[
d(h)\in A^*(h)
\]

is acceptable. If two histories have optimal sets `\{a,b\}` and `\{b,c\}`, they can share an internal decision state by selecting `b`. A theory that stores both option sets would overstate the responsibility's actual state requirement.

Institutional or scientific authority is outside this contract. A model can internally represent support or uncertainty; it cannot manufacture legitimate permission to act, deploy, or publish.

---

# 4. Current responsibility adequacy

Let `\mathcal D` be the set of acceptable Bayes-optimal selectors under the registered semantics.

In the finite exact `ANY_OPTIMAL_ACTION` case, define the current responsibility cost relative to the linguistic predictive state as

\[
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}
H(d(H)\mid S_P).
\]

An equivalent partition formulation groups histories only when:

1. they lie inside the same `S_P` fibre; and
2. their Bayes-optimal action sets have a common acceptable action.

The mechanics of compatible-state minimization are parent-owned. We use the conditional entropy only as an accounting coordinate relative to the reference language state.

## 4.1 P0: zero additional current state

\[
C_{\mathrm{stat}}^*=0
\]

iff some acceptable Bayes-optimal selector factors through `S_P`:

\[
d(H)=\bar d(S_P).
\]

This is the predictive-decisional control case. The language predictive state already contains everything required for the current responsibility.

## 4.2 P1/P2 precursor: positive cross-channel state

\[
C_{\mathrm{stat}}^*>0
\]

means no acceptable current responsibility policy can be implemented from `S_P` alone. A distinction inside at least one linguistic predictive fibre matters to the decision.

We call the missing distinction **cross-channel** because it is not measurable from the declared linguistic predictive quotient. It need not be statistically independent of language or carried by a physically separate subsystem.

Examples include source identity, evidence dependence, scope epoch, evaluator identity, or lineage information that does not alter the declared language-future distribution but does alter a registered responsibility decision.

---

# 5. Prospective revision adequacy

Current decision adequacy is not enough for a long-lived state.

Let `x` denote a future observation/event and

\[
\delta(h,x)
\]

its history transition when defined.

A representation that merges `h` and `h'` is recursively usable only if every jointly feasible future observation keeps the successor histories representationally compatible for the registered future responsibility process.

A **dynamic-admissible** state therefore satisfies both:

- present action compatibility;
- successor/right-congruence compatibility.

Define the minimum dynamic cost relative to `S_P`:

\[
C_{\mathrm{dyn}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_P).
\]

Equivalently, in the registered finite exact model,

\[
C_{\mathrm{dyn}}^*
=
\min_{d\in\mathcal D}
H(S_\infty^d\mid S_P),
\]

where `S_\infty^d` is the stable right-congruent refinement induced by selector `d`.

These minimization structures have direct parents in information-state theory, compatible finite-state-machine minimization, and stable-quotient Markovization. The paper uses them to define a *relative representation audit*, not to claim a new generic algorithm.

---

# 6. Dynamic optionality premium

Define

\[
\boxed{
\Omega_{\mathrm{dyn}}
=
C_{\mathrm{dyn}}^*
-
C_{\mathrm{stat}}^*
}.
\]

Since dynamically admissible representations satisfy at least the static requirements,

\[
\Omega_{\mathrm{dyn}}\ge0.
\]

Interpretation:

> `Omega_dyn` is the additional retained state required only because an acceptable current responsibility policy must remain correct under the registered future evidence process.

It is an accounting metric over parent-owned state classes. We do not present the non-negativity identity as a new information-theoretic law.

## 6.1 Verified one-bit witness

The registered finite construction contains two equiprobable current histories with:

- one shared complete linguistic predictive state;
- one shared **unique** current Bayes-optimal responsibility action;
- one latent provenance bit that is irrelevant to the current action;
- a later evidence event under which the two successor histories require different unique actions.

Exact mechanical execution gives

\[
C_{\mathrm{stat}}^*=0,
\qquad
C_{\mathrm{dyn}}^*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit}.
\]

The use of a unique current action removes tie-selection as an explanation.

This example is small, but it establishes the logical separation needed by the audit below.

---

# 7. An audit-necessity proposition

The one-bit construction implies the following assessment statement.

## Proposition — present adequacy does not certify revision adequacy

There exists a finite process and two representations with equal complete-linguistic predictive adequacy and equal current responsibility adequacy but unequal future evidence-triggered revision adequacy.

Therefore an evaluation that observes only present linguistic prediction and present responsibility performance cannot, in general, certify prospective revision adequacy over this process class.

### Proof idea

Use the one-bit provenance construction. A compressed representation retaining only the current predictive/current decision state and an augmented representation retaining the provenance bit are indistinguishable on the registered present prediction and decision. After the retraction-like future event, only the augmented state can distinguish the required successor actions.

The proposition is an existence/no-certification result. It does not assert that any particular LLM uses either representation.

---

# 8. Representation Audit Profile

To make the practical consequence explicit, define four separately reported coordinates rather than one global “knowledge score”.

## 8.1 Linguistic predictive deficiency

For a proper predictive loss, or under log loss in the finite model,

\[
\Delta_{\mathrm{pred}}(Z)
=
H(Y^+\mid Z)-H(Y^+\mid H).
\]

Zero means the representation is sufficient for the declared linguistic future under this loss.

## 8.2 Current responsibility regret

For responsibility `r`, let

\[
\mathcal R_r(V)
=
\mathbb E\left[
\min_a\mathbb E[\ell(a,Q)\mid V]
\right].
\]

Define

\[
\delta_0(Z;r)
=
\mathcal R_r(Z)-\mathcal R_r(H).
\]

## 8.3 Prospective revision regret

For future evidence sequence `X_{1:k}` and the responsibility registered at the future decision point,

\[
\delta^{\mathrm{rev}}_k(Z;r)
=
\mathcal R_{r_{t+k}}(Z_t,X_{1:k})
-
\mathcal R_{r_{t+k}}(H_t,X_{1:k}).
\]

The definition should be evaluated under a frozen distribution/intervention schedule. A vector over evidence classes is preferable when errors are qualitatively different.

## 8.4 Representation cost

In the exact finite theorem layer, conditional entropy relative to `S_P` is the registered average-state coordinate. In actual neural systems, entropy of a hand-labelled quotient is usually unavailable. An empirical study must therefore register a representation-cost proxy—e.g. transmitted bits under a specified encoder, retained tokens, memory slots, or another operational capacity measure—rather than casually equating hidden dimension with information.

## 8.5 Audit profile

Write

\[
\boxed{
\operatorname{RAP}_k(Z;r)
=
\bigl(
\Delta_{\mathrm{pred}},
\delta_0,
\delta^{\mathrm{rev}}_k,
\operatorname{Cost}
\bigr).
}
\]

The coordinates are not compensatory. Better language prediction does not erase a future-revision failure, and a larger state does not by itself establish epistemic quality.

---

# 9. P0/P1/P2 as an audit taxonomy

The mechanically checked finite fixtures motivate three representation regimes.

## P0 — predictive-decisional

\[
C_{\mathrm{stat}}^*=0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The linguistic predictive state already suffices for current and future responsibility under the registered horizon.

## P1 — current cross-channel refinement

\[
C_{\mathrm{stat}}^*>0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

Additional history-side information is needed for the current responsibility, but no further dormant distinction is needed for future update.

## P2 — prospective refinement

\[
\Omega_{\mathrm{dyn}}>0.
\]

Even an optimally compressed current responsibility state lacks information needed for some registered later evidence-driven revision.

P2 can occur with zero or positive current cross-channel cost.

These are diagnostic regimes, not levels of intelligence.

---

# 10. Horizon-indexed prospective memory

For a finite registered future-evidence horizon `k`, let `\mathfrak P_k` be the states that are current-action compatible and remain compatible under every registered jointly feasible observation word of length at most `k`.

Define

\[
C_k^*
=
\min_{\Pi\in\mathfrak P_k}
H(\Pi(H)\mid S_P),
\]

and

\[
\Omega_k=C_k^*-C_0^*.
\]

Because the feasible state family becomes more constrained as the horizon increases,

\[
C_0^*\le C_1^*\le\cdots\le C_\infty^*.
\]

Finite registered systems stabilize. We denote the smallest stabilized horizon in a fixture by `K_epi`, but the term is purely an audit label; finite-state refinement and stabilization are classical.

The practical use is to ask **how far into the registered future a compressed representation remains sufficient**.

---

# 11. Three different sources of failure

The framework benefits from separating failures that are often all called “hallucination” or “memory error”.

Under log loss:

## 11.1 Acquisition deficit

\[
H(Q\mid H).
\]

The relevant information was not present in the accessible history. More internal computation cannot manufacture the missing evidence.

## 11.2 Current compression deficit

\[
I(Q;H\mid Z).
\]

The history contained useful information, but the representation discarded it for the current target.

## 11.3 Prospective revision deficit

\[
I(Q_{t+k};H_t\mid Z_t,X_{1:k}).
\]

The current representation discarded information that becomes useful after later observations.

These identities are standard information theory. Their value here is diagnostic routing:

- acquisition deficit -> obtain evidence;
- current compression deficit -> retain current responsibility information;
- prospective deficit -> preserve or deliberately re-acquire revision-relevant information.

---

# 12. Bounded responsibility families

No finite compressed state can promise sufficiency for every imaginable future query while also discarding arbitrary history distinctions.

For a registered exact responsibility signature `C_\mathcal R(H)`,

\[
0
\le
H(C_\mathcal R\mid S_P)
\le
H(H\mid S_P).
\]

If the responsibility family separates every positive-support history pair inside the predictive fibres, it recovers all non-predictive history information and reaches the upper bound.

The mechanical suite also confirms the elementary boundary that every non-injective finite representation admits some constructed exact binary responsibility on which it fails.

This is not a universal-memory novelty claim. It enforces a methodological rule:

> prospective sufficiency must always name the responsibility family and evidence horizon it promises to support.

---

# 13. Mechanical audit of the finite theory

The paper's formal ingredients were not left as prose.

## 13.1 Static layer

The partition audit exhaustively enumerated all set partitions through `n=7`, verifying Bell counts

\[
1,2,5,15,52,203,877.
\]

It verified the predictive-refinement and minimal-state structural checks used in the manuscript.

The responsibility-selector audit verified all registered exact semantics, including:

- minimum acceptable selector versus minimum compatible partition;
- ordering between permissive and stronger tie semantics;
- exact-target recovery as a special case;
- joint state sharing across multiple responsibilities;
- zero-cost common-optimal-action control.

## 13.2 Deficit layer

The acquisition/current-compression/prospective identities and five registered controls were checked over 900 seeded rational worlds with exact log-linear arithmetic and a high-precision decimal cross-check.

## 13.3 Dynamic layer

The direct dynamic-partition computation and selector-refinement computation agreed on the registered fixtures. The suite verified:

- non-negative `Omega_dyn`;
- the exact one-bit witness;
- P0/P1/P2 canonical fixtures;
- tie-sensitive selector behavior;
- horizon monotonicity and finite stabilization;
- responsibility-family monotonicity.

A mixed-P2 witness was not found in the registered search of 5,826 small machines and remains `CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS`; absence is not promoted to a theorem.

## 13.4 Universality and rate benchmarks

The registered finite universality checks passed. The log-loss benchmark reproduced the registered classical reveal/erasure family and also froze a counterexample preventing an over-broad converse outside that family.

## 13.5 Assumption mutations

Six mutations were executed against the exact predictive-compression layer.

Load-bearing failures were found when:

- entropy minimality was removed;
- arbitrary zero-mass nominal history labels were treated as constrained;
- near-minimal entropy was treated as if it guaranteed structural closeness.

The registered stochastic, cardinality-minimal and approximate variants retained narrower exact consequences.

## 13.6 Remaining mechanical gap

The theorem-location map currently supports 37 of 38 registered rows. `T8D_WORST_FIBRE_CARDINALITY` remains without a distinct mechanized check. It is not load-bearing for the prospective-audit thesis and should either be checked mechanically or removed from the main paper.

---

# 14. Prospective Revision Audit for autoregressive representations

The framework suggests a future experiment that does **not** require training a new language model.

The aim is not to prove that current LLMs “have beliefs”. It is to test whether their retained state supports a declared update responsibility.

## 14.1 Freeze a responsibility and evidence process

Each task should specify:

- initial source/evidence structure;
- current decision and loss;
- later evidence event classes;
- which conclusions should update and which should remain;
- full-history gold state;
- language-prediction/current-decision matching criteria.

A provenance/retraction family is especially useful because the dormant variable has a clear later role.

## 14.2 Establish present equivalence

Compare representations or memory conditions only after they are matched sufficiently on:

- linguistic prediction or a task-appropriate language surrogate;
- current answer/decision;
- current decision risk where relevant.

This guards against calling an ordinary current-performance deficit a prospective-memory effect.

## 14.3 Change only the retained state or memory contract

Possible interventions include:

- hidden-state compression;
- context truncation;
- typed-memory ablation;
- distilled/summarized context;
- selective removal of source/provenance identity;
- controlled retained-bit synthetic encodings.

The intervention identity should be frozen before the later evidence is revealed.

## 14.4 Deliver future evidence

Give a later observation that discriminates histories previously equivalent for the current decision—for example a retraction bound to one source but not another.

Measure both:

- **update accuracy** when revision is required;
- **retain accuracy** when independent support means no revision is required.

The retain control is necessary because a system that changes every answer after every new observation has not demonstrated revision competence.

## 14.5 Compare with ordinary belief-revision evaluation

Belief-R is an important parent baseline because it already tests update-versus-maintain behavior after new premises.

The new audit adds a causal representation question:

> after present behavior has been matched, does manipulating what historical information the representation retains selectively change later revision?

A positive result would demonstrate a representation-retention mechanism. A null would show that the proposed cross-channel variable was unnecessary, recoverable elsewhere, or not used by the model.

No such experiment is claimed in this paper unless it is actually run.

---

# 15. Why this matters for LLM design without claiming a new architecture

If a future audit finds P2-like failures in real models or memory systems, several design responses become testable:

- preserve typed provenance/dependence state in an internal or external memory;
- train an auxiliary objective on later revision rather than only current prediction;
- use selective external memory for dormant cross-channel variables;
- retain recoverable source/evidence identifiers through compression/distillation;
- dynamically increase state only for responsibility families/horizons that require it.

Conversely, a P0 result says no extra machinery is needed for that responsibility. This negative case is just as important: Machine Epistemics should not become a reason to retain metadata that does not change any protected decision.

The framework therefore proposes an **evaluation before architecture** principle.

---

# 16. Strongest-parent reconstruction

A hostile reviewer can reconstruct most of the mathematical substrate from existing work:

```text
causal states / PSRs
    -> linguistic predictive reference state

Brodu / Blackwell / R-PSR / retentive complexity
    -> current decision-relevant compression

POMDP / information state / AIS
+ incomplete-FSM closed cover / right congruence
+ 2026 stable quotient Markovization
    -> recursively updateable decision state

value equivalence / rate distortion
    -> capacity versus decision quality

Belief-R
    -> LLM revision-after-evidence evaluation
```

This is why the paper no longer claims C09/C10 as new state-minimization theorems.

The remaining proposed contribution is the **reference-channel decomposition and prospective representation audit**:

\[
\text{linguistic prediction}
\rightarrow
\text{current responsibility}
\rightarrow
\text{future revision}.
\]

We found no direct parent in the final audit that uses this exact three-stage matched evaluation to distinguish representation retention in autoregressive systems. This is a synthesis claim, not proof of broad mathematical originality.

---

# 17. Relation to Machine Epistemics

The broader Machine Epistemics programme asks how machine systems should represent, test, revise and preserve warranted commitments. This paper studies only one narrow internal-state question from that programme.

It does not formalize scientific authority, institutional permission, full evidence provenance, conceptual change, or experiment selection. Nor does it claim a replacement for transformers.

Its contribution, if it survives review, is simpler:

> **a machine representation should not be called adequate for a declared revision responsibility merely because it predicts language and makes the right decision now.**

Prospective adequacy is a separately testable property.

---

# 18. Limitations

1. **Finite exact foundation.** The strongest checked statements are finite/discrete. Neural hidden states are continuous and high-dimensional.
2. **Reference-state idealization.** The exact minimal complete-future linguistic state is not generally computable for a real LLM. It is a theoretical reference, not a claim about transformer activations.
3. **Responsibility is externally registered.** The framework does not solve which responsibilities society or a scientific institution should require.
4. **State-cost proxy in real models is open.** Conditional entropy is exact in finite fixtures; neural capacity requires an operational proxy.
5. **Parent pressure is severe.** The minimization substrate is largely owned by causal-state, decision-state, information-state, FSM, and RL abstraction theory.
6. **No empirical LLM claim.** We have not demonstrated a P2-like hidden-state failure in a deployed model.
7. **Belief revision already has benchmarks.** The proposed audit must be evaluated against Belief-R and later revision benchmarks, not presented as the first test of updating after evidence.
8. **A later evidence event can add genuinely new information.** The audit only attributes failure to retention when the full prior history plus future evidence suffices and the compressed representation plus future evidence does not.
9. **No universal memory prescription.** Unbounded responsibility families trivially push toward retaining all history; practical systems need bounded responsibility/horizon contracts.

---

# 19. Publication gate

JMLR explicitly accepts theoretical studies, formalizations of new learning tasks and performance-assessment methods, and new analytical frameworks when they advance understanding of practical learning systems. Its reviewer guidance also requires theoretical practical utility and sufficient difference from prior work.

Accordingly, this manuscript has only one plausible JMLR route:

> **formal assessment task / analytical framework**, not new generic state-minimization theorem.

JMLR submission should remain unauthorized until:

- final theorem-level parent locations are bound;
- the remaining T8D item is checked or deleted;
- the prospective representation audit is presented as the primary contribution throughout;
- no paragraph implies observed LLM hidden-state failure;
- a hostile editor judges the three-stage audit sufficiently distinct and useful relative to Belief-R, information-state theory, and current decision-aware memory work.

If that distinctness fails, the work should route to TMLR/a focused theory venue or merge into the broader Machine Epistemics flagship rather than exaggerating novelty.

---

# 20. Conclusion

Prediction, present decision, and future revision are different representation obligations.

Existing theory already explains much of how to compress history for prediction or decision and how to construct recursively updateable state. The useful residual here is not another generic state ontology. It is a way to **audit an autoregressive representation against three separately registered requirements**.

The exact finite witness proves why the distinction matters: two systems can be indistinguishable on complete linguistic prediction and the current responsibility while differing by one bit of information that becomes decisive after later evidence. This makes prospective revision adequacy impossible to certify from present performance alone.

For language-model research, that yields a concrete question:

> **after current language and decision behavior are matched, does the retained representation preserve the dormant information needed for the right update when evidence changes?**

That question can be tested without claiming consciousness, a human-like belief state, or a new neural architecture. It is the narrow Machine-Epistemic claim this paper can defend after strongest-parent subtraction.

---

# Reference anchors for final bibliography

The final bibliography should bind exact metadata for at least:

- Shalizi & Crutchfield / computational mechanics and causal states.
- Littman/Sutton/Singh and later Predictive State Representation work.
- Brodu (2011), decisional states, DOI `10.1142/S0219525911003347`.
- Baisero & Amato (2021), R-PSR, DOI `10.24963/ijcai.2021/299`.
- Subramanian et al. (2022), Approximate Information State, JMLR 23(12):1–83.
- Grimm et al. (2020), Value Equivalence.
- Grimm et al. (2021), Proper Value Equivalence.
- Arumugam & Van Roy (2022), Value-Equivalent Sampling, NeurIPS 35.
- Arumugam & Singh (2022), Planning to the Information Horizon of BAMDPs via Epistemic State Abstraction, NeurIPS 35.
- classical ISFSM minimization / closed-cover sources.
- Zhang, Chen, Imani & Lan (2026), *Minimal Markovization via Stable Quotients in Holonomy-Cover Decision Processes*, arXiv:2607.27132.
- *History, Hypergraphs, and Memory: The Exact Complexity of Deviation-Rational Control*, public double-blind RLC 2026 manuscript, OpenReview `oNLGDwZo5d`, with publication status clearly qualified.
- Wilie et al. (2024), *Belief Revision: The Adaptability of Large Language Models Reasoning*, EMNLP.
- current LLM hidden-state belief/truth/uncertainty literature already catalogued by the ORION-V2 lane.
- current decision-aware/bounded-memory LLM-agent work as practical neighbors, not theorem parents.
