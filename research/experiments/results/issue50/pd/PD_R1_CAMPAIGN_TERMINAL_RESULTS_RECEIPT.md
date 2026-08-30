# PD R1 Dependence-Evidence Campaign — Terminal Results Receipt

**Receipt ID:** `PD_R1_CAMPAIGN_TERMINAL_RESULTS_RECEIPT`
**Date (executed):** 2026-08-30 (dispatch 03:23:06 → complete 05:25:25 +02:00, billy-old)
**Campaign:** `.orion-dependence-evidence-campaign` — 4 studies (PD-S1..S4) × 8–9 arms × 120–160 tasks = **4,440 dispatches**, chained after the FM/FG R1 suite terminal (receipt #79 lineage). Model arms via `gpt-5.6-terra`; offline arms are deterministic constructed parents (`scripts/orion_pd_arms.py`).
**Preceded by:** `PD_OFFLINE_SMOKE_RECEIPT` (PR #75). This receipt records the terminal execution state and the evaluated arm table. Authority grants remain **false** — this is a recorded mixed cell with one decisive component effect, not a superiority claim.

## 1. Terminal execution state

| Check | Value |
|---|---|
| Responses | **4,440/4,440** `COMPLETED_PROPOSAL_ONLY`, 0 failures (census re-verified at receipt time) |
| run_valid | True for all arms in all 4 studies (`missing_or_invalid = 0` everywhere) |
| Dispatch receipt | `all_dispatches_zero: true`, `all_oracles_restored: true` |
| Oracle custody | `private_oracle_visible_to_solver: false`; strata recorded only in the private oracle; freeze manifest hash-pinned (plan, arms, harness) |
| Elapsed | 2 h 02 m 19 s |

## 2. Arm classes (binding for interpretation)

- **Model arms** (codex dispatch): `P_D_FULL`, `P_D_MINUS_DEPENDENCE`, `ROBUSTNESS_TRIANGULATION_PARENT`, `STRONGEST_ASSURANCE_FEDERATION`, `PERFORMATIVE_SAFETY` (S4 only).
- **Offline constructed arms** (deterministic decision rules, `model_calls=0`, self-labeled "constructed calibration ceiling, not an empirical arm"): `CURRENT_INDEPENDENT_COUNTING`, `PROVENANCE_TRACKING`, `STANDARD_DEPENDENCE_META_ANALYSIS`, `ARGUMENT_ACCEPTABILITY`, `SIMPLE_DIRECT_CONTROL`.
- The causal contrast is **P_D_FULL vs P_D_MINUS_DEPENDENCE** (identical substrate, dependence machinery removed). Offline arms are practice-shape baselines, not compute-matched controls.

## 3. Evaluated accuracy matrix (private-oracle scored, per study)

| Arm | S1 (n=160) | S2 (n=120) | S3 (n=120) | S4 (n=120) |
|---|---|---|---|---|
| `P_D_FULL` | 0.9750 | 0.9833 | **1.0000** | 0.9417 |
| `P_D_MINUS_DEPENDENCE` † | 0.5000 | **1.0000** | **1.0000** | **1.0000** |
| `ROBUSTNESS_TRIANGULATION_PARENT` † | **0.9938** | — | — | — |
| `STRONGEST_ASSURANCE_FEDERATION` † | 0.9875 | 0.9750 | **1.0000** | 0.9833 |
| `PERFORMATIVE_SAFETY` † | — | — | — | 0.9083 |
| `PROVENANCE_TRACKING` ‡ | 0.7500 | 0.2500 | 0.5833 | 0.2500 |
| `STANDARD_DEPENDENCE_META_ANALYSIS` ‡ | 0.7500 | 0.2500 | 0.5833 | 0.2500 |
| `SIMPLE_DIRECT_CONTROL` ‡ | 0.7500 | 0.2500 | 0.5833 | **0.0000** |
| `CURRENT_INDEPENDENT_COUNTING` ‡ | 0.5000 | 0.2500 | 0.5833 | 0.2500 |
| `ARGUMENT_ACCEPTABILITY` ‡ | 0.5000 | 0.2500 | 0.5833 | 0.2500 |

† model arm · ‡ offline constructed arm (calibration ceiling by construction)

`CAMPAIGN_EVALUATION_SUMMARY.json.authority`: `grants_R3: false`, `grants_R4: false`, `grants_dependence_detection_in_real_corpora: false`, `grants_scientific_truth: false`.

## 4. The causal contrast, per stratum

Dependence-sensitive strata (S1-A false-corroboration, S1-C) versus preservation strata:

| Stratum | P_D_FULL | P_D_MINUS_DEP | Reading |
|---|---|---|---|
| S1-A (false corroboration) | 1.000 | 0.000 | machinery is the *only* model-arm fix for dependent-source miscounting |
| S1-C | 0.975 | 0.000 | same, second dependence-sensitive stratum |
| S1-B / S1-D (preservation) | 1.000 / 0.925 | 1.000 / 1.000 | small preservation cost (−7.5 pp on D) |
| S2-A/B/C/D | 1/1/1/0.933 | 1/1/1/1.000 | net −1.7 pp aggregate: machinery over-fires on adequacy-only judgments (D) |
| S3-A/B/C/D | 1/1/1/1 | 1/1/1/1 | ceiling tie; no discriminative power |
| S4-B (authority response) | 0.767 | 1.000 | net −5.8 pp aggregate: dependence checking mislabels valid single-source authority responses |

## 5. Honest verdict (binding for P-D §8 import)

1. **The dependence machinery is causally real and large where dependence exists**: removing it collapses S1 from 0.975 to 0.500, concentrated exactly on the two dependence-sensitive strata (0.000 vs ~1.000). This is the first executed component-attribution positive in the generated-suite programme.
2. **The machinery is net-negative where dependence is absent**: S2 −1.7 pp and S4 −5.8 pp aggregate, both traceable to single strata (S2-D, S4-B) where dependence checking rejects valid responses. A trigger-precision defect, not noise.
3. **P_D_FULL does not dominate the strongest parent emulation**: ROBUSTNESS_TRIANGULATION beats FULL on S1 (0.9938 vs 0.9750); STRONGEST_ASSURANCE_FEDERATION beats it on S1/S4 and trails by 0.8 pp on S2.
4. **Constructed practice baselines collapse** (0.000–0.750) — current independent-counting and provenance-only practice fails these tasks badly; this contextualizes, but does not license, a P-D superiority claim (they are not compute-matched).
5. **No authority granted**: all four grants false; the suite is generated, not real corpora. `grants_dependence_detection_in_real_corpora: false` is the machine-checked record — no prose may upgrade it.

**Verdict class:** `TERMINAL_RECORDED_MIXED__COMPONENT_POSITIVE_METHOD_NET_NEGATIVE` — dependence-evidence machinery validated as a mechanism, full method not certified as superior, trigger-precision repair identified as the named follow-up.

## 6. Chained state

Terminal node of the billy-old FM/FG→PD chain. Nothing auto-chains after this receipt. The P-D manuscript §8 kill/merge decision consumes this receipt per the frozen import map.

skills-applied: none (receipt, no manuscript content)
