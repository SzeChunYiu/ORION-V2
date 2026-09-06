# Machine Epistemics field map V1 — the field as it stands after theory batches 1–11

Status: **theory batch 13 of the field-completion programme (ORION-V2 #353); consolidation only, no new
theorem; NOT sealed. NO NOVELTY OR SUPERIORITY CLAIM.** Date 2026-09-06.

This document is *derived*. Every table below that sits between `FIELD_MAP_GENERATED` markers, and the
summary block, is printed by `kso_field_map_v1_exact.py` from the batch documents, their exact checkers
(read with `ast`, never executed here), the sealed atlas (`ME_THEORY_GAP_ATLAS_V1.md`, read only) and its
addenda, the foundation registry, and a byte-pinned snapshot of the OCM obligation registries
(`OCM_OBLIGATION_REGISTRY_DERIVED_V1.json`, `existing_registry_snapshot`). No count in this document is
typed by hand: the checker fails when a generated region differs from what it renders
(`DOCUMENT_REGION_STALE`), and `tests/unit/test_kso_field_map_v1.py` runs that check. The prose sections
(§1, §8, §9) name the objects and the non-claims and read their counts from the block in §0.

Verification host: billy-old (`~/ocm-verify/v2-b13`, Python 3.14.4); nothing ran on the Mac. Receipts in §10.

## 0. Summary block (produced by the checker)

<!-- FIELD_MAP_GENERATED:summary BEGIN -->
```text
KSO FIELD MAP V1 — Machine Epistemics theory batches 1–11 (first version)
batches                                       11
theorems                                      77
theorems_by_batch                             1 11, 2 8, 3 8, 4 8, 5 11, 6 8, 7 9, 8 4, 9 4, 10 3, 11 3
theorems_by_status                            PROVED 48, PROVED (finite) 16, PARENT_OWNED 7, PARENT_SUFFICIENT 4, CONJECTURE 1, OPEN 1
parent_owned_or_sufficient_primary            11
parent_owned_or_sufficient_any_mention        33
exactly_bounded_impossibilities               22
impossibilities_by_batch                      7 7, 8 4, 9 5, 10 3, 11 3
open_items_current                            7
open_items_current_with_falsifier             0
open_items_current_flagged_no_executable_falsifier 7
open_halves_closed_by_a_later_batch           10
conjectures                                   3
conjectures_with_falsifier                    3
cannot_check_items                            6
kst_ids_cited                                 22
kst_ids_cited_in_registry                     21
kst_ids_cited_flagged                         KS-T14
dependency_edges_theorem_to_theorem           92
dependency_edges_explicit                     51
dependency_edges_bare                         41
registry_rows_in_snapshot                     127
registry_rows_linked_to_theorems              66
registry_rows_discharged                      52
registry_rows_left_open                       14
highest_existing_kst                          KS-T121
derived_obligations                           24
derived_existing_rows                         4
derived_new_rows                              20
derived_new_id_range                          KS-T122–KS-T141
derived_by_status                             OPEN 21, PROVED 3
atlas_sections_present                        A, B, C, D, F, G, H, I, J, K, L, M, N, O
atlas_sections_absent                         E
atlas_gaps_listed                             35
atlas_gaps_with_theorem                       35
foundation_registry_atlas_status_at_freeze    ADOPTED 1, OPEN 21, PROVED 14
inconsistencies_reported_non_fatal            14
batch12_slot                                  PRESENT (on main)
batch12_correspondence_rows                   35
batch12_rows_by_status                        PROVED 33, TIGHTENED 2
batch12_status_block_rows_by_status           CANNOT_CHECK 1, FINITE 1, OPEN 1, PROVED 7, REFUTED 1
batch12_lean_theorems_declared                157
batch12_lean_names_in_table                   113
batch12_lean_sorry                            0
batch12_kst_cited                             12
novelty                                       NOT_ESTABLISHED
```
<!-- FIELD_MAP_GENERATED:summary END -->

`theorems` counts every `## X<n> · …` section of the eleven batch documents (batch 5's `R1–R3` range
heading expands to three). `primary status` is the first vocabulary token of the theorem's status line
(the batch document's final status block for batches 1 and 5–11; the atlas status tables §F–§H for batches
2–4, whose documents carry no status block); `statuses mentioned` lists every vocabulary token the line
contains, so a `PROVED (finite) + EXACTLY_BOUNDED_IMPOSSIBILITY` row is counted once under `PROVED (finite)`
and once in the impossibility list. The vocabulary is exactly `PROVED / PROVED (finite) /
FINITE_CALIBRATION / PARENT_OWNED / PARENT_SUFFICIENT / EXACTLY_BOUNDED_IMPOSSIBILITY / CONJECTURE / OPEN /
CANNOT_CHECK`; `PARENT_HEAVY` (batch 10 J2) is read as its stated companion `PARENT_SUFFICIENT`.

## 1. The object

The field's one object is the **KnowledgeSpace** (`KnowledgeSpace.v1`, OCM `src/ocm/kso/{warrant, types,
space, navigation, revocation, admission, abstraction, jump, resources, nogoods}.py`; contract
`research/orion-machine/theory/KSO_SUBSTRATE_CONTRACT_V1.md`, obligation ids in
`docs/theorems/KSO_OBLIGATION_REGISTRY_V1.json`). Its coordinates, with the document that defines each and
the batch theorems that fix its laws:

| coordinate | definition | defining document | laws (theorem ids in §2) |
|---|---|---|---|
| **warrant profile** `P ∈ 𝒜_E` | antichain of minimal supports over the evidence universe `E`; `P ⊕ Q = Min(P ∪ Q)` (alternatives), `P ⊗ Q = Min{a ∪ b}` (conjunction), `0 = ∅`, `1 = {∅}` — the provenance-semiring order | `KSO_THREE_VALUED_WARRANT_AND_REOPENING_V1.md` §1 (KS-T01, KS-T21); OCM `warrant.py` | T9/T11 (dependence, MEG-01/31), B2 (per-input VSW, MEG-12), C5 (procedure algebra, MEG-10), F6/G6/D3 (graded and measure readings, MEG-02) |
| **warrant interval** `⟦L,U⟧`, `L ≤ U` | lower = exhibited support, upper = possible support; certified profile `L = U`; partial profile `U = 1` | same, §1.1–1.3; KS-T21 | T10 (upper-profile certificates are refinements, MEG-35), C2 (renderer cannot mint support, MEG-25) |
| **three-valued liveness** `λ_R(⟦L,U⟧) ∈ {LIVE, UNKNOWN, DEAD}` under a revocation set `R` | exact Kleene homomorphism from `(⊕, ⊗)` to `(∨₃, ∧₃)`; refinement moves UNKNOWN → LIVE / DEAD only (KS-T21(c)); revoking more never revives (J1 (i)) | KS-T21 (same note); MEG-16 for the nogood-lifted form | T3 (feedback never warrant, MEG-08 / KS-T18), T6 (candidate warrant and evidence-driven collapse, MEG-26), C7 / MEG-16 (contradiction policy) |
| **nogoods** `𝒩 ⊆ 2^E` | registered inconsistent assumption sets; `filter_𝒩` on both sides; post-product filtering mandatory; `CONTRADICTED` is a composition terminal, not a fourth value | `MEG16_NOGOOD_ALGEBRA_V1.md` (MEG-16A–E, the atlas' unconditional Kleene claim refuted and preserved) | C7 (resolution policy), I2 (nogood cover is one of the four flip families of the commitment set) |
| **reopening cone** `Impact_D(X)` | least dependency-closed superset; revocation delta reported as REOPEN / RECHECK / UNAFFECTED | KS-T22 (same note), KS-T09; OCM `revocation.py` | T5 (shared evidence across fibres, MEG-22), B5 (scope / epoch / supersession as revocation families, MEG-03), B6 (repair after REOPEN, MEG-17), E6 (adoption rollback = revoke the stamp), J1 (∪-distributive; batched cones) |
| **authority meet** `A ∧ B` (coordinate-wise min over `{world_truth, speaker, task_contract, commit, …}`) | composition never raises a coordinate; internal operators carry `commit = 0`; import authority `drop_commit(A_sender ∧ cap)` | T1 (MEG-04), KS-T20 (no amplification) in the KSO registry; `types.py::Authority.meet` | B1 (discourse-state warrant, MEG-05), T7/E1 (no self-authority, MEG-29), J1/J2 (import and provider ceilings) |
| **scope / epoch** `Scope.covers(context, at)` | an epoch-bounded scope is never read as current on context alone; current validity needs every dependency root monitored | B5 (MEG-03); H1 (FDX-01); OCM `types.py::Scope`; derived obligation KS-T118 | H1, K3 (revocation mid-emission) |
| **navigation** `a^* = α s + (1−α) Pᵀ a^*` on the gated substochastic matrix | unique fixed point (KS-T05); prune–solve equivalence (KS-T04c); navigation is not truth (KS-T24) | KS-T04c / KS-T24 (same note); OCM `navigation.py` | T2 (budget bracket, MEG-06), D4/G2 (surprise no-drop and per-source normalisation, MEG-07), D7 (multiscale coherence, MEG-09) |
| **typed terminals** `FOUND / GAP_NOT_FOUND / OBSTRUCTION_WITNESSED / CANNOT_CHECK` | four-valued outcome discipline; `CANNOT_CHECK` absorbing, never a pass | KS-T19 (KSO registry); C4 (MEG-11 small-step semantics) | C4, E2/E3/F3/F4 (diagnosis and obstruction certificates), I2 (obstruction = evidence-invariant failure) |
| **certificates and statistical warrant** | a score is outside the lattice; a coverage receipt is a scoped procedure-level claim; individual truth needs a certified profile | `MEG02_STATISTICAL_WARRANT_ACTIONABILITY_V1.md` (MEG-02A–E); `MACHINE_EPISTEMICS_FOUNDATION_V1.md` (MEG-36 certificate identity) | D3, F6, G6, I1 (stochastic claims CONDITIONAL_ON_MODEL) |
| **resources / meter** `m ∈ ℕ^d`, budgets `B` | every mutation metered; strictly positive charge; well-founded termination | KS-S7, KS-R1 (KSO registry) | T8 (no livelock, MEG-30), E7 (metered proposals) |

The foundation registry (`MACHINE_EPISTEMICS_FOUNDATION_V1.json`, `FROZEN_CANDIDATE` on #319) types the
twenty primitives FND-P01…P20 the OCM depends on and carries the MEG-01…36 map *as it stood at the freeze*;
§6 and §9 record that the sealed map is behind the theorems. The mechanised form of the core (Kleene order,
intervals, `⊕`/`⊗`, reopening cone, authority meet) is batch 12 (`KSO_MECHANISED_CORE_BATCH12_V1.md`,
`lean/kso_core/`, merged as #367); the checker fills this slot from that document's correspondence table and
final status block and from the Lean sources (theorem names verified against the declarations, `sorry`
counted), in batch 12's own status vocabulary — it is not added to the batches 1–11 counts above:

<!-- FIELD_MAP_GENERATED:batch12 BEGIN -->
Batch 12 (`KSO_MECHANISED_CORE_BATCH12_V1.md`, sha256 `5f9301577653`; Lake project `lean/kso_core/`, modules `Authority.lean`, `Interval.lean`, `Liveness.lean`, `Mutants.lean`, `Profile.lean`, `Reopening.lean`) is on main. Lean theorems / lemmas declared: 157; names in the correspondence table: 113 (missing from the sources: none); `sorry` occurrences: 0; KS-T ids cited: KS-T01, KS-T02, KS-T04b, KS-T04c, KS-T07b, KS-T09, KS-T18, KS-T20, KS-T21, KS-T22, KS-T23, KS-T24. Status vocabulary is batch 12's own: PROVED (closed in Lean, no `sorry`, standard axioms), TIGHTENED (proved in a form that differs from the prose statement), FINITE (only the OCM finite check exists), CANNOT_CHECK, OPEN, REFUTED (a mutant refuted by a proved witness).

| Lean theorems (module) | statement | KS-T / theory id | OCM finite oracle | status |
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
| `Interval.oplus`, `Interval.otimes` | interval well-formedness preserved by `⊕` / `⊗` | Definition 1.3 | `WarrantProfile.join` / `.meet` never raise `ValueError` on the 168² pairs | PROVED (by construction) |
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

Final status block of the batch-12 document, row by row:

| row | status | statement |
|---|---|---|
| KS-T21 | PROVED | PROVED (lam_otimes, lam_oplus, lam_certified_ne_UNKNOWN, lam_refines) |
| KS-T01 | PROVED | PROVED up to Equiv (live_join, live_meet, semiring laws); canon normal form FINITE (check_semiring) |
| KS-T23 | PROVED | PROVED warrant half (lam_otimesAll_LIVE_iff, lam_otimesAll_DEAD_of_part); authority half = meetAll_le_mem |
| KS-T18 | PROVED | PROVED corollary (lam_zero_DEAD) |
| KS-T22 | PROVED | PROVED (1)/(2) liveness halves, (3) empty seed, cone monotone/union-distributive (fuel-bounded); least-closed-superset and activation clause FINITE |
| J1 (i) | PROVED | PROVED (lam_antitone; revoking more never revives) |
| T1 | PROVED | PROVED (i)(ii)(iii) with the operator-factor premise (meet_le_left, le_meet, dropCommit_commit, InternalOnly.commit_zero) |
| MEG-16 | REFUTED | REFUTED-V0 mechanised (nogood_breaks_unconditional_kleene); 16A PROVED (filterN_join); 16B/C/E FINITE |
| FINITE | FINITE | KS-T04c, KS-T24, KS-T07b, KS-T22 partition, canon normal form, MEG-16B/C/E |
| OPEN | OPEN | typed terminals; representation/revision commutation theorem (FDX-16 list items not attempted) |
| CANNOT_CHECK | CANNOT_CHECK | Lean model ≡ runtime use of WarrantProfile; DecidableEq of the OCM id universe |
<!-- FIELD_MAP_GENERATED:batch12 END -->

## 2. Every theorem, batches 1–11

Identifier, the atlas / frontier / contract id it is filed under, its one-line statement (the section
heading of the batch document), primary status, every status token its status line mentions, the checker
function (exactly one `check_<id>_*` per theorem in the batch's exact checker, verified by name), and the
parent as the section states it (the sentence after `Parent:`, else the `PARENT_OWNED (…)` /
`PARENT_SUFFICIENT (…)` parenthetical of the status line).

<!-- FIELD_MAP_GENERATED:theorems BEGIN -->
| batch | id | filed under | one-line statement (section heading) | primary status | statuses mentioned | checker function | parent |
|---|---|---|---|---|---|---|---|
| 1 | T1 | MEG-04 | commit authority is a bottom for internal composition | PROVED | PROVED | `check_t1_meg04_commit_bottom` | Biba low-water-mark (verified), Denning 1976 (verified); parents table row C(b) |
| 1 | T2 | MEG-06 | budget bracket for the restart iteration | PROVED | PROVED | `check_t2_meg06_budget_bracket` | Banach/Neumann (verified) |
| 1 | T3 | MEG-08 | feedback updates behaviour, never warrant | PROVED | PROVED | `check_t3_meg08_feedback_not_warrant` | TMS premise/assumption distinction (verified); ACT-R base-level learning as the weight-learning parent (Anderson 1993, verified in the F7 rows) |
| 1 | T4 | MEG-18 | Jump rollback is revoke-plus-quarantine | PROVED | PROVED | `check_t4_meg18_jump_rollback` | ATMS context switching (verified) |
| 1 | T5 | MEG-22 | shared evidence across fibres and transfer maps | PROVED | PROVED | `check_t5_meg22_shared_evidence` | ATMS composition (verified); KS-T09/T22 (PROVED) |
| 1 | T6 | MEG-26 | candidate warrant, ambiguity set, evidence-driven collapse | PROVED | PROVED | `check_t6_meg26_candidate_warrant` | KS-T20/T21 (PROVED) |
| 1 | T7 | MEG-29 | no self-authority | PROVED | PROVED | `check_t7_meg29_no_self_authority` | Gödel machine (Schmidhuber, verified in the parents table), reference monitor (Saltzer–Schroeder 1975, verified) |
| 1 | T8 | MEG-30 | no livelock, snapshot consistency | PROVED | PROVED | `check_t8_meg30_no_livelock` | Floyd well-founded termination (verified), Härder–Reuter ACID (verified); snapshot isolation is listed as candidate in the atlas and is used only as a name |
| 1 | T9 | MEG-31 | the certified-information unit | PROVED | PROVED | `check_t9_meg31_information_unit` | Hartley/Rényi `H_0` (Theorem A of lane 200, PARENT_OWNED); version spaces (Mitchell 1982, verified) |
| 1 | T10 | MEG-35 | upper-profile certificates are refinements | PROVED | PROVED | `check_t10_meg35_upper_certificates` | Pawlak 1982 lower/upper approximations (verified) |
| 1 | T11 | MEG-01 | evidence dependence: derived evidence flattens exactly | PROVED | PROVED | `check_t11_meg01_evidence_dependence` | ATMS assumptions vs derived nodes (de Kleer 1986, verified in the parents table); provenance semirings (verified) |
| 2 | B1 | MEG-05 | discourse-state warrant (no laundering) | PROVED | PROVED | `check_b1_meg05_discourse_state` | ATMS assumption vs. justified nodes (de Kleer 1986) and the commitment-store view of dialogue (Hamblin 1970, Walton–Krabbe 1995) — PARENT_OWNED for the objects; the authority-bottom law is KS-T20's corollary |
| 2 | B2 | MEG-12 | per-input version-space warrant | PROVED | PROVED | `check_b2_meg12_per_input_vsw` | Mitchell 1982 version spaces (PARENT_OWNED for VS); the per-input warrant and its reopening law are new statements over KS-T21/T22 |
| 2 | B3 | MEG-13 | gap-learning soundness on a finite class | PROVED (finite) | PROVED (finite) | `check_b3_meg13_gap_learning_soundness` | (no parent sentence in section; see status line) |
| 2 | B4 | MEG-24 | canonical meaning graph | PROVED | PROVED, PARENT_OWNED | `check_b4_meg24_canonical_meaning_graph` | canonical labelling (McKay–Piperno 2014) and the WL-1 limit (Cai–Fürer–Immerman 1992) — PARENT_OWNED; the bounded-exact-else-CANNOT_CHECK discipline is the OCM rule |
| 2 | B5 | MEG-03 | scope / epoch / supersession as revocation families | PROVED | PROVED | `check_b5_meg03_scope_epoch_supersession` | bitemporal validity (Snodgrass 1999) for epochs — candidate parent, cited not verified here; the reopening law is KS-T22 |
| 2 | B6 | MEG-17 | repair after REOPEN | PROVED | PROVED, PARENT_OWNED | `check_b6_meg17_repair_after_reopen` | DRed / Backward-Forward incremental maintenance (Gupta–Mumick–Subrahmanian 1993; Motik et al. 2019) — PARENT_OWNED for the bound; reinstate-exact vs relearn-new-id is the OCM lifecycle rule (KS-T31) |
| 2 | B7 | MEG-19 | consolidation locality (the provable half of KS-T12) | PROVED | PROVED, OPEN | `check_b7_meg19_consolidation_locality` | the improvement half of KS-T12 remains OPEN |
| 2 | B8 | MEG-28 | Jump preservation as a DPO rewrite | PROVED | PROVED, PARENT_OWNED, OPEN | `check_b8_meg28_dpo_jump_preservation` | DPO graph transformation (Ehrig et al. 2006) — PARENT_OWNED for preservation; the OCM contribution is the M4 fixture binding |
| 3 | C1 | MEG-33 | epistemic action value over intervals (clarification as an information action) | PROVED | PROVED, PARENT_OWNED | `check_c1_meg33_epistemic_action_value` | Howard 1966 value of information (verified), Rainforth et al. 2024 BED (verified) — PARENT_OWNED for the objective; the three-valued asymmetry (iv) is WLL-5/KS-T21's corollary |
| 3 | C2 | MEG-25 | external commitment / codec gate (the renderer cannot mint support) | PROVED (finite) | PROVED (finite) | `check_c2_meg25_commitment_gate` | object-capability confinement and closed-under-shown codecs (the atlas F10 rows, verified) for the capability half; Goguen–Meseguer noninterference (candidate, unverified) — the theorem here is the finite semantic half,  |
| 3 | C3 | MEG-27 | prefix commitment and bounded-lookahead satisfiability | PROVED (finite) | PROVED (finite), OPEN | `check_c3_meg27_prefix_commitment` | incremental sentence planning (Cho & Boland 2025, listed in `LANGUAGE_PARENT_RESEARCH_V0.md`, unverified); lookahead in constraint satisfaction (candidate) |
| 3 | C4 | MEG-11 | small-step operational semantics of the solve pipeline | PROVED | PROVED, PARENT_OWNED | `check_c4_meg11_pipeline_semantics` | Wright–Felleisen 1994 syntactic type soundness (verified) for the preservation/progress shape; Bruns–Godefroid 1999 three-valued model checking (verified) for UNKNOWN as "cannot check" |
| 3 | C5 | MEG-10 | procedure-algebra warrant laws | PROVED | PROVED | `check_c5_meg10_procedure_algebra_laws` | KAT (Kozen 1997, verified), provenance semirings (Green et al. 2007, verified); KS-T26 (`ocm.kso.procedures`) already covers L4–L5's core; C5 adds L1–L3, the meter law and the ALT/IF distinction |
| 3 | C6 | MEG-15 | discriminating-interaction certificate | PROVED (finite) | PROVED (finite) | `check_c6_meg15_discriminating_interaction` | KWIK / verifiable reward vs preference feedback — no verified formal parent; `KSO_CORE_PARENTS_V1.md` row 4 ("reward ≠ evidence") is used as an axiom; version spaces (Mitchell 1982, PARENT_OWNED) |
| 3 | C7 | MEG-16 | contradiction resolution policy over nogood-lifted intervals | PROVED | PROVED | `check_c7_meg16_contradiction_policy` | ATMS nogoods (de Kleer 1986, verified); the verdict policy is the OCM rule that KS-T25 left open ("resolution policy") |
| 3 | C8 | MEG-21 | non-quotient representation lifts | PROVED | PROVED | `check_c8_meg21_representation_lifts` | Abadi–Lamport 1991 refinement mappings / conservative extension (candidate, unverified here); DPO preservation is B8 |
| 4 | D1 | MEG-32 | adopt-not-invent: PARENT_SUFFICIENT / RESIDUAL_SUPPORTED as pre-registered exact tests | PARENT_OWNED | PARENT_OWNED | `check_d1_meg32_equivalence_rules` | exact binomial / McNemar 1947 (classic) and TOST (Schuirmann 1987; candidate, unverified) — PARENT_OWNED; nothing here is a theorem of the OCM, it is the adoption the atlas asked for, made executable |
| 4 | D2 | MEG-14 | per-channel acquisition bounds on the registered finite classes (a table with falsifiers) | PARENT_OWNED | PARENT_OWNED | `check_d2_meg14_channel_bounds` | PARENT_OWNED (no new theorem) |
| 4 | D3 | MEG-02 (graded half) | statistical operator outputs enter as ⟦0,U⟧ with a score outside the lattice | PROVED | PROVED, PARENT_OWNED, OPEN | `check_d3_meg02_graded_operator_warrant` | selective classification (Chow 1970, verified) and split conformal prediction (Vovk et al.; candidate, unverified) for the coverage identity — PARENT_OWNED |
| 4 | D4 | MEG-07 | no-drop guarantee for the surprise functional under fan-out | PROVED | PROVED, OPEN | `check_d4_meg07_surprise_no_drop` | personalised PageRank contribution vectors (Andersen–Chung–Lang 2006, verified), IDF (verified) — PARENT_OWNED for the objects; (iii)–(iv) are the OCM rule with its falsifier |
| 4 | D5 | MEG-20 | sufficiency certificate content | PROVED (finite) | PROVED (finite), PARENT_OWNED | `check_d5_meg20_sufficiency_certificate` | Kemeny–Snell 1976 (verified) and KS-T07b (PROVED at M1); this note fixes the *content* of the certificate `proof_ref` must point to |
| 4 | D6 | MEG-34 | identifiability of a construction inventory up to lifecycle equivalence ≡_L | PROVED | PROVED, OPEN | `check_d6_meg34_inventory_identifiability` | Gold 1967 / Angluin 1988 (classic), version spaces (Mitchell 1982) — PARENT_OWNED for identification; ≡_L is B2's per-input warrant lifted to signatures |
| 4 | D7 | MEG-09 | multiscale navigation coherence on a two-level fixture | PROVED | PROVED | `check_d7_meg09_multiscale_coherence` | Kemeny–Snell (verified); multilevel PPR / coarsening (candidate, unverified) — PARENT_OWNED for the walk; the outcome-coherence rule is the OCM's four-valued discipline (KS-T19) |
| 4 | D8 | MEG-23 | organisation search admissibility | PROVED | PROVED, PARENT_OWNED | `check_d8_meg23_organisation_admissibility` | DPO/adhesive rewriting (Lack–Sobociński 2005, verified), Kemeny–Snell (verified), multi-objective dominance — PARENT_OWNED; the admissibility predicate is the OCM's M8 contract |
| 5 | E1 | MEG-29 (extension of batch-1 T7) | the self-model fibre carries no self-authority | PROVED | PROVED | `check_e1_meg29_self_model_fibre` | reference monitor / Biba low-water-mark (verified), Gödel machine (Schmidhuber, verified) for "proof outside the proposer"; batch-1 T1/T5/T7 (PROVED) |
| 5 | E2 | M11 §3 | diagnostic-layer soundness on a finite trace grammar | PROVED | PROVED | `check_e2_m11_diagnostic_layer_soundness` | fault localisation by ablation / delta debugging (Zeller 2002; candidate, unverified); KS-T19's four-valued discipline (OBSTRUCTION only under a ceiling) is the rule — PARENT_OWNED for the object, the OCM contribution is |
| 5 | E3 | MEG-28 / M11 §4 | obstruction certificate content = the precondition of a governed Jump | PROVED | PROVED | `check_e3_meg28_obstruction_certificate` | BMC completeness thresholds / CEGAR (verified) for "all lower-level alternatives exhausted"; B8 (PROVED) for the Jump; KS-T19 (PROVED) |
| 5 | E4 | M11 §5/§8/§10 | proposal object, pre-outcome prediction, adoption on unseen tasks | PROVED | PROVED | `check_e4_m11_proposal_prediction_adoption` | pre-registration and hold-out evaluation (batch-4 D1, PARENT_OWNED); batch-2 B8(iii) external commit (PROVED) |
| 5 | E5 | M11 §9 | shadow execution non-interference and the assurance receipt chain | PROVED | PROVED | `check_e5_m11_shadow_non_interference` | Goguen–Meseguer noninterference (candidate, unverified) — the theorem is the finite, by-construction half (the shadow has no write capability outside K_self, F10 ocap); hash chains / append-only logs (classic) |
| 5 | E6 | MEG-18 / MEG-28 / M11 §11–12 | adoption as a stamped DPO rewrite; exact rollback with caches | PROVED | PROVED | `check_e6_meg18_reopen_and_exact_rollback` | DPO/adhesive (verified), ATMS context switching (verified), batch-1 T4 and batch-2 B8 (PROVED) |
| 5 | E7 | MEG-30 (extension of batch-1 T8) | meta-level termination and the livelock bound | PROVED | PROVED | `check_e7_meg30_meta_termination` | Floyd well-founded termination (verified); batch-1 T8 (PROVED) |
| 5 | E8 | — | KS-T12 / KS-T14 improvement halves stated as CONJECTURES with exact falsifiers | CONJECTURE | CONJECTURE | `check_e8_improvement_conjectures` | (no parent sentence in section; see status line) |
| 5 | R1 | MEG-19 deconsolidation | PROVED (exactness half) / OPEN (decision). | PROVED | PROVED, OPEN, PARENT_OWNED | `check_r1_meg19_deconsolidation` | PARENT_OWNED (DreamCoder/LILO) |
| 5 | R2 | MEG-27 open inventory | PROVED for regular inventories / OPEN for non-regular acceptability. | PROVED | PROVED, OPEN | `check_r2_meg27_regular_inventory` | Rabin–Scott / reachability (classic) — PARENT_OWNED |
| 5 | R3 | MEG-02 graded semiring | OPEN, with a recorded witness. | OPEN | OPEN | `check_r3_meg02_graded_witness` | (no parent sentence in section; see status line) |
| 6 | F1 | P1 | capability-level revocation over ⊕ warrants | PROVED | PROVED, PARENT_OWNED | `check_f1_capability_revocation` | ATMS environments/nogoods (de Kleer 1986), minimal hitting sets (Reiter 1987) — PARENT_OWNED for the lattice facts |
| 6 | F2 | P2 | the unit of inference for lifetime residuals | PROVED | PROVED, PARENT_OWNED | `check_f2_unit_of_inference` | Hurlbert 1984 (pseudoreplication), Kish 1965 (design effect), exact sign test / McNemar — PARENT_OWNED; batch-4 D1 for the decision rule |
| 6 | F3 | P3 | observational limits of self-diagnosis (batch-5 E2 grammar) | PROVED | PROVED | `check_f3_observational_limits` | identifiability / likelihood principle (classic); batch-5 E2 (PROVED) |
| 6 | F4 | P4 | false-structural-alarm lemma | PROVED | PROVED | `check_f4_false_structural_alarm` | batch-5 E2/E3 (PROVED); model-based diagnosis with fault modes (Reiter 1987) — PARENT_OWNED |
| 6 | F5 | P5 | epistemic identity of a persistent machine | PROVED (finite) | PROVED (finite), PARENT_OWNED | `check_f5_epistemic_identity` | hash chains / linked timestamping (Haber–Stornetta 1991), fork consistency (Mazières–Shasha 2002; candidate, unverified), event sourcing — PARENT_OWNED; the identity triple is the OCM reading |
| 6 | F6 | MEG-02 graded half | the (max, ×) graded antichain is exact; scalar retraction is not a function | PROVED | PROVED, PARENT_OWNED | `check_f6_graded_semiring_half` | provenance semirings and specialisation (Green–Karvounarakis–Tannen 2007), absorptive/PosBool provenance, Viterbi semiring — PARENT_OWNED |
| 6 | F7 | MEG-28 | ceilings for J2/J3 on the 3-input Boolean tower (MEG-07 left OPEN) | PROVED | PROVED, OPEN | `check_f7_j2_j3_ceilings` | Reed–Muller / ANF degree (classic), CEGAR / BMC completeness thresholds — PARENT_OWNED; batch-2 B8 and batch-5 E3 (PROVED) |
| 6 | F8 | P6 | information-budget binding for a reference arm | PROVED (finite) | PROVED (finite), PARENT_OWNED | `check_f8_reference_arm_binding` | Hartley counting, teaching dimension (Goldman–Kearns 1995), batch-4 D1/D2 (PARENT_OWNED); benchmark-contamination audits (candidate parents, unverified) |
| 7 | G1 | MEG-28 | ceilings beyond the 3-input tower: depth-4 exact; J4 relative to a registry; J5 has no uniform ceiling | PROVED | PROVED, EXACTLY_BOUNDED_IMPOSSIBILITY | `check_g1_ceilings_beyond_three_inputs` | Reed–Muller / ANF degree, affine invariance of degree (classic); CEGAR / BMC completeness thresholds — PARENT_OWNED; batch-5 E3, batch-6 F7 (PROVED) |
| 7 | G2 | MEG-07 | per-source normalisation: what can and cannot rescue the M2.1 misses | PROVED | PROVED | `check_g2_per_source_normalisation` | topic-sensitive PageRank (Haveliwala 2002), personalised-PageRank contribution vectors (Andersen–Chung–Lang 2006, as cited by the OCM module), IDF — PARENT_OWNED; KS-T05 linearity, KS-T06/T06b (registered design choice) |
| 7 | G3 | MEG-27 | context-free inventory: exact prefix commitment, the completeness threshold, and the honest boundary | PROVED | PROVED, PARENT_OWNED | `check_g3_context_free_inventory` | Bar-Hillel (CFL ∩ REG), emptiness / shortest-word fixed points (Knuth 1977), Cho & Boland 2025 (listed, unverified) — batch-3 C3, batch-5 R2 (PROVED) |
| 7 | G4 | MEG-19 | the deconsolidation decision: the parent's rule, executable, and what is not the parent's | PARENT_OWNED | PARENT_OWNED, PROVED | `check_g4_deconsolidation_decision` | PARENT_OWNED (MDL) |
| 7 | G5 | KS-T12 / KS-T14 | the improvement halves as exact clauses; the unconditional forms refuted | PROVED | PROVED | `check_g5_improvement_halves` | BFS cost, linear span (classic); batch-2 B7/B8, batch-4 D7, batch-5 E3/E8 |
| 7 | G6 | MEG-02 | the (+,×) reading as a measure over warrants: what it licenses without being a homomorphism | PROVED (finite) | PROVED (finite), PARENT_OWNED | `check_g6_measure_reading` | PARENT_OWNED (Green–Karvounarakis–Tannen 2007) |
| 7 | G7 | — | reference-arm grading: "licensed by the given information" vs "true" | PROVED (finite) | PROVED (finite) | `check_g7_reference_arm_grading` | F8 (batch 6) information binding; selective classification / abstention (Chow 1970); closed-world assumption vs licence (Reiter 1978) — PARENT_OWNED |
| 7 | G8 | — | M12 V3 paired lifetimes: exact sizes and powers, multiplicity, the exchangeability condition and its leaks | PROVED | PROVED | `check_g8_paired_lifetimes` | exact sign test, Bonferroni, Hurlbert 1984 (F2), exchangeability / permutation-test null (Fisher; Lehmann–Romano) — PARENT_OWNED |
| 7 | G9 | — | MEG-34 SHRG/CCG half: positive aligned pairs cannot identify a superfinite inventory class | PARENT_OWNED | PARENT_OWNED, EXACTLY_BOUNDED_IMPOSSIBILITY | `check_g9_positive_only_identification` | Gold 1967, Angluin 1980 (tell-tales), Kanazawa 1998 (k-valued categorial grammars, candidate, unverified) |
| 8 | H1 | FDX-01 | open-system epistemic closure: the weakest checkable interface, and the exact impossibility below it | PROVED (finite) | PROVED (finite), EXACTLY_BOUNDED_IMPOSSIBILITY, PARENT_OWNED | `check_h1_open_system_closure` | PARENT_OWNED (Pnueli 1985; Alur–Henzinger 1999, reactive modules) |
| 8 | H2 | FDX-02 | controlled epistemic viability: the kernel is the parent's; the typed interface gives its closed form and separates commit from closure | PARENT_SUFFICIENT | PARENT_SUFFICIENT, PROVED | `check_h2_controlled_viability` | PARENT_SUFFICIENT (finite-horizon safety/reachability game) |
| 8 | H3 | FDX-03 | information/interface conservation: the deterministic typed fragment, exact | PROVED (finite) | PROVED (finite), OPEN | `check_h3_information_conservation` | PARENT_OWNED (Buhrman–de Wolf 2002) |
| 8 | H4 | FDX-05 | reversible and irreversible transitions: an exact four-way classification on the ledger fixture | PROVED (finite) | PROVED (finite), PARENT_OWNED | `check_h4_reversibility_classes` | PARENT_OWNED (Gray–Reuter 1993; ARIES, Mohan et al. 1992) |
| 9 | I1 | FDX-08 | stochastic warrant dynamics: what a time-indexed claim, a reopening bound and a receipt may state | PROVED (finite) | PROVED (finite), EXACTLY_BOUNDED_IMPOSSIBILITY, PARENT_OWNED | `check_i1_stochastic_warrant` | PARENT_OWNED (Markov, Ville/SPRT, Bayes) |
| 9 | I2 | FDX-11 | epistemic bifurcation / obstruction: the boundary is a lattice fact, the obstruction is an evidence-invariant failure | PROVED (finite) | PROVED (finite), PARENT_OWNED | `check_i2_bifurcation` | PARENT_OWNED (monotone sensitivity, ATMS, Dung 1995, E3/G1) |
| 9 | I3 | FDX-13 | self-model calibration under reflexive dependence: performative fixed points, the shadow as the counterfactual arm | PROVED (finite) | PROVED (finite), PARENT_OWNED | `check_i3_self_model_calibration` | PARENT_OWNED (performative prediction, adaptive data analysis, E1/E4/E5) |
| 9 | I4 | FDX-15 | parent-product equivalence / residual theorem: when a measured residual is attributable to the declared difference | PROVED (finite) | PROVED (finite), PARENT_SUFFICIENT, CONJECTURE, PARENT_OWNED | `check_i4_residual_attribution` | PARENT_SUFFICIENT (parent+Δ ≡ OCM) |
| 10 | J1 | FDX-06 | distributed Machine Epistemics: what exchange of warranted atoms can and cannot carry | PARENT_SUFFICIENT | PARENT_SUFFICIENT, PROVED | `check_j1_distributed_epistemics` | PARENT_SUFFICIENT (state-based CRDT convergence, R5 freshness impossibility, Byzantine agreement for authority objects) |
| 10 | J2 | FDX-07 | epistemic games: the attack surface of the commitment gate, then the exact gate statements | PARENT_SUFFICIENT | PARENT_SUFFICIENT, PROVED, EXACTLY_BOUNDED_IMPOSSIBILITY | `check_j2_epistemic_games` | PARENT_SUFFICIENT (cheap talk, disclosure, persuasion, inspection games, Sybil, IP soundness) |
| 10 | J3 | FDX-14 | whole-system lower bounds on the registered finite classes: identification, retention, repair, communication, verification | PARENT_OWNED | PARENT_OWNED, PROVED | `check_j3_whole_system_lower_bounds` | PARENT_OWNED (query complexity, teaching/specifying sets, fooling sets, cell-probe pigeonhole, erasure counting) |
| 11 | K1 | FDX-09 | infinite structured lifecycle learning: the category-level construction frontier | PARENT_OWNED | PARENT_OWNED, PROVED, EXACTLY_BOUNDED_IMPOSSIBILITY | `check_k1_infinite_structured_learning` | PARENT_OWNED (Gold finite classes, Angluin tell-tales, coupon collector, Catalan counting) |
| 11 | K2 | FDX-10 | endogenous representation discovery: search information for a discovered versus a given operator | PARENT_OWNED | PARENT_OWNED, PROVED, EXACTLY_BOUNDED_IMPOSSIBILITY | `check_k2_endogenous_representation_discovery` | PARENT_OWNED (Solomonoff/Levin, MDL, DreamCoder-class, Kolmogorov invariance) |
| 11 | K3 | FDX-12 | safe incremental language commitment: the N2 realiser's theorem | PARENT_SUFFICIENT | PARENT_SUFFICIENT, PROVED | `check_k3_safe_incremental_commitment` | PARENT_SUFFICIENT (Alpern–Schneider, F6, G3, Bar-Hillel) |
<!-- FIELD_MAP_GENERATED:theorems END -->

## 3. Cross-reference graph

**Method.** A theorem depends on another when its section cites it. Two citation forms are counted:
*explicit* (`batch-N Xk`, `batch N Xk's`, and slash / comma lists attached to one) and *bare* (`Xk` alone)
— the latter only for the id letters T, B, E, G, I, whose bare use in these documents has no competing
meaning; the letters C (gate clauses C1–C4, classes C0–C6), D (diagnostic layers D0–D6), F (frontier notes
F1/F2/F6, atlas parents-table rows), H (obligation items) and J (Jump levels J0–J5) are counted only in the
explicit form. A reference is kept only when its target lies in the same or an earlier batch. Definitional
dependencies are the KS-T ids (registry rows of the KSO contract and its OCM extensions) and the MEG / FDX
ids a section cites. `discharges` lists the OCM registry rows whose `gap` field names the theorem (or its
atlas id) and whose status is PROVED / PARENT_OWNED; `leaves open` lists the rows so named whose status is
OPEN, FINITE_CALIBRATION or CANNOT_CHECK. Rows KS-T118 onward are the derived registry of §7.

