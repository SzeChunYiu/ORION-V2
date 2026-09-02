# ME-X1 — Cross-Transition Coupling Benchmark: Exact Known-Answer Study (Registered Design V1)

**Class:** exact-oracle known-answer study — **zero model calls, fully
deterministic, CPU-seconds**. It decides whether ORION-V2's registered
transition logic (`M`: problem contract + typed obligations over provenance,
dependence, typed transport, evaluator contract, atlas gluing, authority
ceiling and selective reopening) makes the exact registered **transition
decision** beyond the strongest faithful parent federation `B5` given the same
registered information. **Parent sufficiency is a successful terminal** of
this design and the pre-registered expectation (§1.2), as it was for ME-X4
(`ME_X4_OUTCOME_RECEIPT.md`: `PARENT_SUFFICIENT`, monotone ladder).

**Protocols served:** `ME_X1_TRANSITION_COUPLING_PROTOCOL_V1.md` (§1–§11),
`MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md` §0–§3, the public
development fixtures `ME_X1_X2_DEVELOPMENT_KNOWN_ANSWER_FIXTURES_V1.json`
(X1-DEV-001…014 bound as G0a known answers; the X2 obstruction cases are the
ME-X2 identity and out of scope here), `ME_X2_LOCUS_DIAGNOSIS_PROTOCOL_V2.md`
(the challenged evaluator is never the sole diagnostic authority; an ontic
`TARGET_CHANGED` is registered, never inferred), field synthesis V4 §7/§8/§10
(residual form 4: individually sound parent-local decisions composing
incorrectly without a coupling condition), and H-EXT-3 (family I named there;
the B5 interface ladder is a first-class gate, G4).

**Status:** frozen design + parent baselines + development fixtures. **No
protected outcome has been generated or inspected.** The protected stage
refuses to run (§8).

Companion: `ME_X1_TRANSITION_COUPLING_EXACT_STUDY_DESIGN_V1.json` (schema
`orion.v2.me-x1.exact-study-design.v1`) carries every constant below;
`ME_X1_PARENT_FIDELITY_RECEIPT_V1.md` carries code hashes, parent fidelity
results and the development-split summary.

## 1. Question, hypothesis, expectation

**Q.** Can every local operation be correct under its local contract while
the requested scientific-state transition is unwarranted — and does `M`
choose the exact registered action (§2) beyond `B5`, the strongest faithful
parent federation receiving the same registered information?

**H0 (strongest-parent sufficiency).** An information-matched federation of
contract binding, formal refinement, provenance, dependence-aware synthesis,
typed transport, evaluator coverage, atlas gluing, governance and
truth-maintenance parents, with ordinary engineering glue, makes the same
decisions at equal or lower cost.

