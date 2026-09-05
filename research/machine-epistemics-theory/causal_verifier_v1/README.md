# Causal and verifier foundation V1

**Delivered scope:** ten self-contained formal statements/counterexamples in `THEORY.md`, a stdlib exact reference, a reproducible finite calibration, 31 unit/hostile tests including eight applied mutants, primary-source boundaries, and an OCM absorption contract. **Not delivered:** whole Machine Epistemics closure, an OCM runtime, learned causal discovery, finite-sample statistical guarantees, independent review, or novelty.

Research identity `ME-CAUSAL-VERIFIER-V1`; V2 issue #316; base `24566f00a9dc4425a438fcfac05d13c6b2d903db`. This additive directory avoids the active foundation work #312/#313 and decision-frontier #314. It preserves the existing #310 atlas rather than rewriting it. Parents and source-access limitations are explicit in `SOURCES.md`.

## Exact findings

| Object | Result | Interpretation |
|---|---:|---|
| Boolean structural causal models | 64 | Public finite model family, not learned knowledge |
| Observational / interventional / response-law classes | 10 / 34 / 36 | Two strict information boundaries |
| Response classes per interventional class | 32 singleton, 2 doubleton | At most one additional coupling bit within this family |
| Structural execution vs response-law integration | 576 agreements | Two code paths, same author |
| Direct entailment vs bitset entailment | 12,288 agreements | Shared evidence predicates disclosed |
| Positive/negative support-retraction checks | 24,576 | Exact over all registered evidence subsets |
| Reverse-order reinstatement checks | 768 | Mathematical record replay, not a runtime persistence test |
| Binary coupling bound checks | 4,544 over 494 tables | Sharp dependency-robust bounds, not samples |
| Unit / mutation tests | 31 / 8 | Mutants are a subset of the 31 tests |

The executable lifecycle retains a supported intervention effect when a counterfactual joint certificate is revoked. Two 5%-error verifiers have a dependency-robust joint-error interval [0,5%]; 0.25% requires an additional independence premise. These are parent-owned mathematical results, not evidence that OCM outperforms a matched conventional solver.

## Reproduce from repository root

```sh
python tests/unit/test_me_causal_verifier_v1.py
python research/machine-epistemics-theory/causal_verifier_v1/causal_verifier.py \
  --verify research/machine-epistemics-theory/causal_verifier_v1/CALIBRATION.json
python -O research/machine-epistemics-theory/causal_verifier_v1/causal_verifier.py \
  --control fail          # expected exit 1
python -O research/machine-epistemics-theory/causal_verifier_v1/causal_verifier.py \
  --control cannot-check  # expected exit 2
python research/machine-epistemics-theory/causal_verifier_v1/verify_receipt.py
```

Local environment, actual command exits, deterministic body digest, source SHA-256 bindings and limitations are in `RECEIPT.json`. Results were executed in an isolated Linux analysis container, not the operator's Mac/billy-old/LUNARC. Full repository CI remains separate. The included workflow requests Python 3.12/3.13 replay; those remote outcomes are not pre-claimed.

Scientific terminal: **PARENT_OWNED_FORMAL_FOUNDATION**. This means a tested integration of established foundations with explicitly proved scope, not a breakthrough, a globally complete theory, or an adoption decision. Unresolved research and cross-lane handoff are in `THEORY.md` §14 and `ABSORPTION.md`.
