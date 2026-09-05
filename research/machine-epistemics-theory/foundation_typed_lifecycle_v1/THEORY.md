# A typed warrant, risk and lifecycle calculus

**Identity:** ME-FOUNDATION-TYPED-LIFECYCLE-V1; ORION-V2 #312.
**Baseline:** `24566f00a9dc4425a438fcfac05d13c6b2d903db`.
**Status:** sixteen written mathematical arguments, exact development calibration, independent review not obtained. None is claimed novel. The arguments, finite checks, proof-assistant lemmas and runtime adoption are separate evidence classes.

This is an additive correction to `../ME_THEORY_GAP_ATLAS_V1.md` and `../KSO_THREE_VALUED_WARRANT_AND_REOPENING_V1.md`. Their original bytes and historical claims are not rewritten. `ATLAS_MAP.json` gives every MEG-01..35 a scoped disposition. A correct special case does not close an entire row.

## 0. Objects, interpretation and trust boundary

Fix a finite base evidence universe E, a current available set A, a family N of inconsistent assumption sets (nogoods), a registered target language, and an external interpretation of that language. A support is a subset of E. A profile P is an inclusion-minimal antichain of supports. Write 0 = empty profile and 1 = {empty support}. Alternative P + Q is minimal union; product P * Q consists of minimal unions of one support from each factor. Write P <= Q when every support in P contains a support in Q: Q is at least as easy to satisfy.

A claim is typed by **proposition, target/specification, quantifiers, context, evidence lineage and epoch**. Its interval [L,U], L <= U, bounds its admissible support function. A LIVE label reports an exhibited admissible support; DEAD means none survives within the certified upper bound; UNKNOWN reports unresolved support. **DEAD(p) is not proof of not-p.** The proposition may remain true after the only available proof is revoked. Soundness of admitted base evidence and inference rules is an explicit semantic assumption, not supplied by a graph label.

Keep at least these distinct claim types:

- EXACT_TARGET: a particular formal target checked under named assumptions;
- OBSERVED: a named measurement, transcript or external result, including its measurement contract;
- RISK_BOUND: a distributional or sequential error statement with explicit randomness and quantifiers;
- ACTION_AUTHORIZATION: externally granted permission for an effect under a policy.

For example, a transcript can warrant `said(user,p)`, not p. A coverage certificate can warrant a statement about a prediction rule, not exact correctness of its next output. A successful action receipt records an effect after execution; it cannot retroactively grant permission to execute it.

The reference implementation is a finite, pure research model. Certificate checkers and authority capabilities are **trusted inputs**. Hashes bind identity, not authenticity, truth, independence, calibration adequacy or scientific authority. There are no real external effects in this package.

## T01. Provenance substitution, without fictitious independence

**Statement.** Assign each derived evidence symbol e a fully expanded profile phi(e) over common base evidence. Extend phi to positive expressions by alternatives and products. Then phi(P + Q) = phi(P) + phi(Q) and phi(P * Q) = phi(P) * phi(Q). In this idempotent instance, two aliases for the same base support do not create two independent supports.

**Proof.** Expand each expression as disjunctions of conjunctions. Substitution distributes over both operations. Canonicalization removes duplicate and absorbed terms without changing the monotone Boolean function. This proves the identities; substitution of the same profile twice reduces by Boolean idempotence. Equivalently this is the monotone-Boolean/support instance of provenance-semiring homomorphism [S1].

**Boundary.** General provenance semirings need not be idempotent. Neither different evidence IDs nor disjoint recorded provenance establish stochastic independence. Two copies of a Bernoulli error with probability p have joint error p, not p squared. Cyclic provenance requires separately specified least-fixed-point semantics and cannot justify itself. Nogoods must be checked after expansion into the same evidence universe.

Checker: `check_substitution`; 14,400 substitution pairs, both identities; shared-source, distinct-source and unresolved-source controls.

## T02. Contradictions require a shared consistent witness

Define F_N(P) = Min{W in P : no N in N is a subset of W}. On normalized profiles use P star Q = F_N(P * Q), with ordinary alternative addition.

