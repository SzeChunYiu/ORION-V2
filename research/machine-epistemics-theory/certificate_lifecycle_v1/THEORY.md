# Certificate lifecycle: identity, applicability and grounded reuse

**Study #318; baseline `24566f00a9dc4425a438fcfac05d13c6b2d903db`.**
Status: scoped written theory and exact reference calibration; independent proof review,
proof-assistant checking and OCM adoption remain open. This is not a replacement for
#312/#313's typed foundation, #314's decision frontier or #315's causal transport.
No protected empirical study is run. The definitions below are proposed contracts,
not an announcement that all Machine Epistemics foundations are complete.

## 1. Semantic boundary and identity theorem (CL1)

Let X be a space of fully interpreted configurations, k:X -> I an identity projection,
and P:X -> {0,1} a particular property. A fingerprint is **P-sufficient** when there
exists g:I -> {0,1} with P=g composed with k.

**Theorem CL1.** Such g exists exactly when P is constant on every nonempty fiber
k^-1(i). Consequently k suffices for *every* Boolean property exactly when k is
injective.

**Proof.** Factorization immediately makes equal identities have equal P values.
Conversely define g(i) to the common value on each nonempty fiber, with arbitrary
values elsewhere. For the universal statement, if x != y share an identity, the
indicator of {x} separates them, contradicting sufficiency. Injectivity gives
singleton fibers. No finiteness assumption is needed for this argument. The
reference exhausts 16 projections and 16 properties on four worlds (256 pairs),
which is calibration of the theorem, not its all-size proof.

**Omission counterexample.** Two operators share an advertised name/version/types,
but one prompt makes the output 0 and the other makes it 1. The property “returns 0”
is not constant on the resulting identity fiber. A certificate for one cannot be
reused for both merely because the advertised identity matches. This is a logical
countermodel, not a claim that a particular live OCM branch still has that defect.

The conservative operator manifest binds 16 coordinates: implementation, model,
weights, prompt, decoding, preprocessing, postprocessing, checker, calibration data,
calibration protocol (including selection, seed and split), assumptions, environment,
resource policy, scope, epoch and schema. Each value is a content digest; inapplicable
coordinates require an explicit content-bound declaration, not an omitted field.
This set is a **declared closed-dependency model**, not a theorem that all real
systems have exactly these dependencies. An opaque provider whose serving version
cannot be observed has an unresolved identity obligation. A digest of “unknown” does
not make that obligation known.

The mathematical identity is the complete typed serialization. SHA-256 is a compact
engineering binding conditional on collision resistance, not a proof of injectivity
on all possible strings. Canonical JSON here rejects floats and non-string map keys,
separates domain/type tags, and preserves exact strings. Arrays represented as Python
lists or tuples share a serialization. This is not a natural-language semantic
equivalence checker. A raw JSON parser must separately reject duplicate keys before
constructing a dictionary; the reference API starts with already parsed objects.

## 2. Certificates are not merely fingerprints (CL2)

A certificate contains a name, kind, statement digest, subject digest, proof/evidence
digest, checker digest, required context bindings, and alternative support clauses.
Kinds in this bounded fragment are `EXACT_OBJECT` and `OPERATOR_GUARANTEE`.

The statement digest must resolve to a typed declaration: quantified proposition,
semantic theory, domain, assumptions, scope and relevant resource/access model.
It must not be a hash of an uninterpreted slogan. Root assumptions are addressed by
digests of their immutable typed declarations. Symbolic certificate names are
interpreted by a frozen whole-registry digest. Changing a dependency declaration,
even under the same name, changes that registry and every associated check target.

Two distinct external facts are mandatory for each certificate:

* a checker judgment bound to the **entire frozen registry and certificate body**;
* a trust premise about that checker, bound to its kind and statement scope.

These facts are inputs at an explicit trusted boundary. `IMPORT_EXTERNAL` does not
implement signatures, source authentication or permission checking. It is an abstract
operation available to the environment, not an operator permission. A production
adapter exposing that operation to untrusted model output would violate the model.
The reference is therefore not a standalone secure evidence service.

