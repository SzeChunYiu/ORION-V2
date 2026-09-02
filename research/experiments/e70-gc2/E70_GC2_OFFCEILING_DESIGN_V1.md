# E70-GC2 — Off-ceiling generated composition design V1 (issue #45, Phase 5)

**Design ID:** `E70_GC2_OFFCEILING_DESIGN_V1` · **Status:** `PROSPECTIVE_SECONDARY_ANTI_COPY_PROTOCOL_NO_RESULTS` · **Frozen:** 2026-09-02 · **Machine-readable twin:** `E70_GC2_OFFCEILING_DESIGN_V1.json` (authoritative for every number below).
**Parent:** E70-GC1 R1 (`research/experiments/results/issue45/e70-gc1-r1/E70_GC1_R1_OUTCOME_RECEIPT.md`): all four arms 24/24 on the syntax-normalized lane; the entire raw-endpoint variance was unified-diff hunk-header miscount. The GC1 family is semantically saturated for `gpt-5.6-terra` and has zero discriminative power for composition ability.
**Evidence class (binding):** secondary fresh anti-copy / source-composition evidence only. Cannot replace E30/E40/E50; does not prove absence of training-data influence; grants no scientific truth, active-solving proof, field status or submission readiness.

## 1. What changes versus GC1 (one lever per GC1 finding)

| GC1 finding | GC2 response |
|---|---|
| Semantic endpoint at ceiling for every arm | Frozen three-rung difficulty ladder (§2) + outcome-blind calibration on a dev split (§3) so the SIMPLE arm sits in 0.3–0.7 |
| Raw variance = hunk-header miscount (interface, not composition) | Primary endpoint = **count-robust native success** through the registered E20/E30 syntax-only canonicalizer (§4); header-exact raw success demoted to a secondary interface-fidelity endpoint |
| 24 tasks × 1 rep, can only detect near-total dominance | n from a prospective simulation power analysis (§5): 96 tasks × 3 nested reps × 4 arms = 1152 responses |
| Single-file, four-fragment family | Multi-file (2–3 editable files), 6–10 fragments incl. an explicit superseded distractor and an erratum, hidden regression / counterfactual / surface-trap / cross-file contract checks (Phase 5 controls) |

Arms are identical to GC1 (`SIMPLE_DIRECT`, `SAME_MODEL_REFLECTION`, `F0_PARENT_FEDERATION`, `F2_ORION_METABOLIC_FULL`), the arm executable (`scripts/orion_codex_arms.py`) and its prompt are unchanged, and the oracle-absent dispatch machinery (`scripts/dispatch_orion_gc1_blinded.py`) is reused with a `--runner-script` pointer. Minus-component arms are deferred until this design leaves the ceiling.

## 2. Frozen difficulty ladder (generator: `scripts/run_orion_generated_composition_gc2_suite.py`, `LADDER`)

Every rung is a strict superset of the one below. Rungs are frozen here; they are never re-tuned after a calibration or protected outcome is seen.

| Rung | Fragments | Editable files | Added mechanics | Hidden checks / task |
|---|---:|---|---|---:|
| L1 | 6 | `solver.py`, `normalize.py` | superseded-revision distractor; erratum that corrects the accept threshold **and revokes one documented source**; affine offset unit; hidden `normalize.to_primary` contract (cross-file); public regression tests | ≈197 |
| L2 | 9 | + `codebook.py` | legacy alias unit + retired alias trap; stale/incomplete codebook that must be completed; tie-break (score = high−1, even y); ambiguity band conditional on primary authority | ≈275 |
| L3 | 10 | same | `solver.decide_batch` with an order-dependent per-source accept quota (12 hidden batches) | ≈287 |

Hidden families (all withheld from the workspace): `regression` (behaviour the incomplete baseline already gets right), forced `edge_*` cases (revoked source, unknown/retired unit, counterexample, corrected vs documented threshold, low boundary, offset unit with negative x, alias, tie-break, ambiguity band), `random` (120–160), `counterfactual_base`/`counterfactual_twin:<mutation>` (one-field interventions that flip the label; 16–24 pairs), `surface_trap_*` (public examples re-issued with a hidden field changed), `normalize_contract` (24–32), `codebook_contract`, `batch_quota`. Generator self-check, asserted per task at generation and recorded in `FROZEN_TASKS.generator_self_check`: the reference solution passes 100 % of hidden checks, the baseline does not (smoke: baseline accuracy 0.12–0.39).

All symbols, units, thresholds, labels, source tokens and records are drawn from the run seed; the run seed is `sha256(seed:nonce)` where the nonce is drawn at generation, its sha256 committed in `FROZEN_TASKS.json`, and the nonce bytes live only under `private/` (absent from disk during dispatch). No child process can regenerate the hidden set from the public protocol.

## 3. Pre-registered outcome-blind difficulty calibration (dev split only)

* Arm: `SIMPLE_DIRECT` only, 1 rep. Dev seed `20260902`, 16 dev tasks per rung, dev nonce distinct from the protected nonce. No protected arm ever sees a dev task; no protected-seed task exists before calibration closes.
* Endpoint: primary (count-robust). Window **[0.30, 0.70]** on the point estimate (Wilson 95 % reported, not decisive).
* Procedure: ascend L1 → L2 → L3, stop at the first rung inside the window → `WINDOW_HIT`, rung frozen into `protected.ladder_level`. Every rung above the window → **`SUITE_STILL_SATURATED`** (stop; report the numbers; no protected generation). A rung below the window after one above it → `LADDER_OVERSHOT_NO_WINDOW_HIT` (stop; the ladder is not re-tuned post hoc). Below the window at L1 → `SUITE_AT_FLOOR_AT_FIRST_RUNG`.
* Receipt: `E70_GC2_CALIBRATION_RECEIPT_DEV.json` (host, codex/model binding, per-rung counts, decision).

