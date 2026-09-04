# Causal evidence, counterfactual revision, and dependent-verifier limits

Identity: **ME-CAUSAL-VERIFIER-V1**. Owner: ORION-V2 #316. Base: `24566f00a9dc4425a438fcfac05d13c6b2d903db` (#310). This is an additive, parent-owned formal foundation companion to #312/#313 and #314, not an OCM implementation or a replacement of their work. Written arguments below establish scoped mathematical statements; exhaustive execution calibrates this implementation. Neither is independent review. No new-field, novelty, architecture-superiority, or full-foundation-closure claim is made.

## 1. The object and the three graphs

A causal model describes mechanisms in a world. A warrant graph describes why a record or claim is licensed. A statistical dependence specification describes a joint law of random quantities, such as verifier errors. An edge in one graph does not supply an edge or an independence assumption in another. In particular, two distinct source identities can share a mechanism of error; two alternative logical proofs need not be statistically independent; a derivation arrow is not an intervention arrow.

The executable family is explicit and deliberately small. Let U be uniform on {0,1}, X=f(U), and Y=g(X,U), where f and g are arbitrary Boolean tables. There are 4 choices for f and 16 for g, giving 64 syntactic models. A surgical intervention replaces an equation: under do(X=x), X=x while Y=g(x,U); it does not condition the old observational law on X=x. All nine combinations of leaving X/Y untouched or setting either to 0/1 are admitted.

The response vector is R=(X_natural,Y_0,Y_1), where Y_x=g(x,U). All coordinates use the SAME exogenous realization. Its law is a probability vector on eight responses. The registered numerical queries are P(Y_0=1), P(Y_1=1), P(Y_0=Y_1), and P(X_natural=1), tested against 0, 1/2, and 1. Broader statements below concern arbitrary finite families and registered Boolean claims, not arbitrary real-world causal systems.

### Epistemic state

For a nonempty registered family H and a finite active evidence set S, each typed record e supplies an admissibility predicate E_e on H. Define H_S={M in H: every e in S admits M}. For a Boolean claim c:

- SUPPORTED: H_S is nonempty and every M in H_S satisfies c.
- REFUTED: H_S is nonempty and every M in H_S satisfies not-c.
- UNKNOWN: some surviving model satisfies c and some does not.
- INCONSISTENT: H_S is empty.

CANNOT_CHECK is separate: the requested query, scope, model-family registration, or required semantic interface is unavailable. It is not an additional truth value. No numerical score appears in this calculus. SUPPORTED means entailed relative to the named model/evidence assumptions, not unconditional world truth, action authority, or statistical confidence.

### Evidence types

EXACT_DISTRIBUTION supplies an entire registered observational/interventional law. OBSERVED_EVENT supplies one occurrence: on this finite probability model it rules out laws assigning that event probability zero, not every law assigning probability less than one. RESPONSE_LAW supplies the full cross-world response law. The latter is a strong mathematical certificate/oracle, explicitly NOT something inferred from ordinary observational samples or unpaired experiments. These types are different information interfaces. A hash or registration records identity, not truth or calibration.

## 2. CV-T01 — conditional soundness and non-vacuity

**Statement (all finite H).** Suppose the actual model M* belongs to H, every admitted evidence predicate admits M*, and the claim evaluator implements c correctly. Then SUPPORTED implies c(M*), REFUTED implies not-c(M*), and H_S cannot be empty. With any premise missing, the respective guarantee is not supplied.

**Proof.** Each evidence premise places M* in E_e, hence M* lies in their intersection with H. Universal quantification over that nonempty set includes M*. If the intersection is empty, there is no included actual model to which the argument applies. Returning SUPPORTED from `all([])` would remove the premise that makes the inference sound. QED.

