# Certificate transport and exact revalidation frontiers

**Study:** ME-CERTIFICATE-TRANSPORT-V1. **Disposition:** a scoped, parent-owned mathematical foundation fragment, with written proofs and exact finite calibration. Not a new-field, architecture, empirical-coverage, independent-review, or OCM-adoption claim.

The primary specification was committed as `a0c10be58bf280867f790dc8aafa9a98de743cfe` before its calibration. `ADDENDUM.md`, commit `798ac9a06174731ff207e8f4e3e90547c38dd434`, records the subsequently derived subset-sum reduction and audit-complementarity question before their supplementary calibration. Nothing here rewrites a protected outcome or the gap atlas at ORION-V2 `24566f00a9dc4425a438fcfac05d13c6b2d903db`.

## 0. Scientific object and assumptions

A **risk statement** concerns the probability of a specified failure event. It is not a proof of an individual proposition, nor permission to perform an external action. This fragment supplies the transport calculation between risk statements; the separate typed-warrant foundation owns the larger admission calculus (#313).

Let `X={0,...,n-1}` be a finite, explicitly registered universe. Let `P` be a complete probability distribution on X, F a reference failure event, U the set where a changed operator may alter failure status, and epsilon, eta in [0,1]. All of these are model inputs. Define

\[
 \operatorname{TV}(P,Q)=\frac12\sum_{x\in X}|P(x)-Q(x)|.
\]

The allowed deployment class is

\[
 \mathcal C=\{(Q,G):\operatorname{TV}(P,Q)\le\epsilon,
       F\triangle G\subseteq U,\ P(F\triangle G)\le\eta\}.
\]

G ranges over **all binary events satisfying these restrictions**. If only some events are realizable by a particular backend, this class is a relaxation: the result remains an upper bound but attainment by that backend is not established. Q may place mass on reference-zero atoms; there is no absolute-continuity restriction. A stochastic operator can be modeled only after its randomness is included in X with the appropriate joint distribution. Unknown, continuous, unenumerated, drifting-label, and noisy-observation models are not silently reduced to this finite object.

Theorems below hold for every finite n and real probabilities under these assumptions. The implementation accepts rational probabilities and caps n at 12. Finite runs check the implementation; the written arguments, not those runs, support the general finite-n statements. No proof-assistant verification has been performed.

**Acquisition boundary.** A sample frequency is not P. A test result is not a complete error table. Neither a registry nor this optimizer establishes U, epsilon, eta, the validity of a checker, or the equivalence of two task specifications. Obtaining, storing, checking, and maintaining these inputs must be separately charged and warranted. Missing premises mean `CANNOT_CHECK` for a deployment claim, even when the conditional calculation is exact.

## CT-01. Typed subject binding is not validity

The reference manifest has 14 mandatory nonempty identity fields: schema, task specification, claim kind, output predicate, domain, operator artifact/configuration, checker artifact, calibration data, assumptions, query policy, resource policy, environment, and epoch. Canonical JSON is hashed. Changed or revoked dependencies return `REVALIDATE`; absent bindings return `CANNOT_CHECK`; non-risk claim kinds return `WRONG_CLAIM_KIND`. The most favorable result is **`BINDING_MATCH_ONLY`**.

**Proposition.** For this interface, a successful binding check cannot itself output a truth warrant, a valid statistical premise, or an action authorization.

**Argument.** Inspect the finite return vocabulary of `binding_status`. None denotes those conclusions; they require separately typed evidence and a separate pre-action authorization. An identity string is not an authenticated attestation, and a cryptographic binding does not establish the proposition bound to it. Equal hashes imply only equality of the serialized manifest subject to the hash assumption; the implementation does not independently attest execution bytes. Unequal hashes do not prove semantic inequivalence: a replacement can be admitted through a separately justified transport/equivalence record, not silent reuse.

The required fields are a scoped V1 schema, not a proof that 14 fields exhaust every possible environment. Additional material factors require a successor schema. Parent: typed subject/predicate attestations [S3]. Relation to atlas: MEG-02, MEG-03, MEG-04, MEG-29. **OCM runtime repair is not performed by this study.**

## CT-02. Sharp risk for a fixed event

Define H(P,G,epsilon)=sup Q(G) over the TV ball. Then

\[
 H(P,G,\epsilon)=
 \begin{cases}
  0,&G=\varnothing,\\
  \min\{1,P(G)+\epsilon\},&G\ne\varnothing.
 \end{cases}
\]

**Proof.** The positive and negative parts of Q-P have equal mass TV(P,Q). Consequently Q(G)-P(G)<=TV(P,Q)<=epsilon; probability is also at most one. For nonempty G choose a receiving atom in G and move t=min(epsilon,1-P(G)) mass from its complement to that atom. There is exactly 1-P(G) available mass outside G. The resulting distribution is nonnegative, sums to one, has TV=t, and assigns P(G)+t to G. For G=X, t=0. For empty G every probability is zero. This proves upper bound and attainment. QED.

**Boundary witness.** P=(1,0), G={1}, epsilon=1/4 has exact risk 1/4 attained at Q=(3/4,1/4), despite P(G)=0. G=empty instead has risk zero. Zero probability and impossibility are different facts.

Parent: total-variation robust expectation; a binary-loss specialization of finite-alphabet extremum theory [S1]. That source uses the L1 convention with radius in [0,2]; its radius R corresponds to 2 epsilon here. The above proof is self-contained.

## CT-03. Joint operator/distribution change, and CT-03b subset-sum reduction

The exact conditional risk frontier is

\[
 \Phi(P,F,U,\epsilon,\eta)=
 \max_{D\subseteq U:\,P(D)\le\eta} H(P,F\triangle D,\epsilon).
\]

**Proof.** Every admissible G corresponds bijectively to D=F symmetric_difference G. For fixed D, CT-02 gives the exact maximum over Q and constructs an attaining Q. A finite maximum over admissible D therefore gives an attainable global maximum. Empty D is always feasible. QED.

A convenient conservative bound is min(1,P(F)+eta+epsilon), because P(G)<=P(F)+P(F symmetric_difference G). It is **not generally the exact frontier**: with P=(2/5,3/5), F=empty, U=X, epsilon=0 and eta=1/2, the exact answer is 2/5, not 1/2. Finite atoms cannot be split to saturate a fractional budget.

**Sharper form.** Let S=U minus F, and

\[
 K=\max\{P(I):I\subseteq S,\ P(I)\le\eta\}.
\]

Let b mean that F is nonempty or some x in S has P(x)<=eta. Then

\[
 \Phi=\begin{cases}0,&\neg b,\\
                    \min(1,P(F)+K+\epsilon),&b.
       \end{cases}
\]

**Proof.** For any D, replace its proposed event by F union (D minus F). This only adds failures back, remains admissible, and weakly reduces change mass. Worst-case risk is monotone in the failure event. Hence removing old failures is dominated and only I subset S need be considered. If K>0, an attaining I is nonempty. If K=0 and b is true, either F is nonempty or an admissible zero-mass singleton supplies the nonempty event needed by CT-02. If b is false, no nonempty event is feasible. QED.

`extensions.subset_sum_frontier` is an ordinary reachable-mass subset-sum dynamic program, preserving a nonempty representative on equal zero-mass states. It is a faithful parent, not an OCM-specific optimizer [S4].

**Grid completeness for the registered calibration.** If every P(x), epsilon and eta is an integer multiple of 1/d, the mass-transfer construction above can be performed with multiples of 1/d. Thus at least one optimum lies on the enumerated Q simplex. The independent-formulation oracle enumerating all such Q is exact for these test inputs. This argument does not extrapolate a three-atom experiment to all n.

## CT-04. Exact pointwise no-change audits

Now omit the eta bound, and suppose exact audits on A subset U establish G(x)=F(x) for every x in A. Outside U the same equality is already part of the model. The coordinatewise largest compatible event is

\[
 G_A=F\cup(U\setminus A),\qquad R(A)=H(P,G_A,\epsilon).
\]

**Proof.** Every event agreeing on A and outside U is contained in G_A. G_A itself agrees in both regions. Event monotonicity and CT-02 give the exact upper bound, and its attaining Q is a witness. An adversary choosing G_A is indistinguishable from the unchanged operator on the audited atoms. No sound bound using only this transcript and this model class can be smaller. QED.

This is a theorem about a **realized no-change transcript**, not a policy guarantee over arbitrary audit results. A changed label needs a new observation record and model. Audits are exact pointwise observations, not sampled Bernoulli evidence with an unmodeled error rate. The optimizer's access to P and F is an explicit public-model assumption.

## CT-05. Audit cost/risk frontier and the strongest parent

Give each atom a positive integer audit cost c_x and a nonnegative integer budget B. Define

\[
 R_B=\min_{A\subseteq U:\,\sum_{x\in A}c_x\le B} R(A).
\]

Auditing points of F cannot remove them from G_A and cannot improve the risk on a no-change transcript. An optimum therefore exists with A subset S=U minus F. Except at the empty-event boundary, minimizing R(A) is equivalent to maximizing covered mass P(A), subject to the cap at risk one. This is 0/1 knapsack [S4].

**Dynamic-programming sufficiency.** After each item, for each exact spend retain a subset with greatest covered mass; among equal masses retain greatest cardinality. A discarded lower-mass subset cannot beat the retained subset after adding any common future suffix, because H is monotone in residual mass. At a zero-mass tie, greatest cardinality preserves the one exceptional possibility: all potentially changed atoms have been audited, so the failure event is empty. A full audit has maximum attainable covered mass and cardinality and cannot be discarded. Compare all final spend states by risk and then actual cost; this avoids spending extra when the risk-one cap makes improvements ineffective. This proves the implemented DP's risk and minimum-cost objective agrees with exhaustive search. Equal-quality audit masks need not be unique. QED.

**Hardness reduction.** Given a 0/1-knapsack instance with positive integer values v_i and costs c_i, introduce one fixed failure atom of mass 1/(1+sum v_i), and mutable good atoms of mass v_i/(1+sum v_i). Set epsilon=0. An audit set A has risk 1-sum_{i in A}v_i/(1+sum v_i). Minimizing this risk under budget B solves the original knapsack instance. Thus the general budgeted audit problem inherits knapsack hardness; a pseudo-polynomial DP is not polynomial in binary-encoded B.

**Resources.** Full enumeration uses O(n 2^|U|) rational arithmetic operations and a full input error table. The present DP recomputes masses, giving an O(n^2 B) arithmetic upper bound and at most B+1 retained masks of n bits; an implementation caching values can recover the textbook O(nB) recurrence. The reachable-mass DP has at most min(2^|S|,d+1) states when masses have denominator d, and may be exponential without a bounded denominator. Exact rational bit costs depend on input precision and are not constant. Reported transition counters are not all machine instructions. The implementation explicitly refuses n>12 and DP budgets>100,000. No practical large-model efficiency claim follows.

## CT-06. Monotonicity, revocation, and selective revalidation

**Proposition.** Enlarging U, epsilon, or eta cannot reduce Phi. If A' subset A, then R(A')>=R(A), and R_B is nonincreasing in B. Unrelated changes leaving the declared model and applicable audit set unchanged leave the calculation unchanged.

