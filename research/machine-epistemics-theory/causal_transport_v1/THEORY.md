# Causal evidence and lifecycle-safe transport: bounded foundation V1

Task ME-CAUSAL-TRANSPORT-V1; ORION-V2 #315. This is an additive theory study, not an OCM runtime, a new causal calculus, or a field/novelty claim. Written proofs below cover the stated finite mathematical models at arbitrary finite sizes. The Python enumeration is separate implementation calibration, not the proof of those quantified statements. No proof assistant or independent review is claimed.

## 0. Objects, information boundary and ownership

A finite acyclic structural causal model is `M=(U,p,V,D,F)`: a finite **joint** exogenous state U with rational probability p; topologically ordered observed variables V; finite domains D; and complete deterministic tables `v_i=f_i(u,pa_i)`. Exogenous coordinates need not be independent. A surgical intervention `do(A=a)` replaces the corresponding equations, leaving the remaining equations and p fixed **by model assumption**, not by empirical deduction.

Write `v^a(u)` for the resulting world. Three different query types are:

- OBS: `P_M(B | C)` in the natural world;
- DO: `P_M(B | C, do(a))`, with B and C both evaluated in the intervened world;
- CF: `P_M(B_a | C)`, with C evaluated in the factual world and B after intervention, using the **same exogenous u**.

These are inherited SCM/response-function semantics [P1,P2]. Identifiability and transportability are established causal-inference objects [P3]. Every result is parent-owned, an elementary specialization/corollary, or an explicitly scoped implementation contract. Source numbers refer to SOURCES.md. No completeness of the literature search is asserted.

The complete model tables and model family are **declared input descriptions**. Their construction, acquisition, storage, rational bit lengths and evaluation cost are not free. A supplied exact population law is an idealized mathematical constraint, not something a finite run produces automatically. A query interpreter does not certify that its supplied model describes the real world. An internally checked consequence of assumptions is not an externally warranted assertion that the assumptions hold.

## CT-01. Unique surgical semantics and normalized query laws

**Statement.** For every well-formed finite acyclic M, every u and every domain-valid intervention a, there is a unique `v^a(u)`. Summing p over assignments induces a normalized probability law. Conditional OBS/DO/CF probabilities are defined only when the conditioning event has positive probability.

**Proof.** Induct over the topological order. An intervened variable has its specified value. Every other variable has already-determined parents and a total function table, hence one value. This gives existence and uniqueness at each step. The sets of u mapping to possible worlds partition U, so their masses are nonnegative and sum to one. Conditional division requires a nonzero denominator. The CF numerator is `sum_u p(u) 1[C(v(u))] 1[B(v^a(u))]`; the denominator is `sum_u p(u) 1[C(v(u))]`. This also proves the code's factual/intervened evaluation order.

**Calibration.** 64 binary models; all nine surgical assignments to subsets of X,Y; direct table indexing versus generic topological evaluation. Cyclic, incomplete, duplicate and out-of-domain inputs are rejected. **Non-consequence:** this does not handle cyclic equilibrium semantics or establish physical controllability.

## CT-02. Identifiability is constancy on a nonempty compatible model class

Let `H_I` be all models in the declared family satisfying the live evidence/assumption constraints I. For a scalar query q defined on every member, set `Q_I={q(M): M in H_I}`.

**Statement.** q has a unique answer relative to I iff `Q_I` is a singleton. If two compatible models disagree, any deterministic rule receiving only I must fail on at least one of them. `H_I=empty` is a model/evidence conflict, not vacuous truth. If q is undefined on a possible model, this reference returns CANNOT_CHECK rather than silently excluding that model.

**Proof.** Singleton constancy supplies the unique common value. Conversely, a single answer cannot equal two different values. Compatible models supply the same admitted information I, so a deterministic I-only rule returns the same answer for both. Empty compatibility supplies no possible-world witness; the explicit nonempty premise disallows promotion from `all([])`. These are the finite form of the inherited identification criterion [P3]. Randomized nonzero-error rules require a loss criterion; CT-10 treats that separately.

