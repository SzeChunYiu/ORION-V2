# KSO field-frontier theorems — batch 10 (J1–J3)

Date 2026-09-06. Tenth one-day batch, third of the field-completion programme (ORION-V2 #353) over the
Machine Epistemics field frontier (`field_dynamics_v1/FRONTIER.md`). Scope: three frontier rows —
FDX-06 distributed Machine Epistemics (J1), FDX-07 epistemic games (J2), FDX-14 whole-system lower
bounds (J3). Each row is closed as PROVED on a finite fixture, bounded exactly (an impossibility with a
witness), or PARENT_SUFFICIENT / PARENT_OWNED with the executable rule and its falsifier. The FDX ids
are kept. Theorem labels J1–J3 are batch labels (batch 8 used H1–H4); they are unrelated to the Jump
levels J2–J5 of batch 7 G1.

Every item has an exact finite checker (`kso_field_frontier_batch10_exact.py`, stdlib only; every count
an integer, every probability an exact `Fraction`; exit 0 / 1 / 2 with 2 = CANNOT_CHECK, exercised by
`--probe-cannot-check`), at least one planted hostile whose mutation is asserted applied and caught, and
a no-alarm control; `tests/unit/test_kso_field_frontier_batch10.py` pins every count. Checker run on
billy-old (Python 3.14.4): exit 0, wall 4.6 s, `"status": "ALL_HOLD"`, three `"OPEN"` rows and three
`"CANNOT_CHECK"` rows listed below; 8/8 new tests. All objects are re-implemented inside the checker
(antichain warrant intervals over a three-id universe, a five-event causal poset of revocations, the
authority product lattice, the MEG-16 nogood filter, decision-tree DPs over 65 535 version spaces,
separating and specifying sets); nothing imports `ocm`; nothing ran on the Mac.

NO NOVELTY OR SUPERIORITY CLAIM. Every replication, game-theoretic or counting fact used is a named
parent's; the contribution is the exact statement on the registered objects of `FIELD.md`, the
executable falsifier, and the reading of what the OCM code can and cannot support. Rigour follows the
batch-6 integration review: guaranteed statements only, never an accusation from an observed answer;
ceilings stated for the registered fixture only; no scalar over-claims.

Notation as in batches 1–8 and `FIELD.md`: `𝒜_E` the antichains over `2^E` with `⊕` (alternative) and
`⊗` (conjunction), warrant interval `⟦L,U⟧`, three-valued liveness `λ_R` (KS-T21), the order
DEAD < UNKNOWN < LIVE written `≤₃`, authority product lattice with coordinate-wise `∧` and undeclared =
0 (T1), `Impact_D` the least dependency-closed superset (KS-T09/T22), `[φ]` the indicator of `φ`.

## J1 · FDX-06 · distributed Machine Epistemics: what exchange of warranted atoms can and cannot carry

**Objects.** Nodes `A, B, C`, each a KnowledgeSpace over the shared assumption universe `E = {e1, e2,
e3}` (168 warrant intervals `⟦L,U⟧`, all of them). *Revocation events* form a causal poset (Lamport
order): `rv1 = revoke(e1)`, `ri1 = reinstate(e1)` after `rv1`, `rv1b = revoke(e1)` after `rv1` and
concurrent with `ri1`, `rv2 = revoke(e2)`, `ri2 = reinstate(e2)` after `rv2`. A node's *view* is a
causally closed subset of events (15 views); its revocation set is the *revoke-wins merge*
`R(V) = {e : some received revoke on e is not causally dominated by a received reinstate on e}` — a
remove-wins observed set. An *import* of atom `x` with interval `⟦L,U⟧` from node `j` is admitted at
node `i` under a fresh *message assumption* `m_{j→i,x}`: `⟦{{m}} ⊗ L, {{m}} ⊗ U⟧` (the T4 Jump-certificate
shape). Its authority is `drop_commit(A_x ∧ T_i(j))` with `T_i(j)` the receiver's *trust cap* for `j`, an
authority over `{source, world_truth, commit}` (18 sender authorities × 9 caps). A *relay* `j → k → i`
applies the rule twice. The receiver's local dependency graph `x → y → z`, `w → y`, `n → q` with `x`
imported (cites `e1`, `m`), `w` native (`e2`), `n` native (`e3`), `y = x ⊗ w`.

**Theorem** (4 536 antitone checks; 59 causally consistent delivery orders; 15 × 168 view verdicts;
162 import-authority pairs; 1 458 relay paths; 1 336 import/revocation pairs; 4 096 union checks).
(i) *Antitone liveness.* For every interval and `R ⊆ R'`, `λ_{R'} ≤₃ λ_R` (4 536/4 536): a node holding
more revocations never returns a higher verdict. (ii) *Revoke-wins exchange converges.* `R(V)` is a
function of the received set, hence identical on all 59 causally consistent delivery orders of the 15
views; a per-id last-writer-wins flag diverges on 117 of 259 order pairs (witness: view `{rv1, ri1,
rv1b}`, orders `rv1·ri1·rv1b` → `e1` revoked, `rv1·rv1b·ri1` → not revoked; honest: revoked). (iii)
*Staleness has one unsafe direction.* Comparing every view with the full history: 354 over-claims, 369
under-claims, 1 797 agreements; **every** over-claim comes from a view missing an effective revocation
(`R(full) ⊄ R(V)`, 354/354) and **every** under-claim from a view holding a revocation the history has
reinstated (369/369). (iv) *Missing update ≠ no update.* The view `V0 = {rv1, ri1, rv1b}` is a prefix of
two histories, with and without `rv2`; a node reading its view as current is right on 168/168 intervals
in the history without `rv2` and wrong on 97 in the history with it — the two histories are indistinguishable at the node (R5). (v)
*Authority under partial trust.* An import's authority is ≤ the sender's and ≤ the cap (162/162), its
commit rank is 0 (162/162); through a relay it is ≤ the source and ≤ every cap on the path (1 458/1 458);
when two paths deliver different authorities the atom's usable authority is their meet — the join produces
an authority no path carried on all 490 differing cases. (vi) *Per-message assumptions localise trust.*
Revoking `m` kills every import from `j` (1 336/1 336) and every composition citing one (148/148), leaves
every native atom's verdict unchanged under every `R` (1 336/1 336), and the receiver's recomputed verdict
equals `[m ∉ R] ∧₃ λ_R⟦L,U⟧` (KS-T21) — the sender's *claimed* verdict is never an input (a sender claiming
LIVE is wrong on 875 of the 1 336 pairs). Equivocation (two messages of `j` about `x` with different
intervals) is detectable iff both reach one node: 37 of 64 delivery patterns; the other 27 leave the two
views individually consistent. (vii) *Reopening under exchange.* `Impact_D(S1 ∪ S2) = Impact_D(S1) ∪
Impact_D(S2)` (4 096/4 096); for every batch of 2–3 remote deltas in every order the batched cone is
contained in the union of the sequential cones and the final state is order-independent (36/36); a
revoke followed by its reinstatement reopens 3 + 3 atoms sequentially and 0 batched. Cones on the fixture:
`revoke e1` → `{x, y, z}`, `revoke m` → `{x, y, z}`, `revoke e3` → `{n, q}`. (viii) *k sources.* `k`
independent source assertions give `⊕_j ⟦{{m_j}}⟧`: LIVE iff fewer than `k` are revoked (2 + 4 + 8
checks); the authority stays at the meet `source = 1`, `world_truth = 0`, `commit = 0`; three nodes agreeing
is not world truth.

