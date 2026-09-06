# KSO mechanised core — batch 12 (FDX-16, Lean 4 core semantics)

Date 2026-09-06. Twelfth one-day batch of the field-completion programme (ORION-V2 #353) over the
Machine Epistemics field frontier (`field_dynamics_v1/FRONTIER.md`). Scope: one frontier row —
FDX-16 mechanised core semantics — restricted to the KnowledgeSpace warrant core: three-valued
liveness with the Kleene order, warrant intervals `⟦L,U⟧`, the composition operators `⊕` / `⊗`, the
reopening cone under revocation, and the authority meet. The Lean statements are checked against the
OCM exact checkers, which are the finite oracle (`SzeChunYiu/ORION-OCM` `src/ocm/kso/{warrant,types,
revocation,checks}.py`, obligation ids from `docs/theorems/KSO_OBLIGATION_REGISTRY_V1.json`).

Deliverables: the Lake project `lean/kso_core/` (six modules, `KsoCore/*.lean`; no external
dependency, no Mathlib), this correspondence document, and
`tests/unit/test_kso_mechanised_core_batch12.py` (stdlib Python; needs no Lean; re-runs the finite
oracle side over the same fixtures and checks the Lean sources for the listed theorem names and for
the absence of `sorry`). Build and pytest ran on billy-laptop only; nothing ran on the Mac.

**Toolchain pin.** `lean-toolchain` = `leanprover/lean4:v4.14.0`; Lake 5.0.0 (`410fab7`); toolchain
directory `~/.elan/toolchains/leanprover--lean4---v4.14.0` on billy-laptop (x86_64 Linux). The
lakefile declares no `require`, so the build needs the pinned toolchain and nothing else.

**Build receipt** (`~/ocm-verify/v2-b12/build.log`, md5 `97791bf4ed413bc6cc4388a11e300935`, clean
build after `rm -rf .lake`; verbatim in §6): `Build completed successfully.` `rc=0`; axiom audit of
27 named theorems reports only `propext`, `Quot.sound`, `Classical.choice` (`audit_rc=0`); `grep -rn
sorry KsoCore KsoCore.lean` finds nothing (`grep_rc=1`). Pytest receipt in §6.

NO NOVELTY OR SUPERIORITY CLAIM. Every mechanised statement is a parent's (Kleene 1938 strong
three-valued logic; Pawlak 1982 lower/upper approximations; Belnap 1977; de Kleer 1986 ATMS labels;
Green–Karvounarakis–Tannen 2007 provenance semirings; Denning 1976 / Biba low-water-mark for the
authority lattice; Doyle 1979 / Acar 2005 for the closure) or an already-proved KS-T / T1 statement
of batches 1–10. The contribution is the machine-checked form, its exact correspondence to the OCM
code, and the recorded gaps. Mechanisation validates the formal statement; it does not prove that
the statement models the real OCM runtime or its environment (FRONTIER, FDX-16 caveat).

## 1. Representation: what the Lean objects are, and why the change of representative is lossless

