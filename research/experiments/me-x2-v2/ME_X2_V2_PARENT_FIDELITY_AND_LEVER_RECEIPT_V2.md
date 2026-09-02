# ME-X2 V2 — Provenance, Parent Fidelity, Lever Known-Answer and Development Receipt (V2)

**Design:** `ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.{md,json}` (this PR).
**Status:** frozen design + lever known-answer fixtures + development split.
**No protected outcome has been generated or inspected.**
`PROTECTED_RUN_AUTHORIZATION.json` is absent; the `protected` stage refuses
(exit 3 / 4 / 5; asserted by `tests/unit/test_me_x2_v2_revival_study.py`). The
authorization file requires a **human-written** token: this lane is delivered
**frozen and armed**, and the protected run is an operator action. "Re-test
against the strongest parent on a fresh protected seed" is what the design
commits to and what the runner will do on the committed seed — it is not
something this PR skipped and not something an agent may authorize.

**Run:** Mac (local), 2026-09-02. `python3 mex2v2_run.py selftest`, `dev`, and
the optional `g0scale` public probe. Selftest and the 48-instance development
split complete in < 1 s wall each; the 1 200-instance three-arm probe took 5.5 s.
Results and custody files byte-identical across two consecutive runs (asserted in
the unit tests). This lane's 23 tests: 2.8 s; run in one session with the V1
test file in both orders (module-name collision surface checked), 46 tests, all
pass.

## 1. Frozen code (sha256)

| file | sha256 |
|---|---|
| `mex2v2_levers.py` | `9cfc1304c36616a03d6847c492bd66747fa13d1df08c8d6732b4704b04900f02` |
| `mex2v2_arms.py` | `458c8fa09589a1519c2ce6a10dbeb591f30bb5f0cbb05789c6a98dbd79166364` |
| `mex2v2_provenance.py` | `ac9e54c7d6079298d7a0c9a3154e8839d2e9097b412f6725ab95af87986c2517` |
| `mex2v2_run.py` | `274c8a64d50b5ddd665dbe932491634383080af06caa285d5f75635eb6c61ebc` |
| `ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.json` | `9ea8c8cd890a0f2e2df1395e58a49f10708e5b0a48f13474c9044fba61a800de` |
| `ME_X2_V2_LEVER_KNOWN_ANSWER_FIXTURES_V2.json` | `d0f75302f7c342966e2c3c8410bb22d54df91c6e5aba10ca45d9402ff1ddf21a` |
| `results/ME_X2_V2_DEVELOPMENT_RESULTS_V2.json` | `533b38af3f8965b3ae34f43f21a66bdfa5073b6502ed6465790fcd452f209485` |
| `results/ME_X2_V2_DEVELOPMENT_EXPECTED_CUSTODY_V2.json` | `cb7d75876ae4a5169ab301689e07db1a6bedace83d1e077a3fc1292c64b03131` |

Protected seed commitment (sha256 of the custody seed string):
`f85372cf187678f7517dcf73d41d6595add7dfd4ed04b6c218e08bb1854646fe` — a fresh
seed, never used by V1 or by V1's discarded dry run, held at
`~/.orion-custody/me-x2-v2/PROTECTED_SEED_V2.txt` (mode 600, outside the
repository). A protected run requires `acknowledged_design_sha256` = the
design-JSON hash above and the V2-specific env override
`MEX2V2_PROTECTED_SEED_FILE`, so a V2 run can never consume V1's committed seed.

## 2. G0d — the V1 lane is imported, never edited

Every frozen V1 file is byte-identical to the hash published in
`../me-x2/ME_X2_PARENT_FIDELITY_RECEIPT_V1.md` §1: `mex2_model.py`,
`mex2_catalogue.py`, `mex2_oracle.py`, `mex2_generator.py`, `mex2_parents.py`,
`mex2_arms.py`, `mex2_run.py` and the V1 design JSON
(`bb63685c…`). **8/8 match.** The V2 lane adds files in its own directory and
touches nothing in `me-x2/`. V1's protected run is complete (PR #164, main
`776d3a1`, route `PARENT_SUFFICIENT (B5_DOMINATES)`, `M` 0.963 vs `B5` 0.983,
p = 0.0032, all 43 of `M`'s losses false `CANNOT_IDENTIFY`); its artifacts are
immutable, are **read by no V2 module** — asserted by a unit test — and are not
re-scored here.