**Statement.** F preserves alternatives, is idempotent and monotone, and

    F(P * Q) <= F(P) * F(Q)
    F(P * Q) = F(F(P) * F(Q)).

Normalized multiplication is associative and distributes over addition. The identity is F(1); when the empty set is a nogood the algebra degenerates to the one-element zero algebra, which must be disclosed as inconsistent rather than used to prove arbitrary claims.

**Proof.** A discarded support contains a nogood; every superset also contains that nogood. It can therefore contribute no consistent product later. This establishes the second identity. The first follows because filtering can only discard product supports. Consistent minimal supports survive either order of alternative union; a subset of a consistent support is consistent. Hence addition commutes with filtering. Replace each intermediate product by the second identity and use associativity/distributivity of unfiltered Boolean products to obtain the normalized laws.

**Shared-world semantics.** `holds(F(P * Q), A)` iff there is one consistent W subset A such that holds(P,W) and holds(Q,W). A surviving product support is such a W. Conversely, supports for P and Q inside a consistent W have a consistent union; a minimal such union survives filtering.

**Counterexample to the atlas's scalar conjunction homomorphism.** Let P={{a}}, Q={{b}}, N={{a,b}}, and A={a,b}. Each claim has a consistent supporting environment, but there is no consistent environment supporting their conjunction. Individual LIVE and LIVE compose to DEAD. Filtering both factors before multiplying, without filtering the product, is wrong.

For intervals, apply F after product to both bounds. In the truth order DEAD < UNKNOWN < LIVE, the conjunction verdict is <= the minimum of the two separate verdicts, not generally equal. Alternatives retain the exact three-valued disjunction law. Restoring equality requires a common-context compatibility condition. An observation can be stored without endorsing every jointly inconsistent factual interpretation.

Parents: assumption-based truth maintenance and nogoods [S2]; the proof here is self-contained. The OCM M2 branch already used a sub-homomorphism description in its historical implementation; this note does not claim that correction originated here.

Checker: `check_nogoods`; all 20 canonical nogood families on three assumptions, 8,000 profile pairs, 64,000 shared-world comparisons and 28,926 normalized triples.

## T03. Upper-bound certificates must be sound refinements

**Statement.** Suppose both L <= P_true <= U and Lc <= P_true <= Uc hold under the same target, scope, epoch and nogoods. Define L' = L + Lc and U' = U * Uc. Then L' <= P_true <= U', so L' <= U'; [L',U'] refines both intervals. With fixed A and N, a previously LIVE or DEAD verdict cannot reverse under refinement.

**Proof.** Both lower functions imply P_true, so their disjunction does. P_true implies both uppers, hence their conjunction. Lower bounds only grow in the implication order and upper bounds only shrink. F_N and evaluation at A are monotone, so surviving lower support and absence of possible upper support are preserved respectively.

**Boundary.** Inconsistent bounds are a conflict, not a more informative certificate. Checking L' <= U' does not itself verify their semantic relation to P_true. A new scope, revoked evidence, altered target, or added nogood is a model change, not the fixed-context refinement theorem. An arbitrary family of allegedly exhaustive alternatives is not an upper certificate without an external justification of exhaustiveness.

Checker: `check_intervals`; all 168 intervals on three assumptions, 225,792 unconstrained conjunction cases and 27,920 refinements; conflicting upper certificate refused.

## T04. Population coverage is not selected-case truth

Let B be an error event under one declared probability measure. If P(B) <= alpha and P(S) >= pi > 0, then

    P(B | S) <= min(1, alpha / pi).

**Proof.** P(B intersect S) <= P(B) <= alpha; divide by P(S). The bound is sharp: for alpha <= pi put all error mass alpha inside S of mass pi; for alpha >= pi put S wholly inside B. This is an elementary conditional-probability bound, not a new conformal theorem [S3].

Thus 95% marginal coverage permits 100% error in a selected 5% subpopulation. Even a valid guarantee averaged over calibration datasets is not automatically conditional on the one calibration dataset already observed. Selection can include abstention, routing, choosing a proof strategy or choosing which claim to publish.

