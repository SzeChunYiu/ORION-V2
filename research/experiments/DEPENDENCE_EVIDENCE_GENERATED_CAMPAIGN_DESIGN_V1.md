# P-D Decisive Study Design V1 — Dependence-Aware Evidence Generated Campaign

**Status:** DESIGN_ONLY — PROSPECTIVE_EXECUTION_PLAN_NO_RESULTS. No experiments run, no
code pushed, no PRs opened. This document grants nothing (see footer).
**Owner paper:** `v2-papers/P-D-dependence-aware-evidence/` (manuscript V4, programme
contract §9 of `TOP_TIER_PAPER_COMPLETION_PROGRAMME_V1.md`).
**Pattern parent:** FM/FG generated campaign (`research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json`
+ `scripts/run_formal_discovery_generated_suite.py` in `SzeChunYiu/ORION-V2`).

## 1. Purpose

Programme §9 defines P-D's decisive evidence: duplicate/shared-source vs genuine-independent
controls, assumption-level dependence, criticism uptake, assurance+argumentation parent
product, oracle/test-sensitivity failures, performative cases, authority boundaries,
selective reopening, blinded adjudication, cost/over-conservatism controls. This design
converts that list into a frozen, mechanically scored generated campaign in the FM/FG
style: synthetic evidence corpora with **dependence structure known by construction**
(latent shared sources, propagation trees, correlated failure modes), so false
corroboration and false authority are exactly quantifiable, and every task asks for a
**protected decision** under a registered decision rule.

Thesis under test (programme §9): support-family + dependence + argument + test/oracle
adequacy + evaluator-response modelling prevents false corroboration and false authority
while preserving genuine independent support better than vote count, provenance, and the
strongest assurance parents. Strongest threat: parent sufficiency.

## 2. Studies (claim spine → 4 generated studies)

| ID | Manuscript slots | Protected decision (exact-match enum) | Tasks |
|---|---|---|---|
| PD-S1 DEPENDENT_CORROBORATION | PD-R1, PD-R2 | `ACCEPT_H / REJECT_H / INCONCLUSIVE_INSUFFICIENT_INDEPENDENT_SUPPORT` + `independent_support_family_count` | 160 |
| PD-S2 ARGUMENT_AND_ADEQUACY | PD-R3, PD-R4 | `SUPPORTED / DEFECT_CIRCULAR / DEFECT_FALSE_PREMISE / DEFECT_STRICT_EXPORT / DEFECT_COMPONENT_GAP / CANNOT_CHECK_TEST_INADEQUATE` | 120 |
| PD-S3 REVOCATION_AND_UPTAKE | PD-R5, PD-R6 (PD-R7 strata) | `reopened_claim_ids`, `preserved_claim_ids`, `objection_outcomes` map | 120 |
| PD-S4 AUTHORITY_AND_RESPONSE | PD-R8, PD-R9 | authority: `REPORT_ONLY / CONDITIONAL_ACTION_AUTHORIZED / REFUSE_AUTHORITY_VIOLATION`; response: `REMAINS_VALID / INVALIDATED_BY_RESPONSE / STABLE_CONTROL_VALID` | 120 |

Total 520 tasks. PD-S3 answer keys are sorted ID lists + enum map (FM10's exact
`node_map` precedent: exact-match on structured answers is the suite norm).

## 3. Corpus construction (ground truth by construction)

**PD-S1.** Generator samples a latent source tree: `k` root sources (data, model,
instrument, assumption, calibration); each emits evidence items via explicit propagation
edges; support families are constructed so the number of **independent singly-sufficient
families** is exact. Item text carries provenance (lineage IDs, replay hashes — visible)
plus natural-language method descriptions in which shared assumptions/calibrations are
stated but never labelled as shared (latent; inferable only by reading). Registered
decision rule ships in the public task (e.g. "ACCEPT_H iff ≥3 independent sufficient
families and no surviving defeater"), so truth is mechanical. Strata (40 each, recorded
**only in the private oracle**, never in the task body):
- S1a dependent-corroboration negative — planted shared latent source/assumption;
  naive counting accepts; truth `INCONCLUSIVE` (or `REJECT_H` when a defeater survives);