**Falsifiers.** Two conflicting exact laws yield INCONSISTENT. An inaccurate but properly registered intervention law can exclude M* and make a wrong claim SUPPORTED. Excluding M* from H creates the same problem without any software error. Thus the theorem does not verify model-class coverage, measurement fidelity, or checker correctness. Parent relation: ordinary model-based entailment and partially identified causal inference [S1,S2]. The 2026 ternary-testing parent studies statistical consistency beyond this exact finite fragment; those statistical guarantees are not imported here.

## 3. CV-T02 — observational equivalence does not identify effects

**Witness.** In M_A, X=U and Y=X. In M_B, X=U and Y=U. Both produce (X,Y)=(0,0) or (1,1), each with probability 1/2. Yet P_A(Y=1 | do(X=1))=1 and P_B(Y=1 | do(X=1))=1/2.

**Proof of impossibility.** Any deterministic evaluator receiving only the common observational law has the same input in both worlds and must give the same answer. No such answer can identify both unequal effects. A randomized evaluator has the same output distribution in both worlds and likewise cannot be almost surely correct in both. This is an access-relative impossibility, not a statement that every causal problem is unidentifiable. Exact model/graph assumptions or intervention data can distinguish these worlds. Parent: structural causal models and the causal hierarchy [S1].

The executable OBSERVED_EVENT control retains 28 models after seeing (1,1); the exact observational law of M_A retains 8. Those are different inputs with different information. Neither identifies the effect as 1 in this family.

## 4. CV-T03 — all single-world interventions still need not identify counterfactuals

**Witness.** Let X=0 in both models. In M_C, Y_0=U and Y_1=U. In M_D, Y_0=U and Y_1=1-U. Observational laws and all nine single-world intervention laws agree: each unforced Y is a fair bit, while forced variables have their specified value. But P_C(Y_0=Y_1)=1 and P_D(Y_0=Y_1)=0.

**Proof.** Every allowed single-world intervention accesses at most one of Y_0,Y_1 in a realization. Both marginals are fair in both models. Their joint coupling is respectively identical and opposite. The same indistinguishable-input argument as CV-T02 proves failure of cross-world identification from these laws alone. QED.

This is a full-law statement: infinitely many observations of the same registered single-world experiments would not identify the missing cross-world coupling without additional assumptions. It does not exclude sequential/unit-level designs whose justified semantics supply stronger joint information; such designs would be a different evidence channel. Parent: counterfactual identifiability [S1,S5]. The explicit Boolean witness is an independently written calibration, not a claim to invent the hierarchy.

## 5. CV-T04 — response-law sufficiency and the exact finite information gap

**Statement.** For this family, equality of response laws is equivalent to equality of expectations of every function of (X_natural,Y_0,Y_1). It implies equality of every registered interventional law. Conditionals determined by this response vector are also equal when their conditioning event has positive probability.

**Proof.** A response law evaluates every such expectation by a finite weighted sum. Conversely, indicators of each individual response recover all eight masses. A single-world interventional output is a deterministic function of the response vector: choose natural or forced X, then its corresponding potential Y unless Y is forced. Push the response law through this function. Equal joint laws have equal pushforwards. For conditionals divide equal joint event probabilities by the same positive denominator. QED.

**Exact counts, with a combinatorial proof rather than an enumeration-only claim.** A syntactic model assigns one of eight responses to each of two labeled U values: 8^2=64 possibilities. Forgetting the U labels leaves an unordered pair with repetition, hence C(9,2)=36 response laws. Observed pairs take four values, giving C(5,2)=10 observational laws, all realizable.

There are 34 interventional classes. When natural X is nonconstant, each X value identifies one U realization; the observational law supplies Y_0 on the X=0 realization and Y_1 on the X=1 realization, and the two intervention marginals recover the two remaining values. When X is constant, the data retain only the separate marginals of Y_0 and Y_1. These determine their joint response law except when both are fair bits: the correlated and anticorrelated pair are indistinguishable. This occurs once for X=0 and once for X=1. Thus exactly two pairs collapse: 36-2=34. The interventional-to-response fiber histogram is 32 singletons and 2 doubletons.

