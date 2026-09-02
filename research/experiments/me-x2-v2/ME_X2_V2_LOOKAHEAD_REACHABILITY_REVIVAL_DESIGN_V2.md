# ME-X2 V2 — Lookahead and Best-Hypothesis Reachability: Revival of M's Two Registered Orderings (Registered Design V2)

**Class:** exact-oracle known-answer study — **zero model calls, fully
deterministic, CPU-seconds**. It re-tests ORION-V2's witnessed-obstruction and
minimum-escalation semantics against the strongest faithful parent federation
with **one thing changed**: the rendering of the two orderings that ME-X2 V1
registered (design V1 §4.1) as *M's rendering* rather than as ORION semantics.
**Parent sufficiency remains a successful terminal** and is again the
pre-registered expectation (§1.3).

**Parent lane.** `research/experiments/me-x2` (design sha256
`bb63685c02da55e7c7ebdf72541e862bcc92661b07a1074e33b8371a35e5d7c9`). V1's
registered expectation and its discarded protected-scale dry run (public seed
`ME-X2-DRYRUN-20260902`, results sha256 `3372a7c5…`, custody `71684694…`,
artifacts discarded) both route `PARENT_SUFFICIENT` with `B5` ahead of `M`.
**V1's result and artifacts are immutable and are not re-scored here.** No
number from that dry run is evidence and none enters this design; it supplied
only the failure signature this lane revives against:

> `M` takes the **cheapest** admissible discriminator with no lookahead, spends
> part of the budget on a weakly discriminating action, and its **fail-closed**
> reachability rule then correctly reports that no live hypothesis is
> establishable, so `M` declares `CANNOT_IDENTIFY`. Nearly all of `M`'s losses
> are false `CANNOT_IDENTIFY`; `M` never over-escalates.

**Status:** frozen design + lever known-answer fixtures + development split.
**No protected outcome has been generated or inspected.** The protected stage
refuses (§8); the authorization file is absent and no agent may author it.

Companion: `ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.json` (schema
`orion.v2.me-x2-v2.revival-study-design.v2`) carries every constant below;
`ME_X2_V2_PARENT_FIDELITY_AND_LEVER_RECEIPT_V2.md` carries code hashes, the
provenance check, parent fidelity, the lever known-answer results and the
development-split summary.

## 1. Question, hypothesis, expectation

**Q.** Do the two registered revival levers — (L1) one-step lookahead on
discriminator choice, and (L2) a reachability rule that preserves the **best**
live hypothesis rather than **every** live hypothesis — recover `M`'s decisions
against the same strongest faithful parent federation (`B5` rung 5), on the same
registered information, without buying decisions with escalation harm?

**H0 (strongest-parent sufficiency).** An exact expected-cost planner over the
same typed modules makes the same intervention decisions at equal or lower cost,
**whichever way** `M`'s two unfixed orderings are rendered.

### 1.2 What changes, and what may not

Changed: the rendering of V1 §4.1(i) and §4.1(ii), in the arm under test only.

Unchanged and **hash-verified** before every run (gate G0d): the generator, the
exact oracle, the template catalogue, every parent implementation, `B5` and the
whole H-EXT-3 ladder, both controls, and V1's rendering of `M` — which is
carried here as a registered arm so the lever delta is measured, not asserted.
The primary endpoint, outcome vector, strata, counts and gate thresholds are
V1's.

No ORION semantics were edited. `M2` subclasses V1's `M` and overrides exactly
two methods (`_reserve_ok`, `_discriminators`); `assess_discrepancy_locus`,
`route_frontier_action`, `JumpTrigger` / `JumpProposal` / `assess_jump` and
`minimum_level` are called exactly as V1 calls them. This is what makes the
lane a **mechanic** change: V1 itself registered these two orderings as choices
the reference semantics do not fix, so both renderings are equally faithful and
neither is a repair of ORION.

### 1.3 Pre-registered expectation

