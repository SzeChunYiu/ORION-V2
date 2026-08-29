# SD00 Receipt V1 — Reference Semantics and Blinding Preflight

**Executed:** 2026-08-29 · **Owner issue:** #50 · **Host:** LUNARC login node (project clone)
**Code state:** `b3e16f129bc24a705ac85eeaf9b0aa36b1f12bde` (origin/main, post-#36)
**Command:** `PYTHONPATH=src python3 scripts/run_scientific_development_reference.py --output sd00-reference.json`

## Terminal

```text
REFERENCE_SEMANTICS_CALIBRATION_ONLY
```

## Observed output (verbatim fields)

| Field | Value |
|---|---|
| `all_reference_checks_pass` | `true` |
| `checks.operator_discovery` | `true` |
| `checks.population_stays_noncausal_without_prospective_test` | `true` |
| `checks.higher_level_prospective_residual` | `true` |
| `checks.recursive_stability_is_bounded_terminal` | `true` |
| `authority.grants_scientific_truth` | `false` |
| `authority.grants_causal_law` | `false` |
| `authority.grants_recursive_ultimate_truth` | `false` |
| `schema_version` | `orion.v2.scientific-development-reference.v1` |

Output artifact sha256: `7dd0da44f0cae9822fc13c5fad23375816718629a2c318b9761297f8e37db4cb`

## Independent CI corroboration

The same reference script runs inside `wave6-scientific-development` CI, which was green on the
merged PR #36 head `0467ead` (18/18 checks, including `scientific-development`,
`scientific-development-sources`, `recursive-framework`). This receipt records an off-CI
execution at the post-merge main commit, confirming the calibration still holds at the exact
content now on main.

## Interpretation boundary

SD00 is software/reference validation only. It creates **no** scientific result, population
claim, causal law, or paper authority. Per the execution backlog it unblocks:

- **SD70** (fresh generated meta-policy benchmark; requires only SD00) — model-arm dispatch
  scheduled for 2026-09-03 evening on the model-account availability window; prepare/stub
  paths already CI-proven.
- **SD10** (population corpus + bias audit) — lawful multi-source adapters under construction
  on a separate branch/PR; not gated by SD00.

```text
SD00_STATUS = EXECUTED__CALIBRATION_ONLY
SD10_SD60_STATUS = OPEN_AWAITING_SD10_CORPUS
SD70_STATUS = UNBLOCKED__MODEL_DISPATCH_SCHEDULED_2026_09_03
SD80_SD90_STATUS = NOT_AUTHORIZED
```
