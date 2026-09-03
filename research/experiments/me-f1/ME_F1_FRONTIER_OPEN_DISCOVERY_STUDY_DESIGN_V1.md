# ME-F1 — Machine-epistemics control under open discovery at a matched resource budget

**Class:** open discovery · post-hoc reference ground truth · model arms · matched budget · no rescue
**Protocols served:** `MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md` §4.2/§4.3 (levels 0–4 only)
**Secondary axis:** H-EXT-3 interface ladder
**Status:** `FROZEN_DESIGN__DEVELOPMENT_CALIBRATION_ONLY__NO_PROTECTED_RUN`
**Companion:** `ME_F1_FRONTIER_OPEN_DISCOVERY_STUDY_DESIGN_V1.json` (every constant; the hashed artifact),
`ME_F1_FEASIBILITY_TABLE_V1.md` (family choice and measured costs),
`ME_F1_PARENT_FIDELITY_RECEIPT_V1.md` (code hashes, parent tests, development split)

---

## 1. Question, hypothesis, expectation

### 1.1 The gap this closes

Three exact studies have terminated `PARENT_SUFFICIENT`: ME-X1 (transition coupling), ME-X2
(obstruction locus and minimum escalation) and ME-X4 (selective reopening). ME-X2's outcome receipt
states the decisive limitation of all three in its own words: its worlds have uniform decidability and
strictly increasing cost bands, which make an exact expected-cost planner optimal **by construction**.
Its honest terminal was *"no ME residual is detectable in a registered decision problem the parents
already solve exactly"* — **not** *"no ME residual exists"*. ME-X1 and ME-X4 share that character:
generated worlds with exhaustive oracles.

So every negative the programme holds comes from a world where a strongest-parent federation can
simply compute the right answer. A control layer plausibly earns its keep precisely where it cannot:
where discovery is open, the oracle does not exist in advance, resources bind, and the system must
decide what to try next and when to stop. No study in the programme has tested that.

The problem the programme names is demonstrably real even inside the solved worlds. ME-X1 measured
its direct arm laundering **492 unwarranted updates**, and the strongest *truth-maintenance*
federation (`B4_PARENT_MODULES_WITH_SHARED_STATE`) laundering **163**, scoring 0.837. That is a
measured failure to point at. This study is built so that failure can be scored again in a world
where nobody can compute the answer.

### 1.2 Pre-registered expectation

**We do not predict that M wins.** The parents in this world already implement a *correct*
warranted-claim discipline — Mitchell version spaces plus calibrated abstention — which is precisely
the organ ORION contributes. On the development split the deterministic parent federation made **zero**
unwarranted claims. The honest prior is that B5 is strong on the endpoint that matters most, and that
any M residual, if it exists at all, lies in resource allocation and stopping rather than in warrant.

Two outcomes are registered in advance as honest terminals:

- **`PARENT_SUFFICIENT` is a successful terminal**, and in this world it is a *stronger* statement
  than the three that preceded it, because the parents no longer have a computability advantage
  handed to them by construction.
- **If `B5_ALGORITHMIC_CORE_NO_MODEL` — the parent federation in pure code, zero model calls — beats
  every model arm**, the honest reading is that model control adds nothing in this world. That is
  written here, before the run, so it cannot be reframed afterwards.

### 1.3 Boundary with sibling lanes

**FG80** (`lane-fg`) generates synthetic mini-frontier episodes with an **exact known-answer oracle**
and **zero model calls**, and asks whether the mechanism can discover that a new intermediate
representation is needed. ME-F1 has **no oracle at the arm budget** and **real model arms**. FG80 asks
*can the mechanism do it at all, in a world where the answer is knowable*; ME-F1 asks *does the whole
system hold up under resource pressure against a real federation, where nothing can compute the answer
at budget*. Resource-to-solution curves, false-completion rate and correct abstention are things an
exact deterministic suite cannot measure. A deterministic zero-model-call variant of this world was
considered and rejected, partly for this reason — feasibility table §2.

**`lane-e30r12`** is the naturalistic arm of the same question (BugsInPy repair). Not duplicated here.
**FG90** (`lane-mex3`) is `EXPLORATORY_ONLY` and not a study.

