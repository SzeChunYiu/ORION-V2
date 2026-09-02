# ME-X2 — Obstruction/Locus Classification and Minimum Escalation: Protected-Run Outcome Receipt (V1)

**Design:** `ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.{md,json}` (PR #157, main `704d379`), design-JSON sha256 `bb63685c02da55e7c7ebdf72541e862bcc92661b07a1074e33b8371a35e5d7c9`.
**Authorization:** operator, in chat, 2026-09-02, verbatim *"run all the computation tasks.. finish all the researxh asap"*, recorded in `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` (sha256 `3a133ad46ac36107f992052e3da3873481411fcc2c9075c301ed4e6f8e15d9e7`; carries the design sha256, the seed commitment and the main sha). The same instruction is the primary record for the sibling ME-X1 and ME-X4 protected runs.
**Run:** Mac (local), 2026-09-02, `python3 mex2_run.py protected` from the merged tree, **executed exactly once**, exit 0, 18.6 s CPU for 1 200 instances × 22 arms. The runner verified sha256(custody seed) = the frozen commitment `4860b800dd43818f2c030c41746abec41068b1a7e998bd17208c5914b1390528` before generating; `analyze` ran once inside that same invocation. Every code file hashed identical to the parent-fidelity receipt table before the run. **No post-outcome change to any design constant, gate, threshold, arm policy, oracle rule, generator rule or seed.**

**Seed reveal (per design §3):** `ME-X2-PROTECTED-79bb1d14da1829efaabde6d7c519ae243b85738d75e2af69` — sha256 equals the commitment above; the 1 200-instance split regenerates byte-for-byte from it.

**Artifacts (sha256):** results `33961a3df74711d9e3bd080a141bcab4b436005600aca74d28ebfe86e5260cd9`; expected-custody `19f4656232a38c893a72c0cd4808660521dd17363e872a2143f2fb78c3834919`; timing `a5032746b6420d2fe7f15e8b45abfbc7ce6a30f29ca52dcc17312bccb0cffcb1`; analysis json `e11a1e8fd3092a9f3a414da90bd9d8f17b84e4b208edbedf80f8414f95493c84`, md `b113c61af08c309851a46892bfb3aa6303bdf19b08524c5f43aceb5db4922578`; selftest report (G0a source, unchanged from main) `d678091c484ed960fb1fd5b43246b7226c113744585aa6237cd01268ecf39e5d`.
Determinism was verified byte-for-byte on the **development** split; the protected split is a single run by design and was not re-run.

## 1. Terminal

```text
ME_X2_STATUS              = EXECUTED_PROTECTED
ROUTE                     = PARENT_SUFFICIENT (B5_DOMINATES)
PRIMARY_ENDPOINT          = INTERVENTION_DECISION_AND_OUTCOME
M_MINIMAL_LEVEL_DECISION  = 0.963
B5_MINIMAL_LEVEL_DECISION = 0.983   (paired diff -0.020, exact p = 0.0032)
LADDER_TERMINAL (H-EXT-3) = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL  [see S5 caveat]
COST_FLAG                 = COST_ADVANTAGE_B5 (per-instance regret sign test; M's MEAN regret is lower)
PRIMARY_COMPARATOR        = B5_STRONGEST_FAITHFUL_PARENT_FEDERATION
FIELD_STATUS_AUTHORITY    = NONE
```

**The strongest faithful parent federation is better than M at choosing the minimum responsible intervention**, on the primary endpoint, at the pre-registered significance level. `PARENT_SUFFICIENT` is a successful terminal of this design (§1.2 of the design, protocol V2 "Parent sufficiency is a successful scientific terminal") — but this is its *stronger* form: not a tie, a loss.

## 2. Gates (frozen pre-outcome; all numbers from `results/ME_X2_PROTECTED_ANALYSIS_V1.json`)

| gate | verdict | numbers |
|---|---|---|
| **G0a KNOWN_ANSWER** (hard) | **PASS** | 14/14 hand-authored fixtures + separation pair reproduced; parents 21/21 native tests (selftest report on main) |
| **G0b ORACLE_SELF_AGREEMENT** (hard) | **PASS** | enumeration = branch-and-bound and a truth-agnostic decision-correct policy on all 1 200; variant invariants hold; decoys 10–110 per apparent class (rule ≥ 5); inverse decoys ≥ 5 on every level-0 class (39 / 10 / 62); 17 apparent-`CANNOT_IDENTIFY` instances in fact identifiable |
| **G0c NULL_CALIBRATION** (hard) | **PASS** | `C_NEVER_INTERVENE` 0/1 060 on identifiable instances; `C_RANDOM_POLICY` 0.2075 (rule ≤ 0.25); within-pair oracle-swap null for M 0.183 vs its true 0.963 (rule ≤ 0.663) |
| **G1a B5_REPRODUCES_M** | not met | decision-*sequence* identity 0.666 — reported, never required (§4 below) |
| **G1b M_ADVANTAGE** | **not fired** | paired diff −0.020; 19 M-only vs 43 B5-only correct; exact p = 0.0032 |
| **G1c B5_ADVANTAGE** | **PASS** | the symmetric test fires: B5 dominates, 95% CI [−0.033, −0.007] |
| **G2 ANTI_ESCALATION** | **PASS** | M false escalations **0** vs B5's **21**; specification damage 0 vs 0 |
| **G3 MEDIATION** | not applicable | no M advantage to mediate |
| **G4 INTERFACE_LADDER** | **PASS** (monotone) | 0.690 → 0.800 → 0.858 → 0.945 → 0.983; every step a significant improvement (p < 0.001), no violation |
| COST | flag only | per-instance regret sign test: B5 lower on 237, M lower on 161, p = 0.00016 → `COST_ADVANTAGE_B5`. **M's mean regret is nevertheless lower** (3.05 vs 3.47) and M's mean cost is lower (10.27 vs 10.61) — the two disagree, see §5 |

## 3. Per-arm outcomes (1 200 instances; §5 of the design)

| arm | decision (primary) | class | locus | success | false esc. | missed esc. | false CI | correct CI | recur. | spec dmg | false world | mean regret | wall ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `B0_RETRY_SEARCH` | 0.218 | 0.102 | 0.312 | 0.223 | 15 | 798 | 0 | 0/140 | 2766 | 0 | 0 | -3.35 | 11 |
| `B1_UNCERTAINTY_ABSTENTION` | 0.593 | 0.752 | 0.800 | 0.478 | 1 | 487 | 487 | 139/140 | 0 | 0 | 9 | 2.10 | 44 |
| `B2_FAILURE_TAXONOMY_DIAGNOSIS` | 0.356 | 0.476 | 0.468 | 0.606 | 517 | 389 | 0 | 0/140 | 1670 | 18 | 63 | 3.59 | 17 |
| `B3_MODEL_BASED_DIAGNOSIS_VOI` | 0.777 | 0.789 | 0.792 | 0.830 | 116 | 107 | 5 | 20/140 | 257 | 5 | 34 | 2.98 | 77 |
| `B3_EQUAL_EXTRA_SEARCH_1_5X` | 0.854 | 0.857 | 0.857 | 0.969 | 163 | 1 | 0 | 1/140 | 228 | 8 | 35 | 4.47 | 83 |
| `B4_MDA_MODEL_EXPANSION` | 0.772 | 0.794 | 0.792 | 0.828 | 128 | 112 | 5 | 19/140 | 271 | 6 | 19 | 2.99 | 66 |
| `B5_R1_VERDICT_ONLY` | 0.690 | 0.693 | 0.694 | 0.719 | 93 | 229 | 0 | 0/140 | 207 | 7 | 29 | 2.04 | 26 |
| `B5_R2_PLUS_CANDIDATE_SET` | 0.800 | 0.838 | 0.855 | 0.702 | 18 | 223 | 223 | 135/140 | 245 | 4 | 10 | 1.59 | 28 |
| `B5_R3_PLUS_DISCRIMINATOR_TABLES` | 0.858 | 0.848 | 0.868 | 0.762 | 20 | 151 | 151 | 134/140 | 852 | 3 | 14 | 1.73 | 713 |
| `B5_R4_PLUS_DISPOSITION_RECORDS` | 0.945 | 0.911 | 0.891 | 0.867 | 37 | 31 | 4 | 121/140 | 884 | 13 | 28 | 3.15 | 584 |
| **`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`** | **0.983** | 0.949 | 0.932 | 0.887 | 21 | 0 | 0 | 135/140 | 829 | 0 | 28 | 3.47 | 564 |
| `B5_NO_ABSTENTION_GATE` | 0.897 | 0.887 | 0.873 | 0.922 | 123 | 3 | 3 | 91/140 | 884 | 6 | 32 | 3.33 | 1763 |
| **`M_ME_LOCUS_PLUS_MINIMUM_ESCALATION`** | **0.963** | 0.923 | 0.902 | 0.846 | **0** | 45 | 45 | **140/140** | 470 | 0 | 20 | 3.05 | 1156 |
| `M_MINUS_LOCUS_DIAGNOSIS` | 0.483 | 0.492 | 0.479 | 0.367 | 0 | 620 | 620 | 140/140 | 990 | 0 | 15 | -5.25 | 336 |
| `M_LOCUS_LABELS_SHUFFLED` | 0.300 | 0.150 | 0.241 | 0.210 | 70 | 808 | 290 | 111/140 | 664 | 0 | 31 | -1.43 | 2439 |
| `M_MINUS_DIAGNOSTIC_EVALUATOR_GATE` | 0.910 | 0.882 | 0.873 | 0.894 | 79 | 25 | 24 | 85/140 | 542 | 2 | 22 | 3.55 | 1172 |
| `M_MINUS_LOWER_LEVEL_DISPOSITION` | 0.895 | 0.884 | 0.880 | 0.892 | 98 | 30 | 30 | 100/140 | 266 | 7 | 24 | 4.05 | 862 |
| `M_MINUS_PROSPECTIVE_DISCRIMINATOR` | 0.843 | 0.834 | 0.843 | 0.733 | 7 | 181 | 181 | 140/140 | 229 | 0 | 6 | 4.48 | 1222 |
| `M_ALWAYS_ESCALATE_WHEN_STUCK` | 0.253 | 0.635 | 0.652 | 0.592 | 848 | 431 | 431 | 59/140 | 1249 | 115 | 30 | 6.85 | 886 |
| `M_NEVER_ESCALATE` | 0.568 | 0.923 | 0.919 | 0.452 | 0 | 518 | 518 | 140/140 | 470 | 0 | 0 | -3.22 | 1169 |
| `C_NEVER_INTERVENE` | 0.117 | 0.117 | 0.129 | 0.000 | 0 | 1060 | 1060 | 140/140 | 0 | 0 | 0 | -7.84 | 3 |
| `C_RANDOM_POLICY` | 0.207 | 0.072 | 0.092 | 0.237 | 285 | 790 | 405 | 61/140 | 750 | 70 | 114 | 0.60 | 54 |

(Regret is against the oracle minimum in registered cost units; it is *negative* for arms that fail cheaply, which is why it routes nothing on its own.)

## 4. Per-stratum decision-correct rate (stratum = oracle class)

| stratum | n | B0 | B2 taxon. | B3 VoI | B4 MDA | R1 | **B5** | **M** | −locus | shuffled | always-esc | never-esc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CANNOT_IDENTIFY | 140 | 0.00 | 0.00 | 0.06 | 0.06 | 0.00 | 0.96 | **1.00** | 1.00 | 0.79 | 0.00 | 1.00 |
| FORMALISM_OR_OPERATOR_INSUFFICIENT | 55 | 0.02 | 0.22 | 0.91 | 0.89 | 0.69 | 1.00 | 1.00 | 0.09 | 0.15 | 0.13 | 0.00 |
| MEASUREMENT_OR_EVALUATOR_BLIND | 63 | 0.00 | 0.00 | 0.75 | 0.75 | 0.25 | **1.00** | 0.89 | 0.06 | 0.27 | 0.59 | 0.00 |
| MISSING_PREMISE_OR_DATA | 91 | 0.55 | 0.37 | 0.93 | 0.91 | 0.92 | 0.99 | 1.00 | 0.69 | 0.19 | 0.14 | 1.00 |
| MODEL_FAMILY_INADEQUATE | 113 | 0.07 | 0.63 | 0.92 | 0.96 | 0.91 | 0.92 | **0.98** | 0.24 | 0.21 | 0.42 | 0.00 |
| NO_ESCALATION_NEEDED | 277 | 0.30 | 0.34 | 0.82 | 0.82 | 0.77 | 0.99 | 0.95 | 0.64 | 0.22 | 0.20 | 0.95 |
| PROBE_ACTION_INSUFFICIENT | 71 | 0.32 | 0.45 | 1.00 | 1.00 | 0.90 | 1.00 | 0.94 | 0.75 | 0.17 | 0.00 | 0.94 |
| PROBLEM_OBJECTIVE_MISSPECIFIED | 80 | 0.00 | 0.05 | 0.82 | 0.78 | 0.65 | **1.00** | 0.90 | 0.07 | 0.26 | 0.29 | 0.00 |
| REPRESENTATION_INSUFFICIENT | 69 | 0.00 | 1.00 | 0.91 | 0.93 | 0.74 | 1.00 | 0.97 | 0.10 | 0.29 | 0.28 | 0.00 |
| SEARCH_INSUFFICIENT | 123 | 0.79 | 0.50 | 0.96 | 0.98 | 0.98 | 0.98 | 0.99 | 0.77 | 0.24 | 0.09 | 0.99 |
| TOOL_INSTRUMENT_INADEQUATE | 68 | 0.00 | 0.00 | 0.84 | 0.75 | 0.81 | **1.00** | 0.91 | 0.04 | 0.34 | 0.60 | 0.00 |
| WORKFLOW_INADEQUATE | 50 | 0.00 | 1.00 | 0.70 | 0.68 | 0.62 | 1.00 | 1.00 | 0.02 | 0.32 | 1.00 | 0.00 |

Per-stratum n is not 100: the stratum is the *oracle* class, so each receives its 50 anchored instances plus re-stratified partners (design §3, as corrected pre-merge).

## 5. Reading (within the frozen gates; no reinterpretation)

- **H0 (strongest-parent sufficiency) holds, in its strong form.** The information-matched federation — GDE consistency-based diagnosis, VoI/metareasoning, exact expected-cost test-and-repair sequencing, calibrated abstention, over the same typed modules — chooses the minimum responsible intervention on 0.983 of protected instances against M's 0.963, paired p = 0.0032. On the pre-registered routing this is `G1c` ⇒ **`PARENT_SUFFICIENT (B5_DOMINATES)`**.

- **The discordance has exactly one mechanism, with two signs.** Of the 62 discordant instances: **all 43 that B5 wins are M declaring `CANNOT_IDENTIFY` where the episode was in fact decidable**, and **all 19 that M wins are B5 escalating above the oracle level**. M's conservatism is not a separate virtue that happens to accompany a loss — it *is* the loss. It buys M `0` false escalations against B5's 21, `140/140` correct `CANNOT_IDENTIFY` against B5's `135/140`, and lower mean regret (3.05 vs 3.47), and it costs M 43 warranted interventions. G2 therefore passes **because** M abstains, and G1c fires for the same reason. Reading the gate row `G2 PASS` as "M is safe and merely slower" would invert the finding.

- **Why M abstains.** M's two orderings, registered in design §4.1 before the run because the ORION reference semantics fix neither: it takes the *cheapest* admissible discriminator (no lookahead), and its reachability rule is *fail-closed over every live hypothesis*. So M spends part of the budget on a weakly discriminating action, then correctly reports that nothing is establishable, and declares `CANNOT_IDENTIFY` — where the planner picks the discriminating test first and succeeds. This was seen in the pre-merge dry run on a public seed and deliberately **not** repaired (parent-fidelity receipt §6b); repairing it after observing that it loses would be tuning an outcome.

- **The G4 terminal label understates this result and must not be quoted alone.** `gap_null` is computed as ¬G1b, so `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL` fires both when M ties B5 *and* when B5 strictly beats it. Here it fires alongside `B5_DOMINATES` and is the weaker of the two statements. The ladder itself is informative and monotone — 0.690 → 0.800 → 0.858 → 0.945 → 0.983, **every** step a significant improvement (p < 0.001), with the final step (the diagnostic-evaluator contract, 45 instances, 0 regressions) the one that separates a federation trusting its scientific evaluator from one that does not. H-EXT-3's prediction (a) is confirmed on this suite: decision quality is monotone in what crosses the module boundary.

- **What the study does *not* license.** Uniform decidability guarantees a truth-agnostic decision-correct policy exists for every admitted instance, and strictly increasing cost bands make minimum-level ≡ minimum-cost. An exact expected-cost planner is therefore optimal for this objective **by construction**. The honest terminal is *"no ME residual is detectable in a registered decision problem the parents already solve exactly"*, not *"no ME residual exists"*. The registered limitations stand: synthetic ORION-authored episodes, registered outcome tables where real episodes carry unregistered hypotheses, ARFT represented by an equivalent taxonomy, a uniform prior shared by every arm.

- **Where the parents break (attribution).** `B0` 0.218 with 2 766 recurrences — retry cannot reach a warranted level ≥ 2. The **ARFT-equivalent taxonomy `B2` is the clearest hostile-decoy casualty: 0.356 with 517 false escalations and 18 specification damages**, 0.00 on `MEASUREMENT_OR_EVALUATOR_BLIND` and `TOOL_INSTRUMENT_INADEQUATE`, 0.05 on `PROBLEM_OBJECTIVE_MISSPECIFIED` — pattern → standard fix is precisely what a decoy punishes, which is the ARFT addendum's own warning turned into a measurement. `B1` abstains well (139/140) but 487 times too often. `B3` (GDE + VoI) reaches 0.777 but is myopic and scores **0.06 on the `CANNOT_IDENTIFY` stratum** — it has no warranted terminal for "the evidence does not decide". `B4` adds 12 further false escalations over B3 through criticism-driven expansion. **The matched extra-search control is decisive for the mechanism question: B3 at 1.5× budget reaches 0.854, still far below both M and B5 — the gap is not bought with search.**

- **Ablations behave as their omission predicts.** Removing locus diagnosis costs 0.480 (0.483, 620 missed escalations); shuffling the locus labels costs **more** — 0.663 (0.963 → 0.300) — so M's decisions ride on the labels being *correct*, not merely present. (Both ablations remain above the `C_RANDOM_POLICY` floor of 0.207; the evidence here is the size of the drop, not a floor comparison.) Removing the diagnostic-evaluator gate converts undiscriminated loci into forced attributions: 79 false escalations appear and correct `CANNOT_IDENTIFY` falls 140 → 85, the evaluator-laundering failure the protocol asks the gate to price. Removing the lower-level disposition: 98 false escalations. Removing the prospective discriminator: 181 missed escalations and the worst mean regret of any M variant (4.48). `M_ALWAYS_ESCALATE_WHEN_STUCK` is the worst arm in the study on escalation harm — **848 false escalations and 115 specification damages**, the only arm except the random control to reformulate objectives that were not wrong. `M_NEVER_ESCALATE` keeps M's class accuracy exactly (0.923) with 518 missed escalations: the "labels beautifully, acts uselessly" shape the ARFT addendum names, and the reason this study's primary endpoint is the intervention and not the label. It also isolates a fact about M worth stating: capped at level 1 it applies precisely M's 731 level-0 and 281 level-1 interventions and none of M's 473 level ≥ 2 ones, yet carries the *same* 470 recurrences — every recurrence M suffers happens in the lower-level disposition phase, and **none of M's escalations recur**. Once M escalates, it escalates to the right level.

## 6. Kill conditions (protocol V2) — status

| condition | outcome |
|---|---|
| B3/B5 matches or exceeds the locus/routing quality-cost frontier | **yes — B5 exceeds it.** Contract the ME-X2 residual |
| failure taxonomy + metareasoning reproduces the same interventions | no: B2 0.356, B3 0.777 vs M 0.963 — the parents that reproduce M are the *federation*, not the taxonomy |
| gains rely on protected oracle information | no: no arm imports the oracle (asserted by unit test); M uses only registered information |
| diagnostic-evaluator failure silently converted into a forced attribution | not by M (0 false escalations, 140/140 correct `CANNOT_IDENTIFY`); the ablation shows the gate is what prevents it |
| false escalation or semantic damage offsets gains | not for M (0 and 0); it is B5 that carries 21 false escalations |
| labels not discriminable at useful calibration | no: M class 0.923 / locus 0.902, B5 0.949 / 0.932 |

## 7. Programme consequence

`ME_X2_STATUS = PARENT_SUFFICIENT (B5_DOMINATES)`. On this registered decision problem the ORION witnessed-obstruction + minimum-escalation control layer does **not** produce a residual beyond an information-matched parent federation; it is measurably worse on the primary endpoint, and the shortfall is fully attributable to two conservative orderings the ORION semantics leave open rather than to the locus diagnosis itself — which the ablations show is load-bearing (−0.480 when removed, −0.663 when shuffled). Consistent with decisive-studies §4.8 and protocol V2's kill conditions, the X2 obstruction-control residual contracts.

Two revival levers are registered and queued as a separate V2 lane, not claimed here: one-step lookahead on discriminator choice, and a reachability rule that preserves the *best* live hypothesis rather than *every* one. A V2 must freeze its own design and seed before any protected run; this V1 result is immutable.

The naturalistic cell (protocol V2 §7 / design §9) remains a separate, unexecuted identity; nothing here transfers to it. No field status, novelty or publication authority is granted or implied.

## 8. Custody

`PROTECTED_RUN_AUTHORIZATION.json` was archived to `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` immediately after the run so the runner's guard is re-armed and the unit test asserting the refusal path continues to hold; a second protected run requires a new explicit authorization. `results/ME_X2_PROTECTED_*` are force-added past the `.gitignore` that guards against unauthorized commits. The custody seed file remains in operator custody; its value is now public (above) and the split is reproducible by anyone from the frozen code on main `704d379`.