**Important boundary.** A finite grid is a complete universe only if that grid was the registered hypothesis family. Agreement on an arbitrary sample of models cannot prove agreement over every SCM.

## CT-03. Perfect observational agreement does not identify interventions

Let `U~Bernoulli(1/2)` and `X=U`. Model A has `Y=X`; model B has `Y=U`. Both have observational mass 1/2 on 00 and 11, hence `P(Y=1 | X=1)=1` in both. But `P_A(Y=1 | do(X=1))=1` and `P_B(Y=1 | do(X=1))=1/2`.

**Proof.** In A the intervention sets X=1 and the Y equation copies it. In B the intervention does not replace Y's U dependence; half the population remains Y=0. The two models remain observationally indistinguishable even with an exact population law. This is an explicit finite nonidentification witness, not a sample-size or computation failure.

**Disposition.** Classical causal countermodel [P1]; no ORION residual. The machine must not convert an association edge into an intervention edge just because the association is certain.

## CT-04. All observed-variable interventions need not identify a counterfactual

Let T,R be independent fair binary coins and X=T. Model C has `Y=R`; model D has `Y=X xor R`. Both have the same uniform observational law of X,Y. Under every surgical intervention on any subset of the **observed variables X,Y**, their remaining observable laws agree. Yet

`P_C(Y_1=1 | X=0,Y=0)=0`, while `P_D(Y_1=1 | X=0,Y=0)=1`.

**Proof.** Under do(X=x), either R or x xor R is fair. Under do(Y=y), X remains fair; under both interventions the observed assignment is fixed. Factual X=0,Y=0 implies T=0,R=0 in both models. After setting X=1, C keeps Y=0 and D changes to Y=1. Interventional marginals do not determine the cross-world coupling of potential outcomes [P2].

**Boundary.** Intervening on the latent R is not among the permitted interfaces. Nor does this claim that *no* assumptions identify counterfactuals: assumptions restricting response functions can do so.

## CT-05. Sharp binary counterfactual bounds, not merely a loose interval

Suppose exact marginals `p0=P(Y_0=1)` and `p1=P(Y_1=1)` are known, and no restriction on the joint response distribution is imposed. For `p0<1`,

`max(0,p1-p0)/(1-p0) <= P(Y_1=1 | Y_0=0) <= min(p1,1-p0)/(1-p0)`.

Both bounds are attainable. If p0=1, the conditional query is undefined.

**Proof.** Set `t=P(Y_0=0,Y_1=1)`. In response-type order 00,01,10,11, the joint weights must be

`(1-p0-t, t, p0-p1+t, p1-t)`.

They sum to one, and all are nonnegative exactly when `max(0,p1-p0)<=t<=min(p1,1-p0)`. Dividing t by 1-p0 proves the interval. Every admissible t constructs a valid response distribution; the endpoints establish sharpness. Each distribution is realizable as an SCM whose latent state chooses a response type. This is an elementary response-function/Fréchet calculation, not a new bound family [P2].

**Calibration.** Independently enumerate all four-response-type distributions on denominator grids 1 through 8, group by p0,p1, and compare group extrema with the formula. Do not identify these grid cells with independent empirical samples.

## CT-06. Retraction widens identified sets; duplicate evidence does not narrow them

Under conjunctive constraint semantics `H_I = intersection_{i in I} C_i`, deleting a live constraint yields `H_I subseteq H_{I\{i}}`. Whenever both are nonempty and q is defined on both, `Q_I subseteq Q_{I\{i}}`; therefore the lower endpoint cannot increase and the upper cannot decrease. Adding the same constraint twice changes nothing.

**Proof.** Intersection over fewer sets admits at least the previous models. Applying q preserves inclusion, giving the endpoint inequalities. Set intersection is idempotent. A newly undefined query produces CANNOT_CHECK instead of artificial narrowing.

