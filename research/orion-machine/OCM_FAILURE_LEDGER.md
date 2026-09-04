# ORION Cognitive Machine failure ledger

Umbrella: ORION-V2 #194
Execution master: ORION-V2 #197
Focused P0: ORION-V2 #221
Independent review: ORION-V2 #199, #245

**Status: `APPEND_ONLY__NO_NOVELTY_OR_BREAKTHROUGH_CLAIM`.**

This ledger follows the form of the repository's root `FAILURE_LEDGER.md`. Failure history is
append-only: a repaired defect remains visible, and **a later green result may not erase how it was
obtained**. Nothing recorded here grants scientific, novelty, priority, architecture, language,
quantum or publication authority.

Scope. This ledger holds process, custody and import-authority failures of the OCM programme. The
scientific negatives of the revocation-complete-learning lane — the eleven killed or threatened
claims `RCL-F01` through `RCL-F11`, each with its disposition, strongest reason and reopen condition
— live in
`research/orion-machine/revocation_complete_learning/RCL_FAILURE_AND_PARENT_COLLAPSE_LEDGER_V0.md`
and are **referenced, not restated**, so that they have exactly one home.

## Retained failure classes

These are failure vocabularies to keep detecting, not a claim that every class currently has an open
critical defect.

- `BINDING_OVER_UNCOMMITTED_BYTES` — a content binding is computed over a working-tree or pre-commit
  draft rather than over the committed blob, and the artifact then enters version control at a
  different length. Every downstream receipt inherits the wrong digest. The failure is invisible to
  every custody instrument the repository has, because each of them compares a recorded digest
  against the bytes that *are* there and correctly reports a mismatch — while no instrument can say
  whether the bytes that *were* recorded ever existed. Distinct from
  `NONREPRODUCIBLE_FROZEN_ARTIFACT` in the root ledger: there the artifact is regenerable and the
  regeneration differs; here there is nothing to regenerate, and recovery is impossible **by
  construction rather than by loss** — the referent was never pushed, so no search of the repository,
  however exhaustive, can reach it. The tell is a `git log --all --full-history` on the path
  returning only the creating commit while the recorded length has never occurred on it. Guard:
  compute every binding from the committed blob (`git show <commit>:<path>`), never from a file on
  disk; and when a drift is found, re-bind with the superseded binding retained and the disposition
  stated, rather than silently replacing it. First observed 2026-09-03, recorded 2026-09-04
  (`RCL_FAILURE_AND_PARENT_COLLAPSE_LEDGER_V0.md`; see the concrete record below).

- `RECORDED_REPAIR_NEVER_LANDED` — a receipt records a checker defect as discovered *and repaired*,
  with the repair stated verbatim, while the module it names still carries the unrepaired value. The
  receipt is internally consistent, the repair description is correct, and the code is wrong; a
  reader auditing the receipt finds a closed defect, and a reader running the module finds a red
  suite. The two never meet, because nothing binds a `repaired` field to a landing commit. Guard: an
  entry under a `discovered_and_repaired_*` key must cite the commit that landed it, and the repaired
  value must be asserted by a test that runs in CI — a repair recorded only in prose is a plan, not a
  repair. First observed 2026-09-03, landed 2026-09-04 (see the concrete record below).

- `DANGLING_CROSS_REFERENCE` — an artifact or issue names an issue or pull-request number as the
  source of authority for something it does not itself establish, and the number resolves to an
  unrelated object. Because GitHub numbers issues and pull requests from one sequence, a number
  written before the object exists will later denote *something*, and that something reads as
  confirmation. The failure is silent in both directions: the citing artifact looks well referenced,
  and the cited object carries no sign that anything points at it. Guard: resolve every imported
  number against what it names — state, title, changed paths — and record the resolution, not the
  number. First observed 2026-09-04 (see the concrete record below).

- `IMMUTABLE_TARGET_MUTATED_BY_ITS_OWN_BINDING_TEST` — an artifact is published as a frozen,
  immutable review target *and* carries a hash-binding self-test that walks every artifact it binds.
  The two properties are incompatible: any correction to any bound artifact forces an edit to the
  frozen target, or its own test fails. Freezing and self-verification pull in opposite directions,
  and the conflict surfaces only when the first correction arrives — at which point the least-bad
  action is to edit the immutable file and disclose it. A second-order consequence follows: the
  target's recorded `base_sha` or head then names a commit that is no longer the branch head, so an
  independent reviewer following the published pointer inspects a different tree from the one under
  review. Guard: separate the frozen statement of the review question from the mutable binding table
  it refers to, so a re-bind never edits the frozen half; and when a published target does move,
  announce the move on the issue that administers it rather than leaving the reviewer to discover it.
  First observed 2026-09-04 (see the concrete record below).

