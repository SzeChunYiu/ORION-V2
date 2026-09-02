# FM20 — Anti-Unification and Generalization: Protected-Run Outcome Receipt (V1)

**Design:** `FM20_ANTI_UNIFICATION_EXACT_STUDY_DESIGN_V1.{md,json}` (PR #184, main `3e39eae`), design-JSON sha256 `ce97a64234f08d1c4657dc215e3a512c494982d310849cb753a7f1c22c591c98`.

**Authorization:** coordinator authorization under the operator's standing instruction, in chat, 2026-09-02, verbatim *"run all the computation tasks.. finish all the researxh asap"*. Archived as `PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM20.json` (byte-identical to the file consumed, sha256 `fd406aec344f41f7108e5647f6102fb2462434e09a3e4c16dd92537198118a0d`), carrying the design sha256 and the seed commitment.

**Run:** Mac (local), 2026-09-02, `python3 fm_run.py FM20 protected`, **executed exactly once**, exit 0. The runner verified sha256(custody seed) = the frozen commitment `2b4eb309a77211c7aabbf4eb0fd760c8a31842888574b5c3a00f64f3a1291aae` before generating; `analyze` ran once in the same invocation. **No post-outcome change to any design constant, gate, arm, oracle rule or seed.**

**Seed reveal:** `FM20-PROTECTED-39029e4d3da34a7ea8beecafb754e0e042e8c35fdba44aaa` — sha256 equals the commitment; the 125-instance split regenerates byte-for-byte, and identically under any `PYTHONHASHSEED`.

**Artifacts (sha256):** results `a756d1c7f94c31231675f6cdc4a0e056cf27030f2a0fee9939ff176a7fea6d49`; expected-custody `9d87a92aa87f71ba0b6f3f39593431338a3fa56e950cd9790f382516b99efda5`; analysis json `4861106dcfeec04484e108b70f3beebecbe9509da3131bf0b58cd57108484c75`, md `9147078047ca7b0bea096457e4c4fd98c8973797da29dc4755c8de6fa6d0738a`; timing `8a671f6db3c659aa96ea601db3a0ffcb9e257b74c9030312c4372e35979ae48c`.

## 1. Terminal

```text
FM20_STATUS            = EXECUTED_PROTECTED
ROUTE                  = PARENT_SUFFICIENT
PRIMARY_COMPARATOR     = F0_PARENT_FEDERATION
COST_FLAG              = COST_PARITY_WITHIN_2X (ratio 1.03)
FIELD_STATUS_AUTHORITY = NONE
```

**Abstraction induction is parent-owned.** On 125 protected instances the pre-registered parent federation reproduces `M`'s (disposition, held-out coverage) endpoint **identically on every instance** — 125/125, 0 discordant, exact two-sided p = 1.0, Holm-adjusted p = 1.0 in all five families — at equal cost.

## 2. Gates (frozen pre-outcome; every verdict with its own denominator)

| gate | verdict | violations / evaluated | numbers |
|---|---|---|---|
| **G0a KNOWN_ANSWER** | **PASS** | 0 / 10 fixtures | reproduced by the exhaustive lattice oracle and by Plotkin's algorithm |
| **G0b ORACLE_SELF_AGREEMENT** | **PASS** | 0 / 125 instances | lattice enumeration = anti-unification on disposition, LGG and coverage |
| **G0c NULL_CALIBRATION** | **PASS** | 0 / 4 checks | C_ALWAYS_ACCEPT 0.032, C_ALWAYS_REJECT 0.000, C_RANDOM 0.064, shuffled-label null 0.248 |
| **G0d DECOY_COVERAGE** | **PASS** | 0 / 4 decoy families | 25 instances each |
| **G0e PLANTED_POSITIVES** | **PASS** | 0 / 6 trip-wires | all fired in the same execution |
| **G0f FAMILY_DISCRIMINATION** | **PASS** | 0 / 2 halves | *solvable* best arm 1.000 over 10 non-control arms; *separating* four weak arms at 0.368 / 0.600 / 0.752 / 0.800 |
| **G1a PARENT_REPRODUCES_M** | **PASS** | 0 / 125 instances | identity 1.000; **liveness control** 79 / 25 / 25 / 21 ablation disagreements; per-family rule permits 1 discordant instance at n = 25 and 0 were observed |
| **G1b M_ADVANTAGE** | **NOT_FIRED** | — / 125 | 0 discordant pairs, exact p = 1.0 |
| **G2 ANTI_PERMISSIVENESS** | **PASS** | 0 / 50 oracle-rejected instances | M 0 ≤ F0 0; **liveness control** — on those same 50 instances `C_ALWAYS_ACCEPT` and `P1_PLOTKIN_LGG` each made 50 unsafe claims, `M_MINUS_NEGATIVE_CHALLENGE` 25 |
| **G3 MECHANISM_BY_OMISSION** | **NOT_APPLICABLE** | 0 / 0 | no claimed advantage |
| COST | flag only | — | M 2.96 ms vs F0 3.04 ms → parity |

Generator rejections, published per family: `LEAST_GENERAL_PATTERN` 18, `OVER_GENERALIZATION` 25, `UNDER_GENERALIZATION` 24, `NO_VALID_COMMON_ABSTRACTION` 4, `DISTRACTOR_REGULARITY` 0.

## 3. Per-arm outcomes (125 instances)

| arm | exact | rate | unsafe claims |
|---|---|---|---|
| **`F0_PARENT_FEDERATION`** | **125/125** | **1.000** | 0 |
| **`M_F2_ABSTRACTION_INDUCTION_FULL`** | **125/125** | **1.000** | 0 |
| `M_MINUS_VARIABLE_IDENTITY` | 104/125 | 0.832 | 0 |
| `M_MINUS_COMPRESSION_CRITERION` | 100/125 | 0.800 | 4 |
| `M_MINUS_NEGATIVE_CHALLENGE` | 100/125 | 0.800 | 25 |
| `P0_FIXED_LESSON_INJECTION` | 100/125 | 0.800 | 25 |
| `P2_CANDIDATE_ELIMINATION` | 100/125 | 0.800 | 4 |
| `P3_MDL_COMPRESSION` | 94/125 | 0.752 | 24 |
| `P1_PLOTKIN_LGG` | 75/125 | 0.600 | 50 |
| `M_MINUS_LEAST_GENERALITY` | 46/125 | 0.368 | 50 |
| `C_RANDOM_DISPOSITION` | 8/125 | 0.064 | 13 |
| `C_ALWAYS_ACCEPT` | 4/125 | 0.032 | 50 |
| `C_ALWAYS_REJECT` | 0/125 | 0.000 | 0 |

## 4. Per-family exact rate (25 instances each)

| arm | LEAST_GENERAL | DISTRACTOR | OVER_GENERAL | UNDER_GENERAL | NO_COMMON_ABSTRACTION |
|---|---|---|---|---|---|
| `P0_FIXED_LESSON_INJECTION` | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 |
| `P1_PLOTKIN_LGG` | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 |
| `P2_CANDIDATE_ELIMINATION` | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| `P3_MDL_COMPRESSION` | 0.96 | 0.84 | 0.00 | 0.96 | 1.00 |
| **`F0_PARENT_FEDERATION`** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **`M_F2_ABSTRACTION_INDUCTION_FULL`** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| `M_MINUS_VARIABLE_IDENTITY` | 1.00 | **0.16** | 1.00 | 1.00 | 1.00 |
| `M_MINUS_NEGATIVE_CHALLENGE` | 1.00 | 1.00 | **0.00** | 1.00 | 1.00 |
| `M_MINUS_COMPRESSION_CRITERION` | 1.00 | 1.00 | 1.00 | 1.00 | **0.00** |
| `M_MINUS_LEAST_GENERALITY` | 0.00 | 0.84 | 0.00 | 1.00 | 0.00 |

## 5. Reading (within the frozen gates; no reinterpretation)

- **The three parent boundaries are exactly complementary, and each is visible in its own column.** Plotkin's LGG is perfect on the three families its theory covers and **0.00** on both families that require a judgement its theory does not contain — over-generalization (no negative examples) and vacuity (no compression criterion). Candidate elimination repairs the first (1.00 on `OVER_GENERALIZATION`) and inherits the second (0.00 on vacuity). MDL repairs the second (1.00 on vacuity) and not the first (0.00 on over-generalization), and pays 0.84 on the distractor family because description length sometimes prefers to generalize a real shared regularity away. Their composition is exact. That decomposition is FM20's content.
- **`M` adds nothing to it.** 0 discordant pairs out of 125 at parity cost. The zero is measured: `M` is a cover-driven specific-to-general search that can variablise too high and diverge, and on this very split the same discordance counter registered 79, 25, 25 and 21 disagreements for the four ablation arms.
- **Every ablation is falsified exactly where its omission predicts, and nowhere else.** Removing variable identity costs the distractor family and only that family (0.16 — the family exists precisely to force a repeated variable). Removing the negative challenge costs only over-generalization (0.00) and produces 25 unsafe claims. Removing the compression criterion costs only vacuity (0.00). Removing least-generality collapses the study (0.368). Each omission is load-bearing for `F0` exactly as much as for `M`.
- **The safety endpoint has a real denominator.** On the 50 instances the oracle rejects, `M` and `F0` each made 0 unsafe claims — and the counter that produced those zeros registered 50 for `C_ALWAYS_ACCEPT`, 50 for `P1_PLOTKIN_LGG` and 25 for `M_MINUS_NEGATIVE_CHALLENGE` on the same instances. `P1`'s 50 is not a defect of the parent: anti-unification has no notion of a negative example, so within its own theory every LGG is acceptable.
- **Cost is a genuine tie** (2.96 vs 3.04 ms), unlike FM10 where the mechanic was 3× slower.

## 6. Kill conditions (protocol §8) — status

| condition | outcome |
|---|---|
| strongest formal parent matches F2 at lower cost | matched exactly, at parity cost → parent-owned |
| fixed lesson injection matches F2 at lower cost | no: fixed lessons reach 0.800 |
| formal abstraction increases false analogy or loses native validity | no: 0 unsafe claims on 50 in-scope instances (G2 pass, counter live) |

## 7. Programme consequence

`FM20_STATUS = PARENT_SUFFICIENT`. ORION's abstraction induction for symbolic generalization contracts to **the pre-registered composition of three mature criteria** — anti-unification, consistency with negatives, and a compression criterion — with no residual and no cost advantage. Fifth sibling exact study to find the strongest faithful parent sufficient, after ME-X1, ME-X2, ME-X4 and FM10.

The FM/FG R2 `fm20` cell reported 0.783 / 0.692 / 0.783 / 0.667 / 0.767 across its five model arms with no separation. This run separates thirteen arms across 0.000–1.000 and attributes every gap to a named missing criterion.

No field status, novelty, F2 superiority or publication authority is granted or implied.

## 8. Custody

The consumed authorization is archived under a new name so the runner's guard is re-armed; the live path is absent again and `fm_run.py FM20 protected` refuses (exit 3). A second protected run would require a new explicit authorization. The custody seed remains in operator custody; its value is public above and the split is reproducible from the frozen code on `3e39eae`.

skills-applied: none (outcome receipt, no manuscript content)
