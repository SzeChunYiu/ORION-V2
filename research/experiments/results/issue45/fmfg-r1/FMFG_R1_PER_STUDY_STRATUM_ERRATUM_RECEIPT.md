# FM/FG R1 Per-Study Stratum Erratum Receipt

**Receipt ID:** `FMFG_R1_PER_STUDY_STRATUM_ERRATUM_RECEIPT`
**Date (corrected):** 2026-08-30
**Corrects:** `FMFG_R1_SUITE_TERMINAL_RESULTS_RECEIPT` (per-study stratum bookkeeping) and
its downstream record `FMFG_R1_GENERATED_SUITE_PAPER_INTERPRETATION_V1` (ORION-paper
`_portfolio/claims/`).
**Trigger:** recomputation from `EVALUATION_ROWS.json` during the P-A manuscript V4
import pass (ORION-paper PR #9). Per-feed-subset paired statistics failed to reconcile
at FM20.

**Scope:** analysis-layer stratum bookkeeping only. The frozen suite, oracle custody,
dispatch receipt, evaluated arm table, all primary paired comparisons and all authority
grants are **unchanged**. `grants_F2_superiority` remains **false**.

## 1. Provenance of the correction

Recomputed directly from `EVALUATION_ROWS.json` (campaign artifact; mirror sha256
`51affd36…351`): 560 rows, 112 tasks/arm, 0 duplicate `(task_id, arm)` pairs, per-arm
correct totals reproduce `EVALUATION_SUMMARY.json` exactly (TARGET 100, STATIC 100,
F2_FULL 99, PARENT 98, F0 97). Verified per-study × per-arm matrix (correct tasks of 8):

| Study | F0 | F2_FULL | F2_STATIC | PARENT | TARGET |
|---|---|---|---|---|---|
| FG10 | 8 | 8 | 8 | 8 | 8 |
| FG20 | 8 | 8 | 8 | 8 | 8 |
| FG30 | 8 | 8 | 8 | 8 | 7 |
| FG40 | 8 | 8 | 8 | 8 | 8 |
| FG50 | 7 | 6 | 8 | 8 | 8 |
| FG60 | 8 | 7 | 8 | 8 | 8 |
| FG70 | 7 | 7 | 7 | 7 | 8 |
| FG80 | 4 | 6 | 4 | 4 | 6 |
| FM10 | 8 | 8 | 8 | 8 | 8 |
| FM20 | 6 | 8 | 8 | **6** | 7 |
| FM30 | 6 | 6 | 6 | 6 | 5 |
| FM40 | 8 | 8 | 8 | 8 | 8 |
| FM50 | 8 | 8 | 8 | 8 | 8 |
| FM60 | 3 | 3 | 3 | 3 | 3 |

Column sums: F0 97, F2_FULL 99, F2_STATIC 100, PARENT 98, TARGET 100 — equal to the
terminal receipt's arm table.

## 2. Corrections

1. **Terminal receipt `ties_at_ceiling_8_of_8` (JSON) and §3 (MD).** FG70 was listed as
   an 8/8 ceiling tie; it is a **7/7 tie** (F2_FULL 7, F2_STATIC 7, all formal arms 7,
   TARGET 8). True 8/8-ceiling ties: FM10, FM20, FM40, FM50, FG10, FG20, FG30, FG40 —
   **8 studies, not 9**. The ties count (11), the FG80 win (+2) and the FG50/FG60
   losses are unchanged.
2. **Paper-interpretation record FM20 row, PARENT column.** Recorded as 8; truth is **6**.
   FM20 truth: F0 6/8, F2_FULL 8/8, F2_STATIC 8/8, PARENT 6/8, TARGET 7/8. The FM20
   signal is a **parent-routing loss** (both parent arms 6/8 vs F2/STATIC 8/8), not a
   federation-specific loss.

## 3. Interpretation impact

- FM20 attribution shifts from "federation uniquely negative" to "both parent arms below
  the method's static configuration". Federation is **not** uniquely defective on FM20.
- The aggregate statement survives: F0 remains the weakest arm overall (97/112 vs PARENT
  98/112). "Federation weakest in aggregate" stands; "federation uniquely negative at
  FM20" does not.
- FG70 is a near-ceiling study (formal arms 7/8, direct control 8/8), not an 8/8 study.

## 4. Paper impact

| Paper | Status |
|---|---|
| P-B V4 (merged `57eae38`) | Audited **unaffected**: FM20 is not in P-B's feed; its FG80 (6 vs 4) and ceiling ("eleven of fourteen … most often at the task ceiling") sentences verify against the corrected matrix. |
| P-A V4 (PR #9, open) | Amended before merge: anti-unification sentence, federation-attribution prose, subset paired statistics, terminal enum. |
| P-C / FLAGSHIP / P-F | Pending imports must cite the verified matrix in this receipt. |

skills-applied: none (evidence-custody erratum record, no manuscript prose)
