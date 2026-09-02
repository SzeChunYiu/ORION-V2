# PRA Real-LLM Audit — Design V2 Environment Receipt V1 (LUNARC, dev smoke + GPC dev check only)

**Issue:** #51 · **Design:** `PRA_REAL_LLM_AUDIT_DESIGN_V2.{md,json}` · **Runner:** `pra_real_llm_audit.py` (shared with V1)
**Scope:** compute environment, frozen model revisions, the development smoke on the dev split, and the
pre-registered GPC competence check on the dev split. **No protected instance was generated, executed
or inspected** (`campaign-pra-llm-v2/protected` does not exist). Nothing here is a scientific result.

## 1. Environment

| item | value |
|---|---|
| host | LUNARC COSMOS, account `lu2026-2-51` |
| base | `/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/` — V1 files (`pra_real_llm_audit.py` sha `e25d969f…`, `PRA_REAL_LLM_AUDIT_DESIGN_V1.json` sha `188bf0b3…`, `campaign-pra-llm-r1/`) untouched; V2 lives in `v2/` and `campaign-pra-llm-v2/` |
| python / packages | the V1 `.venv`, unchanged and with nothing added: Python 3.11.5, torch 2.6.0+cu124, transformers 4.51.3, accelerate 1.6.0, safetensors 0.8.0, huggingface_hub 0.36.2, numpy 2.2.6, scipy 1.17.1, scikit-learn 1.9.0, protobuf 7.36.1, sentencepiece 0.2.2 |
| HF cache | shared `hf-cache/` (`HF_HOME`), 134 GB after the V2 downloads (29 GB V1 + 65.5 + 47.2), `HF_HUB_OFFLINE=1` |
| GPUs used | `gpua100` node cg12: 1 × NVIDIA A100 80GB PCIe · `gpua100i` node cg20: 2 × NVIDIA A100-PCIE-40GB; driver 580.95.05 on both |
| results root | `campaign-pra-llm-v2/`: `dev-smoke/`, `dev-gpc/` (80 GB) and `dev-smoke-2x40/`, `dev-gpc-2x40/` (2×40 GB). `protected/` absent |
| sbatch | `sbatch/pra_llm_v2_dev_smoke.sbatch` (executed twice), `sbatch/pra_llm_v2_r1.sbatch` (**NOT executed, not queued**) |

## 2. Frozen model revisions

Resolved 2026-09-02 via `HfApi.model_info().sha`; snapshots downloaded to `hf-cache` and recorded in
`RESOLVED_REVISIONS_V2.json` by `sbatch/pra_llm_download_models.py --out RESOLVED_REVISIONS_V2.json <repos>`.

| alias | HF id | commit | snapshot (HF shards only) | gated |
|---|---|---|---|---|
| qwen2.5-32b-instruct | `Qwen/Qwen2.5-32B-Instruct` | `5ede1c97bbab6ce5cda5812749b4c0bdf79b18dd` | 65.54 GB (17 safetensors) | no (Apache-2.0) |
| mistral-small-24b-instruct-2501 | `mistralai/Mistral-Small-24B-Instruct-2501` | `9527884be6e5616bdd54de542f9ae13384489724` | 47.18 GB (11 safetensors; the 47 GB `consolidated.safetensors` is skipped) | no (Apache-2.0) |

Both bf16, greedy, `max_new_tokens=160`, seed 51, batch 1 — decoding verbatim from V1. Mistral-Small's
`tokenizer.json` (Tekken vocabulary) loaded with the stock fast tokenizer; **no package or extra was
needed** beyond the V1 venv, and its optional `SYSTEM_PROMPT.txt` is not used.

## 3. Custody hashes

