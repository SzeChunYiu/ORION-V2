# KSO comparison-prerequisite theorems — batch 4 (D1–D8)

Date 2026-09-05. Fourth one-day batch over the machine-epistemics gap atlas
(`ME_THEORY_GAP_ATLAS_V1.md`), chosen as the gaps the OCM M7 milestone (protected comparison against the
strongest faithful parent: pre-registration, matched information/resource accounting, equivalence
testing, ablations, laundering audit — `ORION-OCM` issue #9) and the M8 organisation work need proved,
defined or tabulated. Every item has an exact finite checker (`kso_comparison_prereqs_batch4_exact.py`,
stdlib only; exit 0 / 1 / 2 with 2 = CANNOT_CHECK), at least one planted mutant asserted applied and
caught, and a no-alarm control; tests in `tests/unit/test_kso_comparison_prereqs_batch4.py` pin every
count. Checker run on billy-old: exit 0, wall 2.1 s; 12/12 tests. Objects (antichain semiring, warrant
intervals, Kleene liveness, authority meet, frozen-denominator navigation with exact rational fixed
points, version spaces and the B2 per-input warrant, quotients / lumpability / measurability, DPO-style
organisation rewrites, exact binomial and multinomial enumeration) are re-implemented inside the
checker; nothing imports `ocm`. NO NOVELTY OR SUPERIORITY CLAIM: every result is a corollary of
KS-T01/T05/T06/T07b/T20/T21/T22/T23, batches 1–3 and the named parents; the contribution is the exact
statement, the executable falsifier and — where the atlas wording could not be proved as written — the
tightened wording, marked **tightened** below.

Notation as in batches 1–3: ⊕ join, ⊗ meet, ⟦ℓ,u⟧ warrant interval, Λ(x) the interval of atom x, R the
revoked set, λ_R ∈ {LIVE, DEAD, UNKNOWN}, Γ a revocation family, Q the registered query family, a*_{Q,R}
the restart fixed point (α = 1/3 throughout), π the uniform-seed background (contract §6), κ a partition.

## D1 · MEG-32 · adopt-not-invent: PARENT_SUFFICIENT / RESIDUAL_SUPPORTED as pre-registered exact tests

**Objects.** A protected paired comparison yields a 2×2 table (n11, n10, n01, n00) with n10 = pairs the
OCM arm wins and n01 = pairs the parent wins. The discordant scale is p_d = P(OCM wins | discordant);
the paired-difference scale is θ = p10 − p01. Pre-registered constants: α = 1/20, margin δ = 1/10 on p_d
(δ_u on θ). Decision rule `decide_discordant(n10, n01)`, a pure function of the table:
RESIDUAL_SUPPORTED iff the exact one-sided binomial test rejects H0: p_d ≤ ½+δ; PARENT_DOMINATES iff
it rejects H0: p_d ≥ ½−δ; PARENT_SUFFICIENT iff both one-sided tests of the TOST pair (H0: p_d ≤ ½−δ
and H0: p_d ≥ ½+δ) reject; otherwise INCONCLUSIVE. Exact McNemar (two-sided binomial on discordants)
and the Clopper–Pearson interval are reported, never used as the decision. On the θ scale,
`decide_unconditional_equivalence` declares PARENT_SUFFICIENT iff exact one-sided tests reject both
H0: p10 ≥ δ_u and H0: p01 ≥ δ_u at α/2 (so |θ| < δ_u at confidence 1−α).

**Theorem.** (i) With the rule fixed before outcome access, P(RESIDUAL_SUPPORTED | p_d ≤ ½+δ) ≤ α,
P(PARENT_DOMINATES | p_d ≥ ½−δ) ≤ α and P(PARENT_SUFFICIENT | |p_d − ½| ≥ δ) ≤ α, for every discordant
count — exhaustively over all outcome tables with n ≤ 10 pairs and a grid of 24 multinomial cell vectors
(24 000 table evaluations, 240 grids), over n_d ≤ 15 × 21 values of p_d (315 checks; worst false
RESIDUAL 729/15 625 = 0.6⁶ at n_d = 6), and over n_d ∈ {76, 100, 150, 200} where TOST can pass (24
checks, worst false PARENT_SUFFICIENT ≤ α and > 0). (ii) The θ-scale rule has size ≤ α/2 exhaustively
for n ≤ 8 (128 grids). (iii) Power, exact: RESIDUAL at n_d = 20 is 0.867 for p_d = 0.9, 0.107 for 0.7;
at n_d = 50 it is 0.028 at the margin itself. PARENT_SUFFICIENT by TOST at δ = 1/10 is **impossible below
n_d = 76** discordant pairs and has power 0.24 at n_d = 100, 0.77 at n_d = 200 when p_d = ½.

**Proof.** (i)–(ii) are the exact size of one-sided binomial tests (the rejection region is chosen by
the null tail ≤ α; monotone likelihood ratio makes the boundary the worst null), averaged over n_d
(conditional size ≤ α ⇒ unconditional ≤ α); TOST's size is the larger of its two one-sided sizes
(Schuirmann 1987, candidate parent — the property is re-derived by enumeration here). (iii) is
enumeration. ∎ **Mutants** `mutant_p_gt_005_equivalent` ("not significantly different ⇒ equivalent":
declares PARENT_SUFFICIENT with probability 0.85 at n_d = 10 when p_d = 0.7, a real residual),
`mutant_stop_when_leading` (optional stopping over ≤ 30 discordant pairs: size 0.127 at the null boundary
against 0.0435 for the fixed rule) and `mutant_posthoc_exclusion` (relabel ≤ 2 OCM losses as annotation
errors: size 0.126 at n_d = 20) caught. **Tightened**: the ME-X3 "0/540 discordant ⇒ PARENT_SUFFICIENT"
terminal is INCONCLUSIVE on the discordant scale (no data) and an *equivalence at margin δ_u ≥ 7/1000* on
the θ scale (the smallest 1/1000-grid margin with (1−δ_u)^540 ≤ α/2); the M7 protocol must pre-register
which scale and which margin it means, and at n = 50 items PARENT_SUFFICIENT can only be a θ-scale
statement. Parent: exact binomial / McNemar 1947 (classic) and TOST (Schuirmann 1987; candidate, unverified) — PARENT_OWNED; nothing
here is a theorem of the OCM, it is the adoption the atlas asked for, made executable.

## D2 · MEG-14 · per-channel acquisition bounds on the registered finite classes (a table with falsifiers)

**Objects.** Registered classes: ALL16 (all Boolean functions of two inputs), AFFINE8, MONOTONE6, and the
L0 six-order class (the six S/V/O permutations; an aligned pair with distinct nouns reveals the order, a
pair whose agent and patient share a lexeme reveals only the verb position). Per channel: INSTRUCTION =
teaching dimension TD (smallest specifying example set, worst case over targets); INTERACTION = exact
minimax membership-query depth MQ, with Hegedüs's extended teaching dimension XTD; DEMONSTRATION from
i.i.d. aligned pairs = exact expected number of pairs to identification (absorbing chain on the inputs
seen) and the n at which P(identified) ≥ 0.9; EXPERIMENTATION = closure in |D| evaluations; the LI-1
envelope ⌈log₂ M⌉ certified bits (T9: the bits telescope to log₂ M at identification).

| class | M | TD | XTD | MQ | E[pairs], uniform | n₀.₉ | closure | ⌈log₂ M⌉ |
|---|---|---|---|---|---|---|---|---|
| ALL16 | 16 | 4 | 4 | 4 | 25/3 | 13 | 4 | 4 |
| AFFINE8 | 8 | 3 | 3 | 3 | 13/3 | 6 | 4 | 3 |
| MONOTONE6 | 6 | 3 | 3 | 3 | 52/9 | 11 | 4 | 3 |
| SIX_ORDERS | 6 | 1 | 1 | 1 | 2 (q = ½) | 4 | 2 | 3 |

Every entry is computed by enumeration; Hegedüs's XTD ≤ MQ ≤ XTD·⌈log₂ M⌉ and MQ ≥ ⌈log₂ M⌉ hold on
the three Boolean classes (checked, parent-owned). For the six-order class E[pairs] = 1/q with q the
probability of a distinct-noun pair, and q = 0 never identifies (the version space stalls at {SVO, OVS}).
**Falsifier** `audit_measured`: a channel reporting identification with fewer lessons than its lower
bound has received information from outside the channel. Measured (`KSO_M3_LEARNING_RESULTS_V1.json`,
class ALL16, target AND): INSTRUCTION 4, DEMONSTRATION 4, INTERACTION 4 queries, EXPERIMENTATION 4
evaluations — each **equal** to its bound; the hostile "3 demonstrations → 2 hypotheses" matches
16/2³. Batch-2 B3's four examples for a⊕b on AFFINE8 are consistent with TD = 3 (one redundant, which is
why B2's `VSW(0) = {e0} ⊕ {e1,e2,e3}` has an alternative). A claimed identification of AND from 2
demonstrations or 3 queries fires BELOW_LOWER_BOUND; an unidentified run never alarms. The six-order
class has no lesson-count receipt in the M3/M5 results: recorded NOT_MEASURED, to be filled by M7 RQ3.
Parent-owned throughout (Goldman–Kearns 1995 teaching dimension — classic, unverified in the parents table;
Hegedüs 1995, verified; Mitchell 1982, verified; Hartley counting, lane-200 Theorem A); no new theorem.

## D3 · MEG-02 (graded half) · statistical operator outputs enter as ⟦0,U⟧ with a score outside the lattice

**Objects.** A statistical/neural operator emits candidates c with interval ⟦0, U⟧ (UNKNOWN) and a score
σ(c) ∈ ℚ that is not a lattice coordinate. A coverage/calibration receipt is an EXPERIMENTATION-channel
claim *about the operator*: "coverage ≥ 1−δ on scope S under exchangeability", warranted by the
calibration evidence, scope S; it is a *scoped bridge warrant* for the set-valued claim "truth ∈ C(x)"
on S, never for a candidate. Split-conformal coverage on a finite exchangeable fixture is computed
exactly by enumerating all (n+1)! orderings.

**Theorem.** (i) No composition whose components are all UNKNOWN is LIVE: exhaustively at n = 3, every
⊗ and ⊕ of two ⟦0,U⟧ intervals under every R (5 776 checks) — the lower profile of a composition of
zero lower profiles is zero (KS-T21). (ii) With n = 5 calibration points and δ = 1/3 the level-(1−δ) set
uses k = ⌈(n+1)(1−δ)⌉ = 4 and covers with exact probability 4/6 ≥ 1−δ; the claim atom is LIVE and dies
when a calibration point is revoked (reopening reaches the coverage claim, never the candidates). The
set-valued claim's warrant is bridge ⊗ membership. (iii) A certificate on S does not transfer to S' ≠ S:
its scope on S' is S ∩ S' = ∅, and on the non-exchangeable S' fixture (the test score always the
maximum) exact coverage is 0. (iv) Certified-only gating: a score change leaves the gated matrix
identical and an UNKNOWN head gated out (syntactic non-dependence, batch-1 T3 shape), so KS-T04b's
exact-share retraction is untouched by scores — scores act on *ranking* only. **Mutants**
`mutant_score_as_warrant` (σ ≥ 0.85 ⇒ LIVE: mints LIVE on the two false high-score candidates c2, c5;
the honest rule leaves them UNKNOWN and the exact-checked c1 LIVE) and `mutant_certificate_transferred`
(coverage on S read as coverage on S': refuted by the exact S' coverage and by the empty scope) caught.
**Tightened**: the atlas's "graded semiring with exact-share retraction" stays OPEN; what is proved is
that the OCM can absorb scored operators *without* a graded semiring by the certified-only gating rule
and scoped bridges. Parent: selective classification (Chow 1970, verified) and split conformal
prediction (Vovk et al.; candidate, unverified) for the coverage identity — PARENT_OWNED.

