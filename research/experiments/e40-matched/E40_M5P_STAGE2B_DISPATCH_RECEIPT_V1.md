# E40-m5′ Stage-2b — Seed-Replica Stability Probe: dispatch receipt V1 (2026-09-02)

**Campaign:** `campaign-e40-m5p-stage2b` (LUNARC `/projects/hep/fs9/users/scyiu/orion-v2-e45/`),
exp_ids **503000–503191** (192 native `gies` runs), 48 chains = 12 cells × 4 seed-replicas
(`f2r0`..`f2r3`), 4 cycles each. F0 reference = frozen m2 F0 chains, read-only
(`E40M_REF=campaign-e40-m2`). Design frozen BEFORE any run (m-series discipline):
`E40_M5P_STAGE2B_SEED_REPLICA_PROBE_DESIGN_V1.{md,json}` — copied verbatim into this PR.

## 1. Frozen artifacts (sha256)

| artifact | sha256 |
|---|---|
| `E40_M5P_STAGE2B_SEED_REPLICA_PROBE_DESIGN_V1.md` | `62993f3c86b6cda02e52a7b84b38ca6f8d2ebf49945a2dd762c447bf7741bd9d` |
| `E40_M5P_STAGE2B_SEED_REPLICA_PROBE_DESIGN_V1.json` | `1c503930db07d370a0a7c24a4edeb1890b622c556b91bf15373fd30fd74ecefb` |
| `scripts/e40_matched_runner_m5p_stage2b.py` (runner) | `8e5e9eb8ca3f501bc9c5cee66590591219660f715d45bf7ef50c8069544d600b` |
| `research/experiments/e40-matched/e40_m5p_stage2b_analysis.py` (analysis + controls) | `7b7664b5282e8c24c12b2b48f2b1760e02944f1353d12eb6dedf5bd37fae52f6` |
| `tests/unit/test_e40_m5p_stage2b.py` | `10916630e17e4501dd081e58bc2106f840c2aa69af44334e57a1c896a557ec68` |
| `sbatch/e40_m5p_stage2b_chain_r1.sbatch` | `1b26884496e6865617b13ca99df237e28d8ba34348416c78d633e900a0deb6a0` |
| `sbatch/e40_m5p_stage2b_eval_r1.sbatch` | `b56c8e322819242e1fe4174403fcb14eb00901c620f9f2f19ae6f8a57efcc881` |

Lineage inputs verified on LUNARC before writing the runner: `campaign-e40-m2/e40_matched_runner.py`
sha256 `e13baa88…` (= m2 receipt) differs from `scripts/e40_matched_runner.py` (m1) in the
gies pin ONLY (`/usr/bin/diff`, one hunk); `campaign-e40-m3/e40_matched_runner_m3.py` sha256
`f6a6aaca…` is byte-identical to the repo copy. CausalBench checkout
`campaign-e40-r3/causalbench` at `1a2143cffdc85f835b41ce8d52034be1bf903e71`; native venv
`campaign-e40-r3/run/venv` (Python 3.11.5) — the same install m2/m3 used.

## 2. Single-delta verification (runner vs frozen m2 F2)

- `substrate_header`, `validate_config`, `native_run` (the native invocation: model/dataset/
  regime/fraction/seeds/subset 0.05/do_filter/max_path_length −1/omission/exp_id) are
  `inspect.getsource`-identical to the m3 runner (test `test_header_and_native_invocation_verbatim_from_m3`);
  the m3 runner's native path is itself m2-verbatim (m2→m3 diff: prompt rule + reference roots only).
- Cycles 2–4 prompts: `s2b.f2_prompt(ds, rep, c, history, replica) == m3.f2_prompt(ds, rep, c, history)`
  for every dataset, cycle ∈ {2,3,4} and replica (m3 renders m2-identical prompts for cycles ≥ 2).
- Cycle 1: `s2b prompt == m3 prompt with the m3 CYCLE-1 RULE string replaced by the Stage-2b seed
  rule` — same insertion point, and `s2b prompt minus its rule == m2 base` for all 12 cells × 4 replicas.
  The replica label never enters the prompt; the only inter-replica difference is the two integers.
- Seed rule text (cycle 1 only): "CYCLE-1 RULE (binding): cycle 1 has no feedback yet; its two seed
  knobs are mandated for this chain — model_seed MUST be {ms} and partial_intervention_seed MUST be
  {ps} (exactly these integers). Every other knob (training_regime, fraction_partial_intervention,
  omission_estimation_size) is yours to choose as usual."
