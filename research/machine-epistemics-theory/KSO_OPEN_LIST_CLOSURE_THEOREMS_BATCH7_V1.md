# KSO open-list closure theorems — batch 7 (G1–G9)

Date 2026-09-05. Seventh one-day batch over the machine-epistemics gap atlas
(`ME_THEORY_GAP_ATLAS_V1.md`). Scope: every item still OPEN on the atlas open list after batch 6
(§J) — MEG-28 J4+ ceilings, MEG-07 per-source normalisation, MEG-27 non-regular acceptability,
MEG-19 deconsolidation decision, KS-T12/KS-T14 improvement halves, MEG-02 (+,×) reading, MEG-34
SHRG/CCG half — plus two questions raised by the M12 read-only inputs (reference-arm grading,
`M12_REFERENCE_ARM_V1.json` / `lifetime/reference.py`; the V3 paired-lifetimes design,
`M12_V3_PAIRED_LIFETIMES_DESIGN_V1.md`). Each item is closed as PROVED, or bounded exactly (an
impossibility with a witness, or PARENT_OWNED with the executable rule and its falsifier). After this
batch the open list is empty; what remains is the list of exactly-bounded impossibilities in §K of
the atlas.

Every item has an exact finite checker (`kso_open_list_closure_batch7_exact.py`, stdlib only,
probabilities and sizes exact `Fraction`; the only float is the ranking value a·ln(a/π), and every
ranking decision it supports is also asserted by exact dominance; exit 0 / 1 / 2 with 2 =
CANNOT_CHECK), at least one planted hostile whose mutation is asserted applied and caught, and a
no-alarm control; `tests/unit/test_kso_open_list_closure_batch7.py` pins every count. Checker run on
billy-old (Python 3.14.4): exit 0, wall 3.7 s, `"status": "ALL_HOLD"`, `"OPEN": []`; 13/13 tests;
batches 1–7 together 89/89. All objects are re-implemented inside the checker (antichain semiring,
intervals, Kleene liveness, the exact restart walk of `ocm.kso.navigation`, the batch-5/6 Boolean
towers, the batch-5 B7 chain, a context-free inventory with a product fixed point); nothing imports
`ocm`; nothing ran on the Mac.

NO NOVELTY OR SUPERIORITY CLAIM. Every lattice, counting, automata-theoretic or statistical fact used
is a named parent's; the contribution is the exact statement on OCM objects, the executable
falsifier, and the reading of the M12 inputs. Where an atlas or design wording could not be proved it
is marked **tightened** or **refuted** with the counterexample recorded.

Notation as in batches 1–6: `E` evidence universe, `R ⊆ E` revoked set, antichain (⊕, ⊗) semiring,
interval `⟦lo, up⟧`, liveness LIVE / DEAD / UNKNOWN (KS-T21), `cert(w)` a certificate interval.

## G1 · MEG-28 · ceilings beyond the 3-input tower: depth-4 exact; J4 relative to a registry; J5 has no uniform ceiling

**Objects.** The 65 536 Boolean functions of four inputs packed as 16-bit tables; ANF by the Möbius
butterfly; the nested tower `S_ℓ = {deg ≤ ℓ}`, ℓ = 1…4 (sizes 32 ⊂ 2 048 ⊂ 32 768 ⊂ 65 536).
`C_ℓ(q)` := `q ∉ S_ℓ` with a witness monomial of degree > ℓ whose sub-cube parity is odd (checked
independently of the butterfly). `minimum_level`, `assess_jump` and the trigger built from the
incumbent level's certificate are batch-6 F7's, at any depth. *J4 (problem reformulation)* over a
registered class Φ of input bijections: `S_ℓ^Φ := {q ∘ φ : q ∈ S_ℓ, φ ∈ Φ}`. *J5 (tool
invention)* over a registered tool class 𝒯: `S_1^𝒯 := ⋃_{t∈𝒯} span(affine ∪ {t})`.

