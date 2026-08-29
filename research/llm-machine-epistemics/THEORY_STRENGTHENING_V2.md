# Theory Strengthening V2 — Dynamic Epistemic State and Exact Frontiers

**Issue:** #51  
**Status:** conceptual/mathematical strengthening prepared before independent mechanization.  
**Purpose:** remove open-ended mathematical invention from the execution handoff. The remaining AI should verify/falsify these statements mechanically; it should not invent the theory after seeing outcomes.

This file strengthens `THEORY_V1.md` in two directions:

1. solve the simplest approximate predictive–epistemic log-loss frontier analytically, while explicitly attributing the rate-distortion identity to classical information theory;
2. add a **sequential / recursively updateable epistemic state** theory. Static sufficiency can be inadequate for an autoregressive model because a distinction irrelevant to today's prediction and responsibility may be necessary for tomorrow's revision after a new observation.

---

# Part I — Exact approximate frontier under log loss

## 1. Setup

Let `H` be finite, `S=S_P(H)` the exact minimal linguistic predictive state, and let `Q=q(H)` be a deterministic epistemic responsibility. The representation is allowed to retain `S` exactly and add a stochastic augmentation `U` generated from `H`.

We measure extra state rate by

\[
R=I(H;U\mid S),
\]

and responsibility loss by Bayes log loss

\[
D=H(Q\mid S,U).
\]

Since `Q` is deterministic from `H`, `H(Q|H)=0`, so `D` is also the epistemic deficiency under log loss.

Define

\[
R_{\mathrm{epi}}(D)
=
\inf_{p(u|h):\,H(Q|S,U)\le D}
I(H;U\mid S).
\]

The linguistic predictive state remains available exactly; therefore this frontier measures **additional representation beyond perfect linguistic prediction**.

## Theorem 8A — exact conditional log-loss frontier

For

\[
0\le D\le H(Q\mid S),
\]

\[
\boxed{
R_{\mathrm{epi}}(D)
=
H(Q\mid S)-D
}
\]

and for `D >= H(Q|S)`, `R_epi(D)=0`.

### Lower bound

Because `Q` is a function of `H`, conditioned on `S` we have the Markov chain

\[
U-H-Q.
\]

Hence

\[
I(H;U\mid S)
\ge
I(Q;U\mid S)
=
H(Q\mid S)-H(Q\mid S,U)
\ge
H(Q\mid S)-D.
\]

### Achievability

Let `B~Bernoulli(alpha)` be independent of `(H,Q,S)` and define the erasure augmentation

\[
U=
\begin{cases}
Q,& B=1,\\
\bot,& B=0.
\end{cases}
\]

When erased, `U` leaves the conditional law of `Q` given `S` unchanged; when revealed, the responsibility is exact. Therefore

\[
H(Q\mid S,U)=(1-\alpha)H(Q\mid S),
\]

and because `U` depends on `H` only through `Q`,

\[
I(H;U\mid S)=I(Q;U\mid S)=\alpha H(Q\mid S).
\]

Choose

\[
\alpha=1-\frac{D}{H(Q\mid S)}.
\]

Then the lower bound is attained. ∎

### Novelty boundary

The linear rate-distortion form under logarithmic loss is classical. Courtade–Weissman and the broader log-loss rate-distortion literature own the information-theoretic identity. #51 must **not** claim Theorem 8A as a new rate-distortion law.

Its role is to make the epistemic-state framework complete and to provide a closed-form benchmark for later stronger responsibility constraints.

---

# 2. Multiple typed responsibilities

Let

\[
Q=(Q_1,\ldots,Q_m)
\]

be deterministic from `H`. Require separate non-compensatory log-loss constraints

\[
H(Q_i\mid S,U)\le D_i.
\]

Define

\[
R_{\mathrm{epi}}(D_1,\ldots,D_m)
=
\inf I(H;U\mid S)
\]

over stochastic augmentations satisfying every coordinate constraint.

## Theorem 8B — exact independent-responsibility frontier

If `Q_1,...,Q_m` are conditionally independent given `S`, then

\[
\boxed{
R_{\mathrm{epi}}(D_1,\ldots,D_m)
=
\sum_{i=1}^m
\bigl[H(Q_i\mid S)-D_i\bigr]_+
}
\]

for `0<=D_i`.

### Lower bound

Conditional independence gives

\[
H(Q\mid S)=\sum_i H(Q_i\mid S).
\]

Also

