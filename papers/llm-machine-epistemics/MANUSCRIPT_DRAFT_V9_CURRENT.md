# Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations

**Integrated current manuscript V9**  
**Issue:** #51  
**Supersedes for scientific/editorial use:** V1–V8 manuscript drafts plus the V8 correction register, except as provenance.  
**Bibliography:** `REFERENCES_V1.bib` + `REFERENCES_CLASSICS_SUPPLEMENT_V1.bib`  
**Status:** all currently identified non-computational scientific corrections are integrated. Remaining work is target-format conversion, receipt-derived displays, bibliography-status refresh, human authorship/ownership gates, and external editorial judgment.  
**Empirical claim about current LLM hidden states:** none.

---

## Abstract

Autoregressive models are optimized for language prediction but are increasingly expected to revise decisions when evidence, sources, or assumptions change. Existing theory already provides predictive and decisional states, information states, value-aware compression, and recursively updateable memory; recent LLM work also studies belief revision and context compression. We therefore formalize a narrower representation-assessment problem. Relative to a registered linguistic prediction protocol, we distinguish predictive adequacy, current responsibility-decision adequacy, and prospective evidence-triggered revision adequacy under a distinct later intervention. A mechanically verified finite construction has zero extra state for the current decision but requires one additional bit for correct later revision. Thus matched current prediction and decision do not, in general, certify prospective revision capability. We use this separation to specify a Prospective Revision Audit with equivalence margins, update/maintain controls, representation interventions, alternate-channel and parametric-reconstruction checks, and complete future-action compatibility tests. The contribution is an analytical assessment framework, not a claim that current language models necessarily discard revision-relevant information.

---

# 1. Introduction

A model can give the right answer today and still be in the wrong internal state for tomorrow.

Consider two histories evaluated under the same registered language-prediction protocol. They induce the same declared linguistic prediction target and the same present responsibility decision. In one history a conclusion is supported through source `A`; in the other it is supported through source `B`. If source identity is irrelevant to the current linguistic target and current action, a compressed representation can merge the histories without any visible present loss. Later, however, the same evidence event—say, `RETRACT(A)`—may require reopening the first conclusion and retaining the second. If the representation discarded the support-source distinction and the later evidence does not reconstruct it, current adequacy has not guaranteed correct revision.

The ingredients of this story are largely classical. Computational mechanics and Predictive State Representations formalize future-sufficient state \citep{shalizi2001computational,littman2001predictive}. Brodu's decisional states and statistical decision theory formalize utility-relative decision state \citep{brodu2011decisional,blackwell1953equivalent}. Reward-Predictive State Representations show that a state sufficient for one prediction target can omit another decision target \citep{baisero2021reconciling}. POMDP belief states and Approximate Information State theory formalize recursively useful history statistics for future control \citep{smallwood1973optimal,subramanian2022approximate}. Incompletely specified finite-state-machine reduction and recent stable-quotient work provide close parent mechanisms for compatible recurrent state and minimal Markovization \citep{paull1959minimizing,zhang2026minimal}. Information Bottleneck and value-equivalent model abstractions address task- or decision-relevant compression \citep{tishby1999information,strouse2017deterministic,grimm2020value,grimm2021proper,arumugam2022deciding}. Belief-R already evaluates whether LLM conclusions should update or remain after new evidence \citep{wilie2024belief}, and recent LLM-agent work studies context compression, bounded memory, prospective intentions, and decision-aware state selection \citep{kontonis2026memento,liu2026pmbench,guan2026decision,cheng2026agenticsts}.

These parents rule out a broad novelty claim. We do **not** propose a new generic predictive state, decisional state, information state, memory-minimization algorithm, or belief-revision benchmark.

The narrower question is:

> **After representations have already been matched on a registered linguistic prediction target and the registered current responsibility decision, can a distinct later evidence intervention expose a revision failure caused by historical information that one representation failed to retain?**

This is a question of **prospective revision adequacy**.

## 1.1 Contributions after strongest-parent subtraction

The paper makes four bounded contributions.

**A three-axis representation assessment.** We separately register linguistic predictive adequacy under a reference protocol, current responsibility-decision adequacy, and prospective revision adequacy after a distinct evidence process.

**A finite no-certification result.** We construct and mechanically verify a process in which two representations are equally adequate for the registered linguistic target and the same unique present action, yet differ after identical later evidence because only one retains a one-bit provenance distinction. Therefore current prediction and current decision do not, in general, certify later revision.

