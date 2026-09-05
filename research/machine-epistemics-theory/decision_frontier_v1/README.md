# Machine Epistemics: decision and verification frontier V1

Research child **ORION-V2 #314**, base `24566f00a9dc4425a438fcfac05d13c6b2d903db`, additive to #310. This directory is separate from `foundation_v1/`, already claimed by #312/#313. No existing result, freeze, runtime or paper is overwritten.

## Result

A finite, exact, scope-explicit foundation for deciding **what evidence to acquire next**, distinguishing observational impossibility from insufficient budget, and comparing persistent memory against later verification cost. `THEORY.md` gives twelve numbered written theorem/boundary sections DF-00..DF-11. The mathematics is parent-aligned (decision-region determination, decision trees, covers and Bellman optimality); no novelty or architecture superiority is asserted.

Two important limits are preserved. A complete finite model is not a certificate that the real world belongs to that model. And the compression frontier assumes the encoder has observed the history before compressing it: that acquisition and the codebook are charged, not a free hidden-world oracle. DF-11 gives the exact successor for an encoder limited to a registered observation signal.

## Reproduce

From this directory, on Python 3.11 or newer, with no third-party packages:

```bash
python -m unittest -v test_frontier
python run_checks.py --verify
```

`run_checks.py` exits 0 for a matching finite receipt, 1 for a mismatch/check failure, and 2 for an unavailable prerequisite or instrument cap. It reports exact denominators. These are analysis-container/CI calibrations, not authorized protected experiments. Written all-size finite-family proofs and bounded executable checks are different evidence types. No proof assistant was run.

## Files

`THEORY.md` contains assumptions, proofs, counterexamples and resource accounting. `frontier.py` is the stdlib reference with policy and Bellman-certificate checkers. `test_frontier.py` contains exhaustive table/tree comparison and hostile fixtures. `run_checks.py` writes/verifies `RESULTS_V1.json`. `SOURCES_AND_REVIEW.md` records primary-source ownership and internal review limits. `OCM_ABSORPTION.md` states the application and authority contract. `INTEGRATION_V1.json` maps specific foundation gaps without claiming the entire atlas is closed.

## Evidence ceiling

Finite enumeration covers 5,488 registered three-world tables, not arbitrary OCM workloads. The reference tree enumerator and Bellman checker use different code paths but were authored in the same session, so they are not independent-group replication. The closure identifier is an input assumption, not a validated external attestation. No OCM adoption, main-branch merge, broad Machine Epistemics completion, external demarcation, or publication authority is granted by this directory.
