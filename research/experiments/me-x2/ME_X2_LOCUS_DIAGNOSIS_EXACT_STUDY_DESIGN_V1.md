# ME-X2 — Obstruction/Locus Classification and Minimum Escalation: Exact Known-Answer Study (Registered Design V1)

**Class:** exact-oracle known-answer study — **zero model calls, fully
deterministic, CPU-seconds**. It decides whether ORION-V2's witnessed-obstruction
and minimum-escalation semantics (`ontic_epistemic_boundary.assess_discrepancy_locus`,
`epistemic_architecture.route_frontier_action`, `jump.assess_jump` / `minimum_level`)
choose the **minimum responsible intervention** more often than the strongest
faithful parent federation given the same registered information. **Parent
sufficiency is a successful terminal** and is the pre-registered expectation (§1.2).

**Protocols served:** `ME_X2_LOCUS_DIAGNOSIS_PROTOCOL_V2.md` (axis A locus,
axis B intervention lattice, paired hostile families A–D, meta-evaluator
separation, ablations, kill conditions),
`MACHINE_EPISTEMICS_ME_X2_ONTIC_EPISTEMIC_DIAGNOSTIC_ADDENDUM_V1.md` (§3 cases
A–E, §4 paired fixtures, §5 separate reporting),
`MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md` §0–§2 and §4,
and `…_ADDENDUM_ARFT.md` — whose amendment fixes the **primary endpoint as the
intervention decision and outcome**, with taxonomy agreement secondary.
Ontology: `WORLD_MACHINE_SEPARATION_ONTOLOGY_V1.md` — the hidden cause is a fact
about the world/observation/machine that the acting system never receives; every
arm sees only observations, and `TARGET_WORLD` is a *hypothesis*, never an oracle.
House template: `research/experiments/me-x4/` (whose protected terminal is
`PARENT_SUFFICIENT`, main `4929a44`).

**Status:** frozen design + parent baselines + development fixtures. **No
protected outcome has been generated or inspected.** The protected stage refuses
to run (§8).

Companion: `ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.json` (schema
`orion.v2.me-x2.exact-study-design.v1`) carries every constant below;
`ME_X2_PARENT_FIDELITY_RECEIPT_V1.md` carries code hashes, parent fidelity
results and the development-split summary.

## 1. Question, hypothesis, expectation

**Q.** On paired episodes with the *same observed symptom* and different hidden
causes, does `M` — witnessed obstruction + locus receipt + lower-level
disposition + minimum-level policy — reach the **oracle minimum responsible
intervention** more often than `B5`, the strongest faithful parent federation
receiving the same registered information and budget?

**H0 (strongest-parent sufficiency).** An information-matched composition of
consistency-based diagnosis, value-of-information metareasoning, optimal test
sequencing, calibrated abstention, external process-failure taxonomy and
MDA-style model expansion makes the same intervention decisions at equal or
lower cost.

