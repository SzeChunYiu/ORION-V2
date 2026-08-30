# AH10-R1 Terminal Receipt — Epistemic Atlas & Horizon Reference Semantics

**Stage:** AH10 (issue #108), run r1. **Status:** TERMINAL, GREEN — 10/10 unit tests passed.
**Executed:** 2026-08-30, billy-old (`~/sd10run/ORION-V2` reset to origin/main `5d873b1a`),
Python 3.14.4 / pytest 9.1.1 / typeguard 4.4.4, wall 0.07 s (`RUN.json`).

**Unit under verification:** `src/orion_v2/epistemic_atlas.py` (427 lines, `5b09a6a`),
suite `tests/unit/test_epistemic_atlas_wave6.py`. Protocol:
`research/experiments/EPISTEMIC_ATLAS_HORIZON_VERIFICATION_PROTOCOL_V1.md`.

## Required semantics — each is an explicit assertion, not implicit coverage

| Protocol requirement | Test that asserts it |
|---|---|
| compatible overlaps without global witness → `MATCHING_FAMILY_ONLY` | `test_pairwise_compatibility_does_not_self_grant_global_section` |
| incompatible overlap → `GLOBAL_SECTION_OBSTRUCTED` | `test_incompatible_overlap_is_a_local_to_global_obstruction` |
| separate global witness required for `GLOBAL_SECTION_WITNESSED` | `test_global_section_requires_a_separate_witness` |
| new probe may strictly refine the observational partition | `test_probe_expansion_can_strictly_refine_observational_horizon` |
| no empirical `ABSOLUTE_GLOBAL` claim state | `test_globality_ladder_has_no_empirical_absolute_global_level` (`"ABSOLUTE_GLOBAL" not in values`) |

Additional invariants held by the same suite: authority context is required on every
epistemic context; the probe table must be complete over the candidate-by-probe grid;
`OUTSIDE_CURRENT_ATLAS` is a witnessed sentinel, not an enumerated complement; G4
universality requires an explicit formal universe and theorem; atlas robustness requires
both transport and a hostile challenge.

## Verdict

`AH10_GREEN__REFERENCE_SEMANTICS_VERIFIED` — the integrated unit suite passes all
reference cases (`done_when` for AH10 in `EPISTEMIC_ATLAS_HORIZON_BACKLOG_V1.json`).
Pass count was cross-checked against the protocol's five required semantics test-by-test
(no semantics is green merely by suite aggregation).

## Consequences

- **AH20 unlocked** (its only dependency, AH10, is terminal). AH20 must reuse the EL10 /
  GR10 / MX20 exact worlds wherever identities and custody permit before creating any new
  case; `CANNOT_CHECK` and parent-sufficiency remain valid terminals.
- **AH30 stays closed** until AH20 shows protected incremental value beyond current
  K2/K4/K5 and the strongest parents.
- Non-claims (unchanged): `CURRENT_ATLAS != TOTAL_EPISTEMIC_SPACE`,
  `PAIRWISE_COMPATIBILITY != GLOBAL_SECTION`, `FORMAL_UNIVERSALITY != EMPIRICAL_ABSOLUTE_GLOBALITY`,
  `OUTSIDE_CURRENT_ATLAS != POSITIVE_MECHANISM_DISCOVERY`. This run grants no total
  epistemic space, no absolute globality, no new kernel family, no paper-endpoint change.