**1.2 Pre-registered expectation.** Once every cross-transition condition is
a typed, witness-level module output crossing the federation boundary, `B5`
(JTMS shared state + the registered precedence table as glue) computes the
same decision function as `M`. Expected route: `PARENT_SUFFICIENT`, ladder
terminal `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. The decisive content
is (a) whether any family exposes a composition error in `B5`, (b) where
`B0`–`B4` break (attribution), (c) **where along the ladder the gap appears**
— prediction: at the R4→R5 step, where identity/criterion/specification,
atlas and authority witnesses first cross the boundary, plus the separation
pair at R1, (d) anti-conservatism, (e) cost.

## 2. Frozen inputs: registered actions, state, oracle

### 2.1 Registered transition actions (protocol §2)

`UPDATE`, `PRESERVE`, `SELECTIVELY_REOPEN`, `REVALIDATE`,
`REQUEST_NEW_EVIDENCE`, `BLOCK_TRANSPORT`, `REFORMULATE_PROBLEM`,
`REPLACE_OR_CHALLENGE_EVALUATOR`, `DEFER_CANNOT_CHECK`, `ABSTAIN_AUTHORITY`.
The **decision object** is `(action, reopened-commitment set)`; the set is
non-empty only for `SELECTIVELY_REOPEN`; exactness means both are equal.

### 2.2 Registered information (identical for every arm)

A **World**: claims (context, failure class, scope, criterion id,
`accepted_v0`, intended spec id, global-section witness id, target epoch);
evidence (claim, source, context, scope coverage, evaluator, calibration,
`supports`, identity status); support families (evidence ids, prerequisite
claims, `min_independent` k, `required_relation`); sources
VALID/RETRACTED/DISPUTED; calibrations VALID/INVALID/UNDER_REVIEW; evaluators
(coverage, uncertain, status VALID/INVALID/UNDER_REVIEW); typed context
relations (`orion_v2.structural.RelationType`); dependence declarations
CONFIRMED/SUSPECTED; overlaps (compatible True/False/None + witness); a
criterion-equivalence table; a spec-fidelity table; **results** (bound claim,
basis evidence, context, evaluator, proved spec, checker status, binding
status, comparability status, independence requirement, required relation);
an **authority policy** (ceiling NONE < BELIEF < OPERATIONAL < EXTERNAL,
status). A **TransitionRequest**: kind ∈ {`ACCEPT_RESULT`, `PROPAGATE_DEFEAT`,
`CLOSE_GLOBAL`}, target claim, result id, decision criterion, required
authority level, challenged event index. Twenty-six typed **events** update
the registry (`mex1_model.apply_event`): the fourteen ME-X4 events plus
evaluator invalidated / under review / registered, authority policy changed,
`TARGET_CHANGED` (ontic; registered only), overlap assessed, global witness
registered, spec fidelity assessed, criterion equivalence assessed, result
registered / rebound, comparability assessed, evidence identity lost.

Hidden from arms: the oracle implementation and the expected decisions. No
field of the instance schema is an action.

### 2.3 Atomic conditions (three-valued) and frozen precedence

Request-level atoms are ordered by module rank IDENT < PROV < DEP < TRANS <
EVAL < ATLAS < AUTH; each atom names the action taken when it is the first
INVALID atom:

| module | atom | VALID / UNKNOWN / INVALID | action |
|---|---|---|---|
| IDENT | `identity:R` | bound claim = target; binding unrecoverable → UNKNOWN | REVALIDATE |
| IDENT | `criterion:T` | decision criterion = registered or EQUIVALENT; CANNOT_CHECK → UNKNOWN; NOT_EQUIVALENT/unregistered → INVALID | REFORMULATE_PROBLEM |
| IDENT | `spec:R` (formal) | proved = intended or FAITHFUL; UNFAITHFUL → INVALID; unassessed → UNKNOWN | REVALIDATE |
| IDENT | `checker:R` (formal) | checker VALID/UNKNOWN/INVALID | REQUEST_NEW_EVIDENCE |
| PROV | `src:e` per basis evidence | RETRACTED → INVALID; DISPUTED → UNKNOWN | REQUEST_NEW_EVIDENCE |
| PROV | `ident:e` | identity UNRECOVERABLE → UNKNOWN | REVALIDATE |
| PROV | `cal:e` (if calibrated) | INVALID → INVALID; UNDER_REVIEW → UNKNOWN | REVALIDATE |
| PROV | `comparability:R` (if registered) | NONCOMPARABLE → INVALID; CANNOT_CHECK → UNKNOWN | REVALIDATE |
| DEP | `support:R` (k > 0) | components over CONFIRMED < k → INVALID; over CONFIRMED+SUSPECTED < k → UNKNOWN | REQUEST_NEW_EVIDENCE |
| TRANS | `transport:R` (contexts differ) | no relation → INVALID; CANNOT_CHECK → UNKNOWN; rank ≥ required → VALID | BLOCK_TRANSPORT |
| EVAL | `evaluator:R` | status INVALID → INVALID; UNDER_REVIEW → UNKNOWN; class in coverage → VALID; in uncertain → UNKNOWN; blind with a registered valid alternative → INVALID; blind with none → UNKNOWN | REPLACE_OR_CHALLENGE_EVALUATOR |
| ATLAS | `piece:c` (CLOSE_GLOBAL) | derived: Kleene support of the local claim | REQUEST_NEW_EVIDENCE |
| ATLAS | `overlap:o` | True/None/False | REFORMULATE_PROBLEM |
| ATLAS | `witness:T` | witness registered → VALID; absent (MATCHING_FAMILY_ONLY) → UNKNOWN | REFORMULATE_PROBLEM |
| AUTH | `authority` | policy UNDER_REVIEW → UNKNOWN; ceiling ≥ required → VALID | ABSTAIN_AUTHORITY |

Support-graph atoms (`src`, `ident`, `cal`, `evc`, `tr:F:e`, `ind:F`,
`nocontra:c`) follow ME-X4 §2.3; basis atoms share their ids with the
support graph so that a resolution of censored atoms is consistent. Relation
strength order as in ME-X4. Authority is checked **last**: `ABSTAIN_AUTHORITY`
means "epistemically warranted, not authorized" (fixture X1-DEV-010).

### 2.4 Exact oracle

*ACCEPT_RESULT / CLOSE_GLOBAL:* precedence walk with the **singleton rule** —
the action is the one taken under every resolution of the censored atoms
(first INVALID atom's action, `UPDATE` if none); if the resolutions disagree,
the exact action is `DEFER_CANNOT_CHECK`. *PROPAGATE_DEFEAT:* Kleene support
over the graph; R = commitments unsupported under every resolution, U =
commitments whose support depends on it; U ≠ ∅ → `DEFER_CANNOT_CHECK`;
R ≠ ∅ → `SELECTIVELY_REOPEN(R)`; else `PRESERVE`. Two computations run on
every instance and must agree (G0b): the walk/Kleene decision and
**exhaustive enumeration** of all 2^u resolutions of the censored base atoms
(u ≤ 8 by generator cap). The oracle also records the decisive module and
atom (for the laundering outcomes) and the action set over resolutions.

### 2.5 Generator

Base state: 3–6 accepted claims in ≤ 3 layers; 1–2 families per claim; 1–3
evidence per family (prerequisite-only 20%); 4–6 sources + one unused; 2
instruments × 1–2 calibrations + one unused; 3 evaluators (ev0 covers every
failure class); typed relations among 3 contexts; k = 2 on 30% of
≥ 2-evidence families; authority ceiling OPERATIONAL. **Pre-event validity**
(every accepted claim supported with all atoms VALID at v0) is checked by
the oracle. Each family's planter builds the request and mutates the state /
emits 0–3 events for the scheduled variant; the family invariant (action,
decisive atom, reopened membership, decoy non-membership) is checked by the
oracle; deterministic rejection sampling under
`seed = sha256(split_seed|family|index)[:12]`. Variant schedule by index
(frozen cycle, 50/30/20 per 100): POS, NEG, AMB, POS, NEG, POS, POS, NEG,
POS, AMB.

### 2.6 Finite separation example (H-EXT-3)

The ME-X4 pair P/Q recast as a `PROPAGATE_DEFEAT` transition (composition of
a dependence defeat and a transport defeat across families): P → `SELECTIVELY_REOPEN {c}`,
Q → `PRESERVE`; any federation exporting only family-anonymous per-module
verdicts emits identical outputs on P and Q and errs on one. The selftest
asserts exactly this (rung 1 identical and wrong on one; rung 5 and M exact
on both).

## 3. Case families (protocol §3) and counts

Protected: **100 per family, 1 000 total** (50 positive / 30 negative / 20
ambiguity each). Development: 4 per family, 40 (≤ 5 per family).

| family | positive | negative (warranted) | ambiguity |
|---|---|---|---|
| X1-A claim/problem identity | result bound to a sibling claim with identical output (REVALIDATE); decision criterion not registered/equivalent (REFORMULATE_PROBLEM) | correct binding, identical output; registered EQUIVALENT criterion; decoy event (UPDATE) | binding unrecoverable; basis identity lost (X1-DEV-014); equivalence CANNOT_CHECK (DEFER) |
| X1-B measurement/calibration | basis calibration invalidated; comparability NONCOMPARABLE (REVALIDATE) | sibling calibration of the same instrument invalidated, unused by the basis; **registered ontic `TARGET_CHANGED` with comparability COMPARABLE** (UPDATE) | calibration UNDER_REVIEW; comparability CANNOT_CHECK (DEFER) |
| X1-C hidden dependence | defeat: target's only family needs k=2, dependence defeats it, decoy dependence elsewhere leaves k satisfied (SELECTIVELY_REOPEN, decoy out); accept: basis needs k=2 (REQUEST_NEW_EVIDENCE) | independent second family or k still satisfied (PRESERVE) | dependence SUSPECTED (DEFER) |
| X1-D invalid transport | donor-context result, relation retyped below the required strength or absent; decoy relation retyped elsewhere (BLOCK_TRANSPORT) | typed valid transport; decoy weakening of another relation (UPDATE) | relation CANNOT_CHECK (DEFER) |
| X1-E defeated prerequisite | all sufficient routes share a retracted source; target is the sole prerequisite of a downstream claim (SELECTIVELY_REOPEN incl. dependents) | one route retracted, an independent route remains (PRESERVE) | retraction DISPUTED (DEFER) |
| X1-F evaluator blindness | evaluator built without the claim's failure class while a registered valid alternative covers it; validity contract invalidated (REPLACE_OR_CHALLENGE_EVALUATOR) | evaluator covers; decoy narrowing of an unused evaluator (UPDATE) | class re-scoped to one no evaluator covers (X1-DEV-009); coverage uncertain; evaluator under review (DEFER) |
| X1-G authority mismatch | operational/external adoption above the ceiling (ABSTAIN_AUTHORITY) | within ceiling; ceiling raised (UPDATE) | policy UNDER_REVIEW (DEFER) |
| X1-H proof / wrong specification | checker VALID on a statement registered UNFAITHFUL (REVALIDATE); checker INVALID on a faithful statement (REQUEST_NEW_EVIDENCE) | identical specification or FAITHFUL refinement, checker VALID (UPDATE) | fidelity unassessed; checker UNKNOWN (DEFER) |
| X1-I local compatibility / global obstruction | explicit incompatible overlap = `GLOBAL_SECTION_OBSTRUCTED` (REFORMULATE_PROBLEM) | all overlaps compatible + separate global-section witness (UPDATE) | witness absent = `MATCHING_FAMILY_ONLY` (X1-DEV-012); an overlap unresolved (DEFER) |
| X1-J fully warranted | ACCEPT (plain / transported / operational within ceiling / formal faithful) with 1–2 decoy events (UPDATE) | PROPAGATE_DEFEAT with partial family failure / k-satisfied dependence / unrelated retraction (PRESERVE) | censoring on **unrelated** entities only: UPDATE/PRESERVE, never DEFER |

**Seed commitment.** Protected seed sha256
`84ae78f5676879bfa022460bc17ae36233935e3bdfef4a63a670d9eda431c34d` (operator
custody `~/.orion-custody/me-x1/PROTECTED_SEED_V1.txt`, mode 600; the runner
verifies the hash before any protected generation; the seed string is
revealed in the outcome receipt). Development seed (public): `ME-X1-DEV-20260902`.

**Power / MDE.** Primary statistic = paired instance-level exact decision
M vs B5, exact two-sided binomial test on discordant pairs (McNemar exact);
estimand P(M exact) − P(B5 exact) with a paired Wald interval. Pooled
n = 1 000: 6 one-directional discordants (0.6%) reach p = 0.031, 8 reach
p = 0.008. Per family n = 100: 6 discordants reach p = 0.031. The prior
expectation is zero discordance; the test is two-sided.

## 4. Arms (protocol §4)

| arm | semantics | information policy |
|---|---|---|
| `B0_DIRECT` | local checks pass → proceed (UPDATE / PRESERVE; checker fails → REQUEST_NEW_EVIDENCE) | no cross-transition condition |
| `B1_CALIBRATED_ABSTENTION` | B0 + untyped uncertainty gate: any non-nominal or changed status in the request lineage → DEFER | untyped |
| `B2_PROVENANCE_PLUS_VERIFIER` | `orion_v2.provenance` revocation descendants over the execution graph (sources, calibrations, evaluators, relations, target epochs → evidence, families, results, claims) + local verifier; artifact-lineage identity | typed lineage; two-valued; no criterion/spec/dependence/transport-rank/coverage/atlas/authority vocabulary |
| `B3_PARENT_NATIVE_ASSURANCE` | GSN change-impact over the registered argument with typed context elements; AND semantics; challenged goal → REVALIDATE (re-argue) or reopen | typed contexts; two-valued; single repair action |
| `B4_PARENT_MODULES_WITH_SHARED_STATE` | typed provenance/dependence/transport/evaluator modules, JTMS shared state, registered precedence glue; identity by lineage only; pairwise compatibility taken as global; no authority module | TMS-federation vocabulary (decisive protocol §2 B4) |
| `B5_R1_VERDICT_ONLY` … `B5_R4_PROV+DEP+TRANS+EVAL` | H-EXT-3 rungs: all seven parents typed; modules below the rung's witness level export one per-claim and one per-request **verdict** atom carrying the module default action (IDENT/PROV → REVALIDATE, DEP → REQUEST_NEW_EVIDENCE, TRANS → BLOCK_TRANSPORT, EVAL → REPLACE…, ATLAS → REFORMULATE_PROBLEM, AUTH → ABSTAIN_AUTHORITY) | ablations of B5 |
| **`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`** (rung 5) | full structure = everything M sees; JTMS envelope + registered precedence table | **primary comparator** |
| **`M_ME_TRANSITION_CONTROL`** | `orion_v2.contracts.ProblemContract` (identity, scope, authority requirements) + one typed `Obligation` per condition (SATISFIED / DEFEATED / CENSORED / AUTHORITY_BLOCKED) fed by the parent-owned reference modules (`orion_v2.provenance`, `orion_v2.evidence.assess_evidence_dependence`, `RelationType`, `orion_v2.comparability.ComparabilityCertificate`, `orion_v2.epistemic_atlas.assess_atlas_gluing`) + `orion_v2.reopening.selective_reopen` envelope + the registered precedence walk to a `Terminal` | no answer key; registered information only |

Parents (each passing native known-answer tests before use; receipt §2):
JTMS, assurance case, provenance-only (vendored from ME-X4); contract binding,
refinement fidelity, independence witness, transport licence, metrology
comparability, evaluator coverage, atlas gluing, authority lattice.

**Ablations (protocol §6, eight) + one:** `M_MINUS_PROBLEM_IDENTITY`,
`M_MINUS_DEPENDENCE`, `M_MINUS_EVALUATOR_CONTRACT`, `M_MINUS_TRANSPORT`,
`M_MINUS_SUPPORT_REOPENING` (families merged into one AND family),
`M_MINUS_AUTHORITY`, `M_MINUS_UNRESOLVED_TERMINAL` (censored = satisfied),
`M_MINIMAL_RECEIPT` (atom kinds dropped by the development-frozen backward
elimination rule; the dropped set is frozen in the design JSON:
`witness, piece, evc, tr, comparability, ident, checker, criterion, nocontra`
— the development split does not exercise every sub-variant, and the
protected split measures what a receipt minimised on development loses),
plus `M_MINUS_MEASUREMENT_COMPARABILITY` (beyond §6: family B has no
omission-specific ablation among the eight). **Controls:** `C_ALWAYS_UPDATE`,
`C_ALWAYS_DEFER`, `C_RANDOM_ACTION`.

## 5. Primary outcome vector (protocol §7), per family and per variant

Exact transition decision; false update; missed warranted update; over- and
under-reopening (commitment level); invalid transport; false closure
(oracle DEFER, arm UPDATE/PRESERVE); evaluator laundering (oracle decisive
module EVAL, arm UPDATE); problem/specification laundering (decisive IDENT,
arm UPDATE); authority laundering (oracle ABSTAIN, arm UPDATE); correct
unresolvedness; **warranted-transition recall** and **unnecessary
defer/abstain rate** (protocol §8); cost (module + engine ops; wall-clock in a
separate timing file, the only commensurable scale). All arms × all families
× all variants are reported in full.

## 6. Gates (frozen before any protected outcome exists)

- **G0a `KNOWN_ANSWER` (hard):** the 14 public fixtures and the separation
  pair reproduced by the oracle, and M and B5 exact on all of them (selftest).
- **G0b `ORACLE_SELF_AGREEMENT` (hard):** walk/Kleene = exhaustive on every
  instance; every instance valid at v0; family invariants hold.
- **G0c `NULL_CALIBRATION` (hard):** `C_ALWAYS_UPDATE` exact = 0 where the
  oracle is not UPDATE/PRESERVE; `C_ALWAYS_DEFER` exact = 0 where the oracle
  is determinate; `C_RANDOM` exact ≤ 20%; M vs permuted oracle decisions
  (mean over 200 permutations) exact ≤ 35% (chance = Σ action-frequency², reported).
- **G1a `B5_REPRODUCES_M`:** decisions identical on ≥ 99.5% of instances and
  no family > 5% discordant.
- **G1b `M_ADVANTAGE`:** paired exact difference M − B5 > 0, exact two-sided
  p ≤ 0.05, ≥ 1 family with ≥ 5 M-only-exact instances.
- **G2 `ANTI_CONSERVATISM`:** M's unnecessary defer/abstain count ≤ B5's and
  M's warranted-transition recall ≥ B5's (warranted = every NEGATIVE variant
  and family J).
- **G3 `MECHANISM`** (only if G1b): for each family with ≥ 5 M-only-exact
  instances, the matching omission ablation's exact rate ≤ B5's (A,H →
  PROBLEM_IDENTITY; B → MEASUREMENT_COMPARABILITY; C → DEPENDENCE; D →
  TRANSPORT; E → SUPPORT_REOPENING; F → EVALUATOR_CONTRACT; G → AUTHORITY;
  I,J → UNRESOLVED_TERMINAL).
- **G4 `INTERFACE_LADDER`** (H-EXT-3): (a) no rung k+1 significantly worse
  than rung k; (b) rung-5 gap = the G1 paired test. Terminals: monotone ∧ gap
  null → `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`; monotone ∧ gap persists
  → `CONTROL_RESIDUAL_CANDIDATE_AT_FULL_STRUCTURE`; non-monotone →
  `LADDER_NON_MONOTONE`.
- **COST:** wall-clock ratio with a 2× flag; reported, never a route.

## 7. Pre-registered routing

| outcome | route |
|---|---|
| G0 fail | `CANNOT_CHECK` — lane defect; repair, re-freeze, no arm verdict |
| G1a pass | `PARENT_SUFFICIENT` (with G4a: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`) |
| G1b pass ∧ G2 fail | `M_OVER_CONSERVATIVE` |
| G1b pass ∧ G2 pass ∧ G3 pass | `ME_X1_RESIDUAL_CANDIDATE` |
| G1b pass ∧ G2 pass ∧ G3 fail | `CANNOT_CHECK` — advantage not attributable to a named condition |
| neither G1a nor G1b | `PARENT_SUFFICIENT` |