**Theorem.** (i) *Depth-4 tower exact* (65 536 targets): `minimum_level(q) = max(1, deg q)`; every
ceiling certificate carries an independently checked witness (65 504); the governed Jump from
incumbent ℓ to ℓ′ is `CANDIDATE_FOR_PROTECTED_EVALUATION` iff `ℓ′ = minimum_level(q) > ℓ`
(393 216 checks): skipping a sufficient level is refused (65 472 `NO_JUMP_NEEDED_LOWER_LEVEL_SUFFICIENT`),
an insufficient proposal is refused (129 024), a target inside the incumbent level has no trigger; a
missing level-3 ceiling oracle makes the minimum level `CANNOT_CHECK` for every target above level 2
(63 488), never a jump to level 4. (ii) *J4 is a function of the registry, not of the target.* Under the
1 344 invertible affine maps of GF(2)³ the ANF degree is invariant (344 064 checks), so
`S_ℓ^Φ = S_ℓ` at every level: an affine reformulation never gains a function (gain 0 at levels 1 and 2).
Adding one registered non-affine bijection (the transposition 000 ↔ 001) to Φ gives `S_1^{Φ′} ⊋ S_1`
with 8 new degree-2 functions (witness table 86): the same target has a level-1 ceiling under Φ and
none under Φ′. (iii) *J5 has no uniform ceiling.* With an unrestricted tool class the predicate
"q ∉ span(affine ∪ {t}) for every tool t" is identically false — the tool `t = q` witnesses it for all
240 non-affine targets — so "minimum sufficient level" is undefined across J5 unless the tool class is
registered; with the registered class {xy, yz, xz, xyz} the one-tool level has exactly 80 functions and
176 targets carry a decidable J5 ceiling (e.g. xy ⊕ yz needs two tools).

**Proof.** (i) enumeration; degree = minimum level is the Reed–Muller order. (ii) an invertible
affine substitution permutes monomials of equal degree; the transposition is a non-affine point
permutation, and `x₀ + (1+x₁)(1+x₂)` = `x₀ ∘ σ` is degree 2. (iii) `q = q ⊕ 0` lies in
`span(affine ∪ {q})`. ∎

**Hostiles.** `mutant_partial_level3_degree` (a level-3 enumerator that never forms the cubic
monomial yzw) certifies a false ceiling on all 16 384 degree-3 targets that contain it — caught
against the honest certificate. `mutant_poor_score_trigger` refused on every probed target (256).
`mutant_uniform_reformulation_ceiling` (a J4 ceiling read off the degree while the registry contains
σ) certifies a ceiling on a reachable target — caught. `mutant_unregistered_tool` ("a tool exists":
t = q, not in 𝒯) — caught by the registry check (E3(iii)). **No-alarm:** affine targets produce no
trigger at any proposed level (96).

**Status.** PROVED on the depth-4 tower; J4 PROVED relative to a registered reformulation class with
the registry-dependence witness; J5 uniform ceiling IMPOSSIBLE (exact, vacuous) and decidable only per
registered finite tool class. **Tightened:** MEG-28's "minimum sufficient level is well defined iff
each level has a decidable ceiling predicate" holds verbatim for J1–J3 (degree levels) and for
J4/J5 only after the level's class is registered — the class is part of the level, not of the target.
Parent: Reed–Muller / ANF degree, affine invariance of degree (classic); CEGAR / BMC completeness
thresholds — PARENT_OWNED; batch-5 E3, batch-6 F7 (PROVED).

## G2 · MEG-07 · per-source normalisation: what can and cannot rescue the M2.1 misses

**Objects.** The exact restart walk `a = α s + (1−α) Pᵀ a` (row-normalised, substochastic, exact
rational solve) on the M2.1 finding-1 shape: request atom r with fan-out 13, five popular sources
feeding every child, one grand-child per child, two further seeds; query seed uniform on three atoms,
α = 1/5; background π = the walk from the uniform seed. Surprise sign: `ρ_Q(v) > 0 ⇔ a_Q(v) > π(v)`
(exact; `a·ln(a/π) > 0 ⇔ a > π`). Registered structural clause: `G_Q := {ρ > 0} ∪ supp(S) ∪ {LIVE
one-hop heads v of s ∈ supp(S) with in-share 1/out(s) ≥ σ}`, σ = 1/16.

**Theorem.** (0) The miss is reproduced exactly: every child has `a_Q = 4/975 < π = 89/11050` (13/13)
although each is LIVE, one hop from the request atom, with in-share 1/13 ≥ σ; the request atom itself
is surprise-positive. (i) *Monotone impossibility.* Any functional φ(a, π) nondecreasing in a,
nonincreasing in π and with φ(x, x) ≤ 0 (KS-T06) satisfies φ(a, π) ≤ 0 whenever a ≤ π
(`φ(a,π) ≤ φ(a,a) ≤ 0`): no re-normalisation of the same pair admits the misses (log-ratio, difference,
ratio − 1 all exclude all 13; 39 checks). (ii) *Matched-cardinality background is a placebo.* For every
seed cardinality m, the mean activation over all seed sets of size m equals the uniform-seed background
(linearity of the fixed point in the seed): exhaustive on a 7-atom graph over all 127 seed sets. (iii)
*Structural clause.* All 13 children enter `G_Q`, no grand-child does, the added set equals the clause's
cone bound `Σ_s min(k_s, ⌊1/σ⌋)` = 13, a revoked child never enters (DEAD gating), and the surprise
values are untouched (the clause reads a and π, never writes them). KS-T06 (uniform seed ⇒ zero surprise
everywhere, the hub included) and KS-T06b (a seed touching hub h and specific x: `a(h) = a(x)`,
`π(h) > π(x)` ⇒ x surprise-positive, h not, h first by popularity; hub-only seed ⇒ h first by both) hold
on the hub fixture with the clause in place.