**Resource corollary.** Given the interventional class, a worst-case exact response-class disambiguator needs and suffices to receive one binary choice on either doubleton, zero on a singleton. Necessity follows from two possible answers to the equality query; sufficiency names which response law. This is an elementary interface-information bound, not OCM-specific efficiency or a free way to obtain that choice. Obtaining, authenticating, storing, and later revoking a joint certificate remains charged work.

Two implementation paths calibrate the pushforward theorem on 64 x 9 = 576 model/intervention pairs: direct structural equation execution and response-vector integration. They are different algorithms written by the same session, not independent-author replication.

## 6. CV-T05 — exact evidence-revocation semantics for causal claims

**Assumptions.** Fix finite H, a consistent full record set S (H_S nonempty), fixed evidence meanings, and a fixed claim c. For positive warrant define P_c as the inclusion-minimal subsets J of S with H_J entailing c. For negative warrant define N_c similarly for not-c. An empty minimal subset is legitimate when H alone entails the claim. All subsets of S remain consistent because they contain H_S in their surviving model set.

**Statement.** For any revoked R subset S, H_(S\R) entails c iff some J in P_c avoids R. The identical statement holds for not-c using N_c. Therefore exact retraction preserves an alternative surviving justification and reopens the claim precisely when no positive or negative justification remains. It does not treat lost positive warrant as a refutation.

**Proof.** If a sufficient J avoids R, then J subset S\R. Adding valid constraints narrows the surviving set and preserves entailment, so H_(S\R) entails c. Conversely, if S\R entails c, repeatedly remove dispensable records until an inclusion-minimal sufficient J remains; finiteness guarantees this process stops. J avoids R and is also minimal among subsets of S. Apply the argument to not-c. QED.

**Why consistency matters.** With contradictory S, non-vacuous entailment is not monotone in added records: a previously supported claim may become INCONSISTENT. A monotone antichain profile cannot silently encode this extra behavior. The implementation refuses compilation on inconsistent S; contradiction/repair semantics belong to the companion typed-warrant lane. Parent: minimal supports/ATMS and provenance [S3,S4]; this is their finite causal-query instantiation, not a new provenance algebra.

**Concrete lifecycle.** M_C's observation, do(X=0), and do(X=1) laws support P(Y_1=1)=1/2 but leave P(Y_0=Y_1)=1 UNKNOWN. Adding its joint-response certificate supports the counterfactual claim. Revoking that certificate restores UNKNOWN while retaining the intervention effect. Reinstating the exact certificate restores its support. The executable `revision_trace` records the four phases; it is not a persistence or external-action receipt.

**Calibration.** For all 64 models, all 16 subsets of four typed law certificates, and 12 query-value propositions, two family evaluators agree on 12,288 classifications. Positive and negative profiles match direct recomputation in 24,576 checks; 768 reverse-order reinstatements agree. The bitset and list family evaluators share the evidence predicate implementation; their agreement is not independent verification of that shared code.

## 7. CV-T06 — sharp dependence-robust joint bounds

Let A and B be binary events on a single registered population, with certified exact marginal probabilities p and q. Write t=P(A and B). Their entire joint law, in order 00,01,10,11, is

`(1-p-q+t, q-t, p-t, t)`.

**Statement.** A joint law exists iff max(0,p+q-1) <= t <= min(p,q). Every t in this interval is realizable. For any Boolean event h on the four cells, its sharp probability bounds are the minimum and maximum of its expectation at the two endpoint tables.

**Proof.** Nonnegative probabilities imply each inequality. Conversely the four listed cells are nonnegative and sum to one for every feasible t, giving a realizing probability space. E[h] is affine in t, hence its extrema on the closed interval occur at endpoints. QED. Parent: elementary Frechet-Hoeffding bounds/coupling optimization [S6]; neither optimal transport nor probability coupling is an ORION invention.