**Operational meaning.** A previously identified causal claim may become partially identified after an identifying experiment or assumption is revoked. A retained source copy cannot count as fresh independent evidence. This is a semantic rule, not a proof of minimal incremental update cost. Alternative-support warrant algebra and dynamic dependency implementation remain owned by the existing foundation lanes.

**Finite sample guard.** Observing one successful event removes only zero-likelihood models in support-only exact inference. It does not establish `P(event)=1`: the two CT-03 models both allow one do(X=1),Y=1 observation. Treating that observation as an exact population law incorrectly removes model B. Confidence-region or Bayesian updates require their separate assumptions and calibration.

## CT-07. Sharp distribution-plus-mechanism transport envelope

Let p,q be probability distributions on the same declared finite latent alphabet. Let K,L be stochastic kernels to a common outcome alphabet, with a fixed registered outcome/estimand correspondence. Define

`epsilon = TV(p,q)`, `eta_u=TV(K(u,.),L(u,.))`, `eta=max_u eta_u`.

Then

`TV(pK,qL) <= epsilon + sum_u min(p_u,q_u) eta_u`

`             <= 1-(1-epsilon)(1-eta) <= min(1,epsilon+eta)`.

For every common loss `0<=ell<=B`, the absolute expectation change is at most B times any valid envelope above.

**Proof.** Couple the latent draws with common diagonal mass `min(p_u,q_u)`; remaining disagreement mass is epsilon. On each equal-u branch, couple the two output rows with mismatch eta_u. On the unmatched branch use any coupling and bound mismatch by one. The probability of output disagreement is at most the first expression, and total variation is at most any coupling mismatch [P4]. Since the common mass sums to 1-epsilon, the second expression follows. For the expectation bound, write positive and negative signed masses separately: a loss in [0,B] changes by at most B times the positive signed mass, which equals TV.

**Sharpness of the uniform envelope.** Use three latent states, `p=(1-epsilon,epsilon,0)` and `q=(1-epsilon,0,epsilon)`. On the common state take `K=(1-eta,eta,0)` and `L=(1-eta,0,eta)`. On private states both kernels output their corresponding distinct symbols. The resulting laws share exactly `(1-epsilon)(1-eta)` mass and have disjoint residuals. Equality holds. The bound is sharp given only epsilon and eta, not necessarily for every fixed pair of fully known kernels.

**Why this belongs in the foundation.** Identical mechanism names do not imply p=q. Identical populations do not imply K=L. Either missing assumption can permit target error one despite source error zero. Structural causal transportability has stronger graphical parents [P3]; this envelope is a bounded perturbation rule, not a replacement for do-calculus.

**No hidden empirical promotion.** Knowing/estimating epsilon or eta is a separate scientific obligation. A finite calibration run cannot simply assert these as deterministic bounds. Interventions, policies, measurement semantics and populations are part of the binding.

## CT-08. Conditioning can amplify a small drift sharply

For finite laws P,Q and a common event A with masses `a=P(A)>0`, `b=Q(A)>0`,

`TV(P(.|A),Q(.|A)) <= min(1, TV(P,Q)/max(a,b))`.

**Proof.** Suppose a>=b. Write conditional masses r_i=P_i/a and s_i=Q_i/b on A. On the subset where r_i>s_i, `P_i-Q_i=a*r_i-b*s_i >= a*(r_i-s_i)`. Summing and bounding by the full positive signed mass gives `TV(P,Q)>=a*TV(r,s)`. Exchange P,Q for b>=a.

**Sharpness.** `P=(kappa,0,1-kappa)` and `Q=(0,kappa,1-kappa)`, conditioned on the first two states, have TV=kappa before conditioning and TV=1 afterward. Mixing some common mass within A supplies intermediate sharp cases. A zero denominator remains CANNOT_CHECK.