**Proof.** (i) two inequalities; (ii) `a* = α(I − (1−α)Pᵀ)⁻¹ s` is linear in s and the mean of the
uniform-on-S seed vectors over all S of size m is the uniform seed; (iii) enumeration on the fixture.
∎

**Hostiles.** `mutant_seed_conditioned_background` (background := the walk from the same seed support
with uniform weights) equals `a_Q` exactly, so every atom — the request atom included — is dropped:
caught by no-drop. `mutant_rescaled_background` (π·|S|/N) admits the 13 children but also the 13
grand-children (a < π, two hops): caught by the cone bound. `mutant_attribution_ratio` (per-source
reactivity N·w_s for every atom reached from s) ties the hub with the specific atom (8 = 8): KS-T06b's
strict order is lost — caught. **No-alarm:** with σ = 1 the clause is inert and `G_Q` equals the
surprise set plus seeds.

**Status.** PROVED. **Tightened:** the atlas's two candidate levers are settled: "background at
matched seed cardinality" is inert (ii) — independently the OCM's own
`ocm.kso.surprise.check_seed_count_lemma` records the same fact — and "degree-normalised reactivity"
as a per-source ratio destroys ranking; a lever must either change the *pair* (as the OCM's registered
PROPAGATED model does: propagated mass against propagated background, re-checked against T06/T06b) or
add a registered structural clause with a cone bound. G2 does not adjudicate between those two; it
proves what no lever of the first kind can do. Parent: topic-sensitive PageRank (Haveliwala 2002),
personalised-PageRank contribution vectors (Andersen–Chung–Lang 2006, as cited by the OCM module),
IDF — PARENT_OWNED; KS-T05 linearity, KS-T06/T06b (registered design choice).

## G3 · MEG-27 · context-free inventory: exact prefix commitment, the completeness threshold, and the honest boundary

**Objects.** The inventory `S → NP VP | NP REL S VP` (centre embedding), `NP → N`, `VP → V`, seven
tokens (three referents, `that`, three claims). Discourse state: resolvable referents (⊆ 3), claim
liveness (c1, c2, c3 ∈ {LIVE, DEAD}), referent budget m ∈ {1, 2, 3} — 192 states. Acceptability per
token is regular given the state (referent resolvable and within budget; claim LIVE). Prefix
configurations = the finite set of (stack, used-referents) after an LL parse of the prefix (no left
recursion). *Exact decision:* `gen[X][U]` = used-sets reachable after generating X acceptably from U —
a least fixed point over a finite lattice; SAT iff some configuration's stack folds to a non-empty set.
*Bounded lookahead* `cf_bounded(prefix, k)`: SAT if an acceptable completion of ≤ k tokens exists,
UNSAT only if every continuation died with nothing pruned, else CANNOT_CHECK. *Threshold*
`ℓ*(prefix, state)`: the exact shortest acceptable completion from the min-plus table
`ml[X][U][U′]` (a second, independent fixed point).

**Theorem** (61 prefixes × 192 states = 11 712 cases, bounds 0…5). (i) The set fixed point and the
min-plus table agree on SAT/UNSAT (11 712/11 712). (ii) A decisive bounded verdict never contradicts
the exact decision (64 356 agreements, 5 916 CANNOT_CHECK, each decided by the fixed point). (iii)
*Completeness threshold:* on every SAT case the bounded check is SAT exactly at k ≥ ℓ* and
CANNOT_CHECK below it (2 643/2 643; ℓ* histogram 0:432, 1:972, 2:567, 3:252, 4:420); on the 213 UNSAT
cases whose prefix is valid but whose claims are all DEAD no bound ever decides — only the fixed point
does. (iv) *No prefix-independent bound:* the nested prefix with d open clauses has ℓ* = d + 1
(d = 0…4), so for every fixed k the prefix with k open clauses is SAT yet CANNOT_CHECK at k. (v) A
budget-exhausted prefix is a genuine UNSAT decided exactly; a regular approximation of the inventory
(the DFA `N (REL N)* V+`, nesting forgotten) accepts the prefix `cat chased ran`, which is outside the
inventory (exact: UNSAT).

**Proof.** Fixed points on finite lattices; the bounded search prunes only stacks longer than the
remaining budget (a stack symbol emits ≥ 1 token), so it never loses a completion of length ≤ k;
enumeration. ∎

