# ME-X5 — Cross-Domain Field Residual: Exact Known-Answer Study across Three Native Epistemic Modes (Registered Design V1)

**Class:** exact-oracle known-answer study — **zero model calls, fully deterministic,
CPU-seconds**. It decides whether ORION-V2's cross-transition epistemic control
makes registered scientific-transition decisions that the strongest faithful
parent federation cannot reproduce from the same registered information, **in
more than one materially different native epistemic mode**. **Parent sufficiency
is a successful terminal** of this design and is the pre-registered expectation
(§1.2).

**Protocols served:** `ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_PROTOCOL_V1.md` §1–§12
verbatim, `MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md` §0–§2.
**Secondary axis (H-EXT-3):** the B5 interface-information ladder of
`research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md`, carried
here with its own gate (G4, §6.5) **reported per mode and never pooled**.

**Status:** frozen design + code + development split. **No protected outcome has
been generated or inspected.** The protected stage refuses to run (§8).

Companion: `ME_X5_CROSS_DOMAIN_FIELD_RESIDUAL_EXACT_STUDY_DESIGN_V1.json`
(schema `orion.v2.me-x5.cross-domain-study-design.v1`) carries every constant
below; `ME_X5_PARENT_FIDELITY_RECEIPT_V1.md` carries code hashes, parent fidelity
results, the native-review records and the development-split summary.

## 0. What this study can and cannot decide

It can support or kill the **scientific residual** an emerging-field claim would
need. It cannot grant field status: protocol §11 `R3_ESTABLISHED_FIELD` is not
grantable by any experiment, and `R2_EMERGING_INTERDISCIPLINARY_RESIDUAL`
requires *independent adjudication* which this study does not have (§8.3, §10).
The strongest terminal reachable here is `ME_X5_FIELD_RESIDUAL_CANDIDATE`,
pending independent adjudication.

Three sibling studies have already terminated `PARENT_SUFFICIENT`
(ME-X1 `0fde96f`/`59b1f5b`, ME-X2 `704d379`/`776d3a1` in its stronger
`B5_DOMINATES` form, ME-X4 `4929a44`). X5 is not an attempt to rescue the claim
against them; it tests whether the contraction they force is the *right* one
across modes.

## 1. Question, hypothesis, expectation

**Q.** Does one stable scientific-transition object — decide the transition
action, name the responsible registered element, and bound the authority the
evidence licenses — survive native reconstruction in three materially different
epistemic modes, and does ORION-V2's cross-transition control decide it beyond
`B5`, the strongest faithful parent federation receiving the same registered
information, in more than one of those modes?

**H0 (strongest-parent sufficiency).** An information-matched federation of
provenance revocation, truth maintenance over support families, dependence
assessment, typed transport, evaluator-coverage contracts, scope bookkeeping,
assurance/global-witness checking and native numeric aggregation, composed by
ordinary engineering glue, makes the same decisions at equal or lower cost — in
every mode.

**1.2 Pre-registered expectation.** `PARENT_SUFFICIENT`. On a registered,
exactly adjudicable decision problem an information-complete federation is
optimal by construction (§10), so the expected route is no gap at full
structure, with the decisive content lying in (a) where each *single* parent
breaks, per mode; (b) which ME components are load-bearing, per mode, and whether
any one mechanism is load-bearing in ≥ 2 modes (protocol §7(1)); (c) the
interface ladder **per mode**; (d) whether the common object is recoverable when
ORION vocabulary is hidden (protocol §8); (e) cost.

**1.3 What would change the expectation.** A composition error in B5 that M does
not make; a mode whose native rules defeat the federation's glue; a rung at which
the federation cannot recover what M recovers even at full structure.

## 2. The three native epistemic modes (protocol §2, §3)

Each mode is implemented in its own module with its own vocabulary, its own
native rules and its own native-review record (protocol §3). The rules disagree:
the *same* planted structure means different things in different modes.

