# FG Series — Parent Fidelity, Code Custody and Development-Split Receipt V1

**Series:** `ORION-FG-L5-EXACT-V1` (owner issue #50 §L5). **Suite covered by this
revision:** FG70. This receipt is extended in place as FG10–FG60 and FG80 land;
parents are shared across the series and are registered once here.

**Not the fmfg-r2 campaign.** `research/experiments/fmfg-r2/` ran studies named
`fg10`–`fg80` under owner issue #48 with language-model solver arms (1 712 tasks
× 5 arms = 8 560 dispatches, terminal `REGISTERED_SCALE_NULL`). This series is
deterministic, calls no model, and shares no generator, oracle, arm or task with
it. Those receipts are frozen and are not modified by this lane. See the FG70
design §0.

## 1. Code custody (sha256, as merged)

| file | sha256 |
|---|---|
| `fg_model.py` | `ccb6e451255a569b8bd50333929a65fed50ed21e0f1ad50fd75cf6ea4d2684b7` |
| `fg_oracle.py` | `4208bece29735019d2cd4e3a5add6af412302cba32eea61f087b7e4d4269c20a` |
| `fg70_generator.py` | `ea4db4f47b81e67915138984c1f35be7ca01c842b030e1ef6fc6b8de694c4083` |
| `fg_parents.py` | `5e056922cdfd8e0ff8340ec7c507227f9a3a5a949f169b87811ecdf77ce34255` |
| `fg_arms.py` | `9d82d9e8105b5ddacb163ea67cdc9477da72006d7fce2ad660ccc06a155a845d` |
| `fg_run.py` | `db996e36db643807a6e283315d53b6b8515a121246efe051252141da4a38754e` |
| `FG70_FORMALISM_NEEDED_OR_NOT_EXACT_STUDY_DESIGN_V1.json` | `64ae856df7853e9e4840628069608dc87eaf9ffbe9a49cbaeef96797c50d2e89` |

Protected seed commitment (design §2.6):
`4b34cb8798a01c5a2223a50453b6491d3dcf10f12139c7a8a8144aa4f68355bb`
(`~/.orion-custody/fg/PROTECTED_SEED_V1.txt`, mode 600, value not disclosed until
the outcome receipt). `PROTECTED_RUN_AUTHORIZATION.json` is **absent**;
`fg_run.py protected` exits 3 and a test asserts it.

**Determinism.** The split and every arm output reproduce byte-for-byte across
processes under `PYTHONHASHSEED` 0, 1 and 12345 (asserted in
`tests/unit/test_fg70_exact_study.py`). This was not free: the first
implementation of the generator drew RNG values while iterating an unordered
`set` of signatures in three planters, so the "same" split regenerated
differently in a different process. The defect was found by cross-process
hashing before any protected artifact existed, fixed at the root (every set that
drives an RNG draw is sorted first), and is now guarded by both a behavioural
test and a source-level test.

## 2. Parent fidelity — 42/42 native known-answer checks pass

Every parent is implemented to its own published semantics and tested against
its *own* literature examples before it may be used as a comparator
(`fg_parents.fidelity_selftests`). A parent that could not be implemented
faithfully would be `CANNOT_CHECK`, never a strawman.

| parent | checks | what is checked |
|---|---|---|
| `LGG` (Plotkin 1970) | 9/9 | classic pair lgg `f(a,b,a) ⊓ f(a,c,a) = f(a,?,a)`; identity on equal tuples; all-variable lgg on disjoint tuples; lgg of a set = iterated pair lgg; lgg subsumes every input; θ-subsumption rejects a constant mismatch; **exhaustive** least-generality check over the full pattern space; arity mismatch and empty-set errors raise |
| `FCA` (Ganter & Wille) | 12/12 | object intent and attribute extent on the classic living-beings context; derivation of the empty object/attribute set; closure extensive, idempotent and monotone (four ordered pairs); every concept is a fixed point of the derivation pair; top and bottom concepts present; `milk → limbs` holds and `limbs → milk` does not; **the Galois adjunction `A ⊆ B′ ⟺ B ⊆ A′` is certified `SATISFIED` by `orion_v2.meta_formalization.assess_galois_connection`** over the full power-set posets |
| `MDL` | 7/7 | `NO_CHANGE` costs nothing; a parent costs only its name; a new primitive costs its whole extension (66 + 1 bits at n = 12); residual collisions dominate any model term; the code is monotone in residuals; patch cost grows with patch size; **and the code's native order differs from the registered order** — MDL prices a derived term below a two-case patch, which the registered §L5 order reverses. The disagreement is reported, not repaired: a parent whose ordering were copied from M would not be an independent parent |
| `MODEL_SEARCH` | 4/4 | first countermodel to `a → J`; no countermodel to `ab → J`; empty determiner set finds the first disagreement; constant target has no countermodel |
| `CONSERVATIVE` | 5/5 | conservative, non-conservative and lost-consequence cases through `orion_v2.meta_formalization.assess_conservative_extension`; shrinking language yields `CANNOT_CHECK`; the check is non-authorizing |
| `THEORY_REVISION` | 5/5 | Hansson kernel contraction removes one element per kernel; inclusion; vacuity; two kernels give two incisions; an empty kernel is ignored |