**Hostiles.** `mutant_bound_is_pass` (CANNOT_CHECK read as SAT) commits 1 374 unsatisfiable
(prefix, state, bound) cases; `mutant_fixed_bound_is_unsat` (CANNOT_CHECK read as UNSAT) refuses
4 542 committable cases — the realiser stalls; `mutant_regular_approximation` commits a prefix outside
the inventory. **No-alarm:** with every claim LIVE, all referents resolvable and budget 3, every prefix
of a full sentence commits.

**Status.** PROVED for a context-free inventory with a state-regular acceptability predicate: the exact
decision exists (product fixed point), the bounded check is complete iff `k ≥ ℓ*` with ℓ* computable
from the min-plus table, and ℓ* is unbounded over prefixes. **The honest boundary:** CANNOT_CHECK is
the only honest answer of a bounded checker exactly when no completeness threshold is available; that
is the case when the acceptability predicate is itself context-free (nesting-dependent anaphora,
balanced obligations), since prefix commitment is then emptiness of the intersection of two
context-free languages — undecidable in general (Bar-Hillel–Perles–Shamir 1961; PCP). PARENT_OWNED,
cited, not checked (no finite fixture can exhibit undecidability). Parent: Bar-Hillel (CFL ∩ REG),
emptiness / shortest-word fixed points (Knuth 1977), Cho & Boland 2025 (listed, unverified) — batch-3
C3, batch-5 R2 (PROVED).

## G4 · MEG-19 · the deconsolidation decision: the parent's rule, executable, and what is not the parent's

**Objects.** A macro m over k constituents, `u` uses, `e` registered exceptions, each exception an atom
with its own warrant; the two-part code (Rissanen; the DreamCoder/LILO library objective) with the
fixture's symbol costs: without the macro `u·k`; with it `(k+1) + u + e·(k+1)`.

**Theorem.** (i) *MDL decision, closed form* (315 cases, k ≤ 5, u ≤ 8, e ≤ 6): KEEP iff
`(k+1)(1+e) ≤ u(k−1)`; a one-constituent macro never pays; crossover uses at k = 3: 2, 4, 6, 8 for
e = 0…3 (table recorded). (ii) *Not parent-owned (a):* an exception counts only while LIVE — on
{g1, g2, g3} under every revocation set the LIVE count is `3 − |R|`; counting DEAD exceptions splits a
macro the honest rule keeps on all 7 non-empty revocation sets (k = 3, u = 6). (iii) *Not parent-owned
(b):* MDL-keep is not navigation gain: k = 2, u = 8, e = 0 keeps (11 ≤ 16) while navigation on
Q = {t, x1} worsens 4 → 5 (E8 witness); it improves only on Q ⊆ exports (3 → 2). (iv) *Not parent-owned
(c):* the decision is a proposal; adoption needs the external commit (batch-5 E4). (v) The exactness
half (R1: split restores the constituent space byte-identically, export liveness unchanged over Γ)
stands as proved in batch 5.

**Proof.** Arithmetic; enumeration. ∎

**Hostiles.** `mutant_count_dead_exceptions` — premature split on 7/7; `mutant_mdl_implies_navigation_gain`
— refuted on the E8 fixture. **No-alarm:** no exceptions, long macro, many uses: both counts agree,
KEEP.

**Status.** PARENT_OWNED decision (MDL two-part code; DreamCoder Ellis et al. 2021, LILO), executable
with its closed form and falsifier; PROVED that the LIVE-gating of the exception count, the exactness
of undo, the governance of the split, and the non-identity of MDL gain with navigation gain are OCM
obligations no parent supplies. **Tightened:** the atlas's `PARENT_SUFFICIENT` expectation is
confirmed for the objective and refuted for its scope (which exceptions count) and its authority.

## G5 · KS-T12 / KS-T14 · the improvement halves as exact clauses; the unconditional forms refuted

**Objects.** Batch-5 E8's fixtures: the chain `s → x1 … xk → t` consolidated to `s → m → t` with only t
exported, navigation cost = breadth-first edges traversed, batch-4 D7's coarse-first rule (a coarse GAP
costs the coarse walk plus the fine walk); the four features {1, a, b, ab} with the XOR-span ceiling
`|Q ∩ span(R)|`.

