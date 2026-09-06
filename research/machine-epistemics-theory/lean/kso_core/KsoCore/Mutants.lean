import KsoCore.Interval
import KsoCore.Reopening
import KsoCore.Authority

/-!
# Planted mutants, refuted inside the build

Each OCM planted mutant (`warrant.mutant_*`, `types.mutant_authority_max`,
`revocation.mutant_impact_cone_direct_only`) and each theory-level control (§1.3 completeness bit,
MEG-16-REFUTED-V0, the missing well-formedness premise, a wrong Kleene order) is defined here and
*refuted by a proved witness*.  The batch document also describes, per theorem, the `example` that
fails to typecheck when the mutant is substituted for the honest definition; that failing code is
not part of the build — what is here are the positive statements that the mutants are wrong.
-/

namespace KsoCore

open Liveness

namespace Mutants

/-! ## A wrong Kleene order (UNKNOWN below DEAD) -/

/-- Mutant rank: `UNKNOWN < DEAD < LIVE`. -/
def mutantRank : Liveness → Nat
  | UNKNOWN => 0
  | DEAD => 1
  | LIVE => 2

def mutantLe (a b : Liveness) : Prop := mutantRank a ≤ mutantRank b

instance (a b : Liveness) : Decidable (mutantLe a b) := Nat.decLe _ _

/-- Under the mutant order `kand` is no longer the meet: `kand_eq_min` fails at `(DEAD, UNKNOWN)`. -/
theorem kand_not_min_under_mutant_order :
    ∃ a b : Liveness, kand a b ≠ (if mutantLe a b then a else b) :=
  ⟨DEAD, UNKNOWN, by decide⟩

/-! ## OCM `mutant_unknown_as_dead`: UNKNOWN collapsed into DEAD -/

def unknownAsDead {E : Type} (I : Interval E) (R : Revocation E) : Liveness :=
  if live I.lower R then LIVE else DEAD

theorem unknownAsDead_wrong :
    ∃ (I : Interval Unit) (R : Revocation Unit), unknownAsDead I R ≠ lam I R :=
  ⟨Interval.partialIv [], fun _ => false, by decide⟩

/-! ## OCM `mutant_unknown_as_live`: uncertified absence read as LIVE -/

def unknownAsLive {E : Type} [DecidableEq E] (I : Interval E) (R : Revocation E) : Liveness :=
  if live I.lower R then LIVE else if I.lower = I.upper then DEAD else LIVE

theorem unknownAsLive_wrong :
    ∃ (I : Interval Unit) (R : Revocation Unit), unknownAsLive I R ≠ lam I R :=
  ⟨⟨[], [[()]], zero_leq _⟩, fun _ => true, by decide⟩

/-! ## OCM `mutant_meet_as_union`: `⊗` replaced by `⊕` -/

theorem meet_as_union_wrong :
    ∃ (P Q : Profile Bool) (R : Revocation Bool), live (join P Q) R ≠ live (meet P Q) R :=
  ⟨[[true]], [[false]], fun e => !e, by decide⟩

/-! ## §1.3: a completeness bit does not compose -/

/-- Profile with a completeness bit (the pre-interval OCM representation). -/
structure BitProfile (E : Type) where
  profile : Profile E
  complete : Bool

def bitLam {E : Type} (P : BitProfile E) (R : Revocation E) : Liveness :=
  if live P.profile R then LIVE else if P.complete then DEAD else UNKNOWN

def bitOtimes {E : Type} (P Q : BitProfile E) : BitProfile E :=
  ⟨meet P.profile Q.profile, P.complete && Q.complete⟩

/-- The natural bit rule reads `UNKNOWN` where `∧₃` says `DEAD`
(`P = ⟨(), complete=False⟩`, `Q = ⟨{{2}}, complete=True⟩`, `R = {2}`). -/
theorem completeness_bit_does_not_compose :
    ∃ (P Q : BitProfile Unit) (R : Revocation Unit),
      bitLam (bitOtimes P Q) R ≠ kand (bitLam P R) (bitLam Q R) :=
  ⟨⟨[], false⟩, ⟨[[()]], true⟩, fun _ => true, by decide⟩