- S1b genuine-independent positive control — truth `ACCEPT_H`; measures preservation;
- S1c provenance-visible duplicates — exact lineage identity; cheap parents should
  catch (parent-sufficiency probe);
- S1d insufficient-evidence baseline — few items; truth `INCONCLUSIVE`.

**PD-S2.** Assurance-case bundles: claim, argument graph, premises, strict/defeasible
rules, evidence, `TestSensitivityProfile` / `OracleAdequacyProfile`. Strata:
formally-acceptable-but-scientifically-defective (false premise, strict export of a
defeasible step, component gap — argumentation parent ACCEPTs by construction);
formally-defective (circular support, attack cycle); test-inadequacy (passing test
provably blind to the registered error class → `CANNOT_CHECK_TEST_INADEQUATE`); clean
positive control.

**PD-S3.** Support-family hypergraphs + events. Revocation tasks: item/relation/evaluator
failure with (i) surviving alternative family (truth: preserved), (ii) sole family lost
(truth: reopen), (iii) unrelated-family failure (control: no reopen). Distributed-handoff
strata (PD-R7): a warning lost at a named actor boundary reopens the dependent claim.
Objection tasks: matched criticism with planted target validity → `REVISION_REQUIRED /
OBJECTION_REJECTED / LOGGED_WITHOUT_CHANGE` (theatre trap: objection cites a
tangential assumption; correct outcome is rejection/log, not revision).

**PD-S4.** Authority tasks: evidence supports a claim but the requested action
(deploy/publish/allocate) lacks an external authorization root (`REFUSE`); conditional
actions with an explicit external root (`CONDITIONAL_ACTION_AUTHORIZED`). Response tasks:
post-intervention environments (benchmark publication + optimization, adaptive
adversary, policy response) where the planted response invalidates the static pass;
stable non-performative controls (false-alarm control).

## 4. Arms

Core (all studies): `CURRENT_INDEPENDENT_COUNTING`, `PROVENANCE_TRACKING`,
`STANDARD_DEPENDENCE_META_ANALYSIS`, `ARGUMENT_ACCEPTABILITY`,
`STRONGEST_ASSURANCE_FEDERATION` (F0-analogue: provenance + argumentation + dependence
graph + severe testing configured together), `P_D_FULL`, `P_D_MINUS_DEPENDENCE`
(plant-title ablation), `SIMPLE_DIRECT_CONTROL`. Study-specific:
`ROBUSTNESS_TRIANGULATION_PARENT` (PD-S1), `PERFORMATIVE_SECURITY_PARENT` (PD-S4).

Execution modes:
- **Deterministic offline, zero model calls** (algorithmic parents, per FM/FG
  precedent): counting (item votes vs registered threshold), provenance (lineage dedup
  then distinct-lineage count), meta-analysis (declared-correlation pooling), argument
  acceptability (grounded/preferred-extension labelling of the supplied AF),
  simple control (fixed heuristic). Their failure rates are **constructed, not
  discovered** — they quantify exactly how much false corroboration each cheap rule
  suffers; the empirical content is whether the model arms beat that ceiling.
- **Model arms** (judgment over latent dependence/adequacy text): codex `exec
  --ephemeral` via `ORION_CODEX_BIN` / `ORION_CODEX_MODEL` (default `gpt-5.6-terra`,
  matching FM/FG for cross-campaign comparability), one call per task, read-only
  sandbox, `--output-schema` JSON contract: `STRONGEST_ASSURANCE_FEDERATION`,
  `P_D_FULL`, `P_D_MINUS_DEPENDENCE`, `ROBUSTNESS_TRIANGULATION_PARENT`,
  `PERFORMATIVE_SECURITY_PARENT`.

Model-arm volume: 520×3 core + 160 + 120 = **1840 codex calls**; offline arms 2600 jobs,
0 calls. All arms receive matched public information; no arm sees strata or oracle.

## 5. Oracle and scoring

