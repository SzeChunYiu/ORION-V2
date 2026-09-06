/-!
# Warrant profiles: the antichain semiring read through its liveness function

OCM `src/ocm/kso/warrant.py` stores a profile as a canonical antichain (`canon`) and defines

* `live(P, R)  = any(not (W & R) for W in P)`          (two-valued `ℓ_R`),
* `join(P, Q)  = canon(P ∪ Q)`                          (`⊕`, alternative support),
* `meet(P, Q)  = canon({a ∪ b | a ∈ P, b ∈ Q})`         (`⊗`, conjunctive support),
* `leq(P, Q)   = ∀ W ∈ P, ∃ V ∈ Q, V ⊆ W`               (semiring order `f_P ≤ f_Q`).

Here a profile is a plain list of warrants (lists of evidence ids) and the algebra is stated on
the *liveness function* `R ↦ live P R`, which is exactly the monotone Boolean function `f_P` of
KS-T01.  Canonicalisation is therefore not needed: two lists with the same liveness function are
the same profile (`Equiv`), and the theory's order `P ≤ Q ⇔ f_P ≤ f_Q` is `Leq`.  Theorems
`leq_of_synLeq` / `synLeq_of_leq` prove that OCM's syntactic `leq` and the semantic order coincide,
so nothing is lost by the change of representative.

What is *not* mechanised: that `canon` returns a unique antichain representative of each `Equiv`
class (Dedekind / free distributive lattice).  That is finitely checked by OCM `check_semiring`
(exhaustive at `n = 3`) and recorded as such in the batch document.
-/

namespace KsoCore

variable {E : Type}

/-- A warrant: a finite set of evidence ids, represented as a list. -/
abbrev Warrant (E : Type) := List E

/-- A profile: a finite family of warrants (OCM antichain `Profile`, up to canonicalisation). -/
abbrev Profile (E : Type) := List (Warrant E)

/-- A revocation set `R ⊆ E` as its indicator. -/
abbrev Revocation (E : Type) := E → Bool

/-- `W ∩ R = ∅`. -/
def avoids : Warrant E → Revocation E → Bool
  | [], _ => true
  | e :: W, R => (!R e) && avoids W R

/-- Two-valued liveness `ℓ_R(P) = 1 ⇔ ∃ W ∈ P, W ∩ R = ∅` (OCM `live`). -/
def live : Profile E → Revocation E → Bool
  | [], _ => false
  | W :: P, R => avoids W R || live P R

/-- OCM `ZERO = ()`: no sufficient warrant at all. -/
def zero : Profile E := []

/-- OCM `ONE = (∅,)`: unconditionally warranted. -/
def one : Profile E := [[]]

/-- `P ⊕ Q` — alternative support (OCM `join`, before canonicalisation). -/
def join (P Q : Profile E) : Profile E := P ++ Q

/-- `P ⊗ Q` — conjunctive support (OCM `meet`, before canonicalisation). -/
def meet : Profile E → Profile E → Profile E
  | [], _ => []
  | W :: P, Q => Q.map (fun V => W ++ V) ++ meet P Q

/-! ## Characterisations -/

theorem avoids_iff (W : Warrant E) (R : Revocation E) :
    avoids W R = true ↔ ∀ e, e ∈ W → R e = false := by
  induction W with
  | nil => simp [avoids]
  | cons a W ih =>
    simp only [avoids, Bool.and_eq_true, ih]
    constructor
    · intro h e he
      rcases List.mem_cons.mp he with h1 | h1
      · subst h1
        revert h
        cases R e <;> simp
      · exact h.2 e h1
    · intro h
      refine ⟨?_, fun e he => h e (by simp [he])⟩
      have := h a (by simp)
      rw [this]
      rfl

theorem live_iff (P : Profile E) (R : Revocation E) :
    live P R = true ↔ ∃ W, W ∈ P ∧ avoids W R = true := by
  induction P with
  | nil => simp [live]
  | cons W P ih =>
    simp only [live, Bool.or_eq_true, ih]
    constructor
    · rintro (h | ⟨V, hV, hVa⟩)
      · exact ⟨W, by simp, h⟩
      · exact ⟨V, by simp [hV], hVa⟩
    · rintro ⟨V, hV, hVa⟩
      rcases List.mem_cons.mp hV with rfl | hV'
      · exact Or.inl hVa
      · exact Or.inr ⟨V, hV', hVa⟩

/-- A profile is dead under `R` exactly when every warrant is hit by `R`. -/
theorem live_eq_false_iff (P : Profile E) (R : Revocation E) :
    live P R = false ↔ ∀ W, W ∈ P → ∃ e, e ∈ W ∧ R e = true := by
  constructor
  · intro h W hW
    apply Classical.byContradiction
    intro hne
    have hav : avoids W R = true := by
      rw [avoids_iff]
      intro e he
      cases hr : R e
      · rfl
      · exact absurd ⟨e, he, hr⟩ hne
    have := (live_iff P R).mpr ⟨W, hW, hav⟩
    rw [h] at this
    exact absurd this (by decide)
  · intro h
    cases hl : live P R
    · rfl
    · obtain ⟨W, hW, hWa⟩ := (live_iff P R).mp hl
      obtain ⟨e, he, hr⟩ := h W hW
      have := (avoids_iff W R).mp hWa e he
      rw [hr] at this
      exact absurd this (by decide)