**Proof.** (i) `ℓ_R(P) = 1 ⇔ ∃W ∈ P: W ∩ R = ∅` is antitone in `R` on both endpoints. (ii) the merge
reads only the set of received events and their fixed causal order; a flag overwritten in arrival order
depends on which linear extension arrived. (iii) contrapositive of (i): if `R(full) ⊆ R(V)` the view
cannot exceed the history, and if `R(V) ⊆ R(full)` it cannot fall below. (iv) construction; the two
histories restrict to the same `V0`. (v) `∧` is the greatest lower bound of the product order and
`drop_commit` lowers; the join of incomparable elements is above both. (vi) every warrant of the import
contains `m`; native warrants do not; `ℓ_R({{m}} ⊗ P) = [m ∉ R] · ℓ_R(P)`. (vii) forward reachability is
a union-preserving closure; an atom whose verdict differs between the start and the end of a sequence
changed at some step, so it lies in that step's `C` and the union of cones; the final `R` is the union of
the deltas. (viii) KS-T21 for `⊕`; T1 for the meet. ∎

**Hostiles.** `mutant_lww_revocation_bit` — 117 divergent order pairs, witness recorded.
`mutant_stale_view_as_current` — 97 wrong verdicts in the history with `rv2`, 0 without: the mutant is
exactly the R5 policy. `mutant_commit_travels` (import keeps the sender's commit rank) — 81 forged commit
ranks. `mutant_authority_join_over_paths` — 490/490 caught. `mutant_import_without_message_assumption`
(the T4 uncertified-structure shape) — 883 imports survive the revocation of trust in their sender.
`mutant_trust_sender_verdict` — 875 caught. `mutant_majority_is_world_truth` — caught (the OCM's own
`mutant_repetition_raises_authority` in `knowledge/world.py` is the same hostile). **No-alarm:** a view
holding every event agrees with the history on 168/168 intervals; relay through a full-trust cap returns
the sender's authority minus commit; the two-sensor alternative of J2 counts as two independent supports.

**Status.** PARENT_SUFFICIENT for every replication fact, exactly as FRONTIER predicted: convergence of
the revoke-wins set is the state-based CRDT theorem (Shapiro–Preguiça–Baquero–Zawirski 2011; the
remove-wins observed set of Bieniusa et al. 2012 — candidate, cited not verified here); causal views are
Lamport 1978; the one-unsafe-direction fact and the indistinguishable histories are R5 of
`revision_consistency_v1` (PROVED there) and, for the knowledge reading, Halpern–Moses 1990 (candidate);
the authority bound is Biba low-water-mark / Denning 1976 (verified, T1); per-message assumptions are ATMS
assumptions (de Kleer 1986) and the T4 certificate stamp; the reopening statements are KS-T22 / T5;
equivocation detection is fork consistency / accountability (Mazières–Shasha 2002; Haeberlen–Kouznetsov–
Druschel 2007 — both candidate). Byzantine agreement (Lamport–Shostak–Pease 1982) is PARENT_OWNED and
*not needed for warrant*: every import is a per-source revocable assumption, so nodes never have to agree
on truth, only each on its own view; agreement is needed only for authority-bearing registry objects
(`store/registry.py` COMMIT_AUTHORITY, trust roots), and there the parent owns everything. **The exact
residual statement** (PROVED corollaries, no new mathematics): *under exchange of warrant intervals with
per-message assumptions and trust caps, every verdict at a receiver is a function of its causally closed
view, its caps and the received intervals; staleness over-claims only by a missing revocation and
under-claims only by a missing reinstatement; no exchange raises any authority coordinate or creates
commit; trust revocation is local to the message cone; batching remote deltas never reopens more than
sequencing them.* FRONTIER's four required distinctions are met on the fixture: causal consistency ≠
application invariant (R7 — a causally closed view still over-claims), message authenticity ≠ truth
(`m` is an assumption with authority `source`), consensus ≠ world truth ((viii)), missing update ≠ no
update ((iv)). **OPEN:** graded / probabilistic trust and Byzantine-fraction thresholds for warrant
exchange (FDX-08 territory). **CANNOT_CHECK:** message authenticity itself (signatures, trust-root
provenance) is assumed, as R6's anchor authenticity is.

## J2 · FDX-07 · epistemic games: the attack surface of the commitment gate, then the exact gate statements

**Objects.** Legitimate evidence `o1, o2` (OBSERVATION channel, authority `source = 1, world_truth = 1`);
an adversarial provider controlling ids `a1, a2, a3` (IMPORTED "source asserts P", authority
`source = 1` only — `knowledge/world.py::assert_fact`). Six claims with certified intervals: `c_native`
`{{o1}}`, `c_native2` `{{o1},{o2}}`, `c_report` `{{a1}}`, `c_sybil` `{{a1},{a2},{a3}}`, `c_mixed`
`{{o1,a1},{o2}}`, `c_composed` `{{o1,a1}}`. The *gate* (the `commitment_gate` shape): commit iff some
exhibited warrant `W` survives the receiver's revocations and the MEG-16 nogood filter and
`required ≤ (⋀_{e∈W} A_e with commit dropped) ∧ A_commit` — the per-alternative existential form, with the
committing `W` written to the receipt. Requirements: `REQ_REPORT` (`source ≥ 1`), `REQ_TRUTH`
(`world_truth ≥ 1`), `REQ_COMMIT` (`commit ≥ 1`). The provider's *strategy*: for each id one of {absent,
asserted, retracted}, plus any subset of the contradiction registrations `{a1,o1}`, `{a1,o2}` when `a1`
exists, plus a "confidence" coordinate in `{0, 1/2, 1}` (81 lattice strategies; confidence is not a gate
input). The provider cannot touch the OBSERVATION channel, the checker channel, the receiver's own
revocations, or any authority coordinate above `source`. A 2 × 2 *inspection game* (provider lies /
honest; gate audits / not; rational payoffs `g, f, c, d`) is included as the parent's object.