For each root the environment supplies VALID, INVALID, UNKNOWN or CONFLICT. Missing
roots are UNKNOWN. A conflict is represented, not automatically discovered: a report
adapter must establish report identity and disagreements before importing CONFLICT.
The reference contains no majority vote or count-based authority rule. It does not
claim to solve arbitrary conflicting-verifier adjudication.

Certificate applicability uses three values:

| Value | Meaning | Not a consequence |
|---|---|---|
| 2 APPLICABLE | this typed certificate can be used under the current declared premises | unqualified truth, external action permission |
| 1 UNRESOLVED | missing, stale, unknown, conflicting or ungrounded prerequisite | falsehood of the proposition |
| 0 UNUSABLE | a necessary certificate route has an invalid prerequisite | proof of the negated proposition |

Operator guarantees require exact operator, scope and epoch bindings. Any mismatch
makes the binding gate UNRESOLVED and blocks applicability; another invalid
prerequisite can make the overall result UNUSABLE. Reuse requires revalidation
or a separately checked transport result.
Even a *subset* of a population is not automatically authorized by a marginal
coverage result. A 20-case population with 19 correct results has 95% marginal
accuracy and a one-case failing subgroup has 0%. Neither pointwise correctness nor
subgroup coverage follows. This elementary countermodel is not a conformal procedure
or a statistical experiment. #312/#313 own the full truth/risk separation; #315 owns
its causal/distributional transport extensions.

**CL2 type-preservation proposition.** A successful `USE` preserves exactly the
certificate's kind, statement and subject. A request for an exact individual claim
cannot succeed solely by relabeling an operator guarantee. This follows directly
from the equality guard, before applicability checking. The planted coercion mutant
removes that guard and is detected. The guard cannot establish that a trusted
checker interpreted the statement correctly; that remains an explicit soundness
premise, not a benefit granted by field names.

## 3. Grounded dependency semantics (CL3)

Fix a finite registry of n certificates. Each support alternative is a conjunction
of roots/certificates; alternatives are disjoined. Empty conjunction is permitted
for an unconditional checked proof. An empty family means NO_DERIVATION and is
UNRESOLVED, not closed-world negation of the claim.

Use the truth ordering 0 < 1 < 2 for min/max evaluation. Map INVALID to 0, UNKNOWN
and CONFLICT to 1, VALID to 2. Each certificate's own gate is the minimum of its
judgment, checker-trust and context-binding gates. Its update is own gate AND the
OR of its support alternatives. Start all certificate values at 1 and iterate.

**Theorem CL3a.** This iteration stabilizes after at most n strict-changing rounds
and one equality check, yielding the least fixed point in the *information* order
1 <=_i 0 and 1 <=_i 2. No unrooted cycle creates APPLICABLE.

**Proof.** Strong-Kleene min/max are monotone in that information order (inspect the
three-value tables). The initial vector is its least element. Each strict change
refines at least one coordinate from 1 to either 0 or 2; monotonicity forbids later
switching 0 to 2 or 2 to 0. There are n coordinates. Leastness follows by induction
that each iterate is below any fixed point. A pure cycle with otherwise valid own
gates remains at 1. A cycle with a grounded alternative may become 2.

**Theorem CL3b (grounded-use soundness).** Assume every VALID root judgment is sound
for its immutable declaration, all required context bindings correctly describe the
use context, and a VALID checker judgment certifies a sound inference from the named
support alternatives. Every APPLICABLE certificate has a finite grounded proof tree
and its **typed conclusion under those premises** is sound.

**Proof.** Take the round in which a node first becomes 2. Its own gates are 2 and
one support clause has only VALID roots and certificate nodes already 2 in the
previous round. Recursively use their earlier-round trees. The round index strictly
decreases along recursive branches, so this construction terminates. Apply the
sound inference judgment at each node. The converse also holds for a finite tree
whose own gates and leaves are all valid: induction on tree height puts its root
at 2 after finitely many rounds.

