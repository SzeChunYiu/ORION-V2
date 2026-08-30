# Result Addendum to Demarcation Review Packet V2 — AH20-R2 Frozen Outcome

**Addendum date:** 2026-08-30
**Adds to:** `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V2.md` (`PACKET_VERSION = V2_PRE_AH20_OUTCOME`)
**Follows:** `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V2_RESULT_ADDENDUM_AH20_R1.md` (R1 terminal `CONTROL_DIVERGENT`, frozen, unedited)
**Status:** post-outcome addendum. The V2 pre-outcome questions remain frozen and are NOT
modified, reinterpreted or re-scored by this file. This addendum appends the AH20-R2
frozen outcome and asks whether it changes the reviewer's judgment; it does not rewrite
anything before it.

---

## A. What was run (freeze V2, supersede-disciplined)

- **Suite:** AH20-R2 (108 tasks × 5 arms = 540 jobs), frozen at
  `research/experiments/EPISTEMIC_ATLAS_HORIZON_AH20_SUITE_FREEZE_V2.md`, pre-registered
  BEFORE dispatch as a V2 supersede of V1 under V1's own provision. R1's frozen record
  and its `CONTROL_DIVERGENT` terminal stand unedited.
- **Composition:** 48 EL10 worlds reused byte-identical (unchanged from R1) + 60 fresh
  atlas/horizon worlds (AHC0–AHC4 × 12, seed 20260902).
- **Four registered repairs (why R2 is a new suite, not a re-score):**
  1. **Contract split** — the R1 failure field `holds_across_contexts` (one field serving
     scored warrant AND descriptive claim) became `holds_warranted_by_registered_evidence`
     (scored) + `proposal_global_scope_claimed` (descriptive, never scored).
  2. **Gluing scored on text-derivable classes only** (48 worlds with a chart/overlap
     registry in public text); the all-worlds rate retained as descriptive.
  3. **Pre-registered calibration block** — within-arm difference-in-differences
     (treatment-stratum overclaim rate − own AHC0 control rate), interface minus base,
     10 000 seeded within-task arm-label permutations; co-primary, non-promoting.
  4. **Power** — per-class count 6 → 12.
- **Integrity:** 540/540 returned, all returncodes zero, single executor
  (codex-cli `gpt-5.6-terra`), private oracle sha256-committed and unlinked during
  dispatch, restored hash-matched; every response stamped `orion.v2.ah20-response.v2`.
- **Receipt:** `research/experiments/results/issue108/ah20-r2/` (RECEIPT.md + frozen artifacts).

## B. Frozen outcome (terminal)

```text
AH20_R2_TERMINAL = INTERFACE_PROTECTED_RESIDUAL
```

Kill-rule walk in frozen order, every gate executed:

- K5 missing: 0/540. **Invariance sentinel: NOT FIRED** — all five arms return the
  scored control answer on 12/12 AHC0 tasks (R1: 1/6, 3/6, 3/6, 5/6, 5/6). The R1
  confound (wrapper-induced baseline divergence on the control) is removed by the
  contract split, not observed away.
- K3 non-compensatory: `false_globalization_rate` interface **0/42** (every base arm
  exactly 1/42); `false_outside_atlas_rate` **0/96** on every arm (exact CP 95% CI
  [0, 0.0377]).
- K1 cost: interface wall-time 0.971× the cheapest base arm (cap 1.10).
- K2 protected residual: interface **strictly better on two pre-registered critical
  point estimates** — `false_globalization_rate` 0.000 vs best-other 0.0238;
  `transport_correctness` 1.000 vs best-other 0.9722. One Holm-significant paired
  contrast: gluing vs SIMPLE_NATIVE **+13/−1, p_Holm 0.029**.
- Recorded against the interface: CURRENT_F0 leads gluing 0.875 vs 0.854 (one task at
  the derivable ceiling); the calibration DiD block reports the one-task overclaim and
  transport margins as individually non-significant (p_perm = 1.0) and cannot promote
  anything.
- **Registered defect, verdict-neutral, disclosed:** the ELC1 oracle's witness token
  (`full-envelope-sweep`) does not occur in the byte-identical EL10-reuse public text;
  all 30 arm-answers across five arms are CANNOT_CHECK/MATCHING (uniform ⇒ cancels in
  every paired test). Candidate R3 repair; not executed.

## C. Post-outcome questions for the reviewer (analogous to the R1 addendum's E-questions)

- **E1′.** Does a pre-registered repair suite that converts a `CONTROL_DIVERGENT`
  instrument null into a discriminating `INTERFACE_PROTECTED_RESIDUAL` — with the
  sentinel fixed at the contract level and every kill gate executed — meet the
  demarcation standard the packet set for "executed, not logged"?
- **E2′.** The protected residual rests on pre-registered point estimates plus ONE
  Holm-significant contrast; the calibration block honestly reports the remaining
  margins as underpowered. Is that honesty a strength of the claim or a limit of the
  evidence?
- **E3′.** CURRENT_F0 (strongest parent) sits within one gluing task of the interface
  at the derivable ceiling. Does the atlas/horizon interface's zero-false-globalization
  / perfect-transport / lower-cost profile justify "protected residual," or does
  parent-sufficiency remain the more parsimonious reading?
- **E4′.** The ELC1 witness-token defect is disclosed as arm-uniform and verdict-neutral.
  Does its disclosure change your confidence in the suite's custody and audit trail?

## D. What this outcome does NOT claim (unchanged)

No paper endpoint change (FLAGSHIP_V14 stands); no AH30; no naturalistic claim; no
absolute globality; no new kernel family; `INTERFACE_PROTECTED_RESIDUAL` is a
formal/interface discriminator verdict on 108 synthetic worlds, not deployment evidence;
the calibration block attributes but never promotes. R1's null remains the honest record
of the V1 instrument; R2 is its pre-registered repair, not its erasure.
