# ORION-V2 Wave 04 Execution and Finding Report V0

**Subject branch:** `research/wave4-native-recovery-adaptation-corpus-20260827`

## Scope

Wave 04 tests whether generalized domain theories recover donor-native decisions and counterexamples as explicit special cases. It also separates native recovery from target-domain adaptation.

The corpus is constructed and finite. It grants no claim about naturalistic industry, clinical, legal, political, linguistic or scientific performance.

## Scientific objects

- `NativeRecoveryCase`
- `NativeRecoveryAssessment`
- `NativeRecoverySuiteAssessment`
- strict independent expectation registry
- seventeen-case native recovery corpus
- three target adaptation contracts

## Domains represented

- manufacturing quality and release;
- administrative/legal procedure;
- reliability engineering;
- medicine;
- metrology;
- psychometrics;
- political methodology;
- diachronic linguistics;
- robust control;
- control/planning;
- education and learning spaces;
- local/global reasoning;
- statistical decision theory;
- evidence synthesis;
- performative evaluation;
- research portfolio management.

## Retained self-audit findings

### F1 — tautological recovery answer key

The first corpus helper constructed each recovery map as:

```text
native terminal -> observed generalized terminal
```

That makes every observation recover itself and cannot detect decision drift.

The defect was found before reporting a Wave-04 result. The repaired path uses `native_corpus_strict.py`, whose expected generalized terminals are frozen independently of the computations. A hostile test corrupts an observed terminal and requires `INVALID_DECISION_DRIFT`.

The original computed fixture generator remains an internal observation source only and is not exported through the public research package. The strict wrapper owns all reported recovery assessments.

### F2 — plain-Python CI import path

GitHub Actions run `33072830735` and successor run `33072881041` both completed the integrated pytest suite successfully but failed afterwards because plain-Python audit steps did not have `src/` on `PYTHONPATH`.

This was a harness defect, not a scientific-test failure. It was repaired by binding `PYTHONPATH: src` at the workflow-job level. The red runs remain in Actions history.

## Integrated verification

GitHub Actions workflow:

```text
wave4-native-recovery
run_id = 33073086747
head_sha = 39d235d9a0be7fa2f66f0592142fb1ac2139ee62
runner = ubuntu-24.04
python = 3.12.14
```

Executed:

```text
python -m compileall -q src/orion_v2
python -m pytest -q
research/test JSON parse
independent expectation registry audit
non-authority audit
```

Observed:

```text
91 tests passed
0 test failures
JSON_PARSE_PASS
INDEPENDENT_EXPECTATION_REGISTRY_BOUND
AUTHORITY_BOUNDARY_PASS
workflow conclusion = success
```

## Native recovery result

```text
cases = 17
exact native recoveries = 17
sound over-approximate recoveries = 0 in built-in corpus
invalid decision drift = 0
assumption erasure = 0
counterexample loss = 0
cannot check = 0
```

These are known-answer results by construction against independently frozen expected terminals. They establish implementation non-vacuity and hostile-check reachability, not external validity.

## Target adaptation controls

- manufacturing process logic to scientific review: complete enough for target-native validation;
- engineering diagnosis to medicine: blocked by missing clinical calibration;
- political latent-scale linking to diachronic semantics: blocked by absent target-native tests.

`READY_FOR_TARGET_NATIVE_VALIDATION` does not establish successful adaptation.

## Main findings

1. Recovery expectations must be independent of generalized computations.
2. A common formal object is useful only when native terminals and counterexamples are recoverable.
3. Native recovery and target adaptation are different scientific gates.
4. Domain assumptions should be mapped or retained, never silently deleted.
5. Exact and sound/set-valued recovery require different terminals.
6. Negative controls are constitutive of a recovery claim, not optional validation.
7. The generalized layer can unify machine interfaces while leaving units, risks, institutions, populations, interventions and authority native.

## Limitations

- authored finite worlds;
- native source cards are not yet independently adjudicated;
- no real industrial, legal, clinical, political or linguistic datasets;
- no statistical uncertainty around recovery rates;
- no comparison with strongest native implementations;
- no protected target-domain transfer study;
- no novelty or adoption authority.

## Honest terminal

```text
WAVE_04_NATIVE_RECOVERY = CONSTRUCTED_EXACT_17_OF_17
INTEGRATED_REFERENCE_TESTS = GREEN_91
NATURALISTIC_NATIVE_VALIDATION = OPEN
TARGET_ADAPTATION_VALUE = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```