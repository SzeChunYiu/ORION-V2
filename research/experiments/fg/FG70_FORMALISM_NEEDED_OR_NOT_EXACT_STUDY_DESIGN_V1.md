# FG70 — Formalism Needed or Not: Exact Known-Answer Study (Registered Design V1)

**Series:** `ORION-FG-L5-EXACT-V1` — the L5 formalism-genesis layer of ORION-V2,
owner issue #50 §L5, registered protocol
`research/experiments/FORMALISM_GENESIS_PROTOCOL_V1.json` (study `FG70`),
registered backlog `research/experiments/FORMALISM_GENESIS_BACKLOG_V1.json`.

**Class:** exact-oracle known-answer study — **zero model calls, fully
deterministic, CPU-seconds**. It decides whether ORION's formalism-genesis
mechanism routes a registered representational deficit to the *cheapest
adequate* repair, and whether it does so beyond the strongest faithful parent
federation receiving the same registered information. **Parent sufficiency is a
successful terminal** and is the pre-registered expectation (§1.2).

**Status:** frozen design + parent baselines + development split. **No protected
outcome has been generated or inspected.** The protected stage refuses to run
(§8).

Companion: `FG70_FORMALISM_NEEDED_OR_NOT_EXACT_STUDY_DESIGN_V1.json` (schema
`orion.v2.fg70.exact-study-design.v1`) carries every constant below;
`FG_PARENT_FIDELITY_RECEIPT_V1.md` carries code hashes, parent fidelity results
and the development-split summary.

## 0. Disambiguation — this is not the fmfg-r2 campaign