<!-- FIELD_MAP_GENERATED:graph BEGIN -->
| id | depends on (explicit) | depends on (bare) | KS-T cited | MEG / FDX cited | discharges | leaves open |
|---|---|---|---|---|---|---|
| T1 | — | — | — | MEG-04 | KS-T30, KS-T80 | — |
| T2 | — | — | KS-T05 | — | — | — |
| T3 | — | — | KS-T02, KS-T18, KS-T24 | — | — | — |
| T4 | — | — | KS-T04, KS-T04b, KS-T04c | MEG-28 | — | — |
| T5 | — | — | KS-T09, KS-T21, KS-T22 | — | KS-T74, KS-T81 | — |
| T6 | — | T3 | KS-T02, KS-T20, KS-T21 | — | KS-T35, KS-T37 | — |
| T7 | — | T1 | KS-T21 | MEG-01, MEG-25 | — | — |
| T8 | — | — | KS-T05 | — | — | — |
| T9 | — | — | — | MEG-01 | — | — |
| T10 | — | — | KS-T21 | MEG-03 | KS-T96 | — |
| T11 | — | — | KS-T20, KS-T21 | — | KS-T33, KS-T87 | — |
| B1 | — | T1 | KS-T20 | — | KS-T38, KS-T43, KS-T60 | — |
| B2 | — | — | KS-T21 | — | KS-T39, KS-T51, KS-T82 | — |
| B3 | — | B2 | KS-T31 | MEG-12 | KS-T39, KS-T51, KS-T82 | KS-T31 |
| B4 | — | — | KS-T10a | — | KS-T34 | — |
| B5 | — | — | KS-T22 | — | KS-T36, KS-T44, KS-T92 | — |
| B6 | — | — | KS-T31 | — | KS-T92 | — |
| B7 | — | — | KS-T12 | — | KS-T73 | — |
| B8 | — | T4 | KS-T14 | — | — | — |
| C1 | — | — | KS-T21 | — | KS-T46, KS-T55, KS-T89 | — |
| C2 | — | B1 | — | — | KS-T47, KS-T61, KS-T63, KS-T70, KS-T94 | KS-T62 |
| C3 | — | — | — | — | — | KS-T62 |
| C4 | — | — | — | — | — | — |
| C5 | — | — | KS-T26 | — | KS-T26 | — |
| C6 | — | B2 | KS-T18 | — | KS-T54 | KS-T31 |
| C7 | — | B1, B5 | KS-T25 | — | KS-T25, KS-T48, KS-T60 | — |
| C8 | — | B8, T4 | KS-T07b | — | — | — |
| D1 | — | — | — | — | KS-T67, KS-T90, KS-T106 | KS-T66 |
| D2 | — | B2, B3, T9 | — | — | KS-T57 | KS-T58 |
| D3 | — | T3 | KS-T21, KS-T04b | — | KS-T27, KS-T53 | — |
| D4 | — | — | KS-T06, KS-T06b | — | KS-T28 | — |
| D5 | — | — | KS-T07b | — | KS-T73 | — |
| D6 | B2, B3 | — | — | — | KS-T56 | KS-T72 |
| D7 | — | — | KS-T19, KS-T07b | — | — | KS-T42, KS-T50, KS-T72, KS-T75, KS-T78 |
| D8 | — | T1, T3 | KS-T20, KS-T23, KS-T07b | — | — | KS-T42, KS-T50, KS-T76, KS-T78 |
| E1 | D3 | T1, T5, T7 | — | — | KS-T96 | — |
| E2 | — | E3 | KS-T19 | — | — | KS-T97 |
| E3 | — | B8 | KS-T19 | — | KS-T98 | — |
| E4 | B8, D1 | — | — | — | KS-T99 | — |
| E5 | — | E1 | — | — | KS-T100 | — |
| E6 | B8 | T4 | KS-T22 | — | KS-T101 | — |
| E7 | — | T8 | — | — | KS-T102 | — |
| E8 | D7 | B7, B8, E3 | KS-T12, KS-T14 | — | — | — |
| R1 | — | B7 | — | MEG-19 | KS-T73 | — |
| R2 | C3 | — | — | MEG-27 | — | KS-T62 |
| R3 | D3 | — | KS-T04b | MEG-02 | KS-T27, KS-T53 | — |
| F1 | — | — | — | — | KS-T114 | — |
| F2 | D1 | — | — | — | — | KS-T115 |
| F3 | E2 | — | — | — | — | — |
| F4 | E2, E3 | — | — | — | KS-T110 | — |
| F5 | — | — | — | — | KS-T112 | — |
| F6 | — | — | KS-T21, KS-T04b | MEG-02 | KS-T27, KS-T53 | — |
| F7 | B8, E3 | — | — | MEG-07 | — | — |
| F8 | D1, D2 | — | — | — | — | — |
| G1 | E3, F7 | — | — | MEG-28 | — | — |
| G2 | — | — | KS-T05, KS-T06, KS-T06b | — | KS-T28 | — |
| G3 | C3 | — | — | — | — | KS-T62 |
| G4 | E4 | E8 | — | — | KS-T73 | — |
| G5 | B7, B8, D7, E3, E8 | — | KS-T12, KS-T14 | — | KS-T116 | — |
| G6 | D3 | — | KS-T21 | — | KS-T27, KS-T53 | — |
| G7 | — | — | — | — | — | KS-T117 |
| G8 | — | — | — | — | — | — |
| G9 | C6, D6 | — | — | — | KS-T56 | KS-T72 |
| H1 | — | — | — | — | KS-T118 | — |
| H2 | E4 | — | — | FDX-02 | — | KS-T119 |
| H3 | D2, F8 | — | — | — | KS-T120 | — |
| H4 | F5 | — | — | — | KS-T121 | — |
| I1 | — | G6 | KS-T21 | FDX-01, FDX-02 | — | — |
| I2 | E3, F1, G1 | E2 | — | — | — | — |
| I3 | D8 | E1, E4, E5 | KS-T21 | — | — | — |
| I4 | D1, F1, F2, G7, G8 | — | — | — | — | — |
| J1 | — | T1, T4, T5 | KS-T21, KS-T22 | FDX-08 | — | — |
| J2 | — | T1, T3 | — | MEG-16 | — | — |
| J3 | D2, H3 | T9 | — | MEG-34, FDX-09 | — | — |
| K1 | B2, B3, D3, D6, G9 | — | — | — | — | — |
| K2 | E4 | — | — | FDX-14 | — | — |
| K3 | G3 | — | — | — | — | — |
<!-- FIELD_MAP_GENERATED:graph END -->