`PARENT_SUFFICIENT` remains the expected terminal. The registered outcome tables
make diagnosis a finite decision problem for which an exact planner is optimal;
a myopic rendering of minimum-escalation semantics cannot beat it. The decisive
content of a revival lane is the **lever verdict** (§7): whether the registered
levers recover the decisions V1's rendering lost.

**Lever expectation.** The levers are expected to recover the
*foreclosure-induced* abstentions — the class L2 addresses — and **not** the
*budget-horizon* ones: an action can be individually harmless and yet, two steps
later, leave a warranted high-level fix unaffordable. No one-step rule can see
that; only a finite-horizon planner can, and a rendering that could would be
`B5`. If the residual gap to `B5` is horizon-shaped, `PARENT_SUFFICIENT` is the
honest terminal and the residual is **interface-standard, not control**.

**G1a reading, registered in advance.** L1's ordering pushes `M2`'s test choices
toward `B5`'s, so the decision-sequence identity rate may rise from V1's
development value (0.646) to a G1a pass, short-circuiting the route to
`PARENT_SUFFICIENT` before G1b is consulted. Registered now, so it is a finding
and not a discovery: under G1a-pass the result is that the **improved** rendering
of ORION's unfixed orderings is reproduced by an exact planner, which is a
*stronger* parent-sufficiency result than V1's, not a weaker one.

**Escalation risk.** V1's `M` never over-escalated, so every new failure mode
`M2` can have is escalation harm or a moved failure. G2 is therefore this lane's
live gate and is evaluated against `B5` **and** against V1's `M`.

**Predicted shift (falsifiable, not a gate).** Because "best" is rendered as the
minimum-responsible hypothesis (§2.2), L2 forfeits expensive high-level
hypotheses before cheap ones. `M2`'s residual failures should therefore shift
from uniform false `CANNOT_IDENTIFY` toward **missed escalation concentrated on
the high-level strata** (`MEASUREMENT_OR_EVALUATOR_BLIND`,
`TOOL_INSTRUMENT_INADEQUATE`, `WORKFLOW_INADEQUATE`). Reported per stratum.

### 1.4 Primary endpoint

Unchanged from V1 (ARFT addendum). Per instance, **decision-correct** is:

- oracle level *L* exists → the episode ends in `SUCCESS` whose last intervention
  is the oracle minimal fix **and no intervention above level *L* was applied**;
- oracle level is null → the episode ends in a `CANNOT_IDENTIFY` declaration
  **with no level ≥ 2 intervention applied**.

## 2. The levers

### 2.1 L1 — one-step lookahead on discriminator choice

Replaces V1 §4.1(i). Admissible discriminators are ordered lexicographically by

```
(expected_abstention, best_foreclosed, foreclosed, expected_residual_ambiguity, cost, kind_rank, action_id)
```

computed from the registered outcome tables one step ahead, under the uniform
prior over live causes that every arm shares.

| term | definition |
|---|---|
| `expected_abstention` | Σ over registered outcome branches of P(branch) × 1[no live hypothesis in the branch remains establishable] — **M's own diagnostic-evaluator adequacy check applied prospectively to the successor state** |
| `best_foreclosed` | Σ P(branch) × 1[the minimum-responsible establishable hypothesis of the branch is foreclosed] |
| `foreclosed` | Σ P(branch) × (number of hypotheses establishable now and not after) |
| `expected_residual_ambiguity` | Σ P(branch) × (\|branch\| − 1) |
| `(cost, kind_rank, action_id)` | V1's own total order |

Abstention leads the key because abstention **is** the diagnosed failure;
ambiguity is only a proxy for it. The tail is V1's order, so **M2 reduces to M
whenever the diagnostic terms are indifferent** — asserted in the unit tests. A
repair-as-test branch in which the repair resolves the hypothesis ends the
episode in `SUCCESS`: its weight is counted and all four diagnostic terms are
zero.

