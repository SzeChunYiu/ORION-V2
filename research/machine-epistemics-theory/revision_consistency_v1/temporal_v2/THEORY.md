# Temporal validity under permitted revision: a scoped foundation successor

Status: written proofs + separately reported finite calibration. Parent disposition:
`PARENT_SUFFICIENT`. No novelty or full-foundation closure. V1 is unchanged.

## 1. Object, access model and quantifiers

Let S be a finite, nonempty, explicitly represented set of states; n = |S|. Let
P subset S be a fixed, exactly decidable predicate of registered admissibility.
A state may encode evidence status, checker/configuration identity, scope and
prior permission. Calling it admissible does NOT make a factual claim true.
The trusted interpretation from machine states to this model is an assumption.

A revision relation T subset S x S specifies ALL permitted one-step changes.
Transitions are possibilities, not inevitable next actions. A path may have
length zero; every finite path prefix is tested. A dead end is quiescent, not an
error. Thus persistence is a safety property, not termination, fairness, eventual
success or an optimal control policy. The machine does not choose T here.

For nonempty initial belief B subset S, define

    G(T,P,B) iff for every b in B and every finite T-path starting at b,
                 every state on that path belongs to P.

This is the safety fragment conventionally written AG P, with quiescent dead
ends. Completing dead ends with self-loops leaves this predicate unchanged.
All results below quantify over every finite n, not merely n <= 3.

## 2. TV-1: maximal persistent-validity kernel

Define F_T(X) = P intersect {s : every T-successor of s belongs to X}.
Then

    K(T,P) = greatest fixed point of F_T
           = S minus Pre_T^*(S minus P),
    G(T,P,B) iff B subset K(T,P).

Proof. Define Q as the states from which no bad state is reachable. Q subset P
because length-zero paths count. Every successor of a Q-state lies in Q,
otherwise concatenating the first edge with an adverse suffix reaches a bad
state. Conversely, if s belongs to P and every successor lies in Q, no adverse
path starts at s. Thus Q = F_T(Q). For any fixed point X of F_T, induction on
path length shows every path starting in X stays in X subset P. Consequently
X subset Q. This establishes maximality and both displayed equivalences.

An operational construction starts X_0=P and X_(i+1)=F_T(X_i). Monotonicity of
F_T and X_1 subset X_0 give a descending chain. Each strict iteration removes at
least one state, so at most n strict removals occur, followed by a fixed-point
check. The construction agrees with reverse reachability by the preceding proof.

Hostile: 0 -> 1 -> 2 with P={0,1}. At 0 the predicate and every immediate successor
are good, yet 0 is NOT in K. Current validity and one-step checking are insufficient.
No-alarm: 0 <-> 1 entirely inside P remains persistent even though it never terminates.
Parent: standard safety model checking/greatest fixed points; NOT an OCM invention.

## 3. TV-2: shortest counterexamples and finite certificates

For every s outside K there is a simple adverse path beginning at s of length at
most n-1. Among all adverse paths choose one of minimum length. Repeated states
would allow removing a cycle, contradicting minimality. A bad start has length 0.

Reverse breadth-first search from S minus P assigns each reachable predecessor
its minimum distance to a bad state. This follows by induction over BFS distance
layers: a newly discovered predecessor has a path one longer than the current
layer, while any shorter path would already have discovered it. A next-hop pointer
whose distance decreases by one therefore supplies a shortest adverse witness.

Checking a witness requires its model/scope identity, start, adjacency of each edge,
and a bad endpoint. The checker here additionally rejects cycles. It proves existence
of an adverse path, NOT that the path will occur or that no other path stays safe.
A two-edge fork 0 -> 0 and 0 -> bad refutes G while admitting an indefinitely safe run.

## 4. TV-3: exact decisions with incomplete transition knowledge

Suppose lower relation L and upper relation U satisfy L subset U. The admissible
completions are EXACTLY all T with L subset T subset U. S and P remain fixed.
Both extreme completions L and U must be allowed; no unstated constraint requires
an optional edge or couples optional choices. Then

    K(U,P) subset K(T,P) subset K(L,P).

Proof. Adding edges cannot destroy a previously existing adverse path. Apply TV-1.
For nonempty B, the following classifier is SOUND AND COMPLETE for this model:

* B subset K(U,P): MODEL_PERSISTENT. G holds in every completion.
* B not subset K(L,P): MODEL_PERSISTENCE_REFUTED. G fails in every completion.
* Otherwise: CANNOT_CHECK. G holds in completion L and fails in completion U.

The first two branches are disjoint by the bracket. In the third branch the two
extremes explicitly witness disagreement; therefore no completion-independent
Boolean answer is possible. This is a statement about UNIVERSAL persistence of
the whole belief, not a pointwise assertion that every state or every execution is bad.