| | `FORMAL` (mathematics / theorem proving / formal verification) | `MEASUREMENT` (experimental-computational physical science) | `SYNTHESIS` (evidence synthesis and recommendation revision) |
|---|---|---|---|
| registered target | a theorem statement | an observable at a phase space, with a decision threshold | a PICO question, with a decision threshold on the pooled effect |
| supports | proof terms, lemmas, ported lemmas, case proofs | measurement channels, transported efficiencies, partial-acceptance channels | primary studies, transported studies, subgroup reports |
| validating apparatus | kernel at a pinned version + linters | calibration valid over an operating range + closure/null test | risk-of-bias appraisal + outcome ascertainment |
| **identity rule** | **exact**: a different universe level or binder shape is a different theorem | **fiducial restriction allowed**: the same observable in a strictly smaller phase space is a *narrowed* commitment | **over I/C/O only**: a different population is a transport question, not a different question |
| **dependence rule** | **strict defeat**: any shared confirmed lemma or axiom merges two proofs | **error-budget**: shared systematic source *or* shared ancestor correlates channels; systematics add linearly within a source group and in quadrature across groups | **deduplication**: overlapping cohorts are collapsed to the largest report, changing the pooled estimate and its precision |
| **scope rule** | a **single** artefact must carry the registered scope | the **union** of the channels' acceptance | the **union** of the studies' population coverage |
| **transport rule** | a *ported lemma* needs `ISOMORPHIC`, not the family's declared minimum | the declared regime relation rank | the declared population relation rank |
| global obstruction | a missing case-analysis / gluing lemma | a missing covariance-aware global consistency test | a missing network-transitivity check |
| numeric layer | **none** (Boolean mode) | inverse-variance combination with a correlation model, `estimate − 2σ > threshold` | inverse-variance pooling after deduplication, `pooled − 2σ > threshold` |

Native-review records (protocol §3: native objects and vocabulary, strongest
native methods, valid/invalid transitions, native failure classes, evaluator
assumptions, which ME abstractions are lossy/redundant/invalid, and the strongest
plausible parent composition) are frozen in `mex5_native_*.NATIVE_REVIEW` and
checked for completeness by G0a. **The reviewer is the study author**: no
independent domain reviewer was available (§10).

## 3. Frozen inputs: episode container, generator and exact oracle

### 3.1 Registered information (identical for every arm)

An **episode** registers a target (identity signature, scope, asserted failure
class, requested authority, context, threshold), support units (native kind,
signature, context, coverage, ancestry with CONFIRMED/SUSPECTED, validator,
status, estimate/statistical error/systematic error/systematic source/weight),
support families (unit ids, minimum independent supports `k`, required transport
relation, whether a global witness is required), validators (coverage sets,
uncertain classes, status, operating range), typed context relations, the
operating point, the global-witness registry, the authority grant, and an
optional registered narrowed scope. Twelve typed events update it. Every arm
receives the whole episode and the whole event history. Hidden from every arm:
the oracle module and the expected decisions (custody file). No arm imports the
oracle (asserted by a unit test).

### 3.2 The decision (protocol §6)

For the registered target, at the final registered version, decide a triple:

- **action** ∈ `COMMIT` · `COMMIT_NARROWED` · `WITHHOLD` · `UNRESOLVED`;
- **responsibility locus** ∈ `NONE` · `TARGET_IDENTITY` · `APPARATUS_VALIDITY` ·
  `EVALUATOR_COVERAGE` · `DEPENDENCE` · `TRANSPORT` · `SUPPORT_DEFEAT` · `SCOPE` ·
  `GLOBAL_OBSTRUCTION`;
- **authority** ∈ `BELIEF_ONLY` · `BELIEF_AND_ACTION`.

Arms decide **once, on the final registered state**, with the full event history
available. The oracle is computed at every version; the primary comparison uses
the final version.

### 3.3 The exact oracle

Family = conjunction of its registered members (a proof path uses all its lemmas;
a combination uses all its channels; a pooled body includes all its studies).
A family fails on a locus when the mode's native rule fails for it. The target
commits when some family survives *and* the mode's numeric gate clears; it
commits narrowed when the only survivors are fiducial-identity families or
families that fail on scope alone while covering a registered narrowed scope;
otherwise it is withheld.