**Proof.** Each first change enlarges a feasible set in a maximization. Audit revocation enlarges the compatible-event class; raising B enlarges a feasible set in a minimization. The last conclusion is functional identity. QED.

Consequently a decision previously justified by R(A)<=r may need revalidation when an audit is revoked. It does **not** follow that every dependent decision must change or every claim becomes false: the new bound may still be below r. Numeric sufficiency, evidence validity, task scope, and action authority remain separate coordinates. This is the certificate-level instance of dependency-aware reopening, not a replacement for the foundation's general reopening theory.

## CT-07. Sequential transport and verifier error

Suppose a common universe and a common semantic failure target justify a chain (P_j,F_j), with TV(P_j,P_{j+1})<=epsilon_j and P_j(F_j symmetric_difference F_{j+1})<=eta_j. Then

\[
 P_k(F_k)\le\min\left(1,P_0(F_0)+\sum_{j<k}(\epsilon_j+\eta_j)\right).
\]

**Proof.** P_{j+1}(F_{j+1})<=P_j(F_{j+1})+epsilon_j<=P_j(F_j)+eta_j+epsilon_j. Induct and cap at one. QED. This is a safe composition bound, not a claim of joint sharpness.

If F measures checker-reported failure but H is the actual target violation, a separately warranted missed-violation bound Q(H minus F)<=nu yields Q(H)<=Q(F)+nu. This follows by splitting H into its intersection with F and its complement. Without such a relation, checker coverage is not target correctness. Changing the task or predicate requires an explicit common semantics/correspondence, not merely a new epsilon.