**Theorem** (81 strategies × 6 claims × 3 requirements; 4 374 confidence checks; 63 equilibria). *What
the provider cannot do:* (i) *Non-interference.* For a claim none of whose warrants cite a provider id
the verdict is one value across all strategies (486/486); a claim with a provider-free alternative
commits under `REQ_TRUTH` through that alternative on every strategy (81/81, receipt `W = {o2}`). (ii)
*Authority ceiling — exactly bounded.* No strategy commits `c_report`, `c_sybil` or `c_composed` under
`REQ_TRUTH` (0 of 243) or under `REQ_COMMIT` (0 of 243); `REQ_COMMIT` is never met from evidence at all
(0 of 486, T1). (iii) *No persuasion lever.* The verdict is invariant under the confidence coordinate
(4 374/4 374); a gate that reads it commits `c_report` under `REQ_TRUTH` on 36 strategies. (iv)
*Contradictions are local.* Registering `{a1,o1}` refuses `c_composed` (its only support contains both)
and changes nothing for `c_native` or `c_mixed` (4/4); no registration makes a legitimate id DEAD.
*What the provider can do:* (v) *Enable REPORT-typed commits* of claims within its channel authority:
under `REQ_REPORT`, `c_report` commits on exactly the 36 strategies with `a1` asserted, `c_sybil` on the 61
with any id asserted, `c_composed` on the 18 with `a1` asserted and no `{a1,o1}` nogood — every such
commitment carries authority `source = 1` and is typed REPORTED (`dialogue/gate.py::required_marker`).
(vi) *Force refusal* of a claim iff every exhibited warrant cites a provider id: `c_report` 45,
`c_sybil` 20, `c_composed` 63 strategies; `c_native`, `c_native2`, `c_mixed` 0. (vii) *Commit then
retract.* After a licensed commit of `c_report` the receipt names `W = {a1}`; retracting `a1` reopens
exactly `{a1, commit:c_report}`; a receipt without evidence ids misses the commitment. The commitment was
licensed when made (R4: a historical record is not a lie). (viii) *Sybil.* Three ids of one principal
give one independent support under a principal-aware count (honest 1) and three under id-disjointness
(mutant 3); two sensors give 2 under both. (ix) *Inspection game (parent).* With provider payoff `+g`
for an unaudited lie, `−f` when caught, and gate payoff `−c` per audit, `−d` per unaudited lie, the
interior mixed equilibrium `q* = g/(g+f)`, `p* = c/d` exists iff `0 < c < d`; both indifference
identities hold exactly on 63 of 108 rational payoff grids (45 have no interior equilibrium; example
`g = f = c = 1, d = 2`: `p* = q* = 1/2`). Whatever `p`, the truth-typed gate's verdict on provider-only
claims is REFUSE by (ii); the game bears only on REPORT-typed commitments and on audit cost.