This is conditional proof-carrying reuse, not a proof that a checker is sound because
it ran successfully. The external trust base cannot be eliminated by a circle of
checkers certifying one another. An incorrect external VALID judgment is outside
the theorem's assumptions and can make the system wrong. Code does not hide that
failure behind the word “certificate.”

No numerical independence is inferred. Shared root identifiers refer to one
assumption. Repeated testimony cannot increase a probability or authority score
because this calculus has no such aggregation operation. Dependence discovery,
collusion detection and graded risk composition remain separate problems.

## 4. Dependency locality and alternate support (CL4)

For a fixed registry, construct edges from every root/certificate to each dependent
certificate, including mandatory judgment/trust roots. A changed contextual binding
seeds the certificates that require it. Let I be these direct changes and their
forward transitive dependency cone.

**Theorem CL4.** Changing only the specified root values and context bindings leaves
every certificate outside I unchanged. Membership in I is a *reevaluation obligation*,
not proof that the certificate must lose applicability.

**Proof.** The equations for nodes outside I have unchanged own gates and no incoming
dependency from I. Their least-information fixed point is thus the same before and
after the change. For non-necessity of retraction, a node supported by either e1 or e2
remains applicable when e1 is invalidated and e2 is still valid. A node requiring
both loses that route. Both examples are exercised by AND/OR substitution mutants.

The reference recomputes the whole fixed point; it does **not** implement an optimized
incremental algorithm or prove a minimal repair set. Registry edits are outside this
locality theorem: they change the bound interpretation and require new judgments.

## 5. Lifecycle, history and the check/use race (CL5)

A snapshot contains registry digest, immutable contextual bindings and root facts,
a nonnegative generation, and a journal binding. An event carries the expected full
snapshot identity and generation. IMPORT_EXTERNAL changes environment facts/context;
USE checks certificate identity, kind, statement, subject and current applicability.
Every successful transition increments the generation, including uses and no-op
imports, and hashes the preceding snapshot and the full event. Rejected transitions
return no new snapshot and cannot mutate the frozen input.

**Theorem CL5a (snapshot-use invariant).** In any finite sequence of these abstract
serialized transitions, every successful USE receipt refers to an applicable typed
certificate at its exact preceding snapshot. A request prepared before any intervening
transition cannot succeed afterward, even when all visible facts are restored.

**Proof.** The base state is explicit. At each step the snapshot/generation guard is
checked and USE recomputes applicability before constructing a receipt. Generation
strictly increases at every accepted step, so a previous expected generation cannot
match after a revoke-and-restore ABA cycle. Snapshot hashing additionally prevents
substitution of a different registry, state or history at the same generation.
Induct on the length of the transition sequence.

**Theorem CL5b (deterministic replay).** The same initial snapshot and event sequence
produce the same snapshots and receipts, or fail at the same first invalid event.
A replay must match an independently supplied final checkpoint; a proper prefix,
reordering or altered event does not certify that final state.

**Proof.** Every transition is a deterministic function over canonical finite values.
Induction yields equality of intermediate states and receipts. The generation and
snapshot guards reject incompatible sequencing; the final checkpoint binds completion.
Different valid uses with otherwise equal state changes still have different event
bindings, conditional on collision resistance.

A hash chain cannot authenticate itself. A party that can replace both the whole
history and its purported checkpoint can create a different consistent history.
The checkpoint is an external input. Historical receipts describe the past and do
not assert current liveness after later revocation.

**Limits:** serialized transitions are the specification, not a demonstrated threaded,
crash-safe, database or distributed implementation. No filesystem crash model,
write-ahead-log proof, exactly-once effect, consensus, wall-clock expiry source or
sandbox is provided. A revoke between local USE and a real external effect remains
a separate executor-fencing obligation. USE is not ActionIntent authorization or
an ActionReceipt and cannot authorize a real-world action.

## 6. Artifact-specific independence (CL6)

**Theorem CL6.** For a certificate about an immutable object, changing only a producer
configuration absent from its complete dependency closure preserves applicability.

**Proof.** This is CL4 with no path from the changed producer coordinate to the
certificate. The exact checked subject, statement, proof, checker and trust premises
remain fixed. The test changes a producer binding while an immutable-object proof
remains applicable; an operator guarantee pinned to that binding becomes unresolved.

