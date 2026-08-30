# Result Addendum to Demarcation Review Packet V2 — AH20-R1 Frozen Outcome

**Addendum date:** 2026-08-30
**Adds to:** `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V2.md` (`PACKET_VERSION = V2_PRE_AH20_OUTCOME`)
**Status:** post-outcome addendum. The V2 pre-outcome questions are frozen and are NOT
modified, reinterpreted or re-scored by this file. Per V2's own provision: *"A later result
addendum may append the frozen outcome and ask whether it changes the reviewer's judgment;
it must not rewrite these pre-outcome questions."* A reviewer who supplied a V2 judgment
before reading this addendum remains a valid pre-outcome reviewer; their judgment is not
revised by this document.

---

## A. What was run (frozen suite, unchanged)

- **Suite:** AH20 (78 tasks × 5 arms = 390 jobs), frozen at
  `research/experiments/EPISTEMIC_ATLAS_HORIZON_AH20_SUITE_FREEZE_V1.md`
  (V1 FROZEN; V14 canonical anchor).
- **Strata:** 48 EL10 worlds reused byte-identical under custody (locality suite) +
  30 fresh atlas/horizon tasks (classes AHC0–AHC4 × 6).
- **Arms:** SIMPLE_NATIVE; CURRENT_F0 (parent federation); CURRENT_F2 (ORION kernel);
  PARENT_LOCAL_GLOBAL (strongest local-to-global parent: OED probe + sheaf gluing);
  F2_PLUS_ATLAS_HORIZON (the interface under test).
- **Integrity:** 390/390 returned, single executor, `all_returncodes_zero=true`;
  private oracle unlinked during dispatch (`GOLD/OUTCOME_ACCESS=NONE`), restored
  hash-matched; EL10 reuse byte-identical asserted at prepare.

## B. Frozen outcome (terminal)

```text
AH20_R1_TERMINAL = CONTROL_DIVERGENT
```

The frozen invariance sentinel fired **before** any elimination rule: the five arms
disagree on the AHC0 (LOCAL_ONLY) control signatures (1/6, 3/6, 3/6, 5/6, 5/6 correct).
Per the freeze, *"a null here is not evidence about the interface."* Between-arm
differences on this run are confounded by wrapper-induced baseline differences; the run
therefore carries **no evidence for or against the atlas/horizon interface**, and no
parent result was weakened. Parent-sufficiency nulls (EL10) and audit passes (EL20, AH10)
stand exactly as recorded in V2.

## C. Three facts a reviewer needs

1. **The control did its job, and nothing more.** Every AHC0 failure is the same cell:
   the decision is correct and `holds_across_contexts=true` is over-claimed — while the
   same answer simultaneously (and correctly) returns `transport_verdict=INVALID`. The
   wrapper texts themselves shift local-only behavior across arms. The suite treats this
   as disqualifying confounding rather than re-scoring around it.
2. **All measured contrasts are null.** 16 paired exact-McNemar tests × Holm(α=0.05):
   0/16 significant. Transport correctness 0.972 in every arm; probe selection at
   ceiling (1.000) in every arm; false-outside-atlas rate 0.000 in every arm
   (exact Clopper–Pearson 95% CI [0, 0.0499], n=72 per arm).
3. **One representation limit is recorded, not patched.** The reused EL10 stratum and the
   probe-world texts expose no atlas registry in public text, so the textually faithful
   gluing answer there is CANNOT_CHECK while the frozen oracle encodes underlying world
   state — a structural ceiling (~30/78) for text-faithful arms. The executed oracle was
   NOT altered; the limit is recorded as the fiber any future iteration must repair.

## D. Non-claims (unchanged from freeze)

`claim_limit = "formal/interface discriminator only"`; no absolute globality, no new
kernel family, no paper-endpoint change, no scientific truth, no total epistemic space.
A parent-sufficiency win remains a valid terminal. AH30 (naturalistic transfer) remains
gated and not authorized by default.

## E. Post-outcome reviewer questions (additive; do not replace V2 questions)

These may be answered only AFTER a V2 judgment has been supplied and recorded.

- **E1.** Does a suite whose own invariance control refuses to attribute an interface
  effect (rather than silently proceeding) raise, lower, or not change your confidence in
  the programme's guarding against local-to-global overclaim?
- **E2.** Given outcome C1 — all arms making the *same* field-level error under different
  wrappers — is the recorded failure better described as a benchmark-contract ambiguity,
  a solver limitation, or evidence about the interface itself? Which description does the
  evidence support?
- **E3.** Given outcome C3, is "interface question open, representation limit recorded"
  the correct scientific status, or should the local-to-global residual be closed as
  unmeasurable in principle at this benchmark's granularity?
- **E4.** Does the AH20-R1 null change any answer you gave in V2? If yes, which item and
  in which direction?

## F. Addendum terminal

```text
CANONICAL_MANUSCRIPT = FLAGSHIP_V14
PACKET_VERSION = V2_PRE_AH20_OUTCOME + RESULT_ADDENDUM_AH20_R1
EL10 = PARENT_SUFFICIENCY_NULL_RETAINED
EL20 = CATEGORY_ERROR_AUDIT_PASS_RETAINED
AH10 = EXACT_REFERENCE_SEMANTICS_PASS
AH20 = CONTROL_DIVERGENT_NULL_RETAINED__NO_INTERFACE_EVIDENCE
AH30 = GATED_NOT_AUTHORIZED_BY_DEFAULT
FIELD_STATUS = HYPOTHESIS_NOT_FOUNDED
REVIEW_STATUS = READY_TO_BIND_GENUINELY_INDEPENDENT_REVIEWERS
```

**Artifacts:** `research/experiments/results/issue108/ah20-r1/` (RECEIPT.md,
DISPATCH_RECEIPT.json, EVALUATION_SUMMARY.json, PER_TASK_SCORING.json,
FROZEN_SUITE.json, PRIVATE_ORACLE_COMMITMENT.json, public_tasks.json).
