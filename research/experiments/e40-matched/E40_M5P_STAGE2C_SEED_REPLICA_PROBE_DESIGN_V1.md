# E40-m5′ Stage-2c — Seed-Replica Stability-Probe Design V1 (frozen before any run)

**Supersedes:** `E40_M5P_STAGE2B_SEED_REPLICA_PROBE_DESIGN_V1` (frozen in PR #139,
merged main `0cb33488`, **never run** — 0 chains, 0 native runs, 0 outcome data).
**Cause of the re-freeze:** the model channel began serving a different model than
the one the frozen m2 F0 reference chains were produced under (§2.2 evidence), so
Stage-2b's read-only F0 reuse would have added an unregistered second delta.
**Lineage:** m5′ Stage-1 outcome receipt (PR #135), GS1-fail route.
**Class:** prospective native campaign (new runs), single-delta revival of the
E40 metabolic-drag negative; freeze precedes run (m-series discipline).

Nothing outcome-facing changes: the question, probe statistic, seed table, gates,
thresholds, permutation seeds, routing and no-rescue clause are Stage-2b V1
verbatim. The changes are the reference arm's provenance and a substrate pin
(§2.2, §2.3), decided with no campaign data in existence.

## 1. Question and mechanism hypothesis

Unchanged from Stage-2b V1. m2–m5′ attributed the F2 metabolic drag to the
**information content of the cycle-visible feedback channel**: search is fine
(m3), no computable rule over the channel recovers the good cycles (m4), no
composite of the 8 visible fields ranks truth (m5′ GS1), and the channel's one
stable internal signal (significance purity) **anti-ranks** truth (m5′ §2).

The one untested information source that (a) does not modify the pinned
substrate, (b) does not come from the misleading feedback channel, and (c)
requires no oracle: **self-consistency across independent seed-replicas of the
loop itself**. Hypothesis: cycles where independent replicas of the same cell
converge on the same output graph are tracking substrate-determined structure,
while divergent cycles ride seed noise; replica edge-set agreement is therefore
a candidate **truth-anchor** the loop does not already possess. This is the last
named lever in the m4/m5′ routing; if its gate fails, the E40 line is terminal.

## 2. Frozen inputs and campaign grid

- Substrate: pinned CausalBench, model `gies`, datasets
  `weissmann_k562` / `weissmann_rpe1`, `subset_data=0.05`, `do_filter`,
  `max_path_length=-1` — byte-identical to m2/m3 (no substrate modification).
- Cells: 2 datasets × 6 reps = **12 cells** (same grid as m2/m3).
- Replicas: **K = 4** independent F2 chains per cell (`f2r0`..`f2r3`),
  4 cycles each → **192 native runs** (+192 model decision calls, temp 0).
- **F0 reference: re-run IN-CAMPAIGN** — 12 federation chains × 4 upfront
  configs → **48 native runs** (+12 decision calls). Prompt byte-identical to
  the m2/m3 `f0_prompt`; no feedback; K configs committed upfront.
- Total: **60 chains, 240 native runs**, exp_ids **504000–504239**
  (F2 504000–504191, F0 504192–504239).
- `SIMPLE_DIRECT_CONTROL` is not run: no Stage-2c gate consumes it.

### 2.1 Replica delta (the ONLY prompt difference from the frozen m2 F2 arm)

Unchanged from Stage-2b V1. Cycle 1 of replica k mandates the seed knobs to
frozen values; all other knobs stay model-orchestrated exactly as in m2; cycles
2–4 prompts byte-identical to m2 F2 given the replica's own history:

| replica | model_seed | partial_intervention_seed |
|---|---|---|
| f2r0 | 11 | 13 |
| f2r1 | 29 | 31 |
| f2r2 | 47 | 53 |
| f2r3 | 71 | 79 |

Mandate handling per m3 conventions: ≤3 parse/validate re-asks; a cycle-1
decision that does not carry exactly the replica's mandated seeds is a
CANNOT_CHECK chain (excluded, counted, reported — never silently repaired).

### 2.2 Model-channel finding and the served-model pin (new)

Probed from LUNARC on 2026-09-02 (verbatim evidence in the Stage-2c dispatch
receipt): the E60-lane endpoint answers HTTP 200 but **silently substitutes the
model**. Requesting `glm-5.2` (the value frozen in `~/.orion-campaign.env`, last
modified 2026-08-24, i.e. the value in force when m2/m3 ran on 2026-08-30) is
served `glm-5.3`; `glm-5.1` is also served `glm-5.3`; `glm-4.6` is served
`glm-5.3-flash`. No response field warns of the substitution. m2/m3 logged only
prompt/response hashes and token counts — a search of all 1,810 files under
`campaign-e40-m2` / `campaign-e40-m3` and the campaign logs finds **no served
model id anywhere**, so the reference model is **unrecoverable** and no provider
tested serves it.

Consequences, decided before any run:

1. **The F0 arm is re-run in-campaign** so both arms are produced by one model;
   this restores the single delta (§2.1) that the whole probe rests on.
2. **The pinned quantity is the SERVED id, not the requested one:**
   `SERVED_MODEL = "glm-5.3"`. Every model response must report exactly this id;
   any other value raises `ChainCannotCheck` (chain recorded, excluded, counted,
   reported). The analysis re-checks every used chain's logged call ids and marks
   any chain with a foreign id — or with **no** served-model record at all —
   CANNOT_CHECK. Silent substitution therefore fails closed at both ends.
3. The frozen m2 F0 chains are retained as a **historical, cross-model,
   explicitly non-gating panel** (§4.1) for continuity with m2/m3/m4/m5′.

### 2.3 Custody deltas vs Stage-2b V1 (complete list)

| # | Delta | Reason |
|---|---|---|
| D1 | F0 federation re-run in-campaign; m2 F0 becomes a non-gating panel | restores the single delta under one served model |
| D2 | `SERVED_MODEL` pin asserted on every call (runner) and every used chain (analysis) | the endpoint substitutes models silently |
| D3 | campaign dir `campaign-e40-m5p-stage2c`, exp_ids 504000–504239, 60 chains | own identity; Stage-2b's 503000 block retired unused |

Unchanged: probe statistic, contrasts, seed table, gates and thresholds,
permutation seeds/draws, routing, controls, leakage rule, substrate pins,
K_CYCLES, cell grid, call/retry mechanics, temperature 0.

## 3. Probe statistic (truth-anchor candidate)

Per cell, per cycle c: **consensus**
`J_c = mean_{k<l} |E_k(c) ∩ E_l(c)| / |E_k(c) ∪ E_l(c)|`
where `E_k(c)` = edge set of replica k's `output_network.csv` at cycle c
(≈417 edges each; J ∈ [0,1]). Computable from replica outputs alone; truth
(raw `wasserstein_distance.mean`) never enters it, the prompts, or the
feedback. Cycle-level truth anchor per cell:
`T_c = mean_k wasserstein_k(c)` (replica-mean, analysis-side only).

## 4. Shipping counterfactuals (re-analysis of the same 192 runs)

| rule | shipped cycle per replica | role |
|---|---|---|
| TERMINAL | cycle 4 | baseline (must reproduce the drag) |
| CONSENSUS-ARGMAX | argmax_c J_c (cell-level index, earliest tie) | **the probe** |
| PURITY-ARGMAX | argmax_c sig_purity (per m5′ §2 definition, replica-local) | registered anti-control (expected to anti-select) |
| ORACLE-BEST | argmin_c wasserstein_k(c) (replica-local) | ceiling reference only; no claim |

Contrast per cell: `d = f0_best_primary − mean_k shipped_truth_k`
(12 primary diffs; negative = F0 better — m4 CT1 convention), where
`f0_best_primary` is the **in-campaign** F0 best-of-4 by true score. Per-replica
(48-diff) version reported secondary (within-cell correlation noted).

### 4.1 Historical m2-F0 panel (non-gating)

Every contrast is additionally computed against the frozen m2 F0 bests and
reported under `historical_m2_f0_panel_nongating`, labelled as a cross-model
comparison. It informs continuity discussion only: **no gate, route, or claim
may cite it**.

## 5. Gates (frozen before computing; Stage-2b V1 verbatim)

Statistics: pooled arithmetic mean of per-cell Spearman ρ (J_c vs T_c over 4
cycles); within-cell cycle-shuffle two-sided permutation, 10,000 draws, seed
**20260902**; paired sign-flip permutation for contrasts (m-series convention,
exhaustive 2^12, one-sided P(T_perm ≥ T_obs), positive = F2 better).

- **G0 `DRAG_PRESENT_UNDER_TERMINAL` (validity):** TERMINAL contrast pooled
  mean_d < 0 AND f0_wins ≥ 8/12. Fail → campaign off-course (disposition
  CANNOT_CHECK-class; no science claim either way).
- **G1 `CONSENSUS_RANKS_TRUTH` (probe validity, pooled 12 cells):** directed
  pooled ρ = −rawρ > 0 with perm p ≤ 0.05.
- **G2 `CONSENSUS_SHIPPING_CLOSES_DRAG` (decision, pooled 12 cells):**
  CONSENSUS contrast mean_d ≥ −0.001 AND perm p ≤ 0.10.
- **G3 `ANTI_CONTROL_DISTINGUISHES` (specificity):** PURITY contrast does NOT
  close the drag (mean_d < −0.001 OR perm p > 0.10).
- **G4 `SPLIT_CONSISTENT` (out-of-sample sign check):** within EACH dataset
  stratum (6 cells), CONSENSUS mean_d > TERMINAL mean_d.

## 6. Pre-registered routing (Stage-2b V1 verbatim)

| Outcome | Route |
|---|---|
| G1 ∧ G2 ∧ G3 ∧ G4 (G0 passed) | authorize **m6 prospective confirm campaign** under its own freeze — no revival claim issues from Stage-2c alone |
| G0 passed, any of G1–G4 fails | **E40 line TERMINAL**: the deficit is attributable to the information available to the loop by any channel tested (external knowledge, visible composites, replica self-consistency); further revival needs a new mechanism class |
| G0 failed | CANNOT_CHECK disposition; diagnose campaign mechanics before any re-dispatch (separate freeze) |

## 7. Controls (m-series battery, verbatim where inherited)

- **Planted control** (m2/m3 form, plant v4): known-config planted signal must pass.
- **Null calibration** (m2/m3 form, 400 reps, seed 20260830): rejection in
  [0.02, 0.09]; and a null gate-chain pass rate < 1%.
- **Leakage re-check:** FORBIDDEN_SUBSTRINGS assert on every feedback write, every
  feedback read and every outgoing prompt (executed, not logged).
- **Jaccard selftest:** J(E,E)=1; J(E, shuffled-E) small; edge-parse round-trip
  on a fixture csv.
- **Served-model control (new):** a fixture campaign whose artifacts carry a
  substituted id must make every chain CANNOT_CHECK and the disposition
  CANNOT_CHECK; a chain with no served-model record must be CANNOT_CHECK.
- **Power note (registered honesty):** 12-cell primary contrasts detect
  |mean_d| ≳ 2·sd/√12; m2/m3 drag sd implies MDE ≈ 0.003–0.004 wasserstein vs
  the ≈0.007–0.011 drag — adequately powered for the drag-size effect, not
  for sub-half-drag effects; G4 is a sign check by design.

## 8. Custody

- Runner `e40_matched_runner_m5p_stage2c.py`, analysis
  `e40_m5p_stage2c_analysis.py`, sha256 frozen in the PR carrying this design;
  campaign dir `campaign-e40-m5p-stage2c/`; exp_ids **504000–504239**.
- Every input file read (60 chains × {decision logs, feedback, exp_ids};
  240 × {arguments, metrics, output_network.csv}; the historical m2 F0 files)
  sha256-manifested in the rollup.
- Decision calls logged (prompt sha, raw response, call-log, **served model id**,
  temperature 0).
- Deterministic analysis: only RNGs are the frozen-seed shuffles above; all sums
  via `math.fsum` so results are interpreter-independent.
- Output `E40_M5P_STAGE2C_ROLLUP_V1.{json,md}` under the campaign rollup dir,
  archived in-repo under `rollup-m5p-stage2c/` with the outcome receipt.

## 9. Non-goals / no-rescue clause (Stage-2b V1 verbatim)

This probe measures ONE hypothesis: replica self-consistency as a truth-anchor.
Whatever it shows: no positive F2 claim, no component claim, no revival of any
frozen negative. A full pass authorizes only the m6 prospective campaign; a fail
on G1–G4 with G0 passed **terminates the E40 line**. Purity inversion, seed-table
re-picks, gate re-thresholding after unblinding are all outcome tuning and
forbidden. The §2.2 re-freeze is authorized only because it happened with zero
campaign data in existence; no comparable change may be made after any run.
