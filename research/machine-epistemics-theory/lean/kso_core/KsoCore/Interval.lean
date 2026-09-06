import KsoCore.Liveness
import KsoCore.Profile

/-!
# Warrant intervals `⟦L, U⟧` and three-valued liveness (KS-T21)

OCM `warrant.WarrantProfile(lower, upper)` requires `leq(lower, upper)` and defines

    liveness(R) = LIVE if live(lower, R) else (DEAD if not live(upper, R) else UNKNOWN)

with `join`/`meet` component-wise.  `Interval` carries the order constraint as a proof field, so
every interval built by `oplus` / `otimes` is well-formed by construction (Definition 1.3 of
`KSO_THREE_VALUED_WARRANT_AND_REOPENING_V1.md`).  `lam` is `λ_R`.
-/

namespace KsoCore

open Liveness

variable {E : Type}

/-- A warrant interval `⟦lower, upper⟧` with `lower ≤ upper` (Definition 1.1). -/
structure Interval (E : Type) where
  lower : Profile E
  upper : Profile E
  wf : Leq lower upper

namespace Interval

/-- `⟦P, P⟧` — certified (OCM `WarrantProfile.certified`). -/
def certified (P : Profile E) : Interval E := ⟨P, P, Leq.refl P⟩

/-- `⟦P, 1⟧` — partial (OCM `WarrantProfile.partial`). -/
def partialIv (P : Profile E) : Interval E := ⟨P, one, leq_one P⟩

/-- `⟦0, 0⟧` — certified-unwarranted (FEEDBACK atoms, KS-T18). -/
def zero : Interval E := certified KsoCore.zero

/-- `⟦1, 1⟧`. -/
def one : Interval E := certified KsoCore.one

/-- OCM `complete`: lower and upper are the same profile (up to representative). -/
def Certified (I : Interval E) : Prop := Equiv I.lower I.upper

/-- `J` refines `I`: `L_I ≤ L_J` and `U_J ≤ U_I` (KS-T21 (b), T10). -/
def Refines (J I : Interval E) : Prop := Leq I.lower J.lower ∧ Leq J.upper I.upper

/-- `⟦L,U⟧ ⊕ ⟦L',U'⟧ = ⟦L ⊕ L', U ⊕ U'⟧`, well-formed by `join_mono`. -/
def oplus (I J : Interval E) : Interval E :=
  ⟨join I.lower J.lower, join I.upper J.upper, join_mono I.wf J.wf⟩

/-- `⟦L,U⟧ ⊗ ⟦L',U'⟧ = ⟦L ⊗ L', U ⊗ U'⟧`, well-formed by `meet_mono`. -/
def otimes (I J : Interval E) : Interval E :=
  ⟨meet I.lower J.lower, meet I.upper J.upper, meet_mono I.wf J.wf⟩

end Interval

/-- Three-valued liveness `λ_R⟦L,U⟧` (Definition 1.2; OCM `WarrantProfile.liveness`). -/
def lam (I : Interval E) (R : Revocation E) : Liveness :=
  if live I.lower R then LIVE else if live I.upper R then UNKNOWN else DEAD

/-! ## Basic case facts -/

theorem lam_eq_LIVE_iff (I : Interval E) (R : Revocation E) :
    lam I R = LIVE ↔ live I.lower R = true := by
  unfold lam
  cases live I.lower R <;> cases live I.upper R <;> simp

theorem lam_eq_DEAD_iff (I : Interval E) (R : Revocation E) :
    lam I R = DEAD ↔ live I.upper R = false := by
  have hw := I.wf R
  unfold lam
  cases h1 : live I.lower R <;> cases h2 : live I.upper R <;> simp_all

theorem lam_eq_UNKNOWN_iff (I : Interval E) (R : Revocation E) :
    lam I R = UNKNOWN ↔ live I.lower R = false ∧ live I.upper R = true := by
  unfold lam
  cases live I.lower R <;> cases live I.upper R <;> simp

/-! ## KS-T21: `λ_R` is a Kleene homomorphism -/

/-- `λ_R(P ⊗ Q) = λ_R(P) ∧₃ λ_R(Q)`. -/
theorem lam_otimes (I J : Interval E) (R : Revocation E) :
    lam (Interval.otimes I J) R = kand (lam I R) (lam J R) := by
  have hI := I.wf R
  have hJ := J.wf R
  simp only [lam, Interval.otimes, live_meet]
  cases h1 : live I.lower R <;> cases h2 : live I.upper R <;>
    cases h3 : live J.lower R <;> cases h4 : live J.upper R <;> simp_all [kand]

/-- `λ_R(P ⊕ Q) = λ_R(P) ∨₃ λ_R(Q)`. -/
theorem lam_oplus (I J : Interval E) (R : Revocation E) :
    lam (Interval.oplus I J) R = kor (lam I R) (lam J R) := by
  have hI := I.wf R
  have hJ := J.wf R
  simp only [lam, Interval.oplus, live_join]
  cases h1 : live I.lower R <;> cases h2 : live I.upper R <;>
    cases h3 : live J.lower R <;> cases h4 : live J.upper R <;> simp_all [kor]