- Mandate handling (design §2.1, m3 conventions): `ask_config` keeps the m2/m3 ≤3 parse/validate
  re-asks; `ask_config_f2` adds ≤3 mandate re-asks with a VIOLATION note; a cycle-1 decision that
  still does not carry exactly the replica's pair ⇒ `ChainCannotCheck` ⇒ `CANNOT_CHECK.json`
  (excluded, counted, reported; never repaired). The mandate transcript (`asked`, `violations`,
  `mandated`) is frozen into `decision.json` `call_log`. Resumed chains re-check the stored cycle-1
  decision; `arguments.json` seed drift on cycle 1 is a CANNOT_CHECK.
- Leakage: `FORBIDDEN_SUBSTRINGS` asserted (executed) on every feedback write, every feedback read,
  and every outgoing prompt (runner), and on every feedback read in the analysis. Truth is opened
  only by the analysis script's `primary_score`.
- Custody adds vs m3 (logging only, no prompt effect): `response.txt` (raw model reply),
  `model`/`temperature 0`/`response_sha256`/per-call `model_id` in `decision.json`.

## 3. Analysis + controls (frozen now, validated through `main()` before the freeze)

`e40_m5p_stage2b_analysis.py run` implements design §3–§6 verbatim: per-cell per-cycle mean
pairwise Jaccard of replica `output_network.csv` edge sets (`J_c`), `T_c = mean_k wasserstein_k(c)`,
per-cell Spearman pooled arithmetically, within-cell cycle-shuffle two-sided permutation
(10,000 draws, seed 20260902, `rng.sample` per cell in ds-major order), four shipping counterfactuals
(TERMINAL / CONSENSUS-ARGMAX cell-level earliest tie / PURITY-ARGMAX replica-local
`sig_purity = pooled_sig_tp / max(pooled_tp, 1)` / ORACLE-BEST), `d = f0_best_primary − mean_k shipped_k`
with exhaustive 2^12 sign-flip (m-series one-sided P(T_perm ≥ T_obs), positive = F2 better), gates
G0–G4 and the §6 routing (dispositions `M6_AUTHORIZED` / `E40_TERMINAL` / `CANNOT_CHECK`).
It **refuses (exit 3)** unless all 48 chains are settled (COMPLETE or CANNOT_CHECK); CANNOT_CHECK
chains are excluded and counted; a cell with < 2 usable replicas is `CANNOT_CHECK__TOO_FEW_REPLICAS`
and drops out of every contrast (n reported). A COMPLETE chain whose cycle-1 `config_1.json` does not
carry its mandated seeds is re-classified CANNOT_CHECK by the analysis (custody re-check).
Every file read is sha256-manifested (m2 F0 exp_ids + metrics; 192 × {arguments, metrics,
output_network.csv}; all feedback; CHAIN_COMPLETE/CANNOT_CHECK/config_1).

`selftest` (executed locally and on LUNARC; the eval sbatch re-runs it before the real analysis):

| control | result |
|---|---|
| Jaccard selftest: J(E,E)=1; J(E, rewired-E) < 0.05; J(E,∅)=0; 3-set consensus algebra | PASS |
| edge-parse round-trip (417-edge fixture; upstream `,0,1` header shape; foreign header rejected) | PASS |
| null calibration, m2/m3 form (400 reps, seed 20260830; exhaustive sign-flip at α=0.05) | PASS — rejection 0.055 ∈ [0.02, 0.09] |
| null gate-chain pass rate (400 random null campaigns, seed 20260830; G1∧G2∧G3∧G4) | PASS — 0.0025 < 0.01 |
| planted fixture through `main()` (consensus tracks truth; F0 slightly under the consensus ship) | G0–G4 all PASS, disposition `M6_AUTHORIZED`, ρ_directed = +1.0, perm p = 0.0 |
| null fixture through `main()` (truth independent of consensus; F0 at the cell oracle) | G0 PASS, G1 FAIL (ρ_directed +0.17, p = 0.34), disposition `E40_TERMINAL` |
| refusal: one MISSING / one IN_PROGRESS chain | exit 3, no rollup written |
| exclusion: 4 CANNOT_CHECK chains (one cell left with 1 replica) | counted 4; 3-replica cell evaluated on `f2r0,f2r1,f2r3`; 1-replica cell CANNOT_CHECK; contrasts n = 11 |
| leaked feedback (`wasserstein` injected into one feedback file) | analysis aborts on read (`redaction failed`) |
| seed-mandate drift in a COMPLETE chain | surfaces as CANNOT_CHECK (`… != mandated 71/79`) |
| cross-interpreter determinism (one fixture tree, byte-identical on both hosts) | J, T, d, contrasts, ρ, perm p, gates hash-identical on CPython 3.13.12 (Mac) and 3.11.5 (LUNARC campaign venv) |

