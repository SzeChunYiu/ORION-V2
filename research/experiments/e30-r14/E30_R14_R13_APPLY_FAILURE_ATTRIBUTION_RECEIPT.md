# E30-R14 — attribution receipt: why E30-R13's patches did not apply, and the interface that follows

```text
E30_R14_STATUS         = ATTRIBUTION_COMPLETE__INTERFACE_REGISTERED__CALIBRATION_PENDING
ATTRIBUTED_STAGE       = ARM_WORKSPACE_INTERFACE  (two sub-stages: presentation, emission)
LEVER                  = anchored-edit interface (search/replace located by content) + mentioned_files_full presentation
RESCORED_R13           = FALSE   (read-only over the 480 archived envelopes; no endpoint, no test, no gold)
CHANGES_E30_R13        = NONE
GRANTS_SCIENTIFIC_TRUTH = false  GRANTS_FIELD_STATUS = false  GRANTS_MANUSCRIPT_CHANGE = false
```

E30-R13 terminated `INTERFACE_STILL_BROKEN`: 480/480 envelopes completed under a registered
channel contract, and GR1's apply-rate diagnostic failed on every arm (apply-failure
0.69–0.78 against the 0.40 ceiling), so the separation question was never reached. The
doctrine says a negative is intermediate: attribute to one stage, apply the lever, re-test.
This receipt records the attribution and the lever; the re-test is E30-R14, under a new
campaign identity, and it has not run.

## 1. What was measured, and how it was kept honest

Four read-only scripts (`attribution/`) walked the 480 archived R13 envelopes on LUNARC
(campaign `…427bfc90`, interpreter 3.11.5) and the frozen gold-blind solver workspaces the
requests name. They ran no test, scored no endpoint, opened no gold tree and wrote nothing
into the campaign. Output: `results/E30_R14_R13_APPLY_FAILURE_ATTRIBUTION_V1.json`.

Every zero carries a control that fired in the same run: a fabricated context block returned
0 anchors while a real block from the same file returned exactly 1 (the `CONTROL` line of the
anchored-recovery diagnostic); the presentation rule was replicated from
`scripts/orion_claude_arms._context` and its outputs matched the archived receipts'
`source_snapshot_truncation` fields; the recovered patches were confirmed by `git apply
--check` on the frozen workspace, not by the diagnostic's own opinion (143 of 145 confirmed;
the 2 that failed are reported as failures).

## 2. The decomposition of the 346 non-applying envelopes