**L1 is not a planner.** It has no cost model beyond the registered costs, no
failure penalty, no free parameter and no recursion. It ranks admissible
discriminators by prospective diagnostic adequacy, then discrimination, then
V1's tie-break; it does not minimise expected total cost and is myopic by
construction. A rendering that minimised expected total cost over the full
horizon would be `B5`, not `M`.

**Registered alternative, untried:** leading the key with
`expected_residual_ambiguity` and demoting the foreclosure terms. Placing
foreclosure above discrimination is a registered choice, made because G2 is this
lane's live risk; the alternative is V3 material and is not evaluated here.

### 2.2 L2 — best-live-hypothesis reachability

Replaces V1 §4.1(ii). A discriminating action is admissible if the **best** live
hypothesis — the establishable account requiring the least escalation, ordered by
(minimal-fix level, minimal-fix cost, cause id) — **remains establishable in the
registered outcome branch that contains it**. A branch that *refutes* the best
hypothesis is a defeat, not a resource foreclosure, and does not bar the action;
a repair-as-test that resolves the best hypothesis is its own fix and does not
bar it either. Where no live hypothesis is establishable at all the rule is
vacuous, exactly as in V1.

The effect is to demote V1's fail-closed rule from a **prohibition** to a
**preference**: L2 sets admissibility on the minimum-responsible hypothesis, and
L1's `best_foreclosed` / `foreclosed` terms still prefer actions that foreclose
nothing.

**Registered bias.** Rendering "best" as the minimum-responsible hypothesis is
anti-escalation by construction: it preferentially forfeits expensive high-level
hypotheses. This is registered before outcomes, priced by G2 and by the
missed-escalation and false-`CANNOT_IDENTIFY` outcomes, and predicted per
stratum in §1.3.

**Registered alternatives, untried:** preserve the *most-escalating* live
hypothesis (worst-case preservation); preserve the *cheapest-to-complete*
hypothesis (planner-flavoured); preserve one hypothesis *per registered outcome
branch* — strictly more conservative than L2, and rejected because it is not the
registered lever and does not release the abstentions L2 targets (§9).

## 3. Arms

25 arms. The comparator side is the **frozen V1 classes**, imported and not
re-implemented.

| group | arms |
|---|---|
| baselines | `B0_RETRY_SEARCH`, `B1_UNCERTAINTY_ABSTENTION`, `B2_FAILURE_TAXONOMY_DIAGNOSIS`, `B3_MODEL_BASED_DIAGNOSIS_VOI`, `B4_MDA_MODEL_EXPANSION` |
| matched control | `B3_EQUAL_EXTRA_SEARCH_1_5X` |
| H-EXT-3 ladder | `B5_R1_VERDICT_ONLY` → `B5_R2_PLUS_CANDIDATE_SET` → `B5_R3_PLUS_DISCRIMINATOR_TABLES` → `B5_R4_PLUS_DISPOSITION_RECORDS` → **`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`** (primary comparator), plus `B5_NO_ABSTENTION_GATE` |
| reference | `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION` — V1's rendering, imported unchanged |
| **arm under test** | **`M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS`** (L1 ∧ L2) |
| lever decomposition | `M2_L1_LOOKAHEAD_ONLY`, `M2_L2_BEST_HYPOTHESIS_ONLY` |
| ablations (protocol V2, applied to the arm under test) | `M2_MINUS_LOCUS_DIAGNOSIS`, `M2_LOCUS_LABELS_SHUFFLED`, `M2_MINUS_DIAGNOSTIC_EVALUATOR_GATE`, `M2_MINUS_LOWER_LEVEL_DISPOSITION`, `M2_MINUS_PROSPECTIVE_DISCRIMINATOR`, `M2_ALWAYS_ESCALATE_WHEN_STUCK`, `M2_NEVER_ESCALATE` |
| controls | `C_RANDOM_POLICY`, `C_NEVER_INTERVENE` |

## 4. Strata, counts, seeds

