# Machine Epistemics Foundation: corrected finite core and frontier bounds

Identity: ME-FOUNDATION-REVISION-V1; ORION-V2 #313; baseline #310 at
`24566f00a9dc4425a438fcfac05d13c6b2d903db`. This is an additive successor to
`ME_THEORY_GAP_ATLAS_V1.md`, not an edit to its history or to a protected result.

**Status:** self-contained mathematical arguments plus finite exact calibration.
No proof-assistant certification, independent review, OCM parity, empirical language
competence, novelty or overall foundation-completion claim is made. Registry coverage
is not theorem completion. New mechanisms remain research proposals until absorbed.

## 0. Domain, evidence and inference contract

Use a finite set A of root evidence identifiers and a declared context c containing
query family Q, intervention family Gamma, time/epoch, checker identities, semantics,
operator implementations and assumptions. A root is a *logical dependency*, not an
assertion of statistical independence. Root truth/reliability and authorization are
external premises, not consequences of assigning an identifier.

A support profile P is an inclusion-minimal antichain of subsets of A. Write
0 = empty profile; 1 = {empty support}; P + Q = Min(P union Q);
P * Q = Min{p union q : p in P, q in Q}. The order P <= Q means that satisfying
P implies satisfying Q. An interval [L,U] satisfies L <= U. Under revocations R,
lambda_R([L,U]) is LIVE if a support in L avoids R, DEAD if no support in U avoids R,
and UNKNOWN otherwise. The unmodified algebra is inherited from #310.

**DEAD means no admissible support in this contract. It does not mean the proposition
is false.** NEGATED_CLAIM(p) is a distinct proposition requiring its own warrant.
Likewise LIVE means an admissible derivation exists, not unconditional real-world truth.
An exact proof is conditional on its premises, specification and trusted checking kernel.

Maintain four distinct judgments:

    c;E |- p : EXACT_CONDITIONAL_ON_PREMISES
    c;E |- risk(loss, population, selector, horizon) <= epsilon
    current_identity |- certificate : VALID_BINDING | REVALIDATE
    external_policy |- action : AUTHORIZED | NOT_AUTHORIZED

A numerical prediction score inhabits none of these judgments by itself. A coverage
certificate warrants the stated coverage proposition; it does not change every prediction
into an exact assertion. The reference gate is a declarative model using trusted premises,
NOT an implementation that authenticates external certificates.

## F01. Conditional soundness and authority non-amplification

**Statement.** In a finite derivation whose leaves are true under the declared premises
and whose rules are sound for that same context, every conclusion is true under those
premises. If authority coordinates compose by meet, scope by intersection, and internal
transitions cannot create external capabilities, composition cannot grant a capability
absent from a required input. A live proof is insufficient to authorize an external action.

**Proof.** Induct on derivation length. Soundness of each rule preserves the conditional
truth judgment. A meet is <= each argument; intersected scopes are subsets of each input
scope. Thus a missing authorization cannot appear through composition. The action rule
requires a distinct, valid *pre-action* capability. An ActionReceipt reports an effect;
it cannot retroactively authorize that effect. Failed mandatory checks block the current
attempt. A separately identified repair/recheck may establish a new successful attempt;
CANNOT_CHECK is not a permanent absorbing state of the entire machine.

**Boundary.** These premises require enforcement and a complete dependency manifest in
the runtime. A string saying EXACT_CHECKER or an evidence id alone proves nothing.
This is ordinary proof/type preservation and capability discipline, not a new logic.

## F02. Statistical warrant, selection and sequential risk

**Counterexample.** On eight equiprobable input types, a predictor correct on seven and
wrong on one has marginal error 1/8. Select only the erroneous type using its observable
input tag: conditional error is 1. No label access is needed for this construction.
Thus marginal coverage does not entail per-instance truth or validity after selection.
This matches the marginal/conditional distinction in [S1, section 3.1].

**Selection bound.** For failure F and selection S with Pr(F)<=delta and Pr(S)=p>0,

    Pr(F | S) <= min(1, delta/p).