**KS-T ids cited by the theorem sections.** Every cited id resolves to a registry row of the snapshot or is
flagged with the reason; a flagged id that later acquires a row makes the checker fail (`STALE_FLAG`).

<!-- FIELD_MAP_GENERATED:kst BEGIN -->
| KS-T id | registry | status | cited by |
|---|---|---|---|
| KS-T02 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T3, T6 |
| KS-T04 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T4 |
| KS-T04b | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T4, D3, R3, F6 |
| KS-T04c | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T4 |
| KS-T05 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T2, T8, G2 |
| KS-T06 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | D4, G2 |
| KS-T06b | KSO_OBLIGATION_REGISTRY_V1.json | FINITE_CALIBRATION | D4, G2 |
| KS-T07b | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | C8, D5, D7, D8 |
| KS-T09 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T5 |
| KS-T10a | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | B4 |
| KS-T12 | KSO_OBLIGATION_REGISTRY_V1.json | OPEN | B7, E8, G5 |
| KS-T14 | **FLAGGED: no registry row** — KSO substrate contract §20 OPEN_M4 id (Jump improvement); no registry row — preservation half B8, improvement clause G5 (registry KS-T116 PROVED_WITH_CLAUSE) | — | B8, E8, G5 |
| KS-T18 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T3, C6 |
| KS-T19 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | D7, E2, E3 |
| KS-T20 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T6, T11, B1, D8 |
| KS-T21 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T5, T6, T7, T10, T11, B2, C1, D3, F6, G6, I1, I3, J1 |
| KS-T22 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T5, B5, E6, J1 |
| KS-T23 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | D8 |
| KS-T24 | KSO_OBLIGATION_REGISTRY_V1.json | PROVED | T3 |
| KS-T25 | OCM_RUNTIME_OBLIGATION_REGISTRY_V1.json | PROVED | C7 |
| KS-T26 | OCM_RUNTIME_OBLIGATION_REGISTRY_V1.json | PROVED | C5 |
| KS-T31 | OCM_RUNTIME_OBLIGATION_REGISTRY_V1.json | FINITE_CALIBRATION | B3, B6 |
<!-- FIELD_MAP_GENERATED:kst END -->

