# E40-m5′ Stage-2d — Planted-Control Cause Discrimination: outcome receipt (V1)

**Disposition: `PROMPT_IMPLICATED` (D2) — not ambiguous.** The cycle-1 mandate text is implicated;
the served model channel alone does **not** explain the Stage-2c planted-control failure.

**Design:** `E40_M5P_STAGE2D_PLANT_DISCRIMINATION_DESIGN_V1.{md,json}` (PR #169, main `b42bf470`),
md sha256 `12857a058a0dc9b654c3a97ab6180a18ac92b2d1cc12f645828c6b27452a031c`,
json sha256 `5a65936e4428f9a87bcd2695854901a7c700936ba3a45393b0fa7fc73cad02bf`.
**Script (unchanged from main, verified on the node):**
`e40_m5p_stage2d_plant_discrimination.py` sha256
`1206abf6ed645456b7286fb2fddb06617851e1c557fa9b74bde1f01c327186ef`.
**Run:** LUNARC login node, 2026-09-02, `run --arm all` then `analyze`, both exit 0 —
**27 model decision calls, zero native runs**, temperature 0, served model `glm-5.3` on every call.
**Rollup:** `rollup-m5p-stage2d/E40_M5P_STAGE2D_ROLLUP_V1.{json,md}`, json sha256
`b5acea3852b34d6f6454b7f3cb476105abb60f78f5cda12bbd797021768e5c0d`.
**Authorization:** operator, in chat, 2026-09-02, verbatim *"run all the computation tasks.. finish
all the researxh asap"*; this diagnostic was authorized by the session coordinator under that
standing instruction (no separate operator act), design shas above, identity
`campaign-e40-m5p-stage2d`.

## 1. Result

All four registered controls **PASS** (`PLANT_INTEGRITY`, `SERVED_MODEL_PIN`, `LEAKAGE`,
`TRAJECTORY_REPLAY`), so the D-gates are admissible (design §5 control-gating).

| arm | cycle-1 rule | verdict | terminal quality | distinct configs | fracs sampled | first cycle ≥0.9 |
|---|---|---|---|---|---|---|
| **A_NO_MANDATE** (m2 form) | none | **PASS** | 0.9877 | 5 | 0.5, 0.75, **0.8**, 0.85, 0.9 | **2** |
| **B_REGIME_ANCHOR** (m3 form) | regime extreme | **FAIL** | 0.9518 | 6 | 0.0, 0.5, 0.75, 0.9, 1.0 | 6 |
| **C_SEED_MANDATE** (Stage-2c form) | seeds 11/13 | **FAIL** | 0.0233 | 2 | **0.0 only** | never |

D0 `ARMS_VALID` **true** (3/3 arms, 9 cycles each, no CANNOT_CHECK); D1 `MODEL_CHANNEL_CAUSE`
**false**; **D2 `PROMPT_IMPLICATED` true**; D3 `STAGE2C_FAILURE_NOT_REPRODUCED` false. Every cycle-1
mandate was satisfied on the first ask (`asked: 1, violations: 0` in all three arms).

**The model channel is exonerated as a sufficient cause.** On the *same* model that failed in
Stage-2c, the *unmandated* form recovers the planted optimum by cycle 2, samples five distinct
`frac` values, lands exactly on the plant's optimum `partial@0.8` (quality 1.0) at cycle 8, and
holds the basin to the end. The loop follows an informative feedback channel on `glm-5.3` perfectly
well — when nothing pins its first cycle.

## 2. Mechanism: mandate-induced exploration collapse, graded by mandate specificity

- **C (seed mandate)** is a total freeze: `interventional @ frac 0.0` for **all nine** cycles, two
  distinct configs (differing only in a seed digit), `frac` never leaves 0.0, quality flat at 0.0233.
  It is *worse* than Stage-2c's own control run (0.6412), i.e. the same failure mode, more severe.
- **B (regime anchor)** is a partial freeze: four cycles pinned on the anchored regime
  (`interventional @ 0.0`, quality 0.0233), then it escapes, reaches 0.9877 at cycle 6, but wobbles
  to `frac 1.0` (0.8208) at cycle 7 — so the last three cycles are not all ≥0.9 and the inherited
  PASS rule fails it. **B is a near-miss, not a collapse.**
- **A (no mandate)** never freezes.

The gradient — none → regime → exact seeds — tracks mandate specificity, which is the mechanism the
Stage-2c receipt named (exploration collapse) now measured directly: a binding cycle-1 rule anchors
the arm on its mandated cycle-1 config and it keeps re-choosing it.

## 3. Honest boundary: the cause is an interaction, not the prompt alone

D2's registered meaning is exactly "the model channel alone does not explain it" — and that is what
is filed. It must **not** be read as "the model is irrelevant":

- **B passed under the m3-era model (0.9877, PASS) and fails here (0.9518, FAIL).** Same prompt
  form, same plant, same rule — different served model, different verdict.
- So the failure requires a **mandate to be present**, and its severity depends on the model: on
  `glm-5.3` both mandate forms suppress exploration, one fatally, one marginally.
- Stage-2d was powered to separate "model alone" from "mandate implicated". It was **not** designed
  to quantify the interaction, and no interaction estimate is claimed. That would need the m2-era
  model, which is unrecoverable (Stage-2c dispatch receipt §2).

## 4. What this does and does not change

- **Stage-2c's disposition is unchanged: `CHECKER_INVALID__NO_VERDICT`.** Its control failure is now
  explained, not repaired; its campaign still yields no probe verdict, and **the E40 line stays
  open** (design §8, no-rescue).
- **The E40 line is not revived and m6 is not authorized.**
- **Consequence a future freeze must confront (not a claim here):** the Stage-2c *live* F2 arm
  carried the same cycle-1 seed mandate whose control counterpart froze completely. If mandates
  suppress exploration on this channel, the drag reproduced by Stage-2c's G0 and the near-disjoint
  replica edge sets (J = 0.028) may both be partly mandate artefacts rather than properties of the
  metabolic loop. Testing that requires a mandate-free replica design — a new prospective identity.
- **The seed-replica probe remains blocked** on the separate `DEGENERATE_PROBE_STATISTIC` finding
  (≈3 % replica edge overlap), which is independent of everything above.

## 5. Custody

- Arms `campaign-e40-m5p-stage2d/{A_NO_MANDATE,B_REGIME_ANCHOR,C_SEED_MANDATE}/cycle{1..9}/`
  (`prompt.txt`, `response.txt`, `decision.json` with prompt/response sha, served model id and the
  mandate transcript, `feedback.json`), per-arm `arm.json`, rollup with a sha256 manifest.
- Archived here: rollup json/md and the three `arm.json` summaries, byte-identical to the LUNARC
  originals (A `a2cedcfe…`, B `9d6de7c8…`, C `233d8463…`).
- `run` refuses to overwrite an existing arm directory, so the 27 calls happened exactly once.
- No design constant, plant parameter, PASS rule, arm set, cycle count or gate was changed after the
  freeze.