**Theorem.** (i) *KS-T12, exact clause on the chain family* (k = 1…6, every non-empty Q ⊆ internals ∪
{t}: 246 cases): `gain(Q) = (k−1)·[t ∈ Q] − 2·|Q ∩ internals|`, so consolidation improves iff
`(k−1)[t∈Q] > 2|Q∩internals|`; for Q ⊆ exports it is never worse and improves iff k ≥ 2 (smallest
holding fixture k = 2, Q = {t}: 3 → 2). The unconditional statement is **refuted**: k = 1, Q = {x1}
costs 1 → 3. (ii) *KS-T14, exact clause* (all 256 feature-set pairs × 4 query families = 1 024 cases):
if `span(R) ⊆ span(R′)` (a nesting: the DPO interface keeps every feature) the ceiling never drops
(324/324) and improves on Q iff `Q ∩ (span(R′) ∖ span(R)) ≠ ∅` (324/324) — i.e. the E3 certificate at R
plus reachability in R′; a non-nested rewrite lowers the ceiling in 281 cases, the S6 shape being
R = {1, a, b} → R′ = {1, ab} on Q = {XOR}: 1 → 0. The unconditional statement is **refuted** by that
witness.

**Proof.** (i) `before(t) = k+1, after(t) = 2; before(x_j) = j, after(x_j) = 2 + j`; (ii) set arithmetic
on spans. ∎

**Hostiles.** The two unconditional laws, planted as predicates, contradict the recorded
counterexamples. **No-alarm:** Q ⊆ exports at k = 2 improves; AND under affine → quadratic improves
(0 → 1).

**Status.** PROVED (exact clauses on the recorded fixtures — theorems, not conjectures);
CONJECTURE status of E8 retired; unconditional forms REFUTED with the counterexamples as witnesses.
**Tightened:** the registry entries KS-T12/KS-T14 should carry the clauses `Q ⊆ exports` and
`span(R) ⊆ span(R′)` respectively; outside them the sign is a per-query fact, not a law. Parent: BFS
cost, linear span (classic); batch-2 B7/B8, batch-4 D7, batch-5 E3/E8.

## G6 · MEG-02 · the (+,×) reading as a measure over warrants: what it licenses without being a homomorphism

**Objects.** Ids {a, b, c} with grades g(e) ∈ (0, 1) read as independent truth probabilities; worlds
ω ⊆ E with the product law; a derivation family D (antichain) is *supported* in ω iff some alternative
d ⊆ ω survives R (d ∩ R = ∅); `μ_R(D) := P(supported)`, exact by world enumeration (revoked ids are
made unusable, not conditioned on). The homomorphic sum `h(D) = Σ_d Π_{e∈d} g(e)`.

**Theorem** (20 antichains = Dedekind M(3), two gradings). (i) *Valuation:* `μ(D₁ ⊕ D₂) = μ(D₁) +
μ(D₂) − μ(D₁ ⊗ D₂)` (800/800) and μ is monotone in the antichain order (336). (ii) *Not a
homomorphism:* `μ(D₁ ⊗ D₂) = μ(D₁)·μ(D₂)` on every evidence-disjoint pair (188) and on no pair that
shares an id (612 strict failures; Harris–FKG strictness for increasing events with a common relevant
coordinate). (iii) `h(D) = μ(D)` iff |D| ≤ 1 (40); h exceeds 1 (D = {{a},{c}}: 7/6 vs 5/6). (iv)
*Retraction is exact:* `μ_R(D)` equals μ of the surviving alternatives (320). (v) *What it licenses:*
for any batch of atoms, `E[#supported] = Σ_i μ_i` under sharing (1 540 batches, linearity of
expectation) — the expectation receipt needs no independence across atoms; a *concentration* receipt
`P(#supported ≥ n(1−δ))` needs the joint law: the independent (Poisson-binomial) value is wrong on
1 404 shared batches and right on the 77 pairwise-disjoint ones. (vi) The measure is never a warrant:
an interval ⟦0, {a}⟧ with μ(up) = 9/10 is UNKNOWN (KS-T21); the R3 witness reads 1/2 (double count)
vs the exact 3/8.

**Proof.** Inclusion–exclusion on events; independence of disjoint coordinates; linearity;
enumeration. ∎

**Hostiles.** `mutant_independent_coverage` — 1 404 wrong concentration claims; `mutant_measure_promotes_liveness`
(μ > ½ ⇒ LIVE) — caught by KS-T21. **No-alarm:** a single derivation: sum, measure and product rule
coincide.

