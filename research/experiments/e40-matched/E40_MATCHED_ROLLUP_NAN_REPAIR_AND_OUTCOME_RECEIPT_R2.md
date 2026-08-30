# E40-matched rollup NaN-policy repair + campaign outcome — receipt R2 (2026-08-30)

**Campaign:** `campaign-e40-m1` (SLURM chain array 3554313, 36/36 COMPLETED, 0 failed;
eval array 3554362 terminal 2026-08-30; controls planted=PASS, nullcal=PASS,
uninformative=present — all recorded before this receipt).
**Repaired runner sha256:** `48ac88dc11ecf8b798bac7c3a2b144e1d94e32ebaf95ef58ea19f27e715f9e01`
(dispatched copy at `campaign-e40-m1/e40_matched_runner.py`; prior frozen-dispatch
sha256 `386fd194…` per dispatch receipt V1).

## 1. Defect (found at rollup, before any verdict was accepted)

The R1b rollup reported `mean_d = NaN`, `perm_p_exact = 0.0`, `wins 1/1` of 12 pairs —
an internally impossible combination (NaN contrast with a zero p-value). Census over the
108 frozen chain runs (separate static code path):

| Arm × regime | NaN primary / total |
|---|---|
| simple (pinned partial_interventional 0.5) | **12 / 12** |
| f0 interventional | 12 / 12 |
| f0 partial_interventional | 24 / 24 |
| f0 observational | **0 / 12** (0.1538–0.1839) |
| f2 interventional | 12 / 12 |
| f2 partial_interventional | 9 / 9 |
| f2 observational | **0 / 27** (0.1538–0.1856) |

Attribution is perfect and structural: every interventional-family run produces a NaN
primary (empty output-graph evaluation, `wasserstein_distance.mean = NaN` in the native
metrics); every observational run is real. Two checker-level consequences:

1. **`_best_by_primary` used Python `min()` with no NaN policy.** `x < NaN` is always
   False, so `min` keeps the first element; in the 4 F0 chains whose (only) real
   observational run sat **last** in the run list, "best" was a NaN run → `f0_best`
   NaN → `d = NaN` for 4/12 pairs → `mean_d = NaN` while wins/p were computed over the
   surviving pairs — the impossible rollup. (Session-level census over all 120 result
dirs including the 12 uninformative-blind finals counts 79 NaN; the chain-scope
number — the one the rollup aggregates — is 69/108.)
2. No distinction between "no defined primary" (a real substrate outcome: the config
   predicted nothing scoreable) and "checked".

## 2. Repair (checker-only; treatment surface untouched)

`scripts/e40_matched_runner.py` → `orion.v2.e40-matched.rollup.v2`:

- `_best_by_primary` now ranks NaN primaries **worst** — a run with no prediction is
  never "best" while a real-valued run exists; all-NaN ⇒ `None` ⇒ the pair is
  `CANNOT_CHECK__NO_DEFINED_PRIMARY` (counted, never fabricated as d=0).
- `f0_mean` over real-valued runs only, with explicit `f0_real_runs` count.
- New fields: `nan_policy`, per-pair `nan_counts`, arm-level
  `degenerate_run_accounting` (simple 12/12, f0 36/48, f2 21/48).
- Selftest: 4 new NaN-policy cases (NaN-prefix preference regression, interleaved NaN,
  all-NaN ⇒ None, NaN predicate), 0 failures locally and on LUNARC.

**Not changed:** any arm prompt, planted gate, gate criterion/threshold, native
invocation, or frozen chain artifact; no native run re-executed. The primary metric
(mean wasserstein of `quantitative_test_evaluation.output_graph`) is unchanged — the
repair defines how undefined values aggregate, which the R1b contract left implicit.

## 3. Validation against real data (before the rollup re-run)

Independent static recomputation (separate script, `/tmp/e40m1_static_validate.py`,
reads the 108 frozen chain runs directly — not via the runner) predicted post-repair:
12/12 valid pairs, mean_d = −0.000967, wins 2/3/7 (at 4-decimal rounding),
p = 0.8125 (rounded). The re-run rollup reproduced every unrounded quantity exactly
(mean_d = −0.0009676610…, degenerate counts 12/12, 36/48, 21/48). The remaining
counting difference (wins_f0 4 vs 3, p 0.625 vs 0.8125) is the static script's own
4-decimal rounding of a k562/rep1 pair with d = −3×10⁻⁷ (two different observational
configs with numerically indistinguishable primaries); the rollup counts the raw value.

