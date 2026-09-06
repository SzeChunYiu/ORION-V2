import KsoCore.Interval

/-!
# Revocation monotonicity and the reopening cone (KS-T22 / KS-T09 / KS-T18 shapes)

* `lam_antitone` — revoking more never revives: `R ⊆ R' → λ_{R'} ≤₃ λ_R` (batch 10 J1 (i)).
* `lam_ne_LIVE_of_lower_hit` / `lam_DEAD_of_upper_hit` — an atom whose exhibited supports are all
  revoked is DEAD or UNKNOWN, never LIVE; if every possible support is revoked it is DEAD.
* `lam_zero_DEAD` — the certified-zero interval is DEAD under every revocation (KS-T18 corollary).
* `reach` — the dependency closure with a fuel bound (OCM `revocation.impact_cone` iterates the same
  successor step to a fixed point).  It is extensive, monotone in the seed and distributes over
  unions; the non-LIVE seed set grows with `R`, so the cone never shrinks under more revocation.

Not mechanised (finitely checked by OCM `check_impact_and_reopening`): that the fuel-bounded closure
with fuel `≥ |V|` is the *least* dependency-closed superset (needs a pigeonhole argument on the
finite vertex list), and the REOPEN / RECHECK / UNAFFECTED partition of KS-T22 on the eight-atom
witness.
-/

namespace KsoCore

open Liveness

variable {E : Type}

