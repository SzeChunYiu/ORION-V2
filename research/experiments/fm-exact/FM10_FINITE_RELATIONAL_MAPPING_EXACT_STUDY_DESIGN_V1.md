# FM10 — Finite Relational Mapping: Exact Known-Answer Study Design (V1)

**Lane:** FM10, L4 formal transfer mechanics (issues #48, #50 §C1).
**Status:** frozen prospective design. No protected outcome has been generated or inspected.
**Machine-readable companion:** `FM10_FINITE_RELATIONAL_MAPPING_EXACT_STUDY_DESIGN_V1.json`.
**House style:** `research/experiments/me-x1`, `me-x2`, `me-x4` — exact generator,
exhaustive oracle cross-checked by an independent algorithm, seed commitment in
operator custody, development split separate from protected.

## 1. Why this suite exists, given FM/FG R2

The FM/FG R2 registered-scale campaign (2026-08-30,
`research/experiments/fmfg-r2/`) already dispatched a *model-arm* version of
FM10–FM60 at registered counts and terminated `REGISTERED_SCALE_NULL`. Its own
receipt records why the null is weakly informative: **eight of fourteen studies
sat at ceiling** (≥ 1 arm perfect, margins ≤ 2 tasks) and `fm10` in particular
scored 1.000 for all five arms. A comparison in which every arm is perfect could
not have detected a difference had one existed.

FM10 here is the *exact algorithmic* study the backlog actually asks for: real
parent implementations rather than model prompts, an exhaustive oracle, and — as
a first-class gate — a **non-degeneracy requirement** (`G0f`) that fails the run
if the task family cannot separate a registered weak arm from the strongest
parent. The ceiling defect that made R2 uninformative is now a gate, not a
footnote.

## 2. Task and endpoint

Each instance is a donor and a target finite typed relational structure. The
registered question is a **transfer disposition with an exact obstruction
class**, not mapping existence:

| disposition | meaning |
|---|---|
| `TRANSFER_VALID` | a total injective type-respecting node map exists under which every donor fact holds in the target, and every registered donor invariant also holds in the target |
| `BLOCK_INVARIANT_VIOLATION` | a perfect fact-level embedding exists, but a registered donor invariant fails in the target's ambient structure |
| `BLOCK_NO_TYPE_RESPECTING_MAP` | no injective type-respecting map exists at all |
| `BLOCK_DIRECTION_REVERSAL` | the optimal map's unmet facts are present with arguments reversed |
| `BLOCK_RELATION_TYPE_MISMATCH` | unmet facts are present with the right predicate and arguments but the wrong relation type |
| `BLOCK_MIXED_TYPED_OBSTRUCTION` | the optimal profile mixes the two typed obstructions with no outright-absent fact |
| `BLOCK_NO_HOMOMORPHISM` | the optimal profile contains a donor fact absent in any form |

**Mapping existence is deliberately not the endpoint.** A complete typed
homomorphism search decides it exactly, so a study built on it would report
parent sufficiency *by construction* rather than by measurement. Two things are
added instead: exact obstruction classification, and a **registered-invariant
stratum**.

### Registered invariants and their scope

A donor carries 1–2 structural invariants that genuinely hold in it, drawn from
`ACYCLIC:<pred>`, `ANTISYMMETRIC:<pred>`, `FUNCTIONAL:<pred>`. They are computed
from the donor's own facts, never asserted. A transfer is valid only if those
invariants also hold **in the target's whole structure**, not merely in the image
of the donor's fragment: a donor whose argument presupposes that `causes` is
acyclic is not entitled to transfer into a target where `causes` cycles, even
when its own fragment embeds cleanly. That scope choice is a substantive,
registered commitment, frozen here before any outcome, and the
`INVARIANT_BREAKING_EMBEDDING` family is what measures it.

Classification order is registered: a fact-level obstruction dominates an
invariant break, and the invariant test fires only when a perfect fact-level
embedding exists. Fixture `KA-11` pins this.

## 3. Oracle and its independent cross-check

`oracle_exhaustive` enumerates every injective type-respecting node map and
takes the lexicographically best obstruction profile, preferring fewest unmet
facts, then the most informative explanation (typed obstructions over outright
absence).

`oracle_branch_and_bound` is an independent algorithm: forward-checking
backtracking over node assignments with a monotone admissible bound, pruning any
partial assignment whose profile key already exceeds the incumbent. It never
materialises the map space. The two share only the per-fact status primitive.

They must agree on `disposition`, `min_missing`, `best_profile`,
`n_optimal_maps` and `broken_invariants` for **every** instance of every split
(`G0b`). The generator itself runs this check: it *proposes* a family and the
oracle *verifies* it; an instance whose exhaustive disposition is not in its
family's registered set is rejected and resampled, and rejection counts are
published per family, never hidden.

## 4. Arms, and why the comparator is the federation

| arm | kind | fidelity |
|---|---|---|
| `P0_SURFACE_SIMILARITY` | parent | literal/attribute similarity — the "mere appearance" baseline surface decoys exist to defeat |
| `P1_SME_STRUCTURE_MAPPING` | parent | Structure Mapping Engine, Falkenhainer, Forbus & Gentner 1989: local match hypotheses under tiered identicality, greedy structurally consistent gmap merging, systematicity evaluation |
| `P2_COMPLETE_HOMOMORPHISM` | parent | complete typed relational homomorphism search with obstruction profiling |
| `P3_FIXED_LESSON_INJECTION` | parent | the protocol's frozen-lesson-table baseline |
| `P4_INVARIANCE_PARENT` | parent | invariance / group-action reasoning over the registered invariants |
| `F0_PARENT_FEDERATION` | federation | **primary comparator** |
| `M_F2_TRANSFER_DISCOVERY_FULL` | mechanic | ORION L2 transfer discovery over `orion_v2.transfer_formal_mechanics` |
| four `M_MINUS_*` ablations | ablation | relational mapping / invariance test / obstruction search / type discipline |
| three `C_*` controls | control | always-transfer, always-block, random |

**No single parent owns the endpoint.** `P2` is complete on the mapping question
and structurally blind to the invariant stratum; `P4` owns the invariant
question and performs no alignment at all. The strongest faithful comparator is
therefore their federation under a rule fixed before any outcome and blind to
it: *P2 decides the mapping question; if and only if P2 finds a perfect
fact-level embedding is P4 consulted, and it may veto.* Neither parent is used
outside its native competence; neither ever sees the oracle.

### M is an independent implementation, deliberately

An earlier draft of `M` issued the same two calls as `F0` (complete search, then
invariant check). That would have made `G1a`'s decision identity an **algebraic
identity rather than a measurement**: discordance could not have been nonzero,
and the gate would have printed `n_evaluated = 126` over an effective
denominator of zero — the very defect this design is written to avoid, in mirror
form.

`M` therefore runs its own anytime alignment: greedy seeding on relational
overlap, then local search over single reassignments and pairwise swaps,
restarted from every seed, with candidates scored through
`assess_partial_homomorphism`; native recovery checks the donor's invariants on
the **image subgraph** first and escalates to the target's ambient structure.
Local search is not guaranteed to reach the optimum, so `M` *can* diverge from
the complete parent, and "the federation reproduces M" is something the run
measures rather than something the code guarantees.

`G1a` additionally carries a **liveness control**: at least one ablation arm
must register discordance against the parent on the same split, or the identity
counter is dead and its zero means nothing.

### Two results that are definitional, and are labelled as such

- `P2_COMPLETE_HOMOMORPHISM` is the same complete search as the branch-and-bound
  oracle algorithm, minus the invariant check. A complete typed search genuinely
  *is* the mature parent for the mapping question, so this is defensible — but
  P2's row is not independent parent evidence, and its 1.00 on every fact-level
  family and 0.00 on the invariant family are both by construction. Its
  informative content is that neither property alone reaches the endpoint.
- `SURFACE_DECOY` instances are rejected and resampled unless the surface
  correspondence is genuinely invalid, so `P0`/`P3` scoring 0.00 on that family
  is definitional, not measured. Rejection counts are published per family.

Every parent passes its own native known-answer tests before it is used as a
comparator; see `FM_PARENT_FIDELITY_RECEIPT_V1.md` (21/21 for FM10).

## 5. Gates

All gates are frozen here, before protected outcome access.

| gate | rule | hard |
|---|---|---|
| `G0a_KNOWN_ANSWER` | every hand-authored fixture's disposition reproduced by the oracle (≥ 8 fixtures) | yes |
| `G0b_ORACLE_SELF_AGREEMENT` | the two independent oracle algorithms agree on every instance | yes |
| `G0c_NULL_CALIBRATION` | constant arms ≤ 0.40, random ≤ 0.40, M against within-split shuffled oracle labels ≤ 0.40 | yes |
| `G0d_DECOY_COVERAGE` | each registered decoy family carries ≥ 3 instances | yes |
| `G0e_PLANTED_POSITIVES` | every registered planted positive trips its own gate predicate (≥ 3) | yes |
| `G0f_FAMILY_DISCRIMINATION` | two halves, each with its own denominator: *solvable* (some non-control arm ≥ 0.95) **and** *separating* (some registered weak arm ≤ 0.85) | yes |
| `G1a_PARENT_REPRODUCES_M` | F0 reproduces M on ≥ 99.5% of instances, no family > 5% discordant, **and** the discordance counter is shown live by ≥ 1 ablation disagreeing with the parent | yes |
| `G1b_M_ADVANTAGE` | detector: paired diff > 0, exact two-sided p ≤ 0.05, ≥ 1 family with ≥ 5 M-only-exact | no |
| `G2_ANTI_PERMISSIVENESS` | on oracle-blocked instances, M accepts no more transfers than F0 (≥ 10 blocked) | yes |
| `G3_MECHANISM_BY_OMISSION` | if G1b fires: the matching omission ablation's rate ≤ the parent's on that family | no |

Multiplicity: Holm across the seven per-family paired tests, reported for every
run.

### Two reporting rules, both learned from defects found on 2026-09-02

1. **Every gate publishes its own denominator.** Three defects found that day
   were gates reporting zero violations because they never ran on the relevant
   cases (a counter nested inside a guard that excluded the family under test; a
   CI regex matching text that is never emitted; a horizon check flat by
   construction). Each gate here carries `n_evaluated`, and a gate whose
   denominator is below its registered minimum returns `CANNOT_CHECK` — never
   `PASS`. "Could not check" is never "checked and fine".
2. **Every no-alarm assertion is paired with a planted positive.** Five
   trip-wires are registered for FM10 and must all fire in the same execution
   that reports the study's zeros: an incomplete pseudo-oracle must be caught by
   `G0b`'s predicate; a deliberately wrong expected label must be caught by
   `G0a`'s; the over-transfer counter must count `C_ALWAYS_TRANSFER` on a blocked
   instance; a synthetic all-ceiling arm table must **fail** `G0f`; and
   `M_MINUS_INVARIANCE_TEST` must be wrong where `M` is right.

## 6. Routes

`PARENT_SUFFICIENT` is a first-class successful terminal, and it is the
pre-registered expectation: three sibling exact studies (ME-X1, ME-X2, ME-X4)
have already found the strongest faithful parent sufficient. A residual
(`FM_RESIDUAL_CANDIDATE`) requires G1b to fire, G2 to hold and G3 to attribute
the advantage to a named omission — and would deserve correspondingly hard
scrutiny. `M_OVER_ACCEPTS` and `CANNOT_CHECK` are the remaining terminals.

## 7. Sizes, seeds and execution

126 protected instances (18 per family × 7 families ≥ the 120 required by issue
#50 §C1); 21 development; 14 selftest. Deterministic and single-core; the whole
protected run is well under a minute on the Mac.

Protected seed commitment, frozen here:
`b630beec4e60723caa3435b8c06754ecc184f66b2fc0787d27430979e4e447a4`
(sha256 of the seed string held at `~/.orion-custody/fm/FM10_PROTECTED_SEED_V1.txt`).
Development and selftest seeds are public (`FM10-DEV-20260902`, `FM10-SELFTEST`).

`fm_run.py FM10 protected` refuses (exit 3/4) unless a human-written
`PROTECTED_RUN_AUTHORIZATION.json` is present, names this suite, and carries
this file's sha256; and unless the custody seed hashes to the commitment above.
Exactly one protected run and one analysis are permitted. No design constant,
gate, arm, oracle rule or seed may change after outcome access; a legitimate
repair gets a new prospective identity.

## 8. Authority

This design grants no scientific truth, no F2 superiority, no field status and
no submission readiness. A formal witness does not establish empirical truth.
