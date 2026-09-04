# ME-X1 — Cross-Transition Coupling Benchmark: Protected-Run Outcome Receipt (V1)

**Design:** `ME_X1_TRANSITION_COUPLING_EXACT_STUDY_DESIGN_V1.{md,json}` (PR #155, main `0fde96f`), design-JSON sha256 `b9ae7b02fe0168ec94fed3bf36e4a7d223aac52e7f30a0fd44e9cfe0c664d7de`.
**Authorization:** operator, in chat, 2026-09-02, verbatim *"run all the computation tasks.. finish all the researxh asap"*, recorded in `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` (the file the runner consumed as `PROTECTED_RUN_AUTHORIZATION.json`, archived under a new name after the single run so the runner's guard is re-armed; content and sha256 unchanged `9dfb849bd5aca633bca0896f8c00529f222148c45bf18d57201872db68c5eb4c`; carries the verbatim instruction, the UTC timestamp, the design sha256 and the seed-commitment sha256).
**Run:** Mac (local), 2026-09-02 14:26 UTC, `python3 mex1_run.py protected --out results`, **executed exactly once**, exit 0, 5.3 s CPU; the runner verified sha256(custody seed) = frozen commitment `84ae78f5676879bfa022460bc17ae36233935e3bdfef4a63a670d9eda431c34d` before generating; `analyze` ran once inside the same invocation. Code unchanged from main (`mex1_run.py` `f4c8ed6b…`, `mex1_arms.py` `cbe3d48e…`, `mex1_oracle.py` `5a34146c…`). **No post-outcome change to any design constant, gate, arm, oracle rule, precedence or seed.** Re-arming verified: with the file archived, `mex1_run.py protected` refuses again (exit 3).

**Seed reveal (per design §3):** `ME-X1-PROTECTED-a047cc2636884cc90bb0f2c7086e0744` — sha256 equals the commitment above; the 1 000-instance split regenerates byte-for-byte from it.

**Artifacts (sha256):** results `f3065bfee46c6326079a17b55af373fa752c3333c8861c90f894545e9606012f`; expected-custody `387cec102ff843a9e0c024cb766d7ce763c583f3d1756e58af3aed14aefe223f`; timing `9dc54c5ca0b93361d610958f9ece232f21850bab322b543c5ffc1fcd69310029`; analysis json `cd69f435013c7fa57d06ffc63bf2984537104de5f49ea1059616406600f01951`; selftest report (G0a source, unchanged from the design PR) `1f4b8a6eac26072c4b25fda4a05b09a306f9cacabbc974514a5e1bb4f48e0353`.

## 1. Terminal

```text
ME_X1_STATUS              = EXECUTED_PROTECTED
ROUTE                     = PARENT_SUFFICIENT
LADDER_TERMINAL (H-EXT-3) = RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL
COST_FLAG                 = COST_ADVANTAGE_M (wall-clock ratio 2.14; reported, no route)
PRIMARY_COMPARATOR        = B5_STRONGEST_FAITHFUL_PARENT_FEDERATION
COMPARATOR_CLASS          = CEILING_CONTROL_NOT_PRIOR_WORK
                          -- Despite its name, B5 is NOT a published-method parent. Per the design's
                             pre-registered b5_information_matching field it holds THIS PROJECT'S OWN
                             typed orion_v2 modules, at the mechanism's registry visibility and behind
                             the same frozen adjudicator. It is information-matched to M by construction,
                             so it bounds what ANY faithful composition could reach. Agreement with it is
                             therefore not evidence that prior work suffices.
ROUTE_AS_READ             = ORION_TYPED_INTERFACE_SUFFICIENT__CONTROLLER_ADDS_NOTHING_ON_TOP
                          -- PARENT_SUFFICIENT does NOT mean 'prior work suffices'. No arm citing a
                             published method matches M: B3 (assurance alone) 0.498, B4 (TMS federation minus ORION's typed organs) 0.837, B5 1.000 = M.
                             This is the same statement as LADDER_TERMINAL
                             RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL. Qualification only:
                             no gate, datum, weight, seed or terminal verdict is changed.
FIELD_STATUS_AUTHORITY    = NONE
```

**Cross-transition coupling, as an exact decision function, is parent-owned.** On 1 000 protected instances across all ten families, the strongest faithful parent federation reproduces `M`'s transition decisions — action *and* reopened set — **identically on every instance** (decision identity 1 000/1 000; 0 discordant pairs; every family 0/100 discordant). The design's central conjecture, that locally valid operations can compose into an unwarranted transition, is confirmed *as a benchmark property* — B0 launders 492 unwarranted updates and B4, the TMS federation, launders 163 — but it is **not** a Machine-Epistemics control residual: once every cross-transition condition crosses the module boundary as a typed witness, ordinary engineering glue computes the same function.

**The H-EXT-3 ladder is sharper here than in ME-X4.** It is monotone with **exactly one significant step, at R4→R5** (+29 instances, exact p < 10⁻⁸) — precisely where §1.2 predicted it, and the prediction was registered before the run. The whole interface content of this benchmark is the identity/criterion/specification witness; provenance, dependence, transport and evaluator witnesses added *nothing* beyond their verdict form on this generator (0 discordant at every earlier step).

## 2. Gates (frozen pre-outcome; all numbers from `results/ME_X1_PROTECTED_ANALYSIS_V1.json`)

| gate | verdict | numbers |
|---|---|---|
| **G0a KNOWN_ANSWER** (hard) | **PASS** | 14/14 public `X1-DEV-001…014` fixtures reproduced by the oracle, M and B5 exact on all; separation pair P/Q reproduced (selftest report on main) |
| **G0b ORACLE_SELF_AGREEMENT** (hard) | **PASS** | precedence walk / Kleene support = exhaustive enumeration on all 1 000 instances; all valid at v0; family invariants held at generation; 100/100 per family |
| **G0c NULL_CALIBRATION** (hard) | **PASS** | `C_ALWAYS_UPDATE` exact 0/630 where the oracle is not warranted; `C_ALWAYS_DEFER` exact 0/820 where the oracle is determinate; `C_RANDOM` exact 0.097; M vs permuted oracle decisions 0.143 (200 permutations, 200 000 draws) against chance 0.1496 |
| **G1a B5_REPRODUCES_M** | **PASS** | decision identity **1.000** (rule ≥ 0.995); per-family discordance **0/100 in all ten families** (rule ≤ 5%) |
| **G1b M_ADVANTAGE** | not fired | paired diff 0.000, discordant 0/1 000, exact p = 1.0, Wald CI [0, 0] |
| **G2 ANTI_CONSERVATISM** | **PASS** | unnecessary defer/abstain: M 0 ≤ B5 0; warranted-transition recall M 1.000 ≥ B5 1.000 on n = 370 warranted instances |
| **G3 MECHANISM** | not applicable | no claimed advantage |
| **G4 INTERFACE_LADDER** | **PASS** (monotone, gap null) | rung exact 0.971 → 0.971 → 0.971 → 0.971 → **1.000**; steps R1→R2 0/0 (p = 1.0), R2→R3 0/0, R3→R4 0/0, **R4→R5 +29/−0 (p = 3.7×10⁻⁹)**; no violation; rung-5 gap 0 |
| COST | flag only | M 146 ms vs B5 313 ms wall (ratio 2.14 → `COST_ADVANTAGE_M`); ops M 80 650 (obligations + reopen size proxy) vs B5 193 052 (JTMS checks), not commensurable |

Oracle action mix (1 000 instances): UPDATE 0.270, DEFER_CANNOT_CHECK 0.180, REVALIDATE 0.121, PRESERVE 0.100, SELECTIVELY_REOPEN 0.084, REFORMULATE_PROBLEM 0.065, ABSTAIN_AUTHORITY 0.050, BLOCK_TRANSPORT 0.050, REPLACE_OR_CHALLENGE_EVALUATOR 0.050, REQUEST_NEW_EVIDENCE 0.030.

## 3. Per-arm outcome vector (1 000 instances; protocol §7)

| arm | exact | false upd. | missed warr. | over-reop. | under-reop. | inv. transp. | false closure | eval. laund. | prob/spec laund. | auth. laund. | correct unres. | warr. recall | unnec. defer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0_DIRECT | 0.384 | 492 | 0 | 0 | 133 | 50 | 180 | 50 | 86 | 50 | 0.00 | 1.000 | 0.000 |
| B1_CALIBRATED_ABSTENTION | 0.347 | 55 | 118 | 0 | 133 | 0 | 5 | 0 | 35 | 15 | 0.97 | 0.465 | 0.731 |
| B2_PROVENANCE_PLUS_VERIFIER | 0.434 | 362 | 18 | 60 | 45 | 18 | 160 | 34 | 51 | 50 | 0.00 | 0.843 | 0.000 |
| B3_PARENT_NATIVE_ASSURANCE | 0.498 | 0 | 12 | 143 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 | 0.816 | 0.000 |
| B4_PARENT_MODULES_WITH_SHARED_STATE | 0.837 | 163 | 0 | 0 | 0 | 0 | 62 | 0 | 51 | 50 | 0.66 | 1.000 | 0.000 |
| B5_R1_VERDICT_ONLY | 0.971 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 |
| B5_R2_PROV | 0.971 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 |
| B5_R3_PROV+DEP | 0.971 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 |
| B5_R4_PROV+DEP+TRANS+EVAL | 0.971 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 |
| **B5_STRONGEST_FAITHFUL_PARENT_FEDERATION** | **1.000** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 |
| **M_ME_TRANSITION_CONTROL** | **1.000** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 1.000 | 0.000 |
| M_MINUS_PROBLEM_IDENTITY | 0.889 | 111 | 0 | 0 | 0 | 0 | 25 | 0 | 86 | 0 | 0.86 | 1.000 | 0.000 |
| M_MINUS_DEPENDENCE | 0.930 | 16 | 0 | 0 | 45 | 0 | 20 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 |
| M_MINUS_EVALUATOR_CONTRACT | 0.946 | 54 | 0 | 0 | 0 | 0 | 20 | 34 | 0 | 0 | 0.89 | 1.000 | 0.000 |
| M_MINUS_TRANSPORT | 0.930 | 70 | 0 | 0 | 0 | 50 | 20 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 |
| M_MINUS_SUPPORT_REOPENING | 0.935 | 0 | 0 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 1.00 | 0.849 | 0.000 |
| M_MINUS_AUTHORITY | 0.930 | 70 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 50 | 0.89 | 1.000 | 0.000 |
| M_MINUS_UNRESOLVED_TERMINAL | 0.820 | 140 | 0 | 0 | 0 | 0 | 180 | 0 | 0 | 0 | 0.00 | 1.000 | 0.000 |
| M_MINUS_MEASUREMENT_COMPARABILITY | 0.930 | 70 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 0 | 0.89 | 1.000 | 0.000 |
| M_MINIMAL_RECEIPT | 0.900 | 100 | 0 | 0 | 0 | 0 | 48 | 0 | 29 | 0 | 0.73 | 1.000 | 0.000 |
| C_ALWAYS_UPDATE | 0.370 | 506 | 0 | 0 | 133 | 50 | 180 | 50 | 100 | 50 | 0.00 | 1.000 | 0.000 |
| C_ALWAYS_DEFER | 0.180 | 0 | 270 | 0 | 133 | 0 | 0 | 0 | 0 | 0 | 1.00 | 0.000 | 1.000 |
| C_RANDOM_ACTION | 0.097 | 67 | 242 | 208 | 127 | 6 | 46 | 6 | 7 | 1 | 0.08 | 0.103 | 0.199 |

## 4. Per-family exact-transition rate (100 instances each: 50 positive / 30 negative / 20 ambiguity)

| family | B0 | B1 | B2 | B3 | B4 | R1 | R2 | R3 | R4 | **B5 (R5)** | **M** | −ident | −dep | −eval | −transp | −reopen | −auth | −unres | −meas | minimal | always-upd | always-defer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A claim/problem identity | 0.30 | 0.28 | 0.65 | 0.65 | 0.71 | 0.85 | 0.85 | 0.85 | 0.85 | **1.00** | **1.00** | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 | 0.73 | 0.30 | 0.20 |
| B measurement/calibration | 0.30 | 0.30 | 0.40 | 0.77 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 0.30 | 0.67 | 0.30 | 0.20 |
| C hidden dependence | 0.30 | 0.20 | 0.30 | 0.43 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | **1.00** | 1.00 | 0.30 | 1.00 | 1.00 | 0.79 | 1.00 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 |
| D invalid transport | 0.30 | 0.45 | 0.29 | 0.30 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | **1.00** | 1.00 | 1.00 | 1.00 | 0.30 | 1.00 | 1.00 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 |
| E defeated prerequisite | 0.30 | 0.20 | 0.46 | 0.46 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | 0.66 | 1.00 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 |
| F evaluator blindness | 0.30 | 0.36 | 0.30 | 0.21 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | **1.00** | 1.00 | 1.00 | 0.46 | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 |
| G authority mismatch | 0.30 | 0.36 | 0.30 | 0.30 | 0.30 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.30 | 0.80 | 1.00 | 1.00 | 0.30 | 0.20 |
| H proof / wrong specification | 0.44 | 0.30 | 0.44 | 0.66 | 0.53 | 0.86 | 0.86 | 0.86 | 0.86 | **1.00** | **1.00** | 0.53 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 | 0.77 | 0.30 | 0.20 |
| I local compat. / global obstruction | 0.30 | 0.41 | 0.30 | 0.30 | 0.83 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 | 0.83 | 0.30 | 0.20 |
| J fully warranted | 1.00 | 0.61 | 0.90 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |

Per variant (M and B5 = 1.00 everywhere): POSITIVE B0 0.13 / B1 0.06 / B2 0.34 / B3 0.49 / B4 0.80 / R1–R4 0.94; NEGATIVE B0 1.00 / B1 0.40 / B2 0.81 / B3 0.77 / B4 1.00 / R1–R4 1.00; AMBIGUITY B0 0.10 / B1 0.97 / B2 0.10 / B3 0.10 / B4 0.69 / R1–R4 1.00.

## 5. Reading (within the frozen gates; no reinterpretation)

- **H0 (strongest-parent sufficiency) holds exactly.** The information-matched federation — the same parent-owned modules M's obligations are fed by (`orion_v2.provenance`, `evidence.assess_evidence_dependence`, `structural.RelationType`, `comparability`, `epistemic_atlas`, contract binding, refinement fidelity, evaluator coverage, authority lattice), JTMS shared state, the registered precedence table as glue — is decision-identical to `M` on every one of the 1 000 instances. The content of "cross-transition control" lives in the *typed registration of the conditions and what crosses the module boundary*, not in a control layer.
- **Interface ladder (H-EXT-3, prediction (a) confirmed, and localised.** Exactness is flat at 0.971 through rungs 1–4 and reaches 1.000 only at full structure: **one significant step, R4→R5, +29/−0, p = 3.7×10⁻⁹**, exactly the step §1.2 predicted before the run. All 29 rung-1..4 misses are in families A (15) and H (14) and are **pure action-granularity errors, not laundering**: with the IDENT module compressed to one family-anonymous verdict carrying the module default, a criterion mismatch is answered `REVALIDATE` instead of `REFORMULATE_PROBLEM` (15 cases) and a failed proof checker `REVALIDATE` instead of `REQUEST_NEW_EVIDENCE` (14 cases). Verdict-only exchange in this benchmark is **safe but imprecise**: 0 false updates, 0 false closures, 0 laundering of any kind, correct-unresolved 1.00 — it knows *that* the transition is blocked and not *which repair the condition names*. The separation pair P/Q (selftest) remains the finite witness that verdict exchange can also be outright *wrong*, not merely imprecise, once defeats compose across families.
- **Where the parents break (attribution).** `B0` launders 492 unwarranted updates (86 problem/specification, 50 evaluator, 50 authority) and closes all 180 uncheckable cases. `B1`'s generic uncertainty gate is over-conservative exactly as protocol §8 anticipates: 0.731 unnecessary-defer rate, warranted recall 0.465, 118 missed warranted updates — it buys 0.97 correct-unresolvedness by refusing 73% of the determinate cases. `B2` (provenance + verifier) catches binding by artifact lineage and calibration by revocation but has no transport-rank, coverage, dependence, atlas or authority vocabulary: 362 false updates, 160 false closures, and 60 over-reopenings, including revalidation on the registered ontic `TARGET_CHANGED` control (a native property of execution-graph runtimes, not a handicap). `B3` never launders (0 false updates) but over-reopens 143 commitments under AND semantics and answers every challenge with the same single repair (0.21–0.46 on D/E/F/G/I). `B4`, the TMS federation, is **exact on B–F** — typed provenance, dependence, transport and evaluator are TMS-owned — and fails on precisely the four conditions that are not: authority (70 misses, 50 of them authority laundering), specification fidelity and criterion identity (47 + 29), and the atlas witness (17, pairwise compatibility taken as a global section). `B5` recovers all of them because those parents are typed and witness-level at rung 5.
- **Ablations behave as their omission predicts, family by family:** −problem identity fails A (0.36) and H (0.53) with 86 problem/specification launderings; −dependence fails C (0.30); −transport fails D (0.30) with 50 invalid transports; −evaluator contract fails F (0.46) with 34 evaluator launderings; −authority fails G (0.30) with 50 authority launderings; −measurement/comparability fails B (0.30); −support reopening over-reopens 92 commitments on the independent-route controls (E 0.66, C 0.79, J 0.90) and is the only ablation that damages warranted recall (0.849); −unresolved terminal closes all 180 uncheckable cases (0.80 on every family, AMBIGUITY 0.10). Every omission has causal value **for M and equally for B5** — these are properties of the typed interface, not of a control layer.
- **`M_MINIMAL_RECEIPT` is the prospective ablation that bit.** Frozen on the development split — where dropping `witness, piece, evc, tr, comparability, ident, checker, criterion, nocontra` cost nothing (1.000 on 40 instances) — it falls to **0.900 on the protected split**, 100 misses: 23 calibration REVALIDATE→UPDATE and 10 ambiguity closures in B, 15 criterion and 12 ambiguity in A, 14 checker and 9 ambiguity in H, 17 atlas-witness closures in I. A receipt minimised against a development split silently discards conditions the protected distribution exercises; this is a measured cost of receipt minimisation, registered before the run.
- **Anti-conservatism (protocol §8) is clean.** M's unnecessary defer/abstain count is 0 and its warranted-transition recall is 1.000 on 370 warranted instances (every NEGATIVE variant plus family J positives). M obtains its exactness by deciding correctly, not by refusing; `C_ALWAYS_DEFER` scores 0.180 and `B1` shows what buying safety by abstention costs.
- **Cost:** M's stateless obligation walk plus double reopening fixed point is ≈ 2.1× faster in wall-clock than the incremental JTMS federation at these sizes (146 vs 313 ms for 1 000 instances). Not a route: a cost claim needs a separate scaling cell under its own freeze.

## 6. Field-support rule (protocol §10) and kill conditions (§11) — status

| §10 requirement | outcome |
|---|---|
| 1. B5 has the information and parent mechanisms locally | satisfied by construction (every module typed and witness-level at rung 5) |
| 2. B5 makes a systematic composition error in some protected family | **not satisfied**: 0/100 discordant in all ten families |
| 3. M avoids an error because of a predeclared condition | vacuous (no error to avoid) |
| 4. matching omission ablation restores the error | ablations do restore family-specific errors — but symmetrically for M and B5 |
| 5. effect transfers to an independently authored family | not attempted (separate naturalistic cell, §9) |
| 6. gain is not generic over-conservatism | satisfied (G2), but there is no gain to attribute |

**X1 is therefore at most a benchmark/integration result, as protocol §10 provides.** Kill conditions: B5 ties on decisions at ≈ 2× wall-clock cost → *parent-owned on decisions*, cost-only residual not claimed; M received no extra information or evaluator access (arms never import the oracle; M and B5 read the identical registry); no omission-specific causal effect is M-exclusive; M's exactness is not abstention.

## 7. Programme consequence

`ME_X1_STATUS = PARENT_SUFFICIENT`. Together with the merged ME-X4 protected run (`PARENT_SUFFICIENT`, `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`), the flagship's two decisive exact-oracle lanes now agree: the Machine-Epistemics residual in known-answer worlds is an **interface-information residual, not a control residual**. ME-X1 adds three things ME-X4 could not: (i) the residual is **localised** — one ladder step, carrying the identity/criterion/specification witness, is worth 29/1 000 instances while provenance, dependence, transport and evaluator witnesses are exactly verdict-compressible on this generator; (ii) verdict-only exchange here is **safe but imprecise** (right that a transition is blocked, wrong about which repair) — the separation pair remains the witness that it can be outright wrong; (iii) the **strongest TMS federation is not enough** (0.837): authority ceilings, specification fidelity, criterion identity and the local-to-global witness are not truth-maintenance objects, and a federation only recovers them by adopting those parents as typed modules — which is an interface standard, precisely the surviving contribution H-EXT-3's negative terminal preserves. The naturalistic cell (protocol §9) remains a separate, unexecuted identity; nothing here transfers to it. No field status, novelty or publication authority is granted or implied.

## 8. Custody

The authorization file (archived as `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json`, byte-identical to the one consumed) and `results/ME_X1_PROTECTED_*` are archived in this PR (force-added past the `.gitignore` that guards against unauthorized commits). The live path `PROTECTED_RUN_AUTHORIZATION.json` is absent again, so `mex1_run.py protected` refuses (exit 3, verified) and the design-time single-run invariant test holds; a second protected run would require a new, explicit authorization. The selftest report used for G0a is the one on main. The custody seed file remains in operator custody; its value is now public (above) and the split is reproducible by anyone from the frozen code on `0fde96f`.
