# ME-X2 V3 — outcome receipt: the identification threshold is not a lever; the M2–B5 parity replicates on a fresh seed

```text
ME_X2_V3_STATUS   = EXECUTED_PROTECTED (fresh-seed replication + threshold ablation)
ROUTE             = PARENT_SUFFICIENT (parity within power)
LEVER_VERDICT     = THRESHOLD_LEVER_NULL_AT_CALIBRATION (public, pre-freeze) -> THRESHOLD_NULL (protected: M3 ≡ M2, 0 discordant)
M2 / M3(τ*=1.0)   = 0.9900   B5 = 0.9883   (paired diff +0.0017, 14 vs 12 discordant, exact p = 0.845)
FALSE_ESCALATIONS = M3 0 · M2 0 · M(V1) 1 · B5 14      MISSED = M3 12 · M2 12 · B5 0
GRANTS            = nothing
```

**Design (frozen after the public calibration, before any protected instance):** `ME_X2_V3_IDENTIFICATION_THRESHOLD_DESIGN_V1.json`
sha256 `7827d29c1079636942f48815197bbd994fd4e28f8c4538a799d68c7e2a200a31` (PR #338). **Authorization:** minted from the operator's standing verbatim
authorization (2026-09-02; reaffirmed 2026-09-04), coordinator-written and says so; consumed, archived as `PROTECTED_RUN_AUTHORIZATION_USED_V1.json`.
**Run:** LUNARC `lu48` job **3579603**, clone `9c32d2b`, `.venv` CPython 3.13.5; selftest PASS and a 48-instance development rehearsal in the same job;
executed once. **Seed revealed:** `ME-X2-V3-PROTECTED-8bbfc87810e00d66399e5a5755826b3fc385d8619a6acd02` (hashes to the commitment). **Results:** `results/ME_X2_V3_PROTECTED_RESULTS_V1.json`
sha256 `8ff4f6fd2a52b25cb2bd0e72821ed17618f2c716e959e2fc8849cff4a24f8f28`; transfer LUNARC → billy-old → Mac, md5 `ec97249c…` both ends.

## 1. The lever, closed in two stages

1. **Calibration (public, 240 instances, frozen rule).** Every commitment the coverage-share threshold made was a false escalation (13/13 at
   τ = 0, 9/9 at τ = 0.5); above τ = 0.6 it never fired; the MINRANK and MAXSHARE selectors coincided on every instance. τ\* = 1.0 ≡ M2.
2. **Protected (fresh seed, 1200).** `M3_MINRANK_TAU_100` reproduces M2 decision-for-decision (0 discordant, G5 null by identity, as
   pre-registered). The threshold was *consulted* on 73 instances and committed on none. The always-commit ablation `M3_MINRANK_TAU_000`
   costs 0.9900 → 0.9292 with **73 false escalations and 12 specification damages** — the harm the threshold exists to prevent, measured on
   the protected split.

**Mechanism, stated as the attribution correction it is:** when M2 abstains, no live hypothesis' warranted fix covers more than half of the live
set, and the minimum-responsible (= maximum-coverage) candidate is systematically not the truth. A commitment rule that reads only the live set's
coverage structure cannot recover those episodes; the exact planner recovers them by finite-horizon reasoning over the registered outcome
tables — which is B5 (V2 §10). The R1b lever is **dead after a revival attempt**, with its mechanism recorded.

## 2. The replication (secondary, pre-registered as such)

On a fresh committed seed M2 and B5 are at parity: 0.9900 vs 0.9883, 14 vs 12 discordant, p = 0.845 — V2's `PARENT_SUFFICIENT (parity within
power)` replicates, this time with M2 numerically ahead, which changes nothing at the registered α. The escalation-harm asymmetry replicates
exactly in kind: B5 reaches its rate with 14 false escalations and 0 missed; M2 with 0 false and 12 missed. The H-EXT-3 ladder is monotone
(0.687 → 0.822 → 0.869 → 0.951 → 0.988); B3 at 1.5× budget stays at 0.850 (the gap is not bought with search). V1's M reads 0.9742 here
(V1's protected value was 0.963; V2's 0.9658).

## 3. Disclosed deviation

The design text lists "τ = 0 / 0.5 ablations" for the protected stage; the frozen runner's arm rule executed τ = 0 only (`{τ\*, 0, 1}`). The
τ = 0.5 ablation exists at calibration strength (public split) and was not run protected. No gate reads it; recorded, not repaired.

## 4. Gates

G0a/G0b/G0c PASS; G1b not fired, G1c not fired; G2 anti-escalation PASS (0 vs 14); G2b counts above; G4 ladder monotone; G5 lever attribution
null by identity (pre-registered). Route `PARENT_SUFFICIENT (parity within power)`. Unit tests 4/4 + V2's 23/23 on billy-old.

Authority: grants nothing — ME-X2 V1/V2 unchanged; no field status, novelty or manuscript change. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

skills-applied: none (outcome receipt, no manuscript content)