## 4. Exactly bounded impossibilities

Each entry is one string of the owning batch checker's `EXACTLY_BOUNDED_IMPOSSIBILITIES` constant (batches
7–11; batches 1–6 record their impossibility witnesses inside theorem status lines — F6's scalar retraction,
D1's `n_d ≥ 76` — and batch 7 restates the ones that survive in §K of the atlas). The checker requires a
bound marker in every entry (`no`, `never`, `below`, `≥`, `cannot`, `impossible`, `undecidable`, `not`, `only`)
and an owning theorem. The fixture / witness column is the owning theorem's status line, which carries the
counts; the parent column is the theorem's parent.

<!-- FIELD_MAP_GENERATED:impossibilities BEGIN -->
| # | batch | row | theorem | exact bound | fixture / witness (status line) | parent |
|---|---|---|---|---|---|---|
| 1 | 7 | MEG-28 J5 | G1 | no uniform ceiling — the predicate is identically false over an unrestricted tool class (witness t = q); decidable only per registered finite class | MEG-28 J4+ PROVED depth-4 tower; J4 exact per registered class (witness); J5 uniform ceiling IMPOSSIBLE (t = q), decidable per registered class | Reed–Muller / ANF degree, affine invariance of degree (classic); CEGAR / BMC completeness thresholds — PARENT_OWNED; batch-5 E3, batch-6 F7 (PROVED) |
| 2 | 7 | MEG-28 J4 | G1 | the ceiling is a function of the registered reformulation class, not of the target (transposition witness) | MEG-28 J4+ PROVED depth-4 tower; J4 exact per registered class (witness); J5 uniform ceiling IMPOSSIBLE (t = q), decidable per registered class | Reed–Muller / ANF degree, affine invariance of degree (classic); CEGAR / BMC completeness thresholds — PARENT_OWNED; batch-5 E3, batch-6 F7 (PROVED) |
| 3 | 7 | MEG-07 | G2 | no monotone functional of (a_Q, π) admits an atom with a_Q < π while satisfying KS-T06; matched-cardinality averaging is inert (linearity) | MEG-07 PROVED: monotone re-normalisation impossible (KS-T06); matched-cardinality background inert; structural clause no-drop with cone bound | topic-sensitive PageRank (Haveliwala 2002), personalised-PageRank contribution vectors (Andersen–Chung–Lang 2006, as cited by the OCM module), IDF — PARENT_OWNED; KS-T05 linearity, KS-T06/T06b (registered design choice) |
| 4 | 7 | MEG-27 | G3 | prefix commitment under a context-free acceptability predicate is intersection emptiness of two CFLs — undecidable in general (PARENT_OWNED); CANNOT_CHECK without a threshold | MEG-27 PROVED (CF inventory, state-regular acceptability; threshold ℓ*; no prefix-independent bound); CF acceptability PARENT_OWNED (undecidable) | Bar-Hillel (CFL ∩ REG), emptiness / shortest-word fixed points (Knuth 1977), Cho & Boland 2025 (listed, unverified) — batch-3 C3, batch-5 R2 (PROVED) |
| 5 | 7 | MEG-19 | G4 | the split/keep objective is not a theorem of the warrant algebra (MDL, PARENT_OWNED); only its LIVE-gating, exactness and governance are OCM theorems | MEG-19 PARENT_OWNED decision (MDL) executable + falsifier; PROVED LIVE-gating, exactness, governance, MDL ≠ navigation gain | PARENT_OWNED (MDL) |
| 6 | 7 | MEG-02 | G6 | the (+,×) reading is a measure (valuation), never a semiring homomorphism once evidence is shared | MEG-02 (+,×) PROVED (finite): valuation, exact retraction, expectation receipts under sharing; not a homomorphism; measure facts PARENT_OWNED | PARENT_OWNED (Green–Karvounarakis–Tannen 2007) |
| 7 | 7 | MEG-34 | G9 | positive aligned pairs cannot identify a superfinite inventory class (Gold 1967); the registered query channel is necessary | MEG-34 PARENT_OWNED, exactly bounded (Gold 1967 / Angluin 1980); registered query channel separates | Gold 1967, Angluin 1980 (tell-tales), Kanazawa 1998 (k-valued categorial grammars, candidate, unverified) |
| 8 | 8 | FDX-01 | H1 | no function of the registered state is a sound current-validity claim for a conclusion with an uncovered dependency root (registered view identical, validity differs) | FDX-01 PROVED (finite): interface = cover every dependency root (monitor \| revocable assumption); unconditional ⇔ all monitored; below it EXACTLY_BOUNDED_IMPOSSIBILITY (view-identical witness, 1 727); closure relative to D; PARENT_OWNED interface | PARENT_OWNED (Pnueli 1985; Alur–Henzinger 1999, reactive modules) |
| 9 | 8 | FDX-02 | H2 | against an adversarial declared envelope, commit is forceable only from states with no information action pending (every information action hands the answer to the environment) | FDX-02 PARENT_SUFFICIENT (finite-horizon safety/reachability game); PROVED corollaries: closed form 10 584/10 584, commit attractor = no information action pending (312), abstain trivialisation, deadline vs indefinite contracts separate | PARENT_SUFFICIENT (finite-horizon safety/reachability game) |
| 10 | 8 | FDX-03 | H3 | guaranteed zero-error identification over the whole class needs a discrete declared join; below it at least ceil(log2(largest class)) undeclared bits | FDX-03 PROVED (finite deterministic typed fragment): version space = join class; garbling adds nothing (memory 533); parity verifier = missing observation; D(H) = 4 = entropy bound; scope charged to assumption ids (32); risk never exact; identification bound ⌈log2 L⌉, success ≠ channel; FD-07 general OPEN | PARENT_OWNED (Buhrman–de Wolf 2002) |
| 11 | 8 | FDX-05 | H4 | the full append-only state is never restored by any transition; identity-creating transitions have no exact semantic inverse | FDX-05 PROVED (finite classification): ESI / BOI_STABLE / BOI_DIVERGENT / NI on 12 singles, 142 + 1 667 sequences; all-ESI ⇔ ESI composite; act ⇒ NI; full state never restored; identity loss invisible to π_sem, witnessed by history; PARENT_OWNED components | PARENT_OWNED (Gray–Reuter 1993; ARIES, Mohan et al. 1992) |
| 12 | 9 | FDX-08 | I1 | no bound below T on the number of liveness flips over T steps without a registered generating model or a declared revision envelope (every smaller bound has an admissible counter-path) | FDX-08 PROVED (finite) + EXACTLY_BOUNDED_IMPOSSIBILITY: ledger liveness exact; stochastic claims CONDITIONAL_ON_MODEL (model id revocable); reopening rate bounded iff model or envelope registered (min(2ρ,T)); predictive probability not a function of the path (spread ½, 44 paths match no model); Bayesian revocation = marginalisation (divide-out wrong on 320/384); anytime-valid guarantee revocation 0.011 ≤ α vs per-step 0.075; PARENT_OWNED (Markov, Ville/SPRT, Bayes); graded semiring not reopened | PARENT_OWNED (Markov, Ville/SPRT, Bayes) |
| 13 | 9 | FDX-08 | I1 | no predictive probability is a function of the observed ledger path alone (every registered model has positive likelihood on every path and they disagree by 1/2) | FDX-08 PROVED (finite) + EXACTLY_BOUNDED_IMPOSSIBILITY: ledger liveness exact; stochastic claims CONDITIONAL_ON_MODEL (model id revocable); reopening rate bounded iff model or envelope registered (min(2ρ,T)); predictive probability not a function of the path (spread ½, 44 paths match no model); Bayesian revocation = marginalisation (divide-out wrong on 320/384); anytime-valid guarantee revocation 0.011 ≤ α vs per-step 0.075; PARENT_OWNED (Markov, Ville/SPRT, Bayes); graded semiring not reopened | PARENT_OWNED (Markov, Ville/SPRT, Bayes) |
| 14 | 9 | FDX-11 | I2 | an obstruction certificate cannot be issued at any state with an evidence neighbour that solves the task; conversely an obstruction is moved by no evidence change | FDX-11 PROVED (finite): boundary = cut ∪ completion ∪ nogood cover ∪ authority meet (3 840/3 840, 2 524 flips all explained); jumps ≤ 2 (evidence) / 5 (authority); sensitivity per atom; commitment set = grounded extension (512), two stable extensions on 32 conflict states; obstruction ⇔ E-invariant failure (12/12), moved only by R; PARENT_OWNED (monotone sensitivity, ATMS, Dung 1995, E3/G1) | PARENT_OWNED (monotone sensitivity, ATMS, Dung 1995, E3/G1) |
| 15 | 9 | FDX-13 | I3 | with the reflexive loop unregistered no self-prediction is stable on 9 of 75 fixtures (period-2 orbits); the counterfactual (shadow) rate is defined on all of them | FDX-13 PROVED (finite): performative fixed points {rA if rA<θ} ∪ {m if m≥θ} (0/1/2 on 9/59/7 fixtures), orbits converge or period 2 (594/81); caused-outcome scoring self-fulfilling (42); shadow = counterfactual arm (E4 tightened); held-out reuse optimism 15/64; self-prediction never a warrant; PARENT_OWNED (performative prediction, adaptive data analysis, E1/E4/E5) | PARENT_OWNED (performative prediction, adaptive data analysis, E1/E4/E5) |
| 16 | 9 | FDX-15 | I4 | within one lifetime of four items the D1 rule can reject in neither direction; PARENT_SUFFICIENT needs n_d ≥ 76 discordant pairs; at m = 8 lifetimes the minimum detectable win probability at power 0.8 is 0.90 | FDX-15 PROVED (finite attribution theorem: five clauses, three failure modes) / PARENT_SUFFICIENT on the fixture (parent+Δ ≡ OCM) / CONJECTURE for the general equivalence (falsifier = ablation arm ≠ parent on a matched unit); real 1/256 attributable, unmatched confounded, undetectable 1/8 (min detectable p 0.90), collapsed flagged, pooled refused, reference refused; PARENT_OWNED (D1, F2, F8, G7, G8) | PARENT_SUFFICIENT (parent+Δ ≡ OCM) |
| 17 | 10 | FDX-06 | J1 | a node whose view misses an effective revocation cannot distinguish the history with that revocation from the one without (identical view, different verdicts) — no non-abstaining current-validity policy is sound (R5) | FDX-06 PARENT_SUFFICIENT (state-based CRDT convergence, R5 freshness impossibility, Byzantine agreement for authority objects); PROVED corollaries: antitone liveness 4 536, revoke-wins order-independent 59 orders (LWW diverges 117), over-claim ⇔ missing revocation 354/354, indistinguishable histories (97 wrong / 0), import authority ≤ sender ∧ cap with commit 0 (162), relay bounded 1 458, join caught 490, trust revocation local 1 336, Impact ∪-distributive 4 096, batched cone ⊆ sequential 36, k-source ⊕ without world_truth | PARENT_SUFFICIENT (state-based CRDT convergence, R5 freshness impossibility, Byzantine agreement for authority objects) |
| 18 | 10 | FDX-07 | J2 | no strategy of an evidence provider whose channel carries authority (source=1) makes the gate commit a claim requiring world_truth ≥ 1 or commit ≥ 1 through its evidence alone; and no strategy changes the gate's verdict on a claim none of whose warrants cite its ids | FDX-07 PARENT_HEAVY / PARENT_SUFFICIENT (cheap talk, disclosure, persuasion, inspection games, Sybil, IP soundness); PROVED gate-specific: non-interference 486, authority ceiling 0/486 (EXACTLY_BOUNDED), no persuasion lever 4 374, contradictions local, REPORT-typed commits exactly 36/61/18, forced refusal iff every warrant cites the provider, receipt names W (cone exact), Sybil 1 vs 3, inspection equilibrium 63/63 | PARENT_SUFFICIENT (cheap talk, disclosure, persuasion, inspection games, Sybil, IP soundness) |
| 19 | 10 | FDX-14 | J3 | no memory with fewer than log2\|H\| mutable bits retains every member of H; no adaptive transcript identifies H in fewer than log2\|H\| channel bits; no deterministic equality protocol on retained procedures uses fewer than log2\|H\| transcript bits; Σ(retention ids) + worst-case repair queries ≥ n + k against k revocations | FDX-14 PARENT_OWNED (query complexity, teaching/specifying sets, fooling sets, cell-probe pigeonhole, erasure counting); PROVED on the registered classes: bits ≥ ⌈log2\|V\|⌉ for 5 mixes (327 675), retention 3-bit refuses 8, Σm + repair ≥ n + k (648 + 48, tight 164), equality ≥ 4 bits with digest collisions 56/24/8/0, oblivious 4 > adaptive 3 = entropy 3 on MONOTONE6, description moves one unit per phase for 8 CANNOT_REPRESENT | PARENT_OWNED (query complexity, teaching/specifying sets, fooling sets, cell-probe pigeonhole, erasure counting) |
| 20 | 11 | FDX-09 | K1 | under a category-level inventory that attests two attachments (or two relation labellings) of one category string, no further positive demonstration lowers the derivation count below 2 — a unique parse is unreachable from positive data; only revocation / a negative channel reaches it | FDX-09 PARENT_OWNED (Gold finite classes, Angluin tell-tales, coupon collector, Catalan counting); PROVED: chart = brute force 12/12; Cat(k+1) = 1 2 5 14 42; treebank 3 / 2 / 1; positive monotone 192/192, unique parse 14/64 all below (EXACTLY_BOUNDED), revocation → 1; identified 255/255, characteristic sample 4 (bound 2); cover time 761/35 uniform, ≈ 38.9 Zipf; unbounded arity never converges 6/6; ranking 9:3 licenses nothing; packing 125 vs 36 | PARENT_OWNED (Gold finite classes, Angluin tell-tales, coupon collector, Catalan counting) |
| 21 | 11 | FDX-10 | K2 | no representation change alters the version space of an evidence table or the identification bits ⌈log2 \|V\|⌉; an abstraction adopted by compression alone licenses no claim on an unseen row | FDX-10 PARENT_OWNED (Solomonoff/Levin, MDL, DreamCoder-class, Kolmogorov invariance); PROVED: version spaces invariant 81/81, unseen rows 104/104 (EXACTLY_BOUNDED); XOR 2 936 → 16, EQV 6 990 → 38, 7 rise / 2 fall, Levin bound 32/32; adoption only with XOR + EQV (4/15, gain 1); discovery 4 bits + 26 032 terms vs 0; memorising abstraction 39 vs 0; 8 minimal XOR definitions | PARENT_OWNED (Solomonoff/Levin, MDL, DreamCoder-class, Kolmogorov invariance) |
| 22 | 11 | FDX-12 | K3 | no bounded lookahead below the saturation depth (non-empty committed content) or below the existential threshold decides SAFE; no existential completion check establishes the universal criterion | FDX-12 PARENT_SUFFICIENT (Alpern–Schneider, F6, G3, Bar-Hillel); PROVED: 5 UNSAFE states by reachability; bounded exact iff k ≥ ℓ* / max(ℓ*, d) / nearest violation (147 + 33); atomic 6 vs streaming 2; revocation refuses, history kept; CF readings undecidable (cited) | PARENT_SUFFICIENT (Alpern–Schneider, F6, G3, Bar-Hillel) |
<!-- FIELD_MAP_GENERATED:impossibilities END -->