The comparator side of the study is therefore not a re-implementation: the unit
tests assert that `B5`, every ladder rung, every parent, both controls and V1's
`M` are the **same Python classes** the V1 lane froze. `M2` subclasses V1's `M`
and overrides exactly two methods; `_receipt`, `_dispositions`, `_escalate`,
`_apply`, `_disposition_action`, `act`, `live`, `declare` and `cannot_identify`
are asserted to be the *identical function objects* as V1's, so
`assess_discrepancy_locus`, `route_frontier_action`, `assess_jump` and
`minimum_level` are reached exactly as V1 reaches them. With both lever switches
off, `M2` reproduces V1's `M` trajectory for trajectory on every stratum.

## 3. Parent fidelity (21/21 PASS) and G0a

Every comparator passed its own native known-answer tests before use
(`mex2_parents.fidelity_selftests`, unchanged from V1: GDE, VoI, exact planner,
minimal separating-total sequencing, abstention, taxonomy, MDA).

- **G0a:** V1's 14 hand-authored fixtures reproduced by the oracle, with `M2`
  **and** `B5` decision-correct on every one and `M2` showing no false
  escalation and no specification damage.
- **Separation pair (H-EXT-3):** the verdict-only rung emits identical decisions
  on `SEP-P` and `SEP-Q` and fails one of them; structure exchange (`B5` rung 5)
  and `M2` are decision-correct on both.
- **G0b / G0c** on the generated selftest split: enumeration = branch-and-bound
  and uniform decidability on every instance; variant invariants hold; the
  null-calibration clauses hold with the swap null computed against **`M2`**, the
  arm under test (V1's `swap_null_M` is deliberately dropped by `score_v2` so no
  V2 gate can silently read the wrong arm).

## 4. Lever known-answer fixtures (6/6 PASS) — the diagnosed failure and its repair

`ME_X2_V2_LEVER_KNOWN_ANSWER_FIXTURES_V2.json` freezes six episodes verbatim
(truth included, generator-independent), located by scanning the public seed
`ME-X2-V2-FIXTURE-SEARCH-20260902` (144 instances) for the V1 signature: `M`
declares a **false `CANNOT_IDENTIFY`** where the oracle level exists. Six of 144
instances show it; every one is a false `CANNOT_IDENTIFY` with **no** false
escalation, reproducing V1's diagnosis on an independent public seed.

| fixture | oracle level | V1's `M` | `M2` | L1 only | L2 only |
|---|---|---|---|---|---|
| `LEVER-REC-01` | 0 | false CI | **correct** | ✗ | ✓ |
| `LEVER-REC-02` | 2 | false CI | **correct** | ✗ | ✓ |
| `LEVER-REC-03` | 5 | false CI | **correct** | ✗ | ✓ |
| `LEVER-REC-04` | 1 | false CI | **correct** | ✗ | ✓ |
| `LEVER-RES-01` (registered limit) | 5 | false CI | not rescued | ✗ | ✗ |
| `LEVER-RES-02` (registered limit) | 5 | false CI | not rescued | ✗ | ✗ |

**The two registered limits are frozen as expected failures.** The fixture pins
the boundary of the claim, not only the win: if a later change rescues one, the
test fails and the lane must be re-frozen.