**Relative audit coordinates.** We account for state required beyond the registered linguistic predictive reference for the current responsibility and separately for future updateability. Their difference, the dynamic optionality premium, is a derived audit coordinate over parent-owned state constructions rather than a new information law.

**A Prospective Revision Audit.** Protocol V3 freezes prediction/intervention scope, present-equivalence margins, update and maintain controls, representation interventions, alternate-channel and parametric-reconstruction checks, complete one-step future-action compatibility, and symmetric negative/`CANNOT_CHECK` terminals. It can be executed with a frozen model or agent memory without training a new LLM.

---

# 2. Claim ceiling from prior theory

## 2.1 Predictive state is relative to a registered channel

Let `H` be a finite current history. Let `rho` denote the registered reference input protocol for the language-prediction task and `Y^+_rho` the complete declared linguistic continuation under that protocol. Define

\[
h\sim_{P,\rho} h'
\iff
P(Y^+_\rho\mid H=h)
=
P(Y^+_\rho\mid H=h').
\]

Let

\[
S_{P,\rho}=[H]_{\sim_{P,\rho}}.
\]

Causal-state theory and PSRs own the underlying predictive-state idea \citep{shalizi2001computational,littman2001predictive}. We use `S_{P,rho}` as a reference channel only. Once `rho` is fixed, we abbreviate it by `S_P` when no ambiguity arises.

The scope matters. The later evidence intervention studied below is **not** silently included in `rho` unless the protocol explicitly says so. If the reference state is instead required to be sufficient for the joint controlled future across the registered evidence-intervention family, the dormant provenance distinction may already become state-relevant. That stronger controlled state is a parent control, not a contradiction.

## 2.2 Decision state is parent-owned

A current decision may require less or different information than full prediction. Brodu's decisional-state framework groups predictive states according to utility/payoff and preferred decision \citep{brodu2011decisional}. Blackwell-style decision theory more generally formalizes comparative informativeness and Bayes risk \citep{blackwell1953equivalent}.

Conversely, a state sufficient for one target can omit another. R-PSR shows that an observation-predictive state need not represent rewards \citep{baisero2021reconciling}. Thus

\[
\text{prediction sufficiency}
\not\Rightarrow
\text{arbitrary secondary-decision sufficiency}
\]

is background rather than our novelty claim.

## 2.3 Recursive state is parent-owned

Approximate Information State theory defines history compression adequate for current performance and for predicting/evolving the next compressed state \citep{subramanian2022approximate}. Classical POMDP belief-state control already provides a sufficient information state for partially observed control \citep{smallwood1973optimal}. Incompletely specified FSM reduction studies compatible outputs with successor-closure constraints \citep{paull1959minimizing}; recent stable-quotient work provides a particularly close coarsest exact recursively updateable abstraction and minimal state result in a structured partially observed process \citep{zhang2026minimal}. A current public double-blind manuscript also studies finite memory required for acceptable continuation behavior \citep{anonymous2026history}.

We therefore use recurrent-state minimization as inherited machinery. We claim no new right-congruence or minimal-memory algorithm.

## 2.4 Decision-aware compression is parent-owned

Information Bottleneck and deterministic variants formalize target-relevant compression \citep{tishby1999information,strouse2017deterministic}. Value Equivalence, Proper Value Equivalence, and Value-Equivalent Sampling formalize decision-relevant model abstraction and capacity/decision tradeoffs \citep{grimm2020value,grimm2021proper,arumugam2022deciding}. Bayes-adaptive work already uses the term *epistemic state abstraction* and an information-horizon concept \citep{arumugam2022information}. The generic principle that representation capacity should preserve task-relevant information is therefore established.

## 2.5 Revision and LLM memory are active prior art

Iterated belief revision already studies state representations retaining information beyond present beliefs \citep{liberatore2024representing}. Belief-R evaluates LLM update versus maintain behavior after new evidence \citep{wilie2024belief}. Standards for LLM belief representation emphasize functional use rather than decodability alone \citep{herrmann2025standards}; current mechanistic work finds causally useful belief-like signals \citep{mendozza2026beliefs}, while other work cautions that hidden-state self-knowledge can reflect recall rather than truthfulness \citep{cheang2026know}. Representation-identifiability theory also warns that matched predictor behavior does not determine arbitrary internal representation properties \citep{sevetlidis2026fiber}.

Recent practical memory work makes the boundary tighter still. MEMENTO learns compact internal reasoning state and shows that nominally evicted content can persist through another KV-state channel \citep{kontonis2026memento}. PM-Bench evaluates prospective memory for delayed intentions \citep{liu2026pmbench}. Lossy LLM hand-off state can harm downstream exact decisions \citep{sharma2026state}; Router-Mem asks whether current memory/evidence suffices or deeper retrieval is needed \citep{lin2026stop}; decision-aware and bounded-memory architectures are also active research objects \citep{guan2026decision,cheng2026agenticsts}. Evidence-informed persistent LLM beliefs and selected/omitted-evidence updating are likewise current topics \citep{agarwal2026evidence,deng2026selected}.

Accordingly, this paper does not claim novelty for belief revision, memory compression, future-intention memory, decision-aware memory, or downstream failure from compressed state.

---

# 3. Responsibility contracts

A responsibility is an operational contract

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where `Q` is an externally or mechanically specified target, `A` a finite action/terminal set, `ell(a,q)` a registered loss, and `sigma` the exact decision semantics.

We distinguish:

- `ANY_OPTIMAL_ACTION`;
- `CANONICAL_ACTION`;
- `OPTIMAL_ACTION_SET`;
- `ACTION_AND_RISK`;
- `EXACT_TARGET`.

For history `h`, let

\[
A^*(h)=\arg\min_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

Under `ANY_OPTIMAL_ACTION`, any selector `d(h) in A^*(h)` is acceptable. This prevents overestimating required state under ties: histories with acceptable sets `{a,b}` and `{b,c}` can share one decision state by selecting `b`.

The responsibility must concern the status or management of a claim, model, evidence relation, scope, support relation, identifiability condition, or revision obligation. An arbitrary auxiliary label does not become “epistemic” by notation. Institutional authority remains external.

---

# 4. Present responsibility adequacy

Let `D` be the set of acceptable Bayes-optimal selectors. Define the registered current conditional state cost

\[
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}
H(d(H)\mid S_{P,\rho}).
\]

Equivalently, histories may be merged only within an `S_{P,rho}` fibre and only when their acceptable-action sets have a common member. The selector/partition equivalence is proved in the proof appendix and mechanically verified in the static audit.

This quantity is an accounting coordinate, not a new decision-complexity theorem; its interpretation is explicitly placed against Brodu/Blackwell-style parents \citep{brodu2011decisional,blackwell1953equivalent}.

## 4.1 P0 current control

\[
C_{\mathrm{stat}}^*=0
\]

iff some acceptable present policy factors through `S_{P,rho}`. This is the mandatory no-extra-state control.

## 4.2 Positive current cross-channel cost

\[
C_{\mathrm{stat}}^*>0
\]

means no acceptable current responsibility policy can be implemented from the registered linguistic predictive state alone. At least one distinction inside a predictive fibre matters to the current responsibility.

“Cross-channel” means only “not measurable from the declared predictive quotient under `rho`.” It does not imply statistical independence or a physically distinct substrate.

---

# 5. Prospective revision adequacy

Let `x` be a registered later evidence event from a distinct intervention family and `delta(h,x)` the corresponding successor history when defined. A state adequate for a present action may fail to evolve into the correct future action.

A dynamic-admissible state must satisfy:

1. present action compatibility;
2. successor compatibility under every registered feasible evidence event.

Let `P_dyn` denote the resulting finite partitions and define

\[
C_{\mathrm{dyn}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_{P,\rho}).
\]

Equivalently, in the registered finite deterministic setting,

\[
C_{\mathrm{dyn}}^*
=
\min_{d\in\mathcal D}
H(S_\infty^d\mid S_{P,\rho}),
\]

where `S_inf^d` is the stable right-congruent refinement of `(S_{P,rho},d)`. The equivalence is proved in the appendix and mechanically verified by independent direct and selector-based calculations.

The construction is a specialization of parent recurrent-state theory \citep{paull1959minimizing,subramanian2022approximate,zhang2026minimal}; the paper uses it only to define a relative assessment coordinate.

---

# 6. Dynamic optionality premium

Define

\[
\boxed{
\Omega_{\mathrm{dyn}}
=C_{\mathrm{dyn}}^*-C_{\mathrm{stat}}^*
}.
\]

Because every dynamic-admissible state is also static-admissible,

\[
\Omega_{\mathrm{dyn}}\ge0.
\]

Interpretation:

> `Omega_dyn` is the additional retained state required solely because an acceptable current responsibility policy must remain correct under the registered future evidence process.

It is a derived metric over parent-owned state classes, not a new information law.

---

# 7. One-bit prospective witness

Let two equiprobable histories `h_A,h_B` share the same registered linguistic predictive state `S_{P,rho}` and the same unique current action `RETAIN`. They differ only in a one-bit provenance variable: the current conclusion is supported through source `A` or source `B`. Under the reference prediction protocol `rho`, that provenance bit does not change the declared language target.

Now provide the same controlled later event

\[
x=\mathrm{RETRACT}(A).
\]

At the successor histories require

\[
h_A'\to\mathrm{REOPEN},
\qquad
h_B'\to\mathrm{RETAIN}.
\]

The two current histories may share one present responsibility state, so

\[
C_{\mathrm{stat}}^*=0.
\]

A recursively adequate state must nevertheless distinguish them before the event: the same compressed state plus the same evidence cannot deterministically yield incompatible successor actions. With equal prior,

\[
C_{\mathrm{dyn}}^*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit}.
\]

