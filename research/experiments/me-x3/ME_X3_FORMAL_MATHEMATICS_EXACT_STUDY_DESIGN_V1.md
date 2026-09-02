# ME-X3 — Formal Mathematical Discovery and Regime Change: Exact Known-Answer Study (Registered Design V1)

**Class:** exact-oracle known-answer study — **zero model calls, fully
deterministic, CPU-minutes**. It decides whether explicit obstruction diagnosis
plus minimum-responsible escalation makes formal-mathematical decisions that the
strongest faithful parent federation cannot reproduce from the same registered
information — while keeping **proof validity** and **specification fidelity**
separate endpoints throughout. **Parent sufficiency is a successful terminal**,
and it is the pre-registered expectation (§1.2).

**Protocols served:** `ME_X3_FORMAL_MATHEMATICS_PROTOCOL_V1.md` (§2–§12),
`MACHINE_EPISTEMICS_ME_X3_FORMAL_MATH_PROTOCOL_V1.md` (§1–§14),
`MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md` §0–§2 and §5.

**Secondary axis (H-EXT-3):** the B5 interface-information ladder of
`research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md`, with
its own gate (G4).

**Status:** frozen design + arms + development split. **No protected outcome has
been generated or inspected.** The protected stage refuses to run without a
recorded authorization (§8).

Companions: `ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json` (schema
`orion.v2.me-x3.exact-study-design.v1`) carries every constant below and the code
hashes; `ME_X3_FORMAL_MATHEMATICS_FEASIBILITY_RECEIPT_V1.md` carries the Lean
toolchain decision; `ME_X3_PARENT_FIDELITY_RECEIPT_V1.md` carries the parent
behaviours and the development-split summary.

## 1. Question, hypothesis, expectation

**Q.** When a formal problem is not being solved efficiently, does explicit
obstruction diagnosis identify whether the right next move is more search, a
retrievable lemma, an invented lemma, a representation change, a counterexample
probe, a repair of the formalization, or honest unresolvedness — and does
choosing the *minimum* responsible move beat `B5`, the strongest faithful parent
federation receiving the same registered information and the same budget?

The study does **not** ask whether a system can prove more theorems with more
search. Extra compute is not an ME residual.

**H0 (strongest-parent sufficiency).** An information-matched federation of
proof search, retrieval, discover-and-prove, lemma/abstraction discovery,
counterexample tooling and autoformalization checking makes the same decisions at
equal or lower cost.