**1.2 Pre-registered expectation.** The registered outcome tables make this a
finite decision problem, and an exact expected-cost planner over the same typed
modules is optimal for it. The expected route is therefore `PARENT_SUFFICIENT`
with ladder terminal `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. The decisive
content is (a) whether any stratum breaks this, (b) where the single parents,
the taxonomy arm and the MDA arm break (attribution), (c) the H-EXT-3 ladder,
(d) false/missed escalation and regret.

**1.3 Primary endpoint (ARFT addendum).** Per instance, **decision-correct** is:

- oracle level *L* exists → the episode ends in `SUCCESS` whose last intervention
  is the oracle minimal fix **and no intervention above level *L* was applied**;
- oracle level is null → the episode ends in a `CANNOT_IDENTIFY` declaration
  **with no level ≥ 2 intervention applied**.

Class and locus agreement are secondary and enter as the mediation variable of
G3. A system that labels beautifully and intervenes wrongly fails this study.

## 2. Frozen inputs: generator and exact oracle

### 2.1 Registered information (identical for every arm)

An **instance** is a registered episode: a shared `symptom` and trajectory
`pattern`; an `apparent_class` (what the symptom looks like); **live cause
hypotheses**, each carrying an obstruction class (§4.2 of the decisive-studies
protocol), a discrepancy locus (protocol V2 axis A / addendum §2) and a
canonical minimal fix; **probes** with cost, an `evaluator_mediated` flag and an
exact registered outcome table; **interventions** with a Jump level (axis B),
cost and a registered `resolves` set; and a total **budget**. Hidden from every
arm: the true cause, the oracle module, the oracle targets and the partner
instance's truth.

Level cost bands are strictly increasing (0: 1–2, 1: 3–4, 2: 5–8, 3: 9–12,
4: 13–16, 5: 17–22, 6: 23–30), so the minimum-level resolving intervention is
also the minimum-cost one: level regret and cost regret cannot disagree.

### 2.2 Meta-evaluator separation

An `evaluator_mediated` probe returns its **nominal** outcome under every cause
whose locus is `EVALUATOR_VALIDATION`: a blind scientific evaluator launders its
own check. The **designed** table — what the check would report if the evaluator
were valid — is registered alongside it. Ladder rungs below the evaluator
contract read the designed table (they trust the scientific evaluator); the
diagnostic-evaluator contract reads the effective one. This is protocol V2's
requirement that the evaluator under diagnosis is never the evaluator that
certifies the diagnosis.

### 2.3 Templates (protocol V2 paired hostile families)

| template | symptom | family |
|---|---|---|
| `A_RESIDUAL` | systematic model–observation residual after t0 | A (same residual, different cause): target shift vs sensor drift vs model inadequacy vs preprocessing bug vs stale cache vs missing covariate vs blind evaluator vs no calibration standard |
| `A_PLATEAU` | evaluator score stops improving | addendum plateau signature: more search vs model vs representation collapse vs saturated evaluator vs criterion already met vs objective omits the criterion vs misset parameter |
| `B_PROOF` | proof search fails | B (same proof failure): shallow search vs missing lemma vs encoding vs missing operator vs wrong specification vs semantic-alignment evaluator vs transient tool failure vs prover capability |
| `C_NONDISCRIM` | hypotheses remain undiscriminated | C: more samples vs insensitive channel vs inadequate family vs intervention needed vs unidentifiable criterion vs blind evaluator vs analysis bug |
| `D_WORKFLOW` | pipeline output invalid | D: local tool bug vs orchestration metadata loss vs locally fixable metadata loss vs invalid evaluator vs wrong model vs wrong criterion vs transient env vs tool capability |

Every registered obstruction class appears as a truth; the locus set covers
`TARGET_WORLD`, `OBSERVATION_MEASUREMENT`, `EPISTEMIC_MODEL`,
`REPRESENTATION_REGIME`, `PROBLEM_CRITERION`, `EVALUATOR_VALIDATION`,
`PROCESS_TOOL_WORKFLOW`, `NO_MATERIAL_DISCREPANCY` and `CANNOT_IDENTIFY`.
Addendum §3 cases are realised directly: *world changed / model valid before*
(`TARGET_SHIFT_REFIT`, level 0) vs *sensor changed / world did not*
(`SENSOR_DRIFT_RECAL`, level 1) vs *model inadequate* (level 2) vs *preprocessing
bug* (level 1) vs *stale cache* (level 1) vs *cannot tell* — all under one
residual symptom.

### 2.4 Exact oracle

Tests = probes ∪ level ≤ 1 interventions (repair-as-test). The total of a test
set is its cost plus the cost of the truth's minimum fix, except that a repair
in the set that already resolves the truth *is* the fix. A set is affordable
when that total is within budget.

- **identifiable** ⟺ some affordable set separates the truth from every rival;
- **U** = the truth plus every rival that no affordable set separates individually;
- **oracle class / locus** = the common class / locus over U, else `CANNOT_IDENTIFY`;
- **oracle level** = the common minimum-fix level over U when every member of U
  has the same minimum fix, else null.

So a `SAME_FIX` pair yields an identified class and level with an unresolved
*locus* — exactly the addendum's "the intervention is determined while the
ontic/epistemic question is not". Two implementations must agree on every
instance (G0b): bitmask enumeration over all 2ⁿ subsets and an independent
branch-and-bound DFS.

**Uniform decidability.** An instance is admitted only if a single
**truth-agnostic policy tree** is decision-correct for *every* live cause taken
as the truth (exact search over registered actions). Without this an oracle
target can be unreachable except by knowing the answer, and the study would
measure luck. The generator raises the budget within a bounded scan until this
holds, then re-checks the variant invariant.

### 2.5 Generator and hostile decoys

Pairs share template, symptom, apparent class, live causes, probes,
interventions, costs and budget; only the hidden truth differs. Variants:
`PLAIN` (probe-identifiable), `PARTIAL` (identifiable only via a repair-as-test),
`SAME_FIX` (locus unresolved, level determined), `CI` (planted
`CANNOT_IDENTIFY`). Instance seed = `sha256(split_seed|stratum|index)[:12]`;
deterministic rejection sampling.

The apparent class is drawn by a frozen rule: ½ the highest-typical-level live
class, ¼ the truth's class, ¼ a random other live class. Hence:

- a **decoy** (apparent typical level > oracle level) punishes "escalate when
  stuck" — protocol §4.4's requirement of at least one per family;
- an **inverse decoy** (apparent typical level < oracle level) punishes a blanket
  refusal to escalate;
- apparent-`CANNOT_IDENTIFY` instances that are in fact identifiable punish
  premature abstention.

G0b requires ≥ 5 of each per class on the protected split.

### 2.6 Finite separation example (H-EXT-3)

`SEP-P` / `SEP-Q` share symptom, probes, interventions, costs and budget. Live:
`PREPROCESS_BUG` (locus `PROCESS_TOOL_WORKFLOW`, minimal fix level 1) and
`MODEL_INADEQUATE` (locus `EPISTEMIC_MODEL`, minimal fix level 2, whose
`resolves` set also covers the bug). The only probe is evaluator-mediated and
rejects under both. A federation whose inter-module channel carries only a
family-anonymous per-claim **class verdict** receives the identical verdict in P
and Q and must therefore err on one of them (in P it escalates to level 2 where
level 1 suffices); structure exchange (rung 5) and M are decision-correct on
both. The selftest asserts exactly this.

## 3. Strata and counts

Stratum = **oracle class** (the 12 registered obstruction families, including
`NO_ESCALATION_NEEDED` and `CANNOT_IDENTIFY`). Protected: 50 pairs per stratum =
**1 200 instances**. Development: 2 pairs per stratum = 48.

**Seed commitment.** Protected seed sha256
`4860b800dd43818f2c030c41746abec41068b1a7e998bd17208c5914b1390528`
(operator custody `~/.orion-custody/me-x2/PROTECTED_SEED_V1.txt`, mode 600; the
runner verifies the hash before any protected generation; the seed string is
revealed in the outcome receipt so the split regenerates byte-for-byte).
Development seed (public): `ME-X2-DEV-20260902`.

**Power / MDE.** Primary statistic = paired per-instance decision-correct
indicator, M vs B5, exact two-sided binomial (McNemar exact) on discordant
pairs; estimand P(M) − P(B5) with a paired Wald interval. Pooled n = 1 200:
6 one-directional discordants (0.5%) reach p = 0.031, 8 reach p = 0.008; per
stratum n = 100, 6 discordants reach p = 0.031. Prior expectation is zero
discordance; the test is two-sided, so a B5 advantage is equally detectable (G1c).

## 4. Arms (protocol V2 §Baselines, §4.5)

Every parent passes its own native known-answer tests before use
(`mex2_parents.fidelity_selftests`, 21/21; receipt §2).

| arm | native semantics |
|---|---|
| `B0_RETRY_SEARCH` | repeat the cheapest registered intervention (≤ 3 times) |
| `B1_UNCERTAINTY_ABSTENTION` | Chow / selective prediction, τ = 0.9 on the class posterior |
| `B2_FAILURE_TAXONOMY_DIAGNOSIS` | ARFT-equivalent pattern → standard fix, then ascending level |
| `B3_MODEL_BASED_DIAGNOSIS_VOI` | GDE consistency-based diagnosis (de Kleer & Williams 1987) + myopic VoI / rational metareasoning (Howard 1966; Russell & Wefald 1991), failure penalty 10× budget |
| `B3_EQUAL_EXTRA_SEARCH_1_5X` | the same arm at 1.5× budget — matched extra-search control |
| `B4_MDA_MODEL_EXPANSION` | model-discovery-agent criticism → model-family expansion, else B3 |
| `B5_…_FEDERATION` (rung 5) | exact finite-horizon expected-cost planner over (candidate set, budget) with the τ gate on level ≥ 2 acts: Bayes-optimal test-and-repair sequencing over the typed modules |
| `B5_NO_ABSTENTION_GATE` | federation variant without the abstention gate |
| `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION` | ORION reference semantics only (§4.1) |

**B5 ladder (H-EXT-3).** Rungs differ only in what crosses the module boundary:
R1 verdict only → R2 + candidate set → R3 + discriminator tables → R4 +
disposition records → R5 + the diagnostic-evaluator contract (= everything M
sees). **Rung 5 is the primary comparator**; rungs 1–4 are ablations of B5, never
of M. B5 is never artificially isolated.

### 4.1 What M is

No new engine. Per step M builds a `LocusHypothesis` per live cause and calls
`assess_discrepancy_locus` with a `LocusDiagnosisEvidence` whose
`diagnostic_evaluator_adequate` flag is the *diagnostic* evaluator (registered
discriminators exist, or a single fix is common to the live set) — never the
scientific evaluator under diagnosis. A unique supported hypothesis yields
`ACTIONABLE_LOCUS_HYPOTHESIS`; several yield
`MULTIPLE_LIVE_LOCUS_HYPOTHESES`; an inadequate diagnostic evaluator yields
`CANNOT_IDENTIFY`, which M reports rather than converting into a forced causal
attribution. A level ≥ 2 intervention is routed through
`route_frontier_action` on a `FrontierObstruction` carrying witnesses,
discriminators and **lower-level dispositions** (every registered level ≤ 1
intervention tried, semantically excluded or unaffordable), and then through
`JumpTrigger` / `JumpProposal` / `assess_jump`, with `minimum_level` selecting
among admissible proposals. One addition, registered here as part of M: a
**fail-closed reachability rule** — a discriminating action is admissible only
if, under every registered outcome, every hypothesis establishable now stays
establishable. Spending the episode out of reach of a warranted minimal
intervention is a resource leak, not a lower-level disposition.

**Ablations / controls (protocol V2 §Required ablations):**
`M_MINUS_LOCUS_DIAGNOSIS`, `M_LOCUS_LABELS_SHUFFLED`,
`M_MINUS_DIAGNOSTIC_EVALUATOR_GATE`, `M_MINUS_LOWER_LEVEL_DISPOSITION`,
`M_MINUS_PROSPECTIVE_DISCRIMINATOR`, `M_ALWAYS_ESCALATE_WHEN_STUCK`,
`M_NEVER_ESCALATE`, `B3_EQUAL_EXTRA_SEARCH_1_5X`, plus `C_RANDOM_POLICY` and
`C_NEVER_INTERVENE`.

### 4.2 ARFT mapping hypothesis (frozen before outcomes)

Registered in the design JSON: each trajectory pattern maps to ORION classes as
`MANY_TO_ONE`, `ONE_TO_MANY` or `MULTI_CAUSAL`, and one registered pattern
(`UNMAPPED_AGENT_LOOP_PATTERN`) has **`NO_MAPPING`** — a hostile counterexample
to universality, kept in the table rather than removed. The ORION taxonomy is
not edited to improve agreement. **Limitation, registered before outcomes:**
ARFT itself is not licensed or executed here; B2 uses an equivalently strong
pattern → standard-fix taxonomy with complete trajectory access.

## 5. Outcomes (protocol V2 primary outcome vector, addendum §5)

Per arm: obstruction classification accuracy; locus accuracy; confidence
calibration (Brier, 5-bin ECE); **minimal-level decision accuracy (primary)**;
verified success; false escalation; missed escalation; false / correct
`CANNOT_IDENTIFY`; recurrence after a wrong intervention; specification damage
(a level-4 reformulation where the truth locus is not `PROBLEM_CRITERION`);
false world-change, false model and false representation attribution; regret vs
the oracle minimal responsible intervention; total cost; wall-clock (reported
only). Reported per arm, per stratum and per variant. No pooled score
compensates for wrong target-change attribution, evaluator laundering or
specification damage.

## 6. Gates (frozen before any protected outcome exists)

- **G0a `KNOWN_ANSWER` (hard):** 14 hand-authored fixtures (oracle targets by
  hand; M and B5 decision-correct) + the separation pair, in `selftest`.
- **G0b `ORACLE_SELF_AGREEMENT` (hard):** enumeration = branch-and-bound on every
  instance; a truth-agnostic decision-correct policy exists on every instance;
  variant invariants hold; ≥ 5 decoys per apparent class (typical level ≥ 1),
  ≥ 5 inverse decoys per level-0 class, ≥ 5 apparent-`CANNOT_IDENTIFY`
  identifiable instances.
- **G0c `NULL_CALIBRATION` (hard):** `C_NEVER_INTERVENE` decision-correct = 0 on
  identifiable instances; `C_RANDOM_POLICY` ≤ 0.25; **M scored against the
  partner instance's oracle** (within-pair label swap) ≤ M's true rate − 0.30.
- **G1a `B5_REPRODUCES_M`:** decision sequences identical on ≥ 99.5% of instances,
  no stratum > 5% discordant.
- **G1b `M_ADVANTAGE`:** paired decision-correct difference > 0, exact two-sided
  p ≤ 0.05, ≥ 1 stratum with ≥ 5 M-only-correct instances.
- **G1c `B5_ADVANTAGE`:** the symmetric test.
- **G2 `ANTI_ESCALATION`:** M's false escalations ≤ B5's **and** M's
  specification damage ≤ B5's.
- **G3 `MEDIATION`** (only if G1b): (a) M's class correct on ≥ 80% of
  M-only-correct instances; (b) on every advantaged stratum both locus ablations
  ≤ B5; (c) B3 at 1.5× budget does not reach M (paired exact p ≤ 0.05).
- **G4 `INTERFACE_LADDER`** (H-EXT-3): monotonicity (no rung k+1 significantly
  worse than rung k) and the rung-5 gap. Terminals: monotone ∧ gap null →
  `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`; monotone ∧ gap persists →
  `CONTROL_RESIDUAL_CANDIDATE_AT_FULL_STRUCTURE`; non-monotone →
  `LADDER_NON_MONOTONE`.
- **COST:** paired sign test on per-instance regret in registered cost units,
  p ≤ 0.05. Wall-clock is reported only and routes nothing.

## 7. Pre-registered routing

| outcome | route |
|---|---|
| G0 fail | `CANNOT_CHECK` — lane defect; repair, re-freeze, no arm verdict |
| G1a pass | `PARENT_SUFFICIENT` (ladder `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`) |
| G1b ∧ ¬G2 | `M_OVER_ESCALATES` |
| G1b ∧ G2 ∧ ¬G3 | `CANNOT_CHECK` — advantage not attributable to locus diagnosis |
| G1b ∧ G2 ∧ G3 ∧ cost `COST_ADVANTAGE_B5` | `QUALITY_COST_TRADEOFF_NO_DOMINANCE` |
| G1b ∧ G2 ∧ G3 otherwise | `ME_X2_RESIDUAL_CANDIDATE` |
| G1c pass | `PARENT_SUFFICIENT` (`B5_DOMINATES`) |
| neither | `PARENT_SUFFICIENT` |

Protocol V2's kill conditions map onto: `PARENT_SUFFICIENT` (B3/B5 matches the
routing frontier, or taxonomy + metareasoning reproduces the interventions),
`M_OVER_ESCALATES` (false escalation or specification damage offsets gains),
`CANNOT_CHECK` (gains not mediated by correct locus, or a diagnostic-evaluator
failure silently converted into a forced attribution — the
`M_MINUS_DIAGNOSTIC_EVALUATOR_GATE` ablation exists to price exactly that), and
the design invariant that no arm imports the oracle.

## 8. Custody and protected-run discipline

- Code: `mex2_model.py`, `mex2_catalogue.py`, `mex2_oracle.py`,
  `mex2_generator.py`, `mex2_parents.py`, `mex2_arms.py`, `mex2_run.py`; sha256
  frozen in the receipt. Determinism: results and custody files byte-identical
  on re-run; wall-clock in a separate timing file.
- Stages: `selftest`, `dev` (≤ 48 instances, label DEVELOPMENT, never protected),
  `protected`, `analyze`.
- The `protected` stage **refuses** unless `PROTECTED_RUN_AUTHORIZATION.json`
  (human_written = true, a human-written token ≥ 16 chars,
  `acknowledged_design_sha256` = sha256 of the frozen design JSON) is present
  next to the runner **and** the custody seed hashes to the commitment. The file
  is absent in this PR; the tests assert its absence and the refusal paths.
- Estimated protected cost: 1 200 instances × 22 arms ≈ 20–60 CPU-seconds on one
  core (development: 48 instances in < 1 s). Runs locally on the Mac; never as a
  heavy job; never CI on the Mac mini.

## 9. Non-goals, no-rescue clause, registered limitations

No stratum weight, oracle rule, arm, seed, gate or threshold changes after the
protected results file exists. Development-only tuning surface: arm-glue bug
fixes validated by the G0a known-answer tests before the seed is revealed. A
protected result is never re-run under a new seed; a lane defect found mid-run
halts the lane, is receipted, and re-freezes as V2. No claim from this study
reaches the naturalistic cell. No field status, novelty or publication authority.

Registered limitations (before outcomes): these are synthetic ORION-authored
episodes and cannot alone support a field-level residual (decisive-studies
§11.6); the registered outcome tables make diagnosis a finite decision problem
whereas real episodes carry unregistered hypotheses; ARFT is represented by an
equivalent taxonomy rather than the licensed artifact; the uniform prior over
live causes is a modelling choice shared by every arm; the Jump lattice is used
as a comparator interface and is not presumed correct.
