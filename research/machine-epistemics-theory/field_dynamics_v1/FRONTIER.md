# Machine Epistemics Field Frontier V1

This frontier begins **after** the original MEG-01…35 programme and batches 1–5. It asks field-level questions that are not just missing OCM functions.

Every row may terminate positive, negative, parent-sufficient or `CANNOT_CHECK`. No row is a novelty claim.

## FDX-01 — open-system epistemic closure

When is a registered dependency/model/revision description sufficient to support claims about a system whose real environment may contain unmodelled transitions or dependencies?

Target: characterize the weakest checkable closure interface under which outside-model events cannot invalidate the registered conclusion, or prove that no nontrivial current-validity guarantee exists without such an interface.

Strong parents: robust model checking, assume-guarantee reasoning, open systems, distributional/causal robustness.

## FDX-02 — controlled epistemic viability

Given truth-warrant, authority, scope, risk and resource predicates, characterize the largest set of epistemic states from which a policy over `{query, observe, experiment, clarify, wait, abstain, act, propose-representation-change}` can maintain a registered commitment invariant against the declared environment/revision envelope.

First right of refusal: viability theory, safety games, POMDP/belief-state control. Residual must come from the typed epistemic predicate/interface, not renaming the viability kernel.

## FDX-03 — information/interface conservation

Find the strongest theorem relating reduction of epistemic uncertainty to information actually supplied by observations, traces, certificates, interventions, verifiers, model restrictions and memory. The theorem must charge all side information and distinguish exact truth, distributional risk, upper/closure evidence and action authority.

Finite version-space counting is only one special case. Strong parents: communication complexity, decision-tree/query complexity, Blackwell sufficiency, information theory, teaching/query dimensions.

## FDX-04 — nonstationary fast/slow tracking

FD-04 gives one-step fixed-point sensitivity. Extend to a time-indexed sequence `(P_t,s_t)` and derive tracking/regret/decision-stability bounds under bounded drift, asynchronous revision and finite iteration budgets. Separate activation tracking from correctness/warrant tracking.

Parents: nonstationary Markov chains, online optimization/control, tracking of contractions.

