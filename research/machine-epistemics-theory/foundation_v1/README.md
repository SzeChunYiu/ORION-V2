# Machine Epistemics: typed foundation V1

Research issue: ORION-V2 #312. Source baseline: `24566f00a9dc4425a438fcfac05d13c6b2d903db` (2026-09-04, #310).

This package completes a **bounded foundation contribution**, not all of Machine Epistemics. It supplies sixteen written theorem/counterexample arguments, an executable exact reference calculus, a complete disposition map for the 35 current MEG atlas rows, a hash-bound calibration receipt, and an OCM absorption contract. Original theory, protected results, manuscripts and OCM runtime files remain untouched.

## Read and run

Start with `THEORY.md`, then `ATLAS_MAP.json` and `OCM_HANDOFF.md`. `SOURCES.md` distinguishes inspected primary texts from abstract-only leads. `FRONTIER.md` specifies the remaining research problems. `REVIEW.md` records constructive and hostile analytical roles; those roles are not independent reviewers.

From this directory, using Python 3.12 or newer and only its standard library:

```sh
python verify_bundle.py
python check_calculus.py --output /tmp/me-foundation-results.json
python -O verify_bundle.py
python verify_bundle.py --hostile
```

Exit 0 means the declared finite checks and bindings pass; 1 means a detected defect; 2 means a required artifact/tool/check is unavailable. No reduced mode, no live model calls, no external effects and no third-party Python dependencies. Case enumeration is development calibration, not a protected empirical experiment or a random sample from all possible machines.

The recorded run contains **530,312 explicit checks across 11 groups, with 61 named distinction/rejection/no-alarm controls**. These are assertion counts, not independent replications. The theorem arguments have separate authority from the finite enumerations. See `RESULTS.json` for all denominators.

## What changes scientifically

Population coverage is not individual truth; actionability is typed separately. Inconsistent assumptions require a common compatible support, not Boolean multiplication of isolated LIVE labels. Structural rollback must restore effective normalization. Graded navigation has a fixed-normalization contraction/error/perturbation theorem. Query-specific learning can retain a correct answer without globally identifying the learner's hypothesis. Dependency locality, termination, snapshot consistency, codec invariance and information accounting all acquire explicit conditions and counterexamples to overbroad versions.

These constructions are parent-owned or compositions of established machinery. They are not a claim of architectural superiority or field novelty. A fuller source/priority search and independent assumption review remain necessary for any new-contribution claim.

## Proof assistant and custody

`Foundation.lean` is a small logical bridge: compatible witnesses, interval verdicts, agreement, type separation and integer work. It does **not** formalize the probability or matrix theorems. `verify_lean.py` builds it with Lean 4.19.0, audits reported axioms, and tests rejection of a false theorem, an injected axiom and an admitted proof. It returns CANNOT_CHECK if Lean is unavailable. The authoring container has Python 3.13.5 but no Lean binary or outbound Git access; remote CI results must be reported separately rather than invented.

`RECEIPT.json` binds the exact package files and results, not a changing repository-wide README. Its body digest detects accidental receipt changes, not malicious rewriting of both content and hash. Git commit identity and external review supply separate custody. A fresh run reproduces the result object and verifies byte bindings; it does not certify all mathematical assumptions.

Current local terminal: `EXACT_CALIBRATION_PASS / WRITTEN_PROOFS_PENDING_INDEPENDENT_REVIEW`.
Full foundation: `OPEN`. OCM runtime adoption: `NOT_GRANTED`. Independent review: `NOT_OBTAINED`. Novelty and superiority: `NOT_CLAIMED`.
