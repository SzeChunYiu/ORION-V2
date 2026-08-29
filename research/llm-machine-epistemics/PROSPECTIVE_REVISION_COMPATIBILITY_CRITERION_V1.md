# Prospective Revision Compatibility Criterion V1

**Issue:** #51  
**Purpose:** strengthen the pairwise revision-collision diagnostic into a complete one-step exact criterion under `ANY_OPTIMAL_ACTION` semantics.

This is a decision-sufficiency/intersection result, not a new mathematical novelty claim. Its purpose is to prevent the empirical audit from falsely treating “no disjoint pair found” as proof that a compressed state is prospectively adequate.

## 1. Setup

Let:

- `H` be the registered current history space;
- `Z=Z(H)` be the representation under audit;
- `x` be a registered common future evidence event;
- `delta(h,x)` be the successor history when the event is feasible/defined;
- `A_x^*(h)` be the acceptable Bayes-optimal future action set at `delta(h,x)`.

For a representation value `z` and event `x`, define the reachable representation/event cell

\[
\mathcal C(z,x)
=
\{h:\; Z(h)=z,\;\delta(h,x)\text{ is defined}\}.
\]

Define its **future compatibility set**

\[
\boxed{
\mathcal I(z,x)
=
\bigcap_{h\in\mathcal C(z,x)} A_x^*(h)
}
\]

for each nonempty cell.

## 2. Proposition — exact one-step compatibility

There exists a deterministic future decision rule

\[
g: (z,x)\mapsto a
\]

that is acceptable for **every** registered history in every representation/event cell iff

\[
\boxed{
\mathcal I(z,x)\neq\varnothing
\quad\text{for every nonempty }\mathcal C(z,x).
}
\]

### Proof

**Necessity.** Suppose such `g` exists. For any `h` in `C(z,x)`, correctness requires

\[
g(z,x)\in A_x^*(h).
\]

The same action `g(z,x)` therefore belongs to every acceptable-action set in that cell, so it lies in their intersection.

**Sufficiency.** If every nonempty `I(z,x)` is nonempty, choose one action from each intersection and define `g(z,x)` to be that action. By construction it is acceptable for every history represented by the cell. ∎

## 3. Pairwise collision is sufficient but not complete

The existing pairwise prospective-revision collision

\[
A_x^*(h)\cap A_x^*(h')=\varnothing
\]

for two histories with the same `Z` value is a simple certificate that

\[
\mathcal I(z,x)=\varnothing.
\]

But the converse is false when more than two histories occupy a cell.

### Mandatory three-history counterexample

Let three merged histories have future acceptable-action sets

```text
A1 = {a,b}
A2 = {b,c}
A3 = {a,c}
```

Then

```text
A1 intersect A2 = {b}
A1 intersect A3 = {a}
A2 intersect A3 = {c}
```

so **every pair overlaps**, yet

```text
A1 intersect A2 intersect A3 = empty.
```

No deterministic rule seeing only the merged state and common evidence can choose an action acceptable for all three histories.

Therefore:

> **absence of a pairwise collision does not certify prospective revision adequacy.**

The complete one-step certificate is the full cell intersection.

## 4. Unique-action special case

If every future acceptable-action set is a singleton, then any two histories requiring different future actions have disjoint sets. In that special case, pairwise collision detection is complete.

The canonical one-bit provenance witness uses unique future actions `REOPEN` versus `RETAIN`, so its pairwise certificate remains exact and unchanged.

## 5. Protocol consequence

Protocol V2's collision analysis must be interpreted as:

1. pairwise disjoint-set collision = **easy positive insufficiency certificate**;
2. no pairwise collision = **not a sufficiency result** unless action sets are singleton;
3. for general tied-action cells, compute/establish the full joint intersection `I(z,x)`;
4. empty joint intersection = exact one-step prospective incompatibility;
5. nonempty joint intersection = one-step action compatibility only; multi-step updateability can still require a richer recurrent state/right-congruence test.

## 6. Audit output fields

For each registered `(z,x)` cell, an implementation should emit:

```text
cell_id
history_count
future_action_sets
pairwise_disjoint_witnesses
joint_acceptable_action_intersection
one_step_compatible = true/false/CANNOT_CHECK
```

A large cell may use a symbolic/constraint representation of action sets instead of materializing all elements, but the meaning must remain the joint intersection.

## 7. Multi-responsibility extension

When several responsibilities must be satisfied simultaneously, define the acceptable **joint action-vector set** for each history and apply the same intersection criterion. Do not intersect each responsibility independently if action choices are coupled.

## 8. Horizon boundary

The criterion above is exact for one registered future evidence event when the future decision is computed from `(Z,x)`.

For a multi-step evidence horizon, one-step compatibility at every individual event does not by itself establish existence of one recursively updateable compressed state. The dynamic/right-congruence construction remains the appropriate finite exact parent mechanism.

## 9. Publication classification

```text
PAIRWISE_COLLISION = SUFFICIENT_WITNESS_NOT_COMPLETE_GENERAL_TEST
JOINT_CELL_INTERSECTION = COMPLETE_ONE_STEP_ANY_OPTIMAL_ACTION_CRITERION
CANONICAL_ONE_BIT_WITNESS = UNCHANGED
MATHEMATICAL_NOVELTY = PARENT_STYLE_DECISION_SUFFICIENCY_COROLLARY
AUDIT_VALUE = HIGHER_DIAGNOSTIC_COMPLETENESS
```
