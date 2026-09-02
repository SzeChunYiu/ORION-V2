# FG70 — Formalism Needed or Not: Protected-Run Outcome Receipt (V1)

**Series:** `ORION-FG-L5-EXACT-V1`, the L5 formalism-genesis layer of issue #50 §L5.

**Design:** `FG70_FORMALISM_NEEDED_OR_NOT_EXACT_STUDY_DESIGN_V1.{md,json}` (PR #181, main `39276fa`), design-JSON sha256 `64ae856df7853e9e4840628069608dc87eaf9ffbe9a49cbaeef96797c50d2e89`.

**Authorization:** operator, in chat, 2026-09-02, verbatim *"run all the computation tasks.. finish all the researxh asap"*, recorded as coordinator authorization in `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` (the file the runner consumed as `PROTECTED_RUN_AUTHORIZATION.json`, archived under a new name after the single run so the guard is re-armed; sha256 `d50a239f9906872d8da453b16c688217a7c27651e47334778264ff7bb07d23dc`; carries the design sha256, the seed commitment and all six code hashes).

**Run:** Mac (local), 2026-09-02, `python3 fg_run.py protected --out results`, **executed exactly once**, exit 0, **4.37 s wall** for 168 instances × 21 arms. The runner verified sha256(custody seed) = the frozen commitment `4b34cb8798a01c5a2223a50453b6491d3dcf10f12139c7a8a8144aa4f68355bb` before generating; `analyze` ran once inside the same invocation. Code byte-identical to main `39276fa` (`git diff origin/main -- research/experiments/fg/` empty at run time; all six code hashes re-verified against the fidelity receipt). **No post-outcome change to any design constant, gate, arm, oracle rule, count or seed.**

**Seed reveal (design §2.6):** `FG70-PROTECTED-280ec70813bff85e7471148abf3dd2fa1a1feb9f279f03b2` — sha256 equals the commitment above; the 168-instance split regenerates byte-for-byte from it, in any process (design §8 determinism invariant).

**Artifacts (sha256):** results `e458b31fb8109c37ede2ad62556dcf7410f8cdb012b901d02ff480eb6c98fcd2`; expected-custody `387c81545d1df723608d770c85d67fa29e9b6fd8a3577446a90a57fcaa9c7159`; analysis `d8825f5bd7446799ebc8ade45b2177bffdc00d1cbe183c689109101a9e109ce6`; timing `f341ba1e399f27466dca3dfd91ee98c40759b951c182a727020ca4c5748d6736`; selftest report (G0a source) `a47bcb7a78cab2a27d60b9a0b74ff4749be792003b339e176f0ea9e6afb0f958`.

**Not the fmfg-r2 campaign.** `research/experiments/fmfg-r2/` ran studies *named* `fg10`–`fg80` under owner issue #48 with language-model solver arms (1 712 tasks × 5 arms = 8 560 dispatches, terminal `REGISTERED_SCALE_NULL`). This study is a different object with the same label: deterministic, zero model calls, mechanism versus faithful parent federation. It shares no generator, oracle, arm or task with that campaign, does not replicate it and does not contradict it. Those receipts are frozen and untouched. See design §0.

## 1. Terminal

```text
FG70_STATUS             = EXECUTED_PROTECTED
ROUTE                   = PARENT_SUFFICIENT
CO_PRIMARY (anti-invention) = PASS -- M false-invention rate 0.000 over 140 eligible instances
PRIMARY_COMPARATOR      = B_STRONGEST_FAITHFUL_PARENT_FEDERATION
REGISTERED_PREDICTION   = P-FG70-1 CONFIRMED (see §5)
FIELD_STATUS_AUTHORITY  = NONE
```

**Repair-tier selection is parent-owned.** On 168 protected instances across all six terminals of the §L5 search order, the strongest faithful parent federation reproduces `M`'s terminal on **every instance** (identity 168/168, 0 discordant pairs, McNemar exact p = 1.0). Choosing the cheapest adequate repair is not a control residual of the formalism-genesis mechanism; it is what a federation of anti-unification, formal concept analysis, MDL abstraction, countermodel search, conservative-extension checking and AGM base revision already does once it is given the registered search order — which is public, being stated in the issue itself.

**The negative is the point, not a disappointment.** The suite's registered question was whether a system can tell "the language is too coarse" from "the problem is merely unsolved", and its critical metric was whether it invents a formalism when something cheaper would do. Both are answered, and neither answer required a residual.

## 2. Gates (frozen pre-outcome; all numbers from `results/FG70_PROTECTED_ANALYSIS_V1.json`)

| gate | verdict | numbers | instances evaluated |
|---|---|---|---|
| **G0a KNOWN_ANSWER** (hard) | **PASS** | 6/6 hand-authored fixtures, one per terminal, reproduced by the oracle, by M and by the federation | 6 |
| **G0b ORACLE_SELF_AGREEMENT** (hard) | **PASS** | method A (signature buckets + bitmask cover) = method B (set-partition meet) on terminal, collision set and feasible-tier vector; 0 violations | **168** |
| **G0c NULL_CALIBRATION** (hard) | **PASS** | random control 0.202 (rule ≤ 0.25, chance 1/6 = 0.167); M vs within-split shuffled labels 0.220 (rule ≤ 0.30); planted positives below | 168 |
| **G1a FEDERATION_REPRODUCES_M** | **PASS** | terminal identity **1.000** (rule ≥ 0.995); per-stratum discordance 0/28 in all six strata (rule ≤ 0.05) | 168 |
| **G1b M_ADVANTAGE** | not fired | paired diff 0.000, discordant 0/168, McNemar exact two-sided p = 1.0 | 168 |
| **G2 ANTI_CONSERVATISM** | **PASS** | M missed deficits 0 ≤ federation 0; planted positive `C_NEVER_CHANGE` **140/140** | **140** |
| **G2M ANTI_INVENTION** (co-primary, non-compensatory) | **PASS** | M false inventions **0**, rate 0.000 (rule ≤ 0.02) ≤ federation 0; no stratum with an empty denominator (28 each × 5) | **140** |
| **G3 MECHANISM_BY_OMISSION** | reported (G1b not fired) | every stratum's omission ablation collapses to 0/28 against M's 28/28 | 168 |

### 2.1 The planted positives — every no-alarm gate was shown to fire

| gate | planted positive | value | rule |
|---|---|---|---|
| G2M anti-invention | `C_ALWAYS_INVENT` false-invention rate | **0.80** (112/140) | ≥ 0.50 |
| G2M anti-invention | `M_MINUS_ORDER_AND_GATE` false-invention rate | **0.80** (112/140) | > 0 |
| G2 anti-conservatism | `C_NEVER_CHANGE` missed-deficit rate | **1.00** (140/140) | ≥ 0.50 |
| G0c | random control accuracy | 0.202 | ≤ 0.25 |
| G0c | M vs shuffled labels | 0.220 | ≤ 0.30 |

A zero in this receipt means *the counter ran and stayed at zero*, not *the counter never ran*. Both gate defects that would have made those zeros meaningless were found and repaired **before** the freeze and are recorded in `FG_PARENT_FIDELITY_RECEIPT_V1.md` §5.1: G2 could not fire at all (every arm's first move is the shared collision check, so under-detection is structurally unreachable and the gate would have reported `PASS` on `0 ≤ 0` over a denominator of 140), and G3's per-stratum rule was unsatisfiable on three of six strata (a fail-closed admission gate can only ever *block*, so removing it cannot degrade the stratum where invention is correct).

## 3. Per-arm outcomes (168 instances; design §4)

Denominators: false invention over the **140** instances whose truth is cheaper than `NEW_PRIMITIVE`; missed deficit over the **140** whose truth is not `NO_CHANGE`.

| arm | accuracy | false inventions (/140) | missed deficits (/140) | over-esc. | under-esc. | `CANNOT_CHECK` |
|---|---|---|---|---|---|---|
| `P1_LGG_ANTIUNIFICATION` | 0.524 | 14 | 0 | 56 | 0 | 24 |
| `P2_FCA_GALOIS_CLOSURE` | 0.833 | 14 | 0 | 28 | 0 | 0 |
| `P3_MDL_ABSTRACTION_SEARCH` | 0.702 | 0 | 0 | 22 | 28 | 0 |
| `P4_MODEL_COUNTERMODEL_SEARCH` | 0.667 | 43 | 0 | 56 | 0 | 0 |
| `P5_CONSERVATIVE_EXTENSION_CHECK` | 0.333 | 14 | 0 | 14 | 0 | 98 |
| `P6_THEORY_REVISION_BASELINE` | 0.333 | 0 | 0 | 18 | 0 | 94 |
| **`B_STRONGEST_FAITHFUL_PARENT_FEDERATION`** | 1.000 | 0 | 0 | 0 | 0 | 0 |
| **`M_FG_SEARCH_ORDER`** | 1.000 | 0 | 0 | 0 | 0 | 0 |
| `M_MINUS_PARENT_SEARCH` | 0.833 | 0 | 0 | 28 | 0 | 0 |
| `M_MINUS_DATA_TIER` | 0.833 | 7 | 0 | 28 | 0 | 0 |
| `M_MINUS_PATCH_TIER` | 0.833 | 14 | 0 | 28 | 0 | 0 |
| `M_MINUS_REPRESENTATION_TIER` | 0.833 | 28 | 0 | 28 | 0 | 0 |
| `M_MINUS_INVENTION_TIER` | 0.833 | 0 | 0 | 0 | 0 | 28 |
| `M_MINUS_DEFICIT_CHECK` | 0.833 | 0 | 0 | 28 | 0 | 0 |
| `M_MINUS_ADMISSION_GATE` | 1.000 | 0 | 0 | 0 | 0 | 0 |
| `M_MINUS_COST_ORDER` | 0.625 | 0 | 0 | 63 | 0 | 0 |
| `M_MINUS_ORDER_AND_GATE` | 0.333 | 112 | 0 | 112 | 0 | 0 |
| `M_EAGER_INVENT` | 0.500 | 26 | 0 | 84 | 0 | 0 |
| `C_ALWAYS_INVENT` | 0.333 | 112 | 0 | 112 | 0 | 0 |
| `C_NEVER_INVENT` | 0.833 | 0 | 0 | 0 | 28 | 0 |
| `C_NEVER_CHANGE` | 0.167 | 0 | 140 | 0 | 140 | 0 |
| `C_RANDOM_TERMINAL` | 0.202 | 24 | 20 | 71 | 63 | 0 |

### 3.1 Per-stratum accuracy (correct / 28 per cell)

| arm | NO_CHANGE | PARENT | ADD_ONE_OBS | LOCAL_PATCH | REPRESENTATION | NEW_PRIMITIVE |
|---|---|---|---|---|---|---|
| `P1_LGG_ANTIUNIFICATION` | 4 | 0 | 28 | 0 | 28 | 28 |
| `P2_FCA_GALOIS_CLOSURE` | 28 | 28 | 28 | 0 | 28 | 28 |
| `P3_MDL_ABSTRACTION_SEARCH` | 28 | 28 | 16 | 18 | 28 | 0 |
| `P4_MODEL_COUNTERMODEL_SEARCH` | 28 | 0 | 28 | 28 | 0 | 28 |
| `P5_CONSERVATIVE_EXTENSION_CHECK` | 28 | 0 | 0 | 0 | 0 | 28 |
| `P6_THEORY_REVISION_BASELINE` | 28 | 0 | 0 | 28 | 0 | 0 |
| **`B_STRONGEST_FAITHFUL_PARENT_FEDERATION`** | 28 | 28 | 28 | 28 | 28 | 28 |
| **`M_FG_SEARCH_ORDER`** | 28 | 28 | 28 | 28 | 28 | 28 |
| `M_MINUS_PARENT_SEARCH` | 28 | 0 | 28 | 28 | 28 | 28 |
| `M_MINUS_DATA_TIER` | 28 | 28 | 0 | 28 | 28 | 28 |
| `M_MINUS_PATCH_TIER` | 28 | 28 | 28 | 0 | 28 | 28 |
| `M_MINUS_REPRESENTATION_TIER` | 28 | 28 | 28 | 28 | 0 | 28 |
| `M_MINUS_INVENTION_TIER` | 28 | 28 | 28 | 28 | 28 | 0 |
| `M_MINUS_DEFICIT_CHECK` | 0 | 28 | 28 | 28 | 28 | 28 |
| `M_MINUS_ADMISSION_GATE` | 28 | 28 | 28 | 28 | 28 | 28 |
| `M_MINUS_COST_ORDER` | 28 | 0 | 7 | 14 | 28 | 28 |
| `M_MINUS_ORDER_AND_GATE` | 28 | 0 | 0 | 0 | 0 | 28 |
| `M_EAGER_INVENT` | 28 | 0 | 0 | 0 | 28 | 28 |
| `C_ALWAYS_INVENT` | 28 | 0 | 0 | 0 | 0 | 28 |
| `C_NEVER_INVENT` | 28 | 28 | 28 | 28 | 28 | 0 |
| `C_NEVER_CHANGE` | 28 | 0 | 0 | 0 | 0 | 0 |
| `C_RANDOM_TERMINAL` | 4 | 10 | 3 | 6 | 7 | 4 |

## 4. Mechanism by omission

| stratum | ablation | M | ablation |
|---|---|---|---|
| `NO_CHANGE` | `M_MINUS_DEFICIT_CHECK` | 28/28 | 0/28 |
| `PARENT_FORMALISM_SUFFICIENT` | `M_MINUS_PARENT_SEARCH` | 28/28 | 0/28 |
| `ADD_ONE_OBSERVATION` | `M_MINUS_DATA_TIER` | 28/28 | 0/28 |
| `LOCAL_PATCH` | `M_MINUS_PATCH_TIER` | 28/28 | 0/28 |
| `REPRESENTATION_CHANGE` | `M_MINUS_REPRESENTATION_TIER` | 28/28 | 0/28 |
| `NEW_PRIMITIVE` | `M_MINUS_INVENTION_TIER` | 28/28 | 0/28 |

Every stratum's tier-omission ablation collapses to **0/28**, and no ablation damages any stratum but its own. The ladder is therefore not decorative: each rung is load-bearing for exactly the cases it is registered to handle.

### 4.1 The 2×2 anti-invention factorial

| cost order | admission gate | arm | accuracy | false inventions (/140) |
|---|---|---|---|---|
| registered | on | `M_FG_SEARCH_ORDER` | 1.000 | **0** |
| registered | off | `M_MINUS_ADMISSION_GATE` | 1.000 | **0** |
| reversed | on | `M_MINUS_COST_ORDER` | 0.625 | **0** |
| reversed | off | `M_MINUS_ORDER_AND_GATE` | 0.333 | **112** |

The development result replicates exactly at protected scale. **Either guard alone suffices; removing both produces false invention on 112 of the 140 eligible instances (0.80).** With the registered order and no admission gate, M is still perfect. With the admission gate and a reversed order, M never invents but its accuracy falls to 0.625 — it stops escalating at the wrong rung instead (63 over-escalations), which is a cheaper failure than inventing.

## 5. The registered prediction P-FG70-1 — confirmed on both halves

Registered in `FG_PARENT_FIDELITY_RECEIPT_V1.md` §5.2 **before** this run, from an n = 36 development observation:

> `P4_MODEL_COUNTERMODEL_SEARCH` will have the highest false-invention count of any non-control arm, and `P3_MDL_ABSTRACTION_SEARCH` will have a false-invention count of 0 together with the lowest accuracy of any parent on the `NEW_PRIMITIVE` stratum.

**Both halves hold at n = 168.**

- `P4_MODEL_COUNTERMODEL_SEARCH`: **43 false inventions**, the highest of any non-control arm (next highest is an ablation, `M_MINUS_REPRESENTATION_TIER` at 28; the next parent is 14). Its inventions fall exactly where its alphabetical scan reaches `NEW_PRIMITIVE` first: **28/28 on `REPRESENTATION_CHANGE`** (`NEW_PRIMITIVE` < `REPRESENTATION_CHANGE`) and **15/28 on `PARENT_FORMALISM_SUFFICIENT`** (`NEW_PRIMITIVE` < `PARENT_FORMALISM_SUFFICIENT`), and nowhere else — it never invents on `ADD_ONE_OBSERVATION` or `LOCAL_PATCH`, both of which precede `NEW_PRIMITIVE` alphabetically. The pattern is a property of the scan order, not of the instances.
- `P3_MDL_ABSTRACTION_SEARCH`: **0 false inventions** and **0/28 on `NEW_PRIMITIVE`**, the floor. One honest qualification the development split did not show: `P6_THEORY_REVISION_BASELINE` also scores 0/28 there and also never invents, so P3 *ties* for the lowest rather than holding it alone. The two get there differently and the difference matters — P6 refuses (94 `CANNOT_CHECK`, it cannot extend a language at all) while P3 answers on every instance and still never invents.

**Reading, as registered:** what prevents false formalism invention is the **ordering** of the repair search, not the verification of the repair. `P4` verifies every candidate exactly by finite countermodel search and is nonetheless the worst inventor in the study, because it has no cost model and scans terminals in canonical alphabetical order, in which `NEW_PRIMITIVE` precedes `NO_CHANGE`, `PARENT_FORMALISM_SUFFICIENT` and `REPRESENTATION_CHANGE`. `P3` has a cost model and never invents, but prices a relational primitive by its whole extension (67 bits at n = 12) and is consequently blind to the 28 instances where invention is correct. Neither is a failure of verification; both are failures of ordering, in opposite directions. The registered §L5 search order is precisely an ordering prescription, and §4.1 shows it is sufficient on its own.

This is the suite's substantive finding, and it survives the `PARENT_SUFFICIENT` terminal: the federation reproduces M because it was *given* the order, not because ordering does not matter.

## 6. Kill conditions (protocol) — status

| condition | outcome |
|---|---|
| the strongest existing parent resolves the deficit | **yes, on every instance** — the federation is terminal-identical to M at equal cost (4.37 s for 168 × 21 arms) |
| one local variable or patch resolves the deficit at lower cost | this is the study's own ladder; M and the federation both select it correctly wherever it is true (28/28 on `ADD_ONE_OBSERVATION`, 28/28 on `LOCAL_PATCH`) |
| candidate lacks a semantics/model witness | not reached: M's `assess_formalism_candidate` admission gate was never the binding constraint (§4.1, `M_MINUS_ADMISSION_GATE` = 1.000) |
| candidate overgenerates registered countermodels | not observed: M false inventions 0/140 |
| candidate improves only notation aesthetics | not reached |

## 7. Programme consequence

`FG70_STATUS = PARENT_SUFFICIENT`. The routing decision "is the active language too coarse, or is the problem merely unsolved" contracts from a candidate control residual to an **ordering convention over faithful parents** — the registered §L5 search order, applied to parent-owned machinery. Two things survive that contraction and are worth carrying:

1. **The ordering is the mechanism.** §5 shows exact verification without an order is the worst false-inventor in the study, and §4.1 shows the order alone is sufficient. That is a claim about how to avoid false formalism invention, not about ORION's control layer.
2. **False formalism invention is measurable and the measurement is not trivial.** On 112 of 168 instances a new primitive was registered, available, and adequate; refusing it there is what the metric scores. An arm that invents in this suite is never wrong because the primitive failed.

The remaining FG suites (FG10–FG60, FG80) are unaffected: none of them reads an FG70 outcome, and the ordering deviation is recorded in the design §7 and the backlog. No field status, novelty, adoption or publication authority is granted or implied; the analysis JSON's authority block is false in every field.

## 8. Custody

`results/FG70_PROTECTED_*` and `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` are archived in this PR, force-added past the `.gitignore` that guards against unauthorized commits. The live path `PROTECTED_RUN_AUTHORIZATION.json` is absent again, verified: `fg_run.py protected` was re-invoked after archiving and exited **3** with `REFUSED`. A second protected run would require a new, explicit authorization. The custody seed file remains in operator custody at `~/.orion-custody/fg/PROTECTED_SEED_V1.txt` (mode 600); its value is now public above, and the split is reproducible by anyone from the frozen code on `39276fa` in any process.

skills-applied: none (results receipt, no manuscript content)
