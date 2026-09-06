/-!
# The authority product lattice and the meet (T1 · MEG-04; KS-T20; KS-T23 authority half)

OCM `src/ocm/kso/types.py::Authority` is a product lattice of named non-negative integer ranks with
an undeclared coordinate read as `0`, `meet` = coordinate-wise `min`, `≤` = coordinate-wise `≤`, and
`internal_authority` = the meet with the `commit` coordinate dropped.  Here an authority is a rank
function `K → Nat` on a coordinate type `K` (missing = 0 is built in).

Theorems: the meet never raises any coordinate (`meet_le_left`, `meet_le_right`,
`meet_never_raises`), it is the greatest lower bound (`le_meet`), commutative / associative /
idempotent, monotone in each argument; a fold over any list of factors is below every factor
(`meetAll_le_mem`); dropping `commit` is below the input and pins `commit` to `0`; and no chain of
internal operations (each carrying an operator factor with `commit = 0`) reaches a positive
`commit` rank (`InternalOnly.commit_zero`, T1 (iii)).
-/

namespace KsoCore

/-- An authority: a rank per coordinate; undeclared = 0. -/
structure Authority (K : Type) where
  rank : K → Nat

namespace Authority

variable {K : Type}

/-- Product order `a ⪯ b`. -/
protected def le (a b : Authority K) : Prop := ∀ k, a.rank k ≤ b.rank k

instance : LE (Authority K) := ⟨Authority.le⟩

/-- Coordinate-wise `min` (OCM `Authority.meet`). -/
def meet (a b : Authority K) : Authority K := ⟨fun k => min (a.rank k) (b.rank k)⟩

theorem rank_meet (a b : Authority K) (k : K) : (meet a b).rank k = min (a.rank k) (b.rank k) := rfl

theorem le_refl (a : Authority K) : a ≤ a := fun _ => Nat.le_refl _

theorem le_trans {a b c : Authority K} (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c :=
  fun k => Nat.le_trans (h1 k) (h2 k)

/-- The meet never raises: `a ∧ b ⪯ a`. -/
theorem meet_le_left (a b : Authority K) : meet a b ≤ a := fun _ => Nat.min_le_left _ _

theorem meet_le_right (a b : Authority K) : meet a b ≤ b := fun _ => Nat.min_le_right _ _

/-- Composition with *any* object authority `x` never raises `a` on any coordinate. -/
theorem meet_never_raises (a x : Authority K) (k : K) : (meet a x).rank k ≤ a.rank k :=
  meet_le_left a x k

/-- Greatest lower bound. -/
theorem le_meet {a b c : Authority K} (h1 : c ≤ a) (h2 : c ≤ b) : c ≤ meet a b := fun k => by
  have := h1 k
  have := h2 k
  show c.rank k ≤ min (a.rank k) (b.rank k)
  omega

theorem meet_comm (a b : Authority K) : meet a b = meet b a := by
  unfold meet
  congr 1
  funext k
  exact Nat.min_comm _ _

theorem meet_assoc (a b c : Authority K) : meet (meet a b) c = meet a (meet b c) := by
  unfold meet
  congr 1
  funext k
  exact Nat.min_assoc _ _ _

theorem meet_idem (a : Authority K) : meet a a = a := by
  cases a with
  | mk r =>
    unfold meet
    congr 1
    funext k
    exact Nat.min_self _

/-- Monotone in each argument. -/
theorem meet_mono {a a' b b' : Authority K} (h1 : a ≤ a') (h2 : b ≤ b') : meet a b ≤ meet a' b' :=
  fun k => by
    have := h1 k
    have := h2 k
    show min (a.rank k) (b.rank k) ≤ min (a'.rank k) (b'.rank k)
    omega

/-- Fold of the meet over a list of factors starting from `base` (OCM `meet_authority`). -/
def meetAll : Authority K → List (Authority K) → Authority K
  | base, [] => base
  | base, a :: rest => meetAll (meet base a) rest

theorem meetAll_le_base (base : Authority K) (l : List (Authority K)) : meetAll base l ≤ base := by
  induction l generalizing base with
  | nil => exact le_refl base
  | cons a rest ih => exact le_trans (ih (meet base a)) (meet_le_left base a)

/-- The composite authority is below every factor: no amplification (KS-T20 authority clause). -/
theorem meetAll_le_mem (base : Authority K) (l : List (Authority K)) (x : Authority K) (hx : x ∈ l) :
    meetAll base l ≤ x := by
  induction l generalizing base with
  | nil => exact absurd hx (by simp)
  | cons a rest ih =>
    rcases List.mem_cons.mp hx with rfl | hx'
    · exact le_trans (meetAll_le_base (meet base x) rest) (meet_le_right base x)
    · exact ih (meet base a) hx'

/-- OCM `internal_authority`: the `commit` coordinate is undeclared for internal operators. -/
def dropCommit [DecidableEq K] (commit : K) (a : Authority K) : Authority K :=
  ⟨fun k => if k = commit then 0 else a.rank k⟩

theorem dropCommit_le [DecidableEq K] (commit : K) (a : Authority K) : dropCommit commit a ≤ a := by
  intro k
  show (if k = commit then 0 else a.rank k) ≤ a.rank k
  split
  · exact Nat.zero_le _
  · exact Nat.le_refl _

theorem dropCommit_commit [DecidableEq K] (commit : K) (a : Authority K) :
    (dropCommit commit a).rank commit = 0 := by
  show (if commit = commit then 0 else a.rank commit) = 0
  simp

/-- T1 (ii): an internally composed object has `commit = 0` whatever its tails carry. -/
theorem internal_commit_zero [DecidableEq K] (commit : K) (base : Authority K)
    (tails : List (Authority K)) : (dropCommit commit (meetAll base tails)).rank commit = 0 :=
  dropCommit_commit commit _

/-- Derivations by internal operators only: leaves have `commit = 0`; every step composes tails
with an operator factor whose `commit` is `0`. -/
inductive InternalOnly (commit : K) : Authority K → Prop
  | base (a : Authority K) (h : a.rank commit = 0) : InternalOnly commit a
  | compose (op : Authority K) (hop : op.rank commit = 0) (tails : List (Authority K))
      (htails : ∀ t, t ∈ tails → InternalOnly commit t) : InternalOnly commit (meetAll op tails)

/-- T1 (iii): no chain of internal operations of any length produces a positive `commit` rank. -/
theorem InternalOnly.commit_zero {commit : K} {a : Authority K} (h : InternalOnly commit a) :
    a.rank commit = 0 := by
  cases h with
  | base _ h => exact h
  | compose op hop tails _ =>
    have := meetAll_le_base op tails commit
    omega

/-- The meet of a list with an operator factor is below the operator on the `commit` coordinate even
when a tail is a receipt with positive `commit` (receipt tails cannot lend commit authority). -/
theorem receipt_tail_cannot_lend_commit {commit : K} (op : Authority K) (hop : op.rank commit = 0)
    (tails : List (Authority K)) : (meetAll op tails).rank commit = 0 := by
  have := meetAll_le_base op tails commit
  omega

end Authority

end KsoCore