Reuse the suite mechanism unchanged in spirit and in code path: `prepare()` writes
`public_tasks.json` + `private_oracle.json` (`{answers, strata}`) + `FROZEN_SUITE.json`;
`dispatch()` hash-commits the oracle (`PRIVATE_ORACLE_COMMITMENT.sha256`), **deletes it
for the entire child dispatch**, aborts if it reappears, restores and hash-checks after
(`oracle_restored_hash_match`); `evaluate()` is exact-match `canon(actual)==canon(expected)`
per required key, emitting `EVALUATION_ROWS.json` / `EVALUATION_SUMMARY.json` with
all-false `authority` flags. PR #72 truth gates inherited verbatim: any
missing/`EXECUTION_FAILED`/null answer → `{"missing": true}` row, per-arm `run_valid`,
campaign `all_runs_valid`, driver exit 3 + `CAMPAIGN INVALID`; a null run can never
render as accuracy-0.0 verdicts.

PD analysis step (new, reads restored oracle + rows): joins strata, computes per-stratum
confusion, false-corroboration rate (arm accepts on S1a), independent-support
preservation (arm accepts on S1b), false-authority rate (arm authorizes on REFUSE
stratum), reopening precision/recall, false-performativity alarms, per-arm protected-
decision accuracy, per-arm resource receipts.

## 6. Metrics, estimands, statistics

Primary (frozen): false-corroboration rate; false-authority rate; independent-support
preservation; per-arm protected-decision accuracy (all studies). Secondary: reopening
precision/recall; defect-correction rate; weak-pass/overreach detection; false
performativity alarms; unresolved-state correctness; over-conservatism (refusals on
positive controls); cost (model calls, wall time) — feeding the resource-adjusted
Pareto (PD-R10 partial: FULL vs MINUS_DEPENDENCE vs parents only).

Paired design (same tasks across arms) → McNemar on discordant pairs per stratum;
task-level bootstrap 80% CIs; no pooling across strata with incompatible semantics
(manuscript rule); hard authority/integrity failures non-compensatory (any
REFUSE-stratum authorization by P_D_FULL caps the arm at failed regardless of other
scores). Stochastic model arms: 3 repeats on a 20% sub-sample per study (repeat
agreement reported; repeats are not independent replication — plan rule kept).

## 7. Powering

Paired proportions: detecting a 12-point difference (e.g. discordance 0.15 vs 0.03) at
α=0.05 two-sided, 80% power needs n ≈ (1.96+0.84)²·(0.18)/(0.12)² ≈ 98 tasks/stratum
pair. 160 tasks (4×40 strata) powers PD-S1's primary contrasts with margin; 120
(4×30 strata) powers the 15–20-point contrasts expected in PD-S2/S3/S4. If any primary
contrast's observed discordance falls below the powered band, the pre-registered
fallback is a second seeded instantiation of that study (new seed, same frozen
generators) rather than widening claims — "multiple studies if the claim spine needs
more" is satisfied by instantiation, not by post-hoc pooling.

## 8. Kill / merge contract (pre-registered)

Terminal `PARENT_SUFFICIENCY` — P-D contracts to a reference implementation /
traceability-evaluation resource or merges into the flagship (programme §9) — if any of:
1. PD-S1: `STRONGEST_ASSURANCE_FEDERATION` matches `P_D_FULL` on false-corroboration
   rate AND preservation within the CI overlap across all four strata (parents already
   make the same decisions); or
2. PD-S1: `P_D_FULL` fails to beat the best of the deterministic cheap arms
   (`CURRENT_INDEPENDENT_COUNTING`, `PROVENANCE_TRACKING`, their union) on the
   false-corroboration/preservation pair (≥12-point paired difference not met); or
3. PD-S1: `P_D_MINUS_DEPENDENCE` ≈ `P_D_FULL` (dependence modelling adds nothing
   measurable — kills the title concept); or
4. PD-S2 + PD-S4: `P_D_FULL` commits any hard authority failure or misses the
   formally-acceptable-but-defective stratum at the parents' rate (integration adds no
   cross-parent value).
Survival requires ALL of: (1)–(4) false, over-conservatism bound met (preservation
≥90% of S1b accepts), and cost within 3× the cheapest parent achieving half the
improvement. Ambiguity (`CANNOT_CHECK` dominant, repeat disagreement) →
`CANNOT_CHECK` terminal, not quiet survival.

## 9. Execution plan

