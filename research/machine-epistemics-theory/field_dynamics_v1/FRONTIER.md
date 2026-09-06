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

Batch 9 disposition (I1, `../KSO_FIELD_FRONTIER_THEOREMS_BATCH9_V1.md`, checker
`../kso_field_frontier_batch9_exact.py`): **PROVED (finite) + EXACTLY_BOUNDED_IMPOSSIBILITY.** A
time-indexed claim "LIVE at t" is the ledger fact for t ≤ now and, for the future, a statement about the
law of paths under a *registered generating model*; a receipt may state the ledger liveness exactly and a
predictive probability only as CONDITIONAL_ON_MODEL with the model id as a revocable assumption
(NO_MODEL_REGISTERED carries nothing stochastic). On 9 two-state chains × 64 paths: the predictive
probability is not a function of the path (three values, spread ½, on every path; the empirical rate
matches no registered model on 44/64); a reopening-rate bound exists iff a model or a revision envelope is
registered (adversary with ρ revocations: ≤ min(2ρ, T) flips; unbudgeted: T, every smaller bound has a
counter-path); Bayesian revocation is marginalisation (the divide-out is wrong on 320/384 pairs, exact only
at the last step and on the i.i.d. subclass); a registered guarantee is revoked by an anytime-valid
e-process (false revocation 0.011 ≤ α over 12 steps, Ville) where per-step fixed-level re-testing reaches
0.075; the guarantee never touches an individual output's exactness (⟦0,{g}⟧ UNKNOWN on 4 096/4 096).
PARENT_OWNED (Markov chains, test martingales / SPRT, Bayes). The graded half (imprecise probability,
credal sets, D–S) is not entered: D3 / F6 / G6 stand and no scalar-semiring claim is added; batch 10's
open item "graded / probabilistic trust and Byzantine-fraction thresholds for warrant exchange" stays open.

## FDX-09 — infinite structured lifecycle learning

For a natural infinite grammar/program/transducer family, identify behaviour **and future revocation/reopening behaviour** up to a registered lifecycle equivalence. Derive positive bounds or a non-identifiability theorem under explicit channels.

Parents: Gold/Angluin learning, grammar/transducer learning, computational traces, characteristic samples, version spaces, incremental provenance.

Batch 11 disposition (K1, `../KSO_FIELD_FRONTIER_THEOREMS_BATCH11_V1.md`, checker
`../kso_field_frontier_batch11_exact.py`): **PARENT_OWNED mathematics; PROVED exact corollaries on the
category-level construction fixture; NOT sealed.** The learner the OCM N1 grammar induction runs (the
attested set of `H ← [dep … HEAD … dep]` rules, one relation label per dependent, a dependent slot accepting
any phrase of its category) identifies every finite inventory of bounded arity in the limit from positive
demonstrations (255/255 sub-inventories of an eight-rule universe; Gold 1967 for finite classes) after a
characteristic sample of one demonstration per rule (4 trees for the six-rule treebank, lower bound
⌈|G| / max rules per tree⌉ = 2); the expected cover time of a uniform demonstration text over `r` rules is
`r·H_r` (761/35 for `r = 8`), a Zipf text pays ≈ 38.9; the unbounded-arity family changes its conjecture at
every arity and never converges (G9 restated, 6/6). The exact obstruction for the class N1 uses: the
derivation count of a category string is the number of projective trees × attested labellings (chart =
brute force, 12/12); it is Catalan(k+1) = 1, 2, 5, 14, 42 for `N V N (P N)^k` under the saturated inventory
and 3 / 2 / 1 for the treebank strings (two attachments plus two relation labellings of `N V N`); positive
demonstrations never lower it (192/192 monotone), so a unique parse is unreachable from positive data once
two attachments are attested — only revocation / a negative channel (C6) reaches `INTERPRETED` (14 of 64
sub-inventories, all below). Evidence-licensed ranking orders derivations for unpacking and licenses
nothing (top-1 commit picks the wrong gold; caught). A packing key that contains the sub-derivation's key
stores one node per derivation (4, 10, 22, 50, 125 vs 4, 9, 16, 25, 36) — the item-cap consequence. OPEN:
lexicalised inventories, the exact UD-EWT sample cost. CANNOT_CHECK: convergence of the UD-EWT inventory;
that the real cap is reached for this reason.

## FDX-10 — endogenous representation discovery

When can a machine discover a representation/partition/operator vocabulary from evidence rather than selecting from a fixed candidate menu, while preserving externally checked semantics and avoiding self-certification?

Parents: program synthesis, representation learning, abstraction discovery, CEGAR, state aggregation, dictionary/library learning. A result must count search and evaluation information.