Proof: Pr(F intersect S)<=Pr(F)<=delta. The bound is sharp: nest F inside S when
delta<=p, and S inside F otherwise. The same argument gives Pr_Q(F)<=delta+eta
under a *proved* total-variation bound TV(P,Q)<=eta on the entire relevant event law.
An unmeasured distribution change is not such a bound. [S2] gives substantially more
specialized conformal drift guarantees; no such guarantee is imported here untested.

**Adaptive risk theorem.** Let A_t be a predictable decision to execute invocation t,
F_t its failure, and epsilon_t a nonnegative predictable bound satisfying
Pr(F_t | H_{t-1}, A_t=1)<=epsilon_t on every executed history. Suppose
sum_t A_t epsilon_t<=B almost surely. Then Pr(any executed failure)<=B.
Proof: union bound followed by conditional expectation gives
Pr(union_t A_t F_t)<=E sum_t A_t 1_{F_t}<=E sum_t A_t epsilon_t<=B.
For an unbounded horizon, use monotone convergence. No independence is needed.
The conditioning must include the actual selection policy; ordinary marginal conformal
coverage does not supply this premise. An additional certificate-validity failure event
of probability beta can be included by a union bound, yielding beta+B, when the above
conditional guarantee holds on the certificate-good event.

**Idempotence boundary.** Repeating an evidence citation does not duplicate its provenance.
Repeated output failures are different events: ten independent 0.1-risk uses have failure
probability 1-(0.9)^10, not 0.1. Deduplicate a certificate-failure event only when it is
proved to be the *same event*, not merely the same text/id. Risk-bounded action remains
risk-bounded action, never EXACT truth. Risk control parents [S1-S3] own this territory.

## F03. Root flattening and dependence

For an acyclic derived-evidence graph, replace each derived identifier d by its root
profile phi(d); extend phi using + and *. Then evaluation after substitution equals
nested evaluation for every R subset A. The proof is structural induction, using the
Boolean conjunction/disjunction evaluation homomorphism. Repeated root a gives a+a=a
and a*a=a, so aliases of one source do not create independent support.

Cycles require an explicitly chosen least-fixed-point semantics over the finite lattice;
a recursive call without this semantics is not justified by the DAG proof. Root sharing
captures declared logical provenance, not unobserved statistical confounding. Different
root ids do not license multiplication of probabilities. Parents: ATMS/provenance [S4,S5].

## F04. Nogoods: corrected algebra and its exact boundary

Let N be a family of inconsistent root sets; an admissible support contains none of them.
Define F_N(P)=Min{w in P : no n in N is a subset of w}. Then

    F_N(P+Q) = F_N(P)+F_N(Q)
    F_N(P*Q) = F_N(F_N(P)*F_N(Q)) <= F_N(P)*F_N(Q).

Proof: admissibility is downward-closed. An admissible union has admissible factors;
filtering factors does not remove any admissible final union. Canonical minimization
preserves the same upward-closed satisfaction set. These facts also show that clean
profiles with addition + and product P *_N Q = F_N(P*Q) form the corresponding
absorptive semiring (for an empty nogood, use its degenerate zero algebra).

**Refuted original MEG-16(ii).** With P={{a}}, Q={{b}}, N={{a,b}}, each factor is LIVE
under R=empty, but their filtered product is DEAD. Support-local liveness is therefore
NOT a Kleene-conjunction homomorphism on arbitrary environments. It is a conjunction
*upper bound*, and is still a disjunction homomorphism. Exact conjunction homomorphism
is recovered when the active environment A\R is itself globally N-consistent: any two
supports inside it then have an admissible union. Both readings must be named.

A CONSTRAINT must specify the inconsistent assumptions or certified conflict, not merely
assert that two source strings differ. This is an ATMS parent reconstruction, not novelty.

## F05. Query-relative learning and revocable agreement warrants

