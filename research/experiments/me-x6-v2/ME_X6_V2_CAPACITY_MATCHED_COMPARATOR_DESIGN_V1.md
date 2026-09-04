# ME-X6 V2 — a LEARNED capacity-matched untyped comparator (frozen design V1)

**New run identity.** ME-X6 V1 is immutable. Nothing here re-runs it, re-fits its frozen
signs, or changes one of its gates, numbers, terminals or authorizations. V2 has its own
design digest, its own seed commitment, its own authorization and its own routed
terminals.

Frozen design: `ME_X6_V2_CAPACITY_MATCHED_COMPARATOR_DESIGN_V1.json`,
sha256 `ce7942af1d36092dc24c3ab310f80a0b836be4171d5e11a51bffe129772fa3d7`.
Protected seed commitment: sha256
`e117ba6a68c99e5a19eaf51602a416c7bf357707d23c27d6b8efbfe95831cb56`, published here
**before** the run; the seed value is revealed in the outcome receipt afterwards.

## 1. The question V1 could not answer

V1's terminal, as receipted, was
`UNTYPED_AGGREGATE_CANNOT_REPRESENT_THE_CONJUNCTION_AT_MATCHED_INFORMATION`. Its own
provenance receipt disproved that reading: the mechanism `M` and the comparator
`B4X_FITTED_UNTYPED` are **the same function** over the same channels differing only in a
weight dict, so loading M's weights into the untyped path reproduces M **56/56** (control
28/56). The terminal now carries the corrected reading `DOES_NOT_RECOVER`.

The single-stage cause was attributed: **the comparator cannot set a weight to zero.** Its
class is {−1, 0, +1} — with 0 reachable only through an exact tie in a per-channel tally —
while M's is {−2, −1, 0, +1} and zeroes eight channels. Restoring magnitudes alone
recovers one stratum (32/56); zeroing the six channels M weights at zero recovers all
seven (56/56). Information matching was genuine — both hold 16/16 channels — but
**capacity matching was not**.

**The distinction V2 exists to keep from collapsing:** V1 showed that a **hand-set**
zeroing recovers the conjunction. It did **not** show that a **learned** capacity-matched
parent ties M. V2 measures exactly that.

## 2. The comparator, named for what it is

`B8_CAPACITY_MATCHED_BEST` is **constructed for this study** and is **not a
published-method parent**. It receives no fidelity receipt, and the absence is correct
rather than a gap: ME-X6's generator emits per-period integer channel counts and no
bibliographic substrate — no papers, reference lists, citation edges, author records or
venues — so no published science-of-science estimator is natively computable on this
input and none is manufactured here. (V1 provenance receipt §2; the outputs of those
method families — `disruption`, `semantic_novelty`, `concentration`, `topic_spread` — are
already handed to every arm as planted channels.)

What it **is**: an untyped weighted aggregate of the same 16 channels, over the same
late-minus-early half difference every V1 arm uses, whose weight class **contains zero**
and non-unit magnitudes, and whose vector is **fitted from the public development split**,
not written down.

Two standard procedures are registered, both deterministic and RNG-free, both pure
standard library:

| arm | procedure |
|---|---|
| `B6_GREEDY_SUBSET_UNTYPED` | forward selection over (channel, weight ∈ {−2,−1,+1}); unselected channels weigh exactly 0; accept only on a **strict** improvement; tie-break by accuracy, then smaller \|weight\|, then channel order, then weight order; ≤ 16 rounds |
| `B7_L1_PATH_UNTYPED` | L1-penalised least squares by cyclic coordinate descent (zero init, 5000 iterations, tol 1e-10) over a frozen λ grid `λ_max·10^(−6j/24)`, `j = 0…24`, in two registered scalings (`RAW`, `STANDARDIZED`); selected by development accuracy, ties to the **larger** λ then `RAW`; \|w\| < 1e-9 is exactly 0 |

`B8` is whichever scores higher on the development split; an exact tie goes to `B6`.
Selecting the stronger of two **pre-specified** fitters on the development split only is
what makes the comparator the strongest available in its class. It sees no protected
instance.

## 3. The capacity control — what makes this a controlled comparison

`B4X_FITTED_UNTYPED_UNIT_SIGN_LEARNED_CONTROL` is **V1's own comparator**, refitted by
**V1's own `fit_signs`** on V2's development split. It is learned and information-matched;
only its weight class differs. G2 tests `B8` against it, so the study varies **capacity
while holding learnedness fixed** — which is precisely the confound V1's hand-set
diagnostic could not remove.

## 4. Pre-run reachability audit (a pre-outcome correction, recorded as one)

- **A clause of the form "the comparator is AHEAD of M" is deliberately NOT registered.**
  M is exact by construction on this generator (V1 design §1.3), so such a clause is
  **unreachable** — a gate that could not fire. The two live outcomes are the tie (G1b)
  and M-ahead (G1a). `G0d_M_EXACT_BY_CONSTRUCTION` therefore exists as a **validity**
  check, not a contrast: a failure there is generator drift, not a result.