**Hand check (`LEVER-REC-01`).** Live: `TARGET_SHIFT_REFIT` (minimal fix
`refit_post_t0`, level 0, cost 2), `MISSING_COVARIATE` (`measure_covariate`,
level 0, cost 2), `STALE_CACHE` (`refresh_cache`, level 1, cost 4); budget 6.
`covariate_availability` (1) separates `MISSING_COVARIATE`;
`provenance_freshness_audit` (2) separates `STALE_CACHE`; so
1 + 2 + 2 = 5 ≤ 6 establishes the truth and applies its level-0 fix — oracle
class `NO_ESCALATION_NEEDED`, locus `TARGET_WORLD`, level 0, cost 2, identifiable
and probe-identifiable, exactly as frozen. V1's `M` probes
`covariate_availability`, and at the next step its fail-closed rule refuses
`provenance_freshness_audit` because the `STALE_CACHE` branch would leave a
4-cost fix against 3 remaining units — so it abstains with 5 units unspent.
Under L2 the branch that refutes the best hypothesis is a defeat rather than a
foreclosure, the probe is admissible, and `M2` reaches the level-0 fix. Every
fixture's oracle targets are additionally reproduced by both oracle
implementations (enumeration and branch-and-bound).

**Which lever does what (development, registered before the protected run).**

- **L2 is the recovering lever:** alone it recovers all four recoverable
  fixtures; L1 alone recovers none of them.
- **L1 is the protecting lever:** alone, L2 spends budget on the cheapest
  admissible action it has newly unlocked and *loses* instances V1 kept — 0.917
  vs 1.000 on the 48-instance V2 development split, and 19 false
  `CANNOT_IDENTIFY` against V1's 6 on the 144-instance fixture-search surface.
  With L1 ordering the newly admissible actions, the conjunction loses none.
- Neither lever alone is both, which is what G5(b) tests on the protected split.

## 5. Development split (48 instances, public seed `ME-X2-V2-DEV-20260902`)

Not protected evidence.

| arm | decision | class | false esc. | missed esc. | false CI | spec dmg | mean regret |
|---|---|---|---|---|---|---|---|
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 0.979 | 0.875 | 1 | 0 | 0 | 0 | 2.88 |
| `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION` (V1) | 1.000 | 0.896 | 0 | 0 | 0 | 0 | 3.25 |
| **`M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS`** | **1.000** | 0.896 | 0 | 0 | 0 | 0 | 3.23 |
| `M2_L1_LOOKAHEAD_ONLY` | 1.000 | 0.896 | 0 | 0 | 0 | 0 | 3.23 |
| `M2_L2_BEST_HYPOTHESIS_ONLY` | 0.917 | 0.896 | 0 | 4 | 4 | 0 | 1.65 |
| `B3_MODEL_BASED_DIAGNOSIS_VOI` | 0.729 | 0.750 | 4 | 4 | 0 | 0 | 2.38 |
| `B3_EQUAL_EXTRA_SEARCH_1_5X` | 0.792 | 0.792 | 8 | 0 | 0 | 0 | 4.73 |
| `B2_FAILURE_TAXONOMY_DIAGNOSIS` | 0.292 | 0.458 | 24 | 12 | 0 | 1 | 4.90 |
| `M2_MINUS_LOCUS_DIAGNOSIS` | 0.625 | 0.646 | 0 | 18 | 18 | 0 | −4.68 |
| `M2_LOCUS_LABELS_SHUFFLED` | 0.354 | 0.125 | 2 | 26 | 4 | 0 | −0.05 |
| `M2_MINUS_DIAGNOSTIC_EVALUATOR_GATE` | 0.938 | 0.833 | 3 | 0 | 0 | 0 | 3.23 |
| `M2_MINUS_LOWER_LEVEL_DISPOSITION` | 0.896 | 0.854 | 3 | 2 | 2 | 0 | 3.43 |
| `M2_MINUS_PROSPECTIVE_DISCRIMINATOR` | 0.750 | 0.917 | 0 | 12 | 12 | 0 | 4.13 |
| `M2_ALWAYS_ESCALATE_WHEN_STUCK` | 0.208 | 0.646 | 37 | 15 | 15 | 6 | 7.70 |
| `M2_NEVER_ESCALATE` | 0.604 | 0.896 | 0 | 19 | 19 | 0 | −3.68 |
| `C_RANDOM_POLICY` | 0.271 | 0.021 | 8 | 30 | 14 | 2 | −1.15 |
| `C_NEVER_INTERVENE` | 0.167 | 0.167 | 0 | 40 | 40 | 0 | −8.08 |