For adaptive selection, the premises must hold for the selected law/event (for example uniformly or conditionally on relevant history). A marginal guarantee for a preselected procedure does not supply that fact. Conformal drift analysis is an important nearest parent [S2], but its exchangeability/swap/weight assumptions are not automatically satisfied by this OCM interface.

## CT-08. Necessary non-consequences and refuted shortcuts

A population failure rate 1/20 is consistent with failure rate one on the failing twentieth of the population. Selecting exactly that subgroup changes the relevant distribution. Even a valid marginal certificate does not make each output an exact fact.

The executable controls reject omitting distribution drift, operator changes, mutable scope, the factor one-half in TV, finite atom granularity, the empty-event exception, zero-mass support, unaudited regions, revoked audits, and dependency revocation. Fourteen independently changed manifest fields force revalidation or a typed rejection. No-alarm controls preserve identity transport, irrelevant revocation and canonical ordering.

These are explicit countermodels and specification corrections. They are not vulnerability exploitation, new probability theory, or evidence that OCM currently has a repaired runtime. Missing evidence must not be manufactured to make a bound applicable.

## CT-09. Audit benefits can be complementary, not diminishing

For A subset S=U minus F define g(A)=R(empty)-R(A). Under the CT-04 model, g is monotone **supermodular**:

