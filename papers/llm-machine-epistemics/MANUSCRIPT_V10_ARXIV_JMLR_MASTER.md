# Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations

## Abstract

Autoregressive models are optimized for language prediction but are increasingly expected to revise decisions when evidence, sources, or assumptions change. Existing theory already provides predictive and decisional states, information states, value-aware compression, and recursively updateable memory; recent LLM work also studies belief revision and context compression. We therefore formalize a narrower representation-assessment problem. Relative to a registered linguistic prediction protocol, we distinguish predictive adequacy, current responsibility-decision adequacy, and prospective evidence-triggered revision adequacy under a distinct later intervention. A mechanically verified finite construction has zero extra state for the current decision but requires one additional bit for correct later revision. Thus matched current prediction and decision do not, in general, certify prospective revision capability. We use this separation to specify a Prospective Revision Audit with equivalence margins, update/maintain controls, representation interventions, alternate-channel and parametric-reconstruction checks, and complete future-action compatibility tests. The contribution is an analytical assessment framework, not a claim that current language models necessarily discard revision-relevant information.

## 1. Introduction

A representation can be sufficient for what a system must do **now** and still be insufficient for what the same system must do after evidence changes.

This distinction matters increasingly for language-model and agent systems. Long-lived systems summarize conversation histories, compress context, retain key–value or hidden-state memory, retrieve selected records, and carry intermediate state between decisions. Most evaluations ask whether the compressed or transformed representation preserves a current prediction, answer, reward, or task decision. That is a legitimate question, but it does not exhaust the responsibilities placed on a state that will later receive new evidence.

Consider two current histories. Under a declared language-prediction protocol, they induce the same linguistic prediction target and the same unique current action. One history contains a conclusion supported through source \(A\); the other contains the same conclusion supported through source \(B\). If support-source identity is irrelevant to the current prediction target and current action, a compact representation can merge the histories with no present loss. Now reveal the same later evidence to both systems: source \(A\) is retracted. The first history should reopen the conclusion; the second should retain it. A representation that discarded source identity cannot realize both revisions unless that distinction is reconstructed from another channel.

The ingredients of this example are not new state theory. Computational mechanics and predictive-state representations formalize histories that are equivalent for a future-prediction target \citep{shalizi2001computational,littman2001predictive}. Statistical decision theory and Brodu's decisional states formalize task- or utility-relative state \citep{blackwell1953equivalent,brodu2011decisional}. Reward-predictive state representations already show that a representation sufficient for one predictive target can omit another decision-relevant target \citep{baisero2021reconciling}. POMDP belief states, approximate information states, compatible finite-state reductions, and recent stable-quotient work address recursively useful or minimal state for future control \citep{smallwood1973optimal,subramanian2022approximate,paull1959minimizing,zhang2026minimal}. Information-bottleneck and value-equivalent frameworks formalize task-aware compression \citep{tishby1999information,strouse2017deterministic,grimm2020value,grimm2021proper,arumugam2022deciding}. These are direct parents, not ideas renamed here.

Recent LLM work narrows the residual further. Belief-R tests whether model conclusions should update or remain after new evidence \citep{wilie2024belief}. MEMENTO studies learned compact reasoning state and shows that apparently evicted information can persist through another internal channel \citep{kontonis2026memento}. PM-Bench studies prospective intention memory \citep{liu2026pmbench}; other work studies lossy state hand-offs, retrieval-memory sufficiency, decision-aware memory, and bounded long-horizon memory \citep{sharma2026state,lin2026stop,guan2026decision,cheng2026agenticsts}. Evidence-informed and selected-evidence updating are also active topics \citep{agarwal2026evidence,deng2026selected}. The present paper therefore does not claim novelty for belief revision, context compression, future memory, or the generic fact that lossy state can harm downstream performance.

The narrower question is an **assessment** question:

> After two representations have already been matched on a registered linguistic prediction target and a registered current decision, can the same later evidence expose a revision difference caused by historical information retained by one representation but not the other?

We call this **prospective revision adequacy**. The paper makes four contributions after strongest-parent subtraction.

First, we separate three evaluation axes: adequacy for a registered linguistic prediction target, adequacy for a current responsibility decision, and adequacy for future evidence-triggered revision. Second, we give a finite no-certification result: current adequacy on the first two axes does not in general certify the third. Third, we define relative state coordinates that quantify current decision state and future-only state requirements without claiming a new generic memory-minimization theory. Fourth, we turn the separation into a Prospective Revision Audit with controls for present equivalence, evidence acquisition, alternate retention channels, parametric reconstruction, correct updating, correct maintaining, and tied future actions.

