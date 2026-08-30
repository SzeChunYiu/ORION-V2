# AH20 Suite Freeze V2 (R2 repair suite)

**Status:** V2 FROZEN (pre-registered 2026-08-30, BEFORE any R2 dispatch).
**Supersedes:** `EPISTEMIC_ATLAS_HORIZON_AH20_SUITE_FREEZE_V1.md` under V1's own provision
("any change … before dispatch requires a V2 supersede — not an edit"). V1 remains the
frozen authority for the R1 run; R1's outcome record
(`research/experiments/results/issue108/ah20-r1/`, terminal `CONTROL_DIVERGENT`) is
**preserved unedited**. R2 is a NEW suite with its own pre-registration — not a post-hoc
re-scoring of R1 responses and not an oracle patch of executed material.

**Canonical paper anchor:** FLAGSHIP_V14 (unchanged). No paper endpoint changes; no AH30;
R1's null and every parent win stand exactly as recorded.

## 0. Why R2 exists (R1 diagnosis, from the frozen receipt)

R1 terminated `CONTROL_DIVERGENT`: the five arms disagreed on the AHC0 control
(local_scope signatures 1/6, 3/6, 3/6, 5/6, 5/6). Three mechanisms, each now repaired:

- **D1 (contract ambiguity).** Every AHC0 failure was the same cell: decision correct,
  `holds_across_contexts=true` over-claimed, while the same answer correctly returned
  `transport_verdict=INVALID` — an internal contradiction caused by one field having to
  serve two roles (what the proposal claims vs what the registry warrants).
- **D2 (representation floor).** Gluing was scored over all 78 worlds, but the reused EL10
  stratum and the probe worlds expose no chart/overlap registry in public text; the
  text-faithful answer there (`CANNOT_CHECK`) was scored wrong, capping text-faithful
  arms at ~30/78 regardless of interface quality.
- **D3 (power + attribution).** 6 control tasks per class give the sentinel and the
  paired tests almost no power; and with arms diverging on the control itself, between-arm
  level differences are confounded — nothing in R1 could attribute overclaiming to an arm.

## 1. The four repairs (frozen)

1. **Contract split (fixes D1).** `holds_across_contexts` is replaced by two fields:
   - `holds_warranted_by_registered_evidence` (SCORED) — "IGNORING what any proposal,
     review or report in the scenario claims: do the REGISTERED facts themselves warrant
     reading the finding you rely on as holding across ALL values of the registered
     coordinates?"
   - `proposal_global_scope_claimed` (DESCRIPTIVE, never scored) — does the scenario's
     proposal text itself claim global scope?
   Oracle values: warranted=True only on ELC1 (registered full-envelope witness); False
   everywhere else. claimed=True on AHC0, AHC1 and all 48 reused ELC worlds (their texts
   carry explicit global-scope transport proposals); False on AHC2/AHC3/AHC4 (no
   global-scope claim in those texts).
2. **Gluing scored on text-derivable classes only (fixes D2).**
   `gluing_disposition_correctness` denominator = `GLUING_SCORED_CLASSES` =
   {AHC0, AHC1, AHC4, ELC1, ELC7} = **48** — exactly the worlds whose scenario text
   contains a chart/overlap/witness registry. ELC2–ELC6/ELC8 (obstruction needs
   overlap-registry facts absent from the reused texts) and AHC2/AHC3 (no chart registry)
   are honestly excluded. The all-worlds rate is retained as the descriptive
   `gluing_reference_all_worlds_r1_comparable` for R1 comparability. The R1 executed
   oracle is NOT edited.
3. **Pre-registered calibration block (fixes D3 attribution).** Co-primary analysis,
   registered here BEFORE the run: for each base arm, the within-arm difference-in-
   differences — (overclaim rate on the false-globalization strata) − (same arm's AHC0
   control overclaim rate) — contrasted interface − base; two-sided p by seeded
   within-task arm-label swaps (10 000 permutations, seed 20260902). A wrapper that
   inflates global claims should raise its treatment-minus-control gap relative to the
   base arms; this cancels arm-level baseline differences by construction. The block is
   emitted regardless of sentinel state and is the run's evidential content if the
   sentinel fires. **It does not relax the kill rule and cannot promote the interface.**
4. **Power (fixes D3 power).** Fresh per-class count 6 → **12** (60 fresh worlds; suite
   108 tasks; 540 jobs), new AH seed **20260902**. EL10 reuse stays 48, byte-identical
   under EL10's own seed 20260830.

## 2. Suite composition (108 tasks)

48 reused EL10 worlds (byte-identical, unchanged from R1) + 60 fresh AH worlds
(5 classes × 12, seed 20260902, same generators, same domain dressing, same machine
cross-checks against the AH10-green `src/orion_v2/epistemic_atlas.py`). Public texts
carry no class ids, no enum values, no contract field names.