---

## 2. Frozen inputs

### 2.1 The world

A **discovery campaign** is `k` **independent sub-ladders** ("blocks") sharing **one** frozen budget.
Each block is a monotone chain of random 3-SAT systems over its own variable set; rung *j* of a block
uses the first `round(n_vars · α_j)` clauses of that block's pool, with

    α = (3.2, 4.0, 4.267, 4.7, 5.6)

straddling the random-3-SAT satisfiability threshold (α ≈ 4.267): two comfortably satisfiable rungs,
one critical, two comfortably unsatisfiable. Prefix nesting makes every sub-ladder monotone **by
construction** — a subset relation, not a checked property.

### 2.2 Why blocks, and not one ladder

This is the design's load-bearing correction, and it was found by measurement. With a **single**
ladder, two verified events that bracket the boundary entail **every** rung by monotone closure, so
the primary endpoint saturates however hard the individual rungs are made. Measured on the development
split at `n_vars=40`: the deterministic arms scored **12/12**. Independent blocks make an arm buy a
bracket in each block separately. After the change, the same development split gives
`C_UNIFORM_ALLOCATION` **0.575** and `B5_ALGORITHMIC_CORE_NO_MODEL` **0.912** — a wide band that moves
with control quality rather than with instance size.

### 2.3 What the ladder licenses, and what it forbids

Within a block, and only within a block:

| Inference | Licensed by |
|---|---|
| `SATISFIABLE` at every **lower** rung | a **verified witness** at this rung |
| `UNSATISFIABLE` at every **higher** rung | a **completed refutation** at this rung |

Forbidden: failing to find a witness licenses nothing; a witness licenses nothing upward; a refutation
licenses nothing downward; **nothing crosses a block boundary**. An arm that converts "I searched and
did not find one" into `UNSATISFIABLE` has made an unwarranted claim, and the scorer detects that from
the arm's own execution log without consulting ground truth.

Verification is mechanical and free — O(clauses). Finding a witness, or exhausting the space to
refute, is what the budget buys and what no arm can complete for every rung.

### 2.4 Protocol coverage, and what this world cannot test

Levels 0–4 have faithful realisations here: more budget (L0), restart (L1), switch tool class (L2),
re-encode (L3), attack a different rung (L4). Protocol levels **5** (method/tool/instrument invention)
and **6** (workflow/meta-skill revision) have **no** faithful realisation in a fixed-toolbox world and
are out of scope **by registration, not by oversight**. No claim about levels 5–6 may be read from this
study. This is a deliberate application of the understand-before-fitting rule: the escalation ladder is
mapped where the mechanism genuinely corresponds, and declared absent where it does not.

### 2.5 Openness is bounded-resource openness

This is openness **at the registered budget**, not undecidability. The reference solver settles these
rungs at 40× the arm budget. The claim is that **no arm can compute the answer with the resources it is
given** — exactly what ME-X2's worlds did not have — and *not* that the problems are absolutely
intractable. Registered as a limitation, not glossed.

### 2.6 The identical-toolbox constraint

Every arm calls the same primitives through the same meter with the same budget and the same
model-call cap. No arm has a primitive another lacks. This forecloses the strongest objection available
against any residual this study might find: that the openness of the search was an artefact of denying
some arm a solver.

- `local_search` — WalkSAT. Returns a **verified** witness or `INCONCLUSIVE`. **Can never establish
  unsatisfiability.**
- `exact_solve` — DPLL with unit propagation. Returns `WITNESS_FOUND`, `REFUTED` (**only** when the
  space was exhausted within the node limit), or `INCONCLUSIVE`.
- `preprocess` — `none | unit_pure | subsumption | symmetry`, satisfiability-preserving by
  construction (asserted by G0b).
- `verify` — free, unmetered, available to every arm.

### 2.7 The budget unit

One **constraint check** = one evaluation of one clause against one assignment. It is the only
primitive shared by stochastic local search and backtracking search, it is hardware- and
language-independent, and it is exactly countable — which wall-clock is not. Wall-clock is a reported
secondary and never a matched budget.

