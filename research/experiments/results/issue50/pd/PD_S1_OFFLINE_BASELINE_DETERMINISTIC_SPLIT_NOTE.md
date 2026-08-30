# PD-S1 offline-baseline deterministic split — diagnosis note (no defect)

**Question raised (2026-08-30 review):** PD-S1 shows a suspicious 0.0/1.0 accuracy
split by stratum (PDS1A 0/40, PDS1C 0/40, PDS1B/D 40/40 for two offline arms) —
zero variance in every cell. Artifact or finding?

**Verdict: by construction, correctly labeled in the shipped receipt. No repair needed.**

## Mechanism (root cause)

PD-S1 strata are keyed to evidence-item count and dependence structure
(`run_dependence_evidence_generated_suite.py`, `gen_pds1a..d`):

| Stratum | Items | Structure | Correct answer |
|---|---|---|---|
| PDS1A | 4 | latent-assumption dependence (items 3-4 adopt item 1's calibration convention) | INCONCLUSIVE, count 2 |
| PDS1B | 3 | genuinely independent (positive control) | ACCEPT_H, count 3 |
| PDS1C | 4 | provenance-visible duplicates (2 lineage roots, labeled dups) | INCONCLUSIVE, count 2 |
| PDS1D | 2 | insufficient-evidence baseline | INCONCLUSIVE, count 2 |

The 0/40 and 40/40 cells belong to the **offline constructed arms** (listed under
`offline_constructed` in `PD_R1_CAMPAIGN_TERMINAL_RESULTS_RECEIPT.json`), which are
fixed decision rules, not stochastic model dispatches:

- `CURRENT_INDEPENDENT_COUNTING` counts every item as an independent family:
  count=4 on A → ACCEPT (false corroboration, 0/40); count=3 on B → ACCEPT (40/40);
  count=4 on C → ACCEPT (0/40); count=2 on D → INCONCLUSIVE (40/40). Exactly the
  observed 0/1/0/1.
- `PROVENANCE_TRACKING` dedups by lineage root: 4 distinct roots on A → ACCEPT (0/40);
  3 on B → correct; **2 distinct roots on C** (duplicates share roots) → INCONCLUSIVE
  (40/40 — the C asymmetry); 2 on D → correct. Exactly the observed 0/1/1/1.

Zero variance is therefore the deterministic signature of fixed policies against an
item-count-keyed design — expected, not anomalous.

## Custody of the claim

- The shipped terminal receipt already labels these arms `offline_constructed`, carries
  the analysis note "offline parent rates are constructed calibration ceilings; only
  model arms carry empirical content", and the caveat "constructed practice baselines
  collapse (0.000-0.750); not compute-matched, no superiority license".
- The empirical S1 finding lives in the **model arms**: P_D_FULL 0.975 aggregate with
  dependence-sensitive strata A/C ≈ 1.000, vs P_D_MINUS_DEPENDENCE 0.500 aggregate with
  A/C = 0.000 — the registered ablation, unaffected by this note.

Diagnosis run read-only against the frozen campaign workdir
(`.orion-dependence-evidence-campaign`, billy-old) and the registered plan
`DEPENDENCE_EVIDENCE_GENERATED_CAMPAIGN_PLAN_V1.json`.

skills-applied: none (diagnosis note, no manuscript content)
