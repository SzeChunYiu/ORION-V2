# Exact certificate transport and revalidation

**Terminal:** `EXACT_FINITE_PARENT_PARITY`, with a separately registered deductive extension. **Status:** proposed Machine Epistemics foundation fragment; no novelty, independent-review, real-model-validity, or OCM-adoption claim.

This study asks what a scoped risk certificate can still support when the deployment distribution and an operator's failure event both change. It gives sharp finite bounds, attaining countermodels, an exact budgeted no-change-audit frontier, and a complementarity result: two audits can be useful together despite having no individual benefit.

Read `THEORY.md` and `SAMPLING.md` for assumptions/proofs and `CLAIMS.json` for claim-by-claim status. `PROTOCOL.md` was committed before the primary finite run. `ADDENDUM.md` explicitly records the later deductive extension. `SOURCES.md` records primary-parent reconstruction and its limits. `OCM_ABSORPTION.md` defines integration obligations without modifying OCM.

## Reproduce

From this directory, using Python 3.12 or later and only the standard library:

```sh
python -m py_compile transport.py checks.py extensions.py sampling.py test_transport.py verify_package.py
python -m unittest -v test_transport.py
python checks.py --verify RESULTS.json
python extensions.py --verify EXTENSION_RESULTS.json
python sampling.py --verify SAMPLING_RESULTS.json
python -O checks.py --verify RESULTS.json
python -O extensions.py --verify EXTENSION_RESULTS.json
python -O sampling.py --verify SAMPLING_RESULTS.json
python verify_package.py
```

Exit 0 means the stated finite checks passed; 1 means a failed invariant or result drift; 2 means missing/unsupported input, resource cap, or an unavailable artifact. Python optimization does not remove the exhaustive checker's explicit invariant checks. Local commands and actual environment are recorded in `RECEIPT.json`; local replay is not full-repository CI or independent replication.

## Measured finite coverage

| Check | Executed cells |
|---|---:|
| Fixed-event bound versus finite-simplex oracle | 320 |
| Joint event/distribution frontier versus oracle | 10,240 |
| Audit transcript semantics versus oracle | 8,640 |
| Audit cost frontier versus faithful knapsack parent | 28,160 |
| Joint frontier versus reachable-mass subset-sum parent | 10,240 |
| Supermodular audit-benefit inequalities | 13,720 |
| Nested audit monotonicity | 8,640 |
| Exact binomial limits / coverage cells | 270 / 612 |
| Pointwise prediction-disagreement inclusions | 1,536 |
| Adaptive-selection sample vectors | 16 |

The primary grid is every probability distribution on three atoms with denominator 3, every reference/mutable failure mask, and all grid-valued drift/change budgets. Two integer cost profiles are used for audits. These are related checks on a small complete model, not independent empirical samples. Bounds are also tested on explicit off-grid and zero-mass examples.

Fourteen boundary unit tests, ten applied mutation controls, fourteen manifest-field mutations, and five no-alarm controls supplement the grid. The manifest matcher deliberately returns `BINDING_MATCH_ONLY`, never scientific validity or action permission.

## Parent and ownership boundaries

TV extremum theory, subset-sum/knapsack, and convex-over-modular reasoning own the mathematics. The exact implementations agree with faithful parent algorithms; superiority is not inferred. `foundation_v1/**` (#312/#313), `decision_frontier_v1/**` (#314), historical outcomes, and OCM runtime paths are untouched.

Complete distributions and failure tables are public model assumptions, not free deployment knowledge. Statistical estimation, noisy/adaptive audits, realizable backend classes, independent proof review, and OCM runtime absorption remain open. A complete registry is not a complete science.

The later `SAMPLING_PROTOCOL.md` was committed before the finite-sample extension. It adds a conservative route using labeled reference errors and unlabeled paired-prediction disagreements, with confidence budgets and joint-drift assumptions kept explicit. It does not require a complete P/error table, but it still requires justified sampling, labels, fixed or simultaneously covered model selection, and deployment assumptions.
