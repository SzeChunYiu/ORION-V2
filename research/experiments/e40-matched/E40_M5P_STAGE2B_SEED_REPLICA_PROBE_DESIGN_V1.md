# E40-m5′ Stage-2b — Seed-Replica Stability-Probe Design V1 (frozen before any run)

**Lineage:** m5′ Stage-1 outcome receipt (PR #135) routed here on GS1-fail:
"no visible composite ranks truth even in-sample → same Stage-2b route;
strengthens the terminal reading if Stage-2b also fails."
**Class:** prospective native campaign (new runs), single-delta revival of the
E40 metabolic-drag negative; freeze precedes run (m-series discipline).

## 1. Question and mechanism hypothesis

m2–m5′ attributed the F2 metabolic drag to the **information content of the
cycle-visible feedback channel**: search is fine (m3 — oracle-matching cycles
exist), no computable rule over the channel recovers them (m4), no composite
of the 8 visible fields ranks truth (m5′ GS1), and the channel's one stable
internal signal (significance purity) **anti-ranks** truth (m5′ §2).

The one information source not yet tested that (a) does not modify the pinned
substrate, (b) does not come from the misleading feedback channel, and (c)
requires no oracle: **self-consistency across independent seed-replicas of the
loop itself**. Hypothesis: cycles where independent replicas of the same cell
converge on the same output graph are tracking substrate-determined structure
(replicable signal), while divergent cycles are riding seed noise; replica
edge-set agreement is therefore a candidate **truth-anchor** the loop does not
already possess. This is the last named lever in the m4/m5′ routing; if its
gate fails, the E40 line is terminal.

## 2. Frozen inputs and campaign grid

- Substrate: pinned CausalBench, model `gies`, datasets
  `weissmann_k562` / `weissmann_rpe1`, `subset_data=0.05`, `do_filter`,
  `max_path_length=-1` — byte-identical to m2/m3 (no substrate modification).
- Cells: 2 datasets × 6 reps = **12 cells** (same grid as m2/m3).
- Replicas: **K = 4** independent F2 chains per cell (`f2r0`..`f2r3`),
  4 cycles each → **192 native runs** (+192 model decision calls, temp 0).
- F0 reference: frozen m2 F0 chains, **read-only reuse** (m3 precedent; the
  contrast stays single-delta: many-seed F2 vs frozen F0 federation).

### 2.1 Replica delta (the ONLY prompt difference from m2 F2)

Cycle 1 of replica k mandates the seed knobs to frozen values; all other knobs
stay model-orchestrated exactly as in m2; cycles 2–4 prompts byte-identical to
m2 F2 given the replica's own history:

| replica | model_seed | partial_intervention_seed |
|---|---|---|
| f2r0 | 11 | 13 |
| f2r1 | 29 | 31 |
| f2r2 | 47 | 53 |
| f2r3 | 71 | 79 |

Mandate handling per m3 conventions: ≤3 parse/validate re-asks; a cycle-1
decision that does not carry exactly the replica's mandated seeds is a
CANNOT_CHECK chain (excluded, counted, reported — never silently repaired).

## 3. Probe statistic (truth-anchor candidate)

Per cell, per cycle c: **consensus**
`J_c = mean_{k<l} |E_k(c) ∩ E_l(c)| / |E_k(c) ∪ E_l(c)|`
where `E_k(c)` = edge set of replica k's `output_network.csv` at cycle c
(417-ish edges each; J ∈ [0,1]). Computable from replica outputs alone; truth
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
(12 primary diffs; negative = F0 better — m4 CT1 convention). Per-replica
(48-diff) version reported secondary (within-cell correlation noted).

## 5. Gates (frozen before computing)

Statistics: pooled arithmetic mean of per-cell Spearman ρ (J_c vs T_c over 4
cycles); within-cell cycle-shuffle two-sided permutation, 10,000 draws, seed
**20260902** (new stream; no GS0-exactness constraint applies — there is no
prior rollup to reproduce); paired sign-flip permutation for contrasts
(m-series convention, exhaustive 2^12).

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

## 6. Pre-registered routing

| Outcome | Route |
|---|---|
| G1 ∧ G2 ∧ G3 ∧ G4 (G0 passed) | authorize **m6 prospective confirm campaign** under its own freeze (consensus in prompt+feedback; m-series gates) — no revival claim issues from Stage-2b alone |
| G0 passed, any of G1–G4 fails | **E40 line TERMINAL**: the deficit is attributable to the information available to the loop by any channel tested (external knowledge, visible composites, replica self-consistency); further revival needs a new mechanism class |
| G0 failed | CANNOT_CHECK disposition; diagnose campaign mechanics before any re-dispatch (separate freeze) |

## 7. Controls (m-series battery, verbatim where inherited)

- **Planted control** (m2/m3 form): known-config planted signal must pass.
- **Null calibration** (m2/m3 form, 400 reps, seed 20260830): random-config
  pass rate < 1%.
- **Leakage re-check:** FORBIDDEN_SUBSTRINGS assert on every feedback write
  and read (executed, not logged).
- **Jaccard selftest:** J(E,E)=1; J(E, shuffled-E) small; edge-parse round-trip
  on a fixture csv (added because Stage-2b adds the edge-parsing path).
- **Power note (registered honesty):** 12-cell primary contrasts detect
  |mean_d| ≳ 2·sd/√12; m2/m3 drag sd implies MDE ≈ 0.003–0.004 wasserstein vs
  the ≈0.007–0.011 drag — adequately powered for the drag-size effect, not
  for sub-half-drag effects; G4 is a sign check by design.

## 8. Custody

- Runner `e40_matched_runner_m5p_stage2b.py`, sha256 frozen in the PR carrying
  this design; campaign dir `campaign-e40-m5p-stage2b/`; exp_ids **503000+**
  (own results root; no collision with m2 500000s / m3 501000s).
- Every input file read (m2 F0 exp_ids + metrics; 192×{arguments, metrics,
  output_network.csv}; all feedback files) sha256-manifested in the rollup.
- Decision calls logged (prompt sha, raw response, call-log, model id, temp 0).
- Deterministic analysis: only RNGs are the frozen-seed shuffles above.
- Output `E40_M5P_STAGE2B_ROLLUP_V1.{json,md}` under the campaign rollup dir,
  archived in-repo under `rollup-m5p-stage2b/` with the outcome receipt.

## 9. Non-goals / no-rescue clause

This probe measures ONE hypothesis: replica self-consistency as a
truth-anchor. Whatever it shows: no positive F2 claim, no component claim, no
revival of any frozen negative. A full pass authorizes only the m6
prospective campaign; a fail on G1–G4 with G0 passed **terminates the E40
line**. Purity inversion, seed-table re-picks, gate re-thresholding after
unblinding are all outcome tuning and forbidden.
