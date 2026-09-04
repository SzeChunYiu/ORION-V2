# KSO one-day theorems, batch 1 — eleven atlas gaps closed on the canonical core objects

Status: **theory note for the ORION machine-epistemics programme. Proved statements with an exact finite checker; NO NOVELTY OR SUPERIORITY CLAIM — every construction names its parent with the verification status recorded in the atlas.**
Source of the obligations: `ME_THEORY_GAP_ATLAS_V1.md` §B, "next tier (≤ 1 day each)": MEG-04, 06, 08, 18, 22, 26, 29, 30, 31, 35, 01. This note adds no obligation ids of its own; each theorem is filed under its atlas id.
Objects: exactly those of the OCM canonical core (`ORION-OCM` `src/ocm/kso/{warrant,types,space,navigation,revocation,admission,abstraction,jump,resources}.py`) and of `KSO_THREE_VALUED_WARRANT_AND_REOPENING_V1.md` (KS-T21, KS-T22, KS-T04c, KS-T24). Checker: `kso_one_day_theorems_batch1_exact.py` (stdlib only, exact rationals; exit 0 / 1 / 2 = holds / fails / `CANNOT_CHECK`); tests: `tests/unit/test_kso_one_day_theorems_batch1.py`.

## 0. Shared definitions (nothing new)

`E` is the evidence universe; `𝒜_E` the antichains of finite subsets of `E` with `P ⊕ Q = Min(P ∪ Q)`, `P ⊗ Q = Min{a ∪ b}`, `0 = ()`, `1 = {∅}`, and the order `P ≤ Q ⇔ f_P ≤ f_Q ⇔` every warrant of `P` contains a warrant of `Q` (KS-T01; provenance semirings, Green et al. 2007, verified). A warrant interval is `⟦L,U⟧` with `L ≤ U`; certified when `L = U`, partial when `U = 1`. For `R ⊆ E`, `ℓ_R(P) = 1 ⇔ ∃W ∈ P: W ∩ R = ∅` and

\[
\lambda_R\llbracket L,U\rrbracket=\mathrm{LIVE}\ (\ell_R(L)=1),\quad \mathrm{DEAD}\ (\ell_R(U)=0),\quad \mathrm{UNKNOWN}\ \text{otherwise};\qquad
\lambda_R(P\otimes Q)=\lambda_R(P)\wedge_3\lambda_R(Q),\ \ \lambda_R(P\oplus Q)=\lambda_R(P)\vee_3\lambda_R(Q)\ \ \text{(KS-T21)}.
\]

KS-T02 (enabling): a hyperedge `h` is ENABLED under `R` iff `λ_R(Λ_h) = LIVE` and every tail is LIVE. KS-T20 (composition): `Λ = Λ_b ⊗ ⨂ Λ_i`, `A = A_b ∧ ⋀ A_i`, `S = S_b ∩ ⋂ S_i`. `Authority` is the product lattice of named non-negative integer ranks with a missing coordinate read as `0` and `∧` = coordinate-wise `min` (`types.Authority`). Navigation (contract §5, `navigation.py`): structural denominators `D_Q(v) = Σ_{h: v∈T_h} w_h β_{r_h}(Q)` are computed on the registered structure and never renormalised; the gated matrix `P_{Q,R}` has entries `Σ_h w_h β_{r_h} γ_h(u) g_R(v) g_R(h) g_R(u) ∏_{z∈T_h} g_R(z) / D_Q(v)` with `g_R = [λ_R = LIVE]`; it is row-substochastic. The restart operator is `F(a) = α s + (1−α) P^{\top} a`, an `ℓ_1` contraction with unique fixed point `a^*` (KS-T05, Banach). `Impact_D(X)` is the least dependency-closed superset of `X` (KS-T09); the reopening report is KS-T22. A refinement of `⟦L,U⟧` is any `⟦L',U'⟧` with `L ≤ L'` and `U' ≤ U`; KS-T21(c): a refinement can move UNKNOWN to LIVE or DEAD, never LIVE to DEAD or back.

Every theorem below is stated with: statement · proof · parent (verification status as in the atlas) · checker function · planted mutant · limitation.

## T1 · MEG-04 · commit authority is a bottom for internal composition

**Definition.** The authority coordinate set contains at least `{world_truth, speaker, task_contract, commit}`. An *internal operator* (compose, summarize, any acquisition channel other than an external `ActionReceipt`) carries its own authority `A_op` in which `commit` is undeclared, hence `rank_{commit}(A_op) = 0` (S5: undeclared = bottom). The composition law always includes the operator as a factor: `A = A_op ∧ ⋀_i A_i`.