**1.2 Pre-registered expectation.** `PARENT_SUFFICIENT`, ladder terminal
`RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. The top-rung federation runs the
same specification check and the same escalation modules, and on an exhaustive
finite oracle a well-ordered cascade with the same information should reach the
same decisions. The decisive content of the study is therefore (a) the systematic
fidelity blindness of proof-only parents, (b) where single parents break, (c) the
ablations, (d) the ladder, (e) cost.

**1.3 Delta from ME-X1 family 8.** ME-X1 already contained "formal proof / wrong
specification" as one of ten case families, scored as one transition decision.
ME-X3 makes specification fidelity a **co-primary endpoint** over a dedicated
stratum with registered drift subtypes, adjudicated by explicit witnesses, and
reports it separately from proof validity so that no pooled score can absorb it.
That is the non-duplication boundary required by protocol §14.5.

## 2. The object formal system

A **term** is a word `w = (a_1 … a_k)` over a finite alphabet of unary operator
symbols, read as `a_1(a_2(… a_k(x)))`. A **statement** is a schematic equation
`lhs =?= rhs`, universally quantified in the schema variable. A **presentation**
is a finite set of equational axioms.

Because every operator is unary, Birkhoff derivation is exactly two-sided factor
rewriting: `p u s → p v s` for any prefix `p` (congruence) and suffix `s`
(instantiation). A derivation is therefore a finite rewrite chain and proof
validity is decidable by breadth-first search under a registered word-length and
expansion cap.

A **model** is a finite set `[0,n)` with one function per symbol satisfying every
axiom as an equality of composed functions. By soundness a model in which a
statement fails certifies that the statement is *not* derivable; the model class
up to `max_model_size` is enumerated exhaustively.

An **alternative presentation** is produced by a Tietze transformation: introduce
a generator `g := d` and fold `d` into `g` in the axioms. This changes the
representation while presenting the same algebra, which is checked semantically
(every model of the alternative restricts to a model of the base).

Everything the study needs is thus exactly computable, with a witness in every
case: a rewrite chain, or a finite model.

### 2.1 Why not Lean + Mathlib as the primary verifier

See the feasibility receipt. In one line: an unbounded library makes the
minimum-escalation oracle uncomputable rather than merely expensive. Lean 4.33.1
is used as an **external cross-check** on emitted derivations, as genuine
inductive proof terms rather than reflection, with negative controls required to
fail for a registered reason.

## 3. The exact minimum-escalation oracle

The oracle answer is not a generator intention. For every task it is computed by
exhaustive search over the **registered finite intervention space**, in this
frozen order, each level carrying a witness:

| level | succeeds when | witness | action |
|---|---|---|---|
| `L0_REFUTE` | a finite model of the axioms falsifies the statement | that model | `GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL` |
| `L1_DIRECT` | a rewrite chain exists within `solve_expansions` | the chain | `CONTINUE_DIRECT_PROOF_SEARCH` |
| `L2_RETRIEVE` | some library lemma brings the target inside that cap | the lemma | `RETRIEVE_EXISTING_LEMMA` |
| `L3_INVENT` | some lemma in the registered candidate pool is itself derivable and brings the target inside the cap | the lemma | `INVENT_LOCAL_LEMMA` |
| `L4_REPRESENTATION` | the offered alternative presentation does, and presents the same theory | the translated statement | `CHANGE_REPRESENTATION` |
| `L5_DEFER` | nothing in the space succeeds | the saturation record | `DEFER_CANNOT_IDENTIFY` |

The minimal action is the **first** level that succeeds, so minimality holds by
construction over the registered space rather than by assertion. The candidate
pool (`registered_lemma_pool`) is a frozen deterministic function of the
presentation and the statement — no randomness, no oracle labels.

**Fidelity overrides the action.** If the presented statement does not encode the
intended one, the correct high-level move is to repair the formalization
(`REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK`), or to ask
(`REQUEST_SPECIFICATION_CLARIFICATION`) when the intent cannot be adjudicated at
all — whatever the proof search returned. A proof of the wrong statement is not
the right next move. Both `B5` and `M` apply this rule, because both run the
check: it is part of the shared contract, not an `M` privilege.

## 4. Specification fidelity, adjudicated by witnesses

Fidelity is decided in the presentation the formal statement is written in.

- **FAITHFUL** requires *interderivability in both directions* between the
  intended and the presented equation — an exact certificate, not bounded model
  agreement.
- **Drift** requires a **separating model**: a model of the axioms in which
  exactly one of the two statements holds. Every drift instance is generated
  *from its separating model outward*, so the witness is inside the registered
  model-size bound by construction. A bounded-agreement fidelity oracle, in which
  a mismatch first appearing at size `k+1` would score FAITHFUL, is exactly the
  soft spot this construction removes.
- **CANNOT_CHECK_INTENT** is the honest terminal when neither route settles it,
  and is generated deliberately (an intended statement that is itself undecided
  within the frozen environment).

Registered drift subtypes, each a distinct syntactic operation with a semantic
witness: `MATERIALLY_WEAKENED` (a context added to both sides),
`MATERIALLY_STRENGTHENED` (a context dropped), `NOTATIONAL_COLLAPSE` (two
distinct operators identified), `ABSTRACTION_ELEVATION` (the statement restated
over the alternative presentation's new generator, quantifying over a signature
the intent never mentioned), `DEGENERATE_TRIVIALIZATION` (the presented statement
restates one side of the intended equation and is vacuously provable),
`OTHER_SEMANTIC_DRIFT`.

The **FAITHFUL controls are the anti-conservatism half of F7** (about a third of
the stratum): the presented statement differs on the surface but is
interderivable. An arm that flags every surface difference as drift fails here,
and the pooled `false_drift_alarm_rate` is gated (G2).

## 5. Task families

Each family's label is an **oracle fact**, enforced by rejection sampling: a
candidate is emitted only if the oracle verdict lands in the family's registered
cell (`FAMILY_CELL` in `mex3_generator.py`).

| family | oracle cell | purpose |
|---|---|---|
| `F1_DIRECT_SEARCH` | `L1_DIRECT`, faithful | false-escalation control |
| `F2_MISSING_LEMMA` | `L2_RETRIEVE` or `L3_INVENT`, faithful | lemma level, not representation |
| `F3_REPRESENTATION_CHANGE` | `L4_REPRESENTATION`, faithful | the level-3 intervention |
| `F4_DECEPTIVE_CHANGE` | `L1_DIRECT` with an attractive alternative offered and strictly worse | punishes "creativity = progress" |
| `F5_PROBE_OR_COUNTEREXAMPLE_NEEDED` | `L0_REFUTE`, faithful | the next move is a probe, not a proof |
| `F6_UNDERDETERMINED_OR_CANNOT_CHECK` | `L5_DEFER`, faithful | calibration, anti-fabrication |
| `F7_SPECIFICATION_MISMATCH` | fidelity equals the registered subtype | verifier/specification separation |
| `F8_TRANSFER` | source and held-out target both at the lemma level | held-out reach at the lemma level (see the registered limitation below) |

F8 emits a **pair**: a source task and a held-out sibling frozen with it, before
any arm runs, solvable within budget only at the lemma level. Only an arm's *own*
invention is carried; reusing it is reported as the invention it was.

**Registered limitation.** The held-out target admits *independent re-invention*
from the registered candidate pool as well as *reuse* of the source's artefact,
so carrying the artefact is sufficient but not necessary. F8 therefore measures
held-out solve rate at the lemma level, not reuse gain, and it does **not**
support a strong reusability claim; the G3 row for F8 is expected to show no
degradation for that structural reason rather than because transfer tracking is
inert. The analysis prints the no-carry counterfactual
(`M_MINUS_TRANSFER_REUSE_TRACKING`) beside the rate so the zero is visible rather
than implied. A study that isolates reuse would have to make the target
unreachable by any pool lemma except the source's, which is a different
generator and a different identity.

Surface cues (an alternative presentation offered under a suggestive label, a
symmetric-looking statement) are visible to every arm on both `F3` and `F4`, so
cue-following cannot be a shortcut.

## 6. Arms

Every arm is built from the **same** module toolkit and runs under the **same**
per-task ledger. No arm sees the family label, the oracle action, the oracle
truth value or any oracle witness.

| arm | parent recovered |
|---|---|
| `A0_DIRECT` | base proof search, no metacognitive scaffold, no intent check |
| `A1_RETRIEVAL` | + library retrieval |
| `A2_SELF_REFLECT` | + generic self-reflection/retry under the same total budget |
| `A3_DISCOVER_AND_PROVE_PARENT` | Discover-and-Prove: settle the answer semantically, then prove |
| `A4_LEMMA_ABSTRACTION_PARENT` | lemma/abstraction discovery and verified reuse |
| `B5_R1…R4` | the federation at restricted interface rungs (H-EXT-3) |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | all of the above composed, with the FormalScience-style specification check, at full structure |
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | the candidate |

`A0`–`A4` report `FAITHFUL` whenever they verify: a proof-only system treats
proof success as intent success. That is not a strawman, it is the parent
boundary the FormalScience result is about, and it is the study's clearest
prediction.

**M's declared delta** is control only: a witnessed obstruction hypothesis, a
lower-level disposition, a minimum-sufficient escalation, a preservation
obligation attached to any representation change, and an unresolved terminal. It
calls the same modules as the top-rung federation and receives the same reports.

### 6.1 The H-EXT-3 ladder and the parity rule

The rungs restrict **what the modules may report back to the federation's glue**:
`R1` verdict only; `R2` + search saturation (a closed reachable set, which
certifies unreachability, versus an exhausted budget, which certifies nothing);
`R3` + frontier structure; `R4` + semantic witnesses; `R5` full structure.

> **The ladder is a property of the federation's internal channel alphabet, never
> of `M`'s privilege. G1 compares `M` against the TOP RUNG, which receives exactly
> what `M` receives. The study is invalid if `M` is given any task information,
> module report, or oracle label that the top-rung federation is not given.**

## 7. Outcomes and gates

Reported **per family and per arm**, never collapsed into one scalar first:
proof-validity accuracy (with witness re-checking), specification-intent match
(also broken down by registered drift subtype, with the realized draw reported,
since a family average must not hide a subtype that is never detected),
minimal-intervention accuracy, terminal accuracy, the joint endpoint, false
representation-change rate, false-defer rate, missed-escalation rate,
drift-missed rate, false-drift-alarm rate, held-out reuse rate, cost.

A claimed verdict counts only if it **carries a witness that re-checks**: a
`VERIFIED` needs a chain that is an axiom-instance chain; a `REFUTED` needs a
model that satisfies the axioms and falsifies the statement. This is where the
low ladder rungs lose — they can say "refuted" but cannot produce the certificate.

| gate | content |
|---|---|
| **G0** | oracle self-agreement (breadth-first vs iterative-deepening on minimal length; the definable-generator fast path vs brute-force model enumeration), hand-authored known-answer fixtures, parent fidelity, null calibration on a trivial identity |
| **G1** | `M` vs the top-rung federation on the joint endpoint, paired exact binomial, α = 0.05, **per family and pooled** |
| **G2** | anti-conservatism: on `F1`/`F4`, `M`'s false-change and false-defer rates, and its pooled false-drift-alarm rate, may not exceed `B5`'s by more than 0.05 |
| **G3** | mechanism by omission: the registered ablation must degrade the family it controls |
| **G4** | ladder monotonicity and terminal |

**A pooled average may not hide a family-specific failure.** The per-family table
is the primary report; the pooled row is secondary.

### 7.1 Routing

`CANNOT_CHECK` (G0 fails) · `PARENT_SUFFICIENT` (no significant `M` advantage;
the cost delta is reported with it) · `MECHANISM_UNSUPPORTED` (an advantage that
G2 shows is bought by conservatism, or that G3 shows the named omissions do not
remove) · `SPECIFICATION_FIDELITY_RESIDUAL` (the advantage is on fidelity, not on
validity) · `ME_RESIDUAL_SUPPORTED` (G1–G3 all pass).

### 7.2 No-rescue clause

No threshold, family, arm, budget, generator constant or gate may be changed
after any protected outcome has been inspected. The protected stage runs exactly
once and `analyze` runs exactly once on its output. `PARENT_SUFFICIENT` and
`CANNOT_CHECK` are successful scientific terminals and may not be repaired.

## 8. Custody and the protected stage

The protected split seed lives in `~/.orion-custody/me-x3/PROTECTED_SEED_V1.txt`;
its sha256 is frozen in the design JSON. `mex3_run.py protected` refuses to run
unless `PROTECTED_RUN_AUTHORIZATION.json` is present next to it **and** the
custody file's sha256 equals that commitment. Development results are labelled
`DEVELOPMENT` and are never protected evidence; the federation's stage order and
the two budget constants were fixed there, before any protected run, to avoid
ceiling and floor effects.

## 9. Contamination and leakage

The corpus is generated after freeze with arbitrary operator renaming; hidden
transformation identities never appear in the task view; the split is by
generated family and by seed, not by instance; the protected seed is sealed; the
oracle implementation, the expected verdicts and the drift subtypes are in the
custody file only. No protected outcome may be used to tune any threshold.

## Terminal

```text
ME_X3_STATUS = FROZEN_DESIGN_NO_PROTECTED_OUTCOME_INSPECTED
LOCAL_VERIFIER = EXHAUSTIVE_FINITE_ORACLE_PLUS_LEAN_KERNEL_CROSS_CHECK
MATHLIB_USED = FALSE
PROOF_VALIDITY_EQUALS_INTENT_FIDELITY = FALSE
PRIMARY_DECISION = SEARCH_VS_LEMMA_VS_REPRESENTATION_VS_PROBE_VS_REFORMULATE_VS_UNRESOLVED
PRIMARY_COMPARATOR = B5_STRONGEST_FAITHFUL_PARENT_FEDERATION_AT_FULL_STRUCTURE
EXTRA_COMPUTE_COUNTS_AS_ME_RESIDUAL = FALSE
PRE_REGISTERED_EXPECTATION = PARENT_SUFFICIENT
FIELD_STATUS_AUTHORITY = NONE
```