The claim is deliberately bounded. We do not show that deployed LLMs generally exhibit prospective revision failure. We do not propose a universal epistemic-state calculus. We do not claim that a state sufficient for **every possible controlled future** can forget information needed for one of those controlled futures. The reference prediction task and later evidence process are registered separately, and a stronger controlled-state target is an explicit parent control.

## 2. Registered prediction and responsibility

### 2.1 Prediction is relative to a reference protocol

Let \(H\) be a finite current-history variable. Let \(ho\) denote the registered input protocol or channel under which current linguistic prediction is evaluated, and let \(Y^+_ho\) denote the declared linguistic continuation under that protocol. Define predictive equivalence by

\[
h\sim_{P,\rho} h'
\quad\Longleftrightarrow\quad
P(Y^+_\rho\mid H=h)=P(Y^+_\rho\mid H=h').
\]

The corresponding predictive quotient is

\[
S_{P,\rho}=[H]_{\sim_{P,\rho}}.
\]

This object is inherited from sufficient-statistic and predictive-state theory. We use it as a reference representation, not as a new construction. When the protocol is fixed, we abbreviate \(S_{P,\rho}\) by \(S_P\).

The protocol index is essential. The later evidence intervention studied below is not silently included in \(ho\). If the reference task instead requires sufficiency across a controlled family that already includes the later intervention, then the distinction needed for revision may become present-state-relevant. That stronger reference is a legitimate control and can eliminate the prospective premium. Our result concerns certification across **different registered responsibilities**, not a failure of a universally sufficient controlled state.

### 2.2 Responsibility is a decision contract

A responsibility is represented by

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where \(Q\) is an externally or mechanically specified target, \(\mathcal A\) is an action or terminal set, \(\ell(a,q)\) is a registered loss, and \(\sigma\) specifies what counts as satisfying the responsibility.

For a history \(h\), define the Bayes-optimal action set

\[
A^*(h)=\arg\min_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

Different responsibilities require different semantics. Sometimes any Bayes-optimal action is acceptable; sometimes a canonical action, the complete optimal-action set, calibrated risk, or the exact target must be preserved. This distinction matters when optimal actions are tied. If one history permits \(\{a,b\}\) and another permits \(\{b,c\}\), both can share a current decision state under an `ANY_OPTIMAL_ACTION` contract by choosing \(b\). Requiring the entire optimal-action set would be a stronger responsibility and can require more state.

The term *responsibility* is intentionally operational. It can represent claim status, support dependence, scope validity, identifiability, an abstention requirement, or a revision obligation. It does not create institutional authority, and it does not turn an arbitrary auxiliary label into an epistemic target.

## 3. Present and prospective state costs

### 3.1 Present responsibility state

Let \(\mathcal D\) be the set of acceptable Bayes-optimal selectors \(d\) satisfying \(d(h)\in A^*(h)\) for every history under `ANY_OPTIMAL_ACTION` semantics. Define the conditional present-state cost

\[
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}
H(d(H)\mid S_{P,\rho}).
\]

This is an accounting coordinate relative to the registered prediction state. It does not claim a new decision-complexity theorem. Equivalently in the finite deterministic setting, histories can share one state only when they lie inside the same predictive fibre and admit a common acceptable current action.

The zero-cost case is important:

\[
C_{\mathrm{stat}}^*=0
\]

if and only if some acceptable present policy factors through \(S_{P,\rho}\). In that case, the registered linguistic predictive state is already sufficient for the current responsibility.

Positive \(C_{\mathrm{stat}}^*\) means that distinctions invisible to the registered linguistic target matter **now** for the current decision. We call those distinctions *cross-channel* only in this decision-relative sense; no physical or statistical independence is implied.

### 3.2 Prospective state

Now let \(x\) be a registered future evidence event and \(\delta(h,x)\) the successor history when the event is feasible. A state that is adequate for the present action may still be unable to evolve to the appropriate future action.

In the finite exact setting, a dynamically admissible partition must preserve current action compatibility and successor compatibility under the registered evidence process. Let \(\mathfrak P_{\mathrm{dyn}}\) denote those partitions. Define

\[
C_{\mathrm{dyn}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_{P,\rho}).
\]

Equivalently, for a fixed acceptable current selector one can refine \((S_{P,\rho},d)\) until it is stable under registered successor transitions. Minimizing across acceptable selectors gives the same optimum in the registered finite construction. These minimization mechanisms are classical finite-state/information-state machinery; their role here is to measure a relative representation requirement.

Define the **dynamic optionality premium**

\[
\boxed{
\Omega_{\mathrm{dyn}}
=C_{\mathrm{dyn}}^*-C_{\mathrm{stat}}^*.
}
\]

Because dynamic admissibility contains the present decision constraints,

\[
\Omega_{\mathrm{dyn}}\ge 0.
\]

The interpretation is narrow: \(\Omega_{\mathrm{dyn}}\) measures state needed solely because a present-acceptable policy must remain correct under the registered future evidence process.

## 4. A one-bit no-certification witness

Consider two equiprobable histories \(h_A\) and \(h_B\). Under the registered prediction protocol \(ho\), they have the same predictive state and the same unique current action `RETAIN`. They differ only in one provenance bit:

- in \(h_A\), claim \(C\) is currently supported through source \(A\);
- in \(h_B\), the same claim is currently supported through source \(B\).

By construction, the support-source bit does not change \(Y^+_ho\) and does not change the current action. Therefore the present responsibility can be implemented directly from \(S_{P,ho}\), and

\[
C_{\mathrm{stat}}^*=0.
\]

Now supply the same later evidence event to both histories:

\[
x=\operatorname{RETRACT}(A).
\]

The correct successor actions are

\[
h_A'\rightarrow \operatorname{REOPEN},
\qquad
h_B'\rightarrow \operatorname{RETAIN}.
\]

A compressed representation that merged the histories has the same state before the event and receives the same event. It therefore cannot deterministically produce both required successor actions. Retaining the one provenance bit is sufficient, so under the equal prior

\[
C_{\mathrm{dyn}}^*=1\text{ bit}
\]

and hence

\[
\boxed{
\Omega_{\mathrm{dyn}}=1\text{ bit}.
}
\]

The present action is unique, so the result is not created by arbitrary tie-breaking.

This construction supports the central theorem.

### Theorem 1 — prospective no-certification

For some finite registered prediction protocol \(ho\), current responsibility \(r_0\), future evidence event \(x\), and future responsibility \(r_1\), there exist representations \(Z_c\) and \(Z_a\) such that:

1. \(Z_c\) and \(Z_a\) are equally adequate for the declared linguistic prediction target \(Y^+_\rho\);
2. both support the same zero-regret current responsibility decision;
3. after the same future evidence event \(x\), their achievable future responsibility risks differ.

Therefore evaluation of only the registered current prediction target and current responsibility cannot, in general, certify prospective revision adequacy under a distinct later evidence process.

**Proof.** Let \(Z_c=S_{P,\rho}\) and \(Z_a=(S_{P,\rho},B)\), where \(B\) is the provenance bit above. By construction \(B\) changes neither the registered current prediction law nor the unique current action. Thus both representations are equivalent on the two observed current criteria. After `RETRACT(A)`, the future responsibility distinguishes histories according to \(B\). The augmented representation can implement the distinct future actions; the compressed representation cannot, because the same \((Z_c,x)\) input would have to map to two incompatible actions. Therefore current equivalence does not certify future revision equivalence. ∎

The theorem is intentionally existential. It does not establish how often this occurs in neural representations, and it does not say that a representation explicitly sufficient for the joint controlled future can omit a distinction required by that same controlled future.

## 5. Complete one-step compatibility

The one-bit example uses unique future actions. With tied actions, a pairwise collision test is only a sufficient failure witness.

For a representation value \(z\) and evidence event \(x\), define the reachable cell

\[
\mathcal C(z,x)
=
\{h:Z(h)=z,\;\delta(h,x)\text{ is defined}\}.
\]

Let \(A_x^*(h)\) denote the acceptable future-action set after the event. Define the joint compatibility set

\[
\boxed{
\mathcal I(z,x)
=
\bigcap_{h\in\mathcal C(z,x)} A_x^*(h).
}
\]

Under exact one-step `ANY_OPTIMAL_ACTION` semantics, a deterministic future rule using only \((z,x)\) is acceptable for every history in the cell if and only if

\[
\mathcal I(z,x)\neq\varnothing.
\]

Necessity follows because a single output action must be acceptable for every history represented by the cell. Sufficiency follows by choosing any element of the intersection.

This distinction matters because pairwise overlap is not enough. The sets

\[
\{a,b\},\quad \{b,c\},\quad \{a,c\}
\]

have nonempty pairwise intersections but empty three-way intersection. Thus the absence of a disjoint pair does not certify compatibility. In the canonical one-bit witness, the future sets are singletons \(\{\mathrm{REOPEN}\}\) and \(\{\mathrm{RETAIN}\}\), so the pairwise collision is complete.

The intersection criterion is ordinary decision-sufficiency logic, not a new mathematical contribution. Its role is to make the audit complete in tied-action cases.

## 6. An audit taxonomy

The relative state coordinates define three useful regimes.

### P0 — current and prospective sufficiency

\[
C_{\mathrm{stat}}^*=0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The registered predictive state already supports the current responsibility and the registered revision process. Extra state is unnecessary.

### P1 — current cross-channel state

\[
C_{\mathrm{stat}}^*>0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The predictive reference omits information needed for the current responsibility, but no additional future-only distinction is required once that state is retained.

### P2 — prospective refinement

\[
\Omega_{\mathrm{dyn}}>0.
\]

A representation adequate for the present responsibility still omits information needed only after later evidence.

Acquisition failure is separate. If even the full accessible history plus later evidence cannot identify the correct future action, the problem is not compression. Likewise, if the later evidence itself reconstructs the dormant distinction, persistent storage was not required. Finally, a stronger reference state that was explicitly optimized for the controlled intervention family may turn a P2 case into P0 or P1. The taxonomy is therefore responsibility- and channel-relative, not a universal scale of intelligence.

For a finite evidence horizon \(k\), the same construction yields a nondecreasing sequence of minimum state costs \(C_k^*\). Finite systems eventually stabilize because successive compatible partitions cannot refine indefinitely. This supporting fact is inherited finite-state machinery; the audit interpretation asks how far into a registered evidence process the current representation remains adequate.

## 7. Prospective Revision Audit

The theorem motivates an assessment procedure rather than a new memory architecture. The audit asks whether a representation retains, or can reliably reconstruct, the information required for correct later revision **after current behavior has already been matched**.

### 7.1 Register the evaluation object

Before future outcomes are examined, register separately:

- the reference input protocol \(ho\);
- the linguistic prediction target;
- the current responsibility and loss;
- the future evidence-intervention family;
- the future responsibility;
- the representation conditions;
- the resource budget;
- the decoding policy;
- equivalence margins for present behavior.

This prevents the prediction target from being broadened or weakened after the later-evidence result is known.

### 7.2 Establish present equivalence

A prospective-revision contrast is interpretable only if the representation conditions are sufficiently matched on the current criteria. The gate should cover the registered linguistic metric, current action or risk, tool access, and current inference budget aside from the intended state difference.

For noisy empirical metrics, failure to reject a difference is not evidence of equivalence. Equivalence margins must be chosen prospectively and supported by an appropriate interval or equivalence test. The independent unit is the registered case or episode, not repeated stochastic samples from one case unless sampling variability itself is the estimand.

If current equivalence fails, the result is a current-state deficit rather than evidence of P2 prospective loss.

### 7.3 Intervene on retained state

The audit compares a full or prospective representation against a state designed to preserve the registered current criteria while removing or collapsing a specified dormant distinction. Candidate surfaces include prompt/context memory, summaries, retrieval memory, key–value state, hidden-state projections, or explicit external memory.

The intervention must target representation state rather than merely prompt the model to forget a fact verbally.

### 7.4 Exclude alternate retention and reconstruction

Visible deletion does not prove information removal. The supposedly removed variable may remain in:

- prompt or context text;
- key–value cache;
- residual or hidden activations;
- a summary embedding;
- retrieval keys or index metadata;
- tool or session state;
- external memory.

Fixed model parameters are also side information. A model can sometimes reconstruct a public source identity or infer a missing variable from content even when episode memory does not contain it explicitly. Where the scientific question is episode-state retention, randomized or nonce episode-local assignments can help separate stored state from parametric reconstruction, provided they do not destroy the meaning of the responsibility.

A strong state-removal attribution requires evidence that the registered dormant information is absent from the channels being claimed as removed. If this cannot be established, the appropriate terminal is `CANNOT_CHECK`, not a causal statement about memory loss.

### 7.5 Deliver common later evidence

After the present-equivalence and removal gates pass, deliver the same registered later evidence to each representation condition. The evidence must be bound to the same scientific object; differences in evidence access would convert the comparison into an acquisition study.

### 7.6 Score both update and maintain

Revision competence is not simply a tendency to change answers. An adequate system must update when evidence defeats support and maintain a commitment when the evidence is irrelevant or independent sufficient support survives. When a support/dependency structure is registered, selective reopening should be scored: only commitments whose sufficient support has been defeated should reopen.

Thus the primary behavioral measures are:

- missed-revision rate or regret;
- false-revision rate or regret;
- update accuracy;
- maintain accuracy;
- selective-reopening precision and recall when dependencies are known.

For exact finite cases, the structural diagnostic is whether any representation/evidence cell has an empty joint acceptable-action intersection \(\mathcal I(z,x)\).

### 7.7 Distinguish deterministic and stochastic systems

The finite theory uses deterministic zero-regret action semantics. If stochastic decoding is part of the system under study, the temperature, sampling policy, number of samples, seed policy, aggregation rule and decision estimand must be frozen. Repeated generations from one episode do not create independent scientific cases.

A randomized policy with zero regret for every history in a cell can only put mass on actions acceptable to every history, so the joint intersection condition remains necessary. If nonzero regret is permitted, mixtures can trade losses across histories; the registered loss and expected or worst-case regret should then replace the exact zero-regret terminal.

## 8. Relation to existing LLM evaluation

The Prospective Revision Audit is deliberately adjacent to, but not identical with, several current evaluation families.

Belief-R asks whether an LLM should update or maintain a conclusion after new evidence \citep{wilie2024belief}. The present audit adds a representation-state question: before common future evidence is delivered, the compared states must be matched on current prediction and decision, and the historical distinction under test must be manipulated or measured.

MEMENTO studies compact internal reasoning state and demonstrates that apparently evicted information can remain available through another internal state channel \citep{kontonis2026memento}. This motivates the audit's alternate-channel gate. Passing a visible-deletion intervention without checking hidden retention would not support a P2 state-loss interpretation.

PM-Bench studies prospective memory for future intentions \citep{liu2026pmbench}. Our target is different: evidence-triggered revision of a current responsibility rather than delayed execution of an intention.

State-compression relay studies show that lossy state can hurt downstream exact decisions \citep{sharma2026state}. The present-equivalence requirement asks a narrower question: can two states behave equivalently **now** and diverge only after common later evidence?

Router-Mem and decision-aware/bounded-memory approaches evaluate current memory sufficiency or choose memory according to present task utility \citep{lin2026stop,guan2026decision,cheng2026agenticsts}. Those systems are natural substrates for the audit precisely because a representation can be sufficient for current utility while remaining untested for future revision.

Accordingly, the paper's residual is not any one component. It is the conjunction:

\[
\text{registered current target}
+\text{present equivalence}
+\text{state-retention contrast}
+\text{common later evidence}
+\text{reconstruction controls}
+\text{update/maintain evaluation}.
\]

We found no direct prior work through the registered 2026-08-29 search frontier that uses this complete sequence as its primary assessment object. This is a bounded search-frontier claim, not a universal priority claim.

## 9. Mechanical validation

The theory is accompanied by deterministic finite audits intended to expose statement errors and boundary cases rather than to substitute computation for proof.

The static layer exhaustively enumerated all set partitions through seven states and independently recovered the Bell numbers

\[
1,2,5,15,52,203,877.
\]

The audit verified predictive-refinement structure, current decision semantics under several tie policies, selector/partition equivalence, zero-cost controls, and shared-state savings for correlated responsibilities. The information layer checked the registered conditional-entropy and mutual-information identities over seeded rational finite worlds. The dynamic layer independently computed recurrent state by direct admissible-partition search and selector-based stable refinement; both routes agreed on the registered fixtures, including the one-bit witness. P0/P1/P2 controls, horizon monotonicity, finite stabilization, responsibility-family monotonicity, and bounded-history limits were also checked.

A separate mutation battery removed or weakened assumptions to determine which statements survived. The resulting contractions are reflected in the manuscript rather than hidden. A search over 5,826 small machines found no registered mixed-P2 witness and remains `CANNOT_CHECK`; absence in that finite search is not reported as an impossibility theorem.

The complete tied-action joint-intersection criterion was added after the main mechanical batches and has an elementary proof. Its three-history control should be included in the final executable package; until that check is run, it is reported as proof-supported rather than separately mechanized.

## 10. Practical implications

The theorem does not prescribe one neural architecture. It changes what should be **tested** when a representation is intended to support evidence-responsive behavior.

For context compression, present perplexity or task accuracy can establish that a current target was preserved, but not that the summary retained what a later source correction will require. For retrieval memory, a current sufficiency router can correctly decide that no additional retrieval is needed now while still leaving a future revision underdetermined if source-dependence information was discarded. For KV-cache or hidden-state compression, a present-output match does not identify which dormant distinctions remain available to later computation. For long-lived agents, a memory policy optimized only for present reward or current task loss can be adequate under that objective without being certified for later evidence-sensitive reopening.

The audit therefore offers a simple design principle:

> A representation intended to support evidence-responsive decisions should be evaluated not only on present prediction and present decisions, but also on registered future evidence processes under which currently dormant distinctions can become decision-relevant.

The principle is deliberately conditional. If the future process is already included in the state objective, the required distinction may be retained and the prospective premium may be zero. If later evidence reconstructs the missing variable, persistent storage may be unnecessary. If full history cannot identify the future decision, more memory is not the solution. The audit's purpose is to distinguish these cases rather than to demand maximal retention.

## 11. Limitations

The exact results are finite and discrete. They establish an existence and certification boundary, not the prevalence of prospective revision failures in neural language models.

The predictive reference is task- and protocol-relative. A stronger controlled-state target that includes the later intervention family may absorb the distinction used in the witness. This is expected and is an explicit control.

The responsibility family is externally declared. The framework does not determine which responsibilities a system ought to have, and it does not convert internal representation adequacy into scientific, legal, or institutional authority.

Real-model state removal can be difficult to establish. Information may survive in unobserved activations, cached state, retrieval metadata, external tools, or fixed parameters. The protocol therefore permits `CANNOT_CHECK` rather than treating probe failure or visible deletion as proof of absence.

Operational memory size and information-theoretic state cost should not be conflated. Exact conditional entropy is meaningful in the finite fixtures; in real systems, practical costs may instead be retained tokens, serialized bytes, cache budget, transmitted bits under a fixed encoder, or another explicitly defined resource.

Most of the underlying mathematics is parent-owned. The paper's case for standalone publication rests on the usefulness and distinctness of the **assessment task**, not on renaming causal states, decision states, information states, rate-distortion theory, or finite-state minimization.

Finally, the theory-first paper does not require a real-LLM experiment for its logical claim. Such experiments would be valuable for measuring prevalence and practical effect size, but adding one post hoc should not be used to rescue a failed novelty or correctness argument.

## 12. Conclusion

A representation can be adequate for a registered language-prediction target and the exact decision required today while remaining inadequate for a decision that becomes distinguishable only after evidence changes.

The one-bit construction makes that separation explicit:

\[
C_{\mathrm{stat}}^*=0,
\qquad
C_{\mathrm{dyn}}^*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit}.
\]

The result is not a claim that current LLMs are generally missing epistemic state. It is a no-certification result: present prediction and present decision do not, by themselves, certify future revision adequacy under a distinct registered evidence process.

The Prospective Revision Audit turns that logical gap into an evaluation procedure. It first establishes present equivalence, then tests whether a historical distinction was genuinely removed rather than retained or reconstructed elsewhere, supplies the same later evidence, and scores both correct updating and correct maintaining or selective reopening. Under exact tied-action semantics, the full joint acceptable-action intersection provides the one-step compatibility criterion.

This framing makes the contribution deliberately modest and testable. Existing state theories remain the mathematical parents. The proposed advance is to treat **future evidence-triggered revision as a separate representation-assessment axis** after current behavior has already been matched.

For long-lived language models and agents, that is the question the paper asks evaluators to add:

> When later evidence changes what should be done, did the representation preserve—or make reliably reconstructable—the distinctions required to change the right commitments and leave the others intact?

## Reproducibility and AI-assistance statement

The core finite claims have both human-readable proofs and deterministic executable audit artifacts. The computational suite includes exhaustive finite partition checks, independent constructions of dynamic state, registered counterexamples and assumption-mutation tests. No LLM training or empirical hidden-state benchmark is required for the theorem stated here.

Large language model systems were used extensively as research-assistance tools for literature discovery, formalization, adversarial critique, software generation, and manuscript drafting/editing. AI systems are not authors. Human authors must review and adopt the final scientific claims, proofs, citations, and reported mechanical evidence and take responsibility for the submitted work.