**Field-support rule (protocol §10, restated).** X1 supports a nontrivial
residual only if at least one protected family satisfies all of: (1) B5 has
the information and parent mechanisms locally (true by construction at rung
5); (2) B5 makes a systematic composition error (G1b in that family); (3) M
avoids it because of a predeclared cross-transition condition (the oracle's
decisive module); (4) the matching omission ablation restores the error (G3);
(5) the effect transfers to an independently authored / native-reviewed
family — **the separate naturalistic cell (§9), not this study**; (6) M does
not obtain the gain by over-conservatism (G2). Otherwise X1 is at most a
benchmark/integration result. Kill conditions of protocol §11 map onto
`PARENT_SUFFICIENT`, `M_OVER_CONSERVATIVE`, and the design invariants (arms
receive only registered information; the oracle is never imported by an arm;
M has no evaluator access B5 lacks).

**Naturalistic transfer (protocol §9)** is declared a **separate later
cell**: ≥ 2 independently authored / native-reviewed case families from
materially distinct modes (formal mathematics / software verification;
measurement science; evidence synthesis); native reviewers define the
protected decision and the strongest parent before seeing arm outcomes.
Nothing from this exact study transfers to it.

## 8. Custody and protected-run discipline

- Code: `mex1_model.py`, `mex1_oracle.py`, `mex1_generator.py`,
  `mex1_parents.py`, `mex1_arms.py`, `mex1_run.py`; sha256 frozen in the
  receipt. Determinism: results and custody files byte-identical on re-run
  (only RNGs: instance seeds, the random-control seed, the shuffle-null seed
  20260902); wall-clock lives in a separate timing file.