| theory / OCM object | OCM representation (`warrant.py`, `types.py`) | Lean representation (`KsoCore`) |
|---|---|---|
| `Liveness` | `Enum {LIVE, DEAD, UNKNOWN}`; `kleene_and`, `kleene_or` | `inductive Liveness \| DEAD \| UNKNOWN \| LIVE`, constructor order = Kleene truth order; `kand`, `kor` with the same case order as the Python functions; `≤` via `rank` |
| warrant `W ⊆ E`, revocation `R ⊆ E` | `frozenset`; `frozenset` | `List E`; indicator `E → Bool` |
| profile `P ∈ 𝒜_E` | canonical antichain `canon(...)` (tuple of frozensets) | `List (List E)` — **no canonicalisation**; the algebra is stated on the liveness function `R ↦ live P R`, which is `f_P` of KS-T01 |
| `ℓ_R(P)` | `live(profile, revoked)` | `live P R : Bool` (recursive `any`/`all`) |
| `P ⊕ Q`, `P ⊗ Q` | `join` = `canon(P ∪ Q)`; `meet` = `canon({a ∪ b})`, `ZERO` if a factor is empty | `join P Q = P ++ Q`; `meet` = list of all `a ++ b` (empty if a factor is empty) |
| order `P ≤ Q ⇔ f_P ≤ f_Q` | `leq(lower, upper)` = every warrant of `lower` contains a warrant of `upper` | `Leq P Q := ∀ R, live P R → live Q R` (semantic); OCM's syntactic form is `SynLeq`; **`synLeq_iff_leq` proves the two coincide** (needs `DecidableEq E`; the witness revocation is the complement of a warrant) |
| equality of profiles | equality of canonical antichains | `Equiv P Q := ∀ R, live P R = live Q R` |
| `⟦L,U⟧` | `WarrantProfile(lower, upper)`; `__post_init__` raises unless `leq(lower, upper)` | `structure Interval` with proof field `wf : Leq lower upper`; `oplus` / `otimes` carry their well-formedness proofs (`join_mono`, `meet_mono`) |
| `λ_R⟦L,U⟧` | `WarrantProfile.liveness` | `lam I R := if live I.lower R then LIVE else if live I.upper R then UNKNOWN else DEAD` (same case order) |
| certified / partial / zero | `certified(p)`, `partial(p)`, `zero()` | `Interval.certified`, `Interval.partialIv`, `Interval.zero`, `Interval.one` |
| `Impact_D(C)` | `revocation.impact_cone`: iterate `X ∪ {u : ∃ h, T_h ∩ X ≠ ∅, u ∈ O_h}` to a fixed point | `reach dep n C`: the same step (`step dep C = C ++ succs dep C`) iterated `n` times (fuel) |
| `Authority` | named non-negative integer ranks, missing = 0, `meet` = coordinate-wise `min`, `__le__` coordinate-wise | `structure Authority K where rank : K → Nat` (missing = 0 built in); `meet`, `≤`, `meetAll` (fold), `dropCommit` (= `internal_authority`) |

Why the representative change is lossless: two lists are the same semiring element iff they have the
same liveness function, and every theorem below is stated on that function (or on `Equiv` / `Leq`),
so the canonical antichain never has to be computed. What this does *not* mechanise is that `canon`
returns a unique representative of each `Equiv` class and that `join`/`meet` of canonical inputs are
canonical (`is_antichain` in `check_semiring`) — that stays finitely checked (exhaustive at `n = 3`, 20
antichains, OCM `warrant.check_semiring`).

## 2. Correspondence table

Every row: the Lean theorem (module `KsoCore/…`), the statement, the theory identifier it mechanises,
the OCM checker that is its finite oracle, and the status. PROVED = closed in Lean with no `sorry` and
no non-standard axiom; TIGHTENED = proved in a form that differs from the prose statement, difference
stated; FINITE = only the OCM finite check exists (not mechanised here); CANNOT_CHECK = neither.

