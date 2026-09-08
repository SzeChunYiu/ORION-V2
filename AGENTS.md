# ORION-V2 Agent and Contributor Constitution

## Status

ORION-V2 is post-freeze. The V1 architecture/local-formalism handoff is bound in `provenance/ORION_V1_HANDOFF_RECEIPT_V1.json`. Local reference implementation, unit tests and known-answer suites are authorized. Protected external evaluation and scientific-claim promotion are not.

Current programme terminal: `CONVERGENCE_ACTIVE`. First closeout blocker on the Wave-06 ledger: `BLOCKED_PARENT_BASELINE_BINDING` (not evaluator custody). Evaluator custody is a disclosed limitation (`NOT_OBTAINED__DISCLOSED_LIMITATION`, issue #37).

## Non-negotiable rules

1. **Do not mutate ORION V1 from this repository.** V1 results, failures and `CANNOT_CHECK` history remain immutable external inputs.
2. **No inherited atom or workflow.** Every V1 capability must receive a re-derivation disposition before admission to V2.
3. **Native donors remain identifiable.** Never erase the assumptions or judgments that make a donor strong merely to fit a common ORION representation.
4. **No prose-only promotion.** A surviving theory requires a quantitative/formal object, falsifier and machine-executable evaluation route.
5. **Similarity is contextual.** Every cross-domain neighbourhood claim must name its probes, interventions, decision class, resource bound and lost distinctions.
6. **Strongest donor product first.** If a native donor or their composition solves the proposed task, use it and contract the ORION claim.
7. **Authority stays external.** Research artifacts and local tests cannot self-promote scientific truth, novelty, V2 admission or constitution changes.
8. **Preserve negative history.** Nulls, harms, failed routes and censored searches remain addressable.
9. **Fail closed.** Search absence is not evidence of domain absence; ambiguous cells remain `CANNOT_CHECK`.
10. **Do not silently retarget the frozen parity subject.** Kernel blob changes require a new subject-binding identity. The named subject commit `f33d2f4…` must remain checkout-able or be rebound to a commit that exists.

## Repository ownership

- `research/`: prospective studies, donor reduction, and frozen experiment receipts.
- `papers/`: V2-only candidate publications; canonical writing also lives in `SzeChunYiu/ORION-paper`.
- `provenance/`: exact source, donor, mapping and decision identities.
- `src/orion_v2/`: candidate kernel (K0–K6 facade). Reference modules are importable; they are not a frozen solver.
- `tests/`: known-answer and hostile suites. A green run is engineering evidence only.
- `scripts/`: gates (`check_v1_handoff.py`, `pr_merge_gate.py`) and campaign runners.
- `development/`, `examples/`, `packages/`: unused stubs in this checkout — do not treat them as product surfaces.

## Required receipt chain

`source projection -> donor reconstruction -> structural mapping -> strongest donor product -> discriminator/falsifier -> protected evaluation -> external admission`.

## Merging

Every merge into `main` is decided by `scripts/pr_merge_gate.py` (six fields,
exit 0 only; see `docs/00-programme/PR_MERGE_GATE.md`): **base branch == the
repository default, read from the API and checked first** (a stacked PR whose
base already landed merges into that branch and reads `MERGED` while nothing
reaches `main` — FM40 stranding, recurred as #290), open, mergeable, not
draft, every check completed and not failing, and no changed path pinned by
digest in a live freeze on the base (the #282/#276 pair). Exit 1 names the
field; exit 2 is could-not-check and is never a merge -- a cancelled or
still-running check is 2, not a failure: re-run the workflow on this head. The
workflow `pr-merge-gate` is partial coverage, not enforcement: `main` has no
branch protection and the pair is only visible at merge time, so run the gate
then and record its verdict in the PR ("merge gate: exit 0 at <base sha>").
