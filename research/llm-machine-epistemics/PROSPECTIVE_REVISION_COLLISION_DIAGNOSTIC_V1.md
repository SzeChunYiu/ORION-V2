# Prospective Revision Collision Diagnostic V1

**Issue:** #51  
**Status:** operational diagnostic / decision-sufficiency corollary; **not claimed as new fibre mathematics**.  
**Purpose:** give the audit an exact falsifying witness that can be emitted for a compressed representation, rather than relying only on average accuracy.

## 1. Setup

Let:

- `H` be the present history;
- `Z=f(H)` be a representation under audit;
- `D_0(h)` be the registered acceptable current action semantics;
- `x` be a registered future evidence event;
- `delta(h,x)` be the resulting successor history when defined;
- `A^+_x(h)` be the set of acceptable Bayes-optimal future actions after `x`.

The present-equivalence gate additionally requires the histories to be equivalent for the declared linguistic-prediction target under the audit.

---

# 2. Collision definition

A **prospective revision collision** is a tuple

```text
(h, h', x)
```

such that:

1. `h != h'` and both have positive support;
2. `Z(h) = Z(h')`;
3. the declared linguistic prediction target treats `h,h'` as present-equivalent;
4. the registered current responsibility admits the same present action under both histories;
5. the same future evidence event `x` is jointly feasible from both histories;
6. after the event, the acceptable future-action sets are disjoint:

   `A_x^+(h) ∩ A_x^+(h') = empty`.

The last condition can be weakened for calibrated-loss responsibilities to require that no single compressed-state decision attains the full-history Bayes risk on both successors.

---

# 3. Certificate theorem

## Proposition RC1 — collision implies prospective insufficiency

If a prospective revision collision exists for representation `Z`, then no deterministic future decision rule using only `(Z,x)` can be exactly responsibility-sufficient on both collided histories.

### Proof

Because

`Z(h)=Z(h')`

and the future event `x` is the same, any deterministic decision rule `g(Z,x)` returns the same action at both histories.

But the registered acceptable future-action sets are disjoint. Therefore the common output cannot be acceptable for both histories. At least one positive-probability history incurs nonzero responsibility error/regret. ∎

### Ownership

This is a direct fibre/decision-sufficiency argument. It is an audit certificate, not an original representation theorem.

---

# 4. Converse in the finite exact deterministic-action setting

## Proposition RC2 — no collisions iff an exact future-action selector exists

Fix one evidence event `x` and a deterministic representation `Z`. Suppose each future acceptable-action set is nonempty.

There exists a deterministic selector

`g_x : Z -> A`

that chooses an acceptable future action for every positive-support history after `x` iff, for every `Z` fibre, the intersection

`intersection_{h in fibre} A_x^+(h)`

is nonempty.

### Proof

- If such a selector `g_x` exists, its chosen action belongs to every acceptable-action set in the fibre, so the intersection is nonempty.
- If every fibre has nonempty intersection, choose one action from each intersection and define `g_x` by that action. ∎

For several possible future evidence events, impose the condition event-by-event. For multi-step recursive update, successor-state/right-congruence constraints from the parent information-state/FSM theory are additionally required.

---

# 5. Present-matched collision subset

For #51, the practically relevant collision set is not every future collision. It is

`C_rev^matched(Z)`

containing only tuples that also pass the present-equivalence gate:

```text
language_target_equal
AND current_decision_equal
AND current_risk_within_registered_tolerance
AND same tool/resource access
```

A nonempty `C_rev^matched(Z)` is a direct certificate that **present matched performance does not imply prospective revision adequacy for that representation and episode family**.

---

# 6. Relation to the one-bit witness

The canonical provenance example emits exactly one collision family:

```text
h_A  = current claim supported via source A
h_B  = current claim supported via source B
Z_c(h_A) = Z_c(h_B)
current action = RETAIN for both
x = RETRACT(A)
future actions:
    h_A -> REOPEN
    h_B -> RETAIN
```

Thus

`(h_A,h_B,RETRACT(A))`

is a prospective revision collision for the compressed state.

The augmented state that retains the one-bit source identity separates the histories and removes the collision.

---

# 7. Empirical audit use

A future frozen-model/memory experiment should report both average metrics and **collision certificates** where the state intervention is explicit.

Preferred workflow:

1. freeze current language/current-decision equivalence;
2. identify candidate dormant variables;
3. construct matched history pairs differing only in the dormant variable and nuisance randomization;
4. apply a common future evidence event;
5. verify that full-history future actions differ;
6. test whether the compressed representation/memory still distinguishes the required future action;
7. emit the exact collision tuple and intervention receipt when it fails.

A collision is stronger evidence of state inadequacy than an aggregate revision error because it identifies the exact distinction the representation lost.

---

# 8. False-positive controls

Do **not** call a pair a prospective revision collision when:

- full history is itself insufficient to identify the future action;
- the future event differs across histories;
- the current decision already differs (that is a P1/current-state case);
- the representation conditions were not matched on current performance;
- later evidence itself reconstructs the dormant variable and the representation can use it;
- the alleged future action difference comes only from an arbitrary tie rule under `ANY_OPTIMAL_ACTION` semantics.

---

# 9. Diagnostic terminal vocabulary

- `REVISION_COLLISION_FOUND`
- `NO_REVISION_COLLISION_IN_REGISTERED_FINITE_UNIVERSE`
- `CURRENT_STATE_COLLISION_NOT_PROSPECTIVE`
- `FULL_HISTORY_NONIDENTIFIABLE`
- `FUTURE_EVIDENCE_RECONSTRUCTS_STATE`
- `TIE_ONLY__NO_REQUIRED_ACTION_SEPARATION`
- `CANNOT_CHECK_PRESENT_EQUIVALENCE`

Absence of a collision in a bounded suite does not establish universal prospective sufficiency.

---

# 10. Manuscript role

The diagnostic should appear as a practical certificate under the Prospective Revision Audit, not as an additional novelty claim.

Recommended statement:

> A prospective revision collision is a matched pair of histories that a representation merges today but that the same later evidence maps to incompatible future responsibility actions. Its existence certifies prospective insufficiency for the registered responsibility; the criterion is an ordinary decision-fibre argument used here as an auditable witness.
