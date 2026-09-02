# E80 Arm-Side Patch Emission V1

**Status:** forward-looking infrastructure fix. **Changes future runs only.**
**Parents:** E20 serialization confound audit; E70-GC1 R1; E70-GC2 calibration terminal.
**Authority:** `FROZEN_CAMPAIGN_RESCORING = FORBIDDEN`, `SCIENTIFIC_CLAIM_CHANGE = NONE`.

## The defect

Two independent frozen studies localized the entire raw-endpoint variance between
solver arms to unified-diff *serialization* rather than reasoning.

| Study | Raw (header-exact) endpoint | Syntax-normalized endpoint |
| --- | --- | --- |
| E70-GC1 R1 (24 tasks × 4 arms) | F2 3/24, SIMPLE 5/24, REFLECTION 5/24, F0 8/24 | **24/24 every arm**, accuracy 1.000 |
| E70-GC2 (16 tasks × 3 rungs, SIMPLE only) | **0/16 at every rung** (48/48 diffs needed canonicalization) | 46/46 applied cells at accuracy 1.000 |

GC1 established `success_iff_header_unchanged = true` for all four arms: raw success
held exactly when the canonicalizer left the hunk header alone. The two mechanisms
are an over-counted `N` in `@@ -a,N +b,M @@` (git rejects the patch as corrupt) and an
under-counted `N` (git silently truncates the hunk, leaving a prefix of the intended
file that runs but mis-scores). GC2 sharpened it: multi-file patches carry more hunks,
so the raw lane degraded from 5/24 to 0/16 while the semantic lane stayed at ceiling.

Solver experiments were therefore measuring diff syntax, not reasoning.

## The fix

Arms now canonicalize at **emission** instead of relying on downstream normalization.
`src/orion_v2/patch_emission.py` sits between the model response and the response
envelope in both `scripts/orion_claude_arms.py` and `scripts/orion_codex_arms.py`:

1. **extract** the diff from raw model output (Markdown fences, surrounding prose);
2. **synthesize** the `diff --git` header implied by an adjacent `---`/`+++` pair,
   copying the path the model already wrote — never guessing one;
3. **canonicalize** via the frozen `orion_v2.unified_diff_interface` (`a/`–`b/` header
   prefixes, blank context markers, hunk counts recomputed from the unchanged body);
4. **verify** with a non-mutating `git apply --check` against the gold-blind solver
   workspace the arm already reads.

### Why not the structured-edit contract

Switching arms from a unified diff to a structured `(file, anchor, replacement)` edit
was the alternative considered. It was rejected: it changes the solver-facing prompt
and therefore what the experiment measures, and it breaks the `response_format`
declared by three prospective protocol manifests. Emission-side canonicalization
fixes the measured confound without touching the task the arm is asked to perform.

### Why hunks are never relocated

`git apply` already searches the whole file for a hunk's context regardless of the
declared start line — the sole exception is a hunk declaring `old_start = 1`, which git
forces to match at the beginning of the file. A wrong start line therefore almost never
causes a failure, and a residual apply failure means the emitted *context lines* are
wrong. Repairing that would be semantic inference, which is forbidden. Emission
detects it, records `emission_status = CANONICAL_BUT_APPLY_CHECK_FAILED` with git's
own error, and changes nothing. This is the class the GC2 residuals fell into
(`gc2-003` at `normalize.py:5`, `gc2-004` at `solver.py:3`).

## Contract

**Preserved:** `schema_version` stays `orion.v2.agent-response.v1`. The three
prospective protocol manifests declare `"response_format": "orion.v2.agent-response.v1.json"`,
and `proposed_patch_or_artifact.content` is contractually a string containing a unified
diff — which a canonical diff satisfies. `patch_emission_receipt` is **additive and
optional**; archived v1 responses without it validate unchanged.