/-- The interval on the same data returns DEAD, as KS-T21 requires. -/
theorem interval_composes_where_bit_fails :
    lam (Interval.otimes (Interval.partialIv ([] : Profile Unit)) (Interval.certified [[()]]))
      (fun _ => true) = DEAD := by decide

/-! ## Missing-premise control: KS-T21 needs `lower ≤ upper` -/

/-- An interval without the well-formedness proof. -/
structure RawPair (E : Type) where
  lower : Profile E
  upper : Profile E

def rawLam {E : Type} (I : RawPair E) (R : Revocation E) : Liveness :=
  if live I.lower R then LIVE else if live I.upper R then UNKNOWN else DEAD

def rawOtimes {E : Type} (I J : RawPair E) : RawPair E := ⟨meet I.lower J.lower, meet I.upper J.upper⟩

/-- With an ill-formed pair (`lower` live, `upper` dead) the homomorphism fails: the premise
`Interval.wf` is load-bearing. -/
theorem homomorphism_fails_without_wf :
    ∃ (I J : RawPair Unit) (R : Revocation Unit),
      rawLam (rawOtimes I J) R ≠ kand (rawLam I R) (rawLam J R) :=
  ⟨⟨[[]], []⟩, ⟨[], [[]]⟩, fun _ => false, by decide⟩

/-! ## OCM `mutant_authority_max`: composition amplifies to the strongest component -/

def authorityMax {K : Type} (a b : Authority K) : Authority K := ⟨fun k => max (a.rank k) (b.rank k)⟩

theorem authority_max_raises :
    ∃ a b : Authority Unit, ¬ (authorityMax a b ≤ a) :=
  ⟨⟨fun _ => 0⟩, ⟨fun _ => 1⟩, fun h => by
    have := h ()
    revert this
    decide⟩

/-- The same witness through `internal_authority`'s shape: `max` lends `commit = 1` from a receipt
tail, the honest meet does not. -/
theorem authority_max_mints_commit :
    (authorityMax (⟨fun _ => 0⟩ : Authority Unit) ⟨fun _ => 1⟩).rank () = 1 ∧
      (Authority.meet (⟨fun _ => 0⟩ : Authority Unit) ⟨fun _ => 1⟩).rank () = 0 := by decide

/-! ## OCM `mutant_impact_cone_direct_only`: one hop instead of the closure -/

def chain : Nat → List Nat
  | 0 => [1]
  | 1 => [2]
  | _ => []

/-- On `0 → 1 → 2` the deep dependent `2` is in the closure but not in the one-hop cone. -/
theorem shallow_cone_misses_deep_dependent :
    2 ∈ reach chain 2 [0] ∧ 2 ∉ reach chain 1 [0] := by decide

/-! ## MEG-16-REFUTED-V0: liveness under nogoods is not an unconditional Kleene homomorphism -/

/-- `n ⊆ W` for lists. -/
def subList {E : Type} [DecidableEq E] (n W : List E) : Bool := n.all (fun e => decide (e ∈ W))

/-- `filter_N(P)`: drop every warrant containing a registered nogood. -/
def filterN {E : Type} [DecidableEq E] (N : List (Warrant E)) (P : Profile E) : Profile E :=
  P.filter (fun W => !(N.any (fun n => subList n W)))

/-- `λ_N` on a certified profile after nogood filtering. -/
def lamN {E : Type} [DecidableEq E] (N : List (Warrant E)) (P : Profile E) (R : Revocation E) :
    Liveness := lam (Interval.certified (filterN N P)) R

/-- `P = {{a}}`, `Q = {{b}}`, `N = {{a, b}}`: LIVE ∧₃ LIVE = LIVE but the joint support is a nogood. -/
theorem nogood_breaks_unconditional_kleene :
    ∃ (N : List (Warrant Bool)) (P Q : Profile Bool) (R : Revocation Bool),
      lamN N (meet P Q) R ≠ kand (lamN N P R) (lamN N Q R) :=
  ⟨[[true, false]], [[true]], [[false]], fun _ => false, by decide⟩

/-- MEG-16A: the nogood filter commutes with `⊕` (choice adds no joint support). -/
theorem filterN_join {E : Type} [DecidableEq E] (N : List (Warrant E)) (P Q : Profile E) :
    filterN N (join P Q) = join (filterN N P) (filterN N Q) := by
  simp [filterN, join, List.filter_append]

end Mutants

end KsoCore