## 5. Open list and conjectures, with falsifiers

`CONJECTURE` rows carry an executable falsifier (a function of the batch checker, verified to exist by
name) or the stated falsifier of the batch document. `OPEN` rows are the batch checkers' `OPEN` constants
(batches 8–11); none of them names an executable falsifier, so each is flagged `NO_EXECUTABLE_FALSIFIER`
rather than passed. `OPEN_HALF_CLOSED_LATER` rows are the halves batches 2–6 left open and a later batch
closed (`CLOSED_LATER by …` names the closing theorems; batch 7 reports the open list empty). `CANNOT_CHECK`
rows are recorded and are never a pass.

<!-- FIELD_MAP_GENERATED:open BEGIN -->
| kind | batch | row | theorem | item | falsifier | flag |
|---|---|---|---|---|---|---|
| CONJECTURE | 9 | FDX-15 | I4 | for every OCM mechanism there is a composition of the registered parents plus the typed interface that is outcome-identical on matched channels (FORMALISM_USEFUL_NO_ARCHITECTURE_RESIDUAL); falsifier = an OCM-minus-Δ arm that differs from the parent product on a matched unit | an OCM−Δ arm that differs from the parent product on a matched unit | — |
| CONJECTURE | 5 | KS-T12 | E8 | KS-T12/T14 CONJECTURE (falsifiers exact; smallest holding and failing fixtures recorded) | `falsify_ks_t12` (kso_self_model_prereqs_batch5_exact.py) | — |
| CONJECTURE | 5 | KS-T14 | E8 | KS-T12/T14 CONJECTURE (falsifiers exact; smallest holding and failing fixtures recorded) | `falsify_ks_t14` (kso_self_model_prereqs_batch5_exact.py) | — |
| OPEN | 8 | FD-07 | H3 | FD-07 / FDX-03 general (graded, continuous, adaptive-prior) information conservation — no finite checker promotes it | — | NO_EXECUTABLE_FALSIFIER |
| OPEN | 10 | FDX-06 | J1 | graded / probabilistic trust and Byzantine-fraction thresholds for warrant (not authority) exchange — FDX-08 territory; the exact fragment here is per-source revocable assumptions only | — | NO_EXECUTABLE_FALSIFIER |
| OPEN | 10 | FDX-07 | J2 | truthful-revelation mechanisms with costly verification for real provider utilities — parent-owned and utility-model dependent; only the lattice action set of the gate is bounded here | — | NO_EXECUTABLE_FALSIFIER |
| OPEN | 10 | FDX-14 | J3 | coded / cross-row redundant storage (Singleton-type bounds) and infinite classes (MEG-34 / FDX-09) — not covered by the uncoded evidence-id fixture | — | NO_EXECUTABLE_FALSIFIER |
| OPEN | 11 | FDX-09 | K1 | identification of a *lexicalised* (bilexical) construction inventory from positive demonstrations — the class is finite for a finite lexicon but its characteristic sample scales with lexical pairs; the exact sample cost for the UD-EWT inventory (14 967 of 19 642 rules attested once) is not computed here | — | NO_EXECUTABLE_FALSIFIER |
| OPEN | 11 | FDX-10 | K2 | the proposal policy over an infinite abstraction space (which candidates to price) — parent-owned search policy; only the pricing / adoption rule and its hostile are bounded here | — | NO_EXECUTABLE_FALSIFIER |
| OPEN | 11 | FDX-12 | K3 | prefix safety when acceptability is context-free and the listener reading is regular is decidable by the Bar-Hillel product (stated, not checked); with context-free readings it is undecidable (G3) — no finite fixture exhibits either | — | NO_EXECUTABLE_FALSIFIER |
| OPEN_HALF_CLOSED_LATER | 2 | MEG-19 | B7 | PROVED; improvement half OPEN | — | CLOSED_LATER by R1, G4 |
| OPEN_HALF_CLOSED_LATER | 2 | MEG-28 | B8 | PROVED / PARENT_OWNED (DPO); improvement half OPEN | — | CLOSED_LATER by E3, E6, F7, G1 |
| OPEN_HALF_CLOSED_LATER | 3 | MEG-27 | C3 | PROVED (finite inventory); open-inventory half OPEN (M6) | — | CLOSED_LATER by R2, G3 |
| OPEN_HALF_CLOSED_LATER | 4 | MEG-02 | D3 | PROVED (definitional half) / PARENT_OWNED (Chow 1970, split conformal); graded semiring with exact-share retraction stays OPEN — tightened | — | CLOSED_LATER by R3, F6, G6 |
| OPEN_HALF_CLOSED_LATER | 4 | MEG-07 | D4 | PROVED (exact); tightened: the atlas lever "matched seed cardinality" is inert, the guarantee is for π' (`ocm.kso.surprise` PROPAGATED); per-source normalisation for the 3 residual misses OPEN | — | CLOSED_LATER by G2 |
| OPEN_HALF_CLOSED_LATER | 4 | MEG-34 | D6 | PROVED (six-order class, exhaustive ≤ 3 examples); SHRG/CCG infinite-class half OPEN | — | CLOSED_LATER by G9 |
| OPEN_HALF_CLOSED_LATER | 5 | MEG-19 | R1 | MEG-19 PROVED exactness half / OPEN decision (PARENT_OWNED) | MDL two-part code KEEP iff (k+1)(1+e) ≤ u(k−1) | CLOSED_LATER by G4 |
| OPEN_HALF_CLOSED_LATER | 5 | MEG-27 | R2 | MEG-27 PROVED regular inventories / OPEN non-regular acceptability | `lookahead_regular` (kso_self_model_prereqs_batch5_exact.py) | CLOSED_LATER by G3 |
| OPEN_HALF_CLOSED_LATER | 5 | MEG-02 | R3 | MEG-02 OPEN with witness | scalar retraction witness {{a}} vs {{a},{b}} | CLOSED_LATER by F6, G6 |
| OPEN_HALF_CLOSED_LATER | 6 | MEG-28 | F7 | MEG-28 J2/J3 ceilings PROVED on the 3-input tower; J4+ OPEN; MEG-07 per-source normalisation OPEN | — | CLOSED_LATER by G1 |
| CANNOT_CHECK | 10 | FDX-06 | — | message authenticity (signatures, trust-root provenance) — assumed, not checkable inside the finite model (R6 anchor authenticity) | — | recorded, never a pass |
| CANNOT_CHECK | 10 | FDX-07 | — | that a real provider's utilities match the inspection-game payoffs — outside the model | — | recorded, never a pass |
| CANNOT_CHECK | 10 | FDX-14 | — | collision resistance of digests used for cross-space identity — a computational assumption; the finite model exhibits collisions for every digest shorter than log2\|H\| | — | recorded, never a pass |
| CANNOT_CHECK | 11 | FDX-09 | — | that the UD-EWT induced inventory has converged (the singleton fraction is a Good–Turing reading, not a certificate) and that the real chart cap is reached for the packing reason exhibited here — the checker re-implements the shapes, it does not run the OCM code | — | recorded, never a pass |
| CANNOT_CHECK | 11 | FDX-10 | — | that a real proposed abstraction's evaluator is registered (governance premise; self-certification is refused by construction only when the evaluator is external) | — | recorded, never a pass |
| CANNOT_CHECK | 11 | FDX-12 | — | the listener's reading table J for natural language (F6: empirical, separate); the fixture readings are constructed controls | — | recorded, never a pass |
<!-- FIELD_MAP_GENERATED:open END -->