| Lean theorem | statement | KS-T / theory id | OCM finite oracle | status |
|---|---|---|---|---|
| `kand_comm`, `kand_assoc`, `kand_idem`, `kor_comm`, `kor_assoc`, `kor_idem`, `kand_absorb`, `kor_absorb`, `kand_kor_distrib` (Liveness) | `∧₃` / `∨₃` form a distributive lattice | KS-T21 (connectives) | `warrant.kleene_and` / `kleene_or` truth tables via `warrant.check_three_valued_reduction` | PROVED |
| `kand_eq_min`, `kor_eq_max`, `kand_le_left`, `kand_le_right`, `le_kor_left`, `le_kor_right` | `∧₃` is the meet and `∨₃` the join of the Kleene order DEAD < UNKNOWN < LIVE | batch-10 notation `≤₃` | same | PROVED |
| `kand_mono`, `kor_mono` | monotone in each argument over all 3⁴ cases | KS-T21 (c) shape | same | PROVED |
| `le_refl`, `le_trans`, `le_antisymm`, `DEAD_le`, `le_LIVE`, `LIVE_le_iff`, `le_DEAD_iff` | the Kleene order is a bounded total order with DEAD bottom, LIVE top | — | — | PROVED |
| `live_join`, `live_meet` (Profile) | `ℓ_R(P ⊕ Q) = ℓ_R(P) ∨ ℓ_R(Q)`, `ℓ_R(P ⊗ Q) = ℓ_R(P) ∧ ℓ_R(Q)` for all lists and all `R` | KS-T01 (monotone-Boolean-function reading); KS-T21 proof core | `warrant.check_semiring` (n = 3: 20 antichains, 400 pairs, 8 000 triples) | PROVED |
| `join_comm`, `join_assoc`, `join_idem`, `join_zero`, `meet_comm`, `meet_assoc`, `meet_idem`, `meet_one`, `meet_zero`, `meet_join_distrib` | commutative idempotent semiring laws **up to `Equiv`** | KS-T01 | `warrant.check_semiring` | TIGHTENED: stated on the liveness function, not on canonical antichains (see §3.1) |
| `meet_leq_left`, `meet_leq_right`, `leq_join_left`, `leq_join_right`, `zero_leq`, `leq_one` | `⊗` is the meet and `⊕` the join of the order; `0` bottom, `1` top | KS-T01 order; T10 (`U ⊗ 𝔽 ≤ U`) | `check_semiring`; batch-1 `check_t10_meg35_upper_certificates` | PROVED |
| `join_mono`, `meet_mono`, `join_mono_left`, `join_mono_right`, `meet_mono_left`, `meet_mono_right` | `⊕`, `⊗` monotone in each argument | Definition 1.3 well-definedness | `check_three_valued_reduction` (interval construction never raises) | PROVED |
| `avoids_iff`, `live_iff`, `live_eq_false_iff` | `ℓ_R(P) = 1 ⇔ ∃ W ∈ P, W ∩ R = ∅`; `= 0 ⇔` every warrant is hit | contract §3 definition | `warrant.live` | PROVED |
| `leq_of_synLeq`, `synLeq_of_leq`, `synLeq_iff_leq` | OCM `leq` (subset witnesses) ⇔ `f_P ≤ f_Q` | KS-T01 order; `WarrantProfile.__post_init__` | `warrant.leq` on the 20 × 20 profile pairs that build the 168 intervals of `check_three_valued_reduction` | PROVED (needs `DecidableEq E`) |
| `Interval.oplus`, `Interval.otimes` (definitions with proof fields) | interval well-formedness preserved by `⊕` / `⊗` | Definition 1.3 | `WarrantProfile.join` / `.meet` never raise `ValueError` on the 168² pairs | PROVED (by construction) |
| `lam_eq_LIVE_iff`, `lam_eq_DEAD_iff`, `lam_eq_UNKNOWN_iff` | the three cases are exclusive and exhaustive because `L ≤ U` | Definition 1.2 | `WarrantProfile.liveness` | PROVED |
| `lam_otimes` (Interval) | `λ_R(P ⊗ Q) = λ_R(P) ∧₃ λ_R(Q)` for all intervals, all `R` | **KS-T21** | `warrant.check_three_valued_reduction` (225 792 homomorphism checks) | PROVED |
| `lam_oplus` | `λ_R(P ⊕ Q) = λ_R(P) ∨₃ λ_R(Q)` | **KS-T21** | same | PROVED |
| `lam_certified_ne_UNKNOWN`, `lam_certified_eq` | KS-T21 (a): certified intervals are never UNKNOWN and agree with `ℓ_R` | KS-T21 (a) | same (160 reduction checks) | PROVED (certified = `Equiv lower upper`, weaker premise than `lower == upper`) |
| `lam_refines`, `lam_refines_le`, `lam_refines_DEAD` | KS-T21 (b): a refinement changes the verdict only from UNKNOWN | KS-T21 (b); T10 (MEG-35) | same (27 920 refinement checks); batch-1 `check_t10_meg35_upper_certificates` | PROVED |
| `oplus_comm`, `oplus_assoc`, `oplus_idem`, `otimes_comm`, `otimes_assoc`, `otimes_idem`, `otimes_oplus_distrib` | interval algebra up to `IEquiv` | Definition 1.3 | `check_three_valued_reduction` | TIGHTENED (up to `IEquiv`, §3.1) |
| `oplus_mono`, `otimes_mono`, `oplus_refines`, `otimes_refines`, `lam_mono_ILeq` | monotone in the component order and in the refinement order; `λ_R` monotone in the component order | KS-T21 (b), T10 | same | PROVED |
| `lam_otimesAll`, `lam_otimesAll_LIVE_iff`, `lam_otimesAll_LIVE_part`, `lam_otimesAll_DEAD_of_part` | `λ_R(⨂ parts)` is the Kleene fold; LIVE only if every exported part is LIVE; DEAD as soon as one is | **KS-T23** (warrant half, *no authority from abstraction*) | `checks.check_summary_no_authority` (`summary_live_dead_unknown = 3`) | PROVED |
| `avoids_antitone`, `live_antitone` | `ℓ_R` antitone in `R` | batch-10 J1 (i) | batch-10 checker (4 536 antitone checks) | PROVED |
| `lam_antitone` (Reopening) | **revoking more never revives**: `R ⊆ R' → λ_{R'} ≤₃ λ_R` | batch-10 J1 (i); KS-T22 premise | same | PROVED |
| `nonLive_mono`, `DEAD_mono` | non-LIVE and DEAD are upward-closed in `R` | same | same | PROVED |
| `lam_ne_LIVE_of_lower_hit`, `lam_ne_LIVE_of_common_evidence` | an atom all of whose exhibited supports are revoked is DEAD or UNKNOWN, never LIVE | KS-T02 shape (revoked tail disables) | `checks.check_firing` | PROVED |
| `lam_DEAD_of_upper_hit` | an atom all of whose possible supports are revoked is DEAD | Definition 1.2 | `WarrantProfile.liveness` | PROVED |
| `lam_zero_DEAD`, `lam_one_LIVE` | `⟦0,0⟧` is DEAD under every `R` (FEEDBACK atoms); `⟦1,1⟧` LIVE | **KS-T18** corollary | `checks.check_admission_channels` | PROVED |
| `reach_extensive`, `reach_mono`, `reach_congr` | the cone contains its seed and is monotone in it | KS-T09 / KS-T22 (4) shape | `checks.check_impact_and_reopening` (`least_closed_superset = 3`) | PROVED for the fuel-bounded closure (§3.2) |
| `reach_union` | `Impact_D(S₁ ∪ S₂) = Impact_D(S₁) ∪ Impact_D(S₂)` | batch-10 J1 (vii) | batch-10 checker (4 096 union checks) | PROVED |
| `reach_nil`, `cone_nil_of_unchanged` | an irrelevant revocation (`C = ∅`) reopens nothing | KS-T22 (3) | `check_impact_and_reopening` (`irrelevant_revocation_noop = 1`) | PROVED |
| `changed_sub_cone`, `unaffected_unchanged` | every liveness-changed atom is in the cone; an atom outside the cone did not change liveness | KS-T22 (1) first half, (2) first half | same (`cone_exact = 1`, `activation_change_within_reach = 1`) | PROVED |
| `deadSet_mono`, `reachDead_mono` | the non-LIVE seed grows with `R`, hence `Reach(D_R) ⊆ Reach(D_{R'})` for `R ⊆ R'`: **the reopening cone never shrinks under more revocation** | KS-T04b (ii) / contract §25 `Reach(D_R)` | `revocation.reach_of_dead` in `check_impact_and_reopening` | PROVED |
| `meet_le_left`, `meet_le_right`, `meet_never_raises` (Authority) | **the meet with any object authority never raises** any coordinate | T1 (i) (MEG-04); KS-T20 authority clause | batch-1 `check_t1_meg04_commit_bottom` (6 561 glb pairs); `checks.check_composition_law` | PROVED |
| `le_meet`, `meet_comm`, `meet_assoc`, `meet_idem`, `meet_mono` | greatest lower bound; lattice laws; monotone | T1 (i) | same | PROVED |
| `meetAll_le_base`, `meetAll_le_mem` | a fold over any list of factors is below every factor (no amplification) | KS-T20 (`A = A_b ∧ ⋀ A_i`) | `check_composition_law` (`rec.authority == Authority.of(src=1, ver=1)`) | PROVED |
| `dropCommit_le`, `dropCommit_commit`, `internal_commit_zero` | `internal_authority` is below its input and has `commit = 0` | T1 (ii) | `types.internal_authority`; batch-1 checker | PROVED |
| `InternalOnly.commit_zero`, `receipt_tail_cannot_lend_commit` | no chain of internal operations of any length produces `commit > 0`, even over receipt tails with `commit = 1` | T1 (iii) | batch-1 checker (receipt tails composed internally give 0) | PROVED (§3.3 on the operator-factor premise) |

