# Beyond Predictive Sufficiency: A Prospective Revision Audit for Autoregressive Representations

## Abstract

Autoregressive models are optimized for language prediction but are increasingly expected to revise decisions when evidence, sources, or assumptions change. Existing theory already provides predictive and decisional states, information states, value-aware compression, and recursively updateable memory; recent LLM work also studies belief revision and context compression. We formalize a narrower representation-assessment problem. Relative to a registered linguistic prediction protocol, we distinguish predictive adequacy, current responsibility-decision adequacy, and prospective evidence-triggered revision adequacy under a distinct later intervention. A finite compatibility theorem shows exactly when a merged representation state can support all acceptable future actions after common evidence; a mechanically verified construction matches current prediction and a unique current action while requiring one additional retained bit for correct later revision. We use this separation to define a Prospective Revision Audit with equivalence margins, state interventions, update/maintain controls, alternate-channel and parametric-reconstruction checks, and explicit unresolved terminals. The contribution is an assessment framework, not a new generic state theory or a claim that current language models necessarily discard revision-relevant information.

## 1. Introduction

A representation can be sufficient for what a system must do **now** and still be insufficient for what the same system must do after evidence changes.

This distinction matters for language-model and agent systems that summarize histories, compress context, retain key–value or hidden-state memory, retrieve selected records, or pass intermediate state between decisions. Most evaluations ask whether the transformed representation preserves a current prediction, answer, reward or task decision. That is an important question, but it does not establish what the representation will support after later evidence makes a previously irrelevant distinction decision-relevant.

Consider two current histories. Under a declared language-prediction protocol, they induce the same linguistic target and the same unique current action. One contains a conclusion supported through source \(A\); the other contains the same conclusion supported through source \(B\). If source identity is irrelevant to the present target, a compressed state can merge the histories without visible current loss. Now reveal the same later event to both systems: source \(A\) is retracted. The first history should reopen the conclusion; the second should retain it. Unless the missing distinction is reconstructed elsewhere, a representation that merged the histories cannot realize both revisions.

The paper turns this observation into a **matched-current prospective revision assessment**:

1. **match the current state** on a registered linguistic target and current responsibility decision;
2. **intervene on or compare retained historical representation**, with a registered dormant distinction;
3. **deliver the same later evidence**, after excluding alternate retention or reconstruction routes where possible;
4. **score future compatibility, correct updating and correct maintaining/selective reopening**.

This is the scientific object of the paper. It is not a claim that future tasks can generically require more information than present tasks; that principle is already embedded in mature state and decision theories.

Computational mechanics and predictive-state representations formalize future-sufficient state for a declared predictive target \citep{shalizi2001computational,littman2001predictive}. Statistical decision theory and Brodu's decisional states formalize task- or utility-relative state \citep{blackwell1953equivalent,brodu2011decisional}. Reward-predictive state representations show that a state sufficient for one predictive target can omit another decision target \citep{baisero2021reconciling}. POMDP belief states, approximate information states, compatible finite-state reductions and stable-quotient theory address recursively useful or minimal state for future control \citep{smallwood1973optimal,subramanian2022approximate,paull1959minimizing,zhang2026minimal}. Information-bottleneck and value-equivalent frameworks formalize task-aware compression \citep{tishby1999information,strouse2017deterministic,grimm2020value,grimm2021proper,arumugam2022deciding}. These are mathematical parents, not contributions renamed here.

Recent LLM work narrows the residual further. Belief-R evaluates whether conclusions should update or remain after new evidence \citep{wilie2024belief}. MEMENTO studies compact reasoning state and demonstrates that apparently evicted content can persist through another internal channel \citep{kontonis2026memento}. PM-Bench studies prospective intention memory \citep{liu2026pmbench}; other work studies lossy state transfer, retrieval-memory sufficiency, decision-aware memory and bounded long-horizon memory \citep{sharma2026state,lin2026stop,guan2026decision,cheng2026agenticsts}. Evidence-informed and selected-evidence updating are also active topics \citep{agarwal2026evidence,deng2026selected}.

The residual is therefore a certification question:

> **After current prediction and decision adequacy have been established, what additional evidence is needed before a representation can be treated as adequate for later evidence-triggered revision?**

