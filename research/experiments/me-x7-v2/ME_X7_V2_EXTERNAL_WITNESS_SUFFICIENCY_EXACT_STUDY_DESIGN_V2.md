# ME-X7 V2 — Claim-Sufficient External Witnesses: Exact Known-Answer Study (Registered Design V2)

**Class:** exact-oracle known-answer study — **zero model calls, fully
deterministic, CPU-seconds**. It decides what information must cross the
boundary to an *external verifier* for a machine-produced scientific claim to
stay accountable: whether a compact claim-sufficient witness suffices, against a
full human-style trace, a domain-native proof/replay certificate,
provenance-plus-output, opaque output, and the strongest faithful audit parent
federation at full registry information. **Parent sufficiency is a successful
terminal** of this design and is the pre-registered expectation (§1.2).

**Protocols served:** `ME_X7_EXTERNAL_WITNESS_SUFFICIENCY_PROTOCOL_V1.md`
§2–§10 verbatim, `MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md` §0–§2,
§9 and §11 (rule 5: no LLM judge where the claim is formally checkable; rule
10: a proof accepted by a checker is not thereby a faithful formalization).
Ontology: every episode is an **epistemic transition** — the audit changes what
is known about the claim, never the world.

**Relation to the flagship's surviving residual.** ME-X1 and ME-X4 both
terminated `PARENT_SUFFICIENT` with the residual contracted to an
*interface-information* statement: what must cross a **module boundary** inside
the system. X7 asks the dual question — what must cross the boundary to an
**external** verifier — and answers it with the same machinery (H-EXT-3 ladder,
custody scheme, McNemar-exact conventions).

**Status:** frozen design + parent baselines + development split. **No V2
protected outcome has been generated or inspected.** The protected stage refuses
to run (§8).

Companion: `ME_X7_V2_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V2.json`
(schema `orion.v2.me-x7-v2.exact-study-design.v2`) carries every constant below;
`ME_X7_V2_PARENT_FIDELITY_RECEIPT_V1.md` carries code hashes, the parents'
native known-answer results and the development-split summary.

## 0. Why there is a V2, and exactly what it changes

The V1 protected run routed `CANNOT_CHECK`: hard gate G0b
`ORACLE_SELF_AGREEMENT` failed at 1244/1250, and G5's `S2_REPLAY_SUPPORT`
conjunct failed on the same six instances. The diagnosis is
`research/experiments/me-x7/ME_X7_OUTCOME_RECEIPT.md` §2 and §7; V1 design §9
prescribes halt, receipt, re-freeze as V2. **No V1 arm verdict was issued and
none is carried forward.** The V1 protected seed is revealed in that receipt and
is burned.

The defect: the `CENSOR_ENV` variant clears the artifact's `actual_env` and
`actual_seed`, the registered "environment is not recoverable" condition. The
arm-side `m_artifact_digest` re-executes the replay machine without the
recoverability guard its siblings `m_env_identity`/`b5_env_identity` already
carry, so an unrecoverable environment was misread as a proof/code mismatch —
6 of 1250 instances, all in `CENSORED_UNDECIDABLE × MODE_COMPUTATIONAL ×
DIRECT`, symmetric across M and B5 because the implementation is shared.

V2 differs from V1 by **three registered corrections and a new protected seed
commitment, and by nothing else** — no gate, stratum weight, arm, surface
definition or threshold changes, and the development seed is deliberately
unchanged so that any difference in the development split would be attributable
to the corrections alone.

**Correction 1 — the check table gains a censored state for
`C_ARTIFACT_DIGEST`** (V1 receipt §7 incompleteness A). In `MODE_COMPUTATIONAL`,
when the environment is not recoverable, the check is `CENSORED`. The
declared-versus-actual digest comparison needs no environment and decides first,
so an unrecoverable environment never suppresses a real mismatch: unrecoverable
environment with mismatched digests is still `INVALID`; unrecoverable
environment with matching digests is `CENSORED`. `MODE_FORMAL` is untouched —
that branch runs the resolution checker over the payload and never consults the
environment or the seed. Applied in the oracle (`check_artifact_digest`) **and**
in the arm-side shared implementation (`m_artifact_digest`, used by both
`MODULE_CHECK_M` and `MODULE_CHECK_B5`).

  *Declared consequence, not an independent arm change.*
  `A0_PROOF_CERTIFICATE_ONLY` consumes `m_artifact_digest` and in V1 mapped
  `INVALID → REJECT` and everything else to `ACCEPT`. A `CENSORED` value is now
  reachable, and "everything else → `ACCEPT`" would make that parent accept an
  artifact it could not re-run. It abstains (`CANNOT_CHECK`) instead, exactly as
  `A2_REPLAY_ONLY` already does on the same condition. There was no
  leave-it-alone option: V1 returned `REJECT` there, so both `ACCEPT` and
  `CANNOT_CHECK` differ from V1, and `ACCEPT` would be the rejected repair 1
  smuggled into a parent.