## D4 · MEG-07 · no-drop guarantee for the surprise functional under fan-out

**Objects.** ρ_Q(v) = a*_Q(v)·[log((a*_Q(v)+ε)/(π(v)+ε))]₊ (contract §6); its exact reading is
ρ_Q(v) > 0 ⇔ a*_Q(v) > 0 ∧ a*_Q(v) > π(v). Backgrounds: π = fixed point of the uniform seed; π' = π − α·u
(the teleport-free / propagated background: restart mass removed, `ocm.kso.surprise` PROPAGATED);
π_S = the average fixed point over all seed sets of cardinality |S| ("matched seed cardinality").

**Theorem.** (i) One-hop lower bound: a*_Q(v) ≥ α(1−α) Σ_s s_Q(s) P_R(s, v), hence for a LIVE one-hop
head v of a seed with in-share ≥ σ under uniform s_Q on S, a*_Q(v) ≥ α(1−α)σ/|S| (1 176 checks on 30
random spaces × 8 revocations, all atoms). (ii) **Matched seed cardinality is a no-op**: π_S = π exactly
for |S| = 1, 2, 3 (41 seed sets; linearity of the fixed point in the seed, the M2.1 lemma). (iii) The
teleport-free background never drops: π' ≤ π pointwise, so ρ' > 0 whenever ρ > 0 and G'_Q ⊇ G_Q (187
checks). (iv) The M2 finding reproduced exactly: on the 20-atom fan-out fixture (one seed r with k = 13
one-hop heads, α = 1/3) a*_Q(c) = α(1−α)/k < π(c) = (α/20)(1 + (1−α)/k) exactly when (1−α)(|V|−1) < k
(12.67 < 13), so all 13 heads are dropped by π and all 13 kept by π' because α(1−α)σ/|S| > π'(c); the
three-seed variant behaves the same. (v) KS-T06 (a_Q = π ⇒ ρ = 0) and the KS-T06b hub witness (specific
atom first by surprise, hub first by popularity; hub-only query hub-first by both) hold under both π
and π'. **Mutants** `mutant_scaled_background` (π/2: every atom becomes surprising under the uniform
seed — KS-T06 broken) and `mutant_matched_cardinality_as_fix` (equals π, the fan-out head stays dropped)
caught. **Tightened**: the atlas's "background π_S at matched seed cardinality" lever is provably inert;
the guarantee is stated for π' (or any background ≤ π), and the M2.1 remaining three misses
(`piece:cN` with two background sources) are outside this theorem — the next lever there is per-source
normalisation, not tried. Parent: personalised PageRank contribution vectors (Andersen–Chung–Lang 2006,
verified), IDF (verified) — PARENT_OWNED for the objects; (iii)–(iv) are the OCM rule with its falsifier.