Parent attack disposition: the elementary tracking recurrence is reconstructed
in DYNAMICS.md and is `PARENT_SUFFICIENT`. Bernstein and Dall'Anese,
[Asynchronous and Distributed Tracking of Time-Varying Fixed Points (2018)](https://arxiv.org/abs/1804.09768v2),
already treat moving contractions, imperfect maps and asynchronous updates.
Reusing that mathematics is parent specialization. Only a separately formulated
decision/warrant/revision theorem could reopen a residual; changing vocabulary
or adding an OCM implementation cannot do so.

## FDX-05 — reversible and irreversible epistemic transitions

Characterize when a sequence of evidence, representation and self-modification transitions has an exact semantic inverse, a behaviour-only inverse, or no inverse. Include append-only history, quarantine, irreversible external effects and lost model/evidence identity.

Do **not** use physical-thermodynamics language as evidence. Parent families: reversible computation, event sourcing, transactional rollback, belief revision and provenance.

## FDX-06 — distributed Machine Epistemics

For multiple machines with delayed/partial communication, characterize which warranted claims and commitments can be maintained under stale replicas, shared/independent evidence, Byzantine or fallible sources, and changing authority.

Required distinctions: causal consistency ≠ application invariant; message authenticity ≠ truth; consensus ≠ world truth; missing update ≠ no update.

Parents: distributed knowledge, consensus, CRDT/replication theory, Byzantine agreement, information-flow security.

## FDX-07 — epistemic games

Model agents that strategically choose what evidence, claims or certificates to reveal. Determine truthful-equilibrium or impossibility conditions for machine-to-machine/human-to-machine evidence exchange when verification and querying are costly.

Parents: mechanism design, signaling, Bayesian games, interactive proofs, peer prediction. This is likely parent-heavy and must be attacked as such.

## FDX-08 — stochastic warrant dynamics

Develop a mathematically disciplined extension for uncertain/graded evidence without laundering probability into individual truth. Requirements: exact dependence semantics, revocation/update, scope/population identity, calibration drift, and compatibility with certified-only truth gating.

The current graded navigation score is not this object. Parent families: imprecise probability, credal sets, Dempster-Shafer/possibility where applicable, probabilistic databases/provenance, selective/conformal prediction.

## FDX-09 — infinite structured lifecycle learning

For a natural infinite grammar/program/transducer family, identify behaviour **and future revocation/reopening behaviour** up to a registered lifecycle equivalence. Derive positive bounds or a non-identifiability theorem under explicit channels.

Parents: Gold/Angluin learning, grammar/transducer learning, computational traces, characteristic samples, version spaces, incremental provenance.

## FDX-10 — endogenous representation discovery

When can a machine discover a representation/partition/operator vocabulary from evidence rather than selecting from a fixed candidate menu, while preserving externally checked semantics and avoiding self-certification?

Parents: program synthesis, representation learning, abstraction discovery, CEGAR, state aggregation, dictionary/library learning. A result must count search and evaluation information.

## FDX-11 — epistemic bifurcation / obstruction

Characterize points at which a registered task family ceases to be solvable under the current representation/operator/observation interface and what certificate is sufficient to distinguish an actual expressive obstruction from missing evidence, revoked support, insufficient budget or a bad search policy.

This generalizes governed-Jump obstruction certificates. Parent first refusal: completeness thresholds, CEGAR, proof search, model-class misspecification tests.

## FDX-12 — safe incremental language commitment

Find the exact condition under which a generated prefix may be externally committed while semantic, referential or evidential obligations remain unresolved. A candidate condition is invariance of already committed semantic content across all currently admissible completions plus live/authorized support.

Parents: incremental NLG/parsing, safety games, runtime monitoring, prefix-closed languages. Natural-language measurement is empirical and separate.

## FDX-13 — self-model calibration and reflexive dependence

Quantify what a self-model can reliably infer about the machine’s future performance when its own predictions affect routing, representation proposals or evaluation. Separate observational self-modeling from self-authority.

Parents: adaptive data analysis, performative prediction, self-modifying systems, calibration under distribution shift.

## FDX-14 — whole-system lower bounds

Derive lower bounds across immutable description, mutable memory, verification, communication and test-time computation for natural task families. Representation or external memory may move cost but cannot erase it.

Parents: communication/cell-probe/branching-program/advice complexity, data-structure lower bounds, streaming and online computation.

## FDX-15 — parent-product equivalence / residual theorem

Construct the strongest faithful parent product:

`dynamic belief/provenance + abstract interpretation + POMDP/PSR + causal inference + active information acquisition + runtime verification + algorithm selection/program synthesis + distributed transaction/noninterference controls`.

Then prove either:

- a precise Machine-Epistemics residual the parent product lacks under matched interfaces/resources; or
- a simulation/equivalence theorem showing the field is a useful integration/typing discipline with no architecture-specific mathematical residual.

This is the load-bearing novelty/identity question.

## FDX-16 — mechanized core semantics

Mechanize a small but representative core: warrant intervals/support composition, nogood normalization, authority meet, local reopening, typed terminals, and at least one representation/revision commutation theorem. Include false-theorem, missing-premise and axiom/sorry leak controls.

Mechanization validates a formal statement; it does not prove that the statement models the real OCM/environment.

## Empirical frontier, separately typed

Theorems cannot establish these alone:

- open-domain natural-language grounding and communication;
- real scientific/coding-task superiority;
- large-scale representation discovery;
- calibration under real nonstationarity;
- practical energy/wall-clock benefit;
- human/multi-agent trust dynamics;
- external academic-field recognition.

These must use frozen empirical protocols and strongest matched parents, with negative and `CANNOT_CHECK` terminals preserved.

## Priority

The highest-value mathematical sequence is FDX-02 → FDX-03 → FDX-04 → FDX-15, while FDX-06/09/12/13 develop the distributed, learning, language and self frontiers. FDX-16 should mechanize only statements that survive parent attack.

`GENERAL_NOVELTY = NOT_ESTABLISHED`. `FIELD_STATUS = NOT_ESTABLISHED`.