We make four bounded contributions. First, we define a complete one-step compatibility condition for a representation/evidence cell under exact decision semantics. Second, we derive a no-certification corollary: present adequacy alone cannot establish prospective adequacy unless the corresponding future compatibility condition is also known. Third, we give an exact one-bit construction that is currently sufficient yet prospectively insufficient. Fourth, we define an operational Prospective Revision Audit for representation compression and memory systems.

The paper is deliberately narrow. It does not establish that deployed LLMs generally exhibit this failure. It does not propose a universal epistemic-state calculus. It does not claim that a representation sufficient for **every possible controlled future** can discard information required by one of those controlled futures. The current prediction protocol and later evidence process are registered separately, and a stronger controlled-state target is an explicit parent control.

## 2. Registered current tasks

### 2.1 Prediction is relative to a reference protocol

Let \(H\) be a finite current-history variable. Let \(ho\) denote the registered input protocol under which current linguistic prediction is evaluated and \(Y^+_ho\) the declared linguistic continuation under that protocol. Define

\[
h\sim_{P,\rho}h'
\quad\Longleftrightarrow\quad
P(Y^+_\rho\mid H=h)=P(Y^+_\rho\mid H=h').
\]

Let

\[
S_{P,\rho}=[H]_{\sim_{P,\rho}}.
\]

This quotient is inherited from sufficient-statistic and predictive-state theory. Once the reference protocol is fixed, we abbreviate it by \(S_P\).

The protocol index is essential. The later evidence intervention studied below is not silently included in \(ho\). If a representation is instead required to be sufficient across a controlled family that already contains the later intervention, then the distinction needed for revision may become present-state-relevant and the prospective deficit can disappear. That stronger controlled state is a positive control, not a contradiction.

### 2.2 Responsibility is a decision contract

Represent a responsibility by

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where \(Q\) is an externally or mechanically specified target, \(\mathcal A\) an action/terminal set, \(\ell(a,q)\) a registered loss and \(\sigma\) the semantics of satisfying the responsibility.

For history \(h\), define the Bayes-optimal action set

\[
A^*(h)=\arg\min_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

The contract may require any optimal action, a canonical action, the complete optimal-action set, calibrated risk or exact target recovery. These requirements are not interchangeable. Under an `ANY_OPTIMAL_ACTION` contract, histories with acceptable sets \(\{a,b\}\) and \(\{b,c\}\) can share a current decision state by choosing \(b\); preserving the entire optimal-action set would require a stronger representation.

The term *responsibility* is operational. It can denote claim status, support dependence, scope validity, identifiability, abstention or a revision obligation. It does not create institutional authority and does not turn an arbitrary label into an epistemic object.

## 3. Exact one-step prospective compatibility

Let \(Z=Z(H)\) be the representation under audit. For a registered later evidence event \(x\), let \(\delta(h,x)\) be the successor history when the event is feasible and let \(A_x^*(h)\) be the acceptable future-action set at that successor.

For representation value \(z\), define the reachable representation/evidence cell

\[
\mathcal C(z,x)
=
\{h:Z(h)=z,\;\delta(h,x)\text{ is defined}\}.
\]

Define the joint acceptable-action intersection

\[
\boxed{
\mathcal I(z,x)
=
\bigcap_{h\in\mathcal C(z,x)}A_x^*(h).
}
\]

### Theorem 1 — one-step compatibility characterization

Under exact `ANY_OPTIMAL_ACTION` semantics, there exists a deterministic future decision rule

\[
g:(z,x)\mapsto a
\]

that is acceptable for every history in every nonempty representation/evidence cell if and only if

\[
\mathcal I(z,x)\neq\varnothing
\]

for every such cell.

**Proof.** If \(g\) is acceptable for every history in \(\mathcal C(z,x)\), then \(g(z,x)\) belongs to every set \(A_x^*(h)\), so the intersection is nonempty. Conversely, if the intersection is nonempty, choose any action in it for \(g(z,x)\); that action is acceptable for every history in the cell. ∎

A pair of histories with disjoint future action sets is therefore an easy failure certificate, but pairwise overlap is not enough for compatibility. The three sets

\[
\{a,b\},\qquad \{b,c\},\qquad \{a,c\}
\]

have nonempty pairwise intersections and empty joint intersection.

The theorem is elementary decision-sufficiency logic. We do not claim mathematical priority for the intersection principle. Its role is to provide a complete one-step audit criterion.

### Corollary 1 — current adequacy is not a prospective certificate

Suppose a representation is adequate for the registered current prediction and responsibility tasks. That current adequacy certifies one-step prospective responsibility only if the future compatibility condition in Theorem 1 also holds for every registered evidence event and every representation/evidence cell.

Thus present adequacy alone is insufficient whenever a common future event produces an empty future-action intersection inside a state that current evaluation permitted to merge.

This corollary is the paper's no-certification statement. It identifies the extra condition that current-only evaluation does not test.

### One-step versus recurrent memory

Theorem 1 concerns one registered future decision given the representation and event. It does **not** characterize the minimum state needed to compress a sequence of future observations recursively. Multi-step updateability requires the established recurrent/information-state or right-congruence constructions. We use those parents below only to quantify the state needed when the representation itself must continue evolving.

## 4. A one-bit sharp witness

Consider equiprobable histories \(h_A\) and \(h_B\). Under the registered prediction protocol \(ho\), they share the same predictive state and the same unique current action `RETAIN`. They differ only in one provenance bit:

- in \(h_A\), claim \(C\) is supported through source \(A\);
- in \(h_B\), the same claim is supported through source \(B\).

By construction, support-source identity changes neither \(Y^+_ho\) nor the current action. The current responsibility therefore requires no additional state beyond \(S_{P,\rho}\).

Now supply the same evidence event

\[
x=\operatorname{RETRACT}(A).
\]

The future acceptable action sets are

\[
A_x^*(h_A)=\{\operatorname{REOPEN}\},
\qquad
A_x^*(h_B)=\{\operatorname{RETAIN}\}.
\]

Their intersection is empty. By Theorem 1, a representation that merged the histories cannot implement both decisions after the event. Retaining the source bit suffices.

To quantify the relative state cost, let \(\mathcal D\) be acceptable current Bayes-optimal selectors and define

\[
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}H(d(H)\mid S_{P,\rho}).
\]

For the witness,

\[
C_{\mathrm{stat}}^*=0.
\]

Let \(C_{\mathrm{dyn}}^*\) be the minimum conditional state entropy among representations that are also recursively compatible with the registered future process, using the established finite-state refinement machinery. The two equiprobable histories must then be separated, so

\[
C_{\mathrm{dyn}}^*=1\text{ bit}.
\]

Define

\[
\Omega_{\mathrm{dyn}}
=C_{\mathrm{dyn}}^*-C_{\mathrm{stat}}^*.
\]

The exact witness gives

\[
\boxed{
C_{\mathrm{stat}}^*=0,
\qquad
C_{\mathrm{dyn}}^*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit}.
}
\]