Fix a finite hypothesis class H, query x, and correct, indexed lessons E consistent with
some target h* in H. V(J) is the nonempty subset consistent with J. Admit answer y at x
exactly when every h in V(E) gives y. Its profile is

    W_x,y = Min{J subset E : V(J) nonempty and all h in V(J) satisfy h(x)=y}.

For every deletion R of lessons, this profile has a surviving support iff the remaining
version space agrees on y at x. Proof: surviving support implies agreement on any
consistent superset; conversely E\R itself witnesses agreement and has a minimal subset.
The consistency premise matters: contradictory lessons must produce CONTRADICTION,
not an answer by vacuous universal quantification. Uniqueness of h is unnecessary.

This closes a finite, realizable, noiseless fragment of MEG-12/13. Enumerating supports
costs up to 2^|E| version-space evaluations. Efficient grammar learning, unknown H,
noisy lessons and out-of-class targets are not solved by this proof. Parents: version
spaces/exact learning [S7] and ATMS; no equal-information architecture separation.

## F06. Trace, static and repeated-procedure warrants

A bounded, well-typed trace must carry warrants for executed steps, guards, inputs,
checker versions and any read state. Its warrant is their conjunction. A conservative
static certificate conjoins obligations from all declared reachable traces; it is <=
each trace's certificate, provided both use the same context and trace obligations.
This static rule is sufficient, not generally necessary or the most precise summary.

Fixed support W repeated k>=1 times satisfies W^k=W. **This does not prove that a loop
with changing inputs/evidence has warrant W.** Iterations supported by {a} then {b}
need {a,b}. The existential Kleene-star reading contains the zero-iteration trace,
so 1+W+W^2+...=1 in this absorptive algebra. It says nothing about successful termination
or universal loop correctness. Guard warrants cannot be dropped. KAT [S6] owns the
program algebra; runtime traces must declare which interpretation they use.

## F07. Full-signature reopening and output-sensitive maintenance

For every cached object v, define its obligation signature sigma(v): semantic payload,
query/specification, support interval, scope/epoch, authority, operator/checker identity,
normalization and any risk/selection contract relevant to its use. Let D be a complete
read-dependency graph for a finite pure acyclic computation; structural edits use the union of old and new read dependencies
conservatively before invalidation. Let C be the changed roots and Reach_D(C) their
least forward-closed impact cone.

Recompute the cone in dependency order. Outside it, output is unchanged by induction:
no input or operator read there changed. Rechecking work is
O(|V_cone|+|E_cone|+sum_{v in cone} cost(v)), assuming indexed reverse dependencies and
charging certificate checks/index maintenance. This is an upper bound, not a theorem
that graph reachability equals the semantically minimal change set. Cyclic computations
require a separately justified fixed-point solver and its convergence cost.

**Two counterexamples to MEG-19.** DEAD AND LIVE changing to DEAD AND UNKNOWN stays DEAD;
thus changing some constituent is not sufficient to change a conjunctive summary.
Conversely, a live constituent can change payload 1 to 2 while remaining LIVE, changing
a dependent answer. Liveness-only reopening misses that change. An alternative live
support can also mask revocation. The correspondence certificate itself is a dependency.
These observations correct claims of exact interference in MEG-22 as well.
Immutable snapshots alone do not imply serializability: two transactions can each read
x=y=1, independently set x or y to 0 after seeing the other equal to 1, and jointly
violate x OR y. Read/write conflict validation or another serializable commit protocol
is a separate premise, not supplied by immutability. Incremental
computation parents [S8] own the maintenance principle; OCM integration remains untested.

## F08. Epochs, testimony and target-relative feedback

Treat valid-time/epoch and transaction identity as explicit dependencies. Expiry and
supersession invalidate the applicable support, never delete the historical observation.
`said(person,p)` can have a transcript-backed warrant while p remains unsupported.
A speech act, a speaker commitment and a world claim are three different propositions.
Their authority coordinates cannot be conflated by F01.

