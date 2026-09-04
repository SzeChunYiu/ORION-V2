# Concurrent main reconciliation and an additional stopping counterexample

Observed after the core RECEIPT.json was generated: ORION-V2 main advanced from
24566f00a9dc4425a438fcfac05d13c6b2d903db to
`d756c086edc46ad4e5e682f69730b72c1dc26a4c` through merged #317.
Read target: `research/machine-epistemics-theory/KSO_ONE_DAY_THEOREMS_BATCH1_V1.md`.
The core receipt remains immutable and binds its seven source files. This note and
`stopping_counterexample.py` are a separate, later additive extension, bound by their
Git commit rather than retroactively inserted into the core receipt.

## Overlap disposition

The new batch already corrects several atlas overstatements: T4 records changed
normalization after revocation, T5 makes interference an upper bound, T9 rejects general
information subadditivity, and T10 checks compatibility of a new upper profile. These
agree with F10, F07, F13 and F15 here. They are parallel corroborating derivations, not
independent external replication and not multiple novel contributions. No #317 file is
replaced by this package. Its canonical-object calibration and our typed risk/graded
extension have different scopes.

## C01: T2(c)'s claimed earliest deciding budget is false

T2(c) starts from a_k < theta and defines k' by shrinking the global tail width below
theta-a_k. It then claims no earlier budget can decide. That only reasons about the
upper endpoint; an increasing LOWER endpoint can cross theta earlier and certify FOUND.

Take the one-state system P=[1], s=[1], alpha=1/2 and theta=3/5. Exact iteration gives

    a_k = 1 - 2^(-(k+1));  w_k = 2^(-(k+1)).
    a_0 = 1/2; a_1 = 3/4.
    theta-a_0 = 1/10.

The proposed width rule first gives k'=3, since w_2=1/8 >= 1/10 but w_3=1/16 < 1/10.
Nevertheless k=1 already certifies FOUND because 3/4 >= 3/5. This refutes the minimality
claim, not T2's Neumann-sum/error bound or the soundness of a lower-bound FOUND.

Correct decision rule at EACH recomputed iteration j:

    YES when a_j(t) >= theta;
    NO when a_j(t)+w_j < theta;
    UNRESOLVED otherwise.

The width test against an old lower endpoint cannot establish the earliest deciding
iteration. A residual or coordinate-specific error enclosure may be sharper than w_j;
its calculation and cost must be charged. The rule may also use a separate exact solver
or other justified certificate, rather than pretending the tail bound is the only route.

## C02: convergence need not yield a finite threshold certificate

In that same system take theta=1=a*. Every finite k has a_k < 1 and a_k+w_k=1. The
interval rule stays UNRESOLVED although the limiting predicate a*>=theta is true. This
holds for all finite k by the displayed closed form, not by extrapolating a finite run.
A positive decision margin, a separate equality proof, or a typed unresolved exit is
needed. Convergence alone does not provide finite threshold completeness.

## Remaining scope differences to review

T6 defines singleton selection as a policy; F12 additionally permits sound query
consensus across several interpretations. This is a less restrictive alternative, not
a claim that singleton selection is internally inconsistent. T8's natural-number meter
fixes the real-valued Zeno issue, but total-run termination also needs to bound repeated
query invocations. Snapshot-repeatability is not a substitute for validating concurrent
state-changing commits; F07 supplies the write-skew warning. These qualifications should
be reconciled before promoting the combined results to one canonical runtime contract.

## Executed calibration

Command (same isolated Linux/Python 3.13.5 environment as the core receipt):

    python research/machine-epistemics-theory/foundation_v1/stopping_counterexample.py

Exit 0; terminal COUNTEREXAMPLE_REPRODUCED; claimed_earliest_budget=3;
actual_first_FOUND=1; threshold_equality_controls=21 (k=0..20). Arithmetic is exact.
The all-finite-k equality argument is above. No OCM run, new protected experiment,
independent review, source saturation or novel-theorem claim follows.