**Frozen responsibility rule** (chosen to be invariant under relabelling): among
the families closest to repair (fewest failing loci), take each family's
highest-priority failing locus in the frozen order
`TARGET_IDENTITY > APPARATUS_VALIDITY > EVALUATOR_COVERAGE > DEPENDENCE >
TRANSPORT > SUPPORT_DEFEAT > SCOPE > GLOBAL_OBSTRUCTION`, and report the most
downstream of those — the nearest repair that would restore support.

**Authority rule:** a committed transition carries `BELIEF_AND_ACTION` only when
`ACTION` was requested *and* the registered authority grant stands; otherwise
`BELIEF_ONLY`. Belief and operational authority are separately registered.

**`UNRESOLVED` is defined by exhaustive enumeration**, not by a three-valued
envelope: in the two numeric modes a censored study or channel can move a pooled
estimate in either direction, so the decision is **not monotone** in the censored
facts and an optimistic/pessimistic bracket is unsound. The oracle enumerates all
2^u readings of the u censored facts (u ≤ 6 by generator cap) and returns
`UNRESOLVED` exactly when the readings disagree.

### 3.4 Oracle self-check (G0b)

Three independent checks on every generated instance: (i) **validity at v0** — the
episode is a warranted commitment before its registered events; (ii) **stratum
invariant** — the hand-declared expected decision of §3.6 is reproduced;
(iii) **relabelling invariance** — the decision is unchanged when every unit,
family and validator identifier is renamed and the container's insertion order
reversed. Instances failing any check are rejected by the generator.

### 3.5 Generator

Deterministic per instance under `sha256(split_seed | mode | stratum | index)`
with rejection sampling (≤ 400 attempts). Planting is shared across modes;
*semantics* are not — the same plant is read by three native rule sets and, where
those rules differ, produces different episodes and different variants.

### 3.6 Episode families (strata) and hand-declared invariants

**Protected: 40 per (mode × stratum) = 1 440.** Development: 1 per cell = 36.

| stratum | planted structure | declared final decision (the known answer) |
|---|---|---|
| `TARGET_IDENTITY_DRIFT` | a shared artefact turns out to establish a different target | `WITHHOLD` / `TARGET_IDENTITY` |
| `APPARATUS_INVALID` | apparatus withdrawn, or (measurement) the operating point leaves the calibrated range | `WITHHOLD` / `APPARATUS_VALIDITY` |
| `BLIND_EVALUATOR` | the check cannot expose the asserted failure class | `WITHHOLD` / `EVALUATOR_COVERAGE` |
| `HIDDEN_DEPENDENCE` | a confirmed shared ancestor inside every redundant family | `WITHHOLD` / `DEPENDENCE` |
| `INVALID_TRANSPORT` | the reuse licence is retyped below the requirement | `WITHHOLD` / `TRANSPORT` |
| `DEFEATED_SUPPORT` | every sufficient support withdrawn; **or** (numeric modes) a new unit drags the aggregate below threshold with nothing structural broken | `WITHHOLD` / `SUPPORT_DEFEAT` |
| `SCOPE_OVERREACH` | registered scope widened past coverage; a narrowed scope is registered in ~60% (and, in the measurement mode, the native fiducial route) | `COMMIT_NARROWED` / `SCOPE` when narrowing is registered, else `WITHHOLD` / `SCOPE` |
| `LOCAL_COMPATIBILITY_GLOBAL_OBSTRUCTION` | pieces agree pairwise, the global witness is withdrawn | `WITHHOLD` / `GLOBAL_OBSTRUCTION` |
| `AUTHORITY_MISMATCH` | the operational mandate is withdrawn, belief intact | `COMMIT` / `NONE` / `BELIEF_ONLY` (and `BELIEF_AND_ACTION` at v0) |
| `CENSORED_UNRESOLVED` | five censoring variants (unit, validator, coverage, suspected ancestry, unchecked relation) that flip the decision | `UNRESOLVED` |
| `FULLY_WARRANTED_CONTROL` | 1–2 registered events touching used entities that change nothing decisive (five variants) | `COMMIT` / `NONE` |
| `SINGLE_PARENT_SUFFICIENT` | one family, one retraction: provenance alone decides (protocol §9 negative control) | `WITHHOLD` / `SUPPORT_DEFEAT` |

