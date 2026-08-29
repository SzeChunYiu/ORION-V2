# Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations

**Final research manuscript draft V7**  
**Issue:** #51  
**Status:** scientific framing, proofs, strongest-parent reconstruction, direct-neighbor saturation, and assessment design complete. Remaining work is citation serialization, generated displays, target-format conversion, and external editorial judgment.  
**Empirical claim about current LLM hidden states:** none.

---

## Abstract

Autoregressive models are optimized for language prediction but are increasingly expected to make decisions that must later change when evidence, sources, or assumptions change. Existing theory already provides minimal predictive states, utility-defined decisional states, task-aware predictive representations, information states, value-equivalent abstractions, and minimal recursively updateable memory; recent LLM work also studies belief revision, decision-aware memory, bounded memory, and learned context compression. We therefore do not propose another generic state-minimization or memory theory. Instead, we formalize a representation-assessment problem. Taking a state sufficient for the complete declared linguistic future as a reference, we distinguish three obligations: linguistic predictive adequacy, current responsibility-decision adequacy, and prospective evidence-triggered revision adequacy. We define conditional state-cost coordinates for the latter two and a dynamic optionality premium measuring state required solely for later revision after optimizing the present acceptable action. A mechanically verified finite construction has zero extra current-decision state but a one-bit prospective premium. Hence matched language prediction and matched current decisions do not, in general, certify future revision capability. We use this separation to specify a Prospective Revision Audit with present-equivalence gates, update/maintain controls, representation interventions, alternate-channel retention checks, and collision certificates. The contribution is a formal assessment task and analytical framework, not a claim that current language models necessarily discard revision-relevant information.

---

# 1. Introduction

A model can give the right answer today and still be in the wrong internal state for tomorrow.

Consider two histories that induce the same declared linguistic future and the same present responsibility decision. In one history, a conclusion is supported through source `A`; in the other, through source `B`. If support-source identity is irrelevant to the linguistic prediction target and to the current action, a compressed representation can merge the histories without any visible current loss. Later, however, an observation may report that source `A` was retracted. Correct behavior now requires reopening one conclusion while retaining the other. A representation that discarded the support-source distinction cannot necessarily perform that update even though it was adequate at the previous time step.

The underlying ingredients are not new. Computational mechanics and Predictive State Representations formalize future-sufficient state. Brodu's decisional states and statistical decision theory formalize utility-relative decision state. Reward-Predictive State Representations show that observation prediction can omit a reward target. POMDP belief states and Approximate Information State theory formalize recursively updateable history statistics for future control. Compatible-state and right-congruence constructions are classical in finite-state systems, and 2026 stable-quotient work gives a particularly close coarsest exact recursively updateable state and memory result in a structured partially observed process. Information Bottleneck, Value Equivalence, and rate-distortion approaches study how limited representation capacity should be allocated to decision-relevant information. Belief-R already evaluates whether LLM conclusions should update or remain after new evidence. Recent LLM-agent research studies learned context compression, decision-aware memory, bounded memory, and downstream failures caused by state compression.

These parents eliminate the broad claim that Machine Epistemics has discovered a new generic state theory.

The remaining question is narrower:

> **After two representations have already been matched on the declared linguistic prediction target and the registered current decision, can later evidence reveal a revision failure caused by historical information that one representation failed to retain?**

This is an assessment question about **prospective revision adequacy**.

The distinction is important because a present test can certify only what it observes. A representation may be adequate for today's prediction and today's decision yet lack a dormant historical distinction that becomes decision-relevant only after tomorrow's evidence. Conversely, a system may need no additional state at all for a particular responsibility; the framework must therefore include zero-extra-state controls rather than presuppose an architectural advantage.

## 1.1 Contributions after strongest-parent subtraction

This paper makes four bounded contributions.

**A three-stage representation assessment.** We separately register linguistic predictive adequacy, current responsibility-decision adequacy, and prospective revision adequacy. We do not treat one scalar confidence or memory score as a substitute for these distinct obligations.

**A finite no-certification theorem.** We construct and mechanically verify a process in which two representations are equally adequate for the declared language target and the same unique present action, yet differ after identical later evidence because only one retained a one-bit provenance distinction. Therefore the first two forms of adequacy do not certify the third.

**Conditional audit coordinates.** We account for state required beyond the linguistic predictive reference for the current responsibility and separately for future updateability. Their difference, the dynamic optionality premium, is a derived audit metric over parent-owned state constructions rather than a new information law.

