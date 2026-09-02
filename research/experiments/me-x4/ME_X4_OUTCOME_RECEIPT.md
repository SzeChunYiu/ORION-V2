# ME-X4 — Selective Reopening under Dynamic Evidence: Protected-Run Outcome Receipt (V1)

**Design:** `ME_X4_SELECTIVE_REOPENING_EXACT_STUDY_DESIGN_V1.{md,json}` (PR #143, main `ee32108`), design-JSON sha256 `dd6c2602bc0759900e1659a8ad97a2d8e13e2df9969f689e322323f19b25b0cd`.
**Authorization:** operator, in chat, 2026-09-02, verbatim *"run all the computation tasks.. finish all the researxh asap"*, recorded in `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` (the file the runner consumed as `PROTECTED_RUN_AUTHORIZATION.json`, archived under a new name after the single run so the runner's guard is re-armed; content and sha256 unchanged `fc1f7b1ac47f3bbc523ab4756e431e7062708b8aa0e2bf678ec321cd94c40f41`; carries the design sha256 and the seed commitment).
**Run:** Mac (local), 2026-09-02 09:54 UTC, `python3 mex4_run.py protected --out results`, **executed exactly once**, exit 0, 18.6 s CPU; the runner verified sha256(custody seed) = frozen commitment `1314772902394af2583d924bc7eeb15f492e5aa8480dae3ac8cf9a93bfe12af9` before generating; `analyze` ran once inside the same invocation. Code unchanged from main (`mex4_run.py` `f58f4664…`, `mex4_arms.py` `967fc646…`). **No post-outcome change to any design constant, gate, arm, oracle rule or seed.**

**Seed reveal (per design §3):** `ME-X4-PROTECTED-4af0e016eac29b3757100c4807ecdba4e4bfad86ed31945a` — sha256 equals the commitment above; the 1 200-instance split regenerates byte-for-byte from it.

**Artifacts (sha256):** results `7bd0f8c20c037a2000ffafe2fe1809287b2dbdb0e299125c99b72df554a87117`; expected-custody `5ac9d3521d557220ef987d69b593c163a8e0863710af4e25b85e680ec856e708`; timing `20d9242de0ed98c94e78c3102176a314a5110e34ae2e586b39af0f3a42526775`; analysis json `5ae1b8ab5c7e926d68e5b1a28f28ff1b0e937c5100b10221529149f294431c14`, md `cb2d77bb7fbf8376a359e7d4f03f0531d413ec5213d64c6a6f98ddb771216d55`; selftest report (G0a source) `ad0ab7a2adfb7082ee7aa71d4ef438a4af90f714213329e17ff554523fe95f71`.

## 1. Terminal

```text
ME_X4_STATUS            = EXECUTED_PROTECTED
ROUTE                   = PARENT_SUFFICIENT
LADDER_TERMINAL (H-EXT-3) = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL
COST_FLAG               = COST_ADVANTAGE_M (wall-clock ratio 2.07; reported, no route)
PRIMARY_COMPARATOR      = B5_STRONGEST_FAITHFUL_PARENT_FEDERATION
FIELD_STATUS_AUTHORITY  = NONE
```

**Selective reopening is parent-owned.** On 1 200 protected instances across all 12 strata, the strongest faithful parent federation reproduces M's reopened / preserved / unresolved decisions **identically on every instance and every version** (decision identity 1 200/1 200; 0 discordant pairs). Per protocol §8 and decisive-studies §6.5, selective reopening remains an interface convention; per H-EXT-3, M's advantage over the federation is a monotone function of what crosses the module boundary and vanishes at full-structure exchange.

## 2. Gates (frozen pre-outcome; all numbers from `results/ME_X4_PROTECTED_ANALYSIS_V1.json`)

| gate | verdict | numbers |
|---|---|---|
| **G0a KNOWN_ANSWER** (hard) | **PASS** | 12/12 hand-authored fixtures + separation pair reproduced (selftest report on main) |
| **G0b ORACLE_SELF_AGREEMENT** (hard) | **PASS** | Kleene = exhaustive on every version of all 1 200 instances (max 8 censored atoms); all valid at v0; 100/100 per stratum |
| **G0c NULL_CALIBRATION** (hard) | **PASS** | NEVER_REOPEN exact 0/767 where the oracle requires change; GLOBAL_RESET exact 0/765 where the oracle is mixed; RANDOM exact 0.0025; M vs shuffled labels exact 0.000 (n = 545) |
| **G1a B5_REPRODUCES_M** | **PASS** | decision identity 1.000 (rule ≥ 0.995); per-stratum discordance 0/100 in all 12 strata (rule ≤ 5%) |
| **G1b M_ADVANTAGE** | not fired | paired diff 0.000, discordant 0/1 200, exact p = 1.0, Wald CI [0, 0] |
| **G2 ANTI_CONSERVATISM** | **PASS** | over-reopened commitments on NO_REOPENING_NEEDED ∪ NEW_INDEPENDENT_SUPPORT: M 0 ≤ B5 0 |
| **G3 MECHANISM** | not applicable | no claimed advantage |
| **G4 INTERFACE_LADDER** | **PASS** (monotone, gap null) | rung exact 0.9675 → 0.9925 → 0.9925 → 1.000 → 1.000; steps R1→R2 +30/−0 (p < 0.001), R2→R3 0/0, R3→R4 +9/−0 (p = 0.0039), R4→R5 0/0; no violation; rung-5 gap 0 |
| COST | flag only | M 357 ms vs B5 739 ms wall (ratio 2.07 → `COST_ADVANTAGE_M`); engine ops M 174 900 (size proxy) vs B5 383 829 (JTMS checks), not commensurable |

## 3. Per-arm outcomes (1 200 instances; §5)

| arm | instance exact | final exact | over | under | invalid pres. | false unres. | missed unres. | recovery (n=239) |
|---|---|---|---|---|---|---|---|---|
| A0_PROVENANCE_ONLY_INVALIDATION | 0.229 | 0.298 | 2398 | 67 | 147 | 0 | 176 | 0.787 |
| A1_JTMS_CLASSICAL | 0.766 | 0.766 | 318 | 118 | 198 | 0 | 176 | 1.000 |
| A2_ATMS_CLASSICAL | 0.818 | 0.818 | 318 | 118 | 122 | 0 | 73 | 1.000 |
| A3_AGM_KERNEL_CONTRACTION | 0.763 | 0.763 | 324 | 118 | 198 | 0 | 176 | 1.000 |
| A4_BAYES_NOISY_OR | 0.805 | 0.805 | 334 | 111 | 115 | 3 | 73 | 0.996 |
| A5_ASSURANCE_CASE_UPDATE | 0.237 | 0.306 | 2414 | 44 | 124 | 0 | 176 | 0.787 |
| B5_R1_VERDICT_ONLY | 0.968 | 0.971 | 0 | 43 | 47 | 0 | 4 | 1.000 |
| B5_R2_PROV | 0.993 | 0.993 | 0 | 9 | 10 | 0 | 1 | 1.000 |
| B5_R3_PROV+DEP | 0.993 | 0.993 | 0 | 9 | 10 | 0 | 1 | 1.000 |
| B5_R4_PROV+DEP+TRANS+EVAL | 1.000 | 1.000 | 0 | 0 | 0 | 0 | 0 | 1.000 |
| **B5_STRONGEST_FAITHFUL_PARENT_FEDERATION** | **1.000** | **1.000** | 0 | 0 | 0 | 0 | 0 | 1.000 |
| **M_ME_SELECTIVE_REOPENING** | **1.000** | **1.000** | 0 | 0 | 0 | 0 | 0 | 1.000 |
| M_MINUS_DEPENDENCE_ANCESTRY | 0.978 | 0.978 | 0 | 44 | 48 | 0 | 4 | 1.000 |
| M_MINUS_TYPED_TRANSPORT | 0.988 | 0.988 | 25 | 0 | 0 | 0 | 0 | 1.000 |
| M_MINUS_EVALUATOR_CONTRACT | 0.894 | 0.894 | 296 | 2 | 2 | 0 | 69 | 1.000 |
| M_MINUS_SUPPORT_FAMILIES | 0.254 | 0.323 | 2100 | 0 | 0 | 167 | 0 | 0.787 |
| M_GLOBAL_RESET_CONTROL | 0.054 | 0.098 | 6928 | 0 | 0 | 0 | 176 | 0.389 |
| M_PROVENANCE_ONLY_CONTROL | 0.229 | 0.298 | 2398 | 67 | 147 | 0 | 176 | 0.787 |
| C_NEVER_REOPEN | 0.361 | 0.481 | 0 | 1266 | 1442 | 0 | 176 | 1.000 |
| C_RANDOM_DISPOSITION | 0.003 | 0.003 | 2598 | 846 | 516 | 2959 | 116 | 0.343 |

## 4. Per-stratum instance-exact rate (100 instances each)

| stratum | A0 prov | A1 JTMS | A2 ATMS | A3 AGM | A4 Bayes | A5 assur | R1 | R2 | R3 | R4 | **B5 (R5)** | **M** | −dep | −transp | −eval | −families | reset | never |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SOURCE_RETRACTED | 0.00 | 1.00 | 1.00 | 1.00 | 0.98 | 0.00 | 0.97 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| DEPENDENCE_DISCOVERED | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.78 | 1.00 | 1.00 | 0.15 | 0.00 | 0.78 |
| CALIBRATION_INVALIDATED | 0.17 | 1.00 | 1.00 | 1.00 | 0.98 | 0.17 | 0.96 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.17 | 0.00 | 0.33 |
| TRANSPORT_RELATION_INVALIDATED | 0.19 | 0.95 | 0.95 | 0.95 | 0.95 | 0.19 | 0.98 | 0.98 | 0.98 | 1.00 | 1.00 | 1.00 | 1.00 | 0.95 | 1.00 | 0.20 | 0.00 | 0.55 |
| EVALUATOR_BLIND_OR_REPLACED | 0.02 | 0.33 | 0.33 | 0.33 | 0.33 | 0.11 | 0.94 | 0.94 | 0.94 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 0.23 | 0.00 | 0.22 |
| PROBLEM_SCOPE_CHANGED | 0.30 | 0.45 | 0.45 | 0.45 | 0.46 | 0.30 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.30 | 0.00 | 0.45 |
| NEW_INDEPENDENT_SUPPORT | 0.56 | 1.00 | 1.00 | 1.00 | 1.00 | 0.56 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.56 | 0.21 | 0.56 |
| CORRECTION_RESTORES_SUPPORT | 0.22 | 1.00 | 1.00 | 1.00 | 0.99 | 0.22 | 0.97 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.22 | 0.00 | 0.00 |
| PARTIAL_SUPPORT_FAILURE | 0.00 | 1.00 | 1.00 | 1.00 | 0.94 | 0.00 | 0.96 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.44 |
| ALL_SUFFICIENT_SUPPORT_FAILED | 0.17 | 1.00 | 1.00 | 0.97 | 1.00 | 0.17 | 0.87 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.17 | 0.00 | 0.00 |
| CANNOT_CHECK_EDGE | 0.00 | 0.00 | 0.62 | 0.00 | 0.59 | 0.00 | 0.96 | 0.99 | 0.99 | 1.00 | 1.00 | 1.00 | 0.96 | 1.00 | 0.66 | 0.21 | 0.00 | 0.00 |
| NO_REOPENING_NEEDED | 0.34 | 0.68 | 0.68 | 0.68 | 0.66 | 0.34 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.91 | 0.74 | 0.84 | 0.44 | 1.00 |

(C_RANDOM ≤ 0.01 everywhere; M_PROVENANCE_ONLY_CONTROL = A0.)

## 5. Reading (within the frozen gates; no reinterpretation)

- **H0 (strongest-parent sufficiency) holds exactly.** The information-matched federation — parent-owned ORION provenance and dependence modules, typed transport/evaluator/scope statuses, JTMS propagation with a censored-atom envelope — is decision-identical to `selective_reopen` on every instance. The entire content of "selective reopening" lives in the typed registration of support and in what crosses the module boundary, not in the propagation engine.
- **Interface ladder (H-EXT-3, prediction (a) confirmed):** exactness rises monotonically with the information that crosses module boundaries — verdict-only 0.968 → +provenance records 0.993 → +dependence ancestry 0.993 → +typed transport/evaluator 1.000 → full structure 1.000 — and the rung-5 gap is exactly zero. The two significant steps are provenance records (30 instances, concentrated in ALL_SUFFICIENT_SUPPORT_FAILED, SOURCE_RETRACTED, CALIBRATION, CORRECTION, PARTIAL) and typed evaluator/transport statuses (9 instances, EVALUATOR and CANNOT_CHECK). Dependence ancestry at witness level added nothing beyond its verdict form on this generator (0 discordant): a family-level independence defeat is already exactly compressible to a per-claim verdict here. The separation example (P/Q) remains the finite proof that verdict-only exchange is insufficient in general.
- **Where single parents break (attribution, from §4):** provenance-only and assurance-case update over-reopen every redundantly supported commitment (0.229 / 0.237); untyped TMS/AGM/Bayes miss dependence discovery (0.78), evaluator typing (0.33) and scope semantics (0.45) and over-reopen on `NO_REOPENING_NEEDED` decoys (0.68); two-valued engines score 0.00 on `CANNOT_CHECK_EDGE` while ATMS environments (0.62) and the noisy-OR envelope (0.59) express censoring partially. The noisy-OR arm's residual failures (0.94–0.98 on retraction strata) are reliability compounding along prerequisite chains — its native boundary.
- **Ablations behave as their omission predicts:** −dependence ancestry fails `DEPENDENCE_DISCOVERED` (0.78) and `CANNOT_CHECK` (0.96); −typed transport over-reopens 25 commitments (`TRANSPORT` 0.95, `NO_REOPENING_NEEDED` 0.91 — the protected decoys separated it, as the development receipt anticipated); −evaluator contract over-reopens 296 (`EVALUATOR` 0.33); −support families over-reopens 2 100 (0.254). Each omission has causal value **for M and equally for B5** — they are properties of the typed interface, not of M's control layer.
- **Cost:** M's stateless double fixed point is ≈ 2× faster in wall-clock than the incremental JTMS federation on these sizes (357 vs 739 ms for 1 200 × 1–3 versions). Not a route: a cost claim needs a separate scaling cell under its own freeze.
- **Recovery:** every family-aware arm recovers 239/239 reopened→corrected commitments; the AND-semantics arms (provenance-only, assurance, −families) recover 0.787 because they never reopened correctly to begin with.

## 6. Kill conditions (protocol §8) — status

| condition | outcome |
|---|---|
| B5 exactly reproduces M's decisions at equal or lower cost | decisions: **reproduced exactly**; cost: B5 ≈ 2× M wall-clock (flag only) → **parent-owned on decisions**; cost-only residual not claimed |
| M over-reopens enough to erase independent valid support | no: M over-reopening 0 on all strata (G2 pass) |
| M depends on hidden oracle relations | no: arms never import the oracle; M uses only registered information and the existing ORION reference modules |
| support-family schema cannot preserve native semantics | not observed: every native parent was expressible over the same registered families |

## 7. Programme consequence

`ME_X4_STATUS = PARENT_SUFFICIENT`. Selective reopening contracts from a Machine Epistemics control residual to an **interface standard** (typed support families + what crosses module boundaries), consistent with field synthesis §7 ("no ME residual exists if [parents] recover the same decisions") and with H-EXT-3's negative terminal `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`, which keeps the interface contribution and contracts the control claim. The naturalistic cell (protocol §7) remains a separate, unexecuted identity; nothing here transfers to it. No field status, novelty or publication authority is granted or implied.

## 8. Custody

The authorization file (archived as `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json`, byte-identical to the one consumed) and `results/ME_X4_PROTECTED_*` are archived in this PR (force-added past the `.gitignore` that guards against unauthorized commits). The live path `PROTECTED_RUN_AUTHORIZATION.json` is absent again, so `mex4_run.py protected` refuses (exit 3) and the design-time single-run invariant test holds; a second protected run would require a new, explicit authorization. Selftest report used for G0a is the one on main. The custody seed file remains in operator custody; its value is now public (above) and the split is reproducible by anyone from the frozen code on `ee32108`.
