# FORMAL_DISCOVERY_CAMPAIGN NULL RUN RECEIPT V1 (2026-08-29)

**Disposition: NULL RUN — no scientific content. Zero model calls reached a backend.
No accuracy in this run is a verdict, and none may be imported into any manuscript.**

## What was dispatched

`run_formal_discovery_campaign.sh all` on billy-old (`~/sd10run/ORION-V2`), plan
`research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json`, 14 studies
(FM10-FM60, FG10-FG80), 8 arms each, 640-1,280 tasks per study (~14k jobs total),
concurrency 4. The dispatch mechanics completed: private oracle removed during child
execution and restored hash-identical (`all_oracles_restored: true`), all child
return codes zero.

## What actually happened

Every arm invokes the model backend through `ORION_CODEX_BIN` (default `codex`).
`codex` is installed on billy-old at `/home/billy/.npm-global/bin/codex`
(0.129.0-alpha.15, the pinned version) but `~/.npm-global/bin` was not on PATH for
the campaign's non-interactive shell. Every job therefore failed in ~0.08 s with:

```json
{"status": "EXECUTION_FAILED_MODEL_RESPONSE",
 "answer": null,
 "reasoning_summary": "[Errno 2] No such file or directory: 'codex'",
 "resource_receipt": {"model_calls": 0}}
```

## The two defects (both fixed in this commit)

1. **Launcher environment**: the campaign had no absolute/`which`-resolved backend path.
   Fix for the re-dispatch: set `ORION_CODEX_BIN=/home/billy/.npm-global/bin/codex`
   explicitly. (Backend additionally requires a live codex auth on billy-old; the
   shared account session currently rotates on the Mac mini.)
2. **Evaluator masked the outage as data**: `evaluate()` scored `answer: null`
   responses as `correct: false` while counting `missing_or_invalid: 0`, so a total
   backend outage produced "accuracy 0.0, all arms, 0 missing" — indistinguishable
   from a legitimate all-wrong scientific result. Fix: null/`EXECUTION_FAILED*`
   responses and missing/unparseable response files now count as `missing_or_invalid`
   with an explicit row (`"missing": true`), each arm summary carries `run_valid`,
   the campaign summary carries `all_runs_valid`, and the driver exits `3` with a
   `CAMPAIGN INVALID` banner instead of returning success.

## Checker validation (fix verified against the real failure data)

Re-running the fixed evaluator over the null run produced exactly the truthful
reading: e.g. FG10 160/160 missing, FG20 120/120 missing, `run_valid: false`
everywhere, `all_runs_valid: false`, bare exit code 3. Unit tests added:
`test_execution_failed_responses_are_missing_not_wrong`,
`test_missing_response_files_are_reported_in_rows`
(`tests/unit/test_formal_discovery_generated_suite_wave6.py`).

## Preserved evidence

The full null run is preserved at
`.orion-formal-discovery-campaign-nullrun-20260829/` (untracked, 113 MB):
dispatch receipts, all `EXECUTION_FAILED*` responses, and the re-evaluated
(truthful) `EVALUATION_SUMMARY.json` per study. It is the ground-truth fixture for
the evaluator-truth fix.

## Re-dispatch condition

Re-run `all` with `--force --overwrite` into a fresh campaign root once the backend
is genuinely available (absolute `ORION_CODEX_BIN` + verified live auth, one-call
smoke test before launch). The frozen plan/suite is unchanged; the null run grants
nothing and revokes nothing.
