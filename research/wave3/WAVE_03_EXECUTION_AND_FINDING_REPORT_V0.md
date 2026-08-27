# Wave-03 Execution and Finding Report V0

## Branch

```text
research/wave3-conservative-adaptation-calculus-20260827
```

Base:

```text
research/wave2-generalized-domain-theories-20260827
0aa679fdb7b8316781993ee4789ca977cb429e20
```

## Added reference modules

- `src/orion_v2/theory_transport.py`
- `src/orion_v2/meta_formalization.py`

## Added machine semantics

- rich scientific theories with epochs;
- typed resource intervals and calibrations;
- exact, conservative, decision-relative and sound interpretations;
- source/generalized round-trip laws;
- backward reflection inside the native image;
- explicit information-loss calculation;
- decisive/non-decisive counterexample reflection;
- transport expiration;
- certificate composition;
- target-native realization;
- finite satisfaction-condition checker;
- finite Galois-connection checker;
- abstract-transformer soundness checker;
- finite lens-law checker;
- old-language conservative-extension checker;
- Wave-02 finite-theory migration helper.

## Isolated development execution

```text
38 passed
0 failed
runtime approximately 0.12 seconds
network/model dependencies: none
```

## Full repository CI

GitHub Actions run `33073364546` executed the PR merge subject under CPython 3.12.14.

```text
compileall src/orion_v2 = PASS
pytest tests/unit = 106 passed in 0.32s
GENERALIZATION_RECEIPT_SCHEMA_V0.json = PARSED
THEORY_ADAPTATION_CERTIFICATE_SCHEMA_V1.json = PARSED
workflow conclusion = SUCCESS
```

This is package and finite-reference evidence. It is not a protected scientific transfer result.

The execution covered:

- exact interpretation;
- conservative extension;
- unsupported new old-image behavior;
- decision-relative quotient;
- declared and undeclared information loss;
- scalar and set-valued sound abstraction;
- relaxed and calibrated assumptions;
- resource understatement;
- evidence-bound unit conversion;
- authority amplification;
- hidden counterexamples;
- transport expiration;
- multi-link composition;
- target-native realization and validation;
- institution satisfaction;
- Galois connection;
- abstract-transformer soundness;
- lens round trips;
- old-language consequence conservativity.

## Defects discovered during Wave 03

### D1 — set-valued counterexample mismatch

The first implementation compared a singleton generalized set directly with a scalar native falsifier and incorrectly rejected a sound singleton abstraction.

Correction: counterexample values are compared through normalized value sets.

### D2 — exactness ignored calibrated unit equality

The first exactness gate compared native and generalized resource tuples byte-for-byte, rejecting an exact `hours -> minutes` calibration.

Correction: exactness is evaluated after evidence-bound calibration.

### D3 — Wave-02 set-valued preservation seam

The Wave-02 helper tests scalar membership in a generalized set but does not correctly express subset preservation when the native judgment is itself set-valued.

Wave 03 does not rewrite the Wave-02 result. It introduces a normalized set-inclusion law and records the earlier object as a weaker special case pending migration.

### D4 — exact interpretation needed stronger identity

The audit found that bijective states/actions alone could still permit extra generalized judgments or unequal authority.

Correction: exactness now requires bijective judgment correspondence, exact assumptions, authority and calibrated resources.

## Main findings

1. Generalization is a bundle of laws, not one relation.
2. Forward preservation is insufficient without reflection or typed approximation.
3. Conservative extension and exact interpretation must remain separate.
4. Native information loss must be computed, not merely declared.
5. Counterexample reflection needs a decisiveness grade.
6. Resource calibration belongs inside the transport proof.
7. Transport certificates are configuration- and epoch-dependent.
8. Composition degrades by weakest link.
9. Source and target sharing an envelope only authorizes target evaluation.
10. The strongest parent product already owns most formal structure.

## Honest terminal

```text
WAVE_03_REFERENCE_LAWS = 38_ISOLATED_PASS
FULL_REPOSITORY_REGRESSION = 106_PASS
MACHINE_SCHEMA_PARSE = 2_OF_2_PASS
PROTECTED_TARGET_TRANSFER = NOT_EXECUTED
C11_STANDALONE_STATUS = MERGE_UNLESS_SEPARATED
STRICT_ORION_RESIDUAL = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```