Batch 11 disposition (K2): **PARENT_OWNED (Solomonoff/Levin size-ordered search, Rissanen MDL,
DreamCoder-class library learning, Kolmogorov invariance); PROVED exact corollaries on the Boolean
library fixture; NOT sealed.** Over `{x, y, NOT, AND, OR}` (9 168 terms up to size 8) the version space of
every partial evidence table is a set of behaviours identical under every library (81/81), so the
identification bits ⌈log2 |V|⌉ are representation-invariant and no unseen row is determined by a
representation (104/104). A discovered operator moves search cost both ways: XOR falls from position 2 936
to 16 and EQV from 6 990 to 38, seven functions rise, all positions stay within the finite Levin bound
(32/32). The MDL / library-learning adoption rule (Σ size savings − definition cost) adopts XOR (cost 8)
only on task sets containing both XOR and EQV (4 of 15 sets; a single XOR task has gain −2); discovering
the operator costs 4 selection bits and 26 032 evaluated terms per candidate against 0 when it is given. The
self-certification hostile (a memorising abstraction priced as one symbol) is adopted on 39 partial tables
and claims the unseen row; honest table pricing adopts it on 0. A definition is identified only up to its
extension (8 minimal XOR definitions, indistinguishable by any evidence). OPEN: the proposal policy over an
infinite abstraction space. CANNOT_CHECK: that a real proposed abstraction's evaluator is registered.

## FDX-11 — epistemic bifurcation / obstruction

Characterize points at which a registered task family ceases to be solvable under the current representation/operator/observation interface and what certificate is sufficient to distinguish an actual expressive obstruction from missing evidence, revoked support, insufficient budget or a bad search policy.

This generalizes governed-Jump obstruction certificates. Parent first refusal: completeness thresholds, CEGAR, proof search, model-class misspecification tests.

Batch 9 disposition (I2): **PROVED (finite).** On 512 states (16 evidence × 8 nogood × 4 authority) × 3 840
single changes the flip set of the commitment set is exactly {revoked id is a cut of the live alternatives}
∪ {reinstated id completes an alternative} ∪ {new nogood covers every live alternative} ∪ {authority bit of
the meet}; all 2 524 flips are explained and none is a mechanism failure (the hostile that reads a jump ≥ 2
as a defect alarms 588 times, always on an explained flip; a graded support score masks 1 688 flips).
Evidence and nogood changes flip ≤ 2 atoms, an authority withdrawal up to 5 (the meet is discontinuous by
FD-01). The C7 verdict policy equals Dung's grounded extension on 512/512 states; the 32 conflict states
have two stable extensions and a credulous pick is not a function of the evidence. The obstruction
certificate is exactly the *evidence-invariant failure inside the registered representation*: OBSTRUCTION
iff the target fails at every evidence state (12/12 on the E3 fixture), so an obstruction lies on no
E-boundary and only an R-transition moves it; certifying on an E-boundary (5 cases a reinstatement solves)
is caught. That predicate is what separates an expressive obstruction from missing evidence and revoked
support (E-boundaries) and from budget / search (E2 verdicts). PARENT_OWNED (monotone Boolean sensitivity,
ATMS label change, hitting sets / F1, Dung 1995, batch-5 E3 / batch-7 G1).

## FDX-12 — safe incremental language commitment

Find the exact condition under which a generated prefix may be externally committed while semantic, referential or evidential obligations remain unresolved. A candidate condition is invariance of already committed semantic content across all currently admissible completions plus live/authorized support.

Parents: incremental NLG/parsing, safety games, runtime monitoring, prefix-closed languages. Natural-language measurement is empirical and separate.

Batch 11 disposition (K3): **PARENT_SUFFICIENT (Alpern–Schneider safety; F6's finite criterion; G3's
completeness threshold; Bar-Hillel for the context-free × regular product); PROVED exact corollaries on a
finite-state generator with listener readings; NOT sealed.** A prefix may be emitted iff an accepting
completion is reachable, every reachable accepting reading contains the prefix reading, and every
committed claim is LIVE and authorised — decided by reachability (20 states; garden-path and late-negation
prefixes UNSAFE, 5 states). A bounded lookahead is exact at two thresholds: SAFE is decisive iff `k ≥ ℓ*`
(shortest accepting completion) when nothing is committed and iff `k ≥ max(ℓ*, d)` (saturation depth of the
reachable set) otherwise; UNSAFE is decisive iff `k` reaches the first violating accepting state; decisive
verdicts never contradict the exact ones (147 agreements, 33 CANNOT_CHECK). The channel is a premise: the
atomic final-reading check the N2 realiser performs passes all 6 accepted strings, the streaming check
passes 2 (the four refused strings carry an unsafe intermediate prefix). Revoking the evidence of a
committed claim blocks further emission and keeps the history. Hostiles: existential lookahead (SAFE on all
5 unsafe states), bounded pass read as SAFE (16 cases), forgetting committed content (emits through a
revocation). Context-free acceptability with a regular reading is decidable by the product (stated, not
checked); context-free readings are undecidable (G3, cited). CANNOT_CHECK: the listener's reading table
for natural language.

