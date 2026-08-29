# P-D dependence-evidence campaign — offline-only smoke receipt (2026-08-29)

## What ran

`ORION_PD_OFFLINE_ONLY=1 bash scripts/run_dependence_evidence_campaign.sh all`
on billy-old, campaign root `.orion-dependence-evidence-campaign-smoke-20260829`
(dedicated smoke root; the real run uses a fresh root). Wall ≈2 min: all four studies
prepared → dispatched → evaluated → analyzed; 520 tasks; 4440 offline jobs across arms.

This is the design's required smoke step (PD_DECISIVE_STUDY_DESIGN_V1 §9:
smoke → full dispatch), executed before the real model-arm dispatch. Zero model calls.

## Machinery verified

- **Oracle integrity**: per-study `private_oracle.json` hash-committed
  (`PRIVATE_ORACLE_COMMITMENT.json`), absent for the entire child dispatch, restored
  with `oracle_restored_hash_match: true` in all four studies; `all_returncodes_zero`,
  `all_oracles_restored`, `all_dispatches_zero` (see CAMPAIGN_DISPATCH_RECEIPT.json).
- **Truth gates (PR #72 semantics)**: model arms (`P_D_FULL`, `P_D_MINUS_DEPENDENCE`,
  `STRONGEST_ASSURANCE_FEDERATION`, `ROBUSTNESS_TRIANGULATION_PARENT`,
  `PERFORMATIVE_SECURITY_PARENT`) come back all-missing with `run_valid: false` —
  the campaign terminates `CAMPAIGN INVALID` (single verdict line in the driver log);
  a null run never renders as accuracy-0.0 verdicts.
- **Offline arms**: every deterministic arm answered all tasks (`missing=0`,
  `run_valid=true`) — the deterministic-arm router (`orion_pd_arms.py`) is wired and
  schema-correct on all four request types.

## Constructed-rate consistency (offline arms are calibration quantities, not discoveries)

- **PD-S1**: `CURRENT_INDEPENDENT_COUNTING`/`ARGUMENT_ACCEPTABILITY` — false-corroboration
  rate 1.0 on S1a (planted shared latent source), preservation 1.0 on S1b, wrong on S1c
  (duplicate votes), correct INCONCLUSIVE on S1d. `PROVENANCE_TRACKING` /
  `STANDARD_DEPENDENCE_META_ANALYSIS` 0.75 (catch S1c by lineage dedup).
- **PD-S2**: `ARGUMENT_ACCEPTABILITY` exactly 2/4 strata (right on formally-defective +
  clean control; blind to false-premise/strict-export/component-gap and test-inadequacy).
- **PD-S4**: naive offline arms authorize on the no-root stratum (`false_authority_rate`
  1.0) and are right only on the conditional-authorization stratum (0.25);
  `SIMPLE_DIRECT_CONTROL` = the over-conservative ceiling — never authorizes
  (`false_authority_rate` 0.0) but never emits the required enum (0/120).

Every constructed rate lands where PD_DECISIVE_STUDY_DESIGN_V1 §3–§4 says it must.
Strata correctness here is a generator/oracle consistency check, not an empirical result
(offline parents' failure rates are constructed by design; §10).

## Copied artifacts

CAMPAIGN_STATUS.json, CAMPAIGN_DISPATCH_RECEIPT.json, CAMPAIGN_EVALUATION_SUMMARY.json,
CAMPAIGN_ANALYSIS_SUMMARY.json (offline arms; model arms all-missing). Per-study
`private_oracle.json` deliberately NOT copied — the commitment file is the public
artifact. Smoke root retained on billy-old.

## Verdict

PIPELINE_SMOKE_VALID — the real model-arm dispatch (chained launch, codex backend)
is de-risked. No results; no authority of any kind is granted by this receipt.
