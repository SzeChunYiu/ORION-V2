# ME-F1 R3 — the controller's development-split loss attributed by organ ablation (Design V1, frozen before dispatch)

**Class:** development-split measurement through the frozen V1 runner (`mef1_run.py dev`, imported
read-only), on the same eight development campaigns every V1 run measured, using the three omission
ablations V1 froze for M and never ran. **Machine-readable twin:**
`ME_F1_R3_ORGAN_ABLATION_DESIGN_V1.json` (constants asserted equal by the selftest). **Runner:**
`mef1r3_ablation.py` (`selftest` / `freeze` / `run --run-id` / `evaluate`).
**Cannot alter:** ME-F1's terminal (`CANNOT_CHECK`, G0e structural), the refusal of protected
dispatch, or the B5 comparator question left open between the R2 freeze and PR #276.

## 1. The negative, and why it is still unattributed

The G0e receipt (§5) records, at identical budget, toolbox, model and control-call count, the bare
model above the ORION control above the parent federation: **`SIMPLE_DIRECT` 0.7562 > M 0.4062 >
B5 0.3000**, reproduced in a second run (0.6625 / 0.4500 / 0.2437). §5.1 attributed **B5's** loss to
its own control text — a band rule prescribing the dominated solver at the critical rung — and R2
discharged that with a trained selector, deterministically. **M's loss was never attributed.**
PR #276 is the nearest evidence: with M's prompt untouched it held at 0.31–0.45 across four runs, and
it switched tool after an `INCONCLUSIVE` 0.30–0.44 of the time (B5 pre-repair: 0.03–0.05), so M is
not simply B5's defect under another name.

M is three organs, and V1 registered an omission ablation for each (`M_MINUS_WARRANT_GATE`,
`M_MINUS_LOCUS_DIAGNOSIS`, `M_MINUS_MINIMUM_ESCALATION`; texts in `mef1_arms.py`, written before any
outcome, never dispatched because the protected campaign was refused). Two of the three name a
candidate stage:

| hypothesis | organ | mechanism the hypothesis names |
|---|---|---|
| **(b) mandate** | minimum escalation | *"take the CHEAPEST action … L0 more budget, L1 restart, before L2 switch tool"* — on this geometry the cheap tool is dominated (R2 §3: `local_search` settles 0–12 % at the critical ratios, `exact_solve` 100 %), so the ordering sends the loop back to `INCONCLUSIVE` |
| **(a) discipline** | warrant gate | abstention scores zero, and on a world where nothing launders (G0e) the gate buys nothing — M abstains on 95 rungs to `SIMPLE_DIRECT`'s 39 |
| (a′) residual | — | neither organ carries it |

## 2. The test — one lever per arm, zero new text

Five V1-frozen arms — the parent, M, the three ablations — on the eight development campaigns
(7 `F_CRITICAL` + 1 `F_PLANTED`, the planted one excluded from the primary by V1 registration),
two runs, the V1 channel (`call_control` → codex-cli 0.129.0-alpha.15 / `gpt-5.5` / medium on
billy-old; served id not exposed, carried as `UNPINNED_SUBSTRATE_CONDITION`), the V1 geometry
(calibration receipt sha256-asserted at freeze, run and evaluate; `mef1_arms.py` likewise).
**Primary:** `warranted_correct_rate` over decided rungs. **Statistic:** per (run, campaign) paired
difference, one-sided sign-flip p over the 16 pairs (4000 flips, seed 20260904).

## 3. Controls — consumed by the gates

| control | rule |
|---|---|
| `ALL_CELLS_PRESENT_AND_SCORABLE` | 5 × 8 × 2 cells, zero `cannot_check` |
| `BUDGET_MATCHED_ACROSS_ARMS` | one distinct action count and one distinct call count over every cell |
| `INSTRUMENT_REPRODUCES_V1_ENVELOPE` | the two untouched arms land inside V1's observed range widened by one range width each side: `SIMPLE_DIRECT` ∈ [0.5688, 0.8499], M ∈ [0.1750, 0.5875] |
| `LAUNDERING_MEASUREMENT_POPULATED` | total claims > 0 (an unwarranted count over zero claims is not a measurement) |

## 4. Gates and routing

- **A0** all controls PASS (a failure refuses every gate, exit 4).
- **A1 `MANDATE_IMPLICATED`** — mean(`M−MinEsc` − M) > 0, p ≤ 0.05, **and** its `INCONCLUSIVE`
  rate is below M's — the mechanism the hypothesis names must move, not only the score.
- **A2 `DISCIPLINE_COST`** — mean(`M−WarrantGate` − M) > 0, p ≤ 0.05.
- A3 (locus diagnosis) and A4 (best ablation vs the parent, both directions' p) reported; parity
  with the parent is never gated as an absence claim.

| outcome | terminal |
|---|---|
| A0 fails | `CANNOT_CHECK__CONTROL_FAILED` |
| A1 ∧ ¬A2 | `M_HANDICAPPED_BY_ITS_ESCALATION_MANDATE__PROMPT_IMPLICATED_MODEL_EXONERATED` — (b) |
| A2 ∧ ¬A1 | `WARRANT_DISCIPLINE_COSTS_COVERAGE_ON_A_WORLD_THAT_FORECLOSES_LAUNDERING__REGIME_CONDITIONAL` — (a), intermediate |
| A1 ∧ A2 | `BOTH_MANDATE_AND_DISCIPLINE_IMPLICATED__TWO_ORGANS_EACH_COST_COVERAGE` |
| neither | `M_DEFICIT_NOT_ATTRIBUTABLE_TO_A_NAMED_ORGAN__ARCHITECTURAL_RESIDUAL` — (a′) |

**What a (b) outcome would license.** A re-derived escalation order for M (the trained selector R2
built, applied to M's own L-ladder) under a **new** identity; not a repair of V1, not a protected
run, not a comparator decision. **What an (a) outcome means.** Regime-conditional, by the doctrine
intermediate: the organ costs coverage on a world that forecloses the failure it prevents; the
test that would make it terminal is a world in which warrant status is a judgment call, and V1's
own receipt says that is a different study.

## 5. Pre-run reachability audit

Seed does something (flips); campaigns fixed by registration so the instrument control is
meaningful. Every routing row reachable on synthetic input (selftest); the instrument control can
fail (selftest plants an out-of-envelope parent and the verdict is refused). No parent isolation:
identical budget, toolbox, model, calls, campaigns; every text V1-frozen and sha-asserted. A1 cannot
fire on a score move without the named mechanism moving. Served model not pinned — disclosed.

## 6. Pre-run expectation, disclosed

PR #276's untouched-M numbers predict A1 (the mandate) and leave A2 open (the 95-vs-39 abstention
gap). Written before dispatch so neither can be read afterwards as a surprise.

## 7. No-rescue clause

No arm, constant, envelope, gate, seed or routing row changes after dispatch begins. A defect found
afterwards is recorded in the receipt and repaired under a new identity.

skills-applied: none (frozen design, no manuscript content)