Unit tests: `tests/unit/test_e40_m5p_stage2b.py` — 16 tests (byte-identity, mandate paths, numbering,
leakage asserts, runner selftest, analysis controls + end-to-end fixtures); full `tests/unit` green
locally (`python -m pytest tests/unit -q`).

## 4. Endpoint probe (E60 lane, from LUNARC login node)

`e40_matched_runner_m5p_stage2b.py probe-endpoint` (one-shot, temperature 0, `~/.orion-campaign.env`,
configured `ANTHROPIC_MODEL=glm-5.2`) run from the LUNARC login node 2026-09-02 04:02–04:04 UTC,
5 attempts 20 s apart, DNS resolving (2 records): **every attempt answered HTTP 429**
`rate_limit_error` code `1310` — `"Weekly/Monthly Limit Exhausted. Your limit will reset at
2026-09-05 10:04:26"` (provider clock UTC+8 per its request-id timestamps ⇒ reset =
2026-09-05 02:04:26 UTC = 04:04:26 CEST). The endpoint is reachable and authenticating (a
structured provider error, ≈0.35 s round trip) but is not serving completions until that reset;
no model id could be recorded yet. The runner's own retry path (m3 mechanics, `ORION_ARM_HTTP_RETRIES=10`)
would exhaust on 429 and raise — an HTTPError is deliberately NOT a `ChainCannotCheck`, so a walled
endpoint never manufactures exclusion markers. Job-time re-probe: the chain sbatch now runs
`probe-endpoint` as a pre-flight gate (exit 75 before touching any chain dir if the lane is still
walled; per-task probe JSON under `logs/e40m5p2b-probe-<array>_<task>.json`, model id recorded there).
`campaign-e40-m5p-stage2b/run/endpoint_probe.json` holds the last probe verbatim.

## 5. Dispatch

- Deploy: `orion-v2-wave6` clone pulled to the merged main; runner + analysis copied into the
  campaign dir and sha-verified against the merged tree; runner `selftest` and analysis `selftest`
  (full battery) re-run on LUNARC.
- Chain array: `sbatch/e40_m5p_stage2b_chain_r1.sbatch` — `--array=0-47%8`, 8 cpu / 64 G / 3 h per
  task (m3 chains took 12–24 min each, sacct 3554920; each Stage-2b chain is the same 4 native runs + 4
  decision calls). Task numbering cell-major: `task = cell*4 + replica`, chain dir
  `NN_f2rK_<dataset>_<rep>`, exp_id = 503000 + task*4 + (cycle−1).
- Eval job (`sbatch/e40_m5p_stage2b_eval_r1.sbatch`: status → control-planted → control-nullcal → audit
  → analysis selftest → analysis run) is committed but **NOT submitted**: unblinding is an operator
  decision; submit once `status` reports `all_settled`.

Dispatch decision (conservative): the chain array is submitted **deferred**
(`sbatch --begin=2026-09-05T04:45:00` Europe/Stockholm, 40 min after the provider's stated reset;
compute on LUNARC is committed to SD70/E70-GC1 through Sep 4 per the m4 receipt, so no collision)
with the pre-flight probe gate above. If the gate still fails at start, every task exits 75 within
seconds, nothing is written under `run/chains/`, and the identical array is resubmitted after a
manual probe succeeds. SLURM job ids are recorded in the amendment section below (added by the
follow-up PR after submission, since the PR carrying this receipt must merge before deployment).

### 5.1 Amendment — submission record

- Design/runner/analysis PR **#139** squash-merged as main `0cb33488f47ec12b7d4fb42813b044d141957456`
  (6/6 check-runs `conclusion=success` before merge).
- Deploy (2026-09-02 04:22 UTC): `orion-v2-wave6` clone at `0cb33488…`; copies in the campaign dir
  sha256-verified against §1 — runner `8e5e9eb8…`, analysis `7b7664b5…`, chain sbatch `1b268844…`,
  eval sbatch `b56c8e32…`; runner `selftest` 0 failures and analysis `selftest` (full battery: planted,
  null, refusal, exclusion, leak, seed-drift, nullcal 400/400, gate-chain 400) 0 failures on the LUNARC
  campaign venv (Python 3.11.5).