/-- `R ⊆ R'` on revocation indicators. -/
def Subrev (R R' : Revocation E) : Prop := ∀ e, R e = true → R' e = true

theorem avoids_antitone {R R' : Revocation E} (h : Subrev R R') (W : Warrant E) :
    avoids W R' = true → avoids W R = true := by
  intro ha
  rw [avoids_iff] at ha ⊢
  intro e he
  cases hr : R e
  · rfl
  · have := h e hr
    rw [ha e he] at this
    exact absurd this (by decide)

/-- `ℓ_R` is antitone in `R`. -/
theorem live_antitone {R R' : Revocation E} (h : Subrev R R') (P : Profile E) :
    live P R' = true → live P R = true := by
  intro hl
  obtain ⟨W, hW, hWa⟩ := (live_iff P R').mp hl
  exact (live_iff P R).mpr ⟨W, hW, avoids_antitone h W hWa⟩

/-- Revoking more never revives: `R ⊆ R' → λ_{R'}⟦L,U⟧ ≤₃ λ_R⟦L,U⟧`. -/
theorem lam_antitone {R R' : Revocation E} (h : Subrev R R') (I : Interval E) :
    lam I R' ≤ lam I R := by
  have hl := live_antitone h I.lower
  have hu := live_antitone h I.upper
  have hI := I.wf R
  have hI' := I.wf R'
  simp only [lam]
  cases h1 : live I.lower R' <;> cases h2 : live I.upper R' <;>
    cases h3 : live I.lower R <;> cases h4 : live I.upper R <;> simp_all <;> decide

/-- Once non-LIVE, an atom stays non-LIVE under any larger revocation. -/
theorem nonLive_mono {R R' : Revocation E} (h : Subrev R R') (I : Interval E) :
    lam I R ≠ LIVE → lam I R' ≠ LIVE := by
  intro hne hL
  have := lam_antitone h I
  rw [hL] at this
  exact hne ((LIVE_le_iff _).mp this)

/-- Once DEAD, an atom stays DEAD under any larger revocation. -/
theorem DEAD_mono {R R' : Revocation E} (h : Subrev R R') (I : Interval E) :
    lam I R = DEAD → lam I R' = DEAD := by
  intro hD
  have := lam_antitone h I
  rw [hD] at this
  exact (le_DEAD_iff _).mp this

/-! ## Revoked support -/

/-- If every exhibited warrant is hit by `R`, the atom is DEAD or UNKNOWN — never LIVE. -/
theorem lam_ne_LIVE_of_lower_hit (I : Interval E) (R : Revocation E)
    (h : ∀ W, W ∈ I.lower → ∃ e, e ∈ W ∧ R e = true) : lam I R ≠ LIVE := by
  intro hL
  have := (lam_eq_LIVE_iff I R).mp hL
  rw [(live_eq_false_iff I.lower R).mpr h] at this
  exact absurd this (by decide)

/-- If every possible warrant is hit by `R`, the atom is DEAD. -/
theorem lam_DEAD_of_upper_hit (I : Interval E) (R : Revocation E)
    (h : ∀ W, W ∈ I.upper → ∃ e, e ∈ W ∧ R e = true) : lam I R = DEAD :=
  (lam_eq_DEAD_iff I R).mpr ((live_eq_false_iff I.upper R).mpr h)

/-- A single evidence id shared by every exhibited warrant kills liveness when revoked. -/
theorem lam_ne_LIVE_of_common_evidence (I : Interval E) (R : Revocation E) (e : E)
    (he : ∀ W, W ∈ I.lower → e ∈ W) (hr : R e = true) : lam I R ≠ LIVE :=
  lam_ne_LIVE_of_lower_hit I R (fun W hW => ⟨e, he W hW, hr⟩)

/-- KS-T18 corollary: the certified-zero interval (FEEDBACK atoms) is DEAD under every `R`. -/
theorem lam_zero_DEAD (R : Revocation E) : lam (Interval.zero : Interval E) R = DEAD := rfl

/-- The certified-one interval is LIVE under every `R` (nothing to revoke). -/
theorem lam_one_LIVE (R : Revocation E) : lam (Interval.one : Interval E) R = LIVE := rfl

/-! ## The dependency closure (impact cone) -/

section Cone

variable {V : Type}

/-- Successors of every vertex in a list. -/
def succs (dep : V → List V) : List V → List V
  | [] => []
  | v :: C => dep v ++ succs dep C

/-- One closure step: `C ∪ {u : ∃ v ∈ C, u ∈ dep v}` (OCM `impact_cone` body). -/
def step (dep : V → List V) (C : List V) : List V := C ++ succs dep C

/-- The fuel-bounded closure `Impact_D`. -/
def reach (dep : V → List V) : Nat → List V → List V
  | 0, C => C
  | n + 1, C => reach dep n (step dep C)

theorem mem_succs (dep : V → List V) (C : List V) (u : V) :
    u ∈ succs dep C ↔ ∃ v, v ∈ C ∧ u ∈ dep v := by
  induction C with
  | nil => simp [succs]
  | cons v C ih =>
    simp only [succs, List.mem_append, ih, List.mem_cons]
    constructor
    · rintro (h | ⟨w, hw, hu⟩)
      · exact ⟨v, Or.inl rfl, h⟩
      · exact ⟨w, Or.inr hw, hu⟩
    · rintro ⟨w, hw | hw, hu⟩
      · subst hw
        exact Or.inl hu
      · exact Or.inr ⟨w, hw, hu⟩

theorem succs_append (dep : V → List V) (C₁ C₂ : List V) :
    succs dep (C₁ ++ C₂) = succs dep C₁ ++ succs dep C₂ := by
  induction C₁ with
  | nil => simp [succs]
  | cons v C ih => simp [succs, ih, List.append_assoc]

theorem mem_step_of_mem (dep : V → List V) {C : List V} {v : V} (h : v ∈ C) : v ∈ step dep C :=
  List.mem_append.mpr (Or.inl h)

theorem step_mono (dep : V → List V) {C C' : List V} (h : ∀ v, v ∈ C → v ∈ C') :
    ∀ v, v ∈ step dep C → v ∈ step dep C' := by
  intro v hv
  rcases List.mem_append.mp hv with hv | hv
  · exact List.mem_append.mpr (Or.inl (h v hv))
  · obtain ⟨w, hw, hvw⟩ := (mem_succs dep C v).mp hv
    exact List.mem_append.mpr (Or.inr ((mem_succs dep C' v).mpr ⟨w, h w hw, hvw⟩))

/-- The cone contains its seed. -/
theorem reach_extensive (dep : V → List V) (n : Nat) :
    ∀ (C : List V) (v : V), v ∈ C → v ∈ reach dep n C := by
  induction n with
  | zero => intro C v h; exact h
  | succ n ih => intro C v h; exact ih (step dep C) v (mem_step_of_mem dep h)

/-- The cone is monotone in its seed (more changed atoms, larger cone). -/
theorem reach_mono (dep : V → List V) (n : Nat) :
    ∀ (C C' : List V), (∀ v, v ∈ C → v ∈ C') → ∀ v, v ∈ reach dep n C → v ∈ reach dep n C' := by
  induction n with
  | zero => intro C C' h v hv; exact h v hv
  | succ n ih => intro C C' h v hv; exact ih (step dep C) (step dep C') (step_mono dep h) v hv

theorem reach_congr (dep : V → List V) (n : Nat) {C C' : List V}
    (h : ∀ v, v ∈ C ↔ v ∈ C') (v : V) : v ∈ reach dep n C ↔ v ∈ reach dep n C' :=
  ⟨reach_mono dep n C C' (fun w hw => (h w).mp hw) v,
   reach_mono dep n C' C (fun w hw => (h w).mpr hw) v⟩

theorem mem_step_append (dep : V → List V) (C₁ C₂ : List V) (v : V) :
    v ∈ step dep (C₁ ++ C₂) ↔ v ∈ step dep C₁ ++ step dep C₂ := by
  simp only [step, succs_append, List.mem_append]
  constructor
  · rintro ((h | h) | (h | h))
    · exact Or.inl (Or.inl h)
    · exact Or.inr (Or.inl h)
    · exact Or.inl (Or.inr h)
    · exact Or.inr (Or.inr h)
  · rintro ((h | h) | (h | h))
    · exact Or.inl (Or.inl h)
    · exact Or.inr (Or.inl h)
    · exact Or.inl (Or.inr h)
    · exact Or.inr (Or.inr h)

/-- `Impact_D(S₁ ∪ S₂) = Impact_D(S₁) ∪ Impact_D(S₂)` (batch 10 J1 (vii), 4 096 finite checks). -/
theorem reach_union (dep : V → List V) (n : Nat) :
    ∀ (C₁ C₂ : List V) (v : V),
      v ∈ reach dep n (C₁ ++ C₂) ↔ v ∈ reach dep n C₁ ∨ v ∈ reach dep n C₂ := by
  induction n with
  | zero => intro C₁ C₂ v; exact List.mem_append
  | succ n ih =>
    intro C₁ C₂ v
    simp only [reach]
    rw [reach_congr dep n (mem_step_append dep C₁ C₂) v]
    exact ih (step dep C₁) (step dep C₂) v

/-- The cone of an empty seed is empty (irrelevant revocation reopens nothing, KS-T22 (3)). -/
theorem reach_nil (dep : V → List V) (n : Nat) : reach dep n [] = [] := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [reach, step, succs, List.append_nil]; exact ih

end Cone

/-! ## The non-LIVE seed grows with `R`, so the cone never shrinks -/

section Dead

variable {V : Type}

/-- Atoms of `atoms` that are not LIVE under `R` (the seed `D_R` of `Reach(D_R)`). -/
def deadSet (atoms : List V) (ival : V → Interval E) (R : Revocation E) : List V :=
  atoms.filter (fun v => decide (lam (ival v) R ≠ LIVE))

theorem mem_deadSet {atoms : List V} {ival : V → Interval E} {R : Revocation E} {v : V} :
    v ∈ deadSet atoms ival R ↔ v ∈ atoms ∧ lam (ival v) R ≠ LIVE := by
  simp [deadSet, List.mem_filter]

theorem deadSet_mono {atoms : List V} {ival : V → Interval E} {R R' : Revocation E}
    (h : Subrev R R') : ∀ v, v ∈ deadSet atoms ival R → v ∈ deadSet atoms ival R' := by
  intro v hv
  obtain ⟨ha, hne⟩ := mem_deadSet.mp hv
  exact mem_deadSet.mpr ⟨ha, nonLive_mono h (ival v) hne⟩

/-- Revoking more never revives: `R ⊆ R' → Reach(D_R) ⊆ Reach(D_{R'})`. -/
theorem reachDead_mono (dep : V → List V) (n : Nat) {atoms : List V} {ival : V → Interval E}
    {R R' : Revocation E} (h : Subrev R R') :
    ∀ v, v ∈ reach dep n (deadSet atoms ival R) → v ∈ reach dep n (deadSet atoms ival R') :=
  reach_mono dep n _ _ (deadSet_mono h)

/-- The liveness-changed set `C(Δ)` of a revocation delta `R₀ → R₁`. -/
def changedSet (atoms : List V) (ival : V → Interval E) (R₀ R₁ : Revocation E) : List V :=
  atoms.filter (fun v => decide (lam (ival v) R₀ ≠ lam (ival v) R₁))

theorem mem_changedSet {atoms : List V} {ival : V → Interval E} {R₀ R₁ : Revocation E} {v : V} :
    v ∈ changedSet atoms ival R₀ R₁ ↔ v ∈ atoms ∧ lam (ival v) R₀ ≠ lam (ival v) R₁ := by
  simp [changedSet, List.mem_filter]

/-- KS-T22 (1), first half: every atom whose liveness changed lies in the cone. -/
theorem changed_sub_cone (dep : V → List V) (n : Nat) {atoms : List V} {ival : V → Interval E}
    {R₀ R₁ : Revocation E} (v : V) (hv : v ∈ atoms) (hc : lam (ival v) R₀ ≠ lam (ival v) R₁) :
    v ∈ reach dep n (changedSet atoms ival R₀ R₁) :=
  reach_extensive dep n _ v (mem_changedSet.mpr ⟨hv, hc⟩)

/-- KS-T22 (2), first half (no-alarm): an atom outside the cone did not change liveness. -/
theorem unaffected_unchanged (dep : V → List V) (n : Nat) {atoms : List V} {ival : V → Interval E}
    {R₀ R₁ : Revocation E} (v : V) (hv : v ∈ atoms)
    (hout : v ∉ reach dep n (changedSet atoms ival R₀ R₁)) : lam (ival v) R₀ = lam (ival v) R₁ := by
  apply Classical.byContradiction
  intro hc
  exact hout (changed_sub_cone dep n v hv hc)

/-- KS-T22 (3), irrelevant revocation: nothing changed ⇒ the cone is empty. -/
theorem cone_nil_of_unchanged (dep : V → List V) (n : Nat) {atoms : List V} {ival : V → Interval E}
    {R₀ R₁ : Revocation E} (h : ∀ v, v ∈ atoms → lam (ival v) R₀ = lam (ival v) R₁) :
    reach dep n (changedSet atoms ival R₀ R₁) = [] := by
  have hc : changedSet atoms ival R₀ R₁ = [] := by
    apply List.eq_nil_iff_forall_not_mem.mpr
    intro v hv
    obtain ⟨ha, hne⟩ := mem_changedSet.mp hv
    exact hne (h v ha)
  rw [hc, reach_nil]

end Dead

end KsoCore
