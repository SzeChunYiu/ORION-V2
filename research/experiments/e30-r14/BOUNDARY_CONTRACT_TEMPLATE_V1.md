# Boundary contract template V1 — the arm↔workspace edit interface, written as a contract

**Component fed:** the knowledge-space object's codec boundary (#284 M5), shaped like the
one typed interface in this programme that worked (`patch_emission.py` /
`APPLY_CLEAN_BY_CONSTRUCTION`). **Checker:** E30-R14's GR1 apply-rate gate (≤ 0.40
apply-failure) with GR0f interface homogeneity ahead of it. **Status:** contract registered
in code (`src/orion_v2/anchored_edit_interface.py`, `scripts/orion_claude_arms.py`,
`research/experiments/e30-r14/e30_r14_analysis.py`); checker staged, unmeasured
(the 2×2 calibration has no answered cell yet). Nothing here is a repair mechanism and
nothing here claims novelty: locate-by-content editing is the contract the leading agent
harnesses converged on.

## 0. Why a boundary needs a contract, measured

E30-R13 pinned the served model (GR0c), the request body (GR0d) and the channel's behaviour
(GR0e) and still could not test repair: 346 of 480 emitted unified diffs did not apply,
apply-failure 0.69–0.78 on every arm including the parent federation. The read-only
decomposition (`results/E30_R14_R13_APPLY_FAILURE_ATTRIBUTION_V1.json`) found the failure
at the boundary and nowhere else: 152 of 205 canonical non-applying patches edit a region
the 30 000-character per-file snapshot never showed, and 141 patches were refused for
syntax a diff can carry but the reader did not accept. The failure class is
`INTERFACE_ASKS_FOR_WHAT_IT_WITHHELD` (ledger, 2026-09-04): the boundary asked the model for
information — verbatim context and line arithmetic — that only the untruncated view holds,
then scored the boundary's own failure as the model's.

The general lesson for every KSO boundary: **the crossing type must be closed under what
the sender was shown.** A codec that asks for coordinates into a space it did not present
will fail at a rate that is flat across senders of any capability, and a paired contrast
across senders will never see it.

## 1. What crosses, in what type

### 1.1 Inbound (workspace → arm): the presentation

| field | type | invariant |
|---|---|---|
| `task` | the frozen public task object | gold-blind; no oracle key at any depth (canary-asserted) |
| `python_files` | list of repository-relative paths | complete listing of the workspace |
| `source_snapshots[]` | `{path, content}` | **every file the baseline observation names is shown whole** (`mentioned_files_full`); other files cut at `max_file_chars` inside `max_total_chars` |
| `source_snapshot_truncation` | `{presentation_policy, files_shown, mentioned_files_shown, mentioned_files_truncated, files_truncated, context_chars, per_file[]}` | the receipt of what was withheld; `mentioned_files_truncated` must be 0 under the full policy |

The sender may only be asked to quote what is inside `source_snapshots`. That is the
closure condition, and it is recorded per envelope rather than assumed.

### 1.2 Outbound (arm → workspace): the edit

| field | type | invariant |
|---|---|---|
| `edits[]` | `{path, search, replace}` or `{path, create: true, replace}` | `path` is repository-relative, no `..`, no absolute; `search` is a contiguous block of complete lines copied verbatim from the shown snapshot and occurs **exactly once** in the file; `replace` is the full replacement block (empty deletes) |
| `diagnosis`, `assumptions`, `uncertainty`, `discriminator_or_tests`, `falsifier` | strings / lists | unchanged from the R13 response contract; not part of the crossing type the evaluator reads |

Fallback (recorded, never silent): a unified diff in `patch` is read leniently — duplicated
`diff --git` headers, `index`/mode lines, numberless `@@` anchors, `/dev/null` new-file
headers, dropped leading spaces — and each hunk becomes a `(search, replace)` pair located by
content like any native edit; `edit_origins` names which path was taken.

### 1.3 Materialised (boundary → evaluator): the derived diff

| field | type | invariant |
|---|---|---|
| `proposed_patch_or_artifact.content` | a unified diff rooted at repository paths | **derived by `git diff --no-index` from the real file with the located edits applied**; context lines and hunk counts come from the file, never from the sender; header-exact by construction |
| `patch_emission_receipt` | `orion.v2.patch-emission.v1` + additive fields | `emission_status ∈ {APPLY_CLEAN_BY_CONSTRUCTION, EDITS_NOT_LOCATED, DERIVED_BUT_APPLY_CHECK_FAILED, DERIVED_APPLY_CHECK_NOT_VERIFIED}`; `emitted_apply_check` from a non-mutating `git apply --check` on the gold-blind workspace; `unlocated_edits[]` with reasons; `match_modes`; `normalizations[]` (mode, path, start, indent shift) |
| `interface_receipt` | `{edit_interface, edit_interface_sha256, presentation}` | the interface id, its byte fingerprint over the prompt template plus the emission module, and the presentation summary above |

