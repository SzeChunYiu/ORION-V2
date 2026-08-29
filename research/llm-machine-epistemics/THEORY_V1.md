# Predictive and Epistemic State — Theory V1

**Status:** candidate theorem stack for #51.  
**Scope:** finite/discrete probability spaces unless a theorem explicitly states otherwise.  
**Authority:** mathematical research draft; not an empirical claim about any deployed LLM.

## 1. Setup

Let `H` be a finite random variable representing the information/history available to an autoregressive model at a declared point in prediction. Let `Y` denote the **entire declared linguistic future** rather than only the next token. Let `Q=(Q_1,...,Q_m)` denote a finite family of operational epistemic responsibility variables. Let an internal representation be a deterministic statistic

\[
Z=f(H).
\]

The deterministic restriction is intentional for V1. Stochastic representations are deferred to the approximate rate-region programme.

### Definition 1 — linguistic predictive sufficiency

`Z` is linguistically predictive-sufficient when

\[
Y \perp H\mid Z,
\]

or equivalently

\[
P(Y\mid H=h)=P(Y\mid Z=f(h))
\]

for every history in the support.

### Definition 2 — minimal linguistic predictive state

Define the equivalence relation

\[
h\sim_P h'
\iff
P(Y\mid H=h)=P(Y\mid H=h').
\]

Let

\[
S_P=[H]_{\sim_P}.
\]

This is the finite analogue of the causal/predictive-state quotient. Its existence/minimality is donor-owned background from sufficient-statistic and computational-mechanics theory; ORION claims no priority for it.

### Definition 3 — responsibility sufficiency

For one responsibility variable `Q`, `Z` is responsibility-sufficient when

\[
Q\perp H\mid Z.
\]

For the family `\mathcal Q={Q_1,...,Q_m}`, require this for every member. When exact joint decisions matter, one may equivalently use the vector `Q=(Q_1,...,Q_m)` and require `Q\perp H\mid Z`; the distinction must be stated because componentwise sufficiency need not preserve every joint dependence property.

### Definition 4 — deterministic responsibility

A responsibility is deterministic when

\[
Q=q(H)
\]

for a declared map `q`. Examples include a mechanically specified source class, a mechanically defined identifiability terminal, or a registered scope/defeater status computed from the full history. Human legitimacy or institutional authority is deliberately outside this class.

### Definition 5 — joint predictive–epistemic equivalence

For a declared joint responsibility vector `Q`, define

\[
h\sim_{PE} h'
\iff
h\sim_P h'
\quad\text{and}\quad
P(Q\mid h)=P(Q\mid h').
\]

Let

\[
S_{PE}=[H]_{\sim_{PE}}.
\]

For deterministic `Q=q(H)`, the second condition reduces to `q(h)=q(h')`.

---

# 2. Foundation lemma — every predictive-sufficient state refines the predictive quotient

## Lemma 1

If deterministic `Z=f(H)` is linguistically predictive-sufficient, then `S_P` is a deterministic function of `Z` almost surely:

\[
S_P=g(Z).
\]

### Proof sketch

Take any histories `h,h'` with `f(h)=f(h')=z`. Predictive sufficiency gives

\[
P(Y\mid h)=P(Y\mid Z=z)=P(Y\mid h').
\]

Hence `h\sim_P h'`. Therefore every fibre of `Z` lies inside one predictive-equivalence class, so the class label `S_P` is constant on each `Z` fibre and factors through `Z`. ∎

### Consequence

For every deterministic predictive-sufficient representation,

\[
H(S_P\mid Z)=0.
\]

This is the exact point at which classical minimal-sufficient-statistic theory enters. The theorem is background infrastructure, not a novelty claim.

---

# 3. T1 — Predictive sufficiency does not imply epistemic sufficiency

## Theorem 1 — predictive–epistemic separation

Suppose there exist histories `h,h'` with positive probability such that

\[
P(Y\mid h)=P(Y\mid h')
\]

but

\[
P(Q\mid h)\neq P(Q\mid h').
\]

Then the minimal predictive state `S_P` is not sufficient for `Q`:

\[
Q\not\perp H\mid S_P.
\]

### Proof

The two histories belong to the same predictive-equivalence class by the first equality. If `S_P` were sufficient for `Q`, every history inside that class would induce the same conditional law of `Q`, contradicting the second inequality. ∎

### Corollary 1 — strict log-loss consequence

Under the assumptions of Theorem 1, whenever the differing conditional laws occur on positive mass,

\[
I(Q;H\mid S_P)>0.
\]

Thus a Bayes-optimal decoder restricted to `S_P` has strictly larger expected log loss for `Q` than one that may use the full history.

### Scientific interpretation

The theorem does **not** say an LLM trained for language prediction must discard `Q`. It says that the coarsest state sufficient for the linguistic future is not guaranteed to retain `Q`; linguistic predictive sufficiency and epistemic responsibility sufficiency are different information requirements.

---

# 4. T2 — Maximal predictive compression forces epistemic loss

A stronger statement is possible once "minimal predictive representation" is made quantitative rather than rhetorical.

## Theorem 2 — entropy-minimal predictive representations are isomorphic to `S_P`

Let `Z=f(H)` be deterministic and predictive-sufficient. Then

\[
H(Z)\ge H(S_P).
\]

Moreover, if

\[
H(Z)=H(S_P),
\]

then `Z` and `S_P` determine one another almost surely:

\[
H(S_P\mid Z)=H(Z\mid S_P)=0.
\]

### Proof

Lemma 1 gives `H(S_P|Z)=0`. Hence

\[
H(Z,S_P)=H(Z)=H(S_P)+H(Z\mid S_P),
\]

so

\[
H(Z)=H(S_P)+H(Z\mid S_P)\ge H(S_P).
\]

Equality holds iff `H(Z|S_P)=0`; together with Lemma 1, this gives almost-sure mutual recoverability. ∎

## Corollary 2 — maximal predictive compression forces responsibility loss

If `S_P` is not sufficient for responsibility `Q`, then no deterministic predictive-sufficient representation `Z` with minimal possible entropy `H(Z)=H(S_P)` can be sufficient for `Q`.

### Proof

Every entropy-minimal predictive-sufficient `Z` is isomorphic to `S_P` by Theorem 2. Sufficiency for `Q` is preserved under such a bijective relabelling. Since `S_P` is insufficient, so is `Z`. ∎

### Candidate paper significance

This is stronger than the statement that two hidden representations can implement the same predictor. It identifies a specific design objective—**maximal compression under linguistic predictive sufficiency alone**—under which epistemic loss is unavoidable exactly when the epistemic responsibility varies inside predictive fibres.

### Boundary

The result does not apply to non-minimal representations. A large transformer may preserve substantial information beyond `S_P`. Therefore the theorem is an impossibility result about objectives/representations satisfying the stated minimality condition, not a diagnosis of every actual LLM.

---

# 5. T3 — Exact deterministic epistemic overhead

For deterministic responsibility `Q=q(H)`, define an augmentation of the minimal predictive state

\[
Z=(S_P,U).
\]

Require exact responsibility recovery:

\[
H(Q\mid S_P,U)=0.
\]

Define the zero-error epistemic overhead

\[
C_{\mathrm{epi}}^0(Q\mid S_P)
=
\inf_U H(U\mid S_P)
\]

subject to exact recovery.

## Theorem 3 — exact overhead identity

For finite deterministic `Q=q(H)`,

\[
\boxed{
C_{\mathrm{epi}}^0(Q\mid S_P)=H(Q\mid S_P)
}
\]

### Lower bound

Because `Q` is deterministic from `H`, `H(Q|H)=0`. Exact recovery from `(S_P,U)` gives

\[
H(Q\mid S_P,U)=0.
\]

Therefore

\[
I(Q;U\mid S_P)
=
H(Q\mid S_P)-H(Q\mid S_P,U)
=
H(Q\mid S_P).
\]

But

\[
I(Q;U\mid S_P)\le H(U\mid S_P),
\]

so

\[
H(U\mid S_P)\ge H(Q\mid S_P).
\]

### Achievability

Choose `U=Q`. Then exact recovery is immediate and

\[
H(U\mid S_P)=H(Q\mid S_P).
\]

Thus the lower bound is tight. ∎

## Corollary 3 — zero-cost condition

\[
C_{\mathrm{epi}}^0(Q\mid S_P)=0
\iff
H(Q\mid S_P)=0.
\]

Thus predictive compression is epistemically harmless for `Q` exactly when `Q` is already recoverable from the minimal predictive state.

## Multi-responsibility form

For deterministic vector `Q=(Q_1,...,Q_m)`, the exact joint overhead is

\[
H(Q_1,...,Q_m\mid S_P),
\]

not generally the sum of individual conditional entropies. This matters because responsibilities may share information. The vector of individual deficiencies should still be retained for diagnostic interpretation.

---

# 6. T4 — Epistemic deficiency under log loss

Let `Z` be any statistic or stochastic representation generated from `H` such that

\[
Q - H - Z
\]

forms the natural Markov chain induced by representation generation.

For a Bayes-optimal probabilistic decoder under logarithmic loss, the minimum expected loss given variable `V` is `H(Q|V)`.

Define

\[
\Delta_{\mathrm{epi}}(Z;Q)
=
H(Q\mid Z)-H(Q\mid H).
\]

## Theorem 4 — conditional-information identity

\[
\boxed{
\Delta_{\mathrm{epi}}(Z;Q)=I(Q;H\mid Z)
}
\]

### Proof

By the chain rule,

\[
I(Q;H\mid Z)=H(Q\mid Z)-H(Q\mid H,Z).
\]

Because `Z` is generated from `H`, conditioning additionally on `Z` does not alter the law of `Q` once `H` is known, so

\[
H(Q\mid H,Z)=H(Q\mid H).
\]

Substitution yields the identity. ∎

### Responsibility vector

For `\mathcal Q={Q_i}`, preserve

\[
\mathbf\Delta_{\mathrm{epi}}(Z)
=
\bigl(I(Q_1;H\mid Z),...,I(Q_m;H\mid Z)\bigr)
\]

unless a declared decision problem justifies a particular scalarization.

---

# 7. T5 — Evidence-free post-processing cannot restore discarded epistemic information

Let downstream internal computation produce

\[
W\sim K(\cdot\mid Z)
\]

using no new information source correlated with `Q` beyond `Z`. Thus

\[
Q-H-Z-W
\]

is a Markov chain.

## Theorem 5 — post-processing monotonicity

\[
I(Q;W)\le I(Q;Z)
\]

and equivalently

\[
H(Q\mid W)\ge H(Q\mid Z).
\]

This follows directly from the data-processing inequality.

### Correct interpretation

This does **not** say internal reasoning is useless. A computationally weak decoder may fail to extract information that is present in `Z`; additional computation can make that information accessible. The theorem only says that once the representation has genuinely discarded responsibility-relevant information, downstream evidence-free processing cannot recreate it.

This distinction should be carried into all discussion of chain-of-thought, reflection and self-correction.

---

# 8. T6 — Exact log-loss value of an external observation

Suppose the model acquires a new observation `X`. Before acquisition it uses `Z`; afterwards it may use `(Z,X)`.

## Theorem 6

The exact reduction in Bayes-optimal log loss for responsibility `Q` is

\[
\boxed{
H(Q\mid Z)-H(Q\mid Z,X)=I(Q;X\mid Z)
}
\]

by the definition of conditional mutual information.

### Interpretation

This gives a clean mathematical boundary between:

- **epistemic computation:** transformation of information already contained in the current state;
- **epistemic acquisition:** receipt of a new observation with positive conditional information about the responsibility.

The result is donor-owned information theory; the paper's residual must lie in how it composes with responsibility-sufficient LLM state, not in claiming the identity itself as new.

---

# 9. T7 — Responsibility refinement order and joint state

For a deterministic responsibility family `\mathcal A`, let `S_{P\mathcal A}` denote the coarsest partition that refines predictive equivalence and makes every responsibility in `\mathcal A` exactly recoverable.

For deterministic variables this is simply the partition induced by the tuple

\[
(S_P,Q_{a_1},...,Q_{a_k}).
\]

## Theorem 7 — monotone refinement

If

\[
\mathcal A\subseteq\mathcal B,
\]

then `S_{P\mathcal B}` refines `S_{P\mathcal A}`. Consequently,

\[
H(S_{P\mathcal B})\ge H(S_{P\mathcal A}).
\]

The inequality is strict exactly when the additional responsibilities in `\mathcal B\setminus\mathcal A` contain positive conditional entropy given `S_{P\mathcal A}`.

### Proof sketch

Every equivalence class preserving all responsibilities in `\mathcal B` necessarily preserves the subset in `\mathcal A`; hence the partition is finer. For finite variables, refinement gives deterministic recoverability of the coarser state from the finer state, and the entropy inequality follows. Strictness reduces to positive conditional entropy of the additional responsibility vector. ∎

### Interpretation

There is no universal scalar notion of "more epistemic state." State requirements are relative to a declared responsibility family. This is the internal-LLM analogue of ORION responsibility-relative state.

---

# 10. T8 — Approximate predictive–epistemic rate region

V1 does not claim a new rate-distortion theorem. It defines the object that a later mechanical/symbolic analysis must characterize.

Let `Z` be a possibly stochastic representation. One candidate exact-prediction frontier is

\[
R_{\mathrm{epi}}(\epsilon)
=
\inf I(H;Z\mid S_P)
\]

subject to

\[
Y\perp H\mid Z
\]

and

\[
I(Q;H\mid Z)\le\epsilon.
\]

For several responsibilities, use a vector constraint

\[
I(Q_i;H\mid Z)\le\epsilon_i.
\]

A second version should permit controlled linguistic predictive distortion rather than exact sufficiency and expose a two-objective region

\[
(\text{linguistic prediction risk},\text{epistemic responsibility risk},\text{state rate}).
\]

### Required before publication

The paper needs at least one nontrivial family with a closed-form frontier or sharp bound. Merely naming conditional rate distortion is insufficient novelty.

---

# 11. T9 — Internal representation criterion

The mathematics above characterizes information that **can** be preserved. It does not by itself establish that a real LLM has a belief-like internal state.

For future empirical interpretation, adopt a stronger criterion than linear decodability. A candidate epistemic property should be:

1. reliably recoverable under a declared probe;
2. coherent enough to support the declared responsibility;
3. present with appropriate distributional regularity rather than isolated artefact;
4. **causally usable** by the model, tested through interventions or mediation where possible.

This section is explicitly donor-linked to the literature on standards for belief representations in LLMs. It is an interpretation contract, not a new theorem.

---

# 12. Known-answer constructions

## CE1 — one-bit epistemic overhead with zero linguistic cost

Let `T,U` be independent fair bits and define

\[
H=(T,U),\qquad Y=T,\qquad Q=U.
\]

Then `S_P=T`. Hence

\[
H(Q\mid S_P)=H(U\mid T)=1\text{ bit}.
\]

The minimal predictive state is perfect for the linguistic target while carrying zero mutual information about the responsibility. By Theorem 3, exactly one additional bit is necessary and sufficient for exact responsibility recovery.

## CE2 — same predictor, different epistemic capacity

Let

\[
Z_1=S_P,\qquad Z_2=(S_P,Q).
\]

Both can feed an identical optimal linguistic prediction head; `Z_2` additionally supports exact `Q`. This is an illustration only because generic predictor/representation non-identifiability is directly occupied by prior work.

## CE3 — discarded defeater cannot be recreated

Reuse CE1 and let `W` be any stochastic function of `S_P=T` independent of `U` given `T`. Then

\[
I(U;W)=0
\]

and exact responsibility recovery remains impossible regardless of downstream processing.

## CE4 — strict responsibility-family refinement

Let `T,U,V` be independent fair bits, `Y=T`, `Q_a=U`, `Q_b=V`. Then:

\[
H(S_{P\{a\}})=2,
\quad
H(S_{P\{b\}})=2,
\quad
H(S_{P\{a,b\}})=3
\]

bits, with neither single-responsibility state sufficient for the other responsibility.

## CE5 — harmless predictive compression

Let `Q=T` in CE1. Then `Q` is already determined by `S_P=T` and

\[
H(Q\mid S_P)=0.
\]

This negative control is mandatory: predictive compression is not intrinsically epistemically harmful.

---

# 13. What is actually new if the stack survives review?

The following are **not** proposed as novelty: causal-state minimality, fibre factorization, data-processing monotonicity, conditional mutual-information identities, generic sufficiency, or generic rate-distortion theory.

The candidate residual is the combined LLM-specific theorem object:

> For an autoregressive linguistic process, define epistemic competence relative to an explicit family of operational responsibilities. The coarsest entire-future predictive state may be insufficient for those responsibilities. Under deterministic finite-state maximal predictive compression this insufficiency is unavoidable; for deterministic responsibilities the exact additional state entropy is `H(Q|S_P)`; larger responsibility families induce a refinement order; and the approximate problem becomes a responsibility-constrained predictive–epistemic rate region.

This residual remains provisional until the nearest-work audit establishes that the full theorem stack is not already present as one named parent construction.

---

# 14. Mechanical work still required

The conceptual/theoretical work is sufficiently specified for independent attack. Remaining tasks should be executed mechanically rather than by inventing new claims after seeing failures:

- mechanize or independently check Lemma 1 and Theorems 1–7;
- exhaustively enumerate finite distributions/partitions to find missing assumptions;
- specifically attack Theorem 2 when determinism, exact sufficiency, finite entropy or entropy minimality is relaxed;
- compute/derive at least one nontrivial `R_epi(epsilon)` family;
- generate strictness and zero-overhead fixtures automatically;
- bind every final theorem to nearest-work ownership before manuscript promotion.
