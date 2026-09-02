# E70-GC2 calibration terminal receipt — `SUITE_STILL_SATURATED` (no protected generation)

**Receipt ID:** `E70_GC2_CALIBRATION_TERMINAL_RECEIPT` · **Date executed:** 2026-09-02 · **Machine-readable twin:** `E70_GC2_CALIBRATION_TERMINAL_RECEIPT.json` (authoritative; carries all 48 cell rows, custody receipts, a 786-entry sha256 manifest of non-response files and the 48 response-body hashes).
**Design (frozen before execution):** `E70_GC2_OFFCEILING_DESIGN_V1.{md,json}` — ladder, calibration window, endpoints, power and gates were fixed and committed (`1635971`) before any model call.
**Parent:** E70-GC1 R1 (`research/experiments/results/issue45/e70-gc1-r1/E70_GC1_R1_OUTCOME_RECEIPT.md`) — all arms 24/24 on the syntax-normalized lane; that family was semantically saturated for `gpt-5.6-terra`.
**Evidence class (binding):** secondary anti-copy / source-composition **calibration** evidence only. Grants no scientific truth, active-solving proof, field status or submission readiness. Licenses **no** arm comparison of any kind.

## 1. Terminal state

| Field | Value |
|---|---|
| Decision (pre-registered) | **`SUITE_STILL_SATURATED`** |
| Selected rung | none — no rung entered the frozen window |
| Protected split generated | **no** |
| Protected dispatch / arm comparison | **no** — only `SIMPLE_DIRECT` was ever dispatched, on the dev split |
| Arms with any GC2 outcome | `SIMPLE_DIRECT` only (16 tasks × 3 rungs = 48 responses) |
| Host | **billy-old** (`billy-laptop-old`), LUNARC unreachable during the calibration window (expired 2FA socket); the design's fallback clause was used and is recorded here |
| Model / executor | `gpt-5.6-terra` via codex-cli **0.150.1** (native binary sha256 `abf1bb1643a79f73…`, byte-identical to the LUNARC binary bound in E70-GC1 R1) |
| Code identity | commit `1635971`; sha256 of design JSON, generator, dispatcher, arm executable, `unified_diff_interface.py` and the pilot shell in the JSON twin |
| Python | 3.14.4 |

## 2. Per-rung calibration table (primary endpoint = count-robust native success)

Window (frozen before execution): **[0.30, 0.70]** on the `SIMPLE_DIRECT` point estimate. Wilson 95 % is reported, not decisive.

| Rung | Fragments / editable files | Hidden checks per task | Count-robust success | Rate | Wilson 95 % | In window | Raw header-exact success | Mean count-robust accuracy | Unscorable cells |
|---|---|---:|---:|---:|---|---|---:|---:|---:|
| L1 | 6 / `solver.py`, `normalize.py` | 197 | 15/16 | 0.938 | [0.717, 0.989] | **no (above)** | **0/16** | 0.938 | 0 |
| L2 | 9 / + `codebook.py` | 275 | 15/16 | 0.938 | [0.717, 0.989] | **no (above)** | **0/16** | 0.938 | 0 |
| L3 | 10 / same, + `decide_batch` quota | 287 | 16/16 | 1.000 | [0.806, 1.000] | **no (above)** | **0/16** | 1.000 | 0 |

Resource profile (SIMPLE arm, per rung): tokens 240,459 / 165,176 / 157,485 (median per cell 19,272 / 9,010 / 10,102); model wall 639 / 682 / 797 s total. Patches were multi-file in 47 of 48 cells.

**The two non-successes are not partial credit:** `L1/gc2-003` and `L2/gc2-004` both failed at *patch application* on the count-robust lane (context mismatch: `normalize.py:5`, `solver.py:3`) and scored 0.0. Where the artifact applied, the model was correct on **every** hidden check — 46/46 applied cells at accuracy 1.000, across the regression, forced-edge (revoked source, retired unit alias, corrected-vs-documented threshold, tie-break, ambiguity band), random, counterfactual-twin, surface-trap, cross-file `normalize`/`codebook` contract and order-dependent batch-quota families. There is no semantic difficulty gradient left to exploit inside this generator: the ladder raised the *baseline* difficulty as designed (generator self-check: baseline accuracy fell from 0.39–0.41 at L1 to 0.12–0.23 at L2/L3, reference 1.000 at every rung) without moving the model off ceiling.

**Interface finding, unchanged from GC1 and now sharper:** the raw header-exact endpoint is **0/16 at every rung**. All 48 emitted diffs required syntax-only canonicalization (24 hunk-count recomputations at L1 alone, plus `a/`–`b/` header normalizations); none was `INVALID_NOT_CANONICALIZABLE`. Multi-file patches carry more hunks and therefore more chances to miscount, so the raw lane degrades from GC1's 5/24 to 0/16 while the semantic lane stays at ceiling. This independently confirms the GC1 revival attribution (H-EXT-3, interface-information residual) and validates the design's decision to make the count-robust lane primary: had GC2 kept GC1's primary endpoint, it would have reported 0 % success for a model that solves essentially every task.

## 3. Custody (all pass, all three rungs)