`research/experiments/fmfg-r2/` contains studies **named** `fg10`–`fg80` under a
different owner issue (#48), the `FM_FG_GENERATED_EXACT_CAMPAIGN`. That campaign
dispatched **language-model solver arms** (`TARGET_ONLY_DIRECT`,
`STRONGEST_DOMAIN_FORMAL_PARENT`, `F0_PARENT_FEDERATION`,
`F2_STATIC_NO_FORMAL_DISCOVERY`, `F2_FORMAL_DISCOVERY_FULL`) over generated
formal-discovery tasks — 1 712 tasks × 5 arms = 8 560 dispatches — and
terminated at `REGISTERED_SCALE_NULL`.

This study is a **different object with the same label**:

| | fmfg-r2 `fg70` | this FG70 |
|---|---|---|
| owner issue | 48 | 50 (§L5) |
| arms | language-model solvers | deterministic algorithms only; **no model is called** |
| oracle | generated-task answer key | exhaustive tier search, two independent implementations |
| question | does formal discovery raise solver success at registered scale | is the active *language* too coarse, and if so what is the cheapest adequate repair |
| comparator | arm-vs-arm success rate | mechanism vs strongest faithful parent federation |

Nothing here replicates, contradicts or supersedes fmfg-r2, and no generator,
oracle, arm or task is shared with it. The fmfg-r2 receipts are frozen and are
**not** modified by this lane. fmfg-r2 is used only as a *prior*: its `fg70`
stratum carried the widest non-frontier arm spread (0.825–0.900), which is one
reason FG70 is built first in this series.

## 1. Question, hypothesis, expectation

**Q.** When a registered decision family `J` collides under the active formalism
`F` — i.e. `C_F = {(i,j) : q_F(x_i) = q_F(x_j) and J(x_i) ≠ J(x_j)}` is
non-empty — does `M` select the cheapest tier of the §L5 search order that
actually resolves every collision, and does it do so beyond the strongest
faithful parent federation receiving the same registered information?

`C_F ≠ ∅` proves only that `F` is too coarse **for that registered decision
family**. It never proves that a new formalism is needed. The whole content of
the suite is the distance between those two statements.

**H0 (strongest-parent sufficiency).** An information-matched federation of
anti-unification, formal concept analysis, MDL abstraction search, finite
model/countermodel search, conservative-extension checking and AGM-style theory
revision makes the same routing decisions at equal or lower cost.

**1.2 Pre-registered expectation.** The registered search order is *public
information* (it is stated in issue #50 §L5), so the federation receives it, as
ME-X4 §4 requires ("B5 is never artificially isolated"). The expected route is
therefore `PARENT_SUFFICIENT`. The decisive content of the study is (a) the
**false-formalism-invention** behaviour of every arm under maximal temptation,
(b) where single parents break and why, (c) the 2×2 mechanism-by-omission
factorial, and (d) whether any stratum breaks the federation.

## 2. Frozen inputs: generator and exact oracle

### 2.1 Registered information (identical for every arm)

An **instance** carries: a finite observable set (5 recorded, 1 unobserved, each
with a 2- or 3-valued domain); 12 registered **cases**, each a total assignment
plus its registered decision `J(x) ∈ {d0,d1,d2}`; the **active formalism** `F`
(2 atomic terms); a **registered parent-formalism library** of 2–4 alternative
languages over the recorded observables; 0–2 registered **relations** over the
case set; and a **patch budget** (2). Every arm receives exactly this
(`fg_model.arm_view`), which never carries the stratum or the planted decoy
labels. The oracle module is never imported by an arm; a test asserts it.

### 2.2 The repair ladder (frozen; it transcribes §L5's mandated search order)

| tier | terminal | what it is | what it costs |
|---|---|---|---|
| 0 | `NO_CHANGE` | `C_F = ∅` | nothing |
| 1 | `PARENT_FORMALISM_SUFFICIENT` | adopt a language that already exists in the registered library | naming it |
| 2 | `ADD_ONE_OBSERVATION` | add exactly one atomic observable to the signature (recorded-but-unused, or requiring a new measurement) | one variable |
| 3 | `LOCAL_PATCH` | a scope condition excepting ≤ `patch_budget` cases, whose decisions are then enumerated | the exceptions |
| 4 | `REPRESENTATION_CHANGE` | add ≤ 2 terms from the frozen depth-1 grammar `{EQ, SUM3, DIFF3}` over recorded observables — a re-encoding inside the existing primitives | the definitions |
| 5 | `NEW_PRIMITIVE` | introduce a relational primitive (`COMP`, `REACH`) over the registered relation, with its type and derived operation | the primitive's whole extension |

The truth of an instance is **the cheapest feasible tier**, computed by
exhaustion. The brief's four cheaper answers (`parent / local patch / more data
/ no change`) are tiers 0–3; tiers 4 and 5 are the two ways a language can
change, and only tier 5 is *formalism invention* — a representation change stays
inside the old primitives, exactly as §L5's ordering implies.

### 2.3 Exact oracle, two independent implementations

* **Method A** — collisions by signature bucketing; each candidate repair is
  reduced to a bitmask over the required-pair set and tested by cover; the patch
  tier is decided by exhaustive vertex-cover enumeration.
* **Method B** — collisions by an independent pairwise scan; feasibility is
  decided by set-partition semantics (a repair resolves iff no block of the
  common refinement mixes two decisions); the patch tier is decided from the
  *kept* set rather than the cover.

Gate **G0b** requires terminal, collision set and feasible-tier vector to agree
on every instance. Neither method imports `orion_v2.formalism_genesis`; the
selftest separately checks that the reference module's
`representation_collisions` agrees with the oracle's collision set and records
that agreement is **necessary, not sufficient**, for a residual (ME-X4 §9(5)).

### 2.4 Generator and stratum verification

Each planter builds the world, fixes `J` so that its intended tier resolves the
deficit, then selects the registered parent library **after** `J` is fixed by
exhaustively classifying every 2- and 3-atom subset by its residual collision
count (this is what makes "no parent works" a checked fact rather than a hope).
The instance is then re-derived by both oracle methods and **rejected unless its
cheapest feasible tier is the intended stratum**. Instance seed =
`sha256(split_seed | stratum | index)[:12]`; up to 4 000 attempts.

### 2.5 Decoys — the anti-invention design

Every stratum carries structure that rewards a *more expensive* answer:

* **Maximal invention temptation.** On every instance whose truth is
  `PARENT_FORMALISM_SUFFICIENT`, `ADD_ONE_OBSERVATION`, `LOCAL_PATCH` or
  `REPRESENTATION_CHANGE`, the world registers a relation whose connected
  components coincide with the decision classes. A new primitive is therefore
  **always available and always adequate** on 112 of the 168 instances. The
  suite measures parsimony under maximal temptation, not the difficulty of
  finding a working primitive. An arm that escalates is never "wrong because the
  primitive fails"; it is wrong because something cheaper was sufficient.
* **Near-miss parent** — a registered parent leaving exactly one collision,
  wherever one exists (24/28 on most strata in development).
* **Near-miss observation** — an observable resolving all but one collision.
* **Over-budget cover** — on `NEW_PRIMITIVE` instances a patch of size
  `budget + 1` exists, so an arm that relaxes the budget is wrong.
* **Coarser-projection decoy** on `NO_CHANGE`: dropping one active term produces
  apparent collisions, so an arm that mis-projects reports a deficit that is not
  there.

### 2.6 Counts

Protected: **28 per stratum × 6 strata = 168** (registered minimum 160),
perfectly balanced. Development: 6 per stratum = 36. False-invention
denominator = **140** (every instance whose truth is not `NEW_PRIMITIVE`), and
each of the five non-`NEW_PRIMITIVE` strata contributes 28; a stratum with an
empty denominator hard-fails the gate.

**Seed commitment.** Protected seed sha256
`4b34cb8798a01c5a2223a50453b6491d3dcf10f12139c7a8a8144aa4f68355bb`
(operator custody `~/.orion-custody/fg/PROTECTED_SEED_V1.txt`, mode 600; the
runner verifies the hash before any protected generation; the seed string is
revealed in the outcome receipt so the split regenerates byte-for-byte).
Development seed (public): `FG70-DEV-20260902`.

**Power / MDE.** Primary statistic = paired instance-level terminal match, M vs
the federation, exact two-sided binomial on discordant pairs (McNemar exact),
Holm-adjusted across the FG10–FG70 family. At n = 168, 6 one-directional
discordants reach p = 0.031. The prior expectation is zero discordance; the test
is two-sided so a federation advantage is equally detectable.

## 3. Arms

**Single faithful parents** (each passes its own native known-answer tests
before use — `fg_parents.fidelity_selftests`, 42 checks, receipt §2):

| arm | native semantics | native repertoire limit |
|---|---|---|
| `P1_LGG_ANTIUNIFICATION` | Plotkin (1970) least general generalization, θ-subsumption; deficit = a class generalization subsumes a foreign case | extends argument positions; has no notion of adopting a rival language or of a scope exception |
| `P2_FCA_GALOIS_CLOSURE` | Ganter & Wille derivation operators, closure, concept lattice, attribute implications; the adjunction is checked through `orion_v2.meta_formalization.assess_galois_connection` | compares attribute sets; has no exception mechanism |
| `P3_MDL_ABSTRACTION_SEARCH` | two-part code `L(H) + L(D|H)` over a frozen native code, argmin over every registered repair | its own code, **not** the registered order — it prices a derived term below a two-case patch and a new primitive by its whole extension |
| `P4_MODEL_COUNTERMODEL_SEARCH` | finite countermodel search by exhaustion | no cost model at all: canonical (alphabetical) scan over terminals |
| `P5_CONSERVATIVE_EXTENSION_CHECK` | `orion_v2.meta_formalization.assess_conservative_extension` | an *admission filter*, not a selector: `CANNOT_CHECK` whenever more than one extension is admissible |
| `P6_THEORY_REVISION_BASELINE` | Hansson kernel contraction with a canonical incision function | base revision cannot extend a language: `CANNOT_CHECK` when the minimal contraction exceeds the budget |

A parent's `CANNOT_CHECK` is its honest native boundary, never a strawman.

**`B_STRONGEST_FAITHFUL_PARENT_FEDERATION`** — FCA for deficit detection and
parent evaluation, cross-verified by countermodel search (disagreement ⇒
`CANNOT_CHECK`, never a guess); LGG's extension search for the observation and
representation tiers; AGM kernel contraction for the patch tier; MDL for
within-tier minimality; conservative-extension checking for admission — walked
in the **registered public order**. This is the primary comparator.

**`M_FG_SEARCH_ORDER`** — the ORION reference mechanism, no new M:
`orion_v2.formalism_genesis.representation_collisions` for the deficit,
`minimal_discriminating_feature_sets` for minimal distinctions, the §L5 ladder,
and `assess_formalism_candidate` as a **fail-closed admission gate** on any
candidate new primitive. The candidate is bound with the full §L5 tuple
(primitives, types, relations, operations, axioms, derivation rules, semantic
model, recovery map, intended deficit, prospective consequence), and its
`minimality_or_simpler_patch_check_pass` is set to *false whenever a cheaper
adequate repair exists* — which is precisely the condition that must block
invention. M is **not** the oracle: the oracle is an independent exhaustive
search and cannot be blocked by an admission gate.

**Ablations and controls.** One *tier* omission per stratum, so every stratum
has an ablation that removes a mechanism it needs: `M_MINUS_DEFICIT_CHECK`
(NO_CHANGE), `M_MINUS_PARENT_SEARCH`, `M_MINUS_DATA_TIER`, `M_MINUS_PATCH_TIER`,
`M_MINUS_REPRESENTATION_TIER` and `M_MINUS_INVENTION_TIER`. NEW_PRIMITIVE is
attributed to omitting the escalation tier itself rather than to the admission
gate, because a gate that can only ever *block* cannot degrade the stratum where
invention is correct. The gate's own mechanism is
measured on the anti-invention axis instead, through the 2×2 factorial
`M_MINUS_ADMISSION_GATE` (order kept, gate off) × `M_MINUS_COST_ORDER` (gate
kept, order reversed) × `M_MINUS_ORDER_AND_GATE` (both off). Further controls:
`M_EAGER_INVENT` (skips the parent, observation and patch tiers),
`C_ALWAYS_INVENT`, `C_NEVER_CHANGE` (its mirror: emits `NO_CHANGE`
unconditionally, and is the planted positive for G2),
`C_RANDOM_TERMINAL`.

## 4. Outcomes

Per arm: terminal accuracy; **false formalism invention** (`NEW_PRIMITIVE`
emitted when the truth is cheaper) with its denominator; missed deficit
(`NO_CHANGE` emitted when the truth is not); over- and under-escalation by tier
cost; `CANNOT_CHECK` count; and the full per-arm × per-stratum table. All arms ×
all strata are reported in full.

## 5. Gates (frozen before any protected outcome exists)

Every gate reports the **number of instances actually evaluated** beside its
violation count, and every no-alarm assertion is paired with a planted positive
that must trip it.

- **G0a `KNOWN_ANSWER` (hard):** six hand-authored fixtures, one per terminal,
  with expected answers computable by reading them, reproduced by the oracle, by
  M and by the federation.
- **G0b `ORACLE_SELF_AGREEMENT` (hard):** method A = method B on every instance
  (terminal, collision set, feasible-tier vector); `instances_evaluated` must
  equal the split size.
- **G0c `NULL_CALIBRATION` (hard):** `C_RANDOM_TERMINAL` accuracy ≤ 0.25
  (chance = 1/6); M scored against within-split **shuffled labels** ≤ 0.30;
  **planted positive** `C_ALWAYS_INVENT` false-invention rate ≥ 0.50 and
  `M_MINUS_ORDER_AND_GATE` > 0 (both must trip G2M); **planted positive**
  `C_NEVER_CHANGE` missed-deficit rate ≥ 0.50 (must trip G2). A gate that cannot
  be shown to fire is a broken gate.
- **G1a `FEDERATION_REPRODUCES_M`:** terminal identity ≥ 99.5% and no stratum
  discordance > 5%.
- **G1b `M_ADVANTAGE`:** paired exact two-sided p ≤ 0.05 with M ahead, Holm
  across FG10–FG70.
- **G2 `ANTI_CONSERVATISM`:** M's missed-deficit count ≤ the federation's, over
  the 140 instances whose truth is not `NO_CHANGE`. Because every arm's first
  move is the shared collision check, under-detection is structurally hard to
  reach and this counter would otherwise report `0 ≤ 0` with no evidence it can
  fire; it is therefore paired with the planted positive `C_NEVER_CHANGE`, whose
  missed-deficit count on the same denominator is reported beside M's.
- **G2M `ANTI_INVENTION` (co-primary, non-compensatory):** M's false-invention
  count ≤ the federation's **and** rate ≤ 0.02, over the 140 instances whose
  truth is not `NEW_PRIMITIVE`; hard-fails if any non-`NEW_PRIMITIVE` stratum
  has an empty denominator. **This gate cannot be traded against accuracy:** its
  failure routes to `FALSE_INVENTION_HARM` even when M's terminal accuracy is
  higher than the federation's.
- **G3 `MECHANISM_BY_OMISSION`:** per stratum, the matching omission ablation
  degrades relative to M (scored only if G1b fires). Each of the six strata has
  an ablation that removes a mechanism it genuinely needs — a rule that must be
  *satisfiable*: mapping `NEW_PRIMITIVE` to `M_MINUS_ADMISSION_GATE` would make
  it unsatisfiable by construction, because a gate that only blocks cannot
  degrade the stratum where invention is correct. Plus the 2×2 factorial
  omission of the registered cost order and of the admission gate, reported
  unconditionally.

## 6. Pre-registered routing

| outcome | route |
|---|---|
| G0b or G0c fail | `CANNOT_CHECK` — lane defect; repair, re-freeze, no arm verdict |
| G2M fail | `FALSE_INVENTION_HARM` (fires regardless of accuracy) |
| G2 fail | `M_OVER_CONSERVATIVE` |
| G1a pass | `PARENT_SUFFICIENT` |
| G1b pass ∧ G3 pass | `FG70_RESIDUAL_CANDIDATE` |
| G1b pass ∧ G3 fail | `CANNOT_CHECK` — advantage not attributable to a named mechanism |
| otherwise | `PARENT_SUFFICIENT` |

Protocol kill conditions map onto: `PARENT_SUFFICIENT` (the strongest parent
resolves the deficit, or a simpler patch explains the improvement),
`FALSE_INVENTION_HARM` (the candidate is emitted where a cheaper repair
suffices), and the design invariant that no arm imports the oracle.

## 7. Ordering deviation from the registered backlog

The backlog lists `FG70` as `depends_on: [FG10 … FG60]`. That is a **taxonomy**
dependency, not a data dependency: FG70 consumes the deficit families the design
fixes, not the other suites' outcomes. It is executed first because a wrong
answer here is the failure issue #50 §L5 singles out — inventing a formalism
when a parent, a patch or one more observation would do — and because the
fmfg-r2 prior shows the other non-frontier suites are ceiling-heavy. The
remaining suites are unaffected: none of them reads an FG70 outcome.

## 8. Custody and protected-run discipline

- Code: `fg_model.py`, `fg_oracle.py`, `fg70_generator.py`, `fg_parents.py`,
  `fg_arms.py`, `fg_run.py`; sha256 frozen in the fidelity receipt.
  Determinism: results and custody files are byte-identical on re-run **and
  across processes** (the only RNGs are the instance seeds, the random-control
  seed and the shuffle-null seed, all frozen). Cross-process reproducibility is
  a load-bearing invariant, not a nicety: Python randomises string hashing per
  process, so a planter that drew an RNG value while iterating an unordered set
  would regenerate a different "same" split elsewhere. No planter may iterate an
  unordered set; the tests assert it behaviourally (`PYTHONHASHSEED` 0, 1,
  12345) and at source level. Wall-clock lives in a separate timing file.
- Stages: `selftest`, `dev` (≤ 40 instances, label DEVELOPMENT, never
  protected), `protected`, `analyze`.
- The `protected` stage **refuses (exit 3)** unless
  `PROTECTED_RUN_AUTHORIZATION.json` (human_written = true, a human-written
  token ≥ 16 chars, and `acknowledged_design_sha256` = sha256 of the frozen
  design JSON) is present next to the runner **and** the custody seed hashes to
  the commitment. The file is absent in this PR; the tests assert its absence
  and the refusal path.
- Outputs: `results/FG70_<LABEL>_RESULTS_V1.json` (arm outputs only),
  `…_EXPECTED_CUSTODY_V1.json` (oracle verdicts + instances),
  `…_ANALYSIS_V1.json`, `…_TIMING_V1.json`, `FG70_SELFTEST_REPORT_V1.json`.
- Estimated protected cost: 168 instances × 18 arms ≈ 10 CPU-seconds on a laptop
  core. Run on the Mac (exact deterministic suite) or a LUNARC login node; never
  as a heavy job.

## 9. Non-goals, no-rescue clause, resolved ambiguities

No stratum weight, oracle rule, arm, seed, gate constant or count changes after
the protected results file exists. Development-only tuning surface: bug fixes to
arm glue validated by G0a before the seed is revealed. A protected result is
never re-run under a new seed; a lane defect found mid-run halts the lane, is
receipted, and re-freezes as V2. No field status, novelty or publication
authority.

Ambiguities resolved at design time:

1. **Information vs cost.** Every candidate repair, including the unobserved
   variable and the relational primitive, is *evaluable* by every arm. The suite
   therefore measures **repair-tier selection under full information**, not
   information acquisition: the question is which repair is cheapest and
   adequate, not which is discoverable. An arm cannot be credited for guessing
   that an unmeasured variable would help; nor penalised for not knowing.
2. **"Existing parent formalism" means *registered*.** A language that would
   resolve the deficit but is not in the instance's registered library is not a
   tier-1 option. Fixture KA-05 is built on exactly this point.
3. **`NEW_PRIMITIVE` is relational by construction.** The active language is
   attribute-based over individual cases; a relational primitive is not a
   function of any case's own observables at any grammar depth, which is what
   makes it a genuinely new primitive rather than a re-encoding. The generator
   verifies exhaustively that no attribute-based repair works before labelling an
   instance `NEW_PRIMITIVE`.
4. **M's exactness is not the finding.** M and the oracle are two
   implementations over the same registered ladder; their agreement is expected
   and is necessary, not sufficient. The findings are the false-invention
   behaviour under maximal temptation, the parent attribution table, and the 2×2
   mechanism factorial.
5. **`CANNOT_CHECK` is scored as an error but reported separately**, so a
   parent's honest refusal is never confused with a wrong answer.