Two of these parents are ORION reference modules reused rather than rebuilt, as
the design requires ("the federation is never artificially isolated"):
`assess_galois_connection` and `assess_conservative_extension`.

## 3. Development split (public seed `FG70-DEV-20260902`, 36 instances)

**This is development evidence. It is not protected and carries no verdict.**
Route on development: `PARENT_SUFFICIENT`; gates G0b, G0c, G1a, G2, G2M PASS,
G1b NOT_FIRED, G3 REPORTED.

| arm | accuracy | false inventions (/30) | missed deficits (/30) | over-esc. | under-esc. | `CANNOT_CHECK` |
|---|---|---|---|---|---|---|
| `P1_LGG_ANTIUNIFICATION` | 0.528 | 4 | 0 | 12 | 0 | 5 |
| `P2_FCA_GALOIS_CLOSURE` | 0.833 | 4 | 0 | 6 | 0 | 0 |
| `P3_MDL_ABSTRACTION_SEARCH` | 0.778 | 0 | 0 | 2 | 6 | 0 |
| `P4_MODEL_COUNTERMODEL_SEARCH` | 0.667 | 8 | 0 | 12 | 0 | 0 |
| `P5_CONSERVATIVE_EXTENSION_CHECK` | 0.333 | 4 | 0 | 4 | 0 | 20 |
| `P6_THEORY_REVISION_BASELINE` | 0.333 | 0 | 0 | 2 | 0 | 22 |
| **`B_STRONGEST_FAITHFUL_PARENT_FEDERATION`** | 1.000 | 0 | 0 | 0 | 0 | 0 |
| **`M_FG_SEARCH_ORDER`** | 1.000 | 0 | 0 | 0 | 0 | 0 |
| `M_MINUS_PARENT_SEARCH` | 0.833 | 0 | 0 | 6 | 0 | 0 |
| `M_MINUS_DATA_TIER` | 0.833 | 5 | 0 | 6 | 0 | 0 |
| `M_MINUS_PATCH_TIER` | 0.833 | 4 | 0 | 6 | 0 | 0 |
| `M_MINUS_REPRESENTATION_TIER` | 0.833 | 6 | 0 | 6 | 0 | 0 |
| `M_MINUS_INVENTION_TIER` | 0.833 | 0 | 0 | 0 | 0 | 6 |
| `M_MINUS_DEFICIT_CHECK` | 0.833 | 0 | 0 | 6 | 0 | 0 |
| `M_MINUS_ADMISSION_GATE` | 1.000 | 0 | 0 | 0 | 0 | 0 |
| `M_MINUS_COST_ORDER` | 0.750 | 0 | 0 | 9 | 0 | 0 |
| `M_MINUS_ORDER_AND_GATE` | 0.333 | 24 | 0 | 24 | 0 | 0 |
| `M_EAGER_INVENT` | 0.500 | 9 | 0 | 18 | 0 | 0 |
| `C_ALWAYS_INVENT` | 0.333 | 24 | 0 | 24 | 0 | 0 |
| `C_NEVER_INVENT` | 0.833 | 0 | 0 | 0 | 6 | 0 |
| `C_NEVER_CHANGE` | 0.167 | 0 | 30 | 0 | 30 | 0 |
| `C_RANDOM_TERMINAL` | 0.111 | 7 | 3 | 19 | 13 | 0 |

### 3.1 Per-stratum accuracy (correct / 6 per cell)