Stratum = **oracle class** (the 12 registered families). Protected: 50 pairs per
stratum = **1 200 instances**; development: 2 pairs per stratum = 48. The
stratum is the *oracle* class, so partners re-stratify and per-stratum counts are
reported as observed (V1 observed 50–273 at scale).

**Seed commitment.** Protected seed sha256
`f85372cf187678f7517dcf73d41d6595add7dfd4ed04b6c218e08bb1854646fe` — a **fresh**
seed, never used by V1 and never used by V1's discarded dry run (operator custody
`~/.orion-custody/me-x2-v2/PROTECTED_SEED_V2.txt`, mode 600; env override
`MEX2V2_PROTECTED_SEED_FILE`, V2-specific so a V2 run can never consume V1's
committed seed). The runner verifies the hash before any protected generation;
the seed string is revealed in the outcome receipt so the split regenerates
byte-for-byte. Public seeds: development `ME-X2-V2-DEV-20260902`, selftest
`ME-X2-V2-SELFTEST`, lever-fixture search `ME-X2-V2-FIXTURE-SEARCH-20260902`,
G0 scale probe `ME-X2-V2-G0SCALE-PUBLIC-20260902`.

**Power / MDE.** Primary statistic = paired per-instance decision-correct
indicator, `M2` vs `B5`, exact two-sided binomial (McNemar exact) on discordant
pairs. Pooled n = 1 200: 6 one-directional discordants reach p = 0.031, 8 reach
p = 0.008. The lever test (G5a) uses the same paired statistic on `M2` vs V1's
`M`.

## 5. Outcomes

V1's outcome vector unchanged (classification accuracy, locus accuracy, Brier /
5-bin ECE, **minimal-level decision accuracy (primary)**, verified success,
false escalation, missed escalation, false / correct `CANNOT_IDENTIFY`,
recurrence, specification damage, false world-change / model / representation
attribution, regret, total cost, wall-clock reported only), per arm, per stratum
and per variant. V2 adds per-instance **lever receipts**: for each step, the
chosen action's four diagnostic terms, whether the action was admissible only
under L2, and whether L1 changed the choice V1's order would have made. G5(c)
reads the mechanism from these receipts rather than inferring it from the
trajectory. V1's inherited `act()` consults the discriminator ranking *before*
its unique / common-fix branches, so a receipt can describe an action `M2` never
took: attribution counts only receipts whose step matches the **executed**
trajectory step. On the public surfaces this filter removes 2 of 322 receipts
(144-instance fixture search) and 6 of 2 486 (1 200-instance scale) — small, and
it can only inflate G5(c) if left in.

## 6. Gates

- **G0a `KNOWN_ANSWER` (hard):** V1's 14 hand-authored fixtures and the H-EXT-3
  separation pair (oracle targets reproduced; `M2` and `B5` decision-correct),
  plus the 6 V2 lever known-answer fixtures (§9).
- **G0b `ORACLE_SELF_AGREEMENT` (hard):** as V1.
- **G0c `NULL_CALIBRATION` (hard):** `C_NEVER_INTERVENE` = 0 on identifiable
  instances; `C_RANDOM_POLICY` ≤ 0.25; **`M2` scored against the partner
  instance's oracle** ≤ `M2`'s true rate − 0.30. The random-control clause is an
  n-sensitive frequency claim about a 1 200-instance split and is enforced on the
  protected split and the scale probe, reported below that split size — exactly
  how V1 already treats decoy coverage. The never-intervene and swap-null clauses
  are hard at every label, and no clause concerning an arm under test is relaxed
  anywhere.
- **G0d `V1_PROVENANCE` (hard, new):** every frozen V1 file byte-identical to the
  hash published in the V1 parent-fidelity receipt. V2 changes the arm under test
  and nothing else, so a V2 result can never be a comparison against a silently
  different world.
- **G1a `B5_REPRODUCES_M2`**, **G1b `M2_ADVANTAGE`**, **G1c `B5_ADVANTAGE`:** as
  V1, with `M2` in `M`'s place.