Hostile pair: L empty, U={0 -> bad}, B={0}, P={0}. Dropping the optional edge turns
unknown into a false guaranteed-persistence claim. Treating it as a required edge
turns unknown into a false universal-refutation claim. Both must remain distinguishable.
Parent: may/must and generalized model-checking semantics; stronger general parents
exist. This result is a particularly simple fixed-state, fixed-predicate fragment.

## 5. TV-4: information refinement cannot reverse a decisive answer

For L subset L' subset U' subset U, the set of completions shrinks. Every completion
of the refined model is also a completion of the original model. Hence a universal
positive remains positive and a universal negative remains negative; an unknown
may resolve either way. Equivalently use the kernel bracket twice.

This is NOT a theorem that changing the world preserves old conclusions. Enlarging
U, changing S/P, allowing a new checker/policy, or changing the interpretation of a
state changes the model. Such a change requires a new identity and applicability
check, not a claim that the old proof survives information refinement.

## 6. TV-5: exact boundary of freshness-free reuse

Assume (a) a sound nonempty belief B contains the real starting state, (b) U really
contains every unobserved permitted revision, and (c) P keeps its registered meaning.
Then B subset K(U,P) is sufficient to keep asserting P after any unobserved finite
sequence. It is also necessary for a guarantee against ALL U-permitted paths: if it
fails, TV-2 supplies an allowed path ending outside P. A process unable to distinguish
that unobserved path from a no-change continuation cannot safely promise P in both.

This supplies a POSITIVE complement to the predecessor freshness obstruction. It
is not a new CAP theorem and does not establish production coordination freedom.
The epistemic cost moves to proving the revision envelope, belief soundness and
fixed interpretation. When unrestricted revocation is permitted from every good
state, K is empty. Making the envelope smaller by simply omitting revocations is
not a solution. A missing upper-closure certificate remains CANNOT_CHECK in an
OCM adapter even when a caller can construct this finite model and get an answer.

Conversely an immutable historical statement, narrowly typed as a statement about
a fixed archived event, may have a nonempty K under a suitable revision policy;
this does not make the historical event's current authority or relevance persistent.
Policy validity and action permission may themselves expire and must then appear
in S/P/U. A proof of P creates no permission to act.

## 7. Parent reconstruction and resource boundary

The independently coded descending fixed-point parent equals the reverse-BFS
candidate on every registered finite case. Completion enumeration independently
agrees with the may/must classifier. The asymptotic equivalences follow from the
proofs; finite counts alone are not their authority.

For an already materialized n-state, m-edge adjacency representation, reverse BFS
uses O(n+m) graph operations and O(n+m) workspace. The actual Python implementation
sorts edges for deterministic witnesses, adding O(m log m) comparison work; allocating
and hashing serialized model identities costs additional work. A single witness costs
O(length); emitting all witnesses may take O(n^2) output. The straightforward parent
may scan m edges and n states in each of O(n) iterations. An optimized standard parent
can use exactly the same linear algorithm: there is NO algorithmic superiority claim.

Calibration over all graphs is exponential in n^2; enumerating optional-edge
completions costs 2^(|U minus L|), separate from the two-kernel decision algorithm.
State-space construction, acquisition of a sound abstraction, representation storage,
cryptographic/authentication costs, and actual runtime synchronization are NOT free
and are NOT established by the logical probe counters. No measured production speed,
memory efficiency or energy comparison is reported.

## 8. OCM absorption contract and remaining frontier

An eventual adapter needs: an explicit query/predicate; bound subject, schema, scope,
checker and policy versions; a sound mapping from concrete states to model states;
a certified complete upper relation (including revocation, supersession, configuration,
authority and new-conflict changes); sound initial belief; provenance of required
lower edges; parity tests for each mapped transition; immutable model-bound receipts;
and independent external action authority. The result type must retain MODEL_ scope.
CANNOT_CHECK and refuted-persistence must not become either factual falsity or success.
No OCM implementation is authorized by this reference code.

Precise remaining research targets, not claimed results:
1. Sound abstract-envelope acquisition for open-ended knowledge stores; strongest
   parent is abstract interpretation/may-must abstraction. Falsifier: a concrete
   permitted transition missing from U after mapping. Unknown emerging states remain
   outside this finite proof until represented or conservatively abstracted.
2. Incremental maintenance of K under graph/predicate revisions, compared to strongest
   dynamic reachability/model-checking parents including total preprocessing and update
   work. A bound proportional only to changed edges is NOT asserted.
3. Choosing intervention/refresh actions when persistence is unknown is a changing-world
   partially observed control problem, not the static decision-tree problem in #314.
   Fairness, risks, observation costs and effects require a separately frozen successor.
4. Mechanized proof of the refinement/adapter boundary and genuinely independent
   assumption review. Neither is supplied by this authoring session.

The theorem package advances the usable foundation while correctly returning
PARENT_SUFFICIENT. It does not close Machine Epistemics, #197, #312/#313/#314, the
independent-review gates or any OCM milestone.