**Proof.** (i) the gate reads only `W ∩ R`, the nogood filter and `⋀_{e∈W} A_e`; provider ids in `R` or
in nogoods touch no provider-free `W`. (ii) every `W` of these claims contains a provider id whose
authority has `world_truth = 0`, and `∧` is coordinate-wise min; commit is dropped by T1 before the meet
with `A_commit`, which cannot add it. (iii) syntactic non-dependence (as T3). (iv) `filter_N` removes
supports that *contain* a nogood; a support without the provider id contains none. (v)–(vi) enumeration;
liveness of a claim whose every warrant cites a provider id is decided by the provider's asserted set.
(vii) the receipt's ids are the seeds of `Impact_D`. (viii) definitions. (ix) the indifference equations
`(1−q)g − qf = 0` and `−c = −pd`. ∎

**Hostiles.** `mutant_report_as_truth` — 36 false truth-commits. `mutant_confidence_gate` — 36 (the
persuasion lever exists only in the mutant). `mutant_nogood_kills_endpoint` (MEG-16D violation) —
refuses `c_native`; caught. `mutant_receipt_without_evidence_ids` — the retraction cone misses the
commitment; caught. `mutant_sybil_independent_count` (id-disjointness = independence; the shape of
`store/evidence.py::independent_support_count`) — 3 vs honest 1; caught. **No-alarm:** native claims commit
under `REQ_TRUTH` on every strategy; `c_mixed` commits through `{o2}`; two genuine sensors count 2.