## D5 · MEG-20 · sufficiency certificate content

**Objects.** `SufficiencyCertificate(m, Q) := (κ, Q, proof that Solve(K, q) = Solve(K̄, q) ∀ q ∈ Q, R ∈ Γ)`
where Solve returns (activation mass of the target's block, liveness of the target) and K̄ is the
quotient by κ. Issued iff (a) κ is warrant-measurable on Γ (every block one liveness under every R) and
(b) for every R ∈ Γ and every q ∈ Q, κ is Kemeny–Snell lumpable on the rows of P_R reachable from q's
live seeds (the seed-reachable subchain), else REFINE_REQUIRED with the failing clause named.

**Theorem.** (i) The restricted check is sufficient: on the 8-atom fixture (seed s → {a1,a2} → {b1,b2}
→ t, plus an unreachable block {u1,u2} whose rows are *not* lumpable) the global check fails, the
restricted certificate is issued, and fine and coarse solves agree on all of Γ × Q (8 agreements).
(ii) A query outside Q (seeded in the unreachable block) is REFINE_REQUIRED, and the forced coarse
answer there is wrong (1/15 ≠ 1/9). (iii) **Tightened**: measurability alone does not give lumpability
under gating — with a hyperedge whose co-tail x has its own evidence, κ is measurable and lumpable at
R = ∅ but not at R = {e_x} (a1's row loses its edge, a2's does not); the certificate must check (b) *per
R ∈ Γ*, which is what refuses it (certified with Γ = {∅}, refused with Γ ∋ {e_x}). **Mutant**
`mutant_certificate_without_measurability` (lumpability only): issued on a fixture where a1 carries its
own evidence, then after revoking it the macro answers LIVE for a member that is DEAD — caught.
No-alarm: with the certificate the summary answers Q (ANSWERED_FROM_SUMMARY), without it
REFINE_REQUIRED, as `abstraction.answer_with_summary` requires. Parent: Kemeny–Snell 1976 (verified) and
KS-T07b (PROVED at M1); this note fixes the *content* of the certificate `proof_ref` must point to.

## D6 · MEG-34 · identifiability of a construction inventory up to lifecycle equivalence ≡_L

**Objects.** Inventories acquired from example sets over the six-order class (batch-2 B2/B3 rules);
behaviour = the agreed answer on each cell of Q or AMBIGUOUS; per-input warrants VSW(i); reopening sets
`reopen(e) = {i : VSW(i) LIVE before, DEAD after revoking e}`. Two inventories are OCM-equivalent (≡_L)
iff they agree on held-out compositional behaviour *and* their per-input warrant structures coincide up
to a renaming of evidence ids (the lifecycle signature), so example revocation reopens the same sets.

**Theorem.** (i) inv1 = {one distinct pair d1} and inv2 = {reflexive r1, distinct d2} both learn SVO
with identical behaviour on Q, but `reopen(d1) = {distinct, reflexive}` while `reopen(d2) = {distinct}`
and `reopen(r1) = ∅`: behaviourally equal, not ≡_L. (ii) Exhaustively over the 14 example sets of size
≤ 3 over the two pair kinds: 2 behaviour classes, 9 lifecycle classes (≡_L strictly refines behaviour),
and 3 STRUCTURAL_NONIDENTIFIABILITY witness classes — distinct example sets with identical (behaviour,
warrant) signature, so the signature, not the example set, is the identifiable object. (iii) All 51
behaviour-equal pairs with different reopening structure are separated by the lifecycle test and all 51
conflated by `mutant_behaviour_only_equivalent` (caught); renamed evidence ids are ≡_L (no alarm).
(iv) Which aligned-pair distributions identify: with q = P(distinct-noun pair), P(identified by n) =
1 − (1−q)ⁿ and E[pairs] = 1/q; q = 0 never identifies (AMBIGUOUS on distinct inputs forever), and for
0 < q < 1 the *lifecycle class* of the learned inventory is sample-dependent (inv1's class with
probability q, inv2's with q(1−q) after two pairs). **Tightened**: identification "up to ≡_L" is a
statement about the behaviour class plus the *reachable* lifecycle classes, not a unique inventory; the
SHRG/CCG (infinite-class) half stays OPEN. Parent: Gold 1967 / Angluin 1988 (classic), version spaces
(Mitchell 1982) — PARENT_OWNED for identification; ≡_L is B2's per-input warrant lifted to signatures.

## D7 · MEG-09 · multiscale navigation coherence on a two-level fixture

**Objects.** Cells κ over atoms; a *registered coarse structure* (a cell edge per pair of cells with ≥ m
crossing fine edges; m = 1 over-approximates fine reachability). `multiscale_solve`: coarse walk with the
four-valued outcome; FOUND → descend with the certificate; GAP → REFINE_REQUIRED and descend;
OBSTRUCTION_WITNESSED only if the ceiling walker fails at the coarse *and* the fine level.

**Theorem.** (i) On the three-cell fixture (A = {a1,a2,a3}, B = {b1,b2}, C = {c1}; Γ with revocations
inside A and inside B; 12 queries) the multiscale answer equals the fine answer, and a coarse GAP maps to
REFINE_REQUIRED never to OBSTRUCTION (e.g. b1 under {ea2}: fine GAP, coarse FOUND, descend). (ii) With a
thresholded coarse graph (m = 2) the coarse ceiling fails for c1 while the fine walker finds it: the
rule descends and answers FOUND; `mutant_coarse_obstruction_is_final` answers OBSTRUCTION — caught, twice
(also on a 12-cell chain where the coarse level is GAP below θ). (iii) Cross-level prune–solve
commutation κ_*(a*_{K,R}) = a*_{q(K),R}, exhaustively over all 52 partitions of a 5-atom space × 4
revocations × 5 singleton seeds: the 2 KS-T07b-admissible partitions commute for every (R, seed) and
**no** non-admissible partition commutes for all of them (0/50) — on this fixture "exactly when" holds in
both directions. **Tightened**: the converse direction is Kemeny–Snell's "for all initial distributions";
for a *restricted* registered Q it is only the sufficient direction that is guaranteed (D5's certificate
is the restricted object), and the fixture's own A/B/C cells are not a lumpable quotient at all (the
coarse walk is a separate registered structure, not the quotient — which is why a certificate is needed
before ascending). Parent: Kemeny–Snell (verified); multilevel PPR / coarsening (candidate, unverified)
— PARENT_OWNED for the walk; the outcome-coherence rule is the OCM's four-valued discipline (KS-T19).

## D8 · MEG-23 · organisation search admissibility

**Objects.** `Org = (fibre partition, exports, transport maps, router policy)` under the constitution
𝔠 = (Check, Authority, Meter, Commit), stored by digest. `Adm(Org)` := 𝔠 untouched ∧ the fibres partition
the atoms ∧ every fibre's rows are KS-T07b-admissible (measurable on Γ, lumpable under every P_R — the
D5 certificate shape) ∧ every export obeys KS-T20/T23 (Λ = Λ_corr ⊗ ⊗Λ(x), authority = A_op ∧ ⋀A(x)
with the operator factor present, batch-1 T1) ∧ every transport obeys KS-T20 (Λ(Tx) = Λ_T ⊗ Λ(x),
authority meet) and points at an existing export ∧ router weights non-negative. Moves: split / merge of
fibres and relink of a transport, as DPO-style rewrites whose interface (exports, transports, 𝔠) is
carried verbatim; `affected(rewrite)` = rewritten fibres ∪ fibres with an edge into a rewritten atom.

