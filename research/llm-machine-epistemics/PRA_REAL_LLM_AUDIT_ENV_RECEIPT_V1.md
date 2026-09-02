# PRA Real-LLM Audit — Environment Receipt V1 (LUNARC, dev smoke only)

**Issue:** #51 · **Design:** `PRA_REAL_LLM_AUDIT_DESIGN_V1.{md,json}` · **Runner:** `pra_real_llm_audit.py`
**Scope:** compute environment, frozen model revisions, and the development smoke test on the
dev split. **No protected instance was executed or inspected.** Nothing here is a scientific result.

## 1. Environment

| item | value |
|---|---|
| host | LUNARC COSMOS, account `lu2026-2-51`, partition `gpua100` (node cg12: NVIDIA A100 80GB PCIe, driver 580.95.05) |
| base | `/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/` |
| python | `.venv` from login-node Python 3.11.5 (`module load Python/3.11.5`); the `PyTorch/2.6.0` module could not be loaded from the default Milan software tree (its GCC/13.3.0 + OpenMPI/5.0.3 prerequisites are not resolvable there), so torch 2.6.0 was pinned from PyPI instead — same version target |
| packages | torch 2.6.0+cu124, transformers 4.51.3, accelerate 1.6.0, safetensors 0.8.0, huggingface_hub 0.36.2, numpy 2.2.6, scipy 1.17.1, scikit-learn 1.9.0, protobuf 7.36.1, sentencepiece 0.2.2 |
| HF cache | `hf-cache/` (`HF_HOME`), 29 GB, runs with `HF_HUB_OFFLINE=1` |
| results root | `campaign-pra-llm-r1/` (`dev-smoke/` executed; `protected/` absent) |
| sbatch | `sbatch/pra_llm_dev_smoke.sbatch` (executed), `sbatch/pra_llm_r1.sbatch` (NOT executed; array 0-1, `--time=16:00:00`, requires `PRA_PROTECTED_AUTHORIZATION`) |

## 2. Frozen model revisions (resolved 2026-09-02 via `HfApi.model_info().sha`, snapshot downloaded)

| alias | HF id | commit |
|---|---|---|
| qwen2.5-7b-instruct | `Qwen/Qwen2.5-7B-Instruct` | `a09a35458c702b33eeacc393d103063234e8bc28` |
| mistral-7b-instruct-v0.3 | `mistralai/Mistral-7B-Instruct-v0.3` | `c170c708c41dac9275d15a8fff4eca08d52bab71` |

Both ungated, Apache-2.0, bf16, greedy, `max_new_tokens=160`, seed 51, batch 1.

## 3. Custody hashes (frozen with this PR)

| file | sha256 |
|---|---|
| `pra_real_llm_audit.py` | `6e7018963391df06b9c4986fbe121ef0a7d60f51ce1caf021bf0ee936f5e4a08` |
| `PRA_REAL_LLM_AUDIT_DESIGN_V1.json` | `188bf0b3facb5824e6f7952636e44743c2183a5f15ee642458f43ed496e03658` |
| dev suite `suite_dev.json` (seed 20260902, 32 instances) | `21a58a0fc0a5e82a0aacf24d05fa4052b149397948de8c762b1ee636939aa50b` |
| protected suite `suite_protected.json` (seed 20260903, 500 instances; generated, hashed, never read) | `46c2b9cfbbcd4d871a2c3cffc632122a5a6e9cd0438545123272ff86f2af4876` |

## 4. Dev smoke history (dev split only; 8 instances = 4 `F3_P2_CANON` + 4 `F1_P0`)

| job | runner state | outcome |
|---|---|---|
| 3563412 | first deploy | Qwen stages ran; Mistral tokenizer failed (`protobuf` missing) → installed `protobuf`, `sentencepiece` |
| 3563413 | + families filter, strict JSON | both models end-to-end; found 16-token padding granularity and one-word-answer incompetence |
| 3563414 | + reasoning/`Answer:` format, exact padding | GP0 pass both models (per-unit 1.0, budgets exact); both models over-revised under R0 because of the roster line |
| 3563622 | + explicit non-basis statement in R0/R3 (final, sha above) | see §5 |

## 5. Final smoke (job 3563622) — pipeline proof, not evidence

Job 3563622 on cg12, elapsed ≈14 min, `SMOKE_DONE`; every stage ran for both models; archived
under `results/pra-llm-r1/dev-smoke/` (rollup json/md, suite manifest, job log). Rollup runner sha
`6e7018…` matches the frozen file. Dev-split readings (8 instances; NOT evidence, n is tiny):

| item | qwen2.5-7b-instruct | mistral-7b-instruct-v0.3 |
|---|---|---|
| GP0 present equivalence (per-unit pass; budgets) | pass, 1.00; every condition padded to the same token count (207/205) | pass, 1.00 (225/224) |
| current action, both families | RETAIN 40/40 | RETAIN 40/40 |
| F1_P0 future accuracy, every condition | 8/8 | 8/8 |
| CANON arm-level accuracy R0 / R2 / R3 | 0.625 / 0.50 / 1.00 | 0.50 / 0.375 / 0.50 |
| CANON maintain arm (hB) under R0 | REOPEN 3/4 | REOPEN 4/4 |
| probe max test acc R0 / R3 / R2_TRUE_REMOVAL / KV_RETAINED (n_test 4) | 1.00 / 1.00 / 0.50 / 0.75 | 1.00 / 0.75 / 0.75 / 1.00 |
| terminal | `INCOMPLETE__CONTROL_FAMILIES_MISSING` (expected: MIRROR/RECON not in the smoke) | same |

Behavioural observation carried into the design as a registered risk (not tuned away): both 7B
models often REOPEN the maintain arm even under full history — Qwen's rationale misattributes the
recorded basis to the retracted source; Mistral invents "previously used as additional support"
and ESCALATEs under R3. This is the pre-registered `ORDINARY_REASONING_FAILURE_DESPITE_RETAINED_STATE`
class; if the protected run lands there, the contingency is Design V2 with larger frozen models,
never a post-hoc prompt change.

## 6. Timings and protected-run sizing

Measured per-call latency at the final format (job 3563414, same prompts/decoding as final):
Qwen present-gate 160 calls / 154 s, revision 80 gens / 135 s (≈1.7 s per 160-token greedy
generation); Mistral present-gate 255 s, revision 204 s (≈2.6 s per generation); probe ≈0.3 s
per forward; kv-channel ≈2.3–3.3 s per call; model load ≈40–60 s per stage.

Protected split per model: 1000 arms × 5 conditions = 5,000 status-line log-probs (≈0.1 s) +
5,000 current-action generations + 5,000 revision generations + 480 kv-channel generations +
1,440 probe forwards ≈ **5.5 h (Qwen) / 8 h (Mistral)** at measured rates; `pra_llm_r1.sbatch`
requests 16 h per array task (2× margin). Peak host RSS 5.9 GB; GPU memory ≈16 GB.

## 7. Warnings observed (benign, recorded)

- Mistral: "Sliding Window Attention is enabled but not implemented for `sdpa`" — the prompts
  (≤ ~700 tokens) are far below the 4096 window; no effect.
- Qwen generation config carries `top_p`/`top_k`; the runner passes `do_sample=False` and
  nulls them explicitly.

## 8. Authority

`REAL_LLM_EXECUTION = DEV_SMOKE_ONLY` · `PROTECTED_RUN = NOT_AUTHORIZED_NOT_EXECUTED` ·
`EMPIRICAL_LLM_CLAIM = NONE`.