Controls (all PROVED as positive refutations in `KsoCore/Mutants.lean`; the failing-`example`
descriptions are in §4): `kand_not_min_under_mutant_order`, `unknownAsDead_wrong`,
`unknownAsLive_wrong`, `meet_as_union_wrong`, `completeness_bit_does_not_compose`,
`interval_composes_where_bit_fails`, `homomorphism_fails_without_wf`, `authority_max_raises`,
`authority_max_mints_commit`, `shallow_cone_misses_deep_dependent`,
`nogood_breaks_unconditional_kleene`, `filterN_join`.

## 3. Tightened statements and recorded gaps

**3.1 Semiring laws up to `Equiv`, not on canonical antichains.** The prose KS-T01 is an equation
between canonical antichains (`join(a, b) == join(b, a)` in `check_semiring`). The Lean lists are not
canonical (`P ++ Q ≠ Q ++ P` as lists), so commutativity, associativity, idempotence, the unit/zero laws
and distributivity are proved as `Equiv` (identical liveness functions), which is the semiring equality
in the free-distributive-lattice reading. What the tightening loses: the claim that OCM's `canon` is a
normal form for `Equiv` (and hence that `==` on canonical antichains decides `Equiv`) is not mechanised;
`check_semiring` (n = 3, 20 antichains) is its finite check. Everything downstream (`lam`, the homomorphism, the cone)
depends only on the liveness function, so no downstream statement is weakened.

