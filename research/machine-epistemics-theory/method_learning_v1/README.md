# Methods that generate checked methods

The [theory](THEORY.md) gives scoped convergence statements for finite total
program search, learned fragment generators, polynomial verification and
deterministic experimental identification. The construction is parent-owned;
no unrestricted scientific convergence or novelty is claimed.

Run `python research/machine-epistemics-theory/method_learning_v1/check.py`.
The independent finite checker covers 512 identification instances and 1,024
fair-scheduling ranks. The same checks pass under `python -O`.

Validation also ran the method contract, semantic codec and infinite threshold
lifecycle tests together: **85 passed**. The immutable source/check record is
[RECEIPT_V1.json](RECEIPT_V1.json).

The companion implementation is in ORION-OCM:

- `src/ocm/learning/methods.py`: total arithmetic methods, learned fragment
  generators, held-out comparison and revocable KSO admission.
- `src/ocm/science/finite_identification.py`: experiment selection, finite
  version spaces, contradictory observations and revocation.
- `ocm methods`: installed-package demonstration with checked mathematical
  solutions, restart, revocation and explicitly simulated science.

This packet advances the bounded reference mechanics behind #345, #329 and
the recursive-method questions in #48–#50. It does not close their external
evaluation, unrestricted-language, stronger-parent or independent-review gates.
