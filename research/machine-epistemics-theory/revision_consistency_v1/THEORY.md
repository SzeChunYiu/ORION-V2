# Revision consistency: eight scoped foundation results

Identity: ME-REVISION-CONSISTENCY-V1. Registered design commit
`59b6819574f494354b880605998ffddbc5687077`, based on V2 `24566f00a9dc4425a438fcfac05d13c6b2d903db`.
Written proofs below are author arguments, not proof-assistant certificates or independent
review. `RESULT.json` supplies separate finite implementation calibrations. Sources P1–P6
are reconstructed in `SOURCES.md`. Parent sufficiency is the current disposition.

## 0. Object and assumption boundary

Fix a finite, explicit specification q = (subject, payload, equalities, absence predicate).
A state S maps keys to (value, version) and registered namespaces to generation counters.
Values may be explicitly unknown. A trusted mutation increments the affected key's version
and every applicable namespace generation, including insertion; counters never wrap or
reset. Deletion is not implemented here. A production deletion must retain a versioned
tombstone and increment the same guards; otherwise these results do not apply.

The complete read footprint D(q,S) contains every fact on which the registered judgment
and permission depend, including negative/predicate reads. A sound trusted checker record
binds q, the historical state, the checker identity represented in q, and its verdict.
This model assumes the specification is complete and the checker is sound. Neither is
proved by hashing. Nor does a caller know a distributed cut is current merely by saying so.

The modeled judgment J(q,S) is a finite contractual precondition, NOT unqualified truth.
Its positive case requires all equalities, the registered absence condition and *prior*
commit authority. A known violation is FAIL; missing required information is CANNOT_CHECK.
Historical FAIL is not erased by later changes: a new checker record is required.
REOPEN_REQUIRED means a formerly usable certificate's context changed, not that its
underlying proposition has been disproved. These four outcomes are not a truth lattice.

Assumptions are deliberately exposed: trusted transitions and monotone versions;
complete footprints; sound, correctly bound checker records; externally obtained prior
permission; actual current-cut evidence; and one atomic validation/commit boundary.
Dropping any of the last four is not repaired by adding a hash or a receipt.

## R1. Context descriptor sufficiency

For any context domain X, judgment J:X→Y and descriptor h:X→H, there exists a function
f:h(X)→Y with J=f∘h **iff** J is constant on each fibre of h.

Proof. Necessity follows by applying f to equal descriptors. For sufficiency, define
f(z)=J(x) for any x with h(x)=z; fibre constancy makes this well-defined. No finite-size
restriction is needed. This is ordinary factorization through an equivalence relation,
not a new information-theoretic separation.

Counterexample: two operators share id/version/input/output metadata, but use different
checker semantics. Let J be true for only one. A descriptor omitting that difference maps
both to one value; transporting a certificate by descriptor equality fails. Binding every
coordinate is sufficient only relative to the registered influential coordinates, not an
assurance that all influences have been discovered. Cryptographic equality additionally
assumes no relevant digest collision.

Calibration: 256 four-context binary-descriptor/judgment pairs; pairwise and fibre-group
implementations agree. The deliberate omitted-coordinate witness fails; a distinguishing
descriptor passes. No universal finite fingerprint or minimal descriptor is claimed.

## R2. Complete-footprint preservation under revision

Let S' be reachable from S by trusted mutations. Suppose a sound checker returned PASS
for (q,S), and D(q,S')=D(q,S), including namespace generations. Then J(q,S')=PASS.

Proof. Every positive required cell has its old value and version. An unchanged namespace
generation implies no mutation occurred in that namespace along this path, so its absence
condition remains satisfied. Prior permission is an ordinary required cell in the same
footprint. These are all clauses in J; their conjunction is unchanged. Induction extends
the argument to every finite mutation sequence.

A new `conflict/new=BLOCK` record leaves the old positive cells identical while falsifying
the absence condition. Thus readsets containing only existing positive supports are
insufficient. This is the phantom/predicate problem in an epistemic-state interface [P1].

