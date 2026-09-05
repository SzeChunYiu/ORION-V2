# Infinite integer-threshold lifecycle identification

**Terminal: `INFINITE_THRESHOLD_CLASS_PROVED__PARENT_SUFFICIENT__REFERENCE_ONLY`.**

This successor establishes a natural, countably infinite learnable class with
exact revocation, useful-retention and query-repair mechanics. It does not close
the SHRG/CCG construction-inventory problem in MEG-34/F7. Earlier finite results
and their pinned receipts are unchanged. The proofs below concern all integer
parameters; finite executions calibrate the reference implementation only.

## Registered model and architectural use

The class is `H = {h_theta : theta in Z}`, where `h_theta(x) = 1[x >= theta]`
for every integer `x`. There is no global bound on either integer. Such a
procedure is a learned monotone guard on an integer feature; thresholding a
count or a measured ordinal feature is its direct application. This is a
restricted procedure class, not a grammar-induction result.

An observation is `(record_id, revocation_unit, x, label, context)`. Context
binds authority, scope, verifier and epoch. The host authenticates records and
assigns revocation units: deleting one unit deletes all its observations.
Distinct units are independently *revocable*, not statistically independent.
Copying a record under a fresh name does not create new revocation authority.
The reference rejects reused record identities and mismatched contexts; it
cannot authenticate a caller's claimed authority.

`E` is the complete declared ledger for this snapshot, with no claim that all
possible external evidence has been discovered. A permitted intervention
deletes any finite set of its revocation units. The target is fixed and the
oracle is realizable and noiseless. An optional repair query returns the exact
membership label plus host-assigned metadata. The only target-dependent
information is that binary label: identities, timing, source selection and
other metadata cannot encode additional target information. Lower bounds give
every comparator the same surviving prior interval, oracle and evidence.

The operational objective is to answer every currently forced per-input label,
abstain on every unforced label, retain all still-supported answers after
revocation, and, when requested, identify the whole function with additional
queries. Full identification is separate from useful partial retention.

`PROTOCOL_V1.json` was written after selecting this hypothesis and before the
first local checker run. `PROTOCOL_V2.json` preserves it and explicitly records
the information-channel and bit-budget clarifications after initial local
calibration, before successor validation. Neither is external preregistration.

## T1: exact surviving version space and complete witnesses

For surviving records define

\[
L=1+\max\{x_i:y_i=0\},\qquad U=\min\{x_i:y_i=1\},
\]

where absent negative and positive sets give `L=-infinity` and `U=+infinity`.
Then the exact version space is the integer interval `[L,U]`. If `L>U`, the
ledger is contradictory and yields no authorized answer; vacuous universal
truth is deliberately refused.

**Proof.** Every negative observation says `theta>x_i`, equivalently
`theta>=x_i+1`; every positive observation says `theta<=x_i`. Their conjunction
is exactly the displayed interval. Every integer in it satisfies every record.

For a consistent ledger, the query `x` is forced positive iff `U<=x`, forced
negative iff `x<L`, and otherwise both labels remain possible. Its complete
family of minimal revocation-unit witnesses is:

- positive: each singleton unit containing a surviving positive record at
  some `x_i<=x`;
- negative: each singleton unit containing a surviving negative record at
  some `x_i>=x`.

**Completeness proof.** A set of units forcing positivity must have a minimum
positive coordinate at most `x`, so one of those units alone already forces
the same label. Negativity follows from its maximum negative coordinate.
No empty unit set forces a label, because the prior class includes every
integer threshold. Therefore these are exactly the minimal witnesses.

This proves useful retention: deleting a witness unit preserves an answer iff
at least one of its remaining singleton witnesses survives. Deleting everything
cannot masquerade as success, because it loses every previously forced answer.

## T2: exact identification needs adjacent boundary evidence

The whole target `theta` is exactly identified iff the surviving ledger contains
both a negative observation at `theta-1` and a positive observation at `theta`.

**Proof.** Exact identification is equivalent to `L=U=theta` in T1. A finite
nonempty set of integer observations attains both extrema; hence the two
adjacent observations are necessary. Their two inequalities are sufficient.
Other observations may remain essential for useful retention after these
boundary observations are revoked. Keeping only the current two extrema is
therefore insufficient for the full lifecycle objective.

For example, negatives at `-1` and `0`, and a positive at `2`, give the same
current interval as the compressed ledger containing only the latter two
records. Revoke the observation at `0`: the full ledger still justifies a
negative answer at `-1`, while the compressed ledger cannot. The strongest
parent is permitted to retain the full provenance ledger, eliminating this
artificial representation disadvantage.

## T3: optimal finite-interval exact repair

If the surviving interval has `N=U-L+1` integer thresholds, the optimal
deterministic worst-case number of binary membership queries is

\[
Q^*(N)=\lceil\log_2 N\rceil.
\]

**Lower bound.** A decision tree of worst-case depth `q` has at most `2^q`
binary-answer leaves. Each leaf identifying the whole function may contain
only one threshold: distinct thresholds disagree somewhere on the integer
domain. Thus `2^q>=N`. Arbitrary target-encoding metadata would violate the
registered binary interface and invalidate this bound.

