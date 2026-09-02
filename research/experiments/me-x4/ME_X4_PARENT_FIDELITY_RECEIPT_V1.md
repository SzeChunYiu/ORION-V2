# ME-X4 — Parent Fidelity Receipt and Development-Split Summary (V1)

**Design:** `ME_X4_SELECTIVE_REOPENING_EXACT_STUDY_DESIGN_V1.{md,json}` (this PR).
**Status:** development fixtures only. **No protected outcome has been generated
or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent; the `protected`
stage refuses (exit 3/4; asserted by `tests/unit/test_me_x4_exact_study.py`).
**Run:** Mac (local), 2026-09-02, `python3 mex4_run.py selftest` then `dev`;
selftest + 36-instance development split complete in < 1 s wall each;
results and custody files byte-identical across two consecutive runs.

## 1. Frozen code (sha256)

| file | sha256 |
|---|---|
| `mex4_model.py` | `5772442823b185769dd775e913a7bcef48195f833d516bd6a60b039f3bfa6da3` |
| `mex4_oracle.py` | `9d387e3e97ae55f5d3a1689ab81512cbe9bc5766fb3c2f0472c1d1c8862f81ac` |
| `mex4_generator.py` | `d8a4cb8d9f4849bf5069f32ab6417d0e3b12d811b649c2b59c31c4946eac673e` |
| `mex4_parents.py` | `484213b497a51f8e1fc2a2df739b5ef218e76febce66a71e0e7d1aceade420b8` |
| `mex4_arms.py` | `967fc646ad61221b24038f89da39a8e2f21f45e7994df9d88c6c698c02da91a7` |
| `mex4_run.py` | `f58f4664267bd55027d64cf713bc4f959b7fa0ac42c64cefeceae7d87ae94fbf` |
| `ME_X4_SELECTIVE_REOPENING_EXACT_STUDY_DESIGN_V1.json` | `dd6c2602bc0759900e1659a8ad97a2d8e13e2df9969f689e322323f19b25b0cd` |
| `results/ME_X4_DEVELOPMENT_RESULTS_V1.json` | `ad2eeefa710749745f6e6f45201b0a0d87dfebd159a6bcef02acfd44ac9293e1` |
| `results/ME_X4_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `7a37fa0be1f73b1ce5d6fd776ca42143a799e43ce78295aded10319b64829c0c` |

Protected seed commitment (sha256 of the custody seed string):
`1314772902394af2583d924bc7eeb15f492e5aa8480dae3ac8cf9a93bfe12af9`.
A protected run requires `acknowledged_design_sha256` = the design-JSON hash above.

## 2. Parent fidelity: native known-answer tests (33/33 PASS)

Every comparator passed its own native tests before being used
(`mex4_parents.fidelity_selftests`, executed by `selftest` and by the unit test).

| parent | tests (all PASS) |
|---|---|
| JTMS (Doyle 1979; BPS ch. 7 algorithm) | propagation chain; well-founded `assumptions_of`; retraction propagates OUT; alternative justification restores; alternative support found after retraction; out-list default IN when q OUT / OUT when q IN / restored; circular support without premise stays OUT; dependency-directed contradiction handling records the nogood {A,B} and retracts the culprit (most recently enabled assumption) |
| ATMS (de Kleer 1986) | conjunction label {{A,B}}; disjunction {{A,B},{C}}; subsumption-minimal label; nogood removes inconsistent environments; `holds_in` over the environment lattice; premise empty environment |
| AGM / Hansson kernel contraction | closure; kernels are minimal derivations; success; inclusion; core-retainment; entrenchment cuts rules not evidence; downstream lost with contracted support; vacuity; atom contraction removes atom only; Levi revision |
| Noisy-OR support graph | arithmetic (1 − (1 − 0.81)(1 − 0.9) = 0.981); all-support-lost → REOPENED; envelope → UNRESOLVED; documented boundary: a 7-item family at r = 0.9 gives 0.478 < τ (generator caps families at ≤ 4 evidence) |
| Assurance case (GSN change impact) | solution change marks only its own strategy/goal suspect; context change marks the contextualised argument suspect |
| Provenance-only (`orion_v2.provenance`) | revocation descendants with component-tagged edges |

Scope note on the JTMS: conditional-proof justification installation (Doyle's
full DDB) is not implemented; X4 uses only monotone justifications, and the
culprit-retraction step is what the fidelity test exercises.

## 3. Selftest (G0a, separation, G0b, G0c): PASS

- G0a: 12/12 hand-authored fixtures reproduced by the oracle (two hand-authoring
  errors on prerequisite-only families were caught by the oracle during
  development and led to the frozen rule "prerequisite-only families carry no
  scope atom"; recorded here as the only semantic change made on development).
- Separation pair (H-EXT-3): verdict-only rung outputs `c = PRESERVED` on both
  P and Q (identical, blind to the difference) and errs on P; rung 5 and M give
  P → REOPENED, Q → PRESERVED. Exact check, executed.
- G0b: Kleene = exhaustive on every version of every generated instance.
- G0c: NEVER_REOPEN exact = 0 on all 23 instances requiring change; GLOBAL_RESET
  exact = 0 on all 23 mixed instances; RANDOM exact = 0.000; M vs
  within-instance shuffled oracle labels exact = 0.000 (n = 19).

## 4. Development split (36 instances, 3 per stratum; DEVELOPMENT — not protected)

Instance sizes: 4–9 claims, 5–16 families, 10–33 evidence units, 1–2 events.

| arm | instance exact | over | under | invalid pres. | false unres. | missed unres. | recovery (n=5) |
|---|---|---|---|---|---|---|---|
| A0_PROVENANCE_ONLY_INVALIDATION | 0.167 | 56 | 7 | 10 | 0 | 6 | 1.000 |
| A1_JTMS_CLASSICAL | 0.833 | 4 | 4 | 7 | 0 | 6 | 1.000 |
| A2_ATMS_CLASSICAL | 0.889 | 4 | 4 | 4 | 0 | 2 | 1.000 |
| A3_AGM_KERNEL_CONTRACTION | 0.833 | 4 | 4 | 7 | 0 | 6 | 1.000 |
| A4_BAYES_NOISY_OR | 0.861 | 5 | 4 | 4 | 0 | 2 | 1.000 |
| A5_ASSURANCE_CASE_UPDATE | 0.167 | 59 | 4 | 7 | 0 | 6 | 1.000 |
| B5_R1_VERDICT_ONLY | 0.972 | 0 | 1 | 1 | 0 | 0 | 1.000 |
| B5_R2_PROV | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 |
| B5_R3_PROV+DEP | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 |
| B5_R4_PROV+DEP+TRANS+EVAL | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 |
| **B5_STRONGEST_FAITHFUL_PARENT_FEDERATION** | **1.000** | 0 | 0 | 0 | 0 | 0 | 1.000 |
| **M_ME_SELECTIVE_REOPENING** | **1.000** | 0 | 0 | 0 | 0 | 0 | 1.000 |
| M_MINUS_DEPENDENCE_ANCESTRY | 0.944 | 0 | 4 | 4 | 0 | 0 | 1.000 |
| M_MINUS_TYPED_TRANSPORT | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 |
| M_MINUS_EVALUATOR_CONTRACT | 0.944 | 4 | 0 | 0 | 0 | 2 | 1.000 |
| M_MINUS_SUPPORT_FAMILIES | 0.333 | 49 | 0 | 0 | 5 | 0 | 1.000 |
| M_GLOBAL_RESET_CONTROL | 0.083 | 174 | 0 | 0 | 0 | 6 | 0.800 |
| C_NEVER_REOPEN | 0.361 | 0 | 31 | 37 | 0 | 6 | 1.000 |
| C_RANDOM_DISPOSITION | 0.000 | 60 | 23 | 12 | 89 | 4 | 0.000 |

**B5 exactly reproduces M's decisions on every development instance of every
stratum** (G1a decision identity 36/36 = 1.000; G1b discordant pairs = 0). On
development this predicts the pre-registered route **`PARENT_SUFFICIENT`** with
ladder terminal **`RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`** (G4 rung
exact rates 0.972 → 1.000 → 1.000 → 1.000 → 1.000; no step violation;
rung-5 gap null). G2 holds (M over-reopen 0 ≤ B5 0 on the conservative strata);
G3 not applicable (no claimed advantage).

Per-stratum attribution (where single parents break, development): provenance-
only and assurance over-reopen every redundantly supported claim (0.00 on 9 of
12 strata); untyped JTMS/AGM/ATMS/Bayes miss DEPENDENCE_DISCOVERED (0.33) and
over-reopen the evaluator sibling (0.67); two-valued JTMS/AGM score 0.00 on
CANNOT_CHECK_EDGE while ATMS and the noisy-OR envelope reach 0.67; the noisy-OR
arm fails one SOURCE_RETRACTED instance through reliability compounding along a
prerequisite chain (its native boundary). Ablations behave as their omission
predicts: minus dependence ancestry fails DEPENDENCE_DISCOVERED (0.33), minus
evaluator contract fails EVALUATOR (0.67) and CANNOT_CHECK (0.67), minus support
families over-reopens 49 commitments; minus typed transport was not separated
on development (the three transport instances defeat the witness either way;
the protected split's decoy variants are where this ablation is expected to bite).

Cost (wall-clock, laptop, 36 instances): M 9.96 ms vs B5 21.08 ms → ratio 2.12,
flag `COST_ADVANTAGE_M`. Engine op counts (M 4 607 analytic size proxy; B5
10 501 JTMS justification checks) are not commensurable and are reported only.
A 2× wall-clock difference on 36 tiny instances is a laptop timing, not a
claim; the design routes nothing on cost.

## 5. Estimated protected-run cost

1 200 instances × 20 arms, deterministic, single core: development throughput
(36 instances in ≈ 0.6 s including generation, 20 arms and analysis) extrapolates
to **≈ 20–60 CPU-seconds**; budget 3 CPU-minutes. Laptop billy or a LUNARC
login shell; never a heavy job; never CI on the Mac mini.

## 6. Pre-merge defect disclosure

Cursor Bugbot on PR #143 (commit `6c82097`) found that `AGMEngine._build`
assigned entrenchment only to family rules, leaving evidence atoms at the
default rank, so the kernel incision cut evidence instead of rules — the
inverse of the frozen `rules < evidence` policy. The native fidelity test had
passed because it supplied its own entrenchment map; the arm did not. Fixed
before merge (atoms and `neg:` atoms ranked 2, rules 1) with a regression test
(`test_agm_arm_incision_cuts_rules_not_evidence`). Development aggregates for
the AGM arm are unchanged (0.833); hashes above are post-fix. No gate,
constant or oracle rule changed.

## 7. Authority

Development numbers are development numbers. Nothing here grants field status,
novelty, or publication authority. The route above is a prediction of what the
frozen gates will say on the protected split, not a result.