- Endpoint probe at deploy (04:22:50 UTC): HTTP 429 `rate_limit_error` 1310, reset stated
  `2026-09-05 10:04:26` (provider clock UTC+8) — unchanged from §4; `run/endpoint_probe.json`.
- **Chain array SLURM job `3563453`** (`o2-e40m5p2b-chain`, `0-47%8`, lu48, 8 cpu / 64 G / 3 h per
  task), submitted 2026-09-02 06:23:08 CEST with `EligibleTime=2026-09-05T04:45:00` CEST (40 min
  after the provider reset). Pre-flight probe gate per task; expected wall once eligible ≈ 2 h
  (48 chains × 12–24 min at 8 concurrent) ⇒ chains settled ≈ 2026-09-05 07:00 CEST if the gate opens.
- Eval job not submitted (unblinding is an operator decision): after `status` reports `all_settled`,
  `sbatch e40_m5p_stage2b_eval_r1.sbatch` from the campaign dir.
- If the gate is still walled at 04:45 CEST, every task exits 75 within seconds (logs
  `logs/e40m5p2b-probe-3563453_<task>.json`); resubmit the identical array once a manual
  `probe-endpoint` returns `parsed_ok: true`.

## 6. Resolutions taken (conservative, all recorded)

1. **G2/G3 perm p.** The design's "perm p ≤ 0.10" is applied with the m-series convention it names
   (one-sided sign-flip, positive = F2 better), i.e. CONSENSUS shipping must beat F0 at one-sided 10%
   while `mean_d ≥ −0.001`; G3 is its exact complement. No re-thresholding; the convention string is
   recorded in the rollup.
2. **CANNOT_CHECK cells.** A cell needs ≥ 2 usable replicas (Jaccard needs a pair); G0's `f0_wins ≥ 8`
   stays an absolute 8 regardless of the number of complete cells; the exhaustive sign-flip runs over
   the complete cells (n reported).
3. **Uninformative-replay control** (m2/m3) is not in the design's §7 battery and would need 12 extra
   native runs outside the 192; not run. Planted + nullcal + leakage + Jaccard + round-trip are.
4. **Planted control** has two executions: the runner's prompted-policy replay (m2/m3 plant v4, 9
   model calls, inherits the f2r0 seed mandate — part of the eval job) and the analysis-side planted
   fixture (must PASS G1; verified above).
5. **Per-replica 48-diff secondary** is reported as mean/wins only (within-cell correlated; the
   design's exhaustive sign-flip is defined for the 12 primary diffs; no extra RNG introduced).
6. **Empty edge sets**: J = 1 for two empty graphs (flagged via per-run edge counts in the rollup);
   never observed under gies in m2/m3 (0 NaN primaries).
7. **Array concurrency** `%8` (m2/m3 used `%6`): bounded endpoint load; wall ≈ 2 h if 8 slots are
   available.
8. **Interpreter-independent sums.** A pre-freeze check on one shared fixture found the analysis
   output differing between CPython 3.11 and 3.13 with identical inputs: plain `sum()` switched to
   compensated (Neumaier) summation in 3.12, moving last-bit values of `mean`/`pearson` and flipping
   `>=` ties in the permutation counts (null-fixture perm p 0.3433 vs 0.3405). Fixed before the freeze
   by routing every sum in `mean`, `pearson` and `perm_paired_p` through `math.fsum` (correctly
   rounded, identical everywhere); re-verified hash-identical across both interpreters (table above).
   The frozen analysis interpreter for the real run is the LUNARC campaign venv (3.11.5); the fsum
   form is also what the m6 freeze should inherit.

## 7. Custody

- Design PR: this PR (design verbatim + runner + analysis + tests + sbatch + this receipt).
- Frozen chains will live in `campaign-e40-m5p-stage2b/run/chains/` (48 × CHAIN_COMPLETE.json or
  CANNOT_CHECK.json), results `run/results/503000–503191`, controls `run/controls/`, rollup
  `run/rollup/E40_M5P_STAGE2B_ROLLUP_V1.{json,md}` → archived in-repo under `rollup-m5p-stage2b/`
  with the outcome receipt (design §8).
- No science claim issues from this receipt; the no-rescue clause (design §9) is binding.
