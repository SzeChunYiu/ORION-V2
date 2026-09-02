# E40-m5′ Stage-2c — Seed-Replica Stability Probe: dispatch receipt V1 (2026-09-02)

**Campaign:** `campaign-e40-m5p-stage2c` (LUNARC `/projects/hep/fs9/users/scyiu/orion-v2-e45/`),
exp_ids **504000–504239** (240 native `gies` runs): 48 F2 seed-replica chains
(12 cells × `f2r0`..`f2r3`, 4 cycles) + **12 in-campaign F0 federation chains** (4 upfront runs each).
Design frozen BEFORE any run: `E40_M5P_STAGE2C_SEED_REPLICA_PROBE_DESIGN_V1.{md,json}`.
**Supersedes Stage-2b V1** (PR #139, merged main `0cb33488`, **never run**: 0 chains, 0 native runs,
0 outcome data — see §2).

## 1. Frozen artifacts (sha256)

| artifact | sha256 |
|---|---|
| `E40_M5P_STAGE2C_SEED_REPLICA_PROBE_DESIGN_V1.md` | `8f578922459d8cdc8d118197f464ba6691b865b8ec71d35c57640f07a8afe78c` |
| `E40_M5P_STAGE2C_SEED_REPLICA_PROBE_DESIGN_V1.json` | `edb3bd2879b46e328be02ed0525794d594ae82fc7c6fd05851f185b0fc3e14bb` |
| `scripts/e40_matched_runner_m5p_stage2c.py` | `092a62819c86fb659c6a59af04b23376a5978523b828b2fc57c22a4b35d54271` |
| `research/experiments/e40-matched/e40_m5p_stage2c_analysis.py` | `bb11b95316c383e0bb34c070a06dd756385208ef5407efb6476c1ac43ea8ea11` |
| `tests/unit/test_e40_m5p_stage2c.py` | `f88ef7a6834cb70aa7084145a8df17ee431506ba8b7f00c7874c7df25e7a763f` |
| `sbatch/e40_m5p_stage2c_chain_r1.sbatch` | `9a64af97108158ad295cd9e9abd34b93e08b433db258a60646bf20012463bf8e` |
| `sbatch/e40_m5p_stage2c_eval_r1.sbatch` | `b8cc3701aeb6163f7e8221ffaab34bae74271bf934e89801311fdd7ad66ac182` |

## 2. The blocking finding: silent model substitution on the E60 lane

**Evidence (probed from LUNARC 2026-09-02, `~/.orion-campaign.env` → `https://api.z.ai/api/anthropic`).**
Four requests, HTTP 200 each, reading the `model` field of the response body:

| requested | served |
|---|---|
| `glm-5.2` (the frozen env value) | **`glm-5.3`** |
| `glm-5.3` | `glm-5.3` |
| `glm-5.1` | **`glm-5.3`** |
| `glm-4.6` | **`glm-5.3-flash`** |

No response field, header or status code announces the substitution. A full realistic decision call
(the Stage-2b cycle-1 `f2r0` prompt, temperature 0) returned served `glm-5.3`, 578 in / 114 out
tokens, a well-formed config obeying the seed mandate on the first ask — the decision path works,
it is simply a different model.

**Why this blocks Stage-2b:** the frozen m2 F0 chains that Stage-2b reused read-only were produced
on 2026-08-30. `~/.orion-campaign.env` on LUNARC has mtime **2026-08-24** and reads
`ANTHROPIC_MODEL=glm-5.2`, so the *requested* string then was the same one that is silently
substituted today; the *served* model then is unknown. m2/m3 logged prompt/response sha256 and token
counts only: a search over all **1,810** files under `campaign-e40-m2` + `campaign-e40-m3` and the
campaign logs finds **no served model id anywhere** (`grep -rIl "glm"` → no hits). The reference
model is therefore **unrecoverable from artifacts**, and every requested id tested is substituted, so
it cannot be re-requested either.

Running Stage-2b as frozen would have contrasted F2 chains produced by one model against F0 chains
produced by another — a second, unregistered delta in a probe whose entire claim rests on a single
delta. The array was held before it could start (`scontrol hold 3563453`).

### 2.1 Options evaluated

| option | verdict |
|---|---|
| (a) new prospective identity re-running BOTH arms on one served model | **TAKEN** — see §3 |
| (b) keep frozen F0, register the model change as a confound | **REJECTED.** Both the validity gate (G0: drag present under TERMINAL) and the decision gate (G2: consensus shipping closes the drag) are F0-vs-F2 contrasts. A model delta living only in the F2 arm makes a G2 pass unattributable (probe vs newer proposer) and a G0 failure uninterpretable. A single-delta probe cannot carry a second delta in the arm it is measuring |
| (c) pin the exact earlier model at some provider | **REJECTED ON EVIDENCE.** Every requested id is substituted (table above); no second provider is configured anywhere (`ANTHROPIC_*` only, on LUNARC and billy-old); and the earlier served id was never recorded, so even a hypothetical provider could not be verified to serve it |
| (d) `CANNOT_CHECK__SUBSTRATE_MODEL_UNRECOVERABLE` | **not needed** — (a) is available and cheap; (d) would be the route only if re-running F0 were impossible |

