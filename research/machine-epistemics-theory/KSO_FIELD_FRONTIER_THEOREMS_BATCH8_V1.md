# KSO field-frontier theorems — batch 8 (H1–H4)

Date 2026-09-05. Eighth one-day batch, the first of the field-completion programme (ORION-V2 #353) over
the Machine Epistemics field frontier (`field_dynamics_v1/FRONTIER.md`). Scope: four frontier rows —
FDX-01 open-system epistemic closure (H1), FDX-02 controlled epistemic viability (H2), FDX-03
information/interface conservation (H3), FDX-05 reversible and irreversible epistemic transitions (H4).
Each row is closed as PROVED on a finite fixture, bounded exactly (an impossibility with a witness), or
PARENT_SUFFICIENT / PARENT_OWNED with the executable rule and its falsifier. The FDX ids are kept.

Every item has an exact finite checker (`kso_field_frontier_batch8_exact.py`, stdlib only; every count an
integer, every probability an exact `Fraction`; exit 0 / 1 / 2 with 2 = CANNOT_CHECK), at least one planted
hostile whose mutation is asserted applied and caught, and a no-alarm control;
`tests/unit/test_kso_field_frontier_batch8.py` pins every count. Checker run on billy-old (Python 3.14.4):
exit 0, wall 2.2 s, `"status": "ALL_HOLD"`, `"OPEN"` = the FD-07 general principle only; 9/9 new tests;
batches 5–8 together with the batch-6 revision-boundary suite 65/65. All objects are re-implemented inside the checker (dependency closure, a
finite-horizon controller/environment game, deterministic channels as partitions of a 16-hypothesis class,
an append-only ledger with a LIFO component stack); nothing imports `ocm`; nothing ran on the Mac.

NO NOVELTY OR SUPERIORITY CLAIM. Every fixed-point, game-theoretic, information-theoretic or
transactional fact used is a named parent's; the contribution is the exact statement on the registered
objects of `FIELD.md`, the executable falsifier, and the reading of what the OCM code and the M12 V4 inputs
can and cannot support. Rigour follows the batch-6 integration review: guaranteed identification, never an
accusation from a correct answer; ceilings stated for the registered algorithm only; no scalar over-claims.

Notation as in batches 1–7 and `FIELD.md`: registered state `Ξ = (K, Λ, D, N, A, S, P, H, O, 𝔠, B, X)`,
semantic projection `π_sem(Ξ)` (omits history `H`, cost `B`, traces `X`), liveness LIVE / UNKNOWN / DEAD,
transition families F / E / L / R / M / G. `[φ]` is the indicator of `φ`.

## H1 · FDX-01 · open-system epistemic closure: the weakest checkable interface, and the exact impossibility below it

**Objects.** A registered dependency description `D` over environment roots `x1, x2, x3`, an internal claim
`a` and the conclusion `c` (all-tails conjunctive dependence; 128 descriptions). `Roots_D(c)` is the
backward dependency closure of `c` restricted to roots (least fixed point over `D`). The environment is a
valuation `σ` of the roots with unmodelled transitions: it may flip any root of a set `F ⊆ {x1,x2,x3}`
(8 environments, every flip trajectory of length ≤ 2). A *coverage* assigns each root MONITORED (a
registered synchronous observation channel that fires on change), FROZEN (a registered, revocable
invariance assumption whose id enters the certificate) or UNCOVERED (27 coverages). The *registered view*
`ρ(σ)` is the tuple of monitored values — everything the machine can read. The *closure certificate*
`cert_D(c)` is MONITORED_CURRENT if every root is monitored, CONDITIONAL_ON_ASSUMPTIONS (listing the
frozen ids) if every root is monitored or frozen, NO_CLOSURE otherwise. The reported value of `c` reads
monitored roots and takes frozen and uncovered roots at their registration value.

**Theorem** (128 × 27 = 3 456 (D, coverage) pairs × 8 environments; 154 688 covered checks). (i)
*Weakest interface, conditional reading.* The reported value of `c` agrees with its actual validity at every
reachable environment state on which the frozen assumptions hold **iff** every root of `Roots_D(c)` is
covered (3 456/3 456): MONITORED_CURRENT certificates are sound unconditionally (75 712 checks),
CONDITIONAL certificates are sound as implications (78 976 checks). (ii) *Unconditional current validity*
is sound iff every root is monitored (3 456/3 456); a frozen root flipped by the environment makes the
unconditional reading wrong on 22 224 trajectory states while the conditional claim stays true. (iii)
*Exact impossibility below the interface.* For every NO_CLOSURE pair (1 727 of 3 456) the environment that
flips one uncovered root produces two states with identical registered view and different validity of `c`;
hence **no function of the registered state** is a sound current-validity claim — not a weaker interface,
not a smarter monitor, nothing that reads only `ρ`. Smallest witness: `D = {c ← x1}`, `x1` uncovered.
(iv) *Closure is relative to `D`.* A certificate computed over the direct tails only (the transitive root
through `a` unmodelled) certifies 271 pairs the honest certificate refuses; each has the witness of (iii).
Dependency completeness of `D` is a registered assumption of every certificate and `CANNOT_CHECK` from
inside (FD-03). (v) *Lagged monitors.* A monitor delivering with lag 1 supports the claim "valid as of the
last delivered epoch" (29 100 checks) and not "valid now": the current reading fails on 13 128 trajectory
states where the root flipped inside the lag.

**Proof.** (i)–(ii) by enumeration; the "if" direction is the definition of the reported value (monitored
roots read, frozen roots true by hypothesis), the "only if" is (iii). (iii) `ρ(σ0) = ρ(σ1)` because the
flipped root is not monitored, `c` valid at `σ0`, invalid at `σ1` because all-tails dependence needs every
root; any function of `ρ` returns one value on both. (iv) the omitted root is a root of `Roots_D(c)` and
uncovered. (v) by construction of the lag. ∎

**Hostiles.** `mutant_current_validity_without_interface` (read the registered liveness as current validity
under NO_CLOSURE) is wrong on 49 200 of 179 608 states — caught. `mutant_roots_direct_only` (the
certificate that ignores the unmodelled transitive dependency) — 271/271 caught by the (iii) witness.
Reading a CONDITIONAL certificate as unconditional — 22 224 caught. Reading a lagged monitor as current —
13 128 caught. **No-alarm:** every MONITORED_CURRENT certificate is exact on every trajectory (75 712/75 712);
the 9 root-free conclusions are closed vacuously.

**Status.** PROVED (finite): the weakest checkable closure interface is *cover every dependency root of the
conclusion, by a registered monitor or by a registered revocable assumption* — necessary by (iii),
sufficient by (i); the unconditional form needs monitors on every root. Below the interface the
current-validity guarantee is an EXACTLY_BOUNDED_IMPOSSIBILITY with witness. The interface itself is
PARENT_OWNED: it is the assumption set of assume-guarantee reasoning (Pnueli 1985; Alur–Henzinger 1999,
reactive modules), the monitorability boundary of runtime verification (Bauer–Leucker–Schallhart 2011), the
assumption nodes of the ATMS (de Kleer 1986) and the closed-world assumption (Reiter 1978); robust /
module checking (Kupferman–Vardi) owns the open-environment quantifier. What is registered here is only
the typed certificate (MONITORED_CURRENT / CONDITIONAL / NO_CLOSURE with the assumption ids and the
`D`-completeness premise) and the two readings it separates (FIELD distinction 6, historical replay ≠
present validity). **Tightened:** FRONTIER's "or prove that no nontrivial current-validity guarantee exists
without such an interface" — both halves hold: the interface exists and is checkable from `D`, and below it
the impossibility is exact; the two are the same theorem read in two directions.

## H2 · FDX-02 · controlled epistemic viability: the kernel is the parent's; the typed interface gives its closed form and separates commit from closure

**Objects.** Epistemic state `s = (w, a, k, r, q, b, t, ρ)`: warrant `w ∈ {LIVE, UNKNOWN, DEAD}`, commit
authority `a ∈ {0,1}`, scope `k ∈ {IN, OUT, OUT_FINAL}`, risk `r ∈ {LOW, HIGH}`, whether a registered
observation channel exists for the warrant `q ∈ {0,1}`, budget `b ≤ 6`, time `t ≤ T = 6`, declared revision
envelope `ρ ≤ 2` tokens (10 584 states). Controller moves (cost, one time unit each unless terminal):
`query` (1; enabled iff `w = UNKNOWN ∧ q = 1`), `experiment` (2; enabled iff `w ≠ LIVE` — the intervention
channel, the only acquisition on DEAD), `observe` (1; `r := LOW`), `clarify` (1; enabled iff `k = OUT`),
`wait` (0), `abstain` (terminal; *licensed* iff `w = DEAD ∨ a = 0 ∨ k = OUT_FINAL`, otherwise a contract
violation), `act` (1, terminal; COMMITTED iff `w = LIVE ∧ a = 1 ∧ k = IN ∧ r = LOW`, otherwise VIOLATION).
The environment answers every information action (`query`/`experiment` → LIVE or DEAD; `clarify` → IN or
OUT_FINAL) and may then spend one envelope token: revoke a LIVE warrant or expire an IN scope. A pending
state at the deadline with no winning terminal is FAILED. `propose-representation-change` is excluded: it is
a G-proposal with no object effect inside the horizon (batch-5 E4). Two contracts: TYPED_CLOSE (reach
COMMITTED or a licensed ABSTAINED) and COMMIT (force COMMITTED). Both kernels are computed by exact
backward induction over the finite time-indexed game.

**Theorem** (10 584 states, both contracts; closed forms agree 10 584/10 584). Write `c_q = 1` if `q = 1`
else `2`, `c_w = c_q·[w = UNKNOWN]`, `n_w = [w = UNKNOWN]`, `c_k = n_k = [k = OUT]`, `c_r = n_r = [r = HIGH]`.
(i) *Typed-close kernel* (9 010 states):
`Win(s) ⟺ licensed(s) ∨ (complete(s) ∧ b ≥ 1) ∨ (a = 1 ∧ b ≥ c_w + c_k + c_r + ρ·c_q + 1 ∧ t + n_w + n_k + n_r + ρ ≤ T)`,
where `complete(s)` is the commit predicate. Every failing predicate is repaired by exactly one typed action
at a known cost, authority by none, and each envelope token forces one re-warrant at cost `c_q` (the
environment spends a token only in response to the move that completes the predicates, so an
already-complete state commits regardless of `ρ`). (ii) *Commit attractor* (312 states):
`Commit(s) ⟺ a = 1 ∧ w = LIVE ∧ k = IN ∧ ((r = LOW ∧ b ≥ 1) ∨ (r = HIGH ∧ b ≥ 2 ∧ t + 1 ≤ T ∧ ρ = 0))` —
commit is forceable **only when no information action remains**: every query, experiment or clarification
hands the answer to the environment, and one envelope token after an observation forces such an action.
(iii) *Abstain trivialisation.* If abstain is always licensed the kernel is the whole space (10 584); the
1 574 states it adds are exactly the honest losses — FDX-02 has content only under a contract with an
unlicensed terminal. (iv) *The two contracts separate.* The indefinite-safety contract of FD-06 (no
deadline, `wait` available) has kernel = all 1 512 time-free states; the finite-deadline kernel is (i). (v)
By envelope: typed-close 3 132 / 2 986 / 2 892 and commit 144 / 84 / 84 at `ρ = 0 / 1 / 2`.

**Proof.** (i)–(ii) the game graph is time-indexed hence acyclic; backward induction is exact
(Zermelo/Bellman). Closed forms: the controller's repair sequence costs `c_w + c_k + c_r` and `n_w + n_k +
n_r` time units; the environment's best response to any information action is the answer that keeps the
game alive (a DEAD or OUT_FINAL answer licenses abstain), and each token, spent at a completion moment,
forces one re-warrant (cost `c_q`, one unit of time) — revocation dominates expiry since `c_q ≥ 1`; a
terminal act at time `t + time_need ≤ T` closes. For COMMIT, the environment answers every information
action against the controller. (iii)–(iv) fixed-point computation. ∎

**Hostiles.** `mutant_self_authorize` (an internal action that produces commit authority, FD-01 forgery):
its commit attractor contains 100 states with `a = 0`; the honest attractor none — caught.
`mutant_ignore_envelope` (kernel computed at `ρ = 0` against a declared `ρ ≥ 1`): over-claims 386 states;
the recorded witness plays its policy from `(LIVE, 1, IN, HIGH, q=0, b=2, t=0, ρ=1)` against the real
envelope and ends FAILED at the deadline after the token revokes the warrant it had just cleared to act on.
`mutant_abstain_always_licensed`: 1 574 losing states declared viable — caught. **No-alarm:** all 252
complete states with `b ≥ 1` are in both kernels at every envelope; the smallest losing UNKNOWN state with
one token is `(UNKNOWN, 1, IN, LOW, q=0, b=0, t=0, ρ=1)`.

**Status.** PARENT_SUFFICIENT — exactly as FRONTIER predicted. The kernel is the viability kernel / safety
attractor of a finite two-player game (Aubin 1991; Thomas 1995; Zielonka 1998; FD-06's `controlled_kernel`
with controller-then-environment order; finite-horizon backward induction). The typed predicate interface
adds no algorithm; it adds the *action-effect table* (which action repairs which predicate at which cost;
authority repaired by none; DEAD reached only by the intervention channel) from which the closed form (i)
follows, the *licensed-terminal contract* without which the kernel is trivial (iii), and the observation
(ii) that truth-warrant is not controllable — the FIELD distinction "truth warrant ≠ actionability ≠
permission" appears as three different kernels. Residual beyond parent: none claimed (PROVED corollaries
on the fixture, not new mathematics).

## H3 · FDX-03 · information/interface conservation: the deterministic typed fragment, exact

**Objects.** The class `H` of the 16 Boolean functions of two inputs; six registered channels, each a
deterministic response map hence a partition of `H`: four observations `obs_x` (value at input `x`), the
verifier `ver_affine` (degree ≤ 1; 8 functions), the verifier `ver_monotone` (6 functions). A *memory
replay* returns the transcript already held. The *join* of a channel set `S` is the common refinement of its
partitions (equivalently, the partition by transcripts). A *risk-typed* channel answers `obs_11` but the
adversary may flip one answer per transcript. The *class assumption* `A_aff` (registered id) restricts `H`
to the 8 affine functions. Decision-tree depth `D(V)` is the exact worst-case number of adaptive channel
uses that identifies every member of `V ⊆ H` (bitmask DP over all 65 535 nonempty `V`).

**Theorem.** (i) *Conservation, exact.* After any adaptive transcript over channel set `S` the version space
of the truth is its join class (64 sets × 16 truths); a channel reduces no reachable version space **iff**
it is a garbling of the join — a function of the transcript (Blackwell, deterministic case) — 384/384;
memory replay is such a channel on every one of the 533 (set, class) pairs: zero reduction. (ii)
*Identification needs a discrete join.* 12 of 64 channel sets identify all 16; the 5 minimal ones are the
four observations, and any three observations plus `ver_affine` — the parity verifier carries exactly the
information of the missing observation (`obs_11` is a function of `{obs_00, obs_01, obs_10, ver_affine}`).
Joins of `k` observations have `2^k` classes. (iii) *Query complexity.* `D(H) = 4 = ⌈log2 16⌉` with
observations only and with the verifiers added; on every `V`, `D(V) ≥ ⌈log2 |V|⌉` (65 535/65 535, tight on
62 234 of them); verifiers strictly lower `D(V)` on 2 571 subsets but never below the entropy bound (0).
(iv) *Typed scope.* For an affine truth and any observed input set `S` (128 cases) the inputs pinned
unconditionally are exactly `S`; the class assumption pins further inputs in 32 cases (e.g. three
observations pin the fourth); those inputs carry `A_aff` in their support and lose all warrant when `A_aff`
is revoked (32/32 collapse to `S`). (v) *Risk is not truth.* The risk-typed channel leaves the exact version
space unchanged (16/16) and yields a separate risk receipt; read as exact it eliminates the truth in the
error realisation for every truth (16/16). (vi) *Guaranteed-identification bound.* An arm that declares
channels `S` and *guarantees* zero-error identification over all of `H` has used at least
`⌈log2 L(S)⌉` undeclared bits, `L(S)` the largest join class: 4 with nothing declared, 1 with three
observations, 3 with the two verifiers only, 0 with the four observations. Observed correct answers on
sampled truths establish nothing (`IDENTIFICATION_NOT_ESTABLISHED`); the report carries the exact null
probability of the run under uniform guessing inside the declared classes — `1/2` for one success, `1/32`
for five — never an accusation. (vii) No channel carries commit authority; identification leaves it at 0.

**Proof.** (i) the version space is the transcript fibre; a channel constant on every join class is by
definition a function of the transcript. (ii)–(iii) enumeration; the entropy bound is pigeonhole on binary
splits. (iv) set arithmetic on version spaces. (v) construction. (vi) pigeonhole: to separate the largest
class the undeclared partition needs `⌈log2 L⌉` binary answers; a success on a class of size `n` has null
probability `1/n`. ∎

**Hostiles.** `mutant_memory_is_information` (charges a replay as a reduction) — 533 predicted reductions,
all 0. `mutant_class_scope_unconditional` (extrapolated inputs kept LIVE after `A_aff` is revoked) — 32/32
caught. `mutant_risk_as_exact` — 16/16 caught. `mutant_single_success_is_proof` (the batch-6
integration-review correction: one correct answer beyond the declared join read as an undisclosed channel)
— caught; the honest verdict is `IDENTIFICATION_NOT_ESTABLISHED` at null probability `1/2`. **No-alarm:**
the four observations identify with bound 0, `D = 4`, and full unconditional scope.

**Status.** PROVED (finite, deterministic, typed fragment): reduction of exact uncertainty equals the join
of the channels used; garbled channels (memory, repeated tests, coarser verifiers) add nothing; model
restrictions are charged as assumption ids in the support; risk-typed channels never enter the exact
lattice; identification guarantees are bounded by the declared join and observed success is never
evidence of a channel. The mathematics is PARENT_OWNED: decision-tree / query complexity (Buhrman–de Wolf
2002), Blackwell's comparison of experiments (1953; deterministic garbling = coarsening), version spaces
(Mitchell 1982), teaching dimension (Goldman–Kearns 1995; the numbers on ALL16 / AFFINE8 are batch-4 D2's),
batch-6 F8's counting bound (extended here from "k examples" to arbitrary channel joins with verifiers and
memory). **FD-07 stays OPEN_RESEARCH**: the graded, continuous, adaptive-prior principle FRONTIER asks for is
not promoted by this finite fragment, and the pointwise realised reduction may still exceed the expected
bound (FD-07's rare-outcome refutation stands). **Tightened:** FRONTIER's "distinguish exact truth,
distributional risk, upper/closure evidence and action authority" is met by (iv)–(vii) only for
deterministic channels; the distributional coordinate is typed and separated, not bounded.

## H4 · FDX-05 · reversible and irreversible transitions: an exact four-way classification on the ledger fixture

**Objects.** A registered state with evidence ids `{e1, e2, e3, s0}`, atoms `a` (alternatives `{e1}`,
`{e3}`) and `b` (`{e2}`), component table `C, D = art0`, a DPO edge `R` stamped `s0`, an empty quarantine, an
append-only history and a cost meter. Transitions: admit (fresh id), revoke, reinstate, relearn (admit a
fresh id for an atom), delete (identity loss), quarantine / release, adopt (component artefact with a fresh
stamp; the whole component table is snapshotted on a LIFO stack), rollback (top of stack only: restore the
snapshot, revoke the stamp), act (external effect), DPO rewrite `R → R'` with a fresh stamp (the old stamp
revoked). `π_sem` = (active ids, identity registry, Λ, quarantine, components, stack, edges, world);
`B_now` = current answers (atom liveness incl. QUARANTINED, component table with stamp liveness, live edge
shapes, external effects); `B_future` = `B_now` after revoking each identity of the *original* registry
(the future-revision probe, FIELD distinction 9). A transition (sequence) is classified by the best LIFO
product of its registered inverse candidates (the identity move included): **ESI** if `π_sem` is restored;
**BOI_STABLE** if `B_now` and `B_future` are restored but `π_sem` is not; **BOI_DIVERGENT** if only `B_now`
is restored; **NI** if no candidate restores `B_now`.

