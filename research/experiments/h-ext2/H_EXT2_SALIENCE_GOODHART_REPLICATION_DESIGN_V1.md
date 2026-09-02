# H-EXT-2 — Internal-Salience Goodhart Replication Design V1 (frozen; NO dispatch)

**Lineage:** `research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md`
row H-EXT-2 (S2 candidate). Evidence base: E40-m5′ Stage-1 screen (PR #131/#135):
`sig_purity` = sig-TP / max(total-TP, 1) **anti-ranked** raw wasserstein truth on
cohort R (raw ρ = +0.494, perm p = 0.0022, 9/12 chains positive) and trended the
same way on cohort P (+0.224, p = 0.175). The screen had registered `sig_purity`
as +1 (higher = better) and correctly refused post-hoc inversion.
**Class:** prospective native campaign under a NEW identity; the m5′ observation
becomes a *pre-registered directed claim* on a **fresh cell** (different native
learner, same pinned substrate). Freeze precedes any run (m-series discipline).
**Status:** design only. Dispatch is **not licensed by this document** (§9).

## 1. Question

Is the loop's self-generated salience signal (`sig_purity`, produced by the
feedback channel the loop itself consumes) anti-aligned with quantitative truth
as a *mechanism* — i.e. does the anti-ranking replicate under a pre-registered
direction on a fresh native learner, in both cohorts, and is it **specific to the
in-channel signal** (absent for a channel-external signal)?

Parents (absorbed, not avoided): Goodhart / specification gaming, reward hacking,
p-hacking-as-selection, Lucas critique. The delta under test is the **locus**
only: the signal is produced and consumed by the same loop. A positive here
grants one rung on the register ladder, no field/novelty/publication status.

## 2. Fresh-cell feasibility (LUNARC reconnaissance, 2026-09-02, read-only)

Substrate: pinned CausalBench at `campaign-e40-r3/causalbench` (causalbench 1.1.2,
venv Python 3.11.5, torch 2.13.0+cu130 with **CUDA unavailable** on `lu48`,
48 threads visible). `METHODS` at the pinned install: random100/1000/10000,
fully-connected, lasso, random_forest, grnboost, genie, ges, gies, pc, mvpc,
gsp, igsp, notears-{lin,lin-sparse,mlp,mlp-sparse}, DCDI-{G,DSF},
DCDFG-{LIN,MLP}, sortnregress (+ oracle/evaluator pseudo-models, excluded).

Parent-cell cost anchors (verified from frozen receipts/logs/sacct):

| Quantity | Value |
|---|---|
| gies model-train `run_time` | m2 n=120: min 50.9 s, median 116 s, max 152 s; m3 n=60: median 113 s |
| gies full native invocation (load + evaluators + train + eval) | 5 min 54 s wall, 21.5 GB RSS (m3 exp 501000) |
| m3 F2 chain wall (4 native + 4 decision calls) | k562 22:10–23:21; rpe1 12:28–14:05 (sacct 3554920, 8 CPU) |
| m2 array task wall | 3:11 (simple) – 24:57 (F2), 36 tasks `%6` |
| m3 model calls | 48 F2 decisions + 9 planted + 48 uninformative (+ ≤3 re-asks each) |

Learner feasibility (code-level facts; runtimes for non-gies learners are
**unverified** — no non-gies/non-pc run exists in any E40 campaign dir):

