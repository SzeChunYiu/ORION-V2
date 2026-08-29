# E70-GC1 R1 result stub (dispatch-time state)

- **Status: DISPATCH_QUEUED_DEFERRED_ACCOUNT_WALL** — no outcomes yet.
- Deferred SLURM job **3553088** (`--begin=2026-09-04T08:00:00`), lu48, 2 cpus,
  8G, 24h. The only available codex account is server-stated usage-walled until
  Sep 3rd, 2026 6:26 PM; the job probes availability in-loop before dispatching.
- **Per-arm results: CANNOT_CHECK** for all four arms (SIMPLE_DIRECT,
  SAME_MODEL_REFLECTION, F0_PARENT_FEDERATION, F2_ORION_METABOLIC_FULL).
  Reason: zero model responses exist at receipt time; evaluation is executed by
  the same deferred job after generation completes. This is a checked-nothing-yet
  state, not a negative or positive result.
- Infra fixes applied this run: python 3.13.5 venv (3.12.3 bare-LD fix),
  codex 0.150.1 provision (0.129.0-alpha.15 cannot decode the current models
  registry), deferred dispatch + probe-retry guard. Full detail:
  `INFRASTRUCTURE_RECEIPT.md`.
- **Before the job fires**: re-sync `codex-home/auth.json` from the Mac
  (see INFRASTRUCTURE_RECEIPT.md section 4). Without it the job exits 3 at probe
  exhaustion and the pilot never runs.
- When the job completes, outcomes land in the workdir
  (`EXECUTION_SUMMARY.md`, per-arm metrics) and this file is superseded by the
  terminal result receipt under a new run-identity entry.
