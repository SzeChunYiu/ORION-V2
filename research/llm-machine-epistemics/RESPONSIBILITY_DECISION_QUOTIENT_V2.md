# Responsibility Decision Quotient V2 — Exact Action Semantics

**Issue:** #51  
**Supersedes:** `RESPONSIBILITY_DECISION_QUOTIENT_V1.md` wherever optimal-action ties occur.  
**Purpose:** remove an over-strong state requirement in V1. Preserving the *entire set* of Bayes-optimal actions is not necessary when a responsibility contract only requires the system to choose **some** Bayes-optimal action. The exact minimal state cost depends on the contract's decision semantics.

---

# 1. Responsibility contract with explicit decision semantics

A finite epistemic responsibility contract is

\[
r=(Q,\mathcal A,\ell,\sigma),
\]

where:

- `Q` is the epistemic target/state;
- `\mathcal A` is the admissible action/terminal set;
- `\ell(a,q)` is the registered loss;
- `\sigma` declares what must be preserved about the Bayes decision.

For history `h`, define the Bayes-optimal action set

\[
A_r^*(h)
=
\operatorname*{argmin}_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

and Bayes risk value

\[
\rho_r(h)
=
\min_{a\in\mathcal A}
\mathbb E[\ell(a,Q)\mid H=h].
\]

The contract must choose one of the following exact semantics.

## `ANY_OPTIMAL_ACTION`

The internal state only needs to support a decoder that returns **one** Bayes-optimal action for every history.

## `CANONICAL_ACTION`

The contract supplies a deterministic tie rule `\tau` and requires

\[
d_r^\tau(h)=\tau(A_r^*(h)).
\]

This is appropriate when the operational protocol requires a particular deterministic terminal under ties.

## `OPTIMAL_ACTION_SET`

The complete Bayes-optimal set `A_r^*(h)` must be recoverable. This is stronger than merely acting with zero Bayes regret and should be used only when preserving option sets is itself part of the responsibility.

## `ACTION_AND_RISK`

The registered action semantics plus the Bayes risk value `\rho_r(h)` must be recoverable. This is appropriate when calibrated residual risk/uncertainty is part of the responsibility.

The manuscript must never infer one semantics from another silently.

---

# 2. Exact state sufficiency under `ANY_OPTIMAL_ACTION`

Let `Z=f(H)` be a deterministic representation. It is exact action-sufficient for responsibility `r` iff there exists a deterministic decoder

\[
g:\mathcal Z\to\mathcal A
\]

such that

\[
g(Z(h))\in A_r^*(h)
\]

for every positive-support history `h`.

Equivalently, every fibre `F_z={h:Z(h)=z}` must satisfy

\[
\bigcap_{h\in F_z} A_r^*(h)\neq\varnothing.
\]

A single action chosen from that intersection is valid for the entire fibre.

### Important correction to V1

Equality of optimal-action **sets** is sufficient but not necessary. Two histories can have different optimal sets yet share a common optimal action and therefore require no state distinction under `ANY_OPTIMAL_ACTION`.

Example:

\[
A^*(h_1)=\{a,b\},
\qquad
A^*(h_2)=\{b,c\}.
\]

The sets differ, but action `b` is optimal for both. A state that merges the histories can still act optimally.

---

# 3. Theorem R2.1 — exact minimum action-state entropy

Let `S=S_P` be retained exactly. Define the class of valid Bayes-optimal selectors

\[
\mathcal D_r
=
\left\{
 d:\mathrm{supp}(H)\to\mathcal A
 : d(h)\in A_r^*(h)\ \forall h
\right\}.
\]

For each selector, define action variable

\[
D=d(H).
\]

## Theorem R2.1

Under `ANY_OPTIMAL_ACTION`, the minimum additional average deterministic state entropy beyond `S` is

\[
\boxed{
C_{r,\mathrm{any}}^0(S)
=
\min_{d\in\mathcal D_r}
H(d(H)\mid S).
}
\]

### Lower bound

Take any exact action-sufficient representation `Z` retaining `S`. By definition there is a decoder `g` with `g(Z(h))\in A_r^*(h)`. Let

\[
d(h)=g(Z(h)).
\]

Then `d\in\mathcal D_r`, and `D=d(H)` is a deterministic function of `Z`. Hence

\[
H(D\mid S)
\le
H(Z\mid S).
\]

Therefore every sufficient state has conditional entropy at least the minimum selector entropy.

### Achievability

Choose a selector `d^*` attaining the minimum (finite set) and store

\[
Z=(S,d^*(H)).
\]

The decoder outputs the stored action, which is Bayes-optimal at every history. Its extra conditional state entropy is exactly

\[
H(d^*(H)\mid S).
\]

Thus the lower bound is tight. ∎

### Interpretation

The responsibility-state price is the cheapest Bayes-optimal **policy information** that must be retained beyond the linguistic predictive state, not necessarily the entropy of the posterior, target, or full optimal-action set.

---

# 4. Corollary R2.2 — canonical-action cost

If the responsibility contract specifies a fixed deterministic tie rule `\tau`, then the valid selector is fixed:

\[
d_r^\tau(h)=\tau(A_r^*(h)).
\]

The exact extra average state cost is

\[
\boxed{
C_{r,\tau}^0(S)
=
H(d_r^\tau(H)\mid S).
}
\]

This recovers the simple quotient structure used in V1, but with a **declared** selector rather than the full optimal-action set.

---

# 5. Corollary R2.3 — option-set preservation cost

Under `OPTIMAL_ACTION_SET`, define

\[
O_r(H)=A_r^*(H).
\]

Then the exact extra average state cost is

\[
\boxed{
C_{r,\mathrm{set}}^0(S)
=
H(O_r(H)\mid S).
}
\]

and

\[
C_{r,\mathrm{any}}^0(S)
\le
C_{r,\mathrm{set}}^0(S)
\]

because any preserved action set can be deterministically mapped to an allowed optimal action, while the reverse need not hold.

The inequality can be strict.

---

# 6. Corollary R2.4 — action-and-risk cost

If the contract requires a canonical action `d_r(H)` and Bayes risk value `\rho_r(H)`, define

\[
C_r(H)=(d_r(H),\rho_r(H)).
\]

Then exact additional state cost is

\[
\boxed{
H(C_r(H)\mid S).
}
\]

under the same finite deterministic-state assumptions.

If the risk value is a deterministic function of the canonical action and `S`, it adds zero state; otherwise it has positive marginal cost

\[
H(\rho_r\mid S,d_r).
\]

---

# 7. Exact target recovery remains a special case

If the responsibility contract is to recover `Q` itself exactly, take action space `\mathcal A=\mathcal Q` and zero-one loss

\[
\ell(a,q)=\mathbf 1[a\neq q].
\]

When `Q=q(H)` is deterministic, the unique Bayes-optimal action is `Q`. Therefore

\[
\boxed{
C_{r}^0(S)=H(Q\mid S).
}
\]

The original exact-target overhead theorem is therefore fully retained as a special case.

---

# 8. Family of responsibilities

For responsibilities

\[
\mathcal R=\{r_1,\ldots,r_m\},
\]

state semantics must be specified coordinate-by-coordinate.

## Fixed/canonical signatures

If every responsibility has a fixed exact signature `C_i(H)`—canonical action, action-set, action+risk, or exact target—then the joint cost is

\[
\boxed{
H(C_1,\ldots,C_m\mid S_P).
}
\]

and the marginal cost of adding responsibility `m` is

\[
H(C_m\mid S_P,C_1,\ldots,C_{m-1}).
\]

## Multiple `ANY_OPTIMAL_ACTION` responsibilities

If several responsibilities permit arbitrary optimal selectors, the exact joint state cost is

\[
\boxed{
C_{\mathcal R,\mathrm{any}}^0(S_P)
=
\min_{d_i\in\mathcal D_{r_i}}
H(d_1(H),\ldots,d_m(H)\mid S_P).
}
\]

The selectors should be optimized **jointly**, because correlated action choices can share state.

This is the correct finite exact object for a family of decision responsibilities.

---

# 9. Static zero-cost condition

Under `ANY_OPTIMAL_ACTION`, a responsibility has zero extra state cost beyond `S_P` iff there exists a selector `d\in\mathcal D_r` that is already a deterministic function of `S_P`:

\[
\boxed{
C_{r,\mathrm{any}}^0(S_P)=0
\iff
\exists \bar d:\mathcal S_P\to\mathcal A
\text{ with }
\bar d(S_P(h))\in A_r^*(h)
\ \forall h.
}
\]

Equivalently, every predictive fibre has a nonempty intersection of Bayes-optimal action sets.

This is strictly weaker than requiring all histories in a predictive fibre to have identical optimal-action sets.

---

# 10. Dynamic base state correction

The dynamic theory should use a base representation corresponding to the **registered exact responsibility semantics**.

- `CANONICAL_ACTION`: base label includes the canonical action.
- `OPTIMAL_ACTION_SET`: includes the full set.
- `ACTION_AND_RISK`: includes action plus risk.
- exact target: includes target.
- `ANY_OPTIMAL_ACTION`: there need not be a unique coarsest quotient based only on equality of a pre-existing signature unless an entropy-minimizing selector is fixed.

For the exact finite dynamic theorem, choose one of two routes explicitly:

### Route A — fixed-policy dynamic state

First choose a registered optimal selector `d^*`; define the base label using `d^*`; then compute the coarsest right-congruent refinement. This measures dynamic state required to recursively implement that particular Bayes-optimal policy.

### Route B — joint dynamic-policy minimization

Optimize simultaneously over valid current/future Bayes-optimal policy selectors and recursively updateable state machines. This is a stronger synthesis problem and should **not** be claimed solved by the current right-congruence theorem.

The current #51 main theorem should use **Route A** for rigor unless mechanical work establishes Route B exactly.

---

# 11. Revised responsibility admissibility rule

Every paper example must now specify:

1. epistemic target `Q`;
2. action/terminal space `A`;
3. loss/order `ell`;
4. exact decision semantics:
   - `ANY_OPTIMAL_ACTION`,
   - `CANONICAL_ACTION`,
   - `OPTIMAL_ACTION_SET`,
   - `ACTION_AND_RISK`, or
   - `EXACT_TARGET`;
5. tie policy if canonical action is required;
6. scope/evidence assumptions;
7. future update semantics.

Without item 4, the claimed state overhead is underspecified.

---

# 12. Mechanical checks added

The executor must include:

### Tie-overstatement fixture

Two equally likely histories in one predictive fibre:

\[
A^*(h_1)=\{a,b\},
\quad
A^*(h_2)=\{b,c\}.
\]

Expected:

- `ANY_OPTIMAL_ACTION` minimum overhead = 0 bits (choose `b` for both);
- `OPTIMAL_ACTION_SET` overhead = 1 bit under equal history probabilities;
- a canonical tie rule choosing `a` for first set and `b` for second gives 1 bit;
- a canonical tie rule choosing `b` for both gives 0 bits if the rule is valid/registered accordingly.

### Joint-selector fixture

Construct two responsibilities where independently entropy-minimal selectors are not jointly entropy-minimal, if such a finite witness exists. The executor must search this mechanically; if none occurs under the registered small family, report `CANNOT_CHECK_NO_WITNESS`, not a theorem.

### Exact-target control

Verify deterministic zero-one exact-target responsibility reduces to `H(Q|S_P)`.

---

# 13. Publication consequence

The correction makes the paper stronger conceptually:

> **Epistemic state cost is determined by what the system is responsible for doing, not by every distinction present in a latent label.**

This prevents Machine Epistemics from becoming a mandate to retain all provenance, uncertainty and target detail indiscriminately. A distinction is state-relevant only if it changes the registered epistemic action/risk now or is needed for the registered future update horizon.

The result also increases the connection to classical statistical decision theory; that ownership must be granted explicitly.