**Correction 2 — the generator-validity invariant becomes a declared set** (V1
receipt §7 incompleteness B). `planter_agrees`'s "exactly one censored check"
count invariant for the `CENSORED_UNDECIDABLE` stratum is replaced by a
**declared per-variant, per-mode expected-censored set**
(`mex7_oracle.EXPECTED_CENSORED_CHECKS`), asserted by set equality. The table is
total over the drawable `(variant, mode)` pairs — `MODE_FORMAL` cannot draw
`CENSOR_CALIBRATION` — and an unregistered pair raises rather than falling back
to a permissive default; the generator asserts at import time that the two
registries agree. The declared set is a single check for every pair except
`(CENSOR_ENV, MODE_COMPUTATIONAL)`, which declares
`{C_ENV_IDENTITY, C_ARTIFACT_DIGEST}`.

**The two are one repair and neither is valid alone.** Correction 1 alone leaves
the count invariant in force, so every computational `CENSOR_ENV` episode is
re-drawn: measured under the burned V1 seed, `CENSOR_ENV` falls from **8 draws
to 2** and all six computational instances leave the split. G0b would then
report agreement because the hard cases are gone — a counter reporting zero
violations because it never ran on the relevant cases, in the repair to a study
about exactly that. Correction 2 alone is unreachable, since it is correction 1
that makes the second check censored; and the third candidate repair — deciding
`C_ARTIFACT_DIGEST` from the recorded `checker_accepts` flag when the
environment is gone — teaches the auditor to report `VALID` on the strength of a
claim it could not check, which is the failure mode this study exists to
measure.

**Correction 3 — a label, with no numeric effect** (V1 receipt §2.6). The
reported, never gated diagnostic `IMPLEMENTATION_AGREEMENT` is renamed
`ARM_VS_ARM_IMPLEMENTATION_AGREEMENT`, and its rule states that it compares M's
check table with B5's, never either against the oracle, and is therefore
structurally incapable of seeing a defect in one of the seven shared
implementations — which is the defect V1 had. G0b is the three-way comparison
that can, and G0b is what fired.

**Measured, not asserted.** Under the burned V1 seed the V2 code reproduces the
V1 protected split **byte-for-byte** (1250 instances, canonical-JSON digest
`462e6a0bbb46a301e12aefe285424276f520ca959c200184cbbc0c92917b34c9` on both),
`CENSOR_ENV` is still drawn 8 times — 6 computational, 2 formal — the six
computational instances are the same six the V1 receipt names (indices 0002,
0011, 0015, 0019, 0042, 0045), and on each of them the oracle and **both** arm
tables now return `CENSORED` for `C_ARTIFACT_DIGEST` where V1 had oracle `VALID`
against arm `INVALID`. The V2 development split's results, expected-custody and
selftest report are identical to V1's in every field except the `schema_version`
string. This is a G0-only validation: no arm verdict, ladder or G1/G4/G5/G7
number is read off the burned seed, so the V2 protected run stays blind.

## 1. Question, hypothesis, expectation

**Q.** For a scientific transition whose evaluator contract names a set of
decision-relevant failure classes, which **witness surface** lets an external
auditor reach the same accept / reject / cannot-check decision as an auditor
with the whole registry — and does the compact claim-sufficient witness do so
without raising false acceptance and without costing more than the full trace?

**H0 (strongest-parent sufficiency).** An information-matched federation of
proof/certificate checking, provenance lineage, executable replay, dependence
audit, assurance-case update and calibrated abstention, at full registry
information, makes the same audit decisions at equal or lower cost.

### 1.1 Where the information-matching rule lands

Master §2 requires that B5 receive no less information than M. **X7 inverts the
usual arrangement: the arms *are* information levels.** The registered reading,
frozen here before any protected outcome:

- `B5_STRONGEST_FAITHFUL_AUDIT_PARENT` is the **information-matched
  comparator**: all twelve witness fields, the full registry, and the native
  parent engines. G1 compares M with it and with nothing else.
- The witness surfaces below B5 are a **prospectively frozen ladder**, and that
  ladder is X7's primary axis. A surface scoring below B5 is not a violation of
  §2; it is the measurement.
- M is never given anything B5 lacks. M ⊂ B5 as information, always.

### 1.2 Pre-registered expectation

Proof/certificate and provenance surfaces should catch the classes their
artifacts cover and miss the rest; the full trace should catch what the machine
*did* (artifact identity, attempted routes) and be blind to external registry
state; the claim-sufficient witness should match B5. The expected route is
therefore `PARENT_SUFFICIENT` with witness terminal
`WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT`, i.e. a **lower bound on the
boundary surface** — an interface result, the external dual of X1/X4, not a
control residual. The decisive content is (a) whether any surface breaks the
predicted ordering, (b) the per-class surface matrix, (c) whether the five
sufficiency conjuncts of protocol §7 each hold as their own positive test, and
(d) whether the result transfers across both epistemic modes.

## 2. Frozen inputs: episode, oracle, generator

### 2.1 The episode (registered information; identical for every arm modulo the surface)

A **problem contract** (`orion_v2.contracts.ProblemContract`: problem id,
target, decision class, scope, replay requirement, requested authority level,
authority ceiling, and the **evaluator contract** — the decision-relevant
failure classes); a **claim** (context, asserted failure class, formalization
digest, result digest); three **supports**, each with declared provenance
roots, an evaluator, a context and (computational mode) a calibration; a
**provenance registry** of typed nodes with ancestry edges, statuses
(VALID/RETRACTED/SUPERSEDED/DISPUTED), a `declared` flag and a
`suspected_parent` flag; **evaluators** with coverage and uncertain failure-class
sets; **calibrations**; typed **context relations**
(`orion_v2.structural.RelationType` order); an **artifact** (a real resolution
refutation in formal mode, a real register-machine program in computational
mode) with declared/actual digests, recorded/actual environment and seed and an
execution route counter; a **route ledger**; an optional **representation
change** with correspondence evidence; and the machine's **internal step
record**.

