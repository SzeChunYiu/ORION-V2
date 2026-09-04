# Machine Epistemics Foundation — Batch 2

**Status:** research/theory artifact for ORION-V2. **No novelty, field-status, architecture-superiority, or publication-authority claim.** This note closes or contracts only the obligations named below. Negative findings and scope restrictions are part of the result.

**Base audited:** ORION-V2 `24566f00a9dc4425a438fcfac05d13c6b2d903db` and `ME_THEORY_GAP_ATLAS_V1.md`. Open PR #317 owns MEG-01/04/06/08/18/22/26/29/30/31/35 and is deliberately not duplicated here.

**Checker:** `meg_foundation_batch2_exact.py` (stdlib only; exact rationals where arithmetic matters; exit 0/1/2 = PASS/FAIL/CANNOT_CHECK). **Finite enumeration is a counterexample/calibration instrument; the all-size statements below stand on their proofs, not on enumeration.**

## Analytical cells used in this pass

These are same-session analytical lenses, **not independent reviewers and not external authority**.

- **S — statistical inference:** separates population guarantees, conditional guarantees, pointwise truth, abstention and decision risk.
- **F — formal semantics/TMS:** checks warrant algebra, nogoods, scope, refinement and proof obligations.
- **D — dynamic databases/revision:** checks epoch validity, supersession, immutable history and reopening locality.
- **R — runtime/systems:** checks identity binding, replay, locality and fail-closed interfaces.
- **H — hostile parent/referee:** tries to reduce each construction to its strongest parent and searches for counterexamples to over-strong formulations.

The cells agreed on two **contractions** rather than positive proofs of the atlas wording: MEG-02 must distinguish truth warrant from risk-bounded actionability, and MEG-16's conjunction law is a sub-homomorphism rather than a homomorphism.

---

## Shared warrant object

Let `E` be the evidence universe. A profile is a finite antichain of finite evidence sets. As in KS-T01,

`P ⊕ Q = Min(P ∪ Q)`, `P ⊗ Q = Min{p ∪ q : p∈P,q∈Q}`, `0 = ∅`, `1 = {∅}`.

Write `P ≤ Q` when every support in `P` contains some support in `Q`. A warrant interval is `I = ⟦L,U⟧` with `L ≤ U`. For revoked assumptions `R`, `λ_R(I)` is LIVE when some lower support survives, DEAD when no upper support can survive, and UNKNOWN otherwise. KS-T21 supplies the strong-Kleene homomorphism for the unfiltered interval algebra.

Nothing in this note changes those objects.

---

# T1 — MEG-02 corrected: statistical guarantee is not individual truth warrant

### Finding

The atlas's provisional MEG-02 wording allowed a scoped statistical coverage receipt to become a bridge that could make an individual candidate LIVE. That implication is **too strong** when LIVE means warranted truth of the individual claim.

Conformal and other risk/coverage procedures certify a **procedure-level probabilistic property under assumptions and scope**. Standard conformal validity is ordinarily a marginal coverage guarantee under exchangeability; it does not state that the prediction for the particular present case is true. This distinction is load-bearing for OCM because a truth lattice and a decision/risk gate serve different propositions.

### Definitions

For a statistical operator output `c`:

1. `Truth(c) = ⟦0,U_c⟧` by default. A score, likelihood, confidence, posterior, conformal p-value, or empirical success rate is stored outside this truth interval unless a separately registered epistemic calculus explicitly gives it truth semantics.
2. `RiskReceipt ρ = (I_op, guarantee, δ, S, epoch, assumptions, calibration_id, checker_id)` is a claim **about the operator/procedure**, not about the truth of `c`.
3. `I_op` is content-bound to at least `(implementation/model, configuration, checker, calibration set/split, assumptions, scope, epoch)`. Configuration includes any behaviorally relevant inference setting named by the registered study.
4. `Actionable_τ(c,ρ)` is a decision predicate: the task contract permits a probabilistic action, `ρ` matches the current operator identity/scope/epoch, the registered assumptions are in force, and `δ ≤ τ` for the task's maximum risk.