## 6. The atlas, section by section (A–O)

Sections A–K are the sealed atlas (`ME_THEORY_GAP_ATLAS_V1.md`; A existing theory, B the atomic gap list,
C priority, D parent-owned adoptions, F–K the status tables of batches 2–7); L–O are the addenda (batches
8, 10, 9, 11 in that order — N was written after M). `rows` counts the section's table rows (for B, the
`**MEG-nn` entries; for C, the numbered priorities); `theorems` and `by status` come from §2 for the batch
the section records.

<!-- FIELD_MAP_GENERATED:sections BEGIN -->
| section | source | title | rows | theorems | by status | parent-owned/sufficient | note |
|---|---|---|---|---|---|---|---|
| A | atlas | Existing theory map | 16 | — | — | — | existing theory map (no gaps) |
| B | atlas | Atomic gap list | 35 | — | — | — | 35/35 gap ids carry at least one theorem; foundation registry at freeze: ADOPTED 1, OPEN 21, PROVED 14 |
| C | atlas | Priority (milestones unblocked per unit effort) | 8 | — | — | — | priority list (no theorem rows) |
| D | atlas | Not a gap — parent-owned, cite and adopt | 16 | — | — | — | parent-owned, cite and adopt (no theorem rows) |
| E | — | — | 0 | — | — | — | no such section in the atlas or its addenda (letters skip E) |
| F | atlas | Status after batch 2 (2026-09-05) | 8 | 8 | PROVED 7, PROVED (finite) 1 | 0 |  |
| G | atlas | Status after batch 3 (2026-09-05) | 8 | 8 | PROVED 5, PROVED (finite) 3 | 0 |  |
| H | atlas | Status after batch 4 (2026-09-05) | 8 | 8 | PARENT_OWNED 2, PROVED 5, PROVED (finite) 1 | 2 |  |
| I | atlas | Status after batch 5 (2026-09-05) | 11 | 11 | PROVED 9, CONJECTURE 1, OPEN 1 | 0 |  |
| J | atlas | Status after batch 6 (2026-09-05) | 8 | 8 | PROVED 6, PROVED (finite) 2 | 0 |  |
| K | atlas | Status after batch 7 (2026-09-05) | 9 | 9 | PROVED 5, PARENT_OWNED 2, PROVED (finite) 2 | 2 |  |
| L | addenda | Status after batch 8 (2026-09-05) — field frontier, first batch | 4 | 4 | PROVED (finite) 3, PARENT_SUFFICIENT 1 | 1 |  |
| M | addenda | Status after batch 10 (2026-09-06) — field frontier, distributed / games / lower bounds | 3 | 3 | PARENT_SUFFICIENT 2, PARENT_OWNED 1 | 3 |  |
| N | addenda | Status after batch 9 (2026-09-06) — field frontier, stochastic / bifurcation / self / residual rows | 4 | 4 | PROVED (finite) 4 | 0 |  |
| O | addenda | Status after batch 11 (2026-09-06) — field frontier, learning / representation / commitment | 3 | 3 | PARENT_OWNED 2, PARENT_SUFFICIENT 1 | 3 |  |
<!-- FIELD_MAP_GENERATED:sections END -->

