# ME-X2 — Parent Fidelity Receipt and Development-Split Summary (V1)

**Design:** `ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.{md,json}` (this PR).
**Status:** development fixtures only. **No protected outcome has been generated
or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent; the `protected`
stage refuses (exit 3/4; asserted by `tests/unit/test_me_x2_exact_study.py`).
**Run:** Mac (local), 2026-09-02, `python3 mex2_run.py selftest` then `dev`;
selftest and the 48-instance development split complete in < 1 s wall each;
results and custody files byte-identical across two consecutive runs.
Full unit suite `python -m pytest -q tests/unit`: 73 s (this lane's 23 tests: 2 s).

## 1. Frozen code (sha256)

| file | sha256 |
|---|---|
| `mex2_model.py` | `f43462b2d50dda48e9a731ae8f1136807651c18c78a58bdfc10c2040d432db86` |
| `mex2_catalogue.py` | `f809870ae4a20c8df2a8a72db545684e99b64386e146b64997c7ba19c4b1f294` |
| `mex2_oracle.py` | `399a81568011ccfdf7ba69c5f70b69c697874a7d78971cf5c8f12ec390eba241` |
| `mex2_generator.py` | `70eba6705b02a67f9dde08d162c492324c8cac8d7fe66d3f898c398be2e66ef8` |
| `mex2_parents.py` | `211da544f95ffffa7eb381e67ca607f7fc6e29c0a48857e865268357d562b923` |
| `mex2_arms.py` | `fb56bedc5a00c4cf7889b338b867fbcc7557f979d184233c2738174b738342db` |
| `mex2_run.py` | `65886691b467c8b05b44789671dd2f3386678b216c5724a3f3a25d8039e3ff84` |
| `ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.json` | `51c708293faf8d16601cb64597b86d32270711f4d329c4545da84c1b1f993447` |
| `results/ME_X2_DEVELOPMENT_RESULTS_V1.json` | `fb6c55e058a857ad37f3972fb0cc2d0f34bf3d3cf45349f197f400aed281a520` |
| `results/ME_X2_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `451eb5b4d997bd550585c52df9c66c34e9238e82dc724524a811bb786100b3eb` |

Protected seed commitment (sha256 of the custody seed string):
`4860b800dd43818f2c030c41746abec41068b1a7e998bd17208c5914b1390528`.
A protected run requires `acknowledged_design_sha256` = the design-JSON hash above.

## 2. Parent fidelity: native known-answer tests (21/21 PASS)

Every comparator passed its own native tests before being used
(`mex2_parents.fidelity_selftests`, executed by `selftest` and by the unit test).

| parent | tests (all PASS) |
|---|---|
| GDE consistency-based diagnosis (de Kleer & Williams 1987) | one observation eliminates exactly the inconsistent hypothesis; two observations intersect candidate sets; the *designed* table trusts the scientific evaluator while the effective table does not (the meta-evaluator separation, at the parent level); an intervention recurrence eliminates the hypotheses it resolves |
| Myopic VoI / rational metareasoning (Howard 1966; Russell & Wefald 1991) | expected cost of the best immediate act (hand-computed 13.0); a perfect probe's value (13 − 5.5 − 2 = 5.5); a non-splitting probe's value = −cost |
| Exact test-and-repair planner (Kalagnanam & Henrion 1990 style, exact by enumeration) | cheap repair-as-test first when 3 + 0.5·8 < 8; a perfect 1-cost probe first when 1 + 0.5·3 + 0.5·8 = 6.5; the τ gate admits a level ≥ 2 act only when it resolves the whole candidate set; no admissible act → declare at the failure penalty; a budget-infeasible act is excluded |
| Minimal separating-total sequencing | a repair resolving the target is its own test and fix; the probe route when no repair resolves it; unaffordable → None |
| Selective prediction / abstention (Chow 1970; Geifman & El-Yaniv 2017) | posterior below τ abstains; a class shared by every candidate reaches τ |
| ARFT-equivalent process-failure taxonomy | every registered pattern maps to an intervention kind of its template; standard fix first, then ascending level; the `NO_MAPPING` pattern is retained as a hostile counterexample to universality |
| MDA-style model expansion (arXiv:2608.09696 style) | expansion fires only after a criticism rejection *and* with a model-locus candidate live |

**Scope note.** ARFT (arXiv:2608.14905) is not licensed or executed here; B2 is
an equivalently strong pattern → standard-fix taxonomy with complete trajectory
access, which is the strongest form the addendum permits without the external
artifact. Registered as a limitation in the design before any outcome.

## 3. Selftest (G0a, separation, G0b, G0c): PASS

- **G0a:** 14/14 hand-authored fixtures reproduced by the oracle, and M and B5
  are decision-correct on every one. The fixtures cover every registered
  obstruction class as a truth, both `NO_ESCALATION_NEEDED` shapes (a local
  repair after a decoy symptom; a warranted stop when the criterion is already
  met), the `SAME_FIX` case (class and level identified, **locus**
  `CANNOT_IDENTIFY`) and a full `CANNOT_IDENTIFY` terminal.
- **Separation pair (H-EXT-3):** the verdict-only rung emits the identical
  decision sequence on P and Q (`expand_model_family`) and therefore errs on P,
  where the level-1 repair is the oracle minimum; rung 5 and M are
  decision-correct on both (P → `fix_unit_conversion`; Q → the level-1 repair as
  a disposition, then `expand_model_family`). Exact check, executed.
- **G0b:** bitmask enumeration = branch-and-bound on every instance; a
  truth-agnostic decision-correct policy exists on every instance; variant
  invariants hold.
- **G0c:** `C_NEVER_INTERVENE` decision-correct 0/41 on identifiable instances;
  `C_RANDOM_POLICY` 0.208 (≤ 0.25); **M scored against the partner instance's
  oracle 0.083 vs its true 1.000** — the within-pair label-swap null, which is
  the sharpest available: the two instances are byte-identical except for the
  hidden truth.

## 4. Development split (48 instances, 2 pairs per stratum; DEVELOPMENT — not protected)

| arm | decision (primary) | class | locus | success | false esc. | missed esc. | false CI | correct CI | recur. | spec dmg | mean regret | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `B0_RETRY_SEARCH` | 0.188 | 0.146 | 0.250 | 0.188 | 1 | 32 | 0 | 0/7 | 117 | 0 | −2.34 | 0.4 |
| `B1_UNCERTAINTY_ABSTENTION` | 0.729 | 0.875 | 0.875 | 0.583 | 0 | 13 | 13 | 7/7 | 0 | 0 | 3.54 | 1.5 |
| `B2_FAILURE_TAXONOMY_DIAGNOSIS` | 0.250 | 0.500 | 0.562 | 0.479 | 25 | 19 | 0 | 0/7 | 80 | 1 | 3.73 | 0.7 |
| `B3_MODEL_BASED_DIAGNOSIS_VOI` | 0.812 | 0.812 | 0.812 | 0.854 | 5 | 2 | 0 | 0/7 | 8 | 0 | 3.27 | 2.8 |
| `B3_EQUAL_EXTRA_SEARCH_1_5X` | 0.854 | 0.854 | 0.854 | 0.938 | 5 | 0 | 0 | 0/7 | 5 | 0 | 4.41 | 2.9 |
| `B4_MDA_MODEL_EXPANSION` | 0.750 | 0.771 | 0.771 | 0.812 | 8 | 4 | 0 | 0/7 | 11 | 0 | 3.71 | 2.4 |
| `B5_R1_VERDICT_ONLY` | 0.688 | 0.688 | 0.688 | 0.708 | 5 | 8 | 0 | 0/7 | 6 | 0 | 2.24 | 1.0 |
| `B5_R2_PLUS_CANDIDATE_SET` | 0.875 | 0.917 | 0.917 | 0.729 | 0 | 6 | 6 | 7/7 | 3 | 0 | 2.24 | 0.9 |
| `B5_R3_PLUS_DISCRIMINATOR_TABLES` | 0.979 | 0.958 | 0.958 | 0.833 | 0 | 1 | 1 | 7/7 | 29 | 0 | 3.15 | 14.4 |
| `B5_R4_PLUS_DISPOSITION_RECORDS` | 0.979 | 0.958 | 0.958 | 0.833 | 0 | 1 | 0 | 7/7 | 32 | 0 | 3.15 | 12.0 |
| **`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`** | **1.000** | 0.979 | 0.979 | 0.854 | 0 | 0 | 0 | 7/7 | 31 | 0 | 3.10 | 11.4 |
| `B5_NO_ABSTENTION_GATE` | 0.875 | 0.875 | 0.875 | 0.896 | 6 | 0 | 0 | 5/7 | 36 | 0 | 2.98 | 29.8 |
| **`M_ME_LOCUS_PLUS_MINIMUM_ESCALATION`** | **1.000** | 0.938 | 0.938 | 0.854 | 0 | 0 | 0 | 7/7 | 16 | 0 | 3.49 | 34.6 |
| `M_MINUS_LOCUS_DIAGNOSIS` | 0.583 | 0.625 | 0.583 | 0.438 | 0 | 20 | 20 | 7/7 | 46 | 0 | −4.24 | 10.1 |
| `M_LOCUS_LABELS_SHUFFLED` | 0.250 | 0.146 | 0.250 | 0.125 | 3 | 35 | 9 | 6/7 | 29 | 0 | −1.29 | 78.4 |
| `M_MINUS_DIAGNOSTIC_EVALUATOR_GATE` | 0.917 | 0.854 | 0.854 | 0.896 | 4 | 0 | 0 | 5/7 | 19 | 0 | 3.49 | 35.9 |
| `M_MINUS_LOWER_LEVEL_DISPOSITION` | 0.917 | 0.854 | 0.854 | 0.896 | 4 | 0 | 0 | 5/7 | 7 | 0 | 4.17 | 26.0 |
| `M_MINUS_PROSPECTIVE_DISCRIMINATOR` | 0.938 | 0.875 | 0.875 | 0.792 | 0 | 3 | 3 | 7/7 | 4 | 0 | 5.46 | 38.8 |
| `M_ALWAYS_ESCALATE_WHEN_STUCK` | 0.271 | 0.604 | 0.625 | 0.625 | 34 | 16 | 16 | 2/7 | 46 | 5 | 7.02 | 27.0 |
| `M_NEVER_ESCALATE` | 0.646 | 0.938 | 0.938 | 0.500 | 0 | 17 | 17 | 7/7 | 16 | 0 | −2.71 | 32.6 |
| `C_NEVER_INTERVENE` | 0.146 | 0.146 | 0.146 | 0.000 | 0 | 41 | 41 | 7/7 | 0 | 0 | −7.63 | 0.1 |
| `C_RANDOM_POLICY` | 0.208 | 0.104 | 0.104 | 0.333 | 17 | 27 | 13 | 4/7 | 29 | 3 | 1.27 | 1.9 |

(Regret is measured against the oracle minimum in registered cost units and is
negative for arms that fail cheaply — a reason it routes nothing on its own.)

**B5 and M are both decision-correct on every development instance of every
stratum** (0 discordant pairs; G1b diff 0.000, p = 1.0). On development this
predicts the pre-registered route **`PARENT_SUFFICIENT`** with ladder terminal
**`RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`** (G4 rung decision rates
0.688 → 0.875 → 0.979 → 0.979 → 1.000, no step violation, rung-5 gap null).
G2 holds (M false escalation 0 ≤ B5 0; specification damage 0 ≤ 0); G3 not
applicable (no claimed advantage); cost `COST_PARITY` (M lower regret on 5
instances, B5 on 11, sign-test p = 0.21).

**G1a is *false* on development** (decision-sequence identity 0.646) while both
arms are perfect: M and B5 reach the same minimum-level interventions by
different routes — B5 plans the whole sequence to minimise expected cost, M
disposes of the registered lower level first and then routes a Jump. The
pre-registered routing already handles this: no advantage in either direction
⇒ `PARENT_SUFFICIENT`. Sequence identity is reported, never required.

**Where the parents break (attribution, development).** `B0` never reaches a
level ≥ 2 warranted intervention (0.188, 117 recurrences). `B2`, the
ARFT-equivalent taxonomy, is the clearest hostile-decoy casualty: it escalates
on the symptom, 25 false escalations and 0.250 overall, with 0.14 on
`SEARCH_INSUFFICIENT` and 0.20 on `NO_ESCALATION_NEEDED` — pattern → standard
fix is exactly what the decoys punish. `B1` abstains correctly (7/7
`CANNOT_IDENTIFY`) but abstains too often (13 false `CANNOT_IDENTIFY`). `B3`
(GDE + VoI) is strong (0.812) but myopic: it commits where a two-step plan is
needed and scores 0.00 on the `CANNOT_IDENTIFY` stratum, which it has no
terminal for. `B4` inherits B3 and adds 3 further false escalations from
criticism-driven expansion. The `1.5×` extra-search control reaches 0.854 —
matched extra budget does not recover the gap to 1.000, which is what G3(c)
prices on the protected split.

**Ablations behave as their omission predicts.** Removing locus diagnosis costs
0.417 (0.583; 20 missed escalations); shuffling locus labels collapses the arm
to 0.250, below the random control's class accuracy; removing the
diagnostic-evaluator gate converts an undiscriminated locus into a forced
attribution (4 false escalations, 0.917); removing the lower-level disposition
does the same by a different route (4 false escalations); removing the
prospective discriminator wastes budget on non-splitting probes (0.938, mean
regret 5.46 vs 3.49); always-escalate-when-stuck is the worst arm in the study
on escalation harm (34 false escalations, **5 specification damages** — the only
arm besides the random control to reformulate an objective that was not wrong);
never-escalate keeps a perfect class rate (0.938) with 17 missed escalations,
the exact shape of "label well, act uselessly" the ARFT addendum warns about.

## 5. Estimated protected-run cost

1 200 instances × 22 arms, deterministic, single core: development throughput
(48 instances including generation, 22 arms and analysis in ≈ 0.6 s)
extrapolates to **≈ 20–60 CPU-seconds**; budget 5 CPU-minutes. Mac local; never
a heavy job; never CI on the Mac mini.

## 6. Development-only repairs (before any protected outcome)

Three defects were found and fixed on development, each validated by the G0a
known-answer tests before the seed is revealed. Recorded here because the design
permits arm-glue repair only on development:

1. **Truth-dependent instances.** The first generator admitted pairs whose
   oracle target was unreachable without knowing the answer. Fixed by the
   **uniform-decidability** admission rule (§2.4 of the design): a single
   truth-agnostic policy tree must be decision-correct for every live cause.
2. **Failure penalty too small.** With the failure penalty equal to the budget,
   every expected-cost parent preferred to declare rather than pay for a
   warranted high-level fix. Frozen at 10× budget for every expected-cost arm,
   B5 included — a change that strengthens the comparator.
3. **M's resource leak.** M's first reserve rule checked only that the *fix*
   stayed affordable, so M could spend the episode out of reach of the very
   intervention its diagnosis warranted (3 instances). Replaced by the
   fail-closed **reachability rule** now registered as part of M in design §4.1.

No gate, stratum weight, oracle rule, arm or seed changed after the design JSON
was written; the design hash above is the one a protected run must acknowledge.

## 7. Authority

Development numbers are development numbers. Nothing here grants field status,
novelty, or publication authority. The route above is a prediction of what the
frozen gates will say on the protected split, not a result.
