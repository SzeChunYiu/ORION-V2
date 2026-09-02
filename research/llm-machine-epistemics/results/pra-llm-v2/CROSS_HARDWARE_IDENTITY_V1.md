# V2 dev split — cross-hardware determinism receipt

Both frozen V2 models were run twice over the same frozen dev suite
(`suite_dev.json` sha256 `a8c58107bd53f9f55d3e53df9edbc59d6879bc82cee1294eb38b106217383842`),
same runner, same design, greedy decoding (`do_sample=False`, `num_beams=1`, seed 51, batch 1, bf16):

| configuration | job | partition | node | GPUs | placement |
|---|---|---|---|---|---|
| 1×A100-80GB | 3563845 | `gpua100` | cg12 | 1 × A100 80GB PCIe | single device (`--device cuda`) |
| 2×A100-40GB | 3563855 | `gpua100i` | cg20 | 2 × A100-PCIE-40GB | layer-wise sharding (`--device auto`, GPU-only) |

Driver 580.95.05 in both cases; torch 2.6.0+cu124, transformers 4.51.3.

## Result: identical

| model | stage | records compared | identical parsed actions | identical raw completion text |
|---|---|---|---|---|
| qwen2.5-32b-instruct | revision (dev-smoke) | 80 | 80/80 | 80/80 |
| qwen2.5-32b-instruct | revision (dev-gpc, full dev split) | 360 | 360/360 | 360/360 |
| qwen2.5-32b-instruct | present-gate (dev-smoke) | 80 | 80/80 | 80/80 |
| mistral-small-24b-instruct-2501 | revision (dev-smoke) | 80 | 80/80 | 80/80 |
| mistral-small-24b-instruct-2501 | revision (dev-gpc, full dev split) | 360 | 360/360 | 360/360 |
| mistral-small-24b-instruct-2501 | present-gate (dev-smoke) | 80 | 80/80 | 80/80 |

1,760 generations in total, 100 % identical raw text; both models' GPC verdicts are identical
(maintain 1.000 n=32, update 1.000 n=20, `COMPETENT__MODEL_RETAINED`) and every probe
max-test-accuracy in the two smoke rollups agrees.

## Scope of the claim

This shows that on this workload greedy decoding is invariant to **GPU count, memory SKU and
layer sharding within the A100 (sm_80) family** — the sharded case being the harder one. It is
**not** evidence of invariance across GPU *architectures* (e.g. A40, sm_86), which was not tested.
It grants no scientific authority and says nothing about any gate outcome.
