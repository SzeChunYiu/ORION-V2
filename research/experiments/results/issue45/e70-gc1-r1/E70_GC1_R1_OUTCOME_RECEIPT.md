# E70-GC1 R1 Outcome Receipt — generated-composition (anti-copy) pilot

**Receipt ID:** `E70_GC1_R1_OUTCOME_RECEIPT`
**Date (executed):** 2026-09-02 (SLURM job 3563411, COMPLETED 00:31:56, exit 0:0, node cn133, lu48, 2 cpus / 8G)
**Campaign:** `campaign-e70-gc1-r1` (LUNARC, `/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e70-gc1-r1`) — 4 core pilot arms × 24 frozen generated tasks × 1 repetition = 96 responses.
**Protocol:** `research/experiments/ORION_GENERATED_COMPOSITION_COUNTERFACTUAL_SUITE_V1.json` (suite `E70-GC1`, freeze 2026-08-28, seed 20260828; `FROZEN_TASKS.json.protocol_sha256 = fc5e084c…`).
**Supersedes:** `RESULT.md` (dispatch-time stub, `DISPATCH_QUEUED_DEFERRED_ACCOUNT_WALL`, all arms CANNOT_CHECK).
**Evidence class (binding, from the protocol):** secondary fresh anti-copy / source-composition evidence only. Cannot replace E30/E40/E50; does not prove absence of training-data influence; grants no scientific truth, active-solving proof, field status or submission readiness.

## 1. Terminal execution state

| Check | Value |
|---|---|
| Dispatch | Deferred job 3553088 (`--begin=2026-09-04T08:00`) CANCELLED at 05:49:18 cluster clock; the **unchanged** sbatch `e70_gc1_dispatch_deferred_r1.sbatch` (sha256 `f596371d…`, identical to the copy in this directory) resubmitted with `--begin=now` after the codex login was refreshed. Submit 05:49:19, start 05:49:20, end 06:21:16. |
| Availability probe | `PROBE_OK attempt=1 reply=OK` (first attempt of the 20-attempt loop). |
| Preflight inside the job | `py_compile` clean; `pytest -q` 9/9 on `test_unified_diff_interface_wave6.py` + `test_generated_composition_suite_wave6.py`. |
| Pipeline | `generate --force` → blinded `dispatch` (max-concurrency 2) → `evaluate` → `analyze`, all via `scripts/run_orion_generated_composition_pilot.sh` verbatim. |
| Responses | **96/96** (24 per arm); every response `status = COMPLETED_PROPOSAL_ONLY`; `DISPATCH_RECEIPT.json`: 96 jobs, `returncode = 0` ×96, `response_exists = true` ×96. |
| Authority flags | `scientific_truth_authorized = field_status_authorized = publication_readiness_authorized = false` ×96; `requested_authority = EXECUTION_TEST_ONLY` ×96. |
| F2 lifecycle | `metabolic_stages` carries 9/9 stage receipts on all 24 F2 responses. |
| Model / executor | codex-cli 0.150.1, model `gpt-5.6-terra`, one model call per response (`resource_receipt`); bindings in `ENVIRONMENT_AND_MODEL_BINDINGS.json`. |
| stderr | `slurm-3563411.err` is empty (0 lines). |
| Code identity | Clone `orion-v2-wave6` at `1f49eda` during the run (reflog: checkout to `main`/`0cb3348` at 06:22:16, one minute after the job ended). The six run-relevant blobs (`ORION_GENERATED_COMPOSITION_COUNTERFACTUAL_SUITE_V1.json`, `run_orion_generated_composition_pilot.sh`, `run_orion_generated_composition_suite.py`, `dispatch_orion_gc1_blinded.py`, `orion_codex_arms.py`, `src/orion_v2/unified_diff_interface.py`) are blob-identical at `1f49eda`, `0cb3348` and current `origin/main`; pilot-entrypoint and arm-executable sha256 match `ENVIRONMENT_AND_MODEL_BINDINGS.json`; protocol sha256 `fc5e084c…` matches `FROZEN_TASKS.json`. |

## 2. Custody checks (all pass)

