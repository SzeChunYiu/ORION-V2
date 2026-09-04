# MEG-09 Frontier F2 — multiscale navigation reduces to parent lumpability/intertwining

**Status:** strongest-parent reduction for issue #329 F2. **NO NOVELTY OR NEW CATEGORY-THEORY CLAIM.** For the current finite KSO navigation semantics, the proposed fibre/base commutation problem is already owned mathematically by strong lumpability/intertwining of finite Markov/substochastic kernels. KSO adds a separate three-valued warrant-measurability gate.

## Object

Let a finite fine KSO state space `V` be partitioned into fibres `B_1,...,B_m`. Let `A` be the linear pushforward that sums fine activation mass inside each fibre. For a registered revocation state `R`, let `P_R` be the warranted fine transition matrix (possibly substochastic because revoked/disabled structure dissipates mass). Restart navigation is

`a* = α s + (1-α) P_R^T a*`, `0<α≤1`.

A base transition matrix `Q_R` is a valid projected dynamics when

`A P_R^T = Q_R^T A`.                                         (1)

This is the standard intertwining/strong-lumpability condition. In row form, (1) exists iff for every source fibre `B_i`, every two fine states `x,x'∈B_i`, and every target fibre `B_j`,

`Σ_{y∈B_j} P_R[x,y] = Σ_{y∈B_j} P_R[x',y]`.                  (2)

Substochasticity changes none of the algebra; missing mass may equivalently be sent to a cemetery state.

## Theorem F2.1 — restart fixed points commute with the parent projection

If (1) holds and the base seed is `A s`, then

`A a* = \bar a*`,

where `\bar a*` is the restart fixed point of `Q_R` with seed `A s` and the same `α`.

### Proof

Apply `A` to the fine fixed-point equation:

`A a* = α A s + (1-α) A P_R^T a*`
`      = α A s + (1-α) Q_R^T A a*`.

The right side is exactly the base restart equation. By KS-T05/Banach uniqueness, its solution is `\bar a*`. ∎

Equivalently, the result follows termwise from the Neumann series because (1) implies `A(P_R^T)^j=(Q_R^T)^j A` for every `j`.

## Theorem F2.2 — strong lumpability is the exact finite criterion for state-only fibre projection

For a fixed partition and fine kernel, a Markovian base kernel whose transition probabilities depend only on the source fibre exists exactly when (2) holds.

### Proof

If (2) holds, define `Q_R[i,j]` as the common total transition mass from any `x∈B_i` into `B_j`; this gives (1). Conversely, if a base state `i` has one well-defined transition mass to `j`, every fine state projecting to `i` must have that same aggregate target-fibre mass, yielding (2). ∎

This is parent-owned strong lumpability, not an ORION theorem.

## Theorem F2.3 — KSO multiscale warrant gate

Navigation commutation alone is insufficient for a KSO quotient/fibre state. For every registered revocation/evidence state `R`, three-valued liveness must also be constant inside each fibre for any atom-level predicate represented at the base. Otherwise the base state has no well-defined `LIVE/DEAD/UNKNOWN` value.

Thus a valid KSO multiscale certificate for `(partition, Γ)` requires, for every `R∈Γ`:

1. **transition lumpability** of `P_R`;
2. **warrant measurability** inside every fibre;
3. seed/query aggregation and any base answer functional to factor through the projection (MEG-20).

When a revocation changes fine gating so that either 1 or 2 fails, the certificate becomes `REFINE_REQUIRED`; the old base dynamics may not be reused by name.

## Cross-fibre transport

No extra theorem is obtained by naming certain edges “transport.” Every cross-fibre edge contributes to the aggregate sums in (2). If two fine states in one fibre export different total mass to another fibre, the partition is non-lumpable. A larger state that records the distinguishing fine context may restore lumpability; that is a state refinement, not a new navigation law.

## Hostile examples

The exact checker includes:

- a 4-state / 2-fibre lumpable kernel with exact rational restart pushforward equality;
- a cross-fibre mutant where one fine state exports a different aggregate mass, making base navigation ill-defined;
- a warranted partition that is transition-lumpable but has `LIVE` and `DEAD` fine states in one fibre under revocation, hence `REFINE_REQUIRED`;
- a revocation family where both transition and liveness criteria hold as a no-alarm case;
- a cemetery-state embedding showing the substochastic case reduces to ordinary stochastic lumpability without changing live-state projections.

## Parent subtraction

Strong lumpability of finite Markov chains (Kemeny–Snell line) owns the state-projection theorem. Markov-kernel intertwining is equivalent algebra. Hierarchical/multilevel methods supply additional computational schemes but are not needed to establish the current KSO commutation criterion. Graph-fibration/category language is optional notation unless a later OCM representation has structure not expressible as this finite kernel projection.

The only KSO-specific addition is the already-required warrant/answer measurability: a dynamically lumpable fibre may still be epistemically invalid if its members disagree in liveness or registered answers.

## Terminal

```text
MEG-09 = PARENT_LUMPABILITY_SUFFICIENT__KSO_ADDS_WARRANT_AND_ANSWER_MEASURABILITY
MULTISCALE_NAVIGATION_NOVELTY = NONE_ESTABLISHED
GENERAL_NOVELTY = NOT_ESTABLISHED
```

Reopen only if a future OCM multiscale object cannot be represented as a finite fine-state kernel plus projection, or if a claimed cross-scale operator has a discriminating theorem beyond strong lumpability/intertwining.
