# ME-X4 — Selective Reopening under Dynamic Evidence: Exact Known-Answer Study (Registered Design V1)

**Class:** exact-oracle known-answer study — **zero model calls, fully
deterministic, CPU-minutes**. It decides whether ORION-V2's selective
reopening (`src/orion_v2/reopening.py` over typed support families) makes
reopening/preservation/unresolved decisions that the strongest faithful parent
federation cannot reproduce from the same registered information. **Parent
sufficiency is a successful terminal** of this design, and it is the
pre-registered expectation (§1.2).

**Protocols served:** `ME_X4_SELECTIVE_REOPENING_PROTOCOL_V1.md` (§2–§8
verbatim), `MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md` §0–§2 and §6,
`MACHINE_EPISTEMICS_FIELD_SYNTHESIS_V4.md` §7 ("no ME residual exists if
[truth-maintenance/belief-revision/assurance parents] recover the same
decisions"), §8 (provenance and reopenability are parent-owned), §10 (what
counts as a residual). Ontology: every event here is an **epistemic
transition** `E_{t+1} = U(E_t, o, a, ρ)` of `WORLD_MACHINE_SEPARATION_ONTOLOGY_V1.md`
§2 — retractions, dependence discoveries, evaluator audits and scope changes
change what the machine knows, never the world.

