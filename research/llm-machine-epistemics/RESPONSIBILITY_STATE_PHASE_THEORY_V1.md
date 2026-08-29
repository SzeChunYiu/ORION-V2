# Responsibility State Phase Theory V1

**Issue:** #51  
**Purpose:** synthesize the parent-aware theory into a falsifiable three-regime classification and a horizon-indexed state-cost curve. The mathematical ingredients are close to decision-state, compatible-FSM and information-state theory; novelty credit is therefore package/interpretation-level unless the theorem audit proves otherwise.

---

# 1. Primitive objects

Use the setup from `JOINT_DYNAMIC_STATE_OPTIMIZATION_V1.md`:

- finite history set `\mathcal H`;
- complete-linguistic predictive state `S_P`;
- future observation alphabet `\mathcal X` and deterministic partial transition `\delta`;
- Bayes-optimal responsibility action set `A^*(h)` under `ANY_OPTIMAL_ACTION`;
- positive history distribution `p(h)`.

For other exact responsibility semantics, replace `A^*` compatibility with the registered fixed signature equality constraints. The phase theory below is stated for `ANY_OPTIMAL_ACTION` because it is the weakest exact action requirement.

---

# 2. Horizon-k admissible states

## Definition 1 — zero-horizon admissibility

A partition `\Pi` is **0-admissible** iff:

1. it refines `S_P`;
2. every block `B` admits a common Bayes-optimal action:

   \[
   \bigcap_{h\in B}A^*(h)\neq\varnothing.
   \]

This is exactly the static responsibility-admissibility condition.

## Definition 2 — k-horizon consistency

For integer `k>=1`, a partition `\Pi` is **k-admissible** iff it is 0-admissible and, for every block `B`, every two histories `h,h'\in B`, and every input word

\[
w=x_1\cdots x_j,
\qquad 1\le j\le k,
\]

such that sequential extensions are evaluated under `\delta`:

1. definedness of `\delta(h,w)` and `\delta(h',w)` matches;
2. when defined, their successor histories lie in the same `\Pi` block.

Equivalently, the same compressed state plus the same future input word of length at most `k` determines the same compressed successor state.

Let `\mathfrak P_k` be the set of k-admissible partitions.

### Infinite-horizon limit

A partition is dynamically admissible/right-congruent iff it is k-admissible for every finite `k`. In a finite state machine it is sufficient to check the one-step right-congruence condition; repeated application gives all horizons.

---

# 3. Horizon-indexed minimum state cost

Define

\[
\boxed{
C_k^*
=
\min_{\Pi\in\mathfrak P_k}
H(\Pi(H)\mid S_P)
}
\]

for `k=0,1,2,...`, and

\[
C_\infty^*
=
C_{\mathrm{dyn}}^*.
\]

The static cost is

\[
C_0^*=C_{\mathrm{stat}}^*.
\]

Define the horizon-k optionality premium

\[
\boxed{
\Omega_k=C_k^*-C_0^*.
}
\]

and the infinite-horizon premium

\[
\Omega_\infty=\Omega_{\mathrm{dyn}}.
\]

---

# 4. Theorem PH1 — monotone horizon cost

Because

\[
\mathfrak P_{k+1}\subseteq\mathfrak P_k,
\]

we have

\[
\boxed{
C_0^*
\le C_1^*
\le C_2^*
\le\cdots\le C_\infty^*
}
\]

and therefore

\[
\boxed{
0=\Omega_0
\le\Omega_1
\le\Omega_2
\le\cdots\le\Omega_\infty.
}
\]

This is an immediate feasible-set monotonicity result.

### Interpretation

Longer guaranteed future responsibility horizons can only increase or preserve the minimum state needed now. The curve identifies the horizon at which currently dormant distinctions become load-bearing.

---

# 5. Finite stabilization

There are finitely many partitions of `\mathcal H`, and the admissible sets form a nested sequence. Therefore the sequence of minimum costs takes only finitely many values and eventually stabilizes.

Moreover, for a deterministic finite transition system, if a partition satisfies the one-step right-congruence condition it satisfies all horizons. The executor should determine the smallest horizon `k_*` at which

\[
C_k^*=C_\infty^*
\]

for each fixture.

Define

\[
\boxed{
K_{\mathrm{epi}}
=
\min\{k:C_k^*=C_\infty^*\}
}
\]

as the **epistemic memory horizon** of the registered finite responsibility process.

This quantity is finite for every finite fixture, though its interpretation outside finite stationary systems requires caution.

---

# 6. Three exact state phases

The combination of Brodu-like decisional states and #51's cross-channel/dynamic refinements yields three regimes.

## Phase P0 — predictive-decisional sufficiency

\[
\boxed{
C_0^*=0
}
\]

There exists a Bayes-optimal responsibility action that is a function of `S_P` alone.

Equivalent condition: every linguistic-predictive fibre has a common Bayes-optimal responsibility action.

This includes the Brodu-style regime where the decision is determined from the same future distribution represented by the causal/predictive state.

No additional internal state beyond `S_P` is required for the current responsibility.

## Phase P1 — static cross-channel refinement