## 4. Endpoints

**Primary — `count_robust_hidden_oracle_success`.** The emitted unified diff is passed through `src/orion_v2/unified_diff_interface.py` (arm-blind; may only recompute hunk old/new counts from the hunk body, normalize `a/`/`b/` headers already bound by the `diff --git` line, and blank context markers; may never infer paths, start lines or semantic lines — the contract registered in `research/evaluation/E20_PATCH_SERIALIZATION_CONFOUND_AUDIT_V1.md` and frozen in `E30_SYNTAX_SENSITIVITY_CONTROL_FREEZE_V1.json`), applied with `git apply` to a fresh copy of the public workspace restricted to the editable files, and every hidden check must pass. Fail-closed: `INVALID_NOT_CANONICALIZABLE`, a path outside the editable set, a rename, an import failure, a runtime error or a timeout are failures.

**Secondary:** `raw_hidden_oracle_success` (header-exact, GC1's primary; interface-fidelity), count-robust / raw patch-apply, count-robust hidden accuracy (continuous), per-family accuracy, tokens, wall time, patch bytes.

## 5. Power and sample size (`E70_GC2_POWER_ANALYSIS.json`, seed 20260902)

Task-level exact two-sided discordant (sign) test on majority-of-3-reps task outcomes; task heterogeneity Beta(mean 0.5, concentration 4); treatment = logit shift giving a marginal rep-level risk difference of **0.15**; α = 0.05 two-sided; 1000 simulations per n. Simulated power: n = 80 → 0.807, 88 → 0.814, **96 → 0.884**, 120 → 0.953. Rule (frozen): smallest grid n whose power minus two Monte-Carlo SEs (≈0.025) clears 0.80 → **n = 96 tasks**, 3 reps, 4 arms = 1152 responses. Analytic McNemar cross-check under rep-level independence without reps: 173 pairs (reps and task heterogeneity are what buy the reduction; the assumption set is stated, not hidden).

## 6. Analysis (E30-R11 / E60 conventions)

Unit = frozen task; task outcome = majority over 3 nested reps (registered), with all-reps / any-rep aggregations and rep-level rates reported descriptively. Exact discordant test + paired bootstrap CI95 (10 000, seeded) on the risk difference. Multiplicity: fixed-sequence gatekeeping **G1** (F2 vs F0) → **G2** (F2 vs SIMPLE) → **G3** (F2 vs REFLECTION), each at α = 0.05, a later gate tested only if the earlier one rejects in F2's favour; Holm over the three-contrast family reported as robustness. Parent sufficiency: F0 vs SIMPLE, descriptive, uncorrected, outside the family. Post-outcome diagnostics only: identical canonical-patch rate across arms (rep 1) and the per-family accuracy breakdown.

## 7. Gates and routing

* **G0 validity:** commitment/restoration hashes match; no private bytes in any request envelope; calibration `WINDOW_HIT` at the frozen rung; all 1152 cells evaluated (a missing cell is regenerated one-shot from its frozen request *before* any analysis; never after outcome access); generator self-check recorded. Protected SIMPLE count-robust rep-level rate ≥ 0.95 → `SUITE_STILL_SATURATED`; ≤ 0.05 → `SUITE_AT_FLOOR`.
* **Routing:** `POSITIVE_F2_BEATS_PARENT_AND_SIMPLE` (G1 ∧ G2) · `PARTIAL_F2_BEATS_PARENT_NOT_SIMPLE` · `NEGATIVE_COMPONENT_HARM_F2_BELOW_PARENT` (G1 rejects for F0) · `NEGATIVE_PARENT_SUFFICIENT` (G1 not rejected, F0 > SIMPLE descriptively) · `NEGATIVE_NO_DETECTABLE_F2_GAIN_AT_MDE` · `SUITE_STILL_SATURATED` · `SUITE_AT_FLOOR` · `G0_FAIL_*`.
* **Phase 5 anti-memorization controls:** gold withheld; fresh evaluator workspaces per cell; retrieval-off instruction + `codex --sandbox read-only` (not provably enforced at the network layer — recorded limitation, as in GC1); post-freeze identifier/label/unit permutations; hidden regression tests; counterfactual twins and surface traps; source-use and stage receipts; solution-similarity diagnostic post-outcome only; nonce commitment.

## 8. No-rescue clause

After any protected outcome is inspected there is no change to the generator, ladder, canonicalizer, evaluator, checks, arms, seeds, task count, aggregation or gates; no re-dispatch of an evaluated cell; no normalization beyond the registered syntax-only canonicalization; no post hoc rung change. A defect discovered after outcome access requires a new run identity (E70-GC2 R2) with a new nonce.

## 9. Custody and execution

Campaign `orion-v2-e45/campaign-e70-gc2-r1` on LUNARC (lu48, lu2026-2-51), or the recorded fallback host with the same machinery; pipeline `scripts/run_orion_generated_composition_gc2_pilot.sh`; dispatch through `scripts/dispatch_orion_gc1_blinded.py --runner-script scripts/run_orion_generated_composition_gc2_suite.py` (private oracle + nonce hashed, removed before any child process, restored and hash-verified after). The outcome receipt binds sha256 of the design JSON, generator, dispatcher, arm executable, `unified_diff_interface.py` and the pilot shell, plus manifests of all non-response files and response bodies (referenced by hash).

skills-applied: none (design freeze, no manuscript content)