**Theorem T1.** (i) For all authorities, `rank_c(A ∧ B) = min(rank_c A, rank_c B) ≤ rank_c A` for every coordinate `c`; `∧` is the greatest lower bound of the product order, so composition never raises any coordinate. (ii) Every atom produced by an internal operator has `rank_{commit} = 0`, whatever the tails' authorities. (iii) By induction on derivation length, no chain of internal operations of any length produces an atom with `rank_{commit} > 0`; the only atoms with positive commit rank are those whose authority was set directly by an external `ActionReceipt`.

*Proof.* (i) is the definition of the product order and of coordinate-wise `min`: `m = A ∧ B` satisfies `m ≤ A`, `m ≤ B`, and any `C ≤ A, C ≤ B` has `rank_c C ≤ min = rank_c m`. (ii) `rank_{commit}(A_op ∧ ⋀ A_i) = min(0, …) = 0`. (iii) Base: a receipt-free atom is created by an internal operator, so (ii) applies; step: an internal operator over atoms each satisfying the claim or being a receipt yields `commit = 0` by (ii) regardless of the tails. ∎

Parent: Biba low-water-mark (verified), Denning 1976 (verified); parents table row C(b). Checker: `check_t1_meg04_commit_bottom` (exhaustive glb over `{0,1,2}^4` pairs, 6,561 pairs; receipt tails with `commit = 1` composed internally give `0`; `world_truth` is kept — no-alarm). Mutants: `mutant_authority_max` (max instead of min → `commit = 1`, caught) and `mutant_compose_drops_operator_factor` (meet over tails only → `commit = 1`, caught). Limitation: the theorem needs the operator factor to be *present*; `admission.compose` in the m2-runtime takes the meet over the tails only when `bridge_authority` is `None` (`authorities = [tails] + ([bridge] if bridge is not None else [])`), which is exactly the second mutant's shape — two receipt-authorised tails then compose to `commit = 1`. That is a runtime defect relative to MEG-04, not a theory gap; the fix is to default the bridge authority to the operator's authority (commit undeclared) rather than omitting it.

## T2 · MEG-06 · budget bracket for the restart iteration

**Theorem T2.** Let `P` be row-substochastic and non-negative, `s ≥ 0` with `‖s‖_1 ≤ 1`, `α ∈ (0,1]`, `a_0 = α s`, `a_{k+1} = F(a_k)`. Then

\[
a_k=\alpha\sum_{j=0}^{k}(1-\alpha)^j (P^{\top})^j s,\qquad a_k\le a_{k+1}\le a^*\ \text{entry-wise},\qquad a^*(t)-a_k(t)\le \|a^*-a_k\|_1\le(1-\alpha)^{k+1}\|s\|_1 .
\]

Consequences. (a) FOUND at budget `k` (`a_k(t) ≥ θ`) is sound for the fixed point: `a^*(t) ≥ a_k(t) ≥ θ`. (b) `BUDGET_EXHAUSTED` carries the bracket `a^*(t) ∈ [a_k(t), a_k(t) + w_k]`, `w_k = (1−α)^{k+1}‖s‖_1`; the verdict `a^*(t) ≥ θ` is decided iff `θ ∉ (a_k(t), a_k(t)+w_k]`. (c) `MORE_BUDGET` hook: if `a_k(t) < θ` let `k'` be the least index with `w_{k'} < θ − a_k(t)`; then no budget in `[k, k')` decides (for such `k''`: `a_{k''} + w_{k''} ≥ a_k + w_{k''} ≥ θ`), so `k'` is the least budget that *can* decide. (d) Float solver: if one float step computes `F̂(x)` with `‖F̂(x) − F(x)‖_1 ≤ δ`, then `‖â_k − a_k‖_1 ≤ δ Σ_{j<k}(1−α)^j ≤ δ/α`, hence `‖â_k − a^*‖_1 ≤ (1−α)^{k+1}‖s‖_1 + δ/α`.

*Proof.* Induction: `a_{k+1} = αs + (1−α)P^{\top} a_k` and the partial-sum form give the identity; all terms are non-negative (`P ≥ 0`, `s ≥ 0`) so the partial sums are monotone and bounded by the full Neumann series `a^* = α Σ_j (1−α)^j (P^{\top})^j s`, which converges because `‖(1−α)P^{\top} x‖_1 ≤ (1−α)‖x‖_1` for `x ≥ 0` (column sums of `P^{\top}` are row sums of `P`, `≤ 1`) and solves `a = F(a)`, the unique fixed point (KS-T05). The tail is `α Σ_{j>k}(1−α)^j ‖(P^{\top})^j s‖_1 ≤ α ‖s‖_1 (1−α)^{k+1}/α`. (a)–(c) are read off the bracket; (d) is the standard error recursion `e_{k+1} ≤ (1−α)e_k + δ`. ∎