- Stages: `selftest`, `dev` (≤ 5 per family, label DEVELOPMENT, never
  protected; also derives the minimal-receipt kinds), `protected`, `analyze`.
- The `protected` stage **refuses** unless `PROTECTED_RUN_AUTHORIZATION.json`
  (human_written = true, a human-written token ≥ 16 chars,
  `acknowledged_design_sha256` = sha256 of the frozen design JSON) is present
  next to the runner **and** the custody seed hashes to the commitment. The
  file is absent at design freeze; the tests assert its absence and the
  refusal paths; `.gitignore` blocks protected outputs.
- Outputs: `results/ME_X1_<LABEL>_RESULTS_V1.json` (arm decisions only),
  `…_EXPECTED_CUSTODY_V1.json`, `…_TIMING_V1.json`, `…_ANALYSIS_V1.{json,md}`.
- Estimated protected cost: 1 000 instances × 23 arms ≈ 10–30 CPU-seconds
  (development: 40 instances, all arms, minimal-receipt derivation and
  analysis in ≈ 0.5 s). Deterministic Python on the Mac.

## 9. Non-goals, no-rescue clause, resolved ambiguities

No family weight, oracle rule, precedence, arm, seed or gate changes after
the protected results file exists. Development-only tuning surface: bug
fixes to arm glue validated by G0a before the seed is revealed. A protected
result is never re-run under a new seed; a lane defect found mid-run halts
the lane, is receipted, and re-freezes as V2. No field status, novelty or
publication authority.

