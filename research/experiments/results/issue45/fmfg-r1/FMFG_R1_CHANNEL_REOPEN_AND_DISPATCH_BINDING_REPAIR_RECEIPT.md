# FM/FG R1 + PD Campaign: Codex Channel Reopen + Dispatch Binding Repair Receipt

**Receipt ID:** `FMFG_R1_CHANNEL_REOPEN_AND_DISPATCH_BINDING_REPAIR_RECEIPT`
**Date (executed):** 2026-08-30
**Runs governed:** FM/FG generated suite (`.orion-formal-discovery-suite`, 560 dispatches)
and PD dependence-evidence campaign (S1–S4, 4440 jobs), both on billy-old
`~/sd10run/ORION-V2` (driver `~/sd10run/fmfg_pd_driver_20260830.sh`, PID 2354300).
**Scientific status:** NONE — execution-state and repair record only. No results, no
evaluation, no claims. PROSPECTIVE.

## 1. Channel reopen (~4 days ahead of the assumed Sep 3–4 window)

The FM/FG→PD lane was gated on the Sep 3–4 model-channel availability window (same
window class as SD70/E70-GC1/R11). On 2026-08-30 the channel was probed directly and
found open, so the lane launched immediately instead of waiting:

1. **Dead auth diagnosed, not a channel wall.** billy-old codex failed with
   "refresh token was already used" + websocket 401s — a copied-credential rotation
   kill, not availability. Heal: archived `~/.codex/auth.json.dead-20260830`,
   transferred the Mac's live `auth.json` (single-active-consumer discipline kept:
   Mac codex stays off while billy-old consumes). Probe returned a normal completion.
2. **Model-gate cleared with the pin preserved.** `gpt-5.6-terra` is rejected by the
   pinned CLI (`0.129.0-alpha.15`, HTTP 400 "requires a newer version of Codex").
   Side-by-side install `~/.npm-terra` (`codex-cli 0.147.0`) selected via
   `ORION_CODEX_BIN`; the canonical pin `~/.npm-global` remains
   `0.129.0-alpha.15`, untouched — this is a documented exception for the terra
   model only.

## 2. Defect found and fixed: strict output-schema dispatch binding (PR #77)

First live dispatch failed **55/55** (`EXECUTION_FAILED_MODEL_RESPONSE`,
`model_calls 0`, ~8 s each). Manual single-arm reproduction exposed the true error —
not a network/auth problem:

```
invalid_request_error invalid_json_schema: In context=('properties', 'answer'),
'additionalProperties' is required to be supplied and to be false.
(param text.format.schema, status 400)
```

The backend now enforces strict mode on `--output-schema`: every object must declare
`additionalProperties: false`. The free-form per-task `answer` object cannot satisfy
that by construction.

**Repair** (merged `722bc09df4a150887146357d1df70feabd829521`, PR #77, both
`scripts/orion_formal_discovery_arms.py` and `scripts/orion_pd_arms.py`):

- `answer` travels as a **JSON-encoded string** on the wire (strict-compliant scalar);
  the runner decodes it back to an object before the `answer_contract` check.
  Response envelopes and evaluator semantics unchanged.
- `answer_encoding_instruction(contract)` injects a **contract-derived worked example**
  into the prompt — without it the model echoes the contract's shape placeholders
  (`"array-item"`) as keys; with it, real data returns.

**Validated on real data before relaunch, on BOTH runners:** FM/FG single arm →
`COMPLETED_PROPOSAL_ONLY` with concrete values (`{"minimal_feature_ids": [……]}`);
PD `P_D_FULL` single arm → same. CI foundation check `formal-generated-suite` green
before merge.

## 3. Poisoned-workdir purge + determinism proof

The 55 failed response files would have been preserved forever by dispatch-skip
resume. Purged `rm -rf` + re-`prepare`. Determinism of the regeneration proven by
hash equality (byte-identical private oracle vs the committed value):

| Artifact | sha256 |
|---|---|
| `FROZEN_SUITE.json` | `d680c358ad4113125ffdb6e19cb8c3126c1da038613bdf501b887baecb564090` |
| `public_tasks.json` | `0d48bbf6246a9f3670979ea521500417950ddcdf064138423aff2b376aa87fb6` |
| `private_oracle.json` (regenerated == committed) | `3cc97cf2134ab9f558cf15b308cd9cf67e0aa9dc3279425b406301e73cdd9cc9` |

Oracle discipline unchanged: hash-committed, removed during dispatch, restored in
`finally`.

## 4. Launch state (verified live)

- Driver chain: FM/FG prepare (14 studies × 5 arms × 8 tasks = 560) → dispatch
  `--max-concurrency 2` → evaluate → `run_dependence_evidence_campaign.sh all`
  (S1 1440 + S2 960 + S3 960 + S4 1080). Log:
  `~/sd10run/logs-fmfg/driver-20260830T024302.log`.
- Census at T+10 min: **134/560 responses, 134 `COMPLETED_PROPOSAL_ONLY`, 0
  failures**; driver process alive. Every response so far carries a decoded,
  contract-conformant answer.

## 5. Next actions

- On suite completion: fetch `EVALUATION_SUMMARY.json`, assert `run_valid`
  (failures == 0), results receipt PR, then imports per
  `RECURSIVE_DEVELOPMENT_RESULT_IMPORT_MAP_V1.json` (P-B, P-A first).
- On PD completion: fetch `CAMPAIGN_ANALYSIS_SUMMARY.json` /
  `CAMPAIGN_STATUS.json`, results receipt PR, P-D §8 kill/merge decision.
- Monitor cadence: every 2 h; resume rule = rerun dispatch only (never `prepare
  --force` on a live workdir — it rmtree's the resumable state).

skills-applied: none (receipt, no manuscript content)