**Critical type restriction.** P,Q must be the laws of the **relevant joint object**. Equality of CT-04's interventional marginals cannot be fed into this theorem as equality of counterfactual joint laws. The theorem preserves neither causal semantics nor cross-world coupling by magic.

## CT-09. Lifecycle-aware conditional transport certificate (corollary)

Let the output alphabet in CT-07 encode the joint `(conditioning context, target outcome)` required by the claim. Suppose a proof-bound deterministic Delta bounds the joint-law TV change, both conditioning masses are positive, and their maximum is at least a declared kappa>0. Then every common [0,B] conditional loss satisfies

`|R_target(A)-R_source(A)| <= B*min(1,Delta/kappa)`.

In particular, a valid source conditional risk bound r licenses only the target **risk statement** `R_target(A)<=min(B,r+B*min(1,Delta/kappa))`, not individual output truth and not permission to act.

**Proof.** Apply CT-08 and then the bounded-loss part of CT-07. Both-masses-at-least-kappa is a stronger convenient sufficient premise. If a bound/assumption/evidence dependency is revoked, recompute or withdraw this certificate; do not retain its endpoint merely because the source result is unchanged.

**Proved mathematical scope, open empirical bridge.** This is an elementary composition of two parent bounds. Obtaining calibrated drift certificates under adaptive nonstationarity, and proving a useful cost advantage for their maintenance, remain research targets. No statistical confidence level is implicitly converted into a deterministic Delta.

## CT-10. Adaptive experiments: a transcript distinguishability and abstention limit

Consider two possible environments, one common adaptive (possibly randomized) policy, a fixed finite horizon T, and common history/action/observation alphabets. For each step t and every common history/action, suppose the two conditional observation kernels differ by at most epsilon_t in TV. Histories may summarize changing hidden state; these conditional kernels must already account for that state. Then

`TV(P_transcript,Q_transcript) <= D_T := 1-product_t(1-epsilon_t)`.

**Proof.** Couple policy randomness identically as long as histories match. At step t on a matched history the action agrees, and maximal coupling of the observation rows disagrees with probability at most epsilon_t. Inductively, entire-history agreement has probability at least `product_t(1-epsilon_t)`. No independence of the actual observations is required: the bound is conditional at every matched history. Total variation is bounded by coupling disagreement [P4].

For an equal-prior test between these two environments, let e be average wrong-answer probability and a be average abstention probability. Then

`2e+a >= 1-TV(P_transcript,Q_transcript) >= 1-D_T`.

**Proof.** At each transcript, denote its masses p,q. A decision for environment 1 incurs p in the sum of the two error probabilities; a decision for 0 incurs q; abstaining incurs `(p+q)/2` when abstention is charged half as much as error. Each is at least min(p,q). Sum over transcripts, using `sum min=1-TV`, and normalize by the equal priors. Randomized decisions are convex combinations. With no abstention this is the two-point testing bound; always abstaining has e=0 and a=1 and is not a counterexample. General interactive lower bounds have substantially stronger parents [P5].

**Sharpness.** At each round let both environments output a common no-information symbol with probability 1-epsilon, and otherwise different identifying symbols. The first informative symbol distinguishes them. The transcript TV is exactly `1-(1-epsilon)^T`; the remaining common mass attains the error/abstention line. Uniform kernel bounds, common policy and fixed horizon are load-bearing. Different policies can make transcripts disjoint even with identical channels. Unbounded optional stopping needs a separate theorem or a valid bounded padding construction.

## CT-11. Evidence rollback cannot in general undo a physical intervention

Represent the external world and epistemic state separately as `(w,e)`. An intervention changes w through f. Revoking its receipt changes e; it has no defined inverse action on w. A state-only inverse g satisfying `g(f(w))=w` for all admitted w exists only if f is injective.

**Proof.** If f(w1)=f(w2) with w1!=w2, applying one g to that image cannot yield both originals. The witness `f(0)=f(1)=1` defeats every possible binary state-only inverse. Erasing an event record does not execute a compensating physical operation.