/-! ## The liveness homomorphism (KS-T01 in Boolean-function form) -/

theorem avoids_append (W V : Warrant E) (R : Revocation E) :
    avoids (W ++ V) R = (avoids W R && avoids V R) := by
  induction W with
  | nil => simp [avoids]
  | cons e W ih => simp [avoids, ih, Bool.and_assoc]

theorem live_append (P Q : Profile E) (R : Revocation E) :
    live (P ++ Q) R = (live P R || live Q R) := by
  induction P with
  | nil => simp [live]
  | cons W P ih => simp [live, ih, Bool.or_assoc]

/-- `ℓ_R(P ⊕ Q) = ℓ_R(P) ∨ ℓ_R(Q)`. -/
theorem live_join (P Q : Profile E) (R : Revocation E) :
    live (join P Q) R = (live P R || live Q R) := live_append P Q R

theorem live_map_prepend (W : Warrant E) (Q : Profile E) (R : Revocation E) :
    live (Q.map (fun V => W ++ V)) R = (avoids W R && live Q R) := by
  induction Q with
  | nil => simp [live]
  | cons V Q ih =>
    simp only [List.map_cons, live, ih, avoids_append]
    cases avoids W R <;> cases avoids V R <;> cases live Q R <;> rfl

/-- `ℓ_R(P ⊗ Q) = ℓ_R(P) ∧ ℓ_R(Q)`: a union `W ∪ V` avoids `R` iff both parts do. -/
theorem live_meet (P Q : Profile E) (R : Revocation E) :
    live (meet P Q) R = (live P R && live Q R) := by
  induction P with
  | nil => simp [meet, live]
  | cons W P ih =>
    simp only [meet, live_append, live_map_prepend, ih, live]
    cases avoids W R <;> cases live P R <;> cases live Q R <;> rfl

theorem live_zero (R : Revocation E) : live (zero : Profile E) R = false := rfl

theorem live_one (R : Revocation E) : live (one : Profile E) R = true := rfl

/-! ## Semantic order and equivalence -/

