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
- `MANDATE_EXPLORATION_COLLAPSE` — a binding cycle-1 prompt mandate anchors an iterative arm on its mandated first config, which it then keeps re-choosing, so the search never samples the axis the objective varies along and a feedback-following control fails. Severity tracks mandate specificity and is model-dependent. Guard: run any mandated design alongside an unmandated planted control on the same channel before reading its trajectories. First measured 2026-09-02 (E40-m5′ Stage-2d: unmandated PASS 0.9877 reaching the optimum by cycle 2; regime anchor FAIL 0.9518; exact-seed mandate FAIL 0.0233 with `frac` never leaving 0.0 across nine cycles).
- `UNGATED_CONTROL_VERDICT` — an analysis records control verdicts without consuming them, so it can emit a scientific verdict while a registered control is failing. Guard: `evaluate_gates()` takes the control verdicts as input and refuses every gate when one fails, with a fixture proving the refusal fires. First observed 2026-09-02 (E40-m5′ Stage-2c analysis emitted a routing terminal while its planted control failed; repaired in the Stage-2d freeze, not retrofitted to the frozen Stage-2c script).
- `NONREPRODUCIBLE_FROZEN_ARTIFACT` — a "frozen" artifact is regenerated from its committed seed through iteration over an unordered container, so per-process hash randomisation yields a different artifact from the same commitment while every seed record, sha256 and freeze receipt remains internally consistent and correct: the custody chain is honest and the artifact is still not reproducible. Guard: regenerate the frozen artifact in a fresh process under at least two `PYTHONHASHSEED` values and compare hashes, and forbid RNG draws ordered by an unordered container (the reproducible-builds practice of rebuilding in a deliberately varied environment and comparing bit-for-bit, applied to a research split). **Near miss, not a realised defect** — unlike every other class in this list, no contaminated result was produced: it was caught before any protected artifact existed. Found by regenerating the split from a second process and comparing digests, not by a review or an auditor. First observed 2026-09-02 (FG70 `ORION-FG-L5-EXACT-V1`, PR #181: three generator planters drew decision assignments while iterating `set(...)` of signature tuples; fixed at the root and guarded by a cross-`PYTHONHASHSEED` behavioural test and a source-level test).

- `FORECLOSED_FAILURE_MODE` — a world is built so that the failure its primary endpoint measures **cannot occur in it**, so a hard validity gate fails and the study cannot be rescued without degrading an arm. Distinct from `NONIDENTIFIABLE`: the effect is not merely unlearnable under the probe family, it is absent by construction. The tell is a validity gate that survives a full revival attempt while every arm reads a clean zero on a detector proven to fire on the same records. Guard: before freezing an endpoint, establish that its failure mode has **dynamic range in the world as built** — and treat the world's cost structure as part of that check, since a failure of over-assertion cannot arise where verification is cheap relative to assertion. First observed 2026-09-03 (ME-F1 G0e: `SIMPLE_DIRECT` laundered 0 of 121 claims, then 0 of 106 bare verdicts after the warrant field was removed from its interface entirely; ME-X1's 492 laundered updates arose where warrant was *not* freely checkable, while ME-F1 §2.6 made verification O(clauses), unmetered and available to every arm every turn. Routed `CANNOT_CHECK`; no protected campaign dispatched).

Every concrete failure must preserve its source identities, affected claims and reopening conditions. No failure may be deleted merely because a later theory is more successful.

## Retained concrete failure records

- `research/failures/2026-08-parallel-wave3-ownership-collision/README.md`
- `research/failures/2026-08-wave4-recovery-and-ci-preterminal-defects/README.md`
- `research/failures/2026-08-wave5-epoch-and-chain-binding-defects/README.md`
- `research/failures/2026-08-parity-preflight-test-expectation-drift/README.md`
- `research/experiments/e40-matched/E40_M5P_STAGE2D_OUTCOME_RECEIPT.md` — E40-m5′ Stage-2d: the Stage-2c control failure is attributed to the cycle-1 mandate (D2 `PROMPT_IMPLICATED`, all controls PASS); the model channel alone is exonerated, though the m3-form arm passed under the earlier model and fails now, so the cause is an interaction whose magnitude is not estimable (the m2-era model is unrecoverable). Stage-2c stays `CHECKER_INVALID__NO_VERDICT`; the E40 line stays open.
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