## FDX-13 — self-model calibration and reflexive dependence

Quantify what a self-model can reliably infer about the machine’s future performance when its own predictions affect routing, representation proposals or evaluation. Separate observational self-modeling from self-authority.

Parents: adaptive data analysis, performative prediction, self-modifying systems, calibration under distribution shift.

Batch 9 disposition (I3): **PROVED (finite).** With a router that adopts the self-prediction (at or above θ
every task goes to the operator, below θ only the easy ones), the realised rate depends on the prediction;
on 75 fixtures the performatively stable predictions are exactly {r_A if r_A < θ} ∪ {(r_A+r_B)/2 if ≥ θ} —
none on 9, one on 59, two on 7 (bistability) — and repeated retraining converges in ≤ 2 steps iff a fixed
point exists in the reached regime, else oscillates with period 2 (81 orbits); the counterfactual (shadow)
rate is defined on all 75. A self-model that ignores the loop is wrong under adoption on 26 fixtures. A
prediction scored on the outcomes its adoption caused is self-fulfilling (42 cases calibrated
performatively and not counterfactually); the E4 disjointness clause is necessary and not sufficient when
the router reads the prediction — the shadow (E5), whose routing does not, is the counterfactual arm and
the only E4 evidence. Reusing one held-out across k = 3 candidates reports 47/64 for a true ½ (optimism
15/64). A self-prediction may steer routing (J0) and is never a warrant (⟦0,{r}⟧ UNKNOWN). PARENT_OWNED
(performative prediction — Perdomo et al. 2020; adaptive data analysis — Dwork et al. 2015; E1/E4/E5).

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

Batch 9 disposition (I4): **PROVED (finite attribution theorem) / PARENT_SUFFICIENT on the fixture /
CONJECTURE for the general equivalence.** A measured residual over the strongest parent buildable is
attributable to the declared experimental difference Δ iff (1) the reference arm is outside the decision
(F8), (2) no unit is pooled (F2), (3) the pre-registered rule rejects on independent lifetimes (G8), (4) the
ablation arm OCM−Δ equals the parent *unit for unit* on the matched channels — the only executable
matching certificate; declared-identical inputs are necessary and not sufficient — and (5) the differences
are not one coin. On the 12-task × 8-lifetime fixture: a real residual (differences vary, p = 1/256,
ablation ≡ parent on 96/96 units) is attributable; a parent missing half the manifest rejects 8/8 on a family
Δ never touches and the ablation arm still wins (16 units) — CONFOUNDED_BY_UNMATCHED_INFORMATION; a residual
on three lifetimes gives p = 1/8 — INCONCLUSIVE_UNDERPOWERED (minimum detectable win probability 0.90 at
power 0.8 with m = 8; inside one lifetime of four items D1 is INCONCLUSIVE on all 15 tables and
PARENT_SUFFICIENT needs n_d ≥ 76); a deterministic family is 8/8 one coin — flagged; pooled orderings and a
reference arm inside the decision (verdict flips with the grader, G7) are refused. Parent+Δ ≡ OCM and OCM−Δ
≡ parent on the fixture by construction: the measured residual is Δ, and Δ is parent-owned machinery — the
dichotomy FRONTIER poses is not exclusive (a real *measured* residual against the buildable parent with a nil
*mathematical* residual). The general equivalence (FORMALISM_USEFUL_NO_ARCHITECTURE_RESIDUAL) is a
CONJECTURE with the falsifier "an OCM−Δ arm that differs from the parent product on a matched unit"; no
finite fixture promotes it. The M12 V4 result satisfies clauses 1, 2, 3, 5 and *declares* clause 4
(RESIDUAL_ATTRIBUTION_DECLARED_NOT_ABLATED); V5 needs the ablation arm.

## FDX-16 — mechanized core semantics

Mechanize a small but representative core: warrant intervals/support composition, nogood normalization, authority meet, local reopening, typed terminals, and at least one representation/revision commutation theorem. Include false-theorem, missing-premise and axiom/sorry leak controls.

Mechanization validates a formal statement; it does not prove that the statement models the real OCM/environment.