### 2.2 The twelve witness fields (protocol §2) and their registered ORION homes

| protocol §2 item | field | registered home |
|---|---|---|
| exact input/problem/criterion identity | `PROBLEM_BINDING` | `orion_v2.contracts.ProblemContract` |
| source/evidence/provenance identities | `PROVENANCE` | `orion_v2.provenance.ReticulateProvenance` |
| executable code/proof/certificate | `ARTIFACT` | resolution checker / replay machine (`mex7_parents`) |
| assumptions and parameter versions | `ASSUMPTION_VERSION` | artifact environment + seed identity |
| measurement/experiment records | `MEASUREMENT_CALIBRATION` | calibration statuses under instruments |
| — (transport) | `TRANSPORT_RELATION` | `orion_v2.structural.RelationType` rank |
| support/reopening dependencies | `DEPENDENCE` | `orion_v2.evidence.assess_evidence_dependence` |
| evaluator identity and applicable failure class | `EVALUATOR_CONTRACT` | evaluator coverage + `ProblemContract` decision-relevant classes |
| preservation/correspondence after representation change | `PRESERVATION` | `orion_v2.correspondence` / `orion_v2.comparability` |
| unresolved limitations | `ROUTE_LEDGER` | registered attempted routes and outcomes |
| authority ceiling | `AUTHORITY_CEILING` | `orion_v2.development_controller` ceiling semantics |
| the reported result | `RESULT` | — |

Every field is a **projection of registered ORION state**; no new `Witness`
type is introduced, and the field set carries no answer key: the injected
class, the stratum and the oracle verdict live on the `Instance`, never inside
an `Episode`, and the unit tests assert that no arm payload contains a string
from the failure-class or verdict vocabulary.

### 2.3 The eleven checks and the frozen adjudication rule

Each check is a bijection onto one protocol §5 failure class, and each declares
the fields it needs. A check is **runnable** iff all its required fields are on
the surface.

| check | class | required fields | INVALID when | CENSORED when |
|---|---|---|---|---|
| `C_SPEC_BINDING` | wrong problem/specification | `PROBLEM_BINDING` | formalization ≠ intended question | intended question not recorded |
| `C_SOURCE_STATUS` | stale/wrong source | `PROVENANCE` | a reachable ancestor is RETRACTED/SUPERSEDED | a reachable ancestor is DISPUTED |
| `C_DEPENDENCE` | hidden dependence | `DEPENDENCE` | confirmed independent components < k | only suspected edges bring it below k |
| `C_ARTIFACT_DIGEST` | code/proof mismatch | `ARTIFACT` | declared ≠ actual digest, or the checker rejects | **(V2 correction 1)** in `MODE_COMPUTATIONAL` the environment is not recoverable, so the checker cannot be re-run; the digest comparison decides first and is unaffected |
| `C_ENV_IDENTITY` | seed/version mismatch | `ASSUMPTION_VERSION` | replay under the recorded identities diverges | the environment is not recoverable |
| `C_CALIBRATION` | invalid calibration | `MEASUREMENT_CALIBRATION` | a used calibration is INVALID | a used calibration is UNDER_REVIEW |
| `C_TRANSPORT` | invalid transport | `TRANSPORT_RELATION` | relation missing or below required rank | relation typed `CANNOT_CHECK` |
| `C_ROUTE_COMPLETENESS` | omitted failed route | `ROUTE_LEDGER` **and** `ARTIFACT` | declared routes < the artifact's execution count | the execution log was not retained |
| `C_EVALUATOR_COVERAGE` | evaluator blind spot | `EVALUATOR_CONTRACT` | the asserted class is outside coverage | the asserted class is in `uncertain` |
| `C_AUTHORITY` | authority overreach | `AUTHORITY_CEILING` | requested level > ceiling | ceiling not recorded |
| `C_PRESERVATION` | representation change loses information | `PRESERVATION` | a required invariant is violated or lost | a required invariant is unresolved |

**Adjudication (frozen, identical for every surface arm):** run every runnable
check; if any is INVALID the verdict is `REJECT` and the class is the first
INVALID check in the frozen order; otherwise, if the surface carries
`EVALUATOR_CONTRACT`, any decision-relevant class whose check is *not runnable*
makes the verdict `CANNOT_CHECK`; a censored runnable check does the same;
otherwise `ACCEPT`. **This is the study's central mechanism and it is
falsifiable:** the evaluator-contract field is what converts a silent false
acceptance into an honest abstention, and `M_MINUS_EVALUATOR_CONTRACT` is
predicted to convert abstentions back into false acceptances.

### 2.4 The exact oracle, and how M and B5 are kept apart

The oracle is the adjudication at full field visibility and full registry
visibility. Three things must hold on every instance (G0b), and the design is
explicit about which of them are independent *implementations* and which is a
generator-validity check:

1. **Two implementations of the verdict rule.** The direct rule and an
   **exhaustive enumeration** over all `2^c` resolutions of the censored checks
   (a verdict is definite only when every resolution agrees) — the same
   three-valued discipline as ME-X4 §2.4.
