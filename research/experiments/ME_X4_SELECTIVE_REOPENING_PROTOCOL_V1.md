# ME-X4 — Selective Reopening under Dynamic Evidence V1

**State date:** 2026-09-01  
**Status:** prospective/unexecuted

## 1. Question

When evidence ancestry, calibration, transport or evaluator validity changes, can the system reopen exactly the commitments whose registered sufficient support has failed while preserving independently supported commitments—beyond mature truth-maintenance, belief-revision, provenance and assurance parents?

## 2. Known-answer support-graph generator

Freeze a generator producing versioned scientific support graphs with:

- claims and alternative hypotheses;
- multiple sufficient support families;
- necessary and sufficient prerequisite relations;
- shared-source/data/model/instrument ancestry;
- independent redundant support;
- retractions/corrections;
- calibration or measurement invalidation;
- context/transport invalidation;
- evaluator replacement or failure-class change;
- scope/criterion change;
- unresolved/censored edges;
- negative evidence and contradiction edges.

The generator exposes the expected reopened, preserved and unresolved sets to protected custody—not to the acting system.

## 3. Event strata

- `SOURCE_RETRACTED`
- `DEPENDENCE_DISCOVERED`
- `CALIBRATION_INVALIDATED`
- `TRANSPORT_RELATION_INVALIDATED`
- `EVALUATOR_BLIND_OR_REPLACED`
- `PROBLEM_SCOPE_CHANGED`
- `NEW_INDEPENDENT_SUPPORT`
- `CORRECTION_RESTORES_SUPPORT`
- `PARTIAL_SUPPORT_FAILURE`
- `ALL_SUFFICIENT_SUPPORT_FAILED`
- `CANNOT_CHECK_EDGE`
- `NO_REOPENING_NEEDED`

## 4. Baselines

- provenance-only invalidation;
- classical TMS;
- ATMS/assumption environments;
- belief-revision baseline;
- Bayesian/support graph baseline;
- assurance-case update;
- `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`;
- `M_ME_SELECTIVE_REOPENING`.

B5 receives all registered support/dependence/transport/evaluator information available to M.

## 5. Primary outcomes

- exact reopened set;
- exact preserved-valid set;
- exact unresolved set;
- over-reopening;
- under-reopening;
- invalid preservation;
- recovery after corrective evidence;
- reopening latency/cost;
- dependence/transport/evaluator-specific error strata.

## 6. Mechanistic ablations

- minus dependence ancestry;
- minus typed transport status;
- minus evaluator contract;
- minus sufficient-support-family representation;
- global-reset control;
- provenance-only control.

## 7. Naturalistic validation

Require at least one independently authored case each from two of:

- systematic evidence synthesis;
- scientific software/formal dependency systems;
- experimental/measurement revision histories;
- model/versioned benchmark evaluation.

Native reviewers define what should reopen before arm outcomes.

## 8. Kill conditions

Selective reopening remains parent-owned if B5 exactly reproduces M's reopening/preservation decisions at equal or lower cost. Contract also if M over-reopens enough to erase independent valid support, depends on hidden oracle relations, or its support-family schema cannot preserve native semantics.

## Terminal

```text
ME_X4_STATUS = PROSPECTIVE_UNEXECUTED
PRIMARY_COMPARATOR = TMS_ATMS_BELIEF_REVISION_PROVENANCE_ASSURANCE_FEDERATION
EXACT_REOPEN_PRESERVE_UNRESOLVED_SETS = PRIMARY_OUTCOMES
PARENT_SUFFICIENCY = VALID_TERMINAL
FIELD_STATUS_AUTHORITY = NONE
```
