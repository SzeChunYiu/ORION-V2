# H-EXT-1 Reconnaissance Receipt (2026-09-02)

What the P-D generated suite is, what is archived, and what a fresh-seed run costs. Every
line below was checked against the live artifact named in it.

## Generator and strata

- `scripts/run_dependence_evidence_generated_suite.py` — four studies, 520 tasks, strata
  recorded only in the private oracle: PD-S1 (160; A dependent-corroboration via a shared
  calibration convention stated in `method_text`, B genuine-independent, C provenance-visible
  duplicates sharing `lineage_root`/`replay_hash`, D insufficient evidence), PD-S2 (120;
  argument/adequacy defects), PD-S3 (120; revocation/objection uptake), PD-S4 (120;
  authority/response). Task ids are neutral per-study ordinals assigned by a seeded shuffle.
- Deterministic: `prepare` on the registered plan (seed 20260903) regenerated on the Mac
  reproduces `public_tasks.json` and `private_oracle.json` byte-for-byte for all four
  studies (sha256 equal to `CAMPAIGN_FREEZE_MANIFEST.json`, checked 2026-09-02).
- Evidence records arms can see: PD-S1 `items`, PD-S2 `evidence`, PD-S3 revocation `items`,
  PD-S4 authority `evidence_items`; each carries `item_id, lineage_root, source_type,
  method_text, replay_hash` (+ optional `declared_overlap`). PD-S3 objection tasks and PD-S4
  response tasks carry no evidence records.

## Arms

- Model arms (`codex exec --ephemeral`, one call per task, JSON output schema):
  `P_D_FULL`, `P_D_MINUS_DEPENDENCE`, `STRONGEST_ASSURANCE_FEDERATION`,
  `ROBUSTNESS_TRIANGULATION_PARENT` (S1), `PERFORMATIVE_SECURITY_PARENT` (S4). They differ
  only in the arm-procedure paragraph of the prompt (`scripts/orion_pd_arms.py`).
- Offline deterministic arms (`model_calls: 0`): counting, provenance, meta-analysis,
  argument acceptability, simple control — constructed calibration ceilings, not empirical.
- The H-EXT-1 contrast `M = P_D_FULL` vs `OFF = P_D_MINUS_DEPENDENCE` is therefore a model
  contrast: every gated evaluation needs archived or fresh model outputs.

## Frozen run (PD R1, 2026-08-30, billy-old)

- Archived at `billy-old:/home/billy/sd10run/ORION-V2/.orion-dependence-evidence-campaign`
  (39 MB): per study `public_tasks.json`, `private_oracle.json`, `EVALUATION_ROWS.json`
  (per task × arm: `correct`, `expected`, `actual`), `responses/<arm>/<task>.json`
  (with `resource_receipt.wall_time_seconds`, model `gpt-5.6-terra`). 4,440/4,440
  `COMPLETED_PROPOSAL_ONLY`; all oracles restored.
- Repo copy (`research/experiments/results/issue50/pd/`) holds only aggregates; the
  per-instance rows needed for a paired gated analysis were pulled from billy-old for this
  study and are archived compactly under `research/experiments/h-ext1/data/`.
- Per-stratum accuracies (FULL / MINUS / SAF): S1 A 1.000/0.000/1.000, B 1.000/1.000/0.950,
  C 0.975/0.000/1.000, D 0.925/1.000/1.000; S2 D 0.933/1.000/0.933 (others 1.0);
  S3 all 1.0; S4 B 0.767/1.000/0.933 (others 1.0). Mean wall time per call ≈ 7.7–7.8 s for
  all three arms (520 responses each).

## Fresh-seed cost

- 520 tasks × 3 arms (`P_D_FULL`, `P_D_MINUS_DEPENDENCE`, `STRONGEST_ASSURANCE_FEDERATION`)
  = 1,560 codex calls. Observed throughput on billy-old at concurrency 3 with gpt-5.5:
  ≈10 responses/min → ≈2.5 h wall.
- Substrate constraint: under the pinned codex `0.129.0-alpha.15` the backend rejects
  `gpt-5.6-terra` ("requires a newer version of Codex", HTTP 400, probed 2026-09-02);
  `gpt-5.5` answers (`PROBE_OK`). The prospective cell therefore runs on gpt-5.5 and is a
  new evaluation identity on both seed and model; the design records this before results.
- Executed on billy-old (not the Mac mini, not CI): plan
  `research/experiments/h-ext1/H_EXT1_PROSPECTIVE_PLAN_V1.json` (seed 20260902),
  campaign root `/home/billy/hext1-prospective`, same suite scripts as origin/main
  (sha256 of the three scripts identical between billy-old's checkout `b528ff2` and
  `origin/main` `7507dfd`, verified two ways).

skills-applied: none (receipt, no manuscript content)