Parent: Banach/Neumann (verified). Checker: `check_t2_meg06_budget_bracket` (retraction witness `s→a→{b,z}→c→d`, `α = 1/3`, `k ≤ 9`: partial-sum identity, monotonicity, entry-wise bracket; 40 bracket decisions; `k' = 6` for the hook; float `ℓ_1` error `9.7·10^{−17}` against the bound `1.6·10^{−14}` with `δ = 4nu`). Mutant: `mutant_unnormalised_iterate` — iterating from `a_0 = s` instead of `α s` gives `a_k = S_k + (1−α)^{k+1}(P^{\top})^k s`, which *overshoots* `a^*` (witnessed on the retraction space) and on the 18-atom chain reports FOUND at `θ = 10^{−3}` with `(2/3)^{17} ≥ θ` while `a^*(17) = (1/3)(2/3)^{17} < θ` — an unsound FOUND. Limitation: `navigation.navigate` in the m2-runtime initialises `a = list(s)` and iterates `F`, i.e. the mutant's start vector; its FOUND is therefore not sound for the fixed point (bracket and hook need `a_0 = α s`). `θ = a^*(t)` exactly is never decided by bracketing (use the exact solve).

## T3 · MEG-08 · feedback updates behaviour, never warrant

**Theorem T3.** Let `θ = (w_h, β_r(Q), γ_h, π)` be the navigation parameters (edge weights, relevance, head shares, routing). For every atom `v`, the liveness signature `σ(v) = (λ_R(Λ_v))_{R∈Γ}`, the live/dead/unknown partition of `V` under each `R`, and the enabled set `En_R` (KS-T02) are functions of `(Λ, Γ)` alone. Hence any FEEDBACK-channel event that changes `θ` and nothing else leaves every liveness signature and every enabled set unchanged, while the matrix `P_{Q,R}` and the fixed point may change. A FEEDBACK-admitted atom carries `⟦0,0⟧` and is DEAD under every `R` (KS-T18), so it never enables anything either.

*Proof.* `λ_R` takes `(L,U,R)` as its only arguments; `En_R` takes `λ_R` values of the edge and its tails. Neither definition mentions `θ`, so the identity of the outputs under `θ ↦ θ'` is a syntactic non-dependence (KS-T24 stated the gate as a function of `λ_R` alone; KS-S1/S5 forbid a FEEDBACK event from editing `Λ`). ∎

Parent: TMS premise/assumption distinction (verified); ACT-R base-level learning as the weight-learning parent (Anderson 1993, verified in the F7 rows). Checker: `check_t3_meg08_feedback_not_warrant` (30 seeded random spaces over `|E| = 3`, all 8 revocations: identical partitions and enabled sets after random re-weighting of `w_h`, `γ_h`, `β_r`; the matrix changed in 30/30 — the perturbation was applied). Mutant: `mutant_feedback_edits_label` (a feedback event that sets an atom's lower profile to `1` changes a liveness signature; caught 30/30). Limitation: the theorem is definitional and says nothing about *which* weight updates are good; negative-transfer counterexample atoms are OBSERVATION-warranted atoms that motivate a J0 weight change — the change itself stays a `θ` move.

## T4 · MEG-18 · Jump rollback is revoke-plus-quarantine

**Definition.** An *additive Jump* with certificate `e_J ∉ E(𝒦)` produces `𝒦' = 𝒦 + (V_J, H_J)` where every new atom/edge `x` carries `Λ'_x = ⟦{{e_J}}⟧ ⊗ Λ^0_x` (so `e_J` lies in every warrant of `L'_x` and of `U'_x`) and every old object is unchanged. A Jump creates only warrant-labelled structure: `U^0_x ≠ 0` for every created object, so `e_J ∈ ev(Λ'_x)`. `rollback(e_J)` := revoke `e_J` and *quarantine* (remove from the navigable structure, keep in the append-only history, K1) every object whose evidence contains `e_J`.

**Theorem T4.** (i) Every Jump-created object is DEAD under any `R ∋ e_J`; every pre-Jump object has `λ_R` unchanged for every `R` (S5). (ii) The quarantine set of `rollback(e_J)` is exactly `(V_J, H_J)`, and the navigable space after rollback equals `𝒦` as a value — same atoms, edges, denominators — so every fixed point and every liveness signature is restored exactly. (iii) Revocation alone is *not* rollback: with `R = {e_J}` on `𝒦'` the frozen denominators `D'_Q(v) = D_Q(v) + Σ_{h∈H_J, v∈T_h} w_h β` keep the Jump's mass, which dissipates (KS-T04), so `a^*_{Q,{e_J}}(𝒦') ≠ a^*_{Q,∅}(𝒦)` whenever some Jump edge has a pre-Jump tail. (iv) A Jump that *removes* structure is invertible only from the quarantine record: deletion loses the removed values, so the structure must be quarantined, not deleted.

*Proof.* (i) every `W ∈ U'_x` contains `e_J`, so `ℓ_R(U'_x) = 0`; old objects' evidence does not contain `e_J`. (ii) `e_J` is fresh, so it lies in the evidence of an object iff the object was stamped, i.e. iff it is Jump-created (with `U^0_x ≠ 0` the stamp is visible in `U'_x`); removing exactly `(V_J, H_J)` restores `𝒦`, and the denominators are recomputed from `𝒦`'s registered structure. (iii) the gated matrix on `𝒦'` under `{e_J}` has the pre-Jump incidences divided by `D'_Q ≥ D_Q`, strictly larger on any tail of a Jump edge, so its rows are strictly smaller there; by KS-T04c the fixed point differs. (iv) is the statement that a function deleting a value is not injective. ∎

