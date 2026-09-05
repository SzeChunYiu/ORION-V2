# E70-GC2 — `INSTRUMENT_SUSPECT__RERUN_PENDING` (revival backlog #308, row R5)

**State of the GC2 calibration terminal:** `SUITE_STILL_SATURATED` stands as the frozen calibration
outcome of `E70_GC2_CALIBRATION_TERMINAL_RECEIPT.md`; nothing in that receipt is rescored
(`FROZEN_CAMPAIGN_RESCORING = FORBIDDEN`). What changes is the **reason** the raw header-exact lane
read 0/16 at every rung, and therefore what a re-run must fix before its secondary endpoint can be
quoted. Attributed stage (one): **instrument — patch serialization**. Date: 2026-09-05.

## 1. The instrument, and the two defects in it

| # | defect | where | effect on GC2 | repaired by |
|---|---|---|---|---|
| D1 | the raw endpoint measured a *model-written* hunk count | `@@ -a,N +b,M @@` emitted by the arm | 48/48 diffs needed canonicalization; 0/16 header-exact at every rung | E80 arm-side emission (`src/orion_v2/patch_emission.py`, merged): arms now emit canonical diffs and carry the pre-canonicalization fact in `patch_emission_receipt.extracted_was_header_exact` |
| D2 | the evaluator's header-exact endpoint is read off the **archived content** | `run_orion_generated_composition_gc2_suite.py::evaluate_one` | post-E80 that read is vacuous (always header-exact), so a re-run would have reported a false 16/16 | this PR: the endpoint reads the emission receipt when present, falls back to the audit of the archived content on legacy responses (`header_exact_endpoint_source` says which) |
| D3 | `str.splitlines()` line model in the serializer path | `patch_emission.extract_unified_diff` / `synthesize_diff_git_headers`, the frozen canonicalizer, and the suite's own `rooted_patch` (difflib on `splitlines(keepends=True)`) | latent: a context line containing VT/FF/FS/GS/RS/NEL/LS/PS is split in two, the empty half becomes a blank context marker, and the recomputed hunk count is one too large — `git apply` rejects the "canonical" patch. Not the cause of the 0/16 (GC2's generated files carry none of these bytes); it is the class of miscount a naturalistic re-run (BugsInPy-scale files with `^L` page breaks) would hit | this PR: emission shields the eight terminators behind private-use sentinels for the whole pipeline and restores them; `rooted_patch` splits newline-exact. The frozen canonicalizer is **not** modified (sha256-pinned by `E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1.json`) |

Checker discipline: `tests/unit/test_patch_emission_newline_exact_r5.py` plants D3 (the frozen
canonicalizer is shown to inflate `-1,4 +1,4` to `-1,5 +1,5` and `git apply --check` is shown to
reject it), shows the emitted patch applies, and asserts the no-alarm case (an ordinary diff is
byte-identical to the frozen canonicalizer's output with an empty shield list). A sentinel
collision is `CANNOT_CHECK`, never a pass. D2 is asserted on the evaluator source and on a
newline-exact reference patch.

## 2. What is and is not claimed

- The calibration outcome is unchanged: the semantic (count-robust) lane was at ceiling on every
  applied cell, and the ladder never entered the window. `SUITE_STILL_SATURATED` is not reopened by
  this receipt; the **secondary** interface-fidelity endpoint is what the instrument mismeasured.
- No arm comparison is licensed. No P-C terminal moves.
- The GC2 identity is marked `INSTRUMENT_SUSPECT__RERUN_PENDING`: the next execution of the frozen
  ladder is E70-GC2 **R2** (`E70_GC2_R2_RERUN_UNDER_EMISSION_DESIGN_V1.{md,json}`), which runs the
  identical frozen design through the repaired instrument. It is channel-dependent and is staged
  behind the frozen channel's window; it does not run on this receipt's authority.

## 3. Pre-registered expectation for R2 (written before any R2 call)

Count-robust success at every rung stays at or above the calibration values (the semantic lane is
saturated; the instrument does not touch it). The receipt-aware header-exact endpoint is reported
per rung as a *measurement of the model's serialization* — it may be anything from 0/16 to 16/16 and
routes nothing. Terminal vocabulary: `INSTRUMENT_REPAIRED__SATURATION_CONFIRMED` (no rung in the
window; expected), `INSTRUMENT_REPAIRED__WINDOW_ENTERED` (a rung enters [0.30, 0.70] — protected
generation would then follow the frozen design), `LANE_DEFECT`.

skills-applied: none (lane receipt, no manuscript content)
