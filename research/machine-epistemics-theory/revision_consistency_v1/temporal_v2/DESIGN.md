# Temporal validity V2: pre-calibration specification

Parent PR #326 and issue #197; work division #304. Predecessor head: 97d35a13c3213fbbfb0c090923bf4271bddbf757. This is an additive successor, not an amendment of V1 results, proofs or receipt. Own paths: this temporal_v2 directory and .github/workflows/me-temporal-validity.yml. No foundation_v1, decision_frontier_v1, OCM runtime or protected empirical outcome is changed.

Question: under a registered finite revision model, exactly when does a currently admissible claim remain admissible after every permitted unobserved revision? What can be concluded when the revision relation is only bounded above and below?

Model: finite nonempty state set S; fixed admissibility predicate P; lower and upper directed edge sets L subset U; actual revision relation T satisfies L subset T subset U. Every intermediate relation is an admissible completion. Initial belief B is nonempty. Safety quantifies over all finite paths including length zero; dead ends may remain quiescent. A model answer is neither factual truth nor external commit permission. Completeness of S/U, authenticity, prior authority and real synchronization remain separate OCM proof obligations.

Targets: greatest invariant subset of P; reverse-reachability construction with a shortest adverse path; independent descending-fixed-point parent; exact may/must bracket and three-valued universal-persistence decision; monotonicity under consistent envelope refinement; one-step checking and observation-only closure counterexamples. Parent sufficiency is expected (temporal-logic safety/model checking and partial-model semantics); no novelty claim.

Registered finite calibration: all directed graphs (self-loops included), all predicates and nonempty beliefs for n=1,2,3; every n=2 lower/upper envelope, predicate, belief and intermediate completion. Report positive, refuted and CANNOT_CHECK denominators separately. Enumerations calibrate the finite implementation, never prove the unbounded statements. No stochastic or protected study is performed.

Hostiles: current validity substituted for future validity; one-step-only check; optional edges silently absent or required; empty belief treated as proof; malformed or wrong-model witness; booleans used as integer identities; mutable nested input; digest drift and missing source. No-alarm cases include cycles entirely inside P and irrelevant additional transitions. Execution limits, missing source and absent model closure must never be relabeled PASS.

Review roles within ONE authoring session: formal epistemics (quantifiers), model checking (construction/parent), distributed systems (freshness premises), resource accounting (whole-model costs), hostile review (counterexamples). These are not independent experts or review authority. No subagents or external compute workers are spawned.

Execution: stdlib-only checks in the isolated Linux analysis container, with actual interpreter recorded; fresh-process and optimized-mode replay; CI from GitHub checkout. Direct local repository clone is unavailable owing to DNS failure. Valid study dispositions: PARENT_SUFFICIENT, CORRECTED_FOUNDATION_FRAGMENT, REFUTED, CANNOT_CHECK. Overall foundation and independent review remain open.