| arm | NO_CHANGE | PARENT | ADD_ONE_OBS | LOCAL_PATCH | REPRESENTATION | NEW_PRIMITIVE |
|---|---|---|---|---|---|---|
| `P1_LGG_ANTIUNIFICATION` | 1 | 0 | 6 | 0 | 6 | 6 |
| `P2_FCA_GALOIS_CLOSURE` | 6 | 6 | 6 | 0 | 6 | 6 |
| `P3_MDL_ABSTRACTION_SEARCH` | 6 | 6 | 5 | 5 | 6 | 0 |
| `P4_MODEL_COUNTERMODEL_SEARCH` | 6 | 0 | 6 | 6 | 0 | 6 |
| `P5_CONSERVATIVE_EXTENSION_CHECK` | 6 | 0 | 0 | 0 | 0 | 6 |
| `P6_THEORY_REVISION_BASELINE` | 6 | 0 | 0 | 6 | 0 | 0 |
| **`B_STRONGEST_FAITHFUL_PARENT_FEDERATION`** | 6 | 6 | 6 | 6 | 6 | 6 |
| **`M_FG_SEARCH_ORDER`** | 6 | 6 | 6 | 6 | 6 | 6 |
| `M_MINUS_PARENT_SEARCH` | 6 | 0 | 6 | 6 | 6 | 6 |
| `M_MINUS_DATA_TIER` | 6 | 6 | 0 | 6 | 6 | 6 |
| `M_MINUS_PATCH_TIER` | 6 | 6 | 6 | 0 | 6 | 6 |
| `M_MINUS_REPRESENTATION_TIER` | 6 | 6 | 6 | 6 | 0 | 6 |
| `M_MINUS_INVENTION_TIER` | 6 | 6 | 6 | 6 | 6 | 0 |
| `M_MINUS_DEFICIT_CHECK` | 0 | 6 | 6 | 6 | 6 | 6 |
| `M_MINUS_ADMISSION_GATE` | 6 | 6 | 6 | 6 | 6 | 6 |
| `M_MINUS_COST_ORDER` | 6 | 0 | 5 | 4 | 6 | 6 |
| `M_MINUS_ORDER_AND_GATE` | 6 | 0 | 0 | 0 | 0 | 6 |
| `M_EAGER_INVENT` | 6 | 0 | 0 | 0 | 6 | 6 |
| `C_ALWAYS_INVENT` | 6 | 0 | 0 | 0 | 0 | 6 |
| `C_NEVER_INVENT` | 6 | 6 | 6 | 6 | 6 | 0 |
| `C_NEVER_CHANGE` | 6 | 0 | 0 | 0 | 0 | 0 |
| `C_RANDOM_TERMINAL` | 0 | 1 | 1 | 0 | 1 | 1 |

### 3.2 Where the single parents break, in their own terms

- **`P1_LGG_ANTIUNIFICATION` — 1/6 on NO_CHANGE.** Its native deficit test is
  cross-subsumption of class generalizations, which is strictly coarser than the
  collision set: on 5 of 6 collision-free instances a class lgg subsumes a
  foreign case although no case pair collides, and the arm returns
  `CANNOT_CHECK` rather than inventing. It scores 0/6 on PARENT and LOCAL_PATCH
  because argument-position extension cannot express either tier; 4 of its 6
  LOCAL_PATCH escalations reach `NEW_PRIMITIVE`.
- **`P2_FCA_GALOIS_CLOSURE` — 0/6 on LOCAL_PATCH only.** FCA compares attribute
  sets exactly and therefore matches M on every other stratum; it has no
  exception mechanism at all, so it escalates past the patch, and 4 of those 6
  escalations reach `NEW_PRIMITIVE`.
- **`P3_MDL_ABSTRACTION_SEARCH` — 0/6 on NEW_PRIMITIVE, zero false
  inventions.** Its native code prices a relational primitive by its whole
  extension (67 bits at n = 12), above every alternative, so it never invents —
  the mirror-image failure: perfect anti-invention bought with total blindness
  to genuine invention need (6 under-escalations). Its other two misses are one
  ADD_ONE_OBSERVATION and one LOCAL_PATCH instance, where the fixed 6-bit
  acquisition term and the per-exception code make a derived definition cheaper.
- **`P4_MODEL_COUNTERMODEL_SEARCH` — 8 false inventions, the worst of any
  non-control arm.** It has no cost model, so it scans terminals in canonical
  alphabetical order, in which `NEW_PRIMITIVE` precedes `NO_CHANGE`,
  `PARENT_FORMALISM_SUFFICIENT` and `REPRESENTATION_CHANGE`: it invents on all 6
  REPRESENTATION_CHANGE instances and 2 of 6 PARENT instances. This is the
  clearest single-parent demonstration that the *ordering*, not the
  verification, is what prevents false invention.
- **`P5_CONSERVATIVE_EXTENSION_CHECK` — 20/36 `CANNOT_CHECK`.** Conservative-
  extension checking is an admission filter, not a selector: whenever more than
  one repair is admissible it refuses. It is correct exactly where the
  admissible set is a singleton (NO_CHANGE, NEW_PRIMITIVE).
- **`P6_THEORY_REVISION_BASELINE` — 22/36 `CANNOT_CHECK`, zero false
  inventions.** AGM base revision cannot extend a language; it is exact on
  LOCAL_PATCH and NO_CHANGE and refuses everywhere else rather than escalating.

### 3.3 Mechanism by omission — every stratum has a degrading ablation