Parent: ATMS context switching (verified). Checker: `check_t4_meg18_jump_rollback` (retraction witness plus Jump atom `m` with edges `a→m→d`; 24 old signatures preserved over `Γ = 2^{\{0,e_J\}}`; revocation alone lowers `z` and `d` — the dissipation witness of (iii); rollback restores matrix and fixed point exactly; unrelated `b` unchanged). Mutant: `mutant_uncertified_structure` (the Jump atom admitted without `e_J` in its warrant stays LIVE after revoking `e_J` and is not quarantined; caught). Limitation: (ii) is for additive Jumps; a Jump that rewrites existing objects (a DPO rule with `L ≠ I`) is MEG-28's preservation half and is not covered here. Nothing here rests on `KS-T04b(iv)` (reinstatement); the atlas's citation of it applies to the revocation half only.

## T5 · MEG-22 · shared evidence across fibres and transfer maps

**Definition.** Fibres `P, M ⊆ V` with evidence supports `W_P = ⋃_{v∈P} ev(Λ_v)`, `W_M` likewise, shared set `Σ = W_P ∩ W_M`, `Sh = {v : ev(Λ_v) ∩ Σ ≠ ∅}`. A `TransferMap T` is an atom with `(Λ_T, A_T, S_T)`; `Tx` is the composite with `Λ(Tx) = Λ_T ⊗ Λ_x`, `A(Tx) = A_T ∧ A_x`, `S(Tx) = S_T ∩ S_x`.

**Theorem T5.** (i) For any revocation delta `Δ = (R_0 → R_1)` with `R_1 △ R_0 ⊆ Σ`, the atoms whose liveness changes satisfy `C(Δ) ⊆ Sh`, so the reopening obligation `Impact_D(C(Δ))` (KS-T22) is contained in `Impact_D(Sh)`; atoms outside `Impact_D(Sh)` are UNAFFECTED in both fibres. (ii) If `R_1 △ R_0 ⊆ W_P \ W_M` then no `M`-atom changes liveness (non-interference for disjoint supports is the case `Σ = ∅`). (iii) `λ_R(Tx) = λ_R(T) ∧_3 λ_R(x)` and `ev(Tx) = ev(T) ∪ ev(x)`, so `Tx ∈ Sh` iff `T` or `x` cites shared evidence; a transfer never mints warrant, authority or scope beyond its map.

*Proof.* (i) `λ_{R_0}(v) ≠ λ_{R_1}(v)` requires a warrant of `Λ_v` to meet `R_1 △ R_0`, hence `ev(Λ_v) ∩ Σ ≠ ∅`; monotonicity of `Impact_D`. (ii) same argument with `W_M ∩ (R_1 △ R_0) = ∅`. (iii) KS-T21 for `⊗`; the evidence of a `⊗` is the union. ∎

Parent: ATMS composition (verified); KS-T09/T22 (PROVED). Checker: `check_t5_meg22_shared_evidence` (shared lemma `L` cited by proof atoms `p1 ∈ P`, `p2 ∈ M` with consequences `c1, c2`; revoke `L`: exact reopening set `{L, p1, p2, c1, c2}` equals the bound `Impact_D(Sh)`, unrelated `u1, u2` stay; revoking `P`-private evidence touches nothing in `M`; 8 Kleene checks for the transfer). Mutants: `mutant_transfer_drop_bridge` (`Λ(Tx) = Λ_x`: the transferred atom survives revoking the map; caught) and whole-fibre over-alarm (`u2` predicted to interfere though its liveness is unchanged; caught). Limitation: (i) is an upper bound; the exact set is KS-T22's report, which the checker confirms coincides on the fixture but need not in general (a shared-evidence atom with an alternative warrant stays RECHECK, not REOPEN).