Feedback can warrant the observation that a reward/click/utterance occurred when its
measurement contract is valid. It does NOT automatically warrant a general factual
claim or procedure. Registered discriminating outcome observations can eliminate
hypotheses under F05; unregistered rewards can adjust ranking only. Therefore the
unqualified statement 'feedback can never be evidence' is a policy over target types,
not an impossibility theorem. Changing weights preserves support liveness when labels
are fixed; it need not preserve activation-threshold firing. Eligibility and firing
must be separately named. DEAD never licenses rendering 'not p'.

## F09. Graded navigation: contraction, retraction and certified error

Let alpha in (0,1], beta=1-alpha. Let P(g) be a nonnegative row-substochastic matrix
on a finite state set and s(g)>=0 with norm_1(s)<=1. The gate vector g is in [0,1]^m.
Assume P and s are coordinatewise nondecreasing in g; products of gates with fixed
nonnegative structural coefficients and frozen denominators satisfy this assumption.
Define a(g)=alpha s(g)+beta P(g)^T a(g).

**Existence/error.** The map is a contraction in l1 with factor beta, hence has a unique
fixed point a=alpha sum_{j>=0} beta^j (P^T)^j s. Starting a_0=alpha s, the k-th iterate
is its first k+1 terms. Thus 0<=a_k<=a and

    norm_1(a-a_k) <= beta^(k+1) norm_1(s).
    norm_1(a-x) <= norm_1(alpha s + beta P^T x - x) / alpha.

The second inequality follows by applying the contraction inequality to a-x and moving
beta norm(a-x) to the left. It also applies to arbitrary numerical approximations x,
provided a rigorously enclosed residual includes rounding/input error. No such enclosure
for OCM's floating implementation is certified here. At alpha=1 the fixed point is s.

**Monotone retraction.** If h<=g, then a(h)<=a(g) entrywise. Proof: each nonnegative
Neumann term is monotone. Gate-zero removes the corresponding coefficients, including
removed head shares; they must not be reassigned to survivors. Differences can propagate
only forward from changed seed coordinates or heads of changed matrix entries in the
union graph. Outside that reach the path expansions are identical.

**Perturbation.** For two admissible systems (P,s),(Q,t), with fixed points a,b,

    norm_1(a-b) <= norm_1(s-t) + (beta/alpha) norm_1((P-Q)^T b).

Subtract equations and use norm_1((I-beta P^T)^(-1))<=1/alpha. For a one-state system
P=1, Q=1-d and s=t=1 the bound is attained. Thus the amplification factor beta/alpha
cannot generally be improved under these assumptions.

This proves a graded-dynamics fragment of MEG-02/06. It does NOT construct a probability
semiring for correlated evidence; activation is neither confidence nor truth. Denominator
renormalization or arbitrary signed interactions invalidate the monotonicity assumptions.
Parent methods: nonnegative linear systems, Neumann resolvents and PageRank contraction.

## F10. Structural rollback requires structural restoration

Consider s=(1,0,0), alpha=1/2, and one unit edge a->b. Its fixed-point activation at b
is 1/4. Add an equally weighted edge a->c and recompute the denominator at a as 2.
Revoke the added edge without restoring that denominator: the surviving a->b coefficient
is 1/2 and b's activation is 1/8. All new warrants can be revoked while old answers move.
Therefore MEG-18's revocation-only rollback claim is false without additional conditions.

A sufficient rollback contract restores the prior transition operator, seed convention,
restart, background/extraction convention, semantic payloads, dependencies and contexts.
On an identical state space, equality of the fixed-point response for *all seeds* at a
fixed alpha in (0,1) is equivalent to equality of P: invert the equal resolvents.
At alpha=1 navigation ignores P, so the converse is false. Snapshot restoration is valid
only for an isolated transaction or a causally correct undo; it must not discard unrelated
intervening writes. Logical retraction and transaction rollback are different operations.

## F11. Query/lifecycle sufficiency, not just graph preservation