### Theorem T1.1 — marginal coverage does not entail pointwise truth

From a statement `Pr{Y ∈ C(X)} ≥ 1−δ` alone one cannot infer `Y ∈ C(x)` for the particular observed `x`, nor can one refine an arbitrary candidate's truth interval to LIVE.

**Proof by finite counterexample.** Let `X∈{a,b}` with `Pr(X=a)=1−δ`, `Pr(X=b)=δ`. Let the prediction set cover the truth on every `a` case and miss on every `b` case. Marginal coverage is exactly `1−δ`, while conditional coverage at `b` is `0`. Therefore the marginal proposition is logically compatible with the present `b` prediction being wrong. Any rule `coverage receipt ⇒ individual LIVE` is unsound. ∎

This is not an attack on conformal prediction; it is the standard distinction between the proposition a coverage method guarantees and a different pointwise proposition.

### Theorem T1.2 — actionability and truth are orthogonal coordinates

`Actionable_τ(c,ρ)` does not change `Truth(c)`. In particular an UNKNOWN candidate may be ACTIONABLE under a risk-tolerant task contract without becoming LIVE.

**Proof.** `Actionable` reads `ρ`, identity, scope, epoch and the task's risk bound. Its transition has no write to `(L,U)`. Hence `λ_R(Truth(c))` is invariant under action-gate evaluation. The planted mutant that rewrites `Truth(c)=1` on receipt acceptance violates this noninterference rule. ∎

### Theorem T1.3 — certificate identity drift is fail-closed

If any bound coordinate of `I_op` changes, a receipt issued for the old identity is inapplicable to the new one. The gate returns `CANNOT_CHECK` (or requires recalibration); it may not silently inherit the guarantee.

**Proof.** Applicability is equality of the content-bound identity tuple plus scope/epoch/assumption predicates. A changed coordinate produces a different digest, so the applicability premise is false. ∎

### Parent/subtraction

- Conformal prediction owns finite-sample coverage guarantees under its assumptions; ORION does not claim them. Lei et al. (2018, *JASA*, distribution-free predictive inference) explicitly state finite-sample **marginal** coverage; Angelopoulos & Bates (2023) is a modern exposition. Conditional/pointwise coverage requires stronger conditions and in general cannot be obtained distribution-free in the same form.
- Classification with reject option owns risk/rejection trade-offs (Chow line of work).
- The OCM-specific requirement here is only the **type separation**: a risk certificate is not an individual truth certificate, and its applicability is content/version/scope bound.

### Terminal

`MEG-02 = PROVED_WITH_CONTRACTION__TRUTH_WARRANT_SEPARATE_FROM_RISK_ACTIONABILITY`

The graded/probabilistic truth semiring proposed in the atlas remains **OPEN_RESEARCH**. This theorem deliberately does not invent one.

---

# T2 — MEG-03: epoch expiry and supersession are scoped revocation, not deletion

### Definitions

Use half-open validity scopes `[s,e)` with open ends allowed. `S1 ∩ S2` is ordinary interval intersection; empty intersection is `SCOPE_EMPTY`. At evaluation time `t`, evidence outside its validity epoch is treated as revoked for that query: `R_t = R_explicit ∪ {e : t ∉ epoch(e)}`.

`supersede(e_old,e_new)` is the append-only transaction:

1. admit `e_new` with a new content identity;
2. append `SUPERSEDED_BY(e_old,e_new)`;
3. add `e_old` to the effective revocation family from the supersession point onward;
4. compute reopening by KS-T22 from the changed evidence.

History is never overwritten.

### Theorem T2.1 — epoch scopes form a meet-semilattice

Intersection of half-open validity scopes is associative, commutative and idempotent; `SCOPE_EMPTY` is an annihilator.

