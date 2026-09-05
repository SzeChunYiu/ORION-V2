# Machine Epistemics: causal evidence and lifecycle-safe transport V1

**Issue:** ORION-V2 #315. **Task:** ME-CAUSAL-TRANSPORT-V1. **Base:** `24566f00a9dc4425a438fcfac05d13c6b2d903db` (merged #310).

**Status:** written scoped theory + executable finite calibration. No claim of whole-foundation completion, novel causal theory, independent review, proof-assistant verification, empirical validation, OCM adoption, or architecture superiority.

This additive package closes a concrete specification gap: what a machine may infer from observations, interventions, counterfactual assumptions and source-to-target evidence, and what must reopen when those dependencies change. It does not edit OCM or any frozen predecessor result. The concurrent typed-foundation and read-only decision-frontier work remains separately owned (#312/#313/#314).

## Read and reproduce

Read `THEORY.md` for the 13 scoped statements/contracts and their written arguments, `CLAIMS.json` for statement hashes and exact test bindings, `SOURCES.md` for parent ownership/access limits, and `FRONTIER.md` for absorption obligations, unresolved research and the retained authoring failure.

From this directory, with Python 3.12 or later and no third-party packages:

```sh
python -m unittest -v test_causal_core
python mutation_audit.py
python run_checks.py --verify
```

The frozen `RECEIPT.json` records the actual generating interpreter/platform. Verification reruns the suite and compares deterministic results and all nine bound source/document bytes. A successful replay on a different Python version does not rewrite the generating environment. The dedicated GitHub workflow runs only this package on Python 3.12/3.13; workflow configuration is not included in the package receipt and is reviewed as a separate Git artifact.

Exit codes are `0=PASS`, `1=defect`, `2=CANNOT_CHECK`. A missing artifact or optimized interpreter (`python -O run_checks.py --verify`) cannot pass. The runner refuses to overwrite a receipt. A successor can use `python run_checks.py --write-receipt --receipt NEW_RECEIPT.json` only with an explicitly disclosed successor identity, not as a way to hide a failed verification.

No network, stochastic model call, real external action, dataset download or protected empirical run occurs. Local verification was performed in this session's isolated Linux container, not the operator's Mac/laptop/LUNARC. The full repository was not cloned or tested: direct clone failed DNS resolution; connected GitHub reads/writes provide repository custody.

## Results and boundaries

The local baseline contains **38 unit tests**, zero failures/errors/skips, and **8 applied source mutants**, each killed by its intended assertion rather than an import error. The first test run had one incorrect expectation; its correction and unchanged core evaluator are recorded in `FRONTIER.md`, not erased.

Calibration reports denominators separately: 64 binary structural models, 1,152 structural evaluations, 576 normalized intervention marginals, 672 defined counterfactual queries and 864 undefined-condition refusals; 494 response distributions yielding 240 sharp-bound cells; 2,025 transport comparisons; 1,800 total-variation event checks and 1,113 conditional checks; 125 adaptive transcript laws, 348 binary decision rules, 1,725 rules including abstention, and 20 sharp transcript witnesses. These are finite deterministic checks, not independent empirical samples or a proof of all-size claims. The reporting pass is not added to the separate pass inside the unit suite.

| Claim | Result / contract | Scientific scope |
|---|---|---|
| CT-01 | Unique surgical SCM semantics, normalized laws | Finite acyclic total-table models |
| CT-02 | Identification is constancy over a nonempty compatible class | Class-relative; conflict/undefined are not truth |
| CT-03 | Same observations, different intervention effects | Explicit two-model counterexample |
| CT-04 | Same observed-variable interventions, different counterfactuals | Shared-latent dependence is extra information |
| CT-05 | Sharp binary counterfactual interval | Exact marginals, unrestricted response coupling |
| CT-06 | Retraction widens compatible answer sets | Conjunctive constraints; no minimal-repair cost claim |
| CT-07 | Sharp distribution-plus-mechanism transport envelope | Declared exact drift bounds and common estimand |
| CT-08 | Sharp conditional-TV amplification bound | Common event of positive probability in both laws |
| CT-09 | Conditional risk-transport corollary | Relevant joint law; risk is not individual truth |
| CT-10 | Adaptive transcript and error/abstention frontier | Common policy, bounded horizon, uniform conditional bounds |
| CT-11 | Noninjective physical effects have no state-only inverse | Evidence erasure is not compensation |
| CT-12 | Model/query/dependency identity contract | Hash match is not authentication, truth or adoption |
| CT-13 | Pairwise optimal couplings need not glue | Parent-owned counterexample and joint-witness checker |

SCM semantics, response-function bounds, coupling, testing and marginal feasibility are inherited from established parents. The contribution offered here is their explicit machine-facing integration with type boundaries, retraction rules, counterexamples and replayable checks. No parent-subtraction residual is demonstrated.

## Known open obligations

Independent proof reconstruction, full neighboring-paper reconstruction, real intervention/measurement validity, time-uniform statistical certificates under adaptive experiments, efficient causal repair, scalable global compatibility, and OCM runtime absorption remain open. `FRONTIER.md` defines their precise targets and falsifiers. Passing this package does not close #197 or any OCM milestone.
