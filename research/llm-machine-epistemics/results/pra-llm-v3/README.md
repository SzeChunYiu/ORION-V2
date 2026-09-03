# pra-llm-v3 — result archive for the real-LLM Prospective Revision Audit, Design V3

Design: `../../PRA_REAL_LLM_AUDIT_DESIGN_V3.{md,json}` · runner: `../../pra_real_llm_audit_v3.py`
(V3's own copy) · diagnosis: `../../PRA_GP2A_CONSTRUCT_VALIDITY_DIAGNOSIS_V1.md`.

**Empty by design. No V3 run exists, is authorized, or is requested.**

V3 repairs the GP2a defect recorded in `../pra-llm-r1/OUTCOME_RECEIPT_R1.md` §6 and carried as an
open obligation in `../pra-llm-v2/README.md` §3. The repair is a new design with a fresh sealed
seed, which is what V2's no-rescue clause requires — not a patch to the V2 campaign, whose
protected run (SLURM array `3566415`) is in flight under its own frozen runner.

What lands here, and only in this order:

1. `CERTIFICATE_dev.json` — the blocking pre-run certificate (label identifiability + registered
   clause coverage), on the dev split.
2. the sealed protected seed's sha256, published into the design in a commit of its own.
3. `PRA_REAL_LLM_AUDIT_ROLLUP_V3.{json,md}` — after an authorized protected run completes.
4. `protected_seed.sealed` — post-run reveal, beside the rollup.

Nothing in this directory grants scientific authority; routing is defined in the design.