\[
 g(A)+g(B)\le g(A\cup B)+g(A\cap B).
\]

It is not generally submodular. Put t=P(F union U), c=t+epsilon-1 and h(z)=max(0,z-c). If F is nonempty,

\[
 g(A)=h(P(A))-h(0).
\]

If F is empty and U is nonempty, add epsilon times the indicator of A=U to that expression. For F=U=empty, g is identically zero.

**Proof.** The displayed expressions follow by substituting CT-02 into CT-04; the additional term removes the spurious epsilon when the event becomes empty. For nonnegative weights, the increment h(z+w)-h(z) is nondecreasing in z because h is convex. Therefore h of covered mass has increasing set marginal returns, equivalently supermodularity. The indicator that all elements of U have been selected is also supermodular: its marginal is one only when the added element completes U. Nonnegative sums and constants preserve the inequality. Monotonicity follows from CT-06. QED.

**Strict counterexample.** For P=(1/2,1/2), F=empty, U=X and epsilon=1/2, the risks for no audit, either singleton audit, and both audits are 1, 1, 1, 0. Neither single audit helps immediately, but the pair eliminates the failure event. A stop-on-zero-single-step-benefit heuristic can therefore stop too early. This does not refute every greedy algorithm, nor does it refute submodularity theorems under other observation models. Parent: convex/concave transforms of modular set functions [S5]; the proof here states the exact specialization and boundary term.

## 10. Evidence, parent subtraction and remaining frontier

`RESULTS.json` contains 10,240 joint-frontier cells checked by a separately formulated finite-simplex oracle, 8,640 audit-semantic cells, and 28,160 exhaustive-vs-knapsack comparisons. `EXTENSION_RESULTS.json` contains 10,240 subset-sum-vs-exhaustive comparisons, 13,720 supermodular inequalities and 8,640 nested audit monotonicity checks. Counts are generated by executed loops. Both formulations were authored in one session: **not independent researcher replication**.

The exact optimizers agree with the faithful parents. CT-02 is classical TV theory; CT-03b and CT-05 use subset-sum/knapsack; CT-06/07 are elementary monotonicity/union arguments; CT-09 is a convex-over-modular specialization. The scientific contribution here is an explicit, tested contract for which certificate can support which later risk statement, including its failure cases. Priority/novelty saturation was not completed and no novel-theorem claim is made.

Open and materially distinct research targets: certified P/U/drift estimation from finite dependent data; noisy/adaptive audits; realizable operator-family constraints; continuous domains; multi-stage changes of semantic target; artifact-to-actual-execution attestation; and end-to-end OCM integration. Each requires additional assumptions, proof/checker and a strongest-parent comparison. The existing foundation and decision-frontier lanes remain their owners; this study does not close them.