**Theorem** (12 single transitions; 142 sequences of length 2; 1 667 of length 3). (i) *Singles.* revoke
(×4) and quarantine are ESI (inverse reinstate / release); admit and adopt are BOI_STABLE (the inverse
restores behaviour and the whole future-revision probe, but the new identity persists in the registry —
dead — so `π_sem` is not restored); deleting a redundant identity (`e3`, `a` stays LIVE via `e1`) is
BOI_DIVERGENT (currently invisible, divergent under a future revocation of `e1`); the DPO round trip is
BOI_DIVERGENT (shapes restored, stamps fresh: revoking the original stamp no longer does anything); deleting
the only support (`e2`) and acting are NI. (ii) *Relearn is not reinstatement.* From the revoked state,
reinstate is ESI and relearn is BOI_DIVERGENT: current answers equal, `π_sem` and the future probe differ.
(iii) *Composition.* If every component is ESI the LIFO composite inverse is ESI (150/150), and an ESI
composite has only ESI components (150/150) — an identity-creating step anywhere in the sequence destroys
exactness; any sequence containing an external act is NI (414/414). Histograms: length 2 — ESI 25,
BOI_STABLE 44, BOI_DIVERGENT 34, NI 39; length 3 — 125 / 494 / 465 / 583. (iv) *The full state is never
restored.* Every ESI inverse leaves the history strictly longer and the cost higher (5/5 singles; asserted on
every chain): FD-05's refutation of full-state reversal holds on every transition of the fixture. (v)
*LIFO.* With two adoptions the rollback of the non-top one is refused (`ROLLBACK_OUT_OF_ORDER`); the LIFO
pair restores the table exactly (object-coordinate exactness) while the round trip is BOI_STABLE on `π_sem`
(the dead stamp persists in the registry). (vi) *Identity loss is invisible to the projection.* A deleted
identity re-minted under its old name restores `π_sem` byte-for-byte; only the append-only history (in the
OCM, the hash chain) witnesses the loss, and the registry rule "an id that appears anywhere in the history
is taken" refuses the re-admission.

