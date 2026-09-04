# E40-m5′ Stage-2e — Replica-Overlap Precondition Probe: outcome receipt (V1)

**Disposition: `E40_PROBE_PRECONDITION_UNMET__REPLICAS_DISJOINT`** — all four registered
controls PASS, all 34 envelopes COMPLETE and homogeneous, P0 true, **P1 false**, P2 false.

**Design:** `E40_M5P_STAGE2E_OVERLAP_PRECONDITION_DESIGN_V1.{md,json}` (PR #253, freeze commit
`b5498bd`), md sha256 `23d8726fd32ef1d8eb439331f9220d7b9d5cbcf20e3398b6e2cec29d16cc031a`,
json sha256 `fa13bb1a8bb11f44a105822a42632714a369aa200d691dc5d8b5b59fd65f77d6`.
**Script:** `e40_m5p_stage2e_overlap_precondition.py` — run array under freeze sha256
`f3ac7d783e765a0ca28949e9dca65f563a1a0ed79302658722adfce22432a41f`; analysis under
`93cef0c8cedbbeb50f69e108db54ba5c0dd3925a61eadfd8c33a549d52df0df8` (amendment R1, §4; node sha
verified equal to the committed file before submission).
**Runs:** SLURM array **3569295** (34/34 COMPLETED, 0 error logs, ~140 s each); eval SLURM
**3573344** (COMPLETED, 18 s: selftest on synthetic fixtures under rebound roots, then the analysis
**exactly once** on the real campaign). Interpreter: campaign venv Python 3.11.5.
**Rollup:** `rollup-m5p-stage2e/E40_M5P_STAGE2E_ROLLUP_V1.json`, sha256
`7d24d01b3d331c9d1c75d9ac85c7d7366b2ad5481dd8826be5530f094fa5e639`, byte-identical to the LUNARC
original; 102-file sha256 manifest; `model_calls: 0`.
**Authorization:** operator, in chat, 2026-09-02, *"run all the computation tasks.. finish all the
researxh asap"*, reaffirmed 2026-09-03 *"you will fix everything"*; dispatched by the E40 closure
lane under that standing instruction after the design was frozen and pushed (PR #253). Archived
here after use.

## 1. Result

| quantity | weissmann_k562 | weissmann_rpe1 | pooled |
|---|---|---|---|
| **seed-only J** (same config, 4 seeds; one value per config) | 0.0150, 0.0113, 0.0144, 0.0210 | 0.0505, 0.0363, 0.0468, 0.0456 | **0.0301** |
| config-only J (same seed, 4 configs; one value per seed) | 0.0106, 0.0151, 0.0119, 0.0136 | 0.0370, 0.0405, 0.0452, 0.0390 | 0.0266 |
| **determinism repeat J** (identical run, own exp_id) | **1.0** | **1.0** | — |

P2 stratified exhaustive permutation (4,900 relabellings, no RNG): t_obs +0.00348, one-sided
p **0.0553** — not below 0.05, so P2 is false as registered; it is reported, not interpreted, since
P1 already voids the premise.

## 2. Reading (the precondition is unmet, and the mechanism is now visible)

- **The substrate is fully deterministic given a seed.** The (c0, s0) repeat reproduces its edge
  set exactly in both datasets — the pipeline demonstrably returns J = 1.0 when two runs are the
  same run, so a J of 0.03 is a substrate fact, not a parser artefact.
- **Changing only the seed pair, config held fixed, destroys 97–98 % of the edge set.** Under
  `subset_data = 0.05` the seed selects the 5 % cell subsample, and at that subsample the inferred
  graph is dominated by sampling variation. This is the most favourable condition replica
  consensus could be given, and it has no dynamic range.
- **Config variation adds nothing beyond the seed floor** (0.030 vs 0.027). The five knobs the
  metabolic loop tunes move the output graph *less* than the seed does.
- **Stage-2c's J band (0.0093–0.0520, mean 0.0282) is this seed-noise floor** — its per-config
  values here span 0.011–0.051. Stage-2c's descriptive §4 reading ("degenerate statistic") is now
  established by direct measurement; it was not established by Stage-2c itself, whose replicas
  confounded seed with config (26/48 cell-cycles on four different configs).

## 3. What this closes, in the registered vocabulary

Stage-2c design §1: the seed-replica probe is *"the last named lever in the m4/m5′ routing; if its
gate fails, the E40 line is terminal."* Its gate G1 (`CONSENSUS_RANKS_TRUTH`) ranks J across four
cycles; when between-cycle differences in J are the size of the seed floor itself, G1 has nothing
to rank, **under any prompt form, mandate, or served model** — none of those touch the substrate.
So the probe is not testable on the pinned substrate, and a valid G0-pass / G1–G4 run — the single
artifact that could award the registered `E40_TERMINAL` — **cannot be produced here**.

This is a **precondition terminal**, and is filed as one. It is not `E40_TERMINAL` and must not be
merged into it. What would make the probe testable is a substrate change (a larger `subset_data`,
or a truth-anchor statistic that is not seed-dominated) — which Stage-2c design §6 already classes
as "a new mechanism class", i.e. outside the E40 line.

## 4. Amendment R1 to the checker, made before the analysis ran (disclosed)

The per-envelope homogeneity gate compared `training_regime` byte-for-byte and marked the first
real envelope INHOMOGENEOUS: upstream canonicalises the CLI value before recording it
(`interventional` → `Interventional`, `partial_interventional` → `PartialIntervational` [sic]).
The gate now compares by canonical form; a genuinely different regime still mismatches, and both
directions are unit-tested against the recorded upstream spellings. No gate, threshold, seed, grid
or routing constant changed; the amendment was committed (`da3d723`) and its sha verified on the
node before the eval was submitted. This is the gate doing its job on its first real input, which
is what it is for.

## 5. Custody

Campaign `campaign-e40-m5p-stage2e/` (LUNARC): `run/results/505000–505033/{arguments,metrics}.json`
+ `output_network.csv` + `slot.json`, `run/logs/native_*.log`, `run/rollup/`. Archived here:
the rollup json (sha above), `selftest_prerun.out` (node selftest before the run array),
`e40m5p2e-eval-3573344.out`. No design constant was changed after the freeze; the design files are
unmodified since `b5498bd`.
