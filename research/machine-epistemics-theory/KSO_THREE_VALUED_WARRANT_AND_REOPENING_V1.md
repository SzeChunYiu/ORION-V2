# Three-valued warrant intervals, reopening locality, and prune–solve equivalence for KnowledgeSpace.v1

Status: **theory note from the ORION-OCM M1 consolidation (SzeChunYiu/ORION-OCM #3). Proved statements with an exact finite checker; NO NOVELTY OR SUPERIORITY CLAIM — every construction names its parent.**
Parent contract: `research/orion-machine/theory/KSO_SUBSTRATE_CONTRACT_V1.md` (frozen at `42b1b0d`; the OCM repository carries the byte-identical copy). This note extends it; it does not edit it.
Executable checker: `kso_three_valued_warrant_exact.py` (this directory; stdlib only; exit 0 / 1 / 2 = holds / fails / `CANNOT_CHECK`).
Canonical implementation: `SzeChunYiu/ORION-OCM` `src/ocm/kso/{warrant,revocation,navigation,abstraction}.py`; obligation ids KS-T21, KS-T22, KS-T04c, KS-T23, KS-T24, KS-T07b in `docs/theorems/KSO_OBLIGATION_REGISTRY_V1.json`.

## 0. Why these statements were needed

The frozen contract defines liveness two-valued (`ℓ_R(P) = 1 ⇔ ∃W ∈ P : W ∩ R = ∅`) and says in prose that when a profile "is not certified complete, absence of a surviving exhibited warrant is `UNKNOWN`, not false" (§3). No algebra was given for `UNKNOWN`, so the reference implementations stayed two-valued and the `complete` flag lived only in `ocm_reference_semantics.py`. Consolidating the core forced the question: what object composes under ⊗ and ⊕ so that `UNKNOWN` is exact rather than a flag? A single completeness bit does not compose (§1.3 below shows the counterexample); an *interval* of profiles does.

The same consolidation exposed two further gaps: the contract proves prune equivalence at the matrix level (KS-T04) but the solve loop consumes the fixed point and the reacting subgraph; and the impact cone (KS-T09) says which objects *may* need reopening but not which *must*, nor what happens to the rest. KS-T04c and KS-T22 close those.

## 1. Warrant intervals and three-valued liveness

Let `𝒜_E` be the antichains over `2^E` with the semiring `(⊕, ⊗, 0, 1)` of KS-T01 and the order

\[
P \le Q \iff f_P \le f_Q \iff \forall W \in P\ \exists W' \in Q:\ W' \subseteq W ,
\]

i.e. `Q` is at least as easy to satisfy as `P`.

**Definition 1.1 (warrant interval).** A warrant interval is a pair `⟦L, U⟧` with `L ≤ U` in `𝒜_E`. `L` (lower) is the antichain of *exhibited* sufficient warrants; `U` (upper) is the antichain of every warrant that *could* suffice. A profile is **certified** when `L = U`; **partial** when `U = 1 = {∅}`; **certified-unwarranted** when `L = U = 0 = ∅`.

**Definition 1.2 (three-valued liveness).** For revoked `R ⊆ E`,

\[
\lambda_R\langle L,U\rangle=
\begin{cases}
\mathrm{LIVE} & \ell_R(L)=1\\
\mathrm{DEAD} & \ell_R(U)=0\\
\mathrm{UNKNOWN} & \text{otherwise.}
\end{cases}
\]

The cases are exclusive and exhaustive because `L ≤ U` gives `ℓ_R(L) = 1 ⇒ ℓ_R(U) = 1`.

**Definition 1.3 (interval operations).** `⟦L,U⟧ ⊗ ⟦L',U'⟧ = ⟦L ⊗ L', U ⊗ U'⟧` and `⟦L,U⟧ ⊕ ⟦L',U'⟧ = ⟦L ⊕ L', U ⊕ U'⟧`. Both are well-defined because ⊗ and ⊕ are monotone in each argument (they are ∧ and ∨ on monotone Boolean functions).

### Theorem KS-T21 (liveness is a Kleene homomorphism)

Let `∧₃, ∨₃` be Kleene's strong three-valued connectives on `{LIVE, UNKNOWN, DEAD}` (LIVE = true, DEAD = false). For all intervals `P, Q` and all `R`:

\[
\lambda_R(P\otimes Q)=\lambda_R(P)\wedge_3\lambda_R(Q),\qquad
\lambda_R(P\oplus Q)=\lambda_R(P)\vee_3\lambda_R(Q).
\]

Moreover (a) *reduction*: on certified intervals `λ_R` never returns `UNKNOWN` and agrees with `ℓ_R`; (b) *refinement monotonicity*: if `Q` refines `P` (`L_P ≤ L_Q` and `U_Q ≤ U_P`) then `λ_R(Q) = λ_R(P)` whenever `λ_R(P) ≠ UNKNOWN`.

*Proof.* `ℓ_R(L ⊗ L') = ℓ_R(L) ∧ ℓ_R(L')`: a union `W ∪ W'` avoids `R` iff both parts do; and `ℓ_R(U ⊗ U') = 0 ⇔ ℓ_R(U) = 0 ∨ ℓ_R(U') = 0` by the same fact negated. Hence `LIVE(P⊗Q) ⇔ LIVE(P) ∧ LIVE(Q)` and `DEAD(P⊗Q) ⇔ DEAD(P) ∨ DEAD(Q)`, which is exactly the truth table of `∧₃`. For ⊕, `ℓ_R(L ⊕ L') = ℓ_R(L) ∨ ℓ_R(L')` and `ℓ_R(U ⊕ U') = 0 ⇔ ℓ_R(U) = 0 ∧ ℓ_R(U') = 0`, the table of `∨₃`. (a) With `L = U` the second case of Definition 1.2 is the negation of the first. (b) `L_P ≤ L_Q` gives `ℓ_R(L_P) ≤ ℓ_R(L_Q)` so LIVE is preserved; `U_Q ≤ U_P` gives `ℓ_R(U_Q) ≤ ℓ_R(U_P)` so DEAD is preserved. ∎

### 1.3 Why a completeness bit does not compose

Take `P = ⟨(), complete=False⟩` (nothing exhibited, not certified) and `Q = ⟨{{2}}, complete=True⟩` with `R = {2}`. `Q` is DEAD, so `P ⊗ Q` must be DEAD by `∧₃`. But the composite profile is `()` and the natural rule `complete(P⊗Q) = complete(P) ∧ complete(Q)` marks it incomplete — hence UNKNOWN. The bit cannot remember *which* factor was certified dead. The interval does: `U_{P⊗Q} = 1 ⊗ {{2}} = {{2}}`, which `R` kills.

**Parents.** Kleene (1938) strong three-valued logic; Belnap (1977) four-valued bilattices (the interval order is the "knowledge" order restricted to consistent pairs); Pawlak (1982) rough sets — `L`/`U` are lower/upper approximations of the true warrant antichain; ATMS labels (de Kleer 1986) for `L`. Nothing in §1 is new mathematics; the contribution is fixing *which* parent object the OCM warrant is, so that `UNKNOWN` composes exactly.

**Consequences used by the OCM.** FEEDBACK-admitted atoms carry `⟦0,0⟧` and are DEAD under every `R` (KS-T18 becomes a corollary). A summary atom's interval is `⟦L_c,U_c⟧ ⊗ ⨂_{x∈exported} ⟦L_x,U_x⟧`; by KS-T21 it is LIVE only if every exported part is LIVE and DEAD as soon as one is — *no authority from abstraction* (OCM KS-T23) is then a one-line corollary, and the "majority" aggregation is exhibited as the mutant.

## 2. Prune–solve equivalence beyond the matrix (KS-T04c)

Notation as in the contract §5–§7: `P_{Q,R}` the gated navigation matrix with frozen denominators `D_Q`, `s_{Q,R} = g_R ⊙ s_Q` the gated seed, `a^*_{Q,R}` the unique fixed point of `F(a) = α s_{Q,R} + (1−α) P_{Q,R}^{\mathsf T} a` (KS-T05), `G_Q` the reacting subgraph (KS-T11a).

**Definition 2.1 (prune with retained shares).** `Prune_R(𝒦)` removes every atom that is not LIVE under `R` and every hyperedge that is not LIVE or has a non-LIVE tail; a hyperedge with a non-LIVE *head* survives with that head deleted, **its share of `γ_h` retained by the surviving heads unchanged** (the dead head's share dissipates). Structural denominators `D_Q` are those of `𝒦`, not recomputed.

The last clause is the part the frozen contract left implicit: the reference's "independent prune" implementation (`navigation_matrix_independent_prune`) skips dead heads without renormalising `γ_h`, and a prune that renormalises the surviving heads' shares is the KS-T04 defect at head level. The OCM checker plants exactly that mutant (`mutant_prune_renormalize_heads`) and found the omission on a random space before the clause was written down.

### Theorem KS-T04c

With `Prune_R` as in 2.1, and `s'` the restriction of `s_Q` to the surviving atoms:

1. (matrix) `P_{Q,R}(𝒦)` restricted to surviving atoms equals `P_{Q,∅}(Prune_R(𝒦))` computed with `𝒦`'s denominators and shares, and every row/column of a removed atom is zero;
2. (fixed point) `a^*_{Q,R}(𝒦)` restricted to survivors equals the fixed point of the pruned system, and is zero on removed atoms;
3. (extraction) the reacting subgraph `G_Q` computed on `𝒦` under `R` equals the one computed on `Prune_R(𝒦)` under `∅` (same background).

*Proof.* (1) Every live incidence `(v, h, u)` contributes the same term `w_h β_{r_h}(Q) γ_h(u) / D_Q(v)` on both sides because denominators and shares are copied, not recomputed; every dead incidence contributes zero on the gated side and is absent on the pruned side. (2) `F_{Q,R}` is a contraction with a unique fixed point (KS-T05). The vector that is the pruned fixed point on survivors and zero elsewhere satisfies the gated equation: for a removed atom `v`, `s_{Q,R}(v) = 0` and column `v` of `P_{Q,R}` is zero, so the equation reads `a(v) = 0`; for a survivor the equation is term-wise the pruned one by (1). Uniqueness gives equality. (3) `G_Q` is a function of `(a^*, background, gated closure of the seed support, live hyperedges inside)` (KS-T11a); by (2) `a^*` agrees on survivors and vanishes elsewhere, the gated closure on `𝒦` under `R` equals the ungated closure on the pruned space (both traverse only live edges with all tails live), and the live hyperedges inside coincide. ∎

Parents: KS-T04 (contract), Banach uniqueness. Not new; it is the statement the solve loop actually needs.

## 3. Reopening locality (KS-T22)

Let `Δ = (R_0 → R_1)` be a revocation delta, `C(Δ) = {v : λ_{R_0}(v) ≠ λ_{R_1}(v)}` the atoms whose three-valued liveness changed (plus the heads of hyperedges whose liveness changed), `Impact_D(·)` the least dependency-closed superset of KS-T09, and `Reach(D_R)` the ungated forward closure of the non-LIVE set (contract §25).

**Definition 3.1 (reopening report).**

\[
\mathrm{REOPEN}=\mathrm{Impact}_D(C)\cap C,\qquad
\mathrm{RECHECK}=\mathrm{Impact}_D(C)\setminus C,\qquad
\mathrm{UNAFFECTED}=V\setminus\mathrm{Impact}_D(C).
\]

### Theorem KS-T22

1. (exactness) Every atom whose liveness changed is in REOPEN; every atom in RECHECK is a dependent of a changed atom whose own liveness did **not** change — it keeps a live alternative warrant and needs re-evaluation of derived content only, never forced revocation;
2. (no-alarm) no atom in UNAFFECTED changes liveness, and no atom outside `Reach(D_{R_1}) ∪ Reach(D_{R_0})` changes activation;
3. (least) `Impact_D(C)` is contained in every dependency-closed set containing `C`; in particular an irrelevant revocation (`C = ∅`) yields `REOPEN = RECHECK = ∅` and an unchanged fixed point;
4. (cycles) dependency cycles need no special case — `Impact_D` is a least fixed point of a monotone operator on the finite lattice `2^V`.

*Proof.* (1) By definition of `C` and of the intersection; RECHECK members are in the cone by a dependency chain from `C` but not in `C`, so their intervals were not moved by `Δ`. (2) First half: liveness is a function of the atom's own interval and `R`, so it changes only on `C ⊆ Impact_D(C)`. Second half is KS-T04b (ii) applied at `R_0` and `R_1`: walks from the seed to an atom outside both reaches avoid every non-live atom under either revocation, and their factors are identical because denominators are frozen. (3), (4) are KS-T09. ∎

Parents: dependency-directed backtracking (Doyle 1979), ATMS label propagation (de Kleer 1986), incremental/self-adjusting computation (Acar 2005). The distinction REOPEN vs RECHECK is what ATMS labels give for free once the label is an antichain: an atom with an alternative environment does not lose its label. What is stated here is only the OCM-level consequence — which objects the runtime is *obliged* to revisit.

## 4. Two admissibility statements consolidated

**KS-T07b (representation move).** A quotient `κ : V → \bar V` is admissible for navigation *and* warrant only if it is Kemeny–Snell lumpable for `P_{Q,∅}` **and** warrant-measurable: for every registered revocation `R ∈ Γ`, all atoms in a block share the same `λ_R`. Either condition alone is refused with its own verdict (`NOT_LUMPABLE`, `NOT_WARRANT_MEASURABLE`, `NEITHER`). Parent: Kemeny & Snell (1976) for the first conjunct; the contract's S4 for the second. Nothing new; the conjunction is the contract's §9.2 made a checkable verdict.

**KS-T24 (navigation is not truth).** Replacing every interval by `⟦0,0⟧` while keeping every weight leaves the exploratory (ungated) fixed point unchanged and makes the warranted fixed point, the warranted reacting subgraph and the set of enabled hyperedges all empty. Proof: every gate is a function of `λ_R` alone. This is the D4 hostile of the M1 issue as a theorem.

## 5. Calibration performed (exact, stdlib)

| statement | finite check | denominators |
|---|---|---|
| KS-T21 | every valid interval over `E = {0,1,2}` × every `R ⊆ E` | 168 intervals; 168² × 8 = 225,792 homomorphism checks (⊗ and ⊕ each); 160 reduction checks; 27,920 refinement checks |
| §1.3 counterexample | the bit-based composite reads UNKNOWN where `∧₃` says DEAD | 1/1 |
| KS-T04c | retraction witness `s→a→{b,z}→c→d` under `R ∈ {∅,{0}}` and seeded random typed hypergraphs with partial intervals under every `R ⊆ {0,1,2}` | matrix, fixed point and reacting subgraph equal in every case; head-renormalising mutant differs on a two-head witness |
| KS-T22 | eight-atom witness: direct, deep chain, shared dependency, alternative live path, cycle, irrelevant revocation | REOPEN = {a}, RECHECK = {b,c,d,e}, UNAFFECTED = {x,y,z}; no-op on irrelevant evidence; one-hop mutant misses the deep dependent |
| KS-T24 | retraction witness with all intervals zeroed | warranted activation 0 on 6/6 atoms; exploratory unchanged; enabled set empty |

The checker in this directory reproduces the KS-T21 table, the §1.3 counterexample, the KS-T22 witness and the KS-T04c head-share witness without importing the OCM package (it re-implements the ~120 lines of exact arithmetic it needs). Finite enumeration calibrates the implementation; the all-size claims rest on the proofs above.

## 6. Non-claims

No statement here is a novelty claim. The interval object is Pawlak/Belnap; the connectives are Kleene's; the reopening set is what an ATMS label update already implies; prune–solve is a corollary of the frozen KS-T04/T05. The value is that the OCM's `UNKNOWN`, its reopening obligation and its solve-level pruning are now *exact objects with checkers* instead of prose. Parent subtraction rows for these constructions are carried in ORION-OCM `docs/parent-subtraction/KSO_CORE_PARENTS_V1.md`.

```text
KS-T21   PROVED  (exhaustive n=3 calibration)
KS-T04c  PROVED  (witness + random calibration)
KS-T22   PROVED  (witness calibration)
KS-T23   PROVED  (corollary of KS-T21)
KS-T24   PROVED
KS-T07b  PROVED  (conjunction of parent theorem and S4)
NOVELTY  NOT_ESTABLISHED
```