The current action is unique, so the result is not a tie-selection artifact. Exact mechanical execution reproduces these values.

A stronger control that explicitly requires the reference state to model the joint controlled future including the retraction family may retain provenance already and shrink the premium. That is expected: the result is relative to the registered prediction and intervention tasks.

---

# 8. No-certification theorem

## Theorem 1 — registered-channel prospective no-certification

For some finite registered reference protocol `rho`, current responsibility `r_0`, future evidence event `x`, and future responsibility `r_1`, there exist two representations `Z_c,Z_a` such that:

1. `Z_c` and `Z_a` are equally adequate for the declared linguistic prediction target `Y^+_rho`;
2. they support the same zero-regret current responsibility decision;
3. after the same future evidence event `x`, their achievable future responsibility risks differ.

Therefore an evaluation observing only adequacy for the registered current linguistic target and current responsibility cannot, in general, certify prospective revision adequacy under a distinct later evidence process.

### Proof sketch

Let

\[
Z_c=S_{P,\rho},
\qquad
Z_a=(S_{P,\rho},B),
\]

where `B` is the provenance bit from Section 7. By construction, `B` changes neither `Y^+_rho` nor the unique present action. After `RETRACT(A)`, the augmented representation can distinguish the successor decisions, while the compressed representation cannot if the later evidence does not itself reconstruct `B`. The complete finite proof appears in `PROOF_APPENDIX_V1.md`. ∎