\[
H(Q\mid S,U)
\le
\sum_i H(Q_i\mid S,U)
\le
\sum_i D_i.
\]

Therefore

\[
I(H;U\mid S)
\ge I(Q;U\mid S)
=H(Q\mid S)-H(Q\mid S,U)
\ge
\sum_i H(Q_i\mid S)-\sum_iD_i,
\]

with coordinates whose allowed distortion exceeds their baseline entropy contributing zero.

### Achievability

Apply independent erasure channels to the individual `Q_i`, revealing coordinate `i` with probability

\[
\alpha_i=\bigl[1-D_i/H(Q_i\mid S)\bigr]_+.
\]

Conditional independence ensures that revealing other coordinates does not reduce the entropy of an erased coordinate beyond the specified construction, and the rate separates as the sum of coordinate rates. ∎

### Interpretation

Independent typed responsibilities consume additive extra state under separate log-loss guarantees. This is a clean **non-compensatory** benchmark: surplus fidelity on one responsibility cannot pay for missing information on another.

Again, the product-source log-loss mathematics is classical; the use here is structural and diagnostic.

---

# 3. Correlated responsibility sharing

At zero error, the exact joint overhead from `THEORY_V1.md` is

\[
H(Q_1,\ldots,Q_m\mid S),
\]

whereas separately storing every coordinate would cost

\[
\sum_i H(Q_i\mid S).
\]

Define the conditional responsibility redundancy

\[
\mathcal R_{\mathrm{shared}}
=
\sum_i H(Q_i\mid S)
-
H(Q_1,\ldots,Q_m\mid S).
\]

This is the conditional total correlation / redundancy available for shared state.

## Corollary 8C — shared exact-state saving

The exact average-state saving from one joint responsibility representation rather than separately optimal coordinate representations is

\[
\boxed{
\mathcal R_{\mathrm{shared}}
}
\]

bits on average.

This prevents an ORION-style vector state from being misread as requiring the sum of all coordinate costs. Typed responsibilities can remain logically non-compensatory while still **sharing representation bits** when statistically dependent.

## Marginal cost identity

For any ordering of deterministic responsibilities,

\[
H(Q_1,\ldots,Q_m\mid S)
=
\sum_{i=1}^m
H(Q_i\mid S,Q_1,\ldots,Q_{i-1}).
\]

Thus the exact marginal state cost of adding responsibility `Q_i` after an already retained family `A` is

\[
\boxed{
\Delta C_i=H(Q_i\mid S,Q_A)
}
\]

under that declared order/family.

This gives a precise redundancy test: a new responsibility costs zero exact average state iff it is already recoverable from the predictive state plus the retained responsibility family.

---

# 4. Worst-case and cardinality state cost

Average entropy is not the only useful internal-state cost.

For deterministic `Q`, define for every predictive state `s`

\[
k_s=|\mathrm{supp}(Q\mid S=s)|.
\]

## Theorem 8D — minimum exact joint-state cardinality

The coarsest deterministic state sufficient for both `S` and exact `Q` has

\[
\boxed{
|S_{PE}|=\sum_s k_s
}
\]

reachable state values.

If `S` is stored separately and `U` is only an augmentation, then the minimum augmentation alphabet size is

\[
\boxed{
|\mathcal U|_{\min}=\max_s k_s
}
\]

because within each predictive fibre distinct `Q` values must receive distinct augmentation labels, while the same labels may be reused across different predictive states.

Therefore a fixed-width exact augmentation requires

\[
\boxed{
\lceil\log_2 \max_s k_s\rceil
}
\]

bits in the worst case.

### Interpretation

`H(Q|S)` is the average exact epistemic overhead; `log max_s k_s` is a worst-fibre representational overhead. The distinction is useful when an architecture has a fixed state-width constraint rather than an entropy-coded average budget.

---

# Part II — Static epistemic sufficiency is not enough for a sequential model

The strongest conceptual gap in `THEORY_V1.md` is that it treats the responsibility at one time slice. An autoregressive model must update its internal state after new observations.

A distinction can be irrelevant to:

- the current linguistic future distribution;
- the current responsibility value;

and nevertheless be necessary to compute a **future responsibility after a new observation**.

This motivates **dynamic epistemic sufficiency**.

---

# 5. Finite history-transition model

Let `\mathcal H` be a finite set of admissible histories with a partial extension operation

\[
(h,x)\mapsto hx
\]