- **The class contains a failing member** (all-+1 weights: 28/56 on development) and **an
  exact member** (V1's hand-set zeroing: 56/56). So the comparator arm can lose and can
  win; neither outcome is arithmetic.
- **Both fitters are heuristics that can miss a member of their own class**, demonstrated
  on constructed datasets in the selftest: forward selection reaches 5/6 where the hidden
  in-class rule reaches 6/6; the lasso path reaches 6/8 where the same rule reaches 8/8.
  **An exhaustive search over a class containing M's own vector was deliberately not
  registered** — it could not fail, and a tie would then be an identity rather than a
  measurement. This is the tautology V2 was most at risk of becoming.
- **The activity half is not scored and not reported.** V1 computes the activity direction
  from the activity channels by the same call for every arm, so an activity agreement is
  equal **by construction** and is not evidence (V1 provenance receipt §3). Publishing it
  would be a contrast that could not exist.
- **The protected seed governs instance generation only.** The comparator fit is a
  deterministic, RNG-free function of the public development split, frozen before the
  seed is revealed. Recorded because a seed with no effect on a parameter, left unstated,
  reads as the "seed doing nothing" defect.
- **The exact binomial tail is computed in rationals.** At n = 1400 the float form
  overflows and would return `inf`, making a `p > α` hard gate incapable of failing. V1
  hit this; the fix is carried, and the selftest asserts the tail is finite at protected
  scale.

## 5. Gates and routing

Every gate is a **positive** test carrying its own `n_evaluated`; a gate with
`n_evaluated == 0` reports `CANNOT_CHECK` and never a pass. No terminal is the negation of
another gate — in particular **G1b (the tie) is its own positive test**: equal totals
**and** zero discordant pairs, so a tie is verdict-level rather than two arms happening to
score the same.

| gate | kind | rule |
|---|---|---|
| `G0a_KNOWN_ANSWER` | hard | every selftest fixture reproduces; the denominator is read from the report |
| `G0b_GENERATOR_VALIDITY` | hard | planter agreement and fit-window decidability on every instance |
| `G0c_NULL_CALIBRATION` | hard | no constant arm reaches 0.60 capability accuracy |
| `G0d_M_EXACT_BY_CONSTRUCTION` | hard | M reproduces the oracle on every instance (validity, not contrast — §4) |
| `G0e_CAPACITY_MATCHING_BIT` | hard | the registered comparator's fitted vector zeroes ≥ 1 channel; otherwise the class containing zero was never exercised and the contrast is empty |
| `G8_VERDICT_CONSTANCY_WITHIN_CELL` | hard | every instance of a cell receives the same verdict, for M, the comparator and the control |
| `G1a_M_AHEAD_OF_CAPACITY_MATCHED_PARENT` | live | M's rate exceeds the comparator's **and** M wins cells while losing none |
| `G1b_TIE_AT_MATCHED_CAPACITY` | live | equal totals **and** zero discordant pairs |
| `G2_CAPACITY_IS_THE_SEPARATOR` | live | the capacity-matched **learned** comparator is ahead of the unit-sign **learned** comparator and loses no cell to it |
| `G6_CROSS_SCALE_CONSISTENCY` | live | the sign of (M − comparator) is the same at both units of analysis |

**Routing.** Any hard gate not passing, or any registered cell unexercised → `CANNOT_CHECK`,
terminal `NONE`. Else G1b → `PARENT_SUFFICIENT` /
`TYPING_NOT_SEPARATED_AT_MATCHED_CAPACITY`. Else G1a (and G6) →
`TYPED_STATE_SEPARATES_FROM_A_LEARNED_CAPACITY_MATCHED_PARENT`. Else `CANNOT_CHECK`.

**A tie is a registered success.** ME-X6's own design §1.3/§6 route it:
`PARENT_SUFFICIENT` / `TYPING_NOT_SEPARATED`, the protocol's contraction to an
interpretive framework — *"a legitimate publishable result and not a failure"*. V2 adopts
that routing unchanged.

## 6. Protected run

28 cells (14 strata × 2 scales) × 50 = **1400 instances**. `stage_protected` refuses
unless `PROTECTED_RUN_AUTHORIZATION.json` is present with `human_written: true`, a token
of ≥ 16 characters and an `acknowledged_design_sha256` equal to the frozen design's
digest (exit 3), and unless the custody seed hashes to the published commitment (exit 4).
The authorization is archived immediately after use so the guard is re-armed.

```text
GRANTS_SCIENTIFIC_TRUTH  = false
GRANTS_FIELD_STATUS      = false
GRANTS_MANUSCRIPT_CHANGE = false
FLAGSHIP_GATE            = false
```
