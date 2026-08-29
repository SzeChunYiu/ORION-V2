# Proof Appendix V1 — Prospective Revision Audit

**Issue:** #51  
**Status:** human-readable finite/discrete proofs for the claims that remain in Manuscript V5.  
**Role of mechanical execution:** independent exact validation/countermodel search; it does not replace these proofs.  
**Novelty boundary:** several lemmas below are elementary or parent-owned. They are included for self-containment, not claimed as original mathematics.

---

# A. Setup

Let `H` be a finite random variable with positive-probability support `supp(H)`. Let `S_P=s_P(H)` be the declared linguistic predictive reference state. The predictive-state construction/minimality is parent-owned and not reproved here except where needed for a local corollary.

A responsibility contract defines, for each history `h`, a nonempty finite set of Bayes-optimal admissible actions

\[
A^*(h)\subseteq \mathcal A.
\]

For `ANY_OPTIMAL_ACTION` semantics, an **acceptable selector** is any deterministic map

\[
d:\operatorname{supp}(H)\to\mathcal A
\]

such that

\[
d(h)\in A^*(h)
\qquad\forall h\in\operatorname{supp}(H).
\]

Let `\mathcal D` be the set of all acceptable selectors.

A partition `\Pi` of `supp(H)` is **static-admissible** when:

1. every block lies within a single `S_P` fibre; and
2. for every block `B\in\Pi`,
   \[
   \bigcap_{h\in B}A^*(h)\neq\varnothing.
   \]

Let `\Pi(H)` denote the block label of history `H`.

Define

\[
C_{\mathrm{stat}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{stat}}}
H(\Pi(H)\mid S_P).
\]

Equivalently we will show

\[
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}H(d(H)\mid S_P).
\]

For the dynamic problem, let `\delta(h,x)` be a deterministic partial successor map for registered future observation/input `x`.

A static-admissible partition is **dynamic-admissible** when, for all histories `h,h'` in the same block and every registered input `x`:

1. `\delta(h,x)` is defined iff `\delta(h',x)` is defined; and
2. when defined, `\delta(h,x)` and `\delta(h',x)` lie in the same partition block.

Let `\mathfrak P_{\mathrm{dyn}}` be the dynamic-admissible partitions and define

\[
C_{\mathrm{dyn}}^*
=
\min_{\Pi\in\mathfrak P_{\mathrm{dyn}}}
H(\Pi(H)\mid S_P).
\]

For a fixed acceptable selector `d`, let `B_d=(S_P,d)` be its present predictive-policy label and let `S_\infty^d` denote the coarsest right-congruent refinement of `B_d` under the registered deterministic transitions. Existence is automatic in the finite setting because repeated partition refinement must terminate.

---

# B. Static selector/partition equivalence

## Proposition B.1

In the finite `ANY_OPTIMAL_ACTION` setting,

\[
\boxed{
C_{\mathrm{stat}}^*
=
\min_{d\in\mathcal D}H(d(H)\mid S_P)
}
\]

where entropy is evaluated on positive-probability support.

### Proof

We prove both inequalities.

### Selector -> admissible partition

Fix any acceptable selector `d\in\mathcal D`. Partition the support by the joint label

\[
(S_P(h),d(h)).
\]

Every block lies inside one `S_P` fibre. Moreover, `d(h)` is the same action `a` throughout a block and, because `d` is acceptable,

\[
a\in A^*(h)
\]

for every history in the block. Hence the intersection of the optimal-action sets in the block contains `a`, so the partition is static-admissible.

Its conditional entropy is exactly

\[
H(S_P,d\mid S_P)=H(d\mid S_P).
\]

Therefore

\[
C_{\mathrm{stat}}^*
\le
\min_{d\in\mathcal D}H(d\mid S_P).
\]

### Admissible partition -> selector

Now fix any static-admissible partition `\Pi`. For each block `B`, choose one action

\[
a_B\in\bigcap_{h\in B}A^*(h),
\]

which exists by admissibility. Define

\[
d_\Pi(h)=a_B
\quad\text{for }h\in B.
\]

Then `d_\Pi` is an acceptable selector.

Because `\Pi` refines `S_P`, and because `d_\Pi` is constant on every `\Pi` block, the joint label `(S_P,d_\Pi)` is a deterministic function of `\Pi`. Therefore conditioning on `S_P`,

\[
H(d_\Pi\mid S_P)
\le
H(\Pi\mid S_P).
\]

Taking the minimum over admissible partitions gives

\[
\min_{d\in\mathcal D}H(d\mid S_P)
\le
C_{\mathrm{stat}}^*.
\]

The two inequalities establish equality. ∎

### Ownership note

