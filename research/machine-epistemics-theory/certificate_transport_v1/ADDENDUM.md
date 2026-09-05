# Deductive addendum — certificate transport V1

This addendum is written after the first primary finite calibration (10,240 joint-frontier and 28,160 audit-parent cells passed) and before executing the supplementary checks below. It is not a retrospective claim of pre-registration. The original protocol, grid, endpoints, and adverse outcomes are unchanged.

## Sharper joint frontier (CT-03b)

Removing a point from the old failure event cannot help its worst-case risk and costs nonnegative change mass. Therefore an optimal change only adds failures from S = U minus F. Let K be the largest subset mass P(I) <= eta over I subset S. If a nonempty failure event is feasible, the exact joint bound is min(1, P(F)+K+epsilon); otherwise it is zero. Nonempty feasibility must be tracked separately when K=0 because zero-reference-mass atoms may carry deployment mass. This is an ordinary subset-sum parent, not a new optimizer.

Supplementary comparator: a reachable-mass dynamic program, with representative masks preserving nonempty support at zero mass, versus the original exhaustive joint_frontier. Use exactly the original 10-distribution / 8-old-mask / 8-mutable-mask / 4-epsilon / 4-eta grid. Report 10,240 paired comparisons if all execute. All masses are exact rational input, not estimated probabilities.

## Audit complementarity (CT-09)

Under the original no-change transcript semantics and A subset S = U minus F, define risk reduction g(A)=R(empty)-R(A). Deductive target: g is monotone supermodular, NOT generally submodular. Away from the empty-event boundary it is a convex positive-part transform of covered mass; when F is empty it additionally includes epsilon times the indicator that every potentially changed atom was audited. That indicator is supermodular. The empty universe is handled separately.

Witness: P=(1/2,1/2), F=empty, U=both atoms, epsilon=1/2. Either singleton audit has zero benefit; both audits eliminate every possible failure. This does not say all greedy methods fail; it rejects an unjustified diminishing-returns argument and a stop-on-zero-single-step-benefit heuristic.

Supplementary exact checker: on the original P/F/U/epsilon grid, enumerate all A,B subset S and test g(A)+g(B)<=g(A union B)+g(A intersection B), plus monotonicity on nested pairs. Counts are measured. Keep the strict two-atom counterexample to submodularity. No empirical or asymptotic superiority claim is added.

These are analytic extensions within one session, not independent review. Parent attribution and full preprocessing/arithmetic/state costs remain mandatory. The formula is exact for the registered arbitrary binary failure-event class; restricting to a realizable backend class can turn it into a conservative relaxation.