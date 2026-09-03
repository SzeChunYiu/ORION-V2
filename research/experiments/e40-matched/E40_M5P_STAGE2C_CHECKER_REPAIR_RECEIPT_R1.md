# E40-m5′ Stage-2c — checker repair R1 (control-gating), receipt

**What was broken.** `e40_m5p_stage2c_analysis.py::evaluate_gates()` read the runner's control
verdicts into the rollup under `controls_runner` but never **consumed** them, so it emitted the
routing terminal `E40_TERMINAL` while the registered planted positive control was FAILing
(terminal quality 0.6412, 0/8 cycles in the ≥0.8 basin). The m2/m3 runner gated on exactly this
(`e40_matched_runner_m3.py rollup()`: `controls_ok = planted PASS and nullcal PASS`). The defect
was disclosed in `E40_M5P_STAGE2C_OUTCOME_RECEIPT.md` §5 and the fix deferred to "the next
freeze"; this is that fix.

**What was NOT broken, and was not touched.** The planted control's 0.6412 is not a checker bug —
it is the checker correctly reporting that a seed-mandated arm cannot follow an informative
feedback channel on `glm-5.3` (Stage-2d measured this directly: `C_SEED_MANDATE` 0.0233 vs
`A_NO_MANDATE` 0.9877). The plant, its quality function, the PASS rule, the cycle count and every
gate threshold are **unchanged**. Making a failing control pass would be outcome tuning and is
forbidden by Stage-2c design §9.

## The repair

`evaluate_gates(ct, rho, strata, controls)` now takes the control verdicts as a **mandatory**
argument and refuses to file a routing disposition when they do not hold. Three statuses, never
conflated:

| control state | disposition | exit |
|---|---|---|
| all registered controls PASS | the registered routing, unchanged | 0 |
| any registered control FAIL | `CHECKER_INVALID__NO_VERDICT` | **4** |
| any registered control absent / verdictless | `CONTROLS_UNAVAILABLE__NO_VERDICT` | **5** |

"Could not check" therefore has its own exit code and its own disposition; it is never reported as
"checked and fine". The computed G-values are still **reported** when a verdict is voided — the
repair removes their routing force, it does not hide them. The null-calibration harness, which has
no real controls by construction, passes a named `SYNTHETIC_CONTROLS_OK` sentinel; `None` never
falls through as a pass.

## Validation (against the REAL archived campaign, not only fixtures)

Replaying the archived Stage-2c contrasts, ρ and strata through the repaired checker:

| controls supplied | disposition | admissible |
|---|---|---|
| the real archived verdicts (planted **FAIL**, nullcal PASS) | **`CHECKER_INVALID__NO_VERDICT`** | False |
| **no-alarm twin** — same numbers, planted PASS | `E40_TERMINAL` | True |
| planted absent | `CONTROLS_UNAVAILABLE__NO_VERDICT` | False |
| nullcal FAIL instead | `CHECKER_INVALID__NO_VERDICT` | False |

and the five computed gate values are **identical** to the frozen run
(G0 pass, G1 fail, G2 fail, G3 pass, G4 fail) — the repair changes routing, never arithmetic.

The no-alarm row is part of the standard: a checker that fires on a clean run is as broken as one
that never fires. A mutation test confirms the guard has teeth — reverting the repair
(`admissible = True`) makes 5 of the new tests plus the end-to-end selftest fail; the no-alarm test
correctly keeps passing.

Regression coverage: `tests/unit/test_e40_m5p_stage2c.py` (+7 tests, all against the archived
artifacts, with a guard test that fails loudly if the archive moves so the suite cannot go
vacuous) and three new `selftest` fixtures inside the analysis itself.

## What the repair does and does not change

- **It does not unblock closure.** A repaired checker run against the same data returns
  `CHECKER_INVALID__NO_VERDICT` — precisely the disposition the Stage-2c receipt already applied by
  hand. The receipt's reading is now what the code produces.
- **The frozen artifacts stand as produced.** `rollup-m5p-stage2c/E40_M5P_STAGE2C_ROLLUP_V1.json`
  is unmodified (sha256 `b9266001db3851def4d6bffd0ee3ebd2c9090400fd749a8706b110eaaf6e1a7c`), and
  `DISPOSITION_SUPERSEDED.md` continues to govern any programmatic read of its
  `gates.disposition`. The frozen analysis was **not** re-run over the archived campaign.
- The script sha256 recorded in the Stage-2c outcome receipt
  (`bb11b95316c383e0bb34c070a06dd756385208ef5407efb6476c1ac43ea8ea11`) refers to the version that
  produced those artifacts and remains the correct custody record for them; this repair changes the
  script going forward, and git preserves the pre-repair version.