**Status.** PARENT_HEAVY, attacked as such. PARENT_SUFFICIENT / PARENT_OWNED: the strategic results —
truthful equilibria and their impossibilities under costly verification (Crawford–Sobel 1982 cheap talk;
Milgrom 1981 and Grossman 1981 disclosure; Kamenica–Gentzkow 2011 persuasion; peer prediction, Miller–
Resnick–Zeckhauser 2005), inspection / security games (Avenhaus–von Stengel–Zamir 2002; Tambe 2011), the
Sybil attack (Douceur 2002), and the soundness quantifier "for every prover" of interactive proofs
(Goldwasser–Micali–Rackoff 1989), which is the parent of the attack-surface reading; adversarial-ML data
poisoning (Biggio–Roli 2018) is the parent of (iv) and (viii) — all candidate citations except where
earlier batches verified them. What is PROVED here is only the gate-specific statement: *the provider's
action set on the gate is exactly {enable REPORT-typed commits of claims within its channel authority,
force refusal of claims whose every warrant cites its ids, poison joint supports containing its ids};
nothing else changes any verdict; no coordinate above its channel is reachable; the persuasion lever has
no argument to act on.* Bayesian persuasion needs a posterior the gate does not compute (the FIELD
distinction "truth warrant ≠ actionability ≠ permission" is what removes the lever). **OPEN:** a
truthful-revelation mechanism for real provider utilities is utility-model dependent and parent-owned;
nothing here bounds the *cost* of audits other than (ix). **CANNOT_CHECK:** that a real provider's utilities
match any payoff matrix. The model's boundary: a provider who compromises an OBSERVATION or checker
channel is outside it — channel typing is an enforced premise (the H1 closure interface of batch 8).

## J3 · FDX-14 · whole-system lower bounds on the registered finite classes: identification, retention, repair, communication, verification

**Objects.** The registered classes ALL16 (the 16 Boolean functions of two inputs, four table rows),
AFFINE8 and MONOTONE6 (batch-4 D2, batch-8 H3). Channels with power-of-two answer alphabets charged
`log2(alphabet)` bits: four row observations (1 bit), two pair observations (2 bits), the whole table
(4 bits); five channel mixes. *Retention*: a mutable memory of `s` bits plus an immutable description;
the affine description determines row 11 from rows 00, 01, 10. *Repair*: a retained target whose warrant
cites `m_i ≥ 1` evidence ids per row (`m ∈ {1,2,3}^4`, 81 designs); an adversary revokes `k` ids; the
worst-case repair cost is the number of rows all of whose ids are revoked (each needs one fresh query).
*Communication*: two nodes decide equality of their retained procedures. *Verification*: a checker probes
rows of a claimed table; *oblivious* if its probe set is fixed before the claim, *adaptive* if it may
depend on the claimed target.

