# ORION-V2 Wave 05 Execution and Finding Report V0

**Subject branch:** `research/wave5-stochastic-approximate-generalization-20260827`

## Scope

Wave 05 extends exact finite generalization to finite stochastic systems with explicit transition, observable, decision, authority and composition error semantics.

It is a reference implementation and known-answer study only.

## Added machine objects

- `FiniteStochasticTheory`
- `StochasticTransport`
- `StochasticTransportAssessment`
- `DecisionRobustnessAssessment`
- `StochasticTransportLink`
- `StochasticChainBound`

## Reference semantics

- pushforward source transition distributions through a declared state map;
- compare against target kernels with total variation distance;
- compare registered numeric observables separately;
- require transport epochs to equal source/target theory epochs;
- certify a unique decision only when nominal margin exceeds twice the value-error bound;
- compose only connected theory/epoch chains with declared uncertainty propagation;
- add transition/observable upper bounds conservatively and take minimum authority.

## Preterminal design findings

### Epoch-presence was not epoch-binding

The first assessor checked that epoch fields were nonblank but did not compare them with the source/target theory epochs. A stale transport could therefore pass.

**Repair:** mismatch now returns `INVALID_EPOCH`; a hostile test binds the failure.

### Error links were not a chain

The first composition function added error bounds from arbitrary links without checking that one link's target theory/epoch matched the next link's source theory/epoch.

**Repair:** every adjacent endpoint and epoch must compose; otherwise the result is `CANNOT_CHECK` with a chain warning.

## Integrated verification

GitHub Actions:

```text
workflow = wave5-stochastic-generalization
run_id = 33074185839
head_sha = acaa0a384772a7011b095f6880fa7d41a22800a8
runner = ubuntu-24.04
python = 3.12.14
```

Executed:

```text
python -m compileall -q src/orion_v2
python -m pytest -q
stochastic non-authority audit
research/test JSON parse
```

Observed:

```text
102 tests passed
0 failures
STOCHASTIC_AUTHORITY_BOUNDARY_PASS
JSON_PARSE_PASS
workflow conclusion = success
```

## Known-answer results

- exact isomorphic stochastic transport: exact;
- micro/macro kernel transport at TV 0.05 and observable error 0.04: epsilon-bounded;
- declared epsilon 0.04 against observed TV 0.05: invalid transition error;
- stale source epoch: invalid epoch;
- nominal decision gap 0.30 with error bound 0.10: preserved by margin;
- gap exactly 0.20 with error bound 0.10: not certified;
- small numerical error with observed winner reversal: decision changed;
- connected two-link chain: error bounds accumulate and authority falls to the minimum;
- disconnected or epoch-mismatched chain: cannot check;
- undeclared dependence: cannot check;
- invalid probability row: construction rejected.

## Main findings

1. Exact transport is one zero-error case of a broader bounded relation.
2. Transition, observable/calibration, semantic and authority coordinates should not be collapsed into one similarity score.
3. Small model distance does not imply decision preservation.
4. Decision stability is task- and margin-relative.
5. Error-chain composition requires connected identities, epochs and a declared propagation/dependence model.
6. Numerical validity cannot amplify authority.
7. Total variation is a transparent finite reference metric, not a universal stochastic abstraction theory.
8. Strong parent ownership from probabilistic verification, stochastic control, robust MDPs, experiment comparison and metrology remains.

## Limitations

- finite state/action spaces;
- one-step kernel comparison;
- total variation only;
- numeric scalar observables;
- additive chain upper bounds;
- no continuous or hybrid systems;
- no trajectory/specification satisfaction bounds;
- no learned uncertainty set;
- no naturalistic stochastic adapter;
- no independent review or protected comparison.

## Honest terminal

```text
WAVE_05_STOCHASTIC_TRANSPORT = FINITE_REFERENCE_GREEN_102_TESTS
DECISION_MARGIN_CERTIFICATE = KNOWN_ANSWER_GREEN
NATURALISTIC_STOCHASTIC_TRANSFER = OPEN
PARENT_SUBSUMPTION = HIGH
PROTECTED_VALUE = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```