| file | sha256 |
|---|---|
| `pra_real_llm_audit.py` (as run in both dev jobs) | `e42c5adc9521544e249213a1f08762a4f8da4fd19c2e8b307658102f38387fdd` |
| `pra_real_llm_audit.py` (frozen, merged in #151, deployed to `v2/` after the jobs) | `198626238170df48325a23d2c65cca71c2e3a162e76ee2b43074fde0cadfda7f` |
| `PRA_REAL_LLM_AUDIT_DESIGN_V2.json` (as run) | `4edc9ca9b410ec9f3754a4301cbf318cce665c30e69c54a3f00b23cda98eb961` |
| `PRA_REAL_LLM_AUDIT_DESIGN_V2.json` (after the sealed-seed commitment was written in) | `c0b65dc40b3123e4da955ab79d5fa60a0f6eff89436efb12b8378f424ea2f5ef` |
| dev suite `suite_dev.json` (seed 20260912, 36 instances) | `a8c58107bd53f9f55d3e53df9edbc59d6879bc82cee1294eb38b106217383842` |
| protected suite | **not generated**; sealed-seed commitment below |

**Runner-sha reconciliation.** The dev jobs ran `e42c5adc`; the frozen file is `1986262…`. The two
differ only by the nonce-collision generator fix and two ruff removals (an unused import and an unused
local). The frozen runner regenerates the dev suite to the identical digest `a8c58107…`, which also
*proves* no A==B nonce collision occurs on seed 20260912 — so the fix cannot have altered any dev
result, and the dev numbers below are attributable to the frozen runner. The frozen runner is what is
now deployed at `v2/pra_real_llm_audit.py`.

## 4. GPC dev check (pre-registered competence gate — the registered pre-run use of the dev split)

Full dev split, 36 instances / 72 arms, condition R0, revision stage. Thresholds: maintain ≥ 0.75 and
update ≥ 0.75.

| model | hardware | maintain accuracy R0 | update accuracy R0 | verdict |
|---|---|---|---|---|
| qwen2.5-32b-instruct | 1×A100-80GB | **1.000** (n=32) | **1.000** (n=20) | `COMPETENT__MODEL_RETAINED` |
| mistral-small-24b-instruct-2501 | 1×A100-80GB | **1.000** (n=32) | **1.000** (n=20) | `COMPETENT__MODEL_RETAINED` |
| qwen2.5-32b-instruct | 2×A100-40GB | 1.000 (n=32) | 1.000 (n=20) | `COMPETENT__MODEL_RETAINED` |
| mistral-small-24b-instruct-2501 | 2×A100-40GB | 1.000 (n=32) | 1.000 (n=20) | `COMPETENT__MODEL_RETAINED` |

Per family (both models, both configurations): `F1_P0`, `F2_P1`, `F3_P2_CANON`, `F3_P2_CANON_SF`,
`F3_P2_INDEP`, `F3_P2_MIRROR`, `F3_P2_RECON` all 1.00 where the class is populated.

**Both models pass; no model was replaced.** The design's §9 replacement record is therefore empty, and
GPC is now exhausted (the protected seed is sealed). This is the contrast with V1, whose 7B models
over-revised the maintain arm under full history on the dev split.

### 4a. Registered observation — GPC does not screen the competence GP0 requires

GPC scores the **future** action under R0 (after the evidence). GP0 requires the **current**
(pre-evidence) action under R0 to be correct and identical across R0/R2/R3. These are different
quantities, and the dev smoke separates them: `mistral-small-24b-instruct-2501` passes GPC at
1.000/1.000 yet fails GP0 on the smoke at per-unit 0.500, because under **R0 only** it answers
ESCALATE on 4 of 8 canonical arms whose gold current action is RETAIN (under R2/R3/R4 its current
accuracy is 1.000; its status-line log-prob equivalence is untouched, TOST mean Δ = 1e-4, and token
budgets match exactly). So the design's stated rationale for GPC — that a V2
`ORDINARY_REASONING_FAILURE` terminal can no longer be explained by a surface that cannot follow the
contract — does **not** extend to the `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` route.

This is disclosed as a gap in a gate registered in this very design, and is a lead for a future design
version (a current-action arm of GPC). It changes nothing now: the thresholds and rule are frozen,
Mistral **passed** GPC and therefore may not be replaced on the strength of a GP0 smoke reading, and
the prompt is not touched (no-rescue clause). The corresponding protected-run risk is recorded in §5.

## 5. Dev smoke (8 instances = 4 `F3_P2_CANON` + 4 `F1_P0`; pipeline proof, **not evidence**)

Every stage ran for both models on both hardware configurations; `V2_SMOKE_DONE`; no errors.
Archived under `results/pra-llm-v2/dev-smoke/`. Dev-split readings (n = 8 — far too small to mean
anything, and the two control families the design gates on are absent by construction):

| item | qwen2.5-32b-instruct | mistral-small-24b-instruct-2501 |
|---|---|---|
| GP0 present equivalence (per-unit pass) | pass, 1.00 | **fail, 0.50** (R0-only ESCALATE, see §4a) |
| GP0 TOST mean Δlogprob (R3−R2) | 0.0000, equivalent | 0.0001, equivalent |
| current-action accuracy R0 / R1 / R2 / R3 / R4 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 0.44 / 0.63 / 1.00 / 1.00 / 1.00 |
| `F1_P0` future accuracy, every condition | 1.000 | 1.000 |
| CANON arm-level accuracy R0 / R1 / R2 / R3 / R4 | 1.000 / 0.375 / 0.000 / 1.000 / 1.000 | 1.000 / 0.500 / 0.375 / 1.000 / 1.000 |
| contrast B (R2→R3), n=8 | 0.000 → 1.000, exact p = 0.008 | 0.375 → 1.000, exact p = 0.062 |
| probe max test acc R0 / R3 / R2_TRUE_REMOVAL / KV_RETAINED (n_test = 4) | 1.00 / 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 / 1.00 |
| smoke terminal | `INCOMPLETE__CONTROL_FAMILIES_MISSING` (expected) | `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` |

**Registered risks carried into the protected run, not tuned away.**
(i) Mistral-Small may fail GP0 on the protected split for the R0-only reason above, which routes to
`CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` — a registered negative on the surface, not on the
theory. (ii) The probe's `R2_TRUE_REMOVAL` accuracy sat at 0.75 (> the 0.65 chance bound) for both
models with n_test = 4, so GP2a would fail as `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION` at
smoke scale; at n_test = 48 on the protected split this statistic is far better resolved. Neither
observation licenses any change to the design.

## 6. Timings, VRAM and protected-run sizing

Measured wall time per stage (`/usr/bin/time`), dev split:

| part | stage | calls | qwen 1×80GB | mistral 1×80GB | qwen 2×40GB | mistral 2×40GB |
|---|---|---|---|---|---|---|
| smoke (16 arms) | present-gate | 160 | 549.5 s | 463.9 s | 716.9 s | 578.4 s |
| smoke | revision | 80 | 540.6 s | 313.3 s | 712.3 s | 398.4 s |
| smoke | probe | 48 | 11.5 s | 10.8 s | 14.0 s | 12.9 s |
| smoke | kv-channel | 16 | 125.0 s | 62.2 s | 160.2 s | 81.5 s |
| GPC (72 arms) | revision | 360 | 2741.0 s | 1589.7 s | 3488.7 s | 2031.5 s |

Per-call rates (s/call) on 1×A100-80GB: qwen present-gate 3.43, revision 7.61, probe 0.24, kv 7.81;
mistral 2.90 / 4.42 / 0.23 / 3.89. Sharding across 2×40 GB costs ≈ 1.27–1.30×.
Peak GPU memory: **64.0 GB** (1×A100-80GB, qwen 32B) and **33.4 GB per card** (2×A100-40GB). Peak host
RSS 4.6 GB (qwen) / 5.7 GB (mistral). Job elapsed: 1 h 51 m (3563845), 2 h 23 m (3563855).

**Protected split per model** — 620 instances / 1240 arms → 12,400 present-gate calls + 6,200 revision
generations + 1,440 probe forwards + 480 kv-channel generations = **20,520 model calls**:

| configuration | qwen2.5-32b (slower task) | mistral-small-24b | `--time` |
|---|---|---|---|
| 1×A100-80GB (`gpua100`) | ≈ 26.3 h | ≈ 18.5 h | 40:00:00 (1.5×) |
| 2×A100-40GB sharded (`gpua100i`) | ≈ 33.8 h | ≈ 23.2 h | **60:00:00 (1.8×)** — as written in `pra_llm_v2_r1.sbatch` |

An array shares one `--time`, so it is sized to the slower task.

## 7. Sealed protected seed

Generated on LUNARC by `v2/seal_seed.sh` **after** both models passed GPC, as
`v2/protected_seed.sealed` (`<int>:<256-bit salt>`, mode 0600, 75 bytes, never printed, never copied
into the repo). Its sha256 — the commitment now written into the design JSON — is

```
d53e374809bfd6f78e4b9a056bbdb237739b09a04cd716a75d0e45748ebc8925
```

Verified functionally without revealing the seed: the runner resolves the protected seed **only** when
handed a file hashing to this commitment (`commitment_matches_and_unlocks: True`), returns `None` when
the file is absent (`without_seed_file_returns_None: True`), and refuses a non-matching file. The salt
makes the commitment non-invertible, so the protected suite cannot be regenerated or inspected from
the repo before the run. The sealed file is archived beside the rollup only post-run.

## 8. Protected run — not submitted

`pra_llm_v2_r1.sbatch` is written, sized and **not queued**. Two independent bars stand:

1. **Authorization.** `protected_run.authorized` is `false`; the token
   `PROTECTED_RUN_AUTHORIZED_AFTER_DESIGN_REVIEW__ORION51_PRA_V2_R1` is the operator's to issue. No
   agent message constitutes that authorization.
2. **The design's own registered note.** `protected_run.note` says the V2 protected job "must not be
   queued while the V1 R1 array is pending or running". V1 R1 (job `3563787_[0-1]`) is PENDING. The
   note was written with resource contention in mind, but its text is unqualified by partition, so it
   is honoured literally even though the V2 script now targets a different partition. The
   intent-vs-text discrepancy is recorded in design §9 as an observation for a future design version,
   not read narrowly here.

Exact submission command, once both bars are lifted:

```bash
ssh lunarc
cd /projects/hep/fs9/users/scyiu/orion-v2-pra-llm
PRA_PROTECTED_AUTHORIZATION=PROTECTED_RUN_AUTHORIZED_AFTER_DESIGN_REVIEW__ORION51_PRA_V2_R1 \
  sbatch sbatch/pra_llm_v2_r1.sbatch
# rollup, once both array tasks finish:
.venv/bin/python v2/pra_real_llm_audit.py --stage rollup \
  --workdir campaign-pra-llm-v2/protected --design v2/PRA_REAL_LLM_AUDIT_DESIGN_V2.json \
  --backend hf --split protected \
  --protected-authorization PROTECTED_RUN_AUTHORIZED_AFTER_DESIGN_REVIEW__ORION51_PRA_V2_R1
```

**Partition (recorded as required).** `gpua100i`, `--gres=gpu:a100:2`, `PRA_DEVICE=auto` (layer-wise
sharding, GPU-only; the runner hard-fails if any layer lands on CPU or disk). This keeps the V2
protected run off `gpua100` entirely, so it cannot starve V1 R1. It is validated by dev job 3563855,
which reproduced the single-80 GB run byte-identically (§9). `gpua40i` is **infeasible**, not merely
slower: its nodes carry a single A40 each, so there is no intra-node sharding, and 32B bf16 (65.5 GB)
does not fit one 48 GB card. To run on `gpua100` instead, use `--gres=gpu:a100:1`, unset
`PRA_DEVICE`, and set `--time=40:00:00`.

## 9. Cross-hardware determinism

The full dev split was executed twice — 1×A100-80GB (`gpua100`, cg12) and 2×A100-40GB layer-sharded
(`gpua100i`, cg20). **All 1,760 generations are byte-identical** (parsed actions and raw completion
text), GPC verdicts agree exactly, and the probe accuracies match. Details and the scope of the claim
are in `results/pra-llm-v2/CROSS_HARDWARE_IDENTITY_V1.md`. The claim covers GPU count, memory SKU and
sharding **within the A100 (sm_80) family**; it is not evidence about other architectures (A40 is
sm_86), which were not tested.

## 10. Authority

`REAL_LLM_EXECUTION = DEV_SMOKE_AND_GPC_DEV_CHECK_ONLY` · `PROTECTED_RUN = NOT_AUTHORIZED_NOT_EXECUTED` ·
`PROTECTED_SUITE = NOT_GENERATED` · `EMPIRICAL_LLM_CLAIM = NONE`.
