# PRA Real-LLM Audit — Pre-registered Design V1 (frozen before any protected run)

**Issue:** #51 · **Lineage:** Protocol V2 §16 optional frozen-LLM extension, executed
under Protocol V3 semantics, CR-02/CR-03/CR-07/CR-08, the compatibility criterion and
the prediction-channel scope note. **Machine-readable twin:** `PRA_REAL_LLM_AUDIT_DESIGN_V1.json`
(`schema_version orion.v2.pra.real-llm-audit-design.v1`). **Class:** prospective empirical
extension; freeze precedes run (m-series discipline). **Scientific authority:** none; the
manuscript is not modified by this design and gains nothing automatically from its outcome.

## 1. Question

> After a frozen open-weight instruct model is matched, per episode, on the registered
> linguistic target (status-line continuation under `rho`) and on the current contract
> action, does removing the dormant `support_source` variable from its representation
> state — while verifying removal across the KV and hidden-activation channels — produce
> the predicted revision failure after the same later evidence, and does restoring only
> that variable (R3) repair it?

The hostile review names `REAL_LLM_EMPIRICAL_SUPPORT = ABSENT_BY_DESIGN` as the decisive
JMLR weakness. This design is the only licensed route to an empirical bridge: a
pre-registered execution of the audit sequence current target → current equivalence →
state contrast → reconstruction/alternate-channel check → common later evidence →
compatibility and behaviour. It cannot establish that deployed LLMs generally fail; it
can establish, for two models and one fixture family, whether the no-certification gap
is realised on a real representation surface.

## 2. Frozen inputs

- **Models** (bf16, one A100, greedy, `max_new_tokens=8`, seed 51, batch 1):
  `Qwen/Qwen2.5-7B-Instruct @ a09a35458c702b33eeacc393d103063234e8bc28`,
  `mistralai/Mistral-7B-Instruct-v0.3 @ c170c708c41dac9275d15a8fff4eca08d52bab71`.
  Two families so no result is single-model; both ungated, Apache-2.0.
- **Registered scope (CR-07 fields):** `rho` = registry status line; present target =
  teacher-forced mean per-token log-prob of `Claim <id> is currently listed as SUPPORTED.`;
  current responsibility = contract `{RETAIN, REOPEN, ESCALATE}` under any-optimal-action
  semantics with 0/1 loss; future evidence family = exogenous registry notices delivered
  identically to every condition; future responsibility = same contract after the notice.
- **Suite generator** (`generate-suite`): templated fictitious scientific claims over 8
  domains; three episode-local nonce sources per instance (invented surname + year +
  registry code — Gate D parametric control); 2 arms per instance. Seeds: dev
  `20260902`, protected `20260903`. Counts (protected, 500 instances / 1000 arms):

  | family | n | role | gold after evidence |
  |---|---|---|---|
  | F0_ACQ | 40 | acquisition ceiling: record does not say which source supports C | ESCALATE both |
  | F1_P0 | 60 | zero-extra-state control (direct refutation / admin notice) | REOPEN both / RETAIN both |
  | F2_P1 | 60 | current cross-channel: buried withdrawal notice | current RETAIN vs REOPEN |
  | F3_P2_CANON | 120 | canonical §5 fixture, unique current action RETAIN, `RETRACT(A)` | hA REOPEN vs hB RETAIN |
  | F3_P2_MIRROR | 60 | unrelated-source retraction `RETRACT(Z)` | RETAIN both |
  | F3_P2_INDEP | 60 | independent sufficient supports, `RETRACT(A)` | hAB RETAIN vs hA REOPEN |
  | F3_P2_RECON | 60 | evidence carries the support annotation (negative control) | annotation-determined |
  | F3_P2_TIE | 40 | expression of concern (tie semantics) | hA {ESCALATE,REOPEN} vs hB {RETAIN,ESCALATE} |

  Dev split: 4 per family (32); the smoke uses at most 8 (one per family).
  The protected suite is generated once, sha256-frozen, and never inspected before
  authorization; the runner refuses the protected split without the design token.
- **Representation conditions** (all deterministic templates, never model-written):
  R0 complete numbered history; R1 prediction-preserving summary (claim, source roster,
  status line — collapses `support_source` and `current_defeat`); R2 current-decision
  state (claim, current support validity, status line); R3 = R2 + recorded support;
  R4 = R2 + full dependency ledger (Protocol V3 controlled-future control).
  Token budget matched per (instance, arm): every condition padded with the frozen filler
  line to the R0 token count (tolerance 4 tokens); padding counts are logged.
- **Alternate-channel conditions on F3_P2_CANON:** `R2_TEXT_REMOVED_KV_RETAINED`
  (unpadded R0 state forwarded with `use_cache=True`, its `past_key_values` retained,
  the R2-based prompt continues from that cache — the MEMENTO-style survival channel) and
  `R2_TRUE_REMOVAL` (fresh cache). Representation cost = retained tokens.