**Proof.** Start is `max` of lower bounds and end is `min` of upper bounds, with open ends as infinities. Associativity/commutativity/idempotence follow from `max/min`; if start ≥ end the result is empty, and intersecting an empty set stays empty. ∎

### Theorem T2.2 — time measurability criterion

For a partition `κ` and a registered evaluation-time family `T`, epoch liveness is block-measurable iff, for every block `B` and time `t∈T`, the indicator `[t∈epoch(e)]` is constant over `e∈B`. Equivalently every validity boundary induces unions of whole blocks over the registered family.

**Proof.** This is exactly the definition of measurability of the Boolean liveness function through a quotient: a quotient value exists iff it is constant on every fibre. Necessity and sufficiency are immediate. ∎

### Theorem T2.3 — supersession reopening is local

Under the dependency model of KS-T09/T22, superseding `e_old` can change only atoms in `Impact_D({e_old})`; every atom outside the cone is unaffected. The replacement `e_new` is not automatically in that cone merely because it supersedes `e_old`.

**Proof.** Supersession's semantic removal operation is the revocation of `e_old`; KS-T09 defines the least dependency-closed set reachable from changed support. S5 prohibits unrelated hidden writes. Admission of `e_new` has its own forward dependency cone. ∎

### Boundaries

- Supersession says the previous source is no longer authoritative/current in the registered scope; it does **not** prove the replacement is true.
- Valid-time/transaction-time ideas are mature temporal-database parents; this note uses them as organization, not novelty.

### Terminal

`MEG-03 = PROVED_UNDER_REGISTERED_EPOCH_SCOPE_AND_DEPENDENCY_MODEL`

---

# T3 — MEG-16 corrected: nogood filtering preserves alternatives, not conjunction exactly

Let `𝒩` be an antichain of inconsistent assumption sets (ATMS nogoods). A support `W` is consistent iff no `N∈𝒩` satisfies `N⊆W`. Define

`F_𝒩(P) = Min{W∈P : W consistent}`

and apply `F_𝒩` to both bounds of an interval.

### Lemma T3.1 — filtering is monotone and preserves intervals

If `P≤Q`, then `F(P)≤F(Q)`. Hence `⟦L,U⟧` remains a valid interval after filtering.

**Proof.** Take any consistent `w∈F(P)`. Because `P≤Q`, some `v∈Q` has `v⊆w`. If `v` contained a nogood, then its superset `w` would too, contradicting consistency. So a consistent support in `Q` lies below `w`; minimization preserves such a witness. ∎

### Theorem T3.2 — exact alternative law

`F(P⊕Q) = F(P)⊕F(Q)`.

**Proof.** `⊕` is antichain minimization of union. Removing inconsistent sets commutes with union; minimization before or after removal yields the same minimal consistent members. ∎

### Theorem T3.3 — conjunction is only a sub-homomorphism

`F(P⊗Q) ≤ F(P)⊗F(Q)` in the antichain order, and equality can fail strictly.

**Strict witness.** `P={{a}}`, `Q={{b}}`, `𝒩={{a,b}}`. Each factor is individually consistent, so `F(P)⊗F(Q)={{a,b}}`; after composition the joint support is a nogood, so `F(P⊗Q)=0`.

Therefore the atlas's provisional phrase “liveness ... is again a Kleene homomorphism” is **refuted for conjunction**. The correct law is:

`λ(F(I⊕J)) = λ(F(I)) ∨₃ λ(F(J))`, while

`λ(F(I⊗J)) ≤₃ λ(F(I)) ∧₃ λ(F(J))`

in the order `DEAD < UNKNOWN < LIVE`.

### Theorem T3.4 — violated constraints disable joint firing

If every joint support of two tails contains a registered nogood, their filtered composite is DEAD; an edge requiring both tails cannot be ENABLED. Each tail may remain individually LIVE.

### Parent/subtraction

ATMS nogoods are parent-owned (de Kleer, 1986). The contribution here is only their exact embedding into the already adopted KSO interval algebra and, importantly, the contraction of an over-strong homomorphism claim.

### Terminal

