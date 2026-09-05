# MEG-16 V1 — contradiction and ATMS nogoods over warrant intervals

Status: **FOUNDATION CANDIDATE WITH A PRESERVED REFUTATION OF THE ATLAS' UNCONDITIONAL KLEENE CLAIM.**
Parent issue: `#319`. Atlas identity: `MEG-16`.
Checker: `machine_epistemics_foundation_v1_check.py`.
Primary parent: ATMS nogoods / assumption environments (de Kleer). No novelty claim.

## 0. Preserved defect in the gap-atlas draft

The atlas proposed that liveness under nogood filtering would remain an unconditional Kleene homomorphism.

That statement is false.

Let the nogood set be `N = {{a,b}}`.

Let profile `P` have the single support `{a}` and profile `Q` have the single support `{b}`.

Individually:

- `P` is LIVE;
- `Q` is LIVE.

Their conjunction has support `{a,b}`, which is a registered nogood and must be rejected.

Therefore the conjunction cannot be LIVE, even though ordinary Kleene conjunction gives `LIVE ∧ LIVE = LIVE`.

The failed statement is preserved here as `MEG-16-REFUTED-V0`; it is not silently rewritten into a passing theorem.

The missing information is **cross-operand dependence/consistency**. A three-valued truth summary alone is not compositional once nogoods can span both operands.

## 1. Objects

Let `E` be the assumption/evidence universe.

A profile `P` is an antichain of sufficient support sets `W ⊆ E`.

A nogood family `N ⊆ 2^E` is an antichain of inconsistent assumption sets.

Define:

`filter_N(P) = Min { W in P | no n in N satisfies n ⊆ W }`.

For warrant interval `I = [L,U]`, filtering applies to both endpoints.

Choice and product before contradiction filtering retain the existing antichain semiring:

- `P ⊕ Q = Min(P ∪ Q)`;
- `P ⊗ Q = Min { p ∪ q | p in P, q in Q }`.

Define contradiction-safe product:

`P ⊗_N Q = filter_N(filter_N(P) ⊗ filter_N(Q))`.

The **final** filter is mandatory.

## 2. Corrected statements

### MEG-16A — filter commutes with choice

`filter_N(P ⊕ Q) = filter_N(filter_N(P) ⊕ filter_N(Q))`.

Reason: choice introduces no new union of assumptions across operands.

The checker exhausts all antichains on three assumptions against seven non-empty nogood families used by the finite harness.

### MEG-16B — product requires a post-filter

`filter_N(P ⊗ Q) = filter_N(filter_N(P) ⊗ filter_N(Q))`.

But in general:

`filter_N(P) ⊗ filter_N(Q) != filter_N(P ⊗ Q)`.

Witness: `P={{a}}`, `Q={{b}}`, `N={{a,b}}`.

Prefilter-only product emits the inconsistent support `{a,b}`. The correct result is the zero profile.

This is the planted mutant in the checker.

### MEG-16C — contradiction-safe product is associative

`(P ⊗_N Q) ⊗_N R = P ⊗_N (Q ⊗_N R)`.

Intuition: once an environment contains a nogood, every superset contains it too, so deleting inconsistent environments early cannot remove a support that could later become consistent.

The checker exercises associativity over a compact basis for every registered finite nogood witness.

### MEG-16D — `CONTRADICTED` is a composition terminal, not a fourth truth value

Foundation V1 keeps truth-warrant values `{LIVE, DEAD, UNKNOWN}`.

`CONTRADICTED` records that composition failed because all candidate joint supports were ruled out by a registered nogood.

It must not be coerced to:

- `LIVE` (would accept an inconsistent derivation);
- `DEAD` as a claim about world falsity;
- `UNKNOWN` (would hide a known inconsistency).

A downstream learner/runtime may branch on this terminal, for example to request clarification, acquire discriminating evidence, split contexts, or preserve competing alternatives.

### MEG-16E — conditional Kleene law under nogood separability

For intervals `I,J`, define `N-separable(I,J)` when no admissible upper support of `I` combined with an admissible upper support of `J` contains any nogood.

Under this condition, contradiction cannot be introduced by the conjunction, and the ordinary KS-T21 Kleene law is preserved:

`lambda_N(I ⊗_N J) = lambda_N(I) ∧3 lambda_N(J)`.

Without `N-separable`, the theorem is false by the `{a}/{b}` witness above.

The checker exercises the conditional theorem over a finite basis and separately asserts the hostile witness.

## 3. Constraints and claims

A `CONSTRAINT` edge does not make either endpoint false merely because the pair is inconsistent.

Instead it registers a nogood over the assumptions required to jointly sustain the forbidden combination.

Consequently, two claims may each remain individually LIVE in different admissible contexts while their attempted joint firing is `CONTRADICTED`.

This is the ATMS reading and is the reason the foundation does not introduce Belnap `Both` as a truth value here.

If later OCM must store explicit object-level contradictory truth assertions as first-class content, that is a separate study; it cannot be obtained by relabeling the nogood terminal.

## 4. Runtime law

Before an operator/hyperedge fires on multiple tails:

1. obtain the candidate joint support by product;
2. apply the registered nogood filter;
3. if every joint support is eliminated specifically by nogoods, return `CONTRADICTED`;
4. otherwise continue ordinary liveness/authority/scope checks.

A runtime that filters each tail independently but omits step 2 is unsound.

## 5. Hostile controls

The checker covers:

- exhaustive choice/filter agreement on the n=3 profile set;
- exhaustive product/post-filter agreement on the same profile set;
- the prefilter-only mutant;
- the `LIVE + LIVE -> CONTRADICTED` cross-nogood witness;
- conditional Kleene checks only when the separability precondition holds;
- associativity witnesses.

## 6. OCM absorption rule

OCM parity must show:

- nogoods are first-class registered objects, not hidden ad-hoc conditions;
- final post-product filtering is present;
- the runtime exposes `CONTRADICTED` distinctly;
- no code treats `CONTRADICTED` as proof of either proposition's falsity;
- the hostile `{a}/{b}` cross-nogood case is present;
- any claimed Kleene homomorphism checks the separability precondition.

## 7. Non-consequences

This note does not solve paraconsistent logic generally, does not define belief revision policy, and does not decide which real-world sources are contradictory.

It closes the foundation's algebraic/runtime boundary for **registered inconsistent assumption environments** and preserves the refutation that forced the corrected statement.