The last four are protocol §9's negative controls: one mature parent fully
sufficient; the correct terminal unresolved; nothing to reopen; local
compatibility not implying globality (which is a *positive* family here and whose
decoys sit in `FULLY_WARRANTED_CONTROL`).

**Seed commitment.** Protected seed sha256
`132c47826e40f57dfd873848a82d160e2f0de114827b1155c015dce60b19467a`
(operator custody `~/.orion-custody/me-x5/PROTECTED_SEED_V1.txt`, mode 600; the
runner verifies the hash before any protected generation; the seed string is
revealed in the outcome receipt so the split regenerates byte-for-byte).
Development seed (public): `ME-X5-DEV-20260902`.

**Power / MDE.** Primary statistic = paired instance-level decision-triple exact
match, M vs B5, exact two-sided McNemar on the discordant pairs, **computed per
mode** and Holm-corrected across the three modes. Per mode n = 480: 7
one-directional discordants (1.5%) give p = 0.0156, which survives Holm at the
most-corrected slot (α/3 = 0.0167); 8 give p = 0.0078. The MDE is therefore
≈ 1.5 percentage points one-directional per mode. The prior expectation is zero
discordance; the test is two-sided, so a federation advantage (`G1c`) is equally
detectable — ME-X2's terminal was exactly that.

## 4. Arms

Three independent decision paths, not three configurations of one.

**Single faithful parents** (each passes its own native known-answer test before
use; `mex5_parents.fidelity_selftests`, 20 tests, receipt §2):

| arm | native semantics | what it cannot see |
|---|---|---|
| `B0_DIRECT_NATIVE_PIPELINE` | the native pipeline, no explicit control layer | everything except artefact presence |
| `B1_CALIBRATED_ABSTENTION` | B0 + selective prediction on any censored fact | as B0; abstains indiscriminately |
| `B2_PROVENANCE_VERIFIER_RUNTIME` | provenance revocation (`orion_v2.provenance`) + apparatus validity | dependence, transport, evaluator coverage, identity, scope, global witness, numerics |
| `B3_DIAGNOSIS_METAREASONING` | model-based diagnosis over identity, apparatus, evaluator coverage, scope | dependence, typed transport, global witness, error budget |
| `B4_TMS_ASSURANCE_FEDERATION` | truth maintenance (`orion_v2.reopening.selective_reopen`) + dependence + assurance global witness, two-valued | identity, typed transport, numerics, the unresolved terminal |

**B5 ladder (H-EXT-3).** The same parent modules composed by ordinary engineering
glue. B5 is never artificially isolated; it reuses the parent-owned ORION
reference implementations. Rungs differ only in **what crosses the module
boundary**:

