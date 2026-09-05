# ME-X6 V4 — outcome receipt: the typed prior is worth exactly the coverage gap, and coverage is channel movement, not lone-carrier exercise

```text
ME_X6_V4_STATUS  = PROTECTED_RUN_COMPLETE
ROUTE            = TYPING_VALUE_EQUALS_COVERAGE_GAP__COMOVEMENT_RECOVERS_SOME_STRATA
n                = 1800 (18 strata x 2 scales x 50), all 36 cells exercised
M                = 1800/1800
B8_D0..D8 refit  = 1100 / 1200 / 1400 / 1600 / 1800 of 1800  (coverage 0/8 .. 8/8)
M − refit        = 350+350 / 300+300 / 200+200 / 100+100 / 0+0 per scale = exactly 50 x (zero-weight unexercised strata) x 2 scales
G1 tie on exercised strata (LIVE) = PASS at every coverage level, both scales, 0 discordant
CHANGES_ME_X6_V1_V2_V3 = NONE   GRANTS = nothing
```

**Design (frozen before the run):** `ME_X6_V4_COVERAGE_LIMITED_REGIME_DESIGN_V1.json` sha256 `d911e9a8610ffea776e32c6a57a5373f829d8c58bc250542c7795a8ea7eb644d`
(PR #337); development fit `ME_X6_V4_DEVELOPMENT_FIT_V1.json` sha256 `050035a6385b223cbb6c8afb11cfc8d0f91335bc5c7bf2480a23073bc4832d1d` (D_8 == V3's frozen refit: known answer, PASS).
**Authorization:** minted from the operator's standing verbatim authorization (2026-09-02; reaffirmed 2026-09-04), coordinator-written and says so; consumed, archived
as `PROTECTED_RUN_AUTHORIZATION_USED_V1.json`. **Run:** LUNARC `lu48` job **3579602**, clone `310a02f`, `.venv` CPython 3.13.5; selftest PASS and a 72-instance
development rehearsal in the same job before the stage; executed once. **Seed revealed:** `ME-X6-V4-PROTECTED-24b4a2af7ddf6742cdf69102d73e4b2a` (hashes to the commitment). Protected split
digest `13957efe860f675c378c3a45d95c89919af2b18a96d0bb212ef2363b6b26c562`. **Results:** `results/ME_X6_V4_PROTECTED_RESULTS_V1.json` sha256 `c18a02a4b741c055dab696a865d4f506a19776bf0bdec0ca63718e2d5ef5d1f6`; transfer LUNARC → billy-old → Mac, md5 `40889332…` both ends.

## 1. The coverage curve

| coverage k | tie on exercised strata (live) | zero-weight unexercised strata (by construction) | co-movement cells (live) | refit correct |
|---|---|---|---|---:|
| 0/8 | True | 7 strata → M ahead by 350 + 350 | {'D0:X6I7_ONE_BREAKTHROUGH|SCALE_PROBLEM_FAMILY': 'TIE', 'D0:X6I7_ONE_BREAKTHROUGH|SCALE_SUBFIELD': 'TIE'} | 1100/1800 |
| 2/8 | True | 6 strata → M ahead by 300 + 300 | — | 1200/1800 |
| 4/8 | True | 4 strata → M ahead by 200 + 200 | — | 1400/1800 |
| 6/8 | True | 2 strata → M ahead by 100 + 100 | — | 1600/1800 |
| 8/8 | True | 0 strata → M ahead by 0 + 0 | — | 1800/1800 |

Every number on the curve is the arithmetic of the gap: 50 instances per stratum per scale, one stratum lost per zeroed role. The refit
never wins an instance M loses (M is exact on all 1800: G0d live on the four V3 strata).

## 2. Reading, at its strength

1. **Typing separates *only* where the untyped learner had no coverage, and there it separates completely.** At every coverage level the
   refit ties M on every stratum it was fitted on (0 discordant, both scales — the live gate), and loses every instance of every stratum whose
   only mover it zeroed. There is no partial credit and no leakage in either direction.
2. **Coverage is channel movement, not lone-carrier exercise — `CORRECTED` against V3's reading.** The one live unexercised case fired as a
   tie: fitted on `D_0`, whose strata never exercise `formal_artifacts` alone, the greedy refit still carried that channel (it co-moves inside
   GAIN/LOSS/I4) and read the `X6I7_ONE_BREAKTHROUGH` stratum 100/100 on both scales. V3 counted `formal_artifacts` among the roles V1
   "exercised as a lone carrier"; V4 shows the lone-carrier condition is sufficient but not necessary — a role reached through co-movement is
   covered. The coverage gap that typing insures against is therefore *roles absent from every trajectory the learner saw*, which is a
   smaller set than the lone-carrier census implied.
3. **What typing is, sharpened once more.** V3: a coverage prior. V4: a coverage prior whose value on a protected population is exactly
   `50 x 2 x (roles absent from the fit data)` — measurable, monotone, and zero at full coverage. It carries no information about any stratum
   the learner has seen, at any coverage level. That is the strength at which the flagship may quote it, and no higher.
4. **Saturation status (V3 §6) is unchanged:** matched on information, capacity and coverage, the tie returns; V4 adds the regime in which
   the prior *does* show and measures it as arithmetic. No further V on this generator is warranted; a different world would be a new study.

## 3. Gates

All hard gates PASS; G1 (live) PASS 5/5 coverage levels x 2 scales; G2 (by construction, disclosed) PASS; G2b co-movement cells: 2 ties, 0 M-ahead,
0 refit-ahead; G3 curve non-increasing and zero at k = 8. Selftest: both planted failures fired (a tie violation on an exercised stratum; a tie on a
zero-weight gap stratum → `LANE_DEFECT`). Unit tests `tests/unit/test_me_x6_v4_coverage_limited.py` 3/3 with V3's 9/9 on billy-old.

Authority: grants nothing — no field status, no novelty, no manuscript change; ME-X6 V1/V2/V3 unchanged. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

skills-applied: none (outcome receipt, no manuscript content)
