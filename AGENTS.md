# ORION-V2 Agent and Contributor Constitution

## Status

ORION-V2 is a pre-implementation research programme until the exact ORION V1 freeze identity is bound.

## Non-negotiable rules

1. **Do not implement V2 before V1 freeze.** Pre-freeze work is limited to research, donor reconstruction, theory reduction, schemas, protocols, fixtures, issue planning and paper planning.
2. **Do not mutate ORION V1 from this repository.** V1 results, failures and `CANNOT_CHECK` history remain immutable external inputs.
3. **No inherited atom or workflow.** Every V1 capability must receive a re-derivation disposition before admission to V2.
4. **Native donors remain identifiable.** Never erase the assumptions or judgments that make a donor strong merely to fit a common ORION representation.
5. **No prose-only promotion.** A surviving theory requires a quantitative/formal object, falsifier and machine-executable evaluation route.
6. **Similarity is contextual.** Every cross-domain neighbourhood claim must name its probes, interventions, decision class, resource bound and lost distinctions.
7. **Strongest donor product first.** If a native donor or their composition solves the proposed task, use it and contract the ORION claim.
8. **Authority stays external.** Research artifacts and local tests cannot self-promote scientific truth, novelty, V2 admission or constitution changes.
9. **Preserve negative history.** Nulls, harms, failed routes and censored searches remain addressable.
10. **Fail closed.** Search absence is not evidence of domain absence; ambiguous cells remain `CANNOT_CHECK`.

## Repository ownership

- `research/`: prospective studies and donor reduction.
- `papers/`: V2-only candidate publications; no final numbering without programme authority.
- `provenance/`: exact source, donor, mapping and decision identities.
- `development/`: blocked until V1 freeze except for non-executable packet specifications.
- `src/`, `packages/`, `scripts/`: blocked from V2 implementation before V1 freeze.
- `tests/`: pre-freeze known-answer and hostile specifications only; outcome-generating execution is blocked.

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