/-- `P ≤ Q ⇔ f_P ≤ f_Q` (the theory's order; `Q` is at least as easy to satisfy). -/
def Leq (P Q : Profile E) : Prop := ∀ R : Revocation E, live P R = true → live Q R = true

/-- Same liveness function: the same element of the antichain semiring. -/
def Equiv (P Q : Profile E) : Prop := ∀ R : Revocation E, live P R = live Q R

theorem Leq.refl (P : Profile E) : Leq P P := fun _ h => h

theorem Leq.trans {P Q S : Profile E} (h1 : Leq P Q) (h2 : Leq Q S) : Leq P S :=
  fun R h => h2 R (h1 R h)

theorem Equiv.refl (P : Profile E) : Equiv P P := fun _ => rfl

theorem Equiv.symm {P Q : Profile E} (h : Equiv P Q) : Equiv Q P := fun R => (h R).symm

theorem Equiv.trans {P Q S : Profile E} (h1 : Equiv P Q) (h2 : Equiv Q S) : Equiv P S :=
  fun R => (h1 R).trans (h2 R)

theorem Equiv.leq {P Q : Profile E} (h : Equiv P Q) : Leq P Q := fun R hp => (h R) ▸ hp

theorem Leq.antisymm {P Q : Profile E} (h1 : Leq P Q) (h2 : Leq Q P) : Equiv P Q := by
  intro R
  cases hp : live P R <;> cases hq : live Q R
  · rfl
  · exact (h2 R hq).symm.trans hp |>.symm ▸ rfl
  · exact ((h1 R hp).symm.trans hq).symm ▸ rfl
  · rfl

theorem zero_leq (P : Profile E) : Leq zero P := fun R h => by
  rw [live_zero] at h
  exact absurd h (by decide)

theorem leq_one (P : Profile E) : Leq P one := fun R _ => live_one R

/-! ## Semiring laws, stated on the liveness function (KS-T01) -/

theorem join_comm (P Q : Profile E) : Equiv (join P Q) (join Q P) := fun R => by
  simp only [live_join, Bool.or_comm]

theorem join_assoc (P Q S : Profile E) : Equiv (join (join P Q) S) (join P (join Q S)) := fun R => by
  simp only [live_join, Bool.or_assoc]

theorem join_idem (P : Profile E) : Equiv (join P P) P := fun R => by
  simp only [live_join, Bool.or_self]

theorem join_zero (P : Profile E) : Equiv (join P zero) P := fun R => by
  simp only [live_join, live_zero, Bool.or_false]

theorem meet_comm (P Q : Profile E) : Equiv (meet P Q) (meet Q P) := fun R => by
  simp only [live_meet, Bool.and_comm]

theorem meet_assoc (P Q S : Profile E) : Equiv (meet (meet P Q) S) (meet P (meet Q S)) := fun R => by
  simp only [live_meet, Bool.and_assoc]

theorem meet_idem (P : Profile E) : Equiv (meet P P) P := fun R => by
  simp only [live_meet, Bool.and_self]

theorem meet_one (P : Profile E) : Equiv (meet P one) P := fun R => by
  simp only [live_meet, live_one, Bool.and_true]

theorem meet_zero (P : Profile E) : Equiv (meet P zero) zero := fun R => by
  simp only [live_meet, live_zero, Bool.and_false]

theorem meet_join_distrib (P Q S : Profile E) :
    Equiv (meet P (join Q S)) (join (meet P Q) (meet P S)) := fun R => by
  simp only [live_meet, live_join]
  cases live P R <;> cases live Q R <;> cases live S R <;> rfl

/-- `⊗` is the meet of the order: `P ⊗ Q ≤ P`. -/
theorem meet_leq_left (P Q : Profile E) : Leq (meet P Q) P := fun R h => by
  rw [live_meet, Bool.and_eq_true] at h
  exact h.1

theorem meet_leq_right (P Q : Profile E) : Leq (meet P Q) Q := fun R h => by
  rw [live_meet, Bool.and_eq_true] at h
  exact h.2

/-- `⊕` is the join of the order: `P ≤ P ⊕ Q`. -/
theorem leq_join_left (P Q : Profile E) : Leq P (join P Q) := fun R h => by
  rw [live_join, h]
  rfl

theorem leq_join_right (P Q : Profile E) : Leq Q (join P Q) := fun R h => by
  rw [live_join, h]
  simp

/-! ## Monotonicity of `⊕` and `⊗` in each argument (Definition 1.3's well-definedness) -/

theorem join_mono {P P' Q Q' : Profile E} (h1 : Leq P P') (h2 : Leq Q Q') :
    Leq (join P Q) (join P' Q') := by
  intro R h
  rw [live_join] at h ⊢
  rw [Bool.or_eq_true] at h
  rcases h with h | h
  · rw [h1 R h]
    rfl
  · rw [h2 R h]
    simp

theorem meet_mono {P P' Q Q' : Profile E} (h1 : Leq P P') (h2 : Leq Q Q') :
    Leq (meet P Q) (meet P' Q') := by
  intro R h
  rw [live_meet] at h ⊢
  rw [Bool.and_eq_true] at h
  obtain ⟨ha, hb⟩ := h
  rw [h1 R ha, h2 R hb]
  rfl

theorem join_mono_left {P P' : Profile E} (Q : Profile E) (h : Leq P P') :
    Leq (join P Q) (join P' Q) := join_mono h (Leq.refl Q)

theorem join_mono_right (P : Profile E) {Q Q' : Profile E} (h : Leq Q Q') :
    Leq (join P Q) (join P Q') := join_mono (Leq.refl P) h

theorem meet_mono_left {P P' : Profile E} (Q : Profile E) (h : Leq P P') :
    Leq (meet P Q) (meet P' Q) := meet_mono h (Leq.refl Q)

theorem meet_mono_right (P : Profile E) {Q Q' : Profile E} (h : Leq Q Q') :
    Leq (meet P Q) (meet P Q') := meet_mono (Leq.refl P) h

/-! ## OCM's syntactic order coincides with the semantic one -/

/-- `V ⊆ W` on warrants. -/
def Subwarrant (V W : Warrant E) : Prop := ∀ e, e ∈ V → e ∈ W

/-- OCM `leq(lower, upper)`: every warrant of `P` contains some warrant of `Q`. -/
def SynLeq (P Q : Profile E) : Prop := ∀ W, W ∈ P → ∃ V, V ∈ Q ∧ Subwarrant V W

theorem leq_of_synLeq {P Q : Profile E} (h : SynLeq P Q) : Leq P Q := by
  intro R hP
  obtain ⟨W, hW, hWa⟩ := (live_iff P R).mp hP
  obtain ⟨V, hV, hVW⟩ := h W hW
  refine (live_iff Q R).mpr ⟨V, hV, ?_⟩
  exact (avoids_iff V R).mpr fun e he => (avoids_iff W R).mp hWa e (hVW e he)

/-- The revocation that revokes exactly the evidence outside `W`. -/
def complementOf [DecidableEq E] (W : Warrant E) : Revocation E := fun e => !(decide (e ∈ W))

theorem synLeq_of_leq [DecidableEq E] {P Q : Profile E} (h : Leq P Q) : SynLeq P Q := by
  intro W hW
  have hWa : avoids W (complementOf W) = true :=
    (avoids_iff W _).mpr (fun e he => by simp [complementOf, he])
  have hQ := h (complementOf W) ((live_iff P _).mpr ⟨W, hW, hWa⟩)
  obtain ⟨V, hV, hVa⟩ := (live_iff Q _).mp hQ
  refine ⟨V, hV, fun e he => ?_⟩
  have := (avoids_iff V _).mp hVa e he
  simpa [complementOf] using this

theorem synLeq_iff_leq [DecidableEq E] (P Q : Profile E) : SynLeq P Q ↔ Leq P Q :=
  ⟨leq_of_synLeq, synLeq_of_leq⟩

end KsoCore