**Secondary axis (H-EXT-3):** the B5 interface-information ladder of
`research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md`
(PR #138, main `2f3b561`) is pre-registered here with its own gate (G4, §6.5)
and the finite separation example it asks for (§2.6).

**Status:** frozen design + parent baselines + development fixtures. **No
protected outcome has been generated or inspected.** The protected stage
refuses to run (§8).

Companion: `ME_X4_SELECTIVE_REOPENING_EXACT_STUDY_DESIGN_V1.json` (schema
`orion.v2.me-x4.exact-study-design.v1`) carries every constant below;
`ME_X4_PARENT_FIDELITY_RECEIPT_V1.md` carries code hashes, parent fidelity
results and the development-split summary.

## 1. Question, hypothesis, expectation

**Q.** When evidence ancestry, calibration, transport or evaluator validity
changes, does `M` reopen *exactly* the commitments whose registered
sufficient support failed, preserve the independently supported ones, and
mark the censored ones unresolved — and does it do so beyond `B5`, the
strongest faithful parent federation receiving the same registered
information?

**H0 (strongest-parent sufficiency).** An information-matched federation of
truth maintenance (JTMS/ATMS), belief revision, provenance, dependence-aware
evidence synthesis, typed transport and assurance-case update makes the same
decisions at equal or lower cost.

**1.2 Pre-registered expectation.** On acyclic registered support graphs,
both `selective_reopen`'s fixed point and a JTMS/ATMS federation compute the
same monotone-formula semantics once typed information crosses the module
boundary. The expected route is therefore `PARENT_SUFFICIENT` with ladder
terminal `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. The decisive content of
the study is (a) whether any generated stratum breaks this by exposing a
composition error in B5, (b) where single parents break (attribution), (c) the
ladder (H-EXT-3), and (d) cost. A `PARENT_SUFFICIENT` outcome contracts the X4
residual to an interface convention, exactly as protocol §6.5 and field §7
foresee.

## 2. Frozen inputs: generator and exact oracle

### 2.1 Registered information (identical for every arm)

A **World** at each version: claims (context, failure class, scope,
`accepted_v0`, `alternative_of`); evidence units (claim, source, context,
scope coverage, evaluator, calibration, data/model/instrument, `supports`);
**support families** (evidence ids, prerequisite claims, `min_independent`
k, `required_relation`); sources (VALID/RETRACTED/DISPUTED); calibrations
(VALID/INVALID/UNDER_REVIEW); evaluators (coverage, uncertain); typed context
relations (`orion_v2.structural.RelationType`); dependence declarations
(CONFIRMED/SUSPECTED). Fourteen typed **events** update the registry
(`mex4_model.apply_event`): source retracted / disputed / corrected;
calibration invalidated / under review / revalidated; dependence discovered /
suspected; relation retyped (incl. `CANNOT_CHECK`); evaluator coverage changed;
claim failure class changed; claim scope changed; family added; evidence
added (positive = new support, negative = contradiction registered).

Every arm receives the World at every version, the event history and the
accepted list. Hidden from arms: the oracle implementation and the expected
sets (custody file).

### 2.2 Coverage of protocol §2

| Protocol §2 item | Representation |
|---|---|
| claims and alternative hypotheses | claims; `alt0` rejected at v0 by valid negative evidence (50% of instances) |
| multiple sufficient support families | 1–3 families per claim, OR semantics |
| necessary and sufficient prerequisites | `prerequisite_ids` inside families (a family is sufficient; a prerequisite is necessary for that family); prerequisite-only families (20%) |
| shared source/data/model/instrument ancestry | shared `source_id`, calibrations per instrument, provenance graph |
| independent redundant support | families with `min_independent = k` over evidence with no registered dependence |
| retractions/corrections | SOURCE_RETRACTED / SOURCE_CORRECTED, CALIBRATION_INVALIDATED / REVALIDATED |
| calibration or measurement invalidation | calibration nodes under instruments |
| context/transport invalidation | evidence in a foreign context uses a typed relation; family records required strength |
| evaluator replacement / failure-class change | evaluator coverage sets; claim failure classes |
| scope/criterion change | claim scope vs union of family evidence coverage (`ProblemContract.scope` on the M side) |
| unresolved/censored edges | DISPUTED / UNDER_REVIEW / SUSPECTED / CANNOT_CHECK statuses |
| negative evidence and contradiction edges | evidence with `supports=False` against a claim |

### 2.3 Atomic conditions (three-valued)

| atom | present when | VALID / UNKNOWN / INVALID |
|---|---|---|
| `ev:e` | always | source RETRACTED or calibration INVALID → INVALID; source DISPUTED or calibration UNDER_REVIEW → UNKNOWN |
| `evc:e` | evidence has an evaluator | claim failure class ∈ coverage → VALID; ∈ uncertain → UNKNOWN; else INVALID |
| `tr:F:e` | evidence context ≠ claim context | no relation → INVALID; `CANNOT_CHECK` → UNKNOWN; rank(relation) ≥ rank(required) → VALID |
| `ind:F` | `min_independent > 0` | components over CONFIRMED < k → INVALID; over CONFIRMED+SUSPECTED < k → UNKNOWN |
| `scope:F` | family has positive evidence | ∪ coverage ⊇ claim scope → VALID (prerequisite-only families inherit scope) |
| `nocontra:c` | always | valid negative evidence → INVALID; censored negative evidence → UNKNOWN |

Frozen relation strength order: ISOMORPHIC 5 > BEHAVIORALLY_EQUIVALENT 4 >
PREDICTIVELY_EQUIVALENT 3 > DECISION_DOMINATES 2 > APPROXIMATELY_EQUIVALENT 1
> INCOMPARABLE = DISTINGUISHED_BY 0; CANNOT_CHECK is censored.

### 2.4 Exact oracle

Family = AND(atoms) AND AND(prerequisites supported); claim = OR(families)
AND `nocontra`, Kleene three-valued, bottom-up over the prerequisite DAG.
Dispositions over the accepted-at-v0 set: **PRESERVED** = supported under
every resolution of censored atoms; **REOPENED** = unsupported under every
resolution; **UNRESOLVED** otherwise. Two computations run on every version
and must agree (G0b): the Kleene fixed point and **exhaustive enumeration**
of all 2^u resolutions (u ≤ 8 by generator cap). Prerequisite graphs are DAGs
by construction, so `CANNOT_CHECK_CYCLE` never arises; cyclic support is out
of scope for this exact study (ambiguity resolved, §9).

### 2.5 Generator

Base world: 4–8 accepted claims in ≤ 3 layers; 1–3 families per claim; 0–3
evidence per family (+1 transported unit in some strata; ≤ 4 total); 4–7
sources plus one unused; 2 instruments × 1–2 calibrations plus one unused; 3
evaluators; typed relations among 3 contexts; k = 2 on 35% of ≥ 2-evidence
families; alternative hypothesis in 50%. **Pre-event validity** (every
accepted claim supported with all atoms VALID at v0) is checked by the oracle.
Each stratum's planter mutates the base world at v0, emits 1–3 events, and
the stratum invariant (§3) is checked by the oracle; deterministic rejection
sampling under `seed = sha256(split_seed|stratum|index)[:12]`.

### 2.6 Finite separation example (H-EXT-3, family "local compatibility / global obstruction")

Instances P and Q share the event sequence *dependence discovered (e1, e2);
relation ctx1→ctx0 retyped to APPROXIMATELY_EQUIVALENT*:

- **P:** `c` has F1 = {e1, e2 | k = 2}, F2 = {e3 transported, requires
  PREDICTIVELY_EQUIVALENT}. Oracle: F1 and F2 both defeated → **REOPENED**.
- **Q:** `c` has F1 = {e1, e2, e3 transported | k = 2 over e1, e2}, F2 = {e4
  native}. Oracle: F1 defeated twice over, F2 intact → **PRESERVED**.

Any federation whose inter-module channel carries only *family-anonymous
per-claim verdicts from a fixed finite alphabet* (DEFEATS_ALL / DEFEATS_SOME
/ UNKNOWN / NONE) receives the identical verdict tuple in P and Q — the
dependence module says DEFEATS_SOME in both, the transport module says
DEFEATS_SOME in both, every other module says NONE — and therefore errs on at
least one of them: each module's local verdict is compatible with
preservation, but in P the defeats jointly cover all families (a global
obstruction visible only when the *identity* of the defeated family crosses
the boundary). Witness-level exchange is exact on both. The selftest asserts
exactly this (verdict-only rung: identical outputs on P and Q and one error;
rung 5 and M exact on both).

## 3. Event strata (protocol §3 verbatim) and counts

Protected: **100 per stratum, 1 200 total**. Development: 3 per stratum, 36.

| stratum | planted structure / invariant checked by the oracle |
|---|---|
| `SOURCE_RETRACTED` | shared ancestry; a claim with an alternative family PRESERVED, a claim with all families touched REOPENED |
| `DEPENDENCE_DISCOVERED` | target family `ind` INVALID (k = 2 or 3); decoy where the edge leaves k satisfied or no requirement exists stays VALID |
| `CALIBRATION_INVALIDATED` | evidence under the calibration INVALID; sibling calibration of the same instrument PRESERVED |
| `TRANSPORT_RELATION_INVALIDATED` | relation retyped below the family's required strength; decoy relation retyped but still sufficient |
| `EVALUATOR_BLIND_OR_REPLACED` | BLIND / REPLACED_NARROWER / FAILURE_CLASS_CHANGED; sibling evaluated by the same evaluator PRESERVED |
| `PROBLEM_SCOPE_CHANGED` | old family's scope atom INVALID; covering family → PRESERVED, else REOPENED |
| `NEW_INDEPENDENT_SUPPORT` | ADD_ONLY or FAIL_THEN_ADD; final reopened = unresolved = ∅; recovery scored |
| `CORRECTION_RESTORES_SUPPORT` | reopened at v1; after correction reopened = unresolved = ∅ |
| `PARTIAL_SUPPORT_FAILURE` | strict subset of families defeated; target PRESERVED |
| `ALL_SUFFICIENT_SUPPORT_FAILED` | SHARED_SOURCE / CONTRADICTION / SEQUENCE; target with a dependent claim REOPENED |
| `CANNOT_CHECK_EDGE` | five censoring variants; ≥ 1 UNRESOLVED; sibling with alternative family PRESERVED |
| `NO_REOPENING_NEEDED` | 1–2 registered events touching used entities; reopened = unresolved = ∅ at every version |

**Seed commitment.** Protected seed sha256
`1314772902394af2583d924bc7eeb15f492e5aa8480dae3ac8cf9a93bfe12af9`
(operator custody `~/.orion-custody/me-x4/PROTECTED_SEED_V1.txt`, mode 600;
the runner verifies the hash before any protected generation; the seed string
is revealed in the outcome receipt so the split can be regenerated
byte-for-byte). Development seed (public): `ME-X4-DEV-20260902`.

**Power / MDE.** Primary statistic = paired instance-level exact-set match
(all versions, all three sets) M vs B5, exact two-sided binomial test on
discordant pairs (McNemar exact); estimand P(M exact) − P(B5 exact) with a
paired Wald interval. Pooled n = 1 200: 6 one-directional discordants (0.5%)
reach p = 0.031, 8 reach p = 0.008. Per stratum n = 100: 6 discordants (6%)
reach p = 0.031. The prior expectation is zero discordance; the test is
two-sided so a B5 advantage is equally detectable.

## 4. Arms (protocol §4)

Single faithful parents (each passes its own native known-answer tests before
use; `mex4_parents.fidelity_selftests`, receipt §2):

| arm | native semantics | information policy |
|---|---|---|
| `A0_PROVENANCE_ONLY_INVALIDATION` | `orion_v2.provenance` revocation descendants over sources, calibrations, evaluators, relations, scope and contradiction nodes, evidence, families, claims | no families; censored = not revoked; no dependence node |
| `A1_JTMS_CLASSICAL` | Doyle 1979 (IN/OUT, in/out-lists, well-founded support, DDB culprit retraction; algorithm after Forbus & de Kleer 1993 ch. 7) | untyped: identity change = premise retraction; two-valued |
| `A2_ATMS_CLASSICAL` | de Kleer 1986 (assumptions, minimal consistent environments, nogoods, subsumption) | untyped; censored atoms expressed through the environment lattice |
| `A3_AGM_KERNEL_CONTRACTION` | Hansson kernel contraction, entrenchment rules < evidence, Levi revision on contradiction | untyped; stateful base without recovery; two-valued |
| `A4_BAYES_NOISY_OR` | noisy-OR support propagation, r = 0.9 evidence, 1.0 structural witnesses, τ = 0.5 | untyped; optimistic/pessimistic envelope |
| `A5_ASSURANCE_CASE_UPDATE` | GSN change impact: challenged → suspect ancestors via supported-by / in-context-of | context elements typed; AND semantics; two-valued |

**B5 ladder (H-EXT-3)** — typed modules (provenance via `orion_v2.provenance`;
dependence via `orion_v2.evidence.assess_evidence_dependence`; transport via
`RelationType` rank; evaluator coverage; scope; contradiction), JTMS
propagation with the censored-atom envelope. Rungs differ only in what
crosses the module boundary:

| rung | witness-level export | everything else |
|---|---|---|
| `B5_R1_VERDICT_ONLY` | none | per-claim verdict atom per module |
| `B5_R2_PROV` | provenance records (evidence statuses) | verdict |
| `B5_R3_PROV+DEP` | + dependence ancestry (family independence witnesses) | verdict |
| `B5_R4_PROV+DEP+TRANS+EVAL` | + typed transport and evaluator statuses | verdict |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` (rung 5) | full structure = everything M sees | — |

Verdict compression rule (frozen): module defeats every family → INVALID;
defeats-or-censors every family with ≥ 1 censored → UNKNOWN; else VALID; the
verdict atom is attached to every family of the claim so prerequisites still
propagate. **Rung 5 is the primary comparator**; rungs 1–4 are ablations of
B5, not of M. B5 is never artificially isolated: it reuses the parent-owned
ORION reference implementations and any engineering glue it needs.

**`M_ME_SELECTIVE_REOPENING`** — the existing reference semantics, no new M:
`ReticulateProvenance.descendants` for revocations, `assess_evidence_dependence`
for independence witnesses, `RelationType` rank for transport, evaluator
coverage, `ProblemContract.scope` for scope, then
`orion_v2.reopening.selective_reopen` run twice (censored = valid / censored =
invalid). For monotone support this envelope is exact and equals the
exhaustive oracle; the study checks that empirically on every instance.

**Ablations / controls (protocol §6):** `M_MINUS_DEPENDENCE_ANCESTRY`,
`M_MINUS_TYPED_TRANSPORT`, `M_MINUS_EVALUATOR_CONTRACT`,
`M_MINUS_SUPPORT_FAMILIES` (families merged into one AND family),
`M_GLOBAL_RESET_CONTROL`, `M_PROVENANCE_ONLY_CONTROL` (= A0), plus
`C_NEVER_REOPEN` and `C_RANDOM_DISPOSITION`.

## 5. Outcomes (protocol §5)

Per arm: instance exact-set match (all versions; reopened, preserved,
unresolved all equal), final-version exact match, over-reopening (arm
REOPENED ∧ oracle PRESERVED), under-reopening (oracle REOPENED ∧ arm ≠
REOPENED), invalid preservation (arm PRESERVED ∧ oracle ≠ PRESERVED), false /
missed unresolved, recovery after corrective evidence (commitments reopened at
an earlier version and preserved at the final version: arm final =
PRESERVED), cost (engine-native primitive operations + module operations,
reported; wall-clock, the only commensurable scale, drives the 2× flag), and
the per-stratum error table. All arms × all strata are reported in full.

## 6. Gates (frozen before any protected outcome exists)

- **G0a `KNOWN_ANSWER` (hard):** the 12 hand-authored fixtures (one per
  stratum, expected sets computed by hand) and the separation pair are
  reproduced by the oracle in `selftest`.
- **G0b `ORACLE_SELF_AGREEMENT` (hard):** Kleene = exhaustive on every version
  of every instance; every instance valid at v0; stratum invariants hold.
- **G0c `NULL_CALIBRATION` (hard):** `C_NEVER_REOPEN` exact = 0 on instances
  whose oracle reopens/censors something; `M_GLOBAL_RESET_CONTROL` exact = 0
  on instances whose oracle mixes preserved with reopened/unresolved;
  `C_RANDOM` exact ≤ 10%; M scored against within-instance shuffled oracle
  labels exact ≤ 10%.
- **G1a `B5_REPRODUCES_M`:** decisions identical (all versions) on ≥ 99.5% of
  instances and no stratum > 5% discordant.
- **G1b `M_ADVANTAGE`:** paired instance-exact difference M − B5 > 0, exact
  two-sided p ≤ 0.05, and ≥ 1 stratum with ≥ 5 M-only-exact instances.
- **G2 `ANTI_CONSERVATISM`:** on `NO_REOPENING_NEEDED` and
  `NEW_INDEPENDENT_SUPPORT`, M's over-reopened commitments ≤ B5's.
- **G3 `MECHANISM`** (only if G1b): for each stratum with ≥ 5 M-only-exact
  instances, the matching omission ablation's exact rate on that stratum ≤
  B5's (DEPENDENCE → minus dependence ancestry; TRANSPORT → minus typed
  transport; EVALUATOR → minus evaluator contract; all others → minus support
  families).
