# Machine Epistemics Field Frontier V1

This frontier begins **after** the original MEG-01…35 programme and batches 1–5. It asks field-level questions that are not just missing OCM functions.

Every row may terminate positive, negative, parent-sufficient or `CANNOT_CHECK`. No row is a novelty claim.

## FDX-01 — open-system epistemic closure

When is a registered dependency/model/revision description sufficient to support claims about a system whose real environment may contain unmodelled transitions or dependencies?

Target: characterize the weakest checkable closure interface under which outside-model events cannot invalidate the registered conclusion, or prove that no nontrivial current-validity guarantee exists without such an interface.

Strong parents: robust model checking, assume-guarantee reasoning, open systems, distributional/causal robustness.

Batch 8 disposition (H1, `../KSO_FIELD_FRONTIER_THEOREMS_BATCH8_V1.md`, checker
`../kso_field_frontier_batch8_exact.py`): **PROVED (finite) + EXACTLY_BOUNDED_IMPOSSIBILITY.** The
weakest checkable closure interface is "every dependency root of the conclusion is covered by a
registered monitor or a registered revocable assumption" (necessary and sufficient, 3 456/3 456
(D, coverage) pairs); unconditional current validity needs a monitor on every root. Below the
interface no function of the registered state is a sound current-validity claim (1 727 view-identical
witnesses). Closure is relative to `D`; dependency completeness stays a registered assumption
(`CANNOT_CHECK` from inside). The interface is PARENT_OWNED (assume-guarantee assumptions,
monitorability, ATMS assumptions); only the typed certificate MONITORED_CURRENT /
CONDITIONAL_ON_ASSUMPTIONS / NO_CLOSURE is registered here.

## FDX-02 — controlled epistemic viability

Given truth-warrant, authority, scope, risk and resource predicates, characterize the largest set of epistemic states from which a policy over `{query, observe, experiment, clarify, wait, abstain, act, propose-representation-change}` can maintain a registered commitment invariant against the declared environment/revision envelope.

First right of refusal: viability theory, safety games, POMDP/belief-state control. Residual must come from the typed epistemic predicate/interface, not renaming the viability kernel.

Batch 8 disposition (H2): **PARENT_SUFFICIENT**, as predicted. On the 10 584-state fixture the
typed-close kernel and the commit attractor are the parent's finite-horizon safety/reachability
kernels (backward induction). The typed interface adds only the action-effect table, from which the
closed form `Win ⟺ licensed ∨ (complete ∧ b ≥ 1) ∨ (a = 1 ∧ b ≥ c_w + c_k + c_r + ρ·c_q + 1 ∧
t + n_w + n_k + n_r + ρ ≤ T)` follows (agrees 10 584/10 584); commit is forceable only with no
information action pending (312 states); with an always-licensed abstain the kernel is trivial
(10 584); the indefinite-safety contract of FD-06 has the total kernel (1 512) and is not the deadline
contract. No residual claimed.

## FDX-03 — information/interface conservation

Find the strongest theorem relating reduction of epistemic uncertainty to information actually supplied by observations, traces, certificates, interventions, verifiers, model restrictions and memory. The theorem must charge all side information and distinguish exact truth, distributional risk, upper/closure evidence and action authority.

Finite version-space counting is only one special case. Strong parents: communication complexity, decision-tree/query complexity, Blackwell sufficiency, information theory, teaching/query dimensions.

Batch 8 disposition (H3): **PROVED for the finite deterministic typed fragment; FD-07 general stays
OPEN_RESEARCH.** On 16 hypotheses × 6 channels (observations, two verifiers, memory replay, a
risk-typed channel, a class assumption): the version space after any transcript is the join class of
the channels used; a channel adds nothing iff it is a garbling of the join (384/384; memory 533/533
zero); the parity verifier carries exactly the missing observation; `D(H) = 4 = ⌈log2 16⌉` with or
without verifiers (65 535 subsets at or above the entropy bound); class-assumption extrapolations
carry the assumption id and collapse on its revocation (32/32); a risk-typed channel never reduces
the exact space; guaranteed identification against declared channels needs `⌈log2 L⌉` undeclared
bits (`L` the largest join class) and observed success establishes nothing (null probability
reported, never an accusation). PARENT_OWNED mathematics (query complexity, Blackwell, teaching
dimension via batch-4 D2).

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

Batch 8 disposition (H4): **PROVED (finite classification) / PARENT_OWNED components.** On the
ledger fixture (12 single transitions, 142 + 1 667 sequences) every transition is exactly one of
ESI (semantic projection restored: revoke/reinstate, quarantine/release), BOI_STABLE (behaviour and
future-revision probe restored, a dead identity persists: admit, adopt, LIFO rollback),
BOI_DIVERGENT (current behaviour only: relearn, deletion of a redundant identity, DPO round trip with
fresh stamps) or NI (external act, loss of the only support). All-ESI components ⇔ ESI composite;
an act anywhere ⇒ NI; the full append-only state is never restored; a re-minted deleted identity
restores the projection byte-for-byte and is witnessed only by the history. Event sourcing, LIFO
transactional undo, AGM recovery and provenance identity own the components; FD-05 is extended.

