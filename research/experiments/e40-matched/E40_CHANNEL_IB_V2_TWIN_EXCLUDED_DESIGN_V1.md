# E40 — Channel information bound and ranker shipping, V2: twins leave the fold (frozen before computing)

**Class:** registered re-analysis; a **fold repair** of two frozen V1 re-analyses
(`E40_CHANNEL_INFORMATION_BOUND_DESIGN_V1`, `E40_RANKER_SHIPPING_REANALYSIS_DESIGN_V1`). Zero model
calls, zero native runs, pure Python. **Twin:** `E40_CHANNEL_IB_V2_TWIN_EXCLUDED_DESIGN_V1.json`.
**Runner:** `e40_channel_ib_v2_twin_excluded.py`, which imports the two V1 modules read-only and
changes exactly one thing.

## 1. The defect, found on the real data after the V1 rollups were filed

The m2/m3 substrate is deterministic: the same configuration produces the same native run and the
same truth. Fifteen exact configurations — same dataset, regime, fraction, `model_seed` and
`partial_intervention_seed` — were executed in **more than one chain** (F0 chains re-using seeds;
m3's cycle-1 anchor landing on the same `interventional@0` config an F0 chain also ran). **39 of the
144 rows have a byte-identical run in another chain, with identical truth in every twin group.**

V1's leave-one-chain-out held out one chain while its twin rows sat in the training fold. So the
V1 "out of sample" ranker saw the very sample it was scoring in 27 % of its rows, and the direction
of the bias is favourable to the ranker. The V1 verdicts that rest on those folds are withdrawn:

| V1 quantity | V1 value | status |
|---|---|---|
| IB1 `FEEDBACK_RANKS_TRUTH_OOS` (`FB8` ρ 0.220, p 0.019) | fired | **WITHDRAWN → CANNOT_CHECK** |
| IB2 `CONFIG_RANKS_TRUTH_OOS` (`CFG` ρ 0.324, p 0.003) | fired | **WITHDRAWN → CANNOT_CHECK** |
| IB3 (`FB8+CFG` − `CFG` +0.067, p 0.205) | not fired | withdrawn with the others; re-derived here |
| RS recovered fraction 0.41; RS1 p 0.0585 | not fired | **WITHDRAWN → CANNOT_CHECK**; the negative terminal is re-derived under clean folds rather than kept on a "favourable direction" argument |

The V1 rollups are not edited. The pre-run audit asked whether the contrast could exist and whether
each clause was reachable; it did not ask whether the held-out stimulus had an exact twin across
the fold boundary. That question is now a ledger guard (`HELD_OUT_SAMPLE_HAS_A_TWIN_IN_THE_FOLD`).

## 2. The one change

For a held-out chain, the training fold **excludes every row whose exact configuration equals any
configuration in the held-out chain**. Ranker (ridge, λ = 1.0), feature sets, statistics, nulls,
seeds, plant and null-calibration constants, IB gates IB0–IB3, RS pairing/contrasts/gates RS0–RS4,
routing and the primary kind are inherited verbatim from the V1 designs.

Chains sharing dataset and rep remain correlated substrate draws even when their configs differ.
That is legitimate substrate structure — the configuration prior, which `CFG` measures — not a
twin, and it is disclosed rather than removed.

## 3. Controls (evaluated first, consumed by the gates)

| control | rule |
|---|---|
| `TWIN_CENSUS_FIRES` | the census reproduces **15 configs / 39 rows**, identical truth within every twin group — the detector must fire on the real data |
| `V2_FOLD_HAS_NO_TWIN` | for every held-out chain, training-fold size = all-other-rows − twin rows, recounted from the rows, not from the filter |
| `M4_M1_REPRODUCED`, `M2_M3_PRIMARY_AND_CENSUS_REPRODUCED` | inherited |
| `PLANTED_SIGNAL_DETECTED` (IB), `PLANTED_SIGNAL_SHIPS` (RS) | inherited, evaluated under V2 folds |
| `NULL_CALIBRATION` (IB and RS) | inherited, evaluated under V2 folds |
| `RECOVERABLE_IMPROVEMENT_EXISTS` (RS) | inherited |

## 4. Gates and routing

Inherited verbatim. The V2 terminals replace the withdrawn V1 terminals in the receipt and in the
ORION-paper registry (P-C carries the E40 entry).

## 5. Pre-run reachability audit

Seed does something (inherited draws). Contrast could exist: removing at most a handful of rows
from a ~140-row fold leaves the ranker fittable; the plant must still fire and the shuffled null
must still sit near zero. Every clause satisfiable (the plant) and failable (the null calibration).
Held-out sample has a twin: **no, by construction**, asserted by `V2_FOLD_HAS_NO_TWIN`.

## 6. No-rescue

No constant, gate, threshold, seed or routing row changes after the V2 rollup is computed.

skills-applied: none (frozen design, no manuscript content)
