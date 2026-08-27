# ORION-V2 Wave 05 — Stochastic and Approximate Generalization V0

**Status:** finite stochastic reference semantics and protocol design. No naturalistic, asymptotic, novelty, or adoption authority.

## 1. Why exact finite recovery is insufficient

Wave 03 compiled exact finite decision envelopes. Wave 04 required native recovery. Real scientific theories usually include sampling error, stochastic transitions, measurement noise, uncertain parameters, approximate abstractions and decision margins.

An exact relation can therefore fail for harmless numerical drift, while an untyped “approximately similar” relation can hide a decision reversal.

Wave 05 introduces a bounded form:

```text
native stochastic theory
  -- state/action map -->
approximate generalized theory
  + transition error
  + observable error
  + authority ceiling
  + assumption/epoch bindings
  + decision-margin certificate
```

The central question is not whether two models are close in one generic metric. It is whether the registered scientific decisions remain justified under explicit error budgets.

## 2. Expert cell

### Probabilistic verification lead

Background: probabilistic bisimulation, labelled Markov processes, approximate process metrics and formal abstraction.

Role: define pushforward transition comparisons and total-variation error bounds.

Veto: zero distance, bounded distance and unmeasured distance are different terminals.

### Stochastic control and robust decision lead

Background: robust MDPs, stochastic simulation functions, uncertainty sets and safe policy refinement.

Role: determine when an abstract policy/decision remains valid under transition uncertainty.

Veto: a nominal optimum may not be promoted when its margin is smaller than the error budget.

### Statistical decision and experiment-comparison lead

Background: Blackwell/Le Cam comparison, loss functions, sufficient statistics and value of information.

Role: connect model distance to task-relative decision stability.

Veto: small model distance cannot substitute for a registered loss/decision family.

### Measurement and metrology lead

Background: calibration chains, uncertainty propagation, measurement invariance and error budgets.

Role: separate transition uncertainty, observable/calibration uncertainty and semantic loss.

Veto: independent uncertainty terms may not be added when dependence or propagation rules are unidentified.

### Native-domain and governance lead

Role: preserve target-native units, risk, authority, populations, interventions and epochs.

Veto: an epsilon-bounded mapping grants no target authority.

## 3. Finite stochastic theory

```text
STheory = (
  states,
  actions,
  transition_kernel P(. | s,a),
  registered_observables,
  source_ids,
  assumptions,
  epoch
)
```

Every kernel row is a probability distribution over declared states.

## 4. Approximate stochastic transport

A transport consists of:

```text
Transport = (
  alpha : source_state -> target_state,
  beta  : source_action -> target_action,
  registered_observables,
  declared_transition_epsilon,
  declared_observable_epsilon,
  source/target epochs,
  authority ceiling
)
```

For every source state/action, the source transition distribution is pushed forward through `alpha` and compared with the target transition kernel using total variation distance:

```text
TV(p,q) = 0.5 * sum_x |p(x)-q(x)|
```

Registered numeric observables are compared by absolute deviation after state mapping.

## 5. Transport terminals

```text
EXACT_STOCHASTIC_TRANSPORT
EPSILON_BOUNDED_STOCHASTIC_TRANSPORT
INVALID_TRANSITION_ERROR
INVALID_OBSERVABLE_ERROR
CANNOT_CHECK
```

The assessment reports observed maximum errors separately from declared bounds. It grants no scientific truth, novelty or target adoption.

## 6. Decision-margin certificate

Let nominal action values be `V(a)` and let every transported value have absolute error at most `eta`.

If the nominal best action has margin:

```text
gap = V(best) - max_{a != best} V(a)
```

then `gap > 2*eta` is sufficient for the best action to remain unique under all coordinate-wise perturbations bounded by `eta`.

Wave 05 uses this elementary robust-margin certificate as a transparent sufficient condition. It is not claimed to be necessary.

Terminals:

```text
DECISION_PRESERVED_BY_MARGIN
DECISION_NOT_CERTIFIED_MARGIN_TOO_SMALL
DECISION_CHANGED
CANNOT_CHECK
```

## 7. Composition

For a chain of finite reference links, Wave 05 records conservative upper bounds:

```text
transition_error <= min(1, sum link transition errors)
observable_error <= sum link observable errors
authority_ceiling = min link authority ceilings
unresolved assumptions = union
```

This additive rule is deliberately conservative and applies only when the declared link errors are compatible upper bounds. Dependence, cancellation or nonlinear propagation require target-native rules and otherwise return `CANNOT_CHECK`.

## 8. Native recoveries to add

Wave 05 starts with transparent finite cases:

- noisy engineering sensor abstraction;
- stochastic clinical test abstraction;
- robust versus nominal policy margin;
- calibration-chain error accumulation;
- an approximate model with small transition error but a decision reversal because the decision margin is too small;
- a chain whose numerical error remains bounded but whose authority ceiling prevents promotion.

These are constructed non-vacuity cases. Naturalistic adapters remain open.

## 9. Parent ownership

The mathematical core is strongly parent-owned by:

- probabilistic bisimulation and testing;
- metrics for labelled Markov processes;
- stochastic simulation functions and abstraction-based synthesis;
- robust and distributionally robust MDPs;
- statistical experiment comparison;
- metrological uncertainty propagation.

The only candidate ORION residual is an integrated scientific receipt connecting approximate transport, native recovery, decision margin, authority, provenance, epoch and reopening.

## 10. Hostile controls

- malformed probability distributions;
- state or action map not total;
- transition TV exceeds declared epsilon;
- observable error exceeds declared epsilon;
- tiny transition distance but changed protected decision;
- nominal margin exactly equal to `2*eta`—not certified;
- chained error budget exceeding one;
- unknown dependence in uncertainty composition;
- numerical transport valid but target epoch missing;
- numerical transport valid but authority amplified.

## 11. Paper implications

- **C02:** gains stochastic/approximate relation grades.
- **C04:** action selection must consume decision-margin and robust-policy certificates.
- **C06:** comparability gains separate transition/observable/semantic uncertainty budgets.
- **C07:** uncertainty dependence and covariance become unavoidable.
- **C11:** exact compiler becomes one special case of bounded transport; standalone status remains unearned.
- **Possible C12:** only if stochastic transport plus decision/authority receipts demonstrates a distinct theorem or protected transfer result.

## 12. Current terminal

```text
WAVE_05_FINITE_STOCHASTIC_TRANSPORT = IMPLEMENTED_REFERENCE
DECISION_MARGIN_CERTIFICATE = IMPLEMENTED_REFERENCE
COMPOSITION_RULE = CONSERVATIVE_FINITE_BOUND
NATURALISTIC_STOCHASTIC_ADAPTATION = OPEN
PROTECTED_VALUE = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```