The theorem is an existence/non-certification result. It does not establish that a state sufficient for all possible controlled future interventions can forget intervention-relevant information, and it does not establish that real LLMs frequently exhibit this failure.

---

# 9. Complete one-step future compatibility

A pairwise revision collision is a useful failure witness but is not a complete compatibility test under ties.

For representation value `z` and common evidence event `x`, define the registered cell

\[
\mathcal C(z,x)
=
\{h:Z(h)=z,\delta(h,x)\text{ defined}\}
\]

and its joint acceptable future-action intersection

\[
\boxed{
\mathcal I(z,x)
=
\bigcap_{h\in\mathcal C(z,x)}A_x^*(h).
}
\]

Under exact one-step `ANY_OPTIMAL_ACTION` semantics, one deterministic future rule using only `(z,x)` is acceptable for every history in the cell iff

\[
\mathcal I(z,x)\neq\varnothing.
\]

Necessity follows because one output action must be acceptable for every history in the cell; sufficiency follows by choosing any action in the intersection.

A disjoint pair is therefore an easy positive insufficiency certificate. But absence of a pairwise collision is not sufficient in general. For example,

```text
A1={a,b}
A2={b,c}
A3={a,c}
```

has nonempty pairwise intersections but empty three-way intersection. The canonical one-bit witness has singleton future-action sets `{REOPEN}` and `{RETAIN}`, so its pairwise collision is complete.

The criterion is ordinary decision-sufficiency/intersection logic; the contribution is its use as an audit diagnostic, not a new mathematical theorem \citep{blackwell1953equivalent}.

For a multi-step evidence horizon, one-step compatibility is insufficient; the recurrent/right-congruent state analysis remains the appropriate finite parent mechanism.

---

# 10. P0/P1/P2 audit taxonomy

The finite coordinates define three diagnostic regimes.

## P0 — predictive-decisional