Ambiguities resolved at design time: (1) the protocol allows "one or more"
actions per case; this study freezes **one** action plus a reopened set, with
`DEFER_CANNOT_CHECK` as the exact answer whenever the censored resolutions
disagree (the action set is recorded); (2) source retraction of a basis →
`REQUEST_NEW_EVIDENCE` (the evidence is gone) but calibration break /
comparability / identity mismatch / unfaithful specification → `REVALIDATE`
(recompute or rebind); (3) a blind evaluator with no registered alternative
is *uncheckable* (`DEFER`, X1-DEV-009), with a registered alternative it is
*replaceable*; (4) an explicit incompatible overlap is `GLOBAL_SECTION_OBSTRUCTED`
→ `REFORMULATE_PROBLEM` (the global claim as posed cannot be glued), an
absent witness is `MATCHING_FAMILY_ONLY` → `DEFER` (X1-DEV-012); (5)
authority is checked last, after every epistemic condition; (6) `TARGET_CHANGED`
is a registered ontic fact that does not by itself defeat any condition
(locus protocol V2: the machine never infers it); (7) a `PROPAGATE_DEFEAT`
request is decided over all accepted commitments (all supported at v0 by
construction); (8) `B2` invalidates downstream of a changed target epoch, as
execution-graph runtimes do — its unnecessary revalidation on the ontic
control is a native property, not a handicap; (9) cycles are out of scope
(DAG by construction); (10) the X2 obstruction fixtures are not bound here.