## T6 · MEG-26 · candidate warrant, ambiguity set, evidence-driven collapse

**Definition.** An interpretation candidate `c` has `Λ(c) = Λ(construction) ⊗ ⨂_i Λ(lexeme_i) ⊗ Λ(morph)`. An ambiguity set `𝒜 = {c_1,…,c_m}` is a set of candidate atoms, each with its own interval — never a `⊕`-merged atom. `select(𝒜, R)` = SELECTED `c_i` iff exactly one candidate is LIVE and none is UNKNOWN; NO_CANDIDATE iff all are DEAD; AMBIGUOUS otherwise. A downstream operator with a candidate tail fires only on SELECTED (KS-T02 with AMBIGUOUS as the UNKNOWN case). A score `σ(c) ∈ ℝ` is a coordinate outside the lattice.

**Theorem T6.** (i) `λ_R(c) = ∧_3` of its parts (KS-T21), so a DEAD part kills the candidate and an UNKNOWN part leaves it at most UNKNOWN. (ii) The `⊕`-merged atom `⊕_i Λ(c_i)` is LIVE whenever any candidate is LIVE; firing on it fires under ambiguity — the merged reading is the false-collapse defect. (iii) Under `select`, a firing under `R` names a unique LIVE candidate and the fired derivation has warrant `Λ(c_i) ⊗ Λ_{op}` (KS-T20). (iv) Collapse is an evidence event: adding context or a clarification answer is a revocation (kills every candidate citing the revoked lexeme) or a refinement (KS-T21(c): never flips a LIVE candidate to DEAD or promotes a DEAD one); `σ` is not an argument of `λ_R` or `select`, so no score changes a verdict.

*Proof.* (i)–(ii) KS-T21 applied to `⊗` and `⊕`. (iii) definition of `select` plus KS-T20. (iv) revocation and refinement are the only operations on intervals; the non-dependence on `σ` is syntactic, as in T3. ∎

Parent: KS-T20/T21 (PROVED). Checker: `check_t6_meg26_candidate_warrant` ("bank" fixture with shared construction and morphology parts, 32 Kleene checks; AMBIGUOUS blocks firing; revoking the river-lexeme evidence selects the finance reading; revoking the shared morphology kills both; the merged atom is LIVE under ambiguity). Mutant: `mutant_forced_collapse_by_score` (fires the top-scored candidate while `select` says AMBIGUOUS; caught). No-alarm: a candidate with an UNKNOWN part is never SELECTED. Limitation: the false-collapse *rate* of a ranking model (M3) is an empirical quantity outside this theorem.

## T7 · MEG-29 · no self-authority

**Definition.** A *reflexive* atom is one whose content references the constitution `𝔠` or the machine's own correctness (a registered predicate on content). Each evidence id `e` carries the authority `A_e` of the certificate that produced it; the evidence-conferred authority of an atom is `A_{ev}(x) = ⋁_{W∈L_x} ⋀_{e∈W} A_e` (the best exhibited warrant). Admission rule for reflexive atoms: `rank_{commit} = 0` and `rank_{world\_truth}(A_x) ≤ rank_{world\_truth}(A_{ev}(x))`.

**Theorem T7.** (i) Every reflexive atom and every internal composition containing one has `commit = 0` (T1) and `world_truth` bounded by its OBSERVATION evidence (the rule plus T1(i): meets never raise). (ii) A calibration claim `κ` about a self-model `M` whose warrant depends on `M`'s evidence, `Λ_κ = Λ^0_κ ⊗ Λ_M` (MEG-01: `κ` cites derived evidence with provenance `Λ_M`), satisfies `λ_R(M) = DEAD ⇒ λ_R(κ) = DEAD` for every `R`; hence `κ` cannot survive the revocation it would have to detect and certifies nothing about `M` beyond `M`'s own liveness. A certificate of `M` must have `ev(Λ_κ) ∩ ev(Λ_M) = ∅` (held-out OBSERVATION evidence), and then a `DEAD` `M` with a LIVE `κ` is possible. Consequence: the Gödel-machine utility proof is an EXACT_CHECKER certificate produced outside `K_self`, never by `K_self`.

