# KSO language-prerequisite theorems — batch 2 (B1–B8)

Date 2026-09-05. Second one-day batch over the machine-epistemics gap atlas
(`ME_THEORY_GAP_ATLAS_V1.md`), chosen as the eight gaps the OCM M3 language milestone and the
M4 repair/consolidation work need first. Every theorem has an exact finite checker
(`kso_language_prereqs_batch2_exact.py`, stdlib only; exit 0 / 1 / 2 with 2 = CANNOT_CHECK), a
planted mutant asserted applied and caught, and a no-alarm control; tests in
`tests/unit/test_kso_language_prereqs_batch2.py` pin every count. Checker run on billy-old:
exit 0, wall 3.63 s, 12/12 tests. Objects (antichain semiring, warrant intervals, Kleene
liveness, authority meet, frozen-denominator navigation, impact cone, version spaces, typed
hypergraph fragments, DPO rewriting) are re-implemented inside the checker; nothing imports
`ocm`. NO NOVELTY OR SUPERIORITY CLAIM: every result is a corollary of KS-T01/T20/T21/T22 and the
named parents; the contribution is the exact statement and the executable falsifier.

Notation: ⊕ join (alternative), ⊗ meet (conjunction), ⟦ℓ,u⟧ warrant interval, Λ(x) the interval
of atom x, R the revoked set, LIVE/DEAD/UNKNOWN the Kleene liveness of KS-T21, Impact_R the
KS-T09 cone, `reopen`/`recheck` the KS-T22 report.

## B1 · MEG-05 · discourse-state warrant (no laundering)

**Objects.** `said(s,p)` is an OBSERVATION atom warranted by the transcript evidence alone with
authority `{speaker:1}`; `committed(s,p)` is the composition of said-atoms under KS-T20, so its
authority is the meet of its parts and `world_truth = 0`. `Λ_machine(p)` is the interval of the
machine's own atom for p, computed from the store *without* the discourse atoms unless a bridge
(an admitted machine atom whose evidence licenses p from what was said) is present.

**Theorem.** (i) For every speaker set and every composition mode (meet or join of committed
atoms), the authority of the discourse layer is bottom in the `world_truth` coordinate; ten
speakers asserting p leave `Λ_machine(p) = ⟦0, U⟧` (UNKNOWN), exactly as one speaker does.
(ii) `promote(dialogue_object, scope, bridge=None)` yields authority bottom; with a bridge the
promoted atom's *only* support is the bridge evidence, and revoking it returns the machine
interval to UNKNOWN while the said/committed atoms are unchanged (retraction is local to the
discourse layer). (iii) A bridge for p leaves an unrelated proposition q untouched.

**Proof.** (i) authority is a product lattice with missing coordinate 0 (batch-1 T1); said atoms
have no `world_truth` coordinate, and meet/join of vectors with a 0 coordinate keep 0 there
(join is not permitted to raise authority in KS-T20; the checker composes both ways to show
neither route reaches 1). (ii)–(iii) unfold the definitions: promotion is admission under the
authority meet with the bridge; its warrant is `Λ(bridge) ⊗ Λ(committed)` restricted to
machine-channel evidence, which is the bridge evidence alone. Counts: 10 speakers, 270 authority
chains, 2 composition modes bottom, retraction leaves machine unchanged 2/2. **Mutants**
`mutant_majority_promote` (k of n speakers ⇒ LIVE) and `mutant_summary_majority` (a summary
atom taking the majority authority) caught. Parent: ATMS assumption vs. justified
nodes (de Kleer 1986) and the commitment-store view of dialogue (Hamblin 1970, Walton–Krabbe
1995) — PARENT_OWNED for the objects; the authority-bottom law is KS-T20's corollary.

## B2 · MEG-12 · per-input version-space warrant

**Objects.** Finite class C, labelled examples S = {(i, y_i, e_i)} with evidence ids, VS(S) the
consistent subset. For input i, `VSW(i) = ⊕ over minimal example subsets T ⊆ S such that VS(T)
agrees at i` of `⊗_{t∈T} e_t` — the antichain of agreement sets.

**Theorem.** (i) `live(VSW(i), R) ⇔ VS(S∖R) agrees at i` (liveness equals agreement after
revocation), for every class in {AFFINE8, ALL16, MONOTONE6}, every S and every R ⊆ E.
(ii) The per-input reopening set of revoking e is `{i : VSW(i) LIVE before, DEAD after}`, and it
is contained in — usually strictly smaller than — the whole-procedure reopening. (iii) The
family warrant on a query family Q is `⊗_{i∈Q} VSW(i)`.