**Proof.** Enumeration over the registered inverse table; (iii) because every identity-creating transition
grows the registry, which no registered transition shrinks except delete, and delete is never an inverse
candidate; (iv) history append is the definition of a transition. ∎

**Hostiles.** `mutant_classify_by_current_behaviour` (any inverse restoring current answers reported as
exact): on the route where reinstatement is impossible (`revoke e2`, `delete e2`) the only inverse is relearn
— honest BOI_DIVERGENT, mutant ESI — caught. `mutant_history_rewind` (full-state equality asserted after an
ESI inverse) — refuted 5/5. `mutant_out_of_order_rollback` (restore the non-top snapshot in place): leaves
D's stamp active over a table showing `D = art0`, and the subsequent rollback of D resurrects `C = art1` —
caught (witness recorded). `mutant_readmit_deleted` — refused by the registry/history rule; the projection
alone would not have caught it (vi). `mutant_stamp_transitive_inverse` (the inverse DPO rewrite claimed to
restore the original stamps) — caught: shapes equal, stamps differ, `s0` dead. **No-alarm:**
revoke → reinstate and quarantine → release are ESI; the single LIFO adopt → rollback restores the table
exactly.

**Status.** PROVED (finite classification) / PARENT_OWNED: append-only log with projected state is event
sourcing; LIFO undo of table snapshots is transactional rollback (Gray–Reuter 1993; ARIES, Mohan et al.
1992); "current beliefs recovered, provenance not" is the AGM recovery postulate (Alchourrón–Gärdenfors–
Makinson 1985) read against provenance identity (Green–Karvounarakis–Tannen 2007); reversible computation
(Bennett 1973) is the parent family for exact inverses — no thermodynamic language is used or needed.
FD-05 (PROVED_SCOPE_LIMITED on revoke/reinstate) is extended to the four classes and to sequences; batch-6
F5 (rollback artefacts lost across restart) is the NI-by-artifact-loss case. **Tightened:** FRONTIER's
three classes split BOI into stable and divergent, and the divergent case is detected only by the
future-revision probe — current behaviour never separates reinstate from relearn.