On a finite world set W and declared tests T=Q x Gamma, a representation kappa supports
all registered answers and revisions iff its fibers refine equality of the complete
answer/revision signature f_T(w). Proof: necessity follows because a deterministic decoder
cannot return two different signatures from one encoding; sufficiency defines the decoder
on each constant-signature fiber. This is a standard quotient/sufficient-statistic fact.

Lumpability can preserve a walk and warrant measurability can preserve support statuses,
yet equal graph behavior need not preserve payload-dependent answers. A proof/certificate
must bind the query decoder, content, signature family and correspondence. Exhaustion of
a finite *complete* domain is one certification method; a mathematical proof is another.
Experiments are not the only possible sufficiency certificate. Non-quotient embeddings
and DPO rewrites are candidate implementation techniques, not necessary-and-sufficient
conditions for all semantic preservation. OCM must verify the actual obligation signature.

## F12. Ambiguity, grounding and renderer limits

Let I be a nonempty set of possible interpretations containing the true interpretation.
A query answer y is sound under ambiguity when every i in I gives y, with valid
interpretation/answer contracts. Proof: the actual interpretation is a member of I.
Singleton I is sufficient but not necessary. Two possible meanings may disagree elsewhere
and agree on the question being answered. A rank score alone does not establish I's
coverage or license deleting alternatives.

Equal canonical meanings implying equal seeds is a useful sufficient contract. Equal
extraction does NOT imply equal meanings: seeding/extraction can be many-to-one. Graph
isomorphism also does not certify natural-language semantic equivalence. A renderer with
no store-write capability cannot mutate warrants, but can still utter a false sentence.
Every externally asserted proposition needs a semantics-preserving link to the checked
plan; read-only access is not that link. Prefix satisfiability is insufficient if an
already-emitted prefix contains an unsupported assertion. Natural-language equivalence,
coverage of interpretations and discourse realization remain empirical/proof obligations.

## F13. Information accounting without a false subadditivity rule

For nonempty nested finite version spaces V_0 superset ... superset V_k define
I_i=log2(|V_{i-1}|/|V_i|). Then sum I_i=log2(|V_0|/|V_k|) exactly by telescoping.
Contradictory empty spaces produce CONTRADICTION, not infinite earned information.

The unconditional per-lesson gains need not be subadditive: take |V|=4,
A={0,1,2}, B={0,1,3}. Each lesson gains log2(4/3) bits, but their joint gain is
log2(4/2)=1 > 2log2(4/3). Thus MEG-31's general dependent-lesson subadditivity claim
is false. Repeated identical lessons do add zero *conditional* information.
These counts are not physical description lengths or a universal cross-channel price;
charge lesson bytes, access, verification, computational work and hidden assumptions
separately. Statistical expected information requires its own probability model.

## F14. Parent sufficiency: theorem identity versus empirical equivalence

An algorithmic identity on a declared class can establish exact parent sufficiency on
that class without a significance test. An empirical tie cannot. For n independent
Bernoulli task-discordance indicators with zero observed discordances, the one-sided
(1-eta) confidence upper bound on discordance probability is 1-eta^(1/n): solve
Pr_p(zero)=(1-p)^n=eta. For eta=.05 and n=50, this exceeds .05; n=59 is the first
integer for which it is at most .05. This is a *discordance* bound, not a generic
quality-equivalence, cost-dominance or signed paired-effect test. Repeated seeds within
a task are not independent tasks. A preregistered estimand/margin is required for any
empirical equivalence claim. A parent-owned exact identity and an underpowered tie
must remain distinct terminals.

## F15. Bounded progress, obstruction and negative-side refinement

A finite computation whose nonterminal transitions strictly decrease a natural-number
fuel counter, with mandatory typed handling of exhausted fuel, terminates. This proves
bounded progress, not eventual solution. A strictly increasing bounded real-valued meter
does not suffice: positive costs 2^(-t) have finite total and permit infinitely many
transitions. A finite Jump-level alphabet also permits cycles unless a well-founded
measure decreases. A missing reachable target in a COMPLETE finite
search class certifies an obstruction only for that class; timeout does not. Neither
graph-rewrite syntax nor a proof of type preservation proves that a new solver improves.

