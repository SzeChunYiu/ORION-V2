# Lane #202 F4 correction: resource-bounded compiler inequalities

**Current status: `F4_ORIGINAL_FORM_REFUTED__SCOPED_COMPILER_BOUND_CORRECTION`.**

This successor has scope precedence over F4, the F4-dependent row of §4, and the
“F1–F4 supported exactly” sentence in
`OCM_LANE_202_TERMINAL_V1.md`. **F1–F3 and their numerical evidence are unchanged.**
Issue #202 remains open pending acceptance/integration of this correction.
No full architecture comparison, independent external review or mechanization
is supplied.

## Historical identity and reason for a successor

The original document is retained byte-for-byte because
`receipts/OCM_LANES_202_203_RECEIPT_V1.json` binds it:

- Source commit: `05f08fe71466d4dd192294fe00cf26d526026522`.
- Git blob: `eeec47166f557e681e0a93d47a4578fa788e155e`.
- SHA-256: `c064cb533f673b4c9b1499344497ad0557dc0058cb09f092ab9fc3c7d6514029`.
- Bytes: 9,753.

The original F4 asserted an absolute difference bound between time-bounded
description optima at one pair of budgets and inferred constant-factor slowdown
from mutual interpreters. Neither inference follows from those premises.
The original exact checker enumerates F1–F3; its “all-size authority” metadata
points to the written F4 argument and is not an executed simulation proof.
Its old receipt therefore cannot establish the corrected claim.

## Correct directional statement

Fix a finite nonempty task family F of input/output requirements, inputs of
length at most N, source description cap L, and source time bound t. Write

`C_U(F; L,t) = min {|p| : |p|≤L and U(p,x) returns the required output within t for every x in F}`,

with an infeasible minimum represented by a typed unavailable/infinite value,
never zero.

Register a compiler `τ_12` from U to U′ with all of these premises:

1. It preserves each registered task's output semantics.
2. `|τ_12(p)|≤|p|+c_12` on the admitted descriptions.
3. Every admitted source execution within t, description cap L and input cap N
   executes after compilation within the explicitly justified envelope
   `h_12(L,N,t)`.
4. The runtime model counts the compiler/interpreter work in the declared
   resource coordinates. Extra parser, verifier, precision, storage and
   preprocessing assumptions are not silently free.

If the source optimum is finite, then

`C_U′(F; L+c_12, h_12(L,N,t)) ≤ C_U(F; L,t)+c_12`.

**Proof.** Select a source minimizing program p. By the three compiler premises,
its translation solves F within the target description and time caps.
The target minimum is no larger than this particular translated program.
This is a one-sided feasible-witness argument. ∎

A reverse compiler separately proves

`C_U(F; L′+c_21, h_21(L′,N,s)) ≤ C_U′(F; L′,s)+c_21`.

It does **not** prove a bound on `C_U(F;L,t)` unless its translated witness
also fits that original L,t pair. In general applying both directions
composes time envelopes; it does not cancel them.

Mere mutual computable interpretation supplies no constant-factor runtime
envelope. Such a bound must be proved for the actual compiler and machine
model. Even when both factors are constant, the absolute-gap claim still
fails, as the following example shows.

After **removing the runtime bounds**, two semantics-preserving description
translations with additive overheads do give the usual two directional
description inequalities and hence an absolute difference bounded by the larger
overhead. The familiar invariance theorem concerns appropriate universal/
optimal description languages. It does not restore the unsupported
same-paired-budget time-bounded statement. Parent ownership is retained; this
correction introduces no novel complexity principle.

## Exact executable counterexample with constant-factor compilers

Two fixed transducers A and B read binary programs:

- `0w` outputs literal binary word w.
- `1bin(n)` outputs n zeros, where n is positive and its binary encoding is
  canonical.

Both charge one abstract decode tick per program bit and one write tick per
output bit. A additionally charges 2n padding ticks for run-length programs;
B does not. All other behavior is identical. Identity is a semantics-preserving
compiler in **both** directions, with description overhead **zero**, and each
translated runtime is at most **three times** its source runtime.

For task F_n (“output n zeros”), the grammar has exactly two candidate programs:
the literal of length n+1 and the run-length code of length 1+bit_length(n).
Set t_n=2n+1.

The literal takes t_n ticks on both machines. A's run-length code takes
`1+bit_length(n)+3n>t_n`, whereas B's takes
`1+bit_length(n)+n≤t_n`. Therefore, with an adequate shared description cap,

`C_A(F_n;t_n)=n+1` and
`C_B(F_n;3t_n)=1+bit_length(n)`.

Their gap is `n-bit_length(n)`, despite zero description overhead and both
runtime factors being three. At n=8 this is **9 versus 5 bits** at budgets
**17 versus 51 ticks**. The reverse compiled short program executes on A in
29 ticks: it meets the reverse compiler's relaxed bound but not the original
17-tick source budget.

The gap is not repairable by choosing a larger constant independent of F:
for any integer c≥0 choose `n=2^(c+2)`; then
`n-bit_length(n)=2^(c+2)-(c+3)>c`.
This all-size conclusion is a written argument for these fixed program
languages, not extrapolation from the finite enumeration and not a universal
architecture lower bound. The transducers are deliberately simple and are not
claimed to be universal computers. They already satisfy the original stated
“mutual interpreters” premise and the additional constant-factor condition.

The independent claim that mutual interpretation guarantees constant slowdown
also fails: make A's padding n² while keeping B unchanged. The compiler runtime
ratio on run-length code grows proportionally to n. That is a separate
written countermodel; the executable calibration below uses the stronger
**constant-factor** example, so it does not rely on this missing premise.

## Calibration, controls and limits

Checker:
`research/orion-machine/reference/ocm_lane202_invariance_correction_exact.py`.

Tests:
`tests/unit/test_ocm_lane202_invariance_correction.py`.

The registered finite inventory has n=1…128, two programs per target, and two
compiler directions: **512 program-contract checks**. Both directional
inequalities hold. The invalid absolute zero-overhead bound fails on
**126/128 targets**; the largest registered gap is **120 bits**.
These counts are computed from actual interpreter runs and exact minima.

Controls alter a compiled program to a different output and separately claim
an unearned factor-one reverse runtime bound. Both are detected. Missing/
noncanonical programs, unknown machines, non-materialized inventories,
Boolean numeric aliases and targets outside the explicit cap return
`CANNOT_CHECK`. Infeasibility remains distinct from zero description cost.

The meter is an explicitly registered abstract decode/write/padding model.
It is not Python wall time, bit-complexity of an implementation, or a
whole-system production benchmark. Static substrate descriptions and any
additional resource coordinates remain separate. This is a corrective
counterexample to a claimed mathematical implication, not an efficiency win
for either transducer or OCM.

The successor receipt records the actual interpreter, command exits, new file
hashes and original historical hash. It grants no closure of #199/#245,
architecture equivalence, scientific novelty, field recognition or OCM
adoption.