| learner | uses interventions | primary defined across regimes | runtime evidence | seed-sensitive (G2 replica) | verdict |
|---|---|---|---|---|---|
| gies | yes (30-gene partitions, threaded) | yes (0/108 NaN in m2) | above | partition seed | **parent cell** — not fresh |
| pc, mvpc, ges, gsp, notears-* | no: `return []` unless Observational | **no** — NaN primary on the interventional family (m1: f0 36/48 NaN) | pc 1–4 s | — | excluded (m1 confound: degenerate decision space) |
| DCDI-G / DCDI-DSF | yes | expected | `opt.gpu = True` hard-coded → CUDA default tensors; **fails on lu48** (no CUDA); 60 000 iters | yes | excluded for the CPU lane (GPU partitions exist: gpua40/gpua100; not provisioned, not verified) |
| **DCDFG-LIN** (DCDFG-MLP) | **yes** (WeissmannDataset carries interventions) | expected (edges from thresholded module graph) | pytorch-lightning, 600 + 50 epochs, batch 64, early-stopping patience 5; CPU accelerator by default; **wall unknown** | yes (train/val split + init) | **PRIMARY candidate** (different learner family: differentiable vs greedy score-based) |
| igsp | yes (causaldag `igsp`, invariance tests, α = 1e-3) | expected | **no partitioning** (full gene set after 0.5 expression filter; one setting per intervened gene) — runtime risk, **wall unknown** | no (seed unused) → G2 replica degenerate | fallback 2 |
| grnboost / genie | labels ignored; all cells used | yes (always returns edges) | arboreto GRNBoost2 via dask `LocalCluster(25 workers × 5 threads)` on 8 CPUs; **wall unknown** | yes | fallback 3 (knobs act only through sample composition) |
| sortnregress | labels ignored | yes | fast (regression) | no | not registered (linear-regression ordering is too close to "no learner") |

**Cross-substrate option (E50 / Matbench Discovery): NOT feasible now.**
`campaign-e50-r{1,2,3}/run/venv` site-packages hold only pip/setuptools/packaging
(0 matbench/pymatgen entries); `E50_NATIVE_RESULT.json` was produced on
`billy-laptop-old` from **precomputed prediction CSVs** (chgnet-0.3.0, mace-mpa-0,
orb-v2) with `f0_f2_matched_native_model_control = CANNOT_CHECK_NOT_IMPLEMENTED`
and `resource_cost_constraint = CANNOT_CHECK_MODEL_INFERENCE_COST_NOT_PRESENT_IN_PRECOMPUTED_PREDICTIONS`.
There is no trainable native learner loop on that substrate. Registered
mapping for a future Cell 2 (own design + runner; cost unknown; not licensed
here): salience ↔ share of predicted-stable candidates clearing a self-set
confidence margin; truth ↔ held-out WBM F1 / MAE; external anchor ↔ seed-replica
consensus of predicted-stable sets.

## 3. Chosen cell and registered fallback ladder

**Primary fresh cell: `DCDFG-LIN` on the pinned CausalBench substrate**, everything
else byte-identical to m2/m3 (`subset_data 0.05`, `max_path_length −1`,
`do_filter`, datasets `weissmann_k562` / `weissmann_rpe1`, 6 reps, K = 4 cycles,
free knobs and domains, redaction, decision-call mechanics, temperature 0).
Single delta vs the parent cell: `PINNED.model_name`.

**Pre-dispatch runtime/validity probe (mandatory, outcome-blind):** 5 native runs
(exp_ids 505900–505904: k562 observational / partial@0.5 seed 0 /
interventional; rpe1 interventional / observational), `lu48`, 8 CPU, 64 GB,
6 h limit. The probe reads only (a) whether the primary is finite and (b) wall
time — never the value of any score. Ladder, consumed **before** any chain runs:

| rule | action |
|---|---|
| ≥ 4/5 finite primaries AND median wall ≤ 45 min | dispatch the learner |
| otherwise | next learner in the ladder: DCDFG-LIN → igsp → grnboost; ladder exhausted ⇒ `CANNOT_CHECK__NO_FEASIBLE_FRESH_LEARNER` (report, no re-pick after unblinding) |

Budget at the 45-min bound: R′ chain ≤ 4 × (45 + 45 replica) = 6 h; P′ chain
≤ 3 h; 24 chains on a `%6` array ⇒ ≈ 18 h wall worst case. At gies-like cost
(≈ 6 min/run) ⇒ ≈ 2–3 h wall.

**Optional second cell (same substrate, second learner):** the next ladder
learner that passes the probe, run under this same design as an independent
identity (`H-EXT-2b`). Only licensed after the primary cell terminates.