`MEG-16 = PROVED_WITH_CORRECTION__JOIN_HOMOMORPHISM_MEET_SUBHOMOMORPHISM`

No Belnap “Both” value is introduced; contradiction remains an explicit nogood record. If future OCM requirements need contradictory propositions to remain simultaneously truth-valued, that is a different research object.

---

# T4 — MEG-17: reinstate and relearn are different lifecycle operations

### Definitions

- `reinstate(e)` removes the same evidence identity `e` from the explicit revocation set. It does not mint new support.
- `relearn(c,e')` admits new evidence identity `e'`, creates new support for content/procedure `c`, and appends a lineage edge from the old learned object/version to the new one. Old evidence/history remains addressable.

### Theorem T4.1 — reinstate exactness

When no other state changed, reinstate of the same evidence identity restores the pre-revocation warrant/liveness/navigation state exactly.

**Proof.** This is KS-T04b(iv) for the same profile, structure, denominators and seed; removing `e` from `R` restores the same gates and therefore the same fixed point. ∎

### Theorem T4.2 — relearn may be current-equivalent while lifecycle-distinct

Suppose old and new learned objects compute the same registered behavior and are supported respectively by distinct evidence ids `e` and `e'`. They can be behaviorally identical at current `R=∅`, while their lifecycle signatures differ because revoking `{e}` kills the old support but not the new one (and vice versa).

**Proof.** Current behavior equality is an explicit premise. The profiles `{{e}}` and `{{e'}}` are both LIVE at `R=∅`, but have different liveness under the two singleton revocations. Thus WLL current-equivalence does not imply lifecycle-equivalence. ∎

### Theorem T4.3 — non-macro repair locality

For a finite dependency graph with explicit forward adjacency and no hidden global state, a support change `C` can affect only `Impact_D(C)`. A local repair algorithm therefore needs at most the induced cone plus incident dependency edges; any algorithm that recomputes unrelated components is correct but not locality-optimal.

**Proof.** By definition `Impact_D(C)` is the least dependency-closed superset. A node outside it has no dependency path from `C`, and S5 forbids a state change without an explicit dependency/write. Induct on topological distance (or fixed-point iterations for cycles) to show its inputs are unchanged, hence its derived state is unchanged. ∎

This closes MEG-17 for ordinary explicit-dependency objects. It does **not** close KS-T12's harder macro-content/deconsolidation problem.

### Terminal

`MEG-17 = PROVED_SCOPE_LIMITED__EXPLICIT_NONMACRO_DEPENDENCY_MODEL`

---

# T5 — MEG-20: content of a sufficiency certificate for quotient summaries

A summary/quotient is allowed to answer only a registered query family for which solving commutes with the quotient. The phrase “registered sufficiency certificate” is therefore expanded into the following content-bound object.

### Definition — `SufficiencyCertificate(m,Q,Γ)`

It binds:

1. source KSO/state-schema identity;
2. partition/quotient map `κ` and quotient identity;
3. registered query family `Q` (including seed construction);
4. registered revocation family `Γ`;
5. navigation/normalization version and any parameters that change the transition matrix;
6. the answer/decision functional `h_q` for each `q∈Q`;
7. proof/checker identity and validity epoch;
8. evidence showing the obligations below hold.

For every `q∈Q` and `R∈Γ`, let `P_{q,R}` be the gated transition matrix on the query-reachable subchain.

Required obligations:

- **Lumpability:** for any two states in one block, total transition mass into every target block is identical in `P_{q,R}`.
- **Warrant measurability:** three-valued liveness is constant within each block under `R`.
- **Answer factorization:** `h_q` is constant on quotient-equivalent detailed states, i.e. there exists `\bar h_q` with `h_q = \bar h_q ∘ κ_*` on the registered reachable state space.

### Theorem T5.1 — restart navigation commutes with a certified quotient

If the obligations hold, then for every registered seed `s_q`,

`κ_*(a*_{q,R}) = \bar a*_{q,R}`,

