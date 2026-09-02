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

No file in this directory grants scientific authority; routing is defined in the design.
