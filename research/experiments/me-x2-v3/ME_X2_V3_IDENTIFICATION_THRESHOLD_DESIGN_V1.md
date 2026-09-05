# ME-X2 V3 — identification-threshold calibration under the H-EXT-3 interface standard (frozen design V1)

**Revival backlog:** #308 row **R1b**. **Predecessors:** ME-X2 V1 `PARENT_SUFFICIENT (B5_DOMINATES)` — all 43 of B5's
discordant wins were M declaring `CANNOT_IDENTIFY` on decidable episodes, all 19 of M's wins were B5 over-escalations;
ME-X2 V2 `PARENT_SUFFICIENT` (parity, p = 0.265) with `LEVERS_RECOVER_M` and 18 residual missed escalations.
**Attributed stage (one):** the *identification rule* — M2 abstains unless one intervention resolves every live
hypothesis. **Lever:** a registered threshold τ on the coverage share of the minimum-responsible live hypothesis'
fix (`mex2v3_levers.py`); τ = 1.0 is M2 exactly (identity, asserted), τ = 0.0 always commits. **Frozen:** 2026-09-05,
after the PUBLIC calibration and before any protected instance exists. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. Calibration (public split, 240 instances, seed `ME-X2-V3-CALIBRATION-20260905`) — the finding

Frozen selection rule (written before the calibration ran): the highest decision-correct rate among grid points whose
false escalations and specification damage do not exceed B5's; ties → largest τ, then the MINRANK selector.

| grid point | decision | false esc. | missed esc. | spec dmg | committed |
|---|---:|---:|---:|---:|---:|
| τ = 0.00 (always commit), either selector | 0.9208 | **13** | 6 | 2 | 13 |
| τ = 0.50, either selector | 0.9375 | **9** | 6 | 2 | 9 |
| τ ≥ 0.60, either selector | 0.9750 | 0 | 6 | 0 | **0** |
| M2 (≡ τ = 1.0) | 0.9750 | 0 | 6 | 0 | — |
| B5 federation | 0.9833 | 4 | 0 | 0 | — |

**Every commitment the threshold makes is a false escalation** (13/13 at τ = 0, 9/9 at τ = 0.5) and above τ = 0.6 it
never fires: whenever M2 abstains, no live hypothesis' warranted fix covers more than half of the live set, and the
minimum-responsible candidate (identically the maximum-coverage candidate — the two selectors coincide on every
instance) is never the truth. **τ\* = 1.0 (≡ M2), selector MINRANK.** Lever verdict at calibration:
`THRESHOLD_LEVER_NULL_AT_CALIBRATION`. The stage attribution is therefore corrected before the protected run: M2's
residual abstentions are not a *threshold* failure — the live set at abstention is diffuse, and a coverage-share
commitment is dominated by the exact planner's own commitment, which is B5. The constraint is named for any successor:
recovering these decisions needs finite-horizon reasoning, which *is* the parent (V2 §10).

## 2. Protected stage (pre-registered, executed under this freeze)

Because τ\* ≡ M2, the protected split is a **fresh-seed replication** of V2's primary contrast with the threshold
ablations run beside it: arms B3, B3 × 1.5, the H-EXT-3 ladder R1–R4 + B5, M (V1), M2, `M3_MINRANK_TAU_100` (≡ M2, identity),
`M3_MINRANK_TAU_000` and `M3_MINRANK_TAU_050` (ablations), both controls; 50 pairs per stratum = 1200.

Pre-registered expectations: G1b (M3 > B5) does **not** fire; route `PARENT_SUFFICIENT` (parity or B5 ahead); the
τ = 0 / 0.5 ablations show false escalations ≥ 1 on the protected split while M2 and τ\* show 0; over-escalation counts
reported in absolute numbers for M3/M2/M(V1)/B5 (co-primary, `G2b`). Lever verdict `THRESHOLD_NULL` (M3 ≡ M2, 0 discordant).

## 3. Gates

G0a selftest (τ = 1.0 ≡ M2 decision-for-decision and trajectory-for-trajectory; τ = 0 fires somewhere; a planted G2
mutation is caught); G0b oracle self-agreement + variant invariants; G0c null calibration; G1b/G1c exact paired tests
M3 vs B5; G2 anti-escalation vs B5 (live); G2b over-escalation counts; G4 ladder monotone; G5 lever attribution (M3 vs M2).
Routes: `LANE_DEFECT`, `M3_ADVANTAGE__THRESHOLD_COMMITMENT_WITHIN_B5_HARM`, `M3_ADVANTAGE_BOUGHT_WITH_ESCALATION_HARM`,
`PARENT_SUFFICIENT (B5_DOMINATES)`, `PARENT_SUFFICIENT (parity within power)`.

## 4. Custody

V1 and V2 files sha256-pinned (`substrate_pins_sha256`); the calibration JSON is pinned by sha256; `protected` refuses
without the ME-X-shape authorization (3), on pin/calibration drift (5), on a seed not hashing to the commitment (4).
Seed custody `~/.orion-custody/me-x2-v3/PROTECTED_SEED_V3.txt` (scp+md5 to LUNARC; revealed after). LUNARC `lu48`.

## 5. Authority

Grants nothing; ME-X2 V1/V2 unchanged. What this design adds at earned strength is a *negative with its mechanism*: the
coverage-share identification threshold is not a lever on this problem, shown on a public split before any protected run.

skills-applied: none (frozen design, no manuscript content)
