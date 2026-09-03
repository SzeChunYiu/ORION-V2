# FM60 — Obstruction and Counterexample Discovery: Exact Known-Answer Study Design (V1)

**Lane:** FM60, L4 formal transfer mechanics (issues #48, #50 §C1).
**Status:** frozen prospective design. No protected outcome has been generated or inspected.
**Machine-readable companion:** `FM60_OBSTRUCTION_COUNTEREXAMPLE_EXACT_STUDY_DESIGN_V1.json`.
**House style:** `research/experiments/me-x{1,2,4}` and the FM10 exemplar — exact
generator, exhaustive oracle cross-checked by an independent algorithm, seed
commitment in operator custody, development split separate from protected.

## 1. Why this suite exists, given FM/FG R2

The FM/FG R2 registered-scale campaign (2026-08-30,
`research/experiments/fmfg-r2/`) already dispatched a *model-arm* version of
FM10–FM60 at registered counts and terminated `REGISTERED_SCALE_NULL`. Its own
receipt records `fm60` as the campaign's single **floor** study: all five arms
scored exactly 32/120 = 0.267, and the receipt's own words are that the
generated task family was *uninformative for every arm*. A comparison in which
no arm can solve anything could not have detected a difference had one existed,
just as surely as the eight ceiling studies could not.

FM60 here is the *exact algorithmic* study the backlog actually asks for. The
floor defect is addressed head-on and in two places:

1. **`G0f`'s solvable half is a hard gate.** The run fails unless some
   non-control arm reaches 0.95. It is not enough to observe a null; the family
   must be one a strong arm can actually solve.
2. **The `no_obstruction` family is solvable by construction and verified by the
   oracle.** Its conclusions are drawn from the forward-chaining closure of the
   hypotheses in the registered rule base, so a derivation provably exists; the
   exhaustive oracle then independently confirms that no countermodel exists.
   A family whose acceptance cases were semantically valid but not derivable
   would put every witness-bearing arm on the floor, which is exactly the R2
   failure mode.

A **floor planted positive** is registered alongside the ceiling one: a
synthetic per-arm table in which every arm scores 0.267 — the literal R2 fm60
row — must **FAIL** `G0f`, and it must fail on the *solvable* half specifically.

## 2. Task and endpoint

The registered signature is one binary relation `R`, one unary predicate `P`,
no constants and no function symbols. The registered bounded model space is
every structure with domain size 1, 2 or 3: **4,164 structures**, materialised
once and never sampled.

Each instance is a **bounded conjecture**: a hypothesis set `H` (2–3 formulas
from a registered 26-formula vocabulary) and a conclusion
`C = c_1 ∧ … ∧ c_k` (1–3 formulas, disjoint from `H`). Each instance also
carries an **evidence set**: up to 12 models of `H`, drawn deterministically
from the instance seed.

| disposition | registered meaning | witness the arm must supply |
|---|---|---|
| `TRANSFER_VALID` (gloss `ACCEPT_WITH_PROOF_WITNESS`) | no countermodel exists in the bounded space | a **derivation** of every conjunct from `H` in the registered rule base |
| `REJECT_WITH_COUNTEREXAMPLE` | exactly one conjunct fails, and its minimum countermodel is no deeper than the shallowest model of `H` | a **countermodel**: a structure satisfying `H` and falsifying a conjunct |
| `REJECT_MINIMAL_COUNTEREXAMPLE_REQUIRED` | exactly one conjunct fails and every countermodel is strictly deeper than the shallowest model of `H` | a countermodel **of minimum size**, verified against every smaller structure |
| `MULTIPLE_INDEPENDENT_OBSTRUCTIONS` | ≥ 2 conjuncts fail and no failing conjunct's countermodel set contains another's | an **obstruction set** covering ≥ 2 distinct failing conjuncts |
| `UNDECIDED_BUDGET_EXHAUSTED` | honest abstention; never an oracle label, never an acceptance | none (an abstention carrying a witness is invalid) |
| `CLAIM_WITHOUT_VALID_WITNESS` | the arm's witness failed validation; never an oracle label | — |

Registered classification order: **multiplicity dominates minimality.** Two
failing conjuncts is `MULTIPLE_INDEPENDENT_OBSTRUCTIONS` even when one of them
first fails above the shallowest hypothesis model size. Fixture `KA-11` pins
this.

**Why deciding countermodel existence is not the endpoint on its own.**
Exhaustive enumeration decides it exactly, so a study built on it would report
parent sufficiency *by construction* rather than by measurement. Three things
are added: minimality, the number of independent obstructions, and a **witness
requirement that an enumerating search cannot discharge on the acceptance
side**.

### Why the accept label is spelled `TRANSFER_VALID`

The shared runner's `over_accept` / `under_accept` counters and the
`G2_ANTI_PERMISSIVENESS` gate key on that literal string. Spelling FM60's
acceptance anything else would have left `G2` printing a full denominator over a
predicate that could never fire — the exact defect `fm_core` was written to
prevent, in mirror form. The disposition's human-readable name is
`ACCEPT_WITH_PROOF_WITNESS`; the string is chosen so a hard gate stays live.

### The hard gate, made operational

The protocol's `formal_claim_without_witness_allowed: false` is enforced inside
`run_arm`: every **non-control** arm's witness is checked by the registered
validator, and a claim whose witness fails is rewritten to
`CLAIM_WITHOUT_VALID_WITNESS` — never an oracle label, therefore always scored
wrong. Witness validity is part of the endpoint, not a side report.

The three `C_*` control arms are **registered exempt**, before any outcome. A
control exists to exercise a counter; if every bare claim were rewritten before
it was counted, `G2`'s over-acceptance predicate could never fire and the gate
would be vacuous. The exemption is confined to `kind == CONTROL` and is stated
in the frozen design JSON.

## 3. Oracle and its independent cross-check

`oracle_exhaustive` materialises the bounded model space once and computes each
registered formula's truth column as a **bitset over all 4,164 structures**;
dispositions are then set algebra over those columns. It is exhaustive by
construction.

`oracle_stratified_dpll` never materialises the space. It runs a size-ascending
depth-first search over the **cells** of a partial model — the `n²` edge cells
and the `n` membership cells — and after every cell assignment evaluates each
hypothesis under **three-valued (Kleene) semantics**, cutting the branch as soon
as one is definitely false. Because sizes are visited in ascending order, the
first countermodel it reports is of minimum size *by construction*.

The two share only the grounded-circuit representation of a formula, exactly as
FM10's two oracle algorithms shared only the per-fact status primitive. They
must agree on `disposition`, `failing_conjuncts`, `minimal_size` and
`min_hypothesis_model_size` for **every** instance of every split (`G0b`).

The pairwise non-containment condition that makes multiple obstructions
*independent* is a **generator acceptance predicate, not an agreement field**:
it needs the full countermodel sets, which the stratified search never
materialises, so claiming both algorithms agree on it would be a check that
cannot actually be run.

### The generator proposes; the oracle verifies

An instance whose exhaustive disposition is not in its family's registered set,
whose family predicate fails, or on which the two algorithms disagree, is
rejected and resampled. Rejections are counted per family and published, never
hidden.

## 4. Arms, and why the comparator is the federation

| arm | kind | fidelity |
|---|---|---|
| `P0_INDUCTIVE_CONFIRMATION` | parent | generalises from the evidence set actually presented; refutes only if one of those instances happens to be a countermodel. The arm `misleading_surface_support` exists to defeat, and a real position in the confirmation literature rather than a strawman |
| `P1_FIXED_LESSON_TABLE` | parent | the protocol's frozen-lesson baseline: a verdict and a canned countermodel per conclusion formula, learned once from a frozen three-structure reference corpus; the hypotheses are never consulted |
| `P2_EXHAUSTIVE_MODEL_SEARCH` | parent | exhaustive finite-model search to the registered bound (Mace4-style) |
| `P3_DERIVATION_PROOF_SEARCH` | parent | saturating forward chaining over the registered rule base (Prover9-style), emitting the derivation as its witness |
| `P4_SMALL_SCOPE_BOUNDED_CHECK` | parent | bounded small-scope check, exhaustive to size 2 only (Alloy-style small-scope hypothesis) |
| `F0_PARENT_FEDERATION` | federation | **primary comparator** |
| `M_F2_OBSTRUCTION_DISCOVERY_FULL` | mechanic | ORION L2 obstruction and counterexample discovery |
| four `M_MINUS_*` ablations | ablation | obstruction search / proof witness / minimality escalation / multiplicity check |
| three `C_*` controls | control | always-accept, always-block, random |

**No single parent owns the endpoint.** `P2` decides the countermodel side
exactly, but exhausting the space yields no derivation, so its acceptance is a
claim without a proof witness and the hard gate rejects it. `P3` owns the
acceptance side but produces no countermodels and can only abstain on the reject
side. `P4` is exhaustive inside its scope and structurally blind one size above
it. The strongest faithful comparator is therefore their federation under a rule
fixed before any outcome and blind to it:

> *The acceptance question goes to `P3` first, because only a derivation can
> discharge the witness requirement. **Only if** `P3` fails to derive the
> conclusion is `P2` consulted, and its verdict and witness are taken as they
> stand. If neither parent discharges the claim, the federation abstains.*

Neither parent is consulted outside its native competence; neither ever sees the
oracle. Every parent passes its own native known-answer tests before it is used
as a comparator: **32/32 for FM60**, see
`FM_PARENT_FIDELITY_RECEIPT_FM60_V1.md`.

### M is an independent implementation, deliberately

`M` does **not** call either parent's procedure. Its proof stage is a bounded
forward chaining with its own rule ordering and a budget of 12 rule
applications. Its obstruction stage explores the hypothesis region by **local
repair** — breadth-first over single-cell edits that stay inside the region,
seeded from the instance's evidence set plus bounded random probing — and is
exhaustive only at domain sizes ≤ 2, where the space is small enough to certify
minimality directly.

Local repair is complete only on the components its seeds reach, so `M` *can*
miss an obstruction the complete parent finds, and "the federation reproduces M"
is something the run measures rather than something the code guarantees. This is
the FM10 lesson applied: an `M` that issued the same calls as `F0` would have
made `G1a`'s decision identity an **algebraic identity rather than a
measurement**.

`G1a` additionally carries a **liveness control**: at least one ablation arm
must register discordance against the parent on the same split, or the identity
counter is dead and its zero means nothing.

### Results that are definitional, and are labelled as such

- `P2` is exact on every reject family **by construction** (it is a complete
  search over the bounded space) and 0.00 on `no_obstruction` **by
  construction** (it has no derivation to offer). Its row is not independent
  parent evidence; its informative content is that neither property alone
  reaches the endpoint.
- `P3` is the mirror: exact on `no_obstruction` because that family's
  conclusions are drawn from the closure of `H`, and 0.00 elsewhere.
- `F0` is therefore expected to be exact by construction. Its content is the
  *attribution* — which parent owns which half of the endpoint — not a measured
  score.
- `misleading_surface_support` instances are rejected and resampled unless every
  model of the presented evidence set confirms the conclusion, so `P0` scoring
  0.00 there is definitional, not measured.

## 5. Gates

All gates are frozen here, before protected outcome access.

| gate | rule | hard |
|---|---|---|
| `G0a_KNOWN_ANSWER` | every hand-authored fixture's disposition reproduced by the oracle (≥ 8 required; 12 registered) | yes |
| `G0b_ORACLE_SELF_AGREEMENT` | the two independent oracle algorithms agree on every instance | yes |
| `G0c_NULL_CALIBRATION` | constant arms ≤ 0.40, random ≤ 0.40, M against within-split shuffled oracle labels ≤ 0.40 | yes |
| `G0d_DECOY_COVERAGE` | each registered decoy family carries ≥ 3 instances | yes |
| `G0e_PLANTED_POSITIVES` | every registered planted positive trips its own gate predicate (≥ 3 required; 7 registered) | yes |
| `G0f_FAMILY_DISCRIMINATION` | two halves, each with its own denominator: *solvable* (some non-control arm ≥ 0.95) **and** *separating* (some registered weak arm ≤ 0.85) | yes |
| `G1a_PARENT_REPRODUCES_M` | F0 reproduces M on ≥ 99.5% of instances, no family > 5% discordant, **and** the discordance counter shown live by ≥ 1 ablation | yes |
| `G1b_M_ADVANTAGE` | detector: paired diff > 0, exact two-sided p ≤ 0.05, ≥ 1 family with ≥ 5 M-only-exact | no |
| `G2_ANTI_PERMISSIVENESS` | on oracle-blocked instances, M accepts no more conjectures than F0 (≥ 10 blocked) | yes |
| `G3_MECHANISM_BY_OMISSION` | if G1b fires: the matching omission ablation's rate ≤ the parent's on that family | no |

Multiplicity: Holm across the five per-family paired tests, reported for every
run.

### Two reporting rules

1. **Every gate publishes its own denominator.** A gate whose denominator is
   below its registered minimum returns `CANNOT_CHECK` — never `PASS`. "Could
   not check" is never "checked and fine".
2. **Every no-alarm assertion is paired with a planted positive.** Seven
   trip-wires are registered and must all fire in the same execution that
   reports the study's zeros:

   | gate | planted case |
   |---|---|
   | `G0b_ORACLE_SELF_AGREEMENT` | a small-scope-only pseudo-oracle on an instance whose obstruction first appears one size above that scope |
   | `G0a_KNOWN_ANSWER` | a deliberately wrong expected disposition |
   | `G2_ANTI_PERMISSIVENESS` | `C_ALWAYS_ACCEPT` on an oracle-blocked instance |
   | `G0f_FAMILY_DISCRIMINATION` (ceiling) | a synthetic table in which every arm scores 1.000 must **FAIL** |
   | `G0f_FAMILY_DISCRIMINATION` (floor) | a synthetic table in which every arm scores 0.267 — the literal R2 fm60 row — must **FAIL**, on the *solvable* half |
   | `HARD_GATE_FORMAL_CLAIM_WITHOUT_WITNESS` | an arm returning the oracle's own disposition with an invalid witness must be caught by the same dispatcher that produces the study's numbers |
   | `G3_MECHANISM_BY_OMISSION` | `M_MINUS_MINIMALITY_ESCALATION` must be wrong where `M` is right |

## 6. Routes

`PARENT_SUFFICIENT` is a first-class successful terminal and is the
pre-registered expectation: three sibling exact studies (ME-X1, ME-X2, ME-X4)
and FM10's development split already found the strongest faithful parent
sufficient. A residual (`FM_RESIDUAL_CANDIDATE`) requires G1b to fire, G2 to
hold and G3 to attribute the advantage to a named omission — and would deserve
correspondingly hard scrutiny. `M_OVER_ACCEPTS` and `CANNOT_CHECK` are the
remaining terminals.

## 7. Sizes, seeds and execution

125 protected instances (25 per family × 5 families ≥ the 120 required by issue
#50 §C1); 15 development; 10 selftest. Deterministic, single-core and
byte-identical across processes; a protected-size probe on the public
development seed completed generation, dispatch, cross-check and scoring in
**1.17 s** wall on the Mac.

Protected seed commitment, frozen here:
`54a74a5960b88ed7973b690890a3fcb21bf80580d2a459075aae799aacbe02f2`
(sha256 of the stripped bytes of the seed file held at
`~/.orion-custody/fm/FM60_PROTECTED_SEED_V1.txt`).
Development and selftest seeds are public (`FM60-DEV-20260902`,
`FM60-SELFTEST`).

`fm_run.py FM60 protected` refuses (exit 3/4) unless a human-written
`PROTECTED_RUN_AUTHORIZATION.json` is present, names this suite, and carries
this file's companion JSON sha256; and unless the custody seed hashes to the
commitment above. Exactly one protected run and one analysis are permitted. No
design constant, gate, arm, oracle rule or seed may change after outcome access;
a legitimate repair gets a new prospective identity.

## 8. Authority

This design grants no scientific truth, no F2 superiority, no field status and
no submission readiness. A formal witness does not establish empirical truth.
