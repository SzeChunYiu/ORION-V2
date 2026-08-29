# E20 Patch-Serialization Confound Audit V1

**Status:** post-pilot diagnostic; no authority to alter the frozen E20 primary result.  
**Parents:** issues #45, #46, #47.  
**Purpose:** separate scientific/problem-solving failure from executable-artifact serialization failure before E30 confirmatory interpretation.

## Observed E20 fact

The valid E20 pilot produced:

| Arm | Native successes / 3 | Patch-apply failures |
| --- | ---: | ---: |
| SIMPLE_DIRECT | 2 / 3 | 1 |
| SAME_MODEL_REFLECTION | 2 / 3 | 1 |
| F0_PARENT_FEDERATION | 1 / 3 | 2 |
| F2_ORION_METABOLIC_FULL | 1 / 3 | 2 |

The pilot remains underpowered and does not establish F2 superiority or inferiority.

## F2 failure localization

### pandas-1

The F2 diagnosis selected the same substantive one-line categorical exclusion used by the successful SIMPLE arm. The F2 artifact declared:

`diff --git a/pandas/core/dtypes/common.py b/pandas/core/dtypes/common.py`

but emitted file headers without the required `a/` and `b/` prefixes:

`--- pandas/core/dtypes/common.py`

`+++ pandas/core/dtypes/common.py`

Native evaluation therefore stopped at patch application with `core/dtypes/common.py: No such file or directory`. The scientific edit was not tested.

### pandas-3

The F2 artifact proposed explicit TypeError guards in `pandas/core/series.py`. Native evaluation stopped at patch parsing with `patch fragment without header`. Inspection shows both hunk headers declare `7 -> 8` lines while their unchanged hunk bodies imply `8 -> 9`. Again, the proposed semantic edit did not reach compilation or tests.

## Control observation

SIMPLE also had one patch-application failure (`corrupt patch`) on pandas-2. Therefore this is not a F2-only excuse. It is an end-to-end interface variable shared by all model arms.

## Scientific implication

Raw executable success remains the primary end-to-end outcome: a scientific agent that cannot return an executable artifact has failed the task.

However, using only raw success confounds at least two quantities:

1. scientific diagnosis/edit quality;
2. serialization of that edit into syntactically executable unified-diff form.

For a top-tier mechanism claim, these should be reported separately rather than silently treated as one latent capability.

## Prospectively admissible E30 sensitivity control

Before E30 model outcomes, all registered arms may be passed through the same arm-blind **syntax-only** interface audit. The canonicalizer is permitted to change only representation facts recoverable from the diff itself:

- normalize `--- path` / `+++ path` to `--- a/path` / `+++ b/path` only when the preceding `diff --git` header binds that exact path;
- normalize an empty hunk context marker to a single-space blank context line;
- recompute hunk old/new line counts from the unchanged hunk body.

It is forbidden to:

- infer or change a file path;
- add/remove/reorder semantic edit lines;
- change hunk start positions;
- inspect a gold/fixed patch;
- use arm identity when deciding a normalization;
- replace the raw end-to-end primary result.

Implementation:

- `src/orion_v2/unified_diff_interface.py`
- `scripts/audit_orion_diff_interface.py`
- `tests/unit/test_unified_diff_interface_wave6.py`

## Required E30 reporting

For every arm report both:

- **RAW_END_TO_END_SUCCESS** — original frozen response evaluated exactly as emitted;
- **SYNTAX_NORMALIZED_SENSITIVITY_SUCCESS** — only if the above prospective control was frozen before E30 outcomes and applied identically to all arms.

Also report:

- diff valid unchanged;
- valid after syntax-only normalization;
- invalid/not canonicalizable;
- patch apply success;
- compile success;
- registered-test success;
- full-regression status where bound.

If F2 gains only after syntax normalization, the valid conclusion is that reasoning/edit content may be stronger than its raw artifact interface; it is **not** evidence that the original F2 end-to-end system was superior.

If SIMPLE/F0 gain similarly, retain those gains.

## Mechanism-revision boundary

This audit does not authorize F2 theory revision. It creates a cleaner failure decomposition for issue #47.

A future mechanism change is justified only after confirmatory evidence distinguishes:

- representation/serialization drag;
- diagnosis/reasoning failure;
- parent sufficiency;
- component harm;
- resource drag;
- genuine higher-order gain.

## Authority

`E20_PRIMARY_RESULT_CHANGED = FALSE`  
`E20_F2_SUPERIORITY = NOT_ESTABLISHED`  
`E30_SYNTAX_SENSITIVITY_CONTROL = AVAILABLE_FOR_PROSPECTIVE_FREEZE`  
`THEORY_REVISION_AUTHORITY = NONE`