## Retained concrete failure records

- **`BINDING_OVER_UNCOMMITTED_BYTES` — RCL parent-collapse ledger, 2026-09-03/04.** The binding
  recorded in commit `4655495` for
  `research/orion-machine/revocation_complete_learning/RCL_FAILURE_AND_PARENT_COLLAPSE_LEDGER_V0.md`
  is 4,751 bytes / `466e6da9…`; the bytes actually committed are 4,746 / `12ca96d8…`. The artifact
  and both receipts that bind it were created together in one all-insertions commit across 18 files.
  Three searches with stated scope agree that only `4655495` and its merge `7015cdb` ever touched the
  path — `git log --all --full-history`, an object-store scan of 6,765 objects that found the
  4,746-byte blob as its control, and the GitHub commits API for the branch, which closes the gap the
  shallow clone leaves. **The file has never existed in version control at its recorded length**, so
  there was no clean version to restore. Six reconstruction sweeps — 5-gram over 4,747 positions,
  inflection-aware anomaly scan, space-multiset over 16,108,764 multisets, structured whitespace over
  113 enumerated combinations, typographic/encoding over 33.6M candidates, and whole-word omission
  across 5,007 words — each carried a positive control that fired, and none produced the recorded
  hash. **This is birth drift, not corruption.** Disposition `DRIFT_RECORDED_NOT_BLESSED`: the
  binding was re-taken over the committed bytes with `superseded_binding` retained in every receipt
  that carries it, nothing above the custody note was altered to make hashes agree, and nothing was
  overwritten. What remains open is whether the pre-commit draft differed in substance or only in
  transport formatting; that is not determinable from any source reachable from this repository. No
  claim, disposition, strongest reason or reopen condition in the RCL ledger is changed by it.
  Record: the artifact's own section *Custody note — binding re-freeze 2026-09-04*; audit row
  `IA-04` in `research/orion-machine/OCM_SNAPSHOT_V1.json`.

- **`RECORDED_REPAIR_NEVER_LANDED` — WLL interface hierarchy, 2026-09-03/04.**
  `research/orion-machine/receipts/OCM_WLL_P0_THEOREM_BUNDLE_RECEIPT_V1.json` records, under
  `discovered_and_repaired_checker_defects`, the defect *"endpoint parity relation counted as one
  individually known target coordinate"*, its effect *"endpoint-only safe coverage overstated by one
  coordinate"*, and its repair *"correct endpoint-only guaranteed coordinates from one to zero and
  abstentions from five to six"*, with `theorem_statement_changed: false`. The repair was not in
  `research/orion-machine/reference/ocm_wll_interface_hierarchy_exact.py`, which still pinned
  `I0_ENDPOINT_ONLY` at `(answerable=1, abstentions=5)` while the registered 256-world model yields
  `(0, 6)`. The module failed its own calibration and took five CI checks down with one root cause.
  **The gate was strengthened, not relaxed**, when the recorded repair was landed in commit
  `4cb6dca`: `THEOREM_BOUNDS` now holds the Section 6 lower bounds *as bounds*; `TARGET_WIDTH` with
  an assertion that `answerable + abstentions == target_width` pins the denominator, so a bound
  cannot be satisfied vacuously by `(0, 0)`; `REGISTERED_MODEL_VALUES` retains the exact measured
  pair, so drift detection is no weaker than before; and Theorem WLL-8 monotonicity — coverage
  non-decreasing and abstention non-increasing along the refinement chain — is newly asserted on
  measured metrics. Mutation controls M1 through M5 are each caught, with the unmutated case M0 as
  the no-alarm control. No theorem, computation or claim changed. Verified under Python 3.12.13,
  matching the CI pin. Record: audit row `IA-05` in `OCM_SNAPSHOT_V1.json`.