This distinguishes accidental provenance from logical dependence. A generated proof
can be independently checked without trusting the generator. Conversely, a claim
about how the producer was run, or a statistical guarantee about its outputs, may
depend essentially on that producer. Omitting an essential dependency violates the
complete-dependency premise; calling a certificate EXACT_OBJECT does not repair it.
If the original checker becomes untrusted, the prior route is revalidated; a new
trusted check can establish a new route without rewriting the old receipt.

## 7. Absorption boundary (CL7)

The bounded absorption record pins source/target commit identities, statement,
artifact manifest, permitted scoped study terminal, parity receipt, independent
review receipt and scope. The source repository is ORION-V2 and the target repository
is ORION-OCM by this contract, not caller-selectable aliases. The artifact manifest
must resolve to exact paths/bytes/dependency identities; fake digests in unit fixtures
are never treated as actual source verification.

Four external facts bind the *entire record*: source verification, independent review
verification, parity verification and adoption authorization. Missing/conflicting
facts are UNRESOLVED. The validator additionally compares source and target commits
with the externally observed expected commits and rejects unresolved study terminals.

**Proposition CL7.** A record alone, or the author's local green tests alone, cannot
pass this model's absorption gate. Changing any bound record field cannot reuse its
old approval facts, conditional on digest collision resistance.

**Proof.** All four record-bound roots are conjunctively required. They are not
created by validation. A changed record has a different root namespace; prior facts
do not satisfy the new requirements. This is an interface condition, not a
cryptographic implementation of those external checks. No approved absorption
record is shipped here.

## 8. Resource and parent accounting

For registry serialization size B, n certificates and m declared support/binding
occurrences, this intentionally simple evaluator recomputes registry hashes for each
judgment and iterates at most n+1 times: O(nB + n(m+n)) work, besides input validation
and arbitrary-precision integer/hash costs. State/event storage and proof/checker
execution are separate costs, not free. The reference does not execute the substantive
checker, discover dependencies, prove assumptions or establish semantic equivalence.
The Boolean completion oracle is exponential by design and is used only for tiny
calibration. No scale/performance advantage is claimed.

Primary-source parent reconstruction (source access 2026-09-04):

| Parent | Reconstructed ownership and boundary |
|---|---|
| W3C PROV-DM (2013), generation/use/derivation/invalidation | Typed provenance records support lifecycle accounting; provenance alone does not prove the recorded claim. https://www.w3.org/TR/prov-dm/ |
| SLSA provenance v1, resolved to specification v1.1 | Subjects, build definition, parameters and resolved dependencies bind build evidence. Reused as an identity discipline, not a scientific truth test. https://slsa.dev/spec/v1.1/provenance |
| Appel, Foundational Proof-Carrying Code (LICS 2001), sections 1–2 | A checked proof still has a trusted logic/checker/semantics base; generator trust can be removed when the actual artifact is checked. This owns the essential CL3/CL6 assurance idea. https://www.cs.princeton.edu/~appel/papers/fpcc.pdf |
| de Kleer, A Perspective on Assumption-based Truth Maintenance (1993), pp.63–67 | Alternative assumption environments and nogoods motivate preserving independent routes. This owns the dependency/alternative-support mechanism, not hidden-source independence discovery. https://www.dekleer.org/Publications/A%20Perspective%20on%20Assumption-based%20truth%20maintenance.pdf |
| Herlihy and Wing, Linearizability (1990), sequential specification and locality | An implementation must refine the abstract sequential object; declaring atomic operations does not prove an implementation linearizable. Our serialized model is only the specification side. https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf |

The factorization and fixed-point arguments are elementary scoped results, not claimed
as new. The strongest parent product—typed provenance + proof-carrying checking +
truth maintenance + version-checked state transitions—accounts for this package's
mechanisms. Full novelty saturation is not performed. The appropriate disposition is
**SCOPED_THEORY_PARENT_OWNED**, subject to independent assumption/proof review; no
architecture separation, field recognition or OCM milestone follows.