**3.2 The cone is fuel-bounded.** `reach dep n C` iterates the OCM step `n` times; OCM iterates to a
fixed point. Extensivity, monotonicity, union-distributivity and the empty-seed law are proved for every
`n`. The *least dependency-closed superset* characterisation (KS-T09 / KS-T22 (3)–(4): closure reached
at `n ≥ |V|`, containment in every closed superset) needs a pigeonhole argument on the finite vertex
list and is not mechanised; `check_impact_and_reopening` (`least_closed_superset = 3`, `cycle = 1`) is its
finite check. KS-T22's REOPEN / RECHECK / UNAFFECTED partition and its activation clause (KS-T04b (ii))
are likewise FINITE only (eight-atom witness).

**3.3 T1 (iii) needs the operator factor.** `InternalOnly.compose` composes tails *with an operator
factor whose `commit` is 0*, exactly the MEG-04 law; the proof uses only that factor
(`meetAll_le_base`), which is why the theorem holds "whatever the tails carry". Batch 1's recorded
limitation stands: `admission.compose` takes the meet over the tails only when `bridge_authority` is
`None`, which is the `mutant_compose_drops_operator_factor` shape; the Lean theorem does not cover that
call path because its premise is not met there.

**3.4 Certified = `Equiv`, not `==`.** `Interval.Certified I := Equiv I.lower I.upper` is weaker than
OCM's `lower == upper`, so `lam_certified_ne_UNKNOWN` covers strictly more intervals than the checker's
`reduction` loop. Nothing is lost in the other direction.

**3.5 Not mechanised in this batch** (all FINITE in OCM, none CANNOT_CHECK in the theory sense):
KS-T04c (prune–solve equivalence; needs the navigation matrix over `Fraction` and Banach uniqueness —
`checks.check_prune_equivalence`), KS-T24 (navigation is not truth — `check_navigation_is_not_truth`),
KS-T07b (lumpability ∧ warrant measurability — `check_quotient`), MEG-16B/C/E (post-filtered product,
its associativity and the conditional Kleene law under `N`-separability — foundation checker
`machine_epistemics_foundation_v1_check.py`; only MEG-16A and the refutation MEG-16-REFUTED-V0 are
mechanised), FRONTIER's *typed terminals* and *representation/revision commutation theorem* (FDX-16
lists them; they belong to `foundation_typed_lifecycle_v1` and `revision_consistency_v1` and were not
attempted here — OPEN for a later batch).

**3.6 CANNOT_CHECK.** That the Lean `Interval` models the runtime `WarrantProfile` *as used by the
solve loop* (gates, receipts, admission channels) is not a theorem of either side; the correspondence in
§1 is a reading of the source, checked by the pytest's re-implementation of the same finite fixtures,
not by executing OCM against Lean. Whether the OCM antichain universe `E` (hashable ids) satisfies
`DecidableEq` is assumed (it does for every registered id type, but is not verified by the build).

## 4. Planted mutants and how the Lean statements reject them

Each row names the mutant, the `example` that stops typechecking when the mutant definition is
substituted for the honest one (described, not left in the build), and the proved refutation that *is*
in the build (`KsoCore/Mutants.lean`).