/-- KS-T21 (a), reduction: a certified interval is never UNKNOWN … -/
theorem lam_certified_ne_UNKNOWN (I : Interval E) (hc : I.Certified) (R : Revocation E) :
    lam I R ≠ UNKNOWN := by
  intro h
  obtain ⟨h1, h2⟩ := (lam_eq_UNKNOWN_iff I R).mp h
  have := hc R
  rw [h1, h2] at this
  exact absurd this (by decide)

/-- … and agrees with the two-valued `ℓ_R`. -/
theorem lam_certified_eq (P : Profile E) (R : Revocation E) :
    lam (Interval.certified P) R = (if live P R then LIVE else DEAD) := by
  show (if live P R then LIVE else if live P R then UNKNOWN else DEAD) = (if live P R then LIVE else DEAD)
  cases live P R <;> rfl

/-- KS-T21 (b), refinement monotonicity: refining can only move UNKNOWN. -/
theorem lam_refines {I J : Interval E} (h : J.Refines I) (R : Revocation E)
    (hne : lam I R ≠ UNKNOWN) : lam J R = lam I R := by
  obtain ⟨hl, hu⟩ := h
  have hlR := hl R
  have huR := hu R
  have hI := I.wf R
  have hJ := J.wf R
  simp only [lam] at hne ⊢
  cases h1 : live I.lower R <;> cases h2 : live I.upper R <;>
    cases h3 : live J.lower R <;> cases h4 : live J.upper R <;> simp_all