**Status.** PROVED (finite). The (+,×) reading is admissible as a *measure* that licenses scoped
expectation receipts (batch-4 D3's coverage bridge is exactly such a receipt) and exact retraction;
it is not, and cannot be made, a semiring homomorphism once evidence is shared; concentration claims
must enumerate the joint law (or bound it). Measure facts PARENT_OWNED: provenance semirings
(Green–Karvounarakis–Tannen 2007), probabilistic databases / #P-hardness of the general case
(Valiant 1979, Dalvi–Suciu 2007), Harris–FKG.

## G7 · reference-arm grading: "licensed by the given information" vs "true"

**Objects.** The 24 verified triples of `KNOWLEDGE_MANIFEST_V1` that the M7 factual suite uses, with
the registered closure rules (transitivity of LOCATED_IN and IS_A: closure 28); the twenty
`OUT_OF_SCOPE` questions of `m7_comparison.py` as triples with their world truth (all twenty are false
in the world); a balancing companion of ten world-true triples equally unsettled by the manifest.
`Lic_K(q)` := YES iff `q ∈ Cn(K_verified)`, NO iff `¬q ∈ Cn(K_verified ∪ registered negative rules)`,
UNKNOWN otherwise. **Grading rule:** on a licensed question, correct iff the answer equals the licence;
on an UNKNOWN-licensed question only UNKNOWN is `LICENSED_CORRECT`, an assertion is
`UNLICENSED_TRUE` or `UNLICENSED_FALSE` (evidence of a channel outside K), never "correct". Three
arms: honest (answers the licence), unbound reference (answers the world), K-only constant policy
(licence where one exists, NO otherwise).

**Theorem.** (i) The licence is a function of (K, rules), never of the world: with the manifest's
rules every out-of-scope item is UNKNOWN (20/20) and every in-scope item YES (26/26); registering one
negative rule (functional LOCATED_IN) makes four of them licensed NO. (ii) The M12 reference row is
reproduced exactly: the unbound arm scores 0/20 licensed with 20 `UNLICENSED_TRUE` ("always attempts
20"), 26/26 in scope; the honest arm 20/20. (iii) *Truth grading rewards the channel and cannot detect
it:* under the truth grader the unbound arm scores 20/20 and so does the K-only constant policy —
on a suite whose UNKNOWN-licensed items are all world-false the two are indistinguishable — while the
honest arm scores 0/20. (iv) *Balanced suite as channel detector:* on 10 true + 10 false
UNKNOWN-licensed items the truth grader gives honest 0, constant policy 10, unbound 20; a K-only
guesser reaches ≥ 18/20 with probability exactly 211/1 048 576; the licensed grader gives honest 20,
both others 0.

**Proof.** Closure computation; enumeration; exact binomial. ∎

**Hostiles.** `mutant_truth_grader` (correct = agrees with the world) — rewards the channel (20/20)
and is blind to the constant policy (20/20). **No-alarm:** on in-scope items every arm and both
graders agree (26/26).

**Status.** PROVED (finite). The reference arm's `honest_unknown 0/20` is the correct reading of an
unbound channel under the licensed rule, and its 28/30 in-scope row is comparable only there; the V3
out-of-scope suite should be balanced in world truth if the reference row is to *detect* the channel
(it cannot grade it). Parent: F8 (batch 6) information binding; selective classification / abstention
(Chow 1970); closed-world assumption vs licence (Reiter 1978) — PARENT_OWNED.

## G8 · M12 V3 paired lifetimes: exact sizes and powers, multiplicity, the exchangeability condition and its leaks

**Objects.** m = 8 paired lifetimes, per-family lifetime differences, the exact sign test (ties
dropped), the per-lifetime score vector of F families; seeded lexical substitution σ (injective,
identity on registered words, image inside the fresh vocabulary), deterministic arms.

**Theorem.** (i) *Sizes/powers, one-sided:* reject iff ≥ 7/8 (size 9/256 = 0.035; ≥ 6/8 has size
37/256), power 0.813 at p = 0.9, 0.503 at 0.8, 0.255 at 0.7; with ties m = 7, 6, 5 need 7/7, 6/6, 5/5
and m = 4 cannot reject. *Two-sided:* only 8/8 rejects (2/256); 7/8 has p = 18/256 = 0.070. (ii)
*The implemented rule* (`m12_paired_eval.sign_test`: two-sided p and unanimity): size 1/128 per family,
power p⁸ = 0.430 at p = 0.9; the decision "RESIDUAL iff ≥ 1 of F families rejects in OCM's favour"
keeps the family-wise error ≤ α (independent families) only for F ≤ 6 (F = 7: 0.0533). With the
one-sided ≥ 7/8 rule, F ≥ 2 families need Bonferroni at 8/8 (α/F ≥ 1/256 up to F = 12; F = 13 cannot
reject). (iii) *EQUIVALENT rule* ("every difference within margin") has no size: P(all 8 inside) =
(1−q)⁸ for per-lifetime exceedance q. (iv) *Exchangeability:* if both arms are deterministic and
equivariant under the substitution, and the eight lifetimes share their non-substitution variation,
the eight differences are identical (24 valid substitutions, one distinct difference) — the sign test
is then one coin (size 1/2, never α); distinct i.i.d. variation draws (ordering, drift/revision
events) give distinct differences and the binomial size. (v) *Leaks:* a substitution that maps a fresh
word onto a registered word makes a K-only arm answer before any lesson (refused
`REFUSED_COLLISION_WITH_REGISTERED`); a pattern that is a sub-sequence of the question is passed by an
echo arm (refused by `echo_leak`); valid substitutions leak nothing (0/72 items). (vi) The secondary
exact paired test stays inside one lifetime (1/64 each at 6 discordant wins); pooling 48 items across
lifetimes multiplies the evidence (F2) and is refused.

**Proof.** Exact binomial arithmetic; enumeration of substitutions; the collapse is the F2
pseudo-replication in paired form. ∎

**Hostiles.** Collision and echo substitutions — caught; pooled items — refused; the one-coin collapse
— exhibited. **No-alarm:** 24/24 valid substitutions and i.i.d. variation reproduce the binomial.

**Status.** PROVED (exact). **Tightened:** the V3 design text's "8 gives power 0.81 at p = 0.9" is the
one-sided ≥ 7/8 rule; the implementation's unanimous two-sided rule has power 0.43 — one of the two
must be re-registered before the freeze, and the multiplicity clause (F ≤ 6 families, or a
pre-registered primary family) added. Parent: exact sign test, Bonferroni, Hurlbert 1984 (F2),
exchangeability / permutation-test null (Fisher; Lehmann–Romano) — PARENT_OWNED.

## G9 · MEG-34 SHRG/CCG half: positive aligned pairs cannot identify a superfinite inventory class

**Objects.** Inventories `L_n` (at most n conjuncts: `NP (CONJ NP)^{≤ n−1} VP`, n = 1…6) and `L_∞`
(unbounded conjunction); positive texts of `L_∞`; a registered membership query (the batch-3 C6
discriminating interaction).

**Theorem** (finite witness of Gold's argument). (i) Every positive sample of `L_∞` of length ≤ j is a
sample of `L_j`: no finite positive text separates `L_∞` from a finite member (6/6); the smallest
non-separating sample is {NP VP}. (ii) A learner that identifies every finite `L_n` from positive data
conjectures `L_j` after the j-th sentence of the text of `L_∞` and never converges (the planted
`mutant_positive_only_identifies` locks on the finite language, 6/6) — the tell-tale condition fails
for `L_∞` (Angluin 1980). (iii) One registered membership query (the sentence with j conjuncts)
separates `L_j` from `L_∞` (6/6). **No-alarm:** the finite class {L_1…L_6} alone is identified from
positive data.

**Proof.** Set inclusion on the fixture; Gold 1967 for the limit statement (cited). ∎

**Status.** PARENT_OWNED, exactly bounded: the open half "which aligned-pair distributions identify
SHRG/CCG-class inventories up to ≡_L" has the answer *none that are positive-only over a superfinite
class*; identification needs the registered query/negative channel (C6), which the OCM has. The
≡_L lifecycle refinement (per-input warrant signature) is batch-4 D6 (PROVED, finite). Parent: Gold
1967, Angluin 1980 (tell-tales), Kanazawa 1998 (k-valued categorial grammars, candidate, unverified).

## Consequences for the OCM build (read-only observations on `ORION-OCM-wt/m11-self`; nothing touched)

File states read on 2026-09-05. Each item names the runtime obligation the theorem makes concrete;
none is a claim about an M12 result.

* **G1 — the level is (tower, registered class), never a bare integer.** `src/ocm/kso/jump.py::assess_jump`
  (line 128) takes `lower_level_sufficient` as a caller-supplied boolean and `minimum_level` (line 155)
  returns the *lowest proposed* complete proposal, not the minimum *sufficient* level. Obligation: a
  registered tower object with a per-level ceiling enumerator (degree for J1–J3; the reformulation
  class Φ for J4; the tool class 𝒯 for J5), `lower_level_sufficient` computed from it, and
  `CANNOT_CHECK` when a level's enumerator is missing; a J4/J5 proposal without its registered class is
  `JUMP_PROPOSAL_INCOMPLETE`.
* **G2 — where the no-drop clause attaches; what the registered lever must show.**
  `src/ocm/kso/extraction.py::reacting_subgraph_from_surprise` builds `atoms = {ρ > 0} ∪ support`;
  the structural clause is one more union term (LIVE one-hop heads with in-share ≥ σ, σ registered,
  cone bound recorded in the receipt). `src/ocm/kso/surprise.py` already records the seed-count no-op
  lemma (`check_seed_count_lemma`) and the PROPAGATED model; G2(i) says PROPAGATED is admissible only
  because it changes the pair (b_Q, b_π), so `check_hub_theorem_under_model` (T06/T06b) is a
  precondition of registration, not a post-hoc check; `m21_surprise_revival.py`'s expectation (iv)
  "no live request atom lost that UNIFORM had found" is the no-drop half restricted to UNIFORM's
  finds — the clause covers the 12 misses UNIFORM never found.
* **G3 — M6 incremental realiser.** Batch-5 R2's obligation (reachability for regular inventories)
  extends to context-free inventories: the exact decision is the product fixed point, and the bounded
  check may report SAT/UNSAT only with a threshold certificate `k ≥ ℓ*`; `runtime/solve.commitment_gate`
  (line 363) commits on outcome, not on prefix — the incremental path must carry the CANNOT_CHECK
  branch verbatim and never approximate the inventory by a DFA.
* **G4 — M8 split policy.** The MDL rule is executable as a pure function of (k, uses, LIVE
  exceptions); the exception ledger must be warrant-bearing atoms whose liveness gates the count; the
  split is a `SelfChangeProposal` (batch-5 E4), and its expected navigation effect must be predicted
  per registered Q, never inferred from the code length.
* **G5 — registry wording.** `KSO_OBLIGATION_REGISTRY_V1` entries KS-T12 and KS-T14 can move from
  OPEN to PROVED-with-clause: KS-T12 needs `Q ⊆ exports` (gain formula on the chain family), KS-T14
  needs `span(R) ⊆ span(R′)` (nesting) — the S6 benchmark oracle is exactly the non-nested case.
* **G6 — `kso/warrant.WarrantProfile`.** A grade per alternative may carry a (max,×) value (batch 6
  F6) or a measure μ (this batch); μ licenses `Σ μ_i` expectation receipts and exact retraction, must
  enumerate (or bound) the joint law for any concentration receipt, and never sets liveness — batch-4
  D3's score-outside-lattice rule stands.
* **G7 — `lifetime/reference.py::_expect` / `phase_A_reference`.** `_expect("I do not know") =
  {"unknown"}` already grades by licence; the report should carry the four-class vector
  (licensed / unlicensed-true / unlicensed-false / wrong) so "0/20" reads as "20 unlicensed-true", and
  `m7_comparison.OUT_OF_SCOPE` (line 34; all twenty world-false) should get a world-true balancing
  half before the V3 freeze if the reference row is meant to detect the channel.
* **G8 — `evaluation/m12_paired_eval.py::sign_test` (line 77) and `lifetime/streams.py`.** The
  implemented rule is two-sided and unanimous (size 1/128, power 0.43 at p = 0.9); the design text's
  power 0.81 is the one-sided ≥ 7/8 rule — re-register one of them before the freeze; the decision
  "≥ 1 family rejects" needs the family count bounded (≤ 6 at α under the unanimous rule) or a
  pre-registered primary family. `streams.py` bans manifest words for nonce lessons (collision leak
  refused by construction) and `leak_check` covers the pattern leak; the remaining obligation is the
  collapse gate: a family whose eight lifetime differences are identical is one coin — report it
  `COLLAPSED_ONE_COIN`, never RESIDUAL (V2's phase-A vectors were byte-identical across orderings, so
  substitution-equivariant families are at risk).
* **G9 — `ocm.language.acquisition` (M3).** Identification of a construction inventory must record
  the channel: positive aligned pairs alone cannot close a superfinite class; the C6 discriminating
  interaction (membership/negative) is the closing channel and belongs in the identifiability receipt.

```text
G1  MEG-28 J4+       PROVED depth-4 tower; J4 exact per registered class (witness); J5 uniform ceiling IMPOSSIBLE (t = q), decidable per registered class
G2  MEG-07           PROVED: monotone re-normalisation impossible (KS-T06); matched-cardinality background inert; structural clause no-drop with cone bound
G3  MEG-27           PROVED (CF inventory, state-regular acceptability; threshold ℓ*; no prefix-independent bound); CF acceptability PARENT_OWNED (undecidable)
G4  MEG-19           PARENT_OWNED decision (MDL) executable + falsifier; PROVED LIVE-gating, exactness, governance, MDL ≠ navigation gain
G5  KS-T12 / KS-T14  PROVED exact clauses (chain gain formula; nesting ⇒ monotone, improves iff Q meets span difference); unconditional forms REFUTED
G6  MEG-02 (+,×)     PROVED (finite): valuation, exact retraction, expectation receipts under sharing; not a homomorphism; measure facts PARENT_OWNED
G7  reference grading PROVED (finite): licence = f(K, rules); grading rule; truth grading rewards the channel and is blind to a constant policy; balanced suite detects
G8  paired lifetimes PROVED (exact): ≥ 7/8 one-sided (0.813 at 0.9) vs unanimous two-sided (0.43); F ≤ 6 families; i.i.d. variation required; leaks refused
G9  MEG-34           PARENT_OWNED, exactly bounded (Gold 1967 / Angluin 1980); registered query channel separates
OPEN: none
NOVELTY NOT_ESTABLISHED
```