**Calibration parent.** For a fixed scoring rule, n calibration scores and one test score that are exchangeable, take the calibration order statistic k = ceil((n+1)(1-alpha)), with threshold +infinity if k > n. Uniform rank with distinct scores gives test coverage min(k,n+1)/(n+1) >= 1-alpha. Conservative tie handling preserves the lower bound. The scoring rule's training/adaptation must be accounted for before claiming exchangeability. The checker illustrates this result; it does not calibrate a real OCM operator.

Checker: `check_selection_and_conformal`; 65,280 error/selection pairs on eight points, 600 distinct-rank permutations, 32 tied-score orbits. A wrong finite-sample quantile has 3/5 rather than required 4/5 coverage.

## T05. Two legitimate routes to risk control under adaptive use

**Predictable-exposure route.** Let F_t be a filtration, I_t in {0,1} and q_t in [0,1] be F_(t-1)-measurable, and B_t be the next potential error. Assume, whenever I_t=1,

    P(B_t | F_(t-1)) <= q_t,
    sum_t I_t q_t <= epsilon almost surely.

Then P(exists t: I_t=1 and B_t) <= epsilon, over a finite or countable horizon.

**Proof.** The union indicator is bounded by sum_t I_t 1_(B_t). Conditional expectation gives E[I_t 1_(B_t)] <= E[I_t q_t]. Sum and use monotone convergence for the countable case. No independence between attempts is required. Stopping decisions based on past observations are incorporated in I_t.

If all bounds hold on a common validation-good event G in F_0 with P(G complement) <= eta, the total failure probability is at most eta + epsilon: split off G complement and apply the same conditional argument on G. This requires the stated conditional bounds on G, not merely a label saying validation passed.

**Fixed-family route.** Alternatively, fix a finite/countable universe of potential exposure events B_j with valid marginal bounds alpha_j and sum_j alpha_j <= epsilon. Any adaptively chosen subset has an error event contained in the union of that whole universe, so the same epsilon bound holds. One must budget the **whole declared family**, not retrospectively just the selected tests. A new adaptive input outside that universe has no inherited guarantee.

These are ordinary union-bound and sequential-validity constructions; stronger anytime methods are parents, not claimed inventions [S4,S5]. The pure `commit_gate` implements the conservative predictable-exposure route only. Its refusal of a marginal certificate does not say every use of marginal guarantees is impossible.

A new exposure consumes risk again even when it reuses the same certificate. Replaying the same immutable event is not a new exposure. Shared validation failure can be charged once only when it is genuinely the same event G; per-exposure errors cannot be deduplicated by certificate ID.

Checker: `check_adaptive_risk`, `check_budget_and_locality`; 216 two-step predictable policies with exact path probabilities and immutable-budget controls. The fixed-family argument is written above; no separate empirical deployment is claimed.

## T06. Drift, target change and selection have an explicit joint price