| Check | Result |
|---|---|
| Hidden oracle absent during dispatch | `PRIVATE_ORACLE_COMMITMENT.json`: 24 private files hashed, `private_directory_removed_before_child_process = true`, `private_path_forwarded_to_model = false`, status `COMMITTED_BEFORE_MODEL_DISPATCH`. |
| Restoration | `PRIVATE_ORACLE_RESTORATION.json`: 24 restored, `hashes_match_commitment = true`, `dispatch_returncode = 0`. Commitment map == restoration map (24/24 sha256 equal). |
| Oracle still intact | `private/*.json` re-hashed on 2026-09-02 after the run: 24/24 equal to the commitment. |
| No private bytes in the solver channel | 96 request envelopes contain no `expected`, `records`, `/private/`, `scale_factor` or `allowed_sources` markers; `source_ids_used` union over 96 responses = `{gold-blind-solver-workspace}`; `FROZEN_TASKS.json.private_gold_mounted_to_solver = false`. |
| Manifest | `CUSTODY_MANIFEST_SHA256_NON_RESPONSES.json` — 1,518 files (public workspaces, requests, private oracle, evaluations, raw + syntax-normalized evaluation trees, aggregate, receipts); `CUSTODY_MANIFEST_SHA256_RESPONSES.json` — 96 response bodies (referenced by hash; bodies stay on LUNARC). |
| Deviation (recorded) | The sbatch writes its probe stdout/log into `<workdir>/infra/`, and the pilot's `generate --force` then recreates the workdir, so the probe files did not survive the run. The `PROBE_OK` line is preserved in `slurm-3563411.out`. Pre-run probe/binary receipts referenced by `INFRASTRUCTURE_RECEIPT.md` were likewise removed; the binary sha256 in `ENVIRONMENT_AND_MODEL_BINDINGS.json` remains the binding record. |

## 3. Endpoint table (24 tasks per arm, 96 hidden cases per task)

Primary endpoint = `raw_hidden_oracle_success` (the raw emitted unified diff applies and passes all 96 hidden cases). Secondary = syntax-normalized success (E20 syntax-only canonicalization; semantic repair forbidden), patch-apply, resources.