for symbols/observations `x` in finite alphabet `\mathcal X`.

Let the current required output label be

\[
B(h)=(S_P(h),Q(h)),
\]

where `Q(h)` may itself be a vector of deterministic current responsibilities.

The **static joint state** is the partition induced by equality of `B`.

A recursively updateable internal state is a map

\[
R:\mathcal H\to\mathcal R
\]

for which:

1. `B(h)` is recoverable from `R(h)`;
2. there exists a deterministic update function `\delta` such that whenever `hx` is admissible,

\[
R(hx)=\delta(R(h),x).
\]

This is the exact finite-state online-update requirement.

---

# 6. Right-congruence refinement

Define equivalence relations recursively.

### Horizon 0

\[
h\equiv_0 h'
\iff
B(h)=B(h').
\]

### Horizon `k+1`

\[
h\equiv_{k+1}h'
\]

iff:

1. `B(h)=B(h')`; and
2. for every symbol `x`, either both extensions are inadmissible, or both are admissible and

\[
hx\equiv_k h'x.
\]

Let `S_k=[H]_{\equiv_k}`.

For finite `\mathcal H`, repeated refinement eventually stabilizes. Call the stable partition

\[
S_\infty.
\]

---

# 7. T10 — horizon monotonicity and finite stabilization

## Theorem 10

For all `k`,

\[
\equiv_{k+1}\subseteq\equiv_k,
\]

so `S_{k+1}` refines `S_k`. Consequently, under any distribution over histories,

\[
H(S_{k+1})\ge H(S_k).
\]

Because the history set is finite, the refinement stabilizes after finitely many strict partition splits; in particular, no more than `|\mathcal H|-|S_0|` class-splitting events are possible.

### Interpretation

Increasing the horizon of future epistemic obligations can only increase or preserve the required internal-state information. It cannot make a previously necessary distinction disappear at the same time slice.

Define the finite-horizon optionality cost

\[
C_{\mathrm{opt}}(k)
=
H(S_k)-H(S_0)
=
H(S_k\mid S_0).
\]

This is the additional state needed solely to preserve correct future update possibilities beyond current static sufficiency.

---

# 8. T11 — stable refinement is the coarsest recursively updateable state

A relation `\approx` on histories is a right congruence if

\[
h\approx h'
\implies
hx\approx h'x
\]

for every jointly admissible symbol extension, with admissibility/undefinedness preserved.

## Theorem 11 — coarsest right-congruent refinement

`\equiv_\infty` is the **coarsest right congruence refining `\equiv_0`**.

### Proof sketch

At stabilization, equality of current labels is preserved and equivalent histories have equivalent successors under every symbol, hence `\equiv_\infty` is a right congruence.

Now let `\approx` be any right congruence refining `\equiv_0`. By induction on `k`, if `h\approx h'`, then `h\equiv_kh'`:

- base: refinement of `\equiv_0`;
- induction: right congruence gives `hx\approx h'x`; the induction hypothesis gives successor `\equiv_k`; therefore `h\equiv_{k+1}h'`.

Thus every admissible recursively stable relation is finer than every finite-horizon refinement and therefore finer than the stabilized relation. ∎

### Parent boundary

The underlying mathematics is closely related to Myhill–Nerode/right-congruence theory, deterministic automaton minimization, bisimulation/partition refinement and recursively calculable causal states. #51 must explicitly cite these parents and cannot claim right congruence itself as a new theorem.

The proposed residual is its use to define **future epistemic responsibility optionality cost inside autoregressive internal state**.

---

# 9. T12 — recursive implementability theorem

## Theorem 12

A deterministic internal state `R(h)` can both recover `B(h)` and update recursively from `(R(h),x)` only if its kernel equivalence

\[
h\sim_Rh'\iff R(h)=R(h')
\]

is a right-congruent refinement of `\equiv_0`.

Therefore every such `R` must refine `S_\infty`, and

\[
H(R)\ge H(S_\infty).
\]

Conversely, the stable state `S_\infty` itself admits a well-defined deterministic update and recovers `B`.

Hence:

\[
\boxed{
S_\infty
=\text{the minimal exact recursively updateable predictive–epistemic state}
}
\]

up to state relabelling/isomorphism.

### Exact dynamic overhead

Because the static state `S_0` is a function of `S_\infty`, the minimum additional average state needed for **future update correctness** beyond current static sufficiency is

\[
\boxed{
C_{\mathrm{dyn}}
=H(S_\infty\mid S_0)
=H(S_\infty)-H(S_0)
}
\]