| stratum | ablation | M | ablation |
|---|---|---|---|
| `NO_CHANGE` | `M_MINUS_DEFICIT_CHECK` | 6/6 | 0/6 |
| `PARENT_FORMALISM_SUFFICIENT` | `M_MINUS_PARENT_SEARCH` | 6/6 | 0/6 |
| `ADD_ONE_OBSERVATION` | `M_MINUS_DATA_TIER` | 6/6 | 0/6 |
| `LOCAL_PATCH` | `M_MINUS_PATCH_TIER` | 6/6 | 0/6 |
| `REPRESENTATION_CHANGE` | `M_MINUS_REPRESENTATION_TIER` | 6/6 | 0/6 |
| `NEW_PRIMITIVE` | `M_MINUS_INVENTION_TIER` | 6/6 | 0/6 |

Each ablation fails exactly the stratum whose mechanism it omits and no other.
`NEW_PRIMITIVE` is attributed to `M_MINUS_INVENTION_TIER` — like-for-like with
the other five — rather than to `M_MINUS_ADMISSION_GATE`: the fail-closed
admission gate can only ever *block*, so removing it cannot degrade the stratum
where invention is correct, and a rule that mapped it there would be
unsatisfiable by construction. The gate's own
mechanism is measured on the anti-invention axis instead:

## 4. The 2×2 mechanism factorial (development)

| cost order | admission gate | arm | accuracy | false inventions (/30) |
|---|---|---|---|---|
| registered | on | `M_FG_SEARCH_ORDER` | 1.000 | **0** |
| registered | off | `M_MINUS_ADMISSION_GATE` | 1.000 | **0** |
| reversed | on | `M_MINUS_COST_ORDER` | 0.750 | **0** |
| reversed | off | `M_MINUS_ORDER_AND_GATE` | 0.333 | **24** |

Neither mechanism is necessary on its own; removing both produces invention harm
on 80% of the eligible instances, spread evenly across all four cheaper strata
(6/6 on each of PARENT, ADD_ONE_OBSERVATION, LOCAL_PATCH and
REPRESENTATION_CHANGE). On development this reads as **two independent
sufficient guards against false formalism invention** — the registered search
order, and the fail-closed admission gate whose
`minimality_or_simpler_patch_check` fails exactly when a cheaper adequate repair
exists. Whether it survives the protected split is the protected question.

## 5. Gates that had to be shown to fire

The recurring defect this receipt is written against: a gate reporting zero
violations because it never executed on the relevant cases. Every FG gate
reports `instances_evaluated` beside its violation count, and each no-alarm
assertion is paired with a planted positive:

| gate | planted positive | development value | rule |
|---|---|---|---|
| `G2M_ANTI_INVENTION` | `C_ALWAYS_INVENT` false-invention rate | 0.80 | ≥ 0.50 |
| `G2M_ANTI_INVENTION` | `M_MINUS_ORDER_AND_GATE` false-invention rate | 0.80 | > 0 |
| `G2_ANTI_CONSERVATISM` | `C_NEVER_CHANGE` missed-deficit rate | 1.00 | ≥ 0.50 |
| `G0c` | random control accuracy | 0.111 | ≤ 0.25 (chance 1/6 = 0.167) |
| `G0c` | M vs within-split shuffled labels | 0.139 | ≤ 0.30 |

`G2` needed this most. Every arm's first move is the shared collision check, so
under-detection is structurally hard to reach: **every arm except the random
control (3) and the planted `C_NEVER_CHANGE` control (30) scores 0 missed
deficits**, and without `C_NEVER_CHANGE` the gate would
report `PASS` on `0 ≤ 0` over a denominator of 140 with no evidence it can fire
at all. `C_NEVER_CHANGE` misses 30/30.

Two further selftest checks guard the denominators rather than the counters:

- `ANTI_INVENTION_DENOMINATOR_IS_NON_EMPTY_AND_TEMPTING` requires the eligible
  instances to carry a *working* new primitive, so a passing G2M means "refused
  an available and adequate escalation", not "no escalation was on offer".
- `EVERY_STRATUM_HAS_A_DEGRADING_OMISSION_ABLATION` requires G3's per-stratum
  rule to be satisfiable before it is scored.
- `G2M_ANTI_INVENTION` reports its per-stratum denominators and **hard-fails if
  any non-`NEW_PRIMITIVE` stratum has an empty denominator** (development:
  6/6/6/6/6, none empty; protected: 28 each, total 140).

## 6. Boundary

Development evidence only. No protected outcome exists. No field status,
novelty, adoption or publication authority is granted or implied; the analysis
JSON carries an authority block that is false in every field.

skills-applied: none (execution receipt, no manuscript content)