**Theorem.** Exhaustively over the fixture's 17 moves (8 splits, 3 merges, 6 relinks): (i) global
Adm(Org') ⇔ interface carried verbatim ∧ every affected fibre re-certifies ∧ exports/transports lawful
(17/17); (ii) locality: every unaffected fibre keeps its certificate unchanged (37 checks); (iii) some
moves of each kind are admissible (2 splits, 1 merge, 6 relinks) and some are refused (6 splits, 2
merges: the split of a 3-cycle fibre is not lumpable; a merge across evidence is not measurable).
**Mutants** — a relink that raises authority through an export (`{world_truth: 2, commit: 1}` on the
transported atom): REFUSED; a rewrite touching 𝔠.Commit: REFUSED:CONSTITUTION_TOUCHED; an export built
by ⊕ over constituents (KS-T23's majority shape): REFUSED; removing the export a transport uses (the DPO
dangling condition): REFUSED. The evaluation object is a Pareto vector: two organisations incomparable
under dominance are ordered by every scalarisation and the order *flips* with the weights (20:1:1 vs
1:1:0), so `mutant_scalar_objective` is not a decision rule; a router re-weighting changes no liveness
signature (batch-1 T3: a J0 feedback move) and a negative weight is refused. **Tightened**: closure of
Adm under split/merge/relink is *local*, not unconditional — the rewritten fibres and their in-neighbours
must re-certify (lumpability is a global row condition), which is exactly what the DPO interface makes
cheap; the atlas's "(ii) no universally best Org" is NFL (Wolpert–Macready 1997, verified) and is not
re-proved. Parent: DPO/adhesive rewriting (Lack–Sobociński 2005, verified), Kemeny–Snell (verified),
multi-objective dominance — PARENT_OWNED; the admissibility predicate is the OCM's M8 contract.

## Consequences for the OCM build (read-only observations; nothing in ORION-OCM was touched)

* M7 §12/§15: the decision rules must name the scale (p_d or θ) and the margin *before* protected
  outcome access. At n = 50 items TOST on p_d at δ = 1/10 cannot declare PARENT_SUFFICIENT (needs
  n_d ≥ 76); the M2 "0/540 discordant" terminal is a θ-scale equivalence at δ_u ≥ 7/1000 and should be
  re-labelled as such. The three hostile mutations of §14 ("stopping when OCM leads", "failed examples
  removed post hoc", "p > 0.05 ⇒ equivalent") each inflate the size above α by a computable factor.
* M7 RQ3 / information accounting: D2's table gives the per-channel lower bounds an
  `INFORMATION_BUDGET_RECEIPT` must be checked against; a channel identifying below its bound is a
  laundering finding, not a sample-efficiency result. The six-order class needs a lesson-count receipt.
* M2 operator backends / M3 ranking / M6 uncertainty: scored operators are admitted as ⟦0,U⟧ candidates
  with the score outside the lattice; coverage receipts are EXPERIMENTATION atoms with scope, and the
  gate reads liveness only (D3). `ocm.kso.surprise` PROPAGATED is D4's π'; the "seed-count-conditioned
  background" listed as the M2.1 lever is a no-op and should be dropped from the design.
* `abstraction.SufficiencyCertificate.proof_ref` has content now: the per-R restricted lumpability ∧
  measurability record of D5; `answer_with_summary` should refuse a certificate whose Γ is narrower than
  the space's registered Γ.
* M8: `RecursiveKSO` topology moves are admissible iff D8's local predicate holds; the router is a J0
  object; the tournament (`RECURSIVE_KSO_ARCHITECTURE_V1.md` §11) reports a Pareto vector.
* Open after this batch: the graded-semiring half of MEG-02, the SHRG/CCG half of MEG-34, the
  open-inventory half of MEG-27, the deconsolidation half of MEG-19, per-source normalisation for the
  M2.1 residual misses (MEG-07 tail), the improvement halves of KS-T12/KS-T14, and MEG-23's NFL
  context-relativity (parent-owned, not a theorem to prove).
