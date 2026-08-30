# AH20-R2 outcome receipt (issue #108)

**Terminal: `INTERFACE_PROTECTED_RESIDUAL`** — first non-null AH20 terminal (R1:
`CONTROL_DIVERGENT`; its frozen record at `../ah20-r1/` stands unedited).

## 1. Run identity and custody

| field | value |
|---|---|
| Suite | AH20-R2, freeze V2 (PR #120, squash-fe9c380) superseding V1 under its own provision |
| Composition | 108 tasks = 48 byte-identical EL10 reuse + 60 fresh (5 classes × 12, seed 20260902) |
| Jobs | 540 (108 × 5 arms), concurrency 5, **all returncodes zero**, `missing_or_invalid` 0 on every arm |
| Executor | codex-cli `gpt-5.6-terra` (billy-old, `ORION_AH_TIMEOUT=1800`), all 540 responses schema `orion.v2.ah20-response.v2` |
| Custody | private oracle sha256 `e1f1a842e6ca82c59f68590023f636813de33c90a266c51d6aef3a83d04fe9ed`, unlinked before dispatch, `oracle_restored_hash_match: true` |
| Wall time | interface 1478 s vs base arms 1523–1594 s |

**Scoring-code note (transparency).** Verdict assembly required a one-token fix to
`_kill_rule` (PR #124): the INTERFACE branch tested the aggregate
`other_matches_or_beat_all` instead of the loop-local `other_matches_or_beats`, so
`others_match_or_beat_interface_on_all_critical` could never flip via metric
comparison. The bug is a dormant V1 defect — R1 terminated at the sentinel and never
executed this branch — and it NameError'd on first real execution here. The identical
one-token patch was applied to the executor clone before evaluation; after #124 merged,
evaluation was re-run from `origin/main` and produced an identical verdict. No task,
arm, metric, oracle value, or kill-rule order changed.

## 2. Kill-rule walk (order per freeze V2 §6)

| stage | result |
|---|---|
| K5 missing | 0/540 missing or invalid — pass |
| Invariance sentinel (CONTROL_DIVERGENT) | **not fired**: all five arms return `holds_warranted_by_registered_evidence=false` on 12/12 AHC0 control tasks (R1: 1/6, 3/6, 3/6, 5/6, 5/6). Repair 1 (contract split) removed the R1 failure cell. |
| K3 non-compensatory | `false_globalization_rate` interface **0/42** (every base arm exactly 1/42); `false_outside_atlas_rate` **0/96** on every arm, exact CP 95% CI [0, 0.0377] — pass |
| K1 cost | interface wall-time ratio vs cheapest other **0.971** (cap 1.10) — pass |
| K2 protected residual | interface **strictly better on two critical point estimates**: `false_globalization_rate` 0.0 vs best-other 0.0238; `transport_correctness` 1.0 vs best-other 0.9722 |
| Terminal | `INTERFACE_PROTECTED_RESIDUAL` (`other_strictly_better`: CURRENT_F0 on gluing 0.875 vs 0.854 — recorded, does not override) |

## 3. Per-arm critical-metric table (n = 108 per arm)

| metric (dir, denominator) | SIMPLE_NATIVE | CURRENT_F0 | CURRENT_F2 | PARENT_LOCAL_GLOBAL | F2_PLUS_ATLAS_HORIZON |
|---|---|---|---|---|---|
| false_globalization_rate (↓, 42) | 0.0238 | 0.0238 | 0.0238 | 0.0238 | **0.0000** |
| false_outside_atlas_rate (↓, 96) | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| gluing_disposition_correctness (↑, 48) | 0.6042 | **0.8750** | 0.6875 | 0.8542 | 0.8542 |
| transport_correctness (↑, 36) | 0.9722 | 0.9722 | 0.9722 | 0.9722 | **1.0000** |
| probe_selection_correctness (↑, 24) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| decision_relevant_partition_refinement (↑, 24) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| local_scope_correctness (↑, 18) | 0.6667 | 0.6667 | 0.6667 | 0.6667 | 0.6667 |
| gluing all-worlds (R1-comparable, descriptive) | 0.2870 | 0.6019 | 0.3056 | 0.4444 | 0.3796 |

## 4. Paired statistics (exact McNemar ×16, Holm α=0.05)

- **One Holm-significant contrast:** gluing vs SIMPLE_NATIVE **+13/−1, p_exact 0.0018,
  p_Holm 0.0293** — the interface strictly beats the unwrapped arm on text-derivable
  gluing dispositions.
- Gluing vs CURRENT_F2: +9/−1, p_exact 0.0215, p_Holm 0.322 (survives raw, not Holm).
- Gluing vs CURRENT_F0 (+0/−1) and vs PARENT_LOCAL_GLOBAL (+1/−1): p 1.0 (F0's one-task
  gluing edge and the tie with the OED/gluing parent stand).
- `false_globalization` (+1/−0 vs each base) and `transport` (+1/−0 vs each base):
  p 1.0 — point estimates favor the interface; individually underpowered at these
  near-ceiling rates (honest reading: directionally consistent, not separately
  certified). Probe: all ties.

## 5. Pre-registered calibration block (repair 3; co-primary, non-promoting)

Within-arm DiD (overclaim rate on false-globalization strata − own AHC0 control rate),
interface minus base, 10 000 seeded within-task arm-label swaps (seed 20260902):

| base | base ctrl (n=12) | base treat (n=42) | iface ctrl | iface treat | DiD | p (two-sided) |
|---|---|---|---|---|---|---|
| SIMPLE_NATIVE / CURRENT_F0 / CURRENT_F2 / PARENT_LOCAL_GLOBAL (identical) | 0.000 | 0.0238 | 0.000 | 0.0000 | **−0.0238** | 1.0 |

No arm — interface or base — inflates global claims relative to its own control
(control rates all 0/12). The interface's false-globalization advantage is a one-task
margin over each base at the point-estimate level; the calibration block reports its
non-significance rather than claiming it. It does not relax the kill rule and cannot
promote the interface.

## 6. ELC1 structural finding (registered defect of the freeze; arm-uniform)

The ELC1 oracle requires `gluing_disposition=GLOBAL_SECTION_WITNESSED` with witness id
`full-envelope-sweep`; that token does **not occur** in the 1,356-char byte-identical
EL10-reuse public text. Result: **30/30 arm-task answers are CANNOT_CHECK (26) or
MATCHING_FAMILY_ONLY (4); no arm, including the atlas interface arm, ever emits the
witness id.** Arms do extract the derivable part — `holds_warranted_by_registered_
evidence=true` on ELC1 at 17/18 across arms — so the failure is text-derivability of
the witness token, not comprehension.

Consequences, all arm-uniform and therefore verdict-neutral (concordant cells cancel in
every paired test): `local_scope_correctness` is capped at 12/18 for every arm (all five
observe exactly 0.6667); every arm loses the same 6 gluing cells, so
`gluing_disposition_correctness` measures the 42 derivable cells (CURRENT_F0's 0.875 =
42/48 is the derivable ceiling). Candidate R3 repair, **not executed** (no further
re-instrumentation without a new freeze): register the witness token in the ELC1 text,
or split ELC1's gluing requirement into its derivable component. The R2 terminal stands.

## 7. What this run licenses (non-claims carried from freeze V2 §7)

Formal/interface discriminator only, on 108 synthetic worlds. No paper endpoint change
(FLAGSHIP_V14 stands); AH30 stays gated; `INTERFACE_PROTECTED_RESIDUAL` is a kill-rule
verdict on pre-registered point estimates plus one Holm-significant paired contrast —
not deployment evidence, not naturalistic claim, not absolute globality, no new kernel
family. Parent sufficiency (CURRENT_F0 within one gluing task of the interface at the
derivable ceiling) remains a valid reading of this run; the honest statement is that the
atlas/horizon interface **earned a protected residual** (zero false globalizations,
perfect transport rejection, Holm-significant gluing gain over the unwrapped arm) at 0.97×
the base arms' wall-time cost.

## 8. Artifacts

`DISPATCH_RECEIPT.json` (540 jobs, all rc 0), `EVALUATION_SUMMARY.json` (verdict,
per-arm metrics, McNemar ×16, calibration block), `PER_TASK_SCORING.json` (oracle +
per-task per-arm indicators), `FROZEN_SUITE.json` (freeze v2 identity), 
`PRIVATE_ORACLE_COMMITMENT.json` (sha256 e1f1a842…), `public_tasks.json` (108 public
scenarios).