\[
\boxed{
C_0^*>0,
\qquad
\Omega_\infty=0.
}

The responsibility needs distinctions absent from the linguistic predictive state, but an optimally compressed current responsibility state is already sufficient for all registered future updates.

Examples should be constructed where source identity changes the current epistemic action but future dynamics introduce no additional distinctions.

## Phase P2 — prospective refinement

\[
\boxed{
\Omega_\infty>0.
}

Even after optimally compressing the current responsibility policy, additional state is irreducibly required for future recursive responsibility updates.

P2 may occur with either `C_0^*=0` or `C_0^*>0`.

The canonical provenance witness is

\[
C_0^*=0,
\quad
\Omega_\infty=1\text{ bit}.
\]

---

# 7. Phase witnesses to preregister

The execution package must include one finite exact fixture per phase.

## P0 control

- histories share/differ in ways already resolved by `S_P`;
- every predictive fibre has common optimal action;
- transition is right congruent without extra split.

Expected:

```text
C0=0
Cinf=0
Omega=0
```

## P1 cross-channel static fixture

- one predictive fibre contains histories with disjoint unique current optimal actions due to a provenance/source variable not represented in `S_P`;
- future transitions preserve the resulting current action partition.

Expected:

```text
C0>0
Cinf=C0
Omega=0
```

Choose equal prior binary histories for a simple 1-bit example:

```text
C0=1 bit
Cinf=1 bit
```

## P2 prospective fixture

Canonical one-bit dynamic witness:

```text
C0=0
Cinf=1 bit
Omega=1 bit
```

Also seek a mixed fixture:

```text
C0>0
Omega>0
```

If a minimal 4-state construction is found mechanically, freeze it; otherwise mixed P2 is illustrative/non-load-bearing.

---

# 8. Acquisition as a pre-phase gate

The phase theory concerns information available somewhere in the accessible history.

Before assigning P0/P1/P2 for an exact responsibility target, ask whether the responsibility is identifiable from full `H`.

If

\[
H(Q\mid H)>0
\]

under an exact-target/log-loss interpretation, then the principal blocker is **acquisition/non-identifiability**, and internal state refinement cannot create exact information that history lacks.

Thus a complete diagnostic is:

```text
A0: information absent / acquisition required
or, if accessible:
P0: predictive state enough
P1: static cross-channel refinement needed
P2: prospective refinement needed
```

These are not a total order of “intelligence”; they classify state/information obligations.

---

# 9. Responsibility family growth and phase transitions

For nested responsibility families

\[
\mathcal R_1\subseteq\mathcal R_2\subseteq\cdots,
\]

both static and dynamic state costs can increase.

Define

\[
G_0(\mathcal R)=C_0^*(\mathcal R),
\]

\[
G_\infty(\mathcal R)=C_\infty^*(\mathcal R).
\]

The exact monotonicity under family inclusion is immediate when adding responsibility constraints can only shrink the admissible partition sets.

The executor should verify:

\[
G_0(\mathcal R_1)\le G_0(\mathcal R_2),
\]

\[
G_\infty(\mathcal R_1)\le G_\infty(\mathcal R_2)
\]

for fixed exact semantics.

A system may therefore move P0 -> P1 or P0/P1 -> P2 as its declared responsibility set expands.

Unrestricted separating responsibility families eventually push state cost to full non-predictive history.

---

# 10. LLM representation consequence

The phase theory creates a simple evaluation protocol for a language-model representation at matched linguistic prediction.

### Test 1 — acquisition

Is the target responsibility identifiable from the full accessible context/history?

### Test 2 — P0/P1

Can the responsibility action be implemented from a state that preserves only the linguistic predictive quotient? In empirical approximations: does a language-preserving compression/distillation retain current decision performance?

### Test 3 — P2

After controlled future evidence, can the compressed state update the responsibility correctly without reconstructing discarded history?

A failure at Test 3 with Tests 1–2 passing is the empirical signature corresponding to prospective state insufficiency.

This is more specific than a generic truth/confidence probe.

---

# 11. Parent ownership and residual

Brodu 2011 already provides causal, iso-prediction, iso-utility and decisional states and decisional-state entropy; P0 is substantially parent-owned.

Information Bottleneck/multi-task/R-PSR parents occupy much of P1's generic “secondary target requires more/different state” story.

POMDP/AIS/ISFSM/right-congruence parents occupy the generic dynamic-state machinery behind P2.

The potential residual is therefore the **cross-channel phase classification, entropy differences relative to a linguistic predictive base, and prospective-revision representation audit for LLM-like systems**.

Whether that is enough for JMLR remains an explicit open gate, not an assumption.

---

# 12. Mechanical verification

The executor adds to V4:

1. enumerate `C_k^*` for `k=0..K` on all registered small machines;
2. verify monotonicity `PH1`;
3. compute stabilization horizon `K_epi`;
4. verify P0/P1/P2 canonical fixtures;
5. search smallest mixed P2 fixture (`C0>0,Omega>0`);
6. verify family-inclusion monotonicity of static/dynamic costs;
7. output a phase table derived entirely from exact results.

No phase boundary is tuned after enumeration.