2. **Generator validity, not a third implementation.** The planter's declared
   defect is compared with a full-structure recomputation: exactly the planted
   class INVALID, nothing else INVALID, no censoring. For the
   `CENSORED_UNDECIDABLE` stratum the drawn variant is required and its censored
   set must **equal the set declared for that (variant, mode) pair** (V2
   correction 2); V1 required exactly one censored check, which is false for a
   variant whose erased field two checks depend on. This runs through the
   oracle's own code, so it validates the *generator*, not the semantics; a
   planter that fails to plant, plants twice, or turns a decoy into a defect
   cannot enter a split. Four planted positives in the selftest show it is
   trippable, and the unit suite adds a fifth for the declared set itself: an
   episode whose censored set differs from its declaration must be rejected, or
   "the declared set matched" would be unfalsifiable.
3. **Two implementations of the check table, one per side of the primary
   comparison.** `M` and `B5` must not be the same computation under two names,
   or G1, G2 and three of the five sufficiency conjuncts would be `x == x`.
   They are therefore adjudicated through two separately written tables, both
   arm-side and neither importing the oracle:

   | check | `MODULE_CHECK_M` | `MODULE_CHECK_B5` |
   |---|---|---|
   | `C_SOURCE_STATUS` | ancestor walk up from the claim's supports | `ReticulateProvenance.affected_by_revocation` reachability down from flagged nodes |
   | `C_DEPENDENCE` | overlap of ancestor sets, counted by `assess_evidence_dependence` | pairs from the descendant walk, same parent counter |
   | `C_ENV_IDENTITY` | recorded assumption/version identities compared | the replay machine actually re-run under the recorded versus the actual environment |
   | `C_PRESERVATION` | `orion_v2.correspondence.assess_correspondence_chain` | `orion_v2.comparability.ComparabilityCertificate` |
   | the other seven | shared | shared |

   **Four of eleven checks run different code; the other seven are arithmetic
   thin enough that two implementations would be the same three lines, and are
   reported as shared rather than counted as independent.** Both tables re-run
   the resolution checker and the replay machine instead of trusting a recorded
   flag — and, under V2 correction 1, report `CENSORED` rather than re-running
   in an environment that is not the one that ran. Per-check agreement between
   the two is reported in the analysis
   (`ARM_VS_ARM_IMPLEMENTATION_AGREEMENT`), so a divergence between the two arms
   is a visible lane defect rather than a silent one. **It is arm-vs-arm and
   nothing else** (V2 correction 3): it never compares either side against the
   oracle, so it is structurally incapable of seeing a defect in one of the
   seven shared implementations, which is what V1 had. **G0b** is the three-way
   comparison that can, and in V1 it fired while this diagnostic read 1250/1250
   on all eleven checks. Every arm except `B5` uses the M table, so the ladder and
   the ablations vary information, not implementation.

### 2.5 Generator, decoys and the base episode