Unrelated changes preserve usability. An ABA change LIVE→REVOKED→LIVE advances versions
and conservatively reopens even when J is again true. Rechecking issues new lineage and
allows use again. Therefore this rule is sound, not a claim of minimal necessary reopening.
Missing records, unknown guards or incomplete footprints do not satisfy the premise.

Resource scope: with an already available indexed snapshot and trustworthy guard, d logical
reads cost O(d). The provided Python reference builds maps, hashes whole snapshots, sorts
and serializes; it uses at least O(N) data movement, potentially O(N log N) ordering work,
and O(N) extra storage. Certificates use O(d) fields. No wall-clock, concurrency-throughput
or constant-time hashing claim is made.

## R3. Immutability does not imply serializability

Original target is precisely the MEG-30 serializability subclaim in the unchanged atlas at
base `24566f00...`. This correction neither deletes that original nor adjudicates the other
MEG-30 termination propositions owned by the parallel foundation work.

Take initial booleans x=y=true and invariant x∨y. T0 reads x,y and sets x=false only if
y=true; T1 symmetrically sets y=false only if x=true. Both use immutable initial snapshots
and write different cells. They can both commit, leaving false,false. No serial execution
of these conditional transactions permits that state: the second transaction observes the
other already false and declines. Hence snapshot immutability is insufficient [P1].

There are six interleavings preserving each read-before-write order. Four violate the
invariant under write-conflict-only validation; zero do under full readset validation.
The two serial schedules are non-alarm controls. This is a finite counterexample refuting
the original unrestricted implication, not a performance comparison.

## R4. Current validation-to-commit preservation

Assume R2's model, a sound externally trusted record, a correctly discharged current-cut
premise and an indivisible operation that validates then records the commitment at time τ.
If it returns PASS, J(q,Sτ) holds, including prior permission.

Proof. Certificate and checker identities are validated against the historical object;
unknown/failure records cannot pass. Equal complete footprints transfer the historical
precondition by R2. Atomicity excludes a relevant change between validation and commitment.
Thus the precondition holds at the operation's linearization point. Later revocation may
invalidate future use without making the historical record a lie [P2,P3].

Dropping atomicity permits CHECK(LIVE), REVOKE, COMMIT using a cached positive bit. Checking
each cell atomically is not enough: the multi-cell validation and commitment must form the
required operation. This model emits no physical effects and does not implement a database
transaction, lock, consensus protocol, authentication service or current-cut oracle.
`current_cut_known` represents a discharged premise in the mathematical input. OCM may NOT
implement that premise as a freely settable Boolean. The production refinement stays open.

Calibration compares separate candidate and straightforward readset-parent implementations
on 2,916 state/freshness/budget combinations. It includes **one accepted case** in that
exhaustive matrix, with zero false applicability there; the other cases exercise FAIL,
CANNOT_CHECK and REOPEN_REQUIRED. Additional unit controls exercise unrelated changes and
successful revalidation. No architecture residual: PARENT_SUFFICIENT in this model.

## R5. Asynchronous freshness versus non-abstaining availability

Assume a replica has seen a valid certificate. Remote revocation may complete before its
next request, but messages may be delayed beyond any finite response. Compare two histories
with identical local observations: H0 has no remote revocation; H1 has completed revocation
whose notification is delayed. A local policy has identical affirmative-response probability
p in both histories. Its false-current-affirmation probability in H1 is therefore p.

Consequently zero such error for every history forces p=0 on this view. Requiring positive
probability of a useful affirmative response on H0 is incompatible with that requirement.
This follows by indistinguishability, including randomized policies whose coins are coupled;
the five-value rational grid is illustrative only [P4].

CANNOT_CHECK is a legitimate terminating answer; it does not satisfy the *non-abstaining*
availability premise used here. Communication/coordination, a proved lease regime, weaker
consistency or a forward-invariant predicate can alter the contract. The theorem does not
forbid such designs. A proof verified once under an immutable theory is not automatically
subject to this revocable-current-permission model.

