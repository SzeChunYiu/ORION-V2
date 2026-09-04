# Authoring corrections and failure record

This file discloses development changes, not independent hostile review.

1. Before the first calibration, the log prototype used an unbound constant genesis.
Source inspection identified that replacing the initial snapshot could then preserve the
same event chain. Genesis was changed to bind schema and initial-state fingerprint; a
snapshot-substitution hostile now fails. No protected or confirmatory run occurred.

2. The first 33-test run passed. Its exact calibration is retained byte-for-byte in
`CALIBRATION_INITIAL.json`. Subsequent input-boundary review added four tests containing
seven failing subcases: truthy string/integer/None freshness premises, Boolean event-id
aliasing, non-string subject/payload and non-string predicate. The run was RED (37 tests,
seven failures), then exact type checks were added; the run became GREEN (37 tests).
The finite result remained byte-equivalent because the registered well-typed domain did
not change. Rejecting a string is not evidence that a real current-cut oracle exists.

3. The R5 rational policy grid is explicitly an illustration of a written impossibility
argument, not an empirical discovery. Likewise R8's two histories instantiate its stated
observation model. The receipt does not count either as independent experimental evidence.

4. No existing repository theorem, outcome, negative terminal, atlas or manuscript was
rewritten. The DESIGN.md committed before calibration remains byte-identical. A new
counterexample requires a successor record, not retroactive promotion of the predecessor.

5. After PR #326 was opened at `6e75df8e15b44c45202a140e1fc15ea52a463f11`, the
actual PR run list showed only path-filtered package/guard workflows, not the full unit
suite. The dedicated workflow was therefore extended with a sequential full `tests/unit`
regression job (no exclusions). The README's exit-code statement was narrowed to the study
and package verifier; unittest retains its native exit behavior. The receipt was rebound
for these CI/documentation-only changes. Model, test, design and finite-result bytes are
unchanged from that head. No scientific predicate, denominator or terminal was changed.