The current action is unique, so this separation is not a tie-breaking artifact.

## 5. P0, P1 and P2 assessment regimes

The relative state coordinates define three useful diagnostic regimes.

### P0 — current and prospective sufficiency

\[
C_{\mathrm{stat}}^*=0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The registered predictive state already supports the current responsibility and the future revision process.

### P1 — current cross-channel state

\[
C_{\mathrm{stat}}^*>0,
\qquad
\Omega_{\mathrm{dyn}}=0.
\]

The registered prediction state omits information needed **now**, but no additional future-only distinction is required once that state is retained.

### P2 — prospective refinement

\[
\Omega_{\mathrm{dyn}}>0.
\]

A present-adequate state omits information needed only after future evidence.

These regimes are not stages of intelligence. They are assessment outcomes relative to a declared prediction protocol, responsibility family and evidence horizon.

Acquisition failure is separate. If even full accessible history plus later evidence cannot identify the appropriate future action, the problem is not compression. Likewise, if later evidence reconstructs the dormant distinction, persistent storage was not required. A stronger reference state explicitly optimized for the controlled intervention family may also convert a P2 case into P0 or P1.

For a finite evidence horizon \(k\), established finite-state refinement gives a nondecreasing sequence of minimum compatible state costs \(C_k^*\) that eventually stabilizes. We use this as an audit curve, not as a new finite-state theorem.

## 6. Prospective Revision Audit

The formal results motivate an evaluation procedure rather than a memory architecture.

### Step 1 — register the current and future tasks

Before future outcomes are examined, freeze:

- reference prediction protocol \(ho\);
- current linguistic target;
- current responsibility and loss;
- future evidence-intervention family;
- future responsibility;
- representation conditions;
- resource budget;
- decoding policy;
- present-equivalence margins.

This prevents target definition from moving after the revision outcome is known.

### Step 2 — establish current equivalence

The compared states must be equivalent, within prospectively frozen margins, on the registered current prediction and decision criteria. Relevant resources and tool access must also be matched apart from the intended state difference.

For noisy empirical metrics, failure to reject a difference is not evidence of equivalence. Use a registered equivalence margin and an interval or equivalence test appropriate to the estimand. The independent unit is the episode/case, not repeated stochastic generations from the same episode unless sampling variability itself is the target.

If current equivalence fails, the result is a current-state deficit rather than prospective revision evidence.

### Step 3 — manipulate or compare retained state

Compare a full or prospectively sufficient representation against a state designed to preserve the registered current criteria while removing or collapsing a specified dormant distinction. Candidate surfaces include prompt/context memory, summaries, retrieval memory, key–value state, hidden-state projections and explicit external memory.

The intervention should target representation state, not merely instruct the model verbally to forget.

### Step 4 — exclude alternate retention or reconstruction

Visible deletion is not evidence that information has left the system. The dormant variable may remain in prompt text, key–value cache, hidden activations, summary embeddings, retrieval metadata, tool/session state or external memory. Fixed model parameters can also reconstruct public information or infer missing variables from content.

Where the scientific question is episode-state retention, randomized episode-local identities can help distinguish stored state from parametric knowledge when doing so preserves the meaning of the task. If the relevant alternate channel cannot be examined, the causal interpretation should remain unresolved.

### Step 5 — deliver common later evidence

After current equivalence and state-removal checks, provide the same registered later evidence to each representation condition. Different evidence access would turn the comparison into an acquisition study.

### Step 6 — evaluate future compatibility and behavior

For exact one-step tasks, compute or approximate the joint future compatibility condition from Theorem 1 where the action semantics are known. Behaviorally, evaluate both:

- correct updating when evidence defeats or changes support;
- correct maintaining when evidence is irrelevant or independent sufficient support remains.

When a support graph is registered, score selective reopening so a system is not rewarded for changing every conclusion after every evidence event.

Primary empirical quantities can include missed-revision regret, false-revision regret, update accuracy, maintain accuracy and selective-reopening precision/recall.

### Step 7 — handle stochastic systems explicitly

If stochastic decoding is part of the system, freeze temperature or sampling policy, seeds, number of samples, aggregation rule and the expected/worst-case regret estimand. Repeated samples from one episode remain nested observations.

A zero-regret randomized policy for every history in a merged cell can place probability only on actions accepted by all histories, so the joint-intersection condition remains necessary. With nonzero allowable regret, use the registered loss rather than an exact compatibility terminal.

## 7. Relation to current LLM evaluation

The Prospective Revision Audit is adjacent to several active evaluation families but asks a different conjunction of questions.

| Work family | Primary question already studied | Distinction added here |
|---|---|---|
| Belief-R | Should an output update or remain after new evidence? | Match the current representation/decision first and manipulate retained historical state before common future evidence. |
| MEMENTO / context compression | Can compact internal state preserve useful reasoning? | Audit whether a nominally removed distinction survives another channel and whether its loss affects later revision specifically. |
| PM-Bench | Can an agent remember and execute a delayed intention? | Evaluate evidence-triggered revision of a current decision rather than future intention execution. |
| State-compression relays | Does lossy state hurt a later downstream task? | Require equivalence on current prediction/decision before the common later event. |
| Router-Mem | Is current retrieved memory sufficient? | Test whether a state sufficient now remains adequate only after later evidence. |
| Decision-aware/bounded memory | Which information should memory preserve for current utility? | Treat future revision as an additional registered responsibility that may be dormant under current utility. |

The residual is not any one row. It is the registered sequence:

\[
\text{current target}
\rightarrow
\text{current equivalence}
\rightarrow
\text{state contrast}
\rightarrow
\text{reconstruction gate}
\rightarrow
\text{common later evidence}
\rightarrow
\text{update/maintain audit}.
\]

Through the registered literature search ending 29 August 2026, we found no direct prior work using this complete sequence as its primary assessment object. This is a bounded search-frontier statement, not a universal priority claim.

## 8. Mechanical validation and proof support

The finite theory is accompanied by deterministic audits designed to expose statement errors and boundary cases rather than substitute computation for proof.

The static layer exhaustively enumerated all set partitions through seven states and recovered the Bell counts

\[
1,2,5,15,52,203,877.
\]

It checked predictive-refinement structure, current decision semantics under multiple tie policies, selector/partition equivalence, zero-cost controls and shared-state savings for correlated responsibilities.

The dynamic layer independently computed recurrent state through direct admissible-partition search and selector-based stable refinement. The two methods agreed on the registered fixtures, including the one-bit witness. P0/P1/P2 controls, horizon monotonicity, finite stabilization, responsibility-family monotonicity and bounded-history limits were also checked.

An assumption-mutation battery removed or weakened conditions to identify which statements survive. The resulting contractions are reflected in this manuscript. A search over 5,826 small machines found no registered mixed-P2 witness and remains inconclusive rather than being reported as an impossibility theorem.

The joint-intersection theorem has the elementary proof above. A separate three-history checker is a reproducibility task, not a condition of the proof.

## 9. Practical implications

The results do not prescribe one neural architecture. They change what should be tested when representations are intended to support evidence-responsive behavior.

For context compression, current perplexity or task accuracy can establish that a present target was preserved but not that a summary retained what a later source correction will require. For retrieval memory, a current sufficiency router can correctly decide that no additional retrieval is needed now while leaving a later revision underdetermined if dependence information was discarded. For key–value or hidden-state compression, a present-output match does not identify which dormant distinctions remain available to later computation. For long-lived agents, memory optimized only for current reward can be adequate under that objective without being certified for later evidence-sensitive reopening.

This yields a conditional design principle:

> A representation intended to support evidence-responsive decisions should be evaluated not only on present prediction and present decisions, but also on registered future evidence processes under which currently dormant distinctions can become decision-relevant.

The principle does not imply maximal retention. If the future process is already included in the state objective, the required distinction can be retained and the premium can be zero. If later evidence reconstructs the missing variable, persistent storage may be unnecessary. If full history cannot identify the future decision, additional memory is not the solution.

## 10. Limitations

The exact theory is finite and discrete. It establishes a certification boundary, not the prevalence of prospective-revision failures in neural language models.

The prediction reference is protocol-relative. Stronger controlled-state targets can absorb the witness distinction. This is expected and is an explicit positive control.

Responsibilities are externally declared. The framework does not determine which responsibilities a system ought to have and does not convert internal representation adequacy into institutional authority.

Real-model state removal can be difficult to establish because information may remain in unobserved activations, cached state, retrieval metadata, external tools or parameters. The audit therefore permits unresolved outcomes rather than treating probe failure or visible deletion as proof of absence.

Operational state size and information-theoretic state cost should not be conflated. Exact conditional entropy is meaningful in the finite fixtures; real systems may require operational measures such as retained tokens, transmitted bits, cache budgets or serialized state under a fixed encoder.

Finally, most underlying state mathematics is parent-owned. The standalone case rests on the usefulness and distinctness of the **assessment task**, not on renaming causal states, decision states, information states, rate-distortion theory or finite-state minimization.

## 11. Conclusion

A representation can be adequate for a registered language-prediction target and the exact decision required today while remaining inadequate for a decision that becomes distinguishable only after evidence changes.

The complete one-step compatibility theorem identifies the missing condition: every representation/evidence cell must admit at least one future action acceptable for all histories it merges. The one-bit provenance construction shows that current sufficiency does not guarantee this condition, even when the current action is unique.

The Prospective Revision Audit turns the gap into an evaluation procedure. It first establishes current equivalence, then tests whether a historical distinction was genuinely removed rather than retained or reconstructed elsewhere, supplies the same later evidence and scores both correct updating and correct maintaining or selective reopening.

Existing state theories remain the mathematical parents. The proposed advance is to treat **future evidence-triggered revision as a separate representation-assessment axis after current behavior has already been matched**.

For long-lived language models and agents, that produces a concrete evaluation question:

> When later evidence changes what should be done, did the retained representation preserve—or make reliably reconstructable—the distinctions required to change the right commitments and leave the others intact?

## Reproducibility and AI-assistance statement

The core finite claims have human-readable proofs and deterministic executable audit artifacts. The computational package includes exhaustive finite partition checks, independent constructions of dynamic state, registered counterexamples and assumption-mutation tests. No LLM training or empirical hidden-state benchmark is required for the theorem.

Large language model systems were used extensively as research-assistance tools for literature discovery, formalization, adversarial critique, software generation and manuscript drafting/editing. AI systems are not authors. Human authors must review and adopt the final scientific claims, proofs, citations and reported mechanical evidence and take responsibility for the released work.
