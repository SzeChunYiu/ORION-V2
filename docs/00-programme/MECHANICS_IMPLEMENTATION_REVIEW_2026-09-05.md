# Mechanics implementation and issue review — 2026-09-05

This revision implements and reviews existing work across ORION-V2 and ORION-OCM.
It does not declare every research question solved. The [issue evidence audit](OPEN_ISSUE_EVIDENCE_AUDIT_2026-09-05.md)
preserves the initial 52 open V2 issues, 19 open PRs and the OCM roadmap evidence,
then separately records five justified issue dispositions.

## Implemented in V2

| Work | Concrete result | Scope |
|---|---|---|
| Foundation integration | Ten source PRs (#320–328, #331), 130 source files, conflicting package paths reconciled, complete source inventories and preserved receipts | Native finite studies retain their own hypotheses and judgments |
| Field dynamics (#345, source #346) | Field object, seven transition families, twelve law dispositions, controlled viability, finite information bound, quotient/revision commutation, resource accounting and OCM handoff | Exact finite models; general information principle remains open |
| Frontier F1/F2 (sources #330/#332) | Extraction certificates with explicit closed-family binding; exact multiscale parent reduction with warranted transitions | No universal no-drop claim; no silent empty-scope validation |
| Frontier F6 | Universal semantic invariance over all admissible completions, historical prefix checks, current LIVE/authorized commitments and immutable semantic inventory | Closed finite registered semantics; unrestricted English remains open |
| Lifetime batch 6 (source #347) | Correct predecessor/commit-prefix checks, small-sample and two-sided decision correction, information-budget and identification separation, optimized-interpreter refusal | Graded scalar projection and oracle-complexity claims explicitly contracted |
| Lane #202 F4 erratum | Directional compiler/time-envelope theorem and growing-gap counterexample to the previous absolute bound | Original F1–F3 and all pinned historical bytes preserved |

Integration details and exact source heads are in
[Foundation custody](../../research/machine-epistemics-theory/foundation_integration_v1/README.md),
[field validation](../../research/machine-epistemics-theory/field_dynamics_v1/VALIDATION.md),
[batch-6 review](../../research/machine-epistemics-theory/KSO_LIFETIME_BATCH6_INTEGRATION_REVIEW_V1.md), and
[the #202 correction](../../research/orion-machine/theory/OCM_LANE_202_RESOURCE_INVARIANCE_CORRECTION_V1.md).

Internal independent-agent reviews supplied concrete counterexamples for generator consumption,
malformed revision maps, incomplete source custody and semantic-digest validation. Authors fixed
them and reviewers rechecked the changes. This process is not the independent external assessment
required by the programme's scientific admission gates.

## Verified locally

Python 3.12.13, pytest 8.3.5, SymPy 1.14.0 where required:

- Complete collected V2 unit suite: **2,151 tests, zero failures/errors/skips**, 1,247.283 seconds.
- After final frontier and erratum edits: **165 targeted tests passed**, 15.62 seconds, covering
  field dynamics, F1/F2/F6, batch 6 and #202. This overlaps the full run and is not an additive count.
- Foundation integration replay: 19 commands returned their registered expected exits; complete
  source custody and finite conformance passed. The unavailable Lean route remains `CANNOT_CHECK`.
- V1 handoff validator: `V1_HANDOFF_VALID`. V1 was not modified.
- After incorporating upstream #347, merge-gate replay of `origin/main` (`1d06d8a`) against
  the local integrated head passed **field 5**: no live freeze pins a changed path. This replay
  does not check remote PR state or CI (fields 0–4) and is not permission to merge.
- Independent finite checks include 12,288 F6 semantic cases and 1,533 #202 compiler-contract
  cases, with 16 separately enumerated complexity minima. They do not establish empirical validity.

The dedicated mechanics workflow and Foundation integration workflow reproduce the relevant
finite checks and custody gates. Repository merge permission still depends on the six-field
`scripts/pr_merge_gate.py` verdict at the actual current base and head.

## Corresponding OCM implementation

The companion OCM revision fixes durable intent/checkpoint behavior, stale ledger CAS, restart
operator metadata, adoption predecessor binding, staged LIFO rollback, UNKNOWN interval replay,
derived-warrant revocation and honest remaining-alternative reporting. Population coverage now
produces a separate guarantee; an individual result requires its own exact checker for LIVE status.

KnowledgeSpace uses immutable structural indexes and exact positive support for large admission
queries. Measured synthetic admission speedups are 4.35×–15.92× at 256–4,096 atoms. Sparse numerical
checking is about 32% slower at 4,096 atoms because it now certifies the represented float system's
error bound. Neither measurement is a cognition or organisation superiority claim.

OCM's full collected suite passed 613 tests. The successor-receipt work separately preserves all
historical milestone receipts and marks same-scenario replays as engineering evidence. M11
historical adoption cells and M12 protected evaluation require renewed evaluation after the fixes.

## Remaining acceptance obligations

1. External assumption review, stronger-parent binding and protected evaluation cannot be replaced
   by same-session code checks or by rereading historical result JSON.
2. Frontier F3 needs an organisation/resource comparison with a genuinely matched strongest parent;
   F4/F5 need independently bound codec/semantic-fidelity evidence and actual runtime capability parity.
3. F7 requires a registered natural infinite learnable class and query/lifecycle/resource model.
   Finite version-space counts do not prove that theorem.
4. General field information laws, scalable synthesis, model validity and runtime absorption remain
   separate obligations. Host-supplied executable identity and arbitrary concurrent external effects
   are not certified by the reference mechanics.

Issue states should follow these exact acceptance scopes after integration, not the existence of
a document or passing local test. Five earlier explicit dispositions were closed: #37, #204 and
#205 at their recorded limited terminals; #213 and #214 as accidental placeholders. No positive
scientific result was manufactured for those closures.
