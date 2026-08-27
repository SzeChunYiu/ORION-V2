# ORION V1 → ORION-V2 Handoff Register V1

**Status:** `V1_FREEZE_HANDOFF_BOUND_AND_NON_RETROACTIVE`.

**Machine receipt:** `provenance/ORION_V1_HANDOFF_RECEIPT_V1.json`.

**Checker:** `python scripts/check_v1_handoff.py`.

## Bound source

| Coordinate | Exact identity |
|---|---|
| Source repository | `SzeChunYiu/ORION` |
| V1 freeze commit | `8f250fc3e55d6d6a28fb1fb33d9932ef1a8760b5` |
| Frozen subject/base main | `ef51b7b9263a72c725dc9d2045627b934b772a92` |
| Frozen base tree | `5d5ff0985551b0a94453ea6eaa9925bda3e10fa2` |
| Observed ORION main | `405247aad9b8fdda285b13590f6a5d4e96247d7e` |
| Descendant check | observed main is 16 commits ahead and 0 behind the freeze commit |
| V1 terminal | `ORION_V1_ARCHITECTURE_AND_LOCAL_FORMALISM_FROZEN` |
| Paper-authority delta | `NONE` |

The freeze identity is the exact freeze commit and control-plane content, not the moving ORION `main` branch.

## Control-plane bindings

The handoff receipt binds exact Git object identities for:

- the V1 freeze contract and manifest;
- component graph and component binding;
- issue disposition ledger;
- theorem census;
- P1–P15 result-bound claim ledger;
- root failure/negative ledger;
- research-harness tree.

The V1 theorem census reports 101 locally formalized theorems with zero local proof holes, while external proof review remains an authority-level open item. The freeze records zero local implementation gaps and zero unclassified open issues, with three external/heavy blockers retained as explicit `CANNOT_CHECK` rather than converted to success.

## Non-retroactivity

ORION-V2 may cite, embed, compare with or replace a V1 capability prospectively. It may not:

- rewrite a V1 claim, theorem, result or failure;
- convert a V1 negative, harmful result or `CANNOT_CHECK` into a pass;
- alter P1–P15 paper ownership or numbering retrospectively;
- claim that post-freeze ORION commits changed the identity frozen here.

## Permission boundary after this handoff

The handoff unlocks:

- ORION-V2 reference implementation;
- unit, known-answer and hostile tests;
- deterministic research tooling;
- local prospective pilots after their own protocols are frozen;
- V1 capability-parity implementation.

It does **not** unlock:

- protected external evaluator/holdout access without a separate protocol;
- scientific truth, superiority or novelty promotion;
- final V2 architecture or paper identity;
- self-authorized framework or constitution adoption.

## Reopen rule

A content-identity mismatch, missing negative history, revocation of the underlying freeze, or a checker that allows authority laundering reopens this handoff immediately.
