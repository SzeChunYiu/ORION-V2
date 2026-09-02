# H-EXT-4 — Quantitative Prospective-Revision Premium V1

**Hypothesis register:** `research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md`, row H-EXT-4 (S1).
**Objects:** the PRA one-step compatibility criterion (`PROSPECTIVE_REVISION_COMPATIBILITY_CRITERION_V1.md`), the joint static/dynamic state optimisation (`JOINT_DYNAMIC_STATE_OPTIMIZATION_V1.md`, Proof Appendix B–F), the premium `Omega_dyn = C_dyn^* - C_stat^*`, and the one-bit witness.
**Mechanisation:** `h_ext4_premium_bounds.py` (exhaustive finite enumeration; receipt in `H_EXT4_RESULT_V1.json`); tests `tests/unit/test_h_ext4_premium_bounds.py`.
**Status:** proof attempt with honest terminals. No manuscript edit; no change to the paper's identity or claims. `NEW_VOCABULARY != NEW_SCIENCE`.

---

## 0. Verdict at a glance

| Candidate | Result | Terminal |
|---|---|---|
| A1 ε-compatibility criterion | proved; sublevel-set restatement of `min_a max_h regret <= ε` | `PARENT_OWNED` (Li–Walsh–Littman a*-irrelevance; Abel et al. approximate abstraction) |
| A2 expected-regret identity + garbling monotonicity | proved; Bayes risk of a garbled experiment | `PARENT_OWNED` (Blackwell 1953; Le Cam deficiency) |
| A3 regret ⇄ added-entropy sandwich (Thm A.1) | proved + mechanised; tight on the witness; assumption PC load-bearing | `PROVED_ELEMENTARY_COMPOSITION` (Fano + min-entropy + refinement lemma) |
| A4 premium-level Fano bound (Cor A.2): every current-optimal state that declines `Omega_dyn` pays regret `>= phi^{-1}(Omega_dyn)` | proved + mechanised; tight on the witness for every prior | `PROVED_ELEMENTARY_COMPOSITION` |
| A5 converse: a lower bound on `Omega_dyn` from the static optimum's regret | refuted by an explicit family (`Omega_dyn -> 0` with regret `>= 1/3`) | `NO_NONTRIVIAL_BOUND` |
| B cardinality (prior-independent) premium | minimisation is classical; witness formula exact; zero-conditions of the two premia are inequivalent (both directions mechanised) | `PARENT_OWNED` (Paull–Unger; Zhang et al. Cor. 3.12) + elementary facts |
| C multi-step reduction to right-congruence | proved; k=2 dormant-conflict counterexample and shared-successor counterexample found | `PARENT_OWNED` (Nerode / AIS P2a / stable quotient / own J3) + counterexamples |

Nothing here is a new information law. The one statement a paper could carry is Corollary A.2 (with its two conceded parents and its explicit assumption); see §6.

---

## 1. Setting

A **registered machine** is `M = (H, P, delta, A*, p)`: a finite state set `H`; a predictive-fibre map `P: H -> fibres`; a deterministic partial successor map `delta: H x X -> H`; nonempty Bayes-optimal action sets `A*(h)`; masses `p(h) >= 0` with `supp = {p > 0}`. This is exactly the object of the paper's mechanical audit (`llm_epistemics_dynamic_phase_audit.py::Machine`).

