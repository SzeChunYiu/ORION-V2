# FM/FG R2 Registered-Scale Dispatch Receipt (prospective)

**Lane:** `FM_FG_GENERATED_EXACT_CAMPAIGN` (owner issue #48)
**Registered plan:** `research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json`
**Dispatch started:** 2026-08-30T08:09:49+02:00 (billy-old, `~/sd10run/logs-fmfg/driver-r2-20260830T080949.log`)
**Status at freeze of this receipt:** RUNNING (class 1 of 4)

## Why R2 exists (the registered-scale gap)

R1 (receipt `fmfg-r1/FMFG_R1_SUITE_TERMINAL_RESULTS_RECEIPT.md`, PR #79) executed
**8 tasks/study = 112 tasks × 5 arms = 560 dispatches** — a pilot, not the registered
campaign. The registered plan's per-study minimums are materially larger:

| Class | Studies (per-study) | Tasks | Dispatches |
|---|---|---|---|
| n80 | FG80 (80) | 80 | 400 |
| n96 | FM30, FM50 (96) | 192 | 960 |
| n120 | FM10, FM20, FM40, FM60, FG20, FG40, FG50, FG60 (120) | 960 | 4,800 |
| n160 | FG10, FG30, FG70 (160) | 480 | 2,400 |
| **Total** | 14 studies | **1,712** | **8,560** |

R1's aggregate null (TARGET_ONLY_DIRECT 0.8929 = F2_STATIC 0.8929 > F2_FULL 0.8839 >
STRONGEST_PARENT 0.8750 > F0 0.8661, 11/14 studies tied at ceiling) was a pilot-scale
statement; the registered counts are the pre-declared evidence base for the lane.
This receipt records the dispatch binding before any outcome is read.

## Execution binding (frozen at dispatch)

- **Runner:** `scripts/run_formal_discovery_generated_suite.py` (same as R1; one
  `--per-study` value per invocation → 4 size-class workdirs).
- **Workdirs:** `.orion-fmfg-r2-n80`, `.orion-fmfg-r2-n96`, `.orion-fmfg-r2-n120`,
  `.orion-fmfg-r2-n160` under `~/sd10run/ORION-V2` (billy-old).
- **Seed:** `20260829` (plan seed) for every class; generators + arm set frozen by the plan.
- **Arms (verified in FROZEN_SUITE at n80):** TARGET_ONLY_DIRECT,
  STRONGEST_DOMAIN_FORMAL_PARENT, F0_PARENT_FEDERATION,
  F2_STATIC_NO_FORMAL_DISCOVERY, F2_FORMAL_DISCOVERY_FULL.
- **Concurrency:** `dispatch --max-concurrency 2`.
- **Model lane:** `ORION_CODEX_BIN=$HOME/.npm-terra/bin/codex` (0.147.0 side-by-side;
  canonical repo pin 0.129.0-alpha.15 untouched), `ORION_CODEX_MODEL=gpt-5.6-terra`,
  `ORION_FORMAL_TIMEOUT=1800`.
- **Driver:** `~/sd10run/fmfg_r2_registered_scale_driver.sh` (md5
  `04155f08967cc3919e74ebac979c87f5`, byte-verified against the authored copy).

## Oracle rule (verified before dispatch)

`PRIVATE_ORACLE_COMMITMENT.json` present in the workdir with keys
`{private_removed_before_dispatch, sha256}` — private oracle answers hash-committed and
absent from disk throughout every child/model dispatch, per the lane's registered rule.

## Custody note (launch repair, no outcome impact)

The first driver copy was corrupted at creation (unquoted remote heredoc expanded
`$LOGDIR`/`$STAMP`/function locals at write time); under `set -euo pipefail` it exited
at `mkdir -p ""` **before** any prepare/dispatch — no partial campaign state was created.
The driver was rewritten offline, scp'd, byte-verified (md5 match), and relaunched. R2
workdirs are all fresh; no R1 artifact was reused or mutated.

## Schedule and next artifact

At the observed R1 rate (~8.6 s/dispatch, concurrency 2) the full 8,560-dispatch
campaign is ~11 h: n80 ≈ 48 min → n96 ≈ 1.9 h → n120 ≈ 5.7 h → n160 ≈ 2.9 h.
Each class runs `prepare → dispatch → evaluate` sequentially in one driver process.
Terminal artifact: per-class evaluate outputs + a suite terminal results receipt
(success counts by arm × study, stratum analysis at registered counts, tie/ceiling
accounting), PR'd on completion.

## Boundary inheritance

Same as R1: formal generated-task success-resource outcomes only. No naturalistic
transfer claim, no critical-failure/safety endpoint, no field-status or
publication-readiness grant (authority block false in all machine outputs).

skills-applied: none (dispatch receipt, no manuscript content)
