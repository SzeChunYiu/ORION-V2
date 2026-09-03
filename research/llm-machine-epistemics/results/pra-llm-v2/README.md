# pra-llm-v2 — result archive for the real-LLM Prospective Revision Audit, Design V2

Design: `../../PRA_REAL_LLM_AUDIT_DESIGN_V2.{md,json}` · runner: `../../pra_real_llm_audit.py`.

Contents:

- `dev-smoke/` — development smoke on the **dev split only** (8 instances: 4 `F3_P2_CANON`,
  4 `F1_P0`), both frozen models, every stage, run twice on different hardware
  (`1xA100-80GB` = job 3563845 on `gpua100`; `2xA100-40GB` = job 3563855 on `gpua100i`,
  layer-sharded). Pipeline proof, **not** a scientific result; its numbers are not to be read
  as evidence for or against any terminal.
- `dev-gpc/` — the pre-registered GPC competence gate on the **full dev split** (36 instances,
  72 arms, condition R0), per model, on both hardware configurations. GPC decides model
  *eligibility* before the protected seed is sealed; it is not a result and never gates GP0–GP3.
- `CROSS_HARDWARE_IDENTITY_V1.md` — receipt: the two hardware configurations produced
  byte-identical raw generations.
- `PRA_REAL_LLM_AUDIT_ROLLUP_V2.{json,md}` — will hold the protected-run rollup **only after**
  the protected run is authorized and executed under the frozen design. Absent until then.

## Protected run — IN FLIGHT (open obligations)

The V2 protected run was submitted on 2026-09-03 as SLURM array `3566415` on `gpua100i`
(`sbatch/pra_llm_v2_r1.sbatch`, the reviewed script, byte-identical to the repo copy
`03241256…`), after the V1 R1 array had finished — the ordering condition registered in
`protected_run.note`. The job verified, at launch, all three frozen inputs by sha256:
runner `19862623…`, design `c0b65dc4…`, and the **sealed seed `d53e3748…`, matching the
commitment published in the design**. The protected suite generated to 620 instances
(sha256 `526b47b8…`).

Task 0 (`qwen2.5-32b-instruct`) started immediately on `cg20`. Task 1
(`mistral-small-24b-instruct-2501`) is queued: only `cg20`/`cg21` carry two A100-40GB cards,
and neither V2 model fits a single 40 GB card in bf16 (65.5 / 47.2 GB), so the task waits for
a two-GPU node. `gpua100` was checked and is **not** a faster route (twelve jobs pending
through 2026-09-08).

**Open obligations, not yet discharged:**

1. **Rollup.** `--stage rollup` is run once, manually, only after **both** array tasks finish;
   the rollup requires both model directories to be present.
2. **Post-run seed reveal.** The design registers that `v2/protected_seed.sealed` is archived
   in the repo **only after the protected run completes**. The seed has *not* been revealed and
   this obligation is **outstanding** until the rollup lands beside it.
3. **Known limitation to carry into the V2 rollup.** GP2a's registered clause reads "probe
   decodes support_source under R0 **and R3** (≥ 0.80)", but the frozen runner evaluates the
   positive control on R0 only. This was found on unblinding R1 (see
   `../pra-llm-r1/OUTCOME_RECEIPT_R1.md` §6) and the V2 runner carries the same code. Per the
   design's no-rescue clause the runner is **not** patched — a patch would invalidate the
   sealed seed. GP2a's R3 half is therefore expected to report `CANNOT_CHECK` in V2 as well,
   and repair belongs to a V3 design with a fresh sealed seed.

No file in this directory grants scientific authority; routing is defined in the design.