where the right side is the restart fixed point in the quotient with seed `κ_*s_q`.

**Proof.** Strong lumpability gives the intertwining identity `κ_* P^T = \bar P^T κ_*`. Therefore it also commutes with every power `(P^T)^j`. Apply `κ_*` termwise to the convergent restart/Neumann series `a*=αΣ_j(1−α)^j(P^T)^j s`. The result is exactly the quotient series. ∎

### Theorem T5.2 — registered answers are equal

Under answer factorization, `Solve(K,q,R)=Solve(K̄,q,R)` for every `(q,R)` covered by the certificate.

**Proof.** T5.1 makes the quotient-observable navigation state identical after pushforward; warrant measurability makes block gating unambiguous; factorization makes the final registered decision depend only on that quotient-observable state. ∎

### Refusal rules

A certificate returns `REFINE_REQUIRED`, never PASS, if any registered revocation breaks liveness measurability, any reachable transition breaks lumpability, or the answer functional distinguishes members of one block. A certificate for another KSO/configuration/query family/epoch is `CANNOT_CHECK`, not reusable by name.

### Boundaries

This theorem is about registered finite-state KSO navigation/decision functions. It does not say a quotient preserves every future query, arbitrary renderer semantics, or unregistered representation move. MEG-21 remains the non-quotient conservative-extension problem.

### Terminal

`MEG-20 = PROVED_SCOPE_LIMITED__REGISTERED_Q_GAMMA_AND_ANSWER_FUNCTIONAL`

---

# Batch terminal and OCM consequences

The exact checker currently returns PASS on all five registered finite sanity/hostile suites. The scientific disposition is:

```text
MEG-02 = PROVED_WITH_CONTRACTION__TRUTH_WARRANT_SEPARATE_FROM_RISK_ACTIONABILITY
MEG-03 = PROVED_UNDER_REGISTERED_EPOCH_SCOPE_AND_DEPENDENCY_MODEL
MEG-16 = PROVED_WITH_CORRECTION__JOIN_HOMOMORPHISM_MEET_SUBHOMOMORPHISM
MEG-17 = PROVED_SCOPE_LIMITED__EXPLICIT_NONMACRO_DEPENDENCY_MODEL
MEG-20 = PROVED_SCOPE_LIMITED__REGISTERED_Q_GAMMA_AND_ANSWER_FUNCTIONAL
GENERAL_NOVELTY = NOT_ESTABLISHED
FIELD_STATUS = NOT_ESTABLISHED
```

## Required absorption changes for ORION-OCM

These are engineering consequences, not implementation authority from this note alone:

1. **Do not let a marginal statistical coverage receipt refine an individual candidate's truth interval to LIVE.** Add a separate risk/actionability gate.
2. Bind every statistical certificate to behaviorally complete operator/configuration/checker/calibration/assumption/scope/epoch identity. Drift ⇒ `CANNOT_CHECK` / recalibrate.
3. Apply nogood filtering **after** conjunction/composition. Filtering factors first is unsound.
4. Preserve superseded evidence as immutable history; effective expiry is scoped revocation.
5. Distinguish `reinstate` (same evidence lineage) from `relearn` (new evidence identity and lifecycle profile).
6. A summary may answer only while its exact sufficiency certificate remains applicable to the current KSO/query/revocation/answer-functional identity.

## What remains open after this batch

This batch does **not** close the field. In particular: graded/probabilistic truth algebra; multiscale navigation; procedure control algebra; small-step runtime preservation/progress; per-input VSW procedure warrants; structured gap learning; macro consolidation/deconsolidation; non-quotient representation moves; learned organization/topology; full codec invariance; semantic renderer non-laundering; prefix commitment; DPO Jump preservation and J2+ ceilings; open-world action value; infinite-class lifecycle identifiability; independent demarcation and replication.

Those remain explicit OPEN/PARENT/CANNOT_CHECK rows in `ME_FOUNDATION_V1.json` rather than being silently implied by this batch.