Each campaign gets **300 000 constraint checks** and **8 control calls**: seven action decisions plus
one **closing call**. The closing call executes no action and exists so an arm can claim the evidence
its last action produced; without it the last action's result is unclaimable by construction. An arm
that stops early keeps its unspent calls but still receives its closing call, on the same terms as
every other arm. A **failed** model call is booked as `model_calls = 1` — a failure consumes channel
capacity and must appear in the matched budget.

### 2.8 The model channel, and what is actually attested

The channel is the **Codex CLI** (`codex exec`, strict structured output) on **billy-old**, requesting
**`gpt-5.5`** at `medium` reasoning effort, identical for every model arm. The protected run does not
execute on the Mac. LUNARC's login node has no `codex` on PATH; billy-old carries the programme-pinned
`codex-cli 0.129.0-alpha.15`, on which `gpt-5.6-sol` fails outright (rc=1, models-cache `unknown
variant \`max\``) and `gpt-5.5` returns schema-valid output. The frozen model is what the execution host
can actually serve, fixed before any protected campaign exists.

The z.ai channel was rejected: it **substitutes silently** — a `glm-5.2` request is served `glm-5.3`
with HTTP 200 and no warning (issue #45). A study whose budget is matched in model calls cannot
tolerate a silent mid-campaign model swap.

On the Codex channel, **no served-model id is exposed**. The CLI's `model:` header is an *echo of the
request*: a probe requesting `definitely-not-a-real-model-xyz` printed that id back verbatim, and with
`--json` no model id appears at all. This design therefore does **not** fake an attestation. It records
the triad `requested_model` / `served_model_observed: null` / `served_model_source:
NOT_EXPOSED_BY_CODEX_CLI__HEADER_IS_REQUEST_ECHO`.

The fail-closed guarantee rests instead on **refusal-not-substitution**, established by probe **on the
execution host** (billy-old, 2026-09-02): the bogus-model request returned `rc=1` with `not found` and
wrote **no output file** at all.
Because the channel refuses rather than substitutes, a call returning `rc=0` with a schema-valid body
was served by a model the endpoint accepted for the frozen id. Any non-zero exit, missing output,
timeout or schema violation is a hard arm failure: recorded, counted, never retried into silence, never
scored as an answer.

### 2.9 Ground truth

The **same sound primitives** at **K = 40×** the arm budget, run entirely outside the experiment and
never visible to any arm. Ground truth is closed under each block's own monotonicity — a sound
inference from the prefix construction that can only convert `UNSETTLED` into a known status, and is
applied to ground truth **only**. The reference pass depends solely on the campaign and K, never on any
arm, so it may run before or after the arms without affecting anything. Ground truth is not a field of
the campaign object the arms receive.

---

## 3. Splits, calibration, and the difficulty knob

### 3.1 Calibration is on the primary endpoint

Difficulty is a tuning knob and is frozen like one, on a development split, under a window and a rule
fixed before any protected campaign exists. The calibration arm is `C_UNIFORM_ALLOCATION` and the
calibration endpoint is **the primary endpoint itself** — `warranted_correct_rate`.

That is a correction. An earlier version of this design calibrated on a *proxy* (the fraction of rungs
a uniform policy settles directly by a tool), selected a rung on which the proxy sat inside the window,
and would have run a study whose primary endpoint was in fact saturated at 1.0.

| | |
|---|---|
| Window | **[0.30, 0.70]**, point estimate inclusive |
| Ladder | L1 (24 vars, 240 k) → L2 (30, 300 k) → L3 (36, 360 k) → L4 (42, 420 k) |
| Campaigns per rung | 16, from the development seed |
| Procedure | ascend; stop at the **first** rung inside the window (`WINDOW_HIT`) |

Terminals, each tested **explicitly** — none is a fall-through: `WINDOW_HIT`,
`SUITE_STILL_SATURATED`, `LADDER_OVERSHOT_NO_WINDOW_HIT`, `SUITE_AT_FLOOR_AT_FIRST_RUNG`,
`CALIBRATION_INVALID_INCONSISTENT_GROUND_TRUTH`.

**If no rung enters the window, that is a terminal**, not a reason to adjust the ladder, the budget, the
block count or the alphas.

### 3.2 Splits

Development campaigns use the development seed; the protected split uses the committed protected seed
and does not exist until that seed is revealed to the runner. Protected: **150** `F_CRITICAL`
campaigns and **12** `F_PLANTED`.

### 3.3 Planted campaigns are excluded from the primary by registration

`F_PLANTED` campaigns plant a satisfying assignment in every rung, which makes them easier than
critical density. They are used **only** for G0 generator validity and for clean false-completion
measurement, and are excluded from the primary **by registration, not by a post-hoc decision**.

---

## 4. Arms

| Arm | Role |
|---|---|
| `SIMPLE_DIRECT` | model control, no warrant discipline |
| `SAME_MODEL_REFLECTION` | + a registered self-review pass |
| `B5_R1_VERDICT_ONLY` … `B5_R3_PLUS_FEATURE_TABLES` | H-EXT-3 interface ladder rungs 1–3 |
| **`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`** | **primary comparator**, ladder rung 4 |
| **`M_ME_FRONTIER_CONTROL`** | **M**, ORION control |
| `M_MINUS_WARRANT_GATE`, `M_MINUS_LOCUS_DIAGNOSIS`, `M_MINUS_MINIMUM_ESCALATION` | omission ablations |
| `M_LOCUS_LABELS_SHUFFLED` | separates *labels present* from *labels correct* |
| `B5_ALGORITHMIC_CORE_NO_MODEL` | the federation in pure code; bounds the model arms from **above** |
| `C_UNIFORM_ALLOCATION`, `C_RANDOM_ALLOCATION`, `C_NEVER_CLAIM` | calibration arm and null floors |

**B5 is built from named published methods at real strength**, because ME-X2's B5 beat M and that is
the bar: algorithm selection (Rice 1976; SATzilla, Xu et al. 2008), per-block binary search over the
monotone ladder, the Luby et al. (1993) / Gomes et al. (1998) restart policy, Mitchell (1982) version
spaces, and calibrated abstention. It is information- and resource-matched, allowed ordinary glue, and
deliberately not isolated.

**M** is three organs: (1) a **warrant gate** — every asserted verdict must name its licence, and
failing to find licenses nothing; (2) **locus diagnosis** of what obstructs each unsettled rung; (3)
**minimum escalation** over levels 0–4, cheapest action addressing the diagnosis first.

### 4.1 Information matching is a property of the code

B5 and M receive the same campaign view, toolbox, budget, model, reasoning effort and number of control
calls. They differ **only** in the frozen control text, published verbatim in the design JSON. The
arm-facing view is a single function (`Campaign.arm_view`) that excludes ground truth, the reference
budget, the seed and every per-rung difficulty annotation — so matching is checkable, not asserted.

### 4.2 The risk this design carries, stated plainly

Because both arms are the same model under different instructions, a difference between them is a
difference between two frozen prompts. The ablations and the deterministic B5 core are what separate
*"ORION's organs carry the effect"* from *"this prompt happens to be better written"*. **A residual the
ablations cannot attribute routes `CANNOT_CHECK`, not `FRONTIER_RESIDUAL_CANDIDATE`.**

---

## 5. Outcomes

### 5.1 Primary — `warranted_correct_rate`

Over ground-truth-decided rungs of `F_CRITICAL` campaigns: the fraction whose claimed verdict is **both**
correct against ground truth **and** structurally warranted by the arm's own execution log.

Two axes are kept strictly separate, and the separation is the point:

- **correctness** is scored against ground truth no arm ever saw;
- **warrant** is computed from the arm's own log and never reads ground truth.

An arm can be **correct-and-unwarranted** — the laundering failure ME-X1 measured — or
warranted-and-correct. A study that scored only correctness would rank a laundering arm at the top of
the unsatisfiable rungs, because those rungs really are unsatisfiable; it would just have no right to
say so.

**Abstention scores zero.** `UNRESOLVED` contributes 0, so **no arm can win the primary by refusing to
answer**. This is the structural repair of the exact failure ME-X2 found, where M's `CANNOT_IDENTIFY`
on decidable episodes was simultaneously its G2 pass and its loss.

Estimand: paired difference M − B5. Test: campaign-level paired exact sign test (two-sided, α = 0.05).
The rung-level difference is reported with a **campaign-cluster bootstrap** interval, because rungs
inside a campaign share a budget and a trajectory and are not independent.

### 5.2 Secondary

Coverage; witness-found rate; **false-completion rate**; **unwarranted-claim rate** (the ME-X1
laundering analogue); `correct_and_unwarranted` (the count a correctness-only endpoint would silently
reward); abstention and correct abstention; **resource-to-solution curves** at 10/25/50/75/100 % of
budget spent; cost in checks, calls and tokens.

### 5.3 Cost is reported, never a route

Wall-clock is flagged at 2× and never routes by itself.

---

## 6. Gates

| Gate | Rule |
|---|---|
| **G0a** `KNOWN_ANSWER` (hard) | warrant-validity fixtures for every licensed and every forbidden inference, including the block-crossing case; parent fidelity self-tests pass N/N |
| **G0b** `TOOLBOX_SOUNDNESS` (hard) | every `WITNESS_FOUND` independently verified against the unpreprocessed rung; `REFUTED` only on an exhausted space; every preprocess mode satisfiability-preserving; ground truth monotone within every block |
| **G0c** `NULL_CALIBRATION` (hard) | `C_NEVER_CLAIM` exactly 0; `C_RANDOM_ALLOCATION` ≤ 0.75 (a loose bound by design — the random arm still claims only what is entailed, so it floors *allocation*, not warrant) |
| **G0d** `GENERATOR_VALIDITY` (hard) | every `F_PLANTED` rung is ground-truth SAT; `F_CRITICAL` campaigns contain both SAT and UNSAT rungs |
| **G0e** `LAUNDERING_VARIANCE` (hard) | on the development split, `SIMPLE_DIRECT`'s unwarranted-claim rate must be **> 0** and **> B5's** — otherwise the primary endpoint has no variance to detect and the study routes `CANNOT_CHECK` **before any protected dispatch** |
| **G1** `M_ADVANTAGE` | paired difference > 0 and sign-test p ≤ 0.05 |
| **G1c** `B5_ADVANTAGE` | the symmetric test |
| **G2** `ANTI_CONSERVATISM` | M coverage ≥ B5 coverage − **0.05** |
| **G3** `MECHANISM` | applicable only if G1 fires: every M ablation strictly below M |
| **G4** `INTERFACE_LADDER` | H-EXT-3 monotonicity across the four B5 rungs, tolerance 0.02 |

### 6.1 Which anti-conservatism defence binds

Two defences guard the same failure, and the design says which is which. The **primary** defence is
**structural**: abstention scores zero in the primary endpoint, so an abstaining arm cannot win it at
all. **G2 is the secondary defence**, catching the residual case where M wins the primary while still
answering materially less often. A G2 pass is therefore informative about *coverage parity*, not about
whether abstention was rewarded — that question is already settled by the endpoint's construction.

### 6.2 G4's terminal must not be quoted alone

As ME-X2's receipt records, the gap-null terminal `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL` fires
both when M ties B5 **and** when B5 strictly beats it.

### 6.3 Integrity: per-instance and global

**Per-instance:** a rung the reference cannot settle has no ground truth and is excluded from the
primary, with the exclusion rate reported; a campaign whose model call failed is marked `cannot_check`,
excluded, and counted.

**Global** — these route the **whole study** to `CANNOT_CHECK` rather than reporting a primary on the
residue: unsettled fraction > 0.05; pooled model-arm failure rate > 0.05; any of `SIMPLE_DIRECT` /
`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` / `M_ME_FRONTIER_CONTROL` above 0.10; design sha256 changed
after freeze; non-monotone ground truth in any block; a recorded channel-identity violation.
Comparisons are strict — exactly at a threshold passes.

---

## 7. Pre-registered routing

Evaluated in this order; **`CANNOT_CHECK` pre-empts every scientific route**.

1. **`CANNOT_CHECK`** — an integrity or G0 gate fails; or an M advantage is not attributable by
   omission (G3); or **a null at an inadequate MDE**.
2. **`FRONTIER_RESIDUAL_CANDIDATE`** — G1 fires, G2 passes, G3 passes.
3. **`RESOURCE_EFFICIENCY_RESIDUAL_ONLY`** — G1 fires but G2 fails: M leads while answering materially
   less often, so the advantage is not distinguishable from answering less.
4. **`PARENT_SUFFICIENT`** — G1c fires, or a null **at an adequate MDE**.

### 7.1 Power, and the binding underpowered rule

Connor (1987) paired-binary normal approximation, in a frozen stdlib-only module that reproduces the
SD70-V2 reference value `paired_sample_size(0.1, 0.3) = 234`.

- registered minimum effect **0.15**, set from what this design can actually see at the affordable n,
  not from what would be desirable;
- at n = 150 the MDE is **0.124 / 0.152 / 0.175** for discordance 0.30 / 0.45 / 0.60;
- **binding rule:** if the observed discordance implies an MDE above 0.15, **a null routes
  `CANNOT_CHECK`, not `PARENT_SUFFICIENT`.** An underpowered null must never be reported as a third
  parent-sufficiency result it has not earned.

**The power is matched to the hypothesis, not to the budget.** The frontier hypothesis is that
epistemic control earns its keep precisely where no planner can compute the answer at budget. If that
is true at all, the effect should be **large**. An effect small enough to need ~29 000 calls to detect
would not support *"the framework solves frontier problems"* even if it were real. So a design powered
for 0.15 is well matched to the claim under test, and a null at that MDE is interpretable rather than
merely quiet.

**Scale caveat on the ME-X2 comparison.** ME-X2's decisive difference was 0.020, which this design
could not see. That is a useful *scale reference*, not a like-for-like target: it came from an exact
deterministic study with zero model calls and therefore no model variance, whereas this design has
model calls in the loop. Comparing the two MDEs directly would compare a noiseless estimator with a
noisy one.

---

## 8. Custody and protected-run discipline

The protected seed lives in operator custody at `~/.orion-custody/frontier/PROTECTED_SEED_V1.txt`
(mode 600); its sha256 is published in the design JSON. The runner verifies the hash before any
protected generation. `protected` refuses without an authorization file (exit 3) and without a matching
custody seed (exit 4), and invokes `analyze` once in the same invocation. The authorization is archived
immediately after the run so the guard re-arms.

**Determinism, honestly.** Campaign generation, the toolbox, the reference pass and all scoring are
byte-deterministic from the seed. **Model responses are not.** This study has model arms and cannot
claim byte-identical re-runs. Every call is logged with its prompt sha256, response body, requested
model, served-model triad, token count and wall time, so the **analysis** is exactly reproducible from
the frozen call log even though a re-dispatch would differ. Stated rather than papered over.

The outcome receipt must present, **per campaign**, the arm's claim, what it actually verified, and the
oracle verdict **side by side**, so a reader can audit an individual laundering call rather than trust
an aggregate.

---

## 9. Non-goals, no-rescue clause, resolved ambiguities

1. **No-rescue.** After any protected outcome is inspected: no change to the generator, block geometry,
   alphas, budget, K, calibration ladder or window, arm control text, toolbox, warrant rules, gates,
   thresholds, seeds, campaign counts, aggregation or routing. No post-hoc rung change. A protected
   result is never re-run under a new seed. A defect found after outcome access requires a new run
   identity (ME-F1 R2) with its own frozen design and seed commitment; this V1 result is immutable.
2. **Development tuning surface**, exhausted before freeze and disclosed in the parent-fidelity
   receipt: block geometry, the calibration rung, arm-glue defects, and the schema shape. Three defects
   were found on the development split and are recorded in the feasibility table §7 — endpoint
   saturation under a single ladder, calibration on a proxy endpoint, and the unclaimable final action.
3. **Levels 5–6 are out of scope by registration** (§2.4).
4. **Openness is bounded-resource openness**, not undecidability (§2.5).
5. **Prompt-difference risk is registered** (§4.2) and its remedy is the routing rule, not an assurance.
6. This study grants **no** field status, novelty or publication authority. Parent sufficiency is a
   valid terminal.

---

*No field status, novelty or publication authority is granted or implied.*