*Proof.* (i) T1 and the admission rule; the bound is preserved under `∧` because `∧` is coordinate-wise `min`. (ii) KS-T21: `λ_R(Λ^0_κ ⊗ Λ_M) = λ_R(Λ^0_κ) ∧_3 λ_R(Λ_M)` and DEAD is absorbing for `∧_3`. Independence of evidence makes the two liveness values vary independently under `R`. ∎

Parent: Gödel machine (Schmidhuber, verified in the parents table), reference monitor (Saltzer–Schroeder 1975, verified). Löb-obstacle literature is listed as candidate/unverified in the atlas and is not cited. Checker: `check_t7_meg29_no_self_authority` (reflexive atom with observation evidence of `world_truth = 1` admitted; dependent `κ` dies with `M`; independent `κ'` survives). Mutants: `mutant_self_commit` (declares `commit = 1`; refused at admission) and `mutant_world_truth_above_evidence` (declares `2` over evidence `1`; refused). Limitation: the reflexivity predicate on content is registered, not derived; an unregistered self-reference is not caught by this rule (it is the MEG-25 semantic half).

## T8 · MEG-30 · no livelock, snapshot consistency

**Model.** A state is `(𝒦, m, j)`: an immutable space value, a meter `m ∈ ℕ^d` (KS-S7), an escalation level `j ∈ {0,…,8}` (`jump.JumpLevel`). A declared budget `B ∈ ℕ^d`. Transitions: *query* — a pure function of the snapshot `𝒦` it reads (matrix, iterate or fixed point; KS-T05 gives a unique limit, and a step budget bounds the iterate); *learning/Jump* — produces a new value `𝒦'` and charges `m' = m + δ` with `δ ≥ 0`, `δ ≠ 0` (every mutation is metered), admissible only if `m' ≤ B`, else the terminal `CANNOT_CHECK`; *escalation* — `j' > j` (`JumpProposal` requires a level above the incumbent), metered likewise.

**Theorem T8.** (i) Every run performs at most `Σ_i B_i` learning/Jump/escalation transitions and at most 8 escalations; it terminates (`DONE`) or ends in `CANNOT_CHECK`. Queries converge on their snapshot (KS-T05). (ii) Any interleaving of queries with transitions is view-equivalent to the serial schedule that orders transitions by meter value and places each query immediately after the transition that produced the snapshot it read; every query result is reproduced by recomputation on its snapshot's digest.

*Proof.* (i) `ρ(m) = Σ_i (B_i − m_i) ∈ ℕ` strictly decreases at every metered transition and `j` strictly increases in a finite ladder; both are well-founded (Floyd). A transition that would make `ρ < 0` is refused as `CANNOT_CHECK`. (ii) Spaces are values: a transition creates a new value and never mutates the old one, so there are no write–write conflicts on one object and no read of a partially written value; a query's result depends only on its snapshot, so moving it to right after that snapshot's producing transition changes no result (snapshot isolation). ∎

Parent: Floyd well-founded termination (verified), Härder–Reuter ACID (verified); snapshot isolation is listed as candidate in the atlas and is used only as a name. Checker: `check_t8_meg30_no_livelock` (10 simulated runs with budgets 3–20 and a ladder-only run; every run ends `DONE` (4) or `CANNOT_CHECK` (6) within budget; 50 queries replayed on their snapshots with zero mismatches; learning-only loops terminate by the meter alone). Mutants: `mutant_unmetered_transition` (a `δ = 0` learning loop never reaches the budget and runs to the step cap — livelock; caught) and `mutant_stale_cache` (a query served from a cache not invalidated after a transition contradicts recomputation on its snapshot; caught). Limitation: the meter must be strictly positive on every mutation for (i); the OCM `Meter.charge` counts events but a zero `ResourceVector` charge is representable, so KS-S7 should require `δ ≠ 0`, which this note assumes.

## T9 · MEG-31 · the certified-information unit

**Definition.** For a finite hypothesis class `H` and lesson sets `E_0 ⊆ E_1` with version spaces `V(E) = {h ∈ H : h ⊨ E}` (Mitchell), the certified information of the step is `C(E_0 → E_1) = log_2|V(E_0)| − log_2|V(E_1)|` bits, defined only when `V(E_1) ≠ ∅` (otherwise CONTRADICTION / `CANNOT_CHECK`). For a single lesson `ℓ` relative to `V_0`, write `S_ℓ = V_0 ∩ {h ⊨ ℓ}`.

