# Temporal validity V2

**Terminal: PARENT_SUFFICIENT, within the registered finite revision model.**
This is an additive successor to PR #326's revision-consistency package, not an
upgrade of its result. The original V1 artifacts and receipt are unchanged.

The practical question is when a claim remains admissible despite unobserved
updates. We compute the largest subset of admissible states from which no allowed
revision can reach an inadmissible state. With partially known transitions we use
separate lower and upper relations; missing updates are never assumed absent.

`MODEL_PERSISTENT` means the universal persistence property holds in every allowed
completion. `MODEL_PERSISTENCE_REFUTED` means the universal guarantee fails in every
completion, NOT that every actual execution fails or the current claim is false.
`CANNOT_CHECK` means the extremes admit different answers, no model is bound, or
initial belief is empty. None of these model outputs creates scientific authority.

## Reproduce

From repository root, with Python >=3.12 and standard library only:

```sh
python research/machine-epistemics-theory/revision_consistency_v1/temporal_v2/run.py --verify
python research/machine-epistemics-theory/revision_consistency_v1/temporal_v2/run.py --selftest
```

The verifier reruns 28 unit tests, the whole registered finite calibration and all
source bindings. Exit 0 = checked, 1 = defect, 2 = missing/unavailable input. The
selftest plants source drift, missing source, omitted binding and false independence.
`calibrate.py` prints the deterministic result for fresh-process comparison.

## Executed calibration

530 directed graphs, self-loops included, over n=1,2,3; 4,164 graph/predicate kernels;
28,868 nonempty-belief cases: 5,570 persistent and 23,298 refuted. Independent parent
comparison: 0 disagreements. All 12,420 start/predicate/graph cases compare shortest
paths; 9,298 adverse paths verify.

81 two-state lower/upper envelopes produce 972 predicate/belief cases: 297 persistent,
621 refuted and 54 CANNOT_CHECK. All 3,072 intermediate-completion evaluations agree
with the classifier. Of 7,500 consistent envelope-refinement cases, 0 reverse a
previously decisive answer. These are synthetic finite denominators, not deployment
success rates or proof of an all-size theorem.

## Scientific custody

Design committed before calibration: 81beff7df934d4502d01d252353d7a213e9f0a61.
Written proofs: THEORY.md; source ownership/read limits: SOURCES.md; executable
semantics: temporal.py; exhaustive comparisons: calibrate.py; hostiles: test_temporal.py.
RESULT.json is bound by RECEIPT.json, which does not hash itself. An independently
fixed Git commit anchors the package, not a self-issued digest.

Actual local execution: CPython 3.13.5 on isolated Linux, not Mac/LUNARC. Local
repository git clone failed DNS, so this package's local materialization is NOT a
full clean clone. GitHub CI independently checks a real checkout. All-size arguments
are written proofs, not proof-assistant verified. Analytic roles within this authoring
session do not count as independent reviewers.

## Remaining obligations

Overall foundation remains OPEN_RESEARCH; independent review remains
NOT_OBTAINED__DISCLOSED_LIMITATION. Production model-closure, abstraction fidelity,
authentication, atomicity, actual action execution and resource performance remain
CANNOT_CHECK in this package. A caller-supplied graph is not evidence that the graph
covers reality. THEORY.md specifies the required OCM absorption contract and exact
research targets for envelope acquisition, incremental maintenance and active refresh.
The original scientific terminals, OCM milestone gates and other sessions' files are
not changed.