**Theorem** (5 × 65 535 identification checks; 648 + 48 repair checks; 120 fooling pairs; every probe
set of every class). (i) *Identification.* For every version space `V ⊆ ALL16` and every channel mix the
minimal worst-case total channel bits of an identifying adaptive transcript is `≥ ⌈log2 |V|⌉`
(327 675/327 675) and equals 4 on the full class for all five mixes — a wider channel moves bits into the
alphabet, it does not remove them; observations alone identify AFFINE8 and MONOTONE6 in 3 bits. (ii)
*Retention.* A 3-bit memory with the affine description retains all 8 affine targets exactly and must
refuse the 8 others (`CANNOT_REPRESENT`); every 3-row projection of the 16 tables collides on 8 pairs
(32 over the four projections) — fewer than `log2 |H|` mutable bits cannot retain `H`. (iii) *Repair ×
retention.* For every design `m` and every `k ≤ Σ m`: `Σ m + repair_k(m) ≥ 4 + k` (648/648; equality on
164 cases, e.g. `m = (1,1,1,1)`), and `≥ n + k` on `n = 2, 3` rows (48/48): redundancy converts repair
queries into retained ids one for one and never below `n + k`; the minimal total at `k = 1` is 5 on four
rows and 4 on three. (iv) *Communication.* The 16 diagonal pairs are a fooling set for equality (120/120
off-diagonal pairs separate), so a deterministic equality check needs `≥ 4` transcript bits; a `d`-bit
truncation digest declares unequal procedures equal on 56 / 24 / 8 / 0 pairs for `d = 1, 2, 3, 4`. (v)
*Verification.* Smallest oblivious probe set / largest adaptive specifying set / entropy bound:
ALL16 4 / 4 / 4, AFFINE8 3 / 3 / 3, MONOTONE6 **4 / 3 / 3** — on MONOTONE6 an oblivious verifier needs one
probe more than the teaching-dimension bound (D2: TD = 3), and any three-probe oblivious verifier accepts
a forged table on 6 (probe set, pair) cases (witness: probes {00, 01, 10}, claimed `0`, actual AND).
(vi) *Whole system.* Per phase, ALL16 vs AFFINE8: identification 4 / 3 bits, retention 4 / 3 bits,
oblivious verification 4 / 3 probes, equality 4 / 3 bits, repair + retention at `k = 1` 5 / 4 — the
description moves exactly one unit out of every phase and adds 8 `CANNOT_REPRESENT` targets.

**Proof.** (i) a transcript tree with `|V|` leaves whose internal nodes have fan-outs `f_v` satisfies
`|V| ≤ max_path ∏ f_v` (induction on the tree), so the worst path carries `≥ log2 |V|` bits; the DP is
exact. (ii) pigeonhole; the affine completion `row_11 = row_00 ⊕ row_01 ⊕ row_10` is exact on AFFINE8 by
definition and wrong on every non-affine table. (iii) sort the rows by multiplicity; if the adversary
wipes `j` rows with `s_j = Σ_{i≤j} m_(i) ≤ k < s_{j+1}`, the unwiped rows hold `Σ m − s_j ≥ (n−j)·m_(j+1)
≥ (n−j) + (m_(j+1) − 1) ≥ (n−j) + (k − s_j)`, i.e. `Σ m + j ≥ n + k`; if all rows are wiped `k ≤ Σ m`
gives it. (iv) fooling-set lemma (any two diagonal inputs in one rectangle force an off-diagonal input
into it); a `d`-bit digest has `2^d` buckets. (v) enumeration of all 16 probe sets; the bound is
pigeonhole on binary probes. (vi) table. ∎