- A partition `Pi` of `H` is **static-admissible** if it refines `P` and every block has nonempty joint intersection of `A*`. It is **dynamic-admissible** if in addition it is a right congruence (matched definedness, successors of a block under each `x` lie in one block). `C(Pi) = H(Pi(H) | P(H))` in bits over `supp`; `C_stat^*`, `C_dyn^*`, `Omega_dyn = C_dyn^* - C_stat^* >= 0`.
- **One-step terminal model (T).** `supp` is the set of current histories; every defined `(h, x)` has a distinct successor `s_{h,x}` of mass zero, absorbing under all inputs. The paper's P2 fixture is in T.
- **Predictive congruence (PC).** For current `h, h'` with `P(h) = P(h')`: `delta(h,x)` is defined iff `delta(h',x)` is, and then `P(delta(h,x)) = P(delta(h',x))`. (The paper's P2 fixture violates PC: its two successors sit in distinct fibres. See §2.5.)
- **Future regret.** For event `x` and a registered future loss `l_x(s, a) >= 0` on successors, `r_x(h,a) = l_x(delta(h,x),a) - min_b l_x(delta(h,x),b)`. Under 0–1 loss `r_x(h,a) = 1[a notin A*(delta(h,x))]`. For a representation `Z = Pi(H)`,

  `R*_x(Pi) = sum_{cells B} min_a sum_{h in B, delta(h,x) defined} p(h) r_x(h,a) / p(supp)`,  `R*(Pi) = max_x R*_x(Pi)`.

  This is the minimal expected future regret of any `(Z, x)`-measurable deterministic rule (the minimum is attained cell-wise, Prop. A.P2).
- **Added entropy.** For a static-admissible `Pi`,

  `Delta(Pi) = min { H(Pi' | Pi) : Pi' dynamic-admissible, Pi' refines Pi on supp }`

  — the entropy a given current-history representation must add to become prospectively adequate. Always finite (the discrete partition is dynamic-admissible). `Omega_dyn = min_{Pi static-admissible} [ (C(Pi) - C_stat^*) + Delta(Pi) ]` (every dynamic partition refines itself), so `Omega_dyn <= min_{Pi_s static-optimal} Delta(Pi_s)`.
- `h_b` is binary entropy; `phi_k(t) = h_b(t) + t log2(k-1)` is the Fano function for an alphabet of size `k`.

---

## 2. Candidate A — approximate / regret-tolerant compatibility

### 2.1 Lemma A.L1 (one-step reduction; the "adopted finite-state refinement semantics" for one terminal event)

In model T, a partition `Pi` of the current histories extends to a dynamic-admissible partition of `H` iff `Pi` is static-admissible and, for every block `B` and event `x`: definedness is constant on `B`, `P(delta(h,x))` is constant on `B`, and `bigcap_{h in B} A*(delta(h,x)) != emptyset`.

*Proof.* (⇒) Right congruence puts all successors of `B` under `x` in one block, which must be static-admissible: one fibre, nonempty intersection. (⇐) Take the successor blocks `{delta(h,x): h in B}` per `(B, x)`; successors are distinct, so these blocks are disjoint; each is static-admissible by hypothesis; absorbing successors make the partition right-congruent. ∎

Under 0–1 loss the third condition is `R*_x(Pi) = 0`. Hence in T ∧ PC: **dynamic admissibility = static admissibility + zero one-step future regret**, which is the one-sentence appendix statement the clean-room review asked for (Objection 2(a)): for a single terminal event the class `Z_dyn` coincides with Theorem 1's criterion. Mechanised: check `A_L1` (every partition of every machine in the `n0=3` family plus 200 random non-PC terminal machines).

### 2.2 Proposition A.P1 (ε-criterion) — `PARENT_OWNED`

Define `A*_{x,ε}(h) = {a : r_x(h,a) <= ε}`. A deterministic rule `g(z,x)` with `r_x(h, g(z,x)) <= ε` for every `h` in cell `C(z,x)` exists iff `bigcap_{h in C(z,x)} A*_{x,ε}(h) != emptyset`, iff `min_a max_{h in C(z,x)} r_x(h,a) <= ε`.

*Proof.* Identical to Theorem 1 with `A*` replaced by its ε-sublevel set; the minimax form is the definition of the sublevel set. ∎

This is the ε-tolerant version of Li–Walsh–Littman's `a*`-irrelevance abstraction (Abel–Hershkowitz–Littman 2016 give the approximate ladder). It is not a result. Mechanised on random loss tables (`A_P1_P2`).

### 2.3 Proposition A.P2 (expected regret; garbling) — `PARENT_OWNED`

`R*_x(Pi)` as defined in §1 is the minimum over all `(Pi, x)`-measurable rules of the expected future regret, and if `Pi'` coarsens `Pi` then `R*_x(Pi') >= R*_x(Pi)`.

*Proof.* A rule is a choice per cell; the expectation is a sum over cells, minimised cell-wise. A `Pi'`-measurable rule is `Pi`-measurable. ∎

This is the Bayes risk of a garbled experiment (Blackwell 1953); the loss-uniform version is Le Cam's deficiency (`R*(Z) <= deficiency(Z, H) · sup l`). The "trivial cell-wise bound" the task mentions is therefore not a bound but the exact value; no information-theoretic inequality can be stronger than it.

### 2.4 Theorem A.1 (regret ⇄ added-entropy sandwich) — `PROVED_ELEMENTARY_COMPOSITION`

Let `Pi` be static-admissible with 0–1 future loss.

**(i) Lower side, every registered machine:** `-log2(1 - R*(Pi)) <= Delta(Pi)`, equivalently `R*(Pi) <= 1 - 2^{-Delta(Pi)}`.

**(ii) Upper side, model T with PC:** `Delta(Pi) <= sum_{x in X} phi_{k_x}(R*_x(Pi))`, where `k_x` is the size of the future action alphabet `bigcup_h A*(delta(h,x))` for event `x`.

**(iii) General label form, model T without PC:** `Delta(Pi) = min_d H(L_d | Pi, P)` where `d` ranges over successor selectors (`d(s) in A*(s)`) and `L_d(h) = (1[delta(h,x) defined], P(delta(h,x)), d(delta(h,x)))_{x in X}`.

*Proof of (i).* Let `Pi'` be a dynamic-admissible refinement of `Pi` on `supp` attaining `Delta(Pi)`. Fix an event `x` and a block `B` of `Pi` with `Pi'`-sub-blocks `B_1..B_k` of mass fractions `q_1..q_k`. Dynamic admissibility of `Pi'` gives, for each `i`, either `delta(·,x)` undefined on all of `B_i`, or all successors of `B_i` in one static-admissible block, hence some `a_i in bigcap_{h in B_i} A*(delta(h,x))`. Let `i* = argmax_i q_i`. Playing `a_{i*}` on cell `B` is wrong at most on `B \ B_{i*}`, so the cell regret satisfies `R*_{x,B} <= 1 - max_i q_i <= 1 - 2^{-H(q)}` by `H_inf(q) <= H(q)` (min-entropy is at most Shannon entropy), where `H(q) = H(Pi' | B)`. Averaging over blocks with weights `w_B = p(B)/p(supp)` and using concavity of `t -> 1 - 2^{-t}` (Jensen):
`R*_x(Pi) = sum_B w_B R*_{x,B} <= sum_B w_B (1 - 2^{-H(Pi'|B)}) <= 1 - 2^{-H(Pi'|Pi)} = 1 - 2^{-Delta(Pi)}`.
Take the maximum over `x`. ∎

*Proof of (iii).* By Lemma A.L1 the join `Pi ∨ L_d` (on `supp`) extends to a dynamic-admissible partition, with `H(Pi ∨ L_d | Pi) = H(L_d | Pi, P)`; so `Delta(Pi) <= min_d H(L_d|Pi,P)`. Conversely any dynamic-admissible `Pi'` refining `Pi` has, per block and event, a common successor fibre, matched definedness and a common acceptable action `d'`; hence `Pi'` refines `Pi ∨ L_{d'}` and `H(Pi'|Pi) >= H(L_{d'}|Pi,P)`. ∎

*Proof of (ii).* Under PC, definedness and the successor fibre are functions of `P(h)`, so `H(L_d | Pi, P) = H((d(delta(H,x)))_x | Pi, P) <= sum_x H(d(delta(H,x)) | Pi, P)` (subadditivity). For each `x` choose `d` on the successors of `x` as follows: let `g(B)` be the cell-optimal action of cell `B`; put `d(delta(h,x)) = g(B)` when `g(B) in A*(delta(h,x))` and any element of `A*(delta(h,x))` otherwise. Then the estimator `hat d = g(Pi(H))` errs exactly when `g(B) notin A*(delta(h,x))`, i.e. with probability `R*_x(Pi)` (conditional on definedness). Fano's inequality for an arbitrary estimator gives `H(d | Pi, P, defined) <= phi_{k_x}(R*_x(Pi) / p_def)`, and `p_def · phi(t/p_def) <= phi(t)` because `phi` is concave with `phi(0) = 0`. Sum over `x`. ∎

**Tightness (mechanised, `A_T3`).** On the two-history witness with prior `(q, 1-q)` and the merged (static-optimal) state: `Delta = h_b(q)`, `R* = min(q, 1-q)`, so the Fano side is an equality for **every** prior (`phi_2(min(q,1-q)) = h_b(q)`), and the lower side is an equality exactly at `q = 1/2` (`-log2(1/2) = 1`). Both sides are also equalities for any uniform cell whose histories all require distinct future actions (`k` histories: `Delta = log2 k = -log2(1 - (k-1)/k) = phi_k((k-1)/k)`). Neither side is tight in general: the fixture `loose_ub_label` (masses `1/2,1/4,1/4`) has `-log2(1-R*) = 0.415 < Delta = 0.689 < phi = 0.811`.

### 2.5 Corollary A.2 (premium-level bound; regret floor for declining the premium)

In model T with PC, for every static-optimal `Pi_s`:

`Omega_dyn <= Delta(Pi_s) <= sum_x phi_{k_x}(R*_x(Pi_s))`,

hence, for a single event, **every current-task-optimal representation has one-step future regret `R*(Pi_s) >= phi_{k}^{-1}(Omega_dyn)`** (inverse of `phi_k` on `[0, 1 - 1/k]`, where `R*` always lies because `max_a P(a acceptable | cell) >= 1/k`). Under 0–1 loss with two future actions this reads `R*(Pi_s) >= h_b^{-1}(Omega_dyn)`; on the witness it is an equality for every prior: `h_b^{-1}(h_b(q)) = min(q, 1-q)`.

*Proof.* `Omega_dyn <= Delta(Pi_s)` because `Pi_s` costs `C_stat^*` and its cheapest dynamic refinement costs `C_stat^* + Delta(Pi_s)`; the rest is Theorem A.1(ii). ∎

**PC is load-bearing (mechanised, `A_T2_upper_bound_without_pc`).** The fixture `phantom_premium` (two equiprobable histories, identical unique actions everywhere, successors in distinct fibres) has `Omega_dyn = 1 bit` with `R*(Pi_s) = 0` for the static optimum: the Fano form gives `0`, and fails. The label form (iii) still holds (`H(P(delta(H,x)) | Pi_s) = 1`). Interpretation: `Omega_dyn` as defined in the paper charges for **successor predictive-state separation** even when no decision is ever affected — a predictive-drift component with no regret meaning. In the paper's own P2 fixture the successors are placed in distinct fibres (`P = (0,0,1,2)`), so its 1 bit is over-determined (decision conflict and fibre drift both force the split); the `same_succ_fibre` variant (`P = (0,0,1,1)`) shows the decision conflict alone yields the same 1 bit (witness table, both rows). No manuscript claim changes; the observation is recorded for the paper's owners.

### 2.6 Theorem A.3 (no non-trivial converse) — `NO_NONTRIVIAL_BOUND`

There is no function `f` with `f(t) > 0` for `t > 0` such that `Omega_dyn >= f(min_{Pi_s static-optimal} R*(Pi_s))` on every machine in T ∧ PC.

*Proof (explicit family, mechanised `A_C1`).* Masses `(1-2u, u, u)`, one fibre; current actions `{0}, {0,1}, {1}`; future actions `{0}, {1}, {1}`. For `u < 1/3` the unique static optimum is `{h0,h1},{h2}` with cost `h_b(u)` and regret `R* = u` (history `h1` is mis-served); the dynamic optimum is `{h0},{h1,h2}` with cost `h_b(2u)`. Hence `Omega_dyn = h_b(2u) - h_b(u) -> 0` as `u -> 1/3^-` while `R* -> 1/3`. Values: `u = 1/4: Omega = 0.189`; `u = 0.30: 0.090`; `u = 0.33: 0.0099`; `u = 0.333: 0.0010`. ∎

Two related candidate bounds are also dead: (a) `Omega_dyn >= -log2(1 - R*(Pi_s))` for a static optimum fails on the same fixture at `u = 1/4` (`0.415 > 0.189`); (b) the "min over all static-admissible `Pi` of `(C(Pi) - C_stat^*) - log2(1 - R*(Pi))`" is a valid but **vacuous** lower bound — it is attained by the dynamic optimum itself (`R* = 0`, overhead `Omega_dyn`) — and is not reported as a result. The mechanism: `Omega_dyn` is a *difference of two minima* that can vanish through near-ties in static cost while every static optimum keeps large regret; the per-representation quantity `Delta(Pi)` (Theorem A.1) is the object that is genuinely sandwiched by regret. `Omega_dyn = 0` iff some static optimum has `R* = 0` remains true in T ∧ PC (by A.L1) — Theorem-1-level content.

---

## 3. Candidate B — prior-independent (cardinality) premium

Let `K(Pi) = max_f |{blocks of Pi inside fibre f} ∩ supp|`, `K_stat^* = min over static-admissible`, `K_dyn^* = min over dynamic-admissible`, `Omega_card = log2 K_dyn^* - log2 K_stat^* >= 0`.

**Proposition B.1.** `C_stat^* <= log2 K_stat^*` and `C_dyn^* <= log2 K_dyn^*`. *Proof.* Take the cardinality minimiser `Pi`; `H(Pi|P) = sum_f w_f H(Pi | f) <= sum_f w_f log2 K_f <= log2 K(Pi)`. ∎ (Mechanised on 25k+ machines, zero violations.)

**Proposition B.2 (witness formula).** For the two-history witness with prior `(q, 1-q)`, `q in (0,1)`: `C_stat^* = 0`, `C_dyn^* = Omega_dyn = h_b(q)`, `K_stat^* = 1`, `K_dyn^* = 2`, `Omega_card = 1` (prior-independent), `R*(merged) = min(q,1-q)` and `Omega_dyn = h_b(R*)`. In particular `Omega_dyn(0.9) = 0.469 bit` as quoted by the clean-room review, `Omega_dyn <= Omega_card` with equality iff `q = 1/2`. *Proof.* The single fibre must be split dynamically (disjoint successor actions) and need not be split statically; entropy of the split is `h_b(q)`, its cardinality is 2. ∎

**Proposition B.3 (no ordering; inequivalent zero-conditions).** Both `Omega_dyn > Omega_card` and `Omega_dyn < Omega_card` occur (uniform 3-history machine with `Omega_dyn = 2/3 > log2(3/2)`; witness at `q = 0.9`). Moreover `Omega_card = 0` does not imply `Omega_dyn = 0` (`loose_ub_label`: `K_stat^* = K_dyn^* = 2`, `Omega_dyn = 0.189`) and `Omega_dyn = 0` does not imply `Omega_card = 0` (`omega_dyn_zero_card_positive`: masses `(49,49,1,1)/100`, current `{0,1},{0,2},{1},{2}`, future `{0},{0},{1},{2}`: the entropy-optimal static partition `{h0,h1},{h2},{h3}` (3 blocks, 0.161 bit) is dynamic, while the only 2-block static partition `{h0,h2},{h1,h3}` is not; `Omega_dyn = 0`, `Omega_card = log2 1.5`). *Proof.* Exhaustive check of the named fixtures. ∎

**Ownership.** `K_dyn^*` restricted to a fibre is the minimum closed cover of an incompletely specified machine (Paull–Unger 1959) and is the object of Zhang et al. 2026 Cor. 3.12 (`max_o |C_o|` reusable memory symbols). Terminal: `PARENT_OWNED` for the minimisation; B.2–B.3 are elementary computed facts that answer the review's request to report `log2|Z|` beside `H(Z|S)`: the two premia agree on *existence* (both positive on the witness for every prior) but not on *zero-ness* or *ordering*, so neither is a faithful surrogate for the other.

---

## 4. Candidate C — multi-step (recursive) case

On a general registered machine and a partition `Pi` of `H` define: **N1(Pi)** — one-step action compatibility at every node (matched definedness and nonempty `bigcap_{h in B} A*(delta(h,x))` for every block `B` and input `x`); **W_k(Pi)** — the same for every word of length `1..k`; **RC(Pi)** — right congruence.

**Theorem C.1.**
(a) `Pi` is the state partition of a deterministic recursively updateable state with an acceptable decoder at every node iff `Pi` is static-admissible, `RC(Pi)` and `N1(Pi)`.
(b) `RC ∧ N1 ⇒ W_k` for all `k`; (c) `W_k ⇒ N1` for `k >= 1`; (d) the coarsest right-congruent refinement `rc(Pi)` preserves `N1` and `W_k`; hence every `N1` partition has a recursively compatible refinement, and the cheapest one is `rc(Pi)`: `min{ C(Pi') : Pi' dynamic-admissible, Pi' refines Pi } = C(rc(Pi))`.

*Proof.* (a) A recursive state `z_{t+1} = u(z_t, x)` induces a partition whose blocks have matched definedness and successors in one block (RC); an acceptable decoder per block is exactly N1 at the block's successors together with static admissibility. Conversely RC defines `u` and N1 supplies the decoder. (b) Induction on word length: successors of a block under `x` lie in one block, which is N1 for the remaining word. (c) Words of length 1. (d) Refinement shrinks cells, so intersections can only grow; `rc(Pi)` is right-congruent by construction; any right-congruent refinement of `Pi` refines `rc(Pi)` (coarsest), and conditional entropy is monotone under refinement. ∎

This is the paper's Proposition D.1/J3 with a general base partition in place of `(S_P, d)`; the substrate is Nerode right congruence, Subramanian et al. 2022 P2a and Zhang et al. 2026's stable quotient. Terminal: `PARENT_OWNED`.

**Counterexample C.2 (k = 2 dormant conflict; mechanised `dormant_two_step`).** Chain `h0,h1 -> s0,s1 -> t0,t1`, masses `1/2,1/2` on `h`, zero below; `A* = {0}` everywhere except `A*(t0) = {1}`, `A*(t1) = {2}`; fibres by depth. `Pi = {h0,h1},{s0},{s1},{t0},{t1}` satisfies static admissibility, `N1` and `W_1`, but not `W_2` and not `RC`; `rc(Pi)` is discrete. Horizon costs: `C_{W_1} = 0 < C_{W_2} = 1 = C_dyn^*`. So one-step compatibility at every node — the non-recursive reading, where the representation is recomputed from the full history at each step — is insufficient at `k = 2`: the conflict is dormant for one step and a recursive state cannot separate `s0` from `s1` because `z_1 = u(z_0, x)` is the same for both.

**Counterexample C.3 (shared successors; mechanised `shared_successor`).** With non-injective `delta` (`h0,h2 -> s_a`, `h1 -> s_b`, `h3 -> s_c`, `A*(s_a) = {0,1}`, `A*(s_b) = {0}`, `A*(s_c) = {1}`), the initial partition `{h0,h1},{h2,h3}` is word-compatible for every `k` yet has **no** recursive extension: the successor blocks `{s_a,s_b}` and `{s_a,s_c}` must merge transitively into `{s_a,s_b,s_c}`, whose intersection is empty. In the injective zero-mass chain model (histories as sequences, `delta(h,x) = h·x`), word compatibility of an initial partition is equivalent to the existence of a recursive extension (mechanised on depth-2 chains, `chain_equivalence_violations = 0`; proof: image blocks are disjoint under injectivity and admissible by `W_k`). Hence the paper's word-horizon semantics and its recursive semantics agree exactly in the sequence model and separate only through shared successors.

**Remark C.4 (multi-step Fano form; mechanised `C3`).** On depth-`k` chains with PC, `Omega_dyn <= phi_{|A|^W}( sum_{|w| <= k} R*_w(Pi_s) )` with `W` the number of words (union bound on the future-action profile); valid, loose, mechanised for `k = 2`.

**Observation C.5 (audit horizon semantics; out of scope, recorded).** `llm_epistemics_dynamic_phase_audit.py::k_admissible_literal` uses block-level word *congruence* (word successors of a block must land in one block). For `k = 1` this is already right congruence, so on every machine its `C_1 = C_inf` and the horizon curve cannot distinguish horizons `>= 1`. The action-word notion `W_k` of this note is the one that produces a non-trivial curve (`0, 0, 1` on C.2). This does not affect any manuscript claim (the paper reports `C_stat^*`/`C_dyn^*`, not the curve) and is flagged as a separate task.

---

## 5. Parent attribution

| Ingredient | Parent | Where used | Verdict |
|---|---|---|---|
| Garbling never lowers Bayes risk; exact cell-wise Bayes risk | Blackwell 1953 (comparison of experiments); Brodu decisional states | A.P2, A.L1 | `DIRECT_PARENT` |
| Loss-uniform regret gap | Le Cam deficiency | A.P2 remark | `DIRECT_PARENT` |
| `H(X|Y) <= h_b(P_e) + P_e log(|X|-1)` for any estimator | Fano 1961 (Cover–Thomas Thm 2.10.1) | A.1(ii), A.2 | `DIRECT_PARENT` |
| `H_inf <= H`; `1 - max q <= 1 - 2^{-H(q)}`; Jensen | elementary (Rényi entropies) | A.1(i) | `ELEMENTARY` |
| any-optimal-action semantics = `a*`-irrelevance; ε-tolerant abstraction | Li–Walsh–Littman 2006; Abel–Hershkowitz–Littman 2016 | A.P1 | `DIRECT_PARENT` |
| refine-by-label construction; closed cover / compatibles | Paull–Unger 1959 ISFSM minimisation | A.L1, A.1(iii), B | `STRONG_PARENT` |
| per-fibre symbol count `max_o |C_o|` | Zhang et al. 2026 Cor. 3.12 | B | `DIRECT_PARENT` |
| recursive state = right congruence; coarsest stable refinement | Nerode; Subramanian et al. 2022 P2a; Zhang et al. 2026 Thm 3.8 | C.1 | `DIRECT_PARENT` |
| selector-refinement equality | own `JOINT_DYNAMIC_STATE_OPTIMIZATION_V1` J3 / Appendix D.1 | C.1(d) | internal |

---

## 6. What this licenses, and what it does not

- **Licensed (one sentence, if the paper's owners want it):** "In the one-step evidence model with predictive congruence, a representation that is optimal for the current tasks and declines the prospective premium `Omega_dyn` incurs one-step future regret at least `phi^{-1}(Omega_dyn)` (Fano), and the added entropy `Delta(Pi)` any current-task representation needs is sandwiched as `-log2(1-R*(Pi)) <= Delta(Pi) <= phi(R*(Pi))`; both bounds are attained by the one-bit witness at the uniform prior, and the Fano bound at every prior." It must concede Fano and the min-entropy inequality as the entire analytic content and Li–Walsh–Littman / Paull–Unger for the constructions, and must state PC explicitly (the phantom-premium fixture shows the bound is false without it).
- **Not licensed:** any lower bound on `Omega_dyn` from regret (Theorem A.3); any claim that the cardinality and entropy premia are interchangeable (B.3); any claim that per-step one-step compatibility certifies recursive compatibility (C.2, C.3); any change to the paper's identity. The result modestly strengthens Objection 1(ii) ("a quantitative theorem connecting current-equivalence margins to prospective regret") at corollary level; it does not turn the paper from framework into method.
- **Honest grade of the composite:** `PROVED_ELEMENTARY_COMPOSITION`, not `NONTRIVIAL_THEOREM`. The information-theoretic side collapses to standard Fano; the decision side collapses to Blackwell; the only non-parent content is the identification of `Delta(Pi)` as the sandwiched object and the explicit witnesses (tight, loose, phantom, vanishing).

---

## 7. Mechanised-check receipt

Pure Python, exhaustive enumeration, `TOL = 1e-9` on floats (masses exact `Fraction`; entropies `log2` floats). The sweep is now run with no cap, so every enumerated terminal family is exhausted and no stride subsample is taken: `terminal_n0=2_x=1_A<=3_uniform+skewed`: size 14406, stride 1, examined 14406 (exhaustive); `terminal_n0=3_x=1_A<=3_uniform`: size 588245, stride 1, examined 588245 (exhaustive); `terminal_n0=3_x=1_A<=2_skewed`: size 7290, stride 1, examined 7290 (exhaustive); `terminal_n0=4_x=1_A<=2_uniform`: size 98415, stride 1, examined 98415 (exhaustive); `terminal_n0=3_x=2_A<=2_uniform`: size 98415, stride 1, examined 98415 (exhaustive). Random families: 3000 general machines (`n <= 5`, arbitrary partial `delta`, masses on any state) and 3000 non-PC terminal machines, seed 20260902. The A.L1 lemma check enumerates all Bell(n) partitions of the full state set on the `n0=3, A<=2` family plus 200 non-PC machines; the bound sweep enumerates partitions of the current histories and extends them canonically to the zero-mass successors (justified by Lemma A.L1). Run: `python3 research/llm-machine-epistemics/h_ext4_premium_bounds.py --full --json-out research/llm-machine-epistemics/H_EXT4_RESULT_V1.json`.

**Scope of the A.1(ii) Fano-form check (receipt schema v2).** The Fano upper bound is asserted only for one-step terminal models satisfying PC, and `T1_fano_ub_violations` counts violations on exactly that hypothesis set; its denominator is `T1_fano_applicable_partitions`. A zero there is a pass on the machines where the bound is claimed, **not** a statement about the machines where it is not: on those the check is skipped, not passed. `T1_fano_ub_violations_ungated_by_pc` drops the PC gate (keeping the terminal model, without which `phi_{k_x}` is not the right-hand side of the bound at all) over `T1_fano_terminal_partitions_ungated_by_pc`, and records how often `Delta(Pi) > sum_x phi_{k_x}(R*_x(Pi))` actually fails. Both numbers are reported per family below.

| Check | Instances | Outcome |
|---|---|---|
| A.1(i) `-log2(1-R*) <= Delta` — terminal_n0=2_x=1_A<=3_uniform+skewed | 19845 static partitions / 14406 machines | 0 violations; tight (Δ>0): 444 |
| A.1(ii) `Delta <= Fano` — terminal_n0=2_x=1_A<=3_uniform+skewed | gated (terminal ∧ PC): 19845 partitions; ungated by PC (terminal): 19845 | 0 violations gated / 0 ungated (on 0 machines); PC machines 14406/14406, terminal 14406/14406; tight (Δ>0): 666; both tight: 222 |
| A.2 `Omega <= min Delta(Pi_s)`; label formula = Δ; `Omega <= Fano` — terminal_n0=2_x=1_A<=3_uniform+skewed | 14406 machines (1332 with Ω>0) | 0 / 0 / 0 violations; Fano tight among Ω>0: 666 |
| A.1(i) `-log2(1-R*) <= Delta` — terminal_n0=3_x=1_A<=3_uniform | 1179234 static partitions / 588245 machines | 0 violations; tight (Δ>0): 1014 |
| A.1(ii) `Delta <= Fano` — terminal_n0=3_x=1_A<=3_uniform | gated (terminal ∧ PC): 1179234 partitions; ungated by PC (terminal): 1179234 | 0 violations gated / 0 ungated (on 0 machines); PC machines 588245/588245, terminal 588245/588245; tight (Δ>0): 7098; both tight: 1014 |
| A.2 `Omega <= min Delta(Pi_s)`; label formula = Δ; `Omega <= Fano` — terminal_n0=3_x=1_A<=3_uniform | 588245 machines (103458 with Ω>0) | 0 / 0 / 0 violations; Fano tight among Ω>0: 7098 |
| A.1(i) `-log2(1-R*) <= Delta` — terminal_n0=3_x=1_A<=2_skewed | 14904 static partitions / 7290 machines | 0 violations; tight (Δ>0): 30 |
| A.1(ii) `Delta <= Fano` — terminal_n0=3_x=1_A<=2_skewed | gated (terminal ∧ PC): 14904 partitions; ungated by PC (terminal): 14904 | 0 violations gated / 0 ungated (on 0 machines); PC machines 7290/7290, terminal 7290/7290; tight (Δ>0): 360; both tight: 30 |
| A.2 `Omega <= min Delta(Pi_s)`; label formula = Δ; `Omega <= Fano` — terminal_n0=3_x=1_A<=2_skewed | 7290 machines (1244 with Ω>0) | 0 / 0 / 0 violations; Fano tight among Ω>0: 360 |
| A.1(i) `-log2(1-R*) <= Delta` — terminal_n0=4_x=1_A<=2_uniform | 306990 static partitions / 98415 machines | 0 violations; tight (Δ>0): 1362 |
| A.1(ii) `Delta <= Fano` — terminal_n0=4_x=1_A<=2_uniform | gated (terminal ∧ PC): 306990 partitions; ungated by PC (terminal): 306990 | 0 violations gated / 0 ungated (on 0 machines); PC machines 98415/98415, terminal 98415/98415; tight (Δ>0): 2726; both tight: 1362 |
| A.2 `Omega <= min Delta(Pi_s)`; label formula = Δ; `Omega <= Fano` — terminal_n0=4_x=1_A<=2_uniform | 98415 machines (24410 with Ω>0) | 0 / 0 / 0 violations; Fano tight among Ω>0: 2162 |
| A.1(i) `-log2(1-R*) <= Delta` — terminal_n0=3_x=2_A<=2_uniform | 201204 static partitions / 98415 machines | 0 violations; tight (Δ>0): 0 |
| A.1(ii) `Delta <= Fano` — terminal_n0=3_x=2_A<=2_uniform | gated (terminal ∧ PC): 201204 partitions; ungated by PC (terminal): 201204 | 0 violations gated / 0 ungated (on 0 machines); PC machines 98415/98415, terminal 98415/98415; tight (Δ>0): 5400; both tight: 0 |
| A.2 `Omega <= min Delta(Pi_s)`; label formula = Δ; `Omega <= Fano` — terminal_n0=3_x=2_A<=2_uniform | 98415 machines (28248 with Ω>0) | 0 / 0 / 0 violations; Fano tight among Ω>0: 5400 |
| A.1(i) `-log2(1-R*) <= Delta` — random_general_n<=5 | 17991 static partitions / 3000 machines | 0 violations; tight (Δ>0): 10 |
| A.1(ii) `Delta <= Fano` — random_general_n<=5 | gated (terminal ∧ PC): 10 partitions; ungated by PC (terminal): 12 | 0 violations gated / 1 ungated (on 1 machines); PC machines 1508/3000, terminal 11/3000; tight (Δ>0): 0; both tight: 0 |
| A.2 `Omega <= min Delta(Pi_s)`; label formula = Δ; `Omega <= Fano` — random_general_n<=5 | 3000 machines (1541 with Ω>0) | 0 / 0 / 0 violations; Fano tight among Ω>0: 0 |
| A.1(i) `-log2(1-R*) <= Delta` — random_terminal_nonPC | 5460 static partitions / 3000 machines | 0 violations; tight (Δ>0): 49 |
| A.1(ii) `Delta <= Fano` — random_terminal_nonPC | gated (terminal ∧ PC): 1962 partitions; ungated by PC (terminal): 5460 | 0 violations gated / 1308 ungated (on 991 machines); PC machines 1409/3000, terminal 3000/3000; tight (Δ>0): 23; both tight: 7 |
| A.2 `Omega <= min Delta(Pi_s)`; label formula = Δ; `Omega <= Fano` — random_terminal_nonPC | 3000 machines (1363 with Ω>0) | 0 / 0 / 934 violations; Fano tight among Ω>0: 79 |
| A.2 without PC (random non-PC terminal) | 3000 machines (1409 satisfy PC) | PC_LOAD_BEARING_FOR_FANO_FORM__LABEL_FORM_HOLDS: premium-level Fano-form violations 934, `Omega <= min Delta` violations 0, label-form violations 0; per-partition `Delta > Fano` ungated by PC 1308 of 5460 partitions on 991 machines, vs 0 on the 1962 PC partitions |
| A.L1 one-step reduction lemma | 761547 partitions | PASS (0 mismatches) |
| A.P1 ε-criterion = minimax cell regret ≤ ε | 5967 (cell, ε) pairs | PASS (0 mismatches) |
| A.P2 garbling monotonicity of Bayes regret | 2649 nested pairs | 0 violations |
| A.3 no converse bound | vanishing family (488 sweep violations of the candidate lower bound) | REFUTED: u=1/4: Ω=0.1887, R*≥0.250; u=3/10: Ω=0.0897, R*≥0.300; u=8/25: Ω=0.0383, R*≥0.320; u=33/100: Ω=0.0099, R*≥0.330; u=333/1000: Ω=0.0010, R*≥0.333 |
| A.T3 witness table | 8 rows (priors × fibre layouts) | q=1/2: Ω=1.0000, Ω_card=1, Fano tight=True; q=3/4: Ω=0.8113, Ω_card=1, Fano tight=True; q=9/10: Ω=0.4690, Ω_card=1, Fano tight=True; q=99/100: Ω=0.0808, Ω_card=1, Fano tight=True |
| B.1 `C* <= log2 K*` | 223171 machines | 0 violations |
| B.3 orderings / zero-conditions | same | Ω_dyn>Ω_card: 6646; Ω_dyn<Ω_card: 45307; Ω_card=0<Ω_dyn: 4800; Ω_dyn=0<Ω_card: 0 (+ named fixture) |
| B.4 is the Ω_card/Ω_dyn non-ordering a max-over-classes artifact? | 5 instances behind Remark A.5(d) | NON_ORDERING_NOT_A_MAX_VS_MEAN_ARTIFACT: all 5 have one predictive class among current histories, so max and total block count coincide; 0 orderings flip under a total-count K |
| C.1 (b),(c) implications | 2526 random partitions | 0 / 0 violations; N1∧¬W2 instances: 152 |
| C.3 shared successor / chain equivalence | 1113 chain instances | chain violations 0 |
| C.4 multi-step Fano form, depth-2 chains | 400 chains | 0 violations |

Totals: 812771 machines and 1745628 static-admissible partitions in the bound sweep; seed 20260902; all five enumerated terminal families exhausted. Bound (i) holds on every one of the 1745628 partitions. Bound (ii) is asserted on 1724149 partitions (terminal ∧ PC) and holds on all of them; dropping PC over the 1727649 partitions of terminal models exposes 1309 violations on 992 machines, every one of them a machine that fails PC. Receipt schema `orion-v2.h-ext4-premium-bounds.v2`.

## 8. Files

- `research/llm-machine-epistemics/h_ext4_premium_bounds.py` — checker (`--full` for the receipt above).
- `research/llm-machine-epistemics/H_EXT4_RESULT_V1.json` — machine-readable terminals + receipt.
- `tests/unit/test_h_ext4_premium_bounds.py` — named fixtures and the small sweep (seconds).

`scientific_authority = false`, `empirical_llm_result = false`.
