# Paper Re-audit Status — Academic Paper Skill PR17 / PR16 V1

**Date:** 2026-08-30  
**Skill state applied:** academic-paper-skills PR #17 head `ef47c81101e1e1b97864019dde143456a581de1c`, stacked on PR #16 head `087e47330826295a0b114563ec33238951ac56a9`.

## Why this re-audit exists

PR17 adds a fail-closed **formal-spine preservation** gate. A paper whose contribution is partly formal cannot be called complete after compression if a competent reader can no longer recover the defining scientific object, transition/operator, context boundary, decisive non-implication or hierarchy.

PR16 adds a separate **research-integrity verification** gate. Previous citation/key checks are useful but are not equivalent to an independent full-manuscript claim/source provenance audit bound to the exact final artifact.

## Flagship — Machine Epistemics

### Formal-spine result

V14 fails the new PR17 release gate as a final manuscript because its Perspective compression preserved the concepts but removed the explicit formal state and transition from main text.

Repair:

```text
V15_FORMAL_SPINE_COMPOSITE
= frozen V14 cited Perspective
+ papers/flagship/FLAGSHIP_FORMAL_SPINE_MAIN_TEXT_V1.tex
```

The restored main-text core contains:

```text
E_t=(P_t,S_t,O_t,A_t,R_t,M_t,V_t,X_t,H_t,K_t)
\widetilde E_t=(E_t;\Gamma_t,\Pi_t,\mathcal A_t)
T_t:(\widetilde E_t,a_t,x_t)->(\widetilde E_{t+1},\rho_t)
C=(environment, task family, resources, boundary, substrate/interface, timescale, criterion)
successful execution !=> warranted scientific transition
\mathcal A_t != \mathfrak E^*
pairwise compatible !=> global section witnessed
```

The surrounding prose explicitly distinguishes definitions/scope boundaries from candidate conservation, transport, reopening and closure hypotheses. No new scientific result is created; the formal items are recovered from existing programme formal records.

`AH20-R2` is **not** backfilled into this Perspective. Its result remains a separate protected journal-strengthening evidence object.

**Formal-spine terminal:** `PASS_RESTORED_IN_MAIN_TEXT`.

### Research-integrity result

The prior bibliography/citation-key/atomic-claim work remains useful evidence, but PR16 requires a verifier independent of the authoring agent/context, a fresh coverage pass, claim-to-source evidence receipts with exact locators/fingerprints, and binding to the exact final artifact hash.

This session cannot truthfully self-certify that independent gate.

**Integrity terminal:** `BLOCKED_ON_INDEPENDENT_PR16_VERIFIER`.

## LLM paper — Prospective Revision Adequacy

### Formal-spine result

V12 already exposes the required formal state/criterion hierarchy in main text: predictive-state equivalence, responsibility tuple, representation/evidence cell, joint acceptable-action intersection, Theorem 1, the no-certification corollary, recurrent-state limitation and exact one-bit witness.

PR17 therefore prohibits adding decorative equations merely to mirror the flagship.

**Formal-spine terminal:** `PASS_NO_SCIENTIFIC_REWRITE_REQUIRED`.

### Research-integrity result

As with the flagship, previous citation and theorem audits do not by themselves satisfy PR16's new independent full-release ledger requirement.

**Integrity terminal:** `BLOCKED_ON_INDEPENDENT_PR16_VERIFIER`.

## Current release posture

```text
FLAGSHIP_SCIENTIFIC_CONTENT = PR17_REPAIRED
FLAGSHIP_RELEASE_COMPOSITE = V15_FORMAL_SPINE_COMPOSITE
FLAGSHIP_FORMAL_SPINE = PASS
PRA_SCIENTIFIC_CONTENT = V12_UNCHANGED
PRA_FORMAL_SPINE = PASS
AH20_R2_BACKFILLED_INTO_FLAGSHIP = FALSE
PR16_INDEPENDENT_RESEARCH_INTEGRITY = OPEN_EXTERNAL
SUBMISSION_READY_UNDER_PR17_STACK = FALSE_UNTIL_INDEPENDENT_INTEGRITY_PASS
```

This is a stricter terminal than the pre-PR16/PR17 release status. The papers can be scientifically content-complete while the newly introduced independent verification authority remains open.