## 4. Repaired outcome (frozen gate map applied verbatim)

```
gate            METABOLIC_DRAG_MATCHED_NATIVE
pairs           12/12 COMPLETE, 0 CANNOT_CHECK
mean_d          −0.000968   (F0_best − F2_final; negative ⇒ F2 slightly worse)
perm_p_exact    0.625       (sign-flip exact, 12 pairs)
wins            f2 2 / f0 4 / exact-config ties 6
controls        planted=PASS nullcal=PASS uninformative=present
```

Per-pair d: k562 ≈ 0 (6 pairs; five identical configs, one d=−3e−7), −0.0065;
rpe1 +0.0146, −0.0245, −0.0071, +0.0119, two exact ties.

**Reading (pre-declared contrast, no post-hoc re-scoping):** at 4× matched native
compute the full metabolic loop shows **no advantage over the upfront federation** —
the effect is mildly negative and statistically indistinguishable from zero
(p = 0.625). Two substrate facts carry the interpretation:

- **The decision space is regime-degenerate at subset 0.05.** Only observational
  configs produce a defined primary (69/108 chain runs NaN, all interventional-family);
  the SIMPLE control's pinned default (partial 0.5) is NaN on 12/12.
- **The loop rationally escapes the degenerate basin but lands where F0 already is.**
  Every F2 chain opened interventional (NaN → redacted feedback shows all-zero
  diagnostics), then moved to observational by cycle 2–4 in 12/12 chains using only
  redacted (held-out-blind) feedback. Its finals coincide with the F0 upfront
  observational config on ~half the pairs (deterministic same-config repeats); where
  they differ, F2 is net worse by ≤0.025.

So the drag is not an orchestration failure — it is the cost of re-deriving, at 4×
compute, a configuration the federation already contains, with no counterbalancing
discovery. The gate label per the frozen map is `METABOLIC_DRAG_MATCHED_NATIVE`.

## 5. Mechanism probe — outcome (SLURM 3554405, terminal 2026-08-30)

The NaN mechanism question — subset×regime interaction vs regime-intrinsic emptiness
— is now resolved. Probe (separate root `campaign-e40-m1-probe/`, exp_ids 510001–510004,
weissmann_k562, all other knobs at campaign pins):

| exp | regime | subset_data | primary | TP | FP |
|---|---|---|---|---|---|
| 510001 | interventional | 0.5 | NaN | 0 | 0 |
| 510002 | partial_interventional | 0.5 | NaN | 0 | 0 |
| 510003 | interventional | 1.0 (full data) | NaN | 0 | 0 |
| 510004 | partial_interventional | 1.0 (full data) | NaN | 0 | 0 |

**Regime-intrinsic, subset-independent.** Native logs show `Mean of empty slice.`
(numpy warning) in every interventional-family run, including full-data: the PC model
emits an **empty predicted graph** under interventional/partial-interventional
training, so the output-graph wasserstein evaluates over an empty edge set (NaN mean,
TP=FP=0). This also resolves the label-permutation control's AMBIGUOUS_EMPTY cells:
the emptiness is not a 5%-subsample artifact.

Implications (recorded, not acted on here):

- The E40-m1 contrast therefore tested **within-observational configuration
  exploration only** — the substrate cannot exercise the metabolic hypothesis's
  regime-exploration component at any subset. The null verdict (no F2 advantage,
  p=0.625) is about seed/knob exploration around one working basin.
- The SIMPLE control's pinned default (partial 0.5) was structurally unable to score
  — an E40 R1 default defect on this substrate, not an arm behaviour.
- Any revival must first repair the native interventional path (why PC returns an
  empty graph under interventional regimes — a causalscbench pipeline question) or
  change substrate. Pre-registering a NaN-robust composite endpoint would only mask
  a broken cell; that is not a valid revival lever.

## 6. Chain of custody

- Frozen chains: `campaign-e40-m1/run/chains/` (36 × CHAIN_COMPLETE.json, untouched).
- Repaired rollup artifacts: `campaign-e40-m1/run/rollup/E40_MATCHED_ROLLUP_V1.{json,md}`
  (filename per campaign convention; in-file `schema_version` bumped to v2).
- Static validation script + output: transcribed above; probe outputs under
  `campaign-e40-m1-probe/run/results/51000{1..4}`.