\[
C_{\mathrm{stat}}^*=0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The registered linguistic predictive state supports both the current responsibility and the registered future revision process. Extra state is unnecessary.

## P1 — current cross-channel refinement

\[
C_{\mathrm{stat}}^*>0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

Additional history-side state is needed for the current responsibility, but once retained, no further future-only refinement is required.

## P2 — prospective refinement

\[
\Omega_{\mathrm{dyn}}>0.
\]

The present-adequate state omits information needed only after later evidence.

Acquisition/non-identifiability sits outside this taxonomy. A stronger controlled reference target can also legitimately move a former P2 case toward P0/P1. These are representation-audit classes, not stages of intelligence.

---

# 11. Horizon-indexed audit

For horizon `k`, let `P_k` contain present-compatible states that remain compatible under every registered future evidence sequence of length at most `k`. Define

\[
C_k^*
=
\min_{\Pi\in\mathfrak P_k}
H(\Pi(H)\mid S_{P,\rho}),
\qquad
\Omega_k=C_k^*-C_0^*.
\]

Nested feasible sets imply

\[
C_0^*\le C_1^*\le\cdots.
\]

Finite registered systems stabilize after finitely many refinements. These are supporting finite-state facts rather than novelty claims \citep{paull1959minimizing,subramanian2022approximate,zhang2026minimal}. Their audit interpretation asks how far into the registered evidence process the retained representation remains adequate.

---

# 12. Representation Audit Profile

Report four separate coordinates:

\[
\boxed{
\operatorname{RAP}_k(Z;r)
=
(\Delta_{\mathrm{pred}},\delta_0,\delta^{\mathrm{rev}}_k,\operatorname{Cost})
}.
\]

In the finite log-loss reference,

\[
\Delta_{\mathrm{pred}}(Z)
=
H(Y^+_\rho\mid Z)-H(Y^+_\rho\mid H).
\]

Current responsibility regret is

\[
\delta_0(Z;r)
=
\mathcal R_r(Z)-\mathcal R_r(H),
\]

and future revision regret is

\[
\delta^{\mathrm{rev}}_k(Z;r)
=
\mathcal R_{r_{t+k}}(Z_t,X_{1:k})
-
\mathcal R_{r_{t+k}}(H_t,X_{1:k}).
\]

In actual neural systems, `Cost` must be an operational capacity proxy—retained tokens, serialized bytes, transmitted bits under a fixed encoder, memory slots, or another registered state budget. Hidden dimension alone is not an information measure.

The coordinates are non-compensatory: better language prediction does not cancel a revision failure.

---

# 13. Acquisition, compression, prospective loss, and reconstruction

Under log loss, distinguish:

\[
H(Q\mid H)
\]

for information absent from accessible current history;

\[
I(Q;H\mid Z)
\]

for useful current information lost by representation compression; and

\[
I(Q_{t+k};H_t\mid Z_t,X_{1:k})
\]

for current historical information that becomes useful only after future evidence.

The identities are standard information theory \citep{courtade2014multiterminal}. Their role is diagnostic routing:

- acquisition failure -> obtain evidence;
- current compression failure -> retain current decision information;
- prospective loss -> preserve or deliberately re-acquire revision-relevant information.

Two reconstruction routes must be separated from retention:

1. the later evidence itself reveals the dormant variable;
2. fixed model parameters/parametric knowledge plus observed content allow the system to infer it.

Success through either route is not evidence that the variable was retained in episode state.

---

# 14. Prospective Revision Audit V3

The canonical protocol is `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V3.md`.

Every audit freezes separately:

```text
prediction_reference_protocol rho
present_linguistic_target
current_responsibility
future_evidence_intervention_family
future_responsibility
```

A valid suite includes acquisition controls, P0, P1, P2, and a stronger controlled-target condition that explicitly includes the intervention family.

## 14.1 Present-equivalence gate

Future revision comparisons are interpretable only after present equivalence is established within prospectively frozen margins on:

- registered linguistic prediction metric under `rho`;
- current action/terminal;
- current responsibility risk/calibration if registered;
- resource/tool access;
- current inference budget apart from the state-size intervention.

For noisy empirical metrics, do **not** treat `p>0.05` as evidence of equivalence. Freeze equivalence margins and require an equivalence-test/interval rule that supports equivalence within those margins.

## 14.2 Representation intervention

Compare, where feasible:

- full-history reference;
- prediction-preserving targeted compression;
- current-decision-sufficient state;
- prospective-augmented state;
- stronger controlled-future state.

The load-bearing P2 contrast compares current-decision-sufficient and prospective-augmented states after present equivalence has passed.

## 14.3 Alternate-channel and parametric reconstruction gate

A claimed state-removal intervention is invalid if the supposedly removed variable survives in another accessible channel:

- prompt/context;
- KV cache;
- hidden activations;
- summary embeddings;
- retrieval keys;
- tool/session state;
- external memory.

MEMENTO makes this concern practical rather than hypothetical: nominally evicted reasoning can persist through another internal channel \citep{kontonis2026memento}.

Model parameters are also registered side information. Fixed parameters cannot know a randomized episode-local assignment that never enters the model, but they can reconstruct public facts or infer missing variables from content. Where the scientific question is episode-state retention, use randomized/nonce identities when semantically valid; otherwise report parametric reconstruction as part of the system.

Terminals include:

- `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION`;
- `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`;
- `PARAMETRIC_RECONSTRUCTION_EXPLAINS_SUCCESS`;
- `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`.

## 14.4 Update and maintain/selective reopening

Score both correct updating and correct maintaining. If dependency structure is registered, score selective reopening: only commitments dependent on defeated support should change.

This prevents indiscriminate updating from appearing epistemically successful.

## 14.5 Complete one-step compatibility

For exact tied-action cases, use the joint intersection `I(z,x)`, not pairwise collisions alone. Report incompatible representation/evidence cell rate as the primary exact one-step structural diagnostic; pairwise disjoint collisions are secondary easy witnesses.

## 14.6 Deterministic versus stochastic systems

The core finite theory uses deterministic zero-regret decisions. For stochastic decoding, freeze temperature/top-p, seed policy, samples per episode, aggregation rule, and expected/worst-case regret estimand. Repeated draws from one episode do not create independent scientific cases.

A zero-regret randomized policy for a merged cell still requires its support to lie in every acceptable-action set, so the joint intersection must be nonempty. Under approximate regret, randomized mixtures can trade loss across histories; use the registered decision loss rather than an exact collision terminal.

---

# 15. Direct LLM revision/memory baselines

**Belief-R** already evaluates update versus maintain after new evidence \citep{wilie2024belief}. Our audit adds matched current prediction/current decision plus a representation-retention intervention before common later evidence.

**MEMENTO** learns compact internal reasoning state and shows hidden alternate retention routes \citep{kontonis2026memento}. Our audit uses this as a causal-removal control, not a memory-method novelty claim.

**PM-Bench** evaluates future-intention memory \citep{liu2026pmbench}; our task is revision of a current responsibility decision, not delayed intention execution.

**State Compression in Two-Agent LLM Relays** shows generic downstream failures after compressed hand-off \citep{sharma2026state}; our contrast first matches current behavior and then introduces common later evidence.

**Router-Mem** evaluates current evidence/memory sufficiency \citep{lin2026stop}; the P2 case is adequate now and fails only later.

**Decision-Aware Memory Cards** and **AgenticSTS** make decision-aware and bounded-memory systems direct practical controls \citep{guan2026decision,cheng2026agenticsts}. Evidence-informed and selected-evidence updating work likewise supplies direct parent context \citep{agarwal2026evidence,deng2026selected}.

The registered residual is therefore not belief revision, memory compression, or decision-aware memory in isolation. It is:

```text
registered current prediction target
+ registered current decision
+ present-equivalence gate
+ representation retention intervention
+ alternate-channel/parametric reconstruction gate
+ identical later evidence
+ joint future compatibility
+ update and maintain/selective-reopening scoring
```

No universal first-work claim is made.

---

# 16. Mechanical validation

Four merged mechanical batches support the finite theory.

**Static audit.** All set partitions through `n=7` were exhaustively enumerated with Bell counts `1,2,5,15,52,203,877`. Predictive structural checks, decision semantics, tie behavior, selector/partition equivalence, joint state sharing, and zero-cost controls passed.

**Information-deficit audit.** Acquisition/current/prospective identities and controls were tested over 900 seeded rational worlds using exact log-linear arithmetic and high-precision cross-checks.

**Dynamic audit.** Direct dynamic-partition and selector-refinement calculations agreed on the registered fixtures. Non-negative optionality, the one-bit witness, P0/P1/P2, horizon stabilization, responsibility-family monotonicity, and bounded/universality checks passed.

**Mutation audit.** Removing entropy minimality, relaxing support treatment, and assuming structural stability from near-minimal entropy exposed counterexamples; narrower registered variants survived where stated.

A search of 5,826 small machines found no mixed-P2 witness and remains `CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS`.

The three-history joint-intersection control added after these batches has an elementary proof but not yet a separate mechanical receipt. It is not novelty-bearing and must remain labeled as such until a checker is run.

---

# 17. Limitations and claim ceilings

1. Core exact results are finite/discrete.
2. `S_{P,rho}` is a theoretical reference; real-model studies need a frozen prediction surrogate.
3. The theorem is relative to a registered prediction channel and a distinct later intervention. It does not concern a state sufficient for every possible controlled future.
4. Responsibilities are externally specified; the framework does not decide which responsibilities institutions should require.
5. Real-model state cost is intervention-dependent and cannot be read off from hidden dimension.
6. State-minimization mathematics is heavily parent-owned \citep{shalizi2001computational,brodu2011decisional,subramanian2022approximate,zhang2026minimal}.
7. Belief revision, decision-aware memory, prospective memory, and context compression all have active direct prior art \citep{wilie2024belief,kontonis2026memento,liu2026pmbench,guan2026decision,cheng2026agenticsts}.
8. No real-LLM P2 failure is demonstrated.
9. Visible deletion can be invalidated by alternate retained channels \citep{kontonis2026memento}.
10. Fixed parameters or later evidence can reconstruct a dormant variable; reconstruction must be separated from retention.
11. Absence of a pairwise collision does not establish one-step compatibility under tied actions; use the full joint action intersection.
12. For approximate/stochastic decisions, use registered regret rather than exact zero-regret compatibility mechanically.
13. Unbounded responsibility families force increasing history retention, so every sufficiency claim is bounded by target and horizon.

---

# 18. Publication positioning

The strongest-parent reconstruction makes the paper unsuitable as a new generic state theory.

The JMLR route is defensible only as a formal assessment-task/analytical-framework contribution. Internal hostile review rates this as borderline/high risk because an editor may regard the framework as a careful application of information-state theory plus belief-revision and memory-ablation ideas. TMLR is an editorially stronger fallback under soundness/audience-interest criteria, but current TMLR AI-use policy creates a separate human intellectual-ownership/policy-fit gate because this project used LLMs extensively for scientific assistance.

No venue route permits inflation of parent-owned mathematics or concealment of AI assistance.

---

# 19. Conclusion

Prediction, present decision, and future revision are distinct representation obligations—but only relative to declared tasks and input channels.

Existing theory already explains how to compress history for prediction or decision and how to construct recursively updateable state \citep{shalizi2001computational,brodu2011decisional,subramanian2022approximate,zhang2026minimal}. Recent LLM research already studies belief revision, context compression, decision-aware memory, bounded memory, and prospective intentions \citep{wilie2024belief,kontonis2026memento,guan2026decision,cheng2026agenticsts,liu2026pmbench}.

The surviving contribution is narrower: a way to **audit a representation only after current prediction and current decision behavior have been matched under a registered reference protocol**, then ask whether the same later evidence exposes a dormant distinction that the representation failed to retain or reconstruct.

The one-bit construction proves why the third test cannot be inferred from the first two. The complete one-step compatibility criterion shows how to diagnose failure even when future actions admit ties. Protocol V3 then adds the controls required for real systems: equivalence margins, alternate-channel retention, parametric reconstruction, common later evidence, and update/maintain/selective-reopening evaluation.

For language-model and agent research, the resulting question is concrete:

> **After current prediction and decision behavior are matched, has the retained representation preserved—or made reliably reconstructable—the information needed for the right revision when evidence changes?**

That question can be tested with frozen models, external memories, context compression, retrieval state, KV/hidden-state interventions, or synthetic representations without claiming consciousness, human-like belief, or a new neural architecture.

---

# Submission note

Load-bearing parent concessions are bound by `CITATION_COVERAGE_MATRIX_V1.md`. Reviewer-facing summaries are in `REVIEWER_TABLES_V1.md`. Mechanical assembly should use `SUBMISSION_FRONTMATTER_V2.md`, `CLAIM_LEDGER_V6.json`, `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V3.md`, and the current submission manifest. Preprints, working papers, and public double-blind manuscripts require status refresh immediately before filing.
