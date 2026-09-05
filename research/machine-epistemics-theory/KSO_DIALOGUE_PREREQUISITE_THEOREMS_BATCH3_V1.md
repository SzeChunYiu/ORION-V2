# KSO dialogue-prerequisite theorems — batch 3 (C1–C8)

Date 2026-09-05. Third one-day batch over the machine-epistemics gap atlas
(`ME_THEORY_GAP_ATLAS_V1.md`), chosen as the eight gaps the OCM M4 milestone (persistent dialogue
cognition: discourse workspace, reference, correction/supersession, clarification as an information
action, thought↔language feedback, external commitment gate — `ORION-OCM` issue #6) needs proved or
defined. Every theorem has an exact finite checker (`kso_dialogue_prereqs_batch3_exact.py`, stdlib
only; exit 0 / 1 / 2 with 2 = CANNOT_CHECK), at least one planted mutant asserted applied and caught,
and a no-alarm control; tests in `tests/unit/test_kso_dialogue_prereqs_batch3.py` pin every count.
Checker run on billy-old: exit 0, wall 3.2 s; 13/13 tests. Objects (antichain semiring, warrant
intervals, Kleene liveness, authority meet, impact cone / KS-T22 report, version spaces and the B2
per-input warrant, the KS-T25 nogood filter, procedure terms, a seven-stage solve pipeline) are
re-implemented inside the checker; nothing imports `ocm`. NO NOVELTY OR SUPERIORITY CLAIM: every result
is a corollary of KS-T01/T20/T21/T22/T25/T26, batches 1–2, and the named parents; the contribution is
the exact statement, the executable falsifier, and — where the atlas wording could not be proved as
written — the tightened wording, marked **tightened** below.

Notation as in batches 1–2: ⊕ join (alternative), ⊗ meet (conjunction), ⟦ℓ,u⟧ warrant interval
(partial when u = 1, certified when ℓ = u), Λ(x) the interval of atom x, R the revoked set, λ_R ∈
{LIVE, DEAD, UNKNOWN} the Kleene liveness of KS-T21, Γ a revocation family, Q the registered query
family, `reopen`/`recheck`/`unaffected` the KS-T22 report.

## C1 · MEG-33 · epistemic action value over intervals (clarification as an information action)

**Objects.** Hypotheses h ∈ H are assignments to the cells of Q plus hidden coordinates outside Q;
the live hypothesis set V ⊆ H is the version space. A cell q is *decided* on V iff every h ∈ V agrees
on q (`agreed(V)`). A question a is a partition of V by answer (uniform prior over V). The
three-valued cell state is ⟦L_q, U_q⟧: an INTERACTION answer exhibits a new warrant, `L_q ⊕ {e}`, with
U_q untouched; an EXPERIMENTATION closure on the scope pins `U_q := L_q` (WLL-7 manifest). The action
value is `V(a) = E[#cells moved UNKNOWN → decided on Q | a] − cost(a) − risk(a)`; the policy asks the
highest-value question and only if that value is positive.

**Theorem.** (i) If the ambiguity in V is irrelevant to Q (`agreed(V) = Q`), every question has zero
information value, so under any positive cost none is asked. (ii) If question b *refines* a (every
answer block of b lies inside a block of a), then `V(b) ≥ V(a)` under matched cost and risk, strictly
when some block of a is undecided on a cell that b's sub-blocks decide. (iii) Once a has been answered
(V replaced by an answer block), asking a again has value `−cost − risk ≤ 0`, strictly negative under
positive cost. (iv) Queries move the LIVE side only: no INTERACTION answer makes a cell DEAD, and a
LIVE cell stays LIVE; a closure certificate is the only action that makes a cell DEAD (exactly when L
is dead under R), and it never moves LIVE to DEAD (KS-T21(c)).

**Proof.** (i) `agreed(B) ⊆ Q = agreed(V)` for every block, so every term of the expectation is
zero. (ii) For B ⊆ A, agreement is antitone (`agreed(A) ⊆ agreed(B)`), hence
`Σ_{B⊆A} |B|/|V| · |agreed(B)∖agreed(V)| ≥ |A|/|V| · |agreed(A)∖agreed(V)|` block by block. (iii)
the partition of a restricted to one of its blocks is trivial, so the moved count is zero. (iv) the
answer's evidence e is fresh, so `L ⊕ {e}` is live under every R not containing e and U = 1 is always
live, which excludes DEAD; a closure sets U = L, so DEAD ⇔ L dead. Counts: 2 500 hypothesis sets
(|V| = 2…4 over 16 hypotheses), 8 irrelevant-ambiguity sets with all-zero values, 4 040 refinement
pairs (3 920 strict), 73 300 repeated-question checks, 160 + 160 query/closure interval checks (n = 3
exhaustive). **Mutants** `mutant_value_by_separation` (counts hypotheses separated instead of cells
decided on Q: asks on irrelevant ambiguity — the M4 §14 clarification-loop hostile), `mutant_never_clarify`
(regret 1 cell against the oracle on the consequential case) and `mutant_query_closes_upper` (a
speaker's answer read as a closure: mints DEAD-side certainty in 80/160 cases once the answer is
revoked) caught. The four M4 §4 cases hold in the microworld (A proceed, B clarify with value 3/4,
C refining question preferred, D repeat penalised). **Tightened**: the atlas phrase "a question
separating *more* hypotheses has higher value" is proved for *refinement* only; two incomparable
partitions need not be value-ordered (the test pins an equal-value incomparable pair). Parent: Howard
1966 value of information (verified), Rainforth et al. 2024 BED (verified) — PARENT_OWNED for the
objective; the three-valued asymmetry (iv) is WLL-5/KS-T21's corollary.

## C2 · MEG-25 · external commitment / codec gate (the renderer cannot mint support)

**Objects.** A response plan is a set of (proposition, mode) with mode ∈ {ASSERT, HEDGE, WITHHOLD};
the marker function is `μ(LIVE) = ASSERT`, `μ(UNKNOWN) = HEDGE`, `μ(DEAD) = WITHHOLD`. The honest
codec `render(plan)` is a pure function of the plan (its signature has no store parameter — the
capability half, ocap/F10); `decode(surface)` recovers (proposition, marker) pairs and the gate
compares meaning digests. The gate commits iff (G1) `digest(decode(surface)) = digest(meaning(plan))`;
(G2) every asserted proposition is LIVE at the task scope with authority ≥ the act's requirement
(`world_truth ≥ 1` for ASSERT); (G3) every rendered marker equals `μ(state)`; (G4) no protected
proposition is rendered.

**Theorem.** (i) On every state vector in {LIVE, DEAD, UNKNOWN}³ and every mode vector in
{ASSERT, HEDGE, WITHHOLD}³ (729 cases), the honest surface commits iff every *rendered* marker equals
`μ(state)`; withholding a LIVE claim is never laundering and is accepted. (ii) On all 12 honest plans
of the fixture the four planted renderers are refused: `mutant_renderer_injects_fact` (a store handle
adds a LIVE fact absent from the plan: G1), `mutant_uncertainty_dropped` (HEDGE rendered as ASSERT:
G1/G3, 6 cases), `mutant_protected_leak` (the hidden gold answer: G1/G4), `mutant_paraphrase_flips`
(negation flip of an assertion: G1, 8 cases). (iii) A speaker record LIVE as a record cannot be
asserted as world fact (authority `{speaker:1}` fails G2 — the B1 non-laundering law at the surface).
(iv) A protected proposition is refused even inside a plan (G4 is defence in depth over the
capability half).

**Proof.** (i) is the definition of G1–G3 unfolded on the honest codec (`decode ∘ render = meaning`).
(ii)–(iv) are direct: each mutant changes the decoded meaning or its marker/authority. Parent:
object-capability confinement and closed-under-shown codecs (the atlas F10 rows, verified) for the capability half;
Goguen–Meseguer noninterference (candidate, unverified) — the theorem here is the finite semantic
half, not a general noninterference proof; Rashkin et al. 2023 attribution (verified). This is the
gate `solve.commitment_gate` must grow into for M4 §8 (see the OCM notes at the end).

## C3 · MEG-27 · prefix commitment and bounded-lookahead satisfiability

**Objects.** A finite construction inventory (3 noun phrases × 5 verb phrases = 15 sentences over
tokens) whose sentences carry (claim, marker) pairs and a referent requirement; a discourse state
assigns each claim a liveness and the number of resolvable referents. `lookahead(prefix, k)` returns
SAT if an acceptable completion of remaining length ≤ k exists, UNSAT if the (finite) language has no
acceptable completion, CANNOT_CHECK if the bound cut off unfinished continuations. A prefix is
committed iff lookahead is SAT, or a registered repair act (retract-and-restart) is affordable within
the repair budget (`COMMIT_WITH_REPAIR`, never plain `COMMIT`).

**Theorem.** (i) Every committed prefix has an acceptable completion (371/371 over 60 prefixes × 18
states), every refused prefix has none (709/709): under the rule no committed prefix forces an
unsupported assertion. (ii) At the full bound the check is exact (1 080/1 080 SAT or UNSAT); below the
bound CANNOT_CHECK is refused, never committed. (iii) The token-by-token realiser reproduces the three
protected reopen cases of #8 §7: missing referent (nothing committed, reopen reference), unsupported
comparative weakened to *may be safer*, missing intermediate premise stated as a gap (*the reason is
not established*). **Mutants** `mutant_greedy_prefix` (commits whenever no claim has yet completed:
commits 709 dead-end prefixes) and `mutant_bound_is_pass` (reads CANNOT_CHECK at the bound as SAT:
commits 1 713 unsatisfiable prefixes across bounds) caught; no-alarm: with every claim LIVE and
referents resolvable, every prefix of the full assertion commits. **Tightened**: the atlas states the
rule for "the remaining construction inventory" in general; the theorem is proved for a finite
inventory with exhaustive lookahead, and the general (M6, open-inventory) case remains OPEN — the
bounded check reports CANNOT_CHECK, which is the OCM discipline. Parent: incremental sentence
planning (Cho & Boland 2025, listed in `LANGUAGE_PARENT_RESEARCH_V0.md`, unverified); lookahead in
constraint satisfaction (candidate).

## C4 · MEG-11 · small-step operational semantics of the solve pipeline

**Objects.** Configurations ⟨stage, status, payload⟩ over stages ATOMIZE → NAVIGATE → FIRE → EXTRACT
→ COMPOSE → CHECK → COMMIT; status ∈ {PASS, FAIL, CANNOT_CHECK}; typed terminals {FOUND, GAP,
OBSTRUCTION, CANNOT_CHECK}. NAVIGATE computes three-valued reachability (`r(seed) = λ(seed)`,
`r(head) = ⊕₃ over edges of λ(edge) ⊗₃ ⊗₃ r(tails) ⊗₃ λ(head)`); FIRE fires only ENABLED (all-LIVE)
edges and records each derived atom's step set; COMPOSE takes the candidate interval as the ⊗ of
seeds, fired edges, target and operator; CHECK runs the registered checker; COMMIT re-checks the
candidate's liveness.

**Theorem.** On 40 random fixtures × 8 revocation sets (320 runs, 1 056 non-terminal
configurations): (preservation) every atom marked LIVE by FIRE has a derivation whose every fired edge
and every atom on it is LIVE and whose interval is LIVE (1 376 marks); (progress) every non-terminal
configuration steps and every terminal is one of the four typed terminals (all four occur: FOUND 36,
GAP 156, OBSTRUCTION 92, CANNOT_CHECK 36); (absorption) after the first CANNOT_CHECK every later
status is CANNOT_CHECK and the terminal is CANNOT_CHECK (36 runs); (replay) persisting the fixture and
R and re-running gives the identical trace digest (320/320). **Mutants** `fire_unknown` (fires
UNKNOWN-enabled edges and marks heads LIVE: 44 LIVE marks without a LIVE derivation),
`launder` (CHECK's pass mints the candidate from its upper profile and COMMIT trusts it: 4 FOUND
terminals with a CANNOT_CHECK in the trace) and `stale_cache` (navigation cached by target only: 244
runs where the cached verdict differs from the recomputed one) caught. Parent: Wright–Felleisen 1994
syntactic type soundness (verified) for the preservation/progress shape; Bruns–Godefroid 1999
three-valued model checking (verified) for UNKNOWN as "cannot check". The pipeline order here is the
atlas order; the OCM runtime's order (navigate → extract → fire → compose → check) is a permutation
of the same rules and the theorems do not depend on it.

## C5 · MEG-10 · procedure-algebra warrant laws

**Objects.** Terms `PRIM(w)`, `SKIP`, `FAIL`, `SEQ(p,q)`, `ALT(p,q,certified)`, `IF(g,p,q)`,
`LOOP(g,p,n)` with a meter. STATIC reading: `Λ(SEQ) = ⊗`, `Λ(ALT certified) = ⊕`, `Λ(ALT uncertified)
= ⊗`, `Λ(IF) = Λ(g) ⊗ Λ(p) ⊗ Λ(q)`, `Λ(LOOP n≥1) = Λ(g) ⊗ Λ(p)`, `Λ(LOOP 0) = Λ(g)`. TRACE reading:
⊗ of what fired. Each loop iteration increments the meter; exceeding the registered bound or the
budget raises CANNOT_CHECK, never a result.

**Theorem** (exhaustive over the 20 antichain profiles at n = 3, 8 000 triples). (L1) SEQ is
associative with unit SKIP and annihilator FAIL, and its warrant commutes although the procedure does
not. (L2) certified ALT is associative, commutative, idempotent with unit FAIL. (L3) SEQ distributes
over certified ALT on both sides. (L4) guarded choice: static ≤ trace for both branch takings (6 400)
and LIVE(static) ⇒ LIVE(trace) over all revocations (51 200), strict in 2 824 cases. (L5) iteration is
idempotent in the bound (3 200), the trace of k ≥ 1 iterations is `Λ(g) ⊗ Λ(p)`, and the meter refuses
beyond bound/budget (3/3 CANNOT_CHECK). (L6) certified ALT: trace ≤ join (the atom is at least as live
as either derivation), sound only under the equivalence certificate; static ≤ trace on 217 random
programs of depth ≤ 3 with uncertified choice. **Mutants** `mutant_unmetered_loop` (returns a LIVE
result after exhaustion), `mutant_if_as_alternative` (guarded choice read as ⊕: LIVE while the taken
branch is DEAD), `mutant_static_for_trace` (KS-T26's, re-witnessed) and `mutant_alt_join_without_certificate`
(⊕ over two methods that produce different outputs: warrants an output the live method never produces)
caught. **Tightened**: the atlas "choice ⊕" is sound only for *certified* alternative derivations of one
registered function; nondeterministic/guarded choice is ⊗ in the static reading. Parent: KAT (Kozen
1997, verified), provenance semirings (Green et al. 2007, verified); KS-T26 (`ocm.kso.procedures`)
already covers L4–L5's core; C5 adds L1–L3, the meter law and the ALT/IF distinction.

## C6 · MEG-15 · discriminating-interaction certificate

**Objects.** A registered outcome function ω on scope S (the sandbox evaluates the utterance's probe);
`observe(ω, world, u, S)` returns an OBSERVATION atom about the *outcome claim* `ω(u) = o`
(EXPERIMENTATION channel, its own evidence id) or CANNOT_CHECK outside S. Elimination:
`V' = {h ∈ V : h(u) = o}`. An unregistered endpoint reward is a FEEDBACK atom with interval ⟦0,0⟧.

**Theorem.** (i) Elimination by a registered outcome never eliminates the true world (48/48 over 16
worlds × 3 in-scope probes); outside the scope no atom and no elimination exist (16 CANNOT_CHECK).
(ii) FEEDBACK admits nothing (192 checks, interval ⟦0,0⟧); `mutant_reward_as_outcome` eliminates the
true world in 96 cases, so elimination is sound iff the outcome function is registered. (iii) The
procedure's own interval is feedback-free — identical before and after any interaction —
(`mutant_feedback_raises_interval` caught, KS-T18); the claim "the procedure achieves the goal on Q"
carries the B2 per-input version-space warrant of the outcome observations, and revoking one
observation reopens exactly its per-input set ({0, 3} for the affine fixture). Parent: KWIK /
verifiable reward vs preference feedback — no verified formal parent; `KSO_CORE_PARENTS_V1.md` row 4
("reward ≠ evidence") is used as an axiom; version spaces (Mitchell 1982, PARENT_OWNED).

## C7 · MEG-16 · contradiction resolution policy over nogood-lifted intervals

**Objects.** Records `said(s, p)` / `said(s', ¬p)` (B1); a registered nogood on their joint warrant
(KS-T25, the `contradicts` link of `workspace.commit`); scoped bridges (B1) and epochs (B5). Verdict
policy: `verdict(p)` is UNKNOWN while p and ¬p are both LIVE on an overlapping scope (their joint
warrant is a nogood), otherwise the Kleene liveness of p's own nogood-filtered interval.

**Theorem.** (i) Two live records: neither promoted, machine UNKNOWN both ways, composite DEAD while
each record stays LIVE (KS-T25(iv)). (ii) Majority never resolves: up to ten more records on either
side leave both verdicts UNKNOWN (20 checks); history only grows. (iii) A scoped bridge for p resolves
the machine on its scope while the records are untouched; two bridges on an overlapping scope give
UNKNOWN exactly while both are live (16-row verdict table over R ⊆ {t1,t2,b1,b2}), and revoking one
returns the other's own liveness; disjoint scopes (epochs) are no contradiction. (iv) Retraction of one
record deactivates the contradiction without promoting the survivor. (v) Supersession (B5) is the
correction route: Γ_time ends the old record's evidence, dependents reopen exactly ({c_tue, plan}),
unrelated atoms are unaffected, history digest unchanged. **Mutants** — the four M4 §5 hostiles and one
more: correction rewrites history (digest changes), stale cached answer (LIVE before, DEAD after),
correction touches an unrelated entity (reopen set strictly larger, `note` reopened), retraction of an
un-admitted record moves world knowledge (the gazetteer atom flips), `mutant_majority_resolves`
(k ≥ 3 records ⇒ LIVE) — all caught. Parent: ATMS nogoods (de Kleer 1986, verified); the verdict policy
is the OCM rule that KS-T25 left open ("resolution policy").

## C8 · MEG-21 · non-quotient representation lifts

**Objects.** `ι: K → K'` on atoms (content, interval) and typed edges; the four-valued outcome of a
query (seeds, target) is FOUND with its answer content, GAP, OBSTRUCTION (target warrant DEAD) or
CANNOT_CHECK (UNKNOWN reachability). `admissible(K, K', ι, Q, Γ)` := ι injective and total; intervals
and contents preserved on the image; every edge of K has an image edge with mapped tails/heads, the
same interval and relation; liveness signatures over Γ preserved; on Q, every FOUND outcome is
preserved with its answer and no other outcome is degraded (`outcome' ∈ {outcome, FOUND}`).
Rollback = revoke e_J and quarantine the added structure (batch-1 T4).

**Theorem.** The M4 affine → quadratic lift (features 1, a, b + ab; AND ∉ affine span of size 8,
AND ∈ quadratic span of size 16) is admissible: the eight old procedures embed with a zero coefficient
on ab, all 8 FOUND outcomes keep their answers, the obstructed AND query improves GAP → FOUND, and
rollback restores K byte-identically. Refused: a lift changing one liveness signature, one changing a
FOUND answer's content, one dropping an edge (FOUND → GAP), one changing an edge interval, and a
non-injective (quotient) map — the last is KS-T07b's object, not this theorem's. On the exhaustive small
family (288 candidate maps of a 2-atom space into 3-atom spaces) 48 are admissible and each rolls back
exactly. **Tightened**: "four-valued outcomes preserved" is proved as *FOUND preserved with answer,
others never degraded*; full preservation would forbid the lift from ever answering the obstructed
query, which is its purpose. Parent: Abadi–Lamport 1991 refinement mappings / conservative extension
(candidate, unverified here); DPO preservation is B8.

## Consequences for the OCM build (read-only observations; nothing in ORION-OCM was touched)

* M4 §4 clarification policy = C1's `select_question` with cost/risk registered (value in cells of Q).
* M4 §8 external commitment gate = C2's G1–G4; `runtime/solve.commitment_gate` today checks candidate
  warrant/authority/scope only — no meaning-digest equality, no marker check, no protected set.
* `runtime/solve.solve` discards the enabled set of `fire_stage` (`fire_res, _ = …`), so
  `compose_stage` composes operators over the reacting subgraph regardless of enabling verdicts, and a
  FIRE-stage CANNOT_CHECK does not absorb (COMPOSE/CHECK still run; `decide` can return ANSWER; only
  the gate refuses). C4's absorption and the `fire_unknown` falsifier are the obligations.
* `dialogue/workspace.propose_promote` admits the promoted atom as IMPORTED *assumption* evidence
  (`admit_evidence` registers with `derived_from=None`; the bridge ids travel only in the payload), so
  revoking the bridge never reopens the promoted atom — B1(ii) violated; and it meets the authority
  with `Authority.of(speaker=1)`, whose undeclared `world_truth` is 0 (batch-1 T1), so every promoted
  atom has `world_truth = 0` and promotion is inert. C7's bridge semantics (warrant = the bridge's
  interval as `derived_from`, authority = operator ∧ bridge, the dialogue object as non-dependency
  provenance) is the fix.
* `workspace.commit` registers the contradiction but no verdict policy exists; C7 supplies it.
* `kso.procedures` has no metered loop and no certified/uncertified distinction for alternatives (C5).
* Open after this batch: MEG-02 (graded half), MEG-07, MEG-09, MEG-14, MEG-20, MEG-23, MEG-32,
  MEG-34, the open-inventory half of MEG-27, and the improvement halves of KS-T12/KS-T14.