(Full table, per stratum and per variant, in
`results/ME_X2_V2_DEVELOPMENT_ANALYSIS_V2.md`.)

**The development split cannot discriminate the levers.** V1's `M` is already
perfect on it (1.000), so `M2` matches it exactly, G5 is `LEVERS_NULL`, and the
route is `PARENT_SUFFICIENT` ("no `M2` advantage over `B5`"). That is the correct
reading of a saturated development surface, not a result. The levers show
themselves only where V1's rendering fails, which is what §4's frozen fixtures
are for. Ladder rung rates 0.729 → 0.896 → 0.917 → 0.979 → 0.979 (monotone);
G2 holds against both `B5` and V1's `M` (0 false escalations, 0 specification
damage); cost `COST_PARITY` (6 / 11, sign-test p = 0.33); `M2` vs `B5` decision
identity 0.667 — reported, never required.

**Lever activity on development:** 18 of 48 instances contain a step where the
prospective abstention term is positive (so L1's leading term is not degenerate),
15 contain a step where L1 changes the choice V1's cheapest-first order would
make, and 0 contain an action admissible only under L2 — on a surface with this
much budget slack, L2 never has to bite, which is precisely why the fixtures of
§4 exist. Attribution counts only receipts whose step matches the **executed**
trajectory step: V1's inherited `act()` consults the discriminator ranking before
its unique / common-fix branches, so a receipt can describe a candidate `M2` only
considered. The filter is not inert — it removes 2 of 322 receipts on the
144-instance fixture surface and 6 of 2 486 at 1 200-instance scale (0 of 100 on
this development split) — and left in, it could only ever inflate G5(c).

**G0c note.** The random control scores 0.271 on this 48-instance split
(0.178 on the 1 200-instance probe below, 0.202 on V1's discarded dry run). The
0.25 clause is an n-sensitive frequency claim about a 1 200-instance split and is
registered as enforced on the protected split and on the scale probe, reported
below that split size — exactly how V1 already treats decoy coverage. The
never-intervene clause (0 correct on 40 identifiable instances) and the `M2` swap
null (0.125 against `M2`'s 1.000) are hard at every label and both hold.

## 6. G0 coverage at protected scale (public seed, V1-known arms only)

`python3 mex2v2_run.py g0scale --public-seed ME-X2-V2-G0SCALE-PUBLIC-20260902`
generated 1 200 instances and ran **only** `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION`,
`C_RANDOM_POLICY` and `C_NEVER_INTERVENE` — the V2 arms are excluded by
construction, so the probe reveals nothing about the V2 comparison. **PASS:**
enumeration = branch-and-bound and uniform decidability on all 1 200; variant
invariants hold; decoys 20–112 per apparent class (all ≥ 5); inverse decoys 49 /
31 / 5 on the three level-0 classes; 18 apparent-`CANNOT_IDENTIFY` instances that
are in fact identifiable; `C_RANDOM_POLICY` 0.178; `C_NEVER_INTERVENE` 0 / 1 047
identifiable; V1's `M` 0.976 with a within-pair swap null of 0.203. Per-stratum
counts 51–272, matching V1's observed range.

**No protected-scale V2 dry run was executed, deliberately** (design §9). V1's
receipt documents why running the arms at scale before the protected run is
uncomfortable; the clauses that motivated V1's dry run are properties of the
generator, which G0d freezes byte-identical and which this probe re-checks.

## 7. Development-only work before the freeze, disclosed

1. **One lever-rendering repair.** L2 was first rendered as "some establishable
   hypothesis survives in **every** registered outcome branch". That is still
   fail-closed per branch, so it is not the registered lever, and on
   `LEVER-REC-01` it refuses the very probe that reaches the oracle level. It was
   corrected to the registered rule — the **best** live hypothesis remains
   establishable in the branch containing it — before the design was frozen. Both
   renderings are stated in design §2.2; the rejected one is registered there as
   an untried alternative.
2. **The L1 key ordering was authored before any V2 arm was executed**, from the
   diagnosed mechanism: abstention leads because abstention is the failure;
   foreclosure precedes discrimination because G2 is this lane's live risk; the
   tail is V1's own order so `M2` reduces to `M` under indifference. The
   alternative ordering is registered as untried.
3. **No gate, threshold, stratum weight, oracle rule, generator rule, seed or
   arm policy was changed in response to any development number.** The
   n-sensitivity note in §5 is a registration of *when* an inherited clause is
   enforced, made before the protected run and concerning the random control, not
   an arm under test.
4. **Two attribution repairs after the first freeze pass, before the PR.** The
   lever receipts were counting candidates that were only *considered*, which can
   only inflate G5(c), the one clause that makes the mechanism auditable; scoring
   now counts executed steps only (§5). And the lever verdict could return
   `LEVERS_RECOVER_M` with a mechanism rate of 0 because it never read G5(c);
   a distinct `LEVERS_NOT_ATTRIBUTED` verdict now sits ahead of both recovery
   verdicts. G5(b) was also loosened from `<` to `≤` — an aggregate tie between a
   single lever and the conjunction is a live possibility on this evidence and
   would have failed the clause for the wrong reason — and G5(b) is registered as
   a reported diagnostic while (a), (c) and (d) route the verdict.
5. **What the levers do not fix, diagnosed rather than tuned away.** The two
   registered-limit fixtures fail for a different reason than the four recovered
   ones: an action that is individually harmless leaves, two steps later, a
   warranted level-5 fix unaffordable (in `LEVER-RES-02`, `M2` spends 2 + 3 + 4
   of 29 units and the warranted fix costs 21; `B5` spends 3 + 5 and pays the 21
   exactly). No one-step rule can see that, and a rendering that could would be an
   exact planner — that is, `B5`. This is registered in design §1.3 as the
   pre-registered expectation, so that a horizon-shaped residual on the protected
   split reads as `PARENT_SUFFICIENT` with the residual **interface-standard, not
   control**, and not as a lever defect.

## 7b. Post-freeze factual amendment (V1's protected outcome)

This lane was authored from a checkout predating PR #164 and first described V1's
route from the registered expectation and the discarded pre-merge dry run. On
rebasing onto main, V1's protected outcome receipt was found and every
parent-lane description was corrected to cite it — which strengthens the lane's
premise, since the failure signature is now measured rather than predicted (43 of
43 of `M`'s losses are false `CANNOT_IDENTIFY`, 0 false escalations, 140/140
correct `CANNOT_IDENTIFY`).

**Nothing mechanical changed.** No lever, gate, threshold, stratum weight, arm,
seed or routing rule differs from the frozen version; V2's committed seed is
unrelated to V1's; and no V1 protected number informed any V2 design choice — the
levers, the L1 key ordering, the gates and the fixtures were all frozen and
committed before this amendment. V1's frozen code and design JSON are
byte-identical on main to the hashes G0d checks, which is why this is a
description change rather than a re-freeze. The design-JSON hash moved with the
text, and the table in §1 is the current one.

The correction was **found by this lane's own test**: `test_v1_lane_artifacts…`
asserted that V1 had no protected output, and it failed in CI against the merged
tree. The test now asserts the claim that actually matters — no V2 file writes
into the V1 directory, no V2 module reads V1's protected artifacts or seed, and
V1's frozen code is byte-identical.

## 8. Estimated protected-run cost

1 200 instances × 25 arms, deterministic, single core. Measured arm time on
development is 0.41 s for 48 instances × 25 arms, which extrapolates to ≈ 10 s of
arm time; generation and the exact oracle add ≈ 5 s at that scale (measured by
the three-arm probe). Estimate **≈ 15–60 CPU-seconds**; budget 5 CPU-minutes.
Mac local; never a heavy job; never CI on the Mac mini.

## 9. Authority

Development numbers are development numbers. Nothing here grants field status,
novelty, or publication authority. The route and lever verdict on the
development split are properties of a saturated 48-instance surface, not
predictions dressed as results. `PARENT_SUFFICIENT` is a successful scientific
terminal, and so is `LEVERS_NULL`. V1's result is immutable and untouched.
