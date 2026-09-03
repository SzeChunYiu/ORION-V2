# pra-llm-r1 — result archive for the real-LLM Prospective Revision Audit

Design: `../../PRA_REAL_LLM_AUDIT_DESIGN_V1.{md,json}` · runner: `../../pra_real_llm_audit.py`.

Contents:

- `dev-smoke/` — development smoke on the **dev split only** (8 instances: 4 `F3_P2_CANON`,
  4 `F1_P0`), both frozen models, every stage. Pipeline proof, **not** a scientific result;
  its numbers are not to be read as evidence for or against any terminal.
- `PRA_REAL_LLM_AUDIT_ROLLUP_V1.{json,md}` — the protected-run rollup, executed under the
  frozen design (array job 3564879, 2026-09-02/03, both frozen models, all four stages).
- `OUTCOME_RECEIPT_R1.md` — outcome receipt: terminal, artifact verification, custody hashes,
  model-identity assertion, single-stage failure attribution, the GP2a implementation
  divergence, the silent-failure audit and the registered revival lever.

Terminal: **`REGISTERED_NEGATIVE_OR_BOUNDARY__CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE`** in
both models, attributed to the `F3_P2_MIRROR` false-revision control under R3. Because GP3
fails, the GP0/GP1/GP2 positives are **not** interpretable as a positive result.

No file in this directory grants scientific authority; routing is defined in the design.
