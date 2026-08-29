# Component Value Reference Execution Report V1

**Date:** 2026-08-27  
**Scope:** transparent local known-answer tests for the ORION-V2 component value and efficiency protocol.  
**Authority:** none beyond the finite reference cases.

## Frozen objects

- implementation: `src/orion_v2/component_value.py`;
- tests: `tests/unit/test_component_value_wave6.py`;
- protocol: `research/evaluation/COMPONENT_VALUE_AND_EFFICIENCY_PROTOCOL_WAVE06_V1.md`.

## Local execution before commit

```text
14 tests passed
0 tests failed
```

## Tested distinctions

- critical scientific failures cannot be compensated by speed or a higher scalar quality score;
- a Pareto frontier preserves quality–cost trade-offs rather than forcing one weighting;
- removal causing false completion marks a component `NECESSARY` on the authored case;
- a strongest parent that matches full performance/cost yields `PARENT_REPLACEABLE`;
- a component adding only cost yields `REDUNDANT_DRAG`;
- a component reducing cost with no scientific change yields `EFFICIENCY_IMPROVING`;
- removal repairing a critical/quality failure yields `HARMFUL`;
- mixed gains and harms yield `CONTEXTUAL`;
- unmatched arms yield `CANNOT_CHECK`;
- 2×2 interventions distinguish complementary, substitutable, additive and context-dependent pairs;
- invalid full references are excluded from interaction attribution.

## Non-claims

The run does not establish the value of any real K0–K6 component. It does not prove that the declared cost vector is complete, that pairwise interactions capture all higher-order coalitions, or that a component will generalize beyond frozen cases.

## Next required evidence

1. bind component identities and replacement arms before outcomes;
2. run leave-one-out and parent replacement on protected parity and paper benchmarks;
3. record latency, compute, memory, annotation and implementation/failure burden;
4. run pair interactions for suspected substitutes/complements;
5. repeat on a materially different domain;
6. independently adjudicate semantic outcomes;
7. issue component-specific survival/removal receipts.

## Terminal

```text
COMPONENT_VALUE_REFERENCE_TESTS = GREEN_14
REAL_COMPONENT_SURVIVAL = CANNOT_CHECK
PARENT_REPLACEMENT_LOGIC = EXECUTABLE_REFERENCE_ONLY
PARETO_COST_ACCOUNTING = EXECUTABLE_REFERENCE_ONLY
ARCHITECTURE_AUTHORITY = NONE
KERNEL_FREEZE = BLOCKED
```