**Verifier specialization.** If A and B denote false acceptance of the same false proposition and each has error probability 1/20 under the SAME registered selection/population, requiring both to accept has joint-error bound [0,1/20]. The independent value 1/400 is one feasible point, not the general upper bound. A common failure source attains 1/20. Disjoint failures attain zero. No independence is inferred from different process IDs, prompts, seeds, model names, authors, or evidence IDs.

The assumptions are essential: pass rates are not false-acceptance rates; rates estimated on different populations do not supply p and q here; adaptive selection may change the population. This package does not manufacture marginal-error certificates or a statistically valid estimator for them. Unavailable marginals mean CANNOT_CHECK for a numerical risk claim.

The exact checker compares all 16 Boolean events against every rational coupling with denominator 1 through 8: 494 feasible integer tables and 4,544 bound comparisons. These are calibration denominators, not independent empirical samples.

## 8. CV-T07 — agreement alone cannot verify a checker

**Statement.** Suppose the only observation about a proposition and its checkers is a common transcript T, and the admissible world class contains (truth=true,T) and (truth=false,T). No procedure based only on T can give a sound unconditional truth certificate for that proposition in both worlds.

**Proof.** The procedure's input is identical. A truth certificate emitted in the first world is also emitted in the second; if it instead refuses, agreement has not certified the truth. Randomization does not change the indistinguishable observation law. QED.

The checked witness is two PASS labels in both worlds. It is not an assertion that actual proof kernels have arbitrary correctness: a kernel's semantics, soundness theorem, audited assumptions, implementation identity, and trusted computing base can exclude the false world. Nor does the theorem demand an impossible authority-free starting point. It demands that the trusted assumptions and their scopes be stated, rather than replaced by self-agreement. This is a standard identifiability argument; no distinct meta-verifier theorem is claimed.

## 9. CV-T08 — a joint composition needs a coupling contract

For two finite component laws mu and nu, let C(mu,nu) be a NONEMPTY admitted set of couplings, optionally restricted by justified dependence information. An empty coupling set is INCONSISTENT, not an identified answer. Let h be a bounded query on the joint state. The joint answer is identified exactly when E_pi[h] is constant over all pi in C. If not, a sound result is the range of these expectations (or a certified outer bound), not the value under an unregistered independent coupling.

**Proof.** Constancy is sufficient by universal evaluation. If expectations differ for two admitted couplings, those couplings are indistinguishable from the provided component marginals but require different joint answers, proving necessity. For the finite binary case the exact range is CV-T06. QED.

A concrete composition of two fair-bit components yields equality probability 1 under the correlated joint law and 0 under the anticorrelated law. Each component's marginal certificate is unchanged. Thus individually correct causal/operator summaries do not license every composition. This same missing object explains the counterfactual and verifier examples: the absent evidence is about a joint law, not an extra vote. Logical conjunction of two valid marginal claims warrants their conjunction as claims; it does NOT assert a joint stochastic independence relation.

Parent: coupling theory, partial identification, and counterfactual identifiability [S1,S5,S6]. The scope-specific connection to warrant dependencies is an integration result whose independent utility still needs evaluation.

## 10. CV-T09 — source evidence does not authorize transport by itself

Consider a source model M_s and a target model M_t. The family containing (M_A,M_A) and (M_A,M_B) has identical source observational AND interventional laws but different target effects P(Y=1 | do(X=1)). Source-only evidence cannot identify that target effect.

**Proof.** The source evidence is identical and target queries differ; apply CV-T02's indistinguishability argument to pairs of environments. QED.

A transfer certificate must specify and justify the invariant mechanisms, population/selection assumptions, variables, estimand, and measurement mappings that remove the incompatible target world. A matching schema, name, benchmark score, or string-valued scope is insufficient. The code rejects source/target scope mismatch; it does not implement a complete transportability algorithm. Mature graphical transportability machinery has first right of refusal [S7].

## 11. CV-T10 — registration, observation and implementation boundaries

A registered exact-law record need not describe the actual population. In the executable falsifier, the do(X=1) law from M_A is registered while the actual model is M_B. All record-shape checks pass; M_B is excluded; the effect 1 is incorrectly supported relative to those false premises. This proves that registration alone is not sufficient for truthfulness. It does not contradict CV-T01 because an explicit premise fails.

