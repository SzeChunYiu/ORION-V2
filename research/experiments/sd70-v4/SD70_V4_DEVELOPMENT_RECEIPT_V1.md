# SD70-V4 — development parent-ceiling receipt (exact, LUNARC job 3579607, 2026-09-05)

```text
SD70_V4_DEV_STATUS  = EXECUTED (development split, public seeds; no protected task exists)
TERMINAL (dev)      = PARENT_CEILING_INFORMATION_BOUND   (pre-registered branch (c) of the frozen design)
FAMILY              = XOR_GATED_TWO_REGIME, certified outside the linear multiclass class on 600/600 tasks (min 1, mean 5.5, max 29 certificates; 202 rejections)
PARENT CEILING      = F0_PARENT_FEDERATION 0.4817 [0.442, 0.522]  (chance 0.260)   -- the comparator any model arm must beat
CHANGES_SD70_V3     = NONE     GRANTS = nothing
```

**Design (frozen before this run):** `SD70_V4_GATED_FAMILY_DESIGN_V1.json` sha256 `31281475532a1ea0f46bf8396e4ee03f37254114279fbce61ffbd1ee121a36ce` (PR #339; pins re-frozen pre-dev
after the V4-native query-shuffle control, supersession note in the JSON). **Run:** LUNARC `lu48` job **3579607**, clone `65e184c`, `.venv` CPython 3.13.5, 11 min;
selftest PASS in the same job (V3's linear family 0 certificates on 80/80 tasks; planted label-ignoring mutant caught; gated-parent fidelity on the planted surface).
**Results:** `results/SD70_V4_DEVELOPMENT_RESULTS_V1.json` sha256 `13967ddd70319a05f8fbfa8666531b005825735ac42133853086a36c6b3b7471`; transfer LUNARC → billy-old → Mac, md5 `88883551…` both ends.

## 1. The parent ceiling on the certified family (3 × 200 tasks, 16 episodes each)

| parent | exact accuracy | Wilson 95 % | critical false direction | LP / QS control |
|---|---:|---|---:|---|
| `DECISION_LIST_PARENT` | 0.4617 | [0.422, 0.502] | 0.180 | 0.257 / 0.240 |
| `F0_PARENT_FEDERATION` | 0.4817 | [0.442, 0.522] | 0.157 | nan / nan |
| `F0_PLUS_FEDERATION` | 0.4800 | [0.440, 0.520] | 0.152 | nan / nan |
| `GATED_MAXMARGIN_PARENT` | 0.4633 | [0.424, 0.503] | 0.148 | 0.255 / 0.247 |
| `MATCHED_CASE_PARENT` | 0.4283 | [0.389, 0.468] | 0.192 | 0.237 / 0.250 |
| `MAXMARGIN_PARENT` | 0.4700 | [0.430, 0.510] | 0.170 | 0.267 / 0.267 |
| `NAIVE_BAYES_PARENT` | 0.4483 | [0.409, 0.488] | 0.173 | 0.242 / 0.250 |
| `PAIRWISE_LINEAR_PARENT` | 0.4650 | [0.425, 0.505] | 0.177 | 0.262 / 0.268 |
| `PERCEPTRON_PARENT` | 0.4617 | [0.422, 0.502] | 0.162 | 0.275 / 0.277 |
| `SIMPLE_FREQUENCY_PARENT` | 0.3917 | [0.353, 0.431] | 0.207 | 0.257 / 0.262 |

Strongest generator-faithful parent by the frozen rule: **`MAXMARGIN_PARENT`** (0.4700); strongest linear parent the same. Comparator by the frozen rule:
**`F0_PARENT_FEDERATION` 0.4817** (> `F0_PLUS` 0.4800 > MAXMARGIN). Every control sits at chance (0.24–0.28 against 0.260).

## 2. Pre-registered expectations, read one by one

| | expectation | outcome |
|---|---|---|
| (a) | every task ≥ 1 certificate | **held** — 600/600, rejections published (202) |
| (b) | linear parents below their V3 dev accuracies (MAXMARGIN 0.678 on the linear family) | **held** — MAXMARGIN 0.470, every linear parent 0.39–0.47: the family is outside their class and it shows |
| (c) | GATED beats the strongest linear parent, else `PARENT_CEILING_INFORMATION_BOUND` | **not held** — gated − linear = -0.0067 [-0.052, +0.040], b = 98, c = 102: the family-aware parent cannot identify the gate from 8 training contexts (21 candidate pairs, two regimes of ≤ 4 contexts each). Terminal branch **`PARENT_CEILING_INFORMATION_BOUND`** |
| (d) | F0_PLUS ≥ F0 | **not held**, within noise (0.4800 vs 0.4817); adding an information-bound member does not help the plurality |
| (e) | controls at chance | **held** |

## 3. What this establishes for R12, at its strength

- **The lever moved the problem class.** On V3's family the parent ceiling was 0.678 and contained the truth by construction; on the certified
  gated family the best registered parent — including the one that knows the family's form — reaches 0.48 against chance 0.26. About half the
  protected population is out of reach of every registered parent at the 16-episode budget. That is the room a recursive meta-discovery arm
  would need, and V3 had none.
- **The ceiling is information-bound, not class-bound.** The gated parent's failure to beat max-margin is the registered reading (c): at this
  budget the gate is not identifiable, so *no* parent in the family's own class benefits from knowing the form. A model arm that beats
  F0 here would be doing something the parents cannot do *from the same 16 episodes* — which is exactly the claim SD70 was built to test and
  could not test on a family the parents already solve. It also means a model-arm residual, if one appears, is a residual against an
  information-bound ceiling, and the design's mechanism gate (F2 − F2_STATIC ≥ 0.05) is what separates discovery from a better prior.
- **Nothing about the model arms is known.** They are `FROZEN_PENDING_CHANNEL`; the comparator they must beat is frozen by this receipt
  (`F0_PARENT_FEDERATION`, 0.4817 on dev), and the protected seed is committed and unrevealed.

Authority: grants nothing; SD70-V3's `PARENT_SUFFICIENT` stands. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

skills-applied: none (development receipt, no manuscript content)