| emission status (R13's own receipts) | envelopes |
|---|---|
| `APPLY_CLEAN_BY_CONSTRUCTION` | 134 |
| `CANONICAL_BUT_APPLY_CHECK_FAILED` | 205 |
| `NOT_CANONICALIZABLE_EMITTED_UNCHANGED` | 141 |

**Sub-stage A — emission (the model cannot serialise a unified diff the interface accepts).**
141 patches were refused by the frozen canonicalizer for forms a diff can carry: duplicated
`diff --git` headers with `index`/`new file mode` metadata (95), numberless `@@ def f(): @@`
anchors (45), `--- /dev/null` new-file headers (35), unprefixed body lines (8), an ellipsis
in context (4). None of these is an edit error; each is a serialisation the parser does not
read. A lenient reader recovers hunks from all but 1 of the 346.

**Sub-stage B — location (the model quotes context and line numbers it cannot know).**
Locating each hunk by its own context or removed lines, ignoring the line arithmetic:

| anchored recovery class | of 346 |
|---|---|
| `RECOVERABLE_ANCHORED` (context located uniquely; 108/110 confirmed by `git apply --check`) | 110 |
| `RECOVERABLE_REMOVED_ONLY` (only the removed lines locate; 35/35 confirmed) | 35 |
| `UNRECOVERABLE: CONTEXT_NOT_IN_FILE` | 94 |
| `UNRECOVERABLE: CONTEXT_AND_REMOVED_NOT_IN_FILE` | 103 |
| `UNRECOVERABLE: REMOVED_LINES_AMBIGUOUS` | 3 |
| `NO_HUNKS_PARSED` | 1 |

So 145 of 346 failures are **interface** failures in the narrow sense: the edit is there and
the interface could not read it. 201 are not recoverable by any reader of the archived text,
because the context the model wrote does not occur in the file.

**Sub-stage C — presentation (why the context does not occur in the file).** The workspace
snapshot shows every file cut at 30 000 characters inside a 120 000-character budget. Of the
205 canonical-but-non-applying patches, **152 declare a hunk start beyond the shown prefix of
a truncated file, or in a file not shown at all** — the model "quoted" context it was never
shown. Presentation visibility over all 480: 122 all-targets-fully-shown, 129 targets in the
shown region of a truncated file, 188 some-target-unseen, 41 with no numbered hunks.

## 3. The attribution, and the ceiling it implies

The stage is the **arm↔workspace interface**, and it fails in two places that a single lever
does not cover: an emission-only repair (accept every syntax the models emit, locate by
content) recovers 145 of 346, which puts the apply-failure floor at (346 − 145)/480 ≈ **0.42**
— still above the 0.40 GR1 ceiling. The presentation sub-stage must be repaired as well.
That is why E30-R14's interface changes both halves, and why the split between them is
**measured pre-freeze by a 2×2 calibration** (edit interface × presentation policy, one call
per cell on `SIMPLE_DIRECT` over the 40 frozen tasks) rather than assumed.

## 4. The lever, as registered

`src/orion_v2/anchored_edit_interface.py` asks the model for the edit only — a verbatim
`search` block and a `replace` block per contiguous change — locates the block in the
gold-blind workspace (exact, then rstrip, then collapsed whitespace; never across meaning),
and derives the unified diff with `git diff --no-index` from the file itself, so context and
counts come from the file rather than from the model. It never guesses a path, never chooses
between two locations, never partially applies, never opens a gold tree, and records every
unlocated edit with its reason. The evaluator's `git apply` invocation is untouched and the
`orion.v2.patch-emission.v1` receipt is preserved with additive fields.

`scripts/orion_claude_arms.py` makes the interface a **registered condition**: `EDIT_INTERFACES`
(fail-closed on unknown ids), a byte fingerprint over the prompt template plus the emission
module (`edit_interface_sha256`), a `mentioned_files_full` presentation policy that shows
every baseline-named file whole and outside the budget, and an `interface_receipt` on every
envelope (interface id, fingerprint, files shown, mentioned files truncated). The default
stays `unified_diff` / `per_file_cap`, so no existing lane changes. 28 unit tests
(`test_anchored_edit_interface.py`, `test_e30_r14_interface_contract.py`); R12/R13 lane
tests and the arms tests pass unchanged.

The registered R14 gate that reads the receipt is **GR0f INTERFACE_HOMOGENEITY**
(`e30_r14_analysis.py`): one interface id and one fingerprint across 480 envelopes, equal to
the registered pair, and zero truncated mentioned files under the full policy; a receipt
absent, two fingerprints, or a truncated mentioned file each fail it, ahead of any endpoint.

## 5. What this does not claim

Nothing here is a repair mechanism and nothing here rescores E30-R13: its terminal, gates,
endpoints and apply rates stand exactly as receipted. Locating an edit by content is the edit
contract the leading agent harnesses converged on; it is not novel, and the receipt does not
say otherwise. Whether the interface brings apply-failure under the 0.40 ceiling is what the
calibration measures and what R14's GR1 will decide; this receipt licenses the freeze of that
design, not any statement about repair.

## 6. Calibration status

The 2×2 calibration (`e30_r14_interface_calibration.py`, `sbatch/e30_r14_calibration.sbatch`)
was staged on LUNARC from branch sha `3e516a1` under E30-R13's registered channel condition
(served `glm-5.3`, `thinking_disabled`, 14 000 cap). Its first three calls, all under the
historical `unified_diff|per_file_cap` cell, returned HTTP 429 through ten retries each
(≈373 s per call) and were recorded as `EXECUTION_FAILED_MODEL_RESPONSE` with the failure text
attached; the channel then answered a 20-token probe with the same status. **No cell has a
measurement.** The attempt is archived as attempt 1 and the job was cancelled rather than left
to write 157 more failures; the calibration will be re-run in full under a new attempt id when
a channel answers, and the design freezes only after it does.

skills-applied: none (receipt, no manuscript content)