## 7. Derived OCM obligation registry (KS-T118 onward)

`OCM_OBLIGATION_REGISTRY_DERIVED_V1.json` is emitted by the checker from the H/I-items of the consequences
sections of batches 8–11 (batch 8 items H1–H4, batch 9 items I1–I4, batches 10 and 11 items H1–H8 each,
labelled by the theorem and clauses they follow from). Ids continue after the highest KS-T id of the OCM
registries in the snapshot; the four batch-8 items already registered in `OCM_SELF_OBLIGATION_REGISTRY_V2`
keep their ids (KS-T118–T121) and their registry status; every new row is `OPEN` (no checker exists yet),
its runtime location is the backticked OCM path the source item names, and its mutant is the hostile the
source item names, if any. The checker fails if the committed JSON differs from what it derives
(`DERIVED_REGISTRY_STALE`), if the new ids do not continue contiguously after the highest existing id, or
if a `PROVED` row lacks a checker.

<!-- FIELD_MAP_GENERATED:derived BEGIN -->
| id | existing | source | frontier row | statement | runtime location | status | checker | mutant |
|---|---|---|---|---|---|---|---|---|
| KS-T118 | yes | batch 8 H1 (H1) | FDX-01 | the closure interface has no runtime object; the commit gate reads scope without an epoch. Obligation: pass the evaluation epoch, and type the commitment receipt MONITORED_CURRENT / CONDITIONAL_ON_ASSUMPTIONS (assumption ids listed) / NO_CLOSURE, with the `D`-completeness premise named (the `is_dependency_closed` result is that premise for the cited set). | `src/ocm/kso/revocation.py::impact_cone`; `src/ocm/kso/types.py::Scope.covers`; `src/ocm/runtime/solve.py::commitment_gate`; `op.scope.covers(task.context)` | PROVED | tests/m11/test_batch8_obligations.py | — |
| KS-T119 | yes | batch 8 H2 (H2) | FDX-02 | reason-typed abstention; no envelope, risk or budget coordinate at the gate. Obligation: abstentions carry a reason from a registered set; if a viability claim ("will close by T") is ever made, the envelope and budget/deadline become state coordinates and the closed form (i) is the check; a promise to *commit* by T is unlicensed while any information action is pending (ii). | `src/ocm/runtime/solve.py::Decision`; `Decision.UNKNOWN` | OPEN | — (obligation: extend solve.decide / the commitment gate with typed risk/resource/envelope coordinates; report UNKNOWN reasons by predicate) | — |
| KS-T120 | yes | batch 8 H3 (H3) | FDX-03 | the information-budget receipt should charge the join, the assumption ids and the verdict type. | `src/ocm/store/evidence.py::Channel`; `src/ocm/kso/admission.py::WARRANTING_KINDS`; `src/ocm/runtime/state.py::EventStore.replay` | PROVED | tests/m12 (info fields present) | — |
| KS-T121 | yes | batch 8 H4 (H4) | FDX-05 | the ledger already realises the classes; receipts should name them. | `src/ocm/runtime/state.py::EventStore`; `RuntimeState.apply`; `src/ocm/selfmodel/govern.py::AdoptionLedger.rollback`; `src/ocm/selfmodel/replay.py`; `src/ocm/kso/admission.py::AdmissionReceipt.quarantined` | PROVED | tests/m11/test_batch6_obligations.py (rollback), tests/m11/test_selfmodel.py | — |
| KS-T122 | new | batch 9 I1 (I1) | FDX-08 | guarantees need an anytime-valid revocation monitor; stochastic claims need a model id. | `src/ocm/kso/warrant.py::WarrantProfile.liveness`; `src/ocm/operators/registry.py`; `docs/RUNTIME_LIFECYCLE_REVALIDATION_V2.md`; `src/ocm/selfmodel/govern.py::monitor`; `src/ocm/runtime/ocm_runtime.py::admit_evidence`; `src/ocm/runtime/state.py::RuntimeState.apply`; `EventStore.replay`; `src/ocm/selfmodel/model.py::FailureRecord.frequency`; `diagnose.py` | OPEN | — | — |
| KS-T123 | new | batch 9 I2 (I2) | FDX-11 | the reopening report can carry the boundary; the certificate should carry E-invariance. | `src/ocm/kso/revocation.py::reopening_report`; `WarrantProfile.lower`; `src/ocm/kso/nogoods.py:: NogoodSet.add`; `src/ocm/kso/types.py::Authority.meet`; `runtime/solve.py:: commitment_gate`; `src/ocm/selfmodel/diagnose.py::ObstructionCertificate.valid`; `src/ocm/kso/jump.py::_STRONG_TRIGGERS` | OPEN | — | — |
| KS-T124 | new | batch 9 I3 (I3) | FDX-13 | the calibration receipt needs a distribution tag; the shadow is the counterfactual arm. | `src/ocm/selfmodel/govern.py::shadow_evaluate`; `src/ocm/selfmodel/proposal.py::Prediction`; `proposal.py::SelfChangeProposal.discriminator` | OPEN | — | — |
| KS-T125 | new | batch 9 I4 (I4) | FDX-15 | V4 satisfies clauses 1, 2, 3, 5 and declares clause 4; V5 should ablate. | `docs/M12_V4_PAIRED_LIFETIMES_REPORT.md`; `src/ocm/lifetime/reference.py::INFORMATION_BINDING`; `m12_paired_eval.py`; `src/ocm/lifetime/machine.py::WholeSystemParent`; `PersistentOCM.ablations = frozenset()`; `docs/M12_V4R_REEVALUATION_NOTE.md`; `src/ocm/lifetime/phases.py::phase_E(matched_cells=True)`; `m12_paired_eval.py::sign_test_one_sided`; `ST.tost_equivalence(pair, 0.05)`; `8/8` | OPEN | — | — |
| KS-T126 | new | batch 10 H1 (J1 vi) | FDX-06 | imports need a per-principal message assumption. Obligation: every IMPORTED record carries a message assumption bound to `(principal, message)` in its warrant, and principal revocation is capability-level revocation over the principal's assumptions (batch-6 F1), so the cone of (vi) is what `kso/revocation.py::reopening_report` (line 188) reports. | `src/ocm/store/evidence.py::EvidenceRegistry.register`; `src/ocm/knowledge/world.py::assert_fact`; `src/ocm/dialogue/workspace.py`; `kso/revocation.py::reopening_report` | OPEN | — | — |
| KS-T127 | new | batch 10 H2 (J1 ii–iv) | FDX-06 | revocation state must merge as an event set, and verdicts that depend on it are "as of the view". Obligation: exchange revoke/reinstate as events with causal predecessors and merge revoke-wins; type any verdict computed over imported revocation state CONDITIONAL_ON_VIEW (the batch-8 H1 "as of" reading), never current (iv). | `EvidenceRegistry.revoked`; `store/event.py` | OPEN | — | — |
| KS-T128 | new | batch 10 H3 (J1 v) | FDX-06 | trust caps as authority meets at import; no join across paths. Obligation: `A_import = drop_commit(A_sender ∧ T(principal))`, and a claim with alternatives from several imports uses the meet of their authorities, never the coordinate-wise max (T7's `⋁` form is an upper bound, not a licence). | `src/ocm/kso/types.py::internal_authority`; `knowledge/world.py::authority` | OPEN | — | `mutant_repetition_raises_authority` |
| KS-T129 | new | batch 10 H4 (J2 i, v–vii) | FDX-07 | the gate's authority check should be per committing alternative and the receipt should name it. | `src/ocm/runtime/solve.py::commitment_gate`; `task.required_authority <= op.authority.meet(commit_authority)`; `kso/admission.py::compose`; `dialogue/gate.py::required_marker` | OPEN | — | — |
| KS-T130 | new | batch 10 H5 (J2 viii) | FDX-07 | independence over principals, not ids. Obligation: disjointness over registered principals (`source`), else `INDEPENDENCE_NOT_ESTABLISHED`; `mutant_majority_truth` (line 217) stays the runtime's own hostile for the truth half. | `src/ocm/store/evidence.py::independent_support_count` | OPEN | — | `mutant_majority_truth` |
| KS-T131 | new | batch 10 H6 (J2 iv) | FDX-07 | contradiction registrations carry provenance. Obligation: a nogood carries the registrant's message assumption and dies with it. | `EvidenceRegistry.register(contradicts=…)` | OPEN | — | — |
| KS-T132 | new | batch 10 H7 (J3 i–iii) | FDX-14 | information receipts charge alphabet bits; class-restricted memories refuse; repair names fresh evidence. | `src/ocm/kso/admission.py::admit`; `src/ocm/runtime/state.py::EventStore.replay` | OPEN | — | — |
| KS-T133 | new | batch 10 H8 (J3 iv) | FDX-14 | cross-space identity by digest is a computational claim. | `src/ocm/kso/space.py::KnowledgeSpace.digest`; `store/canonical.py::canonical_digest` | OPEN | — | — |
| KS-T134 | new | batch 11 H1 (K1 ii–iv) | FDX-09 | the category-level slot is the ambiguity; record it as such. Obligation: the identifiability receipt of an induced inventory records the *class* it identifies (category-level, arity bound) and the consequence `UNIQUE_PARSE_UNREACHABLE_FROM_ POSITIVE_DATA` for strings whose category shape has ≥ 2 attested decompositions; a unique reading needs a registered negative / membership channel (`ocm.language.acquisition`, batch-7 G9's receipt) or a finer class (bilexical slots, OPEN). | `src/ocm/learning/language/ud_grammar.py::constructions_from_grammar`; `ocm.language.acquisition` | OPEN | — | — |
| KS-T135 | new | batch 11 H2 (K1 v–vii) | FDX-09 | `Grammar.learned` is an identification receipt only for bounded arity. Obligation: the receipt carries the arity bound and the coverage state (rules attested once — 14 967 of 19 642 on UD-EWT — mark the inventory `NOT_CONVERGED`, a Good–Turing reading, not a certificate); a family with a single attested order at count 1 is LEARNED-at-`n = 1`, never a construction with a lifecycle warrant past its one demonstration (D6). | `ud_grammar.py::Grammar.learned` | OPEN | — | — |
| KS-T136 | new | batch 11 H3 (K1 viii) | FDX-09 | the verdict is the count; a ranking orders the unpack. Obligation: keep it; any clarification policy that scores derivations (`max_unpack`, line 86) orders the unpacked meanings and writes the score outside the lattice (batch-4 D3); `AMBIGUOUS_WITH_GOLD_AMONG_UNPACKED` (7 of 32 on dev) is a coverage measure of the unpack order, not evidence for a reading. | `src/ocm/language/chart.py` | OPEN | — | `mutant_first_derivation_only` |
| KS-T137 | new | batch 11 H4 (K1 ix) | FDX-09 | pack by span and type, not by sub-derivation identity. Obligation: key completed nodes by `(start, end, produces, lexical readings of the span)`, keep exact counts by summation, build one representative meaning per node lazily; the count stays exact and the item bound becomes polynomial in the token count. | `chart.py::_lex_key` | OPEN | — | — |
| KS-T138 | new | batch 11 H5 (K2 ii, v) | FDX-10 | a representation introduction carries a search-and-evaluation receipt. | `ud_grammar.py`; `src/ocm/kso/admission.py:: admit` | OPEN | — | — |
| KS-T139 | new | batch 11 H6 (K2 iv, vi) | FDX-10 | adoption by compression is a proposal, never a licence. | `selfmodel/govern`; `kso/jump.assess_jump` | OPEN | — | — |
| KS-T140 | new | batch 11 H7 (K3 i–iii) | FDX-12 | the realiser's check certifies the final reading; a streaming channel needs the prefix criterion. Obligation: declare the channel in the realisation receipt (`ATOMIC` — the surface is delivered whole — or `STREAMING`); under `STREAMING` run the K3 exact criterion per prefix against the inventory's completion automaton (finite-state today: five templates), returning SAFE / UNSAFE / CANNOT_CHECK with the thresholds `(ℓ*, d)` as the completeness certificate; never approximate a context-free inventory by a DFA (G3) and never read a bounded pass as SAFE. | `src/ocm/language/realize.py::realize`; `Realization.checked` | OPEN | — | — |
| KS-T141 | new | batch 11 H8 (K3 iv) | FDX-12 | revocation during emission refuses the next token and keeps the history. Obligation: the streaming path re-checks gate (3) at every token, refuses on a DEAD committed claim with the claim named, and appends — never subtracts — the emitted history (F6.2); a correction is a new typed act. | `realize.py`; `src/ocm/runtime/solve.py::commitment_gate` | OPEN | — | — |
<!-- FIELD_MAP_GENERATED:derived END -->

## 8. What the field does not claim

* **No novelty.** Every batch document closes with `NOVELTY NOT_ESTABLISHED`; the foundation's
  `non_consequences` and the frontier's `GENERAL_NOVELTY = NOT_ESTABLISHED`, `FIELD_STATUS = NOT_ESTABLISHED`
  stand. The parent-owned share is stated as a count, not argued away: the block's
  `parent_owned_or_sufficient_primary` is the number of theorems whose *primary* status is PARENT_OWNED or
  PARENT_SUFFICIENT, and `parent_owned_or_sufficient_any_mention` the number whose status line names a
  parent as owning part of the result. The rest are exact finite statements over the KnowledgeSpace object
  with planted hostiles — a contribution of form (an exact object, a checker, a mutant) whose mathematics is
  the parents' (Kleene, Pawlak, de Kleer, Green–Karvounarakis–Tannen, Denning / Biba, Doyle, Mitchell, Gold /
  Angluin, Banach, Floyd, Härder–Reuter, Kemeny–Snell, Dung, Alpern–Schneider, Ville, Perdomo, Dwork, …).
* **No superiority.** No theorem compares the OCM to any system; the comparison theorems (D1, F2, G8, I4)
  are the *rules* under which such a comparison would be licensed, and I4's general parent-product
  equivalence stays a CONJECTURE with its falsifier.
* **Finite means finite.** `PROVED (finite)` and every exhaustive count calibrate an implementation on a
  registered fixture; none is an all-size claim (KSO registry rule). `CANNOT_CHECK` is never a pass.
* **Nothing here authorises OCM absorption.** A row enters the OCM only with an exact parity test
  (foundation absorption rule); the derived registry of §7 lists obligations, all `OPEN` unless the OCM
  registry already records a checker.
* **Frontier rows not entered.** FDX-04 is parent-sufficient by `DYNAMICS.md`; FDX-16 is batch 12's row
  (§1 slot: PROVED in Lean for the warrant core, typed terminals and the representation / revision commutation
  theorem OPEN there); the graded / probabilistic half of FDX-08 (imprecise probability, credal sets, Dempster–Shafer) is
  deliberately not entered — D3 / F6 / G6 stand and no scalar-semiring claim is added.
* **External demarcation stays external.** The registry cannot turn any issue into field recognition, nor
  upgrade `PARENT_SUFFICIENT`, `CANNOT_CHECK` or `NOT_ESTABLISHED`.

## 9. Inconsistencies found in the earlier batches (listed, not fixed)

The checker reports the following non-fatal findings; nothing in batches 1–11, the sealed atlas, the
addenda §L–§O or the OCM registries was edited.

<!-- FIELD_MAP_GENERATED:inconsistencies BEGIN -->
| # | finding |
|---|---|
| 1 | STATUS_WORDING F3: document status block says 'PROVED', checker STATUS says 'PROVED (finite)' (same family) |
| 2 | STATUS_WORDING F4: document status block says 'PROVED', checker STATUS says 'PROVED (finite)' (same family) |
| 3 | ATLAS_SECTION_LETTER_ABSENT E: the atlas skips this letter (D → F) |
| 4 | ADDENDA_SECTION_ORDER section N records batch 9 after section M records batch 10 (written in parallel) |
| 5 | HEADING_WITHOUT_TOPIC_CELL E8: two-part heading; filed under ['KS-T12', 'KS-T14'] |
| 6 | HEADING_WITHOUT_TOPIC_CELL G7: two-part heading; filed under no atlas id |
| 7 | HEADING_WITHOUT_TOPIC_CELL G8: two-part heading; filed under no atlas id |
| 8 | HEADING_WITHOUT_TOPIC_CELL G9: two-part heading; filed under ['MEG-34'] |
| 9 | OBLIGATION_ID_COLLISION batches [10, 11] label obligation items ['H1', 'H2', 'H3', 'H4'] with batch-8 theorem ids |
| 10 | FRONTIER_PRIORITY_STALE FDX-09 listed as untouched in the Priority paragraph but carries a batch disposition |
| 11 | FRONTIER_PRIORITY_STALE FDX-10 listed as untouched in the Priority paragraph but carries a batch disposition |
| 12 | FRONTIER_PRIORITY_STALE FDX-12 listed as untouched in the Priority paragraph but carries a batch disposition |
| 13 | FRONTIER_PRIORITY_STALE FDX-16 listed as untouched in the Priority paragraph but carries a batch disposition |
| 14 | FOUNDATION_REGISTRY_SEALED 21 atlas rows are OPEN in MACHINE_EPISTEMICS_FOUNDATION_V1.json (frozen at #319) while every one of the 35 atlas gap ids now carries a theorem; the sealed registry is not the current status |
<!-- FIELD_MAP_GENERATED:inconsistencies END -->

Findings the checker cannot phrase mechanically, read from the same sources:

1. **KS-T119's registry row mixes two batch-8 items.** `OCM_SELF_OBLIGATION_REGISTRY_V2.json` files
   KS-T119 under `gap = batch 8 H2 (FDX-02)` (viability: reason-typed abstention, envelope and budget
   coordinates) but its `statement`, `proof` and `checker` describe H4's rollback classes
   (`AdoptionLedger.last_rollback`, ESI / BOI_DIVERGENT), and its status is `OPEN`. The derived registry
   keeps the id and the `OPEN` status for H2 as the registry records them; H4's content is registered
   separately as KS-T121.
2. **KS-T12 stays `OPEN` in the KSO registry although G5 proved its exact clause.** Batch 7 G5's consequence
   says "`KSO_OBLIGATION_REGISTRY_V1` entries KS-T12 and KS-T14 can move from OPEN to PROVED-with-clause";
   the lifetime registry records KS-T116 `PROVED_WITH_CLAUSE` for the KS-T14 half only, and KS-T12's row is
   unchanged. KS-T14 itself has no registry row (flagged in §3).
3. **Obligation numbering collides with theorem numbering.** Batches 10 and 11 label their runtime
   obligations H1–H8 while batch 8's theorems are H1–H4 (batch 8 and 9 label obligations by the theorem
   they follow from). The derived registry disambiguates by `source_batch`; the checker's graph excludes
   bare H-references for this reason.
4. **Status vocabulary drifts across batches.** Batches 1–7 write `PROVED (exhaustive …)`, `PROVED (policy …)`,
   `PROVED (grammar)`, `PROVED (exact)`; batches 8–11 write `PROVED (finite)`; batch 6's checker `STATUS` says
   `PROVED (finite)` for F3 and F4 where the document says `PROVED`. This map normalises to the nine-token
   vocabulary and counts the two wording differences as findings, not errors.
5. **The atlas has no section E**, and the addenda record batch 9 as §N after batch 10's §M (the two were
   written in parallel and the letter was taken). Section letters are therefore not batch order.
