# E40-m2 (gies revival) — campaign outcome receipt (2026-08-30)

**Campaign:** `campaign-e40-m2` — the §5b revival lever executed: identical
matched-compute contrast to e40-m1 with the single pin delta
`PINNED.model_name: pc → gies` (intervention-aware model; probe 510005–510008,
receipt R2 §5c). Runner sha256
`e13baa88b8281096a655bcf2bbcfba01c62ae9c00420549ef9ee8c235f3bf6f2`; selftest
0 failures. SLURM chain array **3554467** (0-35%6, 36/36 COMPLETED), eval
**3554585** (controls → audit → rollup). Arms, prompts, K_CYCLES=4, 12 pairs,
frozen gate map, and the v2 NaN-policy rollup are byte-identical in behavior to
e40-m1 apart from the model pin.

## 1. Substrate validity (the point of the revival)

| NaN-primary runs | m1 (pc) | m2 (gies) |
|---|---|---|
| simple | 12/12 | **0/12** |
| f0 | 36/48 | **0/48** |
| f2 | 21/48 | **0/48** |
| pairs CANNOT_CHECK | (12 valid after repair) | **0** |

The decision space is fully live: every regime produces a defined primary, so
m2 measures the metabolic loop on the **complete** configuration space
(regime × fraction × seed × omission), not the observational corner.

## 2. Outcome (frozen gate map applied verbatim)

```
gate            METABOLIC_DRAG_MATCHED_NATIVE
pairs           12/12 COMPLETE, 0 CANNOT_CHECK
mean_d          −0.008979   (F0_best − F2_final; negative ⇒ F2 worse)
perm_p_exact    0.9990      (sign-flip exact, 12 pairs)
wins            f2 1 / f0 11 / ties 0
controls        planted=PASS nullcal=PASS uninformative=present
audit           leakage+pin, 285 artifacts, 0 violations
```

Per-pair d (F0best−F2final): k562 +0.0056, −0.0234, −0.0101, −0.0069,
−0.0096, −0.0153; rpe1 −0.0076, −0.0065, −0.0077, −0.0033, −0.0017, −0.0214.

## 3. Mechanism (from the frozen chains)

- **F0's best-of-4 lands on regime extremes**: f0_best census = interventional
  5, observational 4, partial 3 (0.8 / 0.25 / 0.5).
- **F2's finals land in the interior**: f2_final census = interventional 5,
  partial 0.5–0.9 6, observational-interior 1; every chain's path spans ≥2
  regime families — the loop genuinely explores the restored axis.
- The extremes score better than the interior on 11/12 pairs, so sequential
  feedback-driven search pays 4× compute to converge mid-axis while the
  upfront federation's parallel sample catches an extreme.
- The planted-feedback control PASSES (chains recover a planted
  partial@0.8 basin, terminal quality 1.0) — the loop *can* follow feedback.
  The drag is therefore not broken feedback plumbing: it is greedy sequential
  exploration on a landscape whose optimum sits at regime extremes the
  cycle-visible feedback gradient does not point to.

## 4. Programme reading

The metabolic hypothesis now carries **two matched-compute verdicts on this
substrate class**: e40-m1 (pc) = within-observational null, p=0.625, verdict
confounded to one basin by the upstream capability stub; e40-m2 (gies) =
full-decision-space **active drag**, p=0.999, 11/12 pairs, mechanism
identified (interior-convergent greedy search vs extreme-sitting optimum).
The revival condition was met — the interventional path was repaired, the
confound removed — and the verdict strengthened against F2, so this is a
mechanism-backed terminal negative for the 4×-metabolic-loop contrast on
causalscbench/weissmann, not a substrate artifact. Further revival would
require a different substrate (not a re-pin); the E40 line is closed here
unless the operator opens one.

## 5. Chain of custody

- Frozen chains: `campaign-e40-m2/run/chains/` (36 × CHAIN_COMPLETE.json).
- Rollup: `campaign-e40-m2/run/rollup/E40_MATCHED_ROLLUP_V1.{json,md}`
  (schema v2 NaN policy), archived under `rollup-m2/` with the eval log
  (`eval-3554585.out`: full planted/nullcal/uninformative control records +
  audit + rollup).
- Design lineage: PR #90 (design), R2 receipt §5b (root cause) / §5c (probe +
  dispatch), PR #97.
