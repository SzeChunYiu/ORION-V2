# E40-m4 — Shipping-Operator Counterfactual Outcome Receipt (V1)

**Campaign:** `campaign-e40-m4` (re-analysis rollup; no model calls, no native runs)
**Design:** `E40_M4_SHIPPING_OPERATOR_COUNTERFACTUAL_DESIGN_V1.{md,json}` (PR #129, main `0a5a1fa`)
**Script:** `e40_m4_shipping_counterfactual.py` sha256 `9827fe38b9df807c8836eae8c759dd582e9c76dec11e53b1736459d66f5c39fd`
**Run:** LUNARC login, 2026-08-31; deterministic; inputs read-only (m2/m3 frozen chains + results); 288-file sha256 manifest in rollup.
**Rollup:** `rollup-m4/E40_M4_SHIPPING_COUNTERFACTUAL_ROLLUP_V1.{json,md}`
json sha256 `b8d2554097b43299a3aff8e200c580476baded8150b057e997a5f9898a732817`,
md sha256 `ecb832f408079011c4e80698f96b1134e8ad1ea20e829eddba9d4385829ae774`.

## 1. Outcome

| Gate | Verdict | Basis (cohort P / replication R) |
|---|---|---|
| **G0 `M3_REPRODUCED`** | **PASS** | all five frozen m3 numbers reproduced from raw artifacts (primary mean_d/perm_p, TP mean_d/perm_p with orientation auto-resolved `f0_minus_f2`, both_best mean_d) — the analysis pipeline is bit-faithful to the frozen m3 rollup |
| **G1 `DRAG_ELIMINATED_UNDER_PROXY_SHIPPING`** | **NOT FIRED** | CT1 (f0_best − f2_ship, raw wasserstein): P mean_d **−0.01127**, perm_p 0.99951, F0 wins **11/12**; R mean_d **−0.00744**, perm_p 0.99927, 11/12. Proxy shipping does not eliminate the drag; in m3 it is **worse than terminal shipping** (terminal: −0.00741), in m2 a ns wash (CT2_R +0.0015, p=0.20) |
| **G2 `PROXY_CHANNEL_UNINFORMATIVE`** | **FIRED** | pooled proxy-truth ρ: P **+0.191** (perm p=0.253), R **−0.0007** (p=0.997); per-chain ρ sign-flips (P: six chains ≥+0.4, four ≤−0.7); shipped-cycle true-rank mean 2.58 (P) / 2.33 (R) vs 2.5 chance — **selection at chance** |

**Pre-registered route taken:** `G2 ∧ ¬G1` → **draft m5′ feedback-channel design**
(calibrated extreme-resident probes / proxy-truth calibration feedback).
Zero fallback chains (both cohorts `OK`); C2 leakage re-check clean on all 96
feedback files; C1 census: proxy-argmax lands on cycle1 in 6/12 (P) / 7/12 (R).

## 2. Mechanism (the new fact m4 adds beyond m3)

CT3 TP family (d = f2_ship − f0_best; positive = F2 ship has more):

| channel | P | R |
|---|---|---|
| true_positives | **+14.58 (p=0.00073)** | **+12.92 (p=0.00073)** |
| corum_tp | **+10.33 (p=0.00122)** | **+10.33 (p=0.00391)** |
| string_tp | **+28.17 (p=0.00171)** | **+26.50 (p=0.00024)** |

The proxy-argmax cycle **significantly beats the oracle-selected federation
shipper on exactly the channels the proxy measures** — external-knowledge TP
agreement — while being significantly *worse* on the true objective
(wasserstein to the held-out quantitative graph). The cycle-visible feedback
channel is therefore not a noisy estimate of the truth; it is a **different
objective** whose argmax anti-selects on truth. Combined with m3
(trajectory contains oracle-matching cycles — `both_best` null; terminal rule
discards them), the E40 drag now decomposes fully:

1. the terminal shipping rule loses the good cycle (m3), **and**
2. no rule computable from the existing cycle-visible channel can recover it,
   because that channel does not rank truth (m4: pooled ρ≈0, selection at
   chance, argmax anti-selects) — a pure selection-operator fix (m5) is
   **excluded by evidence**, not merely unhelpful.

The remaining named lever is exactly the m3-named one, now with a sharper
specification: the feedback channel needs a **truth-calibrated component**
(calibration line against a held-out truth-anchored statistic, or calibrated
extreme-resident probes) — any pure external-knowledge channel selects for
external-knowledge agreement, which on this substrate is at best uncorrelated
with, and at the argmax anti-correlated to, the quantitative objective.

## 3. Design erratum (disclosed, verdicts unaffected)

The design's CT2 gloss reads "negative = proxy shipping improves"; the
computed quantity d = f2_final − f2_ship on raw wasserstein has the **opposite
sign convention** (negative = terminal better). The quantity, the G1 primary
clauses (mean_d, perm_p), and all verdicts above are computed from CT1/CT3
and are unaffected; CT2's `recovery_nonneg_chains` clause (8/12 both cohorts)
is correctly read with the corrected gloss as "terminal at least as good as
the proxy pick in 8/12 chains" — which *supports* G2 rather than the gate's
intent, and G1 fails on its two primary clauses regardless (−0.0113 < −0.001;
0.9995 > 0.90). No gate outcome changes under the correction.

## 4. Programme reading

- E40 line now carries **four matched verdicts** (m1 substrate-invalid → m2
  GIES drag → m3 anchor-robust drag → m4 channel-attribution) with a single
  consistent, narrowing mechanism. The m4 step was requested by the operator
  ("improve the theories and try to save them") and executed under the
  no-rescue clause: it selects levers, it does not rescue the negatives.
- **m5 (selection-operator fix) is closed by evidence** — the compute-free
  half of the named lever class is exhausted.
- **m5′ (feedback-channel redesign) is authorized for design**, with the
  §2 specification. It requires new matched-scale compute; LUNARC is
  committed through Sep 4 (SD70 from Sep 3 18:35, E70-GC1 from Sep 4 08:00),
  so the m5′ design PR may proceed now and dispatch after those complete —
  its own freeze precedes any run, per discipline.
- If m5′ also fails its gate, the E40 line is terminal: the metabolic loop's
  deficit is then attributable to the information available to it, not to its
  search or selection machinery, and further revival would need a new
  mechanism class.

## 5. Custody

- Inputs: `campaign-e40-m3/run/{chains,results}` (exp_ids 501000–501047),
  `campaign-e40-m2/run/{chains,results}` — untouched; every file read is in
  the rollup's 288-entry sha256 manifest.
- Determinism: no RNG except the frozen-seed (20260831, 10,000-draw) M1
  shuffle; re-run produces byte-identical JSON (rollup shas above).
- This receipt + `rollup-m4/` archive land in-repo via the PR carrying this
  file; the frozen design/script land in PR #129 (merged `0a5a1fa`).
