# FM70 Extension — Routing Headroom on the Exact FM Suites

**Terminal: `NO_ROUTING_HEADROOM_PARENT_FEDERATION_ALREADY_OPTIMAL`.**

**Lane:** `FM70_CONTEXTUAL_REGIME_SELECTOR` (owner issue #48, §C1 of #50).
**Extends, does not restart:** `research/experiments/fm70/FM70_GATE0_TERMINAL_RECEIPT.md`
(2026-08-30, `INSUFFICIENT_ROUTING_SIGNAL_ON_DEVELOPMENT_FOLD`). That receipt
stands unchanged; nothing in it is reinterpreted.
**Driver:** `fm70_headroom.py` (this directory).
**Machine result:** `FM70_ROUTING_HEADROOM_RESULT_V1.json`.
**Inputs:** the two protected outcome matrices, `FM10_PROTECTED_RESULTS_V1.json`
(PR #179) and `FM20_PROTECTED_RESULTS_V1.json` — both frozen, both read-only here.

## 1. Why this is decidable without fitting anything

The gate-0 receipt asked whether a *fitted* selector could recover routing signal
from pre-outcome features, and found it could not on 40 BugsInPy tasks. The FM
suites did not exist then. Rather than refit a selector on them, this extension
answers the prior question, which is exact and model-free:

> Is there anything to route **to**?

A regime selector can only pay when there is **headroom** — instances where some
routable arm is correct while the best single always-arm is wrong:

```
ceiling      = instances on which at least one routable arm is correct
best_always  = max over arms of that arm's own correct count
headroom     = ceiling − best_always
```

If the headroom is zero then **no selector, however well fitted and however rich
its features, can beat the best always-arm.** That is a structural property of
the outcome matrix, not an empirical claim about a model class, so it needs no
held-out fold and admits no overfitting. It is also the cheap, pre-declared
branch: the gate-0 receipt already reported the analogous oracle ceiling (8/40 vs
6/40 always-best) as the quantity that bounds the lane.

## 2. Result

| suite | n | routing ceiling | best always-arm | headroom |
|---|---|---|---|---|
| FM10 | 126 | 126/126 | 126 (`F0_PARENT_FEDERATION`) | **0** |
| FM20 | 125 | 125/125 | 125 (`F0_PARENT_FEDERATION`) | **0** |

Per-arm always-policies (protected splits):

| FM10 arm | correct | | FM20 arm | correct |
|---|---|---|---|---|
| `F0_PARENT_FEDERATION` | 126/126 | | `F0_PARENT_FEDERATION` | 125/125 |
| `M_F2_TRANSFER_DISCOVERY_FULL` | 126/126 | | `M_F2_ABSTRACTION_INDUCTION_FULL` | 125/125 |
| `P2_COMPLETE_HOMOMORPHISM` | 108/126 | | `P2_CANDIDATE_ELIMINATION` | 100/125 |
| `P1_SME_STRUCTURE_MAPPING` | 104/126 | | `P0_FIXED_LESSON_INJECTION` | 100/125 |
| `P0_SURFACE_SIMILARITY` | 77/126 | | `P3_MDL_COMPRESSION` | 94/125 |
| `P3_FIXED_LESSON_INJECTION` | 54/126 | | `P1_PLOTKIN_LGG` | 75/125 |
| `P4_INVARIANCE_PARENT` | 54/126 | | | |

The always-best policy is already perfect on both suites, so the ceiling cannot
exceed it. **The routing question is closed on these benchmarks before any
selector is trained.**

## 3. Validating the statistic before believing it

A headroom computation that can only ever return zero would be worth nothing, so
the same function is run on the same protected matrices restricted to the
**single parents only**, where a nonzero answer is expected:

| suite | best single parent | ceiling over single parents | headroom |
|---|---|---|---|
| FM10 | 108/126 | 126/126 | **18** |
| FM20 | 100/125 | 125/125 | **25** |

The statistic reports 18 and 25 where headroom exists and 0 where it does not, in
the same execution as the verdict. The zeros in §2 are therefore measured zeros,
not a dead computation — the defect this programme keeps rediscovering, applied
here to its own diagnostic.

The 18 and 25 are also the substantive point restated: routing headroom over the
single parents is exactly the gap that the pre-registered **federation** closes.
Composition, not selection, is what recovers it.

## 4. The resource question, separately

FM70's protocol primary is a quality-resource Pareto frontier, so zero *quality*
headroom does not by itself close the cost side. Measured wall-clock on the
protected splits:

- **FM10:** `F0` 12.0 ms — the **cheapest** arm measured, and cheaper than `P2`
  alone (16.5 ms) because the federation short-circuits before consulting its
  second parent. `M` costs 37.7 ms.
- **FM20:** `F0` 3.04 ms vs `M` 2.96 ms — a tie; `P3_MDL_COMPRESSION` alone costs
  22.9 ms, an order of magnitude more than the federation.

So the federation is not a costly way of buying accuracy that a selector might
undercut: on these suites it is simultaneously the most accurate arm and among
the cheapest. A 27% wall-clock gap on a few milliseconds is within noise and
nothing is claimed from it beyond "no cost frontier to trade against here".

## 5. Scope and boundary inheritance

- The verdict covers **the exact FM suites with protected outcomes** (FM10,
  FM20). It is not a statement about routing in general, about the BugsInPy
  benchmark class, or about suites not yet executed. FM30–FM60 are not included;
  when their protected outcomes exist the same statistic should be recomputed,
  and if any of them shows nonzero headroom the fitted-selector question
  genuinely reopens for that suite.
- The boundary inherited from the gate-0 receipt and the E30 R11 terminal holds:
  **no critical-failure, safety or non-inferiority endpoint claims** may be made
  from FM70 outcomes, including from this negative. Routing claims are
  success-resource claims only.
- No field status, novelty, F2 superiority or publication authority is granted.

## 6. Disposition

`FM70_CONTEXTUAL_REGIME_SELECTOR` remains **terminal**. Its gate-0 vocabulary
(`INSUFFICIENT_ROUTING_SIGNAL_ON_DEVELOPMENT_FOLD`) is joined by
`NO_ROUTING_HEADROOM_PARENT_FEDERATION_ALREADY_OPTIMAL` on the exact suites: on
the benchmarks where the FM series does have protected outcomes, contextual
regime selection has nothing to contribute, because the pre-registered parent
federation is already optimal and already cheap.

skills-applied: none (lane receipt, no manuscript content)
