# Checked methods and generators of methods

Status: `PROVED_SCOPE_LIMITED` for the statements below; `PARENT_SUFFICIENT` for
the construction. This is an additive research reference. It grants no new
protected outcome, general intelligence, external scientific truth, or novelty.

## Object and progression

A problem is `(input domain, specification, checker, resource envelope)`.
A method is a finite program. A generator is an ordered search over methods.
A meta-method uses checked training solutions to propose a new generator.
Generator effectiveness is checked on different mathematical task identities.
Learned priorities never change the specification or the checker.

The OCM reference uses rational univariate polynomials and four total instructions:
increment, decrement, doubling and squaring. It mines recurring proper program
fragments from distinct verified training tasks. The fragments become generator
productions; a primitive enumerator remains available through an alternating
schedule. This is a small instance of learning a method that generates methods.
It does not implement unrestricted recursive self-improvement.

## M1: finite completeness and bounded convergence

For `p` primitive instructions and maximum length `L`, the candidate universe has
`N = sum(p**i for i=0..L)` words, including the empty program. All instructions
and the checker terminate on the registered domain. Exhaustively evaluating the
universe therefore decides existence **in this grammar and bound**.

Let a correct program have primitive enumeration rank `r`, starting at 1. An
alternating guided/primitive schedule reaches the first `r` primitive candidates
within `2r` slots. Rejecting duplicate guided words does not remove the primitive
slot. Thus any solution found by the primitive parent in `r` slots is found in
at most `2r` slots, provided that budget is available. This is a slot bound, not
a bound on arbitrary-precision arithmetic time or memory. A slot includes failed,
duplicate and over-length guided expansions; those costs cannot disappear.

Finite budget exhaustion says nothing about longer programs. If the grammar is
extended to every finite length and each candidate checker is total, fairness
gives eventual discovery of an existing finite solution. It gives neither a
uniform finite bound nor a terminating procedure for every unsatisfiable problem.
The executable OCM reference deliberately bounds length at 8 and slots at 200,000.

## M2: examples, counterexamples and mathematical solutions

Numeric evaluation and symbolic coefficient propagation are separate
implementations. Each primitive preserves polynomial semantics by the ordinary
addition, scaling and convolution identities. Structural induction on program
length proves that coefficient propagation represents the program on every
rational input. Equality of canonical coefficient tuples is therefore sufficient
for the requested polynomial identity, beyond the finitely sampled examples.

If a candidate fits the examples but has unequal coefficients, the difference
is a nonzero degree-`d` polynomial. It cannot vanish at all of `0,...,d`, so a
counterexample exists among those `d+1` points. The example set can eliminate the
candidate without turning example agreement into a proof.

The proof obligation is confined to this total arithmetic language. Arbitrary
Python callbacks, general theorem proving and Lean kernel integration do not
inherit it. Host code is never synthesized or executed by this reference.

## M3: method learning and evidence lifecycle

Fragment support counts distinct specification hashes, not task labels or copied
traces. Only independently rechecked training solutions contribute. Holdout
specification hashes must be nonempty, distinct and disjoint from training.
One fixed proposal is tested; this holdout must not be reused for adaptive tuning
and then described as an independent test.

Acceptance means all declared holdout tasks are solved, every measured slot count
is no worse than the primitive parent, and at least one is better. It proves a
finite measured statement only. Two selected examples cannot support a population
speedup, architecture superiority or novelty claim.

The runtime stores generator data and support links, rather than executable host
objects. Its warrant is the conjunction of training proof support and holdout
comparison support. If an essential support is revoked, the generator cannot be
loaded after restart. The old program, outcomes and history remain addressable.
Reinstatement and newly acquired evidence remain distinct operations.

## M4: convergence of experimental identification

Freeze a finite deterministic model class `H`, a finite query family `Q`, and a
complete prediction `h(q)` for each pair. Assume the true model belongs to `H`,
observations are accurate, and every surviving distinct pair is separated by a
query. Choose a query minimizing the largest resulting outcome partition.

The true model remains in the version space. Every non-singleton version space
has a separating query, whose observed partition removes at least one model.
Consequently identification terminates within `|H|-1` observations. No balance
assumption is needed. A logarithmic worst-case bound requires an additional
balanced-splitting assumption and is not implied by minimax selection alone.

Identical prediction rows remain observationally equivalent. An empty version
space means the class or the observations must be revised. Revocation removes
constraints and can expand the version space, reopening experiment selection.
Model-class identity is immutable; expanding the class creates a new contract.
No claim here covers noise, missing models, uncontrolled confounding, measurement
error, nonstationarity, or empirical truth outside the registered experiments.

## M5: honest statistical comparison

For IID paired Bernoulli outcomes define category probabilities `p10` and `p01`.
The population success difference is `p10-p01`. Bound each probability with a
Clopper–Pearson interval having confidence `1-alpha`. Bonferroni gives joint
coverage at least `1-2*alpha`; interval subtraction then bounds the difference.
Each one-sided difference-bound error has probability at most `alpha` because
only two marginal tails, each of probability at most `alpha/2`, can invalidate it.
This supports conservative equivalence testing and directional margin tests.

The observed discordance proportion must not be treated as the population value.
In particular, one agreeing pair does not yield a zero-width population interval.
Mismatched pairs, missing observations and truthy `CANNOT_CHECK` strings are
invalid inputs. For fixed authored suites, even correct statistical code does
not establish IID population sampling; report descriptive results.

## Parent reconstruction and external requirements

The strongest parent product is counterexample-guided inductive synthesis,
program-fragment abstraction, fair enumeration, generalized binary search,
exact polynomial normalization and dependency-based truth maintenance.
The reference demonstrates their composition; no residual is claimed.

Primary references:

- [Solar-Lezama, verified synthesis and CEGIS](https://people.csail.mit.edu/asolar/SynthesisCourse/Lecture17.htm).
- [NIST exact binomial confidence intervals](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/propconf.htm).
- [NIST simultaneous Bonferroni intervals](https://www.itl.nist.gov/div898/handbook/prc/section4/prc463.htm).

Next empirical gate: a preregistered task distribution and stronger matched
synthesis parents, fresh tasks unavailable during generator construction,
training/search/checking/storage costs, independent evaluator custody, and
real external observations for science. This packet does not satisfy those gates.