- **G4 `INTERFACE_LADDER`** (H-EXT-3): (a) monotonicity — no rung k+1
  significantly worse than rung k (paired exact p ≤ 0.05 in the wrong
  direction is a violation); (b) rung-5 gap = the G1 paired test. Terminals:
  monotone ∧ gap null → `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`; monotone
  ∧ gap persists → `CONTROL_RESIDUAL_CANDIDATE_AT_FULL_STRUCTURE`; non-monotone
  → `LADDER_NON_MONOTONE` (H-EXT-3 falsifier fires). Rung k+1 information
  contains rung k's, so monotonicity is predicted by construction; a violation
  is reported as a lane defect of the compression rule, not as a finding.
- **COST:** wall-clock ratio with a 2× flag; reported, never a route by
  itself (a cost-only claim needs a separate scaling cell).

## 7. Pre-registered routing

| outcome | route |
|---|---|
| G0 fail | `CANNOT_CHECK` — lane defect; repair, re-freeze, no arm verdict |
| G1a pass | `PARENT_SUFFICIENT` (with G4a: `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`) |
| G1b pass ∧ G2 fail | `M_OVER_REOPENS` |
| G1b pass ∧ G2 pass ∧ G3 pass | `ME_X4_RESIDUAL_CANDIDATE` |
| G1b pass ∧ G2 pass ∧ G3 fail | `CANNOT_CHECK` — advantage not attributable to a named mechanism |
| neither G1a nor G1b | `PARENT_SUFFICIENT` (B5 not worse, or discordance without significance) |