| theorem (honest) | mutant | rejection when the mutant is substituted | proved refutation in the build |
|---|---|---|---|
| `kand_eq_min` / `kor_eq_max` | wrong Kleene order `UNKNOWN < DEAD < LIVE` (`mutantRank`) | `example : ∀ a b, kand a b = (if a ≤ b then a else b) := by cases a <;> cases b <;> decide` fails at `(DEAD, UNKNOWN)`: `decide` evaluates to `false` | `kand_not_min_under_mutant_order` |
| `kand_comm` etc. | `kand` with `UNKNOWN, _ => UNKNOWN` placed before `_, DEAD => DEAD` (UNKNOWN absorbing) | `example : kand UNKNOWN DEAD = DEAD := rfl` fails (`UNKNOWN ≠ DEAD` after reduction); `lam_otimes` then fails on the partial-times-dead case `P = ⟦0,1⟧, Q = ⟦{{e}},{{e}}⟧, R = {e}` | `completeness_bit_does_not_compose` uses the same data |
| `lam_otimes` | OCM `mutant_unknown_as_dead` (`liveness := LIVE if ℓ_R(L) else DEAD`) | the `simp_all` case `live lower = false, live upper = true` closes to `DEAD = UNKNOWN`, unprovable; `lam_eq_UNKNOWN_iff` becomes false | `unknownAsDead_wrong` (`⟦0,1⟧`, `R = ∅`) |
| `lam_otimes` | OCM `mutant_unknown_as_live` (uncertified absence read as LIVE) | with `if lower = upper then DEAD else LIVE` in the `else` branch, `lam_eq_LIVE_iff` fails (LIVE without a live lower warrant) and `lam_ne_LIVE_of_lower_hit` fails on `⟦0, {{e}}⟧, R = {e}` | `unknownAsLive_wrong` |
| `live_meet` | OCM `mutant_meet_as_union` (`⊗ := ⊕`) | `live_meet` becomes `live (join P Q) R = (live P R && live Q R)`, refuted by `cases` at `P = {{a}}, Q = {{b}}, R = {b}` (`true ≠ false`) | `meet_as_union_wrong` |
| `lam_otimes` (premise) | drop `Interval.wf` (a raw pair) | the case `live lower = true, live upper = false` is no longer closed by `hI`; goal `LIVE = kand LIVE UNKNOWN` i.e. `LIVE = UNKNOWN` remains — the **missing-premise control** | `homomorphism_fails_without_wf` |
| `lam_otimes` (representation) | completeness bit instead of an interval (§1.3 of the three-valued note) | `bitLam (bitOtimes P Q) R = kand (bitLam P R) (bitLam Q R)` is false at `P = ⟨(), false⟩, Q = ⟨{{2}}, true⟩, R = {2}` (`UNKNOWN ≠ DEAD`) — the **false-theorem control** | `completeness_bit_does_not_compose`, `interval_composes_where_bit_fails` |
| `meet_le_left`, `meetAll_le_mem` | OCM `mutant_authority_max` (coordinate-wise `max`) | `example : ∀ a b : Authority Unit, authorityMax a b ≤ a := fun a b k => Nat.max_le_left _ _` has no such lemma; `decide` on the witness `(0, 1)` gives `false` | `authority_max_raises`, `authority_max_mints_commit` (`commit = 1` minted) |
| `InternalOnly.commit_zero` | drop the operator factor (`mutant_compose_drops_operator_factor`: `meetAll` over tails only) | with `compose (tails) : InternalOnly (meetAll t₀ rest)`, the `omega` step has no `hop`; the theorem is false for a receipt tail with `commit = 1` | `receipt_tail_cannot_lend_commit` is exactly the statement that needs `hop` |
| `reach_extensive` / `changed_sub_cone` | OCM `mutant_impact_cone_direct_only` (one hop) | replacing `reach dep n` by `step dep` makes `shallow_cone_misses_deep_dependent`'s second conjunct the negation of `changed_sub_cone` on the chain `0 → 1 → 2` | `shallow_cone_misses_deep_dependent` |
| `lam_antitone` | a "revoke-wins" that *removes* an id from `R` (last-writer-wins flag of batch-10 `mutant_lww_revocation_bit`) | the premise `Subrev R R'` is not met; substituting `R' ⊆ R` flips the conclusion, refuted on `⟦{{e}},{{e}}⟧` | (covered by `lam_antitone` itself: the statement is direction-exact) |
| MEG-16 | the atlas's unconditional Kleene law under nogoods (MEG-16-REFUTED-V0) | `example : ∀ N P Q R, lamN N (meet P Q) R = kand (lamN N P R) (lamN N Q R)` fails at `N = {{a,b}}, P = {{a}}, Q = {{b}}` | `nogood_breaks_unconditional_kleene`; `filterN_join` is MEG-16A |

**Axiom / sorry leak control.** `Audit.lean` (`lake env lean Audit.lean`, not part of the library)
prints the axiom set of 27 theorems: only `propext`, `Quot.sound` and `Classical.choice` appear
(`Classical.byContradiction` is used in three proofs); no `sorryAx`, no custom axiom. `grep -rn sorry`
over the sources returns nothing (rc 1). The pytest repeats the `sorry` scan and the theorem-name
check without Lean.