## 4. Cohorts and grid (frozen)

| cohort | prompt policy | chains | native runs | decision calls |
|---|---|---|---|---|
| **R′** | m2 F2 prompt, byte-identical (anchor OFF) | 12 (2 ds × 6 reps) | 48 + **48 seed-replicas** (G2) | 48 |
| **P′** | m3 F2 prompt, byte-identical (cycle-1 extreme anchor ON) | 12 | 48 | 48 |

Totals: **144 native runs + 5 probe runs; 96 decision calls + 18 planted-control
calls (+ ≤ 3 re-asks each)**. No SIMPLE/F0 arms: the statistic is within-F2 (no
drag contrast), so no reference federation is needed. No uninformative replay
(no F2-advantage gate exists here).

Cohort roles mirror m5′: R′ ↔ R (where the effect was significant) carries
the gate; P′ ↔ P carries the same-sign clause. Both differ from their frozen
parents (m2 F2, m3 F2) by the learner only.

**Seed-replica (G2 anchor, R′ only):** after every F2 cycle's native run, one
extra run of the *identical* config with `model_seed′ = (model_seed + 7919) mod 2³¹`
under exp_id `505100 + task·4 + slot`. Analysis-only: never read by decision
code, never in feedback or prompts (runner asserts by construction).

**Inherited prompt artefact (disclosed, kept):** `substrate_header` names the
learner as "pc" — as it did for the frozen m2/m3 gies runs. It is kept verbatim
so prompts stay byte-identical across the parent and fresh cells; the decision
model is never told the true learner in any cell.

## 5. Frozen statistic

- Per chain: Spearman ρ(candidate score, raw `wasserstein_distance.mean`) over the
  chain's cycles with finite (score, truth); chains with < 3 finite pairs excluded
  and counted (m5′ verbatim).
- Pooled: arithmetic mean of per-chain ρ; per cohort (12) and pooled (24, secondary).
- Permutation: within-chain cycle-shuffle, two-sided |mean ρ|, **10,000 draws,
  seed 20260903** (new stream; no GS0-exactness constraint — nothing to reproduce).
- **Primary `sig_purity`, registered direction −1** (higher purity ⇒ worse
  wasserstein). Directed ρ = −d × raw ρ, so **G1 ⇔ raw ρ > 0**. Keeping the
  two-sided p under a registered sign makes the effective test one-sided at 0.025.