- **`DANGLING_CROSS_REFERENCE` — draft-carrier number 226, 2026-09-04.** Issue #221 carries the
  header *"Active draft: #226"*, and the field `draft_pr: 226` appears in both
  `research/orion-machine/receipts/OCM_WLL_P0_THEOREM_BUNDLE_RECEIPT_V1.json` and
  `research/orion-machine/theory/OCM_WLL_CANDIDATE_TERMINAL_V3.json`. Pull request 226 is
  *"pra-r1: protected run under operator authorization — outcome receipt
  (CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE)"*, head ref `pra-r1-outcome`, merged
  2026-09-03T00:17:48Z. It changes four files, all under
  `research/llm-machine-epistemics/results/pra-llm-r1/`, and **zero** files under
  `research/orion-machine/`. Issue #221 was created at 00:05:27Z, four minutes before pull request
  226 was opened at 00:09:48Z: the number was written before it denoted anything, and then came to
  denote a different research line. The actual carriers are pull requests #244 and #254, established
  by enumerating the changed files of all 188 pull requests of this repository in every state, which
  returns 22 and 30 paths under `research/orion-machine/` respectively and 0 for every other pull
  request. No frozen receipt was edited to correct this; the reference is recorded as dangling.
  Record: audit row `IA-01` in `OCM_SNAPSHOT_V1.json`.

- **`IMMUTABLE_TARGET_MUTATED_BY_ITS_OWN_BINDING_TEST` — RCL review packet V0, 2026-09-04.**
  `research/orion-machine/revocation_complete_learning/RCL_INDEPENDENT_REVIEW_PACKET_V0.json` is the
  frozen hostile-review target published to issue #199 and is declared immutable
  (`RCL_INDEPENDENT_REVIEW_PACKET_V1.json`: *"V0 remains immutable"*). Its own hash-binding test
  walks every entry of its `artifacts[]` array, so the ledger re-bind above forced an in-place edit
  of the frozen file. The edit was made, every non-`artifacts` key was verified byte-for-byte
  unchanged, and the change was disclosed inside the packet itself. The second-order consequence is
  the operative one: the packet's `base_sha`, `7ae42207…`, is no longer the head of the branch it
  names, which is at `d4eb281` — and issue #245 records a *"Current rebased head"* of `7015cdb`,
  which has since advanced by four commits. **An independent reviewer following either published
  pointer would inspect a different tree from the one under review.** The administrators of #199 and
  #245 have been told the target moved. Record: audit rows `IA-02` and `IA-03` in
  `OCM_SNAPSHOT_V1.json`.

### Unreturned by construction, not repaired

Issue #221's deliverable 10 — *"independent hostile review stating which candidates collapse and what
exact residual remains"* — is `NOT_OBTAINED__DISCLOSED_LIMITATION`, and so is the parallel review of
issue #245. This is **not** a pass and **not** `CANNOT_CHECK`: the check is well defined and
executable by any independent party, and it simply has not been performed. No review was simulated,
role-played or generated. Issue #221's own gate reads *"same-session theorem authorship cannot close
the independent review issue #199"*, and a generated reviewer would supply from inside the authoring
session exactly the external authority this P0 exists to withhold — which would poison a
parent-subtraction record whose entire purpose is to keep that authority external.

The cost is named rather than absorbed: `literature_priority_established: false`,
`novelty_established: false` and `clean_post_material_passes: 0` remain as the carriers record them;
every `promotion_blockers` and `blocking_obligations` list in those carriers names independent
hostile proof reconstruction, so no candidate advances past its recorded terminal; and `RCL-F10`
stays `BLOCKED` with `RCL-F11` `BLOCKED_HIGH_COLLISION`. The smallest next action is to route issues
#199 and #245 to a party outside the authoring sessions.

## Reopening rule

This ledger reopens on any of the following, each of which produces a *passing* artifact and is
therefore invisible to a green suite:

- a content binding is shown to have been taken over bytes that never entered version control, or
  over a working-tree file rather than a committed blob;
- a receipt-recorded repair is shown to be absent from the module it names, or a `repaired` entry is
  found that cites no landing commit and is asserted by no test that runs in CI;
- an imported issue or pull-request number is shown to resolve to an object other than the one the
  citing artifact describes;
- a published review target is shown to name a commit that is no longer the head of the branch under
  review, or a file declared immutable is shown to have been edited without disclosure;
- an independent review terminal is found to have been produced by, or on behalf of, a session that
  authored the work it reviews.

A verdict resting on any of these is withdrawn to `CANNOT_CHECK`. It is not converted into a repaired
defect, and a later green result does not erase how the earlier one was obtained.