## FDX-06 — distributed Machine Epistemics

For multiple machines with delayed/partial communication, characterize which warranted claims and commitments can be maintained under stale replicas, shared/independent evidence, Byzantine or fallible sources, and changing authority.

Required distinctions: causal consistency ≠ application invariant; message authenticity ≠ truth; consensus ≠ world truth; missing update ≠ no update.

Parents: distributed knowledge, consensus, CRDT/replication theory, Byzantine agreement, information-flow security.

Batch 10 disposition (J1, `../KSO_FIELD_FRONTIER_THEOREMS_BATCH10_V1.md`, checker
`../kso_field_frontier_batch10_exact.py`): **PARENT_SUFFICIENT, with PROVED corollaries on the
fixture.** Convergence of exchanged revocation state is the state-based CRDT theorem (revoke-wins
observed set; 59 causally consistent delivery orders agree, a last-writer-wins flag diverges on 117
order pairs); the freshness impossibility is R5 (a view missing an effective revocation is a prefix of
two histories with different verdicts: 97 wrong / 0); Byzantine agreement is needed only for
authority-bearing registry objects and is the parent's. Exact typed statements: liveness is antitone in
the revocation set (4 536); a stale view over-claims only by a missing revocation and under-claims only
by a missing reinstatement (354/354, 369/369); an import's authority is `drop_commit(A_sender ∧ trust
cap)` — never raised, commit 0, bounded along relays (1 458), never joined across paths (490 caught);
per-message assumptions make trust revocation local to the import cone (1 336) and leave native atoms
untouched; `Impact_D` distributes over unions (4 096) so batched remote deltas never reopen more than
sequenced ones (36); `k` agreeing sources are `⊕` alternatives at authority `source` — consensus is not
world truth. The four required distinctions are met on the fixture. OPEN: graded / probabilistic trust
(FDX-08). CANNOT_CHECK: message authenticity.

## FDX-07 — epistemic games

Model agents that strategically choose what evidence, claims or certificates to reveal. Determine truthful-equilibrium or impossibility conditions for machine-to-machine/human-to-machine evidence exchange when verification and querying are costly.

Parents: mechanism design, signaling, Bayesian games, interactive proofs, peer prediction. This is likely parent-heavy and must be attacked as such.

Batch 10 disposition (J2): **PARENT_HEAVY / PARENT_SUFFICIENT, attacked as an attack surface.** The
strategic results (truthful equilibria, disclosure, persuasion, inspection games, Sybil) are the
parents'; the inspection-game equilibrium `q* = g/(g+f)`, `p* = c/d` is verified exactly on 63 rational
grids as the parent's object. PROVED gate-specific, on 81 provider strategies × 6 claims × 3
requirements: the provider's action set on the commitment gate is exactly {enable REPORT-typed commits
of claims within its channel authority (36 / 61 / 18 strategies), force refusal of claims whose every
exhibited warrant cites its ids (45 / 20 / 63; 0 for claims with a provider-free alternative), poison
joint supports containing its ids}; it never changes the verdict on a provider-free claim (486/486),
never reaches `world_truth` or `commit` (0/486, EXACTLY_BOUNDED), and has no persuasion lever because
the gate computes no posterior (4 374 invariance checks). A licensed commit names its committing warrant
so retraction reopens exactly the cone; three Sybil ids are one independent support over principals.
OPEN: truthful mechanisms for real provider utilities. CANNOT_CHECK: that real utilities match any payoff
matrix; a provider who compromises a typed channel is outside the model.

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

Batch 10 disposition (J3): **PARENT_OWNED mathematics; PROVED exact table on the registered classes
ALL16 / AFFINE8 / MONOTONE6.** Identification: total channel bits along any adaptive transcript
`≥ ⌈log2 |V|⌉` for every version space and every mix of 1-, 2- and 4-bit channels (327 675 checks;
4 bits on the full class for all five mixes — wider channels move bits, they do not remove them).
Retention: fewer than `log2 |H|` mutable bits cannot retain `H`; the affine description with 3 bits
retains 8 and must refuse 8 (`CANNOT_REPRESENT`). Repair: `Σ(retained ids) + worst-case repair queries
≥ n + k` against `k` revocations for every redundancy design (648 + 48 checks, tight on 164); a repair
from memory replay violates it on 324 cases. Communication: equality of retained procedures needs
`≥ 4` transcript bits (fooling set); a `d`-bit digest admits 56 / 24 / 8 / 0 false-equality pairs.
Verification: oblivious probes / adaptive probes / entropy bound = 4/4/4, 3/3/3 and **4/3/3** on
MONOTONE6 — one probe above the teaching-dimension bound for a target-oblivious verifier. Whole system:
the affine description moves exactly one unit out of every phase and adds 8 `CANNOT_REPRESENT`
targets — cost moves, it is not erased. Scale: four-row classes, checked at `n = 2` (repair at
`n = 2, 3`); the general forms are the parents' pigeonhole facts. OPEN: coded cross-row redundancy
(Singleton-type), infinite classes. CANNOT_CHECK: digest collision resistance.

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