Each instance starts from a clean base episode that the oracle certifies as
`ACCEPT` before any planting, and that already carries **nine standing
decoys**: a retracted source no support descends from (a registry-wide "any
retraction rejects" policy is punished); an undeclared node that is nobody's
ancestor; an evaluator blind to a class the claim does not assert; an evaluator
blind to the asserted class but attached to no support; an unused INVALID
calibration; a transport relation exactly at the required strength (`>` instead
of `≥` is punished); a far-below-requirement relation between unused contexts;
an over-registered route the machine never ran; and an authority request exactly
at the ceiling. Decoys are why conservatism does not pay.

Deterministic rejection sampling under
`seed = sha256(split_seed | stratum | mode | index)[:12]`, `MAX_ATTEMPTS = 400`.

### 2.6 Defect locus, and the finite separation example

Two strata are registry-graph defects and carry a registered **locus**
dimension with frozen weights `DIRECT 0.50 / TRANSITIVE_ANCESTOR 0.25 /
UNDECLARED_SHARED_UPSTREAM 0.25`: `STALE_OR_WRONG_SOURCE` and
`HIDDEN_DEPENDENCE`. Every other stratum is `DIRECT`; the locus cross-cut is
reported only where it varies, with `n_evaluated`.

The `UNDECLARED_SHARED_UPSTREAM` locus is the finite separation example:
episodes **P** and **Q** are identical on every value the producing system ever
recorded, and differ only in an ancestry edge through a node the system never
declared. Q's supports are genuinely independent (oracle `ACCEPT`); P's share
that undeclared upstream, so independence fails (oracle `REJECT`). **A
self-contained witness — the same twelve fields carried as values — returns the
identical verdict on P and Q and is therefore wrong on one.** An
identity-exporting witness, whose exported identities the auditor resolves
against the shared registry, is exact on both. The selftest asserts exactly
this.

**Registered reading of §2 (ambiguity resolved before the run):** protocol §2
says a witness may contain "source/evidence/provenance **identities**", so the
faithful `M_CLAIM_SUFFICIENT_WITNESS` is **identity-exporting with registry
resolution**, and the self-contained variant is a registered *ablation*
(`M_MINUS_REGISTRY_RESOLUTION`), not the primary M. Reading it the other way
round would manufacture an M loss out of a definition.

## 3. Strata, modes and counts

Thirteen strata × two modes, minus one non-applicable cell (`INVALID_CALIBRATION`
has no computational meaning in the formal mode, where no measurement
calibration exists) = **25 cells**. Protected: **50 per cell, 1 250 instances**.
Development: **1 per cell, 25 instances** (cap 40).

**Modes (protocol §4, two materially different modes where external checking is
strong).** `MODE_FORMAL`: propositional resolution refutations, verified by a
real checker, so `CODE_OR_PROOF_MISMATCH` is a checker rejection and
`WRONG_PROBLEM_OR_SPECIFICATION` is a valid derivation of a statement that is
not the intended question (master §11 rule 10 made into a measurement).
`MODE_COMPUTATIONAL`: deterministic register-machine programs with executable
replay, so `SEED_OR_VERSION_MISMATCH` is an actual replay divergence.

**The non-applicable cell is generated zero times and is reported as
`n_evaluated = 0`, never as a passing row.** Every violation count in the
analysis carries the number of instances actually evaluated for it, and the
selftest pairs each no-alarm assertion with a planted positive that must trip
it: a planter that fails to plant, a planter that plants twice, a "clean" case
that is not clean, and a correct plant that must be accepted.

**Seed commitment.** Protected seed sha256
`08631e5fa419e350a2c4d71bcee487fdebb166875ed8647a79f76f2519f02cfd`
(operator custody `~/.orion-custody/me-x7-v2/PROTECTED_SEED_V1.txt`, mode 600;
the runner verifies the hash before any protected generation; the seed string is
revealed in the V2 outcome receipt so the split regenerates byte-for-byte).
Development seed (public): `ME-X7-DEV-20260902` — **deliberately unchanged from
V1**, so any difference in the development split is attributable to the
registered corrections and to nothing else.

**The V1 protected seed is burned.**
`ME-X7-PROTECTED-b35d0617f13ec73ed96368bfb7019f603e5818bfa69d6de1` was revealed
in the V1 outcome receipt §1 and can never again be a protected seed. It is used
in the V2 unit suite as a **public validation seed only**, and only for
G0-relevant quantities: the variant draws and the oracle-versus-arm check
statuses on the cell that failed. No arm verdict or gate number is read off
it.

**Power / MDE.** Primary statistic = paired instance-level exact audit-verdict
match (verdict, plus defect class when `REJECT`), M vs B5, McNemar exact
two-sided on discordant pairs, with a paired Wald interval. Pooled n = 1 250: 6
one-directional discordants (0.48%) reach p = 0.031, 8 reach p = 0.008; per cell
n = 50: 6 discordants reach p = 0.031. The prior expectation is zero
discordance; the test is two-sided so a federation advantage is equally
detectable, and G1c gives it its own positive test.

## 4. Arms

**Witness surfaces (protocol §3).**

| arm | exported fields | note |
|---|---|---|
| `S0_OPAQUE_OUTPUT_ONLY` | `RESULT` | protocol §3 opaque output |
| `S1_PROVENANCE_PLUS_OUTPUT` | + `PROVENANCE` | protocol §3 provenance + output |
| `S2_FULL_HUMAN_STYLE_TRACE` | `RESULT`, `ARTIFACT`, `ROUTE_LEDGER` (+ the step record in the export accounting) | a complete step-by-step record of what the machine executed and attempted — and *nothing about external registry state*, because registry facts are not machine steps (protocol §9) |
| `S3_PROOF_OR_CERTIFICATE_PARENT` | `RESULT`, `ARTIFACT`, `ASSUMPTION_VERSION` | a domain-native proof or replay bundle: statement, derivation/program, pinned versions |
| `M_CLAIM_SUFFICIENT_WITNESS` | all twelve, identity-exporting | the structured minimal witness, selected prospectively from registered ORION semantics |
| `B5_STRONGEST_FAITHFUL_AUDIT_PARENT` | all twelve, full registry, **adjudicated through the parents' own engines** (`MODULE_CHECK_B5`, §2.4) | **primary comparator** |

The trace arm is the one place where the design takes a substantive modelling
decision and states it: a narrative trace is a faithful record of the machine's
own steps, and is therefore *unverifiable against external registries*. It sees
proof mismatch and route omission; it cannot see a retraction, a calibration, an
evaluator's coverage, a typed context relation, an authority ceiling or the
intended question. Its accuracy is bounded by what it carries, not by its
length.

**Nested ladder (H-EXT-3), six rungs, fields only (registry resolution held
constant):** `L1_OUTPUT_ONLY` ⊂ `L2_PLUS_PROVENANCE` ⊂
`L3_PLUS_PROBLEM_ARTIFACT` ⊂ `L4_PLUS_VERSION_CALIBRATION_TRANSPORT` ⊂
`L5_PLUS_DEPENDENCE_ROUTE_AUTHORITY_PRESERVATION` ⊂ `L6_FULL_WITNESS` (= M).
Rung k+1's fields contain rung k's, so monotonicity is predicted by
construction; a violation is a lane defect of the surface definitions, not a
finding.

**Single faithful parents (each passes its own native known-answer tests before
use; `mex7_parents.fidelity_selftests`, 23 tests, receipt §2).**

| arm | native semantics | predicted break |
|---|---|---|
| `A0_PROOF_CERTIFICATE_ONLY` | resolution refutation checking (Robinson 1965; presentation after Bachmair & Ganzinger, *Handbook of Automated Reasoning* ch. 2); abstains where the artifact cannot be re-run because the environment is not recoverable (V2 correction 1's declared consequence) | blind to the intended question; blind to every registry class |
| `A1_PROVENANCE_ONLY` | `orion_v2.provenance` revocation descendants, two-valued | treats DISPUTED as revoked → over-rejects on censored episodes |
| `A2_REPLAY_ONLY` | deterministic re-execution under recorded environment and seed | catches version drift only |
| `A3_ASSURANCE_CASE` | GSN change impact (Kelly & Weaver 2004), conjunctive, two-valued | no censoring channel; misattributes calibration failures to provenance |
| `A4_DEPENDENCE_AUDIT` | `orion_v2.evidence.assess_evidence_dependence`, conservative | counts suspected ancestry against independence → over-rejects censored dependence |
| `A5_CALIBRATED_ABSTENTION` | selective prediction at a fixed coverage threshold (Geifman & El-Yaniv 2017) | no failure-class semantics at all: the B1 rung |

**Ablations (protocol §8), all eleven single-field omissions plus registry
resolution:** `M_MINUS_{PROVENANCE, PROBLEM_BINDING, DEPENDENCE, ARTIFACT,
ASSUMPTION_VERSION, CALIBRATION, TRANSPORT, ROUTE_LEDGER, EVALUATOR_CONTRACT,
AUTHORITY_CEILING, PRESERVATION, REGISTRY_RESOLUTION}`. This strictly covers
protocol §8's seven groups.

**Controls:** `C_ALWAYS_ACCEPT`, `C_ALWAYS_CANNOT_CHECK` (the degenerate
abstainer, which has zero false acceptance and zero coverage — it is why
coverage is scored), `C_RANDOM_VERDICT`, and M scored against shuffled oracle
labels.

## 5. Outcomes (protocol §6)

Per arm: exact audit-verdict match; false acceptance (arm `ACCEPT` where the
oracle rejects); false rejection; misclassified rejection (right verdict, wrong
class); abstention on decidable episodes; missed censoring; **detection recall
by failure class with `n_evaluated`**; replay support; exported records and
checks run (the structural audit-cost measures); wall-clock (reported, never
decisive); per-cell and per-locus exact rates. All arms × all cells are reported
in full.

## 6. Gates (frozen before any protected outcome exists)

- **G0a `KNOWN_ANSWER` (hard):** one hand-authored fixture per applicable cell,
  the P/Q separation pair, and the four planted positives are reproduced in the
  selftest report.
- **G0b `ORACLE_SELF_AGREEMENT` (hard):** direct rule = exhaustive enumeration;
  **both** arm check tables (M's and B5's, §2.4) = the oracle's check table at
  full visibility; and, as a generator-validity check rather than a third
  implementation, the planter's declared defect = the full-structure
  recomputation. Each counted with `n_evaluated`.
- **G0c `NULL_CALIBRATION` (hard):** `C_ALWAYS_ACCEPT` exact = 0 where the
  oracle rejects; `C_ALWAYS_CANNOT_CHECK` exact = 0 where the episode is
  decidable; `C_RANDOM_VERDICT` ≤ 0.15; M against shuffled labels ≤ 0.15.
- **G1a `B5_REPRODUCES_M`:** identical exact-match indicator on ≥ 99.5% of
  instances and no cell above 5% discordant.
- **G1b `M_ADVANTAGE`:** paired difference M − B5 > 0, exact two-sided p ≤ 0.05,
  ≥ 1 cell with ≥ 5 M-only-exact instances.
- **G1c `B5_AHEAD`:** **its own positive test** — paired difference M − B5 < 0
  with exact two-sided p ≤ 0.05. (ME-X2's interface terminal was computed as the
  negation of its gap gate and therefore fired on a tie *and* on a federation
  win; that is not repeated. Every terminal here has a positive test.)
- **G2 `ANTI_CONSERVATISM`:** on `NO_DEFECT_WARRANTED`, M's non-`ACCEPT`
  verdicts ≤ B5's.
- **G3 `MECHANISM_BY_OMISSION`:** for every injection class, the set of field
  omissions that lowers its detection recall **equals exactly** the set of
  fields its check requires — so `C_ROUTE_COMPLETENESS`, which needs two fields,
  is predicted to be broken by two ablations and no others. Reported per class
  with `n_evaluated`.
- **G4 `INTERFACE_LADDER` (H-EXT-3):** no rung k+1 significantly worse than rung
  k (paired exact p ≤ 0.05 in the wrong direction is a violation).
- **G5 `SUFFICIENCY`:** protocol §7's five conjuncts, each **its own positive
  test with its own `n_evaluated`**:
  - `S1_FAILURE_CLASS_PRESERVATION` — per class *and mode*, M's detection recall
    ≥ B5's − δ;
  - `S2_REPLAY_SUPPORT` — on every replay-required episode the witness's own
    artifact-identity and environment-identity checks **reproduce the
    full-structure statuses**. This is deliberately instance-by-instance: a
    conjunct that only restated the arm's field set would be constant across
    the split and would report a non-zero `n_evaluated` for a quantity that
    never varied;
  - `S3_SELECTIVE_REOPENING_WITHOUT_HIDDEN_HISTORY` — on support-defeat episodes
    the witness names the same defect class as the full-structure audit;
  - `S4_FALSE_ACCEPTANCE_NONINFERIORITY` — FA(M) − FA(B5) ≤ **δ = 0.01
    absolute**, reported with the discordant counts and the one-sided exact
    tail. This is a non-inferiority test with a prespecified margin, *not* a
    failure to reject;
  - `S5_PREFERABLE_TO_FULL_TRACE` — protocol §7(5) in its positive form: M is
    **strictly more accurate** than the full-trace arm under a paired exact
    test. That is the whole pass condition. Exported record counts are printed
    beside it and are **not** part of the test, because export size turns on the
    generator's trace-length range and nothing else (§9(7)).
- **G6 `CROSS_MODE_TRANSFER`:** the ladder is monotone and M is non-inferior to
  B5 **separately in each mode** (protocol §10 kills a result that fails to
  transfer to a second epistemic mode).
- **G7 `WITNESS_SELF_CONTAINMENT`:** a positive test with its own denominator.
  On `UNDECLARED_SHARED_UPSTREAM` episodes the identity-exporting witness must
  be strictly more exact than the self-contained one
  (`M_MINUS_REGISTRY_RESOLUTION`), **and** the two must be identical on every
  other episode — so the separation is the mechanism (an arm is exact or wrong
  on every such instance) and not a prevalence artifact. Zero such episodes
  reports `CANNOT_CHECK`, never a pass, and qualifies the witness terminal
  accordingly. With G1 expected to tie, this is where the study's separating
  content lives.
- **`ARM_VS_ARM_IMPLEMENTATION_AGREEMENT` (reported, not a gate):** per-check
  concordance between M's table and B5's. It compares arm against arm and never
  either against the oracle, so it cannot see a defect in a shared
  implementation; G0b is the gate that can (§2.4, V2 correction 3).
- **COVERAGE_LEDGER (reported, not a gate):** every registered mechanism —
  each (stratum, mode) cell, each defect locus, each of the ten censoring
  variants — with the number of instances that exercised it, and an explicit
  list of those exercised zero times.
- **COST:** wall-clock ratio with a 2× flag, plus exported records and checks
  run; reported, never a route by itself.

## 7. Pre-registered routing

| outcome | route | witness terminal |
|---|---|---|
| a hard G0 gate fails | `CANNOT_CHECK` — lane defect | `NONE` |
| G1c passes | `PARENT_SUFFICIENT` | `WITNESS_INSUFFICIENT_PARENT_AHEAD` |
| G1b ∧ ¬G2 | `M_OVER_ABSTAINS` | `NONE` |
| G1b ∧ G3 | `ME_X7_RESIDUAL_CANDIDATE` | `WITNESS_ABOVE_PARENT` |
| G1b ∧ ¬G3 | `CANNOT_CHECK` | `NONE` |
| ¬G6 | `PARENT_SUFFICIENT` | `NO_CROSS_MODE_TRANSFER` |
| G5 all pass ∧ G7 pass | `PARENT_SUFFICIENT` | `WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT__REQUIRES_IDENTITY_EXPORT` |
| G5 all pass ∧ G7 unevaluated | `PARENT_SUFFICIENT` | `…__SELF_CONTAINMENT_CANNOT_CHECK` |
| G5 all pass ∧ G7 fails | `PARENT_SUFFICIENT` | `…__SELF_CONTAINMENT_NOT_SEPARATED` |
| G5 partial | `PARENT_SUFFICIENT` | `WITNESS_NOT_CLAIM_SUFFICIENT:<failed conjuncts>` |

Protocol §10's kill conditions map onto: `WITNESS_INSUFFICIENT_PARENT_AHEAD`
(B5's artifacts already provide the frontier), `WITNESS_NOT_CLAIM_SUFFICIENT`
(compact witnesses miss decision-critical failures, or the audit cost erases the
gain), `NO_CROSS_MODE_TRANSFER` (results do not transfer to the second mode),
and the design invariant that no witness field's semantics depend on
undocumented internal state — every field is a projection of registered ORION
state and no arm imports the oracle.

## 8. Custody and protected-run discipline

- Code: `mex7_model.py`, `mex7_oracle.py`, `mex7_generator.py`,
  `mex7_parents.py`, `mex7_arms.py`, `mex7_run.py`; sha256 frozen in the
  receipt. `mex7_model.py` and `mex7_parents.py` are **byte-identical to V1**;
  the other four carry the registered corrections and the V2 path/label
  rebindings and nothing else. Determinism, stated to exactly what was checked: the **results** and
  **expected-custody** files are byte-identical on re-run (the only RNGs are
  instance seeds, the random-control seed and the shuffle null's seed
  20260902), and the raw wall-clock lives in a separate timing file. The
  **analysis** file is byte-identical *apart from* the wall-clock fields it
  quotes (`wall_ms` per arm and the `COST` block's `M_wall_ms`, `B5_wall_ms`,
  `wall_ratio_b5_over_m`); with those stripped it hashes identically, and the
  derived `COST` flag was stable across re-runs. Claiming the analysis is
  byte-identical outright would have been a claim wider than the check.
- Stages: `selftest`, `dev` (≤ 40 instances, label DEVELOPMENT, never
  protected), `protected`, `analyze`.
- The `protected` stage **refuses** unless `PROTECTED_RUN_AUTHORIZATION.json`
  (`human_written = true`, a human-written token ≥ 16 chars, and
  `acknowledged_design_sha256` = sha256 of the frozen design JSON) is present
  next to the runner **and** the custody seed hashes to the commitment. The file
  is absent in this PR; the tests assert its absence and both refusal paths —
  **exit 3** for a missing, malformed or wrongly-acknowledged authorization and
  **exit 4** for a missing or non-matching custody seed, each distinct from the
  exit 1 a broken run gives.
- Outputs: `results/ME_X7_<LABEL>_RESULTS_V1.json` (arm outputs only),
  `…_EXPECTED_CUSTODY_V1.json` (oracle verdicts + instances),
  `…_TIMING_V1.json`, `…_ANALYSIS_V1.{json,md}`.
- Estimated protected cost: 1 250 instances × 33 arms ≈ 10 CPU-seconds on a
  laptop core (development: 25 instances in < 0.2 s). Never run as a CI job on
  the Mac mini.

## 9. Non-goals, no-rescue clause, resolved ambiguities

No stratum weight, oracle rule, arm, surface definition, seed or gate changes
after the protected results file exists. Development-only tuning surface: bug
fixes to arm glue validated by the G0a known-answer tests before the seed is
revealed. A protected result is never re-run under a new seed; a lane defect
found mid-run halts the lane, is receipted, and re-freezes as the next version.
No field status, novelty or publication authority.

**V2's own no-rescue statement.** V2 differs from V1 by exactly the three
registered corrections of §0 — two semantic, one label-only — and a new
protected seed commitment. The V1 outcome is known and public, so any divergence
beyond those would read as tuning; the freeze PR body carries the full
V1-versus-V2 code diff and the measured equivalences of §0 for that reason. A V2
protected result that failed a hard gate would halt, receipt and re-freeze as
V3 under the same rule; it would not be re-run under a new seed.

Ambiguities resolved at design time:

1. **What a witness carries.** Protocol §2 lists provenance *identities*, so the
   faithful M is identity-exporting with registry resolution; the self-contained
   value-carrying variant is the `M_MINUS_REGISTRY_RESOLUTION` ablation (§2.6).
2. **What a full human-style trace is.** A faithful record of the machine's own
   steps: what it executed and what it attempted. External registry state is not
   a machine step, so the trace is blind to it. This is a modelling decision,
   stated here, and it is what makes the trace non-dominant rather than
   omniscient (protocol §9).
3. **Detecting an omission needs an independent count.** A ledger cannot report
   what it omitted, so `C_ROUTE_COMPLETENESS` requires the route ledger *and*
   the artifact's execution counter. G3's prediction is adjusted accordingly:
   two ablations, not one, are predicted to blind that class.
4. **B5 is expected to be exact, and the tie is therefore weak evidence.** The
   adjudication is exact given full fields and full registry, so a federation
   with both should score 1.000, and M — which has the same fields and the same
   visibility — should too. The M-vs-B5 comparison is a **cross-implementation**
   test (§2.4), not an information test: it can detect a bug in either side's
   four distinct checks, and it cannot detect a residual that does not exist.
   Stated in advance, not discovered. The decisive axes are the ladder (G4), the
   omission matrix (G3), the sufficiency conjuncts (G5), cross-mode transfer
   (G6) and self-containment (G7). The honest terminal of a tie is *"no witness
   residual is detectable against a federation that already has everything, and
   the two implementations agree"*, not *"witnesses add nothing"* and certainly
   not *"the witness beat the parents"*.
5. **Independence requirement.** `k = 3` over three supports, so any single
   shared ancestor defeats independence and the check has a live `n_evaluated`
   on every instance.
7. **Export size is a generator parameter, so it does not gate anything.** The
   full-trace arm's record count is the number of steps the generator emits
   (20–59). S5 therefore turns only on accuracy dominance, which is bounded by
   what the trace *carries*; the record counts are printed for the reader.
10. **The order of the two grounds inside `C_ARTIFACT_DIGEST`.** The check has
   two grounds for `INVALID` — the digests differ, or the checker rejects. Only
   the second needs the environment, so under V2 correction 1 the first decides
   first. This is observable semantics, stated in advance: an unrecoverable
   environment **with mismatched digests is still `INVALID`**, and only the
   matching-digest case is censored. An unrecoverable environment does not
   launder a mismatch the auditor could see without it.
11. **What the burned V1 seed may be used for.** It is a public validation seed
   for G0-relevant quantities only — variant draws, oracle censored sets, and
   oracle-versus-arm check statuses. Reading an arm verdict, a ladder rung or a
   G1/G4/G5/G7 number off it would pre-empt the protected run on a split whose
   answer is already public, so the V2 unit suite reads none of them.
8. **A planted version mismatch must actually diverge on replay.**
   `C_ENV_IDENTITY` has two faithful operationalizations (identity comparison on
   the M side, re-execution on the B5 side). An instance where following the
   record happens to reproduce the output is a degenerate member of the class
   and would split them for an artifactual reason — appearing as an M advantage
   over the federation. The generator rejects such candidates, so the split
   cannot contain one.
9. **A mechanism drawn zero times is named.** The coverage ledger lists every
   registered mechanism with its instance count and every one at zero. On the
   development split (one instance per cell) eight of the ten censoring variants
   and three of the six locus combinations are drawn zero times, and the ledger
   says so.
6. **Locus prevalence is a generator parameter.** Where the undeclared-upstream
   locus separates arms, the finding is the *mechanism* (an arm is either exact
   or wrong on every such instance), not the rate; the cross-cut is reported
   with its own `n_evaluated` and never drives a gate on its own.