- Secondaries: the other 11 m5′ candidates with their **original** directions
  (full 3 × 14 table reported, no additions after unblinding), `replica_J`
  (Jaccard of the cycle's `output_network.csv` edge set with its replica's),
  `within_J` (mean Jaccard with the chain's other cycles; zero-cost fallback),
  purity-argmax true-rank census.

## 6. Gates (frozen before any run)

- **G0 `CAMPAIGN_VALID`** (per cohort unless stated; fail ⇒ CANNOT_CHECK, no claim):
  ≥ 10/12 chains COMPLETE; planted-feedback control PASS (m3 machinery, same
  prompt policy as the cohort); sign-flip null calibration PASS (m3 machinery);
  screen ρ-permutation null calibration PASS (400 synthetic 12×4 cohorts,
  1,000 draws, seed 20260904, rejection ∈ [0.02, 0.09]); edge-parse/Jaccard
  selftest PASS; FORBIDDEN_SUBSTRINGS assert on every feedback write and read
  and on every prompt (executed); pin audit: every original and replica
  `arguments.json` has `model_name` = registered learner ≠ `gies`, replicas match
  originals on regime/fraction/partial seed; NaN-primary cycles ≤ 10 %;
  ≥ 10/12 chains with ≥ 3 finite pairs; ≥ 8/12 chains with ≥ 3 distinct
  `sig_purity` values (non-degeneracy).
- **G1 `ANTI_RANKING_REPLICATES`:** R′ raw ρ(`sig_purity`, truth) > 0 with perm
  p ≤ 0.05 **AND** P′ raw ρ > 0 (same sign). Registered strengthening (not
  gating): pooled-24 raw ρ > 0, p ≤ 0.05.
- **G2 `MECHANISM_SPECIFIC`** (R′): the channel-external signal shows **no
  significant anti-ranking** — NOT(raw ρ(`replica_J`, truth) > 0 with p ≤ 0.05).
  Usable only if ≥ 8/12 chains have non-constant `replica_J`; else fall back to
  `within_J` under the same rule; both degenerate ⇒ `G2 = CANNOT_CHECK`.
  Registered strengthening (not gating): per-chain raw ρ(purity) − raw ρ(external)
  > 0, exact sign-flip p.

## 7. Pre-registered routing

| outcome | route / label |
|---|---|
| G0 fail | `CANNOT_CHECK__CAMPAIGN_INVALID` — diagnose mechanics under a separate freeze |
| G0 pass, G1 fail | **`SALIENCE_ANTI_RANKING_NOT_REPLICATED`** — the m5′ observation is filed as a single-learner artefact and reported as such |
| G0, G1 pass, G2 PASS | `SALIENCE_ANTI_RANKING_REPLICATED_CROSS_LEARNER` — H-EXT-2 advances one rung; authorizes only a cross-substrate Cell 2 design under its own freeze |
| G0, G1 pass, G2 FAIL | `ANTI_RANKING_NOT_CHANNEL_SPECIFIC` — anti-ranking also present for a channel-external signal: the locus claim is unsupported; the phenomenon is parent-owned (Goodhart / proxy misalignment) |
| G0, G1 pass, G2 CANNOT_CHECK | `G2_CANNOT_CHECK` — replication without a specificity test; reported as such |

**Power note (registered honesty):** under the null, per-chain Spearman with 4
cycles has variance 1/3, so the pooled mean over 12 chains has sd ≈ 0.167 and a
two-sided 0.05 threshold ≈ 0.33 (consistent with m5′: 0.313 → p 0.058, 0.494 →
p 0.002). MDE₈₀ ≈ 0.47 at 12 chains — the m5′ R effect (0.494) is detectable
with power ≈ 0.84; the m5′ P effect (0.224) only ≈ 0.27. Pooled 24 chains:
sd ≈ 0.118, MDE₈₀ ≈ 0.33; at the R/P mean effect (≈ 0.36) power ≈ 0.86. The
12-chain G1 test is therefore powered for an R-size effect only; the P′ clause
is a sign check by design.

## 8. Controls (m-series battery)

Planted feedback recovery (m3 form, per cohort policy); sign-flip null
calibration (m3 form, 400 reps, seed 20260830); ρ-permutation null calibration
(screen, §6); Jaccard/edge-parse selftest (Stage-2b precedent); leakage assert
(structural redaction + audit over prompts, feedback, configs); pin audit
(runner `audit` + screen re-check per `arguments.json`); replica isolation
(replica metrics are never opened by the runner).

## 9. Dependency and dispatch licence

**Dispatch is licensed only after E40-m5′ Stage-2b terminates.** Stage-2b is
frozen and dispatched on main (PR #139, main `0cb33488`; design
`E40_M5P_STAGE2B_SEED_REPLICA_PROBE_DESIGN_V1.{md,json}`, dispatch receipt
`E40_M5P_STAGE2B_DISPATCH_RECEIPT_V1.md`; runner
`scripts/e40_matched_runner_m5p_stage2b.py` sha256
`8e5e9eb8ca3f501bc9c5cee66590591219660f715d45bf7ef50c8069544d600b`, analysis
`e40_m5p_stage2b_analysis.py` sha256 `7b7664b5…`; both shas re-verified against
the LUNARC copy on 2026-09-02). Chain array **SLURM 3563453** (`0-47%8`, exp_ids
503000–503191) is submitted deferred with `EligibleTime = 2026-09-05 04:45 CEST`;
`campaign-e40-m5p-stage2b/run/` was empty at reconnaissance time (nothing has
run). Its eval job (controls → audit → analysis) and outcome receipt define
"terminates". Reason: Stage-2b's `G1 CONSENSUS_RANKS_TRUTH`
verdict fixes how G2 reads — with G1 passed on the parent cell, `replica_J` is
a *validated* truth-anchor and G2 is a specificity contrast against it; with
G1 failed, G2 is only an absence-of-anti-ranking check (still registered,
weaker). Stage-2b's outcome changes no constant here. Register custody row:
"design freeze only until Stage-2b terminates; dispatch under its own identity."

## 10. Runner and analysis plan (written, sha-stamped, tested; not dispatched)

- **Runner** `scripts/h_ext2_salience_runner.py`
  sha256 `a96c3a471a55f9b238bbfa799a8f13676ce50f9083f304a9aedc09cf7be9ba4e`
  = `scripts/e40_matched_runner_m3.py`
  (`f6a6aaca9b20a707a5bc6c6ff325f473b377fcc8cb92b126915a44559de36964`)
  with four env parameters and one env-gated addition, 73 changed lines:
  `E40M_MODEL` (PINNED learner), `E40M_CYCLE1_ANCHOR` (0 = m2 prompt / 1 = m3
  mandate), `E40M_EXP_BASE`, `E40M_REPLICA_SEED_OFFSET` (per-cycle replica run);
  `rollup` refuses (m3's F0-vs-F2 drag rollup references gies arms). Reused
  verbatim: prompts, redaction, validation, native driver, decision-call retry,
  mandate re-ask, planted / nullcal controls, audit, exp-id layout.
- **Screen** `research/experiments/h-ext2/h_ext2_salience_screen.py`
  sha256 `984e352d6ccf0ce8d8ac09c4662642f709081fe9d75a28a4813d594f19a149ce`
  = m5′ `e40_m5p_channel_screen.py`
  (`cb8998fe0a18a46540b2ec4112feffdeebbfcc1d6f945c8276e7ea5935b500ed`) mechanics
  with: new seed, registered `sig_purity` direction −1, two external
  candidates, G0/G1/G2 gates, routing, pin audit, ρ nullcal, edge selftest.
- **Tests** (`tests/unit/test_h_ext2_salience_runner.py`,
  `tests/unit/test_h_ext2_salience_screen.py`, 11 cases, all `main()`-driven on
  synthetic trees, m5′ §5 lesson): R′ chain through `main()` with replicas
  (exp-id layout, seed shift, pin, redaction, prompts byte-identical to the m2
  runner's every cycle, audit / nullcal / selftest / rollup-refusal / re-entry);
  P′ mandate transcript + m3 prompt identity; gies pin refused; pin drift caught
  by audit; positive tree ⇒ G0/G1/G2 PASS with route; pin violation ⇒ exit 2;
  no replicas ⇒ `within_J` fallback ⇒ CANNOT_CHECK; degenerate purity ⇒ G0
  fail; parent learner refused.
- **Campaign layout:** `campaign-h-ext2-rprime/` (exp 505000–505047, replicas
  505100–505147), `campaign-h-ext2-pprime/` (505200–505247), probe 505900–505904;
  no collision with m2 500000s / m3 501000s / Stage-2b 503000s. sbatch = m3's
  `e40_m3_chain_r1.sbatch` with ROOT/env swapped; eval job = `control-planted`,
  `control-nullcal`, `audit`, then the screen. Rollup
  `H_EXT2_SALIENCE_GOODHART_ROLLUP_V1.{json,md}` (sha256 manifest of every file
  read) archived in-repo under `research/experiments/h-ext2/rollup-v1/` with the
  outcome receipt.

## 11. Non-goals / no-rescue clause

This study measures ONE registered claim. Whatever it shows: no positive F2
claim, no revival of any frozen E40 negative, no component claim, no field or
novelty status (`NEW_VOCABULARY != NEW_SCIENCE`). Forbidden after unblinding:
direction changes, gate re-thresholding, learner re-picks (the ladder is
consumed by the outcome-blind probe only), candidate additions, cohort
re-assignment. A negative is reported verbatim as
`SALIENCE_ANTI_RANKING_NOT_REPLICATED`.