## 5. Finite oracle re-run (pytest, stdlib, no Lean, no `ocm` import)

`tests/unit/test_kso_mechanised_core_batch12.py` re-implements the ~120 lines of exact arithmetic
(`canon`, `join`, `meet`, `leq`, `live`, `liveness`, `kleene_and/or`, `Authority.meet`, `impact_cone`)
and pins: the two 3 × 3 truth tables against the Lean case order; `kand`/`kor` = min/max of the Kleene
order and monotonicity over all 81 quadruples; at `n = 3`: 20 antichains, 168 intervals, 160 reduction
checks, 225 792 homomorphism checks per operator, 27 920 refinement checks, 4 536 antitone checks (the
batch-10 count); interval well-formedness of every `⊕` / `⊗` result (56 448 constructions); OCM syntactic
`leq` ⇔ semantic order on all 400 profile pairs (the `synLeq_iff_leq` oracle); the §1.3 counterexample; the
authority glb over `{0,1,2}³` pairs (729) with `max` caught; `internal_authority` `commit = 0` over
receipt tails; the eight-atom reopening witness (`cone = {a,b,c,d,e}`, cycle `{x,y}`, one-hop mutant
misses `c`); union-distributivity of the cone on every pair of subsets of the witness (256); and the
source checks (files exist, `lean-toolchain` pinned, lakefile has no `require`, every backticked name in
the §2 / §4 tables is a `theorem` or `def` in `KsoCore/*.lean`, no `sorry`, no `axiom`).

## 6. Receipts (verbatim)

`~/ocm-verify/v2-b12/build.log` on billy-laptop (md5 `97791bf4ed413bc6cc4388a11e300935`):

```text
== clean build 2026-09-06T04:35:45Z Lean (version 4.14.0, x86_64-unknown-linux-gnu, commit 410fab728470, Release) / Lake version 5.0.0-410fab7 (Lean version 4.14.0)
info: kso_core: no previous manifest, creating one from scratch
info: toolchain not updated; already up-to-date
✔ [2/9] Built KsoCore.Authority
✔ [3/9] Built KsoCore.Profile
✔ [4/9] Built KsoCore.Liveness
✔ [5/9] Built KsoCore.Interval
✔ [6/9] Built KsoCore.Reopening
✔ [7/9] Built KsoCore.Mutants
✔ [8/9] Built KsoCore
Build completed successfully.
rc=0
== axiom audit
'KsoCore.Liveness.kand_mono' does not depend on any axioms
'KsoCore.Liveness.kand_eq_min' does not depend on any axioms
'KsoCore.live_meet' depends on axioms: [propext]
'KsoCore.live_join' depends on axioms: [propext]
'KsoCore.synLeq_iff_leq' depends on axioms: [propext, Quot.sound]
'KsoCore.lam_otimes' depends on axioms: [propext]
'KsoCore.lam_oplus' depends on axioms: [propext]
'KsoCore.lam_certified_ne_UNKNOWN' depends on axioms: [propext]
'KsoCore.lam_refines' depends on axioms: [propext]
'KsoCore.lam_antitone' depends on axioms: [propext, Quot.sound]
'KsoCore.lam_ne_LIVE_of_lower_hit' depends on axioms: [propext, Classical.choice, Quot.sound]
'KsoCore.lam_DEAD_of_upper_hit' depends on axioms: [propext, Classical.choice, Quot.sound]
'KsoCore.lam_zero_DEAD' does not depend on any axioms
'KsoCore.reach_union' depends on axioms: [propext, Quot.sound]
'KsoCore.reachDead_mono' depends on axioms: [propext, Quot.sound]
'KsoCore.unaffected_unchanged' depends on axioms: [propext, Classical.choice, Quot.sound]
'KsoCore.cone_nil_of_unchanged' depends on axioms: [propext, Classical.choice, Quot.sound]
'KsoCore.lam_otimesAll_LIVE_iff' depends on axioms: [propext, Quot.sound]
'KsoCore.lam_otimesAll_DEAD_of_part' depends on axioms: [propext]
'KsoCore.Authority.le_meet' depends on axioms: [propext, Quot.sound]
'KsoCore.Authority.meetAll_le_mem' depends on axioms: [propext]
'KsoCore.Authority.InternalOnly.commit_zero' depends on axioms: [propext, Quot.sound]
'KsoCore.Mutants.completeness_bit_does_not_compose' does not depend on any axioms
'KsoCore.Mutants.homomorphism_fails_without_wf' does not depend on any axioms
'KsoCore.Mutants.authority_max_raises' does not depend on any axioms
'KsoCore.Mutants.nogood_breaks_unconditional_kleene' depends on axioms: [propext]
'KsoCore.Mutants.filterN_join' depends on axioms: [propext]
audit_rc=0
== sorry scan
grep_rc=1
```

