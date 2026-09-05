# KSO self-model-prerequisite theorems — batch 5 (E1–E8, residual halves R1–R3)

Date 2026-09-05. Fifth one-day batch over the machine-epistemics gap atlas
(`ME_THEORY_GAP_ATLAS_V1.md`), chosen as the gaps the OCM M11 milestone (ORION-of-ORION: governed
self-modelling, diagnosis, obstruction certificates, self-change proposals, shadow assurance, external
adoption, reopening and rollback — `ORION-OCM` issue #13) and M12 (lifetime evaluation, issue #14) need
proved or defined, plus the three halves batches 1–4 left open (MEG-19 deconsolidation, MEG-27 open
inventory, MEG-02 graded semiring). Every item has an exact finite checker
(`kso_self_model_prereqs_batch5_exact.py`, stdlib only; exit 0 / 1 / 2 with 2 = CANNOT_CHECK), at
least one planted mutant asserted applied and caught, and a no-alarm control; tests in
`tests/unit/test_kso_self_model_prereqs_batch5.py` pin every count. Checker run on billy-old: exit 0,
wall 1.4 s; 13/13 tests. Objects (antichain semiring, warrant intervals, Kleene liveness, authority
meet, frozen-denominator navigation with exact rational fixed points, impact cone, batch-1 T4
stamping / rollback, the batch-2 B7 consolidation fixture and B8 DPO rewrite on the M4 Boolean
fixture, the batch-1 T8 metered loop) are re-implemented inside the checker; nothing imports `ocm`.
NO NOVELTY OR SUPERIORITY CLAIM: every result is a corollary of KS-T01/T09/T19/T20/T21/T22, batches
1–4 and the named parents; the contribution is the exact statement, the executable falsifier and —
where the requested wording could not be proved as written — the tightened wording, marked
**tightened** below. Objects are named to match `ORION-OCM` `src/ocm/selfmodel/{model,diagnose,
proposal,govern}.py` (read only; nothing there was touched).

Notation as in batches 1–4: ⊕ join, ⊗ meet, ⟦ℓ,u⟧ warrant interval, Λ(x) the interval of atom x, R the
revoked set, λ_R ∈ {LIVE, DEAD, UNKNOWN}, Γ a revocation family, Q the registered query family,
a*_{Q,R} the restart fixed point (α = 1/3), Impact_D the KS-T09 cone, 𝔠 = (Check, Authority, Meter,
Commit) the external constitution. E_obj / E_self are the evidence supports of the object fibre and of
the self-model fibre K_self (scope `task` vs scope `self`; disjoint).

## E1 · MEG-29 (extension of batch-1 T7) · the self-model fibre carries no self-authority

**Objects.** K_self is a fibre whose atoms are OBSERVATION / derived records about the machine's own
runs (traces, receipts, failure evidence, benchmark results), supported on E_self, authority
A_self = {self_model: 1} (world_truth 0, commit 0 — batch-1 T1 undeclared = bottom), scope `self`.
Rule E1(i): an edge with a K_self tail may only have K_self heads (a diagnosis *proposes*; it never
derives an object-level atom). A self-change proposal is a K_self atom p with interval ⟦0, U_p⟧
(U_p = its trigger evidence ⊗ its prediction record, both in E_self) and authority {proposal: 1}.
`adopt(p, receipt)` admits the adopted-change atom ⟦{{e_A}}⟧ ⊗ U_p only for a receipt with
commit ≥ 1 and source *external*.

**Theorem.** (i) Non-interference, both directions: for every object atom x and every R,
λ_R(x) = λ_{R ∩ E_obj}(x) and the object-fibre fixed point is identical with and without K_self (30
random spaces × 2^|E_obj| × {∅, revoke a trace}: 2 832 liveness and 472 activation checks); a query
seeded in K_self activates no object atom (30/30). (ii) No atom of K_self raises the authority or the
warrant of an atom outside K_self: an internal composition with a K_self tail has world_truth 0 and
commit 0 (meet), and a K_self record is refused as a closure certificate on an object claim because
its scope `self` does not meet the task scope (batch-4 D3(iii) shape), so the claim's verdict is
untouched. (iii) A proposal is never LIVE under any R (lower profile 0; 8/8 revocations) and becomes
LIVE only through an external commit receipt; it dies with that receipt or with its trigger evidence.
**Mutants** `mutant_self_edge_into_object` (a diagnosis as SUPPORT tail of an object claim: refused by
the rule, and if applied a self-seeded query activates the object atom, 30/30),
`mutant_self_record_raises_world_truth` (max instead of meet: world_truth 1, commit 1),
`mutant_self_diagnosis_promotes_object` (a self record used as closure: flips an UNKNOWN object claim
to DEAD under {e0}) and `mutant_adopted_by_own_prediction` (the prediction record as adoption
evidence: LIVE with self evidence only) caught; no-alarm: an EXPERIMENTATION certificate on the task
scope does close the same claim, and an external receipt does adopt. Parent: reference monitor /
Biba low-water-mark (verified), Gödel machine (Schmidhuber, verified) for "proof outside the
proposer"; batch-1 T1/T5/T7 (PROVED). Nothing new: this is T5(ii) with Σ = ∅ plus T1 on the
K_self boundary.

## E2 · M11 §3 · diagnostic-layer soundness on a finite trace grammar

**Objects.** A typed trace of a failed run: stage verdicts `complete ∈ {T,F}`, `resource`,
`authority`, `drift` (scope epoch ended), `info` (a registered input missing), `order`, `router`,
`operator`, `adapter`, plus the registered lower-level alternatives {router_alt, operator_alt,
adapter_alt} each untried or (warrant ∈ {LIVE, DEAD}, succeeded ∈ {T,F}), and a ceiling witness flag:
2⁹ · 5³ · 2 = 128 000 traces. `certificate_valid` (E3's content) := every alternative tried ∧ none
succeeded ∧ every attempt warrant LIVE ∧ witness. `classify(trace)` is a pure function of the trace:
CANNOT_CHECK (incomplete) → RESOURCE → AUTHORITY → DRIFT → MISSING_INFORMATION → BAD_ORDER →
REPRESENTATION iff the certificate is valid → WRONG_OPERATOR / OPERATOR_WRONG / BAD_ADAPTER →
INSUFFICIENT_EVIDENCE (all stages nominal, no certificate: gather evidence, never escalate).

**Theorem** (exhaustive, 128 000 traces). (a) REPRESENTATION ⇔ the six non-method stages are nominal
∧ the certificate is valid (8 traces); (b) every METHOD verdict (1 743) has an invalid certificate;
(c) the verdict is replay-invariant under serialisation (1 267 sampled); (d) the two hostiles:
`mutant_repeated_failure_escalates` (frequency ≥ 3 without a certificate ⇒ REPRESENTATION) sends 800
traces to a Jump in which *restoring the operator solved the task* (the M11 §4 hostile "disable a
local operator"); `mutant_ignore_certificate` (the run's own method fields read first) blames method
on all 7 REPRESENTATION traces whose failed run also shows a method symptom. Both caught; the mutants
agree with the honest verdict on the 126 000 traces of the six non-method classes (no alarm). (e) S5
false structural alarm: a missing dependency with a valid-looking certificate is
MISSING_INFORMATION. **Tightened**: the requested wording "METHOD only when the ceiling is absent"
is proved as *the certificate dominates the run's own method fields*, because a valid certificate
contains the method attempts (the repaired operator was tried, LIVE, and failed); the run's method
symptom is then not the responsible layer. Frequency is not an input of `classify`. Parent: fault
localisation by ablation / delta debugging (Zeller 2002; candidate, unverified); KS-T19's
four-valued discipline (OBSTRUCTION only under a ceiling) is the rule — PARENT_OWNED for the object,
the OCM contribution is the finite grammar with the two hostiles as exact counts.

## E3 · MEG-28 / M11 §4 · obstruction certificate content = the precondition of a governed Jump

**Objects.** `ObstructionCertificate(Q, R, witness)` on the M4 Boolean fixture: the registered
operators under representation R are the feature tables, compositions are the XOR-span; the
certificate is issued iff every composition fails on every q ∈ Q, every registered feature's warrant
is LIVE under the current revocation, and a checkable ceiling witness exists (parity: every
composition has even weight, q odd). `trigger_from_certificate` builds the B8 trigger
(EXPRESSIVE_CEILING, witness ids) from the certificate and nothing else.

**Theorem.** (i) Over all 16 targets × 8 revocations of {r1, r2, r3}: the B8 DPO Jump applies iff the
certificate reads OBSTRUCTION (128/128); exactly the 8 odd-weight tables under R = ∅ are obstructions
(AND among them), XOR ∈ affine span is LOWER_LEVEL_SUFFICIENT, and after the Jump AND is reachable.
(ii) A dead-warrant failure is not an obstruction: with feat_b revoked, XOR is unreachable from
{1, a}; the honest certificate says REINSTATE_FIRST (dead: feat_b) and the Jump is refused;
`mutant_certificate_without_live_clause` certifies OBSTRUCTION — caught; reinstating feat_b makes
XOR reachable. (iii) `mutant_partial_enumeration` (depth-1 operators only, no compositions)
certifies XOR falsely — caught; the AND certificate names 8 compositions tried and its witness.
No-alarm: a family inside the span never yields a certificate. **Tightened**: "every registered
operator composition" must be an *enumeration of the registered composition closure* (here the
span), not a list the proposer supplies; the LIVE clause is what separates an obstruction from a
revocation (S5). Parent: BMC completeness thresholds / CEGAR (verified) for "all lower-level
alternatives exhausted"; B8 (PROVED) for the Jump; KS-T19 (PROVED).

## E4 · M11 §5/§8/§10 · proposal object, pre-outcome prediction, adoption on unseen tasks

**Objects.** A proposal names its change class (C0 parameters … C5 organisation; C6 constitutional =
recommendation only), target, the proposer's dev tasks, and a prediction: an effect vector on frozen
held-out families plus a pre-registered margin, hashed before outcome access. `adopt_decision`
returns ADOPT iff class ≠ C6 ∧ target not protected (adoption./assurance./constitution./meter./
authority.) ∧ token external ∧ prediction digest = the pre-access digest ∧ the realised tasks are
disjoint from the dev tasks ∧ |realised − predicted| ≤ margin on every family. The proposer's own
evaluation is accepted as an argument and never read.

**Theorem** (exhaustive over 2 families, predicted and held-out deltas in −2…2, dev deltas in
{−2, 0, 2}, margins {0, 1}: 11 250 cases). (i) The decision equals the specification predicate
written independently (11 250/11 250; 1 746 adoptions). (ii) Syntactic non-dependence on the
proposer's score (11 250). (iii) Self-adoption (internal or absent token) and a prediction written
after the outcome are refused (11 250). (iv) `mutant_graded_on_dev_tasks` adopts in 1 080 cases the
held-out result refutes (and refuses 1 376 the held-out confirms) — caught; the memorising
challenger (dev +2, held-out −1, predicted +2) is refused honestly and adopted by the mutant. Held-out
tasks the proposer saw are refused as held-out; C6 and protected targets are refused regardless of
outcome; an honest realised prediction is adopted (no alarm). **Tightened**: "adoption iff the
external adopter confirms the prediction" needs the *disjointness* clause as part of the rule (a
proposal object must carry its dev-task ids), otherwise the mutant is undetectable from the
outcome table alone. Parent: pre-registration and hold-out evaluation (batch-4 D1, PARENT_OWNED);
batch-2 B8(iii) external commit (PROVED).

## E5 · M11 §9 · shadow execution non-interference and the assurance receipt chain

**Objects.** A live stream of tasks; the incumbent writes the object store and the external
commitment log; a shadow runs the challenger on the frozen snapshot after each incumbent step and
writes only a receipt to K_self: (index, task, snapshot digest, both answers, the *same* hard gates
applied to the challenger's answer, previous receipt hash) — a hash chain.

**Theorem** (30 random streams, 125 receipts). (i) The object-store digest and the commitment-log
digest are identical with and without the shadow (30/30); K_self grows by one receipt per task.
(ii) Every receipt's snapshot equals the incumbent-only state at the same index (replay, 125/125).
(iii) Assurance is the chain: every receipt carries the gate verdicts of the shared gates and the
chain verifies; `mutant_edit_receipt` (a gate verdict flipped after the fact) breaks it (30/30).
**Mutants** `mutant_shadow_writes_object` (the challenger's answer overwrites the incumbent's:
object digest differs on every stream where the operators disagree, 30/30) and
`mutant_shadow_commits_externally` (commitment log differs, 30/30) caught; a stream on which the
two operators agree everywhere is the no-alarm case. Parent: Goguen–Meseguer noninterference
(candidate, unverified) — the theorem is the finite, by-construction half (the shadow has no write
capability outside K_self, F10 ocap); hash chains / append-only logs (classic). This is E1(i)
applied to the runtime: the shadow *is* a K_self writer.

## E6 · MEG-18 / MEG-28 / M11 §11–12 · adoption as a stamped DPO rewrite; exact rollback with caches

**Objects.** Adoption = the B8 DPO rewrite L ← I → R on the M4 fixture with every produced object
(R ∖ I, and anything later derived from it) stamped with the adoption evidence e_A (batch-1 T4), a
compiled cache (which goal tables are FOUND under the current representation), and a cached
conclusion derived from the produced procedure. Rollback = revoke e_A, quarantine every object
whose evidence contains e_A, apply the inverse rewrite, recompile the cache.

**Theorem.** (i) The produced objects are exactly {feat_ab, phi_quad, h_0001,
cached_and_conclusion}; the 16 interface / untouched atoms keep their intervals (B8(i)). (ii)
Revoking e_A kills exactly the produced objects and the reopening obligation is their impact cone
{…, renderer, report, archive} (KS-T22); `unrelated` is outside. (iii) Rollback restores the
pre-adoption state *hash-identically* (space digest and cache), and the quarantined set equals the
produced set. **Mutants** `mutant_rollback_leaves_cache` (state digest differs; the cache still
answers FOUND for AND on the affine space — the M11 §18 hostile "rollback restores code but not
epistemic dependencies") and `mutant_rollback_without_revoke` (component-table rollback of the
rule's own R ∖ I without revoking e_A: the cached conclusion derived outside the rule's image
survives LIVE, digest differs) caught; an atom outside the cone is unchanged through adoption and
rollback (no alarm). **Tightened**: "reopens exactly the objects the change produced" is exact
only when *produced* is read through the evidence stamp (transitive), not through the rewrite rule's
image; the rule's image misses derived objects. Parent: DPO/adhesive (verified), ATMS context
switching (verified), batch-1 T4 and batch-2 B8 (PROVED).

## E7 · MEG-30 (extension of batch-1 T8) · meta-level termination and the livelock bound

**Objects.** The batch-1 T8 loop with proposals as the metered transitions: every proposal charges
δ > 0 from a registered schedule that may only *raise* the charge; the meter lies outside every
proposal's write set (a proposal targeting `meter.*` is refused); adoptions per lifetime window are
bounded by a window budget.

**Theorem.** (i) For budgets {1, 2, 3, 5, 8, 13, 21} × charges {1, ½, 2} the loop ends in
CANNOT_CHECK with at most ⌊B/δ⌋ proposals (21/21); (ii) adoptions per window ≤ the window budget
for windows 0…3 regardless of the outcome draws; (iii) a rising schedule terminates sooner than a
flat one. **Mutants** `mutant_proposal_sets_charge_zero` (refused as unmetered, KS-S7; the
protected-target rule refuses it before it runs) and `mutant_proposal_halves_future_charge`
(Σ δ/2^k < 2δ ≤ B: the loop never reaches the budget and livelocks at the cap of 60) caught; an
unreached window budget refuses nothing (no alarm). **Tightened**: the bound is ⌊B/δ_min⌋ with
δ_min the *registered minimum charge*; "a proposal may not lower the charge" is necessary — a
geometric schedule defeats the ranking function even though every charge is positive. Parent:
Floyd well-founded termination (verified); batch-1 T8 (PROVED).

## E8 · KS-T12 / KS-T14 improvement halves stated as CONJECTURES with exact falsifiers

Neither is claimed. Each is stated with its exact falsifier and the smallest fixture on which it
holds and the smallest on which it fails (both exist).

**KS-T12 (conjecture).** Consolidation improves future navigation cost on the registered Q.
Falsifier `falsify_ks_t12(k, Q)`: exact breadth-first edge count on the B7 chain s → x1 … xk → t
versus the consolidated s → m → t under batch-4 D7's rule (coarse first; a coarse GAP is
REFINE_REQUIRED and the fine walk runs too). Holds on the smallest chain with two internals (k = 2,
Q = {t}: 3 → 2; k = 1 gives 2 → 2, no improvement). Fails as soon as Q reaches a non-exported
internal (k = 1, Q = {t, x1}: 3 → 5; k = 2: 4 → 5; k = 3: 5 → 5; k = 4: 6 → 5 holds again). The
sign is Q-dependent; the conjecture cannot be a theorem without a clause on Q ⊆ exports.

**KS-T14 (conjecture).** A Jump improves the expressive ceiling on Q. Falsifier
`falsify_ks_t14(Q, R, R')`: |Q ∩ span(R')| > |Q ∩ span(R)|. Holds for Q = {AND}, affine → quadratic
(0 → 1; the whole family 8 → 16). Fails for Q = {XOR} (1 → 1: no change), and a lift can *lower* the
ceiling (R' = {1, ab} on Q = {XOR}: 1 → 0 — the S6 "harmful high-level Jump" shape). The
preservation half (B8) is proved; the improvement half is exactly "q ∉ span(R) ∧ q ∈ span(R')",
i.e. the E3 certificate plus a reachability check on R', which is a per-query fact, not a law.

## R1–R3 · the residual halves of MEG-19, MEG-27, MEG-02

**R1 · MEG-19 deconsolidation — PROVED (exactness half) / OPEN (decision).** `deconsolidate` on the
B7 fixture restores the constituent space byte-identically and every export's liveness over the 128
revocations of Γ is identical before, during and after consolidation (384 checks);
`mutant_deconsolidate_keeps_summary_edge` leaves a dangling summary edge (not the undo). Cost table
on the 3-chain (a fact, not a law): direct 4; through the macro 2 + one check per registered
exception, crossover at 2 exceptions. *When* to split (the MDL library choice) stays PARENT_OWNED
(DreamCoder/LILO) — there is no theorem of the warrant algebra that decides it.

**R2 · MEG-27 open inventory — PROVED for regular inventories / OPEN for non-regular
acceptability.** For an infinite inventory given by a DFA (NP (CONJ NP)* VP, 4 states) with a
regular acceptability predicate (claims LIVE, referents resolvable), `lookahead_regular` decides
prefix commitment by reachability, with no bound: over 13 prefixes × 16 discourse states × bounds
0…4, the batch-3 bounded check never contradicts it (879 decisive agreements), reachability decides
its 161 CANNOT_CHECK cases, the bound k = |states| is complete for SAT (208/208) but never reaches
UNSAT on the cyclic inventory (17 cases stay CANNOT_CHECK), and `mutant_bound_is_pass` commits 89
unsatisfiable prefixes. **Tightened**: batch-3 C3's "CANNOT_CHECK at the bound" is the right
discipline only for inventories where reachability is unavailable; for regular (and, by Bar-Hillel,
context-free — cited, not checked) inventories the exact decision exists. Acceptability that depends
on unbounded discourse state (counting referents) is the open remainder. Parent: Rabin–Scott /
reachability (classic) — PARENT_OWNED.

**R3 · MEG-02 graded semiring — OPEN, with a recorded witness.** No clean statement exists: (max, ×)
has no additive inverse, so revoking the top derivation requires recomputation over the survivors
(3/5), and "retraction by subtraction" is meaningless (0); (+, ×) counts a shared assumption twice
(1/2 vs the exact 3/8) where the antichain semiring reads DEAD. Exact-share retraction (KS-T04b)
therefore has no graded analogue without a new rule; batch-4 D3's certified-only gating remains the
OCM answer. Left OPEN with this reason.

## Consequences for the OCM build (read-only observations on `ORION-OCM-wt/m11-self`; nothing touched)

* `selfmodel/govern.assure`: the `prediction_realised` check reads the families the proposer named
  and has no disjointness clause — `SelfChangeProposal` carries no dev-task ids, so E4's
  `mutant_graded_on_dev_tasks` is not refused by `assure`; the object needs a `dev_tasks` field and
  the adopter a `REFUSED_TASKS_SEEN_BY_PROPOSER` branch. `prediction_digest_before_access` is a
  caller-supplied string; it should be a K_self receipt admitted before outcome access (E5 chain).
* `govern.shadow_evaluate` compares `kso_state_hash` only; E5 requires the external commitment log
  in the compared state, and the runner's write capability confined to K_self by construction.
* `govern.AdoptionLedger.rollback` restores artifact and component table and revokes the stamp, but
  no cache is recompiled and hash equality is left to the caller — E6's `rollback_leaves_cache` is
  not refused by the ledger; the ledger should own the state-hash assertion and the cache.
* `govern.AdoptionLedger.charge` is a mutable field and `proposal.touches_protected_target` is a
  string-prefix test on `target_component` and `change` keys; E7 needs the meter structurally
  outside every proposal's write set (a key `budget` or `Meter` passes today).
* `diagnose.diagnose` returns `minimum_sufficient = D3` from a single D3 ablation without a
  certificate and gates escalation only in `escalation_allowed`; `architecture_alarm` takes
  `frequency ≥ 3` as an input — E2's classifier has no frequency term (repeated failure never
  contributes). `ObstructionCertificate.registered_alternatives` is supplied by the certificate
  itself; E3(iii) requires the alternative closure from the component registry.
* `selfmodel/model.SelfModel.record` admits derived diagnoses as OBSERVATION (channel default);
  E1 needs derived provenance so revoking a trace reopens the diagnoses built on it.
* Open after this batch: the graded-semiring half of MEG-02 (with witness), non-regular
  acceptability for MEG-27, the deconsolidation *decision* of MEG-19 (parent-owned), per-source
  normalisation for MEG-07, the SHRG/CCG half of MEG-34, ceilings for J2+ (MEG-28; E3 gives J1/J3
  on the Boolean fixture only), and the M11 measurements these gate (S1–S7 benchmark, real-failure
  replay, the strongest-parent comparison).

```text
E1  MEG-29 ext.   PROVED (non-interference both directions; proposal ⟦0,U⟧ until external adoption)
E2  M11 §3        PROVED (128 000-trace grammar); tightened: certificate dominates run symptoms
E3  MEG-28/M11 §4 PROVED (certificate ⇔ Jump precondition, 128/128); LIVE clause and closure enumeration
E4  M11 §5/§8/§10 PROVED (11 250 cases); tightened: disjointness clause is part of the rule
E5  M11 §9        PROVED (by construction, finite); chain assurance tamper-evident
E6  MEG-18/28     PROVED (hash-exact rollback incl. cache); tightened: produced = stamp-transitive
E7  MEG-30 ext.   PROVED (⌊B/δ_min⌋); tightened: non-decreasing charge is necessary
E8  KS-T12/T14    CONJECTURE (falsifiers exact; smallest holding and failing fixtures recorded)
R1  MEG-19        PROVED exactness half / OPEN decision (PARENT_OWNED)
R2  MEG-27        PROVED regular inventories / OPEN non-regular acceptability
R3  MEG-02        OPEN with witness
NOVELTY NOT_ESTABLISHED
```
