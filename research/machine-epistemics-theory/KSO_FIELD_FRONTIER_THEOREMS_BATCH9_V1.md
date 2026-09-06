# KSO field-frontier theorems — batch 9 (I1–I4)

Date 2026-09-06. Ninth one-day batch, the second of the field-completion programme (ORION-V2 #353) over
the Machine Epistemics field frontier (`field_dynamics_v1/FRONTIER.md`). Scope: four frontier rows —
FDX-08 stochastic warrant dynamics (I1), FDX-11 epistemic bifurcation / obstruction (I2), FDX-13 self-model
calibration and reflexive dependence (I3), FDX-15 parent-product equivalence / residual theorem (I4). Each
row is closed as PROVED on a finite fixture, bounded exactly (an impossibility with a witness), PARENT_OWNED /
PARENT_SUFFICIENT with the executable rule and its falsifier, or stated as a CONJECTURE with its falsifier.
The FDX ids are kept.

Every item has an exact finite checker (`kso_field_frontier_batch9_exact.py`, stdlib only; every count an
integer, every probability an exact `Fraction`; exit 0 / 1 / 2 with 2 = CANNOT_CHECK), at least one planted
hostile whose mutation is asserted applied and caught, and a no-alarm control;
`tests/unit/test_kso_field_frontier_batch9.py` pins every count. Checker run on billy-old (Python 3.14.4):
exit 0, wall 6.6 s, `"status": "ALL_HOLD"`, `"OPEN": []`, one CONJECTURE (the general FDX-15 equivalence);
new tests and batches 5–8 (with the batch-6 revision-boundary suite) as reported in the verification block
at the end. All objects are re-implemented inside the checker (two-state evidence chains and a
likelihood-ratio test martingale, an antichain warrant lattice with nogoods and authority bits, a routed
self-prediction loop, a paired-lifetime comparison with an ablation arm); nothing imports `ocm`; nothing
ran on the Mac. The status table for this batch is section N of `ME_THEORY_GAP_ATLAS_ADDENDA_V1.md`
(the atlas itself is byte-sealed by `authority_reconciliation_v1/SOURCES_V1.json` and is not edited;
section M is batch 10's, written in parallel); the frontier dispositions are in
`field_dynamics_v1/FRONTIER.md` (not sealed).

NO NOVELTY OR SUPERIORITY CLAIM. Every probabilistic, lattice-theoretic, game-theoretic or statistical fact
used is a named parent's; the contribution is the exact statement on the registered objects of `FIELD.md`,
the executable falsifier, and the reading of what the OCM code and the M12 V4 / V4-R inputs can and cannot
support. Rigour follows the batch-6 integration review: two-sided decisions use twice the smaller tail
(only one-sided pre-registered rules appear here); exchangeability alone is never sufficient for binomial
inference (the one-coin collapse is a first-class verdict); no scalar-semiring over-claim (the graded half
of MEG-02 is not reopened — D3 / F6 / G6 stand); ceilings are stated for the registered algorithm only;
identification bounds are guarantees, never accusations.

Notation as in batches 1–8 and `FIELD.md`: registered state `Ξ = (K, Λ, D, N, A, S, P, H, O, 𝔠, B, X)`,
semantic projection `π_sem(Ξ)`, liveness LIVE / UNKNOWN / DEAD (KS-T21), warrant interval `⟦lo, up⟧`,
transition families F / E / L / R / M / G. `[φ]` is the indicator of `φ`.

## I1 · FDX-08 · stochastic warrant dynamics: what a time-indexed claim, a reopening bound and a receipt may state

**Objects.** One atom `a` whose single supporting evidence id is active (LIVE) or revoked (DEAD) at each of
`T = 6` ledger steps; the ledger path `ω ∈ {L, D}^6` (64 paths, `x₀ = L` at admission). A *registered
generating model* is a two-state chain `M(a, b)`: `P(L→D) = a`, `P(D→L) = b`, `a, b ∈ {¼, ½, ¾}` (9 models;
the 3 with `a + b = 1` are the i.i.d. members — the next state does not depend on the current one). An
*adversary with envelope ρ* chooses any path with at most `ρ` revocations (`L→D` transitions) and carries
no probability (the FDX-02 envelope). A *time-indexed claim* is "`a` is LIVE at `t`": for `t ≤ T` it is the
ledger fact `x_t`; for `t > T` it is a statement about the law of future paths. A *receipt* may carry the
ledger liveness now (exact) and a predictive probability `P_M(x_{T+1} = L | ω)` **only** as a claim typed
`CONDITIONAL_ON_MODEL:M` — the model id is a revocable assumption in the receipt, as the frozen ids are in
FDX-01's CONDITIONAL_ON_ASSUMPTIONS; with no model registered the receipt is `NO_MODEL_REGISTERED` and
carries nothing stochastic. Separately, a *registered operator guarantee* `g` ("success probability ≥ ¾",
the scoped OPERATOR_GUARANTEE of D3) is monitored on a Bernoulli outcome stream of length `T₂ = 12`; the
*e-process* is the likelihood-ratio test martingale of the alternative `½` against the guaranteed `¾`, and
the guarantee is revoked when `e_t ≥ 1/α = 20` at any `t` (α = 1/20).

**Theorem.** (i) *Exactness of time-indexed claims.* The marginal `P_M(x_t = L)` by path enumeration equals
the Chapman–Kolmogorov recursion on all 54 (M, t) pairs; every path has positive probability under every
registered model. (ii) *Reopening rates.* `E_M[#flips]` is exact per model (`3` at `a = b = ½`, `3/2` at
`a = b = ¼`, `9/2` at `a = b = ¾`); under an adversary with envelope `ρ` the number of liveness flips over `T`
steps is at most `min(2ρ, T)` (exact on all 7 envelopes); with **no** model and **no** envelope the only
bound is `T` itself — for every claimed bound `b < T` there is an admissible path with more than `b` flips
(6 witnesses). So a bounded reopening rate exists **iff** a generating model or a revision envelope is
registered: EXACTLY_BOUNDED_IMPOSSIBILITY otherwise. (iii) *Receipts.* All 64 × 10 receipts are typed; every
predictive value lies strictly inside (0, 1) and is stamped with its model id. (iv) *The predictive
probability is not a function of the path.* On every path the 9 registered models give exactly three
predictive values with spread `½` (64/64); the empirical LIVE rate equals a registered prediction on 20 paths
(those with exactly three LIVE steps) and equals no registered model's prediction on the other 44; the
largest likelihood ratio between two registered models on 6 observations is `729 = 3⁶` — finite data weighs
the models and rules none out. (v) *Bayesian updating with revocation.* Revoking the observation at step `j`
means the honest posterior over the model class is recomputed from the surviving observations
(marginalising `x_j`); dividing the likelihood by the revoked step's transition factor is exact at the last
step (64/64) and on the i.i.d. subclass (1 152/1 152 per-model checks) and wrong on 320 of the 384 (path, j)
pairs — all of them interior steps under a Markov member. (vi) *Anytime-valid guarantee revocation.* The
e-process is a martingale under the guarantee (`E = 1` at each of 12 steps); revoking at `e_t ≥ 20`
anywhere in the horizon has false-revocation probability `23 633 / 2 097 152 ≈ 0.011 ≤ α` (Ville's
inequality, exact by enumeration of 4 096 outcome paths) with power `307/1 024 ≈ 0.30` at the alternative;
re-running a fixed-level exact binomial test at every step has false-revocation probability
`78 277 / 1 048 576 ≈ 0.075 > α` (power `151/256`, bought by invalidity). (vii) *The guarantee is a scoped
assumption, never a warrant.* An individual output resting on `g` alone is `⟦0, {g}⟧` and UNKNOWN on every
one of the 4 096 paths whatever the e-value says (KS-T21 / D3).

**Proof.** (i) enumeration; (ii) a flip sequence starts with a revocation and alternates, so `ρ` revocations
give at most `2ρ` flips and there are at most `T` transitions; the unbudgeted alternating path has `T`
flips. (iv) the predictive value is `1 − a` or `b` by the Markov property, so it ranges over the grid;
`a, b ∈ (0, 1)` makes every likelihood positive. (v) marginalisation is the definition of the posterior
without the observation; the divide-out equals it iff the transition out of `x_j` does not depend on `x_j`
(i.i.d.) or there is no transition out of it (last step). (vi) `E_null[LR_t] = 1` by construction;
`P(sup_t M_t ≥ 1/α) ≤ α` for a nonnegative martingale with `M₀ = 1` (Ville 1939); the per-step test has
level α *at each fixed t*, and the union over 12 stopping rules is larger. ∎

**Hostiles.** `mutant_frequency_as_warrant` (LIVE rate ≥ ⅔ over the ledger read as the atom's warrant) is
wrong about the **present** on the 6 paths with ≥ 4 LIVE steps that end DEAD (the honest reading of the
ledger is right on 64/64) and wrong about the **next** step with positive probability under every registered
model (`11/64` at `a = b = ½`) — caught. `mutant_rate_as_probability` (the empirical rate reported as "the
probability `a` is LIVE next" with no model) — caught by (iv): the number is a function of (path, M), and on
44 paths it is nobody's prediction. `mutant_divide_out` (Bayesian un-update by division) — caught on 320
pairs, exact only where (v) says so. `mutant_stepwise_fixed_level_revoke` — false revocation 0.075 > α,
caught. `mutant_evalue_promotes_output` (a low e-value read as exact truth of an output) — mints LIVE on 794
of 4 096 paths, caught by KS-T21. **No-alarm:** every registered model yields every marginal, predictive
value and reopening rate exactly (9/9); the honest anytime monitor stays under α.

**Status.** PROVED (finite) for the typed statements; EXACTLY_BOUNDED_IMPOSSIBILITY for "a bounded
reopening rate without a registered model or envelope" and for "a predictive probability as a function of
the observed path". PARENT_OWNED mathematics: finite Markov chains (Kemeny–Snell 1976), test martingales
and Ville's inequality (Ville 1939; Shafer–Vovk 2019; Ramdas–Grünwald–Vovk–Shafer 2023 game-theoretic
statistics), the SPRT likelihood ratio (Wald 1945), Bayesian updating. What is registered here is only the
typing: ledger liveness is exact and time-indexed; anything stochastic is CONDITIONAL_ON_MODEL with the
model id as a revocable assumption (FIELD distinction 1, truth warrant ≠ score; distinction 6, historical
replay ≠ present validity); a guarantee is revoked by an anytime-valid monitor and reopens its dependents
through the cone (FD-03), never touching an individual output's exactness. **Tightened:** FRONTIER's
"exact dependence semantics, revocation/update, scope/population identity, calibration drift" are met as
follows — dependence: the model id in the receipt; revocation: marginalisation (v); population identity:
the guarantee's scope (D3, unchanged); calibration drift: the e-process (vi). The graded half FRONTIER also
lists (imprecise probability, credal sets, Dempster–Shafer) is **not** entered: D3's score-outside-the-lattice
rule and F6/G6's measure reading remain the answer, and this batch adds no scalar-semiring claim.

## I2 · FDX-11 · epistemic bifurcation / obstruction: the boundary is a lattice fact, the obstruction is an evidence-invariant failure

**Objects.** Evidence ids `E = {e1, e2, e3, e4}`, authority bits `{s1, s2}`, three registrable nogoods
`{e1,e2}, {e2,e3}, {e1,e3}`; six atoms with antichain alternatives and a required authority bit:
`x1: {{e1}}`, `x2: {{e1},{e2}}`, `x3: {{e1,e2},{e3}}`, `x4: {{e2,e3}}`, `x5: {{e4}} (s2)`,
`c = x1 ⊗ x4: {{e1,e2,e3}}`. A *state* `s = (R, N, A)` is the revoked set, the registered nogoods and the
granted authority bits (16 × 8 × 4 = 512 states). The *commitment set* `C(s)` is the set of atoms with a
live alternative that survives the nogood filter and whose authority bit is granted. A *small change* is one
registered move: revoke or reinstate one id, add one nogood, grant or withdraw one bit (3 840 (state,
change) pairs). The *boundary* at `s` is the set of atoms flipped by some single change; the *jump* of a
change is `|C(s) Δ C(s')|`. A registered symmetric *conflict* `x3 ↔ x4` is an argumentation attack (Dung
1995). The obstruction fixture is batch-5 E3's: features `{1, a, b}` with `a ← e1`, `b ← e2`, targets `a`,
`XOR`, `AND` over the XOR-span; the *R-transition* adds the feature `ab`.

**Theorem.** (i) *Exact boundary characterisation* (3 840/3 840): the flip set of a single change is
**exactly** — revoke `e`: the committed atoms for which `e` is a *cut* of the live alternatives (belongs to
every one; batch-6 F1(i)); reinstate `e`: the uncommitted atoms with granted authority for which some
unfiltered alternative is dead by `e` alone (`W ∩ R = {e}`); add nogood `n`: the committed atoms whose every
live alternative contains `n`; withdraw / grant `b`: the atoms requiring `b` with a live alternative. All
2 524 flips on the fixture are explained by one of these four clauses; none is anything else. (ii)
*Jumps.* Histogram of jump sizes 0 / 1 / 2 / 3 / 4 / 5 = 2 136 / 1 116 / 396 / 160 / 24 / 8; an evidence or
nogood change flips at most 2 atoms here, an authority change up to 5 (withdrawing `s1` at the full state
flips `x1, x2, x3, x4, c` at once — the meet coordinate is discontinuous by design, FD-01). 504 of 512 states
lie on some boundary. (iii) *Sensitivity.* The commitment indicator of each atom is a monotone Boolean
function of the evidence coordinate (1 024 reinstatement checks), and its single-flip sensitivity at the
full state is `x1: 1, x2: 0, x3: 0, x4: 2, x5: 1, c: 3` — an atom with two disjoint alternatives (`x2`) sits
on no evidence boundary. (iv) *Argumentation.* With committed atoms as arguments and the conflict as a
symmetric attack, the C7 verdict policy (both UNKNOWN while both live) equals Dung's grounded extension on
all 512 states; on the 32 states where both conflict atoms are committed there are exactly two stable
extensions, each containing one of them, and every stable extension contains the grounded one; a single
revocation of one side's support resolves the conflict (32 states) — a bifurcation *by design*, not a defect.
(v) *Obstruction.* On the E3 fixture (3 targets × 4 evidence states): the certificate reads OBSTRUCTION
**iff** the target fails at the current state **and** at every evidence state of the registered
representation (no reinstatement helps) — 12/12; `AND` is OBSTRUCTION at all four states and flips at no
evidence neighbour (0), `XOR` and `a` are REINSTATE_FIRST wherever they fail (5 cases) and SUCCESS otherwise;
the R-transition (adding `ab`) reaches `AND`. Hence an obstruction is an atom on **no** E-boundary and on an
R-boundary: the certificate is the statement "this failure is invariant under every E-change inside the
registered class", which is what separates it from missing evidence (E-boundary), revoked support
(REINSTATE_FIRST, F4), budget (RESOURCE, E2) and search (INSUFFICIENT_EVIDENCE, E2).

**Proof.** (i) an atom is committed iff some alternative is live, unfiltered and authorised; a single
revocation kills exactly the alternatives containing the id, so the atom flips iff every live alternative
does (cut); a single reinstatement revives exactly the alternatives whose only dead id is that one; a
nogood removes the alternatives containing it; the authority clause is the meet. Enumeration confirms
there is no fifth case. (iii) monotonicity: reinstatement enlarges the live set of every alternative. (iv)
the grounded extension is the least fixed point of the defence operator; two arguments attacking each other
and attacked by nothing else are undefended, so neither is in it; a stable extension must attack the one it
excludes, hence contains the other. (v) enumeration; the span of `{1, a, b}` has even-weight tables only,
`AND` has odd weight (the E3 parity witness). ∎

**Hostiles.** `mutant_flip_is_mechanism_failure` (a jump of size ≥ 2 under one change raised as a defect)
alarms on 588 of 3 840 changes, every one of which is explained by clause (i) — caught (the honest report
names the cut / completing id / nogood / bit and raises nothing). `mutant_graded_continuity` (a graded
support score — live alternatives over unfiltered ones — reported "stable" when it moves by ≤ ½) masks
1 688 of the 2 524 flips: the discontinuity is in the lattice and a score hides it — caught.
`mutant_pick_a_stable_extension` (commit the first stable extension: a credulous choice) commits one of two
symmetric arguments on all 32 conflict states; the choice is not a function of the evidence — caught by the
grounded reading. `mutant_certify_on_boundary` (OBSTRUCTION whenever the target fails now) certifies 5 cases
that a single reinstatement solves — caught. **No-alarm:** `x2` at full evidence has sensitivity 0; `AND`
has zero evidence neighbours that succeed; with no conflict the grounded and the unique stable extension
coincide.

**Status.** PROVED (finite). PARENT_OWNED mathematics: sensitivity of monotone Boolean functions (the
cut / completion clauses are the coordinates on which the indicator is sensitive; Nisan–Szegedy 1994 for the
measure), ATMS label change under assumption retraction (de Kleer 1986), minimal hitting sets / cuts (Reiter
1987; batch-6 F1), argumentation semantics (Dung 1995: grounded ⊆ every stable), the E3 certificate (batch
5) and the registered-class ceiling (batch-7 G1). **Tightened:** FRONTIER asks for a certificate that
distinguishes "an actual expressive obstruction from missing evidence, revoked support, insufficient budget
or a bad search policy" — the distinguishing predicate is *E-invariance of the failure inside the registered
representation class*: missing evidence and revoked support are E-boundaries (a reinstatement or an
acquisition flips them), budget and search are E2 verdicts, and only the E-invariant failure moved by an
R-transition is an obstruction. A flip of the commitment set under a small change is never by itself
evidence of a mechanism failure; the only diagnostic content of a flip is the id that caused it.

## I3 · FDX-13 · self-model calibration under reflexive dependence: performative fixed points, the shadow as the counterfactual arm

**Objects.** A self-model predicts the operator's success rate `ŝ` on a grid of ninths `{0, ⅛, …, 1}`. A
router *adopts* the prediction: at or above a threshold `θ` every task of an epoch (4 easy, 4 hard) goes to
the operator; below `θ` only the easy ones do (hard tasks go to a fallback, not counted for the operator).
The operator succeeds on easy tasks at rate `r_A` and on hard tasks at rate `r_B`, `r_A, r_B ∈ {0, ¼, …, 1}`,
`θ ∈ {¼, ½, ¾}` (75 fixtures). The *realised* rate under adoption is `s(ŝ) = (r_A + r_B)/2` if `ŝ ≥ θ` else
`r_A`; the *counterfactual* (shadow) rate — every task on the operator, nothing reads `ŝ` — is
`m = (r_A + r_B)/2`. A prediction is *performatively stable* iff `ŝ = s(ŝ)`; *repeated retraining* is the
orbit `ŝ ↦ s(ŝ)`. A calibration receipt is PERFORMATIVE (`|ŝ − s(ŝ)| ≤ ⅛`) or COUNTERFACTUAL (`|ŝ − m| ≤ ⅛`).
Adaptive reuse: `k = 3` candidate self-predictors scored on one shared held-out set of `n = 3` fair-coin
outcomes each (true rate ½ for all); the best held-out score is reported for the selected one.

**Theorem.** (i) *Fixed points, closed form* (75/75): the stable predictions are exactly `{r_A if r_A < θ}
∪ {m if m ≥ θ}` — none on 9 fixtures, one on 59, two on 7 (bistability: `r_A = 0, r_B = ½, θ = ¼` has the
stable predictions `0` and `¼`, chosen by the starting point). (ii) *Orbits.* Repeated retraining converges
(594 of 675 orbits, in ≤ 2 steps, always to a fixed point of (i)) iff a fixed point exists in the regime
reached; on the 9 fixtures without one every orbit is period 2 (81) — no self-prediction is stable, while the
counterfactual rate `m` is a fixed number on all 75. A self-model that ignores the loop and predicts `m` is
wrong under adoption on 26 fixtures (`s(m) ≠ m`). (iii) *Scoring on caused outcomes.* On 42 of 675
(fixture, ŝ) cases the prediction is PERFORMATIVELY calibrated and COUNTERFACTUALLY miscalibrated (the
routing produced the outcomes that confirm it); on 46 cases the reverse; the two receipts are different
objects (215 vs 219 calibrated cases). (iv) *E4 tightened.* Held-out tasks disjoint from the proposer's dev
tasks (E4's clause) are still *performative* when the router that reads the prediction routes them; the
honest adopter scores the prediction on the shadow (E5), whose routing does not read it — the shadow *is*
the counterfactual arm. (v) *Adaptive reuse.* Over all 512 outcome tables the reported held-out score of the
selected predictor has expectation `47/64` against the true rate `½` (optimism `15/64`); a fresh held-out for
the selected predictor has expectation `½`. (vi) *Self-authority.* The prediction record has authority
`{self_model: 1}`, world_truth 0, commit 0; an output resting on it alone is `⟦0, {r}⟧`, UNKNOWN at every
predicted rate. Routing may read the prediction (a J0 feedback move, batch-4 D8); warrant and commit may not.

**Proof.** (i) `s` takes two values, `r_A` below `θ` and `m` at or above; a value is a fixed point iff it lies
in its own regime. (ii) the orbit enters one of the two values after one step and stays iff that value is a
fixed point; otherwise it alternates between the two, which is period 2 iff neither is a fixed point. (iii)
enumeration. (v) `E[max of k held-out scores] > ½` by the max of exchangeable non-degenerate variables;
exact value by enumeration. ∎

**Hostiles.** `mutant_score_on_caused_outcomes` — 42 self-fulfilling cases caught against the counterfactual
receipt. `mutant_reuse_heldout_selects_best` — optimism `15/64`, caught against the fresh held-out. A
self-model that predicts `m` with the loop unregistered — wrong on 26 fixtures, caught by the fixed-point
check. `mutant_prediction_as_warrant` (`ŝ ≥ ⅞ ⇒` the output is LIVE) — mints LIVE on 2 grid points, caught by
KS-T21. **No-alarm:** with the loop registered (router policy and rates known) the stable prediction is
computed exactly on all 66 fixtures that have one; with no reflexive loop (`θ > 1`, never adopted) the two
receipts coincide.

**Status.** PROVED (finite). PARENT_OWNED mathematics: performative prediction — performative stability vs
performative optimality, repeated risk minimisation and its convergence condition (Perdomo, Zrnic,
Mendler-Dünner, Hardt 2020); adaptive data analysis and the reuse of a holdout (Dwork, Feldman, Hardt,
Pitassi, Reingold, Roth 2015); self-fulfilling / performative forecasts (Dawid 1982 for sequential
calibration). Batch-5 E1 (no self-authority), E4 (pre-outcome prediction, disjointness) and E5 (shadow
non-interference) are the registered objects. **Tightened:** FRONTIER's "quantify what a self-model can
reliably infer about the machine's future performance when its own predictions affect routing" has the
exact answer *the performative fixed point, when the reflexive dependence is registered* (the router policy
and the rates are inputs), and *nothing stable* when it is not (period-2 witness); "separate observational
self-modeling from self-authority" is (vi) plus the receipt type: OBSERVATIONAL = shadow / counterfactual,
PERFORMATIVE = under adoption, and only the former is the E4 evidence for an adoption decision.

## I4 · FDX-15 · parent-product equivalence / residual theorem: when a measured residual is attributable to the declared difference

**Objects.** Twelve tasks: `F1–F4` factual in scope (licensed YES), `V1–V4` a lesson taught then revoked
(licensed: honour the revocation), `O1–O4` out of scope (licensed UNKNOWN; `O1, O2` world-true, `O3, O4`
world-false). An *arm* is a function of its *information channels* (`LESSONS`, `MANIFEST`, `MANIFEST_PARTIAL`
= `F1, F2` only, `U` = an unbound world channel) and of the *declared difference* `Δ` (typed revocation
machinery): with `Δ` the revocation is honoured on every `V` task; without it the parent's coarse per-domain
flag coincides with the right answer only where the lifetime's stream variation bit `v_i = 1`. Eight paired
lifetimes with distinct variation vectors; per-family lifetime scores; the pre-registered one-sided exact
sign test over the eight differences (`≥ 7/8` at α = 1/20, size `9/256`; batch-7 G8) with the
COLLAPSED_ONE_COIN flag (all eight differences identical); the batch-4 D1 discordant rule inside one
lifetime (never pooled, F2). The *ablation arm* is the OCM with `Δ` switched off; the *parent-plus-Δ* arm is
the parent with the typed interface added. **Attribution rule:** a measured residual is
`RESIDUAL_ATTRIBUTABLE_TO_DECLARED_DIFFERENCE` iff (1) the reference arm is outside the decision (F8), (2)
no unit is pooled (F2), (3) the registered rule rejects on independent lifetimes, (4) the ablation arm
equals the parent **unit for unit** on the matched channels (the executable matching certificate), (5) the
differences are not one coin (G8). Failing (4) is `RESIDUAL_CONFOUNDED_BY_UNMATCHED_INFORMATION`; failing
(5) is `RESIDUAL_ONE_COIN_FLAGGED`; failing (3) is `INCONCLUSIVE_UNDERPOWERED` with the exact power.

**Theorem.** (a) *A real residual.* Matched channels, `Δ` declared: the `V` differences are
`1, ¾, ¾, ½, ¾, ½, ½, ¼` (varying, all positive), `p = 1/256`, ablation arm ≡ parent on all 96 unit
outcomes, parent + Δ ≡ OCM — attributable. (b) *An artefact of unmatched information.* The parent lacks half
the manifest: the `F` family rejects `8/8` with identical differences `½` although `Δ` plays no role on `F`;
the ablation arm still beats the parent on 16 units — the residual is the channel's, and the rule says
CONFOUNDED (before the one-coin flag, which also holds). (c) *Undetectable at this n.* A residual present on
three lifetimes (one item each): differences `0, 0, 0, 0, 0, ¼, ¼, ¼`, `p = 1/8`, INCONCLUSIVE_UNDERPOWERED;
the exact power of the `≥ 7/8` rule at win probability `½ / 0.6 / 0.7 / 0.8 / 0.9` is
`9/256 / 0.106 / 0.255 / 0.503 / 0.813`; the minimum detectable win probability at power 0.8 on a 1/100 grid
is `0.90`. Inside one lifetime of four items the D1 rule is INCONCLUSIVE on all 15 discordant tables
(RESIDUAL_SUPPORTED needs 6 discordant pairs all won; PARENT_SUFFICIENT needs `n_d ≥ 76` at `p_d = ½`, D1) —
at `m = 8` the lifetime-level test is the only one with any size. (d) *Collapsed one coin.* A family whose
outcome is a deterministic function of the planted design rejects `8/8` with eight identical differences:
flagged, inferential weight one coin (size ½ under shared variation, G8(iv)). (e) *Pseudo-replication.* Three
orderings of one lifetime pooled as discordant pairs move `3–0` (`p = 1/8`) to `9–0` (`p = 1/512`) from zero
new information — refused (F2). (f) *The reference arm inside the decision.* An arm with `U` scores `0/4` on
`O` under licence grading (differences `+1`) and `4/4` under truth grading (differences `−1`): the verdict
flips with the grader (G7), and the ablation check also fails (`U` is unmatched) — refused (F8). (g)
*Equivalence on the fixture.* Parent + Δ ≡ OCM and OCM − Δ ≡ parent on every matched case (3/3): the whole
measured residual is `Δ`, and `Δ` is itself parent-owned machinery (ATMS revocation, batch-6 F1) — on the
fixture the field is a typing discipline over parent components with no further mathematical residual.

**Proof.** (a)–(f) exact binomial arithmetic and enumeration of the arm functions. (g) by construction: the
arm is a function of (channels, Δ), so adding Δ to the parent's channels *is* the OCM arm. This is the
*shape* of the equivalence theorem, not a proof of it for the real OCM: the general claim is stated below as
a CONJECTURE with the falsifier this fixture makes executable. ∎

**Hostiles.** `mutant_attribute_any_rejection_to_delta` (every rejection read as the declared difference at
work) — attributes (b) and (d): caught by the ablation clause and the collapse flag. The pooled orderings —
refused. The reference arm as parent — refused. **No-alarm:** matched arms on a family `Δ` does not touch tie
everywhere (TIES_ONLY); the real residual (a) passes all five clauses.

**Status.** PROVED (finite attribution theorem: the five clauses and the three failure modes with
witnesses). PARENT_SUFFICIENT on the fixture (parent + Δ ≡ OCM by construction). **CONJECTURE** for the
general parent-product equivalence FRONTIER asks for — "for every OCM mechanism there is a composition of
the registered parents plus the typed interface that is outcome-identical on matched channels", i.e.
`FORMALISM_USEFUL_NO_ARCHITECTURE_RESIDUAL` — with the falsifier *an OCM-minus-Δ arm that differs from the
parent product on a matched unit*. No finite fixture can promote it; the executable content is the
attribution rule. PARENT_OWNED statistics: matched-pair designs and ablation methodology (Fisher; Cochran
1965 on matching), the exact sign test and its power, batch-4 D1 (exact binomial / TOST), batch-6 F2
(pseudo-replication) and F8 (reference binding), batch-7 G7 (licence vs truth grading) and G8 (sizes,
family bound, one-coin collapse), the detectable-difference ceiling of ORION-V2 #354. **Tightened:**
FRONTIER's dichotomy — "a precise Machine-Epistemics residual the parent product lacks" **or** "a
simulation/equivalence theorem" — is not exclusive: a *measured* residual against the *strongest parent
buildable* can be real and attributable (a) while the *mathematical* residual is nil (g); the M12 V4
result is a claim of the first kind and says nothing about the second. "Matched information" is certifiable
only *by the ablation arm* (clause 4); declared-identical inputs are necessary and not sufficient (b).

## Consequences for the OCM build (read-only observations on `ORION-OCM-wt/m11-self`; nothing touched)

File states read on 2026-09-05/06. Each item names the runtime obligation the theorem makes concrete; none
is a claim about an M12 result.

* **I1 — guarantees need an anytime-valid revocation monitor; stochastic claims need a model id.**
  `src/ocm/kso/warrant.py::WarrantProfile.liveness` (line 169) is the exact ledger fact and has no
  stochastic coordinate — correct. The scoped guarantee is `src/ocm/operators/registry.py` (`kind =
  "OPERATOR_GUARANTEE"`, line 110; `docs/RUNTIME_LIFECYCLE_REVALIDATION_V2.md` row "Statistical output").
  `src/ocm/selfmodel/govern.py::monitor` (lines 492–507) triggers `target_regression` when
  `target_success < target_threshold` at **each step** of the window (line 497) and
  `prediction_miscalibration` when `|prediction_error| > tolerance` (line 505) — the fixed-level per-step
  shape of I1(vi), whose false-trigger probability grows with the window; obligation: an anytime-valid
  trigger (e-process against the guaranteed rate) or the per-step rule with its exact union size in the
  receipt. `src/ocm/runtime/ocm_runtime.py::admit_evidence` (line 222) has `derived_from` and `authority`
  slots but no place for a generating-model / exchangeability assumption id: a rate admitted as an
  OBSERVATION payload would be read as a fact; obligation: the model id enters as a `derived_from`
  assumption record (as `A_aff` does in batch-8 H3), so the claim is CONDITIONAL_ON_MODEL and dies with the
  model. `src/ocm/runtime/state.py::RuntimeState.apply` REVOKE/REINSTATE (lines 84–85) with replay
  (`EventStore.replay`, line 103) already implements I1(v): a posterior is recomputed from surviving
  observations, never divided out. `src/ocm/selfmodel/model.py::FailureRecord.frequency` (line 94) is inert
  for the alarm (E2/F3, `diagnose.py` line 44) and, by I1(iv), also not a probability.
* **I2 — the reopening report can carry the boundary; the certificate should carry E-invariance.**
  `src/ocm/kso/revocation.py::reopening_report` (line 188) already separates `reopen` (cone ∩ liveness
  changed) from `recheck` (an alternative survives) — the flip set of I2(i); a `boundary_report` per LIVE
  atom (its cut ids over `WarrantProfile.lower`, the single-flip sensitivity of I2(iii)) is computable from
  the same data and is a distance-to-flip receipt, never a defect signal. `src/ocm/kso/nogoods.py::
  NogoodSet.add` (line 64) and `register_constraint_nogood` (line 74) are the nogood-cover flips of I2(i),
  by design (MEG-16(iv)); `src/ocm/kso/types.py::Authority.meet` (line 143) and `runtime/solve.py::
  commitment_gate` (line 377) make the authority jumps of I2(ii) — discontinuous by FD-01, no graded
  coordinate exists (correct). `src/ocm/selfmodel/diagnose.py::ObstructionCertificate.valid` (lines 72–85)
  has the negative half (a DEAD attempt is not an obstruction, line 83; F4 cap in `diagnose_with_path`, line
  159); I2(v) gives the positive half: the certificate should record that the failure persists at every
  evidence state of the registered representation (the closure argument or the enumerated states), which is
  what licenses the R-transition. `src/ocm/kso/jump.py::_STRONG_TRIGGERS` (lines 34–46) contains no
  "commitment flipped" trigger — consistent with the mechanism-failure hostile.
* **I3 — the calibration receipt needs a distribution tag; the shadow is the counterfactual arm.**
  `src/ocm/selfmodel/govern.py::shadow_evaluate` (line 61) runs both artefacts on frozen suites that no
  routing reads — it is I3(iv)'s counterfactual arm and the right place for E4's `prediction_realised`
  (lines 156–159). `monitor` (line 492) scores `prediction_error` on the **live** post-adoption stream, where
  routing may read the adopted component's own outputs — a PERFORMATIVE receipt; obligation: tag each
  receipt PERFORMATIVE / COUNTERFACTUAL and admit only the latter as E4 evidence.
  `src/ocm/selfmodel/proposal.py::Prediction` (lines 44–55) declares `improve`, `may_regress`, `margin` but
  not which components read the predicted quantity; obligation: a reflexive-dependence field so the
  fixed-point check of I3(i) applies (and a NO_STABLE_SELF_PREDICTION terminal where none exists).
  `proposal.py::SelfChangeProposal.discriminator` (line 72, "pre-registered suite id") reused across
  proposals is the shared held-out of I3(v); the `Meter` (govern.py line 209) already counts proposals, so
  the reuse is chargeable as the max-of-k count.
* **I4 — V4 satisfies clauses 1, 2, 3, 5 and declares clause 4; V5 should ablate.**
  `docs/M12_V4_PAIRED_LIFETIMES_REPORT.md` §2: the primary family's differences vary (parent 0.593–0.611)
  and reject at size 9/256 (clause 3, 5); the six secondary rejections are flagged collapsed (I4(d)); §4
  keeps the reference arm beside the decision (`src/ocm/lifetime/reference.py::INFORMATION_BINDING`, line
  29; `m12_paired_eval.py` line 167) (clause 1); the unit is the lifetime (clause 2). Clause 4 is
  *declared*, not certified: `src/ocm/lifetime/machine.py::WholeSystemParent` (docstring lines 8–15, "the
  experimental difference is declared, not hidden") and `PersistentOCM.ablations = frozenset()` (line 92)
  exist, but `ARMS` (line 219) has no `ocm_minus_delta` arm and `m12_paired_eval.py` runs none. The honest
  label for V4 is RESIDUAL_ATTRIBUTION_DECLARED_NOT_ABLATED; obligation for V5: an ablation arm whose
  outcomes must equal the parent's unit for unit on the matched families (I4(b) is what it would catch).
  `docs/M12_V4R_REEVALUATION_NOTE.md`: the transfer family's CANNOT_CHECK_MATCHED_CASES (6 vs 4 cells) is
  I4(b) refused correctly; `src/ocm/lifetime/phases.py::phase_E(matched_cells=True)` (line 161) is the V5
  fix. `m12_paired_eval.py::sign_test_one_sided` (line 93) carries the collapsed flag (line 99) and the
  primary / secondary α (line 141). The within-lifetime rows (`ST.tost_equivalence(pair, 0.05)`, line 154)
  can never reach PARENT_SUFFICIENT with ≤ 12 items (I4(c): `n_d ≥ 76`); the V4 report's "PARENT_SUFFICIENT
  descriptively wherever no revision … repair needed" (§5) is a descriptive tie and should not carry the D1
  terminal's name. At `m = 8` the minimum detectable win probability at power 0.8 is 0.90; a V5 with more
  pre-registered families needs G8's Bonferroni `8/8`.

## Verification (billy-old, `~/ocm-verify/v2-b9`, Python 3.14.4)

```text
python research/machine-epistemics-theory/kso_field_frontier_batch9_exact.py   → exit 0, "status": "ALL_HOLD", "OPEN": [], wall 6.6 s
python -m pytest -q tests/unit/test_kso_field_frontier_batch9.py               → 9 passed
python -m pytest -q tests/unit/test_kso_self_model_prereqs_batch5.py tests/unit/test_kso_lifetime_prereqs_batch6.py \
  tests/unit/test_kso_lifetime_revision_boundaries.py tests/unit/test_kso_open_list_closure_batch7.py \
  tests/unit/test_kso_field_frontier_batch8.py tests/unit/test_kso_field_frontier_batch9.py           → 74 passed
md5 of the checker and the test identical on the Mac worktree and on billy-old
```

```text
I1  FDX-08  PROVED (finite) + EXACTLY_BOUNDED_IMPOSSIBILITY: ledger liveness exact; stochastic claims CONDITIONAL_ON_MODEL (model id revocable); reopening rate bounded iff model or envelope registered (min(2ρ,T)); predictive probability not a function of the path (spread ½, 44 paths match no model); Bayesian revocation = marginalisation (divide-out wrong on 320/384); anytime-valid guarantee revocation 0.011 ≤ α vs per-step 0.075; PARENT_OWNED (Markov, Ville/SPRT, Bayes); graded semiring not reopened
I2  FDX-11  PROVED (finite): boundary = cut ∪ completion ∪ nogood cover ∪ authority meet (3 840/3 840, 2 524 flips all explained); jumps ≤ 2 (evidence) / 5 (authority); sensitivity per atom; commitment set = grounded extension (512), two stable extensions on 32 conflict states; obstruction ⇔ E-invariant failure (12/12), moved only by R; PARENT_OWNED (monotone sensitivity, ATMS, Dung 1995, E3/G1)
I3  FDX-13  PROVED (finite): performative fixed points {rA if rA<θ} ∪ {m if m≥θ} (0/1/2 on 9/59/7 fixtures), orbits converge or period 2 (594/81); caused-outcome scoring self-fulfilling (42); shadow = counterfactual arm (E4 tightened); held-out reuse optimism 15/64; self-prediction never a warrant; PARENT_OWNED (performative prediction, adaptive data analysis, E1/E4/E5)
I4  FDX-15  PROVED (finite attribution theorem: five clauses, three failure modes) / PARENT_SUFFICIENT on the fixture (parent+Δ ≡ OCM) / CONJECTURE for the general equivalence (falsifier = ablation arm ≠ parent on a matched unit); real 1/256 attributable, unmatched confounded, undetectable 1/8 (min detectable p 0.90), collapsed flagged, pooled refused, reference refused; PARENT_OWNED (D1, F2, F8, G7, G8)
OPEN: none
CONJECTURE: FDX-15 general parent-product equivalence (FORMALISM_USEFUL_NO_ARCHITECTURE_RESIDUAL), falsifier stated
NOVELTY NOT_ESTABLISHED
```
