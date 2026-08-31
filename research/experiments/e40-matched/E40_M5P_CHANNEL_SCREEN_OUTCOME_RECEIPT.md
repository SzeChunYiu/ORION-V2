# E40-m5′ Stage-1 — Truth-Calibration Channel Screen Outcome Receipt (V1)

**Campaign:** `campaign-e40-m5p/stage1` (re-analysis screen; no model calls, no native runs)
**Design:** `E40_M5P_CHANNEL_SCREEN_DESIGN_V1.{md,json}` (PR #131, main `0a5a1fa`)
**Script:** `e40_m5p_channel_screen.py` sha256 `cb8998fe0a18a46540b2ec4112feffdeebbfcc1d6f945c8276e7ea5935b500ed`
(sha chain `207192b5…` PR #131 → `e2360040…` PR #133 → `cb8998fe…` PR #134; see §5)
**Run:** LUNARC login, 2026-08-31, exit 0; deterministic; inputs read-only (m2/m3 frozen
chains + results + the m4 rollup); 289-file sha256 manifest in the rollup.
**Rollup:** `rollup-m5p-stage1/E40_M5P_CHANNEL_SCREEN_ROLLUP_V1.{json,md}`
json sha256 `0feed3286f844475a4272d6dbb55c805ca8b172296d0ff6ca6f2c3e1229e8672`,
md sha256 `86f395c66dd65283928c47d867b2478ba812b19cb26553a639afabfa760d26da`.

## 1. Outcome

| Gate | Verdict | Basis |
|---|---|---|
| **GS0 `M4_REPRODUCED`** | **PASS** | m4 M1 numbers for `pooled_tp` reproduced bit-exactly from raw artifacts on both cohorts — P: ρ=+0.1907263740160503, p=0.2530; R: ρ=−0.0006852169173363308, p=0.9968 (both \|Δ\| = 0 vs the archived rollup, whose sha256 equals the pinned `b8d25540…`). The pooled-tp row of the tables below IS m4's M1, recomputed independently |
| **GS1 `SELECTION_AVAILABLE_ON_R`** | **NOT FIRED** | zero non-baseline candidates with R perm p ≤ 0.05 and directed pooled ρ > 0. Best directed ρ among eligible signs: `chipseq_tp` +0.145 (p=0.34); best raw \|ρ\| overall: `sig_purity` −0.4945 (p=0.0022 — anti-directed, see §2). No winner exists |
| **GS2 `WINNER_CONFIRMED_ON_P`** | **NOT REACHABLE** | no winner to confirm |

**Pre-registered route taken (design §6, GS1-fail row):** draft **Stage-2b
seed-replica stability-probe design** (the remaining truth-anchor without
substrate modification; needs new native runs); this outcome *strengthens the
terminal reading* if Stage-2b also fails.

## 2. Full screen (24 rows, no selection)

Directed ρ = −direction × raw ρ (truth lower-better; positive directed = candidate ranks truth). All 24 cohort×candidate rows had 12/12 chains used (zero exclusions, zero <3-finite-pair chains).

| candidate | P raw ρ (p) | R raw ρ (p) | reading |
|---|---|---|---|
| pooled_tp (m4 baseline) | +0.191 (0.253) | −0.0007 (0.997) | m4's M1 reproduced |
| pooled_sig_tp | +0.315 (0.056) | +0.313 (0.058) | anti-truth, marginal both cohorts |
| sig_purity | +0.224 (0.175) | **+0.494 (0.0022)** | **significantly anti-truth on R** |
| string_phys_tp | +0.292 (0.084) | +0.172 (0.280) | ns |
| efficiency | +0.314 (0.063) | +0.008 (0.962) | ns, sign-unstable |
| string_net_tp | +0.209 (0.208) | −0.026 (0.874) | ns |
| zmean_tp | +0.208 (0.210) | −0.139 (0.397) | ns |
| corum_tp | −0.051 (0.765) | +0.223 (0.141) | sign-unstable |
| chipseq_tp | −0.160 (0.320) | −0.145 (0.342) | consistently pro-truth-signed, ns |
| rankmean_tp | +0.186 (0.268) | −0.083 (0.612) | ns |
| fast_runtime | −0.001 (0.996) | −0.046 (0.788) | null |
| ligand_tp | +0.000 (1.000) | +0.000 (1.000) | null (degenerate ranking) |

**Frozen-direction observation (not a lever):** the only screen-wide signal is
`sig_purity` = sig-TP / max(total-TP, 1), which *anti-ranks* truth on R
(+0.494 raw, p=0.0022; 9/12 chains positive, three ≥ +0.82) and trends the same
way on P (+0.224, p=0.175). The significance-family (`pooled_sig_tp`, 
`sig_purity`) is the *only* family with consistent, cohort-stable sign — and it
is negative for truth: **cycles that concentrate feedback mass into
"significant" hits are the cycles that drift away from the quantitative
graph**. This is the same object m4's CT3 measured at the shipping boundary
(proxy-argmax ships more external-knowledge TP while being worse on
wasserstein); here it shows up inside the trajectory as well. Per the freeze,
directions were registered pre-outcome (all TP composites +1, `fast_runtime`
−1); inverting `sig_purity` post-hoc would be outcome tuning and is not
authorized by this screen. It is recorded as a mechanism fact for the Stage-2b
design to consider under its own freeze.

## 3. Programme reading

- The m5′ Stage-1 question — *does any computable composite of the existing
  cycle-visible feedback fields rank truth?* — is answered **no, in-sample**
  (GS1): the compute-free half of the feedback-channel lever class is now
  exhausted alongside m4's operator half.
- The drag attribution is complete and mutually consistent across m2–m5′:
  the deficit is neither search (m3: oracle-matching cycles exist) nor
  selection operator (m4: no computable rule from the channel recovers them)
  nor any single visible field or 11-member composite family (m5′ GS1) — it is
  the **information content of the channel itself**. The one stable internal
  structure the channel carries (significance purity) points *away* from
  truth, i.e. the loop's internal salience signal is actively misleading on
  this substrate, not merely absent.
- Remaining named lever: **Stage-2b seed-replica stability probe** — a
  truth-anchor that does not modify the substrate. If it fails its gate, the
  E40 line is terminal (per m4 receipt §4 and this screen's §6 routing), and
  further revival would need a new mechanism class.

## 4. GS0 note (rng-equivalence engineering paid off)

Reproducing m4's perm_p bit-exactly required the same seed (20260831), the
same draw count (10,000), and the same rng call sequence (fresh `Random`,
`rng.sample(4-list)` per chain, chain order ds-major) as m4's M1 — reasoned at
design time, now *verified by execution*: both cohorts reproduce to |Δ| = 0.0
(≤1e-9 gate margin). This also retro-validates the m4 perm_p numbers as
reproducible from raw artifacts end-to-end.

## 5. Runtime-defect disclosure (3 script defects, all pre-verdict, verdicts unaffected)

The frozen script failed twice on LUNARC before completing; each failure was
fixed, locally validated, PR'd, merged, and re-shipped before the successful
run. No design constant (gates, seed, draws, candidates, directions,
thresholds) changed in any amendment:

1. **`_z` NameError** (run 1): `m, s = mean(xs), …(x − m)…` bound `m` inside
   its own defining expression. Fixed in PR #133 (`e2360040…`). Caught only at
   runtime — `py_compile` is syntax-only.
2. **`KeyError: 'P_confirm'`** (run 2): `main()`'s table comprehension passed
   the cohort name where the candidate key belongs
   (`eval_candidate(v, c)` → `eval_candidate(v, k)`). Fixed in PR #134
   (`cb8998fe…`). Root cause: smoke tests called `eval_candidate` directly and
   never exercised `main()`.
3. **Validation upgrade** (before run 3): a full end-to-end fixture —
   synthetic campaign tree (m2+m3 layout, f0 run0–3 + f2 cycle1–4, fake m4
   rollup bootstrapped from the fixture's own pooled_tp numbers so GS0 is
   exactly satisfiable) — exercised `main()` GS0-true (exit 0), the
   sha-mismatch exit-2 path via subprocess with pinned constants, and the
   winner branch (`argmax_census`, `loo_stability`, 12-chain cohort). Run 3
   then completed exit 0 on the first attempt.

## 6. Custody

- Inputs: `campaign-e40-m2/run/{chains,results}`, `campaign-e40-m3/run/{chains,results}`,
  `campaign-e40-m4/run/rollup/E40_M4_SHIPPING_COUNTERFACTUAL_ROLLUP_V1.json` —
  untouched; all 289 files read are in the rollup's sha256 manifest.
- C2 leakage re-check clean on all 96 F2 feedback files (FORBIDDEN_SUBSTRINGS
  assert, executed not logged).
- Determinism: only RNG is the frozen-seed (20260831, 10,000-draw) within-chain
  cycle shuffle; re-run produces byte-identical JSON (rollup shas above).
- This receipt + `rollup-m5p-stage1/` archive land in-repo via the PR carrying
  this file; frozen design/script in PR #131 (amended #133, #134).