Kill conditions of protocol §8 map onto: `PARENT_SUFFICIENT` (B5 reproduces
at equal or lower cost), `M_OVER_REOPENS` (M erases valid independent
support), and the design invariant that M depends on no hidden oracle relation
(arms receive only registered information; the oracle module is never
imported by an arm).

**Naturalistic validation (protocol §7)** is declared a **separate later cell**:
native reviewers define reopening sets before arm outcomes; nothing from this
exact study transfers to it.

## 8. Custody and protected-run discipline

- Code: `mex4_model.py`, `mex4_oracle.py`, `mex4_generator.py`,
  `mex4_parents.py`, `mex4_arms.py`, `mex4_run.py`; sha256 frozen in the
  receipt. Determinism: results and custody files are byte-identical on
  re-run (only RNGs: instance seeds, the random-control seed, the shuffle-null
  seed 20260902); wall-clock lives in a separate timing file.
- Stages: `selftest`, `dev` (≤ 40 instances, label DEVELOPMENT, never
  protected), `protected`, `analyze`.
- The `protected` stage **refuses** unless `PROTECTED_RUN_AUTHORIZATION.json`
  (human_written = true, a human-written token ≥ 16 chars, and
  `acknowledged_design_sha256` = sha256 of the frozen design JSON) is present
  next to the runner **and** the custody seed hashes to the commitment. The
  file is absent in this PR; the tests assert its absence and the refusal
  paths.
