# FG80 R3 — dispatch deviation record V1 (freeze deviation: executed ~18h34m before the registered start)

**Written:** 2026-09-06, *while the run was still in flight*, so that the deviation is durable in the committed
record independently of the outcome. A frozen run that executed ahead of its registered start whose only evidence
of that is an untracked log file on a laptop is the worst possible pairing: an outcome that later reads as though
it ran exactly as registered. `CLASS = FREEZE_DEVIATION__DISPATCH_TIME_ONLY`. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. What deviated

| | registered | actual |
|---|---|---|
| dispatch start | `START_EPOCH` = **2026-09-07 16:25** (Europe/Stockholm), `fg80_r3_deferred_dispatch.sh` | **2026-09-06T21:51:18+02:00** |
| delta | — | **18 h 33 m 42 s early** |
| dispatcher | armed daemon pid 1751039, sleeping on `START_EPOCH` | killed **by PID** 2026-09-06T19:50:58Z; run driven by `fg80_r3_execute_now.sh` pid 1847954 |
| host | billy-old | billy-old (unchanged) |

The armed dispatcher was killed by PID (never `pkill -f`) specifically so that it could not wake at 16:25 and
produce a duplicate `evaluate` pass over the same responses.

## 2. Why

The run is **channel-dependent**, and its registered deferral is to *the channel window*, not to a calendar date:
the design's state was `FROZEN__DISPATCH_DEFERRED_TO_THE_CHANNEL_WINDOW (~2026-09-07)`. The channel opened early.

On 2026-09-06 the codex channel on billy-old was returning HTTP 401 `token_revoked` /
`refresh_token_invalidated` — a dead login, not a cap. A direct refresh against the OAuth token endpoint returned
the same `refresh_token_invalidated`, confirming the credential was revoked rather than rate-limited. The account
(`232c8b04-b3a9-4952-b9b4-80cecf4dc747`) was **unchanged**; billy-old simply held a refresh token that had been
rotated out by a later refresh elsewhere. `~/.codex/auth.json` was re-synced from the Mac's copy of the *same
account* (backup kept at `~/.codex/auth.json.bak-20260906-lane-pa-pb-pf`; md5 `546f032ec169affa8842f2f886a073f5`
verified identical on both sides after transfer), after which `codex exec --model gpt-5.6-terra` answered
`CHANNEL_OK`. The frozen suite was then dispatched rather than left waiting for a clock.

## 3. What did NOT change

Nothing in the registered design was altered. Verbatim, the invariants:

- **design** — `FG80_R3_INTERFACE_RERUN_DESIGN_V1.md/.json`, unamended
- **seed** — `20260904`
- **arms** — all five: `TARGET_ONLY_DIRECT`, `STRONGEST_DOMAIN_FORMAL_PARENT`, `F0_PARENT_FEDERATION`,
  `F2_STATIC_NO_FORMAL_DISCOVERY`, `F2_FORMAL_DISCOVERY_FULL`
- **registered dispatches** — `400` (80 tasks × 5 arms)
- **ceiling row** — registered unchanged as
  `FG80_AT_CEILING_UNDER_A_CATEGORICAL_CONTRACT__NO_DYNAMIC_RANGE_FOR_THE_P_F_TRIGGER` (row 1: both ≥ 0.90 and
  p > 0.05), α = 0.05, ceiling = 0.90
- **channel / model pin** — `--channel codex --pin gpt-5.6-terra`, as armed
- **command** — byte-identical to the dispatcher's own post-wait line:
  `python3 fg80_r3.py run --workdir .fg80-r3-run --channel codex --pin gpt-5.6-terra --max-concurrency 3`

**The deviation is the dispatch time and nothing else.** Had any of the above changed, that would be a different
and much larger disclosure than this one.

## 4. Head SHA at arming vs at execution

A reader cannot check this after the fact, so it is recorded:

| | commit |
|---|---|
| head when the dispatcher was **armed** (2026-09-04) | `d6eda4c9e3667f5b2ece0882499a0da0472cd582` |
| head the run **executed** against | `308531e36a6c3034853fedde7474bd9c81c2f1c3` |

48 commits separate them. Within `research/experiments/fg80-r3` the two trees differ by **exactly one added
documentation file** (`FG80_R3_PRE_DISPATCH_RECEIPT_V1.md`, +114 lines); every executable and design blob is
byte-identical across the interval:

```
fg80_r3.py                        af7b5f4d720b6bb6290271343ee901824f184faf   IDENTICAL
FG80_R3_FROZEN_SUITE_V1.json      adb7c4dd7619853cf6dd05ff2dfed34ac844e983   IDENTICAL
FG80_R3_INTERFACE_RERUN_DESIGN_V1.json  6a641d9414ed848c765033bf660ca150e1725548   IDENTICAL
FG80_R3_INTERFACE_RERUN_DESIGN_V1.md    5173bfe9ca18a256e52969910f87592ff417aa41   IDENTICAL
FG80_R2_RENDERING_CENSUS_V1.json  0f23ffda6382bca028e3dc98f22de4500319203f   IDENTICAL
```

## 5. Custody actually observed at dispatch

- run-dir artifacts match the freeze commitment: `private_oracle.json` sha256
  `b219f0e0f6c18e5818a05a261bce1313fae6f902639d894b33300008ae67d5fa`, `public_tasks.json`
  `3e7b7319160d3e088a41d08ef4dd3813baf90d9acc0df9994c3525ef5c0adc61` — both equal to the values recorded inside
  `FROZEN_SUITE.json`, which the executor re-checks and aborts on;
- the private oracle was **removed before dispatch**, leaving `PRIVATE_ORACLE_COMMITMENT.json`
  (`private_removed_before_dispatch: true`); no arm workspace could see it;
- `fg80_r3.py selftest` was run immediately before dispatch: **0 failures**, including the ceiling route and the
  design-twin check that seed / n_tasks / arms / treatment / parent / α / ceiling agree with the script.

## 6. Served model

The codex CLI does not expose a served model id; the executor records this honestly per response as
`served_model: null`, `served_model_source: NOT_EXPOSED_BY_CODEX_CLI__HEADER_IS_REQUEST_ECHO`,
`requested_model: gpt-5.6-terra`. The requested pin is therefore **not** an assertion that gpt-5.6-terra served
the run, and no outcome from it may be reported as if it were.

```text
FG80_R3_DISPATCH = EXECUTED_EARLY__FREEZE_DEVIATION_DISPATCH_TIME_ONLY
  registered START_EPOCH 2026-09-07 16:25 -> actual 2026-09-06T21:51:18+02:00 (18h33m42s early)
  reason: channel-dependent deferral; channel opened early after a revoked-refresh-token repair (same account)
  UNCHANGED: design, seed 20260904, five arms, 400 dispatches, ceiling row, alpha, channel/pin, command
  armed head d6eda4c -> exec head 308531e; fg80-r3 executable+design blobs byte-identical
  SERVED_MODEL = NOT_EXPOSED_BY_CODEX_CLI (requested gpt-5.6-terra; not asserted as served)
```

skills-applied: none (evidence lane, no manuscript content)