Likewise, observing an event of positive probability does not imply that event has probability one or reveal the whole distribution. In continuous families even this support-only event rule needs different semantics because individual points can have probability zero; this implementation is expressly finite-discrete. Neither endpoint feedback nor a completed tool process is automatically an exact observation of a causal effect.

The necessary OCM distinction is: **record well formed / record content bound / evidence applicable / evidence semantically warranted / claim entailed / action authorized**. They are separate judgments. The types and resource-preserving action calculus are owned by #312/#313; this companion supplies causal and verifier cases they must be able to express.

## 12. Resource model and reproducibility boundary

The candidate evaluator gets the complete public finite model family and evidence predicates. This is substantial prior knowledge, not learned world structure. The hidden model is accessed only by the calibration generator to produce mathematical certificates and judge conclusions. The strong response-law channel has no field-data interpretation here.

For family size m, k fixed evidence predicates, per-predicate cost C_E and per-query cost C_Q, direct evaluation costs O(m*k*C_E + m*C_Q). Exhaustive support compilation scans at most 2^k subsets and costs O(2^k*m*(k*C_E+C_Q)) plus subset-minimality tests and output storage. The number of minimal supports can be exponential. Do not report this as output-sensitive local repair: enumerating and storing the profile is paid preprocessing. Revocation against a stored profile scans its support incidence data; no runtime optimality is proved.

Code uses rational probabilities and counts only declared finite tables; there are no model/network calls or estimated energy claims. Whole-process wall time, peak resident memory, file sizes, environment and command exits are recorded separately in RECEIPT.json, not mixed into the deterministic calibration body. Neither clean-checkout CI on the full repository, Lean mechanization, nor an external reviewer is supplied by local replay. `python -O` must retain every require-based check.

## 13. Constructive and hostile review roles

These are analytic duties within one session, not five independent people. Causal inference owns the intervention semantics and hierarchy; formal methods owns non-vacuous entailment and revocation; statistics owns sharp joint bounds and invalid independence shortcuts; systems owns content binding and reproducible exits; the hostile-parent role owns source collisions, failed formulations and scope contractions. For every theorem, the constructive argument is paired above with a counterexample, a premise-removal test, or a limiting case. The machine mutations are supplementary, not an independent assumption audit.

Eight applied code mutants are rejected: vacuous truth; ignored scope; independent counterfactual coupling; independent verifier errors; ignored revocation; a coordinate-swapping alternate oracle; sample-to-law promotion; and observation substituted for intervention. The last mutant was initially caught at an EARLIER consistency gate than the test expected. The test's exact expected reason was corrected to `INCONSISTENT_BASE_FOR_MONOTONE_PROVENANCE`; the production algorithm, model family, outcomes and thresholds did not change. That initial test failure is disclosed in RECEIPT.json.

## 14. Frontier left explicit

This closes a scoped exact causal/verifier foundation fragment, not all Machine Epistemics. The next scientific questions are: finite-sample confidence sets that preserve model coverage under adaptive experiments; partial coupling certificates that permit useful composition without imposing independence; revision when the model family itself expands or the intervention semantics change; and efficient support maintenance without exhaustive profiles. Each needs the strongest partial-identification/provenance parent and its full costs. #314 owns decision-cost optimization; #312/#313 own graded warrant/risk and generic foundation corrections. No parallel remint is created here.

Current targeted prior-art search found a direct 2026 ternary causal-testing parent [S2]. A surfaced August 2026 partial-identification/linear-programming preprint could not be fetched from its primary arXiv endpoint [S8]. This unresolved source prevents a saturation or priority claim. It does not block the self-contained elementary proofs above.

Sources and actual access levels are in SOURCES.md. Runtime adoption requirements are in ABSORPTION.md. Every theorem remains subject to independent reconstruction and counterexample-based reopening.