- Outputs: `results/ME_X4_<LABEL>_RESULTS_V1.json` (arm outputs only),
  `…_EXPECTED_CUSTODY_V1.json` (oracle sets + instances),
  `…_TIMING_V1.json`, `…_ANALYSIS_V1.{json,md}`.
- Estimated protected cost: 1 200 instances × 20 arms ≈ 1–3 CPU-minutes on a
  laptop core (development: 36 instances in < 1 s). Run on laptop billy or a
  LUNARC login node; never as a heavy job; never on the Mac mini as CI.

## 9. Non-goals, no-rescue clause, resolved ambiguities

No stratum weight, oracle rule, arm, seed or gate changes after the protected
results file exists. Development-only tuning surface: bug fixes to arm glue
validated by G0a known-answer tests before the seed is revealed. A protected
result is never re-run under a new seed; a lane defect found mid-run halts the
lane, is receipted, and re-freezes as V2. No claim from this study reaches the
naturalistic cell (§7). No field status, novelty or publication authority.

Ambiguities resolved at design time: (1) cycles are out of scope (DAG by
construction; `CANNOT_CHECK_CYCLE` unreachable); (2) contradiction edges act
through a per-claim `nocontra` condition shared by every family — "all
sufficient support failed" is then literally true when a valid contradiction
is registered; (3) prerequisite-only families carry no scope atom; (4)
"evaluator replaced" is modelled as a coverage change (a replacement with
wider coverage is a `NO_REOPENING_NEEDED` decoy); (5) the oracle's
event→atom semantics and M's compiler are two implementations of the same
frozen §2.3 table — agreement is necessary, not sufficient, for a residual;
the decisive comparison is M vs B5, which share the registered inputs and the
parent-owned ORION modules; (6) engine cost proxies are engine-native and not
commensurable across engines, so only wall-clock drives the cost flag.
