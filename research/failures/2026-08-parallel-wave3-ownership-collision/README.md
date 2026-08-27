# Parallel Wave-03 Ownership Collision

## Failure class

`PARALLEL_RESEARCH_LANES_WITH_OVERLAPPING_FRAMEWORK_OWNERSHIP`

## Observation

Two branches independently developed Wave-03 generalization theory:

- PR #26: decision-envelope compiler and generalized families;
- PR #29: conservative adaptation and meta-formalization calculus.

Both were internally green and scientifically useful. They nevertheless overlapped in terminology, documents, schemas, adaptation statuses and publication ownership.

## Risk

If later work selected one branch by familiarity, it could silently lose the other branch's tests and findings. If both were merged without reconciliation, ORION-V2 would carry duplicate or inconsistent generalization interfaces.

## Resolution

Wave 06 assigns distinct layers:

- PR #26 owns envelope derivation and domain-neutral families;
- PR #29 owns interpretation/certificate laws;
- Wave 04 owns independent native recovery;
- Wave 05 owns stochastic/approximate transport;
- protected external evaluation owns scientific success/adoption.

The distinct PR-29 code, schema and tests are imported into the Wave-06 branch. A unified non-authorizing layer receipt prevents later success from compensating for an earlier failure.

## What remains open

- schema/version migration;
- direct object-identity bindings across layers;
- resolution of duplicate status names;
- review of overlapping documentation;
- final PR merge/closure sequence;
- strongest parent-product comparison.

## Authority

Reconciliation prevents internal loss and duplication. It does not establish scientific correctness, novelty or V2 admission.