The compatibility/decision-sufficiency idea is classical. The proposition is retained because it makes the paper's conditional accounting convention explicit.

---

# C. Zero-cost current responsibility criterion

## Corollary C.1

\[
\boxed{
C_{\mathrm{stat}}^*=0
}
\]

if and only if there exists an acceptable selector `d` that is almost surely a deterministic function of `S_P`.

Equivalently, for every positive-probability predictive fibre `F_s`,

\[
\bigcap_{h\in F_s}A^*(h)\neq\varnothing.
\]

### Proof

By Proposition B.1,

\[
C_{\mathrm{stat}}^*=0
\iff
\exists d\in\mathcal D:
H(d\mid S_P)=0.
\]

For finite random variables, `H(d|S_P)=0` iff `d` is almost surely a function of `S_P`.

Such a selector exists exactly when, inside every predictive fibre, one action is Bayes-optimal for every history in that fibre. ∎

### Interpretation

This is the mandatory P0/Brodu-like control. If the current responsibility can already be implemented from the linguistic predictive state, the framework assigns **zero** additional current state.

---

# D. Dynamic partition / selector-refinement equivalence

## Proposition D.1

In the registered finite deterministic setting,

\[
\boxed{
C_{\mathrm{dyn}}^*
=
\min_{d\in\mathcal D}
H(S_\infty^d\mid S_P)
}
\]

where `S_\infty^d` is the coarsest right-congruent refinement of `(S_P,d)`.

### Proof

Again prove both inequalities.

### Fixed selector -> feasible dynamic state

For any acceptable selector `d`, `S_\infty^d` refines `(S_P,d)` by construction and is right-congruent. Therefore each block lies inside one `S_P` fibre and has constant chosen action `d`, which is optimal for every history in the block. Hence `S_\infty^d` is dynamic-admissible.

Thus

\[
C_{\mathrm{dyn}}^*
\le
H(S_\infty^d\mid S_P)
\]

for every `d`, and therefore

\[
C_{\mathrm{dyn}}^*
\le
\min_d H(S_\infty^d\mid S_P).
\]

### Dynamic partition -> fixed selector refinement

Now let `\Pi` be any dynamic-admissible partition. Choose one common optimal action `a_B` per block and form the acceptable selector `d_\Pi` exactly as in Proposition B.1.

Then `\Pi` refines `(S_P,d_\Pi)`. It is also right-congruent. Since `S_\infty^{d_\Pi}` is by definition the **coarsest** right-congruent refinement of `(S_P,d_\Pi)`, `\Pi` must refine `S_\infty^{d_\Pi}`.

Therefore

\[
H(S_\infty^{d_\Pi}\mid S_P)
\le
H(\Pi\mid S_P).
\]

Taking the minimum over dynamic-admissible `\Pi`,

\[
\min_d H(S_\infty^d\mid S_P)
\le
C_{\mathrm{dyn}}^*.
\]

Combining inequalities proves the result. ∎

### Ownership note

The right-congruent/closed-cover minimization substrate is classical and has strong direct current parents. The proposition is a specialization used to validate the two independent computation routes in #51.

---

# E. Dynamic optionality premium

## Proposition E.1

Define

\[
\Omega_{\mathrm{dyn}}
=
C_{\mathrm{dyn}}^*-C_{\mathrm{stat}}^*.
\]

Then

\[
\boxed{\Omega_{\mathrm{dyn}}\ge0}.
\]

### Proof

Every dynamic-admissible partition is, by definition, static-admissible. Therefore

\[
\mathfrak P_{\mathrm{dyn}}
\subseteq
\mathfrak P_{\mathrm{stat}}.
\]

Minimizing the same objective over the smaller feasible set cannot produce a smaller value:

\[
C_{\mathrm{dyn}}^*
\ge
C_{\mathrm{stat}}^*.
\]

Subtract. ∎

### Ownership note

This is a nested-feasible-set inequality, not a new theorem. `Omega_dyn` is kept only as a useful derived audit coordinate.

---

# F. One-bit prospective-revision witness

## Proposition F.1

There exists a finite process with

\[
C_{\mathrm{stat}}^*=0,
\qquad
C_{\mathrm{dyn}}^*=1\text{ bit},
\qquad
\Omega_{\mathrm{dyn}}=1\text{ bit},
\]

while the current Bayes-optimal action is unique.

### Construction

Let the present history variable be equiprobable on two states:

\[
H_0\in\{h_A,h_B\},
\qquad
P(h_A)=P(h_B)=\tfrac12.
\]

Let both histories share one linguistic predictive reference state:

\[
S_P(h_A)=S_P(h_B)=s.
\]

Let the current responsibility have one unique optimal action `RETAIN` in both histories:

