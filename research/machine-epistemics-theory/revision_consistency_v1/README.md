# Machine Epistemics: revision-consistency foundation fragment

**Terminal: CORRECTED_FOUNDATION_FRAGMENT. Parent disposition: PARENT_SUFFICIENT.**
**Overall Machine Epistemics foundation: OPEN_RESEARCH.** No OCM adoption is authorized.

This additive package supplies written scoped proofs/counterexamples and a stdlib-only
finite checker for certificate context, revision freshness, concurrent commitment,
historical replay and effect acknowledgement. It corrects the MEG-30 inference that
immutable snapshots make interleavings serializable, without changing the frozen atlas.

## Run from any checkout

```sh
D=research/machine-epistemics-theory/revision_consistency_v1
python -m unittest discover -s "$D" -p test_model.py -v
python "$D/study.py" --verify "$D/RESULT.json"
python "$D/verify_package.py" --verify
```

Requires Python >=3.12, standard library only. Each verification command exits 0 on its
specified checks, 1 on a defect, 2 when required input is unavailable. Neither exit 0 nor
an artifact hash grants scientific truth, external review, production atomicity or OCM
milestone closure. `verify_package.py --write` is for issuing a new authoring receipt, not
for repairing a frozen receipt after unnoticed drift.

## Evidence with denominators

| object | exact finite result |
|---|---|
| R1 context sufficiency | 256 cases; 60 sufficient, 196 insufficient; two implementations agree |
| R2 dependency binding | 11 influential-coordinate mutations reopen; predicate-insertion mutant caught; unrelated-change control passes |
| R3 write skew | 4/6 schedules violate the joint invariant under snapshot-only validation; 0/6 under full readset validation |
| R4 candidate versus readset parent | 2,916 combinations, 0 disagreements; PASS 1, FAIL 1,026, CANNOT_CHECK 1,863, REOPEN_REQUIRED 26 |
| R5 freshness | two locally indistinguishable histories; five probability-grid illustrations, NOT an empirical sample |
| R6 historical replay | 4/4 prefixes verify against their own anchor; only 1/4 matches the final anchor; 4/4 unanchored cases CANNOT_CHECK |
| R7 causal closure | 1,098 cuts of 75 ordered DAGs through four vertices, 0 direct/transitive-check disagreements |
| R8 effect boundary | two histories share a local intent but have different external effects; no external effects executed |

The R4 matrix contains only **one accepted case**; it is not 2,916 successful commitments.
Unit tests additionally admit unchanged/unrelated states and a newly revalidated ABA state.
`CALIBRATION_INITIAL.json` and `CORRECTIONS.md` preserve the development record.

## Artifacts and review

`DESIGN.md` was committed before finite calibration at `59b6819574f494354b880605998ffddbc5687077`.
`THEORY.md` states the object, assumptions, proofs, counterexamples, resources and open
refinements. `SOURCES.md` binds the primary-source reading scopes and parent subtraction.
`model.py` has separate candidate and parent validators. `study.py` recomputes `RESULT.json`.
`test_model.py` contains the hostile and no-alarm suite. `RECEIPT.json` binds the complete
package input list; it deliberately does not hash itself. The independent trust anchor
is the externally supplied repository commit, not the receipt's self-assertion.

Analytic review assignments in this authoring session (not external experts):
formal epistemics checked that applicability is not truth; distributed consistency
constructed write skew and delayed-revocation histories; proof/refinement checked each
premise against the reference; resource review rejected free full-state hashing;
hostile-parent review required the equally informed readset comparator and challenged
truthy unknowns, phantom insertions, ABA and self-anchored replay. The corrective record
is in `CORRECTIONS.md`. Independent assumption review remains NOT_OBTAINED__DISCLOSED_LIMITATION.

## OCM absorption contract — not implemented here

OCM must supply authenticated checker/permission records, a proved-complete dependency
footprint including negative predicates, correctly updated guards, and a real atomic
validation-to-commit boundary. Its fresh-cut claim needs evidence or a registered weaker
consistency contract. The model's Boolean premise is **not** a production implementation.
A post-action receipt must not mint the prior permission. Historical replay must not be
labelled current validity. Unknown checker, missing authority, insufficient budget and
unavailable freshness remain separately visible non-successes.

An OCM adapter needs parity against the finite reference plus real transaction/crash tests,
including revoke-between-check-and-use, predicate insertion, stale model/checker/context,
cross-domain shared dependencies, changed operator code, and ambiguous external effects.
Changing a caller's Boolean or locally recomputing a hash cannot pass these obligations.

## Work division and limitations

Base: V2 main `24566f00a9dc4425a438fcfac05d13c6b2d903db` (#310). Parent #197; division #304.
This directory complements, does not replace, #312/#313 typed foundation and #314 decision
frontier work. It changes no OCM runtime, paper, protected experiment or existing freeze.

Small exact checks ran in the isolated Linux analysis container; direct GitHub clone failed
DNS. This local materialization is NOT a complete clean clone. Remote CI uses an actual
checkout; its eventual status is reported in the PR rather than asserted in this file.
No protected Mac/LUNARC run, external reviewer or full local repository test is claimed.

The eight scoped arguments are complete as written under their premises, but are not
proof-assistant checked. New model/empirical bridge and cryptographic authentication are
not supplied. Follow-on research is specified in THEORY.md §9. No novelty, superiority,
field establishment or full-foundation closure is inferred from these results.
