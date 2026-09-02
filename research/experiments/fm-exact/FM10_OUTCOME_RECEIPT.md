# FM10 — Finite Relational Mapping: Protected-Run Outcome Receipt (V1)

**Design:** `FM10_FINITE_RELATIONAL_MAPPING_EXACT_STUDY_DESIGN_V1.{md,json}` (PR #173, main `e4ce1f9`), design-JSON sha256 `ae23f7cfba5409ec200d90051834260041521e12510520e7b7c2920a6332d90d`.

**Authorization:** coordinator authorization under the operator's standing instruction, in chat, 2026-09-02, verbatim *"run all the computation tasks.. finish all the researxh asap"*. Recorded in `PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` — the file the runner consumed as `PROTECTED_RUN_AUTHORIZATION.json`, archived under a new name after the single run so the runner's guard is re-armed; content and sha256 unchanged (`61a2bb6b289f0279ae8da12e61b51945ec56c728ea42308be06c272c33060d72`). It carries the design sha256 and the seed commitment.

**Run:** Mac (local), 2026-09-02, `python3 fm_run.py FM10 protected`, **executed exactly once**, exit 0, 0.77 s wall. The runner verified sha256(custody seed) = the frozen commitment `b630beec4e60723caa3435b8c06754ecc184f66b2fc0787d27430979e4e447a4` before generating, and `analyze` ran once inside the same invocation. Code unchanged from main. **No post-outcome change to any design constant, gate, arm, oracle rule or seed.**

**Seed reveal (per design §7):** `FM10-PROTECTED-a9aa70234f651a2be06b5e95369629d3caedcd7b680e3e2b` — sha256 equals the commitment above; the 126-instance split regenerates byte-for-byte from it.

**Artifacts (sha256):** results `e2556b000e4db6d637807d83ab1c369f4b6f11d8bcd4e3f0861325969cf131c8`; expected-custody `7fdb3a53e2cf6361b9f33a74a174f1dd7929290fc940884a1b5264dfad3fb59b`; analysis json `333f6592b19b3fcd875a27fd7320bf3650fc543590e5a284cd57c67c9dac7b54`, md `a350a5b0cd2e1e9d768a4128279d7424b632c54a2e98dfd9000334bb879b41ec`; timing `22905e43de68e195a90860a8d7d3575cc1c5b58fe16f87185ad0a5ede50f1375`; selftest report (G0a/G0e source) `08fa50bc18324dc855b97820b2bc703d2931026b3acaf6acda094c973dd74a0c`.

## 1. Terminal

```text
FM10_STATUS            = EXECUTED_PROTECTED
ROUTE                  = PARENT_SUFFICIENT
PRIMARY_COMPARATOR     = F0_PARENT_FEDERATION
COST_FLAG              = COST_ADVANTAGE_PARENT (wall-clock ratio 3.14; reported, no route)
FIELD_STATUS_AUTHORITY = NONE
```

**Finite relational mapping is parent-owned.** On 126 protected instances across all seven families, the pre-registered parent federation reproduces `M`'s disposition **identically on every instance** (decision identity 126/126; 0 discordant pairs; exact two-sided p = 1.0; Wald CI [0, 0]). Holm across the seven per-family paired tests: every adjusted p = 1.0.

## 2. Gates (frozen pre-outcome; every verdict carries its own denominator)

| gate | verdict | violations / evaluated | numbers |
|---|---|---|---|
| **G0a KNOWN_ANSWER** (hard) | **PASS** | 0 / 11 fixtures | 11 hand-authored fixtures reproduced by the exhaustive oracle and by the independent cross-check |
| **G0b ORACLE_SELF_AGREEMENT** (hard) | **PASS** | 0 / 126 instances | exhaustive enumeration = branch-and-bound on disposition, min_missing, optimal profile, optimal-map count and broken invariants, on every instance |
| **G0c NULL_CALIBRATION** (hard) | **PASS** | 0 / 4 checks | C_ALWAYS_TRANSFER 0.286, C_ALWAYS_BLOCK 0.286, C_RANDOM 0.190, M vs within-split shuffled oracle labels 0.262 (all ≤ 0.40) |
| **G0d DECOY_COVERAGE** (hard) | **PASS** | 0 / 4 decoy families | 18 instances in each of the four decoy families (minimum 3) |
| **G0e PLANTED_POSITIVES** (hard) | **PASS** | 0 / 5 trip-wires | all five fired in the same execution that reports the zeros |
| **G0f FAMILY_DISCRIMINATION** (hard) | **PASS** | 0 / 2 halves | *solvable*: best arm 1.000 ≥ 0.95 over 11 non-control arms; *separating*: four registered weak arms at 0.571 / 0.611 / 0.429 / 0.429, all ≤ 0.85 |
| **G1a PARENT_REPRODUCES_M** (hard) | **PASS** | 0 / 126 instances | decision identity 1.000; 0/18 discordant in every family; **liveness control**: the same counter registered 73, 54, 18 and 2 disagreements for the four ablation arms |
| **G1b M_ADVANTAGE** (detector) | **NOT_FIRED** | — / 126 | paired diff 0.000, 0 discordant pairs, exact p = 1.0 |
| **G2 ANTI_PERMISSIVENESS** (hard) | **PASS** | 0 / 90 oracle-blocked instances | M over-accepts 0 ≤ F0 over-accepts 0 |
| **G3 MECHANISM_BY_OMISSION** | **NOT_APPLICABLE** | 0 / 0 | no claimed advantage |
| COST | flag only | — | M 37.7 ms vs F0 12.0 ms wall → `COST_ADVANTAGE_PARENT` |

Generator rejections (published, not hidden): `SURFACE_DECOY` 135, `ISOMORPHIC_TRANSFER` 1, `PARTIAL_HOMOMORPHISM` 1, `DIRECTION_REVERSAL` 1, others 0. The decoy family rejects heavily because a random relabelling frequently leaves the surface correspondence valid, which would not be a decoy.

## 3. Per-arm outcomes (126 instances)

| arm | exact | rate | over-accept | under-accept |
|---|---|---|---|---|
| **`F0_PARENT_FEDERATION`** | **126/126** | **1.000** | 0 | 0 |
| **`M_F2_TRANSFER_DISCOVERY_FULL`** | **126/126** | **1.000** | 0 | 0 |
| `M_MINUS_TYPE_DISCIPLINE` | 124/126 | 0.984 | 2 | 0 |
| `M_MINUS_INVARIANCE_TEST` | 108/126 | 0.857 | 18 | 0 |
| `P2_COMPLETE_HOMOMORPHISM` | 108/126 | 0.857 | 18 | 0 |
| `P1_SME_STRUCTURE_MAPPING` | 104/126 | 0.825 | 18 | 0 |
| `P0_SURFACE_SIMILARITY` | 77/126 | 0.611 | 15 | 23 |
| `M_MINUS_RELATIONAL_MAPPING` | 72/126 | 0.571 | 0 | 18 |
| `P3_FIXED_LESSON_INJECTION` | 54/126 | 0.429 | 18 | 18 |
| `P4_INVARIANCE_PARENT` | 54/126 | 0.429 | 68 | 0 |
| `M_MINUS_OBSTRUCTION_SEARCH` | 53/126 | 0.421 | 0 | 30 |
| `C_ALWAYS_BLOCK` | 36/126 | 0.286 | 0 | 36 |
| `C_ALWAYS_TRANSFER` | 36/126 | 0.286 | 90 | 0 |
| `C_RANDOM_DISPOSITION` | 24/126 | 0.190 | 14 | 30 |

## 4. Per-family exact rate (18 instances each)

| arm | ISO | PARTIAL | NON_HOM | SURFACE_DECOY | REVERSAL | RELTYPE | INVARIANT_BREAK |
|---|---|---|---|---|---|---|---|
| `P0_SURFACE_SIMILARITY` | 0.72 | 1.00 | 1.00 | 0.00 | 0.78 | 0.78 | 0.00 |
| `P1_SME_STRUCTURE_MAPPING` | 1.00 | 1.00 | 1.00 | 1.00 | 0.83 | 0.94 | 0.00 |
| `P2_COMPLETE_HOMOMORPHISM` | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| `P3_FIXED_LESSON_INJECTION` | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `P4_INVARIANCE_PARENT` | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 |
| **`F0_PARENT_FEDERATION`** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **`M_F2_TRANSFER_DISCOVERY_FULL`** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| `M_MINUS_RELATIONAL_MAPPING` | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| `M_MINUS_INVARIANCE_TEST` | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| `M_MINUS_OBSTRUCTION_SEARCH` | 0.11 | 1.00 | 1.00 | 0.22 | 0.28 | 0.11 | 0.22 |
| `M_MINUS_TYPE_DISCIPLINE` | 1.00 | 1.00 | 1.00 | 1.00 | 0.89 | 1.00 | 1.00 |

## 5. Reading (within the frozen gates; no reinterpretation)

- **The parent federation is sufficient, exactly.** `M` adds nothing: 0 discordant pairs out of 126. Unlike an earlier draft in which `M` and `F0` shared an implementation, this is a measurement — `M` runs its own greedy-plus-local-search alignment which is not guaranteed to reach the optimum, and the G1a liveness control shows the same counter registering 73, 54, 18 and 2 disagreements for the ablation arms on this very split. The zero is a zero the counter was capable of not reporting.
- **No single parent reaches the endpoint, and the two boundaries are complementary.** `P2` (complete typed homomorphism search) is exact on all six fact-level families and **0.00 on the invariant family**; `P4` (invariance parent) is 1.00 on the invariant family and 0.00 on four of the six mapping families, over-accepting 68 transfers. Their pre-registered composition is exact. That decomposition — which parent owns which obstruction class — is FM10's actual content.
- **Where the weaker parents break.** Surface similarity fails every decoy (0.00) and, unexpectedly, 28% of plain isomorphic transfers, because a name-similar map is not always the structurally valid one. `P1` SME reaches 0.825: its greedy gmap merge, which is the published algorithm, costs it 17% of the reversal family and 6% of the relation-type family — it commits to a locally systematic correspondence and does not backtrack. The fixed-lesson table is 0.429, failing every decoy family outright.
- **Ablations behave as their omissions predict**, and each omission is load-bearing for `F0` exactly as much as for `M`: removing the invariance test costs precisely the invariant family (18 over-accepts, nothing else); removing relational alignment costs the three alignment-sensitive decoy families; removing obstruction search collapses to 0.421 because an arbitrary first typed map is usually not the optimal one. Removing type discipline costs only 2 instances — the weakest of the four ablations, and nothing is claimed from it.
- **Cost is against the mechanic.** `M` is ≈ 3× *slower* than the federation (37.7 ms vs 12.0 ms for 126 instances): its restarts-and-local-search costs more than a complete branch-and-bound at these sizes. Reported as a flag; the design routes nothing on cost.
- **Two results in the tables are definitional, and are labelled as such rather than read as findings.** `P2` is the branch-and-bound oracle algorithm minus the invariant check, so its 1.00/0.00 split is by construction; and `SURFACE_DECOY` instances are rejected unless the surface correspondence is genuinely invalid, so `P0`/`P3` scoring 0.00 there is definitional. The `G0f` *solvable* half is likewise satisfied by `F0`, whose exactness follows from composing two complete predicates — the informative half of that gate is *separating*, which four independent weak arms satisfy.

## 6. Kill conditions (protocol §8) — status

| condition | outcome |
|---|---|
| strongest formal parent matches F2 at lower cost | **yes on both counts**: identical decisions, and the federation is ≈ 3× faster → parent-owned |
| fixed lesson injection matches F2 at lower cost | no: fixed lessons reach 0.429 |
| formal abstraction increases false analogy or loses native validity | no: M over-accepts 0 on 90 oracle-blocked instances (G2 pass) |
| categorical/formal machinery helps only where the parent already solves the case | consistent with the observed decomposition; no separate residual |

## 7. Programme consequence

`FM10_STATUS = PARENT_SUFFICIENT`. ORION's L2 transfer-discovery loop for finite relational mapping contracts to **the pre-registered composition of two mature parents** — a complete typed relational homomorphism search and an invariance check — with no control residual and a cost disadvantage. This is the fourth sibling exact study to find the strongest faithful parent sufficient (after ME-X1, ME-X2, ME-X4).

It also supersedes nothing and *repairs* something: the FM/FG R2 `fm10` cell scored 1.000 for all five arms and could not have detected a difference. This run separates fourteen arms across a 0.190–1.000 range under a gate that would have failed the run had it not.

No field status, novelty, F2 superiority or publication authority is granted or implied. A formal witness does not establish empirical truth.

## 8. Custody

The authorization file (archived as `PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json`, byte-identical to the one consumed) and `fm10/results/FM10_PROTECTED_*` are archived in this PR (force-added past the `.gitignore` that guards against unauthorized commits). The live path `PROTECTED_RUN_AUTHORIZATION.json` is absent again, so `fm_run.py FM10 protected` refuses (exit 3) and the design-time single-run invariant test holds; a second protected run would require a new, explicit authorization. The custody seed file remains in operator custody at `~/.orion-custody/fm/FM10_PROTECTED_SEED_V1.txt`; its value is now public (above) and the split is reproducible by anyone from the frozen code on `e4ce1f9`.

skills-applied: none (outcome receipt, no manuscript content)