- **G2 `ANTI_ESCALATION`:** `M2`'s false escalations ≤ `B5`'s **and** `M2`'s
  specification damage ≤ `B5`'s (V1's clause), **and both ≤ V1's `M`**. A revival
  may not buy decisions with escalation harm.
- **G3 `MEDIATION`** (only if G1b): as V1, with the `M2` locus ablations.
- **G4 `INTERFACE_LADDER`:** as V1.
- **G5 `LEVER_ATTRIBUTION` (new):**
  (a) paired `M2` − `M_V1` decision-correct > 0 at exact two-sided p ≤ 0.05;
  (b) neither single-lever arm improves on `M_V1` by more than the conjunction
  does;
  (c) ≥ 80% of `M2`-only-correct-vs-V1 instances are ones where V1 declared a
  **false `CANNOT_IDENTIFY`** *and* `M2`'s **executed** lever receipts show an
  L2-only-admissible action or an L1-changed choice;
  (d) `M2` loses fewer instances to V1 than it gains from it — **the revival must
  not move the failure**.
  Clauses (a), (c) and (d) each route the lever verdict of §7; (b) is a reported
  diagnostic. G5 does not route the primary comparison, which is `B5`-relative by
  design.
- **COST:** paired sign test on per-instance regret, p ≤ 0.05. Wall-clock routes
  nothing.

## 7. Pre-registered routing

| outcome | route |
|---|---|
| G0 fail (a/b/c/d) | `CANNOT_CHECK` — lane defect; repair, re-freeze, no arm verdict |
| G1a pass | `PARENT_SUFFICIENT` (ladder `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`) |
| G1b ∧ ¬G2 | `M2_OVER_ESCALATES` |
| G1b ∧ G2 ∧ ¬G3 | `CANNOT_CHECK` |
| G1b ∧ G2 ∧ G3 ∧ cost `COST_ADVANTAGE_B5` | `QUALITY_COST_TRADEOFF_NO_DOMINANCE` |
| G1b ∧ G2 ∧ G3 otherwise | `ME_X2_RESIDUAL_CANDIDATE` |
| G1c pass | `PARENT_SUFFICIENT` (`B5_DOMINATES`) |
| neither | `PARENT_SUFFICIENT` |

**Lever verdict** (reported alongside every primary route; the decisive content
of a revival lane):

| condition | verdict |
|---|---|
| `M2` significantly worse than V1's `M` | `LEVERS_HARM` |
| no significant `M2` − `M_V1` difference | `LEVERS_NULL` |
| `M2` better than V1 but G2's vs-V1 clause fails, or V1-only-correct ≥ M2-only-correct (G5d) | `LEVERS_MOVE_THE_FAILURE` |
| `M2` better than V1 but G5(c) fails: the executed receipts do not attribute the gain to either lever | `LEVERS_NOT_ATTRIBUTED` |
| `M2` better than V1, attributed, `B5` still significantly ahead | `LEVERS_PARTIAL_RECOVERY` |
| `M2` better than V1, attributed, no escalation regression, `B5` not significantly ahead | `LEVERS_RECOVER_M` |

`PARENT_SUFFICIENT` is a successful scientific terminal, and so is `LEVERS_NULL`.

## 8. Custody and protected-run discipline

- Code: `mex2v2_levers.py`, `mex2v2_arms.py`, `mex2v2_provenance.py`,
  `mex2v2_run.py`; sha256 frozen in the receipt. The V1 lane is imported, never
  edited. Determinism: results and custody files byte-identical on re-run;
  wall-clock in a separate timing file.
- Stages: `selftest`, `dev` (≤ 48 instances, label DEVELOPMENT, never protected),
  `g0scale` (public seed, V1-known arms only), `protected`, `analyze`.