## 3. Resolution (Stage-2c), and what it costs

- **D1 — F0 re-run in-campaign.** 12 federation chains × 4 upfront configs = **48 additional native
  runs** (+12 decision calls), prompt byte-identical to the m2/m3 `f0_prompt` (unit-tested over all
  12 cells). Campaign grows 192 → **240 native runs** (+25 %), 48 → **60 chains**; wall grows from
  ≈2 h to ≈2.5 h at `%8`. Both arms are now produced by one served model: the single delta (the
  cycle-1 seed mandate) is restored.
- **D2 — the pinned quantity is the SERVED id.** `SERVED_MODEL = "glm-5.3"`; `assert_served_model`
  runs on **every** response (runner, fail-closed → `ChainCannotCheck`, chain recorded/excluded/
  counted), and the analysis re-checks every used chain's logged call ids, marking any chain with a
  foreign id — or with **no** served-model record at all — CANNOT_CHECK. A mid-campaign swap can no
  longer be absorbed silently by either the run or the analysis.
- **D3 — own identity:** `campaign-e40-m5p-stage2c`, exp_ids 504000–504239 (Stage-2b's 503000 block
  retired unused).
- **Historical panel:** every contrast is also computed against the frozen m2 F0 bests and reported
  under `historical_m2_f0_panel_nongating`, labelled cross-model; no gate, route or claim may cite it.
- **Unchanged (no outcome tuning):** question, probe statistic, seed table, gates and thresholds,
  permutation seeds/draws, routing, controls, leakage rule, substrate pins, cell grid, call mechanics.
  The re-freeze is legitimate only because it happened with **zero** campaign data in existence; the
  design records that no comparable change may be made after any run.

## 4. Validation (all executed before the freeze)

| check | result |
|---|---|
| runner `selftest` (validator, regime canon, perm p, numbering 60 chains / 240 disjoint exp_ids, seed mandate re-ask + exhaustion + non-binding at cycle ≥2, served-model pin, F0 prompt, leakage asserts) | 0 failures (Mac + LUNARC) |
| analysis `selftest` full battery through `main()` | 0 failures (Mac + LUNARC) |
| planted fixture (in-campaign F0) | G0–G4 all PASS, disposition `M6_AUTHORIZED`, ρ_directed +1.0, perm p 0.0 |
| null fixture | G0 PASS, G1 FAIL (ρ_directed +0.17, p 0.34), disposition `E40_TERMINAL` |
| refusal: unsettled F2 chain / unsettled in-campaign F0 chain | exit 3, no rollup written (both) |
| exclusion: CANNOT_CHECK F2 replicas | counted; 3-replica cell still used; <2-replica cell CANNOT_CHECK; contrasts n=11 |
| exclusion: CANNOT_CHECK in-campaign F0 chain | drops exactly that cell (`CANNOT_CHECK__NO_F0_REFERENCE`), contrasts n=11 |
| **served-model substitution fixture** (artifacts carrying `glm-5.2`) | all **60** chains CANNOT_CHECK, 0 cells complete, disposition `CANNOT_CHECK` |
| **chain with no served-model record** | CANNOT_CHECK (`no served-model record …`) |
| leaked feedback (`wasserstein` injected) | analysis aborts on read |
| seed-mandate drift in a COMPLETE chain | CANNOT_CHECK |
| historical m2-F0 panel | present, 12 cells, `gating: false`, no gate keys |
| null calibration 400 reps seed 20260830 / null gate-chain 400 reps | rejection 0.055 ∈ [0.02, 0.09] / pass rate 0.0025 < 0.01 |
| Jaccard selftest, edge-parse round-trip | PASS |
| unit tests `tests/unit/test_e40_m5p_stage2c.py` | 15 passed; full `tests/unit` green |
| determinism | `math.fsum` throughout; fixture-identical output on CPython 3.11.5 (LUNARC) and 3.13.12 (Mac) |

## 5. Dispatch

DISPATCH_RECORD

## 6. Standing guard (what changes for future campaigns)

Any m-series runner reusing an earlier campaign's model-produced artifacts must (i) log the served
model id on every call — Stage-2b/2c do, m2/m3 did not — and (ii) assert the served id against a
frozen pin, so a provider-side swap fails closed instead of entering the data. Where an earlier
campaign lacks that record, its artifacts may be reused only as a labelled non-gating panel.