Batch 12 disposition (`../KSO_MECHANISED_CORE_BATCH12_V1.md`, Lake project `../lean/kso_core/`,
`../../../tests/unit/test_kso_mechanised_core_batch12.py`; NOT sealed): **PROVED in Lean 4.14.0 (no
Mathlib, no `sorry`, axioms ⊆ {propext, Quot.sound, Classical.choice}) for the warrant core**, with
the OCM exact checkers as the finite oracle. Mechanised: the Kleene order and connectives as a
distributive lattice with `∧₃` = min, `∨₃` = max, monotone (all 81 quadruples); `ℓ_R(P ⊕ Q)`,
`ℓ_R(P ⊗ Q)` and the semiring laws on the liveness function (KS-T01, up to `Equiv`); OCM's syntactic
`leq` ⇔ the semantic order (`synLeq_iff_leq`); warrant intervals with well-formedness carried by
`⊕` / `⊗` by construction; **KS-T21** in full (`lam_otimes`, `lam_oplus`, reduction, refinement
monotonicity); KS-T23's warrant half (`lam_otimesAll_*`); KS-T18 (`lam_zero_DEAD`); revoking more
never revives (`lam_antitone`, batch-10 J1 (i)); revoked exhibited support ⇒ never LIVE, revoked
possible support ⇒ DEAD; the fuel-bounded closure `reach` extensive, monotone, union-distributive
(J1 (vii)), empty on an empty seed, with the non-LIVE seed and hence the cone monotone in `R`
(`reachDead_mono`); KS-T22 (1)/(2) liveness halves and (3) on the changed set; the authority meet
never raises (T1 (i)), is the glb, folds below every factor (KS-T20), `internal_authority` pins
`commit = 0`, and no internal chain reaches commit (T1 (iii), with the operator-factor premise).
Controls in the build: wrong Kleene order, OCM `mutant_unknown_as_dead` / `_as_live` /
`mutant_meet_as_union` / `mutant_authority_max` / `mutant_impact_cone_direct_only`, the §1.3
completeness bit (false-theorem control), the dropped `wf` premise (missing-premise control),
MEG-16-REFUTED-V0 — each refuted by a proved witness; the failing `example` per mutant is described
in the batch document. Tightened: semiring and interval laws hold up to liveness equivalence (canon
normal form stays FINITE, `check_semiring`); the cone's least-closed-superset characterisation, the
REOPEN / RECHECK / UNAFFECTED partition, KS-T04c, KS-T24, KS-T07b and MEG-16B/C/E stay FINITE
(OCM checkers). **OPEN** on this row: typed terminals and a representation/revision commutation
theorem (listed above, not attempted). **CANNOT_CHECK:** that the Lean `Interval` is the runtime's
`WarrantProfile` as the solve loop uses it; `DecidableEq` of the OCM id universe. Row stays open.

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

After batches 8–10 the rows with a disposition are FDX-01/02/03/04/05/06/07/08/11/13/14/15; untouched: FDX-09, 10, 12, 16. The one open conjecture is FDX-15's general equivalence; batch 10's open items (graded / probabilistic trust, truthful revelation, coded redundancy / infinite classes) stand.

After batch 12, FDX-16 carries a disposition (PROVED in Lean for the warrant core; typed terminals and the representation/revision commutation theorem remain OPEN on that row).

`GENERAL_NOVELTY = NOT_ESTABLISHED`. `FIELD_STATUS = NOT_ESTABLISHED`.

Batch 13 disposition (field map, `../MACHINE_EPISTEMICS_FIELD_MAP_V1.md`, checker
`../kso_field_map_v1_exact.py`, derived registry `../OCM_OBLIGATION_REGISTRY_DERIVED_V1.json`; NOT sealed):
**first version of the field closed by consolidation, no new theorem.** The map is derived by the checker
from batches 1–11 (exit 0 on billy-old, `"status": "CONSISTENT"`, 7/7 planted mutants caught, no-alarm
control passes, 11 tests): 77 theorems (PROVED 48, PROVED (finite) 16, PARENT_OWNED 7, PARENT_SUFFICIENT 4,
CONJECTURE 1, OPEN 1; parent-owned or parent-sufficient as primary status 11, as any mention 33), 22 exactly
bounded impossibilities, 3 conjectures each with an executable or stated falsifier, 7 current OPEN items (all
flagged NO_EXECUTABLE_FALSIFIER: FD-07 general, FDX-06/07/14 residues, FDX-09/10/12 residues), 6 CANNOT_CHECK
items, 10 open halves of batches 2–6 closed by a later batch, 22 KS-T ids cited (21 resolve, KS-T14 flagged as
a contract id without a registry row), 66 OCM registry rows linked (52 discharged, 14 left open), and the
derived obligation registry KS-T118–T141 (4 existing rows kept, 20 new rows KS-T122–T141, all OPEN). Batch 12
(FDX-16, Lean core) is a marked slot the checker fills from `KSO_MECHANISED_CORE_BATCH12_V1.md` once it is on
main. Rows with a disposition after batches 8–13: FDX-01/02/03/04/05/06/07/08/09/10/11/12/13/14/15; FDX-16 per
batch 12. Thirteen non-fatal inconsistencies in the earlier batches are listed in the map's §9 (none fixed).
`GENERAL_NOVELTY = NOT_ESTABLISHED`. `FIELD_STATUS = NOT_ESTABLISHED`.