**Theorem T9.** (i) Chain additivity: `C(E_0 → E_2) = C(E_0 → E_1) + C(E_1 → E_2)`. (ii) Independence: if `|S_{ℓ_1} ∩ S_{ℓ_2}|·|V_0| = |S_{ℓ_1}|·|S_{ℓ_2}|` (product rule under the uniform measure on `V_0`), then `C(\{ℓ_1,ℓ_2\}) = C(ℓ_1) + C(ℓ_2)`. (iii) Dependence in the MEG-01 sense (a common source: `S_{ℓ_1} ⊆ S_{ℓ_2}`, in particular the same lesson under two evidence ids): `C(\{ℓ_1,ℓ_2\}) = max(C(ℓ_1), C(ℓ_2)) ≤ C(ℓ_1) + C(ℓ_2)`, strict iff both are positive — two ids for one source count once.

*Proof.* (i) telescoping of logarithms. (ii) `log|V_0| − log|S_1 ∩ S_2| = log|V_0| − (log|S_1| + log|S_2| − log|V_0|)`. (iii) `S_1 ∩ S_2 = S_1` and `C(ℓ_1) ≥ C(ℓ_2)`. ∎

Parent: Hartley/Rényi `H_0` (Theorem A of lane 200, PARENT_OWNED); version spaces (Mitchell 1982, verified). Checker: `check_t9_meg31_information_unit` (`H` = the 16 Boolean functions on two inputs; 50 random chains telescope; two examples on distinct inputs are independent and additive `1 + 1 = 2`; the same example under two ids yields 1 bit). Mutant: `mutant_count_split_source_twice` (sums per-id bits → 2; caught); no-alarm: per-id sums equal the joint for independent ids. Limitation (recorded, not a law): for general dependence `C` is neither sub- nor super-additive — the checker exhibits a super-additive pair on a 15-hypothesis class (`c_{12} = log_2 5 > 2 log_2(15/7)`); "subadditive over dependent lessons" holds for the nested (common-source) case that MEG-01 defines, not for arbitrary correlation.

## T10 · MEG-35 · upper-profile certificates are refinements

**Definition.** Three certificate kinds act on `⟦L,U⟧`: (i) closure ⇒ `⟦L,L⟧`; (ii) bounded alternatives with admissible family `F` (antichain `𝔽 = antichain(F)`) ⇒ `⟦L, U ⊗ 𝔽⟧`, refused (`CANNOT_CHECK`) unless `L ≤ U ⊗ 𝔽`; for a partial profile (`U = 1`) this is `U' = 𝔽`, the atlas form; (iii) hypothesis-class bound with a registered antichain `U_H` (the VSW upper antichain in M3) satisfying `L ≤ U_H ≤ U` ⇒ `⟦L, U_H⟧`.

**Theorem T10.** Each certificate maps `⟦L,U⟧` to a refinement `⟦L,U'⟧` with `L ≤ U' ≤ U`; therefore (KS-T21(c)) certification moves UNKNOWN to LIVE or DEAD only, never flips LIVE and DEAD; LIVE verdicts are untouched (they depend on `L` alone) and DEAD verdicts can only be gained.

*Proof.* (i) `L ≤ L ≤ U`. (ii) `U ⊗ 𝔽 ≤ U` because `⊗` is the meet in the semiring order (`f_{U⊗𝔽} = f_U ∧ f_𝔽`), and `L ≤ U ⊗ 𝔽` is the admissibility check. (iii) by hypothesis. The consequence is KS-T21(c) verbatim. ∎

Parent: Pawlak 1982 lower/upper approximations (verified). Checker: `check_t10_meg35_upper_certificates` (exhaustive at `|E| = 3`: 168 intervals × all 20 families × 8 revocations = 16,064 bounded-alternative checks, 1,344 closure checks, 7,096 class-bound checks; a contradicting certificate is refused as `CANNOT_CHECK`). Mutant: `mutant_certificate_replaces_upper` (`U' = 𝔽` without `⊗ U`, the naive reading when `U ≠ 1`): not a refinement in 1,121 cases, where it turns a DEAD verdict into UNKNOWN (de-certification); caught. Limitation: certificates compose by `⊗` on `U` only when their scopes intersect non-emptily (MEG-03); scope is not modelled here.

## T11 · MEG-01 · evidence dependence: derived evidence flattens exactly

**Definition.** `E = A ⊔ D`; assumptions `A` are the independently revocable ids, `R ⊆ A` always; each derived id `d ∈ D` is an atom with its own interval `Λ_d` over `E`, and the citation relation is well-founded (acyclic). Flattening: `flat⟦L,U⟧ = ⟦flat_L(L), flat_U(U)⟧` with `flat_L(P) = ⊕_{W∈P} ⨂_{e∈W} ι_L(e)`, `ι_L(a) = {{a}}` for `a ∈ A`, `ι_L(d) = flat_L(L_d)`, and `flat_U` likewise on upper sides. A claim citing `d` in a warrant `W ∪ {d}` therefore has flattened warrant `ι(W) ⊗ flat(Λ_d)`, i.e. `Λ_{claim} ⊗ Λ_d` (KS-T20 instance).

