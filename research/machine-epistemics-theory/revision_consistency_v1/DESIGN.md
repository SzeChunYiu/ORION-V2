# Revision consistency V1 — pre-calibration design

TASK_ID: ME-REVISION-CONSISTENCY-V1. Parent: #197; division: #304.
Base: 24566f00a9dc4425a438fcfac05d13c6b2d903db (#310).
Branch: research/me-revision-consistency-20260904.

This additive theoretical study addresses certificate applicability, immutable snapshots,
concurrent commitment, causal cuts and revision freshness. It does not own the typed
risk/warrant or graded-dynamics work in #312/#313, or decision optimization in #314.
Only this directory and .github/workflows/me-revision-consistency.yml are in scope.
Existing atlas statements and scientific terminals are retained, not overwritten.

## Declared objects and boundaries

A finite registered store has named versioned cells; every mutation advances the relevant
version, including a protected predicate-generation cell for insertions into a queried
namespace. A specification states the actual dependency set, required values, subject,
payload and absence predicate. Checker judgments and commit permissions are separate
trusted inputs in the model. An immutable snapshot records a historical state, NOT a
promise that no later revocation occurred. A validation-to-commit step is one indivisible
transition only in the abstract model; production atomicity is an implementation obligation.
No code here performs an external action or authenticates a real authority.

## Targets declared before running the finite checker

R1: a descriptor is sufficient for transporting a judgment exactly when that judgment is
constant on descriptor fibres; omitting an influential configuration coordinate fails.
R2: complete versioned dependency validation preserves applicability under unrelated
changes; absence/predicate dependencies must be included; changed dependencies reopen.
R3: immutable snapshots alone do NOT entail serializability (MEG-30 correction, write skew).
R4: atomic current validation plus prior authority preserves the commitment precondition;
splitting validation from commitment admits a revoke-between-steps counterexample.
R5: under asynchronous unbounded delay, a useful terminating affirmative decision cannot
guarantee globally current revocation validity without additional information/coordination.
R6: a log can replay exactly yet be an old or truncated valid prefix; an externally fixed
checkpoint certifies completeness only to that checkpoint, not freshness beyond it.
R7: causally closed cuts reject missing predecessors, but do not alone enforce a joint
application invariant across concurrent changes.
R8: without atomic effect/receipt or an adequate external reconciliation interface, a crash
can leave effect-happened and effect-not-happened histories observationally identical.

## Finite calibration and controls

Enumerate registered small cell assignments, dependency mutations, interleavings and DAG
cuts (at most four event vertices). No stochastic or protected seed is used. Run distinct
reference and candidate validation implementations against the same declared information.
Record denominators from loops, not constants presented as observations. Each target gets
a planted defect plus a valid no-alarm witness; missing checker/freshness/budget is distinct
CANNOT_CHECK, never a successful judgment. Test canonical serialization and fresh-process
replay. Exact finite enumeration calibrates code; written arguments carry all-size claims.

## Expected ownership and execution

Transactional validation, linearizability, snapshot-isolation counterexamples, consistent
cuts, complete mediation and asynchronous indistinguishability have established parents.
Expected parent disposition: PARENT_SUFFICIENT within the registered model. No novelty,
architecture superiority, independent review, field recognition or OCM adoption is granted.
Internal review roles: formal epistemics; distributed consistency; proof/refinement;
resource accounting; hostile parent. These are analytic roles in one authoring session.

Execution uses the actual isolated Linux analysis container, not the operator's Mac or
LUNARC. A direct git clone failed DNS; connector access works. Local materialization is
not a full clean clone. Full repository checks will be attempted through GitHub CI and
reported separately. The first source-level counterexample ideas are already known from
inspection: this is not an outcome-blind empirical experiment. Later changes require a
recorded correction, not retroactive rewriting of this design.

Allowed package outcomes: CORRECTED_FOUNDATION_FRAGMENT, REFUTED_ORIGINAL_STATEMENT,
PARENT_SUFFICIENT, OPEN_RESEARCH, CANNOT_CHECK. Overall foundation closure remains OPEN.
