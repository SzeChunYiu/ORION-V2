# Wave 05 Expert Decision Log V0

## Decision 1 — exact transport is a special case, not the default

Small probability or calibration differences should not force `NONCOMPARABLE`, but vague approximate similarity is unsafe.

**Disposition:** bind transition and observable errors separately and compare them with declared tolerances.

## Decision 2 — distance alone is not scientific preservation

Two systems can be numerically close while the best action changes when the nominal margin is small.

**Disposition:** add a task-relative decision-margin certificate and an explicit `DECISION_CHANGED` terminal.

## Decision 3 — use total variation only as a finite reference metric

Total variation makes pushforward kernel comparisons transparent and exact on finite spaces.

**Veto:** do not claim it subsumes Wasserstein, bisimulation metrics, stochastic simulation functions, trajectory metrics or domain-specific calibration distances.

## Decision 4 — composition must be conservative and typed

Numerical link errors may accumulate, while authority can only decrease. Semantic loss and unresolved assumptions do not cancel automatically.

**Disposition:** additive upper bounds, minimum authority and union of unresolved assumptions; return `CANNOT_CHECK` when dependence or propagation is not declared.

## Decision 5 — rectangularity/dependence is a scientific coordinate

Robust MDP parents show that uncertainty coupling affects both tractability and conservatism.

**Disposition:** the future solver state must track uncertainty-set/dependence structure, not only one epsilon.

## Decision 6 — approximate native recovery requires intervals or sets

A generalized result may soundly contain the native result without equaling it.

**Disposition:** keep exact recovery and sound over-approximation separate; add probabilistic coverage/calibration in later naturalistic studies.

## Decision 7 — authority remains external

An epsilon-bounded transport can still be unfit for use, outdated, or below the target evidence/authority threshold.

**Disposition:** numerical transport assessments grant no scientific truth, novelty or adoption.

## Open vetoes

1. No mechanized proof of the decision-margin or composition propositions.
2. No continuous-state or stochastic-hybrid adapter.
3. No empirical calibration of epsilon on real scientific models.
4. No covariance-aware multi-link uncertainty propagation.
5. No robust-policy benchmark against parent implementations.
6. No independent domain review.

## Current panel terminal

```text
EXACT_ONLY_GENERALIZATION = REJECTED
UNTYPED_APPROXIMATE_SIMILARITY = REJECTED
FINITE_ERROR_BOUNDED_TRANSPORT = REFERENCE_ADMITTED
PROTECTED_INCREMENTAL_VALUE = CANNOT_CHECK
```