and can be strictly positive.

This is the central sequential strengthening.

---

# 10. T13 — static sufficiency can have zero cost while dynamic sufficiency has positive cost

## Canonical witness

Let current histories be `h_0,h_1`, each with probability `1/2`, encoding a hidden provenance bit `A in {0,1}`.

At the current time:

- both histories induce the same complete linguistic-future law;
- current responsibility `Q_0` is identical on both histories.

Therefore

\[
S_0(h_0)=S_0(h_1)
\]

and the **static** epistemic overhead beyond linguistic prediction is zero.

Now let one future observation symbol `x` occur, and define the future responsibility after extension by

\[
Q_1(h_ax)=a.
\]

Then the two successor histories require different responsibility outputs. Consequently the horizon-1 refinement separates `h_0` and `h_1`:

\[
S_1(h_0)\neq S_1(h_1).
\]

Under the equal prior,

\[
C_{\mathrm{opt}}(1)=1\text{ bit}.
\]

### Interpretation

The past bit `A` has:

- zero current linguistic prediction value;
- zero current responsibility value;
- **positive future epistemic option value**.

Compressing it away is harmless under a static objective yet makes correct future revision impossible.

A concrete Machine-Epistemics reading is provenance/defeater memory: the identity of a source may not change today's answer, but when a future retraction or contradiction arrives, the system must know which commitments depended on that source.

---

# 11. Dynamic safety criterion

The static compression to `S_0` is dynamically safe iff `\equiv_0` is already a right congruence. Equivalently:

\[
\boxed{
C_{\mathrm{dyn}}=0
\iff
S_0=S_\infty
}
\]

up to isomorphism.

This is a stronger criterion than

\[
H(Q\mid S_P)=0,
\]

which tests only current responsibility recoverability.

A representation can therefore be:

1. linguistically sufficient;
2. currently responsibility-sufficient;
3. yet **dynamically epistemically insufficient**.

This three-way distinction should become central to the paper if the nearest-work audit confirms a residual.

---

# 12. Horizon-relative state law

The sequence

\[
S_0\preceq S_1\preceq\cdots\preceq S_\infty
\]

provides a responsibility-horizon state-complexity curve

\[
C(k)=H(S_k).
\]

Candidate theoretical questions that are now fully specified for mechanical study:

- rate of stabilization;
- maximum number of strict refinements;
- relation between `C(k)` and future responsibility horizon;
- approximate/lossy versions using responsibility error instead of exact labels;
- compression phase boundaries when future responsibilities have expiry times.

No execution AI should invent these objects; it should compute them on the registered finite families and test the stated theorems/counterexamples.

---

# 13. Revised candidate headline

If T10–T13 survive strongest-parent subtraction, the paper should no longer be framed only as a static state-overhead result.

A stronger headline is:

> **Prediction-sufficient state can fail twice:** it can omit information needed for a current epistemic responsibility, and even a state sufficient for both current prediction and current responsibility can omit information required for correct future epistemic revision. The first cost is quantified by responsibility information such as `H(Q|S_P)` in the exact deterministic case; the second is the entropy of the coarsest right-congruent refinement needed for recursive update.

This connects information-theoretic sufficiency to a genuinely sequential internal-state property of autoregressive systems.

---

# 14. Updated novelty pressure

The final external theorem matrix must now include additional parents:

- Myhill–Nerode theorem and deterministic automaton minimization;
- Moore/Hopcroft partition refinement;
- bisimulation / right congruence;
- recursively calculable causal states in computational mechanics;
- predictive-state and reward-predictive-state update theory;
- finite-state filters / sufficient information states in control and POMDPs;
- dynamic sufficient statistics / belief-state recursion;
- truth-maintenance / belief-revision systems where provenance is retained for future retraction.

The paper earns a dynamic theorem residual only if the **responsibility-horizon / optionality-cost formulation and LLM-internal consequence** are not already fully contained in one strongest parent.

---

# 15. What remains mechanical after V2

The executor is not asked to create new mathematics. It must only:

1. formally verify T8A–T8D and T10–T13;
2. generate finite counterexamples when any omitted assumption matters;
3. run exact partition refinement and entropy calculations on registered small systems;
4. check that the canonical dynamic witness returns zero static overhead and one bit horizon-1 overhead;
5. search nearest work for direct theorem collisions;
6. contract claims if a parent owns them.