**Proof.** (i) is the antichain semantics of ⊕/⊗: a warrant survives R iff some agreement set
avoids R iff the surviving examples still pin the answer at i. (ii) follows from (i) pointwise.
(iii) is the definition of conjunction of per-input claims. Counts: 9 720 liveness/agreement
checks, 960 per-input reopening checks, 1 440 family = meet checks. **Mutant**
`mutant_whole_procedure_reopen` (revoking any example reopens every input) over-reopens in
840/960 cases; unrelated evidence gives no alarm in 480/480. Named witness: for AFFINE8 with the
four examples of x ↦ a⊕b, `VSW(0) = {e0} ⊕ {e1,e2,e3}` and revoking e0 reopens nothing at input 0
(the other three examples still pin it). Parent: Mitchell 1982 version spaces (PARENT_OWNED for
VS); the per-input warrant and its reopening law are new statements over KS-T21/T22.

## B3 · MEG-13 · gap-learning soundness on a finite class

**Theorem.** In the governed space (KS-S1…S7 as re-implemented), a navigation GAP with reason
TARGET_ABSENT admits only through the learning channels of the reason table (DEMONSTRATION /
INSTRUCTION / EXPERIMENTATION — never FEEDBACK); a learner proposal is admitted iff the version
space agrees on the query family Q, and the admitted atom's warrant is exactly the VSW antichain
of B2; AMBIGUOUS (no agreement) is not admitted; CONTRADICTION (inconsistent examples) is
quarantined, never averaged; FEEDBACK evidence admits nothing (weight 0); prior signatures are
preserved; after admission the target is FOUND and the genome S1/S4/S5/S6/S7 holds; a warrant
still UNKNOWN is closed by an EXPERIMENTATION query at the disagreeing input.

**Proof.** Each clause is a direct check of the corresponding rule against the AFFINE8 class
with target a⊕b: KS-T31's lifecycle plus B2's warrant. Counts: target absent then found 1,
ambiguous not admitted 1, contradiction not averaged 1, feedback admits zero 1, prior
signatures preserved 3, genome after admit all true. **Mutants** `mutant_admit_without_agreement`
and `mutant_average_contradiction` caught. MEG-12 locality is re-witnessed: `Λ(f_xor)` is LIVE
under {e0} and DEAD under {e0, e1}.

## B4 · MEG-24 · canonical meaning graph

**Theorem.** For typed hypergraph fragments with |V| ≤ 7, the exhaustive canonical form `can`
(minimum encoding over vertex orders within colour classes) satisfies `can(g₁) = can(g₂) ⇔ g₁ ≅ g₂`
(exhaustive over all 64 directed graphs on 3 vertices, 4 096 pairs, plus 40 random relabellings
of larger fragments); two parsers producing the same fragment with different vertex numbering and
edge order yield the same `can` and hence the same navigation seed (`η = seed ∘ can`, KS-T10a
consequence); beyond the bound the checker raises CANNOT_CHECK rather than returning a
possibly-colliding hash. **Mutant** `mutant_eta_wl` (seed from a WL-1 hash) is caught by the
C6 vs 2·C3 collision. Parent: canonical labelling (McKay–Piperno 2014) and the WL-1 limit
(Cai–Fürer–Immerman 1992) — PARENT_OWNED; the bounded-exact-else-CANNOT_CHECK discipline is the
OCM rule. This is the theorem `ocm.language.meaning.canonical` implements.

## B5 · MEG-03 · scope / epoch / supersession as revocation families

**Objects.** Evidence e carries a validity epoch (start, end); `R_t = {e : end(e) ≤ t}`. A scope
is an epoch interval; supersession `supersede(x, x', t)` := admit x' (evidence valid from t) +
end the conversation-scoped evidence of x at t + a SUPERSEDED_BY link that is *not* a dependency.