- **Probe (Gate A):** mass-mean difference-direction linear probe on the last prompt
  token of the pre-evidence current-action prompt, every layer, label `support_source`;
  train = first 60 % of instances in frozen order, test = remainder; max-over-layers test
  accuracy is the gate statistic. Frozen before any revision outcome is read.
- **Gate B (causal use / activation patching):** omitted prospectively →
  `CANNOT_CHECK_ALTERNATE_CHANNEL_CAUSAL_USE` is recorded in every rollup.

## 3. Statistics

- Independent unit = instance (episode). Primary test for every contrast: exact McNemar
  (two-sided binomial on discordant pairs) at instance level (instance correct iff every
  arm correct); arm-level McNemar reported as nested secondary. Wilson 95 % intervals.
- Present equivalence: paired TOST on `logprob(R3) − logprob(R2)` with frozen margin
  0.05 nats/token (90 % CI inside ±margin); per-unit tolerance 0.15 nats/token.
  Non-significance is never read as equivalence.
- Metrics per family × condition: update accuracy, maintain accuracy, false-revision
  rate, missed-revision rate, current-action correctness, retained tokens, unparseable
  count. Certificates (CR-02/CR-03): per (instance, condition) cell — arms whose
  rendered state+evidence coincide — joint acceptable-set intersection; **incompatible
  cell rate is the primary structural metric**, pairwise disjoint collisions secondary.
  The three-history `{a,b},{b,c},{a,c}` control is re-executed in every rollup.
- Power (registered honesty): under greedy decoding the hA/hB prompts are identical
  under R2, so instance-level R2 accuracy on F3_P2_CANON is 0 by construction; contrast B
  therefore tests whether R3 reaches instance accuracy ≥ 0.15 (exact binomial, α 0.05,
  power > 0.99 at R3 = 0.70). Arm-level MDE for paired McNemar at 20–30 % discordance is
  0.11–0.14 accuracy points. Control families (n = 60) resolve |gap| ≳ 0.16–0.20, so
  the 0.10 control bound is a registered bound, not a demonstrated null.

## 4. Gates (frozen pre-outcome; thresholds live in the JSON)

- **GP0 present equivalence (F3_P2_CANON):** per unit |Δlogprob| ≤ 0.15, current action
  identical across R0/R2/R3 and correct, budgets matched; pass fraction ≥ 0.90 AND TOST
  equivalent. Fail → `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE`.
- **GP1 R3 > R2 on P2 (load-bearing contrast B):** instance-level exact McNemar
  p ≤ 0.05 with positive direction AND arm-level gain ≥ 0.15, in **both** models.
  R3 arm-level accuracy ≥ 0.70 separates `NO_MECHANISM_EFFECT` from
  `ORDINARY_REASONING_FAILURE_DESPITE_RETAINED_STATE`.
- **GP2 alternate channel.** GP2a (required): probe decodes under R0 (≥ 0.80), is at
  chance under `R2_TRUE_REMOVAL` (≤ 0.65), and true-removal accuracy sits ≥ 0.15 below
  R0 → `INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION`; otherwise
  `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`; probe positive control failing →
  `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`. GP2b (control quality, contrast D): probe
  decodes under KV-retained (≥ 0.80), KV-retained accuracy ≥ R0 − 0.10, p ≤ 0.05;
  otherwise the survival control is reported as not reproduced / retained-but-not-used.
- **GP3 controls:** F1_P0 |R2−R3| ≤ 0.10; F3_P2_RECON |R2−R3| ≤ 0.10; F3_P2_MIRROR
  false-revision rate under R3 ≤ 0.10. Any failure →
  `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE`.
- Secondary, reported not gated: contrast A (R1 vs R2 current action on F2_P1), contrast
  C (R3 vs R0), contrast E (R3 vs R4), F0_ACQ R0 accuracy (acquisition ceiling),
  F3_P2_TIE compatible-cell behaviour, F3_P2_INDEP selective reopening.

## 5. Pre-registered routing

| outcome | terminal | route |
|---|---|---|
| GP0 ∧ GP1 ∧ GP2a ∧ GP3 in both models | `P2_PROSPECTIVE_REVISION_STATE_REQUIRED__BOTH_MODELS` | manuscript MAY gain ONE registered empirical section under a NEW manuscript version and NEW freeze; never automatic |
| passes in one model only | `P2_SINGLE_MODEL_ONLY__REGISTERED_BOUNDARY_RESULT` | reported as boundary result; no section |
| GP0 fail | `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` | registered negative on the surface, not on the theory |
| GP1 fail, R2 and R3 both ≥ 0.85 | `P0_CURRENT_AND_PROSPECTIVE_SUFFICIENT` | valid negative (P0-dominated) |
| GP1 fail, R3 < 0.70 | `ORDINARY_REASONING_FAILURE_DESPITE_RETAINED_STATE` | registered negative; §16 distinction preserved |
| GP2a fail | `INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION` / `CANNOT_CHECK_…` | no P2 attribution; scope to excluded channels |
| GP3 fail | `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE` | fix only under a new design version and fresh protected seed |

