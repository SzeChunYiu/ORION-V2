# E20 R4 native BugsInPy pilot execution summary

## Frozen identity

- Source commit: `582a125aa80660229fa6f29da4f5263645d62c0d`
- LUNARC campaign: `/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e20-r4-native-r1`
- Setup job: `3551053`
- Native evaluation array: `3551054_[0-11%6]`
- After-any rollup job: `3551055`
- Model proposal generator: `gpt-5.6-terra`
- Registered design: four arms by three pandas BugsInPy tasks

All jobs completed with Slurm exit code `0:0`. Response schema validation passed
for all 12 proposals. Fresh evaluation workspaces matched their expected buggy
commits, and the evaluator did not read gold or fixed-patch content.

## Native registered-test result

| Arm | Native successes | Tasks | Rate | Patch-apply failures |
| --- | ---: | ---: | ---: | ---: |
| `F0_PARENT_FEDERATION` | 1 | 3 | 0.333 | 2 |
| `F2_ORION_METABOLIC_FULL` | 1 | 3 | 0.333 | 2 |
| `SAME_MODEL_REFLECTION` | 2 | 3 | 0.667 | 1 |
| `SIMPLE_DIRECT` | 2 | 3 | 0.667 | 1 |

Across all arms, 6/12 proposals passed the registered native tests and 6/12
failed during patch application. No evaluation was classified as an
infrastructure error. Every successful evaluation used Python 3.8.20, compiled
successfully, imported the evaluated workspace, found 41 native pandas
extensions, and returned native test status 0.

Registered paired comparisons were underpowered (`n=3` tasks). F2 tied F0 in
success rate (risk difference 0.000, bootstrap 95% CI [-1.000, 1.000], exact
discordant p=1.0). F2 was below both SIMPLE and reflection by 0.333 in observed
success rate (bootstrap 95% CI [-1.000, 1.000], exact discordant p=1.0 for each).
These observations are retained without protocol retuning.

## Authority boundary

This is an `E20_INFRASTRUCTURE_PILOT_ONLY` result. It does not establish ORION
superiority, field status, publication readiness, or acceptance. The full
regression suite was not run and remains `CANNOT_CHECK_NOT_RUN`. Component
effects are `CANNOT_CHECK_UNDERPOWERED` because the corresponding removal arms
were not part of this four-arm pilot.

## Integrity hashes

- `work/aggregate/E20_R4_NATIVE_ROLLUP.json`: `b2a7cf68cc526bcf1071cba2690b7dfca2e15ed1bb88cb575697a30aff05fcfc`
- `work/aggregate/analysis.json`: `211a1c0caca8ca89139b89095498cfd4cf1b69e029dcc0ee7e97c63141ad27fe`
- The complete archived file manifest is `SHA256SUMS`.