## 3. Arms — carried from V1 verbatim

SIMPLE_NATIVE; CURRENT_F0; CURRENT_F2; PARENT_LOCAL_GLOBAL; F2_PLUS_ATLAS_HORIZON.
Same solver, same payload, wrapper-only difference; single executor per run
(codex-cli `gpt-5.6-terra` primary, whole-suite anthropic fallback rule unchanged).

## 4. Runner and custody — carried from V1

Same `scripts/run_epistemic_atlas_suite.py` mechanics: oracle sha256-commit → unlink →
`ORION_GOLD_ACCESS=NONE` / `ORION_OUTCOME_ACCESS=NONE` → restore + hash-assert; missing ≠
wrong; GR10/MX20 deferred-slot ledger re-checked at prepare AND dispatch. Schema stamps
bump to `.v2` (request/public/private/freeze/evaluation/response) so R1 and R2 artifacts
can never be silently mixed.

## 5. Metrics and statistical treatment (frozen)

| metric | definition (denominator) | critical |
|---|---|---|
| `local_scope_correctness` | correct stay-local decision + no warranted-global claim, over AHC0 (12) + ELC1 (6) = 18 | no |
| `false_globalization_rate` | warranted-global claim (or WITNESSED, or VALID transport-to-global) against a local oracle, over AHC1 (12) + ELC2–5, ELC8 (30) = 42 | **yes (non-compensatory)** |
| `gluing_disposition_correctness` | exact disposition + witness discipline over GLUING_SCORED_CLASSES = AHC0, AHC1, AHC4, ELC1, ELC7 = 48 (repair 2) | yes |
| `gluing_reference_all_worlds_r1_comparable` | same over all 108 — descriptive only | no |
| `transport_correctness` | 1 − P(VALID \| oracle INVALID) over ELC2–5, ELC7, ELC8 = 36 | yes |
| `probe_selection_correctness` | correct ADOPT/REJECT + probe id over AHC2 + AHC3 = 24 | yes |
| `decision_relevant_partition_refinement` | over AHC2 + AHC3 = 24 | no |
| `false_outside_atlas_rate` | P(OUTSIDE_CURRENT_ATLAS \| registered explanation exists) over the 96 non-sentinel tasks | **yes (non-compensatory)** |
| `resource_cost` | model_calls, tokens, wall-time | gate only |
| `calibration_analysis` | within-arm DiD overclaim contrasts, 4 bases, permutation null (repair 3) | co-primary, non-promoting |

Statistics: paired exact McNemar × 16 (4 metrics × 4 bases; gluing indicators restricted
to GLUING_SCORED_CLASSES), single family, Holm step-down α=0.05 — unchanged from V1
except denominators. `false_outside_atlas_rate` point estimate + exact Clopper–Pearson
95% CI, kill rule on point estimates (unchanged). Missing ≠ wrong (unchanged).

## 6. Kill rules — carried from V1 verbatim, order unchanged

K5 missing → **invariance sentinel (CONTROL_DIVERGENT)** → K3 non-compensatory → K1 cost
→ K2 protected residual → K4 null → `INTERFACE_NULL__CRITICAL_METRIC_TIES`. The sentinel
is NOT relaxed by R2: if arms still disagree on AHC0, the run is again reported
CONTROL_DIVERGENT and carries no interface evidence — but this time the pre-registered
calibration block (repair 3) is computed and reported as the run's evidential content,
and repair 1 removes the known field-level ambiguity from the control's failure cell.

## 7. What this freeze does NOT claim (carried from V1)

No total epistemic space; no absolute globality; no global sheaf structure assumed; no
K7 / new kernel family; no P-A/P-B/P-D endpoint change; `OUTSIDE_CURRENT_ATLAS` carries
no positive mechanism content; pairwise compatibility never promotes to a global section;
sheaf/cohomology language is parent-owned with zero ORION novelty credit; AH20-R2 is a
formal/interface discriminator only and licenses no naturalistic claim (AH30 stays
gated); parent sufficiency and CANNOT_CHECK are valid terminals; results bind only the
108 synthetic worlds run; the calibration block cannot promote the interface, only
attribute overclaiming.

## 8. Supersede discipline (what V2 does not touch)

Arms and wrappers (V1 §3), custody mechanics (V1 §4), kill-rule order (V1 §6), authority
non-claims (V1 §7), executor pinning (V1 §8.6), EL10 byte-identical reuse, and all R1
artifacts. R1's `CONTROL_DIVERGENT` verdict, its receipt, and the V2 demarcation packet
addendum remain the frozen record of that run. If R2 also terminates CONTROL_DIVERGENT,
the honest terminal is again recorded — with the calibration block as content — and no
further re-instrumentation is authorized without a new freeze and a new supersede record.