Let P,Q be measures on a common measurable space, B the old error event and B' the new error event. Suppose

    P(B) <= alpha, TV(P,Q) <= tau,
    Q(B symmetric_difference B') <= d, Q(S) >= pi > 0.

Then

    Q(B' | S) <= min(1, (alpha + tau + d) / pi).

**Proof.** Q(B') <= Q(B) + Q(B symmetric_difference B') <= P(B) + tau + d. Apply T04. Without selection, omit division by pi. A bound of one is uninformative, not an error.

**Sequential consequence.** These same inequalities may be used to construct predictable q_t in T05 only if the underlying bounds hold conditionally on F_(t-1), with all bound parameters and applicability checks available before the action. A marginal conformal certificate does not supply this stronger premise.

**Boundary.** A changed hash proves an identity mismatch, not that a guarantee became false. Either revalidate or provide a sound semantic transport certificate bounding drift and target disagreement. Unknown tau or d cannot be silently set to zero. Byte-identical models can also face distribution shift. TV is not automatically estimable distribution-free from small samples.

Checker: `check_drift` for all 14,400 pairs of events under rational distributions on three points; T04 supplies the selection step.

## T07. Graded navigation: convergence, certified error, monotonicity and locality

Let n be finite; let P be a nonnegative row-substochastic n by n matrix; let s >= 0 have l1 norm at most one; let 0 < alpha <= 1 and beta=1-alpha. The operator may be assembled from fixed nonnegative incidence shares times gates in [0,1], provided decreasing gates cannot increase any entry. **Normalization is fixed for this comparison.**

For F(x)=alpha*s + beta*P^T*x:

1. F is an l1 contraction with factor beta and unique fixed point
   a = alpha * sum_(j>=0) beta^j (P^T)^j s.
2. Starting x_0=alpha*s and iterating k times gives 0 <= x_k <= a coordinatewise and
   ||a-x_k||_1 <= beta^(k+1) ||s||_1.
3. Any candidate y has certified error ||a-y||_1 <= ||F(y)-y||_1/alpha.
4. If P' <= P and s' <= s coordinatewise, then a' <= a.
5. In common coordinates,
   ||a'-a||_1 <= ||s'-s||_1 + (beta/alpha) ||P'^T-P^T||_1 ||s||_1.
6. The change is supported inside the P'-forward reach of changed seed coordinates and heads of changed matrix entries. Their union-graph reach is also a valid conservative region.

**Proof.** The induced l1 norm of P^T is the maximum row sum of P, hence at most one. This gives contraction and the Neumann expansion. Positivity gives partial-sum ordering; summing the geometric tail gives (2). The triangle inequality gives ||a-y|| <= beta||a-y|| + ||F(y)-y||, proving (3). Nonnegative multiplication preserves ordering in every series term, proving (4). Subtract the fixed-point equations:

    a'-a = (I-beta*P'^T)^(-1)
           [alpha*(s'-s) + beta*(P'^T-P^T)*a].

The inverse norm is at most 1/alpha and ||a||_1 <= ||s||_1, proving (5). The bracketed vector is supported on the changed seeds and changed-entry heads; successive powers of P'^T propagate only forward, proving (6).

This closes a **restricted mathematical part** of the atlas's graded-gate question without claiming that gate values are probabilities or warrants. UNKNOWN may influence explicitly exploratory ranking; it must not become exact factual warrant. For approximate arithmetic, the residual itself needs a validated error bound; use (measured residual + certified rounding error)/alpha. Ordinary floating residual output is not such a certificate. For the predicate a(t) >= theta, the lower bound >= theta proves FOUND and the upper bound < theta proves NOT_FOUND; otherwise this bracket alone is unresolved. Equality at an attained lower bound can decide FOUND. A width-only future-budget estimate is not a minimum deciding budget: with P=[1], s=[1], alpha=1/2, x_0=1/2 and theta=7/10, the first iterate 3/4 already proves FOUND, although the first index with tail width < theta-x_0 is 2. See POST_BASELINE_DELTA.md for the concurrent #317 comparison.

Parents: contraction/positive linear systems, Neumann resolvents and personalized PageRank [S7]. Hypergraph constructions must establish the matrix premises, not merely name a random walk [S8].

Checker: `check_navigation`; 36 rational two-state matrices, four seeds, three restart values; 2,592 iteration cases, 5,184 operator perturbations, 900 ordered decreases and 1,728 seed changes. Positive finite agreement is calibration, not the proof above.

## T08. Structural rollback must restore the effective operator

**Counterexample.** With alpha=1/2, seed concentrated at x and one unit edge x->y, a_y=1/4. Add an equal-weight edge x->z, so x's denominator becomes two. Revoke the added edge but retain that denominator: the surviving x->y share is 1/2 and a_y=1/8. All new authority can be revoked while old navigation still changes.

**Corrected statement.** Exact rollback of navigation and extraction follows when a transaction restores the pre-change effective matrix, seed, restart coefficient, background, extraction parameters and coordinate interpretation (or a checked conjugate representation), as well as all relevant warrant/context versions.

**Proof.** Restored inputs define the same contraction and therefore the same unique fixed point by T07; deterministic extraction on identical inputs is identical. Retaining removed structure is necessary to reconstruct its old role but does not by itself restore normalization. A reversible delta or immutable pre-change snapshot must contain those data.

Checker: exact 1/4 vs 1/8 witness and full-operator restoration in `check_navigation`. No proof is claimed for arbitrary concurrent graph rewrites or external-effect rollback.

## T09. Dependency cones bound maintenance, not inevitable semantic change

Fix a finite directed acyclic dependency graph, complete reverse indexes, immutable base values and pure deterministic derived-node functions. A base-value change can alter derived values only in the forward dependency cone. Recomputing that cone in topological order restores exactly the from-scratch derived values.

**Proof.** Outside the cone no parent changed. Induct in topological order: base values and recomputed parents equal the from-scratch values, hence each deterministic node does too. Every node outside the cone remains identical by the same induction.

**Cost.** With the given indexes, work is bounded by the visited incidence count plus the sum of actual evaluation costs for revisited nodes. Include index construction, provenance materialization, dependency discovery, storage and validation in total resources. There is no universal O(number-of-changed-nodes) promise. Cyclic/incremental fixed-point maintenance needs separate assumptions and algorithms.

**Corrections.** A summary being a conjunction means a change in its verdict requires a changed factor when the composition rule is fixed; the converse is false. One child can change while another already-DEAD child keeps the summary DEAD. Shared evidence likewise need not change a claim with surviving alternatives. An unchanged LIVE/DEAD/UNKNOWN label does not imply unchanged payload or unchanged applicability. A RECHECK node need not have a live alternative: it may have remained DEAD or UNKNOWN throughout.

The smallest graph-closed impact cone is not necessarily the smallest semantically changed set. Primitive liveness-change discovery itself must be charged; defining C as the set of all changed nodes does not give a local algorithm for obtaining C.

Checker: summary and alternative-support witnesses, least reachability through a cycle in `check_budget_and_locality`. The DAG recomputation theorem is proved above; no full incremental runtime or general KS-T12 efficiency theorem is claimed.

## T10. Bounded positive work needs a non-Zeno premise

If each of k transitions consumes at least one integer work unit and total work <= B, then k <= B. More generally costs >= c_min > 0 imply k <= floor(B/c_min).

**Proof.** Sum the lower bounds on transition costs. The integer statement is a direct induction on the trace length.

**Counterexample.** Strictly positive real costs alone are insufficient: costs 2^(-t), t>=1, sum to one over an infinite sequence. A finite Jump-level set also permits infinite cycling among levels. Charge every retry, learner update and no-op loop, or provide a separate well-founded variant. Blocking external calls additionally require a termination/timeout assumption. CPU work bounds do not themselves bound wall-clock waiting.

Checker: positive integer `Budget`, uncharged-step rejection and finite prefix of the geometric counterexample. The infinite counterexample is established by the geometric series argument, not by its finite prefix.

## T11. Immutable snapshots are not serializable transactions

A valid snapshot does not make independently validated concurrent writes globally valid. From state (0,0) with invariant x+y<=1, one transaction can read (0,0) and write x=1 while another reads (0,0) and writes y=1. Each sees a valid candidate; their union violates the invariant. This is the classical snapshot-isolation write-skew distinction [S6].

**Sufficient finite-model rule.** Each operation computes a pure candidate from a versioned snapshot; an atomic compare-and-swap validates the complete relevant read version and the invariant, and commits exactly that candidate as the next version. Failed comparisons retry without effects. The successful commits are equivalent to their linearization order and preserve the invariant inductively.

**Proof.** At each successful atomic commit the checked predecessor is the actual current predecessor. Its checked successor satisfies the invariant. Order successes by the atomic commit points and induct. This is not obtained just by using immutable values.

**Boundary.** Dynamic read-set completeness, distributed linearizability, crash recovery, durable logs and exactly-once external effects are additional obligations. Reserve risk/work and check certificate/evidence epochs in the same commitment transaction. A receipt written after an unrecorded effect cannot undo it.

Checker: two-coordinate witness and stale-second-version detection; no production exploit or deployment verification is claimed.

## T12. Query-specific learning with revocable lessons

Let H be a finite, nonempty explicit hypothesis class; each lesson e restricts it to H_e. For lesson set S define V(S)=intersection of H with all H_e in S. Fix a query q and answer a. Compile the inclusion-minimal subsets S for which V(S) is nonempty and every h in V(S) answers q with a.

**Statement.** For any active lesson set A with V(A) nonempty, a compiled support is contained in A iff all h in V(A) answer a. If the real hypothesis h* belongs to V(A), that answer is correct. Revocation removes lessons; exact retention is decided by the surviving minimal supports. Global identification of h* is unnecessary.

**Proof.** A surviving support S subset A has V(A) subset V(S), so its unanimous answer remains true on V(A). Conversely if V(A) agrees, A itself is a support, and finite subset minimization yields a minimal support inside A. Membership of h* gives semantic soundness. Revocation simply replaces A by a subset and reuses the same equivalence while its consistency premise holds.

**Costs and limits.** Brute-force compilation tests 2^m subsets for m lessons and at least O(2^m |H| m) consistency work, plus support canonicalization and storage. The library implementation caps compilation at 12 lessons and 256 hypotheses. Empty V(A) is a conflict, not vacuous proof; class misspecification and bad lessons invalidate the true-hypothesis premise. No bound on natural-language learning or advantage over equally informed parents follows. This is version-space agreement plus provenance, not a new learning class [S1,S9].

Checker: eight affine Boolean functions on two bits, eight teachers, four queries and 16 revocation masks = 512 oracle comparisons. A target withheld as a direct lesson can remain derivable from the other three; removing all support reopens it. Contradictory lessons do not warrant arbitrary answers.

## T13. Meaning preservation is directional and query-relative

Equal canonical meanings imply equal seeds when grounding is a function; equal seeds and identical runtime state imply equal deterministic extraction. Neither converse follows without injectivity/faithfulness assumptions. A many-to-one seed map can map both p and not-p to the same seed. Two codecs can agree on the same wrong interpretation.

If an admitted nonempty set M of possible meanings contains the true meaning and every m in M yields answer a to q, then a is correct for q. Restricting M to a nonempty subset preserves this agreement; revocation may expand M and force reopening. This is the same agreement argument as T12. It is unnecessary to collapse every ambiguity before answering a query on which all alternatives agree.

A renderer must not elevate a plan's epistemic type. Every external factual assertion must be entailed by appropriately warranted plan content; every denial needs warrant for the negation, not DEAD for the positive. Rendering is a separate semantic check: read-only capabilities prevent state mutation but not an incorrect sentence. Prefix grammatical feasibility alone does not prove factual entailment of every future completion.

Checker: equal-seed/different-meaning, robust-agreement, disagreement and empty-model controls. Open-language semantic entailment, independent codec fidelity and prefix production remain open empirical/formal bridges.

## T14. Case-bound certificates preserve types only under an explicit trust contract

Bind a certificate to its actual task/input/candidate/assertion, or explicitly declared risk family, and to the implementation/model/configuration, representation/preprocessing, checker and calibration identities, target, quantifiers, selection policy, resource contract, assumptions, scope and epoch. Include the support interval and risk value in the certificate's own identity. A trusted checker must validate the actual certificate for the actual requested proposition; an arbitrary `PASS` string or well-formed hash is not validation.

**Restricted gate theorem.** The pure gate in `calculus.py` returns ASSERT_EXACT only for an EXACT_TARGET certificate under the exact-target quantifier, live compatible support, matching binding, valid scope/epoch, checker PASS and external assertion authority. It returns RISK_AUTHORIZED without asserting target truth only for an accepted conditional-risk certificate below the requested limit. Missing required checks cannot return either accepted terminal.

**Proof.** Exhaust the gate's branches. Every accepted branch is dominated by the shared checks. The exact branch tests both kind and quantifier; the risk branch returns `asserts_target=False`. Every failed/absent prerequisite returns a distinct refusal, revalidation or CANNOT_CHECK. Given sound validation and faithful target interpretation, exact assertions inherit that conditional soundness. They do not acquire external scientific authority from this proof.

**Boundary.** A trusted callback in a research model is not a production trust root. The machine needs authenticated evidence/checker provenance, immutable payloads, atomic current-version checks, an effect-specific capability and a durable action protocol. A type named PROGRAMMATIC or SEARCH is not a correctness proof for arbitrary output. Formal checker acceptance also does not verify that an informal request was formalized correctly.

Checker: fifteen binding-coordinate mutations; valid exact and risk controls; revoked/contradicted support; expiry; checker absence/failure/untyped return; wrong risk/quantifier and unauthorized operations.

## T15. Realized information gain does not obey blanket subadditivity

For nested nonempty version spaces V0 superset V1 superset ... superset Vk, define g_i=log2(|V_(i-1)|/|V_i|). Then sum g_i=log2(|V0|/|Vk|), by cancellation. No independence assumption is needed.

**Counterexample to separate marginal subadditivity.** Let |H|=4, |A|=|B|=3 and |A intersection B|=2. Joint gain is 1 bit, exceeding 2*log2(4/3). The exact inequality is 3*3 > 4*2. Expected Shannon information, conditional information and realized Hartley cardinality reductions are different objects; their algebraic laws cannot be exchanged. Empty version spaces have no finite information-gain score and must be reported as conflict.

Checker: exact cardinality inequality and multiplicative telescoping in `check_semantics_and_information`. No per-channel sample-complexity theorem is claimed from a scalar information score.

## T16. Conditional end-to-end commitment theorem

Consider the following deliberately restricted machine: finite typed claims and supports; trusted sound certificate checking; explicit external authority; a complete binding/applicability check; serialized current-epoch commitments as in T11; and an immutable risk/work ledger. Every successful effect reservation has a fresh event ID, while exact replay has the identical event payload. Risk exposures satisfy either the predictable premise of T05 with q_t justified before action, or a separately checked fixed-family contract. Every progress step consumes a positive integer work unit.

Then, throughout a run: (i) no risk certificate becomes an exact assertion through the gate; (ii) no certificate made inapplicable by revocation or staleness passes a later serialized commitment; (iii) a risk ledger whose total predictable charge is <= epsilon gives probability <= epsilon of any accepted risk error, plus separately declared validation risk eta; (iv) k completed progress transitions need at least k work units. Unavailable required evidence/checkers produce refusals or CANNOT_CHECK, not accepted claims.

**Proof.** Induct over the serialized commit order. T14 establishes accepted-case typing and applicability; T11 makes those checks current at the commitment point. Immutable event identities make replay and new exposure distinct, preserving budget sums. Apply T05 to the predictable accepted-exposure indicators, and T10 to the positive work charges. No component licenses itself: trusted semantics, probabilistic validity and external permissions remain premises.

This is a conditional composition/refinement result over the declared machine, not a claim that existing OCM code implements it, that its empirical assumptions are true, or that the construction is novel. The strongest parent product—provenance/TMS, typed contracts, selective/sequential risk control and versioned transactions—already supplies its ingredients. Production refinement, useful risk certificates under adaptive distribution shift, formal-specification fidelity and resource-optimal implementation are the next substantive research frontiers.

## Evidence and non-consequences

`RESULTS.json` records the finite calibration; `RECEIPT.json` binds its code, statements, registry and audit surface. `Foundation.lean` contains only the explicitly listed logical bridge lemmas; it is not a mechanization of all sixteen arguments. Missing proof tooling is CANNOT_CHECK, never a pass. No check count substitutes for theorem assumption review. Reproducible self-authored code is not independent replication.

The contribution is a corrected, executable foundation fragment and a sharper set of frontier questions. It grants no complete-science, architecture-superiority, general-language, model-efficiency, quantum, field-recognition or publication claim.
