# E40-m3 (cycle-1 anchor revival) — campaign outcome receipt (2026-08-30)

**Campaign:** `campaign-e40-m3` — the operator-directed second revival of the E40
matched-compute line, testing the one named-but-untested lever left by the m2
`METABOLIC_DRAG_MATCHED_NATIVE` negative: an **exploration prior**. Single delta
vs m2: F2's cycle-1 prompt carries a binding regime-extreme anchor
(`training_regime ∈ {observational, interventional}` at cycle 1; interior
fractions reserved for cycles 2+), enforced by `ask_config_f2` re-ask (≤3,
exhaustion ⇒ `CANNOT_CHECK`, never silent fill). Cycles 2–4 prompts byte-identical
to m2. SIMPLE/F0 not re-run — frozen m2 chains reused read-only
(`E40M_REF=campaign-e40-m2`), keeping the contrast single-delta. Design
pre-registered in PR #100 (`E40_MATCHED_M3_EXPLORATION_PRIOR_REVIVAL_DESIGN_V1.{md,json}`).
Runner sha256 `f6a6aaca9b20a707a5bc6c6ff325f473b377fcc8cb92b126915a44559de36964`;
selftest 0 failures (Mac + LUNARC login node). SLURM chain array **3554920**
(0-11%6, 12/12 COMPLETE, 0 CANNOT_CHECK), eval **3554985** (controls → audit →
rollup). F2 native runs 48 (exp_ids 501000–501047).

## 1. Substrate + control validity

| Check | Value |
|---|---|
| NaN primaries | simple 0/12, f0 0/48, f2 0/48 |
| pairs COMPLETE | 12/12, `CANNOT_CHECK__NO_DEFINED_PRIMARY` 0 |
| planted feedback recovery | **PASS** — inherits the anchor (cycle 1 `interventional@0.0`), terminal planted quality 0.9877, no post-arrival dip |
| permutation null calibration | **PASS** — rejection 0.055 ∈ [0.02, 0.09] (400 reps) |
| uninformative replay | present, 12 chains, finals 0.156–0.188 |
| leakage+pin audit | 0 violations |

## 2. Outcome (pre-registered gate map applied verbatim)

```
gate            METABOLIC_DRAG_ROBUST_TO_ANCHOR   (mean_d < 0 AND perm_p >= 0.95)
mean_d          −0.007414   (F0_best − F2_final; m2: −0.008979)
perm_p_exact    0.986084    (sign-flip exact, 12 pairs; m2: 0.999)
wins            f2 2 / f0 10   (m2: 1/11)
```

The alternative pre-registered gates did not fire: not
`F2_METABOLIC_ADVANTAGE_UNDER_ANCHOR` (p ≫ 0.05), not
`EXPLORATION_PRIOR_EXPLAINS_DRAG` (|d̄| = 0.0074 ≥ 0.005). Mandating the
exploration prior moved the drag by +0.0016 and one pair — far from removing it.

## 3. Mechanism (pre-registered secondary readouts, from the frozen chains)

- **The anchor binds perfectly and is then abandoned.** Cycle-1 census:
  `interventional@0.0` **12/12**, every chain on the FIRST ask (mandate
  transcripts: asked=1, violations=0 in all 12 — the re-ask path never fired).
  Cycle-4 finals: extreme only **5/12** (`interventional@0.0`); **7/12 drift
  interior** (partial 0.25/0.4/0.6/0.75/0.8×2/0.85). The loop was handed the
  extreme family that wins and the cycle-visible feedback pulled it off again.
- **The drag is the selection operator, not per-cycle quality.** Decomposition
  contrasts: `both_final` d̄=+0.0009 (p=0.388), `both_best` d̄=−0.0012
  (p=0.696) — both nulls. Only `F0_best − F2_final` separates (−0.0074,
  p=0.986). Matched cycle-for-cycle, the metabolic loop equals the federation;
  the entire deficit is that F0 ships **max-of-4 selected by true score** while
  F2 must ship its single sequential terminal **selected by the cycle-visible
  proxy**.
- **True-structure cost of that operator:** true_positives −13.08 (p=0.996),
  corum_tp −9.42 (p=0.995), string_tp −25.75 (p=0.991); false_positives +2.67
  (p=0.274, n.s.) — F0's best recovers more true edges at no significant FP cost.
- Per-dataset collapse check: k562 passes (f2 median TP 157.0 vs simple 135.5),
  rpe1 fails (45.5 vs 54.5) — the rpe1 asymmetry carried over from m2 unchanged.

## 4. Programme reading

Three matched-compute verdicts now sit on this substrate class: m1 (pc)
confounded within-observational null; m2 (gies) full-space drag p=0.999 with an
exploration-prior attribution candidate; **m3 (gies+anchor) drag p=0.986 with the
exploration-prior candidate refuted**. The anchor experiment converts the m2
attribution into a sharper one: the loop is not starved of extreme coverage — it
is given the extreme and leaves it, because the visible proxy points interior
while true wasserstein favors extremes. That is the signature of the
**proxy-objective misalignment** hypothesis named in the design §5. One
pre-registration caveat stated plainly: the design's trigger for auto-naming
that lever was "drag persists AND finals sit on extremes"; the observed census is
stronger in kind (extreme gifted → interior finish, 7/12) but is a descriptive
readout, not a gated claim.

**Named next lever class (not opened): feedback-channel design** — cycle-visible
diagnostics that include calibrated extreme-resident probes (or proxy-vs-truth
calibration feedback) so the visible gradient cannot point uniformly interior.
Opening it is an operator decision: the E40 line now carries three matched
verdicts with a consistent mechanism, and compute through Sep 4 is committed to
SD70 and E70-GC1.

## 5. Chain of custody

- Frozen chains: `campaign-e40-m3/run/chains/` (12 × CHAIN_COMPLETE.json,
  per-cycle decision.json with mandate transcripts in `call_log`).
- Rollup: `campaign-e40-m3/run/rollup/E40_MATCHED_ROLLUP_V1.{json,md}`
  (`"variant": "e40-m3-cycle1-anchor-revival"`,
  `"reference_arms_root": …/campaign-e40-m2`), archived under `rollup-m3/` with
  the eval log (`eval-3554985.out`: planted/nullcal/uninformative control
  records + audit + rollup).
- Design lineage: PR #100 (pre-registered design + runner), m2 receipt §4
  (parent negative), m2 §3 mechanism census (attribution basis).
