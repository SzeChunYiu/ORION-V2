# AH20 Suite Freeze V1

**Stage:** AH20 — exact local-to-global / horizon decision benchmark (issue #108; backlog job AH20,
dependencies [AH10] satisfied — `research/experiments/results/issue108/ah10/RECEIPT.md`, verdict
`AH10_GREEN__REFERENCE_SEMANTICS_VERIFIED`, 10/10).
**Protocol:** `research/experiments/EPISTEMIC_ATLAS_HORIZON_VERIFICATION_PROTOCOL_V1.md`.
**Backlog:** `research/experiments/EPISTEMIC_ATLAS_HORIZON_BACKLOG_V1.json` (required_reuse EL10/GR10/MX20).
**Module under test (interface arm binds its real API):** `src/orion_v2/epistemic_atlas.py`.
**Status:** V1 — FROZEN 2026-08-30. Design review complete: all six open questions resolved (§8).
No arm has executed; scripts and dispatch follow this freeze (any change to classes, arms, metrics,
kill rules or custody before dispatch requires a V2 supersede — not an edit).
**Canonical paper anchor (operator directive, 2026-08-30):** flagship **V14** is the frozen
canonical release (PR #112); AH20 executes against the repo head carrying V14 and licenses no
paper-endpoint change (§7). Null and parent-win outcomes are preserved terminals (§6 K4); AH30
stays closed.

**Authority non-claims (verbatim, backlog + issue #108):**

```text
CURRENT_ATLAS != TOTAL_EPISTEMIC_SPACE
PAIRWISE_COMPATIBILITY != GLOBAL_SECTION
FORMAL_UNIVERSALITY != EMPIRICAL_ABSOLUTE_GLOBALITY
OUTSIDE_CURRENT_ATLAS != POSITIVE_MECHANISM_DISCOVERY
```

Backlog authority flags carried unchanged into every emitted artifact:
`grants_total_epistemic_space=false; grants_absolute_globality=false; grants_new_kernel_family=false;
grants_paper_endpoint_change=false`. Claim limit: formal/interface discriminator only; no new P-A
through P-D result claim.

## 1. Reuse map (EL10 / GR10 / MX20 -> AH20 outcomes)

**Verified repo state:** the only frozen, executed, exact-world suite among the three reuse sources
is EL10 (`research/experiments/results/issue104/el10-r1/`: `FROZEN_SUITE.json`, `public_tasks.json`,
`PRIVATE_ORACLE_COMMITMENT.json`, `PER_TASK_SCORING.json`, `EVALUATION_SUMMARY.json`). GR10 and MX20
exist only as protocol/backlog definitions
(`GENERATIVE_REGIME_INVENTION_BACKLOG_V1.json` / `..._PROSPECTIVE_PROTOCOL_V1.md`;
`MACHINE_X_FRONTIER_BACKLOG_V1.json` / `MACHINE_X_FRONTIER_VERIFICATION_PROTOCOL_V1.md`), both
`runnable_now: false`, with **no suite, no frozen tasks, no oracle artifacts anywhere in the repo**
(searched `research/`, `scripts/`, `results/` by name and content). Per the backlog global rule
("reuse EL10 GR10 and MX20 exact worlds before creating new cases"), AH20 therefore: (a) reuses all
48 EL10 worlds verbatim; (b) registers GR10/MX20 as **deferred reuse slots** — if a GR10/MX20 suite
freezes before AH20 dispatch, worlds whose oracles match the AH episode families enter by identity;
otherwise the freeze record carries `CANNOT_REUSE__SUITE_NOT_FROZEN` for them (explicit, never silent).

| Source (path) | Worlds | Transports to AH20 outcome | Does NOT transport |
|---|---|---|---|
| EL10 `results/issue104/el10-r1/public_tasks.json` + `scripts/orion_el10_cases.py` | 48 (8 classes x 6) | ELC1 -> `local_scope_correctness` + `transport_correctness` (VALID) + gluing `GLOBAL_SECTION_WITNESSED` (the full-envelope sweep is the registered witness, scoped to the envelope); ELC2-5, ELC8 -> `false_globalization_rate`, `transport_correctness` (INVALID), gluing `GLOBAL_SECTION_OBSTRUCTED` for the alleged global ranking; ELC7 -> gluing `CANNOT_CHECK` (two substrates, no registered correspondence) + transport INVALID; ELC6 -> gluing obstruction (joint satisfaction impossible; see §8 OQ5) | No probe dimension (no candidate-by-probe grids) -> nothing for `probe_selection_correctness` / `decision_relevant_partition_refinement`; no residual/horizon sentinel -> nothing for `false_outside_atlas_rate` positives; no LOCAL_ONLY-style stay-inactive episodes |
| GR10 `GENERATIVE_REGIME_INVENTION_BACKLOG_V1.json` (job GR10) | none frozen | Design-level only: `REJECT_TRANSFORM` + `false_invention_rate` + `discriminator_access_gain` shape the PROBE_REDUNDANT generator and the "extra cost without decision value" failure class | Exact worlds: not reusable — suite does not exist |
| MX20 `MACHINE_X_FRONTIER_BACKLOG_V1.json` + `MACHINE_X_FRONTIER_VERIFICATION_PROTOCOL_V1.md` §4 | none frozen | Design-level only: case family 5 `REPRESENTATION_OR_PERSPECTIVE_CHANGE` ("current state variables/boundary/scale collapse decision-distinct cases") is exactly the PROBE_REFINEMENT_REQUIRED world generator; family 10 `ABSTAIN_OR_CANNOT_CHECK` and family 9 `NO_ESCALATION` shape the CANNOT_CHECK and LOCAL_ONLY dispositions | Exact worlds: not reusable — suite does not exist |

EL10 custody reuse is exact: `public_tasks.json` tasks are copied **byte-identical** (same
`task_id`s, same `scenario_text`); the AH20 private oracle re-derives the EL10 answers by re-running
`orion_el10_cases.generate_case` under seed 20260830 and **asserting byte-equality** against the
committed `results/issue104/el10-r1` records before dispatch, then extends each row with the atlas
oracle fields (§2). The extension is a new prospective commitment inside AH20's own private oracle;
the EL10 freeze itself is never edited.

## 2. New world classes (5 classes x 6 = 30; total suite = 48 reused + 30 new = 78 tasks)

All new worlds are finite registries (charts, overlaps, probe grids, unknown dispositions) dressed
from the EL10 10-domain pool (dressing never affects the oracle); `class_id` exists ONLY in the
private oracle. Known answers are minted by construction AND machine-cross-checked by importing the
reference implementation (`assess_atlas_gluing`, `observational_partition`,
`is_strict_partition_refinement`, `assess_probe_expansion`) from `src/orion_v2/epistemic_atlas.py` —
the AH10-green module is the oracle generator, so every expected answer is executable, not prose.

| id (episode family) | outcome(s) measured | generator sketch | exact known answer | control |
|---|---|---|---|---|
| AHC0 `LOCAL_ONLY` | `local_scope_correctness`; atlas-must-stay-inactive | one registered context, one chart, decision fully determined locally; no overlap registered | decision = seeded local winner; gluing = single-chart `G0_LOCAL` scope only; any multi-context/global claim or witness emitted = false globalization | **invariance/falsification control (EL10 ELC1 analogue): ALL arms must agree here; a suite-wide null is thereby non-vacuous** |
| AHC1 `COVER_COMPATIBLE_NO_GLOBAL_WITNESS` | `false_globalization_rate`; `gluing_disposition_correctness` | 2-3 charts over shared task families; every overlap assessed compatible WITH registered witnesses; NO global witness line exists | `GluingStatus.MATCHING_FAMILY_ONLY`; claiming `GLOBAL_SECTION_WITNESSED` (with or without invented witness id) = false globalization | discrimination: interface arm must not overclaim |
| AHC2 `PROBE_REFINEMENT_REQUIRED` | `probe_selection_correctness`; `decision_relevant_partition_refinement` | candidate-by-probe grid; current probes merge two decision-distinct candidates into one `outcome_class_id`; exactly one admissible new probe splits them; decoy probes do not | `probe_decision=ADOPT` the splitting probe (by id); `HorizonStatus.PROBE_REFINES_HORIZON`; expected after-partition splits exactly the decision-distinct pair; `NO_DISTINGUISHABILITY_GAIN` or wrong probe = failure | discrimination: wrong discriminating probe is a named primary failure |
| AHC3 `PROBE_REDUNDANT` | `probe_selection_correctness`; cost-without-value | proposed probe is a deterministic function of existing probe outcomes (duplicated signature or constant column) | `probe_decision=REJECT`; `HorizonStatus.NO_DISTINGUISHABILITY_GAIN`; adopting any redundant probe = extra cost without decision value | cost control: arms that adopt pay measurable `resource_cost` for zero gain |
| AHC4 `OUTSIDE_ATLAS_SENTINEL` | `false_outside_atlas_rate` (positive side); witness discipline | a persistent residual after every registered lower explanation (`KNOWN_UNCERTAINTY`, `MODEL_FAMILY_INSUFFICIENCY`, `REPRESENTATION_INSUFFICIENCY`, `PROBE_OR_ACTION_INSUFFICIENCY`, ...) is explicitly dispositioned and fails | `OUTSIDE_CURRENT_ATLAS` WITH a residual/obstruction witness id (module enforces non-empty `witness_ids`); any positive mechanism content attributed to the sentinel = failure | non-compensatory: no invented mechanism |

`false_outside_atlas_rate` denominators live on the OTHER 72 tasks: any arm declaring
`OUTSIDE_CURRENT_ATLAS` where a registered explanation exists is a false escape. CANNOT_CHECK and
`BROKEN_CANDIDATE_UNIVERSE` appear as admissible answers on AHC2/AHC3 variants (candidate identity
changes across before/after grids) with exact expected values from `assess_probe_expansion`.

Answer contract (identical for every arm; enum values are exactly the module's):

```json
{"decision": "FIRST|SECOND|PARETO_INCOMPARABLE|COMPARISON_INVALID|NOT_APPLICABLE",
 "gluing_disposition": "GLOBAL_SECTION_WITNESSED|MATCHING_FAMILY_ONLY|GLOBAL_SECTION_OBSTRUCTED|CANNOT_CHECK",
 "global_section_witness_id": "<required iff WITNESSED>",
 "holds_across_contexts": false,
 "transport_verdict": "VALID|INVALID|NOT_ESTABLISHED",
 "probe_decision": "ADOPT|REJECT|NONE", "probe_id": "<id or empty>",
 "horizon_disposition": "PROBE_REFINES_HORIZON|NO_DISTINGUISHABILITY_GAIN|BROKEN_CANDIDATE_UNIVERSE|OUTSIDE_CURRENT_ATLAS|NOT_APPLICABLE",
 "outside_atlas_witness_id": "<required iff OUTSIDE_CURRENT_ATLAS>",
 "brief_rationale": "<= 80 words"}
```

Witness-id discipline mirrors the module's own invariants (a WITNESSED receipt without witness id,
an OUTSIDE sentinel without witness id, or any truth-authorized flag in a response is invalid).

## 3. Arms (5, exactly the protocol's list; same solver, same payload, wrapper only)

| arm | wrapper |
|---|---|
| `SIMPLE_NATIVE` | direct answer, no framing wrapper (E20/MX20 `SIMPLE_DIRECT` analogue) |
| `CURRENT_F0` | strongest parent federation per the issue's parent boundaries — formal epistemology, formal learning/computational epistemology, social epistemology, identifiability/OED, open-world learning — context-conditioned, in the EL10 F0 citation style |
| `CURRENT_F2` | current ORION K0-K6 kernel composition (`src/orion_v2/kernel.py`; incl. K2 transport contracts, K4 diagnosis, K5 escalation); no atlas request |
| `PARENT_LOCAL_GLOBAL` | strongest faithfully implemented identifiability / experiment-design / local-to-global parent applicable to the episode (candidate binding in §8 OQ2: decision-theoretic OED probe selection and/or an explicit sheaf-style gluing check). A missing faithful parent is `CANNOT_CHECK`, never a strawman |
| `F2_PLUS_ATLAS_HORIZON` | same solver/resources + explicit atlas/horizon request/receipt interface: bind charts/overlaps, complete the `AtlasGluingReceipt` fields (status from the 4-member `GluingStatus`, witness id iff WITNESSED), `HorizonStatus` for probe proposals, `OUTSIDE_CURRENT_ATLAS` only with residual witness — i.e. the real `epistemic_atlas.py` API surface |

## 4. Runner and custody (mirror of the EL10 runner)

New `scripts/run_epistemic_atlas_suite.py` + `orion_ah20_cases.py` + `orion_epistemic_atlas_arms.py`,
structurally cloned from `scripts/run_epistemic_locality_suite.py` (541 lines) /
`orion_epistemic_locality_arms.py` / `orion_el10_cases.py`:

- `prepare` — seed 20260901 for the 30 new cases (per-case RNG derivation identical to EL10); EL10
  48 tasks copied verbatim; emits `public_tasks.json`, `private_oracle.json`, per-arm requests,
  `FROZEN_SUITE.json` (schema `orion.v2.ah20-freeze.v1`; arms, classes, seed, task_count=78,
  `private_oracle_visible_to_solver: false`, answer-contract string, authority flags, and the
  GR10/MX20 reuse-ledger rows incl. `CANNOT_REUSE__SUITE_NOT_FROZEN` if still unfrozen at dispatch).
- `dispatch` — sha256-commit `private_oracle.json` -> `PRIVATE_ORACLE_COMMITMENT.json` -> **unlink**
  -> run all arms with `ORION_GOLD_ACCESS=NONE` / `ORION_OUTCOME_ACCESS=NONE`; `finally` restores the
  oracle bytes and asserts hash equality; oracle reappearing mid-dispatch = hard error.
- `evaluate` — missing != wrong; per-arm metric vector; McNemar x Holm (§5); kill rule on point
  estimates (§6); `PER_TASK_SCORING.json` + `EVALUATION_SUMMARY.json`.
- `selftest` — no-model structural audit: oracle exactness and class balance; `class_id`/expected
  answers absent from public tasks; gluing-status balance across the 78; EL10 byte-equality check;
  winner-consistency audit (EL10-style, parsed from public text only) extended to gluing/probe
  consistency (the registered witness line for WITNESSED tasks must be present in public text, etc.).
- Executor pinned as in EL10: codex-cli `gpt-5.6-terra` (`ORION_EL_EXECUTOR=anthropic` fallback
  admissible for the whole suite only, never mixed per-arm within a run). Honest token overhead of
  any wrapper counts as `resource_cost`.

## 5. Metrics and statistical treatment (frozen definitions)

| backlog outcome | definition (denominator) | critical |
|---|---|---|
| `local_scope_correctness` | mean(correct stay-local decision + no global claim) over AHC0 + ELC1 (12) | no |
| `false_globalization_rate` | P(arm claims global/holds or WITNESSED or VALID transport-to-global &#124; oracle local / no witness) over AHC1 + ELC2-5, ELC8 (36) | **yes (non-compensatory)** |
| `gluing_disposition_correctness` | P(exact `GluingStatus` + witness-id discipline) over all 78 | yes |
| `transport_correctness` | 1 - P(transport=VALID &#124; oracle INVALID) over ELC2-5, ELC7, ELC8 (36) | yes |
| `probe_selection_correctness` | P(correct ADOPT/REJECT + correct probe id) over AHC2 + AHC3 (12) | yes |
| `decision_relevant_partition_refinement` | P(refinement splits exactly the decision-distinct pair / no spurious split) over AHC2 + AHC3 (12) | no |
| `false_outside_atlas_rate` | P(declares OUTSIDE_CURRENT_ATLAS &#124; registered explanation exists) over 72 non-sentinel tasks | **yes (non-compensatory)** |
| `resource_cost` | model_calls, tokens, wall-time from resource receipts | gate only |

Statistics (frozen, EL10-identical machinery): paired exact McNemar (two-sided binomial on
discordant pairs) on per-task protected-success indicators; contrasts
`F2_PLUS_ATLAS_HORIZON - {SIMPLE_NATIVE, CURRENT_F0, CURRENT_F2, PARENT_LOCAL_GLOBAL}` x
{gluing_disposition_correctness, false_globalization protected-success, transport protected-success,
probe_selection_correctness} = **16 tests, single family, Holm step-down, alpha 0.05**.
`false_outside_atlas_rate` is expected near-zero (rare events): reported as point estimate + exact
binomial 95% CI, enters the kill rule on point estimates, and is NOT in the McNemar family (frozen
decision — adding zero-discordance tests would only inflate the Holm family). Missing responses
(absent file, EXECUTION_FAILED*, unparseable) are missing, not wrong: they drop out of paired tests
and force `run_valid: false` + INDETERMINATE kill rule. If `PARENT_LOCAL_GLOBAL` has no faithful
implementation at dispatch, that arm is `CANNOT_CHECK` and its 4 contrasts are removed from the
family (12 tests), documented in the freeze record — never replaced by a weak substitute.

## 6. Kill rules (verbatim-proposed)

- **K1 (cost gate).** Compute per critical metric whether any other arm matches or beats
  `F2_PLUS_ATLAS_HORIZON`. If every other arm matches/beats it on ALL critical metrics AND
  `F2_PLUS_ATLAS_HORIZON` costs <= **1.10x the cheapest other arm** (`wall_time_seconds_sum`, as
  EL10) -> `INTERFACE_KILLED__CONTRACT_TO_DOCUMENTATION`.
- **K2 (protected residual).** If `F2_PLUS_ATLAS_HORIZON` is strictly better on >= 1 critical
  metric -> `INTERFACE_PROTECTED_RESIDUAL` (statistical support judged from the Holm table, not
  assumed).
- **K3 (non-compensatory strict-worse kill).** If `F2_PLUS_ATLAS_HORIZON` is strictly worse than
  `CURRENT_F2` or `PARENT_LOCAL_GLOBAL` on either non-compensatory rate (`false_globalization_rate`,
  `false_outside_atlas_rate`) -> `INTERFACE_KILLED__NON_COMPENSATORY` regardless of other metrics
  (protocol: false global-section claims and false OUTSIDE_CURRENT_ATLAS calls are
  non-compensatory).
- **K4 (null terminal).** Otherwise, if some other arm is strictly better on a critical metric and
  K1/K3 do not fire -> `F2_PLUS_ATLAS_HORIZON_STRICTLY_WORSE_ON_A_CRITICAL_METRIC__NULL_TERMINAL`.
  Parent win or null is a VALID terminal (`PARENT_SUFFICIENCY`).
- **K5 (indeterminacy).** Any missing response in any arm -> `INDETERMINATE_MISSING_RESPONSES`;
  kill rule not evaluable; missing != wrong.
- **Invariance sentinel.** If arms disagree materially on AHC0 (the control class), the run is
  reported `CONTROL_DIVERGENT` before any kill verdict — a null obtained while arms cannot even
  agree on the trivial class is not evidence about the interface.

## 7. What this freeze does NOT claim

No total epistemic space; no absolute globality; no global sheaf structure assumed; no K7 / new
kernel family; no P-A/P-B/P-D endpoint change; `OUTSIDE_CURRENT_ATLAS` carries no positive mechanism
content; pairwise compatibility never promotes to a global section; G4-style universality is only
ever relative to an explicit formal universe + theorem witness; sheaf/cohomology language is
parent-owned and receives zero ORION novelty credit; AH20 is a formal/interface discriminator only
and licenses no naturalistic claim (AH30 stays gated); parent sufficiency and CANNOT_CHECK are valid
terminals; results bind only the 78 synthetic worlds run, not any field status.

## 8. Design review resolutions (2026-08-30, applied at freeze)

1. **GR10/MX20 absence — RESOLVED: proceed EL10-only + deferred slots.** The backlog's global
   reuse rule is satisfied maximally by what exists: all 48 EL10 worlds verbatim; GR10/MX20 ledger
   rows written `CANNOT_REUSE__SUITE_NOT_FROZEN` at `prepare` AND re-checked at `dispatch`. If a
   GR10/MX20 suite freezes in between, worlds enter by oracle-identity match only (never re-dressed,
   never merged classes); otherwise the explicit CANNOT_REUSE row is the honest record. Holding AH20
   on suites that may never freeze would convert a required-reuse rule into an indefinite block —
   the deferred-slot mechanism is the reconciliation.
2. **PARENT_LOCAL_GLOBAL binding — RESOLVED: one federation, both components.** The arm carries
   decision-theoretic OED probe selection AND an explicit sheaf-style gluing check as its two
   components; which component applies is decided inside the wrapper per episode; where neither
   binds the arm answers `CANNOT_CHECK`. No per-episode arm switching outside the wrapper (arms must
   stay comparable — one wrapper identity per suite).
3. **Budget — RESOLVED: keep 78 x 5 = 390.** The 12-task denominators (AHC0+ELC1, AHC2+AHC3) are
   the minimum at which the exact McNemar discordance machinery has any power; trimming new classes
   to 4 cases each (denominator 8) would gut the paired tests AH20 exists to run. All 390 jobs are
   bounded synthetic-registry prompts (no tool use, no long chains), inside `LOW_COST_PROSPECTIVE`.
4. **`decision` on atlas-native classes — RESOLVED: `NOT_APPLICABLE` on AHC1-AHC4.** The absence of
   a method registry in those worlds is part of the world, not an omission; retrofitting a local
   decision to every class would inflate `local_scope_correctness` with decisions the generator
   never seeded. AHC0 keeps its seeded local decision; the §5 denominator (AHC0 + ELC1 = 12) stands,
   and `decision=NOT_APPLICABLE` is scored as the exact expected value on AHC1-AHC4.
5. **ELC6 mapping — RESOLVED: `GLOBAL_SECTION_OBSTRUCTED` stands.** The criteria in ELC6 are fully
   registered — the correspondence is not missing, it exists and is jointly unsatisfiable (the
   Pareto frontier with no registered exchange rate IS the obstruction witness). `CANNOT_CHECK` is
   reserved for absent correspondence (ELC7's two-substrate case), and spending it here would erase
   the local-to-global obstruction class the suite is named for.
6. **Executor pinning — RESOLVED: single primary, whole-suite fallback rule retained.** Primary =
   codex-cli `gpt-5.6-terra` exactly as EL10. The anthropic fallback may fire only if the primary
   channel is dead BEFORE any arm starts (whole-suite switch, recorded in
   `FROZEN_SUITE.json.executor_note`); never mid-run, never per-arm — a mixed-executor run is
   `run_valid: false` by construction.