| Check | Result |
|---|---|
| Hidden oracle absent during dispatch | `PRIVATE_ORACLE_COMMITMENT.json` per rung: 17 private files hashed (16 task oracles + the seed nonce), `private_directory_removed_before_child_process = true`, `private_path_forwarded_to_model = false` |
| Restoration | `PRIVATE_ORACLE_RESTORATION.json`: `hashes_match_commitment = true`, `dispatch_returncode = 0` on all three rungs |
| Dispatch completeness | 3 × 16 jobs, 0 non-zero return codes, 0 missing responses; 48/48 `COMPLETED_PROPOSAL_ONLY`, 48/48 evaluated (`status = EVALUATED`), 48 model calls |
| No hidden bytes in the solver channel | Request envelopes carry no checks/expected values; hidden set never rendered into a workspace; nonce committed by sha256 only, so no child process can regenerate the hidden set from the public protocol |
| Manifests | 786 non-response files by sha256 in the JSON twin; 48 response bodies referenced by hash (bodies stay on the execution host) |

## 4. Honest reading

1. **The generated-composition family is semantically saturated for `gpt-5.6-terra` at every rung of the frozen ladder.** Adding a superseded distractor, an erratum that both corrects a threshold and revokes a source, an affine offset unit, a legacy-alias/retired-unit trap, a second and third editable file with hidden cross-file contracts, a conditional tie-break, an authority-conditional ambiguity band and an order-dependent batch quota did not move the SIMPLE arm off ceiling.
2. **Under the frozen procedure this terminates the run.** The ladder is not re-tuned after a calibration outcome is seen, so no protected split was generated and no arm was compared. Nothing here says anything about F2, F0 or reflection — the design's whole point is that a saturated suite has zero discriminative power, and reporting a contrast from it would be the error GC1 already documented.
3. **What is licensed:** a second, stronger anti-copy observation. On 48 post-freeze generated tasks whose symbols, units, thresholds, labels, sources and hidden checks did not exist before 2026-09-02, with the oracle provably absent from disk during dispatch, the model composed 6–10 fragments across 2–3 files — including rules that contradict their own documentation (erratum) and rules requiring an explicit distractor to be ignored — at accuracy 1.000 on every applied cell. This is consistent with active composition rather than retrieval, and it does **not** prove absence of training-data influence.
4. **What is not licensed:** any superiority or inferiority claim for any arm; any change to a paper's scientific terminal; any claim that the ORION lifecycle helps or hurts on composition tasks.
5. **Verdict class:** `CALIBRATION_COMPLETE_48_OF_48__CUSTODY_CLEAN__ALL_THREE_RUNGS_ABOVE_WINDOW__SUITE_STILL_SATURATED__NO_PROTECTED_GENERATION__NO_ARM_COMPARISON_LICENSED__RAW_HEADER_EXACT_ENDPOINT_ZERO_AT_EVERY_RUNG`.

## 5. What would be needed (proposal only — not a licensed design, nothing scheduled)

The constraint is now precise: **synthetic rule-composition difficulty does not bind this model, and stacking more frozen rules is not a lever.** Two directions follow, both requiring their own prospective freeze before any run:

- **Change the task family, not the rule count.** Move to naturalistic multi-file defects at BugsInPy / real-repository scale, where difficulty comes from unfamiliar code, long-range dependencies and incomplete failure information rather than from rules the model can read off a spec. E30/E60 already show non-ceiling rates there (F2 5/40, arms 4–7/40), which is the regime a discriminative comparison needs; the open cost is that such tasks are not post-freeze-fresh, so the anti-copy property GC1/GC2 were built for is weakened and would have to be recovered by another control (e.g. post-freeze mutation of real defects).
- **Change the subject.** Run the identical frozen GC2 ladder against a weaker or smaller model. If a rung lands in the window there, the suite retains discriminative power for that subject and the ladder is reusable as frozen; a capability-conditional comparison is a narrower claim but an honest one.
- **Not proposed:** re-tuning this ladder post hoc, adding rungs after seeing this outcome, or reporting any F2/F0 contrast from the dev split.

## 6. Downstream bindings

- Issue #45 Phase 5: E70-GC1 R1 remains the E70 pilot terminal; **E70-GC2 terminates at calibration** and produces no protected result.
- `EXECUTION_BACKLOG_V1.json`: unchanged (no status field in that schema; no new evidence head).
- Paper registry / P-C status row: **untouched** — no scientific terminal changes.

## 7. Artifacts

`E70_GC2_OFFCEILING_DESIGN_V1.{md,json}`, `E70_GC2_POWER_ANALYSIS.json`, `E70_GC2_CALIBRATION_TERMINAL_RECEIPT.{md,json}`, `drivers/assemble_gc2_calibration_receipt.py`, `drivers/e70_gc2_protected_r1.sbatch` and `drivers/e70_gc2_protected_r1_billyold.sh` (unused — no protected run), plus the code: `scripts/run_orion_generated_composition_gc2_suite.py`, `scripts/run_orion_generated_composition_gc2_pilot.sh`, `tests/unit/test_generated_composition_gc2_suite.py`, `tests/unit/fixtures_gc2_fake_arm.py`, and the `--runner-script` extension to `scripts/dispatch_orion_gc1_blinded.py`.

skills-applied: none (receipt, no manuscript content)