Falsifiers §17 map as: (1) GP0; (2) GP2a/probe; (3) F3_P2_RECON; (4) F0_ACQ ceiling;
(5) GP1; (6) token-budget matching + retained-token cost; (7) R4/contrast E; (8) P0 terminal.

## 6. Controls and leakage

Nonce identities, domain rotation, identical evidence text across arms (except RECON,
where the annotation is the control), unrelated-evidence mirror, independent-support
selective reopening, P1 current-visible control, future-evidence-reconstructs control,
KV survival and true-removal controls, matched token budget, full-history ceiling,
three-history joint-intersection control, deterministic decoding frozen. Unit tests
(`tests/unit/test_pra_real_llm_audit.py`) run every stage on a stub backend: a planted
contract-follower must trip GP1/GP2a/GP2b, a constant-RETAIN null must not; the frozen
suite refuses tampering; the protected split refuses execution without the token.

## 7. Custody

- Runner `research/llm-machine-epistemics/pra_real_llm_audit.py`; sha256 recorded in
  the PR, in every receipt and in the rollup. Design JSON sha256 likewise.
- Every model call logs prompt sha256, raw completion, parsed action, status-line
  log-probs, token counts; hidden states are dumped as float16 arrays per condition.
- LUNARC results root `/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/campaign-pra-llm-r1/`
  (`dev-smoke/` now; `protected/` only after authorization). Rollup
  `PRA_REAL_LLM_AUDIT_ROLLUP_V1.{json,md}` archived under
  `research/llm-machine-epistemics/results/pra-llm-r1/`.
- Environment: `PRA_REAL_LLM_AUDIT_ENV_RECEIPT_V1.md`; sbatch `sbatch/pra_llm_dev_smoke.sbatch`
  (run) and `sbatch/pra_llm_r1.sbatch` (not run; `--time` sized from the smoke).

## 8. Non-goals / no-rescue clause

This design measures ONE thing: whether the registered dormant variable is necessary
for correct revision on a frozen-LLM surface after present equivalence and channel
removal are verified. No result here upgrades the theorem, the P0/P1/P2 taxonomy or the
parent contraction. No post-hoc change to families, counts, prompts, filler, tolerances,
probe split, gate thresholds or terminal mapping. A defect found after unblinding is
reported as `CANNOT_CHECK` for the affected component and repaired only under Design V2
with a fresh protected seed. Gate B remains `CANNOT_CHECK` unless a later design adds it.

## 9. Ambiguities resolved at freeze

- Protocol V2 §16 is executed under V3 semantics (equivalence margins, R4, parametric
  Gate D, instance as independent unit) because status V9 names V3 canonical.
- "KV retained, text removed" for a frozen model is realised literally (prefix
  `past_key_values` kept, R2 text continues); informationally this equals leaving the R0
  segment attendable, which is precisely why visible deletion is not removal.
- The probe positive control is R0 (R3 is reported); GP2 hinges on true removal.
- ESCALATE is the registered acceptable action for the acquisition-limit family and
  one of two acceptable actions in the tie family; under R2 an ESCALATE on a
  determinable case counts as a maintain/update failure, not as a revision.
- The design JSON, not this note, is authoritative for numeric thresholds.
- Dev-split iterations before freeze (recorded, never repeated post-freeze): smoke 1 —
  Mistral tokenizer needed `protobuf`/`sentencepiece`; smoke 2 — bare one-word answers
  left both models incompetent even under R0 and filler-line padding matched budgets
  only to 16 tokens → brief-reasoning-then-`Answer:` format, sharpened contract rules,
  exact token top-up; smoke 3 — with the roster line "Sources on file: A, B, Z" both
  models treated a retracted non-basis source as support under R0 → the complete
  history and R3 state now say explicitly that no other source is a recorded basis.
  Gate thresholds, families, counts and seeds were never changed across iterations.
- Registered risk from the final smoke (4 dev instances, not evidence): both 7B models
  still over-revise the maintain arm under R0 in most cases. The design is frozen
  regardless; that outcome maps to `ORDINARY_REASONING_FAILURE_DESPITE_RETAINED_STATE`
  (a competence boundary of the surface, not a prospective-state result), and the
  contingency is Design V2 with larger frozen models under a fresh protected seed.
