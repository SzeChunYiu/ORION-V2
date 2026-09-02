# pra-llm-r1 — result archive for the real-LLM Prospective Revision Audit

Design: `../../PRA_REAL_LLM_AUDIT_DESIGN_V1.{md,json}` · runner: `../../pra_real_llm_audit.py`.

Contents:

- `dev-smoke/` — development smoke on the **dev split only** (8 instances: 4 `F3_P2_CANON`,
  4 `F1_P0`), both frozen models, every stage. Pipeline proof, **not** a scientific result;
  its numbers are not to be read as evidence for or against any terminal.
- `PRA_REAL_LLM_AUDIT_ROLLUP_V1.{json,md}` — will hold the protected-run rollup **only after**
  the protected run is authorized and executed under the frozen design. Absent until then.

No file in this directory grants scientific authority; routing is defined in the design.