**Hostiles.** `mutant_charge_channel_one_bit` (every channel charged one bit whatever its alphabet) —
258 644 version spaces reported below the entropy bound; caught. `mutant_description_without_cannot_
represent` (the affine memory silently stores the affine completion of a non-affine target) — 8 wrong
tables; honest 0 wrong, 8 refusals. `mutant_repair_from_memory_replay` (repair by re-admitting the revoked
id's content under a fresh id at cost 0 — batch-8 H3's memory replay, H4's relearn) — violates `n + k` on
324 of 648 (design, k) cases; caught. `mutant_digest_equality` — 56 / 24 / 8 false "same" verdicts for
`d < 4`. `mutant_oblivious_verifier_three_probes` on MONOTONE6 — 6 forgeries accepted. **No-alarm:** four
probes separate every pair of ALL16 (120/120); the affine memory retains all 8 affine targets; the 4-bit
digest never collides; the `n + k` bound is tight on 164 cases, so the honest total is never over-charged.

**Status.** PARENT_OWNED mathematics throughout: decision-tree / query complexity (Buhrman–de Wolf 2002,
verified in batch 8), teaching dimension (Goldman–Kearns 1995) and specifying / witness sets
(Kushilevitz–Linial–Rabinovich–Saks 1996 — candidate), fooling sets and deterministic communication
complexity (Yao 1979; Kushilevitz–Nisan 1997), cell-probe / pigeonhole retention (Yao 1981), advice and
description (Karp–Lipton 1982 — candidate), Hartley counting (T9, lane-200 Theorem A), erasure counting;
the coded case (parity across rows, Singleton 1964) is the parent's and is *not* covered by the
uncoded evidence-id fixture. What is PROVED is the exact table on the registered classes and the
whole-system reading FRONTIER asked for: *representation (the description) and external memory move cost
between phases and buy it with `CANNOT_REPRESENT` targets; nothing erases the `log2 |H|` bits or the
`n + k` repair-plus-retention floor.* **What is bounded and at what scale:** the four-row registered
classes only; the general statements ((i), (ii), (iii), (iv)) are the parents' pigeonhole facts and hold
for `2^n` rows with `2^n` in place of 4, but are checked here at `n = 2` (and (iii) at `n = 2, 3`).
**OPEN:** coded / cross-row redundancy and infinite classes (MEG-34 / FDX-09). **CANNOT_CHECK:** collision
resistance of a digest used for cross-space identity is a computational assumption (R6); inside the
finite model every digest shorter than `log2 |H|` collides.

## Consequences for the OCM build — runtime obligations H1–H8 (read-only observations on `ORION-OCM-wt/m11-self` at `f157927`, 2026-09-06; nothing touched)

Each H-item names the runtime location the theorem would change; none is a claim about an M12 result.
H-numbering is this batch's obligation list, not batch 8's theorem labels.

* **H1 (J1 vi) — imports need a per-principal message assumption.**
  `src/ocm/store/evidence.py::EvidenceRegistry.register` (line 117) admits IMPORTED records with authority
  `source = 1` (`src/ocm/knowledge/world.py::assert_fact`, line 75; `src/ocm/dialogue/workspace.py`
  promote, line 271) but the record's warrant is its own id only; revoking trust in a *principal* has no
  object — revocation is per evidence id (`revoke`, line 173). Obligation: every IMPORTED record carries a
  message assumption bound to `(principal, message)` in its warrant, and principal revocation is
  capability-level revocation over the principal's assumptions (batch-6 F1), so the cone of (vi) is what
  `kso/revocation.py::reopening_report` (line 188) reports.
* **H2 (J1 ii–iv) — revocation state must merge as an event set, and verdicts that depend on it are "as of the view".**
  `EvidenceRegistry.revoked` (line 112) is one `frozenset`; `reinstate` (line 181) is set removal — the
  last-writer-wins shape of (ii) once two registries exchange. Locally the `store/event.py` chain
  (`next_event`, line 214; `verify_chain`, line 224) gives the causal order; no cross-registry merge exists.
  Obligation: exchange revoke/reinstate as events with causal predecessors and merge revoke-wins; type any
  verdict computed over imported revocation state CONDITIONAL_ON_VIEW (the batch-8 H1 "as of" reading),
  never current (iv).
* **H3 (J1 v) — trust caps as authority meets at import; no join across paths.**
  `src/ocm/kso/types.py::internal_authority` (line 168) drops commit; no trust cap per principal exists
  and `knowledge/world.py::authority` (line 113) fixes `source = 1`, raising `verified = 1` only from a
  LIVE verification record (its planted `mutant_repetition_raises_authority`, line 172, is J1 (viii)'s
  hostile). Obligation: `A_import = drop_commit(A_sender ∧ T(principal))`, and a claim with alternatives
  from several imports uses the meet of their authorities, never the coordinate-wise max (T7's `⋁` form is
  an upper bound, not a licence).
* **H4 (J2 i, v–vii) — the gate's authority check should be per committing alternative and the receipt should name it.**
  `src/ocm/runtime/solve.py::commitment_gate` (line 365) checks `task.required_authority <=
  op.authority.meet(commit_authority)` (line 377) with one operator authority (the meet over all tails,
  `kso/admission.py::compose`, line 161), and writes `evidence_ids = warrant.evidence` — all exhibited
  evidence — into the receipt (line 387). J2 (i) needs the existential form (some LIVE `W` whose own
  authority meets the requirement) so that a claim with a provider-free alternative commits under
  `REQ_TRUTH`; J2 (vii) needs the receipt to name the committing `W` so that retraction reopens exactly.
  `dialogue/gate.py::required_marker` (line 120) already types source-layer assertions REPORTED — that is
  the J2 (v) typing and should be the only commitment type reachable from IMPORTED evidence.
* **H5 (J2 viii) — independence over principals, not ids.**
  `src/ocm/store/evidence.py::independent_support_count` (line 198) counts alternatives with pairwise
  disjoint assumption *ids* — three Sybil ids count 3. Obligation: disjointness over registered
  principals (`source`), else `INDEPENDENCE_NOT_ESTABLISHED`; `mutant_majority_truth` (line 217) stays the
  runtime's own hostile for the truth half.
* **H6 (J2 iv) — contradiction registrations carry provenance.**
  `EvidenceRegistry.register(contradicts=…)` (lines 127, 147–150) lets any registrant add the nogood
  `{eid, o}` against legitimate evidence `o`. The effect is bounded to joint supports containing `eid`
  (J2 iv), but the registration itself has no assumption id and cannot be revoked with its author.
  Obligation: a nogood carries the registrant's message assumption and dies with it.
* **H7 (J3 i–iii) — information receipts charge alphabet bits; class-restricted memories refuse; repair names fresh evidence.**
  Batch-4 D2's `INFORMATION_BUDGET_RECEIPT` should charge `log2(alphabet)` per channel use, not one
  per query (J3 i). `src/ocm/kso/admission.py::admit` (line 81) refuses unregistered atom types
  (`UNREGISTERED_ATOM_TYPE`) but has no `CANNOT_REPRESENT` for a target outside a registered
  class-restricted memory (J3 ii). `src/ocm/runtime/state.py::EventStore.replay` (line 103) restores
  behaviour from the log at zero information cost — a repair receipt must cite re-acquired evidence ids,
  or it is batch-8 H4's relearn (BOI), not repair (J3 iii).
* **H8 (J3 iv) — cross-space identity by digest is a computational claim.**
  `src/ocm/kso/space.py::KnowledgeSpace.digest` (line 284) and `store/canonical.py::canonical_digest`
  (line 164) would be the equality transcript between spaces; a receipt should say
  `EQUAL_UNDER_COLLISION_RESISTANCE`, and an equality check that must be exact without the assumption
  needs the `log2 |H|` transcript bits of J3 (iv).

```text
J1  FDX-06  PARENT_SUFFICIENT (state-based CRDT convergence, R5 freshness impossibility, Byzantine agreement for authority objects); PROVED corollaries: antitone liveness 4 536, revoke-wins order-independent 59 orders (LWW diverges 117), over-claim ⇔ missing revocation 354/354, indistinguishable histories (97 wrong / 0), import authority ≤ sender ∧ cap with commit 0 (162), relay bounded 1 458, join caught 490, trust revocation local 1 336, Impact ∪-distributive 4 096, batched cone ⊆ sequential 36, k-source ⊕ without world_truth
J2  FDX-07  PARENT_HEAVY / PARENT_SUFFICIENT (cheap talk, disclosure, persuasion, inspection games, Sybil, IP soundness); PROVED gate-specific: non-interference 486, authority ceiling 0/486 (EXACTLY_BOUNDED), no persuasion lever 4 374, contradictions local, REPORT-typed commits exactly 36/61/18, forced refusal iff every warrant cites the provider, receipt names W (cone exact), Sybil 1 vs 3, inspection equilibrium 63/63
J3  FDX-14  PARENT_OWNED (query complexity, teaching/specifying sets, fooling sets, cell-probe pigeonhole, erasure counting); PROVED on the registered classes: bits ≥ ⌈log2|V|⌉ for 5 mixes (327 675), retention 3-bit refuses 8, Σm + repair ≥ n + k (648 + 48, tight 164), equality ≥ 4 bits with digest collisions 56/24/8/0, oblivious 4 > adaptive 3 = entropy 3 on MONOTONE6, description moves one unit per phase for 8 CANNOT_REPRESENT
OPEN: graded/probabilistic trust (FDX-08); truthful mechanisms for real utilities; coded redundancy and infinite classes
CANNOT_CHECK: message authenticity; provider utilities; digest collision resistance
NOVELTY NOT_ESTABLISHED
```