## Consequences for the OCM build (read-only observations on `ORION-OCM-wt/m11-self`; nothing touched)

File states read on 2026-09-05. Each item names the runtime obligation the theorem makes concrete; none is
a claim about an M12 result.

* **H1 — the closure interface has no runtime object; the commit gate reads scope without an epoch.**
  `src/ocm/kso/revocation.py::impact_cone` (line 127) and `is_dependency_closed` (line 147) compute the
  forward cone and set-closure over `D`; the backward root set of a conclusion and the per-root coverage
  (monitor channel vs revocable assumption) are not represented. `src/ocm/kso/types.py::Scope.covers`
  (line 207) skips the epoch test when `at` is `None` (line 210), and
  `src/ocm/runtime/solve.py::commitment_gate` (line 377) calls `op.scope.covers(task.context)` without
  `at` — an epoch-bounded scope is committed on context alone, the H1 (iii)/(v) reading of registered
  liveness as current validity. Obligation: pass the evaluation epoch, and type the commitment receipt
  MONITORED_CURRENT / CONDITIONAL_ON_ASSUMPTIONS (assumption ids listed) / NO_CLOSURE, with the
  `D`-completeness premise named (the `is_dependency_closed` result is that premise for the cited set).
* **H2 — reason-typed abstention; no envelope, risk or budget coordinate at the gate.**
  `src/ocm/runtime/solve.py::Decision` (line 52) is the licensed-terminal set; `decide` returns
  `Decision.UNKNOWN` with reason `"UNKNOWN"` (line 353) — an abstention without a registered reason class
  (H2's unlicensed terminal). `commitment_gate` (lines 368–378) checks trace cleanliness, LIVE warrant,
  authority meet and scope; no risk or resource predicate and no declared revision envelope exist at the
  gate. Obligation: abstentions carry a reason from a registered set; if a viability claim ("will close by
  T") is ever made, the envelope and budget/deadline become state coordinates and the closed form (i) is
  the check; a promise to *commit* by T is unlicensed while any information action is pending (ii).
* **H3 — the information-budget receipt should charge the join, the assumption ids and the verdict type.**
  `src/ocm/store/evidence.py::Channel` (line 31) registers eight channels and
  `src/ocm/kso/admission.py::WARRANTING_KINDS` (line 39) excludes FEEDBACK — the typed rule that a
  feedback channel reduces nothing exactly (batch-3 C6). `src/ocm/runtime/state.py::EventStore.replay`
  (line 103) is a garbling: replay supplies no information (H3 (i)). Batch-4 D2's
  `INFORMATION_BUDGET_RECEIPT` should record the join of channels used, the model-restriction assumption
  ids (H3 (iv)), and one of the two verdicts of (vi); the M12 V4 report's reference-arm reading (§4, "the
  unbound pretraining channel, visible only because the world-true half was added") is a declared-channel
  statement under G7's licence grading and is consistent with (vi) as such — it is not, and the report does
  not call it, an identification guarantee.
* **H4 — the ledger already realises the classes; receipts should name them.**
  `src/ocm/runtime/state.py::EventStore` (line 100) is append-only and hash-chained (history NI by
  construction); `RuntimeState.apply` REVOKE/REINSTATE (lines 84–85) is the ESI pair.
  `src/ocm/selfmodel/govern.py::AdoptionLedger.rollback` enforces LIFO (`ROLLBACK_OUT_OF_ORDER`, line 434),
  matching hostile (v); its `exact` flag (line 449) is object-coordinate exactness with the stamp DEAD — H4
  classifies the adoption round trip BOI_STABLE on `π_sem` and ESI on components/cache, so the receipt
  should say `EXACT_ON_OBJECT_COORDINATES` rather than "exact". `CANNOT_CHECK_ROLLBACK_ARTIFACT_UNAVAILABLE`
  (line 429) is NI by artefact loss (batch-6 F5). `src/ocm/selfmodel/replay.py` S24 ("identical bytes
  deduplicate onto the revoked id") is the reinstate-vs-relearn boundary of (ii): the `stamped` / `lineage`
  fields written at govern line 404 are where ESI vs BOI_DIVERGENT must be legible. The runtime has no
  delete; H4 (vi) says any future compaction must keep the history as the witness of identity loss.
  `src/ocm/kso/admission.py::AdmissionReceipt.quarantined` (line 54) is the ESI quarantine coordinate.

```text
H1  FDX-01  PROVED (finite): interface = cover every dependency root (monitor | revocable assumption); unconditional ⇔ all monitored; below it EXACTLY_BOUNDED_IMPOSSIBILITY (view-identical witness, 1 727); closure relative to D; PARENT_OWNED interface
H2  FDX-02  PARENT_SUFFICIENT (finite-horizon safety/reachability game); PROVED corollaries: closed form 10 584/10 584, commit attractor = no information action pending (312), abstain trivialisation, deadline vs indefinite contracts separate
H3  FDX-03  PROVED (finite deterministic typed fragment): version space = join class; garbling adds nothing (memory 533); parity verifier = missing observation; D(H) = 4 = entropy bound; scope charged to assumption ids (32); risk never exact; identification bound ⌈log2 L⌉, success ≠ channel; FD-07 general OPEN
H4  FDX-05  PROVED (finite classification): ESI / BOI_STABLE / BOI_DIVERGENT / NI on 12 singles, 142 + 1 667 sequences; all-ESI ⇔ ESI composite; act ⇒ NI; full state never restored; identity loss invisible to π_sem, witnessed by history; PARENT_OWNED components
OPEN: FD-07 general information conservation (graded / continuous / adaptive prior)
NOVELTY NOT_ESTABLISHED
```