- The `protected` stage **refuses** unless `PROTECTED_RUN_AUTHORIZATION.json`
  (human_written = true, a human-written token ≥ 16 chars,
  `acknowledged_design_sha256` = sha256 of this design JSON) is present next to
  the runner, **and** the custody seed hashes to the commitment, **and** G0d
  holds. The file is absent in this PR; the tests assert its absence and every
  refusal path. **No agent may author it** — the lane is delivered frozen and
  armed, and the protected run is an operator action.
- Estimated protected cost: 1 200 instances × 25 arms ≈ 15–60 CPU-seconds on one
  core; budget 5 CPU-minutes. Mac local; never a heavy job; never CI on the Mac
  mini.

## 9. Development surfaces, disclosed

Everything below is public-seed development. No protected instance has been
generated or inspected, and no gate, threshold, stratum weight, oracle rule,
generator rule or arm policy was chosen by looking at a protected outcome.

| seed (public) | n | role |
|---|---|---|
| `ME-X2-V2-DEV-20260902` | 48 | development split, all arms, committed artifacts |
| `ME-X2-DEV-20260902` | 48 | V1's development split, re-run with the V2 arms as a regression check |
| `ME-X2-V2-FIXTURE-SEARCH-20260902` | 144 | located the 6 episodes on which V1's `M` declares a false `CANNOT_IDENTIFY`; frozen verbatim as the lever known-answer fixtures; also the V1-vs-`M2` regression check (no parent comparison was run on this surface) |
| `ME-X2-V2-G0SCALE-PUBLIC-20260902` | 1 200 | G0 coverage probe at protected scale with **V1-known arms only** (`M_V1` and both controls), so it reveals nothing about the V2 comparison |

**Lever known-answer fixtures.** `ME_X2_V2_LEVER_KNOWN_ANSWER_FIXTURES_V2.json`
freezes those 6 episodes verbatim (truth included) so the test does not depend on
the generator: 4 that the levers recover and **2 registered limits** that they do
not. Freezing the limits is deliberate — the fixture pins the boundary of the
claim, not only the win; a change there is a lane event requiring a re-freeze.

**One rendering repair before the freeze.** L2 was first rendered as "some
establishable hypothesis survives in every registered outcome branch". That is
still fail-closed per branch and therefore not the registered lever; it was
corrected to the registered rule (§2.2). Both renderings are stated; the rejected
one is registered as an untried alternative.

**No protected-scale V2 dry run.** Deliberate. The G0 clauses concern the
generator, which G0d freezes byte-identical, and they are re-checked at scale by
the public probe with V1-known arms. Running the V2 arms at scale before the
protected run would reveal the V2 comparison, and V1's receipt already documents
why that is uncomfortable.

## 10. No-rescue clause and registered limitations

No stratum weight, oracle rule, arm, lever, seed, gate or threshold changes after
the protected results file exists. A protected result is never re-run under a new
seed. A lane defect found mid-run halts the lane, is receipted, and re-freezes as
V3. **No third lever is added after this freeze**: the registered alternatives of
§2.1 and §2.2 are V3 material and require their own design and their own
committed seed. V1's result and artifacts are immutable and are not re-scored.

Registered limitations (before outcomes): synthetic ORION-authored episodes
cannot alone support a field-level residual (decisive-studies §11.6); the
registered outcome tables make diagnosis a finite decision problem whereas real
episodes carry unregistered hypotheses; ARFT is represented by an equivalent
taxonomy rather than the licensed artifact; the uniform prior over live causes is
a modelling choice shared by every arm and L1's branch weights use it; the Jump
lattice is a comparator interface and is not presumed correct; **both levers are
myopic by construction**, so a residual gap to `B5` that is horizon-shaped is not
evidence against the levers and is not a defect this lane can repair without
turning `M` into a planner; and the lever fixtures were located by scanning a
public development seed for the diagnosed signature — frozen and hand-checkable,
but not an independent sample of that failure mode.

**Authority.** None. Development numbers are development numbers; a protected
outcome under this design decides only this study's registered question. No field
status, novelty, architecture-adoption or publication authority is granted or
implied. No claim from this study reaches the naturalistic cell.