## R6. Anchored replay is historical, not a freshness certificate

Bind a log's genesis to its initial snapshot and schema. Each event binds its sequence,
payload and predecessor digest. Under canonical serialization and absence of relevant hash
collisions, an independently supplied (length, final digest) checkpoint selects one such
prefix; deterministic replay reproduces its state. Induction on the sequence proves replay
correctness; predecessor binding and the final anchor exclude substitution of a different
accepted prefix. Authenticity of the anchor is a separate assumption.

Any old prefix also verifies against its own old checkpoint. H0 ending at that prefix and
H1 extending it with an unseen revocation are indistinguishable to that verifier. Therefore
PASS means only *matches this historical checkpoint*. No supplied checkpoint yields
CANNOT_CHECK for anchored completeness, though internal replay can still be computed.
A file that contains both a log and its freshly recomputed hash is not its own authority.

Controls include truncation, reordering, payload mutation, rehashing against the fixed
anchor, and changing the initial snapshot. No append-only storage or cryptographic origin
authentication is implemented; these are explicit OCM obligations.

## R7. Causal closure versus application invariants

In a finite directed acyclic event graph, a subset C is downward closed exactly when it can
be an initial segment of some topological ordering. Necessity: every predecessor must
occur earlier. Sufficiency: topologically order C, then its complement; downward closure
excludes any edge from the complement into C, so concatenation is a legal ordering.

This is an event-poset statement, not proof that C occurred at one wall-clock instant. The
distributed-snapshot parent likewise distinguishes a consistent recorded state from the
literal sequence of states observed during execution [P5]. It does not turn every
application invariant into an inductive invariant.

For example, include r0,w0,r1,w1 from R3 with each read preceding its own write; the full
cut is causally closed yet x∨y is false after the allowed weak commits. Causal metadata and
application-level validation are separate obligations. The checker compares direct-parent
and transitive-ancestor closure on 1,098 cuts of 75 topologically indexed graphs, n≤4.
These are all graphs over the registered fixed vertex order, not all labelled DAGs.

## R8. Effect/receipt ambiguity after a crash

A durable local log contains an action intent but no result. In H0 the process crashed
before the external effect; in H1 it crashed after the effect but before observing or
persisting its acknowledgement. The same local log corresponds to both actual outcomes.
Any local deterministic classification DONE or NOT_DONE is wrong in one history; a
randomized classifier cannot make both error probabilities zero. Return CANNOT_CHECK
until an adequate external observation distinguishes the histories [P6].

An atomic effect/record service or an appropriate idempotent operation plus outcome lookup
can change the observation model. Merely attaching an idempotency label does not prove
either property. Nor can a later effect receipt supply permission that was absent before
the effect. Our reference invokes no external backend and makes no exactly-once claim.

## 9. What this closes and what it does not

Closed at written-argument plus finite-calibration strength: R1–R8 under their explicit
premises, and the R3 refutation of the cited atlas inference. All mechanisms are attributed
to established parents or elementary reductions. No blanket claim that every statement in
MEG-03/04/22/30 or the Machine Epistemics foundation is finished follows.

Still required before OCM absorption: a trustworthy checker/permission boundary; complete
positive and negative dependency discovery; authoritative freshness or a precisely weaker
contract; actual atomic commit refinement; predicate-guard correctness for every update;
effect reconciliation and crash testing; parity tests against this reference; independent
assumption audit. These are not provided by the research model's trusted arguments.

Frontier targets: characterize the weakest observation/lease contract making a specified
revocable predicate decidable; synthesize sound footprints including negative dependencies;
prove preservation across changing checker semantics using explicit transport certificates;
quantify useful progress versus stale-authority risk under bounded communication. Each
needs a successor design, strongest transactional/verification parent and real discriminating
cases, not an OCM-specific shortcut. Statistical actionability and decision-tree frontiers
remain with #312/#313/#314, respectively. Foundation overall: OPEN_RESEARCH.