At a fixed context, [L',U'] refines [L,U] only when L<=L'<=U'<=U. A proposed upper profile
excluding an exhibited lower support is a conflict, not a refinement. A checked refutation
can take [0,1] to [0,0] without exhaustive enumeration of every possible positive proof.
A negative query with sufficient semantics can also narrow U. Therefore 'only closure
experiments can resolve DEAD-side uncertainty' is too strong. A change of context,
assumptions or nogoods can legitimately invalidate prior LIVE/DEAD states and must be
recorded as revision rather than same-context refinement.

## F16. Joint computational-epistemic commitment theorem

This is the package's frontier synthesis, not a novelty claim.
Suppose (i) F09 supplies a rigorous activation error bound e; (ii) each of finitely many
candidate action utilities u_j is L-Lipschitz in l1 on that state; (iii) the approximate
winner has a score margin strictly greater than 2Le; (iv) required exact premises or
conditional action-risk contracts are valid and bound to the active selector; (v) all
read dependencies/signatures are tracked as in F07; and (vi) pre-action authority holds.
Then the selected action is the unique exact-state utility maximizer, reuse outside a
complete changed-dependency cone is sound, and executed failures satisfy F02's B bound
(or beta+B when the separate certificate-failure condition applies).

**Proof.** Each utility differs from its exact value by at most Le. A margin >2Le survives
both opposing perturbations. Dependency induction is F07, while conditional expectation
and the union bound are F02. Their obligations are conjunctive: no conclusion substitutes
for a missing premise of another. Equality at 2Le can create a tie, so strictness matters.

**Useful new research target.** Compare exact-all-state recomputation to certified local
approximation over naturally coupled, revocable task families, measuring the full vector
(storage, query work, repair work, certificate work, abstention, realized loss). A real
residual requires a strongest-parent construction under the same information, selector,
verifier and total resource access. This theorem does not supply that residual or a
learnable optimal scheduler. It does supply a falsifiable mechanism for safe approximate
computation without confusing speed, evidence and authority.

## F17. Causal evidence is not observational provenance

Let U be an unbiased bit. Model M1 has X=U, Y=X. Model M2 has X=U, Y=U.
Both give exactly Pr(X=Y)=1 with equal mass on (0,0),(1,1). Under do(X=0), M1
has Y=0 surely while M2 has Pr(Y=1)=1/2. Thus even complete observational provenance
cannot identify this intervention without additional assumptions or interventional data.
This is a standard structural-causal-model indistinguishability witness [S9]. An OCM
causal certificate must bind the structural assumptions, intervention, outcome/estimand,
identification argument and data-generating/measurement regime. The witness closes an
anti-laundering guard, not the full causal-discovery/experimental-design programme.

## F18. Verifier dependence and specification fidelity

Let two verifiers fail on the same one of eight equiprobable worlds. Requiring both to
accept leaves false-acceptance probability 1/8, not (1/8)^2. Different process ids or
repeated evaluations do not establish error independence. Conversely, an exact kernel
can correctly verify translated proposition p' while p' differs from the user's p.
Kernel correctness does not prove translation fidelity. The necessary composition is
source-to-specification fidelity AND sound checker execution AND valid premises, with
all versions bound. This follows directly from conjunction of proof obligations; the
statistical variant uses F02 with the actual dependence/selection law. Such internal
checks do not count as independent external scientific review.

## Source/parent audit boundary

Sources and inspection depth are in SOURCES.md. F01-F18 have self-contained arguments;
parent labels are concessions, never proof by citation. The external literature search
was targeted, not saturated. No claim is made that this is the first occurrence of these
bounds or their combination. In particular, no full-paper reconstruction is claimed for
sources available only as abstracts. The next independent reviewer should reconstruct
the statements from their quantified assumptions, not treat checker counts as proof.