Pytest (billy-laptop, Python 3.8.10, pytest 8.3.5, `python3 -m pytest -q
tests/unit/test_kso_mechanised_core_batch12.py -p no:cacheprovider`), appended to the same `build.log`
(final md5 `0927abd21e70636d23c4fc1d5b2cc289`; the md5 quoted above is the build-only prefix):

```text
== pytest 2026-09-06T04:41:45Z Python 3.8.10  … 5 failed, 11 passed (first run: my count fixture said 168 profiles; the Dedekind number at n = 3 is 20 — test and document corrected, no Lean change)
== pytest … (rerun after count fix)            … 1 failed, 15 passed (the Lean keyword `example` in prose was read as a theorem name — excluded)
== pytest 2026-09-06 … (final)
................                                                         [100%]
16 passed, 1 warning in 0.87s
rc=0
```

## 7. Consequences for the OCM build (read-only observations, no code changed)

* **M1 (§1, `synLeq_iff_leq`).** `WarrantProfile.__post_init__` checks the syntactic `leq`; the Lean
  proof shows this is exactly the semantic well-formedness `∀ R, ℓ_R(L) ⇒ ℓ_R(U)`, so the constructor's
  `ValueError` is the complete guard for Definition 1.1 — no second check is needed, and none should be
  weakened to `lower ⊆ upper` (that is strictly stronger than `leq`).
* **M2 (`lam_otimes`/`lam_oplus`).** `WarrantProfile.meet` / `.join` construct the composite and let
  `__post_init__` re-check the order; the Lean `join_mono` / `meet_mono` show the re-check can never
  fail on well-formed inputs, so a failure there is a caller-side corruption, not an algebra failure.
* **M3 (`InternalOnly.commit_zero`, §3.3).** The theorem's premise is the operator factor; batch 1's
  `admission.compose` limitation (bridge authority `None` ⇒ tails-only meet) remains the one call path
  the theorem does not cover. Obligation unchanged: default the bridge authority to the operator's.
* **M4 (`reach_union`, `reachDead_mono`).** `revocation.impact_cone` may be computed per delta and
  unioned (batch-10 H-obligations on batching) — the Lean statement is the licence for that
  refactor at the closure level; the fixed-point iteration count is not part of the licence (§3.2).
* **M5 (`lam_otimesAll_*`).** `abstraction.summarize`'s warrant rule is the fold `lam_otimesAll`; the
  majority mutant (`check_summary_no_authority`) is rejected by `lam_otimesAll_DEAD_of_part` at the
  first DEAD exported part, independent of how many parts are LIVE.

```text
Lean      kso_core  6 modules, 0 sorry, axioms ⊆ {propext, Quot.sound, Classical.choice}; lean4:v4.14.0 / Lake 5.0.0; billy-laptop rc=0
KS-T21    PROVED (lam_otimes, lam_oplus, lam_certified_ne_UNKNOWN, lam_refines)
KS-T01    PROVED up to Equiv (live_join, live_meet, semiring laws); canon normal form FINITE (check_semiring)
KS-T23    PROVED warrant half (lam_otimesAll_LIVE_iff, lam_otimesAll_DEAD_of_part); authority half = meetAll_le_mem
KS-T18    PROVED corollary (lam_zero_DEAD)
KS-T22    PROVED (1)/(2) liveness halves, (3) empty seed, cone monotone/union-distributive (fuel-bounded); least-closed-superset and activation clause FINITE
J1 (i)    PROVED (lam_antitone; revoking more never revives)
T1        PROVED (i)(ii)(iii) with the operator-factor premise (meet_le_left, le_meet, dropCommit_commit, InternalOnly.commit_zero)
MEG-16    REFUTED-V0 mechanised (nogood_breaks_unconditional_kleene); 16A PROVED (filterN_join); 16B/C/E FINITE
FINITE    KS-T04c, KS-T24, KS-T07b, KS-T22 partition, canon normal form, MEG-16B/C/E
OPEN      typed terminals; representation/revision commutation theorem (FDX-16 list items not attempted)
CANNOT_CHECK  Lean model ≡ runtime use of WarrantProfile; DecidableEq of the OCM id universe
NOVELTY   NOT_ESTABLISHED
```