The evaluator's `git apply` invocation is untouched: what it consumes is still a unified
diff, and every archived response remains readable.

## 2. What is rejected, and how the rejection is typed

| condition | status | consequence |
|---|---|---|
| `search` not found (exact → rstrip → collapsed-whitespace, in that order; no semantic matching) | `SEARCH_NOT_FOUND` with `search_lines_present_individually` | edit unlocated; **no patch emitted for the response** |
| `search` occurs more than once | `SEARCH_AMBIGUOUS` with `occurrences` | unlocated; the boundary never chooses between locations |
| `path` not in the workspace | `PATH_NOT_IN_WORKSPACE` | unlocated; the boundary never invents a path |
| `create: true` on an existing file | `CREATE_TARGET_EXISTS` | unlocated |
| two edits overlap in one file | `EDITS_OVERLAP` with spans | unlocated; a sender error is reported, not resolved |
| all edits are no-ops | `EDITS_ARE_A_NO_OP` | no patch emitted |
| unsafe or empty path, malformed edit object, no edits and no diff | `AnchoredEditError` → envelope `EXECUTION_FAILED_MODEL_RESPONSE` | the response is a failure envelope, never a scored proposal |
| derived diff fails `git apply --check` | `DERIVED_BUT_APPLY_CHECK_FAILED` | should not occur (the diff is derived from the file); kept so a defect here is reported rather than hidden |
| git unavailable | `DERIVED_APPLY_CHECK_NOT_VERIFIED` | distinct from PASS; a campaign gate treats it as could-not-check |

**Partial application never happens**: one unlocated edit voids the whole response's patch.
**The replacement text is never altered** except by the exact indentation offset at which a
collapsed-whitespace match was found, and that offset is in the receipt.

## 3. Authority the boundary does and does not have

```text
gold_or_fixed_patch_access      = FORBIDDEN_NOT_USED
may_change_semantic_edit        = false
may_guess_paths                 = false
may_relocate_hunks              = false      (a hunk is located by its own content or not at all)
resolves_ambiguous_search_blocks = false
partial_application             = false
may_rescore_a_frozen_campaign   = false
mutates_the_workspace           = false      (git diff --no-index against a temporary copy)
```

## 4. Registration and homogeneity

The interface is a **registered condition**, like the served model and the request body:
`EDIT_INTERFACES` fails closed on an unknown id; `edit_interface_sha256` fingerprints the id,
the presentation policy, the final-prompt template and the emission module's bytes; the
dispatch chain refuses to start unless the dispatched interface equals the design's
`interface_binding` (setup), the arms' FINAL count refuses fewer than 480 interface
receipts or more than one fingerprint (agents), and **GR0f INTERFACE_HOMOGENEITY** is
evaluated ahead of every endpoint (rollup): one id, one fingerprint, zero truncated
mentioned files, else `INTERFACE_CONTRACT_VIOLATION` and no endpoint is read. The gate is
proven to fail on each mode and to report `COULD_NOT_CHECK` — never `PASS` — on zero
receipts (`tests/unit/test_e30_r14_analysis_gr0f.py`).

## 5. The checker, and what would falsify the contract

The contract's checker is E30-R14's **GR1**: apply-failure ≤ 0.40 across the four arms over
480 envelopes, evaluated only after GR0c/d/e/f pass. Before R14 freezes, the 2×2
calibration (interface × presentation, one call per task on `SIMPLE_DIRECT`) must show at
least one cell at or under the ceiling; the selection rule — lowest apply-failure, ties to
the historical cell, registration only under 0.40 — is declared in
`e30_r14_build_design.py` before any cell is measured. If no cell clears the ceiling the
contract is falsified as written (`INTERFACE_CALIBRATION_ABOVE_CEILING`) and returns to
attribution; the attribution's own floor for an emission-only lever is ≈0.42, which is why
both halves are in the contract.

## 6. Template for the KSO codec boundary (M5), by substitution

| this contract | KSO codec boundary |
|---|---|
| `source_snapshots` shown whole for named files | the subgraph rendered to the codec is the **whole** extracted subgraph, with a receipt of anything elided |
| `search` block located by verbatim content, exactly once | an atom reference located by its content hash, exactly once; never by position in the rendering |
| derived diff from the real file | the graph mutation derived by the substrate from located atoms; the codec never writes graph coordinates |
| `EDITS_NOT_LOCATED` voids the response | an unlocatable atom reference voids the codec's proposal; no partial mutation |
| `interface_receipt` + GR0f | codec id + fingerprint on every exchange; **translator invariance** (#284 §1) is the homogeneity gate across two codecs |
| GR1 apply-rate | the fraction of codec proposals that materialise as a warranted mutation |

skills-applied: none (contract, no manuscript content)
