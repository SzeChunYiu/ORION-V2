/-!
# Three-valued liveness and the Kleene connectives

Mechanises the value set of OCM `src/ocm/kso/warrant.py::Liveness` and its two connectives
`kleene_and` / `kleene_or` (Kleene 1938, strong three-valued logic).  The constructor order is the
Kleene truth order `DEAD < UNKNOWN < LIVE` (written `≤₃` in the theory documents); `kand` is the
meet and `kor` the join of that order (theorems `kand_eq_min`, `kor_eq_max`).

Every statement is closed by case analysis on the finite type; nothing is admitted.
-/

namespace KsoCore

/-- OCM `warrant.Liveness`.  Constructor order = Kleene truth order. -/
inductive Liveness where
  | DEAD
  | UNKNOWN
  | LIVE
  deriving DecidableEq, Repr

namespace Liveness

/-- Rank in the Kleene truth order: DEAD = 0, UNKNOWN = 1, LIVE = 2. -/
def rank : Liveness → Nat
  | DEAD => 0
  | UNKNOWN => 1
  | LIVE => 2

/-- The Kleene truth order `a ≤₃ b`. -/
protected def le (a b : Liveness) : Prop := a.rank ≤ b.rank

instance : LE Liveness := ⟨Liveness.le⟩

instance decLe (a b : Liveness) : Decidable (a ≤ b) := Nat.decLe a.rank b.rank

/-- OCM `kleene_and`: DEAD absorbs, then UNKNOWN, else LIVE. -/
def kand : Liveness → Liveness → Liveness
  | DEAD, _ => DEAD
  | _, DEAD => DEAD
  | UNKNOWN, _ => UNKNOWN
  | _, UNKNOWN => UNKNOWN
  | LIVE, LIVE => LIVE

/-- OCM `kleene_or`: LIVE absorbs, then UNKNOWN, else DEAD. -/
def kor : Liveness → Liveness → Liveness
  | LIVE, _ => LIVE
  | _, LIVE => LIVE
  | UNKNOWN, _ => UNKNOWN
  | _, UNKNOWN => UNKNOWN
  | DEAD, DEAD => DEAD

/-! ## Order facts -/

theorem le_refl (a : Liveness) : a ≤ a := by cases a <;> decide

theorem le_trans {a b c : Liveness} (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  cases a <;> cases b <;> cases c <;> first
    | decide
    | exact absurd h1 (by decide)
    | exact absurd h2 (by decide)

theorem le_antisymm {a b : Liveness} (h1 : a ≤ b) (h2 : b ≤ a) : a = b := by
  cases a <;> cases b <;> first
    | rfl
    | exact absurd h1 (by decide)
    | exact absurd h2 (by decide)

theorem DEAD_le (a : Liveness) : DEAD ≤ a := by cases a <;> decide

theorem le_LIVE (a : Liveness) : a ≤ LIVE := by cases a <;> decide

/-- LIVE is the top: nothing but LIVE lies above it. -/
theorem LIVE_le_iff (a : Liveness) : LIVE ≤ a ↔ a = LIVE := by
  cases a <;> simp <;> decide

/-- DEAD is the bottom. -/
theorem le_DEAD_iff (a : Liveness) : a ≤ DEAD ↔ a = DEAD := by
  cases a <;> simp <;> decide

/-! ## Lattice laws of the Kleene connectives (the finite oracle is OCM `kleene_and` / `kleene_or`
truth tables, exercised by `warrant.check_three_valued_reduction`). -/

theorem kand_comm (a b : Liveness) : kand a b = kand b a := by cases a <;> cases b <;> rfl

theorem kand_assoc (a b c : Liveness) : kand (kand a b) c = kand a (kand b c) := by
  cases a <;> cases b <;> cases c <;> rfl

theorem kand_idem (a : Liveness) : kand a a = a := by cases a <;> rfl

theorem kor_comm (a b : Liveness) : kor a b = kor b a := by cases a <;> cases b <;> rfl

theorem kor_assoc (a b c : Liveness) : kor (kor a b) c = kor a (kor b c) := by
  cases a <;> cases b <;> cases c <;> rfl

theorem kor_idem (a : Liveness) : kor a a = a := by cases a <;> rfl

theorem kand_absorb (a b : Liveness) : kand a (kor a b) = a := by cases a <;> cases b <;> rfl

theorem kor_absorb (a b : Liveness) : kor a (kand a b) = a := by cases a <;> cases b <;> rfl

theorem kand_kor_distrib (a b c : Liveness) : kand a (kor b c) = kor (kand a b) (kand a c) := by
  cases a <;> cases b <;> cases c <;> rfl

theorem kand_LIVE (a : Liveness) : kand LIVE a = a := by cases a <;> rfl

theorem kand_DEAD (a : Liveness) : kand DEAD a = DEAD := by cases a <;> rfl

theorem kor_DEAD (a : Liveness) : kor DEAD a = a := by cases a <;> rfl

theorem kor_LIVE (a : Liveness) : kor LIVE a = LIVE := by cases a <;> rfl

/-- `kand` is the meet of the Kleene order. -/
theorem kand_eq_min (a b : Liveness) : kand a b = (if a ≤ b then a else b) := by
  cases a <;> cases b <;> decide

/-- `kor` is the join of the Kleene order. -/
theorem kor_eq_max (a b : Liveness) : kor a b = (if a ≤ b then b else a) := by
  cases a <;> cases b <;> decide

theorem kand_le_left (a b : Liveness) : kand a b ≤ a := by cases a <;> cases b <;> decide

theorem kand_le_right (a b : Liveness) : kand a b ≤ b := by cases a <;> cases b <;> decide

theorem le_kor_left (a b : Liveness) : a ≤ kor a b := by cases a <;> cases b <;> decide

theorem le_kor_right (a b : Liveness) : b ≤ kor a b := by cases a <;> cases b <;> decide

/-- Monotonicity of `kand` in each argument (all 3 × 3 × 3 × 3 cases). -/
theorem kand_mono {a a' b b' : Liveness} (h1 : a ≤ a') (h2 : b ≤ b') : kand a b ≤ kand a' b' := by
  cases a <;> cases a' <;> cases b <;> cases b' <;> first
    | decide
    | exact absurd h1 (by decide)
    | exact absurd h2 (by decide)

/-- Monotonicity of `kor` in each argument. -/
theorem kor_mono {a a' b b' : Liveness} (h1 : a ≤ a') (h2 : b ≤ b') : kor a b ≤ kor a' b' := by
  cases a <;> cases a' <;> cases b <;> cases b' <;> first
    | decide
    | exact absurd h1 (by decide)
    | exact absurd h2 (by decide)

/-- A conjunction is LIVE only when both conjuncts are. -/
theorem kand_eq_LIVE_iff (a b : Liveness) : kand a b = LIVE ↔ a = LIVE ∧ b = LIVE := by
  cases a <;> cases b <;> simp [kand]

/-- A conjunction is DEAD as soon as one conjunct is. -/
theorem kand_eq_DEAD_iff (a b : Liveness) : kand a b = DEAD ↔ a = DEAD ∨ b = DEAD := by
  cases a <;> cases b <;> simp [kand]

end Liveness

end KsoCore