6. **`FRONTIER.md`'s Priority paragraph is stale**: it lists FDX-09, 10, 12 as untouched although batch 11
   wrote their dispositions (batch 11 appended dispositions without editing the paragraph). Batch 13 appends
   a closing line under Priority and does not rewrite the paragraph.
7. **The sealed foundation registry is behind the theorems.** `MACHINE_EPISTEMICS_FOUNDATION_V1.json`
   records the MEG map at the #319 freeze (its `atlas_status` counts are in the block); every one of the
   atlas' gap ids now carries at least one theorem (§6, row B). The registry is sealed by the authority
   reconciliation and is not edited; this map is the current status, the registry the frozen one.
8. **Batch 10 files an OPEN item under FDX-08 "territory"** (graded / probabilistic trust) although FDX-08
   is batch 9's row; batch 9 records that it deliberately does not enter the graded half. The open item is
   therefore listed once, under J1 (its source), and FDX-08 (I1) carries no OPEN row.
9. **Batch 12 was written on a base that predates batch 11** (its branch diff removed batch 11's files
   until it was rebased and merged as #367); its addenda section P and its `FRONTIER.md` FDX-16 disposition
   are on main, and the §1 slot is filled from its document. Batch 12's status vocabulary (PROVED /
   TIGHTENED / FINITE / CANNOT_CHECK) differs from the nine-token vocabulary of batches 1–11, so the slot is
   reported in its own vocabulary and not merged into the block's `theorems_by_status`.
10. **KS-T13 and KS-T14 are contract ids without registry rows.** The atlas files MEG-13 under
    "KS-T13 OPEN_M3 (contract §20)" and MEG-28 under "KS-T14 OPEN_M4 (contract §20)"; the KSO registry has
    KS-T12 but neither of these. The theorem sections cite KS-T14 (B7, B8, E8, G5); KS-T13 is cited only
    in the atlas. Both are flagged in the checker with the reason (§3).

## 10. Verification receipts

billy-old, `~/ocm-verify/v2-b13` (rsync of this worktree after the rebase onto main with batch 12 (#367), `.git` and
`.code-review-graph` excluded), Python 3.14.4; the OCM registries copied to `~/ocm-verify/ocm-registries/docs/theorems/`
for the live comparison; exit codes written to `~/ocm-verify/b13-run7.log` and read back, never taken from the
terminal proxy:

```text
python3 research/machine-epistemics-theory/kso_field_map_v1_exact.py --emit-derived … --snapshot-from-ocm --ocm-root ~/ocm-verify/ocm-registries   emit_rc=0   (24 rows, errors [])
python3 research/machine-epistemics-theory/kso_field_map_v1_exact.py --splice-doc --ocm-root ~/ocm-verify/ocm-registries                            splice_rc=0 (10 regions)
python3 research/machine-epistemics-theory/kso_field_map_v1_exact.py --ocm-root ~/ocm-verify/ocm-registries                                         check_rc=0  "status": "CONSISTENT", errors [], document_errors [], no_alarm_control true, 7/7 mutants caught, wall 0.39 s
python3 -m pytest -q tests/unit/test_kso_field_map_v1.py                                                                                            pytest_rc=0 12 passed, wall 0.99 s
```

The generated regions are unchanged by this section; the run recorded in the PR body re-checks the committed
file byte for byte.

## 11. Non-claims of this document

This map adds no theorem, no obligation status and no authority. It is the index of batches 1–11 in the
form the checker can re-derive; when a batch document, a checker constant or a registry row changes, the
checker fails until this document and the derived registry are regenerated. `NOVELTY NOT_ESTABLISHED`.