**A fully specified Prospective Revision Audit.** The protocol freezes present-equivalence gates, P0/P1/P2 controls, update and maintain metrics, selective-reopening controls, representation interventions, alternate-channel retention checks, and exact collision certificates. It can be used with a frozen model or agent memory without training a new LLM.

---

# 2. Claim ceiling from prior theory

## 2.1 Predictive state is parent-owned

Let `H` be a finite history variable and `Y^+` the declared complete linguistic future. Define

\[
h\sim_P h'
\iff
P(Y^+\mid H=h)=P(Y^+\mid H=h')
\]

and let

\[
S_P=[H]_{\sim_P}.
\]

Causal-state theory defines equivalence classes by future conditional laws and proves minimal predictive properties under its assumptions. Predictive State Representations similarly use future predictions to represent controlled dynamical state. We use `S_P` only as a reference channel and claim no novelty for it.

## 2.2 Decision state is parent-owned

A decision may require less or different information than full prediction. Brodu's decisional-state framework groups predictive states according to user-provided utility/payoff and preferred decision. Blackwell-style decision theory more generally formalizes decision sufficiency and the effect of information loss on risk.

The opposite problem is also established: a state sufficient for one target can omit another. R-PSR shows that a PSR can accurately represent future observations while failing to represent rewards and gives conditions under which reward representation is possible.

Thus

\[
\text{prediction sufficiency}
\not\Rightarrow
\text{arbitrary secondary-decision sufficiency}
\]

is background rather than our novelty claim.

## 2.3 Recursive decision state is parent-owned

Approximate Information State theory defines history compression sufficient for current performance and for prediction/evolution of the next state, with recursive-update formulations and dynamic programming. Standard POMDP belief state is a special case. Classical finite-state compatibility/closed-cover theory requires both current compatibility and successor closure. Recent stable-quotient work provides an especially strong current parent: finite monotone refinement stabilizes to a coarsest exact abstraction, yields an exact value-preserving Markov state, and under its conditions implies a minimal reusable class-tracking memory size.

The dynamic construction used later is therefore inherited machinery. The paper does not claim a new right-congruence or minimal-memory algorithm.

## 2.4 Decision-aware compression is parent-owned

Information Bottleneck and deterministic variants formalize target-relevant compression. Value Equivalence and Proper Value Equivalence formalize when different environment models are indistinguishable for planning. Value-Equivalent Sampling explicitly uses rate-distortion ideas to trade representation complexity against decision quality. These literatures own the generic principle that capacity should preserve task-relevant information rather than reconstruct everything.

## 2.5 Revision state and LLM updating are active prior art

Iterated belief revision already studies state representations that preserve information beyond present beliefs; Liberatore analyzes the storage/succinctness of several exact doxastic-state representations under repeated revision.

Belief-R evaluates LLM belief revision after new evidence and explicitly distinguishes cases where the conclusion should update from cases where it should remain. Herrmann and Levinstein argue that belief-like representation requires more than decodability, including appropriate use. Recent ACL work provides evidence for causally useful internal belief-like signals, while other work warns that hidden-state self-knowledge signals may primarily track recall rather than truthfulness. Representation-identifiability theory also shows that matched predictor behavior does not identify arbitrary hidden representation properties.

These results make two boundaries mandatory:

1. this paper cannot assume LLMs contain no epistemic structure;
2. output-level revision performance alone does not identify what historical information the representation retained.

---

# 3. Direct 2026 LLM-memory neighbors

The practical memory literature makes the final contribution narrower still.

**MEMENTO** teaches reasoning models to compress prior reasoning blocks into compact learned states and continue reasoning from them. Particularly relevant to our audit, its ablations indicate that information from nominally evicted reasoning can persist implicitly through another KV-state channel. This means visible deletion is not evidence of actual information removal.

**PM-Bench** already uses the term prospective memory for LLM-agent delayed intentions and cue-triggered future execution. We therefore avoid using “prospective memory” as the name of our object; the target here is **prospective revision adequacy**.

**State Compression in Two-Agent LLM Relays** shows directly that lossy hand-off representation can change downstream constraint satisfaction. **Router-Mem** decides whether current memory/evidence suffices or deeper retrieval is needed. **Decision-Aware Memory Cards** selects/compresses context using decision utility, while **AgenticSTS** treats long-horizon memory as a bounded typed retrieval contract. Recent evidence-informed scientific-discovery and selected-evidence studies also model persistent/updating LLM beliefs.

Accordingly, the paper claims none of the following as new: LLM state compression, decision-aware memory, future reasoning from compact context, prospective-memory evaluation, evidence-updated LLM beliefs, or downstream failures caused by compressed state.

The remaining design delta is the **matched-current representation intervention**:

```text
match present language behavior
+ match present responsibility behavior
+ change/compare retained historical representation
+ reveal common later evidence
+ test selective update/maintain behavior
```

No direct parent found in the final search uses that sequence as its primary representation-certification object.

---

# 4. Responsibility contracts

A responsibility is an operational contract

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where `Q` is a mechanically or externally specified target, `\mathcal A` a finite action/terminal set, `\ell(a,q)` a registered loss, and `\sigma` the exact semantics that must be preserved.

We distinguish:

- `ANY_OPTIMAL_ACTION`;
- `CANONICAL_ACTION`;
- `OPTIMAL_ACTION_SET`;
- `ACTION_AND_RISK`;
- `EXACT_TARGET`.

For history `h`, let

\[
A^*(h)=
\arg\min_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

Under `ANY_OPTIMAL_ACTION`, any selector

\[
d(h)\in A^*(h)
\]

is acceptable. This avoids overestimating required state when optimal-action sets overlap. If two histories have sets `\{a,b\}` and `\{b,c\}`, a common selector may choose `b` for both even though the full option sets differ.

The responsibility is externally registered. Internal representation of support or uncertainty does not create institutional authority.

---

# 5. Present responsibility adequacy

Let `\mathcal D` be the set of acceptable Bayes-optimal selectors. Define the registered current conditional state cost

\[
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}
H(d(H)\mid S_P).
\]

Equivalently, histories may be merged only within an `S_P` fibre and only when their acceptable-action sets have a common member. The selector/partition equivalence is proved in the proof appendix and independently verified in the mechanical suite.

The quantity is an accounting coordinate, not a new decision-complexity theorem.

## P0 current control

\[
C_{\mathrm{stat}}^*=0
\]

iff some acceptable present policy factors through `S_P`. This is the mandatory Brodu-like/no-extra-state control.

## Positive present cross-channel cost

\[
C_{\mathrm{stat}}^*>0
\]

means no acceptable current responsibility policy can be implemented from the linguistic predictive state alone. At least one distinction inside a predictive fibre matters to the responsibility.

“Cross-channel” means only “not measurable from the declared linguistic predictive quotient.” It does not imply statistical independence or a separate physical channel.

---

# 6. Prospective revision adequacy

Let `x` be a registered future evidence event and `\delta(h,x)` the corresponding successor history when defined. A state adequate for a present action may fail to evolve into the correct future action.

A dynamic-admissible state must satisfy both:

1. present action compatibility;
2. successor compatibility under every registered feasible evidence event.

Let `\mathfrak P_{\mathrm{dyn}}` be the resulting finite state partitions and define

\[
C_{\mathrm{dyn}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_P).
\]

Equivalently, in the registered finite deterministic setting,

\[
C_{\mathrm{dyn}}^*
=
\min_{d\in\mathcal D}
H(S_\infty^d\mid S_P),
\]

where `S_\infty^d` is the stable right-congruent refinement of `(S_P,d)`. The equivalence is proved in the appendix and verified mechanically by independent direct and selector-based implementations.

The construction is a specialization of parent state/minimization theory; the paper uses it to define a **relative audit**.

---

# 7. Dynamic optionality premium

Define

\[
\boxed{
\Omega_{\mathrm{dyn}}
=
C_{\mathrm{dyn}}^*-C_{\mathrm{stat}}^*
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

# 8. One-bit prospective witness

Let two equiprobable current histories `h_A,h_B` share the same linguistic predictive state and the same unique present action `RETAIN`. They differ only in a one-bit provenance variable: the current conclusion is supported through source `A` or source `B`.

Reveal the same future event

\[
x=\mathrm{RETRACT}(A).
\]

At the successor histories, require

\[
h_A'\to\mathrm{REOPEN},
\qquad
h_B'\to\mathrm{RETAIN}.
\]

The two current histories may share one present responsibility state, so

\[
C_{\mathrm{stat}}^*=0.
\]

A recursively adequate state must nevertheless distinguish the histories before the event, because the same current state plus the same evidence event cannot deterministically yield two incompatible successor actions. With equal prior,

\[
C_{\mathrm{dyn}}^*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit}.
\]

The current action is unique; the result is not a tie-selection artifact. Exact mechanical execution reproduces these values.

---

# 9. No-certification theorem

## Theorem 1

There exists a finite process and two representations `Z_c,Z_a` such that:

1. they are equally adequate for the declared complete linguistic prediction target;
2. they support the same zero-regret current responsibility decision;
3. after the same registered future evidence, their achievable future responsibility risks differ.

Therefore an evaluation observing only present linguistic prediction and present responsibility performance cannot, in general, certify prospective revision adequacy over a process class containing the construction.

### Proof sketch

Let

\[
Z_c=S_P,
\qquad
Z_a=(S_P,B),
\]

where `B` is the provenance bit from Section 8. The bit changes neither the declared language target nor the unique present action. After `RETRACT(A)`, the augmented representation can distinguish the two successor decisions while the compressed representation cannot, provided the later evidence does not itself reconstruct `B`. The complete proof is in `PROOF_APPENDIX_V1.md`. ∎

The theorem establishes logical non-certification, not empirical frequency in real models.

---

# 10. Prospective revision collision certificates

For a representation `Z`, define a matched prospective revision collision `(h,h',x)` when:

1. `Z(h)=Z(h')`;
2. the histories are matched for the present linguistic target;
3. they admit the same acceptable current decision;
4. the same future evidence event `x` is feasible;
5. their acceptable future-action sets after `x` are disjoint.

Any deterministic future rule using only `(Z,x)` must output the same action for both histories and therefore fail at least one. The criterion is an ordinary decision/fibre argument; its value is as an **audit certificate** identifying the exact distinction lost by the representation.

Collision certificates should accompany aggregate revision metrics whenever possible.

---

# 11. P0/P1/P2 audit taxonomy

The finite state costs define three diagnostic regimes.

## P0 — predictive-decisional

\[
C_{\mathrm{stat}}^*=0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The linguistic predictive state supports the present and registered future responsibility. Extra state is unnecessary.

## P1 — current cross-channel refinement

\[
C_{\mathrm{stat}}^*>0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

Additional history-side state is required for the current decision, but the optimally compressed present responsibility state is already recursively sufficient.

## P2 — prospective refinement

\[
\Omega_{\mathrm{dyn}}>0.
\]

Additional dormant state is required specifically for later revision.

These are representation-audit classes, not levels of intelligence.

---

# 12. Horizon-indexed audit

For horizon `k`, let `\mathfrak P_k` contain present-compatible states that remain compatible under every registered future observation sequence of length at most `k`. Define

\[
C_k^*=
\min_{\Pi\in\mathfrak P_k}
H(\Pi(H)\mid S_P),
\qquad
\Omega_k=C_k^*-C_0^*.
\]

Nested feasible sets imply

\[
C_0^*\le C_1^*\le\cdots.
\]

Finite registered systems stabilize after finitely many refinements. These facts are inherited from finite-state theory; the audit interpretation asks how far into the registered evidence process the retained state remains adequate.

The mechanical suite verified monotonicity and stabilization on every registered finite horizon fixture.

---

# 13. Representation Audit Profile

Report four separate coordinates:

\[
\boxed{
\operatorname{RAP}_k(Z;r)
=
(
\Delta_{\mathrm{pred}},
\delta_0,
\delta^{\mathrm{rev}}_k,
\operatorname{Cost}
)
}.
\]

Here:

\[
\Delta_{\mathrm{pred}}(Z)
=
H(Y^+\mid Z)-H(Y^+\mid H)
\]

in the finite log-loss reference;

\[
\delta_0(Z;r)
=
\mathcal R_r(Z)-\mathcal R_r(H)
\]

is current responsibility regret; and

\[
\delta^{\mathrm{rev}}_k(Z;r)
=
\mathcal R_{r_{t+k}}(Z_t,X_{1:k})
-
\mathcal R_{r_{t+k}}(H_t,X_{1:k})
\]

is future revision regret.

In actual neural systems, `Cost` must be an operational capacity proxy—retained tokens, serialized bytes, transmitted bits under a fixed encoder, memory slots, or another registered state budget. Hidden dimension alone is not an information measure.

The coordinates are non-compensatory: better language prediction does not cancel a revision failure.

---

# 14. Acquisition, compression, and prospective loss

Under log loss, distinguish:

\[
H(Q\mid H)
\]

for information absent from the accessible history;

\[
I(Q;H\mid Z)
\]

for useful current information lost by compression; and

\[
I(Q_{t+k};H_t\mid Z_t,X_{1:k})
\]

for current historical information that becomes useful only after future evidence.

The identities are standard information theory. Their purpose is diagnostic routing:

- acquisition failure -> obtain evidence;
- current compression failure -> retain current decision information;
- prospective loss -> preserve or deliberately re-acquire revision-relevant information.

---

# 15. Bounded responsibility families

No compressed state should be called universally sufficient without specifying the responsibilities and future horizon it promises to support.

For any deterministic responsibility signature `C_\mathcal R(H)`,

\[
0
\le
H(C_\mathcal R\mid S_P)
\le
H(H\mid S_P).
\]

If the family separates every positive-support history pair within predictive fibres, it recovers all non-predictive history information and reaches the upper bound. Every non-injective finite representation also fails some constructed binary exact responsibility.

These are classical/elementary boundaries. Their role is to prevent unbounded claims such as “this compressed state is epistemically sufficient for any future question.”

---

# 16. Mechanical validation

The finite theory was executed in four merged mechanical batches.

**Static audit.** All set partitions through `n=7` were exhaustively enumerated with Bell counts `1,2,5,15,52,203,877`. Predictive-state structural checks, decision semantics, tie behavior, selector/partition equivalence, joint state sharing, and zero-cost controls passed.

**Information-deficit audit.** Acquisition/current/prospective identities and five controls were tested over 900 seeded rational worlds using exact log-linear arithmetic with a high-precision decimal cross-check.

**Dynamic audit.** Direct dynamic-partition and selector-refinement calculations agreed on registered fixtures; non-negative optionality, the one-bit witness, P0/P1/P2 controls, horizon stabilization, responsibility-family monotonicity, and bounded/universality checks passed.

**Mutation audit.** Removing entropy minimality, constraining zero-mass nominal histories, and assuming structural stability from near-minimal entropy produced counterexamples. Registered approximate/stochastic/cardinality variants retained narrower conclusions.

A search of 5,826 small machines found no mixed-P2 witness and remains `CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS`. One non-load-bearing worst-fibre bound lacked a distinct mechanized check and was removed from the publication claim set rather than preserved for completeness.

---

# 17. Prospective Revision Audit Protocol

The canonical protocol is `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V2.md`.

A valid empirical audit contains four case families:

- acquisition/non-identifiability controls;
- P0 cases;
- P1 current-cross-channel cases;
- P2 prospective-revision cases.

It compares, where feasible:

- full-history state;
- prediction-preserving compressed state;
- current-decision-sufficient state;
- prospective-augmented state.

Future revision comparisons are valid only after present-equivalence tolerances for language, current action/risk, resources, and inference budget pass.

Primary future metrics include separate **update** and **maintain** accuracy, false-revision and missed-revision rates, prospective regret, and representation cost. Independent-support controls test selective rather than global reopening.

---

# 18. Alternate-channel retention is a mandatory causal gate

A claimed state-removal intervention is invalid if the supposedly removed dormant variable remains in another channel.

This concern is not hypothetical. MEMENTO demonstrates that reasoning content can be nominally evicted while useful information persists implicitly through downstream KV representations. Therefore deletion from visible text or a summary object cannot by itself establish that the model no longer retains the information.

The audit must enumerate relevant surviving channels—prompt/context, KV cache, hidden activations, summary embeddings, retrieval keys, explicit tool state, or external memory—and where feasible test recoverability, causal use, and channel ablation.

Use terminals:

- `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION`;
- `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`;
- `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`.

A strong P2 claim requires actual removal or an explicitly bounded statement naming the channels that remain unchecked.

---

# 19. Relation to direct LLM revision/memory baselines

## Belief-R

Already evaluates output update versus maintain after new evidence. Our audit adds matched current behavior and a representation intervention.

## MEMENTO

Already learns compact internal reasoning state and demonstrates hidden alternate information channels. Our audit uses this as a causal-removal warning/control.

## PM-Bench

Already evaluates prospective memory for future intentions. Our task concerns later **revision of a current epistemic decision**, not remembering an intention.

## State Compression in Two-Agent LLM Relays

Already shows that compressed hand-off state can harm downstream exact decisions. Our audit adds the requirement that the current decision be matched and that a later common evidence event expose the lost distinction.

## Router-Mem

Already evaluates current memory/evidence sufficiency and routes to deeper retrieval. Our P2 state is sufficient now but becomes insufficient only after later evidence.

## Decision-Aware Memory Cards / AgenticSTS

Already study decision-critical memory selection and bounded typed long-horizon memory. They provide natural practical surfaces for applying, not motivating novelty of, the audit.

## Evidence-informed / selected-evidence belief studies

Already study persistent/evolving beliefs and omitted evidence. The audit distinguishes acquisition/selection from same-information retention loss.

---

# 20. Optional frozen-model execution

No training is required.

Useful state surfaces include:

- prompt/context truncation or deterministic summary;
- explicit external agent memory;
- retrieval memory fields;
- KV cache compression/ablation where accessible;
- hidden-state intervention if present behavior remains matched.

The load-bearing contrast is current-decision-sufficient versus prospective-augmented state on P2 cases. A hidden-state probe alone is insufficient; prefer a causal intervention that changes retained information while leaving present behavior within the frozen equivalence tolerance.

Valid outcomes include P0, P1, P2, no mechanism effect, acquisition limit, future-evidence reconstruction, or CANNOT_CHECK alternate-channel removal. The experiment may not be tuned to manufacture P2.

---

# 21. Limitations

1. The strongest proofs and exhaustive checks are finite/discrete.
2. Exact `S_P` is a theoretical reference and generally unavailable in a deployed LLM; empirical studies require a registered prediction surrogate.
3. Responsibilities are externally specified; the framework does not decide which responsibilities institutions should require.
4. Real-model state cost is intervention-dependent and cannot be read off from hidden dimension.
5. The state-minimization mathematics is heavily parent-owned.
6. Belief revision, decision-aware memory, prospective memory, and context compression all have active direct prior art.
7. No real LLM P2 failure is demonstrated in this paper.
8. A state-removal intervention can be invalidated by alternate retained channels.
9. Later evidence can reconstruct information that did not need to be stored permanently.
10. Unbounded responsibility families force increasing history retention, so all sufficiency claims must be bounded by responsibility and horizon.

---

# 22. Publication positioning

The final strongest-parent and direct-neighbor audits make the paper unsuitable as a new generic state theory.

JMLR is defensible only through its scope for formalizing new assessment tasks and analytical frameworks for learning systems. The current internal hostile-editor assessment is borderline/high risk because a reviewer may regard the audit as a straightforward application of information-state theory plus Belief-R and memory ablation.

The publication route is therefore frozen:

1. finish mechanical bibliography/display binding;
2. run final hostile review on the exact final manuscript;
3. submit JMLR only if the distinctness gate reaches at least `BORDERLINE_SUBMIT`;
4. otherwise route to TMLR;
5. if independent review judges the audit not standalone paper-scale, merge it into the Machine Epistemics flagship.

No route permits inflation of parent-owned mathematics.

---

# 23. Conclusion

Prediction, present decision, and future revision are different representation obligations.

Existing theory already explains how to compress history for prediction or decision and how to construct recursively updateable state. Recent LLM research already studies belief revision, context compression, decision-aware memory, bounded memory, and prospective intentions. The surviving contribution here is narrower: a way to **audit a representation only after current language and current decision behavior have been matched**, then ask whether later evidence exposes a dormant distinction the representation failed to retain.

The exact one-bit construction proves why that third test cannot be inferred from the first two. Two representations can be indistinguishable on the declared linguistic target and current unique optimal action yet differ in whether the same later evidence can trigger the correct selective revision.

For language-model and agent research, the resulting question is concrete:

> **After current language and decision behavior are matched, has the retained representation preserved the information needed for the right update when evidence changes?**

That question can be tested with frozen models, external memories, context compression, or synthetic representations without claiming consciousness, human-like belief, or a new neural architecture. It is the bounded Machine-Epistemic assessment claim that remains after strongest-parent and direct-neighbor subtraction.

---

# Citation set for mechanical `.bib` materialization

Use the exact roles/placements in `CITATION_AND_RELATED_WORK_PLAN_V1.md` and include the additional direct-neighbor identities in `NEAREST_WORK_PASS_05_LLM_MEMORY_AND_REVISION.md`.

No bibliography generator may omit a direct parent because it weakens a novelty narrative.