**Upper bound.** Query `x=floor((L+U)/2)`. Label one leaves `[L,x]`; label zero
leaves `[x+1,U]`. The largest remaining size is `ceil(N/2)`. Repeating gives a
singleton in at most `ceil(log2 N)` queries. Each added observation is kept
with its own revocation identity. The lower and upper bounds coincide.

The bound is for the surviving prior, without a free retained copy of the
revoked target. A system retaining old answer bits may guess a threshold sooner,
but those bits are not current warrant under this agreement-region objective.

## T4: unbounded repair has no uniform finite bound, but is pointwise learnable

If one interval endpoint is infinite, no fixed finite query budget guarantees
exact identification for every consistent threshold. The decision-tree proof
still applies: infinitely many distinct functions cannot fit into `2^q` leaves.
This is not a claim that an individual finite integer target is unlearnable.

The reference learner first queries `0` when neither bound exists. With only
a finite lower bound `L`, it queries `max(L,2*abs(L)+1)` until a positive label
supplies an upper bound. With only a finite upper bound `U`, it queries
`min(U-1,-2*abs(U)-1)` until a negative label supplies a lower bound. Each
one-sided sequence tends to its missing infinite endpoint, so for every fixed
integer target it terminates after finitely many queries. T3 then identifies
the target.

For the empty initial ledger let `b=bit_length(abs(theta)+1)`. The positive
bracketing probes after `0` are `3,9,21,...,3*2^k-3`; the negative probes are
`-1,-3,-7,...,-(2^k-1)`. A crossing occurs by `k<=b`. The resulting finite
interval has size below `3*2^b`; bisection takes at most `b+2` additional
queries. Thus the conservative total bound `2*b+4` holds. Query-coordinate
length is `O(b)`. This is an all-integer argument, not extrapolation from a
finite test interval.

The implementation enforces a query-count budget and a signed coordinate
bit-length budget; exhaustion returns `CANNOT_CHECK` with accepted evidence
and actual query count preserved. Temporary endpoint/doubling arithmetic can
use a constant number of extra bits. Oracle failures and malformed replies
count as attempted queries, and cannot create an identified target.

## T5: sharp robustness against r revocation units

Suppose the current ledger identifies `theta`. Let `A` be the set of live
revocation units containing a negative record at `theta-1`, and `B` the units
containing a positive record at `theta`. Exact identification survives **every**
deletion of at most `r` revocation units iff

\[
|A|\ge r+1\quad\hbox{and}\quad |B|\ge r+1.
\]

**Necessity.** If `|A|<=r`, delete all of `A`. No remaining negative record is
at `theta-1`; consequently both `theta-1` and `theta` satisfy all surviving
evidence. The symmetric argument deletes `B`, leaving `theta` and `theta+1`.
The empty corresponding side is covered by the same argument.

**Sufficiency.** Deleting at most `r` units leaves at least one member of both
`A` and `B`; T2 identifies exactly the original threshold.

If each record answers one membership query, the minimum robust boundary
certificate contains `2*(r+1)` records. It needs only `r+1` distinct units in
total when every unit authenticates both boundaries. If repeated records share
one common upstream revocation unit, they count only once on each side. This
is a deterministic availability theorem, not a probabilistic independence
claim and not a promise that fresh independent authorities are available.

## Strongest-parent reduction and resource accounting

Query learning already supplies the binary observation model and decision-tree
lower-bound method. [Angluin, *Queries and Concept Learning* (1988)](https://link.springer.com/article/10.1023/A%3A1022821128753)
studies query interfaces and exact-learning upper/lower bounds. Active threshold
learning already uses binary search; a current primary example is
[Bressan et al., *Margin-Based Active Learning of Multiclass Classifiers* (2024), p.24](https://jmlr.org/papers/volume25/22-1127/22-1127.pdf).
These sources support the parent mapping; the lifecycle statements above have
self-contained proofs and make no literature-priority claim.

The equal-interface parent maintains an ordered multiset of signed observations,
an index from revocation unit to its records, and a list of all surviving
witness units. It applies exactly the same interval, witness and query rules.
There is a direct state correspondence preserving every future deletion and
query response. Therefore the parent product is sufficient: this package
establishes no architecture separation, new learning paradigm, parameter
advantage or superiority to an equally provisioned recurrent implementation.

For `n` stored records, this transparent reference scans the ledger: each
interval or prediction computation costs `O(n)` integer/identity operations
plus emitted witnesses. With `q` repair queries it performs
`O(q*(n+q))` such operations and retains all `n+q` records. Integers and
identities are not free: stored size is the sum of their encoded lengths;
integer comparisons/additions scale with coordinate bit length. An indexed
parent may improve update costs; no indexed performance claim is measured here.
External certificate verification and acquisition costs are not measured.

## Falsifiers and remaining boundary

The checker must reject inconsistent labels, reused record IDs, context
changes without fresh bindings, unknown revocation units, attempted source
resurrection, wrong-query replies, mutable/incomplete input containers, Boolean
integer substitutes and exhausted budgets. It checks lower/upper equality on
all small finite intervals and evaluates the complete deletion quantifier in
small redundant ledgers, including shared source units and compressed-state
retention counterexamples. Large integers are representation controls only.

Still open: learning construction inventories for a frozen infinite SHRG/CCG
class, noisy evidence, correlated authority failure beyond the registered unit
model, unregistered external support discovery, unrestricted language,
computational advantage, novelty, external review and scientific admission.