**Boundary.** A richer system can retain old state and sometimes perform an authorized compensation; that is additional information, mechanism and authority. It does not invalidate the noninjective state-only result. The reference runs no real external action. Pre-action authorization, actual-effect receipts and compensation feasibility must remain separate in OCM.

## CT-12. Syntactic identity is a necessary custody check, not proof of semantics

A causal certificate must bind at least: query kind and event; intervention and factual-conditioning interpretation; model-family identity; complete relevant table/model/configuration identity; population and measurement mapping; policy/horizon; evidence and assumption dependencies; estimation versus exact-law status; checker/toolchain; scope/epoch; resource model; and external action authorization when applicable.

This package's model digest covers the complete finite equations, domains and joint prior. Its query digest includes OBS/DO/CF and canonical assignments. A changed declared dependency returns REVALIDATE; missing dependency returns CANNOT_CHECK. Unchanged undeclared display metadata is not a scientific change **provided the dependency declaration is complete**.

**Contract, not a theorem of trust.** Matching hashes only establishes identity under the chosen encoding/hash assumptions. It proves neither authentic origin, complete dependencies, model truth, intervention feasibility, checker correctness nor external authority. A changed digest need not mean the science is false: an explicit verified equivalence/transport witness may justify reuse. There is no automatic such witness in this package.

## CT-13. Pairwise transport certificates need not admit one global realization

Let X be uniform on {0,1}, Y uniform on {0,2}, and Z uniform on {1,2}. Each pair has TV distance 1/2 and separately admits a coupling with disagreement probability 1/2. No one joint law can attain these three optimal pairwise couplings at once.

**Proof.** Every possible triple contains at least two unequal pairs (no value occurs in all three supports). Therefore the sum of pairwise disagreement probabilities is at least 2 for any joint law. Three claims of disagreement 1/2 would sum to 3/2, a contradiction. This is the parent witness in [P4], explicitly retained as parent-owned.

More generally, on declared finite domains, joint compatibility of proposed marginal certificates is exactly feasibility of nonnegative joint weights with total one and the stated marginal-sum equalities. This follows in both directions from the definition of a joint law. `verify_joint_marginals` checks a supplied primal witness; rejecting one proposed witness **does not prove infeasibility**. The three-variable pointwise inequality above is a separate impossibility witness. A general LP/dual-certificate solver is not included.

**Foundation consequence.** Separate domain comparisons cannot be silently treated as one coherent multi-domain/counterfactual universe. Global compatibility is an additional obligation when a downstream claim requires a shared joint model. Pairwise bounds alone remain valid at their original scope. This does not undermine CT-10, which couples just two entire processes sequentially rather than demanding simultaneously optimal couplings of many processes.

## 14. Resource and incompleteness accounting

For n variables and L latent states, table storage is proportional to `sum_i L*product_{j in pa_i}|D_j|` entries. A query scans all L states and evaluates the finite equations. The implementation uses tuple domain indexing, so parent-domain search cost is additional; rational arithmetic is exact, not constant-cost arithmetic. Finite-class identification also scans the supplied |H| models. Finding/encoding H and validating its adequacy are outside this evaluator, not free services.

A kernel transport certificate requires comparing the declared rows and populations; direct mixtures cost O(|U|*|Y|) rational operations. Exact full transcript enumeration is exponential in horizon, with explicit runtime reference caps at T=8 and 65,536 histories. There is no scalability or advantage claim. Hand-written proofs do not depend on those implementation caps. A supplied global marginal witness can itself have exponentially many entries.

Not completed here: general graphical identification/transport algorithms, noisy causal discovery, nonparametric continuous models, time-uniform statistical drift estimation, human/native validation of interventions and measurements, real-world action safety, minimal incremental causal-repair complexity, architecture advantage, independent proof reconstruction, or all-foundation closure. FRONTIER.md gives precise successor questions and non-overlapping ownership.