| Arm | Raw hidden success | Mean raw hidden accuracy | Raw `git apply` failures | Under-count truncation (partial / zero acc.) | Syntax-normalized success | Hunk header changed by canonicalization | Model tokens (total / median) | Model wall (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `SIMPLE_DIRECT` | 5/24 (0.208) | 0.457 | 10 | 7 / 2 | **24/24** | 19 | 242,586 / 7,587 | 835.6 |
| `SAME_MODEL_REFLECTION` | 5/24 (0.208) | 0.355 | 14 | 4 / 1 | **24/24** | 19 | 245,654 / 8,068 | 1,031.6 |
| `F0_PARENT_FEDERATION` | **8/24 (0.333)** | 0.509 | 10 | 5 / 1 | **24/24** | 16 | 164,594 / 6,946 | 888.8 |
| `F2_ORION_METABOLIC_FULL` | **3/24 (0.125)** | 0.309 | 14 | 5 / 2 | **24/24** | 21 | 210,163 / 7,672 | 936.0 |

Per-task pattern on the primary endpoint: 8 tasks solved raw by no arm (`gc1-004/005/006/009/013/015/016/019`), 12 by exactly one arm, 3 by two, 1 by three, 0 by all four. Every arm reaches 24/24 on the syntax-normalized lane with accuracy 1.000 on all 96 cells — the secondary endpoint is at ceiling.

## 4. Paired tests (task-level, exact discordant test, Holm family = F2 vs each of 3 controls)

The pilot's own analysis layer (`aggregate/analysis.json`) emits task-level exact discordant p-values and a 10,000-rep paired bootstrap (seed 20260828) but no Holm correction; the Holm column below is added by `drivers/e70_gc1_r1_paired_analysis.py` over the same verbatim evaluation records (`E70_GC1_R1_EVALUATION_ROLLUP.json`). Nothing was re-scored.

**Primary — raw hidden-oracle success**

| Comparison | Both / neither | Discordants (F2-only / control-only) | Risk difference (pilot bootstrap CI95) | Exact p | Holm p | Reject |
|---|---|---|---|---|---|---|
| F2 vs `F0_PARENT_FEDERATION` | 1 / 14 | 2 / 7 | −0.208 [−0.458, 0.000] | 0.180 | 0.539 | no |
| F2 vs `SIMPLE_DIRECT` | 1 / 17 | 2 / 4 | −0.083 [−0.292, 0.125] | 0.688 | 1.000 | no |
| F2 vs `SAME_MODEL_REFLECTION` | 0 / 16 | 3 / 5 | −0.083 [−0.292, 0.167] | 0.727 | 1.000 | no |

**Secondary — raw patch applies:** F2 vs F0 2/6 (p 0.289, Holm 0.867); vs SIMPLE 6/10 (p 0.454, Holm 0.909); vs REFLECTION 5/5 (p 1.0). **Secondary — syntax-normalized success:** 0 discordants in every contrast (all arms 24/24; test undefined). **Descriptive, outside the family, uncorrected:** F0 vs SIMPLE 6/3 (p 0.508); F0 vs REFLECTION 6/3 (p 0.508).

**Per-family breakdown:** `FROZEN_TASKS.json` carries no per-task counterfactual-family label — all 24 tasks are one registered family (four-fragment composition: measurement/normalization, source authority, threshold/codebook, precedence; generated coordinates in `private_spec_features_no_cases.json`, hidden cases withheld). A breakdown by family therefore reduces to the failure-mode ledger in §6; on the semantic (normalized) lane every family branch, including the three forced authority/unit/counterexample edge cases per task, passes for every arm.

**Power (stated, binding):** 24 paired tasks with 9 discordant pairs (F2 vs F0) can reject at α = 0.05 only a 1-vs-8 or more extreme split (p = 0.039); the observed 2-vs-7 gives p = 0.180. The pilot detects only near-total one-sided dominance and is not powered for moderate arm differences. No direction of superiority is established.

## 5. Honest verdict

1. **Execution complete and custody-clean:** 96/96 responses, oracle provably absent from disk during dispatch, restoration hash-verified, no private bytes in the solver channel.
2. **Primary endpoint adverse for F2, not significant:** F2 3/24 is numerically last; `F0_PARENT_FEDERATION` 8/24 is numerically first; no contrast survives Holm (smallest Holm p = 0.539). The protocol's *negative* reading applies ("F2 ties/loses to simpler or parent controls") **as a pilot-scale observation**, not as a certified effect.
3. **Secondary endpoint at ceiling:** with syntax-only canonicalization every arm solves every task (96/96, accuracy 1.000). The whole raw-endpoint variance is patch serialization, not composition (§6).
4. **Verdict class:** `EXECUTION_COMPLETE_96_OF_96__CUSTODY_CLEAN__PRIMARY_RAW_ENDPOINT_ADVERSE_FOR_F2_NOT_SIGNIFICANT__F0_NUMERICALLY_BEST__SYNTAX_NORMALIZED_ENDPOINT_AT_CEILING_ALL_ARMS__UNDERPOWERED_PILOT__DEFICIT_ATTRIBUTED_TO_PATCH_SERIALIZATION_INTERFACE`
5. `publication_readiness`, `field_status`, `active_solving_proof`: `NOT_ESTABLISHED`.

**What this receipt licenses.** (a) Anti-copy/composition evidence only: on a post-freeze generated suite whose symbols, units, thresholds, labels and hidden cases did not exist before 2026-08-28, all four arms composed the four public fragments into a correct `decide` on all 24 tasks (normalized lane) — consistent with active composition rather than retrieval of a memorised solution. (b) It does **not** prove absence of training-data influence, does **not** license any superiority claim in either direction (F0's lead is not significant and is a serialization-fidelity difference), does **not** replace the naturalistic E30/E40/E50 evidence, and does **not** change P-C's scientific terminal (it is consistent with P-C's existing "software repair shows no terminal-rate advantage" line and adds no new claim).

## 6. Revival attribution — ONE stage, one lever, one register row

**Failure ledger (primary endpoint, per arm):**

| Arm | Success (header exact) | Header over-count → `git apply` "corrupt patch" | Header under-count → silent hunk truncation, partial acc. | … zero acc. |
|---|---:|---:|---:|---:|
| `SIMPLE_DIRECT` | 5 | 10 | 7 | 2 |
| `SAME_MODEL_REFLECTION` | 5 | 14 | 4 | 1 |
| `F0_PARENT_FEDERATION` | 8 | 10 | 5 | 1 |
| `F2_ORION_METABOLIC_FULL` | 3 | 14 | 5 | 2 |

**Attributed stage: proposal serialization — the unified-diff hunk-header line count (`@@ -1,4 +1,N @@`).** Evidence: (i) in all four arms, raw success holds **if and only if** the canonicalizer left the header unchanged (`success_iff_header_unchanged = true` ×4); (ii) recomputing the count and nothing else yields 96/96 hidden-oracle success — there is no semantic failure left to attribute; (iii) the two failure mechanisms are verified on the raw evaluation trees: an over-counted `N` makes `git apply` reject the patch ("corrupt patch at line 27–34"), an under-counted `N` makes `git apply` silently stop after `N` lines, leaving a prefix of the intended `solver.py` (raw file is a strict prefix of the normalized file on the probed cells `SIMPLE_DIRECT/gc1-004`, `F2/gc1-006`, `F2/gc1-020`), which runs but mis-scores. Decomposition drag, counterprobe over-conservatism and reflection dilution are **excluded** as the stage: every arm's semantic proposal is correct, so no lifecycle stage changed what was composed; F2's deficit is 21 miscounted headers vs F0's 16 (p = 0.18), and the miscount rate is not monotone in reasoning volume (`SIMPLE_DIRECT` spent the most tokens and still miscounted 19).

**Matching lever: the artifact interface, not the controller.** Register the count-robust contract as the primary raw lane — a full-file replacement artifact, or `git apply --recount` with the E20 syntax-only canonicalization already frozen as the secondary protocol — and demote header-exact fidelity to a secondary "interface-fidelity" endpoint. No new mechanism is claimed; the lever is already registered (`research/evaluation/E20_PATCH_SERIALIZATION_CONFOUND_AUDIT_V1.md`).

**Extension-register mapping:** this pattern most resembles **H-EXT-3** (interface-information residual: what crosses a module boundary — here the solver→evaluator boundary — determines the observed outcome; honest terminal `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`). **H-EXT-1 (conditional activation) is explicitly not the match:** the deficit does not concentrate in any input-detectable family — the semantic endpoint is at ceiling for every arm, so there is no regime in which F2's machinery binds or drags and nothing for a gate to condition on.

**Suite limitation (binding for GC2):** as frozen, the generated family is semantically saturated for `gpt-5.6-terra` (96/96 after recount); it has zero discriminative power for composition ability and measures only diff-serialization fidelity.

**Named next design — E70-GC2 (design freeze first; no revival claim, no outcome predicted):** (1) raise semantic difficulty until a development-seed `SIMPLE_DIRECT` normalized success rate sits clearly off both floors and ceilings — distractor fragments, conflicting precedence, ≥2 files, larger hidden edge families; (2) primary endpoint on the count-robust artifact contract, header-exact raw apply as a secondary interface-fidelity endpoint; (3) task count set by a pre-registered power calculation under the E30-R11 conventions, ≥3 repetitions to expose endpoint nondeterminism; (4) F2 minus-component arms only once (1)–(3) leave the ceiling.

## 7. Downstream bindings

- `research/experiments/EXECUTION_BACKLOG_V1.json` E70 row: no row in that file carries a status field (schema keys are id/title/priority/type/dependencies/runnable_now/controls/paper_targets/done_when/…), so the row is left unchanged; its `done_when` ("active-solving evidence reported without claiming proof of training-data absence") is met at pilot scope by this receipt.
- ORION-paper P-C status row: **left untouched.** The registry update rule triggers on a change of a paper's scientific terminal and requires `PAPER_REGISTRY.json` first plus the dashboard in the same commit with the new ORION-V2 evidence head; this pilot changes no terminal, and the evidence-head binding needs the merged commit of this receipt. Import note for the P-C lane: "E70-GC1 R1 (24 generated composition tasks, oracle absent at dispatch): F2 3/24 vs F0 8/24 vs direct 5/24 vs reflection 5/24, no contrast significant (Holm ≥ 0.539); all arms 24/24 after syntax-only patch recount — the raw deficit is diff-serialization fidelity, not composition; underpowered pilot; no claim in either direction."
- Issue #45 Phase 5: this receipt is the E70 pilot terminal; E70-GC2 is a named design, not a scheduled run.

## 8. Artifacts in this directory

`E70_GC1_R1_OUTCOME_RECEIPT.{md,json}` (this receipt), `E70_GC1_R1_PAIRED_ANALYSIS.json` + `drivers/e70_gc1_r1_paired_analysis.py` (reproducible from the rollup), `E70_GC1_R1_EVALUATION_ROLLUP.json` (96 verbatim evaluation records), `aggregate/analysis.json` (pilot's own analysis), `EXECUTION_SUMMARY.md`, `DISPATCH_RECEIPT.json`, `FROZEN_TASKS.json`, `PRIVATE_ORACLE_COMMITMENT.json`, `PRIVATE_ORACLE_RESTORATION.json`, `private_spec_features_no_cases.json` (generated coordinates, hidden cases withheld), `CUSTODY_MANIFEST_SHA256_{NON_RESPONSES,RESPONSES}.json`, `slurm-3563411.{out,err}`, plus the prep-time `INFRASTRUCTURE_RECEIPT.md`, `ENVIRONMENT_AND_MODEL_BINDINGS.json`, `e70_gc1_dispatch_deferred_r1.sbatch`, `RUN_IDENTITY.json`, `JOB_IDS.env`, `RESULT.md` (superseded stub).

skills-applied: none (receipt, no manuscript content)