\[
A^*(h_A)=A^*(h_B)=\{\text{RETAIN}\}.
\]

Hence one static block `{h_A,h_B}` is action-compatible, so

\[
C_{\mathrm{stat}}^*=0.
\]

Now introduce a registered future observation `x=RETRACT(A)` with deterministic successors

\[
\delta(h_A,x)=h_A',
\qquad
\delta(h_B,x)=h_B'.
\]

At the successors, let the unique optimal future actions differ:

\[
A^*(h_A')=\{\text{REOPEN}\},
\qquad
A^*(h_B')=\{\text{RETAIN}\}.
\]

### Dynamic lower bound

A dynamic-admissible partition cannot put `h_A` and `h_B` in the same block. If it did, right congruence under `x` would require `h_A'` and `h_B'` to remain in one block, but no dynamic/static admissible block may contain successor histories with disjoint unique optimal-action sets.

Thus the two equiprobable histories must occupy different dynamic-state classes. Since `S_P` is constant,

\[
C_{\mathrm{dyn}}^*
\ge
H(H_0)=1\text{ bit}.
\]

### Achievability

Retain the one-bit source/provenance distinction, i.e. use separate state classes for `h_A` and `h_B`. The state then updates deterministically under `x` and supports the correct successor actions. Hence

\[
C_{\mathrm{dyn}}^*=1\text{ bit}.
\]

Subtracting `C_stat^*=0` gives `Omega_dyn=1` bit. ∎

### Why unique current action matters

There is no choice among current optimal actions, so the prospective premium cannot be an artefact of a poor tie-breaking policy.

---

# G. Present adequacy does not certify revision adequacy

## Theorem G.1 — no-certification theorem for the registered finite process class

There exist two representations `Z_c` and `Z_a` of the same initial histories such that:

1. both are equally sufficient for the declared linguistic predictive target;
2. both support the same Bayes-optimal current responsibility action with zero current regret;
3. after the same registered future evidence, their achievable future responsibility risks differ.

Therefore no assessment based **only** on the first two properties can certify prospective revision adequacy over a process class containing this construction.

### Proof

Use Proposition F.1.

Let the compressed representation be

\[
Z_c=S_P,
\]

which is constant on `h_A,h_B`.

Let the augmented representation be

\[
Z_a=(S_P,B),
\]

where `B` is the one-bit provenance variable distinguishing `A` from `B`.

By construction, the provenance bit does not change the declared linguistic predictive target, so both representations are equally adequate for language prediction.

Before the future observation, the unique current optimal action is `RETAIN` for both histories, so both representations have identical zero-regret current decision performance.

After `RETRACT(A)`, `Z_a` retains enough information to distinguish the two initial support paths and therefore choose `REOPEN` for the `A` history and `RETAIN` for the `B` history.

`Z_c` maps both initial histories to the same state. Given the same future observation and no other information that reconstructs the provenance bit, any future decision rule based only on `(Z_c,x)` must take the same action for both histories. Since the required actions differ, it incurs positive error/risk on at least one positive-probability history.

Thus present linguistic and decision adequacy are equal while prospective revision adequacy differs. Any test observing only the first two properties has identical observations on `Z_c` and `Z_a` and therefore cannot certify which prospective property holds. ∎

### Scope

This is an **existence / logical non-certification** theorem. It does not say real LLMs instantiate the compressed representation.

---

# H. Horizon monotonicity

Let `\mathfrak P_k` be the static-admissible partitions that preserve compatibility for every registered jointly feasible input word of length at most `k`. Define

\[
C_k^*
=
\min_{\Pi\in\mathfrak P_k}H(\Pi(H)\mid S_P).
\]

## Proposition H.1

\[
\boxed{
C_0^*\le C_1^*\le C_2^*\le\cdots
}
\]

### Proof

Every partition valid through horizon `k+1` is also valid through horizon `k`, hence

\[
\mathfrak P_{k+1}\subseteq\mathfrak P_k.
\]

The objective is unchanged, so its minimum is nondecreasing as the feasible set shrinks. ∎

## Proposition H.2 — finite stabilization

In a finite history/state system with a finite registered transition alphabet, the iterated partition refinement stabilizes after finitely many strict refinements.

### Proof

A partition of an `n`-element support can be strictly refined only finitely many times; for example, each strict refinement increases the number of blocks and there are at most `n` blocks. The registered refinement operator never coarsens the partition. Therefore some finite iteration is a fixed point. ∎

### Ownership note

Finite monotone refinement and stable right congruence are parent-owned state-minimization facts. The paper uses `C_k^*` as an audit curve.

---

# I. Responsibility-family upper bound

Let `C_\mathcal R(H)` be any deterministic registered responsibility signature derived from history.

## Proposition I.1

\[
0
\le
H(C_\mathcal R\mid S_P)
\le
H(H\mid S_P).
\]

### Proof

Nonnegativity is standard. Since `C_\mathcal R` is a deterministic function of `H`, the conditional data-processing/entropy inequality gives

\[
H(C_\mathcal R\mid S_P)
\le
H(H\mid S_P).
\]

∎

## Proposition I.2 — saturation by a fibre-separating family

If `(S_P,C_\mathcal R)` uniquely determines `H` on positive-probability support, then

\[
H(C_\mathcal R\mid S_P)=H(H\mid S_P).
\]

### Proof

Because `C_\mathcal R` is a deterministic function of `H`,

\[
H(H,C_\mathcal R\mid S_P)=H(H\mid S_P).
\]

If `(S_P,C_\mathcal R)` determines `H`, then

\[
H(H\mid S_P,C_\mathcal R)=0.
\]

By the conditional chain rule,

\[
H(H,C_\mathcal R\mid S_P)
=
H(C_\mathcal R\mid S_P)
+
H(H\mid S_P,C_\mathcal R),
\]

which yields equality. ∎

### Ownership note

This is elementary conditional entropy. It is a bounded-responsibility warning, not a novelty claim.

---

# J. Every non-injective state fails some exact binary responsibility

## Proposition J.1

Let `Z=f(H)` be non-injective on positive-probability support. Then there exists a deterministic binary target/responsibility `Q=q(H)` that cannot be recovered with zero error from `Z`.

### Proof

Because `Z` is non-injective, there exist distinct positive-probability histories `h_0,h_1` with

\[
f(h_0)=f(h_1).
\]

Define

\[
q(h_0)=0,
\qquad
q(h_1)=1,
\]

and assign arbitrary binary values to all other histories.

Any decoder using only `Z` must give the same output distribution/decision at `h_0` and `h_1`, because they share the same `Z` value. It therefore cannot be exactly correct at both histories. ∎

### Ownership note

This is a trivial fibre argument. It remains in the paper only to rule out unbounded claims of universal responsibility sufficiency.

---

# K. Information-deficit identities

For a representation `Z` generated from `H` and a target `Q`,

\[
H(Q\mid Z)-H(Q\mid H)
=
I(Q;H\mid Z)
\]

because `Q-H-Z` and hence `H(Q|H,Z)=H(Q|H)`.

For a new observation `X`,

\[
H(Q\mid Z)-H(Q\mid Z,X)
=
I(Q;X\mid Z).
\]

For future target `Q_{t+k}` and future evidence `X_{1:k}`, define the prospective information lost from current representation as

\[
I(Q_{t+k};H_t\mid Z_t,X_{1:k}).
\]

These are standard information identities. Their only role is to keep acquisition, current compression, and prospective revision loss distinct.

---

# L. Mutation-derived assumption boundaries

The registered mechanical mutation audit supplies counterexamples/robustness checks that refine the prose scope of the predictive-compression background lemma:

1. **Entropy minimality is load-bearing** for selecting an isomorph of the minimal predictive state; sufficiency alone permits refinements.
2. **Positive-probability support is load-bearing**; arbitrary labels assigned only to zero-mass nominal histories are unconstrained by predictive loss.
3. **Near-minimal entropy does not imply structural closeness** without additional assumptions.
4. The exact entropy floor has robust variants under the registered approximate and stochastic relaxations.
5. Cardinality- and entropy-minimality coincide on the registered exact deterministic lattice, but the paper does not elevate that finite audit into a universal continuous-state theorem.

These boundaries should be stated near the relevant background lemma rather than hidden in an appendix receipt.

---

# M. Proof / parent classification summary

| Result | Proof status | Novelty status |
|---|---|---|
| static selector/partition equality | proved + mechanically checked | specialization / parent substrate |
| zero-current-cost criterion | proved + checked | decision-sufficiency corollary |
| dynamic selector/refinement equality | proved + checked | parent-substrate specialization |
| `Omega_dyn >= 0` | proved + checked | derived metric property |
| one-bit witness | constructive proof + exact receipt | #51 known-answer witness |
| present adequacy cannot certify future revision | proved from witness | strongest formal support for assessment task |
| horizon monotonicity/stabilization | proved + checked | parent-style refinement, audit interpretation only |
| family overhead bound/saturation | proved + checked | elementary/classical boundary |
| noninjective representation fails some binary target | proved + checked | elementary fibre boundary |
| information deficits | standard identities + checked | parent-owned |

The load-bearing **paper contribution is Theorem G.1 as the justification for a new assessment coordinate/protocol**, not a claim that the supporting state-minimization lemmas are novel.