| rung | witness-level export | everything else |
|---|---|---|
| `B5_R1_VERDICT_ONLY` | none | a **family-anonymous** per-target verdict per module (`DEFEATS_ALL` / `DEFEATS_SOME` / `CENSORS_SOME` / `CLEAR`) |
| `B5_R2_PROVENANCE` | + per-unit validity witnesses | verdict |
| `B5_R3_PLUS_DEPENDENCE_ANCESTRY` | + independence witnesses / ancestry partition | verdict |
| `B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR` | + typed transport relations, evaluator coverage, apparatus status | verdict |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` (rung 5) | full structure = everything M sees, including identity signatures, scope sets, the global-witness registry and the numeric correlation structure | — |

**Frozen composition policy at rungs 1–4** (registered before any protected run):
the target is withheld when a witness-level module defeats every family, when any
anonymous module reports `DEFEATS_ALL`, or when the number of anonymous defeating
modules is at least the number of families the witness-level modules left
standing; censoring is handled by the optimistic/pessimistic bracket of the
composition. **Rung 5 is the primary comparator**; rungs 1–4 are ablations of B5,
not of M.

**§2.6 finite separation example (H-EXT-3).** Two FORMAL episodes P and Q share
the identical event sequence (*a shared lemma is discovered behind two proofs; the
structure morphism is retyped below isomorphism*), the identical per-module
family-anonymous verdict tuple (dependence `DEFEATS_SOME`, transport
`DEFEATS_SOME`, all else `CLEAR`) and the identical family count. In P the two
defeats cover both families → `WITHHOLD`; in Q both land on one family with
`k = 3` while a native family stands → `COMMIT`. Any federation whose channel
carries only family-anonymous verdicts emits the *same* decision on P and Q and
therefore errs on one. Witness-level exchange is exact on both. The selftest
asserts exactly this.

**`M_ME_CROSS_TRANSITION_CONTROL`** — the ME arm, compiled to the ORION reference
objects (`ReticulateProvenance` for revocation descendants,
`assess_evidence_dependence` for independence witnesses, `RelationType` ranks for
typed transport, `ProblemContract.scope` for scope, `selective_reopen` for family
survival) and decided through the ME control layer: target/observation boundary,
problem identity, discrepancy-locus hypotheses, evaluator/diagnostic-evaluator
separation, typed transport, support-family reopening, the unresolved terminal
and the external authority boundary. Unused components are still charged for.

**Ablations (11):** `M_MINUS_{IDENTITY, APPARATUS, EVALUATOR, DEPENDENCE,
TRANSPORT, SCOPE, GLOBAL, NUMERIC, FAMILIES, AUTHORITY, UNRESOLVED}`.
**Controls (4 + 1):** `C_ALWAYS_COMMIT`, `C_NEVER_COMMIT`, `C_ALWAYS_UNRESOLVED`,
`C_RANDOM_DECISION`, and `M_ABSTAIN_WHENEVER_CENSORED` as an over-abstention
reference. 27 arms in total; all are reported in full, per mode.

## 5. Outcomes (protocol §6), reported per mode

Primary: the decision-triple exact rate. Secondary, per arm **and per mode**:
action / locus / authority exact rates; false scientific transition; missed
warranted transition; responsibility error; invalid transport accepted; false
closure over an unresolved terminal; unnecessary abstention; missed necessary
abstention; narrowing error; authority violation; cost (module operations, and
wall-clock which is the only commensurable scale). Per-stratum tables are emitted
for every arm. **A pooled average never routes anything on its own**: every gate
below is evaluated per mode, and the route reads the per-mode results.

## 6. Gates (frozen before any protected outcome exists)

- **G0a `NATIVE_KNOWN_ANSWER` (hard):** every parent passes its own native
  known-answer tests (20); the nine hand-authored fixtures (three per mode:
  partial family failure that must *not* defeat; a censored fact that must *not*
  produce `UNRESOLVED`; the narrowing route) are reproduced by the oracle; the
  separation pair behaves as §4 states; the three native-review records are
  complete.
- **G0b `ORACLE_VALIDITY` (hard):** every instance valid at v0, stratum invariant
  reproduced, censored facts within the frozen cap, decision invariant under a
  full relabelling of every element identifier.
- **G0c `NULL_CALIBRATION` (hard):** every truth-agnostic control ≤ 0.25
  decision-exact; `C_RANDOM_DECISION` ≤ 0.05; M scored against within-mode
  shuffled oracle decisions at least 0.50 below M's own rate in **every** mode.
- **G1a `B5_REPRODUCES_M`:** M and B5 emit the identical decision on ≥ 99.5% of
  instances in every mode.
- **G1b `M_ADVANTAGE_PER_MODE`:** paired decision-exact difference M − B5 > 0 with
  an exact two-sided McNemar p surviving **Holm correction across the three
  modes**.
- **G1c `B5_ADVANTAGE_PER_MODE`:** the symmetric test, likewise Holm-corrected.
  Registered because ME-X2's terminal was a federation win, not a tie.
- **G2 `ANTI_CONSERVATISM`:** on `FULLY_WARRANTED_CONTROL`, `AUTHORITY_MISMATCH`
  and `SINGLE_PARENT_SUFFICIENT`, M's manufactured doubt (false withholding +
  unnecessary abstention + missed warranted transitions) does not exceed B5's, in
  every mode.
- **G3a `MECHANISM_ATTRIBUTION`** (only where an advantage is claimed): for each
  stratum in an advantage mode where M is exact on ≥ 5 more instances than B5, the
  matching omission ablation's exact rate on that stratum ≤ B5's.
- **G3b `CROSS_MODE_MECHANISM_IDENTIFIABILITY`** (protocol §7(1)): for every
  ablation, the Holm-corrected paired loss when it is omitted, per mode. At least
  one mechanism must be load-bearing in ≥ 2 modes. **Reported whether or not any
  residual over B5 exists** — this is the study's positive content under a
  parent-sufficient terminal.
- **G4 `INTERFACE_LADDER`** (H-EXT-3), **per mode, never pooled:** (a)
  monotonicity — no rung k+1 significantly worse than rung k; (b) the
  **significant steps and the decisive rung are reported per mode**, together with
  whether the decisive rung varies across modes; (c) the **positive
  interface-standard test** — see §6.5.
- **G5 `CHANGED_VOCABULARY`** (protocol §8): one mode-blind rule set, written in
  ordinary scientific English without ORION vocabulary and reading native fields
  through a per-mode adapter, recovers the responsibility class in ≥ 90% of
  decidable instances in every mode, while the same classifier scored against
  within-mode shuffled oracle labels stays ≤ 35% (evaluated only where a mode has
  ≥ 100 decidable instances; below that the null is `NOT_ESTIMABLE`, never
  passed). The full 3 × 3 cross-adapter matrix is reported as a diagnostic.
- **COST:** wall-clock ratio with a 2× flag; reported, never a route by itself.

### 6.5 The interface-standard terminal is a positive test

ME-X2's `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL` was computed as the
*negation* of its gap gate, so it fired both on a tie and on a federation win and
could not be quoted alone. Here it is its own positive test and requires, **in
every mode**:

1. the ladder is monotone;
2. rung 1 is significantly worse than rung 5 (exact two-sided p ≤ 0.05) — the
   interface information is demonstrably load-bearing rather than merely
   sufficient;
3. M and B5 at full structure are **statistically equivalent** within a
   pre-registered margin: the 95% interval on the paired difference lies inside
   ±0.02 per mode (±0.01 pooled).

If any of the three fails, the terminal is plain `PARENT_SUFFICIENT`, not the
interface-standard reading.

## 7. Pre-registered routing

| outcome | route | field-support ladder (protocol §11) |
|---|---|---|
| G0 fail | `CANNOT_CHECK` — lane defect; repair, re-freeze, no arm verdict | not assigned |
| G1b in ≥ 2 modes ∧ G2 ∧ G3a ∧ G5 | `ME_X5_FIELD_RESIDUAL_CANDIDATE` | `R2_NOT_GRANTABLE_INDEPENDENT_ADJUDICATION_ABSENT` |
| G1b in ≥ 2 modes ∧ (¬G2 ∨ ¬G3a ∨ ¬G5) | `CANNOT_CHECK` | not assigned |
| G1b in exactly 1 mode | `MODE_SPECIFIC_RESIDUAL` (protocol §12: a single-domain residual contracts the field claim) | `R1_BENCHMARK_INTEGRATION_VALUE` |
| no advantage ∧ §6.5 positive test fires in every mode | `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL` | `R1` (or `R0` if G5 fails) |
| no advantage otherwise | `PARENT_SUFFICIENT` | `R1` (or `R0` if G5 fails) |

`R3_ESTABLISHED_FIELD` is never grantable. Where `G1c` fires the route is
annotated `(B5_DOMINATES in <modes>)`.

**No-rescue clause.** No stratum, weight, oracle rule, arm, seed, gate or margin
changes after the protected results file exists. Development-only tuning surface:
bug fixes to arm glue validated by the G0a known-answer tests before the seed is
revealed. A protected result is never re-run under a new seed; a lane defect found
mid-run halts the lane, is receipted, and re-freezes as V2.

## 8. Custody and protected-run discipline

- Code: `mex5_model.py`, `mex5_native_formal.py`, `mex5_native_measurement.py`,
  `mex5_native_synthesis.py`, `mex5_oracle.py`, `mex5_generator.py`,
  `mex5_parents.py`, `mex5_arms.py`, `mex5_vocab.py`, `mex5_run.py`; sha256 frozen
  in the receipt. Determinism: results and custody files are byte-identical on
  re-run (the only RNGs are instance seeds, the random-control seed and the
  shuffle-null seed 20260902); wall-clock lives in a separate timing file.
- Stages: `selftest`, `dev` (≤ 40 instances, label `DEVELOPMENT`, never
  protected), `protected`, `analyze`.
- The `protected` stage **refuses** unless `PROTECTED_RUN_AUTHORIZATION.json`
  (`human_written = true`, a human-written token ≥ 16 chars, and
  `acknowledged_design_sha256` = sha256 of the frozen design JSON) is present next
  to the runner **and** the custody seed hashes to the commitment. The file is
  absent in this PR; the tests assert its absence and the refusal paths.
- Outputs: `results/ME_X5_<LABEL>_RESULTS_V1.json` (arm outputs only),
  `…_EXPECTED_CUSTODY_V1.json` (oracle decisions + episodes), `…_TIMING_V1.json`,
  `…_ANALYSIS_V1.{json,md}`.
- Estimated protected cost: 1 440 instances × 27 arms ≈ 2 CPU-seconds on a laptop
  core (development: 36 instances in < 0.2 s). Never run as CI on the Mac mini.

### 8.3 What was inspected before freezing

A **full-scale dry run on the public seed `ME-X5-PUBLIC-DRYRUN-NOT-PROTECTED`**
was executed while writing this design, to verify runtime and that the gates are
estimable at n = 480 per mode. Its numbers are development evidence and are
reported in the parent-fidelity receipt. **No design constant, gate, threshold,
margin, arm, oracle rule, stratum or seed was changed after it.** The protected
split uses a different, committed seed.

## 9. Non-goals

No field status, novelty, adoption or publication authority. No claim from this
study reaches a naturalistic cell; protocol §7's naturalistic validation with
independent native reviewers remains a separate, unexecuted identity.

## 10. Registered limitations — read before quoting any number

1. **The common object is a design input, not a finding.** The decision shell
   (which family survives, which registered element is responsible, what authority
   the evidence licenses) was written once and instantiated three times. The three
   modes were authored by one team in one repository; shared authorship is a
   common cause for any cross-mode recurrence. G5 bounds this — it asks whether
   the structure is recoverable from native surface features without ORION
   vocabulary — but cannot remove it. **This study cannot show that the object was
   discovered independently in three fields.**
2. **No independent adjudication.** Protocol §8 asks for a separate reviewer;
   what is implemented is a formal recoverability surrogate. Protocol §11's `R2`
   requires independent adjudication and is therefore **not grantable here**,
   whatever the numbers.
3. **An exact planner is optimal by construction — in all three modes.** Carrying
   ME-X2's caveat (b) forward honestly: the numeric modes remove *Boolean-parent*
   optimality (a truth-maintenance system cannot represent an error budget or a
   pooled interval, which is why `B4` breaks on the numeric-defeat variant), but
   they do not remove *exact-computability* optimality. The registered information
   determines the decision in every mode, and the episodes are small enough for
   every arm to compute it exactly. The honest terminal under a null result is
   therefore **"no residual is detectable in a registered decision problem the
   parents already solve exactly"**, not "no residual exists". The one separation
   this design *can* exhibit is finite-information, not computational: the
   H-EXT-3 ladder (§4, §6.5).
4. **The oracle shell and the arms' compositions are two implementations of the
   same frozen decision format.** Agreement is necessary, not sufficient, for a
   residual; the decisive comparison is M vs B5, which share the registered inputs
   and the parent-owned modules.
5. **Balanced design.** The twelve strata are planted identically in all three
   modes, so cross-mode differences can only arise where the native rules differ.
   A finding that the ladder profile is the same in all three modes is therefore a
   statement about mode-invariance *under matched episode structure*, and is not
   comparable to the cross-*study* variation between ME-X1 (decisive step at
   R4→R5) and ME-X4 (significant steps at R1→R2 and R3→R4, monotone with a null
   final step and a zero rung-5 gap), which used different generators. The decisive
   rung is generator-dependent; X5 holds the generator fixed and varies the
   semantics.
6. **Synthetic, ORION-authored episodes** with registered outcome tables, where
   real episodes carry unregistered structure. Cost proxies are engine-native and
   not commensurable across engines; only wall-clock drives the cost flag.
