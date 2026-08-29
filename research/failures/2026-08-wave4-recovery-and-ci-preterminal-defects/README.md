# Wave 04 Preterminal Defects — Retained Failure Record

## Status

Both defects were found before any Wave-04 scientific terminal was reported. They are retained because deleting them would make the final green state look easier and more direct than it was.

## D1 — Recovery answer key derived from the observation

### Failure class

`TAUTOLOGICAL_NATIVE_RECOVERY_EXPECTATION`

### Defective shape

The first fixture helper stored:

```text
expected_generalized = observed_generalized
```

inside every recovery case. The assessor would therefore certify any computed result, including a wrong one.

### Detection

Adversarial review asked whether corrupting an observed generalized terminal could fail. Under the initial helper, the answer key would have changed with it.

### Repair

- freeze an independent case-id-to-expected-terminal registry;
- combine observations with expectations only in `native_corpus_strict.py`;
- corrupt an observation in a test and require `INVALID_DECISION_DRIFT`;
- use only the strict corpus in exported/reported assessments.

### What the repair does not establish

It does not make the authored expected terminals externally correct. Native-expert review is still required.

## D2 — Plain Python did not import the src-layout package

### Failure class

`REFERENCE_CI_SRC_PATH_UNBOUND`

### Evidence

- Actions run `33072830735`: integrated pytest green, later plain-Python audit failed.
- Actions run `33072881041`: 91 pytest cases green, JSON parse green, then `ModuleNotFoundError: No module named 'orion_v2'`.

### Cause

Pytest read the repository `pythonpath` configuration, while standalone Python audit steps did not. The workflow had no job-level `PYTHONPATH` and did not install the package.

### Repair

Bind:

```yaml
env:
  PYTHONPATH: src
```

at the job level and rerun every step.

### Verified successor

Actions run `33073086747` completed with 91 tests, independent expectation audit and non-authority audit green.

## Authority

Neither repair grants scientific correctness, novelty, target-domain validity or framework admission.