**Theorem T11.** (i) For every `R ⊆ A`, `λ_R(flat Λ_x)` equals the liveness computed *through* the derived atoms by KS-T21: `λ^{\downarrow}_R(x)` where an assumption `a` reads LIVE iff `a ∉ R`, a derived id reads `λ^{\downarrow}_R(d)`, and warrants combine by `∧_3`, alternatives by `∨_3`, lower side first and upper side for the DEAD test. (ii) Two sources sharing an assumption never count twice: if `Λ_{d_1} = ⟦{{a,b_1}}⟧`, `Λ_{d_2} = ⟦{{a,b_2}}⟧` and `Λ_x = ⟦{{d_1},{d_2}}⟧`, then `flat Λ_x = ⟦{{a,b_1},{a,b_2}}⟧` is DEAD under `R = {a}` although `x` exhibits two alternatives; only revoking `b_1` or `b_2` alone leaves `x` LIVE (WL-5 strict subadditivity realised).

*Proof.* (i) induction along the well-founded citation order: the base `λ_R(⟦{{a}},{{a}}⟧) = LIVE ⇔ a ∉ R`; the step uses that `flat` is built from `⊕`/`⊗` and `λ_R` is a homomorphism for both (KS-T21), and that the lower/upper split of `λ_R` is preserved because `flat_L` and `flat_U` are computed side-wise. (ii) direct computation. ∎

Parent: ATMS assumptions vs derived nodes (de Kleer 1986, verified in the parents table); provenance semirings (verified). Checker: `check_t11_meg01_evidence_dependence` (60 seeded random dependence structures with 4 assumptions and 3 derived atoms, all 16 revocations: 960 agreements between `flat` and the through-derived computation; `flat(⟦{{d,2}}⟧) = ⟦{{2}}⟧ ⊗ Λ_d`; the shared-assumption case is DEAD under `{a}`). Mutant: `mutant_derived_as_assumption` (treats `d_1, d_2` as primitive assumptions so revoking `a` never reaches them: reads LIVE; caught). No-alarm: genuinely independent sources survive losing one of them. Limitation: cyclic citation is excluded (well-foundedness is an admission obligation, not proved here); `R ⊆ D` is undefined — revoking a derived atom means revoking assumptions in its flattened support.

## 12. Calibration and non-claims

```text
T1  MEG-04 PROVED  (glb exhaustive 3^4×3^4; commit-bottom chain depth 6)     runtime defect noted: compose omits operator factor
T2  MEG-06 PROVED  (exact bracket k≤9; chain-17 unsound-FOUND mutant)         runtime defect noted: navigate starts at s, not αs
T3  MEG-08 PROVED  (30 random spaces × 8 revocations)
T4  MEG-18 PROVED  (additive Jumps; dissipation witness for revoke-only)     removal half = quarantine obligation, not a theorem
T5  MEG-22 PROVED  (upper bound Impact_D(Sh); exact set = KS-T22)
T6  MEG-26 PROVED  (corollary of KS-T20/T21)
T7  MEG-29 PROVED  (admission rule + dependent-certificate corollary)
T8  MEG-30 PROVED  (ranking function + immutable values)                    assumes strictly positive meter charge per mutation
T9  MEG-31 PROVED  (chain/independent/nested); general dependence: NEITHER sub- nor super-additive (witness)
T10 MEG-35 PROVED  (exhaustive n=3, 24,504 checks)
T11 MEG-01 PROVED  (960 random agreements + shared-assumption witness)
NOVELTY NOT_ESTABLISHED
```

Nothing above is a novelty claim. T1 is Biba/Denning, T2 the Neumann series, T3/T6 syntactic non-dependence plus Kleene, T4/T5/T11 ATMS label algebra, T7 a reference-monitor rule, T8 Floyd plus snapshot isolation, T9 Hartley counting, T10 Pawlak approximations. The contribution is that each atlas gap is now an exact object with a checker and a planted mutant instead of prose. Two findings are for the runtime, not the theory: `compose` drops the operator authority factor when no bridge authority is passed (T1 limitation) and `navigate` iterates from `s` rather than `α s`, so its FOUND is not sound for the fixed point (T2 limitation). Checker runtime: under one second on `/usr/bin/python3`.
