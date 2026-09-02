# ORION-V2 Failure Ledger

This ledger begins before implementation because research-process failures are scientific evidence. Failure history is append-only: a repaired defect remains visible, and a later green result may not erase how it was obtained.

## Retained failure classes

These are **failure vocabularies to keep detecting**, not a claim that every class currently has an open critical defect.

- `COVERAGE_GAP` — a declared knowledge-taxonomy branch lacks adequate native and changed-vocabulary search.
- `REPO_COLLISION` — a proposed omission or novelty was already represented in ORION V1.
- `DONOR_RECONSTRUCTION_FAILURE` — the native parent cannot yet be reproduced faithfully.
- `FALSE_STRUCTURAL_ANALOGY` — apparent cross-domain proximity disappears when assumptions or semantics are restored.
- `DONOR_PRODUCT_TIE` — the strongest donor composition matches the candidate ORION mechanism.
- `NONIDENTIFIABLE` — the intended distinction cannot be learned under the current probe/intervention family.
- `CENSORED_ROUTE` — a required source or evaluation route was unavailable and cannot be counted as a negative search result.
- `V1_PARITY_RISK` — a proposed V2 factorization may lose a frozen V1 capability.
- `PREMATURE_IMPLEMENTATION` — code or outcome-generating execution begins before the V1 freeze gate.
- `AUTHORITY_LAUNDERING` — local research or engineering evidence is used as scientific/novelty/adoption authority.
- `SILENT_MODEL_SUBSTITUTION` — a model endpoint serves a different model than the one requested, with a success status and no warning, so artifacts carry an unrecorded producing-model identity. Guard: log the **served** model id on every call and assert it against a frozen pin (fail closed); where an earlier campaign lacks that record, its artifacts may be reused only as a labelled non-gating panel. First observed 2026-09-02 (E40-m5′ Stage-2b/2c: `glm-5.2` → `glm-5.3`, `glm-4.6` → `glm-5.3-flash`; the m2/m3 served model is unrecoverable — 0 hits across 1,810 artifact files).
- `DEGENERATE_PROBE_STATISTIC` — a proposed statistic lacks the shared structure it needs to rank anything, so a null result measures the statistic rather than the hypothesis. A specialization of `NONIDENTIFIABLE` for constructed proxies. Guard: establish the statistic's dynamic range on the substrate **before** using it as a truth proxy. First observed 2026-09-02 (E40-m5′ Stage-2c: replica-consensus Jaccard J = 0.028 mean, range 0.009–0.052 — independent seed-replicas of the same cell share ≈3 % of their edges).
- `UNGATED_CONTROL_VERDICT` — an analysis records control verdicts without consuming them, so it can emit a scientific verdict while a registered control is failing. Guard: `evaluate_gates()` takes the control verdicts as input and refuses every gate when one fails, with a fixture proving the refusal fires. First observed 2026-09-02 (E40-m5′ Stage-2c analysis emitted a routing terminal while its planted control failed; repaired in the Stage-2d freeze, not retrofitted to the frozen Stage-2c script).

Every concrete failure must preserve its source identities, affected claims and reopening conditions. No failure may be deleted merely because a later theory is more successful.

## Retained concrete failure records

- `research/failures/2026-08-parallel-wave3-ownership-collision/README.md`
- `research/failures/2026-08-wave4-recovery-and-ci-preterminal-defects/README.md`
- `research/failures/2026-08-wave5-epoch-and-chain-binding-defects/README.md`
- `research/failures/2026-08-parity-preflight-test-expectation-drift/README.md`
- `research/experiments/e40-matched/E40_M5P_STAGE2C_OUTCOME_RECEIPT.md` — E40-m5′ Stage-2c: registered planted positive control FAILED (terminal quality 0.6412 vs 0.9877 in m3, 1.0 in m2), so the campaign's computed routing terminal was **not** filed; disposition `CHECKER_INVALID__NO_VERDICT` and the E40 line stays open. Carries the three classes above. Cause discrimination is frozen as Stage-2d (`E40_M5P_STAGE2D_PLANT_DISCRIMINATION_DESIGN_V1`).

Their current closure classification is machine-recorded in:

`research/closure/CRITICAL_FAILURE_DISPOSITION_WAVE06_V1.json`

That receipt may report zero **known open critical local correctness/integrity/authority defects** while protected scientific evidence remains unresolved in other gates. In particular:

- missing independent semantic evaluators are G1/G5 custody evidence;
- strongest parent comparator identity is G4 evidence;
- protected parity and naturalistic/prospective value are G1/G5 evidence;
- scientific novelty/publication/field authority is G8 external authority.

These are not silently converted into repaired defects.

## Reopening rule

The critical-failure gate reopens if current CI exposes a real correctness/integrity/authority defect, if a hostile control demonstrates fail-open behavior, if an identity/custody binding is bypassable after outcome access, or if a historical repair no longer reproduces.