/-- Refinement never flips LIVE to DEAD or DEAD to LIVE (T10's consequence). -/
theorem lam_refines_le {I J : Interval E} (h : J.Refines I) (R : Revocation E) :
    lam I R = LIVE → lam J R = LIVE := by
  intro hL
  rw [lam_refines h R (by rw [hL]; decide), hL]

theorem lam_refines_DEAD {I J : Interval E} (h : J.Refines I) (R : Revocation E) :
    lam I R = DEAD → lam J R = DEAD := by
  intro hD
  rw [lam_refines h R (by rw [hD]; decide), hD]

/-! ## Interval algebra, up to `Equiv` on both components -/

/-- Interval equivalence: same liveness function on both endpoints. -/
def IEquiv (I J : Interval E) : Prop := Equiv I.lower J.lower ∧ Equiv I.upper J.upper

theorem IEquiv.lam_eq {I J : Interval E} (h : IEquiv I J) (R : Revocation E) : lam I R = lam J R := by
  simp only [lam, h.1 R, h.2 R]

theorem oplus_comm (I J : Interval E) : IEquiv (Interval.oplus I J) (Interval.oplus J I) :=
  ⟨join_comm _ _, join_comm _ _⟩

theorem oplus_assoc (I J K : Interval E) :
    IEquiv (Interval.oplus (Interval.oplus I J) K) (Interval.oplus I (Interval.oplus J K)) :=
  ⟨join_assoc _ _ _, join_assoc _ _ _⟩

theorem oplus_idem (I : Interval E) : IEquiv (Interval.oplus I I) I :=
  ⟨join_idem _, join_idem _⟩

theorem otimes_comm (I J : Interval E) : IEquiv (Interval.otimes I J) (Interval.otimes J I) :=
  ⟨meet_comm _ _, meet_comm _ _⟩

theorem otimes_assoc (I J K : Interval E) :
    IEquiv (Interval.otimes (Interval.otimes I J) K) (Interval.otimes I (Interval.otimes J K)) :=
  ⟨meet_assoc _ _ _, meet_assoc _ _ _⟩

theorem otimes_idem (I : Interval E) : IEquiv (Interval.otimes I I) I :=
  ⟨meet_idem _, meet_idem _⟩

theorem otimes_oplus_distrib (I J K : Interval E) :
    IEquiv (Interval.otimes I (Interval.oplus J K))
      (Interval.oplus (Interval.otimes I J) (Interval.otimes I K)) :=
  ⟨meet_join_distrib _ _ _, meet_join_distrib _ _ _⟩

/-! ## Monotonicity of the interval operators in the refinement / component order -/

/-- Component-wise order on intervals (both endpoints in `Leq`). -/
def ILeq (I J : Interval E) : Prop := Leq I.lower J.lower ∧ Leq I.upper J.upper

theorem oplus_mono {I I' J J' : Interval E} (h1 : ILeq I I') (h2 : ILeq J J') :
    ILeq (Interval.oplus I J) (Interval.oplus I' J') :=
  ⟨join_mono h1.1 h2.1, join_mono h1.2 h2.2⟩

theorem otimes_mono {I I' J J' : Interval E} (h1 : ILeq I I') (h2 : ILeq J J') :
    ILeq (Interval.otimes I J) (Interval.otimes I' J') :=
  ⟨meet_mono h1.1 h2.1, meet_mono h1.2 h2.2⟩

/-- `λ_R` is monotone in the component order (raising both endpoints never lowers the verdict). -/
theorem lam_mono_ILeq {I J : Interval E} (h : ILeq I J) (R : Revocation E) : lam I R ≤ lam J R := by
  have hl := h.1 R
  have hu := h.2 R
  have hI := I.wf R
  have hJ := J.wf R
  simp only [lam]
  cases h1 : live I.lower R <;> cases h2 : live I.upper R <;>
    cases h3 : live J.lower R <;> cases h4 : live J.upper R <;> simp_all <;> decide

/-- Refinement in the refinement order is monotone: refining both operands refines the product. -/
theorem otimes_refines {I I' J J' : Interval E} (h1 : I'.Refines I) (h2 : J'.Refines J) :
    (Interval.otimes I' J').Refines (Interval.otimes I J) :=
  ⟨meet_mono h1.1 h2.1, meet_mono h1.2 h2.2⟩

theorem oplus_refines {I I' J J' : Interval E} (h1 : I'.Refines I) (h2 : J'.Refines J) :
    (Interval.oplus I' J').Refines (Interval.oplus I J) :=
  ⟨join_mono h1.1 h2.1, join_mono h1.2 h2.2⟩

/-! ## KS-T23 corollary shape: a conjunction over exported parts -/

/-- `⨂` over a list of intervals with a base (OCM `meet_all_profiles` from `one`). -/
def otimesAll : Interval E → List (Interval E) → Interval E
  | base, [] => base
  | base, I :: rest => otimesAll (Interval.otimes base I) rest

/-- `λ_R(⨂)` is the Kleene conjunction of the parts: LIVE only if every part is LIVE, DEAD as soon
as one part is (KS-T23, *no authority from abstraction*, warrant half). -/
theorem lam_otimesAll (base : Interval E) (parts : List (Interval E)) (R : Revocation E) :
    lam (otimesAll base parts) R = parts.foldl (fun acc I => kand acc (lam I R)) (lam base R) := by
  induction parts generalizing base with
  | nil => rfl
  | cons I rest ih =>
    simp only [otimesAll, List.foldl]
    rw [ih, lam_otimes]

theorem lam_otimesAll_DEAD_of_base (base : Interval E) (parts : List (Interval E))
    (R : Revocation E) (hb : lam base R = DEAD) : lam (otimesAll base parts) R = DEAD := by
  induction parts generalizing base with
  | nil => exact hb
  | cons J rest ih =>
    simp only [otimesAll]
    apply ih
    rw [lam_otimes, hb]
    cases lam J R <;> rfl

theorem lam_otimesAll_DEAD_of_part (base : Interval E) (parts : List (Interval E))
    (R : Revocation E) (I : Interval E) (hI : I ∈ parts) (hD : lam I R = DEAD) :
    lam (otimesAll base parts) R = DEAD := by
  induction parts generalizing base with
  | nil => exact absurd hI (by simp)
  | cons J rest ih =>
    rcases List.mem_cons.mp hI with rfl | hI'
    · simp only [otimesAll]
      apply lam_otimesAll_DEAD_of_base
      rw [lam_otimes, hD]
      cases lam base R <;> rfl
    · exact ih (Interval.otimes base J) hI'

/-- `⨂` is LIVE iff the base and every part are LIVE (KS-T23, LIVE half). -/
theorem lam_otimesAll_LIVE_iff (base : Interval E) (parts : List (Interval E)) (R : Revocation E) :
    lam (otimesAll base parts) R = LIVE ↔ lam base R = LIVE ∧ ∀ I, I ∈ parts → lam I R = LIVE := by
  induction parts generalizing base with
  | nil => simp [otimesAll]
  | cons J rest ih =>
    simp only [otimesAll]
    rw [ih, lam_otimes, kand_eq_LIVE_iff]
    constructor
    · rintro ⟨⟨hb, hJ⟩, hrest⟩
      refine ⟨hb, fun I hI => ?_⟩
      rcases List.mem_cons.mp hI with rfl | hI'
      · exact hJ
      · exact hrest I hI'
    · rintro ⟨hb, hall⟩
      exact ⟨⟨hb, hall J (by simp)⟩, fun I hI => hall I (by simp [hI])⟩

/-- The conjunction is LIVE only if every part is LIVE (KS-T23, LIVE half). -/
theorem lam_otimesAll_LIVE_part (base : Interval E) (parts : List (Interval E)) (R : Revocation E)
    (hL : lam (otimesAll base parts) R = LIVE) : ∀ I, I ∈ parts → lam I R = LIVE :=
  ((lam_otimesAll_LIVE_iff base parts R).mp hL).2

end KsoCore