Artifacts (all new files in `SzeChunYiu/ORION-V2`, one PR, no edits to the frozen FM/FG
suite):
- `research/experiments/DEPENDENCE_EVIDENCE_GENERATED_CAMPAIGN_PLAN_V1.json` —
  `orion.v2.dependence-evidence-generated-campaign-plan.v1`, status
  `PROSPECTIVE_EXECUTION_PLAN_NO_RESULTS`, owner_issue 50 (shared generated-campaign
  tracker), seed frozen at prepare (20260903), `max_concurrency_default: 2`, studies
  block as §2, rules copied from FM/FG (`private_oracle_absent_during_model_calls`,
  `same_model_repetitions_are_independent_replication: false`,
  `generated_results_alone_grant_real_world_evidence_claims: false`,
  `parent_sufficiency_is_valid_terminal: true`), authority block all-false.
- `scripts/run_dependence_evidence_generated_suite.py` — PD generators + PD `prepare`
  (PD request schema `orion.v2.dependence-evidence-request.v1`, strata into private
  oracle) + `analyze`; **imports the FM/FG suite module** and reuses its `write_json/
  read_json/digest/canon/answer_shape/token` and calls its `dispatch()`/`evaluate()`
  unchanged.
- `scripts/orion_pd_arms.py` — one process per request; routes offline arms to local
  deterministic implementations, model arms to codex exec (same failure envelope as
  `orion_formal_discovery_arms.py`, `model_calls: 0` on failure). Wired in via the
  existing `ORION_FORMAL_ARM_COMMAND` override — zero changes to suite dispatch.
- `scripts/run_dependence_evidence_campaign.sh` — single command:
  `ORION_CODEX_BIN=... bash scripts/run_dependence_evidence_campaign.sh all`
  (prepare → dispatch → evaluate → analyze). `ORION_PD_OFFLINE_ONLY=1` runs the
  deterministic arms + oracle-hiding machinery today as a smoke/null-run test;
  model arms launch once the backend is live (window opens Sep 3; codex pinned
  0.129.0-alpha.15). Dispatch and evaluation must run on laptop billy / billy-old per
  the no-CI-on-Mac-mini rule; the campaign is a billy-old/laptop workload, not CI.

Run order: smoke (offline-only, oracle hide/restore verified) → full dispatch (concurrency
2) → evaluate + analyze → results block into P-D manuscript V5 results slots with the
frozen sentence forms → kill/merge decision recorded in the same PR.

## 10. Honest limits (frozen before results)

- Dependence is **planted, not discovered**: this certifies decision rules under known
  ground truth; it cannot certify detection of hidden dependence in real scientific
  record.
- Evidence text is schematic; semantic difficulty ≠ real literature. No claim to
  real-world scientific evidence graphs or naturalistic ground truth.
- Offline parents' failure rates are constructed quantities (calibration ceiling), not
  empirical discoveries; only the model arms carry empirical content.
- Model arms are epoch- and model-bound (`ORION_CODEX_MODEL`); results do not transport
  across models without a new evaluation identity.
- Authority/governance cases are stylized; legitimacy in real institutions cannot be
  standardized (manuscript limitation kept).
- Performative cases simulate response mechanically (planted post-intervention
  invalidation), not true strategic adaptation.
- Exact-match under-credits partially correct reasoning; the protected-decision focus
  mitigates but does not eliminate this.
- Dependence-annotation burden on real corpora is not measured by this design.
- Any null/invalid run (PR #72 gates) terminates in `CAMPAIGN INVALID`, never in
  accuracy-0.0 conclusions.

```text
PD_DECISIVE_STUDY_DESIGN = FROZEN_PROSPECTIVE_NO_RESULTS
POSSIBLE_TERMINALS = PD_SUPPORTED__PARENT_SUFFICIENCY__CONTRACT_TO_RESOURCE__MERGE_INTO_FLAGSHIP__CANNOT_CHECK
GRANTS_SCIENTIFIC_TRUTH = false
GRANTS_REAL_WORLD_EVIDENCE_GRAPH_CLAIMS = false
GRANTS_R3_OR_R4 = false
```

*This design document confers no paper identity, novelty, scientific truth, publication
authority, or result status. Working design only; authority stays with the ORION-V2
freeze ledgers and completion receipts.*