**Theorem.** (i) The time-indexed revocation family Γ_time = (R_t)_t is measurable w.r.t. a
partition of E into blocks iff end-epochs are block-constant (exhaustive, |E| = 4, three times:
1 215 checks). (ii) Epoch intersection is the meet of scopes (associative, commutative,
idempotent, absorbing on empty: 15 625 algebra checks). (iii) Supersession at t reopens exactly
the KS-T22 set of `R_t` — the atoms whose warrant needed x's ended evidence — and nothing else
(the Tuesday/Wednesday witness: reopen = {day_tue, plan}, unaffected = {day_wed, note,
unrelated, venue}); chained supersession is local; before t there is no alarm. **Mutant**
`mutant_stale_plan` (plan keeps consulting the superseded atom) caught. Parent: bitemporal
validity (Snodgrass 1999) for epochs — candidate parent, cited not verified here; the reopening
law is KS-T22.

## B6 · MEG-17 · repair after REOPEN

**Theorem.** On 30 random spaces with a seed→target navigation: after revoking R₁ the target
fails (30/30) while unrelated liveness and activation outside the reach of the dead atoms are
intact (30/30 each); `reinstate` (re-admitting the same evidence) restores the space *exactly*
(intervals and signatures, 30/30); `relearn` admits a live replacement under a *new* id with a
LINEAGE link, so behaviour is equal but the lifecycle differs (30/30); the work of exact repair is
bounded by the impact cone (`|touched| ≤ |Impact_{R₁}|`, 30/30). **Mutant** `mutant_global_rederivation_counted_local`
(re-derive everything, report the work as |REOPEN|) touches more atoms in 30/30. Parent: DRed / Backward-Forward incremental
maintenance (Gupta–Mumick–Subrahmanian 1993; Motik et al. 2019) — PARENT_OWNED for the bound;
reinstate-exact vs relearn-new-id is the OCM lifecycle rule (KS-T31).

## B7 · MEG-19 · consolidation locality (the provable half of KS-T12)

**Objects.** A consolidated atom m exports constituents x₁…x_k under a correspondence
`χ` (provenance map) with `Λ(m) = ⊗ Λ(x_j)` over exports; non-exported internals p_i are
reachable only through χ.

**Theorem.** (i) A change of liveness of m occurs only through an exported constituent
(exhaustive at |E| = 2 over the correspondence and two exports: 50 714 checks; content changes
transfer when the other exports are live: 1 694 checks). (ii) Content changes in non-exported
internals produce `content_recheck` (through χ) without `reopen` of m — six fixture cases
(unrelated / exported dies / middle / deep non-exported / exception / alternative-only) with the
listed reopen/recheck/content_recheck sets. (iii) Deconsolidation (undo) is recorded
PARENT_SUFFICIENT_EXPECTED, not claimed. **Mutants** `mutant_equal_by_liveness` (treat equal
liveness as equal content) and `mutant_recheck_only_on_liveness_change` (drop χ-content rechecks)
caught. Parent: the improvement half of KS-T12 remains OPEN.

## B8 · MEG-28 · Jump preservation as a DPO rewrite

**Theorem.** On the M4 Boolean fixture (features 1, a, b, ab): AND ∉ XOR-span{1,a,b} (parity) and
AND ∈ span{1,a,b,ab}, so the expressive ceiling is exact (affine span 8, quadratic span 16); the
Jump is a double-pushout rewrite L ← I → R whose interface I fixes every atom's interval and
signature (18 preserved), the old eight-function repertoire is byte-identical after the rewrite,
dangling edges are refused, an interface-attribute change is refused, one-hop reopening (`mutant_one_hop_reopening`) is
caught, adoption is refused four ways (no trigger / no external commit / wrong level / stale
signature), the reopening set is the seven listed atoms, and rollback (revoke + quarantine, batch-1
T4) is exact. The *improvement* half of KS-T14 stays OPEN. Parent: DPO graph transformation
(Ehrig et al. 2006) — PARENT_OWNED for preservation; the OCM contribution is the M4 fixture
binding.

## Consequences for the OCM build

* M3: `said`/`committed` records and the authority-bottom promotion rule (B1) are implemented as
  `ocm.language.interpret.SaidRecord`/`promote_authority`; B2/B3 are the acquisition contract of
  `ocm.language.acquisition`; B4 is `ocm.language.meaning.canonical`.
* M2: scope/epoch (B5) matches `ocm.kso.types.Scope`; repair (B6) and consolidation (B7) are the
  M4 obligations with their falsifiers ready.
* Open after this batch: MEG-02 (graded half), MEG-09, MEG-23, MEG-27, MEG-34, and the
  improvement halves of KS-T12/T14.