**Gold-blind:** emission reads only the solver workspace already visible to the arm.
It never opens a gold, fixed or reference patch, never invents a path, never adds,
removes, reorders or rewrites an edit line, and never mutates the workspace
(`git apply --check` only). The receipt records this as non-authority.

**Validator guard tested in both directions.** `scripts/validate_orion_agent_responses.py`
accepts a real emitting-arm response with no errors (the no-alarm case) and rejects a
receipt that claims semantic-edit, path-guessing, hunk-relocation or frozen-campaign
rescoring authority, that fails to disclaim gold access, that carries an unknown
receipt schema version, or that drops the fidelity endpoint.

**Frozen control untouched:** `src/orion_v2/unified_diff_interface.py` and the three
other files pinned by sha256 in `E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1.json` are
byte-unchanged. Emission is a new layer that imports the frozen canonicalizer. CI
asserts all four pins on every run, and `test_frozen_e30_control_code_is_unmodified`
asserts them in the unit suite.

**Interface-fidelity endpoint preserved.** Because arms now emit canonical diffs, the
raw header-exact lane would otherwise become trivially 100% and unmeasurable. The
receipt keeps it reconstructible from the response alone:

| Field | Meaning |
| --- | --- |
| `extracted_was_header_exact` | the extracted artifact needed no canonicalization |
| `extracted_was_apply_clean` | `git apply --check` accepted it (`null` if unverifiable) |
| `extracted_apply_check` | the check outcome, including why it could not be run |
| `raw_sha256`, `extracted_sha256`, `emitted_sha256` | identity of all three forms |
| `normalizations` | the frozen canonicalizer's own reason strings |
| `emission_status` | `APPLY_CLEAN_BY_CONSTRUCTION`, `CANONICAL_BUT_APPLY_CHECK_FAILED`, `CANONICAL_APPLY_CHECK_NOT_VERIFIED`, or `NOT_CANONICALIZABLE_EMITTED_UNCHANGED` |

The fidelity fields are named for their referent. They describe the **extracted**
artifact — post-extraction and post-header-synthesis, pre-canonicalization — not
`raw_sha256`, which is the model text before extraction. Extracted is the form
directly comparable to the archived GC1/GC2 raw lane, whose responses were themselves
stored after the codex arm's header synthesis, so the comparison is like-for-like.

**Never degrades an artifact.** A patch the frozen canonicalizer rejects is emitted
unchanged with `NOT_CANONICALIZABLE_EMITTED_UNCHANGED`; emission is never worse than
the status quo, and never silently drops a proposal.

## Frozen studies that remain unaffected

This changes future runs only. No completed study is re-scored, re-run or re-read, and
no receipt, verdict or paper terminal moves. Specifically unaffected:

Enumerated from `research/experiments/results/issue45/`:

| Frozen study | Status after this change |
| --- | --- |
| `e20-r4-native` + `E20_PATCH_SERIALIZATION_CONFOUND_AUDIT_V1` | unchanged; `E20_PRIMARY_RESULT_CHANGED = FALSE` stands |
| `e30-r11` + `E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1` | unchanged; all four sha256-pinned files byte-identical |
| `e40`, `e40-perm-r1` (incl. M5P Stage-2b/2c dispatch receipts) | unchanged |
| `e50` | unchanged |
| `e60-r1-component-ablation` | unchanged |
| `e70-gc1-r1` | unchanged; F2 3/24 vs F0 8/24 and the 24/24 normalized lane stand as recorded |
| `research/experiments/e70-gc2` | unchanged; `SUITE_STILL_SATURATED`, no protected split, no arm comparison |
| `fmfg-r1`, `pc-r6`, `pc-r7` | unchanged |
| ME-X1 protected-run outcome receipt, ME-X2 study-design freeze | unchanged |

The GC1 revival attribution (H-EXT-3, interface-information residual) is what this
implements; it is not revised by it. No arm is credited, repaired or re-run on this
basis, and any future campaign using these arms needs its own prospective freeze.
